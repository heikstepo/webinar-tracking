const {chromium}=require('playwright'); const fs=require('fs');
const V=JSON.parse(fs.readFileSync('verbatim.json','utf8'));
(async()=>{
  const b=await chromium.launch(); const p=await b.newPage();
  const set=new Set();
  for(const k of Object.keys(V)) for(const s of V[k]) if(s.trim()) set.add(s.trim());
  // also the derived fragments the builder makes (numeral splits, dash splits)
  for(const t of [...set]){
    const m=t.match(/^(\d+\s*[.\-)])\s*(.+)$/s); if(m){ set.add(m[1]); set.add(m[2]); }
    const d=t.match(/^(.*?)(\s*[—–]\s*)(.*)$/s); if(d){ set.add(d[1]+d[2]); set.add(d[3]); }
    for(const part of t.split(/(?<=[?.!…])\s+/)) if(part.trim()) set.add(part.trim());
  }
  const texts=[...set];
  const out=await p.evaluate((ts)=>{
    const c=document.createElement('canvas').getContext('2d');
    c.font='bold 100px Arial';
    const r={}; r.__space=c.measureText(' ').width/100;
    for(const t of ts) r[t]=t.split(/\s+/).map(w=>c.measureText(w).width/100);
    return r;
  }, texts);
  fs.writeFileSync('words.json',JSON.stringify(out));
  console.log('measured',texts.length,'strings; space em =',out.__space.toFixed(4));
  await b.close();
})();
