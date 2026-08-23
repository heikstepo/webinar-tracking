const { chromium } = require('playwright');
const fs = require('fs');
const P = JSON.parse(fs.readFileSync('plan2.json', 'utf8'));

const set = new Set();
const add = t => { if (t && t.trim()) set.add(t); };
for (const k of Object.keys(P.slides)) for (const t of P.slides[k].lines) {
  add(t);
  const m = t.match(/^((?:Q\d+\s*[-–—:])|(?:BONUS\s*\d+\s*:)|(?:\d+\s*[.)\-]))\s*(.+)$/s);
  if (m) { add(m[1]); add(m[2]); }
  const rest = m ? m[2] : t;
  const d = rest.match(/^(.*?)\s*([\u2014\u2013])\s*(.+)$/s);
  if (d) { add(d[1]); add(d[3]); add(d[2] + ' ' + d[3]); }
}
for (const b of Object.values(P.banners)) { add(b.full); add(b.head); add(b.tail); }

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  await page.setContent('<div style="font-family:Poppins;font-weight:700">probe</div>');
  await page.evaluate(() => document.fonts.ready);
  const texts = [...set];
  const out = await page.evaluate((ts) => {
    const c = document.createElement('canvas').getContext('2d');
    c.font = '700 100px Poppins';
    const r = { __space: c.measureText(' ').width / 100 };
    for (const t of ts) r[t] = t.split(/\s+/).filter(Boolean).map(w => c.measureText(w).width / 100);
    return r;
  }, texts);
  fs.writeFileSync('words.json', JSON.stringify(out));
  console.log('measured', texts.length, 'strings in Poppins Bold; space em =', out.__space.toFixed(4));
  await browser.close();
})();
