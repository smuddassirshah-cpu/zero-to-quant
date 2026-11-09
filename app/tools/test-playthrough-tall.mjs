// Test for the playthrough's full-height marked shot (ENGINE-BACKLOG 703). Run from app/: node tools/test-playthrough-tall.mjs [--local-cdn <pkgs>]
// Plays a temporary copy of app/ whose ito/homework-2 is tools/fixtures/overflow/homework-2-tall.json (one longform whose model is
// several viewports tall) with --shots, desktop and --mobile. The -marked PNG must be taller than two viewports and its last rows must not be blank.
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import zlib from 'node:zlib';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
const HERE = path.dirname(fileURLToPath(import.meta.url)), APP = path.resolve(HERE, '..');
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'zq-tall-'));
const copy = path.join(tmp, 'app');
fs.cpSync(APP, copy, { recursive: true });
fs.copyFileSync(path.join(HERE, 'fixtures/overflow/homework-2-tall.json'), path.join(copy, 'content/courses/ito/homework-2.json'));
/* minimal PNG decoder (8-bit, non-interlaced, RGB or RGBA): returns { w, h, row(y) } */
function decode(buf) {
  let p = 8, w = 0, h = 0, ch = 3; const idat = [];
  while (p < buf.length) {
    const n = buf.readUInt32BE(p), t = buf.toString('latin1', p + 4, p + 8), d = buf.subarray(p + 8, p + 8 + n);
    if (t === 'IHDR') { w = d.readUInt32BE(0); h = d.readUInt32BE(4); ch = d[9] === 6 ? 4 : 3; if (d[8] !== 8 || d[12] !== 0 || (d[9] !== 2 && d[9] !== 6)) throw new Error('unsupported PNG'); }
    if (t === 'IDAT') idat.push(d);
    p += 12 + n;
  }
  const raw = zlib.inflateSync(Buffer.concat(idat)), stride = w * ch, out = Buffer.alloc(h * stride);
  for (let y = 0; y < h; y++) {
    const f = raw[y * (stride + 1)], src = raw.subarray(y * (stride + 1) + 1, (y + 1) * (stride + 1));
    for (let x = 0; x < stride; x++) {
      const a = x >= ch ? out[y * stride + x - ch] : 0, b = y ? out[(y - 1) * stride + x] : 0, c = x >= ch && y ? out[(y - 1) * stride + x - ch] : 0;
      let v = src[x];
      if (f === 1) v += a; else if (f === 2) v += b; else if (f === 3) v += (a + b) >> 1;
      else if (f === 4) { const pp = a + b - c, pa = Math.abs(pp - a), pb = Math.abs(pp - b), pc = Math.abs(pp - c); v += pa <= pb && pa <= pc ? a : pb <= pc ? b : c; }
      out[y * stride + x] = v & 255;
    }
  }
  return { w, h, ch, blank: (y0, y1) => { for (let y = y0; y < y1; y++) for (let x = 0; x < w; x++) for (let c = 0; c < 3; c++) if (out[y * stride + x * ch + c] < 250) return false; return true; } };
}
const extra = process.argv.slice(2);
let bad = 0;
for (const mobile of [false, true]) {
  const shots = path.join(tmp, 'shots-' + (mobile ? 'm' : 'd')); fs.mkdirSync(shots);
  const r = spawnSync('node', [path.join(HERE, 'playthrough.mjs'), '--set', 'ito/homework-2', '--shots', shots, ...(mobile ? ['--mobile'] : []), ...extra], { env: { ...process.env, ZQ_APP_DIR: copy }, encoding: 'utf8', timeout: 600000 });
  const tag = mobile ? 'mobile' : 'desktop', vh = mobile ? 956 : 860;
  const f = fs.readdirSync(shots).find((n) => /marked(-440)?\.png$/.test(n) && (mobile ? /-440\.png$/.test(n) : !/-440\.png$/.test(n)));
  if (!f) { bad++; console.log(`FAIL ${tag}: no marked shot\n${((r.stdout || '') + (r.stderr || '')).split('\n').slice(-8).join('\n')}`); continue; }
  const img = decode(fs.readFileSync(path.join(shots, f)));
  const tall = img.h > 2 * vh, lowerInk = !img.blank(img.h - 80, img.h), midInk = !img.blank(Math.floor(vh * 1.5), Math.floor(vh * 1.5) + 100);
  if (!tall || !lowerInk || !midInk) { bad++; console.log(`FAIL ${tag}: ${img.w} x ${img.h} (viewport ${vh}), tall ${tall}, bottom rows inked ${lowerInk}, second screen inked ${midInk}`); }
  else console.log(`ok ${tag}: ${img.w} x ${img.h}, below the first viewport is painted`);
}
fs.rmSync(tmp, { recursive: true, force: true });
console.log(bad ? `${bad} failed` : 'all passed');
process.exitCode = bad ? 1 : 0;
