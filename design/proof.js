/* Render a proof of the *pptx* layout, not the source slides.
 *
 *   node proof.js && ./render.sh proof.html
 *
 * LibreOffice cannot open a pptx in this sandbox, so the deck cannot be
 * checked by converting it. This rebuilds the same boxes in HTML using the
 * same numbers build-deck.js writes — and in Arial, whose metrics PowerPoint
 * will actually use — so the one thing that genuinely differs from the PNG
 * deck can be seen: where a wider face makes a line wrap that did not wrap in
 * Inter. Positions here come from the same measured.json, so if the proof
 * looks right the pptx is laid out right.
 */

const fs = require('fs');
const path = require('path');

const DIR = __dirname;
const measured = JSON.parse(fs.readFileSync(path.join(DIR, 'exports/measured.json'), 'utf8'));
const order = fs.readFileSync(path.join(DIR, 'deck-order.txt'), 'utf8').trim().split('\n');

const SPACE_EM = 0.278;
const esc = s => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
const weight = w => (w >= 600 ? 700 : 400);

const typeCss = t => `font-size:${t.size}px;font-weight:${weight(t.weight)};` +
  `letter-spacing:${t.tracking}px;line-height:${t.lineHeight}px;color:${t.color}`;

function boxCss(m, x, w) {
  return `left:${x}px;top:${m.y}px;width:${w}px`;
}

function numbered(num, label, gapPx) {
  const extra = gapPx - SPACE_EM * num.type.size;
  return `<span style="color:${num.type.color}">${esc(num.text)}</span>` +
    `<span style="letter-spacing:${extra}px"> </span>` +
    `<span style="color:${label.type.color}">${esc(label.text)}</span>`;
}

const pages = order.map(name => {
  const m = measured[name];
  const parts = [];

  if (m.eyebrow) {
    parts.push(`<div class="box" style="${boxCss(m.eyebrow, 100, 1240)};${typeCss(m.eyebrow.type)};text-align:center">${esc(m.eyebrow.text)}</div>`);
  }
  if (m.h1) {
    parts.push(`<div class="box" style="${boxCss(m.h1, 100, 1240)};${typeCss(m.h1.type)};text-align:center">${esc(m.h1.text)}</div>`);
  }
  if (m.head) {
    const gap = m.head.label.x - (m.head.num.x + m.head.num.w);
    const align = m.head.type.align === 'center' ? 'center' : 'left';
    parts.push(`<div class="box" style="${boxCss(m.head, 100, 1240)};${typeCss(m.head.type)};text-align:${align}">${numbered(m.head.num, m.head.label, gap)}</div>`);
  }

  if (m.list) {
    const items = m.list.items;
    const gapAfter = items.length > 1 ? items[1].y - (items[0].y + items[0].h) : 0;
    const lis = items.map((item, i) => {
      const last = i === items.length - 1;
      const style = `${typeCss(item.type)};margin-bottom:${last ? 0 : gapAfter}px`;
      if (item.numbered) {
        const gap = item.label.x - (item.num.x + item.num.w);
        return `<li class="plain" style="${style}">${numbered(item.num, item.label, gap)}</li>`;
      }
      const indent = item.x + 52 - m.list.x;
      return `<li style="${style};padding-left:${indent}px;text-indent:-${indent}px">` +
        `<span class="bul" style="width:${indent}px">&#8226;</span>${esc(item.text)}</li>`;
    }).join('\n');
    parts.push(`<ul class="box list" style="left:${m.list.x}px;top:${m.list.y}px;width:${m.list.w}px">\n${lis}\n</ul>`);
  }

  return `<section class="slide">\n${parts.join('\n')}\n</section>`;
}).join('\n\n');

const html = `<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>five-pillars pptx proof</title>
<style>
  * { box-sizing: border-box; }
  html, body { margin: 0; padding: 0; }
  .slide {
    position: relative;
    width: 1440px; height: 810px;
    margin: 0 auto;
    overflow: hidden;
    background: #F5F5F7;
    /* Arial is what PowerPoint substitutes for Helvetica Neue off macOS, and
       what this sandbox metric-matches with Liberation Sans. */
    font-family: Arial, 'Liberation Sans', sans-serif;
    page-break-after: always;
  }
  .box { position: absolute; margin: 0; }
  .list { list-style: none; padding: 0; }
  .list li { margin: 0; }
  .bul { display: inline-block; color: #0071E3; text-indent: 0; }
  @page { size: 1440px 810px; margin: 0; }
</style>
</head>
<body>

${pages}

</body>
</html>
`;

fs.writeFileSync(path.join(DIR, 'proof.html'), html);
console.log(`wrote proof.html — ${order.length} slides, Arial metrics`);
