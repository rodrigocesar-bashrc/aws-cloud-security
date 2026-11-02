# Política: `DenyUnapprovedRegions.json`

Essa SCP tem como objetivo **restringir o uso da AWS às regiões aprovadas pela organização**, negando qualquer operação fora delas. Neste exemplo, as regiões permitidas são **`sa-east-1`** e **`us-east-1`**. Serviços globais, que operam a partir de `us-east-1` ou não têm região, ficam fora do bloqueio, para que IAM, Organizations, Route 53, CloudFront, billing e afins continuem funcionando.

A política é baseada no exemplo oficial da AWS: [Deny access to AWS based on the requested AWS region](https://github.com/aws-samples/service-control-policy-examples/blob/main/Region-controls/Deny-access-to-AWS-based-on-the-requested-AWS-region.json).

## Ações bloqueadas

- Qualquer ação em região diferente de `sa-east-1` e `us-east-1` (condição `aws:RequestedRegion`)
- Exceto as ações de serviços globais listadas no `NotAction`, como:
  - Identidade e organização (`iam:*`, `sts:*`, `organizations:*`)
  - Rede e borda (`route53:*`, `cloudfront:*`, `globalaccelerator:*`, `waf:*`, `wafv2:*`, `shield:*`)
  - Billing e suporte (`aws-portal:*`, `budgets:*`, `ce:*`, `cur:*`, `support:*`)

## Finalidade

Reduzir a superfície de ataque da organização: região que ninguém usa é exatamente onde um atacante sobe recursos sem ser notado. Esse tipo de abuso está associado às técnicas MITRE ATT&CK:

- [T1535 – Unused/Unsupported Cloud Regions](https://attack.mitre.org/techniques/T1535/)
- [T1496 – Resource Hijacking](https://attack.mitre.org/techniques/T1496/) (ex.: mineração de criptomoeda)

Essa proteção é fundamental para:

- Impedir a criação de recursos em regiões fora do radar da equipe;
- Concentrar monitoramento, logs e custos onde a organização de fato opera;
- Atender requisitos de residência de dados;
- Reduzir o escopo de serviços de detecção, como o GuardDuty, nas contas de workload.

---

## Exceções permitidas

A política isenta uma role privilegiada, para administração e break-glass:

- Role `OrganizationAccountAccessRole`, usada pela Management account para administrar as contas membro (exemplo de laboratório)

Essa exceção é definida via `Condition` com `ArnNotLike`, no bloco `Deny`. Em produção, prefira uma role de break-glass dedicada e monitorada, em vez de uma role usada no dia a dia.

---

## Pontos de atenção

- **A Management account não é afetada por SCPs.** Ela continua podendo usar qualquer região e precisa de monitoramento em todas.
- **A SCP é anexada na raiz da organização.** Ela vale para todas as contas membro, inclusive a de Security (administradora delegada do GuardDuty), que também fica restrita às regiões permitidas. Contas novas já nascem protegidas.
- **A role isenta é o que permite automação nas regiões bloqueadas.** Por exemplo, configurar o GuardDuty da conta de Security em todas as regiões para monitorar a Management. Sem a exceção, nem a administração central consegue operar fora das regiões permitidas.
- **Revise a lista do `NotAction` periodicamente.** O próprio exemplo da AWS avisa que ela pode não incluir os serviços globais mais recentes.

---

## Documentação completa

Para uma explicação detalhada da motivação, estrutura e aplicação da política, leia:

**[Série AWS SCP #04: Restringindo o uso de regiões na AWS Organizations](https://medium.com/@rodrigocesar.bashrc)**  
Autor: Rodrigo Cesar

---

## Como testar

Antes de aplicar a SCP em produção:

1. Aplique em uma conta de **sandbox** ou em uma **OU de testes**;
2. Faça uma chamada numa região bloqueada (ex.: `aws ec2 describe-vpcs --region eu-west-1`) e confirme o `AccessDenied` com menção a uma SCP;
3. Repita numa região permitida e confirme que funciona;
4. Valide que serviços globais (IAM, Route 53, billing) continuam acessíveis;
5. Valide que a role isenta consegue operar na região bloqueada.
