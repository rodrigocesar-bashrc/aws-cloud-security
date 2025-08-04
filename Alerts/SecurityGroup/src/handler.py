import json
import os
import logging
import urllib.request
from botocore.exceptions import ClientError
from boto3 import client as boto3_client

ssm_client = boto3_client('ssm')
org_client = boto3_client('organizations')

SLACK_PARAM_NAME = os.environ['SLACK_WEBHOOK_PARAM_NAME']
SNS_TOPIC_ARN = os.environ.get('SNS_TOPIC_ARN')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

_slack_webhook_cache = None


def get_slack_webhook():
    global _slack_webhook_cache
    if _slack_webhook_cache:
        return _slack_webhook_cache

    try:
        response = ssm_client.get_parameter(Name=SLACK_PARAM_NAME, WithDecryption=True)
        _slack_webhook_cache = response['Parameter']['Value']
        return _slack_webhook_cache
    except ClientError as e:
        logger.error(f'Erro ao buscar webhook do Slack no SSM: {e}')
        raise RuntimeError('Falha ao recuperar o webhook do Slack. Verifique o parâmetro no SSM.')


def send_to_slack(webhook_url: str, message: str):
    data = json.dumps({'text': message}).encode('utf-8')
    req = urllib.request.Request(webhook_url, data=data, headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req) as resp:
        logger.info('Notificação enviada ao Slack. Código HTTP: %s', resp.getcode())


def get_account_name(account_id: str) -> str:
    try:
        response = org_client.describe_account(AccountId=account_id)
        return response['Account']['Name']
    except ClientError as e:
        logger.warning('Não foi possível obter o nome da conta: %s', e)
        return account_id


def lambda_handler(event, context):
    try:
        logger.debug('Evento recebido: %s', json.dumps(event, indent=2))

        slack_url = get_slack_webhook()
        detail = event.get('detail', {})
        permissions = detail.get('requestParameters', {}).get('ipPermissions', {}).get('items', [])
        sg_id = detail.get('requestParameters', {}).get('groupId', 'Desconhecido')
        region = event.get('awsRegion') or event.get('region', 'Desconhecida')
        account_id = event.get('account', 'Desconhecida')
        account_name = get_account_name(account_id)
        timestamp = event.get('time', 'Desconhecida')
        user = detail.get('userIdentity', {}).get('arn') or 'Usuário desconhecido'

        for perm in permissions:
            from_port = perm.get('fromPort')
            to_port = perm.get('toPort')
            ip_protocol = perm.get('ipProtocol')
            ip_ranges = perm.get('ipRanges', {}).get('items', [])

            for ip in ip_ranges:
                if ip.get('cidrIp') == '0.0.0.0/0':
                    if ip_protocol == '-1':
                        service = 'All Traffic'
                    elif from_port == 0 and to_port == 65535 and ip_protocol == 'tcp':
                        service = 'All TCP'
                    else:
                        service = {
                            22: 'SSH',
                            3389: 'RDP',
                            3306: 'MySQL',
                            5432: 'PostgreSQL',
                            1433: 'MSSQL',
                            6379: 'Redis'
                        }.get(from_port, f'Porta {from_port}')

                    message = (
                        '🚨 *Alerta de Segurança detectado!*\n\n'
                        f'🔓 Uma regra de *Security Group* foi criada permitindo acesso à porta *{from_port}* '
                        f'({service}) para a Internet (`0.0.0.0/0`).\n\n'
                        '🧾 *DETALHES DO EVENTO:*\n'
                        f'🔐 Security Group ID: `{sg_id}`\n'
                        f'🌎 Região: `{region}`\n'
                        f'🏢 Conta AWS: `{account_name}` (`{account_id}`)\n'
                        f'👤 Usuário: `{user}`\n'
                        f'🕒 Data/Hora: `{timestamp}`\n'
                    )

                    try:
                        send_to_slack(slack_url, message)
                        logger.info('Notificação enviada para Slack com sucesso.')
                    except ClientError as err:
                        logger.error('Erro ao enviar mensagem: %s', err)

    except Exception as e:
        logger.error('Erro inesperado no processamento do evento: %s', str(e))
        logger.debug(json.dumps(event, indent=2))

