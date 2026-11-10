/* Workload, one source (PLAN 2c item 11, ENGINE-BACKLOG 559 to 563; author side docs/AUTHORING.md section 14, figures docs/curriculum.md).
   Pure functions, no screens, no DOM: loaded by index.html as ZQ.hours and by the node tools (readiness-sums, census,
   curriculum-hours) with require('../js/hours.js'), like js/prereq.js. Nothing else computes hours.

   The contract (docs/readiness.md). A topic's hours are stored on the topic in curriculum.json: the estimate for a learner
   starting from zero, practice included. A stage's hours are never stored: they are the sum of its topic hours (a stored
   stage `hours` field is ignored, and item 11's content script removes it). A topic's hours are shared across its courses,
   and a course's across its lessons, in proportion to each lesson's weight:
     weight 1 for a short lesson (the 11 to 15 minute default), minutes / 14 for a workshop or project (item 10), so a true
     60 minute workshop takes about four short lessons' share of its topic. With no workshop or project the shares are the
     old mapped-lesson counts, so no figure moves until item 10's content script runs. A topic with no mapped lesson shares nothing.
   A role's hours are the readiness.json totals (required plus recommended for the Learn header), which readiness-sums.mjs
   writes by calling roleSums below: the lessons written count their share as "written", the rest as "unwritten".

   In-app hours (session Y; AUTHORING section 14). Stored hours are the whole estimate: time in the app plus study outside it. The in-app
   part is counted from minutes: each lesson's authored `minutes` (SHORT_NORM when the lesson is not written), plus each level's review
   and homework (their file's `minutes` where it states one, else REVIEW_MIN and HOMEWORK_MIN), plus the topic's exam (examMinutes, else
   EXAM_MIN) shared across the topic's courses by lesson weight. Outside hours are stored minus in-app, floored at 0: per lesson and per
   course (a course's outside is the stored share minus its own in-app, so the two are floored separately), per topic from the topic's stored hours,
   a stage as the sum of its topics, a role as the sum of its courses. A surface shows the two apart, in-app first (splitLabel), never the stored total alone.

   Inputs (build): { curriculum, courses: { id: course.json doc or null }, written: (cid, lessonId) => bool,
   sessions: { "cid/lessonId": { session, minutes } } (workshop and project lessons only), minutes: (cid, lessonId) => number | undefined,
   setMinutes: { "cid/review-1": minutes } (reviews and homework whose file states minutes), examMinutes: { "topic-0.1": minutes },
   problemsMinutes: { "cid/problems-1": minutes } (the level problem sets written, ENGINE-BACKLOG 845 to 851: the file's `minutes`, else PROBLEMS_MIN, which the validator writes into the manifest; a level with no set adds nothing) }. */
(function (root) {
  'use strict';
  const SHORT_NORM = 14;                         // the median short lesson, minutes: the weight unit
  const WEEKLY_H = 15;                           // the curriculum's reference week
  const SESSION_RANGE = { short: [5, 20], workshop: [20, 90], project: [60, 240] };   // minutes the validator accepts per session
  const SESSIONS = Object.keys(SESSION_RANGE);
  const REVIEW_MIN = 20, HOMEWORK_MIN = 45, EXAM_MIN = 60, PROBLEMS_MIN = 40;   // minutes allowed for a level review, a level homework and a topic exam whose file states none

  const topicHours = (t) => (t && Number(t.hours)) || 0;
  const stageHours = (s) => ((s && s.topics) || []).reduce((a, t) => a + topicHours(t), 0);
  const totalHours = (cur) => ((cur && cur.stages) || []).reduce((a, s) => a + stageHours(s), 0);
  /* Whole months at a weekly rate: 555 h at 15 h a week is about 9 months */
  const months = (h, weekly = WEEKLY_H) => Math.round(h / weekly * 12 / 52);

  const weightOf = (e) => (!e || !e.session || e.session === 'short' ? 1 : Math.max(1, Number(e.minutes) / SHORT_NORM) || 1);
  const sessionLabel = (session, minutes) => (session === 'workshop' ? 'Workshop' : session === 'project' ? 'Project' : 'Short') + (minutes ? `, ${Math.round(minutes)} min` : '');
  /* The line a course card shows for the workshop and project lessons it holds: "Workshop, 60 min", "2 workshops, 60 to 90 min", "Project, 180 min" */
  function courseSessionLabel(entries) {
    const es = (entries || []).filter(e => e && (e.session === 'workshop' || e.session === 'project'));
    if (!es.length) return '';
    const kinds = [...new Set(es.map(e => e.session))];
    const word = kinds.length > 1 ? 'session' : kinds[0];
    const lo = Math.min(...es.map(e => e.minutes)), hi = Math.max(...es.map(e => e.minutes));
    const name = es.length === 1 ? word.charAt(0).toUpperCase() + word.slice(1) : `${es.length} ${word}s`;
    return `${name}, ${lo === hi ? lo : lo + ' to ' + hi} min`;
  }

  /* "12 h", "3.5 h", "1,650 h": whole hours from 10 up, one decimal below */
  const fmtH = (h) => { const r = h >= 10 ? Math.round(h) : Math.round(h * 10) / 10; return r.toLocaleString('en-GB'); };
  /* The two figures together, in-app first: "about 150 h in the app, about 1,650 h of outside study"; short for a tight spot: "12 h in the app, 48 h outside" */
  const splitLabel = (app, out, { short = false } = {}) => (short ? `${fmtH(app)} h in the app, ${fmtH(out)} h outside` : `about ${fmtH(app)} h in the app, about ${fmtH(out)} h of outside study`);

  function build({ curriculum, courses = {}, written = () => true, sessions = {}, minutes = () => undefined, setMinutes = {}, examMinutes = {}, problemsMinutes = {} } = {}) {
    const stages = (curriculum && curriculum.stages) || [];
    const topicOfCourse = {}, stageOfTopic = {};
    for (const s of stages) for (const t of s.topics || []) { stageOfTopic[t.id] = s.id; for (const c of t.courses || []) topicOfCourse[c] = t.id; }
    const topicRec = {};
    for (const s of stages) for (const t of s.topics || []) topicRec[t.id] = t;
    const cidTopic = (cid) => (courses[cid] && courses[cid].topic) || (curriculum && curriculum.courses && curriculum.courses[cid] && curriculum.courses[cid].topic) || topicOfCourse[cid];
    const lessonsOf = (cid, n) => {
      const d = courses[cid]; if (!d) return [];
      return (d.levels || []).filter(lv => n == null || lv.n === n).flatMap(lv => (lv.lessons || []).map(id => ({ id, level: lv.n })));
    };
    const wOf = (cid, id) => weightOf(sessions[`${cid}/${id}`]);
    const courseW = (cid) => lessonsOf(cid).reduce((a, l) => a + wOf(cid, l.id), 0);
    const topicW = {};
    for (const cid of Object.keys(courses)) { const t = cidTopic(cid); if (t) topicW[t] = (topicW[t] || 0) + courseW(cid); }
    const lesson = (cid, id) => { const t = cidTopic(cid), W = topicW[t]; return W ? topicHours(topicRec[t]) * wOf(cid, id) / W : 0; };
    const level = (cid, n) => lessonsOf(cid, n).reduce((a, l) => a + lesson(cid, l.id), 0);
    const course = (cid) => lessonsOf(cid).reduce((a, l) => a + lesson(cid, l.id), 0);
    const courseWritten = (cid) => lessonsOf(cid).reduce((a, l) => a + (written(cid, l.id) ? lesson(cid, l.id) : 0), 0);
    const courseCounts = (cid) => { const ls = lessonsOf(cid); const w = ls.filter(l => written(cid, l.id)).length; return { mapped: ls.length, written: w }; };
    /* Hours the topic's lessons would carry if each counted its stated minutes (written lessons' own, unwritten at SHORT_NORM): the figure for a topic that stores 0 */
    const topicFromMinutes = (tid) => {
      let m = 0;
      for (const cid of Object.keys(courses)) if (cidTopic(cid) === tid) for (const l of lessonsOf(cid)) {
        const e = sessions[`${cid}/${l.id}`];
        m += (e && e.minutes) || (written(cid, l.id) && minutes(cid, l.id)) || SHORT_NORM;
      }
      return m / 60;
    };
    /* In-app hours (see the header): minutes of lessons, level reviews and homework, and the topic exam's share */
    const lessonMin = (cid, id) => { const e = sessions[`${cid}/${id}`]; return (e && Number(e.minutes)) || (written(cid, id) && Number(minutes(cid, id))) || SHORT_NORM; };
    const setMin = (cid, kind, n) => Number(setMinutes[`${cid}/${kind}-${n}`]) || (kind === 'review' ? REVIEW_MIN : HOMEWORK_MIN);
    const problemsMin = (cid, n) => Number(problemsMinutes[`${cid}/problems-${n}`]) || 0;   // a level's problem set (ENGINE-BACKLOG 845 to 851): its stated minutes, else 40 (the manifest carries the figure); 0 where the level has none
    const examMin = (tid) => Number(examMinutes[`topic-${tid}`]) || EXAM_MIN;
    const lessonApp = (cid, id) => lessonMin(cid, id) / 60;
    const levelApp = (cid, n) => { const ls = lessonsOf(cid, n); return ls.length ? (ls.reduce((a, l) => a + lessonMin(cid, l.id), 0) + setMin(cid, 'review', n) + setMin(cid, 'homework', n) + problemsMin(cid, n)) / 60 : 0; };
    const courseApp = (cid) => {
      const d = courses[cid]; if (!d) return 0;
      const t = cidTopic(cid), W = topicW[t];
      return (d.levels || []).reduce((a, lv) => a + levelApp(cid, lv.n), 0) + (W ? examMin(t) / 60 * courseW(cid) / W : 0);
    };
    const topicApp = (tid) => Object.keys(courses).filter(cid => cidTopic(cid) === tid).reduce((a, cid) => a + courseApp(cid), 0);
    const outside = (stored, app) => Math.max(0, stored - app);
    const lessonOut = (cid, id) => outside(lesson(cid, id), lessonApp(cid, id));
    const courseOut = (cid) => outside(course(cid), courseApp(cid));
    const topicOut = (tid) => outside(topicHours(topicRec[tid]), topicApp(tid));
    const stageOf = (sid) => stages.find(s => s.id === Number(sid));
    const stageApp = (sid) => ((stageOf(sid) || {}).topics || []).reduce((a, t) => a + topicApp(t.id), 0);
    const stageOut = (sid) => ((stageOf(sid) || {}).topics || []).reduce((a, t) => a + topicOut(t.id), 0);
    /* A role's sums over the courses whose status is in `statuses`: lessons and hours, written and unwritten (hours rounded as the readiness contract rounds them); app and out are the in-app and outside hours */
    const roleSums = (statusOf, statuses) => {
      let w = 0, u = 0, hw = 0, hu = 0, app = 0, out = 0;
      for (const cid of Object.keys(courses)) {
        if (!statuses.includes(statusOf(cid))) continue;
        const c = courseCounts(cid), h = course(cid), hwc = courseWritten(cid);
        w += c.written; u += c.mapped - c.written; hw += hwc; hu += h - hwc; app += courseApp(cid); out += courseOut(cid);
      }
      return { w, u, hw: Math.round(hw), hu: Math.round(hu), app: Math.round(app), out: Math.round(out) };
    };
    return {
      lesson, level, course, courseWritten, courseCounts,
      topic: (tid) => topicHours(topicRec[tid]),
      stage: (sid) => stageHours(stageOf(sid)),
      total: () => totalHours(curriculum),
      lessonApp, levelApp, courseApp, topicApp, stageApp, totalApp: () => stages.reduce((a, s) => a + stageApp(s.id), 0),
      lessonOut, courseOut, topicOut, stageOut, totalOut: () => stages.reduce((a, s) => a + stageOut(s.id), 0),
      topicFromMinutes, roleSums, weight: wOf,
    };
  }

  /* The readiness.json totals for a role: { required, recommended, header } each { written, unwritten, total, hoursWritten, hoursUnwritten, hours }, or null */
  const role = (readinessDoc, key) => { const r = readinessDoc && readinessDoc.roles && readinessDoc.roles[key]; return r ? r.totals : null; };

  const api = { SHORT_NORM, WEEKLY_H, SESSION_RANGE, SESSIONS, REVIEW_MIN, HOMEWORK_MIN, EXAM_MIN, PROBLEMS_MIN, fmtH, splitLabel, topicHours, stageHours, totalHours, months, weightOf, sessionLabel, courseSessionLabel, build, role };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  if (root) { root.ZQ = root.ZQ || {}; root.ZQ.hours = api; }
})(typeof window !== 'undefined' ? window : null);
