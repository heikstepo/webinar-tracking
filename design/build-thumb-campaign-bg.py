#!/usr/bin/env python3
"""A full-frame thumbnail background: the campaign structure board.

1920x1080, built to have a person composited into the middle of it. The two
outer thirds carry everything that has to be read; the middle strip holds only
loose icon tiles, so whatever the cut-out covers, nothing is lost.

Content is what the deck and the two Meta pieces actually cover: the campaign
and its one ad set, three creatives per ad, one ad one purpose, sequence
learning, asset consolidation, and the purchase journey.

    ./build-thumb-campaign-bg.py    writes the background
"""
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

# Line glyphs, same vocabulary as the rest of the deck.
G = {
    'ad': '''<rect x="12" y="14" width="100" height="96" rx="11"/>
        <rect x="24" y="26" width="76" height="40" rx="6"/>
        <path class="f" d="M56 36 L 72 46 L 56 56 Z"/>
        <path d="M24 78 H 92 M24 88 H 72"/>
        <rect class="f" x="24" y="96" width="40" height="6" rx="3"/>''',
    'play': '''<rect x="10" y="22" width="104" height="80" rx="12"/>
        <path class="f" d="M52 44 L 80 62 L 52 80 Z"/>''',
    'image': '''<rect x="10" y="22" width="104" height="80" rx="12"/>
        <circle class="f" cx="38" cy="46" r="8"/>
        <path d="M18 92 L 48 62 L 70 84 L 86 70 L 106 92"/>''',
    'chart': '''<path d="M18 16 V 104 H 108"/>
        <path class="h" d="M32 88 L 56 62 L 74 76 L 102 38"/>
        <path class="f" d="M102 38 L 102 58 L 86 38 Z"/>''',
    'target': '''<circle cx="62" cy="62" r="46"/><circle cx="62" cy="62" r="28"/>
        <circle class="f" cx="62" cy="62" r="10"/>''',
}


def glyph(name, size, cls='cb__g'):
    return ('<svg class="%s" style="width:%dpx;height:%dpx" viewBox="0 0 124 124" '
            'aria-hidden="true">%s</svg>' % (cls, size, size, G[name]))


TPL = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Campaign Structure</title>
<link rel="stylesheet" href="../../4pi.css">
<link rel="stylesheet" href="../../voice-quiet.css">
<style>
/* ============================================================================
   See build-thumb-campaign-bg.py. A board to composite a person into: the two
   outer thirds hold everything that has to be read, the middle strip only
   loose tiles.

   Class names are prefixed cb; neither shared sheet uses them.
   ========================================================================= */
@page { size: __W__px __H__px; margin: 0; }

.slide {
  position: relative;
  width: __W__px; height: __H__px; padding: 0; background: var(--ground);
  background-image: radial-gradient(#D7DBE2 1.7px, transparent 1.8px);
  background-size: 30px 30px; background-position: 10px 10px;
}

.cb__h {
  position: absolute; left: 0; top: 24px; width: __W__px; margin: 0;
  text-align: center;
  font-size: 152px; font-weight: 900; letter-spacing: -0.046em; line-height: 1;
  color: var(--ink);
}
.cb__h b { color: var(--blue); font-weight: 700; }

/* ---- board furniture ----------------------------------------------------- */
.cb__wires { position: absolute; inset: 0; }
.cb__wires svg { display: block; width: 100%; height: 100%; }
.cb__wires .flow { fill: none; stroke: #AEB8C6; stroke-width: 3;
                   stroke-linecap: round; stroke-dasharray: 9 9; }
.cb__wires .tip { fill: #AEB8C6; }
.cb__ink { z-index: 4; pointer-events: none; }
.cb__ink .ring { fill: none; stroke: var(--red); stroke-width: 4; }

.cb__card {
  position: absolute; box-sizing: border-box;
  background: var(--surface); border: 1px solid var(--hairline);
  border-radius: 20px; padding: 17px 21px;
  box-shadow: 0 3px 14px rgba(20, 30, 50, 0.08);
}
.cb__t {
  margin: 0 0 13px;
  font-size: 27px; font-weight: 600; letter-spacing: -0.014em; color: var(--ink);
}
.cb__t i { font-style: normal; color: var(--blue); }

.cb__row { display: flex; align-items: center; gap: 12px; }
.cb__g {
  display: block; fill: none; stroke: #7FA8DC; stroke-width: 3.4;
  stroke-linecap: round; stroke-linejoin: round;
}
.cb__g .h { stroke: var(--blue); stroke-width: 4.4; }
.cb__g .f { fill: var(--blue); stroke: none; }

.cb__chip {
  padding: 6px 12px; border-radius: 9px;
  background: #E4EFFD; color: #1E4E8C;
  font-size: 17px; font-weight: 600; white-space: nowrap;
}
.cb__cap { margin: 7px 0 0; font-size: 16px; font-weight: 600; color: var(--ink-3); }
.cb__lab { width: 84px; flex: none; font-size: 16px; font-weight: 600; color: var(--ink-3); }
.cb__sq { width: 27px; height: 27px; border-radius: 7px; background: #CFE2FA; }
/* an ad set, drawn as a tray of ads */
.cb__set {
  display: flex; align-items: center; gap: 7px;
  padding: 9px 11px; border-radius: 12px; background: #E4EFFD;
}
.cb__set--off { background: none; border: 2px dashed #CBD3DD; padding: 7px 9px; }
.cb__pin { width: 22px; height: 22px; border-radius: 50%; background: var(--surface); }
.cb__set--off .cb__pin { background: #DDE2E9; }
.cb__coin {
  width: 38px; height: 38px; border-radius: 50%; background: var(--blue);
  display: flex; align-items: center; justify-content: center;
  font-size: 20px; font-weight: 700; color: #fff;
}

/* the campaign */
.cb__camp { background: #E4EFFD; border-radius: 14px; padding: 12px 14px; }
.cb__camp p { margin: 0 0 10px; text-align: center;
              font-size: 18px; font-weight: 600; color: #1E4E8C; }
.cb__ads { display: grid; grid-template-columns: repeat(4, 46px);
           gap: 12px; justify-content: center; }
.cb__ad { width: 46px; height: 46px; border-radius: 50%; background: var(--surface); }
.cb__ad--open { background: none; border: 2px dashed #BFD6F7; box-sizing: border-box; }

/* little boxes and rails reused across the cards */
.cb__box {
  box-sizing: border-box; padding: 7px 0; width: 70px; text-align: center;
  border: 1px solid var(--hairline); border-radius: 10px; background: var(--surface);
  font-size: 16px; font-weight: 600; color: var(--ink);
}
.cb__arr { width: 18px; height: 2px; background: #B6C2D0; flex: none; }
.cb__cr { width: 30px; height: 52px; border-radius: 8px; background: #4A97EF; }
.cb__dot { width: 16px; height: 16px; border-radius: 50%; background: #9DC2EE; }
.cb__dot--on { background: var(--blue); }
.cb__tick {
  width: 38px; height: 38px; border-radius: 50%;
  background: #E7F5E3; border: 3px solid #34A518;
  display: flex; align-items: center; justify-content: center;
  font-size: 22px; line-height: 1; color: #248A13;
}
.cb__n {
  width: 30px; height: 30px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: 17px; font-weight: 700; color: #fff; background: #5BA1F0;
}

/* the middle strip: texture only, and pale, because a person goes over it */
.cb__tile {
  position: absolute; box-sizing: border-box;
  width: 104px; height: 104px; border-radius: 20px;
  background: var(--surface); border: 1px solid var(--hairline);
  box-shadow: 0 2px 8px rgba(20, 30, 50, 0.05);
  display: flex; align-items: center; justify-content: center;
  opacity: 0.85;
}
.cb__tile svg { stroke: #9DBCE0; }
.cb__tile svg .f { fill: #9DBCE0; }
.cb__tile svg .h { stroke: #9DBCE0; }

.cb__meta { position: absolute; }
.cb__meta svg { display: block; fill: #C3CAD4; }
</style>
</head>
<body>

<section class="slide">

  <h1 class="cb__h">Campaign Structure</h1>

  <div class="cb__wires">
    <svg viewBox="0 0 __W__ __H__" aria-hidden="true">
__WIRES__
    </svg>
  </div>

__PARTS__

  <div class="cb__wires cb__ink">
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


def card(x, y, w, h, rot, title, body):
    return ('<div class="cb__card" style="left:%gpx; top:%gpx; width:%gpx; '
            'height:%gpx; transform:rotate(%gdeg)">'
            '<p class="cb__t">%s</p>%s</div>' % (x, y, w, h, rot, title, body))


def tip(x, y, a=0):
    return ('<g transform="translate(%g %g) rotate(%g)">'
            '<path class="tip" d="M0 0 L -20 -8 L -20 8 Z"/></g>' % (x, y, a))


def wire(x1, y1, x2, y2, a=0):
    dx, dy = (x2 - x1) * 0.45, (y2 - y1) * 0.45
    if abs(x2 - x1) >= abs(y2 - y1):
        c1, c2 = (x1 + dx, y1), (x2 - dx, y2)
    else:
        c1, c2 = (x1, y1 + dy), (x2, y2 - dy)
    return ('<path class="flow" d="M%g %g C %g %g, %g %g, %g %g"/>'
            % (x1, y1, c1[0], c1[1], c2[0], c2[1], x2, y2)) + tip(x2, y2, a)


parts = []


def column(x, top, w, gap, items):
    """Stack cards down a column so the two sides end on the same line."""
    y = top
    for h, rot, title, body in items:
        parts.append(card(x, y, w, h, rot, title, body))
        y += h + gap
    return y - gap


def chain(items, tick=True):
    """Numbered discs joined by rails, optionally ending in the sale."""
    out = []
    for i, n in enumerate(items):
        if i:
            out.append('<div class="cb__arr"></div>')
        out.append('<span class="cb__n">%s</span>' % n)
    if tick:
        out.append('<div class="cb__arr"></div><div class="cb__tick">&#10003;</div>')
    return '<div class="cb__row" style="justify-content:center; gap:10px">%s</div>' % ''.join(out)


CAMP = ('<div class="cb__camp"><p>1 Control Ad Set</p>'
        '<div class="cb__ads">'
        + '<div class="cb__ad"></div>' * 5
        + '<div class="cb__ad cb__ad--open"></div>' * 3
        + '</div></div>'
        '<div class="cb__row" style="margin-top:14px; justify-content:center">'
        '<span class="cb__chip">5&ndash;8 Unique Ads</span>'
        '<span class="cb__chip">Broad</span></div>')

CREATIVES = ('<div class="cb__row" style="justify-content:center; gap:18px">'
             + glyph('ad', 72)
             + '<div class="cb__arr" style="width:26px"></div>'
             + '<div class="cb__row" style="gap:12px">'
             + '<span class="cb__cr"></span>' * 3
             + '</div></div>')

PURPOSE = ('<div class="cb__row" style="justify-content:space-between">'
           + ''.join('<div style="text-align:center">%s<p class="cb__cap">%s</p></div>'
                     % (glyph(g, 58), c)
                     for g, c in (('target', 'Awareness'), ('play', 'Education'),
                                  ('image', 'Objection'), ('chart', 'Conversion')))
           + '</div>')

JOURNEY = chain(['1', '2', '3', '4', '5', '6'])

SEQUENCE = ('<div class="cb__row" style="justify-content:center; gap:10px">'
            + '<span class="cb__dot"></span>' * 4
            + '<span class="cb__dot cb__dot--on"></span>'
            '<div class="cb__arr"></div><div class="cb__tick">&#10003;</div></div>'
            '<div class="cb__row" style="margin-top:16px; justify-content:center">'
            '<span class="cb__chip">Which ad next?</span>'
            '<span class="cb__chip">Impression &rarr; Purchase</span></div>')

CONSOLIDATE = ('<div class="cb__row" style="justify-content:center; gap:16px">'
               '<div class="cb__row" style="gap:8px">'
               + '<span class="cb__cr" style="height:46px"></span>' * 3
               + '</div><div class="cb__arr" style="width:26px"></div>'
               + glyph('ad', 66) + '<div class="cb__arr" style="width:26px"></div>'
               + glyph('chart', 60) + '</div>')

CONCEPTS = ''.join(
    '<div class="cb__row" style="gap:8px; margin-top:%dpx">'
    '<span class="cb__lab">Concept %d</span>%s</div>'
    % (0 if i == 0 else 10, i + 1, '<span class="cb__sq"></span>' * 6)
    for i in range(3))

PIXEL = ('<div class="cb__row" style="justify-content:center; gap:10px">'
         '<div class="cb__box">Opt-in</div><div class="cb__arr"></div>'
         '<div class="cb__box">VSL</div><div class="cb__arr"></div>'
         '<div class="cb__box">TY A</div></div>'
         '<div class="cb__row" style="margin-top:14px; justify-content:center">'
         '<span class="cb__chip">Conversion Event</span>'
         '<span class="cb__chip">Schedule</span></div>')

# The three questions the deck asks about this structure. They sit in the
# middle because a question reads even half covered, where a diagram does not.
BROAD = ('<div class="cb__row" style="justify-content:center; gap:16px">'
         + glyph('target', 62)
         + '<div class="cb__arr" style="width:24px"></div>'
         + '<div class="cb__row" style="gap:7px">'
         + '<span class="cb__ad" style="width:34px;height:34px;'
           'background:#CFE2FA"></span>' * 5
         + '</div></div>')

ONESET = ('<div class="cb__row" style="justify-content:center; gap:14px">'
          '<div class="cb__set"><span class="cb__pin"></span><span class="cb__pin"></span>'
          '<span class="cb__pin"></span><span class="cb__pin"></span></div>'
          '<div class="cb__tick">&#10003;</div></div>'
          '<div class="cb__row" style="margin-top:12px; justify-content:center; gap:8px">'
          + '<div class="cb__set cb__set--off"><span class="cb__pin"></span>'
            '<span class="cb__pin"></span></div>' * 3
          + '</div>')

SPEND = ('<div class="cb__row" style="justify-content:center; gap:10px">'
         + '<span class="cb__coin">$</span>' * 3
         + '<div class="cb__arr" style="width:24px"></div>'
         + glyph('ad', 56) + '</div>'
         '<div class="cb__row" style="margin-top:12px; justify-content:center">'
         '<span class="cb__chip">Spend is earned</span></div>')

DIVERSITY = ('<div class="cb__row" style="justify-content:center; gap:10px">'
             + ''.join('<span class="cb__cr" style="width:26px;height:44px;'
                       'background:%s"></span>' % c
                       for c in ('#9DC2EE', '#6FA8E8', '#4A97EF', '#2E87E8', '#0071E3'))
             + '</div>')

column(40, 214, 600, 14, [
    (286, -1.2, '1 CBO Campaign', CAMP),
    (146, 0.9, '3 Creatives per <i>Ad</i>', CREATIVES),
    (192, -0.6, '1 Ad = 1 <i>Purpose</i>', PURPOSE),
    (162, 0.8, 'Map the Purchase <i>Journey</i>', JOURNEY),
])

column(664, 214, 592, 14, [
    (200, 0.8, 'Why a <i>Broad</i> Ad Set?', BROAD),
    (200, -1.0, 'Why 1 <i>Control</i> Ad Set?', ONESET),
    (200, 0.6, 'Scaling &amp; <i>Testing</i>', SPEND),
    (190, -0.7, 'Creative <i>Diversity</i>?', DIVERSITY),
])

column(1280, 214, 600, 14, [
    (202, 1.1, 'Sequence <i>Learning</i>', SEQUENCE),
    (200, -0.9, 'Fewer Ads, More <i>Creative</i>', CONSOLIDATE),
    (196, 0.7, 'Concept <i>Testing</i>', CONCEPTS),
    (192, -0.5, 'Pixel Conditioning', PIXEL),
])

wires = [
    wire(644, 330, 660, 330),
    wire(1260, 330, 1276, 330),
    wire(340, 504, 340, 530, 90),
    wire(340, 664, 340, 690, 90),
    wire(340, 870, 340, 896, 90),
    wire(1580, 418, 1580, 444, 90),
    wire(1580, 646, 1580, 672, 90),
    wire(1580, 870, 1580, 896, 90),
]

# Tight enough to ring the count and nothing else: at full width it ran over
# the card below and took the chip beside it with it.
ink = ['<ellipse class="ring" cx="262" cy="476" rx="120" ry="29" '
       'transform="rotate(-2 262 476)"/>']

out = (TPL.replace('__W__', str(W)).replace('__H__', str(H))
          .replace('__WIRES__', '\n'.join('      ' + w for w in wires))
          .replace('__INK__', '\n'.join('      ' + i for i in ink))
          .replace('__PARTS__', '\n'.join('  ' + p for p in parts)))

path = 'slides/wide/thumb-campaign-bg.html'
open(path, 'w').write(out)
print('wrote %s' % path)
