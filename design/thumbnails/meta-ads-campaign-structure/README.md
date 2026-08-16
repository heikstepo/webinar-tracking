# Thumbnail — Meta Ads Campaign Structure

Built from the *Meta Ads Campaign Structure* deck (Sol 20 Consulting, 24 slides).
The deck's argument is: 30 ads in one broad ad set wrecks sequential learning, the
wreckage gets misdiagnosed as "ad fatigue", and the fix is 1 CBO campaign with a
control ad set of 5–8 unique ads where spend is earned.

| File | Renders to | Look |
|---|---|---|
| `index.html` | `render/jl-*.png` | Current. Justin Lalonde's system — see below. |
| `variant-b-bold.html` | `render/bold-*.png` | Dan James style: outlined yellow type, red X badge, gradient-blob background. |
| `variant-a-deck.html` | `render/hook-*.png` | Light, deck-accurate, flat. Reads as a slide, not a thumbnail. |

## The Lalonde system

Pulled from twelve of his thumbnails (`i.ytimg.com/vi/<id>/maxresdefault.jpg`),
because guessing at a style from memory produced the gradient-blob background in
`variant-b-bold.html` — the single clearest "AI-made" tell.

What he actually does:

1. **A real room, blurred.** Genuine depth of field, never gradient blobs. Ours is
   built from the shelf/plant half of the source headshot, so the plate is
   literally the same room the video is shot in.
2. **A cyan rim light** down the leading edge of every cutout. Non-negotiable —
   it is the thing that makes his cutouts read as composited rather than pasted.
3. **Clean white grotesque type.** No heavy outlines. Inter here; Poppins is
   geometric and reads wrong against his neutral grotesque.
4. **The blue Meta mark used literally**, at size, in brand blue.
5. **White iOS-widget cards** as evidence panels, with a coloured status pip.
6. **Red reserved** for strikes, arrows and handwritten annotations — never
   for body copy.

## Render

```bash
python3 strip-prop.py    assets/face.png           assets/face-noprop.png
python3 refine-cutout.py assets/face-noprop.png    assets/face-clean.png 980
python3 retouch-face.py  assets/face-clean.png     assets/face-retouched.png
python3 grade-face.py    assets/face-retouched.png assets/face-graded.png
node render.mjs index.html jl
node render.mjs variant-b-bold.html bold
node render.mjs variant-a-deck.html hook
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
| Strip prop | `strip-prop.py` | `assets/face-noprop.png` |
| Despill | `refine-cutout.py` | `assets/face-clean.png` |
| Retouch | `retouch-face.py` | `assets/face-retouched.png` |
| Grade | `grade-face.py` | `assets/face-graded.png` |
| Plate | inline in this README | `assets/bg-room.jpg` |

**No generative retouching happens anywhere in this pipeline** — there is no image
model in the loop. `grade-face.py` is colour work only: an S-curve, a split-tone,
a saturation lift and an unsharp pass. It makes the face read on a dark field; it
cannot change the expression.

The grade is deliberately light (S-curve 0.11, saturation 1.10, unsharp 70%). An
earlier pass at roughly double those values visibly degraded the skin.

`retouch-face.py` does frequency-separation skin work, a shadow lift and a soft
key light. **It cannot remove a beard** — that needs inpainting, which needs a
generative model. `NECK_STRENGTH` reduces the *appearance* of neck stubble by
pulling dark low-contrast pixels toward the surrounding skin tone, and it is
capped at 0.34 deliberately: the first pass ran every constant at roughly double
these values and the result was plastic, with smeared eyes and a waxy forehead.
Subtlety is the whole point — anything stronger looks obviously retouched, which
costs more trust than the blemishes do.

Eyes, brows, lashes and lips are excluded from the skin mask (`lum > 95` and
`chroma < 82`) so they stay sharp while the cheeks and forehead are calmed.

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
- **The shot is chosen for gesture direction.** Of the eight in the Drive folder,
  `s4` has a smirk, direct eye contact and a clear pointing finger. `s2` has a
  stronger expression but the gaze is averted, which costs more than the drama is
  worth in a thumbnail.
- **The flip happens in the pipeline, not in CSS.** The source is mirrored (selfie
  view), so he points off-canvas as shot; flipped, he points straight at the
  winning card. It has to be flipped on the file rather than with
  `transform:scaleX(-1)`, because a CSS transform also mirrors the rim-light
  `drop-shadow` offsets onto the wrong edge.
- **Despill must stop at the neck.** `refine-cutout.py` takes the neck row as
  argv[3] (980 for this shot). A white or grey top is neutral and unwarm —
  exactly what the spill test looks for — so letting the mask run past the neck
  eats the clothing.
- **The plate must not contain his face.** Blurring a crop that includes him
  leaves a ghost head floating in the background. This plate is built from the
  wall-and-plant strip beside him in the same shot.
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

At 168px the Lalonde version holds: `It's not ad fatigue.` reads, both cards read
as shapes with `30` struck and `5–8` in blue, and the face reads. The red
handwritten note does not — his don't either, it is a 360px-and-up flourish.

**Honest trade-off worth knowing.** The Lalonde system is lower-contrast than the
Dan James one. Side by side at 168px, `variant-b-bold.html` punches harder —
huge yellow on near-black is simply louder than white cards on a blurred room.
What the Lalonde version buys instead is looking expensive rather than shouty,
which suits a consulting offer. If raw sidebar CTR is the only goal, test the
bold variant against it rather than assuming.
