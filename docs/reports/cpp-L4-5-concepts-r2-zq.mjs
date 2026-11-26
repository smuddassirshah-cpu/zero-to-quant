// Node port of the page's C++ grading path, used by cpp-L4-5-concepts-r2-run.mjs (audit cpp-4-5-r2). It is the round 1 auditor's port
// (same code path), reused as tooling only and checked here against every solution and starter of the two levels.
// Node port of the page's C++ grading path: the widget's own unit() (js/engine/widgets/cpp-grade.js, Z.cppCode.lib) builds the
// translation unit, the worker's own FLAGS / LINK / RUNTIME / runOne (js/screens/cpp-worker.js) compile and run it with the
// YoWASP clang 21 from the local CDN. Key as the page gives it: null, compile, test-N.
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { Worker, isMainThread, parentPort, workerData } from 'node:worker_threads';
import { pathToFileURL, fileURLToPath } from 'node:url';

const loadWorkerBits = (app) => {
  let t = fs.readFileSync(path.join(app, 'js/screens/cpp-worker.js'), 'utf8');
  t = t.slice(0, t.indexOf('self.onmessage'));
  const f = new Function('self', 'performance', 'crypto', 'TextDecoder', 'TextEncoder', 'WebAssembly', t + '\n;return { FLAGS, LINK, RUNTIME, runOne, argsFor, cc, set: (c, r) => { clang = c; rtObj = r; } };');
  return f({ postMessage() {} }, performance, globalThis.crypto, TextDecoder, TextEncoder, WebAssembly);
};

if (!isMainThread && workerData && workerData.zqExec) {
  const W = loadWorkerBits(workerData.app);
  parentPort.on('message', async (m) => {
    const mod = await WebAssembly.compile(m.wasm);
    m.cases.forEach((c, i) => {
      const r = W.runOne(mod, ['main', ...(c.argv || []).map(String)], c.stdin == null ? '' : String(c.stdin), null);
      parentPort.postMessage({ i, r });
    });
    parentPort.postMessage({ done: true });
  });
}

export const make = async ({ app, pkgs }) => {
  const g = { console, setTimeout, clearTimeout, document: {}, navigator: {}, location: { href: 'http://x/' }, URL };
  g.window = g; g.globalThis = g; vm.createContext(g);
  g.ZQ = { widgets: { register() {} }, esc: (s) => String(s), h: () => ({}) };
  vm.runInContext(fs.readFileSync(path.join(app, 'js/engine/widgets/cpp-grade.js'), 'utf8'), g);
  const lib = g.ZQ.cppCode.lib;
  const W = loadWorkerBits(app);
  const clang = await import(pathToFileURL(path.join(pkgs, 'yowasp-clang-21.1.4-3/package/gen/bundle.js')).href);
  W.set(clang, null);
  const rt = await W.cc([...W.FLAGS, '-c', 'zq_rt.cpp', '-o', 'zq_rt.o'], { 'zq_rt.cpp': W.RUNTIME });
  if (!rt.ok) throw new Error('runtime: ' + rt.diag);
  const rtObj = rt.files['zq_rt.o'];
  const compile = async (u) => {
    const files = { 'main.cpp': u.src, 'zq_rt.o': rtObj };
    const extra = u.files ? Object.entries(u.files) : [];
    extra.forEach(([k, v]) => { files[k] = String(v); });
    const r = await W.cc([...W.argsFor(u.flags), 'main.cpp', ...extra.filter(([k]) => /\.(cpp|cc)$/.test(k)).map(([k]) => k), 'zq_rt.o', '-o', 'main.wasm', ...W.LINK], files);
    return { ok: r.ok && r.files['main.wasm'] instanceof Uint8Array, wasm: r.files['main.wasm'], diag: r.diag };
  };
  const exec = (wasm, cases, limit) => new Promise((resolve) => {
    const results = new Array(cases.length).fill(null);
    let from = 0, timeout = null;
    const start = () => {
      if (from >= cases.length) return resolve({ results, timeout });
      const w = new Worker(fileURLToPath(import.meta.url), { workerData: { zqExec: true, app } });
      let t = setTimeout(() => { w.terminate(); if (timeout == null) timeout = from; resolve({ results, timeout }); }, limit);
      const base = from;
      w.on('message', (m) => {
        if (m.done) { clearTimeout(t); w.terminate(); return resolve({ results, timeout }); }
        results[base + m.i] = m.r; from = base + m.i + 1;
        clearTimeout(t); t = setTimeout(() => { w.terminate(); if (timeout == null) timeout = from; resolve({ results, timeout }); }, limit);
      });
      w.on('error', (e) => { clearTimeout(t); resolve({ results, timeout, crash: String(e) }); });
      w.postMessage({ wasm: wasm.slice(), cases: cases.slice(base) });
    };
    start();
  });
  // helpers copied in behaviour from cpp-grade.js (closure-private there)
  const OUT = '\u001eZQR', EXC = '\u001eZQX', SEP = '\u001f';
  const cleanType = (t) => String(t || '').replace(/std::__1::/g, 'std::').replace(/std::basic_string<char(?:, std::char_traits<char>, std::allocator<char>)?>/g, 'std::string');
  const plain = (t) => String(t || '').replace(/std::__1::/g, 'std::').replace(/^std::/, '').trim();
  const revive = (k, v) => (v && typeof v === 'object' && !Array.isArray(v) && '$num' in v ? Number(v.$num) : v);
  const parseErr = (err) => {
    const lines = String(err || '').split('\n');
    const at = lines.findIndex(l => l.startsWith(EXC));
    const exc = at >= 0 ? lines[at].slice(EXC.length).split('|').map(cleanType) : null;
    if (at >= 0) lines.splice(at, 1);
    return { exc, text: lines.join('\n').replace(/^\/usr\/include\/c\+\+\/v1\/[^:\s]+:\d+: /gm, '').replace(/\n+$/, '') };
  };
  const runError = (r, e) => {
    if (r.trap) return [e.text, 'TRAP ' + r.trap].filter(Boolean).join('\n');
    if (e.exc || r.code === 134) return e.text || 'uncaught exception';
    if (r.code !== 0) return [e.text, `exit status ${r.code}`].filter(Boolean).join('\n');
    return null;
  };
  const tolOf = (c) => (c && c.tol && typeof c.tol === 'object' && (Number.isFinite(+c.tol.rel) || Number.isFinite(+c.tol.abs)) ? [Math.max(0, +c.tol.rel || 0), Math.max(0, +c.tol.abs || 0)] : c && typeof c.tol === 'number' && c.tol >= 0 ? [0, c.tol] : null);
  const isOut = (c) => c.compiles == null && (c.compare === 'stdout' || (c.call == null && c.expect != null && c.compare == null));
  const excMatch = (names, want) => !!names && names.some(n => plain(n) === plain(want));

  const grade = async (spec, src, which = 'tests') => {
    const cases = spec[which] || [];
    const script = lib.scriptMode(cases);
    const rows = cases.map((c) => ({ ok: false, raises: c.compare === 'raises', expect: c.expect, out: isOut(c), tol: tolOf(c), error: null, actual: null, stdout: '' }));
    const runIdx = cases.map((c, i) => (c.compiles == null ? i : -1)).filter((i) => i >= 0), probeIdx = cases.map((c, i) => (c.compiles != null ? i : -1)).filter((i) => i >= 0);
    const keyOf = (c) => JSON.stringify(c && c.defines && typeof c.defines === 'object' ? c.defines : {});
    const groups = new Map(); runIdx.forEach((i) => { const k = keyOf(cases[i]); if (!groups.has(k)) groups.set(k, []); groups.get(k).push(i); });
    if (!groups.size) groups.set('{}', []);
    const limit = 5000 + (spec.budget != null ? Math.max(0, +spec.budget || 0) : 0);
    let warnings = '';
    for (const [k, idxs] of groups) {
      const sub = idxs.map((i) => cases[i]);
      const u = lib.unit(spec, src, sub, script, { defines: JSON.parse(k) });
      const c = await compile(u);
      if (!c.ok) return { ok: false, key: 'compile', rows, diag: lib.cleanDiag(c.diag) };
      if (/main\.cpp:\d+:\d+: warning/.test(c.diag)) warnings = c.diag;
      if (!sub.length) continue;
      const runs = await exec(c.wasm, sub.map((cs, j) => (script ? { argv: cs.argv || [], stdin: cs.stdin == null ? '' : String(cs.stdin) } : { argv: [String(j)], stdin: '' })), limit);
      runs.results.forEach((r, j) => {
        const i = idxs[j], row = rows[i];
        if (!r) return;
        const e = parseErr(r.err);
        const kk = script ? -1 : r.out.lastIndexOf(OUT);
        row.stdout = kk >= 0 ? r.out.slice(0, kk) : r.out;
        row.ms = Math.round(r.ms);
        if (kk >= 0) {
          const line = r.out.slice(kk + OUT.length).replace(/\n$/, ''), q = line.indexOf(SEP);
          row.type = cleanType(line.slice(0, q));
          try { row.value = JSON.parse(line.slice(q + 1), revive); row.hasValue = true; } catch { row.value = undefined; }
        }
        if (row.raises) {
          const want = row.expect == null ? '' : String(row.expect).trim();
          if (e.exc) { row.ok = want ? excMatch(e.exc, want) : true; row.actual = 'uncaught ' + e.exc[0]; return; }
          if (r.trap) { row.ok = !want; row.actual = 'crash: ' + e.text + ' ' + r.trap; return; }
          if (r.code !== 0) { row.ok = !want; row.actual = `exit ${r.code}`; return; }
          row.ok = false; row.actual = 'no error' + (row.hasValue ? ' value ' + lib.fmt(row.value) : ''); return;
        }
        const err = runError(r, e);
        if (row.out) {
          if (err) { row.error = err; return; }
          const cs = cases[i];
          if (cs.match != null) { let re = null; try { re = new RegExp(String(cs.match), 'm'); } catch { re = null; } row.ok = !!re && re.test(row.stdout); return; }
          if (cs.lines) { const want = lib.norm(row.expect).split('\n'), have = lib.norm(row.stdout).split('\n'); let q = 0; have.forEach((l) => { if (q < want.length && l === want[q]) q++; }); row.ok = q === want.length; return; }
          row.ok = cs.exact ? row.stdout === String(row.expect) : lib.norm(row.stdout) === lib.norm(row.expect);
          if (!row.ok && e.text) row.stderr = e.text;
          return;
        }
        if (err || !row.hasValue) { row.error = err || 'no value'; return; }
        row.actual = row.type === 'void' ? 'void' : lib.fmt(row.value);
        row.ok = lib.same(row.value, cases[i].expect, cases[i].compare === 'isclose' ? 'isclose' : 'equal', row.tol);
      });
      if (runs.timeout != null) {
        const r = rows[idxs[runs.timeout]]; if (r) r.error = 'TIMEOUT';
        idxs.forEach((i, j) => { if (j > runs.timeout && !runs.results[j]) rows[i].error = 'not run'; });
      }
    }
    for (const i of probeIdx) {
      const cs = cases[i], row = rows[i];
      const u = lib.unit(spec, src, [], false, { defines: cs.defines, probe: String(cs.compiles), probeSetup: cs.setup == null ? '' : String(cs.setup) });
      const c = await compile(u);
      const want = cs.expect !== false && cs.expect !== 'false';
      row.ok = !!c.ok === want; row.actual = c.ok ? 'it compiled' : 'it did not compile';
      if (!c.ok) row.detail = lib.cleanDiag(c.diag).split('\n').filter((l) => /error:/.test(l)).slice(0, 2).join(' / ');
    }
    const first = rows.findIndex((x) => !x.ok);
    return { ok: first < 0 && rows.length > 0, key: first < 0 ? null : `test-${first + 1}`, rows, warnings };
  };
  // plain program: compile src as a whole program with the page flags, run with stdin; returns {ok, out, err, code, trap, diag}
  const runProg = async (src, stdin = '', flags = []) => {
    const c = await compile({ src, flags });
    if (!c.ok) return { ok: false, diag: lib.cleanDiag(c.diag) };
    const r = await exec(c.wasm, [{ argv: [], stdin }], 10000);
    const x = r.results[0];
    if (!x) return { ok: true, timeout: true, diag: c.diag };
    return { ok: true, out: x.out, err: parseErr(x.err).text, code: x.code, trap: x.trap, diag: c.diag };
  };
  const cc = (args, files) => W.cc(args, files).then((r) => ({ ok: r.ok, diag: lib.cleanDiag(r.diag) }));
  const ccRaw = (args, files) => W.cc(args, files);
  return { grade, runProg, cc, ccRaw, lib, flags: W.FLAGS };
};

// all code widgets of a content file, with a path string
export const widgetsOf = (file) => {
  const d = JSON.parse(fs.readFileSync(file, 'utf8'));
  const out = [];
  const walk = (o, p) => {
    if (Array.isArray(o)) o.forEach((v, i) => walk(v, `${p}[${i}]`));
    else if (o && typeof o === 'object') {
      if (o.kind === 'code' && Array.isArray(o.tests)) out.push({ path: p, spec: o });
      for (const [k, v] of Object.entries(o)) walk(v, p ? `${p}.${k}` : k);
    }
  };
  walk(d, '');
  return out;
};
