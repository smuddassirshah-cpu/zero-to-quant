#!/usr/bin/env node
/* Duplicate-key lint for the engine's JavaScript (ENGINE-BACKLOG 571).
   Reports (1) an object literal that repeats a key, and (2) a later `X.y = <function>` assignment in the same file that replaces
   a function defined in X's own object literal (the shadowed `readiness.status` class of bug).
   No dependencies: a small tokenizer (strings, comments, template literals with ${} nesting, regex) and a brace stack.
   Usage: node tools/lint-dup-keys.mjs [files or directories ...]   (default: everything under js/)
   Exit 1 on any finding. Getter/setter pairs and computed keys are not counted. */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const KW_BEFORE_REGEX = new Set(['return', 'typeof', 'instanceof', 'in', 'of', 'new', 'delete', 'void', 'throw', 'case', 'do', 'else', 'yield', 'await']);

export function tokenize(src) {
  const toks = [];
  let i = 0, line = 1;
  const n = src.length;
  const tpl = [];   /* brace depth markers for open ${ } inside template literals */
  let depth = 0;
  const push = (t, v) => toks.push({ t, v, line });
  const scanTemplate = () => {   /* from just after ` or after the } closing a ${ ; ends at ` or at ${ */
    while (i < n) {
      const c = src[i];
      if (c === '\n') line++;
      if (c === '\\') { i += 2; continue; }
      if (c === '`') { i++; return; }
      if (c === '$' && src[i + 1] === '{') { i += 2; tpl.push(depth); depth++; push('p', '${'); return; }
      i++;
    }
  };
  while (i < n) {
    const c = src[i];
    if (c === '\n') { line++; i++; continue; }
    if (/\s/.test(c)) { i++; continue; }
    if (c === '/' && src[i + 1] === '/') { while (i < n && src[i] !== '\n') i++; continue; }
    if (c === '/' && src[i + 1] === '*') { const e = src.indexOf('*/', i + 2); const end = e < 0 ? n : e + 2; line += (src.slice(i, end).match(/\n/g) || []).length; i = end; continue; }
    if (c === '"' || c === "'") {
      let j = i + 1, v = '';
      while (j < n && src[j] !== c) { if (src[j] === '\\') { v += src[j + 1]; j += 2; } else { v += src[j]; j++; } }
      push('s', v); i = j + 1; continue;
    }
    if (c === '`') { i++; push('s', '`'); scanTemplate(); continue; }
    if (/[A-Za-z_$]/.test(c)) { let j = i + 1; while (j < n && /[\w$]/.test(src[j])) j++; push('i', src.slice(i, j)); i = j; continue; }
    if (/[0-9]/.test(c) || (c === '.' && /[0-9]/.test(src[i + 1] || ''))) { let j = i + 1; while (j < n && /[\w.]/.test(src[j])) j++; push('n', src.slice(i, j)); i = j; continue; }
    if (c === '/') {
      const p = toks[toks.length - 1];
      const div = p && (p.t === 'n' || p.t === 's' || p.t === 'r' || (p.t === 'i' && !KW_BEFORE_REGEX.has(p.v)) || (p.t === 'p' && (p.v === ')' || p.v === ']' || p.v === '}' || p.v === '}$')));
      if (!div) {
        let j = i + 1, cls = false;
        while (j < n && src[j] !== '\n') { if (src[j] === '\\') { j += 2; continue; } if (src[j] === '[') cls = true; else if (src[j] === ']') cls = false; else if (src[j] === '/' && !cls) break; j++; }
        j++; while (j < n && /[a-z]/.test(src[j])) j++;
        push('r', ''); i = j; continue;
      }
    }
    if (c === '{') { depth++; push('p', '{'); i++; continue; }
    if (c === '}') {
      depth--;
      if (tpl.length && tpl[tpl.length - 1] === depth) { tpl.pop(); i++; push('p', '}$'); scanTemplate(); continue; }
      push('p', '}'); i++; continue;
    }
    const m = /^(\.\.\.|===|!==|=>|==|!=|<=|>=|&&|\|\||\?\?|\?\.|\+\+|--|\*\*|[-+*/%&|^]=|<<|>>)/.exec(src.slice(i, i + 3));
    if (m) { push('p', m[0]); i += m[0].length; continue; }
    push('p', c); i++;
  }
  return toks;
}

/* Is a function value (method shorthand, function, arrow) starting at token index k? Plain data keys re-assigned later are normal state updates and are not reported. */
function fnAt(toks, k) {
  const t = toks[k];
  if (!t) return false;
  if (t.t === 'i' && (t.v === 'function' || t.v === 'async')) return true;
  if (t.t === 'i') return !!(toks[k + 1] && toks[k + 1].v === '=>');
  if (t.t === 'p' && t.v === '(') {
    let d = 0, q = k;
    for (; q < toks.length; q++) { const x = toks[q]; if (x.t !== 'p') continue; if (x.v === '(') d++; else if (x.v === ')' && --d === 0) break; }
    return !!(toks[q + 1] && toks[q + 1].v === '=>');
  }
  return false;
}

/* An opening brace starts an object literal (not a block) after these */
const OBJ_PREV = new Set(['(', ',', '=', ':', '[', '?', '||', '&&', '??', '...', '!', '+', '-', '*', '/', '|', '&']);
function opensObject(prev) {
  if (!prev) return false;
  if (prev.t === 'p') return OBJ_PREV.has(prev.v);
  if (prev.t === 'i') return ['return', 'yield', 'typeof', 'await', 'in', 'of'].includes(prev.v);
  return false;
}

export function lint(src, file = '<src>') {
  const toks = tokenize(src), out = [];
  const stack = [];    /* { kind: 'obj' | 'blk' | 'par', keys, line } */
  const literals = []; /* { path, keys, at } for `a.b = { ... }` and `const a = { ... }` */
  for (let k = 0; k < toks.length; k++) {
    const t = toks[k], prev = toks[k - 1];
    if (t.t === 'p' && t.v === '${') { stack.push({ kind: 'par' }); continue; }
    if (t.t === 'p' && t.v === '{') {
      let isObj = opensObject(prev);
      if (isObj && prev.v === ':') {   /* `case x: {` is a block; a property or ternary value is an object */
        let q = k - 2, isCase = false;
        for (; q >= 0 && q > k - 40; q--) { const x = toks[q]; if (x.t === 'p' && (x.v === ';' || x.v === '{' || x.v === '}')) break; if (x.t === 'i' && (x.v === 'case' || x.v === 'default')) { isCase = true; break; } }
        if (isCase) isObj = false;
      }
      const fr = { kind: isObj ? 'obj' : 'blk', keys: new Map(), line: t.line };
      if (isObj && prev.v === '=') {   /* name the literal when it is the right-hand side of `a.b.c =` */
        let q = k - 2; const parts = [];
        while (q >= 0 && toks[q].t === 'i') { parts.unshift(toks[q].v); if (toks[q - 1] && toks[q - 1].v === '.') q -= 2; else break; }
        if (parts.length) literals.push({ path: parts.join('.'), keys: fr.keys, at: k });
      }
      stack.push(fr); continue;
    }
    if (t.t === 'p' && (t.v === '(' || t.v === '[')) { stack.push({ kind: 'par' }); continue; }
    if (t.t === 'p' && (t.v === '}' || t.v === '}$' || t.v === ')' || t.v === ']')) { stack.pop(); continue; }
    const top = stack[stack.length - 1];
    if (top && top.kind === 'obj' && prev && prev.t === 'p' && (prev.v === '{' || prev.v === ',')) {
      let q = k, accessor = null;
      if (toks[q].t === 'p') { if (toks[q].v === '*') q++; else continue; }
      if (toks[q] && toks[q].t === 'i' && toks[q].v === 'async' && toks[q + 1] && (toks[q + 1].t === 'i' || toks[q + 1].t === 's')) q++;
      if (toks[q] && toks[q].t === 'i' && (toks[q].v === 'get' || toks[q].v === 'set') && toks[q + 1] && (toks[q + 1].t === 'i' || toks[q + 1].t === 's' || toks[q + 1].t === 'n')) { accessor = toks[q].v; q++; }
      const kt = toks[q], nx = toks[q + 1];
      if (!kt || !(kt.t === 'i' || kt.t === 's' || kt.t === 'n') || kt.v === '`') continue;
      if (!(nx && nx.t === 'p' && (nx.v === ':' || nx.v === '(' || nx.v === ',' || nx.v === '}'))) continue;
      const seen = top.keys.get(kt.v);
      if (seen && !(accessor && seen.accessor && seen.accessor !== accessor)) out.push({ file, line: kt.line, msg: `duplicate key "${kt.v}" in object literal (first at line ${seen.line})` });
      else if (!seen) top.keys.set(kt.v, { line: kt.line, accessor, fn: nx.v === '(' || (nx.v === ':' && fnAt(toks, q + 2)) });
    }
  }
  /* a later X.y = ... overwriting a key of X's literal */
  for (const lit of literals) {
    for (let k = lit.at; k < toks.length; k++) {
      const t = toks[k];
      if (t.t !== 'p' || t.v !== '=') continue;
      let q = k - 1;
      if (!(toks[q] && toks[q].t === 'i')) continue;
      const parts = [];
      while (q >= 0 && toks[q].t === 'i') { parts.unshift(toks[q].v); if (toks[q - 1] && toks[q - 1].t === 'p' && toks[q - 1].v === '.') q -= 2; else break; }
      if (parts.length < 2 || (toks[q] && toks[q].t === 'p' && toks[q].v === '.')) continue;
      const owner = parts.slice(0, -1).join('.'), key = parts[parts.length - 1];
      if (owner === lit.path && lit.keys.has(key) && lit.keys.get(key).fn && fnAt(toks, k + 1)) out.push({ file, line: t.line, msg: `"${owner}.${key} =" replaces the function "${key}" defined in the literal assigned to "${owner}" (line ${lit.keys.get(key).line})` });
    }
  }
  return out;
}

function collect(p, acc) {
  if (fs.statSync(p).isDirectory()) for (const f of fs.readdirSync(p).sort()) collect(path.join(p, f), acc);
  else if (/\.m?js$/.test(p)) acc.push(p);
  return acc;
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
  const args = process.argv.slice(2);
  const files = args.length ? args.flatMap(a => collect(a, [])) : collect(path.join(root, 'js'), []);
  const found = [];
  for (const f of files) found.push(...lint(fs.readFileSync(f, 'utf8'), path.relative(process.cwd(), f)));
  for (const r of found) console.log(`${r.file}:${r.line}: ${r.msg}`);
  console.log(`lint-dup-keys: ${files.length} files, ${found.length} finding${found.length === 1 ? '' : 's'}`);
  process.exit(found.length ? 1 : 0);
}
