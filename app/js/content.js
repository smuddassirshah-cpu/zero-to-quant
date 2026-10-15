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
  const stages = () => (curriculum ? curriculum.stages : []);
  const stage = (n) => stages().find(s => s.id === Number(n)) || null;
  const topic = (id) => { for (const s of stages()) for (const t of s.topics) if (t.id === String(id)) return { ...t, stage: s.id }; return null; };
  const topicOfCourse = (cid) => { for (const s of stages()) for (const t of s.topics) if ((t.courses || []).includes(cid)) return { s, t }; return null; };
  const course = (id) => {
    if (!curriculum || !curriculum.courses[id]) return null;
    const meta = curriculum.courses[id], doc = courseDocs[id] || {};
    const where = topicOfCourse(id);
    return {
      id, ...meta, ...doc,
      name: doc.name || meta.name, art: doc.art || meta.art, description: doc.description || meta.description,
      topic: (where && where.t.id) || meta.topic, topicName: where ? where.t.name : '', stage: where ? where.s.id : null, track: where ? where.t.track : null,
      skills: doc.skills || {}, levels: doc.levels || [], loaded: !!courseDocs[id],
    };
  };
  const courses = () => stages().flatMap(s => s.topics.flatMap(t => (t.courses || []).map(id => course(id)).filter(Boolean)));

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
  const exam = (id) => load(`exams/${id}.json`);
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
    stages, stage, topic, course, courses, courseLessons, next, exists,
    lesson, review, homework, exam, drill, drills,
    /* Resolves when every lesson, review and homework file of a course is known to exist or not */
    probe: (cid) => Promise.all(courseLessons(cid).map(x => load(`courses/${cid}/${x.id}.json`).catch(() => null))).then(() => courseLessons(cid)),
    deKebab,
  };
  window.ZQ = window.ZQ || {};
  window.ZQ.content = api;
})();
