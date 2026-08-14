# Thumbnail — "The High-Ticket Ad Playbook"

YouTube thumbnail background built from the content of the Miro boards *New Paid Ads
Funnel for High Ticket Products* and its more developed copy (Sol Twenty team).

Variants:

| File | Look |
|---|---|
| `index.html` | Current. White + Miro dot grid, Poppins, coloured section underlines, logo-forward, canvas filled edge to edge. |
| `variant-b-handdrawn.html` | Whiteboard-collage pass — hand-lettered, marker strokes, paper texture. |
| `variant-a-boxed.html` | First pass. Denser, box-per-element, UI sans for small text. |

## Render

```bash
python3 build-sprite.py     # only after changing assets/img/*.svg
node render.mjs
```

Outputs to `render/`, all cropped to the `#board` element:

| File | Use |
|---|---|
| `thumbnail-1280x720.png` | YouTube spec size |
| `thumbnail-2560x1440.png` | 2× |
| `thumbnail-3840x2160.png` | 4K UHD |
| `thumbnail-5120x2880.png` | 5K, for print or heavy crops |

Everything except the two screenshots is vector (text, icons, logos, rules), so the
larger sizes are genuinely sharper rather than upscaled. The screenshots are 1087px
and 602px wide at source against a 100px display box, so they hold up past 4K too.

Requires Playwright + Chromium. The script resolves `playwright` from the project
first, then falls back to a global install.

## Presenter cutout

The canvas is now filled edge to edge — there is no reserved empty zone. A cutout
placed bottom-left will cover part of the Market Awareness / Attribution / case-study
column, which is the intended behaviour: the reference thumbnail runs its wordmarks
and left-hand lists behind the presenter the same way. If you want a specific panel
to stay fully visible, swap it with one further right rather than clearing space.

Add the cutout as the last child of `#board` with
`position:absolute; left:0; bottom:0;`.

## Layout map (1280×720)

| Zone | Region | Content |
|---|---|---|
| A | 14,12 – 252,336 | Cold-traffic funnel — Awareness → Interest → Intent → Education → Close |
| B | 300,4 – 768,120 | "Where the traffic comes from" — six platform cards with colour-matched creative mocks |
| B2 | 800,18 – 926,114 | Red-circled `5–12 ADS / 1 AD SET` |
| C | 954,6 – 1272,142 | What it unlocks — checklist with coloured checkboxes |
| D | 254,136 – 490,280 | Tool-stack discs, then Objection Handling fanning into three assets |
| E | 504,130 – 596,222 | Meta anchor mark |
| F | 628,132 – 1020,290 | Title, red + amber underline, black subtitle bar |
| — | 256,286 – 520,340 | `$40K OFFERS` / `on cold traffic` wordmark |
| G | 589,290 – 948,352 | Four sticky notes — the non-negotiables |
| H | 1002,148 – 1272,262 | Funnel flow wireframes: Hook/Ad → VSL → Application → Calendar |
| I | 1002,268 – 1272,330 | Education window: pre-frame → setter → emails → closing call |
| J | 954,344 – 1272,472 | Four avatar cards + two rule chips |
| J2 | 958,484 – 1258,554 | `SAME OFFER. / 8 DIFFERENT DOORS.` callout |
| K | 954,566 – 1272,712 | Funnel-page and proof-page screenshots + CPL heatmap |
| M | 470,356 – 550,530 | Ad sources list with platform marks |
| N | 556,356 – 945,545 | Three-column build: avatar & angle → ad roles → education window |
| P1 | 14,352 – 232,528 | Market awareness ladder, mapped to which ad targets each level |
| P2 | 240,352 – 462,528 | Viral Coach case study — figures taken from the board's own landing page |
| P3 | 14,536 – 232,712 | HYROS attribution: ad click → booked → showed → closed |
| P4 | 240,536 – 462,712 | The 8 ads in one ad set, colour-coded by role |
| Q | 470,552 – 945,618 | Offer positioning strip |
| O | 494,628 – 945,700 | `$ $ $ BOOKED CALLS / not cheap leads` |

## Type and colour

- **Poppins** for everything except the display lines. 300/400 for body copy, 500 for
  labels, 600 for headings and chips. Permanent Marker is kept only for the title,
  the circled stat, and the three big wordmarks.
- Section headings use `.sec` plus a `u-*` class, which draws the coloured underline:
  `u-blue`, `u-red`, `u-green`, `u-amber`, `u-violet`, `u-teal`, `u-pink`.
- Background is `#ffffff` with a 14px grey dot grid
  (`radial-gradient(circle at 1px 1px, #d3d7de 1.05px, transparent 1.05px)`), matching
  the Miro canvas. No tint, no vignette.

## Assets

- `assets/fonts/` — Poppins 300–700 and Permanent Marker, self-hosted so the render is
  reproducible offline. The hand fonts from the earlier pass are kept for
  `variant-b-handdrawn.html`.
- `assets/img/lander.png`, `assets/img/proof.png` — funnel-page and proof-page
  screenshots pulled from the Miro board.
- `assets/img/*.svg` — source brand marks; `build-sprite.py` inlines them.

## Editing notes

- **HYROS and Viral Coach are typographic recreations**, set in Poppins with brand-ish
  colouring — not official logo files. Swap in real artwork before this goes public if
  that matters. Every other mark is the real logo from Simple Icons.
- **Logos are an inline `<symbol>` sprite, not `<img>` or CSS masks.** CSS
  `mask-image` pointing at an SVG file is silently dropped when the page is loaded over
  `file://` (opaque origin), which renders every logo invisible. `build-sprite.py`
  regenerates the sprite between the `<!--SPRITE:START-->` / `<!--SPRITE:END-->`
  markers; symbols carry `fill="currentColor"` so `.lg-<name>{color:…}` sets the colour.
- Not every brand mark survives being shrunk. Zoom's mark is effectively a wordmark and
  Zapier's reads as a solid block below ~20px; both were dropped in favour of line
  icons. Check any new logo at final size before keeping it.
- `.abs` sets `position:absolute`. Any class used alongside it must not declare its own
  `position` — it would win on source order and drop the element back into normal flow.
  (This is what broke the first pass's screenshot panel.)
