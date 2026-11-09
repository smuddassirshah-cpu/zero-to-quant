/* Practice and redo selection (docs/PLAN.md 10, design-research 5.7 and 8.4).

   ZQ.select.practiceSet({ course, topic, n = 8 })  an interleaved set from the quiz items of finished lessons, plus the
       items of written level reviews (and of submitted homework, without long-form or code items). Each item is weighted
       towards the learner's lowest-mastery skills (summary().skillMastery) and the skills least recently seen
       (skills[*].lastAt), measured against a Leitner interval of 1, 3, 7 or 30 days chosen by the skill's correct
       count. No two consecutive items come from the same lesson when that can be avoided.
   ZQ.select.redoSession()   the due redo entries (ZQ.state.redo.due()), oldest due first, resolved to their items: a
       lesson screen, a quiz item, a review item, a homework item or an exam item ({ exam, item }, from examFinished), by ref. Entries whose source cannot be found are left
       out (and stay in the queue).
   ZQ.select.weeklyProbs()   three probability problems a week from the topic 1.5 pools, once any 1.5 lesson is finished.
       The week's picks are kept in ZQ.state.flags.weeklyProbs = { week, done, ids }, so they stay fixed for the week.
   ZQ.select.weeklyStatus() { eligible, week, done, total }   and   ZQ.select.weeklyRecord(done)
   ZQ.select.bankDeck({ n = 8 })   the Interview practice deck (ENGINE-BACKLOG 456): items from content/bank/*.json plus the
       tagged review and homework items of finished lessons, each scheduled on its own (ZQ.state.bank, Leitner 1, 3, 7, 30
       days). Due items first, then unseen ones, families mixed (round robin, no two neighbours from one family when
       avoidable). A bank item whose `requires` lessons are not all finished is not drawn.
   ZQ.select.bankStatus()  { total, due, fresh, later, locked, families, nextDue }, without drawing anything
   ZQ.select.resolve(ref, kind), ZQ.select.source(ref, kind), ZQ.select.pool({ course, topic }), ZQ.select.interval(skill)

   Every async call resolves to an array of items in the AUTHORING.md item format, each with ref, skills, uid and a
   source label attached. Nothing here writes learner state except the weekly flag; the screens that run these sets
   record practice and weekly answers with ZQ.state.practiceResult (Elo and the streak count) and redos with redo.result. */
(function () {
  'use strict';
  const Z = window.ZQ = window.ZQ || {};
  const DAY = 86400000;
  const LEITNER = [1, 3, 7, 30];
  const WEEKLY_TOPIC = '1.5', WEEKLY_N = 3;
  const RECENT_KEY = 'select.recent', RECENT_MS = DAY;

  const S = () => Z.state;
  const C = () => Z.content;
  const now = () => Date.now();
  const hash = (s) => { let h = 2166136261; for (const c of String(s)) { h ^= c.charCodeAt(0); h = Math.imul(h, 16777619); } return h >>> 0; };
  const rngFrom = (seed) => { let a = seed >>> 0; return () => { a = (a + 0x6D2B79F5) >>> 0; let t = a; t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; };
  const safe = (p) => Promise.resolve(p).catch((e) => { console.warn(e); return null; });

  /* ---------- Content helpers ---------- */
  const courseOf = (cid) => { try { return C().course(cid); } catch { return null; } };
  const lessonNumber = (cid, lid) => { try { const ls = C().courseLessons(cid).filter(x => x.kind === 'lesson'); const i = ls.findIndex(x => x.id === lid); return i >= 0 ? i + 1 : null; } catch { return null; } };
  const levelOf = (cid, lid) => { const c = courseOf(cid); const lv = (c && c.levels || []).find(l => (l.lessons || []).includes(lid) || l.review === lid || l.homework === lid); return lv ? lv.n : null; };
  const written = (cid, id) => { try { return C().exists(cid, id) !== false; } catch { return true; } };
  const loadSet = (cid, id) => (/^review-/.test(id) ? safe(C().review(cid, id)) : /^homework-/.test(id) ? safe(C().homework(cid, id)) : safe(C().lesson(cid, id)));

  /* A readable source for a ref: "Conditional Probability · Lesson 2 quiz" */
  const source = (ref = {}, kind) => {
    if (ref.bank) return `Interview bank · ${ref.bank}`;
    if (ref.exam) return `Exam ${String(ref.exam).replace(/^topic-/, 'topic ').replace(/^stage-/, 'stage ')}`;
    const c = courseOf(ref.course), name = c ? c.name : ref.course || 'Unknown course';
    const id = String(ref.lesson || '');
    if (/^review-/.test(id)) return `${name} · Level ${id.split('-')[1]} review`;
    if (/^homework-/.test(id)) { const n = id.split('-')[1]; return `${name} · Homework ${n}`; }
    const n = lessonNumber(ref.course, id);
    const ln = n ? `Lesson ${n}` : C() && C().deKebab ? C().deKebab(id) : id;
    if (kind === 'screen' || ref.screen != null) return `${name} · ${ln}, screen ${(+ref.screen || 0) + 1}`;
    return `${name} · ${ln} quiz`;
  };

  /* Attach ref, skills, uid and source to an item; lesson screens lose their hints (set mode has none) */
  const norm = (it, { course, lesson, kind = 'quiz', skills, index }) => {
    const out = Object.assign({}, it);
    delete out.hints;
    const ref = kind === 'screen' ? { course, lesson, screen: index } : { course, lesson, item: it.id || 'q' + index };
    out.skills = (it.skills && it.skills.length ? it.skills : skills) || [];
    out.ref = ref;
    out.uid = kind === 'screen' ? `${course}/${lesson}#${index}` : `${course}/${lesson}/${ref.item}`;
    out.source = source(ref, kind);
    out.group = `${course}/${lesson}`;
    if (!out.id) out.id = String(ref.item || 's' + index);
    return out;
  };

  const quizItems = (L, course, lesson) => (L && Array.isArray(L.quiz) ? L.quiz.map((q, i) => norm(q, { course, lesson, skills: L.skills, index: i })) : []);
  const setItems = (D, course, id, { practice = false } = {}) => (D && Array.isArray(D.items) ? D.items.map((q, i) => norm(q, { course, lesson: id, skills: [], index: i }))
    .filter(q => !practice || !(q.kind === 'longform' || (q.widget && (q.widget.kind === 'longform' || q.widget.kind === 'code')) || (Array.isArray(q.parts) && q.parts.some(p => p && p.widget && (p.widget.kind === 'longform' || p.widget.kind === 'code'))))) : []);

  /* ---------- Learner helpers ---------- */
  const finished = () => Object.entries((S() && S().lessons) || {}).filter(([, r]) => r && r.done).map(([id]) => { const [course, lesson] = id.split('/'); return { course, lesson }; });
  const inScope = (cid, { course, topic } = {}) => {
    if (course && cid !== course) return false;
    if (topic) { const c = courseOf(cid); if (!c || String(c.topic) !== String(topic)) return false; }
    return true;
  };
  const skillRec = (s) => ((S() && S().skills) || {})[s] || null;
  /* Leitner box from the skill's correct count: 0 -> 1 day, 1 to 2 -> 3 days, 3 to 6 -> 7 days, 7 or more -> 30 days */
  const interval = (skill) => {
    const r = skillRec(skill), c = r ? r.correct || 0 : 0;
    return LEITNER[Math.min(3, Math.floor(Math.log2(c + 1)))];
  };
  const recent = {
    get() { try { return (Z.store && Z.store.get(RECENT_KEY, {})) || {}; } catch { return {}; } },
    add(uids) {
      const m = this.get(), t = now();
      uids.forEach(u => { m[u] = t; });
      const keep = Object.entries(m).filter(([, at]) => t - at < 7 * DAY).sort((a, b) => b[1] - a[1]).slice(0, 300);
      try { Z.store && Z.store.set(RECENT_KEY, Object.fromEntries(keep)); } catch { /* storage blocked: no memory of recent sets */ }
    },
  };

  /* ---------- Pools ---------- */
  const pool = async ({ course, topic } = {}) => {
    const done = finished().filter(x => inScope(x.course, { course, topic }));
    const lessons = await Promise.all(done.map(x => safe(C().lesson(x.course, x.lesson)).then(L => quizItems(L, x.course, x.lesson))));
    const items = lessons.flat();
    const seenSkills = {};
    done.forEach(x => { seenSkills[x.course] = seenSkills[x.course] || new Set(); });
    items.forEach(it => { const cs = seenSkills[it.ref.course]; it.skills.forEach(s => cs && cs.add(s)); });
    /* Review items: a written review of a level with a finished lesson, when the review was sat or every skill it tests is met */
    const courses = [...new Set(done.map(x => x.course))];
    for (const cid of courses) {
      const c = courseOf(cid); if (!c) continue;
      for (const lv of c.levels || []) {
        if (!(lv.lessons || []).some(l => done.some(x => x.course === cid && x.lesson === l))) continue;
        if (lv.review && written(cid, lv.review)) {
          const sat = !!((S() && S().reviews) || {})[`${cid}/${lv.review}`];
          const D = await loadSet(cid, lv.review);
          setItems(D, cid, lv.review).forEach(it => { if (sat || it.skills.every(s => seenSkills[cid].has(s))) items.push(it); });
        }
        const hw = lv.homework && ((S() && S().homework) || {})[`${cid}/${lv.homework}`];
        if (hw && hw.submitted && written(cid, lv.homework)) {
          const D = await loadSet(cid, lv.homework);
          setItems(D, cid, lv.homework, { practice: true }).forEach(it => items.push(it));
        }
      }
    }
    const seen = new Set();
    return items.filter(it => (seen.has(it.uid) ? false : (seen.add(it.uid), true)));
  };

  /* Weight: low mastery and overdue skills first; items served in the last day count less */
  const weightOf = (it, mastery, recentMap) => {
    const t = now();
    const sk = it.skills.length ? it.skills : ['_'];
    const m = Math.min(...sk.map(s => (s in mastery ? mastery[s] : 0)));
    const due = Math.max(...sk.map(s => {
      const r = skillRec(s);
      if (!r || !r.lastAt) return 2;
      return Math.min(3, (t - r.lastAt) / (interval(s) * DAY));
    }));
    let w = (1.15 - m) * (0.5 + due);
    if (recentMap[it.uid] && t - recentMap[it.uid] < RECENT_MS) w *= 0.25;
    return Math.max(0.01, w);
  };
  /* Order so that no two neighbours share a lesson when another item is available */
  const interleave = (list) => {
    const left = list.slice(), out = [];
    while (left.length) {
      const prev = out.length ? out[out.length - 1].group : null;
      let i = left.findIndex(x => x.group !== prev);
      if (i < 0) i = 0;
      out.push(left.splice(i, 1)[0]);
    }
    return out;
  };

  const practiceSet = async ({ course, topic, n = 8 } = {}) => {
    const items = await pool({ course, topic });
    if (!items.length) return [];
    let mastery = {};
    try { mastery = S().summary().skillMastery || {}; } catch (e) { console.warn(e); }
    const recentMap = recent.get();
    /* Weighted sampling without replacement (Efraimidis and Spirakis keys) */
    const keyed = items.map(it => ({ it, k: Math.pow(Math.random(), 1 / weightOf(it, mastery, recentMap)) })).sort((a, b) => b.k - a.k);
    const chosen = interleave(keyed.slice(0, n).map(x => x.it));
    recent.add(chosen.map(x => x.uid));
    return chosen;
  };

  /* ---------- Interview bank (ENGINE-BACKLOG 456) ---------- */
  /* A bank item in the set-item shape: uid bank/<file>/<id>, family from its first tag (else the file id), group = family */
  const bankItem = (it, file, D) => {
    const out = Object.assign({}, it);
    delete out.hints;
    const family = (Array.isArray(it.tags) && it.tags[0]) || (D && D.family) || file;
    out.ref = { bank: file, item: it.id };
    out.uid = `bank/${file}/${it.id}`;
    out.family = family;
    out.group = family;
    out.skills = it.skills || [];
    out.bankSource = it.source || '';
    out.source = `${family} · ${it.source || 'Interview bank'}`;
    return out;
  };
  const lessonsDone = (refs) => (refs || []).every(r => { try { const l = S().lessons[r]; return !!(l && l.done); } catch { return false; } });
  /* Every candidate for the deck: { items: the drawable ones, locked: the count whose prerequisite lessons are not finished } */
  const bankPool = async () => {
    const items = [];
    let locked = 0;
    for (const id of (C().bankIds ? C().bankIds() : [])) {
      const D = await safe(C().bank(id));
      if (!D || !Array.isArray(D.items)) continue;
      D.items.forEach(it => { if (!it || !it.id) return; if (lessonsDone(it.requires)) items.push(bankItem(it, id, D)); else locked++; });
    }
    /* Tagged items of finished lessons (quizzes, level reviews, submitted homework) join the deck under their own uid */
    try {
      (await pool({})).forEach(it => {
        if (!Array.isArray(it.tags) || !it.tags.length || typeof it.tags[0] !== 'string') return;
        items.push(Object.assign({}, it, { family: it.tags[0], group: it.tags[0] }));
      });
    } catch (e) { console.warn(e); }
    const seen = new Set();
    return { items: items.filter(it => (seen.has(it.uid) ? false : (seen.add(it.uid), true))), locked };
  };
  const entryOf = (uid) => { try { return S().bank.entry(uid); } catch { return null; } };
  const bankStatus = async () => {
    const { items, locked } = await bankPool(), t = now();
    const fam = {};
    let due = 0, fresh = 0, later = 0, nextDue = null;
    items.forEach(it => {
      fam[it.family] = (fam[it.family] || 0) + 1;
      const e = entryOf(it.uid);
      if (!e) fresh++; else if (e.due <= t) due++; else { later++; nextDue = nextDue == null ? e.due : Math.min(nextDue, e.due); }
    });
    return { total: items.length, due, fresh, later, locked, families: fam, nextDue };
  };
  /* One pass of a round robin over families: each family offers its items in order, the families ordered by their best item */
  const roundRobin = (list, n) => {
    const by = new Map();
    list.forEach(it => { const a = by.get(it.family) || []; a.push(it); by.set(it.family, a); });
    const queues = [...by.values()], out = [];
    while (out.length < n && queues.some(q => q.length)) queues.forEach(q => { if (out.length < n && q.length) out.push(q.shift()); });
    return out;
  };
  const bankDeck = async ({ n = 8 } = {}) => {
    const { items } = await bankPool(), t = now();
    if (!items.length) return [];
    const due = items.filter(it => { const e = entryOf(it.uid); return e && e.due <= t; }).sort((a, b) => entryOf(a.uid).due - entryOf(b.uid).due);
    const fresh = items.filter(it => !entryOf(it.uid)).map(it => ({ it, k: Math.random() })).sort((a, b) => a.k - b.k).map(o => o.it);
    const picked = roundRobin(due, n);
    if (picked.length < n) picked.push(...roundRobin(fresh, n - picked.length));
    return interleave(picked);
  };

  /* ---------- Redo ---------- */
  const findIn = (list, id) => (list || []).find((x, i) => (x.id || 'q' + i) === id) || null;
  const resolve = async (ref = {}, kind = 'quiz') => {
    if (ref.bank) { const D = await safe(C().bank(ref.bank)); const it = D && findIn(D.items, ref.item); return it ? bankItem(it, ref.bank, D) : null; }
    if (ref.exam) {
      const E = await safe(C().exam(ref.exam)); if (!E) return null;
      /* an exam document's own `parts` are its papers and checks (stage and mock exams); an item's `parts` (ENGINE-BACKLOG 467) live on the item */
      const all = (E.items || []).concat(...(Array.isArray(E.parts) ? E.parts : []).filter(p => p && p.kind === 'paper').map(p => p.items || []));
      const it = findIn(all, ref.item); if (!it) return null;
      const out = Object.assign({}, it, { ref, uid: `${ref.exam}/${ref.item}`, source: source(ref, kind), group: ref.exam, skills: it.skills || [] });
      delete out.hints; // set mode has none
      return out;
    }
    if (!ref.course || !ref.lesson) return null;
    const D = await loadSet(ref.course, ref.lesson);
    if (!D) return null;
    if (/^(review|homework)-/.test(ref.lesson)) {
      const i = (D.items || []).findIndex((x, j) => (x.id || 'q' + j) === ref.item);
      return i < 0 ? null : norm(D.items[i], { course: ref.course, lesson: ref.lesson, skills: [], index: i });
    }
    if (kind === 'screen' || ref.screen != null) {
      const i = +ref.screen, s = (D.screens || [])[i];
      return s && s.widget ? norm(s, { course: ref.course, lesson: ref.lesson, kind: 'screen', skills: D.skills, index: i }) : null;
    }
    const qi = (D.quiz || []).findIndex((x, j) => (x.id || 'q' + j) === ref.item);
    if (qi >= 0) return norm(D.quiz[qi], { course: ref.course, lesson: ref.lesson, skills: D.skills, index: qi });
    const si = (D.screens || []).findIndex(x => x.id && x.id === ref.item);
    return si >= 0 ? norm(D.screens[si], { course: ref.course, lesson: ref.lesson, kind: 'screen', skills: D.skills, index: si }) : null;
  };
  const redoSession = async () => {
    const due = (S() && S().redo && S().redo.due ? S().redo.due() : []).slice().sort((a, b) => a.due - b.due);
    const items = await Promise.all(due.map(r => resolve(r.ref, r.kind).then(it => (it ? Object.assign(it, {
      skills: (r.skills && r.skills.length ? r.skills : it.skills) || [],
      redo: { id: r.id, kind: r.kind, interval: r.interval, due: r.due, misses: r.misses },
    }) : null))));
    return items.filter(Boolean);
  };

  /* ---------- Weekly probability problems ---------- */
  const weekKey = () => { try { return S().dates.weekStart(); } catch { const d = new Date(); d.setHours(0, 0, 0, 0); d.setDate(d.getDate() - ((d.getDay() + 6) % 7)); return d.toISOString().slice(0, 10); } };
  const weeklyEligible = () => finished().some(x => inScope(x.course, { topic: WEEKLY_TOPIC }));
  const weeklyFlag = () => { try { const f = S().flags.weeklyProbs; return f && typeof f === 'object' ? f : null; } catch { return null; } };
  const weeklyStatus = () => {
    const week = weekKey(), f = weeklyFlag();
    return { eligible: weeklyEligible(), week, done: f && f.week === week ? Math.min(WEEKLY_N, f.done || 0) : 0, total: WEEKLY_N };
  };
  const weeklyRecord = (done) => {
    const week = weekKey(), f = weeklyFlag() || {};
    const cur = f.week === week ? f : { week, done: 0, ids: [] };
    try { S().flags.set({ weeklyProbs: { week, done: Math.min(WEEKLY_N, Math.max(cur.done || 0, done)), ids: cur.ids || [] } }); } catch (e) { console.error(e); }
    return weeklyStatus();
  };
  /* The 1.5 pool: quiz items of every written lesson in the topic and items of its written reviews */
  const topicPool = async (topic) => {
    let cs = [];
    try { cs = C().courses().filter(c => String(c.topic) === String(topic)); } catch { cs = []; }
    const out = [];
    for (const c of cs) {
      for (const x of C().courseLessons(c.id)) {
        if (!written(c.id, x.id) || x.kind === 'homework') continue;
        const D = await loadSet(c.id, x.id);
        if (!D) continue;
        if (x.kind === 'lesson') out.push(...quizItems(D, c.id, x.id));
        else out.push(...setItems(D, c.id, x.id).filter(it => (it.difficulty || 2) <= 3));
      }
    }
    return out;
  };
  const weeklyProbs = async () => {
    if (!weeklyEligible()) return [];
    const week = weekKey(), f = weeklyFlag();
    const all = await topicPool(WEEKLY_TOPIC);
    if (!all.length) return [];
    const byUid = new Map(all.map(x => [x.uid, x]));
    if (f && f.week === week && Array.isArray(f.ids) && f.ids.length && f.ids.every(u => byUid.has(u))) return f.ids.map((u, i) => Object.assign({}, byUid.get(u), { weekly: { week, index: i } }));
    /* New week: prefer items from finished lessons, then the rest of the topic; the same picks all week */
    const done = new Set(finished().map(x => `${x.course}/${x.lesson}`));
    const rng = rngFrom(hash(week));
    const shuffled = all.map(x => ({ x, k: rng() })).sort((a, b) => a.k - b.k).map(o => o.x);
    const first = shuffled.filter(x => done.has(x.group)), rest = shuffled.filter(x => !done.has(x.group));
    const picks = interleave(first.concat(rest).slice(0, WEEKLY_N));
    try { S().flags.set({ weeklyProbs: { week, done: 0, ids: picks.map(x => x.uid) } }); } catch (e) { console.error(e); }
    return picks.map((x, i) => Object.assign({}, x, { weekly: { week, index: i } }));
  };

  /* ---------- Cumulative weekly review (ENGINE-BACKLOG 820 to 829; author and learner side docs/AUTHORING.md section 16) ----------
     ZQ.select.cumulativeStatus()          { eligible, due, dueAt, overdueDays, postponedToday, last, count } for Today (no loading)
     ZQ.select.weeklyReview({ n, seed })   the 20 items of the week's review, resolved for ZQ.player.runSet (async)
     ZQ.select.weeklyFinish(items, res, { partial })   records the result (history row, misses to the redo queue, skill scores, family counts)
     ZQ.select.cumulative.build(model, { n, seed, cap })   the selection itself, pure (tools/test-cumulative.mjs)
   The rules, in order. Tier 1: generated items from the Fluency families of the lessons of every met level, the families with more
   wrong answers and older last practice more likely. Tier 2: authored items the learner has never seen (bank items and the items of
   topic exams not yet sat, on a course that has a met level). Tier 3: authored review items (the quiz and level review items of met
   levels, never long-form or code) least recently seen first. At most four items from one course; the cap relaxes (4, 6, 8, ...) only
   when too few courses are met to fill the set. Consecutive items come from different courses when that can be avoided. With no
   Fluency sets written it is tiers 2 and 3 alone. */
  const CUM_N = 20, CUM_CAP = 4, CUM_LEVELS = 12;
  const lvKey = (cid, n) => `${cid}/L${n}`;
  const cumulativeStatus = () => {
    try {
      const st = S().cumulative.status();
      return Object.assign({ eligible: st.dueAt != null }, st);
    } catch (e) { console.warn(e); return { eligible: false, due: false, dueAt: null, overdueDays: 0, postponedToday: false, last: null, count: 0 }; }
  };
  /* Every level the learner has met that has something written, as { course, n, key, lessons, review } */
  const metLevels = () => {
    const out = [];
    let courses = [];
    try { courses = C().allCourses(); } catch { courses = []; }
    const P = Z.prereq;
    courses.forEach(c => (c.levels || []).forEach(lv => {
      let met = false;
      try { met = P ? !!P.levelMet(c.id, lv.n) : !!(S().prereq.get().met || {})[lvKey(c.id, lv.n)]; } catch { met = false; }
      if (met) out.push({ course: c.id, n: lv.n, key: lvKey(c.id, lv.n), lessons: (lv.lessons || []).filter(l => written(c.id, l)), review: lv.review && written(c.id, lv.review) ? lv.review : null });
    }));
    return out.filter(l => l.lessons.length || l.review);
  };
  const skillOwners = () => { const m = {}; try { C().allCourses().forEach(c => Object.keys(c.skills || {}).forEach(s => { m[s] = c.id; })); } catch { /* none */ } return m; };
  const practiceKind = (q) => !(q.kind === 'longform' || (q.widget && (q.widget.kind === 'longform' || q.widget.kind === 'code')) || (Array.isArray(q.parts) && q.parts.some(p => p && p.widget && (p.widget.kind === 'longform' || p.widget.kind === 'code'))));
  const gen = () => { if (!Z.gen) throw new Error('ZQ.gen is not loaded'); return Z.gen; };

  /* The pure selection. model: { levels: [{ course, n, key }], families: [{ course, n, set, family, right, wrong, lastAt }],
       unseen: [{ uid, course, n, item }], review: [{ uid, course, n, item, lastSeen }], now }. Returns entries in the order to be played:
       { tier: 1, course, n, uid, gen, set } for a generated item, { tier: 2 or 3, course, n, uid, item } for an authored one. */
  const cumBuild = (model, { n = CUM_N, seed = 0, cap = CUM_CAP } = {}) => {
    const rng = rngFrom(hash(`weekly|${seed}`)), t = model.now || now();
    const picks = [], perCourse = {}, uids = new Set(), prompts = new Set();
    const room = (course, cp) => (perCourse[course] || 0) < cp;
    const take = (e) => { picks.push(e); perCourse[e.course] = (perCourse[e.course] || 0) + 1; uids.add(e.uid); };
    const fam = (model.families || []).map(f => Object.assign({}, f, { times: 0, dead: false }));
    const weightOfFam = (f) => {
      const wrongRate = ((f.wrong || 0) + 0.5) / ((f.right || 0) + (f.wrong || 0) + 1);          // more wrong answers, more weight
      const days = f.lastAt ? Math.max(0, (t - f.lastAt) / DAY) : 60;                              // older last practice, more weight (never practised counts as 60 days)
      return (0.15 + wrongRate) * (0.5 + Math.min(4, days / 14)) / (1 + f.times);
    };
    const unseen = (model.unseen || []).slice(), review = (model.review || []).slice();
    const shuffled = (list) => list.map(x => ({ x, k: rng() })).sort((a, b) => a.k - b.k).map(o => o.x);
    for (let cp = cap; picks.length < n && cp <= cap + 40; cp += 2) {
      /* tier 1: generated items */
      let guard = 0;
      while (picks.length < n && guard++ < 400) {
        const open = fam.filter(f => room(f.course, cp) && !f.dead);
        if (!open.length) break;
        const ws = open.map(weightOfFam), tot = ws.reduce((a, b) => a + b, 0);
        let r = rng() * tot, f = open[open.length - 1];
        for (let i = 0; i < open.length; i++) { r -= ws[i]; if (r <= 0) { f = open[i]; break; } }
        const it = gen().draw(f.family, rngFrom(hash(`weekly|${seed}|${picks.length}|${f.set.id}|${f.family.id}|${f.times}`)), { avoid: prompts });
        if (it.rejected) { f.dead = true; continue; }
        prompts.add(it.prompt); f.times++;
        take({ tier: 1, course: f.course, n: f.n, uid: `fluency/${f.course}/${f.set.id}/${f.family.id}#${picks.length}`, gen: it, set: f.set });
      }
      /* tiers 2 and 3: authored; each is taken one course at a time, the course with the fewest picks first */
      const fromTier = (tier, list, order) => {
        const queues = new Map();
        order(list.filter(x => !uids.has(x.uid))).forEach(x => { const q = queues.get(x.course) || []; q.push(x); queues.set(x.course, q); });
        while (picks.length < n) {
          const next = [...queues.entries()].filter(([c, q]) => q.length && room(c, cp)).sort((a, b) => (perCourse[a[0]] || 0) - (perCourse[b[0]] || 0))[0];
          if (!next) break;
          const x = next[1].shift();
          take({ tier, course: x.course, n: x.n, uid: x.uid, item: x.item });
        }
      };
      fromTier(2, unseen, shuffled);
      fromTier(3, review, (list) => shuffled(list).sort((a, b) => (a.lastSeen || 0) - (b.lastSeen || 0)));
    }
    /* play order: no two neighbours from one course when another is available */
    const by = new Map(), out = [];
    picks.forEach(x => { const q = by.get(x.course) || []; q.push(x); by.set(x.course, q); });
    while (out.length < picks.length) {   // from the course with the most items left that is not the last one played (so none is stranded at the end)
      const prev = out.length ? out[out.length - 1].course : null;
      const open = [...by.entries()].filter(([, q]) => q.length), next = open.filter(([c]) => c !== prev).sort((a, b) => b[1].length - a[1].length)[0] || open[0];
      out.push(next[1].shift());
    }
    return out;
  };

  /* The model from the live save and content (loads what the selection needs: fluency sets, bank files, topic exams, at most CUM_LEVELS levels) */
  const cumModel = async () => {
    const levels = metLevels(), t = now(), cumRec = (() => { try { return S().cumulative; } catch { return null; } })();
    const seen = cumRec ? cumRec.seen() : {}, history = cumRec ? cumRec.history() : [];
    const metCourses = new Set(levels.map(l => l.course)), owners = skillOwners();
    const lowest = (cid) => (levels.filter(l => l.course === cid).sort((a, b) => a.n - b.n)[0] || {}).n;
    /* tier 1 */
    const families = [];
    let fl = [];
    try { fl = C().fluencyList ? C().fluencyList() : []; } catch { fl = []; }
    for (const row of fl) {
      const lv = levels.find(l => l.course === row.course && l.lessons.includes(row.lesson));
      if (!lv) continue;
      const doc = await safe(C().fluencySet(row.course, row.id));
      if (!doc || !Array.isArray(doc.families)) continue;
      let rec = null; try { rec = S().fluency.get(row.course, row.id); } catch { rec = null; }
      doc.families.forEach(f => { if (Z.gen && Z.gen.checkFamily(f).length) return; const r = (rec && rec.families && rec.families[f.id]) || {}; families.push({ course: row.course, n: lv.n, set: doc, family: f, right: r.right || 0, wrong: r.wrong || 0, lastAt: r.lastAt || 0 }); });
    }
    /* tier 2 */
    const unseen = [];
    const courseOfItem = (it) => { const s = (it.skills || []).find(x => owners[x]); return s ? owners[s] : null; };
    try {
      for (const id of (C().bankIds ? C().bankIds() : [])) {
        const D = await safe(C().bank(id));
        ((D && D.items) || []).forEach(it => {
          if (!it || !it.id || !practiceKind(it)) return;
          const b = bankItem(it, id, D), cid = courseOfItem(b);
          if (!cid || !metCourses.has(cid) || !lessonsDone(it.requires) || entryOf(b.uid) || seen[b.uid]) return;
          unseen.push({ uid: b.uid, course: cid, n: lowest(cid), item: b });
        });
      }
      const topics = new Set(levels.map(l => { const c = courseOf(l.course); return c && c.topic; }).filter(Boolean));
      for (const tp of topics) {
        const id = `topic-${tp}`, rec = ((S() && S().exams) || {})[id];
        if (rec && Array.isArray(rec.attempts) && rec.attempts.length) continue;   // sat: its items are seen
        const E = await safe(C().exam(id));
        if (!E) continue;
        const all = (E.items || []).concat(...(Array.isArray(E.parts) ? E.parts : []).filter(p => p && p.kind === 'paper').map(p => p.items || []));
        all.forEach(it => {
          if (!it || it.id == null || !practiceKind(it)) return;
          const cid = courseOfItem(it), uid = `${id}/${it.id}`;
          if (!cid || !metCourses.has(cid) || seen[uid]) return;
          const out = Object.assign({}, it, { ref: { exam: id, item: it.id }, uid, source: source({ exam: id }), group: id, skills: it.skills || [] });
          delete out.hints;
          unseen.push({ uid, course: cid, n: lowest(cid), item: out });
        });
      }
    } catch (e) { console.warn(e); }
    /* tier 3: the quiz and level review items of the levels least recently covered by a weekly review */
    const covered = {}; history.forEach(h => (h.levels || []).forEach(k => { covered[k] = Math.max(covered[k] || 0, h.at || 0); }));
    const order = levels.slice().sort((a, b) => (covered[a.key] || 0) - (covered[b.key] || 0) || (a.key < b.key ? -1 : 1)).slice(0, CUM_LEVELS);
    const review = [], sat = (S() && S().reviews) || {}, rc = recent.get();
    const lastOf = (it) => Math.max(seen[it.uid] || 0, rc[it.uid] || 0) || ((sat[`${it.ref.course}/${it.ref.lesson}`] || {}).at || 0) || Math.min(...(it.skills.length ? it.skills : ['_']).map(s => (skillRec(s) && skillRec(s).lastAt) || 0));
    for (const lv of order) {
      const add = (items) => items.filter(practiceKind).forEach(it => review.push({ uid: it.uid, course: lv.course, n: lv.n, item: it, lastSeen: lastOf(it) }));
      for (const l of lv.lessons) add(quizItems(await loadSet(lv.course, l), lv.course, l));
      if (lv.review) add(setItems(await loadSet(lv.course, lv.review), lv.course, lv.review));
    }
    const dup = new Set(unseen.map(u => u.uid));
    return { now: t, levels, families, unseen, review: review.filter(r => !dup.has(r.uid)) };
  };
  /* A selection entry as an item for ZQ.player.runSet */
  const cumItem = (e, k) => {
    const name = (courseOf(e.course) || {}).name || e.course;
    if (e.tier === 1) {
      const it = gen().playerItem(e.gen, e.set, k);
      return Object.assign(it, { uid: e.uid, id: e.uid, group: e.course, source: `${name} · Fluency`, weekly: { tier: 1, course: e.course, n: e.n, set: e.set.id, family: e.gen.family } });
    }
    return Object.assign({}, e.item, { group: e.course, weekly: { tier: e.tier, course: e.course, n: e.n } });
  };
  const weeklyReview = async ({ n = CUM_N, seed } = {}) => {
    const model = await cumModel();
    const items = [];
    items.metKeys = model.levels.map(l => l.key);
    if (!model.levels.length) return items;
    cumBuild(model, { n, seed: seed != null ? seed : (Math.random() * 4294967296) >>> 0 }).forEach((e, k) => items.push(cumItem(e, k)));
    return items;
  };
  /* Record a finished (or, with partial, a left) weekly review. res[j] is the result of items[j] (undefined: not answered). Misses of authored
     items join the redo queue (the same entries a review miss makes); a generated miss only moves the family counts, since a generated
     question cannot be asked again. Answered authored items move the skill scores as a practice set does. */
  const weeklyFinish = (items, res, { partial = false } = {}) => {
    const byLevel = {}, fams = {}, seenUids = [], rows = [];
    let right = 0, fluency = 0, authored = 0, answered = 0, queued = 0;
    items.forEach((it, j) => {
      const r = res[j]; if (!r || !it.weekly) return;
      answered++;
      const w = it.weekly, key = lvKey(w.course, w.n);
      if (r.ok) right++; else byLevel[key] = (byLevel[key] || 0) + 1;
      if (w.tier === 1) {
        fluency++;
        const x = fams[`${w.course}/${w.set}`] || (fams[`${w.course}/${w.set}`] = {}), f = x[w.family] || (x[w.family] = [0, 0]);
        f[r.ok ? 0 : 1]++;
      } else {
        authored++; seenUids.push(it.uid);
        rows.push({ id: it.id, ok: !!r.ok, difficulty: it.difficulty || 2, skills: it.skills || [], ref: it.ref });
        if (!r.ok && it.ref) {
          const kind = it.ref.exam ? 'exam' : it.ref.bank ? 'bank' : 'quiz';
          try { S().redo.add({ id: it.uid, kind, ref: it.ref, skills: it.skills || [], difficulty: it.difficulty || 3 }); queued++; } catch (e) { console.error(e); }
        }
      }
    });
    Object.entries(fams).forEach(([k, families]) => { const [course, ...rest] = k.split('/'); try { S().fluency.result({ course, id: rest.join('/'), families, partial: true }); } catch (e) { console.error(e); } });
    try { if (rows.length) S().practiceResult({ results: rows, source: 'weekly-review' }); } catch (e) { console.error(e); }
    const row = S().cumulative.record({ score: right, n: items.length, byLevel, levels: items.metKeys || [], fluency, authored, seen: seenUids, partial: partial || answered < items.length });
    return { right, byLevel, row, fluency, authored, queued, missed: answered - right };
  };

  Z.select = { practiceSet, redoSession, bankDeck, bankStatus, weeklyProbs, weeklyStatus, weeklyRecord, resolve, source, pool, interval, LEITNER,
    cumulativeStatus, weeklyReview, weeklyFinish, metLevels, cumulative: { build: cumBuild, model: cumModel } };
})();
