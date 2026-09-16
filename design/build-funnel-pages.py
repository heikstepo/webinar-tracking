#!/usr/bin/env python3
"""The three funnel pages, as icons with their names.

Each is a browser window, because all three are pages and a bare symbol would
not say so. What is inside the window is what tells them apart: a form and a
button for the opt in, a star and a button for the upsell, a tick for the thank
you. One accent mark each, same as the rest of the icon set here.

No arrows between them. They were not asked for as a flow, and leaving them out
means each icon also stands on its own if one is needed by itself.

    ./build-funnel-pages.py     writes the 16:9 slide and the vertical card
"""
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Browser chrome, shared: the frame, the bar under it, and the three dots.
CHROME = '''<rect x="10" y="18" width="104" height="88" rx="10"/>
        <path d="M10 41 H 114"/>
        <circle class="dot" cx="22" cy="29.5" r="2.8"/>
        <circle class="dot" cx="31" cy="29.5" r="2.8"/>
        <circle class="dot" cx="40" cy="29.5" r="2.8"/>'''

PAGES = [
    # A headline, a field to type in, and the button that does the opting in.
    ('optin', 'Webinar opt in page', '''<path d="M30 56 H 94"/>
        <rect x="30" y="66" width="64" height="15" rx="4"/>
        <rect class="hot-fill" x="30" y="88" width="64" height="13" rx="4"/>'''),
    # A star for the premium thing being offered, over its button.
    ('vip', 'VIP upsell page', '''<path class="hot-fill" d="M62 48 L65.5 57.1 L75.3 57.7
          L67.7 63.9 L70.2 73.3 L62 68 L53.8 73.3 L56.3 63.9 L48.7 57.7 L58.5 57.1 Z"/>
        <rect class="hot-fill" x="30" y="86" width="64" height="13" rx="4"/>'''),
    # Nothing to do here but confirm, so the tick is the whole page.
    ('thanks', 'Thank you page', '''<path class="hot" d="M45 71 L57 83 L81 55"/>'''),
]

TPL = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>The three funnel pages</title>
<link rel="stylesheet" href="__CSS__4pi.css">
<link rel="stylesheet" href="__CSS__voice-quiet.css">
<style>
/* ============================================================================
   See build-funnel-pages.py. Each icon is a browser window because all three
   are pages; what sits inside the window is what tells them apart.
   ========================================================================= */
@page { size: __W__px __H__px; margin: 0; }

.slide { width: __W__px; height: __H__px; padding: __PY__px __PX__px; background: var(--ground); }

.pgs { display: flex; __DIR__ justify-content: center; gap: __GAP__px; }

.pg { display: flex; __PGDIR__ align-items: center; __PGW__ }

.pg svg {
  display: block; width: __ICON__px; height: __ICON__px; flex: none;
  fill: none; stroke: #7FA8DC; stroke-width: 2.4;
  stroke-linecap: round; stroke-linejoin: round;
}
.pg svg .dot { fill: #9DBCE0; stroke: none; }
.pg svg .hot { stroke: var(--blue); stroke-width: 4.2; }
.pg svg .hot-fill { fill: var(--blue); stroke: none; }

.pg__name {
  margin: __NM__;
  font-size: __NAME__px; font-weight: 600; letter-spacing: -0.008em;
  line-height: 1.24; color: var(--ink); __NALIGN__
}
</style>
</head>
<body>

<!-- no-autofit: its own canvas, not a panel. -->
<section class="slide slide--center slide--mid">

  <div class="pgs">
__PAGES__
  </div>

</section>

</body>
</html>
'''

PAGE = '''    <div class="pg">
      <svg viewBox="0 0 124 124" aria-hidden="true">
        %s
        %s
      </svg>
      <p class="pg__name">%s</p>
    </div>'''

VARIANTS = [
    # 16:9 — three across, name under each.
    dict(path='slides/wide/wide-funnel-pages.html', css='../../',
         W=1920, H=1080, PX=110, PY=90, GAP=130, ICON=250, NAME=44,
         dir='align-items: flex-start;', pgdir='flex-direction: column;',
         pgw='width: 420px;', nm='38px 0 0', nalign='text-align: center;'),
    # vertical — three down, name beside each, because three long names side by
    # side at 1080 wide would each wrap to three lines.
    dict(path='slides/vert-funnel-pages.html', css='../',
         W=1080, H=1200, PX=80, PY=80, GAP=90, ICON=210, NAME=52,
         dir='flex-direction: column; align-items: flex-start;', pgdir='',
         pgw='gap: 48px;', nm='0', nalign='text-align: left;'),
]

pages = '\n\n'.join(PAGE % (CHROME, art, name) for _, name, art in PAGES)

for v in VARIANTS:
    out = TPL
    for k in ('W', 'H', 'PX', 'PY', 'GAP', 'ICON', 'NAME'):
        out = out.replace('__%s__' % k, str(v[k]))
    for k in ('CSS', 'DIR', 'PGDIR', 'PGW', 'NM', 'NALIGN'):
        out = out.replace('__%s__' % k, v[k.lower()])
    out = out.replace('__PAGES__', pages)
    os.makedirs(os.path.dirname(v['path']), exist_ok=True)
    open(v['path'], 'w').write(out)
    print('wrote %s' % v['path'])
