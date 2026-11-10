"""Delta checks beyond run.py. From the repo root: <venv python> docs/reviews/delta-drills-ci-3-4-scripts/extra.py
1. index.json rows against the 30 pack-3 and pack-4 drill files; the pack mix.
2. Changed and added tests against each drill's own constraints.
3. The site samples the review named: still present, or present with the values renamed (same order pattern)?
4. Candidates the fixer did not plant (extra_cands.py) on the hidden tests, and the tests proposed in the delta review."""
import json, glob, re, os, sys, signal, time, importlib.util, inspect
from collections import Counter
S = os.path.dirname(os.path.abspath(__file__)) + '/'
def load(name):
    spec = importlib.util.spec_from_file_location(name, S + name + '.py'); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
mine, cands = load('mine'), load('extra_cands')
D = lambda i: json.load(open('app/content/drills/%s.json' % i))
problems = 0
def flag(msg):
    global problems; problems += 1; print('  FLAG', msg)

print('1. index rows')
idx = json.load(open('app/content/drills/index.json'))
rows = idx['drills'] if isinstance(idx, dict) else idx
rows = {r['id']: r for r in rows}
packs = {}
for f in sorted(glob.glob('app/content/drills/ci-*.json')):
    d = json.load(open(f))
    if d['tags'][0] not in ('pack-3', 'pack-4'): continue
    packs.setdefault(d['tags'][0], []).append(d)
    r = rows.get(d['id'])
    if r is None: flag('no index row for ' + d['id']); continue
    for k in ('name', 'course', 'difficulty'):
        if r.get(k) != d.get(k): flag('%s: index %s %r, file %r' % (d['id'], k, r.get(k), d.get(k)))
    for k in r:
        if k in d and r[k] != d[k] and k not in ('name', 'course', 'difficulty'): flag('%s: index %s %r, file %r' % (d['id'], k, r[k], d[k]))
for p, ds in packs.items():
    print('  ', p, len(ds), 'drills, mix', sorted(Counter(d['difficulty'] for d in ds).items()), 'stdin', sum('stdin' in d['tags'] for d in ds),
          'planted counts', sorted(Counter(len(d['planted']) for d in ds).items()), 'tests', min(len(d['tests']) for d in ds), 'to', max(len(d['tests']) for d in ds))

print('2. tests against constraints')
class Stop(Exception): pass
def args_of(d, t):
    """the arguments a test's call hands to the drill's function"""
    got = []
    def rec(*a):
        got.append(a); raise Stop()
    try: eval(t['call'], {d['fn']: rec})
    except Stop: pass
    return got[0]
def each(did):
    d = D(did); ne = len(d['examples'])
    for n, t in enumerate(d['examples'] + d['tests']):
        yield d, ('example %d' % n if n < ne else 'tests[%d]' % (n - ne)), args_of(d, t)
for d, lab, (text,) in each('ci-live-median'):     # sizes 1 to 10^9, q events, every cancel live
    tok = text.split(); q = int(tok[0]); live = Counter(); out = badc = 0
    assert len(tok) == 1 + 2 * q and q <= 400000, lab
    for i in range(q):
        op, x = tok[1 + 2 * i], int(tok[2 + 2 * i])
        if not 1 <= x <= 10 ** 9: out += 1
        if op == '+': live[x] += 1
        else:
            badc += live[x] <= 0; live[x] -= 1
    if out or badc: flag('ci-live-median %s: %d sizes outside 1 to 10^9, %d cancels of a size not live' % (lab, out, badc))
for d, lab, (board, words) in each('ci-board-words'):
    ok = len(board) <= 12 and all(len(r) <= 12 and len(r) == len(board[0]) for r in board) and len(words) <= 5000 and len(set(words)) == len(words) and all(1 <= len(w) <= 12 and w.islower() for w in words)
    if not ok: flag('ci-board-words %s breaks the constraints' % lab)
    if len(words) > 20: print('   board-words', lab, ':', len(words), 'words, board', len(board), 'x', len(board[0]))
for d, lab, (ring, targets) in each('ci-ring-lookup'):
    s = ring.index(min(ring)) if ring else 0
    flat = ring[s:] + ring[:s]
    ok = flat == sorted(set(ring)) and len(ring) <= 100000 and len(targets) <= 100000 and all(-10 ** 9 <= x <= 10 ** 9 for x in ring + targets)
    if not ok: flag('ci-ring-lookup %s breaks the constraints' % lab)
    if len(ring) > 100:
        have = set(ring)
        print('   ring', lab, ': n', len(ring), '| largest gap between neighbouring ids', max(b - a for a, b in zip(flat, flat[1:])), '| targets absent', sum(1 for x in targets if x not in have))
for d, lab, (text,) in each('ci-tick-ranges'):
    v = [int(x) for x in text.split()]; nn, q = v[0], v[1]; ticks, qs = v[2:2 + nn], v[2 + nn:]
    ok = len(qs) == q and ticks == sorted(ticks) and nn <= 100000 and q <= 100000 and all(0 <= x <= 10 ** 12 for x in ticks + qs)
    if not ok: flag('ci-tick-ranges %s breaks the constraints' % lab)
    have = sorted(set(ticks))
    absent = [x for x in qs if x not in set(ticks) and have and x < have[-1]]
    if absent:
        from bisect import bisect_left
        print('   ticks', lab, ': longest walk up from an absent query to the next tick', max(have[bisect_left(have, x)] - x for x in absent))
for d, lab, (trips, k) in each('ci-busiest-links'):
    ok = len(trips) <= 200000 and 0 <= k <= 200000 and all(a != b and re.fullmatch(r'[A-Z][a-z0-9]*', a) and re.fullmatch(r'[A-Z][a-z0-9]*', b) for a, b in trips)
    if not ok: flag('ci-busiest-links %s breaks the constraints' % lab)
for d, lab, (c, k, ps) in each('ci-funded-projects'):
    if not (len(ps) <= 100000 and 0 <= k <= 100000 and all(0 <= a <= 10 ** 9 and 0 <= b <= 10 ** 9 for a, b in ps)): flag('ci-funded-projects ' + lab)
for d, lab, (ev,) in each('ci-stock-by-prefix'):
    if not (len(ev) <= 200000 and all(re.fullmatch(r'[A-Z0-9]{0,12}', e[1]) and (e[0] == 'ask' or 0 <= e[2] <= 10 ** 6) for e in ev)): flag('ci-stock-by-prefix ' + lab)
for d, lab, (tg, pos, sp) in each('ci-van-convoys'):
    if not (len(set(pos)) == len(pos) == len(sp) <= 200000 and 1 <= tg <= 10 ** 9 and all(0 <= p < tg for p in pos) and all(1 <= s <= 10 ** 6 for s in sp)): flag('ci-van-convoys ' + lab)
for d, lab, (rel, k) in each('ci-relay-masts'):
    if not (rel == sorted(set(rel)) and 2 <= len(rel) <= 100000 and 0 <= rel[0] and rel[-1] <= 10 ** 9 and 0 <= k <= 10 ** 9): flag('ci-relay-masts ' + lab)
for d, lab, (qs, m) in each('ci-clear-rate'):
    if not (1 <= len(qs) <= m <= 10 ** 9 and all(1 <= x <= 10 ** 9 for x in qs)): flag('ci-clear-rate ' + lab)
for d, lab, (log, k) in each('ci-log-compactor'):
    if not (len(log) <= 200000 and 2 <= k <= 200000 and (log == '' or log.islower())): flag('ci-log-compactor ' + lab)
for d, lab, (f,) in each('ci-cell-formula'):
    if not (1 <= len(f) <= 600000 and all(abs(int(x)) <= 10 ** 9 for x in re.findall(r'-?\d+', f))): flag('ci-cell-formula ' + lab)
for d, lab, (pr,) in each('ci-price-ramp'):
    if not (len(pr) <= 200000 and all(0 <= x <= 10 ** 9 for x in pr)): flag('ci-price-ramp ' + lab)
for d, lab, (h,) in each('ci-visible-masts'):
    if not (len(h) <= 200000 and len(set(h)) == len(h) and all(1 <= x <= 10 ** 9 for x in h)): flag('ci-visible-masts ' + lab)
for d, lab, (rd, k, m) in each('ci-ready-blocks'):
    if not (1 <= len(rd) <= 100000 and 1 <= k <= len(rd) and 1 <= m <= 10 ** 6 and all(1 <= x <= 10 ** 9 for x in rd)): flag('ci-ready-blocks ' + lab)
for d, lab, (a, b, k) in each('ci-cheapest-pairs'):
    if not (a == sorted(a) and b == sorted(b) and len(a) <= 100000 and len(b) <= 100000 and 0 <= k <= min(100000, len(a) * len(b)) and all(0 <= x <= 10 ** 9 for x in a + b)): flag('ci-cheapest-pairs ' + lab)
for d, lab, (par, vals, tg) in each('ci-downward-path-sums'):
    if not (1 <= len(par) == len(vals) <= 100000 and par.count(-1) == 1 and all(abs(x) <= 10 ** 4 for x in vals)): flag('ci-downward-path-sums ' + lab)
for d, lab, (sh,) in each('ci-no-repeat-rota'):
    if not (len(sh) <= 200000 and (sh == '' or sh.islower())): flag('ci-no-repeat-rota ' + lab)

print('3. site samples (recalled from memory, as in the first review; not checked online)')
def pattern(xs):
    r = {v: i for i, v in enumerate(sorted(set(xs)))}; return [r[x] for x in xs]
SITE = {  # drill: lists the site's samples use
    'ci-clear-rate': [[3, 6, 7, 11], [30, 11, 23, 4, 20]],
    'ci-price-ramp': [[6, 0, 8, 2, 1, 5], [9, 8, 1, 0, 1, 9, 4, 0, 4, 1]],
    'ci-ready-blocks': [[1, 10, 3, 10, 2], [7, 7, 7, 7, 12, 7, 7]],
    'ci-visible-masts': [[10, 6, 8, 5, 11, 9], [5, 1, 2, 3, 10]],
    'ci-van-convoys': [[10, 8, 0, 5, 3], [2, 4, 1, 1, 3]],
    'ci-cheapest-pairs': [[1, 7, 11], [2, 4, 6]],      # the second sample, [1, 1, 2] and [1, 2, 3], is too plain to search for
    'ci-rebuild-from-orders': [[3, 9, 20, 15, 7], [9, 3, 15, 20, 7]],
    'ci-downward-path-sums': [[10, 5, -3, 3, 2, 11, 3, -2, 1], [10, 5, 3, 2, -3, 11]],
}
for did, lists in SITE.items():
    d = D(did)
    text = ' '.join([d['brief']] + [t['call'] for t in d['examples'] + d['tests']])
    found = [json.loads(m) for m in set(re.findall(r'\[-?\d+(?:, -?\d+)*\]', text))]
    for s in lists:
        same = [f for f in found if f == s]
        if same: flag('%s still holds the site list %s' % (did, s))
        if len(s) < 5: continue      # a short list matches by chance
        ren = [f for f in found if f != s and len(f) >= len(s) and any(pattern(f[a:a + len(s)]) == pattern(s) for a in range(len(f) - len(s) + 1))]
        for f in ren: print('   %s: %s has the order pattern of the site list %s' % (did, f, s))
        near = [f for f in found if f != s and len(f) == len(s) and f not in ren and sum(a != b for a, b in zip(pattern(f), pattern(s))) == 1]
        for f in near: print('   %s: %s has the order pattern of the site list %s but for one entry' % (did, f, s))
for did, words in {'ci-board-words': ['oaan', 'oath'], 'ci-no-repeat-rota': ["'aaab'"], 'ci-funded-projects': ['[[0, 1], [1, 2], [1, 3]]'], 'ci-right-edge-view': ['(1, (2, None, (5, None, None)), (3, None, None))']}.items():
    raw = open('app/content/drills/%s.json' % did).read()
    for w in words:
        if w in raw: print('   %s still holds %s' % (did, w))

print('4. candidates not planted, and proposed tests')
class Slow(Exception): pass
def alarm(*_): raise Slow()
signal.signal(signal.SIGALRM, alarm)
def verdict(fnname, fn, t, limit=6):
    signal.setitimer(signal.ITIMER_REAL, limit)
    try:
        got = eval(t['call'], {fnname: fn}); signal.setitimer(signal.ITIMER_REAL, 0)
    except Slow:
        return 'SLOW over %d s' % limit
    return 'ok' if got == eval(t['expect']) else 'got %r' % (got,)
PROPOSED = json.load(open(S + 'proposed_tests.json'))
for did, cname in (('ci-ring-lookup', 'find_in_ring__dict_probe'), ('ci-tick-ranges', 'solve_tick_ranges__dict_probe')):
    d = D(did); fn = d['fn']; cand = getattr(cands, cname)
    res = [verdict(fn, cand, t) for t in d['tests']]
    print('  ', did, cname, 'on the', len(res), 'hidden tests:', 'PASSES ALL' if all(r == 'ok' for r in res) else res)
    ns = {}; exec(d['solution'], ns)
    for t in PROPOSED[did]:
        print('     proposed', t['call'][:70], '=>', t['expect'], '| model', verdict(fn, ns[fn], t), '| mine', verdict(fn, getattr(mine, fn), t), '| candidate', verdict(fn, cand, t))
d = D('ci-live-median'); ns = {}; exec(d['solution'], ns)
for t in PROPOSED['ci-live-median']:
    print('   ci-live-median proposed', t['call'][-150:-60], '=>', t['expect'], '| model', verdict('solve_live_median', ns['solve_live_median'], t, 20), '| mine', verdict('solve_live_median', mine.solve_live_median, t, 20))
print('flags:', problems)
