#!/usr/bin/env python3
"""The five awareness levels, for an ecom offer.

On the widescreen slide the cards climb: each level sits higher than the one
before it, so the rise itself says these are levels rather than five topics in
a row. The number chips run the same pale to full blue ramp used elsewhere for
one quantity increasing.

Level one has no description, and is left without one. It is the only level
defined by absence, and writing a sentence to fill the box would be inventing
copy to balance a layout.

    ./build-awareness-levels.py   writes the 16:9 slide and the vertical card
"""
import os
import re

os.chdir(os.path.dirname(os.path.abspath(__file__)))

LEVELS = [
    ('Unaware of the Ecom', '', '#C5DDFA'),
    ('Curious but Skeptical',
     'Has heard about ecom and seen the success stories, but isn&rsquo;t sure '
     'it&rsquo;s real or right for them.', '#A7CCF7'),
    ('Actively Researching',
     'Consuming content, comparing models, trying to find the right way in.',
     '#7CB2F3'),
    ('Started and Struggling',
     'Has launched a store and spent money, but isn&rsquo;t getting consistent '
     'sales or profit.', '#4A97EF'),
    ('Profitable but Plateaued',
     'Making money, but hitting a ceiling on scaling and needs systems or '
     'expert help to break through.', '#0071E3'),
]

TPL = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Awareness levels</title>
<link rel="stylesheet" href="__CSS__4pi.css">
<link rel="stylesheet" href="__CSS__voice-quiet.css">
<style>
/* ============================================================================
   See build-awareness-levels.py. The cards climb so the rise says "levels",
   and the chips ramp pale to full because it is one quantity increasing.
   ========================================================================= */
@page { size: __W__px __H__px; margin: 0; }

.slide { width: __W__px; height: __H__px; padding: __PY__px __PX__px; background: var(--ground); }

.awl { display: flex; __DIR__ gap: __GAP__px; __ALIGN__ }

.awl__card {
  __CARDW__
  background: var(--surface);
  border: 1px solid var(--hairline);
  border-radius: 22px;
  padding: __CPAD__;
  text-align: left;
}

.awl__n {
  display: flex; align-items: center; justify-content: center;
  width: __CHIP__px; height: __CHIP__px; border-radius: 50%;
  font-size: __NUM__px; font-weight: 700; color: #fff;
}
.awl__t {
  margin: __TGAP__px 0 0;
  font-size: __TITLE__px; font-weight: 600; letter-spacing: -0.01em;
  line-height: 1.2; color: var(--ink);
}
.awl__b {
  margin: __BGAP__px 0 0;
  font-size: __BODY__px; font-weight: 500; line-height: 1.36; color: var(--ink-2);
}
</style>
</head>
<body>

<!-- no-autofit: its own canvas, not a panel. -->
<section class="slide slide--center slide--mid">

  <div class="awl">
__CARDS__
  </div>

</section>

</body>
</html>
'''

CARD = '''    <div class="awl__card"__STYLE__>
      <span class="awl__n" style="background:%s">%d</span>
      <h3 class="awl__t">%s</h3>
      %s
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

VARIANTS = [
    # 16:9 — five across, each one standing higher than the last.
    dict(path='slides/wide/wide-awareness-levels.html', css='../../',
         W=1920, H=1080, PX=110, PY=90, GAP=28,
         dir='', align='align-items: flex-end;',
         cardw='width: 308px; height: 372px;', cpad='30px 30px 34px',
         CHIP=56, NUM=28, TGAP=22, TITLE=32, BGAP=16, BODY=22,
         rise=46),
    # vertical — five down. No climb here: the stack already runs downward, and
    # indenting each card would only cost width the copy needs.
    dict(path='slides/vert-awareness-levels.html', css='../',
         W=1080, H=1500, PX=70, PY=70, GAP=22,
         dir='flex-direction: column;', align='align-items: stretch;',
         cardw='width: 940px;', cpad='28px 34px 32px',
         CHIP=54, NUM=27, TGAP=18, TITLE=38, BGAP=12, BODY=26,
         rise=0),
]

for v in VARIANTS:
    cards = []
    for i, (title, body, chip) in enumerate(LEVELS):
        style = (' style="margin-bottom:%dpx"' % (i * v['rise'])) if v['rise'] else ''
        b = '<p class="awl__b">%s</p>' % body if body else ''
        cards.append(CARD.replace('__STYLE__', style) % (chip, i + 1, title, b))

    out = TPL
    for k in ('W', 'H', 'PX', 'PY', 'GAP', 'CHIP', 'NUM', 'TGAP',
              'TITLE', 'BGAP', 'BODY'):
        out = out.replace('__%s__' % k, str(v[k]))
    for k in ('CSS', 'DIR', 'ALIGN', 'CARDW', 'CPAD'):
        out = out.replace('__%s__' % k, v[k.lower()])
    out = out.replace('__CARDS__', '\n\n'.join(cards))
    os.makedirs(os.path.dirname(v['path']), exist_ok=True)
    open(v['path'], 'w').write(out)
    print('wrote %s' % v['path'])
