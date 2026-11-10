"""Recompute every number in app/content/courses/markov/problems-<n>.json twice.

Method 1 is exact (fractions.Fraction: matrix products, closed forms, first-step
equations solved by hand). Method 2 is independent: numpy matrix powers and linear
solves, path enumeration, truncated series or a seeded simulation. For each numeric
part the script checks that
  - the two methods agree, and the JSON key equals them within the part's tol;
  - every `wrong` value matches its named slip and lies outside the key's band,
    and no two `wrong` bands overlap;
  - the value printed in `feedback.correct` (the first number after its last `=` or
    `\\approx`) is accepted by the part's own tol;
  - where the question hands the learner a rounded value, the answer that rounded
    value gives is accepted too;
  - the question states the form it wants (a sentence starting "Give").
Choice parts check the keyed option. Exit 0 when all pass.

Run: <scratchpad>/venv/bin/python docs/reports/problems-markov-numbers.py
"""
import json, os, re, sys, itertools
from fractions import Fraction as F
from math import isclose
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
COURSE = os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'markov')
fails, checks = [], 0


def load(n):
    p = os.path.join(COURSE, f'problems-{n}.json')
    if not os.path.exists(p):
        return None
    d = json.load(open(p))
    return {it['id']: it for it in d['items']}


def ok(cond, msg):
    global checks
    checks += 1
    if not cond:
        fails.append(msg)


NUM = re.compile(r'[-−]?\d+(?:\.\d+)?')


def printed(text):
    """First number after the last '=' or '\\approx' in a feedback line."""
    cut = max(text.rfind('='), text.rfind('\\approx'))
    tail = text[cut:] if cut >= 0 else text
    tail = tail.replace('\\approx', '').replace('£', '')
    m = NUM.search(tail)
    if not m:
        return None
    return float(m.group(0).replace('−', '-'))


def num(items, iid, k, exact, alt, slips=None, routes=()):
    """Part k (1-based) of item iid: a numeric key. routes: values a learner gets
    from rounded inputs the question gives; each must be accepted."""
    if items is None:
        return
    part = items[iid]['parts'][k - 1]
    w = part['widget']
    tag = f'{iid} p{k}'
    ok(w['kind'] == 'numeric', f'{tag}: not numeric')
    e = float(exact)
    ok(isclose(e, float(alt), rel_tol=1e-6, abs_tol=1e-9), f'{tag}: methods differ {e} vs {float(alt)}')
    tol = w['tol']['abs']
    ok(abs(w['answer'] - e) <= tol + 1e-9, f'{tag}: key {w["answer"]} vs computed {e} (tol {tol})')
    ok('Give' in part['question'], f'{tag}: no form sentence')
    pv = printed(part['feedback']['correct'])
    ok(pv is not None and abs(pv - w['answer']) <= tol + 1e-9,
       f'{tag}: printed value {pv} not accepted (key {w["answer"]}, tol {tol})')
    for r in routes:
        ok(abs(float(r) - w['answer']) <= tol + 1e-9, f'{tag}: rounded route {float(r)} not accepted')
    slips = slips or {}
    wrongs = {x['id']: x for x in w.get('wrong', [])}
    ok(set(wrongs) == set(slips), f'{tag}: wrong ids {sorted(wrongs)} vs slips {sorted(slips)}')
    for wid, val in slips.items():
        if wid not in wrongs:
            continue
        x = wrongs[wid]
        wt = x['tol']['abs']
        ok(abs(x['value'] - float(val)) <= max(wt, 0.00005) + 1e-9, f'{tag}: wrong {wid} {x["value"]} vs slip {float(val)}')
        ok(abs(x['value'] - w['answer']) > tol + wt, f'{tag}: wrong {wid} {x["value"]} inside the key band')
        ok(abs(float(val) - e) > tol, f'{tag}: slip {wid} equals the answer')
    for a, b in itertools.combinations(list(wrongs), 2):
        A, B = wrongs[a], wrongs[b]
        ok(abs(A['value'] - B['value']) > A['tol']['abs'] + B['tol']['abs'], f'{tag}: wrongs {a} and {b} overlap')
    ok(set(part['feedback'].get('byKey', {})) == set(wrongs), f'{tag}: byKey keys differ from wrong ids')


def pick(items, iid, k, correct_id):
    if items is None:
        return
    w = items[iid]['parts'][k - 1]['widget']
    keyed = [o['id'] for o in w['options'] if o.get('correct')]
    ok(keyed == [correct_id], f'{iid} p{k}: keyed {keyed}, expected {correct_id}')
    ok(all(o.get('why') for o in w['options'] if not o.get('correct')), f'{iid} p{k}: a distractor has no why')


def canvas_matrix(items, iid, rows):
    if items is None:
        return
    got = items[iid]['canvas']['params']['matrices'][0]['rows']
    ok(np.allclose(np.array(got, float), np.array([[float(x) for x in r] for r in rows])), f'{iid}: canvas matrix differs')
    for r in rows:
        ok(sum(r) == 1, f'{iid}: a row does not add to 1')


# exact helpers
def mmul(A, B):
    return [[sum(A[i][m] * B[m][j] for m in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]


def mpow(P, k):
    R = [[F(int(i == j)) for j in range(len(P))] for i in range(len(P))]
    for _ in range(k):
        R = mmul(R, P)
    return R


def npow(P, k):
    return np.linalg.matrix_power(np.array([[float(x) for x in r] for r in P]), k)


def geo_mean_series(p, N=4000):
    """Mean of a geometric run length, summed directly: sum n p^(n-1)(1-p)."""
    p = float(p)
    return sum(n * p ** (n - 1) * (1 - p) for n in range(1, N))


def stationary_np(P):
    A = np.array([[float(x) for x in r] for r in P])
    vals, vecs = np.linalg.eig(A.T)
    v = np.real(vecs[:, np.argmin(abs(vals - 1))])
    return v / v.sum()


# ------------------------------------------------------------------ level 1
L1 = load(1)

# p-thin-book: counts DD 34, DT 6, TD 6, TT 14
DD, DT, TD, TT = 34, 6, 6, 14
pTT, pDD = F(TT, TD + TT), F(DD, DD + DT)
seq_moves = DD + DT + TD + TT
num(L1, 'p-thin-book', 1, pTT, 1 - F(TD, TT + TD),
    {'of-all': F(TT, seq_moves), 'over-stays': F(TT, TT + DD), 'into-d': F(TD, TD + DT)})
P = [[pDD, 1 - pDD], [1 - pTT, pTT]]          # order D, T
num(L1, 'p-thin-book', 2, mpow(P, 2)[1][1], npow(P, 2)[1][1],
    {'stay-path': pTT ** 2, 'd-stays': pTT ** 2 + (1 - pTT) * pDD, 'row-twice': pTT ** 2 + (1 - pTT) ** 2})
num(L1, 'p-thin-book', 3, 1 / (1 - pTT), geo_mean_series(pTT),
    {'used-stay': 1 / pTT, 'further': pTT / (1 - pTT), 'two-step': 1 / (1 - mpow(P, 2)[1][1])})
mT, mD = 1 / (1 - pTT), 1 / (1 - pDD)
num(L1, 'p-thin-book', 4, mT / (mT + mD), stationary_np(P)[1],
    {'equal': F(1, 2), 'swapped': mD / (mT + mD), 'stay-ratio': pTT / (pTT + pDD)},
    routes=[F('3.33') / (F('6.67') + F('3.33'))])
ok(F(TD + TT, seq_moves) == mT / (mT + mD), 'p-thin-book: record share 20/60 differs from 1/3')

# p-two-losses: order W, L, S
P2 = [[F(7, 10), F(3, 10), F(0)], [F(4, 10), F(0), F(6, 10)], [F(0), F(0), F(1)]]
canvas_matrix(L1, 'p-two-losses', P2)
W, L, S = 0, 1, 2


def paths_stop(n):
    """Enumerate win/loss sequences of n trades from W; return chance stopped by trade n
    and chance of stopping exactly on trade n."""
    # Play all n trades as if she never stopped; the stop depends only on the prefix,
    # so the first LL in the sequence is the trade she would have stopped on.
    by, exact_n = 0.0, 0.0
    for seq in itertools.product('WL', repeat=n):
        pr, prev, first = 1.0, 'W', None
        for t, r in enumerate(seq, 1):
            pw = 0.7 if prev == 'W' else 0.4
            pr *= pw if r == 'W' else 1 - pw
            if first is None and r == 'L' and prev == 'L' and t > 1:
                first = t
            prev = r
        if first is not None:
            by += pr
            if first == n:
                exact_n += pr
    return by, exact_n


num(L1, 'p-two-losses', 1, F(3, 10) * F(4, 10) * F(3, 10) * F(6, 10), 0.3 * 0.4 * 0.3 * 0.6,
    {'iid': F(3, 10) * F(7, 10) * F(3, 10) * F(3, 10), 'last-loss': F(3, 10) * F(4, 10) * F(3, 10) * F(3, 10),
     'win-after-loss': F(3, 10) * F(7, 10) * F(3, 10) * F(6, 10)})
R2 = mpow(P2, 2)
ok(R2[W] == [F(61, 100), F(21, 100), F(18, 100)], 'p-two-losses: row W of P^2')
num(L1, 'p-two-losses', 2, R2[W][S], paths_stop(2)[0],
    {'loss-squared': F(9, 100), 'one-step': F(6, 10), 'path-l': R2[W][L]})
R3 = mpow(P2, 3)
num(L1, 'p-two-losses', 3, R3[W][S], paths_stop(3)[0],
    {'new-only': R2[W][L] * F(6, 10), 'no-step': R2[W][L] + R2[W][S], 'loss-low': R2[W][S] + R2[W][L] * F(3, 10)})
R4 = mpow(P2, 4)
num(L1, 'p-two-losses', 4, R4[W][S] - R3[W][S], paths_stop(4)[1],
    {'cumulative': R4[W][S], 'trade-three': R2[W][L] * F(6, 10), 'from-w': R2[W][W] * F(6, 10)})
ok(R3[W][L] * F(6, 10) == R4[W][S] - R3[W][S], 'p-two-losses: two routes to trade-4 stop')

# p-margin-calls: order H, M, X
PM = [[F(9, 10), F(1, 10), F(0)], [F(5, 10), F(3, 10), F(2, 10)], [F(0), F(0), F(1)]]
canvas_matrix(L1, 'p-margin-calls', PM)
H, M, X = 0, 1, 2
first2 = PM[M][H] + PM[M][M] * PM[M][H]
# alt: make H absorbing and read P^2
PMa = np.array([[1, 0, 0], [0.5, 0.3, 0.2], [0, 0, 1]])
num(L1, 'p-margin-calls', 1, first2, np.linalg.matrix_power(PMa, 2)[M][H],
    {'on-day-two': mpow(PM, 2)[M][H], 'one-day': PM[M][H], 'added': PM[M][H] + PM[M][M]})
h = PM[M][H] / (1 - PM[M][M])
num(L1, 'p-margin-calls', 2, h, np.linalg.matrix_power(PMa, 400)[M][H],
    {'two-days': first2, 'one-day': PM[M][H], 'no-x': PM[M][H] / (PM[M][H] + PM[M][M])})
fH = PM[H][H] + PM[H][M] * h
# alt: seeded simulation of returns is slow to converge; use the series over days on M
fH_alt = 0.9 + 0.1 * sum(0.5 * 0.3 ** n for n in range(200))
num(L1, 'p-margin-calls', 3, fH, fH_alt,
    {'loop-only': PM[H][H], 'one-day': PM[H][H] + PM[H][M] * PM[M][H], 'two-days': PM[H][H] + PM[H][M] * first2,
     'via-m': PM[H][M] * h})
ok(fH == F(34, 35), 'p-margin-calls: f_H is 34/35')
pick(L1, 'p-margin-calls', 4, 'liquidated')
ok(abs(float(1 - fH) - 0.0286) < 0.00005, 'p-margin-calls: option 0.0286')
ok(PM[M][X] / (1 - PM[M][M]) == F(2, 7), 'p-margin-calls: option 2/7')
ok(npow(PM, 2000)[H][X] > 0.999999, 'p-margin-calls: absorbed in the end')

# p-carry-pause: order calm, stressed
PC = [[F(95, 100), F(5, 100)], [F(3, 10), F(7, 10)]]
canvas_matrix(L1, 'p-carry-pause', PC)
win, loss = 3, -8
mS, mC = 1 / (1 - PC[1][1]), 1 / (1 - PC[0][0])
num(L1, 'p-carry-pause', 1, mS, geo_mean_series(PC[1][1]),
    {'used-stay': 1 / PC[1][1], 'further': PC[1][1] / (1 - PC[1][1]), 'calm': mC})
share = mC / (mC + mS)
num(L1, 'p-carry-pause', 2, share, stationary_np(PC)[0],
    {'stay-ratio': PC[0][0] / (PC[0][0] + PC[1][1]), 'used-stay': mC / (mC + 1 / PC[1][1]),
     'swapped': 1 - share, 'equal': F(1, 2)},
    routes=[F(20) / (F(20) + F('3.33'))])
ok(share == F(6, 7), 'p-carry-pause: share 6/7')
avg = share * win + (1 - share) * loss
rng = np.random.default_rng(7)
Pf = npow(PC, 1)
state, tot, n = 0, 0.0, 400000
for _ in range(n):
    tot += win if state == 0 else loss
    state = 0 if rng.random() < Pf[state][0] else 1
sim_avg = tot / n
ok(abs(sim_avg - float(avg)) < 0.05, f'p-carry-pause: simulated average {sim_avg}')
s_used = mC / (mC + 1 / PC[1][1])
num(L1, 'p-carry-pause', 3, avg, float(stationary_np(PC) @ np.array([win, loss])),
    {'equal': F(win + loss, 2), 'used-stay': s_used * win + (1 - s_used) * loss,
     'sign': share * win - (1 - share) * loss, 'swapped': (1 - share) * win + share * loss})
nextS = PC[1][0] * win + PC[1][1] * loss
nextC = PC[0][0] * win + PC[0][1] * loss
num(L1, 'p-carry-pause', 4, nextS, float(npow(PC, 1)[1] @ np.array([win, loss])),
    {'stays': loss, 'calm-row': nextC, 'long-run': avg, 'swapped': PC[1][1] * win + PC[1][0] * loss})
rule = share * nextC
# alt: seeded simulation of the rule
state, tot = 0, 0.0
for _ in range(n):
    on = state == 0
    state = 0 if rng.random() < Pf[state][0] else 1
    if on:
        tot += win if state == 0 else loss
num(L1, 'p-carry-pause', 5, rule, float(stationary_np(PC)[0]) * float(npow(PC, 1)[0] @ np.array([win, loss])),
    {'ignores-switch': share * win, 'unweighted': nextC, 'always-on': avg, 'gain': (1 - share) * (-nextS)})
ok(abs(tot / n - float(rule)) < 0.05, f'p-carry-pause: simulated rule {tot / n}')
ok(avg + (1 - share) * (-nextS) == rule, 'p-carry-pause: rule = always on + skipped loss')
ok(nextC == F(245, 100), 'p-carry-pause: 2.45 after calm')

# ------------------------------------------------------------------ report
print(f'{checks} checks, {len(fails)} failures')
for f in fails:
    print('FAIL', f)
sys.exit(1 if fails else 0)
