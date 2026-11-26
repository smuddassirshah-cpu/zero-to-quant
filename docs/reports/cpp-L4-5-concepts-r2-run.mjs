// Driver of the C++ part of docs/reports/cpp-L4-5-concepts-r2.py (blind concept audit cpp-4-5-r2).
// Every check compiles with the page's own translation-unit builder (js/engine/widgets/cpp-grade.js, Z.cppCode.lib.unit) and the page
// worker's own FLAGS, LINK, RUNTIME and WASI runner (js/screens/cpp-worker.js): YoWASP clang 21.1.4 for wasm32, -std=c++17 -O1, libc++
// hardening (extensive), no exception support. The compiler comes from the local CDN folder (--pkgs, the playthrough's --local-cdn).
//   node cpp-L4-5-concepts-r2-run.mjs --app <app dir> --pkgs <pkgs dir> [--shard i/n]
// One line per check: "ok ..." or "FAIL ...". A FAIL tagged FINDING is a content defect recorded in docs/reviews/audit-cpp-4-5-r2.md.
import fs from 'node:fs';
import path from 'node:path';
import { make } from './cpp-L4-5-concepts-r2-zq.mjs';
import { jobs as mutants, fixes } from './cpp-L4-5-concepts-r2-mutants.mjs';
import { jobs as programs } from './cpp-L4-5-concepts-r2-programs.mjs';

const arg = (k, d) => { const i = process.argv.indexOf(k); return i >= 0 ? process.argv[i + 1] : d; };
const APP = path.resolve(arg('--app', 'app')), PKGS = path.resolve(arg('--pkgs', process.env.ZQ_LOCAL_CDN || 'pkgs'));
const [si, sn] = arg('--shard', '0/1').split('/').map(Number);
const C = path.join(APP, 'content/courses/cpp');
const specOf = (file, where) => {
  const d = JSON.parse(fs.readFileSync(path.join(C, file + '.json'), 'utf8'));
  if (/^s\d+$/.test(where)) return d.screens[+where.slice(1)].widget;
  return (d.items || []).find((x) => x.id === where).widget;
};

/* What each claim program must print, crash with or fail to compile with (regex on the JSON of its result) */
const EXPECT = {
  'sizes': [/Tick=4 VTick=8 B=8 D=12 Quote=24 W=8 S=8 B2=16/, /ptr=4 int=4 long=4 size_t=4 double_align=8 Buffer=8/, /unique=4 shared=8/, /size_max=4294967295/, /m7=-3 shl=2147483648/],
  'growth': [/caps: 1 2 4 4 8 8 8 8 16/, /allocations=11 moves=10 copied=1023 cap=1024/, /reserve\(1000\): cap=1000 size_after_reserve=0 moves=0/, /reserve\(100\)\+150: cap=200/, /reserve\(5\): cap=5/, /v\(3\)\+push: size=4 z0=0/, /five: cap=8/],
  'erase-loop': [/"out":"101.2 0 101.5 /],
  'erase-last': [/"trap":"memory access out of bounds"/],
  'transform-empty': [/size=0 done/],
  'max-element-empty-plain': [/"out":""/, /"trap":"unreachable"/],
  'sort-le-3': [/"out":"99.8 100.5 100.5 /],
  'sort-le-equal-8': [/sorted 8/],
  'sort-le-equal-40': [/does your comparator satisfy the strict-weak ordering requirement/, /"trap":"unreachable"/],
  'sort-le-equal-2000': [/does your comparator satisfy the strict-weak ordering requirement/],
  'null-read-constant': [/"out":"v=0\\n"/, /"trap":null/],
  'null-read-unknown': [/before\\nv=/, /"trap":null/],
  'first-asm': [(t) => { const seg = (n) => { const a = t.indexOf(n + ':'); return a < 0 ? '' : t.slice(a, t.indexOf('end_function', a)); }; const f = seg('_Z5firstPi'), g = seg('_Z6secondPi'); return /local\.get\\t0\\n\\ti32\.load\\t0/.test(f) && !/br_if|i32\.eqz|select/.test(f) && /br_if/.test(g); }],
  'moves-l19': [/l2 copies=1 moves=0/, /l3 copies=0 moves=1/, /l4 copies=0 moves=0/, /l5 copies=1 moves=0/, /l6 copies=0 moves=1/, /l7 copies=0 moves=0/, /l8 copies=1 moves=0/, /cast-only copies=0 moves=0/, /cast\+ctor copies=0 moves=1/, /four pushes noexcept copies=0 moves=7/, /return t copies=0 moves=0/, /return std::move\(t\) copies=0 moves=1/, /r5 three calls const k copies=2 moves=0/, /quiz three calls copies=1 moves=1/],
  'moves-throwing': [/two pushes, move may throw copies=1 moves=2/, /move-only, move may throw: moves=7/],
  'special-members': [/nothing +copy +move +copy +move/, /destructor +copy +copy +copy +copy/, /copy ctor +copy +copy +copy +copy/, /copy assign +copy +copy +copy +copy/, /move ctor +error move +error error/, /move assign +error error error move/, /all five +copy +move +copy +move/, /Pos nothrow move=1 Pos3 nothrow move=0 Pos copyable=1/, /string nothrow move=1 vector nothrow move=1/, /Order: default=1 moveinit=0 copyinit=0 moveassign=0/, /Holder: copy=0 move=1/],
  'numbers': [/bids=3 sum=100.19999999999999/, /ratio-1=0.10000000000000009 eq=0 diff\/prev=0.10000000000000001 eq=1/, /vwap=10.149999999999999 eq=0/, /acc int=173 double=175/, /fees int=8/, /count=3/, /bs=10.45058\d+ bin100=10.43061\d+ bin99=10.4683\d+ bin2000=10.449\d+ bin1999=10.451\d+/, /use=2/, /use after move=2 b=0/, /adj: 100 4 -3 5 -3/],
  'ctor-virtual-and-slice': [/who=Base later=Derived/, /slice=-1 ref=10/],
  'length-error': [/std::length_error/],
  'reserve-huge': [/std::length_error/],
  'const-map-index': [/no viable overloaded operator\[\]/],
  'unordered-order': [/AZN BARC VOD \| SHEL BP AZN/],
  'count-if-begin-plus-1-empty': [/"out":"start\\n"/, /"code":134/],
  'vector-move-source': [/v\.size=0 w\.size=3/],
  'seven-over-two': [/4294967295 3 1/],
  'l21-s9-listing': 'FINDING-compiles',
  'l21-s9-listing-fixed': [/"ok":true/],
};

const G = await make({ app: APP, pkgs: PKGS });
let k = 0, bad = 0;
const say = (ok, tag, text) => { if (!ok) bad++; console.log(`${ok ? 'ok  ' : 'FAIL'} ${tag} ${text}`); };
const mine = () => (k++ % sn) === si;

for (const j of programs) {
  if (!mine()) continue;
  let res;
  if (j.asm != null) { const r = await G.ccRaw([...G.flags, '-S', 'f.cpp', '-o', 'f.s'], { 'f.cpp': j.asm }); const fx = r.files && r.files['f.s']; res = JSON.stringify(r.ok && fx ? (typeof fx === 'string' ? fx : new TextDecoder().decode(fx)) : r.diag); }
  else if (j.cc != null) { const r = await G.cc(j.cc, j.files); res = JSON.stringify({ ok: r.ok, diag: r.diag.slice(0, 600) }); if (EXPECT[j.name] === 'FINDING-compiles') { say(r.ok, 'FINDING', `${j.name}: the listing shown on the screen must compile (it does ${r.ok ? '' : 'not'})`); continue; } }
  else { const r = await G.runProg(j.prog, j.stdin || '', j.flags || []); res = JSON.stringify(r.ok ? { out: r.out, err: (r.err || '').slice(0, 300), code: r.code, trap: r.trap, timeout: r.timeout } : { compile: r.diag.slice(0, 600) }); }
  const ex = EXPECT[j.name];
  if (!ex) { console.log(`note ${j.name}: ${res.slice(0, 200)}`); continue; }
  const miss = ex.filter((re) => !(typeof re === 'function' ? re(res) : re.test(res)));
  say(!miss.length, 'PROGRAM', `${j.name}` + (miss.length ? ` missing ${miss.map(String).join(' ; ')} in ${res.slice(0, 400)}` : ''));
}

const gradeJob = async (j) => {
  const spec0 = specOf(j.file, j.where);
  const spec = j.extra ? j.extra(JSON.parse(JSON.stringify(spec0))) : spec0;
  const src = j.src === 'solution' ? spec.solution : j.src === 'starter' ? spec.starter : j.src(spec.solution, spec.starter);
  if (j.src !== 'solution' && j.src !== 'starter' && src === spec.solution) return { key: 'MUTANT-UNCHANGED' };
  return G.grade(spec, src, j.which || 'tests');
};
const WIDGETS = [['l14-vector', ['s3', 's4', 's6', 's7', 's10']], ['l15-maps', ['s4', 's5', 's7']], ['l16-algorithms', ['s3', 's4', 's5', 's9']], ['l17-cmake', ['s4', 's5']], ['l18-unit-tests', ['s3', 's4', 's5', 's9']], ['l19-moving-not-copying', ['s5']], ['l20-rule-of-five', ['s5']], ['l21-virtual-dispatch', ['s5']], ['l22-undefined-behaviour', ['s4']], ['l23-own-smart-pointer', ['s2', 's5']], ['homework-4', ['h4-vwap-book', 'h4-test-drawdown', 'h4-test-median']], ['homework-5', ['h5-scope-guard', 'h5-vec', 'h5-sole-and-counted']]];
for (const [file, ws] of WIDGETS) for (const where of ws) {
  if (!mine()) continue;
  const a = await gradeJob({ file, where, src: 'solution' }), b = await gradeJob({ file, where, src: 'solution', which: 'examples' }), c = await gradeJob({ file, where, src: 'starter' });
  say(a.key === null && b.key === null && c.key !== null, 'WIDGET', `${file} ${where}: solution ${a.key}, examples ${b.key}, starter ${c.key}`);
}
for (const j of mutants) {
  if (!mine()) continue;
  let r; try { r = await gradeJob(j); } catch (e) { say(false, 'MUTANT', `${j.name}: threw ${e && e.message}`); continue; }
  const w = j.want;
  if (w === 'FINDING') say(r.key !== null, 'FINDING', `${j.name} [${j.file} ${j.where}]: a wrong program must fail a hidden test (key ${r.key})`);
  else if (w === 'DOCUMENTED') say(true, 'MUTANT', `${j.name}: passes (key ${r.key}); the widget's own text says no test covers it`);
  else if (w === 'reject') say(r.key !== null, 'MUTANT', `${j.name}: rejected at ${r.key}`);
  else say(String(r.key) === String(w), 'MUTANT', `${j.name} [${j.file} ${j.where}]: key ${r.key}, the line it should reach ${w}`);
}
for (const j of fixes) {
  if (!mine()) continue;
  const r = await gradeJob(j);
  say(j.want === undefined ? r.key !== null : String(r.key) === String(j.want), 'PROPOSED-FIX', `${j.name}: key ${r.key}`);
}
console.log(`shard ${si}/${sn}: ${bad} failing`);
process.exit(bad ? 1 : 0);
