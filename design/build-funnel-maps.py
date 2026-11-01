#!/usr/bin/env python3
"""The two funnels, and the one page that reports back.

Both maps run left to right and split at the thank you pages. Only page A
carries the conversion event, so only page A has an arrow going up to the
pixel: the asymmetry is the point, and drawing B identically but without the
arrow says it more plainly than any label could.

The webinar funnel keeps going after the thank you pages, so it does, in
pills at about half the weight of the boxes before them. They are there to
say the funnel continues, not to be read.

    ./build-funnel-maps.py    writes the two 16:9 slides
"""
import os
import re

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def logo(slug):
    src = open('logos/%s.svg' % slug).read()
    box = re.search(r'viewBox="([^"]+)"', src).group(1)
    body = src[src.index('>', src.index('<svg')) + 1:src.rindex('</svg>')]
    return box, re.sub(r'\s*fill="[^"]*"', '', body).strip()


META_BOX, META = logo('meta')

STAGE_W, STAGE_H = 1700, 680


# ------------------------------------------------------------- connectors --
def tip(x, y, a=0):
    """An arrowhead at (x, y) pointing along a degrees."""
    return ('<g transform="translate(%.1f %.1f) rotate(%g)">'
            '<path class="tip" d="M0 0 L -26 -10 L -26 10 Z"/></g>' % (x, y, a))


def straight(x1, x2, y):
    return ('<path class="flow" d="M%.1f %.1f H %.1f"/>' % (x1, y, x2 - 26)
            + tip(x2, y))


def bend(x1, y1, x2, y2):
    """Leaves and arrives horizontally, so the head is level with the box it
    points at however far the branch drops."""
    dx = (x2 - x1) * 0.5
    return ('<path class="flow" d="M%.1f %.1f C %.1f %.1f, %.1f %.1f, %.1f %.1f"/>'
            % (x1, y1, x1 + dx, y1, x2 - dx, y2, x2 - 26, y2) + tip(x2, y2))


def up(x, y1, y2):
    return ('<path class="flow" d="M%.1f %.1f V %.1f"/>' % (x, y1, y2 + 26)
            + tip(x, y2, -90))


# ------------------------------------------------------------------ parts --
def box(x, y, w, h, title, chip='', event='', cls='map__box'):
    c = ('<span class="map__chip">%s</span>' % chip) if chip else ''
    e = ('<p class="map__ev">%s</p>' % event) if event else ''
    return ('<div class="%s" style="left:%gpx; top:%gpx; width:%gpx; height:%gpx">'
            '<p class="map__t">%s</p>%s%s</div>' % (cls, x, y, w, h, title, c, e))


def pill(x, y, w, text):
    return ('<div class="map__pill" style="left:%gpx; top:%gpx; width:%gpx">%s</div>'
            % (x, y, w, text))


def pixel(x, y, w, h):
    return ('<div class="map__pixel" style="left:%gpx; top:%gpx; width:%gpx; height:%gpx">'
            '<svg viewBox="%s" aria-hidden="true">%s</svg>'
            '<p class="map__px">Meta Pixel</p></div>' % (x, y, w, h, META_BOX, META))


TPL = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>__TITLE__</title>
<link rel="stylesheet" href="../../4pi.css">
<link rel="stylesheet" href="../../voice-quiet.css">
<style>
/* ============================================================================
   See build-funnel-maps.py. Left to right, splitting at the thank you pages.
   Only the page with the conversion event has an arrow up to the pixel.

   Class names are prefixed map; neither shared sheet uses them.
   ========================================================================= */
@page { size: 1920px 1080px; margin: 0; }

.slide { width: 1920px; height: 1080px; padding: 90px 110px; background: var(--ground); }

.wrap { width: __SW__px; text-align: left; }
.map__h {
  margin: 0 0 46px;
  font-size: 54px; font-weight: 600; letter-spacing: -0.022em; color: var(--ink);
}

.map { position: relative; width: __SW__px; height: __SH__px; }

/* The connectors, under the boxes so a head stops at an edge rather than on
   top of one. */
.map__wires { position: absolute; inset: 0; }
.map__wires svg { display: block; width: 100%; height: 100%; }
.map__wires .flow { fill: none; stroke: #B6C2D0; stroke-width: 3; stroke-linecap: round; }
.map__wires .tip { fill: #B6C2D0; }

.map__box, .map__won, .map__pixel {
  position: absolute; box-sizing: border-box;
  background: var(--surface); border: 1px solid var(--hairline); border-radius: 20px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04);
  display: flex; flex-direction: column; align-items: center; justify-content: center;
}
.map__t {
  margin: 0; padding: 0 16px; text-align: center;
  font-size: 28px; font-weight: 600; letter-spacing: -0.01em; line-height: 1.18;
  color: var(--ink);
}

/* The page that reports back. The border is the accent, so the arrow leaving
   it has something to leave from. */
.map__won { border: 3px solid var(--blue); }
.map__chip {
  margin: 14px 0 0; padding: 7px 18px; border-radius: 999px;
  background: var(--blue); color: #fff;
  font-size: 21px; font-weight: 600; letter-spacing: -0.004em;
}

.map__pixel svg { display: block; width: 54px; height: 54px; fill: var(--ink); }
.map__px {
  margin: 12px 0 0;
  font-size: 26px; font-weight: 600; letter-spacing: -0.008em; color: var(--ink);
}

/* Which event it is. Under the chip rather than inside it, so the chip stays
   the same label on both funnels and only this line changes. */
.map__ev {
  margin: 10px 0 0;
  font-size: 24px; font-weight: 600; letter-spacing: -0.006em; color: var(--blue);
}

/* The rest of the funnel: present, and plainly not the subject. */
.map__pill {
  position: absolute; box-sizing: border-box; height: 58px;
  display: flex; align-items: center; justify-content: center;
  padding: 0 12px; border-radius: 14px;
  background: #EAEFF5; color: var(--ink-3);
  font-size: 19px; font-weight: 600; letter-spacing: -0.004em; text-align: center;
}
.map__dots {
  position: absolute; display: flex; align-items: center; gap: 10px;
}
.map__dots i { display: block; width: 9px; height: 9px; border-radius: 50%;
               background: #C3CAD4; }

.map__note {
  position: absolute; margin: 0;
  font-size: 24px; font-weight: 600; letter-spacing: -0.006em; color: var(--ink-3);
}
</style>
</head>
<body>

<!-- no-autofit: its own canvas, not a panel. -->
<section class="slide slide--center slide--mid">

  <div class="wrap">
    <h1 class="map__h">__TITLE__</h1>

    <div class="map">

    <div class="map__wires">
      <svg viewBox="0 0 __SW__ __SH__" aria-hidden="true">
__WIRES__
      </svg>
    </div>

__PARTS__

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


def write(slug, title, wires, parts):
    out = (TPL.replace('__SW__', str(STAGE_W)).replace('__SH__', str(STAGE_H))
              .replace('__TITLE__', title)
              .replace('__WIRES__', '\n'.join('        ' + w for w in wires))
              .replace('__PARTS__', '\n'.join('    ' + p for p in parts)))
    path = 'slides/wide/wide-funnel-%s.html' % slug
    open(path, 'w').write(out)
    print('wrote %s' % path)


# ============================================================ the VSL map ==
BH = 150                                  # main box height
MID = 430                                 # the main row's centre line
AY, BY = 300, 590                         # the two thank you pages' centres

mains = [(0, 260, 'Ads'), (380, 260, 'Opt-in Page'), (760, 260, 'VSL Page')]
parts = [box(x, MID - BH / 2, w, BH, t) for x, w, t in mains]
parts += [
    box(1400, AY - 100, 300, 200, 'TY Page A', 'Conversion Event',
        'Schedule', 'map__won'),
    box(1400, BY - 75, 300, 150, 'TY Page B'),
    pixel(1430, 10, 240, 130),
]
wires = [
    straight(260, 380, MID), straight(640, 760, MID),
    bend(1020, MID, 1400, AY), bend(1020, MID, 1400, BY),
    up(1550, AY - 100, 140),
]
parts.append('<p class="map__note" style="left:1140px; top:%dpx">Call</p>' % (AY + 6))
write('vsl', 'VSL Funnel', wires, parts)

# ======================================================== the webinar map ==
mains = [(0, 210, 'Ads'), (268, 210, 'Opt-in Page'), (536, 210, 'VIP Upsell')]
parts = [box(x, MID - BH / 2, w, BH, t) for x, w, t in mains]
parts += [
    box(836, AY - 100, 250, 200, 'TY Page A', 'Conversion Event',
        'Purchase', 'map__won'),
    box(836, BY - 75, 250, 150, 'TY Page B'),
    pixel(846, 10, 230, 130),
]

# The tail. Half the weight of everything before it, and it ends in dots
# rather than a last box, because the list was given as "etc".
TAIL = [(1150, 197, 'Pre Webinar Nurture'), (1377, 136, 'Live Webinar'),
        (1543, 97, 'Pre Call')]
parts += [pill(x, MID - 29, w, t) for x, w, t in TAIL]
parts.append('<div class="map__dots" style="left:%dpx; top:%dpx">'
             '<i></i><i></i><i></i></div>' % (TAIL[-1][0] + TAIL[-1][1] + 16, MID - 4))

wires = [
    straight(210, 268, MID), straight(478, 536, MID),
    bend(746, MID, 836, AY), bend(746, MID, 836, BY),
    up(961, AY - 100, 140),
    bend(1086, AY, 1150, MID), bend(1086, BY, 1150, MID),
    straight(1347, 1377, MID), straight(1513, 1543, MID),
]
write('webinar', 'Webinar Funnel', wires, parts)
