/* Build five-pillars.pptx with live, editable PowerPoint text.
 *
 *   ./measure.sh && node build-deck.js
 *
 * Geometry comes from exports/measured.json — Chrome's own layout of the
 * slide HTML — so a box lands where the browser put it instead of where a
 * hand-recomputed box model guessed. Every string on every slide ships as a
 * real text run, so the deck can be edited in PowerPoint or Google Slides.
 *
 * build-deck-images.js still exists and builds the same slides as full-bleed
 * PNGs, which is pixel-exact but not editable.
 */

const fs = require('fs');
const path = require('path');
const pptxgen = require('pptxgenjs');

const DIR = __dirname;
const measured = JSON.parse(fs.readFileSync(path.join(DIR, 'exports/measured.json'), 'utf8'));
const order = fs.readFileSync(path.join(DIR, 'deck-order.txt'), 'utf8').trim().split('\n');

/* The slide canvas is 1440x810 CSS px shown at 13.333x7.5in, so one CSS pixel
   is a fixed fraction of an inch and exactly two-thirds of a point. */
const IN = 13.333 / 1440;
const PT = 2 / 3;
const inches = px => px * IN;
const points = px => px * PT;

/* PowerPoint has no weight axis — only bold on or off. The design runs 600 for
   anything that leads and 500 for anything that follows, so that split becomes
   the bold split. */
const isBold = weight => weight >= 600;

/* Every mainstream grotesque sets the word space at 0.278em, which is what
   lets a gap the CSS drew with `flex-gap` be rebuilt out of one space plus
   letter-spacing. */
const SPACE_EM = 0.278;

const FONT = 'Helvetica Neue';

const hex = css => {
  const [r, g, b] = css.match(/\d+/g).map(Number);
  return [r, g, b].map(n => n.toString(16).padStart(2, '0').toUpperCase()).join('');
};

/* Shared text-box options. `margin: 0` strips PowerPoint's built-in inset so
   the box's left edge is the text's left edge, matching the measured x.
   `fit: 'none'` stops PowerPoint from rescaling type to fill the box. */
const boxOpts = (m, extra = {}) => ({
  x: inches(m.x),
  y: inches(m.y),
  w: inches(m.w),
  h: inches(m.h),
  margin: 0,
  valign: 'top',
  fit: 'none',
  wrap: true,
  lineSpacing: points(m.type.lineHeight),
  fontFace: FONT,
  fontSize: points(m.type.size),
  bold: isBold(m.type.weight),
  color: hex(m.type.color),
  charSpacing: points(m.type.tracking),
  ...extra
});

/* A number and its label are one flex row in CSS with an exact gap. Rebuilt as
   two runs around a single space that is stretched to that gap, so the pair
   stays one editable line and still centres as a unit. */
const numberedRuns = (num, label, gapPx) => {
  const spacePx = SPACE_EM * num.type.size;
  return [
    {
      text: num.text,
      options: { color: hex(num.type.color), bold: isBold(num.type.weight) }
    },
    {
      text: ' ',
      options: { charSpacing: points(gapPx - spacePx) }
    },
    {
      text: label.text,
      options: { color: hex(label.type.color), bold: isBold(label.type.weight) }
    }
  ];
};

const pres = new pptxgen();
pres.defineLayout({ name: 'SLIDE16x9', width: 13.333, height: 7.5 });
pres.layout = 'SLIDE16x9';
pres.author = 'SOL 20 Consulting';
pres.title = 'Five Pillars';

for (const name of order) {
  const m = measured[name];
  if (!m) throw new Error(`${name}: not in measured.json — re-run ./measure.sh`);

  const slide = pres.addSlide();
  slide.background = { color: hex(m.background) };

  /* Section title slides: the pillar number over the pillar name, both
     centred. Measured widths come from Inter, so these run the full content
     width and let PowerPoint centre in whatever font it has. */
  if (m.eyebrow) {
    slide.addText(m.eyebrow.text, boxOpts(
      { ...m.eyebrow, x: 100, w: 1240 },
      { align: 'center' }
    ));
  }
  if (m.h1) {
    slide.addText(m.h1.text, boxOpts(
      { ...m.h1, x: 100, w: 1240 },
      { align: 'center' }
    ));
  }

  /* The running head: "2.1  Meta Ads". Centred on overview slides, hard left
     everywhere else. */
  if (m.head) {
    const gap = m.head.label.x - (m.head.num.x + m.head.num.w);
    const centred = m.head.type.align === 'center';
    slide.addText(numberedRuns(m.head.num, m.head.label, gap), boxOpts(
      { ...m.head, x: 100, w: 1240 },
      { align: centred ? 'center' : 'left' }
    ));
  }

  /* The build list. One box holding every item as its own paragraph, rather
     than a box per item, so that editing a line reflows the ones under it and
     a wrapped line pushes rather than overlaps. */
  if (m.list) {
    const items = m.list.items;
    const first = items[0];
    const gapAfter = items.length > 1
      ? items[1].y - (first.y + first.h)
      : 0;

    const body = items.map((item, i) => {
      const common = {
        fontFace: FONT,
        fontSize: points(item.type.size),
        color: hex(item.type.color),
        bold: isBold(item.type.weight),
        charSpacing: points(item.type.tracking),
        lineSpacing: points(item.type.lineHeight),
        paraSpaceAfter: i === items.length - 1 ? 0 : points(gapAfter),
        breakLine: true
      };

      if (item.numbered) {
        const gap = item.label.x - (item.num.x + item.num.w);
        /* The section number stands in for the bullet on overview lists. */
        return numberedRuns(item.num, item.label, gap).map((run, j) => ({
          text: run.text,
          options: {
            ...common,
            ...run.options,
            bullet: false,
            breakLine: j === 2
          }
        }));
      }

      /* A real PowerPoint bullet, hung at the measured text indent. Its colour
         is patched in afterwards — pptxgenjs writes no <a:buClr>. */
      return [{
        text: item.text,
        options: { ...common, bullet: { characterCode: '2022', indent: points(item.x + 52 - m.list.x) } }
      }];
    }).flat();

    slide.addText(body, {
      x: inches(m.list.x),
      y: inches(m.list.y),
      w: inches(m.list.w),
      h: inches(810 - m.list.y - 64),
      margin: 0,
      valign: 'top',
      fit: 'none',
      wrap: true
    });
  }
}

const out = path.join(DIR, 'exports/five-pillars.pptx');
pres.writeFile({ fileName: out }).then(() => {
  console.log(`wrote ${path.relative(DIR, out)} — ${order.length} slides, native text`);
});
