import { ConnectorResult } from "./connectors/types";

// Window for attributing ad spend / calls to a webinar.
// Ad spend D days BEFORE a webinar attributes to that webinar (D <= PRE).
// Calls D days AFTER a webinar attribute to that webinar (D <= POST).
const PRE_DAYS = 4;
const POST_DAYS = 4;

interface WebinarMeta {
  label: string;
  date: string | null; // YYYY-MM-DD, null if unparseable
  registrations: number;
}

const MONTHS: Record<string, number> = {
  jan: 0, january: 0,
  feb: 1, february: 1,
  mar: 2, march: 2,
  apr: 3, april: 3,
  may: 4,
  jun: 5, june: 5,
  jul: 6, july: 6,
  aug: 7, august: 7,
  sep: 8, sept: 8, september: 8,
  oct: 9, october: 9,
  nov: 10, november: 10,
  dec: 11, december: 11,
};

function parseWebinarDate(label: string, refYear: number): string | null {
  const m = label.trim().match(/^([A-Za-z]+)\s+(\d{1,2})\b/);
  if (!m) return null;
  const month = MONTHS[m[1].toLowerCase()];
  if (month === undefined) return null;
  const day = parseInt(m[2], 10);
  if (day < 1 || day > 31) return null;
  const d = new Date(Date.UTC(refYear, month, day));
  return d.toISOString().slice(0, 10);
}

function refYearFromData(r: ConnectorResult): number {
  for (const reg of r.registrations) {
    const y = parseInt(reg.date.slice(0, 4), 10);
    if (y) return y;
  }
  for (const a of r.ads) {
    const y = parseInt(a.date.slice(0, 4), 10);
    if (y) return y;
  }
  return new Date().getUTCFullYear();
}

function buildWebinarMeta(r: ConnectorResult): WebinarMeta[] {
  const yr = refYearFromData(r);
  const counts = new Map<string, number>();
  for (const reg of r.registrations) {
    const w = (reg.webinar || "").trim();
    if (!w) continue;
    counts.set(w, (counts.get(w) || 0) + 1);
  }
  return [...counts.entries()]
    .map(([label, registrations]) => ({
      label,
      date: parseWebinarDate(label, yr),
      registrations,
    }))
    .sort((a, b) => {
      if (a.date && b.date) return a.date.localeCompare(b.date);
      if (a.date) return -1;
      if (b.date) return 1;
      return b.registrations - a.registrations;
    });
}

function diffDays(a: string, b: string): number {
  return (Date.parse(a + "T00:00:00Z") - Date.parse(b + "T00:00:00Z")) / 86400000;
}

// Ad day D days before a webinar (0 <= D <= PRE_DAYS) attributes to that
// webinar. If multiple qualify, pick the closest upcoming one.
function attributeAdSpend(
  adDate: string,
  webinars: WebinarMeta[],
): string | null {
  let best: WebinarMeta | null = null;
  let bestDist = Infinity;
  for (const w of webinars) {
    if (!w.date) continue;
    const dist = diffDays(w.date, adDate);
    if (dist >= 0 && dist <= PRE_DAYS && dist < bestDist) {
      best = w;
      bestDist = dist;
    }
  }
  return best?.label ?? null;
}

// Call D days after a webinar (0 <= D <= POST_DAYS) attributes to that
// webinar. If multiple qualify, pick the most recent past one.
function attributeCall(
  callDate: string,
  webinars: WebinarMeta[],
): string | null {
  let best: WebinarMeta | null = null;
  let bestDist = Infinity;
  for (const w of webinars) {
    if (!w.date) continue;
    const dist = diffDays(callDate, w.date);
    if (dist >= 0 && dist <= POST_DAYS && dist < bestDist) {
      best = w;
      bestDist = dist;
    }
  }
  return best?.label ?? null;
}

// Distinct webinar labels seen in UTM Tracking, ordered chronologically when
// parseable. Used to populate the per-webinar tab row.
export function listWebinars(r: ConnectorResult): string[] {
  return buildWebinarMeta(r).map((w) => w.label);
}

// Scope to a single webinar label.
//   - Registrations / buyers: matched by the UTM Webinar Date tag (email or
//     name cross-reference), as before.
//   - Ad spend: ad-day attributed to closest upcoming webinar within 4 days.
//   - Closer EOD: each EOD day attributed to closest past webinar within 4
//     days (so calls booked just after a webinar count for that webinar).
export function filterByWebinar(
  r: ConnectorResult,
  webinar: string | null,
): ConnectorResult {
  if (!webinar) return r;
  const want = webinar.trim().toLowerCase();
  const match = (w: string) => w.trim().toLowerCase() === want;
  const webinars = buildWebinarMeta(r);
  return {
    ...r,
    registrations: r.registrations.filter((x) => match(x.webinar)),
    buyers: r.buyers.filter((b) => b.attributed && match(b.webinar)),
    attendees: r.attendees.filter((a) => match(a.webinar)),
    // Applicants/bookings have no direct webinar tag; cross-reference filtering
    // happens in metrics (against the in-scope attendees).
    // Prefer the explicit Webinar Date tag when the row has one (added by
    // your team in Airtable). Fall back to the 4-day time-window heuristic
    // for older rows that don't carry the tag yet.
    ads: r.ads.filter((a) => {
      if (a.webinar) return match(a.webinar);
      const tag = attributeAdSpend(a.date, webinars);
      return tag !== null && match(tag);
    }),
    sales: r.sales.filter((s) => {
      if (s.webinar) return match(s.webinar);
      const tag = attributeCall(s.date, webinars);
      return tag !== null && match(tag);
    }),
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
    attendees: r.attendees.filter((x) => inRange(x.scheduleDate || x.signupDate)),
    applicants: r.applicants.filter((x) => inRange(x.date)),
    bookings: r.bookings.filter((x) => inRange(x.date)),
  };
}
