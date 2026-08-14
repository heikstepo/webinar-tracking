# Thumbnail — "The Multi-Avatar Ad Funnel"

Whiteboard-collage YouTube thumbnail background, built from the content of the Miro
boards *New Paid Ads Funnel for High Ticket Products* and its more developed copy
(Sol Twenty team).

## Render

```bash
node render.mjs
```

Outputs to `render/`:

- `thumbnail-1280x720.png` — YouTube spec size
- `thumbnail-2560x1440.png` — 2× for crisp downscaling / reframing

Requires Playwright + Chromium. The script resolves `playwright` from the project
first, then falls back to the global install.

## Presenter cutout zone

**`x: 0–345, y: 330–720`** is deliberately kept clear of diagram content. It holds
only the faint decorative wordmarks (`HIGH TICKET`, `COLD TRAFFIC`, `$40k+ offers`),
which are meant to be partially occluded — the same way the reference thumbnail runs
brand wordmarks behind the presenter.

To composite a cutout, drop it in as the last child of `#board` with
`position:absolute; left:0; bottom:0;` and a `z-index` above `59` (the paper-grain
overlay sits at `z-index:60`, so use `z-index:61` if the cutout should sit in front
of the grain, or `55` to keep the grain over it).

## Layout map (1280×720)

| Zone | Region | Content |
|---|---|---|
| A | 14,8 – 280,306 | Interest Spectrum funnel: Curious → Active Interest → Strong Intent → Convicted |
| B | 292,14 – 684,134 | One ad set · 8 distinct jobs (hook, 3 angles, offer, proof, 2 objection handlers) |
| B2 | 700,18 – 912,130 | Red-circled "5–12 ads / 1 ad set" |
| C | 948,10 – 1270,146 | "What it unlocks" checklist |
| F/G | 292,150 – 456,340 | Traffic sources + Meta / Andromeda mark |
| D | 462,146 – 948,285 | Title + subtitle bar |
| E | 466,296 – 944,356 | Four sticky notes (the non-negotiables) |
| H | 948,156 – 1270,302 | Funnel flow wireframes: Hook/Ad → VSL → Application → Calendar |
| I | 948,310 – 1270,384 | Post-booking education window |
| J | 948,392 – 1270,710 | Live assets (real screenshots), CPL heatmap, market awareness, research inputs |
| K | 352,364 – 940,545 | Four-column build: avatars → angles → education window → the call |
| L | 352,556 – 940,710 | Offer positioning pull-quote + old way / multi-avatar way contrast |

## Assets

- `assets/fonts/` — Permanent Marker (title), Caveat (headings/handwriting),
  Patrick Hand + Architects Daughter (annotations), Inter (UI/wireframe text).
  Self-hosted so the render is reproducible offline.
- `assets/img/lander.png`, `assets/img/proof.png` — funnel-page and proof-page
  screenshots pulled from the Miro board, used as the "live assets" panel.
- `assets/img/*.svg` — platform marks for the traffic cluster.

## Editing notes

- The hand-drawn look comes from `.hand` / `.hand-s`: an asymmetric
  `border-radius` with a hard offset shadow. No image textures involved.
- Arrows and circled emphasis are inline SVG in `svg.pen` blocks; strokes inherit
  `stroke-linecap:round` for a marker feel.
- `.abs` sets `position:absolute`. Any class applied alongside it must not declare
  its own `position`, or it wins on source order and the element silently falls
  back into normal flow.
