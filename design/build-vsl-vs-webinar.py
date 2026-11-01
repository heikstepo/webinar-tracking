#!/usr/bin/env python3
"""VSL against webinar: three states of the same slide.

One layout, three slides. Nothing moves between them, which is the point: the
viewer's eye stays where it was and only the weight changes, so the cut reads
as "this one now" rather than as a new slide.

The faded side is set in a pale grey rather than given an opacity, so the
exact value is in the file and will not shift if the ground ever changes.

    ./build-vsl-vs-webinar.py    writes the three 16:9 slides
"""
import os
import re

os.chdir(os.path.dirname(os.path.abspath(__file__)))

INK = 'var(--ink)'
# Visible, clearly recessed: still readable on the ground, never competing.
OFF = '#C7CCD4'

# (slug, left colour, right colour)
STATES = [
    ('both', INK, INK),
    ('vsl', INK, OFF),
    ('webinar', OFF, INK),
]

TPL = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>VSL or webinar</title>
<link rel="stylesheet" href="__CSS__4pi.css">
<link rel="stylesheet" href="__CSS__voice-quiet.css">
<style>
/* ============================================================================
   See build-vsl-vs-webinar.py. One layout in three states: nothing moves
   between the slides, only the weight changes.

   Class names are prefixed duo; voice-quiet.css already owns .split.
   ========================================================================= */
@page { size: 1920px 1080px; margin: 0; }

.slide { width: 1920px; height: 1080px; padding: 0; background: var(--ground); }

.duo { position: relative; width: 1920px; height: 1080px; }

/* Inset top and bottom rather than full bleed: a rule that runs off both
   edges cuts the slide in two where this divides it. */
.duo__rule {
  position: absolute; left: 50%; top: 190px; bottom: 190px;
  width: 3px; margin-left: -1.5px; background: #D2D8E0; border-radius: 2px;
}

.duo__half {
  position: absolute; top: 0; width: 960px; height: 1080px;
  display: flex; align-items: center; justify-content: center;
}
.duo__half--l { left: 0; }
.duo__half--r { left: 960px; }

.duo__word {
  margin: 0;
  font-size: 118px; font-weight: 600; letter-spacing: -0.032em;
}
</style>
</head>
<body>

<!-- no-autofit: its own canvas, not a panel. -->
<section class="slide">

  <div class="duo">
    <div class="duo__rule"></div>

    <div class="duo__half duo__half--l">
      <p class="duo__word" style="color:__L__">VSL</p>
    </div>

    <div class="duo__half duo__half--r">
      <p class="duo__word" style="color:__R__">Webinar</p>
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

for slug, left, right in STATES:
    out = (TPL.replace('__CSS__', '../../')
              .replace('__L__', left).replace('__R__', right))
    path = 'slides/wide/wide-vsl-webinar-%s.html' % slug
    open(path, 'w').write(out)
    print('wrote %s' % path)
