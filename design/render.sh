#!/usr/bin/env bash
# Render a slide file to PDF and a 2x PNG.
#
#   ./render.sh slides/funnel.html          -> exports/funnel.pdf, exports/funnel.png
#   ./render.sh slides/funnel.html 3        -> 3x PNG
#
# Uses Chrome's own print path, so the output is identical to doing
# File > Print > Save as PDF by hand (margins none, 100%, backgrounds on).

set -euo pipefail

SRC="${1:?usage: render.sh <slide.html> [scale]}"
SCALE="${2:-2}"
DIR="$(cd "$(dirname "$0")" && pwd)"
NAME="$(basename "$SRC" .html)"
OUT="$DIR/exports"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

CHROME="${CHROME:-}"
if [ -z "$CHROME" ]; then
  for c in \
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
    "/opt/pw-browsers/chromium-1194/chrome-linux/chrome" \
    "$(command -v google-chrome || true)" \
    "$(command -v chromium || true)"; do
    [ -x "$c" ] && CHROME="$c" && break
  done
fi
[ -n "$CHROME" ] || { echo "No Chrome found. Set CHROME=/path/to/chrome" >&2; exit 1; }

mkdir -p "$OUT"

# Fold CSS + font in first so the render has no external requests to wait on.
python3 "$DIR/build-standalone.py" "$DIR/$SRC" "$TMP/$NAME.html" >/dev/null

"$CHROME" --headless --disable-gpu --no-sandbox --no-pdf-header-footer \
  --virtual-time-budget=3000 \
  --print-to-pdf="$OUT/$NAME.pdf" "file://$TMP/$NAME.html" 2>/dev/null

if command -v pdftoppm >/dev/null; then
  pdftoppm -png -r "$((96 * SCALE))" "$OUT/$NAME.pdf" "$TMP/page" 2>/dev/null
  # Single-slide files produce one page; decks keep their page numbers.
  count=$(find "$TMP" -name 'page-*.png' | wc -l | tr -d ' ')
  if [ "$count" = "1" ]; then
    mv "$TMP"/page-*.png "$OUT/$NAME.png"
    echo "wrote exports/$NAME.pdf and exports/$NAME.png (${SCALE}x)"
  else
    i=1
    for f in "$TMP"/page-*.png; do
      mv "$f" "$OUT/$NAME-$i.png"; i=$((i + 1))
    done
    echo "wrote exports/$NAME.pdf and $count PNG pages (${SCALE}x)"
  fi
else
  echo "wrote exports/$NAME.pdf (install poppler-utils for PNG output)"
fi
