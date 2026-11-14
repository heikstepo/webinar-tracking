#!/usr/bin/env python3
"""How to decrease CPMs: the grid, the blurred grid, and one slide per lever.

Three shapes from one source, so the words only exist once:

    wide-decrease-cpm.html        all six, readable
    wide-decrease-cpm-blur.html   the same six with everything but the numbers
                                  blurred out, so only the headline reads
    wide-decrease-cpm-1..6.html   one lever per slide, at size

The last lever is the aside, so it loses the white ground and the accent in
every one of them.

    ./build-decrease-cpm.py
"""
import os
import re

os.chdir(os.path.dirname(os.path.abspath(__file__)))

W, H = 1920, 1080

HEAD = 'How to decrease <i>CPMs</i>'

# (number, disc colour, lever, reason)
CARDS = [
    ('1', '#8FC0F5', 'Type of person / competition',
     'More advertisers competing for the same people = more expensive auctions '
     '= <i>higher CPM</i>'),
    ('2', '#74B0F1', 'Format diversity / native formats',
     'More feed-native creative can improve predicted response + ad quality, '
     'helping you win impressions more efficiently'),
    ('3', '#58A0EE', 'More organic content',
     'Creates more engaged/warm users Meta can still reach inside broad '
     'targeting, which can improve delivery efficiency'),
    ('4', '#3D90EA', 'Keep audience broad',
     'Gives Meta access to more auctions instead of forcing delivery into a '
     'small, expensive pool'),
    ('5', '#0071E3', 'Better copy',
     'Makes the right people more likely to react or convert, so Meta can show '
     'the ad more efficiently.'),
    ('6', '#AEB8C6', 'Cost Caps', 'lowkey bro science lmao'),
]

TPL = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>How to decrease CPMs</title>
<link rel="stylesheet" href="../../4pi.css">
<link rel="stylesheet" href="../../voice-quiet.css">
<style>
/* ============================================================================
   See build-decrease-cpm.py. Each lever is a card rather than a bulleted line,
   which is what lets the lever be a heading and the reason be body text: the
   break does the work a dash would have done.

   The blurred variant keeps only the headline and the numbers sharp and takes
   the levers and their reasons out of focus, so the slide can be put up before
   any of it is said and the count still reads.

   Class names are prefixed cp; neither shared sheet uses them.
   ========================================================================= */
@page { size: __W__px __H__px; margin: 0; }

.slide { position: relative; width: __W__px; height: __H__px; padding: 0;
         background: var(--ground); }

.cp__h {
  position: absolute; left: 110px; top: 50px; margin: 0;
  font-size: 56px; font-weight: 600; letter-spacing: -0.024em; color: var(--ink);
}
.cp__h i { font-style: normal; color: var(--blue); }

.cp__grid {
  position: absolute; left: 110px; top: 206px; width: 1700px;
  display: grid; grid-template-columns: repeat(3, 1fr); gap: 28px;
}

.cp__card {
  box-sizing: border-box; height: 318px;
  display: flex; flex-direction: column; justify-content: center;
  background: var(--surface); border: 1px solid var(--hairline);
  border-radius: 22px; padding: 28px 30px;
  box-shadow: 0 3px 16px rgba(20, 30, 50, 0.07);
}
.cp__n {
  display: flex; align-items: center; justify-content: center;
  width: 46px; height: 46px; flex: none; border-radius: 50%;
  font-size: 22px; font-weight: 700; letter-spacing: -0.01em; color: #fff;
}
.cp__t {
  margin: 20px 0 0;
  font-size: 33px; font-weight: 600; letter-spacing: -0.016em; line-height: 1.18;
  color: var(--ink);
}
.cp__b {
  margin: 15px 0 0;
  font-size: 25px; font-weight: 600; letter-spacing: -0.006em; line-height: 1.38;
  color: var(--ink-2);
}
.cp__b i { font-style: normal; color: var(--blue); }

/* the aside */
.cp__card--off { background: #EDEFF2; border-color: #DEE2E8; box-shadow: none; }
.cp__card--off .cp__t { color: var(--ink-2); }
.cp__card--off .cp__b { color: var(--ink-3); }

/* out of focus, but still the right shape and length */
.cp__t--blur { filter: blur(8px); }
.cp__b--blur { filter: blur(7px); }

/* one lever on its own */
.cp__one {
  position: absolute; left: 310px; top: 322px; width: 1300px; height: 434px;
  padding: 56px 64px;
}
.cp__one .cp__n { width: 68px; height: 68px; font-size: 32px; }
.cp__one .cp__t { margin-top: 30px; font-size: 62px; letter-spacing: -0.026em; }
.cp__one .cp__b { margin-top: 24px; font-size: 36px; line-height: 1.34; }
</style>
</head>
<body>

<!-- no-autofit: its own canvas, not a panel. -->
<section class="slide">

  <h1 class="cp__h">__HEAD__</h1>

__BODY__

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


def card(n, colour, lever, reason, blur=False, one=False):
    off = n == CARDS[-1][0]
    return ('    <div class="cp__card%s%s">'
            '<span class="cp__n" style="background:%s">%s</span>'
            '<p class="cp__t%s">%s</p>'
            '<p class="cp__b%s">%s</p></div>'
            % (' cp__card--off' if off else '', ' cp__one' if one else '',
               colour, n, ' cp__t--blur' if blur else '', lever,
               ' cp__b--blur' if blur else '', reason))


def write(path, body):
    open(path, 'w').write(TPL.replace('__W__', str(W)).replace('__H__', str(H))
                             .replace('__HEAD__', HEAD).replace('__BODY__', body))
    print('wrote %s' % path)


def grid(blur):
    return ('  <div class="cp__grid">\n'
            + '\n'.join(card(*c, blur=blur) for c in CARDS)
            + '\n  </div>')


write('slides/wide/wide-decrease-cpm.html', grid(False))
write('slides/wide/wide-decrease-cpm-blur.html', grid(True))

for c in CARDS:
    write('slides/wide/wide-decrease-cpm-%s.html' % c[0], card(*c, one=True))
