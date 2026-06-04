import { ConnectorResult } from "./connectors/types";

// Distinct webinar labels seen in UTM Tracking, ordered by registration volume
// then label. Used to populate the per-webinar tab row.
export function listWebinars(r: ConnectorResult): string[] {
  const counts = new Map<string, number>();
  for (const reg of r.registrations) {
    const w = (reg.webinar || "").trim();
    if (!w) continue;
    counts.set(w, (counts.get(w) || 0) + 1);
  }
  return [...counts.entries()]
    .sort((a, b) => b[1] - a[1] || a[0].localeCompare(b[0]))
    .map(([w]) => w);
}

// Scope to a single webinar label. Registrations and buyers are filtered by
// the webinar tag (buyers via their UTM-joined webinar). Ad spend and Closer
// EOD aren't webinar-tagged at the source, so they're cleared in per-webinar
// mode rather than misleadingly applied to one webinar.
export function filterByWebinar(
  r: ConnectorResult,
  webinar: string | null,
): ConnectorResult {
  if (!webinar) return r;
  const want = webinar.trim().toLowerCase();
  const match = (w: string) => w.trim().toLowerCase() === want;
  return {
    ...r,
    registrations: r.registrations.filter((x) => match(x.webinar)),
    buyers: r.buyers.filter((b) => b.attributed && match(b.webinar)),
    ads: [],
    sales: [],
  };
}

// Inclusive on both ends; either side can be null for open-ended.
export function filterByRange(
  r: ConnectorResult,
  from: string | null,
  to: string | null,
): ConnectorResult {
  if (!from && !to) return r;
  const inRange = (d: string) => {
    const day = (d || "").slice(0, 10);
    if (!day) return false;
    if (from && day < from) return false;
    if (to && day > to) return false;
    return true;
  };
  return {
    ...r,
    registrations: r.registrations.filter((x) => inRange(x.date)),
    ads: r.ads.filter((x) => inRange(x.date)),
    sales: r.sales.filter((x) => inRange(x.date)),
    buyers: r.buyers.filter((x) => inRange(x.date)),
  };
}
