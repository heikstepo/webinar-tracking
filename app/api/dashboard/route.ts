import { NextRequest, NextResponse } from "next/server";
import { fetchAirtable } from "@/lib/connectors/airtable";
import { buildDashboard } from "@/lib/metrics";
import { filterByRange } from "@/lib/filter";
import { ConnectorResult } from "@/lib/connectors/types";

export const dynamic = "force-dynamic";
export const revalidate = 0;

// Cache the raw Airtable fetch briefly so date-range changes don't re-hit
// Airtable every time the user slides the picker.
let cache: { at: number; data: ConnectorResult } | null = null;
const TTL_MS = 60_000;

async function getResult(): Promise<ConnectorResult> {
  if (cache && Date.now() - cache.at < TTL_MS) return cache.data;
  const data = await fetchAirtable();
  cache = { at: Date.now(), data };
  return data;
}

export async function GET(req: NextRequest) {
  try {
    const { searchParams } = new URL(req.url);
    const from = searchParams.get("from");
    const to = searchParams.get("to");
    const refresh = searchParams.get("refresh");
    if (refresh) cache = null;
    const result = await getResult();
    const filtered = filterByRange(result, from, to);
    return NextResponse.json({
      ...buildDashboard(filtered),
      range: { from, to },
      available: dateBounds(result),
    });
  } catch (e) {
    return NextResponse.json({ error: (e as Error).message }, { status: 500 });
  }
}

function dateBounds(r: ConnectorResult): { min: string | null; max: string | null } {
  const dates: string[] = [];
  for (const x of r.registrations) if (x.date) dates.push(x.date.slice(0, 10));
  for (const x of r.ads) if (x.date) dates.push(x.date.slice(0, 10));
  for (const x of r.sales) if (x.date) dates.push(x.date.slice(0, 10));
  for (const x of r.buyers) if (x.date) dates.push(x.date.slice(0, 10));
  if (!dates.length) return { min: null, max: null };
  dates.sort();
  return { min: dates[0], max: dates[dates.length - 1] };
}
