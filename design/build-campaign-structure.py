#!/usr/bin/env python3
"""The campaign structure, with one ad opened up.

Circles for the ads, as in the rough. The three creatives could not go inside a
circle without crowding its edge, so instead one ad is pulled out and blown up:
the same circle, larger, with its three creatives in it. That keeps the ad a
circle everywhere it appears and still shows what one contains.

The two leader lines are the external tangents of the small circle and the big
one, computed rather than eyeballed. Lines drawn to the big circle's centre
would read as spokes; tangents read as a magnifier.

    ./build-campaign-structure.py    writes the 16:9 slide
"""
import math
import os
import re

os.chdir(os.path.dirname(os.path.abspath(__file__)))

STAGE_W, STAGE_H = 1700, 760

# The card, measured from its own padding so the anchor circle can be found.
# The card is centred on the stage: it is the subject, and the blown up ad
# is an annotation in the margin beside it.
CARD_X, CARD_Y = 453, 34
PAD, IPAD = 48, 38
HEAD, IHEAD = 80, 74          # label plus its margin, outer then inner
DISC, CGAP, RGAP = 130, 34, 30

GRID_X = CARD_X + PAD + IPAD
GRID_Y = CARD_Y + PAD + HEAD + IPAD + IHEAD

# Row 1, column 4: the rightmost filled ad, so the lines leave on the open side.
ANCHOR = (GRID_X + 3 * (DISC + CGAP) + DISC / 2, GRID_Y + DISC / 2, DISC / 2)
# Small on purpose. At anything like the grid's size it stopped being a
# detail of the campaign and started competing with it.
ZOOM = (1500, ANCHOR[1], 95)


def tangents(c1, c2):
    """The two external tangents, as (x1, y1, x2, y2) pairs.

    Both centres sit on one horizontal line here, so the geometry reduces to a
    single angle: the tangent leaves each circle at 90 degrees plus that angle
    from the line joining them.
    """
    (x1, y1, r1), (x2, y2, r2) = c1, c2
    d = math.hypot(x2 - x1, y2 - y1)
    a = math.asin((r2 - r1) / d)
    out = []
    for side in (1, -1):
        th = math.pi / 2 + a
        dx, dy = math.cos(th), math.sin(th) * side
        out.append((x1 + r1 * dx, y1 - r1 * dy, x2 + r2 * dx, y2 - r2 * dy))
    return out


TPL = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Campaign structure</title>
<link rel="stylesheet" href="../../4pi.css">
<link rel="stylesheet" href="../../voice-quiet.css">
<style>
/* ============================================================================
   See build-campaign-structure.py. Nested boxes for the structure, and one ad
   pulled out and blown up for what an ad holds.
   ========================================================================= */
@page { size: 1920px 1080px; margin: 0; }

.slide { width: 1920px; height: 1080px; padding: 90px 110px; background: var(--ground); }

.cst { position: relative; width: __SW__px; height: __SH__px; margin: 0 auto; }

/* Above the card, so each line visibly leaves the ringed circle. Drawn under
   it, they appeared at the card's edge and pointed at nothing in particular. */
.cst__link { position: absolute; inset: 0; z-index: 2; pointer-events: none; }
.cst__link svg {
  display: block; width: 100%; height: 100%;
  fill: none; stroke: #C6CED8; stroke-width: 2.2; stroke-linecap: round;
}

/* ---- the campaign -------------------------------------------------------- */
.cst__card {
  position: absolute; left: __CX__px; top: __CY__px;
  background: var(--surface); border: 1px solid var(--hairline);
  border-radius: 32px; padding: __PAD__px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04);
}
.cst__name {
  margin: 0 0 26px; text-align: center;
  font-size: 44px; font-weight: 600; letter-spacing: -0.014em; color: var(--ink-2);
}

/* ---- the ad set ---------------------------------------------------------- */
.cst__set { background: #E4EFFD; border-radius: 26px; padding: __IPAD__px; }
.cst__sname {
  margin: 0 0 26px; text-align: center;
  font-size: 40px; font-weight: 600; letter-spacing: -0.012em; color: #1E4E8C;
}

/* ---- the ads ------------------------------------------------------------- */
.cst__row {
  display: grid; grid-template-columns: repeat(4, __DISC__px);
  column-gap: __CGAP__px; row-gap: __RGAP__px;
}
.cst__ad {
  width: __DISC__px; height: __DISC__px; border-radius: 50%;
  background: var(--surface);
}
/* The headroom in "5 to 8": outlined, and holding nothing. */
.cst__ad--open { background: none; border: 2px dashed #BFD6F7; box-sizing: border-box; }
/* The one that is opened up on the right. */
.cst__ad--pick { box-shadow: 0 0 0 2px #4A97EF; }

.cst__count {
  margin: 28px 0 0; text-align: center;
  font-size: 40px; font-weight: 600; letter-spacing: -0.012em; color: #1E4E8C;
}

/* ---- that one ad, enlarged ----------------------------------------------- */
.cst__zoom {
  position: absolute; left: __ZX__px; top: __ZY__px;
  width: __ZD__px; height: __ZD__px; border-radius: 50%;
  background: var(--surface); border: 2px solid #4A97EF;
  display: flex; align-items: center; justify-content: center; gap: 10px;
}
.cst__cr { width: 46px; height: 92px; border-radius: 8px; background: #4A97EF; }

/* Wider than the circle it sits under, so the line does not break. */
.cst__per {
  position: absolute; left: __LX__px; top: __PY__px; width: __LW__px;
  margin: 0; text-align: center; white-space: nowrap;
  font-size: 30px; font-weight: 600; letter-spacing: -0.008em; color: var(--ink-2);
}
</style>
</head>
<body>

<!-- no-autofit: its own canvas, not a panel. -->
<section class="slide slide--center slide--mid">

  <div class="cst">

    <div class="cst__link">
      <svg viewBox="0 0 __SW__ __SH__" aria-hidden="true">
__LINES__
      </svg>
    </div>

    <div class="cst__card">
      <p class="cst__name">1 CBO Campaign</p>

      <div class="cst__set">
        <p class="cst__sname">1 Control Ad Set</p>

        <div class="cst__row">
          <span class="cst__ad"></span>
          <span class="cst__ad"></span>
          <span class="cst__ad"></span>
          <span class="cst__ad cst__ad--pick"></span>
          <span class="cst__ad"></span>
          <span class="cst__ad cst__ad--open"></span>
          <span class="cst__ad cst__ad--open"></span>
          <span class="cst__ad cst__ad--open"></span>
        </div>

        <p class="cst__count">5&ndash;8 Unique Ads</p>
      </div>
    </div>

    <div class="cst__zoom">
      <span class="cst__cr"></span><span class="cst__cr"></span><span class="cst__cr"></span>
    </div>
    <p class="cst__per">3 Creatives per Ad</p>

  </div>

</section>

</body>
</html>
'''


def _check_class_collisions():
    """4pi.css already owns .ad and .ads, which is why everything here is cst__."""
    css = open('4pi.css').read() + open('voice-quiet.css').read()
    taken = set(re.findall(r'\.([a-zA-Z][\w-]*)', css))
    mine = set(re.findall(r'^\.([a-zA-Z][\w-]*)', TPL, re.M)) - {'slide'}
    clash = sorted(mine & taken)
    if clash:
        raise SystemExit('class names already used by the shared stylesheets: '
                         + ', '.join(clash))


_check_class_collisions()

lines = '\n'.join('        <path d="M%.1f %.1f L %.1f %.1f"/>' % t
                  for t in tangents(ANCHOR, ZOOM))

out = TPL
for k, v in (('SW', STAGE_W), ('SH', STAGE_H), ('CX', CARD_X), ('CY', CARD_Y),
             ('PAD', PAD), ('IPAD', IPAD), ('DISC', DISC),
             ('CGAP', CGAP), ('RGAP', RGAP),
             ('ZX', int(ZOOM[0] - ZOOM[2])), ('ZY', int(ZOOM[1] - ZOOM[2])),
             ('ZD', int(ZOOM[2] * 2)), ('PY', int(ZOOM[1] + ZOOM[2] + 26)),
             ('LX', int(ZOOM[0] - 170)), ('LW', 340)):
    out = out.replace('__%s__' % k, str(v))
out = out.replace('__LINES__', lines)

path = 'slides/wide/wide-campaign-structure.html'
open(path, 'w').write(out)
print('wrote %s (anchor at %.0f,%.0f)' % (path, ANCHOR[0], ANCHOR[1]))
