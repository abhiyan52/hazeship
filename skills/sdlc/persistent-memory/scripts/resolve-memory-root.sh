#!/usr/bin/env bash
#
# resolve-memory-root.sh — print the absolute path of the persistent-memory
# store root for the current working directory.
#
# Resolution order (first hit wins):
#   1. $HAZESHIP_MEMORY_DIR                       (source: env)
#   2. nearest ancestor containing a .hazeship/    (source: marker)
#        - if that .hazeship/config.env sets HAZESHIP_MEMORY_DIR, use it
#        - otherwise use <marker>/.hazeship/memory
#   3. nothing found                               (source: default)
#        - prints the proposed root (<repo root>/.hazeship/memory) and
#          exits 3, unless --init is passed, in which case the marker and
#          config are created and it exits 0 (source: created)
#
# stdout is always exactly one line: the absolute store root.
# Usage: resolve-memory-root.sh [--start DIR] [--init] [--why]

set -euo pipefail

start=$PWD
do_init=0
why=0

while [ $# -gt 0 ]; do
  case $1 in
    --start) start=${2:?--start needs a directory}; shift 2 ;;
    --init) do_init=1; shift ;;
    --why) why=1; shift ;;
    -h|--help) sed -n '2,25p' "$0"; exit 0 ;;
    *) echo "resolve-memory-root.sh: unknown argument: $1" >&2; exit 2 ;;
  esac
done

[ -d "$start" ] || { echo "resolve-memory-root.sh: not a directory: $start" >&2; exit 2; }
start=$(cd "$start" && pwd)

# Expand a leading ~ and make the path absolute relative to $2.
abspath() {
  local path=$1 base=$2
  case $path in
    "~") path=$HOME ;;
    "~/"*) path=$HOME/${path#\~/} ;;
  esac
  case $path in
    /*) printf '%s\n' "$path" ;;
    *) printf '%s\n' "$base/$path" ;;
  esac
}

report() {
  [ "$why" -eq 1 ] && echo "source=$1" >&2
  printf '%s\n' "$2"
}

# 1. Explicit environment override.
if [ -n "${HAZESHIP_MEMORY_DIR:-}" ]; then
  report env "$(abspath "$HAZESHIP_MEMORY_DIR" "$start")"
  exit 0
fi

# 2. Nearest ancestor with a .hazeship/ marker directory. Nearest wins, so a
#    nested package may keep its own store while a plain repo (or $HOME)
#    resolves to the single one above it.
dir=$start
while :; do
  if [ -d "$dir/.hazeship" ]; then
    cfg=$dir/.hazeship/config.env
    configured=
    if [ -f "$cfg" ]; then
      # Read the key without sourcing the file.
      configured=$(sed -n 's/^[[:space:]]*HAZESHIP_MEMORY_DIR[[:space:]]*=[[:space:]]*//p' "$cfg" | tail -n1)
      configured=${configured%%#*}
      configured=${configured%"${configured##*[![:space:]]}"}
      configured=${configured#\"}; configured=${configured%\"}
      configured=${configured#\'}; configured=${configured%\'}
    fi
    if [ -n "$configured" ]; then
      report marker "$(abspath "$configured" "$dir")"
    else
      report marker "$dir/.hazeship/memory"
    fi
    exit 0
  fi
  [ "$dir" = "/" ] && break
  dir=$(dirname "$dir")
done

# 3. Nothing configured yet — propose the repo root. --git-common-dir keeps
#    git worktrees pointed at the main checkout's store instead of creating a
#    throwaway one per worktree.
root=$start
if common=$(git -C "$start" rev-parse --git-common-dir 2>/dev/null) && [ -n "$common" ]; then
  common=$(cd "$start" && cd "$common" && pwd)
  root=$(dirname "$common")
fi

proposed=$root/.hazeship/memory

if [ "$do_init" -eq 1 ]; then
  mkdir -p "$proposed/buckets"
  cfg=$root/.hazeship/config.env
  if [ ! -f "$cfg" ]; then
    cat >"$cfg" <<'EOF'
# hazeship persistent-memory configuration.
# Leave HAZESHIP_MEMORY_DIR unset to use ./memory next to this file, or point
# it at any absolute path (a shared store outside the repo, for example).
# HAZESHIP_MEMORY_DIR=
EOF
  fi
  report created "$proposed"
  exit 0
fi

report default "$proposed"
exit 3
