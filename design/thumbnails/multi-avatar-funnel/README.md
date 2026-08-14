# Thumbnail — "The High-Ticket Ad Playbook"

Whiteboard-collage YouTube thumbnail background, built from the content of the Miro
boards *New Paid Ads Funnel for High Ticket Products* and its more developed copy
(Sol Twenty team).

Two variants:

| File | Look |
|---|---|
| `index.html` | Current. Logo-forward, mostly unboxed, everything hand-lettered. |
| `variant-a-boxed.html` | First pass. Denser, box-per-element, UI sans for small text. |

## Render

```bash
node render.mjs             # renders index.html
```

Outputs to `render/`:

- `thumbnail-1280x720.png` — YouTube spec size
- `thumbnail-2560x1440.png` — 2× for crisp downscaling / reframing

Requires Playwright + Chromium. The script resolves `playwright` from the project
first, then falls back to the global install.

## Presenter cutout zone

**`x: 0–466, y: 352–720`** is deliberately free of diagram content. The `$40K OFFERS`
/ `ON COLD TRAFFIC` wordmarks sit just above it and the `AD SOURCES` column starts at
`x: 470`, so a cutout placed bottom-left will clip that column's left edge — which is
the intended effect (the reference runs its wordmarks and left-hand list behind the
presenter the same way).

To composite a cutout, add it as the last child of `#board` with
`position:absolute; left:0; bottom:0;`. The paper-grain overlay sits at `z-index:60`,
so use `z-index:61` to put the cutout in front of the grain, or `55` to let the grain
fall over it.

## Layout map (1280×720)

| Zone | Region | Content |
|---|---|---|
| A | 14,12 – 252,320 | Cold-traffic funnel, drawn straight on the paper: Awareness → Interest → Intent → Education → Close |
| B | 300,6 – 768,120 | "Where the traffic comes from" — six ad-platform cards with mini creative mocks |
| B2 | 800,18 – 926,114 | Red-circled `5–12 ADS / 1 AD SET` |
| C | 954,6 – 1272,142 | What it unlocks — checklist |
| D | 254,136 – 490,280 | Tool-stack discs, then Objection Handling fanning into three assets |
| E | 504,130 – 596,222 | Meta anchor mark |
| F | 628,132 – 1020,290 | Title, red underline, black subtitle bar |
| L | 254,284 – 540,350 | `$40K OFFERS` / `on cold traffic` wordmarks (presenter overlaps) |
| G | 589,290 – 948,352 | Four sticky notes — the non-negotiables |
| H | 1002,148 – 1272,262 | Funnel flow wireframes: Hook/Ad → VSL → Application → Calendar |
| I | 1002,268 – 1272,330 | Education window: pre-frame → setter → emails → closing call |
| J | 954,344 – 1272,472 | Four avatar cards + two dark rule chips |
| J2 | 958,484 – 1258,554 | `SAME OFFER. / 8 DIFFERENT DOORS.` marker callout |
| K | 954,566 – 1272,712 | Real funnel-page and proof-page screenshots + CPL heatmap |
| M | 470,356 – 550,510 | Ad sources list with platform marks |
| N | 556,356 – 945,580 | Three-column build: avatar & angle → ad roles → education window |
| O | 478,612 – 945,712 | `$ $ $ BOOKED CALLS / not cheap leads` |

## Assets

- `assets/fonts/` — Permanent Marker (display), Architects Daughter (all body and
  label lettering), Inter (subtitle bar and heatmap digits only). Self-hosted so the
  render is reproducible offline.
- `assets/img/lander.png`, `assets/img/proof.png` — funnel-page and proof-page
  screenshots pulled from the Miro board.
- `assets/img/*.svg` — the source brand marks the inline sprite was generated from.

## Editing notes

- **Logos are an inline `<symbol>` sprite, not `<img>` or CSS masks.** CSS
  `mask-image` pointing at an SVG file is silently dropped when the page is loaded
  over `file://` (opaque origin), which renders every logo invisible. The sprite
  carries `fill="currentColor"`, so `.lg-<name>{color:…}` sets the brand colour.
- Not every brand mark survives being shrunk. Zoom's mark is effectively a wordmark
  and Zapier's reads as a solid block below ~20px; both were replaced with line
  icons. Check any new logo at final size before keeping it.
- The hand-drawn look comes from `.box` / `.box-s`: an asymmetric `border-radius`
  plus a hard offset shadow. No image textures involved.
- Arrows, the funnel outline, converging strokes and circled emphasis are inline SVG
  in `svg.pen` blocks.
- `.abs` sets `position:absolute`. Any class used alongside it must not declare its
  own `position` — it would win on source order and drop the element back into
  normal flow. (This is what broke the first pass's screenshot panel.)
- Text sizes are tuned for Architects Daughter, which has a small x-height: its
  labels need ~2px more than an equivalent UI sans.
