# "So far…" recap section — header + one bullet per slide

Just this section (v2 deck slides 326–331), rebuilt in the AA pattern.

| | before | after |
|---|---|---|
| Slides | 6 | 6 |
| Layout | one heading, five bullets accumulating | persistent header box, **one item per slide** |
| Item size | 14pt | **37pt** |

**Slide 1** shows the line at full size — 44pt, centred.
**Slides 2–6** demote it to a bordered header box at the top and give the whole
frame to one item: a teal numeral, then the item centred at 37pt.

All five items share one size so the section holds still as it advances, capped
at five lines each so nothing gets dense. Every character of the six source
lines is preserved; 0 word tokens lost, 0 overflows, 0 margin violations.

Needs Poppins Bold installed.

```bash
node recap_section.js      # reads plan2.json from the parent directory
```
