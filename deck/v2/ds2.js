// Design system v2 -- modelled on the AA live-class deck.
// Teal accent, Poppins Bold, one weight, size as the only hierarchy, lots of air.
const C = { ink:"0A0A0A", accent:"12977F", muted:"9A9A9A", sub:"545454",
            hair:"C9C9C9", paper:"FFFFFF", darkRule:"2E2E2E", white:"FFFFFF" };
const FONT = "Poppins";
const RAIL = 0.90, RIGHT = 9.10, CW = RIGHT - RAIL;
const TIERS = [15,17,19,22,25,28,32,36,40,46,52];
const CHARW = 0.0079;                       // Poppins Bold fallback estimate

const WORDS = require("./words.json");
const SPACE = WORDS.__space;

const T = (o={}) => Object.assign({ fontFace:FONT, bold:true, margin:0,
  isTextBox:true, valign:"middle", color:C.ink }, o);

function nlines(text, size, width){
  const w = WORDS[text];
  if (!w){ const cpl = Math.max(6, Math.floor(width/(CHARW*size)));
           return Math.max(1, Math.ceil(text.length/cpl)); }
  const maxEm = width*72/size;
  let lines = 1, cur = 0;
  for (const ww of w){
    if (cur === 0){ cur = ww; continue; }
    const nx = cur + SPACE + ww;
    if (nx > maxEm){ lines++; cur = ww; } else cur = nx;
  }
  return lines;
}
function textW(text, size){
  const w = WORDS[text];
  if (!w) return text.length*CHARW*size;
  return (w.reduce((a,b)=>a+b,0) + SPACE*(w.length-1))*size/72;
}

// ---- choosing the one thing on the line that carries the colour ------------
const BRACKET = /\[[^\]]*\]/g;
const HARD = [                                   // concrete, always wins
  /\$[\d,]+(?:\.\d+)?/,
  /\d{1,2}:\d{2}\s*[-–]\s*\d{1,2}:\d{2}/,
  /\d{1,2}:\d{2}/,
  /\b\d+\s*(?:figures?|candles?|trades?|lines?|levels?|boxes|mornings?|minutes?|hours?|weeks?|months?|years?|days?|spots?|people|questions|sides?|steps?|bonuses)\b/i,
  /\b\d+\s*(?:to|-|–)\s*\d+\b/,
  /[“"][^”"]{1,34}[”"]/,
];
const LEX = [                                    // the vocabulary of this deck
  /\btime based ranges?\b/i, /\bdealing range\b/i, /\border block\b/i,
  /\binverse gap\b/i, /\bdouble break\b/i, /\bliquidity\b/i, /\bswing (?:high|low)\b/i,
  /\bbreak even\b/i, /\btake profit\b/i, /\b3 candle rotation\b/i, /\bthe reversal\b/i,
  /\bconsistently profitable\b/i, /\bfunded trader\b/i, /\bprop firm\b/i,
  /\bguarantee\b/i, /\bmentorship\b/i, /\bTBR\b/, /\bPnL\b/, /\bNDA\b/,
  /\bfor free\b/i, /\bunlimited\b/i, /\b1on1\b/i, /\bfunded\b/i, /\bbias\b/i,
];
const STOP = new Set(("a an the and or but so if then that this these those it its is are was were be been being am " +
  "i you we they he she me my your our their them us to of in on at for with from by as into about over under " +
  "not no nor just only even still also more most much very really actually literally basically genuinely " +
  "do does did done doing have has had having can could will would should may might must " +
  "what when where which who whom why how all any some each every other another there here now " +
  "up down out off again once because before after while until than too s t re ve ll d m " +
  "get got go going come came make made take took see saw know knew think thought want wanted " +
  "like right left thing things way ways day days one two").split(/\s+/));
const POWER = new Set(("profitable funded guarantee free never always exactly everything nothing personally " +
  "unlimited consistently predict prediction reversal liquidity mentorship bootcamp intensive " +
  "risk money profit profits loss losses stop entry exit range ranges bias market markets " +
  "private secure protected proven verified live challenge scaling coaching community blueprint " +
  "commentaries onboarding course workbooks foundations framework structure confirmation " +
  "wrong broken stuck scared enormous unreasonable selective immediately tomorrow " +
  "morning mornings week weeks minute minutes second seconds " +
  "buy sell buyer seller yes win wins green filled sweep swept break candle candles " +
  "chart charts box boxes target direction gap order orders funded prop spots limit " +
  "access calls dms data proof results students witness").split(/\s+/));

function pickAccent(text, override, pats){
  if (override === null) return null;
  if (override){ const i = text.indexOf(override); return i<0 ? null : [i, i+override.length]; }
  const masked = text.replace(BRACKET, m => " ".repeat(m.length));
  for (const p of (pats || HARD.concat(LEX))){
    const m = masked.match(p);
    if (m && (text.length <= 26 || m[0].length/text.length <= 0.7))
      return [m.index, m.index+m[0].length];
  }
  if (pats) return null;
  return keyword(text);
}
// last resort: the strongest single word on the line
function keyword(text){
  const re = /[A-Za-z][A-Za-z-]*/g;              // no contractions
  let m, best = null;
  while ((m = re.exec(text)) !== null){
    const w = m[0], lw = w.toLowerCase();
    if (STOP.has(lw) || lw.length < 3) continue;
    if (text[m.index + w.length] === "'" || text[m.index + w.length] === "\u2019") continue;
    let s = lw.length;
    if (POWER.has(lw)) s += 16;
    if (/^[A-Z]/.test(w) && m.index > 0) s += 3;         // proper noun mid-line
    if (/[A-Z]{2,}/.test(w)) s += 7;                     // shouted word
    s += (m.index / text.length) * 3;                    // later words land harder
    if (!best || s > best.s) best = { s, a:m.index, b:m.index+w.length };
  }
  if (!best) return null;
  // pull in the next word only when it is itself strong, so it reads as a phrase
  const after = text.slice(best.b).match(/^ ([A-Za-z][A-Za-z-]*)(?![\u2019'])/);
  if (after && POWER.has(after[1].toLowerCase())) best.b += after[0].length;
  return [best.a, best.b];
}
function runs(text, size, color, override, pats){
  const a = pickAccent(text, override, pats);
  if (!a) return [{ text, options:{ fontSize:size, color } }];
  const out = [];
  if (a[0] > 0) out.push({ text:text.slice(0,a[0]), options:{ fontSize:size, color } });
  out.push({ text:text.slice(a[0],a[1]), options:{ fontSize:size, color:C.accent } });
  if (a[1] < text.length) out.push({ text:text.slice(a[1]), options:{ fontSize:size, color } });
  return out;
}

// ---- chrome ---------------------------------------------------------------
function chapterBanner(s, head, sep, tail, dark){
  const label = head + sep + " " + tail;
  const approx = textW(label, 11.7) || label.length*0.0079*11.7;
  const half = Math.max(0.55, Math.min(1.45, (7.19-approx)/2 - 0.30));
  const lx = 5.0 - approx/2 - 0.30 - half, rx = 5.0 + approx/2 + 0.30;
  s.addShape("line", { x:lx, y:0.26, w:half, h:0, line:{ color:C.accent, width:0.9 } });
  s.addShape("line", { x:rx, y:0.26, w:half, h:0, line:{ color:C.accent, width:0.9 } });
  s.addShape("ellipse", { x:lx-0.025, y:0.235, w:0.05, h:0.05, fill:{ color:C.accent } });
  s.addShape("ellipse", { x:rx+half-0.025, y:0.235, w:0.05, h:0.05, fill:{ color:C.accent } });
  s.addText([{ text:head, options:{ color:C.accent } },
             { text:sep,  options:{ color:C.hair } },
             { text:" "+tail, options:{ color: dark?C.white:C.ink } }],
    T({ x:1.40, y:0.06, w:7.19, h:0.40, fontSize:11.7, align:"center" }));
}
const accentDot = s => s.addShape("ellipse",
  { x:0.60, y:0.62, w:0.10, h:0.10, fill:{ color:C.accent } });
function eyebrow(s, text, dark){
  accentDot(s);
  s.addText(text, T({ x:0.82, y:0.50, w:8.50, h:0.34, fontSize:11,
                      color: dark?C.white:C.ink }));
}
module.exports = { C, FONT, RAIL, RIGHT, CW, TIERS, T, nlines, textW, runs,
                   pickAccent, keyword, chapterBanner, eyebrow, accentDot, LEX };
