/* Lesson player (docs/PLAN.md section 7). Renders a lesson file (docs/AUTHORING.md) with the prototype's lesson
   look: top bar (close, progress bar with the trailing quiz pill, XP, streak), frame, card utilities, the 540px
   column, canvas, question line, widget, verdict chip and the button group. Spec: design-research 4.5 to 4.9, 5.

   ZQ.player.mount(host, { course, lesson, start })   lesson is an id or a lesson object; start: undefined (resume),
                                                       'quiz', 'done' or a screen index. Returns cleanup().
   ZQ.player.renderItem(item, host, { mode, onGraded }) one item for reviews, homework, redo, practice and exams.
   ZQ.player.runSet(host, { title, items, mode, hints: false, onDone }) a list with dot progress, one try each.
   window.ZQ.test while a lesson is mounted: current(), answerCorrect(), check(), continue() (see the bottom). runSet
   installs the same four calls for its set (current().phase is 'set'; kind is 'item' until the last Finish, then 'done').

   Learner state goes through ZQ.state mutators when they exist (screenGraded, lessonFinished, quizFinished,
   notebook.add, hours.log, lessonPosition.get/set, summary). Every call is guarded, and without ZQ.state the
   player keeps an in-memory and localStorage fallback so a lesson always plays. */
(function () {
  'use strict';
  const Z = window.ZQ;
  const G = () => Z.grade;
  const XP = { first: 15, retry: 5, quiz: 15, finish: 20, perfect: 15 };
  const RUNG = { nudge: 'Nudge', point: 'Point', step: 'Step' };
  const BOUND = new Set(['tap-regions', 'drag-point', 'sketch', 'balance']); // widgets that act on the canvas itself
  const fmt = (n) => Math.round(n).toLocaleString('en-GB');
  const clock = (s) => `${Math.floor(s / 60)}:${String(Math.round(s) % 60).padStart(2, '0')}`;
  const ymd = (d = new Date()) => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`;
  const rngFrom = (seed) => { let a = seed >>> 0; return () => { a = (a + 0x6D2B79F5) >>> 0; let t = a; t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; };
  const hash = (s) => { let h = 2166136261; for (const c of String(s)) { h ^= c.charCodeAt(0); h = Math.imul(h, 16777619); } return h >>> 0; };
  const empty = (v) => v == null || v === '' || (Array.isArray(v) && !v.length) || (typeof v === 'object' && !Array.isArray(v) && Object.values(v).every(empty));

  /* ---------- Learner state adapter ---------- */
  const stFn = (path) => {
    const S = window.ZQ && window.ZQ.state; if (!S) return null;
    let o = S, parent = S;
    for (const k of path.split('.')) { parent = o; o = o == null ? undefined : o[k]; }
    return typeof o === 'function' ? o.bind(parent) : null;
  };
  const st = (path, ...args) => { const f = stFn(path); if (!f) return undefined; try { return f(...args); } catch (e) { console.error('ZQ.state.' + path + ' failed', e); return undefined; } };
  const mem = { day: null, streak: null };
  const position = {
    get(c, l) { if (stFn('lessonPosition.get')) return st('lessonPosition.get', c, l); return Z.store.get(`pos.${c}/${l}`, null); },
    set(c, l, v) { if (stFn('lessonPosition.set')) st('lessonPosition.set', c, l, v); else Z.store.set(`pos.${c}/${l}`, v); },
  };
  /* Streak and today, from ZQ.state.summary() whatever its exact shape, else a local fallback */
  const daySummary = () => {
    const s = st('summary');
    const today = ymd();
    if (s && typeof s === 'object') {
      const so = s.streak && typeof s.streak === 'object' ? s.streak : {};
      const current = typeof s.streak === 'number' ? s.streak : (so.current ?? s.currentStreak ?? 0);
      let done = s.todayQualified ?? s.todayDone ?? s.qualifiedToday ?? (s.today && (s.today.qualified ?? s.today.done)) ?? so.todayDone;
      if (done == null && so.days) done = !!so.days[today];
      if (done == null && so.lastDay) done = so.lastDay === today;
      const off = !!s.streakOff || (s.settings && s.settings.streakMode === 'off') || so.mode === 'off';
      return { streak: +current || 0, todayDone: !!done, off: !!off, real: true };
    }
    const local = Z.store.get('player.streak', { n: 0, day: null });
    return { streak: mem.streak ?? local.n ?? 0, todayDone: (mem.day ?? local.day) === today, off: false, real: false };
  };
  const qualifyLocal = () => {
    const local = Z.store.get('player.streak', { n: 0, day: null }), today = ymd();
    if (local.day === today) return;
    const y = new Date(); y.setDate(y.getDate() - 1);
    const n = local.day === ymd(y) ? (local.n || 0) + 1 : 1;
    Z.store.set('player.streak', { n, day: today }); mem.day = today; mem.streak = n;
  };
  const xpOf = (r, local) => (typeof r === 'number' ? r : r && typeof r === 'object' && typeof r.xp === 'number' ? r.xp : local);

  /* ---------- Content ---------- */
  const fetchLesson = (course, id) => fetch(`content/courses/${encodeURIComponent(course)}/${encodeURIComponent(id)}.json`, { cache: 'no-cache' }).then(r => { if (!r.ok) throw new Error('Lesson file not found: ' + course + '/' + id); return r.json(); });
  const loadLesson = async (course, id) => {
    const C = window.ZQ.content;
    if (C && typeof C.lesson === 'function') {
      try { const L = await C.lesson(course, id); if (L && L.screens) return L; } catch (e) { /* not registered yet: read the file directly */ }
    }
    return fetchLesson(course, id);
  };
  const courseInfo = (course, lessonId) => {
    const C = window.ZQ.content;
    let c = null;
    try { c = C && C.course ? C.course(course) : null; } catch { c = null; }
    let level = null, n = null;
    (c && c.levels || []).forEach(lv => { const i = (lv.lessons || []).indexOf(lessonId); if (i >= 0) { level = lv.n ?? lv.level; n = i + 1; } });
    let track = c && c.track;
    if (!track && c && c.topic && C && C.topic) { try { track = (C.topic(c.topic) || {}).track; } catch { /* no topic */ } }
    return { name: c && c.name, art: (c && c.art) || 'tree', track: track || 'prob', level, n };
  };
  const nextItem = async (course, lessonId) => {
    const C = window.ZQ.content;
    if (!C || typeof C.next !== 'function') return null;
    try {
      const n = await C.next(course, lessonId);
      if (!n || n.written === false) return null;
      if (typeof n === 'string') return { kind: /^review/.test(n) ? 'review' : /^homework/.test(n) ? 'homework' : 'lesson', id: n, course };
      return { kind: n.kind || n.type || 'lesson', id: n.id || n.lesson, course: n.course || course, name: n.name || n.title, level: n.level };
    } catch (e) { console.error(e); return null; }
  };
  const routeFor = (n) => `#${n.kind === 'review' ? 'review' : n.kind === 'homework' ? 'homework' : 'lesson'}/${n.course}/${n.id}`;

  /* ---------- Feedback copy ---------- */
  const strip = (line, title) => {
    if (!line) return line;
    const t = title.replace(/\.$/, '');
    return line.replace(new RegExp('^' + t.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '\\.?\\s*'), '');
  };
  const notYetLine = (spec, r) => {
    const fb = spec.feedback || {};
    return (r.key != null && fb.byKey && fb.byKey[r.key]) || r.line || fb.generic || 'Look again at what the question asks.';
  };

  /* The current value of a control's bind on a canvas: canvas.getParam(bind) when the canvas has it, else the state path
     for a dotted bind, else state.params[bind], params.params[bind] or state[bind] */
  const boundValue = (canvas, bind, cspec = {}) => {
    if (!canvas || bind == null) return NaN;
    try {
      if (canvas.getParam) { const v = canvas.getParam(bind); if (v != null) return +v; }
      const st = canvas.get ? canvas.get() || {} : {};
      const path = String(bind).split('.');
      if (path.length > 1) { let o = st; for (const k of path) o = o == null ? undefined : Array.isArray(o) ? o.find(it => it && it.id === k) : o[k]; return o == null ? NaN : +o; } // points.p1.x finds the item by id
      const p = cspec.params || {};
      const v = (st.params || {})[bind] ?? (p.params || {})[bind] ?? st[bind];
      return v == null || typeof v === 'object' ? NaN : +v;
    } catch { return NaN; }
  };

  /* ---------- Screen builder: lesson screens, quiz items and set items ---------- */
  function buildScreen(spec, o) {
    const mode = o.mode || 'lesson';
    const w = spec.widget || (spec.kind === 'longform' ? { ...spec, kind: 'longform' } : null);
    const type = spec.type || (mode === 'lesson' ? 'problem' : 'item');
    const bound = w && (BOUND.has(w.kind) || (w.kind === 'slider' && w.bind) || (w.kind === 'sliders' && (w.sliders || []).some(x => x && x.bind)) || (w.kind === 'place' && w.mode === 'boxes'));
    const el = Z.h(`<section class="lsn-step lsn-t-${Z.esc(type)}"></section>`);
    const add = (html) => { const n = typeof html === 'string' ? Z.h(html) : html; el.append(n); return n; };
    const rng = o.rng || rngFrom(hash((o.key || '') + JSON.stringify(spec.widget || {}).length));
    let canvas = null, born = null, widget = null, cvHost = null, cbar = null, countEl = null, stepper = null;

    if (spec.title && type !== 'title') add(`<h2 class="t-h1 lsn-h">${G().inline(spec.title)}</h2>`);
    const proseSrc = spec.prose || (spec.kind === 'longform' ? spec.prompt : '');
    if (proseSrc) G().prose(proseSrc).split(/(?=<p class|<div class="lsn-code|<ul class="lsn-list|<ol class="lsn-list)/).filter(Boolean).forEach(h => add(h));
    const qLine = spec.question ? `<h2 class="t-h2 lsn-q">${G().inline(spec.question)}<span class="lsn-count tnum" aria-live="polite" hidden></span></h2>` : '';
    const tapHint = () => {
      const k = spec.canvas && spec.canvas.kind;
      if (!bound) return '';
      if (w.kind === 'tap-regions') return k === 'grid' ? 'Tap a cell to shade it' : k === 'venn' ? 'Tap a region to shade it' : k === 'tree' ? 'Tap a branch to pick it' : 'Tap to select';
      if (w.kind === 'drag-point') return 'Drag the point';
      if (w.kind === 'sketch') return 'Drag the control points';
      if (w.kind === 'place') return 'Drag the items into the containers';
      return '';
    };
    /* item 122: Start over only where there is something to put back: a canvas-bound widget, a canvas with controls or a
       draggable point, or a widget whose pieces move (order, place, manipulate, table); not on choice or code screens */
    const cvSpec = spec.canvas || {}, movable = (c) => !!(c && ((c.controls || []).length || ((c.state || {}).points || []).some(p => p && p.drag) || (c.params || {}).drag || (c.state || {}).drag));
    const resettable = w && (bound || movable(cvSpec) || movable(cvSpec.left) || movable(cvSpec.right) || ['order', 'place', 'manipulate', 'table'].includes(w.kind));
    const cbarHTML = (cap) => `<div class="lsn-cbar"><span class="t-caption lsn-cap">${Z.esc(cap || '')}</span>${mode === 'lesson' && resettable ? '<button type="button" class="link-btn lsn-so" disabled>Start over</button>' : ''}</div>`;
    if (bound && qLine) { const q = add(qLine); countEl = q.querySelector('.lsn-count'); }
    if (spec.canvas) {
      if (mode === 'lesson' && (w || spec.steps)) cbar = add(cbarHTML(tapHint()));
      cvHost = add('<div class="lsn-canvas"></div>');
      try {
        canvas = Z.canvas ? Z.canvas.create(cvHost, spec.canvas, { mode, rng, reducedMotion: Z.reducedMotion() }) : null;
        try { born = canvas && canvas.get ? JSON.parse(JSON.stringify(canvas.get() || {})) : null; } catch { born = null; } // item 115: the state as first drawn
        if (!Z.canvas) cvHost.append(Z.h(`<div class="cv cv-missing t-caption">Canvas "${Z.esc(spec.canvas.kind)}" is not available.</div>`));
      } catch (e) { console.error('Canvas ' + spec.canvas.kind + ' failed', e); canvas = null; cvHost.innerHTML = `<div class="cv cv-missing t-caption">Canvas "${Z.esc(spec.canvas.kind)}" could not be drawn.</div>`; }
      if (spec.canvas.controls && spec.canvas.controls.length) {
        /* Explore controls: each slider drives canvas.setParam(bind, v) (else state.params[bind], or the state path for a
           dotted bind). `start` sets the opening value and is applied to the canvas; without it the slider opens at the
           bound value's current value (a number-line point's x, an area split, a param), else at min. */
        const shown = (c, v) => G().fmtAs(v, c.format, c.decimals);
        const drive = (c, v) => {
          if (!canvas) return;
          try {
            const listPath = /^(points|intervals|arrows|markers|vectors|segments|pointers)\./.test(String(c.bind)); // an item by id: points.p1.x
            if (canvas.setParam && !listPath) canvas.setParam(c.bind, v);
            else if (String(c.bind).includes('.')) canvas.set(String(c.bind).split('.').reduceRight((acc, k) => ({ [k]: acc }), v), { instant: true });
            else canvas.set({ params: { [c.bind]: v } }, { instant: true });
          } catch (err) { console.error(err); }
        };
        const opening = (c) => {
          if (c.start != null || c.value != null) return +(c.start ?? c.value);
          const cur = boundValue(canvas, c.bind, spec.canvas);
          return Number.isFinite(cur) ? Math.min(c.max ?? 1, Math.max(c.min ?? 0, cur)) : +(c.min ?? 0);
        };
        const vals = spec.canvas.controls.map(opening);
        const ctl = add(`<div class="lsn-controls">${spec.canvas.controls.map((c, i) => `<label class="lsn-ctl"><span class="t-label">${G().inline(c.label || c.bind)}</span><input type="range" class="slider" min="${c.min ?? 0}" max="${c.max ?? 1}" step="${c.step ?? 0.01}" value="${vals[i]}" data-i="${i}"><output class="tnum">${shown(c, vals[i])}</output></label>`).join('')}</div>`);
        spec.canvas.controls.forEach((c, i) => { if (c.start != null || c.value != null) drive(c, vals[i]); });
        ctl.addEventListener('input', (e) => {
          const r = e.target.closest('input'); if (!r || !canvas) return;
          const c = spec.canvas.controls[+r.dataset.i], v = +r.value;
          r.nextElementSibling.textContent = shown(c, v);
          drive(c, v);
        });
      }
    }
    if (type === 'demonstrate' && Array.isArray(spec.steps) && spec.steps.length) {
      stepper = add(`<div class="lsn-demo"><p class="t-body lsn-demo-cap" aria-live="polite"></p>
        <div class="lsn-stepper"><button type="button" class="btn secondary round lsn-demo-prev" aria-label="Previous step">${Z.icon('chevronL')}</button>
        <span class="dots" aria-hidden="true">${spec.steps.map(() => '<i></i>').join('')}</span>
        <button type="button" class="btn secondary round lsn-demo-next" aria-label="Next step">${Z.icon('chevronR')}</button></div></div>`);
    }
    if (!bound && qLine) { const q = add(qLine); countEl = q.querySelector('.lsn-count'); }
    const wHost = w ? add('<div class="lsn-widget"></div>') : null;
    if (w && !spec.canvas && mode === 'lesson' && (w.kind === 'order' || w.kind === 'place' || w.kind === 'manipulate')) { cbar = Z.h(cbarHTML('')); wHost.before(cbar); }

    const listeners = [];
    const count = (text) => { if (!countEl) return; countEl.hidden = text == null || text === ''; countEl.textContent = text ?? ''; };
    /* tap-regions running count: "3 shaded", "2 of 3 shaded" in count mode, with the authored countWord */
    const tapCount = (n) => { const word = w.countWord || (spec.canvas && spec.canvas.kind === 'grid' ? 'shaded' : 'selected'); return Number.isInteger(w.count) ? `${n} of ${w.count} ${word}` : `${n} ${word}`; };
    if (w) {
      try {
        widget = Z.widgets ? Z.widgets.create(wHost, w, { canvas, rng, reducedMotion: Z.reducedMotion(), mode: mode === 'quiz' ? 'set' : mode, count, screen: spec, draftKey: o.draftKey || null }) : null;
        if (!Z.widgets) wHost.append(Z.h(`<div class="wd wd-missing t-caption">Widget "${Z.esc(w.kind)}" is not available.</div>`));
      } catch (e) { console.error('Widget ' + w.kind + ' failed', e); widget = null; wHost.innerHTML = `<div class="wd wd-missing t-caption">Widget "${Z.esc(w.kind)}" could not be drawn.</div>`; }
      if (widget) widget.onChange((d) => {
        if (w.kind === 'tap-regions') { const v = widget.value(); const n = Array.isArray(v) ? v.length : 0; count(tapCount(n)); }
        listeners.forEach(f => f(d));
      });
      if (widget && w.kind === 'tap-regions') count(tapCount(0));
    }

    /* Canvas states: initial (with the optional enter patch), reset, reveal, explanation */
    const initial = Object.assign({}, (spec.canvas && spec.canvas.state) || {}, (spec.canvas && spec.canvas.enter) || {});
    /* item 115: a key the author did not set goes back to what the canvas drew first (its own defaults), not to empty */
    const resetFor = (cur, init, first) => {
      const patch = {};
      Object.keys(cur || {}).forEach(k => { patch[k] = k in init ? init[k] : first && k in first ? first[k] : (Array.isArray(cur[k]) ? [] : cur[k] && typeof cur[k] === 'object' ? {} : null); });
      return Object.assign(patch, init);
    };
    const resetCanvas = () => {
      if (!canvas || !canvas.set) return;
      let cur = {}; try { cur = canvas.get ? canvas.get() || {} : {}; } catch { cur = {}; }
      /* a pair resets each side to its own authored state */
      const patch = canvas.kind === 'pair'
        ? { left: resetFor(cur.left, Object.assign({}, (spec.canvas.left || {}).state, initial.left), born && born.left), right: resetFor(cur.right, Object.assign({}, (spec.canvas.right || {}).state, initial.right), born && born.right), caption: initial.caption || '' }
        : resetFor(cur, initial, born);
      if (canvas.clearTrace) try { canvas.clearTrace(); } catch { /* no trails */ }
      try { canvas.set(patch); } catch (e) { console.error(e); }
    };
    let demoAt = 0;
    const demo = (k) => {
      if (!stepper) return;
      demoAt = Math.max(0, Math.min(spec.steps.length - 1, k));
      const s = spec.steps[demoAt];
      if (canvas && canvas.set) {
        try {
          resetCanvas();
          spec.steps.slice(0, demoAt).forEach(p => p.canvas && canvas.set(p.canvas, { instant: true }));
          if (s.canvas) canvas.set(s.canvas);
        } catch (e) { console.error(e); }
      }
      stepper.querySelector('.lsn-demo-cap').innerHTML = G().inline(s.caption || '');
      stepper.querySelectorAll('.dots i').forEach((d, i) => { d.className = i < demoAt ? 'ok' : i === demoAt ? 'cur' : ''; });
      stepper.querySelector('.lsn-demo-prev').disabled = demoAt === 0;
      stepper.querySelector('.lsn-demo-next').disabled = demoAt === spec.steps.length - 1;
    };
    if (stepper) {
      stepper.querySelector('.lsn-demo-prev').addEventListener('click', () => demo(demoAt - 1));
      stepper.querySelector('.lsn-demo-next').addEventListener('click', () => demo(demoAt + 1));
    }

    const graded = !!widget;
    const step = {
      spec, el, type, mode, widget, canvas, cbar,
      kind: mode === 'quiz' ? 'quiz' : graded ? 'task' : 'read',
      key: o.key,
      onChange: (f) => listeners.push(f),
      ready: () => !!widget && (widget.ready ? !!widget.ready() : !empty(widget.value())),
      dirty: () => !!widget && (widget.dirty ? !!widget.dirty() : !empty(widget.value())),
      lock: () => widget && widget.lock(),
      grade: async () => {
        if (!widget) return { ok: true, key: null };
        try { return (await widget.grade()) || { ok: false, key: null }; } catch (e) { console.error(e); return { ok: false, key: 'error', line: 'This answer could not be checked.' }; }
      },
      mark(r) { if (!widget) return; widget.markGraded(r); if (!r.ok && !r.final && widget.showWhy) { try { widget.showWhy(r.key); } catch (e) { console.error(e); } } },
      clear() { widget && widget.unlock(); },
      reset() { widget && widget.reset(); resetCanvas(); if (w && w.kind === 'tap-regions') count(tapCount(0)); },
      reveal() {
        if (!widget) return;
        widget.reveal();
        if (canvas && spec.explain && spec.explain.canvas) { try { canvas.set(spec.explain.canvas); } catch (e) { console.error(e); } }
      },
      point(h) {
        if (canvas && h && h.highlight && canvas.highlight) { try { canvas.highlight(h.highlight, true); } catch (e) { console.error(e); } o.into && o.into(cvHost); return; }
        o.pointEl && o.pointEl(cvHost || (widget && widget.el));
      },
      hasPoint: (h) => !!(h && (h.rung === 'point' || h.highlight)),
      explainText: () => (spec.explain && spec.explain.text) || (spec.feedback && spec.feedback.correct) || '',
      explainCanvas(host) {
        if (!spec.canvas || !Z.canvas) return null;
        let state = {};
        try { state = canvas && canvas.get ? canvas.get() || {} : Object.assign({}, initial); } catch { state = Object.assign({}, initial); }
        const patch = (spec.explain && spec.explain.canvas) || {};
        const merged = Z.canvas.merge ? Z.canvas.merge(state, patch) : Object.assign({}, state, patch);
        /* derive runs again on the explained state, so derived points and captions follow the patch */
        try { return Z.canvas.create(host, { ...spec.canvas, state: merged }, { mode: 'static', reducedMotion: true }) /* the whole spec, so a pair keeps stack, active and shareMargins (item 194) */; } catch (e) { console.error(e); return null; }
      },
      answer() {
        if (!widget) return true;
        const v = widget.answer ? widget.answer() : G().correctValue(w);
        if (v == null) return false;
        widget.set(v);
        return true;
      },
      enter(later) {
        if (stepper) demo(0);
        if (spec.canvas && spec.canvas.enter && canvas && canvas.set) later(() => { try { canvas.set(spec.canvas.enter); } catch (e) { console.error(e); } }, Z.reducedMotion() ? 0 : 350);
      },
      focusInput() { if (widget && /numeric|expression|table|code|longform/.test(w.kind)) widget.focus(); },
      pick: (i) => widget && widget.pick && widget.pick(i),
      destroy() { try { widget && widget.destroy(); } catch (e) { console.error(e); } try { canvas && canvas.destroy && canvas.destroy(); } catch (e) { console.error(e); } },
    };
    return step;
  }

  /* Explanation modal: the authored text and a copy of the canvas in the explained state */
  const openExplain = (step) => {
    const box = Z.h(`<div class="lsn-sheet lsn-why"><h2 class="t-sheet-title">Explanation</h2><div class="lsn-why-b">${G().prose(step.explainText())}</div><div class="lsn-why-cv"></div></div>`);
    const close = Z.sheet(box, { label: 'Explanation' });
    const cv = box.querySelector('.lsn-why-cv');
    const inst = step.explainCanvas(cv);
    if (!inst && !cv.children.length) cv.remove();
    Z.mathify(box);
    return close;
  };

  /* ---------- The lesson ---------- */
  function mount(host, opts = {}) {
    const course = opts.course || 'conditional';
    const lessonArg = opts.lesson || 'l3-shrinking';
    const lessonId = typeof lessonArg === 'object' ? lessonArg.id : lessonArg;
    let alive = true, inner = null;
    host.innerHTML = `<div class="lsn lsn-loading" data-track="prob"><div class="lsn-load t-caption">Loading the lesson</div></div>`;
    const lessonP = typeof lessonArg === 'object' ? Promise.resolve(lessonArg) : loadLesson(course, lessonId);
    lessonP.then((L) => { if (alive) inner = run(host, L, course, opts.start); }).catch((e) => {
      if (!alive) return;
      console.warn(e);
      host.innerHTML = `<div class="lsn lsn-missing" data-track="prob"><main class="lsn-frame"><div class="lsn-scroll"><div class="lsn-col"><section class="lsn-step lsn-title">
        <div class="t-overline lsn-over">Not yet written</div><h1 class="t-lesson-title">This lesson is not ready</h1>
        <p class="t-prose">The file for ${Z.esc(course)}/${Z.esc(lessonId)} could not be loaded. Use the course map to pick another lesson.</p>
        <a class="btn" href="#course/${Z.esc(course)}">Back to the course</a></section></div></div></main></div>`;
    });
    return () => { alive = false; if (inner) inner(); };
  }

  function run(root, LSN, course, start) {
    const { h, icon } = Z;
    const lessonId = LSN.id;
    const info = courseInfo(course, lessonId);
    const screens = LSN.screens || [];
    const quizSpec = LSN.quiz || [];
    const N = screens.length + (LSN.summary ? 1 : 0);
    const SUMMARY = LSN.summary ? screens.length : -1;
    const gradedLesson = screens.filter(s => s.widget).length;
    const GRADED = gradedLesson + quizSpec.length;
    const rm = () => Z.reducedMotion();
    let alive = true, gen = 0;
    const timers = new Set();
    const later = (fn, ms) => { const id = setTimeout(() => { timers.delete(id); if (alive) fn(); }, ms); timers.add(id); return id; };
    const clearTimers = () => { timers.forEach(clearTimeout); timers.clear(); };
    let xpGen = 0;
    const counter = (el, from, to, ms, f = fmt, tok = () => gen) => {
      const my = tok();
      if (rm() || ms <= 0) { el.textContent = f(to); return Promise.resolve(); }
      return new Promise(res => {
        const t0 = performance.now();
        const tick = (now) => {
          if (!alive || my !== tok()) return res();
          const p = Math.min(1, (now - t0) / ms);
          const e = p < 0.8 ? p / 0.8 * 0.9 : 0.9 + (1 - Math.pow(1 - (p - 0.8) / 0.2, 3)) * 0.1;
          el.textContent = f(from + (to - from) * e);
          if (p < 1) requestAnimationFrame(tick); else res();
        };
        requestAnimationFrame(tick);
      });
    };

    const S = { phase: 'lesson', i: 0, q: 0, st: 'read', xp: 0, checks: 0, okChecks: 0, anyCheck: false, results: {}, quiz: [], attempts: 0, rung: 0, t0: Date.now(), elapsed: null, streakDone: false, finished: false, loggedAt: Date.now() };
    let saved = null;
    if (start == null || start === '' || start === 'resume') {
      saved = position.get(course, lessonId);
      if (typeof saved === 'number') saved = { phase: 'lesson', i: saved };
      if (saved && typeof saved === 'object' && (saved.phase === 'lesson' || saved.phase === 'quiz')) {
        ['xp', 'checks', 'okChecks', 'anyCheck', 'results', 'quiz'].forEach(k => { if (saved[k] != null) S[k] = saved[k]; });
        S.t0 = Date.now() - (saved.spent || 0) * 1000;
      } else saved = null;
    } else if (start === 'quiz' || start === 'done') {
      const p = position.get(course, lessonId);
      if (p && typeof p === 'object') ['xp', 'checks', 'okChecks', 'anyCheck', 'results', 'quiz'].forEach(k => { if (p[k] != null) S[k] = p[k]; });
      if (p && p.spent) S.t0 = Date.now() - p.spent * 1000;
      S.anyCheck = true;
      // Opening .../done directly shows the celebration; it records the finish only when the quiz was really played
      if (start === 'done' && !(p && p.phase === 'quiz' && (p.q || 0) >= quizSpec.length)) S.finished = true;
    }

    const before = daySummary();
    root.innerHTML = '';
    const app = h(`<div class="lsn" data-track="${Z.esc(info.track)}">
      <div class="lsn-wash" aria-hidden="true"></div>
      <header class="lsn-top">
        <button type="button" class="icon-btn lsn-close" aria-label="Close lesson and return to the course map">${icon('close')}</button>
        <div class="lsn-prog">
          <div class="bar lsn-bar" role="progressbar" aria-label="Lesson progress" aria-valuemin="0" aria-valuemax="${N}" aria-valuenow="0"><i></i></div>
          ${quizSpec.length ? '<span class="lsn-qpill" title="Lesson quiz" aria-hidden="true"></span>' : ''}
        </div>
        <div class="lsn-stats">
          <span class="lsn-xp" title="XP this lesson"><span class="lsn-xp-n tnum">0</span>${Z.spark(false)}<span class="sr-only"> XP this lesson</span></span>
          <span class="lsn-streak" title="Streak"${before.off ? ' hidden' : ''}><span class="lsn-odo tnum"><span>${before.streak}</span></span>${Z.bolt(before.todayDone)}<span class="sr-only"> day streak</span></span>
        </div>
      </header>
      <main class="lsn-frame">
        <div class="lsn-utils">
          <button type="button" class="icon-btn lsn-flag" aria-label="Report a problem with this screen">${icon('flag', 'sm')}</button>
          <button type="button" class="icon-btn lsn-snd" aria-pressed="false" aria-label="Sound">${icon('mute', 'sm')}</button>
        </div>
        <div class="lsn-scroll"><div class="lsn-col" tabindex="-1"></div></div>
        <div class="lsn-foot">
          <div class="lsn-verdict" aria-live="polite"></div>
          <div class="lsn-solve" hidden><button type="button" class="link-btn lsn-solve-btn">Show solution</button></div>
          <div class="lsn-actions">
            <button type="button" class="btn round secondary lsn-hint" aria-label="Get help">${icon('bulb')}</button>
            <button type="button" class="btn secondary lsn-sec" hidden></button>
            <button type="button" class="btn lsn-primary">Continue</button>
          </div>
        </div>
      </main>
    </div>`);
    root.append(app);
    const $ = (s) => app.querySelector(s);
    const col = $('.lsn-col'), scroller = $('.lsn-scroll'), verdict = $('.lsn-verdict');
    const primary = $('.lsn-primary'), sec = $('.lsn-sec'), hintBtn = $('.lsn-hint'), solveWrap = $('.lsn-solve');
    const barFill = $('.lsn-bar > i'), bar = $('.lsn-bar'), qpill = $('.lsn-qpill');
    const xpN = $('.lsn-xp-n'), sparkEl = $('.lsn-xp .spark');
    const odo = $('.lsn-odo'), boltEl = $('.lsn-streak .bolt'), sndBtn = $('.lsn-snd');
    let step = null, next = null, nextP = null;

    let showGen = 0;
    const stopShows = () => { showGen++; };
    const into = (el) => { if (el && el.isConnected) el.scrollIntoView({ block: 'nearest', behavior: rm() ? 'auto' : 'smooth' }); };
    const pointEl = (el) => {
      if (!el) return;
      el.classList.remove('lsn-pointed'); void el.offsetWidth; el.classList.add('lsn-pointed');
      into(el); later(() => el.classList.remove('lsn-pointed'), 3200);
    };
    const changed = () => {
      if (!step) return;
      if (S.st === 'idle' || S.st === 'engaged') S.st = step.ready() ? 'engaged' : 'idle';
      refresh();
    };

    /* ----- chrome ----- */
    const setProgress = () => {
      const frac = S.phase === 'lesson' ? S.i / N : 1;
      barFill.style.width = (frac * 100).toFixed(3) + '%';
      bar.setAttribute('aria-valuenow', String(S.phase === 'lesson' ? S.i : N));
      if (qpill) { qpill.classList.toggle('cur', S.phase === 'quiz'); qpill.classList.toggle('ok', S.phase === 'complete'); }
    };
    const setXP = (to, ms = 400) => {
      const from = S.xpShown || 0; S.xpShown = to;
      sparkEl.classList.toggle('on', to > 0);
      xpGen++;
      counter(xpN, from, to, ms, fmt, () => xpGen);
    };
    const addXP = (n) => { S.xp += n; setXP(S.xp); };
    const setFrame = (k) => { app.classList.remove('is-ok', 'is-no'); if (k) app.classList.add('is-' + k); };
    const chip = (kind, title, line, xp, extra = '') => {
      const ic = { ok: 'check', no: 'cross', rev: 'bulb' }[kind];
      verdict.innerHTML = `<div class="lsn-chip is-${kind}"><span class="lsn-chip-ic">${icon(ic, 'sm')}</span><div class="lsn-chip-tx"><div class="lsn-chip-h"><b>${Z.esc(title)}</b>${xp ? `<span class="lsn-chip-xp tnum">${Z.spark(true)}+${xp} XP</span>` : ''}</div>${line ? `<span>${G().inline(strip(line, title))}</span>` : ''}${extra ? `<span class="lsn-chip-x">${extra}</span>` : ''}</div></div>`;
    };
    const clearChip = () => { verdict.innerHTML = ''; };
    const updateSO = () => {
      const so = col.querySelector('.lsn-so'); if (!so || !step) return;
      so.disabled = !(['idle', 'engaged', 'no'].includes(S.st) && step.dirty());
    };

    /* Buttons follow the state machine in design-research 5.4 */
    const refresh = () => {
      const task = step && (step.kind === 'task' || step.kind === 'quiz');
      const quiz = S.phase === 'quiz';
      const hasHints = !!(step && step.spec && step.spec.hints && step.spec.hints.length);
      let p = { label: 'Continue', cls: '', disabled: false, hidden: false }, s = null, hint = 'hidden';
      const helpOpen = task && !quiz && S.anyCheck && hasHints;
      switch (S.st) {
        case 'read': break;
        case 'idle': p = { label: 'Check', disabled: true }; hint = quiz || !hasHints ? 'hidden' : S.anyCheck ? 'on' : 'off'; if (helpOpen) s = 'Get help'; break;
        case 'engaged': p = { label: 'Check', disabled: false }; hint = quiz || !hasHints ? 'hidden' : S.anyCheck ? 'on' : 'off'; if (helpOpen) s = 'Get help'; break;
        case 'eval': p = { label: 'Check', disabled: true }; hint = quiz || !hasHints ? 'hidden' : 'off'; if (helpOpen) s = 'Get help'; break;
        case 'ok': p = { label: 'Continue', cls: 'correct' }; s = 'Why?'; break;
        case 'no': p = { label: 'Try again', cls: 'notyet' }; s = hasHints ? 'Get help' : 'Why?'; hint = hasHints ? 'on' : 'hidden'; break;
        case 'rev': p = { label: 'Continue' }; s = 'Why?'; break;
        case 'qok': p = { label: 'Continue', cls: 'correct' }; s = 'Why?'; break;
        case 'qno': p = { label: 'Continue', cls: 'notyet' }; s = 'Why?'; break;
        case 'play': p = { label: 'Continue', hidden: true }; break;
        case 'done': p = { label: next ? 'Next' : 'Done' }; s = next ? 'Done' : null; break;
      }
      primary.textContent = p.label;
      primary.className = 'btn lsn-primary' + (p.cls ? ' ' + p.cls : '');
      primary.disabled = !!p.disabled;
      primary.classList.toggle('lsn-hide', !!p.hidden);
      primary.setAttribute('aria-hidden', String(!!p.hidden));
      primary.tabIndex = p.hidden ? -1 : 0;
      if (S.st === 'eval' && S.slow) primary.textContent = 'Checking';
      sec.hidden = !s; sec.textContent = s || '';
      sec.classList.toggle('is-help', s === 'Get help');
      hintBtn.hidden = !task || hint === 'hidden';
      hintBtn.disabled = hint === 'off';
      hintBtn.setAttribute('aria-label', hint === 'off' ? 'Hints open after your first check' : 'Get help');
      app.classList.toggle('lsn-two', !!s);
      solveWrap.hidden = !(S.st === 'no' && S.attempts >= 2 && S.phase === 'lesson');
      updateSO();
    };

    /* ----- screens ----- */
    const swap = async (build) => {
      gen++;
      const old = col.firstElementChild;
      if (old && !rm()) { try { await old.animate([{ opacity: 1 }, { opacity: 0 }], { duration: 120, easing: 'cubic-bezier(0.3, 0, 0.8, 0.15)', fill: 'forwards' }).finished; } catch (e) { /* interrupted */ } }
      if (!alive) return null;
      if (step && step.destroy) step.destroy();
      col.innerHTML = '';
      const el = build();
      col.append(el);
      Z.mathify(el);
      scroller.scrollTop = 0;
      if (!rm()) el.animate([{ opacity: 0, transform: 'translateY(8px)' }, { opacity: 1, transform: 'none' }], { duration: 200, easing: 'cubic-bezier(0.05, 0.7, 0.1, 1)' });
      return el;
    };
    const wireStep = () => {
      const so = col.querySelector('.lsn-so');
      if (so) so.addEventListener('click', () => {
        if (!['idle', 'engaged', 'no'].includes(S.st)) return;
        stopShows(); clearPoints();
        step.clear(); step.reset();
        setFrame(null); clearChip(); S.st = 'idle'; refresh();
      });
    };
    let busy = false;
    const enterStep = async (factory) => {
      busy = true; stopShows();
      clearChip(); setFrame(null);
      S.attempts = 0; S.rung = 0;
      let made = null;
      const el = await swap(() => { made = factory(); return made.el; });
      busy = false;
      if (!el) return;
      step = made;
      if (step.onChange) step.onChange(changed);
      S.st = step.kind === 'read' ? 'read' : 'idle';
      wireStep(); refresh(); setProgress();
      col.focus({ preventScroll: true });
      if (matchMedia('(min-width: 768px)').matches && step.focusInput) step.focusInput();
      step.enter && step.enter(later);
    };
    const ctxFor = (key, mode) => ({ mode, key, into, pointEl, rng: rngFrom(hash(course + '/' + lessonId + '/' + key)), draftKey: `${course}/${lessonId}/${key}` });
    const titleStep = (spec) => {
      const meta = info.level && info.n ? `Level ${info.level} · Lesson ${info.n}` : (info.name || 'Lesson');
      const el = h(`<section class="lsn-step lsn-title">
        <div class="lsn-title-art" data-track="${Z.esc(info.track)}">${window.ZQArt ? window.ZQArt(info.art, { label: 'Course art' }) : ''}</div>
        <div class="t-overline lsn-over">${Z.esc(meta)}</div>
        <h1 class="t-lesson-title">${G().inline(spec.title || LSN.title)}</h1>
        ${G().prose(spec.prose || '')}
        <p class="t-caption lsn-meta">${icon('clock', 'xs')} About ${LSN.minutes || 12} minutes${quizSpec.length ? `, then a ${quizSpec.length}-question quiz` : ''}</p>
      </section>`);
      return { el, kind: 'read', type: 'title', spec, ready: () => false, dirty: () => false, destroy() {} };
    };
    const summaryStep = () => {
      const sm = LSN.summary || {};
      const f = sm.formula;
      const el = h(`<section class="lsn-step lsn-sum">
        <div class="t-overline lsn-over">Summary</div>
        <h1 class="t-lesson-title">What you found</h1>
        <ol class="lsn-ideas">${(sm.ideas || []).map((t, i) => `<li><span class="lsn-idea-n">${i + 1}</span><div class="t-body">${G().prose(t, 'lsn-idea-p')}</div></li>`).join('')}</ol>
        ${f ? `<div class="lsn-card">
          <div class="lsn-card-top"><span class="t-overline">${G().inline(f.name || 'Formula')}</span><span class="lsn-saved t-caption">${icon('book', 'xs')} Saved to Notebook</span></div>
          <div class="lsn-card-f">${Z.tex(f.tex || '', true)}</div>
          ${f.note ? `<p class="t-caption lsn-card-n">${G().inline(f.note)}</p>` : ''}
        </div>` : ''}
        ${sm.trap ? `<p class="t-body lsn-trap"><b>Common trap.</b> ${G().inline(sm.trap)}</p>` : ''}
        ${quizSpec.length ? `<p class="t-caption lsn-next">Next: a ${quizSpec.length}-question quiz. No hints, one try each.</p>` : ''}
      </section>`);
      if (f && !S.noteSaved) {
        S.noteSaved = true;
        const r = st('notebook.add', { course, lesson: lessonId, name: f.name, tex: f.tex, note: f.note || '', at: Date.now() });
        if (r === undefined && !stFn('notebook.add')) { const nb = Z.store.get('player.notebook', []); if (!nb.some(x => x.course === course && x.lesson === lessonId)) { nb.push({ course, lesson: lessonId, name: f.name, tex: f.tex, note: f.note || '', at: Date.now() }); Z.store.set('player.notebook', nb); } }
      }
      return { el, kind: 'read', type: 'summary', ready: () => false, dirty: () => false, destroy() {} };
    };
    const lessonFactory = (i) => () => {
      if (i === SUMMARY) return summaryStep();
      const spec = screens[i];
      if (spec.type === 'title') return titleStep(spec);
      return buildScreen(spec, ctxFor('s' + i, 'lesson'));
    };
    const enterLesson = (i) => { S.phase = 'lesson'; S.i = i; setProgress(); return enterStep(lessonFactory(i)); };
    const quizHead = () => `<div class="lsn-qhead"><span class="t-overline">Lesson quiz</span><span class="dots" aria-hidden="true">${quizSpec.map((_, j) => `<i class="${S.quiz[j] === 'ok' ? 'ok' : S.quiz[j] === 'bad' ? 'bad' : j === S.q ? 'cur' : ''}"></i>`).join('')}</span><span class="t-caption lsn-qof">Question ${S.q + 1} of ${quizSpec.length} · No hints, one try</span></div>`;
    const enterQuiz = (q) => {
      S.phase = 'quiz'; S.q = q; setProgress();
      return enterStep(() => { const s = buildScreen(quizSpec[q], ctxFor('q' + q, 'quiz')); s.el.prepend(h(quizHead())); return s; });
    };
    const syncDots = () => col.querySelectorAll('.lsn-qhead .dots i').forEach((d, j) => { d.className = S.quiz[j] === 'ok' ? 'ok' : S.quiz[j] === 'bad' ? 'bad' : j === S.q ? 'cur' : ''; });

    /* ----- Check and its outcomes ----- */
    let checking = null;
    const check = () => {
      if (S.st !== 'engaged') return Promise.resolve(null);
      S.st = 'eval'; S.slow = false; step.lock(); refresh();
      const slow = later(() => { if (S.st === 'eval') { S.slow = true; refresh(); } }, 400);
      checking = new Promise(res => later(() => grade().then((r) => { clearTimeout(slow); S.slow = false; res(r); }), 90));
      return checking;
    };
    const scrollGraded = () => into(col.querySelector('.wd-accept:not([hidden])') || col.querySelector('.opt.correct, .opt.wrong, .opt.wd-rev, .field.correct, .field.wrong, .field.wd-rev, .wd-line.bad, .wd-res'));
    const skillsOf = (spec) => spec.skills || LSN.skills || [];
    const grade = async () => {
      stopShows();
      const spec = step.spec;
      const r = await step.grade();
      if (!alive) return r;
      if (r && r.pending) { step.clear(); S.st = step.ready() ? 'engaged' : 'idle'; refresh(); return r; }
      S.checks++; S.anyCheck = true;
      if (S.phase === 'quiz') {
        r.final = true;
        S.quiz[S.q] = r.ok ? 'ok' : 'bad';
        S.results['q' + S.q] = { first: r.ok, xp: r.ok ? XP.quiz : 0, key: r.key ?? null, quiz: true };
        if (r.ok) S.okChecks++;
        step.mark(r); setFrame(r.ok ? 'ok' : 'no'); syncDots();
        if (r.ok) { Z.sound('correct'); Z.haptic(10); } else Z.sound('notyet');
        later(() => r.ok ? chip('ok', 'Correct.', spec.feedback && spec.feedback.correct, XP.quiz) : chip('no', 'Not quite right.', notYetLine(spec, r)), 80);
        if (r.ok) later(() => addXP(XP.quiz), 160);
        S.st = r.ok ? 'qok' : 'qno'; refresh();
        later(scrollGraded, 140);
        return r;
      }
      const base = { course, lesson: lessonId, screen: S.i, id: spec.id || 's' + S.i, type: spec.type, ok: !!r.ok, firstTry: !!r.ok && S.attempts === 0, attempt: S.attempts + 1, key: r.key ?? null, revealed: false, skills: skillsOf(spec), difficulty: spec.difficulty || 1, mode: 'lesson' };
      if (r.ok) {
        S.okChecks++;
        const local = S.attempts === 0 ? XP.first : XP.retry;
        const gain = xpOf(st('screenGraded', base), local);
        S.results['s' + S.i] = { first: S.attempts === 0, xp: gain };
        S.st = 'ok'; step.mark(r); setFrame('ok');
        Z.sound('correct'); Z.haptic(10);
        later(() => chip('ok', S.attempts === 0 ? 'Correct.' : "That's it.", spec.feedback && spec.feedback.correct, gain), 80);
        if (gain) later(() => addXP(gain), 160);
      } else {
        S.attempts++;
        st('screenGraded', base);
        S.st = 'no'; setFrame('no'); Z.sound('notyet');
        step.mark(r);
        later(() => chip('no', S.attempts === 1 ? 'Not quite right.' : 'Give it another shot.', notYetLine(spec, r)), 80);
      }
      refresh();
      later(scrollGraded, 140);
      return r;
    };
    const clearPoints = () => { col.querySelectorAll('.lsn-pointed').forEach(n => n.classList.remove('lsn-pointed')); if (step && step.canvas && step.canvas.highlight && step.spec && step.spec.hints) { step.spec.hints.forEach(hh => { if (hh.highlight) { try { step.canvas.highlight(hh.highlight, false); } catch (e) { /* canvas without highlight off */ } } }); } };
    const tryAgain = () => {
      stopShows(); clearPoints();
      step.clear();
      setFrame(null); clearChip();
      S.st = step.ready() ? 'engaged' : 'idle'; refresh();
      if (step.focusInput) step.focusInput();
    };
    const reveal = () => {
      if (S.phase !== 'lesson' || !step || step.kind !== 'task') return;
      stopShows(); clearPoints();
      if (!rm()) { app.classList.add('lsn-revealing'); later(() => app.classList.remove('lsn-revealing'), 700); }
      step.clear(); step.reveal(); step.lock();
      S.results['s' + S.i] = { first: false, xp: 0, revealed: true };
      st('screenGraded', { course, lesson: lessonId, screen: S.i, id: step.spec.id || 's' + S.i, type: step.spec.type, ok: false, firstTry: false, attempt: S.attempts + 1, key: null, revealed: true, skills: skillsOf(step.spec), difficulty: step.spec.difficulty || 1, mode: 'lesson' });
      setFrame(null);
      chip('rev', 'Solution', step.spec.feedback && step.spec.feedback.correct, 0, 'No XP for this screen. It returns in your Redo queue.');
      S.st = 'rev'; refresh();
      later(scrollGraded, 140);
    };
    const savePosition = () => {
      if (S.phase === 'complete') { position.set(course, lessonId, null); return; }
      const done = ['ok', 'rev', 'qok', 'qno'].includes(S.st) || (S.st === 'read');
      let phase = S.phase, i = S.i, q = S.q;
      if (phase === 'lesson' && done) { i++; if (i >= N) { phase = 'quiz'; q = 0; } }
      else if (phase === 'quiz' && ['qok', 'qno'].includes(S.st)) q++;
      if (phase === 'lesson' && i === 0) { position.set(course, lessonId, null); return; }
      position.set(course, lessonId, { phase, i, q, xp: S.xp, checks: S.checks, okChecks: S.okChecks, anyCheck: S.anyCheck, results: S.results, quiz: S.quiz, spent: Math.round((Date.now() - S.t0) / 1000), at: Date.now() });
    };
    const logHours = () => {
      const minutes = Math.round((Date.now() - S.loggedAt) / 60000);
      if (minutes < 1) return;
      S.loggedAt = Date.now();
      st('hours.log', { date: ymd(), block: 'main', minutes, source: `lesson:${course}/${lessonId}` });
    };
    const advance = () => {
      if (S.phase === 'lesson') {
        const p = S.i < N - 1 ? enterLesson(S.i + 1) : quizSpec.length ? enterQuiz(0) : enterComplete();
        later(savePosition, 0);
        return p;
      }
      if (S.phase === 'quiz') { const p = S.q < quizSpec.length - 1 ? enterQuiz(S.q + 1) : enterComplete(); later(savePosition, 0); return p; }
      if (S.phase === 'complete') return finish(!!next);
      return Promise.resolve();
    };
    const onPrimary = () => {
      if (primary.disabled || S.st === 'play' || busy) return Promise.resolve();
      if (S.st === 'idle' || S.st === 'engaged') return check();
      if (S.st === 'no') { tryAgain(); return Promise.resolve(); }
      return advance();
    };

    /* ----- Sheets: hints, explanation, report ----- */
    const openHelp = () => {
      const hints = step && step.spec && step.spec.hints;
      if (!hints || !hints.length || S.phase !== 'lesson') return;
      S.rung = Math.max(1, S.rung);
      const n = hints.length;
      const box = h('<div class="lsn-sheet"></div>');
      const draw = () => {
        box.innerHTML = `<h2 class="t-sheet-title">Get help</h2>
          <p class="t-body lsn-sheet-sub">${n === 1 ? 'One hint' : n === 2 ? 'Two hints' : 'Three hints'}, from a nudge to the first step. Hints never cost XP.</p>
          <ol class="lsn-rungs">${hints.map((x, i) => `<li class="${i < S.rung ? 'on' : ''}"><span class="lsn-rung-n">${i + 1}</span><div>
            <div class="t-overline">${RUNG[x.rung] || ['Nudge', 'Point', 'Step'][i]}</div>
            ${i < S.rung ? `<p class="t-body">${G().inline(x.text)}</p>${step.hasPoint(x) ? `<button type="button" class="btn secondary lsn-showme" data-i="${i}">${icon('target', 'sm')} Show me on the diagram</button>` : ''}` : '<p class="t-body lsn-locked">Open the hint above first.</p>'}
          </div></li>`).join('')}</ol>
          <div class="lsn-sheet-act">${S.rung < n ? '<button type="button" class="btn" data-next>Next hint</button>' : '<button type="button" class="btn secondary" data-solve>Show solution</button>'}<button type="button" class="btn secondary" data-close>Back to the problem</button></div>`;
        Z.mathify(box);
      };
      draw();
      const close = Z.sheet(box, { label: 'Hints' });
      box.addEventListener('click', (e) => {
        if (e.target.closest('[data-next]')) { S.rung = Math.min(n, S.rung + 1); draw(); const b = box.querySelector('[data-next], [data-solve]'); b && b.focus(); }
        else if (e.target.closest('.lsn-showme')) { const hh = hints[+e.target.closest('.lsn-showme').dataset.i]; close(); later(() => step.point && step.point(hh), 300); }
        else if (e.target.closest('[data-solve]')) { close(); later(reveal, 200); }
      });
    };
    const openWhy = () => { if (step && step.explainText) openExplain(step); };
    const openReport = () => {
      const kinds = ['The answer looks wrong', 'The wording is unclear', 'The diagram has a problem', 'Something else'];
      const box = h(`<div class="lsn-sheet"><h2 class="t-sheet-title">Report this screen</h2>
        <p class="t-body lsn-sheet-sub">Note what went wrong. The note is saved with this screen and your answer, and it goes out with your data export.</p>
        <div class="opts lsn-report" role="radiogroup" aria-label="What went wrong">${kinds.map((k, i) => `<button type="button" class="opt" role="radio" aria-checked="false" data-i="${i}">${k}</button>`).join('')}</div>
        <div class="lsn-sheet-act"><button type="button" class="btn" data-send disabled>Save note</button></div></div>`);
      const close = Z.sheet(box, { label: 'Report this screen' });
      let pick = -1;
      box.addEventListener('click', (e) => {
        const o = e.target.closest('.lsn-report .opt');
        if (o) { pick = +o.dataset.i; box.querySelectorAll('.lsn-report .opt').forEach(b => { const on = b === o; b.classList.toggle('selected', on); b.setAttribute('aria-checked', String(on)); }); box.querySelector('[data-send]').disabled = false; }
        if (e.target.closest('[data-send]')) {
          let answer = null; try { answer = step && step.widget ? step.widget.value() : null; } catch { answer = null; }
          const list = Z.store.get('reports', []); list.push({ course, lesson: lessonId, phase: S.phase, screen: S.phase === 'quiz' ? S.q : S.i, kind: kinds[pick], answer, at: Date.now() }); Z.store.set('reports', list.slice(-200));
          box.innerHTML = `<h2 class="t-sheet-title">Note saved</h2><p class="t-body lsn-sheet-sub">It is kept with this lesson, so the screen can be fixed when the content is next edited.</p><div class="lsn-sheet-act"><button type="button" class="btn" data-close>Back to the lesson</button></div>`;
          box.querySelector('[data-close]').focus();
        }
      });
      return close;
    };

    /* ----- Lesson complete (design-research 4.7), the streak moment and Next ----- */
    let skip = null, finalizeP = null;
    const finalize = () => {
      if (finalizeP) return finalizeP;
      const res = Object.values(S.results);
      const first = res.filter(r => r.first).length;
      const perfect = GRADED > 0 && first === GRADED;
      const quizOk = S.quiz.filter(x => x === 'ok').length;
      const spent = S.elapsed;
      let finishXP = XP.finish + (perfect ? XP.perfect : 0);
      if (!S.finished) {
        S.finished = true;
        const qr = st('quizFinished', { course, lesson: lessonId, score: quizOk, items: quizSpec.length, skills: LSN.skills || [], seconds: 0, results: quizSpec.map((it, j) => ({ index: j, id: it.id || 'q' + j, ok: S.quiz[j] === 'ok', key: (S.results['q' + j] || {}).key ?? null, skills: it.skills || LSN.skills || [], difficulty: it.difficulty || 2, ref: { course, lesson: lessonId, item: it.id || 'q' + j } })) });
        const unlogged = Math.max(0, Math.round((Date.now() - S.loggedAt) / 1000));
        S.loggedAt = Date.now();
        const lr = st('lessonFinished', { course, lesson: lessonId, seconds: stFn('lessonFinished') ? unlogged : spent, secondsSpent: spent, firstTry: [first, GRADED], perfect, xp: S.xp, quiz: [quizOk, quizSpec.length] });
        finishXP = xpOf(lr, finishXP);
        void qr; void spent;
        if (!stFn('summary')) qualifyLocal();
        position.set(course, lessonId, null);
      }
      S.finishXP = finishXP;
      finalizeP = { first, perfect, total: S.xp + finishXP, base: S.xp };
      return finalizeP;
    };
    const enterComplete = async () => {
      S.phase = 'complete'; setProgress(); clearChip(); setFrame(null);
      if (S.elapsed == null) S.elapsed = Math.round((Date.now() - S.t0) / 1000);
      const { first, perfect, total, base } = finalize();
      const after = daySummary();
      const qualified = !before.todayDone && after.todayDone;
      nextP = nextP || nextItem(course, lessonId).then(n => { next = n; return n; });
      const acc = S.checks ? Math.round(S.okChecks / S.checks * 100) : 100;
      const badge = (k, ic, label) => `<div class="lsn-badge" data-k="${k}"><span class="lsn-badge-l t-caption">${icon(ic, 'xs')} ${label}</span><b class="tnum lsn-badge-v">0</b></div>`;
      let made = null;
      const el = await swap(() => {
        made = h(`<section class="lsn-done${rm() ? ' rm' : ''}" aria-labelledby="lsn-done-t">
          <div class="lsn-done-mark">${Z.mark('lsn-markic')}</div>
          <h1 class="t-complete" id="lsn-done-t">Lesson complete</h1>
          <div class="lsn-total"><div class="t-overline lsn-total-l">Total XP</div><div class="t-stat lsn-total-n tnum">0</div><p class="t-caption lsn-total-note">&#8203;</p></div>
          <div class="lsn-perfect off"${perfect ? '' : ' hidden'}>${icon('star', 'xs')} Perfect lesson</div>
          <div class="lsn-badges">${badge('acc', 'target', 'Accuracy')}${badge('time', 'clock', 'Time')}${badge('first', 'check', 'First try')}</div>
          <p class="t-body lsn-streakline" hidden></p>
          <p class="t-body lsn-nextline" hidden></p>
          <p class="t-caption lsn-skip">Tap anywhere to skip</p>
        </section>`);
        return made;
      });
      if (!el) return;
      step = { kind: 'done', el, type: 'done', destroy() {} };
      S.st = 'play'; refresh();
      const q = (s) => el.querySelector(s);
      const totalN = q('.lsn-total-n');
      const vals = { acc: [acc, (v) => Math.round(v) + '%'], time: [S.elapsed, (v) => clock(v)], first: [first, (v) => `${Math.round(v)} of ${GRADED}`] };
      const note = S.finishXP === XP.finish + (perfect ? XP.perfect : 0) ? `Includes ${XP.finish} for finishing${perfect ? ` and ${XP.perfect} for a perfect lesson` : ''}.` : S.finishXP ? `Includes ${S.finishXP} for finishing.` : 'You finished this lesson before, so it adds no new XP.';
      const streakLine = () => {
        if (after.off) return;
        const sl = q('.lsn-streakline');
        if (qualified) sl.innerHTML = after.streak <= 1 ? `${Z.bolt(true)}<span>You started a streak. Come back tomorrow to make it 2.</span>` : `${Z.bolt(true)}<span>Today counts. ${after.streak} days in a row.</span>`;
        else if (after.todayDone) sl.innerHTML = `${Z.bolt(true)}<span>Today already counted. Your streak is on ${after.streak} ${after.streak === 1 ? 'day' : 'days'}.</span>`;
        else return;
        sl.hidden = false;
      };
      const nextLine = () => {
        if (!next) return;
        const nl = q('.lsn-nextline');
        if (next.kind === 'homework') nl.innerHTML = `${icon('clipboard', 'sm')}<span>Level ${Z.esc(next.level ?? info.level ?? '')} homework is ready. It is due in 7 days.</span>`;
        else if (next.kind === 'review') nl.innerHTML = `${icon('review', 'sm')}<span>Next: the level review.</span>`;
        else nl.innerHTML = `${icon('arrowR', 'sm')}<span>Next: ${Z.esc(next.name || 'the next lesson')}.</span>`;
        nl.hidden = false;
      };
      const finalState = () => {
        gen++; clearTimers();
        el.classList.add('final');
        totalN.textContent = fmt(total);
        Object.entries(vals).forEach(([k, [v, f]]) => { q(`[data-k="${k}"] .lsn-badge-v`).textContent = f(v); });
        q('.lsn-total-note').textContent = note;
        if (perfect) q('.lsn-perfect').classList.remove('off');
        lightStreak(false); streakLine();
        setXP(total, 0);
        S.st = 'done'; skip = null;
        q('.lsn-skip').hidden = true;
        nextP.then(() => { if (!alive) return; nextLine(); refresh(); });
        refresh();
      };
      const lightStreak = (animate) => {
        if (S.streakDone || !qualified || after.off) return;
        S.streakDone = true;
        const to = after.streak;
        boltEl.classList.add('lit');
        const wrap = $('.lsn-streak');
        wrap.setAttribute('title', `Streak: ${to} days`);
        if (!animate || rm()) { odo.innerHTML = `<span>${to}</span>`; return; }
        Z.sound('streak');
        const spring = getComputedStyle(document.documentElement).getPropertyValue('--spring-bounce').trim() || 'cubic-bezier(0.2, 0, 0, 1)';
        try { wrap.animate([{ transform: 'scale(1)', easing: 'cubic-bezier(0.2, 0, 0, 1)' }, { transform: 'scale(1.25)', offset: 0.36, easing: spring }, { transform: 'scale(1)' }], { duration: 560 }); }
        catch (e) { wrap.animate([{ transform: 'scale(1)' }, { transform: 'scale(1.25)', offset: 0.36 }, { transform: 'scale(1)' }], { duration: 560, easing: 'cubic-bezier(0.2, 0, 0, 1)' }); }
        later(() => {
          const old = odo.firstElementChild, nu = h(`<span>${to}</span>`);
          odo.append(nu);
          const o = { duration: 250, easing: 'cubic-bezier(0.2, 0, 0, 1)', fill: 'forwards' };
          const k = [{ transform: 'translateY(0)' }, { transform: 'translateY(-100%)' }];
          if (old) old.animate(k, o);
          nu.animate(k, o).onfinish = () => { odo.innerHTML = `<span>${to}</span>`; };
        }, 80);
      };
      skip = finalState;
      Z.sound('complete');
      if (rm()) { finalState(); return; }
      later(() => { q('.lsn-done-mark').classList.add('pulse'); Z.burst(q('.lsn-done-mark'), { colors: ['var(--t)', 'var(--green-face)', 'var(--s4)', 'var(--s3)'] }); }, 60);
      later(() => counter(totalN, 0, base, 700), 260);
      ['acc', 'time', 'first'].forEach((k, i) => later(() => { const [v, f] = vals[k]; counter(q(`[data-k="${k}"] .lsn-badge-v`), 0, v, 700, f); }, 420 + i * 80));
      if (perfect) later(() => { q('.lsn-perfect').classList.remove('off'); q('.lsn-badges').classList.add('sweep'); }, 1200);
      later(() => {
        const target = totalN.getBoundingClientRect();
        el.querySelectorAll('.lsn-badge').forEach((b, i) => {
          later(() => {
            const r = b.getBoundingClientRect();
            const g = h('<i class="lsn-ghost" aria-hidden="true"></i>');
            Object.assign(g.style, { left: r.left + r.width / 2 - 6 + 'px', top: r.top + 10 + 'px' });
            document.body.append(g);
            const a = g.animate([{ transform: 'translate(0,0) scale(1)', opacity: 1 }, { transform: `translate(${target.left + target.width / 2 - (r.left + r.width / 2)}px, ${target.top + target.height / 2 - (r.top + 16)}px) scale(0.5)`, opacity: 0.2 }], { duration: 340, easing: 'cubic-bezier(0.3, 0, 0.8, 0.15)' });
            a.onfinish = () => g.remove(); a.oncancel = () => g.remove();
            b.animate([{ transform: 'none' }, { transform: 'translateY(-4px)' }, { transform: 'none' }], { duration: 300 });
          }, i * 80);
        });
        later(() => { totalN.animate([{ transform: 'scale(1)' }, { transform: 'scale(1.08)' }, { transform: 'scale(1)' }], { duration: 420 }); counter(totalN, base, total, 420); q('.lsn-total-note').textContent = note; setXP(total, 420); }, 400);
      }, 1320);
      later(() => { lightStreak(true); streakLine(); }, 1900);
      later(() => { if (skip) finalState(); }, 2350);
    };

    const finish = (goNext) => {
      logHours();
      position.set(course, lessonId, null);
      if (goNext && next) location.hash = routeFor(next);
      else location.hash = '#course/' + course;
      return Promise.resolve();
    };

    /* ----- wiring ----- */
    $('.lsn-close').addEventListener('click', () => {
      if (S.phase === 'complete') { if (skip) skip(); position.set(course, lessonId, null); } else savePosition();
      logHours();
      location.hash = '#course/' + course;
    });
    primary.addEventListener('click', onPrimary);
    sec.addEventListener('click', () => {
      const t = sec.textContent;
      if (t === 'Why?') openWhy(); else if (t === 'Done') finish(false); else openHelp();
    });
    hintBtn.addEventListener('click', () => { if (!hintBtn.disabled) openHelp(); });
    $('.lsn-solve-btn').addEventListener('click', reveal);
    $('.lsn-flag').addEventListener('click', openReport);
    const syncSound = () => { const on = !!Z.settings.sound; sndBtn.setAttribute('aria-pressed', String(on)); sndBtn.innerHTML = icon(on ? 'sound' : 'mute', 'sm'); sndBtn.setAttribute('aria-label', on ? 'Sound on. Turn sound off' : 'Sound off. Turn sound on'); };
    sndBtn.addEventListener('click', () => { Z.setSetting('sound', !Z.settings.sound); Z.sound('tap'); });
    Z.on('settings', () => { if (alive) syncSound(); });
    syncSound();
    app.addEventListener('click', (e) => { if (skip && S.phase === 'complete' && S.st === 'play' && !e.target.closest('.lsn-top, .lsn-utils')) skip(); });

    const onKey = (e) => {
      if (!alive || document.querySelector('.scrim')) return;
      const t = e.target;
      const inField = t && (t.tagName === 'INPUT' || t.tagName === 'TEXTAREA' || t.tagName === 'MATH-FIELD' || t.isContentEditable);
      if (e.key === 'Enter') {
        if (e.repeat) return;
        if (t && t.tagName === 'TEXTAREA') return;
        if (t && t.closest && t.closest('button, a') && !t.closest('.opt, .lsn-cell, .wd-tok, .wd-line')) return; // native activation
        if (skip && S.st === 'play') { e.preventDefault(); skip(); return; }
        if (primary.disabled || primary.classList.contains('lsn-hide')) return;
        e.preventDefault(); primary.classList.add('is-pressed'); later(() => primary.classList.remove('is-pressed'), 90); onPrimary();
        return;
      }
      if (!inField && !e.ctrlKey && !e.metaKey && !e.altKey && /^[1-9]$/.test(e.key) && step && step.pick && (S.st === 'idle' || S.st === 'engaged')) {
        e.preventDefault(); step.pick(+e.key - 1);
      }
    };
    document.addEventListener('keydown', onKey);

    /* ----- Test hook (docs/PLAN.md section 7) ----- */
    const settle = (p) => Promise.resolve(p).then(() => new Promise(r => setTimeout(r, rm() ? 20 : 260)));
    const hook = {
      current: () => ({
        screenIndex: S.phase === 'lesson' ? S.i : S.phase === 'quiz' ? S.q : -1,
        kind: S.phase === 'quiz' ? 'quiz' : S.phase === 'complete' ? 'done' : (step && step.type) || 'loading',
        phase: S.phase, state: S.st, lesson: `${course}/${lessonId}`, total: S.phase === 'quiz' ? quizSpec.length : N,
      }),
      answerCorrect: () => { if (!step || !step.answer) return false; const ok = step.answer(); changed(); return ok; },
      check: () => (S.st === 'engaged' ? check() : Promise.resolve(null)),
      continue: () => {
        if (S.st === 'play' && skip) { skip(); return Promise.resolve(); }
        if (['ok', 'rev', 'qok', 'qno', 'read', 'done'].includes(S.st)) return settle(advance());
        return Promise.resolve();
      },
      reveal: () => { reveal(); return Promise.resolve(); },
      goto: (i) => { S.anyCheck = true; return settle(i === 'quiz' ? enterQuiz(0) : i === 'done' ? enterComplete() : enterLesson(Math.max(0, Math.min(N - 1, i)))); },
      step: () => step,
    };
    window.ZQ.test = hook;

    setXP(S.xp, 0);
    if (start === 'done') enterComplete();
    else if (start === 'quiz' && quizSpec.length) enterQuiz(0);
    else if (Number.isInteger(+start) && start !== null && start !== '' && !isNaN(+start)) enterLesson(Math.max(0, Math.min(N - 1, +start)));
    else if (saved) {
      if (saved.phase === 'lesson') enterLesson(Math.min(N - 1, saved.i || 0));
      else if (saved.q >= quizSpec.length) enterComplete();
      else enterQuiz(saved.q || 0);
      Z.toast('Picked up where you left off');
    } else enterLesson(0);

    return () => {
      if (alive && S.phase !== 'complete') { try { savePosition(); logHours(); } catch (e) { console.error(e); } }
      alive = false; gen++; clearTimers();
      if (window.ZQ.test === hook) delete window.ZQ.test;
      document.removeEventListener('keydown', onKey);
      if (step && step.destroy) step.destroy();
      document.querySelectorAll('.lsn-ghost').forEach(n => n.remove());
    };
  }

  /* ---------- One item, for set mode and exams ---------- */
  function renderItem(item, host, { mode = 'set', onGraded, key } = {}) {
    const ref = item.ref || {};
    const draftKey = ref.exam ? `${ref.exam}/${ref.item}` : ref.course && ref.lesson ? `${ref.course}/${ref.lesson}/${ref.item ?? 's' + ref.screen}` : null;
    const step = buildScreen(item, { mode, key: key || item.id || 'item', pointEl: () => {}, into: () => {}, draftKey });
    host.append(step.el);
    Z.mathify(step.el);
    step.enter((fn, ms) => setTimeout(fn, ms));
    let result = null;
    return {
      el: step.el, item, widget: step.widget, canvas: step.canvas, step,
      ready: step.ready, value: () => (step.widget ? step.widget.value() : null), set: (v) => step.widget && step.widget.set(v),
      onChange: step.onChange, answerCorrect: () => step.answer(), pick: step.pick,
      async check() {
        if (result) return result;
        step.lock();
        const r = await step.grade();
        if (r && r.pending) { step.clear(); return r; }
        r.final = true;
        if (mode !== 'exam') step.mark(r);
        result = Object.assign({}, r, { line: r.ok ? (item.feedback && item.feedback.correct) || null : notYetLine(item, r), value: step.widget ? step.widget.value() : null, item });
        onGraded && onGraded(result);
        return result;
      },
      result: () => result,
      why: () => openExplain(step),
      reveal: () => step.reveal(),
      focus: () => step.focusInput && step.focusInput(),
      destroy: () => { step.destroy(); step.el.remove(); },
    };
  }

  /* ---------- A list of items with dot progress, one attempt each ---------- */
  function runSet(host, { title = 'Practice', items = [], mode = 'set', onDone, track = 'prob' } = {}) {
    const { h, icon } = Z;
    let alive = true, i = 0, cur = null, st0 = 'idle';
    const results = [];
    const wrap = h(`<div class="lsn-set" data-track="${Z.esc(track)}">
      <div class="lsn-qhead"><span class="t-overline">${Z.esc(title)}</span><span class="dots" aria-hidden="true">${items.map(() => '<i></i>').join('')}</span><span class="t-caption lsn-qof"></span></div>
      <div class="lsn-set-body"></div>
      <div class="lsn-foot lsn-set-foot"><div class="lsn-verdict" aria-live="polite"></div>
        <div class="lsn-actions"><button type="button" class="btn secondary lsn-sec" hidden>Why?</button><button type="button" class="btn lsn-primary" disabled>Check</button></div></div>
    </div>`);
    host.append(wrap);
    const body = wrap.querySelector('.lsn-set-body'), verdict = wrap.querySelector('.lsn-verdict'), primary = wrap.querySelector('.lsn-primary'), sec = wrap.querySelector('.lsn-sec');
    const dots = () => wrap.querySelectorAll('.lsn-qhead .dots i').forEach((d, j) => { d.className = results[j] ? (results[j].ok ? 'ok' : 'bad') : j === i ? 'cur' : ''; });
    const sync = () => {
      primary.className = 'btn lsn-primary' + (st0 === 'ok' ? ' correct' : st0 === 'no' ? ' notyet' : '');
      primary.textContent = st0 === 'idle' || st0 === 'engaged' || st0 === 'eval' ? 'Check' : i < items.length - 1 ? 'Continue' : 'Finish';
      primary.disabled = st0 === 'idle' || st0 === 'eval';
      sec.hidden = !(st0 === 'ok' || st0 === 'no');
      wrap.classList.toggle('is-ok', st0 === 'ok'); wrap.classList.toggle('is-no', st0 === 'no');
    };
    const show = (k) => {
      if (cur) cur.destroy();
      i = k; st0 = 'idle'; verdict.innerHTML = '';
      wrap.querySelector('.lsn-qof').textContent = `Question ${i + 1} of ${items.length} · No hints, one try`;
      cur = renderItem(items[i], body, { mode, key: 'set' + i });
      if (!Z.reducedMotion()) cur.el.animate([{ opacity: 0, transform: 'translateY(8px)' }, { opacity: 1, transform: 'none' }], { duration: 200, easing: 'cubic-bezier(0.05, 0.7, 0.1, 1)' });
      cur.onChange(() => { if (st0 === 'idle' || st0 === 'engaged') { st0 = cur.ready() ? 'engaged' : 'idle'; sync(); } });
      if (!cur.widget) st0 = 'engaged';
      dots(); sync();
    };
    const doCheck = async () => {
      st0 = 'eval'; sync();
      const r = await cur.check();
      if (!alive) return;
      if (r && r.pending) { st0 = cur.ready() ? 'engaged' : 'idle'; sync(); return; }
      results[i] = r; st0 = r.ok ? 'ok' : 'no';
      if (mode !== 'exam') {
        if (r.ok) { Z.sound('correct'); } else Z.sound('notyet');
        verdict.innerHTML = `<div class="lsn-chip is-${r.ok ? 'ok' : 'no'}"><span class="lsn-chip-ic">${icon(r.ok ? 'check' : 'cross', 'sm')}</span><div class="lsn-chip-tx"><div class="lsn-chip-h"><b>${r.ok ? 'Correct.' : 'Not quite right.'}</b></div>${r.line ? `<span>${G().inline(strip(r.line, r.ok ? 'Correct.' : 'Not quite right.'))}</span>` : ''}</div></div>`;
      }
      dots(); sync();
    };
    const onPrimary = () => {
      if (primary.disabled) return;
      if (st0 === 'engaged') return doCheck();
      if (i < items.length - 1) return show(i + 1);
      alive = false;
      if (onDone) onDone(results.slice());
      else { body.innerHTML = `<p class="t-prose">You got ${results.filter(r => r && r.ok).length} of ${items.length}.</p>`; wrap.querySelector('.lsn-foot').hidden = true; }
    };
    primary.addEventListener('click', onPrimary);
    sec.addEventListener('click', () => cur && cur.why());
    const onKey = (e) => {
      if (!wrap.isConnected || document.querySelector('.scrim')) return;
      if (e.key === 'Enter' && !e.repeat && !(e.target.closest && e.target.closest('button, a, textarea') && !e.target.closest('.opt, .wd-tok, .wd-line'))) { e.preventDefault(); onPrimary(); }
      else if (/^[1-9]$/.test(e.key) && !/INPUT|TEXTAREA/.test(e.target.tagName || '') && cur && (st0 === 'idle' || st0 === 'engaged')) cur.pick && cur.pick(+e.key - 1);
    };
    document.addEventListener('keydown', onKey);
    /* Test hook in set mode (docs/PLAN.md 7), the same calls as the lesson's: current(), answerCorrect(), check(), continue() */
    const hook = {
      current: () => ({ screenIndex: i, kind: alive ? 'item' : 'done', phase: 'set', state: st0, total: items.length, mode, title }),
      answerCorrect: () => {
        if (!alive || !cur || !(st0 === 'idle' || st0 === 'engaged')) return false;
        const ok = cur.answerCorrect();
        st0 = cur.ready() ? 'engaged' : 'idle'; sync();
        return ok;
      },
      check: async () => {
        if (st0 !== 'engaged') return null;
        await doCheck();
        return results[i] || (cur && cur.result()) || { pending: true, ok: false, key: null };
      },
      continue: () => { if (alive && (st0 === 'ok' || st0 === 'no')) onPrimary(); return new Promise(r => setTimeout(r, 60)); },
      results: () => results.slice(),
    };
    window.ZQ.test = hook;
    if (items.length) show(0);
    return {
      results: () => results.slice(),
      current: () => cur,
      hook,
      destroy() { alive = false; document.removeEventListener('keydown', onKey); if (window.ZQ.test === hook) delete window.ZQ.test; if (cur) cur.destroy(); wrap.remove(); },
    };
  }

  Z.player = { mount, renderItem, runSet, buildScreen, openExplain, XP };
})();
