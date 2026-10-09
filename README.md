# agent-skills

As skills do Gustavo para o Claude Code e o Codex, num só lugar, para instalar na máquina local e
no setup de qualquer ambiente cloud (Claude Code na web, Codex cloud).

## O que tem

| Pasta | Quando entra | Skills |
| --- | --- | --- |
| `skills/` | sempre | `iniciar-projeto` (cria um projeto no fluxo spec-first), `skill-pessoal` (cria ou muda uma skill deste repo), `liberar-disco` (mede o disco e propõe o que limpar, sem apagar sem ok); 8 skills do MLflow, do [mlflow/skills](https://github.com/mlflow/skills), e 5 de Obsidian, do [kepano/obsidian-skills](https://github.com/kepano/obsidian-skills) (ver [TERCEIROS.md](TERCEIROS.md)) |
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

Cole no começo do script de setup do ambiente e, no Codex cloud, também no script de manutenção
(o repo é público, então não precisa de token):

```bash
# agent-skills: skills pessoais (github.com/gustavocamin/agent-skills)
(
  d="${TMPDIR:-/tmp}/agent-skills"
  if [ -d "$d/.git" ]; then
    git -C "$d" pull -q --ff-only
  else
    git clone -q --depth 1 https://github.com/gustavocamin/agent-skills "$d"
  fi
  bash "$d/install.sh"
) || echo "agent-skills: instalação falhou; a tarefa segue sem as skills pessoais"
```

- **Claude Code na web:** em claude.ai/code, no ambiente → script de setup. Precisa de acesso
  de rede que alcance o github.com (o nível **Trusted** padrão alcança).
- **Codex cloud:** no ambiente → script de setup e script de manutenção (este roda quando um
  contêiner em cache, de até 12 h, é retomado; sem ele, a tarefa usa as skills do dia do setup).
  O setup tem internet; a fase do agente, por padrão, não. Com o HOME sem escrita (observado no
  curso-lab em 08/10/2026), o instalador cai para `.agents/skills` do repo da tarefa (o do
  diretório atual ou, fora dele, o único repo em `/workspace`) e põe cada pasta no
  `.git/info/exclude`: o Codex enxerga as skills e o `git status` fica limpo. O Codex só procura
  skills do diretório atual até a raiz do repo, então não há pasta fora do repo que sirva.
  Skill com o mesmo nome de uma do repo não é tocada.
- **Testes do repo da tarefa:** um teste que lista `.claude/skills` ou `.agents/skills` precisa
  ignorar o que o git ignora, ou vai conferir as skills pessoais como se fossem do projeto. Os
  projetos da `iniciar-projeto` já fazem isso (`_skills_do_repo` no `tests/test_processo.py`).

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
