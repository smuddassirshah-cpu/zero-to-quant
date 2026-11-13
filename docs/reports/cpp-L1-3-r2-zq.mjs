/* Node grader for the app's C++ code widgets: the app's own harness text (cpp-grade.js), its exception runtime and WASI
   shim (cpp-worker.js), and the YoWASP clang bundle. usage: node zq.mjs <app dir> <pkgs> <jobs.json> <out.json>
   job: { name, file, path, src? | which: 'solution'|'starter' }  -> { key, rows:[{ok,actual,error,stdout}] }
        { name, prog, flags?, stdin?, argv? }                      -> { ok, diag, out, err, code, trap } */
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import os from 'node:os';
import { spawnSync } from 'node:child_process';
const [APP, PKGS, JOBS, OUTF] = process.argv.slice(2);
const gsrc = fs.readFileSync(path.join(APP, 'js/engine/widgets/cpp-grade.js'), 'utf8');
const wsrc = fs.readFileSync(path.join(APP, 'js/screens/cpp-worker.js'), 'utf8');
const inj = gsrc.replace(/\n  const scriptMode = [^\n]*\n/, (m) => m + '  window.__zq = { unit, same, norm, isOut, scriptMode, raisesRow, parseErr, runError, cleanType, revive, fmt, OUT, SEP, tolOf };\n');
if (inj === gsrc) throw new Error('could not patch cpp-grade.js');
const win = { ZQ: {} };
const ctx = vm.createContext({ window: win, document: {}, console, performance, setTimeout, clearTimeout, navigator: {}, URL, Worker: function () {} });
try { vm.runInContext(inj, ctx); } catch (e) { /* the widget registration needs a DOM; the helpers are already out */ }
const G = win.__zq; if (!G) throw new Error('helpers not exported');
const FLAGS = eval(wsrc.match(/let FLAGS = (\[[^\n]*\]);/)[1]);
const LINK = eval(wsrc.match(/const LINK = (\[[^\n]*\]);/)[1]);
const RUNTIME = wsrc.match(/const RUNTIME = String\.raw`([\s\S]*?)`;/)[1];
const runnerSrc = wsrc.slice(wsrc.indexOf('class WasiExit'), wsrc.indexOf('self.onmessage'));
const TMP = fs.mkdtempSync(path.join(os.tmpdir(), 'zqr2-'));
const RUNJS = path.join(TMP, 'run.mjs');
fs.writeFileSync(RUNJS, `import fs from 'node:fs';
const dec = new TextDecoder();
const collector = () => { const parts = []; return { write: (b) => { if (b && b.length) parts.push(dec.decode(b, { stream: true })); }, text: () => parts.join('') + dec.decode(), peek: () => parts.join('') }; };
${runnerSrc}
const [w, cases] = process.argv.slice(2);
const mod = new WebAssembly.Module(fs.readFileSync(w));
const cs = JSON.parse(fs.readFileSync(cases, 'utf8'));
const k = +process.argv[4];
const r = runOne(mod, cs[k].argv, cs[k].stdin, null);
process.stdout.write(JSON.stringify(r));
`);
const { runClang } = await import(path.join(PKGS, 'yowasp-clang-21.1.4-3/package/gen/bundle.js'));
const dec = new TextDecoder();
const cc = async (args, files) => {
  let diag = '';
  const w = (b) => { if (b && b.length) diag += dec.decode(b); };
  try { const out = await runClang(['clang++', ...args], files, { stdout: w, stderr: w }); return { ok: true, files: out, diag }; }
  catch (e) { return { ok: false, files: {}, diag: diag + (e && typeof e.code === 'number' ? '' : String((e && e.message) || e)) }; }
};
const rt = await cc([...FLAGS, '-c', 'zq_rt.cpp', '-o', 'zq_rt.o'], { 'zq_rt.cpp': RUNTIME });
if (!rt.ok) throw new Error('runtime: ' + rt.diag);
const rtObj = rt.files['zq_rt.o'];
const argsFor = (flags) => { const extra = (flags || []).map(String); let base = [...FLAGS]; const o = extra.filter((f) => /^-O/.test(f)).pop(), std = extra.filter((f) => /^-std=/.test(f)).pop(); if (o) base = base.map((f) => (/^-O/.test(f) ? o : f)); if (std) base = base.map((f) => (/^-std=/.test(f) ? std : f)); return [...base, ...extra.filter((f) => !/^-O|^-std=/.test(f))]; };
const compile = async (src, flags) => { const r = await cc([...argsFor(flags), 'main.cpp', 'zq_rt.o', '-o', 'main.wasm', ...LINK], { 'main.cpp': src, 'zq_rt.o': rtObj }); return { ok: r.ok && !!r.files['main.wasm'], wasm: r.files['main.wasm'], diag: r.diag }; };
let seq = 0;
const runAll = (wasm, cases) => {
  const wf = path.join(TMP, `m${++seq}.wasm`), cf = path.join(TMP, `c${seq}.json`);
  fs.writeFileSync(wf, wasm); fs.writeFileSync(cf, JSON.stringify(cases));
  return cases.map((_, k) => {
    const p = spawnSync(process.execPath, ['--no-warnings', RUNJS, wf, cf, String(k)], { encoding: 'utf8', timeout: 8000, maxBuffer: 1 << 26 });
    if (p.error || p.status !== 0) return { timeout: true, out: '', err: String(p.stderr || p.error), code: -1, trap: null };
    return JSON.parse(p.stdout);
  });
};
const at = (o, p) => p.split('.').filter(Boolean).reduce((a, k) => a[k], o);
const grade = async (spec, src) => {
  const cases = spec.tests || [];
  const script = G.scriptMode(cases);
  const rows = cases.map((c) => ({ raises: c.compare === 'raises', expect: c.expect, out: G.isOut(c), ok: false, actual: null, error: null, stdout: '', compiles: c.compiles != null ? String(c.compiles) : null, tol: G.tolOf(c) }));
  const runIdx = cases.map((c, i) => (c.compiles == null ? i : -1)).filter((i) => i >= 0), probeIdx = cases.map((c, i) => (c.compiles != null ? i : -1)).filter((i) => i >= 0);
  const sub = runIdx.map((i) => cases[i]);
  const u = G.unit(spec, src, sub, script, {});
  const c = await compile(u.src, u.flags);
  if (!c.ok) return { key: 'compile', diag: c.diag.slice(0, 1500), rows: [] };
  const res = runAll(c.wasm, sub.map((cs, j) => (script ? { argv: ['main', ...(cs.argv || [])], stdin: cs.stdin == null ? '' : String(cs.stdin) } : { argv: ['main', String(j)], stdin: '' })));
  res.forEach((r, j) => {
    const i = runIdx[j], row = rows[i];
    if (r.timeout) { row.error = 'timeout'; return; }
    const e = G.parseErr(r.err);
    const kk = script ? -1 : r.out.lastIndexOf(G.OUT);
    row.stdout = kk >= 0 ? r.out.slice(0, kk) : r.out;
    if (!row.out) row.stdout = row.stdout.replace(/\n+$/, '');
    if (kk >= 0) { const line = r.out.slice(kk + G.OUT.length).replace(/\n$/, ''), q = line.indexOf(G.SEP); row.type = G.cleanType(line.slice(0, q)); try { row.value = JSON.parse(line.slice(q + 1), G.revive); row.hasValue = true; } catch { row.value = undefined; } }
    if (row.raises) { G.raisesRow(row, r, e); return; }
    const err = G.runError(r, e);
    if (row.out) { if (err) { row.error = err; return; } const cs = cases[i]; if (cs.match != null) { row.ok = new RegExp(String(cs.match), 'm').test(row.stdout); return; } if (cs.lines) { const want = G.norm(row.expect).split('\n'), have = G.norm(row.stdout).split('\n'); let q = 0; have.forEach((l) => { if (q < want.length && l === want[q]) q++; }); row.ok = q === want.length; return; } row.ok = cs.exact ? row.stdout === String(row.expect) : G.norm(row.stdout) === G.norm(row.expect); return; }
    if (err || !row.hasValue) { row.error = err || 'no value'; return; }
    row.actual = row.type === 'void' ? 'void' : JSON.stringify(row.value);
    row.ok = G.same(row.value, cases[i].expect, cases[i].compare === 'isclose' ? 'isclose' : 'equal', row.tol);
  });
  for (const i of probeIdx) {
    const cs = cases[i], row = rows[i];
    const pu = G.unit(spec, src, [], false, { probe: String(cs.compiles), probeSetup: cs.setup == null ? '' : String(cs.setup) });
    const pc = await compile(pu.src, pu.flags);
    const want = cs.expect !== false && cs.expect !== 'false';
    row.ok = !!pc.ok === want; row.actual = pc.ok ? 'it compiled' : 'it did not compile';
  }
  const first = rows.findIndex((x) => !x.ok);
  const hard = rows.find((x) => x.error && !x.raises);
  return { key: first < 0 ? null : `test-${first + 1}`, fails: rows.map((x, i) => (x.ok ? null : i + 1)).filter(Boolean), rows: rows.map((x) => ({ ok: x.ok, actual: x.actual, error: x.error ? String(x.error).slice(0, 300) : null, stdout: String(x.stdout || '').slice(0, 400) })), diag: c.diag.slice(0, 1500) };
};
const jobs = JSON.parse(fs.readFileSync(JOBS, 'utf8'));
const out = {};
for (const j of jobs) {
  try {
    if (j.prog != null) {
      const c = await compile(j.prog, j.flags || []);
      if (!c.ok) { out[j.name] = { ok: false, diag: c.diag }; continue; }
      const r = runAll(c.wasm, [{ argv: ['main', ...(j.argv || [])], stdin: j.stdin || '' }])[0];
      out[j.name] = { ok: true, diag: c.diag, out: r.out, err: r.err, code: r.code, trap: r.trap, timeout: !!r.timeout };
    } else {
      const d = JSON.parse(fs.readFileSync(path.join(APP, 'content/courses/cpp', j.file + '.json'), 'utf8'));
      const spec = at(d, j.path);
      out[j.name] = await grade(spec, j.src != null ? j.src : spec[j.which || 'solution']);
    }
  } catch (e) { out[j.name] = { exception: String(e && e.stack || e).slice(0, 600) }; }
  fs.writeFileSync(OUTF, JSON.stringify(out, null, 1));
}
fs.rmSync(TMP, { recursive: true, force: true });
