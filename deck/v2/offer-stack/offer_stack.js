// The offer stack, modelled on AA: eyebrow + headline that hold still, and a
// spine of rows that grows downward from a fixed top, one node at a time.
const pptxgen = require("pptxgenjs");
const fs = require("fs");
const D = require("./ds2.js");
const { C, T, RAIL, nlines, textW, runs } = D;

const P = JSON.parse(fs.readFileSync("plan2.json", "utf8"));

// ---- added chrome (not in the script) --------------------------------------
const EYEBROW = "THE TIME BASED RANGES ACADEMY";
const HEAD_A  = "What You're ";
const HEAD_B  = "Getting";
const PILL    = "JUST ADDED";

// ---- the nine components, in the order the deck introduces them ------------
const ROWS = P.plan.filter(p => p.k === "stack").reduce((a, p) =>
  p.rows.length > a.length ? p.rows : a, []);
const CODE = /^((?:BONUS\s*\d+\s*:)|(?:\d+\s*[.)\-]))\s*(.+)$/s;
const rows = ROWS.map(t => { const m = t.match(CODE);
  return { code: m ? m[1] : "", label: m ? m[2] : t }; });

// how many nodes each stack slide shows: 1,2,3,4,5,6,7,8,9 then a final recap
const COUNTS = P.plan.filter(p => p.k === "stack").map(p => p.rows.length);

// ---- geometry --------------------------------------------------------------
const TOP = 1.82, BOTTOM = 5.46, GAP = 0.12;
const SPINE_X = 0.80, CODE_X = 0.98, CODE_W = 1.10, LABEL_X = 2.20;
const LABEL_W = 9.10 - LABEL_X;
const PILL_X = 7.95, PILL_W = 1.45, PILL_H = 0.32;

// biggest size at which all nine rows fit the frame; a long label may take two
// lines, and every row keeps the same position on every slide so nothing moves
let fs_ = 18, LINE = 0, ys = [], hs = [];
for (;; fs_--){
  LINE = fs_ * 1.26 / 72;
  hs = rows.map(r => nlines(r.label, fs_, LABEL_W) * LINE);
  const tot = hs.reduce((a, b) => a + b, 0) + GAP * (rows.length - 1);
  if (tot <= BOTTOM - TOP || fs_ <= 11){
    let y = TOP; ys = hs.map(h => { const v = y; y += h + GAP; return v; });
    break;
  }
}

const pres = new pptxgen();
pres.layout = "LAYOUT_16x9";

let seen = 0;
COUNTS.forEach(k => {
  const s = pres.addSlide();
  s.background = { color: C.ink };

  s.addShape("ellipse", { x:0.60, y:0.58, w:0.10, h:0.10, fill:{ color:C.accent } });
  s.addText(EYEBROW, T({ x:0.82, y:0.46, w:8.50, h:0.34, fontSize:11, color:C.white }));
  s.addText([{ text:HEAD_A, options:{ color:C.white } },
             { text:HEAD_B, options:{ color:C.accent } }],
    T({ x:0.60, y:0.82, w:8.60, h:0.86, fontSize:40, valign:"top" }));

  const newest = k > seen ? k - 1 : -1;
  seen = Math.max(seen, k);
  const cyOf = i => ys[i] + LINE/2;              // node sits on the row's first line

  if (k > 1) s.addShape("line", { x:SPINE_X, y:cyOf(0), w:0, h:cyOf(k-1) - cyOf(0),
    line:{ color:C.darkRule, width:2 } });

  rows.slice(0, k).forEach((r, i) => {
    const y = ys[i], cy = cyOf(i), on = i === newest;
    if (on) s.addShape("ellipse", { x:SPINE_X-0.15, y:cy-0.15, w:0.30, h:0.30, fill:{ color:C.accent } });
    else {
      s.addShape("ellipse", { x:SPINE_X-0.10, y:cy-0.10, w:0.20, h:0.20, fill:{ color:C.accent } });
      s.addShape("ellipse", { x:SPINE_X-0.05, y:cy-0.05, w:0.10, h:0.10, fill:{ color:C.ink } });
    }
    s.addText(r.code,  T({ x:CODE_X, y:y, w:CODE_W, h:LINE, fontSize:fs_,
                           color:C.accent, align:"right", valign:"top" }));
    s.addText(r.label, T({ x:LABEL_X, y:y, w:LABEL_W, h:hs[i], fontSize:fs_,
                           color: on ? C.accent : C.white, valign:"top" }));

    // the pill only where the row is short enough to leave it room
    if (on && LABEL_X + textW(r.label, fs_) + 0.30 < PILL_X){
      s.addShape("roundRect", { x:PILL_X, y:cy - PILL_H/2, w:PILL_W, h:PILL_H,
                                rectRadius:PILL_H/2, fill:{ color:C.accent } });
      s.addText(PILL, T({ x:PILL_X, y:cy - PILL_H/2, w:PILL_W, h:PILL_H,
                          fontSize:10, color:C.white, align:"center" }));
    }
  });
});

pres.writeFile({ fileName: process.env.OUT || "DTR_Offer_Stack.pptx" })
  .then(() => console.log(`slides: ${COUNTS.length}   rows: ${rows.length}   row size: ${fs_}pt`));
