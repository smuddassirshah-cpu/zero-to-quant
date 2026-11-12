#!/usr/bin/env node
/* Fails unless every app/tools/test-* file (.mjs, .py, .sh) is named in exactly one job of .github/workflows/acceptance.yml (docs/CI.md).
   A new test file that no job runs, or one that two jobs run, is an error: add it to the job whose command list fits (static: no browser;
   tests-browser: Chromium or Pyodide; validate-tests: the test-validate-* files). A file may appear on several lines of its job (desktop and --mobile).
     node tools/ci-coverage.mjs [--workflow <path>]     Exit 0 covered, 1 a file missing or in two jobs or named but absent, 2 setup. */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const argv = process.argv.slice(2);
const wi = argv.indexOf('--workflow');
const WF = wi >= 0 ? path.resolve(argv[wi + 1]) : path.resolve(HERE, '..', '..', '.github', 'workflows', 'acceptance.yml');
if (!fs.existsSync(WF)) { console.error(`ci-coverage: ${WF} does not exist`); process.exit(2); }

const files = fs.readdirSync(HERE).filter((f) => /^test-.*\.(mjs|py|sh)$/.test(f)).sort();
const lines = fs.readFileSync(WF, 'utf8').split('\n');
/* the jobs: a key at two-space indent under the top-level `jobs:`; commented lines do not count */
const jobs = {}; let inJobs = false, cur = null;
for (const raw of lines) {
  if (/^jobs:\s*$/.test(raw)) { inJobs = true; continue; }
  if (/^\S/.test(raw) && !/^#/.test(raw)) inJobs = false;
  if (!inJobs) continue;
  const m = /^ {2}([A-Za-z0-9_-]+):\s*$/.exec(raw);
  if (m) { cur = m[1]; jobs[cur] = new Set(); continue; }
  if (!cur || /^\s*#/.test(raw)) continue;
  for (const t of raw.matchAll(/\btest-[A-Za-z0-9_-]+\.(?:mjs|py|sh)\b/g)) jobs[cur].add(t[0]);
}
const where = {}; Object.entries(jobs).forEach(([j, set]) => set.forEach((f) => { (where[f] = where[f] || []).push(j); }));
let bad = 0;
for (const f of files) {
  const w = where[f] || [];
  if (w.length === 0) { console.log(`MISSING   tools/${f} is run by no job of ${path.basename(WF)}`); bad++; }
  else if (w.length > 1) { console.log(`DUPLICATE tools/${f} is run by ${w.length} jobs: ${w.join(', ')}`); bad++; }
}
for (const f of Object.keys(where)) if (!files.includes(f)) { console.log(`ABSENT    ${f} is named in job ${where[f].join(', ')} but is not in tools/`); bad++; }
const per = Object.entries(jobs).filter(([, s]) => s.size).map(([j, s]) => `${j} ${s.size}`).join(', ');
console.log(`ci-coverage: ${files.length} test files, ${bad} problem${bad === 1 ? '' : 's'} (${per})`);
process.exit(bad ? 1 : 0);
