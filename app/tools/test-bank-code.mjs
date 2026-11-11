#!/usr/bin/env node
/* Test for Python `code` items in the interview bank (bank part 2, B2-E1 to B2-E3, B2-E5; ENGINE-BACKLOG 920 to 926).
   Copies app/ to a temp folder, drops tools/fixtures/bank-code/fixture-code.json into its content/bank and checks:
     1. the validator accepts both fixture items (0 errors; language left out is allowed) and refuses a C++ code item, a code item with no solution,
        and a starter equal to the solution; warns [bank-code] on a pace outside 240 to 480 and on a how line whose count is not the test count;
     2. [bank-family]: a first tag that is neither a skill id nor a course item's first tag warns, a real family does not;
     3. playthrough --bank fixture-code (needs Python: pass --local-cdn <pkgs>): the passing item is ok, the one whose starter passes is reported
        ("the untouched starter passes every hidden test"), desktop and --mobile (440 px named in the line);
   Run from app/: node tools/test-bank-code.mjs [--local-cdn <pkgs>] [--no-browser]. Exit 1 on a failure. */
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url)), APP = path.resolve(HERE, '..');
const argv = process.argv.slice(2);
const cdn = argv.includes('--local-cdn') ? argv[argv.indexOf('--local-cdn') + 1] : null;
const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'zq-bankcode-'));
const copy = path.join(tmp, 'app');
fs.cpSync(APP, copy, { recursive: true, filter: (s) => !/[\\/](node_modules|\.git)([\\/]|$)/.test(s) });
const fixture = JSON.parse(fs.readFileSync(path.join(HERE, 'fixtures/bank-code/fixture-code.json'), 'utf8'));
const target = path.join(copy, 'content/bank/fixture-code.json');
const put = (fn) => { const d = JSON.parse(JSON.stringify(fixture)); if (fn) fn(d); fs.writeFileSync(target, JSON.stringify(d, null, 2) + '\n'); };
const validate = () => { const r = spawnSync('node', [path.join(copy, 'tools/validate.mjs')], { cwd: copy, encoding: 'utf8', maxBuffer: 1 << 26 }); return { out: (r.stdout || '') + (r.stderr || ''), code: r.status }; };
let fails = 0;
const say = (ok, name, extra) => { console.log(`${ok ? 'PASS' : 'FAIL'} ${name}${!ok && extra ? '\n' + extra : ''}`); if (!ok) fails++; };
const mine = (out) => out.split('\n').filter((l) => /fixture-code/.test(l));

put();
let v = validate();
say(v.code === 0 && !mine(v.out).some((l) => /^error/.test(l)), 'validator: both fixture items accepted (language left out, 0 errors)', mine(v.out).join('\n'));
say(!mine(v.out).some((l) => /\[bank-code\]|\[bank-family\]/.test(l)), 'validator: no [bank-code] or [bank-family] warning on a well-formed fixture', mine(v.out).join('\n'));

put((d) => { d.items[0].widget.language = 'cpp'; d.items[0].widget.starter = '#include <cstdint>\nint lot_round(int q, int l) { return 0; }\n'; });
v = validate();
say(mine(v.out).some((l) => /^error.*C\+\+ code item cannot run in the bank deck/.test(l)), 'validator: a C++ code item is refused');

put((d) => { d.items[0].widget.language = 'python'; });
v = validate();
say(v.code === 0, 'validator: language "python" is accepted');

put((d) => { delete d.items[0].widget.solution; });
v = validate();
say(mine(v.out).some((l) => /^error.*\[bank-code\].*needs a solution/.test(l)), 'validator: a bank code item with no solution is an error');

put((d) => { d.items[0].widget.starter = d.items[0].widget.solution; });
v = validate();
say(mine(v.out).some((l) => /^error.*\[bank-code\].*starter equals the solution/.test(l)), 'validator: a starter equal to the solution is an error');

put((d) => { d.items[0].pace = 90; d.items[1].widget.how = 'Submit runs 9 hidden tests. Each result must equal the expected whole number.'; });
v = validate();
say(mine(v.out).some((l) => /^warning.*pace.*\[bank-code\]|^warning.*\[bank-code\].*pace/.test(l)) && mine(v.out).some((l) => /^warning.*\[bank-code\] how says 9/.test(l)), 'validator: [bank-code] warns on a pace outside 240 to 480 and on a how count that is not the test count', mine(v.out).join('\n'));

put((d) => { d.items[0].widget.tests = d.items[0].widget.tests.slice(0, 4); d.items[0].widget.how = 'Submit runs 4 hidden tests. Each result must equal the expected whole number.'; });
v = validate();
say(mine(v.out).some((l) => /^warning.*\[bank-code\] 4 hidden tests/.test(l)), 'validator: [bank-code] warns on fewer than six hidden tests');

put((d) => { d.items[0].parts = [{ question: 'Part one.', widget: { kind: 'code', language: 'cpp', starter: '#include <cstdint>\nint f() { return 0; }\n', tests: [], examples: [] }, feedback: { correct: 'ok', generic: 'no' } }, { question: 'Part two.', widget: { kind: 'numeric', answer: 1 }, feedback: { correct: 'ok', generic: 'no' } }]; delete d.items[0].widget; });
v = validate();
say(mine(v.out).some((l) => /^error.*C\+\+ code part cannot run in the bank deck/.test(l)), 'validator: a C++ code part is refused');

/* [bank-family] */
put((d) => { d.items[0].tags = ['pf-functoins']; });
v = validate();
say(mine(v.out).some((l) => /^warning.*\[bank-family\] "pf-functoins"/.test(l)) && v.code === 0, 'validator: [bank-family] warns on a misspelt family and is not an error', mine(v.out).join('\n'));
put((d) => { d.items[0].tags = ['pf-functions']; d.items[1].tags = ['estimation-tests']; });
v = validate();
say(mine(v.out).some((l) => /\[bank-family\] "estimation-tests"/.test(l)) && !mine(v.out).some((l) => /\[bank-family\] "pf-functions"/.test(l)), 'validator: [bank-family] accepts a course skill id and warns on an invented one');
const realTag = (() => {
  const walk = (n) => { if (Array.isArray(n)) { for (const x of n) { const r = walk(x); if (r) return r; } } else if (n && typeof n === 'object') { if (Array.isArray(n.tags) && typeof n.tags[0] === 'string' && n.widget) return n.tags[0]; for (const x of Object.values(n)) { const r = walk(x); if (r) return r; } } return null; };
  const root = path.join(APP, 'content/courses');
  for (const c of fs.readdirSync(root)) for (const f of fs.readdirSync(path.join(root, c)).filter((x) => x.endsWith('.json') && x !== 'course.json')) { const r = walk(JSON.parse(fs.readFileSync(path.join(root, c, f), 'utf8'))); if (r) return r; }
  return null;
})();
if (realTag) {
  put((d) => { d.items[0].tags = [realTag]; });
  v = validate();
  say(!mine(v.out).some((l) => /\[bank-family\]/.test(l)), `validator: [bank-family] accepts "${realTag}", the first tag of a course item`);
}

/* playthrough, in the browser */
if (argv.includes('--no-browser')) console.log('skipped the browser checks (--no-browser)');
else {
  put();
  v = validate();
  for (const mobile of [false, true]) {
    const r = spawnSync('node', [path.join(HERE, 'playthrough.mjs'), '--bank', 'fixture-code', ...(mobile ? ['--mobile'] : []), ...(cdn ? ['--local-cdn', cdn] : [])], { env: { ...process.env, ZQ_APP_DIR: copy }, cwd: copy, encoding: 'utf8', maxBuffer: 1 << 26, timeout: 420000 });
    const out = (r.stdout || '') + (r.stderr || ''), tag = mobile ? 'mobile' : 'desktop';
    const lot = new RegExp('FAIL bank/fixture-code/fixture-lot-round').test(out);
    const caught = /FAIL bank\/fixture-code\/fixture-starter-passes( at 440 px)?: the untouched starter passes every hidden test/.test(out);
    const at440 = !mobile || /FAIL bank\/fixture-code\/fixture-starter-passes at 440 px/.test(out);
    const total = /bank total: 1 of 2 items passed/.test(out) || /bank total: 2 of 4 items passed/.test(out);
    say(!lot && caught && at440 && total && r.status !== 0, `playthrough --bank ${tag}: the good item passes, the starter that passes is caught${mobile ? ' (repeated at 440 px)' : ''}`, out.split('\n').slice(-14).join('\n'));
  }
}
/* --why (ENGINE-BACKLOG 926): each named slip is dealt alone and must show its own line; a slip inside the tolerance is marked right and is reported */
if (!argv.includes('--no-browser')) {
  const base = (id, w, fb) => ({ id, difficulty: 2, skills: ['pf-functions'], tags: ['pf-functions'], role: ['developer'], style: 'coding', source: 'Original (engine fixture)', pace: 60, question: 'Pick or type the answer.', widget: w, feedback: fb, explain: { text: 'Because of the working.' } });
  const slips = { id: 'fixture-slips', name: 'Engine fixture, slips', description: 'Engine fixture for the --why check.', items: [
    base('slip-percent', { kind: 'numeric', answer: 0.0617, tol: { abs: 0.00005 }, unit: '%', accept: '6.17%', label: 'Rate', placeholder: 'a percentage', wrong: [{ id: 'nominal', value: 0.06, tol: { abs: 0.00005 } }] }, { correct: 'Right.', generic: 'Not quite.', byKey: { nominal: 'You used the nominal 6%.' } }),
    base('slip-choice', { kind: 'choice', options: [{ id: 'a', text: 'Five', correct: true }, { id: 'b', text: 'Six', why: 'Six counts the end twice.' }, { id: 'c', text: 'Seven', why: 'Seven adds one for luck.' }] }, { correct: 'Right.', generic: 'Not quite.' }),
    base('slip-inside', { kind: 'numeric', answer: 10, tol: { abs: 1 }, wrong: [{ id: 'near', value: 10.5 }], label: 'Count' }, { correct: 'Right.', generic: 'Not quite.', byKey: { near: 'You were close.' } }) ] };
  fs.writeFileSync(path.join(copy, 'content/bank/fixture-slips.json'), JSON.stringify(slips, null, 2) + '\n');
  fs.rmSync(target, { force: true });
  validate();   // refuses slip-inside (a wrong value inside the tolerance is an error), so the manifest is patched by hand: the item exists to be caught by the playthrough
  const mf = path.join(copy, 'content/manifest.json'), m = JSON.parse(fs.readFileSync(mf, 'utf8'));
  m.files = m.files.filter((f) => f !== 'bank/fixture-code.json'); if (!m.files.includes('bank/fixture-slips.json')) m.files.push('bank/fixture-slips.json');
  fs.writeFileSync(mf, JSON.stringify(m, null, 2) + '\n');
  const r = spawnSync('node', [path.join(HERE, 'playthrough.mjs'), '--bank', 'fixture-slips', '--why'], { env: { ...process.env, ZQ_APP_DIR: copy }, cwd: copy, encoding: 'utf8', maxBuffer: 1 << 26, timeout: 300000 });
  const out = (r.stdout || '') + (r.stderr || '');
  say(!/FAIL bank\/fixture-slips\/slip-percent/.test(out) && !/FAIL bank\/fixture-slips\/slip-choice/.test(out) && /FAIL bank\/fixture-slips\/slip-inside: --why: the slip "near" was marked right/.test(out) && /3 slip lines shown|2 slip lines shown/.test(out), '--bank --why: a per cent slip and a distractor show their own lines, a slip inside the tolerance is reported', out.split('\n').slice(-10).join('\n'));
}
fs.rmSync(tmp, { recursive: true, force: true });
console.log(fails ? `${fails} failed` : 'all passed');
process.exitCode = fails ? 1 : 0;
