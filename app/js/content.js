/* Content loader and registry (docs/PLAN.md section 5). At start it fetches content/curriculum.json, then every
   course.json it lists, in parallel; ZQ.content.ready resolves when both are in. Lessons, reviews, homework, exams and
   drills are fetched on demand and cached. content/manifest.json (written by tools/validate.mjs) lists every authored
   file, so a lesson that is not written yet is known as missing without a request; without a manifest, a 404 is
   cached as missing, never thrown. Course art ids are the kinds in js/art.js (ZQArt.kinds). */
(function () {
  'use strict';
  const BASE = 'content/';
  let curriculum = null;          // curriculum.json as loaded
  const courseDocs = {};          // course id -> course.json (or null when it failed to load)
  let manifest = null;            // Set of paths relative to content/, or null when there is no manifest
  const cache = new Map();        // path -> Promise<object|null>
  const known = new Map();        // path -> true (found) | false (missing)
  let drillIndex = null;

  const deKebab = (id) => {
    const s = String(id).replace(/^l\d+-/, '').replace(/-/g, ' ');
    return s.charAt(0).toUpperCase() + s.slice(1);
  };
  const getJSON = async (path, { optional = false } = {}) => {
    const res = await fetch(BASE + path, { cache: 'no-cache' });
    if (res.status === 404 && optional) return null;
    if (!res.ok) throw new Error(`content/${path}: HTTP ${res.status}`);
    try { return await res.json(); } catch (e) { throw new Error(`content/${path}: ${e.message}`); }
  };
  /* Fetch once and cache. Missing files resolve to null; malformed files reject (and are logged once). */
  const load = (path) => {
    if (cache.has(path)) return cache.get(path);
    let p;
    if (manifest && !manifest.has(path)) { known.set(path, false); p = Promise.resolve(null); }
    else {
      p = getJSON(path, { optional: true }).then(d => { known.set(path, d != null); return d; })
        .catch(e => { console.error(e); known.set(path, false); cache.delete(path); throw e; });
    }
    cache.set(path, p);
    return p;
  };

  /* ---------- Registry over the curriculum ---------- */
  /* Strands: a course.json may carry strand ("quant" or "pure") and strandNote (the roles). The "Quant path only"
     setting hides pure courses and the topics that hold only pure courses from stages() and courses(); topic(),
     course() and stage() still find everything, so a link or a saved resume point to a pure course keeps working. */
  const quantOnly = () => { try { const S = window.ZQ && window.ZQ.state; return !!(S && S.settings && S.settings.quantOnly); } catch { return false; } };
  const isPure = (id) => { const m = (curriculum && curriculum.courses[id]) || {}, d = courseDocs[id] || {}; return (d.strand || m.strand) === 'pure'; };
  const strandOfCourse = (id) => { const m = (curriculum && curriculum.courses[id]) || {}, d = courseDocs[id] || {}; const v = d.strand || m.strand; return v === 'pure' || v === 'quant' ? v : null; };
  /* A topic has a strand when every one of its courses carries the same one; mixed or untagged topics have none */
  const topicStrand = (t) => {
    const ids = (t && t.courses) || [];
    const set = new Set(ids.map(id => strandOfCourse(id) || ''));
    return set.size === 1 && ids.length && [...set][0] ? [...set][0] : null;
  };
  const strandNoteOf = (ids) => {
    const notes = [...new Set((ids || []).map(id => (courseDocs[id] || {}).strandNote).filter(Boolean))];
    return notes.join(' ');
  };
  const STRAND_NAME = { pure: 'Pure maths', quant: 'Quant' };
  const escAttr = (v) => String(v).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
  /* The badge markup for a strand with its note as the tooltip and the screen-reader detail; '' for no strand */
  const strandBadge = (strand, note = '', cls = '') => {
    if (!STRAND_NAME[strand]) return '';
    const n = escAttr(note || (strand === 'pure' ? 'Pure maths: not needed to be hired.' : 'Quant path: used in quant roles.'));
    return `<span class="strand-badge is-${strand}${cls ? ' ' + cls : ''}" title="${n}" aria-label="${STRAND_NAME[strand]}. ${n}">${STRAND_NAME[strand]}</span>`;
  };
  const allStages = () => (curriculum ? curriculum.stages : []);
  const stages = () => {
    const all = allStages();
    if (!quantOnly()) return all;
    return all.map(s => ({
      ...s,
      topics: s.topics.flatMap(t => {
        const cs = t.courses || [], kept = cs.filter(id => !isPure(id));
        if (cs.length && !kept.length) return [];
        return [kept.length === cs.length ? t : { ...t, courses: kept }];
      }),
    }));
  };
  const stage = (n) => allStages().find(s => s.id === Number(n)) || null;
  const topic = (id) => { for (const s of allStages()) for (const t of s.topics) if (t.id === String(id)) return { ...t, stage: s.id }; return null; };
  const topicOfCourse = (cid) => { for (const s of allStages()) for (const t of s.topics) if ((t.courses || []).includes(cid)) return { s, t }; return null; };
  /* Tested out: a passed topic exam, read from the saved attempts at call time (nothing stored per lesson).
     Today and the "up next" course skip a course whose topic is passed; lesson flags and progress are untouched. */
  const topicPassed = (tid) => {
    try { const r = window.ZQ.state.exams['topic-' + tid]; return !!(r && Array.isArray(r.attempts) && r.attempts.some(a => a && a.passed)); } catch { return false; }
  };
  const courseTestedOut = (cid) => { const w = topicOfCourse(cid); return !!w && topicPassed(w.t.id); };
  const course = (id) => {
    if (!curriculum || !curriculum.courses[id]) return null;
    const meta = curriculum.courses[id], doc = courseDocs[id] || {};
    const where = topicOfCourse(id);
    return {
      id, ...meta, ...doc,
      name: doc.name || meta.name, art: doc.art || meta.art, description: doc.description || meta.description,
      topic: (where && where.t.id) || meta.topic, topicName: where ? where.t.name : '', stage: where ? where.s.id : null, track: where ? where.t.track : null,
      skills: doc.skills || {}, levels: doc.levels || [], loaded: !!courseDocs[id],
      strand: strandOfCourse(id), strandNote: strandOfCourse(id) ? (doc.strandNote || '') : '',
    };
  };
  const allCourses = () => allStages().flatMap(s => s.topics.flatMap(t => (t.courses || []).map(id => course(id)).filter(Boolean)));
  const courses = () => (quantOnly() ? allCourses().filter(c => c.strand !== 'pure') : allCourses());

  /* Ordered list of everything on a course map: each level's lessons, then its review, then its homework */
  const lessonCache = new Map();  // `${course}/${id}` -> loaded lesson title, for names when the map has none
  const nameOf = (doc, id) => (doc.lessonNames && doc.lessonNames[id]) || lessonCache.get(`${doc.id}/${id}`) || deKebab(id);
  const courseLessons = (id) => {
    const doc = courseDocs[id];
    if (!doc || !Array.isArray(doc.levels)) return [];
    const out = [];
    doc.levels.forEach(lv => {
      (lv.lessons || []).forEach(l => out.push({ level: lv.n, id: l, kind: 'lesson', name: nameOf(doc, l), objective: (doc.lessonObjectives || {})[l] || '', written: exists(id, l) }));
      if (lv.review) out.push({ level: lv.n, id: lv.review, kind: 'review', name: 'Level review', written: exists(id, lv.review) });
      if (lv.homework) out.push({ level: lv.n, id: lv.homework, kind: 'homework', name: `Homework ${lv.n}`, written: exists(id, lv.homework) });
    });
    return out;
  };
  const next = (cid, afterId) => {
    const list = courseLessons(cid);
    const i = list.findIndex(x => x.id === afterId);
    return i >= 0 && i + 1 < list.length ? list[i + 1] : null;
  };
  /* true: the file is there; false: it is not written yet; null: not known yet (no manifest, never fetched) */
  const exists = (cid, id) => {
    const path = `courses/${cid}/${id}.json`;
    if (known.has(path)) return known.get(path);
    if (manifest) return manifest.has(path);
    return null;
  };

  const lesson = (cid, id) => load(`courses/${cid}/${id}.json`).then(d => { if (d && d.title) lessonCache.set(`${cid}/${id}`, d.title); return d; });
  const review = (cid, id) => load(`courses/${cid}/${id}.json`);
  const homework = (cid, id) => load(`courses/${cid}/${id}.json`);
  /* true or false from the manifest; null when there is no manifest */
  const examWritten = (id) => (manifest ? manifest.has(`exams/${id}.json`) : null);
  const exam = (id) => load(`exams/${id}.json`);
  /* The mock assessments written (exams/mock-*.json in the manifest), sorted by id; empty while there is no manifest */
  const mocks = () => (manifest ? [...manifest].filter(f => /^exams\/mock-[^/]+\.json$/.test(f)).map(f => f.slice(6, -5)).sort() : []);
  const drill = (id) => load(`drills/${id}.json`);
  const drills = () => drillIndex || [];

  /* ---------- Start ---------- */
  const ready = (async () => {
    const [cur, man, di] = await Promise.all([
      getJSON('curriculum.json'),
      getJSON('manifest.json', { optional: true }).catch(e => { console.error(e); return null; }),
      getJSON('drills/index.json', { optional: true }).catch(e => { console.error(e); return null; }),
    ]);
    curriculum = cur;
    if (man && Array.isArray(man.files)) { manifest = new Set(man.files); manifest.forEach(f => known.set(f, true)); }
    drillIndex = Array.isArray(di) ? di : [];
    const ids = Object.keys(cur.courses || {});
    await Promise.all(ids.map(id => getJSON(`courses/${id}/course.json`).then(d => { courseDocs[id] = d; })
      .catch(e => { console.error(e); courseDocs[id] = null; })));
    return api;
  })();
  ready.catch(e => console.error('Content failed to load:', e));

  const api = {
    ready,
    get curriculum() { return curriculum; },
    get tracks() { return (curriculum && curriculum.tracks) || {}; },
    stages, allStages, stage, topic, topicPassed, courseTestedOut, course, courses, allCourses, topicStrand, strandNoteOf, strandBadge, quantOnly, courseLessons, next, exists,
    lesson, review, homework, exam, examWritten, mocks, drill, drills,
    /* Resolves when every lesson, review and homework file of a course is known to exist or not */
    probe: (cid) => Promise.all(courseLessons(cid).map(x => load(`courses/${cid}/${x.id}.json`).catch(() => null))).then(() => courseLessons(cid)),
    deKebab,
  };
  window.ZQ = window.ZQ || {};
  window.ZQ.content = api;
})();
