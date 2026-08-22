# Recap → transition section

A standalone deck for the block that runs from "So that's the whole model…" through
"Do you mind if I take a couple minutes to show you something I built that does
exactly that?"

Same design system and same blue accent as the main deck. **No chapter banner** —
this section sits after step 5, and the banners belong to the 5 steps.

| | |
|---|---|
| Source lines | 46 |
| Physical slides | 46 |
| Conceptual slides | **27** |
| Standalone slides | 15 |
| Merged groups | 12 — all tight pairs, except the two numbered lists |

Deliberately lighter merging than the main deck: nothing stacks more than two
thoughts on a slide except the two numbered lists, which are lists by nature.
The five yes-ladder questions are each given their own slide so the room reads one
question at a time.

Content lives in `content.txt`, one line per source line, and is loaded through
`verbatim.json` — the generator never types content, so the words cannot drift.
Verified: all 46 lines present intact, 0 of 296 word tokens lost, and every
character (including the mixed curly/straight apostrophes) preserved.

```bash
node measure.js                              # only after changing text or the font
OUT=DTR_Recap_Transition.pptx node build.js
```
