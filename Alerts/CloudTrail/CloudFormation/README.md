
# 🚨 Alertas de Eventos Críticos do CloudTrail

Este projeto implementa uma solução automatizada para monitorar, detectar e alertar em tempo real sobre eventos críticos do AWS CloudTrail, como interrupção, deleção ou alteração do trail, utilizando AWS CloudFormation para deploy automatizado.

---

## 📌 Visão Geral

- Detecta eventos críticos do CloudTrail: `StopLogging`, `DeleteTrail`, `UpdateTrail`
- Envia notificações para:
  - 🔔 Slack (via Webhook, configurado via SSM Parameter)
  - 📧 E-mail (via SNS subscription)
- Coleta eventos **em tempo real** via CloudTrail e EventBridge

---

## 🧱 Arquitetura

O deploy via CloudFormation cria automaticamente:

- Regra do EventBridge para monitorar eventos críticos do CloudTrail
- Função Lambda para processar e enviar alertas
- Tópico SNS para notificações por e-mail
- Permissões necessárias (IAM Role, Bucket Policy, etc)

![image](https://github.com/user-attachments/assets/95fc6314-6a7b-4ec0-bec3-a93dd75aca72)

---

## ✅ Pré-requisitos

Antes do deploy, siga os passos abaixo:

1. **Criar manualmente o bucket S3**

- Exemplo: `alerts-cloudtrail-code-bashrc`, lembre-se de ajustar para o nome do seu bucket, pois o nome é global (único).
- Realizar o upload do arquivo `alerts-cloudtrail-lambda.zip` contendo o código da Lambda

2. **Criar manualmente o parâmetro SSM** contendo o Webhook do Slack:

- Nome: `/alertas/slack/webhook/alerts-aws-evasao-defesas`
- Tipo: `SecureString`

---

## 🚀 Deploy via CloudFormation

Realize o deploy do template `stack-arquitetura-cloudformation.json` via AWS CloudFormation na conta desejada. Isso criará automaticamente todos os recursos necessários para monitorar e alertar sobre eventos críticos do CloudTrail.

> ⚠️ **Importante:** Certifique-se de ajustar os nomes de bucket, parâmetros SSM, ARNs de SNS e Organization ID conforme seu ambiente antes do deploy.

---

## 📬 Redundância de Notificações

Além do Slack, a solução também conta com **redundância via e-mail** (SNS subscription), garantindo a entrega dos alertas mesmo que o Slack esteja indisponível, por exemplo.

---

📚 Documentação completa
Para uma explicação detalhada da motivação, estrutura e aplicação da política, leia:

👉 **[Série AWS SCP #03: Evasão de controles de Segurança — CloudTrail — Pt.2 [Alertas]](https://medium.com/@rodrigocesar.bashrc/s%C3%A9rie-aws-scp-03-evas%C3%A3o-de-controles-de-seguran%C3%A7a-cloudtrail-pt-2-alertas-ceeef7ece502)**
✍️ Autor: Rodrigo Cesar
