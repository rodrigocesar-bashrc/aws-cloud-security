## 📄 Política: `denyleaveorganization.json`

Essa SCP tem como objetivo **impedir que contas membros saiam da AWS Organizations**, bloqueando a ação organizations:LeaveOrganization. Essa proteção é essencial para manter o controle centralizado, evitando que contas evadam políticas de segurança, auditoria e conformidade aplicadas no nível organizacional.

### 🔒 Ações bloqueadas

- Saída do AWS Organizations (`organizations:LeaveOrganization`)

### 🛡️ Finalidade

Evitar evasão de controles de segurança e governança centralizados ao impedir que contas saiam da organização sem autorização. A saída da organização pode ser usada como tática de evasão (MITRE ATT&CK: [TA0005 - Defense Evasion](https://attack.mitre.org/tactics/TA0005/)
, [T1070 - Indicator Removal](https://attack.mitre.org/techniques/T1070/)) para:

- Fugir da aplicação de SCPs;

- Desativar trilhas de auditoria centralizadas no CloudTrail;

- Romper integrações com AWS Config, GuardDuty, Security Hub e outras ferramentas gerenciadas;

- Ocultar atividades maliciosas ou acidentais.

---

## 🧩 Exceções permitidas

A política pode ser configurada para permitir que apenas entidades confiáveis executem a ação de saída da organização, como:

- 🧑 Usuário(s) IAM: CloudAdmin (exemplo de demonstração)

Essas exceções são definidas através do parâmetro `Condition` no bloco de `Deny`, utilizando `ArnNotEquals`.

---

## 📚 Documentação completa

Para uma explicação detalhada da motivação, estrutura e aplicação da política, leia:

👉 **[Série AWS SCP #02: Evasão de controles de Segurança - DenyLeaveOrganization](https://medium.com/@rodrigocesar.bashrc/s%C3%A9rie-aws-scp-02-evas%C3%A3o-de-controles-de-seguran%C3%A7a-denyleaveorganization-481d92b8480e)**  
✍️ Autor: Rodrigo Cesar

---

## 🧪 Como testar

Antes de aplicar a SCP em produção:

1. Aplique em uma conta de **sandbox** ou uma **OU de testes**;
2. Teste o bloqueio com usuários padrão;
3. Teste a exceção com o(s) usuário(s) ou role(s) autorizadas.
