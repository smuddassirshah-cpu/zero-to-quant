// Test for the playthrough's green-hash cache (engine pass AC part 1): tools/green-cache.mjs and `playthrough.mjs --changed`.
// Run from app/: node tools/test-playthrough-changed.mjs [--local-cdn <pkgs>]   (under two minutes; about a minute is the two real browser runs)
// Works on a scratch copy of app/ (ZQ_APP_DIR) and scratch cache files; app/content is never touched. Checks:
//   an empty cache lists everything; a seeded cache lists nothing; a touched lesson lists that lesson and the fluency set built on it and nothing else;
//   a touched exam lists that exam; a touched file under js/ lists every item; a manifest rewritten with the same data (note and layout changed) lists nothing,
//   and a changed minutes entry lists only its own lesson; --shard applies before the filter (shards partition the changed list); the routes item follows the content;
//   a real run records a passing lesson and not a failing one, and --no-cache records nothing; four processes writing the same cache at once lose no entry.
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawnSync, spawn } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { createHasher, readCache, writeGreen, keyOf, playwrightVersion } from './green-cache.mjs';

const HERE = path.dirname(fileURLToPath(import.meta.url)), APP = path.resolve(HERE, '..');
const PT = path.join(HERE, 'playthrough.mjs');
const extra = process.argv.slice(2);
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'zq-changed-'));
const copy = path.join(tmp, 'app');
fs.cpSync(APP, copy, { recursive: true, filter: (s) => !/\.green-cache/.test(path.basename(s)) });
let bad = 0;
const ok = (c, what) => { if (c) console.log('ok   ' + what); else { bad++; console.log('FAIL ' + what); } };
const run = (args, env = {}) => spawnSync('node', [PT, ...args], { env: { ...process.env, ZQ_APP_DIR: copy, ...env }, encoding: 'utf8', timeout: 110000 });
const cache = path.join(tmp, 'cache.json');

const L1 = 'number-sense/l1-what-a-fraction-measures', L2 = 'number-sense/l2-same-amount', L12 = 'number-sense/l12-which-first';
const SET = 'number-sense/review-1', EXAM = 'topic-0.1', FLU = 'number-sense/fluency-l12-which-first', PRB = 'number-sense/problems-4', BANK = 'mental-1', DRILL = 'daily-returns';
const sel = ['--lesson', L1, '--lesson', L2, '--lesson', L12, '--set', SET, '--exam', EXAM, '--fluency', FLU, '--problems', PRB, '--bank', BANK, '--drill', DRILL, '--no-routes'];
const changed = (more = []) => { const r = run([...sel, ...more, '--changed', '--list', '--cache', cache]); const err = (r.stderr || '').split('\n').find(l => /^changed:/.test(l)) || ''; return { ids: (r.stdout || '').split('\n').filter(Boolean).sort(), err, status: r.status }; };
const items = [['lesson', L1], ['lesson', L2], ['lesson', L12], ['set', SET], ['exam', EXAM], ['fluency', FLU], ['problems', PRB], ['bank', BANK], ['drill', DRILL]];
const seed = () => {
  const h = createHasher({ appDir: copy, selfFile: PT }), e = {};
  for (const [k, id] of items) e[keyOf(k, id, ['desktop'])] = h.itemHash(k, id);
  e[keyOf('routes', 'routes', ['desktop'])] = h.itemHash('routes', 'routes');
  writeGreen(cache, e);
};
const edit = (rel, fn) => { const f = path.join(copy, rel), old = fs.readFileSync(f, 'utf8'); fs.writeFileSync(f, fn(old)); return () => fs.writeFileSync(f, old); };

/* 1. empty cache: everything; seeded: nothing */
let r = changed();
ok(r.ids.length === 9 && /changed: 9 of 9 items/.test(r.err), `empty cache lists all nine selected items (${r.err.trim()})`);
seed();
r = changed();
ok(r.ids.length === 0 && /changed: 0 of 9 items/.test(r.err), `seeded cache lists nothing (${r.err.trim()})`);

/* 2. touching a lesson: that lesson, and the fluency set whose lesson it is */
let undo = edit(`content/courses/${L12.split('/')[0]}/${L12.split('/')[1]}.json`, t => t + '\n');
r = changed();
ok(r.ids.join(' ') === [`fluency/${FLU}`, `lesson/${L12}`].sort().join(' '), `a touched lesson lists itself and its fluency set only (${r.ids.join(', ')})`);
undo();
undo = edit(`content/courses/${L1.split('/')[0]}/${L1.split('/')[1]}.json`, t => t + '\n');
r = changed();
ok(r.ids.join(' ') === `lesson/${L1}`, `a touched lesson with no dependants lists itself only (${r.ids.join(', ')})`);
undo();

/* 3. touching an exam; a review; a bank file; a drill: each lists itself only */
for (const [rel, want] of [[`content/exams/${EXAM}.json`, `exam/${EXAM}`], [`content/courses/${SET.split('/')[0]}/review-1.json`, `set/${SET}`], [`content/bank/${BANK}.json`, `bank/${BANK}`], [`content/drills/${DRILL}.json`, `drill/${DRILL}`]]) {
  undo = edit(rel, t => t + '\n'); r = changed();
  ok(r.ids.join(' ') === want, `touching ${rel} lists ${want} only (${r.ids.join(', ')})`);
  undo();
}

/* 4. the manifest: same data, new note and layout -> nothing; one lesson's minutes -> that lesson only */
const mpath = 'content/manifest.json';
undo = edit(mpath, t => JSON.stringify({ ...JSON.parse(t), note: 'changed note' }));
r = changed();
ok(r.ids.length === 0, `a manifest rewritten with the same data (new note, compact layout) lists nothing (${r.ids.join(', ')})`);
undo();
undo = edit(mpath, t => { const m = JSON.parse(t); m.lessonMinutes[L2] = (m.lessonMinutes[L2] || 10) + 1; return JSON.stringify(m, null, 2) + '\n'; });
r = changed();
ok(r.ids.join(' ') === `lesson/${L2}`, `a changed lessonMinutes entry lists its own lesson only (${r.ids.join(', ')})`);
undo();

/* 5. the engine: a touched file under js/ lists everything, and so does css/ and playthrough's own cache module via the engine hash */
for (const rel of ['js/core.js', 'css/' + fs.readdirSync(path.join(copy, 'css')).find(f => f.endsWith('.css'))]) {
  undo = edit(rel, t => t + '\n/* touched */\n'); r = changed();
  ok(r.ids.length === 9, `touching ${rel} lists all nine items (${r.ids.length})`);
  undo();
}
r = changed(); ok(r.ids.length === 0, 'after undoing every edit nothing is listed');

/* 6. routes: one item, hashed over the content; a lesson edit lists it, a manifest note does not */
const rl = () => run(['--routes-only', '--changed', '--list', '--cache', cache]).stdout.split('\n').filter(Boolean);
ok(rl().join() === '', 'routes: seeded cache lists nothing');
undo = edit(`content/courses/${L1.split('/')[0]}/${L1.split('/')[1]}.json`, t => t + '\n');
ok(rl().join() === 'routes', 'routes: a touched lesson lists the routes item');
undo();
undo = edit('content/prep.json', t => t + '\n');
ok(rl().join() === 'routes', 'routes: a touched prep.json lists the routes item');
undo();

/* 7. --shard applies first, then the filter: with one lesson changed, the shards' lists are disjoint, cover it once, and match the shard of the unfiltered list */
undo = edit(`content/courses/${L1.split('/')[0]}/${L1.split('/')[1]}.json`, t => t + '\n');
let union = [], shardsOk = true;
for (let i = 1; i <= 3; i++) {
  const a = run(['--all', '--no-routes', '--shard', `${i}/3`, '--changed', '--list', '--cache', cache]), plain = run(['--all', '--no-routes', '--shard', `${i}/3`, '--list']);
  const ids = a.stdout.split('\n').filter(Boolean), all = new Set(plain.stdout.split('\n').filter(Boolean));
  if (!ids.every(x => all.has(x))) shardsOk = false;
  union.push(...ids);
}
undo();
const inCache = new Set(Object.keys(readCache(cache)).map(k => k.split('|').slice(0, 2).join('/')));
ok(shardsOk && new Set(union).size === union.length && union.includes(`lesson/${L1}`), `shards 1/3 to 3/3 list each changed item once, each within its own unfiltered shard (${union.length} items, ${inCache.size} seeded)`);
ok(!run(['--all', '--no-routes', '--shard', '1/3', '--changed', '--list', '--cache', cache]).stderr.includes('NaN'), '--shard with --changed prints its changed line');

/* 7b. what the cache may be trusted for (engine pass AC part 5): the same viewport, and the same browser. Seeded at desktop, nothing is green for --mobile or --tablet;
   the installed Playwright version is in the engine hash, so a different version (a new Chromium) lists everything, and the same version lists nothing. */
r = changed();
ok(r.ids.length === 0, `precondition: the desktop-seeded cache lists nothing at desktop (${r.err.trim()})`);
r = changed(['--mobile']);
ok(r.ids.length === 9 && /changed: 9 of 9 items/.test(r.err), `a cache written at desktop is not green for --mobile (${r.err.trim()})`);
r = changed(['--tablet']);
ok(r.ids.length === 9, `a cache written at desktop is not green for --tablet (${r.ids.length} of 9)`);
const fakePw = path.join(tmp, 'node_modules', 'playwright');
fs.mkdirSync(fakePw, { recursive: true });
const setPw = (v) => fs.writeFileSync(path.join(fakePw, 'package.json'), JSON.stringify({ name: 'playwright', version: v }));
setPw('1.63.0'); seed();
r = changed();
ok(r.ids.length === 0, `Playwright 1.63.0 seeded: nothing changed (${r.err.trim()})`);
setPw('1.64.0');
r = changed();
ok(r.ids.length === 9, `Playwright 1.64.0 installed: the whole cache is stale (${r.err.trim()})`);
const e1 = playwrightVersion({ roots: [path.join(tmp, 'node_modules')], env: {} });
ok(e1 === '1.64.0', `playwrightVersion reads the installed package.json (${e1})`);
ok(playwrightVersion({ roots: [path.join(tmp, 'nowhere')], env: { ZQ_PLAYWRIGHT_VERSION: '1.63.0' } }) === '1.63.0', 'with nothing installed the pinned ZQ_PLAYWRIGHT_VERSION stands in (the CI selection step before the browser install)');
ok(playwrightVersion({ roots: [path.join(tmp, 'node_modules')], env: { ZQ_PLAYWRIGHT_VERSION: '1.63.0' } }) === '1.64.0', 'an installed version beats the pin');
ok(playwrightVersion({ roots: [path.join(tmp, 'nowhere')], env: {} }) === 'none', 'no version at all is "none"');
fs.rmSync(path.join(tmp, 'node_modules'), { recursive: true, force: true });
seed();   // back to the ambient browser for the rest

/* 8. a real run: a passing lesson is recorded, a failing one (invalid JSON) is not, and --no-cache records nothing */
const good = `content/courses/${L1.split('/')[0]}/${L1.split('/')[1]}.json`, brk = `content/courses/${L2.split('/')[0]}/${L2.split('/')[1]}.json`;
fs.writeFileSync(path.join(copy, brk), '{"title": "broken"');
const c2 = path.join(tmp, 'real.json');
const t0 = Date.now();
const real = run(['--lesson', L1, '--lesson', L2, '--no-routes', '--cache', c2, ...extra]);
const got = readCache(c2), keys = Object.keys(got);
ok(real.status === 1, `the real run with a broken lesson exits 1 (got ${real.status}, ${((Date.now() - t0) / 1000).toFixed(0)} s)`);
ok(keys.length === 1 && keys[0] === keyOf('lesson', L1, ['desktop']), `only the passing lesson is recorded (${keys.join(', ') || 'nothing'})`);
const h = createHasher({ appDir: copy, selfFile: PT });
ok(got[keyOf('lesson', L1, ['desktop'])] === h.itemHash('lesson', L1), 'the recorded hash is the lesson\'s current hash');
fs.rmSync(path.join(tmp, 'noc.json'), { force: true });
const noc = run(['--lesson', L1, '--no-routes', '--no-cache', '--cache', path.join(tmp, 'noc.json'), ...extra]);
ok(noc.status === 0 && !fs.existsSync(path.join(tmp, 'noc.json')), '--no-cache plays the lesson and writes no cache');
const again = run(['--lesson', L1, '--lesson', L2, '--no-routes', '--changed', '--list', '--cache', c2]);
ok(again.stdout.trim() === `lesson/${L2}`, `--changed after the real run lists only the broken lesson (${again.stdout.trim()})`);

/* 9. four processes write 150 entries each into one cache, one write at a time: no entry is lost */
const c3 = path.join(tmp, 'race.json'), N = 150, P = 4;
const worker = `import { writeGreen } from ${JSON.stringify(path.join(HERE, 'green-cache.mjs'))}; const [f, p, n] = process.argv.slice(2); for (let i = 0; i < +n; i++) writeGreen(f, { ['k|' + p + '-' + i + '|desktop']: 'h' + i });`;
const wf = path.join(tmp, 'worker.mjs'); fs.writeFileSync(wf, worker);
await Promise.all(Array.from({ length: P }, (_, p) => new Promise((res) => { const c = spawn('node', [wf, c3, String(p), String(N)], { stdio: 'inherit' }); c.on('exit', res); })));
const race = readCache(c3);
ok(Object.keys(race).length === N * P, `${P} concurrent writers wrote ${N} entries each and ${Object.keys(race).length} of ${N * P} are in the file`);
ok(!fs.existsSync(c3 + '.lock') && fs.readdirSync(tmp).every(f => !f.endsWith('.tmp')), 'no lock or temporary file is left behind');

fs.rmSync(tmp, { recursive: true, force: true });
console.log(bad ? `${bad} failed` : 'all passed');
process.exitCode = bad ? 1 : 0;
