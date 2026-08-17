// Assemble the rendered slides into one 16:9 deck, one full-bleed image per slide.
const pptxgen = require('pptxgenjs');
const fs = require('fs');
const path = require('path');

const order = fs.readFileSync('deck-order.txt', 'utf8').trim().split('\n');
const pres = new pptxgen();

// Exact 16:9 so the 2880x1620 renders are not resampled to a different ratio.
pres.defineLayout({ name: 'SLIDE16x9', width: 13.333, height: 7.5 });
pres.layout = 'SLIDE16x9';

pres.author = 'SOL 20 Consulting';
pres.title = 'Five Pillars';

for (const name of order) {
  const file = path.join('exports', name + '.png');
  const slide = pres.addSlide();
  slide.addImage({ path: file, x: 0, y: 0, w: 13.333, h: 7.5 });
}

pres.writeFile({ fileName: 'exports/five-pillars.pptx' })
  .then(f => console.log('wrote', f, '—', order.length, 'slides'));
