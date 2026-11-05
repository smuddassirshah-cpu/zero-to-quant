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

   Inputs (build): { curriculum, courses: { id: course.json doc or null }, written: (cid, lessonId) => bool,
   sessions: { "cid/lessonId": { session, minutes } } (workshop and project lessons only), minutes: (cid, lessonId) => number | undefined }. */
(function (root) {
  'use strict';
  const SHORT_NORM = 14;                         // the median short lesson, minutes: the weight unit
  const WEEKLY_H = 15;                           // the curriculum's reference week
  const SESSION_RANGE = { short: [5, 20], workshop: [20, 90], project: [60, 240] };   // minutes the validator accepts per session
  const SESSIONS = Object.keys(SESSION_RANGE);

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

  function build({ curriculum, courses = {}, written = () => true, sessions = {}, minutes = () => undefined } = {}) {
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
    /* A role's sums over the courses whose status is in `statuses`: lessons and hours, written and unwritten (hours rounded as the readiness contract rounds them) */
    const roleSums = (statusOf, statuses) => {
      let w = 0, u = 0, hw = 0, hu = 0;
      for (const cid of Object.keys(courses)) {
        if (!statuses.includes(statusOf(cid))) continue;
        const c = courseCounts(cid), h = course(cid), hwc = courseWritten(cid);
        w += c.written; u += c.mapped - c.written; hw += hwc; hu += h - hwc;
      }
      return { w, u, hw: Math.round(hw), hu: Math.round(hu) };
    };
    return {
      lesson, level, course, courseWritten, courseCounts,
      topic: (tid) => topicHours(topicRec[tid]),
      stage: (sid) => stageHours(stages.find(s => s.id === Number(sid))),
      total: () => totalHours(curriculum),
      topicFromMinutes, roleSums, weight: wOf,
    };
  }

  /* The readiness.json totals for a role: { required, recommended, header } each { written, unwritten, total, hoursWritten, hoursUnwritten, hours }, or null */
  const role = (readinessDoc, key) => { const r = readinessDoc && readinessDoc.roles && readinessDoc.roles[key]; return r ? r.totals : null; };

  const api = { SHORT_NORM, WEEKLY_H, SESSION_RANGE, SESSIONS, topicHours, stageHours, totalHours, months, weightOf, sessionLabel, courseSessionLabel, build, role };
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
  if (root) { root.ZQ = root.ZQ || {}; root.ZQ.hours = api; }
})(typeof window !== 'undefined' ? window : null);
