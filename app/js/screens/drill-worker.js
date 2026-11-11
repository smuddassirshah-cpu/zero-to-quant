/* Python runner for the code drill (#drill). A module Web Worker, so the page can terminate it when a run
   passes the 5-second limit. It loads Pyodide from the jsDelivr CDN, defines the grader, then runs one submission per
   message and streams one JSON event per test back to the page.

   Messages in:  { type: 'init', indexURL }   indexURL (optional) is a local vendor/pyodide/ folder, absolute, ending in '/',
                                              tried only when the CDN is unreachable
                 { type: 'run', id, code, spec }
                   spec = { fn, compare: 'isclose' | 'fraction', prelude, tests: [{ prices } | { gen } | { args }, expected] }
                   args and a string expected are Python source, evaluated after the prelude (lambdas for events, Fraction values)
   Messages out: { type: 'ready', version, ms } | { type: 'fail', message }
                 { type: 'event', id, data }   data is JSON: loaded | test | error | done
                 { type: 'pkgs', id, phase: 'start' | 'msg' | 'end', text }   around loading imported packages
                 { type: 'crash', id, message } | { type: 'end', id }

   Deep recursion (ENGINE-BACKLOG 917): the browser's stack, not Python's recursion limit, ends a recursion that passes through C code
   at every level (a generator expression inside min(), sorted(), a C functools.lru_cache). Pyodide then dies with a RangeError and cannot
   be used again. So (1) functools.lru_cache is the pure-Python version (it adds no C stack), (2) the recursion limit is 3,000 at the start
   of every run (a call through lru_cache costs two Python frames), and (3) a run that still overflows the stack is not lost: the test that
   overflowed is reported as a RecursionError, a fresh Pyodide is loaded in this worker, and the tests after it run and are graded. */
'use strict';

let py = null;
let runFn = null;

/* The grader. User code runs as solution.py in a fresh namespace; stdout and stderr are captured per test;
   tracebacks keep only the learner's own frames. Floats are compared with math.isclose(rel_tol=1e-9);
   'fraction' drills accept only a Fraction exactly equal to the expected value. */
const GRADER = String.raw`
import contextlib, io, json, linecache, math, numbers, sys, time, traceback, types, functools, importlib.util
from fractions import Fraction

def _pure_lru():
    # functools.lru_cache without the C wrapper: a C wrapper adds browser stack at every level of a recursion and ends it at about 450 calls.
    src = importlib.util.find_spec('functools').loader.get_source('functools')
    real = sys.modules['_functools']
    shim = types.ModuleType('_functools')
    for k in dir(real):
        if k != '_lru_cache_wrapper':
            setattr(shim, k, getattr(real, k))
    ns = {'__name__': '_zq_functools'}
    sys.modules['_functools'] = shim
    try:
        exec(compile(src, 'functools.py', 'exec'), ns)
    finally:
        sys.modules['_functools'] = real
    return ns['_lru_cache_wrapper']

try:
    functools._lru_cache_wrapper = _pure_lru()
except Exception:
    pass   # keep the C wrapper: only the depth it reaches changes

RECURSION_LIMIT = 3000

def _walk(n, seed, start, step):
    # Seeded random walk built from an integer LCG, so every Python produces the same prices.
    x = seed
    p = start
    out = []
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        p = p * (1 + step * ((x % 2001 - 1000) / 1000))
        out.append(p)
    return out

def _prices(t):
    g = t.get('gen')
    if g:
        return _walk(g['n'], g['seed'], g['start'], g['step'])
    return [float(v) for v in t['prices']]

def _args(t, env):
    # Python source for the argument tuple (events as lambdas), or a list of prices
    if 'args' in t:
        return tuple(eval(compile(t['args'], '<test>', 'eval'), dict(env)))
    return (_prices(t),)

def _expected(t, env):
    e = t['expected']
    return eval(compile(e, '<test>', 'eval'), dict(env)) if isinstance(e, str) else e

def _check(mode, actual, expected):
    # Returns (right type, accepted)
    if mode == 'fraction':
        typed = isinstance(actual, Fraction)
        return typed, typed and actual == expected
    typed = isinstance(actual, numbers.Real) and not isinstance(actual, bool)
    try:
        return typed, typed and math.isclose(actual, expected, rel_tol=1e-9)
    except Exception:
        return typed, False

def _tb(e):
    frames = [f for f in traceback.extract_tb(e.__traceback__) if f.filename == 'solution.py']
    out = []
    if frames:
        out.append('Traceback (most recent call last):\n')
        out.extend(traceback.format_list(frames))
    out.extend(traceback.format_exception_only(type(e), e))
    return ''.join(out).rstrip()

def _cap(s, n=4000):
    return s if len(s) <= n else s[:n] + '\n[output cut at 4,000 characters]'

def _repr(v):
    try:
        return _cap(repr(v), 400)
    except Exception as e:
        return '<repr failed: ' + type(e).__name__ + '>'

def drl_run(code, spec_json, emit):
    spec = json.loads(spec_json)
    sys.setrecursionlimit(RECURSION_LIMIT)
    name = spec['fn']
    mode = spec.get('compare', 'isclose')
    env = {}
    exec(spec.get('prelude', ''), env)
    start = time.perf_counter()
    linecache.cache['solution.py'] = (len(code), None, code.splitlines(True), 'solution.py')
    ns = {'__name__': '__main__'}
    out = io.StringIO()
    try:
        compiled = compile(code, 'solution.py', 'exec')
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(out):
            exec(compiled, ns)
    except BaseException as e:
        emit(json.dumps({'kind': 'error', 'stage': 'load', 'error': _tb(e), 'stdout': _cap(out.getvalue())}))
        return
    fn = ns.get(name)
    if not callable(fn):
        emit(json.dumps({'kind': 'error', 'stage': 'missing', 'error': 'NameError: solution.py does not define ' + name + '()', 'stdout': _cap(out.getvalue())}))
        return
    if not spec.get('resume'):
        emit(json.dumps({'kind': 'loaded', 'stdout': _cap(out.getvalue()), 'ms': (time.perf_counter() - start) * 1000}))
    for i in range(spec.get('from', 0), len(spec['tests'])):
        t = spec['tests'][i]
        args = _args(t, env)
        expected = _expected(t, env)
        buf = io.StringIO()
        err = None
        actual = None
        t0 = time.perf_counter()
        try:
            with contextlib.redirect_stdout(buf), contextlib.redirect_stderr(buf):
                actual = fn(*args)
        except BaseException as e:
            err = _tb(e)
        ms = (time.perf_counter() - t0) * 1000
        typed, ok = _check(mode, actual, expected)
        emit(json.dumps({'kind': 'test', 'i': i, 'ok': bool(ok and err is None), 'actual': None if err else _repr(actual),
                         'type': type(actual).__name__, 'number': bool(typed), 'error': err,
                         'stdout': _cap(buf.getvalue()), 'ms': ms}))
    emit(json.dumps({'kind': 'done', 'ms': (time.perf_counter() - start) * 1000}))
`;

/* Pyodide comes from the jsDelivr CDN (docs/PLAN.md section 3). A local copy (vendor/pyodide/, passed by the page as
   indexURL) is used only when the CDN cannot be reached and that copy actually exists. */
const CDN = 'https://cdn.jsdelivr.net/pyodide/v0.27.7/full/';
const reachable = async (url) => { try { const r = await fetch(url, { method: 'HEAD' }); return r.ok; } catch { return false; } };
const pickIndexURL = async (local) => {
  if (await reachable(CDN + 'pyodide.mjs')) return CDN;
  if (local && await reachable(local + 'pyodide.mjs')) return local;
  throw new Error('Python could not be loaded: the Pyodide CDN is unreachable and there is no local copy in vendor/pyodide.');
};

let indexURL = null;
/* Loads a Pyodide into this worker and defines the grader; used at start and again after a stack overflow kills the one in use */
const boot = async () => {
  const { loadPyodide } = await import(indexURL + 'pyodide.mjs'); // this Pyodide build needs a module worker
  py = await loadPyodide({ indexURL, stdout: () => {}, stderr: () => {} });
  py.runPython(GRADER);
  runFn = py.globals.get('drl_run');
};

/* The browser stack ran out inside Python: a RangeError, or Pyodide's refusal to run after one */
const isStackOverflow = (err) => err instanceof RangeError || /call stack|fatally failed/i.test(String((err && err.message) || err));
const DEEP = 'RecursionError: maximum recursion depth exceeded. This recursion went too deep for the Python in this page (it passes through a generator expression, min(), sorted() or similar at each call, which stops it at about 300 to 400 calls). Use a loop or a table, or keep the recursion shallower. Python was restarted for the tests after this one.';

self.onmessage = async (e) => {
  const m = e.data || {};
  if (m.type === 'init') {
    const t0 = performance.now();
    try {
      if (typeof WebAssembly !== 'object') throw new Error('This browser has no WebAssembly support.');
      indexURL = await pickIndexURL(m.indexURL);
      await boot();
      const version = py.runPython('import sys\n"%d.%d" % sys.version_info[:2]');
      self.postMessage({ type: 'ready', version, ms: Math.round(performance.now() - t0) });
    } catch (err) {
      self.postMessage({ type: 'fail', message: String((err && err.message) || err) });
    }
    return;
  }
  if (m.type === 'run') {
    const emit = (s) => self.postMessage({ type: 'event', id: m.id, data: String(s) });
    try {
      if (!runFn) throw new Error('Python is not ready.');
      // Packages the learner imports (numpy, pandas) are fetched from the CDN on first use. The page is told when the
      // load starts and ends ({ type: 'pkgs', phase }), so it can keep that time out of the run's limit and say what is
      // loading (item 161); pages that do not know the message ignore it.
      const pk = (phase, text) => self.postMessage({ type: 'pkgs', id: m.id, phase, text });
      const prepare = async () => {
        pk('start');
        try { await py.loadPackagesFromImports(m.code, { messageCallback: (t) => pk('msg', String(t)), errorCallback: (t) => pk('msg', String(t)) }); } catch (e) { emit('Package load failed: ' + ((e && e.message) || e)); }
        pk('end');
        // Item 120: every run starts in a fresh, empty working directory, so files written by one run are gone in the next
        py.runPython("import os as _o, shutil as _s, tempfile as _t\n_p = globals().get('_zq_run_dir')\n_o.chdir('/')\nif _p: _s.rmtree(_p, ignore_errors=True)\n_zq_run_dir = _t.mkdtemp(prefix='run-')\n_o.chdir(_zq_run_dir)\nimport warnings as _w\n_w.filterwarnings('ignore', category=FutureWarning)\n_w.filterwarnings('ignore', category=DeprecationWarning)"); // item 182: library deprecation notices stay out of the learner's output
      };
      await prepare();
      /* ENGINE-BACKLOG 917: a stack overflow kills this Pyodide. Report the test that overflowed, load a new one and carry on after it. */
      const seen = { loaded: false, last: -1 };
      const watch = (s) => { emit(s); try { const d = JSON.parse(s); if (d.kind === 'loaded') seen.loaded = true; else if (d.kind === 'test') seen.last = d.i; } catch { /* not JSON */ } };
      const n = (m.spec && m.spec.tests ? m.spec.tests.length : 0), t0 = performance.now();
      let from = 0, resume = false;
      for (;;) {
        try { runFn(m.code, JSON.stringify({ ...m.spec, from, resume }), watch); break; }
        catch (err) {
          if (!isStackOverflow(err)) throw err;
          if (!seen.loaded) { emit(JSON.stringify({ kind: 'error', stage: 'load', error: DEEP, stdout: '' })); break; }
          const i = seen.last + 1;
          seen.last = i;
          emit(JSON.stringify({ kind: 'test', i, ok: false, actual: null, type: 'NoneType', number: false, error: DEEP, stdout: '', ms: 0 }));
          if (i + 1 >= n) { emit(JSON.stringify({ kind: 'done', ms: performance.now() - t0 })); break; }
          pk('start'); pk('msg', 'Restarting Python after a recursion that went too deep');
          py = null; runFn = null;
          await boot();
          await prepare();
          from = i + 1; resume = true;
        }
      }
    } catch (err) {
      self.postMessage({ type: 'crash', id: m.id, message: String((err && err.message) || err) });
    }
    self.postMessage({ type: 'end', id: m.id });
  }
};
