"use client";

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
} from "recharts";
import { usd, monthLabel } from "./format";

export default function RevenueChart({
  data,
}: {
  data: { month: string; revenue: number; sales: number }[];
}) {
  const rows = data.map((d) => ({ ...d, label: monthLabel(d.month) }));
  return (
    <ResponsiveContainer width="100%" height={260}>
      <BarChart data={rows} margin={{ top: 8, right: 8, left: 8, bottom: 0 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#222836" vertical={false} />
        <XAxis dataKey="label" stroke="#7d869c" fontSize={12} tickLine={false} />
        <YAxis
          stroke="#7d869c"
          fontSize={12}
          tickLine={false}
          tickFormatter={(v) => `$${Math.round(v / 1000)}k`}
        />
        <Tooltip
          contentStyle={{
            background: "#141821",
            border: "1px solid #222836",
            borderRadius: 8,
            color: "#e6e9f0",
          }}
          formatter={(v: number, n) =>
            n === "revenue" ? [usd(v), "Revenue"] : [v, "Sales"]
          }
        />
        <Bar dataKey="revenue" fill="#5b8cff" radius={[4, 4, 0, 0]} />
      </BarChart>
    </ResponsiveContainer>
  );
}
