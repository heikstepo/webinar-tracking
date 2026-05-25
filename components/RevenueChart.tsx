"use client";

import {
  ComposedChart,
  Bar,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
  Legend,
} from "recharts";
import type { TimePoint } from "@/lib/metrics";

const dayLabel = (d: string) => {
  const dt = new Date(d + "T00:00:00");
  return isNaN(dt.getTime())
    ? d
    : dt.toLocaleDateString("en-US", { month: "short", day: "numeric" });
};

export default function TimelineChart({ data }: { data: TimePoint[] }) {
  if (!data.length) {
    return (
      <div className="flex h-[260px] items-center justify-center text-sm text-slate-500">
        No dated activity yet — fills in as ads, registrations, and EOD reports land.
      </div>
    );
  }
  const rows = data.map((d) => ({ ...d, label: dayLabel(d.date) }));
  return (
    <ResponsiveContainer width="100%" height={260}>
      <ComposedChart data={rows} margin={{ top: 8, right: 8, left: 8, bottom: 0 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#222836" vertical={false} />
        <XAxis dataKey="label" stroke="#7d869c" fontSize={12} tickLine={false} />
        <YAxis stroke="#7d869c" fontSize={12} tickLine={false} />
        <Tooltip
          contentStyle={{
            background: "#141821",
            border: "1px solid #222836",
            borderRadius: 8,
            color: "#e6e9f0",
          }}
        />
        <Legend wrapperStyle={{ fontSize: 12 }} />
        <Bar dataKey="registrations" name="Registrations" fill="#5b8cff" radius={[4, 4, 0, 0]} />
        <Line dataKey="spend" name="Ad Spend ($)" stroke="#f0b429" dot={false} strokeWidth={2} />
        <Line dataKey="revenue" name="Revenue ($)" stroke="#34d399" dot={false} strokeWidth={2} />
      </ComposedChart>
    </ResponsiveContainer>
  );
}
