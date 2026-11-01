#!/usr/bin/env python3
"""The thumbnail panel: the whole deck as one roadmap.

Sized 960x1080, which is exactly the right half of a 16:9 frame, so it drops
straight in beside a talking head without being cropped or letterboxed.

Only the headline has to be readable at thumbnail size. Everything under it is
there to look like a lot of ground covered, which is why the chips are dense
and small rather than few and large: at 320px wide they read as substance, and
at full size they read as a contents page.

Every chip is a thing the deck actually contains. Nothing here is a promise
the slides do not keep.

    ./build-thumb-roadmap.py    writes the panel
"""
import os
import re

os.chdir(os.path.dirname(os.path.abspath(__file__)))

W, H = 960, 1080

# (number, step, chips, disc colour)
STEPS = [
    ('1', 'ICP Analysis',
     ['Fathom &middot; Reddit &middot; YouTube', 'ICP 1 &amp; ICP 2',
      'Pain vs Dream'], '#3C8FEC'),
    ('2', 'Offer',
     ['DIY &middot; DWY &middot; DFY', 'Offer Line', 'Done For You Steps'],
     '#5BA1F0'),
    ('3', 'Funnel',
     ['VSL vs Webinar', 'Opt-in &rarr; TY A / B'], '#7CB2F3'),
    ('4', 'Meta Ads',
     ['Campaign Structure', '3 Creatives per Ad', 'Sequence Learning',
      'Purchase Journey', 'Pixel Conditioning'], '#1E7DE8'),
    ('5', 'Sales &amp; Ops',
     ['Speed to Lead', 'Pre Call Sequence', 'Setters'], '#0071E3'),
]

TPL = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Scale Info to $100k/mo</title>
<link rel="stylesheet" href="../../4pi.css">
<link rel="stylesheet" href="../../voice-quiet.css">
<style>
/* ============================================================================
   See build-thumb-roadmap.py. The right half of a 16:9 thumbnail: one headline
   that has to survive being shrunk, over a roadmap that only has to look like
   a lot of ground.

   Class names are prefixed th; neither shared sheet uses them.
   ========================================================================= */
@page { size: __W__px __H__px; margin: 0; }

.slide {
  width: __W__px; height: __H__px; padding: 54px; background: var(--ground);
  display: flex; flex-direction: column; justify-content: center;
}

/* ---- the headline -------------------------------------------------------- */
.th__h {
  margin: 0 0 6px;
  font-size: 84px; font-weight: 700; letter-spacing: -0.038em; line-height: 1.04;
  color: var(--ink);
}
/* Blue and marked. One of the two carries at thumbnail size; both together
   survive being shrunk to a third of this. */
.th__sum {
  color: var(--blue);
  background: linear-gradient(to top, #C6DDFA 0 0.17em, transparent 0.17em);
}
.th__sub {
  margin: 0 0 44px;
  font-size: 42px; font-weight: 600; letter-spacing: -0.016em; color: var(--ink-2);
}

/* ---- the roadmap --------------------------------------------------------- */
.th__row { position: relative; display: flex; gap: 24px; }
.th__row + .th__row { margin-top: 28px; }

/* The rail, drawn per row down to the next one, so it needs no measuring. */
.th__row::before {
  content: ""; position: absolute; left: 25px; top: 54px; bottom: -28px;
  width: 3px; background: #D5DCE5;
}
.th__row:last-child::before { display: none; }

.th__n {
  position: relative; flex: none;
  width: 54px; height: 54px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  font-size: 27px; font-weight: 700; letter-spacing: -0.01em; color: #fff;
}

.th__name {
  margin: 0 0 12px;
  font-size: 42px; font-weight: 600; letter-spacing: -0.018em; color: var(--ink);
}
.th__chips { display: flex; flex-wrap: wrap; gap: 10px; }
.th__chip {
  padding: 8px 15px; border-radius: 11px;
  background: #E4EFFD; color: #1E4E8C;
  font-size: 22px; font-weight: 600; letter-spacing: -0.004em;
  white-space: nowrap;
}
</style>
</head>
<body>

<section class="slide">

  <h1 class="th__h">Scale Info to<br><span class="th__sum">$100k/mo</span></h1>
  <p class="th__sub">(Meta Ads)</p>

__ROWS__

</section>

</body>
</html>
'''

ROW = '''  <div class="th__row">
    <span class="th__n" style="background:%s">%s</span>
    <div>
      <p class="th__name">%s</p>
      <div class="th__chips">%s</div>
    </div>
  </div>'''


def _check_class_collisions():
    css = open('4pi.css').read() + open('voice-quiet.css').read()
    taken = set(re.findall(r'\.([a-zA-Z][\w-]*)', css))
    mine = set(re.findall(r'^\.([a-zA-Z][\w-]*)', TPL, re.M)) - {'slide'}
    clash = sorted(mine & taken)
    if clash:
        raise SystemExit('class names already used by the shared stylesheets: '
                         + ', '.join(clash))


_check_class_collisions()

rows = '\n\n'.join(
    ROW % (chip, n, name,
           ''.join('<span class="th__chip">%s</span>' % c for c in chips))
    for n, name, chips, chip in STEPS)

out = TPL.replace('__W__', str(W)).replace('__H__', str(H)).replace('__ROWS__', rows)

path = 'slides/wide/thumb-roadmap.html'
open(path, 'w').write(out)
print('wrote %s' % path)
