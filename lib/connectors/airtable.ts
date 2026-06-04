import { listRecords, num, str, AirtableRecord } from "./airtableClient";
import {
  ConnectorResult,
  Registration,
  AdDay,
  SalesDay,
  Buyer,
} from "./types";

// App Accelerator base — the live webinar-funnel system.
const BASE = process.env.AIRTABLE_BASE_APP || "appEzSNgcfbsBGteb";

const TABLE_UTM = "UTM Tracking";
const TABLE_ADS = "Ad Level";
const TABLE_EOD = "Closer EOD";
const TABLE_STRIPE = "Stripe Log";
const TABLE_WHOP = "Whop Log";
const TABLE_OTO = "OTO Log";

function dayKey(iso: string): string {
  return iso ? iso.slice(0, 10) : "";
}

function hasData(r: AirtableRecord): boolean {
  return Object.values(r.fields).some(
    (v) => v !== null && v !== "" && !(Array.isArray(v) && v.length === 0),
  );
}

function mapRegistrations(recs: AirtableRecord[]): Registration[] {
  return recs.filter(hasData).map((r) => {
    const f = r.fields;
    return {
      id: r.id,
      date: dayKey(str(f["Date of Entry"]) || r.createdTime),
      name: str(f["Name"]),
      email: str(f["Email"]),
      phone: str(f["Phone"]),
      webinar: str(f["Webinar Date"]),
      source: str(f["UTM Source"]) || "(unknown)",
      medium: str(f["UTM Medium"]),
      campaign: str(f["UTM Campaign"]) || "(none)",
      content: str(f["UTM Content"]),
      adset: str(f["UTM Adset"]) || "(none)",
    };
  });
}

function mapAds(recs: AirtableRecord[]): AdDay[] {
  return recs.filter(hasData).map((r) => {
    const f = r.fields;
    return {
      date: dayKey(str(f["Date"]) || r.createdTime),
      spend: num(f["Total Ad Spend"]),
      impressions: num(f["Impressions"]),
      ctr: num(f["CTR"]),
      cpm: num(f["CPM"]),
      cpc: num(f["CPC"]),
      costPerRegistration: num(f["Cost per Registration"]),
      registrations: num(f["Registrations"]),
      purchases: num(f["Purchases"]),
      costPerPurchase: num(f["Cost per Purchase"]),
    };
  });
}

function mapSales(recs: AirtableRecord[]): SalesDay[] {
  return recs.filter(hasData).map((r) => {
    const f = r.fields;
    return {
      id: r.id,
      date: dayKey(str(f["Date of EOD"]) || r.createdTime),
      closer: str(f["Closer"]) || "Unknown",
      scheduledCalls: num(f["Scheduled Calls on Calendar"]),
      callsTaken: num(f["Calls taken"]),
      noShows: num(f["No Shows"]),
      cancelled: num(f["Cancelled Calls"]),
      rescheduled: num(f["Rescheduled Calls"]),
      offersMade: num(f["Offers Made"]),
      oneCallCloses: num(f["One Call Closes"]),
      followUpCloses: num(f["Follow Up Closes"]),
      cashCollected: num(f["Cash Collected"]),
      revenue: num(f["Revenue Generated"]),
    };
  });
}

function mapBuyers(
  recs: AirtableRecord[],
  logSource: Buyer["logSource"],
  utmByEmail: Map<string, Registration>,
): Buyer[] {
  return recs.filter(hasData).map((r) => {
    const f = r.fields;
    const email = str(f["Email"]).toLowerCase();
    const utm = email ? utmByEmail.get(email) : undefined;
    return {
      id: r.id,
      date: dayKey(str(f["Date"]) || r.createdTime),
      name: str(f["Name"]),
      email,
      amount: num(f["Cash Collected"]),
      status: str(f["Status"]),
      logSource,
      utmSource: utm?.source || "",
      utmMedium: utm?.medium || "",
      utmCampaign: utm?.campaign || "",
      utmAdset: utm?.adset || "",
      utmContent: utm?.content || "",
      webinar: utm?.webinar || "",
      attributed: Boolean(utm),
    };
  });
}

export async function fetchAirtable(): Promise<ConnectorResult> {
  const notes: string[] = [];
  const safe = async (
    label: string,
    fn: () => Promise<AirtableRecord[]>,
  ): Promise<AirtableRecord[]> => {
    try {
      return await fn();
    } catch (e) {
      notes.push(`${label}: ${(e as Error).message}`);
      return [];
    }
  };

  const [utm, ads, eod, stripe, whop, oto] = await Promise.all([
    safe(TABLE_UTM, () => listRecords(BASE, TABLE_UTM)),
    safe(TABLE_ADS, () => listRecords(BASE, TABLE_ADS)),
    safe(TABLE_EOD, () => listRecords(BASE, TABLE_EOD)),
    safe(TABLE_STRIPE, () => listRecords(BASE, TABLE_STRIPE)),
    safe(TABLE_WHOP, () => listRecords(BASE, TABLE_WHOP)),
    safe(TABLE_OTO, () => listRecords(BASE, TABLE_OTO)),
  ]);

  const registrations = mapRegistrations(utm);
  const adDays = mapAds(ads);
  const sales = mapSales(eod);

  // Index registrations by lowercased email for the buyer join. Latest entry
  // wins so we get the most recent UTM attribution if a person registered
  // multiple times.
  const utmByEmail = new Map<string, Registration>();
  for (const r of [...registrations].sort((a, b) =>
    a.date.localeCompare(b.date),
  )) {
    if (r.email) utmByEmail.set(r.email.toLowerCase(), r);
  }

  const buyers: Buyer[] = [
    ...mapBuyers(stripe, "stripe", utmByEmail),
    ...mapBuyers(whop, "whop", utmByEmail),
    ...mapBuyers(oto, "oto", utmByEmail),
  ];

  if (!registrations.length)
    notes.push("UTM Tracking has no registrations yet.");
  if (!adDays.length) notes.push("Ad Level has no populated rows yet.");
  if (!sales.length) notes.push("Closer EOD has no populated rows yet.");
  if (!buyers.length) notes.push("No buyer log entries yet.");

  return {
    connector: "airtable",
    fetchedAt: new Date().toISOString(),
    registrations,
    ads: adDays,
    sales,
    buyers,
    notes,
  };
}
