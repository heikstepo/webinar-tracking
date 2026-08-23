const pptxgen = require("pptxgenjs");
const fs = require("fs");
const D = require("./ds2.js");
const { C, T, CW, RAIL, TIERS, nlines, textW, runs, chapterBanner, eyebrow, accentDot } = D;

const P = JSON.parse(fs.readFileSync("plan2.json", "utf8"));
const S = P.slides, BAN = P.banners;
const OV = fs.existsSync("overrides2.json")
  ? JSON.parse(fs.readFileSync("overrides2.json", "utf8")) : { acc:{}, grey:[] };

const pres = new pptxgen();
pres.layout = "LAYOUT_16x9";
let emitted = 0;

const linesOf = n => S[String(n)].lines;
const picsOf  = n => S[String(n)].pics || [];
const accOf   = t => (OV.acc && OV.acc[t] !== undefined) ? OV.acc[t] : undefined;

function newSlide(g, dark){
  const s = pres.addSlide();
  s.background = { color: dark ? C.ink : C.paper };
  if (g.band > 0 && g.k !== "div"){
    const b = BAN[g.band];
    if (b) chapterBanner(s, b.head, b.sep, b.tail, dark);
  }
  emitted++;
  return s;
}

// ---- vertical stack of lines, sized for air -------------------------------
function sizeFor(total){
  if (total <=  30) return 52;
  if (total <=  55) return 46;
  if (total <=  95) return 40;
  if (total <= 150) return 32;
  if (total <= 230) return 28;
  if (total <= 330) return 25;
  if (total <= 450) return 22;
  return 19;
}
function layout(blocks, top, bottom){
  const all = blocks.flat();
  const total = all.reduce((n,t)=>n+t.length, 0);
  let bi = TIERS.indexOf(sizeFor(total));
  const GAP = 0.36, LGAP = 0.12;
  for (;;){
    const base = TIERS[Math.max(0, bi)];
    const sized = blocks.map(bl => bl.map(t => {
      let sz = base;
      if (t.length < 26)  sz = TIERS[Math.min(TIERS.length-1, TIERS.indexOf(base)+1)];
      if (t.length > 130) sz = TIERS[Math.max(0, TIERS.indexOf(base)-1)];
      return { t, sz, h: nlines(t, sz, CW) * sz * 1.26/72 };
    }));
    let h = 0;
    sized.forEach((bl,i)=>{ if (i) h += GAP; bl.forEach((l,j)=>{ if (j) h += LGAP; h += l.h; }); });
    if (h <= bottom - top || bi <= 0){
      let y = top + Math.max(0, (bottom - top - h)/2);
      const out = [];
      sized.forEach((bl,i)=>{ if (i) y += GAP;
        bl.forEach((l,j)=>{ if (j) y += LGAP; out.push({ ...l, y, blk:i }); y += l.h; }); });
      return out;
    }
    bi--;
  }
}

// every slide must carry the colour somewhere in its text
function withAccent(placed){
  const hits = placed.filter(l => D.pickAccent(l.t, accOf(l.t)));
  if (hits.length > 4){                        // too much colour reads as none
    const keep = new Set([hits[0], ...hits.slice(-3)]);
    hits.forEach(l => { if (!keep.has(l)) l.mute = true; });
  }
  if (hits.length) return;
  for (let i = placed.length-1; i >= 0; i--){
    const k = D.keyword(placed[i].t);
    if (k){ placed[i].force = k; return; }
  }
  // nothing but small words: the shortest line goes teal whole, the way AA does it
  const pick = placed.reduce((a,b) => b.t.length < a.t.length ? b : a);
  pick.force = [0, pick.t.length];
}
function drawLine(s, l, dark){
  const col = (OV.grey || []).includes(l.t) ? C.muted : (dark ? C.white : C.ink);
  const r = l.force
    ? [{ text:l.t.slice(0,l.force[0]), options:{ fontSize:l.sz, color:col } },
       { text:l.t.slice(l.force[0],l.force[1]), options:{ fontSize:l.sz, color:C.accent } },
       { text:l.t.slice(l.force[1]), options:{ fontSize:l.sz, color:col } }].filter(x=>x.text)
    : runs(l.t, l.sz, col, l.mute ? null : accOf(l.t));
  s.addText(r, T({ x:RAIL, y:l.y, w:CW, h:l.h, fontSize:l.sz, valign:"top" }));
}

function kStmt(g){
  const blocks = g.slides.map(linesOf);
  if (g.slides.length === 1 && blocks[0].length === 1 && blocks[0][0].length <= 14){
    const t = blocks[0][0];
    const s = newSlide(g, false);
    accentDot(s);
    let z = 130;
    while (z > 44 && nlines(t, z, CW) > 1) z -= 6;
    s.addText(t, T({ x:RAIL, y:1.35, w:CW, h:2.60, fontSize:z, color:C.accent,
                     align:"center", valign:"middle" }));
    picsOf(g.slides[0]).forEach(p => addPic(s, p));
    return;
  }
  const top = g.band > 0 ? 1.10 : 0.85;
  const placed = layout(blocks, top, 5.20);
  withAccent(placed);
  g.slides.forEach((n,i) => {
    const s = newSlide(g, false);
    accentDot(s);
    placed.forEach(l => { if (l.blk <= i) drawLine(s, l, false); });
    picsOf(n).forEach(p => addPic(s, p));
  });
}

// ---- numbered / lettered lists (AA's agenda and Q rows) -------------------
const NUM = /^((?:Q\d+\s*[-–—:])|(?:BONUS\s*\d+\s*:)|(?:\d+\s*[.)\-]))\s*(.+)$/s;
function kList(g){
  const blocks = g.slides.map(linesOf);
  const flat = blocks.flatMap((bl,i) => bl.map(t => ({ t, blk:i })));
  const headed = !NUM.test(flat[0].t);
  const head = headed ? flat[0] : null;
  const rows = (headed ? flat.slice(1) : flat).map(l => {
    const m = l.t.match(NUM);
    return { ...l, num: m ? m[1] : null, body: m ? m[2] : l.t };
  });
  const top = g.band > 0 ? 1.10 : 0.85;
  let numW = 0.30;
  if (rows.some(r=>r.num))
    numW = Math.min(1.75, Math.max(...rows.filter(r=>r.num).map(r => textW(r.num, 22))) + 0.12);
  const bx = rows.some(r=>r.num) ? RAIL + numW + 0.24 : 1.28, bw = 9.10 - bx;

  // find the largest heading/row pair that genuinely fits the canvas
  let hsz = 0, hh = 0, rsz = 0;
  const headMax = head ? (head.t.length > 78 ? 24 : (head.t.length > 44 ? 28 : 32)) : 0;
  outer:
  for (let hs = headMax; hs >= (head ? 18 : 0); hs -= 2){
    const hgt = head ? nlines(head.t, hs, CW) * hs * 1.26/72 : 0;
    for (let rs = 26; rs >= 13; rs -= 1){
      const hsArr = rows.map(r => Math.max(0.32, nlines(r.body, rs, bw) * rs * 1.28/72));
      const gap = rs >= 22 ? 0.34 : (rs >= 18 ? 0.27 : 0.21);
      const tot = hsArr.reduce((a,b)=>a+b,0) + gap*(rows.length-1);
      if (tot <= 5.34 - (top + hgt + (head?0.40:0)) || (hs <= (head?18:0) && rs <= 13)){
        hsz = hs; hh = hgt; rsz = rs;
        const block = hh + (head?0.40:0) + tot;
        const hy = top + Math.max(0, (5.34 - top - block)/2);
        let y = hy + hh + (head?0.40:0);
        rows.forEach((r,i)=>{ r.y = y; r.h = hsArr[i]; r.sz = rs; y += hsArr[i] + gap; });
        if (head){ head.y = hy; head.h = hh; head.sz = hs; }
        break outer;
      }
    }
  }
  g.slides.forEach((n,i) => {
    const s = newSlide(g, false);
    accentDot(s);
    if (head && head.blk <= i)
      s.addText(runs(head.t, head.sz, C.ink, accOf(head.t)),
        T({ x:RAIL, y:head.y, w:CW, h:head.h, fontSize:head.sz, valign:"top" }));
    rows.forEach(r => {
      if (r.blk > i) return;
      if (r.num) s.addText(r.num, T({ x:RAIL, y:r.y, w:numW+0.16, h:Math.min(r.h,0.58),
        fontSize:Math.round(r.sz*1.05), color:C.accent, valign:"top" }));
      else s.addShape("ellipse", { x:0.98, y:r.y + r.sz*0.62/72, w:0.09, h:0.09,
        fill:{ color:C.accent } });
      s.addText(runs(r.body, r.sz, C.ink, accOf(r.body)),
        T({ x:bx, y:r.y, w:bw, h:r.h, fontSize:r.sz, valign:"top" }));
    });
    picsOf(n).forEach(p => addPic(s, p));
  });
}

// ---- the five-step structure slide (AA's "3 parts of an agency" layout) ---
// numeral / title / quiet descriptor, so the slide reads as a structure and
// not as five wrapping sentences.
const DASH = /^(.*?)\s*([—–])\s*(.+)$/s;
function kSteps(g){
  const rows = g.slides.flatMap(linesOf).map(t => {
    const m = t.match(NUM);
    const num = m ? m[1] : "", rest = m ? m[2] : t;
    const d = rest.match(DASH);
    return { num, title: d ? d[1] : rest, dash: d ? d[2] : "", desc: d ? d[3] : "" };
  });
  const numW = Math.min(1.50, Math.max(...rows.map(r => textW(r.num, 52))) + 0.18);
  const bx = RAIL + numW + 0.30, bw = 9.10 - bx;
  let tz = 32;
  for (;;){
    const dz = Math.max(13, Math.round(tz*0.60));
    const th = tz*1.22/72, dh = dz*1.30/72;
    const rowH = th + dh + 0.06;
    const gap = tz*0.008;
    const tot = rows.length*rowH + gap*(rows.length-1);
    const fits = tot <= 4.72 && rows.every(r => nlines(r.title, tz, bw) === 1
                                             && (!r.desc || nlines(r.dash+" "+r.desc, dz, bw) === 1));
    if (fits || tz <= 20){
      let y = 0.72 + Math.max(0, (5.44 - 0.72 - tot)/2);
      const s = newSlide(g, false);
      accentDot(s);
      const nz = Math.round(tz*1.75);
      rows.forEach(r => {
        s.addText(r.num, T({ x:RAIL, y:y - 0.12, w:numW, h:th + 0.34, fontSize:nz,
                             color:C.accent, valign:"top" }));
        s.addText(r.title, T({ x:bx, y:y, w:bw, h:th, fontSize:tz, color:C.ink, valign:"top" }));
        if (r.desc) s.addText([{ text:r.dash+" ", options:{ color:C.hair } },
                               { text:r.desc,     options:{ color:C.sub } }],
          T({ x:bx, y:y + th + 0.06, w:bw, h:dh, fontSize:dz, valign:"top" }));
        y += rowH + gap;
      });
      return;
    }
    tz -= 1;
  }
}

// ---- step divider ---------------------------------------------------------
function kDiv(g){
  const n = g.slides[0];
  const b = BAN[g.band] || {};
  const s = newSlide({ ...g, k:"div" }, false);
  accentDot(s);
  s.addText([{ text:b.head, options:{ color:C.accent } },
             { text:b.sep,  options:{ color:C.hair } }],
    T({ x:0.82, y:0.50, w:8.50, h:0.34, fontSize:11 }));
  let tz = 46;
  while (tz > 26 && nlines(b.tail, tz, CW)*tz*1.26/72 > 1.60) tz -= 2;
  s.addText(b.tail, T({ x:0.95, y:3.30, w:8.10, h:1.30, fontSize:tz, color:C.ink, valign:"top" }));
  s.addText(String(b.head).match(/\d+/)[0],
    T({ x:0.88, y:0.62, w:2.40, h:2.55, fontSize:150, color:C.accent, valign:"bottom" }));
  linesOf(n).slice(1).forEach(() => {});
  picsOf(n).forEach(p => addPic(s, p));
}

// ---- the offer stack (AA's recurring "what you're getting" slide) ---------
const CODE = /^((?:BONUS\s*\d+\s*:)|(?:\d+\s*[.)\-]))\s*(.+)$/s;
const PITCH = 0.46, ROW = 0.35, SPINE_X = 0.80;
let stackSeen = 0;
function kStack(g){
  const n = g.slides[0];
  const s = newSlide(g, true);
  const rows = (g.rows || []).map(t => {
    const m = t.match(CODE);
    return { code: m ? m[1] : "", label: m ? m[2] : t };
  });
  const k = rows.length;
  const newest = k > stackSeen ? k-1 : -1;
  stackSeen = Math.max(stackSeen, k);
  let fs = 15;
  const LABEL_X = 2.42, LABEL_W = 6.68;
  while (fs > 11 && rows.some(r => nlines(r.label, fs, LABEL_W) > 1)) fs -= 1;
  const total = (k-1)*PITCH + ROW, y0 = (5.625 - total)/2;
  const yOf = i => y0 + i*PITCH;
  if (k > 1) s.addShape("line", { x:SPINE_X, y:yOf(0)+ROW/2, w:0, h:(k-1)*PITCH,
    line:{ color:C.darkRule, width:2 } });
  rows.forEach((r,i) => {
    const y = yOf(i), cy = y + ROW/2, on = i === newest;
    if (on) s.addShape("ellipse", { x:SPINE_X-0.15, y:cy-0.15, w:0.30, h:0.30, fill:{ color:C.accent } });
    else {
      s.addShape("ellipse", { x:SPINE_X-0.10, y:cy-0.10, w:0.20, h:0.20, fill:{ color:C.accent } });
      s.addShape("ellipse", { x:SPINE_X-0.05, y:cy-0.05, w:0.10, h:0.10, fill:{ color:C.ink } });
    }
    s.addText(r.code,  T({ x:1.00, y:y, w:1.20, h:ROW, fontSize:fs, color:C.accent, align:"right" }));
    s.addText(r.label, T({ x:LABEL_X, y:y, w:LABEL_W, h:ROW, fontSize:fs,
                           color: on ? C.accent : C.white }));
  });
  s.addNotes("STACK");
}

// ---- a live chart shot ----------------------------------------------------
function addPic(s, p){
  if (!p.file || !fs.existsSync(p.file)) return;
  s.addImage({ path:p.file, x:p.x, y:p.y, w:p.w, h:p.h });
}
function kShot(g){
  const n = g.slides[0];
  const s = newSlide(g, true);
  const L = linesOf(n);
  if (L.length) eyebrow(s, L[0], true);
  else accentDot(s);
  picsOf(n).forEach(p => addPic(s, p));
  L.slice(1).forEach((t,i) =>
    s.addText(runs(t, 20, C.muted, undefined), T({ x:RAIL, y:4.70 + i*0.34, w:CW, h:0.34,
      fontSize:20, color:C.muted, valign:"top" })));
}

// ---- an offer component's own slide (AA's "what you get" opener) ---------
function kItem(g){
  const n = g.slides[0];
  const s = newSlide(g, false);
  accentDot(s);
  const t = linesOf(n)[0];
  const m = t.match(CODE);
  const code = m ? m[1] : "", title = m ? m[2] : t;
  if (code) s.addText(code, T({ x:RAIL, y:1.55, w:CW, h:0.46, fontSize:26,
                                color:C.accent, valign:"top" }));
  let tz = 46;
  while (tz > 24 && nlines(title, tz, CW)*tz*1.26/72 > 2.00) tz -= 2;
  const th = nlines(title, tz, CW)*tz*1.26/72;
  s.addText(title, T({ x:RAIL, y:2.20, w:CW, h:th, fontSize:tz, color:C.ink, valign:"top" }));
  picsOf(n).forEach(p => addPic(s, p));
}

const K = { stmt:kStmt, list:kList, steps:kSteps, div:kDiv, stack:kStack, shot:kShot, item:kItem };
for (const g of P.plan) K[g.k](g);

pres.writeFile({ fileName: process.env.OUT || "DTR_Webinar_V2.pptx" })
  .then(() => console.log(`conceptual: ${P.plan.length}   physical: ${emitted}`));
