#!/usr/bin/env bash
# Mede o disco e os candidatos a limpeza, sem apagar nada. Saída em linhas
# "<MB>\t<categoria>\t<caminho>", da maior para a menor, depois do resumo do df.
#
#   bash medir.sh [pasta de projetos ...]
#
# As pastas de projetos (padrão: ~/Documents e ~/code) são varridas até 6 níveis atrás de
# node_modules, venvs e worktrees de agentes. Pastas do iCloud sem ".nosync" no caminho não
# entram na busca de node_modules/venv: ler arquivos esvaziados pelo iCloud baixa tudo de volta.
set -uo pipefail

if [ "$(uname -s)" = Darwin ]; then
  df -h /System/Volumes/Data 2>/dev/null | tail -1 | awk '{print "disco: " $4 " livres de " $2 " (" $5 " usados)"}'
else
  df -h "$HOME" | tail -1 | awk '{print "disco: " $4 " livres de " $2 " (" $5 " usados)"}'
fi
echo

mb() { du -sk "$1" 2>/dev/null | awk '{printf "%d", $1 / 1024}'; }
linha() {  # categoria caminho
  [ -e "$2" ] || return 0
  local t
  t=$(mb "$2")
  [ "${t:-0}" -ge 50 ] && printf '%s\t%s\t%s\n' "$t" "$1" "$2"
}

{
  # Caches que se refazem sozinhos.
  linha cache-npm "$HOME/.npm"
  linha cache-pip "$HOME/Library/Caches/pip"
  linha cache-pip "$HOME/.cache/pip"
  linha cache-uv "$HOME/.cache/uv"
  linha cache-homebrew "$HOME/Library/Caches/Homebrew"
  linha cache-pnpm "$HOME/Library/pnpm/store"
  linha cache-yarn "$HOME/Library/Caches/Yarn"
  linha cache-playwright "$HOME/Library/Caches/ms-playwright"
  linha cache-go "$HOME/Library/Caches/go-build"
  linha cache-xcode "$HOME/Library/Developer/Xcode/DerivedData"
  linha xcode-simuladores "$HOME/Library/Developer/CoreSimulator/Devices"
  linha xcode-suporte-ios "$HOME/Library/Developer/Xcode/iOS DeviceSupport"
  linha docker "$HOME/Library/Containers/com.docker.docker/Data"
  linha lixeira "$HOME/.Trash"
  # Outros caches grandes de ~/Library/Caches (apps), um por um.
  for d in "$HOME"/Library/Caches/*/; do
    case $d in */pip/ | */Homebrew/ | */Yarn/ | */ms-playwright/ | */go-build/) continue ;; esac
    linha cache-app "${d%/}"
  done
  # Worktrees de agentes.
  for d in "$HOME"/.codex/worktrees/*/; do linha worktree-codex "${d%/}"; done

  raizes=("$@")
  [ ${#raizes[@]} -eq 0 ] && raizes=("$HOME/Documents" "$HOME/code")
  for raiz in "${raizes[@]}"; do
    [ -d "$raiz" ] || continue
    while IFS= read -r d; do
      linha worktree-claude "$d"
    done < <(find "$raiz" -maxdepth 6 -type d -path '*/.claude/worktrees/*' -prune 2>/dev/null)
    while IFS= read -r d; do
      case $d in */.claude/worktrees/*) continue ;; esac
      case $d in *.nosync*) ;; "$HOME/Documents"* | "$HOME/Desktop"*) continue ;; esac
      case $(basename "$d") in
        node_modules) linha node_modules "$d" ;;
        *) [ -f "$d/pyvenv.cfg" ] && linha venv "$d" ;;
      esac
    done < <(find "$raiz" -maxdepth 6 -type d \( -name node_modules -o -name '.venv*' -o -name venv \) -prune 2>/dev/null)
  done
} | sort -t$'\t' -k1,1nr
