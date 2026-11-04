/* Verified code drills: #drill lists them, #drill/<id> opens one. Runs real Python in the browser: Pyodide (from the
   jsDelivr CDN) inside a Web Worker (drill-worker.js), so a run that passes the 5-second limit can be terminated.
   Visible examples on Run, hidden tests on Submit, the first failing test shown with its input and a diff of expected
   against actual. After a pass the model solution opens with a Compare toggle beside your code.

   Problems are content/drills/<id>.json (docs/AUTHORING.md 5), listed by content/drills/index.json and loaded through
   ZQ.content.drills() and ZQ.content.drill(id). Fields used here beyond the required ones (all optional):
     fn          the function the tests call (default: the first `def` in the starter)
     returns     what the function returns, for the wrong-type message ("a list of floats")
     definition  markdown shown in the shaded box under the brief
     constraints [markdown]   hint   markdown, opens after the first run   notes  [markdown] beside the model solution
     where       one line under the brief    prelude  Python run after the learner's code (helpers the tests call)
     examples[]  { call, expect, compare, note }     tests[] { name, call, expect, compare, why, show, note }
   Each run appends a small harness to the learner's code (see harness()): the worker calls __zq_case(i) for each case,
   which evaluates `call`, compares with `expect` (isclose: element by element for lists, within rel 1e-9 or abs 1e-12;
   fraction: a Fraction equal to it; equal: ==) and prints the actual value after a marker.

   Learner state: the draft is kept per drill with ZQ.state.drills.draft(id, code) (400ms debounce; it is in the state
   document, so Export carries it), attempts in ZQ.store 'drill.<id>.state'. A pass records ZQ.state.drills.verified(id, code) and logs the time on the
   drill to the build block with ZQ.state.hours.log({ block: 'build', minutes, source: 'drill:<id>' }); leaving logs the
   rest. Drills earn no XP (docs/PLAN.md 6 lists none).
   Spec: docs/design-research.md 2.10 and 2.11, 3, 4.5, 4.8, 4.9, 5.1, 5.3 #10, 5.4, 5.5, 9.2, 10.
   Every class carries the drl- prefix; sheet content uses drl-sh-. Test hook: window.ZQDrill while a drill is open. */
(function () {
  'use strict';

  const lib = () => ZQ.drillLib || {}; // js/screens/drill-lib.js: patterns, filters, stopwatch, C++ drills, sessions (item 472)
  const LIMIT_MS = 5000;
  const LOAD_LIMIT_MS = 60000;
  const PKG_MS = 120000;
  const MARK = '\u001eZQ';
  const WORDS = ['no', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve'];
  const num = (n) => (n < WORDS.length ? WORDS[n] : String(n));
  const RULES = {
    isclose: { rule: 'math.isclose(actual, expected,\n             rel_tol=1e-9)', accept: 'Accepted: `math.isclose(actual, expected, rel_tol=1e-9)`, element by element for lists.' },
    fraction: { rule: 'isinstance(actual, Fraction)\nand actual == expected', accept: 'Accepted: a `Fraction` exactly equal to the expected value.' },
    equal: { rule: 'actual == expected', accept: 'Accepted: a value equal to the expected one.' },
  };

  /* ---------- The test harness appended to the learner's code ---------- */
  const py = (v) => JSON.stringify(v); // a JSON string is a valid Python string literal
  const harness = (P, defs) => `


# ---- Test harness, added by the drill when it runs. Not part of your code. ----
${P.prelude || ''}
import contextlib as __zq_cl, io as __zq_io, json as __zq_json, math as __zq_m
from fractions import Fraction as __zq_F


def __zq_typed(a, e, mode):
    if mode == 'fraction':
        return isinstance(a, __zq_F)
    if e is None:
        return a is None
    if isinstance(e, (list, tuple)):
        return isinstance(a, (list, tuple))
    if isinstance(e, (int, float)) and not isinstance(e, bool):
        return isinstance(a, (int, float)) and not isinstance(a, bool)
    return type(a) is type(e)


def __zq_eq(a, e, mode):
    if mode == 'fraction':
        return isinstance(a, __zq_F) and a == e
    if mode == 'isclose':
        if e is None:
            return a is None
        if isinstance(e, (list, tuple)):
            return isinstance(a, (list, tuple)) and len(a) == len(e) and all(__zq_eq(x, y, mode) for x, y in zip(a, e))
        if isinstance(a, bool) or not isinstance(a, (int, float)):
            return False
        return __zq_m.isclose(a, e, rel_tol=1e-9, abs_tol=1e-12)
    return a == e


def __zq_case(i):
    call, expect, mode = __ZQ_CASES[i]
    out = __zq_io.StringIO()
    try:
        with __zq_cl.redirect_stdout(out), __zq_cl.redirect_stderr(out):
            actual = eval(call, globals())
    except BaseException:
        print(${py(MARK)} + __zq_json.dumps({'o': out.getvalue()[-2500:]}), end='')
        raise
    expected = eval(expect, globals())
    try:
        text = repr(actual)
    except Exception:
        text = '<repr failed>'
    if len(text) > 400:
        text = text[:400] + ' ...'
    print(${py(MARK)} + __zq_json.dumps({'r': text, 't': type(actual).__name__, 'typed': bool(__zq_typed(actual, expected, mode)),
                                          'o': out.getvalue()[-2500:]}), end='')
    return 1.0 if __zq_eq(actual, expected, mode) else 0.0


__ZQ_CASES = ${py(defs.map(d => [String(d.call), String(d.expect), d.compare || 'isclose']))}
if not callable(globals().get(${py(P.fn)})):
    raise NameError(${py(P.fn + '() is not defined in solution.py')})
`;
  /* Tracebacks keep only the learner's frames: drop the harness's own lines */
  const cleanTb = (tb) => {
    const lines = String(tb || '').split('\n'), out = [];
    for (let i = 0; i < lines.length; i++) {
      if (/^\s*File "solution\.py", line \d+, in __zq_\w+/.test(lines[i])) {
        if (lines[i + 1] && /^\s{4}\S/.test(lines[i + 1]) && !/^\s*File /.test(lines[i + 1])) i++;
        continue;
      }
      out.push(lines[i]);
    }
    const t = out.join('\n');
    return /File "/.test(t) ? t : t.replace(/^Traceback \(most recent call last\):\s*\n/, '');
  };

  /* ---------- A drill file as the screen uses it ---------- */
  const adapt = (d, Z) => {
    const C = Z.content.course(d.course) || {};
    const topic = C.topic ? Z.content.topic(C.topic) : null;
    const fn = d.fn || ((String(d.starter || '').match(/^def\s+([A-Za-z_]\w*)\s*\(/m) || [])[1]) || 'solution';
    const modes = Array.from(new Set((d.tests || []).map(t => t.compare || 'isclose')));
    const main = modes.includes('fraction') ? 'fraction' : modes.includes('isclose') ? 'isclose' : modes[0] || 'isclose';
    return {
      id: d.id, fn, title: d.name, difficulty: d.difficulty || 2, skills: d.skills || [],
      course: C.name || d.course, courseId: d.course, track: C.track || 'code',
      topic: topic ? `${topic.id} ${topic.name}` : (C.topic || ''),
      brief: d.brief || '', definition: d.definition || '', cons: d.constraints || [], hint: d.hint || '',
      how: d.how || '', rule: RULES[main].rule, accept: RULES[main].accept, where: d.where || '',
      language: 'python', pattern: d.pattern || '', pace: d.pace || 0,
      starter: d.starter || '', reference: d.solution || '', notes: d.notes || [], prelude: d.prelude || '', data: d.data && typeof d.data === 'object' ? d.data : null, returns: d.returns || 'a value of the right type',
      examples: (d.examples || []).map((x, i) => ({ ...x, name: x.name || `Example ${i + 1}` })),
      hidden: (d.tests || []).map((x, i) => ({ ...x, name: x.name || `Test ${i + 1}` })),
    };
  };
  const fmtMs = (ms) => (ms == null ? '' : ms < 0.1 ? '<0.1 ms' : ms < 10 ? ms.toFixed(1) + ' ms' : ms < 1000 ? Math.round(ms) + ' ms' : (ms / 1000).toFixed(2) + ' s');

  /* ---------- Python syntax highlighting (keywords, builtins, strings, numbers, comments) ---------- */
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

  /* ---------- Tangram loader (spec 4.8): seven flat pieces morph die -> rising arrow -> bell curve,
     700ms ease-morph with 400ms holds. Geometry shared in spirit with the onboarding loader. ---------- */
  const normalise = (poly) => {
    let a = 0; for (let i = 0; i < poly.length; i++) { const p = poly[i], q = poly[(i + 1) % poly.length]; a += p[0] * q[1] - q[0] * p[1]; }
    const pts = a < 0 ? poly.slice().reverse() : poly.slice();
    let k = 0; pts.forEach((p, i) => { if (p[0] + p[1] < pts[k][0] + pts[k][1] - 0.01) k = i; });
    return pts.slice(k).concat(pts.slice(0, k));
  };
  const DIE = (() => {
    const A = [60, 14], B = [100, 37], C = [100, 83], Dn = [60, 106], E = [20, 83], F = [20, 37], O = [60, 60];
    const P = [73.33, 21.67], Q = [33.33, 44.67], L1 = [20, 60], M = [60, 83];
    const top = (x) => 60 - (x - 60) * 23 / 40, bot = (x) => 106 - (x - 60) * 23 / 40;
    const s1 = [73.33, top(73.33)], s2 = [86.67, top(86.67)], b1 = [73.33, bot(73.33)], b2 = [86.67, bot(86.67)];
    return [[F, O, M, L1], [L1, M, Dn, E], [A, P, Q, F], [P, B, O, Q], [O, s1, b1, Dn], [s1, s2, b2, b1], [s2, B, C, b2]].map(normalise);
  })();
  const ARROW = (() => {
    const seg = (P, Q, h) => { const dx = Q[0] - P[0], dy = Q[1] - P[1], L = Math.hypot(dx, dy), nx = -dy / L * h, ny = dx / L * h;
      return [[P[0] + nx, P[1] + ny], [Q[0] + nx, Q[1] + ny], [Q[0] - nx, Q[1] - ny], [P[0] - nx, P[1] - ny]]; };
    const mid = (P, Q) => [(P[0] + Q[0]) / 2, (P[1] + Q[1]) / 2];
    const A = [14, 98], B = [44, 66], C = [62, 82], Dn = [92, 48], h = 9;
    const ext = (P, Q, e) => { const L = Math.hypot(Q[0] - P[0], Q[1] - P[1]); return [Q[0] + (Q[0] - P[0]) / L * e, Q[1] + (Q[1] - P[1]) / L * e]; };
    const segX = (P, Q, hh) => seg(ext(Q, P, 4), ext(P, Q, 4), hh);
    const L = Math.hypot(Dn[0] - C[0], Dn[1] - C[1]), ux = (Dn[0] - C[0]) / L, uy = (Dn[1] - C[1]) / L;
    const nx = -uy * 21, ny = ux * 21, K = [Dn[0] - ux * 2, Dn[1] - uy * 2], tip = [Dn[0] + ux * 30, Dn[1] + uy * 30];
    return [segX(A, mid(A, B), h), segX(mid(A, B), B, h), segX(B, C, h), segX(C, mid(C, Dn), h), segX(mid(C, Dn), Dn, h),
      [K, [K[0] + nx, K[1] + ny], tip, tip], [K, tip, [K[0] - nx, K[1] - ny], [K[0] - nx, K[1] - ny]]].map(normalise);
  })();
  const BELL = (() => {
    const top = (x) => 102 - 84 * Math.exp(-0.5 * Math.pow((x - 60) / 19.5, 2));
    const x0 = 7, w = 106 / 7;
    return Array.from({ length: 7 }, (_, i) => { const a = x0 + i * w, b = a + w, m = (a + b) / 2;
      return [[a, top(a)], [m, top(m)], [b, top(b)], [b, 102], [a, 102]]; });
  })();
  const withMid = (q) => [q[0], [(q[0][0] + q[1][0]) / 2, (q[0][1] + q[1][1]) / 2], q[1], q[2], q[3]];
  const SHAPES = [DIE.map(withMid), ARROW.map(withMid), BELL];
  const easeMorph = (t) => (t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2); // = cubic-bezier(0.65, 0, 0.35, 1)
  const ptsOf = (poly) => poly.map(p => p[0].toFixed(2) + ',' + p[1].toFixed(2)).join(' ');
  const tangramSVG = () => `<svg class="drl-tg" viewBox="0 0 120 120" aria-hidden="true">${SHAPES[0].map(p => `<polygon points="${ptsOf(p)}"/>`).join('')}</svg>`;

  /* ---------- Editor: textarea over a synchronised highlighted pre, with line numbers ---------- */
  function Editor(host, { value, label, describedBy, onInput, onRun, onSubmit }) {
    host.innerHTML = `<div class="drl-gut" aria-hidden="true"><div class="drl-gut-in"></div></div>
      <div class="drl-ed-main"><pre class="drl-hl" aria-hidden="true"><code></code></pre>
        <textarea class="drl-ta" wrap="off" spellcheck="false" autocapitalize="off" autocomplete="off" autocorrect="off" aria-label="${label}" aria-describedby="${describedBy}"></textarea></div>`;
    const ta = host.querySelector('textarea'), code = host.querySelector('code'), gut = host.querySelector('.drl-gut-in');
    let lines = 0, cur = -1, escArmed = false;
    const lineStartOf = (v, i) => v.lastIndexOf('\n', i - 1) + 1;
    const scroll = () => {
      code.style.transform = `translate(${-ta.scrollLeft}px, ${-ta.scrollTop}px)`;
      gut.style.transform = `translateY(${-ta.scrollTop}px)`;
    };
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
      mark(); scroll();
    };
    /* Replace a range through the browser's editing commands so Ctrl+Z still works; fall back to setRangeText */
    const edit = (start, end, text, selStart, selEnd = selStart) => {
      ta.focus();
      ta.setSelectionRange(start, end);
      let ok = false;
      if (start !== end || text) {
        try { ok = text ? document.execCommand('insertText', false, text) : document.execCommand('delete'); } catch { ok = false; }
        if (!ok) { ta.setRangeText(text, start, end, 'end'); paint(); onInput(ta.value); }
      }
      ta.setSelectionRange(selStart, selEnd);
      mark();
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
      if ((ev.ctrlKey || ev.metaKey) && ev.key === 'Enter') { ev.preventDefault(); (ev.shiftKey ? onSubmit : onRun)(); return; }
      if (ev.key === 'Escape') { escArmed = true; return; }
      if (ev.key === 'Tab' && !ev.ctrlKey && !ev.altKey && !ev.metaKey) {
        if (escArmed) { escArmed = false; return; } // Esc then Tab leaves the editor
        ev.preventDefault(); indent(ev.shiftKey); return;
      }
      if (ev.key !== 'Shift') escArmed = false;
      if (ev.key === 'Enter' && !ev.isComposing && !ev.shiftKey && !ev.altKey) { ev.preventDefault(); newline(); return; }
      if (ev.key === 'Backspace' && ta.selectionStart === ta.selectionEnd) {
        const v = ta.value, s = ta.selectionStart, before = v.slice(lineStartOf(v, s), s);
        if (before.length && /^ +$/.test(before)) { const n = before.length % 4 || 4; ev.preventDefault(); edit(s - n, s, '', s - n); }
      }
    });
    ta.addEventListener('input', () => { paint(); onInput(ta.value); });
    ta.addEventListener('scroll', scroll, { passive: true });
    ['keyup', 'click', 'focus', 'select'].forEach(t => ta.addEventListener(t, mark));
    ta.value = value;
    paint();
    return {
      el: ta,
      get value() { return ta.value; },
      set(v) { ta.value = v; paint(); onInput(v); },         // direct, for the test hook
      replaceAll(v) { edit(0, ta.value.length, v, 0); ta.scrollTop = 0; ta.scrollLeft = 0; scroll(); }, // undoable
    };
  }

  /* ---------- Python runner: owns the worker, the load state and the 5-second limit ---------- */
  function PyRunner(onStatus) {
    let w = null, status = 'idle', version = '', reason = '', loadTimer = 0, run = null, gen = 0;
    const workerURL = new URL('js/screens/drill-worker.js', location.href).href;
    const set = (s) => { status = s; onStatus(s); };
    const kill = () => {
      clearTimeout(loadTimer);
      if (run) { clearTimeout(run.timer); run = null; }
      if (w) { w.onmessage = null; w.onerror = null; w.terminate(); w = null; }
    };
    const unavailable = (msg) => { kill(); reason = msg; set('unavailable'); };
    const end = (info) => { const r = run; if (!r) return; clearTimeout(r.timer); run = null; r.onEnd(info); };
    const start = (restart = false) => {
      kill();
      const my = ++gen;
      set(restart ? 'restarting' : 'loading');
      if (typeof WebAssembly !== 'object' || typeof Worker !== 'function') { unavailable('This browser cannot run WebAssembly in a background worker.'); return; }
      try { w = new Worker(workerURL, { type: 'module' }); } catch (err) { unavailable(String((err && err.message) || err)); return; }
      w.onmessage = (e) => {
        if (my !== gen) return;
        const m = e.data || {};
        if (m.type === 'ready') { clearTimeout(loadTimer); version = m.version; set('ready'); return; }
        if (m.type === 'fail') { unavailable(m.message); return; }
        if (!run || m.id !== run.id) return;
        if (m.type === 'event') { let d = null; try { d = JSON.parse(m.data); } catch { return; } run.onEvent(d); }
        else if (m.type === 'pkgs') { // ENGINE-BACKLOG 500: package loading is kept out of the run's limit (2 minutes of its own), as in the lesson widget
          const r = run;
          clearTimeout(r.timer);
          if (m.phase === 'end') r.timer = setTimeout(() => { end({ timeout: true }); start(true); }, LIMIT_MS);
          else r.timer = setTimeout(() => { end({ timeout: true }); start(true); }, PKG_MS);
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
      w.postMessage({ type: 'init', indexURL: null }); // the worker loads Pyodide from the jsDelivr CDN
      loadTimer = setTimeout(() => { if (my === gen) unavailable('Python took more than a minute to load.'); }, LOAD_LIMIT_MS);
    };
    const exec = (code, spec, onEvent, onEnd) => {
      if (status !== 'ready' || !w) return false;
      run = { id: Date.now() + Math.random(), onEvent, onEnd, crash: null };
      run.timer = setTimeout(() => { end({ timeout: true }); start(true); }, LIMIT_MS);
      set('running');
      w.postMessage({ type: 'run', id: run.id, code, spec });
      return true;
    };
    return { start, exec, kill, get status() { return status; }, get version() { return version; }, get reason() { return reason; } };
  }


  /* Remember where the learner came from, so Close goes back there */
  let cameFrom = null;
  window.addEventListener('hashchange', (e) => {
    try {
      const n = new URL(e.newURL).hash.slice(1), o = new URL(e.oldURL).hash.slice(1);
      if (/^drill\/./.test(n) && o && !/^drill\/./.test(o)) cameFrom = o;
    } catch { /* malformed URL: keep the previous value */ }
  });
  const leaveTarget = () => cameFrom || 'drill';

  /* The draft lives in the state document (ZQ.state.drills.draft), so Export carries it. A draft from before that, in
     ZQ.store 'drill.<id>.code', is still read once and moves across on the next save. */
  const store = (Z) => ({
    code: (id) => { const d = Z.state && Z.state.drills && Z.state.drills.draft ? Z.state.drills.draft(id) : null; return d != null ? d : Z.store.get(`drill.${id}.code`, null); },
    setCode: (id, v) => {
      if (Z.state && Z.state.drills && Z.state.drills.draft) { Z.state.drills.draft(id, v); if (Z.store.get(`drill.${id}.code`, null) != null) Z.store.set(`drill.${id}.code`, null); }
      else Z.store.set(`drill.${id}.code`, v);
    },
    state: (id) => Z.store.get(`drill.${id}.state`, null) || {},
    setState: (id, v) => Z.store.set(`drill.${id}.state`, v),
  });
  const record = (Z, id) => (Z.state && Z.state.drills ? Z.state.drills.get(id) : null);
  const dots = (n) => `<span class="drl-diff-dots" role="img" aria-label="Difficulty ${n} of 5">${[1, 2, 3, 4, 5].map(i => `<i class="${i <= n ? 'on' : ''}"></i>`).join('')}</span>`;

  /* ---------- #drill: every drill, grouped by course ---------- */
  function listView(root, Z, missing) {
    const { esc, icon: I } = Z;
    const St = store(Z);
    const all = Z.content.drills().filter(d => !d.sample); // a sample drill is for the authors, never listed
    const groups = [];
    all.forEach(d => {
      let g = groups.find(x => x.course === d.course);
      if (!g) { const c = Z.content.course(d.course) || {}; g = { course: d.course, name: c.name || d.course, topic: c.topic || '', track: c.track || 'code', items: [] }; groups.push(g); }
      g.items.push(d);
    });
    const verified = all.filter(d => { const r = record(Z, d.id); return r && r.verified; }).length;
    const lb = lib(), F = lb.filters ? lb.filters(Z) : null; // item 472: pattern, difficulty and language filters
    const status = (d) => {
      const r = record(Z, d.id);
      if (r && r.verified) return `<span class="chip correct drl-l-chip">${I('check', 'xs')}Verified${r.best != null ? ' · ' + lb.clock(r.best) : ''}</span>`;
      const draft = St.code(d.id);
      return draft ? '<span class="chip soft drl-l-chip">Draft saved</span>' : '<span class="t-caption drl-l-new">Not started</span>';
    };
    root.innerHTML = `
      <div class="drl-l">
        <header class="drl-top drl-l-top">
          <button type="button" class="icon-btn drl-close" aria-label="Close">${I('close')}</button>
          <div class="drl-ttl"><span class="drl-glyph" aria-hidden="true" data-track="code">${I('terminal', 'sm')}</span><span class="drl-ttl-t"><span class="drl-ttl-a">Code drills</span></span></div>
          <div></div>
        </header>
        <main class="drl-l-main">
          <div class="drl-l-head">
            <p class="t-overline muted">Build</p>
            <h1 class="t-course-title">Code drills</h1>
            <p class="t-body secondary">Write one function and prove it with hidden tests. Python and C++ run in this browser, and your draft is saved as you type. Time spent here counts toward your build hours.</p>
            <p class="t-caption muted tnum">${verified} of ${all.length} verified</p>
          </div>
          ${missing ? `<p class="drl-l-miss t-body" role="status">${I('flag', 'sm')}<span>There is no drill called “${esc(missing)}”. Pick one below.</span></p>` : ''}
          ${F && all.length ? `<div class="drl-l-tools">${lb.filterBarHTML(Z, F, all, 'drl-l')}<a class="btn secondary drl-l-sess" href="#drill/session">${I('timer', 'sm')}Start a 60-minute session</a></div>` : ''}
          <div class="drl-l-groups" aria-live="polite"></div>
        </main>
      </div>`;
    const paintGroups = () => {
      const shown = F ? lb.filterList(all, F) : all;
      const gs = [];
      shown.forEach(d => {
        let g = gs.find(x => x.course === d.course);
        if (!g) { const c = Z.content.course(d.course) || {}; g = { course: d.course, name: c.name || d.course, topic: c.topic || '', track: c.track || 'code', items: [] }; gs.push(g); }
        g.items.push(d);
      });
      root.querySelector('.drl-l-groups').innerHTML = !all.length ? '<p class="t-body secondary">No drills are written yet.</p>'
        : !shown.length ? '<p class="t-body secondary" role="status">No drill matches these filters. Widen the pattern, difficulty or language.</p>'
        : gs.map(g => `<section class="drl-l-g" data-track="${esc(g.track)}" aria-labelledby="drl-l-${esc(g.course)}">
              <h2 class="drl-l-gh" id="drl-l-${esc(g.course)}">${g.topic ? `<span class="drl-l-tag">${esc(g.topic)}</span>` : ''}<span class="t-h2">${esc(g.name)}</span></h2>
              <ul class="drl-l-list">${g.items.map(d => `<li><a class="drl-l-item" href="#drill/${esc(d.id)}">
                <span class="drl-l-ic" aria-hidden="true">${I('terminal', 'sm')}</span>
                <span class="drl-l-t"><span class="t-label">${esc(d.name)}</span>${dots(d.difficulty || 2)}${lb.langName ? `<span class="t-caption muted drl-l-m">${esc(lb.langName(lb.langOf(d)))}${d.pattern ? ' · ' + esc(lb.patternName(d.pattern)) : ''}${d.pace ? ' · ' + esc(lb.paceText(d.pace)) : ''}</span>` : ''}</span>
                ${status(d)}${I('chevronR', 'sm drl-l-chev')}</a></li>`).join('')}</ul>
            </section>`).join('');
    };
    paintGroups();
    const bar = root.querySelector('.drlf');
    if (bar) lb.bindFilters(Z, bar, F, paintGroups);
    root.querySelector('.drl-close').addEventListener('click', () => Z.go(cameFrom && !/^drill/.test(cameFrom) ? cameFrom : 'today'));
    return null;
  }

  /* ---------- #drill/<id> ---------- */
  function mount(root, Z, P, opts = {}) {
    const esc = Z.esc, I = Z.icon;
    const St = store(Z);
    const mac = /Mac|iPhone|iPad/.test(navigator.platform || navigator.userAgent || '');
    const mod = mac ? '⌘' : 'Ctrl';
    const id = P.id;
    const NX = P.examples.length, NH = P.hidden.length;
    const back = leaveTarget();

    const rec0 = record(Z, id);
    const saved = St.code(id);
    const st0 = St.state(id);
    const initial = typeof saved === 'string' && saved.trim() ? saved : rec0 && rec0.code ? rec0.code : P.starter;
    const S = {
      tab: 'brief', failed: st0.failed | 0, revealed: !!st0.revealed, ran: !!st0.ran,
      done: !!(rec0 && rec0.verified), verCode: rec0 && rec0.verified ? rec0.code : null, verified: false, dirtySinceVerify: false, retry: false,
      verdict: null, run: null, announcedReady: false, compare: false,
    };
    S.verified = S.done && S.verCode === initial && !opts.session; // a verified solution reopens on Continue (in a session Submit always grades)
    const persist = () => St.setState(id, { failed: S.failed, revealed: S.revealed, ran: S.ran });

    /* Time on the drill goes to the build block: logged on a pass and when leaving */
    let since = Date.now();
    const logTime = () => {
      const minutes = Math.min(180, (Date.now() - since) / 60000);
      since = Date.now();
      try { if (Z.state && minutes >= 0.05) Z.state.hours.log({ block: 'build', minutes, source: 'drill:' + id }); } catch (e) { console.error(e); }
    };

    /* Engine pass C, item 472: the stopwatch (a session's own clock replaces it) and what a submit records with its reading */
    const sw = opts.session || !lib().Stopwatch ? null : lib().Stopwatch(true);
    const secs = () => (opts.seconds ? opts.seconds() : sw ? sw.seconds() : 0);
    const recordRun = (passed, total, ok) => {
      try { if (Z.state && Z.state.drills.time) Z.state.drills.time(id, { seconds: secs(), passed, total, ok }); } catch (e) { console.error(e); }
      if (opts.onResult) opts.onResult({ passed, total, ok });
    };

    const timers = new Set();
    const later = (fn, ms) => { const t = setTimeout(() => { timers.delete(t); fn(); }, ms); timers.add(t); return t; };
    let alive = true;

    /* Inline copy: `code` and $maths$, with punctuation kept beside a formula */
    const fmt = (s) => String(s).split(/(\$[^$]+\$[.,;:]?|`[^`]+`[.,;:]?)/g).map((p, i) => {
      if (!(i % 2)) return esc(p);
      if (p[0] === '`') {
        const c = p.match(/^`([^`]+)`(.?)$/), html = `<code class="drl-ic">${esc(c[1])}</code>${esc(c[2])}`;
        return c[1].length > 24 ? html : `<span class="drl-nw">${html}</span>`; // long code may wrap
      }
      const m = p.match(/^\$([^$]+)\$(.?)$/);
      return `<span class="drl-nw">${Z.tex(m[1])}${esc(m[2])}</span>`;
    }).join('');
    /* Block copy: paragraphs, $$display$$ maths and inline code */
    const block = (s, cls = 't-prose') => String(s).split(/\n\s*\n/).map(p => p.trim()).filter(Boolean).map(p => {
      const m = p.match(/^\$\$([\s\S]+)\$\$$/);
      return m ? `<div class="drl-disp">${Z.tex(m[1], true)}</div>` : `<p class="${cls}">${fmt(p)}</p>`;
    }).join('');
    const lines = (s) => esc(s).replace(/\n/g, '<br>');
    const callOf = (d) => d.show || d.call;

    const exampleCard = (d, i) => `
      <div class="drl-exc">
        <p class="t-label drl-exc-h">Example ${i + 1}</p>
        <dl class="drl-io">
          <dt class="t-caption">Input</dt><dd><code>${lines(callOf(d))}</code></dd>
          <dt class="t-caption">Output</dt><dd><code>${esc(d.expect)}</code></dd>
        </dl>
        ${d.note ? `<p class="t-body drl-exc-why">${fmt(d.note)}</p>` : ''}
      </div>`;
    const utils = (k) => `<div class="drl-utils drl-utils-${k}">
        <button type="button" class="icon-btn drl-flag" aria-label="Report a problem with this drill">${I('flag', 'sm')}</button>
        <button type="button" class="icon-btn drl-snd" aria-pressed="false" aria-label="Sound">${I('mute', 'sm')}</button>
      </div>`;
    const hintSummary = (locked) => `<span class="drl-hint-i">${I(locked ? 'lock' : 'bulb', 'sm')}</span><span class="drl-hint-l"><span>Hint</span>${locked ? '<span class="t-caption drl-hint-lk">Available after your first run</span>' : ''}</span>${locked ? '' : I('chevronD', 'sm drl-hint-c')}`;
    const L = Z.state ? Z.state.summary() : { todayQualified: false };

    root.innerHTML = `
    <div class="drl${opts.session ? ' drl-in-session' : ''}" data-track="${esc(P.track)}" data-tab="brief">
      <div class="drl-wash" aria-hidden="true"></div>
      <header class="drl-top">
        <button type="button" class="icon-btn drl-close" aria-label="Close the drill. Your code is saved."${opts.session ? ' hidden' : ''}>${I('close')}</button>
        <div class="drl-ttl">
          <span class="drl-glyph" aria-hidden="true">${I('terminal', 'sm')}</span>
          <span class="drl-ttl-t"><span class="drl-ttl-a">${esc(P.title)}</span><span class="t-caption drl-ttl-b">Code drill · ${esc(P.course)}</span></span>
        </div>
        <div class="drl-stats">
          <span class="drlc-sw-host"></span>
          <span class="drl-bolt" role="img" aria-label="${L.todayQualified ? 'Streak extended today' : 'Streak not yet extended today'}">${Z.bolt(L.todayQualified)}</span>
        </div>
      </header>

      <div class="drl-tabbar">
        <div class="drl-tabs" role="tablist" aria-label="Drill">
          <button type="button" role="tab" id="drl-t-brief" aria-controls="drl-p-brief" aria-selected="true" data-tab="brief">Brief</button>
          <button type="button" role="tab" id="drl-t-code" aria-controls="drl-p-code" aria-selected="false" tabindex="-1" data-tab="code">Code</button>
          <button type="button" role="tab" id="drl-t-res" aria-controls="drl-p-res" aria-selected="false" tabindex="-1" data-tab="res">Results<span class="drl-badge" hidden></span></button>
        </div>
        ${utils('sm')}
      </div>

      <main class="drl-frame">
        <section class="drl-brief" id="drl-p-brief">
          ${utils('lg')}
          <div class="drl-brief-sc" tabindex="0" aria-label="Brief, scrollable">
            <div class="drl-brief-in">
              <p class="t-overline drl-ov">Code drill${P.topic ? ' · ' + esc(P.topic) : ''}</p>
              <h1 class="t-lesson-title drl-h">${esc(P.title)}</h1>
              <div class="drl-meta">
                <span class="chip track">${I('terminal', 'xs')}${esc(P.course)}</span>
                <span class="chip soft">Python</span>
                ${P.pattern && lib().patternName ? `<span class="chip soft">${esc(lib().patternName(P.pattern))}</span>` : ''}
                <span class="chip soft">${I('timer', 'xs')}5 s limit</span>
                ${P.pace && lib().paceText ? `<span class="chip soft">${I('clock', 'xs')}${esc(lib().paceText(P.pace))}</span>` : ''}
                <span class="chip soft drl-meta-d">${dots(P.difficulty)}<span>Difficulty ${P.difficulty}</span></span>
                <span class="chip correct drl-meta-v"${S.done ? '' : ' hidden'}>${I('check', 'xs')}Verified</span>
              </div>
              ${block(P.brief)}
              ${P.definition ? `<div class="drl-def">${block(P.definition, 't-body')}</div>` : ''}

              <h2 class="t-h2 drl-sec">Examples</h2>
              <div class="drl-exs">${P.examples.map(exampleCard).join('')}</div>

              ${P.cons.length ? `<h2 class="t-h2 drl-sec">Constraints</h2>
              <ul class="drl-cons t-body">${P.cons.map(c => `<li>${fmt(c)}</li>`).join('')}</ul>` : ''}

              ${P.hint ? `<details class="drl-hint"${S.ran ? '' : ' data-locked'}>
                <summary${S.ran ? '' : ' aria-disabled="true"'}>${hintSummary(!S.ran)}</summary>
                <div class="drl-hint-b t-body">${fmt(P.hint)}</div>
              </details>` : ''}

              <div class="drl-how">
                <span class="drl-how-i" aria-hidden="true">${I('clipboard', 'sm')}</span>
                <div class="drl-how-t">
                  <p class="t-label">How it is checked</p>
                  <p class="t-body">${fmt(P.how)}</p>
                  <pre class="drl-how-c">${esc(P.rule)}</pre>
                </div>
              </div>
              ${P.where ? `<p class="t-caption drl-where">${fmt(P.where)}</p>` : ''}
            </div>
          </div>
        </section>

        <section class="drl-code" id="drl-p-code">
          <div class="drl-ed-head">
            <span class="drl-file">${I('terminal', 'sm')}<span>solution.py</span></span>
            <span class="drl-py t-caption" data-py><i class="drl-dot" aria-hidden="true"></i><span data-py-t>Loading Python</span></span>
            <button type="button" class="link-btn drl-reset">Reset code</button>
          </div>
          <div class="drl-ed"></div>
          <p class="t-caption drl-keys" id="drl-keys"><kbd>Tab</kbd> indents, <kbd>Shift</kbd> <kbd>Tab</kbd> dedents. <kbd>Esc</kbd> then <kbd>Tab</kbd> leaves the editor. <kbd>${mod}</kbd> <kbd>Enter</kbd> runs the examples.</p>
        </section>

        <section class="drl-res" id="drl-p-res" tabindex="0">
          <div class="drl-res-head"><h2 class="t-h2">Results</h2><span class="t-caption drl-res-meta tnum"></span></div>
          <div class="drl-res-body"></div>
        </section>

        <footer class="drl-foot">
          <p class="t-caption drl-foot-note" hidden>Python could not start here, so the tests cannot run. Details are under Results.</p>
          <button type="button" class="link-btn drl-ref" hidden>Show model solution</button>
          <div class="drl-actions">
            <button type="button" class="btn secondary drl-run" aria-label="Run examples" disabled><span class="drl-run-i">${I('play', 'sm')}</span><span class="drl-run-t">Run</span></button>
            <button type="button" class="btn drl-submit" disabled><span>Loading Python…</span></button>
          </div>
        </footer>
      </main>
      <p class="sr-only" aria-live="polite" data-live></p>
    </div>`;

    const $ = (s) => root.querySelector(s);
    const drl = $('.drl'), body = $('.drl-res-body'), meta = $('.drl-res-meta'), live = $('[data-live]');
    const runBtn = $('.drl-run'), subBtn = $('.drl-submit'), refBtn = $('.drl-ref'), resetBtn = $('.drl-reset'), badge = $('.drl-badge');
    const hint = $('.drl-hint'), briefSc = $('.drl-brief-sc');
    const say = (t) => { live.textContent = ''; later(() => { live.textContent = t; }, 30); };

    /* ---------- Tabs (below 1024px). The sections are tab panels only while the tabs show. ---------- */
    const mq = matchMedia('(max-width: 1023px)');
    const narrow = () => mq.matches;
    const tabs = Array.from(root.querySelectorAll('[role="tab"]'));
    const PANELS = [['brief', 'Brief'], ['code', 'Code'], ['res', 'Results']];
    const applyRoles = () => {
      const n = narrow();
      PANELS.forEach(([t, name]) => {
        const el = $('#drl-p-' + t);
        if (n) { el.setAttribute('role', 'tabpanel'); el.setAttribute('aria-labelledby', 'drl-t-' + t); el.removeAttribute('aria-label'); }
        else { el.removeAttribute('role'); el.removeAttribute('aria-labelledby'); el.setAttribute('aria-label', name); }
      });
    };
    const setTab = (t, focus = false) => {
      S.tab = t; drl.dataset.tab = t;
      tabs.forEach(b => { const on = b.dataset.tab === t; b.setAttribute('aria-selected', String(on)); b.tabIndex = on ? 0 : -1; if (on && focus) b.focus(); });
    };
    $('.drl-tabs').addEventListener('click', (e) => { const b = e.target.closest('[role="tab"]'); if (b) setTab(b.dataset.tab); });
    $('.drl-tabs').addEventListener('keydown', (e) => {
      const i = tabs.findIndex(b => b.dataset.tab === S.tab);
      const j = e.key === 'ArrowRight' ? (i + 1) % 3 : e.key === 'ArrowLeft' ? (i + 2) % 3 : e.key === 'Home' ? 0 : e.key === 'End' ? 2 : -1;
      if (j >= 0) { e.preventDefault(); setTab(tabs[j].dataset.tab, true); }
    });
    mq.addEventListener('change', applyRoles);
    applyRoles();

    /* ---------- Editor: the draft is saved 400ms after the last keystroke ---------- */
    let saveT = 0;
    const pristine = () => ed.value === P.starter;
    const ed = Editor($('.drl-ed'), {
      value: initial,
      label: 'Python code editor, solution.py', describedBy: 'drl-keys',
      onInput: (v) => {
        clearTimeout(saveT); saveT = setTimeout(() => St.setCode(id, v), 400);
        if (S.retry) S.retry = false;          // editing after "Not quite right" is the Try again path
        if (S.verdict) setVerdict(null);
        if (S.verified) S.dirtySinceVerify = v !== S.verCode;
        paintButtons();
      },
      onRun: () => go('examples'), onSubmit: () => go('submit'),
    });
    resetBtn.addEventListener('click', () => { if (resetBtn.disabled) return; if (narrow()) setTab('code'); ed.replaceAll(P.starter); });

    /* ---------- Verdict: frame colour and page wash, as in the lesson player. A reveal uses hint indigo (spec 4.5). ---------- */
    const setVerdict = (v) => { S.verdict = v; ['ok', 'no', 'rev'].forEach(k => drl.classList.toggle('is-' + k, v === k)); };

    /* ---------- Hint: opens after the first run (spec 5.5) ---------- */
    const unlockHint = () => {
      if (!S.ran) { S.ran = true; persist(); }
      if (!hint || !hint.hasAttribute('data-locked')) return;
      hint.removeAttribute('data-locked');
      const sm = hint.querySelector('summary'); sm.removeAttribute('aria-disabled'); sm.innerHTML = hintSummary(false);
    };
    if (hint) {
      hint.querySelector('summary').addEventListener('click', (e) => { if (hint.hasAttribute('data-locked')) { e.preventDefault(); say('The hint opens after your first run.'); } });
      hint.addEventListener('toggle', () => { if (hint.hasAttribute('data-locked') && hint.open) hint.open = false; });
    }
    const openHint = () => {
      if (!hint) return;
      unlockHint();
      if (narrow()) setTab('brief');
      hint.open = true;
      later(() => {
        const top = hint.getBoundingClientRect().top - briefSc.getBoundingClientRect().top + briefSc.scrollTop - 16;
        briefSc.scrollTo({ top, behavior: Z.reducedMotion() ? 'auto' : 'smooth' });
        hint.querySelector('summary').focus({ preventScroll: true });
      }, 30);
    };

    /* ---------- Python status: buttons, editor status, results placeholder ---------- */
    let tgRaf = 0, tgT = 0;
    const stopTangram = () => { cancelAnimationFrame(tgRaf); clearTimeout(tgT); tgRaf = 0; tgT = 0; };
    const runTangram = (svg) => {
      stopTangram();
      if (!svg || Z.reducedMotion()) return;
      const polys = Array.from(svg.querySelectorAll('polygon'));
      let k = 0;
      const morph = () => {
        const a = SHAPES[k], b = SHAPES[(k + 1) % 3], t0 = performance.now();
        const step = (now) => {
          if (!alive || !svg.isConnected) return;
          const t = Math.min(1, (now - t0) / 700), e = easeMorph(t);
          polys.forEach((el, i) => el.setAttribute('points', a[i].map((p, j) => { const q = b[i][j]; return (p[0] + (q[0] - p[0]) * e).toFixed(2) + ',' + (p[1] + (q[1] - p[1]) * e).toFixed(2); }).join(' ')));
          if (t < 1) tgRaf = requestAnimationFrame(step); else { k = (k + 1) % 3; tgT = setTimeout(morph, 400); }
        };
        tgRaf = requestAnimationFrame(step);
      };
      tgT = setTimeout(morph, 400);
    };

    const pyr = PyRunner((st) => { paintButtons(); paintPy(); if (!S.run || st === 'unavailable') paintIdle(); });
    const paintPy = () => {
      const el = $('[data-py]'), st = pyr.status;
      el.className = 'drl-py t-caption is-' + st;
      $('[data-py-t]').textContent = st === 'ready' ? `Python ${pyr.version}` : st === 'running' ? `Running on Python ${pyr.version}`
        : st === 'unavailable' ? 'Python unavailable' : st === 'restarting' ? 'Restarting Python' : 'Loading Python';
      $('.drl-foot-note').hidden = st !== 'unavailable';
      if (st === 'ready' && !S.announcedReady) { S.announcedReady = true; say(`Python ${pyr.version} is ready.`); }
    };
    let pressed = null;
    /* Spec 5.4: idle (Submit flat and disabled until the first edit), engaged, evaluating, correct (Continue),
       not yet ([Get help] [Try again]). Run is the secondary button; on mobile it is the 48px round left slot. */
    const paintButtons = () => {
      const st = pyr.status, ready = st === 'ready';
      const cont = S.verified && !S.dirtySinceVerify;
      const help = S.retry && !cont && !!hint;
      runBtn.classList.toggle('is-help', help);
      runBtn.querySelector('.drl-run-i').innerHTML = I(help ? 'bulb' : 'play', 'sm');
      runBtn.querySelector('.drl-run-t').textContent = help ? 'Get help' : 'Run';
      runBtn.setAttribute('aria-label', help ? 'Get help: open the hint' : 'Run examples');
      runBtn.disabled = help ? false : !ready;
      runBtn.setAttribute('aria-busy', String(st === 'running' && pressed === 'examples'));
      const label = cont ? 'Continue' : S.retry ? 'Try again'
        : st === 'loading' ? 'Loading Python…' : st === 'restarting' ? 'Restarting Python…' : st === 'unavailable' ? 'Python unavailable'
        : st === 'running' && pressed === 'submit' ? 'Running tests…' : 'Submit';
      subBtn.querySelector('span').textContent = label;
      subBtn.classList.toggle('correct', cont && !S.revealed);
      subBtn.classList.toggle('notyet', !cont && S.retry);
      subBtn.disabled = cont || S.retry ? false : !ready || pristine();
      refBtn.hidden = cont || S.done || !(S.revealed || S.failed >= 2);
      refBtn.textContent = S.revealed ? 'Model solution' : 'Show model solution';
      resetBtn.disabled = pristine();
    };

    /* ---------- Model solution with a Compare toggle (after a pass) ---------- */
    const codeBox = (label, src) => `<div class="drl-cmp-col"><p class="t-caption drl-cmp-l">${label}</p><pre class="drl-sh-code drl-cmp-code" tabindex="0" aria-label="${label}"><code>${highlight(String(src).trimEnd())}</code></pre></div>`;
    const modelHTML = () => `<div class="drl-model">
        <div class="drl-model-h"><p class="t-label">Model solution</p>
          <button type="button" class="drl-cmp-btn" aria-pressed="${S.compare}">${I('grid', 'xs')}<span>Compare</span></button></div>
        <div class="drl-cmp${S.compare ? ' is-on' : ''}">${S.compare ? codeBox('Your code', S.verCode || ed.value) : ''}${codeBox('Model solution', P.reference)}</div>
        ${P.notes.length ? `<ul class="drl-sh-pts t-body">${P.notes.map(t => `<li>${fmt(t)}</li>`).join('')}</ul>` : ''}
      </div>`;
    const paintModel = () => { const m = body.querySelector('.drl-model'); if (m) m.outerHTML = modelHTML(); };
    body.addEventListener('click', (e) => { if (e.target.closest('.drl-cmp-btn')) { S.compare = !S.compare; paintModel(); const b = body.querySelector('.drl-cmp-btn'); b && b.focus(); } });

    const paintIdle = () => {
      const st = pyr.status;
      meta.textContent = '';
      if (st === 'unavailable') {
        stopTangram();
        body.innerHTML = `<div class="drl-notice" role="alert">
          <span class="drl-notice-i" aria-hidden="true">${I('terminal')}</span>
          <div class="drl-notice-t">
            <p class="t-h2">Python could not start here</p>
            <p class="t-body">This drill loads Python from the jsDelivr CDN and runs it in a background worker. The download or the worker was blocked. You can still read the brief and write your solution.</p>
            <p class="t-caption drl-reason">Reason: ${esc(pyr.reason || 'unknown')}</p>
            <button type="button" class="btn secondary drl-retry">${I('replay', 'sm')}<span>Try again</span></button>
          </div></div>`;
        body.querySelector('.drl-retry').addEventListener('click', () => pyr.start());
        badge.hidden = false; badge.className = 'drl-badge is-no'; badge.innerHTML = I('cross', 'xs');
        return;
      }
      if (S.run) return;
      const loading = st === 'loading' || st === 'restarting';
      const wasLoading = !!body.querySelector('.drl-load');
      if (loading && wasLoading) return; // keep the loader running across status repaints
      stopTangram();
      body.innerHTML = `<div class="drl-empty">
        ${loading ? `<div class="drl-load">${tangramSVG()}<div class="drl-load-t"><p class="t-label">${st === 'restarting' ? 'Restarting Python…' : 'Loading Python…'}</p><p class="t-caption">The first load takes a few seconds. Python runs on this device, not on a server.</p></div></div>` : ''}
        <span class="drl-empty-i${S.verified ? ' is-ok' : ''}" aria-hidden="true">${I(S.verified ? 'check' : 'terminal')}</span>
        ${S.verified
          ? `<p class="t-body">You verified this code on an earlier visit.</p><p class="t-caption">Change it and Submit runs the ${num(NH)} hidden tests again.</p>`
          : `<p class="t-body">Nothing has run yet.</p><p class="t-caption">Run checks the ${num(NX)} examples in the brief. Submit runs the ${num(NH)} hidden tests.</p>`}
      </div>${S.done ? modelHTML() : ''}`;
      if (loading) runTangram(body.querySelector('.drl-tg'));
    };

    /* ---------- Results ---------- */
    const ST = { pending: ['', 'Waiting'], running: ['', 'Running'], pass: ['check', 'Passed'], fail: ['cross', 'Failed'], error: ['cross', 'Error'], timeout: ['clock', 'Timed out'], skip: ['minus', 'Not run'] };
    const rowHTML = (R, i) => {
      const d = R.defs[i], r = R.res[i], [ic, label] = ST[r.status];
      const t = (r.status === 'pass' || r.status === 'fail' || r.status === 'error') ? fmtMs(r.ms) : '';
      const sub = R.mode === 'examples' ? `<span class="drl-call">${esc(callOf(d))}</span>` : '';
      return `<li class="drl-row is-${r.status}" data-i="${i}">
        <div class="drl-row-l">
          <span class="drl-st" aria-hidden="true">${ic ? I(ic) : ''}</span>
          <span class="drl-nm"><span class="drl-n tnum">${i + 1}</span><span class="drl-nm-t"><span>${esc(d.name)}</span>${sub}</span></span>
          <span class="drl-stx">${label}${t ? `<span class="drl-ms tnum">${t}</span>` : ''}</span>
        </div></li>`;
    };
    const setRow = (i) => {
      const li = body.querySelector(`.drl-row[data-i="${i}"]`);
      if (li) li.outerHTML = rowHTML(S.run, i);
    };

    const dataPrelude = (Q) => (Q.dataText && Object.keys(Q.dataText).length ? `import sys as _zfs\nif '' not in _zfs.path: _zfs.path.insert(0, '')\nfor _zn, _zt in __import__('json').loads(${py(JSON.stringify(Q.dataText))}).items():\n    open(_zn, 'w').write(_zt)\n` : '');
    const go = (mode) => {
      if (P.data && !P.dataText) {
        if (P.dataFailed) { say('The data files could not be loaded. Reload the page and try again.'); return; }
        Z.content.dataFiles(P.data).then((d) => { P.dataText = d; go(mode); }, () => { P.dataFailed = true; say('The data files could not be loaded. Check the connection and try again.'); });
        return;
      }
      if (mode === 'submit' && S.verified && !S.dirtySinceVerify) { leave(); return; }
      if (pyr.status !== 'ready') { if (pyr.status !== 'running') say(pyr.status === 'unavailable' ? 'Python is unavailable in this browser.' : 'Python is still loading.'); return; }
      if (mode === 'submit' && pristine()) { say('Change the starter code before you submit.'); return; }
      const defs = mode === 'examples' ? P.examples : P.hidden;
      const R = S.run = { mode, defs, code: ed.value, res: defs.map(() => ({ status: 'pending' })), loaded: false, loadOut: '', loadErr: null, ms: null, timeout: false, crash: null };
      pressed = mode;
      S.retry = false;
      unlockHint();
      setVerdict(null);
      drl.classList.add('has-run');
      if (narrow()) setTab('res');
      const n = defs.length;
      meta.textContent = mode === 'examples' ? `${n} examples` : `${n} hidden tests`;
      stopTangram();
      body.innerHTML = `<div class="drl-sum"><p class="t-body drl-sum-run">${mode === 'examples' ? `Running the ${num(n)} examples…` : `Running ${num(n)} hidden tests…`}</p></div>
        <ol class="drl-rows" aria-label="${mode === 'examples' ? 'Examples' : 'Hidden tests'}">${defs.map((_, i) => rowHTML(R, i)).join('')}</ol>
        <div class="drl-out" hidden></div>`;
      body.scrollTop = 0;
      badge.hidden = false; badge.className = 'drl-badge is-run'; badge.textContent = '…';
      say(mode === 'examples' ? 'Running the examples.' : `Running ${n} hidden tests.`);
      /* ENGINE-BACKLOG 469 (E14): the drill's data files are written into the working directory before the learner's code loads (spec.prelude runs first) */
      const spec = { fn: '__zq_case', compare: 'isclose', prelude: dataPrelude(P), tests: defs.map((_, i) => ({ args: `(${i},)`, expected: 1 })) };
      const ok = pyr.exec(R.code + harness(P, defs), spec, (d) => onEvent(R, d), (info) => onEnd(R, info));
      if (!ok) { S.run = null; paintIdle(); }
      paintButtons();
    };

    /* The harness prints the actual value after a marker; the rest of the output is the learner's own */
    const readCase = (stdout) => {
      const out = String(stdout || ''), k = out.lastIndexOf(MARK);
      if (k < 0) return { o: out };
      try { return JSON.parse(out.slice(k + MARK.length)); } catch { return { o: out.slice(0, k) }; }
    };
    const onEvent = (R, d) => {
      if (R !== S.run) return;
      if (d.kind === 'loaded') { R.loaded = true; R.loadOut = d.stdout || ''; if (R.res[0]) { R.res[0].status = 'running'; setRow(0); } }
      else if (d.kind === 'error') R.loadErr = { ...d, missing: /is not defined in solution\.py/.test(d.error || '') };
      else if (d.kind === 'test') {
        const info = readCase(d.stdout);
        R.res[d.i] = { status: d.ok && !d.error ? 'pass' : d.error ? 'error' : 'fail', actual: info.r, error: d.error ? cleanTb(d.error) : null, stdout: info.o || '', ms: d.ms, typed: info.typed !== false, type: info.t };
        setRow(d.i);
        if (d.i + 1 < R.defs.length) { R.res[d.i + 1].status = 'running'; setRow(d.i + 1); }
      } else if (d.kind === 'done') R.ms = d.ms;
    };

    /* Why the first failing test failed: mechanical causes first, then the test's own note */
    const whyFor = (R, d, r) => {
      if (r.status === 'timeout') return d.show || /_walk\(/.test(d.call) ? d.why : 'Your code was still running when the limit hit, so Python was restarted. Look for a loop that never ends.';
      if (r.status === 'error' && R.crash) return 'Python stopped while running this test, often from memory use. Python has been restarted.';
      if (r.status === 'fail' && !r.typed) return r.type === 'NoneType' ? `Your function returned \`None\`. Check that every path reaches \`return\`, and that it returns ${P.returns}.` : `Your function returned a \`${r.type}\`. It should return ${P.returns}.`;
      const note = d.why || d.note || '';
      if (r.status === 'error' && !note) return 'Your function raised an error on this input. The traceback shows the line.';
      return note;
    };

    const onEnd = (R, { timeout, crash }) => {
      if (R !== S.run) return;
      R.timeout = !!timeout; R.crash = crash || null;
      const n = R.defs.length;
      const changed = [];
      if (R.loadErr) R.res.forEach((r, i) => { r.status = 'skip'; changed.push(i); });
      else if (timeout || crash) {
        const k = R.res.findIndex(r => r.status === 'running' || r.status === 'pending');
        R.res.forEach((r, i) => { if (r.status === 'running' || r.status === 'pending') { r.status = i === k && R.loaded ? (timeout ? 'timeout' : 'error') : 'skip'; changed.push(i); } });
      }
      const passed = R.res.filter(r => r.status === 'pass').length;
      const first = R.res.findIndex(r => r.status !== 'pass');
      const all = passed === n;
      const msTxt = R.ms != null ? fmtMs(R.ms) : timeout ? 'stopped at 5 s' : '';
      meta.textContent = `${n} ${R.mode === 'examples' ? 'examples' : 'tests'}${msTxt ? ' · ' + msTxt : ''}`;
      changed.forEach(setRow); // rows that already showed their result keep it, so their badges do not pop twice
      const accepted = `<p class="t-caption drl-acc">${fmt(P.accept)}</p>`;

      /* Summary */
      const sum = body.querySelector('.drl-sum');
      if (R.mode === 'submit' && all) {
        const repeat = S.done, rev = S.revealed;
        S.verified = true; S.done = true; S.verCode = R.code; S.dirtySinceVerify = ed.value !== R.code;
        try { if (Z.state) Z.state.drills.verified(id, R.code); } catch (e) { console.error(e); }
        recordRun(n, n, true);
        if (pill) pill.paint();
        logTime();
        St.setCode(id, R.code);
        $('.drl-meta-v').hidden = false;
        const msIn = R.ms != null ? ' in ' + fmtMs(R.ms) : '';
        const tm = lib().spoken ? ` Stopwatch: ${lib().spoken(secs())}${P.pace ? (secs() <= P.pace ? ', inside the pace of ' : ', the pace is ') + lib().spoken(P.pace) : ''}.` : '';
        const note = (repeat ? 'Verified again.' : rev ? 'Verified. You opened the model solution first, so compare it with your own before you move on.' : 'Added to your drill record on You.') + tm;
        sum.innerHTML = `<div class="${rev ? 'drl-match' : 'drl-ver'}">
            <div class="drl-ver-top"><span class="chip ${rev ? 'drl-match-chip' : 'correct drl-ver-chip'}">${I(rev ? 'bulb' : 'check', 'xs')}Verified</span></div>
            <p class="t-h2 drl-ver-h">All ${n} tests passed${msIn}.</p>
            <p class="t-body drl-ver-n">${esc(note)}</p>
            ${accepted}
          </div>`;
        sum.insertAdjacentHTML('afterend', modelHTML());
        setVerdict(rev ? 'rev' : 'ok');
        if (!rev) { Z.sound('correct'); Z.haptic(); later(() => Z.burst(sum.querySelector('.drl-ver-chip')), 120); }
        say(`Verified. All ${n} tests passed.`);
        Z.emit('drill:verified', { id, revealed: rev });
      } else if (R.mode === 'submit') {
        if (R.loaded && !R.loadErr) { S.failed += 1; recordRun(passed, n, false); } // code that never ran is not an attempt
        S.retry = true;
        persist();
        const head = R.loadErr ? 'Your code did not run' : timeout ? 'Stopped at 5 seconds' : crash ? 'Python stopped' : 'Not quite right';
        const line = R.loadErr ? (R.loadErr.missing ? `Keep the function name ${fmt('`' + P.fn + '`')} so the tests can call it.` : 'Python could not run solution.py. The traceback below points at the line.')
          : !R.loaded ? 'Your code never finished loading, so no test ran.'
          : `${passed} of ${n} tests passed. The first failure is test ${first + 1}, ${esc(R.defs[first].name.toLowerCase())}.`;
        sum.innerHTML = `<div class="drl-fail"><span class="chip notyet">${I(timeout ? 'clock' : 'cross', 'xs')}${head}</span><p class="t-body">${line}</p>${R.loaded && !R.loadErr ? accepted : ''}</div>`;
        setVerdict('no');
        Z.sound('notyet');
        say(`${head}. ${passed} of ${n} tests passed.`);
      } else {
        const head = R.loadErr ? 'Your code did not run' : timeout ? 'Stopped at 5 seconds' : `${passed} of ${n} examples passed`;
        const line = R.loadErr ? (R.loadErr.missing ? `Keep the function name ${fmt('`' + P.fn + '`')} so the examples can call it.` : 'Python could not run solution.py. The traceback below points at the line.') : !R.loaded ? 'Your code never finished loading, so no example ran.'
          : all ? `${n === 2 ? 'Both examples match' : 'Every example matches'}. Submit runs the ${num(NH)} hidden tests.` : 'Compare your output with the expected value below.';
        const chip = all ? ['correct', 'check'] : timeout ? ['notyet', 'clock'] : ['notyet', 'cross'];
        sum.innerHTML = `<div class="drl-exsum"><span class="chip ${chip[0]}">${I(chip[1], 'xs')}${head}</span><p class="t-body">${line}</p></div>`;
        say(`${head}.`);
      }

      /* First failing test: input, expected against actual, a likely cause, its output */
      let diffLi = null;
      if (first >= 0 && !R.loadErr) {
        const d = R.defs[first], r = R.res[first];
        const why = whyFor(R, d, r);
        const actual = r.status === 'timeout' ? 'still running after 5 s' : r.status === 'error' ? (R.crash ? 'Python stopped' : 'raised ' + ((r.error || '').trim().split('\n').pop().split(':')[0] || 'an error')) : (r.actual == null ? 'no value' : r.actual);
        const li = body.querySelector(`.drl-row[data-i="${first}"]`);
        if (li && r.status !== 'skip') {
          li.classList.add('is-first');
          li.insertAdjacentHTML('beforeend', `<div class="drl-diff">
            <p class="t-overline drl-diff-h">${R.mode === 'examples' ? 'First failing example' : 'First failing test'}</p>
            <dl class="drl-kv">
              <dt>Input</dt><dd><code>${lines(callOf(d))}</code>${d.note && R.mode !== 'examples' ? `<span class="t-caption drl-kv-n">${esc(d.note)}</span>` : ''}</dd>
              <dt>Expected</dt><dd class="drl-exp"><code>${esc(d.expect)}</code></dd>
              <dt>Actual</dt><dd class="drl-act"><code>${esc(actual)}</code></dd>
            </dl>
            ${why ? `<p class="t-body drl-why"><span class="drl-why-i" aria-hidden="true">${I('bulb', 'xs')}</span><span>${fmt(why)}</span></p>` : ''}
            ${r.error && !R.crash ? `<pre class="drl-pre is-err">${esc(r.error)}</pre>` : ''}
            ${R.crash && r.status === 'error' ? `<pre class="drl-pre is-err">${esc(R.crash)}</pre>` : ''}
            ${r.stdout ? `<p class="t-caption drl-out-h">Your output</p><pre class="drl-pre">${esc(r.stdout)}</pre>` : ''}
          </div>`);
          diffLi = li;
        }
      }

      /* Output: a transcript for examples; script output and load errors for both */
      const out = body.querySelector('.drl-out');
      const parts = [];
      if (R.loadErr) parts.push(`<pre class="drl-pre is-err">${esc(R.loadErr.missing ? `NameError: solution.py does not define ${P.fn}()` : cleanTb(R.loadErr.error))}</pre>`);
      if (R.loadErr && R.loadErr.stdout) parts.push(`<p class="t-caption drl-out-h">Output before the error</p><pre class="drl-pre">${esc(R.loadErr.stdout)}</pre>`);
      if (R.loadOut) parts.push(`<p class="t-caption drl-out-h">Output from solution.py</p><pre class="drl-pre">${esc(R.loadOut)}</pre>`);
      if (R.mode === 'examples' && !R.loadErr) {
        const tx = R.defs.map((d, i) => {
          const r = R.res[i];
          if (r.status === 'skip') return '';
          const call = `<span class="drl-pr">&gt;&gt;&gt;</span> ${esc(callOf(d))}\n`;
          const so = r.stdout ? esc(r.stdout.endsWith('\n') ? r.stdout : r.stdout + '\n') : '';
          const res = r.status === 'error' ? `<span class="drl-err">${esc(r.error || '')}</span>\n` : r.status === 'timeout' ? '<span class="drl-err">Stopped: still running after 5 s</span>\n' : `${esc(r.actual == null ? '' : r.actual)}\n`;
          return call + so + res;
        }).join('');
        if (tx) parts.push(`<pre class="drl-pre drl-tx">${tx.trimEnd()}</pre>`);
      }
      if (timeout && !R.loaded) parts.push('<p class="t-body drl-why"><span class="drl-why-i" aria-hidden="true">' + I('bulb', 'xs') + '</span><span>Your code was still running at the top level after 5 seconds, so Python was restarted. Look for a loop outside the function that never ends.</span></p>');
      if (parts.length) {
        out.hidden = false;
        out.innerHTML = `<p class="t-overline drl-out-t">${R.loadErr ? 'Traceback' : !R.loaded || R.mode !== 'examples' ? 'Details' : 'Output'}</p>${parts.join('')}`;
        if (R.loadErr || !R.loaded) body.insertBefore(out, body.querySelector('.drl-rows')); // the reason comes before the rows that did not run
      }

      /* Bring the diagnosis into view inside Results: the failing row and its diff, or as much of it as fits */
      if (diffLi && body.clientHeight) {
        const top = diffLi.offsetTop - 8, bottom = diffLi.offsetTop + diffLi.offsetHeight + 16;
        const target = Math.min(top, bottom - body.clientHeight);
        if (target > body.scrollTop) body.scrollTo({ top: target, behavior: Z.reducedMotion() ? 'auto' : 'smooth' });
      }

      /* Badge on the Results tab */
      badge.hidden = false;
      badge.className = 'drl-badge ' + (all ? 'is-ok' : 'is-no');
      badge.innerHTML = all && R.mode === 'submit' ? I('check', 'xs') : `${passed}/${n}`;
      pressed = null;
      paintButtons();
    };

    /* ---------- Not yet: [Get help] [Try again] ---------- */
    const tryAgain = () => {
      S.retry = false; setVerdict(null); paintButtons();
      if (narrow()) setTab('code');
      ed.el.focus();
    };

    /* ---------- Model solution before a pass: offered after 2 failed submissions ---------- */
    const showReference = () => {
      const box = Z.h('<div class="drl-sh"></div>');
      let close = () => {};
      const showCode = () => {
        box.innerHTML = `<h2 class="t-sheet-title drl-sh-t">Model solution</h2>
          <pre class="drl-sh-code" tabindex="0" aria-label="Model solution code"><code>${highlight(P.reference.trimEnd())}</code></pre>
          ${P.notes.length ? `<ul class="drl-sh-pts t-body">${P.notes.map(t => `<li>${fmt(t)}</li>`).join('')}</ul>` : ''}
          <div class="drl-sh-act"><button type="button" class="btn secondary" data-copy>Copy into editor</button><button type="button" class="btn" data-close>Done</button></div>`;
        box.querySelector('[data-copy]').addEventListener('click', () => {
          close();
          if (narrow()) setTab('code');
          ed.replaceAll(P.reference);
        });
      };
      if (S.revealed) { showCode(); close = Z.sheet(box, { label: 'Model solution' }); return; }
      box.innerHTML = `<h2 class="t-sheet-title drl-sh-t">Show the model solution?</h2>
        <p class="t-body drl-sh-p">You will see a full answer. The drill still counts once your own code passes, but you learn more from one more try with the hint.</p>
        <div class="drl-sh-act"><button type="button" class="btn secondary" data-close autofocus>Keep trying</button><button type="button" class="btn" data-reveal>Show solution</button></div>`;
      box.querySelector('[data-reveal]').addEventListener('click', () => {
        S.revealed = true; persist(); paintButtons();
        showCode();
        box.querySelector('[data-close]').focus();
      });
      close = Z.sheet(box, { label: 'Model solution' });
    };
    refBtn.addEventListener('click', showReference);

    /* ---------- Card utilities: report and sound (spec 5.1, 4.9) ---------- */
    const openReport = () => {
      const kinds = ['A test looks wrong', 'The brief is unclear', 'The editor misbehaves', 'Something else'];
      const box = Z.h(`<div class="drl-sh"><h2 class="t-sheet-title drl-sh-t">Report this drill</h2>
        <p class="t-body drl-sh-p">Note what went wrong. The note is saved with this drill and your code, and it goes out with your data export.</p>
        <div class="opts drl-sh-opts" role="radiogroup" aria-label="What went wrong">${kinds.map((k, i) => `<button type="button" class="opt" role="radio" aria-checked="false" data-i="${i}">${k}</button>`).join('')}</div>
        <div class="drl-sh-act"><button type="button" class="btn" data-send disabled>Save note</button></div></div>`);
      Z.sheet(box, { label: 'Report this drill' });
      let pick = -1;
      box.addEventListener('click', (e) => {
        const o = e.target.closest('.drl-sh-opts .opt');
        if (o) { pick = +o.dataset.i; box.querySelectorAll('.drl-sh-opts .opt').forEach(b => { const on = b === o; b.classList.toggle('selected', on); b.setAttribute('aria-checked', String(on)); }); box.querySelector('[data-send]').disabled = false; }
        if (e.target.closest('[data-send]')) {
          const list = Z.store.get('reports', []); list.push({ drill: id, kind: kinds[pick], code: ed.value, at: Date.now() }); Z.store.set('reports', list.slice(-200));
          box.innerHTML = `<h2 class="t-sheet-title drl-sh-t">Note saved</h2><p class="t-body drl-sh-p">It is kept with this drill, so the test or the brief can be fixed when the content is next edited.</p><div class="drl-sh-act"><button type="button" class="btn" data-close>Back to the drill</button></div>`;
          box.querySelector('[data-close]').focus();
        }
      });
    };
    const syncSound = () => { const on = !!Z.settings.sound; root.querySelectorAll('.drl-snd').forEach(b => { b.setAttribute('aria-pressed', String(on)); b.innerHTML = I(on ? 'sound' : 'mute', 'sm'); }); };
    root.addEventListener('click', (e) => {
      if (e.target.closest('.drl-flag')) openReport();
      else if (e.target.closest('.drl-snd')) { Z.setSetting('sound', !Z.settings.sound); Z.sound('tap'); }
    });
    const offSettings = Z.on('settings', () => { if (alive) syncSound(); });
    syncSound();

    /* ---------- Leaving ---------- */
    const leave = () => { St.setCode(id, ed.value); if (opts.onClose) opts.onClose(); else Z.go(back); };
    $('.drl-close').addEventListener('click', leave);
    runBtn.addEventListener('click', () => { if (runBtn.classList.contains('is-help')) openHint(); else go('examples'); });
    subBtn.addEventListener('click', () => {
      if (S.verified && !S.dirtySinceVerify) leave();
      else if (S.retry) tryAgain();
      else go('submit');
    });
    drl.addEventListener('keydown', (e) => {
      if ((e.ctrlKey || e.metaKey) && e.key === 'Enter' && e.target !== ed.el) { e.preventDefault(); go(e.shiftKey ? 'submit' : 'examples'); }
    });

    const hook = window.ZQDrill = {
      setCode: (s) => ed.set(String(s)), code: () => ed.value, run: () => go('examples'), submit: () => go('submit'),
      status: () => pyr.status, tab: (t) => setTab(t), reference: () => P.reference, problem: () => id,
      language: 'python', seconds: () => secs(), pace: () => P.pace || null,
      verified: () => S.verified, results: () => (S.run ? { mode: S.run.mode, res: S.run.res.map(r => ({ status: r.status, actual: r.actual })) } : null),
      compare: (on = true) => { S.compare = !!on; paintModel(); },
    };

    paintButtons(); paintPy(); paintIdle();
    const pill = sw ? lib().stopwatchPill(Z, sw, P.pace) : null;
    if (pill) $('.drlc-sw-host').append(pill.el);
    pyr.start();

    return () => {
      alive = false;
      clearTimeout(saveT); St.setCode(id, ed.value);
      logTime();
      timers.forEach(clearTimeout); timers.clear();
      stopTangram();
      mq.removeEventListener('change', applyRoles);
      if (typeof offSettings === 'function') offSettings();
      pyr.kill();
      if (pill) pill.destroy();
      if (window.ZQDrill === hook) delete window.ZQDrill; // a late cleanup must not remove a newer drill's hook
    };
  }

  /* A drill file in a host element (the session screen): Python here, C++ through drill-lib.js */
  ZQ.drillMount = (host, Z, d, opts) => mount(host, Z, adapt(d, Z), opts || {});

  ZQ.screen({
    id: 'drill', title: 'Code drills', group: 'Build', shell: false,
    render(root, Z, params) {
      const id = params && params[0];
      if (!id) return listView(root, Z, null);
      if (id === 'session' && lib().session) return lib().session(root, Z, params.slice(1)); // item 472: two drills, one clock
      let inner = null, dead = false;
      root.innerHTML = `<div class="drl-l"><main class="drl-l-main"><p class="t-body secondary drl-l-wait">Loading the drill…</p></main></div>`;
      Promise.resolve(Z.content.drill(id)).then((d) => {
        if (dead) return;
        if (!d) { listView(root, Z, id); return; }
        inner = d.language === 'cpp' && lib().mountCpp ? lib().mountCpp(root, Z, d, { back: leaveTarget() }) : mount(root, Z, adapt(d, Z));
        Z.mathify(root);
      }).catch((e) => { console.error(e); if (!dead) listView(root, Z, id); });
      return () => { dead = true; if (inner) inner(); };
    },
  });
})();
