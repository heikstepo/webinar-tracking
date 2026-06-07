import { Attendee } from "./types";

// WebinarJam API base. WJ uses POST + form-encoded body with api_key.
const API = "https://api.webinarjam.com/webinarjam";

interface WjRegistrant {
  id: string;
  email?: string;
  first_name?: string;
  last_name?: string;
  schedule?: string; // e.g. "Wed, 3 Jun 2026, 07:00 PM"
  signup_date?: string;
  date_live?: string;
  attended_live?: string; // "Yes" | "No"
  attended_replay?: string;
  time_live?: string; // "HH:MM:SS"
  time_replay?: string;
  entered_live?: string;
  utm_source?: string;
  utm_medium?: string;
  utm_campaign?: string;
  utm_content?: string;
}

interface WjListPage {
  status: string;
  registrants: {
    data: WjRegistrant[];
    next_page_url: string | null;
    last_page: number;
  };
}

interface WjWebinar {
  webinar_id: string;
  webinar_hash: string;
  name: string;
}

const MONTHS_LONG: Record<string, string> = {
  jan: "JANUARY",
  feb: "FEBRUARY",
  mar: "MARCH",
  apr: "APRIL",
  may: "MAY",
  jun: "JUNE",
  jul: "JULY",
  aug: "AUGUST",
  sep: "SEPTEMBER",
  oct: "OCTOBER",
  nov: "NOVEMBER",
  dec: "DECEMBER",
};

// "Wed, 3 Jun 2026, 07:00 PM" -> "JUNE 3" (matches the UTM Tracking label).
export function scheduleToWebinarLabel(schedule: string): string {
  if (!schedule) return "";
  const m = schedule.match(/(\d{1,2})\s+([A-Za-z]+)\s+(\d{4})/);
  if (!m) return "";
  const day = parseInt(m[1], 10);
  const month = MONTHS_LONG[m[2].slice(0, 3).toLowerCase()];
  if (!month) return "";
  return `${month} ${day}`;
}

// "Wed, 3 Jun 2026, 07:00 PM" -> "2026-06-03"
export function scheduleToIso(schedule: string): string {
  if (!schedule) return "";
  const m = schedule.match(/(\d{1,2})\s+([A-Za-z]+)\s+(\d{4})/);
  if (!m) return "";
  const day = parseInt(m[1], 10);
  const monthShort = m[2].slice(0, 3).toLowerCase();
  const idx = [
    "jan",
    "feb",
    "mar",
    "apr",
    "may",
    "jun",
    "jul",
    "aug",
    "sep",
    "oct",
    "nov",
    "dec",
  ].indexOf(monthShort);
  if (idx < 0) return "";
  const year = parseInt(m[3], 10);
  const mm = String(idx + 1).padStart(2, "0");
  const dd = String(day).padStart(2, "0");
  return `${year}-${mm}-${dd}`;
}

function hmsToSeconds(s: string | undefined): number {
  if (!s) return 0;
  const m = s.match(/^(\d+):(\d+):(\d+)$/);
  if (!m) return 0;
  return Number(m[1]) * 3600 + Number(m[2]) * 60 + Number(m[3]);
}

async function postForm(
  endpoint: string,
  body: Record<string, string>,
): Promise<unknown> {
  const params = new URLSearchParams(body);
  const res = await fetch(`${API}/${endpoint}`, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: params.toString(),
    cache: "no-store",
  });
  if (!res.ok) {
    throw new Error(`WJ ${endpoint} -> ${res.status} ${await res.text()}`);
  }
  return await res.json();
}

async function listWebinars(apiKey: string): Promise<WjWebinar[]> {
  const data = (await postForm("webinars", { api_key: apiKey })) as {
    status: string;
    webinars: WjWebinar[];
  };
  if (data.status !== "success") return [];
  return data.webinars || [];
}

async function listRegistrants(
  apiKey: string,
  webinarId: string,
): Promise<WjRegistrant[]> {
  // Fetch page 1 first to learn last_page, then pull the remaining pages
  // in parallel.
  const first = (await postForm("registrants", {
    api_key: apiKey,
    webinar_id: webinarId,
    page: "1",
  })) as WjListPage;
  if (first.status !== "success") return [];
  const rows: WjRegistrant[] = first.registrants?.data || [];
  const lastPage = Math.max(1, Math.min(first.registrants?.last_page || 1, 100));
  if (lastPage <= 1) return rows;
  const pages = await Promise.all(
    Array.from({ length: lastPage - 1 }, (_, i) => i + 2).map(
      (page) =>
        postForm("registrants", {
          api_key: apiKey,
          webinar_id: webinarId,
          page: String(page),
        }) as Promise<WjListPage>,
    ),
  );
  for (const p of pages) {
    if (p.status === "success") rows.push(...(p.registrants?.data || []));
  }
  return rows;
}

function mapRegistrant(r: WjRegistrant): Attendee {
  const schedule = r.schedule || r.date_live || "";
  return {
    id: r.id,
    email: (r.email || "").toLowerCase(),
    name: `${r.first_name || ""} ${r.last_name || ""}`.trim(),
    webinar: scheduleToWebinarLabel(schedule),
    signupDate: scheduleToIso(r.signup_date || "") || scheduleToIso(schedule),
    scheduleDate: scheduleToIso(schedule),
    attendedLive: (r.attended_live || "").toLowerCase() === "yes",
    attendedReplay: (r.attended_replay || "").toLowerCase() === "yes",
    liveWatchSeconds: hmsToSeconds(r.time_live),
    replayWatchSeconds: hmsToSeconds(r.time_replay),
    utmSource: (r.utm_source && r.utm_source !== "None" ? r.utm_source : "") || "",
    utmMedium: (r.utm_medium && r.utm_medium !== "None" ? r.utm_medium : "") || "",
    utmCampaign:
      (r.utm_campaign && r.utm_campaign !== "None" ? r.utm_campaign : "") || "",
    utmContent:
      (r.utm_content && r.utm_content !== "None" ? r.utm_content : "") || "",
  };
}

export async function fetchWebinarJam(): Promise<{
  attendees: Attendee[];
  notes: string[];
}> {
  const apiKey = process.env.WEBINARJAM_API_KEY;
  if (!apiKey) {
    return {
      attendees: [],
      notes: ["WebinarJam: WEBINARJAM_API_KEY is not set"],
    };
  }

  const notes: string[] = [];
  let webinars: WjWebinar[] = [];
  try {
    webinars = await listWebinars(apiKey);
  } catch (e) {
    return {
      attendees: [],
      notes: [`WebinarJam list-webinars failed: ${(e as Error).message}`],
    };
  }
  // Filter out the demo "WebinarJam Example" webinar.
  webinars = webinars.filter((w) => !/example/i.test(w.name));

  // All webinars + all their pages fetched in parallel.
  const results = await Promise.all(
    webinars.map((w) =>
      listRegistrants(apiKey, w.webinar_id)
        .then((rows) => ({ ok: true as const, w, rows }))
        .catch((e) => ({ ok: false as const, w, error: e as Error })),
    ),
  );
  const attendees: Attendee[] = [];
  for (const r of results) {
    if (r.ok) for (const row of r.rows) attendees.push(mapRegistrant(row));
    else notes.push(`WebinarJam ${r.w.name} (${r.w.webinar_id}): ${r.error.message}`);
  }

  return { attendees, notes };
}
