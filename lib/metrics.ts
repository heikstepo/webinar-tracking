import {
  ConnectorResult,
  Registration,
  SalesDay,
  Buyer,
} from "./connectors/types";

export interface NamedCount {
  name: string;
  count: number;
}

export interface NamedTotal {
  name: string;
  buyers: number;
  cash: number;
}

export interface CloserStat {
  name: string;
  scheduled: number;
  callsTaken: number;
  noShows: number;
  offers: number;
  closes: number;
  cashCollected: number;
  revenue: number;
  closeRate: number; // closes / callsTaken
  offerCloseRate: number; // closes / offers
}

export interface TimePoint {
  date: string;
  spend: number;
  registrations: number;
  revenue: number;
  closes: number;
  scheduledCalls: number;
  callsTaken: number;
  cashCollected: number;
}

export interface RecentSale {
  id: string;
  date: string;
  closer: string;
  scheduledCalls: number;
  callsTaken: number;
  oneCallCloses: number;
  cashCollected: number;
  revenue: number;
}

export interface DashboardData {
  fetchedAt: string;
  notes: string[];
  totals: {
    spend: number;
    registrations: number;
    costPerRegistration: number;
    scheduledCalls: number;
    callsTaken: number;
    offers: number;
    closes: number;
    cashCollected: number;
    revenue: number;
    roas: number; // revenue / spend
    showRate: number; // callsTaken / scheduledCalls
    closeRate: number; // closes / callsTaken
    costPerClose: number; // spend / closes
    avgOrderValue: number; // revenue / closes
    cashPerCall: number; // cashCollected / callsTaken
    qualifiedCallsRate: number; // offers / callsTaken
    avgCallsPerDay: number; // callsTaken / distinct sale dates
    offerCloseRate: number; // closes / offers
  };
  funnel: { stage: string; value: number; sub: string }[];
  timeline: TimePoint[];
  bySource: NamedCount[];
  byCampaign: NamedCount[];
  byAdset: NamedCount[];
  byWebinar: NamedCount[];
  closers: CloserStat[];
  cashByCloser: { name: string; value: number }[];
  recentRegistrations: Registration[];
  recentSales: RecentSale[];
  buyerSummary: {
    totalBuyers: number; // unique emails
    totalRows: number; // payment rows
    totalCash: number;
    attributedBuyers: number;
    unattributedBuyers: number;
    attributionRate: number; // attributed / totalBuyers
    attributedCash: number;
    unattributedCash: number;
    byLog: { stripe: BuyerLogSummary; whop: BuyerLogSummary; oto: BuyerLogSummary };
  };
  buyersBySource: NamedTotal[];
  buyersByCampaign: NamedTotal[];
  buyersByAdset: NamedTotal[];
  buyersByContent: NamedTotal[];
  buyersByWebinar: NamedTotal[];
  recentBuyers: Buyer[];
  counts: { registrations: number; adDays: number; salesDays: number; buyers: number };
  range?: { from: string | null; to: string | null };
  available?: { min: string | null; max: string | null };
}

export interface BuyerLogSummary {
  rows: number;
  cash: number;
}

function buyerTally(
  buyers: Buyer[],
  key: (b: Buyer) => string,
): NamedTotal[] {
  const m = new Map<string, { name: string; emails: Set<string>; cash: number }>();
  for (const b of buyers) {
    const k = key(b) || "(unattributed)";
    let cur = m.get(k);
    if (!cur) {
      cur = { name: k, emails: new Set(), cash: 0 };
      m.set(k, cur);
    }
    if (b.email) cur.emails.add(b.email);
    cur.cash += b.amount;
  }
  return [...m.values()]
    .map((v) => ({ name: v.name, buyers: v.emails.size, cash: v.cash }))
    .sort((a, b) => b.cash - a.cash);
}

function tally(items: string[]): NamedCount[] {
  const m = new Map<string, number>();
  for (const x of items) {
    const k = x || "(none)";
    m.set(k, (m.get(k) || 0) + 1);
  }
  return [...m.entries()]
    .map(([name, count]) => ({ name, count }))
    .sort((a, b) => b.count - a.count);
}

function div(a: number, b: number): number {
  return b ? a / b : 0;
}

function closerStats(sales: SalesDay[]): CloserStat[] {
  const m = new Map<string, CloserStat>();
  for (const s of sales) {
    const cur =
      m.get(s.closer) ||
      ({
        name: s.closer,
        scheduled: 0,
        callsTaken: 0,
        noShows: 0,
        offers: 0,
        closes: 0,
        cashCollected: 0,
        revenue: 0,
        closeRate: 0,
        offerCloseRate: 0,
      } as CloserStat);
    cur.scheduled += s.scheduledCalls;
    cur.callsTaken += s.callsTaken;
    cur.noShows += s.noShows;
    cur.offers += s.offersMade;
    cur.closes += s.oneCallCloses + s.followUpCloses;
    cur.cashCollected += s.cashCollected;
    cur.revenue += s.revenue;
    m.set(s.closer, cur);
  }
  const out = [...m.values()];
  out.forEach((c) => {
    c.closeRate = div(c.closes, c.callsTaken);
    c.offerCloseRate = div(c.closes, c.offers);
  });
  return out.sort((a, b) => b.revenue - a.revenue);
}

export function buildDashboard(r: ConnectorResult): DashboardData {
  const spend = r.ads.reduce((a, d) => a + d.spend, 0);
  const registrations = r.registrations.length;

  // Operational metrics still come from Closer EOD (calendar / call activity).
  const scheduledCalls = r.sales.reduce((a, s) => a + s.scheduledCalls, 0);
  const callsTaken = r.sales.reduce((a, s) => a + s.callsTaken, 0);
  const offers = r.sales.reduce((a, s) => a + s.offersMade, 0);

  // Money + closes are ground truth from the payment logs (Stripe + Whop + OTO).
  // Closer EOD self-reports are kept only for per-closer attribution.
  const buyers = r.buyers;
  const uniqueEmails = new Set(buyers.map((b) => b.email).filter(Boolean));
  const closes = uniqueEmails.size;
  const cashCollected = buyers.reduce((a, b) => a + b.amount, 0);
  const revenue = cashCollected;

  // Merge daily series (ads, registrations, calls, payments) onto a shared
  // date axis. Money + closes per day come from the payment logs.
  const tl = new Map<string, TimePoint>();
  const point = (d: string): TimePoint => {
    let p = tl.get(d);
    if (!p) {
      p = {
        date: d,
        spend: 0,
        registrations: 0,
        revenue: 0,
        closes: 0,
        scheduledCalls: 0,
        callsTaken: 0,
        cashCollected: 0,
      };
      tl.set(d, p);
    }
    return p;
  };
  for (const a of r.ads) if (a.date) point(a.date).spend += a.spend;
  for (const reg of r.registrations)
    if (reg.date) point(reg.date).registrations += 1;
  for (const s of r.sales) {
    if (!s.date) continue;
    const p = point(s.date);
    p.scheduledCalls += s.scheduledCalls;
    p.callsTaken += s.callsTaken;
  }
  const buyerEmailsByDay = new Map<string, Set<string>>();
  for (const b of buyers) {
    if (!b.date) continue;
    const p = point(b.date);
    p.cashCollected += b.amount;
    p.revenue += b.amount;
    let set = buyerEmailsByDay.get(b.date);
    if (!set) {
      set = new Set();
      buyerEmailsByDay.set(b.date, set);
    }
    if (b.email) set.add(b.email);
  }
  for (const [date, emails] of buyerEmailsByDay) {
    point(date).closes = emails.size;
  }
  const timeline = [...tl.values()].sort((a, b) =>
    a.date.localeCompare(b.date),
  );

  const distinctSaleDates = new Set(r.sales.map((s) => s.date).filter(Boolean))
    .size;

  const closers = closerStats(r.sales);

  const attributedBuyersSet = new Set(
    buyers.filter((b) => b.attributed && b.email).map((b) => b.email),
  );
  const attributedCash = buyers
    .filter((b) => b.attributed)
    .reduce((a, b) => a + b.amount, 0);
  const totalBuyers = uniqueEmails.size;
  const totalCash = cashCollected;
  const attributedBuyers = attributedBuyersSet.size;
  const byLog = (src: Buyer["logSource"]): BuyerLogSummary => {
    const rows = buyers.filter((b) => b.logSource === src);
    return {
      rows: rows.length,
      cash: rows.reduce((a, b) => a + b.amount, 0),
    };
  };

  return {
    fetchedAt: r.fetchedAt,
    notes: r.notes,
    totals: {
      spend,
      registrations,
      costPerRegistration: div(spend, registrations),
      scheduledCalls,
      callsTaken,
      offers,
      closes,
      cashCollected,
      revenue,
      roas: div(revenue, spend),
      showRate: div(callsTaken, scheduledCalls),
      closeRate: div(closes, callsTaken),
      costPerClose: div(spend, closes),
      avgOrderValue: div(revenue, closes),
      cashPerCall: div(cashCollected, callsTaken),
      qualifiedCallsRate: div(offers, callsTaken),
      avgCallsPerDay: div(callsTaken, distinctSaleDates),
      offerCloseRate: div(closes, offers),
    },
    funnel: [
      { stage: "Registrations", value: registrations, sub: "UTM Tracking" },
      { stage: "Scheduled Calls", value: scheduledCalls, sub: "Closer EOD" },
      { stage: "Calls Taken", value: callsTaken, sub: "showed up" },
      { stage: "Offers Made", value: offers, sub: "Closer EOD" },
      { stage: "Closes", value: closes, sub: "1-call + follow-up" },
    ],
    timeline,
    bySource: tally(r.registrations.map((x) => x.source)),
    byCampaign: tally(r.registrations.map((x) => x.campaign)),
    byAdset: tally(r.registrations.map((x) => x.adset)),
    byWebinar: tally(r.registrations.map((x) => x.webinar || "(unspecified)")),
    closers,
    cashByCloser: closers
      .map((c) => ({ name: c.name, value: c.cashCollected }))
      .sort((a, b) => b.value - a.value),
    recentRegistrations: [...r.registrations]
      .sort((a, b) => b.date.localeCompare(a.date))
      .slice(0, 25),
    recentSales: [...r.sales]
      .sort((a, b) => b.date.localeCompare(a.date))
      .slice(0, 15)
      .map((s) => ({
        id: s.id,
        date: s.date,
        closer: s.closer,
        scheduledCalls: s.scheduledCalls,
        callsTaken: s.callsTaken,
        oneCallCloses: s.oneCallCloses,
        cashCollected: s.cashCollected,
        revenue: s.revenue,
      })),
    buyerSummary: {
      totalBuyers,
      totalRows: buyers.length,
      totalCash,
      attributedBuyers,
      unattributedBuyers: totalBuyers - attributedBuyers,
      attributionRate: div(attributedBuyers, totalBuyers),
      attributedCash,
      unattributedCash: totalCash - attributedCash,
      byLog: {
        stripe: byLog("stripe"),
        whop: byLog("whop"),
        oto: byLog("oto"),
      },
    },
    buyersBySource: buyerTally(buyers, (b) => b.utmSource),
    buyersByCampaign: buyerTally(buyers, (b) => b.utmCampaign),
    buyersByAdset: buyerTally(buyers, (b) => b.utmAdset),
    buyersByContent: buyerTally(buyers, (b) => b.utmContent),
    buyersByWebinar: buyerTally(buyers, (b) => b.webinar),
    recentBuyers: [...buyers]
      .sort((a, b) => b.date.localeCompare(a.date))
      .slice(0, 30),
    counts: {
      registrations: r.registrations.length,
      adDays: r.ads.length,
      salesDays: r.sales.length,
      buyers: buyers.length,
    },
  };
}
