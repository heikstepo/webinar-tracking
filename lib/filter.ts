import { ConnectorResult } from "./connectors/types";

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
