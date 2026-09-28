#!/usr/bin/env python3
"""One icon on its own canvas: the call confirmation page.

Same browser window as the three funnel page icons, so this one sits with them
if it is ever put beside them. Inside is a calendar rather than a bare tick:
the thank you page already owns the bare tick, and what is confirmed here is a
time, not just a submission.

No name under it. It was asked for as an icon, so the canvas is cropped to the
icon and nothing else.

    ./build-call-confirmation-icon.py    writes the icon canvas
"""
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

W = 480
ICON = 440

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
@page { size: %(W)dpx %(W)dpx; margin: 0; }

.slide { width: %(W)dpx; height: %(W)dpx; padding: 0; background: var(--ground); }

.ic { display: flex; align-items: center; justify-content: center;
      width: 100%%; height: 100%%; }
.ic svg {
  display: block; width: %(ICON)dpx; height: %(ICON)dpx;
  fill: none; stroke: #7FA8DC; stroke-width: 2.4;
  stroke-linecap: round; stroke-linejoin: round;
}
.ic svg .dot { fill: #9DBCE0; stroke: none; }
.ic svg .hot { stroke: var(--blue); stroke-width: 4.2; }
</style>
</head>
<body>

<!-- no-autofit: its own canvas, not a panel. -->
<section class="slide">

  <div class="ic">
    <svg viewBox="0 0 124 124" aria-hidden="true">
      <rect x="10" y="18" width="104" height="88" rx="10"/>
      <path d="M10 41 H 114"/>
      <circle class="dot" cx="22" cy="29.5" r="2.8"/>
      <circle class="dot" cx="31" cy="29.5" r="2.8"/>
      <circle class="dot" cx="40" cy="29.5" r="2.8"/>

      <rect x="40" y="56" width="44" height="40" rx="5"/>
      <path d="M40 68 H 84"/>
      <path d="M51 49 V 59 M73 49 V 59"/>
      <path class="hot" d="M52 80 L60 88 L74 72"/>
    </svg>
  </div>

</section>

</body>
</html>
'''

path = 'slides/icon-call-confirmation.html'
open(path, 'w').write(TPL % dict(W=W, ICON=ICON))
print('wrote %s' % path)
