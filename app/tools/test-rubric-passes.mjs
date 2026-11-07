// Tests for tools/rubric-passes.mjs (ENGINE-BACKLOG 698). Run from app/: node tools/test-rubric-passes.mjs
import fs from 'node:fs';
import { analyse } from './rubric-passes.mjs';
const dir = 'tools/fixtures/rubric-passes/';
const load = (n) => JSON.parse(fs.readFileSync(`${dir}${n}.json`, 'utf8')).rubric;
const cases = {
  // 3,3,2,2: any set of 7+ points; minimal ones are the three-row sets reaching 7 and no subset does
  none: { min: [[1, 2, 3], [1, 2, 4], [1, 3, 4], [2, 3, 4]], out: [true, true, true, true] },
  // 4r,3,2,1: row 1 required, needs 3 more points from rows 2 to 4
  'one-required': { min: [[1, 2], [1, 3, 4]], out: [false, true, true, true] },
  // 3r,2r,2r,1,1,1: required rows give 7 alone
  'three-required': { min: [[1, 2, 3]], out: [false, false, false, true, true, true] },
  'all-required': { min: [[1, 2, 3]], out: [false, false, false] },
  // 5,4,3 totals 12: pairs reaching 7
  'not-ten': { min: [[1, 2], [1, 3], [2, 3]], out: [true, true, true] },
};
let bad = 0;
for (const [name, want] of Object.entries(cases)) {
  const r = analyse(load(name));
  const norm = (a) => JSON.stringify([...a].map((s) => s.join(',')).sort());
  const okMin = norm(r.minimalSets) === norm(want.min);
  const okOut = JSON.stringify(r.rows.map((x) => x.canBeLeftOut)) === JSON.stringify(want.out);
  if (!okMin || !okOut) { bad++; console.log(`FAIL ${name}: got ${JSON.stringify(r.minimalSets)} ${JSON.stringify(r.rows.map((x) => x.canBeLeftOut))}`); }
  else console.log(`ok ${name}`);
}
if (analyse(load('not-ten')).total !== 12) { bad++; console.log('FAIL not-ten total'); }
console.log(bad ? `${bad} failed` : 'all passed');
process.exitCode = bad ? 1 : 0;
