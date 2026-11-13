#!/usr/bin/env node
/* Runs every number script and reports failures (ENGINE-BACKLOG 971, docs/CI.md). Number scripts are the author and reviewer Python files that
   recompute each stated figure, key and slip of a level: `docs/reports/*-numbers*.py` and the `*number*.py` files under
   `docs/briefs/*-scripts/` and `docs/reviews/*-scripts/`. Exit 0 from a script means every check passed.

     node tools/run-number-scripts.mjs [--python <exe>] [--timeout <s>] [--jobs <n>] [--only <text>] [--list]
                                       [--changed [<base-ref>]] [--allow <file>] [--root <repo>] [--quiet]

   Prints only the failures (the last lines of each one's output) and a one-line count. The known-failing list
   `tools/number-scripts-known-failing.txt` has one `path | reason` per line (path from the repo root; `#` starts a comment). Exit 1 when
     - a script fails or times out and is not on the list (a new failure), or
     - a script on the list passes (remove its line), or a listed path no longer exists (remove it).
   Exit 0 otherwise, so the job is green while the listed scripts keep failing and red the moment that changes.
   --changed: run only scripts whose own file changed against the base ref (default origin/main, or the ref after --changed), or that name a
   course, exam or bank file whose content changed, or all of them when `tools/numbers_lib.py` or the shared check helpers changed. The list
   check then covers only the scripts that ran. --only runs scripts whose path holds the text (list check likewise). Exit 2: setup error.
   Python: --python, else $ZQ_PYTHON, else python3. Timeout default 100 s per script; jobs default 4. */
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import { spawn, execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const argv = process.argv.slice(2);
const opt = (name) => { const i = argv.indexOf(name); return i >= 0 && i + 1 < argv.length && !argv[i + 1].startsWith('--') ? argv[i + 1] : null; };
const has = (name) => argv.includes(name);

const ROOT = path.resolve(opt('--root') || path.join(HERE, '..', '..'));
const PY = opt('--python') || process.env.ZQ_PYTHON || 'python3';
const TIMEOUT = Number(opt('--timeout') || 100) * 1000;
const JOBS = Math.max(1, Number(opt('--jobs') || Math.min(4, os.cpus().length || 4)));
const ALLOW = path.resolve(opt('--allow') || path.join(HERE, 'number-scripts-known-failing.txt'));
const ONLY = opt('--only');
const QUIET = has('--quiet');
const CHANGED = has('--changed');
const BASE = CHANGED ? (opt('--changed') || 'origin/main') : null;

const rel = (p) => path.relative(ROOT, p).split(path.sep).join('/');
const ls = (d) => { try { return fs.readdirSync(d).map((f) => path.join(d, f)); } catch { return []; } };

/* the scripts */
function findScripts() {
  const out = [];
  for (const f of ls(path.join(ROOT, 'docs', 'reports'))) if (/-numbers[^/]*\.py$/.test(f)) out.push(f);
  for (const top of ['briefs', 'reviews'])
    for (const d of ls(path.join(ROOT, 'docs', top)))
      if (/-scripts$/.test(d)) for (const f of ls(d)) if (/number[^/]*\.py$/.test(f)) out.push(f);
  return out.map(rel).sort();
}

/* the known-failing list: Map path -> reason */
function readAllow() {
  const m = new Map();
  if (!fs.existsSync(ALLOW)) return m;
  for (const [i, raw] of fs.readFileSync(ALLOW, 'utf8').split('\n').entries()) {
    const line = raw.trim();
    if (!line || line.startsWith('#')) continue;
    const k = line.indexOf(' | ');
    if (k < 0) { console.error(`run-number-scripts: ${rel(ALLOW)} line ${i + 1} is not "path | reason"`); process.exit(2); }
    m.set(line.slice(0, k).trim(), line.slice(k + 3).trim());
  }
  return m;
}

/* --changed: which scripts to run */
function changedSelection(all) {
  let names;
  try {
    names = execFileSync('git', ['-C', ROOT, 'diff', '--name-only', `${BASE}...HEAD`], { encoding: 'utf8', stdio: ['ignore', 'pipe', 'pipe'] }).split('\n').filter(Boolean);
  } catch (e) {
    console.error(`run-number-scripts: cannot diff against ${BASE} (${String(e.stderr || e.message).trim().split('\n')[0]}); running every script`);
    return all;
  }
  const set = new Set(names);
  if (names.some((n) => /^app\/tools\/numbers_lib\.py$|^docs\/reports\/(bank_2_code_check|py_found_read12)\.py$/.test(n))) return all;
  const tokens = new Set();
  for (const n of names) {
    let m;
    if ((m = /^app\/content\/courses\/([^/]+)\//.exec(n))) tokens.add(m[1]);
    else if ((m = /^app\/content\/(?:exams|bank)\/([^/]+?)\.json$/.exec(n))) tokens.add(m[1]);
  }
  const res = [];
  for (const s of all) {
    if (set.has(s)) { res.push(s); continue; }
    if (!tokens.size) continue;
    let src = ''; try { src = fs.readFileSync(path.join(ROOT, s), 'utf8'); } catch { /* skip */ }
    const hit = [...tokens].some((t) => new RegExp(`(?<![\\w-])${t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')}(?![\\w-])`).test(src));
    if (hit) res.push(s);
  }
  return res;
}

/* one script, with a timeout that kills its whole process group */
function runOne(script) {
  return new Promise((resolve) => {
    const t0 = Date.now();
    const p = spawn(PY, [path.join(ROOT, script)], { cwd: ROOT, detached: true, stdio: ['ignore', 'pipe', 'pipe'], env: { OMP_NUM_THREADS: '1', OPENBLAS_NUM_THREADS: '1', MKL_NUM_THREADS: '1', ...process.env, PYTHONIOENCODING: 'utf-8' } });
    let buf = '';
    const keep = (d) => { buf += d.toString(); if (buf.length > 20000) buf = buf.slice(-10000); };
    p.stdout.on('data', keep); p.stderr.on('data', keep);
    let timedOut = false, done = false;
    const timer = setTimeout(() => { timedOut = true; try { process.kill(-p.pid, 'SIGKILL'); } catch { /* gone */ } }, TIMEOUT);
    const fin = (code, err) => { if (done) return; done = true; clearTimeout(timer); resolve({ script, ok: !timedOut && code === 0, timedOut, code, secs: (Date.now() - t0) / 1000, out: err ? String(err) : buf }); };
    p.on('error', (e) => fin(-1, e.message));
    p.on('close', (code) => fin(code));
  });
}

async function pool(items, n, fn) {
  const results = []; let next = 0;
  await Promise.all(Array.from({ length: Math.min(n, items.length) }, async () => { while (next < items.length) { const i = next++; results[i] = await fn(items[i]); } }));
  return results;
}

const all = findScripts();
if (!all.length) { console.error(`run-number-scripts: no number scripts under ${ROOT}`); process.exit(2); }
if (has('--list')) { console.log(all.join('\n')); console.log(`${all.length} number scripts`); process.exit(0); }

const allow = readAllow();
let todo = all;
let partial = false;
if (CHANGED) { todo = changedSelection(all); partial = todo.length < all.length; }
if (ONLY) { todo = todo.filter((s) => s.includes(ONLY)); partial = true; }

const t0 = Date.now();
const results = await pool(todo, JOBS, runOne);
const secs = Math.round((Date.now() - t0) / 1000);

let fresh = 0, known = 0, stale = 0, passed = 0;
const ran = new Set(todo);
for (const r of results) {
  const listed = allow.has(r.script);
  if (r.ok) {
    passed++;
    if (listed) { stale++; console.log(`PASSES NOW  ${r.script} is on the known-failing list but passes (${r.secs.toFixed(0)} s): remove its line from ${rel(ALLOW)}`); }
  } else if (listed) known++;
  else {
    fresh++;
    const why = r.timedOut ? `timed out after ${TIMEOUT / 1000} s` : `exit ${r.code}`;
    console.log(`FAILED      ${r.script} (${why})`);
    if (!QUIET) console.log(r.out.trim().split('\n').slice(-6).map((l) => '    ' + l.slice(0, 200)).join('\n'));
  }
}
for (const p of allow.keys()) {
  if (!all.includes(p)) { stale++; console.log(`MISSING     ${p} is on the known-failing list but is not a number script: remove its line`); }
  else if (!partial && !ran.has(p)) { /* cannot happen in a full run */ }
}
const bad = fresh + stale;
console.log(`run-number-scripts: ${todo.length}${partial ? ` of ${all.length}` : ''} scripts, ${passed} passed, ${known} known failing, ${fresh} new failure${fresh === 1 ? '' : 's'}, ${stale} stale list line${stale === 1 ? '' : 's'}, ${secs} s`);
process.exit(bad ? 1 : 0);
