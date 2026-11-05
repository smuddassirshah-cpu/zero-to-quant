/* Setup (#setup): three steps on first run, rerunnable from You. Replaces the prototype's onboarding.
   1 Name and initial. 2 Track. 3 Weekly hours and starting stage, with the curriculum's advice to sit each stage's
   exit test first. Finishing writes ZQ.state.profile and flags.setupDone, then opens #today.
   Look: the onboarding classes in css/screens/onboarding.css (scoped under .screen-onboarding, added to the root here).
   Keys: Enter is the primary button; 1 to 9 pick a row on the choice steps. */
(function () {
  'use strict';
  const STEPS = 3;
  const TRACKS = [
    { id: 'Trader', desc: 'Probability, mental arithmetic, market-making and betting games',
      react: 'Trader interviews test probability hardest, so it gets the most weight from Stage 2.' },
    { id: 'Researcher', desc: 'Probability, statistics, regression, machine learning, a data take-home',
      react: 'Researchers get the most statistics and machine learning, plus projects 1 and 2 and a paper replication.' },
    { id: 'Developer', desc: 'Algorithms, C++, systems design',
      react: 'Developers get more algorithm practice and contests, and C++ needs at least double its 140 hours.' },
    { id: 'Strats', desc: 'Maths, finance, derivatives pricing, Python or C++',
      react: 'Strats gets finance basics as required work, with derivatives and desk quant as a route inside it.' },
    { id: 'Undecided', desc: 'Stages 0 and 1 are the same for every track',
      react: 'That is fine. Stages 0 and 1 are shared; you choose before Stage 2.' },
  ];
  const HOURS = [5, 10, 15, 25];
  const HOURS_REACT = {
    5: 'Slow but steady. Short sessions on most days beat one long one.',
    10: 'Workable alongside a full-time job.',
    15: 'The pace this curriculum is planned around: about 4 years for the full path.',
    25: 'Close to a part-time job: about 2.4 years for the full path, if you can hold it.',
  };
  const FALLBACK_STAGES = [
    { id: 0, name: 'From nothing', hours: 500 }, { id: 1, name: 'Foundations', hours: 1400 },
    { id: 2, name: 'Intermediate', hours: 800 }, { id: 3, name: 'Advanced', hours: 400 },
  ];
  const EXIT_LINE = 'Sit each stage’s exit test first. Pass it and you skip the stage. Fail it and you have a list of what to study.';

  ZQ.screen({
    id: 'setup', title: 'Setup', group: 'Start', shell: false,
    render(root, Z) {
      root.classList.add('screen-onboarding');
      const esc = Z.esc, P = Z.state.profile.get();
      const stages = (Z.content && Z.content.stages().length ? Z.content.stages() : FALLBACK_STAGES);
      const S = {
        step: 1,
        name: P.name || '', initial: P.initial || '', initialEdited: !!P.initial,
        track: Z.state.flags.setupDone ? P.track : null,
        hours: Z.state.flags.setupDone ? P.weeklyGoalH : null,
        stage: Z.state.flags.setupDone ? P.startStage : null,
      };
      root.innerHTML = `<div class="ob">
        <header class="ob-top">
          <button type="button" class="icon-btn ob-back" aria-label="Back">${Z.icon('chevronL')}</button>
          <div class="ob-prog">
            <div class="bar ob-bar" role="progressbar" aria-label="Setup progress" aria-valuemin="1" aria-valuemax="${STEPS}"><i></i></div>
            <span class="ob-count tnum" aria-hidden="true"></span>
          </div>
          <span class="ob-top-r" aria-hidden="true"></span>
        </header>
        <main class="ob-main"><div class="ob-col"></div></main>
        <footer class="ob-foot"><div class="ob-actions"></div><p class="ob-note t-caption" hidden></p></footer>
      </div>`;
      const $ = (s) => root.querySelector(s);
      const col = $('.ob-col'), actions = $('.ob-actions'), note = $('.ob-note'), back = $('.ob-back');
      const bar = $('.ob-bar'), fill = bar.querySelector('i'), count = $('.ob-count');
      let keyFn = null, fadeT = 0;

      const radio = '<span class="ob-radio" aria-hidden="true"></span>';
      const row = (id, name, desc, sel, attr) => `<button type="button" class="opt ob-row" data-${attr}="${esc(id)}" aria-pressed="${sel}">
          <span class="ob-row-tx"><span class="ob-row-h">${esc(name)}</span><span class="ob-row-d">${esc(desc)}</span></span>${radio}</button>`;
      const headline = (t) => `<h1 class="t-display ob-q" tabindex="-1" data-focus>${t}</h1>`;
      const ready = () => (S.step === 1 ? S.name.trim().length > 0 && S.initial.trim().length > 0 : S.step === 2 ? !!S.track : !!S.hours && S.stage != null);
      const primary = () => actions.querySelector('[data-next]');
      const enable = () => { const b = primary(); if (b) b.disabled = !ready(); };
      const setActions = (label, noteHtml = '') => {
        actions.innerHTML = `<button type="button" class="btn block" data-next>${label}</button>`;
        note.hidden = !noteHtml; note.innerHTML = noteHtml;
        enable();
      };
      const pick = (container, attr, onPick) => container.addEventListener('click', (e) => {
        const b = e.target.closest(`[data-${attr}]`); if (!b) return;
        container.querySelectorAll(`[data-${attr}]`).forEach(x => x.setAttribute('aria-pressed', String(x === b)));
        Z.sound('tap'); onPick(b.getAttribute(`data-${attr}`)); enable();
      });
      const swap = (el, html) => { el.innerHTML = html; el.classList.remove('ob-pop'); void el.offsetWidth; el.classList.add('ob-pop'); };

      /* ---------- 1 Name and initial ---------- */
      const stepName = () => {
        col.innerHTML = `${headline('What should we call you?')}
          <p class="t-body ob-react">Your name stays on this device. The initial sits in the corner of every screen.</p>
          <section class="ob-group" aria-labelledby="su-gn"><h2 class="t-h2" id="su-gn">Name</h2>
            <label class="field"><input type="text" data-name autocomplete="given-name" spellcheck="false" maxlength="40" aria-labelledby="su-gn" value="${esc(S.name)}"></label></section>
          <section class="ob-group" aria-labelledby="su-gi"><h2 class="t-h2" id="su-gi">Initial</h2>
            <label class="field ob-num"><input type="text" data-initial autocomplete="off" spellcheck="false" maxlength="2" aria-labelledby="su-gi" value="${esc(S.initial)}"></label></section>`;
        const name = col.querySelector('[data-name]'), ini = col.querySelector('[data-initial]');
        name.addEventListener('input', () => {
          S.name = name.value;
          if (!S.initialEdited) { S.initial = S.name.trim().charAt(0).toUpperCase(); ini.value = S.initial; }
          enable();
        });
        ini.addEventListener('input', () => { S.initial = ini.value.toUpperCase(); ini.value = S.initial; S.initialEdited = S.initial.length > 0; enable(); });
        [name, ini].forEach(el => el.addEventListener('keydown', (e) => { if (e.key === 'Enter' && ready()) { e.preventDefault(); next(); } }));
        setActions('Continue', 'No account. Everything stays in this browser; export it from You.');
        setTimeout(() => name.focus({ preventScroll: true }), 30);
        keyFn = null;
      };

      /* ---------- 2 Track ---------- */
      const stepTrack = () => {
        const t = TRACKS.find(x => x.id === S.track);
        col.innerHTML = `${headline('Which role are you aiming for?')}
          <p class="t-body ob-react" aria-live="polite">${t ? esc(t.react) : '<span class="muted">Pick one. You can change it later on You.</span>'}</p>
          <div class="opts ob-rows" role="group" aria-label="Track">${TRACKS.map(o => row(o.id, o.id === 'Undecided' ? 'Not sure yet' : o.id, o.desc, S.track === o.id, 'track')).join('')}</div>`;
        pick(col.querySelector('.ob-rows'), 'track', (id) => { S.track = id; swap(col.querySelector('.ob-react'), esc(TRACKS.find(x => x.id === id).react)); });
        setActions('Continue');
        keyFn = numberKeys('[data-track]');
      };

      /* ---------- 3 Weekly hours and starting stage ---------- */
      const stepPace = () => {
        col.innerHTML = `${headline('How much time, and where do you start?')}
          <section class="ob-group" aria-labelledby="su-gh"><h2 class="t-h2" id="su-gh">Hours a week</h2>
            <div class="ob-hours" role="group" aria-labelledby="su-gh">${HOURS.map(h => `<button type="button" class="chip ob-hr" data-h="${h}" aria-pressed="${S.hours === h}" aria-label="${h} hours a week"><b class="tnum">${h}</b><span>h</span></button>`).join('')}</div>
            <p class="t-body ob-react" data-hreact aria-live="polite">${S.hours ? esc(HOURS_REACT[S.hours]) : '<span class="muted">The weekly goal on Today splits into main subject, build, review and mental arithmetic.</span>'}</p></section>
          <section class="ob-group" aria-labelledby="su-gs"><h2 class="t-h2" id="su-gs">Starting stage</h2>
            <p class="t-caption secondary">${esc(EXIT_LINE)}</p>
            <div class="opts ob-rows" role="group" aria-labelledby="su-gs">${stages.map(s => row(String(s.id), `Stage ${s.id}: ${s.name}`, `${Number(s.hours).toLocaleString('en-GB')} hours${s.exit ? '. Exit: ' + s.exit : ''}`, S.stage === s.id, 'stage')).join('')}</div></section>`;
        col.querySelector('.ob-hours').addEventListener('click', (e) => {
          const b = e.target.closest('[data-h]'); if (!b) return;
          S.hours = Number(b.dataset.h);
          col.querySelectorAll('[data-h]').forEach(x => x.setAttribute('aria-pressed', String(x === b)));
          Z.sound('tap'); swap(col.querySelector('[data-hreact]'), esc(HOURS_REACT[S.hours])); enable();
        });
        pick(col.querySelectorAll('.ob-rows')[0], 'stage', (id) => { S.stage = Number(id); });
        setActions('Start learning');
        keyFn = numberKeys('[data-stage]');
      };

      const numberKeys = (sel) => (e) => {
        const n = Number(e.key);
        if (!Number.isInteger(n) || n < 1 || n > 9) return;
        const b = col.querySelectorAll(sel)[n - 1]; if (b) { e.preventDefault(); b.click(); }
      };

      const VIEWS = { 1: stepName, 2: stepTrack, 3: stepPace };
      const show = (focus = true) => {
        clearTimeout(fadeT);
        col.innerHTML = '';
        VIEWS[S.step]();
        Z.mathify(col);
        back.style.visibility = S.step === 1 ? 'hidden' : 'visible';
        fill.style.width = ((S.step - 1) / STEPS * 100 + 100 / STEPS / 2).toFixed(2) + '%';
        bar.setAttribute('aria-valuenow', String(S.step));
        bar.setAttribute('aria-valuetext', `Step ${S.step} of ${STEPS}`);
        count.textContent = `${S.step} of ${STEPS}`;
        col.classList.remove('ob-in'); void col.offsetWidth; col.classList.add('ob-in');
        window.scrollTo(0, 0);
        const h = col.querySelector('[data-focus]');
        if (focus && S.step > 1 && h) h.focus({ preventScroll: true });
      };
      const finish = () => {
        Z.state.profile.set({ name: S.name.trim(), initial: S.initial.trim().slice(0, 2), track: S.track, weeklyGoalH: S.hours, startStage: S.stage });
        Z.state.flags.set({ setupDone: true });
        Z.state.flush();
        Z.go('today');
      };
      function next() {
        if (!ready()) return;
        if (S.step < STEPS) { S.step++; show(); } else finish();
      }
      back.addEventListener('click', () => { if (S.step > 1) { S.step--; show(); } });
      actions.addEventListener('click', (e) => { const b = e.target.closest('[data-next]'); if (b && !b.disabled) next(); });
      const onKey = (e) => {
        if (e.defaultPrevented || e.metaKey || e.ctrlKey || e.altKey || document.querySelector('.scrim')) return;
        const t = e.target instanceof Element ? e.target : document.body;
        if (t.closest('input, select, textarea')) return;
        if (e.key === 'Enter' && !e.repeat && !t.closest('button, a')) { const p = primary(); if (p && !p.disabled) { e.preventDefault(); p.click(); } return; }
        if (keyFn) keyFn(e);
      };
      document.addEventListener('keydown', onKey);
      show(false);
      return () => { document.removeEventListener('keydown', onKey); clearTimeout(fadeT); };
    },
  });
})();
