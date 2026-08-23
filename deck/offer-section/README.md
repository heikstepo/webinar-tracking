# Offer section — TBR Academy

The offer block, from "Introducing - The Time Based Ranges Academy." through
"Last Slide". Same system and blue accent as the other decks. No chapter banner —
the banners belong to the 5 steps.

| | |
|---|---|
| Source lines | 162 |
| Physical slides | 161 (+ the 162nd line lives in speaker notes) |
| Conceptual slides | **115** |
| Standalone slides | **83 of 115 (72%)** |
| Merge ratio | **1.40** (vs 1.70 and 1.85 in the earlier decks) |

Merging is deliberately light. Of the 32 merged groups, every one is a pair except
seven, and each of those seven is either a list or a run of very short anaphora
lines ("Personally." / "For free." / "Until you're funded.").

## The stack

The 10 `STACK` markers are built as the reference deck's recurring offer-stack
slide: a dark frame with a vertical spine, hollow accent nodes for what's already
in, and a solid node plus an accent row for whatever was just added. It returns ten
times and grows to nine rows.

Row labels are the offer components' own headings, verbatim, split into an
accent code column (`1)`, `BONUS 1:`) and the label. The code column is
right-aligned so the mixed widths line up.

Unlike a build, these slides are minutes apart and never consecutive, so each one
is centred rather than pinned to a fixed grid — no viewer ever sees them move.

## Production markers

`STACK` and `Last Slide` are stage directions, not audience copy, so printing them
on the slides would be wrong. They are preserved in the **speaker notes** of the
slide they refer to — nothing is lost, and the presenter still sees the cue.

## Verified

All 162 source lines present intact, 0 of 531 word tokens lost, every character
preserved, 0 text overflows, 0 margin violations, and every slide carries the accent.

```bash
node measure.js                  # only after changing text or the font
OUT=DTR_Offer.pptx node build.js
```
