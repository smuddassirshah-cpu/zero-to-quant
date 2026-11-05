// PLAN 2c item 8, user decision (DECISIONS "Capstones and route scope"): the trader lever from
// docs/reports/closure-item7.md. Two graphs-dp edges become diagnostics (gate: false). Idempotent.
import fs from 'node:fs';
const edges = [['game-theory', 'graphs-dp/L4'], ['brainteasers', 'graphs-dp/L3']];
let changed = 0;
for (const [course, ref] of edges) {
  const f = new URL(`../content/courses/${course}/course.json`, import.meta.url);
  const src = fs.readFileSync(f, 'utf8');
  const re = new RegExp(`(\\{ "ref": "${ref.replace('/', '\\/')}", "why": "[^"]*")( \\})`);
  if (!re.test(src)) { console.log(`${course} ${ref}: already diagnostic or absent`); continue; }
  fs.writeFileSync(f, src.replace(re, '$1, "gate": false$2'));
  changed++; console.log(`${course} ${ref}: gate false`);
}
console.log(`changed ${changed}`);
