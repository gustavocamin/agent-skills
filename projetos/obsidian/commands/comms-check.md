---
description: Check-in semanal do ciclo de 12 semanas de Comunicação & Influência — em que semana do ciclo estamos, o que o cronograma pede, o que ficou pendente da semana anterior
---

Check-in do ciclo de Comunicação & Influência. Fonte única da verdade:
`second-brain/02. Areas/Oratória/plano-comunicacao-influencia-12-semanas.md`.

**Calendário do ciclo:** semana 1 começa em 2026-11-02 (segunda); semana 12
= 18–24/01/2027. Cada semana vai de segunda a domingo. (O início original,
21/09/2026, foi abandonado em 03/10/2026: ciclo pausado até a prova DAA de
30/10 — decisão do usuário.)

## Comportamento

1. Calcular em que semana do ciclo a data de hoje cai.
   - Antes de 02/11/2026 → modo contagem regressiva (pausa declarada):
     reportar quantos dias faltam e o que a Semana 1 vai pedir (checklist
     §10 do plano). Não cobrar sinais de falha do §9 durante a pausa.
   - Depois de 24/01/2027 → ciclo encerrado: reportar isso e sugerir uma
     retrospectiva contra os marcos da Semana 12 (§8); não inventar
     "semana 13".
2. Ler o plano e montar o check-in da semana corrente:
   - **Checklist da semana** (§10): itens marcados vs. em aberto.
   - **Pendências da semana anterior**: itens não marcados da semana
     passada (se houver semana anterior no ciclo).
   - **Tipo de semana A/B** (com ou sem sessão do Toastmasters) conforme o
     que o plano/checklist indicar — se não estiver claro, perguntar em vez
     de assumir.
   - **Marcos**: nas semanas 4, 8 e 12, incluir o checklist de verificação
     do marco correspondente (§8).
   - **Sinais de falha precoce** (§9): checar os gatilhos que dependem de
     estado observável (ex.: semana 3 com banco de drills < 4 entradas; 2
     semanas seguidas sem bloco B) e sinalizar quando dispararem.
3. Cruzar com a carga paralela: o projeto `second-brain/01. Projects/
   Certificar Databricks/` roda ao mesmo tempo (bloco 1 começa 22/09) —
   quando as duas frentes tiverem semana pesada simultânea, apontar o
   conflito, sem resolver sozinho.

## Restrições

- **Somente leitura no plano.** Nunca marcar checkbox, nunca editar o
  arquivo do plano — o registro de progresso é do usuário. Se um item
  parecer feito mas não estiver marcado, perguntar, não marcar.
- Não reagendar nem reescrever o plano por conta própria; propostas de
  ajuste vão como sugestão no relatório.

## Output

Resumo curto na tela + relatório `second-brain/05. Reports/Comms-check
YYYY-MM-DD.md`:

```markdown
# Comms-check — YYYY-MM-DD (Semana N/12 · A|B)

## Esta semana pede
- [ ] <itens do checklist §10 ainda em aberto>

## Feito até agora
- <itens já marcados>

## Ficou da semana anterior
- <pendências, ou "nada">

## ⚠️ Sinais
- <sinais de falha disparados, marcos da semana, conflito de carga com a certificação — ou "nenhum">
```

Idempotente: rodar duas vezes no mesmo dia sobrescreve o relatório do dia.
