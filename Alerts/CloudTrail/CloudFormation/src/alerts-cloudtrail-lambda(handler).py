import json
import os
import logging

import urllib.request
import urllib.error
from botocore.exceptions import ClientError
from boto3 import client as boto3_client

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Inicialização dos clients boto3
ssm_client = boto3_client('ssm')
org_client = boto3_client('organizations')
sns_client = boto3_client('sns')


# Parâmetros de ambiente (não logar secrets)
SLACK_PARAM_NAME = os.environ.get('SLACK_WEBHOOK_PARAM_NAME')
SNS_TOPIC_ARN = os.environ.get('SNS_TOPIC_ARN')
if not SLACK_PARAM_NAME:
    logger.warning('SLACK_WEBHOOK_PARAM_NAME não definido.')
if not SNS_TOPIC_ARN:
    logger.warning('SNS_TOPIC_ARN não definido.')

_slack_webhook_cache = None


# Função para obter o webhook do Slack
def get_slack_webhook():
    global _slack_webhook_cache
    if _slack_webhook_cache:
        return _slack_webhook_cache
    if not SLACK_PARAM_NAME:
        logger.error('Variável de ambiente SLACK_WEBHOOK_PARAM_NAME não definida.')
        raise RuntimeError('SLACK_WEBHOOK_PARAM_NAME não definida.')
    try:
        response = ssm_client.get_parameter(Name=SLACK_PARAM_NAME, WithDecryption=True)
        _slack_webhook_cache = response['Parameter']['Value']
        return _slack_webhook_cache
    except ClientError as e:
        logger.error('Erro ao buscar webhook do Slack no SSM: %s', e)
        raise RuntimeError('Falha ao recuperar o webhook do Slack. Verifique o parâmetro no SSM.')


def publish_to_sns(subject: str, message: str):
    if not SNS_TOPIC_ARN:
        logger.error('Variável de ambiente SNS_TOPIC_ARN não definida.')
        raise RuntimeError('SNS_TOPIC_ARN não definida.')
    try:
        sns_client.publish(
            TopicArn=SNS_TOPIC_ARN,
            Subject=subject,
            Message=message
        )
    except ClientError as e:
        logger.error('Erro ao publicar mensagem no SNS: %s', e)
        raise RuntimeError('Falha ao publicar mensagem no SNS.')


# Função para enviar mensagens ao Slack
def send_to_slack(webhook_url: str, message: str):
    data = json.dumps({'text': message}).encode('utf-8')
    req = urllib.request.Request(webhook_url, data=data, headers={'Content-Type': 'application/json'})
    try:
        with urllib.request.urlopen(req) as resp:
            logger.info('Notificação enviada ao Slack. Código HTTP: %s', resp.getcode())
    except urllib.error.HTTPError as e:
        logger.error('Erro HTTP ao enviar notificação ao Slack: %s', e)
        raise
    except urllib.error.URLError as e:
        logger.error('Erro de conexão ao enviar notificação ao Slack: %s', e)
        raise


def get_account_name(account_id: str) -> str:
    """Obtém o nome da conta AWS pelo ID."""
    try:
        response = org_client.describe_account(AccountId=account_id)
        return response['Account']['Name']
    except ClientError as e:
        logger.warning('Não foi possível obter o nome da conta: %s', e)
        return account_id


# Função para tratar eventos do CloudTrail
def lambda_handler(event, _context):
    detail = event.get('detail', {})
    event_name = detail.get('eventName')

    # Log do evento recebido (sem dados sensíveis)
    safe_event = {k: v for k, v in event.items() if k != 'detail'}
    logger.debug(f'Evento recebido (safe): {safe_event}')

    if event_name not in ('StopLogging', 'DeleteTrail', 'UpdateTrail'):
        logger.info('Evento ignorado: %s', event_name)
        return {'ignored': True}

    req = detail.get('requestParameters') or {}
    trail_name = req.get('name', 'desconhecida')
    region = detail.get('awsRegion', 'desconhecida')
    account_id = detail.get('recipientAccountId', 'desconhecida')
    account_name = get_account_name(account_id)
    user = (detail.get('userIdentity') or {}).get('arn', 'desconhecido')
    time = detail.get('eventTime', 'desconhecido')

    text_lines = [
        '🚨 *CloudTrail – ação crítica detectada!*',
        '',
        f'- *Ação*: `{event_name}`',
        f'- *Trail*: `{trail_name}`',
        f'- *Conta*: `{account_name}` (`{account_id}`)',
        f'- *Região*: `{region}`',
        f'- *Usuário*: `{user}`',
        f'- *Quando*: `{time}` (UTC)'
    ]
    text = '\n'.join(text_lines)

    # Envia alerta ao Slack
    try:
        webhook = get_slack_webhook()
        send_to_slack(webhook, text)
    except Exception as e:
        logger.error('Erro ao enviar Slack: %s', e)
        text = f'{text}\n\nWARNING: Failed to deliver to Slack: {str(e)}'

    # Publica alerta no SNS
    try:
        publish_to_sns('[ALERTA] CloudTrail', text)
    except Exception as e:
        logger.error('Erro ao publicar no SNS: %s', e)
        return {'error': 'SNS publish failed', 'details': str(e)}

    return {'ok': True}
