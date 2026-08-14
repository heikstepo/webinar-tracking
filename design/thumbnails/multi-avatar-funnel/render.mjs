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
const page_url = 'file://' + path.join(here, 'index.html');
const outDir = path.join(here, 'render');
fs.mkdirSync(outDir, { recursive: true });

const W = 1280, H = 720;

const browser = await chromium.launch();
for (const scale of [1, 2]) {
  const ctx = await browser.newContext({
    viewport: { width: W, height: H },
    deviceScaleFactor: scale,
  });
  const page = await ctx.newPage();
  await page.goto(page_url, { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(350);
  const el = await page.locator('#board');
  const out = path.join(outDir, scale === 1 ? 'thumbnail-1280x720.png' : 'thumbnail-2560x1440.png');
  await el.screenshot({ path: out });
  console.log('wrote', out);
  await ctx.close();
}
await browser.close();
