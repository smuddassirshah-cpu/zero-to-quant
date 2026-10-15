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
    .filter(q => !practice || !(q.kind === 'longform' || (q.widget && (q.widget.kind === 'longform' || q.widget.kind === 'code')))) : []);

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

  /* ---------- Redo ---------- */
  const findIn = (list, id) => (list || []).find((x, i) => (x.id || 'q' + i) === id) || null;
  const resolve = async (ref = {}, kind = 'quiz') => {
    if (ref.exam) {
      const E = await safe(C().exam(ref.exam)); if (!E) return null;
      const all = (E.items || []).concat(...(E.parts || []).map(p => p.items || []));
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

  Z.select = { practiceSet, redoSession, weeklyProbs, weeklyStatus, weeklyRecord, resolve, source, pool, interval, LEITNER };
})();
