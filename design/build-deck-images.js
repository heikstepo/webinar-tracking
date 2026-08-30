// Assemble rendered slides into one 16:9 deck, one full-bleed image per slide.
//
//   node build-deck-images.js [order-file] [out.pptx] [title]
//
// Pixel-exact but not editable. build-deck.js is the native-text alternative,
// and only handles the slide shapes it knows how to rebuild — anything with
// diagrams or icons has to come through here.
const pptxgen = require('pptxgenjs');
const fs = require('fs');
const path = require('path');

const orderFile = process.argv[2] || 'deck-order.txt';
const outFile = process.argv[3] || 'exports/five-pillars.pptx';
const title = process.argv[4] || 'Five Pillars';

const order = fs.readFileSync(orderFile, 'utf8').trim().split('\n').filter(Boolean);
const pres = new pptxgen();

// Exact 16:9 so the 2880x1620 renders are not resampled to a different ratio.
pres.defineLayout({ name: 'SLIDE16x9', width: 13.333, height: 7.5 });
pres.layout = 'SLIDE16x9';

pres.author = 'SOL 20 Consulting';
pres.title = title;

for (const name of order) {
  const file = path.join('exports', name + '.png');
  if (!fs.existsSync(file)) throw new Error(`${file} not rendered — run ./render.sh slides/${name}.html`);
  const slide = pres.addSlide();
  slide.addImage({ path: file, x: 0, y: 0, w: 13.333, h: 7.5 });
}

pres.writeFile({ fileName: outFile })
  .then(f => console.log('wrote', f, '—', order.length, 'slides'));
