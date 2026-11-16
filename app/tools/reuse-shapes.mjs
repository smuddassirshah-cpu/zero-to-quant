// Reuse shapes (ENGINE-BACKLOG 993, engine pass AE). What tools/same-course-reuse.mjs cannot see from numbers, matrices and sentences: the same mathematics in other clothes.
// shapesOf(strings, node) reads a unit (a lesson screen, a quiz item, a problem set item or one of its parts) and returns keys for four kinds:
//   fn   a function with its interval (`fi`), a polynomial with its factorisation (`fn`, the product of factors is expanded, one variable is renamed to v, so t^2-4t+3 = (t-1)(t-3) = x^2-4x+3),
//        a multivariable polynomial's heavy terms (`terms`, the potential x^3 + xy^2 against x^3 + xy^2 + y)
//   pair two consecutive part keys held in one sentence of another unit (`pkeys` of an item against the `lines` of a source: 0.7 then 0.3 against "r = 1 - 0.7 = 0.3")
//   tr   a polynomial or a denominator shifted and scaled (`dp`: monic, with the x^(d-1) term shifted away, so s(s+1)(s+2) and (s+2)(s+3)(s+4) meet), and a number set under x -> a x + b (`ls`)
//   rg   a region with its integrand: a corner set (`T`, also a plane's intercepts projected on z = 0), a circle with a number the integrand takes (`CI`), end points with a route (`EP`)
// The keys are matched by same-course-reuse.mjs. A hit is an error there (ENGINE-BACKLOG 1059) after the rules R1 to R5 (1053 to 1057) were tightened against review-delta-ae-1; a ruling that stands is waived in tools/same-course-waivers.json.

// ---------- a small polynomial algebra over single letters ----------
const norm = (s) => s.replace(/\\left|\\right/g, '').replace(/\\[,;:! ]|~/g, '').replace(/\\[dt]frac/g, '\\frac').replace(/\\cdot|\\times/g, '*').replace(/\s+/g, '').replace(/\^\{(-?\d+)\}/g, '^$1');
const fmtN = (x) => String(+x.toFixed(6) + 0);

function monoMul(a, b) {
  if (!a) return b; if (!b) return a;
  const m = new Map();
  for (const [, l, e] of a.matchAll(/([a-z])(\d+)/g)) m.set(l, (m.get(l) ?? 0) + Number(e));
  for (const [, l, e] of b.matchAll(/([a-z])(\d+)/g)) m.set(l, (m.get(l) ?? 0) + Number(e));
  return [...m].sort(([p], [q]) => (p < q ? -1 : 1)).map(([l, e]) => `${l}${e}`).join('');
}
const pAdd = (p, q, s = 1) => { const r = new Map(p); for (const [k, c] of q) r.set(k, (r.get(k) ?? 0) + s * c); for (const [k, c] of r) if (Math.abs(c) < 1e-9) r.delete(k); return r; };
const pMul = (p, q) => { const r = new Map(); for (const [a, c] of p) for (const [b, d] of q) { const k = monoMul(a, b); r.set(k, (r.get(k) ?? 0) + c * d); } for (const [k, c] of r) if (Math.abs(c) < 1e-9) r.delete(k); return r; };
const pConst = (p) => (p.size === 0 ? 0 : p.size === 1 && p.has('') ? p.get('') : null);

// Recursive descent: + - * / (by a constant), implicit product, ^ with a whole exponent, \frac{poly}{constant}. Anything else throws.
function parsePoly(src) {
  const s = norm(src);
  if (!s || s.length > 120 || /[_|&%#$]/.test(s) || /ln|pi|sin|cos|tan|exp|log|max|min|sqrt|e\^|[a-z]{3}/.test(s.replace(/\\frac/g, ''))) return null;
  let i = 0;
  const fail = () => { throw new Error('x'); };
  const num = () => { const m = /^\d*\.?\d+/.exec(s.slice(i)); if (!m) fail(); i += m[0].length; return new Map([['', Number(m[0])]]); };
  const group = () => { if (s[i] !== '{') fail(); i++; const v = expr(); if (s[i] !== '}') fail(); i++; return v; };
  const primary = () => {
    const c = s[i];
    if (c === undefined) fail();
    if (/[\d.]/.test(c)) return num();
    if (/[a-z]/i.test(c)) { i++; return new Map([[`${c}1`, 1]]); }
    if (c === '(') { i++; const v = expr(); if (s[i] !== ')') fail(); i++; return v; }
    if (s.startsWith('\\frac', i)) { i += 5; const n = group(), d = group(), k = pConst(d); if (k === null || k === 0) fail(); return new Map([...n].map(([m, v]) => [m, v / k])); }
    return fail();
  };
  const power = () => {
    let b = primary();
    if (s[i] === '^') {
      i++; let e;
      if (s[i] === '(') { i++; const m = /^\d+/.exec(s.slice(i)); if (!m) fail(); i += m[0].length; if (s[i] !== ')') fail(); i++; e = Number(m[0]); }
      else { const m = /^\d+/.exec(s.slice(i)); if (!m) fail(); i += m[0].length; e = Number(m[0]); }
      if (e > 8) fail();
      let r = new Map([['', 1]]); for (let k = 0; k < e; k++) r = pMul(r, b); b = r;
    }
    return b;
  };
  const unary = () => { if (s[i] === '-') { i++; return pMul(new Map([['', -1]]), unary()); } if (s[i] === '+') { i++; return unary(); } return power(); };
  const term = () => {
    let v = unary();
    for (;;) {
      const c = s[i];
      if (c === '*') { i++; v = pMul(v, unary()); }
      else if (c === '/') { i++; const d = unary(), k = pConst(d); if (k === null || k === 0) fail(); v = new Map([...v].map(([m, x]) => [m, x / k])); }
      else if (c !== undefined && (/[a-z\d.(]/i.test(c) || s.startsWith('\\frac', i))) v = pMul(v, power());
      else return v;
    }
  };
  const expr = () => { let v = term(); while (s[i] === '+' || s[i] === '-') { const sg = s[i] === '-' ? -1 : 1; i++; v = pAdd(v, term(), sg); } return v; };
  try { const v = expr(); return i === s.length ? v : null; } catch { return null; }
}
const degOf = (mono) => [...mono.matchAll(/(\d+)/g)].reduce((a, m) => a + Number(m[1]), 0);
const lettersOf = (p) => new Set([...p.keys()].flatMap((m) => [...m.matchAll(/([a-z])\d+/g)].map((x) => x[1])));
// A canonical form: a one-letter polynomial is written in v. Returns { key, deg, nterms, vars, terms }.
function canon(p) {
  const vars = lettersOf(p);
  const ren = vars.size === 1 ? (m) => m.replace(/[a-z]/, 'v') : (m) => m;
  const terms = [...p].map(([m, c]) => ({ m: ren(m), c, d: degOf(m) })).sort((a, b) => b.d - a.d || (a.m < b.m ? -1 : 1));
  return { key: terms.map((t) => `${fmtN(t.c)}${t.m || '1'}`).join(' '), deg: terms.length ? terms[0].d : 0, nterms: terms.length, vars, terms };
}
// monic, depressed: substitute x = y - a/d so the second coefficient goes; two cubics that are shifts and multiples of each other meet here
function depressed(p) {
  const c = canon(p);
  if (c.vars.size !== 1 || c.deg < 3 || c.deg > 8) return null;
  const co = new Array(c.deg + 1).fill(0); for (const t of c.terms) co[t.d] = t.c;
  const lead = co[c.deg], a = co.map((x) => x / lead);
  const sh = -a[c.deg - 1] / c.deg;   // x = y + sh; coefficients of p(y + sh) by repeated synthetic division
  const b = a.slice();
  for (let i = 0; i < c.deg; i++) for (let j = c.deg - 1; j >= i; j--) b[j] += sh * b[j + 1];
  const out = b.map((x) => (Math.abs(x) < 1e-9 ? 0 : x));
  if (out.filter((x, i) => i < c.deg && x !== 0).length < 1) return null;
  const mirror = out.map((x, i) => x * (-1) ** (c.deg - i) + 0);   // x -> -x (and back to monic): the same cubic reflected, whose roots change sign, is the same key (ENGINE-BACKLOG 1059)
  const a1 = out.map(fmtN).join(','), a2 = mirror.map(fmtN).join(',');
  return a1 < a2 ? a1 : a2;
}
const VARS = 'xyztsuvw';
const perfectSquare = (c) => { const co = [0, 0, 0]; for (const t of c.terms) co[t.d] = t.c; return Math.abs(co[1] * co[1] - 4 * co[2] * co[0]) < 1e-9; };
const isStockQuad = (c) => {   // a monic or plain quadratic whose roots are whole numbers of size six or less: the classroom factorising screen
  if (c.vars.size !== 1 || c.deg !== 2) return false;
  const co = [0, 0, 0]; for (const t of c.terms) co[t.d] = t.c;
  const D = co[1] * co[1] - 4 * co[2] * co[0];
  if (D < 0) return false;
  const r = Math.sqrt(D); if (Math.abs(r - Math.round(r)) > 1e-9) return false;
  return [(-co[1] + r) / (2 * co[2]), (-co[1] - r) / (2 * co[2])].every((x) => Math.abs(x - Math.round(x)) < 1e-9 && Math.abs(x) <= 6);
};

// ---------- splitting maths ----------
// Split at the top level (outside (), {}, []) on any of the given separators.
function splitTop(s, seps) {
  const out = []; let d = 0, last = 0;
  for (let i = 0; i < s.length; i++) {
    const c = s[i];
    if ('({['.includes(c)) d++; else if (')}]'.includes(c)) d--;
    else if (d === 0) for (const sep of seps) if (s.startsWith(sep, i) && !(sep.startsWith('\\') && /[a-zA-Z]/.test(s[i + sep.length] ?? ''))) { out.push(s.slice(last, i)); i += sep.length - 1; last = i + 1; break; }
  }
  out.push(s.slice(last)); return out;
}
const RELS = ['=', '\\approx', '\\leq', '\\geq', '\\le', '\\ge', '<', '>', '\\to', '\\Rightarrow'];
const wrapped = (p) => { if (p[0] !== '(' || p[p.length - 1] !== ')') return false; let d = 0; for (let i = 0; i < p.length; i++) { if (p[i] === '(') d++; else if (p[i] === ')') { d--; if (d === 0 && i < p.length - 1) return false; } } return true; };
// expressions of a maths string: each side of a relation, each component of a bracketed tuple, the groups of each \frac
function pieces(m, depth = 0, frac = true) {
  const out = [];
  for (let p of splitTop(m, RELS)) {
    p = p.trim(); if (!p) continue;
    const parts = wrapped(p) ? splitTop(p.slice(1, -1), [',', ';']) : splitTop(p, [',', ';']);
    for (const q of parts) {
      const t = q.trim(); if (!t) continue;
      out.push(t);
      if (frac && depth < 2) for (const g of fracGroups(t)) out.push(...pieces(g, depth + 1));
    }
  }
  return out;
}
function braceAt(s, i) { if (s[i] !== '{') return null; let d = 0; for (let j = i; j < s.length; j++) { if (s[j] === '{') d++; else if (s[j] === '}') { d--; if (d === 0) return j; } } return null; }
function fracGroups(s) {
  const out = []; const t = s.replace(/\\[dt]frac/g, '\\frac');
  for (let i = t.indexOf('\\frac'); i >= 0; i = t.indexOf('\\frac', i + 5)) {
    let j = i + 5; while (t[j] === ' ') j++;
    const e1 = braceAt(t, j); if (e1 === null) continue;
    let k = e1 + 1; while (t[k] === ' ') k++;
    const e2 = braceAt(t, k); if (e2 === null) continue;
    out.push(t.slice(j + 1, e1), t.slice(k + 1, e2));
  }
  return out;
}
// the maths of a string: each $..$ or $$..$$ span; a short string with no $ is an answer written as an expression
function mathOf(str) {
  const out = [];
  if (!str.includes('$')) { if (str.length <= 90 && !/[A-Za-z]{4,}/.test(str.replace(/\\[a-zA-Z]+/g, ''))) out.push(str); return out; }
  for (const m of str.matchAll(/\$\$([\s\S]+?)\$\$|\$([^$]+)\$/g)) out.push(m[1] ?? m[2]);
  return out;
}
const NONPOLY = /\\sqrt|\\ln|\\sin|\\cos|\\tan|\\exp|\\log|e\^|\\arctan|\\frac/;
function nonPolyKey(p) {
  const s = norm(p).replace(/^[a-z]\([a-z]\)/, '');
  if (!NONPOLY.test(s) || s.length > 40 || s.length < 6 || /_/.test(s)) return null;
  const letters = new Set([...s.replace(/\\[a-zA-Z]+/g, '').matchAll(/[a-z]/g)].map((m) => m[0]).filter((c) => c !== 'e'));
  if (letters.size !== 1) return null;
  return s.replace(/\\[a-zA-Z]+|[a-z]/g, (m) => (m.length === 1 && letters.has(m) ? 'v' : m));
}
// ---------- intervals ----------
const endp = (x) => { const t = x.replace(/\s+/g, '').replace(/\\pi/g, 'pi').replace(/^\{|\}$/g, ''); return /^-?(?:\d*\.?\d*)?(?:pi)?$/.test(t) && /\d|pi/.test(t) ? t.replace(/^(-?)pi$/, '$11pi') : null; };
function intervalsIn(text) {   // Map "a:b" -> the interval's variable when it is named (0 <= z <= 2), else null
  const out = new Map();
  for (const m of text.matchAll(/[[(]\s*(-?[\d.]*(?:\\pi)?)\s*,\s*(-?[\d.]*(?:\\pi)?)\s*\]/g)) { const a = endp(m[1]), b = endp(m[2]); if (a && b && a !== b) out.set(`${a}:${b}`, null); }
  for (const m of text.matchAll(/\\int_\{?(-?[\d.]*(?:\\pi)?)\}?\^\{?(-?[\d.]*(?:\\pi)?)\}?/g)) { const a = endp(m[1]), b = endp(m[2]); if (a && b && a !== b) out.set(`${a}:${b}`, null); }
  for (const m of text.matchAll(/(-?[\d.]+(?:\\pi)?)\s*\\le(?:q)?\s*([a-z])\s*\\le(?:q)?\s*(-?[\d.]+(?:\\pi)?)/g)) { const a = endp(m[1]), b = endp(m[3]); if (a && b && a !== b) out.set(`${a}:${b}`, m[2]); }
  return out;
}
// ---------- the unit ----------
const SPAN = /\$\$[\s\S]+?\$\$|\$[^$]+\$/g;
function sentencesOf(str) {   // keeps the maths spans whole
  const spans = []; const t = str.replace(SPAN, (m) => `\u0000${spans.push(m) - 1}\u0000`);
  return t.split(/(?<=[.?!;])\s+|\n/).map((s) => s.replace(/\u0000(\d+)\u0000/g, (_, k) => spans[+k])).filter((s) => s.trim());
}
const fnKeyOf = (expr) => {
  const p = parsePoly(expr);
  if (p && p.size) { const c = canon(p); return { c, key: `p:${c.key}`, disp: showPoly(c.terms) }; }
  const np = nonPolyKey(expr); return np ? { key: `n:${np}`, c: null, disp: pretty(`n:${np}`) } : null;
};
const showMono = (m) => (m === '' ? '' : [...m.matchAll(/([a-z])(\d+)/g)].map(([, l, e]) => (e === '1' ? l : `${l}^${e}`)).join('').replace(/^v/, 'x').replace(/v/g, 'x'));
const showPoly = (terms) => terms.map((t, i) => { const a = Math.abs(t.c), body = (a === 1 && t.m ? '' : fmtN(a)) + showMono(t.m); return (i === 0 ? (t.c < 0 ? '-' : '') : t.c < 0 ? ' - ' : ' + ') + body; }).join('');
const pretty = (k) => k.replace(/^n:/, '').replace(/v/g, 'x');
const ptKey = (a, b, c) => [a, b, c].filter((x) => x !== undefined).map((x) => fmtN(Number(x))).join(',');

export function shapesOf(strings, node) {
  const sh = { fi: new Map(), fn: new Map(), terms: [], dp: new Map(), ls: new Map(), T: new Map(), CI: new Map(), EP: new Map(), lines: [], pkeys: [] };
  const sigPoly = (c) => (c.nterms >= 3 && c.deg >= 2) || (c.nterms >= 2 && c.deg >= 3);
  for (const str of strings) {
    if (str.length > 4000) continue;
    for (const m of mathOf(str)) {
      for (const pc of pieces(m)) {
        const p = parsePoly(pc);
        if (!p || !p.size) continue;
        const c = canon(p);
        if (![...c.vars].every((v) => VARS.includes(v))) continue;   // a, b, c, h, k, n ... are usually parameters: a formula in them is a taught identity, not a worked function
        if (sigPoly(c)) {
          const disp = showPoly(c.terms), d = depressed(p), power = c.deg >= 3 ? d === null : c.deg === 2 && c.vars.size === 1 && perfectSquare(c);   // (x + a)^n expanded is stock
          if (!power) { sh.fn.set(`p:${c.key}`, { disp, cross: c.deg >= 3 && c.nterms >= 3 && !isStockQuad(c) }); if (d && c.nterms >= 3) sh.dp.set(d, disp); }
        }
        if (c.vars.size >= 2) { const heavy = c.terms.filter((t) => t.d >= 3); if (c.nterms >= 2 && heavy.length && c.terms.reduce((a, t) => a + t.d, 0) >= 6) sh.terms.push({ key: c.key, disp: showPoly(c.terms), ts: c.terms.map((t) => `${fmtN(t.c)}${t.m}`), heavy: heavy.map((t) => `${fmtN(t.c)}${t.m}`) }); }
      }
    }
    // function with its interval: in one sentence, or an integral's own bounds
    for (const sen of sentencesOf(str)) {
      const fns = new Map();
      for (const m of mathOf(sen)) {
        const lvl = /^([^=]+?)\s*=\s*([^=]+)$/.exec(m.trim());   // a level set (x^2 + y^2 = 4) keeps its right-hand side: it is not a function of its left side (R5)
        for (const pc of pieces(m, 0, false)) {   // R1 (ENGINE-BACKLOG 1053): a function under a fraction bar is keyed on the whole quotient (1/sqrt(x) is not sqrt(x))
          const f = fnKeyOf(pc);
          if (!f) continue;
          if (f.c && !((f.c.nterms >= 2 && f.c.deg >= 2) || (f.c.nterms >= 2 && f.c.deg >= 1 && f.c.vars.size === 1 && f.c.nterms >= 3))) continue;
          const level = lvl && f.c && f.c.vars.size >= 2 && lvl[1].trim() === pc.trim() ? `=${norm(lvl[2])}` : '';
          fns.set(f.key + level, { disp: f.disp + (level ? ` ${level.replace('=', '= ')}` : ''), pc });
        }
      }
      const ivs = intervalsIn(sen);
      // R5 (ENGINE-BACKLOG 1057): a named interval variable (0 <= z <= 2) must occur in the function, or the range bounds something else
      const has = (pc, v) => new RegExp(`(?<![a-zA-Z\\\\])${v}(?![a-zA-Z])`).test(pc.replace(/\\[a-zA-Z]+/g, ' '));
      for (const [fk, { disp, pc }] of fns) for (const [iv, v] of ivs) if (!/^(?:0:1|-1:1)$/.test(iv) && (!v || has(pc, v))) sh.fi.set(`${fk}@${iv}`, `${disp} on [${iv.replace(':', ', ')}]`);
    }
    for (const m of str.matchAll(/\\int_\{?(-?[\d.]*(?:\\pi)?)\}?\^\{?(-?[\d.]*(?:\\pi)?)\}?\s*(.+?)\s*\\?,?\s*\\?(?:mathrm\{)?d[a-z]\b/g)) {
      const a = endp(m[1]), b = endp(m[2]); if (!a || !b || a === b || /^(?:0:1|-1:1)$/.test(`${a}:${b}`)) continue;
      const f = fnKeyOf(m[3]); if (f && (!f.c || (f.c.nterms >= 2 && f.c.deg >= 2))) sh.fi.set(`${f.key}@${a}:${b}`, `${f.disp} on [${a}, ${b}]`);
    }
    // number sets
    for (const m of str.replace(/\\[,;! ]/g, ' ').matchAll(/-?\d+(?:\.\d+)?(?:\s*,\s*-?\d+(?:\.\d+)?){3,29}/g)) {
      const v = m[0].split(',').map(Number).sort((a, b) => a - b);
      if (new Set(v).size < 4 || v[v.length - 1] === v[0]) continue;
      const gaps = v.slice(1).map((x, i) => +(x - v[i]).toFixed(9)); if (gaps.every((g) => Math.abs(g - gaps[0]) < 1e-9)) continue;   // an arithmetic progression is stock
      const a = v.map((x) => (x - v[0]) / (v[v.length - 1] - v[0])), b = v.map((x) => (v[v.length - 1] - x) / (v[v.length - 1] - v[0])).reverse();
      const ka = a.map((x) => x.toFixed(4)).join(','), kb = b.map((x) => x.toFixed(4)).join(',');
      sh.ls.set(ka < kb ? ka : kb, m[0].replace(/\s+/g, ' ').slice(0, 60));
    }
    // numbers that sit together in one sentence (for a key pair)
    for (const sen of sentencesOf(str)) {
      const all = [...new Set([...sen.replace(/(?<=\d)(?:,|\{,\})(?=\d{3}(?!\d))/g, '').matchAll(/(?<![\w.])\d+(?:\.\d+)?(?![\w])/g)].map((x) => +x[0]))];
      const nums = all.filter(eligibleKey).map(String);
      const decs = [...sen.matchAll(/(?<![\w.])\d+\.\d+/g)].map((x) => x[0]);   // every decimal, including a coefficient (0.5h)
      // R3 (ENGINE-BACKLOG 1055): no decimal in the sentence but the two keys, stock decimals (0.5, 0.1) counted, else it is a row of chances or a ratio, not the pair
      if (nums.length === 2 && all.every((v) => Number.isInteger(v) || eligibleKey(v)) && decs.every((v) => nums.includes(String(+v)))) sh.lines.push({ nums, text: sen.replace(/\s+/g, ' ').slice(0, 90) });
    }
    // regions: corners, circles, end points and routes
    for (const sen of sentencesOf(str)) {
      const pts = []; const seen = new Set();
      for (const m of sen.matchAll(/\(\s*(-?\d+(?:\.\d+)?)\s*,\s*(-?\d+(?:\.\d+)?)(?:\s*,\s*(-?\d+(?:\.\d+)?))?\s*\)/g)) { const k = ptKey(m[1], m[2], m[3]); if (!seen.has(k)) { seen.add(k); pts.push([Number(m[1]), Number(m[2]), m[3] === undefined ? undefined : Number(m[3])]); } }
      if (pts.length >= 3 && /corner|vertex|vertices|triang|polygon|rectangle|quadrilateral|region|axes|intercept|plot|bounded|parallelogram/i.test(sen)) {
        let ps = pts, proj = false;
        if (pts.every((q) => q[2] !== undefined)) {
          proj = true;   // a plane's intercepts: the shadow on z = 0, with the origin when two of them lie on the axes
          ps = pts.filter((q) => q[2] === 0).map((q) => [q[0], q[1]]);
          if (ps.length >= 2 && ps.every((q) => q[0] === 0 || q[1] === 0)) ps.push([0, 0]);
          const u = new Map(ps.map((q) => [ptKey(q[0], q[1]), q])); ps = [...u.values()];
        } else if (pts.some((q) => q[2] !== undefined)) ps = [];
        if (ps.length >= 3 && !ps.every((q) => Math.abs(q[0]) <= 1 && Math.abs(q[1]) <= 1)) sh.T.set(ps.map((q) => ptKey(q[0], q[1])).sort().join(';'), { d: ps.map((q) => `(${q[0]}, ${q[1]})`).join(', '), proj });   // proj: the shadow of a plane's intercepts (R4, ENGINE-BACKLOG 1056)
      }
    }
  }
  const all = strings.join(' \n ').replace(/\\left|\\right/g, ''), plain = all.replace(/\$/g, ' ');
  // circles: x^2 + y^2 = N, "radius N", (N cos t, N sin t)
  const radii = new Set();
  for (const m of all.matchAll(/x\^2\s*\+\s*y\^2\s*=\s*(\d+(?:\.\d+)?)/g)) { const r = Math.sqrt(Number(m[1])); if (Math.abs(r - Math.round(r * 100) / 100) < 1e-9) radii.add(fmtN(r)); }
  for (const m of all.matchAll(/radius\s+(?:of\s+)?\$?(\d+(?:\.\d+)?)/g)) radii.add(fmtN(Number(m[1])));
  for (const m of all.matchAll(/\(\s*-?(\d+(?:\.\d+)?)\s*\\cos\s*t\s*,\s*-?\1\s*\\sin\s*t\s*\)/g)) radii.add(fmtN(Number(m[1])));
  // integrand numbers: after the word integrand, or the constant of \int_a^b N dt
  const integ = new Set();
  for (const m of all.matchAll(/integrand[^.;$]{0,40}\$\s*(-?\d+(?:\.\d+)?)/g)) integ.add(String(Math.abs(+m[1])));
  for (const m of all.matchAll(/integrand\s+(?:is\s+)?(-?\d+(?:\.\d+)?)/g)) integ.add(String(Math.abs(+m[1])));
  for (const m of all.matchAll(/\\int_[^\s]*\^[^\s]*\s*(-?\d+(?:\.\d+)?)\s*\\?,?\s*d[a-z]/g)) integ.add(String(Math.abs(+m[1])));
  for (const r of radii) for (const n of integ) if (n !== r) sh.CI.set(`${r}|${n}`, `circle of radius ${r} with integrand ${n}`);
  // end points and routes
  const eps = new Map(), routes = new Map();
  const PT = '\\(\\s*-?\\d+(?:\\.\\d+)?\\s*,\\s*-?\\d+(?:\\.\\d+)?\\s*\\)';
  for (const m of plain.matchAll(new RegExp(`(${PT})\\s*(?:to|\\\\to|\\\\rightarrow)\\s*(${PT})`, 'g'))) eps.set(`${norm(m[1])}>${norm(m[2])}`, `${m[1]} to ${m[2]}`);
  for (const m of plain.matchAll(/\(\s*t\s*\)\s*=\s*(\(.+)/g)) {
    let d = 0, end = -1; const t = m[1];
    for (let i = 0; i < t.length; i++) { if (t[i] === '(') d++; else if (t[i] === ')') { d--; if (d === 0) { end = i; break; } } }
    if (end < 0) continue;
    const comps = splitTop(t.slice(1, end), [',']).map((c) => norm(c).replace(/^-/, ''));
    if (comps.length >= 2 && comps.some((c) => /t/.test(c))) routes.set(comps.join('|'), `(${comps.join(', ')})`);
  }
  for (const [ek, ed] of eps) for (const [rk, rd] of routes) { if (/^t\|t$/.test(rk) && false) continue; sh.EP.set(`${ek}#${rk}`, `end points ${ed} with route ${rd}`); }
  // key numbers of an item, in part order (for a pair)
  if (node && Array.isArray(node.parts)) sh.pkeys = node.parts.map((p) => { const w = p && p.widget; return w && typeof w.answer === 'number' ? Math.abs(w.answer) : null; });
  // the keys of this unit (a screen, quiz item or part): R3 needs one of a pair's two values to be a key of the source unit
  const keysOf = (n) => { const w = n && n.widget, o = []; if (w && typeof w.answer === 'number') o.push(Math.abs(w.answer)); if (w && Array.isArray(w.answers)) w.answers.forEach((x) => typeof x === 'number' && o.push(Math.abs(x))); if (n && Array.isArray(n.parts)) n.parts.forEach((p) => o.push(...keysOf(p))); return o; };
  sh.keys = new Set(keysOf(node).map((x) => String(+x.toPrecision(10))));
  sh.empty = !(sh.fi.size || sh.fn.size || sh.terms.length || sh.dp.size || sh.ls.size || sh.T.size || sh.CI.size || sh.EP.size || sh.lines.length || sh.pkeys.length);
  return sh;
}

// ---------- matching ----------
const DEC_STOCK = new Set(['0.5', '0.25', '0.75', '0.05', '0.95', '0.01', '0.99', '0.1', '0.9', '0.025', '0.975', '0.001', '0.999', '1.96', '1.645', '2.576']);
const eligibleKey = (v) => { if (v === null || v === 0) return false; const s = String(+v.toPrecision(10)); if (DEC_STOCK.has(s)) return false; return !Number.isInteger(v) || (v > 20 && ![25, 30, 40, 50, 60, 75, 100, 200, 250, 500, 1000, 10000, 365, 252, 120, 150, 300, 400, 600, 1200].includes(v)); };
const shownTerm = (x) => x.replace(/^(-?[\d.]+)(.*)$/, (_, c, m) => (c === '1' ? '' : c === '-1' ? '-' : c) + showMono(m));
export function keyPairs(pkeys) { const out = []; for (let i = 0; i + 1 < pkeys.length; i++) { const a = pkeys[i], b = pkeys[i + 1]; if (eligibleKey(a) && eligibleKey(b) && a !== b) out.push([String(+a.toPrecision(10)), String(+b.toPrecision(10))]); } return out; }

// An index over every unit: kind|key -> Map(file -> unit). Built once by loadCorpus.
export function buildIndex(units) {
  const idx = new Map();
  const put = (k, u) => { let m = idx.get(k); if (!m) idx.set(k, (m = new Map())); if (!m.has(u.file)) m.set(u.file, []); m.get(u.file).push(u); };
  for (const u of units) {
    const s = u.shapes; if (!s || s.empty) continue;
    for (const k of s.fi.keys()) put(`fi|${k}`, u);
    for (const k of s.fn.keys()) put(`fn|${k}`, u);
    for (const k of s.dp.keys()) put(`dp|${k}`, u);
    for (const k of s.ls.keys()) put(`ls|${k}`, u);
    for (const k of s.T.keys()) put(`T|${k}`, u);
    for (const k of s.CI.keys()) put(`CI|${k}`, u);
    for (const k of s.EP.keys()) put(`EP|${k}`, u);
    for (const t of s.terms) for (const h of t.heavy) put(`tm|${h}`, u);
    for (const l of s.lines) for (const n of l.nums) put(`ln|${n}`, u);
  }
  return idx;
}
// Hits of one target unit against the index. `sameCourse(file)` says whether a source file is of the target's course. Returns [{ src, kind, score, evidence }].
export function matchShapes(t, idx, rel, sameCourse, { df = 4 } = {}) {
  const s = t.shapes, out = [];
  if (!s || s.empty) return out;
  const srcs = (k, wantSame) => { const m = idx.get(k); if (!m) return []; const files = [...m.keys()].filter((f) => f !== rel); if (files.length > df) return []; return files.filter((f) => wantSame === null || sameCourse(f) === wantSame).flatMap((f) => m.get(f)); };
  const push = (u, kind, evidence) => out.push({ src: u, kind, score: 1, evidence });
  // (a) function with its interval, app-wide
  for (const [k, disp] of s.fi) for (const u of srcs(`fi|${k}`, null)) push(u, 'function', `${disp} (a function with its interval)`);
  // (a) one polynomial with its factorisation: any file of the course; other courses only when it is not a simple quadratic with small whole roots
  for (const [k, v] of s.fn) {
    for (const u of srcs(`fn|${k}`, true)) push(u, 'function', `${v.disp} (the same polynomial, factorised or not, with the letter renamed)`);
    if (v.cross) for (const u of srcs(`fn|${k}`, false)) push(u, 'function', `${v.disp} (the same polynomial in another course)`);
  }
  // (a) the heavy terms of a multivariable polynomial (a potential against the function it was cut from), app-wide
  const seenT = new Set();
  for (const a of s.terms) {
    const cand = new Map();
    for (const h of a.heavy) { const m = idx.get(`tm|${h}`); if (!m || m.size > df + 2) continue; for (const [f, us] of m) if (f !== rel) for (const u of us) cand.set(u, true); }
    for (const [u] of cand) for (const b of u.shapes.terms) {
      const shared = a.ts.filter((x) => b.ts.includes(x));
      if (shared.length >= 2 && shared.some((x) => a.heavy.includes(x)) && !seenT.has(`${u.file}${u.path}${a.key}`)) { seenT.add(`${u.file}${u.path}${a.key}`); push(u, 'function', `${shared.map(shownTerm).join(', ')} shared by ${a.disp} and ${b.disp} (a function with a term added or dropped)`); }
    }
  }
  // (d) regions: app-wide
  // a projected plane's intercepts run in the same course only (R4); plain corner sets stay app-wide
  for (const [k, v] of s.T) for (const u of srcs(`T|${k}`, v.proj ? true : null)) if (!u.shapes.T.get(k).proj || sameCourse(u.file)) push(u, 'region', `corners ${v.d}${v.proj ? ' (the shadow of a plane\'s intercepts on z = 0)' : ''}`);
  for (const [k, d] of s.CI) for (const u of srcs(`CI|${k}`, null)) push(u, 'region', d);
  for (const [k, d] of s.EP) for (const u of srcs(`EP|${k}`, null)) push(u, 'region', d);
  // (c) shifted and scaled, same course
  for (const [k, d] of s.dp) { const own = new Set([...s.fn].filter(([, v]) => v.disp === d).map(([kk]) => kk)); for (const u of srcs(`dp|${k}`, true)) { const same = [...u.shapes.fn.keys()].some((x) => own.has(x)); if (!same) push(u, 'transform', `${d} against ${u.shapes.dp.get(k)}: the same polynomial shifted and scaled (equal after x -> a x + b, up to a factor)`); } }
  for (const [k, d] of s.ls) for (const u of srcs(`ls|${k}`, true)) push(u, 'transform', `the number set ${d} against ${u.shapes.ls.get(k)}: equal after x -> a x + b`);
  // (b) two consecutive part keys in one sentence of the course
  if (s.pkeys.length) for (const [a, b] of keyPairs(s.pkeys)) {
    const ma = idx.get(`ln|${a}`), mb = idx.get(`ln|${b}`); if (!ma || !mb) continue;
    for (const [f, us] of ma) { if (f === rel || !sameCourse(f)) continue; for (const u of us) for (const l of u.shapes.lines) if (l.nums.includes(a) && l.nums.includes(b) && (u.shapes.keys.has(a) || u.shapes.keys.has(b))) { push(u, 'pair', `consecutive part keys ${a} and ${b} sit together in "${l.text}"`); break; } }
  }
  return out;
}
