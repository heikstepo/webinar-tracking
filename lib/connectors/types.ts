// Shared, source-agnostic schema. Every connector normalizes its data into
// these shapes so the dashboard never needs to know where a number came from.

export type FunnelStage =
  | "spend"
  | "impressions"
  | "clicks"
  | "registrations"
  | "attended"
  | "calls"
  | "shows"
  | "offers"
  | "closes"
  | "revenue";

// A single normalized sale (one payment / deal).
export interface Sale {
  id: string;
  date: string; // ISO
  customer: string;
  email: string;
  product: string; // normalized product family
  rawProduct: string; // original label
  amount: number;
  closer: string;
  setter: string;
  paymentMethod: string;
  isRefund: boolean;
}

// A daily funnel snapshot from any source (ads, webinar, sales EOD...).
export interface DailyFunnel {
  date: string; // YYYY-MM-DD
  source: string; // e.g. "airtable:Ad Level"
  spend?: number;
  impressions?: number;
  clicks?: number;
  registrations?: number;
  attended?: number;
  calls?: number;
  shows?: number;
  offers?: number;
  closes?: number;
  revenue?: number;
}

// Top-of-funnel attribution row (UTM).
export interface AttributionRow {
  date: string;
  name: string;
  email: string;
  source: string;
  medium: string;
  campaign: string;
  content: string;
}

// What a connector returns. Any section may be empty if that source has no
// data yet — the dashboard renders only the sections that have data.
export interface ConnectorResult {
  connector: string; // "airtable"
  fetchedAt: string;
  sales: Sale[];
  daily: DailyFunnel[];
  attribution: AttributionRow[];
  notes: string[]; // human-readable status, e.g. "Ad Level table empty"
}
