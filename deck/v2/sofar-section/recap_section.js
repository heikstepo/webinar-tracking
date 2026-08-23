// "So far on this free live workshop we've covered:" — rebuilt in the AA
// pattern: the line is introduced full size, then demotes to a persistent
// header box while the five items cycle one per slide.
const pptxgen = require("pptxgenjs");
const fs = require("fs");
const D = require("./ds2.js");
const { C, T, RAIL, CW, nlines, runs, accentDot } = D;

const P = JSON.parse(fs.readFileSync("plan2.json", "utf8"));
const S = P.slides;
const HEAD = S["326"].lines[0];
const ITEMS = [327, 328, 329, 330, 331].map(n => S[String(n)].lines[0]);

const NUM = /^(\d+\s*[.)\-])\s*(.+)$/s;
const rows = ITEMS.map(t => { const m = t.match(NUM); return { num: m[1], body: m[2] }; });

const pres = new pptxgen();
pres.layout = "LAYOUT_16x9";

// one size for all five, so the section holds still as it advances
const BAND_TOP = 1.98, BAND_BOT = 5.24, BODY_W = 8.00, BODY_X = (10 - BODY_W) / 2;
let bz = 40;
while (bz > 20 && rows.some(r => nlines(r.body, bz, BODY_W) > 5
       || nlines(r.body, bz, BODY_W) * bz * 1.24 / 72 > BAND_BOT - BAND_TOP)) bz -= 1;

function headerBox(s){
  s.addShape("rect", { x:0.72, y:0.30, w:8.56, h:0.66,
                       fill:{ color:C.paper }, line:{ color:C.hair, width:0.75 } });
  s.addText(runs(HEAD, 15, C.ink),
    T({ x:0.82, y:0.30, w:8.36, h:0.66, fontSize:15, align:"center" }));
}

// 1 — the line, full size
{
  const s = pres.addSlide();
  s.background = { color: C.paper };
  accentDot(s);
  let z = 44;
  while (z > 24 && nlines(HEAD, z, CW) * z * 1.24/72 > 2.30) z -= 2;
  const h = nlines(HEAD, z, CW) * z * 1.24/72;
  s.addText(runs(HEAD, z, C.ink),
    T({ x:RAIL, y:(5.625 - h)/2, w:CW, h, fontSize:z, align:"center" }));
}

// 2..6 — header stays put, one item at a time
rows.forEach(r => {
  const s = pres.addSlide();
  s.background = { color: C.paper };
  headerBox(s);
  s.addText(r.num, T({ x:RAIL, y:1.34, w:CW, h:0.48, fontSize:26,
                       color:C.accent, align:"center" }));
  const h = nlines(r.body, bz, BODY_W) * bz * 1.24/72;
  s.addText(runs(r.body, bz, C.ink),
    T({ x:BODY_X, y:BAND_TOP + Math.max(0, (BAND_BOT - BAND_TOP - h)/2),
        w:BODY_W, h, fontSize:bz, align:"center" }));
});

pres.writeFile({ fileName: process.env.OUT || "DTR_SoFar_Section.pptx" })
  .then(() => console.log(`slides: 6   item size: ${bz}pt`));
