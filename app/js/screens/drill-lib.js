/* Drill library (engine pass C, ENGINE-BACKLOG 472, with C-drill-patterns): what #drill adds to the Python drill screen
   in drill.js. Loaded after it. Everything is exposed as ZQ.drillLib; drill.js calls it.

     C++ drills      a drill file with language: "cpp" opens here (mountCpp): the brief, the C++ code widget of cpp-grade.js
                     (Run examples, compile, hidden tests through widget.grade()), Submit, the model solution after a pass.
     Stopwatch       every drill (Python or C++) shows a count-up clock; a submit records its reading (and the pace) with the
                     result in ZQ.state.drills.time(id, ...). Marks never depend on it.
     Pattern filters PATTERNS is the one list of pattern slugs; tools/validate.mjs reads it from this file, so a drill's
                     `pattern` is checked against it. filterBar() draws the pattern, difficulty and language filters.
     Sessions        #drill/session: two drills, one 60-minute countdown (session()). A result screen gives minutes per drill
                     and hidden tests passed; ZQ.state.drills.session() keeps it and a lesson reads it as {{carry.session.*}}.

   Test hooks while a session is open: window.ZQSession. While a C++ drill is open: window.ZQDrill (as the Python one).
   Classes carry the drlc- (C++ drill page), drls- (session) and drlf- (filters) prefixes; css/screens/drill-lib.css. */
(function () {
  'use strict';
  const ZQ = window.ZQ;

  /* The pattern vocabulary (docs/AUTHORING.md section 5). Keep this a plain JSON array: tools/validate.mjs parses it. */
  const PATTERNS = [
    ["hashing", "Hashing"], ["prefix-sums", "Prefix sums"], ["windows", "Windows"], ["stacks-queues", "Stacks and queues"],
    ["heaps-tries", "Heaps and tries"], ["intervals", "Intervals"], ["bits", "Bits"], ["simulation", "Simulation"],
    ["interpolation", "Interpolation"], ["group-regression", "Group regression"], ["rank-one-update", "Rank-one update"],
    ["data-cleaning", "Data cleaning"], ["cache", "Caches"], ["rate-limiter", "Rate limiters"],
    ["two-pointers", "Two pointers"], ["binary-search", "Binary search"], ["trees", "Trees"], ["graphs", "Graphs"],
    ["dp", "Dynamic programming"], ["backtracking", "Backtracking"], ["greedy", "Greedy"]
  ];
  const LANGS = [['python', 'Python'], ['cpp', 'C++']];
  const SESSION_MINUTES = 60;
  const patternName = (p) => { const k = PATTERNS.find(x => x[0] === p); return k ? k[1] : p; };
  const langOf = (d) => (d && d.language === 'cpp' ? 'cpp' : 'python');
  const langName = (l) => (l === 'cpp' ? 'C++' : 'Python');

  /* ---------- Small helpers ---------- */
  const clock = (sec) => { const s = Math.max(0, Math.floor(sec || 0)); return `${Math.floor(s / 60)}:${String(s % 60).padStart(2, '0')}`; };
  const spoken = (sec) => { const s = Math.max(0, Math.round(sec || 0)), m = Math.floor(s / 60); return m ? `${m} min ${String(s % 60).padStart(2, '0')} s` : `${s} s`; };
  const paceText = (pace) => (pace ? `pace ${Math.round(pace / 60 * 10) / 10 >= 1 ? Math.round(pace / 60) + ' min' : pace + ' s'}` : '');
  const store = (Z, k, v) => { try { if (v === undefined) return Z.store.get(k, null); Z.store.set(k, v); } catch { /* storage blocked */ } return null; };
  /* Inline copy (`code`, $maths$) and block copy, as drill.js does */
  const inline = (Z, s) => String(s).split(/(\$[^$]+\$[.,;:]?|`[^`]+`[.,;:]?)/g).map((p, i) => {
    if (!(i % 2)) return Z.esc(p);
    if (p[0] === '`') { const c = p.match(/^`([^`]+)`(.?)$/); return `<span class="drl-nw"><code class="drl-ic">${Z.esc(c[1])}</code>${Z.esc(c[2])}</span>`; }
    const m = p.match(/^\$([^$]+)\$(.?)$/);
    return `<span class="drl-nw">${Z.tex(m[1])}${Z.esc(m[2])}</span>`;
  }).join('');
  const block = (Z, s, cls = 't-prose') => String(s).split(/\n\s*\n/).map(p => p.trim()).filter(Boolean).map(p => {
    const m = p.match(/^\$\$([\s\S]+)\$\$$/);
    return m ? `<div class="drl-disp">${Z.tex(m[1], true)}</div>` : `<p class="${cls}">${inline(Z, p)}</p>`;
  }).join('');
  const dots = (Z, n) => `<span class="drl-diff-dots" role="img" aria-label="Difficulty ${n} of 5">${[1, 2, 3, 4, 5].map(i => `<i class="${i <= n ? 'on' : ''}"></i>`).join('')}</span>`;

  /* ---------- Stopwatch: counts up from when it starts; Date.now based, so a test can skew it ---------- */
  function Stopwatch(startNow = true) {
    let acc = 0, t0 = startNow ? Date.now() : null;
    return {
      start() { if (t0 == null) t0 = Date.now(); },
      pause() { if (t0 != null) { acc += Date.now() - t0; t0 = null; } },
      reset() { acc = 0; t0 = Date.now(); },
      running: () => t0 != null,
      seconds: () => (acc + (t0 == null ? 0 : Date.now() - t0)) / 1000,
    };
  }
  /* The pill in the top bar: time, pace, pause and restart. Returns { el, destroy }. */
  function stopwatchPill(Z, sw, pace) {
    const el = Z.h(`<div class="drl-sw" role="group" aria-label="Stopwatch">
      <span class="drl-sw-t tnum" role="timer" aria-live="off">0:00</span>
      ${pace ? `<span class="t-caption drl-sw-p">${Z.esc(paceText(pace))}</span>` : ''}
      <button type="button" class="icon-btn drl-sw-b" data-sw="toggle" aria-label="Pause the stopwatch">${Z.icon('pause', 'xs')}</button>
      <button type="button" class="icon-btn drl-sw-b" data-sw="reset" aria-label="Restart the stopwatch">${Z.icon('replay', 'xs')}</button></div>`);
    const t = el.querySelector('.drl-sw-t'), tog = el.querySelector('[data-sw="toggle"]');
    const paint = () => {
      const s = sw.seconds();
      t.textContent = clock(s);
      el.classList.toggle('is-over', !!pace && s > pace);
      el.classList.toggle('is-paused', !sw.running());
      tog.setAttribute('aria-label', sw.running() ? 'Pause the stopwatch' : 'Resume the stopwatch');
      tog.innerHTML = Z.icon(sw.running() ? 'pause' : 'play', 'xs');
    };
    el.addEventListener('click', (e) => {
      const b = e.target.closest('[data-sw]'); if (!b) return;
      if (b.dataset.sw === 'reset') sw.reset(); else if (sw.running()) sw.pause(); else sw.start();
      paint();
    });
    const iv = setInterval(paint, 1000);
    paint();
    return { el, paint, destroy: () => clearInterval(iv) };
  }

  /* ---------- Filters: pattern, difficulty range, language ---------- */
  const FKEY = 'drill.filters';
  const filters = (Z) => { const f = store(Z, FKEY) || {}; return { pattern: f.pattern || '', min: Math.min(5, Math.max(1, f.min | 0 || 1)), max: Math.min(5, Math.max(1, f.max | 0 || 5)), language: f.language || '' }; };
  const saveFilters = (Z, f) => store(Z, FKEY, f);
  const matches = (d, f) => (!f.pattern || d.pattern === f.pattern) && (d.difficulty || 2) >= f.min && (d.difficulty || 2) <= f.max && (!f.language || langOf(d) === f.language);
  const filterList = (list, f) => list.filter(d => matches(d, f));
  /* Only patterns some listed drill uses are offered, in vocabulary order */
  const filterBarHTML = (Z, f, list, idp) => {
    const used = new Set(list.map(d => d.pattern).filter(Boolean));
    const opt = (v, t, cur) => `<option value="${Z.esc(v)}"${String(cur) === String(v) ? ' selected' : ''}>${Z.esc(t)}</option>`;
    const nums = (cur) => [1, 2, 3, 4, 5].map(n => opt(n, n, cur)).join('');
    return `<form class="drlf" aria-label="Filter the drills" onsubmit="return false">
      <label class="drlf-f"><span class="t-caption">Pattern</span><select class="drlf-s" data-f="pattern" id="${idp}-p">${opt('', 'Any pattern', f.pattern)}${PATTERNS.filter(p => used.has(p[0])).map(p => opt(p[0], p[1], f.pattern)).join('')}</select></label>
      <label class="drlf-f"><span class="t-caption">Language</span><select class="drlf-s" data-f="language" id="${idp}-l">${opt('', 'Any language', f.language)}${LANGS.map(l => opt(l[0], l[1], f.language)).join('')}</select></label>
      <label class="drlf-f drlf-n"><span class="t-caption">Difficulty from</span><select class="drlf-s" data-f="min" id="${idp}-a">${nums(f.min)}</select></label>
      <label class="drlf-f drlf-n"><span class="t-caption">to</span><select class="drlf-s" data-f="max" id="${idp}-b">${nums(f.max)}</select></label>
    </form>`;
  };
  /* Wire a filter bar: a change updates and saves the filters (min never above max), then onChange(f) */
  const bindFilters = (Z, host, f, onChange) => {
    host.addEventListener('change', (e) => {
      const s = e.target.closest('[data-f]'); if (!s) return;
      const k = s.dataset.f;
      f[k] = k === 'min' || k === 'max' ? +s.value : s.value;
      if (f.min > f.max) { if (k === 'min') f.max = f.min; else f.min = f.max; host.querySelector('[data-f="min"]').value = f.min; host.querySelector('[data-f="max"]').value = f.max; }
      saveFilters(Z, f);
      onChange(f);
    });
  };

  /* ---------- Opening a drill by id in a host element (the session uses this; #drill/<id> goes through drill.js) ---------- */
  const openDrill = (host, Z, id, opts) => Promise.resolve(Z.content.drill(id)).then((d) => {
    if (!d) { host.innerHTML = `<p class="t-body secondary drl-l-wait">There is no drill called “${Z.esc(id)}”.</p>`; return () => {}; }
    const off = d.language === 'cpp' ? mountCpp(host, Z, d, opts) : ZQ.drillMount(host, Z, d, opts);
    Z.mathify(host);
    return off;
  });

  /* ---------- C++ drill page ---------- */
  /* d is the drill file; opts: { session: true } hides the close button and the stopwatch, seconds() gives the time on
     this drill (a session's), onResult({ passed, total, ok }) hears every submit, onClose() replaces leaving. */
  function mountCpp(root, Z, d, opts = {}) {
    const esc = Z.esc, I = Z.icon, id = d.id;
    const C = Z.content.course(d.course) || {};
    const topic = C.topic ? Z.content.topic(C.topic) : null;
    const tests = d.tests || [], examples = d.examples || [];
    const St = {
      code: (k) => { const x = Z.state && Z.state.drills && Z.state.drills.draft ? Z.state.drills.draft(k) : null; return x != null ? x : Z.store.get(`drill.${k}.code`, null); },
      setCode: (k, v) => { if (Z.state && Z.state.drills && Z.state.drills.draft) Z.state.drills.draft(k, v); else Z.store.set(`drill.${k}.code`, v); },
      state: (k) => Z.store.get(`drill.${k}.state`, null) || {},
      setState: (k, v) => Z.store.set(`drill.${k}.state`, v),
    };
    const rec0 = Z.state && Z.state.drills ? Z.state.drills.get(id) : null;
    const st0 = St.state(id);
    const S = { failed: st0.failed | 0, revealed: !!st0.revealed, ran: !!st0.ran, done: !!(rec0 && rec0.verified), verCode: rec0 && rec0.verified ? rec0.code : null,
      dirty: false, busy: false, last: null, compare: false };
    S.verified = S.done && !opts.session; // in a session Submit always grades
    const persist = () => St.setState(id, { failed: S.failed, revealed: S.revealed, ran: S.ran });
    const sw = opts.session ? null : Stopwatch(true);
    const secs = () => (opts.seconds ? opts.seconds() : sw.seconds());
    let since = Date.now(), alive = true;
    const timers = new Set();
    const later = (fn, ms) => { const t = setTimeout(() => { timers.delete(t); fn(); }, ms); timers.add(t); return t; };
    const logTime = () => {
      const minutes = Math.min(180, (Date.now() - since) / 60000); since = Date.now();
      try { if (Z.state && minutes >= 0.05) Z.state.hours.log({ block: 'build', minutes, source: 'drill:' + id }); } catch (e) { console.error(e); }
    };
    const callText = (c) => (c.compiles != null ? String(c.compiles)
      : Array.isArray(c.args) ? `${c.call}(${c.args.map(v => JSON.stringify(v)).join(', ')})` : c.call != null ? `${c.setup ? c.setup + '\n' : ''}${c.call}` : c.stdin != null ? String(c.stdin) : '(runs the whole program)');
    const expText = (c) => (c.expect == null ? '' : typeof c.expect === 'string' ? c.expect : JSON.stringify(c.expect));
    const exCard = (c, i) => `<div class="drl-exc"><p class="t-label drl-exc-h">Example ${i + 1}</p>
        <dl class="drl-io"><dt class="t-caption">Input</dt><dd><code>${esc(callText(c)).replace(/\n/g, '<br>')}</code></dd><dt class="t-caption">Output</dt><dd><code>${esc(expText(c))}</code></dd></dl>
        ${c.note ? `<p class="t-body drl-exc-why">${inline(Z, c.note)}</p>` : ''}</div>`;
    const L = Z.state ? Z.state.summary() : { todayQualified: false };

    root.innerHTML = `
    <div class="drlc${opts.session ? ' drl-in-session' : ''}" data-track="${esc(C.track || 'code')}">
      <header class="drlc-top">
        <button type="button" class="icon-btn drlc-close" aria-label="Close the drill. Your code is saved."${opts.session ? ' hidden' : ''}>${I('close')}</button>
        <div class="drl-ttl"><span class="drl-glyph" aria-hidden="true">${I('terminal', 'sm')}</span>
          <span class="drl-ttl-t"><span class="drl-ttl-a">${esc(d.name)}</span><span class="t-caption drl-ttl-b">Code drill · C++ · ${esc(C.name || d.course)}</span></span></div>
        <div class="drl-stats"><span class="drlc-sw-host"></span>${opts.session ? '' : `<span class="drl-bolt" role="img" aria-label="${L.todayQualified ? 'Streak extended today' : 'Streak not yet extended today'}">${Z.bolt(L.todayQualified)}</span>`}</div>
      </header>
      <main class="drlc-main"><article class="drlc-in">
        <p class="t-overline drl-ov">Code drill${topic ? ' · ' + esc(topic.id + ' ' + topic.name) : ''}</p>
        <h1 class="t-lesson-title drl-h">${esc(d.name)}</h1>
        <div class="drl-meta">
          <span class="chip track">${I('terminal', 'xs')}${esc(C.name || d.course)}</span>
          <span class="chip soft">C++</span>
          ${d.pattern ? `<span class="chip soft">${esc(patternName(d.pattern))}</span>` : ''}
          <span class="chip soft">${I('timer', 'xs')}5 s a test</span>
          ${d.pace ? `<span class="chip soft">${I('clock', 'xs')}${esc(paceText(d.pace))}</span>` : ''}
          <span class="chip soft drl-meta-d">${dots(Z, d.difficulty || 2)}<span>Difficulty ${d.difficulty || 2}</span></span>
          <span class="chip correct drl-meta-v"${S.done ? '' : ' hidden'}>${I('check', 'xs')}Verified</span>
        </div>
        ${block(Z, d.brief || '')}
        ${d.definition ? `<div class="drl-def">${block(Z, d.definition, 't-body')}</div>` : ''}
        <h2 class="t-h2 drl-sec">Examples</h2>
        <div class="drl-exs">${examples.map(exCard).join('')}</div>
        ${(d.constraints || []).length ? `<h2 class="t-h2 drl-sec">Constraints</h2><ul class="drl-cons t-body">${d.constraints.map(c => `<li>${inline(Z, c)}</li>`).join('')}</ul>` : ''}
        ${d.hint ? `<details class="drl-hint drlc-hint"${S.ran ? '' : ' hidden'}><summary><span class="drl-hint-i">${I('bulb', 'sm')}</span><span class="drl-hint-l"><span>Hint</span></span></summary><div class="drl-hint-b t-body">${inline(Z, d.hint)}</div></details>` : ''}
        <div class="drl-how"><span class="drl-how-i" aria-hidden="true">${I('clipboard', 'sm')}</span><div class="drl-how-t"><p class="t-label">How it is checked</p><p class="t-body">${inline(Z, d.how || '')}</p></div></div>
        ${d.where ? `<p class="t-caption drl-where">${inline(Z, d.where)}</p>` : ''}
        <h2 class="t-h2 drl-sec">Your code</h2>
        <div class="drlc-code"></div>
        <div class="drlc-act"><button type="button" class="link-btn drlc-ref" hidden>Show model solution</button>
          <button type="button" class="btn drlc-submit" disabled><span>Loading C++…</span></button></div>
        <div class="drlc-sum" aria-live="polite"></div>
        <div class="drlc-model"></div>
      </article></main>
      <p class="sr-only" aria-live="polite" data-live></p>
    </div>`;
    const $ = (s) => root.querySelector(s);
    const page = $('.drlc'), sum = $('.drlc-sum'), modelBox = $('.drlc-model'), subBtn = $('.drlc-submit'), refBtn = $('.drlc-ref'), live = $('[data-live]'), hint = $('.drlc-hint');
    const say = (t) => { live.textContent = ''; later(() => { live.textContent = t; }, 30); };
    const setVerdict = (v) => ['ok', 'no', 'rev'].forEach(k => page.classList.toggle('is-' + k, v === k));
    let pill = null;
    if (sw) { pill = stopwatchPill(Z, sw, d.pace); $('.drlc-sw-host').append(pill.el); }

    /* The widget: every drill field the C++ code widget reads is passed on */
    const KEYS = ['starter', 'solution', 'how', 'flags', 'prelude', 'postlude', 'files', 'leakCheck', 'testkit', 'signature', 'budget'];
    const spec = { kind: 'code', language: 'cpp', examples, tests };
    KEYS.forEach(k => { if (d[k] != null) spec[k] = d[k]; });
    const widgetHost = $('.drlc-code');
    let w = null; // the widget reports its status while it is being built, before w is set
    w = Z.cppCode(widgetHost, spec, { draftKey: id, change: (c) => { if (!alive) return; if (c && c.code != null && S.verCode != null) S.dirty = c.code !== S.verCode; paint(); } });
    if (St.code(id) == null && rec0 && rec0.verified && typeof rec0.code === 'string' && rec0.code.trim()) w.set(rec0.code);
    const status = () => { const e = widgetHost.querySelector('.wd-py'); return e ? e.dataset.s : 'idle'; };
    widgetHost.querySelector('.wd-run').addEventListener('click', () => { S.ran = true; persist(); unlockHint(); });
    const unlockHint = () => { if (hint) hint.hidden = false; };
    if (S.ran) unlockHint();

    function paint() {
      if (!w) return;
      const cont = S.verified && !S.dirty, st = status();
      subBtn.querySelector('span').textContent = cont ? 'Continue' : S.busy ? 'Running tests…' : st === 'unavailable' ? 'C++ unavailable' : st === 'ready' || st === 'running' ? 'Submit' : 'Loading C++…';
      subBtn.classList.toggle('correct', cont && !S.revealed);
      subBtn.disabled = cont ? false : S.busy || !(st === 'ready') || !w.dirty();
      refBtn.hidden = cont || S.done || !(S.revealed || S.failed >= 2);
      refBtn.textContent = S.revealed ? 'Model solution' : 'Show model solution';
    }
    const iv = setInterval(paint, 400); // the widget reports its status through its own element; poll it
    const modelHTML = () => `<div class="drl-model"><div class="drl-model-h"><p class="t-label">Model solution</p></div>
        <pre class="drl-sh-code drl-cmp-code" tabindex="0" aria-label="Model solution"><code>${esc(String(d.solution || '').trimEnd())}</code></pre>
        ${(d.notes || []).length ? `<ul class="drl-sh-pts t-body">${d.notes.map(t => `<li>${inline(Z, t)}</li>`).join('')}</ul>` : ''}</div>`;
    if (S.done) modelBox.innerHTML = modelHTML();

    const result = (r) => {
      const total = r.detail ? r.detail.total : tests.length, passed = r.detail ? r.detail.passed : 0;
      return { passed, total, ok: !!r.ok };
    };
    const submit = async () => {
      if (S.verified && !S.dirty) { leave(); return; }
      if (S.busy || status() !== 'ready' || !w.dirty()) return;
      S.busy = true; S.ran = true; unlockHint(); setVerdict(null); paint();
      let r;
      try { r = await w.grade(); } catch (e) { r = { ok: false, key: 'error', line: String((e && e.message) || e), detail: null }; }
      S.busy = false;
      if (!alive) return r;
      try { w.markGraded(r); } catch { /* the widget is gone */ }
      const code = w.value(), x = result(r), t = secs();
      S.last = { mode: 'submit', ...x, key: r.key };
      if (pill) pill.paint();
      const counted = r.detail && r.key !== 'compile' && r.key !== 'unavailable';
      if (counted) {
        try { if (Z.state) Z.state.drills.time(id, { seconds: t, passed: x.passed, total: x.total, ok: x.ok }); } catch (e) { console.error(e); }
        if (opts.onResult) opts.onResult(x);
      }
      if (r.ok) {
        const repeat = S.done, rev = S.revealed;
        S.verified = S.done = true; S.verCode = code; S.dirty = false;
        try { if (Z.state) Z.state.drills.verified(id, code); } catch (e) { console.error(e); }
        logTime(); St.setCode(id, code);
        $('.drl-meta-v').hidden = false;
        const note = repeat ? 'Verified again.' : rev ? 'Verified. You opened the model solution first, so compare it with your own.' : 'Added to your drill record on You.';
        sum.innerHTML = `<div class="${rev ? 'drl-match' : 'drl-ver'}"><div class="drl-ver-top"><span class="chip ${rev ? 'drl-match-chip' : 'correct drl-ver-chip'}">${I(rev ? 'bulb' : 'check', 'xs')}Verified</span></div>
          <p class="t-h2 drl-ver-h">All ${x.total} tests passed in ${esc(spoken(t))}.</p>
          <p class="t-body drl-ver-n">${esc(note)}${d.pace ? esc(t <= d.pace ? ` That is inside the pace of ${spoken(d.pace)}.` : ` The pace is ${spoken(d.pace)}.`) : ''}</p></div>`;
        modelBox.innerHTML = modelHTML();
        setVerdict(rev ? 'rev' : 'ok');
        if (!rev) { Z.sound('correct'); Z.haptic(); later(() => Z.burst(sum.querySelector('.drl-ver-chip')), 120); }
        say(`Verified. All ${x.total} tests passed.`);
        Z.emit('drill:verified', { id, revealed: rev });
      } else {
        if (counted) { S.failed += 1; persist(); }
        const first = /^test-(\d+)$/.exec(r.key || '');
        const line = r.key === 'compile' ? 'Your code did not compile, so no test ran. The compiler message is under the editor.'
          : r.key === 'unavailable' ? (r.line || 'The C++ compiler could not load.')
          : r.key === 'error' ? (r.line || 'The tests could not run. Try again.')
          : `${x.passed} of ${x.total} tests passed.${first ? ` The first failure is test ${first[1]}.` : ''}`;
        sum.innerHTML = `<div class="drl-fail"><span class="chip notyet">${I('cross', 'xs')}Not quite right</span><p class="t-body">${esc(line)}</p></div>`;
        setVerdict('no'); Z.sound('notyet');
        say(`Not quite right. ${x.passed} of ${x.total} tests passed.`);
      }
      paint();
      return r;
    };
    subBtn.addEventListener('click', submit);
    const showReference = () => {
      const box = Z.h('<div class="drl-sh"></div>');
      let close = () => {};
      const showCode = () => {
        box.innerHTML = `<h2 class="t-sheet-title drl-sh-t">Model solution</h2>
          <pre class="drl-sh-code" tabindex="0" aria-label="Model solution code"><code>${esc(String(d.solution || '').trimEnd())}</code></pre>
          ${(d.notes || []).length ? `<ul class="drl-sh-pts t-body">${d.notes.map(t => `<li>${inline(Z, t)}</li>`).join('')}</ul>` : ''}
          <div class="drl-sh-act"><button type="button" class="btn secondary" data-copy>Copy into editor</button><button type="button" class="btn" data-close>Done</button></div>`;
        box.querySelector('[data-copy]').addEventListener('click', () => { close(); w.set(d.solution || ''); paint(); });
      };
      if (S.revealed) { showCode(); close = Z.sheet(box, { label: 'Model solution' }); return; }
      box.innerHTML = `<h2 class="t-sheet-title drl-sh-t">Show the model solution?</h2>
        <p class="t-body drl-sh-p">You will see a full answer. The drill still counts once your own code passes, but you learn more from one more try with the hint.</p>
        <div class="drl-sh-act"><button type="button" class="btn secondary" data-close autofocus>Keep trying</button><button type="button" class="btn" data-reveal>Show solution</button></div>`;
      box.querySelector('[data-reveal]').addEventListener('click', () => { S.revealed = true; persist(); paint(); showCode(); box.querySelector('[data-close]').focus(); });
      close = Z.sheet(box, { label: 'Model solution' });
    };
    refBtn.addEventListener('click', showReference);
    const leave = () => { St.setCode(id, w.value()); if (opts.onClose) opts.onClose(); else Z.go(leaveTo()); };
    const leaveTo = () => opts.back || 'drill';
    $('.drlc-close').addEventListener('click', leave);
    page.addEventListener('keydown', (e) => { if ((e.ctrlKey || e.metaKey) && e.key === 'Enter' && e.shiftKey) { e.preventDefault(); submit(); } });
    paint();

    const hook = window.ZQDrill = {
      language: 'cpp', setCode: (s) => { w.set(String(s)); paint(); }, code: () => w.value(), run: () => { const b = widgetHost.querySelector('.wd-run'); if (b && !b.disabled) b.click(); },
      submit, status, tab: () => {}, reference: () => d.solution || '', problem: () => id, verified: () => S.verified,
      results: () => (S.last ? { mode: S.last.mode, passed: S.last.passed, total: S.last.total, ok: S.last.ok } : null),
      seconds: () => secs(), pace: () => d.pace || null, summary: () => sum.textContent.replace(/\s+/g, ' ').trim(),
    };
    return () => {
      alive = false; clearInterval(iv);
      try { St.setCode(id, w.value()); } catch { /* gone */ }
      logTime();
      timers.forEach(clearTimeout); timers.clear();
      if (pill) pill.destroy();
      try { w.destroy(); } catch { /* gone */ }
      if (window.ZQDrill === hook) delete window.ZQDrill; // a late cleanup must not remove a newer drill's hook
    };
  }

  /* ---------- Sessions: two drills, one countdown ---------- */
  const SKEY = 'drill.session';
  const rand = { f: Math.random };
  /* Two drills from the list that pass the filters: unverified first, and two different patterns when there is a choice */
  const pickTwo = (Z, list, f, avoid) => {
    const rec = (id) => (Z.state && Z.state.drills ? Z.state.drills.get(id) : null) || {};
    const pool = filterList(list, f).filter(d => !d.sample);
    if (pool.length < 2) return null;
    const take = (a) => a[Math.floor(rand.f() * a.length) % a.length];
    const fresh = pool.filter(d => !rec(d.id).verified && !(avoid || []).includes(d.id));
    const first = take(fresh.length ? fresh : pool);
    const rest = pool.filter(d => d.id !== first.id);
    const best = rest.filter(d => d.pattern !== first.pattern && !rec(d.id).verified && !(avoid || []).includes(d.id));
    const mid = rest.filter(d => !rec(d.id).verified);
    const second = take(best.length ? best : mid.length ? mid : rest);
    return [first.id, second.id];
  };

  function session(root, Z, params) {
    const esc = Z.esc, I = Z.icon;
    let alive = true, off = null, tick = 0, drillOff = null;
    const getS = () => store(Z, SKEY);
    const putS = (s) => store(Z, SKEY, s);
    const nowS = () => Date.now();
    const used = (S) => (nowS() - S.startAt) / 1000;
    const left = (S) => S.minutes * 60 - used(S);
    /* what a drill is called: the listed row, else its file (a sample drill is not listed), else its id */
    const info = {};
    const row = (Z2, id) => info[id] || Z.content.drills().find(r => r.id === id) || { id, name: id, difficulty: 2 };
    const loadInfo = (ids) => Promise.all(ids.map(i => Promise.resolve(Z.content.drill(i)).then(d => { if (d) info[i] = { id: i, name: d.name, difficulty: d.difficulty, pace: d.pace, pattern: d.pattern, language: d.language }; }).catch(() => {})));
    const stop = () => { clearInterval(tick); tick = 0; if (drillOff) { try { drillOff(); } catch { /* gone */ } drillOff = null; } delete window.ZQSession; };

    const wrap = (inner, cls = '') => { root.innerHTML = `<div class="drls ${cls}">${inner}</div>`; };
    const goBackLink = `<a class="link-btn" href="#drill">Back to the drill list</a>`;

    /* ----- Setup ----- */
    const setup = async (fixedId) => {
      const list = Z.content.drills();
      const f = filters(Z);
      const act = getS();
      const fixedIds = (Z.content.drillSessionIds ? Z.content.drillSessionIds() : []);
      const fixedDocs = (await Promise.all(fixedIds.map(i => Z.content.drillSession(i).catch(() => null)))).filter(x => x && !x.sample);
      let fixed = null;
      if (fixedId) { fixed = await Z.content.drillSession(fixedId).catch(() => null); if (!fixed) { fixedId = null; } }
      if (!alive) return;
      let picks = fixed ? fixed.drills.slice() : pickTwo(Z, list, f);
      if (fixed) await loadInfo(fixed.drills);
      if (!alive) return;
      const minutes = fixed && fixed.minutes ? fixed.minutes : SESSION_MINUTES;
      const paint = () => {
        const items = (picks || []).map((id, i) => { const r = row(Z, id), total = (r.pace || 0); return `<li class="drls-pick"><span class="drls-n tnum">${i + 1}</span>
          <span class="drls-pick-t"><span class="t-label">${esc(r.name)}</span><span class="t-caption muted">${esc(langName(langOf(r)))}${r.pattern ? ' · ' + esc(patternName(r.pattern)) : ''}${total ? ' · ' + esc(paceText(total)) : ''}</span></span>${dots(Z, r.difficulty || 2)}</li>`; }).join('');
        wrap(`<header class="drl-top drl-l-top"><button type="button" class="icon-btn drl-close" aria-label="Close">${I('close')}</button>
            <div class="drl-ttl"><span class="drl-glyph" aria-hidden="true" data-track="code">${I('timer', 'sm')}</span><span class="drl-ttl-t"><span class="drl-ttl-a">Drill session</span></span></div><div></div></header>
          <main class="drl-l-main">
            <div class="drl-l-head"><p class="t-overline muted">Build</p><h1 class="t-course-title">${fixed ? esc(fixed.name) : 'A session of two drills'}</h1>
              <p class="t-body secondary">${fixed && fixed.brief ? esc(fixed.brief) : `Two drills against one ${minutes}-minute clock, as an online assessment or a live round gives them. Split your time as you like: a plan of 5, 25, 25 and 5 minutes for reading, solving, solving and checking works well. The clock keeps running if you leave the page.`}</p></div>
            ${act && !act.done ? `<div class="drls-warn" role="status"><p class="t-body">A session is already running, with ${esc(clock(Math.max(0, left(act))))} left.</p>
              <div class="drls-btns"><a class="btn secondary" href="#drill/session">Resume it</a><button type="button" class="btn secondary" data-abandon>Abandon it</button></div></div>` : ''}
            ${fixed ? '' : `<section aria-label="Filters"><h2 class="t-h2">Choose the kind</h2>${filterBarHTML(Z, f, list, 'drls')}</section>`}
            <section aria-label="The two drills"><h2 class="t-h2">Your two drills</h2>
              ${picks ? `<ol class="drls-picks">${items}</ol>` : '<p class="t-body secondary" role="status">Fewer than two drills match these filters. Widen the pattern, difficulty or language.</p>'}
              <div class="drls-btns">${fixed || !picks ? '' : '<button type="button" class="btn secondary" data-again>Pick again</button>'}
                <button type="button" class="btn" data-start${picks ? '' : ' disabled'}>Start the ${minutes}-minute session</button></div>
            </section>
            ${!fixed && fixedDocs.length ? `<section aria-label="Set sessions"><h2 class="t-h2">Set sessions</h2><ul class="drl-l-list">${fixedDocs.map(x => `<li><a class="drl-l-item" href="#drill/session/${esc(x.id)}"><span class="drl-l-ic" aria-hidden="true">${I('timer', 'sm')}</span><span class="drl-l-t"><span class="t-label">${esc(x.name)}</span><span class="t-caption muted">${x.drills.length} drills · ${x.minutes || SESSION_MINUTES} minutes</span></span>${I('chevronR', 'sm drl-l-chev')}</a></li>`).join('')}</ul></section>` : ''}
            <p>${goBackLink}</p>
          </main>`);
        root.querySelector('.drl-close').addEventListener('click', () => Z.go('drill'));
        const fb = root.querySelector('.drlf');
        if (fb) bindFilters(Z, fb, f, () => { picks = pickTwo(Z, list, f); paint(); });
        const ag = root.querySelector('[data-again]'); if (ag) ag.addEventListener('click', () => { picks = pickTwo(Z, list, f, picks); paint(); });
        const ab = root.querySelector('[data-abandon]'); if (ab) ab.addEventListener('click', () => { putS(null); paint(); });
        const go = root.querySelector('[data-start]');
        if (go) go.addEventListener('click', () => {
          if (!picks) return;
          putS({ v: 1, name: fixed ? fixed.name : 'Drill session', fixedId: fixed ? fixed.id : null, minutes, startAt: nowS(), ids: picks.slice(), cur: 0, curSince: nowS(),
            per: picks.map(() => ({ seconds: 0, passed: 0, total: 0, ok: false })), done: false });
          Z.go('drill/session');
        });
      };
      paint();
    };

    /* Close a session: the running drill's minutes are added, the total is held to the budget, the result is kept */
    const finishS = (S, why) => {
      if (S.done) return;
      const per = S.per;
      per[S.cur].seconds += (nowS() - S.curSince) / 1000; S.curSince = nowS();
      const budget = S.minutes * 60, total = per.reduce((a, p) => a + p.seconds, 0);
      if (total > budget) per[S.cur].seconds = Math.max(0, per[S.cur].seconds - (total - budget));
      S.done = true; S.endedBy = why; S.seconds = Math.min(budget, per.reduce((a, p) => a + p.seconds, 0));
      S.result = { name: S.name, minutes: S.minutes, seconds: S.seconds, drills: S.ids.map((id, i) => ({ id, seconds: per[i].seconds, passed: per[i].passed, total: per[i].total, ok: per[i].ok })) };
      try { if (Z.state) Z.state.drills.session(S.result); } catch (e) { console.error(e); }
      putS(S);
      stop();
      result(S);
    };

    /* ----- Running ----- */
    const run = (S) => {
      const per = S.per;
      const secsOn = (i) => per[i].seconds + (i === S.cur ? (nowS() - S.curSince) / 1000 : 0);
      const nameOf = (i) => row(Z, S.ids[i]).name;
      wrap(`<div class="drls-bar" role="group" aria-label="Session">
          <button type="button" class="icon-btn drls-leave" aria-label="Leave this page. The clock keeps running.">${I('close')}</button>
          <div class="drls-tabs" role="tablist" aria-label="Drills in this session">${S.ids.map((id, i) => `<button type="button" role="tab" class="drls-tab" data-i="${i}" aria-selected="${i === S.cur}"><span class="drls-tab-n tnum">${i + 1}</span><span class="drls-tab-t">${esc(nameOf(i))}</span><span class="drls-tab-s" aria-hidden="true"></span></button>`).join('')}</div>
          <div class="drls-clock" role="timer" aria-live="off" aria-label="Time left"><span class="drls-clock-t tnum">60:00</span></div>
          <button type="button" class="btn secondary drls-fin">Finish</button></div>
        <div class="drls-host"></div><p class="sr-only" aria-live="polite" data-live></p>`);
      const bar = root.querySelector('.drls-bar'), host = root.querySelector('.drls-host'), ct = root.querySelector('.drls-clock-t'), live = root.querySelector('[data-live]');
      let warned = 0;
      const paintBar = () => {
        const r = left(S);
        ct.textContent = clock(Math.ceil(Math.max(0, r)));
        bar.classList.toggle('is-low', r <= 300);
        bar.querySelectorAll('.drls-tab').forEach(b => { const i = +b.dataset.i; b.setAttribute('aria-selected', String(i === S.cur)); b.tabIndex = i === S.cur ? 0 : -1; b.querySelector('.drls-tab-s').innerHTML = per[i].ok ? I('check', 'xs') : ''; });
        [300, 60].forEach(t => { if (r <= t && warned < t && r > 0) { warned = t; live.textContent = ''; setTimeout(() => { live.textContent = `${t / 60} minute${t > 60 ? 's' : ''} left.`; }, 30); } });
      };
      const mountCur = () => {
        if (drillOff) { try { drillOff(); } catch { /* gone */ } drillOff = null; }
        const i = S.cur;
        host.innerHTML = '<p class="t-body secondary drl-l-wait">Loading the drill…</p>';
        openDrill(host, Z, S.ids[i], {
          session: true, seconds: () => secsOn(i),
          onResult: (x) => { const p = per[i]; if (x.passed >= p.passed || x.ok) { p.passed = x.passed; p.total = x.total; } p.total = x.total; p.ok = p.ok || x.ok; putS(S); paintBar(); },
          onClose: () => switchTo(S.cur === 0 ? 1 : 0),
        }).then((o) => { if (!alive || S.cur !== i) { try { o(); } catch { /* gone */ } return; } drillOff = o; });
      };
      const switchTo = (i) => {
        if (i === S.cur || i < 0 || i >= S.ids.length) return;
        per[S.cur].seconds += (nowS() - S.curSince) / 1000; S.cur = i; S.curSince = nowS(); putS(S);
        paintBar(); mountCur();
      };
      bar.addEventListener('click', (e) => {
        const t = e.target.closest('.drls-tab'); if (t) { switchTo(+t.dataset.i); return; }
        if (e.target.closest('.drls-leave')) { Z.go('today'); return; }
        if (e.target.closest('.drls-fin')) {
          const box = Z.h(`<div class="drl-sh"><h2 class="t-sheet-title drl-sh-t">Finish the session?</h2><p class="t-body drl-sh-p">Each drill counts as it stands: the hidden tests it last passed and the minutes you spent on it. You cannot reopen the session afterwards.</p>
            <div class="drl-sh-act"><button type="button" class="btn secondary" data-close autofocus>Keep going</button><button type="button" class="btn" data-fin>Finish</button></div></div>`);
          const close = Z.sheet(box, { label: 'Finish the session' });
          box.querySelector('[data-fin]').addEventListener('click', () => { close(); finishS(S, 'finish'); });
        }
      });
      bar.querySelector('.drls-tabs').addEventListener('keydown', (e) => {
        const j = e.key === 'ArrowRight' ? (S.cur + 1) % S.ids.length : e.key === 'ArrowLeft' ? (S.cur + S.ids.length - 1) % S.ids.length : -1;
        if (j >= 0) { e.preventDefault(); switchTo(j); const b = bar.querySelector(`.drls-tab[data-i="${j}"]`); if (b) b.focus(); }
      });
      tick = setInterval(() => { if (left(S) <= 0) { finishS(S, 'time'); return; } paintBar(); }, 1000);
      paintBar(); mountCur();
      window.ZQSession = {
        state: () => ({ cur: S.cur, ids: S.ids.slice(), per: per.map(p => ({ ...p })), left: left(S), done: S.done }),
        switchTo, finish: (why) => finishS(S, why || 'finish'),
        /* move the start so that `s` seconds remain (the clock is not waited for) */
        setRemaining: (s) => { S.startAt = nowS() - (S.minutes * 60 - s) * 1000; putS(S); paintBar(); },
        tick: () => { if (left(S) <= 0) finishS(S, 'time'); else paintBar(); },
      };
    };

    /* ----- Result ----- */
    const result = (S) => {
      const R = S.result || { name: S.name, minutes: S.minutes, seconds: S.seconds || 0, drills: [] };
      const row2 = (d, i) => { const r = row(Z, d.id), pace = r.pace;
        return `<tr><th scope="row"><span class="drls-n tnum">${i + 1}</span> <a href="#drill/${esc(d.id)}">${esc(r.name)}</a></th>
          <td class="tnum" data-k="minutes">${esc(spoken(d.seconds))}${pace ? `<span class="t-caption muted"> of ${esc(spoken(pace))} pace</span>` : ''}</td>
          <td class="tnum" data-k="tests">${d.total ? `${d.passed} of ${d.total}` : 'not submitted'}</td>
          <td data-k="state">${d.ok ? `<span class="chip correct">${I('check', 'xs')}Verified</span>` : '<span class="chip soft">Not solved</span>'}</td></tr>`; };
      const solved = R.drills.filter(d => d.ok).length;
      wrap(`<header class="drl-top drl-l-top"><button type="button" class="icon-btn drl-close" aria-label="Close">${I('close')}</button>
          <div class="drl-ttl"><span class="drl-glyph" aria-hidden="true" data-track="code">${I('timer', 'sm')}</span><span class="drl-ttl-t"><span class="drl-ttl-a">Session result</span></span></div><div></div></header>
        <main class="drl-l-main"><div class="drl-l-head"><p class="t-overline muted">${esc(R.name)}</p><h1 class="t-course-title">${solved} of ${R.drills.length} drills solved</h1>
          <p class="t-body secondary drls-sum">You used ${esc(spoken(R.seconds))} of ${R.minutes} minutes${S.endedBy === 'time' ? ': the clock ran out' : ''}. ${R.drills.length === 2 ? `Your split was ${esc(spoken(R.drills[0].seconds))} then ${esc(spoken(R.drills[1].seconds))}.` : ''}</p></div>
          <div class="drls-tw"><table class="drls-table"><thead><tr><th scope="col">Drill</th><th scope="col">Time on it</th><th scope="col">Hidden tests passed</th><th scope="col">Result</th></tr></thead><tbody>${R.drills.map(row2).join('')}</tbody></table></div>
          <div class="drls-btns"><a class="btn" href="#drill/session/new">Start another session</a><a class="btn secondary" href="#drill">Back to the drills</a></div>
        </main>`);
      root.querySelector('.drl-close').addEventListener('click', () => Z.go('drill'));
      window.ZQSession = { result: () => R, state: () => ({ done: true }) };
    };

    /* ----- Route ----- */
    const a = params && params[0];
    const S = getS();
    if (a === 'new') setup(null);
    else if (a && a !== 'result') setup(a);
    else if (S && S.v === 1 && Array.isArray(S.ids) && S.ids.length && (S.done ? S.result : true)) {
      loadInfo(S.ids).then(() => {
        if (!alive) return;
        if (S.done) result(S); else if (left(S) <= 0) finishS(S, 'time'); else run(S);
      });
    } else setup(null);
    return () => { alive = false; stop(); };
  }

  ZQ.drillLib = { PATTERNS, LANGS, SESSION_MINUTES, patternName, langOf, langName, clock, spoken, paceText, Stopwatch, stopwatchPill,
    filters, filterList, filterBarHTML, bindFilters, matches, pickTwo, openDrill, mountCpp, session, inline, block, dots, rand };
})();
