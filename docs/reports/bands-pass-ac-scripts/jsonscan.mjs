// Minimal JSON scanner with character offsets, for text-level edits that keep a file's own formatting.
// scan(text) -> node { t:'obj'|'arr'|'str'|'num'|'lit', s, e, members:[{key, ks, ke, v}] | items:[node] }
export function scan(text) {
  let i = 0;
  const ws = () => { while (i < text.length && /\s/.test(text[i])) i++; };
  const val = () => {
    ws();
    const s = i, c = text[i];
    if (c === '{') {
      i++; const members = [];
      ws();
      if (text[i] === '}') { i++; return { t: 'obj', s, e: i, members }; }
      for (;;) {
        ws(); const ks = i; const k = str(); const ke = i; ws(); i++; // colon
        const v = val(); members.push({ key: k, ks, ke, v }); ws();
        if (text[i] === ',') { i++; continue; }
        if (text[i] === '}') { i++; break; }
        throw new Error('bad object at ' + i);
      }
      return { t: 'obj', s, e: i, members };
    }
    if (c === '[') {
      i++; const items = [];
      ws();
      if (text[i] === ']') { i++; return { t: 'arr', s, e: i, items }; }
      for (;;) {
        items.push(val()); ws();
        if (text[i] === ',') { i++; continue; }
        if (text[i] === ']') { i++; break; }
        throw new Error('bad array at ' + i);
      }
      return { t: 'arr', s, e: i, items };
    }
    if (c === '"') { const k = str(); return { t: 'str', s, e: i, v: k }; }
    const m = /^-?\d+(\.\d+)?([eE][+-]?\d+)?|^true|^false|^null/.exec(text.slice(i));
    if (!m) throw new Error('bad token at ' + i);
    i += m[0].length;
    return { t: /^-?\d/.test(m[0]) ? 'num' : 'lit', s, e: i, v: m[0] };
  };
  const str = () => {
    const s = i; i++;
    while (text[i] !== '"') { if (text[i] === '\\') i++; i++; }
    i++;
    return JSON.parse(text.slice(s, i));
  };
  return val();
}

export const prop = (n, k) => n?.t === 'obj' ? n.members.find(m => m.key === k)?.v : undefined;
export const at = (n, path) => {
  for (const t of path.matchAll(/([A-Za-z_][A-Za-z0-9_]*)|\[(\d+)\]/g)) n = t[1] !== undefined ? prop(n, t[1]) : n?.items?.[+t[2]];
  return n;
};
// the object that holds node `target` (walks the tree)
export const parentOf = (root, path) => {
  const toks = [...path.matchAll(/([A-Za-z_][A-Za-z0-9_]*)|\[(\d+)\]/g)];
  let n = root, par = null;
  for (const t of toks) { par = n; n = t[1] !== undefined ? prop(n, t[1]) : n?.items?.[+t[2]]; }
  return par;
};
// path of the parent of a widget path ("items[2].parts[1].widget" -> "items[2].parts[1]")
export const upPath = (p) => p.replace(/\.?[A-Za-z_][A-Za-z0-9_]*$/, '');
export const toJS = (text, n) => JSON.parse(text.slice(n.s, n.e));

// Edit to append `memberText` (already formatted) to an array or object node, copying the separators in use.
// kind 'arr': memberText is the element text; kind 'obj': memberText is `"key": value` text.
export function appendEdit(text, node, memberText) {
  const els = node.t === 'arr' ? node.items : node.members;
  const first = node.t === 'arr' ? els[0].s : els[0].ks;
  const lastEnd = node.t === 'arr' ? els[els.length - 1].e : els[els.length - 1].v.e;
  let sep;
  if (els.length >= 2) {
    const e2 = els[els.length - 2], l = els[els.length - 1];
    const prevEnd = node.t === 'arr' ? e2.e : e2.v.e;
    const lastStart = node.t === 'arr' ? l.s : l.ks;
    sep = text.slice(prevEnd, lastStart);           // ",\n        " or ", "
  } else {
    sep = ',' + (/\n/.test(text.slice(node.s, first)) ? text.slice(node.s + 1, first).replace(/^[^\n]*/, '') : ' ');
  }
  return { pos: lastEnd, del: 0, text: sep + memberText };
}
export const applyEdits = (text, edits) => {
  const es = [...edits].sort((a, b) => b.pos - a.pos);
  for (const e of es) text = text.slice(0, e.pos) + e.text + text.slice(e.pos + e.del);
  return text;
};
