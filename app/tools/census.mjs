#!/usr/bin/env node
// Census of the app's content, from source files only. Read-only: writes nothing.
// Run from anywhere: node app/tools/census.mjs [--courses] [--exams] [--json]
// The last 20 lines are the summary that state files quote (PLAN, PROGRESS, KNOWN_ISSUES).
import { readFileSync, readdirSync, existsSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';

const APP = join(dirname(fileURLToPath(import.meta.url)), '..');
const C = join(APP, 'content');
const args = new Set(process.argv.slice(2));
const read = (p) => JSON.parse(readFileSync(p, 'utf8'));
const jsonFiles = (d) => (existsSync(d) ? readdirSync(d).filter((f) => f.endsWith('.json')).sort() : []);

const { entriesOf } = createRequire(import.meta.url)('../js/prereq.js');
const HOURS = createRequire(import.meta.url)('../js/hours.js');   // the one workload function (PLAN 2c item 11): a stage's hours are the sum of its topics', stored stage field ignored   // the one requires normaliser (ENGINE-BACKLOG 551)
const cur = read(join(C, 'curriculum.json'));
const topicStage = {};
const topicHours = {};
for (const s of cur.stages) for (const t of s.topics) { topicStage[t.id] = s.id; topicHours[t.id] = t.hours ?? 0; }

// Courses: mapped lessons from course.json levels, authored = lesson file on disk.
const courses = [];
for (const id of readdirSync(join(C, 'courses')).sort()) {
  const p = join(C, 'courses', id, 'course.json');
  if (!existsSync(p)) continue;
  const cj = read(p);
  const topic = cj.topic ?? cur.courses?.[id]?.topic ?? '?';
  const row = { id, topic, stage: topicStage[topic] ?? '?', strand: cj.strand ?? 'core', levels: 0, levelsWritten: 0,
    mapped: 0, authored: 0, reviewsMapped: 0, reviews: 0, homeworkMapped: 0, homework: 0, reviewItems: 0, reviewPassSet: 0, cross: 0, noWhy: 0 };
  for (const lv of cj.levels ?? []) {
    row.levels++;
    let w = 0;
    const ents = entriesOf(lv.requires).concat((lv.lessons ?? []).flatMap((l) => entriesOf((cj.lessonRequires ?? {})[l])));
    for (const e of ents) if (e.ref.split('/')[0] !== id) { row.cross++; if (!e.why) row.noWhy++; }
    for (const l of lv.lessons ?? []) { row.mapped++; if (existsSync(join(C, 'courses', id, `${l}.json`))) { row.authored++; w++; } }
    if (w === (lv.lessons ?? []).length && w > 0) row.levelsWritten++;
    if (lv.review) { row.reviewsMapped++; const rp = join(C, 'courses', id, `${lv.review}.json`);
      if (existsSync(rp)) { row.reviews++; const r = read(rp); row.reviewItems += (r.items ?? []).length; if (r.pass != null) row.reviewPassSet++; } }
    if (lv.homework) { row.homeworkMapped++; if (existsSync(join(C, 'courses', id, `${lv.homework}.json`))) row.homework++; }
  }
  courses.push(row);
}

// Exams: kind, item count (fixed items plus drawn items), pass mark per part.
const exams = [];
for (const f of jsonFiles(join(C, 'exams'))) {
  const e = read(join(C, 'exams', f));
  const id = f.replace(/\.json$/, '');
  const kind = id.startsWith('mock-') ? 'mock' : id.startsWith('stage-') ? 'stage' : id.startsWith('topic-') ? 'topic' : 'other';
  const drawn = (ds) => (ds ?? []).reduce((a, d) => a + (d.count ?? d.n ?? 1), 0);
  let items = (e.items ?? []).length + drawn(e.draw);
  const passes = [];
  if (e.pass != null) passes.push(e.pass);
  for (const p of e.parts ?? []) {
    if (p.kind === 'check') continue;
    items += (p.items ?? []).length + drawn(p.draw);
    if (p.pass != null) passes.push(p.pass);
    else if (p.passNet != null) passes.push(`net ${p.passNet}`);
  }
  exams.push({ id, kind, sample: !!e.sample, items, pass: passes.join('/') || 'default', minutes: e.minutes ?? (e.parts ?? []).reduce((a, p) => a + (p.minutes ?? 0), 0) });
}

// Drills and bank.
const drills = jsonFiles(join(C, 'drills')).filter((f) => f !== 'index.json').map((f) => ({ f, d: read(join(C, 'drills', f)) }));
const drillReal = drills.filter((x) => !x.d.sample);
const drillPack = {};
for (const { f, d } of drillReal) { const k = d.pack ?? (f.match(/^(ci|rq|sy|oa)-/)?.[1]) ?? 'untagged'; drillPack[k] = (drillPack[k] ?? 0) + 1; }
const bank = jsonFiles(join(C, 'bank')).map((f) => ({ f, b: read(join(C, 'bank', f)) }));
const bankReal = bank.filter((x) => !x.b.sample && !x.f.startsWith('sample'));
const bankItems = bankReal.reduce((a, x) => a + (x.b.items ?? []).length, 0);

// Generated fluency sets (ENGINE-BACKLOG 817): content/courses/<course>/fluency-<lesson>.json, samples left out.
let fluencySets = 0, fluencyFamilies = 0, fluencySamples = 0;
for (const c of courses) for (const f of jsonFiles(join(C, 'courses', c.id)).filter((x) => /^fluency-.+\.json$/.test(x))) {
  const d = read(join(C, 'courses', c.id, f));
  if (d.sample) { fluencySamples++; continue; }
  fluencySets++; fluencyFamilies += (d.families ?? []).length;
}

// Level problem sets (ENGINE-BACKLOG 845 to 851): content/courses/<course>/problems-<n>.json, samples left out.
let problemSets = 0, problemItems = 0;
for (const c of courses) for (const f of jsonFiles(join(C, 'courses', c.id)).filter((x) => /^problems-\d+\.json$/.test(x))) {
  const d = read(join(C, 'courses', c.id, f));
  if (d.sample) continue;
  problemSets++; problemItems += (d.items ?? []).length;
}

// Prep paths: mock ids referenced with no file.
let prepPaths = 0; const prepMissing = new Set();
if (existsSync(join(C, 'prep.json'))) {
  const prep = read(join(C, 'prep.json'));
  const paths = prep.paths ?? prep;
  prepPaths = Array.isArray(paths) ? paths.length : Object.keys(paths).length;
  const txt = JSON.stringify(prep);
  for (const m of txt.matchAll(/"(mock-[a-z0-9-]+)"/g)) if (!existsSync(join(C, 'exams', `${m[1]}.json`))) prepMissing.add(m[1]);
}

if (args.has('--json')) { console.log(JSON.stringify({ courses, exams, drillPack, bankFiles: bankReal.length, bankItems, prepPaths, prepMissing: [...prepMissing] }, null, 1)); process.exit(0); }

const pad = (s, n) => String(s).padEnd(n);
const lpad = (s, n) => String(s).padStart(n);
if (args.has('--courses') || args.size === 0) {
  console.log('Courses: course, stage, topic, strand, lessons authored/mapped, levels written/mapped, reviews, homework');
  for (const r of courses) console.log(`  ${pad(r.id, 16)} S${r.stage} ${pad(r.topic, 5)} ${pad(r.strand, 5)} ${lpad(r.authored, 3)}/${pad(r.mapped, 3)} L ${r.levelsWritten}/${r.levels}  rev ${r.reviews}/${r.reviewsMapped}  hw ${r.homework}/${r.homeworkMapped}`);
}
if (args.has('--exams') || args.size === 0) {
  console.log('Exams: id, kind, items (fixed + drawn), pass mark(s), minutes');
  for (const e of exams) console.log(`  ${pad(e.id, 26)} ${pad(e.kind + (e.sample ? ' sample' : ''), 12)} ${lpad(e.items, 3)} items  pass ${pad(e.pass, 18)} ${e.minutes} min`);
}

// Summary: the last 20 lines.
const sum = (rows, k) => rows.reduce((a, r) => a + r[k], 0);
const out = [];
out.push('== Census summary (from source) ==');
for (const s of cur.stages) {
  const rows = courses.filter((r) => String(r.stage) === String(s.id));
  const summed = s.topics.reduce((a, t) => a + (t.hours ?? 0), 0);
  out.push(`Stage ${s.id}: lessons ${sum(rows, 'authored')}/${sum(rows, 'mapped')} (missing ${sum(rows, 'mapped') - sum(rows, 'authored')}), courses ${rows.length}, hours stored ${HOURS.stageHours(s)} summed ${summed}`);
}
const real = exams.filter((e) => !e.sample);
const storedH = HOURS.totalHours(cur);   // derived: what the Learn header and stage cards show
const legacy = cur.stages.filter((s) => s.hours != null);
const summedH = Object.values(topicHours).reduce((a, h) => a + h, 0);
out.push(`Total lessons ${sum(courses, 'authored')}/${sum(courses, 'mapped')} (missing ${sum(courses, 'mapped') - sum(courses, 'authored')}); course maps ${courses.length}; courses with 0 lessons ${courses.filter((r) => r.authored === 0).length}`);
out.push(`Levels fully written ${sum(courses, 'levelsWritten')}/${sum(courses, 'levels')}; cross-course requires edges ${sum(courses, 'cross')}, without why ${sum(courses, 'noWhy')}`);
out.push(`Reviews ${sum(courses, 'reviews')}/${sum(courses, 'reviewsMapped')} (items ${sum(courses, 'reviewItems')}, with own pass ${sum(courses, 'reviewPassSet')}); homework ${sum(courses, 'homework')}/${sum(courses, 'homeworkMapped')}`);
out.push(`Exams (non-sample) ${real.length}: topic ${real.filter((e) => e.kind === 'topic').length}, stage ${real.filter((e) => e.kind === 'stage').length}, mock ${real.filter((e) => e.kind === 'mock').length} (mock versions included); samples ${exams.length - real.length}`);
out.push(`Topic exams: ${real.filter((e) => e.kind === 'topic').map((e) => e.id.replace('topic-', '')).join(', ')}`);
out.push(`Topics with no topic exam: ${Object.keys(topicStage).filter((t) => !existsSync(join(C, 'exams', `topic-${t}.json`))).join(', ')}`);
out.push(`Stage exams: ${real.filter((e) => e.kind === 'stage').map((e) => e.id).join(', ') || 'none'}`);
out.push(`Topic exam pass marks: ${[...new Set(real.filter((e) => e.kind === 'topic').map((e) => e.pass))].join(', ')}; items ${Math.min(...real.filter((e) => e.kind === 'topic').map((e) => e.items))} to ${Math.max(...real.filter((e) => e.kind === 'topic').map((e) => e.items))}`);
out.push(`Drills (non-sample) ${drillReal.length}: ${Object.entries(drillPack).map(([k, v]) => `${k} ${v}`).join(', ')}; samples ${drills.length - drillReal.length}`);
out.push(`Bank: ${bankReal.length} files, ${bankItems} items; sample files ${bank.length - bankReal.length}`);
out.push(`Fluency sets ${fluencySets} (families ${fluencyFamilies})${fluencySamples ? `; sample sets ${fluencySamples}` : ''}`);
out.push(`Problem sets ${problemSets} (items ${problemItems})`);
out.push(`Prep paths ${prepPaths}; mock ids named in prep.json with no file: ${prepMissing.size} (${[...prepMissing].join(', ')})`);
out.push(legacy.length ? `Legacy stage hours field present on ${legacy.length} stage(s), total ${legacy.reduce((a, s) => a + s.hours, 0)}, ignored by the engine (run tools/apply-item11-content.mjs)` : 'Legacy stage hours field: absent (stage hours are derived from topics)');
out.push(`Hours: stored stage total ${storedH}, summed topic total ${summedH}, gap ${summedH - storedH}`);
console.log(out.join('\n'));
