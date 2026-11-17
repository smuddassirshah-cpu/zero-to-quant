#!/usr/bin/env node
// Writes every same-course reuse hit of the problem sets as a Markdown triage list (engine pass AF part 1, task 3; engine pass 8 B): a count table (kinds by course), then one block per hit,
// grouped by course: set path, item and part, kind, source path (an exam source is marked), the tag ([exam-reuse] or [slip-line] for a hit of the checks of pass 8 B), and EVERY matched pair, both texts cut to 200 characters.
// Waivers are ignored, so the list shows what the checks see.
// Usage (from app/): node tools/reuse-hits-report.mjs [--out ../docs/reports/same-course-reuse-af-hits.md] [--content <dir>] [--exclude <hits.json>] [--title <text>]
//   --exclude  a JSON of hits (same-course-reuse.mjs --all --no-waivers --json, of an older checker): a hit with the same set, item, kind and source file is left out, so that the list holds only what the newer checker adds.
import { readFileSync, writeFileSync } from 'node:fs';
import { join, dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { loadCorpus, scanSet } from './same-course-reuse.mjs';

const HERE = dirname(fileURLToPath(import.meta.url)), APP = join(HERE, '..');
const argv = process.argv.slice(2), O = (k, d) => { const i = argv.indexOf(k); return i >= 0 ? argv[i + 1] : d; };
const C = resolve(O('--content', join(APP, 'content'))), OUT = resolve(O('--out', join(APP, '..', 'docs', 'reports', 'same-course-reuse-af-hits.md')));
process.env.ZQ_NO_WAIVERS = '1';
process.env.ZQ_EXAM_ERRORS = '1';   // the list shows exam hits as the errors they will be for a new set
const corpus = loadCorpus(C);
const KINDS = ['retold', 'rate', 'numbers', 'matrix', 'text', 'function', 'pair', 'transform', 'region'];
const old = O('--exclude', null) ? new Set(JSON.parse(readFileSync(resolve(O('--exclude')), 'utf8')).map((h) => `${h.file}|${h.itemId}|${h.kind}|${h.source.split(':')[0]}`)) : new Set();
const rows = [];
const sets = [...corpus.byFile.keys()].filter((f) => /\/problems-\d+\.json$/.test(f));
for (const rel of sets) {
  const doc = JSON.parse(readFileSync(join(C, rel), 'utf8'));
  for (const h of scanSet(corpus, rel, doc)) {
    const id = (doc.items?.[Number(h.item.match(/\d+/)[0])] ?? {}).id;
    if (old.has(`${h.file}|${id}|${h.kind}|${h.source.split(':')[0]}`)) continue;
    rows.push({ ...h, course: rel.split('/')[1], id });
  }
}
const cut = (s, n = 200) => { s = String(s ?? '').replace(/\s+/g, ' ').trim(); return s.length > n ? `${s.slice(0, n - 1)}…` : s; };
const courses = [...new Set(rows.map((r) => r.course))].sort();
const ks = KINDS.filter((k) => rows.some((r) => r.kind === k));
const out = [];
out.push(`# ${O('--title', 'Same-course reuse hits')}`, '');
out.push(`Every hit of \`node tools/same-course-reuse.mjs --all --no-waivers --exam-errors\` over the ${sets.length} problem sets${old.size ? ', less the hits that the older checker already reported (same set, item, kind and source file)' : ''}, written by \`node tools/reuse-hits-report.mjs\`. No content was edited and no waiver added.`, '');
out.push('A block gives the set, the item id and part, the kind, the source (file and unit; an **exam** source also names the exam item), a tag, and every matched pair, the problem\'s text first and the source\'s second. Tags: `[exam-reuse]` the source is an item of a topic, stage or mock exam that carries the course\'s skills; `[slip-line]` the hit rests on an identical short slip line ("You ...", numbers and maths masked) alone. `retold`: sentences or a chain of steps retold; `rate`: a rate in a decimal or fraction against a per cent; a pair printed as `[w, n]` has the weight of the match and its count of informative common words (99: an identical slip line).', '');
out.push('## Count', '');
out.push(`| course | ${ks.join(' | ')} | exam | slip-line | total |`, `|${'---|'.repeat(ks.length + 4)}`);
for (const c of courses) { const r = rows.filter((x) => x.course === c); out.push(`| ${c} | ${ks.map((k) => r.filter((x) => x.kind === k).length || '').join(' | ')} | ${r.filter((x) => x.exam).length || ''} | ${r.filter((x) => x.tag === 'slip-line').length || ''} | ${r.length} |`); }
out.push(`| **all** | ${ks.map((k) => `**${rows.filter((r) => r.kind === k).length}**`).join(' | ')} | **${rows.filter((r) => r.exam).length}** | **${rows.filter((r) => r.tag === 'slip-line').length}** | **${rows.length}** |`, '');
out.push('## Hits by course', '');
for (const c of courses) {
  out.push(`### ${c}`, '');
  for (const r of rows.filter((x) => x.course === c)) {
    out.push(`- \`${r.file.replace('courses/', '')}\` ${r.id} (${r.item}${r.part ? `, part ${r.part}` : ''}) | ${r.kind} | ${r.exam ? `**exam** \`${r.source}\`${r.sourceId ? ` (${r.sourceId})` : ''}` : `\`${r.source.replace(/^courses\//, '')}\``}${r.exam ? ' | [exam-reuse]' : ''}${r.tag ? ` | [${r.tag}]` : ''}`);
    const pairs = r.pairs ?? (r.texts ? [r.texts] : []);
    if (pairs.length) for (const p of pairs) out.push(`  - "${cut(p[0])}" <- "${cut(p[1])}"${p.length > 3 ? ` [${p[2]}, ${p[3]}]` : ''}`);
    else out.push(`  - ${cut(r.evidence, 330)}`);
  }
  out.push('');
}
writeFileSync(OUT, `${out.join('\n')}\n`);
console.log(`${rows.length} hits in ${courses.length} courses written to ${OUT}`);
