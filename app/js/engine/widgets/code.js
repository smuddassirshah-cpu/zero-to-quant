/* Code widget (docs/AUTHORING.md 3, design-research 5.3 no. 10). The editor from drill.js (line numbers, Python
   highlighting, Tab inserts 4 spaces, Shift Tab dedents, Esc then Tab leaves). "Run examples" runs the visible
   examples; the player's Check runs the hidden tests. Both go to js/screens/drill-worker.js with the drill's own
   messages ({ type: 'init', indexURL } then { type: 'run', id, code, spec }). Each test is wrapped by a small
   harness appended to the learner's code, so one worker spec covers every compare mode (isclose, equal, fraction):
   the harness returns 1.0 for a pass and prints the actual value after a marker, which the widget reads back.
   grade() returns a Promise; results are cached per source text. Results show per test. Drafts: with ctx.draftKey the
   source is saved with ZQ.state.drills.draft(key, code) as you type and restored when the item opens again.
   Script mode (any example or test with compare "stdout" or a stdin): the learner's code is not run at load. The
   harness carries it as a string and runs it afresh for every case, with input() and sys.stdin fed from that case's
   stdin and print output captured; a stdout case compares the captured text with expect (whitespace-normalised, or
   exactly with exact: true), and a call case is evaluated in that run's namespace, which also holds printed (the
   captured lines as a list). input() prompts are not part of the output. Any case may carry setup (Python run before
   call); compare "raises" passes when the call (or, in script mode with no call, the program) raises the named
   exception or a subclass.
   Item 430: isclose is complex-aware (cmath.isclose, same tolerances): a function may return a complex number or a
   NumPy complex array and the case's expect can be written as a complex literal such as (0.5-0.5j).
   Pass 7: a case may carry tol: { rel, abs } for isclose (items 378, 425, 464), shown in its row; each case has its own
   time limit (5 s, plus the case's budget or the widget's caseBudget) reported against the case that hit it, so a slow
   attempt stops after one case (items 394, 419); __learner_source__ is always defined (item 395); a stdout case may
   check only some lines (lines: true, every expected line in order) or a pattern (match: "regex") (item 451). */
(function () {
  'use strict';
  const Z = window.ZQ;
  const PYODIDE = 'https://cdn.jsdelivr.net/pyodide/v0.27.7/full/';
  const TEST_MS = 5000, LOAD_MS = 60000, PKG_MS = 120000;
  const MARK = '\u001eZQ';

  /* ---------- Python highlighting (from drill.js) ---------- */
  const KW = new Set('False None True and as assert async await break case class continue def del elif else except finally for from global if import in is lambda match nonlocal not or pass raise return try while with yield'.split(' '));
  const BI = new Set('abs all any bool dict enumerate filter float int isinstance len list map max min print range reversed round set sorted str sum tuple zip'.split(' '));
  const TOK = /(#[^\n]*)|((?:\b[rRbBfFuU]{1,2})?(?:"""[\s\S]*?(?:"""|$)|'''[\s\S]*?(?:'''|$)|"(?:[^"\\\n]|\\.)*"?|'(?:[^'\\\n]|\\.)*'?))|(\b\d[\d_]*(?:\.[\d_]*)?(?:[eE][+-]?\d+)?j?|\.\d[\d_]*(?:[eE][+-]?\d+)?)|([A-Za-z_]\w*)/g;
  const escH = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  const highlight = (src) => {
    let out = '', last = 0, prev = '';
    src.replace(TOK, (m, com, str, nm, id, at) => {
      out += escH(src.slice(last, at)); last = at + m.length;
      let cls = '';
      if (com) cls = 'com';
      else if (str) cls = /^[rRbBfFuU]{0,2}("""|''')/.test(str) ? 'doc' : 'str';
      else if (nm) cls = 'num';
      else if (id) cls = KW.has(id) ? 'kw' : (prev === 'def' || prev === 'class') ? 'fn' : BI.has(id) ? 'bi' : '';
      prev = id || '';
      out += cls ? `<span class="tok-${cls}">${escH(m)}</span>` : escH(m);
      return m;
    });
    return out + escH(src.slice(last));
  };

  /* ---------- Editor (from drill.js) ---------- */
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
      if (line.replace(/#.*$/, '').trimEnd().endsWith(':')) ind += '    ';
      else if (/^\s*(return|pass|break|continue|raise)\b/.test(line)) ind = ind.slice(0, Math.max(0, ind.length - 4));
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

  /* ---------- One shared Python runner (the drill's PyRunner, trimmed) ---------- */
  const Py = (() => {
    let w = null, status = 'idle', reason = '', run = null, gen = 0, loadTimer = 0;
    const subs = new Set();
    const set = (s) => { status = s; subs.forEach(f => f(s)); };
    const kill = () => { clearTimeout(loadTimer); if (run) { clearTimeout(run.timer); run = null; } if (w) { w.onmessage = null; w.onerror = null; w.terminate(); w = null; } };
    const unavailable = (msg) => { kill(); reason = msg; set('unavailable'); };
    const end = (info) => { const r = run; if (!r) return; clearTimeout(r.timer); run = null; r.onEnd(info); };
    const start = (restart = false) => {
      kill();
      const my = ++gen;
      set(restart ? 'restarting' : 'loading');
      if (typeof WebAssembly !== 'object' || typeof Worker !== 'function') { unavailable('This browser cannot run WebAssembly in a background worker.'); return; }
      try { w = new Worker(new URL('js/screens/drill-worker.js', location.href).href, { type: 'module' }); } catch (err) { unavailable(String((err && err.message) || err)); return; }
      w.onmessage = (e) => {
        if (my !== gen) return;
        const m = e.data || {};
        if (m.type === 'ready') { clearTimeout(loadTimer); set('ready'); return; }
        if (m.type === 'fail') { unavailable(m.message); return; }
        if (!run || m.id !== run.id) return;
        if (m.type === 'event') {
          let d = null; try { d = JSON.parse(m.data); } catch { return; }
          if (run.perCase && (d.kind === 'loaded' || d.kind === 'test')) { const r = run; r.at = d.kind === 'loaded' ? 0 : d.i + 1; r.limit = r.perCase(r.at); clearTimeout(r.timer); r.timer = setTimeout(() => { end({ timeout: true, at: r.at }); start(true); }, r.limit); }
          run.onEvent(d);
        }
        else if (m.type === 'pkgs') { // item 161: package loading is kept out of the run's limit (2 minutes of its own)
          clearTimeout(run.timer);
          const r = run;
          if (m.phase === 'end') r.timer = setTimeout(() => { end({ timeout: true, at: r.at }); start(true); }, r.limit);
          else r.timer = setTimeout(() => { end({ timeout: true, loading: true }); start(true); }, PKG_MS);
          if (m.phase === 'msg' && r.onPkgs) r.onPkgs(String(m.text || ''));
        }
        else if (m.type === 'crash') run.crash = m.message;
        else if (m.type === 'end') { const crash = run.crash; end({ crash }); set('ready'); if (crash) start(true); }
      };
      w.onerror = (e) => {
        if (e && e.preventDefault) e.preventDefault();
        if (my !== gen) return;
        const msg = (e && e.message) || 'The Python worker could not start.';
        if (run) { end({ crash: msg }); start(true); } else unavailable(msg);
      };
      w.postMessage({ type: 'init', indexURL: PYODIDE });
      loadTimer = setTimeout(() => { if (my === gen) unavailable('Python took more than a minute to load.'); }, LOAD_MS);
    };
    /* items 394, 419: perCase(k) is the limit for case k (k = -1 while the code loads); each event re-arms the timer, so
       a timeout names the case that hit it */
    const exec = (code, spec, limit, onEvent, onEnd, onPkgs, perCase) => {
      if (status !== 'ready' || !w) return false;
      run = { id: Date.now() + Math.random(), onEvent, onEnd, onPkgs, crash: null, limit, perCase, at: -1 };
      if (perCase) limit = run.limit = perCase(-1);
      run.timer = setTimeout(() => { end({ timeout: true, at: -1 }); start(true); }, limit);
      set('running');
      w.postMessage({ type: 'run', id: run.id, code, spec });
      return true;
    };
    return {
      ensure() { if (status === 'idle') start(); },
      exec, sub(f) { subs.add(f); return () => subs.delete(f); },
      get status() { return status; }, get reason() { return reason; },
    };
  })();

  /* Shared by both harnesses: __zq_raises (compare "raises", item 137: the call raises the named exception or a
     subclass) and __zq_cmp (the value compares); each prints the marker and the actual value. setup (item 136) runs
     first, in each harness's case function. */
  const JUDGE = `
def __zq_raises(_call, _exp, _ns):
    try:
        _a = eval(_call, _ns)
    except Exception as _x:
        print(${JSON.stringify(MARK)} + 'raised ' + type(_x).__name__, end='')
        return 1.0 if _exp.strip().strip(chr(34) + chr(39)) in [_k.__name__ for _k in type(_x).__mro__] else 0.0
    print(${JSON.stringify(MARK)} + 'no error, the value was ' + repr(_a), end='')
    return 0.0

def __zq_cmp(_a, _exp, _cmp, _ns, _tol=None):
    import math as _m
    from fractions import Fraction as _F
    print(${JSON.stringify(MARK)} + repr(_a), end='')
    _e = eval(_exp, _ns)
    if _cmp == 'fraction':
        return 1.0 if isinstance(_a, _F) and _a == _e else 0.0
    # arrays, Series and nested lists compare element by element (item 143): tolist() first
    def _flat(_v):
        return _v.tolist() if hasattr(_v, 'tolist') and not isinstance(_v, (int, float, complex, str)) else _v
    def _close(_x, _y):
        _x, _y = _flat(_x), _flat(_y)
        if isinstance(_x, (list, tuple)) or isinstance(_y, (list, tuple)):
            return isinstance(_x, (list, tuple)) and isinstance(_y, (list, tuple)) and len(_x) == len(_y) and all(_close(_p, _q) for _p, _q in zip(_x, _y))
        if isinstance(_x, (str, bytes)) and not isinstance(_y, (str, bytes)):
            return False  # item 121: "0.05" is text, not the number 0.05
        # item 430: a complex value (Python, or a NumPy complex scalar) compares as cmath.isclose, with the same tolerances
        if any(isinstance(_v, complex) or type(_v).__name__.startswith('complex') for _v in (_x, _y)):
            try:
                import cmath as _cm
                _rt, _at = (float(_tol[0]), float(_tol[1])) if _tol else (1e-9, 1e-12)
                return _cm.isclose(complex(_x), complex(_y), rel_tol=_rt, abs_tol=_at)
            except Exception:
                return _x == _y
        try:
            if _tol:
                return _m.isclose(float(_x), float(_y), rel_tol=float(_tol[0]), abs_tol=float(_tol[1]))
            return _m.isclose(float(_x), float(_y), rel_tol=1e-9, abs_tol=1e-12)
        except Exception:
            return _x == _y
    if _cmp == 'isclose':
        return 1.0 if _close(_a, _e) else 0.0
    try:
        return 1.0 if bool(_flat(_a) == _flat(_e)) else 0.0
    except Exception:
        return 0.0
`;
  /* The harness: one function the worker calls per case, returning 1.0 for a pass */
  /* tol: { rel, abs } on a case: math.isclose with those tolerances (a missing one is 0) */
  const tolOf = (c) => (c.tol && typeof c.tol === 'object' && (Number.isFinite(+c.tol.rel) || Number.isFinite(+c.tol.abs)) ? [Math.max(0, +c.tol.rel || 0), Math.max(0, +c.tol.abs || 0)] : typeof c.tol === 'number' && c.tol >= 0 ? [0, c.tol] : null);
  /* ENGINE-BACKLOG 595: a test's setup lines are read for imports too, so a data test that imports pandas loads it though the learner's code does not */
  const harness = (cases, src) => `
${importHint(...cases.map(c => c.setup == null ? '' : String(c.setup)))}${JUDGE}
def __zq_case(_i):
    _call, _exp, _cmp, _setup, _tol = __ZQ_CASES[_i]
    if _setup:
        exec(_setup, globals())
    if _cmp == 'raises':
        return __zq_raises(_call, _exp, globals())
    _a = eval(_call, globals())  # evaluated here, one frame under the worker, as before
    return __zq_cmp(_a, _exp, _cmp, globals(), _tol)

if '__learner_source__' not in globals():
    __learner_source__ = ${JSON.stringify(String(src ?? ''))}
__ZQ_CASES = __import__('json').loads(${JSON.stringify(JSON.stringify(cases.map(c => [String(c.call ?? ''), String(c.expect ?? ''), c.compare || 'equal', c.setup == null ? '' : String(c.setup), tolOf(c)])))})
`;
  /* Script mode harness: the learner's source runs once per case in a fresh namespace (see the header) */
  /* The worker loads packages from the imports it can see (loadPackagesFromImports); in script mode the learner's code is
     a string, so its import lines are repeated, never run, under if False */
  /* inbox (backtest 1, alpha 1, opt-dash 1): "import numpy as np, pandas as pd" names both packages (an alias used to end
     the list, so pandas never loaded) */
  const importsOf = (src) => String(src).split('\n').map(l => l.match(/^\s*(?:import\s+([\w.]+(?:\s+as\s+\w+)?(?:\s*,\s*[\w.]+(?:\s+as\s+\w+)?)*)|from\s+([\w.]+)\s+import\b)/)).filter(Boolean)
    .flatMap(m => (m[1] ? m[1].split(',').map(x => x.replace(/\s+as\s+\w+\s*$/, '')) : [m[2]]).map(x => x.trim())).filter(x => x && !x.startsWith('.'));
  const importHint = (...srcs) => { const im = [...new Set(srcs.flatMap(importsOf))]; return im.length ? 'if False:\n' + im.map(x => '    import ' + x).join('\n') + '\n' : ''; };
  Z.widgets.codeImports = { importsOf, importHint, harness };   // read by tools/test-engine-runtime.mjs
  /* item 163: prelude (hidden Python run in the learner's namespace before their code) and postlude (run after it).
     With either, the learner's code is carried as a string and compiled as solution.py, so its line numbers stay true. */
  /* inbox (backtest 2): files: { "engine_lib.py": "..." } are written into the run's working directory (on sys.path)
     before the prelude, so the learner's code and a pytest file can import helper modules */
  const filesCode = (files) => (files && typeof files === 'object' && Object.keys(files).length ? `import sys as _zfs\nif '' not in _zfs.path: _zfs.path.insert(0, '')\nfor _zn, _zt in __import__('json').loads(${JSON.stringify(JSON.stringify(files))}).items():\n    open(_zn, 'w').write(_zt)\n` : '');
  const loadHarness = (src, pre, post, files) => `${importHint(src, pre, post, ...Object.values(files || {}))}${filesCode(files)}import linecache as _zlc
__ZQ_SRC = ${JSON.stringify(src)}
__ZQ_PRE = ${JSON.stringify(pre)}
__ZQ_POST = ${JSON.stringify(post)}
_zlc.cache['solution.py'] = (len(__ZQ_SRC), None, __ZQ_SRC.splitlines(True), 'solution.py')

def __zq_load():
    _g = globals()
    _g['__learner_source__'] = __ZQ_SRC
    if __ZQ_PRE:
        exec(compile(__ZQ_PRE, '<prelude>', 'exec'), _g)
    exec(compile(__ZQ_SRC, 'solution.py', 'exec'), _g)
    if __ZQ_POST:
        exec(compile(__ZQ_POST, '<postlude>', 'exec'), _g)

__zq_load()
`;
  const scriptHarness = (src, cases, pre = '', post = '', files = null) => `
${importHint(src, pre, post, ...Object.values(files || {}), ...cases.map(c => c.setup == null ? '' : String(c.setup)))}${filesCode(files)}import sys as _zs, io as _zio, linecache as _zlc
__ZQ_SRC = ${JSON.stringify(src)}
__ZQ_PRE = ${JSON.stringify(pre)}
__ZQ_POST = ${JSON.stringify(post)}
_zlc.cache['solution.py'] = (len(__ZQ_SRC), None, __ZQ_SRC.splitlines(True), 'solution.py')
__ZQ_CODE = compile(__ZQ_SRC, 'solution.py', 'exec')
__ZQ_CASES = __import__('json').loads(${JSON.stringify(JSON.stringify(cases.map(c => [c.call == null ? '' : String(c.call), String(c.expect ?? ''), c.compare || (c.call == null ? 'stdout' : 'equal'), c.stdin == null ? '' : String(c.stdin), !!c.exact, c.setup == null ? '' : String(c.setup), Array.isArray(c.argv) ? c.argv.map(String) : [], tolOf(c), !!c.lines, c.match == null ? '' : String(c.match)])))})
${JUDGE}
def __zq_norm(_t):
    _ls = [_l.rstrip() for _l in _t.replace('\\r\\n', '\\n').split('\\n')]
    while _ls and not _ls[0]: _ls.pop(0)
    while _ls and not _ls[-1]: _ls.pop()
    return _ls

def __zq_case(_i):
    import math as _m
    from fractions import Fraction as _F
    _call, _exp, _cmp, _stdin, _exact, _setup, _argv, _tol, _lines, _match = __ZQ_CASES[_i]
    _feed = _zio.StringIO(_stdin)
    _out = _zio.StringIO()
    def _input(prompt=''):
        _ln = _feed.readline()
        if not _ln:
            raise EOFError('EOF when reading a line (this test gives input() no more lines)')
        return _ln[:-1] if _ln.endswith('\\n') else _ln
    _ns = {'__name__': '__main__', 'input': _input}
    _old = (_zs.stdout, _zs.stdin)
    _oldargv = list(_zs.argv)
    _zs.argv = ['main.py'] + list(_argv)  # item 140: argv per case, as python3 main.py a b would give
    _zs.stdout, _zs.stdin = _out, _feed
    _ns['__learner_source__'] = __ZQ_SRC
    try:
        if __ZQ_PRE:
            exec(compile(__ZQ_PRE, '<prelude>', 'exec'), _ns)
        exec(__ZQ_CODE, _ns)
        if __ZQ_POST:
            exec(compile(__ZQ_POST, '<postlude>', 'exec'), _ns)
    except SystemExit:
        pass
    except BaseException as _x:
        _zs.stdout, _zs.stdin = _old
        print(_out.getvalue(), end='')
        if _cmp == 'raises' and not _call and isinstance(_x, Exception):
            print(${JSON.stringify(MARK)} + 'raised ' + type(_x).__name__, end='')
            return 1.0 if _exp.strip().strip(chr(34) + chr(39)) in [_k.__name__ for _k in type(_x).__mro__] else 0.0
        raise
    finally:
        _zs.stdout, _zs.stdin = _old
        _zs.argv = _oldargv
    _txt = _out.getvalue()
    print(_txt, end='')
    _ns['printed'] = _txt.splitlines()
    if _cmp == 'stdout':
        print(${JSON.stringify(MARK)}, end='')
        if _match:
            import re as _re
            return 1.0 if _re.search(_match, _txt, _re.M) else 0.0
        if _lines:
            _want, _have, _k = __zq_norm(_exp), __zq_norm(_txt), 0
            for _l in _have:
                if _k < len(_want) and _l == _want[_k]:
                    _k += 1
            return 1.0 if _k == len(_want) else 0.0
        if _exact:
            return 1.0 if _txt == _exp else 0.0
        return 1.0 if __zq_norm(_txt) == __zq_norm(_exp) else 0.0
    if _cmp == 'raises' and not _call:
        print(${JSON.stringify(MARK)} + 'no error: the program ran to the end', end='')
        return 0.0
    if _setup:
        exec(_setup, _ns)
    if _cmp == 'raises':
        return __zq_raises(_call, _exp, _ns)
    return __zq_cmp(eval(_call, _ns), _exp, _cmp, _ns, _tol)
`;
  /* item 169: library housekeeping lines (matplotlib's font cache notice, warnings that slip through) are not the learner's output */
  const quietLib = (t) => String(t || '').split('\n').filter(l => !/^Matplotlib is building the font cache|^\S+\.py:\d+: (FutureWarning|DeprecationWarning):/.test(l)).join('\n');
  const isOut = (c) => c.compare === 'stdout' || (c.call == null && c.expect != null && c.compare == null);
  /* Tracebacks keep only the learner's frames: harness functions (__zq_*), <string>, and the harness line that calls
     __zq_load are dropped, each with its source and caret lines */
  const cleanTb = (tb) => {
    const L = String(tb || '').split('\n'), out = [], head = (s) => /^\s*File "/.test(s);
    const frames = []; let cur = null;
    L.forEach((ln) => {
      if (head(ln)) { cur = { head: ln, body: [] }; frames.push(cur); }
      else if (cur && /^\s{4}/.test(ln)) cur.body.push(ln);
      else { cur = null; frames.push({ text: ln }); }
    });
    frames.forEach((f, i) => {
      if (f.text != null) { out.push(f.text); return; }
      const next = frames.slice(i + 1).find(x => x.head);
      if (/in __zq_\w+$|File "<string>"/.test(f.head) || (/in <module>$/.test(f.head) && next && /in __zq_load$/.test(next.head))) return;
      out.push(f.head, ...f.body);
    });
    return out.join('\n');
  };

  Z.widgets.register('code', (host, spec, ctx) => {
    if (spec.language === 'cpp' && Z.cppCode) return Z.cppCode(host, spec, ctx); // item 304: C++ is compiled and graded by js/engine/widgets/cpp-grade.js
    const examples = spec.examples || [], tests = spec.tests || [];
    /* ENGINE-BACKLOG 469 (E14): spec.data { "name.csv": "content/data/..." } is copied into the working directory before every run;
       a read-only peek at the first rows sits under the editor unless dataPeek is false */
    const dataMap = spec.data && typeof spec.data === 'object' && Object.keys(spec.data).length && Z.content && Z.content.dataFiles ? spec.data : null;
    const hasData = !!dataMap && spec.dataPeek !== false;
    let dataP = null;
    const loadData = () => (dataP || (dataP = dataMap ? Z.content.dataFiles(dataMap).catch(e => { dataP = null; throw e; }) : Promise.resolve({})));
    const el = Z.h(`<div class="wd-code">
      <div class="wd-code-head">
        <span class="t-label">${spec.language === 'python' || !spec.language ? 'Python' : Z.esc(spec.language)}</span>
        <span class="wd-py t-caption" aria-live="polite"></span>
        <button type="button" class="btn secondary wd-run" disabled>${Z.icon('play', 'sm')} Run examples</button>
      </div>
      <div class="wd-ed"></div>
      ${hasData ? '<details class="wd-code-data"><summary class="t-caption">Data files in the working directory</summary><div class="wd-code-data-b t-caption">Loading the files…</div></details>' : ''}
      <p class="t-caption wd-code-keys"><kbd>Tab</kbd> indents. <kbd>Esc</kbd> then <kbd>Tab</kbd> leaves the editor. <kbd>Ctrl</kbd> <kbd>Enter</kbd> runs the examples. Check runs the hidden tests.</p>
      ${spec.how ? `<p class="t-caption wd-code-how">${Z.grade.inline(spec.how)}</p>` : ''}
      <div class="wd-res" aria-live="polite"></div>
    </div>`);
    host.append(el);
    const runBtn = el.querySelector('.wd-run'), pyEl = el.querySelector('.wd-py'), res = el.querySelector('.wd-res'), edHost = el.querySelector('.wd-ed');
    let alive = true, busy = false, cache = null, locked = false, saveT = 0, quiet = false;
    /* Drafts: with ctx.draftKey (the player passes course/lesson/item or exam/item) the source is kept with
       ZQ.state.drills.draft(key, code), 400ms after the last keystroke, and reopens from there */
    const D = Z.state && Z.state.drills && typeof Z.state.drills.draft === 'function' && ctx.draftKey ? Z.state.drills : null;
    const draft = (v) => { try { return D ? D.draft(ctx.draftKey, v) : null; } catch (e) { console.error(e); return null; } };
    const saved = D ? draft() : null;
    const ed = Editor(edHost, { value: typeof saved === 'string' && saved.trim() ? saved : spec.starter || '', label: 'Code editor', onInput: () => {
      if (D && !quiet) { clearTimeout(saveT); saveT = setTimeout(() => draft(ed.value === (spec.starter || '') ? null : ed.value), 400); }
      ctx.change && ctx.change({ code: ed.value });
    }, onRun: () => runExamples() });
    const sync = (s = Py.status) => {
      if (!alive) return;
      const txt = { idle: 'Python not loaded', loading: 'Loading Python', restarting: 'Restarting Python', ready: 'Python ready', running: 'Running', unavailable: 'Python is not available here' }[s] || '';
      pyEl.textContent = txt; pyEl.dataset.s = s;
      runBtn.disabled = busy || locked || s !== 'ready';
      ctx.change && ctx.change({ code: ed.value, status: s });
    };
    const unsub = Py.sub(sync);
    Py.ensure(); sync();

    const pre = (t, cls = 'wd-res-out') => `<pre class="${cls} t-code">${Z.esc(t)}</pre>`;
    const outRow = (r) => {
      const said = r.stdout.trim() ? pre(r.stdout) : '<div class="t-caption">Your code printed nothing.</div>';
      const input = (r.argv && r.argv.length ? `<div class="t-caption">Run as</div>${pre('python3 main.py ' + r.argv.map(a => (/\s/.test(a) ? JSON.stringify(a) : a)).join(' '), 'wd-res-out wd-res-in')}` : '') + (r.stdin ? `<div class="t-caption">Input</div>${pre(r.stdin.replace(/\n$/, ''), 'wd-res-out wd-res-in')}` : '');
      if (r.error) return `${input}${pre(cleanTb(r.error), 'wd-res-err')}${r.stdout.trim() ? `<div class="t-caption">Printed before the error</div>${said}` : ''}`;
      if (r.ok) return `${input}<div class="t-caption">Printed the expected output</div>${said}`;
      return `${input}<div class="t-caption">Expected output</div>${pre(r.expect.replace(/\n$/, ''))}<div class="t-caption">Your code printed</div>${said}`;
    };
    const row = (r, label) => `<li class="wd-res-row ${r.ok ? 'ok' : 'bad'}">
        <span class="wd-res-ic" aria-hidden="true">${Z.icon(r.ok ? 'check' : 'cross', 'xs')}</span>
        <div class="wd-res-b"><div class="wd-res-h"><b>${label}</b> ${r.out ? (r.stdin ? 'what it prints with this input' : 'what it prints') : r.call ? `${r.setup ? `<code class="lsn-ic">${Z.esc(r.setup)}</code> then ` : ''}<code class="lsn-ic">${Z.esc(r.call)}</code>` : 'the whole program'}</div>
        ${r.out ? outRow(r) : `${r.error ? pre(cleanTb(r.error), 'wd-res-err') : r.raises ? `<div class="t-caption">Expected it to raise <code class="lsn-ic">${Z.esc(r.expect)}</code>, got <code class="lsn-ic">${Z.esc(r.actual ?? 'nothing')}</code></div>` : `<div class="t-caption">Expected <code class="lsn-ic">${Z.esc(r.expect)}</code>${r.tol ? ` (within ${[r.tol[0] ? 'relative ' + r.tol[0] : '', r.tol[1] ? 'absolute ' + r.tol[1] : ''].filter(Boolean).join(' or ')})` : ''}, got <code class="lsn-ic">${Z.esc(r.actual ?? 'nothing')}</code></div>`}
        ${r.stdout ? pre(r.stdout) : ''}`}</div></li>`;
    const render = (title, rows, cases, extra = '') => {
      const n = rows.filter(r => r.ok).length;
      res.innerHTML = `<div class="wd-res-top"><span class="t-label">${title}</span><span class="t-caption">${n} of ${cases.length} passed</span></div>${extra}<ol class="wd-res-list">${rows.map((r, i) => row(r, (title === 'Examples' ? 'Example ' : 'Test ') + (i + 1))).join('')}</ol>`;
    };
    /* Run a list of cases; resolves to { rows, error } */
    const script = [...examples, ...tests].some(c => isOut(c) || c.stdin != null || c.argv != null || (c.compare === 'raises' && c.call == null));
    const runCases0 = (cases, dataTexts) => new Promise((resolve) => {
      const pre = String(spec.prelude || ''), post = String(spec.postlude || '');
      const own = spec.files && typeof spec.files === 'object' && Object.keys(spec.files).length ? spec.files : null;
      const files = dataTexts && Object.keys(dataTexts).length ? { ...(own || {}), ...dataTexts } : own; // data files are written like files, before the prelude
      const code = script ? scriptHarness(ed.value, cases, pre, post, files) : (pre || post || files ? loadHarness(ed.value, pre, post, files) : ed.value) + harness(cases, ed.value);
      const rows = cases.map(c => ({ tol: tolOf(c), argv: Array.isArray(c.argv) ? c.argv.map(String) : null, call: c.call ?? '', raises: c.compare === 'raises', setup: c.setup == null ? '' : String(c.setup), expect: String(c.expect ?? ''), out: isOut(c), stdin: c.stdin == null ? '' : String(c.stdin), ok: false, actual: null, error: null, stdout: '' }));
      let loadErr = null, loaded = '';
      /* item 143: spec.budget (ms) is added to the run's limit; code importing numpy, pandas or scipy gets 30 s on top
         without one, so the first package load is not charged against the 5 s per case */
      const heavy = /^\s*(?:import|from)\s+(numpy|pandas|scipy|matplotlib|pytest|sklearn|statsmodels)\b/m.test(ed.value + '\n' + String(spec.prelude || '') + '\n' + String(spec.postlude || '') + '\n' + Object.values(spec.files || {}).join('\n'));
      const extra = (spec.budget != null ? Math.max(0, +spec.budget || 0) : 0) + (heavy ? 30000 : 0); // inbox (alpha 4): budget adds to the heavy-import allowance
      const limit = TEST_MS * Math.max(1, cases.length) + extra;
      /* the load gets 5 s plus the widget's budget (or 30 s for heavy imports); each case 5 s plus its own budget, the
         widget's caseBudget, or, when the widget has a budget, that budget again (a slow numpy case keeps its room) */
      const caseMs = (k) => (k < 0 ? TEST_MS + extra : TEST_MS + (cases[k] && cases[k].budget != null ? Math.max(0, +cases[k].budget || 0) : spec.caseBudget != null ? Math.max(0, +spec.caseBudget || 0) : extra));
      const ok = Py.exec(code, { fn: '__zq_case', compare: 'isclose', prelude: '', tests: cases.map((_, i) => ({ args: `(${i},)`, expected: 1 })) }, limit,
        (d) => {
          if (d.kind === 'error') { loadErr = d.error; loaded = quietLib(d.stdout); }
          if (d.kind === 'loaded') loaded = quietLib(d.stdout);
          if (d.kind === 'test') {
            const r = rows[d.i]; if (!r) return;
            const out = quietLib(d.stdout), k = out.lastIndexOf(MARK);
            r.actual = k >= 0 ? out.slice(k + MARK.length) : null;
            r.stdout = k >= 0 ? out.slice(0, k) : out;
            if (!r.out) r.stdout = r.stdout.trim();
            r.error = d.error || null;
            r.ok = !!d.ok && !d.error;
          }
        },
        (info) => {
          /* a case that ran past its limit is reported on its own row; the rest did not run */
          if (info.timeout && !info.loading && info.at != null && info.at >= 0 && info.at < rows.length && !loadErr) {
            const k = info.at, secs = Math.round(caseMs(k) / 100) / 10;
            rows[k].error = `Stopped after ${secs} s on this test. Look for a loop that never ends, work that grows too fast for this input, or an input() waiting for a line the test does not give.`;
            rows.forEach((x, i) => { if (i > k) x.error = 'Not run: an earlier test went past its time limit.'; });
            resolve({ rows, printed: loaded, error: null }); return;
          }
          resolve({ rows, printed: loaded, error: loadErr ? cleanTb(loadErr) : info.loading ? 'The packages your code imports took more than two minutes to load. Check the connection and try again.' : info.timeout ? 'Stopped after the time limit. Look for a loop that never ends, or an input() waiting for a line the test does not give.' : info.crash || null });
        },
        (msg) => { if (alive && /^Loading\b/.test(msg)) res.innerHTML = `<p class="t-caption wd-res-load" aria-live="polite">${Z.esc(msg.replace(/\s*$/, ''))}. The first run that imports a package fetches it once.</p>`; },
        caseMs);
      if (!ok) resolve({ rows, printed: '', error: Py.status === 'unavailable' ? 'Python could not load: ' + Py.reason : 'Python is still loading. Try again in a moment.' });
    });
    /* the data files are fetched once (cached by Z.content.dataFiles); a file that cannot be read stops the run with a plain message */
    const runCases = async (cases) => {
      let d = null;
      if (dataMap) { try { d = await loadData(); } catch (e) { return { rows: cases.map(c => ({ tol: tolOf(c), argv: null, call: c.call ?? '', raises: false, setup: '', expect: String(c.expect ?? ''), out: false, stdin: '', ok: false, actual: null, error: null })), printed: '', error: 'The data files for this exercise could not be loaded (' + (e && e.message || e) + '). Check the connection and try again.' }; } }
      return runCases0(cases, d);
    };
    if (hasData) loadData().then((d) => {
      if (!alive) return;
      const b = el.querySelector('.wd-code-data-b'); if (!b) return;
      b.textContent = '';
      Object.entries(d).forEach(([n, t]) => {
        const ls = String(t).split('\n'); if (ls.length && ls[ls.length - 1] === '') ls.pop();
        const first = ls.slice(0, 6).map(x => (x.length > 120 ? x.slice(0, 120) + '…' : x)).join('\n');
        const bytes = new Blob([t]).size;
        const box = Z.h(`<div class="wd-code-data-f"><p class="t-caption"><b></b> <span></span></p><pre class="wd-res-out"></pre></div>`);
        box.querySelector('b').textContent = n;
        box.querySelector('span').textContent = `${ls.length.toLocaleString('en-GB')} line${ls.length === 1 ? '' : 's'}, ${bytes < 1024 ? bytes + ' bytes' : (bytes / 1024).toFixed(1) + ' KB'}. First ${Math.min(6, ls.length)}:`;
        box.querySelector('pre').textContent = first;
        b.append(box);
      });
    }).catch(() => { const b = el.querySelector('.wd-code-data-b'); if (b) b.textContent = 'The data files could not be loaded. Check the connection and reload.'; });
    const runExamples = async () => {
      if (busy || locked || Py.status !== 'ready' || !examples.length) return;
      busy = true; sync();
      const r = await runCases(examples);
      busy = false; if (!alive) return;
      /* Item 110: outside script mode, what the code printed when it loaded is shown above the example rows */
      const printed = !script && r.printed.trim() ? `<div class="t-caption">Your code printed</div>${pre(r.printed.replace(/\n$/, ''))}` : '';
      render('Examples', r.rows, examples, (r.error ? pre(r.error, 'wd-res-err') : '') + printed);
      sync();
    };
    runBtn.addEventListener('click', runExamples);
    if (!examples.length) runBtn.hidden = true;

    return {
      el,
      value: () => ed.value,
      set(v) { quiet = true; ed.set(String(v ?? '')); quiet = false; cache = null; },
      answer: () => spec.solution ?? null,
      ready: () => !busy && ed.value.trim() !== '' && (Py.status === 'ready' || Py.status === 'unavailable'),
      dirty: () => ed.value !== (spec.starter || ''),
      async grade() {
        const src = ed.value;
        if (cache && cache.src === src) return cache.result;
        if (Py.status === 'unavailable') return { ok: false, key: 'unavailable', line: 'Python could not load in this browser, so the tests cannot run.', detail: null };
        busy = true; sync();
        const r = await runCases(tests);
        busy = false; sync();
        const n = r.rows.filter(x => x.ok).length;
        const first = r.rows.findIndex(x => !x.ok);
        const ok = !r.error && n === tests.length && tests.length > 0;
        const result = { ok, key: ok ? null : r.error ? 'error' : `test-${first + 1}`, line: ok ? null : r.error && src.trim() === String(spec.starter || '').trim() ? 'The starter does not run yet on its own: fill in the parts it asks for, then check again.' : r.error ? 'Your code stopped before the tests finished. The error is shown below the editor.' : `${n} of ${tests.length} tests passed. The first failure is test ${first + 1}.`, detail: { passed: n, total: tests.length, rows: r.rows } };
        /* item 156: an untouched starter that errors gets a plain sentence, with the traceback folded away */
        const untouched = r.error && src.trim() === String(spec.starter || '').trim();
        if (alive) render('Tests', r.rows, tests, !r.error ? '' : untouched ? `<p class="t-caption">The starter is not finished yet, so Python stopped. Fill in what it asks for and check again.</p><details class="wd-res-more"><summary class="t-caption">Show the error</summary>${pre(r.error, 'wd-res-err')}</details>` : pre(r.error, 'wd-res-err'));
        cache = { src, result };
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
  });
})();
