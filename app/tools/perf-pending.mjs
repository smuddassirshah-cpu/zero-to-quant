#!/usr/bin/env node
/* The grandfather list for performance tasks (ENGINE-BACKLOG 529, docs/AUTHORING.md section 5): the rule-matched levels that have no task.
   node tools/perf-pending.mjs            report: matched, with a task, pending (and the by-stage split); writes nothing
   node tools/perf-pending.mjs --write    regenerate tools/perf-pending.json from the content as it is now (matched levels with no task)
   node tools/perf-pending.mjs --prune    drop the levels that now carry a task (never adds a level)
   Run from app/. Content agents never run --write; the main session prunes. */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { matchVerb } from './perf-rules.mjs';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const CONTENT = path.join(HERE, '..', 'content');
const FILE = path.join(HERE, 'perf-pending.json');
const rd = (p) => { try { return JSON.parse(fs.readFileSync(p, 'utf8')); } catch { return null; } };

export const scan = () => {
  const cur = rd(path.join(CONTENT, 'curriculum.json')) || { stages: [] };
  const stageOf = {};
  (cur.stages || []).forEach(st => (st.topics || []).forEach(t => (t.courses || []).forEach(c => { stageOf[c] = st.id; })));
  const rows = [];
  Object.keys(stageOf).sort().forEach(cid => {
    const dir = path.join(CONTENT, 'courses', cid), co = rd(path.join(dir, 'course.json'));
    if (!co) return;
    (co.levels || []).forEach((lv, i) => {
      const objs = []; let all = (lv.lessons || []).length > 0;
      (lv.lessons || []).forEach(l => { const d = rd(path.join(dir, `${l}.json`)); if (!d) { all = false; return; } objs.push(...(d.objectives || []).filter(o => typeof o === 'string')); });
      const rev = rd(path.join(dir, `${lv.review || 'review-' + (i + 1)}.json`)), hw = rd(path.join(dir, `${lv.homework || 'homework-' + (i + 1)}.json`));
      const tasks = [rev, hw].flatMap(d => (d && Array.isArray(d.items) ? d.items.filter(it => it && it.performance !== undefined) : []));
      const matched = all && rev && hw ? matchVerb(cid, stageOf[cid], objs) : null;
      rows.push({ key: `${cid}/L${lv.n || i + 1}`, cid, stage: stageOf[cid], written: !!(all && rev && hw), matched, hasTask: tasks.length > 0 });
    });
  });
  return rows;
};

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const args = new Set(process.argv.slice(2));
  const rows = scan();
  const matched = rows.filter(r => r.matched), pending = matched.filter(r => !r.hasTask);
  const byStage = {}; matched.forEach(r => { byStage[r.stage] = (byStage[r.stage] || 0) + 1; });
  console.log(`written levels ${rows.filter(r => r.written).length}; rule-matched ${matched.length} (${Object.keys(byStage).sort().map(k => `Stage ${k}: ${byStage[k]}`).join(', ')}); with a task ${matched.length - pending.length}; without ${pending.length}`);
  const old = (rd(FILE) || {}).levels || [];
  const note = 'Grandfathered levels: the verb rule matches them and they have no performance task yet (ENGINE-BACKLOG 529). Never edit by hand and never add a level. node tools/perf-pending.mjs --prune drops levels that gained a task; --write regenerates.';
  if (args.has('--write')) { fs.writeFileSync(FILE, JSON.stringify({ note, levels: pending.map(r => r.key).sort() }, null, 2) + '\n'); console.log(`wrote tools/perf-pending.json (${pending.length} levels)`); }
  else if (args.has('--prune')) {
    const has = new Set(rows.filter(r => r.hasTask).map(r => r.key)), keep = old.filter(k => !has.has(k));
    fs.writeFileSync(FILE, JSON.stringify({ note, levels: keep }, null, 2) + '\n'); console.log(`pruned ${old.length - keep.length}, kept ${keep.length}`);
  } else console.log(`perf-pending.json lists ${old.length}`);
}
