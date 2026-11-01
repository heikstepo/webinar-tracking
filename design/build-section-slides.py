#!/usr/bin/env python3
"""A standalone card for each section, in the running order's own typography.

The number stays beside the title rather than stacking above it, because that
is how the contents slide sets them, and a section card that rhymes with the
contents tells a viewer where they are without a word of explanation.

Section four's parts each get their own card carrying the parent above them:
the parent quiet and small, the part itself full size. A card that said only
"4.1 Meta Ads Strategy" would make the viewer remember what four was.

    ./build-section-slides.py    writes one 16:9 slide per section
"""
import os
import re

os.chdir(os.path.dirname(os.path.abspath(__file__)))

PARENT = ('4', 'Meta Ads')

# (slug, number, title, parent or None)
SECTIONS = [
    ('1-icp-analysis', '1', 'ICP Analysis', None),
    ('2-offer', '2', 'Offer', None),
    ('3-funnel', '3', 'Funnel', None),
    ('4-1-meta-ads-strategy', '4.1', 'Meta Ads Strategy', PARENT),
    ('4-2-scripting-meta-ads', '4.2', 'Scripting Meta Ads', PARENT),
    ('4-3-pixel-conditioning', '4.3', 'Pixel Conditioning', PARENT),
    ('5-sales-ops', '5', 'Sales &amp; Ops', None),
]

TPL = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>__PLAIN__</title>
<link rel="stylesheet" href="../../4pi.css">
<link rel="stylesheet" href="../../voice-quiet.css">
<style>
/* ============================================================================
   See build-section-slides.py. Number beside title, as on the contents slide,
   so a section card rhymes with the list it came from.
   ========================================================================= */
@page { size: 1920px 1080px; margin: 0; }

.slide { width: 1920px; height: 1080px; padding: 90px 110px; background: var(--ground); }

.sec { width: max-content; max-width: 1700px; margin: 0 auto; text-align: left; }

/* The parent, when there is one: the same line one size down and quiet, with
   a rule under it so the two read as one block rather than two titles. */
.sec__up {
  display: flex; align-items: baseline; gap: 20px;
  margin: 0 0 26px; padding-bottom: 26px;
  border-bottom: 3px solid #D7DCE3;
}
.sec__up-n {
  font-size: 46px; font-weight: 600; letter-spacing: -0.016em; color: #7CB2F3;
}
.sec__up-t {
  font-size: 46px; font-weight: 600; letter-spacing: -0.016em; color: var(--ink-2);
}

.sec__row { display: flex; align-items: baseline; gap: 34px; }
.sec__n {
  font-size: 108px; font-weight: 600; letter-spacing: -0.03em; color: var(--blue);
}
.sec__t {
  font-size: 108px; font-weight: 600; letter-spacing: -0.03em; color: var(--ink);
}
</style>
</head>
<body>

<!-- no-autofit: its own canvas, not a panel. -->
<section class="slide slide--center slide--mid">

  <div class="sec">
__UP__
    <div class="sec__row">
      <span class="sec__n">__N__</span><span class="sec__t">__T__</span>
    </div>
  </div>

</section>

</body>
</html>
'''

UP = '''    <div class="sec__up">
      <span class="sec__up-n">%s</span><span class="sec__up-t">%s</span>
    </div>
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

for slug, n, title, parent in SECTIONS:
    out = (TPL.replace('__UP__', UP % parent if parent else '')
              .replace('__N__', n)
              .replace('__T__', title)
              .replace('__PLAIN__', '%s %s' % (n, title.replace('&amp;', '&'))))
    path = 'slides/wide/wide-sec-%s.html' % slug
    open(path, 'w').write(out)
    print('wrote %s' % path)
