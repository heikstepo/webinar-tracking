#!/usr/bin/env python3
"""The Amazon example: every step, and the done-for-you element on each.

Two rows against one gutter. The row labels are said once on the left rather
than repeated on all five cards, and both of them are words from the script.

The fifth card is empty on purpose. The paid ads step is named but its
done-for-you element is never stated, so there is nothing to put there. A
dashed outline says the slot exists and is waiting, where writing a plausible
line would put words in the mouth of someone who did not say them.

    ./build-dfy-steps.py    writes the 16:9 slide
"""
import os
import re

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# (step, done-for-you element, disc colour). The ramp is one thing increasing,
# matching the step map this sits next to.
STEPS = [
    ('Pick Product', 'We pick 3 proven products, you choose one', '#C5DDFA'),
    ('Branding', 'AI branding templates', '#A7CCF7'),
    ('Build Store', 'We build the store with AI', '#7CB2F3'),
    ('Influencers', 'We connect you to our influencer network', '#4A97EF'),
    ('Paid Ads', '', '#0071E3'),
]

COL, GAP, GUTTER = 254, 30, 290

TPL = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Every step, done for you</title>
<link rel="stylesheet" href="../../4pi.css">
<link rel="stylesheet" href="../../voice-quiet.css">
<style>
/* ============================================================================
   See build-dfy-steps.py. Two rows against one gutter, so "Steps" and "Done
   for you" are each said once instead of five times.
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

/* Behind the discs, from the first centre to the last. */
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

/* The done-for-you element. One fixed height, so the five bottoms line up
   however long the line inside is. */
.dfy__card {
  position: absolute; top: 186px; width: __COL__px; height: 170px;
  box-sizing: border-box;
  display: flex; align-items: center; justify-content: center;
  padding: 22px 26px; border-radius: 20px;
  background: #E4EFFD;
}
.dfy__card p {
  margin: 0; text-align: center;
  font-size: 25px; font-weight: 500; line-height: 1.36; color: #1E4E8C;
}
/* The slot that was never filled in. */
.dfy__card--open { background: none; border: 3px dashed #BFD6F7; }
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

  </div>

</section>

</body>
</html>
'''

COLUMN = '''    <div class="dfy__col" style="left:%(x)dpx">
      <span class="dfy__n" style="background:%(chip)s">%(n)d</span>
      <h3 class="dfy__step">%(step)s</h3>
    </div>
    <div class="dfy__card%(mod)s" style="left:%(x)dpx">%(body)s</div>'''


def _check_class_collisions():
    css = open('4pi.css').read() + open('voice-quiet.css').read()
    taken = set(re.findall(r'\.([a-zA-Z][\w-]*)', css))
    mine = set(re.findall(r'^\.([a-zA-Z][\w-]*)', TPL, re.M)) - {'slide'}
    clash = sorted(mine & taken)
    if clash:
        raise SystemExit('class names already used by the shared stylesheets: '
                         + ', '.join(clash))


_check_class_collisions()

cols = []
for i, (step, dfy, chip) in enumerate(STEPS):
    cols.append(COLUMN % dict(
        x=GUTTER + i * (COL + GAP), n=i + 1, chip=chip, step=step,
        mod='' if dfy else ' dfy__card--open',
        body='<p>%s</p>' % dfy if dfy else ''))

first = GUTTER + COL // 2
last = GUTTER + (len(STEPS) - 1) * (COL + GAP) + COL // 2

out = (TPL.replace('__COL__', str(COL))
          .replace('__L0__', str(first))
          .replace('__LW__', str(last - first))
          .replace('__COLS__', '\n\n'.join(cols)))

path = 'slides/wide/wide-dfy-steps.html'
open(path, 'w').write(out)
print('wrote %s' % path)
