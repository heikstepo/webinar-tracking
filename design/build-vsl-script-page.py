#!/usr/bin/env python3
"""The VSL script page: the numbers panel, then the structure.

A page rather than a slide, so it is one self-contained file with the deck's
tokens inlined: it opens anywhere, including on a phone, with no stylesheet or
font to fetch.

The panel at the top is the dark dashboard card redone on our ground: the same
figures, the same dot matrix, our ink and our one accent.

    ./build-vsl-script-page.py    writes pages/vsl-script.html
"""
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

VIEWS, APPS = 214, 28

# (step, bullets) exactly as written
STEPS = [
    ('Offer', [
        "Lay out the entire offer statement in the first few seconds: who it&rsquo;s "
        "for, what result they get and timeframe",
        "Open Loop what&rsquo;s coming (how it works, who it&rsquo;s for, what it "
        "costs) so they have a reason to keep watching",
    ]),
    ('Proof', [
        "Right after the big claim, show why they should believe you, otherwise the "
        "promise just sounds like hype",
        "Your own results first so you come across as the expert, then client results "
        "so it&rsquo;s not just you",
        "Always specific numbers and timeframes, since vague proof is basically no "
        "proof",
    ]),
    ('Soft CTA', [
        "Give people who are already sold a way to book right away instead of forcing "
        "them through the whole video",
        "Everyone else gets permission to keep watching, so nobody feels pressured and "
        "they stay on",
        "You catch the hot leads early and keep the cold ones around",
    ]),
    ('Current State + Reframe', [
        "Describe their situation so well they think &ldquo;that&rsquo;s literally "
        "me&rdquo;, which builds trust fast",
        "Call out what they&rsquo;ve already tried and why it didn&rsquo;t work, so "
        "they don&rsquo;t think you&rsquo;re pitching the same thing",
        "Reframe it so the problem is the method, which opens the door to your Unique "
        "Mechanism",
    ]),
    ('How It Works', [
        "Quickly Explain your unique mechanism tied to the service deliverables",
        "Explain the actual deliverables",
        "Make it clear what they do vs what you do, and keep their part as small as "
        "possible",
        "Future Pace to onboarding - Walk through exactly what happens after they sign "
        "up, step by step",
    ]),
    ('What It Costs', [
        "Be upfront about price instead of hiding it, so the people who book are "
        "already okay with it",
        "Compare the cost to what the result is worth so the price feels small next to "
        "it",
        "(Optional: Take the risk away with a guarantee or some kind of safety net, so "
        "the decision feels safe)",
    ]),
    ("Who It&rsquo;s For", [
        "Disqualify first, saying who it&rsquo;s NOT for, so bad-fit leads filter "
        "themselves out before booking",
        "Then describe the ideal client clearly, so the right people feel like it was "
        "made for them",
        "Makes the offer feel exclusive instead of desperate",
    ]),
    ('CTA', [
        "Tell them exactly what happens after they click (form, call, next steps) so "
        "there&rsquo;s no uncertainty",
        "Keep it no-pressure, &ldquo;if it&rsquo;s not a fit I&rsquo;ll tell "
        "you&rdquo;, which makes booking feel low-risk",
        "Repeat the main promise from the opening so it&rsquo;s the last thing in "
        "their head when they decide",
    ]),
]

# The 28 applications, scattered through the 214 views rather than bunched:
# evenly spaced, then nudged by a fixed pattern so the eye reads it as data.
JITTER = [0, 3, -2, 4, -3, 1, 2, -4, 3, -1]
hits = set()
for k in range(APPS):
    i = int((k + 0.5) * VIEWS / APPS) + JITTER[k % len(JITTER)]
    while i in hits or not 0 <= i < VIEWS:
        i = (i + 1) % VIEWS
    hits.add(i)

DOTS = ''.join('<span class="dot%s"></span>' % (' dot--on' if i in hits else '')
               for i in range(VIEWS))

STEPS_HTML = '\n\n'.join(
    '''    <article class="step">
      <div class="step__head">
        <span class="step__n">%d</span>
        <h3 class="step__t">%s</h3>
      </div>
      <ul class="step__list">
%s
      </ul>
    </article>''' % (i + 1, name,
                     '\n'.join('        <li%s>%s</li>'
                               % (' class="step__opt"' if b.startswith('(Optional')
                                  else '', b)
                               for b in bullets))
    for i, (name, bullets) in enumerate(STEPS))

HTML = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>High-Ticket B2B VSL Script</title>
<style>
/* ============================================================================
   See build-vsl-script-page.py. A page, not a slide, so the deck's tokens are
   inlined and nothing is fetched.

   One accent, one ground, one ink ramp. The panel at the top is the dashboard
   card redone on our ground; the structure below it is a two column list, the
   step on the left and what the step has to do on the right.
   ========================================================================= */
:root {
  --ground: #F5F6F7;
  --surface: #FFFFFF;
  --ink: #1B1D20;
  --ink-2: #5A5E66;
  --ink-3: #8A9099;
  --hairline: #E3E5E8;
  --blue: #1877F2;
  --blue-tint: #E4EFFD;
  --blue-deep: #1E4E8C;
  --sans: -apple-system, BlinkMacSystemFont, 'SF Pro Display', 'SF Pro Text',
          'Helvetica Neue', Helvetica, Arial, sans-serif;
}

* { box-sizing: border-box; }

html { -webkit-text-size-adjust: 100%; }
body {
  margin: 0; background: var(--ground); color: var(--ink);
  font-family: var(--sans); -webkit-font-smoothing: antialiased;
}

/* The page is recorded with a facecam in the bottom right, so the column sits
   left of centre with the right third kept clear. It sits about halfway
   between centred and flush left, so it still reads as a page. */
.wrap {
  width: min(1000px, 94vw);
  margin: 0 auto 0 clamp(24px, 15.5vw, 300px);
  padding: 72px 0 160px;
}

/* ---- headline ------------------------------------------------------------ */
.h1 {
  margin: 0 0 44px;
  font-size: 62px; font-weight: 600; letter-spacing: -0.028em; line-height: 1.06;
  color: var(--ink);
}
.h1 i { font-style: normal; color: var(--blue); }

/* ---- the numbers panel --------------------------------------------------- */
.panel {
  background: var(--surface); border: 1px solid var(--hairline);
  border-radius: 26px; padding: 44px 48px 40px;
  box-shadow: 0 4px 24px rgba(20, 30, 50, 0.06);
}

.chip {
  display: inline-block; padding: 7px 14px; border-radius: 9px;
  background: var(--blue-tint); color: var(--blue-deep);
  font-size: 14px; font-weight: 700; letter-spacing: 0.12em; text-transform: uppercase;
}

.panel__k {
  margin: 30px 0 6px;
  font-size: 19px; font-weight: 600; letter-spacing: -0.004em; color: var(--ink-3);
}
.big {
  margin: 0; font-size: 136px; font-weight: 700; letter-spacing: -0.045em;
  line-height: 1; color: var(--blue);
}
.big span { font-size: 0.42em; letter-spacing: -0.02em; }

.panel__sub {
  margin: 22px 0 0;
  font-size: 20px; font-weight: 600; color: var(--ink-2);
}
.panel__sub b { font-weight: 700; color: var(--ink); }

/* the 214 views, 28 of which became applications */
.dots {
  display: grid; grid-template-columns: repeat(auto-fill, 12px);
  gap: 8px; margin: 30px 0 0;
}
.dot { width: 12px; height: 12px; border-radius: 50%; background: #DCE0E6; }
.dot--on { background: var(--blue); }

.legend { display: flex; gap: 28px; margin: 22px 0 0; }
.legend span {
  display: flex; align-items: center; gap: 9px;
  font-size: 16px; font-weight: 600; color: var(--ink-3);
}
.legend i { width: 11px; height: 11px; border-radius: 50%; background: #DCE0E6; }
.legend .on { background: var(--blue); }

/* three figures under a rule, the last one accented */
.stats {
  display: grid; grid-template-columns: repeat(3, 1fr); gap: 40px; margin: 40px 0 0;
}
.stat { padding-top: 22px; border-top: 2px solid var(--hairline); }
.stat--on { border-top-color: var(--blue); }
.stat__k { margin: 0; font-size: 17px; font-weight: 600; color: var(--ink-3); }
.stat__v {
  margin: 8px 0 0;
  font-size: 46px; font-weight: 700; letter-spacing: -0.028em; color: var(--ink);
}
.stat--on .stat__v { color: var(--blue); }
.stat__n { margin: 10px 0 0; font-size: 17px; font-weight: 600; color: var(--ink-3); }

/* the three costs */
.costs {
  display: grid; grid-template-columns: repeat(3, 1fr); gap: 22px; margin: 34px 0 0;
}
.cost { background: #EFF1F4; border-radius: 18px; padding: 22px 24px 24px; }
.cost__k { margin: 0; font-size: 17px; font-weight: 600; color: var(--ink-3); }
.cost__v {
  margin: 8px 0 0;
  font-size: 40px; font-weight: 700; letter-spacing: -0.03em; color: var(--ink);
}
.cost__n { margin: 10px 0 0; font-size: 16px; font-weight: 600; color: var(--ink-3); }

.note {
  margin: 36px 0 0; padding-top: 22px; border-top: 1px solid var(--hairline);
  font-size: 16px; font-weight: 600; line-height: 1.5; color: var(--ink-3);
  max-width: 740px;
}

/* ---- the structure ------------------------------------------------------- */
.steps { margin: 64px 0 0; }

.step {
  display: grid; grid-template-columns: 340px 1fr; gap: 44px;
  padding: 36px 0;
  border-top: 1px solid var(--hairline);
}
.step:last-child { border-bottom: 1px solid var(--hairline); }

.step__head { display: flex; align-items: center; gap: 18px; }
.step__n {
  flex: none; width: 48px; height: 48px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  background: var(--blue); color: #fff;
  font-size: 22px; font-weight: 700; letter-spacing: -0.01em;
}
.step__t {
  margin: 0;
  font-size: 34px; font-weight: 600; letter-spacing: -0.02em; line-height: 1.12;
  color: var(--ink);
}

.step__list { margin: 0; padding: 0; list-style: none; }
.step__list li {
  position: relative; padding-left: 28px;
  font-size: 21px; font-weight: 500; line-height: 1.5; color: var(--ink-2);
}
.step__list li + li { margin-top: 15px; }
.step__list li::before {
  content: ""; position: absolute; left: 0; top: 12px;
  width: 9px; height: 9px; border-radius: 50%; background: var(--blue);
}
.step__opt { color: var(--ink-3); }
.step__opt::before { background: #C3CAD3 !important; }

/* ---- narrow --------------------------------------------------------------- */
@media (max-width: 900px) {
  .wrap { width: auto; margin: 0; padding: 44px 20px 80px; }
  .h1 { font-size: 40px; margin-bottom: 28px; }
  .panel { padding: 28px 24px 30px; border-radius: 20px; }
  .big { font-size: 88px; }
  .stats, .costs { grid-template-columns: 1fr; gap: 20px; }
  .step { grid-template-columns: 1fr; gap: 20px; padding: 28px 0; }
  .step__t { font-size: 28px; }
  .step__list li { font-size: 18px; }
}
</style>
</head>
<body>

<main class="wrap">

  <h1 class="h1">High-Ticket B2B <i>VSL Script</i></h1>

  <section class="panel">
    <span class="chip">All Meta Ads</span>

    <p class="panel__k">VSL conversion rate</p>
    <p class="big">13.1<span>%</span></p>

    <p class="panel__sub"><b>28</b> applications from <b>214</b> VSL views</p>

    <div class="dots">__DOTS__</div>

    <div class="legend">
      <span><i></i>VSL view</span>
      <span><i class="on"></i>Became an application</span>
    </div>

    <div class="stats">
      <div class="stat">
        <p class="stat__k">VSL views</p>
        <p class="stat__v">214</p>
        <p class="stat__n">People who landed on the VSL page from an ad</p>
      </div>
      <div class="stat">
        <p class="stat__k">Applications</p>
        <p class="stat__v">28</p>
        <p class="stat__n">Completed Typeform applications</p>
      </div>
      <div class="stat stat--on">
        <p class="stat__k">VSL conversion rate</p>
        <p class="stat__v">13.1%</p>
        <p class="stat__n">Applications &divide; VSL views</p>
      </div>
    </div>

    <div class="costs">
      <div class="cost">
        <p class="cost__k">Ad spend</p>
        <p class="cost__v">$3,763.96</p>
        <p class="cost__n">Total spent on Meta ads</p>
      </div>
      <div class="cost">
        <p class="cost__k">Cost per call</p>
        <p class="cost__v">$198.10</p>
        <p class="cost__n">Ad spend &divide; 19 booked calls</p>
      </div>
      <div class="cost">
        <p class="cost__k">Ticket price</p>
        <p class="cost__v">$15,000</p>
        <p class="cost__n">Price of one closed deal</p>
      </div>
    </div>

    <p class="note">VSL views are Meta landing page views across every campaign.
      All views and applications come from the ads.</p>
  </section>

  <div class="steps">

__STEPS__

  </div>

</main>

</body>
</html>
'''

os.makedirs('pages', exist_ok=True)
path = 'pages/vsl-script.html'
open(path, 'w').write(HTML.replace('__DOTS__', DOTS).replace('__STEPS__', STEPS_HTML))
print('wrote %s (%d dots, %d of them applications)' % (path, VIEWS, len(hits)))
