import { ConnectorResult, Sale } from "./connectors/types";

export interface NamedTotal {
  name: string;
  revenue: number;
  count: number;
}

export interface DashboardData {
  fetchedAt: string;
  notes: string[];
  hasSales: boolean;
  totals: {
    revenue: number;
    grossRevenue: number;
    refunds: number;
    sales: number;
    avgDeal: number;
    customers: number;
  };
  revenueByMonth: { month: string; revenue: number; sales: number }[];
  byCloser: NamedTotal[];
  bySetter: NamedTotal[];
  byProduct: NamedTotal[];
  byPaymentMethod: NamedTotal[];
  recentSales: Sale[];
  funnel: {
    spend: number;
    registrations: number;
    calls: number;
    shows: number;
    offers: number;
    closes: number;
    revenue: number;
    hasData: boolean;
  };
  attributionCount: number;
}

function group(sales: Sale[], key: (s: Sale) => string): NamedTotal[] {
  const m = new Map<string, NamedTotal>();
  for (const s of sales) {
    const k = key(s) || "Unknown";
    const cur = m.get(k) || { name: k, revenue: 0, count: 0 };
    cur.revenue += s.amount;
    cur.count += 1;
    m.set(k, cur);
  }
  return [...m.values()].sort((a, b) => b.revenue - a.revenue);
}

export function buildDashboard(r: ConnectorResult): DashboardData {
  const sales = r.sales;
  const refunds = sales.filter((s) => s.isRefund);
  const grossRevenue = sales
    .filter((s) => !s.isRefund)
    .reduce((a, s) => a + s.amount, 0);
  const refundTotal = refunds.reduce((a, s) => a + Math.abs(s.amount), 0);
  const revenue = grossRevenue - refundTotal;

  const months = new Map<string, { revenue: number; sales: number }>();
  for (const s of sales) {
    const month = s.date.slice(0, 7);
    if (!month) continue;
    const cur = months.get(month) || { revenue: 0, sales: 0 };
    cur.revenue += s.isRefund ? -Math.abs(s.amount) : s.amount;
    cur.sales += 1;
    months.set(month, cur);
  }
  const revenueByMonth = [...months.entries()]
    .map(([month, v]) => ({ month, ...v }))
    .sort((a, b) => a.month.localeCompare(b.month));

  const f = r.daily.reduce(
    (acc, d) => {
      acc.spend += d.spend || 0;
      acc.registrations += d.registrations || 0;
      acc.calls += d.calls || 0;
      acc.shows += d.shows || 0;
      acc.offers += d.offers || 0;
      acc.closes += d.closes || 0;
      acc.revenue += d.revenue || 0;
      return acc;
    },
    { spend: 0, registrations: 0, calls: 0, shows: 0, offers: 0, closes: 0, revenue: 0 },
  );

  return {
    fetchedAt: r.fetchedAt,
    notes: r.notes,
    hasSales: sales.length > 0,
    totals: {
      revenue,
      grossRevenue,
      refunds: refundTotal,
      sales: sales.length,
      avgDeal: sales.length ? grossRevenue / sales.filter((s) => !s.isRefund).length : 0,
      customers: new Set(sales.map((s) => s.email || s.customer)).size,
    },
    revenueByMonth,
    byCloser: group(sales, (s) => s.closer),
    bySetter: group(sales, (s) => s.setter),
    byProduct: group(sales, (s) => s.product),
    byPaymentMethod: group(sales, (s) => s.paymentMethod),
    recentSales: [...sales]
      .sort((a, b) => b.date.localeCompare(a.date))
      .slice(0, 25),
    funnel: {
      ...f,
      hasData: r.daily.length > 0,
    },
    attributionCount: r.attribution.length,
  };
}
