#!/usr/bin/env python3
"""Ten personas, one campaign.

Ten silhouettes rather than three, and no labels on them. They are not a list
to read, they are a quantity to see, so numbering them would invite counting
and reading where the only point is "a lot of different people".

Different means drawn differently, not scaled differently. Each figure gets its
own silhouette (hair, a cap, a bag, a build, a stance) because ten copies of one
outline at ten sizes reads as one person at ten distances.

The crowd sits in two columns offset by half a row, so every line out of the
back column passes through a gap in the front one instead of behind a figure.

    ./build-personas-campaign.py    writes the 16:9 slide
"""
import math
import os
import re

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Shared parts. All figures are solid ink with real gaps left between the arms
# and the torso: overlapped, they merge into one lump and stop reading.
HEAD = '<circle cx="33" cy="16" r="14"/>'
TORSO = ('<path d="M33 34 C 23 34, 17 41, 17 51 L 17 84 C 17 88, 21 90, 25 90 '
         'L 41 90 C 45 90, 49 88, 49 84 L 49 51 C 49 41, 43 34, 33 34 Z"/>')
ARMS = ('<rect x="3" y="46" width="11" height="44" rx="5.5"/>'
        '<rect x="52" y="46" width="11" height="44" rx="5.5"/>')
LEGS = ('<rect x="19" y="88" width="12" height="58" rx="6"/>'
        '<rect x="35" y="88" width="12" height="58" rx="6"/>')

# (width, height, body). Heights vary a little on top of the shape changes,
# because real groups of people are not all one height either.
FIGURES = [
    # plain
    (64, 146, HEAD + TORSO + ARMS + LEGS),
    # long hair: a crown, then two falls past the jaw. A single rounded
    # slab here swallowed the head and read as a hood instead.
    (64, 146, '<path d="M19 20 C 19 8, 26 3, 33 3 C 40 3, 47 8, 47 20 L 50 54 L 41 54 L 41 36 L 25 36 L 25 54 L 16 54 Z"/>'
              + HEAD + TORSO + ARMS + LEGS),
    # hands on hips: the triangle of ground between arm and torso is what makes
    # this one carry at a glance. A cap sat here first and read as a frying pan:
    # a brim long enough to see is longer than a head is wide.
    (64, 146, HEAD + TORSO
     + '<path d="M15 46 L 2 70 L 16 88 L 23 84 L 10 69 L 21 50 Z"/>'
       '<path d="M51 46 L 64 70 L 50 88 L 43 84 L 56 69 L 45 50 Z"/>'
     + LEGS),
    # broader build
    (70, 146, HEAD
     + '<path d="M33 32 C 21 32, 14 40, 14 52 L 14 85 C 14 89, 18 91, 23 91 '
       'L 43 91 C 48 91, 52 89, 52 85 L 52 52 C 52 40, 45 32, 33 32 Z"/>'
     + '<rect x="0" y="45" width="12" height="46" rx="6"/>'
       '<rect x="54" y="45" width="12" height="46" rx="6"/>'
     + '<rect x="17" y="89" width="13" height="57" rx="6.5"/>'
       '<rect x="36" y="89" width="13" height="57" rx="6.5"/>'),
    # a ponytail off the back of the head
    (64, 141, HEAD
     + '<path d="M45 11 C 55 14, 59 26, 54 37 L 46 32 C 50 24, 49 17, 45 11 Z"/>'
     + TORSO + ARMS + LEGS),
    # taller and slimmer: narrower torso, longer legs
    (58, 152, HEAD
     + '<path d="M33 34 C 25 34, 20 41, 20 51 L 20 84 C 20 88, 23 90, 27 90 '
       'L 39 90 C 43 90, 46 88, 46 84 L 46 51 C 46 41, 41 34, 33 34 Z"/>'
     + '<rect x="7" y="46" width="10" height="44" rx="5"/>'
       '<rect x="49" y="46" width="10" height="44" rx="5"/>'
     + '<rect x="21" y="88" width="11" height="60" rx="5.5"/>'
       '<rect x="34" y="88" width="11" height="60" rx="5.5"/>'),
    # a dress: the torso flares instead of splitting at the hip
    (66, 144, HEAD
     + '<path d="M33 34 C 23 34, 17 41, 17 51 L 10 97 L 56 97 L 49 51 '
       'C 49 41, 43 34, 33 34 Z"/>'
     + ARMS
     + '<rect x="21" y="95" width="9" height="51" rx="4.5"/>'
       '<rect x="36" y="95" width="9" height="51" rx="4.5"/>'),
    # a bag on a strap across the body
    (64, 146, HEAD + TORSO
     + '<rect x="40" y="34" width="5" height="40" rx="2.5" '
       'transform="rotate(-24 42.5 34)"/>'
     + '<rect x="46" y="66" width="16" height="21" rx="4"/>'
     + '<rect x="3" y="46" width="11" height="44" rx="5.5"/>' + LEGS),
    # arms folded in front
    (64, 146, HEAD + TORSO
     + '<rect x="4" y="46" width="11" height="26" rx="5.5"/>'
       '<rect x="51" y="46" width="11" height="26" rx="5.5"/>'
       '<rect x="8" y="64" width="50" height="11" rx="5.5"/>'
     + LEGS),
    # shorter, with the legs to match
    (64, 128, HEAD + TORSO + ARMS
     + '<rect x="19" y="88" width="12" height="40" rx="6"/>'
       '<rect x="35" y="88" width="12" height="40" rx="6"/>'),
]

# ---- the stage ------------------------------------------------------------
STAGE_W, STAGE_H = 1700, 900
TIP = (1150, 450)          # where the ten lines meet
COL_X = (0, 196)           # the two columns of the crowd
PITCH = 165                # row to row inside one column
STAGGER = 82               # the back column drops half a row

def layout():
    """Figure boxes and the point each one's line leaves from."""
    out = []
    for i, (w, h, body) in enumerate(FIGURES):
        col, row = i % 2, i // 2
        x = COL_X[col]
        y = row * PITCH + (STAGGER if col else 0)
        out.append(dict(x=x, y=y, w=w, h=h, body=body,
                        sx=x + w + 16, sy=y + h / 2))
    return out


def curve(sx, sy):
    """Leaves horizontally and arrives horizontally, so the fan closes on the
    tip rather than veering into it."""
    dx = TIP[0] - sx
    return ('M%.1f %.1f C %.1f %.1f, %.1f %.1f, %.1f %.1f'
            % (sx, sy, sx + dx * 0.45, sy, TIP[0] - dx * 0.45, TIP[1], *TIP))


FIG = ('    <div class="per" style="left:%dpx; top:%dpx">'
       '<svg width="%d" height="%d" viewBox="0 0 66 150" aria-hidden="true">'
       '%s</svg></div>')

TPL = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Many personas, one campaign</title>
<link rel="stylesheet" href="../../4pi.css">
<link rel="stylesheet" href="../../voice-quiet.css">
<style>
/* ============================================================================
   See build-personas-campaign.py. Ten different silhouettes, no labels, and
   one arrow into the campaign: the crowd is a quantity to see, not a list.
   ========================================================================= */
@page { size: 1920px 1080px; margin: 0; }

.slide { width: 1920px; height: 1080px; padding: 90px 110px; background: var(--ground); }

.fan { position: relative; width: __SW__px; height: __SH__px; }

.per { position: absolute; }
.per svg { display: block; fill: var(--ink); }

/* The routing. Behind everything, so a line that grazes a figure passes under
   it instead of cutting across the silhouette. */
.fan__lines { position: absolute; inset: 0; z-index: 0; }
.fan__lines svg {
  display: block; width: 100%; height: 100%;
  fill: none; stroke: #B6C2D0; stroke-width: 2.6;
  stroke-linecap: round; stroke-linejoin: round;
}
/* The open paths above would otherwise take the default fill and flood. */
.fan__lines svg .tip { fill: #B6C2D0; stroke: none; }

/* ---- the campaign -------------------------------------------------------- */
.fan__camp { position: absolute; left: __BX__px; top: __BY__px; }

/* Its name sits on the border, so the box needs no header row. */
.fan__box {
  border: 3px solid #C6CDD6; border-radius: 30px;
  padding: 62px 70px;
  display: flex; align-items: center; gap: 44px;
}
.fan__name {
  position: absolute; left: 60px; top: 0; transform: translateY(-50%);
  margin: 0; padding: 0 24px; background: var(--ground);
  font-size: 34px; font-weight: 600; letter-spacing: -0.008em; color: var(--ink-2);
}

.fan__box svg {
  display: block; width: 160px; height: 160px;
  fill: none; stroke: var(--blue); stroke-width: 3;
  stroke-linecap: round; stroke-linejoin: round;
}
.fan__box svg .fill { fill: var(--blue); stroke: none; }
</style>
</head>
<body>

<!-- no-autofit: its own canvas, not a panel. -->
<section class="slide slide--center slide--mid">

  <div class="fan">

    <div class="fan__lines">
      <svg viewBox="0 0 __SW__ __SH__" aria-hidden="true">
__PATHS__
        <path d="M__TX__ __TY__ H __SHAFT__"/>
        <path class="tip" d="M__SHAFT__ __TUP__ L __APEX__ __TY__ L __SHAFT__ __TDN__ Z"/>
      </svg>
    </div>

__FIGS__

    <div class="fan__camp">
      <p class="fan__name">Campaign</p>
      <div class="fan__box">
        <svg viewBox="0 0 124 124" aria-hidden="true">
          <rect x="12" y="14" width="100" height="96" rx="11"/>
          <rect x="24" y="26" width="76" height="40" rx="6"/>
          <path class="fill" d="M56 36 L 72 46 L 56 56 Z"/>
          <path d="M24 78 H 92 M24 88 H 72"/>
          <rect class="fill" x="24" y="96" width="40" height="6" rx="3"/>
        </svg>
        <svg viewBox="0 0 124 124" aria-hidden="true">
          <rect x="12" y="14" width="100" height="96" rx="11"/>
          <rect x="24" y="26" width="76" height="40" rx="6"/>
          <path class="fill" d="M56 36 L 72 46 L 56 56 Z"/>
          <path d="M24 78 H 92 M24 88 H 72"/>
          <rect class="fill" x="24" y="96" width="40" height="6" rx="3"/>
        </svg>
      </div>
    </div>

  </div>

</section>

</body>
</html>
'''


def _check_class_collisions():
    """Fail loudly on a name the shared stylesheets already use.

    A local rule only overrides the properties it actually restates, so a
    shared `.seq { height: 522px }` silently clipped an earlier slide even
    though the local rule set position, width and alignment.
    """
    css = open('4pi.css').read() + open('voice-quiet.css').read()
    taken = set(re.findall(r'\.([a-zA-Z][\w-]*)', css))
    mine = set(re.findall(r'^\.([a-zA-Z][\w-]*)', TPL, re.M)) - {'slide'}
    clash = sorted(mine & taken)
    if clash:
        raise SystemExit('class names already used by the shared stylesheets: '
                         + ', '.join(clash))


_check_class_collisions()

crowd = layout()
bottom = max(f['y'] + f['h'] for f in crowd)
assert bottom <= STAGE_H, 'the crowd is %dpx tall, the stage is %d' % (bottom, STAGE_H)

paths = '\n'.join('        <path d="%s"/>' % curve(f['sx'], f['sy'])
                  for f in crowd)
figs = '\n'.join(FIG % (f['x'], f['y'], f['w'], f['h'], f['body']) for f in crowd)

out = TPL
for k, v in (('SW', STAGE_W), ('SH', STAGE_H),
             ('TX', TIP[0]), ('TY', TIP[1]),
             ('SHAFT', TIP[0] + 48), ('APEX', TIP[0] + 84),
             ('TUP', TIP[1] - 17), ('TDN', TIP[1] + 17),
             ('BX', TIP[0] + 112), ('BY', TIP[1] - 149)):
    out = out.replace('__%s__' % k, str(v))
out = out.replace('__PATHS__', paths).replace('__FIGS__', figs)

path = 'slides/wide/wide-personas-one-campaign.html'
open(path, 'w').write(out)
print('wrote %s (crowd %dpx tall)' % (path, bottom))
