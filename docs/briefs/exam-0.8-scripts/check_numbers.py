"""Recompute every number stated in app/content/exams/topic-0.8.json by a second route and assert it at its path.

Route A is build.py (plain floats and loops). Route B here is independent: exact Fractions, Decimal money, brute-force
enumeration of neuron patterns and biases, Counter tables parsed from the item's own prose, and both code items run in
CPython (the solution passes every hidden test, the starter fails every one, each mutant first fails its named test,
and a second implementation written with Fractions gives every expected value). Exits 1 on any failure.
Run: python3 docs/briefs/exam-0.8-scripts/check_numbers.py
"""
import json
import math
import os
import re
import signal
import sys
from collections import Counter
from decimal import Decimal as D, ROUND_HALF_UP
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', '..', 'app', 'tools'))
from numbers_lib import Level, _walk  # noqa: E402

EXAM = os.path.join(HERE, '..', '..', '..', 'app', 'content', 'exams', 'topic-0.8.json')


class Exam(Level):
    """numbers_lib's Level, pointed at one exam file (ref "exam")."""

    def __init__(self, path):
        self.course, self.n, self.results = 'exam', 0, []
        with open(path, encoding='utf8') as f:
            self.files = {'exam': json.load(f)}


ex = Exam(EXAM)
doc = ex.files['exam']
items = doc['items']
idx = {it['id']: k for k, it in enumerate(items)}


def P(iid, part=None):
    base = f'items[{idx[iid]}]'
    return base if part is None else f'{base}.parts[{part}]'


def W(iid, part=None):
    return P(iid, part) + '.widget'


def node(path):
    return _walk(doc, path)[0]


def key(iid, value, part=None, nd=None):
    w = node(W(iid, part))
    v = float(value)
    want = round(v, nd) if nd is not None else v
    ok = abs(w['answer'] - want) <= 1e-9 and abs(w['answer'] - v) <= w['tol']['abs'] + 1e-12
    ex._rec(ok, f'{iid}{"" if part is None else f" part {part}"} answer {w["answer"]!r} = {want!r}', '' if ok else 'route B differs')


CHECKED = set()


def wrong(iid, wid, value, part=None):
    CHECKED.add((iid, part, wid))
    w = node(W(iid, part))
    hit = [x for x in w['wrong'] if x['id'] == wid]
    ok = len(hit) == 1 and abs(hit[0]['value'] - float(value)) <= max(hit[0]['tol']['abs'], 1e-9)
    ex._rec(ok, f'{iid} wrong "{wid}" = {float(value)!r}', '' if ok else f'found {hit}')


def say(iid, path, value, part=None, fmt=None):
    ex.expect('exam', f'{P(iid, part)}.{path}', value, fmt=fmt)


def correct_id(iid, part=None):
    return [o['id'] for o in node(W(iid, part))['options'] if o.get('correct')]


def mse(w, b, xs, ys):
    return sum((F(w) * x + F(b) - y) ** 2 for x, y in zip(xs, ys)) / len(xs)


def money(x):
    return D(x).quantize(D('0.01'), rounding=ROUND_HALF_UP)


def fires(ws, xs, b):
    return 1 if sum(F(w) * x for w, x in zip(ws, xs)) + F(b) > 0 else 0


CORNERS = [(0, 0), (0, 1), (1, 0), (1, 1)]

# ------------------------------------------------------------------ difficulty 2
# e-mse-three-points: y = 3x - 1 on (1, 4), (2, 4), (4, 12)
pts = [(1, 4), (2, 4), (4, 12)]
errs = [3 * x - 1 - y for x, y in pts]
sq = sum(e * e for e in errs)
key('e-mse-three-points', F(sq, 3))
wrong('e-mse-three-points', 'sum', sq)
wrong('e-mse-three-points', 'raw', round(F(sum(errs), 3), 4))
wrong('e-mse-three-points', 'n-minus-1', F(sq, 2))
for v in (2, 5, 11, -2, 6):
    say('e-mse-three-points', 'explain.text', v)

# e-four-input-sum
wts, xin, b = [F(3, 2), F(-1, 2), F(2), F(-1)], [1, 0, 1, 1], F(-3, 2)
s = sum(w * x for w, x in zip(wts, xin)) + b
key('e-four-input-sum', s)
wrong('e-four-input-sum', 'no-bias', s - b)
wrong('e-four-input-sum', 'zero-input', sum(wts) + b)
say('e-four-input-sum', 'explain.text', 2.5)

# e-pick-buy: running totals 0.45, 0.75, 1
run = [F(45, 100), F(75, 100), F(1)]
u = F(52, 100)
pick = ['hold', 'buy', 'sell'][next(k for k, t in enumerate(run) if u < t)]
ex._rec(correct_id('e-pick-buy') == [pick], f'e-pick-buy key is {pick}', '')
say('e-pick-buy', 'explain.text', 0.75)

# ------------------------------------------------------------------ difficulty 3
# e-always-no
acc = F(2000 - 60, 2000)
key('e-always-no', acc)
wrong('e-always-no', 'flipped', F(60, 2000))
say('e-always-no', 'feedback.correct', 1940)
say('e-always-no', 'feedback.byKey.flipped', 3)

# e-round-by-hand: points (0, 1), (1, 3), (2, 4), start (1, 1), step 1/2
xs2, ys2 = [0, 1, 2], [1, 3, 4]
m0 = mse(1, 1, xs2, ys2)
mwu, mwd = mse(F(3, 2), 1, xs2, ys2), mse(F(1, 2), 1, xs2, ys2)
w_after = F(3, 2) if mwu < m0 and mwu <= mwd else (F(1, 2) if mwd < m0 else F(1))
mbu, mbd = mse(w_after, F(3, 2), xs2, ys2), mse(w_after, F(1, 2), xs2, ys2)
b_after = F(3, 2) if mbu < mwu and mbu <= mbd else (F(1, 2) if mbd < mwu else F(1))
key('e-round-by-hand', m0, part=0, nd=4)
wrong('e-round-by-hand', 'sum', m0 * 3, part=0)
key('e-round-by-hand', w_after, part=1)
key('e-round-by-hand', b_after, part=2)
ex._rec(min(mbu, mbd) == mbu and mbu > mwu, 'e-round-by-hand: b = 1.5 is the better trial but above the MSE after the w nudge', '')
for v in (mwu, mwd):
    say('e-round-by-hand', 'feedback.correct', round(float(v), 4), part=1)
for v in (mbu, mbd, mwu):
    say('e-round-by-hand', 'explain.text', round(float(v), 4))
say('e-round-by-hand', 'feedback.byKey.better-trial', round(float(mbu), 4), part=2)
say('e-round-by-hand', 'feedback.byKey.down', round(float(mbd), 4), part=2)

# e-mse-tie
A, B = [1, 1, 1, 1, 4], [2] * 5
ex._rec(F(sum(a * a for a in A), 5) == F(sum(x * x for x in B), 5) == 4, 'e-mse-tie: both MSEs are 4', '')
ex._rec(sum(A) == 8 and sum(B) == 10 and sum(a * a for a in A) == 20, 'e-mse-tie: raw totals 8 and 10, squares 20', '')
ex._rec(correct_id('e-mse-tie') == ['tie'], 'e-mse-tie key is the tie', '')

# e-alarm-neuron: weights 1.5, -2, 1, bias -1
wa, ba = [F(3, 2), F(-2), F(1)], F(-1)
pats = [(p, q, r) for p in (0, 1) for q in (0, 1) for r in (0, 1)]
sums = {p: sum(w * x for w, x in zip(wa, p)) + ba for p in pats}
key('e-alarm-neuron', sums[(0, 0, 1)], part=0)
key('e-alarm-neuron', fires(wa, (0, 0, 1), ba), part=1)
nfire = sum(fires(wa, p, ba) for p in pats)
key('e-alarm-neuron', nfire, part=2)
wrong('e-alarm-neuron', 'with-zero', sum(1 for p in pats if sums[p] >= 0), part=2)
ex._rec(sorted(float(sums[p]) for p in pats if sums[p] > 0) == [0.5, 1.5], 'e-alarm-neuron: firing sums 0.5 and 1.5', '')

# e-neither-neuron: each option's truth table
want = [1, 0, 0, 0]
opts = {'nor': (-2, -2, 1), 'nand': (-2, -2, 3), 'or': (2, 2, -1), 'never': (-2, -2, -1)}
tables = {k: [fires(v[:2], c, v[2]) for c in CORNERS] for k, v in opts.items()}
ex._rec([k for k, t in tables.items() if t == want] == correct_id('e-neither-neuron'), 'e-neither-neuron: only the key computes neither', '')
ex._rec([sum(w * x for w, x in zip(opts['nand'][:2], c)) + 3 for c in CORNERS] == [3, 1, 1, -1], 'nand sums 3, 1, 1, -1', '')
ex._rec([sum(w * x for w, x in zip(opts['never'][:2], c)) - 1 for c in CORNERS] == [-1, -3, -3, -5], 'never sums -1, -3, -3, -5', '')
ex._rec([sum(w * x for w, x in zip(opts['nor'][:2], c)) + 1 for c in CORNERS] == [1, -1, -1, -3], 'nor sums 1, -1, -1, -3', '')

# e-sell-row: parse the log from the prose
logtxt = re.search(r'`([^`]+)`', node(P('e-sell-row') + '.prose')).group(1).split()
cnt = Counter(zip(logtxt, logtxt[1:]))
row_total = sum(c for (a, _), c in cnt.items() if a == 'sell')
key('e-sell-row', F(cnt[('sell', 'buy')], row_total), nd=4)
wrong('e-sell-row', 'all-sells', F(cnt[('sell', 'buy')], logtxt.count('sell')))
wrong('e-sell-row', 'all-pairs', round(F(cnt[('sell', 'buy')], len(logtxt) - 1), 4))
wrong('e-sell-row', 'words', F(cnt[('sell', 'buy')], len(logtxt)))
ex._rec(row_total == 3 and len(logtxt) - 1 == 7 and logtxt.count('sell') == 4, 'e-sell-row: 3 of 7 pairs start with sell, 4 sells', '')

# e-cold-three
c3 = [F(1, 2), F(3, 10), F(1, 5)]
sq3 = [c * c for c in c3]
cold = sq3[0] / sum(sq3)
key('e-cold-three', round(float(cold), 3))
ex._rec(abs(float(cold) - round(float(cold), 3)) < 0.0005, 'e-cold-three: rounded key within tol of exact', '')
roots = [D(c.numerator) / D(c.denominator) for c in c3]
roots = [x.sqrt() for x in roots]
hot = roots[0] / sum(roots)
wrong('e-cold-three', 'roots', round(float(hot), 3))
wrong('e-cold-three', 'no-rescale', sq3[0])
ex._rec(sum(sq3) == F(38, 100), 'e-cold-three: squares add to 0.38', '')
say('e-cold-three', 'explain.text', round(float(cold), 3))

# e-examples-two-docs: count (input, label) places by enumeration
n_ex = sum(sum(1 for k in range(n) if k >= 1) for n in (12, 30))
key('e-examples-two-docs', n_ex)
wrong('e-examples-two-docs', 'every-token', 12 + 30)
wrong('e-examples-two-docs', 'joined', sum(1 for k in range(42) if k >= 1))

# e-compound-check
bal = money(D(15000) * D('1.045') ** 3)
key('e-compound-check', bal)
wrong('e-compound-check', 'simple', money(D(15000) * (1 + 3 * D('0.045'))))
b4 = money(D(15000) * D('1.045') ** 4)
wrong('e-compound-check', 'four-years', b4)
say('e-compound-check', 'feedback.byKey.four-years', float(b4))
say('e-compound-check', 'explain.text', 13.5)
say('e-compound-check', 'explain.text', float(bal))

# e-unique-rows: parse the table from the prose
trows = re.findall(r'^\| \d+ \| (\w+) \| ([^|]+?) \|$', node(P('e-unique-rows') + '.prose'), re.M)
cc = Counter(trows)
key('e-unique-rows', sum(1 for r in trows if cc[r] == 1))
wrong('e-unique-rows', 'all', len(trows))
wrong('e-unique-rows', 'distinct', len(cc))
ex._rec(len(trows) == 7, 'e-unique-rows: 7 rows parsed', '')

# ------------------------------------------------------------------ difficulty 4
# e-signal-days
sx, sy = [1, 2, 2, 3, 4, 5, 5, 6], [0, 0, 1, 0, 1, 1, 0, 1]
tx, ty = [1, 3, 4, 6, 5], [0, 1, 1, 1, 0]


def right(xs, ys, t):
    return sum((x >= t) == (y == 1) for x, y in zip(xs, ys))


sc = {t: right(sx, sy, t) for t in range(8)}
tb = max(sc, key=lambda t: (sc[t], -t))
key('e-signal-days', tb, part=0)
ex._rec(sorted(sc.values())[-2] == 5 and sc[tb] == 6, 'e-signal-days: t = 4 gets 6, every other t 5 or fewer', '')
key('e-signal-days', F(sc[tb], 8), part=1)
wrong('e-signal-days', 'five', F(5, 8), part=1)
key('e-signal-days', F(right(tx, ty, tb), 5), part=2)
ex._rec(max(F(right(tx, ty, t), 5) for t in range(8)) == F(4, 5), 'e-signal-days: best t on the kept-back days gets 80%', '')
ex._rec((F(3, 4) + F(3, 5)) / 2 == F(675, 1000), 'e-signal-days: average of 75% and 60% is 67.5%', '')
ex._rec([x for x, y in zip(tx, ty) if (x >= 4) == (y == 1)] == [1, 4, 6], 'e-signal-days: right on signals 1, 4, 6', '')


# e-same-network
def same(x1, x2):
    return fires([2, 2], [fires([2, 2], [x1, x2], -3), fires([-2, -2], [x1, x2], 1)], -1)


key('e-same-network', 1 + 0 * 0, part=0)
ex._rec(sum(F(w) * x for w, x in zip([-2, -2], (0, 0))) + 1 == 1, 'h2 sum at (0, 0) is 1', '')
key('e-same-network', same(1, 0), part=1)
ex._rec([same(*c) for c in CORNERS] == [1, 0, 0, 1], 'e-same-network computes both-the-same', '')
ex._rec(2 * 1 + 2 * 0 - 3 == -1 and -2 * 1 - 2 * 0 + 1 == -1, 'e-same-network: h1 and h2 sum to -1 at (1, 0)', '')

# e-desk-bigram: parse the log, count, sample, score
dt = re.search(r'`([^`]+)`', node(P('e-desk-bigram') + '.prose')).group(1).split()
ex._rec(len(dt) == 12, 'e-desk-bigram: 12 words', '')
pairs = list(zip(dt, dt[1:]))


def row(word):
    order = []
    for a, bb in pairs:
        if a == word and bb not in order:
            order.append(bb)
    c = Counter(bb for a, bb in pairs if a == word)
    tot = sum(c.values())
    return [(x, F(c[x], tot)) for x in order]


key('e-desk-bigram', sum(1 for a, _ in pairs if a == 'the'), part=0)
key('e-desk-bigram', dict(row('the'))['rip'], part=1, nd=4)
wrong('e-desk-bigram', 'words', round(F(2, 12), 4), part=1)
w0, out = 'sell', ['sell']
for uu in (F(4, 10), F(5, 10), F(2, 10), F(7, 10)):
    t = F(0)
    for x, c in row(w0):
        t += c
        if uu < t:
            w0 = x
            break
    out.append(w0)
ex._rec(' '.join(out) == [o['text'] for o in node(W('e-desk-bigram', 2))['options'] if o.get('correct')][0], 'e-desk-bigram: sample matches key', '')
chain = ['sell', 'the', 'dip', '.', 'buy', 'the']
pc = F(1)
for a, bb in zip(chain, chain[1:]):
    pc *= dict(row(a))[bb]
key('e-desk-bigram', pc, part=3, nd=4)
ex._rec(' '.join(chain) not in ' '.join(dt), 'e-desk-bigram: the run is not in the log', '')

# e-pension-reply
key('e-pension-reply', 250 * 12 * 3, part=0)
ex._rec(7500 == 250 * 30, 'e-pension-reply: £7,500 is 30 months', '')
g = money(D(9000) * D('1.04') ** 10)
key('e-pension-reply', g, part=1)
wrong('e-pension-reply', 'simple', 9000 * (1 + F(4, 100) * 10), part=1)
say('e-pension-reply', 'explain.text', float(g))

# e-fewest-shortlisted
rE = F(117, 180)
kmin = min(k for k in range(201) if abs(rE - F(k, 200)) < F(5, 100))
key('e-fewest-shortlisted', kmin)
wrong('e-fewest-shortlisted', 'at-five', kmin - 1)
ex._rec(abs(rE - F(kmin - 1, 200)) == F(5, 100), 'e-fewest-shortlisted: 120 of 200 is exactly 5 points', '')
wrong('e-fewest-shortlisted', 'equal', rE * 200)
ex._rec(F(121, 200) == F(605, 1000) and rE == F(65, 100), 'e-fewest-shortlisted: 60.5% and 65%', '')
ex._rec((rE - F(117, 200)) * 100 == F(13, 2), 'e-fewest-shortlisted: 117 of 200 is 6.5 points below', '')

# e-profit-days
At = 19 * F(1, 2) - 15
Bt = 12 * 1 - 8 * F(1, 2)
key('e-profit-days', At, part=0)
wrong('e-profit-days', 'gains-only', 19 * F(1, 2), part=0)
wrong('e-profit-days', 'sign', -At, part=0)
key('e-profit-days', Bt, part=1)
wrong('e-profit-days', 'gains-only', 12, part=1)
wrong('e-profit-days', 'one-loss', 12 - F(1, 2), part=1)
say('e-profit-days', 'explain.text', 5.5)
say('e-profit-days', 'explain.text', 8)

# ------------------------------------------------------------------ difficulty 5
# e-two-of-three: biases on a grid of quarters from -10 to 10
wt = [2, 3, 4]
p3 = [(p, q, r) for p in (0, 1) for q in (0, 1) for r in (0, 1)]


def works(bb):
    return all(fires(wt, p, bb) == (1 if sum(p) >= 2 else 0) for p in p3)


key('e-two-of-three', min(sum(w * x for w, x in zip(wt, p)) for p in p3 if sum(p) >= 2), part=0)
key('e-two-of-three', max(sum(w * x for w, x in zip(wt, p)) for p in p3 if sum(p) < 2), part=1)
whole = [bb for bb in range(-20, 21) if works(bb)]
ex._rec(len(whole) == 1, 'e-two-of-three: one whole-number bias', '')
key('e-two-of-three', whole[0], part=2)
grid = [F(k, 8) for k in range(-80, 81)]
ok_grid = [bb for bb in grid if works(bb)]
ex._rec(min(ok_grid) == F(-39, 8) and max(ok_grid) == -4 and not works(F(-5)), 'e-two-of-three: the biases that work are (-5, -4]', '')
ex._rec(not works(F(-5)) and not works(F(-3)), 'e-two-of-three: -5 and -3 fail', '')


# ------------------------------------------------------------------ code items, run in CPython
class TO(Exception):
    pass


def _alarm(*a):
    raise TO()


signal.signal(signal.SIGALRM, _alarm)


def close(a, e):
    if isinstance(a, (list, tuple)):
        return isinstance(e, (list, tuple)) and len(a) == len(e) and all(close(x, y) for x, y in zip(a, e))
    if isinstance(a, str) or isinstance(e, str):
        return a == e
    return math.isclose(float(a), float(e), rel_tol=1e-9, abs_tol=1e-12)


def run_cases(src, tests):
    out = []
    for t in tests:
        ns = {}
        signal.setitimer(signal.ITIMER_REAL, 1.0)
        try:
            exec(src, ns)
            got = eval(t['call'], ns)
            want = eval(t['expect'])
            res = 'ok' if (close(got, want) if t['compare'] == 'isclose' else got == want) else 'fail'
        except TO:
            res = 'timeout'
        except Exception:
            res = 'error'
        finally:
            signal.setitimer(signal.ITIMER_REAL, 0)
        out.append(res)
    return out


def code_checks(iid):
    w = node(W(iid))
    sol = run_cases(w['solution'], w['tests'])
    ex._rec(all(r == 'ok' for r in sol), f'{iid}: solution passes all {len(sol)} hidden tests', str(sol))
    sol_ex = run_cases(w['solution'], w['examples'])
    ex._rec(all(r == 'ok' for r in sol_ex), f'{iid}: solution passes the examples', '')
    st = run_cases(w['starter'], w['tests'])
    ex._rec(all(r != 'ok' for r in st), f'{iid}: starter fails all {len(st)} hidden tests', str(st))
    ex._rec(f'runs {len(w["tests"])} hidden tests' in w['how'], f'{iid}: how names {len(w["tests"])} tests', '')
    for m in w['mutants']:
        res = run_cases(m['source'], w['tests'])
        first = next((k + 1 for k, r in enumerate(res) if r != 'ok'), None)
        kind = res[first - 1] if first else None
        ok = first == m['test'] and (kind == 'timeout') == bool(m.get('timeout'))
        ex._rec(ok, f'{iid}: mutant first fails test {m["test"]} ({m["symptom"][:40]})', str(res))
    return w


# fit_halving, route B: the same rule on exact Fractions
def fit_b(xs, ys):
    w, b = F(0), F(0)
    for step in (F(1), F(1, 2), F(1, 4), F(1, 8)):
        while True:
            old = (w, b)
            best = mse(w, b, xs, ys)
            cand = [(mse(w + step, b, xs, ys), w + step), (mse(w - step, b, xs, ys), w - step)]
            if cand[0][0] < best and cand[0][0] <= cand[1][0]:
                best, w = cand[0]
            elif cand[1][0] < best:
                best, w = cand[1]
            cand = [(mse(w, b + step, xs, ys), b + step), (mse(w, b - step, xs, ys), b - step)]
            if cand[0][0] < best and cand[0][0] <= cand[1][0]:
                best, b = cand[0]
            elif cand[1][0] < best:
                best, b = cand[1]
            if (w, b) == old:
                break
    return [float(w), float(b), round(float(mse(w, b, xs, ys)), 6)]


fw = code_checks('e-fit-halving')
for t in fw['tests'] + fw['examples']:
    m = re.fullmatch(r'list\(fit_halving\((\[[^\]]*\]), (\[[^\]]*\])\)\)', t['call'])
    xs, ys = json.loads(m.group(1)), [F(str(v)) for v in json.loads(m.group(2))]
    ex._rec(close(fit_b(xs, ys), eval(t['expect'])), f'fit_halving{m.group(1)} = {t["expect"]} by Fractions', '')
ex._rec(fit_b([0, 0], [1, 4])[1] == 2.5, 'fit_halving on x = 0 points settles at the mean, 2.5', '')


# sample_name, route B: Counter rows and exact running totals of chances
def sample_b(names, us, boundary):
    pairs = Counter()
    for nm in names:
        mk = '.' + nm + '.'
        pairs.update(zip(mk, mk[1:]))
    rows = {}
    for (a, bb), c in pairs.items():
        rows.setdefault(a, {})[bb] = c
    letter, out = '.', ''
    for u in us:
        r = rows[letter]
        tot = sum(r.values())
        uu = F(u)                                    # the exact binary value of the float the test passes
        run_t = F(0)
        for x in sorted(r):
            run_t += F(r[x], tot)
            gap = abs(F(str(u)) - run_t)
            if gap == 0:
                boundary.append((u, tot))
            elif gap < F(1, 10 ** 9):
                boundary.append(('near', u, tot))
            if uu < run_t:
                break
        if x == '.':
            break
        out += x
        letter = x
    return out


nw = code_checks('e-sample-name')
for t in nw['tests'] + nw['examples']:
    m = re.fullmatch(r'sample_name\((\[[^\]]*\]), (\[[^\]]*\])\)', t['call'])
    names, us = eval(m.group(1)), eval(m.group(2))
    bnd = []
    got = sample_b(names, us, bnd)
    ex._rec(got == eval(t['expect']), f'sample_name{m.group(1)} = {t["expect"]} by Counter and Fractions', '')
    ok = all(isinstance(x[0], float) and (x[1] & (x[1] - 1)) == 0 for x in bnd)
    ex._rec(ok, f'sample_name{m.group(1)}: every tie of u with a running total is exact in binary (u {sorted(set(x[0] for x in bnd if x[0] != "near"))})', str(bnd))
runs_out = [t for t in nw['tests'] if len(eval(t['expect'])) == len(eval(re.fullmatch(r'sample_name\((\[[^\]]*\]), (\[[^\]]*\])\)', t['call']).group(2)))]
ex._rec(len(runs_out) >= 1, f'sample_name: {len(runs_out)} hidden test(s) run out of draws before the end mark', '')


# ------------------------------------------------------------------ the remaining slips, each from its why
wrong('e-always-no', 'half', F(1, 2))
wrong('e-round-by-hand', 'stay', 1, part=1)
wrong('e-round-by-hand', 'down', F(1, 2), part=1)
wrong('e-round-by-hand', 'better-trial', F(3, 2), part=2)
wrong('e-round-by-hand', 'down', F(1, 2), part=2)
ex._rec(mwd > m0 and mbd > mwu, 'e-round-by-hand: the down trials raise the error', '')
wrong('e-alarm-neuron', 'no-bias', sums[(0, 0, 1)] - ba, part=0)
wrong('e-alarm-neuron', 'bias-only', ba, part=0)
wrong('e-alarm-neuron', 'zero-fires', 1, part=1)
wrong('e-alarm-neuron', 'half', len(pats) // 2, part=2)
wrong('e-cold-three', 'same', c3[0])
wrong('e-unique-rows', 'none', 0)
wrong('e-signal-days', 'middle', 3, part=0)
ex._rec(sc[3] == 5, 'e-signal-days: t = 3 gets 5', '')
wrong('e-signal-days', 'train', F(3, 4), part=2)
wrong('e-same-network', 'weights', -2 - 2 + 1, part=0)
wrong('e-same-network', 'one', 1 - same(1, 0), part=1)
ex._rec(fires([2, 2], [1, 0], -1) == 1, 'e-same-network: OR of the raw inputs at (1, 0) would give 1', '')
wrong('e-desk-bigram', 'dip-rip', len(row('the')), part=0)
wrong('e-desk-bigram', 'half', F(1, len(row('the'))), part=1)
wrong('e-desk-bigram', 'not-in-text', 0, part=3)
wrong('e-desk-bigram', 'one-step', round(dict(row('the'))['dip'], 4), part=3)
ex._rec(dict(row('.'))['buy'] == F(1, 2) and dict(row('the'))['dip'] == F(1, 3), 'e-desk-bigram: the . to buy step is 1/2, the to dip 1/3', '')
wrong('e-pension-reply', 'chatbot', 7500, part=0)
wrong('e-pension-reply', 'one-year', 250 * 12, part=0)
wrong('e-fewest-shortlisted', 'same-count', 117)
wrong('e-two-of-three', 'all-three', sum(wt), part=0)
wrong('e-two-of-three', 'smallest-single', min(wt), part=0)
wrong('e-two-of-three', 'none-on', 0, part=1)
wrong('e-two-of-three', 'pair', 2 + 3, part=1)
wrong('e-two-of-three', 'zero-fires', -5, part=2)
wrong('e-two-of-three', 'too-high', -3, part=2)
wrong('e-two-of-three', 'sign', -whole[0], part=2)
ex._rec(all(fires(wt, p, 4) for p in p3), 'e-two-of-three: bias 4 makes every pattern fire', '')
ex._rec(not fires(wt, (1, 1, 0), -5) and fires(wt, (0, 0, 1), -3), 'e-two-of-three: -5 silences (1, 1, 0), -3 fires the single 4', '')
ex._rec(not works(F(-6)) and works(F(-9, 2)), 'e-two-of-three: below -5 fails, -4.5 works', '')

# every numeric wrong[] in the exam was recomputed above
allw = set()
for it in items:
    for k, host in ([(None, it)] if 'widget' in it else list(enumerate(it.get('parts', [])))):
        for x in host['widget'].get('wrong', []):
            allw.add((it['id'], k, x['id']))
ex._rec(allw <= CHECKED, f'every one of the {len(allw)} numeric slips is recomputed', str(sorted(allw - CHECKED)))

ex.check_wrongs()
ex.report()
