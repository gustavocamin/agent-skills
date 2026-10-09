---
name: iniciar-projeto
description: Cria um projeto novo já no fluxo spec-first — constituição semente (mission, tech_stack, roadmap), AGENTS.md e CLAUDE.md, start_here, template de feature, as skills do ciclo (constitution-interview, spec-feature, implementar-grupo, validate-feature, replan), CI com o conferidor de handoff e testes das regras do fluxo e, se pedido, Codex, Databricks e agente de IA — com os aprendizados do curso-lab-agent embutidos. Use sempre que quiserem começar, iniciar, criar, montar ou fazer o bootstrap de um projeto ou repositório novo, ou aplicar o fluxo spec-first a uma pasta nova ou existente, mesmo sem citar a skill.
---

# Iniciar projeto (spec-first)

O produto desta skill é um repositório que nasce no fluxo spec-first: regras para os agentes, constituição semente, rituais em skills, CI que confere o processo e um primeiro commit verde. Código de produto não entra aqui; ele começa na F01, pela `spec-feature` do próprio projeto.

**Pasta desta skill** (`<KIT>` nos comandos abaixo): no Claude Code, `${CLAUDE_SKILL_DIR}`; no Codex, a pasta onde este `SKILL.md` está (na instalação pessoal, `~/.agents/skills/iniciar-projeto`). Escreva o caminho completo em cada comando: variável de shell não passa de um comando para o outro.
- `scripts/criar_projeto.py` gera o projeto a partir de `assets/` (a camada `base` sempre e a camada `codex` com esse módulo; os módulos `databricks` e `agente` são blocos dentro dos templates).
- [references/fluxo.md](references/fluxo.md): o que cada artefato gerado faz, quem o escreve, os papéis, os rituais, as convenções de git e a ativação do Codex. Leia antes de explicar o resultado ou de adaptar um artefato.
- [references/aprendizados.md](references/aprendizados.md): o porquê de cada regra, com a feature do curso-lab que a originou. Leia quando alguém perguntar por que uma regra existe ou quiser tirá-la.

## Passos

1. **Pré-voo.**
   - Destino: pasta nova ou vazia. Com conteúdo, é adoção (seção "Repo existente").
   - iCloud: destino em `~/Documents` ou `~/Desktop` ganha o sufixo `.nosync` (ex.: `meu-app.nosync`, com um link `meu-app` se quiserem o nome de sempre). O iCloud esvaziou `.git`, venv e `node_modules` no curso-lab, e "Manter baixado" não segurou.
   - Disco: `df -h`. Abaixo de 15 GB, grupos em paralelo (worktrees) ficam limitados; abaixo de 5 GB, o setup de worktree do Codex recusa, e os grupos do Codex vão para o cloud; abaixo de 1 GB, pare e peça limpeza antes de criar a venv.
   - Ferramentas: `git`; um Python 3.11 ou mais novo para o projeto (`python3.11`; o `python3` do sistema pode ser mais velho, e o gerador roda com 3.9+); `gh` (opcional, para o GitHub); `codex` (opcional).
   - Se o destino fica fora do diretório desta sessão, a escrita lá pede aprovação; abrir a sessão na pasta-mãe evita isso.
2. **Entrevista**, em rodadas de 3 a 5 perguntas, com default e recomendação. Não pergunte o que veio no pedido ou dá para inferir (o dono pelo `git config user.name`). O que ficar sem resposta vira [A CONFIRMAR] para a F00: a `constitution-interview` do projeto fecha o resto.
   - Rodada 1: nome do projeto (e slug); quem decide (aprova ⚠ e merge); em 2 ou 3 frases, o que é, para quem e por que agora.
   - Rodada 2: agentes (só Claude Code, ou com Codex → módulo `codex`); Databricks (módulo `databricks`); o produto é um agente de IA (módulo `agente`); a stack do produto, se já se sabe (linguagem, onde roda, banco, provedor de LLM); o que é ⚠ além de segredos; invariantes já conhecidos.
   - Rodada 3 (opcional): marcos com data e candidatas a F01–F03.
3. **Gerar.** Escreva as respostas num JSON fora do projeto (no scratchpad):

   ```json
   {"projeto": "Painel de Vendas", "slug": "painel-vendas", "dono": "Gustavo",
    "modulos": ["codex", "databricks", "agente"],
    "alerta": ["segredos", "o banco de produção"],
    "invariantes": ["O app nunca escreve no schema de vendas."], "python": "3.11"}
   ```

   Só `projeto` e `dono` são obrigatórios. Rode `python3 "<KIT>/scripts/criar_projeto.py" --destino <pasta> --respostas <json> --simular`, mostre a lista e, com o ok, rode sem `--simular`. Se ele recusar a entrada (dono com ":" ou aspas, data inválida), corrija o JSON. O gerador nunca sobrescreve, renderiza tudo antes de escrever, cria o link `.agents/skills` (codex), deixa o template de feature somente leitura e roda `git init -b main`.
4. **Semear a constituição** com o que foi dito, e só isso:
   - `mission.md`; `tech_stack.md` (a stack e os limites citados); a frase do `README.md`; a próxima ação e o "Aguardando" do `start_here.md`;
   - `roadmap.md`: calendário e features candidatas; em "Decisões em aberto", as perguntas sem resposta e as decisões de arquitetura que ninguém tomou ainda (stack, onde roda, banco); em "Decisões", uma entrada datada por decisão da entrevista, acima da entrada de criação. Quando o porquê não foi dito, escreva "pedido de <dono> na abertura".
   - Dado desconhecido (data, versão) não se chuta: fica [A CONFIRMAR].
5. **Nascer verde:** `python3.11 -m venv .venv && .venv/bin/pip install -e ".[dev]"` (com a versão escolhida), depois `.venv/bin/pytest -q` e `.venv/bin/ruff check .`. Preencha o "Estado técnico" do `start_here.md` com o que observou (data, contagem de testes, interpretador, disco livre). Se um teste falhar pelo template, é defeito do kit: corrija na origem, rode o autoteste, gere de novo e conte ao dono; se falhar pela entrada ou pelo ambiente, corrija a entrada ou o ambiente.
6. **Primeiro commit:** confira `git status` (nenhum `.env`, nada fora do esperado) e faça `chore: esqueleto spec-first`.
7. **GitHub (opcional):** só com o ok explícito, `gh repo create <slug> --private --source . --push`. Confira o CI do primeiro push (`gh run list --limit 1`); o run entra no `start_here.md` no primeiro PR (o da constituição), e não num commit direto na `main`.
8. **Fechamento:** resumo de uma tela com onde o projeto ficou, o que foi criado (por grupo de artefatos), o que está [A CONFIRMAR] e a próxima ação: sessão nova na pasta do projeto e "vamos fechar a constituição" (F00). Com o módulo `codex`, passe os passos de "Ativar o Codex" de [references/fluxo.md](references/fluxo.md).

## Repo existente

`--adotar` cria só o que falta e lista o que pulou; o destino é a raiz do repositório (o gerador recusa uma subpasta de outro repo). Integre à mão o que pulou, acrescentando sem substituir: `AGENTS.md`, `CLAUDE.md` (com `@AGENTS.md` na primeira linha), `.claude/settings.json`, `start_here.md`, README, `.gitignore`, `pyproject.toml` e CI. Depois rode os testes: o `tests/test_processo.py` aponta o que ainda não confere. Código que já existe sem spec entra na primeira feature por um Grupo 0 que importa sem mudar nada; as correções vêm nos grupos seguintes, com diffs separados.

## Manter o kit

- Aprendizado novo de um projeto (pelo passo final da `replan` dele) entra em [references/aprendizados.md](references/aprendizados.md) e no template que o aplica, juntos.
- Depois de mudar templates ou o gerador, rode `python3 "<KIT>/scripts/autoteste.py" --python <interpretador com pytest e ruff>`. Ele gera os projetos sem módulos e com todos, confere que nascem verdes e prova com mutação que os testes do processo pegam uma spec quebrada.
- Toda regra de comando do Codex mudada no template muda também a tabela `EXPECTED_DECISIONS` de `assets/base/tests/test_processo.py.tmpl`.
