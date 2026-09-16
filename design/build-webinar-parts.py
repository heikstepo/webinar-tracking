#!/usr/bin/env python3
"""The webinar, in its five parts.

A numbered stepper rather than cards. Five parts with this much detail in a row
of cards would either shrink the type past reading or force each card to a
different height; down a track, every part gets the width of the slide and the
numerals carry the order.

The arrows inside parts three and four are kept as arrows rather than flattened
to commas, because that is how the sequence was written and they are doing work:
they say these happen in this order, inside that part.

    ./build-webinar-parts.py    writes the 16:9 slide and the vertical card
"""
import os
import re

os.chdir(os.path.dirname(os.path.abspath(__file__)))

A = '<span class="arw">&rarr;</span>'

PARTS = [
    ('Intro',
     'Hook with live proof, establish authority, sell the mechanism, '
     'get commitments, open 5 loops.'),
    ('Content',
     '3-5 logical steps. Teach the what, show a glimpse of how. '
     'Weave in proof, objections, and commitments.'),
    ('Transition',
     'Recap %s 3-5 &ldquo;yes&rdquo; questions %s Crossroads close' % (A, A)),
    ('Pitch',
     'Core offer %s price anchor for offers below $3k %s bonuses '
     '(second best first, best last) %s guarantee %s booking/payment link.'
     % (A, A, A, A)),
    ('Q&amp;A',
     'Stay 20-30+ minutes. Address 5-10 common objections, '
     'then answer live questions.'),
]

TPL = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>The webinar, in five parts</title>
<link rel="stylesheet" href="__CSS__4pi.css">
<link rel="stylesheet" href="__CSS__voice-quiet.css">
<style>
/* ============================================================================
   See build-webinar-parts.py. A stepper, because five parts this detailed
   cannot be cards side by side without shrinking the type past reading.
   ========================================================================= */
@page { size: __W__px __H__px; margin: 0; }

.slide { width: __W__px; height: __H__px; padding: __PY__px __PX__px; background: var(--ground); }

.plan { position: relative; width: __COLW__px; text-align: left; }

/* Behind the discs, from the first centre to the last, so the five read as one
   run rather than as five separate rows. */
.plan__line {
  position: absolute; left: __HALF__px; top: __HALF__px; bottom: __HALF__px;
  width: 3px; background: #D5DCE5; border-radius: 2px;
}

.plan__row { position: relative; display: flex; align-items: flex-start; gap: __GAP__px; }
.plan__row + .plan__row { margin-top: __RGAP__px; }

.plan__n {
  flex: none;
  width: __DISC__px; height: __DISC__px; border-radius: 50%;
  background: #E4EFFD;
  display: flex; align-items: center; justify-content: center;
  font-size: __NUM__px; font-weight: 700; letter-spacing: -0.01em; color: var(--blue);
}

.plan__t {
  margin: 0;
  font-size: __TITLE__px; font-weight: 600; letter-spacing: -0.012em; color: var(--ink);
}
.plan__b {
  margin: __BGAP__px 0 0;
  font-size: __BODY__px; font-weight: 500; line-height: 1.36; color: var(--ink-2);
}
/* The sequence arrows: the accent, so the order inside a part is visible at a
   glance without reading the words around it. */
.arw { color: var(--blue); font-weight: 700; padding: 0 __APAD__px; }
</style>
</head>
<body>

<!-- no-autofit: its own canvas, not a panel. -->
<section class="slide slide--center slide--mid">

  <div class="plan">
    <div class="plan__line"></div>
__ROWS__
  </div>

</section>

</body>
</html>
'''

ROW = '''    <div class="plan__row">
      <span class="plan__n">%d</span>
      <div>
        <h3 class="plan__t">%s</h3>
        <p class="plan__b">%s</p>
      </div>
    </div>'''

def _check_class_collisions():
    """Fail loudly on a name the shared stylesheets already use.

    A local rule only overrides the properties it actually restates, so a
    shared `.steps { display: flex }` silently kept this list laid out as a
    row even though the local rule set position, width and alignment.
    """
    css = open('4pi.css').read() + open('voice-quiet.css').read()
    taken = set(re.findall(r'\.([a-zA-Z][\w-]*)', css))
    mine = set(re.findall(r'^\.([a-zA-Z][\w-]*)', TPL, re.M)) - {'slide'}
    clash = sorted(mine & taken)
    if clash:
        raise SystemExit('class names already used by the shared stylesheets: '
                         + ', '.join(clash))


_check_class_collisions()

VARIANTS = [
    dict(path='slides/wide/wide-webinar-parts.html', css='../../',
         W=1920, H=1080, PX=110, PY=90, COLW=1700, GAP=36, RGAP=38,
         DISC=72, HALF=36, NUM=34, TITLE=40, BGAP=10, BODY=26, APAD=9),
    dict(path='slides/vert-webinar-parts.html', css='../',
         W=1080, H=1200, PX=70, PY=70, COLW=940, GAP=28, RGAP=42,
         DISC=64, HALF=32, NUM=30, TITLE=42, BGAP=10, BODY=30, APAD=8),
]

plan = '\n\n'.join(ROW % (i, t, b) for i, (t, b) in enumerate(PARTS, 1))

for v in VARIANTS:
    out = TPL
    for k in ('W', 'H', 'PX', 'PY', 'COLW', 'GAP', 'RGAP', 'DISC', 'HALF',
              'NUM', 'TITLE', 'BGAP', 'BODY', 'APAD'):
        out = out.replace('__%s__' % k, str(v[k]))
    out = out.replace('__CSS__', v['css']).replace('__ROWS__', plan)
    os.makedirs(os.path.dirname(v['path']), exist_ok=True)
    open(v['path'], 'w').write(out)
    print('wrote %s' % v['path'])
