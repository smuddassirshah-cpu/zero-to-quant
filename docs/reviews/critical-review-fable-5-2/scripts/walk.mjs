// Reviewer click-through as a fresh learner: setup, Today, Learn, Prepare, Review, a mock start card, bank, drill, You.
// Usage: PW=$(npm root -g)/playwright/index.mjs node walk.mjs <outdir>   (app served on :8080)
const { chromium } = await import(process.env.PW || 'playwright');
import fs from 'node:fs';
const out = process.argv[2]; fs.mkdirSync(out, { recursive: true });
const b = await chromium.launch();
const log = [];
for (const [w, h, sfx] of [[1280, 860, ''], [440, 956, '-440']]) {
  const ctx = await b.newContext({ viewport: { width: w, height: h }, deviceScaleFactor: 1 });
  const p = await ctx.newPage();
  p.on('console', (m) => { if (m.type() === 'error') log.push(`${sfx} console: ${m.text().slice(0, 200)}`); });
  const shot = async (n) => { await p.waitForTimeout(900); await p.screenshot({ path: `${out}/${n}${sfx}.png`, fullPage: true }); };
  await p.goto('http://localhost:8080/'); await shot('00-first-load');
  log.push(`${sfx} first url ${p.url()}`);
  await p.waitForSelector('[data-name]'); await p.fill('[data-name]', 'Sam'); await shot('01-setup-1'); await p.click('[data-next]');
  await p.waitForTimeout(400); await p.click('[data-track="Trader"]'); await shot('01-setup-2'); await p.click('[data-next]');
  await p.waitForTimeout(400); await p.click('[data-h="15"]'); await p.click('[data-stage="0"]'); await shot('01-setup-3'); await p.click('[data-next]');
  await p.waitForTimeout(800);
  log.push(`${sfx} after setup ${p.url()} state ${await p.evaluate(() => JSON.stringify((JSON.parse(localStorage['zq.state'] || '{}').profile) || {}))}`);
  for (const r of ['today', 'learn', 'prepare', 'review', 'you', 'course/number-sense', 'course/puzzles', 'exam/mock-superday-trader', 'exam/mock-oa-arith', 'exam/topic-1.5', 'exam/stage-0', 'bank', 'drill', 'drill/oa-rain-water', 'homework/conditional/homework-2', 'exam/mock-video']) {
    await p.goto('http://localhost:8080/#' + r); await p.waitForTimeout(700);
    await shot('10-' + r.replace(/\W+/g, '_'));
    log.push(`${sfx} ${r}: ${(await p.locator('#app').innerText()).replace(/\s+/g, ' ').slice(0, 700)}`);
  }
  await ctx.close();
}
await b.close();
fs.writeFileSync(`${out}/walk-log.txt`, log.join('\n\n'));
