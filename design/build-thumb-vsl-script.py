#!/usr/bin/env python3
"""A thumbnail panel about VSL scripts for high ticket offers.

1240x1080, the same width as the funnel tactics panel, so it drops into the
right of a 16:9 frame and leaves 680px for a head.

The eight beats of the script run down the left as one spine, because the
order is the content. The right holds what the script produced: the conversion
rate, the cost of a call against the ticket, and the length of the video.

    ./build-thumb-vsl-script.py    writes the panel
"""
import os
import re

os.chdir(os.path.dirname(os.path.abspath(__file__)))

W, H = 1240, 1080
BW, BH = 1160, 790

STEPS = ['Offer', 'Proof', 'Soft CTA', 'Current State + Reframe', 'How It Works',
         'What It Costs', "Who It&rsquo;s For", 'CTA']

VIEWS, APPS = 76, 10          # the dot row, in proportion rather than in full

TPL = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>VSL Scripts</title>
<link rel="stylesheet" href="../../4pi.css">
<link rel="stylesheet" href="../../voice-quiet.css">
<style>
/* ============================================================================
   See build-thumb-vsl-script.py. The eight beats down the left as one spine,
   what the script produced down the right, on the same dotted paper as the
   other panels.

   Class names are prefixed vs; neither shared sheet uses them.
   ========================================================================= */
@page { size: __W__px __H__px; margin: 0; }

.slide {
  position: relative;
  width: __W__px; height: __H__px; padding: 0; background: var(--ground);
  background-image: radial-gradient(#D7DBE2 1.7px, transparent 1.8px);
  background-size: 30px 30px; background-position: 10px 10px;
}

.vs__h {
  position: absolute; left: 40px; top: 40px; width: 1160px; margin: 0;
  font-size: 112px; font-weight: 700; letter-spacing: -0.042em; line-height: 1;
  color: var(--ink);
}
.vs__h i {
  display: block; margin-top: 10px;
  font-style: normal; font-size: 58px; letter-spacing: -0.028em; color: var(--blue);
}

/* ---- the board ----------------------------------------------------------- */
.vs { position: absolute; left: 40px; top: 254px; width: __BW__px; height: __BH__px; }

.vs__card {
  position: absolute; box-sizing: border-box;
  background: var(--surface); border: 1px solid var(--hairline);
  border-radius: 20px; padding: 18px 22px;
  box-shadow: 0 2px 10px rgba(20, 30, 50, 0.07);
}
.vs__t {
  margin: 0 0 16px;
  font-size: 28px; font-weight: 600; letter-spacing: -0.014em; color: var(--ink);
}
.vs__t i { font-style: normal; color: var(--blue); }

/* the spine */
.vs__step { display: flex; align-items: center; gap: 18px; }
.vs__step + .vs__step { margin-top: 34px; }
.vs__n {
  flex: none; width: 54px; height: 54px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: 24px; font-weight: 700; color: #fff;
}
.vs__s {
  margin: 0;
  font-size: 33px; font-weight: 600; letter-spacing: -0.016em; color: var(--ink);
}

/* the rate */
.vs__k { margin: 0; font-size: 20px; font-weight: 600; color: var(--ink-3); }
.vs__big {
  margin: 4px 0 0;
  font-size: 96px; font-weight: 700; letter-spacing: -0.044em; line-height: 1;
  color: var(--blue);
}
.vs__big span { font-size: 0.42em; }
.vs__sub { margin: 12px 0 0; font-size: 21px; font-weight: 600; color: var(--ink-2); }
.vs__sub b { color: var(--ink); }
.vs__dots { display: flex; flex-wrap: wrap; gap: 7px; margin-top: 16px; }
.vs__dot { width: 11px; height: 11px; border-radius: 50%; background: #DCE0E6; }
.vs__dot--on { background: var(--blue); }

/* the two figures */
.vs__pair { display: flex; gap: 20px; }
.vs__fig { flex: 1; }
.vs__fig p { margin: 0; }
.vs__fig .k { font-size: 19px; font-weight: 600; color: var(--ink-3); }
.vs__fig .v {
  margin-top: 6px !important;
  font-size: 40px; font-weight: 700; letter-spacing: -0.03em; color: var(--ink);
}

/* the length */
.vs__row { display: flex; align-items: center; gap: 16px; }
.vs__g { display: block; fill: none; stroke: #7FA8DC; stroke-width: 3.6;
         stroke-linecap: round; stroke-linejoin: round; }
.vs__g .f { fill: var(--blue); stroke: none; }
.vs__scrub { flex: 1; height: 10px; border-radius: 5px; background: #DDE3EA; }
.vs__scrub span { display: block; width: 34%; height: 10px; border-radius: 5px;
                  background: var(--blue); }

.vs__ink { position: absolute; inset: 0; z-index: 3; pointer-events: none; }
.vs__ink svg { display: block; width: 100%; height: 100%; }
.vs__ink .ring { fill: none; stroke: var(--red); stroke-width: 3.6; }
</style>
</head>
<body>

<section class="slide">

  <h1 class="vs__h">VSL Scripts<i>(high ticket offers)</i></h1>

  <div class="vs">

__CARDS__

    <div class="vs__ink">
      <svg viewBox="0 0 __BW__ __BH__" aria-hidden="true">
        <ellipse class="ring" cx="790" cy="112" rx="104" ry="54"
                 transform="rotate(-2 790 112)"/>
      </svg>
    </div>

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


def card(x, y, w, h, rot, body):
    cards.append('    <div class="vs__card" style="left:%gpx; top:%gpx; width:%gpx; '
                 'height:%gpx; transform:rotate(%gdeg)">%s</div>'
                 % (x, y, w, h, rot, body))


def ramp(n, a=(0x8F, 0xC0, 0xF5), b=(0x00, 0x71, 0xE3)):
    return ['#%02X%02X%02X' % tuple(round(a[c] + (b[c] - a[c]) * i / (n - 1))
                                    for c in range(3)) for i in range(n)]


RAMP = ramp(len(STEPS))

SPINE = ('<p class="vs__t">The <i>script</i>, in order</p>'
         + ''.join('<div class="vs__step">'
                   '<span class="vs__n" style="background:%s">%d</span>'
                   '<p class="vs__s">%s</p></div>' % (RAMP[i], i + 1, s)
                   for i, s in enumerate(STEPS)))

# every eighth view became an application, give or take, so the row scans
HITS = {2, 9, 17, 24, 31, 39, 46, 54, 61, 69}
DOTS = ''.join('<span class="vs__dot%s"></span>'
               % (' vs__dot--on' if i in HITS else '') for i in range(VIEWS))

RATE = ('<p class="vs__k">VSL conversion rate</p>'
        '<p class="vs__big">13.1<span>%</span></p>'
        '<p class="vs__sub"><b>28</b> applications from <b>214</b> views</p>'
        '<div class="vs__dots">' + DOTS + '</div>')

PAIR = ('<div class="vs__pair">'
        '<div class="vs__fig"><p class="k">Cost per call</p><p class="v">$198.10</p></div>'
        '<div class="vs__fig"><p class="k">Ticket price</p><p class="v">$15,000</p></div>'
        '</div>')

LENGTH = ('<p class="vs__t">3&ndash;5 min <i>VSL</i></p>'
          '<div class="vs__row">'
          '<svg class="vs__g" viewBox="0 0 124 124" style="width:52px;height:52px" '
          'aria-hidden="true"><rect x="8" y="26" width="108" height="72" rx="12"/>'
          '<path class="f" d="M50 46 L 76 62 L 50 78 Z"/></svg>'
          '<div class="vs__scrub"><span></span></div></div>')

card(0, 0, 640, 790, -0.5, SPINE)
card(664, 8, 496, 300, 0.8, RATE)
card(664, 330, 496, 158, -0.9, PAIR)
card(664, 510, 496, 144, 0.7, LENGTH)
card(664, 676, 496, 114, -0.6,
     '<div style="display:flex; align-items:center; height:100%">'
     '<p class="vs__t" style="margin:0">Open Loop &rarr; <i>Proof</i> &rarr; Soft CTA'
     '</p></div>')

out = (TPL.replace('__W__', str(W)).replace('__H__', str(H))
          .replace('__BW__', str(BW)).replace('__BH__', str(BH))
          .replace('__CARDS__', '\n'.join(cards)))

path = 'slides/wide/thumb-vsl-script.html'
open(path, 'w').write(out)
print('wrote %s' % path)
