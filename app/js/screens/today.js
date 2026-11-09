/* Today (Home) and the mental arithmetic warm-up.
   Spec: 7.2 Today, 6.2 streak, rest days and weekly goal, 2.6 charts, 4 motion, 9.2 voice.
   Curriculum: the weekly rhythm (9 / 3 / 2 / 1 h at 15 h) and the two daily habits
   (10 minutes of mental arithmetic a day; three probability problems a week from 1.5).
   Layout modes: under 768px the mobile order; 768 to 1023 one column of the desktop cards;
   1024 and up two columns, the left 480px. Cards are moved between modes, never duplicated,
   so reading order and focus order always match what is on screen.
   Data: every number comes from ZQ.state.summary() and the ZQ.state getters, every list from ZQ.content.
   The screen rebuilds itself on the 'state' event when the summary has changed. Launching a lesson sets
   window.ZQLaunch ({ course, id, kind, wasDone, qualifiedBefore, at }); the course map reads it on return
   to play the completion animation. */
(function () {
  'use strict';

  /* Shared across visits to these two screens in one session. shown: what the goal bar and ring last drew,
     so their fills animate only when a value has changed (spec 1: celebration is kept for the boundaries). */
  const session = { shown: null };

  /* Weekly rhythm from the curriculum. Chart slots 1 to 4 in fixed order (spec 2.6). Goals come from ZQ.state.weeklySplit. */
  const BLOCKS = [
    { key: 'main', name: 'Main subject', slot: '--s1' },
    { key: 'build', name: 'Build', slot: '--s2' },
    { key: 'review', name: 'Review', slot: '--s3' },
    { key: 'mental', name: 'Mental arithmetic', slot: '--s4' },
  ];

  /* The 9 / 3 / 2 / 1 split scaled to the goal. ZQ.state.weeklySplit is used when its blocks add up to the goal;
     otherwise (its three shared blocks divide by 7 rather than 14) the same rule is computed here: mental stays at 1 h,
     the rest share 9 : 3 : 2 in half hours. */
  const weeklySplit = (S, h) => {
    try { const s = S.weeklySplit(h); if (s && Math.abs(s.main + s.build + s.review + s.mental - h) < 0.01) return s; } catch { /* compute below */ }
    const rest = Math.max(0, h - 1), raw = [9, 3, 2].map(w => rest * w / 14);
    const halves = raw.map(v => Math.floor(v * 2)); let left = Math.round(rest * 2) - halves.reduce((a, b) => a + b, 0);
    raw.map((v, i) => [v * 2 - Math.floor(v * 2), i]).sort((a, b) => b[0] - a[0] || a[1] - b[1]).forEach(([, i]) => { if (left > 0) { halves[i]++; left--; } });
    const [main, build, review] = halves.map(v => v / 2);
    return { main, build, review, mental: Math.min(1, h) };
  };

  /* Warm-up settings: content/warmup.json, with the same values as a fallback while it loads */
  const WARM = {
    seconds: 120, demoSeconds: 10, roundsADay: 5, minutesADay: 10, targets: { stage0: 25, stage3: 50 }, trendLength: 10,
    operations: [
      { id: 'add', symbol: '+', tex: '+', a: [2, 100], b: [2, 100] },
      { id: 'sub', symbol: '-', tex: '-', inverseOf: 'add' },
      { id: 'mul', symbol: '×', tex: '\\times', a: [2, 12], b: [2, 100] },
      { id: 'div', symbol: '÷', tex: '\\div', inverseOf: 'mul' },
    ],
  };
  const warmReady = fetch('content/warmup.json', { cache: 'no-cache' })
    .then(r => (r.ok ? r.json() : null)).then(j => { if (j && typeof j === 'object') Object.assign(WARM, j); })
    .catch(() => { /* keep the defaults */ });

  /* One 'state' listener for the module; the mounted screen sets onState and clears it on leave (core.js has no off) */
  let onState = null;
  ZQ.on('state', (e) => { if (onState) onState(e); });

  /* Lesson file facts (screens, minutes) once loaded, keyed course/lesson */
  const lessonMeta = {};

  /* Lower case, no apostrophes, no accents: "Bayes’ rule" matches "bayes rule", "Itô" matches "ito" */
  const norm = (s) => String(s).toLowerCase().replace(/[’‘']/g, '').normalize('NFD').replace(/[\u0300-\u036f]/g, '');
  const fmtH = (v) => String(Math.round(v * 10) / 10);
  const plural = (n, one, many) => `${n} ${n === 1 ? one : many}`;
  const greeting = () => { const h = new Date().getHours(); return h >= 4 && h < 12 ? 'Good morning' : h >= 12 && h < 17 ? 'Good afternoon' : 'Good evening'; };
  const longDate = () => new Date().toLocaleDateString('en-GB', { weekday: 'long', day: 'numeric', month: 'long' }).replace(',', '');
  const shortDate = (t) => new Date(t).toLocaleDateString('en-GB', { weekday: 'short', day: 'numeric', month: 'short' }).replace(',', '');
  const pctOf = (a) => { // an exam attempt's score as a percentage, whatever scale it was stored on
    if (!a) return 0;
    const s = Number(a.score) || 0, n = Number(a.items) || 0;
    if (n > 0 && s <= n && s > 1) return Math.round(s / n * 100);
    return Math.round(s <= 1 ? s * 100 : s);
  };

  /* ---------- Where the learner is: shared by Today, Learn and the course map (each file keeps its own copy) ---------- */
  const keyOf = (c, l) => `${c}/${l}`;
  const itemDone = (S, cid, x) => {
    if (x.kind === 'lesson') { const r = S.lessons[keyOf(cid, x.id)]; return !!(r && r.done); }
    if (x.kind === 'review') return !!S.reviews[keyOf(cid, x.id)];
    const h = S.homework[keyOf(cid, x.id)]; return !!(h && h.submitted);
  };
  /* Prerequisite gating (ENGINE-BACKLOG 486): the next lesson is the first one not done that is unlocked; anyLock reads past the locks */
  const nextLesson = (Z, cid, anyLock) => Z.content.courseLessons(cid).find(x => x.kind === 'lesson' && x.written === true && !itemDone(Z.state, cid, x) && (anyLock || !Z.prereq || !Z.prereq.lessonLocked(cid, x.id))) || null;
  /* The resume course if a lesson is open (not one in a tested-out course left since the pass, ENGINE-BACKLOG 461); else the first course in curriculum order, from the learner's starting stage,
     that is not finished and has a written lesson still to do. null when no written lesson is left anywhere. */
  const currentCourse = (Z, sum, anyLock) => {
    const C = Z.content;
    const track = Z.state.profile.get().track;
    if (sum.resume && C.course(sum.resume.course) && C.resumeStands(sum.resume) && C.readiness.offerable(sum.resume.course, track)) return sum.resume.course;
    const start = Number(Z.state.profile.startStage) || 0;
    const open = C.readiness.plan(C.courses(), track).filter(c => (sum.courseProgress[c.id] || 0) < 1 && nextLesson(Z, c.id, anyLock));
    /* A course in a passed topic is skipped; it is chosen only when nothing else has a lesson left */
    const fresh = open.filter(c => !C.courseTestedOut(c.id));
    const c = fresh.find(x => x.stage >= start) || fresh[0] || open[0];
    return c ? c.id : null;
  };
  /* With nothing written to do: the first course of the learner's starting stage, for its map and its topic resource */
  const fallbackCourse = (Z) => {
    const start = Number(Z.state.profile.startStage) || 0;
    const all = Z.content.courses();
    const c = all.find(x => x.stage === start) || all[0];
    return c ? c.id : null;
  };

  /* ---------- Tooltip shared by the two charts (values lead, labels follow; textContent only) ---------- */
  const showTip = (wrap, tip, x, y, strong, light) => {
    tip.replaceChildren();
    const b = document.createElement('b'); b.textContent = strong;
    const s = document.createElement('span'); s.textContent = light;
    tip.append(b, s); tip.hidden = false;
    const ww = wrap.clientWidth, tw = tip.offsetWidth;
    tip.style.left = Math.max(0, Math.min(ww - tw, x - tw / 2)) + 'px';
    tip.style.top = (y - tip.offsetHeight - 10) + 'px';
  };

  /* Pointer, touch and keyboard reading for a chart with n positions along x.
     A tap fires no pointermove, so pointerdown picks the point; the focus that follows keeps it. */
  const hoverable = (svg, n, indexAt, show, hide) => {
    let idx = -1;
    const set = (i) => { idx = i; if (i < 0) hide(); else show(i); };
    const at = (e) => { const r = svg.getBoundingClientRect(); return indexAt(e.clientX - r.left, r.width); };
    svg.addEventListener('pointermove', (e) => set(at(e)));
    svg.addEventListener('pointerdown', (e) => set(at(e)));
    /* A finger "leaves" on lift, before the tap's focus arrives, so only a mouse or pen leaving hides the reading */
    svg.addEventListener('pointerleave', (e) => { if (e.pointerType !== 'touch' && document.activeElement !== svg) set(-1); });
    svg.addEventListener('focus', () => { if (idx < 0) set(n - 1); });
    svg.addEventListener('blur', () => set(-1));
    svg.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowLeft' || e.key === 'ArrowRight') { e.preventDefault(); set(Math.max(0, Math.min(n - 1, (idx < 0 ? n - 1 : idx) + (e.key === 'ArrowLeft' ? -1 : 1)))); }
      if (e.key === 'Home') { e.preventDefault(); set(0); }
      if (e.key === 'End') { e.preventDefault(); set(n - 1); }
    });
  };

  /* Sparkline: one series, the speed track gold, endpoint emphasised with a surface ring. Needs two or more values. */
  const sparkline = (wrap, values) => {
    const W = 168, H = 56, P = 9, n = values.length;
    if (n < 2) { wrap.innerHTML = `<span class="t-caption muted zt-spark-empty">Your trend shows after two rounds.</span>`; return; }
    const lo = Math.min(...values), hi = Math.max(...values);
    const x = (i) => P + i * (W - 2 * P) / (n - 1);
    const y = (v) => H - P - (v - lo) / Math.max(1, hi - lo) * (H - 2 * P);
    const d = values.map((v, i) => `${i ? 'L' : 'M'}${x(i).toFixed(1)},${y(v).toFixed(1)}`).join(' ');
    wrap.innerHTML = `<svg viewBox="0 0 ${W} ${H}" width="${W}" height="${H}" tabindex="0" role="img"
        aria-label="Your last ${n} scores, oldest first: ${values.join(', ')}. Use the arrow keys to read each one.">
        <line class="zt-cross" x1="0" x2="0" y1="2" y2="${H - 2}" visibility="hidden"/>
        <path class="zt-sline" d="${d}"/>
        <circle class="zt-hot" r="4" visibility="hidden"/>
        <circle class="zt-end" cx="${x(n - 1).toFixed(1)}" cy="${y(values[n - 1]).toFixed(1)}" r="4.5"/>
      </svg><div class="zt-tip" hidden></div>`;
    const svg = wrap.querySelector('svg'), tip = wrap.querySelector('.zt-tip');
    const cross = svg.querySelector('.zt-cross'), hot = svg.querySelector('.zt-hot');
    hoverable(svg, n, (px, w) => Math.max(0, Math.min(n - 1, Math.round((px * W / w - P) / ((W - 2 * P) / (n - 1))))), (i) => {
      cross.setAttribute('x1', x(i)); cross.setAttribute('x2', x(i)); cross.setAttribute('visibility', 'visible');
      hot.setAttribute('cx', x(i)); hot.setAttribute('cy', y(values[i])); hot.setAttribute('visibility', i === n - 1 ? 'hidden' : 'visible');
      const back = n - 1 - i;
      showTip(wrap, tip, x(i), y(values[i]), String(values[i]), back === 0 ? 'Last round' : plural(back, 'round', 'rounds') + ' before');
    }, () => { cross.setAttribute('visibility', 'hidden'); hot.setAttribute('visibility', 'hidden'); tip.hidden = true; });
  };

  /* =====================================================================================
     TODAY
     ===================================================================================== */
  ZQ.screen({
    id: 'today', title: 'Today', group: 'App', shell: true, tab: 'today',
    render(root, Z) {
      let teardown = null, lastSig = '', raf = 0;
      const sig = () => { try { return JSON.stringify(Z.state.summary()) + '|' + Z.state.notebook.list().length; } catch { return String(Math.random()); } };
      const build = (restore) => {
        lastSig = sig();
        teardown = renderToday(root, Z, restore);
      };
      onState = () => {
        cancelAnimationFrame(raf);
        raf = requestAnimationFrame(() => {
          if (!root.isConnected || sig() === lastSig) return;
          const q = root.querySelector('#zt-q');
          const restore = { y: window.scrollY, q: q ? q.value : '', focus: q && document.activeElement === q };
          if (teardown) teardown();
          build(restore);
        });
      };
      build(null);
      return () => { onState = null; cancelAnimationFrame(raf); if (teardown) teardown(); };
    },
  });

  function renderToday(root, Z, restore) {
    const C = Z.content, S = Z.state, esc = Z.esc;
    const sum = S.summary();
    const offs = [];
    const listen = (target, ev, fn, opt) => { target.addEventListener(ev, fn, opt); offs.push(() => target.removeEventListener(ev, fn, opt)); };
    let alive = true;
    offs.push(() => { alive = false; });

    /* ---------- Course and level state ---------- */
    const curId = currentCourse(Z, sum);
    const cid = curId || fallbackCourse(Z);
    /* The course the learner would be on if nothing were locked: when its next lesson is locked, Today says so and offers Start here */
    const wantId = currentCourse(Z, sum, true), wantNext = wantId && wantId !== curId ? nextLesson(Z, wantId, true) : null;
    const wantMissing = wantNext && Z.prereq && Z.prereq.lessonLocked(wantId, wantNext.id) ? Z.prereq.missingFor(wantId, wantNext.id) : null;
    const co = cid ? C.course(cid) : null;
    const list = cid ? C.courseLessons(cid) : [];
    const lessonNo = {}; list.filter(x => x.kind === 'lesson').forEach((x, i) => { lessonNo[x.id] = i + 1; });
    const resume = sum.resume && sum.resume.course === cid && C.resumeStands(sum.resume) ? sum.resume : null;
    const curItem = resume ? list.find(x => x.id === resume.lesson) || null : (curId ? nextLesson(Z, cid) : null);
    const levels = co ? co.levels : [];
    const curLevel = Math.max(0, curItem ? levels.findIndex(lv => lv.n === curItem.level) : 0);
    const anyDone = list.some(x => itemDone(S, cid, x));
    const levelInfo = (i) => {
      const lv = levels[i];
      const items = list.filter(x => x.level === lv.n);
      const isCurrent = !!curItem && curItem.level === lv.n;
      const next = isCurrent ? curItem
        : items.find(x => x.kind === 'lesson' && x.written === true && !itemDone(S, cid, x))
          || items.find(x => x.kind === 'lesson') || null;
      return { lv, next, isCurrent, no: next ? lessonNo[next.id] : 0, done: items.filter(x => itemDone(S, cid, x)).length, total: items.length };
    };
    const art = (lv) => [(lv && lv.art) || (co && co.art) || 'steps', lv ? lv.name : ''];
    const track = co ? co.track || 'prob' : 'prob';
    const topic = co ? C.topic(co.topic) : null;
    const resource = topic && topic.resource;

    /* ---------- Numbers ---------- */
    const goal = sum.weeklyGoalH || 15;
    const split = weeklySplit(S, goal);
    const blocks = BLOCKS.map(b => ({ ...b, goal: split[b.key], done: sum.hoursWeek[b.key] || 0 }));
    const doneH = sum.hoursWeekTotal;
    /* Readiness for the topic exam: mastery averaged over every skill the topic's courses teach */
    const topicSkills = topic ? [...new Set((topic.courses || []).flatMap(id => Object.keys((C.course(id) || {}).skills || {})))] : [];
    const examPct = topicSkills.length ? Math.round(topicSkills.reduce((a, s) => a + (sum.skillMastery[s] || 0), 0) / topicSkills.length * 100) : 0;
    const examRec = topic ? S.exams['topic-' + topic.id] : null;
    const attempts = examRec && Array.isArray(examRec.attempts) ? examRec.attempts : [];
    const passedAt = attempts.filter(a => a.passed);
    const trend = sum.warmupTrend;
    const today = S.dates.todayKey();
    const roundsToday = S.warmup.list().filter(e => e.date === today).length;
    const roundsADay = WARM.roundsADay || 5;

    /* Fills animate on the first visit and when a value changes; a changed fill grows from where it was */
    const fills = blocks.map(b => (b.goal > 0 ? Math.min(100, b.done / b.goal * 100) : 0).toFixed(1));
    const prev = session.shown;
    const goalGrow = !prev || prev.fills.join() !== fills.join();
    const growFrom = (i) => (prev && +fills[i] > 0 ? Math.min(1, prev.fills[i] / fills[i]).toFixed(3) : 0);
    const ringGrow = !prev || prev.exam !== examPct;
    session.shown = { fills, exam: examPct };

    /* ---------- Parts ---------- */
    const restPills = (big) => `<span class="${big ? 'zt-pills' : 'rest-slots'}" aria-hidden="true">${[0, 1].map(i => `<i class="${i < sum.restDays ? 'on' : ''}"></i>`).join('')}</span>`;
    const hello = sum.name ? `${greeting()}, ${esc(sum.name)}` : greeting();
    const P = {};

    P.top = `<div class="zt-top" data-part="top">
        <h1 class="sr-only">${hello}</h1>
        <span class="zt-date">${esc(longDate())}</span>
        <button class="streak-pill" type="button" data-streak ${sum.streakOff ? 'hidden' : ''} aria-label="Streak ${sum.streak} days, ${sum.restDays} of 2 rest days. Open streak details.">${sum.streak}${Z.bolt(sum.todayQualified)}${restPills(false)}</button>
      </div>`;

    /* The done state is carried by the streak card and the deck's "Done for today.", so the greeting stays one line */
    P.hello = `<header class="zt-hello" data-part="hello"><h1 class="t-h1">${hello}</h1></header>`;

    P.search = `<div class="zt-search" data-part="search" role="search">
        <div class="zt-pill">${Z.icon('search', 'sm')}
          <input type="search" id="zt-q" placeholder="Search courses, lessons, formulas" aria-label="Search courses, lessons, formulas" autocomplete="off" spellcheck="false"
            role="combobox" aria-expanded="false" aria-controls="zt-results" aria-autocomplete="list"></div>
        <ul class="zt-results" id="zt-results" role="listbox" aria-label="Results" hidden></ul>
      </div>`;

    const streakTop = sum.streakOff ? '' : `<button class="zt-streak-top" type="button" data-streak aria-label="Streak ${sum.streak} days, ${sum.restDays} of 2 rest days held. Open streak details.">
          <span class="t-stat">${sum.streak}</span>${Z.bolt(sum.todayQualified, 'xl')}
          <span class="zt-streak-l"><span class="t-h2">day streak</span>
            <span class="t-caption muted">${sum.todayQualified ? `Today counts. Tomorrow makes it ${sum.streak + 1}.` : 'One lesson or three problems keeps it going.'}</span></span>
          <span class="zt-rest">${restPills(true)}<span class="t-caption muted">${sum.restDays} of 2 rest days</span></span>
        </button>
        ${Z.weekStrip(sum.week, sum.todayQualified)}`;
    P.streak = `<section class="card zt-streak${sum.streakOff ? ' is-off' : ''}" data-part="streak" aria-label="${sum.streakOff ? 'Weekly goal' : 'Streak and weekly goal'}">
        ${streakTop}
        <div class="zt-goal">
          <div class="zt-goal-head"><span class="t-overline muted">Weekly goal</span><span class="t-label tnum"><b>${fmtH(doneH)}</b> of ${fmtH(goal)} h</span></div>
          <div class="zt-hbar ${goalGrow ? 'grow' : ''}" role="img" aria-label="${fmtH(doneH)} of ${fmtH(goal)} hours this week. ${blocks.map(b => `${b.name} ${fmtH(b.done)} of ${fmtH(b.goal)}`).join(', ')}.">
            ${blocks.map((b, i) => `<span class="zt-seg" style="--g:${b.goal};--c:var(${b.slot})"><i style="width:${fills[i]}%;--from:${growFrom(i)}"></i></span>`).join('')}
          </div>
          <ul class="zt-keys" aria-hidden="true">${blocks.map(b => `<li style="--c:var(${b.slot})"><i class="zt-sw"></i><span class="t-label tnum">${fmtH(b.done)} of ${fmtH(b.goal)} h</span><span class="t-caption secondary">${b.name}</span></li>`).join('')}</ul>
        </div>
      </section>`;

    const dueRow = (icon, title, meta, go) => `<li><button class="zt-row" type="button" data-go="${esc(go)}">
        <span class="zt-ico">${Z.icon(icon, 'sm')}</span>
        <span class="zt-row-t"><span class="t-label">${title}</span><span class="t-caption muted">${meta}</span></span>
        ${Z.icon('chevronR', 'sm zt-chev')}</button></li>`;
    const hwRow = (h) => {
      const n = (String(h.id).match(/homework-(\d+)/) || [])[1];
      const cname = (C.course(h.course) || {}).name || h.course;
      const when = h.due ? (h.overdue ? `Overdue, it was due ${esc(shortDate(h.due))}` : `Due ${esc(shortDate(h.due))}`) : 'No due date';
      return dueRow('clipboard', `${n ? 'Homework ' + n + ' · ' : 'Homework · '}${esc(cname)}`, when, 'review');
    };
    /* Weekly probability problems, once ZQ.select.weeklyStatus() reports the feature active (a 1.5 lesson finished) */
    let weekly = null;
    try { const ws = ZQ.select && ZQ.select.weeklyStatus ? ZQ.select.weeklyStatus() : null; if (ws && ws.eligible) weekly = ws; } catch (e) { console.error(e); }
    /* ENGINE-BACKLOG 825: the weekly mixed review, due once a week from the first level met (ZQ.state.cumulative); postponing keeps it here */
    let cumRow = '';
    try {
      const cs = ZQ.select && ZQ.select.cumulativeStatus ? ZQ.select.cumulativeStatus() : null;
      if (cs && cs.eligible && cs.due) {
        cumRow = dueRow('review', 'Weekly mixed review', cs.postponedToday ? 'Postponed today. It stays due.' : `20 questions from every level you have met · about 20 minutes${cs.overdueDays > 0 ? ` · due since ${esc(shortDate(cs.dueAt))}` : ''}`, 'weekly');
      }
    } catch (e) { console.error(e); }
    /* ENGINE-BACKLOG 810: practice after the due work: a generated fluency set whose lesson is done and that has not been passed yet, the newest lesson first */
    let flu = [];
    try {
      flu = (C.fluencyList ? C.fluencyList() : []).filter(r => { const l = S.lesson(r.course, r.lesson), f = S.fluency.get(r.course, r.id); return !!(l && l.done) && !(f && f.passedAt); })
        .sort((x, y) => ((S.lesson(y.course, y.lesson) || {}).completedAt || 0) - ((S.lesson(x.course, x.lesson) || {}).completedAt || 0));
    } catch (e) { console.error(e); }
    const fluRow = (r) => dueRow('target', esc(r.title || 'Fluency'), `${r.n} fresh questions · about ${r.minutes} minutes`, `fluency/${r.course}/${r.id}`);
    const practice = flu.length ? `<h3 class="t-overline muted zt-prac-h" id="zt-prac-h">Practice</h3>
        <ul aria-labelledby="zt-prac-h" data-fluency-rows>${flu.slice(0, 2).map(fluRow).join('')}</ul>${flu.length > 2 ? `<p class="t-caption muted zt-prac-more">${plural(flu.length - 2, 'more fluency set', 'more fluency sets')} on the course maps.</p>` : ''}` : '';
    P.due = `<section class="card zt-due" data-part="due" aria-labelledby="zt-due-h">
        <h2 class="t-h2" id="zt-due-h">Due</h2>
        <ul>
          ${sum.redoDue ? dueRow('review', plural(sum.redoDue, 'redo problem', 'redo problems'), `About ${sum.redoMinutes} minutes`, 'review')
            : dueRow('check', 'Redo queue clear', sum.redoTotal ? `Nothing due today. ${plural(sum.redoTotal, 'problem comes', 'problems come')} back later.` : 'Nothing due today', 'review')}
          ${sum.homeworkOpen.slice(0, 2).map(hwRow).join('')}
          ${weekly ? dueRow('star', `Weekly probability problems: ${weekly.done} of ${weekly.total}`, weekly.done >= weekly.total ? 'Done for this week. Three new ones arrive on Monday.' : 'About 2 minutes each', 'practice/weekly') : ''}
          ${cumRow}
        </ul>
        ${practice}
      </section>`;

    const lastScore = sum.warmupLast;
    P.warm = `<section class="card zt-warm" data-part="warm" data-track="speed" aria-labelledby="zt-warm-h">
        <div class="zt-warm-head"><span class="t-overline zt-deep">Daily warm-up</span><h2 class="t-h2" id="zt-warm-h">Mental arithmetic</h2></div>
        <div class="zt-warm-body">
          <div class="zt-warm-score"><span class="t-stat">${lastScore == null ? 0 : lastScore}</span><span class="t-caption muted">${lastScore == null ? 'No rounds yet' : 'Last score'}</span></div>
          <div class="zt-spark" data-spark></div>
        </div>
        <p class="t-caption secondary zt-warm-note">${roundsToday >= roundsADay ? `All ${roundsADay} rounds done. That is your ${WARM.minutesADay || 10} minutes today.`
          : roundsToday ? `${roundsToday} of ${roundsADay} rounds done today.` : `${cap(numWord(roundsADay))} ${Math.round((WARM.seconds || 120) / 60)}-minute rounds make your ${WARM.minutesADay || 10} minutes a day.`}</p>
        <button class="btn secondary block" type="button" data-go="warmup">${Z.icon('timer', 'sm')}Start ${Math.round((WARM.seconds || 120) / 60)}-minute drill</button>
      </section>`;

    if (wantMissing) {
      const wc = C.course(wantId) || {};
      P.lock = `<section class="lk-line" data-part="lock" aria-label="Locked course">${Z.icon('lock')}<span class="t-body">${esc(wc.name || wantId)} is locked until ${plural(wantMissing.count, 'thing', 'things')} before it ${wantMissing.count === 1 ? 'is' : 'are'} met.</span>
        ${wantMissing.start ? `<button class="btn secondary" type="button" data-go="${esc(wantMissing.start.route)}">Start here</button>` : `<button class="btn secondary" type="button" data-go="lesson/${esc(wantId)}/${esc(wantNext.id)}">See what is missing</button>`}</section>`;
    }
    P.jump = co ? `<section class="zt-jump" data-part="jump" data-track="${track}" aria-labelledby="zt-jump-h">
        <h2 class="t-h1" id="zt-jump-h">${anyDone || resume ? 'Jump back in' : 'Start here'}</h2>
        <div class="zt-deck"><div class="zt-deck-card" data-deck></div></div>
        ${levels.length > 1 ? `<div class="zt-thumbs" role="group" aria-label="Levels" style="grid-template-columns:repeat(${Math.min(levels.length, 5)}, minmax(0, 1fr))">
          ${levels.map((lv, i) => `<button class="zt-thumb" type="button" data-level="${i}" aria-pressed="false" aria-label="Level ${lv.n}, ${esc(lv.name)}">
            <span class="zt-thumb-art">${ZQArt(art(lv)[0])}</span><span class="t-caption">Level ${lv.n}</span>
            <span class="zt-tick" aria-hidden="true">${Z.icon('check')}</span></button>`).join('')}
        </div>` : ''}
      </section>` : '';

    P.hero = co ? `<section class="zt-hero" data-part="hero" data-track="${track}" aria-label="${esc(co.name)}, levels">
        <h2 class="t-course-title">${esc(co.name)}</h2>
        <div class="zt-car" data-car>
          ${levels.map(lv => `<div class="zt-slide" role="group" aria-roledescription="slide" aria-label="Level ${lv.n} of ${levels.length}">
            <span class="t-overline zt-deep">Level ${lv.n}</span><span class="t-label secondary">${esc(lv.name)}</span>
            <span class="zt-slide-art">${ZQArt(art(lv)[0], { label: '' })}</span></div>`).join('')}
        </div>
        ${levels.length > 1 ? `<div class="zt-dots" role="group" aria-label="Choose a level">
          ${levels.map((lv, i) => `<button type="button" data-dot="${i}" aria-label="Level ${lv.n}" aria-pressed="false"><i></i></button>`).join('')}
        </div>` : ''}
      </section>` : '';

    P.resume = co ? `<section class="card zt-resume" data-part="resume" data-track="${track}" aria-label="Next lesson" data-resume></section>` : '';

    const C_ = 2 * Math.PI * 26;
    const examLine = passedAt.length ? `Passed with ${Math.max(...passedAt.map(pctOf))}%. Sit it again any time to check it has stuck.`
      : attempts.length ? `Best so far ${Math.max(...attempts.map(pctOf))}%. Mastery map estimate: ${examPct}%.`
      : `Mastery map estimate: ${examPct}%. Timed, with no hints and no retries.`;
    P.exam = topic ? `<section class="card zt-exam" data-part="exam" data-track="${topic.track || track}" aria-labelledby="zt-exam-h">
        <div class="zt-ring ${ringGrow ? 'grow' : ''}" role="img" aria-label="Readiness ${examPct}%">
          <svg viewBox="0 0 64 64" width="64" height="64" aria-hidden="true"><circle cx="32" cy="32" r="26" class="zt-ring-track"/>
            <circle cx="32" cy="32" r="26" class="zt-ring-fill" ${examPct > 0 ? '' : 'visibility="hidden"'/* at 0% a round cap would draw a dot */} stroke-dasharray="${(C_ * examPct / 100).toFixed(2)} ${C_.toFixed(2)}" transform="rotate(-90 32 32)"/></svg>
          <span class="zt-ring-n tnum" aria-hidden="true">${examPct}%</span>
        </div>
        <div class="zt-exam-t">
          <span class="t-overline muted">${Z.icon('shield', 'xs')} ${passedAt.length ? 'Topic exam passed' : 'Next topic exam'}</span>
          <h2 class="t-h2" id="zt-exam-h">${esc(topic.id)} ${esc(topic.name)} topic exam</h2>
          <span class="t-caption secondary">${examLine}</span>
        </div>
        <button class="btn secondary zt-sit" type="button" data-go="exam/topic-${esc(topic.id)}">${passedAt.length ? 'Sit again' : 'Sit now'}</button>
      </section>` : '';

    root.innerHTML = `<div class="zt"><div class="zt-col zt-left"></div><div class="zt-col zt-right"></div><div hidden data-hold></div></div>`;
    const left = root.querySelector('.zt-left'), right = root.querySelector('.zt-right'), hold = root.querySelector('[data-hold]');
    const parts = {};
    Object.entries(P).forEach(([k, html]) => { if (html) { parts[k] = Z.h(html); hold.append(parts[k]); } });

    /* ---------- Arrange for the current width ---------- */
    const MQ_M = matchMedia('(max-width: 767px)'), MQ_LG = matchMedia('(min-width: 1024px)');
    const mode = () => (MQ_M.matches ? 'm' : MQ_LG.matches ? 'lg' : 'md');
    const ORDER = {
      m: [['top', 'lock', 'hero', 'resume', 'warm', 'due', 'exam', 'search'], []],
      md: [['hello', 'lock', 'search', 'jump', 'streak', 'due', 'warm', 'exam'], []],
      lg: [['hello', 'lock', 'search', 'streak', 'due', 'warm'], ['jump', 'exam']],
    };
    let laid = '', arrangeRaf = 0;
    const arrange = () => {
      if (laid === mode()) return;
      laid = mode();
      const [a, b] = ORDER[laid], used = new Set([...a, ...b]);
      a.forEach(k => parts[k] && left.append(parts[k]));
      b.forEach(k => parts[k] && right.append(parts[k]));
      Object.keys(parts).forEach(k => { if (!used.has(k)) hold.append(parts[k]); });
      root.querySelector('.zt').dataset.mode = laid;
      closeResults();
      /* The hero has just entered the page: show the selected level at once, after layout */
      if (laid === 'm' && car) { cancelAnimationFrame(arrangeRaf); arrangeRaf = requestAnimationFrame(() => centreOn(sel, false)); }
    };
    offs.push(() => cancelAnimationFrame(arrangeRaf));

    /* ---------- Level views: desktop deck and thumbnails, mobile carousel and resume card ---------- */
    let sel = curLevel;
    const deck = parts.jump ? parts.jump.querySelector('[data-deck]') : null;
    const resumeEl = parts.resume || null;
    const launchTo = (x) => `lesson/${cid}/${x.id}`;
    const actionBtn = (info) => {
      if (!info.next || info.next.written !== true) {
        if (info.isCurrent || !curItem) {
          return resource && resource.url
            ? `<a class="btn track block" href="${esc(resource.url)}" target="_blank" rel="noopener">Open the topic resource</a>`
            : `<button class="btn track block" type="button" data-go="course/${esc(cid)}">See the course map</button>`;
        }
        return `<button class="btn track block" type="button" data-go="course/${esc(cid)}">See level ${info.lv.n}</button>`;
      }
      if (info.isCurrent) return `<button class="btn track block" type="button" data-launch="${esc(info.next.id)}">${resume ? 'Continue lesson' : anyDone ? 'Continue course' : 'Start'}</button>`;
      if (Z.prereq && Z.prereq.lessonLocked(cid, info.next.id)) return `<button class="btn track block" type="button" data-go="course/${esc(cid)}">See what is missing for level ${info.lv.n}</button>`;
      return `<button class="btn track block" type="button" data-go="course/${esc(cid)}">${info.done ? 'Continue' : 'Start'} level ${info.lv.n}</button>`;
    };
    const metaLine = (info) => {
      const x = info.next;
      if (!x) return 'Nothing in this level yet';
      if (x.written !== true) return `Lesson ${info.no} · Not yet written`;
      const m = lessonMeta[keyOf(cid, x.id)];
      if (info.isCurrent && resume && resume.lesson === x.id && resume.position) {
        const p = resume.position;
        if (p.phase === 'quiz') return `Lesson ${info.no} · Quiz, question ${(p.q || 0) + 1}${m && m.quiz ? ' of ' + m.quiz : ''}`;
        return `Lesson ${info.no} · Screen ${(p.i || 0) + 1}${m ? ' of ' + m.screens : ''}`;
      }
      return `Lesson ${info.no} · ${m ? `${m.screens} screens · about ${m.minutes} min` : 'about 12 min'}`;
    };
    const lessonRow = (info) => {
      if (!info.next || (info.next.written !== true && (info.isCurrent || !curItem) && resource)) {
        return `<div class="zt-lrow">
          <span class="zt-puck" aria-hidden="true">${Z.icon('book', 'sm')}</span>
          <span class="zt-lrow-t"><span class="t-h2">${esc(resource ? resource.name : 'No lessons written yet')}</span>
            <span class="t-caption muted">${esc(topic ? `${topic.id} ${topic.name}` : '')} · The lessons here are not written yet, so study from this resource</span></span>
        </div>`;
      }
      return `<div class="zt-lrow">
          <span class="zt-puck" aria-hidden="true">${info.no}</span>
          <span class="zt-lrow-t"><span class="t-h2">${esc(info.next.name)}</span>
            <span class="t-caption muted">${esc(metaLine(info))}</span></span>
        </div>`;
    };
    const doneLine = (info) => (info.isCurrent && sum.todayQualified ? `<p class="zt-donetoday t-label">${Z.icon('check', 'xs')}Done for today.</p>` : '');
    const renderDeck = (fade) => {
      if (!deck || !levels.length) return;
      const info = levelInfo(sel), [kind] = art(info.lv);
      deck.innerHTML = `<div class="zt-deck-in ${fade ? 'zt-fade' : ''}">
          <div class="zt-deck-head"><h3 class="t-h1">${esc(co.name)}</h3>
            <span class="t-overline zt-deep">Level ${info.lv.n}</span>
            <span class="t-caption secondary">${esc(info.lv.name)} · ${info.done} of ${info.total} done</span></div>
          <div class="zt-deck-art">${ZQArt(kind, { label: '' })}</div>
          ${doneLine(info)}${lessonRow(info)}${actionBtn(info)}</div>`;
    };
    const renderResume = () => {
      if (!resumeEl || !levels.length) return;
      const info = levelInfo(sel);
      resumeEl.innerHTML = `${doneLine(info)}${lessonRow(info)}${actionBtn(info)}`;
    };
    const thumbs = parts.jump ? Array.from(parts.jump.querySelectorAll('[data-level]')) : [];
    const dots = parts.hero ? Array.from(parts.hero.querySelectorAll('[data-dot]')) : [];
    const car = parts.hero ? parts.hero.querySelector('[data-car]') : null;
    /* Scrolls the code starts itself (a dot tap, entering the page) set `target`. Scroll positions are ignored
       until the carousel reaches that slide, so the resume card and dots never flash through the levels it passes. */
    let target = null;
    const slideLeft = (i) => { const s = car.children[i]; return s.offsetLeft - (car.clientWidth - s.offsetWidth) / 2; };
    const nearest = () => {
      const mid = car.scrollLeft + car.clientWidth / 2;
      let best = 0, bd = Infinity;
      Array.from(car.children).forEach((s, j) => { const d = Math.abs(s.offsetLeft + s.offsetWidth / 2 - mid); if (d < bd) { bd = d; best = j; } });
      return best;
    };
    const centreOn = (i, smooth) => {
      if (!car || !car.isConnected || !car.clientWidth || !car.children[i]) return;
      const l = Math.max(0, Math.min(car.scrollWidth - car.clientWidth, slideLeft(i)));
      if (Math.abs(car.scrollLeft - l) < 1) { target = null; return; }
      target = i;
      car.scrollTo({ left: l, behavior: smooth && !Z.reducedMotion() ? 'smooth' : 'auto' });
    };
    const setLevel = (i, { fade = false, scroll = false } = {}) => {
      const changed = i !== sel; sel = i;
      thumbs.forEach((t, j) => t.setAttribute('aria-pressed', String(j === sel)));
      dots.forEach((d, j) => d.setAttribute('aria-pressed', String(j === sel)));
      renderDeck(fade && changed); renderResume();
      if (scroll) centreOn(i, true);
    };
    thumbs.forEach((t, i) => t.addEventListener('click', () => setLevel(i, { fade: true })));
    dots.forEach((d, i) => d.addEventListener('click', () => setLevel(i, { scroll: true })));
    let scrollRaf = 0;
    if (car) {
      car.addEventListener('scroll', () => {
        cancelAnimationFrame(scrollRaf);
        scrollRaf = requestAnimationFrame(() => {
          const best = nearest();
          if (target !== null) { if (best === target) target = null; return; }
          if (best !== sel) setLevel(best);
        });
      }, { passive: true });
      /* An interrupted programmatic scroll cannot leave the guard set; settle on wherever the carousel stopped */
      car.addEventListener('scrollend', () => { target = null; const best = nearest(); if (best !== sel) setLevel(best); });
    }
    offs.push(() => cancelAnimationFrame(scrollRaf));

    /* Screens and minutes come from the lesson file: fetch the ones on show, then redraw the rows */
    const wantMeta = () => {
      const ids = new Set(levels.map((_, i) => levelInfo(i).next).filter(x => x && x.written === true).map(x => x.id));
      ids.forEach(id => {
        const k = keyOf(cid, id);
        if (lessonMeta[k]) return;
        C.lesson(cid, id).then(L => {
          if (!L) return;
          lessonMeta[k] = { screens: (L.screens || []).length + (L.summary ? 1 : 0), minutes: L.minutes || 12, quiz: (L.quiz || []).length };
          if (alive) { renderDeck(false); renderResume(); }
        }).catch(() => { /* the row keeps its estimate */ });
      });
    };

    /* ---------- Search: courses, topics, lessons and the learner's notebook cards ---------- */
    const sWrap = parts.search, q = sWrap.querySelector('#zt-q'), listEl = sWrap.querySelector('#zt-results');
    const index = [];
    C.stages().forEach(s => s.topics.forEach(t => {
      index.push({ kind: 'Topic', icon: 'grid', title: `${t.id} ${t.name}`, name: t.name, sub: `Stage ${s.id} · ${s.name}`, go: 'learn', own: !!co && (t.courses || []).includes(co.id) });
      (t.courses || []).forEach(id => {
        const c = C.course(id); if (!c) return;
        index.push({ kind: 'Course', icon: 'book', title: c.name, sub: `${t.id} ${t.name}`, go: `course/${id}`, own: id === cid });
        /* A lesson is found by its own name, not by its course's name, or "conditional" would list every lesson */
        C.courseLessons(id).filter(x => x.kind === 'lesson').forEach(x => index.push({
          kind: 'Lesson', icon: 'play', title: x.name, sub: `${c.name} · Level ${x.level}${x.written === true ? '' : ' · Not yet written'}`, subHidden: true,
          go: x.written === true ? `lesson/${id}/${x.id}` : `course/${id}`, launch: x.written === true ? { course: id, id: x.id } : null, own: id === cid,
        }));
      });
    }));
    C.prepPaths().forEach(p => index.push({ kind: 'Prepare', icon: 'target', title: p.name, sub: p.kind === 'firm' ? 'Prepare for · firm' : p.kind === 'stage' ? `Prepare for · ${C.prepStageLabel(p.stage)}, ${p.track}` : 'Prepare for · general', go: `prepare/${p.id}`, own: false }));
    S.notebook.list().forEach(n => {
      const c = C.course(n.course) || {};
      index.push({ kind: 'Formula', icon: 'sparkle', title: n.name || 'Formula', f: n, sub: c.name || '', own: n.course === cid });
    });
    index.forEach((e, i) => {
      const hay = norm([e.title, e.subHidden ? '' : e.sub, e.kind, e.f ? e.f.note || '' : ''].join(' ')).replace(/\s+/g, ' ');
      e.i = i; e.t = norm(e.name || e.title);
      e.hay = ' ' + hay;
      e.toks = hay.split(/[^a-z0-9]+/).filter(Boolean);
    });
    /* Words match at word starts only: "put" finds put-call parity, not computer. "1.5" still finds the topic. */
    const hasWord = (e, w) => e.toks.some(t => t.startsWith(w)) || e.hay.includes(' ' + w);
    const kindRank = { Formula: 0, Lesson: 0.2, Course: 0.4, Prepare: 0.5, Topic: 0.6 };
    const rank = (e, v) => (e.t.startsWith(v) ? 0 : (' ' + e.t).includes(' ' + v) ? 1 : 2) + (e.own ? 0 : 1.5) + kindRank[e.kind];
    let hits = [], active = -1;
    function closeResults() { listEl.hidden = true; q.setAttribute('aria-expanded', 'false'); q.removeAttribute('aria-activedescendant'); active = -1; hits = []; }
    const search = () => {
      const v = norm(q.value.trim()).replace(/\s+/g, ' ');
      if (!v) { closeResults(); return; }
      const words = v.split(' ');
      hits = index.filter(e => words.every(w => hasWord(e, w)))
        .map(e => ({ e, r: rank(e, v) }))
        .sort((a, b) => a.r - b.r || a.e.i - b.e.i).slice(0, 7).map(x => x.e);
      active = -1;
      listEl.classList.toggle('up', mode() === 'm');
      listEl.innerHTML = hits.length ? hits.map((e, i) => `<li role="option" id="zt-opt-${i}" aria-selected="false" data-i="${i}">
          <span class="zt-ico">${Z.icon(e.icon, 'sm')}</span>
          <span class="zt-opt-t"><span class="t-label">${esc(e.title)}</span>
            ${e.f && e.f.tex ? `<span class="zt-opt-tex">${Z.tex(String(e.f.tex).replace(/\\dfrac/g, '\\tfrac'))}</span>` : `<span class="t-caption muted">${esc(e.sub)}</span>`}</span>
          <span class="t-caption muted zt-kind">${e.kind}</span></li>`).join('')
        : `<li class="zt-none t-body secondary" role="presentation">Nothing matches. Try a course or a lesson, such as Bayes or integrals.</li>`;
      listEl.hidden = false; q.setAttribute('aria-expanded', 'true');
    };
    const highlight = (i) => {
      active = i;
      Array.from(listEl.querySelectorAll('[role="option"]')).forEach((o, j) => o.setAttribute('aria-selected', String(j === i)));
      if (i >= 0) { q.setAttribute('aria-activedescendant', 'zt-opt-' + i); listEl.querySelector('#zt-opt-' + i).scrollIntoView({ block: 'nearest' }); }
      else q.removeAttribute('aria-activedescendant');
    };
    const launch = (course, id) => {
      const r = S.lessons[keyOf(course, id)];
      window.ZQLaunch = { course, id, kind: 'lesson', wasDone: !!(r && r.done), qualifiedBefore: !!S.summary().todayQualified, at: Date.now() };
      Z.go(`lesson/${course}/${id}`);
    };
    const choose = (e) => {
      closeResults();
      if (!e.f) { if (e.launch) launch(e.launch.course, e.launch.id); else Z.go(e.go); return; }
      const f = e.f, c = C.course(f.course);
      const lx = c && f.lesson ? C.courseLessons(f.course).find(x => x.id === f.lesson) : null;
      const where = c ? `From ${esc(c.name)}${lx ? `, ${esc(lx.name)}` : ''}.` : '';
      const go = lx && lx.written === true ? 'lesson' : c ? 'course' : '';
      const close = Z.sheet(`<div class="zt-fsheet">
          <span class="t-overline muted">Notebook</span>
          <h2 class="t-sheet-title">${esc(f.name || 'Formula')}</h2>
          ${f.tex ? `<div class="zt-fsheet-tex">${Z.tex(f.tex, true)}</div>` : ''}
          ${f.note ? `<p class="t-body">${Z.md(esc(f.note))}</p>` : ''}
          ${where ? `<p class="t-caption secondary">${where}</p>` : ''}
          ${go ? `<button class="btn block" type="button" data-fgo="${go}">${go === 'lesson' ? 'Open the lesson' : 'Open the course map'}</button>` : ''}
        </div>`, { label: f.name || 'Formula' });
      document.querySelector('[data-fgo]')?.addEventListener('click', (ev) => {
        const to = ev.currentTarget.dataset.fgo; close();
        if (to === 'lesson') launch(f.course, f.lesson); else Z.go(`course/${f.course}`);
      });
    };
    listen(q, 'input', search);
    listen(q, 'focus', () => {
      if (mode() === 'm') sWrap.scrollIntoView({ block: 'center', behavior: Z.reducedMotion() ? 'auto' : 'smooth' }); // clear of the tab bar, room above for results
      if (q.value.trim()) search();
    });
    listen(q, 'keydown', (e) => {
      if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
        if (listEl.hidden) { if (!q.value.trim()) return; search(); }
        const n = hits.length;
        if (!n) return;
        e.preventDefault();
        highlight(e.key === 'ArrowDown' ? (active + 1) % n : active <= 0 ? n - 1 : active - 1);
      }
      else if (e.key === 'Enter' && !listEl.hidden && hits.length) { e.preventDefault(); choose(hits[active < 0 ? 0 : active]); }
      else if (e.key === 'Escape') { if (!listEl.hidden) { e.stopPropagation(); closeResults(); } else q.value = ''; }
    });
    listen(listEl, 'pointerdown', (e) => e.preventDefault()); // keep focus in the input
    listen(listEl, 'click', (e) => { const o = e.target.closest('[data-i]'); if (o) choose(hits[+o.dataset.i]); });
    listen(listEl, 'pointermove', (e) => { const o = e.target.closest('[data-i]'); if (o && +o.dataset.i !== active) highlight(+o.dataset.i); });
    listen(document, 'pointerdown', (e) => { if (!sWrap.contains(e.target)) closeResults(); });

    /* ---------- Wiring ---------- */
    listen(root, 'click', (e) => {
      if (e.target.closest('[data-streak]')) { Z.streakSheet(); return; }
      const l = e.target.closest('[data-launch]');
      if (l) { launch(cid, l.dataset.launch); return; }
      const g = e.target.closest('[data-go]');
      if (g) Z.go(g.dataset.go);
    });
    sparkline(parts.warm.querySelector('[data-spark]'), trend);
    listen(MQ_M, 'change', arrange); listen(MQ_LG, 'change', arrange);
    arrange();
    setLevel(sel);
    wantMeta();
    if (restore) {
      window.scrollTo(0, restore.y);
      if (restore.q) { q.value = restore.q; }
      if (restore.focus) { q.focus({ preventScroll: true }); if (restore.q) search(); }
    }

    return () => offs.forEach(f => f());
  }
  const numWord = (n) => ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten'][n] || String(n);
  const cap = (s) => s.charAt(0).toUpperCase() + s.slice(1);

  /* =====================================================================================
     MENTAL ARITHMETIC WARM-UP
     Settings from content/warmup.json (Zetamac defaults): addition 2 to 100 + 2 to 100; subtraction is addition in
     reverse; multiplication 2 to 12 by 2 to 100; division is multiplication in reverse. 120 seconds.
     A finished full round is saved with ZQ.state.warmup.record(score, seconds), which also logs its minutes to 'mental'.
     ===================================================================================== */
  /* The generator is shared with the mock exams' generated items (js/engine/arith.js) */
  const makeProblem = (prev) => ZQ.arith.problem(WARM.operations, Math.random, prev);
  const clock = (s) => `${Math.floor(s / 60)}:${String(s % 60).padStart(2, '0')}`;

  /* Column chart: the last 10 rounds in a lighter step, this round in the track colour,
     the Stage 3 mark as a dashed target line (spec 2.6: targets 1.5px dashed ink).
     Both text labels keep clear of the line and of the columns, and carry a surface halo as a last resort. */
  const columns = (wrap, values, curLabel) => {
    const n = values.length, TARGET = (WARM.targets && WARM.targets.stage3) || 50;
    const draw = () => {
      const W = Math.max(240, Math.floor(wrap.clientWidth)), H = 200, PL = 30, PR = 4, PT = 22, PB = 26;
      const iw = W - PL - PR, ih = H - PT - PB;
      const top = Math.max(60, Math.ceil((Math.max(...values) + 8) / 10) * 10);
      const y = (v) => PT + ih - v / top * ih;
      const band = iw / n, bw = Math.min(24, band * 0.62);
      const bx = (i) => PL + band * i + (band - bw) / 2;
      const ticks = []; for (let t = 0; t <= top; t += 25) ticks.push(t);
      const bar = (i) => {
        const v = values[i], h = Math.max(0, y(0) - y(v)), r = Math.min(4, h, bw / 2), x0 = bx(i), x1 = x0 + bw, yt = y(v), yb = y(0);
        if (h <= 0) return `<path class="zw-col ${i === n - 1 ? 'now' : ''}" d="M${x0},${yb - 1}H${x1}V${yb}H${x0}Z"/>`;
        return `<path class="zw-col ${i === n - 1 ? 'now' : ''}" d="M${x0},${yb}V${yt + r}Q${x0},${yt} ${x0 + r},${yt}H${x1 - r}Q${x1},${yt} ${x1},${yt + r}V${yb}Z"/>`;
      };
      const last = n - 1, cx = bx(last) + bw / 2, tY = y(TARGET), vTop = y(values[last]);
      /* This round's value sits 6px above its column. Its digits are about 10px tall, centred 5px above the baseline:
         if that centre comes within 12px of the target line, lift the label clear of both the line and the column. */
      const vY = Math.abs(vTop - 6 - 5 - tY) < 12 ? Math.min(vTop, tY) - 7 : vTop - 6;
      wrap.querySelector('svg')?.remove();
      wrap.insertAdjacentHTML('afterbegin', `<svg width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" tabindex="0" role="img"
          aria-label="${n > 1 ? `Scores for your last ${n - 1} rounds, oldest first: ${values.slice(0, -1).join(', ')}. ` : ''}${curLabel}: ${values[last]}. Use the arrow keys to read each one.">
          <rect class="zw-hot" x="0" y="${PT}" width="${band}" height="${ih}" visibility="hidden"/>
          ${ticks.filter(t => t !== TARGET).map(t => `<line class="zw-grid" x1="${PL}" x2="${W - PR}" y1="${y(t)}" y2="${y(t)}"/>`).join('')}
          ${ticks.map(t => `<text class="zw-tick" x="${PL - 8}" y="${y(t) + 4}" text-anchor="end">${t}</text>`).join('')}
          ${values.map((_, i) => bar(i)).join('')}
          <line class="zw-target" x1="${PL}" x2="${W - PR}" y1="${tY}" y2="${tY}"/>
          <text class="zw-tlabel" x="${PL + 6}" y="${tY - 6}">Stage 3 mark</text>
          <text class="zw-vlabel" x="${cx}" y="${vY}" text-anchor="middle">${values[last]}</text>
          ${n > 1 ? `<text class="zw-xlabel" x="${bx(0)}" y="${H - 6}">Oldest</text>` : ''}
          <text class="zw-xlabel strong" x="${Math.min(cx, W - PR - 14)}" y="${H - 6}" text-anchor="middle">${curLabel}</text>
        </svg>`);
      const svg = wrap.querySelector('svg'), tip = wrap.querySelector('.zw-tip'), hot = svg.querySelector('.zw-hot');
      /* Place "Stage 3 mark" over the first run of columns that all stay below the line, never over this round */
      const tl = svg.querySelector('.zw-tlabel');
      let lw = 84; try { lw = tl.getComputedTextLength() || lw; } catch { /* not laid out: keep the estimate */ }
      const clearAt = (x0) => values.every((v, j) => { const a = bx(j) - 3, b = bx(j) + bw + 3; return b < x0 || a > x0 + lw || (j !== last && v < TARGET); });
      const starts = [PL + 6, ...values.map((_, j) => bx(j) + bw + 4)].filter(x => x + lw <= cx - 14);
      const spot = starts.find(clearAt);
      if (spot !== undefined) tl.setAttribute('x', spot.toFixed(1));
      hoverable(svg, n, (px, w) => Math.max(0, Math.min(n - 1, Math.floor((px * W / w - PL) / band))), (i) => {
        hot.setAttribute('x', PL + band * i); hot.setAttribute('visibility', 'visible');
        const back = last - i;
        showTip(wrap, tip, bx(i) + bw / 2, y(values[i]), String(values[i]), back === 0 ? curLabel : plural(back, 'round', 'rounds') + ' ago');
      }, () => { hot.setAttribute('visibility', 'hidden'); tip.hidden = true; });
    };
    draw();
    let w0 = wrap.clientWidth;
    const ro = new ResizeObserver(() => { if (Math.abs(wrap.clientWidth - w0) > 2) { w0 = wrap.clientWidth; draw(); } });
    ro.observe(wrap);
    return () => ro.disconnect();
  };

  /* Layout follows the lesson player (spec 2.11): a 64px top bar; from 768px a frame of the viewport minus 32px,
     radius 24, 2px border, with the 366px button group bottom-centre; under 768px no frame and a 286px button
     right-aligned with a 16px margin. The clock is a timer pill, as in the topic exam, not a progress bar. */
  ZQ.screen({
    id: 'warmup', title: 'Mental arithmetic warm-up', group: 'Practice', shell: false,
    render(root, Z) {
      const S = Z.state;
      const offs = [];
      const listen = (target, ev, fn, opt) => { target.addEventListener(ev, fn, opt); offs.push(() => target.removeEventListener(ev, fn, opt)); };
      const FULL = () => WARM.seconds || 120, DEMO = () => WARM.demoSeconds || 10, KEEP = () => WARM.trendLength || 10;
      const STAGE3 = () => (WARM.targets && WARM.targets.stage3) || 50, STAGE0 = () => (WARM.targets && WARM.targets.stage0) || 25;
      const scores = () => S.warmup.list().map(e => e.score);
      let state = 'ready', raf = 0, countRaf = 0, endAt = 0, remaining = 0, total = FULL(), demo = false, score = 0, prob = null, lastShown = -1, flashT = 0, gone = false;

      root.innerHTML = `<div class="zw" data-track="speed">
          <header class="zw-top">
            <button class="icon-btn zw-x" type="button" aria-label="Quit the warm-up">${Z.icon('close')}</button>
            <p class="zw-ttl t-label">Mental arithmetic warm-up</p>
            <span class="zw-timer" role="timer"><span class="sr-only">Time left </span>${Z.icon('timer', 'sm')}<span data-time>${clock(FULL())}</span></span>
          </header>
          <div class="zw-frame">
            <main class="zw-scroll" id="zw-main"><div class="zw-col" data-col></div></main>
            <footer class="zw-foot" data-foot hidden></footer>
          </div>
        </div>`;
      const col = root.querySelector('[data-col]'), scroller = root.querySelector('.zw-scroll'), foot = root.querySelector('[data-foot]');
      const timerEl = root.querySelector('.zw-timer'), timeEl = root.querySelector('[data-time]');
      const setFoot = (html) => { foot.innerHTML = html; foot.hidden = !html; };

      /* The pill turns amber for the last 10 seconds of a full round */
      const setClock = (ms) => {
        const s = Math.max(0, Math.ceil(ms / 1000));
        timerEl.classList.toggle('is-low', state === 'run' && total > 10 && s <= 10);
        if (s !== lastShown) { lastShown = s; timeEl.textContent = clock(s); }
      };
      const resetClock = (secs) => { total = secs; lastShown = -1; setClock(secs * 1000); };

      /* Count-up from the first frame's own timestamp, so the first frame always reads 0 */
      const countTo = (el, to, ms) => {
        cancelAnimationFrame(countRaf);
        if (Z.reducedMotion()) { el.textContent = String(to); return; }
        let t0 = null;
        const step = (now) => {
          if (t0 === null) t0 = now;
          const p = Math.max(0, Math.min(1, (now - t0) / ms));
          const e = p < 0.8 ? p / 0.8 * 0.9 : 0.9 + (1 - Math.pow(1 - (p - 0.8) / 0.2, 3)) * 0.1; // as core.js countUp
          el.textContent = String(Math.round(to * e));
          if (p < 1) countRaf = requestAnimationFrame(step);
        };
        countRaf = requestAnimationFrame(step);
      };

      /* ---------- Ready ---------- */
      const ex = () => {
        const ops = WARM.operations, by = (id) => ops.find(o => o.id === id) || {};
        const add = by('add'), mul = by('mul');
        return [
          ['47 + 38', `Addition, ${add.a ? `${add.a[0]} to ${add.a[1]}` : '2 to 100'} each side`],
          ['85 - 47', 'Subtraction, addition in reverse'],
          ['7 \\times 64', `Multiplication, ${mul.a ? `${mul.a[0]} to ${mul.a[1]} by ${mul.b[0]} to ${mul.b[1]}` : '2 to 12 by 2 to 100'}`],
          ['448 \\div 7', 'Division, multiplication in reverse'],
        ];
      };
      const ready = () => {
        state = 'ready'; resetClock(FULL());
        const t = scores().slice(-KEEP());
        const lastLine = t.length
          ? `Last score ${t[t.length - 1]}. Best of your last ${t.length}: ${Math.max(...t)}. Stage 3 asks for ${STAGE3()}.`
          : `Your first round sets the score to beat. Stage 0 asks for ${STAGE0()} and Stage 3 for ${STAGE3()}.`;
        col.innerHTML = `<div class="zw-ready enter">
            <div class="zw-art">${ZQArt('timer', { label: 'A stopwatch' })}</div>
            <div class="zw-copy">
              <span class="t-overline zt-deep">Daily warm-up</span>
              <h1 class="t-lesson-title">Mental arithmetic</h1>
              <p class="t-prose">You have ${FULL()} seconds. Type each answer. It moves on by itself when it is right, so there is no Enter.</p>
            </div>
            <ul class="zw-kinds">${ex().map(([tx, line]) => `<li><span class="zw-ex">${Z.tex(tx)}</span><span class="t-body">${Z.esc(line)}</span></li>`).join('')}</ul>
            <p class="t-caption secondary zw-last">${lastLine}</p>
          </div>`;
        setFoot(`<button class="link-btn zw-demo" type="button" data-demo>Quick demo (${DEMO()} s)</button>
            <div class="zw-actions"><button class="btn zw-primary" type="button" data-start>Start</button></div>`);
        scroller.scrollTop = 0;
        foot.querySelector('[data-start]').addEventListener('click', () => start(FULL(), false));
        foot.querySelector('[data-demo]').addEventListener('click', () => start(DEMO(), true));
        foot.querySelector('[data-start]').focus({ preventScroll: true });
      };

      /* ---------- Drill ---------- */
      let input, probEl, scoreEl, field;
      const next = () => { prob = makeProblem(prob); probEl.innerHTML = Z.tex(prob.tex); input.value = ''; };
      const tick = () => {
        if (state !== 'run') return;
        const left = endAt - Date.now();
        setClock(left);
        if (left <= 0) { finish(); return; }
        raf = requestAnimationFrame(tick);
      };
      const start = (secs, isDemo) => {
        demo = isDemo; score = 0; prob = null; state = 'starting'; resetClock(secs);
        col.innerHTML = `<div class="zw-drill">
            <div class="zw-score"><span class="t-overline muted">Score</span><span class="zw-score-n" data-score>0</span></div>
            <div class="zw-prob" data-prob aria-live="polite"></div>
            <label class="field zw-field"><span class="sr-only">Answer</span>
              <input type="text" inputmode="numeric" pattern="[0-9]*" autocomplete="off" autocorrect="off" spellcheck="false" enterkeyhint="next" data-answer></label>
            <p class="t-caption muted">${demo ? `Demo round, ${secs} seconds. It is not saved.` : 'Right answers move on by themselves.'}</p>
          </div>`;
        setFoot('');
        scroller.scrollTop = 0;
        input = col.querySelector('[data-answer]'); probEl = col.querySelector('[data-prob]'); scoreEl = col.querySelector('[data-score]'); field = col.querySelector('.zw-field');
        input.addEventListener('input', onInput);
        input.addEventListener('keydown', (e) => { if (e.key === 'Enter') e.preventDefault(); });
        next();
        state = 'run'; endAt = Date.now() + secs * 1000;
        input.focus({ preventScroll: true });
        raf = requestAnimationFrame(tick);
      };
      const onInput = () => {
        if (state !== 'run') return;
        const v = input.value.replace(/\D/g, '');
        if (v !== input.value) input.value = v;
        if (v === '' || Number(v) !== prob.ans) return;
        score += 1; scoreEl.textContent = String(score);
        scoreEl.classList.remove('bump'); void scoreEl.offsetWidth; scoreEl.classList.add('bump');
        field.classList.add('correct'); clearTimeout(flashT); flashT = setTimeout(() => field && field.classList.remove('correct'), 180);
        Z.sound('tap');
        next();
      };

      /* ---------- Pause and quit ---------- */
      const pause = () => { if (state !== 'run') return; state = 'paused'; remaining = endAt - Date.now(); cancelAnimationFrame(raf); };
      const resume = () => { if (state !== 'paused') return; state = 'run'; endAt = Date.now() + remaining; raf = requestAnimationFrame(tick); input && input.focus({ preventScroll: true }); };
      const quit = () => {
        if (state !== 'run') { Z.go('today'); return; }
        pause();
        let stopping = false;
        const close = Z.sheet(`<div class="zw-quit">
            <h2 class="t-sheet-title">Stop this round?</h2>
            <p class="t-body secondary">The clock is paused. A stopped round is not saved.</p>
            <div class="zw-quit-btns"><button class="btn secondary" type="button" data-stop>Stop</button><button class="btn" type="button" data-keep autofocus>Keep going</button></div>
          </div>`, { label: 'Stop this round?', onClose: () => { if (!stopping && !gone) resume(); } });
        const box = document.querySelector('.zw-quit');
        box.querySelector('[data-keep]').addEventListener('click', () => close());
        box.querySelector('[data-stop]').addEventListener('click', () => { stopping = true; close(); Z.go('today'); });
      };
      listen(root.querySelector('.zw-x'), 'click', quit);
      listen(document, 'keydown', (e) => { if (e.key === 'Escape' && state === 'run') { e.preventDefault(); quit(); } });

      /* ---------- End ---------- */
      let stopChart = null;
      const finish = () => {
        state = 'end'; cancelAnimationFrame(raf); setClock(0);
        const past = scores().slice(-KEEP());
        const last = past.length ? past[past.length - 1] : null, best = past.length ? Math.max(...past) : null;
        const avg = past.length ? past.reduce((s, v) => s + v, 0) / past.length : 0;
        const isBest = !demo && best != null && score > best;
        const delta = demo
          ? `That was the ${total}-second demo, so it is not saved. A full round runs for ${FULL()} seconds.`
          : last == null ? 'Your first round. This is the score to beat.'
          : score > last ? `${plural(score - last, 'more answer', 'more answers')} than your last round.`
          : score === last ? 'Level with your last round.'
          : `${plural(last - score, 'fewer answer', 'fewer answers')} than your last round. Single rounds move around; the trend is what counts.`;
        const label = demo ? 'Demo' : 'Now';
        const head = past.length ? `This round against your last ${past.length === 1 ? 'one' : past.length}` : 'Your first round';
        const note = past.length
          ? `Last ${plural(past.length, 'round', 'rounds')}: average ${avg.toFixed(1)}, best ${best}. The dashed line is the Stage 3 mark of ${STAGE3()}.`
          : `The dashed line is the Stage 3 mark of ${STAGE3()}. Stage 0 asks for ${STAGE0()}.`;
        col.innerHTML = `<div class="zw-end">
            <h1 class="t-complete enter">Round complete</h1>
            <span class="t-overline muted enter">Score</span>
            <span class="zw-big tnum enter" data-big>0</span>
            <p class="t-body secondary zw-delta enter">${delta}</p>
            ${isBest ? `<span class="chip track zw-best">${Z.icon('star', 'xs')}Best of your last ${past.length} rounds</span>` : ''}
            <section class="card zw-chartcard enter" aria-labelledby="zw-chart-h">
              <h2 class="t-h2" id="zw-chart-h">${head}</h2>
              <div class="zw-chart" data-chart><div class="zw-tip zt-tip" hidden></div></div>
              <p class="t-caption secondary">${note}</p>
              <table class="sr-only"><caption>Scores, oldest first</caption><thead><tr><th>Round</th><th>Score</th></tr></thead><tbody>
                ${past.map((v, i) => `<tr><td>${plural(past.length - i, 'round', 'rounds')} ago</td><td>${v}</td></tr>`).join('')}<tr><td>${label}</td><td>${score}</td></tr></tbody></table>
            </section>
          </div>`;
        setFoot(`<div class="zw-actions">
            <button class="btn secondary zw-sec" type="button" data-again>${demo ? 'Full round' : 'Go again'}</button>
            <button class="btn zw-primary" type="button" data-done>Done</button></div>`);
        scroller.scrollTop = 0;
        stopChart = columns(col.querySelector('[data-chart]'), [...past, score], label);
        foot.querySelector('[data-done]').addEventListener('click', () => Z.go('today'));
        foot.querySelector('[data-again]').addEventListener('click', () => { stopChart && stopChart(); stopChart = null; cancelAnimationFrame(countRaf); start(FULL(), false); });
        foot.querySelector('[data-done]').focus({ preventScroll: true });
        countTo(col.querySelector('[data-big]'), score, 700);
        Z.sound('complete');
        if (!demo) S.warmup.record(score, total); // logs the round's minutes to the 'mental' block too
      };

      warmReady.then(() => { if (!gone && state === 'ready') ready(); });
      ready();
      return () => {
        gone = true; state = 'gone'; cancelAnimationFrame(raf); cancelAnimationFrame(countRaf); clearTimeout(flashT);
        stopChart && stopChart(); offs.forEach(f => f());
      };
    },
  });
})();
