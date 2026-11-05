#!/usr/bin/env node
// PLAN 2c item 4: write a per-level `pass` share into every mapped level review file.
// Content change run by the main session, never by the engine. Idempotent: a file that already
// carries `pass` is left alone. The key is inserted textually after the `"level": n,` line so each
// file keeps its own indentation and layout.
// Usage (from the repo root): node app/tools/write-review-pass.mjs [--pass 0.8] [--dry]
import { readFileSync, writeFileSync, existsSync, readdirSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..', 'content', 'courses');
const args = process.argv.slice(2);
const dry = args.includes('--dry');
const pi = args.indexOf('--pass');
const PASS = pi >= 0 ? Number(args[pi + 1]) : 0.8;   // matches the quiz MASTERY bar (state.js)
if (!(PASS > 0 && PASS <= 1)) { console.error('bad --pass'); process.exit(2); }

let written = 0, kept = 0, failed = 0;
for (const cid of readdirSync(ROOT)) {
  const cp = join(ROOT, cid, 'course.json');
  if (!existsSync(cp)) continue;
  const course = JSON.parse(readFileSync(cp, 'utf8'));
  for (const lv of course.levels || []) {
    if (!lv.review) continue;
    const rp = join(ROOT, cid, `${lv.review}.json`);
    if (!existsSync(rp)) continue;
    const src = readFileSync(rp, 'utf8');
    const doc = JSON.parse(src);
    if (doc.pass != null) { kept++; continue; }
    const m = src.match(/^([ \t]*)"level":[ \t]*[^,\n]+,[ \t]*\n/m);
    if (!m) { console.error(`FAIL no level line: ${cid}/${lv.review}`); failed++; continue; }
    const at = m.index + m[0].length;
    const out = src.slice(0, at) + `${m[1]}"pass": ${PASS},\n` + src.slice(at);
    const back = JSON.parse(out);
    if (back.pass !== PASS || JSON.stringify({ ...back, pass: undefined }) !== JSON.stringify({ ...doc, pass: undefined })) {
      console.error(`FAIL round trip: ${cid}/${lv.review}`); failed++; continue;
    }
    if (!dry) writeFileSync(rp, out);
    written++;
  }
}
console.log(`review pass ${PASS}: written ${written}, already set ${kept}, failed ${failed}${dry ? ' (dry run)' : ''}`);
process.exit(failed ? 1 : 0);
