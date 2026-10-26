/* C++ runner for the code widget's language "cpp" (docs/AUTHORING.md section 3, C++ addendum; ENGINE-BACKLOG 304).
   A module Web Worker with two roles, so a program that never ends can be stopped without losing the compiler:

   Compiler (the first message is init). Loads YoWASP Clang (clang and lld 21 compiled to WebAssembly, with the
   wasi-libc and libc++ sysroot) from `base` (the jsDelivr copy of the npm package @yowasp/clang, or any folder that
   serves its gen/ files), compiles the small exception runtime below once, and then compiles one translation unit per
   message to a WASI command module. A unit whose leading #include lines have a precompiled header (pch-add) compiles
   in about a second instead of three.
     in:  { type: 'init', base, local, role }             base: the CDN folder; local: a vendor/ copy, used only when
                                                          the CDN cannot be reached and it exists (both end in '/');
                                                          role 'builder' skips the runtime (see below)
          { type: 'compile', id, src, srcPch, head }      src: the whole unit; srcPch: the same with the head's
                                                          include lines blanked (used when head has a precompiled header)
          { type: 'pch-add', head, data }                 a precompiled header for head (from a builder)
     out: { type: 'progress', text } | { type: 'ready', version, ms, patched } | { type: 'fail', message }
          { type: 'compiled', id, ok, wasm, diag, ms, pch }   wasm is an ArrayBuffer when ok

   Builder (init with role 'builder'). A second, short-lived compiler that builds precompiled headers (10 to 30 s each
   in Chrome) while the main compiler stays free for Checks; the page closes it when it has nothing left to build.
     in:  { type: 'pch', head }   out: { type: 'pch', head, data }   data: an ArrayBuffer, or null when head does not compile

   Runner (any worker that receives exec; it never loads the compiler). Runs a compiled module once per case with a
   small WASI preview 1 shim (args, stdin, stdout, stderr, clocks, random; files are not available).
     in:  { type: 'exec', id, wasm, cases: [{ argv: [..], stdin }] }
     out: { type: 'case', id, i, phase: 'start' }
          { type: 'case', id, i, phase: 'end', out, err, code, trap, ms }   code: exit status; trap: a crash message
          { type: 'done', id } | { type: 'crash', id, message } */
'use strict';

/* The libc++ debug hardening mode turns an out-of-range vector[] or a bad iterator into a readable message
   ("libc++ Hardening assertion __n < size() failed: vector[] index out of bounds") instead of a silent wrong read */
let FLAGS = ['-std=c++17', '-O1', '-D_LIBCPP_HARDENING_MODE=_LIBCPP_HARDENING_MODE_DEBUG', '-fno-color-diagnostics', '-fmessage-length=0', '-ferror-limit=10'];
/* --stack-first: a stack overflow traps (memory access out of bounds) instead of overwriting the program's data */
const LINK = ['-Wl,--stack-first,-z,stack-size=8388608'];

/* The sysroot's libc++abi is built without exception support, so a throw would not link. The compiler lowers
   try/catch away (catch blocks never run), and these two functions end the program the way an uncaught exception
   does on a desktop: a "terminate called after throwing an instance of" message on stderr and exit status 134. The
   first stderr line, after a \x1eZQX marker, lists the thrown type and its base classes for compare "raises". */
const RUNTIME = String.raw`
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <exception>
#include <stdexcept>
#include <string>
#include <typeinfo>
extern "C" char* __cxa_demangle(const char*, char*, size_t*, int*);
namespace {
struct ZA { virtual ~ZA() {} };
struct ZB { virtual ~ZB() {} };
struct ZC : ZA, ZB {};
struct ZD : std::exception {};
void* vptr(const std::type_info* t) { return *(void* const*)t; }
std::string nice(const std::type_info* t) {
  int st = 0;
  char* n = __cxa_demangle(t->name(), nullptr, nullptr, &st);
  std::string s = st == 0 && n ? n : t->name();
  std::free(n);
  return s;
}
/* Walks the Itanium type_info of a class: __si_class_type_info has one base after the name, __vmi_class_type_info a
   flags word, a count and (base, offset_flags) pairs. Collects every class name and finds std::exception's offset. */
void walk(const std::type_info* t, std::string& names, long here, long* exc, int depth) {
  if (depth > 40) return;
  if (!names.empty()) names += '|';
  names += nice(t);
  if (*t == typeid(std::exception) && *exc < 0) *exc = here;
  static void* vsi = vptr(&typeid(ZD));
  static void* vmi = vptr(&typeid(ZC));
  if (vptr(t) == vsi) {
    walk(*(const std::type_info* const*)((const char*)t + 2 * sizeof(void*)), names, here, exc, depth + 1);
  } else if (vptr(t) == vmi) {
    const char* p = (const char*)t + 2 * sizeof(void*);
    unsigned count = *(const unsigned*)(p + sizeof(unsigned));
    const char* arr = p + 2 * sizeof(unsigned);
    for (unsigned i = 0; i < count && i < 64; i++) {
      const char* e = arr + i * (sizeof(void*) + sizeof(long));
      long of = *(const long*)(e + sizeof(void*));
      walk(*(const std::type_info* const*)e, names, (of & 1) ? -1000000 : here + (of >> 8), exc, depth + 1);
    }
  }
}
}
extern "C" void* __cxa_allocate_exception(size_t n) throw() {
  void* p = std::malloc(n ? n : 1);
  if (!p) std::abort();
  std::memset(p, 0, n);
  return p;
}
extern "C" void __cxa_free_exception(void* p) throw() { std::free(p); }
extern "C" void __cxa_throw(void* obj, std::type_info* t, void (*)(void*)) {
  std::fflush(stdout);
  std::string names;
  long exc = -1;
  walk(t, names, 0, &exc, 0);
  std::string name = nice(t);
  std::fprintf(stderr, "\x1eZQX%s\n", names.c_str());
  if (exc >= 0) std::fprintf(stderr, "terminate called after throwing an instance of '%s'\n  what():  %s\n", name.c_str(), ((const std::exception*)((const char*)obj + exc))->what());
  else std::fprintf(stderr, "terminate called after throwing an instance of '%s'\n", name.c_str());
  std::fflush(stderr);
  std::_Exit(134);
}
`;

let clang = null, version = '', rtObj = null, patched = false;
let queue = Promise.resolve();
const pchs = new Map(); // head text -> Uint8Array, most recent last, at most 4
const serial = (fn) => { const p = queue.then(fn, fn); queue = p.catch(() => {}); return p; };
const dec = new TextDecoder();
const collector = () => { const parts = []; return { write: (b) => { if (b && b.length) parts.push(dec.decode(b, { stream: true })); }, text: () => parts.join('') + dec.decode(), peek: () => parts.join('') }; };

/* The package's virtual file system copies the whole file on every write, so writing a 13 MB precompiled header
   takes seconds of copying. For the pinned version the write is replaced, at load, by one that grows a buffer
   by doubling; import.meta.url becomes the package URL because the patched copy is imported from a blob: URL. If the
   text is not exactly as expected (another version) the package is imported unchanged and only runs slower. */
const SLOW_WRITE = `  write(contents) {
    const offset = Number(this.offset);
    const newData = new Uint8Array(Math.max(this.file.data.length, offset + contents.length));
    newData.set(this.file.data);
    newData.subarray(offset).set(contents);
    this.file.data = newData;
    this.offset += BigInt(contents.length);
  }`;
const FAST_WRITE = `  write(contents) {
    const f = this.file, offset = Number(this.offset), len = Math.max(f.data.length, offset + contents.length);
    if (!(f.__zqBuf && f.data.buffer === f.__zqBuf && f.data.byteOffset === 0 && len <= f.__zqBuf.byteLength)) {
      const nb = new Uint8Array(Math.max(len, 2 * f.data.length, 65536)); nb.set(f.data); f.__zqBuf = nb.buffer; f.data = nb.subarray(0, f.data.length);
    }
    if (len > f.data.length) f.data = new Uint8Array(f.__zqBuf, 0, len);
    f.data.set(contents, offset);
    this.offset += BigInt(contents.length);
  }`;
const importClang = async (base) => {
  const url = base + 'bundle.js';
  try {
    const text = await (await fetch(url)).text();
    if (text.split(SLOW_WRITE).length === 2) {
      const src = text.replace(SLOW_WRITE, FAST_WRITE).replaceAll('import.meta.url', JSON.stringify(url));
      const blob = URL.createObjectURL(new Blob([src], { type: 'text/javascript' }));
      const mod = await import(blob);
      patched = true;
      return mod;
    }
  } catch (e) { /* fall back to the package as published */ }
  return import(url);
};

const cc = async (args, files, extra = {}) => {
  const err = collector();
  try {
    const out = await clang.runClang(['clang++', ...args], files, { stdout: err.write, stderr: err.write, ...extra });
    return { ok: true, files: out, diag: err.text() };
  } catch (e) {
    if (e && typeof e.code === 'number') return { ok: false, files: e.files || {}, diag: err.text() };
    return { ok: false, files: {}, diag: err.text() + String((e && e.message) || e) };
  }
};
const own = (u8) => (u8.byteOffset === 0 && u8.buffer.byteLength === u8.byteLength ? u8.buffer : u8.slice().buffer);

const buildPch = async (head) => {
  const r = await cc([...FLAGS, '-x', 'c++-header', 'zq_pch.h', '-o', 'zq_pch.h.pch'], { 'zq_pch.h': head });
  return r.ok && r.files['zq_pch.h.pch'] instanceof Uint8Array ? r.files['zq_pch.h.pch'] : null;
};

/* Pass 7: flags from the page (items 402, 452, 476: -W..., -O0 to -O3, -D, -U, -ffast-math, -std), checked again here;
   extra source files (item 403) compiled and linked with main.cpp; a precompiled-header compile that fails because a
   header cannot be opened is retried without the header (item 471) */
const FLAG_OK = /^-(W[\w=+-]*|O[0-3sz]|D[A-Za-z_]\w*(=[\w.+-]*)?|U[A-Za-z_]\w*|f(no-)?fast-math|std=c\+\+(14|17|20))$/;
const argsFor = (flags) => {
  const extra = (flags || []).map(String).filter((f) => FLAG_OK.test(f));
  let base = [...FLAGS];
  const o = extra.filter((f) => /^-O/.test(f)).pop(), std = extra.filter((f) => /^-std=/.test(f)).pop();
  if (o) base = base.map((f) => (/^-O/.test(f) ? o : f));
  if (std) base = base.map((f) => (/^-std=/.test(f) ? std : f));
  return [...base, ...extra.filter((f) => !/^-O|^-std=/.test(f))];
};
const compile = async (m) => {
  const t0 = performance.now();
  const extraFiles = m.files && typeof m.files === 'object' ? Object.entries(m.files).filter(([k]) => /^[\w.-]+\.(cpp|cc|h|hpp)$/.test(k) && k !== 'main.cpp') : [];
  let pch = m.head ? pchs.get(m.head) : null;
  const run = async (usePch) => {
    const files = { 'main.cpp': usePch ? m.srcPch : m.src, 'zq_rt.o': rtObj };
    extraFiles.forEach(([k, v]) => { files[k] = String(v); });
    const args = argsFor(m.flags);
    if (usePch) { files['zq_pch.h'] = m.head; files['zq_pch.h.pch'] = usePch; args.push('-include-pch', 'zq_pch.h.pch'); }
    return cc([...args, 'main.cpp', ...extraFiles.filter(([k]) => /\.(cpp|cc)$/.test(k)).map(([k]) => k), 'zq_rt.o', '-o', 'main.wasm', ...LINK], files);
  };
  let r = await run(pch);
  if (pch && !r.ok && /cannot open file|Out of memory/.test(r.diag || '')) { pchs.delete(m.head); pch = null; r = await run(null); }
  const wasm = r.ok ? r.files['main.wasm'] : null;
  const ms = Math.round(performance.now() - t0);
  if (wasm instanceof Uint8Array) {
    const buf = own(wasm);
    self.postMessage({ type: 'compiled', id: m.id, ok: true, wasm: buf, diag: r.diag, ms, pch: !!pch }, [buf]);
  } else self.postMessage({ type: 'compiled', id: m.id, ok: false, diag: r.diag || 'The compiler stopped without a message.', ms, pch: !!pch });
};

/* ---------- Runner: a minimal WASI preview 1 ---------- */
class WasiExit { constructor(code) { this.code = code; } }
const CAP = 200000;
const runOne = (mod, argv, stdin, live) => {
  const enc = new TextEncoder();
  const input = enc.encode(stdin || '');
  let inPos = 0, mem = null;
  const out = collector(), err = collector();
  let outN = 0, errN = 0;
  const args = argv.map(a => enc.encode(String(a) + '\0'));
  const dv = () => new DataView(mem.buffer);
  const u8 = () => new Uint8Array(mem.buffer);
  const iov = (ptr, n, f) => { let total = 0; const d = dv(); for (let k = 0; k < n; k++) { const p = d.getUint32(ptr + k * 8, true), len = d.getUint32(ptr + k * 8 + 4, true); const got = f(p, len); total += got; if (got < len) break; } return total; };
  const ENOSYS = 52, EBADF = 8, ESPIPE = 70;
  const impl = {
    args_sizes_get(c, s) { const d = dv(); d.setUint32(c, args.length, true); d.setUint32(s, args.reduce((a, b) => a + b.length, 0), true); return 0; },
    args_get(pp, bp) { const d = dv(), m8 = u8(); args.forEach(a => { d.setUint32(pp, bp, true); m8.set(a, bp); pp += 4; bp += a.length; }); return 0; },
    environ_sizes_get(c, s) { const d = dv(); d.setUint32(c, 0, true); d.setUint32(s, 0, true); return 0; },
    environ_get() { return 0; },
    fd_write(fd, ptr, n, nw) {
      if (fd !== 1 && fd !== 2) return EBADF;
      const m8 = u8();
      const total = iov(ptr, n, (p, len) => {
        const chunk = m8.slice(p, p + len);
        if (fd === 1) { if (outN < CAP) out.write(chunk.subarray(0, Math.max(0, CAP - outN))); outN += len; if (live) live(out); } else { if (errN < CAP) err.write(chunk.subarray(0, Math.max(0, CAP - errN))); errN += len; }
        return len;
      });
      dv().setUint32(nw, total, true); return 0;
    },
    fd_read(fd, ptr, n, nr) {
      if (fd !== 0) return EBADF;
      const m8 = u8();
      const total = iov(ptr, n, (p, len) => { const k = Math.min(len, input.length - inPos); m8.set(input.subarray(inPos, inPos + k), p); inPos += k; return k; });
      dv().setUint32(nr, total, true); return 0;
    },
    fd_fdstat_get(fd, p) {
      if (fd > 2) return EBADF;
      const d = dv(); d.setUint8(p, 2); d.setUint16(p + 2, 0, true); d.setBigUint64(p + 8, 0n, true); d.setBigUint64(p + 16, 0n, true); return 0;
    },
    fd_fdstat_set_flags() { return 0; },
    fd_close(fd) { return fd > 2 ? EBADF : 0; },
    fd_seek(fd) { return fd > 2 ? EBADF : ESPIPE; },
    fd_prestat_get() { return EBADF; },
    fd_prestat_dir_name() { return EBADF; },
    fd_filestat_get(fd, p) { if (fd > 2) return EBADF; new Uint8Array(mem.buffer, p, 64).fill(0); dv().setUint8(p + 16, 2); return 0; },
    path_open() { return 76; }, // ENOTCAPABLE: there is no file system
    proc_exit(code) { throw new WasiExit(code); },
    sched_yield() { return 0; },
    clock_res_get(id, p) { dv().setBigUint64(p, 1000n, true); return 0; },
    clock_time_get(id, prec, p) {
      const ns = id === 0 ? BigInt(Date.now()) * 1000000n : BigInt(Math.round(performance.now() * 1e6));
      dv().setBigUint64(p, ns, true); return 0;
    },
    random_get(p, len) { const m8 = u8(); for (let k = 0; k < len; k += 65536) crypto.getRandomValues(m8.subarray(p + k, p + Math.min(len, k + 65536))); return 0; },
    poll_oneoff() { return ENOSYS; },
  };
  const imports = {};
  WebAssembly.Module.imports(mod).forEach(({ module, name, kind }) => {
    if (kind !== 'function') return;
    imports[module] = imports[module] || {};
    imports[module][name] = module === 'wasi_snapshot_preview1' && impl[name] ? impl[name] : () => ENOSYS;
  });
  let code = 0, trap = null;
  const t0 = performance.now();
  try {
    const inst = new WebAssembly.Instance(mod, imports);
    mem = inst.exports.memory;
    inst.exports._start();
  } catch (e) {
    if (e instanceof WasiExit) code = e.code;
    else { trap = e instanceof RangeError ? 'call stack exhausted (a recursion that never stops?)' : String((e && e.message) || e); code = 134; }
  }
  const cut = (c, n) => c.text() + (n > CAP ? `\n[output cut at ${CAP.toLocaleString('en-GB')} characters]` : '');
  return { out: cut(out, outN), err: cut(err, errN), code, trap, ms: performance.now() - t0 };
};

self.onmessage = async (e) => {
  const m = e.data || {};
  if (m.type === 'init') {
    const t0 = performance.now();
    try {
      if (typeof WebAssembly !== 'object') throw new Error('This browser has no WebAssembly support.');
      if (/^-O[0-3s]$/.test(m.opt || '')) FLAGS = FLAGS.map(f => (/^-O/.test(f) ? m.opt : f)); // a benchmarking knob; the page sends none
      const reachable = async (u) => { try { const r = await fetch(u + 'bundle.js', { method: 'HEAD' }); return r.ok; } catch { return false; } };
      const base = (await reachable(m.base)) ? m.base : m.local && (await reachable(m.local)) ? m.local : null;
      if (!base) throw new Error('the compiler CDN (' + m.base + ') is unreachable and there is no local copy in vendor/yowasp-clang/.');
      clang = await importClang(base);
      version = clang.version || '';
      let last = -1;
      const fetchProgress = ({ totalLength, doneLength }) => { const pc = totalLength ? Math.floor(doneLength / totalLength * 100) : 0; if (pc !== last) { last = pc; self.postMessage({ type: 'progress', text: `Downloading the C++ compiler, ${pc}%` }); } };
      if (m.role === 'builder') {
        const r = await cc(['-c', 'zq_warm.cpp', '-o', 'zq_warm.o'], { 'zq_warm.cpp': 'int zq_warm;\n' }, { fetchProgress });
        if (!r.ok) throw new Error(r.diag || 'The compiler did not start.');
      } else {
        const r = await cc([...FLAGS, '-c', 'zq_rt.cpp', '-o', 'zq_rt.o'], { 'zq_rt.cpp': RUNTIME }, { fetchProgress });
        rtObj = r.ok ? r.files['zq_rt.o'] : null;
        if (!(rtObj instanceof Uint8Array)) throw new Error('The C++ runtime did not compile: ' + (r.diag || 'no message'));
      }
      self.postMessage({ type: 'ready', version, patched, ms: Math.round(performance.now() - t0) });
    } catch (err) {
      self.postMessage({ type: 'fail', message: String((err && err.message) || err) });
    }
    return;
  }
  if (m.type === 'pch') {
    serial(async () => {
      const head = String(m.head || '');
      const data = clang ? await buildPch(head).catch(() => null) : null;
      const buf = data ? own(data) : null;
      self.postMessage({ type: 'pch', head, data: buf }, buf ? [buf] : []);
    });
    return;
  }
  if (m.type === 'pch-add') {
    if (m.data) { pchs.delete(m.head); pchs.set(m.head, new Uint8Array(m.data)); while (pchs.size > 4) pchs.delete(pchs.keys().next().value); }
    return;
  }
  if (m.type === 'compile') {
    if (!clang || !rtObj) { self.postMessage({ type: 'compiled', id: m.id, ok: false, diag: 'The C++ compiler is not ready.', ms: 0 }); return; }
    serial(() => compile(m).catch((x) => self.postMessage({ type: 'compiled', id: m.id, ok: false, diag: 'The compiler crashed: ' + ((x && x.message) || x), ms: 0 })));
    return;
  }
  if (m.type === 'exec') {
    try {
      const mod = await WebAssembly.compile(m.wasm);
      (m.cases || []).forEach((c, i) => {
        self.postMessage({ type: 'case', id: m.id, i, phase: 'start' });
        /* item 369: what the case has printed so far is posted every 100 ms, so a timeout can still show it */
        let last = 0;
        const live = (col) => { const t = performance.now(); if (t - last < 100) return; last = t; self.postMessage({ type: 'case', id: m.id, i, phase: 'out', out: col.peek().slice(-20000) }); };
        const r = runOne(mod, ['main', ...(c.argv || []).map(String)], c.stdin == null ? '' : String(c.stdin), live);
        self.postMessage({ type: 'case', id: m.id, i, phase: 'end', ...r });
      });
    } catch (err) {
      self.postMessage({ type: 'crash', id: m.id, message: String((err && err.message) || err) });
    }
    self.postMessage({ type: 'done', id: m.id });
  }
};
