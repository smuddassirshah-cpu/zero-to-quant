// Runs a cpp level 5 problem the way the app does: the app's own unit() builds main.cpp (prelude, learner code, postlude, harness, leakCheck and allocCheck wrappers),
// YoWASP clang 21 (libc++, debug hardening) compiles it, and each test runs as its own WASI process.
// Setup: python3 dump.py ; export ZQ_PKGS=<pkgs folder> ; STD=c++17 node run.mjs P-vec   (STD defaults to c++17)
// usage: node run.mjs <problem-id> [variant ...]   variants: solution starter mut:<name> alt:<name> (default all)
import fs from 'fs';
import { spawnSync } from 'child_process';
import { unit } from './loadunit.mjs';
if (!process.env.ZQ_PKGS) throw new Error('set ZQ_PKGS to the local packages folder (the one holding yowasp-clang-21.1.4-3)');
const PK = process.env.ZQ_PKGS + '/yowasp-clang-21.1.4-3/package/gen/bundle.js';
const { runClang } = await import(PK);
const probs = JSON.parse(fs.readFileSync(new URL('./probs.json', import.meta.url)));
const FLAGS = ['-std=c++17', '-O1', '-D_LIBCPP_HARDENING_MODE=_LIBCPP_HARDENING_MODE_DEBUG', '-fno-color-diagnostics', '-fmessage-length=0', '-ferror-limit=10', '-Wl,--stack-first,-z,stack-size=8388608'];
const RT = `#include <cstdio>\n#include <cstdlib>\nextern "C" void* __cxa_allocate_exception(size_t n) throw() { return std::malloc(n?n:1); }\nextern "C" void __cxa_free_exception(void* p) throw() { std::free(p); }\nextern "C" void __cxa_throw(void*, void*, void(*)(void*)) { std::fputs("THROW\\n", stderr); std::_Exit(134); }\n`;

const id = process.argv[2];
const P = probs[id];
const want = process.argv.slice(3);
const variants = { solution: P.solution, starter: P.starter };
for (const [k, v] of Object.entries(P.mutants || {})) variants['mut:' + k] = v;
for (const [k, v] of Object.entries(P.alts || {})) variants['alt:' + k] = v;
for (const [k, v] of Object.entries(P.uncaught || {})) variants['unc:' + k] = v;
const run = want.length ? want : Object.keys(variants);
const std = process.env.STD || 'c++17';
const TMP = (process.env.TMPDIR || '/tmp') + '/';
const same = (a, e) => (typeof e === 'number' ? typeof a === 'number' && (a === e || Math.abs(a - e) <= 1e-9 * Math.max(Math.abs(a), Math.abs(e)) + 1e-12) : a === e);
const spec = { prelude: P.prelude || '', postlude: P.postlude || '', allocCheck: !!P.alloc, leakCheck: !!P.leak, language: 'cpp' };
const cases = P.tests.filter(t => !t.compiles);
for (const name of run) {
  const code = variants[name];
  const u = unit(spec, code, cases, false);
  const files = { 'main.cpp': u.src + '\n', 'rt.cpp': RT };
  let wasm, diag = '';
  const t0 = Date.now();
  try {
    const out = await runClang(['clang++', ...FLAGS.map(f => f.replace('c++17', std)), ...u.flags, 'main.cpp', 'rt.cpp', '-o', 'a.wasm'], files, { stdout: b => b && (diag += Buffer.from(b)), stderr: b => b && (diag += Buffer.from(b)) });
    wasm = out['a.wasm'];
  } catch (e) { console.log(`[${id}] ${name}: COMPILE ERROR\n${diag.slice(0, 1500)}`); continue; }
  const wf = TMP + 'zq_' + process.pid + '.wasm'; fs.writeFileSync(wf, wasm);
  let failed = 0; const lines = [];
  for (let i = 0; i < cases.length; i++) {
    const c = cases[i];
    const of = TMP + 'zq_o_' + process.pid, ef = TMP + 'zq_e_' + process.pid;
    const r = spawnSync('node', ['--no-warnings', new URL('./runcase.mjs', import.meta.url).pathname, wf, String(i), of, ef], { timeout: 20000 });
    const code2 = r.status === null ? 'signal ' + r.signal : r.status;
    const o = fs.readFileSync(of, 'utf8'), er = fs.readFileSync(ef, 'utf8');
    let ok = false, actual = '';
    const m = o.indexOf('\x1eZQR');
    if (code2 === 0 && m >= 0) {
      const body = o.slice(m + 4).trim(); const k = body.indexOf('\x1f');
      let v; try { v = JSON.parse(body.slice(k + 1)); } catch (e) { v = body; }
      actual = JSON.stringify(v); ok = same(v, c.expect);
    } else actual = `exit ${code2} ${er.slice(0, 120).replace(/\n/g, ' ')}`;
    if (!ok) { failed++; lines.push(`  FAIL ${i}: ${(c.setup || '').slice(0, 70)} ${c.call.slice(0, 60)} expected ${JSON.stringify(c.expect)} got ${actual.slice(0, 100)}`); }
  }
  // `compiles` cases: the snippet must not compile (expect false), as the app's compile checks run it
  for (const t of P.tests.filter(t => t.compiles)) {
    const pu = unit(spec, code, [], false, { probe: t.compiles, probeSetup: t.setup || '' });
    let compiled = true;
    try { await runClang(['clang++', ...FLAGS.map(f => f.replace('c++17', std)).filter(f => !f.startsWith('-Wl,')), ...pu.flags, '-fsyntax-only', 'main.cpp'], { 'main.cpp': pu.src + '\n' }, { stdout: () => {}, stderr: () => {} }); } catch (e) { compiled = false; }
    if (compiled !== t.expect) { failed++; lines.push(`  FAIL compile check: ${t.compiles.slice(0, 60)} compiled=${compiled}`); }
  }
  console.log(`[${id}] ${std} ${name}: ${failed} of ${P.tests.length} failed (${((Date.now() - t0) / 1000).toFixed(0)} s)`);
  if (name === 'solution' && failed || process.env.V) console.log(lines.join('\n'));
}
