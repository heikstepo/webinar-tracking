"use client";

import { useEffect, useState } from "react";
import type { DashboardData } from "@/lib/metrics";
import { usd, usd2, int } from "@/components/format";
import { StatCard, Card, BarList } from "@/components/Panels";
import RevenueChart from "@/components/RevenueChart";

export default function Page() {
  const [data, setData] = useState<DashboardData | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  const load = () => {
    setLoading(true);
    setError(null);
    fetch("/api/dashboard")
      .then(async (r) => {
        if (!r.ok) throw new Error((await r.json()).error || r.statusText);
        return r.json();
      })
      .then(setData)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  };

  useEffect(load, []);

  return (
    <main className="mx-auto max-w-7xl px-5 py-8">
      <header className="mb-6 flex items-end justify-between">
        <div>
          <h1 className="text-xl font-semibold text-slate-50">
            Sol Twenty — Tracking Dashboard
          </h1>
          <p className="text-sm text-slate-500">
            Unified funnel & revenue across all sources · Connector 1: Airtable
          </p>
        </div>
        <button
          onClick={load}
          className="rounded-lg border border-edge bg-panel px-3 py-1.5 text-sm text-slate-300 hover:border-accent"
        >
          {loading ? "Refreshing…" : "Refresh"}
        </button>
      </header>

      {error && (
        <div className="mb-6 rounded-lg border border-red-900 bg-red-950/40 p-4 text-sm text-red-300">
          Failed to load: {error}
        </div>
      )}

      {!data && loading && (
        <div className="text-sm text-slate-500">Loading data from Airtable…</div>
      )}

      {data && (
        <div className="space-y-6">
          {/* KPI row */}
          <section className="grid grid-cols-2 gap-4 md:grid-cols-5">
            <StatCard
              label="Net Revenue"
              value={usd(data.totals.revenue)}
              sub={`${usd(data.totals.refunds)} refunded`}
            />
            <StatCard label="Sales" value={int(data.totals.sales)} />
            <StatCard label="Avg Deal" value={usd(data.totals.avgDeal)} />
            <StatCard label="Customers" value={int(data.totals.customers)} />
            <StatCard
              label="Gross Revenue"
              value={usd(data.totals.grossRevenue)}
            />
          </section>

          {/* Revenue over time */}
          <Card title="Revenue by Month">
            <RevenueChart data={data.revenueByMonth} />
          </Card>

          {/* Breakdowns */}
          <section className="grid grid-cols-1 gap-4 md:grid-cols-2">
            <Card title="Revenue by Closer">
              <BarList rows={data.byCloser} />
            </Card>
            <Card title="Revenue by Setter">
              <BarList rows={data.bySetter} />
            </Card>
            <Card title="Revenue by Product">
              <BarList rows={data.byProduct} />
            </Card>
            <Card title="Revenue by Payment Method">
              <BarList rows={data.byPaymentMethod} />
            </Card>
          </section>

          {/* Funnel (lights up when ad / EOD / UTM tables fill) */}
          <Card
            title="Acquisition Funnel"
            right={
              <span className="text-xs text-slate-500">
                {data.funnel.hasData
                  ? "live"
                  : "waiting on Ad Level / Closer EOD / UTM data"}
              </span>
            }
          >
            <div className="grid grid-cols-2 gap-3 md:grid-cols-4 lg:grid-cols-7">
              <FunnelStat label="Ad Spend" value={usd(data.funnel.spend)} />
              <FunnelStat
                label="Registrations"
                value={int(data.funnel.registrations)}
              />
              <FunnelStat label="Calls" value={int(data.funnel.calls)} />
              <FunnelStat label="Shows" value={int(data.funnel.shows)} />
              <FunnelStat label="Offers" value={int(data.funnel.offers)} />
              <FunnelStat label="Closes" value={int(data.funnel.closes)} />
              <FunnelStat
                label="Attribution rows"
                value={int(data.attributionCount)}
              />
            </div>
          </Card>

          {/* Recent sales */}
          <Card title="Recent Sales">
            <div className="overflow-x-auto">
              <table className="w-full text-left text-sm">
                <thead className="text-xs uppercase text-slate-500">
                  <tr className="border-b border-edge">
                    <th className="py-2 pr-3">Date</th>
                    <th className="py-2 pr-3">Customer</th>
                    <th className="py-2 pr-3">Product</th>
                    <th className="py-2 pr-3">Closer</th>
                    <th className="py-2 pr-3">Setter</th>
                    <th className="py-2 pr-3 text-right">Amount</th>
                  </tr>
                </thead>
                <tbody>
                  {data.recentSales.map((s) => (
                    <tr key={s.id} className="border-b border-edge/50">
                      <td className="py-2 pr-3 text-slate-400">
                        {s.date.slice(0, 10)}
                      </td>
                      <td className="py-2 pr-3 text-slate-200">{s.customer}</td>
                      <td className="py-2 pr-3 text-slate-400">{s.product}</td>
                      <td className="py-2 pr-3 text-slate-400">{s.closer}</td>
                      <td className="py-2 pr-3 text-slate-400">{s.setter}</td>
                      <td
                        className={`py-2 pr-3 text-right ${
                          s.isRefund ? "text-red-400" : "text-slate-200"
                        }`}
                      >
                        {usd2(s.amount)}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </Card>

          {data.notes.length > 0 && (
            <Card title="Connector Notes">
              <ul className="list-disc space-y-1 pl-5 text-sm text-slate-400">
                {data.notes.map((n, i) => (
                  <li key={i}>{n}</li>
                ))}
              </ul>
            </Card>
          )}

          <footer className="pt-2 text-xs text-slate-600">
            Last fetched {new Date(data.fetchedAt).toLocaleString()}
          </footer>
        </div>
      )}
    </main>
  );
}

function FunnelStat({ label, value }: { label: string; value: string }) {
  return (
    <div className="rounded-lg border border-edge bg-ink p-3">
      <div className="text-[11px] uppercase tracking-wide text-slate-500">
        {label}
      </div>
      <div className="mt-0.5 text-lg font-semibold text-slate-100">{value}</div>
    </div>
  );
}
