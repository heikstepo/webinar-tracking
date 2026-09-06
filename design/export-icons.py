#!/usr/bin/env python3
"""Cut the named elements out of a slide as standalone files.

    python3 export-icons.py slides/webinar-and-vsl.html exports/icons

Writes, per .piece on the page:
  <name>.png   the element — drawing and caption — on a transparent ground
  <name>.svg   the drawing alone, as vector, with the stroke colours resolved

The PNG is shot through Playwright with omit_background, because Chrome's
print-to-pdf path always paints a white page and would hand back a white box
instead of a transparent one.
"""
import os, re, sys
from playwright.sync_api import sync_playwright

src = os.path.abspath(sys.argv[1])
out = os.path.abspath(sys.argv[2] if len(sys.argv) > 2 else 'exports/icons')
os.makedirs(out, exist_ok=True)

CHROME = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'

with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=CHROME,
                           args=['--force-color-profile=srgb', '--font-render-hinting=none'])
    pg = b.new_page(viewport={'width': 1440, 'height': 810}, device_scale_factor=4)
    pg.goto('file://' + src)

    # Strip the card and the ground: what ships is the drawing and its name,
    # so it can be dropped onto any background without a white slab behind it.
    pg.add_style_tag(content='''
      html, body { background: transparent !important; }
      .slide { background: transparent !important; }
      .piece { background: transparent !important; box-shadow: none !important;
               padding: 0 !important; width: auto !important; }
      .piece svg { width: 220px !important; height: 220px !important; }
      .piece__name { font-size: 46px !important; margin-top: 22px !important; }
    ''')

    names = pg.eval_on_selector_all('.piece__name', 'els => els.map(e => e.textContent.trim())')
    for i, name in enumerate(names):
        slug = re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')
        pg.locator('.piece').nth(i).screenshot(
            path=os.path.join(out, slug + '.png'), omit_background=True)

        # The vector, with computed stroke/fill baked in so the file stands on
        # its own — the colours live in the stylesheet, not in the markup.
        svg = pg.locator('.piece svg').nth(i).evaluate('''el => {
          const c = el.cloneNode(true);
          const src = el.querySelectorAll('*'), dst = c.querySelectorAll('*');
          const root = getComputedStyle(el);
          src.forEach((s, j) => {
            const cs = getComputedStyle(s), d = dst[j];
            d.setAttribute('stroke', cs.stroke);
            d.setAttribute('fill', cs.fill);
            d.setAttribute('stroke-width', cs.strokeWidth);
            d.removeAttribute('class');
          });
          c.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
          c.setAttribute('width', '220'); c.setAttribute('height', '220');
          c.setAttribute('stroke-linecap', root.strokeLinecap);
          c.setAttribute('stroke-linejoin', root.strokeLinejoin);
          return c.outerHTML;
        }''')
        open(os.path.join(out, slug + '.svg'), 'w').write(svg + '\n')
        print('wrote', slug + '.png', 'and', slug + '.svg')
    b.close()
