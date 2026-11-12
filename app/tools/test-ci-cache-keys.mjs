// Test for the CI cache-key design (engine pass AC part 5, docs/CI.md "The green-hash cache"). No browser, no network, about a second.
// Run from app/: node tools/test-ci-cache-keys.mjs
// 1. A small model of actions/cache (immutable keys, a restore takes an exact key or else the newest cache whose key starts with a restore-key, branch scoped) is driven by
//    the real writeGreen / readCache / makeLookup with two fake jobs and a cancelled one: a job restores its own file only; a cancelled job saves nothing, so its greens are
//    lost, never wrongly kept; a failed job saves its passes and never its failure; a re-run (same run id) cannot overwrite; prefixes "-1-" and "-10-" do not collide;
//    another branch starts empty; an older engine hash shows everything as changed.
// 2. The workflow text still uses the keys the model assumes (a restore-key ending in "-", every save and restore under one scheme, saves guarded by !cancelled()).
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { readCache, writeGreen, makeLookup } from './green-cache.mjs';

const HERE = path.dirname(fileURLToPath(import.meta.url));
let bad = 0;
const ok = (c, what) => { if (c) console.log('ok   ' + what); else { bad++; console.log('FAIL ' + what); } };
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'zq-cachekeys-'));

/* ---- the model of actions/cache ---- */
const store = [];   // { key, branch, seq, data }
let seq = 0;
const save = (branch, key, file) => {
  if (store.some(c => c.key === key && c.branch === branch)) return 'exists';   // immutable: the second save of a key is refused, not an overwrite
  if (!fs.existsSync(file)) return 'no file';
  store.push({ key, branch, seq: ++seq, data: fs.readFileSync(file, 'utf8') }); return 'saved';
};
const restore = (branch, key, restoreKeys, file) => {
  const vis = store.filter(c => c.branch === branch || c.branch === 'main');
  let hit = vis.filter(c => c.key === key).sort((a, b) => b.seq - a.seq)[0];
  for (const rk of restoreKeys) { if (hit) break; hit = vis.filter(c => c.key.startsWith(rk)).sort((a, b) => b.seq - a.seq)[0]; }
  if (hit) fs.writeFileSync(file, hit.data);
  return hit ? hit.key : null;
};

/* ---- a fake job: restore, select, "play" the items, record greens in batches, then save when not cancelled and the file grew ---- */
const ENGINE = 'E1';
const hashOf = (item, engine = ENGINE) => `${engine}:${item}:v1`;
let runId = 0;
const job = ({ id, branch = 'dev', mode = 'changed', items, fails = [], cancelAfter = null, engine = ENGINE, attempt = 1, run = runId }) => {
  const file = path.join(tmp, `${id}-${run}-${attempt}.json`);
  const prefix = `green-${id}-`, key = `${prefix}${run}-${attempt}`;
  const restoredFrom = mode === 'changed' ? restore(branch, key, [prefix], file) : null;
  const lookup = makeLookup(readCache(file));
  const sel = mode === 'changed' ? items.filter(i => !lookup('lesson', i, ['desktop'], hashOf(i, engine))) : items;
  const before = fs.existsSync(file) ? fs.readFileSync(file, 'utf8') : 'none';
  const batch = {};
  let played = 0, cancelled = false;
  for (const i of sel) {
    if (cancelAfter !== null && played === cancelAfter) { cancelled = true; break; }
    played++;
    if (!fails.includes(i)) batch['lesson|' + i + '|desktop'] = hashOf(i, engine);
    if (Object.keys(batch).length >= 2) { writeGreen(file, batch); for (const k of Object.keys(batch)) delete batch[k]; }   // batches, as playthrough writes every 12
  }
  if (!cancelled) writeGreen(file, batch);
  else writeGreen(file, batch);   // the process was killed in reality: what it had written stays on the dead runner; only the save step decides
  const after = fs.existsSync(file) ? fs.readFileSync(file, 'utf8') : 'none';
  const dirty = after !== 'none' && after !== before;
  const saved = (!cancelled && dirty) ? save(branch, key, file) : 'skipped';
  return { k: sel.length, n: items.length, restoredFrom, saved, file };
};

/* ---- run 1: two jobs seed, one is cancelled half way ---- */
runId = 1;
const A = ['a1', 'a2', 'a3'], B = ['b1', 'b2', 'b3', 'b4'], C = ['c1', 'c2', 'c3', 'c4', 'c5'];
let r = job({ id: 'play-16-desktop-1', items: A });
ok(r.k === 3 && r.saved === 'saved' && r.restoredFrom === null, 'run 1, job A: nothing restored, all 3 played, cache saved');
r = job({ id: 'play-16-desktop-2', items: B, fails: ['b2'] });
ok(r.k === 4 && r.saved === 'saved', 'run 1, job B fails one item: it still saves its other greens');
const bRun1 = readCache(r.file);
ok(!('lesson|b2|desktop' in bRun1) && Object.keys(bRun1).length === 3, 'the failed item is never recorded, the other three are');
r = job({ id: 'play-16-desktop-3', items: C, cancelAfter: 3 });
ok(r.saved === 'skipped' && Object.keys(readCache(r.file)).length >= 2, 'run 1, job C is cancelled half way: it had written greens on its runner but saves nothing');

/* ---- run 2: each restores its own file; latest wins ---- */
runId = 2;
r = job({ id: 'play-16-desktop-1', items: A });
ok(r.k === 0 && r.restoredFrom === 'green-play-16-desktop-1-1-1' && r.saved === 'skipped', 'run 2, job A: restored run 1\'s cache, changed 0 of 3, nothing to save');
r = job({ id: 'play-16-desktop-2', items: B });
ok(r.k === 1 && r.restoredFrom === 'green-play-16-desktop-2-1-1', 'run 2, job B: replays only the item that failed in run 1 (changed 1 of 4)');
r = job({ id: 'play-16-desktop-3', items: C });
ok(r.k === 5 && r.restoredFrom === null, 'run 2, job C: the cancelled job\'s greens were lost, not kept (changed 5 of 5)');
ok(r.saved === 'saved', 'run 2, job C then saves a cache');

/* ---- no cross-talk, no overwrite, no stale branch ---- */
runId = 3;
store.push({ key: 'green-play-16-desktop-10-1-1', branch: 'dev', seq: ++seq, data: JSON.stringify({ version: 1, entries: { 'lesson|zz|desktop': hashOf('zz') } }) });
r = job({ id: 'play-16-desktop-1', items: ['zz', ...A] });
ok(r.restoredFrom === 'green-play-16-desktop-1-2-1' || r.restoredFrom === 'green-play-16-desktop-1-1-1', 'shard 1 does not pick up shard 10 (the restore-key ends in "-")');
ok(r.k === 1, 'and shard 1 does not see shard 10\'s entry (changed 1 of 4)');
ok(save('dev', 'green-play-16-desktop-1-1-1', r.file) === 'exists', 'a second save under an existing key is refused, never an overwrite (a re-run uses the attempt number in the key)');
r = job({ id: 'play-16-desktop-2', items: B, branch: 'feature' });
ok(r.restoredFrom === null && r.k === 4, 'another branch cannot see the development branch\'s caches: everything is changed');
r = job({ id: 'play-16-desktop-2', items: B, engine: 'E2' });
ok(r.k === 4, 'an older engine hash in the cache shows every item as changed (changed 4 of 4)');
r = job({ id: 'play-16-desktop-2', items: B, mode: 'full', run: 7 });
ok(r.k === 4 && r.restoredFrom === null && r.saved === 'saved', 'a full run restores nothing, replays all 4 and saves a fresh cache (it reseeds)');
r = job({ id: 'play-16-desktop-2', items: B, mode: 'changed', run: 9 });
ok(r.k === 0, 'the next changed run restores the newest cache (the reseed) and replays nothing');
r = job({ id: 'play-16-mobile-2', items: B });
ok(r.restoredFrom === null && r.k === 4, 'a mobile job never reads a desktop job\'s file (the viewport is in the key)');

/* ---- the workflow text ---- */
const wf = fs.readFileSync(path.resolve(HERE, '..', '..', '.github', 'workflows', 'acceptance.yml'), 'utf8');
const keys = [...wf.matchAll(/^\s+(restore-keys|key): (green-[^\n]+)$/gm)].map(m => [m[1], m[2]]);
ok(keys.length === 6, `the workflow has 2 restore, 2 restore-key and 2 save keys under green- (${keys.length} found)`);
ok(keys.filter(([t]) => t === 'restore-keys').every(([, v]) => /-$/.test(v.trim())), 'every restore-keys prefix ends in "-"');
ok(keys.filter(([t]) => t === 'key').every(([, v]) => v.includes('github.run_id') && v.includes('github.run_attempt')), 'every key carries the run id and the attempt');
ok([...wf.matchAll(/actions\/cache\/save@v4/g)].length === 2 && [...wf.matchAll(/Save the green cache\n\s+if: \$\{\{ !cancelled\(\)/g)].length === 2, 'both saves are guarded by !cancelled()');
ok(!/actions\/cache@v4\s+with:\s+path: app\/tools\/\.green-cache/.test(wf), 'the green cache is never saved by the post step of actions/cache (which would save on a failed job too, and be restored without a guard)');

fs.rmSync(tmp, { recursive: true, force: true });
console.log(bad ? `${bad} failed` : 'all passed');
process.exitCode = bad ? 1 : 0;
