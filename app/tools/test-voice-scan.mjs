#!/usr/bin/env node
/* Test for docs/reviews/voice-scan.py (engine pass 9, item e; ENGINE-BACKLOG 1187): a lesson id written as a code span in learner text is listed, a bare id, a call in a code span,
   another course's name in a code span and a fenced block are not; a doubled word in prose is listed (pass 9b), one in maths, code or "had had" is not. Usage: node tools/test-voice-scan.mjs. Exit 0 pass, 1 failure. */
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
const APP = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const r = spawnSync('python3', [path.join(APP, '../docs/reviews/voice-scan.py'), '35'], { env: { ...process.env, VOICE_BASE: path.join(APP, 'tools/fixtures/voice') }, encoding: 'utf8' });
const out = (r.stdout || '') + (r.stderr || '');
const lines = out.split('\n').filter((l) => l.startsWith('# lesson id in a code span'));
const ok = [
  ['two ids listed', lines.length === 2],
  ['`l4` listed', lines.some((l) => l.includes('`l4`'))],
  ['`l12-name` listed', lines.some((l) => l.includes('`l12-name`'))],
  ['count line', /# lesson ids in code spans: 2/.test(out)],
  ['no other course name listed', !lines.some((l) => l.includes('`ito`'))],
  /* engine pass 9b, ENGINE-BACKLOG 1209: a doubled word in prose */
  ['"the the" listed', /# doubled word: .*"the the"/.test(out)],
  ['"Is is" listed', /# doubled word: .*"Is is"/.test(out)],
  ['two doubled words, none from maths, code or "had had"', /# doubled words: 2\b/.test(out)],
];
let bad = 0;
for (const [n, c] of ok) { console.log(`${c ? 'PASS' : 'FAIL'} ${n}`); if (!c) bad++; }
console.log(bad ? `${bad} failed` : 'all passed');
process.exit(bad ? 1 : 0);
