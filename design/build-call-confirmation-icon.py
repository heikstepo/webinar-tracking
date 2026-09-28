#!/usr/bin/env python3
"""One icon on its own canvas: the call confirmation page.

Same browser window as the three funnel page icons, so this one sits with them
if it is ever put beside them. Inside is a calendar rather than a bare tick:
the thank you page already owns the bare tick, and what is confirmed here is a
time, not just a submission.

Two canvases, both cropped to the icon rather than laid out as a slide: one
bare, one with the name under it. The named one is wider because the name is
longer than the icon, and it is left on one line on purpose.

    ./build-call-confirmation-icon.py    writes both canvases
"""
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

ART = '''<svg viewBox="0 0 124 124" aria-hidden="true">
      <rect x="10" y="18" width="104" height="88" rx="10"/>
      <path d="M10 41 H 114"/>
      <circle class="dot" cx="22" cy="29.5" r="2.8"/>
      <circle class="dot" cx="31" cy="29.5" r="2.8"/>
      <circle class="dot" cx="40" cy="29.5" r="2.8"/>

      <rect x="40" y="56" width="44" height="40" rx="5"/>
      <path d="M40 68 H 84"/>
      <path d="M51 49 V 59 M73 49 V 59"/>
      <path class="hot" d="M52 80 L60 88 L74 72"/>
    </svg>'''

TPL = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Call confirmation page</title>
<link rel="stylesheet" href="../4pi.css">
<link rel="stylesheet" href="../voice-quiet.css">
<style>
/* ============================================================================
   See build-call-confirmation-icon.py. The browser window is the same one the
   funnel page icons use; the calendar inside is what makes it this page.
   ========================================================================= */
@page { size: %(W)dpx %(H)dpx; margin: 0; }

.slide { width: %(W)dpx; height: %(H)dpx; padding: 0; background: var(--ground); }

.ic { display: flex; flex-direction: column; align-items: center;
      justify-content: center; width: 100%%; height: 100%%; }
.ic svg {
  display: block; width: %(ICON)dpx; height: %(ICON)dpx;
  fill: none; stroke: #7FA8DC; stroke-width: 2.4;
  stroke-linecap: round; stroke-linejoin: round;
}
.ic svg .dot { fill: #9DBCE0; stroke: none; }
.ic svg .hot { stroke: var(--blue); stroke-width: 4.2; }

.ic__name {
  margin: %(NGAP)dpx 0 0;
  font-size: %(NAME)dpx; font-weight: 600; letter-spacing: -0.008em;
  line-height: 1.2; color: var(--ink); text-align: center; white-space: nowrap;
}
</style>
</head>
<body>

<!-- no-autofit: its own canvas, not a panel. -->
<section class="slide">

  <div class="ic">
    %(ART)s
%(NAME_EL)s
  </div>

</section>

</body>
</html>
'''

VARIANTS = [
    dict(path='slides/icon-call-confirmation.html',
         W=480, H=480, ICON=440, NAME=0, NGAP=0, name_el=''),
    # The gap is negative because the drawing stops well short of the bottom of
    # its own viewBox, so a positive margin here would leave the name floating
    # a long way under a window that had already ended.
    dict(path='slides/icon-call-confirmation-named.html',
         W=820, H=680, ICON=440, NAME=46, NGAP=-34,
         name_el='    <p class="ic__name">Call Confirmation Page</p>'),
]

for v in VARIANTS:
    out = TPL % dict(W=v['W'], H=v['H'], ICON=v['ICON'], NAME=v['NAME'],
                     NGAP=v['NGAP'], ART=ART, NAME_EL=v['name_el'])
    open(v['path'], 'w').write(out)
    print('wrote %s' % v['path'])
