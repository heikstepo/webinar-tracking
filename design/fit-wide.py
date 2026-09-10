#!/usr/bin/env python3
"""Scale each 16:9 slide's content up to fill the frame.

The widescreen slides are the panels on a wider canvas. The canvas grew but
the type did not, so a two line title that filled an 800px panel became a
small island in the middle of 1920px. Blowing everything up by one factor
does not work either: the dense slides already fill 1080px of height, and any
scale above 1 pushes them off the bottom.

So each slide is measured and given its own scale, the largest that still fits
the frame. Content is wrapped in a box the width of the original panel's text
column, which keeps every line break, measure and fixed width component exactly
as it was drawn, and that box is scaled about its centre.

    ./fit-wide.py            rewrites slides/wide/*.html in place
"""
import glob
import os
import re

os.chdir(os.path.dirname(os.path.abspath(__file__)))

CHROME = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome'

PANEL_W = 680          # 800px panel less its 60px side padding
FRAME_W, FRAME_H = 1920, 1080
MARGIN_X, MARGIN_Y = 120, 90

# A single line of type scaled to the width limit reads as a billboard rather
# than a slide, so the growth is capped short of it.
MAX_SCALE = 2.0

FIT_CSS = """
/* Auto-fit: see fit-wide.py. The box keeps the panel's text column width so
   nothing reflows, and scales about its centre so the slide's own centring
   still places it. Scale is written in per slide. */
.fit { display: flex; flex-direction: column; align-items: center;
       justify-content: center; width: %dpx; transform: scale(%s); }
</style>""" % (PANEL_W, '%s')


def wrap(html):
    """Put the slide's contents in the fit box, if they are not already."""
    if 'class="fit"' in html:
        return html
    html = re.sub(r'(<section class="slide[^"]*">)', r'\1\n<div class="fit">',
                  html, count=1)
    return html.replace('\n</section>', '\n</div>\n</section>', 1)


def set_scale(html, scale):
    html = re.sub(r'\n/\* Auto-fit:.*?</style>', '</style>', html, flags=re.S)
    return html.replace('</style>', FIT_CSS % round(scale, 4), 1)


files = sorted(glob.glob('slides/wide/*.html'))
if not files:
    raise SystemExit('no wide slides; run the generators first')

for p in files:
    # Read fully before opening for write: the write target is evaluated first,
    # so doing both in one expression truncates the file before it is read.
    src = open(p).read()
    open(p, 'w').write(set_scale(wrap(src), 1))

from playwright.sync_api import sync_playwright

with sync_playwright() as pw:
    b = pw.chromium.launch(executable_path=CHROME,
                           args=['--force-color-profile=srgb',
                                 '--font-render-hinting=none'])
    pg = b.new_page(viewport={'width': FRAME_W, 'height': FRAME_H})
    for p in files:
        pg.goto('file://%s/%s' % (os.getcwd(), p))
        pg.wait_for_timeout(120)
        # Unscaled height of the content, measured with the scale at 1.
        h = pg.evaluate("document.querySelector('.fit').getBoundingClientRect().height")
        scale = min(MAX_SCALE,
                    (FRAME_H - 2 * MARGIN_Y) / h,
                    (FRAME_W - 2 * MARGIN_X) / PANEL_W)
        src = open(p).read()
        open(p, 'w').write(set_scale(src, scale))
        print('%-46s h=%4d  scale=%.2f' % (os.path.basename(p), h, scale))
    b.close()

print('\n%d slides fitted' % len(files))
