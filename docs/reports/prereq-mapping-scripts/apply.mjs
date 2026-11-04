// Usage (from repo root): node docs/reports/prereq-mapping-scripts/apply.mjs
// Reads mapping.txt and inserts "requires" (per level) and "lessonRequires" (top level) into each
// app/content/courses/<course>/course.json by text insertion, so no other byte of the file changes.
import fs from 'fs'; import path from 'path';
import { parseMapping } from './lib.mjs';
const root = 'app/content/courses';
const { levels, lessons } = parseMapping('docs/reports/prereq-mapping-scripts/mapping.txt');
const byCourse = {};
for (const [k, refs] of Object.entries(levels)) { const [c, n] = k.split(' L'); (byCourse[c] ||= { levels: {}, lessons: {} }).levels[n] = refs; }
for (const [k, refs] of Object.entries(lessons)) { const [c, n, id] = k.split(/ L| /); (byCourse[c] ||= { levels: {}, lessons: {} }).lessons[id] = refs; }
const fmt = refs => '[' + refs.map(r => JSON.stringify(r.ref)).join(', ') + ']';
for (const [c, m] of Object.entries(byCourse)) {
  const f = path.join(root, c, 'course.json');
  let txt = fs.readFileSync(f, 'utf8');
  const j = JSON.parse(txt);
  for (const [n, refs] of Object.entries(m.levels)) {
    const lv = j.levels.find(l => String(l.n) === n);
    if (!lv) throw new Error(`${c} L${n} not on the map`);
    const re = new RegExp(`("homework": "${lv.homework}")(\\r?\\n)(\\s*)\\}`);
    if (!re.test(txt)) throw new Error(`${c} L${n}: homework anchor not found`);
    txt = txt.replace(re, (_, a, nl, ind) => `${a},${nl}${ind}  "requires": ${fmt(refs)}${nl}${ind}}`);
  }
  if (Object.keys(m.lessons).length) {
    const body = Object.entries(m.lessons).map(([id, refs]) => `    ${JSON.stringify(id)}: ${fmt(refs)}`).join(',\n');
    if (!txt.includes('\n  "levels": [')) throw new Error(`${c}: levels anchor`);
    txt = txt.replace('\n  "levels": [', `\n  "lessonRequires": {\n${body}\n  },\n  "levels": [`);
  }
  fs.writeFileSync(f, txt);
}
console.log('edited', Object.keys(byCourse).length, 'courses');
