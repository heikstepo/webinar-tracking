import { usd, int } from "./format";
import type { NamedTotal } from "@/lib/metrics";

export function StatCard({
  label,
  value,
  sub,
}: {
  label: string;
  value: string;
  sub?: string;
}) {
  return (
    <div className="rounded-xl border border-edge bg-panel p-4">
      <div className="text-xs uppercase tracking-wide text-slate-400">
        {label}
      </div>
      <div className="mt-1 text-2xl font-semibold text-slate-50">{value}</div>
      {sub && <div className="mt-1 text-xs text-slate-500">{sub}</div>}
    </div>
  );
}

export function Card({
  title,
  children,
  right,
}: {
  title: string;
  children: React.ReactNode;
  right?: React.ReactNode;
}) {
  return (
    <div className="rounded-xl border border-edge bg-panel p-4">
      <div className="mb-3 flex items-center justify-between">
        <h2 className="text-sm font-medium text-slate-200">{title}</h2>
        {right}
      </div>
      {children}
    </div>
  );
}

export function BarList({ rows }: { rows: NamedTotal[] }) {
  const max = Math.max(1, ...rows.map((r) => r.revenue));
  return (
    <div className="space-y-2">
      {rows.map((r) => (
        <div key={r.name}>
          <div className="flex justify-between text-sm">
            <span className="truncate pr-2 text-slate-300">{r.name}</span>
            <span className="text-slate-400">
              {usd(r.revenue)}{" "}
              <span className="text-slate-600">· {int(r.count)}</span>
            </span>
          </div>
          <div className="mt-1 h-1.5 w-full rounded bg-ink">
            <div
              className="h-1.5 rounded bg-accent"
              style={{ width: `${(r.revenue / max) * 100}%` }}
            />
          </div>
        </div>
      ))}
      {!rows.length && (
        <div className="text-sm text-slate-500">No data yet.</div>
      )}
    </div>
  );
}
