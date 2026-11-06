#!/usr/bin/env python3
"""Two slides about what a set of ads is actually made of.

Both are the same shape: the lines, stacked, at the size they deserve. The ad
itself is one small label at the left, because the angle is the content here
and a video thumbnail beside every line only takes room away from it.

The first is one idea written five ways, with the repeated phrase picked out
in the accent so the sameness is visible before the title is read. The second
is eight ads that each come at the buyer from somewhere else.

    ./build-ad-sets.py    writes both 16:9 slides
"""
import os
import re

os.chdir(os.path.dirname(os.path.abspath(__file__)))

W, H = 1920, 1080

ONE_IDEA = [
    'Make money with <i>TikTok Shop</i>',
    '<i>TikTok Shop</i> is exploding',
    'Start a <i>TikTok Shop</i> brand',
    '<i>TikTok Shop</i> opportunity 2026',
    'Why <i>TikTok Shop</i> is huge',
]

EIGHT_REASONS = [
    'Tried ecom before and failed',
    'Can&rsquo;t choose a product',
    'Already want a brand but don&rsquo;t know the steps',
    'Need something compatible with existing job/business',
    'Skeptical of ecommerce gurus',
    'Considering wholesale instead',
    'Overthinking LLC/name/logo',
    'Direct opportunity',
]

# Eight tints, so no two of the eight look like the same ad twice.
TINTS = ['#E4EFFD', '#DCEAFB', '#D3E4FA', '#CBDFF9',
         '#C3DAF8', '#BBD5F7', '#B3D0F6', '#AACBF5']

TPL = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>__TITLE__</title>
<link rel="stylesheet" href="../../4pi.css">
<link rel="stylesheet" href="../../voice-quiet.css">
<style>
/* ============================================================================
   See build-ad-sets.py. A row (or two rows) of ad creatives, each one a frame
   over its line. The frames carry no art: the line is the point.

   Class names are prefixed as; neither shared sheet uses them.
   ========================================================================= */
@page { size: __W__px __H__px; margin: 0; }

.slide { position: relative; width: __W__px; height: __H__px; padding: 0;
         background: var(--ground); }

.as__h {
  position: absolute; left: 110px; top: 44px; margin: 0;
  font-size: 54px; font-weight: 600; letter-spacing: -0.022em; color: var(--ink);
}
.as__h i { font-style: normal; color: var(--blue); }
.as__h em { font-style: normal; color: var(--ink-3); font-weight: 600; }

.as__list { position: absolute; left: 110px; }

.as__card {
  box-sizing: border-box; width: 1700px;
  background: var(--surface); border: 1px solid var(--hairline);
  border-radius: 18px; padding: 0 34px;
  box-shadow: 0 2px 12px rgba(20, 30, 50, 0.06);
  display: flex; align-items: center;
}
.as__card + .as__card { margin-top: __GAP__px; }

/* the ad is a label, not a picture */
.as__n {
  width: 104px; flex: none; margin: 0;
  font-size: 17px; font-weight: 700; letter-spacing: 0.08em;
  text-transform: uppercase; color: var(--ink-3);
}
.as__bar { width: 1px; flex: none; background: var(--hairline); margin-right: 30px; }
.as__t {
  margin: 0;
  font-weight: 600; letter-spacing: -0.018em; line-height: 1.2; color: var(--ink);
}
.as__t i { font-style: normal; color: var(--blue); }
</style>
</head>
<body>

<!-- no-autofit: its own canvas, not a panel. -->
<section class="slide">

  <h1 class="as__h">__HEAD__</h1>

__ROWS__

</section>

</body>
</html>
'''

PLAY = '<path class="f" d="M46 34 L 86 62 L 46 90 Z"/>'


def _check_class_collisions():
    css = open('4pi.css').read() + open('voice-quiet.css').read()
    taken = set(re.findall(r'\.([a-zA-Z][\w-]*)', css))
    mine = set(re.findall(r'^\.([a-zA-Z][\w-]*)', TPL, re.M)) - {'slide'}
    clash = sorted(mine & taken)
    if clash:
        raise SystemExit('class names already used by the shared stylesheets: '
                         + ', '.join(clash))


_check_class_collisions()


def card(n, text, h, font):
    return ('<div class="as__card" style="height:%gpx">'
            '<p class="as__n">Ad %d</p>'
            '<div class="as__bar" style="height:%gpx"></div>'
            '<p class="as__t" style="font-size:%gpx">%s</p></div>'
            % (h, n, h * 0.46, font, text))


def write(path, title, head, rows, gap):
    out = (TPL.replace('__W__', str(W)).replace('__H__', str(H))
              .replace('__TITLE__', title).replace('__HEAD__', head)
              .replace('__GAP__', str(gap))
              .replace('__ROWS__', '\n'.join(rows)))
    open(path, 'w').write(out)
    print('wrote %s' % path)


# ---------------------------------------------------------------------------
# one idea, five times
# ---------------------------------------------------------------------------
rows = ''.join(card(i + 1, t, 128, 44) for i, t in enumerate(ONE_IDEA))
write('slides/wide/wide-ads-one-idea.html', 'One idea five times',
      '5 Ads <em>-</em> <i>1 Idea 5 Times</i>',
      ['  <div class="as__list" style="top:250px">%s</div>' % rows], 20)

# ---------------------------------------------------------------------------
# eight reasons
# ---------------------------------------------------------------------------
rows = ''.join(card(i + 1, t, 86, 34) for i, t in enumerate(EIGHT_REASONS))
write('slides/wide/wide-ads-eight-reasons.html', 'Eight reasons',
      '8 Ads <em>-</em> <i>8 Different Reasons to Convert</i>',
      ['  <div class="as__list" style="top:228px">%s</div>' % rows], 12)
