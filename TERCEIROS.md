# Skills de terceiros

## MLflow

Copiadas sem alteração do [mlflow/skills](https://github.com/mlflow/skills), commit
`51a42ea2b07fadb45fb34c7cecf0c87edbe05686` (copiado em 09/10/2026), sob a licença Apache-2.0
([licencas/mlflow-skills-LICENSE](licencas/mlflow-skills-LICENSE)). Para atualizar, copie de novo
do repo de origem num commit novo e troque o hash acima; o `scripts/sincronizar.sh` não mexe nelas.

| Skill | Pasta de origem |
| --- | --- |
| `agent-evaluation` | `agent-evaluation/` |
| `analyze-mlflow-chat-session` | `analyze-mlflow-chat-session/` (name: `analyzing-mlflow-session`) |
| `analyze-mlflow-trace` | `analyze-mlflow-trace/` (name: `analyzing-mlflow-trace`) |
| `instrumenting-with-mlflow-tracing` | `instrumenting-with-mlflow-tracing/` |
| `mlflow-onboarding` | `mlflow-onboarding/` |
| `querying-mlflow-metrics` | `querying-mlflow-metrics/` |
| `retrieving-mlflow-traces` | `retrieving-mlflow-traces/` |
| `searching-mlflow-docs` | `searching-mlflow-docs/` |

## Obsidian

Copiadas sem alteração do [kepano/obsidian-skills](https://github.com/kepano/obsidian-skills),
commit `3ccff5338ea700537839b21900aa5358a0402c98` (copiado em 09/10/2026), sob a licença MIT
([licencas/obsidian-skills-LICENSE](licencas/obsidian-skills-LICENSE)). A `obsidian-cli` precisa
do app do Obsidian aberto, então só serve na máquina; a `defuddle` precisa do CLI
(`npm install -g defuddle`).

| Skill | Pasta de origem |
| --- | --- |
| `defuddle` | `skills/defuddle/` |
| `json-canvas` | `skills/json-canvas/` |
| `obsidian-bases` | `skills/obsidian-bases/` |
| `obsidian-cli` | `skills/obsidian-cli/` |
| `obsidian-markdown` | `skills/obsidian-markdown/` |

## Matt Pocock

Copiadas sem alteração do [mattpocock/skills](https://github.com/mattpocock/skills), commit
`49dd158d1076134a641b33efb035946536778336` (copiado em 15/10/2026), sob a licença MIT
([licencas/mattpocock-skills-LICENSE](licencas/mattpocock-skills-LICENSE)). A `grill-me` só
chama a `grilling` e não dispara sozinha (`disable-model-invocation`): use `/grill-me`.

| Skill | Pasta de origem |
| --- | --- |
| `grill-me` | `skills/productivity/grill-me/` |
| `grilling` | `skills/productivity/grilling/` |

## Superpowers

Copiadas sem alteração do [obra/superpowers](https://github.com/obra/superpowers), commit
`bb92a77741419a4ab5f06e711a283343f1ada0c3` (copiado em 15/10/2026), sob a licença MIT
([licencas/superpowers-LICENSE](licencas/superpowers-LICENSE)). Entram só as que disparam numa
situação específica; as de fluxo (`using-superpowers`, `brainstorming`, `writing-plans`,
`executing-plans`, `subagent-driven-development`, `test-driven-development`, `using-git-worktrees`,
`finishing-a-development-branch`) ficam de fora por decisão do Gustavo (15/10/2026), porque
disparam em quase toda tarefa e competem com o fluxo spec-first; a `diagnosing-superpowers` só
serve a quem usa o pacote inteiro. Algumas citam `superpowers:test-driven-development`, que
não está aqui.

| Skill | Pasta de origem |
| --- | --- |
| `dispatching-parallel-agents` | `skills/dispatching-parallel-agents/` |
| `receiving-code-review` | `skills/receiving-code-review/` |
| `requesting-code-review` | `skills/requesting-code-review/` |
| `systematic-debugging` | `skills/systematic-debugging/` |
| `verification-before-completion` | `skills/verification-before-completion/` |
| `writing-skills` | `skills/writing-skills/` |

## Anthropic

Copiada sem alteração do [anthropics/skills](https://github.com/anthropics/skills), commit
`dbd4588f9e1033efb41dad4bef2f7947c8993d44` (copiado em 15/10/2026), sob a licença Apache-2.0
(o `LICENSE.txt` vai dentro da pasta da skill).

| Skill | Pasta de origem |
| --- | --- |
| `frontend-design` | `skills/frontend-design/` |
