#!/usr/bin/env node
/* Assemble the numbered 16:9 slides into a PowerPoint deck.
 *
 * Every slide is one full-bleed image. The slides are already typeset by the
 * HTML pipeline, so there is nothing for PowerPoint to lay out and nothing it
 * can reflow: what ships is exactly what was rendered, on any machine, with no
 * font to install. The slug goes in the speaker notes so a slide can still be
 * traced back to the file that made it.
 *
 *   node build-deck.js       ->  exports/vsl-deck.pptx
 */
const fs = require('fs');
const path = require('path');
const pptxgen = require('pptxgenjs');

const DIR = path.join(__dirname, 'exports', 'run-wide');
const OUT = path.join(__dirname, 'exports', 'vsl-deck.pptx');

if (!fs.existsSync(DIR)) {
  console.error('no ' + DIR + ' — run ./number-run.py first');
  process.exit(1);
}

// Numeric sort, not lexical: without it 10 lands between 1 and 2.
const files = fs.readdirSync(DIR)
  .filter(f => f.endsWith('.png'))
  .sort((a, b) => parseInt(a, 10) - parseInt(b, 10));

if (!files.length) {
  console.error('no slides in ' + DIR);
  process.exit(1);
}

const pres = new pptxgen();
pres.layout = 'LAYOUT_16x9';          // 10 x 5.625in — set before any slide
pres.title = 'VSL slides';

files.forEach(f => {
  const slide = pres.addSlide();
  slide.background = { color: 'F2F3F5' };   // matches the slide ground
  slide.addImage({ path: path.join(DIR, f), x: 0, y: 0, w: 10, h: 5.625 });
  slide.addNotes(f.replace(/\.png$/, ''));
});

pres.writeFile({ fileName: OUT }).then(() => {
  const mb = (fs.statSync(OUT).size / 1e6).toFixed(1);
  console.log('wrote ' + path.relative(__dirname, OUT) +
              '  (' + files.length + ' slides, ' + mb + ' MB)');
});
