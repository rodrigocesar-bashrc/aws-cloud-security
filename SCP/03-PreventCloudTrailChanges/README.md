## 📄 Política: `PreventCloudTrailChanges.json`

Essa SCP tem como objetivo **impedir alterações críticas no AWS CloudTrail**, protegendo a integridade dos logs de auditoria da organização. Ao negar ações como `StopLogging`, `DeleteTrail` e `PutEventSelectors`, essa política evita que usuários mal-intencionados ou mal configurados comprometam a rastreabilidade de eventos na nuvem.

### 🔒 Ações bloqueadas

- Interrupção da trilha (`cloudtrail:StopLogging`)
- Criação de trilhas (`cloudtrail:CreateTrail`)
- Exclusão de trilhas (`cloudtrail:DeleteTrail`)
- Atualização de trilhas (`cloudtrail:UpdateTrail`)
- Alteração do escopo de eventos registrados (`cloudtrail:PutEventSelectors`)
- Consulta de eventos (`cloudtrail:LookupEvents`)

### 🛡️ Finalidade

Evitar que qualquer conta ou usuário consiga **sabotar ou interromper os mecanismos de auditoria** da organização. Esse tipo de ataque está associado à técnica MITRE ATT&CK:

- [T1562.008 – Impair Defenses: Disable Cloud Logs](https://attack.mitre.org/techniques/T1562/008/)

Essa proteção é fundamental para:

- Manter o rastreamento de ações em toda a organização;
- Prevenir a ocultação de atividades maliciosas;
- Reforçar auditoria, conformidade e investigações forenses;
- Garantir que logs não sejam manipulados ou silenciados.

---

## 🧩 Exceções permitidas

A política pode ser configurada para permitir que **apenas entidades confiáveis**, como roles federadas via AWS SSO, possam executar as ações bloqueadas:

- 🧑‍💼 Usuário(s) específico(s) do Identity Center ou IAM, alguma role específica de usuário.

Essas exceções são definidas via `Condition` com `ArnNotLike`, no bloco `Deny`.

---

## 📚 Documentação completa

Para uma explicação detalhada da motivação, estrutura e aplicação da política, leia:

👉 **[Série AWS SCP #03: Evasão de controles de Segurança - CloudTrail](https://medium.com/@rodrigocesar.bashrc)**  
✍️ Autor: Rodrigo Cesar

---

## 🧪 Como testar

Antes de aplicar a SCP em produção:

1. Aplique em uma conta de **sandbox** ou em uma **OU de testes**;
2. Verifique o bloqueio das ações com usuários padrão;
3. Valide se as exceções (ex: roles SSO confiáveis) funcionam conforme esperado;
4. Simule um cenário de tentativa de desativação do CloudTrail para validar a efetividade.
