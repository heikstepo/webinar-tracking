#!/usr/bin/env python3
"""The worked example: one offer, two ICPs.

Every word is kept exactly as written, colons included. The hierarchy is done
with colour and weight inside the lines rather than by pulling the labels out
into chips, which would have meant dropping the colons and rewriting the lines
as fragments.

Each ICP is a label column beside a text column rather than one wrapped
paragraph, so when the longer line runs to two lines the second sits under the
text and not under the label.

    ./build-icp-example.py      writes both the panel and the 16:9 slide
"""
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

TITLE_KEY, TITLE_REST = 'Example:', 'SaaS Consulting Offer'
ROWS = [
    ('ICP 1:', 'Live SaaS, struggle with marketing and conversion'),
    ('ICP 2:', 'Close to Launching, no clear plan'),
]

TPL = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Example: SaaS Consulting Offer</title>
<link rel="stylesheet" href="__CSS__4pi.css">
<link rel="stylesheet" href="__CSS__voice-quiet.css">
<style>
/* ============================================================================
   See build-icp-example.py. Labels are emphasised in place rather than lifted
   out into chips, so the lines stay exactly as written.
   ========================================================================= */
@page { size: __W__px __H__px; margin: 0; }

.slide { width: __W__px; height: __H__px; padding: 90px __PX__px; background: var(--ground); }
__EDGE_CSS__
.ex { margin: 0; font-size: __TITLE__px; font-weight: 600; line-height: 1.2;
      letter-spacing: -0.016em; color: var(--ink); }
/* The framing word, quieter than the thing being framed. */
.ex__k { color: var(--ink-3); }

.exrule { width: 56px; height: 3px; border-radius: 2px; background: var(--blue);
          margin: __RULE__px auto; }

.icps { display: flex; flex-direction: column; gap: __RGAP__px;
        width: __COL__px; text-align: left; }

/* Label beside the text, not in front of it: the long line wraps under its own
   first word rather than under the label. */
.icprow { display: flex; gap: __KGAP__px; align-items: baseline;
          font-size: __BODY__px; font-weight: 500; line-height: 1.34;
          letter-spacing: -0.004em; color: var(--ink); }
.icprow__k { flex: none; font-weight: 600; color: var(--blue); }
</style>
</head>
<body>

__NOFIT__<section class="slide slide--center slide--mid">
__EDGE__
  <p class="ex"><span class="ex__k">__TK__</span> __TR__</p>

  <div class="exrule"></div>

  <div class="icps">
__ROWS__
  </div>

</section>

</body>
</html>
'''

ROW = ('    <div class="icprow"><span class="icprow__k">%s</span>'
       '<span>%s</span></div>')

EDGE_CSS = ('\n/* Full height hairline against the camera crop, as on every panel. */\n'
            '.edge { position: absolute; left: 0; top: 0; bottom: 0; width: 6px;'
            ' background: #B9C0C9; }\n')

VARIANTS = [
    dict(path='slides/icp-example.html', css='../', W=800, H=1080, PX=60,
         TITLE=44, RULE=44, RGAP=34, COL=640, KGAP=12, BODY=27,
         edge=True, nofit=''),
    dict(path='slides/wide/wide-icp-example.html', css='../../', W=1920, H=1080,
         PX=120, TITLE=72, RULE=64, RGAP=48, COL=1340, KGAP=18, BODY=44,
         edge=False,
         nofit='<!-- no-autofit: sized for 1920 here, and its text column is wider\n'
               '     than the panel column the fit pass would wrap it into. -->\n'),
]

rows = '\n'.join(ROW % r for r in ROWS)

for v in VARIANTS:
    out = TPL
    for k in ('W', 'H', 'PX', 'TITLE', 'RULE', 'RGAP', 'COL', 'KGAP', 'BODY'):
        out = out.replace('__%s__' % k, str(v[k]))
    out = (out.replace('__CSS__', v['css'])
              .replace('__EDGE_CSS__', EDGE_CSS if v['edge'] else '')
              .replace('__EDGE__', '  <div class="edge"></div>\n' if v['edge'] else '')
              .replace('__NOFIT__', v['nofit'])
              .replace('__TK__', TITLE_KEY).replace('__TR__', TITLE_REST)
              .replace('__ROWS__', rows))
    os.makedirs(os.path.dirname(v['path']), exist_ok=True)
    open(v['path'], 'w').write(out)
    print('wrote %s' % v['path'])
