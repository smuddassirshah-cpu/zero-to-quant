// The inputs of js/hours.js (ZQ.hours.build) read from a content folder, for the node tools (readiness-sums, census, curriculum-hours).
//   import { loadHours } from './hours-source.mjs';  const { H, cur, courses } = loadHours(contentDir);
// "Written" means the lesson file exists; sessions and minutes come from the lesson files themselves.
import { readFileSync, readdirSync, existsSync } from 'node:fs';
import { join } from 'node:path';
import { createRequire } from 'node:module';

const hours = createRequire(import.meta.url)('../js/hours.js');

export function loadHours(C) {
  const read = (p) => JSON.parse(readFileSync(p, 'utf8'));
  const cur = read(join(C, 'curriculum.json'));
  const courses = {}, sessions = {}, mins = {};
  for (const id of readdirSync(join(C, 'courses')).sort()) {
    const p = join(C, 'courses', id, 'course.json');
    if (!existsSync(p)) continue;
    courses[id] = read(p);
    for (const lv of courses[id].levels ?? []) for (const l of lv.lessons ?? []) {
      const lf = join(C, 'courses', id, `${l}.json`);
      if (!existsSync(lf)) continue;
      const L = read(lf);
      mins[`${id}/${l}`] = L.minutes;
      if (L.session === 'workshop' || L.session === 'project') sessions[`${id}/${l}`] = { session: L.session, minutes: L.minutes };
    }
  }
  const written = (cid, l) => `${cid}/${l}` in mins;
  const H = hours.build({ curriculum: cur, courses, written, sessions, minutes: (cid, l) => mins[`${cid}/${l}`] });
  return { H, cur, courses, sessions, hours };
}
