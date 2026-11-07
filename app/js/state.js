/* Learner state (docs/PLAN.md section 6). One versioned JSON document in localStorage['zq.state'].
   Screens read through getters and change it only through the typed mutators below; every mutator saves
   (debounced 200ms, flushed on pagehide) and emits 'state' on ZQ's event bus.
   Rules enforced here: XP and MP (design-research 6.2), mastery at 80%, the redo queue (7 days, then 30, then out;
   a miss resets to 7), the streak (3 graded problems or 1 finished lesson, quiz, review or homework; one rest day per
   7 qualifying days, at most 2 held, used automatically on a missed day), hours by block, export and import.
   All dates are local. A day key is 'YYYY-MM-DD'; weeks start on Monday. */
(function () {
  'use strict';
  const KEY = 'zq.state';
  const V = 1;
  const DAY = 86400000;
  const K = 32;                         // Elo K factor
  const ELO_START = 1200;               // PLAN section 6 schema
  const MASTERY = 0.8;                  // lesson quiz share that marks a lesson mastered
  const REVIEW_PASS = 0.8;              // review pass share when a review file carries no pass (matches MASTERY); met rule 1
  const SKILL_FLOOR = 0.7;              // per-skill share every essential skill of a level needs for a review, test-out or exam pass to meet it (rules 2, 4)
  const REVEAL_CAP = 0.25;              // share of a lesson's gradable screens that may be revealed (Solve) before it stops counting as done (rule 3)
  const REDO_FIRST = 7, REDO_SECOND = 30;
  const REST_EVERY = 7, REST_MAX = 2;
  const QUALIFY_PROBLEMS = 3;
  const BLOCKS = ['main', 'build', 'review', 'mental'];
  const TRACKS = ['Trader', 'Researcher', 'Developer', 'Strats', 'Undecided'];
  const GOALS = [5, 10, 15, 25];
  const XP = { first: 15, retry: 5, lesson: 20, perfect: 15, quizItem: 15, homework: 50, homeworkItem: 5, topicExam: 200, stageExam: 1000 };

  /* ---------- Clock and date helpers (written once; screens use ZQ.state.dates) ---------- */
  let clock = () => Date.now();
  const now = () => clock();
  const pad = (n) => String(n).padStart(2, '0');
  const keyOf = (d) => `${d.getFullYear()}-${pad(d.getMonth() + 1)}-${pad(d.getDate())}`;
  const parseKey = (k) => { const [y, m, d] = String(k).split('-').map(Number); return new Date(y, m - 1, d); };
  const todayKey = (t) => keyOf(new Date(t == null ? now() : t));
  const addDays = (k, n) => { const d = parseKey(k); d.setDate(d.getDate() + n); return keyOf(d); };
  const daysBetween = (a, b) => Math.round((parseKey(b) - parseKey(a)) / DAY); // whole local days, DST safe
  const weekStart = (t) => { const d = new Date(t == null ? now() : t); d.setHours(0, 0, 0, 0); d.setDate(d.getDate() - ((d.getDay() + 6) % 7)); return keyOf(d); };
  const dates = { todayKey, weekStart, addDays, daysBetween, parseKey, keyOf };

  /* ---------- The document ---------- */
  const fresh = () => ({
    v: V,
    profile: { name: '', initial: '', track: 'Undecided', weeklyGoalH: 15, startStage: 0, createdAt: null },
    settings: { theme: 'system', motion: 'system', sound: false, haptics: true, streakMode: 'daily', quantOnly: false, strictPrereqs: true },
    xp: 0, mp: 0,
    lessons: {}, reviews: {}, homework: {}, exams: {}, skills: {}, selfMarked: {},   // selfMarked: per skill { seen, correct, lastAt } from self-ticked rows, never mixed into skills (provenance, N01)
    redo: [], notebook: [], drills: {}, drillSessions: [],
    bank: {}, timing: { families: {} },
    warmup: { history: [] },
    hours: [],
    streak: { current: 0, best: 0, lastDay: null, restDays: 0, restEarnedAt: 0, days: {}, count: { day: null, problems: 0 } },
    flags: { setupDone: false, streakGoal: null },
    perf: {},   // performance tasks passed (ENGINE-BACKLOG 529): "course/L<n>" -> { item, kind, how, at }; sticky, read by the met rule
    prereq: { met: {}, testouts: {}, opened: {}, started: {}, grandfathered: false },   // prerequisite gating (ENGINE-BACKLOG 481): levels recorded met, test-out attempts, levels opened early
  });
  const isObj = (x) => x && typeof x === 'object' && !Array.isArray(x);
  /* The skills below the floor: bySkill is { skill: [correct, total] } over auto rows; an essential skill that is absent or has no rows is below it */
  const floorGaps = (bySkill, essential, floor = SKILL_FLOOR) => (essential || []).filter(s => {
    const v = bySkill && bySkill[s];
    const [c, t] = Array.isArray(v) ? v : v == null ? [0, 0] : [v, v];
    return !(t > 0 && c / t >= floor - 1e-9);
  });
  /* Fill anything missing from a loaded or imported document with the defaults, one level deep, keeping unknown keys */
  const normalise = (raw) => {
    const d = fresh();
    if (!isObj(raw)) return d;
    for (const k of Object.keys(raw)) {
      if (isObj(d[k]) && isObj(raw[k]) && ['profile', 'settings', 'streak', 'flags', 'warmup', 'prereq'].includes(k)) d[k] = { ...d[k], ...raw[k] };
      else if (Array.isArray(d[k])) d[k] = Array.isArray(raw[k]) ? raw[k] : d[k];
      else if (isObj(d[k])) d[k] = isObj(raw[k]) ? raw[k] : d[k];
      else d[k] = raw[k];
    }
    if (!isObj(d.streak.days)) d.streak.days = {};
    if (!isObj(d.streak.count)) d.streak.count = { day: null, problems: 0 };
    if (!Array.isArray(d.warmup.history)) d.warmup.history = [];
    if (!isObj(d.timing.families)) d.timing.families = {};   // old saves have neither bank nor timing
    d.v = V;
    return d;
  };
  const read = () => {
    try { const s = localStorage.getItem(KEY); return s ? normalise(JSON.parse(s)) : fresh(); } catch { return fresh(); }
  };
  let doc = read();

  /* ---------- Saving: debounced, flushed on pagehide ---------- */
  let timer = 0;
  const flush = () => {
    clearTimeout(timer); timer = 0;
    try { localStorage.setItem(KEY, JSON.stringify(doc)); } catch { /* storage full or blocked: the state lasts for this visit */ }
  };
  const emit = (what) => { try { window.ZQ && typeof window.ZQ.emit === 'function' && window.ZQ.emit('state', { what }); } catch (e) { console.error(e); } };
  const changed = (what) => { clearTimeout(timer); timer = setTimeout(flush, 200); emit(what); };
  if (typeof window.addEventListener === 'function') {
    window.addEventListener('pagehide', flush);
    window.addEventListener('beforeunload', flush);
  }

  /* ---------- Small helpers ---------- */
  const lessonId = (course, lesson) => `${course}/${lesson}`;
  const lessonRec = (course, lesson) => {
    const id = lessonId(course, lesson);
    return doc.lessons[id] || (doc.lessons[id] = { attempts: 0, done: false, firstTry: null, xp: 0, bestQuiz: null, mastered: false, perfect: false, completedAt: null, secondsSpent: 0, position: null, positionAt: null, revealed: [], gradable: 0 });
  };
  const itemRating = (difficulty) => 1000 + (Math.min(5, Math.max(1, Number(difficulty) || 1)) - 1) * 150;
  const mpFor = (difficulty) => 2 * Math.min(5, Math.max(1, Math.round(Number(difficulty) || 2)));
  const skillRec = (id) => doc.skills[id] || (doc.skills[id] = { mp: 0, elo: ELO_START, seen: 0, correct: 0, lastAt: null });
  /* Elo-style update for one graded item against each of its skills; adds MP when asked */
  /* Provenance of a graded row (N01): 'auto' machine-marked, 'self' ticked by the learner, 'external' entered by a reviewer.
     Only 'self' is kept apart; 'external' counts like 'auto'. Anything else reads as 'auto'. */
  const HOWS = ['auto', 'self', 'external'];
  const howOf = (x) => (x && HOWS.includes(x.how) ? x.how : 'auto');
  const isSelf = (x) => howOf(x) === 'self';
  /* The provenance of an item spec: a longform item (or one with a longform part) is marked by the learner's own ticks */
  const provenance = (it) => { const L = (w) => !!w && w.kind === 'longform'; return it && (it.kind === 'longform' || L(it.widget) || (Array.isArray(it.parts) && it.parts.some(q => q && L(q.widget)))) ? 'self' : 'auto'; };
  const selfRec = (id) => { if (!isObj(doc.selfMarked)) doc.selfMarked = {}; return doc.selfMarked[id] || (doc.selfMarked[id] = { seen: 0, correct: 0, lastAt: null }); };
  const rate = (skills, ok, difficulty, { elo = true, mp = 0, how = 'auto' } = {}) => {
    const R = itemRating(difficulty);
    (skills || []).forEach(s => {
      if (!s) return;
      if (how === 'self') { const q = selfRec(s); q.seen++; if (ok) q.correct++; q.lastAt = now(); return; }   // no Elo, MP, seen or correct on the skill
      const r = skillRec(s);
      r.seen++; if (ok) r.correct++; r.lastAt = now();
      if (elo) { const E = 1 / (1 + Math.pow(10, (R - r.elo) / 400)); r.elo = Math.round((r.elo + K * ((ok ? 1 : 0) - E)) * 10) / 10; }
      if (mp) r.mp += mp;
    });
  };
  /* Score each item of a set: results [{ id, ok, difficulty, skills }] if given, else wrongItems and a count of correct */
  const itemsOf = ({ results, wrongItems = [], score = 0, skills = [], difficulty = 2 }) => {
    if (Array.isArray(results) && results.length) return results.map(r => ({ id: r.id, ok: !!r.ok, difficulty: r.difficulty || difficulty, skills: r.skills || skills, ref: r.ref, how: howOf(r) }));
    const wrong = wrongItems.map(w => ({ id: w.id, ok: false, difficulty: w.difficulty || difficulty, skills: w.skills || skills, ref: w.ref, how: howOf(w) }));
    const right = Array.from({ length: Math.max(0, Number(score) || 0) }, (_, i) => ({ id: null, ok: true, difficulty, skills, how: 'auto' }));
    return right.concat(wrong);
  };

  /* ---------- Streak ---------- */
  const qualifiedTotal = () => Object.values(doc.streak.days).filter(v => v === true).length;
  /* Bring the streak up to today: cover missed days with rest days when there are enough, otherwise break it.
     Runs on load, on every touch and in summary(); idempotent. */
  const rollover = () => {
    const s = doc.streak, today = todayKey();
    if (!s.lastDay || s.current === 0) return false;
    const gap = daysBetween(s.lastDay, today);
    if (gap <= 1) return false;
    const missed = gap - 1;
    if (missed <= s.restDays) {
      for (let i = 1; i <= missed; i++) s.days[addDays(s.lastDay, i)] = 'rest';
      s.restDays -= missed;
      s.lastDay = addDays(today, -1);
    } else {
      s.current = 0;
    }
    return true;
  };
  /* Mark today as qualifying. Returns true when today has just qualified (the player shows the streak moment). */
  const touch = () => {
    rollover();
    const s = doc.streak, today = todayKey();
    if (s.days[today] === true) return false;
    s.days[today] = true;
    s.current = s.lastDay === addDays(today, -1) && s.current > 0 ? s.current + 1 : 1;
    s.lastDay = today;
    s.best = Math.max(s.best || 0, s.current);
    const total = qualifiedTotal();
    if (total - (s.restEarnedAt || 0) >= REST_EVERY) { if (s.restDays < REST_MAX) s.restDays++; s.restEarnedAt = total; }
    if (!doc.profile.createdAt) doc.profile.createdAt = now();
    changed('streak');
    return true;
  };
  const countProblem = () => {
    const c = doc.streak.count, today = todayKey();
    if (c.day !== today) { c.day = today; c.problems = 0; }
    c.problems++;
    return c.problems >= QUALIFY_PROBLEMS ? touch() : false;
  };

  /* ---------- Hours ---------- */
  const logHours = ({ block, minutes, source = 'manual', date } = {}) => {
    if (!BLOCKS.includes(block)) throw new Error(`hours.log: unknown block "${block}"`);
    const m = Math.round((Number(minutes) || 0) * 10) / 10;
    if (m <= 0) return null;
    const e = { date: date || todayKey(), block, minutes: m, source };
    doc.hours.push(e);
    changed('hours');
    return e;
  };
  const logSeconds = (block, seconds, source) => { if (seconds > 0) logHours({ block, minutes: seconds / 60, source }); };

  /* ---------- Redo queue ---------- */
  const redoAdd = ({ id, kind = 'screen', ref = {}, skills = [], difficulty = 2 } = {}) => {
    const rid = id || (ref.exam ? `${ref.exam}/${ref.item}` : kind === 'screen' ? `${ref.course}/${ref.lesson}#${ref.screen}` : `${ref.course}/${ref.lesson}/${ref.item}`);
    const due = now() + REDO_FIRST * DAY;
    const ex = doc.redo.find(r => r.id === rid);
    if (ex) { ex.interval = REDO_FIRST; ex.due = due; ex.misses = (ex.misses || 0) + 1; changed('redo'); return ex; }
    const r = { id: rid, kind, ref, due, interval: REDO_FIRST, misses: 1, skills: skills || [], difficulty, addedAt: now() };
    doc.redo.push(r);
    changed('redo');
    return r;
  };
  const redoDue = (t) => { const at = t == null ? now() : t; return doc.redo.filter(r => r.due <= at).sort((a, b) => a.due - b.due); };
  /* A correct 7-day redo comes back in 30 days; a correct 30-day redo leaves; a miss goes back to 7 days. MP on success. */
  const redoResult = ({ id, ok, seconds = 0 } = {}) => {
    const i = doc.redo.findIndex(r => r.id === id);
    if (i < 0) return null;
    const r = doc.redo[i];
    let out;
    if (ok) {
      const gain = mpFor(r.difficulty);
      doc.mp += gain; rate(r.skills, true, r.difficulty, { mp: gain });
      if (r.interval >= REDO_SECOND) { doc.redo.splice(i, 1); out = { id, left: true, mp: gain }; }
      else { r.interval = REDO_SECOND; r.due = now() + REDO_SECOND * DAY; out = { id, left: false, interval: r.interval, due: r.due, mp: gain }; }
    } else {
      rate(r.skills, false, r.difficulty);
      r.interval = REDO_FIRST; r.due = now() + REDO_FIRST * DAY; r.misses = (r.misses || 0) + 1;
      out = { id, left: false, interval: r.interval, due: r.due, mp: 0 };
    }
    logSeconds('review', seconds, 'redo');
    out.qualified = countProblem();
    changed('redo');
    return out;
  };

  /* ---------- Mutators ---------- */
  /* Lesson screens earn XP and feed the redo queue and the streak count. They do not move MP or skill scores:
     those come only from scaffold-free items (quizzes, reviews, homework, exams, redos). */
  const screenGraded = ({ course, lesson, screen, ok, firstTry, revealed, difficulty = 1, skills = [] } = {}) => {
    const rec = lessonRec(course, lesson);
    const repeat = rec.done;
    /* revealed screens (met rule 3): a Solve before the lesson is first finished adds the screen; a later honest solve takes it off */
    if (screen != null) {
      if (!Array.isArray(rec.revealed)) rec.revealed = [];
      const at = rec.revealed.indexOf(screen);
      if (revealed && !rec.done && at < 0) rec.revealed.push(screen);
      else if (ok && !revealed && at >= 0) rec.revealed.splice(at, 1);
    }
    let xp = 0;
    if (ok && !revealed && !repeat) xp = firstTry ? XP.first : XP.retry;
    doc.xp += xp; rec.xp += xp;
    let redo = null;
    if (!ok || revealed) redo = redoAdd({ kind: 'screen', ref: { course, lesson, screen }, skills, difficulty });
    const qualified = ok || revealed ? countProblem() : false;
    changed('lessons');
    return { xp, redo, qualified };
  };

  const lessonFinished = ({ course, lesson, firstTry = null, perfect = false, seconds = 0 } = {}) => {
    const rec = lessonRec(course, lesson);
    const repeat = rec.done;
    const xp = repeat ? 0 : XP.lesson + (perfect ? XP.perfect : 0);
    doc.xp += xp; rec.xp += xp;
    rec.attempts++; rec.done = true;
    if (firstTry) rec.firstTry = firstTry;
    if (Array.isArray(firstTry) && Number(firstTry[1]) >= 0) rec.gradable = Number(firstTry[1]);   // gradable screens plus quiz items, the denominator of the reveal cap
    rec.perfect = rec.perfect || !!perfect;
    rec.completedAt = rec.completedAt || now();
    rec.secondsSpent += Math.max(0, Number(seconds) || 0);
    rec.position = null; rec.positionAt = null;
    logSeconds('main', seconds, 'lesson');
    const qualified = touch();
    changed('lessons');
    return { xp, qualified, repeat };
  };

  /* Rule 3: a lesson counts as done (for prerequisites and progress) unless more than REVEAL_CAP of its gradable screens were revealed. Raw rec.done still means finished. */
  const revealShare = (r) => (r && Number(r.gradable) > 0 && Array.isArray(r.revealed) ? r.revealed.length / Number(r.gradable) : 0);
  const lessonCounts = (r) => !!(r && r.done && !(revealShare(r) > REVEAL_CAP + 1e-9));
  const quizFinished = ({ course, lesson, score = 0, items = 0, wrongItems = [], results, skills = [], seconds = 0 } = {}) => {
    const rec = lessonRec(course, lesson);
    const repeat = !!rec.bestQuiz;
    const list = itemsOf({ results, wrongItems, score, skills, difficulty: 2 });
    const correct = list.filter(x => x.ok).length;
    const total = items || list.length;
    let mp = 0;
    list.forEach(x => { const gain = x.ok && !repeat && !isSelf(x) ? mpFor(x.difficulty) : 0; mp += gain; rate(x.skills, x.ok, x.difficulty, { mp: gain, how: x.how }); });
    const xp = repeat ? 0 : XP.quizItem * list.filter(x => x.ok && !isSelf(x)).length;
    doc.xp += xp; doc.mp += mp; rec.xp += xp;
    if (!rec.bestQuiz || correct > rec.bestQuiz[0]) rec.bestQuiz = [correct, total];
    const share = total ? correct / total : 0;
    const mastered = share >= MASTERY;
    if (mastered) rec.mastered = true;
    const redo = list.filter(x => !x.ok).map(x => redoAdd({ kind: 'quiz', ref: x.ref || { course, lesson, item: x.id }, skills: x.skills, difficulty: x.difficulty }));
    logSeconds('main', seconds, 'quiz');
    const qualified = touch();
    changed('lessons');
    return { xp, mp, mastered, redo, qualified };
  };

  const reviewFinished = ({ course, id, score = 0, items = 0, wrongItems = [], results, skills = [], seconds = 0, pass = REVIEW_PASS } = {}) => {
    const key = `${course}/${id}`;
    const prev = doc.reviews[key];
    const repeat = !!prev;
    const list = itemsOf({ results, wrongItems, score, skills, difficulty: 3 });
    const correct = list.filter(x => x.ok).length;
    let mp = 0;
    list.forEach(x => { const gain = x.ok && !repeat && !isSelf(x) ? mpFor(x.difficulty) : 0; mp += gain; rate(x.skills, x.ok, x.difficulty, { mp: gain, how: x.how }); });
    const xp = repeat ? 0 : XP.quizItem * list.filter(x => x.ok && !isSelf(x)).length;
    doc.xp += xp; doc.mp += mp;
    const total = items || list.length;
    /* passed is sticky: a later weaker attempt never takes it away (prerequisite gating, ENGINE-BACKLOG 481) */
    /* passedAuto: the same pass mark over auto and external rows only (self rows leave numerator and denominator); prerequisite met reads it */
    const selfN = list.filter(isSelf).length, aTotal = Math.max(0, total - selfN), aCorrect = list.filter(x => x.ok && !isSelf(x)).length;
    /* Rule 2: passedAuto also needs every essential skill (every skill tagged on the items) at SKILL_FLOOR over the auto rows of this attempt; passBySkill keeps the attempt that met it */
    const bySkill = {}, essential = [...new Set(list.flatMap(x => x.skills || []).filter(Boolean))];
    list.filter(x => !isSelf(x)).forEach(x => (x.skills || []).forEach(sk => { if (!sk) return; const b = bySkill[sk] || (bySkill[sk] = [0, 0]); b[1]++; if (x.ok) b[0]++; }));
    const metNow = aTotal > 0 && aCorrect >= Math.ceil(aTotal * pass - 1e-9) && floorGaps(bySkill, essential).length === 0;
    const kept = !!(prev && prev.passedAuto);
    doc.reviews[key] = { score: correct, items: total, at: now(), passed: !!((prev && prev.passed) || (total > 0 && correct >= Math.ceil(total * pass - 1e-9))),
      passedAuto: kept || metNow, essential, bySkill, ...(kept ? (prev.passBySkill ? { passBySkill: prev.passBySkill } : {}) : metNow ? { passBySkill: bySkill } : {}) };
    perfFrom(course, Number((String(id).match(/(\d+)$/) || [])[1]) || null, results);
    const redo = list.filter(x => !x.ok).map(x => redoAdd({ kind: 'quiz', ref: x.ref || { course, lesson: id, item: x.id }, skills: x.skills, difficulty: x.difficulty }));
    logSeconds('main', seconds, 'review');
    const qualified = touch();
    changed('reviews');
    return { xp, mp, redo, qualified };
  };

  /* Performance task (ENGINE-BACKLOG 529): a result row carrying `perf` (the item's kind) that came back ok records the level's task passed.
     how is the row's own provenance: auto (code, numeric data), self (the rubric mark) or external. Sticky: a later miss never removes it. */
  const perfPass = ({ course, level, item, kind, how } = {}) => {
    if (!course || !level) return null;
    if (!isObj(doc.perf)) doc.perf = {};
    const key = `${course}/L${level}`;
    if (doc.perf[key]) return doc.perf[key];
    doc.perf[key] = { item: item || null, kind: kind || null, how: how === 'self' || how === 'external' ? how : 'auto', at: now() };
    changed('perf');
    return doc.perf[key];
  };
  const perfFrom = (course, level, results) => {
    (Array.isArray(results) ? results : []).forEach(x => { if (x && x.perf && x.ok) perfPass({ course, level, item: x.id, kind: x.perf, how: howOf(x) }); });
  };

  const homeworkAssigned = ({ course, level, dueDays = 7 } = {}) => {
    const key = `${course}/homework-${level}`;
    if (doc.homework[key]) return doc.homework[key];
    const t = now();
    const rec = doc.homework[key] = { assignedAt: t, due: t + dueDays * DAY, submitted: false, score: null, items: null, selfMarks: null };
    changed('homework');
    return rec;
  };

  const homeworkSubmitted = ({ course, level, id, score = 0, items = 0, selfMarks = null, wrongItems = [], results, skills = [], seconds = 0 } = {}) => {
    const key = `${course}/${id || 'homework-' + level}`;
    const rec = doc.homework[key] || (doc.homework[key] = { assignedAt: now(), due: now(), submitted: false });
    const repeat = !!rec.submitted;
    const list = itemsOf({ results, wrongItems, score, skills, difficulty: 4 });
    const correct = list.filter(x => x.ok).length;
    let mp = 0;
    list.forEach(x => { const gain = x.ok && !repeat && !isSelf(x) ? mpFor(x.difficulty) : 0; mp += gain; rate(x.skills, x.ok, x.difficulty, { mp: gain, how: x.how }); });
    const xp = repeat ? 0 : XP.homework + XP.homeworkItem * list.filter(x => x.ok && !isSelf(x)).length;   // self-ticked items earn no item XP
    doc.xp += xp; doc.mp += mp;
    Object.assign(rec, { submitted: true, submittedAt: now(), score: correct, items: items || list.length, selfMarks });
    perfFrom(course, level, results);
    const redo = list.filter(x => !x.ok).map(x => redoAdd({ kind: 'homework', ref: x.ref || { course, lesson: id || 'homework-' + level, item: x.id }, skills: x.skills, difficulty: x.difficulty }));
    logSeconds('main', seconds, 'homework');
    const qualified = touch();
    changed('homework');
    return { xp, mp, redo, qualified };
  };

  /* Practice and weekly problems (ZQ.select sets): each result moves the skill scores (Elo) and counts toward the day's
     3 graded problems for the streak. No XP and no MP: practice repeats content already scored elsewhere. */
  const practiceResult = ({ results = [], source = 'practice' } = {}) => {
    let qualified = false;
    (results || []).forEach(x => {
      if (!x) return;
      rate(x.skills || [], !!x.ok, x.difficulty || 2);
      if (countProblem()) qualified = true;
    });
    logTiming(results);
    changed('skills');
    return { source, items: (results || []).length, qualified };
  };

  /* Seconds per item (ENGINE-BACKLOG 457): a running total per family, kept from exams, practice and the bank deck so a
     later view can show where the learner is slow. Rows are { seconds, family, pace }; rows without both are skipped.
     Nothing here touches grading, XP or mastery. */
  function logTiming(rows) {
    if (!isObj(doc.timing)) doc.timing = { families: {} };
    if (!isObj(doc.timing.families)) doc.timing.families = {};
    (rows || []).forEach(x => {
      if (!x || typeof x.seconds !== 'number' || !(x.seconds >= 0) || !x.family) return;
      const f = doc.timing.families[x.family] || (doc.timing.families[x.family] = { n: 0, seconds: 0, over: 0 });
      f.n++; f.seconds = Math.round((f.seconds + x.seconds) * 10) / 10;
      if (x.pace > 0 && x.seconds > x.pace) f.over++;
    });
  }

  /* ---------- Interview bank deck (ENGINE-BACKLOG 456): each item has its own Leitner schedule ----------
     doc.bank[uid] = { box, due, seen, miss, last, secs, at, family }, uid like "bank/<file>/<item>" or, for a tagged
     review or homework item, its own "course/lesson/item". box is the interval in days (1, 3, 7 or 30). A new item
     starts in box 1; a right answer moves it up one box and it returns after that many days; a miss sends it back to
     box 1, due in 1 day. Unseen items have no entry. */
  const BANK_BOXES = [1, 3, 7, 30];
  const bankEntry = (uid) => doc.bank[uid] || null;
  const bankDue = (t) => { const at = t == null ? now() : t; return Object.entries(doc.bank).filter(([, r]) => r && r.due <= at).map(([uid]) => uid); };
  /* results: [{ uid, ok, seconds, family, pace, difficulty, skills }]. Skill scores and the streak count move as in practice. */
  const bankResult = ({ results = [] } = {}) => {
    let qualified = false;
    const boxes = { 1: 0, 3: 0, 7: 0, 30: 0 };
    const rows = (results || []).filter(x => x && x.uid);
    rows.forEach(x => {
      const r = doc.bank[x.uid] || (doc.bank[x.uid] = { box: 1, due: 0, seen: 0, miss: 0, last: null, secs: null, at: null, family: x.family || '' });
      const i = Math.max(0, BANK_BOXES.indexOf(r.box));
      r.box = x.ok ? BANK_BOXES[Math.min(BANK_BOXES.length - 1, i + 1)] : BANK_BOXES[0];
      r.due = now() + r.box * DAY;
      r.seen++; if (!x.ok) r.miss++;
      r.last = !!x.ok; r.at = now(); if (typeof x.seconds === 'number') r.secs = x.seconds;
      if (x.family) r.family = x.family;
      boxes[r.box]++;
      rate(x.skills || [], !!x.ok, x.difficulty || 3);
      if (countProblem()) qualified = true;
    });
    logTiming(rows);
    changed('bank');
    return { items: rows.length, boxes, qualified };
  };

  /* bySkill: { skill: [correct, total] }. results (optional): per-item { id, ok, difficulty, skills } for exact Elo updates.
     Each missed result with an id joins the redo queue as kind 'exam' with ref { exam, item } (ZQ.select.resolve reads it).
     results may carry seconds, family and pace per item; they feed ZQ.state.timing and never affect marks.
     extra (optional): more fields kept on the attempt (itemSeconds, a mock's net). A mock exam (mock-*) earns no XP and keeps every attempt. */
  const examFinished = ({ id, score = 0, passed = false, passedAuto, bySkill = {}, items = 0, results, seconds = 0, extra, checks } = {}) => {
    const rec = doc.exams[id] || (doc.exams[id] = { attempts: [] });
    const passedBefore = rec.attempts.some(a => a.passed);
    let mp = 0;
    if (Array.isArray(results) && results.length) {
      results.forEach(x => { const gain = x.ok && !isSelf(x) ? mpFor(x.difficulty || 3) : 0; mp += gain; rate(x.skills || [], !!x.ok, x.difficulty || 3, { mp: gain, how: howOf(x) }); });
    } else {
      Object.entries(bySkill).forEach(([s, v]) => {
        const [ok, total] = Array.isArray(v) ? v : [v, v];
        for (let i = 0; i < total; i++) { const right = i < ok, gain = right ? mpFor(3) : 0; mp += gain; rate([s], right, 3, { mp: gain }); }
      });
    }
    const xp = passed && !passedBefore && !String(id).startsWith('mock-') ? (String(id).startsWith('stage-') ? XP.stageExam : XP.topicExam) : 0; // a mock is sat many times: no XP
    doc.xp += xp; doc.mp += mp;
    /* passedAuto: the pass with self rows (and self checks) left out; absent when the caller gave none and an old attempt has none either.
       Without results or self rows it equals passed. checks: [{ name, how: 'self', ok }], the tick boxes the app cannot mark. */
    const hasSelf = Array.isArray(results) && results.some(isSelf);
    /* bySkillAuto (met rule 4): { skill: [correct, total] } over auto and external rows only; without results it is bySkill */
    let bySkillAuto = bySkill;
    if (Array.isArray(results) && results.length && results.every(x => x && Array.isArray(x.skills))) {
      bySkillAuto = {};
      results.filter(x => !isSelf(x)).forEach(x => x.skills.forEach(sk => { if (!sk) return; const b = bySkillAuto[sk] || (bySkillAuto[sk] = [0, 0]); b[1]++; if (x.ok) b[0]++; }));
    }
    const pa = typeof passedAuto === 'boolean' ? passedAuto : (hasSelf || (Array.isArray(checks) && checks.length) ? undefined : !!passed);
    rec.attempts.push({ at: now(), score, items, passed: !!passed, ...(typeof pa === 'boolean' ? { passedAuto: pa } : {}), ...(Array.isArray(checks) && checks.length ? { checks: checks.map(c => ({ name: String(c.name), how: 'self', ok: !!c.ok })) } : {}), bySkill, bySkillAuto, ...(extra && typeof extra === 'object' ? extra : {}) }); // extra: a mock's net, wrong, blank, seed, seconds
    const redo = (Array.isArray(results) ? results : []).filter(x => x && !x.ok && (x.id != null || (x.ref && x.ref.item != null)))
      .map(x => redoAdd({ kind: 'exam', ref: x.ref && x.ref.exam ? x.ref : { exam: id, item: x.id }, skills: x.skills || [], difficulty: x.difficulty || 3 }));
    logTiming(results);
    logSeconds('main', seconds, 'exam');
    changed('exams');
    return { xp, mp, redo };
  };

  /* ---------- Prerequisite gating records (ENGINE-BACKLOG 481; rules in js/prereq.js). Nothing here is ever removed. ---------- */
  const prq = () => { const p = doc.prereq; ['met', 'testouts', 'opened', 'started'].forEach(k => { if (!isObj(p[k])) p[k] = {}; }); return p; };
  const prereqMet = (keys, how = 'met') => {
    const p = prq(), t = now();
    (Array.isArray(keys) ? keys : [keys]).forEach(k => { if (!p.met[k]) p.met[k] = { at: t, how }; });
    changed('prereq');
    return p.met;
  };
  /* A test-out attempt for a level key "course/L<n>": { at, score, items, passed, missed: [item ids], tries } */
  const prereqTestout = ({ key, score = 0, items = 0, passed = false, missed = [], seen = [] } = {}) => {
    const p = prq(), prev = p.testouts[key];
    const was = prev && Array.isArray(prev.seen) ? prev.seen : [];
    p.testouts[key] = { at: now(), score, items, passed: !!passed || !!(prev && prev.passed), missed, seen: [...new Set(was.concat(seen))], tries: ((prev && prev.tries) || 0) + 1 };
    if (passed && !p.met[key]) p.met[key] = { at: now(), how: 'testout' };
    changed('prereq');
    return p.testouts[key];
  };
  const prereqOpened = (key) => { const p = prq(); if (!p.opened[key]) { p.opened[key] = now(); changed('prereq'); } return p.opened[key]; };
  /* Levels the learner has started (a finished lesson): kept open, never counted as met */
  const prereqStarted = (keys) => { const p = prq(), t = now(); let n = 0; (Array.isArray(keys) ? keys : [keys]).forEach(k => { if (!p.started[k]) { p.started[k] = t; n++; } }); if (n) changed('prereq'); return n; };
  const prereqGrandfathered = (keys) => { const p = prq(); const t = now(); keys.forEach(k => { if (!p.met[k]) p.met[k] = { at: t, how: 'finished' }; }); p.grandfathered = true; changed('prereq'); };

  const notebookAdd = (card = {}) => {
    const dup = doc.notebook.find(c => c.course === card.course && c.lesson === card.lesson && c.name === card.name);
    if (dup) { Object.assign(dup, card); changed('notebook'); return dup; }
    const c = { course: card.course || null, lesson: card.lesson || null, name: card.name || '', tex: card.tex || '', note: card.note || '', at: now() };
    doc.notebook.push(c);
    changed('notebook');
    return c;
  };

  const drillVerified = (id, code) => {
    const prev = doc.drills[id] || {};
    doc.drills[id] = { ...prev, verified: true, code: String(code || ''), at: now() };
    changed('drills');
    return doc.drills[id];
  };
  /* Unverified code, kept in the document so Export carries it: draft(id) reads it, draft(id, code) saves it, and
     draft(id, null) clears it. A drill's id is its file id; a code item in a lesson, set or exam uses its item path
     (course/lesson/item or exam/item). A draft-only record has verified: false. */
  const drillDraft = (id, code) => {
    if (id == null) return null;
    const rec = doc.drills[id];
    if (code === undefined) return rec && typeof rec.draft === 'string' ? rec.draft : null;
    if (code === null || code === '') {
      if (!rec) return null;
      delete rec.draft; delete rec.draftAt;
      if (!rec.verified && !rec.code && !rec.runs) delete doc.drills[id];
    } else {
      const r = rec || (doc.drills[id] = { verified: false, code: '', at: null });
      if (r.draft === String(code)) return r.draft;
      r.draft = String(code); r.draftAt = now();
    }
    changed('drills');
    return code ?? null;
  };

  /* Drill clocks (engine pass C, item 472). time(id, { seconds, passed, total, ok, pace }) keeps the stopwatch reading of a
     submit on the drill's record: runs (the last 20, newest last), and on a pass seconds (that run) and best (the lowest
     passing time). Nothing here changes marks or the verified flag. A session is one finished two-drill sitting:
     { at, name, minutes (the budget), seconds (used), drills: [{ id, seconds, passed, total, ok }] }, the last 50 kept. */
  const drillTime = (id, r) => {
    if (id == null || !r) return null;
    const rec = doc.drills[id] || (doc.drills[id] = { verified: false, code: '', at: null });
    const seconds = Math.max(0, Math.round(Number(r.seconds) || 0));
    const run = { at: now(), seconds, passed: r.passed | 0, total: r.total | 0, ok: !!r.ok };
    rec.runs = (Array.isArray(rec.runs) ? rec.runs : []).concat(run).slice(-20);
    if (run.ok) { rec.seconds = seconds; rec.best = typeof rec.best === 'number' ? Math.min(rec.best, seconds) : seconds; }
    changed('drills');
    return run;
  };
  const drillSessionRecord = (s) => {
    if (!s || !Array.isArray(s.drills)) return null;
    const e = { at: now(), name: String(s.name || ''), minutes: Number(s.minutes) || 60, seconds: Math.max(0, Math.round(Number(s.seconds) || 0)),
      drills: s.drills.map(d => ({ id: String(d.id), seconds: Math.max(0, Math.round(Number(d.seconds) || 0)), passed: d.passed | 0, total: d.total | 0, ok: !!d.ok })) };
    doc.drillSessions = (Array.isArray(doc.drillSessions) ? doc.drillSessions : []).concat(e).slice(-50);
    changed('drillSessions');
    return e;
  };

  const warmupRecord = (score, seconds = 120) => {
    const e = { date: todayKey(), score: Number(score) || 0, at: now() };
    doc.warmup.history.push(e);
    logSeconds('mental', seconds, 'warmup');
    changed('warmup');
    return e;
  };

  const positionSet = (course, lesson, position) => {
    const rec = lessonRec(course, lesson);
    rec.position = position; rec.positionAt = position == null ? null : now();
    changed('position');
  };
  /* A lesson opened on purpose from Learn or the course map (ENGINE-BACKLOG 617): only this lets a saved position in a tested-out course stand after the pass. */
  const positionPick = (course, lesson) => { const rec = lessonRec(course, lesson); rec.pickedAt = now(); changed('position'); };
  const positionGet = (course, lesson) => { const r = doc.lessons[lessonId(course, lesson)]; return r ? r.position : null; };

  const profileSet = (patch = {}) => {
    const p = { ...patch };
    if ('track' in p && !TRACKS.includes(p.track)) throw new Error(`profile.set: track must be one of ${TRACKS.join(', ')}`);
    if ('weeklyGoalH' in p && !GOALS.includes(Number(p.weeklyGoalH))) throw new Error('profile.set: weeklyGoalH must be 5, 10, 15 or 25');
    if ('weeklyGoalH' in p) p.weeklyGoalH = Number(p.weeklyGoalH);
    if ('startStage' in p) p.startStage = Math.min(3, Math.max(0, Number(p.startStage) || 0));
    if ('name' in p && !('initial' in p) && !doc.profile.initial) p.initial = String(p.name).trim().charAt(0).toUpperCase();
    Object.assign(doc.profile, p);
    if (!doc.profile.createdAt) doc.profile.createdAt = now();
    changed('profile');
    return doc.profile;
  };
  const settingsSet = (patch = {}) => { Object.assign(doc.settings, patch); changed('settings'); return doc.settings; };
  const flagsSet = (patch = {}) => { Object.assign(doc.flags, patch); changed('flags'); return doc.flags; };

  /* ---------- Export, import, reset ---------- */
  const exportDoc = () => JSON.stringify(doc, null, 2);
  const importDoc = (json) => {
    let raw;
    try { raw = typeof json === 'string' ? JSON.parse(json) : json; } catch (e) { return { ok: false, error: 'That file is not valid JSON.' }; }
    if (!isObj(raw)) return { ok: false, error: 'That file does not hold a Zero to Quant state.' };
    if (raw.v !== V) return { ok: false, error: `Unsupported state version ${raw.v === undefined ? '(missing)' : raw.v}. This app reads version ${V}.` };
    doc = normalise(raw);
    flush(); emit('import');
    return { ok: true };
  };
  const reset = () => { doc = fresh(); flush(); emit('reset'); return doc; };

  /* ---------- Derived numbers for the screens ---------- */
  const weeklySplit = (h) => {
    // 9 / 3 / 2 / 1 at 15 h (curriculum weekly rhythm). Mental stays at 1 h; the rest share 9 : 3 : 2 in half hours.
    const rest = Math.max(0, h - 1), raw = [9, 3, 2].map(w => rest * w / 14);
    const halves = raw.map(v => Math.floor(v * 2)); let left = rest * 2 - halves.reduce((a, b) => a + b, 0);
    raw.map((v, i) => [v * 2 - Math.floor(v * 2), i]).sort((a, b) => b[0] - a[0] || a[1] - b[1]).forEach(([, i]) => { if (left > 0) { halves[i]++; left--; } });
    const [main, build, review] = halves.map(v => v / 2);
    return { main, build, review, mental: 1 };
  };
  const summary = () => {
    if (rollover()) changed('streak');
    const s = doc.streak, today = todayKey(), ws = weekStart();
    const created = doc.profile.createdAt ? todayKey(doc.profile.createdAt) : today;
    const week = Array.from({ length: 7 }, (_, i) => {
      const k = addDays(ws, i), v = s.days[k];
      if (k === today) return 'today';
      if (k > today) return 'future';
      if (v === true) return 'lit';
      if (v === 'rest') return 'rest';
      return k < created ? 'future' : 'missed';
    });
    const hoursWeek = { main: 0, build: 0, review: 0, mental: 0 };
    doc.hours.forEach(e => { if (e.date >= ws && e.date <= addDays(ws, 6) && hoursWeek[e.block] != null) hoursWeek[e.block] += e.minutes / 60; });
    Object.keys(hoursWeek).forEach(k => { hoursWeek[k] = Math.round(hoursWeek[k] * 100) / 100; });
    const lessons = Object.entries(doc.lessons);
    const C = window.ZQ && window.ZQ.content;
    const courseProgress = {};
    if (C && typeof C.courses === 'function') {
      try {
        (C.allCourses || C.courses)().forEach(c => {
          const ls = C.courseLessons(c.id).filter(x => x.kind === 'lesson');
          const done = ls.filter(x => lessonCounts(doc.lessons[lessonId(c.id, x.id)])).length;
          courseProgress[c.id] = ls.length ? done / ls.length : 0;
        });
      } catch (e) { console.error(e); }
    }
    const skillMastery = {};
    Object.entries(doc.skills).forEach(([k, v]) => { skillMastery[k] = v.seen ? Math.min(1, Math.max(0, (v.elo - 1000) / 600)) : 0; });
    const due = redoDue();
    const open = lessons.filter(([, r]) => !r.done && r.position != null).sort((a, b) => Math.max(b[1].positionAt || 0, b[1].pickedAt || 0) - Math.max(a[1].positionAt || 0, a[1].pickedAt || 0));
    const resume = open.length ? (() => { const [id, r] = open[0]; const [course, lesson] = id.split('/'); return { course, lesson, position: r.position, at: r.positionAt, pickedAt: r.pickedAt || null }; })() : null;
    const homeworkOpen = Object.entries(doc.homework).filter(([, h]) => !h.submitted).map(([id, h]) => ({ id, course: id.split('/')[0], due: h.due, overdue: h.due < now() })).sort((a, b) => a.due - b.due);
    const goal = doc.profile.weeklyGoalH || 15;
    return {
      name: doc.profile.name, initial: doc.profile.initial || (doc.profile.name || '?').charAt(0).toUpperCase(), track: doc.profile.track,
      streak: s.current, best: s.best, todayQualified: s.days[today] === true, restDays: s.restDays,
      restProgress: (qualifiedTotal() - (s.restEarnedAt || 0)) % REST_EVERY, problemsToday: s.count.day === today ? s.count.problems : 0,
      streakOff: doc.settings.streakMode === 'off', week,
      xp: doc.xp, mp: doc.mp,
      hoursWeek, hoursWeekTotal: Math.round(Object.values(hoursWeek).reduce((a, b) => a + b, 0) * 100) / 100, weeklyGoalH: goal, weekGoal: weeklySplit(goal),
      lessonsDone: lessons.filter(([, r]) => lessonCounts(r)).length, mastered: lessons.filter(([, r]) => r.mastered).length,
      courseProgress, skillMastery,
      redoDue: due.length, redoMinutes: due.length * 2, redoTotal: doc.redo.length,
      homeworkOpen, resume,
      warmupLast: doc.warmup.history.length ? doc.warmup.history[doc.warmup.history.length - 1].score : null,
      warmupTrend: doc.warmup.history.slice(-10).map(e => e.score),
    };
  };

  /* ---------- Public API ---------- */
  /* A namespace that carries methods and also reads through to the document's field: ZQ.state.profile.name and
     ZQ.state.profile.set({...}) both work. Arrays (redo, notebook, hours) read by index and length; use .list() to iterate. */
  const ns = (key, methods) => new Proxy(methods, {
    get(t, p) { if (p in t) return t[p]; const v = doc[key]; return v == null ? undefined : v[p]; },
    has(t, p) { return p in t || (doc[key] != null && p in doc[key]); },
  });
  const api = {
    get doc() { return doc; },
    get v() { return doc.v; },
    get xp() { return doc.xp; },
    get mp() { return doc.mp; },
    get lessons() { return doc.lessons; },
    get reviews() { return doc.reviews; },
    get homework() { return doc.homework; },
    get exams() { return doc.exams; },
    get skills() { return doc.skills; },
    get selfMarked() { return doc.selfMarked; },
    perf: ns('perf', { pass: perfPass, get: () => doc.perf }),
    profile: ns('profile', { set: profileSet, get: () => doc.profile }),
    settings: ns('settings', { set: settingsSet, get: () => doc.settings }),
    flags: ns('flags', { set: flagsSet, get: () => doc.flags }),
    streak: ns('streak', { touch, rollover: () => { const r = rollover(); if (r) changed('streak'); return r; }, get: () => doc.streak }),
    redo: ns('redo', { add: redoAdd, due: redoDue, result: redoResult, list: () => doc.redo.slice() }),
    notebook: ns('notebook', { add: notebookAdd, list: () => doc.notebook.slice() }),
    bank: ns('bank', { entry: bankEntry, due: bankDue, result: bankResult, list: () => ({ ...doc.bank }) }),
    get timing() { return doc.timing; },
    drills: ns('drills', { verified: drillVerified, draft: drillDraft, time: drillTime, session: drillSessionRecord, sessions: () => (Array.isArray(doc.drillSessions) ? doc.drillSessions.slice() : []), get: (id) => (id == null ? doc.drills : doc.drills[id] || null) }),
    warmup: ns('warmup', { record: warmupRecord, list: () => doc.warmup.history.slice() }),
    hours: ns('hours', { log: logHours, list: () => doc.hours.slice() }),
    lessonPosition: { set: positionSet, get: positionGet, pick: positionPick },
    lesson: (course, lesson) => doc.lessons[lessonId(course, lesson)] || null,
    prereq: ns('prereq', { mark: prereqMet, testout: prereqTestout, open: prereqOpened, start: prereqStarted, grandfather: prereqGrandfathered, get: () => prq() }),
    screenGraded, lessonFinished, lessonCounts, revealShare, floorGaps, quizFinished, reviewFinished, homeworkAssigned, homeworkSubmitted, examFinished, practiceResult, bankResult, provenance, howOf,
    summary, weeklySplit,
    export: exportDoc, import: importDoc, reset, flush,
    dates, rules: { XP, MASTERY, REVIEW_PASS, SKILL_FLOOR, REVEAL_CAP, REDO_FIRST, REDO_SECOND, REST_EVERY, REST_MAX, QUALIFY_PROBLEMS, K, ELO_START, BLOCKS, TRACKS, GOALS, itemRating, mpFor },
    /* Test hook: replace the clock (a function returning ms) and reload from storage. Not for screens. */
    _setClock(fn) { clock = typeof fn === 'function' ? fn : () => Date.now(); },
    _reload() { doc = read(); return doc; },
  };
  if (rollover()) flush();
  window.ZQ = window.ZQ || {};
  window.ZQ.state = api;
})();
