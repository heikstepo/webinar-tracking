const pptxgen = require('pptxgenjs');
const fs = require('fs');
const D = require('./diagrams.js');

const base = JSON.parse(fs.readFileSync('slides.json','utf8'));

// diagram slides go immediately AFTER the line named here (i.e. right before a SHOW LIVE)
const INSERT = [
  ['2. Mark the high and the low of that hour', 'range'],
  ['4. Target the opposing end', 'sweep'],
  ['The market takes the sell side first.\n\nThen it can trade to the buy side.', 'liquidity'],
  ['3. My range formed inside a dealing range', 'dealing'],
  ['Earlier → better entry, less confirmation\nLater → more certainty, worse price', 'triggers'],
  ['But the only ones that count are the ones made in liquidity.', 'orderblock'],
  ["So here's what happens while you're holding. 4 things, in order:", 'graded'],
];

const slides = [];
let placed = 0;
base.forEach(s => {
  slides.push(s);
  const hit = INSERT.find(p => p[0] === s.t);
  if (hit) { slides.push({k:'d', d:hit[1]}); placed++; }
});
if (placed !== INSERT.length) { console.error('MISSED an anchor — placed', placed, 'of', INSERT.length); process.exit(1); }

const pres = new pptxgen();
pres.layout = 'LAYOUT_WIDE';
pres.author = 'Day Trading Rauf';
pres.title  = 'TBR Live Class - Content Section';

const INK='111111', PAPER='FFFFFF', DARK='111111', GREY='EFEFEF', MUTE='666666';
const size = t => { const n=t.length;
  return n<45?40 : n<90?32 : n<160?26 : n<260?22 : 18; };

slides.forEach((s,i) => {
  let sl;
  if (s.k === 'd') {
    sl = D[s.d](pres);
  } else if (s.k === 's') {
    sl = pres.addSlide(); sl.background = {color:DARK};
    sl.addText(s.t,{x:0.8,y:1.0,w:11.7,h:5.5,align:'center',valign:'middle',
      fontFace:'Arial',fontSize:44,bold:true,color:PAPER,margin:0});
  } else if (s.k === 'l') {
    sl = pres.addSlide(); sl.background = {color:GREY};
    sl.addText(s.t,{x:0.8,y:1.0,w:11.7,h:5.5,align:'center',valign:'middle',
      fontFace:'Courier New',fontSize:20,color:MUTE,margin:0,lineSpacingMultiple:1.3});
  } else {
    sl = pres.addSlide(); sl.background = {color:PAPER};
    sl.addText(s.t,{x:0.8,y:1.0,w:11.7,h:5.5,align:'center',valign:'middle',
      fontFace:'Arial',fontSize:size(s.t),bold:s.k==='c',color:INK,margin:0,lineSpacingMultiple:1.25});
  }
  const onDark = (s.k==='s'||s.k==='d');
  sl.addText(String(i+1),{x:12.3,y:6.9,w:0.6,h:0.3,align:'right',
    fontFace:'Arial',fontSize:9,color:onDark?'555555':'BBBBBB',margin:0});
});

pres.writeFile({fileName:'TBR-Content-Section.pptx'})
  .then(f=>console.log('wrote',f,'-',slides.length,'slides,',placed,'diagrams'));
