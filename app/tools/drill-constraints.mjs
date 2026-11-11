/* Machine-readable drill constraints (ENGINE-BACKLOG 866, docs/AUTHORING.md section 5).
   A drill's `constraints` array holds strings (markdown, shown on the page, as ever) and may also hold objects that
   state the inputs in a form the validator can test. Shared by tools/validate.mjs and tools/test-drill-constraints.mjs.

   Object shape: { "arg": <parameter name or zero-based position>, "type": "int" | "float" | "number" | "str" | "bool" | "list" | "dict",
                   "len": [lo, hi], "range": [lo, hi], "of": <type string or a nested constraint object>,
                   "sorted": true | "asc" | "desc", "distinct": true, "nonEmpty": true, "pattern": "<regex>" }
   `len` bounds a list, string or dict; `range` bounds a number (null for an open end); `of` describes each element of a list
   (a nested object may carry its own `type`, `len`, `range`, `of`); `pattern` is a regular expression a whole string matches.

   Calls are read as Python literals (numbers, strings, True, False, None, lists, tuples, dicts, sets, a leading minus,
   keyword arguments). A call with anything else in it (`[0] * 200000`, `list(range(9))`) cannot be checked and is skipped. */

class PyFloat { constructor(v) { this.v = v; } }
class PyDict { constructor(entries) { this.entries = entries; } }   // [[key, value], ...]
class PyTuple { constructor(items) { this.items = items; } }

/* ---------- a small Python-literal reader ---------- */
const TOKEN = /\s*(?:(\d[\d_]*\.?[\d_]*(?:[eE][+-]?\d+)?|\.\d[\d_]*(?:[eE][+-]?\d+)?)|('(?:[^'\\\n]|\\.)*'|"(?:[^"\\\n]|\\.)*")|([A-Za-z_][\w.]*)|(.))/y;
const lex = (src) => {
  const out = []; TOKEN.lastIndex = 0;
  for (;;) {
    if (TOKEN.lastIndex >= src.length || /^\s*$/.test(src.slice(TOKEN.lastIndex))) break;
    const m = TOKEN.exec(src); if (!m) return null;
    if (m[1] !== undefined) out.push({ k: 'num', v: m[1] });
    else if (m[2] !== undefined) out.push({ k: 'str', v: m[2] });
    else if (m[3] !== undefined) out.push({ k: 'id', v: m[3] });
    else out.push({ k: 'p', v: m[4] });
  }
  return out;
};
const unq = (s) => s.slice(1, -1).replace(/\\(.)/g, (_, c) => ({ n: '\n', t: '\t' }[c] || c));

/* returns { fn, args: [{ name?, value }] } or null when the text is not one call with literal arguments */
export const parseCall = (src) => {
  const t = lex(String(src)); if (!t || !t.length) return null;
  let i = 0;
  const peek = () => t[i], eat = (v) => { if (t[i] && t[i].k === 'p' && t[i].v === v) { i++; return true; } return false; };
  const fail = () => { throw new Error('x'); };
  const value = () => {
    const x = t[i]; if (!x) fail();
    if (x.k === 'p' && (x.v === '-' || x.v === '+')) { i++; const v = value(); if (typeof v === 'number') return x.v === '-' ? -v : v; if (v instanceof PyFloat) return new PyFloat(x.v === '-' ? -v.v : v.v); fail(); }
    if (x.k === 'num') { i++; const s = x.v.replace(/_/g, ''); return /[.eE]/.test(s) ? new PyFloat(parseFloat(s)) : parseInt(s, 10); }
    if (x.k === 'str') { i++; let s = unq(x.v); while (t[i] && t[i].k === 'str') s += unq(t[i++].v); return s; }
    if (x.k === 'id') { i++; if (x.v === 'True') return true; if (x.v === 'False') return false; if (x.v === 'None') return null; fail(); }
    if (x.k === 'p' && x.v === '[') { i++; const a = seq(']'); return a; }
    if (x.k === 'p' && x.v === '(') { i++; const a = seq(')'); return new PyTuple(a); }
    if (x.k === 'p' && x.v === '{') {
      i++; const e = [], items = [];
      if (eat('}')) return new PyDict([]);
      let dict = null;
      for (;;) {
        const a = value();
        if (eat(':')) { if (dict === false) fail(); dict = true; e.push([a, value()]); } else { if (dict === true) fail(); dict = false; items.push(a); }
        if (eat(',')) { if (eat('}')) break; continue; }
        if (!eat('}')) fail(); break;
      }
      return dict ? new PyDict(e) : items;
    }
    return fail();
  };
  const seq = (close) => { const a = []; if (eat(close)) return a; for (;;) { a.push(value()); if (eat(',')) { if (eat(close)) return a; continue; } if (!eat(close)) fail(); return a; } };
  try {
    const f = t[i++]; if (!f || f.k !== 'id' || !eat('(')) return null;
    const args = [];
    if (!eat(')')) {
      for (;;) {
        if (t[i] && t[i].k === 'id' && t[i + 1] && t[i + 1].k === 'p' && t[i + 1].v === '=') { const name = t[i].v; i += 2; args.push({ name, value: value() }); }
        else args.push({ value: value() });
        if (eat(',')) { if (eat(')')) break; continue; }
        if (!eat(')')) fail(); break;
      }
    }
    if (i !== t.length) return null;
    return { fn: f.v, args };
  } catch (e) { return null; }
};

/* the parameter names of the first (or named) `def` in a Python starter, in order */
export const paramNames = (starter, fn) => {
  const re = fn ? new RegExp(`^def\\s+${fn}\\s*\\(([^)]*)\\)`, 'm') : /^def\s+[A-Za-z_]\w*\s*\(([^)]*)\)/m;
  const m = String(starter || '').match(re); if (!m) return [];
  return m[1].split(',').map(s => s.trim().replace(/^\*+/, '').split(/[:=]/)[0].trim()).filter(Boolean);
};

/* ---------- the constraint objects ---------- */
const TYPES = ['int', 'float', 'number', 'str', 'bool', 'list', 'dict'];
const KEYS = ['arg', 'type', 'len', 'range', 'of', 'sorted', 'distinct', 'nonEmpty', 'pattern', 'note'];
export const isConstraint = (c) => c && typeof c === 'object' && !Array.isArray(c);

/* a message for each way a constraint object is itself malformed; [] when sound */
export const constraintShape = (c, nested = false) => {
  const m = [];
  if (!isConstraint(c)) return ['a constraint is an object, or text for the learner'];
  if (!nested && !(typeof c.arg === 'string' && c.arg || Number.isInteger(c.arg) && c.arg >= 0)) m.push('"arg" is the parameter name or its zero-based position');
  if (nested && c.arg !== undefined) m.push('a nested "of" object has no "arg"');
  Object.keys(c).forEach(k => { if (!KEYS.includes(k)) m.push(`unknown key "${k}" (keys: ${KEYS.join(', ')})`); });
  if (c.type !== undefined && !TYPES.includes(c.type)) m.push(`"type" is one of ${TYPES.join(', ')}`);
  ['len', 'range'].forEach(k => {
    if (c[k] === undefined) return;
    const a = c[k];
    if (!Array.isArray(a) || a.length !== 2 || a.some(x => x !== null && typeof x !== 'number')) m.push(`"${k}" is [lo, hi] with numbers (null for no limit)`);
    else if (a[0] !== null && a[1] !== null && a[0] > a[1]) m.push(`"${k}" has lo above hi`);
  });
  if (c.of !== undefined) {
    if (typeof c.of === 'string') { if (!TYPES.includes(c.of)) m.push(`"of" is a type (${TYPES.join(', ')}) or an object`); }
    else constraintShape(c.of, true).forEach(x => m.push(`of: ${x}`));
    if (c.type !== undefined && c.type !== 'list') m.push('"of" belongs to type "list"');
  }
  if (c.sorted !== undefined && ![true, 'asc', 'desc'].includes(c.sorted)) m.push('"sorted" is true, "asc" or "desc"');
  ['distinct', 'nonEmpty'].forEach(k => { if (c[k] !== undefined && typeof c[k] !== 'boolean') m.push(`"${k}" is true or false`); });
  if (c.pattern !== undefined) { try { new RegExp(c.pattern); } catch (e) { m.push('"pattern" is not a valid regular expression'); } }
  return m;
};

const plainOf = (v) => (v instanceof PyFloat ? v.v : v instanceof PyTuple ? v.items : v);
const keyOf = (v) => JSON.stringify(plainOf(v) instanceof Array ? plainOf(v).map(keyOf) : plainOf(v));
const isNum = (v) => (typeof v === 'number' || v instanceof PyFloat);
const kindOf = (v) => (typeof v === 'boolean' ? 'bool' : typeof v === 'number' ? 'int' : v instanceof PyFloat ? 'float' : typeof v === 'string' ? 'str' : v === null ? 'None' : Array.isArray(v) || v instanceof PyTuple ? 'list' : v instanceof PyDict ? 'dict' : 'value');
const lenOf = (v) => (typeof v === 'string' ? v.length : Array.isArray(v) ? v.length : v instanceof PyTuple ? v.items.length : v instanceof PyDict ? v.entries.length : null);
const shown = (v) => { const s = JSON.stringify(plainOf(v) instanceof Array ? plainOf(v).map(plainOf) : plainOf(v)); return s && s.length > 60 ? s.slice(0, 57) + '...' : String(s); };

/* what is wrong with one value against one constraint; [] when it satisfies it. `where` names the place for the message */
export const violations = (c, v, where = 'value') => {
  const m = [], kind = kindOf(v);
  if (c.type) {
    const ok = c.type === 'int' ? kind === 'int' : c.type === 'float' || c.type === 'number' ? kind === 'int' || kind === 'float' : c.type === kind;
    if (!ok) { m.push(`${where} is ${kind === 'None' ? 'None' : 'a ' + kind}, not ${c.type === 'int' ? 'an int' : 'a ' + c.type}`); return m; }
  }
  if (c.range && isNum(v)) { const x = plainOf(v), [lo, hi] = c.range; if ((lo !== null && x < lo) || (hi !== null && x > hi)) m.push(`${where} is ${x}, outside the range [${lo === null ? '' : lo}, ${hi === null ? '' : hi}]`); }
  const len = lenOf(v);
  if (len !== null) {
    if (c.len) { const [lo, hi] = c.len; if ((lo !== null && len < lo) || (hi !== null && len > hi)) m.push(`${where} has length ${len}, outside [${lo === null ? '' : lo}, ${hi === null ? '' : hi}]`); }
    if (c.nonEmpty && len === 0) m.push(`${where} is empty`);
  }
  if (typeof v === 'string' && c.pattern && !new RegExp(`^(?:${c.pattern})$`).test(v)) m.push(`${where} ${JSON.stringify(v.length > 30 ? v.slice(0, 27) + '...' : v)} does not match the pattern ${c.pattern}`);
  if (kind === 'list') {
    const items = plainOf(v);
    if (c.sorted) {
      const desc = c.sorted === 'desc';
      for (let i = 1; i < items.length; i++) {
        const a = plainOf(items[i - 1]), b = plainOf(items[i]);
        if (typeof a !== typeof b || (a !== b && (desc ? a < b : a > b))) { m.push(`${where} is not sorted ${desc ? 'descending' : 'ascending'} (at position ${i})`); break; }
      }
    }
    if (c.distinct) { const seen = new Set(); for (const x of items) { const k = keyOf(x); if (seen.has(k)) { m.push(`${where} repeats ${shown(x)}`); break; } seen.add(k); } }
    if (c.of !== undefined || c.range) {
      const sub = c.of === undefined ? { range: c.range } : typeof c.of === 'string' ? { type: c.of, range: c.range } : c.of;   // a list's own range bounds its elements
      for (let i = 0; i < items.length && m.length < 3; i++) { const r = violations(sub, items[i], `${where}[${i}]`); if (r.length) { m.push(...r); break; } }
    }
  }
  return m;
};

/* every violation in one test: `call` is a Python call string, or `args` a JSON array (C++); `names` the parameter names */
export const checkTest = (constraints, test, names = []) => {
  const objs = (constraints || []).filter(isConstraint);
  if (!objs.length) return { checked: false, messages: [] };
  let args;
  if (Array.isArray(test.args)) args = test.args.map((a) => ({ value: jsonValue(a) }));
  else { const p = parseCall(test.call); if (!p) return { checked: false, messages: [] }; args = p.args; }
  const messages = []; let checked = false;
  objs.forEach(c => {
    let idx = typeof c.arg === 'number' ? c.arg : args.findIndex(a => a.name === c.arg);
    if (idx < 0 && typeof c.arg === 'string') { const pi = names.indexOf(c.arg); idx = pi >= 0 && !args.some(a => a.name) ? pi : -1; }
    if (idx < 0 || idx >= args.length) return;
    checked = true;
    violations(c, args[idx].value, `argument ${JSON.stringify(c.arg)}`).forEach(x => messages.push(x));
  });
  return { checked, messages };
};

/* a JSON value as the checker's value model (a number with a fraction or exponent is a float) */
const jsonValue = (a) => (typeof a === 'number' ? (Number.isInteger(a) ? a : new PyFloat(a)) : Array.isArray(a) ? a.map(jsonValue) : a && typeof a === 'object' ? new PyDict(Object.entries(a).map(([k, v]) => [k, jsonValue(v)])) : a);

/* Problems to report for a drill file: [{ where, msg }] for the validator (errors), plus whether it states any machine constraint */
export const drillConstraintReport = (d) => {
  const errors = [];
  const list = Array.isArray(d.constraints) ? d.constraints : [];
  const objs = list.map((c, i) => [c, i]).filter(([c]) => isConstraint(c));
  objs.forEach(([c, i]) => constraintShape(c).forEach(msg => errors.push({ where: `constraints[${i}]`, msg })));
  if (errors.length || !objs.length) return { errors, has: objs.length > 0, tested: 0, skipped: 0 };
  const names = d.language === 'cpp' ? [] : paramNames(d.starter, d.fn);
  objs.forEach(([c, i]) => { if (typeof c.arg === 'string' && d.language !== 'cpp' && names.length && !names.includes(c.arg)) errors.push({ where: `constraints[${i}].arg`, msg: `"${c.arg}" is not a parameter of the starter's function (${names.join(', ')})` }); });
  let tested = 0, skipped = 0;
  [['examples', d.examples], ['tests', d.tests]].forEach(([group, arr]) => (Array.isArray(arr) ? arr : []).forEach((t, j) => {
    if (!t || typeof t !== 'object') return;
    const r = checkTest(list, t, names);
    if (r.checked) tested++; else skipped++;
    r.messages.forEach(msg => errors.push({ where: `${group}[${j}]`, msg: `${msg}: the test breaks the drill's stated constraints (fix the test, or widen "constraints")` }));
  }));
  return { errors, has: true, tested, skipped };
};
