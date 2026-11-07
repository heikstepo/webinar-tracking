#!/usr/bin/env python3
"""A thumbnail panel about messaging and ICP journeys.

960x1080, the right half of a 16:9 frame, so it drops in beside a talking head
without being cropped. Same board language as the other panel: dotted paper,
cards pinned at slight angles, dashed connectors, one red ring.

Every card is a piece the deck already has: one ICP with many angles, the
objection and the proof that answers it, the awareness levels, pain against
dream, the Hook / Body / CTA skeleton, and two ICPs walking different paths
through the same funnel.

    ./build-thumb-messaging.py    writes the panel
"""
import os
import re

os.chdir(os.path.dirname(os.path.abspath(__file__)))

W, H = 960, 1080
BW, BH = 880, 800              # the board inside it

G = {
    'flame': '''<path d="M70 10 C 70 36, 52 42, 50 60 C 47 47, 43 42, 38 38
        C 35 50, 26 58, 26 76 a 36 36 0 0 0 72 0 C 98 54, 86 40, 70 10 Z"/>''',
    'fly': '''<path d="M62 42 V 94"/>
        <path d="M62 50 C 40 22, 12 28, 14 54 C 16 78, 44 82, 62 68"/>
        <path d="M62 50 C 84 22, 112 28, 110 54 C 108 78, 80 82, 62 68"/>
        <path d="M58 40 L 46 22 M66 40 L 78 22"/>''',
}

TPL = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Messaging and ICP Journeys</title>
<link rel="stylesheet" href="../../4pi.css">
<link rel="stylesheet" href="../../voice-quiet.css">
<style>
/* ============================================================================
   See build-thumb-messaging.py. The right half of a 16:9 thumbnail: a headline
   that has to survive being shrunk, over a board that only has to look like a
   lot of ground covered.

   Class names are prefixed mb; neither shared sheet uses them.
   ========================================================================= */
@page { size: __W__px __H__px; margin: 0; }

.slide {
  position: relative;
  width: __W__px; height: __H__px; padding: 0; background: var(--ground);
  background-image: radial-gradient(#D7DBE2 1.7px, transparent 1.8px);
  background-size: 30px 30px; background-position: 10px 10px;
}

/* ---- the headline -------------------------------------------------------- */
.mb__h {
  position: absolute; left: 40px; top: 42px; width: 884px; margin: 0;
  font-size: 76px; font-weight: 700; letter-spacing: -0.038em; line-height: 1.04;
  color: var(--ink);
}
.mb__h i { font-style: normal; color: var(--blue); }

/* ---- the board ----------------------------------------------------------- */
.mb { position: absolute; left: 40px; top: 236px; width: __BW__px; height: __BH__px; }

.mb__wires { position: absolute; inset: 0; }
.mb__wires svg { display: block; width: 100%; height: 100%; }
.mb__wires .flow { fill: none; stroke: #AEB8C6; stroke-width: 3;
                   stroke-linecap: round; stroke-dasharray: 9 9; }
.mb__wires .tip { fill: #AEB8C6; }
.mb__ink { z-index: 3; pointer-events: none; }
.mb__ink .ring { fill: none; stroke: var(--red); stroke-width: 3.4; }

.mb__card {
  position: absolute; box-sizing: border-box;
  background: var(--surface); border: 1px solid var(--hairline);
  border-radius: 20px; padding: 17px 20px;
  box-shadow: 0 2px 10px rgba(20, 30, 50, 0.07);
}
.mb__t {
  margin: 0 0 14px;
  font-size: 27px; font-weight: 600; letter-spacing: -0.014em; color: var(--ink);
}
.mb__t i { font-style: normal; color: var(--blue); }

.mb__row { display: flex; align-items: center; gap: 10px; }
.mb__chip {
  padding: 7px 13px; border-radius: 9px;
  background: #E4EFFD; color: #1E4E8C;
  font-size: 19px; font-weight: 600; white-space: nowrap;
}
.mb__chip--p { background: #FBE4E8; color: #AE3047; }
.mb__chip--g { background: #E7F5E3; color: #3C7F2C; }
.mb__arr { width: 18px; height: 2px; background: #B6C2D0; flex: none; }

.mb__g { display: block; fill: none; stroke: #7FA8DC; stroke-width: 3.6;
         stroke-linecap: round; stroke-linejoin: round; }
.mb__g--p { stroke: #D4536B; }
.mb__g--g { stroke: #52A33C; }

/* the angle hub */
.mb__hub svg { display: block; width: 100%; height: 148px; }
.mb__hub .spoke { fill: none; stroke: #C6CED8; stroke-width: 2.6; }
.mb__hub .node { fill: #CFE2FA; }
.mb__hub .core { fill: #E4EFFD; stroke: #8FBDF3; stroke-width: 3; }
.mb__hub text { font-family: inherit; font-size: 21px; font-weight: 700;
                fill: #1E4E8C; text-anchor: middle; }

/* the levels */
.mb__lvl { display: flex; align-items: center; gap: 12px; }
.mb__lvl + .mb__lvl { margin-top: 9px; }
.mb__bar { height: 16px; border-radius: 5px; flex: none; }
.mb__lab { font-size: 18px; font-weight: 600; color: var(--ink-2); white-space: nowrap; }

/* pain and dream */
.mb__half { flex: 1; border-radius: 14px; padding: 10px 0; text-align: center; }
.mb__half--p { background: #FBE4E8; }
.mb__half--g { background: #E7F5E3; }
.mb__half p { margin: 4px 0 0; font-size: 19px; font-weight: 600; }
.mb__half--p p { color: #AE3047; }
.mb__half--g p { color: #3C7F2C; }
.mb__half svg { margin: 0 auto; width: 50px; height: 50px; }

/* the journeys */
.mb__lane { display: flex; align-items: center; gap: 8px; }
.mb__lane + .mb__lane { margin-top: 20px; }
.mb__who {
  width: 68px; flex: none;
  font-size: 18px; font-weight: 700; letter-spacing: 0.04em; color: var(--ink-3);
}
.mb__stop {
  flex: 1; box-sizing: border-box; padding: 9px 0; text-align: center;
  border-radius: 10px; background: #EDF3FB; color: #44536A;
  font-size: 17px; font-weight: 600;
}
.mb__stop--on { background: var(--blue); color: #fff; }
</style>
</head>
<body>

<section class="slide">

  <h1 class="mb__h">Messaging <i>+</i><br>ICP Journeys</h1>

  <div class="mb">

    <div class="mb__wires">
      <svg viewBox="0 0 __BW__ __BH__" aria-hidden="true">
__WIRES__
      </svg>
    </div>

    <div class="mb__wires mb__ink">
      <svg viewBox="0 0 __BW__ __BH__" aria-hidden="true">
__INK__
      </svg>
    </div>

__CARDS__

  </div>

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

cards = []


def card(x, y, w, h, rot, title, body):
    cards.append('    <div class="mb__card" style="left:%gpx; top:%gpx; width:%gpx; '
                 'height:%gpx; transform:rotate(%gdeg)">'
                 '<p class="mb__t">%s</p>%s</div>' % (x, y, w, h, rot, title, body))


def tip(x, y, a=0):
    return ('<g transform="translate(%g %g) rotate(%g)">'
            '<path class="tip" d="M0 0 L -18 -7 L -18 7 Z"/></g>' % (x, y, a))


def wire(x1, y1, x2, y2, a=0):
    dx, dy = (x2 - x1) * 0.45, (y2 - y1) * 0.45
    if abs(x2 - x1) >= abs(y2 - y1):
        c1, c2 = (x1 + dx, y1), (x2 - dx, y2)
    else:
        c1, c2 = (x1, y1 + dy), (x2, y2 - dy)
    return ('<path class="flow" d="M%g %g C %g %g, %g %g, %g %g"/>'
            % (x1, y1, c1[0], c1[1], c2[0], c2[1], x2, y2)) + tip(x2, y2, a)


def glyph(name, cls):
    return ('<svg class="mb__g %s" viewBox="0 0 124 124" aria-hidden="true">%s</svg>'
            % (cls, G[name]))


BLUES = ['#C5DDFA', '#A7CCF7', '#7CB2F3', '#4A97EF', '#0071E3']

# ---- one ICP, many angles --------------------------------------------------
import math

hub = ['<circle class="core" cx="190" cy="74" r="40"/>', '<text x="190" y="82">ICP</text>']
for i in range(7):
    a = math.radians(-90 + i * (360 / 7))
    nx, ny = 190 + 150 * math.cos(a), 74 + 58 * math.sin(a)
    hub.insert(0, '<line class="spoke" x1="190" y1="74" x2="%g" y2="%g"/>' % (nx, ny))
    hub.append('<circle class="node" cx="%g" cy="%g" r="15"/>' % (nx, ny))
ANGLES = ('<div class="mb__hub"><svg viewBox="0 0 380 148" aria-hidden="true">%s</svg>'
          '</div>' % ''.join(hub))

# ---- objection and proof ---------------------------------------------------
OBJ = ''.join(
    '<div class="mb__row" style="margin-top:%dpx">'
    '<span class="mb__chip mb__chip--p">%s</span>'
    '<div class="mb__arr"></div>'
    '<span class="mb__chip mb__chip--g">%s</span></div>'
    % (0 if i == 0 else 12, o, p)
    for i, (o, p) in enumerate(((' &ldquo;Saturated&rdquo;', 'Case Study 1'),
                                ('&ldquo;Tried ads&rdquo;', 'Own Proof'))))

# ---- awareness levels ------------------------------------------------------
LEVELS = ''.join(
    '<div class="mb__lvl"><span class="mb__bar" style="width:%dpx; background:%s">'
    '</span><span class="mb__lab">%s</span></div>' % (w, c, t)
    for w, c, t in ((40, BLUES[0], 'Unaware'), (66, BLUES[1], 'Curious'),
                    (92, BLUES[2], 'Researching'), (118, BLUES[3], 'Struggling'),
                    (144, BLUES[4], 'Plateaued')))

# ---- pain and dream --------------------------------------------------------
PAIN = ('<div class="mb__row" style="gap:14px">'
        '<div class="mb__half mb__half--p">%s<p>Pain</p></div>'
        '<div class="mb__half mb__half--g">%s<p>Dream</p></div></div>'
        % (glyph('flame', 'mb__g--p'), glyph('fly', 'mb__g--g')))

# ---- the skeleton ----------------------------------------------------------
SKEL = ('<div class="mb__row" style="justify-content:space-between">'
        '<span class="mb__chip">Hook</span><div class="mb__arr"></div>'
        '<span class="mb__chip">Body</span><div class="mb__arr"></div>'
        '<span class="mb__chip">CTA</span></div>'
        '<div class="mb__row" style="margin-top:16px; justify-content:space-between">'
        + ''.join('<span class="mb__lab"><b style="color:#1E4E8C">%s</b>%s</span>'
                  % (w[0], w[1:])
                  for w in ('Situation', 'Reframe', 'Proof', 'Ask'))
        + '</div>')

# ---- the journeys ----------------------------------------------------------
LANES = ''.join(
    '<div class="mb__lane"><span class="mb__who">%s</span>%s</div>'
    % (who, ''.join('<span class="mb__stop%s">%s</span>'
                    % (' mb__stop--on' if j == on else '', s)
                    for j, s in enumerate(stops)))
    for who, stops, on in (
        ('ICP 1', ('Ad', 'Opt-in', 'VSL', 'Call'), 2),
        ('ICP 2', ('Ad', 'Organic', 'Webinar', 'Call'), 1)))

# ---------------------------------------------------------------------------
card(0, 0, 424, 252, -1.2, 'One ICP, many <i>angles</i>', ANGLES)
card(0, 276, 424, 246, 0.9, 'Awareness <i>levels</i>', LEVELS)
card(0, 548, 424, 206, -0.7, 'Pain vs <i>Dream</i>', PAIN)

card(456, 24, 424, 212, 1.0, '<i>Objection</i> &rarr; Proof', OBJ)
card(456, 260, 424, 196, -0.9, 'Hook, Body, <i>CTA</i>', SKEL)
card(456, 486, 424, 222, 0.7, 'Two ICPs, two <i>journeys</i>', LANES)

wires = [
    wire(428, 126, 452, 116),
    wire(212, 258, 212, 270, 90),
    wire(212, 528, 212, 542, 90),
    wire(668, 242, 668, 254, 90),
    wire(668, 462, 668, 480, 90),
    wire(430, 640, 450, 616),
]

ink = ['<ellipse class="ring" cx="212" cy="138" rx="62" ry="46" '
       'transform="rotate(-3 212 138)"/>']

out = (TPL.replace('__W__', str(W)).replace('__H__', str(H))
          .replace('__BW__', str(BW)).replace('__BH__', str(BH))
          .replace('__WIRES__', '\n'.join('        ' + w for w in wires))
          .replace('__INK__', '\n'.join('        ' + i for i in ink))
          .replace('__CARDS__', '\n'.join(cards)))

path = 'slides/wide/thumb-messaging-board.html'
open(path, 'w').write(out)
print('wrote %s' % path)
