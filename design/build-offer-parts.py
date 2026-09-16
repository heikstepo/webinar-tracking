#!/usr/bin/env python3
"""The offer, in its three parts.

Cards in a row with arrows between, because the note was written as a sequence
(core offer -> bonuses -> guarantee) rather than as a stack or a list.

Each part carries its own detail at two weights: what it is, and the tactical
note about how to do it, which is set in the accent so it reads as an
instruction rather than as more description. The guarantee has no detail to
carry, so it gets a mark instead of body text. That asymmetry is deliberate:
it is the one part that needs no explaining, and padding it out with invented
copy would be the wrong fix.

    ./build-offer-parts.py      writes the 16:9 slide and the vertical card
"""
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

HEADLINE = 'Offer'

SHIELD = '''<svg viewBox="0 0 124 124" aria-hidden="true">
          <path d="M62 14 L104 31 V 62 C 104 86, 84 103, 62 111
                   C 40 103, 20 86, 20 62 V 31 Z"/>
          <path class="hot" d="M44 62 L56 74 L82 46"/>
        </svg>'''

PARTS = [
    ('01', 'Core offer',
     'Expected essentials<br>(course, community, coaching)',
     'Explain in 3-5 minutes', ''),
    ('02', 'Bonuses',
     '3-5 surprising extras that<br>overcome objections',
     'Second best first, best last.', ''),
    ('03', 'Guarantee', '', '', SHIELD),
]

ARROW = '''    <div class="arr">
      <svg viewBox="0 0 54 26" aria-hidden="true">
        <g fill="none" stroke="#0071E3" stroke-width="4" stroke-linecap="round" stroke-linejoin="round">
          <path d="M4 13 H 40"/><path d="M32 4 L 50 13 L 32 22"/>
        </g>
      </svg>
    </div>'''

ARROW_DOWN = '''    <div class="arr">
      <svg viewBox="0 0 26 54" aria-hidden="true">
        <g fill="none" stroke="#0071E3" stroke-width="4" stroke-linecap="round" stroke-linejoin="round">
          <path d="M13 4 V 40"/><path d="M4 32 L 13 50 L 22 32"/>
        </g>
      </svg>
    </div>'''

CARD = '''    <div class="card">
      <span class="card__n">%s</span>
      <h3 class="card__t">%s</h3>
      %s
    </div>'''

TPL = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Offer</title>
<link rel="stylesheet" href="__CSS__4pi.css">
<link rel="stylesheet" href="__CSS__voice-quiet.css">
<style>
/* ============================================================================
   See build-offer-parts.py. Three cards in sequence; the guarantee carries a
   mark instead of body copy because it is the one part that needs no
   explaining.
   ========================================================================= */
@page { size: __W__px __H__px; margin: 0; }

.slide { width: __W__px; height: __H__px; padding: __PY__px __PX__px; background: var(--ground); }

.hl {
  margin: 0 0 __HGAP__px;
  font-size: __HL__px; font-weight: 600; letter-spacing: -0.022em; color: var(--ink);
}

/* Explicit width on the stacked version: the slide centres its children,
   so a row left to size itself shrinks to its content and the cards stop
   short of the card's own margins. */
.row { display: flex; __DIR__ align-items: stretch; justify-content: center;
       gap: __GAP__px; __ROWW__ }

.card {
  __CARDW__
  background: var(--surface);
  border: 1px solid var(--hairline);
  border-radius: 24px;
  padding: __CPAD__;
  text-align: left;
  display: flex; flex-direction: column;
}

/* Ghosted, so it orders the parts without competing with their names. */
.card__n {
  display: block;
  font-size: __NUM__px; font-weight: 700; line-height: 1;
  letter-spacing: -0.03em; color: #D3DDE9;
}
.card__t {
  margin: __TGAP__px 0 0;
  font-size: __TITLE__px; font-weight: 600; letter-spacing: -0.012em; color: var(--ink);
}
.card__b {
  margin: __BGAP__px 0 0;
  font-size: __BODY__px; font-weight: 500; line-height: 1.34; color: var(--ink-2);
}
/* The how-to line, in the accent: an instruction, not more description. */
.card__note {
  margin: auto 0 0;
  padding-top: __BGAP__px;
  font-size: __NOTE__px; font-weight: 600; letter-spacing: -0.004em; color: var(--blue);
}

.card__art { margin: auto 0 0; padding-top: __BGAP__px; }
.card__art svg {
  display: block; width: __SH__px; height: __SH__px;
  fill: none; stroke: #7FA8DC; stroke-width: 2.6;
  stroke-linecap: round; stroke-linejoin: round;
}
.card__art svg .hot { stroke: var(--blue); stroke-width: 4; }

.arr { flex: none; display: flex; align-items: center; }
.arr svg { display: block; __ARRW__ }
</style>
</head>
<body>

<!-- no-autofit: its own canvas, not a panel. -->
<section class="slide slide--center slide--mid">

  <p class="hl">__HEADLINE__</p>

  <div class="row">
__CARDS__
  </div>

</section>

</body>
</html>
'''

VARIANTS = [
    dict(path='slides/wide/wide-offer-parts.html', css='../../',
         W=1920, H=1080, PX=110, PY=90, HL=88, HGAP=62, GAP=34,
         dir='', roww='', cardw='width: 470px;', cpad='40px 42px 42px',
         NUM=52, TGAP=18, TITLE=44, BGAP=20, BODY=28, NOTE=26, SH=132,
         arrw='width: 54px; height: 26px;', arrow=ARROW),
    dict(path='slides/vert-offer-parts.html', css='../',
         W=1080, H=1400, PX=80, PY=70, HL=86, HGAP=48, GAP=24,
         dir='flex-direction: column;', roww='width: 920px;', cardw='width: 100%;',
         cpad='34px 40px 38px',
         NUM=46, TGAP=14, TITLE=44, BGAP=16, BODY=30, NOTE=28, SH=96,
         arrw='width: 26px; height: 54px; margin: 0 auto;', arrow=ARROW_DOWN),
]

for v in VARIANTS:
    cards = []
    for n, title, body, note, art in PARTS:
        inner = ''
        if body:
            inner = '<p class="card__b">%s</p>\n      ' % body
            inner += '<p class="card__note">%s</p>' % note
        else:
            inner = '<div class="card__art">%s</div>' % art
        cards.append(CARD % (n, title, inner))
    row = ('\n' + v['arrow'] + '\n').join(cards)

    out = TPL
    for k in ('W', 'H', 'PX', 'PY', 'HL', 'HGAP', 'GAP', 'NUM', 'TGAP',
              'TITLE', 'BGAP', 'BODY', 'NOTE', 'SH'):
        out = out.replace('__%s__' % k, str(v[k]))
    for k in ('CSS', 'DIR', 'ROWW', 'CARDW', 'CPAD', 'ARRW'):
        out = out.replace('__%s__' % k, v[k.lower()])
    out = out.replace('__HEADLINE__', HEADLINE).replace('__CARDS__', row)
    os.makedirs(os.path.dirname(v['path']), exist_ok=True)
    open(v['path'], 'w').write(out)
    print('wrote %s' % v['path'])
