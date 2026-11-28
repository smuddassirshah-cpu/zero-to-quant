/* Python code widgets in node, with no browser (ENGINE-BACKLOG 1031, 1008, 1028, 1032). Used by `grade-all.mjs --code`.
   The widget's own source (js/engine/widgets/code.js, through its `casePlan`) builds the harness; the page's worker grader (the GRADER
   string of js/screens/drill-worker.js) runs it in Pyodide inside a worker thread. The page's time limits apply per case: a case that
   passes its limit kills the thread and a fresh one loads, as the page does, and the case reports "Stopped after N s" as on the page.
   Needs the local Pyodide: <pkgs>/pyodide-0.27.7/package or <dir>/pyodide (fetch-vendor.sh layout; the same --local-cdn folder as the playthrough), packages included.
   Exports: makeRunner({ pkgs, root, jobs }) -> { grade(spec, src, which, opts), close() }.
     grade resolves to { ok, key, rows, error, printed, ms } for `which` = 'tests' or 'examples' (key as the page gives: null, test-N, error). */
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { Worker, isMainThread, parentPort, workerData } from 'node:worker_threads';
import { fileURLToPath, pathToFileURL } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));

/* ---------- the worker thread: one Pyodide, the page worker's run loop ---------- */
if (!isMainThread && workerData && workerData.zqCodeWorker) {
  const { indexDir, graderSrc, deep } = workerData;
  const { loadPyodide } = await import(pathToFileURL(path.join(indexDir, 'pyodide.mjs')).href);
  let py = null, runFn = null;
  const boot = async () => { py = await loadPyodide({ indexURL: indexDir + '/', stdout: () => {}, stderr: () => {} }); py.runPython(graderSrc); runFn = py.globals.get('drl_run'); };
  await boot();
  const isStackOverflow = (err) => err instanceof RangeError || /call stack|fatally failed/i.test(String((err && err.message) || err));
  parentPort.postMessage({ type: 'ready' });
  parentPort.on('message', async (m) => {
    if (m.type !== 'run') return;
    const emit = (s) => parentPort.postMessage({ type: 'event', id: m.id, data: String(s) });
    const pk = (phase, text) => parentPort.postMessage({ type: 'pkgs', id: m.id, phase, text });
    try {
      const prepare = async () => {
        pk('start');
        try { await py.loadPackagesFromImports(((own) => (own.size ? py.pyodide_py.code.find_imports(m.code).toJs().filter(x => !own.has(x)).map(x => 'import ' + x).join('\n') : m.code))(new Set(((m.spec && m.spec.local) || []).map(n => String(n).replace(/^.*\//, '').replace(/\.py$/, '')))), { messageCallback: () => {}, errorCallback: () => {} }); } catch (e) { emit('Package load failed: ' + ((e && e.message) || e)); }
        pk('end');
        py.runPython("import os as _o, shutil as _s, tempfile as _t\n_p = globals().get('_zq_run_dir')\n_o.chdir('/')\nif _p: _s.rmtree(_p, ignore_errors=True)\n_zq_run_dir = _t.mkdtemp(prefix='run-')\n_o.chdir(_zq_run_dir)");
      };
      await prepare();
      const seen = { loaded: false, last: -1 };
      const watch = (s) => { emit(s); try { const d = JSON.parse(s); if (d.kind === 'loaded') seen.loaded = true; else if (d.kind === 'test') seen.last = d.i; } catch { /* not JSON */ } };
      const n = m.spec.tests.length;
      let from = 0, resume = false;
      for (;;) {
        try { runFn(m.code, JSON.stringify({ ...m.spec, from, resume }), watch); break; } catch (err) {
          if (!isStackOverflow(err)) throw err;
          if (!seen.loaded) { emit(JSON.stringify({ kind: 'error', stage: 'load', error: deep, stdout: '' })); break; }
          const i = seen.last + 1; seen.last = i;
          emit(JSON.stringify({ kind: 'test', i, ok: false, actual: null, type: 'NoneType', number: false, error: deep, stdout: '', ms: 0 }));
          if (i + 1 >= n) { emit(JSON.stringify({ kind: 'done', ms: 0 })); break; }
          py = null; runFn = null; await boot(); await prepare(); from = i + 1; resume = true;
        }
      }
    } catch (err) { parentPort.postMessage({ type: 'crash', id: m.id, message: String((err && err.message) || err) }); }
    parentPort.postMessage({ type: 'end', id: m.id });
  });
}

/* ---------- the widget's own planning code, loaded in a small fake window ---------- */
const loadPlan = (root) => {
  const g = { console, setTimeout, clearTimeout, document: {}, navigator: {} };
  g.window = g; g.globalThis = g; vm.createContext(g);
  g.ZQ = { widgets: { register() {} }, esc: (s) => String(s), h: () => ({}) };
  vm.runInContext(fs.readFileSync(path.join(root, 'js/engine/widgets/code.js'), 'utf8'), g, { filename: 'code.js' });
  const P = g.ZQ.widgets.codePlan;
  if (!P || !P.casePlan) throw new Error('js/engine/widgets/code.js does not export codePlan.casePlan');
  return P;
};

export const makeRunner = ({ pkgs, root, jobs = 2 }) => {
  const indexDir = [path.join(pkgs, 'pyodide-0.27.7', 'package'), path.join(pkgs, 'pyodide')].find((d) => fs.existsSync(path.join(d, 'pyodide.mjs'))) || path.join(pkgs, 'pyodide-0.27.7', 'package');   // the pkgs layout, else fetch-vendor.sh's
  if (!fs.existsSync(path.join(indexDir, 'pyodide.mjs'))) throw new Error(`no Pyodide at ${indexDir} (give --local-cdn <pkgs>)`);
  const P = loadPlan(root);
  const workerSrc = fs.readFileSync(path.join(root, 'js/screens/drill-worker.js'), 'utf8');
  const graderSrc = /const GRADER = String\.raw`([\s\S]*?)`;/.exec(workerSrc)[1];
  const deep = (/const DEEP = '([^']*)'/.exec(workerSrc) || [0, 'RecursionError: maximum recursion depth exceeded.'])[1];
  const idle = [], waiting = []; let live = 0, closed = false;
  const spawn = () => new Promise((resolve, reject) => {
    const w = new Worker(fileURLToPath(import.meta.url), { workerData: { zqCodeWorker: true, indexDir, graderSrc, deep } });
    live++;
    w.once('message', (m) => (m.type === 'ready' ? resolve(w) : reject(new Error('worker did not start'))));
    w.once('error', reject);
  });
  const take = async () => { if (idle.length) return idle.pop(); if (live < jobs) return spawn(); return new Promise((r) => waiting.push(r)); };
  const give = (w) => { if (closed) { w.terminate(); return; } const next = waiting.shift(); if (next) next(w); else idle.push(w); };
  const replace = async (w) => { live--; await w.terminate(); const next = waiting.shift(); if (next) next(await spawn()); };

  /* one run of cases on a worker; mirrors Py.exec in code.js. cap: an optional hard limit per case (ms) replacing the page's */
  const exec = (w, code, cases, plan, capMs) => new Promise((resolve) => {
    const id = Math.random(); let timer = 0, at = -1, limit = capMs || plan.caseMs(-1), settled = false, crash = null, loadErr = null, loaded = '';
    const rows = plan.rows, times = cases.map(() => null);
    const finish = (info) => { if (settled) return; settled = true; clearTimeout(timer); w.off('message', onMsg); w.off('error', onErr); resolve({ info, rows, loadErr, loaded, times }); };
    const arm = () => { clearTimeout(timer); timer = setTimeout(() => finish({ timeout: true, at }), limit); };
    const onErr = (e) => finish({ crash: String((e && e.message) || e), dead: true });
    const onMsg = (m) => {
      if (m.id !== id) return;
      if (m.type === 'event') {
        let d = null; try { d = JSON.parse(m.data); } catch { return; }
        if (d.kind === 'loaded' || d.kind === 'test') { at = d.kind === 'loaded' ? 0 : d.i + 1; limit = capMs || plan.caseMs(at); arm(); }
        if (d.kind === 'error') { loadErr = d.error; loaded = P.quietLib(d.stdout); }
        if (d.kind === 'loaded') loaded = P.quietLib(d.stdout);
        if (d.kind === 'test') {
          const r = rows[d.i]; if (!r) return;
          const out = P.quietLib(d.stdout), k = out.lastIndexOf(P.MARK);
          r.actual = k >= 0 ? out.slice(k + P.MARK.length) : null;
          r.stdout = k >= 0 ? out.slice(0, k) : out;
          if (!r.out) r.stdout = r.stdout.trim();
          r.error = d.error || null; r.ok = !!d.ok && !d.error; times[d.i] = d.ms;
        }
      } else if (m.type === 'pkgs') { if (m.phase === 'start') { clearTimeout(timer); timer = setTimeout(() => finish({ timeout: true, loading: true }), 120000); } else if (m.phase === 'end') arm(); }
      else if (m.type === 'crash') crash = m.message;
      else if (m.type === 'end') finish({ crash });
    };
    w.on('message', onMsg); w.on('error', onErr);
    arm();
    w.postMessage({ type: 'run', id, code, spec: { fn: '__zq_case', compare: 'isclose', prelude: '', local: plan.local, tests: cases.map((_, i) => ({ args: `(${i},)`, expected: 1 })) } });
  });

  /* grade `src` against the widget's tests (or examples), as the page's grade() does */
  const grade = async (spec, src, which = 'tests', opts = {}) => {
    const cases = (which === 'examples' ? spec.examples : spec.tests) || [];
    const all = [...(spec.examples || []), ...(spec.tests || [])];
    const script = all.some((c) => P.isOut(c) || c.stdin != null || c.argv != null || (c.compare === 'raises' && c.call == null));
    let data = null;
    if (spec.data && typeof spec.data === 'object') { data = {}; for (const [n, p] of Object.entries(spec.data)) data[n] = fs.readFileSync(path.join(root, String(p).replace(/^\/+/, '')), 'utf8'); }
    const plan = P.casePlan(spec, cases, src, script, data);
    const t0 = Date.now();
    let w = await take(), res;
    try { res = await exec(w, plan.code, cases, plan, opts.capMs); } catch (e) { res = { info: { crash: String(e) }, rows: plan.rows, times: [], loadErr: null, loaded: '' }; }
    const { info, rows, loadErr, loaded, times } = res;
    if (info.timeout || info.dead) await replace(w); else give(w);
    let error = null, timeoutAt = null;
    if (info.timeout && !info.loading && info.at != null && info.at >= 0 && info.at < rows.length && !loadErr) {
      const k = info.at, secs = Math.round((opts.capMs || plan.caseMs(k)) / 100) / 10;
      rows[k].error = `Stopped after ${secs} s on this test.`; timeoutAt = k;
      rows.forEach((x, i) => { if (i > k) x.error = 'Not run: an earlier test went past its time limit.'; });
    } else error = loadErr ? P.cleanTb(loadErr) : info.loading ? 'The packages took more than two minutes to load.' : info.timeout ? 'Stopped after the time limit.' : info.crash || null;
    const n = rows.filter((x) => x.ok).length, first = rows.findIndex((x) => !x.ok);
    const ok = !error && n === cases.length && cases.length > 0;
    return { ok, key: ok ? null : error ? 'error' : `test-${first + 1}`, rows, error, printed: loaded, timeoutAt, times, limits: cases.map((_, k) => plan.caseMs(k)), ms: Date.now() - t0 };
  };
  const close = async () => { closed = true; await Promise.all([...idle].map((w) => w.terminate())); };
  return { grade, close };
};

/* ---------- the checks on one Python code widget (ENGINE-BACKLOG 1031, 1028, 1032) ----------
   solution-fails     the authored `solution` fails a hidden test, or errors (detail names the first failing test)
   examples-fail      the `solution` fails an example (the learner's "Run examples" would show a red row)
   starter-passes     the `starter` passes every hidden test (nothing to do, yet marked right)
   mutant-passes      a `mutants` source passes every hidden test
   mutant-wrong-test  a `mutants` source first fails another test than the one it names (the byKey line would not show it)
   mutant-thin-margin a `mutants` entry marked timeout: true finishes within `factor` (default 5) times the case's time limit, or the solution
                      takes more than 1/factor of that limit on it (a faster or slower browser could flip the verdict)
   In ai-strand files (grade-all passes the parent's byKey) also feedback-unreachable and feedback-missing, see below.
   A mutant is { "source": "<Python>", "test": N (1-based, the first failing hidden test), "symptom": "<optional sentence>", "timeout": true, "factor": 5 }.
   spec.mutants is read here only; the page ignores it. */
export const MUTANT_FACTOR = 5;
const firstFail = (r) => (r.error ? `error (${String(r.error).split('\n').slice(-1)[0].slice(0, 80)})` : `test ${r.rows.findIndex((x) => !x.ok) + 1}`);
export const checkCodeWidget = async (runner, spec, byKey = null) => {
  const fails = [], add = (k, d) => fails.push([k, d]), reached = new Set();
  if (!Array.isArray(spec.tests) || !spec.tests.length) return fails;
  let sol = null;
  if (typeof spec.solution === 'string' && spec.solution.trim()) {
    sol = await runner.grade(spec, spec.solution, 'tests');
    if (!sol.ok) add('solution-fails', `the solution fails ${firstFail(sol)}`);
    if (Array.isArray(spec.examples) && spec.examples.length) {
      const ex = await runner.grade(spec, spec.solution, 'examples');
      if (!ex.ok) add('examples-fail', `the solution fails an example: ${firstFail(ex)}`);
    }
  }
  if (typeof spec.starter === 'string' && spec.starter.trim()) {
    const st = await runner.grade(spec, spec.starter, 'tests');
    if (st.ok) add('starter-passes', 'the starter passes every hidden test');
  }
  if (spec.mutants != null && !Array.isArray(spec.mutants)) add('mutant-passes', 'mutants must be an array of { source, test }');
  for (const [i, m] of (Array.isArray(spec.mutants) ? spec.mutants : []).entries()) {
    const at = `mutants[${i}]`;
    if (!m || typeof m.source !== 'string' || !Number.isInteger(m.test) || m.test < 1 || m.test > spec.tests.length) { add('mutant-wrong-test', `${at} needs a source string and test, the 1-based number of the first failing hidden test (1 to ${spec.tests.length})`); continue; }
    const F = m.factor != null ? +m.factor : MUTANT_FACTOR;
    const timed = m.timeout === true;
    if (timed && !(F >= 1)) { add('mutant-thin-margin', `${at}.factor must be a number of at least 1`); continue; }
    const limit = timed && sol ? sol.limits[m.test - 1] : 0;
    const r = await runner.grade(spec, m.source, 'tests', timed ? { capMs: Math.round(limit * F) || undefined } : {});
    if (r.ok) { add('mutant-passes', `${at} passes every hidden test`); continue; }
    const got = r.rows.findIndex((x) => !x.ok) + 1;
    if (r.error) { add('mutant-wrong-test', `${at} stops before the tests (${firstFail(r)}); it should first fail test ${m.test}`); continue; }
    reached.add(got);
    if (got !== m.test) { add('mutant-wrong-test', `${at} first fails test ${got}, not test ${m.test}`); continue; }
    if (timed) {
      if (r.timeoutAt !== m.test - 1) add('mutant-thin-margin', `${at} is marked timeout but test ${m.test} failed on its answer, or finished within ${F} times the limit (${(limit * F / 1000).toFixed(1)} s)`);
      const ms = sol && sol.times[m.test - 1];
      if (ms != null && ms > limit / F) add('mutant-thin-margin', `${at}: the solution takes ${Math.round(ms)} ms on test ${m.test}, more than 1/${F} of its ${limit / 1000} s limit`);
    } else if (r.timeoutAt === m.test - 1) add('mutant-wrong-test', `${at} fails test ${m.test} by running out of time; mark it "timeout": true so its margin is checked`);
  }
  /* ENGINE-BACKLOG 1269: byKey is the parent's feedback.byKey (null: not checked). A test-N line no mutant first fails is never seen; a test a mutant first fails with no line shows only the generic line. */
  if (byKey && typeof byKey === 'object') {
    for (const k of Object.keys(byKey)) { const n = /^test-(\d+)$/.exec(k); if (n && !reached.has(+n[1])) add('feedback-unreachable', `byKey "${k}" is reached by no mutant: no recorded mistake fails test ${n[1]} first`); }
    for (const n of [...reached].sort((a, b) => a - b)) if (!(`test-${n}` in byKey)) add('feedback-missing', `a mutant first fails test ${n} but feedback.byKey has no "test-${n}" line`);
  }
  return fails;
};
