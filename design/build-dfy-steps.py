#!/usr/bin/env python3
"""The Amazon example: the first few steps in full, then the rest trailing off.

Three tiers, getting smaller left to right. The first four steps are shown in
full because they are the ones that explain the idea. Paid ads is named but
drawn smaller and without a card, and after it the track carries plain dots
that shrink and fade: there are more steps, and this is not a list of them.

That also settles a slot that could not be filled honestly. Paid ads is named
in the script but its done-for-you element is never stated, and an empty card
under it read as a mistake where a smaller marker reads as the tail starting.

    ./build-dfy-steps.py    writes the 16:9 slide
"""
import os
import re

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# (step, done-for-you element, disc colour). The ramp is one thing increasing,
# matching the step map this sits next to.
SHOWN = [
    ('Pick Product', 'We pick 3 proven products, you choose one', '#C5DDFA'),
    ('Branding', 'AI branding templates', '#A7CCF7'),
    ('Build Store', 'We build the store with AI', '#7CB2F3'),
    ('Influencers', 'We connect you to our influencer network', '#4A97EF'),
]
TAIL = ('Paid Ads', '#2E87E8')

# (centre, radius, colour) — closing up and fading as they go.
DOTS = [(1496, 16, '#9DBCE0'), (1558, 13, '#AFC6E4'),
        (1612, 10.5, '#BFD2E8'), (1658, 8.5, '#CBDAEC'), (1690, 7, '#D6E1F0')]

COL, GAP, GUTTER = 240, 28, 290
TAIL_X = 1412

TPL = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Every step, done for you</title>
<link rel="stylesheet" href="../../4pi.css">
<link rel="stylesheet" href="../../voice-quiet.css">
<style>
/* ============================================================================
   See build-dfy-steps.py. Three tiers getting smaller: the steps that explain
   the idea, the one that starts the tail, and the dots that say it goes on.
   ========================================================================= */
@page { size: 1920px 1080px; margin: 0; }

.slide { width: 1920px; height: 1080px; padding: 90px 110px; background: var(--ground); }

.dfy { position: relative; width: 1700px; height: 356px; text-align: left; }

/* Named once, on the left, for the whole row. */
.dfy__side {
  position: absolute; left: 0; width: 250px; margin: 0;
  transform: translateY(-50%); text-align: right;
  font-size: 34px; font-weight: 600; letter-spacing: -0.01em; color: var(--ink-3);
}

/* Behind the discs, from the first centre out to the last dot. */
.dfy__line {
  position: absolute; left: __L0__px; width: __LW__px; top: 41px; height: 3px;
  background: #D2D8E0; border-radius: 2px;
}

.dfy__col { position: absolute; top: 0; width: __COL__px; }

.dfy__n {
  display: flex; align-items: center; justify-content: center;
  width: 84px; height: 84px; margin: 0 auto; border-radius: 50%;
  font-size: 38px; font-weight: 700; letter-spacing: -0.01em; color: #fff;
}
.dfy__step {
  margin: 20px 0 0; text-align: center;
  font-size: 34px; font-weight: 600; letter-spacing: -0.012em; color: var(--ink);
}

/* The step that starts the tail: same thing, one size down and no card. */
.dfy__tail { position: absolute; top: 9px; width: 220px; transform: translateX(-50%); }
.dfy__tail .dfy__n { width: 64px; height: 64px; font-size: 30px; }
.dfy__tail .dfy__step { margin-top: 16px; font-size: 28px; color: var(--ink-2); }

/* No number, no name. They are a quantity, not entries. */
.dfy__dot { position: absolute; border-radius: 50%; }

/* The done-for-you element. One fixed height, so the four bottoms line up
   however long the line inside is. */
.dfy__card {
  position: absolute; top: 186px; width: __COL__px; height: 170px;
  box-sizing: border-box;
  display: flex; align-items: center; justify-content: center;
  padding: 22px 24px; border-radius: 20px;
  background: #E4EFFD;
}
.dfy__card p {
  margin: 0; text-align: center;
  font-size: 25px; font-weight: 500; line-height: 1.36; color: #1E4E8C;
}
</style>
</head>
<body>

<!-- no-autofit: its own canvas, not a panel. -->
<section class="slide slide--center slide--mid">

  <div class="dfy">

    <div class="dfy__line"></div>

    <p class="dfy__side" style="top:73px">Steps</p>
    <p class="dfy__side" style="top:271px">Done for you</p>

__COLS__

__TAIL__

__DOTS__

  </div>

</section>

</body>
</html>
'''

COLUMN = '''    <div class="dfy__col" style="left:%(x)dpx">
      <span class="dfy__n" style="background:%(chip)s">%(n)d</span>
      <h3 class="dfy__step">%(step)s</h3>
    </div>
    <div class="dfy__card" style="left:%(x)dpx"><p>%(body)s</p></div>'''


def _check_class_collisions():
    css = open('4pi.css').read() + open('voice-quiet.css').read()
    taken = set(re.findall(r'\.([a-zA-Z][\w-]*)', css))
    mine = set(re.findall(r'^\.([a-zA-Z][\w-]*)', TPL, re.M)) - {'slide'}
    clash = sorted(mine & taken)
    if clash:
        raise SystemExit('class names already used by the shared stylesheets: '
                         + ', '.join(clash))


_check_class_collisions()

cols = '\n\n'.join(
    COLUMN % dict(x=GUTTER + i * (COL + GAP), n=i + 1, chip=chip,
                  step=step, body=dfy)
    for i, (step, dfy, chip) in enumerate(SHOWN))

tail = ('    <div class="dfy__tail" style="left:%dpx">\n'
        '      <span class="dfy__n" style="background:%s">%d</span>\n'
        '      <h3 class="dfy__step">%s</h3>\n'
        '    </div>' % (TAIL_X, TAIL[1], len(SHOWN) + 1, TAIL[0]))

dots = '\n'.join(
    '    <span class="dfy__dot" style="left:%gpx; top:%gpx; width:%gpx; '
    'height:%gpx; background:%s"></span>' % (x - r, 42.5 - r, r * 2, r * 2, c)
    for x, r, c in DOTS)

first = GUTTER + COL // 2
out = (TPL.replace('__COL__', str(COL))
          .replace('__L0__', str(first))
          .replace('__LW__', str(DOTS[-1][0] - first))
          .replace('__COLS__', cols)
          .replace('__TAIL__', tail)
          .replace('__DOTS__', dots))

path = 'slides/wide/wide-dfy-steps.html'
open(path, 'w').write(out)
print('wrote %s' % path)
