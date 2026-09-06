#!/usr/bin/env python3
"""Build the "who this is for" run of VSL panels.

One generator rather than seven files: they are a sequence the viewer sees back
to back, so the ground, the left edge, the type scale and the card treatment
have to be identical across all of them. Kept apart, they drift.
"""
import os
import re

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

/* The one phrase in a sentence that carries it. A weighted underline rather
   than a filled highlighter block: the panel sits beside a talking head, not
   on a keynote screen, and a slab of colour at this size shouts. This was
   referenced by three panels before it existed, so their emphasis was
   silently rendering as plain text. */
.say__mark { color: var(--blue);
             background: linear-gradient(to top, #C6DDFA 0 0.15em, transparent 0.15em); }

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

/* Two halves with a rule between them, so a contrast is a shape and not a
   claim. The volume in the lower half is the argument. */
.vs { width: 660px; text-align: left; }
.vs__half { padding: 30px 0; }
.vs__half + .vs__half { border-top: 1px solid var(--hairline); padding-top: 34px; }
.who { display: inline-block; margin-bottom: 18px; padding: 6px 18px;
       border-radius: 999px; font-size: 18px; font-weight: 600; letter-spacing: 0.01em; }
.who--you { background: #E8EAEE; color: var(--ink-2); }
.who--us  { background: #E4EFFD; color: var(--blue); }
.vs h3 { margin: 0; font-size: 32px; font-weight: 600;
            letter-spacing: -0.008em; color: var(--ink); }
.vs p  { margin: 10px 0 0; font-size: 20px; font-weight: 500; color: var(--ink-3); }
.vs strong { display: block; margin-top: 16px; font-size: 24px;
                font-weight: 600; color: var(--blue); }

/* Forty one small chips against one line of work. The wrap is the point:
   the imbalance has to be felt before any of it is read. */
.chips { display: flex; flex-wrap: wrap; gap: 7px; margin-top: 18px; }
.chips span { padding: 6px 12px; border-radius: 999px; background: var(--surface);
              border: 1px solid var(--hairline); font-size: 14px; font-weight: 500;
              color: var(--ink-2); }

/* Two things that make up one price. */
.duo { display: flex; gap: 22px; }
.duo > div { width: 300px; background: var(--surface); border: 1px solid var(--hairline);
             border-radius: 20px; padding: 30px 26px 32px; text-align: left; }
.duo h4 { margin: 0; font-size: 27px; font-weight: 600; letter-spacing: -0.006em;
          line-height: 1.2; color: var(--ink); }
.duo p  { margin: 12px 0 0; font-size: 19px; font-weight: 500; line-height: 1.35;
          color: var(--ink-3); }

/* The credit, drawn as a bar that gets cleared rather than described. */
.bar { width: 560px; height: 26px; border-radius: 999px; background: #DDE4EC;
       overflow: hidden; }
.bar span { display: block; height: 100%;
            background: linear-gradient(90deg, #9AC4F5 0%, #0071E3 100%); }
.barlab { display: flex; justify-content: space-between; width: 560px;
          margin-bottom: 14px; font-size: 20px; font-weight: 600; color: var(--ink-2); }
.barlab b { color: #248A13; font-weight: 600; }

/* One definition, set as the equation it is. */
.eq { display: flex; align-items: baseline; justify-content: center; gap: 18px;
      font-size: 40px; font-weight: 600; letter-spacing: -0.012em; color: var(--ink); }
.eq i { font-style: normal; color: var(--blue); font-size: 44px; }

/* A quiet numeral that gives the build sequence a spine without spending a
   word on it. Sits above the line it belongs to, not beside it. */
.stepnum { margin: 0 0 20px; font-size: 30px; font-weight: 600;
           letter-spacing: 0.04em; color: #A9BDD4; }

/* Two by two, so a long deliverable list reads as four short ones. A single
   column of fourteen items is the thing to avoid here. */
.gcards { display: grid; grid-template-columns: 320px 320px; gap: 26px;
          text-align: left; }
.gcard { background: var(--surface); border: 1px solid var(--hairline);
         border-radius: 18px; padding: 22px 24px 24px; }
.gcard h4 { margin: 0 0 14px; font-size: 20px; font-weight: 600;
            letter-spacing: -0.003em; color: var(--blue); }
.gcard ul { margin: 0; padding: 0; list-style: none; }
.gcard li { position: relative; padding-left: 18px; margin-bottom: 8px;
            font-size: 16px; font-weight: 500; line-height: 1.3; color: var(--ink); }
.gcard--wide { grid-column: span 2; }
.gcard--wide ul { columns: 2; column-gap: 30px; }
.gcard--wide li { break-inside: avoid; }
.gcard li:last-child { margin-bottom: 0; }
.gcard li::before { content: ""; position: absolute; left: 0; top: 9px;
                    width: 7px; height: 7px; border-radius: 50%; background: #B9CFEC; }

.tag { display: inline-block; padding: 9px 22px; border-radius: 999px;
       background: #E4EFFD; color: var(--blue);
       font-size: 24px; font-weight: 600; letter-spacing: -0.004em; }

/* A running tally: what is already done, and the one thing being added. */
.check { display: flex; flex-direction: column; gap: 26px; text-align: left; width: 600px; }
.check div { display: flex; align-items: flex-start; gap: 18px;
             font-size: 28px; font-weight: 600; letter-spacing: -0.005em; color: var(--ink); }
.check em { flex: none; width: 38px; height: 38px; border-radius: 50%;
            display: flex; align-items: center; justify-content: center;
            font-style: normal; font-size: 20px; }
.check .done em { background: #E7F5E3; color: #248A13; }
.check .now  em { background: #E4EFFD; color: var(--blue); }
.check .now { color: var(--blue); }
.check small { display: block; margin-top: 6px; font-size: 19px;
               font-weight: 500; color: var(--ink-3); }

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
    # 16 — opener for the build. The payoff line takes the accent so the
    #      section is framed by where it ends up, not by what it costs.
    ('initial-launch', 'The initial launch', '''
  <p class="lead">For the initial launch</p>
  <p class="big" style="font-size:52px">Here&rsquo;s exactly<br>what we set up.</p>
  <p class="say" style="margin-top:32px; font-size:28px; color:var(--blue); max-width:620px">
    The foundation to scale to multiple<br>six and seven figures.
  </p>
'''),

    # 17 — first of the build steps, and where the numeral motif starts.
    ('cold-traffic-offer', 'Cold traffic friendly offer', '''
  <p class="stepnum">01</p>
  <p class="big" style="font-size:50px">Make your offer<br>cold traffic friendly.</p>
  <p class="sub" style="max-width:600px">Paid ads only work if the offer does.</p>
'''),

    # 18 — the traffic has to land somewhere, so the slide is two boxes and the
    #      arrow between them. Nothing else to say.
    ('traffic-needs-a-funnel', 'Traffic needs somewhere to go', '''
  <p class="stepnum">02</p>
  <div class="art" style="display:flex; align-items:center; gap:22px">
    <div class="tile" style="width:210px; padding:26px 16px 24px">
      <svg viewBox="0 0 62 62"><rect x="9" y="14" width="44" height="34" rx="6"/>
        <path d="M27 25 L 39 31 L 27 37 Z"/></svg>
      <b>Paid ads</b>
    </div>
    <svg viewBox="0 0 34 14" width="34" height="14" fill="none" style="flex:none">
      <g stroke="#0071E3" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round">
        <path d="M2 7 H 24"/><path d="M19 2.5 L 29 7 L 19 11.5"/></g>
    </svg>
    <div class="tile" style="width:210px; padding:26px 16px 24px">
      <svg viewBox="0 0 62 62"><path d="M9 12 H53 L37 32 V50 L25 44 V32 Z"/></svg>
      <b>Your funnel</b>
    </div>
  </div>
  <p class="say" style="max-width:600px">The traffic has to land<br>somewhere. That is the funnel.</p>
'''),

    # 19 — the two shapes it might already be, then the condition on both.
    ('dialed-in-before-launch', 'Dialed in before launch', '''
  <p class="lead">Whether it&rsquo;s a</p>
  <div class="art" style="display:flex; gap:16px; justify-content:center">
    <span class="tag">VSL funnel</span><span class="tag">Webinar funnel</span>
  </div>
  <p class="say" style="max-width:640px">
    It needs to be super dialed in<br>before we launch.
  </p>
  <p class="sub" style="max-width:600px">Too many leaks and cold traffic will not convert.</p>
'''),

    # 20 — one line, full size. The turn from problem to offer.
    ('we-build-the-whole-thing', 'We build the whole thing', '''
  <p class="big">That&rsquo;s why we build<br>the whole thing<br>for you.</p>
'''),

    # 21 — two routes, and the second is the first plus one more, so it is drawn
    #      that way rather than as two unrelated options.
    ('one-funnel-or-two', 'One funnel or two', '''
  <div class="art" style="display:flex; flex-direction:column; gap:18px">
    <div class="pill pill--in" style="width:600px; font-size:26px">
      <span>VSL call funnel</span><em>&#10003;</em>
    </div>
    <div class="pill pill--in" style="width:600px; font-size:26px; margin:0">
      <span>VSL call funnel plus webinar funnel</span><em>&#10003;</em>
    </div>
  </div>
  <p class="say" style="max-width:600px">Depending on the ICP<br>we&rsquo;re attracting for you.</p>
'''),

    # 22 — fourteen deliverables would be a wall. Four gcards of three is the
    #      same content read four times faster.
    ('vsl-funnel-buildout', 'VSL funnel buildout', '''
  <p class="art" style="margin-bottom:28px"><span class="tag">VSL funnel</span></p>
  <div class="gcards">
    <div class="gcard"><h4>The page</h4><ul>
      <li>VSL landing page</li><li>VSL script</li><li>VSL editing</li></ul></div>
    <div class="gcard"><h4>The booking</h4><ul>
      <li>Application</li><li>Booking automations</li></ul></div>
    <div class="gcard"><h4>The thank you page</h4><ul>
      <li>Thank you page setup</li><li>Thank you video</li>
      <li>FAQ videos</li><li>More sales assets</li></ul></div>
    <div class="gcard"><h4>The post booking process</h4><ul>
      <li>15 to 20 long form pre call emails</li><li>Pre call SMS sequences</li>
      <li>Pre call sales assets</li><li>Pre call videos</li>
      <li>Sales team training</li></ul></div>
    <div class="gcard gcard--wide"><h4>The tech</h4><ul>
      <li>Entire tech integrations</li><li>All the automations</li>
      <li>Every tool connected</li><li>Nothing for you to worry about</li></ul></div>
  </div>
'''),

    # 23 — same grid as 22 on purpose: the two are a pair, and the webinar one
    #      is additive, which the chip under the title says.
    ('webinar-funnel-buildout', 'Webinar funnel buildout', '''
  <p class="art" style="margin-bottom:8px"><span class="tag">Webinar funnel</span></p>
  <p class="sub" style="margin:0 0 26px; font-size:21px">On top of the VSL funnel</p>
  <div class="gcards">
    <div class="gcard"><h4>The webinar</h4><ul>
      <li>Full slideshow presentation</li><li>The script</li></ul></div>
    <div class="gcard"><h4>The pages</h4><ul>
      <li>Webinar opt in page</li><li>Post registration page</li></ul></div>
    <div class="gcard"><h4>The upsell</h4><ul>
      <li>VIP upsell offer</li><li>Sold before the webinar</li></ul></div>
    <div class="gcard"><h4>On the pages</h4><ul>
      <li>Thank you video</li><li>FAQ videos</li><li>More sales assets</li></ul></div>
    <div class="gcard gcard--wide"><h4>Pre and post webinar flows</h4><ul>
      <li>15 to 20 pre webinar emails</li><li>Pre webinar SMS sequences</li>
      <li>Telegram group nurture</li><li>Post webinar SMS sequence</li>
      <li>SDR scripts</li><li>Show up, convert, then close</li></ul></div>
  </div>
'''),

    # 24 — a breath after two dense slides.
    ('thats-the-funnel-side', 'That is the funnel side', '''
  <p class="big" style="font-size:54px">That&rsquo;s everything<br>on the funnel side.</p>
'''),

    # 25 — the running tally. Two ticks already earned, one thing being added,
    #      and the optional flag lives on the item rather than in a sentence.
    ('sales-side-next', 'On to the sales side', '''
  <div class="check">
    <div class="done"><em>&#10003;</em><span>Cold traffic friendly offer</span></div>
    <div class="done"><em>&#10003;</em><span>Funnel set up</span></div>
    <div class="now"><em>&#43;</em><span>Setters and closers
      <small>Optional staffing, on the sales side</small></span></div>
  </div>
'''),
    # 26 — a bridge. Quiet on purpose, sitting between the funnel build and
    #      the ads build.
    ('while-we-build', 'While we build all of this', '''
  <p class="say" style="font-size:40px; max-width:640px">
    And while all of this<br>is being built by us&hellip;
  </p>
  <p class="art" style="margin:34px 0 0"><span class="tag">Still inside the first 14 days</span></p>
'''),

    # 27 — the third build step. Rows rather than the 2x2 grid used for the
    #      funnel slides, so this reads as its own thing and not a third
    #      instalment of the same list.
    ('paid-ads-engine', 'Paid ads engine', '''
  <p class="stepnum">03</p>
  <p class="art" style="margin-bottom:34px"><span class="tag">Paid ads engine</span></p>
  <div class="parts">
    <div class="part">
      <svg viewBox="0 0 42 42"><path d="M10 5 H32 V37 H10 Z"/><path d="M16 14 H26 M16 21 H26 M16 28 H22"/></svg>
      <span><b>All the ad scripts</b></span>
    </div>
    <div class="part">
      <svg viewBox="0 0 42 42"><rect x="5" y="8" width="32" height="26" rx="4"/>
        <path d="M5 15 H37"/><circle cx="10" cy="11.5" r="1.4"/></svg>
      <span><b>The entire account set up</b></span>
    </div>
    <div class="part">
      <svg viewBox="0 0 42 42"><circle cx="21" cy="21" r="15"/><circle cx="21" cy="21" r="8"/>
        <circle cx="21" cy="21" r="2.4"/></svg>
      <span><b>Campaigns and pixel</b></span>
    </div>
    <div class="part">
      <svg viewBox="0 0 42 42"><path d="M21 34 V16"/><path d="M13 24 L21 15 L29 24"/>
        <path d="M10 8 H32"/></svg>
      <span><b>Ready to launch</b></span>
    </div>
  </div>
  <p class="sub" style="margin-top:34px; max-width:600px">Done for you. You don&rsquo;t worry about any of it.</p>
'''),

    # 28 — the fourteen days again. The strip leads this time and the number is
    #      the caption, so the callback is not a copy of slide 15.
    ('all-within-14-days', 'All within 14 days', '''
  <div class="days" style="margin-bottom:40px">
    <span class="on"></span><span class="on"></span><span class="on"></span>
    <span class="on"></span><span class="on"></span><span class="on"></span>
    <span class="on"></span><span class="on"></span><span class="on"></span>
    <span class="on"></span><span class="on"></span><span class="on"></span>
    <span class="on"></span><span class="on"></span>
  </div>
  <p class="big" style="font-size:50px">All of this happens<br>in the first 14 days<br>of working together.</p>
'''),

    # 29 — the contrast, drawn as two halves of one column. One line of work
    #      above the rule, thirteen chips below it. The wrap does the arguing.
    ('your-involvement', 'Your involvement', '''
  <div class="vs">
    <div class="vs__half">
      <span class="who who--you">You</span>
      <h3>Record a couple of videos.</h3>
      <p>The ads and the funnel videos.</p>
      <strong>A couple of hours, max.</strong>
    </div>
    <div class="vs__half">
      <span class="who who--us">Us</span>
      <h3>Everything else.</h3>
      <div class="chips">
        <span>Cold traffic offer</span><span>Sales funnel</span><span>VSL landing page</span>
        <span>VSL script</span><span>VSL editing</span><span>Application</span>
        <span>Booking automations</span><span>Thank you page</span><span>Thank you video</span>
        <span>FAQ videos</span><span>Sales assets</span><span>Pre call emails</span>
        <span>Pre call SMS</span><span>Pre call sales assets</span><span>Tech integrations</span>
        <span>Automations</span><span>Webinar slideshow</span><span>Webinar script</span>
        <span>Opt in page</span><span>VIP upsell offer</span><span>Post registration page</span>
        <span>Registration video</span><span>Webinar FAQ videos</span><span>Pre webinar emails</span>
        <span>Pre webinar SMS</span><span>Telegram nurture</span><span>Post webinar SMS</span>
        <span>SDR scripts</span><span>Ad scripts</span><span>Ad account</span>
        <span>Campaigns</span><span>Pixel</span><span>Setters</span>
        <span>Closers</span><span>Sales systems</span><span>Sales team training</span>
        <span>Fulfillment</span><span>Iterate the funnel</span><span>Iterate the ads</span>
        <span>Continuous testing</span><span>Train more reps</span>
      </div>
    </div>
  </div>
'''),

    # 30 — the thing we are not doing, struck, then what is actually happening.
    ('not-just-the-launch', 'Not just the launch', '''
  <p class="say" style="font-size:32px; color:var(--ink-3); max-width:620px;
                        text-decoration:line-through; text-decoration-color:#C3C9D1;
                        text-decoration-thickness:2px">
    Set it up, launch it,<br>and let it be.
  </p>
  <p class="big" style="margin-top:44px; font-size:50px">This is all<br>just the launch.</p>
'''),

    # 31 — alignment drawn as two paths becoming one, because the sentence is
    #      about incentives pointing the same way.
    ('same-goal', 'Aligned on the same goal', '''
  <div class="art">
    <svg viewBox="0 0 320 140" width="320" height="140" fill="none" aria-hidden="true">
      <defs><marker id="one" viewBox="0 0 10 10" refX="6" refY="5" markerWidth="4.6"
             markerHeight="4.6" orient="auto">
        <path d="M0.5 0.5 L9 5 L0.5 9.5" fill="none" stroke="#0071E3" stroke-width="2.2"
              stroke-linecap="round" stroke-linejoin="round"/></marker></defs>
      <path d="M14 26 C 110 26, 120 70, 190 70" stroke="#AEB6C0" stroke-width="4" stroke-linecap="round"/>
      <path d="M14 114 C 110 114, 120 70, 190 70" stroke="#AEB6C0" stroke-width="4" stroke-linecap="round"/>
      <path d="M190 70 H 292" stroke="#0071E3" stroke-width="5" stroke-linecap="round"
            marker-end="url(#one)"/>
    </svg>
  </div>
  <p class="big" style="font-size:44px">We only get paid from<br>the revenue we generate.</p>
  <p class="say" style="margin-top:30px; font-size:27px; color:var(--blue); max-width:620px">
    So we scale it with you, long term.
  </p>
'''),

    # 32 — a loop, because every item on it is a thing that keeps happening.
    ('continuous-iteration', 'Continuous iteration', '''
  <div class="art">
    <svg viewBox="0 0 90 90" width="90" height="90" fill="none" aria-hidden="true">
      <path d="M45 12 A 33 33 0 1 1 18 27" stroke="#0071E3" stroke-width="5"
            stroke-linecap="round"/>
      <path d="M32 8 L45 12 L41 25" stroke="#0071E3" stroke-width="5"
            stroke-linecap="round" stroke-linejoin="round"/>
    </svg>
  </div>
  <ul class="bul">
    <li>Iterate the funnel, the ads, the sales systems</li>
    <li>Test new things, continuously</li>
    <li>Staff more sales reps</li>
    <li>Train them</li>
  </ul>
'''),

    # 32a — the risk-free claim, and why it exists. Four beats: the aside about
    #       pricing, the claim, the competitive reason, the certainty. The
    #       reason is set quiet because it is an explanation; the certainty
    #       carries the accent because it is what he wants them to leave with.
    ('risk-free-by-design', 'Risk-free by design', '''
  <p class="lead">Pricing structure in a second</p>
  <p class="big" style="font-size:50px">But this whole offer<br>is designed to be<br>
    <span class="say__mark">risk-free</span> on your end.</p>
  <p class="sub" style="margin-top:36px; max-width:640px">
    Simply so our competitors literally<br>can&rsquo;t compete with it,
    because<br>they can&rsquo;t get results.
  </p>
  <p class="say" style="margin-top:30px; font-size:30px; color:var(--blue); max-width:620px">
    And I know we can get you<br>results for certain.
  </p>
'''),

    # 32b — the handoff into the case studies. Nothing on it but the question
    #       and the answer, because the panels that follow are the answer.
    ('here-are-the-results', 'Here are the results', '''
  <p class="lead">Why?</p>
  <p class="big" style="font-size:50px">Here are some of<br>the results<br>we&rsquo;ve seen.</p>
  <p class="sub" style="margin-top:30px; max-width:640px">
    Running high ticket offers<br>over the past couple of years.
  </p>
'''),

    # 33 — section opener for the money part.
    ('the-pricing-structure', 'The pricing structure', '''
  <p class="art" style="margin-bottom:32px"><span class="tag">Pricing</span></p>
  <p class="big" style="font-size:52px">Here&rsquo;s the exact<br>pricing structure.</p>
'''),

    # 34 — the offer restated, same shape as the standalone offer panel so it
    #      lands as the thing they have already been shown.
    ('the-offer-again', 'The offer again', '''
  <p class="lead">Just to revisit the offer</p>
  <p class="say" style="font-size:38px; max-width:640px">
    We build and launch your ads<br>funnel in the next 14 days.<br>
    You only pay us
    <span class="say__mark">from the revenue we generate</span>.
  </p>
'''),

    # 35 — one quiet line before the numbers.
    ('pricing-is-simple', 'Pricing is simple', '''
  <p class="big" style="font-size:52px">And the pricing<br>behind it is<br>pretty simple.</p>
'''),

    # 36 — two components, so two cards, with the term that qualifies both
    #      sitting under them rather than inside either.
    ('setup-fee-and-revshare', 'Setup fee and revenue share', '''
  <div class="duo">
    <div><h4>A credited setup fee</h4><p>Credited, not charged upfront.</p></div>
    <div><h4>A gross revenue share</h4><p>On the revenue we generate for you.</p></div>
  </div>
  <p class="sub" style="margin-top:34px; max-width:600px">
    For the first six months, extendable from there.
  </p>
'''),

    # 37 — the word that needs explaining, and the explanation. The rule sits on
    #      the word, not on the sentence.
    ('credited-not-upfront', 'Credited, not upfront', '''
  <p class="lead">I say <span class="say__mark">credited</span> setup fee</p>
  <p class="big" style="font-size:52px">because we don&rsquo;t<br>charge you upfront.</p>
'''),
    # 38 — the claim on its own. Nothing to read past it.
    ('no-risk', 'No risk on your end', '''
  <p class="big">There is no risk,<br>literally, on<br>your end.</p>
'''),

    # 39 — the mechanism, stated once, with the word that carries it marked.
    ('we-front-the-setup-fee', 'We front the setup fee', '''
  <p class="lead">The way the setup fee works</p>
  <p class="big" style="font-size:50px">We front you<br>the setup fee.</p>
  <p class="say" style="margin-top:30px; font-size:28px; color:var(--blue); max-width:600px">
    You get it as <span class="say__mark">credit</span>.
  </p>
'''),

    # 40 — a number slide. The figure is the whole argument here.
    ('zero-upfront', 'Zero upfront', '''
  <p class="hero">$0</p>
  <p class="say" style="margin-top:26px; font-size:34px">upfront.</p>
  <p class="sub" style="margin-top:34px; max-width:620px">
    We build and launch the entire ads funnel<br>before you pay anything.
  </p>
'''),

    # 41 — the credit clearing, drawn as a bar that fills. Describing it takes
    #      two sentences; showing it takes one glance.
    ('credit-clears', 'The credit clears', '''
  <div class="art">
    <div class="barlab"><span>Setup fee credit</span><b>Paid in full</b></div>
    <div class="bar"><span style="width:100%"></span></div>
  </div>
  <p class="say" style="max-width:640px">
    The first closes we generate<br>go against that credit.
  </p>
'''),

    # 42 — a definition, so it is set as the equation it is.
    ('gross-revenue-share', 'Gross revenue share', '''
  <p class="lead">Gross revenue share</p>
  <div class="art" style="margin-bottom:34px">
    <div class="eq"><span>Cash collected</span><i>&minus;</i><span>Ad spend</span></div>
  </div>
  <p class="art" style="margin:0"><span class="tag">For the next six months</span></p>
  <p class="sub" style="margin-top:30px; max-width:600px">From there, only the revenue share continues.</p>
'''),

    # 43 — where it goes, in the accent, since that is the promise.
    ('scale-together', 'Scale together', '''
  <p class="lead">Working together</p>
  <p class="big" style="font-size:50px">To scale to multiple<br>six and seven figures.</p>
  <p class="sub" style="max-width:600px">Over the next couple of months.</p>
'''),

    # 44 — a conditional, so the two halves get two weights: the condition
    #      quiet, the consequence in full ink.
    ('only-if-you-do', 'We only make money if you do', '''
  <p class="say" style="font-size:36px; color:var(--ink-3); max-width:620px">
    We only make money
  </p>
  <p class="big" style="margin-top:14px; font-size:50px">if we make<br>you money.</p>
  <p class="sub" style="margin-top:34px; max-width:600px">Both aligned on the same goal.</p>
'''),

    # 45 — the closing tally, deliberately the same shape as the one earlier in
    #      the run so it reads as the ledger being settled.
    ('full-clarity', 'Full clarity', '''
  <p class="lead">You now have full clarity on</p>
  <div class="check">
    <div class="done"><em>&#10003;</em><span>The offer</span></div>
    <div class="done"><em>&#10003;</em><span>The pricing structure</span></div>
    <div class="done"><em>&#10003;</em><span>The deliverables</span></div>
  </div>
'''),

    # 46 — the bridge into the ask.
    ('if-you-fall-into-this', 'If you fall into this', '''
  <p class="big" style="font-size:50px">So if this offer<br>is for you&hellip;</p>
'''),

    # 47 — the arrow points down because the thing it points at is literally
    #      below the video.
    ('application-below', 'Application below', '''
  <p class="lead">Below this video</p>
  <div class="art">
    <svg viewBox="0 0 60 76" width="60" height="76" fill="none" aria-hidden="true">
      <g stroke="#0071E3" stroke-width="5" stroke-linecap="round" stroke-linejoin="round">
        <path d="M30 8 V 60"/><path d="M13 45 L 30 64 L 47 45"/></g>
    </svg>
  </div>
  <div class="tiles" style="flex-direction:column; gap:16px">
    <div class="pill pill--in" style="width:520px; font-size:26px; justify-content:center">
      <span>There is an application</span>
    </div>
    <div class="pill pill--in" style="width:520px; font-size:26px; margin:0; justify-content:center">
      <span>Book a call with me personally</span>
    </div>
  </div>
'''),

    # 48 — two moves on the call, so two numbered beats.
    ('on-that-call', 'On that call', '''
  <p class="lead">On that call</p>
  <div class="parts">
    <div class="part">
      <svg viewBox="0 0 42 42"><circle cx="21" cy="13" r="7"/>
        <path d="M7 36 C 7 27, 13 22, 21 22 C 29 22, 35 27, 35 36"/></svg>
      <span><b>You describe your offer</b><i>And the business as it stands</i></span>
    </div>
    <div class="part">
      <svg viewBox="0 0 42 42"><path d="M21 6 V 20"/><path d="M8 20 H34"/>
        <path d="M8 20 L 4 31 H 12 Z"/><path d="M34 20 L 30 31 H 38 Z"/>
        <path d="M14 36 H28"/></svg>
      <span><b>We decide together</b><i>Whether it makes sense for both of us</i></span>
    </div>
  </div>
'''),

    # 49 — if it is a yes, the next two things happen fast, so the window gets
    #      the accent rather than a sentence about urgency.
    ('sign-and-start', 'Sign and start', '''
  <p class="lead">If it does</p>
  <ul class="bul" style="margin-top:0">
    <li>We sign the agreement</li>
    <li>We get to work as soon as possible</li>
  </ul>
  <p class="say" style="margin-top:40px; font-size:30px; color:var(--blue); max-width:620px">
    Your onboarding call<br>within the first 48 hours.
  </p>
'''),

    # 50 — the softest slide in the run. Grey throughout, because the point is
    #      that a no costs nothing.
    ('not-a-fit-is-fine', 'Not a fit is fine', '''
  <p class="say" style="font-size:36px; color:var(--ink-2); max-width:640px">
    And if it&rsquo;s not a good fit,<br>that&rsquo;s cool too.
  </p>
'''),

    # 51 and 52 are one beat in the script, so they are one slide.
    ('schedule-the-meeting', 'Schedule the meeting', '''
  <p class="lead">If you&rsquo;ve watched this far</p>
  <p class="say" style="font-size:30px; max-width:620px">
    You probably already know<br>this is for you.
  </p>
  <p class="big" style="margin-top:36px; font-size:52px; color:var(--blue)">
    So go ahead,<br>schedule the meeting.
  </p>
'''),

    # 53 — what happens on the call, in one line.
    ('everything-on-the-call', 'Everything on the call', '''
  <p class="big" style="font-size:48px">On the call I&rsquo;ll lay out<br>everything you<br>need to know.</p>
  <p class="sub" style="max-width:600px">Then we get to work together.</p>
'''),

    # 54 — the sign off. Nothing else on it.
    ('see-you-on-that-call', 'See you on that call', '''
  <p class="big">I&rsquo;ll see you<br>on that call.</p>
'''),
]

def _check_class_collisions():
    css = open('4pi.css').read() + open('voice-quiet.css').read()
    taken = set(re.findall(r'\.([a-zA-Z][\w-]*)', css))
    mine = set(re.findall(r'^\.([a-zA-Z][\w-]*)', HEAD, re.M)) - {'slide'}
    clash = sorted(mine & taken)
    if clash:
        raise SystemExit('class names already used by the shared stylesheets: '
                         + ', '.join(clash))


_check_class_collisions()

for name, title, body in SLIDES:
    open('slides/vsl-%s.html' % name, 'w').write(
        HEAD.replace('__TITLE__', title) + body + FOOT)
    print('wrote slides/vsl-%s.html' % name)
