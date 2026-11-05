// PLAN 2c item 8 step 2: write an empty capstone record per role into content/capstones.json.
// Keeps any record already present (the reviewer fills them by hand); adds only missing roles. Idempotent.
import fs from 'node:fs';
const f = new URL('../content/capstones.json', import.meta.url);
const roles = ['trader', 'researcher', 'developer', 'strats', 'strats-deriv'];
const have = fs.existsSync(f) ? JSON.parse(fs.readFileSync(f, 'utf8')) : [];
const byRole = new Map(have.map(r => [r.role, r]));
let added = 0;
const out = roles.map(role => byRole.get(role) || (added++, {
  role, project: role === 'researcher' ? 'momentum-rep' : '', repo: '', reviewer: '', date: '', rerun: '', defence: '', external: false,
}));
fs.writeFileSync(f, JSON.stringify(out, null, 2) + '\n');
console.log(`records ${out.length}, added ${added}`);
