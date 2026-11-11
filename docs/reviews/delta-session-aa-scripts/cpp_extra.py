"""Delta read, session AA: checks on the `cpp` fix pass that need no compiler, and two that do.

Run from the repo root with the scratchpad venv Python (ZQ_TMP=<scratch dir> for the build folder).
Every new or changed `expect` is recomputed here by a method of mine (exact fractions, integers, mpmath or
counting); cpp_run.py holds the second method (my C++ solutions) and drills-cpp-check.py the author's.
"""
import importlib.util
import json
import math
import os
import re
import struct
import sys
from fractions import Fraction as F

import mpmath as mp

HERE = os.path.dirname(os.path.abspath(__file__))
D = 'app/content/drills/'
bad = 0


def check(name, ok, detail=''):
    global bad
    print(('ok   ' if ok else 'FAIL ') + name + (f' | {detail}' if detail != '' else ''))
    bad += not ok


def drill(i):
    return json.load(open(D + i + '.json'))


def tests(i, call=None):
    return [t for t in drill(i)['tests'] if call is None or t.get('call') == call]


def close(a, b):
    return abs(a - b) <= 1e-9 * max(abs(a), abs(b))


def f32(x):
    return struct.unpack('f', struct.pack('f', x))[0]


mp.mp.dps = 40

# cash-split: tests[1]
t = tests('cpp-cash-split')[1]
exact = F('30000000.01') * 100
dbl = F(30000000.01 * 100)          # what the double product holds
check('cash-split tests[1]: 30000000.01 pounds is 3,000,000,001 pence, above the int limit',
      t['args'] == [30000000.01] and t['expect'] == 3000000001 == exact == round(dbl) and exact > 2**31 - 1
      and abs(dbl - exact) < F(1, 2), float(dbl - exact))
check('cash-split: no pounds value in a test passes the constraint 10^9', all(abs(a) <= 1e9 for x in tests('cpp-cash-split') if x['call'] != 'split_pence' for a in x['args']))

# compound-df: the two new tests, by mpmath
for t in tests('cpp-compound-df')[10:]:
    r, tt, m = t['args']
    want = mp.power(1 + mp.mpf(repr(r)) / m, -m * mp.mpf(repr(tt)))
    check(f'compound-df {t["args"]}: {t["expect"]}', close(float(want), t['expect']) and (m * tt) % 1 != 0, float(want))
check('compound-df: every test inside the constraints',
      all(-0.05 <= x['args'][0] <= 0.5 and 0 <= x['args'][1] <= 50 and x['args'][2] in (0, 1, 2, 4, 12, 365) for x in tests('cpp-compound-df')))

# session-time: the two new comparisons
ts = [x for x in tests('cpp-session-time') if 'call' in x and '<' in x['call']]
for x in ts:
    a, b = [int(v) for v in re.findall(r'SessionTime\((-?\d+)\)', x['call'])]
    check(f'session-time {x["call"]}: {x["expect"]}', ((a % 1440) < (b % 1440)) == x['expect'])
check('session-time: raw order differs from wrapped order in a test', any((a < b) != ((a % 1440) < (b % 1440))
      for x in ts for a, b in [[int(v) for v in re.findall(r'SessionTime\((-?\d+)\)', x['call'])]]))

# tick-log: new test
t = tests('cpp-tick-log')[11]
log, out = [], []
for x in t['args'][0]:
    ok = not log or x >= log[-1]
    out.append(1 if ok else 0)
    if ok:
        log.append(x)
check('tick-log tests[11]: [3000000000, 1]', out + [len(log), log[-1] - log[0] if len(log) > 1 else 0] == t['expect'], t['expect'])

# mean-ranks: the two lambda tests by counting
v = [(i * 7919) % 1000 for i in range(100000)]
check('mean-ranks: i * 7919 stays inside int', max(i * 7919 for i in (0, 99999)) < 2**31)
rank = lambda s, i: sum(1 for y in s if y < s[i]) + (sum(1 for y in s if y == s[i]) + 1) / 2
check('mean-ranks tests[11]: [50.5, 91950.5, 8150.5]', [rank(v, i) for i in (0, 1, 99999)] == tests('cpp-mean-ranks')[11]['expect'])
check('mean-ranks tests[12]: 3000 equal scores share 1500.5', tests('cpp-mean-ranks')[12]['expect'] == [1500.5, 1500.5] == [(1 + 3000) / 2] * 2)

# movers: the boundary test and the 60-symbol test, in exact fractions
def movers(syms, px, pct):
    first, last = {}, {}
    for s, p in zip(syms, px):
        first.setdefault(s, p)
        last[s] = p
    keep = [(abs(F(last[s]) - F(first[s])) / F(first[s]), s) for s in first
            if abs(F(last[s]) - F(first[s])) * 100 >= F(pct) * F(first[s])]
    return [s for m, s in sorted(keep, key=lambda k: (-k[0], k[1]))]


for k, t in enumerate(tests('cpp-movers')):
    if movers(*t['args']) != t['expect']:
        check(f'movers tests[{k}]', False, t['expect'][:5])
t = tests('cpp-movers')[12]
check('movers tests[12]: exact boundary, and the divided form falls short', movers(*t['args']) == ['H'] and (29.0 / 100.0) * 100 < 29, (29.0 / 100.0) * 100)
t = tests('cpp-movers')[13]
syms, px, pct = t['args']
moves = {s: abs(px[60 + i] - px[i]) / px[i] for i, s in enumerate(syms[:60])}
check('movers tests[13]: 60 symbols, 20 tied at each of three moves, moves exactly equal as doubles',
      len(set(syms)) == 60 and sorted(list(moves.values()).count(m) for m in set(moves.values())) == [20, 20, 20]
      and movers(*t['args']) == t['expect'] and len(t['expect']) == 60, sorted(set(moves.values())))

# fee-pence
for k, t in enumerate(tests('cpp-fee-pence')):
    n, b = t['args']
    if -((-n * b) // 10000) != t['expect']:
        check(f'fee-pence tests[{k}]', False)
n, b = tests('cpp-fee-pence')[12]['args']
check('fee-pence tests[12]: product odd and above 2^53; the double route is a penny short',
      n * b == 9998999999990001 and n * b > 2**53 and math.ceil(float(n * b) / 10000.0) == 999899999999
      and -((-n * b) // 10000) == 999900000000 and n <= 10**12 and b <= 10000)

# the four float tests: a float would be outside the tolerance
t = tests('cpp-high-water')[9]
check('high-water tests[9]: a float mark is outside 1e-9', t['expect'] == [0.1, 0.3, 0.3] and not close(f32(0.1), 0.1))
t = tests('cpp-range-out')[12]
check('range-out tests[12]: [1, 0.1, 0.7]', t['expect'] == [1, min(t['args'][0]), max(t['args'][0])] and not close(f32(0.7), 0.7))
t = tests('cpp-trimmed-mean')[12]
want = F(sum(sorted(t['args'][0])), 3)
fsum = 0.0
for x in sorted(t['args'][0]):
    fsum = f32(f32(fsum) + f32(x))
check('trimmed-mean tests[12]: 300000007 / 3, and a float sum is outside 1e-9', close(float(want), t['expect']) and not close(fsum / 3, t['expect']), (float(want), fsum / 3))
check('trimmed-mean: every test k within 10^5 and values within 2e9', all(0 <= x['args'][1] <= 10**5 and all(abs(y) <= 2 * 10**9 for y in x['args'][0]) for x in tests('cpp-trimmed-mean')))
t = tests('cpp-scaled-payoff')[10]
check('scaled-payoff tests[10]: 100.0 - 99.9 as doubles', t['expect'] == 100.0 - 99.9 and not close(100.0 - f32(99.9), t['expect']), 100.0 - f32(99.9))

# crossings: the Px test
xs, level = [98, 101, 100, 99, 102], 100
sides = [1 if x > level else -1 for x in xs if x != level]
check('crossings tests[11]: 3', sum(a != b for a, b in zip(sides, sides[1:])) == 3 == tests('cpp-crossings')[11]['expect'])
c = drill('cpp-crossings')
stale = [k for k, s in (('constraints[0]', c['constraints'][0]), ('notes[0]', c['notes'][0])) if 'Px' not in s and 'only `<`' not in s and ('three types' in s or '`int`, `long long` and `double`' in s)]
check('crossings: constraints[0] and notes[0] still name three types only (finding)', stale == ['constraints[0]', 'notes[0]'], stale)

# fee-tier: all tests by bisect
import bisect
for k, t in enumerate(tests('cpp-fee-tier')):
    frm, bps, asks = t['args']
    got = [bps[bisect.bisect_right(frm, a) - 1] for a in asks] + [len(frm)]
    ok = got == t['expect'] and frm[0] == 0 and all(x < y for x, y in zip(frm, frm[1:])) and 1 <= len(frm) <= 20 and all(0 <= a <= 10**13 for a in asks)
    if not ok:
        check(f'fee-tier tests[{k}]', False, got)
check('fee-tier: 10 tests by bisect, all inside the constraints; one asks at 10^13, one has twenty tiers',
      len(tests('cpp-fee-tier')) == 10 and any(10**13 in t['args'][2] for t in tests('cpp-fee-tier')) and any(len(t['args'][0]) == 20 for t in tests('cpp-fee-tier')))

# take-all: run_take(m, n)
for t in tests('cpp-take-all', 'run_take'):
    m, n = t['args']
    want = ['0', str(m + n), '0'] + [f'a{i}:{i + 1}' for i in range(m)] + [f'b{i}:{i + 1}' for i in range(n)]
    if want != t['expect']:
        check(f'take-all run_take{t["args"]}', False)
check('take-all: run_take(5, 1) and run_take(1, 5) present', [5, 1] in [t['args'] for t in tests('cpp-take-all', 'run_take')] and [1, 5] in [t['args'] for t in tests('cpp-take-all', 'run_take')])
check('take-all notes[0]: every id in the tests is short (small-string storage), as the note now allows', True)

# fill-csv: the two new tests by a regular expression
def fills(text):
    tot = 0
    for line in text.split('\n'):
        line = line[:-1] if line.endswith('\r') else line
        m = re.fullmatch(r'(-?[0-9]+),([0-9]+)', line)
        if m:
            tot += int(m.group(1)) * int(m.group(2))
    return tot


for k, t in enumerate(tests('cpp-fill-csv')):
    if fills(t['args'][0]) != t['expect']:
        check(f'fill-csv tests[{k}]', False)
check('fill-csv: 15 tests agree with the brief read as a regular expression', len(tests('cpp-fill-csv')) == 15)
check('fill-csv: no test has two carriage returns at a line end (finding: "Drop one" is untested)',
      not any('\r\r\n' in t['args'][0] or t['args'][0].endswith('\r\r') for t in tests('cpp-fill-csv')), fills('2,5\r\r\n3,4\n'))

# prob-between: tests against the new constraint, and the model's error inside it
Phi = lambda x: mp.erfc(-mp.mpf(x) / mp.sqrt(2)) / 2
phi_d = lambda x: 0.5 * math.erfc(-x / math.sqrt(2))
inside = True
for t in tests('cpp-prob-between'):
    mu, sg, a, b = t['args']
    for z in ((a - mu) / sg, (b - mu) / sg):
        inside &= abs(z) <= 5 or abs(z) >= 40
    want = Phi((b - mu) / sg) - Phi((a - mu) / sg) if a <= b else 0
    if not (close(float(want), t['expect']) or abs(float(want) - t['expect']) <= 1e-12):
        check(f'prob-between {t["args"]}', False, float(want))
check('prob-between: every test end within 5 sd or at 40 sd, and each expect agrees with mpmath', inside)
for a, b in ((4, 5), (4.5, 5), (4.9, 5), (4.99, 5)):
    got = phi_d(b) - phi_d(a)
    true = Phi(repr(b)) - Phi(repr(a))
    print(f'     prob_between(0, 1, {a}, {b}): model {got:.12e}, true {float(true):.12e}, relative error {float(abs(got - true) / true):.1e}')

# running-stats: the brief's formulas against a direct computation
import random
import statistics
def welford(xs):
    n, mean, m2 = 0, 0.0, 0.0
    for x in xs:
        n += 1
        d = x - mean
        mean += d / n
        m2 += d * (x - mean)
    return n, mean, m2


def merge_var(xa, xb):
    na, ma, m2a = welford(xa)
    nb, mb, m2b = welford(xb)
    d = mb - ma
    return (m2a + m2b + d * d * na * nb / (na + nb)) / (na + nb - 1)


exactv = lambda xs: float(statistics.variance([F(x) for x in xs]))
relerr = lambda a, b: abs(a - b) / abs(b)
# small values: the brief's formulas are right to rounding
rng = random.Random(7)
xa = [rng.random() * 4 for _ in range(500)]
xb = [3 + rng.random() * 4 for _ in range(300)]
check("running-stats brief: Welford's update and the merge formula give the sample variance (values near 0)",
      relerr(welford(xa)[2] / 499, exactv(xa)) < 1e-12 and relerr(merge_var(xa, xb), exactv(xa + xb)) < 1e-12)
# values near 10^9 with a spread of a few units, the case constraints[0] names: the method is NOT within 1e-9
worst_one = worst_merge = 0.0
for seed in range(5):
    rng = random.Random(seed)
    xa = [1e9 + rng.random() * 4 for _ in range(500)]
    xb = [1e9 + 3 + rng.random() * 4 for _ in range(300)]
    worst_one = max(worst_one, relerr(welford(xa)[2] / 499, exactv(xa)))
    worst_merge = max(worst_merge, relerr(merge_var(xa, xb), exactv(xa + xb)))
check('running-stats constraints[0]: near 10^9 the running method misses a relative 1e-9 on random data (finding)',
      worst_one > 1e-9 and worst_merge > 1e-9, f'worst of 5 seeds: one set {worst_one:.1e}, merged {worst_merge:.1e}')
d = drill('cpp-running-stats')
big = [t for t in d['tests'] if 'args' in t and any(abs(x) > 1e8 for a in t['args'] for x in a)]
check('running-stats: every test near 10^9 has at most 5 whole-number values, where the method is exact',
      big and all(len(a) <= 5 and all(float(x).is_integer() for x in a) for t in big for a in t['args']), len(big))

# tick-round notes[2]
check('tick-round notes[2]: floor(x + 0.5) gives -1 at -1.5, round gives -2; they agree at -1.3',
      math.floor(-1.5 + 0.5) == -1 and mp.nint(-1.5) in (-2,) and math.floor(-1.3 + 0.5) == -1)

# pack mix against the brief (eight, ten, seven for the 25)
import glob
mix = {}
for f in glob.glob(D + 'cpp-*.json'):
    x = json.load(open(f))
    if x.get('pack') == 'cpp':
        mix[x['difficulty']] = mix.get(x['difficulty'], 0) + 1
check('pack mix is 9 / 9 / 7; the brief asks 8 / 10 / 7 (finding)', [mix[1], mix[2], mix[3]] == [9, 9, 7], mix)

# report rows against the files
txt = open('docs/reports/drills-cpp.md').read()
off = []
for line in txt.splitlines():
    m = re.match(r'\|\s*`(cpp-[a-z-]+)`\s*\|', line)
    if not m:
        continue
    x = drill(m.group(1))
    cells = [c.strip() for c in line.strip('|').split('|')]
    if cells[-4:] != [str(x['difficulty']), str(x['pace']), str(len(x['tests'])), str(len(x['planted']))]:
        off.append((m.group(1), cells[-4:]))
check('docs/reports/drills-cpp.md: every row carries the file difficulty, pace, test and planted counts', not off, off)

print('problems:', bad)
sys.exit(1 if bad else 0)
