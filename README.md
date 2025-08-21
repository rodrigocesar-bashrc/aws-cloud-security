# aws-cloud-security

Este repositório reúne práticas, políticas e automações voltadas à segurança em ambientes AWS.

Possui exemplos práticos e templates relacionados à **segurança na AWS**, incluindo **Service Control Policies (SCPs)**, **auto-remediação** e **alertas**.  
O objetivo é fornecer uma base reutilizável para fortalecer ambientes em nuvem, com foco em **prevenção**, **detecção** e **resposta automática** a configurações inseguras.

---

## 📂 Estrutura do Repositório

- **`SCP/`**  
  Contém políticas de controle de serviço (Service Control Policies) para restringir ações sensíveis em contas da AWS Organizations.  
  - Exemplo: impedir que contas saiam da organização (`leaveorganization`).

- **`auto-remediation/`**  
  Soluções de auto-remediação utilizando **AWS Config**, **EventBridge** e **Lambda**, para corrigir automaticamente recursos que estejam em desconformidade com boas práticas de segurança.  
  - Exemplo: fechar portas sensíveis abertas para a Internet em Security Groups.

- **`Alerts/`**  
  Regras de monitoramento e notificações de segurança para detecção de eventos críticos em tempo real.  
  - Exemplo: alertas de portas sensíveis para a internet.
