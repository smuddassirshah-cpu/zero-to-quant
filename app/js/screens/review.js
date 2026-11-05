/* Review hub and the sets it opens (docs/PLAN.md 7 set mode and 10; design-research 5.7, 5.9, 6.2, 8.2, 8.4).
   Routes:
     #review                         the hub: Redo queue, Homework, Exams (left); Practice, Notebook (right)
     #review/<course>/<reviewId>     a level review, run through ZQ.player.runSet, recorded with reviewFinished
     #homework/<course>/<hwId>       a homework set: items rendered by ZQ.player.renderItem in exam mode (nothing marked
                                     until you submit), the long-form item self-marked against its rubric, homeworkSubmitted
     #practice  and  #practice/weekly   a practice set of 8 from ZQ.select.practiceSet, or the week's 3 probability problems;
                                     each answer goes to ZQ.state.practiceResult (skill scores and the streak count only)
     #redo                           every due redo item, oldest first, each result recorded with ZQ.state.redo.result
     #bank                           the Interview practice deck: due and new items from content/bank/*.json and tagged items of
                                     finished lessons (ZQ.select.bankDeck), each scheduled on its own, recorded with ZQ.state.bankResult
                                     (ENGINE-BACKLOG 456). Every set page ends with a pace line (average, slowest families, items over
                                     their `pace`) from the seconds each item took (ENGINE-BACKLOG 457); grading never reads time.
   A set with timed: { seconds, lockAtZero } (a level review's file, or #practice/timed/<seconds>) shows a countdown and a
   live score; at zero a locking set ends by itself and records what was answered (ENGINE-BACKLOG 454, covers 129).
   Each page installs window.ZQ.test (current, answerCorrect, check, continue) for tools/playthrough.mjs; a timed set also
   installs window.ZQSet = { setRemaining(s), remaining(), timed } so a tool can move the clock without waiting.
   Learner state is read through ZQ.state and changed only through its mutators. Every selector carries the rv- (hub),
   rvs- (set pages) or hw- (homework) prefix. */
(function () {
  'use strict';

  const LONG_PASS = 7;                        // the longform widget counts 7 of 10 or more as right
  const PRACTICE_N = 8;
  const DAY = 86400000;
  const clock = (s) => { s = Math.max(0, Math.ceil(s)); const h = Math.floor(s / 3600), m = Math.floor((s % 3600) / 60); return h ? `${h}:${String(m).padStart(2, '0')}:${String(s % 60).padStart(2, '0')}` : `${m}:${String(s % 60).padStart(2, '0')}`; };
  const MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  const DAYS = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];

  /* Homework drafts that live while the app is open (also kept in localStorage per set, for a reload) */
  const session = { hw: {} };

  /* ---------- Helpers ---------- */
  const S = () => ZQ.state;
  const C = () => ZQ.content;
  const G = () => ZQ.grade;
  const plural = (n, one, many) => `${n} ${n === 1 ? one : many}`;
  const listAnd = (a) => (a.length < 2 ? a.join('') : a.slice(0, -1).join(', ') + ' and ' + a[a.length - 1]);
  const pips = (d) => `<span class="rv-pips" role="img" aria-label="Difficulty ${d} of 5">${[1, 2, 3, 4, 5].map(i => `<i class="${i <= d ? 'on' : ''}"></i>`).join('')}</span>`;
  const dayDate = (t) => { const d = new Date(t); return `${DAYS[d.getDay()]} ${d.getDate()} ${MONTHS[d.getMonth()]}`; };
  const dayKey = (t) => { const d = new Date(t); return `${d.getFullYear()}-${d.getMonth()}-${d.getDate()}`; };
  const daysFrom = (t) => { const a = new Date(); a.setHours(0, 0, 0, 0); const b = new Date(t); b.setHours(0, 0, 0, 0); return Math.round((b - a) / DAY); };
  const whenDue = (t) => { const n = daysFrom(t); return n <= 0 ? (n === 0 ? 'Due today' : `Due since ${dayDate(t)}`) : n === 1 ? 'Due tomorrow' : `Due ${dayDate(t)}`; };
  const course = (cid) => { try { return C().course(cid); } catch { return null; } };
  const courseName = (cid) => (course(cid) || {}).name || cid;
  const trackOf = (cid) => (course(cid) || {}).track || 'prob';
  const artOf = (cid) => (course(cid) || {}).art || 'tree';
  const levelOf = (cid, n) => ((course(cid) || {}).levels || []).find(l => l.n === +n) || null;
  const levelOfId = (cid, id) => ((course(cid) || {}).levels || []).find(l => l.review === id || l.homework === id || (l.lessons || []).includes(id)) || null;
  const lessonDone = (cid, lid) => { const r = S().lesson(cid, lid); return !!(r && r.done); };
  const art = (kind) => (window.ZQArt ? window.ZQArt(kind) : '');
  const empty = (v) => v == null || v === '' || (Array.isArray(v) && !v.length) || (typeof v === 'object' && !Array.isArray(v) && Object.values(v).every(empty));
  const skillNames = () => {
    const out = {};
    try { C().courses().forEach(c => Object.assign(out, c.skills || {})); } catch { /* content not ready */ }
    return out;
  };
  const md = (s) => G().inline(s || '');
  const stemOf = (it) => (it ? (it.question || it.prose || it.prompt || it.title || (Array.isArray(it.parts) && it.parts[0] && it.parts[0].question) || '') : '');
  const store = {
    get: (k, d) => { try { return ZQ.store.get(k, d); } catch { return d; } },
    set: (k, v) => { try { ZQ.store.set(k, v); } catch { /* storage blocked */ } },
  };
  const logReview = (seconds, source) => { const m = seconds / 60; if (m >= 0.1) { try { S().hours.log({ block: 'review', minutes: m, source }); } catch (e) { console.error(e); } } };
  const resultRow = (r) => ({ id: r.item.id, ok: !!r.ok, difficulty: r.item.difficulty || 2, skills: r.item.skills || [], ref: r.item.ref, seconds: r.seconds, pace: r.item.pace, family: (ZQ.mock.family(r.item) || {}).id, how: S().provenance(r.item), ...(r.item.performance ? { perf: r.item.performance } : {}) });
  /* The rows ZQ.mock.pacing reads: one per answered item, numbered as the summary lists them */
  const paceRows = (items, res) => items.map((it, j) => { const r = res[j], f = ZQ.mock.family(it, skillNames()); return r && typeof r.seconds === 'number' ? { label: String(j + 1), seconds: r.seconds, pace: it.pace, family: f && f.id, familyLabel: f && f.label } : null; }).filter(Boolean);
  /* Practice and weekly answers move skill scores and the streak's problem count (no XP, no MP) */
  const practiced = (res, source) => { try { S().practiceResult({ results: (res || []).filter(Boolean).map(resultRow), source }); } catch (e) { console.error(e); } };

  /* Every level whose lessons are all finished gets its homework, if the file is written (assigned lazily here) */
  const assignDue = () => {
    let n = 0;
    try {
      const done = Object.entries(S().lessons).filter(([, r]) => r && r.done).map(([id]) => id.split('/')[0]);
      [...new Set(done)].forEach(cid => {
        (course(cid) || {}).levels?.forEach(lv => {
          if (!lv.homework || S().homework[`${cid}/${lv.homework}`]) return;
          if (!(lv.lessons || []).length || !(lv.lessons || []).every(l => lessonDone(cid, l))) return;
          if (C().exists(cid, lv.homework) === false) return;
          S().homeworkAssigned({ course: cid, level: lv.n, dueDays: 7 }); n++;
        });
      });
    } catch (e) { console.error(e); }
    return n;
  };

  /* Notation (docs/AUTHORING.md section 6), with the rows each track adds */
  const NOTATION = [
    ['X, Y', 'Random variables are capitals'], ['x, y', 'Their values are lower case'], ['\\mathbf{v}', 'Vectors are bold lower case'],
    ['\\mathbf{A}', 'Matrices are bold capitals'], ['P(A)', 'Probability of an event'], ['E[X]', 'Expectation'], ['Var(X)', 'Variance'],
    ['\\ln x', 'Natural logarithm'], ['0.25', 'Decimals inside maths; percentages such as 25% in prose'], ['£', 'Money in one currency within a course'],
  ];
  const NOTATION_TRACK = {
    prob: [['P(A \\mid B)', 'Probability of A given B'], ['A \\cap B', 'A and B both happen'], ['A \\cup B', 'A or B or both'], ['A^c', 'A does not happen'],
      ['X \\sim \\text{Bin}(n, p)', 'X has this distribution'], ['Cov(X, Y)', 'Covariance']],
    maths: [['f^{-1}', 'Inverse function'], ['\\sum_{k=1}^{n}', 'Sum over k from 1 to n'], ['\\frac{dy}{dx}', 'Derivative of y with respect to x'], ['\\int_a^b f(x)\\,dx', 'Definite integral']],
    fin: [['r_t', 'Return in period t'], ['\\sigma', 'Volatility, a standard deviation']],
    ml: [['\\hat{y}', 'A fitted or predicted value'], ['\\mathbf{X}', 'The data matrix, one row per observation']],
  };
  const notationSheet = (Z, t) => {
    const rows = NOTATION.concat(NOTATION_TRACK[t.track] || []);
    Z.sheet(`<div class="rv-note" data-track="${Z.esc(t.track || 'prob')}">
      <span class="t-overline muted">Notebook · Notation</span>
      <h2 class="t-sheet-title">${Z.esc(t.id)} ${Z.esc(t.name)}</h2>
      <p class="t-body secondary">The symbols every lesson in this topic uses, and what each one means.</p>
      <table class="rv-nt"><thead><tr><th scope="col">Symbol</th><th scope="col">Meaning</th></tr></thead>
        <tbody>${rows.map(([s, m]) => `<tr><td>${s === '£' ? '£' : Z.tex(s)}</td><td class="t-body">${Z.esc(m)}</td></tr>`).join('')}</tbody></table>
    </div>`, { label: `Notation for ${t.name}` });
  };

  /* =====================================================================================
     HUB
     ===================================================================================== */
  function hub(root, Z) {
    const I = Z.icon, esc = Z.esc;
    const prepPaths = (() => { try { return C().prepPaths(); } catch { return []; } })();
    let alive = true;
    assignDue();
    const sum = S().summary();
    const mastery = sum.skillMastery || {};
    const names = skillNames();

    /* ---------- Redo queue ---------- */
    const all = S().redo.list().sort((a, b) => a.due - b.due);
    const dueIds = new Set(S().redo.due().map(r => r.id));
    const due = all.filter(r => dueIds.has(r.id)), later = all.filter(r => !dueIds.has(r.id));
    const shown = due.concat(later).slice(0, 8);
    const redoRow = (r, i) => {
      const c = course(r.ref && r.ref.course);
      const isDue = dueIds.has(r.id);
      return `<li class="rv-q ${isDue ? '' : 'is-later'}" data-track="${esc(trackOf(r.ref && r.ref.course))}">
        <span class="rv-tag" aria-hidden="true">${esc(c ? c.topic : '·')}</span>
        <div class="rv-q-body">
          <p class="rv-q-stem" data-stem="${i}">${esc(ZQ.select.source(r.ref, r.kind))}</p>
          <p class="rv-q-meta"><span class="chip rv-due ${r.interval >= 30 ? 'd30' : ''}">${I('replay', 'xs')}${r.interval}-day</span>
            <span class="t-caption ${isDue ? 'rv-due-now' : 'secondary'}">${esc(whenDue(r.due))}</span>
            <span class="t-caption muted rv-src" data-src="${i}"></span></p>
        </div>
      </li>`;
    };
    const redoCard = () => `
      <div class="rv-redo-head">
        <div class="rv-redo-t">
          <span class="t-overline rv-ov">${I('review', 'xs')}Redo queue</span>
          <h2 class="t-h1" id="rv-redo-h" tabindex="-1">${due.length ? `${plural(due.length, 'problem', 'problems')} due today` : all.length ? 'Nothing due today' : 'Queue clear'}</h2>
        </div>
        ${all.length ? `<span class="rv-time">${I('clock', 'xs')}<span class="tnum">${due.length ? `About ${due.length * 2} min` : `${plural(all.length, 'item', 'items')} waiting`}</span></span>` : ''}
      </div>
      <p class="t-body secondary rv-redo-why">Each one is a problem you missed. It comes back after 7 days and again after 30. A right answer earns mastery points; XP only counts activity.</p>
      ${shown.length ? `<ol class="rv-qs">${shown.map(redoRow).join('')}</ol>` : `<p class="t-body rv-empty">${I('check', 'sm')}<span>No problems are waiting. Missed screens, quiz items and homework items land here.</span></p>`}
      <div class="rv-redo-foot">
        ${due.length ? `<a class="btn block" href="#redo" data-start-redo>Start redo, about ${due.length * 2} min</a>` : ''}
        ${later.length ? `<p class="t-caption muted">Next: ${plural(later.filter(r => dayKey(r.due) === dayKey(later[0].due)).length, 'problem', 'problems')} due ${esc(dayDate(later[0].due))}.${all.length > shown.length ? ` ${all.length - shown.length} more not shown.` : ''}</p>` : ''}
      </div>`;

    /* ---------- Homework ---------- */
    const hwRows = () => {
      const recs = Object.entries(S().homework).map(([key, h]) => { const [cid, id] = key.split('/'); return { key, cid, id, h }; })
        .sort((a, b) => (a.h.submitted - b.h.submitted) || (a.h.due - b.h.due));
      const row = ({ cid, id, track, over, title, status, extra = '', btn, href, disabled }) => `<li class="rv-hw" data-track="${esc(track)}">
          <span class="rv-art" aria-hidden="true">${art(artOf(cid))}</span>
          <div class="rv-hw-body"><span class="t-overline rv-deep">${over}</span><h3 class="t-h2">${title}</h3><p class="t-caption secondary rv-hw-st">${status}</p>${extra}</div>
          ${disabled ? `<span class="btn secondary rv-hw-go" aria-disabled="true">${btn}</span>` : `<a class="btn secondary rv-hw-go" href="${href}">${btn}</a>`}</li>`;
      const out = recs.map(({ cid, id, h }) => {
        const lv = levelOfId(cid, id) || { n: id.split('-')[1], name: '' };
        const draft = store.get(`hw.draft.${cid}/${id}`, null);
        const answered = draft && Array.isArray(draft.values) ? draft.values.filter(v => !empty(v)).length : 0;
        const base = { cid, id, track: trackOf(cid), over: `${esc(courseName(cid))} · <span class="rv-nw">Level ${esc(lv.n)}</span>`, title: `Homework ${esc(lv.n)}${lv.name ? ' · ' + esc(lv.name) : ''}`, href: `#homework/${cid}/${id}` };
        if (h.submitted) {
          const R = store.get(`hw.result.${cid}/${id}`, null);
          return row({ ...base, status: `${I('check', 'xs')}<span>Marked · ${h.score} of ${h.items} items right${R ? `, ${R.marks} of ${R.total} marks` : ''} · ${esc(dayDate(h.submittedAt || h.due))}</span>`, btn: 'See marks' });
        }
        const overdue = h.due < Date.now();
        return row({ ...base, status: `${I('clock', 'xs')}<span>${overdue ? `Overdue since ${esc(dayDate(h.due))}` : `${esc(whenDue(h.due))}, in ${plural(Math.max(0, daysFrom(h.due)), 'day', 'days')}`}${answered ? ` · ${answered} answered` : ''}</span>`, btn: answered ? 'Continue' : 'Open' });
      });
      /* The level in progress: homework not yet released, with a start-early path */
      const started = [...new Set(Object.entries(S().lessons).filter(([, r]) => r && r.done).map(([id]) => id.split('/')[0]))];
      started.forEach(cid => {
        const c = course(cid); if (!c) return;
        const lv = (c.levels || []).find(l => l.homework && !S().homework[`${cid}/${l.homework}`] && (l.lessons || []).some(x => lessonDone(cid, x)));
        if (!lv) return;
        const done = lv.lessons.filter(x => lessonDone(cid, x)).length;
        const writtenHw = C().exists(cid, lv.homework) !== false;
        out.push(row({ cid, id: lv.homework, track: trackOf(cid), over: `${esc(c.name)} · <span class="rv-nw">Level ${lv.n}</span>`, title: `Homework ${lv.n} · ${esc(lv.name)}`,
          status: `${I('lock', 'xs')}<span>Set when you finish Level ${lv.n}: ${done} of ${lv.lessons.length} lessons done.${writtenHw ? ' You can start it early.' : ' Not yet written.'}</span>`,
          btn: writtenHw ? 'Start early' : 'Not yet written', href: `#homework/${cid}/${lv.homework}`, disabled: !writtenHw }));
      });
      return out.length ? `<ul class="rv-hws">${out.join('')}</ul>` : `<p class="t-body secondary rv-empty">${I('clipboard', 'sm')}<span>Homework is set when you finish the last lesson of a level: six to twelve problems, due in 7 days.</span></p>`;
    };

    /* ---------- Practice ---------- */
    const weakest = Object.entries(mastery).filter(([k]) => S().skills[k] && S().skills[k].seen).sort((a, b) => a[1] - b[1]).slice(0, 5);
    const weekly = ZQ.select.weeklyStatus();
    const weeklyHTML = () => {
      if (!weekly.eligible) return `<div class="rv-wk is-off" data-track="prob"><span class="rv-tag sm" aria-hidden="true">1.5</span><div class="rv-wk-t"><span class="t-label">Weekly probability problems</span><span class="t-caption secondary">Three a week, once you finish a lesson in 1.5 Probability.</span></div></div>`;
      const finished = weekly.done >= weekly.total;
      return `<a class="rv-wk" data-track="prob" href="#practice/weekly" ${finished ? 'aria-disabled="true"' : ''}>
        <span class="rv-tag sm" aria-hidden="true">1.5</span>
        <span class="rv-wk-t"><span class="t-label">Weekly probability problems</span><span class="t-caption secondary">${finished ? 'Done for this week. Three new ones arrive on Monday.' : `${weekly.done} of ${weekly.total} done this week · about 6 min`}</span></span>
        <span class="rv-segs rv-wk-segs" aria-hidden="true">${Array.from({ length: weekly.total }, (_, i) => `<i class="${i < weekly.done ? 'on' : ''}"></i>`).join('')}</span>
        ${finished ? '' : I('chevronR', 'sm rv-chev')}</a>`;
    };
    const practiceHTML = `
      <div class="rv-pset" data-pset>
        <p class="t-body secondary rv-pset-l">Eight problems from the quizzes and reviews of lessons you have finished, interleaved and weighted to your weakest skills.</p>
        ${weakest.length ? `<ul class="rv-sk" aria-label="Weakest skills">${weakest.map(([k, v]) => `<li><span class="t-body">${esc(names[k] || k)}</span><span class="bar track thin" aria-hidden="true"><i style="width:${Math.round(v * 100)}%"></i></span><span class="t-label tnum">${Math.round(v * 100)}%</span></li>`).join('')}</ul>` : ''}
        <div data-pset-go><span class="t-caption muted">Finding problems</span></div>
      </div>
      ${weeklyHTML()}`;

    /* ---------- Notebook ---------- */
    const cards = S().notebook.list();
    const byCourse = {};
    cards.forEach(c => { (byCourse[c.course || ''] = byCourse[c.course || ''] || []).push(c); });
    const topicIds = new Set(cards.map(c => (course(c.course) || {}).topic).filter(Boolean));
    Object.keys(S().lessons).forEach(id => { const t = (course(id.split('/')[0]) || {}).topic; if (t) topicIds.add(t); });
    const topics = [...topicIds].map(t => C().topic(t)).filter(Boolean);
    const nbCard = (c, i) => `<li><button type="button" class="rv-nb" data-nb="${i}" data-track="${esc(trackOf(c.course))}">
        <span class="t-label">${esc(c.name)}</span>
        <span class="rv-nb-f">${c.tex ? Z.tex('\\displaystyle ' + c.tex) : ''}</span>
        <span class="t-caption muted">${esc(ZQ.select.source({ course: c.course, lesson: c.lesson }, 'quiz').replace(/ quiz$/, ''))}</span></button></li>`;
    const notebookHTML = `
      ${cards.length ? Object.entries(byCourse).map(([cid, list]) => `<div class="rv-nb-g"><h3 class="t-label rv-nb-h">${esc(courseName(cid))}</h3>
        <ul class="rv-nbs">${list.map(c => nbCard(c, cards.indexOf(c))).join('')}</ul></div>`).join('')
        : `<p class="t-body secondary rv-empty">${I('book', 'sm')}<span>Each lesson summary saves its formula card here.</span></p>`}
      <div class="rv-nb-g"><h3 class="t-label rv-nb-h">Notation</h3>
        <ul class="rv-nbs">${(topics.length ? topics : [{ id: '', name: 'Every topic', track: 'maths' }]).map((t, i) => `<li><button type="button" class="rv-nb rv-nb-n" data-nt="${i}" data-track="${esc(t.track || 'maths')}">
          <span class="t-label">Notation${t.id ? ' · ' + esc(t.id) : ''}</span><span class="rv-nb-f">${Z.tex('P(A \\mid B),\\ E[X],\\ \\mathbf{v}')}</span><span class="t-caption muted">${esc(t.name)}</span></button></li>`).join('')}</ul></div>`;

    root.innerHTML = `
      <div class="rv">
        <header class="rv-head">
          <h1 class="t-h1">Review</h1>
          <p class="t-body secondary">Clear the redo queue first, then homework. Practice sets lean on your weakest skills.</p>
        </header>
        <div class="rv-grid">
          <div class="rv-col">
            <section class="card rv-redo" aria-labelledby="rv-redo-h" data-sec="redo">${redoCard()}</section>
            <section class="card rv-card" aria-labelledby="rv-hw-h" data-sec="homework">
              <div class="rv-card-h"><h2 class="t-h2" id="rv-hw-h">Homework</h2><span class="t-caption muted">One set per level, due 7 days after it is set</span></div>
              ${hwRows()}
            </section>
            <section class="card rv-card" aria-labelledby="rv-mk-h" data-sec="mocks" ${prepPaths.length ? '' : 'hidden'}>
              <div class="rv-card-h"><h2 class="t-h2" id="rv-mk-h">Mock assessments</h2><span class="t-caption muted">Timed, as the real ones are. Sit them as often as you like</span></div>
              ${prepPaths.length ? `<a class="rv-prep" href="#prepare">${Z.icon('target', 'xs')}<span>Prepare for an assessment or a firm</span>${Z.icon('chevronR', 'xs')}</a>` : ''}
              <div data-mocks></div>
            </section>
            <section class="card rv-card" aria-labelledby="rv-ex-h" data-sec="exams">
              <div class="rv-card-h"><h2 class="t-h2" id="rv-ex-h">Exams</h2><span class="t-caption muted">Timed, no hints, no retries</span></div>
              <div data-exams><p class="t-caption muted">Loading exams</p></div>
            </section>
          </div>
          <div class="rv-col">
            <section class="card rv-card" aria-labelledby="rv-pr-h" data-sec="practice" data-track="prob">
              <div class="rv-card-h"><h2 class="t-h2" id="rv-pr-h">Practice</h2><span class="t-caption muted">Mastery of the skills you have met</span></div>
              ${practiceHTML}
            </section>
            <section class="card rv-card" aria-labelledby="rv-bk-h" data-sec="bank" data-track="speed" hidden>
              <div class="rv-card-h"><h2 class="t-h2" id="rv-bk-h">Interview practice</h2><span class="t-caption muted">Each question on its own schedule</span></div>
              <div class="rv-bk" data-bank></div>
            </section>
            <section class="card rv-card" aria-labelledby="rv-nb-h" data-sec="notebook">
              <div class="rv-card-h"><h2 class="t-h2" id="rv-nb-h">Notebook</h2><span class="t-caption muted">${plural(cards.length, 'formula card', 'formula cards')}</span></div>
              ${notebookHTML}
            </section>
          </div>
        </div>
      </div>`;

    /* ---------- Async fills: redo stems, practice pool, exams ---------- */
    shown.forEach((r, i) => {
      ZQ.select.resolve(r.ref, r.kind).then(it => {
        if (!alive) return;
        const el = root.querySelector(`[data-stem="${i}"]`), src = root.querySelector(`[data-src="${i}"]`);
        if (!el) return;
        if (it && stemOf(it)) { el.innerHTML = md(stemOf(it)); if (src) src.textContent = ZQ.select.source(r.ref, r.kind); }
      }).catch(e => console.warn(e));
    });
    ZQ.select.pool({}).then(items => {
      if (!alive) return;
      const go = root.querySelector('[data-pset-go]');
      if (!go) return;
      go.innerHTML = items.length
        ? `<a class="btn track block" href="#practice" data-start-practice>Start a practice set, ${Math.min(PRACTICE_N, items.length)} problems</a><p class="t-caption muted rv-pset-n">${plural(items.length, 'problem', 'problems')} in your pool. <a class="link-btn" href="#practice/timed/${PRACTICE_N * 60}">Or against the clock, ${PRACTICE_N} minutes</a></p>`
        : `<p class="t-body rv-empty">${I('lock', 'sm')}<span>Finish a lesson to unlock practice. Sets draw on the quizzes of lessons you have finished.</span></p>`;
    }).catch(e => console.error(e));

    /* ---------- Interview practice (content/bank and tagged items of finished lessons) ---------- */
    ZQ.select.bankStatus().then(st => {
      if (!alive) return;
      const sec = root.querySelector('[data-sec="bank"]'), el = root.querySelector('[data-bank]');
      if (!sec || !el || (!st.total && !st.locked)) return;
      const fams = Object.keys(st.families).length, todo = st.due + st.fresh;
      const line = todo ? `${plural(st.due, 'question', 'questions')} due and ${st.fresh} new, from ${plural(fams, 'family', 'families')}.`
        : st.later ? `Nothing due. The next question comes back${st.nextDue ? ' on ' + dayDate(st.nextDue) : ' soon'}.` : 'No questions are available yet.';
      el.innerHTML = `<p class="t-body secondary rv-bk-l">Interview-style questions from several families, mixed. A right answer moves a question to a longer wait: 1, 3, 7, then 30 days. A miss starts it again.</p>
        <p class="t-body rv-bk-n tnum" data-bank-line>${esc(line)}${st.later && todo ? ` ${st.later} scheduled for later.` : ''}${st.locked ? ` ${plural(st.locked, 'more question unlocks', 'more questions unlock')} as you finish lessons.` : ''}</p>
        ${todo ? `<a class="btn track block" href="#bank" data-start-bank>Start interview practice, ${Math.min(BANK_N, todo)} questions</a>` : ''}`;
      sec.hidden = false;
    }).catch(e => console.error(e));

    const examsEl = root.querySelector('[data-exams]');
    const topicsAll = C().stages().flatMap(s => s.topics.map(t => ({ ...t, stage: s.id })));
    Promise.all([
      Promise.all(topicsAll.map(t => C().exam(`topic-${t.id}`).catch(() => null).then(doc => (doc ? { t, doc } : C().examWritten(`topic-${t.id}`) === false ? { t, doc: null } : null)))),
      Promise.all(C().stages().map(s => C().exam(`stage-${s.id}`).catch(() => null).then(doc => (doc ? { s, doc } : null)))),
    ]).then(([tops, stages]) => {
      if (!alive) return;
      tops = tops.filter(Boolean); stages = stages.filter(Boolean);
      const ringC = 2 * Math.PI * 22;
      const attempts = (id) => ((S().exams[id] || {}).attempts || []);
      const best = (id) => attempts(id).reduce((b, a) => Math.max(b, a.items ? a.score / a.items : 0), -1);
      const sb = (t) => C().strandBadge(C().topicStrand(t), C().strandNoteOf(t.courses), 'is-sm');
      const topicRow = ({ t, doc }) => {
        if (!doc) return `<li class="rv-ex is-unwritten" data-track="${esc(t.track)}">
          <div class="rv-ex-body"><span class="t-overline rv-deep">${esc(t.id)} ${esc(t.name)} ${sb(t)}</span><h3 class="t-h2">Topic exam</h3>
            <p class="t-caption secondary">Not written yet.</p></div></li>`;
        const id = doc.id, at = attempts(id), passed = at.some(a => a.passed);
        const sk = Object.keys(doc.skills || {});
        const ready = sk.length ? Math.round(sk.reduce((s, k) => s + (mastery[k] || 0), 0) / sk.length * 100) : 0;
        const unlocked = (t.courses || []).every(cid => C().courseLessons(cid).some(x => x.kind === 'lesson' && (S().lesson(cid, x.id) || {}).mastered));
        const b = best(id);
        const note = passed ? `Passed. Best ${Math.round(b * 100)}%. You can sit it again at any time.`
          : at.length ? `Best so far ${Math.round(b * 100)}%. Pass mark ${Math.round(doc.pass * 100)}%. ${doc.minutes} min.`
          : unlocked ? `Unlocked: every course has a mastered lesson. ${doc.minutes} min, pass mark ${Math.round(doc.pass * 100)}%.`
          : `Sit it early to test out. ${doc.minutes} min, pass mark ${Math.round(doc.pass * 100)}%. ${ready}% ready, from your mastery map.`;
        return `<li class="rv-ex" data-track="${esc(t.track)}">
          <span class="rv-ring" role="img" aria-label="${ready}% ready"><svg viewBox="0 0 56 56" aria-hidden="true"><circle cx="28" cy="28" r="22" class="rv-ring-t"/><circle cx="28" cy="28" r="22" class="rv-ring-f" ${ready ? '' : 'opacity="0"'} stroke-dasharray="${(ringC * ready / 100).toFixed(2)} ${ringC.toFixed(2)}" transform="rotate(-90 28 28)"/></svg><span class="tnum" aria-hidden="true">${passed ? I('check', 'sm') : ready + '%'}</span></span>
          <div class="rv-ex-body"><span class="t-overline rv-deep">${esc(t.id)} ${esc(t.name)} ${sb(t)}</span><h3 class="t-h2">Topic exam</h3>
            <p class="t-caption secondary">${esc(note)}</p></div>
          <a class="btn secondary" href="#exam/${esc(id)}">${at.length ? 'Sit again' : 'Sit exam'}</a></li>`;
      };
      const stageBlock = ({ s, doc }) => {
        const at = attempts(doc.id), passed = at.some(a => a.passed);
        return `<div class="rv-exit" data-track="maths">
          <div class="rv-exit-h"><h3 class="t-label">Stage ${s.id} exit test</h3><span class="t-caption muted">${passed ? 'Passed' : at.length ? `${plural(at.length, 'attempt', 'attempts')}, not passed yet` : `Pass every part to leave ${esc(s.name)}`}</span></div>
          <ul class="rv-exit-l">${(doc.parts || []).map(p => `<li data-track="${p.kind === 'check' ? 'code' : 'maths'}"><div class="rv-exit-r is-static">
            <span class="rv-exit-n"><span class="t-label">${esc(p.name)}</span><span class="t-caption muted">${p.kind === 'paper' ? `${plural((p.items || []).length, 'question', 'questions')} · ${p.minutes} min` : 'You tick this yourself'}</span></span>
            <span class="rv-pass t-label tnum">${p.kind === 'paper' ? `Pass ${Math.round(p.pass * 100)}%` : 'Self-tick'}</span><span class="rv-chev-sp" aria-hidden="true"></span></div></li>`).join('')}</ul>
          <a class="btn secondary block" href="#exam/${esc(doc.id)}">${at.length ? 'Sit again' : 'Sit the exit test'}</a>
        </div>`;
      };
      examsEl.innerHTML = (tops.length ? `<ul class="rv-exs">${tops.map(topicRow).join('')}</ul>` : '<p class="t-body secondary rv-empty">No topic exams are written yet.</p>') + stages.map(stageBlock).join('');
    }).catch(e => { console.error(e); examsEl.innerHTML = '<p class="t-body secondary">The exams could not be listed.</p>'; });

    /* ---------- Mock assessments (exams/mock-*.json): every attempt kept, with a net score trend ---------- */
    const mocksEl = root.querySelector('[data-mocks]'), mocksSec = root.querySelector('[data-sec="mocks"]');
    const mockIds = (() => { try { return C().mocks(); } catch { return []; } })();
    if (mockIds.length) {
      Promise.all(mockIds.map(id => C().exam(id).catch(() => null))).then(docs => {
        if (!alive) return;
        const list = docs.filter(d => d && d.id);
        if (!list.length) return;
        const M = ZQ.mock;
        const row = (doc) => {
          const papers = (Array.isArray(doc.parts) ? doc.parts : [doc]).filter(p => Array.isArray(doc.parts) ? p.kind === 'paper' : true);
          const n = papers.reduce((a, p) => a + (p.items || []).reduce((b, it) => b + (it && it.generator ? Math.max(1, +it.n || 1) : 1), 0), 0);
          const minutes = papers.reduce((a, p) => a + (+p.minutes || 0), 0);
          const ways = [...new Set(papers.flatMap(p => [p.navigation === 'forward' ? 'forward only' : null, M.scored(p) ? 'negative marking' : null]).filter(Boolean))];
          const at = ((S().exams[doc.id] || {}).attempts || []);
          const nets = at.map(a => (typeof a.net === 'number' ? a.net : a.score));
          const single = papers.length === 1 && !(Array.isArray(doc.parts) && doc.parts.some(p => p.kind === 'check')) ? papers[0] : null;
          const need = single ? M.need(single, M.scoring(single).right * (single.items || []).reduce((b, it) => b + (it && it.generator ? Math.max(1, +it.n || 1) : 1), 0)) : null;
          const st = M.style(doc.style);
          const note = at.length ? `${plural(at.length, 'attempt', 'attempts')}. Latest ${M.signed(nets[nets.length - 1])}, best ${M.signed(Math.max(...nets))}${need != null ? `, pass mark ${M.signed(need)}` : ''}. ${at[at.length - 1].passed ? 'Latest passed.' : 'Latest not passed.'}` : 'Not sat yet. Every attempt is kept.';
          return `<li class="rv-ex rv-mk" data-track="${esc(st.track)}" data-mock="${esc(doc.id)}">
            <span class="rv-ex-ic">${I('timer')}</span>
            <div class="rv-ex-body"><span class="t-overline rv-deep">${esc(st.label)} · ${esc(String(minutes))} min · ${plural(n, 'question', 'questions')}${ways.length ? ' · ' + esc(ways.join(', ')) : ''}</span>
              <h3 class="t-h2">${esc(doc.name || doc.id)}</h3>
              ${doc.models ? `<p class="t-caption secondary">Models ${esc(doc.models)}</p>` : ''}
              <p class="t-caption secondary tnum">${esc(note)}</p>
              ${nets.length ? `<div class="rv-mk-tr">${M.trend(nets, { pass: need, label: `${doc.name || doc.id}, net score by attempt` })}</div>` : ''}</div>
            <a class="btn secondary" href="#exam/${esc(doc.id)}">${at.length ? 'Sit again' : 'Sit mock'}</a></li>`;
        };
        mocksEl.innerHTML = `<ul class="rv-exs">${list.map(row).join('')}</ul>`;
        mocksSec.hidden = false;
      }).catch(e => console.error(e));
    }

    /* ---------- Events ---------- */
    const onClick = (e) => {
      const nb = e.target.closest('[data-nb]');
      if (nb) {
        const c = cards[+nb.dataset.nb]; if (!c) return;
        Z.sheet(`<div class="rv-note" data-track="${esc(trackOf(c.course))}">
          <span class="t-overline muted">Notebook · ${esc(ZQ.select.source({ course: c.course, lesson: c.lesson }, 'quiz').replace(/ quiz$/, ''))}</span>
          <h2 class="t-sheet-title">${esc(c.name)}</h2>
          <div class="rv-note-f">${c.tex ? Z.tex('\\displaystyle ' + c.tex) : ''}</div>
          ${c.note ? `<p class="t-body">${md(c.note)}</p>` : ''}
          <div class="rv-note-b"><h3 class="t-label">Saved</h3><p class="t-body">${esc(dayDate(c.at || Date.now()))}, from the lesson summary.</p></div>
          ${c.course && c.lesson ? `<a class="btn secondary block" href="#lesson/${esc(c.course)}/${esc(c.lesson)}">Open the lesson</a>` : ''}
        </div>`, { label: c.name });
        return;
      }
      const nt = e.target.closest('[data-nt]');
      if (nt) { const t = topics[+nt.dataset.nt] || { id: '', name: 'Every topic', track: 'maths' }; notationSheet(Z, t); return; }
      const wk = e.target.closest('.rv-wk[aria-disabled="true"]'); if (wk) { e.preventDefault(); }
    };
    root.addEventListener('click', onClick);
    return () => { alive = false; root.removeEventListener('click', onClick); };
  }

  /* =====================================================================================
     SET PAGE: intro card, then ZQ.player.runSet, then a summary. Shared by the level review, practice and redo.
     ===================================================================================== */
  function setPage(host, Z, cfg) {
    const I = Z.icon, esc = Z.esc;
    let alive = true, run = null, t0 = 0, finished = false, timedOut = false, tick = 0, offset = 0;   // cfg.timed is read once the items have loaded
    host.innerHTML = `
      <div class="hw rvs" data-track="${esc(cfg.track || 'prob')}">
        <header class="hw-top">
          <div class="hw-left">
            <button type="button" class="icon-btn hw-close" aria-label="Close and return to Review">${I('close')}</button>
            <div class="hw-ttl"><span class="hw-ttl-a">${esc(cfg.title)}</span><span class="t-caption muted hw-ttl-b">${esc(cfg.sub || '')}</span></div>
          </div>
          <span></span>
          <div class="hw-due"><span class="hw-due-a" data-right></span></div>
        </header>
        <main class="hw-frame"><div class="hw-scroll"><div class="hw-col" tabindex="-1" data-col><p class="t-caption muted">Loading</p></div></div>
          <footer class="hw-foot"><div class="hw-actions" data-acts></div></footer></main>
      </div>`;
    const col = host.querySelector('[data-col]'), acts = host.querySelector('[data-acts]'), right = host.querySelector('[data-right]'), foot = host.querySelector('.hw-foot');
    const leave = () => Z.go('review');
    host.querySelector('.hw-close').addEventListener('click', leave);
    const setActs = (html) => { acts.innerHTML = html; acts.classList.toggle('one', acts.children.length === 1); foot.hidden = !html; };

    const intro = (items) => {
      if (!alive) return;
      if (!items.length) {
        col.innerHTML = `<section class="hw-intro rvs-empty"><span class="t-overline hw-deep">${esc(cfg.over || '')}</span><h1 class="t-lesson-title">${esc(cfg.emptyTitle || 'Nothing to do here')}</h1><p class="t-prose">${esc(cfg.emptyText || '')}</p></section>`;
        setActs('<button type="button" class="btn hw-primary" data-back>Back to Review</button>');
        return;
      }
      right.innerHTML = `${I('clipboard', 'xs')}<span>${plural(items.length, 'problem', 'problems')}</span>`;
      col.innerHTML = `<section class="hw-intro">
        <span class="t-overline hw-deep">${esc(cfg.over || '')}</span>
        <h1 class="t-lesson-title">${esc(cfg.heading || cfg.title)}</h1>
        <p class="t-prose">${esc(cfg.lede || '')}</p>
        <ul class="hw-facts">
          <li>${I('clock', 'sm')}<span>${cfg.timed ? `${esc(clock(cfg.timed.seconds))} on the clock. ${plural(items.length, 'problem', 'problems')}. The clock starts when you press Start.` : `About ${Math.max(2, Math.round(items.length * (cfg.perItem || 1.5)))} minutes. ${plural(items.length, 'problem', 'problems')}.`}</span></li>
          ${cfg.timed ? `<li>${I('timer', 'sm')}<span>${cfg.timed.lockAtZero ? 'At zero the set ends and what you have not answered counts as missed.' : 'The clock is a guide: at zero you can carry on.'} Your score shows as you go.</span></li>` : ''}
          <li>${I('lock', 'sm')}<span>No hints and one try each. Why? opens the explanation after you check.</span></li>
          ${(cfg.facts || []).map(([ic, t]) => `<li>${I(ic, 'sm')}<span>${esc(t)}</span></li>`).join('')}
        </ul>
        <ol class="hw-ov">${items.map((it, j) => `<li><span class="hw-ov-n tnum">${j + 1}</span><span class="t-body rvs-ov-t">${esc(it.title || it.source || '')}</span>${pips(it.difficulty || 2)}<span class="t-caption muted hw-ov-m">${esc(cfg.tag ? cfg.tag(it) : '')}</span></li>`).join('')}</ol>
      </section>`;
      setActs(`<button type="button" class="btn hw-primary" data-start>Start</button>`);
      Z.mathify(col);
    };
    /* Test hook around the set (docs/PLAN.md 7): 'loading', then 'start' (continue() presses Start) or 'empty'; runSet
       installs its own hook while the items run; 'done' on the summary */
    let phase = 'loading';
    const hook = {
      current: () => ({ kind: phase, phase: 'set', state: 'read', screenIndex: -1, total: items0.length }),
      answerCorrect: () => false, check: async () => null,
      continue: () => { if (phase === 'start') start(items0); return Promise.resolve(); },
    };
    window.ZQ.test = hook;
    /* ---------- The clock of a timed set: countdown and live score; the page, not the engine, ends the set ---------- */
    const remaining = () => (cfg.timed ? cfg.timed.seconds - ((Date.now() - t0) / 1000 + offset) : Infinity);
    /* what an item is worth so far: 1 when right, else the share of its parts right (an item with parts, ENGINE-BACKLOG 467), else 0 */
    const creditOf = (res) => Math.round(res.reduce((a, x) => a + (x ? (x.ok ? 1 : typeof x.credit === 'number' ? x.credit : 0) : 0), 0) * 10) / 10;
    const drawClock = () => {
      if (!cfg.timed || !run || finished) return;
      const r = remaining(), res = run.results(), ok = creditOf(res), n = res.filter(Boolean).length;
      const low = r <= Math.min(60, cfg.timed.seconds / 4);
      if (!right.querySelector('.rvs-timer')) {
        right.classList.add('is-timed');
        right.innerHTML = `<span class="rvs-timer" role="timer">${I('timer', 'xs')}<span class="tnum" data-time></span></span><span class="t-caption muted rvs-live tnum"></span>`;
      }
      const tm = right.querySelector('.rvs-timer');
      tm.classList.toggle('is-low', low);
      tm.setAttribute('aria-label', r <= 0 ? 'Time is up' : low ? 'Time left, running low' : 'Time left');
      right.querySelector('[data-time]').textContent = clock(r);
      right.querySelector('.rvs-live').textContent = `Score ${ok} of ${n}${n < items0.length ? ` · ${items0.length - n} to go` : ''}`;
      if (r <= 0 && cfg.timed.lockAtZero && !timedOut) { timedOut = true; clearInterval(tick); run.finish(); }
    };
    const start = (items) => {
      col.innerHTML = ''; setActs('');
      t0 = Date.now(); offset = 0; timedOut = false;
      phase = 'running';
      run = ZQ.player.runSet(col, { title: cfg.setTitle || cfg.title, items, mode: 'set', track: cfg.track || 'prob', onDone: (res) => done(items, res) });
      host._run = run;
      if (cfg.timed) {
        clearInterval(tick); drawClock(); tick = setInterval(drawClock, 250);
        window.ZQSet = { timed: cfg.timed, remaining, setRemaining: (s) => { offset = cfg.timed.seconds - s - (Date.now() - t0) / 1000; drawClock(); } };
      }
    };
    const done = (items, res) => {
      if (finished) return;
      finished = true;
      clearInterval(tick);
      const seconds = Math.round((Date.now() - t0) / 1000);
      const out = cfg.record(items, res, seconds) || {};
      if (run) { run.destroy(); run = null; }
      delete window.ZQSet;
      phase = 'done'; window.ZQ.test = hook;
      summary(items, res, out);
    };
    const summary = (items, res, out) => {
      const nRight = res.filter(r => r && r.ok).length;
      const partsCredit = res.some(r => r && typeof r.credit === 'number') ? creditOf(res) : null;
      const pace = ZQ.mock.pacing(paceRows(items, res));
      col.innerHTML = `<section class="hw-sum">
        <span class="t-overline hw-deep">${esc(cfg.over || '')}</span>
        <h1 class="t-complete">${esc(cfg.doneTitle || 'Set complete')}</h1>
        <div class="hw-score-big"><span class="t-stat tnum" data-count>${nRight}</span><span class="t-h2 secondary">of ${items.length} right</span></div>
        ${partsCredit != null ? `<p class="t-body hw-late hw-credit"><span>Counting each part of a multi-part problem: ${partsCredit} of ${items.length}.</span></p>` : ''}
        ${timedOut ? `<p class="t-body hw-late">${I('timer', 'sm')}<span>Time ran out with ${plural(res.filter(Boolean).length, 'problem', 'problems')} answered. The rest count as missed.</span></p>` : cfg.timed ? `<p class="t-body hw-late">${I('timer', 'sm')}<span>Finished with ${esc(clock(Math.max(0, remaining())))} left on the clock.</span></p>` : ''}
        ${pace.n ? `<p class="t-body hw-late hw-pace">${I('timer', 'sm')}<span>${esc(pace.text)}</span></p>` : ''}
        <div class="hw-badges">${(out.badges || []).map(([v, l], k) => `<div class="hw-badge hw-in" style="animation-delay:${200 + k * 80}ms"><span class="t-h1 tnum">${v}</span><span class="t-caption muted">${esc(l)}</span></div>`).join('')}</div>
        ${out.note ? `<div class="hw-redo">${I('replay', 'sm')}<span>${out.note}</span></div>` : ''}
        <h2 class="t-h2 hw-res-h">Problem by problem</h2>
        <ol class="hw-res">${items.map((it, j) => { const r = res[j]; const ok = !!(r && r.ok); return `<li><div class="hw-res-r ${ok ? 'ok' : 'no'} is-static">
          <span class="hw-res-ic" aria-hidden="true">${I(ok ? 'check' : 'cross')}</span>
          <span class="hw-rl-t"><span class="t-body">${md(stemOf(it))}</span><span class="t-caption secondary">${esc(it.source || '')}${out.lines && out.lines[j] ? ' · ' + esc(out.lines[j]) : ''}${r && typeof r.seconds === 'number' ? ` · ${esc(ZQ.mock.fmtSeconds(r.seconds))}${it.pace > 0 ? ` of ${esc(ZQ.mock.fmtSeconds(it.pace))} pace` : ''}` : ''}</span></span>
          <span class="t-label tnum hw-res-m">${ok ? 'Right' : r && typeof r.credit === 'number' ? `${r.right} of ${r.of} parts` : r ? 'Not right' : 'Skipped'}</span><span></span></div></li>`; }).join('')}</ol>
      </section>`;
      setActs(`${cfg.again ? `<button type="button" class="btn secondary hw-sec" data-again>${esc(cfg.again)}</button>` : ''}<button type="button" class="btn hw-primary" data-back>Back to Review</button>`);
      right.innerHTML = `${I('check', 'xs')}<span>${nRight} of ${items.length} right</span>`;
      Z.sound('complete');
    };
    let items0 = [];
    host.addEventListener('click', (e) => {
      if (e.target.closest('[data-back]')) { leave(); return; }
      if (e.target.closest('[data-start]')) { start(items0); return; }
      if (e.target.closest('[data-again]')) { Z.go(location.hash.slice(1)); }
    });
    Promise.resolve(cfg.load()).then(items => { items0 = items || []; phase = items0.length ? 'start' : 'empty'; intro(items0); }).catch(e => { console.error(e); if (alive) { col.innerHTML = `<p class="t-body">This set could not be loaded: ${esc(e.message)}</p>`; setActs('<button type="button" class="btn hw-primary" data-back>Back to Review</button>'); } });
    return () => {
      alive = false;
      clearInterval(tick); delete window.ZQSet;
      if (window.ZQ.test === hook) delete window.ZQ.test;
      /* Leaving part way records what was answered, so a redo or review is never lost */
      if (run && !finished) {
        const res = run.results().filter(Boolean);
        if (res.length && cfg.partial) { try { cfg.partial(items0, run.results(), Math.round((Date.now() - t0) / 1000)); } catch (e) { console.error(e); } }
        run.destroy(); run = null;
      }
    };
  }

  /* timed: { seconds, lockAtZero } on a review, a practice set or a deck: a clock and a live score (ENGINE-BACKLOG 454) */
  const timedOf = (t) => (t && typeof t === 'object' && Number(t.seconds) > 0 ? { seconds: Math.round(Number(t.seconds)), lockAtZero: t.lockAtZero === true } : null);

  /* ---------- The three set kinds ---------- */
  const redoRecord = (items, res, seconds) => {
    const lines = [];
    let mp = 0, left = 0, back = 0;
    items.forEach((it, j) => {
      const r = res[j];
      if (!r || !it.redo || it._recorded) { lines[j] = ''; return; }
      it._recorded = true;
      const o = S().redo.result({ id: it.redo.id, ok: !!r.ok, seconds: 0 }) || {};
      mp += o.mp || 0;
      if (o.left) { left++; lines[j] = 'Leaves the queue'; }
      else if (r.ok) { lines[j] = `Back on ${dayDate(o.due)} for its 30-day redo`; }
      else { back++; lines[j] = `Back on ${dayDate(o.due)}`; }
    });
    logReview(seconds, 'redo');
    return { lines, mp, left, back };
  };
  function mountRedo(root, Z) {
    return setPage(root, Z, {
      title: 'Redo queue', sub: 'Problems you missed, back on schedule', over: 'Redo queue', heading: 'Redo the problems due today', track: 'prob', perItem: 2,
      lede: 'Each problem here is one you missed 7 or 30 days ago. Get it right at 7 days and it returns once more at 30; right at 30 days and it leaves the queue.',
      facts: [['target', 'A right answer earns mastery points for its skills.'], ['replay', 'A miss starts the clock again: back in 7 days.']],
      tag: (it) => (it.redo ? `${it.redo.interval}-day` : ''),
      emptyTitle: 'Nothing is due', emptyText: 'No redo problems are due today. Missed screens, quiz items and homework items come back here after 7 days.',
      doneTitle: 'Redo done', setTitle: 'Redo',
      load: () => ZQ.select.redoSession(),
      record: (items, res, seconds) => {
        const o = redoRecord(items, res, seconds);
        return { lines: o.lines, badges: [[`+${o.mp}`, 'mastery points'], [o.left, o.left === 1 ? 'problem leaves the queue' : 'problems leave the queue'], [o.back, 'back in 7 days']],
          note: o.back ? `${plural(o.back, 'miss comes', 'misses come')} back in 7 days.` : 'Every one right. Each returns at 30 days or leaves the queue.' };
      },
      partial: (items, res, seconds) => redoRecord(items, res, seconds),
    });
  }
  function mountPractice(root, Z, params) {
    const weekly = params[0] === 'weekly';
    /* #practice/timed/<seconds>: the same set against a locking clock (default 60 seconds a problem) */
    const timed = params[0] === 'timed' ? timedOf({ seconds: Math.min(7200, Math.max(30, parseInt(params[1], 10) || PRACTICE_N * 60)), lockAtZero: true }) : null;
    const done0 = ZQ.select.weeklyStatus().done;
    return setPage(root, Z, weekly ? {
      title: 'Weekly probability problems', sub: '1.5 Probability', over: 'This week', heading: 'Three probability problems', track: 'prob', perItem: 2,
      lede: 'Three problems a week from 1.5 Probability keep the topic warm while you study other things. They stay the same until Monday.',
      tag: (it) => it.source.split(' · ')[0],
      emptyTitle: 'Not yet', emptyText: 'Weekly problems start once you finish any lesson in 1.5 Probability.',
      doneTitle: 'Done for this week', setTitle: 'Weekly problems',
      load: () => ZQ.select.weeklyProbs(),
      record: (items, res, seconds) => {
        const n = res.filter(Boolean).length;
        practiced(res, 'weekly');
        const st = ZQ.select.weeklyRecord(Math.max(done0, n));
        logReview(seconds, 'weekly');
        return { badges: [[`${st.done} of ${st.total}`, 'done this week'], [res.filter(r => r && r.ok).length, 'right first time']], note: 'Three new problems arrive on Monday.' };
      },
      partial: (items, res, seconds) => { practiced(res, 'weekly'); ZQ.select.weeklyRecord(Math.max(done0, res.filter(Boolean).length)); logReview(seconds, 'weekly'); },
    } : {
      title: 'Practice set', sub: 'From the lessons you have finished', over: 'Practice', heading: timed ? 'A timed practice set' : 'A mixed practice set', track: 'prob', perItem: 1.5, timed,
      lede: 'Problems from the quizzes and reviews of lessons you have finished. The set leans on your weakest skills and the ones you have not seen for a while.',
      facts: [['review', 'Topics are mixed on purpose: switching between them is what makes them stick.']],
      tag: (it) => it.source.split(' · ')[0],
      emptyTitle: 'No practice yet', emptyText: 'Finish a lesson first. Practice sets draw on the quizzes of lessons you have finished.',
      doneTitle: 'Practice done', setTitle: 'Practice', again: timed ? 'New timed set' : 'New set',
      load: () => ZQ.select.practiceSet({ n: PRACTICE_N }),
      record: (items, res, seconds) => {
        practiced(res, 'practice');
        logReview(seconds, 'practice');
        const wrong = items.filter((it, j) => res[j] && !res[j].ok).map(it => it.source.split(' · ').slice(-1)[0]);
        const skills = new Set(items.flatMap(it => it.skills || []));
        return { badges: [[seconds < 60 ? 'Under 1 min' : Math.round(seconds / 60) + ' min', 'logged to Review'], [skills.size, skills.size === 1 ? 'skill practised' : 'skills practised']],
          note: wrong.length ? `Worth a second look: ${Z.esc(listAnd([...new Set(wrong)]))}.` : 'Every problem right. The next set leans on other skills.' };
      },
      partial: (items, res, seconds) => { practiced(res, 'practice'); logReview(seconds, 'practice'); },
    });
  }
  /* The Interview practice deck (ENGINE-BACKLOG 456): each item has its own schedule in ZQ.state.bank */
  const BANK_N = 8;
  function mountBank(root, Z) {
    return setPage(root, Z, {
      title: 'Interview practice', sub: 'Questions on their own schedule', over: 'Interview practice', heading: 'An interview practice deck', track: 'speed', perItem: 1.5,
      lede: 'Questions of the kind interviewers ask, from several families at once. Each one comes back on its own schedule: after 1, 3, 7 and then 30 days.',
      facts: [['review', 'A right answer moves a question up one box. A miss sends it back to the first.'], ['timer', 'Each question is timed. The pace line at the end shows where you were slow.']],
      tag: (it) => it.family || '',
      emptyTitle: 'Nothing due', emptyText: 'No interview questions are due, and none are new. Questions that name prerequisite lessons appear as you finish them.',
      doneTitle: 'Interview practice done', setTitle: 'Interview practice', again: 'Next deck',
      load: () => ZQ.select.bankDeck({ n: BANK_N }),
      record: (items, res, seconds) => {
        const rows = items.map((it, j) => (res[j] ? { uid: it.uid, ok: !!res[j].ok, seconds: res[j].seconds, family: it.family, pace: it.pace, difficulty: it.difficulty || 3, skills: it.skills || [] } : null)).filter(Boolean);
        let o = {};
        try { o = S().bankResult({ results: rows }) || {}; } catch (e) { console.error(e); }
        logReview(seconds, 'bank');
        const b = o.boxes || {}, wrong = rows.filter(r => !r.ok).length;
        const later = [[1, 'tomorrow'], [3, 'in 3 days'], [7, 'in 7 days'], [30, 'in 30 days']].filter(([d]) => b[d]).map(([d, w]) => `${b[d]} ${w}`);
        return { badges: [[rows.filter(r => r.ok).length, 'right'], [wrong, 'back in box 1'], [new Set(items.map(it => it.family)).size, 'families']],
          note: rows.length ? `Each question returns on its own day: ${listAnd(later)}.` : 'Nothing was answered, so nothing was scheduled.' };
      },
      partial: (items, res, seconds) => {
        const rows = items.map((it, j) => (res[j] ? { uid: it.uid, ok: !!res[j].ok, seconds: res[j].seconds, family: it.family, pace: it.pace, difficulty: it.difficulty || 3, skills: it.skills || [] } : null)).filter(Boolean);
        try { S().bankResult({ results: rows }); } catch (e) { console.error(e); }
        logReview(seconds, 'bank');
      },
    });
  }
  function mountLevelReview(root, Z, cid, id) {
    const lv = levelOfId(cid, id);
    const c = course(cid);
    const cfg = {
      title: `Level ${lv ? lv.n : ''} review`, sub: `${c ? c.name : cid}${lv ? ', ' + lv.name : ''}`, over: `${c ? c.name : cid} · Level ${lv ? lv.n : ''}`,
      heading: lv ? `Review: ${lv.name}` : 'Level review', track: trackOf(cid), perItem: 1.5,
      lede: 'Mixed problems from every lesson of the level, in no particular order. Each right answer adds mastery points to its skills; each miss joins your redo queue.',
      facts: [['target', 'Right first time earns mastery points and 15 XP each.'], ['replay', 'Misses come back in 7 days, then 30.']],
      tag: (it) => { const n = skillNames(); return (it.skills || []).map(s => n[s] || s).join(', '); },
      emptyTitle: 'Not yet written', emptyText: 'This level review has not been written yet. Use the course map to pick another item.',
      doneTitle: 'Level review done', setTitle: 'Level review',
      load: () => C().review(cid, id).then(D => { cfg.timed = timedOf(D && D.timed); cfg.pass = D && Number(D.pass) > 0 && Number(D.pass) <= 1 ? Number(D.pass) : ZQ.prereq ? ZQ.prereq.PASS : 0.8; return D; }).then(D => (D && Array.isArray(D.items) ? D.items.map((it, i) => Object.assign({}, it, { skills: it.skills || [], ref: { course: cid, lesson: id, item: it.id || 'q' + i }, source: `Item ${i + 1}` })) : [])),
      record: (items, res, seconds) => {
        const results = items.map((it, j) => res[j] ? resultRow(res[j]) : { id: it.id, ok: false, difficulty: it.difficulty || 3, skills: it.skills || [], ref: it.ref });
        const o = S().reviewFinished({ course: cid, id, results, items: items.length, seconds, pass: cfg.pass }) || {};
        const wrong = results.filter(r => !r.ok).length;
        return { badges: [[`+${o.xp || 0}`, 'XP'], [`+${o.mp || 0}`, 'mastery points'], [wrong, 'to the redo queue']],
          note: wrong ? `${plural(wrong, 'problem joins', 'problems join')} your redo queue, back in 7 days.` : 'Nothing to redo. Every problem was right first time.' };
      },
    };
    return setPage(root, Z, cfg);
  }
  /* Test-out (ENGINE-BACKLOG 485): up to 6 items from a level's review, seeded and shuffled, passed at the review's pass share.
     Route #testout/<course>/<n>. A pass records the level met; a miss lists the lessons to revisit and waits 24 hours. */
  function mountTestout(root, Z, cid, n) {
    const P = ZQ.prereq, lv = levelOf(cid, n), key = P ? P.keyOfLevel(cid, +n) : `${cid}/L${n}`;
    const c = course(cid);
    let need = 1, bySkill = {}, shownIds = [];
    const hashOf = (str) => { let h = 2166136261; for (const ch of String(str)) { h ^= ch.charCodeAt(0); h = Math.imul(h, 16777619); } return h >>> 0; };
    const rngOf = (seed) => { let a = seed >>> 0; return () => { a = (a + 0x6D2B79F5) >>> 0; let t = a; t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; };
    const cfg = {
      title: `Test out of level ${n}`, sub: `${c ? c.name : cid}${lv ? ', ' + lv.name : ''}`, over: `${c ? c.name : cid} · Level ${n} · Test out`,
      heading: `Test out: ${lv ? lv.name : 'level ' + n}`, track: trackOf(cid), perItem: 1.5,
      lede: 'A short check drawn from the level review. Pass it and the level counts as met, so what depends on it opens. Miss it and you can try again after 24 hours.',
      facts: [['target', 'No hints and one try each. It does not earn mastery points or add to your redo queue.']],
      tag: (it) => { const nm = skillNames(); return (it.skills || []).map(sk => nm[sk] || sk).join(', '); },
      emptyTitle: 'Not available', emptyText: 'This level cannot be tested out of right now.',
      doneTitle: 'Test-out done', setTitle: 'Test out',
      load: async () => {
        if (!P || !lv) { cfg.emptyText = 'This level is not in the course map.'; return []; }
        if (P.levelMet(cid, +n)) { cfg.emptyTitle = 'Already met'; cfg.emptyText = 'This level already counts as met. There is nothing to test out of.'; return []; }
        const t = P.testOutFacts(cid, lv);
        if (!t.written) { cfg.emptyText = 'This level has no written review to test out with. Finish its lessons instead.'; return []; }
        if (t.nextAt) { cfg.emptyTitle = 'Try again later'; cfg.emptyText = `You can retake this test out in ${Math.max(1, Math.ceil((t.nextAt - Date.now()) / 3600e3))} hours. Use the time to revisit the lessons you missed.`; return []; }
        const D = await C().review(cid, lv.review);
        const all = D && Array.isArray(D.items) ? D.items : [];
        const pass = Number(D && D.pass) > 0 && Number(D.pass) <= 1 ? Number(D.pass) : P.PASS;
        /* seeded by attempt; items shown on an earlier attempt come last, so a retake is a new paper while the review has enough items */
        const rng = rngOf(hashOf(`${key}/${t.tries}`)), seenBefore = new Set(t.seen), idOf = (it, i) => it.id || 'q' + i;
        const picked = all.map((it, i) => ({ it, i, old: seenBefore.has(idOf(it, i)) ? 1 : 0, k: rng() })).sort((a, b) => a.old - b.old || a.k - b.k).slice(0, P.TESTOUT_N).sort((a, b) => a.i - b.i);
        shownIds = picked.map(o => idOf(o.it, o.i));
        const pickedItems = picked.map(o => o.it);
        need = Math.max(1, Math.ceil(pickedItems.length * pass - 1e-9));
        /* lessons by skill, for the links on a miss */
        await Promise.all((lv.lessons || []).filter(id => C().exists(cid, id) !== false).map(id => C().lesson(cid, id).then(L => { (L && L.skills || []).forEach(sk => { if (!bySkill[sk]) bySkill[sk] = { id, title: L.title || id }; }); }).catch(() => null)));
        return pickedItems.map((it, i) => Object.assign({}, it, { skills: it.skills || [], ref: { course: cid, lesson: lv.review, item: it.id || 'q' + i }, source: `Item ${i + 1}` }));
      },
      record: (items, res) => {
        const ok = items.map((it, j) => !!(res[j] && res[j].ok));
        /* the skill floor (met rule 2): every skill the drawn items carry needs P.SKILL_FLOOR of its items right */
        const drawn = {};
        items.forEach((it, j) => (it.skills || []).forEach(sk => { const b = drawn[sk] || (drawn[sk] = [0, 0]); b[1]++; if (ok[j]) b[0]++; }));
        const low = S().floorGaps(drawn, Object.keys(drawn), P.SKILL_FLOOR), nm = skillNames();
        const right = ok.filter(Boolean).length, passed = right >= need && !low.length;
        const missed = items.filter((it, j) => !ok[j]);
        const where = (it) => (it.skills || []).map(sk => bySkill[sk]).find(Boolean) || ((lv.lessons || [])[0] ? { id: lv.lessons[0], title: 'the first lesson' } : null);
        S().prereq.testout({ key, score: right, items: items.length, passed, missed: missed.map(it => it.id).filter(Boolean), seen: shownIds });
        const links = [...new Map(missed.map(where).filter(Boolean).map(l => [l.id, l])).values()].map(l => `<a href="#lesson/${Z.esc(cid)}/${Z.esc(l.id)}">${Z.esc(l.title)}</a>`);
        return { badges: [[`${right} of ${items.length}`, 'right'], [need, 'needed to pass']],
          lines: items.map((it, j) => (ok[j] ? '' : (where(it) ? `Revisit ${where(it).title}` : ''))),
          note: passed && P && lv && P.perfNeeded(cid, lv) && !P.perfPassed(cid, lv) ? `Test passed, but level ${n} has a performance task (in its homework or review) that is not passed yet. It counts as met once you pass it.`
            : passed ? `Level ${n} now counts as met. What depends on it is open.`
            : right >= need ? `Not passed: enough right, but too few on ${low.map(sk => nm[sk] || sk).join(', ')}. You can retake it after 24 hours.${links.length ? ' Revisit: ' + links.join(', ') + '.' : ''}`
            : `Not passed. You can retake it after 24 hours.${links.length ? ' Revisit: ' + links.join(', ') + '.' : ''}` };
      },
    };
    return setPage(root, Z, cfg);
  }
  ZQ.screen({ id: 'testout', title: 'Test out', group: 'Assessment', hidden: true, shell: false, render: (root, Z, params = []) => mountTestout(root, Z, params[0], params[1]) });

  /* Full-screen takeover for set routes that share the shell's screen id */
  const takeover = (Z) => { const app = document.getElementById('app'); app.innerHTML = ''; app.className = 'screen-set'; return app; };

  ZQ.screen({
    id: 'review', title: 'Review', group: 'App', shell: true, tab: 'review',
    render(root, Z, params = []) {
      if (params.length >= 2) {
        const host = takeover(Z);
        const off = Z.lockedFor && Z.lockedFor(host, params[0], params[1], `review/${params[0]}/${params[1]}`);   // prerequisite gating (ENGINE-BACKLOG 483)
        return off || mountLevelReview(host, Z, params[0], params[1]);
      }
      return hub(root, Z);
    },
  });
  ZQ.screen({ id: 'redo', title: 'Redo session', group: 'Assessment', shell: false, render: (root, Z) => mountRedo(root, Z) });
  ZQ.screen({ id: 'bank', title: 'Interview practice', group: 'Assessment', shell: false, render: (root, Z) => mountBank(root, Z) });
  ZQ.screen({ id: 'practice', title: 'Practice set', group: 'Assessment', shell: false, render: (root, Z, params = []) => mountPractice(root, Z, params) });

  /* =====================================================================================
     HOMEWORK SET
     ===================================================================================== */
  function mountHomework(root, Z, params) {
    const I = Z.icon, esc = Z.esc;
    let [cid, id] = params;
    if (!cid || !id) {
      const open = S().summary().homeworkOpen[0];
      if (open) { location.replace(`#homework/${open.id}`); return null; }
      root.innerHTML = `<div class="hw"><main class="hw-frame"><div class="hw-scroll"><div class="hw-col"><section class="hw-intro"><h1 class="t-lesson-title">No homework open</h1>
        <p class="t-prose">Homework is set when you finish the last lesson of a level.</p><a class="btn" href="#review">Back to Review</a></section></div></div></main></div>`;
      return null;
    }
    const key = `${cid}/${id}`;
    const lockOff = Z.lockedFor && Z.lockedFor(root, cid, id, `homework/${cid}/${id}`);   // prerequisite gating (ENGINE-BACKLOG 483)
    if (lockOff) return lockOff;
    const c = course(cid), lv = levelOfId(cid, id) || { n: id.split('-')[1], name: '' };
    const perfGates = (() => { try { return !!(ZQ.prereq && ZQ.prereq.perfNeeded(cid, lv)); } catch { return false; } })();   // 549: only a rule-matched level's task gates met; any other is practice
    let alive = true, view = 'intro', handles = [], items = [], doc = null, t0 = Date.now();
    const rec = () => S().homework[key] || null;
    const stored = () => store.get(`hw.result.${key}`, null);

    root.innerHTML = `
      <div class="hw" data-track="${esc(trackOf(cid))}">
        <header class="hw-top">
          <div class="hw-left">
            <button type="button" class="icon-btn hw-close" aria-label="Close homework. Your answers are saved.">${I('close')}</button>
            <div class="hw-ttl"><span class="hw-ttl-a">Homework ${esc(lv.n)}<span class="hw-ttl-sep"> · </span><span class="hw-ttl-n">${esc(lv.name || '')}</span></span><span class="t-caption muted hw-ttl-b">${esc(c ? c.name : cid)}, Level ${esc(lv.n)}</span></div>
          </div>
          <nav class="hw-dots" aria-label="Items"></nav>
          <div class="hw-due"></div>
        </header>
        <main class="hw-frame">
          <div class="hw-scroll"><div class="hw-col" tabindex="-1"><div class="hw-page" data-page><p class="t-caption muted">Loading the homework</p></div><div class="hw-items" data-items></div></div></div>
          <footer class="hw-foot"><p class="t-caption muted hw-save" aria-live="polite"></p><div class="hw-actions"></div></footer>
        </main>
      </div>`;
    const $ = (s) => root.querySelector(s);
    const page = $('[data-page]'), itemsEl = $('[data-items]'), dots = $('.hw-dots'), acts = $('.hw-actions'), save = $('.hw-save'), scroller = $('.hw-scroll'), dueEl = $('.hw-due');
    let saveT = 0;
    const saved = () => { save.textContent = 'Saved'; clearTimeout(saveT); saveT = setTimeout(() => { save.textContent = ''; }, 1600); };
    const setActions = (html) => { acts.innerHTML = html; acts.classList.toggle('one', acts.children.length === 1); };

    const isLong = (it) => it.kind === 'longform' || (it.widget && it.widget.kind === 'longform');
    const marksOf = (it) => (isLong(it) ? (it.rubric || (it.widget || {}).rubric || []).reduce((a, r) => a + (+r.points || 0), 0) || 10 : it.difficulty || 3);
    const total = () => items.reduce((a, it) => a + marksOf(it), 0);
    const values = () => handles.map(h => (h ? h.value() : null));
    const answered = (j) => { const h = handles[j]; if (!h) return false; const v = h.value(); return isLong(items[j]) ? !!(v && v.marked) : (h.ready ? !!h.ready() : !empty(v)); };
    const result = () => (rec() && rec().submitted ? stored() : null);

    const drawDue = () => {
      const r = rec(), R = result();
      const [ic, a, b] = r && r.submitted ? ['check', `Marked ${esc(dayDate(r.submittedAt || Date.now()))}`, R ? `${R.pct}%` : `${r.score} of ${r.items} right`]
        : r ? ['clock', esc(whenDue(r.due)), r.due < Date.now() ? 'Overdue' : `${plural(Math.max(0, daysFrom(r.due)), 'day', 'days')} left`]
        : ['lock', 'Not set yet', 'You are starting early'];
      dueEl.innerHTML = `<span class="hw-due-a">${I(ic, 'xs')}<span>${a}</span></span><span class="t-caption muted">${b}</span>`;
    };
    const drawDots = () => {
      const R = result();
      dots.innerHTML = items.map((it, j) => {
        const r = R && R.items[j];
        const cls = r ? (r.ok ? 'ok' : 'bad') : answered(j) ? 'ans' : '';
        const state = r ? (r.ok ? 'right' : 'not right') : answered(j) ? 'answered' : 'not answered';
        return `<button type="button" class="hw-dot" data-view="${j}" aria-label="Item ${j + 1}, ${state}" ${view === j ? 'aria-current="step"' : ''}><i class="${cls} ${view === j ? 'cur' : ''}"></i></button>`;
      }).join('');
    };
    const persist = () => {
      if (rec() && rec().submitted) return;
      const v = { values: values(), at: Date.now() };
      session.hw[key] = v; store.set(`hw.draft.${key}`, v); saved(); drawDots();
    };

    /* ---------- Views ---------- */
    const intro = () => {
      const r = rec();
      page.innerHTML = `<section class="hw-intro">
        <span class="t-overline hw-deep">Homework ${esc(lv.n)} · ${esc(c ? c.name : cid)}, Level ${esc(lv.n)}</span>
        <h1 class="t-lesson-title">${esc(lv.name || 'Homework')}</h1>
        <p class="t-prose">${r ? `${plural(items.length, 'problem', 'problems')} on the level you just finished. Work in any order before the due date.`
          : `${plural(items.length, 'problem', 'problems')} on this level. It is set when you finish the level, but you can start it now and submit when you are ready.`}</p>
        <ul class="hw-facts">
          <li>${I('clock', 'sm')}<span>${r ? `${esc(whenDue(r.due))}.` : `Due ${doc.dueDays || 7} days after it is set.`} About ${Math.round(items.length * 6)} minutes.</span></li>
          <li>${I('lock', 'sm')}<span>No hints, and nothing is marked until you submit. You can change answers until then.</span></li>
          <li>${I('replay', 'sm')}<span>Items you miss join your redo queue: back after 7 days and again after 30.</span></li>
          ${items.some(isLong) ? `<li>${I('edit', 'sm')}<span>${(() => { const w = items.map((it, j) => (isLong(it) ? j + 1 : null)).filter(Boolean); return w.length === 1 ? `Item ${w[0]} is written. You mark it yourself` : `Items ${listAnd(w.map(String))} are written. You mark them yourself`; })()} against a model answer and a 10-point rubric.</span></li>` : ''}
          ${items.some(it => it.performance) ? `<li>${I('flag', 'sm')}<span>${(() => { const w = items.map((it, j) => (it.performance ? j + 1 : null)).filter(Boolean); return `${w.length === 1 ? `Item ${w[0]} is` : `Items ${listAnd(w.map(String))} are`} ${perfGates ? `the level's performance task. The level counts as met once you pass ${w.length === 1 ? 'it' : 'one'}.` : `${w.length === 1 ? 'a performance task' : 'performance tasks'} for practice. ${w.length === 1 ? 'It does' : 'They do'} not count towards the level being met.`}`; })()}</span></li>` : ''}
        </ul>
        <ol class="hw-ov">${items.map((it, j) => `<li><span class="hw-ov-n tnum">${j + 1}</span><span class="t-body">${esc(it.title || 'Item ' + (j + 1))}${it.performance ? ' <span class="t-caption secondary hw-perf">Performance task</span>' : ''}</span>${pips(it.difficulty || 3)}<span class="t-caption muted tnum hw-ov-m">${plural(marksOf(it), 'mark', 'marks')}</span></li>`).join('')}</ol>
        <p class="t-caption secondary">${total()} marks in all. Each item is worth its difficulty; a written item is worth 10.</p>
      </section>`;
      setActions(`<button type="button" class="btn hw-primary" data-nav="0">${values().some(v => !empty(v)) ? 'Continue' : 'Start'}</button>`);
    };
    const itemView = (j) => {
      itemsEl.querySelectorAll('.hw-item').forEach((n, k) => { n.hidden = k !== j; });
      const it = items[j], h = handles[j];
      const markBtn = itemsEl.querySelectorAll('.hw-item')[j].querySelector('[data-mark-row]');
      if (markBtn) markBtn.hidden = !h || !!(h.value() || {}).marked || !!result();
      const R = result();
      const last = j === items.length - 1;
      if (R) setActions(`<button type="button" class="btn secondary hw-sec" data-nav="${j === 0 ? 'summary' : j - 1}">${j === 0 ? 'Results' : 'Previous'}</button><button type="button" class="btn hw-primary" data-nav="${last ? 'summary' : j + 1}">${last ? 'Results' : 'Next item'}</button>`);
      else setActions(`<button type="button" class="btn secondary hw-sec" data-nav="${j === 0 ? 'intro' : j - 1}">${j === 0 ? 'Back' : 'Previous'}</button><button type="button" class="btn hw-primary" data-nav="${last ? 'review' : j + 1}">${last ? 'Review and submit' : 'Next'}</button>`);
      void it;
    };
    const reviewView = () => {
      const missing = items.map((it, j) => (answered(j) ? null : j + 1)).filter(Boolean);
      const status = (it, j) => (isLong(it) ? (answered(j) ? `Self-marked ${(handles[j].value() || {}).score || 0} of ${marksOf(it)}` : (handles[j] && (handles[j].value() || {}).text) ? 'Written, not marked yet' : 'No answer') : answered(j) ? 'Answered' : 'No answer');
      page.innerHTML = `<section class="hw-rev">
        <span class="t-overline hw-deep">Homework ${esc(lv.n)} · ${plural(items.length, 'item', 'items')}</span>
        <h1 class="t-lesson-title">Ready to submit?</h1>
        <p class="t-prose">Nothing is marked until you submit, and you cannot change answers afterwards.${rec() ? ` You have until ${esc(dayDate(rec().due))}.` : ''}</p>
        <ol class="hw-rl">${items.map((it, j) => `<li><button type="button" class="hw-rl-r ${answered(j) ? 'is-on' : ''}" data-nav="${j}">
          <span class="hw-ov-n tnum">${j + 1}</span><span class="hw-rl-t"><span class="t-body">${esc(it.title || 'Item ' + (j + 1))}</span><span class="t-caption ${answered(j) ? 'secondary' : 'hw-miss'}">${status(it, j)}</span></span>${I('chevronR', 'sm rv-chev')}</button></li>`).join('')}</ol>
        ${missing.length ? `<p class="hw-warn t-body">${I('flag', 'sm')}<span>${missing.length === 1 ? `Item ${missing[0]} has` : `Items ${listAnd(missing.map(String))} have`} no answer yet. ${missing.length === 1 ? 'It' : 'They'} will score 0 and join your redo queue.</span></p>` : ''}
      </section>`;
      setActions(`<button type="button" class="btn secondary hw-sec" data-nav="${items.length - 1}">Back</button><button type="button" class="btn hw-primary" data-submit>Submit homework</button>`);
    };
    const summaryView = (fresh) => {
      const r = rec(), R = result();
      const right = R ? R.right : r.score, n = R ? R.items.length : r.items;
      page.innerHTML = `<section class="hw-sum">
        <span class="t-overline hw-deep">Homework ${esc(lv.n)} · ${esc(lv.name || '')}</span>
        <h1 class="t-complete">Homework marked</h1>
        <div class="hw-score-big"><span class="t-stat tnum" data-count>${R ? (fresh && !Z.reducedMotion() ? 0 : R.marks) : right}</span><span class="t-h2 secondary">${R ? `of ${R.total} marks · ${R.pct}%` : `of ${n} right`}</span></div>
        <div class="hw-badges">
          <div class="hw-badge"><span class="t-h1 tnum">${right} of ${n}</span><span class="t-caption muted">items right</span></div>
          <div class="hw-badge"><span class="t-h1 tnum hw-xp">${Z.spark(true)}+${R ? R.xp : 0}</span><span class="t-caption muted">XP: 50, plus 5 for each right item</span></div>
          <div class="hw-badge"><span class="t-h1 tnum">${I('target', 'sm')}+${R ? R.mp : 0}</span><span class="t-caption muted">mastery points for first-try answers</span></div>
        </div>
        ${R ? `<div class="hw-redo">${R.wrong.length
          ? `${I('replay', 'sm')}<span><b>To your redo queue: ${R.wrong.length === 1 ? 'item' : 'items'} ${listAnd(R.wrong.map(String))}.</b> ${R.wrong.length === 1 ? 'It comes' : 'They come'} back in 7 days and again after 30.</span>`
          : `${I('check', 'sm')}<span><b>Nothing to redo.</b> Every item was right first time.</span>`}</div>
        <h2 class="t-h2 hw-res-h">Item by item</h2>
        <ol class="hw-res">${items.map((it, j) => { const x = R.items[j] || {}; return `<li><button type="button" class="hw-res-r ${x.ok ? 'ok' : 'no'}" data-nav="${j}">
          <span class="hw-res-ic" aria-hidden="true">${I(x.ok ? 'check' : 'cross')}</span>
          <span class="hw-rl-t"><span class="t-body"><span class="tnum">${j + 1}.</span> ${esc(it.title || 'Item ' + (j + 1))}</span><span class="t-caption secondary">${it.performance ? `Performance task ${x.ok ? 'passed' : 'not passed'}. ` : ''}${isLong(it) ? `Self-marked ${x.got} of ${marksOf(it)}` : x.ok ? 'Right' : Array.isArray(x.parts) && x.answered ? `${x.parts.filter(q => q.ok).length} of ${x.parts.length} parts right` : x.answered ? 'Not right' : 'No answer'}${x.ok ? '' : ' · to redo'}</span></span>
          <span class="t-label tnum hw-res-m">${x.got} of ${marksOf(it)}</span>${I('chevronR', 'sm rv-chev')}</button></li>`; }).join('')}</ol>` : ''}
      </section>`;
      setActions(`<button type="button" class="btn hw-primary" data-back>Back to Review</button>`);
      if (fresh && R) {
        Z.sound('complete');
        Z.countUp(page.querySelector('[data-count]'), R.marks, 900);
        page.querySelectorAll('.hw-badge').forEach((b, k) => { b.style.animationDelay = (300 + k * 80) + 'ms'; b.classList.add('hw-in'); });
      }
    };
    const go = (v, fresh) => {
      if (!alive) return;
      if (v === 'review' && result()) v = 'summary';
      if (v === 'summary' && !(rec() && rec().submitted)) v = 'review';
      view = v;
      const isItem = typeof v === 'number';
      page.hidden = isItem; itemsEl.hidden = !isItem;
      if (v === 'intro') intro(); else if (v === 'review') reviewView(); else if (v === 'summary') summaryView(fresh); else itemView(v);
      root.querySelector('.hw').classList.toggle('is-sum', v === 'summary');
      drawDue(); drawDots();
      scroller.scrollTop = 0;
      Z.mathify(page);
    };

    /* ---------- Submit ---------- */
    const submit = async () => {
      const graded = [];
      for (let j = 0; j < handles.length; j++) {
        const h = handles[j], it = items[j];
        let r = { ok: false, key: null };
        if (h && answered(j)) { try { r = await h.check(); } catch (e) { console.error(e); } }
        if (r && r.pending) r = { ok: false, key: null };
        const got = isLong(it) ? ((r.detail && r.detail.score) || 0) : r.ok ? marksOf(it) : typeof r.credit === 'number' ? Math.round(r.credit * marksOf(it) * 100) / 100 : 0;   // parts: the share of parts right
        graded.push({ r, got, answered: answered(j) });
        if (h) { h.step.lock(); if (answered(j)) h.step.mark(Object.assign({}, r, { final: true })); }
      }
      const results = items.map((it, j) => ({ id: it.id, ok: !!graded[j].r.ok, difficulty: it.difficulty || 3, skills: it.skills || [], how: S().provenance(it), ...(it.performance ? { perf: it.performance } : {}), ref: { course: cid, lesson: id, item: it.id } }));
      const selfMarks = {};
      items.forEach((it, j) => { if (isLong(it)) { const v = handles[j] ? handles[j].value() : {}; selfMarks[it.id] = { score: (v && v.score) || 0, ticks: (v && v.ticks) || [], of: marksOf(it) }; } });
      if (!rec()) S().homeworkAssigned({ course: cid, level: lv.n, dueDays: doc.dueDays || 7 });
      const out = S().homeworkSubmitted({ course: cid, level: lv.n, id, results, items: items.length, selfMarks, seconds: Math.round((Date.now() - t0) / 1000) }) || {};
      const marks = graded.reduce((a, g) => a + g.got, 0);
      const R = { at: Date.now(), marks, total: total(), pct: Math.round(marks / Math.max(1, total()) * 100), right: results.filter(x => x.ok).length, xp: out.xp || 0, mp: out.mp || 0,
        wrong: results.map((x, j) => (x.ok ? null : j + 1)).filter(Boolean),
        items: graded.map((g, j) => ({ id: items[j].id, ok: !!g.r.ok, got: g.got, answered: g.answered, key: g.r.key ?? null, value: handles[j] ? handles[j].value() : null,
          ...(Array.isArray(g.r.parts) ? { credit: g.r.credit, parts: g.r.parts, line: g.r.line || null } : {}) })) };
      store.set(`hw.result.${key}`, R);
      store.set(`hw.draft.${key}`, null); delete session.hw[key];
      itemsEl.querySelectorAll('[data-mark-row]').forEach(n => { n.hidden = true; });
      itemsEl.querySelectorAll('[data-verdict]').forEach((n, j) => { n.innerHTML = verdictHTML(j); n.hidden = false; Z.mathify(n); });
      go('summary', true);
    };
    const verdictHTML = (j) => {
      const R = result(); if (!R) return '';
      const x = R.items[j], it = items[j];
      const fb = it.feedback || {};
      const parted = Array.isArray(it.parts) && Array.isArray(x.parts);
      const line = parted ? (x.line || '') : x.ok ? fb.correct : (x.key != null && fb.byKey && fb.byKey[x.key]) || fb.generic || '';
      const head = (it.performance ? `Performance task ${x.ok ? 'passed' : 'not passed'}. ` : '') + (isLong(it) ? `Self-marked ${x.got} of ${marksOf(it)}` : x.ok ? 'Right' : parted && x.answered ? `${x.parts.filter(q => q.ok).length} of ${x.parts.length} parts right` : x.answered ? 'Not right' : 'No answer');
      return `<div class="rv-chip ${x.ok ? 'is-ok' : 'is-no'} hw-verdict"><span class="rv-chip-ic" aria-hidden="true">${I(x.ok ? 'check' : 'cross')}</span>
        <span class="rv-chip-tx"><span class="rv-chip-h"><b>${head}</b></span><span>${x.got} of ${marksOf(it)} marks.${x.ok ? '' : ' Back in your redo queue in 7 days, then 30.'}</span></span></div>
        ${line ? `<p class="t-body hw-why">${md(line)}</p>` : ''}
        ${(it.explain && it.explain.text ? [it.explain.text] : []).concat(Array.isArray(it.parts) ? it.parts.map(q => (q.explain && q.explain.text) || '').filter(Boolean) : []).map(t => `<p class="t-body hw-why">${md(t)}</p>`).join('')}`;
    };
    const confirmSubmit = () => {
      const box = Z.h(`<div class="hw-conf"><h2 class="t-sheet-title">Submit Homework ${esc(lv.n)}?</h2>
        <p class="t-body secondary">You cannot change answers after this. Items you miss join your redo queue for 7 days, then 30.</p>
        <div class="hw-conf-a"><button type="button" class="btn secondary" data-close>Keep working</button><button type="button" class="btn" data-yes>Submit</button></div></div>`);
      const close = Z.sheet(box, { modal: true, label: 'Submit homework' });
      box.querySelector('[data-yes]').addEventListener('click', () => { close(); submit().catch(e => console.error(e)); });
    };

    /* ---------- Load and mount every item once ---------- */
    C().homework(cid, id).then((D) => {
      if (!alive) return;
      if (!D || !Array.isArray(D.items)) {
        page.innerHTML = `<section class="hw-intro"><span class="t-overline hw-deep">${esc(c ? c.name : cid)}</span><h1 class="t-lesson-title">Not yet written</h1><p class="t-prose">This homework has not been written yet.</p></section>`;
        setActions('<button type="button" class="btn hw-primary" data-back>Back to Review</button>');
        return;
      }
      doc = D;
      items = D.items.map((it, i) => Object.assign({}, it, { skills: it.skills || [], ref: { course: cid, lesson: id, item: it.id || 'q' + i } }));
      const R = result();
      const draft = session.hw[key] || store.get(`hw.draft.${key}`, null);
      items.forEach((it, j) => {
        const wrap = Z.h(`<section class="hw-item" data-kind="${esc(isLong(it) ? 'longform' : (it.widget || {}).kind || '')}" hidden>
          <div class="hw-meta"><span class="t-overline hw-deep">Item ${j + 1} of ${items.length}${it.title ? ' · ' + esc(it.title) : ''}${it.performance ? (perfGates ? ' · Performance task, needed for the level' : ' · Performance task, practice only') : ''}</span><span class="hw-meta-r">${pips(it.difficulty || 3)}<span class="t-caption muted tnum">${plural(marksOf(it), 'mark', 'marks')}</span></span></div>
          <div class="hw-w" data-host></div>
          ${isLong(it) ? `<div class="hw-mark-row" data-mark-row><button type="button" class="btn secondary" data-mark="${j}">Mark my answer</button><span class="t-caption muted">Shows the model answer and the rubric. Your working then locks.</span></div>` : '<p class="t-caption muted hw-note" data-note>No feedback until you submit.</p>'}
          <div data-verdict hidden></div>
        </section>`);
        itemsEl.append(wrap);
        let h = null;
        try { h = ZQ.player.renderItem(it, wrap.querySelector('[data-host]'), { mode: 'exam', key: `hw-${key}-${j}` }); } catch (e) { console.error(e); }
        handles[j] = h;
        const v = R ? (R.items[j] || {}).value : draft && draft.values ? draft.values[j] : null;
        if (h && !empty(v)) { try { h.set(v); } catch (e) { console.error(e); } }
        if (h) h.onChange(() => persist());
        if (R && h) {
          const x = R.items[j] || {};
          h.step.lock();
          if (h.restore && Array.isArray(x.parts)) h.restore(x.parts);   // parts: each part's own verdict
          if (x.answered) h.step.mark({ ok: !!x.ok, key: x.key, final: true });
          const vd = wrap.querySelector('[data-verdict]'); vd.innerHTML = verdictHTML(j); vd.hidden = false;
          const nt = wrap.querySelector('[data-note]'); if (nt) nt.hidden = true;
        }
      });
      Z.mathify(itemsEl);
      go(R ? 'summary' : 'intro');
    }).catch(e => { console.error(e); page.innerHTML = `<p class="t-body">This homework could not be loaded: ${esc(e.message)}</p>`; });

    /* ---------- Events ---------- */
    const onClick = (e) => {
      const t = e.target;
      if (t.closest('.hw-close') || t.closest('[data-back]')) { Z.go('review'); return; }
      const nav = t.closest('[data-nav], [data-view]');
      if (nav) { const v = nav.dataset.nav ?? nav.dataset.view; go(/^\d+$/.test(v) ? +v : v); return; }
      if (t.closest('[data-submit]')) { confirmSubmit(); return; }
      const mk = t.closest('[data-mark]');
      if (mk) {
        const j = +mk.dataset.mark, h = handles[j];
        if (!h) return;
        const v = h.value() || {};
        if (!String(v.text || '').trim() && !(h.ready && h.ready())) { Z.toast('Write your working first. Then mark it against the model answer.'); return; }
        h.check().then(() => { mk.closest('[data-mark-row]').hidden = true; persist(); Z.mathify(itemsEl); }).catch(err => console.error(err));
      }
    };
    root.addEventListener('click', onClick);
    window.ZQHomework = { handles: () => handles.slice(), items: () => items.slice(), go, submit };
    /* Test hook (docs/PLAN.md 7): kind 'loading', 'start' (the intro), 'item' (screenIndex is the item), 'submit' (the
       review page), then 'done' once marked. check() grades the shown item without marking it (a long-form item's first
       check opens its self-marking and returns { pending }); continue() moves on and submits after the last item. */
    const hook = {
      current: () => {
        const R = result();
        if (R) return { kind: 'done', phase: 'homework', state: 'done', screenIndex: -1, total: items.length, right: R.right, marks: R.marks, of: R.total };
        if (!doc) return { kind: 'loading', phase: 'homework', state: 'read', screenIndex: -1, total: 0 };
        if (typeof view === 'number') { const hp = handles[view]; return { kind: 'item', phase: 'homework', state: answered(view) ? 'engaged' : 'idle', screenIndex: view, total: items.length, ...(hp && hp.partCount && hp.partCount() > 1 ? { part: hp.part().index, parts: hp.partCount() } : {}) }; }
        return { kind: view === 'intro' ? 'start' : 'submit', phase: 'homework', state: 'read', screenIndex: -1, total: items.length };
      },
      answerCorrect: () => { const h = typeof view === 'number' && handles[view]; if (!h) return false; const ok = h.answerCorrect(); persist(); return ok; },
      check: async () => {
        const h = typeof view === 'number' && handles[view]; if (!h) return null;
        const r = await h.step.grade();
        if (r && r.pending) { const row = itemsEl.querySelectorAll('.hw-item')[view].querySelector('[data-mark-row]'); if (row) row.hidden = true; persist(); }
        return r;
      },
      continue: async () => {
        if (result()) return;
        if (view === 'intro') go(0);
        else if (typeof view === 'number' && handles[view] && handles[view].more && handles[view].more() && handles[view].advance()) persist();   // the next part of this item
        else if (typeof view === 'number' && view < items.length - 1) go(view + 1);
        else await submit();
      },
    };
    window.ZQ.test = hook;
    return () => {
      alive = false;
      if (window.ZQ.test === hook) delete window.ZQ.test;
      if (window.ZQHomework && window.ZQHomework.go === go) delete window.ZQHomework;
      if (handles.length && !(rec() && rec().submitted)) { try { persist(); } catch (e) { console.error(e); } }
      root.removeEventListener('click', onClick); clearTimeout(saveT);
      handles.forEach(h => { try { h && h.destroy(); } catch (e) { console.error(e); } });
    };
  }

  ZQ.screen({ id: 'homework', title: 'Homework', group: 'Assessment', shell: false, render: (root, Z, params = []) => mountHomework(root, Z, params) });
})();
