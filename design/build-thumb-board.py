#!/usr/bin/env python3
"""The thumbnail panel, as a board rather than a list.

Cards pinned at slight angles on dotted paper, joined by connectors that trace
the order one to five. The point is the impression before the reading: it
should look like a lot of ground covered, and only the headline has to survive
being shrunk to a third of this.

Every card holds a real piece of the deck, drawn small. Lorem shapes would
read as filler the moment anyone paused the video.

    ./build-thumb-board.py    writes the panel
"""
import os
import re

os.chdir(os.path.dirname(os.path.abspath(__file__)))

W, H = 960, 1080


def logo(slug):
    src = open('logos/%s.svg' % slug).read()
    box = re.search(r'viewBox="([^"]+)"', src).group(1)
    body = src[src.index('>', src.index('<svg')) + 1:src.rindex('</svg>')]
    return box, re.sub(r'\s*fill="[^"]*"', '', body).strip()


MARKS = {s: logo(s) for s in ('fathom', 'reddit', 'youtube', 'meta')}


def mark(slug, size):
    box, body = MARKS[slug]
    return ('<svg class="bd__mark" style="width:%dpx;height:%dpx" viewBox="%s" '
            'aria-hidden="true">%s</svg>' % (size, size, box, body))


# Drawn glyphs, same vocabulary as the nurture assets.
GLYPHS = {
    'mail': '''<rect x="30" y="24" width="64" height="42" rx="6"/>
        <rect x="16" y="44" width="80" height="56" rx="7"/>
        <path class="hot" d="M22 51 L56 77 L90 51"/>''',
    'sms': '''<rect x="8" y="26" width="88" height="52" rx="12"/>
        <path d="M34 78 L34 96 L54 78"/>
        <circle class="hot-fill" cx="36" cy="52" r="5"/>
        <circle class="hot-fill" cx="52" cy="52" r="5"/>
        <circle class="hot-fill" cx="68" cy="52" r="5"/>''',
    'setter': '''<path d="M24 102 C 24 82, 41 72, 62 72 C 83 72, 100 82, 100 102"/>
        <circle cx="62" cy="46" r="17"/>
        <path class="hot" d="M42 46 a 20 20 0 0 1 40 0"/>
        <rect class="hot-fill" x="38" y="44" width="9" height="18" rx="4.5"/>
        <rect class="hot-fill" x="77" y="44" width="9" height="18" rx="4.5"/>''',
}


def glyph(name, size):
    return ('<svg class="bd__g" style="width:%dpx;height:%dpx" viewBox="0 0 124 124" '
            'aria-hidden="true">%s</svg>' % (size, size, GLYPHS[name]))


TPL = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Scale Info to $100k/mo</title>
<link rel="stylesheet" href="../../4pi.css">
<link rel="stylesheet" href="../../voice-quiet.css">
<style>
/* ============================================================================
   See build-thumb-board.py. A board, not a list: cards pinned at slight angles
   on dotted paper, connectors tracing one to five.

   Class names are prefixed bd; neither shared sheet uses them.
   ========================================================================= */
@page { size: __W__px __H__px; margin: 0; }

/* Dotted paper, the way the roughs this came from are drawn. */
.slide {
  width: __W__px; height: __H__px; padding: 0; background: var(--ground);
  background-image: radial-gradient(#D7DBE2 1.7px, transparent 1.8px);
  background-size: 30px 30px; background-position: 10px 10px;
}

/* ---- the headline -------------------------------------------------------- */
.bd__h {
  position: absolute; left: 44px; top: 40px; width: 880px; margin: 0;
  font-size: 70px; font-weight: 700; letter-spacing: -0.036em; line-height: 1.04;
  color: var(--ink);
}
.bd__sum {
  color: var(--blue);
  background: linear-gradient(to top, #C6DDFA 0 0.17em, transparent 0.17em);
}
/* The channel is part of the headline now, same size, in the accent. The
   break falls after the figure so the long line runs the full width of the
   panel rather than stopping halfway across it. */
.bd__chan { color: var(--blue); }

/* ---- the board ----------------------------------------------------------- */
.bd { position: absolute; left: 40px; top: 252px; width: 880px; height: 700px; }

.bd__wires { position: absolute; inset: 0; }
/* Over the cards: a ring drawn under them is a ring behind a card. */
.bd__ink { z-index: 3; pointer-events: none; }
.bd__wires svg { display: block; width: 100%; height: 100%; }
.bd__wires .flow { fill: none; stroke: #AEB8C6; stroke-width: 3;
                   stroke-linecap: round; stroke-dasharray: 9 9; }
.bd__wires .tip { fill: #AEB8C6; }
.bd__wires .ring { fill: none; stroke: var(--red); stroke-width: 3.4; }

.bd__card {
  position: absolute; box-sizing: border-box;
  background: var(--surface); border: 1px solid var(--hairline);
  border-radius: 20px; padding: 18px 20px;
  box-shadow: 0 2px 10px rgba(20, 30, 50, 0.07);
}

.bd__head { display: flex; align-items: center; gap: 12px; margin-bottom: 14px; }
.bd__n {
  flex: none; width: 36px; height: 36px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: 19px; font-weight: 700; color: #fff;
}
.bd__t {
  margin: 0;
  font-size: 29px; font-weight: 600; letter-spacing: -0.014em; color: var(--ink);
}

.bd__row { display: flex; align-items: center; gap: 10px; }
.bd__mark { display: block; fill: var(--ink); }
.bd__g {
  display: block; fill: none; stroke: #7FA8DC; stroke-width: 3.4;
  stroke-linecap: round; stroke-linejoin: round;
}
.bd__g .hot { stroke: var(--blue); stroke-width: 4.4; }
.bd__g .hot-fill { fill: var(--blue); stroke: none; }

.bd__chip {
  padding: 6px 12px; border-radius: 9px;
  background: #E4EFFD; color: #1E4E8C;
  font-size: 17px; font-weight: 600; white-space: nowrap;
}
.bd__cap {
  margin: 6px 0 0; text-align: center;
  font-size: 15px; font-weight: 600; color: var(--ink-3);
}

/* mini tiers */
.bd__tier {
  flex: 1; text-align: center; padding: 10px 0; border-radius: 12px;
  border: 1px solid var(--hairline);
  font-size: 20px; font-weight: 700; color: var(--ink);
}
.bd__tier span { display: block; font-size: 14px; font-weight: 600; color: var(--ink-3); }
.bd__tier--main { border: 2px solid var(--blue); color: var(--blue); }

/* mini funnel */
.bd__box {
  box-sizing: border-box; padding: 7px 0; width: 74px; text-align: center;
  border: 1px solid var(--hairline); border-radius: 9px; background: var(--surface);
  font-size: 15px; font-weight: 600; color: var(--ink);
}
.bd__arr { width: 16px; height: 2px; background: #B6C2D0; flex: none; }
.bd__pair { display: flex; flex-direction: column; gap: 7px; }

/* mini campaign */
.bd__camp { background: #E4EFFD; border-radius: 14px; padding: 12px; }
.bd__camp p { margin: 0 0 10px; text-align: center;
              font-size: 16px; font-weight: 600; color: #1E4E8C; }
.bd__ads { display: grid; grid-template-columns: repeat(4, 48px);
           gap: 12px; justify-content: center; }
.bd__ad { width: 48px; height: 48px; border-radius: 50%; background: var(--surface); }
.bd__ad--open { background: none; border: 2px dashed #BFD6F7; }

/* the sticky */
.bd__note {
  position: absolute; box-sizing: border-box;
  background: #DCE9FB; border-radius: 16px; padding: 18px 20px;
  box-shadow: 0 2px 10px rgba(20, 30, 50, 0.08);
  font-size: 31px; font-weight: 700; letter-spacing: -0.016em; color: #11467F;
  line-height: 1.12;
}
.bd__note b { color: var(--blue); }
</style>
</head>
<body>

<section class="slide">

  <h1 class="bd__h">Scale Info to <span class="bd__sum">$100k/mo</span><br>
    <span class="bd__chan">(Meta Ads)</span></h1>

  <div class="bd">

    <div class="bd__wires">
      <svg viewBox="0 0 880 700" aria-hidden="true">
__WIRES__
      </svg>
    </div>

    <div class="bd__wires bd__ink">
      <svg viewBox="0 0 880 700" aria-hidden="true">
        <ellipse class="ring" cx="570" cy="118" rx="78" ry="44"
                 transform="rotate(-4 570 118)"/>
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


def card(x, y, w, h, rot, n, chip, title, body):
    return ('<div class="bd__card" style="left:%gpx; top:%gpx; width:%gpx; '
            'height:%gpx; transform:rotate(%gdeg)">'
            '<div class="bd__head"><span class="bd__n" style="background:%s">%s</span>'
            '<p class="bd__t">%s</p></div>%s</div>' % (x, y, w, h, rot, chip, n, title, body))


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


# ---------------------------------------------------------------- the cards --
cards = []

# 1 — where the research comes from
cards.append(card(0, 0, 330, 176, -1.6, '1', '#7CB2F3', 'ICP Analysis',
                  '<div class="bd__row" style="gap:22px; justify-content:center">'
                  + ''.join('<div>%s</div>' % mark(s, 34)
                            for s in ('fathom', 'reddit', 'youtube'))
                  + '</div>'
                  '<div class="bd__row" style="margin-top:14px; justify-content:center">'
                  '<span class="bd__chip">ICP 1 &amp; ICP 2</span>'
                  '<span class="bd__chip">Pain vs Dream</span></div>'))

# 2 — the three tiers, middle one carrying it
cards.append(card(380, 10, 390, 162, 1.3, '2', '#5BA1F0', 'Offer',
                  '<div class="bd__row" style="gap:10px">'
                  '<div class="bd__tier">DIY<span>3&ndash;7.5k</span></div>'
                  '<div class="bd__tier bd__tier--main">DWY<span>7.5k&ndash;15k</span></div>'
                  '<div class="bd__tier">DFY<span>25&ndash;30k+</span></div>'
                  '</div>'))

# 3 — the funnel, splitting at the thank you pages
cards.append(card(0, 228, 440, 190, -0.9, '3', '#3C8FEC', 'Funnel',
                  '<div class="bd__row">'
                  '<div class="bd__box">Ads</div><div class="bd__arr"></div>'
                  '<div class="bd__box">Opt-in</div><div class="bd__arr"></div>'
                  '<div class="bd__box">VSL</div><div class="bd__arr"></div>'
                  '<div class="bd__pair"><div class="bd__box">TY A</div>'
                  '<div class="bd__box">TY B</div></div>'
                  '</div>'
                  '<div class="bd__row" style="margin-top:12px">'
                  '<span class="bd__chip">VSL vs Webinar</span>'
                  '<span class="bd__chip">Pixel Conditioning</span></div>'))

# 4 — the campaign itself
cards.append(card(492, 212, 388, 286, 1.1, '4', '#1E7DE8', 'Meta Ads',
                  '<div class="bd__camp"><p>1 CBO &middot; 1 Control Ad Set</p>'
                  '<div class="bd__ads">'
                  + '<div class="bd__ad"></div>' * 5
                  + '<div class="bd__ad bd__ad--open"></div>' * 3
                  + '</div></div>'
                  '<div class="bd__row" style="margin-top:12px; justify-content:space-between">'
                  '<span class="bd__chip">3 Creatives per Ad</span>'
                  + mark('meta', 28) + '</div>'))

# 5 — what happens after the call is booked
cards.append(card(0, 466, 430, 172, 0.8, '5', '#0071E3', 'Sales &amp; Ops',
                  '<div class="bd__row" style="justify-content:space-around">'
                  + ''.join('<div><div style="display:flex;justify-content:center">%s</div>'
                            '<p class="bd__cap">%s</p></div>' % (glyph(g, 54), c)
                            for g, c in (('mail', 'Pre Call'), ('sms', 'SMS'),
                                         ('setter', 'Setters')))
                  + '</div>'))

cards.append('<div class="bd__note" style="left:488px; top:548px; width:300px; '
             'transform:rotate(-3.4deg)">Speed to Lead<b>!!!</b></div>')

# --------------------------------------------------------------- the wires --
wires = [
    wire(332, 80, 378, 86),            # 1 -> 2
    wire(560, 176, 300, 226, -90),     # 2 -> 3
    wire(442, 330, 488, 320),          # 3 -> 4
    wire(540, 514, 300, 464, 90),      # 4 -> 5
]

out = (TPL.replace('__W__', str(W)).replace('__H__', str(H))
          .replace('__WIRES__', '\n'.join('        ' + w for w in wires))
          .replace('__CARDS__', '\n'.join('    ' + c for c in cards)))

path = 'slides/wide/thumb-board.html'
open(path, 'w').write(out)
print('wrote %s' % path)
