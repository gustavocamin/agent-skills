# AGENTS.md — agent-skills

Repo público com as skills do Gustavo para o Claude Code e o Codex. O `README.md` explica a
instalação; aqui ficam as regras para quem mexe nele.

- Uma skill = uma pasta com `SKILL.md` (frontmatter com `name` em kebab-case e `description`).
  Gerais em `skills/`; de um projeto em `projetos/<projeto>/`, que espelha o `.claude/` dele
  (`skills/`, `commands/`, `agents/`).
- Skills de terceiros (`TERCEIROS.md`) não se editam aqui: atualizam-se copiando de novo da
  origem, com o commit novo no `TERCEIROS.md`.
- Repo público: nenhum segredo (token, chave, senha), email, host de workspace ou id de conta.
  Exemplos públicos são genéricos: não incluir planos privados, pessoas, clientes ou prazos reais.
- O `install.sh` só atualiza automaticamente itens gerenciados cuja cópia instalada continua
  igual à baseline registrada. Preserva edições locais e itens sem proveniência; `--forcar`
  exige backup. Nunca sobrescreve arquivos versionados do projeto nem suja seu git status.
  Mudou o instalador, mude seus testes e rode `scripts/conferir.py`.
- Antes do commit, `python3 scripts/conferir.py` passa. Commits em português.
- Nomes de produto e caminhos mudam (pastas de skills do Claude Code e do Codex, setup do cloud):
  confirme na documentação atual antes de mudar um caminho.
