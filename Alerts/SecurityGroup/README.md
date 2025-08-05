# 🚨 Alertas de Security Groups Expostos para o Mundo (0.0.0.0/0)

Este projeto implementa uma solução automatizada para monitorar, detectar e alertar em tempo real sobre regras sensíveis em Security Groups na AWS, utilizando a abordagem **Hub-and-Spoke** com AWS CloudTrail, EventBridge, Lambda e SNS.

---

## 📌 Visão Geral

- Detecta regras `AuthorizeSecurityGroupIngress` com `0.0.0.0/0`
- Suporta serviços comuns: SSH, RDP, MySQL, PostgreSQL, Redis, MSSQL, All TCP e All Traffic
- Envia notificações para:
  - 🔔 Slack (via Webhook)
  - 📧 E-mail (via SNS subscription)
- Coleta eventos **em tempo real** via CloudTrail e EventBridge

---

## 🧱 Arquitetura

A arquitetura segue o padrão **Hub-and-Spoke**:

- **Conta Hub**: recebe os eventos e processa via Lambda.
- **Contas Spoke**: enviam eventos para o EventBus da conta Hub via StackSet.
- A função Lambda analisa os eventos e dispara alertas.

<img width="1403" height="745" alt="image" src="https://github.com/user-attachments/assets/a2c6d3cb-d79d-4c1c-b1a5-5b643ffe1fa8" />

---

## ✅ Pré-requisitos

Antes do deploy, siga os passos abaixo:

1. **Criar manualmente o bucket S3** (ex: `bashrc-alerts-security-group`)
   - Realizar o upload do arquivo `lambda.zip` contendo o `handler.py`
2. **Criar manualmente o parâmetro SSM** contendo o Webhook do Slack:
   - Nome: `/alertas/slack/webhook`
   - Tipo: `SecureString`

---

## 🚀 Deploy Hub Account - via Stack

Na conta de gerenciamento/payer (Hub), realize o deploy do template `hub-account-stack.yaml` via AWS CloudFormation (modo padrão). Isso criará os seguintes recursos:

- EventBridge EventBus (default)
- Função Lambda com as permissões apropriadas
- Regra do EventBridge que aciona a Lambda em tempo real
- Tópico SNS com subscription de e-mail
- Permissão no EventBus para aceitar eventos da Organização (via `PrincipalOrgID`)

> ⚠️ **Importante:** Certifique-se de que a `Organization ID` esteja correta no template antes de realizar o deploy.

## 🚀 Deploy Spoke Account - via StackSet

Nas contas membro (Spoke), a stack deve ser implantada usando o AWS CloudFormation StackSets. 
Essa stack cria os recursos necessários para enviar eventos em tempo real para o EventBus da conta Hub:

---

## 📬 Redundância de Notificações

Além do Slack, a solução também conta com **redundância via e-mail** (SNS subscription), garantindo a entrega dos alertas mesmo que o Slack esteja indisponível ou algo do tipo.

---

### 🧪 Payload de Teste
Para validar se a solução está funcionando corretamente após o deploy, até para questões de debug/tshoot, você pode simular um evento de modificação em um Security Group com o seguinte payload na Lambda:

```json
{
  "version": "0",
  "id": "c80cc918-7d6e-41d3-b4dd-example",
  "detail-type": "AWS API Call via CloudTrail",
  "source": "aws.ec2",
  "account": "123456789012",
  "time": "2025-08-03T18:25:43Z",
  "region": "us-east-1",
  "resources": [],
  "detail": {
    "eventSource": "ec2.amazonaws.com",
    "eventName": "AuthorizeSecurityGroupIngress",
    "requestParameters": {
      "groupId": "sg-0123456789abcdef0",
      "ipPermissions": [
        {
          "ipProtocol": "tcp",
          "fromPort": 22,
          "toPort": 22,
          "ipRanges": [
            {
              "cidrIp": "0.0.0.0/0"
            }
          ]
        }
      ]
    }
  }
}
```

---

## 🔔 Exemplo de Alerta Recebido

<img width="1339" height="792" alt="image" src="https://github.com/user-attachments/assets/a187e427-8280-4d0c-bb59-caaf2779c6ed" />

---

📚 Documentação completa
Para uma explicação detalhada da motivação, estrutura e aplicação da política, leia:

👉 **[Série AWS SCP #01 – Restringindo alterações em Security Groups](https://medium.com/@rodrigocesar.bashrc/s%C3%A9rie-aws-scp-01-restringindo-altera%C3%A7%C3%B5es-em-security-groups-pt-2-42098f3e3a5f)**  
✍️ Autor: Rodrigo Cesar
