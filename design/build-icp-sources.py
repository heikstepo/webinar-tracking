#!/usr/bin/env python3
"""ICP, over the three places we go looking for it.

The marks are the real ones, kept in design/logos and inlined here, so nothing
is redrawn from memory and nothing is fetched at build time.

They are set in one ink rather than in brand colour. Reddit orange, YouTube red
and Fathom cyan together would be three loud colours fighting the quiet blue and
grey everything else in this deck is built from, and the slide is about where we
look, not about the brands. Monochrome is also the treatment each of these
companies' own brand guidelines allow for exactly this use.

Note on Fathom: simple-icons ships a "Fathom" icon that belongs to Fathom
Analytics, a different company. The mark used here is the one from fathom.video,
the meeting notetaker.

    ./build-icp-sources.py      writes both the panel and the 16:9 slide
"""
import os
import re

os.chdir(os.path.dirname(os.path.abspath(__file__)))

LOGOS = [('fathom', 'Fathom'), ('reddit', 'Reddit'), ('youtube', 'YouTube')]


def mark(slug):
    """The logo as a single-colour <svg>, sized by CSS.

    Fills are stripped rather than overridden so a brand colour cannot survive
    in a nested element, and the drawing takes the colour set on the tile.
    """
    src = open('logos/%s.svg' % slug).read()
    box = re.search(r'viewBox="([^"]+)"', src).group(1)
    body = src[src.index('>', src.index('<svg')) + 1:src.rindex('</svg>')]
    body = re.sub(r'\s*fill="[^"]*"', '', body)
    return ('<svg viewBox="%s" fill="currentColor" aria-hidden="true">%s</svg>'
            % (box, body.strip()))


TPL = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>ICP</title>
<link rel="stylesheet" href="__CSS__4pi.css">
<link rel="stylesheet" href="__CSS__voice-quiet.css">
<style>
/* ============================================================================
   The word, then the three places. See build-icp-sources.py for why the marks
   are set in one ink rather than in brand colour.

   The marks are optically sized rather than boxed to a common width: Reddit is
   a circle, YouTube a wide rounded rectangle and Fathom a tall stack, so three
   equal boxes would leave YouTube looking twice the size of the others. Each is
   scaled until it carries the same weight on the page.
   ========================================================================= */
@page { size: __W__px __H__px; margin: 0; }

.slide { width: __W__px; height: __H__px; padding: 90px __PX__px; background: var(--ground); }
__EDGE_CSS__
.icp { margin: 0 0 __GAP__px; font-size: __TITLE__px; font-weight: 600;
       letter-spacing: -0.02em; color: var(--ink); }

.srcs { display: flex; align-items: center; justify-content: center; gap: __SGAP__px; }

.src { display: flex; flex-direction: column; align-items: center; }
/* Fixed-height row for the marks. Without it each column is only as tall as
   its own logo, and since a circle, a wide rectangle and a tall stack are all
   different heights, the three captions end up on three different lines. */
.src__mark { height: __MH__px; display: flex; align-items: center; justify-content: center; }
.src svg { display: block; color: var(--ink); }
.src__name { margin: __NGAP__px 0 0; font-size: __NAME__px; font-weight: 600;
             letter-spacing: -0.004em; color: var(--ink-2); }

/* Optical sizing, per mark. */
.src--fathom  svg { width: __M1__px; height: __M1__px; }
.src--reddit  svg { width: __M2__px; height: __M2__px; }
.src--youtube svg { width: __M3__px; height: __M3__px; }
</style>
</head>
<body>

__NOFIT__<section class="slide slide--center slide--mid">
__EDGE__
  <p class="icp">ICP</p>

  <div class="srcs">
__SRCS__
  </div>

</section>

</body>
</html>
'''

SRC = '''    <div class="src src--%s">
      <div class="src__mark">%s</div>
      <p class="src__name">%s</p>
    </div>'''

EDGE_CSS = ('\n/* Full height hairline against the camera crop, as on every panel. */\n'
            '.edge { position: absolute; left: 0; top: 0; bottom: 0; width: 6px;'
            ' background: #B9C0C9; }\n')

VARIANTS = [
    # panel
    dict(path='slides/icp-sources.html', css='../', W=800, H=1080, PX=60,
         TITLE=62, GAP=70, SGAP=54, NAME=21, NGAP=20,
         M1=92, M2=85, M3=87, MH=100, edge=True, nofit=''),
    # 16:9
    dict(path='slides/wide/wide-icp-sources.html', css='../../', W=1920, H=1080,
         PX=120, TITLE=104, GAP=104, SGAP=140, NAME=30, NGAP=28,
         M1=150, M2=138, M3=142, MH=160, edge=False,
         nofit='<!-- no-autofit: sized for 1920 here, and its row is wider than\n'
               '     the panel text column the fit pass would wrap it into. -->\n'),
]

srcs = '\n'.join(SRC % (slug, mark(slug), name) for slug, name in LOGOS)

for v in VARIANTS:
    out = TPL
    for k in ('W', 'H', 'PX', 'TITLE', 'GAP', 'SGAP', 'NAME', 'NGAP',
              'M1', 'M2', 'M3', 'MH'):
        out = out.replace('__%s__' % k, str(v[k]))
    out = (out.replace('__CSS__', v['css'])
              .replace('__EDGE_CSS__', EDGE_CSS if v['edge'] else '')
              .replace('__EDGE__', '  <div class="edge"></div>\n' if v['edge'] else '')
              .replace('__NOFIT__', v['nofit'])
              .replace('__SRCS__', srcs))
    os.makedirs(os.path.dirname(v['path']), exist_ok=True)
    open(v['path'], 'w').write(out)
    print('wrote %s' % v['path'])
