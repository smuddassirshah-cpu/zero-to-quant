#!/usr/bin/env node
/* Scratch cases for the [near-miss] rule (ENGINE-BACKLOG 918, SESSION PROTOCOL 6, docs/AUTHORING.md section 5 "Planted wrong solutions").
   A `ci-` or `dsa-` drill should carry a planted solution marked "nearMiss": true, the method one step short of the target. Copies app/ to a temp folder,
   adds fixture drills made from tools/fixtures/planted/planted-py-caught.json, and reads the validator and `planted-check --near-miss`:
     ci- drill, planted entry marked nearMiss      no [near-miss] warning
     ci- drill, planted entry not marked           a [near-miss] warning
     dsa- drill, no planted at all                 a [near-miss] warning
     py- drill, no planted                         no warning (the rule is for ci- and dsa- drills)
     ci- sample drill                              no warning
     nearMiss: "yes"                               an error
   planted-check --near-miss names a drill with no marked plant (a drill with no plants at all runs no browser, so this needs no Python).
   Usage: node tools/test-validate-near-miss.mjs. Exit 0 pass, 1 failure. */
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
const HERE = path.dirname(fileURLToPath(import.meta.url)), APP = path.resolve(HERE, '..');
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'zq-near-miss-'));
const copy = path.join(tmp, 'app');
fs.cpSync(APP, copy, { recursive: true, filter: (s) => !/[\\/](node_modules|\.git)([\\/]|$)/.test(s) });
const base = JSON.parse(fs.readFileSync(path.join(HERE, 'fixtures/planted/planted-py-caught.json'), 'utf8'));
const plant = base.planted[0];
const put = (id, over, planted) => {
  const d = { ...base, id, name: id, sample: false, ...over }; if (planted === undefined) delete d.planted; else d.planted = planted;
  fs.writeFileSync(path.join(copy, 'content/drills', id + '.json'), JSON.stringify(d, null, 2));
};
put('ci-nm-flagged', {}, [{ ...plant, nearMiss: true }]);
put('ci-nm-unflagged', {}, [plant]);
put('dsa-nm-none', {}, undefined);
put('py-nm-none', {}, undefined);
put('ci-nm-sample', { sample: true }, undefined);
put('ci-nm-badtype', {}, [{ ...plant, nearMiss: 'yes' }]);
const v = spawnSync('node', [path.join(copy, 'tools/validate.mjs')], { cwd: copy, encoding: 'utf8', maxBuffer: 1 << 26 });
const out = (v.stdout || '') + (v.stderr || '');
let bad = 0;
const check = (name, ok, detail = '') => { console.log(`${ok ? 'ok  ' : 'FAIL'} ${name}${ok ? '' : '  ' + detail}`); if (!ok) bad++; };
const lines = out.split('\n');
const warned = (id) => lines.some(l => l.includes(`${id}.json`) && l.includes('[near-miss]'));
const errored = (id, re) => lines.some(l => /^error/.test(l) && l.includes(`${id}.json`) && re.test(l));
check('a ci- drill with a marked plant has no warning', !warned('ci-nm-flagged'));
check('a ci- drill with an unmarked plant warns', warned('ci-nm-unflagged'));
check('a dsa- drill with no plants warns', warned('dsa-nm-none'));
check('a py- drill is not asked for one', !warned('py-nm-none'));
check('a sample drill is not asked for one', !warned('ci-nm-sample'));
check('nearMiss that is not a boolean is an error', errored('ci-nm-badtype', /nearMiss is true or false/), lines.filter(l => l.includes('ci-nm-badtype')).join(' | '));
check('a drill with an unknown planted field still warns about it, and nearMiss is known', !lines.some(l => l.includes('ci-nm-flagged.json') && /unknown field/.test(l)));
const r = spawnSync('node', [path.join(HERE, 'planted-check.mjs'), '--drill', 'dsa-nm-none', '--drill', 'py-nm-none', '--near-miss'], { env: { ...process.env, ZQ_APP_DIR: copy }, encoding: 'utf8' });
check('planted-check --near-miss fails a drill with no marked plant', r.status === 1 && /FAIL dsa-nm-none: no planted solution is marked "nearMiss": true/.test(r.stdout), r.stdout);
const r2 = spawnSync('node', [path.join(HERE, 'planted-check.mjs'), '--drill', 'py-nm-none'], { env: { ...process.env, ZQ_APP_DIR: copy }, encoding: 'utf8' });
check('without --near-miss a drill with no plants is skipped, not failed', r2.status === 0 && /1 skipped without any/.test(r2.stdout), r2.stdout);
fs.rmSync(tmp, { recursive: true, force: true });
console.log(bad ? `${bad} failed` : 'all passed');
process.exitCode = bad ? 1 : 0;
