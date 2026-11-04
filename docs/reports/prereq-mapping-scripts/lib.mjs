// Shared helpers: parse mapping.txt; load course maps.
import fs from 'fs'; import path from 'path';
export function parseMapping(file) {
  const levels = {}, lessons = {};
  for (const raw of fs.readFileSync(file, 'utf8').split('\n')) {
    const line = raw.trim(); if (!line || line.startsWith('#')) continue;
    const [head, rest] = line.split(' | ');
    const parts = head.split(' ');           // course Ln [lesson-id]
    const refs = rest.split('; ').map(s => { const i = s.indexOf(': '); return { ref: s.slice(0, i), why: s.slice(i + 2) }; });
    if (parts.length === 3) lessons[`${parts[0]} ${parts[1]} ${parts[2]}`] = refs;
    else levels[`${parts[0]} ${parts[1]}`] = refs;
  }
  return { levels, lessons };
}
export function loadCourses(root = 'app/content/courses') {
  const out = {};
  for (const c of fs.readdirSync(root)) {
    const f = path.join(root, c, 'course.json'); if (!fs.existsSync(f)) continue;
    out[c] = JSON.parse(fs.readFileSync(f, 'utf8'));
  }
  return out;
}
export const stageOf = topic => Number(String(topic).split('.')[0]);
export const topicKey = topic => { const [a, b] = String(topic).split('.').map(Number); return a * 100 + b; };
