/* Performance-task rules (ENGINE-BACKLOG 529, PLAN 2c item 5, docs/AUTHORING.md section 5). Pure functions, no file reads, so the validator,
   perf-pending.mjs and test-validate-perf.mjs all apply one rule. */

export const KINDS = ['code', 'derivation', 'aloud', 'data'];
const BASE_VERBS = ['write', 'derive', 'prove', 'build', 'code', 'implement', 'design'];
const SOFT_VERBS = ['explain', 'defend', 'justify'];
/* the interview courses (DECISIONS "Performance tasks"): the soft verbs count there whatever the stage */
export const INTERVIEW_COURSES = new Set(['recruiting', 'brainteasers', 'puzzles', 'mm-games', 'mental-pressure', 'game-theory', 'coding-int', 'research-int', 'systems', 'ito', 'measure-prob', 'pdes']);
const STAGE0_KEPT = new Set(['first-python', 'terminal']);

const first = (o) => (String(o || '').trim().toLowerCase().match(/^[a-z]+/) || [''])[0];

/* Does a level match the verb rule? objectives: every objective string of the level's written lesson files. Returns the matching verb or null. */
export const matchVerb = (cid, stage, objectives) => {
  if (Number(stage) === 0 && !STAGE0_KEPT.has(cid)) return null;
  const soft = Number(stage) >= 2 || INTERVIEW_COURSES.has(cid);
  const verbs = soft ? BASE_VERBS.concat(SOFT_VERBS) : BASE_VERBS;
  for (const o of objectives || []) { const v = first(o); if (verbs.includes(v)) return v; }
  return null;
};

const isObj = (x) => x && typeof x === 'object' && !Array.isArray(x);
const isLong = (it) => it.kind === 'longform' || (isObj(it.widget) && it.widget.kind === 'longform');
const longSpec = (it) => (it.kind === 'longform' ? it : it.widget);
const present = (x) => typeof x === 'string' && x.trim() !== '';

/* The shape of one performance item. Returns messages (strings); [] when well formed. `how` is the grading the engine will record. */
export const checkTask = (it) => {
  const out = [];
  if (!isObj(it)) return ['item must be an object'];
  const k = it.performance;
  if (!KINDS.includes(k)) return [`performance must be one of ${KINDS.join(', ')} (found ${JSON.stringify(k)})`];
  if (it.parts !== undefined) out.push('a performance item has no parts: it is one task from a blank start');
  if (it.hints) out.push('a performance item has no hints');
  const kind = isObj(it.widget) ? it.widget.kind : it.kind;
  if (k === 'code') {
    const w = it.widget;
    if (!isObj(w) || w.kind !== 'code') { out.push('code: the item needs a code widget'); return out; }
    const tests = Array.isArray(w.tests) ? w.tests.length : 0, ex = Array.isArray(w.examples) ? w.examples.length : 0;
    if (tests < 3) out.push('code: at least 3 hidden tests');
    else if (tests <= ex) out.push(`code: more tests than examples (${tests} tests, ${ex} examples), so some tests are unseen`);
    if (!present(w.starter)) out.push('code: a starter (a stub that fails the tests) is required');
    if (!present(w.solution)) out.push('code: a model solution is required');
  } else if (k === 'derivation' || k === 'aloud') {
    if (!isLong(it)) { out.push(`${k}: a longform item (kind longform, or a longform widget)`); return out; }
    const s = longSpec(it);
    ['starter', 'steps', 'order', 'derive', 'scaffold'].forEach(f => { if (s[f] !== undefined || it[f] !== undefined) out.push(`${k}: no "${f}" (the box starts empty, nothing to reorder or fill in)`); });
    if (!present(s.model)) out.push(`${k}: a model answer (shown only after the learner marks) is required`);
    if (!Array.isArray(s.rubric) || s.rubric.length < 3) out.push(`${k}: a rubric of at least 3 criteria`);
    if (k === 'aloud') {
      if (!Number.isInteger(s.seconds) || s.seconds < 15 || s.seconds > 1800) out.push('aloud: seconds is a whole number from 15 to 1800 (the time to speak)');
      if (!Array.isArray(s.followUps) || s.followUps.length < 1 || s.followUps.length > 5 || !s.followUps.every(present)) out.push('aloud: followUps is 1 to 5 non-empty strings the interviewer asks next');
    } else {
      if (s.seconds !== undefined) out.push('derivation: seconds is for an aloud task');
      if (s.followUps !== undefined) out.push('derivation: followUps is for an aloud task');
    }
  } else if (k === 'data') {
    if (kind !== 'numeric' && kind !== 'longform') { out.push('data: a numeric or a longform item'); return out; }
    const s = isObj(it.widget) ? it.widget : it;
    if (!isObj(s.data) || !Object.keys(s.data).length) out.push('data: name the data file(s) in data: { "name.csv": "content/data/..." }');
    if (kind === 'longform') {
      if (!present(s.model)) out.push('data: a model answer is required');
      if (!Array.isArray(s.rubric) || s.rubric.length < 3) out.push('data: a rubric of at least 3 criteria');
    }
  }
  return out;
};

/* auto or self, for the manifest and the locked card */
export const howOf = (it) => {
  const k = it.performance;
  if (k === 'code') return 'auto';
  if (k === 'data') return (isObj(it.widget) ? it.widget.kind : it.kind) === 'numeric' ? 'auto' : 'self';
  return 'self';
};

/* One level. matched: the verb or null; tasks: the performance items found in the level's review and homework; pending: the level is on perf-pending.json.
   Returns { errors: [], warnings: [], pendingNoTask: bool } */
export const checkLevel = ({ key, matched, tasks, pending }) => {
  const errors = [], warnings = [];
  if (tasks.length > 1) errors.push(`${key}: ${tasks.length} performance tasks (${tasks.map(t => t.id).join(', ')}); at most one per level`);
  let pendingNoTask = false;
  if (!tasks.length && matched) {
    if (pending) pendingNoTask = true;
    else errors.push(`${key}: an objective starts with "${matched}", so the level needs a performance task (docs/AUTHORING.md section 5); add one item with "performance" to its homework or review`);
  }
  if (tasks.length && pending) warnings.push(`${key}: has a performance task, remove from perf-pending`);
  return { errors, warnings, pendingNoTask };
};
