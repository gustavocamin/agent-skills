#!/usr/bin/env bash
# Traz para este repo a versão local das skills (o caminho inverso do install.sh), para depois
# conferir, fazer commit e push. Só atualiza skills que já estão no repo; uma skill nova entra
# com --nova <caminho da pasta da skill> [--projeto <nome>].
#
#   bash scripts/sincronizar.sh                                   # skills/ ← ~/.claude/skills
#   bash scripts/sincronizar.sh --projeto curso-lab-agent <repo>  # projetos/curso-lab-agent/ ← <repo>/.claude/skills
#   bash scripts/sincronizar.sh --nova ~/.claude/skills/minha-skill
#
# As skills de terceiros (TERCEIROS.md) não vêm da máquina: atualizam-se pelo repo de origem.
set -euo pipefail

repo=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
terceiros=$(sed -n 's/^| `\([a-z0-9-]*\)` |.*/\1/p' "$repo/TERCEIROS.md")

copiar() {
  local origem=$1 alvo=$2
  if [ ! -f "$origem/SKILL.md" ]; then
    echo "sincronizar: $origem não tem SKILL.md; pulei" >&2
    return
  fi
  rsync -a --delete --exclude .DS_Store --exclude __pycache__ "$origem/" "$alvo/"
  echo "sincronizar: $alvo ← $origem"
}

case ${1:-} in
  "")
    for dir in "$repo"/skills/*/; do
      nome=$(basename "$dir")
      if printf '%s\n' "$terceiros" | grep -qxF "$nome"; then continue; fi
      origem="$HOME/.claude/skills/$nome"
      if [ -d "$origem" ]; then copiar "$origem" "${dir%/}"; else echo "sincronizar: sem $origem; pulei"; fi
    done
    ;;
  --projeto)
    nome=${2:?--projeto pede um nome}
    fonte=${3:?--projeto pede o caminho do repo do projeto}
    mkdir -p "$repo/projetos/$nome"
    for dir in "$fonte"/.claude/skills/*/; do
      copiar "${dir%/}" "$repo/projetos/$nome/$(basename "$dir")"
    done
    ;;
  --nova)
    origem=${2:?--nova pede a pasta da skill}
    origem=${origem%/}
    if [ "${3:-}" = --projeto ]; then
      alvo="$repo/projetos/${4:?--projeto pede um nome}/$(basename "$origem")"
    else
      alvo="$repo/skills/$(basename "$origem")"
    fi
    mkdir -p "$(dirname "$alvo")"
    copiar "$origem" "$alvo"
    ;;
  -h | --help) sed -n '2,10p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//' ;;
  *) echo "sincronizar: opção desconhecida: $1" >&2; exit 2 ;;
esac

git -C "$repo" status --short
