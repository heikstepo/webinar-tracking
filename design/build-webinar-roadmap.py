#!/usr/bin/env python3
"""The webinar funnel, as a road with twenty stops.

Serpentine rather than one line: twenty stops across 1920px would leave each
one about ninety pixels of label, and these labels are sentences. Four rows
that double back keep the road continuous and give every stop real width.

Three stops are set apart from the rest. The live webinar is the only thing
the operator is in each week, so it gets the accent and carries that note.
The unqualified branch is grey, because it is the way out of the funnel
rather than a step along it. The closed deal is the green this deck uses for
a sale everywhere else.

    ./build-webinar-roadmap.py    writes the 16:9 slide
"""
import os
import re

os.chdir(os.path.dirname(os.path.abspath(__file__)))

W, H = 1920, 1080

# (label, note, kind) in the order given. kind: '' | 'key' | 'off' | 'end'
STOPS = [
    ('Ads', 'starting 3 days out', ''),
    ('Opt-in Page', '', ''),
    ('OTO Purchase', '', ''),
    ('Opt-in Confirmation Page', '', ''),
    ('Pre-Webinar Emails', '', ''),
    ('YouTube Videos', '', ''),
    ('Telegram Nurture', '', ''),
    ('SMS Nurture', '', ''),
    ('Pre-Webinar Nurture Ads', '', ''),
    ('Live Webinar Presentation', 'the only thing you&rsquo;re in each week', 'key'),
    ('Applied &amp; Unqualified', '&rarr; Downsell', 'off'),
    ('Applied &amp; Qualified', '&rarr; Booked Call', ''),
    ('Call Confirmation Page', '', ''),
    ('Pre-Call Emails', '', ''),
    ('Setters Reaching Out', '', ''),
    ('YouTube Nurture', '', ''),
    ('SMS Nurture', '', ''),
    ('Pre-Call Ads', '', ''),
    ('Sales Call with Closer', '', ''),
    ('Closed Deal', '', 'end'),
]

COLS = [290, 620, 950, 1280, 1610]
ROWS = [216, 438, 660, 882]
R = 50                       # corner radius of the turns
OUT_R, OUT_L = 1790, 110     # where the road turns, clear of the labels

# Pale to full across the twenty. Generated rather than listed so every disc
# is dark enough to carry a white numeral, which a hand-written ramp was not.
def ramp(n, a=(0x8F, 0xC0, 0xF5), b=(0x00, 0x71, 0xE3)):
    out = []
    for i in range(n):
        t = i / (n - 1)
        out.append('#%02X%02X%02X' % tuple(round(a[c] + (b[c] - a[c]) * t)
                                           for c in range(3)))
    return out


RAMP = ramp(len(STOPS))

TPL = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Webinar Funnel</title>
<link rel="stylesheet" href="../../4pi.css">
<link rel="stylesheet" href="../../voice-quiet.css">
<style>
/* ============================================================================
   See build-webinar-roadmap.py. One road, doubling back four times, because
   twenty stops in a line leaves no room for labels that are sentences.

   Class names are prefixed rm; neither shared sheet uses them.
   ========================================================================= */
@page { size: __W__px __H__px; margin: 0; }

.slide { position: relative; width: __W__px; height: __H__px; padding: 0;
         background: var(--ground); }

.rm__h {
  position: absolute; left: 110px; top: 44px; margin: 0;
  font-size: 54px; font-weight: 600; letter-spacing: -0.022em; color: var(--ink);
}

/* The road itself, under the stops so it runs into the discs. */
.rm__road { position: absolute; inset: 0; }
.rm__road svg { display: block; width: 100%; height: 100%; }
.rm__road .lane { fill: none; stroke: #D2D8E0; stroke-width: 7;
                  stroke-linecap: round; stroke-linejoin: round; }
.rm__road .tip { fill: #BAC3CF; }

.rm__stop {
  position: absolute; width: 290px; transform: translateX(-50%);
  text-align: center;
}
.rm__n {
  display: flex; align-items: center; justify-content: center;
  width: 54px; height: 54px; margin: 0 auto; border-radius: 50%;
  border: 4px solid var(--ground);
  font-size: 23px; font-weight: 700; letter-spacing: -0.01em; color: #fff;
}
.rm__t {
  margin: 10px 0 0;
  font-size: 21px; font-weight: 600; letter-spacing: -0.008em; line-height: 1.22;
  color: var(--ink);
}
.rm__note {
  margin: 5px 0 0;
  font-size: 17px; font-weight: 600; line-height: 1.2; color: var(--ink-3);
}

/* The one week-by-week commitment. */
.rm__stop--key .rm__n { width: 64px; height: 64px; font-size: 26px;
                        box-shadow: 0 0 0 4px #BFD6F7; }
.rm__stop--key .rm__t { color: var(--blue); }
.rm__stop--key .rm__note { color: #4A8BD6; }

/* The way out of the funnel, not a step along it. */
.rm__stop--off .rm__n { background: #AEB8C6 !important; }
.rm__stop--off .rm__t,
.rm__stop--off .rm__note { color: var(--ink-3); }

/* The sale. */
.rm__stop--end .rm__n { background: #34A518 !important; }
.rm__stop--end .rm__t { color: #248A13; }
</style>
</head>
<body>

<section class="slide">

  <h1 class="rm__h">Webinar Funnel</h1>

  <div class="rm__road">
    <svg viewBox="0 0 __W__ __H__" aria-hidden="true">
      <path class="lane" d="__PATH__"/>
__TIPS__
    </svg>
  </div>

__STOPS__

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

# ---- the road -------------------------------------------------------------
y0, y1, y2, y3 = ROWS
path = (
    'M %d %d H %d A %d %d 0 0 1 %d %d V %d A %d %d 0 0 1 %d %d '
    'H %d A %d %d 0 0 0 %d %d V %d A %d %d 0 0 0 %d %d '
    'H %d A %d %d 0 0 1 %d %d V %d A %d %d 0 0 1 %d %d H %d'
    % (COLS[0], y0, OUT_R - R, R, R, OUT_R, y0 + R,
       y1 - R, R, R, OUT_R - R, y1,
       OUT_L + R, R, R, OUT_L, y1 + R,
       y2 - R, R, R, OUT_L + R, y2,
       OUT_R - R, R, R, OUT_R, y2 + R,
       y3 - R, R, R, OUT_R - R, y3, COLS[0]))

tips = []
for i, y in enumerate(ROWS):
    # Between the first two stops of the row, so it never lands on a disc.
    x, a = (455, 0) if i % 2 == 0 else (1445, 180)
    tips.append('      <g transform="translate(%d %d) rotate(%d)">'
                '<path class="tip" d="M0 0 L -22 -11 L -22 11 Z"/></g>' % (x, y, a))

# ---- the stops ------------------------------------------------------------
stops = []
for i, (label, note, kind) in enumerate(STOPS):
    row = i // 5
    col = i % 5 if row % 2 == 0 else 4 - (i % 5)
    x, y = COLS[col], ROWS[row]
    cls = ' rm__stop--%s' % kind if kind else ''
    top = y - (32 if kind == 'key' else 27)
    stops.append(
        '  <div class="rm__stop%s" style="left:%dpx; top:%dpx">'
        '<span class="rm__n" style="background:%s">%d</span>'
        '<p class="rm__t">%s</p>%s</div>'
        % (cls, x, top, RAMP[i], i + 1, label,
           '<p class="rm__note">%s</p>' % note if note else ''))

out = (TPL.replace('__W__', str(W)).replace('__H__', str(H))
          .replace('__PATH__', path)
          .replace('__TIPS__', '\n'.join(tips))
          .replace('__STOPS__', '\n'.join(stops)))

path_out = 'slides/wide/wide-webinar-roadmap.html'
open(path_out, 'w').write(out)
print('wrote %s' % path_out)
