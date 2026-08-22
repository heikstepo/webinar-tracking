# DTR Live Class — designed deck

Applies the reference deck's design system (see `../docs/webinar-deck-design-system.md`)
to `DTR_Intro__Content.pptx`, with a **blue** accent.

**Every word of the original is preserved.** Nothing was rewritten, reordered, or
deleted. The generator never types content — it pulls each string out of
`verbatim.json`, which is extracted straight from the source `.pptx`. `verify.py`
and `verify2.py` prove it: all 404 source paragraphs appear intact, 0 of 899 word
tokens lost.

## What changed

| | Source | Designed |
|---|---|---|
| Physical slides | 321 | 321 |
| Conceptual slides | 321 | **174** |
| Design | one centred text box per slide | full system |

147 source slides were **merged** into build-up slides: consecutive slides that
carry one idea now share a frame that grows by one block per click. Click count is
unchanged — the presenter's rhythm is identical, but the audience sees one slide
accumulating instead of unrelated slides flashing past.

## Rebuilding

```bash
npm install pptxgenjs
node build.js && python3 verify2.py
```

- `plan.py` — the merge plan: which source slides group into one conceptual slide, and as what kind
- `ds.js` — palette, type scale, banner + eyebrow chrome
- `build.js` — layout engine and slide kinds
- `words.json` — real Arial Bold advance widths (from `measure.js`), so line-wrap and
  autosizing are exact rather than estimated
- `overrides.json` — per-line accent and grey overrides, keyed `"sourceSlide:paragraph"`

## Knobs

- **Accent colour** — `C.accent` in `ds.js` (`2E7BF6`). Chosen to match how the
  reference red behaves in both contexts: 3.98:1 on white, 4.98:1 on the dark slides.
- **Typeface** — `FONT` in `ds.js` (Arial). One family, one weight, size is the only
  hierarchy. Swap it in this one place; re-run `measure.js` afterwards so the
  wrap metrics match the new face.
- **Anti-bulk threshold** — `splitBulky()` in `build.js`. A merge that would have to
  shrink below 21pt is split back into two slides instead of being crammed.
