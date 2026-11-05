#!/usr/bin/env node
// PLAN 2c item 6 content transform (ENGINE-BACKLOG 546, 547). Idempotent.
//   node app/tools/apply-item6-content.mjs [--dir <content dir>]
// 1. mock-oa-code: pass mark 1.0 (both problems, the curriculum's exit criterion) and a description that says the mark is
//    illustrative and how the unseen-first draw and the "previously seen" label work.
// 2. mock-oa-sig-2, -3 and mock-oa-trader-2, -3: "versionOf": "<base>" after "id".
// Text edits only, so the rest of each file is untouched; the result is parsed to check it is still JSON.
import { readFileSync, writeFileSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const di = process.argv.indexOf('--dir');
const DIR = di > 0 ? process.argv[di + 1] : join(dirname(fileURLToPath(import.meta.url)), '..', 'content');
const path = (name) => join(DIR, 'exams', name + '.json');
const edit = (name, fn) => { const raw = readFileSync(path(name), 'utf8'), out = fn(raw); JSON.parse(out); if (out !== raw) writeFileSync(path(name), out); };
const once = (raw, re, to, what) => { if (!re.test(raw)) throw new Error(`${what}: pattern not found`); return raw.replace(re, to); };

const DESC = 'This is the reported format of an online coding assessment, as candidates described it by Nov 2026. You have two algorithm problems in 60 minutes and write both in Python. The first is medium and the second is harder. Hidden tests include large inputs, so a slow answer fails them. A problem scores only when all its hidden tests pass. The pass mark is both problems. That is this course\'s exit criterion, so treat it as illustrative: firms do not publish cut-offs. The results panel lists each test, so use it to see how far you got. The two problems are drawn from a pool of eight, unseen ones first. A problem you solved in the drill library, or sat before, is drawn last and labelled previously seen. The pool stays open in the drill library, so for a cold test leave the pack `oa` alone until you have sat this. Other reports give three or four problems in 70 to 90 minutes. Use no search engine and no notes. Read both statements and plan your minutes first.';

edit('mock-oa-code', (raw) => {
  let out = once(raw, /^  "description": ".*",$/m, () => '  "description": ' + JSON.stringify(DESC) + ',', 'description');
  out = once(out, /^(\s*)"pass": (0\.5|1),$/m, '$1"pass": 1,', 'pass');
  return out;
});
for (const base of ['mock-oa-sig', 'mock-oa-trader']) for (const n of [2, 3]) {
  edit(`${base}-${n}`, (raw) => (/^  "versionOf":/m.test(raw) ? raw : once(raw, /^(  "id": ".*",\n)/m, (m) => m + `  "versionOf": "${base}",\n`, 'id line')));
}
console.log('item 6 content applied');
