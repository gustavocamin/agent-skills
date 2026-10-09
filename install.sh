#!/usr/bin/env bash
# Instala as skills deste repo nas pastas pessoais do Claude Code (~/.claude/skills) e do Codex
# (~/.agents/skills). Feito para o script de setup de um ambiente cloud e para a máquina local.
#
#   bash install.sh                          # skills gerais (skills/), cópia
#   bash install.sh --projeto curso-lab-agent  # + as de projetos/curso-lab-agent/
#   bash install.sh --link                   # link em vez de cópia (máquina local, clone fixo)
#   bash install.sh --destino <pasta>        # só nessa pasta (repete-se a opção para várias)
#
# Nunca sobrescreve uma skill que já existe e difere, salvo com --forcar. Rodado de novo, só
# atualiza o que mudou. Se nenhuma pasta pessoal tem escrita (no Codex cloud o HOME é só de
# leitura), instala em <repo atual>/.agents/skills e tira as pastas novas do git pelo
# .git/info/exclude, para não sujar o repo da tarefa.
set -euo pipefail

repo=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)

uso() {
  sed -n '2,9p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
}

destinos=()
projetos=()
modo=copia
forcar=0
while [ $# -gt 0 ]; do
  case $1 in
    --destino) destinos+=("${2:?--destino pede uma pasta}"); shift 2 ;;
    --projeto) projetos+=("${2:?--projeto pede um nome}"); shift 2 ;;
    --link) modo=link; shift ;;
    --forcar) forcar=1; shift ;;
    -h | --help) uso; exit 0 ;;
    *) echo "install: opção desconhecida: $1" >&2; uso >&2; exit 2 ;;
  esac
done

real() { python3 -c 'import os, sys; print(os.path.realpath(sys.argv[1]))' "$1"; }

# Origens: skills/ sempre; projetos/<nome>/ só quando pedido.
origens=()
for dir in "$repo"/skills/*/; do origens+=("${dir%/}"); done
for p in ${projetos[@]+"${projetos[@]}"}; do
  if [ ! -d "$repo/projetos/$p" ]; then
    echo "install: projeto '$p' não existe em projetos/ ($(ls "$repo/projetos" | tr '\n' ' '))" >&2
    exit 2
  fi
  for dir in "$repo/projetos/$p"/*/; do origens+=("${dir%/}"); done
done

# Destinos: os pedidos, ou as pastas pessoais com escrita, ou o repo atual.
if [ ${#destinos[@]} -eq 0 ]; then
  for d in "$HOME/.claude/skills" "$HOME/.agents/skills"; do
    if mkdir -p "$d" 2>/dev/null && [ -w "$d" ]; then
      destinos+=("$d")
    else
      echo "install: sem escrita em $d; pulei"
    fi
  done
  if [ ${#destinos[@]} -eq 0 ]; then
    topo=$(git rev-parse --show-toplevel 2>/dev/null || true)
    if [ -n "$topo" ] && [ "$(real "$topo")" = "$(real "$repo")" ]; then topo=; fi
    # A doc do Codex cloud não diz em que pasta o setup roda; o repo da tarefa fica em
    # /workspace/<repo>. Fora de um repo, vale o único repo git dessa pasta.
    if [ -z "$topo" ]; then
      candidatos=()
      for g in "${AGENT_SKILLS_WORKSPACE:-/workspace}"/*/.git; do
        if [ -e "$g" ] && [ "$(real "${g%/.git}")" != "$(real "$repo")" ]; then candidatos+=("${g%/.git}"); fi
      done
      if [ ${#candidatos[@]} -eq 1 ]; then topo=${candidatos[0]}; fi
    fi
    if [ -z "$topo" ]; then
      echo "install: nenhuma pasta pessoal com escrita e nenhum repo de tarefa no diretório atual nem em ${AGENT_SKILLS_WORKSPACE:-/workspace}" >&2
      exit 1
    fi
    destinos+=("$topo/.agents/skills")
    echo "install: instalando no repo da tarefa, em $topo/.agents/skills"
  fi
fi

# Uma pasta instalada dentro de um repo git vai para o .git/info/exclude dele.
excluir_do_git() {
  local alvo=$1 topo git_dir rel
  topo=$(git -C "$(dirname "$alvo")" rev-parse --show-toplevel 2>/dev/null) || return 0
  git_dir=$(git -C "$topo" rev-parse --path-format=absolute --git-common-dir)
  rel=$(python3 -c 'import os, sys; print(os.path.relpath(os.path.realpath(sys.argv[1]), os.path.realpath(sys.argv[2])))' "$alvo" "$topo")
  mkdir -p "$git_dir/info"
  touch "$git_dir/info/exclude"
  grep -qxF "/$rel/" "$git_dir/info/exclude" || echo "/$rel/" >>"$git_dir/info/exclude"
}

instaladas=0 iguais=0 puladas=0
for destino in "${destinos[@]}"; do
  mkdir -p "$destino"
  for origem in "${origens[@]}"; do
    nome=$(basename "$origem")
    alvo="$destino/$nome"
    if [ -e "$alvo" ] || [ -L "$alvo" ]; then
      if [ "$(real "$alvo")" = "$(real "$origem")" ]; then
        iguais=$((iguais + 1)); continue
      fi
      if [ $modo = copia ] && diff -rq -x .DS_Store "$origem" "$alvo" >/dev/null 2>&1; then
        iguais=$((iguais + 1)); continue
      fi
      if [ $forcar = 0 ]; then
        echo "install: $alvo já existe e difere; pulei (use --forcar para substituir)"
        puladas=$((puladas + 1)); continue
      fi
      rm -rf "$alvo"
    fi
    if [ $modo = link ]; then
      ln -s "$origem" "$alvo"
    else
      cp -R "$origem" "$alvo"
    fi
    excluir_do_git "$alvo"
    echo "install: $nome → $destino"
    instaladas=$((instaladas + 1))
  done
done
echo "install: $instaladas instaladas, $iguais já atualizadas, $puladas puladas (${#origens[@]} skills × ${#destinos[@]} destinos)"
