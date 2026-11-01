#!/usr/bin/env python3
"""What goes into the pixel comes back out of it, and two statements after.

Four slides. The two flow slides are one layout in two colours: the pixel does
not change, only what is fed to it, so nothing in the drawing moves between
them. The arrow in and the arrow out carry the same words on each slide,
because that is the whole argument.

Red for the bad input and green for the good one, both already in the deck for
exactly those jobs. The blue accent stays out of it: here it would be a third
hue saying nothing.

    ./build-pixel-quality.py    writes the two flow slides and the two statements
"""
import os
import re

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def logo(slug):
    """A brand mark as a single colour <svg> body, fills stripped so it takes
    the colour set on the tile rather than keeping its own."""
    src = open('logos/%s.svg' % slug).read()
    box = re.search(r'viewBox="([^"]+)"', src).group(1)
    body = src[src.index('>', src.index('<svg')) + 1:src.rindex('</svg>')]
    return box, re.sub(r'\s*fill="[^"]*"', '', body).strip()


META_BOX, META = logo('meta')

# (slug, word, arrow colour, label colour)
FLOWS = [
    ('low', 'Low Quality Leads', 'var(--red)', 'var(--red)'),
    ('high', 'High Quality Leads', 'var(--green)', '#248A13'),
]

FLOW_TPL = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>__WORD__ through the pixel</title>
<link rel="stylesheet" href="../../4pi.css">
<link rel="stylesheet" href="../../voice-quiet.css">
<style>
/* ============================================================================
   See build-pixel-quality.py. One layout in two colours: the pixel does not
   change, only what is fed to it.

   Class names are prefixed pix; neither shared sheet uses them.
   ========================================================================= */
@page { size: 1920px 1080px; margin: 0; }

.slide { width: 1920px; height: 1080px; padding: 90px 110px; background: var(--ground); }

.pix { position: relative; width: 1700px; height: 440px; }

/* ---- the pixel ----------------------------------------------------------- */
.pix__box {
  position: absolute; left: 640px; top: 80px; width: 420px; height: 280px;
  box-sizing: border-box;
  background: var(--surface); border: 1px solid var(--hairline);
  border-radius: 28px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04);
  display: flex; flex-direction: column; align-items: center; justify-content: center;
}
.pix__box svg { display: block; width: 104px; height: 104px; fill: var(--ink); }
.pix__name {
  margin: 22px 0 0;
  font-size: 44px; font-weight: 600; letter-spacing: -0.014em; color: var(--ink);
}

/* ---- in and out ---------------------------------------------------------- */
/* Rail and triangle rather than one SVG, so the head keeps its proportions
   whatever the rail's length. */
.pix__rail { position: absolute; top: 216px; height: 8px; border-radius: 4px; }
.pix__head {
  position: absolute; top: 194px; width: 0; height: 0;
  border-top: 26px solid transparent; border-bottom: 26px solid transparent;
}

.pix__label {
  position: absolute; top: 104px; width: 600px; margin: 0; text-align: center;
  font-size: 46px; font-weight: 600; letter-spacing: -0.014em; color: __LC__;
}
</style>
</head>
<body>

<!-- no-autofit: its own canvas, not a panel. -->
<section class="slide slide--center slide--mid">

  <div class="pix">

    <p class="pix__label" style="left:0">__WORD__</p>
    <div class="pix__rail" style="left:0; width:556px; background:__AC__"></div>
    <div class="pix__head" style="left:556px; border-left:44px solid __AC__"></div>

    <div class="pix__box">
      <svg viewBox="__MBOX__" aria-hidden="true">__META__</svg>
      <p class="pix__name">Meta Pixel</p>
    </div>

    <p class="pix__label" style="left:1100px">__WORD__</p>
    <div class="pix__rail" style="left:1100px; width:556px; background:__AC__"></div>
    <div class="pix__head" style="left:1656px; border-left:44px solid __AC__"></div>

  </div>

</section>

</body>
</html>
'''

# (slug, html of the line)
SAYS = [
    ('protect-your-pixel',
     'Protect your Pixel &amp; Ad Account<br>from '
     '<span class="say__hot">Broke Leads</span>!'),
    ('conversion-event-back',
     'Put your Conversion Event<br>'
     '<span class="say__cool">as far back in the funnel</span> as possible'),
]

SAY_TPL = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Statement</title>
<link rel="stylesheet" href="../../4pi.css">
<link rel="stylesheet" href="../../voice-quiet.css">
<style>
/* ============================================================================
   A statement on its own, set the way the offer line is set: one accent on the
   words the sentence turns on, and nothing else.

   Class names are prefixed say__ with a local .says wrapper; voice-quiet.css
   owns .say and .say__mark, which is why neither is reused here.
   ========================================================================= */
@page { size: 1920px 1080px; margin: 0; }

.slide { width: 1920px; height: 1080px; padding: 90px 110px; background: var(--ground); }

.says { width: 1700px; text-align: center; }
.says p {
  margin: 0;
  font-size: 86px; font-weight: 600; letter-spacing: -0.026em; line-height: 1.24;
  color: var(--ink);
}
.says .say__hot { color: var(--red); }
.says .say__cool { color: var(--blue); }
</style>
</head>
<body>

<!-- no-autofit: its own canvas, not a panel. -->
<section class="slide slide--center slide--mid">
  <div class="says">
    <p>__LINE__</p>
  </div>
</section>

</body>
</html>
'''


def _check_class_collisions(tpl):
    css = open('4pi.css').read() + open('voice-quiet.css').read()
    taken = set(re.findall(r'\.([a-zA-Z][\w-]*)', css))
    mine = set(re.findall(r'^\.([a-zA-Z][\w-]*)', tpl, re.M)) - {'slide'}
    clash = sorted(mine & taken)
    if clash:
        raise SystemExit('class names already used by the shared stylesheets: '
                         + ', '.join(clash))


for t in (FLOW_TPL, SAY_TPL):
    _check_class_collisions(t)

for slug, word, arrow, label in FLOWS:
    out = (FLOW_TPL.replace('__WORD__', word)
                   .replace('__AC__', arrow)
                   .replace('__LC__', label)
                   .replace('__MBOX__', META_BOX)
                   .replace('__META__', META))
    path = 'slides/wide/wide-pixel-%s.html' % slug
    open(path, 'w').write(out)
    print('wrote %s' % path)

for slug, line in SAYS:
    path = 'slides/wide/wide-say-%s.html' % slug
    open(path, 'w').write(SAY_TPL.replace('__LINE__', line))
    print('wrote %s' % path)
