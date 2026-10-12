#!/usr/bin/env bash
# Instala as skills gerais e, opcionalmente, as de projetos, com atualização segura.
# Dependências: bash, Python 3.10+ e git. Veja --help para destinos e simulação.
set -euo pipefail
if ! command -v python3 >/dev/null 2>&1; then
  printf '%s\n' 'install: dependência ausente: python3 (Python 3.10+)' >&2
  exit 1
fi
if ! python3 -c 'import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)'; then
  printf '%s\n' 'install: requer Python 3.10 ou mais recente' >&2
  exit 1
fi
base=${BASH_SOURCE[0]%/*}
[ "$base" != "${BASH_SOURCE[0]}" ] || base=.
repo=$(cd "$base" && pwd)
exec python3 -B "$repo/scripts/instalar.py" "$@"
