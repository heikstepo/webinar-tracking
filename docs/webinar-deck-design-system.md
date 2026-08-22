# Webinar Deck Design System

Reverse-engineered from the reference deck *AA — Live Class* (475 physical slides,
265 conceptual slides). This is the transferable system, not a copy: the specific
typeface and the reference deck's own copy stay with them, the **structure** is what
we reuse.

---

## 1. Canvas & grid

| Token | Value |
|---|---|
| Slide size | 10.0in × 5.625in (16:9, `9144000 × 5143500` EMU) |
| Content left margin | **0.90in** — every content block starts here |
| Content right edge | 9.10in (0.90in gutter) |
| Eyebrow left | 0.82in text / 0.60in marker dot (deliberately outdented ~0.08–0.30in) |
| First content baseline | y = **1.00–1.70in** depending on block weight |
| Bottom safe edge | 5.20in |
| Text box insets | **all zero** (`lIns/rIns/tIns/bIns = 0`), vertical anchor `ctr` |
| Line spacing | **106%** (deck-wide default) |

The 0.90in left rail is the single strongest alignment signal in the deck. 520 of the
text boxes sit on it. Everything else is a deliberate indent off that rail
(1.15 / 1.20 / 1.37 / 1.45 / 2.22).

---

## 2. Color

Four colors. That's the whole palette.

| Role | Hex | Use |
|---|---|---|
| Ink | `#0A0A0A` | All primary text; background of dark slides |
| Accent | `#EE4844` | The single accent. Inline emphasis, markers, rules, numerals, pills |
| Muted | `#9A9A9A` | Dismissed / superseded / throwaway content |
| Sub | `#545454` | Secondary list items under a heading |
| Hairline | `#C9C9C9` | Inactive bullet dots, the `—` separator in the chapter banner |
| Paper | `#FFFFFF` | Background |

**Rules that make it work:**

- **Red is never decorative.** It marks exactly one thing per line: the number, the
  dollar figure, the verb that carries the point. `"My booking page is dropping
  <red>40% of leads</red>… costing me $15k/mo."` Never a red heading *and* red body
  in the same block.
- **Grey is semantic, not a fade.** `#9A9A9A` means *this is the option we're about to
  reject*. It does not mean "previously revealed" — revealed items never restyle.
- **Dark slides are punctuation.** 30 of 475 slides (6%) are `#0A0A0A`. They are used
  only for: proof/screenshots, the recurring offer-stack slide, and the two or three
  emotional peaks. A dark slide means "look up from your notes."

---

## 3. Type

The reference uses **Sora ExtraBold at every single size, with `b="1"` on every run.**
One family, one weight, no italics, no underlines, no letter-spacing tricks.

*We swap the face.* What we keep is the discipline: **one family, one heavy weight,
size is the only hierarchy.**

| Role | Size | Color |
|---|---|---|
| Chapter banner | 11.7pt | tri-color (see §4) |
| Slide eyebrow | 11pt | ink (or white on dark) |
| Micro-label (`SELL HERE`, `Bonus`) | 11pt | accent |
| Sub-list item | 15pt | `#545454` |
| Dense row / callout body | 16–18pt | ink |
| Standard list row | 22pt | ink, accent inline |
| Statement / payoff line | 26–30pt | ink, accent inline |
| Big list line | 34pt | ink |
| Slide headline | 36–40pt | ink or accent |
| Hero title | 46pt | ink + accent |
| Part-divider numeral | **150pt** | accent |

Size gaps are large and deliberate — 11 → 22 → 30 → 46. There is no 13pt, no 20pt
filler tier. If a line needs to matter more, it jumps a whole tier.

---

## 4. The two-tier banner system

This is the signature device and the thing worth stealing wholesale.

### Tier 1 — Chapter banner (persists across a whole part)

Sits at the very top edge, centered, present on **225 slides**. It tells the viewer
which of the three acts they're in, for as long as that act lasts.

```
 •————                PART 1  —  THE AI OFFER                ————•
```

| Element | Geometry |
|---|---|
| Text box | x 1.40, y 0.06, w 7.19, h 0.40, **centered**, 11.7pt |
| Text runs | `PART 1` accent · `  —  ` `#C9C9C9` · `THE AI OFFER` ink |
| Left rule | straight connector, x 1.76 → 3.02, y 0.26, 0.9pt accent |
| Right rule | straight connector, x 6.98 → 8.24, y 0.26, 0.9pt accent |
| End caps | 0.05in accent circles at x 1.74 and x 8.21 (outer ends) |

The rules flank the label and stop well clear of it — they frame, they don't underline.
Rule widths flex slightly (1.26–1.32in) so the label stays optically centered as its
text length changes.

### Tier 2 — Slide eyebrow (per step)

```
 ● MONEY LEAK 1 OF 5
```

| Element | Geometry |
|---|---|
| Marker | 0.10in accent circle at x 0.60, y 0.62 |
| Label | x 0.82, y 0.50, w 8.50, h 0.34, left, 11pt, uppercase |

The eyebrow names the *step*, and it is the label that stays fixed while the body
builds underneath it. `MONEY LEAK 1 OF 5`, `BUILD STEP 4 OF 6`, `WHAT YOU GET — 1 OF 4`
— the "N OF M" form is used constantly and does a lot of work: it tells the audience
how much runway is left in this section.

---

## 5. The build mechanic (merging many slides into one)

**265 conceptual slides across 475 physical slides — 1.79 physical slides per idea.
33% of ideas are click-built.**

| Build length | Count |
|---|---|
| 1 (static) | 177 |
| 2 | 40 |
| 3 | 14 |
| 4 | 6 |
| 5 | 17 |
| 6 | 10 |
| 7 | 1 |

### How it's implemented

Each step is a **full duplicate of the previous slide with one more shape group
added**. Nothing moves, nothing resizes, nothing changes color between steps. The
final state is designed first; earlier states are that same layout with the later
shapes deleted. Advancing is a plain slide change, so it reads as an animation with
zero animation timing to maintain and no risk of a mistimed click.

### What gets added per click

One **semantic unit**, not one line of text. A unit is usually a marker + text pair,
sometimes marker + label + value triple:

```
step 1:  eyebrow + heading
step 2:  + row 1  (dot 0.08 @ x0.95  +  text @ x1.20)
step 3:  + row 2
step 4:  + row 3
step 5:  + row 4
step 6:  + THE CALLOUT  (accent bar 0.06×0.62 @ x0.90 + "SELL HERE" label + payoff)
```

### The size gradient inside one built slide

This is the "different sizes" quality. Within a single built slide the tiers are
mixed on purpose, and the build walks *up* the ladder toward the payoff:

```
THE REFRAME                                       11pt  ink      ← eyebrow, static
The tool you use to fix it?                       30pt  ink      ← step 1, the setup
Could be a voice agent…                           22pt  #9A9A9A  ← step 2, throwaway
Could be a workflow…                              22pt  #9A9A9A  ← step 3, throwaway
They don't care.                                  28pt  ink+red  ← step 4, the turn
They care that the problem stops.                 28pt  ink      ← step 5, the payoff
```

Setup is biggest, the rejected options are small and grey, the payoff comes back up in
full ink with the accent on the pivot word. The *shape* of the slide carries the
argument before anyone reads it.

### Vertical rhythm

Row pitch is constant within a block and scales with the tier:

| Tier | Pitch |
|---|---|
| 15pt sub-list rows | 0.50in |
| 18pt numbered rows | 0.72in |
| 22pt quote rows | 1.18in |
| 34pt big lines | 0.95in |
| Timeline rows | 0.78in |
| Card rows (ladder) | 1.12in |

---

## 6. Component library

Six components cover essentially the whole deck.

**A. Bullet row** — 0.08in `#C9C9C9` circle @ x0.95 + 15pt `#545454` text @ x1.20,
pitch 0.50in. The dot is grey, not accent — bullets are not the point.

**B. Numbered row** — accent numeral in a 0.50×0.60 box @ x0.90 (22pt) + 18pt ink text
@ x1.45, pitch 0.72in. Used for agendas, frameworks, step lists.

**C. Callout bar** — 0.06–0.07in × 0.62in solid accent rectangle @ x0.90, then an 11pt
accent micro-label + 16pt ink payoff on one line @ x1.10. This is the "and here's the
answer" component. *(Note: this is a deliberate accent mark on a single callout — it is
not a page-edge stripe or a header bar.)*

**D. Ladder / price card** — accent bar @ x0.90, title 18pt ink @ x1.15, description
15pt `#545454` @ x1.15 (+0.45in), value **right-aligned** accent @ x7.30 w1.90.
Row pitch 1.12in. The right-aligned value column is what makes it read as a table
without drawing a single table line.

**E. Chat CTA** — centered 36pt statement, then a `roundRect` pill **3.20 × 0.70** at
x3.40 (dead center), accent fill, 13pt white centered label `TYPE IN THE CHAT`.
Appears 9 times at exact intervals — it is the engagement heartbeat of the webinar.

**F. Vertical stack timeline** (the offer-stack slide) — 2pt `#2E2E2E` vertical
connector at x1.05, accent **donut** nodes (0.20in accent circle + 0.10in background-
colored circle inside) at x0.95, code @ x1.37, label @ x2.22, pitch 0.385in.
The newest item is a **solid** 0.30in accent node plus a `JUST ADDED` accent pill
(1.45 × 0.34) right-aligned at x7.95.

Component F is the most important one in the deck: it is a single conceptual slide
that **returns 10 separate times** across the offer section, growing by one node each
time. It's always dark. It is the running scoreboard.

---

## 7. Slide archetypes

| Archetype | Recipe |
|---|---|
| **Hero** | eyebrow · 46pt title (ink + accent split) @ y1.70 · 26pt subline @ y3.25 · 11pt `#9A9A9A` footer note @ y4.92 |
| **One-liner** | Nothing but a 27–30pt statement, left rail, y≈0.70–1.15. Roughly a third of the deck. One thought per slide. |
| **Part divider** | eyebrow `PART ONE — WHAT TO SELL` · 150pt accent numeral @ y1.00 · 40pt accent title @ y3.15. No chapter banner (the divider *is* the banner). |
| **Build list** | eyebrow · 36–40pt heading · 4× bullet rows · callout bar. 6 clicks. |
| **Proof** | Dark slide, framed screenshots centered, minimal or no text. Let the receipt speak. |
| **Chat CTA** | Component E. |
| **Offer stack** | Component F, dark, recurring. |

---

## 8. Rules

**Do**

- One idea per physical slide. If a slide has two thoughts, split it into a build.
- Design the final state first, then delete backwards to make the steps.
- Keep the eyebrow fixed for the whole build — it's the anchor.
- Put the accent on exactly one span per line.
- Use `N OF M` in step eyebrows.
- Let whitespace do the work. Most slides use less than half the canvas.
- Zero insets on every text box, so text aligns to the rail and not to invisible padding.

**Don't**

- Don't restyle already-revealed content between steps.
- Don't move anything between steps — a shifting layout breaks the illusion.
- Don't add a second accent color. The palette's power is that there's one.
- Don't fill the slide because it looks empty. Empty is the aesthetic.
- Don't use PowerPoint entrance animations — duplicate slides instead.
- Don't reach for a mid-tier font size to "balance" a slide. Jump a full tier or leave it.

---

## 9. Pacing (from the reference)

- ~475 slides for a ~60–75 minute class ≈ **one click every 8–9 seconds**.
- Engagement CTA (Component E) roughly every 60–70 slides.
- Dark slide at every emotional peak.
- Three acts, each opened by a part divider and carried by a persistent chapter banner.
- The offer stack returns 10 times in the close — same slide, one more node each time.
