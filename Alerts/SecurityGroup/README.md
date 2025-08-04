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

## 🔔 Exemplo de Alerta Recebido

<img width="1200" height="686" alt="image" src="https://github.com/user-attachments/assets/38f826a7-5d82-48ea-b30a-8e6f16002c67" />

