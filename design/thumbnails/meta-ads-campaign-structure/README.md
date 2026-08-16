# Thumbnail — Meta Ads Campaign Structure

Built from the *Meta Ads Campaign Structure* deck (Sol 20 Consulting, 24 slides).
The deck's argument is: 30 ads in one broad ad set wrecks sequential learning, the
wreckage gets misdiagnosed as "ad fatigue", and the fix is 1 CBO campaign with a
control ad set of 5–8 unique ads where spend is earned.

Two variants of the same layout:

| File | Renders to | Difference |
|---|---|---|
| `index.html` | `render/hook-*.png` | Carries the hook line `IT'S NOT AD FATIGUE` |
| `variant-no-hook.html` | `render/nohook-*.png` | Numbers only, statements re-centred |

## Render

```bash
node render.mjs                              # index.html -> render/thumbnail-*.png
node render.mjs index.html hook              # explicit source + output prefix
node render.mjs variant-no-hook.html nohook
```

Each run emits 1280×720, 2560×1440, 3840×2160 and 5120×2880.

## Palette

Sampled directly out of the PDF so the thumbnail matches the video:

| Token | Value | Source |
|---|---|---|
| `--paper` | `#f5f5f7` | slide background |
| `--ink` | `#1d1d1f` | slide body text |
| `--red` | `#e31d3e` | the X on the "Problematic Campaign Setups" slide |
| `--gold` | `#f6b827` | the winning-ad circle on the "Let Meta Re-Allocate Spend" slide |
| `--dead` | `#a2a6ae` | struck-through statement |

Red marks the discarded option and gold marks the winner — deliberately **not**
red/green. Red-green is the default convention in this niche (so it reads generic),
and ~8% of men can't separate the two hues at all, which would collapse the whole
contrast.

## Presenter cutout

`assets/face.png` is a background-removed headshot, produced with:

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

## Legibility

`render/_legibility-test.png` shows both variants at the sizes YouTube actually
serves — 360px on the home feed, 168px in the sidebar. Regenerate it after any
change and check before shipping.

Current state at 168px: the two numbers read cleanly, `PER AD SET` does not (by
design — it exists to stop "5–8 ads" being misread as a per-account total), and
**the hook line goes to mush**. At nineteen characters no bar that size survives
the sidebar. It reads fine at 360px. Treat the hook as a home-feed element; the
numbers are what carry the sidebar.
