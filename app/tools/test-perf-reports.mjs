// Tests for tools/perf-reports.mjs (ENGINE-BACKLOG 699). Run from app/: node tools/test-perf-reports.mjs
import fs from 'node:fs';
import { checkAll } from './perf-reports.mjs';
const dir = 'tools/fixtures/perf-reports';
const perf = JSON.parse(fs.readFileSync(`${dir}/perf.json`, 'utf8'));
const { missing, noReport } = checkAll(perf, dir);
const got = missing.map((m) => `${m.report}: missing ${m.part}`).sort();
const want = ['demo-2-perf.md: missing Overlapping screens line', 'demo-3-perf.md: missing item id'];
let bad = 0;
const check = (name, ok) => { if (!ok) bad++; console.log(`${ok ? 'ok' : 'FAIL'} ${name}`); };
check('complete report has nothing missing', !got.some((g) => g.startsWith('demo-1')));
check('missing overlap line found', got.includes(want[0]));
check('missing item id found', got.includes(want[1]));
check('no other parts reported', got.length === 2);
check('missing report listed', noReport.length === 1 && noReport[0] === 'demo-4-perf.md');
console.log(bad ? `${bad} failed` : 'all passed');
process.exitCode = bad ? 1 : 0;
