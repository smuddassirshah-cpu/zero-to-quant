#!/usr/bin/env node
// PLAN 2c item 10 content transform (ENGINE-BACKLOG 558). Sets `minutes` and `session` on the lessons whose opening prose states
// their true length. Text edits only: the `"minutes"` line is replaced in place and a `"session"` line follows it; nothing else in the
// file is touched or reformatted. Idempotent: run twice, same result.
//   node app/tools/apply-item10-content.mjs [--dir <content dir>] [--dry]
// The list below was made by reading each hit's context (node app/tools/duration-prose.mjs --all). The script refuses to run when a lesson
// the matcher flags is on neither list, so a new hit is decided by a person. It never runs on app/content/ by itself: the main session runs it.
import { readFileSync, writeFileSync, existsSync } from 'node:fs';
import { join, dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { execFileSync } from 'node:child_process';
import { statedMinutes, ignoreList } from './duration-prose.mjs';

const arg = (k) => { const i = process.argv.indexOf(k); return i > 0 ? process.argv[i + 1] : null; };
const HERE = dirname(fileURLToPath(import.meta.url));
const DIR = arg('--dir') || join(HERE, '..', 'content');
const DRY = process.argv.includes('--dry');

// The true hits: the opening prose states the lesson's own length. session: null keeps the lesson short (minutes 20 is the short ceiling).
const TRUE = {
  'coding-int/l17-two-in-sixty': { minutes: 60, session: 'workshop', why: '"This lesson budgets one hour for two problems"' },
  'contests/l13-virtual-contest': { minutes: 60, session: 'workshop', why: '"four problems in 60 minutes ... set a 60-minute timer outside the app"' },
  'research-int/l1-two-regressions': { minutes: 25, session: 'workshop', why: '"This lesson takes about 25 minutes, two minutes a question"' },
  'research-int/l2-correlation-limits': { minutes: 30, session: 'workshop', why: '"This lesson takes about 30 minutes"' },
  'research-int/l3-estimators-on-the-spot': { minutes: 35, session: 'workshop', why: '"This lesson takes about 35 minutes"' },
  'research-int/l4-tests-in-words': { minutes: 25, session: 'workshop', why: '"This lesson takes about 25 minutes"' },
  'research-int/l5-matrices-on-the-spot': { minutes: 20, session: null, why: '"This lesson takes about 20 minutes": inside the short range, so only minutes moves' },
  'research-int/l14-house-price-case': { minutes: 50, session: 'workshop', why: '"about 50 minutes with the code screens"' },
  'research-int/l19-timed-data-task': { minutes: 25, session: 'workshop', why: '"A 25-minute task: about 6 minutes to read and clean, 8 to analyse, 11 to model and write up"' },
};
// False positives (named, with the reason) live in tools/duration-prose-ignore.json, which the validator reads too.
const IGNORE = ignoreList();

const MIN_LINE = /^(\s*)"minutes":\s*(\d+(?:\.\d+)?),?\s*$/m;
let changed = 0, same = 0, bad = 0;
const log = (m) => console.log(m);

for (const [key, v] of Object.entries(TRUE)) {
  const [cid, id] = key.split('/');
  const f = join(DIR, 'courses', cid, `${id}.json`);
  if (!existsSync(f)) { log(`MISSING ${key}`); bad++; continue; }
  const text = readFileSync(f, 'utf8');
  const m = MIN_LINE.exec(text);
  if (!m) { log(`NO "minutes" LINE ${key}`); bad++; continue; }
  const indent = m[1];
  const hasSession = /^\s*"session":/m.test(text);
  let out = text.replace(MIN_LINE, `${indent}"minutes": ${v.minutes},`);
  if (v.session) {
    if (hasSession) out = out.replace(/^(\s*)"session":\s*"[a-z]+",?\s*$/m, `$1"session": "${v.session}",`);
    else out = out.replace(MIN_LINE, `${indent}"minutes": ${v.minutes},\n${indent}"session": "${v.session}",`);
  }
  if (out === text) { same++; continue; }
  changed++;
  log(`${DRY ? 'would set' : 'set'} ${key}: minutes ${m[2]} -> ${v.minutes}${v.session ? `, session ${v.session}` : ''}   [${v.why}]`);
  if (!DRY) writeFileSync(f, out);
}

// Coverage: every lesson the matcher still flags (differs by more than 5) must be on a list.
const { readdirSync } = await import('node:fs');
for (const cid of readdirSync(join(DIR, 'courses')).sort()) {
  const dir = join(DIR, 'courses', cid);
  if (!existsSync(join(dir, 'course.json'))) continue;
  for (const f of readdirSync(dir).filter((x) => /^l\d+.*\.json$/.test(x))) {
    const key = `${cid}/${f.replace(/\.json$/, '')}`;
    if (TRUE[key] || IGNORE[key]) continue;
    const L = JSON.parse(readFileSync(join(dir, f), 'utf8'));
    const st = Array.isArray(L.screens) ? statedMinutes(L) : null;
    if (st && Math.abs(st.minutes - L.minutes) > 5) { log(`UNDECIDED ${key}: "${st.text}" vs minutes ${L.minutes}; add it to TRUE or to tools/duration-prose-ignore.json`); bad++; }
  }
}
for (const key of Object.keys(IGNORE)) if (!existsSync(join(DIR, 'courses', ...key.split('/')) + '.json')) { log(`IGNORE entry has no file: ${key}`); bad++; }
log(`item 10: ${changed} lesson file(s) ${DRY ? 'would change' : 'changed'}, ${same} already set, ${Object.keys(IGNORE).length} named false positives left alone${bad ? `, ${bad} PROBLEM(S)` : ''}`);
// Workshop lessons weigh more in the hours a topic shares to its courses (js/hours.js), so content/readiness.json and the blocks of docs/readiness.md
// move: regenerate them here so readiness-sums.mjs exits 0 afterwards. Only for the default content folder (this tool's own repo).
if (!bad && !DRY && changed) {
  if (resolve(DIR) === resolve(HERE, '..', 'content')) log(execFileSync('node', [join(HERE, 'readiness-sums.mjs'), '--write'], { encoding: 'utf8' }).trim());
  else log('now run: node app/tools/readiness-sums.mjs --write (in the tree that holds this content folder)');
}
process.exit(bad ? 1 : 0);
