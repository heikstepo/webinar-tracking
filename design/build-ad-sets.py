#!/usr/bin/env python3
"""Two slides about what a set of ads is actually made of.

The first is one idea written five ways: the repeated phrase is picked out in
the accent on every card, so the sameness is visible before the title is read.

The second is eight ads that each come at the buyer from somewhere else, so
nothing repeats and each card carries its own tint.

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

.as__row {
  position: absolute; left: 0; width: __W__px;
  display: flex; justify-content: center;
}

.as__card {
  box-sizing: border-box; flex: none;
  background: var(--surface); border: 1px solid var(--hairline);
  border-radius: 20px; padding: 18px;
  box-shadow: 0 3px 16px rgba(20, 30, 50, 0.07);
  display: flex; flex-direction: column;
}
.as__th {
  border-radius: 12px; background: #E4EFFD;
  display: flex; align-items: center; justify-content: center;
}
.as__th svg { display: block; fill: none; stroke: #7FA8DC; stroke-width: 3.4;
              stroke-linecap: round; stroke-linejoin: round; }
.as__th svg .f { fill: var(--blue); stroke: none; }

.as__n {
  margin: 15px 0 0;
  font-size: 15px; font-weight: 700; letter-spacing: 0.08em;
  text-transform: uppercase; color: var(--ink-3);
}
.as__t {
  margin: 8px 0 0;
  font-weight: 600; letter-spacing: -0.014em; line-height: 1.22; color: var(--ink);
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


def card(n, text, w, h, th_h, font, tint='#E4EFFD', glyph=56):
    return ('<div class="as__card" style="width:%gpx; height:%gpx">'
            '<div class="as__th" style="height:%gpx; background:%s">'
            '<svg viewBox="0 0 124 124" style="width:%gpx;height:%gpx" '
            'aria-hidden="true">%s</svg></div>'
            '<p class="as__n">Ad %d</p>'
            '<p class="as__t" style="font-size:%gpx">%s</p></div>'
            % (w, h, th_h, tint, glyph, glyph, PLAY, n, font, text))


def write(path, title, head, rows):
    out = (TPL.replace('__W__', str(W)).replace('__H__', str(H))
              .replace('__TITLE__', title).replace('__HEAD__', head)
              .replace('__ROWS__', '\n'.join(rows)))
    open(path, 'w').write(out)
    print('wrote %s' % path)


# ---------------------------------------------------------------------------
# one idea, five times: five vertical creatives in a row
# ---------------------------------------------------------------------------
cards = ''.join(card(i + 1, t, 340, 660, 520, 26) for i, t in enumerate(ONE_IDEA))
write('slides/wide/wide-ads-one-idea.html', 'One idea five times',
      '5 Ads <em>-</em> <i>1 Idea 5 Times</i>',
      ['  <div class="as__row" style="top:214px; gap:26px">%s</div>' % cards])

# ---------------------------------------------------------------------------
# eight reasons: two rows of four, each with its own tint
# ---------------------------------------------------------------------------
rows = []
for r in range(2):
    cards = ''.join(
        card(r * 4 + i + 1, EIGHT_REASONS[r * 4 + i], 396, 336, 176, 24,
             TINTS[r * 4 + i], 52)
        for i in range(4))
    rows.append('  <div class="as__row" style="top:%dpx; gap:28px">%s</div>'
                % (206 + r * 370, cards))

write('slides/wide/wide-ads-eight-reasons.html', 'Eight reasons',
      '8 Ads <em>-</em> <i>8 Different Reasons to Convert</i>', rows)
