---
name: replan
description: Passo de replanejamento entre features — revisa a constituição com o que foi aprendido, propaga mudanças para specs e código existentes e ajusta o roadmap. Use depois de fechar uma feature, antes da próxima, ou quando um pedido contradiz a constituição.
---

# replan

## Passos

1. Leia `AGENTS.md`, `specs/constitution/` e o "Resultado" do `validation.md` da última feature fechada.
2. Pergunte ao Gustavo, em uma rodada só:
   - o que aprendeu nessa feature que muda stack, testes ou prioridades;
   - se alguma decisão em aberto do roadmap já pode ser fechada;
   - se as datas do roadmap ainda batem com a agenda de estudo (prova, trilha, trabalho);
   - se alguma feature futura deveria ser reagrupada, dividida ou cortada.
3. Proponha as mudanças como lista antes de editar. Após o OK:
   - atualize `mission.md` / `tech_stack.md` / `roadmap.md`, e o `AGENTS.md` quando a mudança mexe em regra de trabalho;
   - procure specs de features já feitas e código que a mudança invalida; atualize os dois juntos ou registre como pendência numa feature futura.
4. Adicione uma linha datada na seção "Decisões" do `roadmap.md`.
5. Commit `spec(replan): <resumo>` numa branch, e PR para a `main`, mesclado com o ok do Gustavo (nada entra na `main` sem CI verde; as regras do Codex recusam push na `main`).
6. Sugira uma conversa nova (`/clear` no Claude Code; `/new` no Codex CLI ou uma conversa nova no app do ChatGPT) e a próxima feature (`spec-feature`).
