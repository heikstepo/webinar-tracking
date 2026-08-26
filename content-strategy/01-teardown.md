# Teardown: JJ Simon vs. DayTradingRauf vs. the Operator

*Data pulled 2026-08-26 from full channel catalogs (all videos, not just first page)
and from the operator's two live sales pages.*

---

## 1. The headline finding

Rauf and JJ Simon have **effectively identical audience size**. They do not have
identical businesses.

| | **JJ Simon** (@itsjjsimon) | **DayTradingRauf** | |
|---|---|---|---|
| Subscribers | 25.3K | 25.1K | *dead heat* |
| Videos published | 37 | 59 | Rauf ships more |
| Channel age | ~5 months | ~12+ months | Rauf is older |
| Total views | 971,900 | 452,500 | **2.1x** |
| Median views/video | 19,000 | 5,300 | **3.6x** |
| Median, age-normalized (videos 1–6 months old) | **21,000** | **5,200** | **4.0x** |
| Where the channel sends traffic | `jj.jjsimontrades.com/schedule-call` | Discord, Telegram, IG, X | — |

The age-normalized row is the fair comparison — it removes the advantage older
videos have from more accumulation time. JJ gets **4x the views per video** with
the same subscriber count, on a channel less than half the age.

**But view count is the second problem, not the first.**

### The first problem: there is no way to buy anything

JJ Simon's channel has exactly one external destination: a booking page.
Rauf's channel links to a **free Discord** (`discord.gg/timebasedrangecommunity`),
Telegram, Instagram, and X. Not one link leads to an offer, an application, or a call.

Every one of Rauf's 452,500 views has been routed to a free room.

### What makes this urgent

This repository is a dashboard for a **paid-ads → webinar → application → call →
close** funnel. The schema (`lib/connectors/types.ts`) already models ad spend,
UTM tracking, WebinarJam registrants, Typeform applications, Calendly bookings,
closer EOD reports, and Stripe/Whop payments.

So the backend already exists and already works. It is being fed by **paid traffic
only**. The YouTube channel — 452K views of warm, intent-qualified, zero-CAC
audience — is not plugged into it.

**This is the single highest-leverage fix available, and it is a plumbing job, not a
content job.**

---

## 2. The operator's model (HanckFX Business / Create And Collect)

The referenced breakdown video is *"How We Scaled This Trader From $8k/m To
$1,2M+/month (selling trading courses)"* by **HanckFX Business**
(2.87K subs, 67 videos). The agency is **Create And Collect FZ-LLC**, founder
Alexander Baad-Jensen, Ras Al Khaimah, UAE.

> **Note on sourcing:** YouTube hard-blocked transcript retrieval from this
> environment (429 / bot-gate on every route: watch page, InnerTube player across 7
> client types, yt-dlp, headless Chromium, and four third-party transcript services).
> The model below is reconstructed from the agency's **complete 57-video catalog**,
> their **live case-study page**, and their **live sales page** — all of which state
> the mechanics explicitly. It is not reconstructed from the video's audio.

### The thesis, stated on their own case-study page

The entire business is one trade: **kill low-ticket, replace with high-ticket.**

| Client | Before | After |
|---|---|---|
| AdeelTrades | 200 members × $99/mo | **20 students × $5,000** → $100k+/mo in 30 days |
| MangoeTrades | 200 members × $49/mo | **13 students × $4,000** → $55k+/mo in 2 weeks |
| TomTrades | $20,000/mo | $325,000/mo in <30 days |
| JackTrades | $25,000/mo | $103,000/mo, sales team closing at 81% |
| KrabsTrades | $2,000/mo | $25,000+/mo, sales team closing at 65% |
| NikoTrades | $0, no brand | $33,000/mo, grew to 10k+ YT subs |
| BepoTrades | $700/mo | $25,000/mo |

Read the AdeelTrades and MangoeTrades rows carefully. Revenue went **up 10x** while
student count went **down 90%**. That is the whole strategy in one line.

### The three pillars they sell

From `createandcollect.io/implementation-call-org`:

1. **Content ecosystem** — YouTube long-form as the top of funnel
2. **Automated back-end** — "The 5-Step Backend Blueprint We Install", VSL → application → calendar
3. **Sales team** — closers working booked calls (they claim 65–81% close rates)

Their own offer is DFY buildout + consulting, sold on a "*If You Don't See Results,
You Don't Pay*" guarantee, booked through an implementation call.

### Their content catalog is itself the proof of method

All 57 of their video titles follow one pattern: **a client's before → after number**.
"$8k to $110k/mo in 30 days." "$0 to $334k/mo in 13 months." "$25k to $103,250/month
in 30 days." "$250,000 in 9 days." They practice on their own channel exactly what
they install for clients: *every title is a documented transformation with a number.*

Two of their titles state the positioning bluntly:
- *"High Ticket Trading Mentorships vs Low Ticket Trading Communities (full breakdown)"*
- *"trading is NOT gonna make you rich, selling trading courses will"*

---

## 3. JJ Simon's execution — what he actually does

### 3.1 One escalating proof number *is* the brand

His channel description is four words and a number: **"$1,500,000+ In Verifiable Prop
Firm Payouts"**.

Now watch the number move across his upload history, oldest to newest:

> $1,200,000 → $1,300,000 → $1,300,000 → $1,500,000 → $1,500,000 → $1.5M → $1.6M → $1.6M → **$1.8M**

This is the mechanism most people miss when they copy this style. It is not "put a
dollar sign in the title." It is **one cumulative, verifiable, escalating number that
functions as an identity claim** — and it grows in public, on camera, which turns a
catalog of standalone videos into a serialized story with stakes.

The data supports it: his **21 titles carrying a six-figure-or-larger claim average
31,252 views** — above his 27,867 average for dollar-titles generally, and well above
his 21,288 average for titles with no number at all.

### 3.2 A serialized show

Nine episodes of **"Road to $1M / $2.5M In Prop Firm Payouts"** — weekly payout and
trade recaps (Ep. 1 through Ep. 9). Serialized content averages 14,333 views: *below*
his channel median.

**This is important and counterintuitive.** The show is not a reach play. It is a
**trust-and-ritual play** — it converts casual viewers into returning viewers who watch
the number climb week over week. It underperforms on views and overperforms on the
thing that actually matters: making a $5,000 purchase feel safe. Do not judge this
format by its view count.

He also includes losses — *"I Lost $30,000 in Prop Firm Profits in One Day"* — which is
what makes the wins credible.

### 3.3 The five formats he rotates

| Format | Example | Job |
|---|---|---|
| Strategy reveal | "My $1,300,000 Trading Strategy (Explained in 10 Minutes)" — 40K | Reach + demonstrate competence |
| Payout/proof recap (serial) | "Every Trade And Payout From This Week ($50,000+ | Ep. 9)" — 18K | Trust + ritual |
| Belief-shift authority essay | "If You Don't Understand Prop Firms, You Don't Understand Trading" — 44K | Reframe the problem so his offer is the answer |
| Student proof | "I Flew 4 Students to Miami to Trade Live With Me" — 12K | Kill the "works for him, not me" objection |
| Story / lifestyle | "dont give up on trading... my story" — 30K | Parasocial bond |

### 3.4 The destination page

`jj.jjsimontrades.com/schedule-call`, in this exact order:

1. **Headline:** "The Quant Trading Strategy Behind My $1,800,000 In Prop Firm Payouts"
2. **Subhead:** "Will Finally Get You Funded And Consistently Profitable"
3. **VSL** ("Watch The Video")
4. **21+ five-star testimonials** — each with a name, a payout figure, and a *named prop firm* (Topstep, Lucid, Tradeify, Alpha Futures, LFF)
5. **"Exhibit C"** — his own payout receipts and certificates, screenshotted
6. **Guarantee:** "If you don't receive any payouts I will refund you 100% of your payment"
7. **Free intake form**, then **calendar** with scarcity ("A couple spots left today and tomorrow")
8. **No price shown anywhere** — price is revealed on the call

---

## 4. Rauf's actual position — assets and gaps

### 4.1 What he already has that JJ does not

**Genuinely differentiated, ownable IP.** His channel description:

> *"I'm the first in the trading industry to break down time based ranges and use real
> statistical data to show how time controls market behaviour."*

"Time Based Ranges" is a named, defensible system. JJ's "Fair Value Theory" is a
repackaging of well-trodden ICT-adjacent concepts. Rauf's statistical framing is a
**stronger moat than JJ's** — it is under-exploited, not absent.

**A working sales backend** — ads, webinar, Typeform, Calendly, closers, Stripe/Whop,
and a dashboard that already computes show rate, close rate, cash per call, and ROAS.

**A 59-video library** to re-title, re-package, and link.

### 4.2 What his own data says works

Comparing his top 15 videos against his bottom 15:

| Signal | Top 15 | Bottom 15 |
|---|---|---|
| Average views | **16,853** | 2,746 |
| Titles branding the named system (TBR / Time & Price) | **4/15** | 1/15 |
| Titles containing `$` | 4/15 | 4/15 |

**The dollar sign alone does nothing for him** — it appears equally in his best and
worst videos. What separates his winners is **(a) naming his system** and
**(b) a simplicity promise**:

- "This Asia Session Strategy is **Boring** but It Makes Money" — 45K
- "**Stupid Simple** London Session Strategy (+$42,000)" — 18K
- "I've Been Hiding The **Full Time Based Ranges System — Here It Is (A-Z)**" — 22K
- "This ONE Hour Candle Is **All You Need** (+$40,000)" — 14K
- "**30 Minutes Is All You Need** To Trade — The New York Time Based Range" — 6.1K

And his losers are abstract, or negate a mechanism instead of naming one:

- "This 6 Minutes Will Change Your 2026" — 1.4K
- "I Analysed Every Trading Day Of The Week — The Data Will Shock You" — 2.3K
- "I **Stopped Using** Chart Patterns — Here's What Actually Works" — 1.6K
- "SECRET News Trading Strategy made me $40,000" — 2.1K

> **Rule that falls out of this:** name the system, promise less work, attach one
> concrete number. Never lead with "the data will shock you" or a vague time promise.

### 4.3 The gaps, in priority order

1. **No offer destination.** Free Discord instead of a booking page. *Blocking.*
2. **No cumulative proof number.** His figures are scattered and transaction-sized —
   $190,000, $67,000, $56,700, $42,000, $40,000, $30,000, $15,000, $13,470 — never
   consolidated into one identity-scale number that escalates.
3. **No serialized show.** His only serial is "Module 1–4," which is *curriculum*
   (low intent, 2.8K–4.5K views), not *narrative*.
4. **Almost no student proof.** One video, 1K views.
5. **Cadence and trajectory.** ~5 videos/month vs JJ's ~7.4. Worse: **his best videos
   are a year old** (45K, 19K) and his recent 1–6 month median is 5,200. JJ's is
   21,000 and rising. Rauf's channel is drifting down.

---

## 5. What this means

Rauf does not have a traffic problem that content volume alone will fix. He has, in order:

1. A **routing** problem — 452K views sent to a free room
2. A **proof** problem — no single escalating number, almost no student results
3. A **format** problem — no serialized trust engine
4. A **reach** problem — 4x behind on views per video

Fixing #1 is a weekend of work and is worth more than the next six months of #4.

The plan in `02-offer-and-funnel.md` and `03-content-system.md` addresses them in that order.
