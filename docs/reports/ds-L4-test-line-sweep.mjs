// Usage: node docs/reports/ds-L4-test-line-sweep.mjs <absolute app dir> <pkgs dir> docs/reports/ds-L4-test-line-codings.txt
// Sweep of the feedback.byKey.test-N lines of ds level 4 (docs/reviews/audit-ds-4.md): each block "### <file> <s#|i#> <N> <name>\n<python>" is appended to the widget's solution
// (a later def replaces the earlier one) and graded by the page's own harness under Pyodide.
import fs from 'node:fs';
import path from 'node:path';
const [,, appDir, pkgs, mfile] = process.argv;
const { makeRunner } = await import(path.join(appDir, 'tools/code-runner.mjs'));
const runner = makeRunner({ pkgs, root: appDir, jobs: 4 });
const blocks = fs.readFileSync(mfile, 'utf8').split(/^### /m).slice(1);
const cache = {};
const jobs = blocks.map(async (b) => {
  const nl = b.indexOf('\n'); const [file, loc, n, name] = b.slice(0, nl).trim().split(/\s+/); const src = b.slice(nl + 1);
  const j = cache[file] ||= JSON.parse(fs.readFileSync(path.join(appDir, 'content/courses/ds', file + '.json'), 'utf8'));
  const node = loc[0] === 's' ? j.screens[+loc.slice(1)] : j.items[+loc.slice(1)];
  const spec = node.widget;
  const res = await runner.grade(spec, spec.solution + '\n' + src, 'tests');
  const first = res.rows.findIndex((x) => !x.ok);
  const r = first >= 0 ? res.rows[first] : null;
  return `${file} ${loc} line=test-${n} ${name} -> ${res.key || 'PASS'}${res.key === 'test-' + n ? ' MATCH' : ' MISMATCH'}${r ? ' | ' + String(r.error || r.actual || '').split('\n').pop().slice(0, 90) : ''}${res.timeoutAt != null ? ' [timeout]' : ''}`;
});
const out = await Promise.all(jobs);
console.log(out.join('\n'));
await runner.close();
