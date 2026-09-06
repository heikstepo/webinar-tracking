#!/usr/bin/env python3
"""Redraw the Webinar Funnel map in the house style.

Every step and every word is carried over from the original diagram unchanged;
only the drawing is new. The one structural liberty is that the flow is folded
into two tiers instead of one very long row — at one row the labels have to
shrink to about a third of a percent of the canvas width to fit, which is why
the original is hard to read. Folded, the type can be nearly three times that.
"""
import math

W, H, PAD = 2400, 1700, 70
INK, INK2, INK3 = '#1B1D20', '#5A5E66', '#8A9099'
LINE, PANEL, PANEL_EDGE = '#E3E5E8', '#EFF3F9', '#DCE4EF'
FLOW, PIX, PIX_INK = '#0071E3', '#F2A3AE', '#E31D3E'

box, panel, tile, label, sub, head = [], [], [], [], [], []
paths = []


def rpath(pts, r=16):
    """A polyline with rounded corners. Right-angle elbows are what make a
    routed diagram readable; mitred ones read as folds in the paper."""
    d = 'M %g %g' % pts[0]
    for i in range(1, len(pts) - 1):
        (px, py), (x, y), (nx, ny) = pts[i - 1], pts[i], pts[i + 1]
        a = math.hypot(x - px, y - py); b = math.hypot(nx - x, ny - y)
        ra = min(r, a / 2, b / 2)
        d += ' L %g %g' % (x - (x - px) / a * ra, y - (y - py) / a * ra)
        d += ' Q %g %g %g %g' % (x, y, x + (nx - x) / b * ra, y + (ny - y) / b * ra)
    d += ' L %g %g' % pts[-1]
    return d


def arrow(pts, color=FLOW, w=2.6, head=True, r=16):
    mk = ' marker-end="url(#ah)"' if color == FLOW else ' marker-end="url(#ap)"'
    paths.append('<path d="%s" fill="none" stroke="%s" stroke-width="%g" '
                 'stroke-linecap="round" stroke-linejoin="round"%s/>'
                 % (rpath(pts, r), color, w, mk if head else ''))


def B(x, y, w, h, text, note=None):
    box.append('<div class="bx" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx">'
               '<span>%s</span>%s</div>'
               % (x, y, w, h, text, '<i>%s</i>' % note if note else ''))


def L(x, y, w, text, color=INK2, size=17, align='center'):
    label.append('<p class="lb" style="left:%dpx;top:%dpx;width:%dpx;color:%s;'
                 'font-size:%dpx;text-align:%s">%s</p>' % (x, y, w, color, size, align, text))


def SYSTEM(x, y, w, title, items, cols=2, th=76, gap=14, pad=22):
    rows = (len(items) + cols - 1) // cols
    h = rows * th + (rows - 1) * gap + pad * 2
    head.append('<p class="hd" style="left:%dpx;top:%dpx;width:%dpx">%s</p>'
                % (x, y - 44, w, title))
    panel.append('<div class="pn" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx"></div>'
                 % (x, y, w, h))
    cw = (w - pad * 2 - gap * (cols - 1)) // cols
    for i, it in enumerate(items):
        c, r = i % cols, i // cols
        tile.append('<div class="tl" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx">%s</div>'
                    % (x + pad + c * (cw + gap), y + pad + r * (th + gap), cw, th, it))
    return h


# ── the traffic source ────────────────────────────────────────────────────────
# The Meta mark drawn as a true lemniscate rather than pasted as a logo file:
# it is the one thing on the map that is a brand and not a step.
META = ('<svg viewBox="0 0 28 16"><path d="M6 8 C6 5.2 8 3.5 10 3.5 C13 3.5 14.5 12.5 17.5 12.5 '
        'C19.5 12.5 21.5 10.8 21.5 8 C21.5 5.2 19.5 3.5 17.5 3.5 C14.5 3.5 13 12.5 10 12.5 '
        'C8 12.5 6 10.8 6 8 Z"/></svg>')
MX, MY, MW, MH = 70, 300, 214, 300
src = ['<div class="src" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx">' % (MX, MY, MW, MH)]
for r in range(6):
    for c in range(5):
        src.append('<span style="left:%dpx;top:%dpx">%s</span>'
                   % (18 + c * 35, 18 + r * 41, META))
src.append('</div>')

# ── tier 1 ────────────────────────────────────────────────────────────────────
B(570, 265, 210, 70, 'Webinar Opt-In Page')
B(840, 265, 180, 70, 'Order Bump')
B(1080, 178, 220, 86, 'Thank You Page A', '[upsell]')
B(1080, 298, 220, 86, 'Thank you Page B', '[no upsell]')
B(570, 605, 210, 70, 'Webinar Opt-In Page')
B(840, 605, 240, 70, 'Webinar Confirmation Page')
L(380, 262, 200, 'With Order Bump', INK, 18)
L(380, 602, 200, 'No Order Bump', INK, 18)

SYSTEM(1380, 240, 440, 'Pre-Webinar Education System',
       ['Pre-Webinar Email Sequence', 'Retargeting Ads',
        'YouTube Nurturing', 'SMS Blasts',
        'Telegram', 'Lead Magnet'], th=84, gap=18)

box.append('<div class="bx bx--pill" style="left:1880px;top:371px;width:220px;height:72px">'
           '<span>Webinar Execution</span></div>')
B(2150, 371, 180, 72, 'Booked Call')

arrow([(MX + MW, 450), (335, 450), (335, 300), (562, 300)])
arrow([(MX + MW, 450), (335, 450), (335, 640), (562, 640)])
arrow([(780, 300), (832, 300)], r=0)
arrow([(1020, 300), (1050, 300), (1050, 221), (1072, 221)])
arrow([(1020, 300), (1050, 300), (1050, 341), (1072, 341)])
arrow([(1300, 221), (1340, 221), (1340, 330), (1372, 330)])
arrow([(1300, 341), (1340, 341), (1340, 360), (1372, 360)])
arrow([(780, 640), (832, 640)], r=0)
arrow([(1080, 640), (1200, 640), (1200, 470), (1372, 470)])
arrow([(1820, 406), (1872, 406)], r=0)
arrow([(2100, 407), (2142, 407)], r=0)

# Reports back to Pixel — the two loops that make this a closed system rather
# than a one-way chart, so they get their own colour and stay off the flow.
arrow([(1190, 178), (1190, 150), (177, 150), (177, 292)], PIX, 3)
arrow([(960, 675), (960, 732), (177, 732), (177, 608)], PIX, 3)
L(560, 116, 460, 'Reports back to Pixel', PIX_INK, 18)
L(360, 700, 460, 'Reports back to Pixel', PIX_INK, 18)

# ── the fold ──────────────────────────────────────────────────────────────────
arrow([(2240, 443), (2240, 800), (470, 800), (470, 872)], r=22)

# ── tier 2 ────────────────────────────────────────────────────────────────────
SYSTEM(70, 880, 460, 'Back-End Education System',
       ['Pre-Framing confirmation page', 'SDR Process',
        'Retargeting Ads', '15 Long-Form Pre-Call Emails',
        'Text Reminders', 'Puzzle-Youtube Channel',
        'Pre-Call Sales Assets', 'Text SDR Process'])

B(620, 1039, 200, 72, 'Show Call')
B(1080, 1039, 200, 72, 'Closed Deal')
B(1460, 1039, 200, 72, 'Case Study')
B(1840, 1039, 220, 72, 'Referral System')

SYSTEM(620, 1330, 460, 'No-Close Follow-Up System',
       ['Manual SDR Follow-Up', 'Post-Call Emails',
        'YouTube', 'Sales Assets',
        'Close-Up Calls', 'Conversation with clients'])

arrow([(530, 1075), (612, 1075)], r=0)
arrow([(820, 1075), (1072, 1075)], r=0)
arrow([(1280, 1075), (1452, 1075)], r=0)
arrow([(1660, 1075), (1832, 1075)], r=0)
arrow([(720, 1111), (720, 1322)], r=0)
arrow([(1080, 1480), (1190, 1480), (1190, 1119)])
L(820, 1042, 260, '1-call-close')
L(742, 1190, 200, 'No Close', INK2, 17, 'left')
L(1210, 1290, 220, '2-call-close', INK2, 17, 'left')

HTML = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Webinar Funnel</title>
<link rel="stylesheet" href="../4pi.css">
<link rel="stylesheet" href="../voice-quiet.css">
<style>
/* A map, not a slide: the canvas is sized to the diagram. */
@page { size: __W__px __H__px; margin: 0; }
.slide { width: __W__px; height: __H__px; padding: 0; display: block; }

.map { position: relative; width: __W__px; height: __H__px; }
.map svg.links { position: absolute; inset: 0; width: 100%; height: 100%; }

.ttl { position: absolute; left: 70px; top: 54px; margin: 0;
       font-size: 46px; font-weight: 600; letter-spacing: -0.014em; color: var(--ink); }

/* A single step. White, because the systems behind them are tinted — the
   contrast is what separates one action from a bundle of them. */
.bx { position: absolute; background: #fff; border: 1px solid #E1E5EA;
      border-radius: 14px; box-shadow: 0 2px 6px rgba(20,25,35,.06);
      display: flex; flex-direction: column; align-items: center;
      justify-content: center; text-align: center; padding: 0 16px; }
.bx span { font-size: 20px; font-weight: 600; letter-spacing: -0.004em;
           line-height: 1.24; color: var(--ink); }
.bx i { font-style: normal; margin-top: 5px; font-size: 15px; color: #8A9099; }
.bx--pill { border-radius: 999px; }

/* A system: several things that happen together, so they get one container
   and a tint, and the steps stay white. */
.pn { position: absolute; background: __PANEL__; border: 1px solid __PEDGE__;
      border-radius: 20px; }
.hd { position: absolute; margin: 0; font-size: 24px; font-weight: 600;
      letter-spacing: -0.008em; color: var(--ink); }
.tl { position: absolute; background: #fff; border: 1px solid #E4E9F0;
      border-radius: 11px; display: flex; align-items: center;
      justify-content: center; text-align: center; padding: 0 14px;
      font-size: 17px; font-weight: 500; line-height: 1.26; color: var(--ink); }

.lb { position: absolute; margin: 0; font-weight: 600; letter-spacing: -0.002em; }

.src { position: absolute; background: #fff; border: 1px solid #E1E5EA;
       border-radius: 16px; box-shadow: 0 2px 6px rgba(20,25,35,.06); }
.src span { position: absolute; display: block; width: 28px; height: 16px; }
.src svg { width: 28px; height: 16px; fill: none; stroke: #1877F2; stroke-width: 1.7; }
</style>
</head>
<body>

<section class="slide">
  <div class="map">

    <p class="ttl">Webinar Funnel</p>

    <svg class="links" viewBox="0 0 __W__ __H__" fill="none" aria-hidden="true">
      <defs>
        <marker id="ah" viewBox="0 0 10 10" refX="7.5" refY="5" markerWidth="5.5"
                markerHeight="5.5" orient="auto">
          <path d="M0.5 0.5 L9 5 L0.5 9.5" fill="none" stroke="__FLOW__"
                stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </marker>
        <marker id="ap" viewBox="0 0 10 10" refX="7.5" refY="5" markerWidth="5.5"
                markerHeight="5.5" orient="auto">
          <path d="M0.5 0.5 L9 5 L0.5 9.5" fill="none" stroke="__PIX__"
                stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
        </marker>
      </defs>
      __PATHS__
    </svg>

__SRC__
__PANELS__
__HEADS__
__TILES__
__BOXES__
__LABELS__

  </div>
</section>

</body>
</html>
'''

out = (HTML.replace('__W__', str(W)).replace('__H__', str(H))
           .replace('__PANEL__', PANEL).replace('__PEDGE__', PANEL_EDGE)
           .replace('__FLOW__', FLOW).replace('__PIX__', PIX)
           .replace('__PATHS__', '\n      '.join(paths))
           .replace('__SRC__', '    ' + ''.join(src))
           .replace('__PANELS__', '\n'.join('    ' + p for p in panel))
           .replace('__HEADS__', '\n'.join('    ' + p for p in head))
           .replace('__TILES__', '\n'.join('    ' + p for p in tile))
           .replace('__BOXES__', '\n'.join('    ' + p for p in box))
           .replace('__LABELS__', '\n'.join('    ' + p for p in label)))
open('slides/webinar-funnel.html', 'w').write(out)
print('wrote slides/webinar-funnel.html')
