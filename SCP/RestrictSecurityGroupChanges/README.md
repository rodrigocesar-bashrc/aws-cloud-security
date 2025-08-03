## 📄 Política: `RestrictSecurityGroupChanges.json`

Essa SCP tem como objetivo **bloquear alterações em Security Groups** em todas as contas da organização, impedindo mudanças não autorizadas que possam expor recursos à internet ou comprometer o ambiente.

### 🔒 Ações bloqueadas:

- Criação de Security Groups (`ec2:CreateSecurityGroup`)
- Exclusão de Security Groups (`ec2:DeleteSecurityGroup`)
- Autorização de regras de entrada (`ec2:AuthorizeSecurityGroupIngress`)
- Revogação de regras de entrada (`ec2:RevokeSecurityGroupIngress`)
- Modificação direta de regras (`ec2:ModifySecurityGroupRules`)

### 🛡️ Finalidade

Restringir a manipulação de regras de segurança (SGs) a canais controlados, como pipelines automatizadas ou roles de automação específicas, prevenindo alterações manuais que possam resultar em falhas de segurança.

---

## 🧩 Exceções permitidas

A política pode ser configurada para **permitir alterações apenas por entidades confiáveis**, como:

- 👨‍💻 Role(s) utilizada(s) por time(s) autorizado(s);
- 🤖 Role(s) de automação;
- 🧑 Usuário(s) IAM.

Essas exceções são definidas através da cláusula `Condition` no bloco de `Deny`, utilizando `ArnNotLike`.

---

## 📚 Documentação completa

Para uma explicação detalhada da motivação, estrutura e aplicação da política, leia:

👉 **[Série AWS SCP #01 – Restringindo alterações em Security Groups](https://medium.com/@rodrigocesar.bashrc/s%C3%A9rie-aws-scp-01-restringindo-altera%C3%A7%C3%B5es-em-security-groups-9b061e4cb7d4)**  
✍️ Autor: Rodrigo Cesar

---

## 🧪 Como testar

Antes de aplicar a SCP em produção:

1. Aplique em uma conta de **sandbox** ou uma **OU de testes**.
2. Teste com diferentes roles e usuários para garantir que as exceções estão funcionando corretamente.
