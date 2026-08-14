#!/usr/bin/env python3
"""
Fold a slide file's stylesheet and fonts into a single self-contained HTML file.

    python3 build-standalone.py elements.html            -> elements.standalone.html
    python3 build-standalone.py deck.html out.html

The result has no external requests at all, so it renders identically from
file://, from a server, from an email attachment, or inside a sandboxed
viewer that blocks third-party hosts.
"""

import base64
import pathlib
import re
import sys


def inline_fonts(css: str, css_dir: pathlib.Path) -> str:
    """Replace url('fonts/x.woff2') with a base64 data URI."""

    def sub(match: re.Match) -> str:
        rel = match.group("path")
        if rel.startswith("data:"):
            return match.group(0)
        font = (css_dir / rel).resolve()
        if not font.exists():
            print(f"  ! font not found, left as-is: {rel}", file=sys.stderr)
            return match.group(0)
        b64 = base64.b64encode(font.read_bytes()).decode("ascii")
        print(f"  + inlined {rel} ({font.stat().st_size // 1024} KB)")
        return f"url('data:font/woff2;base64,{b64}') format('woff2')"

    return re.sub(
        r"url\(['\"]?(?P<path>[^'\")]+\.woff2)['\"]?\)\s*format\(['\"]woff2['\"]\)",
        sub,
        css,
    )


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 1

    src = pathlib.Path(sys.argv[1]).resolve()
    dst = (
        pathlib.Path(sys.argv[2]).resolve()
        if len(sys.argv) > 2
        else src.with_suffix(".standalone.html")
    )

    html = src.read_text(encoding="utf-8")
    print(f"reading {src.name}")

    def replace_link(match: re.Match) -> str:
        href = match.group("href")
        if href.startswith(("http://", "https://", "//")):
            return match.group(0)
        css_path = (src.parent / href).resolve()
        if not css_path.exists():
            print(f"  ! stylesheet not found, left as-is: {href}", file=sys.stderr)
            return match.group(0)
        print(f"  + inlined {href} ({css_path.stat().st_size // 1024} KB)")
        css = inline_fonts(css_path.read_text(encoding="utf-8"), css_path.parent)
        return f"<style>\n{css}\n</style>"

    out = re.sub(
        r"""<link[^>]*rel=["']stylesheet["'][^>]*href=["'](?P<href>[^"']+)["'][^>]*>""",
        replace_link,
        html,
    )

    dst.write_text(out, encoding="utf-8")
    print(f"wrote {dst.name} ({len(out.encode('utf-8')) // 1024} KB)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
