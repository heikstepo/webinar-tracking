#!/usr/bin/env python3
"""The angle matrix: one ICP in the middle, every reason they buy around it.

One person, one offer, many reasons to say yes. Each reason is an angle, and
each angle is its own ad group, which is why every node carries its own little
tray of ads rather than a label saying so.

The angles are the ecom example: the steps the programme covers (pick the
product, suppliers, branding, the store, influencers, paid ads), the stall
that brings people in off the awareness levels, and the straight offer.

    ./build-angle-matrix.py    writes the 16:9 slide
"""
import math
import os
import re

os.chdir(os.path.dirname(os.path.abspath(__file__)))

W, H = 1920, 1080
CX, CY = 960, 566              # the hub, a little below the title
RX, RY = 626, 306              # the ring the angles sit on

HUB_W, HUB_H = 376, 168
NODE_W, NODE_H = 332, 140

# (angle, the reason in their words)
ANGLES = [
    ('Product Selection', '&ldquo;I don&rsquo;t know what to sell&rdquo;'),
    ('Suppliers', '&ldquo;Where do I source it?&rdquo;'),
    ('Branding', '&ldquo;Mine looks like everyone else&rsquo;s&rdquo;'),
    ('The Store', '&ldquo;Traffic comes, nobody buys&rdquo;'),
    ('Influencers', '&ldquo;How do I get it seen?&rdquo;'),
    ('Paid Ads', '&ldquo;Ads just burn money&rdquo;'),
    ('Plateaued', '&ldquo;Sales stopped growing&rdquo;'),
    ('Straight Offer', '&ldquo;Just show me the program&rdquo;'),
]

TPL = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Angle Matrix</title>
<link rel="stylesheet" href="../../4pi.css">
<link rel="stylesheet" href="../../voice-quiet.css">
<style>
/* ============================================================================
   See build-angle-matrix.py. One ICP in the middle, the reasons they buy on a
   ring around it, a spoke to each. Every angle carries three ads, because an
   angle is an ad group, not a line in a list.

   Class names are prefixed am; neither shared sheet uses them.
   ========================================================================= */
@page { size: __W__px __H__px; margin: 0; }

.slide { position: relative; width: __W__px; height: __H__px; padding: 0;
         background: var(--ground); }

.am__h {
  position: absolute; left: 110px; top: 44px; margin: 0;
  font-size: 54px; font-weight: 600; letter-spacing: -0.022em; color: var(--ink);
}
.am__sub {
  position: absolute; left: 112px; top: 112px; margin: 0;
  font-size: 24px; font-weight: 600; letter-spacing: -0.01em; color: var(--ink-3);
}

/* the spokes, under everything so they run into the cards */
.am__sp { position: absolute; inset: 0; }
.am__sp svg { display: block; width: 100%; height: 100%; }
.am__sp .rail { fill: none; stroke: #D2D8E0; stroke-width: 3;
                stroke-linecap: round; }
.am__sp .tip { fill: #BAC3CF; }

/* ---- the hub ------------------------------------------------------------- */
.am__hub {
  position: absolute; box-sizing: border-box;
  width: __HUBW__px; height: __HUBH__px;
  left: 50%; margin-left: -__HUBHW__px;
  border-radius: 24px; background: #E4EFFD; border: 2px solid #BFD6F7;
  display: flex; flex-direction: column; align-items: center;
  justify-content: center; text-align: center; padding: 0 28px;
}
.am__hub p { margin: 0; }
.am__lab {
  font-size: 19px; font-weight: 700; letter-spacing: 0.06em;
  text-transform: uppercase; color: #5C8ECB;
}
.am__who {
  margin-top: 10px !important;
  font-size: 27px; font-weight: 600; letter-spacing: -0.014em; line-height: 1.26;
  color: #1E4E8C;
}

/* ---- an angle ------------------------------------------------------------ */
.am__node {
  position: absolute; box-sizing: border-box;
  width: __NODEW__px; height: __NODEH__px;
  background: var(--surface); border: 1px solid var(--hairline);
  border-radius: 18px; padding: 15px 19px;
  box-shadow: 0 3px 14px rgba(20, 30, 50, 0.07);
}
.am__t {
  margin: 0;
  font-size: 25px; font-weight: 600; letter-spacing: -0.014em; color: var(--ink);
}
.am__say {
  margin: 6px 0 0;
  font-size: 18px; font-weight: 600; letter-spacing: -0.006em; color: var(--ink-2);
}
/* the ad group: three ads, which is what the angle turns into */
.am__ads { display: flex; gap: 7px; margin-top: 12px; }
.am__ad { width: 34px; height: 22px; border-radius: 6px; background: #CFE2FA; }
.am__ad--on { background: var(--blue); }

.am__key {
  position: absolute; right: 110px; bottom: 54px; margin: 0; text-align: right;
  font-size: 22px; font-weight: 600; letter-spacing: -0.008em; color: var(--ink-3);
}
.am__key b { font-weight: 600; color: var(--blue); }
</style>
</head>
<body>

<!-- no-autofit: its own canvas, not a panel. -->
<section class="slide">

  <h1 class="am__h">Angle Matrix</h1>
  <p class="am__sub">One ICP, every reason they buy</p>

  <div class="am__sp">
    <svg viewBox="0 0 __W__ __H__" aria-hidden="true">
__SPOKES__
    </svg>
  </div>

  <div class="am__hub" style="top:__HUBY__px">
    <p class="am__lab">ICP</p>
    <p class="am__who">Sold on ecom,<br>wants a product brand</p>
  </div>

__NODES__

  <p class="am__key">1 angle = <b>1 ad group</b></p>

</section>

</body>
</html>
'''


def _check_class_collisions():
    css = open('4pi.css').read() + open('voice-quiet.css').read()
    taken = set(re.findall(r'\.([a-zA-Z][\w-]*)', css))
    mine = set(re.findall(r'^\.([a-zA-Z][\w-]*)', TPL, re.M)) - {'slide'}
    clash = sorted(mine & taken)
    if clash:
        raise SystemExit('class names already used by the shared stylesheets: '
                         + ', '.join(clash))


_check_class_collisions()


def edge(w, h, dx, dy, pad=0):
    """Where a ray leaving a box's centre crosses its edge."""
    hw, hh = w / 2 + pad, h / 2 + pad
    tx = hw / abs(dx) if dx else float('inf')
    ty = hh / abs(dy) if dy else float('inf')
    t = min(tx, ty)
    return dx * t, dy * t


spokes, nodes = [], []

for i, (title, say) in enumerate(ANGLES):
    a = math.radians(-90 + i * (360 / len(ANGLES)))
    nx, ny = CX + RX * math.cos(a), CY + RY * math.sin(a)

    # the spoke runs between the two boxes, not between their centres
    dx, dy = nx - CX, ny - CY
    d = math.hypot(dx, dy)
    ux, uy = dx / d, dy / d
    sx, sy = edge(HUB_W, HUB_H, ux, uy, 12)
    ex, ey = edge(NODE_W, NODE_H, -ux, -uy, 14)
    x1, y1 = CX + sx, CY + sy
    x2, y2 = nx + ex, ny + ey
    spokes.append('<path class="rail" d="M%g %g L %g %g"/>' % (x1, y1, x2, y2))
    spokes.append('<g transform="translate(%g %g) rotate(%g)">'
                  '<path class="tip" d="M0 0 L -17 -7 L -17 7 Z"/></g>'
                  % (x2, y2, math.degrees(math.atan2(y2 - y1, x2 - x1))))

    nodes.append(
        '  <div class="am__node" style="left:%gpx; top:%gpx">'
        '<p class="am__t">%s</p><p class="am__say">%s</p>'
        '<div class="am__ads"><span class="am__ad am__ad--on"></span>'
        '<span class="am__ad"></span><span class="am__ad"></span></div></div>'
        % (nx - NODE_W / 2, ny - NODE_H / 2, title, say))

out = (TPL.replace('__W__', str(W)).replace('__H__', str(H))
          .replace('__HUBW__', str(HUB_W)).replace('__HUBH__', str(HUB_H))
          .replace('__HUBHW__', str(HUB_W // 2))
          .replace('__HUBY__', str(CY - HUB_H // 2))
          .replace('__NODEW__', str(NODE_W)).replace('__NODEH__', str(NODE_H))
          .replace('__SPOKES__', '\n'.join('      ' + s for s in spokes))
          .replace('__NODES__', '\n'.join(nodes)))

path = 'slides/wide/wide-angle-matrix.html'
open(path, 'w').write(out)
print('wrote %s' % path)
