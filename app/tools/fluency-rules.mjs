/* Rules and helpers for generated fluency sets (ENGINE-BACKLOG 812 to 816; author side docs/AUTHORING.md section 16).
   Shared by tools/validate.mjs (checkSet), tools/fluency-sample.mjs and tools/test-fluency.mjs. Node, no dependencies.
     checkSet(doc, ctx)        the problems of one set: schema, and every family sampled at 200 seeds
     loadSet(ref)              "<course>/<set id>" from content/courses, "fixture/<id>" from tools/fixtures/fluency, or a file path
     numericGrade(widget, t)   the numeric widget's grade() on typed text t, with the real ZQ.grade helpers (no DOM)
     typedAnswer(item)         what a learner types for the key of a numeric item
   The expression widget needs the Compute Engine to grade, so the validator checks an expression family by text (the answer
   and every wrong are filled, non-empty and different) and tools/test-fluency.mjs grades them in the real browser. */
import fs from 'node:fs';
import path from 'node:path';
import vm from 'node:vm';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
export const APP = path.resolve(HERE, '..');
export const gen = createRequire(import.meta.url)('../js/engine/gen.js');
export const SEEDS = 200;

const sandbox = () => {
  const g = { console, setTimeout, clearTimeout, document: { addEventListener() {}, querySelector() { return null; } }, navigator: {} };
  g.window = g; g.globalThis = g; vm.createContext(g); g.ZQ = {};
  vm.runInContext(fs.readFileSync(path.join(APP, 'js/engine/grade.js'), 'utf8'), g, { filename: 'grade.js' });
  return g.ZQ.grade;
};
let G = null;
export const grade = () => G || (G = sandbox());

/* the numeric widget's grade(), line for line (js/engine/widgets/numeric.js), on the typed text */
export const numericGrade = (w, text) => {
  const pct = w.unit === '%', t = String(text).trim();
  const v0 = grade().parseNum(t), v = pct && !t.includes('%') ? v0 / 100 : v0;
  if (!Number.isFinite(v)) return { ok: false, key: null };
  const ok = grade().within(v, +w.answer, w.tol);
  const hit = ok ? null : grade().matchWrong(v, w.wrong, { abs: 1e-9 });
  return { ok, key: hit ? hit.id : null };
};
export const typedAnswer = (item) => {
  const w = item.widget;
  return grade().fmtNum(w.unit === '%' ? +(w.answer * 100).toPrecision(12) : w.answer);
};
export const typedValue = (w, value) => grade().fmtNum(w.unit === '%' ? +(value * 100).toPrecision(12) : value);
export const norm = (s) => grade().normExpr(s);

export const loadSet = (ref) => {
  const abs = path.isAbsolute(ref) && fs.existsSync(ref) ? ref : null;
  if (abs) return { file: abs, doc: JSON.parse(fs.readFileSync(abs, 'utf8')), course: JSON.parse(fs.readFileSync(abs, 'utf8')).course || null };
  const [c, id] = String(ref).split('/');
  if (!c || !id) throw new Error(`"${ref}" is not <course>/<set id> (or fixture/<id>)`);
  const file = c === 'fixture' ? path.join(APP, 'tools/fixtures/fluency', `${id}.json`) : path.join(APP, 'content/courses', c, `${id}.json`);
  if (!fs.existsSync(file)) throw new Error(`no fluency set at ${path.relative(APP, file)}`);
  const doc = JSON.parse(fs.readFileSync(file, 'utf8'));
  return { file, doc, course: c === 'fixture' ? doc.course : c };
};
export const fixtureFiles = () => {
  const dir = path.join(APP, 'tools/fixtures/fluency');
  return fs.existsSync(dir) ? fs.readdirSync(dir).filter((f) => f.endsWith('.json')).sort().map((f) => path.join(dir, f)) : [];
};

const KEBAB = /^[a-z0-9]+(-[a-z0-9]+)*$/;
const TOP = ['id', 'lesson', 'title', 'n', 'pass', 'minutes', 'families', 'sample', 'course'];
const plural = (n, a, b) => `${n} ${n === 1 ? a : b}`;

/* ctx: { fileId, lessonIds: Set (the course map), written: Set, voice(where, text) -> [{level, where, msg}], seeds, course } */
export const checkSet = (doc, ctx = {}) => {
  const out = [], seen = new Set();
  const add = (level, where, msg) => { const k = `${level}|${where}|${msg}`; if (!seen.has(k)) { seen.add(k); out.push({ level, where, msg }); } };
  const E = (w, m) => add('error', w, m), W = (w, m) => add('warning', w, m);
  const seeds = ctx.seeds || SEEDS, stats = [];
  if (!doc || typeof doc !== 'object' || Array.isArray(doc)) { E('', 'a fluency set is a JSON object'); return { problems: out, stats }; }
  Object.keys(doc).forEach((k) => { if (!TOP.includes(k)) W(k, `unknown field "${k}" in a fluency set`); });
  ['id', 'lesson', 'title', 'families'].forEach((k) => { if (doc[k] === undefined || doc[k] === '') E(k, 'required field missing'); });
  if (typeof doc.id === 'string') {
    if (!KEBAB.test(doc.id)) E('id', 'id is kebab-case');
    if (typeof doc.lesson === 'string' && doc.id !== `fluency-${doc.lesson}`) E('id', `id must be "fluency-${doc.lesson}" (the lesson id after "fluency-")`);
    if (ctx.fileId && doc.id !== ctx.fileId) E('id', `id "${doc.id}" must match the file name "${ctx.fileId}.json"`);
  }
  if (typeof doc.lesson === 'string' && ctx.lessonIds) {
    if (!ctx.lessonIds.has(doc.lesson)) E('lesson', `lesson "${doc.lesson}" is not on the course map of this course`);
    else if (ctx.written && !ctx.written.has(doc.lesson)) W('lesson', `lesson "${doc.lesson}" is not written yet`);
  }
  if (doc.course !== undefined && ctx.course && doc.course !== ctx.course) E('course', `course "${doc.course}" must be "${ctx.course}"`);
  if (doc.n !== undefined && !(Number.isInteger(doc.n) && doc.n >= 5 && doc.n <= 50)) E('n', 'n is a whole number from 5 to 50 (20 is the default)');
  if (doc.pass !== undefined && !(typeof doc.pass === 'number' && doc.pass >= 0.5 && doc.pass <= 1)) E('pass', 'pass is a share from 0.5 to 1 (0.9 is the default)');
  if (doc.minutes !== undefined && !(Number.isInteger(doc.minutes) && doc.minutes >= 1 && doc.minutes <= 60)) E('minutes', 'minutes is a whole number from 1 to 60');
  if (doc.sample !== undefined && typeof doc.sample !== 'boolean') E('sample', 'sample is true, or the field is left out');
  /* the voice rules as drawn: ctx.voice is the validator's checkText; plus the 35-word gate on a sentence (a formula counts as one word) */
  const voice = (where, text) => {
    if (typeof text !== 'string') return;
    if (ctx.voice) ctx.voice(where, text).forEach((p) => add(p.level, p.where, p.msg));
    text.replace(/\$\$[\s\S]*?\$\$|\$[^$]*\$/g, ' MATH ').split(/(?<=[.?!:;])\s+/).forEach((s) => { const k = s.trim().split(/\s+/).filter(Boolean).length; if (k > 35) add('error', where, `a sentence of ${k} words (the gate is 35): "${s.trim().slice(0, 50)}..."`); });
  };
  voice('title', doc.title);
  if (typeof doc.title === 'string' && doc.title.includes('$')) E('title', 'keep maths out of a set title (it shows as plain text)');
  if (!Array.isArray(doc.families)) { if (doc.families !== undefined) E('families', 'families must be a list'); return { problems: out, stats }; }
  if (!doc.families.length) E('families', 'a set needs at least one family');
  if (doc.families.length > 12) E('families', 'at most 12 families in a set');
  const n = Number.isInteger(doc.n) ? doc.n : 20;
  if (doc.families.length > n) W('families', `${plural(doc.families.length, 'family', 'families')} for ${n} items: some families would never be drawn`);
  const ids = new Set();
  doc.families.forEach((f, i) => {
    const w = `families[${i}]`;
    if (f && typeof f.id === 'string') { if (ids.has(f.id)) E(`${w}.id`, `family id "${f.id}" is used twice`); ids.add(f.id); }
    const msgs = gen.checkFamily(f);
    msgs.forEach((m) => E(w, m));
    if (msgs.length) return;
    const tag = `${w} (${f.id})`;
    const r = gen.sample(f, { seeds, set: doc.id || 'set' });
    const rejectRate = r.attempts ? r.rejected / r.attempts : 0;
    stats.push({ id: f.id, distinct: r.distinct, attempts: r.attempts, rejected: r.rejected, failed: r.failed });
    const reason = r.errors.length ? ` (${r.errors[0][0]})` : '';
    if (r.failed) E(tag, `${r.failed} of ${seeds} draws could not be completed${reason}: loosen where, or widen vars`);
    if (rejectRate > 0.8) E(tag, `where and the evaluator reject ${Math.round(rejectRate * 100)}% of draws (the limit is 80%)${reason}: draw the values so the condition mostly holds`);
    if (!r.failed && rejectRate <= 0.8 && r.errors.length) E(tag, `${r.errors.reduce((a, [, k]) => a + k, 0)} draws raised an error: ${r.errors[0][0]}`);
    if (r.distinct < 25) E(tag, `only ${r.distinct} distinct prompts in ${seeds} draws (at least 25 are required, 60 are expected): widen vars`);
    else if (r.distinct < 60) W(tag, `only ${r.distinct} distinct prompts in ${seeds} draws (60 expected): widen vars`);
    const numeric = f.widget.kind === 'numeric';
    const bad = { answer: 0, empty: 0, stray: 0, wrongSame: new Map(), wrongEmpty: new Map(), wrongBlank: 0 };
    r.items.forEach((it) => {
      const wid = it.widget;
      const text = [it.prompt, ...it.solution, wid.answer, ...[].concat(wid.accept || []).filter((x) => typeof x === 'string')].join(' ');
      if (/NaN|undefined|Infinity|\[object/.test(text)) bad.stray++;
      if (!it.prompt.trim() || it.solution.some((s) => !String(s).trim()) || wid.answer === '' || wid.answer === undefined) bad.empty++;
      if (numeric) {
        if (!numericGrade(wid, typedAnswer(it)).ok) bad.answer++;
        it.wrong.forEach((x) => {
          if (!Number.isFinite(x.value)) { bad.wrongBlank++; return; }
          if (numericGrade({ ...wid, wrong: [] }, typedValue(wid, x.value)).ok) bad.wrongSame.set(x.id, (bad.wrongSame.get(x.id) || 0) + 1);
        });
      } else {
        const keys = [wid.answer, ...[].concat(wid.accept || [])].map(norm);
        it.wrong.forEach((x) => {
          if (!String(x.tex).trim()) bad.wrongEmpty.set(x.id, (bad.wrongEmpty.get(x.id) || 0) + 1);
          else if (keys.includes(norm(x.tex))) bad.wrongSame.set(x.id, (bad.wrongSame.get(x.id) || 0) + 1);
        });
      }
    });
    if (bad.stray) E(tag, `${bad.stray} draws put NaN, undefined or Infinity into the text`);
    if (bad.empty) E(tag, `${bad.empty} draws left the prompt, a solution step or the answer empty`);
    if (bad.answer) E(tag, `the typed answer is not graded correct in ${bad.answer} of ${r.items.length} draws`);
    if (bad.wrongBlank) E(tag, `${bad.wrongBlank} wrong values are not numbers`);
    bad.wrongSame.forEach((k, id) => E(`${tag} wrong "${id}"`, `grades as correct in ${k} of ${r.items.length} draws: add a where that keeps it apart from the answer (or change it)`));
    bad.wrongEmpty.forEach((k, id) => E(`${tag} wrong "${id}"`, `is empty in ${k} of ${r.items.length} draws`));
    /* voice: prompt, wrong lines and solution steps of the first draws, as the learner reads them */
    r.items.slice(0, 40).forEach((it) => {
      voice(`${w}.prompt`, it.prompt);
      it.solution.forEach((s, j) => voice(`${w}.solution[${j}]`, s));
      it.wrong.forEach((x, j) => { if (x.line) voice(`${w}.wrong[${j}].line`, x.line); });
    });
  });
  return { problems: out, stats };
};
