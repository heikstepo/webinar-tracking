#!/usr/bin/env python3
"""Build the "who this is for" run of VSL panels.

One generator rather than seven files: they are a sequence the viewer sees back
to back, so the ground, the left edge, the type scale and the card treatment
have to be identical across all of them. Kept apart, they drift.
"""
import os

HEAD = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>__TITLE__</title>
<link rel="stylesheet" href="../4pi.css">
<link rel="stylesheet" href="../voice-quiet.css">
<style>
@page { size: 800px 1080px; margin: 0; }

.slide { width: 800px; height: 1080px; padding: 90px 60px; background: var(--ground); }

/* Full-height hairline down the seam against the camera crop. 6px here so it
   survives the scale down into the edit; see panel-template. */
.edge { position: absolute; left: 0; top: 0; bottom: 0; width: 6px; background: #B9C0C9; }

.lead { margin: 0 0 26px; font-size: 26px; font-weight: 600; letter-spacing: -0.002em; color: var(--ink-3); }
.big  { margin: 0; max-width: 680px; font-size: 62px; font-weight: 600;
        line-height: 1.16; letter-spacing: -0.018em; color: var(--ink); }
.say  { margin: 0; max-width: 660px; font-size: 36px; font-weight: 600;
        line-height: 1.34; letter-spacing: -0.008em; color: var(--ink); }
.sub  { margin: 22px 0 0; font-size: 26px; font-weight: 500; line-height: 1.38; color: var(--ink-2); }

.tiles { display: flex; gap: 22px; justify-content: center; }
.tile  { width: 220px; background: var(--surface); border: 1px solid var(--hairline);
         border-radius: 22px; padding: 30px 18px 26px; text-align: center; }
.tile svg { display: block; width: 62px; height: 62px; margin: 0 auto 16px;
            fill: none; stroke: #7FA8DC; stroke-width: 1.6;
            stroke-linecap: round; stroke-linejoin: round; }
.tile b { display: block; font-size: 26px; font-weight: 600; letter-spacing: -0.004em; color: var(--ink); }
/* The thing that is not there yet reads as an outline, not a card. */
.tile--todo { background: none; border-style: dashed; border-color: #A9BDD4; }
.tile--todo svg { stroke: #A9BDD4; }

.art { margin: 0 0 42px; }

.bul { margin: 34px 0 0; padding: 0; list-style: none; text-align: left; max-width: 620px; }
.bul li { position: relative; padding-left: 34px; margin-bottom: 20px;
          font-size: 26px; font-weight: 500; line-height: 1.32; color: var(--ink); }
.bul li:last-child { margin-bottom: 0; }
.bul li::before { content: ""; position: absolute; left: 0; top: 14px;
                  width: 12px; height: 12px; border-radius: 50%; background: var(--blue); }
.bul li.muted { color: var(--ink-2); }
.bul li.muted::before { background: #C3CCD8; }
/* Struck through, because the point is the things being skipped over. */
.bul li.gone { color: var(--ink-3); text-decoration: line-through;
               text-decoration-color: #BFC6CF; text-decoration-thickness: 2px; }
.bul li.gone::before { background: #D3D8DF; }

/* A stack of icon rows: the densest layout here, used once. Namespaced
   because plain .rows already means something else in voice-quiet.css. */
.parts { display: flex; flex-direction: column; gap: 22px; text-align: left; width: 600px; }
.part  { display: flex; align-items: center; gap: 20px; }
.part svg { flex: none; width: 42px; height: 42px; fill: none; stroke: #7FA8DC;
           stroke-width: 1.6; stroke-linecap: round; stroke-linejoin: round; }
.part b { display: block; font-size: 25px; font-weight: 600; letter-spacing: -0.004em;
         line-height: 1.24; color: var(--ink); }
.part i { display: block; font-style: normal; margin-top: 4px;
         font-size: 19px; font-weight: 500; color: var(--ink-3); }

/* Two states of the same measure, stacked so the cut between them is the shape. */
.pill { width: 560px; border-radius: 18px; padding: 24px 30px;
        font-size: 30px; font-weight: 600; letter-spacing: -0.006em;
        display: flex; align-items: center; justify-content: space-between; }
.pill--in  { background: #E4EFFD; color: var(--ink); border: 1px solid #C3DAF6; }
.pill--out { background: none; color: var(--ink-3); border: 1px dashed #CDD2D8;
             margin-top: 16px; }
.pill--out span { text-decoration: line-through; text-decoration-color: #C3C9D1;
                  text-decoration-thickness: 2px; }
.pill em { font-style: normal; font-size: 28px; }

/* Fourteen days, drawn as fourteen days. */
.days { display: flex; gap: 9px; justify-content: center; }
.days span { width: 26px; height: 26px; border-radius: 8px; background: #C7DCF7; }
.days span.on { background: var(--blue); }

.chipnum { width: 54px; height: 54px; border-radius: 50%; background: #E4EFFD;
           color: var(--blue); font-size: 24px; font-weight: 600;
           display: flex; align-items: center; justify-content: center; }

.hero { margin: 0; font-size: 96px; font-weight: 600; line-height: 1;
        letter-spacing: -0.03em; color: var(--ink); }
</style>
</head>
<body>

<section class="slide slide--center slide--mid">
  <div class="edge"></div>
'''

FOOT = '''
</section>

</body>
</html>
'''

PERSON = ('<svg viewBox="0 0 62 62"><circle cx="31" cy="20" r="10"/>'
          '<path d="M11 52 C 11 39.5, 19.5 33, 31 33 C 42.5 33, 51 39.5, 51 52"/></svg>')

SLIDES = [
    # 1 — the section opens. One line, nothing else.
    ('who-this-is-for', 'Who this is for', '''
  <p class="big">Here&rsquo;s exactly<br>who this is for.</p>
'''),

    # 2 — the qualifying number, drawn as a band rather than written as a range:
    #     a range is a span, and a span is a picture.
    ('doing-20k-to-100k', 'Doing $20K to $100K a month', '''
  <div class="art" style="width:600px">
    <div style="display:flex; justify-content:space-between; align-items:flex-end; margin-bottom:20px">
      <span style="font-size:56px; font-weight:600; letter-spacing:-0.02em; color:var(--ink)">$20K</span>
      <span style="font-size:56px; font-weight:600; letter-spacing:-0.02em; color:var(--blue)">$100K</span>
    </div>
    <div style="height:14px; border-radius:8px;
                background:linear-gradient(90deg,#CFE0F8 0%,#1877F2 100%)"></div>
    <p style="margin:18px 0 0; font-size:26px; font-weight:600; color:var(--ink-2)">per month</p>
  </div>
  <p class="say">Selling your<br>high-ticket offer.</p>
'''),

    # 3 — the funnel drawn small, because the point is that one already exists,
    #     not what is in it.
    ('already-have-a-funnel', 'You already have a funnel', '''
  <div class="art">
    <div style="width:300px; height:44px; background:#E4ECF8; margin:0 auto 8px;
                clip-path:polygon(0% 0%,100% 0%,88% 100%,12% 100%)"></div>
    <div style="width:264px; height:44px; background:#D0E0F5; margin:0 auto 8px;
                clip-path:polygon(0% 0%,100% 0%,86% 100%,14% 100%)"></div>
    <div style="width:227px; height:44px; background:#B9D2F1; margin:0 auto 8px;
                clip-path:polygon(0% 0%,100% 0%,80% 100%,20% 100%)"></div>
    <div style="width:136px; height:16px; background:#A6C6ED; margin:0 auto"></div>
  </div>
  <p class="say">You probably already have<br>some sort of funnel set up.</p>
'''),

    # 4 — two roles, so two tiles. The lead-in runs straight into them.
    ('closers-and-setters', 'Closers and setters', '''
  <p class="lead">Maybe you have some</p>
  <div class="tiles">
    <div class="tile">''' + PERSON + '''<b>Closers</b></div>
    <div class="tile">''' + PERSON + '''<b>Setters</b></div>
  </div>
'''),

    # 5 — one thing done, one thing not yet. The dashed tile carries that on its
    #     own, which is why the caption never has to say "not yet".
    ('organic-now-paid', 'Organic, now paid ads', '''
  <div class="tiles" style="align-items:center">
    <div class="tile" style="width:210px">
      <svg viewBox="0 0 62 62"><path d="M31 52 V 26"/>
        <path d="M31 30 C 31 18, 22 12, 12 12 C 12 24, 20 30, 31 30 Z"/>
        <path d="M31 36 C 31 25, 39 20, 50 20 C 50 31, 42 36, 31 36 Z"/></svg>
      <b>Organic</b>
    </div>
    <span style="font-size:40px; font-weight:600; color:var(--ink-3)">+</span>
    <div class="tile tile--todo" style="width:210px">
      <svg viewBox="0 0 62 62"><rect x="9" y="14" width="44" height="34" rx="6"/>
        <path d="M27 25 L 39 31 L 27 37 Z"/></svg>
      <b>Paid ads</b>
    </div>
  </div>
  <p class="sub" style="max-width:600px; margin-top:38px">
    Fully on organic, and you want<br>to launch paid ads as well.
  </p>
'''),

    # 6 — the line is the argument: flat and wandering, then the turn upward.
    ('already-tried-paid-ads', 'Already tried paid ads', '''
  <div class="art">
    <svg viewBox="0 0 570 220" width="570" height="220" fill="none" aria-hidden="true">
      <defs>
        <marker id="up" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="4.4"
                markerHeight="4.4" orient="auto">
          <path d="M0.5 0.5 L9 5 L0.5 9.5" fill="none" stroke="#0071E3"
                stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>
        </marker>
      </defs>
      <path d="M20 200 H 540" stroke="#DDE1E6" stroke-width="2"/>
      <path d="M20 150 C 80 130, 110 175, 160 150 C 210 125, 250 170, 300 148"
            stroke="#AEB6C0" stroke-width="4" stroke-linecap="round"/>
      <path d="M300 148 C 360 140, 420 100, 512 34"
            stroke="#0071E3" stroke-width="5" stroke-linecap="round"
            stroke-dasharray="2 14" marker-end="url(#up)"/>
      <circle cx="300" cy="148" r="8" fill="#0071E3"/>
    </svg>
  </div>
  <ul class="bul">
    <li class="muted">You already tried paid ads</li>
    <li class="muted">Maybe they worked okay, maybe they didn&rsquo;t</li>
    <li>You want to make it perform better</li>
  </ul>
'''),

    # 7 — the close. Small setup, then the answer at full size.
    ('yes-we-can-help', 'Yes, we can help you', '''
  <p class="lead">If you fall into this</p>
  <p class="big">Yes,<br>we can help you.</p>
'''),
    # 8 — the mirror of 7. Same shape, opposite answer, so the pair reads as
    #     one decision rather than two unrelated cards.
    ('not-for-you', 'This is not for you', '''
  <p class="lead">If you don&rsquo;t fall into this</p>
  <p class="big" style="color:#8A9099">No,<br>this is not for you.</p>
'''),

    # 9 — the cut drawn as a cut: the same measure in two states, one kept and
    #     one struck, stacked so the line between them is the qualification.
    ('under-20k-not-for-you', 'Under $20K a month', '''
  <div class="art">
    <div class="pill pill--in"><span>$20K to $100K / mo</span><em>&#10003;</em></div>
    <div class="pill pill--out"><span>Under $20K / mo</span><em>&#10007;</em></div>
  </div>
  <p class="say" style="max-width:600px">If you&rsquo;re making less<br>than that, this is not for you.</p>
'''),

    # 10 — a list of what is deliberately not being covered, so the crossing out
    #      is the whole slide. The one live line sits under it.
    ('no-pain-points', 'We both know what is going on', '''
  <p class="lead">I won&rsquo;t go into</p>
  <ul class="bul" style="margin-top:0">
    <li class="gone">Your current situation</li>
    <li class="gone">The roadblocks</li>
    <li class="gone">The pain points</li>
    <li class="gone">The desire</li>
  </ul>
  <p class="say" style="margin-top:44px; max-width:600px">
    We&rsquo;re both business owners.<br>We know what&rsquo;s going on here.
  </p>
'''),

    # 11 — two promises, so two sizes: what gets built, then where it goes.
    ('build-and-scale', 'Build it, then scale it', '''
  <p class="lead">If you fall into that bucket</p>
  <p class="big" style="font-size:52px">Build this ad funnel<br>in the next 14 days.</p>
  <p class="say" style="margin-top:34px; color:var(--blue); max-width:600px">
    Scale that offer to multiple<br>six and seven figures.
  </p>
'''),

    # 12 — a section opener like slide 1, but numbered, because what follows is
    #      a sequence and the chips say so before a word of it is read.
    ('how-this-works', 'How this works', '''
  <div class="art" style="display:flex; gap:14px; justify-content:center">
    <span class="chipnum">1</span><span class="chipnum">2</span><span class="chipnum">3</span>
  </div>
  <p class="big" style="font-size:54px">Here&rsquo;s exactly<br>how this works.</p>
  <p class="sub" style="margin-top:26px">Step by step.</p>
'''),

    # 13 — the quietest slide in the run, on purpose: it sets up the dense one
    #      that follows, and two heavy slides back to back read as one.
    ('funnel-has-parts', 'The funnel has parts', '''
  <p class="say" style="font-size:40px; max-width:640px">
    That ads funnel includes a few<br>things in order to work.
  </p>
'''),

    # 14 — the five parts. Rows rather than cards: five cards at this width go
    #      small and square, five rows keep the labels at reading size.
    ('the-five-parts', 'The five parts', '''
  <div class="parts">
    <div class="part">
      <svg viewBox="0 0 42 42"><path d="M4 18 L18 4 H36 V22 L22 36 Z"/><circle cx="29" cy="13" r="3"/></svg>
      <span><b>Cold traffic friendly offer</b></span>
    </div>
    <div class="part">
      <svg viewBox="0 0 42 42"><path d="M5 8 H37 L26 22 V35 L16 30 V22 Z"/></svg>
      <span><b>Dialed in sales funnel</b><i>VSL funnel or webinar funnel</i></span>
    </div>
    <div class="part">
      <svg viewBox="0 0 42 42"><circle cx="15" cy="14" r="6"/>
        <path d="M4 34 C 4 26, 9 22, 15 22 C 21 22, 26 26, 26 34"/>
        <circle cx="30" cy="16" r="4.5"/><path d="M25 34 C 25 28, 28 25, 32 25 C 35 25, 37.5 27, 38 30"/></svg>
      <span><b>Sales team</b><i>with systems and automations</i></span>
    </div>
    <div class="part">
      <svg viewBox="0 0 42 42"><path d="M6 13 L21 5 L36 13 V29 L21 37 L6 29 Z"/>
        <path d="M6 13 L21 21 L36 13 M21 21 V37"/></svg>
      <span><b>Good fulfillment</b></span>
    </div>
    <div class="part">
      <svg viewBox="0 0 42 42"><rect x="4" y="9" width="34" height="24" rx="5"/>
        <path d="M17 17 L26 21 L17 25 Z"/></svg>
      <span><b>A paid ads engine</b></span>
    </div>
  </div>
'''),

    # 15 — fourteen days drawn as fourteen days, so the promise is countable
    #      rather than just asserted.
    ('within-14-days', 'Within 14 days', '''
  <p class="hero">14 days</p>
  <div class="days" style="margin:38px 0 40px">
    <span class="on"></span><span class="on"></span><span class="on"></span>
    <span class="on"></span><span class="on"></span><span class="on"></span>
    <span class="on"></span><span class="on"></span><span class="on"></span>
    <span class="on"></span><span class="on"></span><span class="on"></span>
    <span class="on"></span><span class="on"></span>
  </div>
  <p class="say" style="max-width:620px">
    Everything I&rsquo;m about to explain<br>happens in the first two weeks.
  </p>
'''),
]

for name, title, body in SLIDES:
    open('slides/vsl-%s.html' % name, 'w').write(
        HEAD.replace('__TITLE__', title) + body + FOOT)
    print('wrote slides/vsl-%s.html' % name)
