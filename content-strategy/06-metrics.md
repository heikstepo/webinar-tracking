# Metrics & Targets

The dashboard in this repo already computes every metric below. The only change needed
is **segmenting by `utm_source=youtube`** so organic separates from paid.

---

## 1. Metrics that already exist

From `lib/metrics.ts` — no new code required:

| Metric | Definition in code | Use |
|---|---|---|
| `showRate` | `callsTaken / scheduledCalls` | Booking → call quality |
| `closeRate` | `closes / callsTaken` | Sales execution |
| `offerCloseRate` | `closes / offers` | Closer skill, isolated from lead quality |
| `qualifiedCallsRate` | `offers / callsTaken` | **Application quality — the key organic metric** |
| `cashPerCall` | `cashCollected / callsTaken` | The number to optimize |
| `avgOrderValue` | `revenue / closes` | Offer pricing |
| `costPerClose` | `spend / closes` | Should trend to ~$0 on organic |
| `roas` | `revenue / spend` | Organic ROAS is effectively infinite — track it separately or it distorts blended numbers |

`qualifiedCallsRate` is the one to watch first. It answers *"is YouTube sending
buyers or tyre-kickers?"* If it runs below paid traffic, tighten the CTA
qualification language rather than chasing more views.

---

## 2. New tracking to add

**Per-video attribution** — the whole point:

| Field | Value |
|---|---|
| `utm_source` | `youtube` |
| `utm_medium` | `organic` |
| `utm_campaign` | `tbr-mentorship` |
| `utm_content` | **the 11-character video ID** |

The `Buyer` type in `lib/connectors/types.ts` already joins UTM data to payments by
email and carries `utmContent`, so closed revenue traces to a specific video with no
schema change. Add `YOUTUBE` as a `Webinar`/campaign label so organic segments cleanly
against the existing paid cohorts (`JUNE 3`, `MAY 27`, …).

Then build one view: **revenue per video**, sorted descending. That view drives the
content calendar from month two onward.

---

## 3. Targets

### Channel

| Metric | Now | Day 30 | Day 60 | Day 90 |
|---|---|---|---|---|
| Videos/month | ~5 | 8 | 8 | 8 |
| Median views/video | 5,200 | 6,000 | 8,000 | 11,000 |
| Subscribers | 25.1K | 27K | 30K | 35K |
| Videos linking to the offer | **0** | **59 + all new** | all | all |

The median-views targets are deliberately modest. Reach compounds slowly and it is
**not the primary lever** — routing and close rate are. JJ's 21,000 median took him
five months of twice-weekly publishing to build.

### Funnel (organic only)

| Metric | Day 30 | Day 60 | Day 90 |
|---|---|---|---|
| Landing page visits | 300 | 500 | 900 |
| Applications | 30 | 55 | 100 |
| Calls booked | 15 | 28 | 50 |
| Calls taken (60% show) | 9 | 17 | 30 |
| Closes (25%) | 2 | 4 | 7 |
| **Organic revenue @ $4.5k** | **$9,000** | **$18,000** | **$31,500** |

**Cumulative first 90 days: roughly $58,500 from traffic that already exists and
currently costs nothing.**

### Quality gates

| Metric | Floor | If below |
|---|---|---|
| Show rate | 55% | Add SMS + email reminders; shorten booking→call gap |
| Qualified call rate | 60% | Tighten CTA qualification; make Q7 stricter |
| Close rate | 20% | Sales problem, not a traffic problem — review call recordings |
| Application → booking | 40% | Calendar friction, or applications aren't being worked fast enough |

---

## 4. The one number that matters

**Revenue per 1,000 views.**

```
organic revenue in period / (total views in period / 1000)
```

At the Day 90 targets: ~$31,500 / 130 = **~$242 per 1,000 views**.

This single number collapses reach, routing, and sales execution into one figure, and
it makes the strategic point unmissable:

> Rauf's current revenue per 1,000 views from YouTube is **$0** — not because the
> content is bad, but because 452,500 lifetime views have been routed to a free Discord.

Improving the content raises this number by maybe 2–3x over a quarter.
**Connecting the funnel raises it from zero.** Do that first.

---

## 5. Reporting cadence

| When | Review |
|---|---|
| **Weekly (Sun)** | Applications, bookings, calls, closes — **by video**. Adjust next week's titles |
| **Monthly** | Format performance: which of the four archetypes produced calls. Rebalance the mix |
| **Quarterly** | Full rebuild of the calendar from measured revenue per video. Re-price the offer if close rate holds above 30% |
