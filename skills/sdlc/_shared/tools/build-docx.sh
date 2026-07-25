#!/usr/bin/env bash
#
# build-docx.sh — render a feature document to DOCX for stakeholders.
#
#   tools/docx/build-docx.sh docs/features/<slug>/technical-doc.md
#
# Renders any Mermaid sources in the document's sibling diagrams/ directory
# to PNG, then converts the markdown to DOCX with pandoc. The .md is the
# source of truth and is committed; the .docx is a regenerable artifact and
# should be gitignored.
#
# Requires: pandoc. Optionally mermaid-cli (mmdc) to render diagrams — if it
# is missing, existing PNGs are reused and the script says what it skipped.

set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "usage: $(basename "$0") <path/to/document.md>" >&2
  exit 64
fi

SOURCE="$1"

if [[ ! -f "$SOURCE" ]]; then
  echo "error: no such file: $SOURCE" >&2
  exit 66
fi

if ! command -v pandoc >/dev/null 2>&1; then
  cat >&2 <<'MSG'
error: pandoc is not installed — it is what produces the DOCX.

  macOS:  brew install pandoc
  Debian: sudo apt install pandoc

See https://pandoc.org/installing.html for other platforms.
MSG
  exit 69
fi

SOURCE_DIR="$(cd "$(dirname "$SOURCE")" && pwd)"
BASENAME="$(basename "$SOURCE" .md)"
DIAGRAMS_DIR="$SOURCE_DIR/diagrams"
OUTPUT="$SOURCE_DIR/$BASENAME.docx"

# ---------------------------------------------------------------------------
# Diagrams: .mmd -> .png
# ---------------------------------------------------------------------------

shopt -s nullglob
MERMAID_SOURCES=("$DIAGRAMS_DIR"/*.mmd)
shopt -u nullglob

if [[ ${#MERMAID_SOURCES[@]} -gt 0 ]]; then
  if command -v mmdc >/dev/null 2>&1; then
    for mmd in "${MERMAID_SOURCES[@]}"; do
      png="${mmd%.mmd}.png"
      # Re-render only when the source is newer than the rendered output.
      if [[ ! -f "$png" || "$mmd" -nt "$png" ]]; then
        echo "rendering $(basename "$mmd") → $(basename "$png")"
        mmdc --input "$mmd" --output "$png" --backgroundColor white
      fi
    done
  else
    echo "warning: mmdc (mermaid-cli) not found — not rendering diagrams." >&2
    echo "         Install with: npm install -g @mermaid-js/mermaid-cli" >&2
    missing=0
    for mmd in "${MERMAID_SOURCES[@]}"; do
      [[ -f "${mmd%.mmd}.png" ]] || { echo "         missing: $(basename "${mmd%.mmd}.png")" >&2; missing=1; }
    done
    if [[ $missing -eq 1 ]]; then
      echo "warning: the DOCX will have broken image references." >&2
    fi
  fi
fi

# ---------------------------------------------------------------------------
# Markdown -> DOCX
# ---------------------------------------------------------------------------

PANDOC_ARGS=(
  "$SOURCE"
  --output "$OUTPUT"
  --from gfm
  --resource-path "$SOURCE_DIR"
  --toc
  --toc-depth=2
)

# An optional house style: drop a reference.docx next to this script to
# control fonts, heading styles and page setup.
REFERENCE_DOCX="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/reference.docx"
if [[ -f "$REFERENCE_DOCX" ]]; then
  PANDOC_ARGS+=(--reference-doc "$REFERENCE_DOCX")
fi

pandoc "${PANDOC_ARGS[@]}"

echo "wrote $OUTPUT"
