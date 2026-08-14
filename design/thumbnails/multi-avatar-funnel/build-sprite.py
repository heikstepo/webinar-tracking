#!/usr/bin/env python3
"""Inline the brand marks in assets/img/*.svg into index.html as an SVG sprite.

CSS mask-image pointing at an SVG file is silently dropped when the page is
loaded over file:// (opaque origin), so the logos have to live in the document.
Each symbol uses fill="currentColor", which lets .lg-<name>{color:...} in the
stylesheet set the brand colour.

Run after adding or replacing anything in assets/img/.
"""
import re
import pathlib
import sys

HERE = pathlib.Path(__file__).parent
LOGOS = [
    "meta", "instagram", "tiktok", "youtube", "googleads", "linkedin",
    "calendly", "hubspot", "twilio", "gmail", "zapier", "stripe",
    "reddit", "zoom", "slack", "notion", "whatsapp", "snapchat",
    "googlesheets", "x",
]

symbols = []
for name in LOGOS:
    path = HERE / "assets" / "img" / f"{name}.svg"
    if not path.exists():
        print(f"skip {name}: no {path.name}", file=sys.stderr)
        continue
    src = path.read_text()
    viewbox = re.search(r'viewBox="([^"]+)"', src)
    paths = re.findall(r'<path[^>]*\sd="([^"]+)"', src)
    if not (viewbox and paths):
        print(f"skip {name}: no path/viewBox", file=sys.stderr)
        continue
    inner = "".join(f'<path d="{d}"/>' for d in paths)
    symbols.append(
        f'  <symbol id="lg-{name}" viewBox="{viewbox.group(1)}" '
        f'fill="currentColor">{inner}</symbol>'
    )

sprite = (
    '<!--SPRITE:START-->\n'
    '<svg width="0" height="0" style="position:absolute" aria-hidden="true">\n'
    + "\n".join(symbols)
    + "\n</svg>\n<!--SPRITE:END-->"
)

target = HERE / "index.html"
html = target.read_text()
patched, count = re.subn(
    r"<!--SPRITE:START-->.*?<!--SPRITE:END-->", lambda _: sprite, html, flags=re.S
)
if not count:
    sys.exit("index.html is missing the <!--SPRITE:START--> / <!--SPRITE:END--> markers")

target.write_text(patched)
print(f"inlined {len(symbols)} logo symbols into {target.name}")
