// Renders index.html to PNG at 1x and 2x (YouTube thumbnail: 1280x720).
// Usage: node render.mjs
import { fileURLToPath, pathToFileURL } from 'node:url';
import { execSync } from 'node:child_process';
import path from 'node:path';
import fs from 'node:fs';

// Resolve playwright from the project, or fall back to a global install.
async function loadPlaywright() {
  try {
    return await import('playwright');
  } catch {
    const globalRoot = execSync('npm root -g', { encoding: 'utf8' }).trim();
    const entry = path.join(globalRoot, 'playwright', 'index.mjs');
    return await import(pathToFileURL(entry).href);
  }
}
const { chromium } = await loadPlaywright();

const here = path.dirname(fileURLToPath(import.meta.url));
const srcFile = process.argv[2] || 'index.html';
const prefix  = process.argv[3] || 'thumbnail';
const page_url = 'file://' + path.join(here, srcFile);
const outDir = path.join(here, 'render');
fs.mkdirSync(outDir, { recursive: true });

const W = 1280, H = 720;

// 3x lands exactly on 3840x2160 (4K UHD); 4x is 5120x2880 for print/crops.
const SCALES = [1, 2, 3, 4];

const browser = await chromium.launch();
for (const scale of SCALES) {
  const ctx = await browser.newContext({
    viewport: { width: W, height: H },
    deviceScaleFactor: scale,
  });
  const page = await ctx.newPage();
  await page.goto(page_url, { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(350);
  const el = await page.locator('#board');
  const out = path.join(outDir, `${prefix}-${W * scale}x${H * scale}.png`);
  // 4x with layered drop-shadow filters blows past Playwright's 30s default
  await el.screenshot({ path: out, timeout: 180000 });
  console.log('wrote', out);
  await ctx.close();
}
await browser.close();
