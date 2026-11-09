// Checks docs/reports/<course>-<n>-perf.md for every level with a performance task (ENGINE-BACKLOG 699).
// Run from app/: node tools/perf-reports.mjs [--warn]   (regenerate content/manifest.json with tools/validate.mjs first)
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

export const reportName = (key) => { const [c, l] = key.split('/'); return `${c}-${String(l).replace(/^L/i, '')}-perf.md`; };

const stripLead = (s) => s.replace(/^[\s>#*_\-]+/, '');
const GATES = [['validator', /validat/i], ['voice', /voice/i], ['numbers script', /numbers/i], ['playthrough', /playthrough/i]];

export function checkReport(text, task) {
  const miss = [];
  const lines = text.split('\n');
  if (!text.includes(task.item)) miss.push('item id');
  if (!new RegExp(`\\b${task.kind}\\b`, 'i').test(text)) miss.push('kind');
  if (!lines.some((l) => /objective/i.test(l) && /["“”`]|\bl\d+\b|\blesson\b/i.test(l))) miss.push('matched objective');
  const i = lines.findIndex((l) => /^overlapping screens/i.test(stripLead(l)));
  if (i < 0) miss.push('Overlapping screens line');
  else {
    let rest = stripLead(lines[i]).replace(/^overlapping screens/i, '').replace(/[\s:*_\-]+/, ' ').trim();
    if (!/\w/.test(rest)) { // heading or bold lead alone: read the next non-empty line
      const next = lines.slice(i + 1).find((l) => l.trim());
      rest = next || '';
    }
    if (!(/\bnone\b/i.test(rest) || /`|\bl\d+\b|screen/i.test(rest))) miss.push('Overlapping screens line');
  }
  for (const [name, re] of GATES) if (!re.test(text)) miss.push(`gate: ${name}`);
  return miss;
}

export function checkAll(perf, dir) {
  const missing = [], noReport = [];
  for (const [key, task] of Object.entries(perf)) {
    const name = reportName(key);
    const f = path.join(dir, name);
    if (!fs.existsSync(f)) { noReport.push(name); continue; }
    for (const part of checkReport(fs.readFileSync(f, 'utf8'), task)) missing.push({ report: name, part });
  }
  return { missing, noReport };
}

if (process.argv[1] === fileURLToPath(import.meta.url)) {
  const warn = process.argv.includes('--warn');
  const perf = JSON.parse(fs.readFileSync('content/manifest.json', 'utf8')).perf || {};
  const { missing, noReport } = checkAll(perf, '../docs/reports');
  for (const m of missing) console.log(`${m.report}: missing ${m.part}`);
  if (noReport.length) { console.log(`Levels with a task but no report (${noReport.length}):`); for (const n of noReport) console.log(`  ${n}`); }
  const counts = {};
  for (const m of missing) counts[m.part] = (counts[m.part] || 0) + 1;
  const reports = Object.keys(perf).length - noReport.length;
  console.log(`${Object.keys(perf).length} levels with a task, ${reports} reports, ${noReport.length} without a report, ${missing.length} missing parts in ${new Set(missing.map((m) => m.report)).size} reports`);
  for (const [p, n] of Object.entries(counts)) console.log(`  ${p}: ${n}`);
  process.exitCode = (missing.length || noReport.length) && !warn ? 1 : 0;
}
