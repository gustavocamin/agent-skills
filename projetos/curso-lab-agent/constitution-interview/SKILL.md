---
name: constitution-interview
description: Revisa e fecha a constituição do projeto (specs/constitution/mission.md, tech_stack.md, roadmap.md) entrevistando o Gustavo sobre os itens [A CONFIRMAR]. Use na primeira sessão do repo (feature F00) ou quando ele pedir para revisar a constituição do zero.
---

# constitution-interview

O produto desta skill é a constituição fechada, não código.

## Passos

1. Leia `AGENTS.md` e os três arquivos de `specs/constitution/`.
2. Liste todos os itens marcados **[A CONFIRMAR]** e as "Decisões em aberto" do roadmap. Mostre a lista numerada.
3. Entreviste em rodadas de 3–5 perguntas. Para cada decisão, ofereça as opções com um trade-off de uma linha e a sua recomendação — o Gustavo decide. Também pergunte:
   - se algo da missão ou do escopo mudou;
   - se a granularidade do roadmap está boa (features grandes demais para uma branch?);
   - política de testes e o que conta como "pronto".
4. Aplique as respostas nos três arquivos de forma consistente (uma decisão no tech_stack que mexe no roadmap atualiza os dois; uma que mexe em regra de trabalho atualiza também o `AGENTS.md`). Remova o marcador [A CONFIRMAR] do que foi decidido e o aviso de "Rascunho semente" quando não sobrar nenhum.
5. Registre as decisões numa seção "Decisões" no fim do `roadmap.md`, com data e uma linha de porquê.
6. Mostre o diff resumido e peça correções — correções entram via conversa, e o agente edita.
7. Commit: `spec(constitution): fecha decisões iniciais`.
