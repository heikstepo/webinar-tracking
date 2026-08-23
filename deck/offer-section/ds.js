// Design system — extracted from the reference deck, blue accent.
const C = { ink:"0A0A0A", accent:"2E7BF6", muted:"9A9A9A", sub:"545454",
            hair:"C9C9C9", paper:"FFFFFF", darkRule:"2E2E2E", white:"FFFFFF" };
const FONT = "Arial";                 // single family, single weight
const RAIL = 0.90, RIGHT = 9.10, CW = RIGHT - RAIL;
const TIERS = [15,17,19,22,25,28,32,36,40,46];
const CHARW = 0.0072;                 // in per pt of font size

const T = (o={}) => Object.assign({ fontFace:FONT, bold:true, margin:0, isTextBox:true,
  lineSpacing:undefined, valign:"middle", color:C.ink }, o);

// real greedy word-wrap using Arial Bold advances measured in the browser
const WORDS = require("./words.json");
const SPACE = WORDS.__space;
function nlines(text, size, width){
  const w = WORDS[text];
  if (!w) {                                     // fallback: character estimate
    const cpl = Math.max(8, Math.floor(width / (CHARW*size)));
    return Math.max(1, Math.ceil(text.length / cpl));
  }
  const maxEm = width * 72 / size;              // available width in em
  let lines = 1, cur = 0;
  for (const ww of w){
    if (cur === 0) { cur = ww; continue; }
    const next = cur + SPACE + ww;
    if (next > maxEm) { lines++; cur = ww; } else cur = next;
  }
  return lines;
}
// measured width of a short string, in inches
function textW(text, size){
  const w = WORDS[text];
  if (!w) return text.length * CHARW * size;
  return (w.reduce((a,b)=>a+b,0) + SPACE*(w.length-1)) * size / 72;
}
function blockH(lines, size, width){
  return lines.reduce((h,l)=> h + nlines(l,size,width)*size*1.22/72, 0);
}

// ---- accent span picking -------------------------------------------------
const PATS = [
  /\$[\d,]+(?:\.\d+)?/,                        // money
  /\d{1,2}:\d{2}\s*-\s*\d{1,2}:\d{2}/,         // time range
  /\d{1,2}:\d{2}/,                             // clock
  /[“"][^”"]{1,40}[”"]/,                      // quoted phrase (never apostrophes)
  /\b\d+\s*(?:figures?|candles?|trades?|lines?|levels?|boxes|minutes|years?|months?|weeks?|days?|things|questions|sides?|steps?|times a week)\b/i,
  /\b\d+\s*(?:to|-|–)\s*\d+\b/,
  /\b\d+\b/,
];
// trading vocabulary — the phrases worth marking when nothing numeric is present
const LEX = [
  /\bTime Based Ranges?\b/i, /\bdealing range\b/i, /\border block\b/i,
  /\binverse gap\b/i, /\bdouble break\b/i, /\bliquidity\b/i,
  /\bswing (?:high|low)\b/i, /\bbreak even\b/i, /\btake profit\b/i,
  /\b3 candle rotation\b/i, /\bthe reversal\b/i, /\bPnL\b/, /\bTBR\b/,
];
const BRACKET = /\[[^\]]*\]/g;
function pickAccent(text, override, pats){
  if (override === null) return null;
  if (override) { const i = text.indexOf(override); return i<0 ? null : [i, i+override.length]; }
  // never mark a [PLACEHOLDER] — blank those out before matching
  const masked = text.replace(BRACKET, m => "\u0000".repeat(m.length));
  for (const p of (pats||PATS)){
    const m = masked.match(p);
    // a span covering most of the line isn't emphasis, it's just the line
    if (m && m[0].length / text.length <= 0.7) return [m.index, m.index+m[0].length];
  }
  return null;
}
function runs(text, size, color, override, pats){
  const a = pickAccent(text, override, pats);
  if (!a) return [{ text, options:{ fontSize:size, color } }];
  const out=[];
  if (a[0]>0) out.push({text:text.slice(0,a[0]), options:{fontSize:size, color}});
  out.push({text:text.slice(a[0],a[1]), options:{fontSize:size, color:C.accent}});
  if (a[1]<text.length) out.push({text:text.slice(a[1]), options:{fontSize:size, color}});
  return out;
}

// ---- chrome --------------------------------------------------------------
function chapterBanner(s, head, sep, tail, dark){
  const label = `${head}${sep} ${tail}`;
  const approx = label.length * 0.0072 * 11.7;          // measured width
  const half = Math.max(0.55, Math.min(1.45, (7.19 - approx)/2 - 0.30));
  const lx = 5.0 - approx/2 - 0.30 - half, rx = 5.0 + approx/2 + 0.30;
  s.addShape("line", { x:lx, y:0.26, w:half, h:0, line:{ color:C.accent, width:0.9 } });
  s.addShape("line", { x:rx, y:0.26, w:half, h:0, line:{ color:C.accent, width:0.9 } });
  s.addShape("ellipse", { x:lx-0.025, y:0.235, w:0.05, h:0.05, fill:{ color:C.accent } });
  s.addShape("ellipse", { x:rx+half-0.025, y:0.235, w:0.05, h:0.05, fill:{ color:C.accent } });
  s.addText([
    { text:head, options:{ color:C.accent } },
    { text:sep,  options:{ color:C.hair } },
    { text:" "+tail, options:{ color: dark?C.white:C.ink } },
  ], T({ x:1.40, y:0.06, w:7.19, h:0.40, fontSize:11.7, align:"center" }));
}
function accentDot(s){
  s.addShape("ellipse", { x:0.60, y:0.62, w:0.10, h:0.10, fill:{ color:C.accent } });
}
function eyebrow(s, text, dark){
  s.addShape("ellipse", { x:0.60, y:0.62, w:0.10, h:0.10, fill:{ color:C.accent } });
  s.addText(text, T({ x:0.82, y:0.50, w:8.50, h:0.34, fontSize:11,
                      color: dark?C.white:C.ink }));
}
module.exports = { C, FONT, LEX, PATS, textW, RAIL, RIGHT, CW, TIERS, T, nlines, blockH, runs, pickAccent,
                   chapterBanner, eyebrow, accentDot };
