/* Fixture runner for the O2 validator rules (ENGINE-BACKLOG 523 to 527).
   Each fixtures/o2/<code>.json holds { bad, ok }: bad must raise the code, ok must raise no O2 warning at all.
   Run from app/: node tools/test-validate-o2.mjs */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { scanO2, O2_CODES } from './o2-rules.mjs';

const dir = path.join(path.dirname(fileURLToPath(import.meta.url)), 'fixtures', 'o2');
const run = (json) => { const out = []; scanO2(json, (code, where, msg) => out.push({ code, where, msg })); return out; };
let pass = 0, fail = 0;
for (const code of O2_CODES) {
  const file = path.join(dir, `${code}.json`);
  if (!fs.existsSync(file)) { console.log(`FAIL ${code}: no fixture`); fail++; continue; }
  const fx = JSON.parse(fs.readFileSync(file, 'utf8'));
  const bad = run(fx.bad), ok = run(fx.ok);
  const problems = [];
  if (!bad.some(h => h.code === code)) problems.push('bad fixture did not raise it');
  if (ok.length) problems.push(`ok fixture raised ${ok.map(h => h.code).join(', ')}`);
  if (problems.length) { console.log(`FAIL ${code}: ${problems.join('; ')}`); fail++; } else { console.log(`PASS ${code}`); pass++; }
}
/* ENGINE-BACKLOG 615: O2-unshuffled-numeric is retired; ordered numeric options with shuffle: false, absent or true raise no O2 code */
const retired = path.join(dir, 'O2-unshuffled-numeric.json');
if (fs.existsSync(retired)) {
  const fx = JSON.parse(fs.readFileSync(retired, 'utf8'));
  const raised = [...run(fx.bad), ...run(fx.ok)].filter(h => h.code === 'O2-unshuffled-numeric');
  if (raised.length) { console.log('FAIL O2-unshuffled-numeric still raised (retired)'); fail++; } else { console.log('PASS O2-unshuffled-numeric retired: ordered numeric options raise nothing'); pass++; }
}
console.log(`O2 rules: ${pass} passed, ${fail} failed`);
process.exit(fail ? 1 : 0);
