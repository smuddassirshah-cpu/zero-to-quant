// Usage (from repo root): node docs/reports/prereq-mapping-scripts/gen-report.mjs > /tmp/part.md
// Prints the per-course tables of docs/reports/prereq-mapping.md from mapping.txt and the course maps.
import { parseMapping, loadCourses, topicKey } from './lib.mjs';
const { levels, lessons } = parseMapping('docs/reports/prereq-mapping-scripts/mapping.txt');
const courses = loadCourses();
const order = Object.keys(courses).sort((a, b) => topicKey(courses[a].topic) - topicKey(courses[b].topic));
let stage = null;
for (const c of order) {
  const s = courses[c].topic.split('.')[0];
  if (s !== stage) { stage = s; console.log(`\n## Stage ${s}\n`); }
  console.log(`### ${c} (topic ${courses[c].topic}${courses[c].strand ? ', strand ' + courses[c].strand : ''}): ${courses[c].name}\n`);
  for (const lv of courses[c].levels) {
    const k = `${c} L${lv.n}`; const refs = levels[k];
    if (refs) console.log(`- L${lv.n} ${lv.name}: ` + refs.map(r => `\`${r.ref}\` (${r.why})`).join('; ') + '.');
    else if (lv.n === 1) console.log(`- L${lv.n} ${lv.name}: open (first level, no \`requires\`).`);
    else console.log(`- L${lv.n} ${lv.name}: implicit, \`${c}/L${lv.n - 1}\`.`);
    for (const [lk, lr] of Object.entries(lessons)) if (lk.startsWith(k + ' ')) console.log(`  - override \`${lk.split(' ')[2]}\`: ` + lr.map(r => `\`${r.ref}\` (${r.why})`).join('; ') + '.');
  }
  console.log('');
}
