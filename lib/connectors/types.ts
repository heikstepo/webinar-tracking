// Shared, source-agnostic schema for the App Accelerator webinar funnel.
// Every connector normalizes into these shapes so the dashboard never needs
// to know which tool a number came from.

// One webinar registration (UTM Tracking).
export interface Registration {
  id: string;
  date: string; // date of entry, ISO/YYYY-MM-DD
  name: string;
  email: string;
  phone: string;
  webinar: string; // webinar label/date the person registered for
  source: string; // UTM Source
  medium: string; // UTM Medium
  campaign: string; // UTM Campaign
  content: string; // UTM Content
  adset: string; // UTM Adset
}

// One day of paid-ad performance (Ad Level).
export interface AdDay {
  date: string; // YYYY-MM-DD
  webinar: string; // UTM label (e.g. "JUNE 3") — direct tag from Airtable
  spend: number;
  impressions: number;
  ctr: number;
  cpm: number;
  cpc: number;
  costPerRegistration: number;
  registrations: number;
  purchases: number;
  costPerPurchase: number;
}

// One closer's end-of-day report (Closer EOD).
export interface SalesDay {
  id: string;
  date: string; // YYYY-MM-DD
  webinar: string; // UTM label — direct tag from Airtable
  closer: string;
  scheduledCalls: number;
  callsTaken: number;
  noShows: number;
  cancelled: number;
  rescheduled: number;
  offersMade: number;
  oneCallCloses: number;
  followUpCloses: number;
  cashCollected: number;
  revenue: number;
}

// One paying customer payment row from a billing log (Stripe / Whop / OTO).
// utm* fields are filled in by joining to UTM Tracking on email.
export interface Buyer {
  id: string;
  date: string; // YYYY-MM-DD
  name: string;
  email: string;
  amount: number;
  status: string;
  logSource: "stripe" | "whop" | "oto";
  utmSource: string;
  utmMedium: string;
  utmCampaign: string;
  utmAdset: string;
  utmContent: string;
  webinar: string;
  attributed: boolean; // matched a UTM Tracking row
  matchedBy: "email" | "name" | "none"; // how the join landed
}

// One Typeform application submission (Typeform Log).
export interface Applicant {
  id: string;
  date: string;
  name: string;
  email: string;
  status: string;
}

// One Calendly call booking (Calendly Log).
export interface Booking {
  id: string;
  date: string;
  name: string;
  email: string;
  closer: string;
  status: string;
}

// One WebinarJam registrant — already includes attendance + watch time, so
// the same row represents both "registered" and "attended" (with flags).
export interface Attendee {
  id: string;
  email: string;
  name: string;
  webinar: string; // normalized to UTM label format (e.g. "JUNE 3")
  signupDate: string; // YYYY-MM-DD
  scheduleDate: string; // YYYY-MM-DD — when the session ran
  attendedLive: boolean;
  attendedReplay: boolean;
  liveWatchSeconds: number;
  replayWatchSeconds: number;
  utmSource: string;
  utmMedium: string;
  utmCampaign: string;
  utmContent: string;
}

// What a connector returns. Any array may be empty if that source has no data
// yet — the dashboard renders only the sections that have data.
export interface ConnectorResult {
  connector: string;
  fetchedAt: string;
  registrations: Registration[];
  ads: AdDay[];
  sales: SalesDay[];
  buyers: Buyer[];
  applicants: Applicant[];
  bookings: Booking[];
  attendees: Attendee[];
  notes: string[];
}
