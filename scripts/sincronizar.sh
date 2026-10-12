#!/usr/bin/env bash
# Traz para este repo a versão local das skills (o caminho inverso do install.sh), para depois
# conferir, fazer commit e push. Só atualiza skills que já estão no repo; uma skill nova entra
# com --nova <caminho da pasta da skill> [--projeto <nome>].
#
#   bash scripts/sincronizar.sh                                   # skills/ ← ~/.claude/skills
#   bash scripts/sincronizar.sh --projeto curso-lab-agent <repo>  # projetos/curso-lab-agent/ ← <repo>/.claude/{skills,commands,agents}
#   bash scripts/sincronizar.sh --nova ~/.claude/skills/minha-skill
#
# As skills de terceiros (TERCEIROS.md) não vêm da máquina: atualizam-se pelo repo de origem.
set -euo pipefail

repo=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
terceiros=$(sed -n 's/^| `\([a-z0-9-]*\)` |.*/\1/p' "$repo/TERCEIROS.md")

terceira() {
  printf '%s\n' "$terceiros" | grep -qxF -- "$1"
}

validar_projeto() {
  if [[ ! $1 =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]]; then
    echo "sincronizar: nome de projeto inválido: $1" >&2
    return 1
  fi
  if [ "$1" = databricks ]; then
    echo "sincronizar: projeto databricks é de terceiros; atualize da origem e registre o commit em TERCEIROS.md" >&2
    return 1
  fi
}

validar_caminhos() {
  # Verifica antes de mkdir/rsync/cp, sem normalizar um link seguido de '..' às cegas.
  if ! command -v python3 >/dev/null 2>&1; then
    echo "sincronizar: dependência ausente: python3" >&2
    return 1
  fi
  python3 -B - "$repo" "$1" "$2" <<'PYTHON'
import os
from pathlib import Path
import sys


def seguro(raw):
    path = Path(raw).expanduser()
    current = Path(path.anchor) if path.is_absolute() else Path.cwd()
    for component in path.parts:
        if component in (path.anchor, '.'):
            continue
        current = current.parent if component == '..' else current / component
        if current.is_symlink():
            raise ValueError(f"caminho contém link simbólico: {current}")
    return Path(os.path.abspath(str(path)))


try:
    root, source, target = map(seguro, sys.argv[1:])
    if root == target or root not in target.parents:
        raise ValueError(f"destino fora do clone: {target}")
    if source == target or source in target.parents or target in source.parents:
        raise ValueError("origem e destino se sobrepõem; não há o que sincronizar com segurança")
    if source.is_dir():
        for folder, dirs, files in os.walk(source, followlinks=False):
            for name in dirs + files:
                item = Path(folder) / name
                if item.is_symlink():
                    raise ValueError(f"origem contém link simbólico: {item}")
    if target.is_dir():
        for folder, dirs, files in os.walk(target, followlinks=False):
            for name in dirs + files:
                item = Path(folder) / name
                if item.is_symlink():
                    raise ValueError(f"destino contém link simbólico: {item}")
except (ValueError, OSError) as error:
    print(f"sincronizar: {error}; nada copiado para este destino", file=sys.stderr)
    sys.exit(1)
PYTHON
}

copiar() {
  local origem=$1 alvo=$2
  if terceira "$(basename "$alvo")"; then
    echo "sincronizar: $(basename "$alvo") é de terceiros; atualize da origem e registre o commit em TERCEIROS.md" >&2
    return 1
  fi
  if [ ! -f "$origem/SKILL.md" ]; then
    echo "sincronizar: $origem não tem SKILL.md; pulei" >&2
    return
  fi
  validar_caminhos "$origem" "$alvo"
  mkdir -p "$(dirname "$alvo")"
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
    validar_projeto "$nome"
    fonte=${3:?--projeto pede o caminho do repo do projeto}
    for dir in "$fonte"/.claude/skills/*/; do
      [ -L "${dir%/}" ] && continue  # link para este repo: já é a fonte
      [ -d "$dir" ] && copiar "${dir%/}" "$repo/projetos/$nome/skills/$(basename "$dir")"
    done
    for tipo in commands agents; do
      for f in "$fonte/.claude/$tipo"/*.md; do
        [ -f "$f" ] && [ ! -L "$f" ] || continue
        validar_caminhos "$f" "$repo/projetos/$nome/$tipo/$(basename "$f")"
        mkdir -p "$repo/projetos/$nome/$tipo"
        cp "$f" "$repo/projetos/$nome/$tipo/" && echo "sincronizar: projetos/$nome/$tipo/$(basename "$f") ← $f"
      done
    done
    ;;
  --nova)
    origem=${2:?--nova pede a pasta da skill}
    origem=${origem%/}
    if [[ ! $(basename "$origem") =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]]; then
      echo "sincronizar: nome de skill inválido: $(basename "$origem")" >&2
      exit 1
    fi
    if terceira "$(basename "$origem")"; then
      echo "sincronizar: $(basename "$origem") é de terceiros; não importei a cópia local" >&2
      exit 1
    fi
    if [ "${3:-}" = --projeto ]; then
      nome=${4:?--projeto pede um nome}
      validar_projeto "$nome"
      alvo="$repo/projetos/$nome/skills/$(basename "$origem")"
    else
      alvo="$repo/skills/$(basename "$origem")"
    fi
    copiar "$origem" "$alvo"
    ;;
  -h | --help) sed -n '2,10p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//' ;;
  *) echo "sincronizar: opção desconhecida: $1" >&2; exit 2 ;;
esac

git -C "$repo" status --short
