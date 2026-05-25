import { NextResponse } from "next/server";
import { fetchAirtable } from "@/lib/connectors/airtable";
import { buildDashboard } from "@/lib/metrics";

export const dynamic = "force-dynamic";
export const revalidate = 0;

export async function GET() {
  try {
    const result = await fetchAirtable();
    return NextResponse.json(buildDashboard(result));
  } catch (e) {
    return NextResponse.json(
      { error: (e as Error).message },
      { status: 500 },
    );
  }
}
