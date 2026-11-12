/* Green-hash cache for tools/playthrough.mjs --changed (engine pass AC part 1).
   An item (lesson, set, fluency set, problem set, exam, bank file, drill, session, the routes) that passed is recorded with one hash of everything
   its page reads; --changed replays only the items whose current hash differs from, or is absent from, the cache. See the playthrough usage header
   and docs/AUTHORING.md for the author-facing summary, docs/reports/engine-pass-ac-1.md for the dependency set per kind.

   Cache file: { "version": 1, "entries": { "<kind>|<id>|<mode>": "<sha1>" } }. A mode is the viewports the item was played at, joined with "+"
   (desktop, mobile, narrow, tablet); a green recorded for a superset of the requested modes also counts (desktop+mobile covers desktop).
   Writes take a mkdir lock, re-read the file, merge, write a temporary file and rename it, so concurrent shards lose no entry. */
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { fileURLToPath } from 'node:url';

const sha = (b) => crypto.createHash('sha1').update(b).digest('hex');
const SELF = fileURLToPath(import.meta.url);

/* ---------- The cache file ---------- */
export const readCache = (file) => {
  try { const j = JSON.parse(fs.readFileSync(file, 'utf8')); return j && typeof j.entries === 'object' && j.entries ? j.entries : {}; } catch { return {}; }
};
const sleepMs = (ms) => { try { Atomics.wait(new Int32Array(new SharedArrayBuffer(4)), 0, 0, ms); } catch { const t = Date.now() + ms; while (Date.now() < t) { /* spin */ } } };
const withLock = (file, fn) => {
  const lock = file + '.lock', t0 = Date.now();
  fs.mkdirSync(path.dirname(file), { recursive: true });
  for (;;) {
    try { fs.mkdirSync(lock); break; } catch (e) {
      if (e.code !== 'EEXIST') throw e;
      let age = 0; try { age = Date.now() - fs.statSync(lock).mtimeMs; } catch { continue; }   // released while we looked: try again
      if (age > 15000 || Date.now() - t0 > 30000) { try { fs.rmdirSync(lock); } catch { /* another process took it */ } continue; }   // a crashed holder, or we waited far too long
      sleepMs(5 + Math.floor(Math.random() * 25));
    }
  }
  try { return fn(); } finally { try { fs.rmdirSync(lock); } catch { /* already gone */ } }
};
/* Merge `entries` ({ key: hash }) into the cache file: lock, re-read, merge, atomic rename. */
export const writeGreen = (file, entries) => {
  if (!entries || !Object.keys(entries).length) return;
  withLock(file, () => {
    const cur = readCache(file);
    Object.assign(cur, entries);
    const tmp = `${file}.${process.pid}.${crypto.randomBytes(4).toString('hex')}.tmp`;
    fs.writeFileSync(tmp, JSON.stringify({ version: 1, entries: Object.fromEntries(Object.keys(cur).sort().map(k => [k, cur[k]])) }) + '\n');
    fs.renameSync(tmp, file);
  });
};
export const modeName = (modes) => [...new Set(modes)].join('+');
export const keyOf = (kind, id, modes) => `${kind}|${id}|${modeName(modes)}`;
/* lookup(kind, id, modes, hash): true when a green is recorded with this hash for a mode set that covers `modes` */
export const makeLookup = (entries) => {
  const by = new Map();
  for (const [k, h] of Object.entries(entries || {})) {
    const [kind, id, mode] = k.split('|');
    const key = kind + '|' + id;
    if (!by.has(key)) by.set(key, []);
    by.get(key).push([new Set(String(mode).split('+')), h]);
  }
  return (kind, id, modes, hash) => (by.get(kind + '|' + id) || []).some(([set, h]) => h === hash && modes.every(m => set.has(m)));
};

/* ---------- Hashing ---------- */
export const stable = (v) => JSON.stringify(v, (k, x) => (x && typeof x === 'object' && !Array.isArray(x) ? Object.fromEntries(Object.keys(x).sort().map(y => [y, x[y]])) : x));

/* createHasher({ appDir, selfFile }): every file is read at most once per hasher, so the hashes are a snapshot taken when the run starts. */
export const createHasher = ({ appDir, selfFile }) => {
  const content = path.join(appDir, 'content');
  const memo = new Map();
  const text = new Map();
  const fh = (abs) => {
    if (memo.has(abs)) return memo.get(abs);
    let h = '-';
    try { const b = fs.readFileSync(abs); h = sha(b); if (abs.endsWith('.json') && b.length < 4e6) text.set(abs, b.toString('utf8')); } catch { /* absent */ }
    memo.set(abs, h); return h;
  };
  const txt = (abs) => { fh(abs); if (text.has(abs)) return text.get(abs); try { return fs.readFileSync(abs, 'utf8'); } catch { return ''; } };
  const parse = (abs) => { try { return JSON.parse(txt(abs)); } catch { return null; } };
  const C = (...p) => path.join(content, ...p);
  const names = (dir) => { try { return fs.readdirSync(dir).filter(f => !f.startsWith('.')).sort(); } catch { return []; } };
  const walk = (dir, out = []) => {
    let ents = []; try { ents = fs.readdirSync(dir, { withFileTypes: true }); } catch { return out; }
    ents.sort((a, b) => (a.name < b.name ? -1 : a.name > b.name ? 1 : 0));
    for (const e of ents) { if (e.name.startsWith('.')) continue; const p = path.join(dir, e.name); if (e.isDirectory()) walk(p, out); else out.push(p); }
    return out;
  };
  const rel = (abs) => path.relative(appDir, abs).split(path.sep).join('/');
  const filesHash = (list) => sha(list.map(p => rel(p) + ' ' + fh(p)).join('\n'));

  /* The manifest (content/manifest.json) is rewritten by the validator and holds only data derived from the content files plus the file list. It is never
     hashed as bytes. A normalised copy (note dropped, keys sorted) is hashed for the routes, and each item hashes the slices of it that its page reads
     (its own minutes, session, fluency, problems, drill and exam entries, the perf entries of its course, whether its file is listed and whether it is a sample). */
  let man;
  const manifest = () => { if (man === undefined) { man = parse(C('manifest.json')); } return man; };
  const mslice = (picks) => {
    const m = manifest(); if (!m) return 'no-manifest';
    const out = {};
    for (const [field, key] of picks) { const v = m[field]; if (Array.isArray(v)) out[field + ':' + key] = v.includes(key); else if (v && typeof v === 'object') out[field + ':' + key] = v[key] === undefined ? null : v[key]; }
    return stable(out);
  };
  const mperf = (course) => { const m = manifest(); const p = (m && m.perf) || {}; return stable(Object.keys(p).filter(k => k.startsWith(course + '/')).sort().map(k => [k, p[k]])); };
  const manifestNormal = () => { const m = manifest(); if (!m) return 'no-manifest'; const { note, ...rest } = m; void note; return sha(stable(rest)); };

  /* Every course.json is read by the app at start (skills, requires, strands, hours), so the other courses count, but not their lesson lists and names,
     which only their own pages use: a lesson added elsewhere does not invalidate this course. */
  const courseIds = () => names(C('courses')).filter(c => fs.existsSync(C('courses', c, 'course.json')));
  const graphMemo = new Map();
  const graph = (exclude) => {
    const k = exclude || '';
    if (graphMemo.has(k)) return graphMemo.get(k);
    const parts = courseIds().filter(c => c !== exclude).map(c => {
      const d = parse(C('courses', c, 'course.json'));
      if (!d) return c + ':' + fh(C('courses', c, 'course.json'));
      delete d.lessonNames; delete d.lessonObjectives;
      (d.levels || []).forEach(l => { if (l && typeof l === 'object') delete l.lessons; });
      return c + ':' + sha(stable(d));
    });
    const h = sha(parts.join('\n')); graphMemo.set(k, h); return h;
  };
  const dataRefs = (...files) => {
    const set = new Set();
    for (const f of files) for (const m of txt(f).matchAll(/content\/data\/[A-Za-z0-9_./-]+/g)) set.add(m[0]);
    return [...set].sort().map(p => p + ' ' + fh(path.join(appDir, p)));
  };
  const courseCommon = (c) => [
    'curriculum ' + fh(C('curriculum.json')), 'warmup ' + fh(C('warmup.json')), 'graph ' + graph(c), 'course ' + fh(C('courses', c, 'course.json')),
    'dir ' + names(C('courses', c)).join(','), 'perf ' + mperf(c),
  ];
  const globalCommon = () => ['curriculum ' + fh(C('curriculum.json')), 'warmup ' + fh(C('warmup.json')), 'graph ' + graph(null)];
  const fin = (parts) => sha(parts.join('\n--\n'));

  /* an exam's draw entries resolved to files by the rule in js/engine/mock.js (matchFile): the name, a "*", or a prefix before a dash */
  const drawFiles = (doc) => {
    const out = new Set(), froms = [];
    (function scan(v) { if (Array.isArray(v)) v.forEach(scan); else if (v && typeof v === 'object') { if (typeof v.from === 'string' && /^(bank|drills)\//.test(v.from)) froms.push(v.from); Object.values(v).forEach(scan); } })(doc);
    for (const from of froms) {
      const [kind, name] = from.split('/'), dir = kind === 'bank' ? C('bank') : C('drills');
      for (const f of names(dir).filter(f => f.endsWith('.json') && f !== 'index.json')) {
        const id = f.slice(0, -5);
        if (name === '*' || id === name || id.startsWith(name + '-')) out.add(path.join(dir, f));
      }
    }
    return [...out].sort();
  };

  const kinds = {
    lesson: (id) => {
      const [c, l] = id.split('/'), f = C('courses', c, l + '.json'), k = `${c}/${l}`;
      return fin(['lesson', ...courseCommon(c), 'file ' + fh(f), ...dataRefs(f), mslice([['lessonMinutes', k], ['sessions', k], ['samples', `courses/${c}/${l}.json`], ['files', `courses/${c}/${l}.json`], ['fluency', `${c}/fluency-${l}`]])]);
    },
    set: (id) => {
      const [c, s] = id.split('/'), f = C('courses', c, s + '.json');
      return fin(['set', ...courseCommon(c), 'file ' + fh(f), ...dataRefs(f), mslice([['setMinutes', id], ['samples', `courses/${c}/${s}.json`], ['files', `courses/${c}/${s}.json`]])]);
    },
    problems: (id) => {
      if (id.startsWith('fixture/')) return kinds._fixture('problems', id);
      const [c, s] = id.split('/'), f = C('courses', c, s + '.json');
      return fin(['problems', ...courseCommon(c), 'file ' + fh(f), ...dataRefs(f), mslice([['problems', id], ['files', `courses/${c}/${s}.json`]])]);
    },
    fluency: (id) => {
      if (id.startsWith('fixture/')) return kinds._fixture('fluency', id);
      const [c, s] = id.split('/'), f = C('courses', c, s + '.json'), d = parse(f) || {}, lf = d.lesson ? C('courses', c, d.lesson + '.json') : null;
      return fin(['fluency', ...courseCommon(c), 'file ' + fh(f), 'lesson ' + (lf ? fh(lf) : '-'), mslice([['fluency', id], ['files', `courses/${c}/${s}.json`], ['lessonMinutes', d.lesson ? `${c}/${d.lesson}` : '']])]);
    },
    /* a fixture (tools/fixtures/<kind>/<file>.json) is registered through the test hook against the course and lesson it names */
    _fixture: (kind, id) => {
      const f = path.join(appDir, 'tools', 'fixtures', kind, id.slice(8) + '.json'), d = parse(f) || {}, c = d.course || '', lf = c && d.lesson ? C('courses', c, d.lesson + '.json') : null;
      return fin(['fixture-' + kind, ...(c ? courseCommon(c) : globalCommon()), 'file ' + fh(f), 'lesson ' + (lf ? fh(lf) : '-')]);
    },
    exam: (id) => {
      const f = C('exams', id + '.json'), d = parse(f) || {}, drawn = drawFiles(d), drills = drawn.some(p => p.includes(path.sep + 'drills' + path.sep));
      return fin(['exam', ...globalCommon(), 'file ' + fh(f), 'drawn ' + filesHash(drawn), ...dataRefs(f, ...drawn), 'drills-index ' + (drills ? fh(C('drills', 'index.json')) : '-'),
        mslice([['examMinutes', id], ['selfExams', id], ['samples', `exams/${id}.json`], ['files', `exams/${id}.json`]])]);
    },
    /* a bank file is dealt through the whole deck, so the names of the other bank files count, not their contents */
    bank: (id) => {
      const f = C('bank', id + '.json');
      return fin(['bank', ...globalCommon(), 'file ' + fh(f), ...dataRefs(f), 'bank-files ' + names(C('bank')).join(','), mslice([['samples', `bank/${id}.json`], ['files', `bank/${id}.json`]])]);
    },
    drill: (id) => {
      const f = C('drills', id + '.json'), idx = (parse(C('drills', 'index.json')) || []).find(r => (r.id || r) === id);
      return fin(['drill', ...globalCommon(), 'file ' + fh(f), ...dataRefs(f), 'row ' + stable(idx || null), mslice([['drills', id], ['samples', `drills/${id}.json`]])]);
    },
    'drill-planted': (id) => kinds.drill(id),
    session: (id) => {
      const f = C('drills', 'sessions', id + '.json'), d = parse(f) || {}, ds = (d.drills || []).map(x => C('drills', (x.id || x) + '.json'));
      return fin(['session', ...globalCommon(), 'file ' + fh(f), 'drills ' + filesHash(ds), ...dataRefs(f, ...ds), 'index ' + fh(C('drills', 'index.json'))]);
    },
    /* The route checks read the courses, curriculum, prep, readiness, capstones, the exams, banks, drills, reviews and lessons: the set cannot be bounded
       (gating, cumulative review, provenance, samples), so they fall back to every file under content/ (the manifest as a normalised copy) plus the fixtures. */
    routes: () => fin(['routes', 'content ' + filesHash(walk(C()).filter(p => rel(p) !== 'content/manifest.json')), 'manifest ' + manifestNormal(), 'fixtures ' + filesHash(walk(path.join(appDir, 'tools', 'fixtures')))]),
  };

  /* app/js/**, app/css/**, app/index.html, app/vendor/**, playthrough.mjs and this file, plus the pinned CDN strings found in them */
  let eng = null;
  const engine = () => {
    if (eng) return eng;
    const files = [...walk(path.join(appDir, 'js')), ...walk(path.join(appDir, 'css')), path.join(appDir, 'index.html'), ...walk(path.join(appDir, 'vendor'))];
    const cdn = new Set();
    for (const p of files) if (/\.(js|mjs|html|css)$/.test(p)) { let t = ''; try { t = fs.readFileSync(p, 'utf8'); } catch { /* skip */ } for (const m of t.matchAll(/(?:\/npm\/((?:@[\w.-]+\/)?[\w.-]+@\d[\w.-]*)|\/(pyodide\/v\d[\d.]*))/g)) cdn.add(m[1] || m[2]); }
    eng = sha(['js/css/index/vendor ' + filesHash(files), 'playthrough ' + sha(fs.readFileSync(selfFile)), 'green-cache ' + sha(fs.readFileSync(SELF)), 'cdn ' + [...cdn].sort().join(',')].join('\n'));
    return eng;
  };
  /* itemHash(kind, id): the engine hash plus what the kind's page reads */
  const itemHash = (kind, id) => { const f = kinds[kind]; if (!f) throw new Error('green-cache: no hash for kind ' + kind); return sha(engine() + '\n' + f(id)); };
  return { itemHash, engine };
};
