import { listRecords, num, str, AirtableRecord } from "./airtableClient";
import {
  ConnectorResult,
  Sale,
  DailyFunnel,
  AttributionRow,
} from "./types";

const BASE_APP = process.env.AIRTABLE_BASE_APP || "appEzSNgcfbsBGteb";
const BASE_BACKUP = process.env.AIRTABLE_BASE_BACKUP || "appNMg1z6iAvqM1KW";

// Collapse the many free-text product labels into a few families.
export function normalizeProduct(raw: string): string {
  const s = raw.toLowerCase();
  if (s.includes("refund")) return "Refund";
  if (s.includes("deposit")) return "Deposit";
  if (s.includes("diy")) return "Faceless Launchpad DIY";
  if (s.includes("consulting")) return "Consulting";
  if (s.includes("faceless")) return "Faceless Launchpad";
  return raw.trim() || "Other";
}

function dayKey(iso: string): string {
  return iso ? iso.slice(0, 10) : "";
}

function mapCommissionTracking(recs: AirtableRecord[]): Sale[] {
  return recs
    .map((r): Sale | null => {
      const f = r.fields;
      const rawProduct = str(f["Product"]);
      if (!rawProduct && !f["Total Amount"]) return null;
      const amount = num(f["Total Amount"]);
      return {
        id: r.id,
        date: str(f["Sale Date"]) || r.createdTime,
        customer: str(f["Customer Name"]),
        email: str(f["Customer Email"]),
        product: normalizeProduct(rawProduct),
        rawProduct,
        amount,
        closer: str(f["Assigned Closer"]) || "Unknown",
        setter: str(f["Assigned Setter"]) || "Unknown",
        paymentMethod: str(f["Payment Method"]) || "Unknown",
        isRefund: /refund/i.test(rawProduct) || amount < 0,
      };
    })
    .filter((x): x is Sale => x !== null);
}

function mapAdLevel(recs: AirtableRecord[]): DailyFunnel[] {
  return recs
    .filter((r) => Object.keys(r.fields).length > 0)
    .map((r) => {
      const f = r.fields;
      return {
        date: dayKey(str(f["Date"]) || r.createdTime),
        source: "airtable:Ad Level",
        spend: num(f["Total Ad Spend"]),
        registrations: num(f["Registrations"]),
        closes: num(f["Purchases"]),
      } as DailyFunnel;
    })
    .filter((d) => d.spend || d.registrations || d.closes);
}

function mapCloserEod(recs: AirtableRecord[]): DailyFunnel[] {
  return recs
    .filter((r) => Object.keys(r.fields).length > 0)
    .map((r) => {
      const f = r.fields;
      return {
        date: dayKey(str(f["Date of EOD"]) || r.createdTime),
        source: "airtable:Closer EOD",
        calls: num(f["Calls taken"]),
        shows: num(f["Calls taken"]) - num(f["No Shows"]),
        offers: num(f["Offers Made"]),
        closes: num(f["One Call Closes"]) + num(f["Follow Up Closes"]),
        revenue: num(f["Revenue Generated"]),
      } as DailyFunnel;
    })
    .filter((d) => d.calls || d.offers || d.closes || d.revenue);
}

function mapUtm(recs: AirtableRecord[]): AttributionRow[] {
  return recs
    .filter((r) => Object.keys(r.fields).length > 0)
    .map((r) => {
      const f = r.fields;
      return {
        date: dayKey(str(f["Date of Entry"]) || str(f["Webinar Date"]) || r.createdTime),
        name: str(f["Name"]),
        email: str(f["Email"]),
        source: str(f["UTM Source"]),
        medium: str(f["UTM Medium"]),
        campaign: str(f["UTM Campaign"]),
        content: str(f["UTM Content"]),
      };
    })
    .filter((a) => a.source || a.campaign || a.email);
}

export async function fetchAirtable(): Promise<ConnectorResult> {
  const notes: string[] = [];
  const safe = async <T>(label: string, fn: () => Promise<T>, fallback: T): Promise<T> => {
    try {
      return await fn();
    } catch (e) {
      notes.push(`${label}: ${(e as Error).message}`);
      return fallback;
    }
  };

  const commission = await safe(
    "Commission Tracking",
    () => listRecords(BASE_BACKUP, "Commission Tracking"),
    [] as AirtableRecord[],
  );
  const adLevel = await safe(
    "Ad Level",
    () => listRecords(BASE_APP, "Ad Level"),
    [] as AirtableRecord[],
  );
  const closerEod = await safe(
    "Closer EOD",
    () => listRecords(BASE_APP, "Closer EOD"),
    [] as AirtableRecord[],
  );
  const utm = await safe(
    "UTM Tracking",
    () => listRecords(BASE_APP, "UTM Tracking"),
    [] as AirtableRecord[],
  );

  const sales = mapCommissionTracking(commission);
  const adDaily = mapAdLevel(adLevel);
  const eodDaily = mapCloserEod(closerEod);
  const attribution = mapUtm(utm);

  if (!sales.length) notes.push("No sales found in Commission Tracking.");
  if (!adDaily.length) notes.push("Ad Level table has no populated rows yet.");
  if (!eodDaily.length) notes.push("Closer EOD table has no populated rows yet.");
  if (!attribution.length) notes.push("UTM Tracking table has no populated rows yet.");

  return {
    connector: "airtable",
    fetchedAt: new Date().toISOString(),
    sales,
    daily: [...adDaily, ...eodDaily],
    attribution,
    notes,
  };
}
