# 4PI Slide System

The element kit behind the *Find the weakest link* deck — so new slides land in
the same visual world instead of merely near it.

```
design/
  4pi.css               tokens + every element class
  voice-quiet.css       the typographic layer, loaded after 4pi.css
  elements.html         live reference: the read, tokens, type scale, all elements
  slide-template.html   blank starter, four layouts
  build-standalone.py   folds CSS + font into one portable file
  render.sh             slide file -> PDF + 2x PNG, via Chrome's print path
  deck-order.txt        which slides go into the deck, in order
  measure.sh/.js        read each slide's real laid-out geometry out of Chrome
  build-deck.js         -> five-pillars.pptx, native editable text
  finish-deck.py        the two patches pptxgenjs cannot write itself
  build-deck-images.js  -> the same deck as full-bleed PNGs, not editable
  proof.js              rebuild the pptx layout in HTML, in Arial, to look at it
  slides/               one file per slide
  fonts/caveat.woff2    handwriting face
```

```
./render.sh slides/funnel.html        # -> exports/funnel.pdf + funnel.png (2x)
./render.sh slides/funnel.html 3      # 3x PNG
```

Open `elements.html` in a browser to see everything rendered at slide scale.

---

## The read

What the source deck is actually doing. These are the rules the kit encodes.

**Apple's discipline, not Apple's voice.** One idea per slide, enormous negative
space, a single accent, content held off a hard left margin. But where Apple caps
headlines at weight 600 with near-neutral tracking, these run **900 at −0.022em**.
The skeleton is Cupertino; the volume is a whiteboard. That tension is the style —
copying only the restraint gives you a bland Apple knockoff, copying only the
weight gives you a loud infographic.

**Never pure white.** Everything sits on a cool near-white wash (`#F5F6F7` →
`#FCFCFD`). That single choice is what lets a white card, a white table row, and a
hairline panel all read as separate objects without a drop shadow doing the work.

**Four accents, one job each.**

| Accent | Hex | Means |
| --- | --- | --- |
| Blue | `#1877F2` | structural, neutral, "here's the frame" |
| Yellow | `#F6B827` | the idea worth keeping |
| Red | `#E31D3E` | the problem |
| Green | `#42B72A` | the good outcome |

Blue and green are Facebook's own — the palette quietly belongs to the platform
being taught. One accent per slide; the eyebrow dot carries it.

**The highlighter is the whole system.** A solid rounded block behind one phrase
per headline. Yellow keeps black text because it behaves like a real highlighter;
blue, red and green invert to white because they behave like labels. Two marks in
one headline and the hierarchy collapses.

**A human hand on a machine grid.** Caveat handwriting, outlined hand-drawn
numerals, a sagging underline, a red arrow pointing at the outlier. The geometry
stays rigid; the annotation layer is what makes it feel taught rather than
published.

**Slides are allowed to be half empty.** Several slides carry a headline and four
chips, then stop. Filling the lower third is the fastest way to break the style.

---

## Type scale

SF Pro through the system stack, so macOS engages the real optical-size axis.
These sizes and weights were recovered from the source PDF's font table — the deck
uses only these.

| Role | Class | Size | Weight |
| --- | --- | --- | --- |
| Cover statement | `.h1` | 96 | 900 |
| Big statement | `.h1--sm` | 88 | 900 |
| Section headline | `.h2` | 72 | 900 |
| Part headline | `.h3` | 60 | 900 |
| Compact headline | `.h3--sm` | 46 | 900 |
| Lede | `.lede` / `.lede--lg` | 34 / 40 | 500 |
| Card title | `.card__title` | 34 | 800 |
| Body, arrow item | `.body` | 27 | 500–700 |
| Card label | `.card__label` | 26 | 800 |
| Eyebrow, footer | `.eyebrow` | 24 | 800 |
| Handwriting | `.hand` | 26–38 | 700 |

Headlines are locked at `line-height: 1.06`. Any tighter and a `.mark` block on
one line paints over the descenders of the line above it.

---

## Elements

| Class | What it is |
| --- | --- |
| `.eyebrow` `--blue/yellow/red/green` | dot + tracked uppercase label, top-left |
| `.footer` | muted uppercase wayfinding, bottom-right |
| `.mark` `--blue/red/green/ink/soft` | the highlighter block |
| `.squiggle` | hand-drawn sagging underline |
| `.rule` | short thick accent underline |
| `.numeral` | giant outlined hand-drawn 01–04 |
| `.opener` | numeral-left / headline-right part opener |
| `.card` `--tint` `--hard` | soft tinted card, or offset-ink-shadow card |
| `.verdict` `--yes/--no` | ✓ / ✕ card header |
| `.arrows` `--trend` | → bullets, or ↑ / ↓ trend bullets |
| `.question` + `.connector` | ink question box dropping into a branch |
| `.flow` + `.spectrum` | left-to-right tiles with a gradient rail |
| `.window` + `.tbl` + `tr.flag` | Ads Manager mock with a flagged outlier row |
| `.anno` | handwritten note + curved red arrow |
| `.chip` | outlined pill |
| `.panel` | hairline container for a short question list |
| `.tree` + `.node` + `.ads` | campaign → ad set → ads hierarchy, with a fan-out bus |
| `.funnel-wrap` + `.funnel__band` | three-stage funnel; `--fw` / `--fbh` scale it |
| `.funnel__neck` + `.conversion` | the neck and the conversion falling out of it |
| `.cold` + `.person` | a cold, unaware audience pool |
| `.stage-abs` + `.branch` | fixed canvas for drawing a curve between two elements |

Set `--n` on `.tree` to the number of ad tiles; the fan-out bus computes its own
inset so it meets the outer tiles. Set `--fw`, `--fbh`, `--fsz`, `--fpz` on
`.funnel-wrap` to resize a funnel — the taper and the ad pills scale with it.

Layout helpers: `.grid-2` `.grid-3` `.grid-4` `.stack` `.stack-24` `.stack-40`,
and slide modifiers `.slide--center` `.slide--top` `.slide--bottom` `.slide--mid`.

---

## Making a deck

1. Copy `slide-template.html`. One `<section class="slide">` per slide.
2. Open in Chrome → **Print** → Destination *Save as PDF*, Margins **None**,
   Scale **100%**, **Background graphics ON**. Each slide exports as one
   1440×810 page.
3. Optional: `python3 build-standalone.py deck.html` folds the stylesheet and
   font into a single file with no external requests — portable to email, a
   sandboxed viewer, or anywhere offline.

### Exporting to PowerPoint

```
./measure.sh              # Chrome lays out every slide in deck-order.txt
node build-deck.js        # -> exports/five-pillars.pptx
python3 finish-deck.py exports/five-pillars.pptx
```

The pptx carries live text, so wording can be fixed in PowerPoint, Keynote or
Google Slides without coming back here. Positions are not guessed from the CSS —
`measure.sh` injects `measure.js` into each slide and reads the boxes back out
of Chrome with `--dump-dom`, so a heading lands where the browser actually put
it.

Two things pptxgenjs will not write, so `finish-deck.py` patches them: it emits
one `<a:pPr>` per run where the schema allows one per paragraph, and it has no
option for bullet colour, which the design needs because the bullet is accent
blue while its text is near-black.

Fonts do not survive the trip — SF Pro is not on most machines, so the deck asks
for Helvetica Neue and falls back to Arial off macOS. That is the one real
difference from the HTML, and `node proof.js && ./render.sh proof.html 1`
rebuilds the pptx's own layout in Arial so the effect can be seen before
shipping. `build-deck-images.js` is the alternative: pixel-exact, uneditable.

```html
<section class="slide slide--center">
  <div class="eyebrow eyebrow--yellow">The rule of one</div>

  <h2 class="h2">The simplest, biggest
    <span class="mark">single move</span>. Then watch.</h2>

  <p class="lede">Everything in this system is connected.
    <span class="mark mark--soft">Change multiple things at once</span>
    and you'll never know what caused the outcome.</p>

  <div class="footer">4PI · The rule of one</div>
</section>
```

---

## Briefing a new slide

The fastest brief names four things:

1. **Eyebrow + accent** — "eyebrow: DIAGNOSE, yellow"
2. **Headline, and which phrase is marked** — "Is *GPT* dropping, or is *volume*
   dropping? — mark GPT yellow, volume blue"
3. **The body shape** — two tinted cards / a flow of four / a table with one
   flagged row / four chips
4. **The content of each part**

Anything unspecified follows the rules above: one accent, one mark, ledes capped
around 1000px, lower third left empty unless the content needs it.
