# The Offer & The Funnel

**Do this before touching content.** Every day the channel publishes without a
destination is inventory burned.

---

## 1. The offer

Mirror the *structure* of what the operator installs. Do not mirror the *claims* —
those have to be Rauf's own and documented.

| Element | Specification |
|---|---|
| **Name** | The Time Based Ranges Mentorship (or *TBR Funded Accelerator*) — build the offer name on the IP he already owns |
| **Promise** | Get funded on a prop firm and take your first payout using a time-based system, trading one 30-minute window a day |
| **Price** | **$4,000–$5,000**, one payment or 2–3 split |
| **Capacity** | 15–20 students per cohort — real scarcity, and it matches the operator's own case studies |
| **Delivery** | Live weekly calls + the TBR curriculum + trade reviews + private student channel |
| **Guarantee** | See §1.2 below — this needs care |
| **Price disclosure** | Never on the page. Revealed on the call, exactly as JJ does it |

### 1.1 Why $4k–$5k and not $99/month

From the operator's own case studies: AdeelTrades went from **200 members × $99/mo**
to **20 students × $5,000**. MangoeTrades went from **200 × $49/mo** to **13 × $4,000**.

At $4,500 average, **12 students a month is $54,000**. Rauf's channel already produces
enough traffic to make 12 sales a month plausible (see §4). Twelve high-ticket
students is also a load one person can actually serve — 200 low-ticket members is not.

The free Discord does not go away. It becomes the **top of the funnel**, not the
product: a place where prospects self-identify and get invited to apply.

### 1.2 On the guarantee — read this before copying it

JJ's page runs *"If you don't receive any payouts I will refund you 100% of your
payment."* It is a strong conversion mechanism and it is also a **real, enforceable
financial commitment** on an outcome Rauf does not fully control.

If you use it:
- Define "payout" precisely and in writing (which firms, what account size, what timeframe)
- Attach completion conditions (attended X calls, submitted Y trade journals, followed the risk rules)
- Have someone competent write the terms
- Budget for the refunds you will actually pay

A cleaner alternative that converts nearly as well: **"Stay until you're funded"** —
continued access at no extra cost until the student passes an evaluation. It costs
time instead of cash and is far easier to honour.

### 1.3 Compliance — non-negotiable

Trading education is a regulated-adjacent category and the entire strategy runs on
income claims. Rules:

- **Every number published must be documented.** Real payout receipts, real statements.
  If Rauf cannot screenshot it, it does not go in a title or a thumbnail.
- **Student testimonials need written permission** and should carry a results
  disclaimer.
- **No implied typicality.** "Results are not typical" belongs on the page.
- Do not inherit JJ's or the operator's numbers. They are theirs, and several of the
  operator's headline figures ($1.2M/month) are unverified marketing claims.

---

## 2. The funnel — build this first

### 2.1 Target architecture

```
YouTube video (organic)
   ↓  description link #1, pinned comment, end screen, channel banner
Landing page:  rauf<domain>.com/schedule-call?utm_source=youtube&utm_medium=organic&utm_content=<videoId>
   ↓
VSL (8–14 min)
   ↓
Typeform application  ──→ [Typeform Log]      ← already in the dashboard
   ↓
Calendly booking      ──→ [Calendly Log]      ← already in the dashboard
   ↓
Closer call           ──→ [Closer EOD]        ← already in the dashboard
   ↓
Stripe / Whop         ──→ [Stripe Log / Whop Log]
```

Everything downstream of the landing page **already exists and already reports into
this dashboard**. The only new build is the page and the links.

### 2.2 The landing page — copy JJ's section order exactly

It is a proven sequence. Reordering it is where people lose the conversion.

1. **Headline** — the proof number + the mechanism.
   *"The Time-Based System Behind $XXX,XXX In Verified Prop Firm Payouts"*
2. **Subhead** — the outcome.
   *"Get funded and take your first payout trading one 30-minute window a day."*
3. **VSL** — script skeleton in `04-scripts-and-templates.md`
4. **Testimonial wall** — name, payout figure, **named prop firm**. Target 10+ at
   launch, 20+ by month three. Specificity is what makes these work; "great mentor"
   converts nobody, "$40k in payouts from Lucid" converts.
5. **Rauf's own receipts** — JJ calls this section "Exhibit C." Payout screenshots,
   statements, certificates.
6. **The guarantee** (per §1.2)
7. **Application form**, then **calendar**
8. **Scarcity** — real cohort capacity, stated honestly

### 2.3 Link placement — every video, no exceptions

| Placement | Detail |
|---|---|
| Description **line 1** | Above the fold, before any text that gets truncated |
| Pinned comment | Post it yourself within 5 minutes of publish |
| End screen | Last 20 seconds — call page + next video |
| Channel banner link | Replace the current Discord link |
| Channel "Links" section | Booking page **first**, Discord second |

### 2.4 Attribution — wire it into what's already here

The Airtable base already carries `UTM Source`, `UTM Medium`, `UTM Campaign`,
`UTM Content`, `UTM Adset`, and normalizes into `Registration` in
`lib/connectors/types.ts`. Use it:

| Parameter | Value | Purpose |
|---|---|---|
| `utm_source` | `youtube` | Separates organic from paid in every dashboard view |
| `utm_medium` | `organic` | vs `paid` |
| `utm_campaign` | `tbr-mentorship` | The offer |
| `utm_content` | the 11-char **video ID** | **Per-video revenue attribution** |

`utm_content` = video ID is the important one. It answers *"which video produced
paying students"* — which is the only question that should drive the content calendar
after month two. The `Buyer` type already joins UTM data by email, so closed revenue
traces back to the specific video that produced it with no new code.

Add `YOUTUBE` as a `Webinar`/campaign label so organic segments cleanly against the
paid webinar cohorts (`JUNE 3`, `MAY 27`, etc.) already in the base.

---

## 3. Sequencing — the first 14 days

| Day | Task | Owner |
|---|---|---|
| 1–2 | Lock offer name, price, capacity, guarantee terms | Rauf |
| 1–3 | Collect every documentable payout receipt; compute **one cumulative number** | Rauf |
| 2–5 | Collect 10+ student testimonials — name, figure, firm, written permission | Rauf / VA |
| 3–6 | Record the VSL | Rauf |
| 4–7 | Build the landing page, form, calendar, UTMs | Ops |
| 7 | Swap channel banner + links Discord → booking page | Ops |
| 7–10 | **Retrofit all 59 existing videos**: new description line 1 + pinned comment | VA |
| 10–14 | Closer scripts + objection handling for organic-sourced leads | Ops |
| 14 | First video published under the new content system | Rauf |

**The day-7 to day-10 retrofit is free money.** 59 videos with 452K lifetime views are
still being watched every day and currently point at a free Discord.

---

## 4. The math — what to expect

Modelled on **current** view levels, before any content improvement.

**Assumptions** (all stated so they can be argued with and replaced by real data):

| Input | Value | Basis |
|---|---|---|
| Videos/month | 8 | Recommended cadence, up from ~5 |
| Avg views/video (month 1–2) | 6,000 | Rauf's recent median is 5,200 |
| Monthly views | 48,000 | |
| Click-through to landing page | 0.75% | Typical for a well-placed high-ticket CTA |
| Landing page → application | 10% | |
| Application → booking | 50% | |
| Booking → call taken (show rate) | 60% | Dashboard already tracks this as `showRate` |
| Call taken → close | 25% | Conservative. The operator *claims* 65–81%; treat that as marketing |
| Average order value | $4,500 | |

**Result:**

```
48,000 views → 360 page visits → 36 applications → 18 bookings
             → 11 calls taken → 2.7 closes → ~$12,150/month
```

**If reach reaches JJ's level** (21,000 median views/video → 168,000 views/month), the
same funnel produces **~9.5 closes → ~$42,500/month** from organic alone, at zero ad cost.

Two honest notes on this model:

- **Every rate here is an assumption, not a measurement.** They exist to size the
  opportunity and to be replaced by real numbers from the dashboard within 30 days.
- **The close rate is the swing factor.** At 25% the channel produces ~$12k/mo; at the
  operator's claimed 65% it produces ~$32k/mo on identical traffic. Sales execution
  matters more than view count, which is another reason to fix routing before reach.

---

## 5. What NOT to do

- **Do not delete the Discord.** Repoint it. It becomes the nurture layer and the
  testimonial source.
- **Do not put the price on the page.** JJ doesn't. The call is where a $4,500 price
  gets contextualized.
- **Do not start with content.** A better video pointing at a free Discord is a better
  video pointing at nothing.
- **Do not copy JJ's numbers, niche framing, or testimonials.** Copy the architecture.
  Rauf's Time Based Ranges IP is the differentiator — leaning on someone else's
  positioning throws away the one real advantage he has.
