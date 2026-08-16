# Thumbnail — Meta Ads Campaign Structure

Built from the *Meta Ads Campaign Structure* deck (Sol 20 Consulting, 24 slides).
The deck's argument is: 30 ads in one broad ad set wrecks sequential learning, the
wreckage gets misdiagnosed as "ad fatigue", and the fix is 1 CBO campaign with a
control ad set of 5–8 unique ads where spend is earned.

| File | Renders to | Look |
|---|---|---|
| `index.html` | `render/bold-*.png` | Dark, outlined yellow display type, red X badge, yellow arrow, graded and glowing cutout. Built to compete in a feed. |
| `variant-quiet.html` | `render/hook-*.png` | Light, deck-accurate, flat. Reads as a slide, not a thumbnail — kept for reference. |

The hook line `IT'S NOT AD FATIGUE` was dropped from the bold version on purpose:
it dies at sidebar size (see Legibility), and the claim belongs in the video
title, where it has room. Thumbnail carries the visual, title carries the claim.

## Render

```bash
python3 refine-cutout.py assets/face.png assets/face-clean.png    # despill
python3 grade-face.py assets/face-clean.png assets/face-graded.png # colour grade
node render.mjs index.html bold
node render.mjs variant-quiet.html hook
```

Each run emits 1280×720, 2560×1440, 3840×2160 and 5120×2880.

## Palette

Sampled directly out of the PDF so the thumbnail matches the video:

| Token | Value | Source |
|---|---|---|
| `--paper` | `#f5f5f7` | slide background (quiet variant) |
| `--ink` | `#1d1d1f` | slide body text (quiet variant) |
| `--red` | `#e31d3e` | the X on the "Problematic Campaign Setups" slide |
| `--gold` | `#f6b827` | the winning-ad circle on the "Let Meta Re-Allocate Spend" slide |

The bold variant pushes the same two hues for feed contrast — `#ffe019` yellow
and `#f5162f` red on a near-black field.

Red marks the discarded option and gold marks the winner — deliberately **not**
red/green. Red-green is the default convention in this niche (so it reads generic),
and ~8% of men can't separate the two hues at all, which would collapse the whole
contrast.

## Presenter cutout

Three stages, each a committed script so the whole thing is reproducible:

| Stage | Script | Output |
|---|---|---|
| Matte | rembg (below) | `assets/face.png` |
| Despill | `refine-cutout.py` | `assets/face-clean.png` |
| Grade | `grade-face.py` | `assets/face-graded.png` |

**No generative retouching happens anywhere in this pipeline** — there is no image
model in the loop. `grade-face.py` is colour work only: an S-curve, a split-tone,
a saturation lift and an unsharp pass. It makes the face read on a dark field; it
cannot change the expression.

`assets/face.png` is produced with:

```python
from rembg import remove, new_session
remove(src, session=new_session("u2net_human_seg"), alpha_matting=True,
       alpha_matting_foreground_threshold=250,
       alpha_matting_background_threshold=15,
       alpha_matting_erode_size=8)
```

`u2net_human_seg` plus alpha matting is what keeps the curly hair edge from going
crunchy. Two notes for anyone regenerating it:

- **The office chair behind his shoulders segments as part of him** — it is one
  connected component with the body, so dropping small components does not remove
  it. It is handled compositionally instead: `#face` is sized and positioned so
  everything below roughly 82% of the cutout height falls past the bottom edge.
  If you resize the face, re-check that the chair stays off-canvas.
- **The source photo is mirrored** (shot in selfie view). With the background gone
  there is no text to give it away, so it is left as-is. Set `--fflip:-1` on
  `#face` to un-mirror.
- **Matte spill is invisible on light and glaring on dark.** rembg keeps the wall
  showing through the gaps between hair strands. `refine-cutout.py` handles it by
  scoring each pixel on chroma, warmth and luminance, gating that score on
  distance from the matte edge (spill is a boundary artefact, so this keeps eye
  whites and other low-chroma interior detail safe), then sinking the spill toward
  hair tone rather than punching holes through the strands. One faint patch
  survives at the crown, more than 34px inside the silhouette; it is invisible
  below about 400px wide.

## Legibility

`render/_legibility-test.png` shows both variants at the sizes YouTube actually
serves — 360px on the home feed, 168px in the sidebar. Regenerate it after any
change and check before shipping.

Current state at 168px, bold variant: `5–8 ADS` in yellow carries the frame, the
struck `30 ADS` and the red X badge both read, and the face reads. `PER AD SET`
does not — by design, it exists to stop "5–8 ads" being misread as a per-account
total, and that only matters at sizes where it is legible.

This is why the hook line was cut. At nineteen characters no bar survives the
sidebar; it read fine at 360px and turned to mush at 168px.
