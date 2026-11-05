/* Prerequisite gating (ENGINE-BACKLOG 481 to 490; brief docs/briefs/prereq-gating.md; author side docs/AUTHORING.md section 11).
   Pure rules, no screens: which levels and lessons are locked, what is missing, what "Start here" is, and the test-out
   and Refresh facts. ZQ.prereq reads course.json (via ZQ.content) and the saved state (ZQ.state), never writes except
   through ZQ.state.prereq (met levels, test-out attempts, levels opened early).

   Data. A level in course.json may carry requires: ["<course>/L<n>", "<course>/<lesson-id>", ...] (a level reference means
   the whole level). A first level with no requires is open; a later level with no requires implicitly requires the
   previous level of its own course. course.json may also carry lessonRequires: { "<lesson-id>": [refs] }, which replaces
   the level's list for that one lesson. Topics and stages carry no requires.

   Met. A level is met when: its review has a passed attempt (state.reviews[...].passed), its topic exam is passed, the
   stage exit test of its stage is passed, a test-out passed, it was recorded met (grandfathering, test hook), or it has
   no review written and every lesson on its map is written and finished. A lesson reference is met when that lesson is
   done and its quiz mastered, or its level is met. Opening a lesson never counts. A met level stays met: sync() records
   every level found met in state.prereq.met, so nothing that was unlocked locks again. A met level is also open as a place
   to work (its lessons, review and homework), even when its own references are unmet: it was met by mastery shown. Lessons
   already done, reviews or levels opened early, and levels the learner has started (a finished lesson, state.prereq.started,
   not counted as met for dependants) are never locked either. */
(function () {
  'use strict';
  const DAY = 86400000;
  const PASS = 0.8;            // review pass share when a review file carries no pass (matches the quiz MASTERY bar; rule 1)
  const SKILL_FLOOR = 0.7;     // share every essential skill of a level needs in a review, test-out or exam pass to meet it (rules 2 and 4); state.js holds the same figure for the finish-time check
  const TESTOUT_N = 6;         // items in a test-out
  const RETAKE_H = 24;         // hours before a failed test-out can be retaken
  const REFRESH_D = 30;        // days after which a met prerequisite shows a Refresh chip

  const C = () => window.ZQ.content;
  const S = () => window.ZQ.state;
  const rec = () => { try { return S().prereq.get(); } catch { return { met: {}, testouts: {}, opened: {}, started: {} }; } };
  const keyOfLevel = (cid, n) => `${cid}/L${n}`;
  const strict = () => { try { return S().settings.strictPrereqs !== false; } catch { return true; } };

  const parse = (ref) => {
    const m = /^([^/]+)\/(.+)$/.exec(String(ref));
    if (!m) return null;
    return /^L\d+$/.test(m[2]) ? { kind: 'level', course: m[1], n: +m[2].slice(1) } : { kind: 'lesson', course: m[1], id: m[2] };
  };
  const doc = (cid) => { try { return C().course(cid); } catch { return null; } };
  const levelsOf = (cid) => ((doc(cid) || {}).levels || []);
  const levelOf = (cid, n) => levelsOf(cid).find(l => l.n === n) || null;
  /* The level that holds a lesson, review or homework id */
  const levelHolding = (cid, id) => levelsOf(cid).find(l => (l.lessons || []).includes(id) || l.review === id || l.homework === id) || null;
  const writtenLessons = (cid, lv) => (lv.lessons || []).filter(id => C().exists(cid, id) !== false);

  /* Curriculum order: stage, topic, course, level */
  let ordMap = null;
  const ordOf = (cid, n = 0) => {
    if (!ordMap) {
      ordMap = {};
      C().allStages().forEach((s, si) => s.topics.forEach((t, ti) => (t.courses || []).forEach((id, ci) => { ordMap[id] = [si, ti, ci]; })));
    }
    const o = ordMap[cid] || [99, 99, 99];
    return o[0] * 1e7 + o[1] * 1e5 + o[2] * 1e3 + n;
  };

  /* ---------- What a level or lesson requires ---------- */
  const levelRefs = (cid, n) => {
    const lv = levelOf(cid, n);
    if (!lv) return [];
    if (Array.isArray(lv.requires)) return lv.requires;
    const ls = levelsOf(cid), i = ls.indexOf(lv);
    return i > 0 ? [keyOfLevel(cid, ls[i - 1].n)] : [];
  };
  const lessonRefs = (cid, lid) => {
    const d = doc(cid) || {};
    if (d.lessonRequires && Array.isArray(d.lessonRequires[lid])) return d.lessonRequires[lid];
    const lv = levelHolding(cid, lid);
    return lv ? levelRefs(cid, lv.n) : [];
  };

  /* ---------- Met ---------- */
  /* Met reads only the auto and external part of a pass (N01); the one rule, with its old-attempt fallback, is ZQ.content.examPassedAuto */
  const examPassedAuto = (id) => C().examPassedAuto(id);
  const examPassedAt = (id) => C().examPassedAt(id);
  const reviewRec = (cid, lv) => { try { return lv.review ? S().reviews[`${cid}/${lv.review}`] || null : null; } catch { return null; } };
  /* Rule 2: the essential skills of a level are the skills tagged on its review's items; each needs a skill record that has been seen */
  const essentialsOf = (cid, lv) => {
    if (!lv.review) return null;
    const known = C().essentialSkills(cid, lv.review), r = reviewRec(cid, lv);
    return known || (r && Array.isArray(r.essential) ? r.essential : null);
  };
  const seenAll = (skills) => { try { const k = S().skills; return skills.every(s => k[s] && k[s].seen > 0); } catch { return false; } };
  const reviewPassed = (cid, lv) => {
    const r = reviewRec(cid, lv);
    if (!r) return false;
    if (typeof r.passedAuto === 'boolean') return r.passedAuto && (!Array.isArray(r.essential) || seenAll(r.essential));   // self-marked rows left out; passedAuto holds the skill floor from the attempt itself
    if (typeof r.passed === 'boolean') return r.passed;           // a record from before provenance: level reviews hold no self-marked item
    return Number(r.items) > 0 && Number(r.score) / Number(r.items) >= PASS;   // a record from before this pass
  };
  const lessonRec = (cid, id) => { try { return S().lessons[`${cid}/${id}`] || null; } catch { return null; } };
  const lessonFinished = (cid, id) => { const r = lessonRec(cid, id); return !!(r && r.done); };   // finished, however it was done: never locks, opens the level
  const lessonDone = (cid, id) => { const r = lessonRec(cid, id); return !!(r && S().lessonCounts(r)); };   // finished and not over the reveal cap (rule 3): counts for prerequisites and progress
  /* every lesson on the map is written and finished (a half-written level never counts as complete) */
  const fullyFinished = (cid, lv) => { const all = lv.lessons || [], ws = writtenLessons(cid, lv); return all.length > 0 && ws.length === all.length && ws.every(id => lessonDone(cid, id)); };
  /* Rule 4: a topic or stage exam pass meets a level only when one passing attempt covers every essential skill of the level at SKILL_FLOOR over its auto rows;
     otherwise the pass is a badge for that level. A level whose essentials are not known yet (its review not loaded) is not met by an exam until they are. */
  const examMeets = (examId, cid, lv) => {
    const ess = essentialsOf(cid, lv);
    if (!ess || !ess.length || !seenAll(ess)) return false;
    return C().examAutoAttempts(examId).some(a => S().floorGaps(a.bySkillAuto || a.bySkill || {}, ess, SKILL_FLOOR).length === 0);
  };
  /* Performance task (ENGINE-BACKLOG 529): a level whose manifest row names a task needs it passed as well. The record is state.perf["course/L<n>"],
     written when a homework or review row for the task comes back ok (how: auto, self or external). An extra AND on every route except a grandfathered record. */
  const perfNeeded = (cid, lv) => { try { return C().perfOf(cid, lv.n) || null; } catch { return null; } };
  const perfRec = (cid, lv) => { try { return (S().perf.get() || {})[keyOfLevel(cid, lv.n)] || null; } catch { return null; } };
  const perfPassed = (cid, lv) => !perfNeeded(cid, lv) || !!perfRec(cid, lv);
  /* met by something other than a record in state.prereq.met */
  const derivedMet = (cid, lv) => perfPassed(cid, lv) && derivedMetBase(cid, lv);
  const derivedMetBase = (cid, lv) => {
    if (reviewPassed(cid, lv)) return true;
    const co = doc(cid);
    if (co && co.topic && examPassedAuto('topic-' + co.topic) && examMeets('topic-' + co.topic, cid, lv)) return true;
    if (co && co.stage != null && examPassedAuto('stage-' + co.stage) && examMeets('stage-' + co.stage, cid, lv)) return true;
    if (!lv.review || C().exists(cid, lv.review) === false) return fullyFinished(cid, lv);
    return false;
  };
  const levelMet = (cid, n) => {
    const lv = levelOf(cid, n);
    if (!lv) return true;                         // an unknown reference never blocks (the validator reports it)
    const m = rec().met[keyOfLevel(cid, n)];
    if (m && (m.how !== 'testout' || perfPassed(cid, lv))) return true;   // a test-out pass is a badge until the performance task is passed
    return derivedMet(cid, lv);
  };
  const lessonMet = (cid, id) => {
    const r = lessonRec(cid, id);
    if (r && S().lessonCounts(r) && r.mastered) return true;
    const lv = levelHolding(cid, id);
    return lv ? levelMet(cid, lv.n) : true;
  };
  const refMet = (ref) => {
    const p = parse(ref);
    if (!p) return true;
    return p.kind === 'level' ? levelMet(p.course, p.n) : lessonMet(p.course, p.id);
  };

  /* ---------- Advisory edges (readiness contract, DECISIONS "Readiness contract sign-off") ----------
     Under Strict, a reference into a course that is optional for the profile's role (content/readiness.json) is advisory:
     it never locks, and the level or lesson shows it as a note. Undecided, or no readiness file, keeps every edge blocking. */
  const roleNow = () => { try { const R = C().readiness; return R ? R.roleKey(S().profile.get().track) : 'undecided'; } catch { return 'undecided'; } };
  const advisory = (ref) => {
    if (!strict()) return false;
    const p = parse(ref), role = roleNow();
    if (!p || role === 'undecided') return false;
    try { return C().readiness.status(p.course, role) === 'optional'; } catch { return false; }
  };
  const blocking = (refs) => refs.filter(r => !advisory(r));

  /* ---------- Locked ---------- */
  const openedEarly = (cid, n) => !!rec().opened[keyOfLevel(cid, n)];
  const startedLevel = (cid, n) => !!(rec().started || {})[keyOfLevel(cid, n)];
  /* A level that is met, opened early or started is open as a place to work, whatever its own references say */
  const levelLocked = (cid, n) => !openedEarly(cid, n) && !startedLevel(cid, n) && !levelMet(cid, n) && blocking(levelRefs(cid, n)).some(r => !refMet(r));
  const lessonLocked = (cid, lid) => {
    if (lessonFinished(cid, lid)) return false;
    const lv = levelHolding(cid, lid);
    if (lv && (openedEarly(cid, lv.n) || startedLevel(cid, lv.n))) return false;
    const d = doc(cid) || {};
    const own = !!(d.lessonRequires && Array.isArray(d.lessonRequires[lid]));
    if (lv && !own && levelMet(cid, lv.n)) return false;
    return blocking(lessonRefs(cid, lid)).some(r => !refMet(r));
  };
  /* A lesson, review or homework id of a course map */
  const itemLocked = (cid, id) => {
    const lv = levelHolding(cid, id);
    if (!lv) return false;
    if ((lv.lessons || []).includes(id)) return lessonLocked(cid, id);
    try {
      if (lv.review === id && S().reviews[`${cid}/${id}`]) return false;
      if (lv.homework === id && S().homework[`${cid}/${id}`]) return false;
    } catch { /* fall through */ }
    return levelLocked(cid, lv.n);
  };
  /* A course is locked for the learner when its first startable lesson is locked */
  const courseLocked = (cid) => {
    const ls = C().courseLessons(cid).filter(x => x.kind === 'lesson' && x.written !== false);
    return ls.length > 0 && ls.every(x => lessonLocked(cid, x.id));
  };
  const examRefs = (d) => (d && Array.isArray(d.requires) ? d.requires : []);
  /* A mock names requires at the top of its file (levels or lessons, as on a level); it is locked while one is unmet, unless opened early */
  const examLocked = (id, d) => !rec().opened['exam/' + id] && examRefs(d).some(r => !refMet(r));

  /* ---------- What is missing ---------- */
  const testOutFacts = (cid, lv) => {
    const key = keyOfLevel(cid, lv.n), t = rec().testouts[key];
    const written = !!lv.review && C().exists(cid, lv.review) !== false;
    const nextAt = t && !t.passed ? t.at + RETAKE_H * 3600e3 : 0;
    return { can: written && !(nextAt > Date.now()), written, nextAt: nextAt > Date.now() ? nextAt : 0, tries: t ? t.tries || 0 : 0, missed: t && !t.passed ? t.missed || [] : [], seen: t && Array.isArray(t.seen) ? t.seen : [] };
  };
  const nodeOf = (ref) => {
    const p = parse(ref);
    if (!p) return null;
    const co = doc(p.course);
    if (!co) return null;
    const lv = p.kind === 'level' ? levelOf(p.course, p.n) : levelHolding(p.course, p.id);
    if (!lv) return null;
    const ws = writtenLessons(p.course, lv);
    const base = {
      ref, kind: p.kind, course: p.course, courseName: co.name, stage: co.stage, topic: co.topic, topicName: co.topicName, n: lv.n, levelName: lv.name || '',
      ord: ordOf(p.course, lv.n), review: lv.review || '', reviewPassed: reviewPassed(p.course, lv), reviewWritten: !!lv.review && C().exists(p.course, lv.review) !== false,
      lessonsTotal: (lv.lessons || []).length, lessonsWritten: ws.length, lessonsDone: ws.filter(id => lessonDone(p.course, id)).length,
      refs: p.kind === 'level' ? levelRefs(p.course, p.n) : lessonRefs(p.course, p.id),
      testOut: testOutFacts(p.course, lv),
      perf: perfNeeded(p.course, lv) ? { ...perfNeeded(p.course, lv), passed: perfPassed(p.course, lv) } : null,   // ENGINE-BACKLOG 529: the level's performance task and whether it is passed
    };
    if (p.kind === 'lesson') {
      const x = C().courseLessons(p.course).find(y => y.kind === 'lesson' && y.id === p.id);
      return { ...base, id: p.id, name: x ? x.name : C().deKebab(p.id), done: lessonDone(p.course, p.id) };
    }
    return base;
  };
  /* The first thing to do inside a missing node, or null: the first written lesson not done, else the review */
  const launchOf = (node) => {
    if (node.kind === 'lesson') return C().exists(node.course, node.id) === false ? null : { route: `lesson/${node.course}/${node.id}`, label: node.name };
    const lv = levelOf(node.course, node.n);
    const id = writtenLessons(node.course, lv).find(x => !lessonDone(node.course, x));
    if (id) { const x = C().courseLessons(node.course).find(y => y.id === id); return { route: `lesson/${node.course}/${id}`, label: x ? x.name : id }; }
    if (node.reviewWritten && !node.reviewPassed) return { route: `review/${node.course}/${node.review}`, label: `Level ${node.n} review` };
    return null;
  };
  /* The unmet references under a set of references. direct: the listed ones; indirect: what they need in turn.
     start: the earliest missing node whose own references are met and that has something to open. */
  const missingRefs = (refs) => {
    const seen = new Set(), direct = [], indirect = [];
    const nodeKey = (nd) => (nd.kind === 'lesson' ? nd.ref : keyOfLevel(nd.course, nd.n));
    /* two passes, so that direct and indirect do not depend on list order: every unmet listed reference is direct first */
    const add = (r, into) => {
      if (refMet(r)) return null;
      const nd = nodeOf(r);
      if (!nd) return null;
      const k = nodeKey(nd);
      if (seen.has(k)) return null;
      seen.add(k); into.push(nd);
      return nd;
    };
    const walk = (nd) => blocking(nd.refs).forEach(r => { const x = add(r, indirect); if (x) walk(x); });
    blocking(refs).forEach(r => add(r, direct));
    direct.slice().forEach(walk);
    const byOrd = (a, b) => a.ord - b.ord;
    direct.sort(byOrd); indirect.sort(byOrd);
    const all = direct.concat(indirect).sort(byOrd);
    let start = null;
    for (const nd of all) {
      if (blocking(nd.refs).some(r => !refMet(r))) continue;
      const l = launchOf(nd);
      if (l) { start = { node: nd, ...l }; break; }
    }
    return { direct, indirect, start, count: direct.length + indirect.length };
  };
  /* Advisory references still unmet for a lesson or level: nodes to show as a note, never as a lock */
  const advisoryNodes = (refs) => refs.filter(r => advisory(r) && !refMet(r)).map(nodeOf).filter(Boolean);
  const advisoryFor = (cid, id) => advisoryNodes(lessonRefs(cid, id));
  const advisoryForLevel = (cid, n) => advisoryNodes(levelRefs(cid, n));
  const missingFor = (cid, id) => missingRefs(lessonRefs(cid, id));
  const missingForLevel = (cid, n) => missingRefs(levelRefs(cid, n));

  /* ---------- Refresh: a met prerequisite not reviewed for 30 days ---------- */
  const lastTouch = (cid, lv) => {
    const key = keyOfLevel(cid, lv.n), r = reviewRec(cid, lv), p = rec(), t = p.testouts[key];
    const co = doc(cid) || {};
    return Math.max(r ? Number(r.at) || 0 : 0, t && t.passed ? Number(t.at) || 0 : 0, p.met[key] ? Number(p.met[key].at) || 0 : 0,
      co.topic ? examPassedAt('topic-' + co.topic) : 0, co.stage != null ? examPassedAt('stage-' + co.stage) : 0);
  };
  /* [{ course, n, review, days }] for the level references of a lesson that are met but stale and have a written review */
  const refreshFor = (cid, lid) => lessonRefs(cid, lid).map(parse).filter(p => p && p.kind === 'level').map(p => {
    const lv = levelOf(p.course, p.n);
    if (!lv || !lv.review || C().exists(p.course, lv.review) === false || !levelMet(p.course, p.n)) return null;
    const last = lastTouch(p.course, lv);
    const days = last ? Math.floor((Date.now() - last) / DAY) : 999;
    return days >= REFRESH_D ? { course: p.course, n: p.n, review: lv.review, days, name: `${(doc(p.course) || {}).name || p.course}, level ${p.n}` } : null;
  }).filter(Boolean);

  /* ---------- Recording (grandfathering, persisting what is met) ---------- */
  const allLevels = () => C().allCourses().flatMap(c => (c.levels || []).map(lv => ({ course: c.id, lv })));
  let syncing = false;
  const preloaded = new Set();   // courses whose review skills were requested for rule 4
  const sync = () => {
    if (syncing || !S() || !C() || !C().curriculum) return;
    syncing = true;
    try {
      const p = rec();
      if (!p.grandfathered) {
        const keys = allLevels().filter(({ course, lv }) => fullyFinished(course, lv)).map(({ course, lv }) => keyOfLevel(course, lv.n));
        S().prereq.grandfather(keys);
      }
      /* a level with a finished lesson is work in progress: its remaining lessons, review and homework stay open (never counted as met) */
      const begun = allLevels().filter(({ course, lv }) => !(p.started || {})[keyOfLevel(course, lv.n)] && (lv.lessons || []).some(id => lessonFinished(course, id))).map(({ course, lv }) => keyOfLevel(course, lv.n));
      if (begun.length) S().prereq.start(begun);
      /* levels of a course whose topic or stage exam is passed need their reviews' skills (rule 4); load them, then look again */
      const need = C().allCourses().filter(c => !preloaded.has(c.id) && ((c.topic && examPassedAuto('topic-' + c.topic)) || (c.stage != null && examPassedAuto('stage-' + c.stage)))).map(c => c.id);
      if (need.length) { need.forEach(id => preloaded.add(id)); Promise.all(need.map(id => C().loadEssentials(id))).then(() => sync()).catch(() => {}); }
      const fresh = allLevels().filter(({ course, lv }) => !p.met[keyOfLevel(course, lv.n)] && derivedMet(course, lv)).map(({ course, lv }) => keyOfLevel(course, lv.n));
      if (fresh.length) S().prereq.mark(fresh, 'derived');
    } catch (e) { console.error(e); }
    syncing = false;
  };

  /* Playthrough and test hook: mark every prerequisite of a lesson, level, review or homework met. Returns how many levels it marked. */
  const unlock = (cid, id) => {
    const lv = levelHolding(cid, id);
    const m = lv && (lv.lessons || []).includes(id) ? missingFor(cid, id) : lv ? missingForLevel(cid, lv.n) : { direct: [], indirect: [] };
    const keys = [...new Set(m.direct.concat(m.indirect).map(nd => keyOfLevel(nd.course, nd.n)))];
    if (keys.length) S().prereq.mark(keys, 'test');
    return keys.length;
  };
  const unlockRefs = (refs) => {
    const m = missingRefs(refs || []);
    const keys = [...new Set(m.direct.concat(m.indirect).map(nd => keyOfLevel(nd.course, nd.n)))];
    if (keys.length) S().prereq.mark(keys, 'test');
    return keys.length;
  };

  const api = {
    strict, parse, levelRefs, lessonRefs, examRefs, examLocked, perfNeeded, perfPassed, perfRec, levelMet, lessonMet, refMet, levelLocked, lessonLocked, itemLocked, courseLocked, openedEarly, startedLevel,
    advisory, advisoryFor, advisoryForLevel, missingFor, missingForLevel, missingRefs, nodeOf, launchOf, testOutFacts, refreshFor, sync, unlock, unlockRefs, levelHolding, keyOfLevel,
    openedCount: () => Object.keys(rec().opened).length,
    PASS, SKILL_FLOOR, TESTOUT_N, RETAKE_H, REFRESH_D,
  };
  window.ZQ = window.ZQ || {};
  window.ZQ.prereq = api;
  const start = () => { sync(); window.ZQ.on('state', (e) => { if (e && e.what !== 'prereq') sync(); }); };
  if (window.ZQ.content && window.ZQ.content.ready) window.ZQ.content.ready.then(start).catch(() => {});
})();
