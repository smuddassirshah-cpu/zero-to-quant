#!/usr/bin/env node
// Helper for merge-wave.sh (session V, item 603): after `git merge-file --union` has kept both sides of docs/readiness.md,
// a row that both sides touched appears twice. Reduce each repeated row key (the first cell, within the same heading) to one row:
// ours when ours changed it from the base, else theirs (so a row only theirs edited keeps their edit), ours first in position.
// A row only one side added stays. A key that repeats in one table of OURS is left alone.
// Usage: node tools/union-table-rows.mjs <merged-file> <base-file> <ours-file> <theirs-file>   (rewrites <merged-file>)
import { readFileSync, writeFileSync } from 'node:fs';

const [merged, base, ours, theirs] = process.argv.slice(2);
if (!theirs) { console.error('usage: union-table-rows.mjs <merged> <base> <ours> <theirs>'); process.exit(2); }
const read = (p) => { try { return readFileSync(p, 'utf8').split('\n'); } catch { return []; } };
const keyOf = (line) => { const c = line.split('|')[1]; return c == null ? null : c.trim(); };
const isRow = (line) => /^\|/.test(line) && !/^\|\s*:?-{2,}/.test(line);
/* [{ i, id, line }] for each table row: id is the nearest heading plus the first cell */
const rowsOf = (lines) => {
  const out = []; let head = '';
  lines.forEach((l, i) => { if (/^#{1,6}\s/.test(l)) head = l; if (isRow(l)) out.push({ i, id: `${head}||${keyOf(l)}`, line: l }); });
  return out;
};
const map = (lines) => { const m = new Map(); rowsOf(lines).forEach((r) => { if (!m.has(r.id)) m.set(r.id, r.line); }); return m; };
const B = map(read(base)), O = map(read(ours)), T = map(read(theirs));
const ourDup = new Set(); { const seen = new Set(); rowsOf(read(ours)).forEach((r) => { if (seen.has(r.id)) ourDup.add(r.id); seen.add(r.id); }); }
const lines = read(merged), first = new Map(), drop = new Set();
for (const r of rowsOf(lines)) {
  if (ourDup.has(r.id)) continue;
  if (!first.has(r.id)) { first.set(r.id, r); continue; }
  drop.add(r.i);
}
for (const [id, r] of first) {
  if (![...rowsOf(lines)].some((x) => x.id === id && x.i !== r.i && !ourDup.has(id))) continue;
  const o = O.get(id), t = T.get(id), b = B.get(id);
  lines[r.i] = o !== undefined && o !== b ? o : (t !== undefined ? t : r.line);
}
writeFileSync(merged, lines.filter((_, i) => !drop.has(i)).join('\n'));
console.log(`union-table-rows: reduced ${drop.size} repeated row(s)`);
