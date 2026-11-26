#!/usr/bin/env python3
"""Concept checks for the blind audit cpp-4-5 (course cpp, levels 4 and 5; docs/reviews/audit-cpp-4-5.md).

Every C++ claim is compiled by the page's own compiler and flags: YoWASP clang 21 for wasm32 from the local CDN,
with FLAGS, LINK, the exception runtime and the WASI shim read out of app/js/screens/cpp-worker.js, and the
translation unit built by the widget's own unit() (app/js/engine/widgets/cpp-grade.js). Code widgets are graded
the way the page grades them (key null, compile or test-N). Nothing here is native clang.

Usage:  python3 docs/reports/cpp-L4-5-concepts.py [--pkgs <local-cdn>] [--dump] [--jobs 4]
        <local-cdn> holds yowasp-clang-21.1.4-3/package (default: $ZQ_PKGS, else the session scratchpad pkgs).
Exit 0 when every check holds. A check that fails because the content is wrong is listed as KNOWN-FINDING and
keeps the exit status non-zero until the content is fixed (auditor brief, step 4).

Fix pass (Opus fixer, after commit 7bc79413): checks that encoded the old content text were re-pointed to the new text,
each marked `# re-pointed (fix pass, finding N)`; codings whose expected key changed with a new or changed hidden test
carry the same mark, and new codings for the fix pass's test-N lines and hidden tests are marked `# fix pass`.
Fix pass of audit cpp-4-5-r2: one coding re-pointed (`l18s9.pin_only`, now stopped by planted bug 3 at test-4), marked inline.
"""
import json, math, os, shutil, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
APP = os.path.normpath(os.path.join(HERE, '..', '..', 'app'))
CPP = os.path.join(APP, 'content', 'courses', 'cpp')
ARGS = sys.argv[1:]
def opt(name, default=None):
    return ARGS[ARGS.index(name) + 1] if name in ARGS else default
PKGS = opt('--pkgs') or os.environ.get('ZQ_PKGS') or '/tmp/claude-0/-home-user-zero-to-quant/bb925a25-4e45-5436-9525-d6e3fcf91a82/scratchpad/pkgs'
DUMP = '--dump' in ARGS
NJOBS = int(opt('--jobs', '4'))
ONLY = opt('--only')

RUNNER_JS = r'''
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
  return { grade, runProg, cc, lib };
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

// ---- driver: node runner.mjs <app> <pkgs> <jobs.json> <out.json>
if (isMainThread && process.argv[4]) {
  const [app, pkgs, jobsFile, outFile] = process.argv.slice(2);
  const G = await make({ app, pkgs });
  const jobs = JSON.parse(fs.readFileSync(jobsFile, 'utf8'));
  const out = {};
  const cache = new Map();
  for (const j of jobs) {
    try {
      if (j.kind === 'prog') out[j.name] = await G.runProg(j.src, j.stdin || '', j.flags || []);
      else if (j.kind === 'cc') out[j.name] = await G.cc(j.args, j.files);
      else if (j.kind === 'grade') {
        const f = path.join(app, 'content/courses/cpp', j.file);
        if (!cache.has(f)) cache.set(f, widgetsOf(f));
        const w = cache.get(f).find((x) => x.path === j.path);
        if (!w) { out[j.name] = { fail: 'no widget at ' + j.path }; continue; }
        const src = j.src === '@solution' ? w.spec.solution : j.src === '@starter' ? (w.spec.starter || '') : j.src;
        const r = await G.grade(w.spec, src);
        out[j.name] = { key: r.key, ok: r.ok, diag: (r.diag || '').slice(0, 1500), rows: r.rows.map((x) => ({ ok: x.ok, actual: x.actual == null ? null : String(x.actual).slice(0, 200), error: x.error ? String(x.error).slice(0, 400) : null, stdout: (x.stdout || '').slice(0, 300) })) };
      }
    } catch (e) { out[j.name] = { fail: String((e && e.stack) || e).slice(0, 600) }; }
  }
  fs.writeFileSync(outFile, JSON.stringify(out));
  process.exit(0);
}
'''

JOBS = []
def prog(name, src, stdin='', flags=None):
    JOBS.append({'kind': 'prog', 'name': name, 'src': src, 'stdin': stdin, 'flags': flags or []})
def grade(name, file, path, src):
    JOBS.append({'kind': 'grade', 'name': name, 'file': file, 'path': path, 'src': src})
def cc(name, args, src):
    JOBS.append({'kind': 'cc', 'name': name, 'args': args, 'files': {'t.cpp': src}})

def run_jobs():
    if not os.path.isdir(os.path.join(PKGS, 'yowasp-clang-21.1.4-3', 'package', 'gen')):
        print('FAIL: no YoWASP clang under', PKGS, '(pass --pkgs <local-cdn>)'); sys.exit(2)
    jobs = [j for j in JOBS if not ONLY or ONLY in j['name']]
    tmp = tempfile.mkdtemp(prefix='cpp45-')
    runner = os.path.join(tmp, 'runner.mjs')
    open(runner, 'w').write(RUNNER_JS)
    procs = []
    for k in range(NJOBS):
        part = jobs[k::NJOBS]
        if not part: continue
        jf, of = os.path.join(tmp, f'jobs{k}.json'), os.path.join(tmp, f'out{k}.json')
        json.dump(part, open(jf, 'w'))
        procs.append((subprocess.Popen(['node', runner, APP, PKGS, jf, of], stdout=subprocess.DEVNULL, stderr=subprocess.PIPE), of))
    res = {}
    for p, of in procs:
        err = p.communicate()[1].decode('utf8', 'replace')
        if p.returncode != 0 or not os.path.exists(of):
            print('FAIL: the node runner stopped:', err[-800:]); sys.exit(2)
        res.update(json.load(open(of)))
    shutil.rmtree(tmp, ignore_errors=True)
    return res

def kv(r):
    """key=value lines a program printed, as a dict of strings"""
    out = {}
    for line in (r.get('out') or '').split('\n'):
        if '=' in line:
            k, v = line.split('=', 1); out[k.strip()] = v.strip()
    return out

CHECKS = []
def check(name, cond, note='', finding=None):
    """finding: the audit finding number when the check is expected to fail because the content is wrong"""
    CHECKS.append((name, bool(cond), note, finding))

# ---------------------------------------------------------------------------------------------------------------
# 1. Programs: each prints key=value lines under the page's compiler (wasm32, -std=c++17 -O1, libc++ hardening)
# ---------------------------------------------------------------------------------------------------------------
prog('vec', r'''
#include <vector>
#include <cstdio>
#include <cstddef>
int main() {
  std::vector<double> v; int moves = 0, allocs = 0; long copied = 0;
  std::printf("caps=");
  for (int i = 0; i < 600; ++i) {
    std::size_t before = v.capacity(), sz = v.size();
    v.push_back(1.0);
    if (v.capacity() != before) { ++allocs; if (before) { ++moves; copied += (long)sz; } if (i < 8) std::printf("%zu,", v.capacity()); }
  }
  std::printf("\nmoves=%d\ncopied=%ld\nallocs=%d\ncap600=%zu\n", moves, copied, allocs, v.capacity());
  std::vector<double> t; t.reserve(1000); std::size_t c0 = t.capacity(), s0 = t.size(); const double* d0 = t.data();
  for (int i = 0; i < 600; ++i) t.push_back(1);
  std::printf("res_cap=%zu\nres_size0=%zu\nres_same=%d\n", c0, s0, (int)(d0 == t.data()));
  std::vector<double> p5; std::printf("caps5=");
  for (int i = 0; i < 5; ++i) { p5.push_back(i); std::printf("%zu,", p5.capacity()); }
  std::vector<double> r5; r5.reserve(5); for (int i = 0; i < 5; ++i) r5.push_back(i);
  std::printf("\ncapr5=%zu\n", r5.capacity());
  std::vector<double> h; h.reserve(100); std::size_t h0 = h.capacity(); for (int i = 0; i < 150; ++i) h.push_back(i);
  std::printf("h100=%zu\nh150=%zu\n", h0, h.capacity());
  std::vector<double> z(3); z.push_back(101.5); std::printf("zsize=%zu\nz0=%g\n", z.size(), z[0]);
  std::vector<double> e; std::printf("wrap=%zu\n", e.size() - 1);
  std::vector<double> xs(3); int n = 4; std::printf("size_minus_n_plus_1=%zu\n", xs.size() - n + 1);
  n = 5; std::printf("size_minus_5_plus_1=%zu\n", xs.size() - n + 1);
  n = 4; std::printf("size_minus_n=%zu\n", xs.size() - n);
  std::printf("sizeof_size_t=%zu\nsizeof_int=%zu\nsizeof_long=%zu\nsizeof_ptr=%zu\nsizeof_ll=%zu\n", sizeof(std::size_t), sizeof(int), sizeof(long), sizeof(void*), sizeof(long long));
  std::vector<double> six(6, 1.0), out6; for (int i = 1; i < 6; ++i) out6.push_back(1); std::printf("cap_no_reserve_5=%zu\n", out6.capacity());
  std::vector<double> px{100.0, 101.5, 99.8, 102.3}; double total = 0;
  for (auto it = px.begin() + 1; it != px.end(); ++it) total += *it;
  std::printf("iter_total=%.10g\n", total);
  std::vector<double> c3{101.5, 102.0, 100.8};
  std::printf("first=%zu %g\n", c3.size(), c3[1]);
}
''')

prog('erase_loop', r'''
#include <vector>
#include <cstdio>
int main() {
  std::vector<double> ticks{101.2, 0.0, 0.0, 101.5};
  for (auto it = ticks.begin(); it != ticks.end(); ++it) { if (*it == 0.0) { ticks.erase(it); } }
  std::printf("ticks=");
  for (double t : ticks) std::printf("%g,", t);
  std::printf("\n");
  std::vector<double> f{101.2, 0.0, 0.0, 101.5};
  for (auto it = f.begin(); it != f.end(); ) { if (*it == 0.0) it = f.erase(it); else ++it; }
  std::printf("fixed=");
  for (double t : f) std::printf("%g,", t);
  std::printf("\n");
  std::vector<double> g{1, -2, -3, 4};
  for (std::size_t i = 0; i < g.size(); ++i) { if (g[i] < 0) g.erase(g.begin() + i); }
  std::printf("idx=");
  for (double t : g) std::printf("%g,", t);
  std::printf("\n");
}
''')

prog('idx_oob', r'''
#include <vector>
#include <cstdio>
int main() { std::vector<double> px{100.0, 101.5, 99.8}; volatile int i = 3; std::printf("before=1\n"); std::fflush(stdout); std::printf("v=%g\n", px[i]); }
''')
prog('at_oob', r'''
#include <vector>
#include <iostream>
int main() { std::vector<double> px{100.0, 101.5, 99.8}; std::cout << "before=1" << std::endl; std::cout << px.at(3) << '\n'; }
''')
prog('at_neg', r'''
#include <vector>
#include <iostream>
int main() { std::vector<double> px{100.0, 101.5, 99.8}; volatile int k = -1; std::cout << "before=1" << std::endl; std::cout << px.at(k) << '\n'; }
''')
prog('reserve_wrap', r'''
#include <vector>
#include <cstdio>
int main() { std::vector<double> px, out; std::printf("before=1\n"); std::fflush(stdout); out.reserve(px.size() - 1); std::printf("after=1\n"); }
''')
prog('ctor_wrap', r'''
#include <vector>
#include <cstdio>
int main() { std::vector<double> px; std::printf("before=1\n"); std::fflush(stdout); std::vector<double> out(px.size() - 1); std::printf("after=%zu\n", out.size()); }
''')

prog('maps', r'''
#include <map>
#include <unordered_map>
#include <string>
#include <cstdio>
#include <iostream>
#include <iomanip>
int main() {
  std::map<std::string, int> pos; pos["VOD"] = 500; pos["BARC"] = -200; pos["AZN"] = 50;
  std::cout << "order=";
  for (const auto& [sym, qty] : pos) std::cout << sym << ',';
  std::cout << '\n';
  std::map<std::string, int> p2{{"VOD", 500}, {"BARC", -200}};
  bool flat = p2["AZN"] == 0;
  std::cout << "flat=" << flat << "\nsize_after_read=" << p2.size() << '\n';
  std::map<std::string, int> p3{{"VOD", 500}}; auto r = p3.insert({"VOD", 600});
  std::cout << "after_insert=" << p3.at("VOD") << "\ninserted=" << r.second << '\n';
  p3.emplace("VOD", 700); std::cout << "after_emplace=" << p3.at("VOD") << '\n';
  std::map<double, int> bids; double best = 100.1; bids[best] += 500; bids[best + 0.1] += 300; bids[100.2] += 200;
  std::cout << "levels=" << bids.size() << '\n' << std::setprecision(17) << "sum=" << best + 0.1 << "\nlit=" << 100.2 << '\n';
  std::map<std::string, int> m; m["VOD"]; int c = m.count("BARC");
  std::cout << "r4count=" << m.size() << ' ' << c << ' ' << m["VOD"] << '\n';
  std::map<std::string, int> em; std::cout << "empty_begin_is_end=" << (em.begin() == em.end()) << '\n';
  std::unordered_map<std::string, int> u; u["VOD"] = 1; u["BARC"] = 2; u["AZN"] = 3;
  std::cout << "uorder=";
  for (const auto& kv : u) std::cout << kv.first << ',';
  std::cout << '\n';
  std::unordered_map<std::string, int> u2; u2["CBOE"]; u2["LSE"]; u2["TURQ"];
  std::cout << "uorder2=";
  for (const auto& kv : u2) std::cout << kv.first << ',';
  std::cout << '\n';
  std::map<std::string, int> q; q["AZN"] += 300; q["AZN"] += -300; std::cout << "flat_key_stays=" << q.size() << '\n';
}
''')

prog('algos', r'''
#include <algorithm>
#include <numeric>
#include <vector>
#include <cmath>
#include <cstdio>
#include <type_traits>
struct Strat { const char* n; double sharpe; };
int main() {
  std::vector<double> pnl{120.5, -40.25, 75.0, -10.5, 30.25};
  auto ti = std::accumulate(pnl.begin(), pnl.end(), 0);
  auto td = std::accumulate(pnl.begin(), pnl.end(), 0.0);
  std::printf("acc_int=%d\nacc_dbl=%.10g\nacc_int_is_int=%d\n", ti, td, (int)std::is_same_v<decltype(ti), int>);
  int run = 0; std::printf("steps=");
  for (double x : pnl) { run = run + x; std::printf("%d,", run); }
  std::printf("\n");
  std::vector<double> fees{2.5, 2.5, 2.5, 2.5};
  std::printf("fees=%d\n", std::accumulate(fees.begin(), fees.end(), 0));
  std::vector<double> rets{0.01, -0.03, 0.025, -0.005, 0.04}; double limit = 0.02;
  auto big = [limit](double r) { return std::abs(r) > limit; };
  limit = 0.05;
  std::printf("count_snapshot=%d\n", (int)std::count_if(rets.begin(), rets.end(), big));
  std::printf("count_ref=%d\n", (int)std::count_if(rets.begin(), rets.end(), [&limit](double r) { return std::abs(r) > limit; }));
  std::vector<double> px{100, 104, 101, 106, 103}, d(px.size());
  std::adjacent_difference(px.begin(), px.end(), d.begin());
  std::printf("adj=");
  for (double x : d) std::printf("%g,", x);
  std::vector<double> day{50, -20, 35}, cum(3), dd(3);
  std::partial_sum(day.begin(), day.end(), cum.begin());
  std::adjacent_difference(day.begin(), day.end(), dd.begin());
  std::printf("\npartial=%g,%g,%g\nadjdiff=%g,%g,%g\n", cum[0], cum[1], cum[2], dd[0], dd[1], dd[2]);
  std::vector<double> a{100, 101, 102}, q{200, 100, 100};
  std::printf("inner=%.10g\n", std::inner_product(a.begin(), a.end(), q.begin(), 0.0));
  std::vector<Strat> s{{"ca", 0.6}, {"mr", 1.9}, {"va", 0.9}, {"mo", 1.4}, {"tr", 1.1}};
  std::sort(s.begin(), s.end(), [](const Strat& x, const Strat& y) { return x.sharpe > y.sharpe; });
  std::printf("sorted=");
  for (auto& x : s) std::printf("%s,", x.n);
  std::vector<double> empty;
  std::printf("\nmax_empty_is_end=%d\n", (int)(std::max_element(empty.begin(), empty.end()) == empty.end()));
  std::sort(empty.begin(), empty.end());
  std::vector<double> daily{120, -50, -100, 80, -60, 200}, c2(daily.size());
  std::partial_sum(daily.begin(), daily.end(), c2.begin());
  double peak = 0, worst = 0;
  std::for_each(c2.begin(), c2.end(), [peak, worst](double c) mutable { peak = std::max(peak, c); worst = std::max(worst, peak - c); });
  std::printf("mutable_copy_worst=%g\n", worst);
  std::for_each(c2.begin(), c2.end(), [&peak, &worst](double c) { peak = std::max(peak, c); worst = std::max(worst, peak - c); });
  std::printf("ref_worst=%g\n", worst);
  double zero = 0.0; volatile double vz = 0.0; double nan = zero / vz; std::printf("zero_over_zero_is_nan=%d\n", (int)(nan != nan));
}
''')
prog('transform_empty', r'''
#include <algorithm>
#include <vector>
#include <cstdio>
int main() {
  std::vector<double> px{100.0, 102.0, 99.0};
  std::vector<double> pence;
  std::printf("begin_is_null=%d\n", (int)(pence.data() == nullptr)); std::fflush(stdout);
  std::transform(px.begin(), px.end(), pence.begin(), [](double p) { return p * 100; });
  std::printf("size_after=%zu\nalive=1\n", pence.size());
}
''')
prog('max_empty_deref', r'''
#include <algorithm>
#include <vector>
#include <iostream>
int main() {
  std::vector<double> pnl;
  std::cout << "before=1" << std::endl;
  auto it = std::max_element(pnl.begin(), pnl.end());
  std::cout << "v=" << *it << '\n';
  std::cout << "after=1" << std::endl;
}
''')
prog('sort_le3', r'''
#include <algorithm>
#include <vector>
#include <cstdio>
int main() {
  std::vector<double> px{100.5, 100.5, 99.8};
  std::printf("before=1\n"); std::fflush(stdout);
  std::sort(px.begin(), px.end(), [](double a, double b) { return a <= b; });
  std::printf("out=%g,%g,%g\nafter=1\n", px[0], px[1], px[2]);
}
''')
prog('sort_le_many', r'''
#include <algorithm>
#include <vector>
#include <cstdio>
int main() {
  for (int n : {6, 30, 200, 2000}) {
    std::vector<double> px(n, 100.5);
    std::printf("n%d_before=1\n", n); std::fflush(stdout);
    std::sort(px.begin(), px.end(), [](double a, double b) { return a <= b; });
    std::printf("n%d_after=1\n", n); std::fflush(stdout);
  }
}
''')
prog('sort_le_int', r'''
#include <algorithm>
#include <vector>
#include <cstdio>
int main() {
  for (int n : {6, 30, 200, 2000}) {
    std::vector<int> v(n, 7);
    std::printf("n%d_before=1\n", n); std::fflush(stdout);
    std::sort(v.begin(), v.end(), [](int a, int b) { return a <= b; });
    std::printf("n%d_after=1\n", n); std::fflush(stdout);
  }
}
''')
cc('capture_by_value_assign', ['-std=c++17', '-fsyntax-only', 't.cpp'], r'''
#include <algorithm>
#include <vector>
double f(const std::vector<double>& cum) {
  double peak = 0, worst = 0;
  std::for_each(cum.begin(), cum.end(), [peak, worst](double c) { peak = std::max(peak, c); worst = std::max(worst, peak - c); });
  return worst;
}
''')
cc('const_map_index', ['-std=c++17', '-fsyntax-only', 't.cpp'], r'''
#include <map>
#include <string>
double last_price(const std::map<std::string, double>& px, const std::string& sym) { return px[sym]; }
''')
cc('map_by_value_index', ['-std=c++17', '-fsyntax-only', 't.cpp'], r'''
#include <map>
#include <string>
double last_price(std::map<std::string, double> px, const std::string& sym) { return px[sym]; }
''')
cc('find_eq_nullptr', ['-std=c++17', '-fsyntax-only', 't.cpp'], r'''
#include <unordered_map>
#include <string>
bool f() { std::unordered_map<std::string, double> px{{"VOD", 0.72}}; auto it = px.find("BARC"); return it == nullptr; }
''')
cc('data_ok', ['-std=c++17', '-fsyntax-only', 't.cpp'], r'''
#include <vector>
#include <cstddef>
double pv(const double* cf, std::size_t n);
double f(std::vector<double>& cf) { return pv(cf.data(), cf.size()) + pv(&cf[0], cf.size()); }
''')
cc('addr_of_vector', ['-std=c++17', '-fsyntax-only', 't.cpp'], r'''
#include <vector>
#include <cstddef>
double pv(const double* cf, std::size_t n);
double f(std::vector<double>& cf) { return pv(&cf, cf.size()); }
''')
cc('vector_as_pointer', ['-std=c++17', '-fsyntax-only', 't.cpp'], r'''
#include <vector>
#include <cstddef>
double pv(const double* cf, std::size_t n);
double f(std::vector<double>& cf) { return pv(cf, cf.size()); }
''')
cc('vector_of_refs', ['-std=c++17', '-fsyntax-only', 't.cpp'], r'''
#include <vector>
struct Payoff { virtual ~Payoff() = default; };
std::vector<Payoff&> v;
void g() { Payoff p; v.push_back(p); }
''')
cc('size_t_countdown', ['-std=c++17', '-fsyntax-only', '-Wall', '-Wextra', 't.cpp'], r'''
#include <vector>
#include <cstddef>
double f(const std::vector<double>& v) { double s = 0; for (std::size_t i = v.size() - 1; i >= 0; --i) s += v[i]; return s; }
''')

prog('doubles', r'''
#include <cstdio>
#include <cmath>
#include <vector>
#include <algorithm>
#include <numeric>
double norm_cdf(double x) { return 0.5 * std::erfc(-x / std::sqrt(2.0)); }
double bs(double S, double K, double r, double sig, double T) {
  double d1 = (std::log(S / K) + (r + 0.5 * sig * sig) * T) / (sig * std::sqrt(T)), d2 = d1 - sig * std::sqrt(T);
  return S * norm_cdf(d1) - K * std::exp(-r * T) * norm_cdf(d2);
}
double crr(double S, double K, double r, double sigma, double T, int n) {
  double dt = T / n, u = std::exp(sigma * std::sqrt(dt)), d = 1 / u, disc = std::exp(-r * dt), p = (std::exp(r * dt) - d) / (u - d);
  std::vector<double> val(n + 1);
  for (int j = 0; j <= n; ++j) val[j] = std::max(S * std::pow(u, n - j) * std::pow(d, j) - K, 0.0);
  for (int i = n - 1; i >= 0; --i) for (int j = 0; j <= i; ++j) val[j] = disc * (p * val[j] + (1 - p) * val[j + 1]);
  return val[0];
}
int main() {
  volatile double a = 110.0, b = 100.0, one = 1.0;
  double r = a / b - one;
  std::printf("rise=%.17g\nrise_eq_01=%d\nrise_close=%d\n", r, (int)(r == 0.1), (int)(std::fabs(r - 0.1) <= 1e-12));
  volatile double p1 = 10.1, p2 = 10.2, two = 2.0;
  double m = (p1 + p2) / two;
  std::printf("mid=%.17g\nmid_eq=%d\n", m, (int)(m == 10.15));
  std::vector<double> px{10.1, 10.2}, q{1, 1};
  double vw = std::inner_product(px.begin(), px.end(), q.begin(), 0.0) / std::accumulate(q.begin(), q.end(), 0.0);
  std::printf("vwap_eq=%d\n", (int)(vw == 10.15));
  volatile double h = 100.1, t = 0.1;
  std::printf("tick_sum=%.17g\ntick_eq=%d\n", h + t, (int)(h + t == 100.2));
  std::printf("bs=%.9f\ncrr100=%.9f\ncrr99=%.9f\ncrr2000=%.9f\ncrr1999=%.9f\n", bs(100, 100, 0.05, 0.2, 1), crr(100, 100, 0.05, 0.2, 1, 100), crr(100, 100, 0.05, 0.2, 1, 99), crr(100, 100, 0.05, 0.2, 1, 2000), crr(100, 100, 0.05, 0.2, 1, 1999));
  std::printf("bs_r0=%.9f\n", bs(100, 100, 0.0, 0.2, 1));
  std::printf("neg7_div_2=%d\nseven_div_2=%d\n", -7 / 2, 7 / 2);
  std::printf("df=%.16g\nfwd=%.14f\npv3=%.14f\npv1=%.14f\n", std::exp(-0.05 * 2), 100 * std::exp(0.05), 5 * std::exp(-0.04) + 5 * std::exp(-0.08) + 105 * std::exp(-0.12), 100 * std::exp(-0.015));
}
''')
# ---- level 5 -------------------------------------------------------------------------------------------------
TRACKED = r'''
#include <vector>
#include <cstdio>
#include <utility>
#include <type_traits>
struct Tracked {
  static inline int copies = 0, moves = 0;
  int v;
  explicit Tracked(int x) : v(x) {}
  Tracked(const Tracked& o) : v(o.v) { ++copies; }
  Tracked(Tracked&& o) NOEX : v(o.v) { ++moves; }
  Tracked& operator=(const Tracked& o) { v = o.v; ++copies; return *this; }
  Tracked& operator=(Tracked&& o) NOEX { v = o.v; ++moves; return *this; }
};
static void show(const char* k) { std::printf("%s=%d,%d\n", k, Tracked::copies, Tracked::moves); Tracked::copies = Tracked::moves = 0; }
'''
prog('tracked', '#define NOEX noexcept\n' + TRACKED + r'''
Tracked make() { return Tracked(1); }
void take(Tracked) {}
Tracked ret_plain() { Tracked t(1); return t; }
Tracked ret_move() { Tracked t(1); return std::move(t); }
int main() {
  std::vector<Tracked> v; v.reserve(8);
  Tracked a(1); show("l1");
  Tracked b = a; show("l2");
  Tracked c = std::move(a); show("l3");
  Tracked d = make(); show("l4");
  take(b); show("l5");
  take(std::move(b)); show("l6");
  take(Tracked(2)); show("l7");
  v.push_back(c); show("l8");
  (void)d;
  Tracked e(5); std::move(e); show("cast_only");
  { std::vector<Tracked> w; std::printf("caps="); for (int i = 1; i <= 4; ++i) { w.push_back(Tracked(i)); std::printf("%zu,", w.capacity()); } std::printf("\n"); show("four_pushes"); }
  const Tracked k(9);
  Tracked m = std::move(k); show("const_move");
  take(k); show("take_const");
  take(std::move(k)); show("take_move_const");
  take(Tracked(3)); show("take_temp");
  { Tracked x = ret_plain(); (void)x; } show("ret_plain");
  { Tracked x = ret_move(); (void)x; } show("ret_move");
  { std::vector<Tracked> w; w.reserve(4); for (int i = 0; i < 4; ++i) w.emplace_back(i); show("emplace_reserved"); }
  std::printf("nothrow=%d\n", (int)std::is_nothrow_move_constructible_v<Tracked>);
}
''')
prog('tracked_throwing', '#define NOEX\n' + TRACKED + r'''
struct MoveOnly {
  static inline int moves = 0;
  MoveOnly() = default;
  MoveOnly(MoveOnly&&) { ++moves; }
};
int main() {
  { std::vector<Tracked> w; for (int i = 1; i <= 2; ++i) w.push_back(Tracked(i)); show("two_pushes"); }
  { std::vector<Tracked> w; for (int i = 1; i <= 4; ++i) w.push_back(Tracked(i)); show("four_pushes"); }
  { std::vector<Tracked> w; for (int i = 1; i <= 4; ++i) w.emplace_back(i); show("four_emplace"); }
  { std::vector<Tracked> w; w.reserve(4); for (int i = 1; i <= 4; ++i) w.push_back(Tracked(i)); show("four_reserved"); }
  { std::vector<MoveOnly> w; for (int i = 0; i < 4; ++i) w.push_back(MoveOnly()); std::printf("move_only_throwing_moves=%d\n", MoveOnly::moves); }
  std::printf("nothrow=%d\n", (int)std::is_nothrow_move_constructible_v<Tracked>);
}
''')

# special members: a member M counts what runs; each class declares exactly what the row says
SPECIAL = r'''
#include <cstdio>
#include <utility>
#include <type_traits>
#include <string>
#include <vector>
#include <memory>
struct M {
  static inline int copies = 0, moves = 0;
  M() = default;
  M(const M&) { ++copies; }
  M(M&&) noexcept { ++moves; }
  M& operator=(const M&) { ++copies; return *this; }
  M& operator=(M&&) noexcept { ++moves; return *this; }
};
struct Nothing { M m; };
struct Dtor { M m; ~Dtor() {} };
struct CopyCtor { M m; CopyCtor() = default; CopyCtor(const CopyCtor& o) : m(o.m) {} };
struct CopyAssign { M m; CopyAssign& operator=(const CopyAssign& o) { m = o.m; return *this; } };
struct MoveCtor { M m; MoveCtor() = default; MoveCtor(MoveCtor&& o) noexcept : m(std::move(o.m)) {} };
struct MoveAssign { M m; MoveAssign& operator=(MoveAssign&& o) noexcept { m = std::move(o.m); return *this; } };
struct AllFive { M m; AllFive() = default; ~AllFive() = default; AllFive(const AllFive&) = default; AllFive& operator=(const AllFive&) = default; AllFive(AllFive&&) = default; AllFive& operator=(AllFive&&) = default; };
template <class T> const char* what() { const char* r = M::moves ? "move" : M::copies ? "copy" : "none"; M::copies = M::moves = 0; return r; }
template <class T> void row(const char* name) {
  std::printf("%s=", name);
  if constexpr (std::is_copy_constructible_v<T>) { T a; T b(a); std::printf("%s,", what<T>()); } else std::printf("error,");
  if constexpr (std::is_move_constructible_v<T>) { T a; T b(std::move(a)); std::printf("%s,", what<T>()); } else std::printf("error,");
  if constexpr (std::is_copy_assignable_v<T>) { T a, b; b = a; std::printf("%s,", what<T>()); } else std::printf("error,");
  if constexpr (std::is_move_assignable_v<T>) { T a, b; b = std::move(a); std::printf("%s", what<T>()); } else std::printf("error");
  std::printf("\n");
}
struct Fill {};
struct Pos { std::string sym; std::vector<int> lots; Pos(Pos&&) = default; Pos(const Pos&) = default; };
struct Pos3 { std::string sym; std::vector<int> lots; Pos3(Pos3&& o) : sym(std::move(o.sym)), lots(std::move(o.lots)) {} };
struct Pos3c { std::string sym; std::vector<int> lots; Pos3c(Pos3c&& o) : sym(std::move(o.sym)), lots(std::move(o.lots)) {} Pos3c(const Pos3c&) = default; };
struct Order { std::unique_ptr<Fill> fill; ~Order() {} };
struct Holder { std::unique_ptr<Fill> fill; };
struct Cnt { static inline int copies = 0, moves = 0; Cnt() = default; Cnt(const Cnt&) { ++copies; } Cnt(Cnt&&) { ++moves; } };
struct P3 { Cnt c; P3() = default; P3(P3&& o) : c(std::move(o.c)) {} };
struct P3c { Cnt c; P3c() = default; P3c(P3c&& o) : c(std::move(o.c)) {} P3c(const P3c&) = default; };
int main() {
  row<Nothing>("nothing"); row<Dtor>("dtor"); row<CopyCtor>("copy_ctor"); row<CopyAssign>("copy_assign");
  row<MoveCtor>("move_ctor"); row<MoveAssign>("move_assign"); row<AllFive>("all_five");
  std::printf("pos_nothrow=%d\npos3_nothrow=%d\npos3_copyable=%d\npos3c_nothrow=%d\npos3c_copyable=%d\n", (int)std::is_nothrow_move_constructible_v<Pos>, (int)std::is_nothrow_move_constructible_v<Pos3>, (int)std::is_copy_constructible_v<Pos3>, (int)std::is_nothrow_move_constructible_v<Pos3c>, (int)std::is_copy_constructible_v<Pos3c>);
  std::printf("string_nothrow=%d\nvector_nothrow=%d\n", (int)std::is_nothrow_move_constructible_v<std::string>, (int)std::is_nothrow_move_constructible_v<std::vector<int>>);
  { std::vector<P3> v; for (int i = 0; i < 4; ++i) v.push_back(P3()); std::printf("pos3_like_growth=%d,%d\n", Cnt::copies, Cnt::moves); Cnt::copies = Cnt::moves = 0; }
  { std::vector<P3c> v; for (int i = 0; i < 4; ++i) v.push_back(P3c()); std::printf("pos3_with_copy_growth=%d,%d\n", Cnt::copies, Cnt::moves); }
  std::printf("order=%d,%d,%d,%d,%d\n", (int)std::is_default_constructible_v<Order>, (int)std::is_move_constructible_v<Order>, (int)std::is_copy_constructible_v<Order>, (int)std::is_move_assignable_v<Order>, (int)std::is_copy_assignable_v<Order>);
  std::printf("holder=%d,%d\n", (int)std::is_copy_constructible_v<Holder>, (int)std::is_move_constructible_v<Holder>);
}
'''
prog('special', SPECIAL)
cc('order_move_deleted', ['-std=c++17', '-fsyntax-only', 't.cpp'], r'''
#include <memory>
#include <utility>
struct Fill {};
struct Order { std::unique_ptr<Fill> fill; ~Order() {} };
void f() { Order a; Order b = std::move(a); }
''')
cc('fill_move_ctor_only_ok', ['-std=c++17', '-fsyntax-only', 't.cpp'], r'''
#include <string>
#include <utility>
struct Fill { std::string s; Fill(std::string x) : s(std::move(x)) {} Fill(Fill&& o) noexcept : s(std::move(o.s)) {} };
void f(Fill& a) { Fill b = std::move(a); }
''')
for nm, line in (('copy', 'Fill b = a;'), ('assign', 'b0 = a;'), ('move_assign', 'b0 = std::move(a);')):
    cc('fill_move_ctor_only_' + nm, ['-std=c++17', '-fsyntax-only', 't.cpp'], r'''
#include <string>
#include <utility>
struct Fill { std::string s; Fill(std::string x) : s(std::move(x)) {} Fill(Fill&& o) noexcept : s(std::move(o.s)) {} };
void f(Fill& a, Fill& b0) { ''' + line + ' }\n')

prog('samples_no_guard', r'''
#include <cstdio>
// the lesson's Samples copy assignment (allocate, copy, free, point) with the guard removed
class Samples {
public:
  Samples(int n, double x) : size_(n), data_(new double[n]) { for (int i = 0; i < n; ++i) data_[i] = x; }
  ~Samples() { delete[] data_; }
  Samples(const Samples& o) : size_(o.size_), data_(new double[o.size_]) { for (int i = 0; i < size_; ++i) data_[i] = o.data_[i]; }
  Samples& operator=(const Samples& other) {
    double* fresh = new double[other.size_];
    for (int i = 0; i < other.size_; ++i) fresh[i] = other.data_[i];
    delete[] data_;
    data_ = fresh;
    size_ = other.size_;
    return *this;
  }
  int size() const { return size_; }
  double get(int i) const { return data_[i]; }
private:
  int size_; double* data_;
};
int main() {
  Samples a(10, 1.5); Samples& r = a; a = r;
  double s = 0; for (int i = 0; i < a.size(); ++i) s += a.get(i);
  std::printf("size=%d\nsum=%g\n", a.size(), s);
}
''')

prog('virtuals', r'''
#include <cstdio>
#include <string>
#include <memory>
#include <vector>
struct Tick { int px; };
struct VTick { int px; virtual int level() const { return px; } };
struct B { int x; virtual void f() {} };
struct D : B { int y; void f() override {} };
struct Quote { virtual double mid() const { return 0; } double bid, ask; };
struct W { virtual void f() {} int n; };
struct S { virtual void f() {} char c; };
struct BD { virtual void f() {} double x; };
struct Buffer { int size_; double* data_; };
struct Payoff { double k = 100; virtual double value(double) const { return -1; } virtual ~Payoff() = default; };
struct Call : Payoff { double value(double s) const override { return s > k ? s - k : 0; } };
struct Base { std::string who; Base() { who = name(); } virtual std::string name() const { return "Base"; } virtual ~Base() = default; };
struct Derived : Base { std::string name() const override { return "Derived"; } };
int main() {
  std::printf("Tick=%zu\nVTick=%zu\nB=%zu\nD=%zu\nQuote=%zu\nW=%zu\nS=%zu\nBD=%zu\nBuffer=%zu\nalign_double=%zu\n", sizeof(Tick), sizeof(VTick), sizeof(B), sizeof(D), sizeof(Quote), sizeof(W), sizeof(S), sizeof(BD), sizeof(Buffer), alignof(double));
  std::printf("unique=%zu\nshared=%zu\nlong=%zu\nsize_t=%zu\n", sizeof(std::unique_ptr<int>), sizeof(std::shared_ptr<int>), sizeof(long), sizeof(std::size_t));
  Call c; Payoff q = c; const Payoff& ref = c;
  std::printf("sliced=%g\nvia_ref=%g\n", q.value(110), ref.value(110));
  std::vector<Payoff> v; v.push_back(Call()); std::printf("vector_slice=%g\n", v[0].value(110));
  Derived d; std::printf("ctor_call=%s\nlater_call=%s\n", d.who.c_str(), d.name().c_str());
  std::unique_ptr<Payoff> p = std::make_unique<Call>(); std::printf("via_unique=%g\n", p->value(110));
}
''')

prog('ub_null_check', r'''
#include <cstdio>
__attribute__((noinline)) int first(int* p) {
  int v = *p;
  if (p == nullptr) return -1;
  return v;
}
int main() {
  int* volatile vp = nullptr;
  std::printf("before=1\n"); std::fflush(stdout);
  int r = first(vp);
  std::printf("is_minus_one=%d\nalive=1\n", (int)(r == -1));
}
''')
prog('ub_misc', r'''
#include <cstdio>
#include <climits>
#include <vector>
#include <cstddef>
__attribute__((noinline)) bool after_check(int a, int b) { int s = a + b; return (b > 0 && s < a) || (b < 0 && s > a); }
__attribute__((noinline)) bool after_check2(int a, int b) { return b > 0 ? a + b < a : a + b > a; }
__attribute__((noinline)) bool starter(int a, int b) { return a + b > INT_MAX; }
int main() {
  unsigned u = 0; u = u - 1; std::printf("u_minus_1=%u\n", u);
  volatile unsigned um = UINT_MAX; std::printf("uint_max_plus_1=%u\n", um + 1u);
  volatile unsigned one = 1u; std::printf("one_shl_31=%u\n", one << 31);
  std::vector<int> v; std::printf("size_minus_1=%zu\n", v.size() - 1);
  volatile int a = INT_MAX, b = 1, c = INT_MIN, d = -1;
  std::printf("after_check_max=%d\nafter_check_min=%d\nafter_check2_max=%d\nafter_check2_min=%d\nstarter_max=%d\n", (int)after_check(a, b), (int)after_check(c, d), (int)after_check2(a, b), (int)after_check2(c, d), (int)starter(a, b));
  volatile char ch = -1; std::printf("char_signed=%d\n", (int)(ch < 0));
  std::printf("int_max=%d\nll=%zu\n", INT_MAX, sizeof(long long));
  long long pence = 5000LL * 500000LL; std::printf("pence=%lld\nover=%lld\n", pence, pence - INT_MAX);
}
''')
prog('ub_null_read', r'''
#include <cstdio>
int main() { int* volatile p = nullptr; std::printf("before=1\n"); std::fflush(stdout); int v = *p; std::printf("v_read=1\nalive=1\n"); (void)v; }
''')

prog('smart', r'''
#include <cstdio>
#include <cstdlib>
#include <memory>
#include <new>
static int allocs = 0;
void* operator new(std::size_t n) { ++allocs; return std::malloc(n ? n : 1); }
void operator delete(void* p) noexcept { std::free(p); }
void operator delete(void* p, std::size_t) noexcept { std::free(p); }
struct Tracked { int v; explicit Tracked(int x) : v(x) {} };
struct Message { char body[64]; };
int main() {
  allocs = 0; { std::shared_ptr<Message> p(new Message); std::printf("shared_new=%d\n", allocs); }
  allocs = 0; { auto p = std::make_shared<Message>(); std::printf("make_shared=%d\n", allocs); }
  allocs = 0; { auto p = std::make_unique<Message>(); std::printf("make_unique=%d\n", allocs); }
  { auto a = std::make_shared<Tracked>(1); std::weak_ptr<Tracked> w = a; auto b = a; std::printf("weak_count=%ld\n", a.use_count()); }
  { auto a = std::make_shared<Tracked>(1); auto b = a; auto c = std::move(b); std::printf("moved_count=%ld\nb_empty=%d\n", a.use_count(), (int)(b == nullptr)); }
  { auto a = std::make_shared<Tracked>(1); auto b = a; b = std::move(a); std::printf("move_assign_count=%ld\na_count=%ld\n", b.use_count(), a.use_count()); }
  { allocs = 0; auto a = std::make_shared<Tracked>(1); int base = allocs; auto b = a; auto c = b; std::printf("copy_allocs=%d\n", allocs - base); }
  std::shared_ptr<Tracked> e; std::printf("empty_count=%ld\n", e.use_count());
  std::printf("unique_sz=%zu\nshared_sz=%zu\n", sizeof(std::unique_ptr<int>), sizeof(std::shared_ptr<int>));
}
''')
prog('shared_base_no_virtual', r'''
#include <cstdio>
#include <memory>
static int derived_dtors = 0;
struct Base { ~Base() {} };
struct Derived : Base { ~Derived() { ++derived_dtors; } };
int main() {
  { std::shared_ptr<Base> p = std::make_shared<Derived>(); }
  std::printf("shared_runs_derived=%d\n", derived_dtors);
  derived_dtors = 0;
  { std::shared_ptr<Base> p(new Derived); }
  std::printf("shared_new_runs_derived=%d\n", derived_dtors);
}
''')

# other ABIs, by the same compiler's front end: sizes a learner would meet on a 64-bit desktop
SIZES64 = r'''
struct B { int x; virtual void f(); };
struct D : B { int y; void f() override; };
struct Quote { virtual double mid() const; double bid, ask; };
struct W { virtual void f(); int n; };
struct S { virtual void f(); char c; };
struct VTick { int px; virtual int level() const; };
struct Buffer { int size_; double* data_; };
'''
cc('linux64_sizes', ['--target=x86_64-unknown-linux-gnu', '-std=c++17', '-fsyntax-only', 't.cpp'], SIZES64 + 'static_assert(sizeof(B) == 16 && sizeof(D) == 16 && sizeof(Quote) == 24 && sizeof(W) == 16 && sizeof(S) == 16 && sizeof(VTick) == 16 && sizeof(Buffer) == 16 && sizeof(long) == 8 && sizeof(void*) == 8, "x");\n')
cc('win64_D_is_24', ['--target=x86_64-pc-windows-msvc', '-std=c++17', '-fsyntax-only', 't.cpp'], SIZES64 + 'static_assert(sizeof(B) == 16 && sizeof(D) == 24, "x");\n')
cc('win64_D_is_16', ['--target=x86_64-pc-windows-msvc', '-std=c++17', '-fsyntax-only', 't.cpp'], SIZES64 + 'static_assert(sizeof(D) == 16, "x");\n')
cc('win64_long_is_4', ['--target=x86_64-pc-windows-msvc', '-std=c++17', '-fsyntax-only', 't.cpp'], 'static_assert(sizeof(long) == 4 && sizeof(void*) == 8 && sizeof(long long) == 8, "x");\n')
cc('win64_long_is_8', ['--target=x86_64-pc-windows-msvc', '-std=c++17', '-fsyntax-only', 't.cpp'], 'static_assert(sizeof(long) == 8, "x");\n')

# ---- proposed fixes, verified on the page's compiler --------------------------------------------------------
prog('x.fix_misc', r'''
#include <unordered_map>
#include <string>
#include <vector>
#include <numeric>
#include <iostream>
int main() {
  std::unordered_map<std::string, int> u; u["AZN"]; u["BP"]; u["SHEL"];
  std::cout << "unordered_alpha_in=";
  for (const auto& kv : u) std::cout << kv.first << ',';
  std::vector<double> px{10.25, 10.75}, q{3, 1};
  std::cout << "\nvwap_int_start=" << std::inner_product(px.begin(), px.end(), q.begin(), 0) / static_cast<double>(std::accumulate(q.begin(), q.end(), 0))
            << "\nvwap_dbl_start=" << std::inner_product(px.begin(), px.end(), q.begin(), 0.0) / std::accumulate(q.begin(), q.end(), 0.0) << '\n';
}
''')
prog('x.fix_ma_n5', r'''
#include <vector>
#include <cstdio>
int main() {
  std::vector<double> xs{100, 101, 102}, out; int n = 5;
  std::printf("before=1\n"); std::fflush(stdout);
  for (std::size_t i = 0; i < xs.size() - n + 1; ++i) { double s = 0; for (int j = 0; j < n; ++j) s += xs[i + j]; out.push_back(s / n); }
  std::printf("after=%zu\n", out.size());
}
''')
for _nm, _cmp in (('time_le', 'if (x.price != y.price) return x.price > y.price; return x.time <= y.time;'), ('price_ge', 'return x.price >= y.price;'), ('strict', 'if (x.price != y.price) return x.price > y.price; return x.time < y.time;')):
    prog('x.fix_sort40_' + _nm, r'''
#include <algorithm>
#include <vector>
#include <cstdio>
struct Order { double price; int qty; long long time; };
int main() {
  std::vector<Order> b(40, Order{99.9, 1, 5});
  std::printf("before=1\n"); std::fflush(stdout);
  std::sort(b.begin(), b.end(), [](const Order& x, const Order& y) { ''' + _cmp + r''' });
  std::printf("after=%zu\n", b.size());
}
''')
cc('x.fix_constexpr_defined', ['-std=c++17', '-fsyntax-only', 't.cpp'], '#include <climits>\nconstexpr bool add_overflows(int a, int b) { if (b > 0) return a > INT_MAX - b; return a < INT_MIN - b; }\nstatic_assert(add_overflows(INT_MAX, 1) && add_overflows(INT_MIN, -1) && !add_overflows(1, 2), "x");\n')
cc('x.fix_constexpr_after_sign', ['-std=c++17', '-fsyntax-only', 't.cpp'], '#include <climits>\nconstexpr bool add_overflows(int a, int b) { int s = a + b; return (a > 0 && b > 0 && s < 0) || (a < 0 && b < 0 && s >= 0); }\nstatic_assert(add_overflows(INT_MAX, 1), "x");\n')
prog('x.map_depth', r'''
#include <map>
#include <cstdio>
#include <algorithm>
#include <string>
static long cmps = 0;
struct Less { bool operator()(int a, int b) const { ++cmps; return a < b; } };
struct SLess { bool operator()(const std::string& a, const std::string& b) const { ++cmps; return a < b; } };
int main() {
  std::map<int, int, Less> m; for (int i = 1; i <= 7; ++i) m[i] = i;
  long worst = 0; for (int i = 1; i <= 7; ++i) { cmps = 0; m.lower_bound(i); worst = std::max(worst, cmps); }
  std::printf("depth7_sorted_inserts=%ld\n", worst);
  std::map<std::string, int, SLess> s; for (const char* k : {"HSBA", "BARC", "SHEL", "AZN", "BP", "LLOY", "VOD"}) s[k] = 1;
  worst = 0; for (const char* k : {"HSBA", "BARC", "SHEL", "AZN", "BP", "LLOY", "VOD"}) { cmps = 0; s.lower_bound(k); worst = std::max(worst, cmps); }
  std::printf("depth7_lesson_order=%ld\n", worst);
  std::map<int, int, Less> big; for (int i = 0; i < 1000000; ++i) big[i] = i;
  worst = 0; long total = 0; for (int i = 0; i < 1000000; i += 97) { cmps = 0; big.lower_bound(i); worst = std::max(worst, cmps); total += cmps; }
  std::printf("depth_million_sorted=%ld\n", worst);
  std::map<int, int, Less> r; unsigned x = 12345; for (int i = 0; i < 1000000; ++i) { x = x * 1664525u + 1013904223u; r[(int)(x >> 8)] = i; }
  worst = 0; x = 12345; for (int i = 0; i < 1000000; ++i) { x = x * 1664525u + 1013904223u; if (i % 1009 == 0) { cmps = 0; r.lower_bound((int)(x >> 8)); worst = std::max(worst, cmps); } }
  std::printf("depth_million_random=%ld\nsize_random=%zu\n", worst, r.size());
}
''')

cc('linker_names_caller_symbol', ['-std=c++17', 't.cpp', '-o', 't.wasm'], 'double risk_value(double x);\nint main() { return static_cast<int>(risk_value(1.0)); }\n')
cc('abstract_middle_class', ['-std=c++17', '-fsyntax-only', 't.cpp'], 'struct Payoff { virtual double value(double) const = 0; virtual ~Payoff() = default; };\nstruct Vanilla : Payoff { double strike = 100; };\nstruct Call : Vanilla { double value(double s) const override { return s > strike ? s - strike : 0; } };\nCall c;\n')
cc('abstract_middle_instantiated', ['-std=c++17', '-fsyntax-only', 't.cpp'], 'struct Payoff { virtual double value(double) const = 0; virtual ~Payoff() = default; };\nstruct Vanilla : Payoff { double strike = 100; };\nVanilla v;\n')
# ---------------------------------------------------------------------------------------------------------------
# 2. Code widgets: natural codings of each mistake a feedback.byKey.test-N line names, graded as the page grades
#    EXPECT[name] = the key the content's line implies ('test-4'), or None for a program that should pass
# ---------------------------------------------------------------------------------------------------------------
EXPECT = {}
def coding(name, file, screen, src, expect):
    path = ('items[%d].widget' if file.startswith('homework') else 'screens[%d].widget') % screen
    grade(name, file, path, src)
    EXPECT[name] = expect

# --- l14 s3 moving_average
MA = '#include <vector>\nstd::vector<double> moving_average(const std::vector<double>& xs, int n) {\n    std::vector<double> out;\n%s\n    return out;\n}\n'
WIN = '        double s = 0;\n        for (int j = 0; j < n; ++j) s += xs[i + j];\n        out.push_back(s / n);\n'
coding('l14s3.count_wraps_to_zero', 'l14-vector.json', 3, MA % ('    if (n < 1) return out;\n    for (std::size_t i = 0; i < xs.size() - n + 1; ++i) {\n' + WIN + '    }'), 'test-4')
coding('l14s3.le_size_minus_n', 'l14-vector.json', 3, MA % ('    if (n < 1) return out;\n    for (std::size_t i = 0; i <= xs.size() - n; ++i) {\n' + WIN + '    }'), 'test-4')
coding('l14s3.last_wraps', 'l14-vector.json', 3, MA % ('    if (n < 1) return out;\n    std::size_t last = xs.size() - n;\n    for (std::size_t i = 0; i <= last; ++i) {\n' + WIN + '    }'), 'test-4')  # fix pass
coding('l14s3.no_guards_count', 'l14-vector.json', 3, MA % ('    for (std::size_t i = 0; i < xs.size() - n + 1; ++i) {\n' + WIN + '    }'), 'test-4')  # re-pointed (fix pass, finding 2): with n = 5 in test 4 the unguarded loop now stops there
coding('l14s3.no_n_lt_1', 'l14-vector.json', 3, MA % ('    if (static_cast<std::size_t>(n) > xs.size()) return out;\n    for (std::size_t i = 0; i + n <= xs.size(); ++i) {\n' + WIN + '    }'), 'test-7')
coding('l14s3.int_arith_no_guard', 'l14-vector.json', 3, MA % ('    int m = static_cast<int>(xs.size());\n    for (int i = 0; i + n <= m; ++i) {\n' + WIN + '    }'), 'test-7')
coding('l14s3.window_one_late', 'l14-vector.json', 3, MA % ('    if (n < 1 || static_cast<std::size_t>(n) > xs.size()) return out;\n    for (std::size_t i = 1; i + n <= xs.size(); ++i) {\n' + WIN + '    }'), 'test-2')
# --- l14 s4 returns_from
RF = '#include <vector>\nstd::vector<double> returns_from(const std::vector<double>& px) {\n%s\n    return out;\n}\n'
coding('l14s4.reserve_no_guard', 'l14-vector.json', 4, RF % '    std::vector<double> out;\n    out.reserve(px.size() - 1);\n    for (std::size_t i = 1; i < px.size(); ++i) out.push_back(px[i] / px[i - 1] - 1);', 'test-3')
coding('l14s4.ctor_no_guard', 'l14-vector.json', 4, RF % '    std::vector<double> out(px.size() - 1);\n    for (std::size_t i = 1; i < px.size(); ++i) out[i - 1] = px[i] / px[i - 1] - 1;', 'test-3')
coding('l14s4.loop_to_size_minus_1', 'l14-vector.json', 4, RF % '    std::vector<double> out;\n    for (std::size_t i = 0; i < px.size() - 1; ++i) out.push_back(px[i + 1] / px[i] - 1);', 'test-3')
coding('l14s4.no_reserve', 'l14-vector.json', 4, RF % '    std::vector<double> out;\n    for (std::size_t i = 1; i < px.size(); ++i) out.push_back(px[i] / px[i - 1] - 1);', 'test-5')
coding('l14s4.reserve_size', 'l14-vector.json', 4, RF % '    std::vector<double> out;\n    out.reserve(px.size());\n    for (std::size_t i = 1; i < px.size(); ++i) out.push_back(px[i] / px[i - 1] - 1);', 'test-5')
coding('l14s4.divide_by_later', 'l14-vector.json', 4, RF % '    std::vector<double> out;\n    if (px.size() < 2) return out;\n    out.reserve(px.size() - 1);\n    for (std::size_t i = 1; i < px.size(); ++i) out.push_back((px[i] - px[i - 1]) / px[i]);', 'test-1')
coding('l14s4.inverted', 'l14-vector.json', 4, RF % '    std::vector<double> out;\n    if (px.size() < 2) return out;\n    out.reserve(px.size() - 1);\n    for (std::size_t i = 1; i < px.size(); ++i) out.push_back(px[i - 1] / px[i] - 1);', 'test-1')
coding('l14s4.sized_ctor_ok', 'l14-vector.json', 4, RF % '    if (px.size() < 2) return {};\n    std::vector<double> out(px.size() - 1);\n    for (std::size_t i = 1; i < px.size(); ++i) out[i - 1] = px[i] / px[i - 1] - 1;', None)
# --- l14 s6 three largest
TOP = '#include <algorithm>\n#include <iostream>\n#include <vector>\n\nint main() {\n    std::vector<double> prices;\n    double p;\n    while (std::cin >> p) {\n        prices.push_back(p);\n    }\n%s\n    return 0;\n}\n'
coding('l14s6.always_three', 'l14-vector.json', 6, TOP % "    std::sort(prices.begin(), prices.end());\n    for (std::size_t k = 0; k < 3; ++k) std::cout << prices[prices.size() - 1 - k] << '\\n';", 'test-2')
coding('l14s6.three_ifs', 'l14-vector.json', 6, TOP % "    std::sort(prices.begin(), prices.end());\n    std::size_t n = prices.size();\n    std::cout << prices[n - 1] << '\\n';\n    if (n > 1) std::cout << prices[n - 2] << '\\n';\n    if (n > 2) std::cout << prices[n - 3] << '\\n';", 'test-3')
coding('l14s6.from_front', 'l14-vector.json', 6, TOP % "    std::sort(prices.begin(), prices.end());\n    for (std::size_t k = 0; k < 3 && k < prices.size(); ++k) std::cout << prices[k] << '\\n';", 'test-1')
coding('l14s6.no_sort', 'l14-vector.json', 6, TOP % "    for (std::size_t k = 0; k < 3 && k < prices.size(); ++k) std::cout << prices[prices.size() - 1 - k] << '\\n';", 'test-1')
# --- l14 s7 price_change
PC = '#include <vector>\n#include <stdexcept>\ndouble price_change(const std::vector<double>& px, int from, int to) {\n%s\n}\n'
coding('l14s7.starter', 'l14-vector.json', 7, '@starter', 'test-3')
coding('l14s7.at_to_only', 'l14-vector.json', 7, PC % '    return px.at(to) - px[from];', 'test-4')
coding('l14s7.manual_upper_only', 'l14-vector.json', 7, PC % '    if (to >= static_cast<int>(px.size()) || from >= static_cast<int>(px.size())) throw std::out_of_range("day");\n    return px[to] - px[from];', 'test-4')
coding('l14s7.manual_ok', 'l14-vector.json', 7, PC % '    int n = static_cast<int>(px.size());\n    if (to < 0 || to >= n || from < 0 || from >= n) throw std::out_of_range("day");\n    return px[to] - px[from];', None)
# --- l14 s10 lattice
PL = '#include <vector>\n#include <cmath>\nstd::vector<std::vector<double>> price_lattice(double s0, double u, double d, int steps) {\n    std::vector<std::vector<double>> tree;\n%s\n    return tree;\n}\n'
coding('l14s10.direct_ok', 'l14-vector.json', 10, PL % '    for (int i = 0; i <= steps; ++i) {\n        std::vector<double> row;\n        for (int j = 0; j <= i; ++j) row.push_back(s0 * std::pow(u, i - j) * std::pow(d, j));\n        tree.push_back(row);\n    }', None)
coding('l14s10.steps_rows', 'l14-vector.json', 10, PL % '    for (int i = 0; i < steps; ++i) {\n        std::vector<double> row;\n        for (int j = 0; j <= i; ++j) row.push_back(s0 * std::pow(u, i - j) * std::pow(d, j));\n        tree.push_back(row);\n    }', 'test-1')
coding('l14s10.ups_and_downs_swapped', 'l14-vector.json', 10, PL % '    for (int i = 0; i <= steps; ++i) {\n        std::vector<double> row;\n        for (int j = 0; j <= i; ++j) row.push_back(s0 * std::pow(d, i - j) * std::pow(u, j));\n        tree.push_back(row);\n    }', 'test-1')

# --- l15 s4 position book
PB = '#include <map>\n#include <string>\n#include <vector>\n\nstd::map<std::string, int> position_by_symbol(const std::vector<std::string>& syms, const std::vector<int>& qty) {\n    std::map<std::string, int> pos;\n%s\n    return pos;\n}\n'
coding('l15s4.assign', 'l15-maps.json', 4, PB % '    for (std::size_t i = 0; i < syms.size(); ++i) pos[syms[i]] = qty[i];', 'test-1')
coding('l15s4.erase_flat', 'l15-maps.json', 4, PB % '    for (std::size_t i = 0; i < syms.size(); ++i) { pos[syms[i]] += qty[i]; if (pos[syms[i]] == 0) pos.erase(syms[i]); }', 'test-3')
coding('l15s4.insert_only', 'l15-maps.json', 4, PB % '    for (std::size_t i = 0; i < syms.size(); ++i) pos.insert({syms[i], qty[i]});', 'test-1')
# --- l15 s5 exposure
EX = '#include <map>\n#include <string>\n#include <unordered_map>\n\ndouble exposure(const std::unordered_map<std::string, double>& px, const std::map<std::string, int>& pos) {\n    double total = 0;\n%s\n    return total;\n}\n'
coding('l15s5.index_const', 'l15-maps.json', 5, EX % '    for (const auto& [sym, qty] : pos) total += qty * px[sym];', 'compile')
coding('l15s5.at', 'l15-maps.json', 5, EX % '    for (const auto& [sym, qty] : pos) total += qty * px.at(sym);', 'test-2')
coding('l15s5.find_unchecked', 'l15-maps.json', 5, EX % '    for (const auto& [sym, qty] : pos) total += qty * px.find(sym)->second;', 'test-2')
coding('l15s5.count_then_at', 'l15-maps.json', 5, EX % '    for (const auto& [sym, qty] : pos) if (px.count(sym)) total += qty * px.at(sym);', None)
# --- l15 s7 fills per venue
FV = '#include <iostream>\n#include <map>\n#include <unordered_map>\n#include <string>\n#include <vector>\n\nint main() {\n%s\n    return 0;\n}\n'
coding('l15s7.unordered', 'l15-maps.json', 7, FV % "    std::unordered_map<std::string, int> fills, shares;\n    std::string venue; int qty;\n    while (std::cin >> venue >> qty) { ++fills[venue]; shares[venue] += qty; }\n    for (const auto& [v, n] : fills) std::cout << v << ' ' << n << ' ' << shares[v] << '\\n';", 'test-1')
coding('l15s7.arrival_order', 'l15-maps.json', 7, FV % "    std::map<std::string, int> fills, shares; std::vector<std::string> seen;\n    std::string venue; int qty;\n    while (std::cin >> venue >> qty) { if (!fills.count(venue)) seen.push_back(venue); ++fills[venue]; shares[venue] += qty; }\n    for (const auto& v : seen) std::cout << v << ' ' << fills[v] << ' ' << shares[v] << '\\n';", 'test-1')
coding('l15s7.overwrite_shares', 'l15-maps.json', 7, FV % "    std::map<std::string, int> fills, shares;\n    std::string venue; int qty;\n    while (std::cin >> venue >> qty) { ++fills[venue]; shares[venue] = qty; }\n    for (const auto& [v, n] : fills) std::cout << v << ' ' << n << ' ' << shares[v] << '\\n';", 'test-1')

# --- l16 s3 vwap
VW = '#include <numeric>\n#include <vector>\n\ndouble vwap(const std::vector<double>& px, const std::vector<double>& qty) {\n%s\n}\n'
coding('l16s3.no_check', 'l16-algorithms.json', 3, VW % '    return std::inner_product(px.begin(), px.end(), qty.begin(), 0.0) / std::accumulate(qty.begin(), qty.end(), 0.0);', 'test-3')
coding('l16s3.empty_check_only', 'l16-algorithms.json', 3, VW % '    if (px.empty()) return 0;\n    return std::inner_product(px.begin(), px.end(), qty.begin(), 0.0) / std::accumulate(qty.begin(), qty.end(), 0.0);', 'test-4')
coding('l16s3.plain_mean', 'l16-algorithms.json', 3, VW % '    if (px.empty()) return 0;\n    return std::accumulate(px.begin(), px.end(), 0.0) / px.size();', 'test-1')
coding('l16s3.int_start', 'l16-algorithms.json', 3, VW % '    double shares = std::accumulate(qty.begin(), qty.end(), 0);\n    if (shares == 0) return 0;\n    return std::inner_product(px.begin(), px.end(), qty.begin(), 0) / shares;', 'test-6')  # re-pointed (fix pass, finding 8)
coding('l16s3.int_value_only', 'l16-algorithms.json', 3, VW % '    double shares = std::accumulate(qty.begin(), qty.end(), 0.0);\n    if (shares == 0) return 0;\n    double value = std::inner_product(px.begin(), px.end(), qty.begin(), 0);\n    return value / shares;', 'test-6')  # fix pass
coding('l16s3.int_loop', 'l16-algorithms.json', 3, VW % '    int value = 0;\n    double shares = 0;\n    for (std::size_t i = 0; i < px.size(); ++i) { value += px[i] * qty[i]; shares += qty[i]; }\n    if (shares == 0) return 0;\n    return value / shares;', 'test-6')  # fix pass
# --- l16 s4 sort_book
SB = '#include <algorithm>\n#include <vector>\n\nstd::vector<Order> sort_book(std::vector<Order> b) {\n    std::sort(b.begin(), b.end(), [](const Order& x, const Order& y) {\n%s\n    });\n    return b;\n}\n'
coding('l16s4.price_only', 'l16-algorithms.json', 4, SB % '        return x.price > y.price;', 'test-2')
coding('l16s4.price_ge', 'l16-algorithms.json', 4, SB % '        return x.price >= y.price;', 'test-2')  # re-pointed (fix pass, finding 7): no tie-break, so test 2 first
coding('l16s4.time_le', 'l16-algorithms.json', 4, SB % '        if (x.price != y.price) return x.price > y.price;\n        return x.time <= y.time;', 'test-6')  # re-pointed (fix pass, finding 7)
coding('l16s4.ge_then_le', 'l16-algorithms.json', 4, SB % '        if (x.price > y.price) return true;\n        if (x.price < y.price) return false;\n        return x.time <= y.time;', 'test-6')  # re-pointed (fix pass, finding 7)
coding('l16s4.or_le', 'l16-algorithms.json', 4, SB % '        return x.price > y.price || (x.price == y.price && x.time <= y.time);', 'test-6')  # fix pass
coding('l16s4.ascending', 'l16-algorithms.json', 4, SB % '        if (x.price != y.price) return x.price < y.price;\n        return x.time < y.time;', 'test-1')
# --- l16 s5 count_up_days
CU = '#include <algorithm>\n#include <numeric>\n#include <vector>\n\nint count_up_days(const std::vector<double>& px) {\n%s\n}\n'
coding('l16s5.counts_d0', 'l16-algorithms.json', 5, CU % '    if (px.size() < 2) return 0;\n    std::vector<double> d(px.size());\n    std::adjacent_difference(px.begin(), px.end(), d.begin());\n    return std::count_if(d.begin(), d.end(), [](double x) { return x > 0; });', 'test-1')  # re-pointed (fix pass, finding 11)
coding('l16s5.counts_d0_no_guard', 'l16-algorithms.json', 5, CU % '    std::vector<double> d(px.size());\n    std::adjacent_difference(px.begin(), px.end(), d.begin());\n    return std::count_if(d.begin(), d.end(), [](double x) { return x > 0; });', 'test-1')  # re-pointed (fix pass, finding 11)
coding('l16s5.no_guard', 'l16-algorithms.json', 5, CU % '    std::vector<double> d(px.size());\n    std::adjacent_difference(px.begin(), px.end(), d.begin());\n    return std::count_if(d.begin() + 1, d.end(), [](double x) { return x > 0; });', 'test-2')
coding('l16s5.ge_zero', 'l16-algorithms.json', 5, CU % '    if (px.size() < 2) return 0;\n    std::vector<double> d(px.size());\n    std::adjacent_difference(px.begin(), px.end(), d.begin());\n    return std::count_if(d.begin() + 1, d.end(), [](double x) { return x >= 0; });', 'test-5')
# --- l16 s9 worst_drawdown
WD = '#include <algorithm>\n#include <numeric>\n#include <vector>\n\ndouble worst_drawdown(const std::vector<double>& daily) {\n    std::vector<double> cum(daily.size());\n    std::partial_sum(daily.begin(), daily.end(), cum.begin());\n%s\n    return worst;\n}\n'
LOOP = '    std::for_each(cum.begin(), cum.end(), [&peak, &worst](double c) { peak = std::max(peak, c); worst = std::max(worst, peak - c); });'
coding('l16s9.peak_first_guarded', 'l16-algorithms.json', 9, WD % ('    if (cum.empty()) return 0;\n    double peak = cum[0];\n    double worst = 0;\n' + LOOP), 'test-3')
coding('l16s9.peak_first', 'l16-algorithms.json', 9, WD % ('    double peak = cum[0];\n    double worst = 0;\n' + LOOP), 'test-3')
coding('l16s9.peak_minus_inf', 'l16-algorithms.json', 9, WD % ('    double peak = -1e300;\n    double worst = 0;\n' + LOOP), 'test-3')
coding('l16s9.mutable_copies', 'l16-algorithms.json', 9, WD % '    double peak = 0;\n    double worst = 0;\n    std::for_each(cum.begin(), cum.end(), [peak, worst](double c) mutable { peak = std::max(peak, c); worst = std::max(worst, peak - c); });', 'test-1')
coding('l16s9.value_capture', 'l16-algorithms.json', 9, WD % '    double peak = 0;\n    double worst = 0;\n    std::for_each(cum.begin(), cum.end(), [peak, worst](double c) { peak = std::max(peak, c); worst = std::max(worst, peak - c); });', 'compile')

# --- l17 s4 rates
RT = '#include <cmath>\n#include <vector>\nnamespace pricing {\n\ndouble discount_factor(double r, double t) {\n    return std::exp(-r * t);\n}\n%s\n}  // namespace pricing\n'
FWD = 'double forward_price(double spot, double r, double t) { return spot * std::exp(r * t); }\n'
coding('l17s4.starter', 'l17-cmake.json', 4, '@starter', 'compile')
coding('l17s4.pv_one_time', 'l17-cmake.json', 4, RT % (FWD + 'double present_value(const std::vector<double>& cash, const std::vector<double>& times, double r) {\n    double pv = 0;\n    for (std::size_t i = 0; i < cash.size(); ++i) pv += cash[i] * discount_factor(r, times.back());\n    return pv;\n}\n'), 'test-4')
coding('l17s4.pv_grows', 'l17-cmake.json', 4, RT % (FWD + 'double present_value(const std::vector<double>& cash, const std::vector<double>& times, double r) {\n    double pv = 0;\n    for (std::size_t i = 0; i < cash.size(); ++i) pv += cash[i] * std::exp(r * times[i]);\n    return pv;\n}\n'), 'test-4')
coding('l17s4.wrong_param_types', 'l17-cmake.json', 4, RT % (FWD + 'double present_value(std::vector<double> cash, std::vector<double> times, double r) {\n    double pv = 0;\n    for (std::size_t i = 0; i < cash.size(); ++i) pv += cash[i] * discount_factor(r, times[i]);\n    return pv;\n}\n'), 'compile')
# --- l17 s5 daycount
coding('l17s5.starter', 'l17-cmake.json', 5, '@starter', 'compile')
coding('l17s5.double_params', 'l17-cmake.json', 5, 'double year_fraction(double days, double basis) {\n    return days / basis;\n}\n\ndouble accrued(double coupon, int days, int basis) {\n    return coupon * year_fraction(days, basis);\n}\n', 'compile')
coding('l17s5.basis_fixed', 'l17-cmake.json', 5, 'double year_fraction(int days, int basis) {\n    return days / 365.0;\n}\n\ndouble accrued(double coupon, int days, int basis) {\n    return coupon * year_fraction(days, basis);\n}\n', 'test-1')
coding('l17s5.int_division', 'l17-cmake.json', 5, 'double year_fraction(int days, int basis) {\n    return days / basis;\n}\n\ndouble accrued(double coupon, int days, int basis) {\n    return coupon * year_fraction(days, basis);\n}\n', 'test-1')  # re-pointed (fix pass, finding 11)
DC = 'double year_fraction(int days, int basis) {\n    return %s;\n}\n\ndouble accrued(double coupon, int days, int basis) {\n    return coupon * year_fraction(days, basis);\n}\n'
coding('l17s5.int_division_cast_after', 'l17-cmake.json', 5, DC % 'static_cast<double>(days / basis)', 'test-1')  # fix pass
coding('l17s5.int_division_double_ctor', 'l17-cmake.json', 5, DC % 'double(days / basis)', 'test-1')  # fix pass
coding('l17s5.basis_365_cast', 'l17-cmake.json', 5, DC % 'static_cast<double>(days) / 365', 'test-1')  # fix pass
coding('l17s5.basis_360', 'l17-cmake.json', 5, DC % 'days / 360.0', 'test-2')  # fix pass
coding('l17s5.basis_360_cast', 'l17-cmake.json', 5, DC % 'static_cast<double>(days) / 360', 'test-2')  # fix pass
coding('l17s5.basis_360_ctor', 'l17-cmake.json', 5, DC % 'double(days) / 360.0', 'test-2')  # fix pass

# --- l18 s3 bs_call tests
T3 = 'TEST(at_the_money_matches_known_value) {\n%s\n}\n\nTEST(expiry_pays_intrinsic) {\n%s\n}\n'
ATM = '    CHECK_CLOSE(bs_call(100, 100, 0.05, 0.2, 1.0), 10.4506, %s);'
EXP = '    CHECK_CLOSE(bs_call(90, 100, 0.05, 0.2, 0.0), 0.0, 1e-12);\n    CHECK_CLOSE(bs_call(110, 100, 0.05, 0.2, 0.0), 10.0, 1e-12);'
coding('l18s3.eq', 'l18-unit-tests.json', 3, T3 % ('    CHECK(bs_call(100, 100, 0.05, 0.2, 1.0) == 10.4506);', EXP), 'test-1')
coding('l18s3.tol_1e-5', 'l18-unit-tests.json', 3, T3 % (ATM % '1e-5', EXP), 'test-1')
coding('l18s3.tol_5e-5', 'l18-unit-tests.json', 3, T3 % (ATM % '5e-5', EXP), None)  # re-pointed (fix pass, finding 3)
coding('l18s3.tol_2e-5', 'l18-unit-tests.json', 3, T3 % (ATM % '2e-5', EXP), None)  # re-pointed (fix pass, finding 3)
coding('l18s3.tol_1e-6', 'l18-unit-tests.json', 3, T3 % (ATM % '1e-6', EXP), 'test-1')  # fix pass
coding('l18s3.starter', 'l18-unit-tests.json', 3, '@starter', 'test-2')
coding('l18s3.expiry_only', 'l18-unit-tests.json', 3, T3 % ('', EXP), 'test-2')
coding('l18s3.no_otm_expiry', 'l18-unit-tests.json', 3, T3 % (ATM % '1e-4', '    CHECK_CLOSE(bs_call(110, 100, 0.05, 0.2, 0.0), 10.0, 1e-12);'), 'test-3')
coding('l18s3.zero_rate_pin', 'l18-unit-tests.json', 3, T3 % ('    CHECK_CLOSE(bs_call(100, 100, 0.0, 0.2, 1.0), 7.9656, 1e-4);', EXP), 'test-4')
coding('l18s3.loose_tol', 'l18-unit-tests.json', 3, T3 % (ATM % '1.0', EXP), 'test-2')
# --- l18 s4 documenting test
FLAT = 'TEST(flat_prices_give_zero_returns) {\n    std::vector<double> px{100.0, 100.0, 100.0};\n    std::vector<double> r = simple_returns(px);\n    CHECK(r.size() == 2);\n    CHECK_CLOSE(r[0], 0.0, 1e-12);\n}\n\n'
RISE = 'TEST(rise_from_100_to_110_is_ten_percent) {\n    std::vector<double> px{100.0, 110.0};\n    std::vector<double> r = simple_returns(px);\n%s\n}\n'
coding('l18s4.starter', 'l18-unit-tests.json', 4, '@starter', 'test-1')
coding('l18s4.pins_shipped_value', 'l18-unit-tests.json', 4, FLAT + RISE % '    CHECK_CLOSE(r[0], 0.0909, 1e-4);', 'test-1')
coding('l18s4.eq_exact', 'l18-unit-tests.json', 4, FLAT + RISE % '    CHECK(r[0] == 0.1);', 'test-2')
coding('l18s4.tol_zero', 'l18-unit-tests.json', 4, FLAT + RISE % '    CHECK_CLOSE(r[0], 0.1, 0.0);', 'test-2')
coding('l18s4.percent', 'l18-unit-tests.json', 4, FLAT + RISE % '    CHECK_CLOSE(r[0], 10.0, 1e-9);', 'test-2')
coding('l18s4.size_only', 'l18-unit-tests.json', 4, FLAT + RISE % '    CHECK(r.size() == 1);', 'test-1')
# --- l18 s5 fix the code
SR = '#include <vector>\nstd::vector<double> simple_returns(const std::vector<double>& px) {\n%s\n    return out;\n}\n'
coding('l18s5.starter', 'l18-unit-tests.json', 5, '@starter', 'test-1')
coding('l18s5.divisor_only_fixed', 'l18-unit-tests.json', 5, SR % '    std::vector<double> out(px.size() - 1);\n    for (std::size_t i = 1; i < px.size(); ++i) out[i - 1] = px[i] / px[i - 1] - 1;', 'test-1')
coding('l18s5.guard_only', 'l18-unit-tests.json', 5, SR % '    std::vector<double> out;\n    if (px.size() < 2) return out;\n    for (std::size_t i = 1; i < px.size(); ++i) out.push_back((px[i] - px[i - 1]) / px[i]);', 'test-1')
# --- l18 s9 binomial tests
T9 = 'TEST(matches_python_pricer_at_100_steps) {\n%s\n}\n\nTEST(converges_to_black_scholes) {\n%s\n}\n'
PIN = '    CHECK_CLOSE(binomial_call(100, 100, 0.05, 0.2, 1.0, 100), 10.430612, %s);'
CONV = '    CHECK_CLOSE(binomial_call(100, 100, 0.05, 0.2, 1.0, 2000), 10.450584, 0.002);'
coding('l18s9.starter', 'l18-unit-tests.json', 9, '@starter', 'test-2')
coding('l18s9.pin_1e-7', 'l18-unit-tests.json', 9, T9 % (PIN % '1e-7', CONV), 'test-1')
coding('l18s9.pin_1e-9', 'l18-unit-tests.json', 9, T9 % (PIN % '1e-9', CONV), 'test-1')
coding('l18s9.convergence_only', 'l18-unit-tests.json', 9, T9 % ('', CONV), 'test-3')
coding('l18s9.pin_loose', 'l18-unit-tests.json', 9, T9 % (PIN % '0.05', CONV), 'test-3')
coding('l18s9.pin_only', 'l18-unit-tests.json', 9, T9 % (PIN % '1e-6', ''), 'test-4')  # re-pointed (fix pass of audit cpp-4-5-r2, finding 3): planted bug 3 now needs the convergence test

# --- l22 s4 add_overflows: checks made after the addition
AO = '#include <climits>\nconstexpr bool add_overflows(int a, int b) {\n%s\n}\n'  # re-pointed (fix pass, finding 6): the task now keeps constexpr
coding('l22s4.starter', 'l22-undefined-behaviour.json', 4, '@starter', 'test-1')
coding('l22s4.after_sum_lt', 'l22-undefined-behaviour.json', 4, AO % '    int s = a + b;\n    return (b > 0 && s < a) || (b < 0 && s > a);', 'fail')
coding('l22s4.after_sign', 'l22-undefined-behaviour.json', 4, AO % '    int s = a + b;\n    return (a > 0 && b > 0 && s < 0) || (a < 0 && b < 0 && s >= 0);', 'fail')
coding('l22s4.wide', 'l22-undefined-behaviour.json', 4, AO % '    long long s = static_cast<long long>(a) + b;\n    return s > INT_MAX || s < INT_MIN;', None)
coding('l22s4.unsigned_wrap', 'l22-undefined-behaviour.json', 4, AO % '    int s = static_cast<int>(static_cast<unsigned>(a) + static_cast<unsigned>(b));\n    return (b > 0 && s < a) || (b < 0 && s > a);', None)
coding('l22s4.positive_only', 'l22-undefined-behaviour.json', 4, AO % '    return b > 0 && a > INT_MAX - b;', 'test-3')
coding('l22s4.after_sign_plain', 'l22-undefined-behaviour.json', 4, AO.replace('constexpr ', '') % '    int s = a + b;\n    return (a > 0 && b > 0 && s < 0) || (a < 0 && b < 0 && s >= 0);', 'test-14')  # fix pass
coding('l22s4.unsplit', 'l22-undefined-behaviour.json', 4, AO % '    return a > INT_MAX - b || a < INT_MIN - b;', 'fail')  # fix pass
coding('l22s4.builtin', 'l22-undefined-behaviour.json', 4, AO % '    int r = 0;\n    return __builtin_add_overflow(a, b, &r);', None)  # fix pass
_l22sol = json.load(open(os.path.join(CPP, 'l22-undefined-behaviour.json')))['screens'][4]['widget']['solution']
coding('l22s4.no_constexpr', 'l22-undefined-behaviour.json', 4, _l22sol.replace('constexpr bool', 'bool'), 'test-14')  # fix pass

# --- l20 s5 Samples: the lesson's own copy assignment without the guard (is the guard needed for correctness?)
_sol = json.load(open(os.path.join(CPP, 'l20-rule-of-five.json')))['screens'][5]['widget']['solution']
_head = 'Samples& operator=(const Samples& other) {\n        if (this != &other) {'
assert _head in _sol
coding('l20s5.no_guard_alloc_first', 'l20-rule-of-five.json', 5, _sol.replace(_head, 'Samples& operator=(const Samples& other) {\n        {'), None)

# --- homework 4, item 0 VWAP book
HB = '#include <algorithm>\n#include <iomanip>\n#include <iostream>\n#include <map>\n#include <unordered_map>\n#include <string>\n#include <vector>\n\nstruct Trade { double price; int qty; };\n\nint main() {\n    %s<std::string, std::vector<Trade>> book;\n    std::string sym; double price; int qty;\n    while (std::cin >> sym >> price >> qty) book[sym].push_back({price, qty});\n%s\n    for (auto& [s, trades] : book) {\n%s\n        double value = 0, shares = 0, sum = 0;\n        for (const Trade& t : trades) { value += t.price * t.qty; shares += t.qty; sum += t.price; }\n        std::cout << s << \' \' << trades.size() << \' \' << %s << \' \' << trades.front().price << \' \' << trades.back().price << \'\\n\';\n    }\n    return 0;\n}\n'
SORT = '        std::sort(trades.begin(), trades.end(), [](const Trade& a, const Trade& b) { return a.price < b.price; });'
FIX = '    std::cout << std::fixed << std::setprecision(4);'
coding('h4i0.unweighted', 'homework-4.json', 0, HB % ('std::map', FIX, SORT, 'sum / trades.size()'), 'test-1')  # re-pointed (fix pass, finding 11)
coding('h4i0.unweighted_cast', 'homework-4.json', 0, HB % ('std::map', FIX, SORT, 'sum / static_cast<double>(trades.size())'), 'test-1')  # fix pass
coding('h4i0.unweighted_lambda', 'homework-4.json', 0, HB % ('std::map', FIX, SORT, '[&] { double m = 0; for (const Trade& t : trades) m += t.price / trades.size(); return m; }()'), 'test-1')  # fix pass
coding('h4i0.unordered', 'homework-4.json', 0, HB % ('std::unordered_map', FIX, SORT, 'value / shares'), 'test-6')  # re-pointed (fix pass, finding 9)
coding('h4i0.unordered_reserve8', 'homework-4.json', 0, HB % ('std::unordered_map', FIX + '\n    book.reserve(8);', SORT, 'value / shares'), 'test-6')  # fix pass
coding('h4i0.unordered_reserve64', 'homework-4.json', 0, HB % ('std::unordered_map', FIX + '\n    book.reserve(64);', SORT, 'value / shares'), 'test-6')  # fix pass
coding('h4i0.no_sort', 'homework-4.json', 0, HB % ('std::map', FIX, '', 'value / shares'), 'test-1')
coding('h4i0.no_fixed', 'homework-4.json', 0, HB % ('std::map', '', SORT, 'value / shares'), 'test-1')
# --- homework 4, item 1 drawdown tests
DD = 'TEST(worst_fall_from_running_peak) {\n%s\n}\n\nTEST(rising_prices_have_no_drawdown) {\n    CHECK_CLOSE(max_drawdown({100.0, 101.0, 103.5}), 0.0, 1e-12);\n}\n\nTEST(empty_and_single_price_are_zero) {\n%s\n}\n'
EMP = '    CHECK_CLOSE(max_drawdown({}), 0.0, 1e-12);\n    CHECK_CLOSE(max_drawdown({100.0}), 0.0, 1e-12);'
coding('h4i1.starter', 'homework-4.json', 1, '@starter', 'test-2')
coding('h4i1.wrong_hand_value', 'homework-4.json', 1, DD % ('    CHECK_CLOSE(max_drawdown({100.0, 120.0, 90.0, 130.0, 104.0}), 0.3, 1e-12);', EMP), 'test-1')
coding('h4i1.no_new_peak', 'homework-4.json', 1, DD % ('    CHECK_CLOSE(max_drawdown({100.0, 90.0, 95.0}), 0.1, 1e-12);', EMP), 'test-2')
coding('h4i1.peak_of_one', 'homework-4.json', 1, DD % ('    CHECK_CLOSE(max_drawdown({0.8, 1.0, 0.75, 0.9}), 0.25, 1e-12);', EMP), 'test-3')
coding('h4i1.no_empty_call', 'homework-4.json', 1, DD % ('    CHECK_CLOSE(max_drawdown({100.0, 120.0, 90.0, 130.0, 104.0}), 0.25, 1e-12);', '    CHECK_CLOSE(max_drawdown({100.0}), 0.0, 1e-12);'), 'test-4')
coding('h4i1.worst_is_last', 'homework-4.json', 1, DD % ('    CHECK_CLOSE(max_drawdown({100.0, 120.0, 90.0}), 0.25, 1e-12);', EMP), 'test-5')

# --- level 5 widgets have no test-N lines; check that the hidden tests reject the obvious wrong programs
def variant(name, file, screen, edits, expect):
    d = json.load(open(os.path.join(CPP, file)))
    w = (d['items'] if file.startswith('homework') else d['screens'])[screen]['widget']
    src = w['solution']
    for old, new in edits:
        assert old in src, (name, old[:60])
        src = src.replace(old, new, 1)
    coding(name, file, screen, src, expect)

L19 = 'l19-moving-not-copying.json'
variant('x.l19s5.move_not_noexcept', L19, 5, [('Buffer(Buffer&& other) noexcept :', 'Buffer(Buffer&& other) :')], 'fail')
variant('x.l19s5.source_keeps_size', L19, 5, [('        other.size_ = 0;\n', '')], 'fail')
variant('x.l19s5.no_self_guard', L19, 5, [('    Buffer& operator=(Buffer&& other) noexcept {\n        if (this != &other) {', '    Buffer& operator=(Buffer&& other) noexcept {\n        {')], 'fail')
variant('x.l19s5.assign_leaks_old', L19, 5, [('            delete[] data_;\n            size_ = other.size_;', '            size_ = other.size_;')], 'fail')
variant('x.l19s5.move_that_copies', L19, 5, [('Buffer(Buffer&& other) noexcept : size_(other.size_), data_(other.data_) {', 'Buffer(Buffer&& other) noexcept : size_(other.size_), data_(new double[other.size_]) {\n        for (int i = 0; i < size_; ++i) data_[i] = other.data_[i];\n        delete[] other.data_;')], 'fail')
L20 = 'l20-rule-of-five.json'
variant('x.l20s5.assign_leaks_old', L20, 5, [('            delete[] data_;\n            data_ = fresh;', '            data_ = fresh;')], 'fail')
variant('x.l20s5.shallow_ctor', L20, 5, [('Samples(const Samples& other) : size_(other.size_), data_(new double[other.size_]) {\n        for (int i = 0; i < size_; ++i) data_[i] = other.data_[i];\n    }', 'Samples(const Samples& other) : size_(other.size_), data_(other.data_) {}')], 'fail')
variant('x.l21s5.ignores_table', 'l21-virtual-dispatch.json', 5, [('return p->table->value(p, spot);', 'return std::max(spot - p->strike, 0.0);')], 'fail')
L23 = 'l23-own-smart-pointer.json'
variant('x.l23s2.assign_deletes_first', L23, 2, [('            T* p = other.ptr_;      // take the source first: the old object may own it\n            other.ptr_ = nullptr;\n            delete ptr_;\n            ptr_ = p;', '            delete ptr_;\n            ptr_ = other.ptr_;\n            other.ptr_ = nullptr;')], 'fail')
variant('x.l23s2.release_deletes', L23, 2, [('        T* p = ptr_;\n        ptr_ = nullptr;\n        return p;', '        delete ptr_;\n        ptr_ = nullptr;\n        return nullptr;')], 'fail')
variant('x.l23s2.reset_deletes_first', L23, 2, [('        T* old = ptr_;\n        ptr_ = p;\n        delete old;', '        delete ptr_;\n        ptr_ = p;')], None)
SP_COPY = '        if (count_ != other.count_) {\n            T* p = other.ptr_;      // read the source first: the old object may own it\n            long* c = other.count_;\n            if (c) ++*c;\n            drop();\n            ptr_ = p;\n            count_ = c;\n        }'
variant('x.l23s5.copy_drop_first_guarded', L23, 5, [(SP_COPY, '        if (this != &other) {\n            drop();\n            ptr_ = other.ptr_;\n            count_ = other.count_;\n            if (count_) ++*count_;\n        }')], 'fail')
variant('x.l23s5.copy_drop_first', L23, 5, [(SP_COPY, '        {\n            drop();\n            ptr_ = other.ptr_;\n            count_ = other.count_;\n            if (count_) ++*count_;\n        }')], 'fail')
variant('x.l23s5.copy_add_first_no_guard', L23, 5, [('        if (count_ != other.count_) {', '        {')], None)
variant('x.l23s5.move_drop_first', L23, 5, [('            T* p = other.ptr_;      // take the source first: the old object may own it\n            long* c = other.count_;\n            other.ptr_ = nullptr;\n            other.count_ = nullptr;\n            drop();\n            ptr_ = p;\n            count_ = c;', '            drop();\n            ptr_ = other.ptr_;\n            count_ = other.count_;\n            other.ptr_ = nullptr;\n            other.count_ = nullptr;')], 'fail')
variant('x.l23s5.copy_no_increment', L23, 5, [('        if (count_) ++*count_;\n    }\n    SharedPtr& operator=(const SharedPtr& other)', '    }\n    SharedPtr& operator=(const SharedPtr& other)')], 'fail')
variant('x.l23s5.counter_never_freed', L23, 5, [('            delete ptr_;\n            delete count_;', '            delete ptr_;')], 'fail')
H5 = 'homework-5.json'
variant('x.h5i0.source_stays_active', H5, 0, [('        other.active_ = false;\n', '')], 'fail')
variant('x.h5i0.move_not_noexcept', H5, 0, [('ScopeGuard(ScopeGuard&& other) noexcept :', 'ScopeGuard(ScopeGuard&& other) :')], 'fail')
variant('x.h5i1.plain_move_on_growth', H5, 1, [('std::move_if_noexcept(data_[i])', 'std::move(data_[i])')], 'test-15')  # re-pointed (fix pass, finding 10): the Wobbly test
variant('x.h5i1.forward_cast_on_growth', H5, 1, [('std::move_if_noexcept(data_[i])', 'static_cast<T&&>(data_[i])')], 'test-15')  # fix pass
variant('x.h5i1.trait_dispatch', H5, 1, [('new (fresh + i) T(std::move_if_noexcept(data_[i]));', 'if constexpr (std::is_nothrow_move_constructible_v<T> || !std::is_copy_constructible_v<T>) new (fresh + i) T(std::move(data_[i])); else new (fresh + i) T(data_[i]);')], None)  # fix pass
variant('x.h5i1.trait_dispatch_noexcept_only', H5, 1, [('new (fresh + i) T(std::move_if_noexcept(data_[i]));', 'if constexpr (std::is_nothrow_move_constructible_v<T>) new (fresh + i) T(std::move(data_[i])); else new (fresh + i) T(data_[i]);')], None)  # fix pass: no hidden T is move-only
variant('x.h5i1.copy_on_growth', H5, 1, [('T(std::move_if_noexcept(data_[i]))', 'T(data_[i])')], 'fail')
variant('x.h5i1.build_after_free', H5, 1, [('            new (fresh + size_) T(std::forward<U>(x));      // x may live in the old block, so build it first\n', ''), ('            data_ = fresh;\n            cap_ = new_cap;', '            data_ = fresh;\n            cap_ = new_cap;\n            new (data_ + size_) T(std::forward<U>(x));')], 'fail')
variant('x.h5i9.sole_assign_deletes_first', H5, 9, [('        T* taken = other.release();   // take the source first: the old object may own it\n        T* old = ptr_;\n        ptr_ = taken;\n        delete old;', '        if (this != &other) { delete ptr_; ptr_ = other.ptr_; other.ptr_ = nullptr; }')], 'fail')
variant('x.h5i9.counted_from_sole_no_release', H5, 9, [('CountedPtr(SolePtr<T>&& s) : CountedPtr(s.release()) {}', 'CountedPtr(SolePtr<T>&& s) : CountedPtr(s.get()) {}')], 'fail')

# --- base run: every code widget's solution passes its hidden tests and its starter fails them
FILES = ['l14-vector', 'l15-maps', 'l16-algorithms', 'l17-cmake', 'l18-unit-tests', 'l19-moving-not-copying', 'l20-rule-of-five', 'l21-virtual-dispatch',
         'l22-undefined-behaviour', 'l23-own-smart-pointer', 'review-4', 'review-5', 'homework-4', 'homework-5']
BASE = []
def _walk(o, p, out):
    if isinstance(o, list):
        for i, v in enumerate(o): _walk(v, '%s[%d]' % (p, i), out)
    elif isinstance(o, dict):
        if o.get('kind') == 'code' and isinstance(o.get('tests'), list): out.append((p, o))
        for k, v in o.items(): _walk(v, (p + '.' + k) if p else k, out)
for _f in FILES:
    _found = []
    _walk(json.load(open(os.path.join(CPP, _f + '.json'))), '', _found)
    for _p, _w in _found:
        assert _w.get('language') == 'cpp', (_f, _p)
        _n = 'base.%s.%s' % (_f, _p)
        grade(_n + '.solution', _f + '.json', _p, '@solution')
        grade(_n + '.starter', _f + '.json', _p, '@starter')
        BASE.append(_n)

# ---------------------------------------------------------------------------------------------------------------
# 3. Checks. `finding=N` marks a check that fails because the content is wrong (docs/reviews/audit-cpp-4-5.md).
# ---------------------------------------------------------------------------------------------------------------
R = run_jobs()
if DUMP:
    for k in sorted(R):
        print(k, json.dumps(R[k])[:1200])

def have(*names):
    return all(n in R for n in names)
def K(name):
    return kv(R[name])
def key(name):
    return R[name].get('key')
def stopped(name, text=None):
    r = R[name]
    return (r.get('code') not in (0, None) or bool(r.get('trap'))) and (text is None or text in (r.get('err') or ''))

def load(file):
    return json.load(open(os.path.join(CPP, file)))

# ---- level 4 ---------------------------------------------------------------------------------------------
if have('vec'):
    v = K('vec')
    check('l14 screens[1] explain: the block grows 1, 2, 4, 8', v['caps'] == '1,2,4,8,')
    check('l14 screens[2] explain: without reserve 600 pushes move the block 10 times and copy 1,023 elements', (v['moves'], v['copied'], v['cap600']) == ('10', '1023', '1024'))
    check('l14 screens[2] byKey.eleven: 11 allocations without reserve', v['allocs'] == '11')
    check('l14 screens[2] key: after reserve(1000) the block never moves; size stays 0 after reserve', (v['res_cap'], v['res_size0'], v['res_same']) == ('1000', '0', '1'))
    check('review-4 r4-capacity: capacity 1, 2, 4, 4, 8; reserve(5) gives 5', v['caps5'] == '1,2,4,4,8,' and v['capr5'] == '5')
    check('homework-4 h4-reserve-grow: reserve(100) then 150 pushes gives 200', (v['h100'], v['h150']) == ('100', '200'))
    check('l14 quiz q-sized-ctor: v(3) then push_back gives size 4, first element 0', (v['zsize'], v['z0']) == ('4', '0'))
    check('l14 screens[4] explain: size() - 1 of an empty vector is 4,294,967,295 here; size_t is 4 bytes', (v['wrap'], v['sizeof_size_t']) == ('4294967295', '4'))
    check('l14 screens[4] byKey.test-5: five pushes without reserve leave capacity 8', v['cap_no_reserve_5'] == '8')
    check('l14 screens[5] key: 101.5 + 99.8 + 102.3 = 303.6', v['iter_total'] == '303.6')
    check('l14 screens[0] key: prints 3 102', v['first'] == '3 102')
    # re-pointed (fix pass, finding 2): the hint and line now say 3 closes and n = 5
    _t3 = load('l14-vector.json')['screens'][3]['widget']['tests'][3]['args']
    check('l14 screens[3] hints[1] and byKey.test-4: with 3 closes and n = 5, xs.size() - n wraps (and 3u - 4 + 1 is 0)', v['size_minus_5_plus_1'] == '4294967295' and v['size_minus_n_plus_1'] == '0' and _t3 == [[100, 101, 102], 5],
          'size_minus_5_plus_1 %s, tests[3].args %s' % (v['size_minus_5_plus_1'], _t3), finding=2)
if have('l14s3.count_wraps_to_zero', 'x.fix_ma_n5'):
    check('l14 screens[3] tests: the loop `i < xs.size() - n + 1` (with n < 1 guarded) is rejected', key('l14s3.count_wraps_to_zero') is not None,
          'it passes all 7 hidden tests and stops only when n >= size + 2', finding=2)
    check('l14 screens[3] proposed test (3 closes, n = 5): the same loop stops', stopped('x.fix_ma_n5', 'index out of bounds'))
if have('erase_loop'):
    e = K('erase_loop')
    check('l14 screens[8] key: 101.2, 0, 101.5 in this app; the fixed loop gives 101.2, 101.5', (e['ticks'], e['fixed']) == ('101.2,0,101.5,', '101.2,101.5,'))
    check('review-4 r4-erase options[idx]: two negatives in a row leave one behind', e['idx'] == '1,-3,4,')
if have('idx_oob', 'at_oob', 'at_neg', 'reserve_wrap', 'ctor_wrap'):
    check('l14 screens[7] explain: this app traps [] past the end as a crash', stopped('idx_oob', 'vector[] index out of bounds') and R['idx_oob'].get('trap'))
    check('l14 screens[7], quiz q-at-end: at(3) throws std::out_of_range and the program ends', stopped('at_oob', 'std::out_of_range'))
    check('l14 screens[7] byKey.test-4: at(-1) throws std::out_of_range', stopped('at_neg', 'std::out_of_range'))
    check('l14 screens[4] byKey.test-3: reserve(size() - 1) on an empty vector ends the program', stopped('reserve_wrap', 'std::length_error'))
    check('l18 screens[5] byKey.test-1: out(px.size() - 1) on an empty vector stops with std::length_error', stopped('ctor_wrap', 'std::length_error'))
if have('maps'):
    m = K('maps')
    check('l15 screens[0] key: AZN, BARC, VOD', m['order'] == 'AZN,BARC,VOD,')
    check('l15 screens[6] key: flat AZN then 3', (m['flat'], m['size_after_read']) == ('1', '3'))
    check('l15 screens[8] key: insert keeps 500; emplace too', (m['after_insert'], m['inserted'], m['after_emplace']) == ('500', '0', '500'))
    check('l15 screens[9] key: three levels; 100.1 + 0.1 is 100.19999999999999', (m['levels'], m['sum'], m['lit']) == ('3', '100.19999999999999', '100.2'))
    check('review-4 r4-count: size 1, count 0, VOD is 0', m['r4count'] == '1 0 0')
    check('l15 quiz q-empty-begin: begin() == end() on an empty map', m['empty_begin_is_end'] == '1')
    check('l15 screens[4] byKey.test-3: a flat symbol keeps its key', m['flat_key_stays'] == '1')
    check('l15 quiz q-order: unordered_map order is not insertion order here', m['uorder'] != 'VOD,BARC,AZN,')
if have('x.map_depth'):
    d = K('x.map_depth')
    check('l15 screens[1] explain: the drawn tree (HSBA, BARC, SHEL, AZN, BP, LLOY, VOD) needs at most 3 comparisons', d['depth7_lesson_order'] == '3')
    # re-pointed (fix pass, finding 20): "this tree of 7 keys needs at most 3 steps"; "a million keys need 20 to 40"
    check('l15 screens[1] explain: a std::map of 7 keys can sit deeper than the drawn tree (at most 2 log2(8) = 6)', 3 < int(d['depth7_sorted_inserts']) <= 6,
          '7 keys inserted in sorted order sit ' + d['depth7_sorted_inserts'] + ' deep', finding=20)
    check('l15 screens[1] explain, summary.formula.note: a million keys need 20 to 40 comparisons', 20 <= int(d['depth_million_random']) <= 40 and 20 <= int(d['depth_million_sorted']) <= 40 and 2 * math.log2(1e6 + 1) <= 40,
          'sorted inserts: ' + d['depth_million_sorted'] + '; random inserts: ' + d['depth_million_random'] + ' (a red-black tree is at most 2 log2(n + 1) deep)', finding=20)
if have('algos'):
    a = K('algos')
    check('l16 screens[7] key: accumulate(..., 0) is 173, an int; steps 120, 79, 154, 143, 173', (a['acc_int'], a['acc_int_is_int'], a['steps']) == ('173', '1', '120,79,154,143,173,'))
    check('l16 screens[1] key: accumulate(..., 0.0) is 175', a['acc_dbl'] == '175')
    check('review-4 r4-acc-int: 8', a['fees'] == '8')
    check('homework-4 h4-capture: n is 3; with [&limit] it is 0', (a['count_snapshot'], a['count_ref']) == ('3', '0'))
    check('l16 screens[5] canvas: adjacent_difference gives 100, 4, -3, 5, -3', a['adj'] == '100,4,-3,5,-3,')
    check('l16 quiz q-partial: 50, 30, 65; adjacent_difference 50, -70, 55', (a['partial'], a['adjdiff']) == ('50,30,65', '50,-70,55'))
    check('l16 screens[3] canvas: value 40,300', a['inner'] == '40300')
    check('l16 screens[0] key order', a['sorted'] == 'mr,mo,tr,va,ca,')
    check('l16 screens[8] key: max_element of an empty range is end()', a['max_empty_is_end'] == '1')
    check('l16 screens[9] explain: a mutable by-value capture returns 0; by reference 150', (a['mutable_copy_worst'], a['ref_worst']) == ('0', '150'))
    check('l16 screens[3] byKey.test-3: 0.0 / 0.0 is NaN', a['zero_over_zero_is_nan'] == '1')
if have('capture_by_value_assign'):
    check('l16 screens[9] explain: with [peak, worst] the assignments do not compile', not R['capture_by_value_assign']['ok'] and 'captured by copy' in R['capture_by_value_assign']['diag'])
if have('transform_empty'):
    t = K('transform_empty')
    check('l16 screens[6] key, in this app: size stays 0 and the run goes on', (t.get('size_after'), t.get('alive')) == ('0', '1'))
    # re-pointed (fix pass, finding 14): the question now says "in this app's run" and the key names the desktop crash
    _q6 = load('l16-algorithms.json')['screens'][6]
    check('l16 screens[6] question says "in this app\'s run"; begin() is a null pointer, so a desktop write faults', t.get('begin_is_null') == '1' and "in this app's run" in _q6['question'] and 'desktop build usually crashes' in _q6['feedback']['correct'],
          'pence.begin() is a null pointer: this app writes at address 0 without complaint, a desktop build faults on the first write', finding=14)
if have('max_empty_deref'):
    check('l16 screens[8] explain: reading through end() printed nothing at all here', 'v=' not in (R['max_empty_deref'].get('out') or ''))
if have('sort_le3', 'sort_le_many', 'sort_le_int'):
    # re-pointed (fix pass, finding 7): the why now says the three prices sort and longer ranges stop
    check('l16 quiz q-le options[fine].why: the three prices sort quietly to 99.8, 100.5, 100.5', not stopped('sort_le3') and K('sort_le3').get('out', '').startswith('99.8,100.5,100.5'),
          'the three prices sort without a stop (' + K('sort_le3').get('out', '') + '); the stop comes on longer ranges', finding=7)
    check('l16 quiz q-le, l22 screens[8]: with <= on a longer range the library stops with a strict-weak-ordering message', stopped('sort_le_many', 'strict-weak ordering') and stopped('sort_le_int', 'strict-weak ordering'))
    # re-pointed (fix pass, finding 7): test 4 is now about the tie order; the stop is test 6 (40 orders)
    check('l16 screens[4] byKey.test-4: six equal elements with <= do not stop (so test 4 speaks of tie order only)', 'n6_after' in K('sort_le_many'),
          'six equal elements sort without a stop; the message first appears at 30', finding=7)
if have('l16s4.time_le', 'l16s4.ge_then_le', 'l16s4.price_ge'):
    # re-pointed (fix pass, finding 7)
    check('l16 screens[4] byKey.test-6: a tie-break with <= fails test 6 first', key('l16s4.time_le') == 'test-6' and key('l16s4.ge_then_le') == 'test-6',
          'keys: time_le %s, ge_then_le %s, price_ge %s' % (key('l16s4.time_le'), key('l16s4.ge_then_le'), key('l16s4.price_ge')), finding=7)
    check('l16 screens[4] tests reject a non-strict rule', key('l16s4.time_le') is not None and key('l16s4.ge_then_le') is not None, 'both pass all 5 tests', finding=7)
if have('x.fix_sort40_time_le', 'x.fix_sort40_price_ge', 'x.fix_sort40_strict'):
    check('l16 screens[4] proposed test (40 identical orders): <= and >= stop with the message, the strict rule passes',
          stopped('x.fix_sort40_time_le', 'strict-weak ordering') and stopped('x.fix_sort40_price_ge', 'strict-weak ordering') and K('x.fix_sort40_strict').get('after') == '40')
if have('l16s3.int_start', 'x.fix_misc'):
    check('l16 screens[3] tests reject accumulate and inner_product started at the int 0 (the lesson\'s own trap)', key('l16s3.int_start') is not None, 'passes all 5 tests', finding=8)
    f = K('x.fix_misc')
    check('l16 screens[3] proposed test vwap({10.25, 10.75}, {3, 1}) = 10.375 catches the int start (10)', (f['vwap_int_start'], f['vwap_dbl_start']) == ('10', '10.375'))
    check('homework-4 h4-vwap-book proposed test: unordered_map prints AZN, BP, SHEL out of order when they arrive in order', f['unordered_alpha_in'] != 'AZN,BP,SHEL,')
if have('h4i0.unordered', 'h4i0.unweighted'):
    check('homework-4 h4-vwap-book tests reject std::unordered_map', key('h4i0.unordered') is not None, 'passes all 5 tests: every test happens to insert its symbols in reverse alphabetical order', finding=9)
    # re-pointed (fix pass, finding 11)
    check('homework-4 h4-vwap-book byKey.test-1: the unweighted mean fails test 1 first (VOD 72.3000)', key('h4i0.unweighted') == 'test-1', 'it fails ' + str(key('h4i0.unweighted')) + ' first', finding=11)
if have('l16s5.counts_d0'):
    # re-pointed (fix pass, finding 11): the test-1 line names it; test 4 is now descriptive
    check('l16 screens[5] byKey.test-1: counting d[0] fails test 1 first', key('l16s5.counts_d0') == 'test-1', 'it fails ' + str(key('l16s5.counts_d0')) + ' first', finding=11)
if have('l17s5.int_division'):
    # re-pointed (fix pass, finding 11)
    check('l17 screens[5] byKey.test-1: dividing two ints fails test 1 first', key('l17s5.int_division') == 'test-1', 'it fails ' + str(key('l17s5.int_division')) + ' first (90 / 360 is also 0)', finding=11)
if have('doubles'):
    d = K('doubles')
    check('l18 screens[7] key: 110.0 / 100.0 - 1 is 0.10000000000000009, not 0.1', (d['rise'], d['rise_eq_01'], d['rise_close']) == ('0.10000000000000009', '0', '1'))
    check('review-4 r4-tol: (10.1 + 10.2) / 2 is 10.149999999999999, not 10.15', (d['mid'], d['mid_eq'], d['vwap_eq']) == ('10.149999999999999', '0', '0'))
    check('l18 screens[3], quiz q-tol: Black-Scholes 10.4506 to four places', abs(float(d['bs']) - 10.4506) < 5e-5 and '%.6f' % float(d['bs']) == '10.450584')
    check('l18 screens[9] canvas: 100 steps 10.430612, 2,000 steps 10.449584', ('%.6f' % float(d['crr100']), '%.6f' % float(d['crr2000'])) == ('10.430612', '10.449584'))
    check('l18 screens[9] byKey.test-3: 99 steps give 10.4683, and 1,999 steps stay within 0.002 of Black-Scholes', '%.4f' % float(d['crr99']) == '10.4683' and abs(float(d['crr1999']) - 10.450584) < 0.002)
    check('l18 screens[9] byKey.test-1: 1e-6 holds for the pin, 1e-7 does not', 1e-7 < abs(float(d['crr100']) - 10.430612) < 1e-6)
    # re-pointed (fix pass, finding 3): "the true value is 10.450584, 0.000016 from the pin, so == or 1e-5 fails"
    check('l18 screens[3] byKey.test-1: the true value is 10.450584, 0.000016 from the pin', '%.6f' % float(d['bs']) == '10.450584' and round(abs(float(d['bs']) - 10.4506), 6) == 0.000016 and 1e-5 < abs(float(d['bs']) - 10.4506) < 2e-5,
          '|10.450584 - 10.4506| is 1.6e-5, so any tolerance from 2e-5 up passes', finding=3)
    check('l22 screens[2] byKey.t2, homework-5: -7 / 2 is -3 and 7 / 2 is 3', (d['neg7_div_2'], d['seven_div_2']) == ('-3', '3'))
    check('l17 screens[4] tests: discount factor, forward and the two present values', d['df'] == '0.9048374180359595' and abs(float(d['fwd']) - 105.12710963760242) < 1e-11 and abs(float(d['pv3']) - 102.54617478299633) < 1e-11 and abs(float(d['pv1']) - 98.51119396030627) < 1e-11)
if have('l18s3.tol_2e-5', 'l18s3.tol_5e-5', 'l18s3.tol_1e-5', 'l18s3.eq'):
    # re-pointed (fix pass, finding 3)
    check('l18 screens[3] byKey.test-1 (graded): tolerances 2e-5 and 5e-5 pass, so the line no longer names them', key('l18s3.tol_2e-5') is None and key('l18s3.tol_5e-5') is None, 'both pass every test; 1e-5 and == fail test 1', finding=3)
    check('l18 screens[3] byKey.test-1: == and 1e-5 fail test 1', key('l18s3.eq') == 'test-1' and key('l18s3.tol_1e-5') == 'test-1')
if have('l18s4.eq_exact', 'l18s4.percent'):
    # re-pointed (fix pass, finding 12): the line now names == as well
    check('l18 screens[4] byKey.test-2: CHECK(r[0] == 0.1) fails test 2, as the line now says', key('l18s4.eq_exact') == 'test-2',
          'CHECK(r[0] == 0.1), with the right hand value, also fails test 2 first', finding=12)
    check('l18 screens[4] byKey.test-2: a wrong hand value (10.0) fails test 2', key('l18s4.percent') == 'test-2')
check('l17 screens[6], quiz q-mixed: 1.28 / 0.16 = 8; 4.1 / 0.16 is about 26; 4.1 / 1.3 is about 3', abs(1.28 / 0.16 - 8) < 1e-12 and round(4.1 / 0.16) == 26 and round(4.1 / 1.3) == 3 and abs(1.28 - 0.16 - 1.12) < 1e-12)
check('review-4 r4-which-map, l15 quiz q-cache: log2(4,000) is about 12 and log2(40,000) about 16 (best case of a balanced tree)', round(math.log2(4000)) == 12 and math.ceil(math.log2(40000)) == 16)
check('homework-4 h4-vwap-book expects: 72.26, 210.6667, 4.77, 27.09, 6.425; unweighted BP 4.75',
      all(abs(x - y) < 5e-5 for x, y in (((72.1 * 500 + 72.5 * 300 + 72.3 * 200) / 1000, 72.26), ((210.5 * 200 + 211 * 100) / 300, 210.6667), ((4.75 * 1000 + 4.8 * 3000 + 4.7 * 1000) / 5000, 4.77), ((27.15 * 400 + 27.05 * 600) / 1000, 27.09), ((6.42 * 100 + 6.40 * 100 + 6.44 * 200) / 400, 6.425), ((4.75 + 4.8 + 4.7) / 3, 4.75))))
check('homework-4 h4-test-drawdown: worst fall 0.25 (120 to 90), last 0.2 (130 to 104)', abs((120 - 90) / 120 - 0.25) < 1e-15 and abs((130 - 104) / 130 - 0.2) < 1e-15)
if have('linker_names_caller_symbol'):
    dg = R['linker_names_caller_symbol']['diag']
    # re-pointed (fix pass, finding 5): the prose now says a `risk` function
    check('homework-4 h4-two-libs prose: with `report` linked to nothing the linker reports a `risk` function', 'risk' in dg and 'pricing' not in dg and 'undefined reference to a `risk` function' in load('homework-4.json')['items'][5]['prose'],
          'the linker names what report.o itself calls, a risk function: ' + ' '.join(l for l in dg.split('\n') if 'undefined symbol' in l)[:120], finding=5)

# ---- level 5 ---------------------------------------------------------------------------------------------
if have('tracked', 'tracked_throwing'):
    t, u = K('tracked'), K('tracked_throwing')
    check('l19 screens[0] key: lines 2, 5, 8 copy; 3 and 6 move; 4 and 7 run neither', [t['l%d' % i] for i in range(2, 9)] == ['1,0', '0,1', '0,0', '1,0', '0,1', '0,0', '1,0'])
    check('l19 screens[2] key: std::move alone runs nothing', t['cast_only'] == '0,0')
    check('l19 screens[3] key: four pushes, noexcept move: 0 copies, 7 moves, capacity 1, 2, 4, 4', (t['four_pushes'], t['caps']) == ('0,7', '1,2,4,4,'))
    check('l19 screens[4] key: move not noexcept, two pushes: 1 copy, 2 moves', u['two_pushes'] == '1,2')
    check('l19 screens[6], quiz q-const-move, review-5 r5-take-copies: a const source copies', (t['const_move'], t['take_const'], t['take_move_const'], t['take_temp']) == ('1,0', '1,0', '1,0', '0,0'))
    check('l19 quiz q-return-move: return t runs 0 moves, return std::move(t) runs 1', (t['ret_plain'], t['ret_move']) == ('0,0', '0,1'))
    check('review-5 r5-growth-copies: emplace_back still copies on growth; reserve stops the copies', u['four_emplace'].startswith('3,') and u['four_reserved'].startswith('0,'))
    # re-pointed (fix pass, finding 13): "if their move is noexcept, or if they cannot be copied"
    check('l19 summary.ideas[2]: a vector also moves a type it cannot copy, even with a throwing move', u['move_only_throwing_moves'] != '0' and 'or if they cannot be copied' in load('l19-moving-not-copying.json')['summary']['ideas'][2],
          'a move-only type with a throwing move is still moved on growth (%s moves in 4 pushes): the copy needs a copy constructor' % u['move_only_throwing_moves'], finding=13)
if have('special'):
    s = K('special')
    table = load('l20-rule-of-five.json')['screens'][1]['canvas']['params']['rows']
    got = [s[k].split(',') for k in ('nothing', 'dtor', 'copy_ctor', 'copy_assign', 'move_ctor', 'move_assign', 'all_five')]
    check('l20 screens[1] canvas: all 28 cells of the special-member table', [r[1:] for r in table] == got, str(got))
    check('l20 screens[1] key: b = std::move(a) really moves in 2 of the six rows that declare something', sum(1 for g in got[1:] if g[3] == 'move') == 2)
    check('l20 screens[0] key: only Fill b = std::move(a) compiles with a lone move constructor', got[4] == ['error', 'move', 'error', 'error'])
    check('l20 screens[2] key: A move, B copy, C copy, D move', [got[0][1], got[1][1], got[2][1], got[4][1]] == ['move', 'copy', 'copy', 'move'])
    h5 = load('homework-5.json')['items'][4]['widget']['rows']
    want = {'a copy assignment': got[3], 'a move assignment': got[5], 'a move constructor': got[4], 'a destructor': got[1]}
    check('homework-5 h5-members-table: all 12 cells', all([c['answer'] for c in row[1:]] == want[row[0]][1:] for row in h5))
    check('l20 screens[3] key, review-5 r5-defaulted-nothrow: Pos is nothrow move constructible, Pos3 is not', (s['pos_nothrow'], s['pos3_nothrow'], s['string_nothrow'], s['vector_nothrow']) == ('1', '0', '1', '1'))
    # re-pointed (fix pass, finding 13): the canvas now draws `Pos3(const Pos3&) = default;`
    _c3 = load('l20-rule-of-five.json')['screens'][3]['canvas']['params']['lines']
    check('l20 screens[3] explain: the hand-written Pos3, drawn with a defaulted copy, makes the vector copy', '    Pos3(const Pos3&) = default;' in _c3 and s['pos3_with_copy_growth'].split(',')[0] == '3' and s['pos3_like_growth'].split(',')[0] == '0',
          'Pos3 as drawn is not copy constructible (%s), so the vector moves it: copies,moves = %s; with a defaulted copy added: %s' % (s['pos3_copyable'], s['pos3_like_growth'], s['pos3_with_copy_growth']), finding=13)
    check('l20 screens[3] proposed canvas line `Pos3(const Pos3&) = default;`: the vector then copies on growth', s['pos3_with_copy_growth'].split(',')[0] == '3')
    check('review-5 r5-order-compiles: only `Order d;` compiles', s['order'] == '1,0,0,0,0')
    check('l20 quiz q-unique-class: movable, not copyable', s['holder'] == '0,1')
if have('order_move_deleted', 'fill_move_ctor_only_ok'):
    check('l20 screens[7] key: Order b = std::move(a) selects the deleted copy constructor', not R['order_move_deleted']['ok'] and 'implicitly-deleted copy constructor' in R['order_move_deleted']['diag'])
    check('l20 screens[0]: the move line compiles; the other three do not', R['fill_move_ctor_only_ok']['ok'] and not any(R['fill_move_ctor_only_' + n]['ok'] for n in ('copy', 'assign', 'move_assign')))
if have('samples_no_guard', 'l20s5.no_guard_alloc_first'):
    g = K('samples_no_guard')
    # re-pointed (fix pass, finding 1): the quiz now asks about a free-first assignment; Samples is safe without the guard
    check('l20 quiz q-self-guard explain: the lesson\'s Samples (allocate first) is safe for a = a without the guard', (g.get('size'), g.get('sum')) == ('10', '15') and 'frees its old block first' in [q for q in load('l20-rule-of-five.json')['quiz'] if q['id'] == 'q-self-guard'][0]['prose'],
          'the lesson\'s copy assignment allocates and copies before it frees: a = a without the guard leaves size 10 and the data intact', finding=1)
    # re-pointed (fix pass, finding 1)
    check('l20 quiz q-self-guard explain (graded): the lesson\'s solution with the guard removed passes every hidden test', key('l20s5.no_guard_alloc_first') is None, 'it passes all 13 tests, a = a included', finding=1)
if have('x.l19s5.no_self_guard'):
    check('l19 screens[8] explain: the move assignment needs its guard (a = std::move(a) otherwise loses the block)', key('x.l19s5.no_self_guard') == 'test-8')
if have('virtuals', 'linux64_sizes', 'win64_D_is_24', 'win64_D_is_16', 'win64_long_is_4', 'win64_long_is_8'):
    v = K('virtuals')
    check('l21 sizes here: Tick 4, VTick 8, B 8, D 12, Quote 24, W 8; review-5 S 8; homework-5 B{double} 16', [v[k] for k in ('Tick', 'VTick', 'B', 'D', 'Quote', 'W', 'S', 'BD')] == ['4', '8', '8', '12', '24', '8', '8', '16'])
    check('l19 screens[1] explain: Buffer is 8 bytes here; l23 screens[3]: unique_ptr 4, shared_ptr 8', (v['Buffer'], v['unique'], v['shared']) == ('8', '4', '8'))
    check('64-bit Linux (Itanium ABI): B 16, D 16, Quote 24, W 16, S 16, VTick 16, Buffer 16, long 8', R['linux64_sizes']['ok'])
    # re-pointed (fix pass, finding 16): 16 on 64-bit Linux and macOS, 24 on 64-bit MSVC
    check('l21 screens[2] explain and byKey.sixteen: D is 16 on 64-bit Linux, 24 on 64-bit MSVC', R['win64_D_is_24']['ok'] and not R['win64_D_is_16']['ok'] and R['linux64_sizes']['ok'],
          'x86-64 Windows (MSVC ABI) gives 24: it does not reuse the padding after x', finding=16)
    # re-pointed (fix pass, finding 17)
    check('l22 screens[2] byKey.t3: sizeof(long) is 4 on 64-bit Windows and 8 on 64-bit Linux', R['win64_long_is_4']['ok'] and not R['win64_long_is_8']['ok'] and R['linux64_sizes']['ok'], 'it is 4 on 64-bit Windows (LLP64)', finding=17)
    check('l21 screens[4], quiz q-vector-slice, homework-5: a sliced copy runs the base version; a reference or unique_ptr runs Call', (v['sliced'], v['vector_slice'], v['via_ref'], v['via_unique']) == ('-1', '-1', '10', '10'))
    check('l21 screens[7] key: d.who is "Base"', (v['ctor_call'], v['later_call']) == ('Base', 'Derived'))
    check('l22 screens[2] byKey.t3: sizeof(long) is 4 here', v['long'] == '4')
if have('ub_null_check', 'ub_null_read', 'ub_misc'):
    check('l22 screens[0] canvas: the null test after the read is gone (first(nullptr) does not return -1) and nothing crashes', (K('ub_null_check').get('is_minus_one'), K('ub_null_check').get('alive')) == ('0', '1'))
    check('l22 screens[5] options[crash].why: this app reads address 0 without complaint', K('ub_null_read').get('alive') == '1')
    m = K('ub_misc')
    check('l22 screens[1], [2], [6]: u - 1, UINT_MAX + 1u, 1u << 31, size() - 1', (m['u_minus_1'], m['uint_max_plus_1'], m['one_shl_31'], m['size_minus_1']) == ('4294967295', '0', '2147483648', '4294967295'))
    check('l22 screens[4] explain: this app\'s compiler removes the check `a + b < a` made after the addition', (m['after_check_max'], m['after_check2_max']) == ('0', '0'))
    check('l22 screens[10], review-5: 2,500,000,000 pence is 352,516,353 over INT_MAX', (m['pence'], m['over'], m['int_max']) == ('2500000000', '352516353', '2147483647'))
if have('l22s4.after_sign', 'l22s4.after_sum_lt', 'l22s4.wide', 'l22s4.unsigned_wrap'):
    check('l22 screens[4] feedback.correct, explain: a check made after the addition is rejected by the hidden tests', key('l22s4.after_sign') is not None,
          'the sign test after `int s = a + b` passes all 13 tests and is told "Your check never overflows"; only the `s < a` form is removed by the compiler (%s)' % key('l22s4.after_sum_lt'), finding=6)
    check('l22 screens[4]: defined alternatives (long long sum, unsigned wrap) pass', key('l22s4.wide') is None and key('l22s4.unsigned_wrap') is None)
if have('x.fix_constexpr_defined', 'x.fix_constexpr_after_sign'):
    check('l22 screens[4] proposed fix: as a constexpr function the defined check passes a static_assert and the after-the-sum check does not compile',
          R['x.fix_constexpr_defined']['ok'] and not R['x.fix_constexpr_after_sign']['ok'] and 'outside the range' in R['x.fix_constexpr_after_sign']['diag'])
if have('smart', 'shared_base_no_virtual'):
    s = K('smart')
    check('l23 screens[0], [9], quiz q-make-shared: shared_ptr(new T) allocates twice, make_shared once; a copy allocates nothing', (s['shared_new'], s['make_shared'], s['copy_allocs']) == ('2', '1', '0'))
    check('l23 quiz q-weak-count: 2; review-5 part 0: 2; l23 screens[7] (std::shared_ptr agrees): 1', (s['weak_count'], s['moved_count'], s['move_assign_count'], s['a_count']) == ('2', '2', '1', '0'))
    check('l23 screens[5] solution comment: use_count of an empty pointer is 0', s['empty_count'] == '0')
    check('review-5 r5-virtual-dtor options[shared].why: shared_ptr<Base> from make_shared<Derived> runs ~Derived without a virtual destructor', K('shared_base_no_virtual')['shared_runs_derived'] == '1')
if have('abstract_middle_class', 'abstract_middle_instantiated'):
    # re-pointed (fix pass, finding 18): "a derived class must override value before it can be built"
    check('l21 quiz q-abstract key: a middle class may stay abstract; the built class overrides value', R['abstract_middle_class']['ok'],
          'a derived class may leave it pure and stay abstract; only a class that is built must have it overridden', finding=18)
    check('l21 quiz q-abstract: an abstract class cannot be built', not R['abstract_middle_instantiated']['ok'])
check('l23 screens[9] key: 400,000 and 200,000 allocations, 10 ms saved', 200000 * 2 == 400000 and 200000 * 50e-9 * 1e3 == 10)
check('l19 screens[1] explain: 8,000,000 bytes at 10 GB/s is 0.8 ms; homework-5 model: 1,000 x 1,000 doubles is 8 MB', 1e6 * 8 / 10e9 * 1e3 == 0.8 and 1000 * 1000 * 8 == 8_000_000)
check('l22 screens[10]: INT_MAX pence is 21,474,836.47 pounds; unsigned doubles it to 42,949,672.95', round(2147483647 / 100, 2) == 21474836.47 and round(4294967295 / 100, 2) == 42949672.95 and 2 ** 53 > 2_500_000_000)

# ---- fix pass: new hidden tests and the values they encode -------------------------------------------------
_h5 = load('homework-5.json')['items'][1]['widget']
check('homework-5 h5-vec Wobbly test: 8 pushes move 8 temporaries in, growth at 1, 2, 4 copies 1 + 2 + 4 = 7 (708)',
      _h5['tests'][-1]['expect'] == 708 == (1 + 2 + 4) * 100 + 8 and 'Wobbly(Wobbly&& o) :' in _h5['prelude'] and 'Wobbly(Wobbly&& o) noexcept' not in _h5['prelude'])
if have('x.h5i1.plain_move_on_growth'):
    check('homework-5 h5-vec: a Vec that always moves on growth fails the Wobbly test (test 15)', key('x.h5i1.plain_move_on_growth') == 'test-15', str(key('x.h5i1.plain_move_on_growth')), finding=10)
_l22 = load('l22-undefined-behaviour.json')['screens'][4]['widget']
check('l22 screens[4]: starter and solution are constexpr and the last two tests are static_assert probes',
      'constexpr bool add_overflows' in _l22['starter'] and 'constexpr bool add_overflows' in _l22['solution'] and [c.get('compiles', '')[:14] for c in _l22['tests'][13:]] == ['static_assert('] * 2 and len(_l22['tests']) == 15)
if have('l22s4.after_sign'):
    check('l22 screens[4]: the sign test after the sum now fails a compile-time test (test 14)', key('l22s4.after_sign') == 'test-14', str(key('l22s4.after_sign')), finding=6)
check('l16 screens[3] test 6: vwap({10.25, 10.75}, {3, 1}) = 41.5 / 4 = 10.375; an int total gives 40 / 4 = 10',
      abs((10.25 * 3 + 10.75 * 1) / 4 - 10.375) < 1e-15 and int(int(10.25 * 3) + 10.75 * 1) / 4 == 10)
check('homework-4 h4-vwap-book test 6: one trade each, so VWAP, low and high are the price',
      load('homework-4.json')['items'][0]['widget']['tests'][5]['expect'] == ''.join('%s 1 %.4f %.4f %.4f\n' % (s, p, p, p) for s, p in (('AZN', 118.5), ('BP', 4.75), ('SHEL', 27.15))))

# ---- feedback.byKey.test-N sweep: each coding must reach the key its line implies -------------------------------
SWEEP_FINDING = {'l14s3.count_wraps_to_zero': 2, 'l22s4.no_constexpr': 6, 'l22s4.after_sign_plain': 6, 'l16s3.int_start': 8, 'l16s4.time_le': 7, 'l16s4.ge_then_le': 7, 'l16s4.price_ge': 7, 'l16s5.counts_d0': 11, 'l16s5.counts_d0_no_guard': 11,
                 'l17s5.int_division': 11, 'l18s3.tol_2e-5': 3, 'l18s3.tol_5e-5': 3, 'h4i0.unweighted': 11, 'h4i0.unordered': 9, 'l22s4.after_sign': 6, 'x.h5i1.plain_move_on_growth': 10}
# codings whose first failure is an earlier test than the line being probed, with no claim attached
NEUTRAL = {'l14s3.window_one_late': 'test-1', 'l16s9.peak_first': 'test-2'}
for name, want in sorted(EXPECT.items()):
    if name not in R: continue
    got = key(name)
    if name in NEUTRAL:
        check('sweep ' + name + ' (descriptive line; first failure is ' + NEUTRAL[name] + ')', got == NEUTRAL[name], 'got ' + str(got))
        continue
    ok = (got is not None) if want == 'fail' else (got == want)
    if 'fail' in R[name]: ok = False
    check('sweep ' + name + ': expected ' + str(want), ok, 'got ' + str(got), finding=SWEEP_FINDING.get(name))

# ---- base run ---------------------------------------------------------------------------------------------
for n in BASE:
    if n + '.solution' in R:
        check('base run ' + n + ': the solution passes every hidden test', R[n + '.solution'].get('ok') is True, str(R[n + '.solution'].get('key')) + ' ' + str(R[n + '.solution'].get('fail', ''))[:200])
    if n + '.starter' in R:
        check('base run ' + n + ': the starter fails', R[n + '.starter'].get('ok') is False and 'fail' not in R[n + '.starter'], str(R[n + '.starter'].get('key')))

# ---- report ---------------------------------------------------------------------------------------------------
bad = known = 0
for name, ok, note, finding in CHECKS:
    if ok:
        if finding is not None:
            print('FIXED? (finding %d now holds)' % finding, name)
        continue
    if finding is not None:
        known += 1; print('KNOWN-FINDING %d: %s -- %s' % (finding, name, note))
    else:
        bad += 1; print('FAIL: %s -- %s' % (name, note))
print('%d checks, %d passed, %d failing on audit findings, %d unexpected failures' % (len(CHECKS), len(CHECKS) - bad - known, known, bad))
sys.exit(1 if (bad or known) else 0)
