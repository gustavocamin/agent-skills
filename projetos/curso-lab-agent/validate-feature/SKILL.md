---
name: validate-feature
description: Roda a validação de uma feature implementada contra o validation.md dela — testes, lint, sincronia spec↔código, revisão independente pelo agente que não integra e checklist humano — e prepara o fechamento da branch. Use quando o Gustavo disser que terminou de implementar uma feature ou pedir para validar/fechar a Fxx.
---

# validate-feature

Quem roda esta skill é quem integra a feature: o agente da linha `Integra` do `plan.md`, o Claude Code se ela faltar (protocolo no `AGENTS.md`).

## Passos

1. Leia `specs/features/Fxx-*/` (plan, requirements, validation) e o `AGENTS.md`.
2. **Automática:** rode `pytest -q` e `ruff check .`. Testes de integração (`-m integration`) só se o Gustavo pedir — eles tocam a Free Edition. Para cada teste novo de contrato ou de dado da feature, mostre uma mutação (numa cópia ou worktree temporária, nunca no repo) que o faz falhar, e registre no `validation.md` (replan pós-F27).
3. **Sincronia spec ↔ código:** para cada requisito R/N, aponte o arquivo/teste que o implementa. Liste:
   - requisitos sem implementação ou sem teste;
   - código que não corresponde a nenhum requisito.

   Confira também o "Registro dos grupos": uma linha por grupo, com handoff, CI, integração e a coluna "Handoff conferido" preenchida. Em cada grupo do outro agente, os desvios declarados foram refeitos contra a spec e o diff, o campo `Contrato` bate com o schema do servidor e há mutação própria de quem integra; o que não confere é achado registrado.
4. **Invariantes:** verifique explicitamente os do `AGENTS.md` que a feature toca (ex.: GENERATE nunca escreve `score`; nenhum segredo versionado — rode um `git grep` por tokens óbvios como `dapi`).
5. **Revisão independente (obrigatória em toda feature, desde o replan pós-F26; pelo agente que não integra, desde o replan de 08/10):** quando o Claude Code integra, abra uma sessão nova do Codex (app do ChatGPT ou CLI, na raiz do repo, na branch da feature, sem o histórico da conversa; no Codex cloud, a branch precisa estar no GitHub). Quando o Codex integra, abra uma sessão nova do Claude Code na mesma branch, sem histórico. Cole o prompt abaixo, trocando `Fxx` e a branch. Se o outro agente não estiver disponível, use um subagente ou uma sessão nova de quem integra, com o mesmo prompt, e registre o motivo. Reproduza cada achado antes de corrigir, spec e código juntos, e registre a revisão no `validation.md` (replan pós-F03).

   > Você é o revisor independente da feature Fxx deste repo. Leia só: `specs/constitution/` (mission, tech_stack, roadmap), `AGENTS.md`, `specs/features/Fxx-*/` e o diff `git diff main...feature/Fxx-nome`. Não use outro contexto. Reporte: (1) divergências entre a spec e o diff; (2) bugs, cada um com um cenário concreto (entrada ou estado → resultado errado); (3) testes fracos: para cada teste novo de contrato ou de dado, tente uma mutação do código ou do dado numa cópia temporária (`git archive HEAD | tar -x -C <pasta temporária>` ou uma worktree descartável) e diga se o teste falha. Não altere o repo, não faça commit nem push e não rode comando que toque o workspace Databricks ou o Lakebase. Termine com uma lista numerada de achados, do mais grave ao menos grave.
6. Apresente um relatório curto: passou / falhou / gaps. Cada resultado diz se foi observado nesta sessão ou relatado pelo Gustavo ou por outro agente, com o commit ou o hash do que foi testado, e as provas citadas ficam no `validation.md` (regra de Evidência do `AGENTS.md`). Gaps são corrigidos via conversa, atualizando spec **e** código juntos.
7. Deixe os itens "Humana (Gustavo)" do `validation.md` para ele marcar — não marque por ele.
8. Quando tudo estiver marcado: preencha a seção "Resultado", atualize o status da feature no `roadmap.md`, faça commit `feat(Fxx): <resumo>` com specs + código juntos, e sugira abrir o PR / merge para `main`: um PR por feature, aberto por quem integra; correção achada depois do merge vai num PR `fix(Fxx)` próprio. Depois do merge, se a feature mudou conteúdo publicado (`course/` ou `trilhas/`), rode `python -m agent.publish --check --profile <p>` na `main` e, se o código for 3, publique (`python -m agent.publish --profile <p>`); a publicação recusa sozinha remover id com progresso (F26).
9. Lembre de rodar a skill `replan` antes de começar a próxima feature.
