/* Course map (spec 7.4; progress and celebration motion 4.6, 4.7; glyphs 3). Route #course/<courseId>; with no id it
   opens the learner's current course (the open lesson's course, else the first unfinished course with a written lesson).
   Desktop: course card on the left, 575px path column on the right. Mobile: the header stacks above the path.
   Nodes are tilted pucks on a sine serpentine with no connector lines, built from ZQ.content.courseLessons(id): each
   level's lessons, then its review, then its homework. Node states come from ZQ.state: done, mastered (quiz at 80%),
   current (the first written lesson not done and not locked), upcoming (after it: the card offers "Jump ahead"),
   locked (prerequisites unmet, ENGINE-BACKLOG 484: a lock on the puck and a card that says what is missing), and not written (grey, no launch). Tapping a node opens a card anchored to the bottom of the path
   column (desktop) or a bottom sheet (mobile).
   Hand-offs: before leaving for a lesson the map (and Today) set window.ZQLaunch = { course, id, kind, wasDone,
   qualifiedBefore, at }. The player returns to #course/<course>; if the launched lesson is now done the map draws it
   as it was, then plays the completion (fill, check, halo to the next node) and, when the day has just qualified,
   the streak toast. window.ZQFlash ('streak' or 'done'), if anything sets it, is honoured too. */
(function () {
  'use strict';

  /* Serpentine: a sine sampled every quarter period. Each node steps 13.5% of the column and
     centres swing between 20% and 47% of it (spec: about 13% per node, between about 20% and 50%). */
  const xAt = (g) => 0.335 + 0.135 * Math.sin(g * Math.PI / 2);
  const DEFAULT_MIN = 12; // minutes shown until the lesson file says otherwise

  /* Puck geometry in a 100-unit-wide box: elliptical face 2.1:1, side band 12% of the width. */
  const RY = 23.81, BAND = 12, VH = 59.62;

  /* One 'state' listener for the module; the mounted screen sets onState and clears it on leave (core.js has no off) */
  let onState = null;
  ZQ.on('state', (e) => { if (onState) onState(e); });

  const lessonMeta = {}; // course/lesson -> { screens, minutes } once the lesson file has loaded
  const probed = new Set();

  /* ---------- Where the learner is (the same rule as Today and Learn) ---------- */
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
    if (c) return c.id;
    const all = C.courses();
    const f = all.find(x => x.stage === start) || all[0];
    return f ? f.id : null;
  };
  const pctOf = (a) => {
    if (!a) return 0;
    const s = Number(a.score) || 0, n = Number(a.items) || 0;
    if (n > 0 && s <= n && s > 1) return Math.round(s / n * 100);
    return Math.round(s <= 1 ? s * 100 : s);
  };

  ZQ.screen({
    id: 'course', title: 'Course map', group: 'App', shell: true, tab: 'learn',
    render(root, Z, params) {
      const C = Z.content;
      const asked = params && params[0];
      const cid = asked && C.course(asked) ? asked : currentCourse(Z, Z.state.summary());
      if (!cid || (asked && !C.course(asked))) {
        root.innerHTML = `<div class="zc-missing card pad"><h1 class="t-h2">That course is not in the curriculum</h1>
          <p class="t-body secondary">The link may be out of date.</p><a class="btn secondary" href="#learn">Back to Learn</a></div>`;
        return null;
      }
      let ctl = null, raf = 0;
      const build = (restoreY) => { ctl = renderCourse(root, Z, cid); if (restoreY != null) window.scrollTo(0, restoreY); };
      onState = () => {
        cancelAnimationFrame(raf);
        raf = requestAnimationFrame(() => {
          if (!root.isConnected || !ctl || ctl.busy()) return;
          if (ctl.sig() === ctl.drawn) return;
          const y = window.scrollY;
          ctl.destroy();
          build(y);
        });
      };
      build(null);
      /* Without a manifest, whether a lesson is written is only known once it has been fetched: find out, then redraw */
      if (!probed.has(cid) && C.courseLessons(cid).some(x => x.written == null)) {
        probed.add(cid);
        C.probe(cid).then(() => { if (onState) onState({ what: 'probe' }); }).catch(() => {});
      }
      return () => { onState = null; cancelAnimationFrame(raf); if (ctl) ctl.destroy(); };
    },
  });

  function renderCourse(root, Z, cid) {
    const C = Z.content, S = Z.state, esc = Z.esc;
    const co = C.course(cid);
    const sum = S.summary();
    const topic = C.topic(co.topic) || { id: co.topic || '', name: co.topicName || '', courses: [cid] };
    const tcourses = (topic.courses || []).map(id => C.course(id)).filter(Boolean);
    const courseIdx = tcourses.findIndex(c => c.id === cid);
    const nextCourse = tcourses[courseIdx + 1] || null;
    const resource = topic.resource || null;
    const track = co.track || 'prob';
    const deskMQ = matchMedia('(min-width: 768px)'), wideMQ = matchMedia('(min-width: 1024px)');
    const desk = () => deskMQ.matches;
    const timers = [];
    let alive = true, animating = false;
    const later = (fn, ms) => timers.push(setTimeout(() => alive && fn(), ms));
    const pathOf = (name) => (Z.icon(name).match(/ d="([^"]+)"/) || [])[1] || '';
    const motion = () => (Z.reducedMotion() ? 'auto' : 'smooth');

    /* ---------- Levels and path entries ---------- */
    const items = C.courseLessons(cid);
    const levels = (co.levels || []).map(lv => ({ n: lv.n, name: lv.name }));
    const flat = [];
    let count = 0;
    levels.forEach(lv => items.filter(x => x.level === lv.n).forEach((it, j) => flat.push({ it, lv, j, g: flat.length, no: it.kind === 'lesson' ? ++count : 0 })));
    const byId = (id) => flat.find(e => e.it.id === id);
    const lessonsTotal = count;

    const lrec = (e) => S.lessons[keyOf(cid, e.it.id)] || null;
    const rrec = (e) => S.reviews[keyOf(cid, e.it.id)] || null;
    const hrec = (e) => S.homework[keyOf(cid, e.it.id)] || null;
    const isDone = (e) => (e.it.kind === 'lesson' ? !!(lrec(e) && lrec(e).done) : e.it.kind === 'review' ? !!rrec(e) : !!(hrec(e) && hrec(e).submitted));
    const writtenOf = (e) => e.it.written !== false; // null (not known yet) is treated as written; the lesson screen copes either way
    /* Prerequisite gating (ENGINE-BACKLOG 484): a node that is not done and is locked is drawn with a lock and offers no "Jump ahead" */
    const lockedE = (e) => !isDone(e) && !!Z.prereq && Z.prereq.itemLocked(cid, e.it.id);
    const curE = flat.find(e => e.it.kind === 'lesson' && writtenOf(e) && !isDone(e) && !lockedE(e)) || null;
    const firstLocked = curE ? null : flat.find(e => e.it.kind === 'lesson' && writtenOf(e) && !isDone(e)) || null;
    const statusOf = (e) => (isDone(e) ? 'done' : !writtenOf(e) ? 'nw' : lockedE(e) ? 'locked' : e === curE ? 'current' : 'upcoming');
    const mastered = (e) => e.it.kind === 'lesson' && !!(lrec(e) && lrec(e).mastered);
    const sig = () => {
      /* recomputed against the live state: a fresh closure over the same course */
      const s2 = S.summary();
      const st = (e) => {
        const k = keyOf(cid, e.it.id);
        const d = e.it.kind === 'lesson' ? !!(S.lessons[k] && S.lessons[k].done) : e.it.kind === 'review' ? !!S.reviews[k] : !!(S.homework[k] && S.homework[k].submitted);
        return d ? 'done' : 'x';
      };
      const cur = flat.find(e => e.it.kind === 'lesson' && writtenOf(e) && st(e) !== 'done' && !lockedE(e));
      return JSON.stringify([flat.map(st).join(''), flat.map(e => (lockedE(e) ? 1 : 0)).join(''), flat.map(e => (e.it.kind === 'lesson' && S.lessons[keyOf(cid, e.it.id)] && S.lessons[keyOf(cid, e.it.id)].mastered ? 1 : 0)).join(''),
        s2.courseProgress[cid], s2.streak, s2.todayQualified, S.exams['topic-' + topic.id] || null, cur && S.lessons[keyOf(cid, cur.it.id)] && S.lessons[keyOf(cid, cur.it.id)].position ? 1 : 0,
        flat.map(e => e.it.written).join(',')]);
    };

    /* ---------- Returning from a lesson ---------- */
    const L = window.ZQLaunch, flashSet = window.ZQFlash;
    let view = {}; // id -> status drawn before the completion animation runs
    let finished = null, streakFlash = flashSet === 'streak';
    if (flashSet) window.ZQFlash = null;
    if (L && L.course === cid && Date.now() - (L.at || 0) < 12 * 3600e3) {
      window.ZQLaunch = null;
      const doneE = byId(L.id);
      if (doneE && doneE.it.kind === 'lesson' && !L.wasDone && isDone(doneE)) {
        /* The halo moves on only when the finished lesson was the learner's place; a jump ahead just fills its node */
        const wasCurrent = !curE || curE.g > doneE.g;
        finished = { doneE, nextE: wasCurrent ? curE : null };
        view[doneE.it.id] = wasCurrent ? 'current' : 'upcoming';
        if (wasCurrent && curE) view[curE.it.id] = 'upcoming';
      }
      if (!L.qualifiedBefore && sum.todayQualified) streakFlash = true;
    }
    const shown = (e) => view[e.it.id] || statusOf(e);
    const lessonsDone = (st = statusOf) => flat.filter(e => e.it.kind === 'lesson' && st(e) === 'done').length;
    const pct = (n) => (lessonsTotal ? Math.round(n / lessonsTotal * 100) : 0);

    /* The prep paths a lesson is on (ENGINE-BACKLOG 455); none for a review or homework */
    const prepOf = (e) => (e.it.kind === 'lesson' ? C.prepFor(cid, e.it.id) : []);
    const kindName = (e) => (e.it.kind === 'lesson' ? `Lesson ${e.no}` : e.it.kind === 'review' ? `Level ${e.lv.n} review` : e.it.name);
    const ariaFor = (e, st) => {
      const it = e.it;
      const what = it.kind === 'lesson' ? `Lesson ${e.no}, ${it.name}` : it.kind === 'review' ? `Level ${e.lv.n} review` : `${it.name}, level ${e.lv.n}`;
      const state = st === 'done' ? (mastered(e) ? 'Done, mastered' : 'Done') : st === 'current' ? 'Up next' : st === 'nw' ? 'Not yet written' : st === 'locked' ? 'Locked until its prerequisites are met' : 'Not started';
      return `${what}. ${state}.${prepOf(e).length ? ' Interview prep.' : ''}`;
    };

    /* ---------- Puck ---------- */
    const puck = (kind) => {
      const star = pathOf('star');
      let glyph = '';
      if (kind === 'lesson') glyph = `<g transform="translate(50 ${RY}) scale(1 0.62)"><g class="zc-gpop zc-tick"><path class="zc-emb" d="M-12 0L-4 8L13-9"/><path class="zc-chk" d="M-12 0L-4 8L13-9"/></g></g>`;
      if (kind === 'review') glyph = `<g transform="translate(50 ${RY}) scale(1.4 0.86) translate(-12 -12)"><path class="zc-semb" d="${star}" transform="translate(0 2)"/><path class="zc-star" d="${star}"/></g>`;
      if (kind === 'homework') glyph = `<g transform="translate(50 ${RY + 0.6}) scale(1.35 0.82) translate(-12 -12.5)"><path class="zc-clip" d="${pathOf('clipboard')}"/></g>`;
      const mstar = kind === 'lesson' ? `<g class="zc-mstar" transform="translate(72 14) scale(0.6) translate(-12 -12)"><path d="${star}"/></g>` : '';
      return `<svg class="zc-puck" viewBox="0 0 100 ${VH}" aria-hidden="true" focusable="false">
        <path class="zc-side" d="M0 ${RY}V${RY + BAND}A50 ${RY} 0 0 0 100 ${RY + BAND}V${RY}Z"/>
        <path class="zc-shade" d="M0 ${RY + BAND - 2.5}V${RY + BAND}A50 ${RY} 0 0 0 100 ${RY + BAND}V${RY + BAND - 2.5}A50 ${RY} 0 0 1 0 ${RY + BAND - 2.5}Z"/>
        <g class="zc-top">
          <ellipse class="zc-face" cx="50" cy="${RY}" rx="50" ry="${RY}"/>
          <ellipse class="zc-fill" cx="50" cy="${RY}" rx="50" ry="${RY}"/>
          <ellipse class="zc-glow" cx="50" cy="${RY}" rx="50" ry="${RY}" fill="url(#zc-glow)"/>
          <ellipse class="zc-ring" cx="50" cy="${RY}" rx="37" ry="${(RY * 0.74).toFixed(2)}" pathLength="120"/>
          ${glyph}${mstar}
        </g></svg>`;
    };
    /* Item 10: a workshop or project lesson says so on its row ("Workshop, 60 min"); short lessons say nothing */
    const sessionOf = (e) => (e.it.kind === 'lesson' && C.sessionOf ? C.sessionOf(cid, e.it.id) : null);
    const sessionTag = (e) => { const x = sessionOf(e); return x && Z.hours ? `<span class="zc-sesstag">${esc(Z.hours.sessionLabel(x.session, x.minutes))}</span>` : ''; };
    const nodeCls = (e, st) => `zc-node k-${e.it.kind} s-${st}${st === 'done' && mastered(e) ? ' is-m' : ''}`;
    const node = (e) => {
      const st = shown(e);
      return `<li><button type="button" class="${nodeCls(e, st)}" data-id="${esc(e.it.id)}" style="--x:${xAt(e.g).toFixed(4)};--i:${e.j}" aria-label="${esc(ariaFor(e, st))}">
        <span class="zc-pw">
          <span class="zc-halo" aria-hidden="true"><i></i></span>
          <span class="zc-beam" aria-hidden="true"></span>
          ${puck(e.it.kind)}
          <span class="zc-mark" aria-hidden="true"><span>${Z.mark()}</span></span>
          ${st === 'locked' ? `<span class="zc-lock" aria-hidden="true">${Z.icon('lock', 'sm')}</span>` : ''}
        </span>
        <span class="zc-tt"><span class="zc-title">${esc(e.it.name)}</span>${C.prepChip(prepOf(e), 'is-sm')}${st === 'nw' ? '<span class="zc-nwtag">Not yet written</span>' : sessionTag(e)}</span>
      </button></li>`;
    };

    /* ---------- Page ---------- */
    const written = flat.filter(e => e.it.kind === 'lesson' && writtenOf(e)).length;
    const mapOnly = lessonsTotal > 0 && written === 0;
    const stats = `<span>${Z.icon('learn', 'sm')} ${lessonsTotal} lessons</span><span aria-hidden="true">·</span><span>${Z.icon('grid', 'sm')} ${levels.length} ${levels.length === 1 ? 'level' : 'levels'}</span>${written < lessonsTotal && !mapOnly ? `<span aria-hidden="true">·</span><span>${Z.icon('edit', 'sm')} ${written} written</span>` : ''}`;
    const resLink = resource && resource.name ? (resource.url
      ? `<a class="zc-res" href="${esc(resource.url)}" target="_blank" rel="noopener">${Z.icon('book', 'sm')}<span>${esc(resource.name)}</span><span class="sr-only"> (opens in a new tab)</span></a>`
      : `<span class="zc-res is-plain">${Z.icon('book', 'sm')}<span>${esc(resource.name)}</span></span>`) : '';
    const p0 = pct(lessonsDone(shown));
    const contLabel = () => {
      if (!curE) return null;
      const r = lrec(curE);
      if (r && r.position) return 'Continue lesson';
      return lessonsDone() ? 'Continue course' : 'Start course';
    };
    const cont = curE
      ? `<button type="button" class="btn track block zc-continue" data-cont>${contLabel()}</button>`
      : firstLocked
        ? `<button type="button" class="btn track block zc-continue" data-cont-locked>See what is missing</button>`
      : mapOnly || written < lessonsTotal
        ? (resource && resource.url ? `<a class="btn track block zc-continue" href="${esc(resource.url)}" target="_blank" rel="noopener">Open the topic resource</a>` : '')
        : `<button type="button" class="btn track block zc-continue" data-go="review">Practise in Review</button>`;

    const ex = S.exams['topic-' + topic.id], attempts = ex && Array.isArray(ex.attempts) ? ex.attempts : [];
    const passed = attempts.filter(a => a.passed);
    const examLine = passed.length
      ? `<b>You passed the ${esc(topic.id)} ${esc(topic.name)} exam</b> with ${Math.max(...passed.map(pctOf))}%. <button type="button" class="link-btn zc-testout">Sit it again</button>`
      : `<b>The ${esc(topic.id)} ${esc(topic.name)} exam</b> covers every course in this topic${tcourses.length > 1 ? `, up to ${esc(tcourses[tcourses.length - 1].name)}` : ''}.${attempts.length ? ` Your best so far is ${Math.max(...attempts.map(pctOf))}%.` : ''} Know it already? <button type="button" class="link-btn zc-testout">Sit it now to test out</button>`;

    const curStreak = streakFlash && !sum.streakOff ? Math.max(0, sum.streak - 1) : sum.streak;
    const curLit = streakFlash ? false : sum.todayQualified;
    root.innerHTML = `
    <div class="zc" data-track="${track}">
      <svg class="zc-defs" width="0" height="0" aria-hidden="true" focusable="false"><defs>
        <radialGradient id="zc-glow" cx="50%" cy="42%" r="58%"><stop offset="0" style="stop-color:var(--zc-glow);stop-opacity:0.95"/><stop offset="0.55" style="stop-color:var(--zc-glow);stop-opacity:0.6"/><stop offset="1" style="stop-color:var(--zc-glow);stop-opacity:0"/></radialGradient>
      </defs></svg>
      <div class="zc-topbar">
        <button type="button" class="icon-btn zc-back" aria-label="Back to Learn">${Z.icon('chevronL')}</button>
        <button type="button" class="streak-pill" data-zc-streak ${sum.streakOff ? 'hidden' : ''} aria-label="Streak ${curStreak} days">${curStreak}${Z.bolt(curLit)}<span class="rest-slots">${[0, 1].map(i => `<i class="${i < sum.restDays ? 'on' : ''}"></i>`).join('')}</span></button>
      </div>
      <aside class="zc-course card" aria-labelledby="zc-title">
        <div class="zc-art">${ZQArt(co.art, { label: '' })}</div>
        <div class="zc-course-body">
          <span class="chip track">${esc(topic.id)} ${esc(topic.name)}</span>${C.strandBadge(co.strand, co.strandNote)}
          <h1 class="t-course-title" id="zc-title">${esc(co.name)}</h1>
          <p class="t-body secondary zc-desc">${esc(co.description || '')}</p>
          <p class="t-label zc-stats">${stats}</p>
          ${mapOnly ? `<p class="t-caption secondary zc-maponly"><span class="zc-maptag">Map only</span>The lessons here are not written yet. Study this topic from its resource meanwhile.</p>` : ''}
          ${resLink}
          <div class="zc-prog">
            <div class="bar thin track" role="progressbar" aria-label="Course progress" aria-valuemin="0" aria-valuemax="100" aria-valuenow="${p0}"><i style="width:${p0}%"></i></div>
            <span class="t-caption muted tnum zc-pct">${p0}% complete</span>
          </div>
          ${cont}
        </div>
      </aside>
      <div class="zc-col">
        ${levels.map(lv => {
          const es = flat.filter(e => e.lv === lv);
          return `<section class="zc-level" aria-labelledby="zc-lv${lv.n}">
            <div class="zc-lvwrap"><div class="zc-lvcard"><div class="t-overline zc-deep">Level ${lv.n}</div><h2 class="t-h2" id="zc-lv${lv.n}">${esc(lv.name)}</h2></div></div>
            <ol class="zc-path" style="--n:${Math.max(1, es.length)}">${es.map(node).join('')}</ol>
          </section>`;
        }).join('')}
        <div class="zc-end">
          ${nextCourse ? `<button type="button" class="zc-next card" data-zc-next="${esc(nextCourse.id)}" data-track="${nextCourse.track || track}">
            <span class="zc-next-art">${ZQArt(nextCourse.art, { label: '' })}</span>
            <span class="zc-next-text"><span class="t-overline zc-deep">Next course</span><span class="t-sheet-title">${esc(nextCourse.name)}</span><span class="t-caption muted">${C.courseLessons(nextCourse.id).filter(x => x.kind === 'lesson').length} lessons · ${(nextCourse.levels || []).length} levels</span></span>
            <span class="zc-next-go">${Z.icon('chevronR')}</span>
          </button>` : ''}
          <div class="zc-exam">
            <span class="zc-exam-ic">${Z.icon('shield')}</span>
            <p class="t-body">${examLine}</p>
          </div>
        </div>
      </div>
      <div class="zc-pop" hidden>
        <div class="zc-pop-glow" aria-hidden="true"></div>
        <div class="zc-pop-card" role="dialog" aria-modal="false" aria-labelledby="zc-pop-title">
          <button type="button" class="icon-btn zc-pop-x" aria-label="Close">${Z.icon('close')}</button>
          <div class="zc-pop-body"></div>
        </div>
      </div>
      <button type="button" class="btn secondary round zc-tocur" hidden aria-label="Scroll to your current lesson">${Z.icon('chevronD')}</button>
    </div>`;
    Z.mathify(root);

    const $ = (s) => root.querySelector(s);
    const col = $('.zc-col'), pop = $('.zc-pop'), popCard = $('.zc-pop-card'), popBody = $('.zc-pop-body'), tocur = $('.zc-tocur');
    const nodeEl = (id) => Array.from(col.querySelectorAll('.zc-node')).find(n => n.dataset.id === id) || null;

    /* ---------- Launching: lessons, reviews and homework each have their own route ---------- */
    const routeFor = (e) => `${e.it.kind === 'review' ? 'review' : e.it.kind === 'homework' ? 'homework' : 'lesson'}/${cid}/${e.it.id}`;
    const launch = (e) => {
      if (!e || !writtenOf(e)) return;
      Z.sound('tap');
      if (e.it.kind === 'lesson' && S.lessonPosition && S.lessonPosition.pick) S.lessonPosition.pick(cid, e.it.id);   // a deliberate open: lets a saved place stand in a tested-out course (617)
      window.ZQLaunch = { course: cid, id: e.it.id, kind: e.it.kind, wasDone: isDone(e), qualifiedBefore: !!S.summary().todayQualified, at: Date.now() };
      Z.go(routeFor(e));
    };

    /* ---------- Node card: content shared by the desktop card and the mobile sheet ---------- */
    const pearStar = `<svg class="zc-pstar" viewBox="0 0 24 24" aria-hidden="true"><path d="${pathOf('star')}"/></svg>`;
    const shortDate = (t) => new Date(t).toLocaleDateString('en-GB', { weekday: 'short', day: 'numeric', month: 'short' }).replace(',', '');
    const actFor = (e) => {
      const it = e.it, st = statusOf(e);
      if (st === 'nw') return null;
      if (st === 'locked') return { label: `${Z.icon('lock')}See what is missing`, cap: 'It opens when the levels it relies on are met. You can test out of one from there.' };
      if (it.kind === 'review') return { label: st === 'done' ? `${Z.icon('replay')}Redo the review` : 'Start the review' };
      if (it.kind === 'homework') {
        const h = hrec(e);
        if (h && h.submitted) return { label: 'See your homework' };
        return { label: h ? 'Continue' : 'Start' };
      }
      if (st === 'done') return { label: `${Z.icon('replay')}Redo` };
      if (st === 'current') return { label: lrec(e) && lrec(e).position ? 'Continue' : 'Start' };
      return { label: 'Jump ahead', cap: 'The lessons before it stay on your map, ready when you want them.' };
    };
    const metaFor = (e) => {
      const it = e.it, st = statusOf(e);
      if (st === 'nw') return 'Not yet written';
      if (st === 'locked') return 'Locked until the levels it relies on are met';
      if (it.kind === 'review') {
        const r = rrec(e);
        return r ? `Mixed problems from Level ${e.lv.n} · Last score ${r.score} of ${r.items}` : `Mixed problems from Level ${e.lv.n} · No hints, one try each`;
      }
      if (it.kind === 'homework') {
        const h = hrec(e);
        if (h && h.submitted) return `Submitted · ${h.score != null ? `${h.score} of ${h.items} right` : 'self-marked'}`;
        if (h && h.due) return `Due ${shortDate(h.due)}${h.due < Date.now() ? ', overdue' : ''}`;
        return 'Problems on the whole level · due 7 days after you start';
      }
      const m = lessonMeta[keyOf(cid, it.id)];
      const r = lrec(e);
      const adv = Z.prereq && it.kind === 'lesson' ? Z.prereq.advisoryFor(cid, it.id) : [];
      const note = adv.length ? ` · Note: it relies on ${adv.map(x => `${x.courseName}, level ${x.n}`).join(' and ')}, which is optional on your track` : '';
      const where = r && r.position ? (r.position.phase === 'quiz' ? ` · Paused at quiz question ${(r.position.q || 0) + 1}` : ` · Paused at screen ${(r.position.i || 0) + 1}`) : '';
      const sx = sessionOf(e);
      const len = sx && Z.hours ? Z.hours.sessionLabel(sx.session, sx.minutes) : m ? `about ${m.minutes} min` : `About ${DEFAULT_MIN} min`;
      return (m ? `${m.screens} screens · ${len}` : len) + where + note;
    };
    /* ENGINE-BACKLOG 551: the reason for the first missing prerequisite, "Check first" diagnostics and the route label, as short lines on the card */
    const nodeNotes = (e) => {
      const P = Z.prereq, it = e.it;
      if (!P || !Z.checkFirst || (it.kind !== 'lesson' && it.kind !== 'review' && it.kind !== 'homework')) return '';
      const lesson = it.kind === 'lesson', st = statusOf(e);
      const m = st === 'locked' ? (lesson ? P.missingFor(cid, it.id) : P.missingForLevel(cid, e.lv.n)) : null;
      const first = m && ((m.start && m.start.node) || m.direct[0]);
      const why = first && first.why ? `<p class="t-caption secondary zc-why">${esc(first.why)}</p>` : '';
      const chk = Z.checkFirst(lesson ? P.diagnosticsFor(cid, it.id) : P.diagnosticsForLevel(cid, e.lv.n), esc);
      const lim = lesson ? P.routeLimitsForLesson(cid, it.id) : P.routeLimitsForLevel(cid, e.lv.n);
      return `${why}${chk}${lim.length ? `<div class="rl-row">${Z.routeLimited(lim, esc)}</div>` : ''}`;
    };
    const fillInfo = (body, e, close) => {
      const it = e.it, st = statusOf(e);
      const over = `Level ${e.lv.n} · ${it.kind === 'lesson' ? `Lesson ${e.no}` : it.kind === 'review' ? 'Review' : 'Homework'}`;
      const title = it.kind === 'review' ? `Level ${e.lv.n} review` : it.name;
      const r = it.kind === 'lesson' ? lrec(e) : null;
      const q = r && r.bestQuiz;
      const score = q ? `<div class="zc-score">
          <span class="t-label">Best quiz score <b class="tnum">${q[0]} of ${q[1]}</b></span>
          ${mastered(e) ? `<span class="zc-mchip">${pearStar}Mastered</span>` : `<span class="t-caption muted">Score ${Math.ceil(q[1] * 0.8)} of ${q[1]} to master it</span>`}
        </div>` : '';
      const perfect = r && r.perfect ? `<p class="t-caption secondary zc-perf">${Z.icon('star', 'xs')}Perfect lesson: every problem right first time.</p>` : '';
      const act = actFor(e);
      const pp = prepOf(e);
      const prepLine = pp.length ? `<p class="t-caption secondary zc-prep"><b>Interview prep:</b> ${esc(C.prepDetail(pp))} <a href="#prepare${pp.length === 1 ? '/' + encodeURIComponent(pp[0].id) : ''}">See ${pp.length === 1 ? 'the path' : 'the paths'}</a></p>` : '';
      const nwBody = st === 'nw' ? `${resource && resource.url ? `<a class="btn secondary block" href="${esc(resource.url)}" target="_blank" rel="noopener">Open the topic resource</a>` : ''}
          <p class="t-caption muted zc-cap">${resource && resource.name ? `Until it is written, study it from ${esc(resource.name)}.` : 'Until it is written, study it from the topic resource.'}</p>` : '';
      body.innerHTML = `<div class="zc-info">
        <div class="t-overline zc-deep">${over}</div>
        <h2 class="t-sheet-title" id="zc-pop-title">${esc(title)}</h2>
        ${it.objective ? `<p class="t-body zc-obj">${Z.md(esc(it.objective))}</p>` : ''}
        <p class="t-body secondary zc-meta" data-meta>${esc(metaFor(e))}</p>
        ${nodeNotes(e)}
        ${prepLine}${score}${perfect}
        ${act ? `<button type="button" class="btn track lg block" data-act>${act.label}</button>` : ''}
        ${act && act.cap ? `<p class="t-caption muted zc-cap">${esc(act.cap)}</p>` : ''}
        ${nwBody}
      </div>`;
      Z.mathify(body);
      const b = body.querySelector('[data-act]');
      if (b) b.addEventListener('click', () => { if (close) close(); launch(e); });
      /* Screens and minutes come from the lesson file */
      if (it.kind === 'lesson' && st !== 'nw' && !lessonMeta[keyOf(cid, it.id)]) {
        C.lesson(cid, it.id).then(Ld => {
          if (!Ld) return;
          lessonMeta[keyOf(cid, it.id)] = { screens: (Ld.screens || []).length + (Ld.summary ? 1 : 0), minutes: Ld.minutes || DEFAULT_MIN, session: Ld.session || 'short' };
          const m = body.querySelector('[data-meta]'); if (m && alive) m.textContent = metaFor(e);
        }).catch(() => { /* keep the estimate */ });
      }
    };

    /* ---------- Desktop card anchored to the bottom of the path column ---------- */
    let selected = null, closeSheet = null;
    const place = () => {
      const r = col.getBoundingClientRect();
      if (desk()) {
        pop.style.left = r.left + 'px'; pop.style.width = r.width + 'px';
        tocur.style.left = (r.right - 48) + 'px'; tocur.style.right = 'auto';
        tocur.style.bottom = pop.hidden ? '' : (popCard.offsetHeight + 40) + 'px';
      } else {
        tocur.style.left = ''; tocur.style.right = ''; tocur.style.bottom = '';
      }
    };
    /* Keep the tapped node clear of the card, including after the card grows */
    const keepClear = (btn) => {
      const nb = btn.getBoundingClientRect(), cardTop = popCard.getBoundingClientRect().top;
      if (nb.bottom > cardTop - 16) window.scrollBy({ top: nb.bottom - cardTop + 48, behavior: motion() });
    };
    const unselect = () => { if (selected) { selected.classList.remove('is-sel'); selected.removeAttribute('aria-expanded'); } };
    const closePop = (refocus) => {
      if (pop.hidden) return;
      pop.hidden = true; popBody.innerHTML = '';
      const s = selected; unselect(); selected = null; place();
      if (refocus && s) s.focus({ preventScroll: true });
    };
    const ro = 'ResizeObserver' in window ? new ResizeObserver(() => { place(); if (selected && !pop.hidden && desk()) keepClear(selected); }) : null;
    if (ro) ro.observe(popCard);
    const openNode = (btn) => {
      const e = byId(btn.dataset.id);
      if (!e) return;
      Z.sound('tap');
      unselect(); selected = btn; btn.classList.add('is-sel'); btn.setAttribute('aria-expanded', 'true');
      if (desk()) {
        fillInfo(popBody, e, null);
        pop.hidden = false;
        popCard.classList.remove('zc-in'); void popCard.offsetWidth; popCard.classList.add('zc-in');
        place();
        (popBody.querySelector('[data-act]') || $('.zc-pop-x')).focus({ preventScroll: true });
        if (!ro) keepClear(btn);
      } else {
        const body = Z.h(`<div class="zc-sheet" data-track="${track}"></div>`);
        let closer = null;
        fillInfo(body, e, () => closer && closer());
        closer = closeSheet = Z.sheet(body, { label: e.it.kind === 'review' ? `Level ${e.lv.n} review` : e.it.name, onClose: () => { unselect(); selected = null; closeSheet = null; } });
      }
    };
    $('.zc-pop-x').addEventListener('click', () => closePop(true));

    /* ---------- Scroll-to-current button ---------- */
    let io = null;
    const observe = () => {
      if (io) io.disconnect();
      const cur = col.querySelector('.zc-node.s-current .zc-pw');
      if (!cur || !('IntersectionObserver' in window)) { tocur.hidden = true; return; }
      const top = desk() ? 64 + 110 : 110, bottom = desk() ? 0 : 92;
      io = new IntersectionObserver(([en]) => {
        const off = !en.isIntersecting;
        tocur.hidden = !off;
        if (off) {
          const up = en.boundingClientRect.top < (en.rootBounds ? en.rootBounds.top : 0);
          tocur.innerHTML = Z.icon(up ? 'chevronU' : 'chevronD');
          place();
        }
      }, { rootMargin: `-${top}px 0px -${bottom}px 0px` });
      io.observe(cur);
    };
    tocur.addEventListener('click', () => {
      const cur = col.querySelector('.zc-node.s-current');
      if (!cur) return;
      cur.scrollIntoView({ block: 'center', behavior: motion() });
      cur.focus({ preventScroll: true });
    });

    /* ---------- Wiring ---------- */
    col.addEventListener('click', (ev) => {
      const btn = ev.target.closest('.zc-node');
      if (btn) { openNode(btn); return; }
      const nx = ev.target.closest('[data-zc-next]');
      if (nx) { Z.go('course/' + nx.dataset.zcNext); return; }
      if (ev.target.closest('.zc-testout')) Z.go('exam/topic-' + topic.id);
    });
    const contBtn = $('[data-cont]');
    if (contBtn) contBtn.addEventListener('click', () => launch(curE));
    const lockBtn = $('[data-cont-locked]');
    if (lockBtn) lockBtn.addEventListener('click', () => launch(firstLocked));
    const goBtn = $('.zc-continue[data-go]');
    if (goBtn) goBtn.addEventListener('click', () => Z.go(goBtn.dataset.go));
    $('.zc-back').addEventListener('click', () => Z.go('learn'));
    $('[data-zc-streak]').addEventListener('click', () => Z.streakSheet());
    const onDown = (ev) => { if (!pop.hidden && !popCard.contains(ev.target) && !ev.target.closest('.zc-node')) closePop(false); };
    const onKey = (ev) => { if (ev.key === 'Escape' && !pop.hidden) closePop(true); };
    const onMQ = () => { closePop(false); if (closeSheet) closeSheet(); observe(); place(); };
    document.addEventListener('pointerdown', onDown);
    document.addEventListener('keydown', onKey);
    window.addEventListener('resize', place);
    deskMQ.addEventListener('change', onMQ);
    place();
    later(observe, 60);

    /* ---------- Completion: the done node fills over 300ms, the next takes its halo on spring-bounce ---------- */
    const complete = async ({ doneE, nextE }, scroll) => {
      const nd = nodeEl(doneE.it.id), nn = nextE && nodeEl(nextE.it.id);
      if (!nd) { animating = false; return; }
      if (scroll) {
        /* Bring the finished node and the next one into view together */
        const top = desk() ? 190 : 130, bottom = innerHeight - (desk() ? 40 : 100);
        const a = nd.getBoundingClientRect().top - 70, b = (nn || nd).getBoundingClientRect().bottom;
        if (a < top || b > bottom) {
          window.scrollBy({ top: (a + b) / 2 - (top + bottom) / 2, behavior: motion() });
          await Z.wait(560);
        }
        if (!alive) return;
      }
      view = {};
      nd.className = nodeCls(doneE, 'done') + ' zc-just';
      nd.setAttribute('aria-label', ariaFor(doneE, 'done'));
      const p = pct(lessonsDone());
      const bar = $('.zc-prog .bar');
      bar.firstElementChild.style.width = p + '%'; bar.setAttribute('aria-valuenow', p);
      $('.zc-pct').textContent = `${p}% complete`;
      Z.haptic();
      await Z.wait(300);
      if (!alive) return;
      if (nn) {
        nn.className = nodeCls(nextE, 'current') + ' zc-arrive';
        nn.setAttribute('aria-label', ariaFor(nextE, 'current'));
      }
      observe();
      animating = false;
      if (onState) onState({ what: 'settled' }); // anything that changed while the animation ran
    };

    /* ---------- Streak toast on return from a lesson ---------- */
    if (streakFlash && !sum.streakOff) {
      Z.toast(`${Z.bolt(true)}<span>Streak extended</span>`, 2600);
      /* At 1024px and up the toast sits over the path column */
      const t = [...document.querySelectorAll('body > .toast')].pop();
      if (t && wideMQ.matches) {
        const r = col.getBoundingClientRect();
        Object.assign(t.style, { left: r.left + 'px', width: r.width + 'px', right: 'auto', margin: '0', maxWidth: 'none' });
      }
      /* Both pills start from yesterday's count, unlit, then the bolt lights and the count turns over */
      const pills = [...document.querySelectorAll('#app [data-streak], #app [data-zc-streak]')];
      pills.forEach(p => { if (p.firstChild && p.firstChild.nodeType === 3) p.firstChild.nodeValue = String(curStreak); const b = p.querySelector('.bolt'); if (b) b.classList.remove('lit'); });
      const paint = () => pills.forEach(p => {
        if (p.firstChild && p.firstChild.nodeType === 3) p.firstChild.nodeValue = String(sum.streak);
        const b = p.querySelector('.bolt'); if (b) b.classList.add('lit');
        p.setAttribute('aria-label', `Streak ${sum.streak} days`);
      });
      if (Z.reducedMotion()) paint();
      else later(() => {
        Z.sound('streak');
        pills.forEach(p => { const b = p.querySelector('.bolt'); if (b) { b.classList.add('lit'); b.animate([{ transform: 'scale(1)' }, { transform: 'scale(1.25)', offset: 0.45 }, { transform: 'scale(1)' }], { duration: 500, easing: 'cubic-bezier(0.2, 0, 0, 1)' }); } });
        later(paint, 225);
      }, 300);
    }
    if (finished) { animating = true; later(() => complete(finished, true), 450); }

    const drawn = sig(); // the state is final already; view{} only changes what is drawn until the animation ends
    return {
      sig, drawn, busy: () => animating,
      destroy() {
        alive = false;
        timers.forEach(clearTimeout);
        if (io) io.disconnect();
        if (ro) ro.disconnect();
        if (closeSheet) closeSheet();
        document.removeEventListener('pointerdown', onDown);
        document.removeEventListener('keydown', onKey);
        window.removeEventListener('resize', place);
        deskMQ.removeEventListener('change', onMQ);
      },
    };
  }
})();
