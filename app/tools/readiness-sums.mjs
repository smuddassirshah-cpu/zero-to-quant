#!/usr/bin/env node
// Checks docs/readiness.md against the content: course coverage per role, totals, dependency
// conflicts and mocks. Exits non-zero on any mismatch.
//   node app/tools/readiness-sums.mjs          check (default)
//   node app/tools/readiness-sums.mjs --write  regenerate the generated blocks from the classification tables, and app/content/readiness.json
// Check mode also fails when app/content/readiness.json differs from what --write would generate. Never hand-edit the JSON.
// Hours source is the census source: stored topic hours in curriculum.json, shared by a topic's
// courses in proportion to mapped lessons. Written means the lesson file exists on disk.
import { readFileSync, writeFileSync, readdirSync, existsSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';

const { refsOf } = createRequire(import.meta.url)('../js/prereq.js');   // the one requires normaliser (ENGINE-BACKLOG 551): gating strings only, diagnostics never count as edges
const APP = join(dirname(fileURLToPath(import.meta.url)), '..');
const C = join(APP, 'content');
const MD = join(APP, '..', 'docs', 'readiness.md');
const WRITE = process.argv.includes('--write');
const read = (p) => JSON.parse(readFileSync(p, 'utf8'));
const errors = [];
const err = (m) => errors.push(m);

// Roles: key, heading text in the md, prep.json track.
const ROLES = [
  { key: 'trader', heading: 'Trader', track: 'trader' },
  { key: 'researcher', heading: 'Researcher', track: 'research' },
  { key: 'developer', heading: 'Developer', track: 'developer' },
  { key: 'strats', heading: 'Strats', track: 'strats' },
  { key: 'strats-deriv', heading: 'Derivatives and desk quant sub-route', track: 'strats' },
  { key: 'undecided', heading: 'Undecided', track: null },
];
const STATUS = ['required', 'recommended', 'optional'];

// Catalogue.
const cur = read(join(C, 'curriculum.json'));
const topicStage = {}; const topicHours = {};
for (const s of cur.stages) for (const t of s.topics) { topicStage[t.id] = s.id; topicHours[t.id] = t.hours ?? 0; }
const courses = {};
for (const id of readdirSync(join(C, 'courses')).sort()) {
  const p = join(C, 'courses', id, 'course.json');
  if (!existsSync(p)) continue;
  const cj = read(p);
  const c = { id, topic: cj.topic, stage: topicStage[cj.topic], mapped: 0, written: 0, edges: [] };
  for (const lv of cj.levels ?? []) {
    for (const l of lv.lessons ?? []) { c.mapped++; if (existsSync(join(C, 'courses', id, `${l}.json`))) c.written++; }
    for (const r of refsOf(lv.requires)) {
      const [to, tl] = String(r).split('/');
      if (to !== id) c.edges.push({ from: id, level: lv.n, to, toLevel: tl });
    }
  }
  courses[id] = c;
}
const ids = Object.keys(courses);
const topicMapped = {};
for (const c of Object.values(courses)) topicMapped[c.topic] = (topicMapped[c.topic] ?? 0) + c.mapped;
for (const c of Object.values(courses)) c.hours = topicMapped[c.topic] ? topicHours[c.topic] * c.mapped / topicMapped[c.topic] : 0;

// Parse the md.
const lines = readFileSync(MD, 'utf8').split('\n');
const cls = {}; const mocks = {};
for (const r of ROLES) { cls[r.key] = {}; mocks[r.key] = []; }
let role = null; let tableKind = null;
for (const line of lines) {
  const h = line.match(/^#{2,3} (.+?)\s*$/);
  if (h) { const r = ROLES.find((x) => x.heading === h[1]); role = r ? r.key : null; tableKind = null; continue; }
  if (!role) continue;
  if (/^\| Course \| Stage \| Status \|/.test(line)) { tableKind = 'class'; continue; }
  if (/^\| Mock \| Status \|/.test(line)) { tableKind = 'mock'; continue; }
  if (!line.startsWith('|')) { tableKind = null; continue; }
  if (/^\|\s*-/.test(line)) continue;
  const cells = line.split('|').slice(1, -1).map((s) => s.trim());
  if (tableKind === 'class') {
    const id = cells[0].replace(/`/g, '');
    if (!courses[id]) err(`${role}: unknown course ${id}`);
    else if (cls[role][id]) err(`${role}: course ${id} listed twice`);
    else {
      if (String(courses[id].stage) !== cells[1]) err(`${role}: ${id} stage ${cells[1]} should be ${courses[id].stage}`);
      if (!STATUS.includes(cells[2])) err(`${role}: ${id} status "${cells[2]}" invalid`);
      if (!cells[3]) err(`${role}: ${id} has no reason`);
      cls[role][id] = cells[2];
    }
  } else if (tableKind === 'mock') {
    mocks[role].push({ id: cells[0].replace(/`/g, ''), status: cells[1], note: cells[2] ?? '' });
  }
}
for (const r of ROLES) {
  for (const id of ids) if (!cls[r.key][id]) err(`${r.key}: course ${id} missing`);
}

// Totals.
const fmt = (n) => String(Math.round(n));
function sums(role, statuses) {
  let w = 0, u = 0, hw = 0, hu = 0;
  for (const id of ids) {
    if (!statuses.includes(cls[role][id])) continue;
    const c = courses[id]; w += c.written; u += c.mapped - c.written;
    hw += c.mapped ? c.hours * c.written / c.mapped : 0; hu += c.mapped ? c.hours * (c.mapped - c.written) / c.mapped : 0;
  }
  return { w, u, hw: Math.round(hw), hu: Math.round(hu) };
}
function totalsBlock(role) {
  const rq = sums(role, ['required']); const rc = sums(role, ['recommended']);
  const hd = { w: rq.w + rc.w, u: rq.u + rc.u, hw: rq.hw + rc.hw, hu: rq.hu + rc.hu };
  const row = (n, s) => `| ${n} | ${s.w} | ${s.u} | ${s.w + s.u} | ${s.hw} | ${s.hu} | ${s.hw + s.hu} |`;
  return ['| Set | Lessons written | Lessons unwritten | Lessons total | Hours written | Hours unwritten | Hours total |',
    '| --- | --- | --- | --- | --- | --- | --- |', row('Required', rq), row('Recommended', rc), row('Learn header (required plus recommended)', hd)].join('\n');
}

// Dependency conflicts.
const bySrc = {};
for (const c of Object.values(courses)) bySrc[c.id] = c.edges;
function conflictsBlock(role) {
  const st = cls[role]; const out = [];
  const rows = [];
  for (const a of ids.filter((x) => st[x] !== 'optional')) {
    const direct = {};
    for (const e of bySrc[a]) if (st[e.to] === 'optional') (direct[e.to] ??= []).push(`L${e.level} needs ${e.to}/${e.toLevel}`);
    // Indirect: reached only through optional courses.
    const seen = new Set([a, ...Object.keys(direct)]);
    const path = {}; const queue = Object.keys(direct).sort();
    for (const q of queue) path[q] = [q];
    const indirect = [];
    while (queue.length) {
      const x = queue.shift();
      for (const e of [...bySrc[x]].sort((p, q) => p.to.localeCompare(q.to))) {
        if (seen.has(e.to) || st[e.to] !== 'optional') continue;
        seen.add(e.to); path[e.to] = [...path[x], e.to]; indirect.push(e.to); queue.push(e.to);
      }
    }
    for (const b of Object.keys(direct).sort()) rows.push(`| \`${a}\` | \`${b}\` | ${[...new Set(direct[b])].join(', ')} |`);
    for (const b of indirect.sort()) rows.push(`| \`${a}\` | \`${b}\` | via ${path[b].slice(0, -1).map((x) => `\`${x}\``).join(' > ')} |`);
  }
  if (rows.length) out.push('| From (required or recommended) | Optional course reached | Edge or route |', '| --- | --- | --- |', ...rows);
  else out.push('None.');
  const soft = [];
  for (const a of ids.filter((x) => st[x] === 'required')) {
    const t = [...new Set(bySrc[a].filter((e) => st[e.to] === 'recommended').map((e) => e.to))].sort();
    if (t.length) soft.push(`\`${a}\` needs ${t.map((x) => `\`${x}\``).join(', ')}`);
  }
  out.push('', `Required courses that need a recommended course: ${soft.length ? soft.join('; ') : 'none'}.`);
  return out.join('\n');
}

function catalogueBlock() {
  const m = ids.reduce((a, i) => a + courses[i].mapped, 0); const w = ids.reduce((a, i) => a + courses[i].written, 0);
  return `Catalogue: ${ids.length} courses, ${m} lessons mapped (${w} written, ${m - w} unwritten). Hours are stored topic hours shared across a topic's courses by mapped lessons; topics 3.2 and 3.4 store 0.`;
}

// Mocks check.
const prep = read(join(C, 'prep.json'));
for (const r of ROLES) {
  if (!r.track) continue;
  const want = new Set();
  for (const p of prep.paths) if (p.track === r.track && p.kind === 'stage') for (const m of p.mocks ?? []) want.add(m);
  const have = new Set(mocks[r.key].filter((m) => !/^version of/.test(m.note)).map((m) => m.id));
  for (const m of want) if (!have.has(m)) err(`${r.key}: mock ${m} named in prep.json but not listed`);
  for (const m of have) if (!want.has(m)) err(`${r.key}: mock ${m} listed but not in prep.json for track ${r.track}`);
}
for (const r of ROLES) for (const m of mocks[r.key]) {
  const exists = existsSync(join(C, 'exams', `${m.id}.json`));
  if (exists && m.status !== 'exists') err(`${r.key}: ${m.id} exists but is marked "${m.status}"`);
  if (!exists && m.status !== 'gap: not yet written') err(`${r.key}: ${m.id} is missing but is marked "${m.status}"`);
}

// Generated blocks.
const gen = { catalogue: catalogueBlock() };
for (const r of ROLES) { gen[`totals:${r.key}`] = totalsBlock(r.key); gen[`conflicts:${r.key}`] = conflictsBlock(r.key); }
let text = readFileSync(MD, 'utf8');
for (const [name, body] of Object.entries(gen)) {
  const re = new RegExp(`(<!-- generated:${name} -->\\n)([\\s\\S]*?)(\\n<!-- /generated -->)`);
  const m = text.match(re);
  if (!m) { err(`block generated:${name} missing`); continue; }
  if (WRITE) text = text.replace(re, (_, a, __, c) => a + body + c);
  else if (m[2] !== body) err(`block generated:${name} is out of date (run with --write after checking the tables)`);
}
// readiness.json: what the engine reads (js/readiness.js). Per role: course -> status, totals, mocks.
// LIMITED: courses whose route is cut short by unwritten courses (DECISIONS, item 7); the script fails once the gap closes.
const LIMITED = { pdes: { missing: ['odes', 'numerics'] } };
for (const [cid, l] of Object.entries(LIMITED)) {
  if (!courses[cid]) err(`LIMITED: unknown course ${cid}`);
  for (const m of l.missing) if (!courses[m]) err(`LIMITED: unknown course ${m}`); else if (courses[m].written > 0) err(`LIMITED: ${m} now has written lessons; update LIMITED for ${cid}`);
}
const setOf = (s) => ({ written: s.w, unwritten: s.u, total: s.w + s.u, hoursWritten: s.hw, hoursUnwritten: s.hu, hours: s.hw + s.hu });
const json = { generated: 'node app/tools/readiness-sums.mjs --write; do not edit by hand', roles: {}, limited: {} };
for (const r of ROLES) {
  const rq = sums(r.key, ['required']), rc = sums(r.key, ['recommended']);
  const hd = { w: rq.w + rc.w, u: rq.u + rc.u, hw: rq.hw + rc.hw, hu: rq.hu + rc.hu };
  const courseMap = {}; for (const id of ids) courseMap[id] = cls[r.key][id];
  json.roles[r.key] = {
    courses: courseMap, totals: { required: setOf(rq), recommended: setOf(rc), header: setOf(hd) },
    mocks: { present: mocks[r.key].filter((m) => m.status === 'exists').map((m) => m.id), missing: mocks[r.key].filter((m) => m.status !== 'exists').map((m) => m.id) },
  };
}
for (const [cid, l] of Object.entries(LIMITED)) json.limited[cid] = `route limited: ${l.missing.join(', ')} unwritten`;
const JSON_FILE = join(C, 'readiness.json');
const jsonText = JSON.stringify(json, null, 1) + '\n';
if (!WRITE) {
  if (!existsSync(JSON_FILE)) err('content/readiness.json missing (run with --write)');
  else if (readFileSync(JSON_FILE, 'utf8') !== jsonText) err('content/readiness.json is out of date (run with --write)');
}
if (WRITE && !errors.length) { writeFileSync(JSON_FILE, jsonText); writeFileSync(MD, text); console.log('readiness.md blocks rewritten'); }
if (errors.length) { console.error(errors.join('\n')); console.error(`FAIL: ${errors.length} problem(s)`); process.exit(1); }
console.log(`OK: ${ROLES.length} roles, ${ids.length} courses each, totals, conflicts and mocks agree`);
