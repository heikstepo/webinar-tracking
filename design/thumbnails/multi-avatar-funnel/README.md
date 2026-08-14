# Thumbnail — "7-Figure High Ticket Funnel"

YouTube thumbnail background built from the content of the Miro boards *New Paid Ads
Funnel for High Ticket Products* and its more developed copy (Sol Twenty team).

Variants:

| File | Look |
|---|---|
| `index.html` | Current. Off-white paper, narrow palette, ink connectors between zones, fewer and larger elements. |
| `variant-c-white.html` | Pure-white pass — seven accent colours, no connectors, twenty-odd small panels. |
| `variant-b-handdrawn.html` | Whiteboard-collage pass — hand-lettered, marker strokes, paper texture. |
| `variant-a-boxed.html` | First pass. Denser, box-per-element, UI sans for small text. |

## What makes it hang together

Three rules do most of the work. Breaking any one of them is what made
`variant-c-white.html` read as a dashboard rather than one board:

1. **Two accent colours, not seven.** Ink, red, and sticky-yellow. Every other
   colour on the board comes from a real brand mark, plus the single blue data
   table. Decorative colour — coloured card borders, per-column chip colours,
   rainbow section underlines — is what fragments the composition.
2. **Zones are connected.** Six curves run from the platform row down to the Meta
   mark, the objection pill fans into its three assets, the Meta mark feeds the
   build, and the build feeds the avatars. Without those strokes the panels float.
3. **Fewer, larger elements with real gutters.** 10-12px between neighbouring
   groups, and no panel that duplicates another. The ad-sources list and the
   ad-matrix panel were both cut as duplicates of the funnel and the ad-roles
   column; the landing-page screenshot moved inside the case-study panel rather
   than standing alone.

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

## Presenter frame

`#presenter` is a 500x368 frame flush to the bottom-left corner, sized like the
reference thumbnail. It is currently **`display:none`** — set it back to `block` once
`assets/img/presenter.png` is the real photo rather than the placeholder.

Framing is driven by custom properties on the element, so no cropping is needed
up front:

| Property | Effect |
|---|---|
| `--pflip` | `-1` un-mirrors a selfie-mode shot, `1` leaves it as filmed |
| `--px` / `--py` | `object-position` — which part of the frame is kept |
| `--pzoom` | `>1` pushes in on the face |

The canvas is filled edge to edge, so enabling the frame covers the Market Awareness,
case-study, Attribution and ad-matrix panels. That matches the reference, which runs
its wordmarks and left-hand list behind the presenter. If a specific panel needs to
stay visible, move it right rather than clearing space.

## Layout map (1280×720)

| Zone | Region | Content |
|---|---|---|
| A | 14,10 – 252,336 | Cold-traffic funnel — Awareness → Interest → Intent → Education → Close |
| B | 300,4 – 768,122 | "Where the traffic comes from" — six platform cards, curves converging on the Meta mark |
| B2 | 800,20 – 926,114 | Red-circled `5–12 ADS / 1 AD SET` |
| C | 954,8 – 1272,142 | What it unlocks — checklist |
| D | 266,136 – 476,280 | Tool-stack discs, then Objection Handling fanning into three assets |
| E | 482,100 – 652,278 | Meta Ads lockup |
| F | 660,134 – 980,264 | `*NEW* 7-FIGURE` / `HIGH TICKET FUNNEL` + subtitle bar |
| — | 266,300 – 520,356 | `$40K OFFERS` / `on cold traffic` |
| G | 600,290 – 981,352 | Four sticky notes |
| H | 1002,148 – 1272,262 | Funnel flow wireframes |
| I | 1002,272 – 1272,340 | Education window |
| P1 | 14,360 – 252,510 | Market awareness ladder |
| P2 | 14,522 – 252,712 | HYROS attribution |
| P3 | 264,360 – 470,712 | Viral Coach case study, landing page embedded |
| N | 482,360 – 950,556 | Three-column build |
| Q | 482,572 – 950,636 | Offer positioning strip |
| O | 482,652 – 928,714 | `$ $ $ BOOKED CALLS / not cheap leads` |
| J | 962,360 – 1272,492 | Four avatar cards + rule chip |
| J2 | 962,506 – 1262,564 | `SAME OFFER. / 8 DIFFERENT DOORS.` |
| K | 962,576 – 1272,712 | Proof screenshot + CPL heatmap |

## Type and colour

- **Poppins** for everything, including the title (700). 300/400 for body copy, 500
  for labels, 600 for headings and chips. Permanent Marker survives only on the three
  annotation-style bits: the circled `5-12 ADS` stat, `$40K OFFERS`, and
  `BOOKED CALLS` / `SAME OFFER`.
- Title line sizes are derived from measured advances rather than guessed:
  `*NEW*` 4.10em (tracking included), `7-FIGURE` 4.45em, `HIGH TICKET FUNNEL` 10.03em
  at weight 700. If the copy changes, re-measure and resize so both rows still fill
  the 320px measure — a ragged right edge is what made the earlier version look
  lopsided. The subtitle bar carries `white-space:nowrap` so it can never wrap to a
  second line.
- Section headings are all `.sec`, which draws one red underline. There is no
  per-section colour any more.
- Background is off-white `#f6f4ef` with a 15px dot grid. Pure white made the
  cards float; the warm paper tone sits them down.
- Containers all use the same 1.1-1.3px `--edge` outline and a single soft shadow,
  so nothing reads as more important than its content warrants.

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
