// Rebuild the Sol Twenty DWY deck as native, editable PowerPoint.
//
//   node build-dwy.js
//
// Every string is a real text run and every card a real shape, so the deck can
// be edited in PowerPoint without coming back here. The client's own images
// are carried over from the source deck at their original positions, scaled
// from its 20x11.25in canvas to a 13.333x7.5in one.
//
// The accent is the brand's purple rather than this system's blue: the logo
// on every slide is purple, and an off-brand accent beside it reads as a
// mistake. Everything else — the ground, the type, the restraint — is the
// house style.

const pptxgen = require('pptxgenjs');
const path = require('path');

const MEDIA = '/tmp/claude-0/-home-user-webinar-tracking/f1e7ca79-b012-51af-8534-656fa835e5b8/scratchpad/dwy/ppt/media';
const img = n => path.join(MEDIA, n);

/* The source deck is 20in wide; this one is 13.333in. */
const S = 13.333 / 20;
const s = v => +(v * S).toFixed(3);

const W = 13.333, H = 7.5;
const PAD = 0.9;
const COL = W - PAD * 2;

const INK = '1D1D1F';
const INK2 = '6E6E73';
const INK3 = '86868B';
const LINE = 'D2D2D7';
const GROUND = 'F5F5F7';
const CARD = 'FFFFFF';
const ACCENT = '9904FF';

const FONT = 'Helvetica Neue';

const pres = new pptxgen();
pres.defineLayout({ name: 'SLIDE16x9', width: W, height: H });
pres.layout = 'SLIDE16x9';
pres.author = 'SOL 20 Consulting';
pres.title = 'Sol Twenty DWY';

/* The wordmark sits in the same place on every slide but the first, which
   carries its own mark in the corner. */
const LOGO = { x: s(9.14), y: 0.42, w: s(1.72), h: s(0.87) };

function slide({ logo = true } = {}) {
  const sl = pres.addSlide();
  sl.background = { color: GROUND };
  if (logo) sl.addImage({ path: img('image2.png'), ...LOGO });
  return sl;
}

/* A line of type centred across the content column. */
function line(sl, text, opts) {
  sl.addText(text, {
    x: PAD, w: COL, align: 'center', margin: 0, fit: 'none',
    fontFace: FONT, color: INK, ...opts
  });
}

/* ---------------------------------------------------------------- 1. hook */
{
  const sl = slide({ logo: false });
  line(sl, 'Get 1on1 consulting with me to scale your high-ticket offer to $100k/mo...', {
    y: 2.45, h: 1.5, fontSize: 40, bold: true, charSpacing: -0.6, lineSpacing: 48
  });
  line(sl, [
    { text: 'ROI positive or you don’t pay', options: { color: ACCENT, bold: true } },
    { text: '   +   ', options: { color: INK3 } },
    { text: 'Cancel anytime', options: { color: ACCENT, bold: true } }
  ], { y: 4.2, h: 0.6, fontSize: 27, charSpacing: -0.3 });
  sl.addImage({ path: img('image1.png'), x: s(0.2), y: s(10.37), w: s(1.34), h: s(0.67) });
}

/* ------------------------------------------------- 2 + 17. two guarantees */
function guarantees() {
  const sl = slide();
  line(sl, '2 Guarantees. Both in writing.', {
    y: 1.86, h: 0.72, fontSize: 38, bold: true, charSpacing: -0.5
  });

  /* Sized for the longer of the two titles wrapping to a second line, so the
     rule below it never lands in the middle of the words. */
  const padT = 0.36, numH = 0.28, titleH = 0.72, ruleGap = 0.12, bodyGap = 0.18, bodyH = 0.7, padB = 0.32;
  const ch = padT + numH + titleH + ruleGap + bodyGap + bodyH + padB;
  const gap = 0.34, cw = (COL - gap) / 2, cy = 3.02;

  const cards = [
    ['Guarantee 1', '30-Day ROI Guarantee', 'You’re in profit within 30 days. Or you get a full refund.'],
    ['Guarantee 2', '7-Day Alignment Guarantee', '7 days to see the work and make sure we’re a fit. Don’t like it? Full refund.']
  ];
  cards.forEach(([num, name, body], i) => {
    const x = PAD + i * (cw + gap);
    sl.addShape(pres.ShapeType.roundRect, {
      x, y: cy, w: cw, h: ch, rectRadius: 0.18, fill: { color: CARD }, line: { color: CARD },
      shadow: { type: 'outer', blur: 14, offset: 3, angle: 90, color: '9AA3AE', opacity: 0.22 }
    });
    const px = x + 0.46, pw = cw - 0.92;
    sl.addText(num, { x: px, y: cy + padT, w: pw, h: numH, margin: 0, fit: 'none', fontFace: FONT, fontSize: 14, bold: true, color: ACCENT });
    sl.addText(name, { x: px, y: cy + padT + numH, w: pw, h: titleH, margin: 0, fit: 'none', valign: 'top', fontFace: FONT, fontSize: 23, bold: true, color: INK, charSpacing: -0.4, lineSpacing: 29 });
    sl.addShape(pres.ShapeType.line, { x: px, y: cy + padT + numH + titleH + ruleGap, w: pw, h: 0, line: { color: 'DCDCE1', width: 1 } });
    sl.addText(body, { x: px, y: cy + padT + numH + titleH + ruleGap + bodyGap, w: pw, h: bodyH, margin: 0, fit: 'none', fontFace: FONT, fontSize: 17, color: INK2, lineSpacing: 24 });
  });

  if (cy + ch > H - 0.6) throw new Error('guarantee cards overrun the slide: ' + (cy + ch));
}
guarantees();

/* ------------------------------------------------------- 3 + 4. each one */
function guaranteeDetail(num, title, lead, tail) {
  const sl = slide();
  line(sl, num, { y: 1.95, h: 0.35, fontSize: 17, bold: true, color: ACCENT });
  line(sl, title, { y: 2.45, h: 0.8, fontSize: 44, bold: true, charSpacing: -0.8 });
  line(sl, lead, { y: 3.75, h: 0.9, fontSize: 22, bold: true, color: INK, lineSpacing: 32 });
  line(sl, tail, { y: 4.75, h: 0.5, fontSize: 22, color: INK2, lineSpacing: 32 });
}
guaranteeDetail('Guarantee #1', 'Monthly ROI Guarantee.',
  'Every month, if you haven’t made back more than you’ve paid me, I refund every dollar you’ve paid.',
  'You get a full refund, no questions asked.');
guaranteeDetail('Guarantee #2', '7-Day Alignment Guarantee.',
  'If you don’t like our work within the first 7 days...',
  'You get a full same-day refund, no questions asked.');

/* --------------------------------------------------------- 5. zero downside */
{
  const sl = slide();
  line(sl, 'Your Downside is...', { y: 2.5, h: 0.55, fontSize: 24, color: INK2 });
  line(sl, 'Zero.', { y: 3.15, h: 1.6, fontSize: 84, bold: true, color: ACCENT, charSpacing: -2 });
}

/* ------------------------------------------------------------- 6. wordmark */
{
  const sl = slide({ logo: false });
  sl.addImage({ path: img('image2.png'), x: s(5.89), y: s(3.55), w: s(8.22), h: s(4.15) });
}

/* ------------------------------------------------- 7. the results montage */
{
  const sl = slide();
  line(sl, 'Multiple 7-figures in client Revenue.', {
    y: 1.32, h: 0.8, fontSize: 44, bold: true, charSpacing: -0.8
  });
  sl.addImage({ path: img('image3.png'), x: s(4.88), y: s(3.62), w: s(10.23), h: s(7.22) });
  sl.addImage({ path: img('image4.png'), x: s(7.54), y: s(3.4), w: s(5.01), h: s(4.5) });
}

/* --------------------------------------------------------- 8..15. results */
function result({ pics, big, cap, bigY, capY }) {
  const sl = slide();
  pics.forEach(p => sl.addImage({ path: img(p.f), x: s(p.x), y: s(p.y), w: s(p.w), h: s(p.h) }));
  line(sl, big, { y: bigY, h: 0.8, fontSize: 44, bold: true, charSpacing: -0.8 });
  if (cap) {
    line(sl, cap[0], { y: capY, h: 0.45, fontSize: 21, bold: true, color: INK, lineSpacing: 30 });
    line(sl, cap[1], { y: capY + 0.5, h: 0.45, fontSize: 21, color: INK2, lineSpacing: 30 });
  }
}

result({
  pics: [{ f: 'image6.png', x: 2.77, y: 1.62, w: 6.96, h: 3.52 },
         { f: 'image7.jpeg', x: 10.44, y: 1.62, w: 6.26, h: 3.52 }],
  big: '$15k/mo to $160k/mo', bigY: 3.9,
  cap: ['We hit $100k/mo within 3 months of working together.',
        'Now we’ve made 100s of thousands of dollars.'], capY: 5.05
});

result({
  pics: [{ f: 'image8.png', x: 6.09, y: 1.61, w: 7.82, h: 3.12 }],
  big: '$3k/mo to $300k+', bigY: 3.7,
  cap: ['We launched his high-ticket offer from 0 & scaled to $300k+.',
        'He was making less than $3k/mo with his low ticket offer before.'], capY: 4.85
});

result({ pics: [{ f: 'image9.png', x: 6.08, y: 3.04, w: 7.83, h: 3.16 }],
  big: '$0 to $50k/mo in 2 weeks', bigY: 4.75 });
result({ pics: [{ f: 'image10.png', x: 6.08, y: 2.7, w: 7.85, h: 3.83 }],
  big: '$200k+ in Revenue', bigY: 4.75 });
result({ pics: [{ f: 'image11.png', x: 2.85, y: 3.05, w: 14.31, h: 2.94 }],
  big: '$50k+ in new Revenue', bigY: 4.75 });
result({ pics: [{ f: 'image12.png', x: 5.87, y: 2.59, w: 8.25, h: 4.41 }],
  big: '7 figures+ in Revenue for his offers', bigY: 5.05 });
result({ pics: [{ f: 'image13.png', x: 6.27, y: 3.07, w: 7.46, h: 3.15 }],
  big: '10s of Thousands in Revenue', bigY: 4.75 });
result({ pics: [{ f: 'image14.png', x: 6.3, y: 3.39, w: 7.39, h: 2.81 }],
  big: 'Multiple 6-figures in extra Revenue', bigY: 4.75 });

/* ----------------------------------------------- 16. the programme, in four */
{
  const sl = slide();
  /* Clear of the wordmark, which runs to y=1.0. */
  line(sl, 'What happens after you join', {
    y: 1.3, h: 0.66, fontSize: 36, bold: true, charSpacing: -0.5
  });

  const buckets = [
    ['Within 48 hours', 'Onboarding call',
     ['Offer', 'Funnel', 'Ads', 'Organic', 'Backend', 'Sales performance']],
    ['Every week', '1-on-1 call',
     ['Paid ads', 'Organic content', 'Webinar funnels', 'Call funnels']],
    ['24/7', 'DM access',
     ['Anything that comes up', 'An extra call mid-week']],
    ['Alongside', 'Course library',
     ['SOPs and trainings', 'Being built out now']]
  ];

  /* The card is sized from its contents rather than guessed at: the longest
     list sets the height, and every card takes that height. Guessing is what
     pushed the sixth item out of the first card last time. */
  const LEAD = 19, GAP = 5;                       // list leading and paragraph gap, pt
  const maxItems = Math.max(...buckets.map(b => b[2].length));
  const listH = (maxItems * LEAD + (maxItems - 1) * GAP) / 72;

  const padT = 0.32, whenH = 0.26, titleH = 0.44, ruleGap = 0.16, listGap = 0.2, padB = 0.32;
  const listTop = padT + whenH + titleH + ruleGap + listGap;
  const ch = listTop + listH + padB;

  const gap = 0.26, cw = (COL - gap * 3) / 4;
  const cy = 2.72;
  const dotD = 0.36, dotY = cy - 0.46 - dotD / 2;

  /* One rail through all four markers: the four are a sequence, and without
     the rail they read as four unrelated boxes. */
  const first = PAD + cw / 2, last = PAD + 3 * (cw + gap) + cw / 2;
  sl.addShape(pres.ShapeType.line, {
    x: first, y: dotY + dotD / 2, w: last - first, h: 0, line: { color: 'C9C9CE', width: 1.5 }
  });

  buckets.forEach(([when, what, items], i) => {
    const x = PAD + i * (cw + gap);
    const cx = x + cw / 2;

    sl.addShape(pres.ShapeType.ellipse, {
      x: cx - dotD / 2, y: dotY, w: dotD, h: dotD,
      fill: { color: ACCENT }, line: { color: ACCENT }
    });
    sl.addText(String(i + 1), {
      x: cx - dotD / 2, y: dotY, w: dotD, h: dotD, margin: 0, fit: 'none',
      align: 'center', valign: 'middle', fontFace: FONT, fontSize: 13, bold: true, color: 'FFFFFF'
    });

    sl.addShape(pres.ShapeType.roundRect, {
      x, y: cy, w: cw, h: ch, rectRadius: 0.16, fill: { color: CARD }, line: { color: CARD },
      shadow: { type: 'outer', blur: 14, offset: 3, angle: 90, color: '9AA3AE', opacity: 0.22 }
    });

    const px = x + 0.28, pw = cw - 0.56;
    sl.addText(when, { x: px, y: cy + padT, w: pw, h: whenH, margin: 0, fit: 'none', fontFace: FONT, fontSize: 13, bold: true, color: ACCENT });
    sl.addText(what, { x: px, y: cy + padT + whenH, w: pw, h: titleH, margin: 0, fit: 'none', valign: 'top', fontFace: FONT, fontSize: 19, bold: true, color: INK, charSpacing: -0.3 });
    sl.addShape(pres.ShapeType.line, { x: px, y: cy + padT + whenH + titleH + ruleGap, w: pw, h: 0, line: { color: 'DCDCE1', width: 1 } });
    sl.addText(items.map((t, j) => ({
      text: t, options: { bullet: { characterCode: '2022', indent: 11 }, breakLine: j < items.length - 1 }
    })), { x: px, y: cy + listTop, w: pw, h: listH + 0.1, margin: 0, fit: 'none', valign: 'top',
      fontFace: FONT, fontSize: 13, color: INK2, lineSpacing: LEAD, paraSpaceAfter: GAP });
  });

  if (cy + ch > H - 0.6) throw new Error('programme cards overrun the slide: ' + (cy + ch));
}

/* ------------------------------------------------------ 17. guarantees again */
guarantees();

/* ------------------------------------------------------------ 18. next steps */
{
  const sl = slide();
  line(sl, 'Next Steps...', { y: 2.5, h: 0.5, fontSize: 24, color: INK2 });
  line(sl, [
    { text: 'Reply. Call. ', options: { color: INK } },
    { text: 'Launch.', options: { color: ACCENT } }
  ], { y: 3.2, h: 1.2, fontSize: 62, bold: true, charSpacing: -1.4 });
}

const out = 'exports/sol-twenty-dwy.pptx';
pres.writeFile({ fileName: out }).then(f => console.log('wrote', f));
