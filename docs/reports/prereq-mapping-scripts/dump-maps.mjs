// Usage (from repo root): node docs/reports/prereq-mapping-scripts/dump-maps.mjs [--obj]
// Dumps every course map: topic, strand, levels, lesson counts, written counts, current requires.
import fs from 'fs'; import path from 'path';
const root = 'app/content/courses';
const obj = process.argv.includes('--obj');
const rows = [];
for (const c of fs.readdirSync(root)) {
  const f = path.join(root, c, 'course.json'); if (!fs.existsSync(f)) continue;
  const j = JSON.parse(fs.readFileSync(f, 'utf8'));
  const written = new Set(fs.readdirSync(path.join(root, c)).filter(x => x.endsWith('.json')).map(x => x.replace('.json', '')));
  rows.push({ c, j, written });
}
rows.sort((a, b) => parseFloat(a.j.topic) - parseFloat(b.j.topic) || a.c.localeCompare(b.c));
for (const { c, j, written } of rows) {
  console.log(`## ${c} | ${j.name} | topic=${j.topic} strand=${j.strand || '-'}`);
  for (const lv of j.levels || []) {
    const ls = lv.lessons || [];
    console.log(`  L${lv.n} ${lv.name} [${ls.length}, written ${ls.filter(l => written.has(l)).length}] req=${JSON.stringify(lv.requires)}`);
    if (obj) for (const l of ls) {
      let o = ''; try { const lj = JSON.parse(fs.readFileSync(path.join(root, c, l + '.json'), 'utf8')); o = lj.objective || (lj.objectives || []).join('; ') || lj.title || ''; } catch {}
      console.log(`      - ${l}: ${String(o).slice(0, 110)}`);
    }
  }
}
