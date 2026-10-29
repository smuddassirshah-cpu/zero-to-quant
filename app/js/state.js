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
  const REDO_FIRST = 7, REDO_SECOND = 30;
  const REST_EVERY = 7, REST_MAX = 2;
  const QUALIFY_PROBLEMS = 3;
  const BLOCKS = ['main', 'build', 'review', 'mental'];
  const TRACKS = ['Trader', 'Researcher', 'Developer', 'Undecided'];
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
    settings: { theme: 'system', motion: 'system', sound: false, haptics: true, streakMode: 'daily', quantOnly: false },
    xp: 0, mp: 0,
    lessons: {}, reviews: {}, homework: {}, exams: {}, skills: {},
    redo: [], notebook: [], drills: {},
    warmup: { history: [] },
    hours: [],
    streak: { current: 0, best: 0, lastDay: null, restDays: 0, restEarnedAt: 0, days: {}, count: { day: null, problems: 0 } },
    flags: { setupDone: false, streakGoal: null },
  });
  const isObj = (x) => x && typeof x === 'object' && !Array.isArray(x);
  /* Fill anything missing from a loaded or imported document with the defaults, one level deep, keeping unknown keys */
  const normalise = (raw) => {
    const d = fresh();
    if (!isObj(raw)) return d;
    for (const k of Object.keys(raw)) {
      if (isObj(d[k]) && isObj(raw[k]) && ['profile', 'settings', 'streak', 'flags', 'warmup'].includes(k)) d[k] = { ...d[k], ...raw[k] };
      else if (Array.isArray(d[k])) d[k] = Array.isArray(raw[k]) ? raw[k] : d[k];
      else if (isObj(d[k])) d[k] = isObj(raw[k]) ? raw[k] : d[k];
      else d[k] = raw[k];
    }
    if (!isObj(d.streak.days)) d.streak.days = {};
    if (!isObj(d.streak.count)) d.streak.count = { day: null, problems: 0 };
    if (!Array.isArray(d.warmup.history)) d.warmup.history = [];
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
    return doc.lessons[id] || (doc.lessons[id] = { attempts: 0, done: false, firstTry: null, xp: 0, bestQuiz: null, mastered: false, perfect: false, completedAt: null, secondsSpent: 0, position: null, positionAt: null });
  };
  const itemRating = (difficulty) => 1000 + (Math.min(5, Math.max(1, Number(difficulty) || 1)) - 1) * 150;
  const mpFor = (difficulty) => 2 * Math.min(5, Math.max(1, Math.round(Number(difficulty) || 2)));
  const skillRec = (id) => doc.skills[id] || (doc.skills[id] = { mp: 0, elo: ELO_START, seen: 0, correct: 0, lastAt: null });
  /* Elo-style update for one graded item against each of its skills; adds MP when asked */
  const rate = (skills, ok, difficulty, { elo = true, mp = 0 } = {}) => {
    const R = itemRating(difficulty);
    (skills || []).forEach(s => {
      if (!s) return;
      const r = skillRec(s);
      r.seen++; if (ok) r.correct++; r.lastAt = now();
      if (elo) { const E = 1 / (1 + Math.pow(10, (R - r.elo) / 400)); r.elo = Math.round((r.elo + K * ((ok ? 1 : 0) - E)) * 10) / 10; }
      if (mp) r.mp += mp;
    });
  };
  /* Score each item of a set: results [{ id, ok, difficulty, skills }] if given, else wrongItems and a count of correct */
  const itemsOf = ({ results, wrongItems = [], score = 0, skills = [], difficulty = 2 }) => {
    if (Array.isArray(results) && results.length) return results.map(r => ({ id: r.id, ok: !!r.ok, difficulty: r.difficulty || difficulty, skills: r.skills || skills, ref: r.ref }));
    const wrong = wrongItems.map(w => ({ id: w.id, ok: false, difficulty: w.difficulty || difficulty, skills: w.skills || skills, ref: w.ref }));
    const right = Array.from({ length: Math.max(0, Number(score) || 0) }, (_, i) => ({ id: null, ok: true, difficulty, skills }));
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
    rec.perfect = rec.perfect || !!perfect;
    rec.completedAt = rec.completedAt || now();
    rec.secondsSpent += Math.max(0, Number(seconds) || 0);
    rec.position = null; rec.positionAt = null;
    logSeconds('main', seconds, 'lesson');
    const qualified = touch();
    changed('lessons');
    return { xp, qualified, repeat };
  };

  const quizFinished = ({ course, lesson, score = 0, items = 0, wrongItems = [], results, skills = [], seconds = 0 } = {}) => {
    const rec = lessonRec(course, lesson);
    const repeat = !!rec.bestQuiz;
    const list = itemsOf({ results, wrongItems, score, skills, difficulty: 2 });
    const correct = list.filter(x => x.ok).length;
    const total = items || list.length;
    let mp = 0;
    list.forEach(x => { const gain = x.ok && !repeat ? mpFor(x.difficulty) : 0; mp += gain; rate(x.skills, x.ok, x.difficulty, { mp: gain }); });
    const xp = repeat ? 0 : XP.quizItem * correct;
    doc.xp += xp; doc.mp += mp; rec.xp += xp;
    if (!rec.bestQuiz || correct > rec.bestQuiz[0]) rec.bestQuiz = [correct, total];
    const share = total ? correct / total : 0;
    const mastered = share >= MASTERY;
    if (mastered) rec.mastered = true;
    const redo = mastered ? [] : list.filter(x => !x.ok).map(x => redoAdd({ kind: 'quiz', ref: x.ref || { course, lesson, item: x.id }, skills: x.skills, difficulty: x.difficulty }));
    logSeconds('main', seconds, 'quiz');
    const qualified = touch();
    changed('lessons');
    return { xp, mp, mastered, redo, qualified };
  };

  const reviewFinished = ({ course, id, score = 0, items = 0, wrongItems = [], results, skills = [], seconds = 0 } = {}) => {
    const key = `${course}/${id}`;
    const repeat = !!doc.reviews[key];
    const list = itemsOf({ results, wrongItems, score, skills, difficulty: 3 });
    const correct = list.filter(x => x.ok).length;
    let mp = 0;
    list.forEach(x => { const gain = x.ok && !repeat ? mpFor(x.difficulty) : 0; mp += gain; rate(x.skills, x.ok, x.difficulty, { mp: gain }); });
    const xp = repeat ? 0 : XP.quizItem * correct;
    doc.xp += xp; doc.mp += mp;
    doc.reviews[key] = { score: correct, items: items || list.length, at: now() };
    const redo = list.filter(x => !x.ok).map(x => redoAdd({ kind: 'quiz', ref: x.ref || { course, lesson: id, item: x.id }, skills: x.skills, difficulty: x.difficulty }));
    logSeconds('main', seconds, 'review');
    const qualified = touch();
    changed('reviews');
    return { xp, mp, redo, qualified };
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
    list.forEach(x => { const gain = x.ok && !repeat ? mpFor(x.difficulty) : 0; mp += gain; rate(x.skills, x.ok, x.difficulty, { mp: gain }); });
    const xp = repeat ? 0 : XP.homework + XP.homeworkItem * correct;
    doc.xp += xp; doc.mp += mp;
    Object.assign(rec, { submitted: true, submittedAt: now(), score: correct, items: items || list.length, selfMarks });
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
    changed('skills');
    return { source, items: (results || []).length, qualified };
  };

  /* bySkill: { skill: [correct, total] }. results (optional): per-item { id, ok, difficulty, skills } for exact Elo updates.
     Each missed result with an id joins the redo queue as kind 'exam' with ref { exam, item } (ZQ.select.resolve reads it).
     extra (optional): more fields kept on the attempt. A mock exam (mock-*) earns no XP and keeps every attempt. */
  const examFinished = ({ id, score = 0, passed = false, bySkill = {}, items = 0, results, seconds = 0, extra } = {}) => {
    const rec = doc.exams[id] || (doc.exams[id] = { attempts: [] });
    const passedBefore = rec.attempts.some(a => a.passed);
    let mp = 0;
    if (Array.isArray(results) && results.length) {
      results.forEach(x => { const gain = x.ok ? mpFor(x.difficulty || 3) : 0; mp += gain; rate(x.skills || [], !!x.ok, x.difficulty || 3, { mp: gain }); });
    } else {
      Object.entries(bySkill).forEach(([s, v]) => {
        const [ok, total] = Array.isArray(v) ? v : [v, v];
        for (let i = 0; i < total; i++) { const right = i < ok, gain = right ? mpFor(3) : 0; mp += gain; rate([s], right, 3, { mp: gain }); }
      });
    }
    const xp = passed && !passedBefore && !String(id).startsWith('mock-') ? (String(id).startsWith('stage-') ? XP.stageExam : XP.topicExam) : 0; // a mock is sat many times: no XP
    doc.xp += xp; doc.mp += mp;
    rec.attempts.push({ at: now(), score, items, passed: !!passed, bySkill, ...(extra && typeof extra === 'object' ? extra : {}) }); // extra: a mock's net, wrong, blank, seed, seconds
    const redo = (Array.isArray(results) ? results : []).filter(x => x && !x.ok && (x.id != null || (x.ref && x.ref.item != null)))
      .map(x => redoAdd({ kind: 'exam', ref: x.ref && x.ref.exam ? x.ref : { exam: id, item: x.id }, skills: x.skills || [], difficulty: x.difficulty || 3 }));
    logSeconds('main', seconds, 'exam');
    changed('exams');
    return { xp, mp, redo };
  };

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
      if (!rec.verified && !rec.code) delete doc.drills[id];
    } else {
      const r = rec || (doc.drills[id] = { verified: false, code: '', at: null });
      if (r.draft === String(code)) return r.draft;
      r.draft = String(code); r.draftAt = now();
    }
    changed('drills');
    return code ?? null;
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
          const done = ls.filter(x => doc.lessons[lessonId(c.id, x.id)] && doc.lessons[lessonId(c.id, x.id)].done).length;
          courseProgress[c.id] = ls.length ? done / ls.length : 0;
        });
      } catch (e) { console.error(e); }
    }
    const skillMastery = {};
    Object.entries(doc.skills).forEach(([k, v]) => { skillMastery[k] = v.seen ? Math.min(1, Math.max(0, (v.elo - 1000) / 600)) : 0; });
    const due = redoDue();
    const open = lessons.filter(([, r]) => !r.done && r.position != null).sort((a, b) => (b[1].positionAt || 0) - (a[1].positionAt || 0));
    const resume = open.length ? (() => { const [id, r] = open[0]; const [course, lesson] = id.split('/'); return { course, lesson, position: r.position, at: r.positionAt }; })() : null;
    const homeworkOpen = Object.entries(doc.homework).filter(([, h]) => !h.submitted).map(([id, h]) => ({ id, course: id.split('/')[0], due: h.due, overdue: h.due < now() })).sort((a, b) => a.due - b.due);
    const goal = doc.profile.weeklyGoalH || 15;
    return {
      name: doc.profile.name, initial: doc.profile.initial || (doc.profile.name || '?').charAt(0).toUpperCase(), track: doc.profile.track,
      streak: s.current, best: s.best, todayQualified: s.days[today] === true, restDays: s.restDays,
      restProgress: (qualifiedTotal() - (s.restEarnedAt || 0)) % REST_EVERY, problemsToday: s.count.day === today ? s.count.problems : 0,
      streakOff: doc.settings.streakMode === 'off', week,
      xp: doc.xp, mp: doc.mp,
      hoursWeek, hoursWeekTotal: Math.round(Object.values(hoursWeek).reduce((a, b) => a + b, 0) * 100) / 100, weeklyGoalH: goal, weekGoal: weeklySplit(goal),
      lessonsDone: lessons.filter(([, r]) => r.done).length, mastered: lessons.filter(([, r]) => r.mastered).length,
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
    profile: ns('profile', { set: profileSet, get: () => doc.profile }),
    settings: ns('settings', { set: settingsSet, get: () => doc.settings }),
    flags: ns('flags', { set: flagsSet, get: () => doc.flags }),
    streak: ns('streak', { touch, rollover: () => { const r = rollover(); if (r) changed('streak'); return r; }, get: () => doc.streak }),
    redo: ns('redo', { add: redoAdd, due: redoDue, result: redoResult, list: () => doc.redo.slice() }),
    notebook: ns('notebook', { add: notebookAdd, list: () => doc.notebook.slice() }),
    drills: ns('drills', { verified: drillVerified, draft: drillDraft, get: (id) => (id == null ? doc.drills : doc.drills[id] || null) }),
    warmup: ns('warmup', { record: warmupRecord, list: () => doc.warmup.history.slice() }),
    hours: ns('hours', { log: logHours, list: () => doc.hours.slice() }),
    lessonPosition: { set: positionSet, get: positionGet },
    lesson: (course, lesson) => doc.lessons[lessonId(course, lesson)] || null,
    screenGraded, lessonFinished, quizFinished, reviewFinished, homeworkAssigned, homeworkSubmitted, examFinished, practiceResult,
    summary, weeklySplit,
    export: exportDoc, import: importDoc, reset, flush,
    dates, rules: { XP, MASTERY, REDO_FIRST, REDO_SECOND, REST_EVERY, REST_MAX, QUALIFY_PROBLEMS, K, ELO_START, BLOCKS, TRACKS, GOALS, itemRating, mpFor },
    /* Test hook: replace the clock (a function returning ms) and reload from storage. Not for screens. */
    _setClock(fn) { clock = typeof fn === 'function' ? fn : () => Date.now(); },
    _reload() { doc = read(); return doc; },
  };
  if (rollover()) flush();
  window.ZQ = window.ZQ || {};
  window.ZQ.state = api;
})();
