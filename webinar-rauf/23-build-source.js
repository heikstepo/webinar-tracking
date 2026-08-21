const pptxgen = require('pptxgenjs');
const slides = JSON.parse(require('fs').readFileSync('slides.json','utf8'));

const pres = new pptxgen();
pres.layout = 'LAYOUT_WIDE';                 // 13.3 x 7.5
pres.author = 'Day Trading Rauf';
pres.title  = 'DTR Content Section - internal';

const INK='111111', PAPER='FFFFFF', DARK='111111', MUTE='777777', LIVEBG='FFF4D6';
const BODY = 36;          // one size for every content slide
const SECTION = 44;       // section dividers only

slides.forEach((sl,i)=>{
  const s = pres.addSlide();

  if (sl.k === 's'){
    s.background = { color: DARK };
    s.addText(sl.t,{x:0.7,y:1.0,w:11.9,h:5.5,align:'center',valign:'middle',
      fontFace:'Arial',fontSize:SECTION,bold:true,color:PAPER,margin:0,lineSpacingMultiple:1.25});

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
      fontFace:'Arial',fontSize:BODY,bold:true,color:INK,margin:0,lineSpacingMultiple:1.35});
  }

  s.addText(String(i+1),{x:12.3,y:6.95,w:0.6,h:0.3,align:'right',
    fontFace:'Arial',fontSize:9,color: sl.k==='s' ? '555555' : 'BBBBBB',margin:0});
});

pres.writeFile({fileName:'DTR-Content-Section-internal.pptx'})
  .then(f=>console.log('wrote',f,'-',slides.length,'slides @',BODY,'pt'));
