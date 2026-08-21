// Diagram slides for Rauf. Dark ground so his red pen reads.
// Every element here is something he teaches on the channel — nothing invented.
const BG='0A0A0C', WH='FFFFFF', BL='2B6BFF', TL='3FD0C9', MU='8A8F98',
      UP='C9CDD3', DN='464C55', RULE='2A2E35';

function mk(pres){ const s=pres.addSlide(); s.background={color:BG}; return s; }

function head(s,t,sub){
  s.addText(t,{x:0.7,y:0.4,w:11.9,h:0.6,align:'center',valign:'middle',
    fontFace:'Arial',fontSize:30,bold:true,color:WH,charSpacing:1,margin:0});
  if(sub) s.addText(sub,{x:0.7,y:1.05,w:11.9,h:0.35,align:'center',valign:'middle',
    fontFace:'Arial',fontSize:13,color:MU,charSpacing:1,margin:0});
}
function lbl(s,t,x,y,w,o){o=o||{};
  s.addText(t,{x,y,w,h:o.h||0.3,align:o.align||'left',valign:'middle',fontFace:'Arial',
    fontSize:o.fs||12,bold:!!o.b,color:o.c||MU,charSpacing:o.cs===undefined?0.6:o.cs,margin:0});
}
function hline(pres,s,x,y,w,c,dash){
  s.addShape(pres.ShapeType.line,{x,y,w,h:0,line:{color:c,width:dash?1:1.75,dashType:dash||'solid'}});
}
function arrow(pres,s,x1,y1,x2,y2,c,w){
  s.addShape(pres.ShapeType.line,{
    x:Math.min(x1,x2), y:Math.min(y1,y2), w:Math.abs(x2-x1), h:Math.abs(y2-y1),
    flipH:x2<x1, flipV:y2<y1,
    line:{color:c,width:w||2.25,endArrowType:'triangle'}});
}
// one candle: wick from hi to lo, body between o and c
function candle(pres,s,x,hi,lo,o,c){
  const up=c<o, bw=0.16;
  s.addShape(pres.ShapeType.line,{x:x+bw/2,y:hi,w:0,h:lo-hi,line:{color:up?UP:DN,width:1}});
  s.addShape(pres.ShapeType.rect,{x,y:Math.min(o,c),w:bw,h:Math.max(0.06,Math.abs(c-o)),
    fill:{color:up?UP:DN},line:{color:up?UP:DN,width:1}});
}

const D = {};

// 1 — the range itself
D.range = (pres)=>{ const s=mk(pres);
  head(s,'THE TIME BASED RANGE','NEW YORK  ·  8:12 – 9:12 ET');
  const HI=2.85, LO=4.65, x0=1.6, x1=5.0;
  s.addShape(pres.ShapeType.rect,{x:x0,y:HI,w:x1-x0,h:LO-HI,fill:{color:BL,transparency:92},line:{color:BL,width:1.5}});
  hline(pres,s,x0,HI,10.8,BL); hline(pres,s,x0,LO,10.8,BL);
  const c=[[1.75,3.35,4.35,4.15,3.6],[2.35,3.1,4.5,3.6,4.2],[2.95,2.95,4.45,4.2,3.3],
           [3.55,3.2,4.65,3.3,4.4],[4.15,3.0,4.5,4.4,3.15],[4.6,2.85,3.9,3.15,3.5]];
  c.forEach(k=>candle(pres,s,k[0],k[1],k[2],k[3],k[4]));
  lbl(s,'HIGH OF THE RANGE',x1+0.35,HI-0.34,4,{c:BL,b:true,fs:12});
  lbl(s,'LOW OF THE RANGE',x1+0.35,LO+0.06,4,{c:BL,b:true,fs:12});
  lbl(s,'THAT HOUR',x0,LO+0.28,x1-x0,{align:'center',c:MU,fs:11});
  lbl(s,'TWO LINES. THAT’S YOUR RANGE.',1.6,6.35,10.8,{align:'center',c:WH,b:true,fs:14});
  return s;
};

// 2 — sweep one side, target the other  (+ where the liquidity sits)
D.sweep = (pres)=>{ const s=mk(pres);
  head(s,'SWEEP ONE SIDE  →  TARGET THE OTHER');
  const HI=2.95, LO=4.75, x0=1.6, x1=4.4;
  s.addShape(pres.ShapeType.rect,{x:x0,y:HI,w:x1-x0,h:LO-HI,fill:{color:BL,transparency:92},line:{color:BL,width:1.5}});
  hline(pres,s,x0,HI,10.6,BL); hline(pres,s,x0,LO,10.6,BL);
  [[1.8,3.3,4.4,4.2,3.6],[2.4,3.15,4.6,3.6,4.3],[3.0,3.05,4.55,4.3,3.4],[3.6,3.2,4.7,3.4,4.35],[4.1,3.0,4.5,4.35,3.3]]
    .forEach(k=>candle(pres,s,k[0],k[1],k[2],k[3],k[4]));
  lbl(s,'BUY SIDE LIQUIDITY',x0,HI-0.36,4,{c:TL,b:true,fs:12});
  lbl(s,'SELL SIDE LIQUIDITY',x0,LO+0.08,2.6,{c:TL,b:true,fs:12});
  // the sweep below the low, then the run to the opposing end
  [[4.9,3.6,5.0,3.7,4.8],[5.5,4.2,5.4,4.8,5.15],[6.1,4.7,5.2,5.15,4.9]].forEach(k=>candle(pres,s,k[0],k[1],k[2],k[3],k[4]));
  lbl(s,'1   THE LOW GETS TAKEN',4.5,5.55,3.2,{align:'center',c:TL,b:true,fs:12});
  arrow(pres,s,6.6,4.95,10.85,3.0,WH,2.5);
  lbl(s,'2   TARGET THE OPPOSING END',8.2,2.42,4.1,{align:'right',c:WH,b:true,fs:12});
  lbl(s,'SWEEP ONE SIDE. TRADE TO THE OTHER SIDE.',1.6,6.45,10.6,{align:'center',c:WH,b:true,fs:14});
  return s;
};

// 3 — why price takes the low before it goes up
D.liquidity = (pres)=>{ const s=mk(pres);
  head(s,'WHY PRICE TAKES THE LOW  BEFORE  IT GOES UP');
  const LO=3.5;
  hline(pres,s,1.6,LO,9.4,BL);
  lbl(s,'LOW OF THE RANGE',11.15,LO-0.15,1.9,{c:BL,b:true,fs:11});
  // resting stops below
  for(let i=0;i<9;i++){ hline(pres,s,2.4+i*0.62,LO+0.42+(i%3)*0.16,0.38,MU); }
  lbl(s,'STOPS + BREAKDOWN SELLERS RESTING UNDER THE LOW',2.35,LO+1.05,6.5,{c:MU,fs:12});
  arrow(pres,s,2.0,LO-0.55,2.9,LO+0.55,MU,2);
  lbl(s,'PRICE DIPS IN',1.0,LO-0.85,2.2,{c:MU,b:true,fs:11});
  lbl(s,'ALL THE SELL ORDERS TRIGGER AT ONCE',3.2,LO+1.75,6.5,{c:TL,b:true,fs:13});
  lbl(s,'THAT’S WHAT THE BIG BUY ORDERS GET PAIRED WITH',3.2,LO+2.08,6.8,{c:MU,fs:12});
  arrow(pres,s,9.6,LO+0.9,11.3,1.95,WH,3);
  lbl(s,'THEN IT CAN TRADE\nTO THE BUY SIDE',9.9,1.35,3.1,{c:WH,b:true,fs:12,h:0.55});
  lbl(s,'“FOR EVERY BUYER THERE HAS TO BE A SELLER.”',1.6,6.5,10.6,{align:'center',c:WH,b:true,fs:14});
  return s;
};

// 4 — dealing range, equilibrium, premium / discount
D.dealing = (pres)=>{ const s=mk(pres);
  head(s,'THE DEALING RANGE');
  const HI=2.2, LO=5.6, EQ=(HI+LO)/2, x0=2.2, W=7.2;
  s.addShape(pres.ShapeType.rect,{x:x0,y:HI,w:W,h:EQ-HI,fill:{color:BL,transparency:94},line:{type:'none'}});
  s.addShape(pres.ShapeType.rect,{x:x0,y:EQ,w:W,h:LO-EQ,fill:{color:TL,transparency:94},line:{type:'none'}});
  hline(pres,s,x0,HI,W,BL); hline(pres,s,x0,LO,W,BL); hline(pres,s,x0,EQ,W,MU,'dash');
  lbl(s,'HIGH THAT PUSHED PRICE DOWN',x0+W+0.3,HI-0.15,3.4,{c:BL,b:true,fs:11});
  lbl(s,'EQUILIBRIUM',x0+W+0.3,EQ-0.15,3.4,{c:MU,b:true,fs:11});
  lbl(s,'LOW THAT PUSHED PRICE UP',x0+W+0.3,LO-0.15,3.4,{c:BL,b:true,fs:11});
  lbl(s,'PREMIUM',x0+0.25,HI+0.2,2,{c:WH,b:true,fs:13});
  lbl(s,'DISCOUNT',x0+0.25,LO-0.5,2,{c:WH,b:true,fs:13});
  // the TBR sitting inside, in the discount
  s.addShape(pres.ShapeType.rect,{x:4.7,y:4.28,w:1.9,h:0.8,fill:{color:BG},line:{color:WH,width:1.5}});
  lbl(s,'TIME BASED RANGE',4.55,5.16,2.2,{align:'center',c:WH,b:true,fs:10});
  lbl(s,'“WE WANT TO SEE OUR TIME BASED RANGE ACTUALLY FORM WITHIN THIS.”',1.6,6.45,10.6,{align:'center',c:WH,b:true,fs:14});
  lbl(s,'AND NEVER TRADE THE MIDPOINT.',1.6,6.78,10.6,{align:'center',c:MU,fs:12});
  return s;
};

// 5 — the three triggers on one axis
D.triggers = (pres)=>{ const s=mk(pres);
  head(s,'THE 3 WAYS IN','THE ONLY DECISION IS WHERE YOU SIT ON THIS LINE');
  const Y=4.35, x0=1.9, x1=11.4;
  hline(pres,s,x0,Y,x1-x0,RULE);
  const pts=[[x0+0.6,'1','INVERSE FAIR\nVALUE GAP',BL],
             [(x0+x1)/2,'2','ORDER BLOCK MADE\nIN LIQUIDITY',WH],
             [x1-0.6,'3','THREE CANDLE\nROTATION',TL]];
  pts.forEach(p=>{
    s.addShape(pres.ShapeType.ellipse,{x:p[0]-0.16,y:Y-0.16,w:0.32,h:0.32,fill:{color:p[3]},line:{color:p[3],width:1}});
    s.addText(p[1],{x:p[0]-0.6,y:Y-0.95,w:1.2,h:0.4,align:'center',valign:'middle',
      fontFace:'Arial',fontSize:20,bold:true,color:p[3],margin:0});
    s.addText(p[2],{x:p[0]-1.5,y:Y+0.3,w:3.0,h:0.8,align:'center',valign:'top',
      fontFace:'Arial',fontSize:13,bold:true,color:WH,charSpacing:0.6,margin:0});
  });
  arrow(pres,s,x0,5.75,x1,5.75,MU,1.5);
  lbl(s,'EARLIEST',x0,5.95,3,{c:MU,b:true,fs:12});
  lbl(s,'LATEST',x1-3,5.95,3,{align:'right',c:MU,b:true,fs:12});
  lbl(s,'BEST PRICE',x0,6.25,3,{c:MU,fs:12});
  lbl(s,'MOST CERTAIN',x1-3,6.25,3,{align:'right',c:MU,fs:12});
  lbl(s,'THERE’S NO PERFECT ONE. THERE’S THE RIGHT ONE FOR THE DAY.',1.6,6.8,10.6,{align:'center',c:WH,b:true,fs:14});
  return s;
};

// 6 — which red candle is actually the order block
D.orderblock = (pres)=>{ const s=mk(pres);
  head(s,'THE ORDER BLOCK MADE IN LIQUIDITY','ONLY ONE OF THESE RED CANDLES COUNTS');
  const LO=4.35;
  hline(pres,s,1.9,LO,9.5,BL);
  lbl(s,'LOW OF THE RANGE',9.8,LO-0.36,1.6,{align:'right',c:BL,b:true,fs:11});
  // leg down: four down-close candles, only the last trades below the low
  const c=[[3.3,2.35,3.25,2.5,3.1],[4.3,2.75,3.7,2.95,3.55],[5.3,3.2,4.2,3.4,4.05],[6.3,3.75,5.1,3.95,4.75]];
  c.forEach(k=>candle(pres,s,k[0],k[1],k[2],k[3],k[4]));
  // the reversal candle
  candle(pres,s,7.3,3.5,4.9,4.75,3.7);
  ['NOT THIS ONE','NOT THIS ONE','NOT THIS ONE'].forEach((t,i)=>
    lbl(s,t,c[i][0]-0.77,c[i][1]-0.36,1.7,{align:'center',c:MU,fs:10}));
  s.addShape(pres.ShapeType.rect,{x:6.1,y:3.6,w:0.56,h:1.6,fill:{type:'none'},line:{color:TL,width:2}});
  lbl(s,'THIS ONE',6.38-0.9,5.32,1.8,{align:'center',c:TL,b:true,fs:13});
  lbl(s,'IT’S THE CANDLE THAT TRADED\nINTO THE LIQUIDITY BELOW THE RANGE',8.1,4.6,4.4,{c:WH,b:true,fs:12,h:0.6});
  arrow(pres,s,7.55,3.55,7.75,2.6,WH,2);
  lbl(s,'CLOSE BACK ABOVE IT\n= THAT’S WHERE I CAN TRUST BUYING',7.95,2.25,4.5,{c:WH,b:true,fs:12,h:0.6});
  lbl(s,'ANY OTHER RED CANDLE ON THAT CHART IS JUST A RED CANDLE.',1.9,6.6,9.5,{align:'center',c:MU,fs:13});
  return s;
};

// 7 — the graded price swing
D.graded = (pres)=>{ const s=mk(pres);
  head(s,'THE GRADED PRICE SWING','WHAT HAPPENS WHILE YOU’RE HOLDING');
  const x0=2.6, W=6.2, top=2.05, bot=6.05, span=bot-top;
  const y = p => bot - (p/100)*span;
  s.addShape(pres.ShapeType.rect,{x:x0,y:y(75),w:W,h:y(50)-y(75),fill:{color:TL,transparency:88},line:{type:'none'}});
  [[100,'SWING HIGH',WH,''],[75,'EXTENDED — FULL TAKE PROFIT\nNEVER A NEW POSITION UP HERE',BL,''],
   [50,'MOVE TO BREAK EVEN',BL,''],[25,'CONFIRMATION\nTHE MARKET’S SHIFTING',BL,''],
   [0,'SWING LOW',WH,'']].forEach(r=>{
    hline(pres,s,x0,y(r[0]),W,r[2],r[0]===100||r[0]===0?'solid':'dash');
    lbl(s,String(r[0]),x0-0.85,y(r[0])-0.15,0.65,{align:'right',c:r[2],b:true,fs:14});
    lbl(s,r[1],x0+W+0.35,y(r[0])-0.2,3.9,{c:r[2]===WH?WH:MU,b:r[2]!==WH,fs:11,h:0.42});
  });
  lbl(s,'PROFIT ZONE',x0+0.3,(y(75)+y(50))/2-0.15,2.4,{c:WH,b:true,fs:14});
  lbl(s,'OR JUST TAKE 50 POINTS ON THE NASDAQ AND YOU’RE DONE.',1.6,6.5,10.6,{align:'center',c:WH,b:true,fs:14});
  return s;
};

module.exports = D;
