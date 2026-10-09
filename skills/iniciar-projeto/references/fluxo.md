# O fluxo do projeto gerado

Mapa do que a skill cria e de como o projeto anda depois. Leia antes de explicar o resultado ao dono humano ou de adaptar um artefato. O porquê de cada regra está em [aprendizados.md](aprendizados.md).

## Papéis

| Papel | Quem | Faz |
|---|---|---|
| Dono humano | quem decide (o "dono" das respostas) | aprova cada comando ⚠, marca os itens humanos, dá o ok do merge na `main`, escolhe `Integra: Codex` |
| Quem integra | o agente da linha `Integra` do `plan.md` (padrão: Claude Code) | branch da feature, merge dos grupos, conferência dos handoffs, `validation.md` ("Registro dos grupos", "Resultado"), `start_here.md`, constituição, PR |
| Dono de um grupo | o agente da linha `Dono` do grupo | implementa só o `Toca` do grupo, prova os testes com mutação, fecha com handoff |
| Revisor independente | sessão nova, sem histórico (o agente que não integra, com dois agentes) | lê só constituição, spec e diff; reporta divergências, bugs com cenário, testes fracos e documentos velhos |

## Os artefatos

| Caminho | Para que serve | Quem escreve | Quando muda |
|---|---|---|---|
| `AGENTS.md` | regras para qualquer agente: fluxo, grupos, handoff, invariantes, comandos | quem integra, por `replan` ou `constitution-interview` | quando uma regra de trabalho muda |
| `CLAUDE.md` | `@AGENTS.md` + o que é só do Claude Code | idem | raramente |
| `start_here.md` | próxima ação, o que aguarda o dono humano, estado agora, pendências, registro dos últimos 7 dias | quem integra | ao fim de cada dia de trabalho, no PR em curso |
| `specs/constitution/mission.md` | o que, para quem, objetivos, fora de escopo, critério de sucesso | `constitution-interview`, `replan` | F00 e replans |
| `specs/constitution/tech_stack.md` | stack, desenvolvimento, segredos, política de testes, operação ⚠ | idem | F00 e replans |
| `specs/constitution/roadmap.md` | calendário, features com "Pronto quando", decisões em aberto, Decisões datadas | idem, mais o status no fechamento de cada feature | F00, replans e fechamentos |
| `specs/features/_template/` | plan, requirements e validation de partida (somente leitura local) | `replan`, quando uma regra muda o template | raramente |
| `specs/features/Fxx-nome/plan.md` | objetivo, contexto, grupos com Dono · Branch · Toca, fora do escopo, riscos | `spec-feature`; cada dono marca os próprios checkboxes | durante a feature |
| `specs/features/Fxx-nome/requirements.md` | R/N, invariantes tocados, Interfaces (corpo de pedido e resposta), perguntas da entrevista | `spec-feature`, depois correções pela conversa | durante a feature |
| `specs/features/Fxx-nome/validation.md` | checklist automático e humano, mapa R → teste, mutações, Registro dos grupos, revisão, limites, Resultado | dono (o que é do grupo) e quem integra (o resto) | durante e no fechamento |
| `scripts/check_handoff.py` | conferidor da forma do handoff (`--file`, `--ci`, intervalo) | kit | raramente |
| `tests/test_processo.py` | trava as regras do fluxo, procura segredos e confere a tabela das regras do Codex | quem muda uma regra testada | junto com a regra |
| `tests/test_handoff.py` | contrato do conferidor | idem | junto com o conferidor |
| `.github/workflows/ci.yml` | conferidor, `ruff` e `pytest` em todo push e PR | features de processo | quando entra um gate novo |
| `.claude/settings.json` | o que nenhum agente faz: push forçado, push na `main`, `git add -f`, leitura de `.env`, e cada exclusão que o projeto conhecer (`deny`); comando ⚠ do projeto como `ask` | quem integra, por `replan` | raramente |
| `.claude/skills/` | `constitution-interview`, `spec-feature`, `implementar-grupo`, `validate-feature`, `replan` | `replan` | quando o ritual muda |
| `.agents/skills` (codex) | link para `.claude/skills` | kit | nunca |
| `.codex/config.toml` (codex) | perfil de permissões do projeto: escrita no workspace, rede só para registros de pacote, segredos negados | grupo ⚠ de processo | raramente |
| `.codex/rules/<slug>.rules` (codex) | `forbidden` / `prompt` / `allow` por prefixo de comando; todo `git push` pede aprovação | idem, com a tabela do `test_processo.py` | quando entra comando ⚠ novo |
| `.codex/setup-worktree.sh` (codex) | venv própria da worktree, sem segredo, recusa com menos de 5 GB | idem | raramente |

## O ciclo de uma feature

1. **Especificar** (`spec-feature`): confere se a spec já existe, cria a branch `feature/Fxx-nome`, mapeia o que existe hoje, entrevista, escreve os três arquivos, mostra o resumo com os donos e commita `spec(Fxx): plano, requisitos e validação`. Termina pedindo uma conversa nova.
2. **Implementar** (`implementar-grupo`, uma conversa por grupo): o dono confere `Dono`, `Integra` e branch; o grupo de contrato vem antes dos paralelos; os ⚠ correm em sequência, com aprovação comando a comando e parada para mostrar o diff. Comando novo que toca ambiente real entra nas regras dos agentes no mesmo grupo. Cada grupo fecha com suíte verde, desvios relidos contra Interfaces e Requisitos, `check_handoff.py --file`, push da branch do grupo, CI verde e o commit `handoff(Fxx-gN)`.
3. **Integrar** (quem integra, a cada grupo): confere o handoff (desvios refeitos, contrato, mutação própria), faz o merge `--no-ff` com o CI do grupo verde (`merge(Fxx-gN)`), roda a suíte inteira, transcreve no "Registro dos grupos" e remove a worktree e a branch do grupo.
4. **Validar** (`validate-feature`, por quem integra): suíte, mutações, mapa R → teste, invariantes, revisão independente numa sessão nova (achados reproduzidos e corrigidos com spec e código juntos), revisão humana preparada com veredito proposto. Fecha só com tudo marcado; commit `feat(Fxx)` e um PR por feature. Depois do merge: CI da `main`, publicação e conferência do artefato implantado, se houver.
5. **Replanejar** (`replan`): uma rodada de perguntas, mudanças propostas como lista, constituição, `AGENTS.md`, template e testes atualizados juntos, Decisão datada, `start_here.md`, PR `spec(replan)`. Aprendizado geral volta para este kit.

## Rituais do dia

- **Começo:** ler o `start_here.md` (próxima ação e o que aguarda o dono humano) e conferir que a `main` e a branch da feature no GitHub estão onde quem integra as deixou.
- **Conversa nova** entre especificar e implementar, e a cada grupo: o contexto é a spec, não o histórico.
- **Fim do dia** (quem integra): `start_here.md` atualizado no PR em curso, com uma linha no registro que termina em "Próximo: …".
- **Correções** sempre pela conversa: o agente muda spec e código juntos.

## Convenções de git

- **Commits:** `spec(Fxx)` para spec e registros; `feat(Fxx-gN)` ou `feat(Fxx)`; `fix(Fxx)`; `handoff(Fxx-gN)`; `merge(Fxx-gN)`; `spec(replan)`; `spec(constitution)`; `docs(start_here)`; `chore`. Tudo em português.
- **Branches:** `feature/Fxx-nome`; `feature/Fxx-nome--gN-<claude|codex>`; `feature/Fxx-nome--prova` (branch descartável que prova um gate do CI com um run vermelho e depois verde); `spec/replan-<fxx>`; `spec/constituicao`; `fix/Fxx-<curto>` (correção depois do merge).
- **PRs:** um por feature, aberto por quem integra; um por replan; correção pós-merge num PR `fix(Fxx)` próprio. O merge na `main` é sempre do dono humano, com o CI verde.

## Ativar o Codex num projeto gerado com o módulo `codex`

1. Marcar o projeto como confiável no Codex: a config, as regras e o AGENTS.md do projeto só carregam assim.
2. No app (o Codex agora fica dentro do app desktop do ChatGPT), em Settings, criar o ambiente local com o script `bash .codex/setup-worktree.sh`. O app grava essa configuração em `.codex/`, e ela pode ir para o git. Baixar o limite de worktrees guardadas (o padrão é 15; 3 bastam).
3. Não forçar modo de sandbox: no CLI, sem `-s`; no app, o seletor de permissões no perfil do projeto. Com `sandbox_mode` em qualquer config carregada, o perfil é ignorado.
4. Fazer a fumaça antes do primeiro grupo real: numa conversa nova, pedir ao Codex que descreva, só lendo, o escopo e os grupos de uma feature especificada, e conferir contra a spec. Depois, um grupo pequeno feito pelo Codex e integrado pelo Claude Code.
5. Codex cloud: as skills do repo valem lá; as pessoais, não. Grupo sem ⚠ só, partindo da branch da feature no GitHub. Credencial no cloud novo: "Environment variable" fica legível pelos programas; "Network secret" entra só para os domínios permitidos.

## Fatos conferidos na documentação (08/10/2026)

**Claude Code** (code.claude.com/docs):
- skill pessoal em `~/.claude/skills/<nome>/SKILL.md`, de projeto em `.claude/skills/`; pasta de skill pode ser link simbólico;
- `${CLAUDE_SKILL_DIR}` é trocado pelo caminho da skill no conteúdo dela;
- a lista de skills corta `description` + `when_to_use` em 1.536 caracteres; o padrão Agent Skills limita a `description` a 1.024;
- `CLAUDE.md` com `@AGENTS.md` é a forma documentada de dividir regras com outros agentes, e a recomendação é ficar abaixo de 200 linhas;
- `.claude/settings.json` é versionado e `.claude/settings.local.json` é pessoal; `deny` vence `ask`, que vence `allow`; a regra `Bash(git push *)` casa o texto do comando, então não é trava de segurança;
- `.worktreeinclude` copia arquivos ignorados para as worktrees criadas pelo Claude: nunca liste segredos nele;
- worktrees de subagente ficam em `.claude/worktrees/`, que deve ir para o `.gitignore`.

**Codex** (a doc mudou de developers.openai.com para learn.chatgpt.com/docs):
- skills de usuário em `~/.agents/skills` (o antigo `~/.codex/skills` está obsoleto); de repo em `.agents/skills`, do diretório atual até a raiz; links simbólicos são seguidos;
- o `SKILL.md` exige `name` e `description`, e campos desconhecidos são ignorados;
- `AGENTS.md`: o padrão é 32 KiB no total para os arquivos do projeto, e o que passa disso é truncado; projeto marcado como não confiável não carrega o `AGENTS.md` do projeto;
- perfis de permissões (`[permissions.<nome>]`, `default_permissions`, `extends = ":workspace"`) estão em Beta; a lista de domínios só vale com `[features] network_proxy = true`; `.git`, `.codex` e `.agents` ficam só leitura no workspace;
- as regras (`prefix_rule`, `forbidden` > `prompt` > `allow`) são experimentais e só carregam com o projeto confiável. Para conferir: `codex execpolicy check --rules <arquivo> -- <comando>`;
- o formato de `.codex/environments/environment.toml` não está documentado; ele é gerado pela tela de Settings do app, por isso o kit não o cria.
