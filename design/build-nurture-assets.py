#!/usr/bin/env python3
"""The six nurture assets, as icons with their names.

Drawn icons for the four things that are activities, and the real marks for the
two that are products: YouTube and Telegram come from design/logos and are set
filled in one ink, matching how the ICP sources slide handles them. Mixing a
brand colour in here would put two loud colours against a set otherwise built
from one blue.

Lead magnet is deliberately absent and setters is in its place, as asked.

    ./build-nurture-assets.py    writes the 16:9 slide and the vertical card
"""
import os
import re

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def logo(slug):
    """A brand mark as a single colour <svg> body, fills stripped so it takes
    the colour set on the tile rather than keeping its own."""
    src = open('logos/%s.svg' % slug).read()
    box = re.search(r'viewBox="([^"]+)"', src).group(1)
    body = src[src.index('>', src.index('<svg')) + 1:src.rindex('</svg>')]
    return (box, re.sub(r'\s*fill="[^"]*"', '', body).strip())


DRAWN = '0 0 124 124'

ITEMS = [
    # Three envelopes would crowd; two says "sequence" just as well.
    ('Pre-Webinar Email Sequence', DRAWN, '''<rect x="30" y="24" width="64" height="42" rx="6"/>
        <rect x="16" y="44" width="80" height="56" rx="7"/>
        <path class="hot" d="M22 51 L56 77 L90 51"/>'''),
    # The ad, and a U-turn under it. An arc alone read as a smile rather than
    # as coming back, so the path now visibly goes out, turns, and returns.
    ('Retargeting Ads', DRAWN, '''<rect x="20" y="10" width="84" height="50" rx="8"/>
        <rect x="30" y="20" width="64" height="20" rx="4"/>
        <rect class="hot-fill" x="30" y="46" width="32" height="6" rx="3"/>
        <path class="hot" d="M64 74 H 76 C 92 74, 92 102, 76 102 H 40"/>
        <path class="hot" d="M49 94 L39 102 L49 110"/>'''),
    ('YouTube Nurturing',) + logo('youtube'),
    # A message, and the signal going out to a lot of people at once.
    ('SMS Blasts', DRAWN, '''<rect x="8" y="26" width="88" height="52" rx="12"/>
        <path d="M34 78 L34 96 L54 78"/>
        <circle class="hot-fill" cx="36" cy="52" r="5"/>
        <circle class="hot-fill" cx="52" cy="52" r="5"/>
        <circle class="hot-fill" cx="68" cy="52" r="5"/>
        <path d="M104 40 H 114 M104 52 H 118 M104 64 H 114"/>'''),
    ('Telegram',) + logo('telegram'),
    # A person on calls: the headset is the accent, because that is the job.
    ('Setters', DRAWN, '''<path d="M24 102 C 24 82, 41 72, 62 72 C 83 72, 100 82, 100 102"/>
        <circle cx="62" cy="46" r="17"/>
        <path class="hot" d="M42 46 a 20 20 0 0 1 40 0"/>
        <rect class="hot-fill" x="38" y="44" width="9" height="18" rx="4.5"/>
        <rect class="hot-fill" x="77" y="44" width="9" height="18" rx="4.5"/>
        <path class="hot" d="M42 62 C 42 73, 52 77, 58 77"/>'''),
]

TPL = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Nurture assets</title>
<link rel="stylesheet" href="__CSS__4pi.css">
<link rel="stylesheet" href="__CSS__voice-quiet.css">
<style>
/* ============================================================================
   See build-nurture-assets.py. Four drawn icons and two real brand marks, all
   in one ink so the set reads as one family.
   ========================================================================= */
@page { size: __W__px __H__px; margin: 0; }

.slide { width: __W__px; height: __H__px; padding: __PY__px __PX__px; background: var(--ground); }

.grid {
  display: grid;
  grid-template-columns: repeat(__COLS__, __CELL__px);
  column-gap: __CGAP__px; row-gap: __RGAP__px;
  justify-content: center;
}

.cell { display: flex; flex-direction: column; align-items: center; }

/* Fixed height, so a wide mark and a tall one still leave their captions on
   one line as each other. */
.cell__art { height: __ICON__px; display: flex; align-items: center; justify-content: center; }
.cell__art svg {
  display: block; width: __ICON__px; height: __ICON__px;
  fill: none; stroke: #7FA8DC; stroke-width: 2.6;
  stroke-linecap: round; stroke-linejoin: round;
}
.cell__art svg .hot { stroke: var(--blue); stroke-width: 3.6; }
.cell__art svg .hot-fill { fill: var(--blue); stroke: none; }
/* Real logos are filled marks, not line drawings. */
.cell__art .brand { width: __BRAND__px; height: __BRAND__px; fill: var(--ink); stroke: none; }

.cell__name {
  margin: __NGAP__px 0 0;
  font-size: __NAME__px; font-weight: 600; letter-spacing: -0.006em;
  line-height: 1.22; color: var(--ink); text-align: center;
}
</style>
</head>
<body>

<!-- no-autofit: its own canvas, not a panel. -->
<section class="slide slide--center slide--mid">

  <div class="grid">
__CELLS__
  </div>

</section>

</body>
</html>
'''

CELL = '''    <div class="cell">
      <div class="cell__art">
        <svg class="%s" viewBox="%s" aria-hidden="true">%s</svg>
      </div>
      <p class="cell__name">%s</p>
    </div>'''

VARIANTS = [
    dict(path='slides/wide/wide-nurture-assets.html', css='../../',
         W=1920, H=1080, PX=110, PY=90, COLS=3, CELL=430,
         CGAP=90, RGAP=80, ICON=180, BRAND=170, NAME=40, NGAP=30),
    dict(path='slides/vert-nurture-assets.html', css='../',
         W=1080, H=1200, PX=70, PY=70, COLS=2, CELL=420,
         CGAP=60, RGAP=62, ICON=150, BRAND=142, NAME=36, NGAP=24),
]

cells = '\n\n'.join(
    CELL % ('brand' if box != DRAWN else '', box, art, name)
    for name, box, art in ITEMS)

for v in VARIANTS:
    out = TPL
    for k in ('W', 'H', 'PX', 'PY', 'COLS', 'CELL', 'CGAP', 'RGAP',
              'ICON', 'BRAND', 'NAME', 'NGAP'):
        out = out.replace('__%s__' % k, str(v[k]))
    out = out.replace('__CSS__', v['css']).replace('__CELLS__', cells)
    os.makedirs(os.path.dirname(v['path']), exist_ok=True)
    open(v['path'], 'w').write(out)
    print('wrote %s' % v['path'])
