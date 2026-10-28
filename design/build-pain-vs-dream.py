#!/usr/bin/env python3
"""Two halves: running from pain, walking toward the dream.

Both figures move the same way, left to right. That is what makes the two
halves comparable at all: the difference is not where they are going but what
is moving them, a fire behind pushing one and a butterfly ahead pulling the
other. Mirroring them would have turned it into a picture about direction.

Everything in the top half is off its axis — the house tilts, the debris spins,
the ground is broken, the smoke drifts off the corner. Everything in the bottom
half stands upright on one straight line. The two halves use different colour
too: red and grey above, blue below, so the split reads before any object is
identified.

Limbs are drawn as round-capped strokes rather than filled rounded rectangles.
They come out identical, and a pose is far easier to set from joint positions
than from a rectangle and a rotation about a pivot.

    ./build-pain-vs-dream.py    writes the 16:9 slide
"""
import math
import os
import re

os.chdir(os.path.dirname(os.path.abspath(__file__)))

W, H = 1920, 1080
MID = 540


# ---------------------------------------------------------------- figures --
def limbs(joints, width, cls='ink'):
    """A chain of round-capped segments: joints are the bends."""
    d = 'M%g %g ' % joints[0] + ' '.join('L%g %g' % p for p in joints[1:])
    return ('<path class="%s" d="%s" stroke-width="%g" '
            'stroke-linecap="round" stroke-linejoin="round" fill="none"/>'
            % (cls, d, width))


def runner():
    """Leaning into the run, front arm up, back leg kicked off the ground.

    The trailing arm swings back and UP. Level with the shoulder it ran
    parallel to the trailing leg and the figure read as having three legs.
    """
    return (
        '<circle class="ink-fill" cx="88" cy="22" r="15"/>'
        + limbs([(82, 42), (58, 92)], 32)                     # torso
        + limbs([(80, 48), (106, 36), (113, 13)], 12)         # front arm, up
        + limbs([(78, 50), (54, 40), (32, 27)], 12)           # back arm, up and back
        + limbs([(58, 92), (93, 105), (97, 136)], 14)         # front leg
        + limbs([(58, 92), (31, 115), (9, 103)], 14)          # back leg, trailing
    )


def walker():
    """Upright, mid-stride, arms swinging short. Nothing is urgent.

    The arms sit outside the torso rather than against it. Overlapped they
    merge into one lump and the silhouette stops reading as a person.
    """
    return (
        '<circle class="ink-fill" cx="40" cy="20" r="15"/>'
        + limbs([(40, 38), (40, 92)], 28)                     # torso
        + limbs([(40, 48), (19, 70), (15, 90)], 11)           # back arm
        + limbs([(40, 48), (61, 70), (65, 88)], 11)           # front arm
        + limbs([(40, 92), (53, 118), (58, 146)], 14)         # front leg
        + limbs([(40, 92), (29, 118), (21, 146)], 14)         # back leg
    )


def butterfly(x, y, s, rot=0, cls='blue-fill'):
    """Two wings and a body. Drawn around its own centre so it can be dropped
    anywhere at any angle."""
    wing = ('M0 0 C -7 -21, -29 -26, -33 -11 C -36 -1, -17 5, 0 0 Z'
            'M0 2 C -5 11, -21 19, -27 9 C -31 2, -13 0, 0 2 Z')
    return ('<g transform="translate(%g %g) rotate(%g) scale(%g)">'
            '<path class="%s" d="%s"/>'
            '<g transform="scale(-1 1)"><path class="%s" d="%s"/></g>'
            '<ellipse class="%s" cx="0" cy="0" rx="3.4" ry="12"/>'
            '<path class="%s-line" d="M-2 -10 C -7 -18, -11 -20, -14 -21 '
            'M2 -10 C 7 -18, 11 -20, 14 -21" stroke-width="2.4" '
            'stroke-linecap="round" fill="none"/>'
            '</g>' % (x, y, rot, s, cls, wing, cls, wing, cls,
                      cls.split('-')[0]))


def tree(x, base, s):
    """Trunk and three overlapping puffs, so no two trees are the same lump."""
    return ('<g transform="translate(%g %g) scale(%g)">'
            '<path class="trunk" d="M0 0 V -74" stroke-width="15" '
            'stroke-linecap="round" fill="none"/>'
            '<circle class="leaf" cx="-30" cy="-96" r="36"/>'
            '<circle class="leaf" cx="28" cy="-90" r="32"/>'
            '<circle class="leaf" cx="0" cy="-126" r="42"/>'
            '</g>' % (x, base, s))


def tuft(x, base, s=1):
    return ('<g transform="translate(%g %g) scale(%g)">'
            '<path class="grass" d="M0 0 C -2 -14, -8 -20, -13 -24 '
            'M0 0 C 0 -16, 0 -22, 1 -29 '
            'M0 0 C 2 -14, 8 -19, 13 -23" stroke-width="3.4" '
            'stroke-linecap="round" fill="none"/></g>' % (x, base, s))


def flower(x, base, s=1):
    return ('<g transform="translate(%g %g) scale(%g)">'
            '<path class="grass" d="M0 0 C -1 -16, 1 -24, 0 -34" '
            'stroke-width="3.2" stroke-linecap="round" fill="none"/>'
            '<circle class="leaf" cx="0" cy="-40" r="8"/></g>' % (x, base, s))


def cloud(x, y, s):
    """The calm half's answer to the smoke: same three-puff construction,
    sitting still instead of streaming off the corner."""
    return ('<g transform="translate(%g %g) scale(%g)">'
            '<circle class="hill" cx="0" cy="0" r="34"/>'
            '<circle class="hill" cx="-38" cy="10" r="26"/>'
            '<circle class="hill" cx="36" cy="12" r="24"/>'
            '<rect class="hill" x="-38" y="0" width="76" height="24" rx="12"/>'
            '</g>' % (x, y, s))


def flame(x, y, s, rot=0, cls='fire'):
    return ('<g transform="translate(%g %g) rotate(%g) scale(%g)">'
            '<path class="%s" d="M0 0 C 16 -20, 1 -33, 9 -58 C 30 -40, 40 -16, '
            '26 0 Z"/></g>' % (x, y, rot, s, cls))


# ------------------------------------------------------------------ scene --
# Debris: hand placed rather than random, so it is chaotic but composed.
# (x, y, w, h, angle)
DEBRIS = [
    (486, 196, 54, 72, -34), (604, 322, 42, 58, 62), (560, 120, 38, 50, 18),
    (700, 232, 60, 44, -58), (812, 150, 46, 62, 41), (868, 338, 36, 50, -22),
    (948, 108, 52, 40, 74), (744, 404, 44, 34, 15), (1012, 258, 40, 54, -47),
    (1380, 150, 44, 58, 29), (1486, 300, 36, 48, -63), (1560, 96, 50, 38, 12),
    (1664, 232, 42, 56, -25), (1760, 376, 38, 46, 54),
]

# Long thin pieces and sharp shards, mixed in with the squares.
PLANKS = [
    (540, 262, 118, 18, -28), (760, 112, 96, 16, 52), (1024, 392, 110, 18, 12),
    (1436, 208, 102, 16, -41), (1690, 118, 92, 18, 24), (880, 230, 104, 16, -66),
]
SHARDS = [
    (648, 176, 1.4, 22), (908, 410, 1.1, -48), (1150, 130, 1.3, 64),
    (1536, 386, 1.2, -18), (1778, 268, 1.0, 38), (470, 410, 1.1, -72),
]

# Sparks: short strokes flying off the fire.
SPARKS = [
    (430, 262, 470, 230), (452, 318, 500, 300), (406, 196, 438, 160),
    (470, 372, 512, 362), (390, 140, 408, 104), (502, 238, 546, 214),
]

SMOKE = [(342, 196, 28), (404, 150, 38), (486, 108, 48),
         (596, 70, 58), (730, 38, 68)]

TPL = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Running from pain, walking to the dream</title>
<link rel="stylesheet" href="../../4pi.css">
<link rel="stylesheet" href="../../voice-quiet.css">
<style>
/* ============================================================================
   See build-pain-vs-dream.py. Both figures run the same way across the frame,
   so the only difference left is what is moving them.
   ========================================================================= */
@page { size: __W__px __H__px; margin: 0; }

.slide { width: __W__px; height: __H__px; padding: 0; background: var(--ground); }

.scene { width: __W__px; height: __H__px; }
.scene svg { display: block; width: 100%; height: 100%; }

/* The split itself. */
.scene .split { stroke: #B9C0C9; stroke-width: 3; }

/* ---- people -------------------------------------------------------------- */
.scene .ink { stroke: var(--ink); }
.scene .ink-fill { fill: var(--ink); }

/* ---- the half that is on fire -------------------------------------------- */
.scene .house { stroke: #6E7681; stroke-width: 6; fill: none;
                stroke-linecap: round; stroke-linejoin: round; }
.scene .fire { fill: var(--red); }
.scene .fire-2 { fill: #F2748B; }
.scene .smoke { fill: #C9CFD8; }
.scene .debris { fill: #CBD2DB; }
.scene .spark { stroke: #E8899C; stroke-width: 4; stroke-linecap: round; }
.scene .crack { stroke: #AEB6C1; stroke-width: 4; stroke-linecap: round;
                stroke-linejoin: round; fill: none; }
.scene .dirt { stroke: #9AA3AF; stroke-width: 5; stroke-linecap: round;
               stroke-linejoin: round; fill: none; }

/* ---- the half that is not ------------------------------------------------ */
.scene .turf { stroke: #AEB6C1; stroke-width: 4; stroke-linecap: round; }
.scene .hill { fill: #E6EEF9; }
.scene .trunk { stroke: #9AA3AF; }
.scene .leaf { fill: #C8DEF8; }
.scene .grass { stroke: #9FC0E6; }
.scene .blue-fill { fill: var(--blue); }
.scene .blue-line { stroke: var(--blue); }
.scene .trail { stroke: var(--blue); stroke-width: 4; fill: none;
                stroke-linecap: round; stroke-dasharray: 2 18; opacity: 0.55; }
</style>
</head>
<body>

<!-- no-autofit: its own canvas, not a panel. -->
<section class="slide">
  <div class="scene">
    <svg viewBox="0 0 __W__ __H__" aria-hidden="true">
__BODY__
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

out = []
add = out.append

# =============================================================== top half ==
GROUND_TOP = 492

add('<!-- ---------- the fire ---------- -->')

# Smoke first, so the house sits over it.
for x, y, r in SMOKE:
    add('<g transform="translate(%g %g)"><circle class="smoke" cx="0" cy="0" r="%g"/>'
        '<circle class="smoke" cx="%g" cy="%g" r="%g"/>'
        '<circle class="smoke" cx="%g" cy="%g" r="%g"/></g>'
        % (x, y, r, -r * 0.7, r * 0.3, r * 0.72, r * 0.75, r * 0.24, r * 0.66))

# The house, tilted. Nothing in this half stands straight, and the tilt lifts
# the far corner so it reads as going over rather than as a crooked drawing.
add('<g transform="rotate(-4 300 420)">'
    '<path class="house" d="M186 330 V 486 H 420 V 330"/>'
    '<path class="house" d="M156 338 L 303 232 L 450 338"/>'
    '<path class="house" d="M288 486 V 406 H 346 V 486"/>'
    '<path class="house" d="M214 356 H 260 V 398 H 214 Z"/>'
    '</g>')

for x, y, s_, rot in ((244, 250, 2.2, -10), (300, 238, 2.7, 4), (364, 268, 1.7, 18)):
    add(flame(x, y, s_, rot))
for x, y, s_, rot in ((276, 232, 1.5, 0), (336, 250, 1.3, 12)):
    add(flame(x, y, s_, rot, 'fire-2'))
add(flame(224, 396, 1.1, -14, 'fire-2'))   # out of the window

for x1, y1, x2, y2 in SPARKS:
    add('<path class="spark" d="M%g %g L %g %g"/>' % (x1, y1, x2, y2))

add('<!-- ---------- what the blast threw ---------- -->')
for x, y, w_, h_, a in DEBRIS:
    add('<rect class="debris" x="%g" y="%g" width="%g" height="%g" rx="5" '
        'transform="rotate(%g %g %g)"/>'
        % (x, y, w_, h_, a, x + w_ / 2, y + h_ / 2))
# Planks and shards, because a sky of identical squares is tidy, not chaotic.
for x, y, w_, h_, a in PLANKS:
    add('<rect class="debris" x="%g" y="%g" width="%g" height="%g" rx="4" '
        'transform="rotate(%g %g %g)"/>'
        % (x, y, w_, h_, a, x + w_ / 2, y + h_ / 2))
for x, y, s_, a in SHARDS:
    add('<g transform="translate(%g %g) rotate(%g) scale(%g)">'
        '<path class="debris" d="M0 0 L 34 10 L 12 32 Z"/></g>' % (x, y, a, s_))

# Broken ground: the line itself is in pieces, and the splits notch upward so
# nothing dangles into the gap above the divider.
add('<path class="dirt" d="M0 %d H 300 M344 %d L 520 %d M566 %d H 884 '
    'M930 %d L 1180 %d M1232 %d H 1520 M1566 %d L 1920 %d"/>'
    % (GROUND_TOP, GROUND_TOP - 5, GROUND_TOP + 4, GROUND_TOP,
       GROUND_TOP + 6, GROUND_TOP - 3, GROUND_TOP + 2, GROUND_TOP - 6,
       GROUND_TOP + 4))
add('<path class="crack" d="M612 %d L 636 %d L 620 %d M1040 %d L 1016 %d '
    'L 1042 %d M1420 %d L 1400 %d"/>'
    % (GROUND_TOP - 2, GROUND_TOP - 34, GROUND_TOP - 62,
       GROUND_TOP - 4, GROUND_TOP - 30, GROUND_TOP - 58,
       GROUND_TOP - 2, GROUND_TOP - 40))

add('<!-- ---------- the runner ---------- -->')
add('<g transform="translate(1066 206) scale(2.1)">%s</g>' % runner())

# ============================================================ the division ==
add('<path class="split" d="M0 %d H %d"/>' % (MID, W))

# ============================================================ bottom half ==
add('<!-- ---------- the sky ---------- -->')
add('<circle class="hill" cx="236" cy="668" r="62"/>')
add(cloud(470, 672, 1.0))
add(cloud(846, 636, 0.78))

add('<!-- ---------- the field ---------- -->')
add('<path class="hill" d="M0 1010 C 180 930, 420 946, 620 1010 Z"/>')
add('<path class="hill" d="M520 1010 C 700 952, 860 964, 980 1010 Z"/>')

for x, base, s_ in ((1546, 1010, 1.0), (1700, 1010, 0.82), (1826, 1010, 1.06)):
    add(tree(x, base, s_))
add(tree(286, 1010, 0.62))
add(tree(690, 1010, 0.46))

# One straight line, unbroken, as against the one above.
add('<path class="turf" d="M0 1010 H %d"/>' % W)

for x, s_ in ((120, 1), (402, 0.9), (640, 1.1), (900, 0.95), (1040, 1.05),
              (1420, 1.1), (1500, 0.9), (1648, 1.05), (1792, 0.95), (1896, 1.1)):
    add(tuft(x, 1010, s_))
for x, s_ in ((1470, 1.0), (1620, 0.85), (1770, 1.05), (1884, 0.9), (960, 0.8)):
    add(flower(x, 1010, s_))

add('<!-- ---------- the walker, and the one leading him ---------- -->')
add('<g transform="translate(1118 701) scale(2.1)">%s</g>' % walker())

# Two dashes with the butterfly between them: where it has come from, and
# where it is taking him. One continuous S read as a loop over his head.
add('<path class="trail" d="M1268 828 C 1318 792, 1362 786, 1404 804"/>')
add('<path class="trail" d="M1452 800 C 1512 776, 1562 788, 1618 762"/>')
add(butterfly(1428, 802, 1.5, -12))

for x, y, s_, rot in ((1548, 764, 0.78, 14), (1676, 700, 0.62, -20),
                      (1820, 788, 0.7, 8), (1612, 880, 0.55, -6),
                      (1762, 902, 0.5, 22), (1884, 690, 0.58, -14)):
    add(butterfly(x, y, s_, rot))

body = '\n'.join('      ' + line for line in out)
html = TPL.replace('__W__', str(W)).replace('__H__', str(H)).replace('__BODY__', body)

path = 'slides/wide/wide-pain-vs-dream.html'
open(path, 'w').write(html)
print('wrote %s' % path)
