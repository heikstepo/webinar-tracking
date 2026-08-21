const pptxgen = require('pptxgenjs');
const slides = JSON.parse(require('fs').readFileSync('slides.json','utf8'));

const pres = new pptxgen();
pres.layout = 'LAYOUT_WIDE';                 // 13.3 x 7.5
pres.author = 'Day Trading Rauf';
pres.title  = 'DTR Content Section - internal';

const INK='111111', PAPER='FFFFFF', DARK='111111', MUTE='777777', LIVEBG='FFF4D6';

function size(t){
  // pick the largest size where the longest hand-broken line still fits the box
  const lines = t.split('\n');
  const maxlen = Math.max(...lines.map(l=>l.length));
  const BOX = 11.9 * 72;                 // points
  let fs = Math.floor(BOX / (maxlen * 0.52));
  fs = Math.min(fs, 44);
  // and keep tall slides from running off the bottom
  const maxByHeight = Math.floor((5.7 * 72) / (lines.length * 1.3));
  fs = Math.min(fs, maxByHeight);
  return Math.max(18, fs);
}

slides.forEach((sl,i)=>{
  const s = pres.addSlide();
  const n = i+1;

  if (sl.k === 's'){
    s.background = { color: DARK };
    s.addText(sl.t,{x:0.7,y:1.0,w:11.9,h:5.5,align:'center',valign:'middle',
      fontFace:'Arial',fontSize:46,bold:true,color:PAPER,margin:0,lineSpacingMultiple:1.2});

  } else if (sl.k === 'l'){
    s.background = { color: LIVEBG };
    s.addText('SHOW LIVE',{x:0.7,y:0.5,w:11.9,h:0.9,align:'center',valign:'middle',
      fontFace:'Arial',fontSize:40,bold:true,color:INK,charSpacing:2,margin:0});
    s.addText(sl.d,{x:1.4,y:1.45,w:10.5,h:0.6,align:'center',valign:'top',
      fontFace:'Arial',fontSize:12,italic:true,color:MUTE,margin:0,lineSpacingMultiple:1.2});
    s.addText(sl.s,{x:1.4,y:2.2,w:10.5,h:4.6,align:'left',valign:'top',
      fontFace:'Arial',fontSize:11,color:'555555',margin:0,lineSpacingMultiple:1.35});

  } else {
    s.background = { color: PAPER };
    s.addText(sl.t,{x:0.7,y:0.9,w:11.9,h:5.7,align:'center',valign:'middle',
      fontFace:'Arial',fontSize:size(sl.t),bold:true,color:INK,margin:0,lineSpacingMultiple:1.3});
  }

  s.addText(String(n),{x:12.3,y:6.95,w:0.6,h:0.3,align:'right',
    fontFace:'Arial',fontSize:9,color: sl.k==='s' ? '555555' : 'BBBBBB',margin:0});
});

pres.writeFile({fileName:'DTR-Content-Section-internal.pptx'})
  .then(f=>console.log('wrote',f,'-',slides.length,'slides'));
