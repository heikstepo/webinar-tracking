// "Option 2" — the header holds in a box, one point per slide.
const pptxgen = require("pptxgenjs");
const fs = require("fs");
const D = require("./ds2.js");
const { C, T, RAIL, CW, nlines, runs } = D;

const HEAD = "I could take a more active role and responsibility, and ACTUALLY give you everything you need to help you:";
const ITEMS = [
  "1- Get my NDA-protected & private ranges, entries, workbooks, and more…",
  "2- Execute it consistently, with me working on your trades directly…",
  "3- Get funded, with the exact prop firm rules that get you approved and keep you there…",
];

const NUM = /^(\d+\s*[.)\-])\s*(.+)$/s;
const rows = ITEMS.map(t => { const m = t.match(NUM); return { num: m[1], body: m[2] }; });

// the header box, sized to however many lines the header actually needs
const BOX_X = 0.72, BOX_W = 8.56, TXT_W = BOX_W - 0.40;
let hz = 16;
while (hz > 11 && nlines(HEAD, hz, TXT_W) > 2) hz -= 1;
const hLines = nlines(HEAD, hz, TXT_W);
const BOX_H = Math.max(0.66, hLines * hz * 1.30/72 + 0.30);
const BOX_Y = 0.30;

const BAND_TOP = BOX_Y + BOX_H + 0.34, BAND_BOT = 5.32;   // space below the header
const NUM_H = 0.48, NUM_GAP = 0.20;
const BODY_W = 8.00, BODY_X = (10 - BODY_W) / 2;
let bz = 46;
while (bz > 20 && rows.some(r => nlines(r.body, bz, BODY_W) > 4
       || NUM_H + NUM_GAP + nlines(r.body, bz, BODY_W) * bz * 1.24/72 > BAND_BOT - BAND_TOP)) bz -= 1;

const pres = new pptxgen();
pres.layout = "LAYOUT_16x9";

rows.forEach(r => {
  const s = pres.addSlide();
  s.background = { color: C.paper };
  s.addShape("rect", { x:BOX_X, y:BOX_Y, w:BOX_W, h:BOX_H,
                       fill:{ color:C.paper }, line:{ color:C.hair, width:0.75 } });
  s.addText(runs(HEAD, hz, C.ink),
    T({ x:BOX_X + 0.20, y:BOX_Y, w:TXT_W, h:BOX_H, fontSize:hz, align:"center" }));
  // numeral and text travel together, centred in the space under the header
  const h = nlines(r.body, bz, BODY_W) * bz * 1.24/72;
  const group = NUM_H + NUM_GAP + h;
  const gy = BAND_TOP + Math.max(0, (BAND_BOT - BAND_TOP - group)/2);
  s.addText(r.num, T({ x:RAIL, y:gy, w:CW, h:NUM_H, fontSize:26,
                       color:C.accent, align:"center" }));
  s.addText(runs(r.body, bz, C.ink),
    T({ x:BODY_X, y:gy + NUM_H + NUM_GAP, w:BODY_W, h, fontSize:bz, align:"center" }));
});

pres.writeFile({ fileName: process.env.OUT || "DTR_Option2_Section.pptx" })
  .then(() => console.log(`slides: 3   header: ${hz}pt x${hLines} lines   item: ${bz}pt`));
