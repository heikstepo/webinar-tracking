#!/usr/bin/env python3
"""Number the whole VSL run so a slide can be found by its position.

The running order is not written out again here. It is read from the two
generators that already own it, with the case study panels spliced in at the
point where they are spoken, so adding or reordering a panel in the generator
renumbers the run and nothing has to be kept in step by hand.

Copies rather than moves: every other script, and the rendered exports
themselves, still refer to slides by slug, so the slug-named files stay where
they are and the numbered set is an additional view of them.

    ./number-run.py            writes exports/run/NN-slug.png
"""
import os
import re
import shutil

os.chdir(os.path.dirname(os.path.abspath(__file__)))

OUT = 'exports/run'

# The case studies answer "here are some of the results we've seen", so they
# run immediately after that panel and before the reason for the offer.
AFTER = 'here-are-the-results'


def read(path, pattern):
    return re.findall(pattern, open(path).read(), re.M)


vsl = read('build-vsl-panels.py', r"^    \('([a-z0-9-]+)',")
cases = read('build-case-studies.py', r"^        'slug': '([a-z0-9-]+)',")

if AFTER not in vsl:
    raise SystemExit('panel %r is gone, so the case studies have no anchor '
                     'in the run any more' % AFTER)

cut = vsl.index(AFTER) + 1
order = (['vsl-%s' % s for s in vsl[:cut]]
         + ['case-%s' % s for s in cases]
         + ['vsl-%s' % s for s in vsl[cut:]])

missing = [s for s in order if not os.path.exists('exports/%s.png' % s)]
if missing:
    raise SystemExit('not rendered yet, run ./render.sh on these first:\n  '
                     + '\n  '.join(missing))

shutil.rmtree(OUT, ignore_errors=True)   # so a removed slide leaves no orphan
os.makedirs(OUT)

for i, slug in enumerate(order, 1):
    for ext in ('png', 'pdf'):
        src = 'exports/%s.%s' % (slug, ext)
        if os.path.exists(src):
            shutil.copy(src, '%s/%02d-%s.%s' % (OUT, i, slug, ext))
    print('%2d  %s' % (i, slug))

print('\n%d slides in %s/' % (len(order), OUT))


# ---------------------------------------------------------------------------
# Contact sheet. Finding a slide by scrubbing 64 files is slower than looking
# at one page, so the numbered set gets an index you can scan.
# ---------------------------------------------------------------------------
from PIL import Image, ImageDraw, ImageFont

COLS, TW = 8, 178                       # thumb width; height follows the 800x1080
TH = round(TW * 1080 / 800)
PAD, GUT, LBL = 26, 16, 26              # margin, gutter, label strip under each

FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
num_font = ImageFont.truetype(FONT, 15)

rows = -(-len(order) // COLS)
sheet = Image.new('RGB',
                  (PAD * 2 + COLS * TW + (COLS - 1) * GUT,
                   PAD * 2 + rows * (TH + LBL) + (rows - 1) * GUT),
                  (255, 255, 255))
d = ImageDraw.Draw(sheet)

for i, slug in enumerate(order):
    c, r = i % COLS, i // COLS
    x = PAD + c * (TW + GUT)
    y = PAD + r * (TH + LBL + GUT)
    th = Image.open('exports/%s.png' % slug).convert('RGB').resize((TW, TH),
                                                                   Image.LANCZOS)
    sheet.paste(th, (x, y))
    d.rectangle([x, y, x + TW - 1, y + TH - 1], outline=(214, 218, 224))
    # Number first and set apart, because that is what is being looked up.
    n = '%d' % (i + 1)
    d.text((x, y + TH + 6), n, font=num_font, fill=(0, 113, 227))
    # Trim by measured width, not by character count: the face is proportional,
    # so a fixed cut lets the long slugs run into the next cell.
    w = d.textlength(n, font=num_font) + 7
    name = slug.split('-', 1)[1]
    while name and d.textlength(name, font=num_font) > TW - w:
        name = name[:-1]
    d.text((x + w, y + TH + 6), name, font=num_font, fill=(120, 126, 134))

sheet.save('%s/00-index.png' % OUT)
print('wrote %s/00-index.png  (%dx%d)' % ((OUT,) + sheet.size))
