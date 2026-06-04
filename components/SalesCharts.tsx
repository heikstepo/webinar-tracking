"use client";

import {
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
} from "recharts";
import type { TimePoint } from "@/lib/metrics";

const dayLabel = (d: string) => {
  const dt = new Date(d + "T00:00:00");
  return isNaN(dt.getTime())
    ? d
    : dt.toLocaleDateString("en-US", { month: "short", day: "numeric" });
};

const tip = {
  contentStyle: {
    background: "#141821",
    border: "1px solid #222836",
    borderRadius: 8,
    color: "#e6e9f0",
  },
};

export function DailyLine({
  data,
  dataKey,
  color,
  name,
}: {
  data: TimePoint[];
  dataKey: keyof TimePoint;
  color: string;
  name: string;
}) {
  if (!data.length) {
    return (
      <div className="flex h-[220px] items-center justify-center text-sm text-slate-500">
        No data yet.
      </div>
    );
  }
  const rows = data.map((d) => ({ ...d, label: dayLabel(d.date) }));
  return (
    <ResponsiveContainer width="100%" height={220}>
      <LineChart data={rows} margin={{ top: 8, right: 8, left: 8, bottom: 0 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#222836" vertical={false} />
        <XAxis dataKey="label" stroke="#7d869c" fontSize={12} tickLine={false} />
        <YAxis stroke="#7d869c" fontSize={12} tickLine={false} allowDecimals={false} />
        <Tooltip {...tip} />
        <Line
          dataKey={dataKey as string}
          name={name}
          stroke={color}
          strokeWidth={2}
          dot={{ r: 3, fill: color }}
        />
      </LineChart>
    </ResponsiveContainer>
  );
}

export function CashByCloserChart({
  data,
}: {
  data: { name: string; value: number }[];
}) {
  if (!data.length) {
    return (
      <div className="flex h-[260px] items-center justify-center text-sm text-slate-500">
        No cash collected yet.
      </div>
    );
  }
  return (
    <ResponsiveContainer width="100%" height={260}>
      <BarChart data={data} margin={{ top: 8, right: 8, left: 8, bottom: 0 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#222836" vertical={false} />
        <XAxis dataKey="name" stroke="#7d869c" fontSize={12} tickLine={false} />
        <YAxis
          stroke="#7d869c"
          fontSize={12}
          tickLine={false}
          tickFormatter={(v) => `$${Math.round(v / 1000)}k`}
        />
        <Tooltip
          {...tip}
          formatter={(v: number) => [
            "$" + Math.round(v).toLocaleString(),
            "Cash Collected",
          ]}
        />
        <Bar dataKey="value" fill="#5b8cff" radius={[4, 4, 0, 0]} />
      </BarChart>
    </ResponsiveContainer>
  );
}
