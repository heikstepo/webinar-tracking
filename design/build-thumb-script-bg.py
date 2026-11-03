#!/usr/bin/env python3
"""A full-frame thumbnail background: the ad-script board, as a sprawl.

1920x1080, built to have a person composited onto it. Not a grid of cards: a
whiteboard that has been worked on. Small frames and notes at odd angles, lines
running between them in every direction, clusters ringed with dashed boxes,
a few things circled in red.

Everything on it is something the deck covers about writing the ads: the
Situation / Reframe / Proof / Ask skeleton and the Hook / Body / CTA it groups
into, the awareness levels, pain versus dream, the offer line and its parts,
one ad one purpose, three creatives per ad, concept testing, the ad sequence,
the interest spectrum, the two ICPs, proof, and the vertical cut.

    ./build-thumb-script-bg.py    writes the background
"""
import math
import os
import re

os.chdir(os.path.dirname(os.path.abspath(__file__)))

W, H = 1920, 1080


def logo(slug):
    src = open('logos/%s.svg' % slug).read()
    box = re.search(r'viewBox="([^"]+)"', src).group(1)
    body = src[src.index('>', src.index('<svg')) + 1:src.rindex('</svg>')]
    return box, re.sub(r'\s*fill="[^"]*"', '', body).strip()


META_BOX, META = logo('meta')

G = {
    'play': '<path class="f" d="M46 34 L 86 62 L 46 90 Z"/>',
    'chart': '''<path d="M18 16 V 104 H 108"/>
        <path class="h" d="M32 88 L 56 62 L 74 76 L 102 38"/>''',
    'target': '''<circle cx="62" cy="62" r="44"/><circle cx="62" cy="62" r="26"/>
        <circle class="f" cx="62" cy="62" r="9"/>''',
    'speech': '''<path d="M14 30 a 12 12 0 0 1 12 -12 H 98 a 12 12 0 0 1 12 12
        V 76 a 12 12 0 0 1 -12 12 H 56 L 32 108 V 88 H 26 a 12 12 0 0 1 -12 -12 Z"/>
        <path class="h" d="M32 42 H 92"/><path d="M32 58 H 76"/>''',
    'script': '''<rect x="20" y="8" width="84" height="108" rx="11"/>
        <path class="h" d="M34 32 H 90"/>
        <path d="M34 50 H 90 M34 66 H 76 M34 82 H 90 M34 98 H 62"/>''',
    'image': '''<rect x="10" y="22" width="104" height="80" rx="12"/>
        <circle class="f" cx="38" cy="46" r="8"/>
        <path d="M18 92 L 48 62 L 70 84 L 86 70 L 106 92"/>''',
    'flame': '''<path d="M70 10 C 70 36, 52 42, 50 60 C 47 47, 43 42, 38 38
        C 35 50, 26 58, 26 76 a 36 36 0 0 0 72 0 C 98 54, 86 40, 70 10 Z"/>''',
    'fly': '''<path d="M62 42 V 94"/>
        <path d="M62 50 C 40 22, 12 28, 14 54 C 16 78, 44 82, 62 68"/>
        <path d="M62 50 C 84 22, 112 28, 110 54 C 108 78, 80 82, 62 68"/>
        <path d="M58 40 L 46 22 M66 40 L 78 22"/>''',
    'person': '''<circle cx="62" cy="38" r="20"/>
        <path d="M22 110 C 22 82, 40 68, 62 68 C 84 68, 102 82, 102 110"/>''',
}

TPL = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Ad Scripts</title>
<link rel="stylesheet" href="../../4pi.css">
<link rel="stylesheet" href="../../voice-quiet.css">
<style>
/* ============================================================================
   See build-thumb-script-bg.py. A worked-on whiteboard, not a layout: small
   frames and notes at odd angles with lines running between them.

   Class names are prefixed sb; neither shared sheet uses them.
   ========================================================================= */
@page { size: __W__px __H__px; margin: 0; }

.slide {
  position: relative;
  width: __W__px; height: __H__px; padding: 0; background: var(--ground);
  background-image: radial-gradient(#D9DDE3 1.6px, transparent 1.7px);
  background-size: 28px 28px; background-position: 8px 8px;
}

/* ---- lines --------------------------------------------------------------- */
.sb__w { position: absolute; inset: 0; z-index: 1; }
.sb__w svg { display: block; width: 100%; height: 100%; }
.sb__w .ln { fill: none; stroke: #A9B3C0; stroke-width: 2.2; stroke-linecap: round; }
.sb__w .dash { stroke-dasharray: 8 8; }
.sb__w .pale { stroke: #C3CBD5; stroke-width: 2; }
.sb__w .tip { fill: #A9B3C0; }
.sb__over { z-index: 5; }

.sb__ink { position: absolute; inset: 0; z-index: 6; pointer-events: none; }
.sb__ink svg { display: block; width: 100%; height: 100%; }
.sb__ink .mk { fill: none; stroke: var(--red); stroke-width: 3.4;
               stroke-linecap: round; }

/* ---- nodes --------------------------------------------------------------- */
.sb__n {
  position: absolute; box-sizing: border-box; z-index: 3;
  background: var(--surface); border: 1px solid var(--hairline);
  border-radius: 9px; box-shadow: 0 2px 7px rgba(20, 30, 50, 0.07);
  padding: 6px;
}
.sb__th {
  background: #E2EDFB; border-radius: 5px; width: 100%;
  display: flex; align-items: center; justify-content: center;
}
.sb__ln { height: 4px; border-radius: 3px; background: #DCE1E8; margin-top: 5px; }
.sb__ln--b { background: #B9CEEA; }

/* a ring round a cluster */
.sb__grp {
  position: absolute; box-sizing: border-box; z-index: 2;
  border: 2px dashed #C2CBD6; border-radius: 16px;
}
.sb__grp--b { border-color: #AFCBEE; }
.sb__grp--r { border-color: #E9AEB8; }

/* free text on the board */
.sb__h {
  position: absolute; z-index: 4; margin: 0; white-space: nowrap;
  font-weight: 600; letter-spacing: -0.012em; line-height: 1.2; color: var(--ink);
}
.sb__h i { font-style: normal; color: var(--blue); }
.sb__h em { font-style: normal; color: var(--ink-3); font-weight: 600; }
.sb__h b { font-weight: 600; color: var(--blue); }

.sb__pill {
  position: absolute; z-index: 4; white-space: nowrap;
  padding: 4px 9px; border-radius: 7px;
  background: #E4EFFD; color: #1E4E8C;
  font-size: 15px; font-weight: 600;
}
.sb__pill--open { background: var(--surface); border: 1px dashed #BFD6F7; color: #6E8CB4; }
.sb__pill--p { background: #FBE4E8; color: #AE3047; }
.sb__pill--g { background: #E7F5E3; color: #3C7F2C; }

.sb__box {
  position: absolute; z-index: 3; box-sizing: border-box; white-space: nowrap;
  background: var(--surface); border: 1.5px solid #C6CED9; border-radius: 8px;
  display: flex; align-items: center; justify-content: center;
  font-weight: 600; color: var(--ink);
}
.sb__box--b { border-color: #8FBDF3; color: #1E4E8C; background: #F2F7FE; }

.sb__bar { position: absolute; z-index: 3; border-radius: 4px; }
.sb__dot { position: absolute; z-index: 3; border-radius: 50%; }

.sb__g {
  display: block; fill: none; stroke: #7FA8DC; stroke-width: 3.6;
  stroke-linecap: round; stroke-linejoin: round;
}
.sb__g .h { stroke: var(--blue); stroke-width: 4.4; }
.sb__g .f { fill: var(--blue); stroke: none; }
.sb__g--p { stroke: #D4536B; }
.sb__g--p .f { fill: #D4536B; }
.sb__g--g { stroke: #52A33C; }

.sb__brace { position: absolute; z-index: 3; }
.sb__brace svg { display: block; fill: none; stroke: #9FC3EE; stroke-width: 2.6;
                 stroke-linecap: round; }

.sb__phone {
  position: absolute; z-index: 3; box-sizing: border-box;
  border-radius: 14px; border: 3px solid #C2CAD4; background: var(--surface);
  padding: 7px 6px; box-shadow: 0 2px 8px rgba(20, 30, 50, 0.07);
}
.sb__screen {
  border-radius: 8px; background: #E2EDFB;
  display: flex; align-items: center; justify-content: center;
}
.sb__screen svg { width: 36%; height: 36%; }
.sb__cta { border-radius: 6px; background: var(--blue); }

.sb__cash {
  position: absolute; z-index: 2; margin: 0;
  font-weight: 700; letter-spacing: -0.03em; color: #C6CDD7;
}
.sb__meta { position: absolute; z-index: 2; }
.sb__meta svg { display: block; fill: #C8CFD8; }
.sb__tick {
  position: absolute; z-index: 3; box-sizing: border-box; border-radius: 50%;
  background: #E7F5E3; border: 2.5px solid #34A518;
  display: flex; align-items: center; justify-content: center;
  line-height: 1; color: #248A13;
}
</style>
</head>
<body>

<section class="slide">

  <div class="sb__w">
    <svg viewBox="0 0 __W__ __H__" aria-hidden="true">
__WIRES__
    </svg>
  </div>

__PARTS__

  <div class="sb__w sb__over">
    <svg viewBox="0 0 __W__ __H__" aria-hidden="true">
__OVER__
    </svg>
  </div>

  <div class="sb__ink">
    <svg viewBox="0 0 __W__ __H__" aria-hidden="true">
__INK__
    </svg>
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

parts, wires, over, ink = [], [], [], []


def rot(r):
    return ' transform:rotate(%gdeg);' % r if r else ''


def svg(name, w, h, cls=''):
    return ('<svg class="sb__g%s" viewBox="0 0 124 124" style="width:%s;height:%s" '
            'aria-hidden="true">%s</svg>' % (cls, w, h, G[name]))


# ---- the pieces -----------------------------------------------------------
def frame(x, y, w, h, r=0, kind='play', lines=2):
    """A little screenshot: a thumbnail with a line or two under it."""
    th = h - 12 - lines * 9
    parts.append(
        '<div class="sb__n" style="left:%gpx; top:%gpx; width:%gpx; height:%gpx;%s">'
        '<div class="sb__th" style="height:%gpx">%s</div>%s</div>'
        % (x, y, w, h, rot(r), th, svg(kind, '42%', '46%'),
           ''.join('<div class="sb__ln%s" style="width:%d%%"></div>'
                   % ('--b' if i == 0 else '', 92 - i * 26) for i in range(lines))))


def plain(x, y, w, h, r=0):
    parts.append('<div class="sb__n" style="left:%gpx; top:%gpx; width:%gpx;'
                 ' height:%gpx;%s"><div class="sb__th" style="height:%gpx"></div>'
                 '<div class="sb__ln" style="width:78%%"></div></div>'
                 % (x, y, w, h, rot(r), h - 22))


def head(x, y, text, size=24, r=0):
    parts.append('<p class="sb__h" style="left:%gpx; top:%gpx; font-size:%gpx;%s">'
                 '%s</p>' % (x, y, size, rot(r), text))


def pill(x, y, text, tone='', r=0, size=15):
    parts.append('<span class="sb__pill%s" style="left:%gpx; top:%gpx;'
                 ' font-size:%gpx;%s">%s</span>'
                 % (' sb__pill--' + tone if tone else '', x, y, size, rot(r), text))


def box(x, y, w, h, text, tone='', r=0, size=15):
    parts.append('<div class="sb__box%s" style="left:%gpx; top:%gpx; width:%gpx;'
                 ' height:%gpx; font-size:%gpx;%s">%s</div>'
                 % (' sb__box--' + tone if tone else '', x, y, w, h, size,
                    rot(r), text))


def group(x, y, w, h, tone='', r=0):
    parts.append('<div class="sb__grp%s" style="left:%gpx; top:%gpx; width:%gpx;'
                 ' height:%gpx;%s"></div>'
                 % (' sb__grp--' + tone if tone else '', x, y, w, h, rot(r)))


def bar(x, y, w, h, c):
    parts.append('<div class="sb__bar" style="left:%gpx; top:%gpx; width:%gpx;'
                 ' height:%gpx; background:%s"></div>' % (x, y, w, h, c))


def dot(x, y, d, c):
    parts.append('<div class="sb__dot" style="left:%gpx; top:%gpx; width:%gpx;'
                 ' height:%gpx; background:%s"></div>' % (x, y, d, d, c))


def disc(x, y, d, c, text, size=19):
    parts.append('<div class="sb__dot" style="left:%gpx; top:%gpx; width:%gpx;'
                 ' height:%gpx; background:%s; display:flex; align-items:center;'
                 ' justify-content:center; color:#fff; font-size:%gpx;'
                 ' font-weight:700">%s</div>' % (x, y, d, d, c, size, text))


def mark(x, y, size, name, tone=''):
    parts.append('<div style="position:absolute; z-index:3; left:%gpx; top:%gpx">'
                 '%s</div>'
                 % (x, y, svg(name, '%gpx' % size, '%gpx' % size,
                               ' sb__g--' + tone if tone else '')))


def brace(x, y, h, r=0):
    half = h / 2
    parts.append(
        '<div class="sb__brace" style="left:%gpx; top:%gpx;%s">'
        '<svg viewBox="0 0 26 %g" height="%g" aria-hidden="true">'
        '<path d="M0 2 C 8 2, 10 5, 10 12 L 10 %g C 10 %g, 14 %g, 22 %g '
        'C 14 %g, 10 %g, 10 %g L 10 %g C 10 %g, 8 %g, 0 %g"/></svg></div>'
        % (x, y, rot(r), h, h, half - 12, half - 5, half, half, half,
           half + 5, half + 12, h - 12, h - 5, h - 2, h - 2))


def phone(x, y, w, r=0):
    h = w * 1.9
    parts.append('<div class="sb__phone" style="left:%gpx; top:%gpx; width:%gpx;'
                 ' height:%gpx;%s"><div class="sb__screen" style="height:%gpx">%s'
                 '</div><div class="sb__ln" style="width:86%%"></div>'
                 '<div class="sb__ln" style="width:60%%"></div>'
                 '<div class="sb__cta" style="height:%gpx; margin-top:7px"></div>'
                 '</div>' % (x, y, w, h, rot(r), h * 0.55, svg('play', '36%', '36%'),
                             w * 0.18))


def tick(x, y, d):
    parts.append('<div class="sb__tick" style="left:%gpx; top:%gpx; width:%gpx;'
                 ' height:%gpx; font-size:%gpx">&#10003;</div>'
                 % (x, y, d, d, d * 0.54))


# ---- lines ----------------------------------------------------------------
def tip(x, y, a):
    return ('<g transform="translate(%g %g) rotate(%g)">'
            '<path class="tip" d="M0 0 L -15 -6 L -15 6 Z"/></g>' % (x, y, a))


def link(x1, y1, x2, y2, bend=0.0, dash=False, pale=False, arrow=True, layer=None):
    """A line with a kink in it, so nothing on the board is quite straight."""
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    dx, dy = x2 - x1, y2 - y1
    cx, cy = mx - dy * bend, my + dx * bend
    cls = 'ln' + (' dash' if dash else '') + (' pale' if pale else '')
    s = '<path class="%s" d="M%g %g Q %g %g, %g %g"/>' % (cls, x1, y1, cx, cy, x2, y2)
    if arrow:
        s += tip(x2, y2, math.degrees(math.atan2(y2 - cy, x2 - cx)))
    (over if layer == 'over' else wires).append(s)


BLUES = ['#C5DDFA', '#A7CCF7', '#7CB2F3', '#4A97EF', '#2E87E8', '#0071E3']

# ===========================================================================
# the board
# ===========================================================================

# ---- far left: who you are writing to -------------------------------------
group(22, 30, 320, 272, 'b', -0.8)
head(38, 40, 'Who you&rsquo;re <i>writing to</i>', 20, -0.8)

mark(44, 74, 66, 'person')
head(52, 146, 'ICP 1', 15, -2)
mark(132, 80, 66, 'person')
head(140, 152, 'ICP 2', 15, 1.5)
pill(226, 92, 'Pain', 'p', -3)
pill(226, 134, 'Dream', 'g', 2)

head(46, 176, 'Awareness levels', 15)
for i, (w, c, t) in enumerate((
        (38, BLUES[0], 'Unaware'), (58, BLUES[1], 'Curious'),
        (78, BLUES[2], 'Researching'), (98, BLUES[3], 'Struggling'),
        (118, BLUES[5], 'Plateaued'))):
    y = 202 + i * 20
    bar(46, y, w, 12, c)
    head(46 + w + 14, y - 3, '<em>%s</em>' % t, 14)

# ---- pain and dream --------------------------------------------------------
mark(40, 332, 72, 'flame', 'p')
head(44, 404, 'Pain', 18, -2)
mark(146, 338, 72, 'fly', 'g')
head(150, 404, 'Dream', 18, 1.6)
box(244, 350, 92, 34, 'Angle', '', 2.5)

# ---- the skeleton ----------------------------------------------------------
group(20, 444, 330, 292, 'r', 0.7)
head(36, 452, 'S R P A', 25, 0.7)
for i, t in enumerate(('Situation', 'Reframe', 'Proof', 'Ask')):
    head(42, 494 + i * 52, '<b>%s</b>%s' % (t[0], t[1:]), 23, -0.6 + i * 0.4)
brace(194, 488, 46, 0.5)
head(226, 498, '<i>Hook</i>', 22)
brace(194, 548, 98, -0.4)
head(226, 584, '<i>Body</i>', 22)
brace(194, 658, 46, 0.6)
head(226, 668, '<i>CTA</i>', 22)

# ---- proof, bottom left ----------------------------------------------------
head(30, 758, 'Proof', 21, -1.2)
for i in range(3):
    y = 794 + i * 54
    parts.append('<div class="sb__n" style="left:%gpx; top:%gpx; width:238px;'
                 ' height:44px; padding:8px 9px;%s">'
                 '<div class="sb__ln sb__ln--b" style="margin-top:0; width:%d%%">'
                 '</div><div class="sb__ln" style="width:%d%%"></div></div>'
                 % (28 + i * 9, y, rot(-1.4 + i * 1.2), 44 + i * 10, 86 - i * 8))
    tick(280 + i * 9, y + 8, 28)
pill(32, 970, '8 case studies', '', -1)

# ---- middle left: the offer ------------------------------------------------
head(368, 38, '<i>Offer</i> line', 23, -0.6)
pill(366, 76, '[Result]', '', -1.5, 16)
head(456, 80, '<em>in</em>', 16)
pill(490, 72, '[Time]', '', 1.2, 16)
head(570, 78, '<em>without</em>', 16)
pill(366, 118, '[Pain]', '', 1.8, 16)
head(442, 122, '<em>or</em>', 16)
pill(480, 114, '[Guarantee]', '', -1, 16)

group(354, 166, 268, 152, '', 1.0)
head(368, 176, 'The offer', 20, 1.0)
for i, (n, t) in enumerate((('01', 'Core Offer'), ('02', 'Bonuses'),
                            ('03', 'Guarantee'))):
    y = 212 + i * 34
    box(370, y, 34, 26, n, 'b', -1 + i * 0.9, 13)
    head(414, y + 4, '<em>%s</em>' % t, 17)

# ---- the vertical cut ------------------------------------------------------
phone(388, 350, 112, -3.5)
head(372, 586, '<i>Vertical</i> cut', 19, -2)
pill(532, 368, 'Hook', '', 2)
pill(532, 422, 'Body', '', -1.5)
pill(532, 476, 'CTA', '', 1.8)
link(528, 380, 494, 390, 0.1, layer='over')
link(528, 434, 498, 448, 0.08, layer='over')
link(528, 488, 500, 506, -0.08, layer='over')

# ---- interest spectrum -----------------------------------------------------
head(360, 628, 'Interest <i>spectrum</i>', 20, 0.6)
for i, (hh, t) in enumerate(((22, 'Curious'), (40, 'Active'),
                             (62, 'Strong'), (84, 'Convicted'))):
    x = 366 + i * 62
    bar(x, 768 - hh, 48, hh, BLUES[i * 2 if i < 3 else 5])
    head(x, 776, '<em>%s</em>' % t, 13)
head(614, 718, '$$$', 30, -4)

# ---- ICP to messaging to offer ---------------------------------------------
head(360, 830, 'ICP &rarr; Messaging &rarr; <i>Offer</i>', 19, -0.7)
for i, (w, t) in enumerate(((58, 'ICP'), (102, 'Messaging'),
                            (148, 'Offer Positioning'))):
    y = 870 + i * 30
    bar(364, y, w, 19, BLUES[1 + i * 2])
    head(364 + w + 10, y, '<em>%s</em>' % t, 15)

plain(566, 962, 76, 60, 3)
plain(228, 1008, 76, 58, -2.5)

# ---- centre: one ad, one purpose -------------------------------------------
group(650, 28, 544, 192, 'b', 0.5)
head(666, 38, '1 Ad = 1 <i>Purpose</i>', 23, 0.5)
for i, (t, g) in enumerate((('Awareness', 'target'), ('Education', 'play'),
                            ('Objection', 'speech'), ('Conversion', 'chart'))):
    x = 666 + i * 128
    frame(x, 78, 106, 94, -3 + i * 1.8, g, 1)
    head(x + 4, 180, '<em>%s</em>' % t, 14)
    if i:
        link(x - 16, 126, x - 4, 126, 0.0, pale=True)

# ---- three creatives per ad ------------------------------------------------
head(658, 244, '3 creatives per <i>ad</i>', 22, -0.8)
mark(660, 284, 78, 'script')
for i in range(3):
    frame(798 + i * 74, 282 + (i % 2) * 10, 62, 104, -4 + i * 3.5, 'play', 1)
link(748, 330, 790, 326, 0.06)
head(802, 400, '<em>same script, three cuts</em>', 14, 1)

# ---- concept testing -------------------------------------------------------
group(648, 428, 408, 178, '', -0.6)
head(664, 438, 'Concept <i>testing</i>', 21, -0.6)
for i in range(3):
    y = 478 + i * 40
    head(664, y + 6, '<em>Concept %d</em>' % (i + 1), 14)
    for j in range(5):
        dot(758 + j * 42, y, 30, '#0071E3' if j == 0 else '#CFE2FA')
tick(978, 517, 30)

# ---- the sequence ----------------------------------------------------------
head(654, 642, 'Ad <i>sequence</i>', 22, 0.7)
for i, (t, c) in enumerate((('1', '#5BA1F0'), ('2', '#5BA1F0'), ('3', '#5BA1F0'),
                            ('&#9654;', '#AEB8C6'), ('4', '#0071E3'))):
    x = 660 + i * 86
    disc(x, 686, 44, c, t)
    if i:
        link(x - 38, 708, x - 8, 708, 0.0)
tick(1090, 686, 44)
link(1048, 708, 1082, 708, 0.0)
pill(654, 746, 'Ads', '', -1.5)
pill(910, 744, 'Organic', 'open', 2)
pill(1042, 746, 'Converts', '', -1)

# ---- money -----------------------------------------------------------------
parts.append('<p class="sb__cash" style="left:600px; top:944px; font-size:94px">'
             '$$$</p>')

# ---- the page itself, down the middle where it has room --------------------
head(880, 806, 'The <i>script</i>', 22, -1.2)
parts.append('<div class="sb__n" style="left:876px; top:842px; width:330px;'
             ' height:206px; padding:16px 18px; transform:rotate(-1.4deg)">'
             + ''.join('<div class="sb__ln%s" style="margin-top:%dpx; height:%gpx;'
                       ' width:%d%%"></div>'
                       % ('--b' if i in (0, 4) else '', 0 if i == 0 else 12,
                          7 if i in (0, 4) else 6, w)
                       for i, w in enumerate((62, 96, 88, 74, 54, 92, 80, 96, 46)))
             + '</div>')
pill(1156, 862, 'Hook', '', 2.5)
pill(1156, 926, 'Body', '', -2)
pill(1156, 996, 'CTA', '', 1.5)
frame(788, 866, 84, 96, 3.5, 'play', 1)
plain(806, 996, 76, 56, -2)

# ---- right: where it lands -------------------------------------------------
group(1230, 30, 334, 326, '', 0.6)
head(1246, 40, 'Where it <i>lands</i>', 21, 0.6)
phone(1248, 80, 98, 2.5)
phone(1370, 90, 98, -2)
frame(1246, 288, 142, 58, -2, 'speech', 1)
frame(1402, 282, 142, 58, 2.6, 'image', 1)

head(1598, 40, 'Hook <em>rate</em>', 20, -1)
frame(1594, 78, 302, 146, 1.2, 'chart', 2)

# ---- objection to answer ---------------------------------------------------
head(1238, 390, 'Objection &rarr; <i>Answer</i>', 20, -0.6)
for i, t in enumerate(('&ldquo;Too busy&rdquo;', '&ldquo;Tried ads&rdquo;',
                       '&ldquo;Too soon&rdquo;')):
    y = 428 + i * 50
    box(1242, y, 152, 38, t, '', -1.5 + i * 1.3, 15)
    box(1436, y + 4, 140, 38, 'Proof', 'b', 1.2 - i * 0.9, 15)
    link(1400, y + 19, 1430, y + 23, 0.05)

group(1612, 258, 288, 326, 'b', -0.5)
head(1628, 268, '<i>Script</i> pass', 20, -0.5)
for i, t in enumerate(('Hook first', 'One idea', 'Proof in', 'One ask')):
    y = 306 + i * 44
    tick(1630, y, 28)
    head(1670, y + 5, '<em>%s</em>' % t, 16)
frame(1630, 488, 244, 82, 0.8, 'script', 1)

# ---- bottom right ----------------------------------------------------------
head(1238, 612, 'Creative <i>diversity</i>', 20, 0.8)
for i in range(6):
    frame(1242 + (i % 3) * 112, 650 + (i // 3) * 118, 96, 108,
          -4 + (i * 2.4) % 8, ('play', 'image', 'speech')[i % 3], 1)

head(1598, 616, 'Scaling &amp; <i>testing</i>', 20, -0.7)
for i, hh in enumerate((16, 26, 36, 48, 62, 78)):
    bar(1602 + i * 34, 756 - hh, 26, hh, BLUES[i])
head(1602, 766, '<em>winners take the budget</em>', 14, 0.5)

group(1586, 806, 312, 236, '', 0.5)
head(1602, 816, 'Before it runs', 20, 0.5)
for i, t in enumerate(('ICP named', 'Offer line in', 'Proof shown', 'One CTA')):
    y = 854 + i * 42
    tick(1604, y, 26)
    head(1642, y + 4, '<em>%s</em>' % t, 16)

parts.append('<div class="sb__meta" style="left:1512px; top:1004px">'
             '<svg viewBox="%s" width="58" aria-hidden="true">%s</svg></div>'
             % (META_BOX, META))

# ---- the long lines across the board ---------------------------------------
link(342, 160, 364, 112, 0.06, dash=True)
link(300, 424, 352, 246, 0.12, dash=True, pale=True)
link(352, 596, 384, 440, 0.1, dash=True)
link(342, 232, 646, 118, 0.06, dash=True, layer='over')
link(616, 196, 658, 280, 0.08, dash=True)
link(620, 290, 652, 456, -0.07, dash=True, pale=True)
link(630, 696, 654, 706, 0.0, dash=True)
link(1058, 128, 1236, 150, 0.07, dash=True, layer='over')
link(1194, 330, 1244, 312, -0.06, dash=True)
link(1060, 516, 1236, 442, 0.07, dash=True, layer='over')
link(1116, 708, 1234, 656, 0.07, dash=True)
link(1568, 176, 1592, 148, 0.08, dash=True, pale=True)
link(1580, 466, 1608, 420, 0.07, dash=True)
link(1744, 584, 1744, 612, 0.0, dash=True)
link(1558, 898, 1582, 898, 0.0, dash=True)
link(892, 402, 1236, 424, -0.06, dash=True, pale=True, layer='over')
link(240, 740, 180, 752, 0.1, dash=True)
link(870, 900, 880, 906, 0.08, dash=True, arrow=False)
link(1212, 880, 1240, 876, 0.06, dash=True)
link(508, 990, 556, 980, 0.07, dash=True, pale=True)

frame(352, 986, 80, 80, -3, 'image', 1)
frame(446, 996, 80, 80, 2.4, 'speech', 1)

# ---- the red marks ---------------------------------------------------------
ink.append('<ellipse class="mk" cx="260" cy="508" rx="68" ry="26" '
           'transform="rotate(-3 260 508)"/>')
ink.append('<path class="mk" d="M658 272 C 758 262, 858 266, 940 274"/>')
ink.append('<ellipse class="mk" cx="1112" cy="708" rx="40" ry="34" '
           'transform="rotate(6 1112 708)"/>')
ink.append('<path class="mk" d="M890 876 C 950 870, 1010 872, 1066 878"/>')

out = (TPL.replace('__W__', str(W)).replace('__H__', str(H))
          .replace('__WIRES__', '\n'.join('      ' + w for w in wires))
          .replace('__OVER__', '\n'.join('      ' + w for w in over))
          .replace('__INK__', '\n'.join('      ' + i for i in ink))
          .replace('__PARTS__', '\n'.join('  ' + p for p in parts)))

path = 'slides/wide/thumb-script-bg.html'
open(path, 'w').write(out)
print('wrote %s' % path)
