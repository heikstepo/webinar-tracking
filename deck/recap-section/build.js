const pptxgen = require("pptxgenjs");
const fs = require("fs");
const D = require("./ds.js");
const { C, T, CW, RAIL, TIERS, nlines, runs, chapterBanner, eyebrow, accentDot } = D;

const V = JSON.parse(fs.readFileSync(process.env.VERBATIM||"verbatim.json","utf8"));
const PLAN = JSON.parse(fs.readFileSync(process.env.PLAN||"plan.json","utf8"));
const OV = fs.existsSync("overrides.json") ? JSON.parse(fs.readFileSync("overrides.json","utf8")) : {};

const paras = n => (V[String(n)]||[]).map(s=>s.trim()).filter(Boolean);
const key = (s,i) => `${s}:${i}`;

// step banners, taken verbatim from the deck's own divider slides
const DIV = {1:88, 2:127, 3:204, 4:272, 5:321};
const BANNER = {};
for (const [b,s] of Object.entries(DIV)){
  const t = (paras(s)[0]||"");
  if (!/^STEP\s*\d+:/i.test(t)) { delete BANNER[b]; continue; }                       // "STEP 1: THE TIME BASED RANGES"
  const m = t.match(/^(STEP\s*\d+)(:)\s*(.+)$/i);
  BANNER[b] = { head:m[1], sep:m[2], tail:m[3], full:t };
}

const pres = new pptxgen();
pres.layout = "LAYOUT_16x9";                    // 10 x 5.625 in — matches the source
pres.author = "DTR Live Class";

let emitted = 0;
const rendered = [];                            // for verbatim verification

function newSlide(g, dark){
  const s = pres.addSlide();
  s.background = { color: dark ? C.ink : C.paper };
  if (g.band > 0 && g.k !== "div"){
    const b = BANNER[g.band];
    chapterBanner(s, b.head, b.sep, b.tail, dark);
  }
  if (g.k !== "div" && g.k !== "cue") accentDot(s);
  emitted++;
  return s;
}
function say(t){ rendered.push(t); }

// ---------- collect blocks, deduping lines the source itself repeats -------
function blocksOf(g){
  const seen = new Set(), out = [];
  for (const s of g.src){
    const lines = [];
    paras(s).forEach((t,i) => { if (!seen.has(t)) { seen.add(t); lines.push({ t, s, i }); } });
    out.push(lines);
  }
  return out;
}
const accOf = (l) => (OV.acc && OV.acc[key(l.s,l.i)] !== undefined) ? OV.acc[key(l.s,l.i)] : undefined;
function resolveAccents(flat, max){
  const map = new Map();
  const hits = [];
  for (const l of flat){
    const ov = accOf(l);
    map.set(key(l.s,l.i), ov);
    if (ov === null) continue;
    if (D.pickAccent(l.t, ov)) hits.push(l);
  }
  map.full = new Set();
  if (hits.length === 0){                       // nothing numeric — reach for the vocabulary
    for (let i = flat.length-1; i >= 0; i--){
      const l = flat[i];
      if (accOf(l) === null) continue;
      const a = D.pickAccent(l.t, undefined, D.LEX);
      if (a){ map.set(key(l.s,l.i), l.t.slice(a[0], a[1])); hits.push(l); break; }
    }
  }
  if (hits.length === 0){                       // still nothing — one short line carries the colour
    const ok = l => accOf(l) !== null && l.t.length <= 48;
    // prefer a line from the first step, so the colour is there from the first click
    const first = flat.filter(l => l.s === flat[0].s).filter(ok);
    const cands = first.length ? first : flat.filter(ok);
    if (cands.length){
      const pick = cands.reduce((a,b) => b.t.length < a.t.length ? b : a);
      map.full.add(key(pick.s, pick.i));
    }
  } else if (max && hits.length > max){         // too much blue — keep the last few
    const keep = new Set(hits.slice(-max).map(l => key(l.s,l.i)));
    for (const l of hits) if (!keep.has(key(l.s,l.i))) map.set(key(l.s,l.i), null);
  }
  return map;
}
const colOf = (l, dark, full) => (OV.grey && OV.grey.includes(key(l.s,l.i)))
  ? C.muted : (full && full.has(key(l.s,l.i)))
  ? C.accent : (dark ? C.white : C.ink);

// ---------- vertical stack layout (statements / builds) -------------------
function layoutStack(blocks, top, bottom, dark){
  const all = blocks.flat();
  const total = all.reduce((n,l)=>n+l.t.length, 0);
  let bi = TIERS.indexOf(32);
  if (total > 130) bi--;   if (total > 240) bi--;
  if (total > 380) bi--;   if (total > 520) bi--;
  if (total < 60)  bi++;   if (total < 28)  bi++;
  const GAP = 0.34, LGAP = 0.10;

  for (;;){
    const base = TIERS[Math.max(0, Math.min(TIERS.length-1, bi))];
    const sized = blocks.map(bl => bl.map(l => {
      let s = base;
      if (l.t.length < 32) s = TIERS[Math.min(TIERS.length-1, TIERS.indexOf(base)+1)];
      if (l.t.length > 118) s = TIERS[Math.max(0, TIERS.indexOf(base)-1)];
      return { ...l, size:s, h: nlines(l.t, s, CW) * s * 1.24/72 };
    }));
    let h = 0;
    sized.forEach((bl,i) => { if (i) h += GAP;
      bl.forEach((l,j) => { if (j) h += LGAP; h += l.h; }); });
    if (h <= bottom - top || bi <= 0) {
      let y = top + Math.max(0, (bottom - top - h)/2);
      const placed = [];
      sized.forEach((bl,i) => { if (i) y += GAP;
        bl.forEach((l,j) => { if (j) y += LGAP; placed.push({ ...l, y }); y += l.h; }); });
      placed.base = base;
      return placed;
    }
    bi--;
  }
}

let ACC = new Map();
function drawStack(s, placed, upto, dark){
  for (const l of placed){
    if (l.blk > upto) continue;
    s.addText(runs(l.t, l.size, colOf(l,dark,ACC.full), ACC.get(key(l.s,l.i))),
      T({ x:RAIL, y:l.y, w:CW, h:l.h, fontSize:l.size, valign:"top" }));
  }
}

// ---------- kinds ---------------------------------------------------------
const NUMRE = /^(\d+\s*[.\-)])\s*(.+)$/s;

function kStack(g){
  const blocks = blocksOf(g);
  const A = resolveAccents(blocks.flat(), 2);
  const top = g.band > 0 ? 1.05 : 0.80;
  const placed = layoutStack(blocks, top, 5.20, false);
  let k = 0; blocks.forEach((bl,i)=> bl.forEach(()=> placed[k++].blk = i));
  ACC = A;
  blocks.forEach((_,i) => {
    const s = newSlide(g,false);
    drawStack(s, placed, i, false);
  });
  placed.forEach(l => say(l.t));
}

function kList(g){
  const blocks = blocksOf(g);
  const flat = blocks.flat();
  const A = resolveAccents(flat, 0);
  const headed = flat.length > 1 && !NUMRE.test(flat[0].t);
  const head = headed ? flat[0] : null;
  const rows = (headed ? flat.slice(1) : flat).map(l => {
    const m = l.t.match(NUMRE);
    return { ...l, num: m ? m[1] : null, body: m ? m[2] : l.t };
  });
  const top = g.band > 0 ? 1.05 : 0.80;
  let hy = top, hsz = 0, hh = 0;
  if (head){
    hsz = head.t.length > 70 ? 20 : (head.t.length > 40 ? 25 : 28);
    hh = nlines(head.t, hsz, CW) * hsz * 1.24/72;
  }
  const bx = rows.some(r=>r.num) ? 1.55 : 1.25, bw = 9.10 - bx;
  const rowTop = top + hh + (head ? 0.38 : 0);
  let rsz = 22;
  for (;;){
    const hs = rows.map(r => Math.max(0.30, nlines(r.body, rsz, bw) * rsz * 1.26/72));
    const gap = rsz >= 20 ? 0.32 : (rsz >= 17 ? 0.26 : 0.22);
    const tot = hs.reduce((a,b)=>a+b,0) + gap*(rows.length-1);
    if (tot <= 5.30 - rowTop || rsz <= 15){
      let y = rowTop + (rows.length <= 3 ? Math.max(0,(5.30-rowTop-tot)/3) : 0);
      rows.forEach((r,i) => { r.y = y; r.h = hs[i]; r.size = rsz; y += hs[i] + gap; });
      break;
    }
    rsz -= 1;
  }
  blocks.forEach((_,bi) => {
    const s = newSlide(g,false);
    if (head && head.s <= g.src[bi]) {
      s.addText(runs(head.t, hsz, C.ink, A.get(key(head.s,head.i))),
        T({ x:RAIL, y:hy, w:CW, h:hh, fontSize:hsz, valign:"top" }));
    }
    rows.forEach(r => {
      if (r.s > g.src[bi]) return;
      if (r.num){
        s.addText(r.num, T({ x:RAIL, y:r.y, w:0.60, h:Math.min(r.h,0.50),
          fontSize:Math.round(r.size*1.15), color:C.accent, valign:"top" }));
      } else {
        s.addShape("ellipse", { x:0.98, y:r.y + r.size*0.60/72, w:0.08, h:0.08, fill:{ color:C.hair } });
      }
      s.addText(runs(r.body, r.size, C.ink, A.get(key(r.s,r.i))),
        T({ x:bx, y:r.y, w:bw, h:r.h, fontSize:r.size, valign:"top" }));
    });
  });
  if (head) say(head.t);
  rows.forEach(r => say(r.num ? r.num + " " + r.body : r.body));
}

function kChat(g){
  const blocks = blocksOf(g);
  let flat = blocks.flat();
  if (flat.length === 1){
    const parts = flat[0].t.split(/(?<=[?.!…])\s+/).filter(Boolean);
    if (parts.length > 1){
      const lead = parts.slice(0,-1).join(" ");
      flat = [ { t:lead, s:flat[0].s, i:flat[0].i, frag:true },
               { t:parts[parts.length-1], s:flat[0].s, i:flat[0].i, frag:true } ];
    }
  }
  const A = resolveAccents(flat.slice(0,-1), 2);
  const pill = flat[flat.length-1];
  const rest = flat.slice(0, -1);
  const top = g.band > 0 ? 1.15 : 0.95;
  const placed = rest.length
    ? layoutStack([rest], top, 3.35, false).map(l => ({ ...l, blk: blocks.findIndex(b=>b.includes(rest.find(r=>r.t===l.t))) }))
    : [];
  rest.forEach((l,i) => { const p = placed[i]; if (p) p.blk = blocks.findIndex(b => b.some(x => x.t === l.t)); });
  // a pill standing on its own is the whole slide, so let it carry real weight
  const psz = rest.length ? 17 : 26;
  const ph  = rest.length ? 0.62 : 0.95;
  const pw = Math.max(2.60, Math.min(8.20, pill.t.length * 0.0072 * psz + (rest.length ? 0.80 : 1.20)));
  const py = rest.length ? 3.70 : (5.625 - ph)/2;
  blocks.forEach((_,i) => {
    const s = newSlide(g,false);
    placed.forEach(l => { if (l.blk <= i || l.frag)
      s.addText(runs(l.t, l.size, C.ink, A.get(key(l.s,l.i))),
        T({ x:RAIL, y:l.y, w:CW, h:l.h, fontSize:l.size, align:"center", valign:"top" })); });
    if (pill.frag || blocks[i].some(x => x.t === pill.t)){
      s.addShape("roundRect", { x:(10-pw)/2, y:py, w:pw, h:ph, rectRadius:ph/2, fill:{ color:C.accent } });
      s.addText(pill.t, T({ x:(10-pw)/2, y:py, w:pw, h:ph, fontSize:psz, color:C.white, align:"center" }));
    }
  });
  placed.forEach(l=>say(l.t)); say(pill.t);
}

function kCue(g){
  const s = newSlide(g, true);
  const ls = paras(g.src[0]);
  const lead = ls[0], body = ls.slice(1);
  const isLabel = lead.length <= 28 && !lead.startsWith("[");
  if (isLabel && body.length){
    eyebrow(s, lead, true);
    const placed = layoutStack([body.map((t,i)=>({t, s:g.src[0], i:i+1}))], 1.30, 5.00, true);
    placed.forEach(l => s.addText(runs(l.t, Math.min(l.size,25), C.muted, accOf(l)),
      T({ x:RAIL, y:l.y, w:CW, h:l.h, fontSize:Math.min(l.size,25), color:C.muted, valign:"top" })));
    say(lead); placed.forEach(l=>say(l.t));
  } else {
    const placed = layoutStack([ls.map((t,i)=>({t, s:g.src[0], i}))], 0.90, 5.00, true);
    const solo = ls.length === 1 && ls[0].length <= 34;
    placed.forEach(l => s.addText(runs(l.t, l.size, solo ? C.accent : C.white, solo ? null : accOf(l)),
      T({ x:RAIL, y:l.y, w:CW, h:l.h, fontSize:l.size, color: solo ? C.accent : C.white,
          align:"center", valign:"top" })));
    placed.forEach(l=>say(l.t));
  }
}

function kWord(g){
  const s = newSlide(g,false);
  const t = paras(g.src[0])[0];
  if (t.length <= 10){
    s.addText(t, T({ x:RAIL, y:1.45, w:CW, h:2.60, fontSize:150, color:C.accent, align:"center" }));
  } else {
    s.addText(runs(t, 40, C.ink, accOf({s:g.src[0], i:0})),
      T({ x:RAIL, y:2.00, w:CW, h:1.60, fontSize:40, align:"center" }));
  }
  say(t);
}

function kDiv(g){
  const s = newSlide(g,false);
  const b = BANNER[g.band];
  const n = b.head.match(/\d+/)[0];
  s.addShape("ellipse", { x:0.60, y:0.62, w:0.10, h:0.10, fill:{ color:C.accent } });
  s.addText([ { text:b.head, options:{ color:C.accent } },
              { text:b.sep,  options:{ color:C.hair } } ],
    T({ x:0.82, y:0.50, w:8.50, h:0.34, fontSize:11 }));
  const tsz = b.tail.length > 22 ? 34 : 40;
  s.addText(b.tail, T({ x:0.95, y:3.35, w:8.10, h:1.20, fontSize:tsz, color:C.ink, valign:"top" }));
  s.addText(n, T({ x:0.88, y:0.68, w:2.40, h:2.60, fontSize:150, color:C.accent, valign:"bottom" }));
  say(b.full);
}

function kPair(g){
  const blocks = blocksOf(g);
  const flat = blocks.flat();
  const A = resolveAccents(flat, 0);
  const dashed = flat.filter(l => /—|–/.test(l.t));
  const top = g.band > 0 ? 1.05 : 0.80;
  if (dashed.length >= 2 && dashed.length === flat.filter(l=>/—|–/.test(l.t)).length && dashed.length < flat.length){
    // heading + label — value rows
    const head = flat[0];
    const hsz = head.t.length > 55 ? 22 : 26;
    const hh = nlines(head.t, hsz, CW) * hsz * 1.24/72;
    const rows = flat.slice(1);
    const rh = 1.05;
    let y = top + hh + 0.60;
    rows.forEach(r => { r.y = y; y += rh; });
    blocks.forEach((_,i) => {
      const s = newSlide(g,false);
      if (head.s <= g.src[i]) s.addText(runs(head.t, hsz, C.ink, A.get(key(head.s,head.i))),
        T({ x:RAIL, y:top, w:CW, h:hh, fontSize:hsz, valign:"top" }));
      rows.forEach(r => {
        if (r.s > g.src[i]) return;
        const m = r.t.match(/^(.*?)(\s*[—–]\s*)(.*)$/s);
        const lab = m ? m[1] : r.t, dash = m ? m[2] : "", val = m ? m[3] : "";
        s.addShape("rect", { x:RAIL, y:r.y, w:0.07, h:0.72, fill:{ color:C.accent } });
        s.addText([ { text:lab, options:{ color:C.ink } },
                    { text:dash, options:{ color:C.hair } } ],
          T({ x:1.15, y:r.y, w:3.90, h:0.72, fontSize:24 }));
        s.addText(val, T({ x:5.10, y:r.y, w:4.00, h:0.72,
          fontSize:24, color:C.accent, align:"right" }));
      });
    });
    say(head.t); rows.forEach(r=>say(r.t));
  } else {
    // even horizontal strip
    const s = newSlide(g,false);
    const n = flat.length, colw = (CW - 0.30*(n-1))/n;
    flat.forEach((l,i) => {
      const x = RAIL + i*(colw+0.30);
      s.addShape("ellipse", { x:x, y:2.28, w:0.10, h:0.10, fill:{ color:C.accent } });
      s.addText(l.t, T({ x:x, y:2.55, w:colw, h:0.60, fontSize:26, color:C.ink, valign:"top" }));
    });
    flat.forEach(l=>say(l.t));
  }
}

// A merge is only worth doing while it stays readable. If a group would have to
// drop below 21pt to fit, split it back into two slides rather than cram one.
function splitBulky(g){
  if ((g.k !== "build" && g.k !== "stmt") || g.src.length < 3) return [g];
  const top = g.band > 0 ? 1.05 : 0.80;
  const base = layoutStack(blocksOf(g), top, 5.20, false).base;
  if (base >= 21) return [g];
  const mid = Math.ceil(g.src.length / 2);
  return [ { ...g, src:g.src.slice(0, mid) }, { ...g, src:g.src.slice(mid) } ].flatMap(splitBulky);
}
const PLAN2 = PLAN.flatMap(splitBulky);

const K = { stmt:kStack, build:kStack, num:kList, list:kList, chat:kChat,
            cue:kCue, word:kWord, div:kDiv, pair:kPair };
for (const g of PLAN2) K[g.k](g);

pres.writeFile({ fileName: process.env.OUT||"DTR_Intro_Content_designed.pptx" }).then(() => {
  fs.writeFileSync("rendered.json", JSON.stringify(rendered, null, 0));
  console.log(`conceptual slides: ${PLAN2.length} (from ${PLAN.length} groups)   physical slides: ${emitted}`);
});
