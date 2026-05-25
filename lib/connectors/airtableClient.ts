// Thin Airtable REST client with pagination. Server-side only.

const API = "https://api.airtable.com/v0";

export interface AirtableRecord {
  id: string;
  createdTime: string;
  fields: Record<string, unknown>;
}

function token(): string {
  const t = process.env.AIRTABLE_TOKEN;
  if (!t) throw new Error("AIRTABLE_TOKEN is not set");
  return t;
}

export async function listRecords(
  baseId: string,
  table: string,
): Promise<AirtableRecord[]> {
  const out: AirtableRecord[] = [];
  let offset: string | undefined;
  do {
    const url = new URL(`${API}/${baseId}/${encodeURIComponent(table)}`);
    url.searchParams.set("pageSize", "100");
    if (offset) url.searchParams.set("offset", offset);
    const res = await fetch(url, {
      headers: { Authorization: `Bearer ${token()}` },
      cache: "no-store",
    });
    if (!res.ok) {
      throw new Error(
        `Airtable ${table} -> ${res.status} ${await res.text()}`,
      );
    }
    const data = (await res.json()) as {
      records: AirtableRecord[];
      offset?: string;
    };
    out.push(...data.records);
    offset = data.offset;
  } while (offset);
  return out;
}

export function num(v: unknown): number {
  if (typeof v === "number") return v;
  if (typeof v === "string") {
    const n = parseFloat(v.replace(/[^0-9.\-]/g, ""));
    return isNaN(n) ? 0 : n;
  }
  return 0;
}

export function str(v: unknown): string {
  if (v == null) return "";
  if (typeof v === "string") return v;
  if (typeof v === "number") return String(v);
  // Airtable collaborator / linked-record objects
  if (typeof v === "object") {
    const o = v as Record<string, unknown>;
    if (typeof o.name === "string") return o.name;
    if (typeof o.email === "string") return o.email;
    if (Array.isArray(v)) return v.map(str).join(", ");
  }
  return "";
}
