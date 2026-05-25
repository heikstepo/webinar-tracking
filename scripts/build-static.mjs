import fs from "node:fs";

const real = JSON.parse(fs.readFileSync("/tmp/dash.json", "utf8"));

// Illustrative dataset so each view can be judged when populated.
const sample = {
  fetchedAt: new Date().toISOString(),
  notes: ["Sample data — for layout preview only."],
  counts: { registrations: 312, adDays: 14, salesDays: 22 },
  totals: {
    spend: 8420, registrations: 312, costPerRegistration: 26.99,
    scheduledCalls: 110, callsTaken: 64, offers: 41, closes: 18,
    cashCollected: 41600, revenue: 58200, roas: 6.91,
    showRate: 0.582, closeRate: 0.281, costPerClose: 467.78,
  },
  funnel: [
    { stage: "Registrations", value: 312, sub: "UTM Tracking" },
    { stage: "Scheduled Calls", value: 110, sub: "Closer EOD" },
    { stage: "Calls Taken", value: 64, sub: "showed up" },
    { stage: "Offers Made", value: 41, sub: "Closer EOD" },
    { stage: "Closes", value: 18, sub: "1-call + follow-up" },
  ],
  timeline: [
    ["2026-05-12", 520, 22, 0], ["2026-05-13", 610, 28, 3400],
    ["2026-05-14", 580, 25, 0], ["2026-05-15", 640, 31, 5200],
    ["2026-05-16", 700, 35, 1800], ["2026-05-17", 540, 19, 0],
    ["2026-05-18", 660, 27, 6400], ["2026-05-19", 720, 33, 2100],
    ["2026-05-20", 810, 38, 8200], ["2026-05-21", 690, 29, 3600],
    ["2026-05-22", 750, 34, 9100], ["2026-05-23", 600, 21, 0],
    ["2026-05-24", 700, 30, 5400], ["2026-05-25", 700, 40, 7600],
  ].map(([date, spend, registrations, revenue]) => ({ date, spend, registrations, revenue })),
  bySource: [
    { name: "facebook", count: 198 }, { name: "youtube", count: 54 },
    { name: "instagram", count: 36 }, { name: "google", count: 24 },
  ],
  byCampaign: [
    { name: "Sales - Webinar Campaign", count: 156 },
    { name: "V2WEBBY", count: 88 }, { name: "Retargeting - Warm", count: 44 },
    { name: "(none)", count: 24 },
  ],
  byAdset: [
    { name: "(SLS) May 24 OTO - Broad", count: 92 },
    { name: "Lookalike 1% - US", count: 71 },
    { name: "Interest - Entrepreneur", count: 58 }, { name: "(none)", count: 91 },
  ],
  byWebinar: [
    { name: "MAY 27", count: 142 }, { name: "MAY 20", count: 104 },
    { name: "MAY 13", count: 66 },
  ],
  closers: [
    { name: "Divan", scheduled: 38, callsTaken: 24, noShows: 14, offers: 17, closes: 8, closeRate: 0.333, cashCollected: 18400, revenue: 24600 },
    { name: "Frank", scheduled: 34, callsTaken: 20, noShows: 14, offers: 13, closes: 6, closeRate: 0.30, cashCollected: 13200, revenue: 19800 },
    { name: "Louis", scheduled: 38, callsTaken: 20, noShows: 18, offers: 11, closes: 4, closeRate: 0.20, cashCollected: 10000, revenue: 13800 },
  ],
  recentRegistrations: [
    { id: "s1", date: "2026-05-25", name: "Jay Leishman", webinar: "MAY 27", source: "facebook", campaign: "Sales - Webinar Campaign", adset: "(SLS) May 24 OTO - Broad" },
    { id: "s2", date: "2026-05-25", name: "Maria Gomez", webinar: "MAY 27", source: "youtube", campaign: "V2WEBBY", adset: "(none)" },
    { id: "s3", date: "2026-05-24", name: "Tom Becker", webinar: "MAY 27", source: "facebook", campaign: "Retargeting - Warm", adset: "Lookalike 1% - US" },
    { id: "s4", date: "2026-05-24", name: "Aisha Khan", webinar: "MAY 27", source: "instagram", campaign: "Sales - Webinar Campaign", adset: "Interest - Entrepreneur" },
    { id: "s5", date: "2026-05-23", name: "Forrest M", webinar: "MAY 20", source: "facebook", campaign: "V2WEBBY", adset: "(none)" },
  ],
};

const html = `<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>App Accelerator — Dashboard Draft</title>
<style>
  :root{--ink:#0b0d12;--panel:#141821;--edge:#222836;--accent:#5b8cff;--gold:#f0b429;--green:#34d399;--text:#e6e9f0;--muted:#7d869c;}
  *{box-sizing:border-box}
  body{margin:0;background:var(--ink);color:var(--text);font:14px/1.5 -apple-system,BlinkMacSystemFont,Segoe UI,Roboto,Helvetica,Arial,sans-serif}
  .wrap{max-width:1180px;margin:0 auto;padding:24px 20px 64px}
  header{display:flex;align-items:flex-end;justify-content:space-between;gap:16px;flex-wrap:wrap;margin-bottom:18px}
  h1{font-size:20px;margin:0}
  .sub{color:var(--muted);font-size:13px}
  .toggle{display:flex;align-items:center;gap:8px;font-size:13px;color:var(--muted)}
  .switch{position:relative;width:42px;height:22px;background:var(--edge);border-radius:999px;cursor:pointer;transition:.2s}
  .switch.on{background:var(--accent)}
  .switch .dot{position:absolute;top:2px;left:2px;width:18px;height:18px;border-radius:50%;background:#fff;transition:.2s}
  .switch.on .dot{left:22px}
  nav{display:flex;gap:6px;flex-wrap:wrap;border-bottom:1px solid var(--edge);margin-bottom:20px}
  nav button{background:none;border:none;color:var(--muted);padding:10px 14px;font-size:14px;cursor:pointer;border-bottom:2px solid transparent}
  nav button.active{color:var(--text);border-bottom-color:var(--accent)}
  .grid{display:grid;gap:14px}
  .kpis{grid-template-columns:repeat(auto-fit,minmax(150px,1fr))}
  .cards2{grid-template-columns:repeat(auto-fit,minmax(260px,1fr))}
  .card{background:var(--panel);border:1px solid var(--edge);border-radius:12px;padding:16px}
  .card h2{font-size:13px;font-weight:500;color:#cdd3e0;margin:0 0 12px}
  .stat .lbl{font-size:11px;text-transform:uppercase;letter-spacing:.04em;color:var(--muted)}
  .stat .val{font-size:24px;font-weight:600;margin-top:4px}
  .stat .ssub{font-size:11px;color:var(--muted);margin-top:4px}
  table{width:100%;border-collapse:collapse;font-size:13px}
  th{text-align:left;font-size:11px;text-transform:uppercase;color:var(--muted);border-bottom:1px solid var(--edge);padding:8px 10px 8px 0;font-weight:500}
  td{padding:8px 10px 8px 0;border-bottom:1px solid #1b202c;color:#c7cdda}
  td.r,th.r{text-align:right}
  .bar{height:6px;background:var(--ink);border-radius:4px;margin-top:5px}
  .bar>span{display:block;height:6px;background:var(--accent);border-radius:4px}
  .blrow{display:flex;justify-content:space-between;font-size:13px}
  .blrow .nm{color:#c7cdda;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;padding-right:8px}
  .blrow .ct{color:var(--muted)}
  .frow{display:flex;align-items:center;gap:12px;margin-bottom:8px}
  .frow .fl{width:140px;flex:none;font-size:13px}
  .frow .fl small{display:block;color:#556;font-size:11px}
  .ftrack{flex:1;height:28px;background:var(--ink);border-radius:5px}
  .ftrack>span{display:flex;align-items:center;height:28px;background:rgba(91,140,255,.8);border-radius:5px;color:#fff;font-size:12px;font-weight:500;padding:0 8px;min-width:34px}
  .fconv{width:54px;text-align:right;color:var(--muted);font-size:12px}
  .empty{color:var(--muted);font-size:13px;padding:8px 0}
  .chart{display:flex;align-items:flex-end;gap:6px;height:200px;padding-top:8px}
  .chart .col{flex:1;display:flex;flex-direction:column;justify-content:flex-end;align-items:center;gap:3px}
  .chart .cb{width:60%;background:var(--accent);border-radius:3px 3px 0 0;min-height:2px}
  .chart .cx{font-size:10px;color:var(--muted);transform:rotate(-40deg);white-space:nowrap;margin-top:4px}
  .legend{display:flex;gap:16px;font-size:12px;color:var(--muted);margin-top:10px}
  .legend i{display:inline-block;width:10px;height:10px;border-radius:2px;margin-right:5px;vertical-align:middle}
  .note{background:#1a1410;border:1px solid #5a4420;color:#e7c98a;border-radius:8px;padding:10px 12px;font-size:13px;margin-bottom:14px}
  .hidden{display:none}
  footer{color:#556;font-size:12px;margin-top:24px}
</style></head>
<body><div class="wrap">
<header>
  <div><h1>App Accelerator — Webinar Funnel</h1>
  <div class="sub">Sol Twenty · draft dashboard · Ad Spend → Registrations → Calls → Closes</div></div>
  <div class="toggle"><span id="modeLabel">Live data</span>
    <div class="switch" id="sw"><div class="dot"></div></div></div>
</header>
<nav id="tabs"></nav>
<div id="view"></div>
<footer id="foot"></footer>
</div>
<script>
const DATA={live:${JSON.stringify(real)},sample:${JSON.stringify(sample)}};
let mode="live", tab="overview";
const usd=n=>"$"+Math.round(n||0).toLocaleString();
const usd2=n=>"$"+(n||0).toLocaleString(undefined,{minimumFractionDigits:2,maximumFractionDigits:2});
const intc=n=>Math.round(n||0).toLocaleString();
const pct=n=>((n||0)*100).toFixed(1)+"%";
const el=(h)=>{const d=document.createElement("div");d.innerHTML=h;return d.firstElementChild;};
const TABS=[["overview","Overview"],["registrations","Registrations"],["ads","Paid Ads"],["closers","Closers"],["attribution","Attribution"],["raw","Raw / Notes"]];

function stat(lbl,val,sub){return \`<div class="card stat"><div class="lbl">\${lbl}</div><div class="val">\${val}</div>\${sub?\`<div class="ssub">\${sub}</div>\`:""}</div>\`;}
function barlist(rows){if(!rows||!rows.length)return '<div class="empty">No data yet.</div>';
  const max=Math.max(1,...rows.map(r=>r.count));
  return rows.slice(0,10).map(r=>\`<div style="margin-bottom:8px"><div class="blrow"><span class="nm">\${r.name}</span><span class="ct">\${intc(r.count)}</span></div><div class="bar"><span style="width:\${r.count/max*100}%"></span></div></div>\`).join("");}
function chart(tl){if(!tl||!tl.length)return '<div class="empty">No dated activity yet.</div>';
  const max=Math.max(1,...tl.map(p=>p.registrations));
  const d=new Date();
  const bars=tl.map(p=>{const dt=new Date(p.date+"T00:00:00");const lab=isNaN(dt)?p.date:dt.toLocaleDateString("en-US",{month:"short",day:"numeric"});return \`<div class="col"><div class="cb" style="height:\${p.registrations/max*160}px" title="\${p.date}: \${p.registrations} regs, \${usd(p.spend)} spend, \${usd(p.revenue)} rev"></div><div class="cx">\${lab}</div></div>\`;}).join("");
  return \`<div class="chart">\${bars}</div><div class="legend"><span><i style="background:var(--accent)"></i>Registrations / day (hover for spend & revenue)</span></div>\`;}
function funnel(stages){const max=Math.max(1,...stages.map(s=>s.value));
  return stages.map((s,i)=>{const prev=i>0?stages[i-1].value:0;const conv=i>0&&prev?(s.value/prev*100).toFixed(0)+"%":"";
    return \`<div class="frow"><div class="fl">\${s.stage}<small>\${s.sub}</small></div><div class="ftrack"><span style="width:\${Math.max(s.value/max*100,5)}%">\${intc(s.value)}</span></div><div class="fconv">\${conv}</div></div>\`;}).join("");}

function render(){
  const D=DATA[mode], t=D.totals;
  document.getElementById("modeLabel").textContent = mode==="live"?"Live data":"Sample data";
  document.getElementById("sw").classList.toggle("on",mode==="sample");
  document.getElementById("tabs").innerHTML = TABS.map(([k,l])=>\`<button class="\${k===tab?'active':''}" data-k="\${k}">\${l}</button>\`).join("");
  document.querySelectorAll("#tabs button").forEach(b=>b.onclick=()=>{tab=b.dataset.k;render();});
  let h="";
  const noteHtml = mode==="sample"?'<div class="note">Sample data — illustrative numbers to preview the layout. Toggle off for live Airtable data.</div>':"";

  if(tab==="overview"){
    h=noteHtml+\`<div class="grid kpis">
      \${stat("Ad Spend",usd(t.spend))}
      \${stat("Registrations",intc(t.registrations),usd2(t.costPerRegistration)+" / reg")}
      \${stat("Calls Taken",intc(t.callsTaken),pct(t.showRate)+" show rate")}
      \${stat("Offers",intc(t.offers))}
      \${stat("Closes",intc(t.closes),pct(t.closeRate)+" close rate")}
      \${stat("Cash Collected",usd(t.cashCollected))}
      \${stat("Revenue",usd(t.revenue),t.spend?t.roas.toFixed(2)+"x ROAS":"—")}
    </div>
    <div class="card" style="margin-top:14px"><h2>Daily Activity</h2>\${chart(D.timeline)}</div>
    <div class="card" style="margin-top:14px"><h2>Funnel</h2>\${funnel(D.funnel)}</div>\`;
  }
  else if(tab==="registrations"){
    h=noteHtml+\`<div class="card"><h2>Recent Registrations (\${D.counts.registrations} total)</h2>
      <table><thead><tr><th>Date</th><th>Name</th><th>Webinar</th><th>Source</th><th>Campaign</th><th>Adset</th></tr></thead>
      <tbody>\${D.recentRegistrations.map(r=>\`<tr><td>\${r.date}</td><td>\${r.name}</td><td>\${r.webinar}</td><td>\${r.source}</td><td>\${r.campaign}</td><td>\${r.adset}</td></tr>\`).join("")||'<tr><td colspan=6 class="empty">No registrations yet.</td></tr>'}</tbody></table></div>
      <div class="card" style="margin-top:14px"><h2>Registrations by Webinar</h2>\${barlist(D.byWebinar)}</div>\`;
  }
  else if(tab==="ads"){
    h=noteHtml+\`<div class="grid kpis">
      \${stat("Total Spend",usd(t.spend))}
      \${stat("Registrations",intc(t.registrations))}
      \${stat("Cost / Registration",usd2(t.costPerRegistration))}
      \${stat("Closes",intc(t.closes))}
      \${stat("Cost / Close",t.closes?usd(t.costPerClose):"—")}
      \${stat("ROAS",t.spend?t.roas.toFixed(2)+"x":"—")}
    </div>
    <div class="card" style="margin-top:14px"><h2>Spend & Registrations Over Time</h2>\${chart(D.timeline)}</div>
    \${D.counts.adDays?"":'<div class="note" style="margin-top:14px">Ad Level table has no populated rows yet — this view fills in once daily ad metrics (spend, CPM, CPC, cost/registration) start landing.</div>'}\`;
  }
  else if(tab==="closers"){
    h=noteHtml+\`<div class="card"><h2>Closer Performance (\${D.counts.salesDays} EOD reports)</h2>
      <table><thead><tr><th>Closer</th><th class="r">Scheduled</th><th class="r">Taken</th><th class="r">No-Shows</th><th class="r">Offers</th><th class="r">Closes</th><th class="r">Close %</th><th class="r">Cash</th><th class="r">Revenue</th></tr></thead>
      <tbody>\${D.closers.map(c=>\`<tr><td>\${c.name}</td><td class="r">\${intc(c.scheduled)}</td><td class="r">\${intc(c.callsTaken)}</td><td class="r">\${intc(c.noShows)}</td><td class="r">\${intc(c.offers)}</td><td class="r">\${intc(c.closes)}</td><td class="r">\${pct(c.closeRate)}</td><td class="r">\${usd(c.cashCollected)}</td><td class="r">\${usd(c.revenue)}</td></tr>\`).join("")||'<tr><td colspan=9 class="empty">No Closer EOD reports with metrics yet.</td></tr>'}</tbody></table></div>\`;
  }
  else if(tab==="attribution"){
    h=noteHtml+\`<div class="grid cards2">
      <div class="card"><h2>By Source</h2>\${barlist(D.bySource)}</div>
      <div class="card"><h2>By Campaign</h2>\${barlist(D.byCampaign)}</div>
      <div class="card"><h2>By Adset</h2>\${barlist(D.byAdset)}</div>
      <div class="card"><h2>By Webinar</h2>\${barlist(D.byWebinar)}</div>
    </div>\`;
  }
  else if(tab==="raw"){
    h=\`<div class="card"><h2>Connector Notes</h2><ul style="margin:0;padding-left:18px;color:var(--muted)">\${(D.notes||[]).map(n=>\`<li>\${n}</li>\`).join("")||"<li>None</li>"}</ul></div>
    <div class="card" style="margin-top:14px"><h2>Counts</h2><table><tbody>
      <tr><td>Registrations</td><td class="r">\${intc(D.counts.registrations)}</td></tr>
      <tr><td>Ad days</td><td class="r">\${intc(D.counts.adDays)}</td></tr>
      <tr><td>Closer EOD reports</td><td class="r">\${intc(D.counts.salesDays)}</td></tr>
    </tbody></table></div>\`;
  }
  document.getElementById("view").innerHTML=h;
  document.getElementById("foot").textContent="Generated "+new Date(DATA.live.fetchedAt).toLocaleString()+" · data source: Airtable (Sol Twenty - App Acc)";
}
document.getElementById("sw").onclick=()=>{mode=mode==="live"?"sample":"live";render();};
render();
</script></body></html>`;

fs.writeFileSync("dashboard-draft.html", html);
console.log("wrote dashboard-draft.html", html.length, "bytes");
