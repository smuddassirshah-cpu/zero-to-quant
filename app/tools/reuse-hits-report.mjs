#!/usr/bin/env node
// Writes every same-course reuse hit of the problem sets as a Markdown triage list (engine pass AF part 1, task 3): a count table (kinds by course), then one line per hit,
// grouped by course: set path, item and part, kind, source path, and both texts cut to 160 characters. Waivers are ignored, so the list shows what the checks see.
// Usage (from app/): node tools/reuse-hits-report.mjs [--out ../docs/reports/same-course-reuse-af-hits.md] [--content <dir>]
import { readFileSync, writeFileSync } from 'node:fs';
import { join, dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { loadCorpus, scanSet } from './same-course-reuse.mjs';

const HERE = dirname(fileURLToPath(import.meta.url)), APP = join(HERE, '..');
const argv = process.argv.slice(2), O = (k, d) => { const i = argv.indexOf(k); return i >= 0 ? argv[i + 1] : d; };
const C = resolve(O('--content', join(APP, 'content'))), OUT = resolve(O('--out', join(APP, '..', 'docs', 'reports', 'same-course-reuse-af-hits.md')));
process.env.ZQ_NO_WAIVERS = '1';
const corpus = loadCorpus(C);
const KINDS = ['retold', 'rate', 'numbers', 'matrix', 'text', 'function', 'pair', 'transform', 'region'];
const rows = [];
for (const rel of [...corpus.byFile.keys()].filter((f) => /\/problems-\d+\.json$/.test(f))) {
  const doc = JSON.parse(readFileSync(join(C, rel), 'utf8'));
  for (const h of scanSet(corpus, rel, doc)) {
    // the kinds of before engine pass AF part 1 are held by waivers and the content; list them too, tagged, so that nothing hides
    rows.push({ ...h, course: rel.split('/')[1], id: (doc.items?.[Number(h.item.match(/\d+/)[0])] ?? {}).id });
  }
}
const cut = (s, n = 160) => { s = String(s ?? '').replace(/\s+/g, ' ').trim(); return s.length > n ? `${s.slice(0, n - 1)}…` : s; };
const courses = [...new Set(rows.map((r) => r.course))].sort();
const esc = (s) => s.replace(/\|/g, '\\|');
const out = [];
out.push('# Same-course reuse hits of the extended check (engine pass AF part 1)', '');
out.push(`Every hit of \`node tools/same-course-reuse.mjs --all --no-waivers\` over the ${new Set([...corpus.byFile.keys()].filter((f) => /\/problems-\d+\.json$/.test(f))).size} problem sets, written by \`node tools/reuse-hits-report.mjs\`. No content was edited and no waiver added.`, '');
out.push('A line gives the set, the item id and part, the kind, the source (file and unit of the same course) and the two texts, each cut to 160 characters (the first is the problem\'s, the second the source\'s). `retold`: a sentence skeleton or a chain of steps retold (feedback, explain and why lines are read too); `rate`: a rate in a decimal or fraction against a per cent with a second number shared. Kinds listed as waived are held by `tools/same-course-waivers.json`.', '');
out.push('## Count', '');
out.push(`| course | ${KINDS.filter((k) => rows.some((r) => r.kind === k)).join(' | ')} | total |`);
const ks = KINDS.filter((k) => rows.some((r) => r.kind === k));
out.push(`|${'---|'.repeat(ks.length + 2)}`);
for (const c of courses) out.push(`| ${c} | ${ks.map((k) => rows.filter((r) => r.course === c && r.kind === k).length || '').join(' | ')} | ${rows.filter((r) => r.course === c).length} |`);
out.push(`| **all** | ${ks.map((k) => `**${rows.filter((r) => r.kind === k).length}**`).join(' | ')} | **${rows.length}** |`, '');
out.push(`Of the ${rows.length} hits ${rows.filter((r) => !['retold', 'rate'].includes(r.kind)).length} are of kinds that existed before (held by \`tools/same-course-waivers.json\`, shown here because waivers are ignored); the other ${rows.filter((r) => ['retold', 'rate'].includes(r.kind)).length} are new (retold ${rows.filter((r) => r.kind === 'retold').length}, rate ${rows.filter((r) => r.kind === 'rate').length}).`, '');
out.push('## Hits by course', '');
for (const c of courses) {
  out.push(`### ${c}`, '');
  for (const r of rows.filter((x) => x.course === c)) {
    const t = r.texts ?? [];
    const first = t.length ? `"${cut(t[0])}" | "${cut(t[1])}"${r.kind === 'rate' ? ` (${r.evidence})` : ''}` : cut(r.evidence, 330);
    out.push(`- \`${r.file.replace('courses/', '')}\` ${r.id} (${r.item}${r.part ? `, part ${r.part}` : ''}) | ${r.kind}${r.waived ? ' (waived)' : ''} | \`${r.source.replace(/^courses\//, '')}\` | ${first}`);
  }
  out.push('');
}
writeFileSync(OUT, `${out.join('\n')}\n`);
console.log(`${rows.length} hits in ${courses.length} courses written to ${OUT}`);
