#!/usr/bin/env bash
# Measure every slide named in deck-order.txt and emit one JSON object per
# slide into exports/measured.json, keyed by slide name.
#
#   ./measure.sh
#
# Uses Chrome's --dump-dom, so the geometry is whatever Chrome really laid
# out — the same engine that produced the PNG deck.

set -euo pipefail

DIR="$(cd "$(dirname "$0")" && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

CHROME="${CHROME:-}"
if [ -z "$CHROME" ]; then
  for c in \
    "/opt/pw-browsers/chromium-1194/chrome-linux/chrome" \
    "$(command -v google-chrome || true)" \
    "$(command -v chromium || true)"; do
    [ -x "$c" ] && CHROME="$c" && break
  done
fi
[ -n "$CHROME" ] || { echo "No Chrome found. Set CHROME=/path/to/chrome" >&2; exit 1; }

mkdir -p "$DIR/exports"

while IFS= read -r name; do
  [ -n "$name" ] || continue
  python3 "$DIR/build-standalone.py" "$DIR/slides/$name.html" "$TMP/$name.html" >/dev/null
  # Inject the measuring pass just before </body>.
  python3 - "$TMP/$name.html" "$DIR/measure.js" <<'PY'
import sys
page, script = sys.argv[1], sys.argv[2]
html = open(page, encoding='utf-8').read()
js = open(script, encoding='utf-8').read()
html = html.replace('</body>', '<script>' + js + '</script></body>', 1)
open(page, 'w', encoding='utf-8').write(html)
PY

  "$CHROME" --headless --disable-gpu --no-sandbox \
    --virtual-time-budget=3000 --window-size=1440,810 \
    --dump-dom "file://$TMP/$name.html" > "$TMP/$name.dom" 2>/dev/null
done < "$DIR/deck-order.txt"

python3 - "$TMP" "$DIR/deck-order.txt" "$DIR/exports/measured.json" <<'PY'
import html, json, re, sys
tmp, order_file, out_file = sys.argv[1:4]
order = [l.strip() for l in open(order_file) if l.strip()]
measured = {}
for name in order:
    dom = open(f'{tmp}/{name}.dom', encoding='utf-8').read()
    m = re.search(r'<pre id="measure-out">(.*?)</pre>', dom, re.S)
    if not m:
        raise SystemExit(f'{name}: no measurement in dumped DOM')
    measured[name] = json.loads(html.unescape(m.group(1)))
json.dump(measured, open(out_file, 'w'), indent=1)
print(f'measured {len(measured)} slides -> {out_file}')
PY
