/* interleave (item 471, E13): two or three threads as lanes of numbered steps over shared variables. The learner taps a
   lane to run its next step, so every interleaving can be walked by hand: a lane whose next step is a lock another lane
   holds is blocked, a wait sleeps until a later notify, and a schedule in which no lane can step ends "deadlock" (or
   "asleep forever" when the only lanes left are asleep). The same rules, run over every legal schedule (a memoised
   walk over states, cached per spec), give values.outcomes: each reachable final with its schedule count.
   Contract: docs/AUTHORING.md section 4; details in canvas/README-B.md. HTML inside the canvas wrapper, like the table.
   The first half of this file is the engine (no DOM); tools/validate.mjs loads it with require() for its spec rules, the
   schedule check and the enumeration limit. The second half is the canvas. */
(function () {
  'use strict';

  /* ======================================================================================================
     Engine
     ====================================================================================================== */
  const isObj = (v) => v !== null && typeof v === 'object' && !Array.isArray(v);
  const OPS = ['load', 'add', 'store', 'set', 'fetch-add', 'lock', 'unlock', 'wait', 'notify'];
  const NOTATIONS = ['words', 'assign'];
  const ENDINGS = ['complete', 'deadlock', 'asleep'];
  /* names a shared variable may not take: they are keys of the canvas's values() for derive */
  const RESERVED = ['outcomes', 'outcomeList', 'schedules', 'complete', 'deadlock', 'asleep', 'ending', 'outcome', 'done', 'steps', 'remaining', 'order', 'reached', 'reachedList', 'regs'];
  const LIMITS = { lanes: 3, stepsPerLane: 8, steps: 24, states: 200000 };
  const IDENT = /^[A-Za-z][A-Za-z0-9]*$/;
  const NAME = /^[A-Za-z_][A-Za-z0-9_]*$/;

  /* ---------- A tiny expression language: numbers, names, + - * / %, comparisons, && || !, min max abs ---------- */
  const FN = { min: Math.min, max: Math.max, abs: Math.abs };
  const exprCache = new Map();
  const parseExpr = (src) => {
    src = String(src);
    if (exprCache.has(src)) return exprCache.get(src);
    const toks = [], re = /\s*(?:(\d+(?:\.\d+)?)|([A-Za-z_][A-Za-z0-9_]*)|(<=|>=|==|!=|&&|\|\||[-+*/%<>!(),]))/y;
    let i = 0;
    while (i < src.length) {
      re.lastIndex = i; const m = re.exec(src);
      if (!m) { if (/^\s*$/.test(src.slice(i))) break; throw new Error('cannot read "' + src.slice(i).trim() + '" in "' + src + '"'); }
      i = re.lastIndex; toks.push(m[1] !== undefined ? { n: +m[1] } : m[2] !== undefined ? { id: m[2] } : { op: m[3] });
    }
    let p = 0; const names = new Set();
    const eat = (o) => { const t = toks[p]; if (t && t.op === o) { p++; return true; } return false; };
    let or;
    const primary = () => {
      const t = toks[p++]; if (!t) throw new Error('unfinished expression "' + src + '"');
      if (t.n !== undefined) return () => t.n;
      if (t.id !== undefined) {
        if (eat('(')) {
          const args = []; if (!eat(')')) { do args.push(or()); while (eat(',')); if (!eat(')')) throw new Error('missing ) in "' + src + '"'); }
          const fn = FN[t.id]; if (!fn) throw new Error('unknown function ' + t.id + ' in "' + src + '"');
          return (L) => fn(...args.map((a) => a(L)));
        }
        if (t.id === 'true') return () => 1; if (t.id === 'false') return () => 0;
        names.add(t.id); return (L) => L(t.id);
      }
      if (t.op === '(') { const e = or(); if (!eat(')')) throw new Error('missing ) in "' + src + '"'); return e; }
      throw new Error('unexpected "' + t.op + '" in "' + src + '"');
    };
    const unary = () => { if (eat('-')) { const u = unary(); return (L) => -u(L); } if (eat('!')) { const u = unary(); return (L) => (u(L) ? 0 : 1); } return primary(); };
    const bin = (next, ops) => () => {
      let l = next();
      for (;;) { const t = toks[p]; if (!t || !t.op || !ops[t.op]) return l; p++; const f = ops[t.op], a = l, b = next(); l = (L) => f(a(L), b(L)); }
    };
    const mul = bin(unary, { '*': (a, b) => a * b, '/': (a, b) => (b ? a / b : 0), '%': (a, b) => (b ? a % b : 0) });
    const add = bin(mul, { '+': (a, b) => a + b, '-': (a, b) => a - b });
    const rel = bin(add, { '<': (a, b) => +(a < b), '<=': (a, b) => +(a <= b), '>': (a, b) => +(a > b), '>=': (a, b) => +(a >= b) });
    const eq = bin(rel, { '==': (a, b) => +(a === b), '!=': (a, b) => +(a !== b) });
    const and = bin(eq, { '&&': (a, b) => +(!!a && !!b) });
    or = bin(and, { '||': (a, b) => +(!!a || !!b) });
    const f = or();
    if (p < toks.length) throw new Error('unexpected "' + (toks[p].op || toks[p].id || toks[p].n) + '" in "' + src + '"');
    const out = { f, names: [...names] };
    exprCache.set(src, out); return out;
  };
  const ev = (e, look) => (typeof e === 'number' ? e : typeof e === 'boolean' ? +e : parseExpr(e).f(look));
  const fmt = (v) => (typeof v === 'number' ? (Number.isInteger(v) ? String(v) : String(+v.toFixed(6))) : String(v));

  /* ---------- Spec ---------- */
  const microOf = (s) => {
    if (!isObj(s)) return null;
    const { text, id, ...rest } = s; // eslint-disable-line no-unused-vars
    return rest;
  };
  const normalise = (params) => {
    const P = isObj(params) ? params : {};
    const vars = {};
    Object.entries(isObj(P.vars) ? P.vars : isObj(P.shared) ? P.shared : {}).forEach(([k, v]) => { vars[k] = Number.isFinite(+v) ? +v : 0; });
    const lanes = (Array.isArray(P.lanes) ? P.lanes : []).map((l, li) => {
      l = isObj(l) ? l : {};
      const id = String(l.id ?? 'abcdefgh'[li] ?? 'l' + li);
      const steps = (Array.isArray(l.steps) ? l.steps : []).map((s, k) => {
        s = isObj(s) ? s : {};
        const ops = (Array.isArray(s.ops) ? s.ops : [microOf(s)]).filter(isObj);
        return { id: String(s.id ?? (/\d$/.test(id) ? id + '-' + (k + 1) : id + (k + 1))), text: s.text != null ? String(s.text) : null, ops, n: k + 1 };
      });
      return { id, name: String(l.label ?? l.name ?? 'Thread ' + id.toUpperCase()), short: String(l.short ?? id.toUpperCase()), steps, regs: isObj(l.regs) ? { ...l.regs } : {} };
    });
    const locks = new Set(Array.isArray(P.locks) ? P.locks.map(String) : []);
    lanes.forEach((l) => l.steps.forEach((s) => s.ops.forEach((m) => { if (m.lock != null) locks.add(String(m.lock)); })));
    return { vars, lanes, locks: [...locks], notation: NOTATIONS.includes(P.notation) ? P.notation : 'words', outcome: Array.isArray(P.outcome) ? P.outcome : null, endings: isObj(P.endings) ? P.endings : {} };
  };
  const laneIndex = (spec, ref) => (typeof ref === 'number' && Number.isInteger(ref) ? (ref >= 0 && ref < spec.lanes.length ? ref : -1) : spec.lanes.findIndex((l) => l.id === String(ref)));

  /* ---------- Text of a step ---------- */
  const microText = (m, notation) => {
    const as = notation === 'assign', by = m.by == null ? 1 : m.by;
    const pre = m.if != null ? 'if ' + m.if + ': ' : '';
    let t;
    switch (m.op) {
      case 'load': t = as ? `${m.reg} = ${m.var}` : `load ${m.reg} from ${m.var}`; break;
      case 'add': t = as ? (typeof by === 'number' && by < 0 ? `${m.reg} -= ${-by}` : `${m.reg} += ${by}`) : `add ${m.reg} ${by}`; break;
      case 'store': t = m.reg != null ? (as ? `${m.var} = ${m.reg}` : `store ${m.var} from ${m.reg}`) : (as ? `${m.var} = ${m.value}` : `store ${m.var} = ${m.value}`); break;
      case 'set': t = `${m.reg} = ${m.value}`; break;
      case 'fetch-add': t = as ? `${m.var} += ${by} (atomic)` : `fetch-add ${m.var} ${by}`; break;
      case 'lock': t = `lock ${m.lock}`; break;
      case 'unlock': t = `unlock ${m.lock}`; break;
      case 'wait': t = m.lock != null ? `wait (frees ${m.lock})` : 'wait'; break;
      case 'notify': t = 'notify'; break;
      default: t = String(m.op);
    }
    return pre + t;
  };
  const stepText = (step, notation) => (step.text != null ? step.text : step.ops.map((m) => microText(m, notation)).join('; '));

  /* ---------- Running ---------- */
  const init = (spec) => ({ pcs: spec.lanes.map(() => 0), vars: { ...spec.vars }, regs: spec.lanes.map((l) => ({ ...l.regs })), locks: {}, asleep: spec.lanes.map(() => false) });
  const clone = (S) => ({ pcs: S.pcs.slice(), vars: { ...S.vars }, regs: S.regs.map((r) => ({ ...r })), locks: { ...S.locks }, asleep: S.asleep.slice() });
  const lookOf = (S, li) => (n) => (n in S.regs[li] ? S.regs[li][n] : n in S.vars ? S.vars[n] : 0);
  const holds = (m, look) => m.if == null || !!ev(m.if, look);
  const blockedOn = (spec, S, li) => {
    const step = spec.lanes[li].steps[S.pcs[li]]; if (!step) return null;
    const look = lookOf(S, li);
    for (const m of step.ops) if (m.op === 'lock' && holds(m, look) && S.locks[m.lock] !== undefined) return String(m.lock);
    return null;
  };
  const enabled = (spec, S, li) => S.pcs[li] < spec.lanes[li].steps.length && !S.asleep[li] && blockedOn(spec, S, li) === null;
  const enabledLanes = (spec, S) => spec.lanes.map((_, li) => li).filter((li) => enabled(spec, S, li));
  /* how a finished run ended: every lane ran out ("complete"), a lane waits on a held lock ("deadlock"), or only sleepers remain ("asleep") */
  const endingOf = (spec, S) => {
    if (enabledLanes(spec, S).length) return 'running';
    if (spec.lanes.every((l, li) => S.pcs[li] >= l.steps.length) && !S.asleep.some(Boolean)) return 'complete';
    return spec.lanes.some((l, li) => S.pcs[li] < l.steps.length && !S.asleep[li]) ? 'deadlock' : 'asleep';
  };
  /* one micro-op; returns a short note of what it did, for the result line under the step */
  const exec = (spec, S, li, m) => {
    const look = lookOf(S, li), R = S.regs[li];
    if (!holds(m, look)) return 'skipped';
    const by = () => (m.by == null ? 1 : ev(m.by, look));
    switch (m.op) {
      case 'load': R[m.reg] = S.vars[m.var] ?? 0; return `${m.reg} = ${fmt(R[m.reg])}`;
      case 'add': R[m.reg] = (R[m.reg] ?? 0) + by(); return `${m.reg} = ${fmt(R[m.reg])}`;
      case 'store': S.vars[m.var] = m.reg != null ? look(m.reg) : ev(m.value, look); return `${m.var} = ${fmt(S.vars[m.var])}`;
      case 'set': { const v = ev(m.value, look); R[m.reg] = v; return `${m.reg} = ${/[<>=!&|]/.test(String(m.value)) ? (v ? 'true' : 'false') : fmt(v)}`; }
      case 'fetch-add': { const old = S.vars[m.var] ?? 0; S.vars[m.var] = old + by(); if (m.reg != null) R[m.reg] = old; return `${m.var} = ${fmt(S.vars[m.var])}`; }
      case 'lock': S.locks[m.lock] = li; return `holds ${m.lock}`;
      case 'unlock': if (S.locks[m.lock] === li) delete S.locks[m.lock]; return `frees ${m.lock}`;
      case 'wait': S.asleep[li] = true; if (m.lock != null && S.locks[m.lock] === li) delete S.locks[m.lock]; return 'asleep';
      case 'notify': { const w = []; S.asleep.forEach((a, k) => { if (a) { S.asleep[k] = false; w.push(spec.lanes[k].short); } }); return w.length ? 'wakes ' + w.join(', ') : 'nobody asleep'; }
      default: return '';
    }
  };
  const runStep = (spec, S, li) => {
    const step = spec.lanes[li].steps[S.pcs[li]];
    const notes = step.ops.map((m) => exec(spec, S, li, m)).filter(Boolean);
    S.pcs[li]++;
    return notes;
  };
  /* Replay a schedule (lane ids) from the start. Stops at the first entry that cannot run (bad: its index). */
  const replay = (spec, schedule) => {
    const S = init(spec), hist = []; let bad = null;
    (Array.isArray(schedule) ? schedule : []).some((ref, idx) => {
      const li = laneIndex(spec, ref);
      if (li < 0 || !enabled(spec, S, li)) { bad = idx; return true; }
      const step = spec.lanes[li].steps[S.pcs[li]], notes = runStep(spec, S, li);
      hist.push({ lane: li, step: step.id, note: notes.join(', ') });
      return false;
    });
    return { S, hist, bad, ending: endingOf(spec, S) };
  };

  /* ---------- Outcomes ---------- */
  const outcomeItems = (spec) => (spec.outcome || Object.keys(spec.vars)).map((o) => (isObj(o) ? { label: String(o.label ?? o.of), of: String(o.of) } : { label: String(o), of: String(o) }));
  const readOf = (spec, S, of) => {
    const m = of.match(/^([A-Za-z][A-Za-z0-9]*)\.([A-Za-z_][A-Za-z0-9_]*)$/);
    if (m) { const li = spec.lanes.findIndex((l) => l.id === m[1]); return li >= 0 ? S.regs[li][m[2]] ?? 0 : 0; }
    return S.vars[of] ?? 0;
  };
  const endLabel = (spec, e) => (spec.endings[e] != null ? String(spec.endings[e]) : e === 'asleep' ? 'asleep' : e);
  const outcomeOf = (spec, S, ending) => {
    if (ending !== 'complete') return { key: endLabel(spec, ending), ending, values: {} };
    const items = outcomeItems(spec), values = {};
    items.forEach((it) => { values[it.label] = readOf(spec, S, it.of); });
    return { key: items.length ? items.map((it) => `${it.label}=${fmt(values[it.label])}`).join(', ') : endLabel(spec, 'complete'), ending, values };
  };
  const ser = (o) => Object.keys(o).sort().map((k) => k + ':' + o[k]).join(',');
  const cache = new Map();
  /* Every legal schedule, counted by what it ends in. Null when the state space is over LIMITS.states. */
  const enumerate = (spec) => {
    const ck = JSON.stringify([spec.vars, spec.lanes.map((l) => [l.id, l.regs, l.steps.map((s) => s.ops)]), spec.outcome, spec.endings]);
    if (cache.has(ck)) return cache.get(ck);
    const memo = new Map(), meta = new Map(); let n = 0, over = false;
    const go = (S) => {
      const k = S.pcs.join(',') + '|' + ser(S.vars) + '|' + S.regs.map(ser).join(';') + '|' + ser(S.locks) + '|' + S.asleep.map(Number).join('');
      const hit = memo.get(k); if (hit) return hit;
      if (++n > LIMITS.states) { over = true; return {}; }
      const ls = enabledLanes(spec, S), out = {};
      if (!ls.length) { const o = outcomeOf(spec, S, endingOf(spec, S)); meta.set(o.key, o); out[o.key] = 1; }
      else for (const li of ls) { const S2 = clone(S); runStep(spec, S2, li); const sub = go(S2); for (const key in sub) out[key] = (out[key] || 0) + sub[key]; if (over) return out; }
      memo.set(k, out); return out;
    };
    let res = null;
    try {
      const counts = go(init(spec));
      if (!over) {
        const order = { complete: 0, deadlock: 1, asleep: 2 };
        const list = Object.keys(counts).map((key) => ({ key, count: counts[key], ending: meta.get(key).ending, values: meta.get(key).values }))
          .sort((a, b) => order[a.ending] - order[b.ending] || a.key.localeCompare(b.key, undefined, { numeric: true }));
        const outcomes = {}; list.forEach((o) => { outcomes[o.key] = o.count; });
        const by = (e) => list.filter((o) => o.ending === e).reduce((t, o) => t + o.count, 0);
        res = { outcomes, list, schedules: list.reduce((t, o) => t + o.count, 0), complete: by('complete'), deadlock: by('deadlock'), asleep: by('asleep') };
      }
    } catch (e) { res = null; }
    cache.set(ck, res); return res;
  };

  /* ---------- Ids and spec check (the validator) ---------- */
  const idsOf = (params) => {
    const spec = normalise(params), ids = new Set();
    spec.lanes.forEach((l) => { ids.add('lane-' + l.id); l.steps.forEach((s) => ids.add(s.id)); });
    Object.keys(spec.vars).forEach((v) => ids.add('var-' + v));
    spec.locks.forEach((m) => ids.add('lock-' + m));
    return ids;
  };
  /* Problems with params (and an optional state), as { at, msg } lists: errors and warnings */
  const check = (params, state) => {
    const errors = [], warnings = [], E = (at, msg) => errors.push({ at, msg }), W = (at, msg) => warnings.push({ at, msg });
    const P = params;
    if (!isObj(P)) { E('', 'params is an object with lanes (and vars, locks, outcome)'); return { errors, warnings }; }
    if (!Array.isArray(P.lanes) || !P.lanes.length) { E('params.lanes', 'lanes is a list of 1 to ' + LIMITS.lanes + ' lanes: { id, label, steps: [...] }'); return { errors, warnings }; }
    if (P.lanes.length > LIMITS.lanes) E('params.lanes', `at most ${LIMITS.lanes} lanes`);
    if (P.vars != null && !isObj(P.vars)) E('params.vars', 'vars is { name: starting number }');
    Object.entries(isObj(P.vars) ? P.vars : {}).forEach(([k, v]) => {
      if (!NAME.test(k)) E(`params.vars.${k}`, 'a variable name is letters, digits and _');
      if (RESERVED.includes(k)) E(`params.vars.${k}`, `"${k}" is a name interleave's values() uses; rename the variable`);
      if (!Number.isFinite(v)) E(`params.vars.${k}`, 'a starting value is a number');
    });
    if (P.locks != null && !(Array.isArray(P.locks) && P.locks.every((m) => typeof m === 'string' && NAME.test(m)))) E('params.locks', 'locks is a list of lock names');
    if (P.notation != null && !NOTATIONS.includes(P.notation)) E('params.notation', 'notation is "words" or "assign"');
    if (P.endings != null && !(isObj(P.endings) && Object.keys(P.endings).every((k) => ENDINGS.includes(k)))) E('params.endings', 'endings maps complete, deadlock or asleep to the text shown in values.outcomes');
    const spec = normalise(P), seen = new Map();
    const claim = (id, at) => { if (seen.has(id)) E(at, `id "${id}" is already used at ${seen.get(id)}`); else seen.set(id, at); };
    let total = 0;
    spec.lanes.forEach((l, li) => {
      const at = `params.lanes[${li}]`;
      if (!IDENT.test(l.id)) E(`${at}.id`, 'a lane id is letters and digits starting with a letter ("a", "t1")');
      claim('lane-' + l.id, `${at}.id`);
      if (!l.steps.length) E(`${at}.steps`, 'a lane needs a list of steps');
      if (l.steps.length > LIMITS.stepsPerLane) E(`${at}.steps`, `at most ${LIMITS.stepsPerLane} steps in a lane`);
      total += l.steps.length;
      const known = new Set([...Object.keys(spec.vars), ...Object.keys(l.regs)]);
      l.steps.forEach((s) => s.ops.forEach((m) => { ['reg'].forEach((f) => { if (typeof m[f] === 'string' && ['load', 'add', 'set', 'fetch-add'].includes(m.op)) known.add(m[f]); }); }));
      const held = new Set();
      l.steps.forEach((s, k) => {
        const sat = `${at}.steps[${k}]`;
        claim(s.id, `${sat}.id`);
        if (!NAME.test(s.id.replace(/-/g, '_'))) E(`${sat}.id`, 'a step id is letters, digits and - (it is what tap-regions and highlight use)');
        if (!s.ops.length) { E(sat, 'a step is { op, ... } or { ops: [{ op, ... }], text }'); return; }
        s.ops.forEach((m, j) => {
          const mat = s.ops.length > 1 || (Array.isArray((P.lanes[li].steps[k] || {}).ops)) ? `${sat}.ops[${j}]` : sat;
          if (!OPS.includes(m.op)) { E(`${mat}.op`, `op is one of ${OPS.join(', ')}`); return; }
          const needStr = (f) => { if (typeof m[f] !== 'string' || !NAME.test(m[f])) E(`${mat}.${f}`, `${m.op} needs ${f}, a name`); };
          const exprOk = (f, v) => {
            if (typeof v === 'number') return;
            if (typeof v !== 'string') { E(`${mat}.${f}`, `${f} is a number or an expression such as "r - 80"`); return; }
            try { parseExpr(v).names.forEach((nm) => { if (!known.has(nm)) E(`${mat}.${f}`, `"${nm}" is neither a shared variable nor a register this lane sets (load, add, set or fetch-add with reg)`); }); } catch (e) { E(`${mat}.${f}`, e.message); }
          };
          if (m.if != null) exprOk('if', m.if);
          if (m.op === 'load') { needStr('reg'); needStr('var'); if (typeof m.var === 'string' && !(m.var in spec.vars)) E(`${mat}.var`, `"${m.var}" is not in params.vars`); }
          if (m.op === 'add') { needStr('reg'); if (m.by != null) exprOk('by', m.by); else E(`${mat}.by`, 'add needs by, a number'); }
          if (m.op === 'store') {
            needStr('var'); if (typeof m.var === 'string' && !(m.var in spec.vars)) E(`${mat}.var`, `"${m.var}" is not in params.vars`);
            if ((m.reg == null) === (m.value == null)) E(mat, 'store needs reg (the register to store) or value (a number or expression), not both');
            else if (m.reg != null) { needStr('reg'); if (typeof m.reg === 'string' && !known.has(m.reg)) E(`${mat}.reg`, `"${m.reg}" is not a register this lane sets`); } else exprOk('value', m.value);
          }
          if (m.op === 'set') { needStr('reg'); if (m.value == null) E(`${mat}.value`, 'set needs value, an expression such as "r >= 80"'); else exprOk('value', m.value); }
          if (m.op === 'fetch-add') { needStr('var'); if (typeof m.var === 'string' && !(m.var in spec.vars)) E(`${mat}.var`, `"${m.var}" is not in params.vars`); if (m.by != null) exprOk('by', m.by); if (m.reg != null) needStr('reg'); }
          if (m.op === 'lock' || m.op === 'unlock') {
            needStr('lock');
            if (Array.isArray(P.locks) && typeof m.lock === 'string' && !P.locks.includes(m.lock)) E(`${mat}.lock`, `lock "${m.lock}" is not in params.locks`);
            if (m.op === 'lock') held.add(m.lock); else if (!held.has(m.lock)) W(`${mat}.lock`, `unlock ${m.lock} with no earlier lock ${m.lock} in this lane`);
          }
          if (m.op === 'wait' && m.lock != null) needStr('lock');
        });
      });
    });
    if (total > LIMITS.steps) E('params.lanes', `at most ${LIMITS.steps} steps in all`);
    if (spec.outcome != null) {
      if (!Array.isArray(P.outcome)) E('params.outcome', 'outcome is a list of shared variable names, "lane.reg" names or { label, of }');
      else P.outcome.forEach((o, i) => {
        const of = isObj(o) ? o.of : o;
        if (typeof of !== 'string') { E(`params.outcome[${i}]`, 'an outcome entry is a name or { label, of }'); return; }
        const m = of.match(/^([A-Za-z][A-Za-z0-9]*)\.([A-Za-z_][A-Za-z0-9_]*)$/);
        if (m ? !spec.lanes.some((l) => l.id === m[1]) : !(of in spec.vars)) E(`params.outcome[${i}]`, `"${of}" is not a shared variable or a lane.register (${spec.lanes.map((l) => l.id + '.reg').join(', ')})`);
      });
    }
    if (errors.length) return { errors, warnings };
    if (state && Array.isArray(state.schedule)) {
      const r = replay(spec, state.schedule);
      if (r.bad != null) { const ref = state.schedule[r.bad]; E(`state.schedule[${r.bad}]`, laneIndex(spec, ref) < 0 ? `"${ref}" is not a lane id (${spec.lanes.map((l) => l.id).join(', ')})` : `lane "${ref}" cannot step there (it is blocked, asleep or finished)`); }
    } else if (state && state.schedule != null) E('state.schedule', 'schedule is a list of lane ids, one per step taken');
    if (state && state.outcomes != null && !(typeof state.outcomes === 'boolean' || state.outcomes === 'found')) E('state.outcomes', 'outcomes is true (every outcome with its count), "found" (the ones the learner has reached) or false');
    if (enumerate(spec) === null) E('params', `the lanes have more than ${LIMITS.states} states to enumerate; shorten them or drop registers`);
    return { errors, warnings };
  };

  const engine = { normalise, replay, enumerate, check, idsOf, stepText, LIMITS, RESERVED };
  if (typeof window === 'undefined' || !window.ZQ || !window.ZQ.canvas) { if (typeof module === 'object' && module.exports) module.exports = engine; return; }

  /* ======================================================================================================
     Canvas
     ====================================================================================================== */
  const Z = window.ZQ, C = Z.canvas;

  function interleave(host, params, ctx = {}) {
    const spec = normalise(params), P = isObj(params) ? params : {};
    const h = (tag, cls, text) => { const n = document.createElement(tag); if (cls) n.className = cls; if (text != null) n.textContent = text; return n; };
    const wrap = h('div', 'cv');
    const lanesEl = h('div', 'il-lanes'); lanesEl.style.setProperty('--il-n', String(Math.max(1, spec.lanes.length)));
    const shared = h('div', 'il-shared'); shared.setAttribute('aria-label', 'Shared state');
    const orderEl = h('div', 'il-order t-caption');
    const endEl = h('div', 'il-end'); endEl.setAttribute('role', 'status'); endEl.hidden = true;
    const bar = h('div', 'il-bar');
    const outsEl = h('div', 'il-outs'); outsEl.hidden = true;
    const cap = h('div', 't-caption cv-caption'); cap.hidden = true;
    wrap.append(lanesEl, shared, orderEl, endEl, bar, outsEl, cap); host.append(wrap);
    const inl = (t) => (Z.grade && Z.grade.inline ? Z.grade.inline(String(t)) : Z.md ? Z.md(String(t)) : Z.esc(String(t)));
    const fr = { wrap, caption: (t) => { cap.hidden = !t; cap.innerHTML = t ? inl(t) : ''; } };
    if (P.label) lanesEl.setAttribute('aria-label', String(P.label));

    /* Static structure: lanes with their steps and a Step button; the shared chips; Undo and Reset */
    const laneEls = spec.lanes.map((lane) => {
      const sec = h('section', 'il-lane cv-obj'); sec.dataset.id = 'lane-' + lane.id; sec.setAttribute('aria-label', lane.name);
      const head = h('header', 'il-lane-h'), name = h('span', 'il-lane-name', lane.name), st = h('span', 'il-lane-st t-caption');
      head.append(name, st);
      const ol = h('ol', 'il-steps');
      const rows = lane.steps.map((s) => {
        const li = h('li', 'il-step cv-obj'); li.dataset.id = s.id; li.dataset.tap = ''; li.dataset.label = `Step ${s.id}: ${stepText(s, spec.notation)}`;
        const id = h('span', 'il-id', s.id), tx = h('span', 'il-tx', stepText(s, spec.notation)), res = h('span', 'il-res'), seq = h('span', 'il-seq');
        seq.setAttribute('aria-hidden', 'true');
        li.append(id, tx, res, seq); ol.append(li);
        return { li, res, seq };
      });
      const go = h('button', 'btn secondary il-go'); go.type = 'button'; go.dataset.lane = lane.id; go.textContent = 'Step ' + lane.short;
      sec.append(head, ol, go); lanesEl.append(sec);
      return { sec, st, rows, go };
    });
    const undoB = h('button', 'link-btn il-undo', 'Undo'), resetB = h('button', 'link-btn il-reset', 'Reset');
    undoB.type = 'button'; resetB.type = 'button'; bar.append(undoB, resetB);
    const chips = { vars: {}, locks: {} };
    Object.keys(spec.vars).forEach((v) => {
      const c = h('span', 'il-chip cv-obj'); c.dataset.id = 'var-' + v; const k = h('span', 'il-chip-k', v), val = h('span', 'il-chip-v');
      c.append(k, val); shared.append(c); chips.vars[v] = val;
    });
    spec.locks.forEach((m) => {
      const c = h('span', 'il-chip il-lock cv-obj'); c.dataset.id = 'lock-' + m; const k = h('span', 'il-chip-k', m), val = h('span', 'il-chip-v');
      c.append(k, val); shared.append(c); chips.locks[m] = val;
    });
    shared.hidden = !shared.children.length;

    const reached = new Set(); // outcome keys the learner has finished at (kept across Reset, lost on Start over)
    let fresh = null;
    const sched = () => (Array.isArray(I.state().schedule) ? I.state().schedule : []);

    const outcomesTable = (st, E, R) => {
      const mode = st.outcomes;
      outsEl.hidden = !mode || !E;
      if (!mode || !E) return;
      outsEl.replaceChildren();
      const rows = mode === 'found' ? E.list.filter((o) => reached.has(o.key)) : E.list;
      const n = (v) => v.toLocaleString('en-GB');
      const head = h('p', 't-caption il-outs-h', mode === 'found' ? `Outcomes found: ${rows.length} of ${E.list.length}` : `${n(E.schedules)} schedules, ${E.list.length} outcome${E.list.length === 1 ? '' : 's'}`);
      outsEl.append(head);
      if (!rows.length) return;
      const tbl = h('table', 'il-outs-t'), tb = h('tbody');
      rows.forEach((o) => {
        const tr = h('tr', 'il-out' + (R.ending !== 'running' && outcomeOf(spec, R.S, R.ending).key === o.key ? ' is-now' : '') + (o.ending !== 'complete' ? ' is-stuck' : ''));
        tr.append(h('th', null, o.key));
        if (mode !== 'found') tr.append(h('td', null, n(o.count)));
        if (mode === 'found' || reached.has(o.key)) tr.append(h('td', 'il-found', reached.has(o.key) ? 'found' : ''));
        tb.append(tr);
      });
      tbl.append(tb); outsEl.append(tbl);
    };

    const draw = (st) => {
      const R = replay(spec, st.schedule);
      if (R.bad != null && !draw.warned) { draw.warned = true; console.warn('interleave: schedule entry ' + R.bad + ' cannot run; the rest is ignored'); }
      const S = R.S, off = I.isStatic || I.locked(), end = R.ending !== 'running';
      const doneAt = new Map(); R.hist.forEach((x, i) => doneAt.set(x.step, { i, note: x.note }));
      spec.lanes.forEach((lane, li) => {
        const L = laneEls[li], blocked = blockedOn(spec, S, li), fin = S.pcs[li] >= lane.steps.length, ok = enabled(spec, S, li);
        L.sec.classList.toggle('is-blocked', !!blocked && !fin && !S.asleep[li]);
        L.sec.classList.toggle('is-asleep', S.asleep[li]);
        L.sec.classList.toggle('is-done', fin && !S.asleep[li]);
        L.st.textContent = S.asleep[li] ? 'Asleep, waits for a notify' : fin ? 'Finished' : blocked ? `Blocked: ${blocked} is held by ${spec.lanes[S.locks[blocked]].short}` : 'Ready';
        lane.steps.forEach((s, k) => {
          const row = L.rows[k], d = doneAt.get(s.id), next = k === S.pcs[li] && !fin;
          row.li.classList.toggle('is-done', !!d);
          row.li.classList.toggle('is-next', next && ok);
          row.li.classList.toggle('is-stuck', next && !ok && !S.asleep[li]);
          row.res.textContent = d ? d.note : ''; row.res.hidden = !d || !d.note;
          row.seq.textContent = d ? String(d.i + 1) : '';
          row.li.classList.toggle('is-new', !!d && fresh === s.id);
        });
        L.go.disabled = off || !ok;
        L.go.setAttribute('aria-label', ok ? `Step ${lane.name}: ${stepText(lane.steps[S.pcs[li]], spec.notation)}` : `${lane.name} cannot step: ${L.st.textContent.toLowerCase()}`);
      });
      Object.keys(chips.vars).forEach((v) => { chips.vars[v].textContent = fmt(S.vars[v]); });
      Object.keys(chips.locks).forEach((m) => { const own = S.locks[m]; chips.locks[m].textContent = own === undefined ? 'free' : 'held by ' + spec.lanes[own].short; chips.locks[m].parentElement.classList.toggle('is-held', own !== undefined); });
      orderEl.textContent = R.hist.length ? 'Order: ' + R.hist.map((x) => x.step).join(', ') : 'Order: no step taken yet';
      undoB.disabled = off || !R.hist.length; resetB.disabled = off || !R.hist.length;
      bar.hidden = I.isStatic;
      /* the ending */
      endEl.hidden = !end;
      endEl.className = 'il-end' + (end ? ' is-' + R.ending : '');
      if (end) {
        const o = outcomeOf(spec, S, R.ending);
        if (R.ending === 'complete') endEl.textContent = 'Finished' + (outcomeItems(spec).length ? ': ' + o.key : '. Every lane ran to the end.');
        else if (R.ending === 'deadlock') {
          const w = spec.lanes.map((l, li) => ({ li, m: S.pcs[li] < l.steps.length && !S.asleep[li] ? blockedOn(spec, S, li) : null })).filter((x) => x.m)
            .map((x) => `${spec.lanes[x.li].short} waits for ${x.m} (held by ${spec.lanes[S.locks[x.m]].short})`);
          endEl.textContent = 'Deadlock: no lane can step. ' + w.join('; ') + '.';
        } else endEl.textContent = 'Asleep forever: ' + spec.lanes.filter((l, li) => S.asleep[li]).map((l) => l.short).join(', ') + ' waits for a notify that never comes.';
      }
      if (st.outcomes) outcomesTable(st, enumerate(spec), R); else outsEl.hidden = true;
    };

    const I = C.instance({ kind: 'interleave', factory: interleave, params, ctx, fr, draw, defaults: { schedule: [] } });
    const api = I.api;
    const outcomeNow = () => { const R = replay(spec, sched()); return R.ending === 'running' ? null : outcomeOf(spec, R.S, R.ending); };
    const commit = (schedule, lane) => {
      api.set({ schedule }, { instant: true });
      const o = outcomeNow(); if (o) { reached.add(o.key); if (I.state().outcomes === 'found') api.set({}, { instant: true }); }
      I.emit('change', { type: 'step', lane, schedule: schedule.slice(), ending: o ? o.ending : 'running', outcome: o ? o.key : null });
    };
    const stepLane = (ref) => {
      if (I.isStatic || I.locked()) return false;
      const R = replay(spec, sched()), li = laneIndex(spec, ref);
      if (li < 0 || R.bad != null || !enabled(spec, R.S, li)) return false;
      fresh = spec.lanes[li].steps[R.S.pcs[li]].id; I.later(() => { fresh = null; }, 900);
      if (Z.sound) Z.sound('tap');
      commit([...sched(), spec.lanes[li].id], spec.lanes[li].id);
      return true;
    };
    wrap.addEventListener('click', (e) => {
      const b = e.target.closest('button'); if (!b || !wrap.contains(b) || b.disabled) return;
      if (b.classList.contains('il-go')) stepLane(b.dataset.lane);
      else if (b.classList.contains('il-undo') && !I.isStatic && !I.locked() && sched().length) commit(sched().slice(0, -1), null);
      else if (b.classList.contains('il-reset') && !I.isStatic && !I.locked() && sched().length) commit([], null);
    });
    const baseLock = api.lock;
    api.lock = (on = true) => { baseLock(on); draw(I.state()); return api; };

    /* methods for the test hook, authors' scripts and screenshots */
    api.step = (ref) => stepLane(ref);
    api.enabled = () => { const R = replay(spec, sched()); return enabledLanes(spec, R.S).map((li) => spec.lanes[li].id); };
    api.ending = () => replay(spec, sched()).ending;
    api.reset = () => { if (sched().length) commit([], null); return api; };
    api.undo = () => { if (sched().length) commit(sched().slice(0, -1), null); return api; };
    /* play a list of lane ids from the start (replacing the schedule), stopping at one that cannot run; returns the ending */
    api.play = (list) => { const R = replay(spec, list), ok = (Array.isArray(list) ? list : []).slice(0, R.bad == null ? undefined : R.bad); commit(ok, null); return replay(spec, ok).ending; };
    /* finish the current schedule: always the first lane that can step (or `pick(enabledIds)` chooses) */
    api.finish = (pick) => { for (let g = 0; g < 200; g++) { const en = api.enabled(); if (!en.length) break; stepLane(typeof pick === 'function' ? pick(en) : en[0]); } return api.ending(); };
    api.outcomes = () => enumerate(spec);
    api.values = () => {
      const R = replay(spec, sched()), S = R.S, E = enumerate(spec), o = {};
      Object.keys(spec.vars).forEach((v) => { o[v] = S.vars[v]; });
      o.ending = R.ending; o.done = +(R.ending !== 'running'); o.steps = R.hist.length;
      o.remaining = spec.lanes.reduce((t, l, li) => t + l.steps.length - S.pcs[li], 0);
      o.order = R.hist.map((x) => x.step).join(' ');
      o.outcome = R.ending === 'running' ? '' : outcomeOf(spec, S, R.ending).key;
      o.regs = Object.fromEntries(spec.lanes.map((l, li) => [l.id, { ...S.regs[li] }]));
      o.reached = reached.size; o.reachedList = [...reached];
      if (E) { o.outcomes = E.outcomes; o.outcomeList = E.list.map((x) => ({ key: x.key, count: x.count, ending: x.ending })); o.schedules = E.schedules; o.complete = E.complete; o.deadlock = E.deadlock; o.asleep = E.asleep; }
      return o;
    };
    api.set({}, { instant: true });
    return api;
  }

  C.register('interleave', interleave);
  C.interleaveEngine = engine;
})();
