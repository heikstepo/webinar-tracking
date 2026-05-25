import { ConnectorResult, Registration, SalesDay } from "./connectors/types";

export interface NamedCount {
  name: string;
  count: number;
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
}

export interface TimePoint {
  date: string;
  spend: number;
  registrations: number;
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
  };
  funnel: { stage: string; value: number; sub: string }[];
  timeline: TimePoint[];
  bySource: NamedCount[];
  byCampaign: NamedCount[];
  byAdset: NamedCount[];
  byWebinar: NamedCount[];
  closers: CloserStat[];
  recentRegistrations: Registration[];
  counts: { registrations: number; adDays: number; salesDays: number };
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
  out.forEach((c) => (c.closeRate = div(c.closes, c.callsTaken)));
  return out.sort((a, b) => b.revenue - a.revenue);
}

export function buildDashboard(r: ConnectorResult): DashboardData {
  const spend = r.ads.reduce((a, d) => a + d.spend, 0);
  const registrations = r.registrations.length;

  const scheduledCalls = r.sales.reduce((a, s) => a + s.scheduledCalls, 0);
  const callsTaken = r.sales.reduce((a, s) => a + s.callsTaken, 0);
  const offers = r.sales.reduce((a, s) => a + s.offersMade, 0);
  const closes = r.sales.reduce(
    (a, s) => a + s.oneCallCloses + s.followUpCloses,
    0,
  );
  const cashCollected = r.sales.reduce((a, s) => a + s.cashCollected, 0);
  const revenue = r.sales.reduce((a, s) => a + s.revenue, 0);

  // Merge spend / registrations / revenue onto a shared date axis.
  const tl = new Map<string, TimePoint>();
  const point = (d: string): TimePoint => {
    let p = tl.get(d);
    if (!p) {
      p = { date: d, spend: 0, registrations: 0, revenue: 0 };
      tl.set(d, p);
    }
    return p;
  };
  for (const a of r.ads) if (a.date) point(a.date).spend += a.spend;
  for (const reg of r.registrations)
    if (reg.date) point(reg.date).registrations += 1;
  for (const s of r.sales) if (s.date) point(s.date).revenue += s.revenue;
  const timeline = [...tl.values()].sort((a, b) =>
    a.date.localeCompare(b.date),
  );

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
    closers: closerStats(r.sales),
    recentRegistrations: [...r.registrations]
      .sort((a, b) => b.date.localeCompare(a.date))
      .slice(0, 25),
    counts: {
      registrations: r.registrations.length,
      adDays: r.ads.length,
      salesDays: r.sales.length,
    },
  };
}
