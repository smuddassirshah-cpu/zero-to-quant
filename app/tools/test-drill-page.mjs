#!/usr/bin/env node
/* Tests for the drill page limits (ENGINE-BACKLOG 861 to 865). Run from app/: node tools/test-drill-page.mjs [--local-cdn <pkgs>] [--no-browser]
     1. The shared comparison (JUDGE in js/engine/widgets/code.js, run in real Python): NaN, dicts, lists with NaN, tolerances, raises, Series.
     2. Briefs render lists (block() in js/screens/drill-lib.js, plain node) and the drill harness uses the shared judge, setup and raises.
     3. allocCheck is in the C++ drill's pass-through list.
     4. A temporary copy of app/ plays tools/fixtures/drill-page/drill-aa-page.json with playthrough --drill, desktop and --mobile (must pass: setup, raises,
        NaN, dict, tol all run by the drill page), and a copy whose brief holds an unbreakable formula (must fail --mobile with "the brief runs past").
   Python for part 1: ZQ_PYTHON, else python3. Needs Playwright and Chromium for part 4 (skipped with --no-browser). Exit 1 on a failure. */
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import vm from 'node:vm';
import { spawnSync, execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
const HERE = path.dirname(fileURLToPath(import.meta.url)), APP = path.resolve(HERE, '..');
const argv = process.argv.slice(2);
const cdnI = argv.indexOf('--local-cdn'), cdn = cdnI >= 0 ? ['--local-cdn', argv[cdnI + 1]] : [];
let bad = 0;
const check = (name, ok, detail = '') => { console.log(`${ok ? 'ok  ' : 'FAIL'} ${name}${ok ? '' : '  ' + detail}`); if (!ok) bad++; };

/* ---------- 1. the shared judge, in Python ---------- */
const code = fs.readFileSync(path.join(APP, 'js/engine/widgets/code.js'), 'utf8');
const judgeSrc = code.slice(code.indexOf('const JUDGE = `') + 'const JUDGE = `'.length).split('\n`;')[0].replace(/\$\{JSON\.stringify\(MARK\)\}/g, '"#"');
const PY = process.env.ZQ_PYTHON || 'python3';
const cases = [
  ['isclose: NaN matches NaN', 'float("nan")', 'float("nan")', 'isclose', 1],
  ['isclose: dict by key, within tolerance', '{"a": 1.0000000001, "b": [2, 3]}', '{"a": 1, "b": [2, 3]}', 'isclose', 1],
  ['isclose: dict with a wrong value', '{"a": 1.1}', '{"a": 1}', 'isclose', 0],
  ['isclose: dict with a missing key', '{"a": 1}', '{"a": 1, "b": 2}', 'isclose', 0],
  ['isclose: text equal to text', '"up"', '"up"', 'isclose', 1],
  ['isclose: True against True', 'True', 'True', 'isclose', 1],
  ['isclose: text is not the number', '"0.05"', '0.05', 'isclose', 0],
  ['isclose: list within tolerance', '[0.1 + 0.2, 1]', '[0.3, 1]', 'isclose', 1],
  ['isclose: pandas Series against a list', '__import__("pandas").Series([1.0, float("nan")])', '[1, float("nan")]', 'isclose', 1],
  ['isclose: tol rel on the case', '1.0004', '1.0', 'isclose', 0],
  ['isclose: tol rel 0.001 given', '1.0004', '1.0', 'isclose', 1, '[0.001, 0.0]'],
  ['equal: a list holding NaN', '[float("nan"), 2]', '[float("nan"), 2]', 'equal', 1],
  ['equal: a different list', '[1, 2]', '[1, 3]', 'equal', 0],
  ['fraction: a Fraction', '__import__("fractions").Fraction(1, 3)', '__import__("fractions").Fraction(1, 3)', 'fraction', 1],
  ['fraction: a float is refused', '1/3', '__import__("fractions").Fraction(1, 3)', 'fraction', 0],
];
const script = `${judgeSrc}\nimport json\nfor _n, _a, _e, _c, _w, *_t in json.loads(open(0).read()):\n    _tol = json.loads(_t[0]) if _t else None\n    _r = __zq_judge(eval(_a), eval(_e), _c, _tol)\n    print(json.dumps([_n, bool(_r) == bool(_w)]))\n`;
const py = spawnSync(PY, ['-I', '-c', script], { input: JSON.stringify(cases), encoding: 'utf8' });
if (py.status !== 0) check('judge runs in Python', false, (py.stderr || '').split('\n').slice(-3).join(' '));
else py.stdout.trim().split('\n').forEach(l => { const [n, ok] = JSON.parse(l); check('judge: ' + n, ok); });

/* ---------- 2 and 3. the page code, read in node ---------- */
const drillSrc = fs.readFileSync(path.join(APP, 'js/screens/drill.js'), 'utf8');
check('drill.js has no private comparison any more', !/def __zq_eq\(/.test(drillSrc) && /__zq_judge\(actual, expected, mode, tol\)/.test(drillSrc));
check('drill.js runs a test setup and the raises mode', /exec\(setup, globals\(\)\)/.test(drillSrc) && /mode == 'raises'/.test(drillSrc));
const libSrc = fs.readFileSync(path.join(APP, 'js/screens/drill-lib.js'), 'utf8');
check('allocCheck is passed to the C++ widget', /KEYS = \[[^\]]*'allocCheck'/.test(libSrc));
{
  const win = { console }; win.window = win; win.ZQ = {}; vm.createContext(win);
  vm.runInContext(libSrc, win);
  const Z = { esc: (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'), tex: (s) => `<k>${s}</k>` };
  const B = win.ZQ.drillLib.block;
  const h = B(Z, 'Input lines:\n- the count `n`\n- then `n` numbers, each on its own line\n  continued here\n\nAfter.');
  check('a brief renders a list', /<ul class="drl-list[^"]*"><li>the count/.test(h) && (h.match(/<li>/g) || []).length === 2 && /continued here<\/li>/.test(h), h);
  check('a list sits between paragraphs', /^<p [^>]*>Input lines:<\/p><ul/.test(h) && /<p [^>]*>After\.<\/p>$/.test(h), h);
  check('a numbered list is an ol', /<ol /.test(B(Z, '1. one\n2. two')));
  check('a plain paragraph is unchanged', B(Z, 'Just text.') === '<p class="t-prose">Just text.</p>');
  const long = B(Z, 'Call `' + 'x'.repeat(40) + '` now.');
  check('a long code span may wrap (no nowrap span)', !/drl-nw"><code/.test(long) && /<code class="drl-ic">x{40}/.test(long), long);
  check('a short code span stays together', /drl-nw"><code class="drl-ic">n<\/code>/.test(B(Z, 'the `n` here')));
}

/* ---------- 4. the page, played ---------- */
if (argv.includes('--no-browser')) console.log('note: --no-browser, the played checks are skipped');
else {
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'zq-drill-page-'));
  const copy = path.join(tmp, 'app');
  fs.cpSync(APP, copy, { recursive: true, filter: (s) => !/[\\/](node_modules|\.git)([\\/]|$)/.test(s) });
  const idxFile = path.join(copy, 'content/drills/index.json');
  const place = (doc) => {
    fs.writeFileSync(path.join(copy, 'content/drills', doc.id + '.json'), JSON.stringify(doc, null, 2));
    const idx = JSON.parse(fs.readFileSync(idxFile, 'utf8')); idx.push({ id: doc.id, name: doc.name, course: doc.course, difficulty: doc.difficulty }); fs.writeFileSync(idxFile, JSON.stringify(idx, null, 2));
    const v = spawnSync('node', [path.join(copy, 'tools/validate.mjs')], { cwd: copy, encoding: 'utf8' });
    return v.stdout + v.stderr;
  };
  // CI: the copy is in the OS temp dir, where the workspace node_modules does not resolve; play with the in-place tool, pointed at the copy
  const play = (id, mobile) => { const r = spawnSync('node', [path.join(HERE, 'playthrough.mjs'), '--drill', id, ...(mobile ? ['--mobile'] : []), ...cdn], { env: { ...process.env, ZQ_APP_DIR: copy }, encoding: 'utf8', timeout: 400000 }); return { out: (r.stdout || '') + (r.stderr || ''), code: r.status }; };
  const good = JSON.parse(fs.readFileSync(path.join(HERE, 'fixtures/drill-page/drill-aa-page.json'), 'utf8'));
  const vout = place(good);
  check('the fixture drill validates', /\b0 errors\b/.test(vout), vout.split('\n').filter(l => /^error/.test(l)).join(' | '));
  for (const mobile of [false, true]) {
    const r = play(good.id, mobile), tag = mobile ? 'mobile' : 'desktop';
    check(`fixture drill plays green, ${tag} (setup, raises, NaN, dict, tol run by the drill page)`, r.code === 0 && /ok\s+--drill drill-aa-page/.test(r.out), r.out.split('\n').slice(-6).join(' | '));
  }
  const wide = JSON.parse(JSON.stringify(good)); wide.id = 'drill-aa-wide'; wide.name = 'Drill page wide fixture';
  wide.brief = 'The formula is $' + Array.from({ length: 40 }, (_, i) => `x_{${i}}`).join('+') + '$ and nothing else.';
  place(wide);
  const w = play(wide.id, true);
  check('an unbreakable line in the brief fails --mobile', w.code !== 0 && /the brief runs past the right edge at 440 px/.test(w.out), w.out.split('\n').slice(-6).join(' | '));
  const wd = play(wide.id, false);
  check('the same drill is fine on desktop', wd.code === 0, wd.out.split('\n').slice(-4).join(' | '));
  /* a radical's svg path is 400000 units wide inside its own clipped box (the five drills that failed on CI); it is not a brief running past the edge */
  const rad = JSON.parse(JSON.stringify(good)); rad.id = 'drill-aa-radical'; rad.name = 'Drill page radical fixture';
  rad.brief = 'The scale is $\\sqrt{252}$ a year, and the spread is $\\sqrt{\\frac{a}{b}}$ per period.';
  place(rad);
  const rm = play(rad.id, true);
  check('a radical in the brief does not fail --mobile', rm.code === 0 && !/runs past/.test(rm.out), rm.out.split('\n').slice(-6).join(' | '));
  fs.rmSync(tmp, { recursive: true, force: true });
}
console.log(bad ? `${bad} failed` : 'all passed');
process.exitCode = bad ? 1 : 0;
