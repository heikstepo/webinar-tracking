#!/usr/bin/env python3
"""Case study panels, one per client.

Photos live in design/photos/<slug>.jpg and are inlined as base64 so the
rendered file stays self contained. If a photo is missing the slide still
builds, with a neutral disc in its place, so a missing asset never blocks
a render and is obvious rather than silent.
"""
import base64
import os
import re

W, H = 800, 1080

CASES = [
    {
        'shape': 'jump',
        'slug': 'steven',
        'name': 'Steven',
        'from': '$15K/mo',
        'to':   '$160K/mo',
        'unit': 'per month in cash collected',
        'chip': '$100K/mo within 12 weeks',
        'note': 'Hundreds of thousands of dollars<br>with this offer alone.',
    },
    {
        'shape': 'hero',
        'slug': 'rauf',
        'name': 'Rauf',
        'before': 'Was doing $3K/mo on a low ticket offer',
        'to':   '$350K+',
        'unit': 'from his high ticket offer,<br>launched from zero',
        'chip': 'On track for $100K this month',
        'note': '',
    },
    {
        'shape': 'solo',
        'slug': 'david',
        'name': 'David',
        'crop': '235%; background-position: 50% 9%',
        'to':   '$200K+',
        'unit': 'selling his high ticket offer',
        'chip': '',
        'note': '',
    },
]


def photo(c):
    """Inline the photo if it is there. A slide that renders with a grey disc
    is easier to spot and fix than one that silently ships a broken image.

    `crop` is a background-size / background-position pair. The disc is small,
    so a photo shot wide needs zooming in on the head or the person ends up
    unrecognisable; the default suits a portrait that is already close."""
    crop = c.get('crop', 'cover; background-position: center 22%')
    for ext in ('jpg', 'jpeg', 'png', 'webp'):
        p = 'photos/%s.%s' % (c['slug'], ext)
        if os.path.exists(p):
            mime = 'jpeg' if ext in ('jpg', 'jpeg') else ext
            b64 = base64.b64encode(open(p, 'rb').read()).decode()
            return ('<div class="cs__pic" style="background-size:%s; '
                    'background-image:url(data:image/%s;base64,%s)"></div>'
                    % (crop, mime, b64))
    return '<div class="cs__pic cs__pic--none"></div>'


TPL = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>__NAME__</title>
<link rel="stylesheet" href="../4pi.css">
<link rel="stylesheet" href="../voice-quiet.css">
<style>
/* ============================================================================
   Case study panel.

   Same family as the reference the client sent, but deliberately not the same
   design: our ground and our blue rather than cream and gold, no small caps
   role line under the name (we were not given one and will not invent one),
   and the pill carries a real milestone instead of a computed multiple. The
   supporting claim is set as type rather than a second pill, so the eye lands
   on the figure once and not three times.
   ========================================================================= */
@page { size: __W__px __H__px; margin: 0; }

.slide { width: __W__px; height: __H__px; padding: 90px 60px; background: var(--ground); }
.edge { position: absolute; left: 0; top: 0; bottom: 0; width: 6px; background: #B9C0C9; }

.cs__pic {
  width: 190px; height: 190px; border-radius: 50%;
  background-repeat: no-repeat;
  box-shadow: 0 0 0 5px var(--ground), 0 0 0 8px #BFD6F7,
              0 10px 26px rgba(20, 25, 35, 0.13);
}
.cs__pic--none { background: #DDE3EA; }

.cs__name { margin: 34px 0 0; font-size: 38px; font-weight: 600;
            letter-spacing: -0.012em; color: var(--ink); }

/* Short rule under the name, the one borrowed device, kept in our accent. */
.cs__rule { width: 56px; height: 3px; border-radius: 2px;
            background: var(--blue); margin: 22px auto 30px; }

.cs__jump { display: flex; align-items: baseline; justify-content: center; gap: 22px; }
.cs__from { font-size: 30px; font-weight: 600; letter-spacing: -0.008em; color: var(--ink-3); }
.cs__arrow { font-size: 26px; color: #9CB4D2; }
.cs__to { font-size: 64px; font-weight: 600; letter-spacing: -0.026em; color: var(--blue); }

.cs__unit { margin: 14px 0 0; font-size: 21px; font-weight: 500; color: var(--ink-3); }

.cs__chip { display: inline-block; margin-top: 30px; padding: 10px 22px;
            border-radius: 999px; background: #E4EFFD; color: var(--blue);
            font-size: 21px; font-weight: 600; letter-spacing: -0.003em; }

/* The hero variant carries the old rate above the figure rather than either
   side of an arrow: $3K/mo is a monthly rate and $350K+ is a total, so setting
   them across an arrow would claim a comparison that isn't true. Margins are
   stated on both, because a bare <p> here inherits the stylesheet's paragraph
   spacing and the figure ends up adrift in the middle of the panel. */
.cs__before { margin: 0 0 20px; font-size: 22px; font-weight: 500; color: var(--ink-3); }
.cs__hero { margin: 0; font-size: 78px; font-weight: 600; letter-spacing: -0.03em;
            line-height: 1; color: var(--blue); }
.cs__hero--solo { font-size: 96px; letter-spacing: -0.034em; }

.cs__note { margin: 30px auto 0; max-width: 560px; font-size: 22px;
            font-weight: 500; line-height: 1.36; color: var(--ink-2); }
</style>
</head>
<body>

<section class="slide slide--center slide--mid">
  <div class="edge"></div>

__PHOTO__
  <p class="cs__name">__NAME__</p>
  <div class="cs__rule"></div>

__FIGURE__

__CHIP__
__NOTE__

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

JUMP = '''  <div class="cs__jump">
    <span class="cs__from">%(from)s</span>
    <span class="cs__arrow">&rarr;</span>
    <span class="cs__to">%(to)s</span>
  </div>
  <p class="cs__unit">%(unit)s</p>'''

HERO = '''  <p class="cs__before">%(before)s</p>
  <p class="cs__hero">%(to)s</p>
  <p class="cs__unit">%(unit)s</p>'''

# One number and nothing else. No before line to set it against and no
# milestone to follow it, so the figure gets the whole panel and runs larger.
SOLO = '''  <p class="cs__hero cs__hero--solo">%(to)s</p>
  <p class="cs__unit">%(unit)s</p>'''

SHAPES = {'jump': JUMP, 'hero': HERO, 'solo': SOLO}

for c in CASES:
    figure = SHAPES[c['shape']] % c
    # An empty chip or note still leaves a line box behind, which shifts the
    # whole centred stack. Drop the element rather than emit it empty.
    chip = ('  <p style="margin:0"><span class="cs__chip">%s</span></p>' % c['chip']
            if c['chip'] else '')
    note = '  <p class="cs__note">%s</p>' % c['note'] if c['note'] else ''
    out = (TPL.replace('__W__', str(W)).replace('__H__', str(H))
              .replace('__PHOTO__', '  ' + photo(c))
              .replace('__NAME__', c['name']).replace('__FIGURE__', figure)
              .replace('__CHIP__', chip).replace('__NOTE__', note))
    open('slides/case-%s.html' % c['slug'], 'w').write(out)
    have = 'NO PHOTO, placeholder disc' if 'cs__pic cs__pic--none' in out else 'photo embedded'
    print('wrote slides/case-%s.html  (%s)' % (c['slug'], have))
