// 18 minimal conceptual graphics for the TBR workshop deck.
// Native PowerPoint shapes throughout — vector, editable, recolourable.
// INVERT=1 builds the dark-frame version.
const pptxgen = require("pptxgenjs");
const D = require("./ds2.js");
const { C, T } = D;

const INV   = !!process.env.INVERT;
const BG    = INV ? C.ink   : C.paper;
const FG    = INV ? C.white : C.ink;
const QUIET = INV ? C.sub   : C.muted;      // de-emphasised mass / "everything else"
const RULE  = INV ? "3A3A3A" : C.hair;      // hairlines and boxes
const AC    = C.accent;

const pres = new pptxgen();
pres.layout = "LAYOUT_16x9";

// ---- primitives ------------------------------------------------------------
function slide(note){
  const s = pres.addSlide();
  s.background = { color: BG };
  s.addNotes(note);
  return s;
}
// a line between two arbitrary points
function seg(s, x1, y1, x2, y2, color = FG, width = 2, dash){
  const x = Math.min(x1, x2), y = Math.min(y1, y2);
  const w = Math.abs(x2 - x1), h = Math.abs(y2 - y1);
  const flipV = (x2 - x1) * (y2 - y1) < 0;
  const ln = { color, width };
  if (dash) ln.dashType = dash;
  s.addShape("line", { x, y, w, h, flipV, line: ln });
}
// triangular arrowhead; dir: r | l | u | d
function head(s, x, y, size, color = AC, dir = "r"){
  const rot = { u:0, r:90, d:180, l:270 }[dir];
  s.addShape("triangle", { x: x - size/2, y: y - size/2, w: size, h: size,
                           fill: { color }, rotate: rot });
}
const label = (s, t, x, y, w, o = {}) => s.addText(t,
  T({ x, y, w, h: o.h || 0.30, fontSize: o.sz || 11, color: o.color || FG,
      align: o.align || "center", valign: "middle" }));
const big = (s, t, x, y, w, sz, color) => s.addText(t,
  T({ x, y, w, h: sz * 1.3/72, fontSize: sz, color, align: "center", valign: "middle" }));
// a padlock, drawn shackle-first so the body covers its lower half
function padlock(s, cx, cy, k = 1, color = QUIET){
  s.addShape("roundRect", { x: cx - 0.11*k, y: cy - 0.20*k, w: 0.22*k, h: 0.26*k,
    rectRadius: 0.10*k, fill: { type:"none" }, line: { color, width: 2 } });
  s.addShape("roundRect", { x: cx - 0.17*k, y: cy - 0.06*k, w: 0.34*k, h: 0.26*k,
    rectRadius: 0.04*k, fill: { color } });
}

// ══ 1 ═ Price can do anything. Time can't. ═════════════ slides 50–52 ═══════
{
  const s = slide("Graphic 1 — for slides 50-52: \"Price can do anything on any given day... Time can't\"");
  seg(s, 5.0, 1.30, 5.0, 4.55, RULE, 1);
  label(s, "PRICE", 0.70, 1.30, 3.70, { sz: 12, color: QUIET });
  const pts = [[1.00,3.55],[1.45,2.55],[1.90,3.95],[2.35,2.20],[2.80,3.30],
               [3.25,2.05],[3.70,3.70],[4.15,2.70],[4.55,3.35]];
  for (let i = 1; i < pts.length; i++)
    seg(s, pts[i-1][0], pts[i-1][1], pts[i][0], pts[i][1], QUIET, 2.5);
  label(s, "unpredictable", 0.70, 4.30, 3.70, { sz: 12, color: QUIET });

  label(s, "TIME", 5.45, 1.30, 3.85, { sz: 12, color: AC });
  seg(s, 5.60, 3.00, 9.05, 3.00, AC, 2);
  for (let i = 0; i <= 8; i++)
    s.addShape("rect", { x: 5.60 + i*0.431 - 0.015, y: 2.66, w: 0.03, h: 0.34, fill: { color: AC } });
  label(s, "the same, every day, forever", 5.45, 4.30, 3.85, { sz: 12, color: AC });
}

// ══ 2 ═ Liquidity = orders resting ═══════════════════════ slides 95–96 ═════
{
  const s = slide("Graphic 2 — for slides 95-96: \"That's all liquidity means... orders waiting to get filled\"");
  const X = 3.00, W = 4.00, TOPY = 2.32, BOTY = 3.90;
  s.addShape("rect", { x: X, y: TOPY, w: W, h: BOTY - TOPY,
                       fill: { type:"none" }, line: { color: RULE, width: 1.25 } });
  seg(s, X - 0.45, TOPY, X + W + 0.45, TOPY, FG, 2);
  seg(s, X - 0.45, BOTY, X + W + 0.45, BOTY, FG, 2);
  label(s, "HIGH", X + W + 0.55, TOPY - 0.15, 1.20, { sz: 11, color: QUIET, align: "left" });
  label(s, "LOW",  X + W + 0.55, BOTY - 0.15, 1.20, { sz: 11, color: QUIET, align: "left" });
  for (let i = 0; i < 4; i++){
    const w = 2.30 - i*0.34;
    s.addShape("rect", { x: X + W/2 - w/2, y: TOPY - 0.30 - i*0.24, w, h: 0.10, fill: { color: AC } });
    s.addShape("rect", { x: X + W/2 - w/2, y: BOTY + 0.20 + i*0.24, w, h: 0.10, fill: { color: AC } });
  }
  label(s, "ORDERS RESTING", X, 1.02, W, { sz: 12, color: AC });
  label(s, "ORDERS RESTING", X, 4.86, W, { sz: 12, color: AC });
}

// ══ 3 ═ The range forms INSIDE the dealing range ════════ slides 104–110 ════
{
  const s = slide("Graphic 3 — for slides 104-110: the time based range must form INSIDE the dealing range");
  const OX = 1.70, OW = 5.40, OT = 2.05, OB = 4.20;
  s.addShape("rect", { x: OX, y: OT, w: OW, h: OB - OT,
                       fill: { type:"none" }, line: { color: RULE, width: 1.25 } });
  seg(s, OX, OT, OX + OW, OT, FG, 2);
  seg(s, OX, OB, OX + OW, OB, FG, 2);
  label(s, "DEALING RANGE", OX + OW + 0.18, OT - 0.15, 1.70, { sz: 11, color: QUIET, align: "left" });
  const IX = 3.55, IW = 1.90, IT = 2.55, IB = 3.62;
  s.addShape("rect", { x: IX, y: IT, w: IW, h: IB - IT,
                       fill: { color: AC, transparency: 88 }, line: { color: AC, width: 2 } });
  label(s, "TIME BASED RANGE", IX - 0.70, IB + 0.12, IW + 1.40, { sz: 11, color: AC });
  for (let i = 0; i < 3; i++){
    const w = 1.50 - i*0.30;
    s.addShape("rect", { x: OX + OW/2 - w/2, y: OT - 0.16 - i*0.19, w, h: 0.08, fill: { color: AC } });
    s.addShape("rect", { x: OX + OW/2 - w/2, y: OB + 0.08 + i*0.19, w, h: 0.08, fill: { color: AC } });
  }
  label(s, "both stacks still untouched", 0.80, 5.06, 8.40, { sz: 12, color: QUIET });
}

// ══ 4 ═ The loop ══════════════════════════════════════ slides 129–134 ══════
{
  const s = slide("Graphic 4 — for slides 129-134: the losing loop (spike, buy, reverse, stopped out, flip, reverse again)");
  const cx = 5.0, cy = 2.95, r = 1.32;
  s.addShape("ellipse", { x: cx - r, y: cy - r, w: r*2, h: r*2,
                          fill: { type:"none" }, line: { color: RULE, width: 1.5 } });
  const steps = ["Market spikes", "You buy", "It reverses",
                 "Stops you out", "You flip and sell", "It reverses again"];
  steps.forEach((t, i) => {
    const a = -Math.PI/2 + i * (2*Math.PI/6);
    const nx = cx + r*Math.cos(a), ny = cy + r*Math.sin(a);
    s.addShape("ellipse", { x: nx - 0.075, y: ny - 0.075, w: 0.15, h: 0.15, fill: { color: AC } });
    const lx = cx + (r + 0.52)*Math.cos(a), ly = cy + (r + 0.52)*Math.sin(a);
    label(s, t, lx - 1.15, ly - 0.16, 2.30, { sz: 12, color: FG });
  });
  head(s, cx + r*Math.cos(Math.PI/12), cy + r*Math.sin(Math.PI/12), 0.22, AC, "d");
}

// ══ 5 ═ Sweep one side, trade to the other ═══════════════ slide 158 ════════
{
  const s = slide("Graphic 5 — for slide 158: \"Sweep one side, trade to the other side. That's the trade.\"");
  const X = 2.40, W = 5.20, TOPY = 1.85, BOTY = 4.05;
  s.addShape("rect", { x: X, y: TOPY, w: W, h: BOTY - TOPY,
                       fill: { type:"none" }, line: { color: RULE, width: 1.25 } });
  seg(s, X, TOPY, X + W, TOPY, FG, 2);
  seg(s, X, BOTY, X + W, BOTY, FG, 2);
  seg(s, X + 0.55, 2.95, X + 1.65, BOTY + 0.42, AC, 3);       // dive through the low
  seg(s, X + 1.65, BOTY + 0.42, X + 4.55, TOPY - 0.05, AC, 3); // run to the opposing end
  head(s, X + 4.62, TOPY - 0.14, 0.26, AC, "u");
  s.addShape("ellipse", { x: X + 1.65 - 0.09, y: BOTY + 0.42 - 0.09, w: 0.18, h: 0.18,
                          fill: { color: AC } });
  label(s, "SWEPT", X + 0.70, BOTY + 0.62, 1.90, { sz: 11, color: AC, align: "left" });
  label(s, "TARGET", X + W + 0.15, TOPY - 0.16, 1.40, { sz: 11, color: AC, align: "left" });
}

// ══ 6 ═ The market grades itself — 25 / 50 / 75 ═════ slides 239, 243–247 ═══
{
  const s = slide("Graphic 6 — for slides 239/243-247: the market grades itself 25, 50, 75 on the way to target. "
    + "Levels are unlabelled on purpose — send me the wording for each and I'll add it.");
  const x = 4.55, top = 1.30, bot = 4.75, h = bot - top;
  s.addShape("rect", { x: x - 0.06, y: top, w: 0.12, h, fill: { color: RULE } });
  s.addShape("rect", { x: x - 0.06, y: top, w: 0.12, h: h*0.75, fill: { color: AC } });
  label(s, "TARGET", x + 0.42, top - 0.16, 2.20, { sz: 12, color: FG, align: "left" });
  label(s, "ENTRY",  x + 0.42, bot - 0.14, 2.20, { sz: 12, color: FG, align: "left" });
  [25, 50, 75].forEach(p => {
    const y = bot - h * (p/100);
    seg(s, x - 0.40, y, x + 0.34, y, FG, 1.5);
    s.addShape("ellipse", { x: x - 0.10, y: y - 0.10, w: 0.20, h: 0.20, fill: { color: AC } });
    label(s, String(p), x + 0.44, y - 0.15, 0.90, { sz: 18, color: AC, align: "left" });
  });
}

// ══ 7 ═ All four steps inside ~12 minutes ════════════════ slide 265 ════════
{
  const s = slide("Graphic 7 — for slide 265: all 4 steps happen inside about 12 minutes, same order, every day");
  const x0 = 1.05, x1 = 8.95, y = 3.05;
  seg(s, x0, y, x1, y, RULE, 2);
  const steps = ["RANGE", "BIAS", "ENTRY", "EXIT"];
  steps.forEach((t, i) => {
    const px = x0 + (x1 - x0) * ((i + 0.5) / 4);
    s.addShape("ellipse", { x: px - 0.13, y: y - 0.13, w: 0.26, h: 0.26, fill: { color: AC } });
    s.addText(String(i + 1), T({ x: px - 0.50, y: y - 0.86, w: 1.00, h: 0.34,
      fontSize: 15, color: AC, align: "center" }));
    label(s, t, px - 0.95, y + 0.30, 1.90, { sz: 15, color: FG });
  });
  head(s, x1 + 0.06, y, 0.20, RULE, "r");
  label(s, "~12 MINUTES", x0, 4.34, x1 - x0, { sz: 12, color: QUIET });
}

// ══ 8 ═ Tip of the iceberg ═══════════════════════════════ slide 295 ═══════
{
  const s = slide("Graphic 8 — for slide 295: \"It's genuinely the tip of the iceberg\"");
  const wl = 2.62;
  s.addShape("trapezoid", { x: 2.72, y: wl, w: 4.56, h: 2.30, fill: { color: QUIET }, rotate: 180 });
  s.addShape("triangle", { x: 4.36, y: 1.58, w: 1.28, h: 1.04, fill: { color: AC } });
  seg(s, 0.85, wl, 9.15, wl, FG, 2);
  seg(s, 5.72, 2.06, 6.95, 2.06, AC, 1.25);
  label(s, "WHAT YOU SAW TODAY", 7.05, 1.91, 2.30, { sz: 11, color: AC, align: "left" });
  seg(s, 3.05, 3.50, 4.05, 3.50, C.white, 1.25);
  label(s, "EVERYTHING ELSE", 0.75, 3.35, 2.20, { sz: 11, color: QUIET, align: "right" });
}

// ══ 9 ═ Two choices ═══════════════════════════════════ slides 304–312 ══════
{
  const s = slide("Graphic 9 — for slides 304-312: \"So I basically had 2 choices...\"");
  const cx = 5.0, base = 4.28, fork = 3.24, topY = 1.98;
  seg(s, cx, base, cx, fork, FG, 3);
  s.addShape("ellipse", { x: cx - 0.11, y: fork - 0.11, w: 0.22, h: 0.22, fill: { color: FG } });
  seg(s, cx, fork, 2.55, topY, QUIET, 3);
  seg(s, cx, fork, 7.45, topY, AC, 3);
  head(s, 2.44, topY - 0.08, 0.24, QUIET, "u");
  head(s, 7.56, topY - 0.08, 0.24, AC, "u");
  label(s, "OPTION 1", 1.44, topY - 0.98, 2.00, { sz: 14, color: QUIET });
  label(s, "on your own", 1.44, topY - 0.66, 2.00, { sz: 11, color: QUIET });
  label(s, "OPTION 2", 6.56, topY - 0.98, 2.00, { sz: 14, color: AC });
  label(s, "with me", 6.56, topY - 0.66, 2.00, { sz: 11, color: AC });
}

// ══ 10 ═ 10 spots ═════════════════════════════════════ slides 448–453 ══════
{
  const s = slide("Graphic 10 — for slides 448-453: only the first 10 people get the bonuses and the guarantee");
  big(s, "10", 0.90, 1.52, 8.20, 96, AC);
  label(s, "SPOTS", 0.90, 3.02, 8.20, { sz: 14, color: FG });
  const n = 10, gap = 0.52, x0 = 5.0 - (n - 1) * gap / 2;
  for (let i = 0; i < n; i++){
    s.addShape("roundRect", { x: x0 + i*gap - 0.17, y: 3.94, w: 0.34, h: 0.34,
      rectRadius: 0.09, fill: { color: AC } });
  }
}

// ══ 11 ═ You see A, you do B ═══════════════════════════ slides 43–46 ═══════
{
  const s = slide("Graphic 11 — for slides 43-46: \"You see A, you do B. You see B, you do A.\"");
  const rows = [["A", "B", 2.28], ["B", "A", 3.52]];
  rows.forEach(([from, to, y]) => {
    s.addShape("roundRect", { x: 3.15, y: y - 0.36, w: 0.86, h: 0.72, rectRadius: 0.12,
      fill: { type:"none" }, line: { color: RULE, width: 1.5 } });
    big(s, from, 3.15, y - 0.20, 0.86, 24, FG);
    seg(s, 4.22, y, 5.68, y, AC, 2.5);
    head(s, 5.80, y, 0.22, AC, "r");
    s.addShape("roundRect", { x: 5.99, y: y - 0.36, w: 0.86, h: 0.72, rectRadius: 0.12,
      fill: { color: AC } });
    big(s, to, 5.99, y - 0.20, 0.86, 24, C.white);
  });
  label(s, "YOU SEE", 2.00, 1.72, 2.00, { sz: 11, color: QUIET });
  label(s, "YOU DO",  6.00, 1.72, 2.00, { sz: 11, color: QUIET });
}

// ══ 12 ═ The desks are open ════════════════════════════ slides 53–55 ═══════
{
  const s = slide("Graphic 12 — for slides 53-55: the big players trade when their desks are open");
  const x0 = 1.30, x1 = 9.00, h = 0.42, axis = 4.10;
  const at = t => x0 + (x1 - x0) * t/24;
  const lane = (from, to, name, y) => {
    s.addShape("rect", { x: x0, y, w: x1 - x0, h, fill: { color: RULE } });
    s.addShape("rect", { x: at(from), y, w: at(to) - at(from), h, fill: { color: AC } });
    label(s, name, 0.10, y + h/2 - 0.15, 1.10, { sz: 11, color: AC, align: "right" });
  };
  lane(3, 11.5, "LONDON", 2.30);
  lane(8, 17, "NEW YORK", 3.06);
  seg(s, x0, axis, x1, axis, RULE, 1);
  [0, 6, 12, 18, 24].forEach(t => {
    seg(s, at(t), axis, at(t), axis + 0.13, QUIET, 1);
    label(s, `${String(t).padStart(2,"0")}:00`, at(t) - 0.50, axis + 0.17, 1.00,
      { sz: 10, color: QUIET });
  });
}

// ══ 13 ═ WHERE and WHEN ═══════════════════════════════ slides 112–114 ══════
{
  const s = slide("Graphic 13 — for slides 112-114: the dealing range tells you WHERE, the time based range tells you WHEN");
  seg(s, 5.0, 1.55, 5.0, 4.30, RULE, 1);
  label(s, "DEALING RANGE", 0.70, 1.72, 3.80, { sz: 11, color: QUIET });
  big(s, "WHERE", 0.70, 2.42, 3.80, 46, AC);
  label(s, "the orders are", 0.70, 3.56, 3.80, { sz: 13, color: FG });
  label(s, "TIME BASED RANGE", 5.50, 1.72, 3.80, { sz: 11, color: QUIET });
  big(s, "WHEN", 5.50, 2.42, 3.80, 46, AC);
  label(s, "it goes for them", 5.50, 3.56, 3.80, { sz: 13, color: FG });
}

// ══ 14 ═ It collects the orders first ════════════════════ slide 137 ════════
{
  const s = slide("Graphic 14 — for slide 137: before it can go anywhere it has to collect the orders on one side first");
  const y = 2.95;
  seg(s, 1.60, y, 8.40, y, FG, 2);
  label(s, "YOUR LEVEL", 8.55, y - 0.16, 1.30, { sz: 11, color: QUIET, align: "left" });
  for (let i = 0; i < 4; i++){
    const w = 1.70 - i*0.28;
    s.addShape("rect", { x: 4.30 - w/2, y: y + 0.20 + i*0.24, w, h: 0.10, fill: { color: QUIET } });
  }
  label(s, "ORDERS", 3.00, y + 1.30, 2.60, { sz: 11, color: QUIET });
  seg(s, 2.15, 1.62, 4.30, y + 1.06, AC, 3.5);
  seg(s, 4.30, y + 1.06, 6.75, 1.42, AC, 3.5);
  head(s, 6.86, 1.32, 0.26, AC, "u");
}

// ══ 15 ═ The entry matters least ══════════════════════ slides 209–216 ══════
{
  const s = slide("Graphic 15 — for slides 209-216: the entry is the part everyone obsesses over, and it matters least");
  const items = [["THE RANGE", 6.30, AC], ["THE BIAS", 6.30, AC],
                 ["THE EXIT", 6.30, AC], ["THE ENTRY", 1.35, QUIET]];
  items.forEach(([t, w, col], i) => {
    const y = 1.66 + i * 0.86;
    label(s, t, 0.80, y + 0.02, 2.00, { sz: 12, color: col, align: "right" });
    s.addShape("rect", { x: 3.00, y, w, h: 0.34, fill: { color: col } });
  });
  label(s, "how much it actually decides the trade", 0.80, 5.02, 8.40, { sz: 12, color: QUIET });
}

// ══ 16 ═ Two given away, the rest under NDA ═══════════ slides 296–302 ══════
{
  const s = slide("Graphic 16 — for slides 296-302: only 2 ranges can be given away, the rest are NDA-protected");
  const n = 6, w = 1.16, gap = 0.30, x0 = 5.0 - (n*w + (n-1)*gap)/2, y = 2.10, h = 1.42;
  for (let i = 0; i < n; i++){
    const x = x0 + i*(w + gap), open = i < 2;
    s.addShape("roundRect", { x, y, w, h, rectRadius: 0.10,
      fill: open ? { color: AC, transparency: 88 } : { type: "none" },
      line: { color: open ? AC : RULE, width: open ? 2 : 1.5 } });
    if (open) big(s, String(i + 1), x, y + h/2 - 0.28, w, 30, AC);
    else padlock(s, x + w/2, y + h/2, 1.15);
  }
  label(s, "YOURS TODAY", x0 - 0.20, y + h + 0.26, 2*w + gap + 0.40, { sz: 11, color: AC });
  label(s, "NDA", x0 + 2*(w + gap) - 0.20, y + h + 0.26, 4*w + 3*gap + 0.40,
    { sz: 11, color: QUIET });
}

// ══ 17 ═ The guarantee ════════════════════════════════ slides 426–431 ══════
{
  const s = slide("Graphic 17 — for slides 426-431: the guarantee. I keep working with you, personally, for free, until you're funded.");
  const cx = 5.0, cy = 2.90, r = 1.12;
  s.addShape("ellipse", { x: cx - r, y: cy - r, w: r*2, h: r*2,
    fill: { type:"none" }, line: { color: AC, width: 3 } });
  s.addShape("ellipse", { x: cx - r - 0.20, y: cy - r - 0.20, w: (r + 0.20)*2, h: (r + 0.20)*2,
    fill: { type:"none" }, line: { color: AC, width: 1 } });
  seg(s, cx - 0.46, cy + 0.03, cx - 0.10, cy + 0.38, AC, 5);
  seg(s, cx - 0.10, cy + 0.38, cx + 0.52, cy - 0.40, AC, 5);
  label(s, "UNTIL YOU'RE FUNDED", 2.50, cy + r + 0.50, 5.00, { sz: 13, color: FG });
}

// ══ 18 ═ How to apply ═════════════════════════════════ slides 457–461 ══════
{
  const s = slide("Graphic 18 — for slides 457-461: click the link, 2 minutes to fill out, then book a call");
  const steps = ["THE LINK", "2 MINUTES", "BOOK A CALL"];
  const y = 2.90, x0 = 1.55, dx = 3.45;
  seg(s, x0, y, x0 + 2*dx, y, RULE, 2);
  steps.forEach((t, i) => {
    const px = x0 + i*dx;
    s.addShape("ellipse", { x: px - 0.30, y: y - 0.30, w: 0.60, h: 0.60, fill: { color: AC } });
    s.addText(String(i + 1), T({ x: px - 0.30, y: y - 0.30, w: 0.60, h: 0.60,
      fontSize: 20, color: C.white, align: "center" }));
    label(s, t, px - 1.30, y + 0.52, 2.60, { sz: 14, color: FG });
  });

}

pres.writeFile({ fileName: process.env.OUT || "DTR_Graphics.pptx" })
  .then(() => console.log(`18 graphics — ${INV ? "dark" : "light"} frame`));
