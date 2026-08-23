# DTR Webinar — v2 (full deck)

Rebuilt from `DTR_Webinar_V1_Full.pptx`, keeping every one of your edits.

| | v1 (yours) | v2 |
|---|---|---|
| Slides | 528 | 528 |
| Conceptual slides | 468 | 468 |
| **Accumulating groups** | ~200 | **16 (3%)** |
| Typeface | Arial | **Poppins Bold** |
| Accent | blue `2E7BF6` | **teal `12977F`** |
| Slides with no accent | many | **0** |

## Install Poppins before opening

The deck asks for **Poppins Bold**. If it isn't installed, PowerPoint substitutes
something else and every line re-wraps. It's a free Google font —
`fonts/Poppins-Bold.ttf` is included here; install it on any machine that will
present or edit the deck.

## What changed

**Far less merging.** Only 16 groups accumulate across 528 slides. Everything
else is one thought per slide, set large. The 16 are the seven numbered lists,
the Q&A stack, and eight moments where the stacking *is* the rhetoric —
"I keep working with you / Personally / For free / Until you're funded".

**Every slide carries the teal.** A four-stage picker: concrete values (money,
clock times, "N minutes") win first, then this deck's vocabulary (dealing range,
liquidity, double break, prop firm), then the strongest keyword on the line, and
if a line is nothing but small words the whole line goes teal the way AA does it.
At most four accented lines on any slide, so the colour still means something.

**More air.** A slide holding one short line is set at 40–52pt; anything under
15 characters takes the whole frame at up to 130pt (TIME, BUT…, 8:20.). Body
type is dominated by 40/46/52pt — the small sizes only appear inside lists and
the stack.

**The five-step structure slide** (87) uses AA's "3 parts of an agency" layout:
a large teal numeral, the step title in ink, and the descriptor after the em dash
set small and grey on its own line. Rows no longer wrap, and the slide reads as a
structure instead of five sentences.

**Modelled on AA.** The offer stack is the reference deck's recurring frame:
dark, vertical spine, hollow teal nodes for what's in, a solid node plus a teal
row for what was just added. It returns 10 times and grows to 9 rows. The Q&A
slide uses AA's `Q` marker rows. Step dividers keep the 150pt numeral.

## Your copy is untouched

The generator never types content. `recover.py` reads your v1 deck, strips the
design chrome, and reconstructs the script — verified to cover **every paragraph
in your file, zero missed**. The build then re-lays that script out.

Verified against your v1: all paragraphs present intact, 0 characters missing,
0 text overflows, 0 margin violations, file validation passes. One token, `ha`,
differs — in your file the word "has" is split across two runs as `ha` + `s`;
v2 has it as one word.

Your 18 chart images are carried onto the same slides, at the same positions.

## Rebuilding

```bash
python3 recover.py     # v1 deck -> script + images
python3 plan2.py       # script -> merge plan
node measure2.js       # real Poppins Bold metrics (needs the font installed)
node build2.js
```

- `ds2.js` — palette, type scale, accent picker, banner chrome
- `build2.js` — slide kinds: stmt, list, item, div, stack, shot
- `plan2.py` — where merging happens; the curated list is `CURATED`
