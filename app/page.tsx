"use client";

import { useEffect, useState } from "react";
import type { DashboardData } from "@/lib/metrics";
import { usd, usd2, int, pct } from "@/components/format";
import { StatCard, Card, BarList, BuyerBarList } from "@/components/Panels";
import TimelineChart from "@/components/RevenueChart";
import { DailyLine, CashByCloserChart } from "@/components/SalesCharts";

type Tab = "overview" | "sales" | "buyers";

const TABS: { id: Tab; label: string }[] = [
  { id: "overview", label: "Overview" },
  { id: "sales", label: "Sales Detail" },
  { id: "buyers", label: "Buyer Attribution" },
];

const PRESETS: { label: string; days: number | null }[] = [
  { label: "All time", days: null },
  { label: "Last 7d", days: 7 },
  { label: "Last 30d", days: 30 },
  { label: "Last 90d", days: 90 },
];

function ymd(d: Date): string {
  return d.toISOString().slice(0, 10);
}

export default function Page() {
  const [data, setData] = useState<DashboardData | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);
  const [tab, setTab] = useState<Tab>("overview");
  const [from, setFrom] = useState<string>("");
  const [to, setTo] = useState<string>("");
  const [webinar, setWebinar] = useState<string>(""); // "" = All

  const load = (opts?: { refresh?: boolean }) => {
    setLoading(true);
    setError(null);
    const q = new URLSearchParams();
    if (from) q.set("from", from);
    if (to) q.set("to", to);
    if (webinar) q.set("webinar", webinar);
    if (opts?.refresh) q.set("refresh", "1");
    const qs = q.toString();
    fetch("/api/dashboard" + (qs ? "?" + qs : ""))
      .then(async (r) => {
        if (!r.ok) throw new Error((await r.json()).error || r.statusText);
        return r.json();
      })
      .then(setData)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false));
  };

  // Refetch whenever the scope changes.
  // eslint-disable-next-line react-hooks/exhaustive-deps
  useEffect(() => load(), [from, to, webinar]);

  const applyPreset = (days: number | null) => {
    if (days == null) {
      setFrom("");
      setTo("");
      return;
    }
    const end = new Date();
    const start = new Date();
    start.setDate(end.getDate() - (days - 1));
    setFrom(ymd(start));
    setTo(ymd(end));
  };

  return (
    <main className="mx-auto max-w-7xl px-5 py-8">
      <header className="mb-4 flex flex-wrap items-end justify-between gap-3">
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
          onClick={() => load({ refresh: true })}
          className="rounded-lg border border-edge bg-panel px-3 py-1.5 text-sm text-slate-300 hover:border-accent"
        >
          {loading ? "Refreshing…" : "Refresh"}
        </button>
      </header>

      <section className="mb-4 flex flex-wrap items-center gap-2 rounded-xl border border-edge bg-panel p-3">
        <span className="text-xs uppercase tracking-wide text-slate-500">
          Date range
        </span>
        <input
          type="date"
          value={from}
          min={data?.available?.min || undefined}
          max={to || data?.available?.max || undefined}
          onChange={(e) => setFrom(e.target.value)}
          className="rounded-md border border-edge bg-ink px-2 py-1 text-sm text-slate-200 [color-scheme:dark]"
        />
        <span className="text-slate-500">→</span>
        <input
          type="date"
          value={to}
          min={from || data?.available?.min || undefined}
          max={data?.available?.max || undefined}
          onChange={(e) => setTo(e.target.value)}
          className="rounded-md border border-edge bg-ink px-2 py-1 text-sm text-slate-200 [color-scheme:dark]"
        />
        <div className="ml-auto flex flex-wrap gap-1">
          {PRESETS.map((p) => (
            <button
              key={p.label}
              onClick={() => applyPreset(p.days)}
              className="rounded-md border border-edge bg-ink px-2.5 py-1 text-xs text-slate-300 hover:border-accent hover:text-slate-100"
            >
              {p.label}
            </button>
          ))}
        </div>
        {(from || to) && (
          <button
            onClick={() => applyPreset(null)}
            className="rounded-md border border-edge px-2 py-1 text-xs text-slate-400 hover:text-slate-200"
            title="Clear range"
          >
            ✕
          </button>
        )}
      </section>

      {data?.availableWebinars && data.availableWebinars.length > 0 && (
        <nav className="mb-3 flex flex-wrap gap-1.5">
          <WebinarTab
            label="All Webinars"
            sub={`${(data.availableWebinars?.length ?? 0)} total`}
            active={!webinar}
            onClick={() => setWebinar("")}
          />
          {data.availableWebinars.map((w) => (
            <WebinarTab
              key={w}
              label={w}
              active={webinar === w}
              onClick={() => setWebinar(w)}
            />
          ))}
        </nav>
      )}

      <nav className="mb-6 flex gap-1 border-b border-edge">
        {TABS.map((t) => (
          <button
            key={t.id}
            onClick={() => setTab(t.id)}
            className={`-mb-px border-b-2 px-4 py-2 text-sm transition-colors ${
              tab === t.id
                ? "border-accent text-slate-100"
                : "border-transparent text-slate-500 hover:text-slate-300"
            }`}
          >
            {t.label}
          </button>
        ))}
      </nav>

      {webinar && data && (
        <div className="mb-6 rounded-lg border border-edge bg-panel/60 p-3 text-xs text-slate-400">
          Scoped to webinar <span className="text-slate-200">{webinar}</span> ·
          registrations / buyers matched by UTM Webinar Date (email or name).
          <span className="text-slate-300"> Ad spend</span> in the 4 days{" "}
          <em>before</em> and <span className="text-slate-300">Closer EOD</span>{" "}
          in the 4 days <em>after</em> this webinar are attributed to it (each
          day goes to the closest webinar so adjacent webinars don&apos;t
          double-count).
        </div>
      )}

      {error && (
        <div className="mb-6 rounded-lg border border-red-900 bg-red-950/40 p-4 text-sm text-red-300">
          Failed to load: {error}
        </div>
      )}

      {!data && loading && (
        <div className="text-sm text-slate-500">Loading data from Airtable…</div>
      )}

      {data && tab === "overview" && <Overview data={data} />}
      {data && tab === "sales" && <SalesDetail data={data} />}
      {data && tab === "buyers" && <BuyerAttribution data={data} />}

      {data && (
        <footer className="pt-6 text-xs text-slate-600">
          Last fetched {new Date(data.fetchedAt).toLocaleString()} ·{" "}
          {data.counts.registrations} regs · {data.counts.adDays} ad days ·{" "}
          {data.counts.salesDays} EOD reports
        </footer>
      )}
    </main>
  );
}

function Overview({ data }: { data: DashboardData }) {
  return (
    <div className="space-y-6">
      <section className="grid grid-cols-2 gap-4 md:grid-cols-4 lg:grid-cols-5">
        <StatCard label="Ad Spend" value={usd(data.totals.spend)} />
        <StatCard
          label="Registrations"
          value={int(data.totals.registrations)}
          sub={`${usd2(data.totals.costPerRegistration)} / reg`}
        />
        <StatCard label="Booked Calls" value={int(data.totals.scheduledCalls)} />
        <StatCard label="Calls Taken" value={int(data.totals.callsTaken)} />
        <StatCard
          label="Show Rate"
          value={pct(data.totals.showRate)}
          sub="calls taken / booked"
        />
        <StatCard label="Offers Made" value={int(data.totals.offers)} />
        <StatCard label="Closed Deals" value={int(data.totals.closes)} />
        <StatCard
          label="Close Rate"
          value={pct(data.totals.closeRate)}
          sub="closes / calls taken"
        />
        <StatCard label="Cash Collected" value={usd(data.totals.cashCollected)} />
        <StatCard
          label="Revenue"
          value={usd(data.totals.revenue)}
          sub={data.totals.spend ? `${data.totals.roas.toFixed(2)}x ROAS` : "—"}
        />
      </section>

      <Card title="Daily Activity">
        <TimelineChart data={data.timeline} />
      </Card>

      <Card title="Funnel">
        <Funnel stages={data.funnel} />
      </Card>

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
    </div>
  );
}

function SalesDetail({ data }: { data: DashboardData }) {
  const t = data.totals;
  return (
    <div className="space-y-6">
      <section>
        <h2 className="mb-3 text-sm font-medium text-slate-400">
          Financial Metrics
        </h2>
        <div className="grid grid-cols-2 gap-4 md:grid-cols-4">
          <StatCard
            label="Cash Collected"
            value={usd(t.cashCollected)}
            sub="total collected"
          />
          <StatCard
            label="Revenue Generated"
            value={usd(t.revenue)}
            sub="total revenue"
          />
          <StatCard
            label="Avg Order Value"
            value={usd(t.avgOrderValue)}
            sub="per closed deal"
          />
          <StatCard
            label="Cash Per Call"
            value={usd(t.cashPerCall)}
            sub="average per call"
          />
        </div>
      </section>

      <section>
        <h2 className="mb-3 text-sm font-medium text-slate-400">
          Performance Metrics
        </h2>
        <div className="grid grid-cols-2 gap-4 md:grid-cols-4">
          <StatCard
            label="Close Rate"
            value={pct(t.closeRate)}
            sub="calls to closed deals"
          />
          <StatCard
            label="Show Rate"
            value={pct(t.showRate)}
            sub="scheduled to taken"
          />
          <StatCard
            label="Qualified Calls"
            value={pct(t.qualifiedCallsRate)}
            sub="calls to offers"
          />
          <StatCard
            label="Avg Calls/Day"
            value={t.avgCallsPerDay.toFixed(1)}
            sub="daily average"
          />
        </div>
      </section>

      <section>
        <h2 className="mb-3 text-sm font-medium text-slate-400">
          Volume Metrics
        </h2>
        <div className="grid grid-cols-2 gap-4 md:grid-cols-2">
          <StatCard
            label="Calls on Calendar"
            value={int(t.scheduledCalls)}
            sub="total scheduled"
          />
          <StatCard
            label="Offer Close Rate"
            value={pct(t.offerCloseRate)}
            sub="offers to closed deals"
          />
        </div>
      </section>

      <section className="grid grid-cols-1 gap-4 md:grid-cols-2">
        <Card title="Closed Deals Over Time">
          <DailyLine
            data={data.timeline}
            dataKey="closes"
            color="#34d399"
            name="Closes"
          />
        </Card>
        <Card title="Calls on Calendar Over Time">
          <DailyLine
            data={data.timeline}
            dataKey="scheduledCalls"
            color="#8b5cf6"
            name="Scheduled Calls"
          />
        </Card>
      </section>

      <Card title="Cash Collected by Closer">
        <CashByCloserChart data={data.cashByCloser} />
      </Card>

      <Card title="Closer Performance Summary">
        <div className="grid grid-cols-2 gap-3 md:grid-cols-3 lg:grid-cols-5">
          {data.closers.map((c) => (
            <div
              key={c.name}
              className="rounded-lg border border-edge bg-ink p-3"
            >
              <div className="text-sm font-medium text-slate-100">{c.name}</div>
              <div className="mt-2 text-xs text-slate-400">
                Close Rate:{" "}
                <span className="text-slate-200">{pct(c.closeRate)}</span>
              </div>
              <div className="text-xs text-slate-400">
                Offer Close Rate:{" "}
                <span className="text-slate-200">{pct(c.offerCloseRate)}</span>
              </div>
            </div>
          ))}
          {!data.closers.length && (
            <div className="text-sm text-slate-500">
              No closers reporting yet.
            </div>
          )}
        </div>
      </Card>

      <Card title="Recent EOD Reports">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead className="text-xs uppercase text-slate-500">
              <tr className="border-b border-edge">
                <th className="py-2 pr-3">Date</th>
                <th className="py-2 pr-3">Closer</th>
                <th className="py-2 pr-3 text-right">Scheduled</th>
                <th className="py-2 pr-3 text-right">Taken</th>
                <th className="py-2 pr-3 text-right">1-Call Closes</th>
                <th className="py-2 pr-3 text-right">Cash</th>
                <th className="py-2 pr-3 text-right">Revenue</th>
              </tr>
            </thead>
            <tbody>
              {data.recentSales.map((s) => (
                <tr key={s.id} className="border-b border-edge/50">
                  <td className="py-2 pr-3 text-slate-400">{s.date}</td>
                  <td className="py-2 pr-3 text-slate-200">{s.closer}</td>
                  <td className="py-2 pr-3 text-right text-slate-400">
                    {int(s.scheduledCalls)}
                  </td>
                  <td className="py-2 pr-3 text-right text-slate-400">
                    {int(s.callsTaken)}
                  </td>
                  <td className="py-2 pr-3 text-right text-slate-200">
                    {int(s.oneCallCloses)}
                  </td>
                  <td className="py-2 pr-3 text-right text-slate-400">
                    {usd(s.cashCollected)}
                  </td>
                  <td className="py-2 pr-3 text-right text-slate-200">
                    {usd(s.revenue)}
                  </td>
                </tr>
              ))}
              {!data.recentSales.length && (
                <tr>
                  <td colSpan={7} className="py-3 text-slate-500">
                    No EOD reports yet.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </Card>
    </div>
  );
}

function BuyerAttribution({ data }: { data: DashboardData }) {
  const s = data.buyerSummary;
  const logBadge = {
    stripe: "bg-violet-500/15 text-violet-300 border-violet-500/30",
    whop: "bg-emerald-500/15 text-emerald-300 border-emerald-500/30",
    oto: "bg-amber-500/15 text-amber-300 border-amber-500/30",
  } as const;

  return (
    <div className="space-y-6">
      <section className="grid grid-cols-2 gap-4 md:grid-cols-4">
        <StatCard
          label="Total Buyers"
          value={int(s.totalBuyers)}
          sub={`${int(s.totalRows)} payments`}
        />
        <StatCard label="Total Cash" value={usd(s.totalCash)} />
        <StatCard
          label="Attributed to UTM"
          value={pct(s.attributionRate)}
          sub={`${int(s.attributedBuyers)} of ${int(s.totalBuyers)} buyers`}
        />
        <StatCard
          label="Unattributed Cash"
          value={usd(s.unattributedCash)}
          sub={`${int(s.unattributedBuyers)} buyers w/o UTM`}
        />
      </section>

      <section className="grid grid-cols-1 gap-4 md:grid-cols-3">
        <StatCard
          label="Stripe Log"
          value={usd(s.byLog.stripe.cash)}
          sub={`${int(s.byLog.stripe.rows)} payments`}
        />
        <StatCard
          label="Whop Log"
          value={usd(s.byLog.whop.cash)}
          sub={`${int(s.byLog.whop.rows)} payments`}
        />
        <StatCard
          label="OTO Log"
          value={usd(s.byLog.oto.cash)}
          sub={`${int(s.byLog.oto.rows)} payments`}
        />
      </section>

      <section className="grid grid-cols-1 gap-4 md:grid-cols-2 xl:grid-cols-4">
        <Card title="Buyers by Source">
          <BuyerBarList rows={data.buyersBySource} />
        </Card>
        <Card title="Buyers by Campaign">
          <BuyerBarList rows={data.buyersByCampaign} />
        </Card>
        <Card title="Buyers by Adset">
          <BuyerBarList rows={data.buyersByAdset} />
        </Card>
        <Card title="Buyers by Webinar">
          <BuyerBarList rows={data.buyersByWebinar} />
        </Card>
      </section>

      <Card title="Buyers by UTM Content (ad creative)">
        <BuyerBarList rows={data.buyersByContent} />
      </Card>

      <Card
        title="Recent Buyers"
        right={
          <span className="text-xs text-slate-500">
            {int(data.recentBuyers.length)} of {int(s.totalRows)}
          </span>
        }
      >
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead className="text-xs uppercase text-slate-500">
              <tr className="border-b border-edge">
                <th className="py-2 pr-3">Date</th>
                <th className="py-2 pr-3">Buyer</th>
                <th className="py-2 pr-3">Log</th>
                <th className="py-2 pr-3 text-right">Amount</th>
                <th className="py-2 pr-3">Source</th>
                <th className="py-2 pr-3">Campaign</th>
                <th className="py-2 pr-3">Adset</th>
                <th className="py-2 pr-3">Webinar</th>
              </tr>
            </thead>
            <tbody>
              {data.recentBuyers.map((b) => (
                <tr key={b.id} className="border-b border-edge/50">
                  <td className="py-2 pr-3 text-slate-400">{b.date}</td>
                  <td className="py-2 pr-3 text-slate-200">
                    {b.name || b.email}
                    {b.name && (
                      <div className="text-[11px] text-slate-500">
                        {b.email}
                      </div>
                    )}
                  </td>
                  <td className="py-2 pr-3">
                    <span
                      className={`rounded border px-1.5 py-0.5 text-[10px] uppercase ${logBadge[b.logSource]}`}
                    >
                      {b.logSource}
                    </span>
                  </td>
                  <td className="py-2 pr-3 text-right text-slate-200">
                    {usd(b.amount)}
                  </td>
                  <td className="py-2 pr-3 text-slate-400">
                    {b.attributed ? (
                      <span className="inline-flex items-center gap-1.5">
                        {b.utmSource || "—"}
                        <span
                          className={`rounded px-1 py-0.5 text-[9px] uppercase ${
                            b.matchedBy === "email"
                              ? "bg-slate-700/40 text-slate-400"
                              : "bg-amber-500/15 text-amber-300"
                          }`}
                          title={
                            b.matchedBy === "email"
                              ? "matched by email"
                              : "matched by name (email differed)"
                          }
                        >
                          {b.matchedBy}
                        </span>
                      </span>
                    ) : (
                      <span className="text-slate-600">(unattributed)</span>
                    )}
                  </td>
                  <td className="py-2 pr-3 text-slate-400">
                    {b.attributed ? b.utmCampaign || "—" : ""}
                  </td>
                  <td className="py-2 pr-3 text-slate-400">
                    {b.attributed ? b.utmAdset || "—" : ""}
                  </td>
                  <td className="py-2 pr-3 text-slate-400">
                    {b.attributed ? b.webinar || "—" : ""}
                  </td>
                </tr>
              ))}
              {!data.recentBuyers.length && (
                <tr>
                  <td colSpan={8} className="py-3 text-slate-500">
                    No buyer logs yet.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </Card>

      {s.unattributedBuyers > 0 && (
        <Card title="Attribution gap">
          <p className="text-sm text-slate-400">
            <span className="text-slate-200">
              {int(s.unattributedBuyers)} of {int(s.totalBuyers)} buyers
            </span>{" "}
            ({usd(s.unattributedCash)}) couldn&apos;t be matched to a UTM
            registration by email. This usually means the registration form
            wasn&apos;t hit with UTMs (direct traffic, manual outreach,
            different email at checkout vs. registration). The Stripe / Whop
            high-ticket logs have the lowest match rate — worth investigating.
          </p>
        </Card>
      )}
    </div>
  );
}

function WebinarTab({
  label,
  sub,
  active,
  onClick,
}: {
  label: string;
  sub?: string;
  active: boolean;
  onClick: () => void;
}) {
  return (
    <button
      onClick={onClick}
      className={`rounded-md border px-3 py-1.5 text-xs transition-colors ${
        active
          ? "border-accent bg-accent/15 text-slate-100"
          : "border-edge bg-panel text-slate-400 hover:border-accent/60 hover:text-slate-200"
      }`}
    >
      {label}
      {sub && <span className="ml-1.5 text-[10px] text-slate-500">{sub}</span>}
    </button>
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
