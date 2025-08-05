# Auto-remediação de regras sensíveis em SGs

Repositório para armazenar o template do CloudFormation da solução de auto remediação para regras sensíveis em Security Groups na AWS.

Esta solução implementa uma mitigação automática para regras de segurança (Security Groups) criadas na AWS que expõem serviços críticos ou portas sensíveis para a internet.

<img width="1459" height="804" alt="cloudsec-sg-auto-remediation drawio" src="https://github.com/user-attachments/assets/5f9bef7f-e719-4ef5-b45b-a5fbe98b99a3" />

---

## :rotating_light: Problema

Regras em Security Groups que expõem portas como SSH (22), RDP (3389), Redis (6379), entre outras, para `0.0.0.0/0` ou `::/0` podem representar risco grave de segurança.

---

## :white_check_mark: Solução

Criação de uma função **AWS Lambda** que:

1. É acionada por um evento CloudTrail de `AuthorizeSecurityGroupIngress`;
2. Avalia as permissões configuradas na regra;
3. Identifica regras perigosas (portas `sensíveis`, `All traffic` e/ou `All TCP` expostas à internet);
4. Remove automaticamente essas permissões via `revoke_security_group_ingress`;
5. Envia alerta com detalhes para um canal no Slack: `#alerts-securitygroup-remediation`

---

## :gear: Componentes do CloudFormation

- **Lambda Function:** código em Python 3.13 que implementa a lógica de mitigação.
- **IAM Role:** Permissões mínimas para a Lambda remover regras e enviar logs.
- **EventBridge Rule:** Dispara a Lambda ao detectar `AuthorizeSecurityGroupIngress`.
- **Slack Webhook:** Notificações são enviadas para o canal especificado.

---

## :lock: Portas monitoradas

| Porta | Serviço                  | Descrição                   |
|-------|--------------------------|-----------------------------|
| 22    | SSH                      | Acesso remoto shell         |
| 3389  | RDP                      | Acesso remoto Windows       |
| 3306  | MySQL                    | Banco de dados relacional   |
| 5432  | PostgreSQL               | Banco de dados relacional   |
| 1433  | Microsoft SQL Server     | Banco de dados relacional   |
| 5439  | Amazon Redshift          | Data warehouse              |
| 6379  | Redis                    | Banco de dados em memória   |
| -1    | All Traffic              | Todo o tráfego IP permitido |
| 0-65535 (TCP) | All TCP          | Todas as portas TCP         |

---

## :satellite: Exemplos de alertas no Slack

![Alerta All TCP](https://github.com/user-attachments/assets/5567d534-14df-4180-bd7b-45be6299e01d)

![Alerta All Traffic](https://github.com/user-attachments/assets/a68b87a8-aa14-4cc8-9d77-224bd0cf0b29)

![Alerta Porta Sensível](https://github.com/user-attachments/assets/a451c136-f640-49c6-847a-0311c02dd860)

---

## :rocket: Como usar

1. Baixe o template do Cloudformation: **sg-auto-remediation-stack.yaml**
2. Faça deploy, via Stack (conta individual) ou via Stack Set (várias contas), com a URL do Webhook do Slack;
3. A cada nova regra insegura adicionada em SG, a Lambda será disparada;
4. Regras serão revogadas automaticamente e notificações enviadas ao Slack.

---

## :warning: Limitações

- Só mitiga alterações **novas** via `AuthorizeSecurityGroupIngress`;
- Não atua retroativamente em regras existentes;

---

## :construction_worker: Futuras melhorias

- Ajustar o valor do Webhook para ser armazenado como um SSM Parameter (SecureString), evitando a exposição do valor sensível na variável de ambiente da função Lambda;
- Análise retroativa de regras inseguras.

---

## :bookmark: Referências

- [Using AWS Lambda to Revert Unauthorized Security Group Changes](https://dev.to/aws-builders/using-aws-lambda-to-revert-unauthorized-security-group-changes-5hke)
- [Documentacão completa: Série AWS SCP #01 – Restringindo alterações em Security Groups - Parte 3](https://medium.com/@rodrigocesar.bashrc/s%C3%A9rie-aws-scp-01-restringindo-altera%C3%A7%C3%B5es-em-security-groups-pt-3-495c32d396f1)
