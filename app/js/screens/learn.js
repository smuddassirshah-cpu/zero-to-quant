/* Learn: the catalogue.
   Spec: 7.3 Catalogue, 8.2 Stage > Topic > Course, 3 course art, 2.5 track accents, 4 motion, 9.2 voice.
   Curriculum: four stages with exit tests, topics by number, and the Stage 2 tracks (Trader, Researcher, Developer).
   Two views: Courses (stage selector, exit test, track tabs, topic cards of course cards) and Paths (Stage 2 tracks).
   Course states: Not started, In progress, Complete (course done, topic exam not yet open), Exam ready (every course in
   the topic has a mastered lesson), Passed, and Tested out (topic exam passed before the course was finished).
   Data: stages, topics and courses from ZQ.content; progress from ZQ.state.summary().courseProgress; exam states from
   ZQ.state.exams ('topic-<id>', 'stage-<n>'); the learner's track from ZQ.state.profile. A course with no written
   lesson carries a quiet "Map only" tag and still opens its map. Re-renders on the 'state' event.
   Everything is scoped under .screen-learn and uses the zl- prefix. */
(function () {
  'use strict';

  /* Months at 15 h a week, as the curriculum map states them */
  const MONTHS = { 0: 8, 1: 21, 2: 12, 3: 6 };
  const TRACKS = ['all', 'maths', 'prob', 'code', 'fin', 'ml', 'speed'];
  const TRACK_WORD = { maths: 'maths', prob: 'probability and statistics', code: 'programming', fin: 'finance', ml: 'machine learning', speed: 'interview and speed' };

  /* One-line notes from the curriculum, shown under a topic head */
  const NOTES = (track) => ({
    '0.4': 'Run it alongside 0.1 to 0.3 from the first week.',
    '0.5': 'Ten minutes a day, from the first week.',
    '1.1': 'First, so every maths topic after it can be checked in code.',
    '1.5': 'The priority. Interviews test it hardest.',
    '1.7': 'Run it alongside 1.3 to 1.6.',
    '1.9': track === 'Developer' ? 'The core skill on your track. Give it at least double the hours.'
      : track === 'Undecided' ? 'Developers give it at least double the hours; other tracks can let it slip into Stage 2.'
      : `On the ${track} track you can let it slip into Stage 2.`,
    '2.3': 'Do three properly, not five thinly.',
    '3.2': 'Hours not counted. For derivatives pricing and desk quant roles.',
  });
  /* Topics closed by something other than a timed exam */
  const CLOSE = {
    '0.5': ['timer', 'Target score 25 in 120 s'],
    '2.3': ['clipboard', 'Closed by three projects'],
    '2.4': ['target', 'Target rating 1,400'],
    '3.1': ['clipboard', 'Closed by a replication'],
  };
  const examMinutes = (h) => (h <= 60 ? 45 : h <= 150 ? 60 : 90); // spec 8.2: topic exams run 45 to 90 min

  /* Stage 2 tracks, from the curriculum's track table. Steps are in study order. */
  const PATHS = [
    { id: 'Trader', tests: 'Probability, mental arithmetic, market-making and betting games',
      steps: [
        { course: 'opt-dash', tag: 'Project 3' },
        { course: 'contests', meta: 'Trading competitions' },
        { course: 'puzzles' },
        { course: 'mm-games' },
        { course: 'mental-pressure' },
      ] },
    { id: 'Researcher', tests: 'Probability, statistics, regression, machine learning, a data take-home',
      steps: [
        { topic: '2.1' },
        { topic: '2.2' },
        { course: 'backtest', tag: 'Project 1' },
        { course: 'alpha', tag: 'Project 2' },
        { topic: '3.1', meta: 'Paper replication' },
        { course: 'puzzles' },
      ] },
    { id: 'Developer', tests: 'Algorithms, C++, systems design',
      steps: [
        { topic: '1.9', meta: 'At least double: 280 h' },
        { course: 'contests', meta: 'Codeforces weekly' },
        { course: 'backtest', tag: 'Project 1' },
        { title: 'Live Market Data Handler', topicId: '2.3', meta: 'Project 4 · In C++', art: 'vol', track: 'fin' },
        { course: 'puzzles' },
      ] },
    { id: 'Strats', tests: 'Maths, finance, derivatives pricing, Python or C++',
      steps: [
        { course: 'markets' },
        { course: 'options' },
        { course: 'trees' },
        { course: 'regression' },
        { course: 'backtest', tag: 'Project 1' },
      ] },
  ];

  /* View state lasts for this visit, so returning from a course keeps the stage and tab */
  const view = { stage: null, track: 'all', view: 'courses' };

  /* One 'state' listener for the module; the mounted screen sets onState and clears it on leave (core.js has no off) */
  let onState = null;
  ZQ.on('state', (e) => { if (onState) onState(e); });

  /* ---------- Where the learner is (the same rule as Today and the course map) ---------- */
  const keyOf = (c, l) => `${c}/${l}`;
  const nextLesson = (Z, cid) => Z.content.courseLessons(cid).find(x => x.kind === 'lesson' && x.written === true && !((Z.state.lessons[keyOf(cid, x.id)] || {}).done) && !(Z.prereq && Z.prereq.lessonLocked(cid, x.id))) || null;   // locked lessons are never picked (ENGINE-BACKLOG 486)
  const currentCourse = (Z, sum) => {
    const C = Z.content;
    const track = Z.state.profile.get().track;
    if (sum.resume && C.course(sum.resume.course) && C.resumeStands(sum.resume) && C.readiness.offerable(sum.resume.course, track)) return sum.resume.course;
    const start = Number(Z.state.profile.startStage) || 0;
    const open = C.readiness.plan(C.courses(), track).filter(c => (sum.courseProgress[c.id] || 0) < 1 && nextLesson(Z, c.id));
    /* A course in a passed topic is skipped; it is chosen only when nothing else has a lesson left */
    const fresh = open.filter(c => !C.courseTestedOut(c.id));
    const c = fresh.find(x => x.stage >= start) || fresh[0] || open[0];
    return c ? c.id : null;
  };
  const pctOf = (a) => { // an exam attempt's score as a percentage, whatever scale it was stored on
    if (!a) return 0;
    const s = Number(a.score) || 0, n = Number(a.items) || 0;
    if (n > 0 && s <= n && s > 1) return Math.round(s / n * 100);
    return Math.round(s <= 1 ? s * 100 : s);
  };

  ZQ.screen({
    id: 'learn', title: 'Learn', group: 'App', shell: true, tab: 'learn',
    render(root, Z) {
      const C = Z.content, S = Z.state, esc = Z.esc;
      const reduced = Z.reducedMotion();
      const fmt = (n) => Number(n).toLocaleString('en-GB');
      const cap = (s) => s.charAt(0).toUpperCase() + s.slice(1);
      const titleCase = (s) => s.replace(/(^|\s)([a-z])([a-z]*)/g, (m, sp, a, rest) => (/^(and|of|the|for|in)$/.test(a + rest) && sp ? m : sp + a.toUpperCase() + rest));
      const hrs = (n) => `${fmt(n)} h`;
      const STAGES = C.stages();
      const trackNames = C.tracks, trackShort = (C.curriculum && C.curriculum.trackShort) || {};

      /* ---------- Learner numbers, refreshed by read() ---------- */
      let sum, prof, curId, notes, stagePassed, learnerStage;
      const exam = (id) => { const r = S.exams[id]; const a = r && Array.isArray(r.attempts) ? r.attempts : []; return { sat: a.length > 0, passed: a.filter(x => x.passed), attempts: a }; };
      const read = () => {
        sum = S.summary(); prof = S.profile.get();
        curId = currentCourse(Z, sum);
        notes = NOTES(prof.track || 'Undecided');
        stagePassed = (n) => exam('stage-' + n).passed.length > 0;
        const top = Math.max(-1, ...STAGES.filter(s => stagePassed(s.id)).map(s => s.id));
        learnerStage = Math.min(3, Math.max(Number(prof.startStage) || 0, top + 1));
      };
      read();
      if (view.stage == null) view.stage = learnerStage;

      /* ---------- Course facts ---------- */
      const lessonsOf = (id) => C.courseLessons(id).filter(x => x.kind === 'lesson');
      const writtenCount = (id) => lessonsOf(id).filter(x => x.written === true).length;
      const masteredAny = (id) => lessonsOf(id).some(x => (S.lessons[keyOf(id, x.id)] || {}).mastered);
      const courseOf = (id) => C.course(id);
      const topicCourses = (t) => (t.courses || []).map(courseOf).filter(Boolean);

      /* ---------- State helpers ---------- */
      const prog = (id) => Math.max(0, Math.min(1, sum.courseProgress[id] || 0));
      const passed = (t) => C.topicPassed(t.id);
      /* The topic exam opens when every course in the topic has at least one mastered lesson (PLAN section 10) */
      const topicReady = (t) => topicCourses(t).every(c => masteredAny(c.id));
      const courseState = (c, t) => {
        const p = prog(c.id);
        if (passed(t)) return p >= 1 ? 'pass' : 'out';
        return p >= 1 ? (topicReady(t) ? 'ready' : 'done') : p > 0 ? 'prog' : 'none';
      };
      const topicState = (t) => (passed(t) ? 'pass' : topicReady(t) ? 'ready' : topicCourses(t).some(c => prog(c.id) > 0) ? 'prog' : 'none');
      const ring = '<svg class="zl-ring" viewBox="0 0 16 16" aria-hidden="true"><circle cx="8" cy="8" r="5.5"/><path d="M8 2.5a5.5 5.5 0 0 1 0 11z"/></svg>';
      const dash = '<svg class="zl-ring is-empty" viewBox="0 0 16 16" aria-hidden="true"><circle cx="8" cy="8" r="5.5"/></svg>';
      const STATE = {
        none: ['Not started', dash],
        prog: ['In progress', ring],
        done: ['Complete', Z.icon('check', 'xs')],
        ready: ['Exam ready', Z.icon('shield', 'xs')],
        pass: ['Passed', Z.icon('check', 'xs')],
        out: ['Tested out', Z.icon('check', 'xs')],
      };
      const chip = (s, cls = '') => `<span class="zl-chip is-${s} ${cls}">${STATE[s][1]}<span>${STATE[s][0]}</span></span>`;
      const stageOf = (n) => STAGES.find(s => s.id === n);
      const inTrack = (t) => view.track === 'all' || t.track === view.track;
      const totalH = STAGES.reduce((a, s) => a + (s.hours || 0), 0);
      /* The readiness contract (content/readiness.json): one total for the chosen role, required plus recommended, written and unwritten stated separately.
         Undecided shows the shared foundation. Without the file the old line stands. */
      const roleHeader = () => {
        const role = C.readiness.roleKey(prof.track), t = C.readiness.totals(role), h = t && t.header;
        if (!h) return `${fmt(totalH)} hours in ${STAGES.length === 4 ? 'four' : STAGES.length} stages. Sit a stage’s exit test first to skip it.`;
        const split = `${fmt(h.written)} written, ${fmt(h.unwritten)} unwritten`;
        return role === 'undecided'
          ? `Shared foundation: ${fmt(h.total)} lessons, ${fmt(h.hours)} h (${split}). Choose a role on You before Stage 2. Sit a stage’s exit test first to skip it.`
          : `${esc(prof.track)} route: ${fmt(h.total)} lessons, ${fmt(h.hours)} h, required plus recommended (${split}). Sit a stage’s exit test first to skip it.`;
      };

      /* ---------- Skeleton ---------- */
      root.innerHTML = `
        <div class="zl">
          <header class="zl-head">
            <h1 class="t-h1 zl-h1">Learn</h1>
            <p class="t-body secondary zl-desc">${roleHeader()}</p>
            ${C.prepPaths().length ? `<a class="zl-prepare" href="#prepare">${Z.icon('target', 'xs')}<span>Prepare for an assessment or a firm</span>${Z.icon('chevronR', 'xs')}</a>` : ''}
            <div class="zl-toggle" role="group" aria-label="View">
              <button type="button" data-view="courses">${Z.icon('grid', 'xs')}<span>Courses</span></button>
              <button type="button" data-view="paths">${Z.icon('target', 'xs')}<span>Paths</span></button>
            </div>
          </header>
          <div class="zl-courses">
            <div class="zl-stages" role="group" aria-label="Stage"></div>
            <div class="zl-exit-slot"></div>
            <div class="zl-tabs-wrap"><div class="zl-tabs" role="tablist" aria-label="Track"></div></div>
            <div class="zl-topics" role="tabpanel" id="zl-panel"></div>
          </div>
          <div class="zl-paths-view" hidden></div>
        </div>`;
      const $ = (s) => root.querySelector(s);
      const coursesEl = $('.zl-courses'), pathsEl = $('.zl-paths-view');
      const stagesEl = $('.zl-stages'), exitEl = $('.zl-exit-slot'), tabsEl = $('.zl-tabs'), topicsEl = $('.zl-topics');

      /* ---------- Stage selector ---------- */
      /* Segmented pill: "Stage n" only. A check marks a stage whose exit test is passed, a dot marks the learner's stage. */
      const renderStages = () => {
        stagesEl.innerHTML = STAGES.map(s => `
          <button type="button" class="zl-stage" data-stage="${s.id}" title="${esc(s.name)} · ${fmt(s.hours)} hours">
            ${stagePassed(s.id) ? `<span class="zl-stage-ok" aria-hidden="true">${Z.icon('check', 'xs')}</span>` : ''}<span class="zl-stage-n">Stage ${s.id}</span><span class="sr-only">: ${esc(s.name)}${stagePassed(s.id) ? ', passed' : ''}</span>${s.id === learnerStage ? '<i class="zl-you" aria-hidden="true"></i><span class="sr-only">, your stage</span>' : ''}
          </button>`).join('');
        paintStages();
      };
      const paintStages = () => stagesEl.querySelectorAll('[data-stage]').forEach(b => b.setAttribute('aria-pressed', String(+b.dataset.stage === view.stage)));

      /* ---------- Exit test card ---------- */
      const renderExit = () => {
        const s = stageOf(view.stage);
        const ex = exam('stage-' + s.id);
        const done = ex.passed.length > 0;
        const req = s.topics.filter(t => !t.optional);
        const nPassed = req.filter(passed).length;
        const opt = s.topics.filter(t => t.optional);
        const exit = /^[A-Z][a-z]/.test(s.exit) ? s.exit.charAt(0).toLowerCase() + s.exit.slice(1) : s.exit;
        const facts = [esc(s.name), hrs(s.hours), `<span class="zl-months">about ${MONTHS[s.id]} months at 15 h a week</span>`,
          done ? `Exit test passed with ${Math.max(...ex.passed.map(pctOf))}%` : `${nPassed} of ${req.length} topics passed`,
          ...(!done && ex.sat ? [`Best exit test ${Math.max(...ex.attempts.map(pctOf))}%`] : []),
          ...(opt.length ? [`${opt.map(t => t.id).join(', ')} optional`] : [])];
        const act = done
          ? `${chip('pass', 'lg')}<button type="button" class="link-btn zl-link" data-exam="stage-${s.id}">See results</button>`
          : s.id === 2
            ? '<button type="button" class="btn secondary" data-projects>Check your projects</button><button type="button" class="link-btn zl-link zl-tolink" data-view="paths">See the three paths</button>'
            : `<button type="button" class="btn secondary" data-exam="stage-${s.id}">${ex.sat ? 'Sit the exit test again' : 'Sit the exit test'}</button>`;
        exitEl.innerHTML = `
          <section class="card zl-exit${done ? ' is-done' : ''}" aria-label="Stage ${s.id} exit test">
            <span class="zl-exit-ico" aria-hidden="true">${Z.icon(done ? 'check' : s.id === 2 ? 'clipboard' : 'shield')}</span>
            <div class="zl-exit-t">
              <p class="zl-exit-p"><b>Exit test:</b> ${esc(exit)}</p>
              <p class="t-caption secondary tnum zl-facts">${facts.join('<span class="zl-dot" aria-hidden="true"> · </span>')}</p>
            </div>
            <div class="zl-exit-act">${act}</div>
          </section>`;
      };

      /* ---------- Track tabs ---------- */
      const renderTabs = () => {
        const s = stageOf(view.stage);
        tabsEl.innerHTML = TRACKS.map(k => {
          const n = k === 'all' ? s.topics.length : s.topics.filter(t => t.track === k).length;
          const name = k === 'all' ? 'All' : trackShort[k] || trackNames[k] || k;
          const sel = view.track === k;
          return `<button type="button" role="tab" class="zl-tab${n ? '' : ' is-empty'}" id="zl-tab-${k}" data-tab="${k}" ${k === 'all' ? '' : `data-track="${k}"`}
            aria-selected="${sel}" aria-controls="zl-panel" tabindex="${sel ? 0 : -1}">${esc(name)}<span class="zl-ct tnum" aria-label="${n} topic${n === 1 ? '' : 's'}">${n}</span></button>`;
        }).join('');
        topicsEl.setAttribute('aria-labelledby', 'zl-tab-' + view.track);
        fadeEdges();
      };
      const paintTabs = () => {
        tabsEl.querySelectorAll('[data-tab]').forEach(b => { const on = b.dataset.tab === view.track; b.setAttribute('aria-selected', String(on)); b.tabIndex = on ? 0 : -1; });
        topicsEl.setAttribute('aria-labelledby', 'zl-tab-' + view.track);
        const cur = tabsEl.querySelector('[aria-selected="true"]');
        if (cur) { // keep the selected tab in view inside the strip, without moving the page
          const l = cur.offsetLeft - tabsEl.offsetLeft, r = l + cur.offsetWidth;
          if (l < tabsEl.scrollLeft + 16) tabsEl.scrollTo({ left: Math.max(0, l - 24), behavior: reduced ? 'auto' : 'smooth' });
          else if (r > tabsEl.scrollLeft + tabsEl.clientWidth - 16) tabsEl.scrollTo({ left: r - tabsEl.clientWidth + 24, behavior: reduced ? 'auto' : 'smooth' });
        }
      };
      const fadeEdges = () => {
        const w = tabsEl.parentElement;
        w.classList.toggle('fade-r', tabsEl.scrollLeft + tabsEl.clientWidth < tabsEl.scrollWidth - 2);
        w.classList.toggle('fade-l', tabsEl.scrollLeft > 2);
      };
      tabsEl.addEventListener('scroll', fadeEdges, { passive: true });

      /* ---------- Course card ---------- */
      const card = (c, t) => {
        const p = prog(c.id), pct = Math.round(p * 100), s = courseState(c, t), cur = c.id === curId;
        const n = lessonsOf(c.id).length, w = writtenCount(c.id), mapOnly = n > 0 && w === 0;
        const counts = `${fmt(n)} lessons · ${c.levels.length} ${c.levels.length === 1 ? 'level' : 'levels'}`;
        const lim = C.readiness.limited(c.id);
        const pp = C.prepForCourse(c.id), tags = C.strandBadge(c.strand, c.strandNote) + C.prepChip(pp);
        const label = `${c.name}.${lim ? ` ${lim}.` : ''}${c.strand ? ` ${c.strand === 'pure' ? 'Pure maths' : 'Quant'}.` : ''}${pp.length ? ' Interview prep.' : ''} ${counts}${mapOnly ? ', map only, no lessons written yet' : w < n ? `, ${w} written` : ''}. ${pct}% done. ${STATE[s][0]}.${cur ? ' Your current course.' : ''}`;
        return `<button type="button" class="zl-card${cur ? ' is-current' : ''}${mapOnly ? ' is-map' : ''}" data-track="${t.track}" data-course="${c.id}" aria-label="${esc(label)}">
            <span class="zl-art" aria-hidden="true">${ZQArt(c.art)}</span>
            <span class="zl-body">
              ${cur ? '<span class="zl-cur" aria-hidden="true">Current</span>' : ''}
              <span class="zl-title">${esc(c.name)}</span>${pp.length ? `<span class="zl-tags">${tags}</span>` : tags}
              <span class="zl-label tnum">${counts}</span>${lim ? `<span class="zl-label zl-limited">${esc(lim)}</span>` : ''}
              <span class="zl-foot"><span class="bar thin track" aria-hidden="true"><i data-w="${pct}"></i></span><span class="zl-chips">${chip(s)}${mapOnly ? '<span class="zl-maponly">Map only</span>' : ''}</span></span>
            </span>
          </button>`;
      };

      /* ---------- Topic sections ---------- */
      const examChip = (t) => {
        const ex = exam('topic-' + t.id), min = examMinutes(t.hours);
        const sb = C.strandBadge(C.topicStrand(t), C.strandNoteOf(t.courses), 'is-sm');
        if (C.examWritten('topic-' + t.id) === false) return `<span class="zl-exam-chip is-unwritten" aria-label="${esc(`Topic exam for ${t.id} ${t.name}: not written yet.`)}">${Z.icon('shield', 'xs')}<span>Topic exam</span><span class="zl-sub">Not written yet</span>${sb}</span>`;
        const best = ex.sat ? Math.max(...ex.attempts.map(pctOf)) : 0;
        if (ex.passed.length) {
          const sc = Math.max(...ex.passed.map(pctOf));
          return `<button type="button" class="zl-exam-chip is-pass" data-exam="topic-${t.id}" aria-label="${esc(`Topic exam for ${t.id} ${t.name}: passed with ${sc}%. Open it again.`)}">${Z.icon('shield', 'xs')}<span>Topic exam</span><span class="zl-sub">Passed ${sc}%</span>${sb}</button>`;
        }
        if (ex.sat) return `<button type="button" class="zl-exam-chip" data-exam="topic-${t.id}" aria-label="${esc(`Topic exam for ${t.id} ${t.name}: not passed yet, best score ${best}%. Sit it again.`)}">${Z.icon('shield', 'xs')}<span>Topic exam</span><span class="zl-sub">Best ${best}%</span>${sb}</button>`;
        return `<button type="button" class="zl-exam-chip" data-exam="topic-${t.id}" aria-label="${esc(`Topic exam for ${t.id} ${t.name}: not sat. ${min} minutes, timed, 70% to pass. Sit it first to test out.`)}">${Z.icon('shield', 'xs')}<span>Topic exam</span><span class="zl-sub">${min} min</span>${sb}</button>`;
      };
      const resLink = (t) => {
        const r = t.resource;
        if (!r || !r.name) return '';
        return r.url
          ? `<a class="zl-res" href="${esc(r.url)}" target="_blank" rel="noopener">${Z.icon('book', 'xs')}<span>${esc(r.name)}</span><span class="sr-only"> (opens in a new tab)</span></a>`
          : `<span class="zl-res is-plain">${Z.icon('book', 'xs')}<span>${esc(r.name)}</span></span>`;
      };
      const topicHead = (t) => {
        const st = topicState(t), cs = topicCourses(t), lessons = cs.reduce((a, c) => a + lessonsOf(c.id).length, 0);
        const opt = !!t.optional;
        let close;
        if (opt) close = '';
        else if (CLOSE[t.id] && !exam('topic-' + t.id).sat) close = `<span class="zl-close">${Z.icon(CLOSE[t.id][0], 'xs')}<span>${esc(CLOSE[t.id][1])}</span></span>`;
        else close = examChip(t);
        return `<div class="zl-topic-head">
            <div class="zl-topic-t">
              <span class="t-overline zl-ov">${esc(trackNames[t.track] || '')}</span>
              <h2 class="zl-topic-h" id="zl-t-${t.id.replace('.', '-')}" tabindex="-1"><span class="zl-num tnum">${t.id}</span> ${esc(t.name)} <span class="zl-hrs tnum">· ${opt ? 'Optional' : hrs(t.hours)}</span></h2>
              <p class="zl-meta">${cs.length} course${cs.length === 1 ? '' : 's'} · ${lessons} lessons${notes[t.id] ? `<span class="zl-note">${esc(notes[t.id])}</span>` : ''}</p>
              ${t.exit ? `<p class="zl-target"><b>Target:</b> ${esc(t.exit)}</p>` : ''}
              ${resLink(t)}
            </div>
            <div class="zl-topic-chips">${C.strandBadge(C.topicStrand(t), C.strandNoteOf(t.courses), 'lg')}${chip(st, 'lg')}${close}</div>
          </div>`;
      };

      const emptyState = () => {
        const k = view.track, word = TRACK_WORD[k];
        const where = STAGES.filter(s => s.topics.some(t => t.track === k)).map(s => s.id);
        const list = where.length === 1 ? `Stage ${where[0]}` : `Stages ${where.slice(0, -1).join(', ')} and ${where[where.length - 1]}`;
        const target = where.includes(learnerStage) ? learnerStage : (where.find(n => n > learnerStage) ?? where[where.length - 1]);
        return `<div class="zl-empty" data-track="${k}">
            <span class="zl-empty-ico" aria-hidden="true">${Z.icon('learn')}</span>
            <h2 class="t-h2">Stage ${view.stage} has no ${esc(word)} topics</h2>
            <p class="t-body secondary">${esc(cap(word))} topics are in ${list}.</p>
            <button type="button" class="btn secondary" data-goto="${target}">Go to Stage ${target}</button>
          </div>`;
      };

      const fillBars = (scope, instant) => {
        const bars = scope.querySelectorAll('.bar > i[data-w]');
        if (reduced || instant) { bars.forEach(i => { i.style.width = i.dataset.w + '%'; }); return; }
        requestAnimationFrame(() => requestAnimationFrame(() => bars.forEach(i => { i.style.width = i.dataset.w + '%'; })));
      };

      /* mode: 'stage' rises in with the 80ms list stagger (spec 4.8); 'tab' is a 150ms cross-fade, no slide; '' is static */
      const renderTopics = (mode = '', instant = false) => {
        const s = stageOf(view.stage);
        const topics = s.topics.filter(inTrack);
        const anim = reduced ? '' : mode;
        topicsEl.classList.toggle('zl-xfade', anim === 'tab');
        if (anim === 'tab') { topicsEl.style.animation = 'none'; void topicsEl.offsetWidth; topicsEl.style.animation = ''; }
        topicsEl.innerHTML = topics.length ? topics.map((t, i) => `
          <section class="zl-topic${anim === 'stage' ? ' enter' : ''}" data-track="${t.track}" aria-labelledby="zl-t-${t.id.replace('.', '-')}" ${anim === 'stage' ? `style="animation-delay:${Math.min(i, 5) * 80}ms"` : ''}>
            ${topicHead(t)}
            <div class="zl-grid">${topicCourses(t).map(c => card(c, t)).join('')}</div>
          </section>`).join('') : emptyState();
        fillBars(topicsEl, instant);
      };

      /* ---------- Paths view ---------- */
      const stepData = (s) => {
        if (s.topic) {
          const t = C.topic(s.topic), first = topicCourses(t)[0];
          return { title: titleCase(t.name), meta: `${t.id} · ${s.meta || `${(t.courses || []).length} courses · ${hrs(t.hours)}`}`, art: first ? first.art : 'steps', track: t.track, go: first ? `course/${first.id}` : null };
        }
        if (s.course) {
          const c = courseOf(s.course);
          if (!c) return { title: s.course, meta: '', art: 'steps', track: 'fin', go: null };
          return { title: c.name, meta: `${c.topic}${s.tag ? ' · ' + s.tag : ''} · ${s.meta || `${lessonsOf(c.id).length} lessons`}`, art: c.art, track: c.track, go: `course/${c.id}` };
        }
        return { title: s.title, meta: `${s.topicId} · ${s.meta}`, art: s.art, track: s.track, go: null, projects: true };
      };
      const renderPaths = () => {
        const s2 = stageOf(2), s3 = stageOf(3), sto = C.topic('3.2'), ito = sto ? topicCourses(sto)[0] : null;
        const mineId = prof.track;
        const order = PATHS.some(p => p.id === mineId) ? [...PATHS].sort((a, b) => (b.id === mineId) - (a.id === mineId)) : PATHS;
        const intro = PATHS.some(p => p.id === mineId)
          ? `You chose the ${mineId} track. The three roles are interviewed differently, so each path makes different courses core. Every course stays open to you.`
          : 'The three roles are interviewed differently, so each path makes different courses core. Every course stays open to you.';
        pathsEl.innerHTML = `
          <section class="zl-paths-intro" aria-labelledby="zl-paths-h">
            <span class="t-overline muted tnum">Stage 2 · ${esc(s2.name)} · <span class="zl-unit">${hrs(s2.hours)}</span></span>
            <h2 class="zl-paths-h" id="zl-paths-h">${PATHS.some(p => p.id === mineId) ? 'Your path through Stage 2' : 'Choose a track before Stage 2'}</h2>
            <p class="t-body secondary">${esc(intro)}</p>
          </section>
          <div class="zl-paths">${order.map((p, pi) => {
            const mine = p.id === mineId;
            return `<section class="zl-path${mine ? ' is-mine' : ''}${reduced ? '' : ' enter'}" aria-labelledby="zl-p-${p.id}" ${reduced ? '' : `style="animation-delay:${pi * 80}ms"`}>
                <div class="zl-path-head">
                  <h3 class="zl-path-h" id="zl-p-${p.id}">${p.id}</h3>
                  ${mine ? '<span class="zl-mine">Your track</span>' : ''}
                </div>
                <div class="zl-tests">
                  <span class="t-overline muted">Interviews test</span>
                  <p class="t-body">${esc(p.tests)}</p>
                </div>
                <div class="zl-stack">
                  <span class="t-overline muted">Core, in order</span>
                  <ol class="zl-steps">${p.steps.map((st, i) => {
                    const d = stepData(st);
                    return `<li><button type="button" class="zl-step" data-track="${d.track}" ${d.go ? `data-go="${esc(d.go)}"` : 'data-projects'} aria-label="${esc(`Step ${i + 1}: ${d.title}. ${d.meta}.`)}">
                        <span class="zl-step-n tnum" aria-hidden="true">${i + 1}</span>
                        <span class="zl-step-art" aria-hidden="true">${ZQArt(d.art)}</span>
                        <span class="zl-step-t"><span class="zl-step-name">${esc(d.title)}</span><span class="zl-step-meta tnum">${esc(d.meta)}</span></span>
                      </button></li>`;
                  }).join('')}</ol>
                </div>
              </section>`;
          }).join('')}</div>
          ${sto && ito ? `<section class="zl-opt card" data-track="${sto.track}" aria-labelledby="zl-opt-h">
            <div class="zl-opt-t">
              <div class="zl-opt-top"><span class="t-overline zl-ov">Stage 3 · ${esc(trackNames[sto.track] || '')}</span><span class="zl-chip is-opt">Optional</span></div>
              <h2 class="zl-topic-h" id="zl-opt-h"><span class="zl-num tnum">${esc(sto.id)}</span> ${esc(sto.name)}</h2>
              <p class="t-body secondary">Hours not counted. Needed for derivatives pricing and desk quant roles. Rarely tested for trading or statistical research roles.</p>
              <div class="zl-ito">${Z.tex("df(W_t) = f'(W_t)\\,dW_t + \\tfrac{1}{2}\\,f''(W_t)\\,dt", true)}<span class="t-caption secondary">Itô’s lemma for a function of Brownian motion. The ${Z.tex("\\tfrac{1}{2} f''(W_t)\\,dt")} term is what ordinary calculus misses.</span></div>
            </div>
            <button type="button" class="zl-step zl-opt-course" data-go="course/${esc(ito.id)}" aria-label="${esc(`${ito.name}. ${lessonsOf(ito.id).length} lessons. Optional.`)}">
              <span class="zl-step-art" aria-hidden="true">${ZQArt(ito.art)}</span>
              <span class="zl-step-t"><span class="zl-step-name">${esc(ito.name)}</span><span class="zl-step-meta tnum">${lessonsOf(ito.id).length} lessons · ${ito.levels.length} levels</span></span>
              ${Z.icon('chevronR', 'sm')}
            </button>
          </section>` : ''}
          <p class="t-caption secondary zl-paths-foot">All three paths end at the Stage 3 exit test: ${esc(s3.exit)}.</p>`;
      };

      /* ---------- View switching ---------- */
      const paintView = () => {
        root.querySelectorAll('.zl-toggle [data-view]').forEach(b => b.setAttribute('aria-pressed', String(b.dataset.view === view.view)));
        const paths = view.view === 'paths';
        coursesEl.hidden = paths; pathsEl.hidden = !paths;
        if (paths && !pathsEl.childElementCount) renderPaths();
      };

      /* Keep the tab strip at the top of the viewport when a filter shrinks the list.
         stickTop reads the strip's sticky offset, which includes the safe-area inset. */
      const tabsWrap = $('.zl-tabs-wrap');
      const stickTop = () => parseFloat(getComputedStyle(tabsWrap).top) || 0;
      const stripTop = () => exitEl.getBoundingClientRect().bottom + window.scrollY + (parseFloat(getComputedStyle(coursesEl).rowGap) || 0) - stickTop();
      const settle = () => {
        const top = stripTop();
        if (window.scrollY > top + 1) window.scrollTo({ top, behavior: 'auto' });
      };
      /* Stage 2's exit is three projects: bring 2.3 Projects into view under the stuck strip */
      const showProjects = () => {
        if (view.view !== 'courses') { view.view = 'courses'; paintView(); }
        if (view.stage !== 2) setStage(2);
        if (!$('#zl-t-2-3')) setTrack('all');
        const h = $('#zl-t-2-3'); if (!h) return;
        const sec = h.closest('.zl-topic');
        const top = sec.getBoundingClientRect().top + window.scrollY - stickTop() - tabsWrap.offsetHeight - 12;
        window.scrollTo({ top: Math.max(0, top), behavior: reduced ? 'auto' : 'smooth' });
        h.focus({ preventScroll: true });
      };

      const setStage = (n) => {
        if (n === view.stage) return;
        view.stage = n; paintStages(); renderExit(); renderTabs(); renderTopics('stage'); settle();
      };
      const setTrack = (k) => {
        if (k === view.track) return;
        view.track = k; paintTabs(); renderTopics('tab'); settle();
      };

      /* ---------- Events ---------- */
      const onClick = (e) => {
        const b = e.target.closest('button'); if (!b || !root.contains(b)) return;
        if (b.dataset.stage != null) { setStage(+b.dataset.stage); return; }
        if (b.dataset.tab) { setTrack(b.dataset.tab); return; }
        if (b.dataset.goto != null) { setStage(+b.dataset.goto); stagesEl.querySelector(`[data-stage="${b.dataset.goto}"]`)?.focus(); return; }
        if (b.dataset.view) {
          const was = view.view; view.view = b.dataset.view; paintView();
          if (was !== view.view && b.classList.contains('zl-tolink')) { window.scrollTo(0, 0); root.querySelector('.zl-toggle [data-view="paths"]').focus(); }
          return;
        }
        if (b.dataset.exam) { Z.go('exam/' + b.dataset.exam); return; }
        if (b.hasAttribute('data-projects')) { showProjects(); return; }
        if (b.dataset.course) { Z.go('course/' + b.dataset.course); return; }
        if (b.dataset.go) Z.go(b.dataset.go);
      };
      root.addEventListener('click', onClick);

      /* Arrow keys move between track tabs (automatic activation) */
      tabsEl.addEventListener('keydown', (e) => {
        const keys = { ArrowRight: 1, ArrowLeft: -1, Home: 'first', End: 'last' };
        if (!(e.key in keys)) return;
        e.preventDefault();
        const i = TRACKS.indexOf(view.track), k = keys[e.key];
        const j = k === 'first' ? 0 : k === 'last' ? TRACKS.length - 1 : (i + k + TRACKS.length) % TRACKS.length;
        setTrack(TRACKS[j]);
        tabsEl.querySelector(`[data-tab="${TRACKS[j]}"]`)?.focus();
      });

      const onResize = () => fadeEdges();
      window.addEventListener('resize', onResize);

      renderStages(); renderExit(); renderTabs(); renderTopics(); paintView();
      requestAnimationFrame(paintTabs);

      /* Learner state changed: redraw the numbers in place, keeping the stage, tab, view and scroll position */
      let raf = 0, lastSig = JSON.stringify(sum);
      onState = () => {
        cancelAnimationFrame(raf);
        raf = requestAnimationFrame(() => {
          if (!root.isConnected) return;
          read();
          const sig = JSON.stringify(sum) + JSON.stringify(S.exams);
          if (sig === lastSig) return;
          lastSig = sig;
          const y = window.scrollY;
          renderStages(); renderExit(); renderTopics('', true);
          if (pathsEl.childElementCount) renderPaths();
          window.scrollTo(0, y);
        });
      };
      lastSig = JSON.stringify(sum) + JSON.stringify(S.exams);

      return () => { onState = null; cancelAnimationFrame(raf); window.removeEventListener('resize', onResize); };
    },
  });
})();
