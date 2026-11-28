#!/usr/bin/env node
/* Scratch cases for the [source-ban] warning (ENGINE-BACKLOG 1268; docs/AUTHORING.md section 9, strand "ai").
   Copies tools/fixtures/mini-app (lib/validate-harness.mjs). A code lesson is placed in algo-think (untagged) and in ai-sample (strand "ai").
     warning: an ai course's Python code widget with a hidden test whose call or setup names __learner_source__
     none: zq_no(...) or zq_uses(...) in the call; the same text search in an untagged course
   Usage: node tools/test-validate-source-ban.mjs. Exit 0 pass, 1 failure. */
import fs from 'node:fs';
import { openHarness } from './lib/validate-harness.mjs';

const h = openHarness({ name: 'source-ban' });
const srcFile = h.path('content/courses/algo-think/l1-counting-work.json');
const base = JSON.parse(fs.readFileSync(srcFile, 'utf8'));
const aiFile = h.path('content/courses/ai-sample/l1-step-1.json');
let fails = 0;
const say = (ok, name, detail = '') => { console.log(`${ok ? 'PASS' : 'FAIL'} ${name}${ok ? '' : '  ' + detail}`); if (!ok) fails++; };
const run = (extra, { ai = false, where = 'call' } = {}) => {
  h.reset();
  const d = JSON.parse(JSON.stringify(base));
  const w = d.screens[8].widget;
  if (extra) w.tests = [...w.tests, where === 'call' ? { call: extra, expect: 'True' } : { call: 'True', setup: extra, expect: 'True' }];
  if (ai) { d.course = 'ai-sample'; d.id = 'l1-step-1'; d.skills = ['ai-loss']; fs.writeFileSync(aiFile, JSON.stringify(d, null, 2)); }
  else { fs.writeFileSync(srcFile, JSON.stringify(d, null, 2)); fs.rmSync(aiFile, { force: true }); }
  const r = h.validate(['--no-manifest']);
  return r.warnings.filter((l) => /\[source-ban\]/.test(l));
};

let w = run(undefined, { ai: true });
say(w.length === 0, 'ai course, no source search: no warning', w.join(' | '));
w = run("'.encode' not in __learner_source__", { ai: true });
say(w.length === 1, 'ai course, text search in call: one warning', w.join(' | '));
w = run("__learner_source__ = __learner_source__.count('for ')", { ai: true, where: 'setup' });
say(w.length === 1, 'ai course, text search in setup: one warning', w.join(' | '));
w = run("zq_no(attrs=('.encode',))", { ai: true });
say(w.length === 0, 'ai course, zq_no in call: no warning', w.join(' | '));
w = run("zq_uses('bytes') == []", { ai: true });
say(w.length === 0, 'ai course, zq_uses in call: no warning', w.join(' | '));
w = run("'.encode' not in __learner_source__");
say(w.length === 0, 'untagged course, text search: no warning', w.join(' | '));
h.close();
process.exit(fails ? 1 : 0);
