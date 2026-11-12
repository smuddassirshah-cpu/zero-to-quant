#!/usr/bin/env node
/* Guards for tools/lib/validate-harness.mjs and the mini content root tools/fixtures/mini-app (engine pass AC part 2).
     the mini root validates with 0 errors, alone and with the real problem-set and Fluency fixtures beside it
     the files the test-validate-* scratch cases plant into are all there
     --root writes its manifest into the scratch copy and never into app/content/manifest.json
     --root with --no-manifest writes no manifest at all
   Run: node tools/test-validate-harness.mjs. One PASS or FAIL line per check, exit 1 on a failure. */
import fs from 'node:fs';
import path from 'node:path';
import crypto from 'node:crypto';
import { openHarness, MINI, APP } from './lib/validate-harness.mjs';

let fails = 0;
const say = (ok, name, detail = '') => { console.log(`${ok ? 'PASS' : 'FAIL'} ${name}${ok ? '' : '  ' + detail}`); if (!ok) fails++; };
const sha = (f) => crypto.createHash('sha1').update(fs.readFileSync(f)).digest('hex');
const realManifest = path.join(APP, 'content', 'manifest.json');
const before = fs.existsSync(realManifest) ? sha(realManifest) : null;

const h = openHarness({ name: 'harness', fixtures: ['problems', 'fluency'] });
const withFx = h.validate();
say(withFx.code === 0 && /\b0 errors\b/.test(withFx.out), 'mini root with the problem-set and Fluency fixtures: 0 errors', withFx.errors.slice(0, 3).join(' | '));
h.reset();
const bare = h.validate();
say(bare.code === 0 && /\b0 errors\b/.test(bare.out), 'mini root alone: 0 errors', bare.errors.slice(0, 3).join(' | '));
say(bare.warnings.every((l) => /content\//.test(l)), 'report paths read content/... as on the real root');

const planted = [
  'content/courses/algo-think/l1-counting-work.json', 'content/courses/algo-think/l11-sorting-by-hand.json', 'content/courses/first-python/l8-many-values.json',
  'content/courses/equations/problems-3.json', 'content/courses/equations/fluency-l3-opening-brackets.json', 'content/courses/odes/review-1.json',
  'content/exams/topic-0.7.json', 'content/exams/mock-oa-strats.json', 'content/exams/mock-oa-sig-2.json', 'content/exams/mock-oa-trader-3.json',
  'content/prep.json', 'content/drills/index.json', 'content/manifest.json',
];
const missing = planted.filter((f) => f !== 'content/manifest.json' && !fs.existsSync(path.join(MINI, f)));
say(!missing.length, 'the files the scratch cases plant into exist in the mini root', missing.join(', '));

const scratchManifest = h.path('content/manifest.json');
say(!fs.existsSync(scratchManifest), 'a --no-manifest run writes no manifest into the scratch copy');
const w = h.validate([]);
say(w.code === 0 && fs.existsSync(scratchManifest), 'a run without --no-manifest writes the manifest into the scratch copy', w.out.slice(-200));
say(before === (fs.existsSync(realManifest) ? sha(realManifest) : null), 'app/content/manifest.json is untouched');
h.close();
console.log(fails ? `${fails} failed` : 'all passed');
process.exit(fails ? 1 : 0);
