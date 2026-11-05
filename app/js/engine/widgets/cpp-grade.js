/* C++ mode of the code widget (language: "cpp"; docs/AUTHORING.md section 3, C++ addendum; ENGINE-BACKLOG 304).
   code.js hands a spec with language "cpp" to Z.cppCode(host, spec, ctx), defined here; the widget handle has the
   same shape as the Python one (value, set, answer, ready, dirty, grade, lock, unlock, markGraded, reveal, reset,
   focus, destroy), so the player, sets, exams and the playthrough drive it unchanged.

   Runtime: js/screens/cpp-worker.js. One long-lived compiler worker (YoWASP Clang 21 from the jsDelivr CDN, the npm
   package @yowasp/clang, or vendor/yowasp-clang/ when the CDN cannot be reached) and a cheap runner worker that is
   killed and replaced when a case passes its time limit, so the compiler survives an endless loop.

   One compile per Check. Function mode: the learner's code is followed by a generated harness with one function per
   case and a main that runs the case named by argv[1]; each case runs as its own process (a fresh instance of the
   compiled module), so a crash in one case does not hide the others. The case prints its value after a \x1eZQR
   marker as "<C++ type>\x1f<JSON>", and this file compares it with expect. Script mode (any stdout case, stdin, argv,
   or a raises case without call): the learner's program is compiled as it is and run once per case with that
   case's stdin. Hidden prelude and postlude code sit before and after the learner's code; #line directives keep the
   learner's line numbers (main.cpp), and a case's call is reported as "test N". Compile time is not charged to the
   cases: each case has its own limit (5 s, plus spec.budget).
   Pass 7: a case's tol { rel, abs } (items 425, 442); spec.flags (["-Wall"], "-O2", "-DNDEBUG", "-ffast-math") (items
   402, 452, 476); a case's defines { NAME: value } compiled once per distinct set (item 454); a case { compiles:
   "snippet", expect: false } that must not compile (item 474); stdout cases with lines: true or match: "regex" (item
   451); what a case printed before a timeout (item 369); spec.leakCheck, spec.testkit, spec.signature (items 437, 455,
   438), spec.allocCheck (item 470); spec.files, hidden extra source files compiled and linked with main.cpp (item 403, in part). */
(function () {
  'use strict';
  const Z = window.ZQ;
  /* Where the compiler comes from: the npm package, served by jsDelivr. To self-host, copy the package's gen/ folder
     (bundle.js, llvm*.wasm, llvm-resources.tar) to a static host with CORS and change this URL, or put it in
     app/vendor/yowasp-clang/, which is used when the CDN cannot be reached. */
  const CLANG = 'https://cdn.jsdelivr.net/npm/@yowasp/clang@21.1.4-3/gen/';
  const LOCAL = 'vendor/yowasp-clang/';
  const TEST_MS = 5000, LOAD_MS = 300000, COMPILE_MS = 90000;
  const OUT = '\u001eZQR', EXC = '\u001eZQX', SEP = '\u001f';

  /* ---------- One shared compiler and runner ---------- */
  /* Timings for the record (read by tools): load, and the last compile and run */
  const stats = { loadMs: null, workerMs: null, version: '', patched: false, last: null };
  const Cpp = (() => {
    const url = () => new URL('js/screens/cpp-worker.js', location.href).href;
    const init = (role) => ({ type: 'init', base: CLANG, local: new URL(LOCAL, location.href).href, role });
    let cw = null, rw = null, status = 'idle', reason = '', progress = '', gen = 0, seq = 0, loadTimer = 0;
    const subs = new Set(), pend = new Map(), wanted = new Set(), cache = new Map();
    const notify = () => subs.forEach(f => f(status));
    const set = (s) => { status = s; notify(); };
    /* Precompiled headers come from a second, short-lived compiler (the builder), so a Check never waits behind one;
       it starts once the main compiler is ready and closes when it has nothing left to build */
    let bw = null, bReady = false, bBusy = null, bTimer = 0;
    const bQueue = [], asked = new Set();
    const killB = () => { clearTimeout(bTimer); if (bw) { bw.onmessage = null; bw.onerror = null; bw.terminate(); } bw = null; bReady = false; bBusy = null; };
    const pump = () => {
      if (status !== 'ready' && status !== 'running') return;
      if (!bQueue.length && !bBusy) { killB(); return; }
      if (!bw) {
        try { bw = new Worker(url(), { type: 'module' }); } catch { bQueue.length = 0; return; }
        bw.onmessage = (e) => {
          const m = e.data || {};
          if (m.type === 'ready') { bReady = true; pump(); }
          else if (m.type === 'fail') { killB(); bQueue.length = 0; }
          else if (m.type === 'pch') { clearTimeout(bTimer); if (m.data && cw) cw.postMessage({ type: 'pch-add', head: m.head, data: m.data }, [m.data]); bBusy = null; pump(); }
        };
        bw.onerror = (e) => { if (e && e.preventDefault) e.preventDefault(); killB(); bQueue.length = 0; };
        bw.postMessage(init('builder'));
        return;
      }
      if (!bReady || bBusy) return;
      bBusy = bQueue.shift();
      bTimer = setTimeout(() => { killB(); pump(); }, 180000);
      bw.postMessage({ type: 'pch', head: bBusy });
    };
    const want = (head) => { if (!head || asked.has(head)) return; asked.add(head); bQueue.push(head); pump(); };
    const killC = (why) => {
      clearTimeout(loadTimer);
      if (cw) { cw.onmessage = null; cw.onerror = null; cw.terminate(); cw = null; }
      pend.forEach(p => { clearTimeout(p.timer); p.resolve({ ok: false, diag: why || 'The compiler stopped.', crashed: true }); });
      pend.clear();
      killB(); bQueue.length = 0; asked.clear();
    };
    const unavailable = (msg) => { killC(msg); reason = msg; progress = ''; set('unavailable'); };
    const start = (restart = false) => {
      killC('The compiler was restarted.');
      const my = ++gen, t0 = performance.now();
      progress = '';
      set(restart ? 'restarting' : 'loading');
      if (typeof WebAssembly !== 'object' || typeof Worker !== 'function') { unavailable('This browser cannot run WebAssembly in a background worker.'); return; }
      try { cw = new Worker(url(), { type: 'module' }); } catch (err) { unavailable(String((err && err.message) || err)); return; }
      cw.onmessage = (e) => {
        if (my !== gen) return;
        const m = e.data || {};
        if (m.type === 'progress') { progress = String(m.text || ''); notify(); return; }
        if (m.type === 'ready') { clearTimeout(loadTimer); progress = ''; stats.loadMs = Math.round(performance.now() - t0); stats.workerMs = m.ms; stats.version = m.version; stats.patched = !!m.patched; set('ready'); wanted.forEach(want); return; }
        if (m.type === 'fail') { unavailable(m.message); return; }
        if (m.type === 'compiled') { const p = pend.get(m.id); if (!p) return; pend.delete(m.id); clearTimeout(p.timer); p.resolve(m); }
      };
      cw.onerror = (e) => {
        if (e && e.preventDefault) e.preventDefault();
        if (my !== gen) return;
        const msg = (e && e.message) || 'The C++ compiler worker could not start.';
        if (status === 'ready') start(true); else unavailable(msg);
      };
      cw.postMessage(init());
      loadTimer = setTimeout(() => { if (my === gen) unavailable('The C++ compiler took more than five minutes to load.'); }, LOAD_MS);
    };
    /* The starter's headers are precompiled while the learner reads the question */
    const warm = (head) => { if (!head) return; wanted.add(head); if (status === 'ready') want(head); };
    const compile = (u) => new Promise((resolve) => {
      const ck = (u.flags || []).join(' ') + '\n' + JSON.stringify(u.files || null) + '\n' + u.src;
      const hit = cache.get(ck);
      if (hit) { resolve(hit); return; }
      if (status !== 'ready' || !cw) { resolve({ ok: false, notReady: true }); return; }
      const id = ++seq;
      const timer = setTimeout(() => { pend.delete(id); resolve({ ok: false, diag: 'The compiler took more than ' + COMPILE_MS / 1000 + ' seconds, so it was stopped and restarted. Try again.' }); start(true); }, COMPILE_MS);
      pend.set(id, { resolve: (m) => { if (m.ok || (m.diag && !m.crashed)) { cache.set(ck, m); while (cache.size > 8) cache.delete(cache.keys().next().value); } resolve(m); }, timer });
      const plain = !(u.flags || []).some((f) => !/^-W/.test(f)) && !u.files;
      cw.postMessage({ type: 'compile', id, src: u.src, srcPch: u.srcPch, head: plain ? u.head : '', flags: u.flags || [], files: u.files || null });
      if (plain) want(u.head);
    });
    /* Runs the module once per case; resolves to { results: [..], timeout: index or null, crash } */
    const run = (wasm, cases, limit) => new Promise((resolve) => {
      if (!rw) { try { rw = new Worker(url(), { type: 'module' }); } catch (err) { resolve({ results: [], timeout: null, crash: String((err && err.message) || err) }); return; } }
      const w = rw, id = ++seq, results = new Array(cases.length).fill(null), partial = new Array(cases.length).fill('');
      let timer = 0, crash = null, done = false;
      const guard = () => { clearTimeout(timer); timer = setTimeout(() => fin({ timeout: null, crash: 'The program runner did not respond.' }, true), 20000); };
      const fin = (extra, kill) => {
        if (done) return; done = true;
        clearTimeout(timer); w.onmessage = null; w.onerror = null;
        if (kill) { w.terminate(); if (rw === w) rw = null; }
        resolve({ results, timeout: null, crash: null, ...extra });
      };
      w.onmessage = (e) => {
        const m = e.data || {};
        if (m.id !== id) return;
        if (m.type === 'case' && m.phase === 'start') { clearTimeout(timer); timer = setTimeout(() => fin({ timeout: m.i, partial }, true), limit); }
        else if (m.type === 'case' && m.phase === 'out') partial[m.i] = String(m.out || '');
        else if (m.type === 'case') { results[m.i] = m; guard(); }
        else if (m.type === 'crash') crash = m.message;
        else if (m.type === 'done') fin({ crash });
      };
      w.onerror = (e) => { if (e && e.preventDefault) e.preventDefault(); fin({ crash: (e && e.message) || 'The program runner stopped.' }, true); };
      guard();
      w.postMessage({ type: 'exec', id, wasm, cases });
    });
    return {
      ensure() { if (status === 'idle') start(); },
      warm, compile, run, sub(f) { subs.add(f); return () => subs.delete(f); },
      get status() { return status; }, get reason() { return reason; }, get progress() { return progress; },
    };
  })();

  /* ---------- C++ literals from JSON case values ---------- */
  const cStr = (s) => '"' + Array.from(String(s), (ch) => {
    const c = ch.codePointAt(0);
    if (ch === '\\') return '\\\\';
    if (ch === '"') return '\\"';
    if (ch === '\n') return '\\n';
    if (ch === '\t') return '\\t';
    if (ch === '\r') return '\\r';
    if (c < 0x20 || c === 0x7f) return '\\' + c.toString(8).padStart(3, '0');
    return ch;
  }).join('') + '"';
  const INT_MAX = 2147483647;
  const numLit = (v, asDouble) => {
    if (typeof v !== 'number' || !isFinite(v)) throw new Error('a case value is not a finite number: ' + JSON.stringify(v));
    const s = String(v);
    if (asDouble) return /[.eE]/.test(s) ? s : s + '.0';
    if (Number.isInteger(v)) return Math.abs(v) > INT_MAX ? s + 'LL' : s;
    return s;
  };
  const inner = (t) => { const m = String(t).replace(/\s+/g, ' ').trim().match(/^(?:std::)?vector\s*<\s*(.+)\s*>$/); return m ? m[1].trim() : null; };
  /* lit(value, type): with a type the literal is written out in full (std::vector<double>{1.0, 2.0}); without one a
     list is a braced list, which converts to the parameter's vector type, and a string is a std::string */
  const lit = (v, t, top = true) => {
    const T = t == null ? null : String(t).trim();
    if (T) {
      const e = inner(T);
      if (e != null) {
        if (!Array.isArray(v)) throw new Error(`a value for ${T} is not a list: ${JSON.stringify(v)}`);
        return `${T}{${v.map(x => lit(x, e, false)).join(', ')}}`;
      }
      if (/^(?:std::)?string$/.test(T)) return top ? `std::string(${cStr(v)})` : cStr(v);
      if (T === 'bool') return v ? 'true' : 'false';
      if (T === 'double' || T === 'float') return numLit(v, true);
      if (T === 'long long' || T === 'long') return typeof v === 'number' && Number.isInteger(v) ? String(v) + 'LL' : numLit(v);
      if (T === 'int') return numLit(v);
      if (Array.isArray(v)) return `${T}{${v.map(x => lit(x, null, false)).join(', ')}}`;
      return `${T}(${lit(v, null, false)})`;
    }
    if (typeof v === 'boolean') return v ? 'true' : 'false';
    if (typeof v === 'number') return numLit(v);
    if (typeof v === 'string') return top ? `std::string(${cStr(v)})` : cStr(v);
    if (Array.isArray(v)) return `{${v.map(x => lit(x, null, false)).join(', ')}}`;
    throw new Error('a case value must be a number, a boolean, a string or a list: ' + JSON.stringify(v));
  };
  /* The expression a case runs: call with args (a function name and JSON values) or call alone (C++ source) */
  const callOf = (c) => Array.isArray(c.args) ? `${String(c.call).trim()}(${c.args.map((v, k) => lit(v, Array.isArray(c.types) ? c.types[k] : null)).join(', ')})` : String(c.call ?? '');

  /* ---------- Translation unit ---------- */
  /* The leading block of a source (blank lines, comments, #include <...>) goes into the precompiled header; srcPch
     keeps every other line where it was, so line numbers do not move */
  const splitHead = (src) => {
    const lines = String(src).split('\n'), inc = new Set();
    let block = false;
    for (let i = 0; i < lines.length; i++) {
      const t = lines[i].trim();
      if (block) { const k = t.indexOf('*/'); if (k >= 0) { block = false; if (t.slice(k + 2).trim()) break; } continue; }
      if (!t || t.startsWith('//')) continue;
      if (t.startsWith('/*')) { const k = t.indexOf('*/', 2); if (k < 0) block = true; else if (t.slice(k + 2).trim()) break; continue; }
      if (/^#\s*include\s*<[^>]+>\s*(\/\/.*)?$/.test(t)) { inc.add(i); continue; }
      break;
    }
    return { head: [...inc].map(k => lines[k].trim().replace(/\s*\/\/.*$/, '')), blank: lines.map((l, k) => inc.has(k) ? '' : l).join('\n') };
  };
  const LIB = String.raw`
#line 1 "zq_harness"
#include <cstdio>
#include <cstdlib>
#include <string>
#include <type_traits>
#include <utility>
#include <iterator>
namespace zq {
inline void num(std::string& o, double v) {
  if (v != v) { o += "{\"$num\":\"NaN\"}"; return; }
  if (__builtin_isinf(v)) { o += v > 0 ? "{\"$num\":\"Infinity\"}" : "{\"$num\":\"-Infinity\"}"; return; }
  char b[40]; std::snprintf(b, sizeof b, "%.17g", v); o += b;
}
inline void str(std::string& o, const std::string& s) {
  o += '"';
  for (unsigned char c : s) {
    if (c == '"' || c == '\\') { o += '\\'; o += (char)c; }
    else if (c == '\n') o += "\\n"; else if (c == '\t') o += "\\t"; else if (c == '\r') o += "\\r";
    else if (c < 0x20 || c == 0x7f) { char b[8]; std::snprintf(b, sizeof b, "\\u%04x", c); o += b; }
    else o += (char)c;
  }
  o += '"';
}
template <class T, class = void> struct seq : std::false_type {};
template <class T> struct seq<T, std::void_t<decltype(std::begin(std::declval<const T&>())), decltype(std::end(std::declval<const T&>()))>> : std::true_type {};
template <class T, class = void> struct cplx : std::false_type {};
template <class T> struct cplx<T, std::void_t<decltype(std::declval<const T&>().real()), decltype(std::declval<const T&>().imag())>> : std::true_type {};
template <class T> struct pair : std::false_type {};
template <class A, class B> struct pair<std::pair<A, B>> : std::true_type {};
template <class T> void put(std::string& o, const T& v) {
  using U = std::remove_cv_t<std::remove_reference_t<T>>;
  if constexpr (std::is_same_v<U, bool>) o += v ? "true" : "false";
  else if constexpr (std::is_same_v<U, char>) str(o, std::string(1, v));
  else if constexpr (std::is_integral_v<U>) o += std::to_string(v);
  else if constexpr (std::is_floating_point_v<U>) num(o, (double)v);
  else if constexpr (std::is_enum_v<U>) o += std::to_string((long long)v);
  else if constexpr (std::is_convertible_v<const U&, std::string>) str(o, std::string(v));
  else if constexpr (cplx<U>::value) { o += "{\"re\":"; num(o, (double)v.real()); o += ",\"im\":"; num(o, (double)v.imag()); o += '}'; }
  else if constexpr (pair<U>::value) { o += '['; put(o, v.first); o += ','; put(o, v.second); o += ']'; }
  else if constexpr (seq<U>::value) { o += '['; bool first = true; for (const auto& x : v) { if (!first) o += ','; first = false; put(o, x); } o += ']'; }
  else o += "{\"$unprintable\":true}";
}
template <class T> std::string tname() { std::string s = __PRETTY_FUNCTION__; auto a = s.find("[T = "); if (a == std::string::npos) return "?"; s = s.substr(a + 5); auto b = s.rfind(']'); return b == std::string::npos ? s : s.substr(0, b); }
template <class F> void emit(std::string& o, F&& f) {
  if constexpr (std::is_void_v<decltype(f())>) { f(); o = "void\x1fnull"; }
  else { decltype(auto) v = f(); o = tname<std::remove_cv_t<std::remove_reference_t<decltype(v)>>>(); o += '\x1f'; put(o, v); }
}
inline void finish(const std::string& o) {
#ifdef _LIBCPP_IOSTREAM
  std::cout.flush();
#endif
  std::fflush(stdout);
  std::fputs("\x1eZQR", stdout); std::fputs(o.c_str(), stdout); std::fputs("\n", stdout);
  std::fflush(stdout);
}
}
`;
  const harness = (cases) => LIB + cases.map((c, i) => `
#line 1 "test ${i + 1}"
static void zq_case_${i}(std::string& zq_o) {
${c.setup == null ? '' : String(c.setup)}
zq::emit(zq_o, [&]() -> ${/\)\s*(\[|\.|->)/.test(callOf(c)) ? 'auto' : 'decltype(auto)'} { return
${callOf(c)}
; });
}
`).join('') + `
#line 1 "zq_harness_main"
int main(int argc, char** argv) {
  std::string zq_o;
  switch (argc > 1 ? std::atoi(argv[1]) : -1) {
${cases.map((_, i) => `  case ${i}: zq_case_${i}(zq_o); break;`).join('\n')}
  default: return 3;
  }
  zq::finish(zq_o);
  return 0;
}
`;
  /* In function mode a main the learner wrote (to try things out) is renamed, so it does not clash with the harness */
  const LEAK = String.raw`#include <cstdio>
#include <cstring>
#include <cstdlib>
#include <cstddef>
#include <new>
namespace zq_leak {
inline bool& on() { static bool v = false; return v; }
inline long* counts() { static long c[3] = { 0, 0, 0 }; return c; }
inline unsigned long& quarantined() { static unsigned long q = 0; return q; }
inline void* get(std::size_t n, unsigned kind) { void* raw = std::malloc(n + 16); if (!raw) std::abort(); unsigned* h = static_cast<unsigned*>(raw); h[0] = on() ? 0x5a514c4bu : 0u; h[1] = kind; h[2] = static_cast<unsigned>(n); if (on()) ++counts()[kind]; return static_cast<char*>(raw) + 16; }
inline void put(void* p, unsigned kind) { if (!p) return; char* raw = static_cast<char*>(p) - 16; unsigned* h = reinterpret_cast<unsigned*>(raw); if (h[0] == 0x66726565u) { std::fflush(stdout); std::fprintf(stderr, "Memory error: a block was deleted twice.\n"); std::_Exit(1); } if (h[0] == 0x5a514c4bu) { if (h[1] != kind) ++counts()[2]; --counts()[h[1] ? 1 : 0]; } if (quarantined() > 67108864ul) { std::free(raw); return; } std::memset(p, 0xDD, h[2]); h[0] = 0x66726565u; quarantined() += h[2] + 16; }
inline constexpr bool report = true;
struct Check { Check() { on() = true; } ~Check() { on() = false; long* c = counts(); if (report && (c[0] > 0 || c[1] > 0 || c[2] > 0)) { std::fflush(stdout); if (c[2]) std::fprintf(stderr, "Memory error: %ld block(s) were freed with the wrong form of delete (delete on new[] memory, or delete[] on new).\n", c[2]); if (c[0] > 0 || c[1] > 0) std::fprintf(stderr, "Memory leak: %ld block(s) from new and %ld from new[] were never deleted.\n", c[0] > 0 ? c[0] : 0, c[1] > 0 ? c[1] : 0); std::_Exit(1); } } };
static Check check;
}
void* operator new(std::size_t n) { return zq_leak::get(n, 0); }
void* operator new[](std::size_t n) { return zq_leak::get(n, 1); }
void operator delete(void* p) noexcept { zq_leak::put(p, 0); }
void operator delete[](void* p) noexcept { zq_leak::put(p, 1); }
void operator delete(void* p, std::size_t) noexcept { zq_leak::put(p, 0); }
void operator delete[](void* p, std::size_t) noexcept { zq_leak::put(p, 1); }
`;
  /* ENGINE-BACKLOG 470 (C-alloc-check): spec.allocCheck gives alloc_count() and reset_alloc_count(). One counter, a volatile int that
     every global operator new and new[] (the throwing and the nothrow overloads) bumps, so the optimiser may not drop the count; malloc is
     not counted, and neither are the over-aligned overloads. Clang at -O1 removes a visible new/delete pair (the count would read 0 for `int* t = new int; delete t;`), so an allocCheck unit is compiled with -fno-builtin, which stops that. Alone, the operators here call malloc; with leakCheck the leak wrapper's own
     operators are patched to bump the same counter (two sets of replacement operators would not link). */
  const ALLOC_CNT = String.raw`#include <cstdlib>
#include <cstddef>
#include <new>
namespace zq_alloc { inline volatile int n = 0; inline volatile int f = 0; inline volatile int live = 0; }
inline void reset_alloc_count() { zq_alloc::n = 0; zq_alloc::f = 0; }
inline int alloc_count() { return zq_alloc::n; }
inline int free_count() { return zq_alloc::f; }
inline int live_blocks() { return zq_alloc::live; }
`;
  const LEAK_COUNTED = LEAK.replace('inline void* get(std::size_t n, unsigned kind) {', 'inline void* get(std::size_t n, unsigned kind) { zq_alloc::n = zq_alloc::n + 1; zq_alloc::live = zq_alloc::live + 1;')
    .replace('inline void put(void* p, unsigned kind) { if (!p) return;', 'inline void put(void* p, unsigned kind) { if (!p) return; zq_alloc::f = zq_alloc::f + 1; zq_alloc::live = zq_alloc::live - 1;')
    + 'void* operator new(std::size_t n, const std::nothrow_t&) noexcept { return zq_leak::get(n, 0); }\nvoid* operator new[](std::size_t n, const std::nothrow_t&) noexcept { return zq_leak::get(n, 1); }\n';
  const TESTKIT = String.raw`#include <cmath>
#include <cstdio>
#include <type_traits>
#include <vector>
namespace zq_tk {
template <class T> inline double re_(const T& v) { if constexpr (std::is_arithmetic_v<T>) return (double)v; else return (double)v.real(); }
template <class T> inline double im_(const T& v) { if constexpr (std::is_arithmetic_v<T>) return 0.0; else return (double)v.imag(); }
inline double dist_(double dr, double di) { return di == 0 ? std::fabs(dr) : std::hypot(dr, di); }
struct T { const char* name; void (*fn)(); };
inline std::vector<T>& all() { static std::vector<T> v; return v; }
inline int& fails() { static int f = 0; return f; }
inline const char*& cur() { static const char* c = ""; return c; }
struct Reg { Reg(const char* n, void (*f)()) { all().push_back({ n, f }); } };
}
#define TEST(name) static void name(); static zq_tk::Reg zq_reg_##name(#name, name); static void name()
#define CHECK(cond) do { if (!(cond)) { ++zq_tk::fails(); std::printf("FAILED %s: CHECK(%s), line %d\n", zq_tk::cur(), #cond, __LINE__); } } while (0)
#define CHECK_CLOSE(a, b, tol) do { auto zq_a_ = (a); auto zq_b_ = (b); double zq_ar_ = zq_tk::re_(zq_a_), zq_br_ = zq_tk::re_(zq_b_), zq_ai_ = zq_tk::im_(zq_a_), zq_bi_ = zq_tk::im_(zq_b_); if (!(zq_tk::dist_(zq_ar_ - zq_br_, zq_ai_ - zq_bi_) <= (tol))) { ++zq_tk::fails(); if (zq_ai_ == 0 && zq_bi_ == 0) std::printf("FAILED %s: CHECK_CLOSE(%s, %s) got %.10g and %.10g, line %d\n", zq_tk::cur(), #a, #b, zq_ar_, zq_br_, __LINE__); else std::printf("FAILED %s: CHECK_CLOSE(%s, %s) got (%.10g,%.10g) and (%.10g,%.10g), line %d\n", zq_tk::cur(), #a, #b, zq_ar_, zq_ai_, zq_br_, zq_bi_, __LINE__); } } while (0)
inline int run_tests() { int bad = 0; for (auto& t : zq_tk::all()) { int before = zq_tk::fails(); zq_tk::cur() = t.name; t.fn(); if (zq_tk::fails() > before) ++bad; } std::printf("%d of %d tests passed\n", (int)zq_tk::all().size() - bad, (int)zq_tk::all().size()); return bad; }
inline int test_count() { return (int)zq_tk::all().size(); }
`;
  /* signature: "double total_value(const std::vector<double>&, const std::vector<double>&)" checked by a cast */
  const sigCheck = (sig) => { const m = String(sig || '').trim().match(/^(.+?)\s*\b([A-Za-z_]\w*)\s*\(([\s\S]*)\)\s*$/); return m ? `\n#line 1 "signature check"\n[[maybe_unused]] static auto zq_sig_check = static_cast<${m[1].trim()} (*)(${m[3]})>(&${m[2]});\n` : ''; };
  const FLAG_OK = /^-(W[\w=+-]*|O[0-3sz]|D[A-Za-z_]\w*(=[\w.+-]*)?|U[A-Za-z_]\w*|f(no-)?fast-math|std=c\+\+(14|17|20))$/;
  const flagsOf = (spec) => [].concat(spec.flags || []).map(String).filter((f) => FLAG_OK.test(f));
  const unit = (spec, src, cases, script, extra = {}) => {
    const defs = extra.defines && typeof extra.defines === 'object' ? Object.entries(extra.defines).filter(([k]) => /^[A-Za-z_]\w*$/.test(k)).map(([k, v]) => `#define ${k} ${v === true ? 1 : String(v)}`).join('\n') : '';
    const pre = (spec.allocCheck ? ALLOC_CNT + (spec.leakCheck ? LEAK_COUNTED : LEAK_COUNTED.replace('inline constexpr bool report = true;', 'inline constexpr bool report = false;')) : spec.leakCheck ? LEAK : '') + (spec.testkit ? TESTKIT : '') + (defs ? defs + '\n' : '') + String(spec.prelude || ''); // defines come first, so a hidden prelude can #ifdef on them
    const post = String(spec.postlude || '') + sigCheck(spec.signature) + (extra.probe != null ? `\n#line 1 "compile check"\n[[maybe_unused]] static void zq_compile_probe() {\n${extra.probeSetup || ''}\n${extra.probe}\n}\n` : '');
    const P = splitHead(pre), L = splitHead(src);
    const head = [...new Set([...P.head, ...L.head])].join('\n');
    const build = (p, s) => (p.trim() ? `#line 1 "prelude.cpp"\n${p}\n` : '') + (script ? '' : '#define main zq_learner_main\n') + `#line 1 "main.cpp"\n${s}\n` + (script ? '' : '#undef main\n') + (post.trim() ? `#line 1 "postlude.cpp"\n${post}\n` : '') + (script ? '' : harness(cases));
    const files = spec.files && typeof spec.files === 'object' && Object.keys(spec.files).length ? Object.fromEntries(Object.entries(spec.files).filter(([k]) => /^[\w.-]+\.(cpp|cc|h|hpp)$/.test(k) && k !== 'main.cpp').map(([k, v]) => [k, String(v)])) : null;
    return { src: build(pre, src), srcPch: build(P.blank, L.blank), head: head ? head + '\n' : '', flags: spec.allocCheck ? [...flagsOf(spec), '-fno-builtin'] : flagsOf(spec), files };
  };

  /* ---------- Reading results ---------- */
  const cleanType = (t) => String(t || '').replace(/std::__1::/g, 'std::').replace(/std::basic_string<char(?:, std::char_traits<char>, std::allocator<char>)?>/g, 'std::string');
  const plain = (t) => String(t || '').replace(/std::__1::/g, 'std::').replace(/^std::/, '').trim();
  const revive = (k, v) => (v && typeof v === 'object' && !Array.isArray(v) && '$num' in v ? Number(v.$num) : v);
  const parseErr = (err) => {
    const lines = String(err || '').split('\n');
    const at = lines.findIndex(l => l.startsWith(EXC));
    const exc = at >= 0 ? lines[at].slice(EXC.length).split('|').map(cleanType) : null;
    if (at >= 0) lines.splice(at, 1);
    /* hardening messages name the header's path; the learner needs only the message */
    return { exc, text: lines.join('\n').replace(/^\/usr\/include\/c\+\+\/v1\/[^:\s]+:\d+: /gm, '').replace(/\n+$/, '') };
  };
  const TRAPS = [
    [/unreachable/, 'The program crashed (RuntimeError: unreachable). That is abort(), a failed assert or a libc++ check, or a function that should return a value reaching its end without a return.'],
    [/out of bounds/, 'The program crashed (RuntimeError: memory access out of bounds): it read or wrote memory it does not own, through a bad pointer or index, or the stack overflowed.'],
    [/divide by zero|division by zero/, 'The program crashed: integer division by zero.'],
    [/call stack|Maximum call stack/, 'The program crashed: the call stack ran out (a recursion that never stops?).'],
    [/integer overflow|unrepresentable/, 'The program crashed: an integer division overflowed (INT_MIN / -1).'],
  ];
  const trapLine = (t) => { const hit = TRAPS.find(([re]) => re.test(t)); return hit ? hit[1] : 'The program crashed: ' + t; };
  /* What went wrong in a run, as the learner should read it (or null for a clean exit 0) */
  const runError = (r, e) => {
    if (r.trap) return [e.text, trapLine(r.trap)].filter(Boolean).join('\n');
    if (e.exc || r.code === 134) return e.text || 'The program was stopped by an uncaught exception.';
    if (r.code !== 0) return [e.text, `The program ended with exit status ${r.code}.`].filter(Boolean).join('\n');
    return null;
  };
  const fmt = (v) => {
    if (v === null || v === undefined) return 'nothing (void)';
    if (Array.isArray(v)) return '{' + v.map(fmt).join(', ') + '}';
    if (typeof v === 'string') return JSON.stringify(v);
    if (isCx(v)) return `(${fmt(v.re)},${fmt(v.im)})`;
    if (typeof v === 'number') return Number.isNaN(v) ? 'nan' : v === Infinity ? 'inf' : v === -Infinity ? '-inf' : String(v);
    if (v && typeof v === 'object' && v.$unprintable) return '(a value the tests cannot print)';
    return String(v);
  };
  const isCx = (v) => !!v && typeof v === 'object' && !Array.isArray(v) && 're' in v && 'im' in v;
  const closeCx = (a, e, tol) => { const d = Math.hypot(a.re - e.re, a.im - e.im), m = Math.max(Math.hypot(a.re, a.im), Math.hypot(e.re, e.im)); return a.re === e.re && a.im === e.im || (isFinite(d) && d <= (tol ? Math.max(tol[0] * m, tol[1]) : Math.max(1e-9 * m, 1e-12))); };
  const close = (a, e, tol) => a === e || (isFinite(a) && isFinite(e) && Math.abs(a - e) <= (tol ? Math.max(tol[0] * Math.max(Math.abs(a), Math.abs(e)), tol[1]) : Math.max(1e-9 * Math.max(Math.abs(a), Math.abs(e)), 1e-12)));
  const tolOf = (c) => (c && c.tol && typeof c.tol === 'object' && (Number.isFinite(+c.tol.rel) || Number.isFinite(+c.tol.abs)) ? [Math.max(0, +c.tol.rel || 0), Math.max(0, +c.tol.abs || 0)] : c && typeof c.tol === 'number' && c.tol >= 0 ? [0, c.tol] : null);
  const same = (a, e, mode, tol) => {
    if (Array.isArray(e)) return Array.isArray(a) && a.length === e.length && a.every((x, i) => same(x, e[i], mode, tol));
    if (typeof e === 'number' && isCx(a)) return same(a, { re: e, im: 0 }, mode, tol);
    if (typeof e === 'number') return typeof a === 'number' && (mode === 'isclose' ? close(a, e, tol) : a === e);
    /* item 430: a std::complex result is { re, im }; expect may be a number when the imaginary part is 0 */
    if (isCx(e)) return isCx(a) && (mode === 'isclose' ? closeCx(a, e, tol) : a.re === e.re && a.im === e.im);
    return a === e;
  };
  const norm = (t) => { const ls = String(t).replace(/\r\n/g, '\n').split('\n').map(l => l.replace(/\s+$/, '')); while (ls.length && !ls[0]) ls.shift(); while (ls.length && !ls[ls.length - 1]) ls.pop(); return ls.join('\n'); };
  const excMatch = (names, want) => !!names && names.some(n => plain(n) === plain(want));
  /* compare "raises": expect names an exception type (it or a base class must be thrown and not caught); with no
     expect any abnormal end passes (an uncaught exception, a crash, or a non-zero exit status) */
  const raisesRow = (row, r, e) => {
    const want = row.expect == null ? '' : String(row.expect).trim();
    if (e.exc) { row.ok = want ? excMatch(e.exc, want) : true; row.actual = 'an uncaught ' + e.exc[0]; row.detail = row.ok ? '' : e.text; return; }
    if (r.trap) { row.ok = !want; row.actual = 'a crash'; row.detail = row.ok ? '' : [e.text, trapLine(r.trap)].filter(Boolean).join('\n'); return; }
    if (r.code !== 0) { row.ok = !want; row.actual = `exit status ${r.code}`; row.detail = row.ok ? '' : e.text; return; }
    row.ok = false;
    row.actual = row.hasValue ? 'no error, the value was ' + fmt(row.value) : 'no error: the program ran to the end';
  };
  const isOut = (c) => c.compiles == null && (c.compare === 'stdout' || (c.call == null && c.expect != null && c.compare == null));
  const scriptMode = (cases) => cases.some(c => c.compiles == null && (isOut(c) || c.stdin != null || c.argv != null || (c.compare === 'raises' && c.call == null)));
  /* Compiler output for the learner: the generated harness's notes are dropped, test N keeps no line number, the
     linker's temporary file names and libc++'s inline namespace go */
  const cleanDiag = (d) => {
    const L = String(d || '').replace(/\r/g, '').split('\n'), out = [];
    for (let i = 0; i < L.length; i++) {
      const ln = L[i];
      if (/^zq_harness(_main)?:\d+:\d+: note:/.test(ln) || /^In file included from zq_harness/.test(ln)) { while (L[i + 1] != null && /^\s|^\s*\d+ \|/.test(L[i + 1])) i++; continue; }
      if (/^clang\S*: error: linker command failed/.test(ln)) continue;
      out.push(ln.replace(/^(test \d+):\d+:\d+: /, '$1: ').replace(/^wasm-ld: error: \S+?\.o: /, 'linker error: ').replace(/std::__1::/g, 'std::'));
    }
    let txt = out.join('\n').replace(/\n+$/, '');
    if (/linker error: undefined symbol/.test(txt)) txt += '\n\nThe linker could not find a function the code calls: it is declared but not defined, or its definition has different parameter types.';
    return txt.length > 6000 ? txt.slice(0, 6000) + '\n[compiler output cut at 6,000 characters]' : txt;
  };
  /* Warnings about the learner's own code (main.cpp), shown above the results when the compile succeeded */
  const learnerWarnings = (d) => {
    const L = String(d || '').split('\n'), out = [];
    let keep = false;
    L.forEach(ln => {
      if (/^\S[^:]*:\d+:\d+: (warning|error|note):/.test(ln)) keep = /^main\.cpp:\d+:\d+: (warning|note):/.test(ln);
      else if (/^\d+ warnings? generated\.$|^In file included from/.test(ln)) keep = false;
      if (keep) out.push(ln);
    });
    return out.join('\n').trim();
  };

  /* ---------- C++ highlighting and editor (the Python editor's behaviour; indent after an open brace) ---------- */
  const KW = new Set('alignas alignof auto bool break case catch char class const constexpr const_cast continue decltype default delete do double dynamic_cast else enum explicit extern false final float for friend goto if inline int long mutable namespace new noexcept nullptr operator override private protected public reinterpret_cast return short signed sizeof static static_assert static_cast struct switch template this throw true try typedef typename union unsigned using virtual void volatile while'.split(' '));
  const BI = new Set('std cout cin cerr endl string vector map set unordered_map unordered_set pair size_t array deque queue stack list optional tuple unique_ptr shared_ptr make_unique make_shared move swap sort accumulate min max abs sqrt pow exp log printf scanf puts getline to_string stoi stod size begin end push_back emplace_back runtime_error invalid_argument out_of_range exception'.split(' '));
  const TOK = /(\/\/[^\n]*|\/\*[\s\S]*?(?:\*\/|$))|(^[ \t]*#[ \t]*\w+)|("(?:[^"\\\n]|\\.)*"?|'(?:[^'\\\n]|\\.)*'?|<[\w./]+>(?=[ \t]*(?:\/\/[^\n]*)?$))|(\b\d[\d']*(?:\.\d*)?(?:[eE][+-]?\d+)?[uUlLfF]*|\.\d+(?:[eE][+-]?\d+)?[fF]?)|([A-Za-z_]\w*)/gm;
  const escH = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  const highlight = (src) => {
    let out = '', last = 0, pre = false;
    src.replace(TOK, (m, com, dir, str, nm, id, at) => {
      out += escH(src.slice(last, at)); last = at + m.length;
      let cls = '';
      if (com) cls = 'com';
      else if (dir) cls = 'kw';
      else if (str) cls = str[0] !== '<' || pre ? 'str' : ''; // <vector> is a header name only after #include
      else if (nm) cls = 'num';
      else if (id) cls = KW.has(id) ? 'kw' : BI.has(id) ? 'bi' : '';
      pre = !!dir && /include/.test(dir);
      out += cls ? `<span class="tok-${cls}">${escH(m)}</span>` : escH(m);
      return m;
    });
    return out + escH(src.slice(last));
  };
  function Editor(host, { value, label, onInput, onRun }) {
    host.innerHTML = `<div class="wd-gut" aria-hidden="true"><div class="wd-gut-in"></div></div>
      <div class="wd-ed-main"><pre class="wd-hl" aria-hidden="true"><code></code></pre>
        <textarea class="wd-ta" wrap="off" spellcheck="false" autocapitalize="off" autocomplete="off" autocorrect="off" aria-label="${Z.esc(label)}"></textarea></div>`;
    const ta = host.querySelector('textarea'), code = host.querySelector('code'), gut = host.querySelector('.wd-gut-in');
    let lines = 0, cur = -1, escArmed = false;
    const lineStartOf = (v, i) => v.lastIndexOf('\n', i - 1) + 1;
    const scroll = () => { code.style.transform = `translate(${-ta.scrollLeft}px, ${-ta.scrollTop}px)`; gut.style.transform = `translateY(${-ta.scrollTop}px)`; host.classList.toggle('has-more', ta.scrollLeft + ta.clientWidth < ta.scrollWidth - 2); }; /* item 508: a fade on the right edge says a long line scrolls sideways */
    const mark = () => {
      const line = ta.value.slice(0, ta.selectionStart).split('\n').length - 1;
      if (line === cur) return;
      if (gut.children[cur]) gut.children[cur].classList.remove('cur');
      cur = line;
      if (gut.children[cur]) gut.children[cur].classList.add('cur');
    };
    const paint = () => {
      const v = ta.value;
      code.innerHTML = highlight(v) + '\n';
      const n = v.split('\n').length;
      if (n !== lines) { lines = n; gut.innerHTML = Array.from({ length: n }, (_, i) => `<span>${i + 1}</span>`).join(''); cur = -1; }
      host.style.setProperty('--wd-lines', Math.max(6, Math.min(18, n + 1)));
      mark(); scroll();
    };
    const edit = (start, end, text, selStart, selEnd = selStart) => {
      ta.focus(); ta.setSelectionRange(start, end);
      let ok = false;
      if (start !== end || text) {
        try { ok = text ? document.execCommand('insertText', false, text) : document.execCommand('delete'); } catch { ok = false; }
        if (!ok) { ta.setRangeText(text, start, end, 'end'); paint(); onInput(ta.value); }
      }
      ta.setSelectionRange(selStart, selEnd); mark();
    };
    const indent = (out) => {
      const v = ta.value, s = ta.selectionStart, e = ta.selectionEnd;
      const multi = v.slice(s, e).includes('\n');
      if (!multi && !out) { edit(s, e, '    ', s + 4); return; }
      const a = lineStartOf(v, s);
      const endAt = e > s && v[e - 1] === '\n' ? e - 1 : e;
      let b = v.indexOf('\n', endAt); if (b < 0) b = v.length;
      const old = v.slice(a, b);
      let first = 0, total = 0;
      const next = old.split('\n').map((ln, k) => {
        if (!out) { if (k === 0) first = 4; total += 4; return '    ' + ln; }
        const n = ln.match(/^ {0,4}/)[0].length; if (k === 0) first = -n; total -= n; return ln.slice(n);
      }).join('\n');
      if (next === old) return;
      edit(a, b, next, Math.max(a, s + first), multi ? e + total : Math.max(a, e + first));
    };
    const newline = () => {
      const v = ta.value, s = ta.selectionStart, e = ta.selectionEnd;
      const line = v.slice(lineStartOf(v, s), s);
      let ind = line.match(/^ */)[0];
      const bare = line.replace(/\/\/.*$/, '').trimEnd();
      if (/[{(]$/.test(bare)) ind += '    ';
      edit(s, e, '\n' + ind, s + 1 + ind.length);
    };
    ta.addEventListener('keydown', (ev) => {
      if ((ev.ctrlKey || ev.metaKey) && ev.key === 'Enter') { ev.preventDefault(); ev.stopPropagation(); onRun(); return; }
      if (ev.key === 'Escape') { escArmed = true; return; }
      if (ev.key === 'Tab' && !ev.ctrlKey && !ev.altKey && !ev.metaKey) {
        if (escArmed) { escArmed = false; return; }
        ev.preventDefault(); indent(ev.shiftKey); return;
      }
      if (ev.key !== 'Shift') escArmed = false;
      if (ev.key === 'Enter' && !ev.isComposing && !ev.shiftKey && !ev.altKey) { ev.preventDefault(); ev.stopPropagation(); newline(); return; }
      if (ev.key === '}' && ta.selectionStart === ta.selectionEnd) { // a closing brace on an empty line moves back one level
        const v = ta.value, s = ta.selectionStart, before = v.slice(lineStartOf(v, s), s);
        if (before.length >= 4 && /^ +$/.test(before)) { ev.preventDefault(); edit(s - 4, s, '}', s - 3); return; }
      }
      if (ev.key === 'Backspace' && ta.selectionStart === ta.selectionEnd) {
        const v = ta.value, s = ta.selectionStart, before = v.slice(lineStartOf(v, s), s);
        if (before.length && /^ +$/.test(before)) { const n = before.length % 4 || 4; ev.preventDefault(); edit(s - n, s, '', s - n); }
      }
    });
    ta.addEventListener('input', () => { paint(); onInput(ta.value); });
    ta.addEventListener('scroll', scroll, { passive: true });
    if (window.ResizeObserver) new ResizeObserver(scroll).observe(ta);
    ['keyup', 'click', 'focus', 'select'].forEach(t => ta.addEventListener(t, mark));
    ta.value = value; paint();
    return { ta, get value() { return ta.value; }, set(v) { ta.value = v; paint(); onInput(v); }, readOnly(v) { ta.readOnly = v; } };
  }

  /* ---------- The widget ---------- */
  Z.cppCode = (host, spec, ctx) => {
    const examples = spec.examples || [], tests = spec.tests || [];
    const script = scriptMode([...examples, ...tests]);
    const el = Z.h(`<div class="wd-code wd-cpp">
      <div class="wd-code-head">
        <span class="t-label">C++</span>
        <span class="wd-py t-caption" aria-live="polite"></span>
        <button type="button" class="btn secondary wd-run" disabled>${Z.icon('play', 'sm')} Run examples</button>
      </div>
      <div class="wd-ed"></div>
      <p class="t-caption wd-code-keys"><kbd>Tab</kbd> indents. <kbd>Esc</kbd> then <kbd>Tab</kbd> leaves the editor. <kbd>Ctrl</kbd> <kbd>Enter</kbd> runs the examples. Check compiles your code and runs the hidden tests.</p>
      ${spec.how ? `<p class="t-caption wd-code-how">${Z.grade.inline(spec.how)}</p>` : ''}
      <div class="wd-res" aria-live="polite"></div>
    </div>`);
    host.append(el);
    const runBtn = el.querySelector('.wd-run'), stEl = el.querySelector('.wd-py'), res = el.querySelector('.wd-res'), edHost = el.querySelector('.wd-ed');
    let alive = true, busy = false, cache = null, locked = false, saveT = 0, quiet = false;
    const D = Z.state && Z.state.drills && typeof Z.state.drills.draft === 'function' && ctx.draftKey ? Z.state.drills : null;
    const draft = (v) => { try { return D ? D.draft(ctx.draftKey, v) : null; } catch (e) { console.error(e); return null; } };
    const saved = D ? draft() : null;
    const ed = Editor(edHost, { value: typeof saved === 'string' && saved.trim() ? saved : spec.starter || '', label: 'C++ code editor', onInput: () => {
      if (D && !quiet) { clearTimeout(saveT); saveT = setTimeout(() => draft(ed.value === (spec.starter || '') ? null : ed.value), 400); }
      ctx.change && ctx.change({ code: ed.value });
    }, onRun: () => runExamples() });
    const sync = (s = Cpp.status) => {
      if (!alive) return;
      const txt = { idle: 'C++ not loaded', loading: Cpp.progress || 'Loading the C++ compiler', restarting: 'Restarting the C++ compiler', ready: 'C++ ready', unavailable: 'C++ is not available here' }[s] || '';
      stEl.textContent = busy && s === 'ready' ? busy : txt; stEl.dataset.s = s;
      stEl.title = s === 'unavailable' ? Cpp.reason : '';
      runBtn.disabled = !!busy || locked || s !== 'ready';
      ctx.change && ctx.change({ code: ed.value, status: s });
    };
    const unsub = Cpp.sub(sync);
    Cpp.ensure();
    Cpp.warm(unit(spec, spec.starter || '', [], script).head);
    sync();

    const pre = (t, cls = 'wd-res-out') => `<pre class="${cls} t-code">${Z.esc(t)}</pre>`;
    const label = (r) => r.compiles != null ? `does <code class="lsn-ic">${Z.esc(r.compiles)}</code> compile?` : r.out ? (r.stdin ? 'what it prints with this input' : 'what it prints') : r.call ? `${r.setup ? `<code class="lsn-ic">${Z.esc(r.setup)}</code> then ` : ''}<code class="lsn-ic">${Z.esc(r.call)}</code>` : 'the whole program';
    const outRow = (r) => {
      const said = r.stdout.trim() ? pre(r.stdout) : '<div class="t-caption">Your program printed nothing.</div>';
      const input = (r.argv && r.argv.length ? `<div class="t-caption">Run as</div>${pre('./main ' + r.argv.map(a => (/\s/.test(a) ? JSON.stringify(a) : a)).join(' '), 'wd-res-out wd-res-in')}` : '') + (r.stdin ? `<div class="t-caption">Input</div>${pre(r.stdin.replace(/\n$/, ''), 'wd-res-out wd-res-in')}` : '');
      if (r.error) return `${input}${pre(r.error, 'wd-res-err')}${r.stdout.trim() ? `<div class="t-caption">Printed before the error</div>${said}` : ''}`;
      if (r.ok) return `${input}<div class="t-caption">Printed the expected output</div>${said}`;
      return `${input}<div class="t-caption">Expected output</div>${pre(String(r.expect ?? '').replace(/\n$/, ''))}<div class="t-caption">Your program printed</div>${said}${r.stderr ? `<details class="wd-res-more"><summary class="t-caption">It also wrote to stderr</summary>${pre(r.stderr, 'wd-res-err')}</details>` : ''}`;
    };
    const valRow = (r) => {
      if (r.error) return pre(r.error, 'wd-res-err') + (r.stdout ? `<div class="t-caption">Printed before the error</div>${pre(r.stdout)}` : '');
      const exp = r.compiles != null ? (r.expect === false || r.expect === 'false' ? 'Expected it not to compile' : 'Expected it to compile') : r.raises ? (r.expect ? `Expected it to throw <code class="lsn-ic">${Z.esc(r.expect)}</code>` : 'Expected it to stop with an error') : `Expected <code class="lsn-ic">${Z.esc(fmt(r.expect))}</code>${r.tol ? ` (within ${[r.tol[0] ? 'relative ' + r.tol[0] : '', r.tol[1] ? 'absolute ' + r.tol[1] : ''].filter(Boolean).join(' or ')})` : ''}`;
      const got = r.actual == null ? 'nothing' : r.actual;
      const ty = !r.raises && !r.ok && r.type && r.type !== 'void' ? ` <span class="muted">(${Z.esc(r.type)})</span>` : '';
      return `<div class="t-caption">${exp}, got <code class="lsn-ic">${Z.esc(got)}</code>${ty}</div>${r.detail ? pre(r.detail, 'wd-res-err') : ''}${r.stdout ? pre(r.stdout) : ''}`;
    };
    const row = (r, name) => `<li class="wd-res-row ${r.ok ? 'ok' : 'bad'}">
        <span class="wd-res-ic" aria-hidden="true">${Z.icon(r.ok ? 'check' : 'cross', 'xs')}</span>
        <div class="wd-res-b"><div class="wd-res-h"><b>${name}</b> ${label(r)}</div>${r.out ? outRow(r) : valRow(r)}</div></li>`;
    const render = (title, rows, cases, extra = '', list = true) => {
      const n = rows.filter(r => r.ok).length;
      res.innerHTML = `<div class="wd-res-top"><span class="t-label">${title}</span><span class="t-caption">${list ? `${n} of ${cases.length} passed` : 'no test ran'}</span></div>${extra}${list ? `<ol class="wd-res-list">${rows.map((r, i) => row(r, (title === 'Examples' ? 'Example ' : 'Test ') + (i + 1))).join('')}</ol>` : ''}`;
    };
    const progressNote = (t) => { if (alive) res.innerHTML = `<p class="t-caption wd-res-load" aria-live="polite">${Z.esc(t)}</p>`; };

    /* Compile once per distinct set of defines, run every case; compile-check cases compile a snippet of their own.
       Resolves to { rows, error, compileError, warnings, ms } */
    const firstErr = (d) => { const L = cleanDiag(d).split('\n'); const k = L.findIndex((l) => /error:/.test(l)); return k < 0 ? L.slice(0, 3).join('\n') : L.slice(k, k + 3).join('\n'); };
    const runCases = async (cases) => {
      const rows = cases.map(c => {
        let call = '';
        try { call = c.call == null ? '' : callOf(c); } catch (e) { call = String(c.call); }
        return { argv: Array.isArray(c.argv) ? c.argv.map(String) : null, call, raises: c.compare === 'raises', setup: c.setup == null ? '' : String(c.setup), expect: c.expect, out: isOut(c), stdin: c.stdin == null ? '' : String(c.stdin), ok: false, actual: null, type: '', error: null, stdout: '', detail: '', tol: tolOf(c), compiles: c.compiles != null ? String(c.compiles) : null };
      });
      if (Cpp.status !== 'ready') return { rows, error: Cpp.status === 'unavailable' ? 'The C++ compiler could not load: ' + Cpp.reason : 'The C++ compiler is still loading. Try again in a moment.' };
      const runIdx = cases.map((c, i) => (c.compiles == null ? i : -1)).filter((i) => i >= 0), probeIdx = cases.map((c, i) => (c.compiles != null ? i : -1)).filter((i) => i >= 0);
      const keyOf = (c) => JSON.stringify(c && c.defines && typeof c.defines === 'object' ? c.defines : {});
      const groups = new Map(); runIdx.forEach((i) => { const k = keyOf(cases[i]); if (!groups.has(k)) groups.set(k, []); groups.get(k).push(i); });
      if (!groups.size) groups.set('{}', []);
      let warnings = '', compileMs = 0, msC = 0, error = null, runMs = 0, pchUsed = false;
      const limit = TEST_MS + (spec.budget != null ? Math.max(0, +spec.budget || 0) : 0);
      for (const [k, idxs] of groups) {
        const sub = idxs.map((i) => cases[i]);
        let u;
        try { u = unit(spec, ed.value, sub, script, { defines: JSON.parse(k) }); } catch (e) { return { rows, error: 'This exercise has a case the tests cannot write in C++: ' + e.message }; }
        busy = 'Compiling'; sync(); progressNote('Compiling...');
        const t0 = performance.now();
        const c = await Cpp.compile(u);
        compileMs += Math.round(performance.now() - t0); msC += c.ms || 0; pchUsed = pchUsed || !!c.pch;
        if (!c.ok) {
          busy = false; sync();
          if (c.notReady) return { rows, error: 'The C++ compiler is still loading. Try again in a moment.' };
          /* item 438: a signature that does not match gets a plain sentence before clang's message */
          const sigFail = spec.signature && /signature check:/.test(c.diag || '') && !/main\.cpp:\d+:\d+: error/.test(c.diag || '');
          return { rows, error: (sigFail ? `Your function does not have the signature this exercise asks for: ${spec.signature}\n\n` : '') + cleanDiag(c.diag), compileError: true, compileMs };
        }
        if (!warnings) warnings = learnerWarnings(c.diag);
        if (!sub.length) continue;
        busy = 'Running'; sync(); progressNote('Running...');
        const runs = await Cpp.run(c.wasm, sub.map((cs, j) => (script ? { argv: cs.argv || [], stdin: cs.stdin == null ? '' : String(cs.stdin) } : { argv: [String(j)], stdin: '' })), limit);
        busy = false; sync();
        runMs += runs.results.reduce((a, r) => a + (r ? r.ms : 0), 0);
        runs.results.forEach((r, j) => {
          const i = idxs[j], row = rows[i];
          if (!r) return;
          const e = parseErr(r.err);
          const kk = script ? -1 : r.out.lastIndexOf(OUT);
          row.stdout = kk >= 0 ? r.out.slice(0, kk) : r.out;
          if (!row.out) row.stdout = row.stdout.replace(/\n+$/, '');
          if (kk >= 0) {
            const line = r.out.slice(kk + OUT.length).replace(/\n$/, ''), q = line.indexOf(SEP);
            row.type = cleanType(line.slice(0, q));
            try { row.value = JSON.parse(line.slice(q + 1), revive); row.hasValue = true; } catch { row.value = undefined; }
          }
          if (row.raises) { raisesRow(row, r, e); return; }
          const err = runError(r, e);
          if (row.out) {
            if (err) { row.error = err; return; }
            const cs = cases[i];
            /* item 451: match: "regex" or lines: true (every expected line, in order, among the printed ones) */
            if (cs.match != null) { let re = null; try { re = new RegExp(String(cs.match), 'm'); } catch { re = null; } row.ok = !!re && re.test(row.stdout); return; }
            if (cs.lines) { const want = norm(row.expect).split('\n'), have = norm(row.stdout).split('\n'); let q = 0; have.forEach((l) => { if (q < want.length && l === want[q]) q++; }); row.ok = q === want.length; return; }
            row.ok = cs.exact ? row.stdout === String(row.expect) : norm(row.stdout) === norm(row.expect);
            if (!row.ok && e.text) row.stderr = e.text; // inbox (cpp 4): what the program wrote to stderr, folded under a failing row
            return;
          }
          if (err || !row.hasValue) { row.error = err || 'The test did not report a value.'; return; }
          row.actual = row.type === 'void' ? 'nothing (void)' : fmt(row.value);
          row.ok = same(row.value, cases[i].expect, cases[i].compare === 'isclose' ? 'isclose' : 'equal', row.tol);
        });
        if (runs.timeout != null) {
          const r = rows[idxs[runs.timeout]];
          if (r) { r.error = `Stopped after ${limit / 1000} s. Look for a loop that never ends${script ? ', or a read from std::cin waiting for input the test does not give' : ''}.`; if (runs.partial && runs.partial[runs.timeout]) r.stdout = String(runs.partial[runs.timeout]).replace(new RegExp(OUT + '[\\s\\S]*$'), ''); } // item 369
          idxs.forEach((i, j) => { if (j > runs.timeout && !runs.results[j]) rows[i].error = 'Not run: an earlier test went past the time limit.'; });
        } else if (runs.crash) error = 'The program runner stopped: ' + runs.crash;
      }
      /* item 474: compile checks: { compiles: "Connection b = a;", setup, expect: false } after the learner's code */
      for (const i of probeIdx) {
        const cs = cases[i], row = rows[i];
        busy = 'Compiling'; sync(); progressNote('Checking what compiles...');
        let u; try { u = unit(spec, ed.value, [], false, { defines: cs.defines, probe: String(cs.compiles), probeSetup: cs.setup == null ? '' : String(cs.setup) }); } catch (e) { row.error = e.message; continue; }
        const c = await Cpp.compile(u);
        busy = false; sync();
        if (c.notReady) { error = 'The C++ compiler is still loading. Try again in a moment.'; break; }
        const want = cs.expect !== false && cs.expect !== 'false';
        row.ok = !!c.ok === want;
        row.actual = c.ok ? 'it compiled' : 'it did not compile';
        row.detail = c.ok ? '' : firstErr(c.diag);
      }
      stats.last = { compileWallMs: compileMs, compileMs: msC, pch: pchUsed, runMs: Math.round(runMs * 10) / 10, cases: cases.length };
      return { rows, error, warnings, compileMs, ms: msC };
    };
    const extraOf = (r, untouched) => {
      if (r.compileError) return untouched ? `<p class="t-caption">The starter is not finished yet, so it does not compile. Fill in what it asks for and check again.</p><details class="wd-res-more"><summary class="t-caption">Show the compiler's message</summary>${pre(r.error, 'wd-res-err')}</details>`
        : `<div class="t-caption">Your code did not compile, so no test ran</div>${pre(r.error, 'wd-res-err')}`;
      return (r.error ? pre(r.error, 'wd-res-err') : '') + (r.warnings ? `<div class="t-caption">The compiler warned</div>${pre(r.warnings, 'wd-res-err')}` : '');
    };
    const runExamples = async () => {
      if (busy || locked || Cpp.status !== 'ready' || !examples.length) return;
      const r = await runCases(examples);
      if (!alive) return;
      render('Examples', r.rows, examples, extraOf(r, false), !r.compileError);
      sync();
    };
    runBtn.addEventListener('click', runExamples);
    if (!examples.length) runBtn.hidden = true;

    return {
      el,
      value: () => ed.value,
      set(v) { quiet = true; ed.set(String(v ?? '')); quiet = false; cache = null; },
      answer: () => spec.solution ?? null,
      ready: () => !busy && ed.value.trim() !== '' && (Cpp.status === 'ready' || Cpp.status === 'unavailable'),
      dirty: () => ed.value !== (spec.starter || ''),
      async grade() {
        const src = ed.value;
        if (cache && cache.src === src) return cache.result;
        if (Cpp.status === 'unavailable') return { ok: false, key: 'unavailable', line: 'The C++ compiler could not load in this browser, so the tests cannot run.', detail: null };
        const r = await runCases(tests);
        const n = r.rows.filter(x => x.ok).length;
        const first = r.rows.findIndex(x => !x.ok);
        const ok = !r.error && n === tests.length && tests.length > 0;
        const untouched = !!r.compileError && src.trim() === String(spec.starter || '').trim();
        const line = ok ? null : untouched ? 'The starter does not compile yet on its own: fill in the parts it asks for, then check again.' : r.compileError ? 'Your code did not compile. The compiler\'s message is shown below the editor.' : r.error ? 'The tests could not finish. The reason is shown below the editor.' : `${n} of ${tests.length} tests passed. The first failure is test ${first + 1}.`;
        const result = { ok, key: ok ? null : r.compileError ? 'compile' : r.error ? 'error' : `test-${first + 1}`, line, detail: { passed: n, total: tests.length, rows: r.rows, compileMs: r.compileMs } };
        if (alive) render('Tests', r.rows, tests, extraOf(r, untouched), !r.compileError);
        if (!r.error || r.compileError) cache = { src, result }; // a runner or loading failure is worth retrying
        return result;
      },
      lock() { locked = true; ed.readOnly(true); sync(); },
      unlock() { locked = false; ed.readOnly(false); el.classList.remove('is-ok', 'is-bad'); sync(); },
      markGraded(r) { el.classList.toggle('is-ok', !!r.ok); el.classList.toggle('is-bad', !r.ok); },
      reveal() { quiet = true; if (spec.solution) ed.set(spec.solution); quiet = false; locked = true; ed.readOnly(true); el.classList.add('wd-rev'); sync(); },
      reset() { clearTimeout(saveT); if (D) draft(null); quiet = true; ed.set(spec.starter || ''); quiet = false; res.innerHTML = ''; cache = null; locked = false; ed.readOnly(false); el.classList.remove('is-ok', 'is-bad', 'wd-rev'); sync(); },
      focus() { ed.ta.focus({ preventScroll: true }); },
      destroy() { alive = false; unsub(); if (D && saveT) { clearTimeout(saveT); draft(ed.value === (spec.starter || '') ? null : ed.value); } },
    };
  };
  /* For tools and tests: the pure helpers */
  Z.cppCode.lib = { lit, callOf, splitHead, unit, cleanDiag, same, norm, fmt, scriptMode };
  Z.cppCode.stats = stats;
})();
