import { NextRequest, NextResponse } from "next/server";
import { fetchAirtable } from "@/lib/connectors/airtable";
import { fetchWebinarJam } from "@/lib/connectors/webinarjam";
import { buildDashboard } from "@/lib/metrics";
import { filterByRange, filterByWebinar, listWebinars } from "@/lib/filter";
import { ConnectorResult } from "@/lib/connectors/types";

export const dynamic = "force-dynamic";
export const revalidate = 0;
// WJ pagination across 9 webinars can take 30-40s on cold start; Vercel's
// default function timeout (10s) cuts it short and silently drops webinars.
export const maxDuration = 60;

// Cache the raw upstream fetch so filter changes (date range, webinar tab)
// reuse the same data instead of re-hitting Airtable + WebinarJam each time.
// 5 minutes is well within how fresh you need the dashboard to be.
let cache: { at: number; data: ConnectorResult } | null = null;
const TTL_MS = 5 * 60_000;

async function getResult(): Promise<ConnectorResult> {
  if (cache && Date.now() - cache.at < TTL_MS) return cache.data;
  const [airtable, wj] = await Promise.all([fetchAirtable(), fetchWebinarJam()]);
  const data: ConnectorResult = {
    ...airtable,
    attendees: wj.attendees,
    notes: [...airtable.notes, ...wj.notes],
  };
  cache = { at: Date.now(), data };
  return data;
}

export async function GET(req: NextRequest) {
  try {
    const { searchParams } = new URL(req.url);
    const from = searchParams.get("from");
    const to = searchParams.get("to");
    const webinar = searchParams.get("webinar");
    const refresh = searchParams.get("refresh");
    if (refresh) cache = null;
    const result = await getResult();
    const filtered = filterByWebinar(filterByRange(result, from, to), webinar);
    return NextResponse.json({
      ...buildDashboard(filtered),
      range: { from, to },
      webinar,
      availableWebinars: listWebinars(result),
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
