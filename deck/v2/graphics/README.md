# 18 conceptual graphics

One graphic per slide, in deck order. Every one is built from **native
PowerPoint shapes** — vector, editable, recolourable. Nothing is an image.

Two builds, same geometry: `DTR_Graphics.pptx` (white) and
`DTR_Graphics_Dark.pptx` (dark). Each graphic names its target slides in the
**speaker notes**, so nothing is printed on the artwork itself.

| # | Target slides | Illustrates |
|---|---|---|
| 1 | 50–52 | Price is unpredictable, time isn't — a chaotic line against an even tick ruler |
| 2 | 95–96 | Liquidity = orders resting above the high and below the low |
| 3 | 104–110 | The time based range forming inside the dealing range, both stacks untouched |
| 4 | 129–134 | The losing loop: spike, buy, reverse, stopped out, flip, reverse again |
| 5 | 158 | Sweep one side, trade to the other — the dive through the low and the run to target |
| 6 | 239 / 243–247 | The market grades itself: 25, 50, 75 between entry and target |
| 7 | 265 | All four steps inside ~12 minutes, same order every day |
| 8 | 295 | Tip of the iceberg |
| 9 | 304–312 | Two choices — on your own, or with me |
| 10 | 448–453 | 10 spots |
| 11 | 43–46 | You see A, you do B. You see B, you do A. |
| 12 | 53–55 | The desks are open: London and New York on a 24-hour clock |
| 13 | 112–114 | Dealing range = WHERE. Time based range = WHEN. |
| 14 | 137 | It has to collect the orders first, then it turns |
| 15 | 209–216 | The entry is the part everyone obsesses over, and it decides least |
| 16 | 296–302 | Two ranges given away, the rest NDA-locked |
| 17 | 426–431 | The guarantee — until you're funded |
| 18 | 457–461 | Link, two minutes, book a call |

## One open question

**Graphic 6** marks 25 / 50 / 75 but doesn't say what happens at each level —
this version of the script doesn't state it on the slide. Send me the wording
and I'll label them.

## Colours

Teal `12977F`, ink `0A0A0A`, muted grey for anything deliberately de-emphasised
(the "everything else" mass, the resting orders in 14, option 1 in 9). Change
them at the top of `graphics.js`.

```bash
node graphics.js                                      # white
INVERT=1 OUT=DTR_Graphics_Dark.pptx node graphics.js  # dark
python3 svgpreview.py DTR_Graphics.pptx gfx.html      # SVG proof sheet
```

`svgpreview.py` renders the pptx geometry to SVG — the HTML previewer used for
the text decks draws lines as boxes and ignores rotation, so it cannot check
this kind of artwork.
