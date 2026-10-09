# AGENTS.md — agent-skills

Repo público com as skills do Gustavo para o Claude Code e o Codex. O `README.md` explica a
instalação; aqui ficam as regras para quem mexe nele.

- Uma skill = uma pasta com `SKILL.md` (frontmatter com `name` em kebab-case e `description`).
  Gerais em `skills/`; específicas de um projeto em `projetos/<projeto>/`.
- Skills de terceiros (`TERCEIROS.md`) não se editam aqui: atualizam-se copiando de novo da
  origem, com o commit novo no `TERCEIROS.md`.
- Repo público: nenhum segredo, email, host de workspace, id de conta ou dado pessoal.
- O `install.sh` nunca sobrescreve sem `--forcar` e nunca suja o git do repo onde instala. Mudou
  o instalador, mude o teste dele em `scripts/conferir.py`.
- Antes do commit, `python3 scripts/conferir.py` passa. Commits em português.
- Nomes de produto e caminhos mudam (pastas de skills do Claude Code e do Codex, setup do cloud):
  confirme na documentação atual antes de mudar um caminho.
