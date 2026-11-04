// Usage (from repo root): node docs/reports/prereq-mapping-scripts/candidates.mjs
// For each brief (docs/briefs/<course>.md) and each "## Level N" section, collect every `course lesson-id`
// citation and map it to the cited course level through course.json. Output: candidate references with counts.
// Candidates are input to a human choice; they are not the mapping.
import fs from 'fs'; import path from 'path';
const root = 'app/content/courses';
const maps = {};
for (const c of fs.readdirSync(root)) {
  const f = path.join(root, c, 'course.json'); if (!fs.existsSync(f)) continue;
  const j = JSON.parse(fs.readFileSync(f, 'utf8'));
  const l2n = {}; for (const lv of j.levels) for (const l of lv.lessons) l2n[l] = lv.n;
  maps[c] = l2n;
}
const courses = new Set(Object.keys(maps));
for (const c of Object.keys(maps).sort()) {
  const f = `docs/briefs/${c}.md`; if (!fs.existsSync(f)) continue;
  const txt = fs.readFileSync(f, 'utf8');
  const parts = txt.split(/^## Level (\d+)/m);
  for (let i = 1; i < parts.length; i += 2) {
    const n = parts[i], body = parts[i + 1];
    const counts = {};
    for (const line of body.split('\n')) {
      if (!/builds on|prerequisite|context for this level|depends/i.test(line) && !/^\|/.test(line)) continue;
      let cur = null;
      for (const m of line.matchAll(/l\d+-[a-z0-9-]+|[a-z][a-z0-9-]+/g)) {
        const t = m[0];
        if (/^l\d+-/.test(t)) { if (cur && maps[cur][t] != null) { const k = `${cur}/L${maps[cur][t]}`; counts[k] = (counts[k] || 0) + 1; } }
        else if (courses.has(t)) cur = t;
      }
    }
    const items = Object.entries(counts).filter(([k]) => k !== `${c}/L${n}`).sort((a, b) => a[0].localeCompare(b[0]));
    console.log(`${c} L${n}: ` + items.map(([k, v]) => `${k}(${v})`).join(' '));
  }
}
