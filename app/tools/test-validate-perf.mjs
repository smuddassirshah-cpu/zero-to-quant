#!/usr/bin/env node
/* Fixture runner for the performance-task rules (ENGINE-BACKLOG 529; tools/perf-rules.mjs, the same functions the validator applies).
   Each tools/fixtures/perf/<case>.json is one scratch level: { course, stage, lessons: [[objective, ...]], pending, items: [...homework/review items], expect: "ok" | "error", has?, warns?, expectOptionalRows? }. expectOptionalRows counts the items the [perf-optional-row] advisory (ENGINE-BACKLOG 702) flags.
   "error" must raise at least one error (containing `has` when given); "ok" must raise none (and a warning containing `warns` when given).
   Run from app/: node tools/test-validate-perf.mjs. One PASS or FAIL line per case, a summary line, exit 1 on a failure. */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { checkTask, checkLevel, matchVerb, optionalRows } from './perf-rules.mjs';

const dir = path.join(path.dirname(fileURLToPath(import.meta.url)), 'fixtures', 'perf');
let pass = 0, fail = 0;
for (const f of fs.readdirSync(dir).filter(x => x.endsWith('.json')).sort()) {
  const fx = JSON.parse(fs.readFileSync(path.join(dir, f), 'utf8')), name = f.replace(/\.json$/, '');
  const tasks = (fx.items || []).filter(it => it && it.performance !== undefined);
  const matched = matchVerb(fx.course, fx.stage, (fx.lessons || []).flat());
  const lv = checkLevel({ key: `${fx.course}/L1`, matched, tasks, pending: !!fx.pending });
  const errors = [...lv.errors, ...tasks.flatMap(t => checkTask(t).map(m => `${t.id}: ${m}`))];
  const problems = [];
  if (fx.expect === 'error') {
    if (!errors.length) problems.push('expected an error, got none');
    else if (fx.has && !errors.some(e => e.includes(fx.has))) problems.push(`no error contains "${fx.has}" (got: ${errors.join(' | ')})`);
  } else {
    if (errors.length) problems.push(`expected no error, got: ${errors.join(' | ')}`);
    if (fx.warns && !lv.warnings.concat(lv.pendingNoTask ? ['pending'] : []).some(w => w.includes(fx.warns))) problems.push(`no warning contains "${fx.warns}"`);
  }
  if (fx.expectOptionalRows !== undefined) { const n = tasks.filter(t => optionalRows(t).length).length; if (n !== fx.expectOptionalRows) problems.push(`expected ${fx.expectOptionalRows} perf-optional-row item(s), got ${n}`); }
  if (problems.length) { console.log(`FAIL ${name}: ${problems.join('; ')}`); fail++; } else { console.log(`PASS ${name}`); pass++; }
}
console.log(`${fail ? 'FAIL' : 'PASS'} summary: ${pass} of ${pass + fail} perf cases passed`);
process.exit(fail ? 1 : 0);
