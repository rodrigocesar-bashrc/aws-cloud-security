
# Auto-remediação de interrupção do CloudTrail

Repositório para armazenar o template do CloudFormation da solução de auto remediação para interrupção do AWS CloudTrail.

Esta solução implementa uma mitigação automática para o evento de parada do CloudTrail (StopLogging), garantindo que o serviço de auditoria permaneça ativo na organização.

---

## :rotating_light: Problema

O CloudTrail é responsável por registrar todas as ações realizadas nas contas AWS. Caso o logging seja interrompido (StopLogging), a visibilidade e auditoria das ações ficam comprometidas, representando um risco grave de segurança e compliance.

---

## :white_check_mark: Solução

Criação de uma automação baseada em **EventBridge Rule** e **AWS Systems Manager Automation**:

1. Uma regra do EventBridge detecta o evento CloudTrail `StopLogging`;
2. Aciona um documento de automação (SSM Automation Runbook) que verifica o status do trail e reinicia o logging automaticamente;
3. Utiliza uma IAM Role dedicada para garantir permissões mínimas e seguras;

---

## :gear: Componentes do CloudFormation

- **EventBridge Rule:** Detecta o evento `StopLogging` do CloudTrail e aciona a automação.
- **SSM Automation Document:** Runbook que verifica e reinicia o logging do CloudTrail.
- **IAM Role:** Permissões mínimas para executar a automação e controlar o CloudTrail.

---

## :mag: Evento monitorado

| Evento           | Serviço     | Descrição                                 |
|------------------|------------|-------------------------------------------|
| StopLogging      | CloudTrail | Interrupção do logging do CloudTrail       |

---

## :rocket: Como usar

1. Baixe o template do CloudFormation: **cloudformation-remediation-cloudtrail.yaml**
2. Faça o deploy via Stack (conta individual) ou Stack Set (multi-contas), preferencialmente na região Norte da Virgínia (**us-east-1**), pois o código e os ARNs estão voltados para essa região. Caso deseje adaptar para outra região, ajuste os ARNs e parâmetros conforme necessário.
3. O monitoramento e remediação do CloudTrail será realizado automaticamente ao detectar interrupção do logging.
4. O arquivo **ssm-runbook-cloudtrail.yaml** está presente apenas para consulta do conteúdo do runbook, não é necessário fazer deploy manual desse arquivo.

---

## :construction_worker: Futuras melhorias

- Notificações integradas (SNS, Slack, etc) para alertar sobre remediações automáticas;
