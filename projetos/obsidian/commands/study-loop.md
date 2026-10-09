---
description: Rotina de estudo da certificação Databricks — em que bloco/semana do plano estamos, a sessão do dia, revisão espaçada pendente e checklist administrativo
---

Rotina de acompanhamento do projeto `second-brain/01. Projects/Certificar
Databricks/`. Fontes da verdade:

- Plano mestre: `second-brain/01. Projects/Certificar Databricks/plano-unico-spark-databricks.md`
- Nota do projeto (Próxima ação): `second-brain/01. Projects/Certificar Databricks/Certificar Databricks.md`

**Calendário:** Bloco 1 (Arquitetura) 22–28/09/2026 · Bloco 2 (Spark
Developer Associate) 29/09 → prova na semana de 20–24/10 · Bloco 3 (Data
Engineer + curso-lab) de out/2026 ao 1º tri 2027. Checklist administrativo
(voucher, Webassessor, agendamento) com deadline 29/09.

## Comportamento

1. Calcular pela data de hoje em que bloco e semana do cronograma (§2.3 do
   plano) o usuário está. Antes de 22/09 → contagem regressiva para o
   Bloco 1. Depois da prova → modo Bloco 3 (ritmo do curso-lab, sem data
   fixa semanal — reportar o próximo módulo pendente).
2. Montar a sessão:
   - **O que o cronograma pede hoje/nesta semana** (lições, labs, práticas
     do §2.3 ou do Bloco corrente).
   - **Revisão espaçada** (protocolo "Camada de espaçamento"): o que foi
     estudado há ~1 dia / ~1 semana e está na janela de revisão.
   - **Checklist de objetivos do exam guide** (§2.4): itens ainda não
     auditados, priorizando os da semana corrente.
   - **Administrativo**: até 29/09, status do checklist administrativo em
     destaque; depois, só se houver item aberto.
   - **Desvio de rota**: comparar a "Próxima ação" da nota do projeto com
     a data de hoje; se estiver desatualizada, propor o novo texto no
     relatório (não editar a nota).
3. Cruzar com a carga paralela: o ciclo de Comunicação & Influência
   (`second-brain/02. Areas/Oratória/plano-comunicacao-influencia-12-semanas.md`)
   roda junto — sinalizar semanas de pico simultâneo (ex.: semana da prova
   × marco do ciclo), sem resolver sozinho.

## Restrições

- **Preparation-only.** Nunca escrever resumos de estudo, respostas de
  exercícios ou simulados pelo usuário — o protocolo do plano exige
  recuperação ativa humana. A rotina prepara a sessão; quem estuda é a
  pessoa.
- Somente leitura nos arquivos do projeto: nunca marcar checkbox, nunca
  editar o plano nem a nota do projeto. Propostas (ex.: nova "Próxima
  ação") vão no relatório.

## Output

Resumo curto na tela + relatório `second-brain/05. Reports/Study-loop
YYYY-MM-DD.md`:

```markdown
# Study-loop — YYYY-MM-DD (Bloco N · Semana <intervalo>)

## Sessão de hoje
- <o que o cronograma pede, em itens acionáveis>

## 🔁 Revisão espaçada
- <tópicos na janela de revisão, ou "nada na janela">

## 📋 Exam guide (§2.4)
- <objetivos ainda não auditados, priorizados — máx. 10>

## 🗂️ Administrativo
- <status voucher/Webassessor/agendamento, ou omitir se concluído>

## ⚠️ Sinais
- <próxima ação desatualizada (com proposta), conflito de carga com o ciclo de comunicação — ou "nenhum">
```

Idempotente: rodar duas vezes no mesmo dia sobrescreve o relatório do dia.
