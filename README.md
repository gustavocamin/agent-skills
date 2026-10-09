# agent-skills

As skills do Gustavo para o Claude Code e o Codex, num só lugar, para instalar na máquina local e
no setup de qualquer ambiente cloud (Claude Code na web, Codex cloud).

## O que tem

| Pasta | Quando entra | Skills |
| --- | --- | --- |
| `skills/` | sempre | `iniciar-projeto` (cria um projeto no fluxo spec-first) e 8 skills do MLflow (avaliação de agentes, tracing, traces, métricas, docs), vindas do [mlflow/skills](https://github.com/mlflow/skills) (ver [TERCEIROS.md](TERCEIROS.md)) |
| `projetos/curso-lab-agent/` | só com `--projeto curso-lab-agent` | `constitution-interview`, `spec-feature`, `implementar-grupo`, `validate-feature`, `replan`, na versão do curso-lab |

As skills de `projetos/` falam das regras de um repo específico (exam_map, Lakebase, F23…). Num
projeto novo, use as versões genéricas que a `iniciar-projeto` gera dentro dele. No próprio
curso-lab, elas já vêm do repo (`.claude/skills`); a cópia daqui é referência.

## Instalar

```bash
git clone https://github.com/gustavocamin/agent-skills && bash agent-skills/install.sh
```

- Instala em `~/.claude/skills` (Claude Code) e `~/.agents/skills` (Codex, pasta pessoal da doc
  atual). Pasta sem escrita é pulada.
- Rodado de novo, só atualiza o que mudou. Uma skill que já existe com outro conteúdo fica como
  está e aparece no resumo; `--forcar` a substitui.
- `--link` cria links para o clone em vez de cópias: a máquina local passa a usar o repo como
  fonte. `--destino <pasta>` instala só ali. `--projeto <nome>` soma uma pasta de `projetos/`.

### No setup de um ambiente cloud

Cole no script de setup do ambiente (o repo é público, então não precisa de token):

```bash
d="${TMPDIR:-/tmp}/agent-skills"
git clone -q --depth 1 https://github.com/gustavocamin/agent-skills "$d" 2>/dev/null || git -C "$d" pull -q --ff-only
bash "$d/install.sh" || echo "agent-skills: instalação falhou; a sessão segue sem as skills pessoais"
```

- **Claude Code na web:** em claude.ai/code, no ambiente → script de setup. Precisa de acesso
  de rede que alcance o github.com (o nível **Trusted** padrão alcança).
- **Codex cloud:** no ambiente → script de setup, antes do resto. No container do Codex o HOME é
  só de leitura (observado no curso-lab em 08/10/2026), então o instalador cai para
  `<repo da tarefa>/.agents/skills` e põe cada pasta nova no `.git/info/exclude`: o Codex enxerga
  as skills e o `git status` da tarefa fica limpo. Skill com o mesmo nome de uma do repo da
  tarefa não é tocada.

Para fixar uma versão, troque o clone por `git clone ... && git -C "$d" checkout <commit>`.

## Manter

- Mudou uma skill na máquina: `bash scripts/sincronizar.sh` traz `~/.claude/skills` para
  `skills/`; `bash scripts/sincronizar.sh --projeto curso-lab-agent <caminho do repo>` traz as do
  projeto. Skill nova: `bash scripts/sincronizar.sh --nova <pasta da skill>`.
- Com `install.sh --link` na máquina local, a edição já acontece no clone, e não precisa
  sincronizar.
- Antes do commit: `python3 scripts/conferir.py` (o CI roda o mesmo). Ele confere o frontmatter,
  nomes repetidos, tokens vazados e o `install.sh` num HOME vazio, num HOME só de leitura e com
  uma skill editada.
- Este repo é público: nada de segredo, email, host de workspace ou dado pessoal nas skills.
