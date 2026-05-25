"use client";

import { useEffect, useState } from "react";
import type { DashboardData } from "@/lib/metrics";
import { usd, usd2, int, pct } from "@/components/format";
import { StatCard, Card, BarList } from "@/components/Panels";
import TimelineChart from "@/components/RevenueChart";

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
            App Accelerator — Webinar Funnel
          </h1>
          <p className="text-sm text-slate-500">
            Sol Twenty · live from Airtable · Ad Spend → Registrations → Calls →
            Closes
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
          <section className="grid grid-cols-2 gap-4 md:grid-cols-4 xl:grid-cols-7">
            <StatCard label="Ad Spend" value={usd(data.totals.spend)} />
            <StatCard
              label="Registrations"
              value={int(data.totals.registrations)}
              sub={`${usd2(data.totals.costPerRegistration)} / reg`}
            />
            <StatCard
              label="Calls Taken"
              value={int(data.totals.callsTaken)}
              sub={`${pct(data.totals.showRate)} show rate`}
            />
            <StatCard label="Offers" value={int(data.totals.offers)} />
            <StatCard
              label="Closes"
              value={int(data.totals.closes)}
              sub={`${pct(data.totals.closeRate)} close rate`}
            />
            <StatCard
              label="Cash Collected"
              value={usd(data.totals.cashCollected)}
            />
            <StatCard
              label="Revenue / ROAS"
              value={usd(data.totals.revenue)}
              sub={data.totals.spend ? `${data.totals.roas.toFixed(2)}x ROAS` : "—"}
            />
          </section>

          {/* Timeline */}
          <Card title="Daily Activity">
            <TimelineChart data={data.timeline} />
          </Card>

          {/* Funnel */}
          <Card title="Funnel">
            <Funnel stages={data.funnel} />
          </Card>

          {/* Attribution */}
          <section className="grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-4">
            <Card title="Registrations by Source">
              <BarList rows={data.bySource} />
            </Card>
            <Card title="Registrations by Campaign">
              <BarList rows={data.byCampaign} />
            </Card>
            <Card title="Registrations by Adset">
              <BarList rows={data.byAdset} />
            </Card>
            <Card title="Registrations by Webinar">
              <BarList rows={data.byWebinar} />
            </Card>
          </section>

          {/* Closer performance */}
          <Card
            title="Closer Performance"
            right={
              <span className="text-xs text-slate-500">
                {data.counts.salesDays
                  ? `${data.counts.salesDays} EOD reports`
                  : "waiting on Closer EOD data"}
              </span>
            }
          >
            <div className="overflow-x-auto">
              <table className="w-full text-left text-sm">
                <thead className="text-xs uppercase text-slate-500">
                  <tr className="border-b border-edge">
                    <th className="py-2 pr-3">Closer</th>
                    <th className="py-2 pr-3 text-right">Scheduled</th>
                    <th className="py-2 pr-3 text-right">Taken</th>
                    <th className="py-2 pr-3 text-right">No-Shows</th>
                    <th className="py-2 pr-3 text-right">Offers</th>
                    <th className="py-2 pr-3 text-right">Closes</th>
                    <th className="py-2 pr-3 text-right">Close %</th>
                    <th className="py-2 pr-3 text-right">Cash</th>
                    <th className="py-2 pr-3 text-right">Revenue</th>
                  </tr>
                </thead>
                <tbody>
                  {data.closers.map((c) => (
                    <tr key={c.name} className="border-b border-edge/50">
                      <td className="py-2 pr-3 text-slate-200">{c.name}</td>
                      <td className="py-2 pr-3 text-right text-slate-400">{int(c.scheduled)}</td>
                      <td className="py-2 pr-3 text-right text-slate-400">{int(c.callsTaken)}</td>
                      <td className="py-2 pr-3 text-right text-slate-400">{int(c.noShows)}</td>
                      <td className="py-2 pr-3 text-right text-slate-400">{int(c.offers)}</td>
                      <td className="py-2 pr-3 text-right text-slate-200">{int(c.closes)}</td>
                      <td className="py-2 pr-3 text-right text-slate-400">{pct(c.closeRate)}</td>
                      <td className="py-2 pr-3 text-right text-slate-400">{usd(c.cashCollected)}</td>
                      <td className="py-2 pr-3 text-right text-slate-200">{usd(c.revenue)}</td>
                    </tr>
                  ))}
                  {!data.closers.length && (
                    <tr>
                      <td colSpan={9} className="py-3 text-slate-500">
                        No Closer EOD reports yet.
                      </td>
                    </tr>
                  )}
                </tbody>
              </table>
            </div>
          </Card>

          {/* Recent registrations */}
          <Card title="Recent Registrations">
            <div className="overflow-x-auto">
              <table className="w-full text-left text-sm">
                <thead className="text-xs uppercase text-slate-500">
                  <tr className="border-b border-edge">
                    <th className="py-2 pr-3">Date</th>
                    <th className="py-2 pr-3">Name</th>
                    <th className="py-2 pr-3">Webinar</th>
                    <th className="py-2 pr-3">Source</th>
                    <th className="py-2 pr-3">Campaign</th>
                    <th className="py-2 pr-3">Adset</th>
                  </tr>
                </thead>
                <tbody>
                  {data.recentRegistrations.map((r) => (
                    <tr key={r.id} className="border-b border-edge/50">
                      <td className="py-2 pr-3 text-slate-400">{r.date}</td>
                      <td className="py-2 pr-3 text-slate-200">{r.name}</td>
                      <td className="py-2 pr-3 text-slate-400">{r.webinar}</td>
                      <td className="py-2 pr-3 text-slate-400">{r.source}</td>
                      <td className="py-2 pr-3 text-slate-400">{r.campaign}</td>
                      <td className="py-2 pr-3 text-slate-400">{r.adset}</td>
                    </tr>
                  ))}
                  {!data.recentRegistrations.length && (
                    <tr>
                      <td colSpan={6} className="py-3 text-slate-500">
                        No registrations yet.
                      </td>
                    </tr>
                  )}
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
            Last fetched {new Date(data.fetchedAt).toLocaleString()} ·{" "}
            {data.counts.registrations} regs · {data.counts.adDays} ad days ·{" "}
            {data.counts.salesDays} EOD reports
          </footer>
        </div>
      )}
    </main>
  );
}

function Funnel({
  stages,
}: {
  stages: { stage: string; value: number; sub: string }[];
}) {
  const max = Math.max(1, ...stages.map((s) => s.value));
  return (
    <div className="space-y-2">
      {stages.map((s, i) => {
        const prev = i > 0 ? stages[i - 1].value : 0;
        const conv = i > 0 && prev ? (s.value / prev) * 100 : null;
        return (
          <div key={s.stage} className="flex items-center gap-3">
            <div className="w-36 shrink-0 text-sm text-slate-300">
              {s.stage}
              <div className="text-[11px] text-slate-600">{s.sub}</div>
            </div>
            <div className="h-7 flex-1 rounded bg-ink">
              <div
                className="flex h-7 items-center rounded bg-accent/80 px-2 text-xs font-medium text-white"
                style={{ width: `${Math.max((s.value / max) * 100, 6)}%` }}
              >
                {int(s.value)}
              </div>
            </div>
            <div className="w-16 shrink-0 text-right text-xs text-slate-500">
              {conv != null ? `${conv.toFixed(0)}%` : ""}
            </div>
          </div>
        );
      })}
    </div>
  );
}
