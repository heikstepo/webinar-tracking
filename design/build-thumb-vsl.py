#!/usr/bin/env python3
"""A thumbnail panel about the VSL funnel.

1240x1080 rather than 960: wider than the other panels, so it carries more and
still leaves 680px of the 16:9 frame for a talking head.

The funnel map is the hero across the top, because the shape of the funnel is
the thing being talked about; the six cards under it are the tactics the deck
covers on top of that shape.

    ./build-thumb-vsl.py    writes the panel
"""
import os
import re

os.chdir(os.path.dirname(os.path.abspath(__file__)))

W, H = 1240, 1080
BW, BH = 1160, 870


def logo(slug):
    src = open('logos/%s.svg' % slug).read()
    box = re.search(r'viewBox="([^"]+)"', src).group(1)
    body = src[src.index('>', src.index('<svg')) + 1:src.rindex('</svg>')]
    return box, re.sub(r'\s*fill="[^"]*"', '', body).strip()


MARKS = {s: logo(s) for s in ('youtube', 'meta')}


def mark(slug, size):
    box, body = MARKS[slug]
    return ('<svg class="vb__mark" style="width:%dpx;height:%dpx" viewBox="%s" '
            'aria-hidden="true">%s</svg>' % (size, size, box, body))


G = {
    'mail': '''<rect x="30" y="24" width="64" height="42" rx="6"/>
        <rect x="16" y="44" width="80" height="56" rx="7"/>
        <path class="hot" d="M22 51 L56 77 L90 51"/>''',
    'setter': '''<path d="M24 102 C 24 82, 41 72, 62 72 C 83 72, 100 82, 100 102"/>
        <circle cx="62" cy="46" r="17"/>
        <path class="hot" d="M42 46 a 20 20 0 0 1 40 0"/>
        <rect class="hot-fill" x="38" y="44" width="9" height="18" rx="4.5"/>
        <rect class="hot-fill" x="77" y="44" width="9" height="18" rx="4.5"/>''',
    'clock': '''<circle cx="62" cy="66" r="44"/>
        <path class="hot" d="M62 40 V 66 L 82 78"/>
        <path d="M48 16 H 76"/><path d="M62 16 V 22"/>''',
    'sms': '''<rect x="8" y="26" width="88" height="52" rx="12"/>
        <path d="M34 78 L34 96 L54 78"/>
        <circle class="hot-fill" cx="36" cy="52" r="5"/>
        <circle class="hot-fill" cx="52" cy="52" r="5"/>
        <circle class="hot-fill" cx="68" cy="52" r="5"/>''',
    'deck': '''<rect x="8" y="34" width="78" height="60" rx="8"/>
        <path d="M24 22 H 94 a 8 8 0 0 1 8 8 V 82"/>
        <path d="M22 54 H 66 M22 70 H 52"/>
        <path class="hot" d="M100 14 L 104 26 L 116 30 L 104 34 L 100 46
        L 96 34 L 84 30 L 96 26 Z"/>''',
    'reel': '''<rect x="8" y="26" width="108" height="72" rx="12"/>
        <path class="hot-fill" d="M50 46 L 76 62 L 50 78 Z"/>''',
}


def glyph(name, size):
    return ('<svg class="vb__g" style="width:%dpx;height:%dpx" viewBox="0 0 124 124" '
            'aria-hidden="true">%s</svg>' % (size, size, G[name]))


TPL = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>VSL Funnel Tactics</title>
<link rel="stylesheet" href="../../4pi.css">
<link rel="stylesheet" href="../../voice-quiet.css">
<style>
/* ============================================================================
   See build-thumb-vsl.py. A wider panel: the funnel map across the top, the
   tactics under it, on the same dotted paper as the other boards.

   Class names are prefixed vb; neither shared sheet uses them.
   ========================================================================= */
@page { size: __W__px __H__px; margin: 0; }

.slide {
  position: relative;
  width: __W__px; height: __H__px; padding: 0; background: var(--ground);
  background-image: radial-gradient(#D7DBE2 1.7px, transparent 1.8px);
  background-size: 30px 30px; background-position: 10px 10px;
}

.vb__h {
  position: absolute; left: 40px; top: 42px; width: 1160px; margin: 0;
  font-size: 112px; font-weight: 700; letter-spacing: -0.04em; line-height: 1.02;
  color: var(--ink);
}
.vb__h i { font-style: normal; color: var(--blue); }

/* ---- the board ----------------------------------------------------------- */
.vb { position: absolute; left: 40px; top: 190px; width: __BW__px; height: __BH__px; }

.vb__wires { position: absolute; inset: 0; }
.vb__wires svg { display: block; width: 100%; height: 100%; }
.vb__wires .flow { fill: none; stroke: #AEB8C6; stroke-width: 3;
                   stroke-linecap: round; stroke-dasharray: 9 9; }
.vb__wires .tip { fill: #AEB8C6; }
.vb__ink { z-index: 3; pointer-events: none; }
.vb__ink .ring { fill: none; stroke: var(--red); stroke-width: 3.4; }

.vb__card {
  position: absolute; box-sizing: border-box;
  background: var(--surface); border: 1px solid var(--hairline);
  border-radius: 20px; padding: 17px 20px;
  box-shadow: 0 2px 10px rgba(20, 30, 50, 0.07);
}
.vb__t {
  margin: 0 0 14px;
  font-size: 27px; font-weight: 600; letter-spacing: -0.014em; color: var(--ink);
}
.vb__t i { font-style: normal; color: var(--blue); }

.vb__row { display: flex; align-items: center; gap: 10px; }
.vb__chip {
  padding: 7px 13px; border-radius: 9px;
  background: #E4EFFD; color: #1E4E8C;
  font-size: 19px; font-weight: 600; white-space: nowrap;
}
.vb__chip--off { background: #EDEFF2; color: #6E6E73; }
.vb__chip--g { background: #E7F5E3; color: #3C7F2C; }
.vb__arr { width: 16px; height: 2px; background: #B6C2D0; flex: none; }
.vb__lab { font-size: 18px; font-weight: 600; color: var(--ink-3); white-space: nowrap; }

.vb__g { display: block; fill: none; stroke: #7FA8DC; stroke-width: 3.6;
         stroke-linecap: round; stroke-linejoin: round; }
.vb__g .hot { stroke: var(--blue); stroke-width: 4.4; }
.vb__g .hot-fill { fill: var(--blue); stroke: none; }
.vb__mark { display: block; fill: var(--ink-2); }

/* the funnel map */
.vb__box {
  box-sizing: border-box; padding: 12px 0; width: 170px; text-align: center;
  border: 1px solid var(--hairline); border-radius: 11px; background: var(--surface);
  font-size: 23px; font-weight: 600; color: var(--ink);
}
.vb__box--on { border: 2px solid var(--blue); color: #1E4E8C; background: #F2F7FE; }
.vb__box--off { color: var(--ink-3); }
.vb__pair { display: flex; flex-direction: column; gap: 10px; }
.vb__ev {
  margin: 8px 0 0; text-align: center;
  font-size: 17px; font-weight: 700; letter-spacing: 0.04em;
  text-transform: uppercase; color: var(--blue);
}

/* the length of the VSL, drawn as a scrubber */
.vb__scrub { flex: 1; height: 10px; border-radius: 5px; background: #DDE3EA; }
.vb__scrub span { display: block; width: 34%; height: 10px; border-radius: 5px;
                  background: var(--blue); }
.vb__bang { color: var(--blue); font-size: 34px; font-weight: 700; }
</style>
</head>
<body>

<section class="slide">

  <h1 class="vb__h"><i>VSL</i> Funnel Tactics</h1>

  <div class="vb">

    <div class="vb__wires">
      <svg viewBox="0 0 __BW__ __BH__" aria-hidden="true">
__WIRES__
      </svg>
    </div>

    <div class="vb__wires vb__ink">
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
    cards.append('    <div class="vb__card" style="left:%gpx; top:%gpx; width:%gpx; '
                 'height:%gpx; transform:rotate(%gdeg)">'
                 '<p class="vb__t">%s</p>%s</div>' % (x, y, w, h, rot, title, body))


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


# ---- the funnel, across the top -------------------------------------------
MAP = ('<div class="vb__row" style="gap:14px">'
       '<div class="vb__box">Ads</div><div class="vb__arr"></div>'
       '<div class="vb__box">Opt-in</div><div class="vb__arr"></div>'
       '<div class="vb__box">VSL</div><div class="vb__arr"></div>'
       '<div class="vb__pair">'
       '<div><div class="vb__box vb__box--on">TY A</div>'
       '<p class="vb__ev">Schedule</p></div>'
       '<div class="vb__box vb__box--off">TY B</div></div>'
       '<div class="vb__arr"></div>'
       '<div class="vb__box">Call</div></div>')

# ---- the conversion event --------------------------------------------------
EVENT = ('<div class="vb__row" style="gap:8px">'
         '<span class="vb__chip vb__chip--off">Lead</span>'
         '<div class="vb__arr"></div>'
         '<span class="vb__chip vb__chip--off">View</span>'
         '<div class="vb__arr"></div>'
         '<span class="vb__chip">Schedule</span></div>')

# ---- the length of the VSL -------------------------------------------------
LENGTH = ('<div class="vb__row" style="gap:14px">' + glyph('reel', 52)
          + '<div class="vb__scrub"><span></span></div></div>')

# ---- speed to lead ---------------------------------------------------------
SPEED = ('<div class="vb__row" style="gap:16px">' + glyph('clock', 56)
         + '<span class="vb__bang">!!!</span></div>')

# ---- the offer line --------------------------------------------------------
OFFER = ('<div class="vb__row" style="gap:8px">'
         '<span class="vb__chip">[Result]</span><span class="vb__lab">in</span>'
         '<span class="vb__chip">[Time]</span><span class="vb__lab">without</span>'
         '<span class="vb__chip">[Pain]</span></div>')

# ---- messaging -------------------------------------------------------------
MESSAGING = ('<div class="vb__row" style="gap:8px">'
             '<span class="vb__chip">Hook</span><div class="vb__arr"></div>'
             '<span class="vb__chip">Body</span><div class="vb__arr"></div>'
             '<span class="vb__chip">CTA</span></div>'
             '<div class="vb__row" style="gap:8px; margin-top:14px">'
             '<span class="vb__chip vb__chip--off">Pain</span>'
             '<span class="vb__chip vb__chip--off">Dream</span>'
             '<span class="vb__chip vb__chip--off">Objection</span>'
             '<span class="vb__chip vb__chip--g">Proof</span></div>')

# ---- the pre-call sequence -------------------------------------------------
SEQ = ('<div class="vb__row" style="justify-content:space-between">'
       + glyph('mail', 50) + glyph('sms', 50) + mark('youtube', 50)
       + mark('meta', 42) + glyph('setter', 50) + '</div>'
       '<p class="vb__lab" style="margin:14px 0 0">Emails, SMS, video, ads, setters</p>')

# ---- the decks -------------------------------------------------------------
DECKS = ('<div class="vb__row" style="gap:20px">' + glyph('deck', 64)
         + '<div class="vb__row" style="gap:10px">'
         + ''.join('<span style="display:block; width:52px; height:38px;'
                   ' border-radius:7px; background:%s"></span>' % c
                   for c in ('#CFE2FA', '#CFE2FA', '#E4EFFD'))
         + '</div></div>')

# ---------------------------------------------------------------------------
card(0, 0, 1160, 230, -0.5, 'The <i>funnel</i>', MAP)

card(0, 252, 568, 148, 0.8, 'Conversion <i>event</i>', EVENT)
card(0, 408, 568, 148, -0.9, '3&ndash;5 min <i>VSL</i>', LENGTH)
card(0, 564, 568, 148, 0.6, 'Speed to <i>Lead</i>', SPEED)
card(0, 720, 568, 148, -0.5, '<i>Offer</i> line', OFFER)

card(592, 258, 568, 194, -0.8, '<i>Messaging</i>', MESSAGING)
card(592, 466, 568, 194, 0.9, 'Pre-call <i>nurture</i>', SEQ)
card(592, 674, 568, 194, -0.6, 'AI <i>Pitch Decks</i>', DECKS)

wires = [
    wire(284, 234, 284, 246, 90),
    wire(876, 234, 876, 252, 90),
    wire(284, 402, 284, 403, 90),
    wire(284, 558, 284, 559, 90),
    wire(284, 714, 284, 715, 90),
    wire(876, 456, 876, 460, 90),
    wire(876, 664, 876, 668, 90),
]

# The one red mark, on the event the whole funnel is built to report.
ink = ['<ellipse class="ring" cx="284" cy="335" rx="78" ry="34" '
       'transform="rotate(-2 284 335)"/>']

out = (TPL.replace('__W__', str(W)).replace('__H__', str(H))
          .replace('__BW__', str(BW)).replace('__BH__', str(BH))
          .replace('__WIRES__', '\n'.join('        ' + w for w in wires))
          .replace('__INK__', '\n'.join('        ' + i for i in ink))
          .replace('__CARDS__', '\n'.join(cards)))

path = 'slides/wide/thumb-vsl-board.html'
open(path, 'w').write(out)
print('wrote %s' % path)
