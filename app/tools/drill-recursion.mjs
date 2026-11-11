#!/usr/bin/env node
/* Drills a natural recursive solution could not finish on the page (ENGINE-BACKLOG 917). Run from app/:
     node tools/drill-recursion.mjs [--drill <id>]... [--json] [--all]
   For every Python drill in content/drills (samples left out) it reads the size of every hidden test's arguments, and the upper bounds the
   machine `constraints` objects allow, and compares them with the safe depths of the page's Python (docs/AUTHORING.md, "Deep recursion"):
     plain or dict-remembered recursion   2,900 calls     (recursion limit 3,000)
     lru_cache recursion                  1,400 calls     (two frames a call)
     a generator expression, sorted key or map in each call   300 calls (the browser stack)
   The depth a recursion reaches is not knowable from the data alone, so the estimate is the one a natural linear-depth recursion has:
   a string or list is its length, the lengths of several sequence arguments add (a recursion that steps through two feeds), a grid is
   rows + cols (and rows * cols is shown for a depth-first search), a whole number up to 100,000 is its value (larger ones are taken as
   an input for a formula or a loop), and a stdin text is its longest line or its number of lines.
   `(the text warns ...)` marks a brief, hint, note or `how` that already tells the learner to avoid deep recursion.
   Only drills whose natural method is recursive are listed: a `dp`, `backtracking`, `trees` or `graphs` pattern, a `dp-` tag, or a brief, hint, note or
   model that says recursion, memo, top-down, dfs or lru_cache. The rest (heaps, windows, sorting, prefix sums) are counted, not listed.
   A drill is AT RISK when the tests or the constraints reach past a safe depth: "tests" says the hidden tests do, "bound" that only the
   constraints allow it (a learner's input could, none of the tests does). `dfs` marks a grid whose cell count passes the plain depth.
   Prose-only constraints (no object for an argument) have no bound: the tool says "unbounded" for that drill.
   Exit 0 always (it is a report); --json prints the rows. The check that the models themselves still pass on the page is
   node tools/playthrough.mjs --drills --local-cdn <pkgs>. */
import fs from 'node:fs';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
const HERE = path.dirname(fileURLToPath(import.meta.url));
const APP = process.env.ZQ_APP_DIR ? path.resolve(process.env.ZQ_APP_DIR) : path.resolve(HERE, '..');
const DRILLS = path.join(APP, 'content', 'drills');
const LIMITS = { plain: 2900, lru: 1400, gen: 300 };
const argv = process.argv.slice(2), only = [];
let json = false;
for (let i = 0; i < argv.length; i++) { if (argv[i] === '--drill') only.push(argv[++i]); else if (argv[i] === '--json') json = true; else if (argv[i] === '--all') { /* default */ } else { console.error(`drill-recursion: unknown argument ${argv[i]}`); process.exit(2); } }

const files = fs.readdirSync(DRILLS).filter(f => f.endsWith('.json') && f !== 'index.json').map(f => f.replace(/\.json$/, '')).sort();
const docs = [];
for (const id of (only.length ? only : files)) {
  if (!files.includes(id)) { console.error(`drill-recursion: no drill ${id}`); process.exit(2); }
  const d = JSON.parse(fs.readFileSync(path.join(DRILLS, id + '.json'), 'utf8'));
  if (d.sample === true || (d.language || 'python') !== 'python') continue;
  const text = [d.brief, d.hint, d.solution, ...(d.notes || []), ...(d.constraints || []).filter(c => typeof c === 'string')].join(' ');
  const natural = ['dp', 'backtracking', 'trees', 'graphs'].includes(d.pattern) || (d.tags || []).some(t => /^dp-/.test(t)) || /\brecurs|\bmemo|top-down|\bdfs\b|depth-first|lru_cache/i.test(text);
  const said = [d.brief, d.hint, ...(d.notes || []), d.how, ...(d.constraints || []).filter(c => typeof c === 'string')].join(' ');
  const warned = /recursi\w* (limit|depth)|too deep|iterative|explicit stack|(no|not|without|avoid)\w* recurs|deep recursion|stack of your own/i.test(said);
  docs.push({ id, fn: d.fn, natural, warned, tests: (d.tests || []).map(t => ({ call: t.call, setup: t.setup || '' })), constraints: (d.constraints || []).filter(c => c && typeof c === 'object') });
}

/* Python measures the arguments of every test call: the function name is bound to a recorder, so the call's own argument expressions
   (and any wrapper such as a lambda around it) are evaluated as written. */
const PY = String.raw`
import json, sys
LIM = 100000
def lin(x):
    if isinstance(x, bool): return 0
    if isinstance(x, int): return abs(x) if abs(x) <= LIM else 0
    if isinstance(x, float): return 0
    if isinstance(x, str):
        if '\n' in x:
            ls = x.split('\n'); return max(len(ls), max((len(l) for l in ls), default=0))
        return len(x)
    if isinstance(x, (list, tuple)):
        if x and all(isinstance(r, (list, tuple, str)) for r in x):
            return len(x) + max(len(r) for r in x)   # a grid or a list of words: rows + columns
        return len(x)
    if isinstance(x, (dict, set, frozenset)): return len(x)
    return 0
def cells(x):
    if isinstance(x, (list, tuple)) and x and all(isinstance(r, (list, tuple, str)) for r in x):
        return len(x) * max(len(r) for r in x)
    return 0
def seqlen(x):
    return len(x) if isinstance(x, (list, tuple, str, dict, set)) and not isinstance(x, bool) else 0
class Any:
    # what the recorder returns, so a test that indexes, measures or adds to the result still evaluates
    def __getitem__(self, k): return Any()
    def __len__(self): return 0
    def __iter__(self): return iter(())
    def __bool__(self): return False
    def __getattr__(self, k): return Any()
    def __call__(self, *a, **k): return Any()
    def __index__(self): return 0
    def __int__(self): return 0
    def __float__(self): return 0.0
    def __contains__(self, k): return False
    def __eq__(self, o): return False
    def __hash__(self): return 0
    def __lt__(self, o): return False
    __gt__ = __le__ = __ge__ = __lt__
    def _bin(self, o): return Any()
    __add__ = __radd__ = __sub__ = __rsub__ = __mul__ = __rmul__ = __truediv__ = __rtruediv__ = __floordiv__ = __mod__ = __pow__ = __neg__ = _bin
out = {}
for d in json.load(sys.stdin):
    rows = []
    for t in d['tests']:
        rec = []
        def fn(*a, **k):
            rec.append(list(a) + list(k.values())); return Any()
        env = {d['fn']: fn}
        try:
            if t['setup']: exec(t['setup'], env)
            env[d['fn']] = fn
            eval(t['call'], env)
            args = rec[0] if rec else []
            rows.append({'depth': max([max((lin(a) for a in args), default=0), sum(seqlen(a) if not (isinstance(a, str) and '\n' in a) else 0 for a in args)]), 'cells': max((cells(a) for a in args), default=0)})
        except BaseException as e:
            rows.append({'err': type(e).__name__ + ': ' + str(e)[:60]})
    out[d['id']] = rows
print(json.dumps(out))
`;
const r = spawnSync(process.env.ZQ_PYTHON || 'python3', ['-I', '-c', PY], { input: JSON.stringify(docs), encoding: 'utf8', maxBuffer: 1 << 28 });
if (r.status !== 0) { console.error('drill-recursion: the Python measuring step failed\n' + (r.stderr || '').split('\n').slice(-4).join('\n')); process.exit(2); }
const measured = JSON.parse(r.stdout);

/* The depth the constraints allow: one object per argument, `len` and `range` upper bounds, a grid as rows + cols */
const bound = (d) => {
  const objs = d.constraints.filter(c => c.arg !== undefined);
  if (!objs.length) return null;
  const hi = (c) => {
    if (c.type === 'int') return c.range && c.range[1] <= 100000 ? Math.max(0, c.range[1]) : 0;
    if (c.len) {
      const inner = c.of && typeof c.of === 'object' && c.of.len ? c.of.len[1] : 0;
      return inner ? { depth: c.len[1] + inner, cells: c.len[1] * inner, len: c.len[1] } : { depth: c.len[1], cells: 0, len: c.len[1] };
    }
    return c.type === 'int' || c.type === 'float' || c.type === 'bool' ? 0 : null;
  };
  let depth = 0, cells = 0, sum = 0;
  for (const c of objs) {
    const h = hi(c);
    if (h === null) return null;
    const dv = typeof h === 'number' ? h : h.depth;
    depth = Math.max(depth, dv); cells = Math.max(cells, typeof h === 'number' ? 0 : h.cells); sum += typeof h === 'number' ? 0 : h.len;
  }
  return { depth: Math.max(depth, sum), cells };
};

const rows = [];
for (const d of docs) {
  const ms = measured[d.id] || [], ok = ms.filter(m => !m.err);
  const td = ok.reduce((a, m) => Math.max(a, m.depth), 0), tc = ok.reduce((a, m) => Math.max(a, m.cells), 0);
  const b = bound(d), bd = b ? b.depth : null, bc = b ? b.cells : 0;
  const reach = (n) => ({ gen: n > LIMITS.gen, lru: n > LIMITS.lru, plain: n > LIMITS.plain });
  const t = reach(td), c = b ? reach(bd) : { gen: false, lru: false, plain: false };
  const level = t.plain ? 'plain' : t.lru ? 'lru' : t.gen ? 'gen' : c.plain ? 'plain' : c.lru ? 'lru' : c.gen ? 'gen' : null;
  const by = (t.gen ? 'tests' : (c.gen ? 'bound' : ''));
  rows.push({ id: d.id, natural: d.natural, warned: d.warned, testsDepth: td, boundDepth: bd, testsCells: tc, boundCells: bc, level, by, dfs: Math.max(tc, bc) > LIMITS.plain, unbounded: b === null, unevaluated: ms.filter(m => m.err).length, errs: ms.filter(m => m.err).map(m => m.err).slice(0, 1) });
}
const risk = rows.filter(x => x.level && x.natural), loopOnly = rows.filter(x => x.level && !x.natural);
if (json) console.log(JSON.stringify(rows, null, 1));
else {
  console.log(`drill-recursion: ${rows.length} Python drills measured, ${risk.length} at risk, plus ${loopOnly.length} whose natural method is a loop (a natural recursion passes a safe depth: generator ${LIMITS.gen}, lru_cache ${LIMITS.lru}, plain or dict ${LIMITS.plain})`);
  console.log(`of the ${risk.length}, ${risk.filter(x => x.warned).length} already warn the learner about recursion in their text and ${risk.filter(x => !x.warned).length} do not`);
  const byLevel = (l) => risk.filter(x => x.level === l);
  for (const [l, label] of [['plain', 'past 2,900 (plain, dict-remembered and lru_cache all fail)'], ['lru', 'past 1,400 (lru_cache fails; plain and dict pass)'], ['gen', 'past 300 (fails only with a generator, sorted key or map in each call)']]) {
    const g = byLevel(l); console.log(`\n${label}: ${g.length}`);
    g.forEach(x => console.log(`  ${x.id}  tests ${x.testsDepth}  bound ${x.boundDepth ?? 'unbounded'}  ${x.by === 'tests' ? 'by a hidden test' : 'by the constraints only'}${x.warned ? '  (the text warns about recursion)' : ''}${x.dfs ? `  dfs cells ${Math.max(x.testsCells, x.boundCells)}` : ''}`));
  }
  const dfs = rows.filter(x => x.dfs && x.natural && !x.level); if (dfs.length) console.log(`\ngrid cell count past 2,900 (a depth-first search), not otherwise at risk: ${dfs.length}: ${dfs.map(x => x.id).join(', ')}`);
  const unb = rows.filter(x => x.unbounded); console.log(`\nno machine bound (prose-only constraints, tests only): ${unb.length}`);
  const ue = rows.filter(x => x.unevaluated); if (ue.length) console.log(`tests that could not be evaluated: ${ue.map(x => `${x.id} (${x.unevaluated}: ${x.errs[0]})`).join('; ')}`);
}
