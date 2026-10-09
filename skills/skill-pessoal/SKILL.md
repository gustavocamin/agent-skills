---
name: skill-pessoal
description: Cria, muda ou remove uma skill pessoal do Gustavo no repo público gustavocamin/agent-skills, que alimenta o Claude Code e o Codex na máquina e nos ambientes cloud. Use quando ele pedir uma skill nova "pessoal", "minha" ou "para todos os projetos", quando uma skill de ~/.claude/skills ou ~/.agents/skills for editada, ou quando uma skill de projeto virar geral, mesmo sem citar o repo.
---

# Skill pessoal

As skills pessoais vivem num só lugar: o clone de `gustavocamin/agent-skills` em
`~/Documents/3. Resources/Technology/AI/agent-skills.nosync` (na máquina do Gustavo). Na
máquina, `~/.claude/skills/<nome>` e `~/.agents/skills/<nome>` são links para esse clone; nos
ambientes cloud, o setup clona o repo e roda o `install.sh`. Uma skill só chega ao cloud depois
do push.

Fora da máquina do Gustavo (ambiente cloud, outro computador), não há clone para editar: escreva
a skill, mostre-a e diga que ela entra no repo pela máquina dele ou por um PR no
`gustavocamin/agent-skills`.

## Passos

1. **Pública ou não.** O repo é público. Skill com dado pessoal (planos de vida, finanças,
   saúde, pessoas, empregador, caminhos do vault, emails, hosts de workspace) não entra:
   proponha um lugar privado (o repo do projeto, como o `second-brain` para o vault) ou uma
   versão genérica.
2. **Escrever** em `skills/<nome>/SKILL.md` no clone (específica de um projeto: em
   `projetos/<projeto>/<nome>/`, e a fonte continua sendo o repo do projeto). Use a
   `skill-creator` para o formato e a descrição, se estiver disponível. Em português, como as
   outras; `name` em kebab-case igual ao nome da pasta; descrição com o que faz e quando usar,
   até 1024 caracteres.
3. **Ligar na máquina:** `bash install.sh --link` no clone. Ele cria só os links que faltam e
   não mexe nas outras.
4. **Conferir:** `python3 scripts/conferir.py` no clone (frontmatter, nomes, tokens e o
   instalador).
5. **Publicar:** commit em português e push na `main` do clone. Confira o CI com
   `gh run list -R gustavocamin/agent-skills --limit 1`.

## Casos

- **Editou uma skill direto em `~/.claude/skills`:** como é link, a edição já está no clone;
  faça os passos 4 e 5.
- **Skill copiada (não link) numa máquina:** `bash scripts/sincronizar.sh` traz a versão local
  para o clone, ou `--nova <pasta>` para uma skill que o repo ainda não tem.
- **Skill de projeto mudou** (ex.: curso-lab, `.claude/skills/`): `bash scripts/sincronizar.sh
  --projeto <projeto> <caminho do repo>` e os passos 4 e 5.
- **Skill de terceiros** (`TERCEIROS.md`): não edite; copie de novo da origem num commit novo
  e troque o hash.
- **Remover:** apague a pasta no clone, remova os links (`rm ~/.claude/skills/<nome>
  ~/.agents/skills/<nome>`, que só apaga o link) e faça os passos 4 e 5.
