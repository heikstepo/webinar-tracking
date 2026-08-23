# Offer stack — 10 slides

The recurring offer stack, rebuilt to match AA: an eyebrow and headline that
hold still, and a spine that grows downward from a fixed top, one node per
appearance. Slide 1 shows component 1, slide 9 shows all nine, slide 10 is the
final recap with nothing newly added.

## Three strings were added

The stack had no headline, so these are new — none of them come from the
script. Change them at the top of `offer_stack.js`:

| | text |
|---|---|
| `EYEBROW` | THE TIME BASED RANGES ACADEMY |
| `HEAD_A` + `HEAD_B` | What You're **Getting** |
| `PILL` | JUST ADDED |

The eyebrow is your own product name, taken from "Introducing - The Time Based
Ranges Academy." The headline and pill are AA's phrasing.

## How it works

Row positions are computed once for all nine and reused on every slide, so
nothing moves as the stack grows. The newest row gets a solid node and turns
teal; earlier rows are hollow nodes in white.

The **JUST ADDED** pill is drawn only where the row is short enough to leave it
room — on slide 5 the component-5 label runs long, so the pill is skipped there
rather than colliding. The solid node still marks it.

Rows are 15pt, the largest size at which all nine fit; component 5 takes two
lines at that size, which is why it is the constraint.

Verified: all nine component labels intact, 0 overflows, 0 margin violations.
Needs Poppins Bold installed.

## Two versions

| file | frame |
|---|---|
| `DTR_Offer_Stack.pptx` | dark — white text on `0A0A0A` |
| `DTR_Offer_Stack_Light.pptx` | inverted — dark text on white |

Same geometry, same 15pt rows, same teal. Inverting flips four things: the
background, the text colour, the hollow node's inner fill (so the ring reads
through to whatever the ground is), and the spine (dark grey on black becomes
hairline grey on white). The teal is unchanged — it was picked to sit the same
way on both, 3.65:1 on white and 5.43:1 on the dark frame.

```bash
node offer_stack.js                                        # dark
INVERT=1 OUT=DTR_Offer_Stack_Light.pptx node offer_stack.js  # inverted
```
