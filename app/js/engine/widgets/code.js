/* Code widget (docs/AUTHORING.md 3, design-research 5.3 no. 10). The editor from drill.js (line numbers, Python
   highlighting, Tab inserts 4 spaces, Shift Tab dedents, Esc then Tab leaves). "Run examples" runs the visible
   examples; the player's Check runs the hidden tests. Both go to js/screens/drill-worker.js with the drill's own
   messages ({ type: 'init', indexURL } then { type: 'run', id, code, spec }). Each test is wrapped by a small
   harness appended to the learner's code, so one worker spec covers every compare mode (isclose, equal, fraction):
   the harness returns 1.0 for a pass and prints the actual value after a marker, which the widget reads back.
   grade() returns a Promise; results are cached per source text. Results show per test. Drafts: with ctx.draftKey the
   source is saved with ZQ.state.drills.draft(key, code) as you type and restored when the item opens again. */
(function () {
  'use strict';
  const Z = window.ZQ;
  const PYODIDE = 'https://cdn.jsdelivr.net/pyodide/v0.27.7/full/';
  const TEST_MS = 5000, LOAD_MS = 60000;
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
    const scroll = () => { code.style.transform = `translate(${-ta.scrollLeft}px, ${-ta.scrollTop}px)`; gut.style.transform = `translateY(${-ta.scrollTop}px)`; };
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
        if (m.type === 'event') { let d = null; try { d = JSON.parse(m.data); } catch { return; } run.onEvent(d); }
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
    const exec = (code, spec, limit, onEvent, onEnd) => {
      if (status !== 'ready' || !w) return false;
      run = { id: Date.now() + Math.random(), onEvent, onEnd, crash: null };
      run.timer = setTimeout(() => { end({ timeout: true }); start(true); }, limit);
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

  /* The harness: one function the worker calls per case, returning 1.0 for a pass */
  const harness = (cases) => `

def __zq_case(_i):
    import math as _m
    from fractions import Fraction as _F
    _call, _exp, _cmp = __ZQ_CASES[_i]
    _a = eval(_call, globals())
    print(${JSON.stringify(MARK)} + repr(_a), end='')
    _e = eval(_exp, globals())
    if _cmp == 'fraction':
        return 1.0 if isinstance(_a, _F) and _a == _e else 0.0
    if _cmp == 'isclose':
        try:
            return 1.0 if _m.isclose(float(_a), float(_e), rel_tol=1e-9, abs_tol=1e-12) else 0.0
        except Exception:
            return 1.0 if _a == _e else 0.0
    return 1.0 if _a == _e else 0.0

__ZQ_CASES = ${JSON.stringify(cases.map(c => [c.call, String(c.expect), c.compare || 'equal']))}
`;
  const cleanTb = (tb) => String(tb || '').split('\n').filter((ln, i, all) => !/__zq_case|<string>/.test(ln) && !(/^\s{4}\S/.test(ln) && /__zq_case|<string>/.test(all[i - 1] || ''))).join('\n');

  Z.widgets.register('code', (host, spec, ctx) => {
    const examples = spec.examples || [], tests = spec.tests || [];
    const el = Z.h(`<div class="wd-code">
      <div class="wd-code-head">
        <span class="t-label">${spec.language === 'python' || !spec.language ? 'Python' : Z.esc(spec.language)}</span>
        <span class="wd-py t-caption" aria-live="polite"></span>
        <button type="button" class="btn secondary wd-run" disabled>${Z.icon('play', 'sm')} Run examples</button>
      </div>
      <div class="wd-ed"></div>
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

    const row = (r, label) => `<li class="wd-res-row ${r.ok ? 'ok' : 'bad'}">
        <span class="wd-res-ic" aria-hidden="true">${Z.icon(r.ok ? 'check' : 'cross', 'xs')}</span>
        <div class="wd-res-b"><div class="wd-res-h"><b>${label}</b> <code class="lsn-ic">${Z.esc(r.call)}</code></div>
        ${r.error ? `<pre class="wd-res-err t-code">${Z.esc(cleanTb(r.error))}</pre>` : `<div class="t-caption">Expected <code class="lsn-ic">${Z.esc(r.expect)}</code>, got <code class="lsn-ic">${Z.esc(r.actual ?? 'nothing')}</code></div>`}
        ${r.stdout ? `<pre class="wd-res-out t-code">${Z.esc(r.stdout)}</pre>` : ''}</div></li>`;
    const render = (title, rows, cases, extra = '') => {
      const n = rows.filter(r => r.ok).length;
      res.innerHTML = `<div class="wd-res-top"><span class="t-label">${title}</span><span class="t-caption">${n} of ${cases.length} passed</span></div>${extra}<ol class="wd-res-list">${rows.map((r, i) => row(r, (title === 'Examples' ? 'Example ' : 'Test ') + (i + 1))).join('')}</ol>`;
    };
    /* Run a list of cases; resolves to { rows, error } */
    const runCases = (cases) => new Promise((resolve) => {
      const code = ed.value + harness(cases);
      const rows = cases.map(c => ({ call: c.call, expect: String(c.expect), ok: false, actual: null, error: null, stdout: '' }));
      let loadErr = null;
      const ok = Py.exec(code, { fn: '__zq_case', compare: 'isclose', prelude: '', tests: cases.map((_, i) => ({ args: `(${i},)`, expected: 1 })) }, TEST_MS * Math.max(1, cases.length),
        (d) => {
          if (d.kind === 'error') loadErr = d.error;
          if (d.kind === 'test') {
            const r = rows[d.i]; if (!r) return;
            const out = String(d.stdout || ''), k = out.lastIndexOf(MARK);
            r.actual = k >= 0 ? out.slice(k + MARK.length) : null;
            r.stdout = (k >= 0 ? out.slice(0, k) : out).trim();
            r.error = d.error || null;
            r.ok = !!d.ok && !d.error;
          }
        },
        (info) => resolve({ rows, error: loadErr ? cleanTb(loadErr) : info.timeout ? 'Stopped after the time limit. Look for a loop that never ends.' : info.crash || null }));
      if (!ok) resolve({ rows, error: Py.status === 'unavailable' ? 'Python could not load: ' + Py.reason : 'Python is still loading. Try again in a moment.' });
    });
    const runExamples = async () => {
      if (busy || locked || Py.status !== 'ready' || !examples.length) return;
      busy = true; sync();
      const r = await runCases(examples);
      busy = false; if (!alive) return;
      render('Examples', r.rows, examples, r.error ? `<pre class="wd-res-err t-code">${Z.esc(r.error)}</pre>` : '');
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
        const result = { ok, key: ok ? null : r.error ? 'error' : `test-${first + 1}`, line: ok ? null : r.error ? 'Your code stopped before the tests finished. The error is shown below the editor.' : `${n} of ${tests.length} tests passed. The first failure is test ${first + 1}.`, detail: { passed: n, total: tests.length, rows: r.rows } };
        if (alive) render('Tests', r.rows, tests, r.error ? `<pre class="wd-res-err t-code">${Z.esc(r.error)}</pre>` : '');
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
