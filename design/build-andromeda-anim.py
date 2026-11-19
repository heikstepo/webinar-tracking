#!/usr/bin/env python3
"""The Andromeda retrieval layer, built as an animation.

Three beats, left to right: every eligible ad, the handful retrieval keeps,
and the people those are matched to. The colour coding of the reference is
kept as an idea but done in our one accent: the tints are steps of the blue
ramp rather than four unrelated hues.

The slide exposes render(t), so animate.py can drive it frame by frame:

    ./build-andromeda-anim.py
    python3 animate.py slides/andromeda-retrieval.html exports/andromeda.mp4 8.4 30
"""
import math
import os
import re

os.chdir(os.path.dirname(os.path.abspath(__file__)))

W, H = 1440, 810

src = open('logos/meta.svg').read()
META_BOX = re.search(r'viewBox="([^"]+)"', src).group(1)
META = re.sub(r'\s*fill="[^"]*"', '',
              src[src.index('>', src.index('<svg')) + 1:src.rindex('</svg>')]).strip()


def meta(size, cls):
    return ('<svg class="%s" viewBox="%s" style="width:%gpx;height:%gpx" '
            'aria-hidden="true">%s</svg>' % (cls, META_BOX, size, size, META))


# ---- the pile: every eligible ad ------------------------------------------
PILE = []
for r in range(5):
    for c in range(5):
        if r == 4 and c in (2, 4):       # a ragged bottom edge reads as a heap
            continue
        x = 108 + c * 58 + ((r % 2) * 14) + ((c * 7 + r * 11) % 9) - 4
        y = 232 + r * 62 + ((c * 13 + r * 5) % 11) - 5
        rot = ((c * 5 + r * 3) % 13) - 6
        PILE.append((x, y, rot))

# ---- the grid: what retrieval keeps ---------------------------------------
TINTS = ['#E4EFFD', '#CFE2FA', '#A7CCF7', '#7CB2F3']
GX, GY, GT, GG = 528, 252, 72, 18
# the rightmost column is the three that get matched, so the lines run clean
MATCH = {3: 0, 7: 1, 11: 2}
PEOPLE_TINT = ['#CFE2FA', '#A7CCF7', '#7CB2F3']

GRID = []
for i in range(16):
    r, c = divmod(i, 4)
    tint = PEOPLE_TINT[MATCH[i]] if i in MATCH else TINTS[(i * 5 + r) % 4]
    GRID.append((GX + c * (GT + GG), GY + r * (GT + GG), tint))

# ---- the people ------------------------------------------------------------
PX, PW, PH = 1062, 170, 136
PY = [238, 384, 530]

PILE_HTML = '\n'.join(
    '      <div class="tile" id="p%d" style="left:%gpx; top:%gpx; '
    '--rot:%gdeg">%s</div>' % (i, x, y, rot, meta(30, 'mk'))
    for i, (x, y, rot) in enumerate(PILE))

GRID_HTML = '\n'.join(
    '      <div class="gtile" id="g%d" style="left:%gpx; top:%gpx; background:%s">%s'
    '</div>' % (i, x, y, tint, meta(34, 'mk mk--deep'))
    for i, (x, y, tint) in enumerate(GRID))

PEOPLE_HTML = '\n'.join(
    '''      <div class="pc" id="c%d" style="left:%gpx; top:%gpx">
        <div class="pc__top" style="background:%s">
          <svg class="pc__g" viewBox="0 0 124 124" aria-hidden="true">
            <circle cx="62" cy="40" r="20"/>
            <path d="M22 108 C 22 80, 40 66, 62 66 C 84 66, 104 80, 104 108"/>
          </svg>
        </div>
        <div class="pc__rows">%s</div>
      </div>''' % (j, PX, PY[j], PEOPLE_TINT[j],
                   ''.join('<span class="pc__bar" style="width:%d%%"></span>' % w
                           for w in (86, 62, 74)))
    for j in range(3))

# ---- the lines -------------------------------------------------------------
def curve(x1, y1, x2, y2, lift):
    mx = (x1 + x2) / 2
    return 'M%g %g C %g %g, %g %g, %g %g' % (x1, y1, mx, y1 - lift, mx, y2 - lift,
                                             x2, y2)


ARR1 = curve(398, 430, 508, 404, 36)
ARR2 = curve(892, 404, 1046, 440, 34)
MATCH_PATHS = [
    (curve(GX + 3 * (GT + GG) + GT + 8, GY + r * (GT + GG) + GT / 2,
           PX - 10, PY[j] + PH / 2, 14), PEOPLE_TINT[j])
    for i, j in MATCH.items() for r in [i // 4]
]

TPL = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Andromeda Retrieval Layer</title>
<link rel="stylesheet" href="../4pi.css">
<link rel="stylesheet" href="../voice-quiet.css">
<style>
/* ============================================================================
   See build-andromeda-anim.py. Three beats left to right: every eligible ad,
   what retrieval keeps, who it is matched to.

   The reference colour codes the middle grid in four hues; here the tints are
   steps of our one blue, which keeps the idea (these are not all the same ad)
   without borrowing a palette.

   As everywhere else here: no CSS transitions, every value computed from t.
   ========================================================================= */

.stage { position: relative; width: 1440px; height: 810px; flex: none; }

#ttl {
  position: absolute; left: 0; top: 44px; width: 1440px; margin: 0;
  text-align: center;
  font-size: 50px; font-weight: 600; letter-spacing: -0.024em; color: var(--ink);
}

.lbl {
  position: absolute; top: 706px; margin: 0; text-align: center;
  font-size: 25px; font-weight: 600; letter-spacing: -0.01em; color: var(--ink-2);
}
#l1 { left: 60px; width: 380px; }
#l2 { left: 508px; width: 382px; }
#l3 { left: 1000px; width: 300px; }

/* ---- every eligible ad ---------------------------------------------------- */
.tile {
  position: absolute; width: 60px; height: 60px; border-radius: 12px;
  background: var(--surface); border: 1px solid var(--hairline);
  box-shadow: 0 2px 8px rgba(20, 30, 50, 0.07);
  display: flex; align-items: center; justify-content: center;
}
.mk { display: block; fill: var(--blue); }

/* ---- what retrieval keeps -------------------------------------------------- */
.gtile {
  position: absolute; width: 72px; height: 72px; border-radius: 14px;
  display: flex; align-items: center; justify-content: center;
}
.mk--deep { fill: #11467F; }

/* ---- who it is matched to -------------------------------------------------- */
.pc {
  position: absolute; width: 170px; height: 136px; border-radius: 16px;
  background: var(--surface); border: 1px solid var(--hairline);
  box-shadow: 0 3px 14px rgba(20, 30, 50, 0.08); overflow: hidden;
}
.pc__top { height: 74px; display: flex; align-items: center; justify-content: center; }
.pc__g { width: 46px; height: 46px; fill: none; stroke: #11467F; stroke-width: 5;
         stroke-linecap: round; stroke-linejoin: round; }
.pc__rows { padding: 13px 16px 0; }
.pc__bar { display: block; height: 7px; border-radius: 4px; background: #DCE0E6; }
.pc__bar + .pc__bar { margin-top: 8px; }

/* ---- the lines ------------------------------------------------------------- */
.wires { position: absolute; inset: 0; }
.wires svg { display: block; width: 100%; height: 100%; }
.wires .arr { fill: none; stroke: #AEB8C6; stroke-width: 4; stroke-linecap: round; }
.wires .tip { fill: #AEB8C6; }
.wires .match { fill: none; stroke-width: 4; stroke-linecap: round; }
</style>
</head>
<body>

<section class="slide slide--center slide--mid">

  <div class="stage">

    <h2 id="ttl">Andromeda Retrieval Layer</h2>

    <div class="wires">
      <svg viewBox="0 0 1440 810" aria-hidden="true">
        <path class="arr" id="a1" d="__ARR1__"/>
        <g id="a1t" transform="translate(508 404) rotate(-14)">
          <path class="tip" d="M0 0 L -18 -8 L -18 8 Z"/></g>
        <path class="arr" id="a2" d="__ARR2__"/>
        <g id="a2t" transform="translate(1046 440) rotate(16)">
          <path class="tip" d="M0 0 L -18 -8 L -18 8 Z"/></g>
__MATCH__
      </svg>
    </div>

__PILE__

__GRID__

__PEOPLE__

    <p class="lbl" id="l1">All Eligible Ads</p>
    <p class="lbl" id="l2">Retrieval Layer</p>
    <p class="lbl" id="l3">Matched to Real People</p>

  </div>

</section>

<script>
function $(id) { return document.getElementById(id); }
function clamp(u) { return u < 0 ? 0 : u > 1 ? 1 : u; }
function ramp(t, a, b) { return clamp((t - a) / (b - a)); }
function ease(u) { return u * u * (3 - 2 * u); }
function pop(u) { return u >= 1 ? 1 : 1 - Math.pow(2, -10 * u) * Math.cos(u * 14); }

var ttl = $('ttl'), l1 = $('l1'), l2 = $('l2'), l3 = $('l3'),
    a1 = $('a1'), a1t = $('a1t'), a2 = $('a2'), a2t = $('a2t');

var PILE = __NPILE__, GRID = __NGRID__;
var pile = [], grid = [], people = [], matches = [];
for (var i = 0; i < PILE; i++) pile.push($('p' + i));
for (var i = 0; i < GRID; i++) grid.push($('g' + i));
for (var j = 0; j < 3; j++) { people.push($('c' + j)); matches.push($('m' + j)); }

var MATCHED = __MATCHED__;      // grid index -> person

// Dash every drawn line so it can be drawn on rather than faded in.
[a1, a2].concat(matches).forEach(function (p) {
  var len = p.getTotalLength();
  p.style.strokeDasharray = len; p.dataset.len = len;
});

function draw(p, u) {
  p.style.strokeDashoffset = p.dataset.len * (1 - u);
  p.style.opacity = u > 0 ? 1 : 0;
}

function render(t) {
  var u, i, j;

  u = ease(ramp(t, 0.00, 0.50));
  ttl.style.opacity = u;
  ttl.style.transform = 'translateY(' + (16 * (1 - u)) + 'px)';

  // The heap lands a tile at a time, fast, so it reads as a lot of them.
  for (i = 0; i < pile.length; i++) {
    var a = 0.55 + i * 0.034;
    var pu = pop(ramp(t, a, a + 0.40));
    pile[i].style.opacity = clamp(ramp(t, a, a + 0.16));
    pile[i].style.transform = 'rotate(var(--rot)) scale(' + (0.6 + 0.4 * pu) + ')';
  }

  u = ease(ramp(t, 1.75, 2.15));
  l1.style.opacity = u; l1.style.transform = 'translateY(' + (10 * (1 - u)) + 'px)';

  u = ease(ramp(t, 2.10, 2.60));
  draw(a1, u); a1t.style.opacity = u > 0.92 ? 1 : 0;

  // Each kept ad arrives from the heap, so retrieval looks like a lift rather
  // than a second pile appearing beside the first.
  for (i = 0; i < grid.length; i++) {
    var b = 2.45 + i * 0.045;
    var gu = ease(ramp(t, b, b + 0.46));
    var dim = MATCHED[i] === undefined
            ? 1 - 0.62 * ease(ramp(t, 5.90, 6.50)) : 1;
    grid[i].style.opacity = gu * dim;
    grid[i].style.transform = 'translate(' + (-150 * (1 - gu)) + 'px,'
                            + (16 * (1 - gu)) + 'px) scale(' + (0.7 + 0.3 * gu) + ')';
  }

  u = ease(ramp(t, 3.45, 3.85));
  l2.style.opacity = u; l2.style.transform = 'translateY(' + (10 * (1 - u)) + 'px)';

  u = ease(ramp(t, 3.90, 4.40));
  draw(a2, u); a2t.style.opacity = u > 0.92 ? 1 : 0;
  // The big arrow hands over to the three matched lines, so they are never
  // both on the board saying the same thing.
  var fade = 1 - ease(ramp(t, 5.85, 6.25));
  a2.style.opacity = u * fade; a2t.style.opacity = (u > 0.92 ? 1 : 0) * fade;

  for (j = 0; j < 3; j++) {
    var c = 4.30 + j * 0.26;
    var cu = pop(ramp(t, c, c + 0.52));
    people[j].style.opacity = clamp(ramp(t, c, c + 0.20));
    people[j].style.transform = 'translateX(' + (26 * (1 - cu)) + 'px) scale('
                              + (0.84 + 0.16 * cu) + ')';
  }

  u = ease(ramp(t, 5.30, 5.70));
  l3.style.opacity = u; l3.style.transform = 'translateY(' + (10 * (1 - u)) + 'px)';

  for (j = 0; j < 3; j++) draw(matches[j], ease(ramp(t, 5.95 + j * 0.16, 6.75 + j * 0.16)));

  // The three that matched sit up once their line lands.
  for (i = 0; i < grid.length; i++) {
    if (MATCHED[i] === undefined) continue;
    var mu = ease(ramp(t, 6.55 + MATCHED[i] * 0.16, 7.05 + MATCHED[i] * 0.16));
    grid[i].style.transform = 'scale(' + (1 + 0.1 * mu) + ')';
    grid[i].style.boxShadow = '0 0 0 ' + (4 * mu) + 'px rgba(24,119,242,'
                            + (0.22 * mu) + ')';
  }
}
window.render = render;

// Opened plainly, or printed, the slide shows its finished state.
// Append #play to watch it build.
if (location.hash === '#play') {
  var t0 = performance.now();
  (function loop(now) { render(((now - t0) / 1000) % 8.6); requestAnimationFrame(loop); })(t0);
} else {
  render(8.0);
}
</script>

</body>
</html>
'''

matches_svg = '\n'.join(
    '        <path class="match" id="m%d" style="stroke:%s" d="%s"/>'
    % (j, colour, d) for j, (d, colour) in enumerate(MATCH_PATHS))

out = (TPL.replace('__ARR1__', ARR1).replace('__ARR2__', ARR2)
          .replace('__MATCH__', matches_svg)
          .replace('__PILE__', PILE_HTML).replace('__GRID__', GRID_HTML)
          .replace('__PEOPLE__', PEOPLE_HTML)
          .replace('__NPILE__', str(len(PILE))).replace('__NGRID__', str(len(GRID)))
          .replace('__MATCHED__', '{' + ', '.join('%d: %d' % (k, v)
                                                  for k, v in MATCH.items()) + '}'))

path = 'slides/andromeda-retrieval.html'
open(path, 'w').write(out)
print('wrote %s (%d tiles in the heap, %d kept)' % (path, len(PILE), len(GRID)))
