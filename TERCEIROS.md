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

## Impeccable

Copiada sem alteração do [pbakaus/impeccable](https://github.com/pbakaus/impeccable), commit
`8a0e198da34ebc5b936a9d5975fb7a3b1cf353b7` (versão 4.6.0, copiada em 15/10/2026), sob a licença
Apache-2.0 ([licencas/impeccable-LICENSE](licencas/impeccable-LICENSE) e
[licencas/impeccable-NOTICE.md](licencas/impeccable-NOTICE.md)). Veio a versão compilada para o
Codex (`.agents/skills/impeccable/`), porque o frontmatter dela só usa `name`, `description` e
`metadata` e serve também ao Claude Code; os comandos aparecem como `$impeccable <comando>`, que no
Claude Code é `/impeccable <comando>`.

- Ficaram de fora, a pedido do Gustavo (15/10/2026, "só a pasta, sem hooks"): os hooks do
  `npx impeccable install` (SessionStart, PostToolUse e Stop num `settings.json`) e os quatro
  agentes do Claude Code (`.claude/agents/impeccable-*.md`), que só servem ao `new-work` e ao
  `live`; o `audit`, o `polish` e o `critique` não dependem deles. Copiar só a pasta não instala
  hook.
- No primeiro uso, `scripts/impeccable` baixa um binário das releases do GitHub para
  `~/.impeccable/bin` e confere o sha256 que vem da mesma release (integridade, não autoria). Sem
  rede (fase do agente no Codex cloud), a skill segue lendo o contexto direto, como ela prevê.
- No fluxo spec-first, as skills do ciclo dizem quando ela entra (`polish` ao fechar um grupo de
  tela, `audit` na validação) e recusam o que ela cria fora do `Toca` (`PRODUCT.md`, `DESIGN.md`,
  `.impeccable/`): o contexto de produto é o `mission.md`.

| Skill | Pasta de origem |
| --- | --- |
| `impeccable` | `.agents/skills/impeccable/` |

## Playwright CLI

Copiada sem alteração do [microsoft/playwright-cli](https://github.com/microsoft/playwright-cli),
commit `b85c7a736bb473bf55b584e54a09ffa698d6d871` (copiada em 15/10/2026), sob a licença
Apache-2.0 ([licencas/playwright-cli-LICENSE](licencas/playwright-cli-LICENSE)). O `SKILL.md` é o
mesmo que vem no pacote `@playwright/cli` 0.1.22, com que os comandos foram testados em 15/10/2026.

- Precisa do CLI: `npm install -g @playwright/cli@latest`, com o ok do Gustavo.
- O frontmatter traz `allowed-tools` (`playwright-cli`, `npx playwright`): no Claude Code, esses
  comandos rodam sem pedir aprovação enquanto a skill está ativa. O Codex ignora o campo. Os fluxos
  usam a skill só contra servidor local com dados sintéticos, nunca o Site publicado.
- Na cloud do Claude Code na web, o WebKit não baixa e o `file://` é recusado: a
  `conferir-no-iphone` diz como abrir com o Chromium da imagem por `http://127.0.0.1`.

| Skill | Pasta de origem |
| --- | --- |
| `playwright-cli` | `skills/playwright-cli/` |

## UI Skills

Copiada sem alteração do [ibelick/ui-skills](https://github.com/ibelick/ui-skills), commit
`fdd6c09dd866354a627ddf3fa46b7b01d421176d` (copiada em 15/10/2026), sob a licença MIT
([licencas/ui-skills-LICENSE](licencas/ui-skills-LICENSE)). As outras do pacote ficam de fora: a
`baseline-ui` exige Tailwind e `motion/react`, e a `improve-ui` repete o `polish` da `impeccable`.

| Skill | Pasta de origem |
| --- | --- |
| `fixing-accessibility` | `skills/fixing-accessibility/` |
