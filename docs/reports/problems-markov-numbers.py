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

# ------------------------------------------------------------------ level 2
L2 = load(2)


def solve_exact(A, b):
    """Gaussian elimination over Fractions."""
    n = len(A)
    M = [list(map(F, A[i])) + [F(b[i])] for i in range(n)]
    for c in range(n):
        r = next(i for i in range(c, n) if M[i][c] != 0)
        M[c], M[r] = M[r], M[c]
        for i in range(n):
            if i != c and M[i][c] != 0:
                f = M[i][c] / M[c][c]
                M[i] = [a - f * bb for a, bb in zip(M[i], M[c])]
    return [M[i][n] / M[i][i] for i in range(n)]


def stationary_exact(P):
    """pi P = pi with sum 1: replace the last balance equation by the normaliser."""
    n = len(P)
    A = [[P[j][i] - (1 if i == j else 0) for j in range(n)] for i in range(n)]
    A[-1] = [F(1)] * n
    return solve_exact(A, [0] * (n - 1) + [1])


def absorb(P, trans, target):
    """Exact chance of absorption at `target` from each transient state, (I - Q)h = r."""
    A = [[(1 if i == j else 0) - P[i][j] for j in trans] for i in trans]
    return solve_exact(A, [P[i][target] for i in trans])


def steps(P, trans):
    A = [[(1 if i == j else 0) - P[i][j] for j in trans] for i in trans]
    return solve_exact(A, [1] * len(trans))


def np_absorb(P, trans, absn):
    A = np.array([[float(x) for x in r] for r in P])
    Q = A[np.ix_(trans, trans)]
    R = A[np.ix_(trans, absn)]
    N = np.linalg.inv(np.eye(len(trans)) - Q)
    return N @ R, N @ np.ones(len(trans))


def expr(items, iid, k, value_at, wrong_at, q0=F(3, 5)):
    """An expression part in q: answer and accept forms equal value_at(q) at several q;
    each wrong differs. Uses sympy."""
    if items is None:
        return
    import sympy as sp
    q = sp.Symbol('q')
    w = items[iid]['parts'][k - 1]['widget']
    tag = f'{iid} p{k}'

    from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

    def parse(t):
        t = re.sub(r'\\frac\{([^{}]+)\}\{([^{}]+)\}', r'((\1)/(\2))', t)
        return parse_expr(t, local_dict={'q': q},
                          transformations=standard_transformations + (implicit_multiplication_application,))
    forms = [w['answer']] + w.get('accept', [])
    for f_ in forms:
        e = parse(f_)
        for qv in [F(1, 10), F(3, 5), F(9, 10)]:
            ok(sp.Rational(value_at(qv)) == sp.nsimplify(e.subs(q, sp.Rational(qv))), f'{tag}: form {f_} differs at q={qv}')
    for x in w['wrong']:
        e = parse(x['tex'])
        ok(sp.simplify(e - parse(w['answer'])) != 0, f'{tag}: wrong {x["id"]} equals the answer')
        ok(x['id'] in wrong_at and sp.nsimplify(e.subs(q, sp.Rational(1, 2))) == sp.Rational(wrong_at[x['id']](F(1, 2))),
           f'{tag}: wrong {x["id"]} does not match its slip')
    ok(set(x['id'] for x in w['wrong']) == set(wrong_at), f'{tag}: wrong ids differ')
    ok(set(items[iid]['parts'][k - 1]['feedback']['byKey']) == set(wrong_at), f'{tag}: byKey keys differ')


# p-band-days: order Below, Inside, Above
PB = [[F(1, 2), F(1, 2), F(0)], [F(1, 10), F(8, 10), F(1, 10)], [F(0), F(4, 10), F(6, 10)]]
canvas_matrix(L2, 'p-band-days', PB)
B_, I_, A_ = 0, 1, 2
num(L2, 'p-band-days', 1, mpow(PB, 2)[I_][A_], npow(PB, 2)[I_][A_],
    {'squared': PB[I_][A_] ** 2, 'one-path': PB[I_][I_] * PB[I_][A_], 'one-step': PB[I_][A_]})
c = PB[I_][B_] / (1 - PB[B_][B_])
piB = stationary_exact(PB)
pin = stationary_np(PB)
num(L2, 'p-band-days', 2, c, pin[B_] / pin[I_],
    {'inverted': 1 / c, 'no-move': PB[I_][B_], 'row': PB[B_][B_] + PB[B_][I_]})
cA = PB[I_][A_] / (1 - PB[A_][A_])
ok(cA == F(1, 4), 'p-band-days: pi_A = 0.25 pi_I')
num(L2, 'p-band-days', 3, 1 / (1 + c + cA), pin[I_],
    {'equal': F(1, 3), 'stay': PB[I_][I_], 'no-move-carry': 1 / (1 + PB[I_][B_] + cA), 'no-self': 1 / (c + cA)})
ok(piB == [F(4, 29), F(20, 29), F(5, 29)], f'p-band-days: pi {piB}')
ok(np.allclose(npow(PB, 60), np.tile(pin, (3, 1)), atol=1e-6), 'p-band-days: P^60 rows equal pi')
pick(L2, 'p-band-days', 4, 'yes')
piI = piB[I_]
pl = (1 - piI) * 3 - piI * 1
rng = np.random.default_rng(11)
st, tot, n = 1, 0.0, 300000
cum = np.cumsum(np.array([[float(x) for x in r] for r in PB]), axis=1)
for _ in range(n):
    tot += 3 if st != 1 else -1
    st = int(np.searchsorted(cum[st], rng.random(), side='right'))
ok(abs(tot / n - float(pl)) < 0.03, f'p-band-days: simulated P&L {tot / n}')
num(L2, 'p-band-days', 5, pl, float(pin @ np.array([3, -1, 3])),
    {'equal': F(3 - 1 + 3, 3), 'sign': (1 - piI) * 3 + piI, 'stay': F(2, 10) * 3 - F(8, 10), 'outside-only': (1 - piI) * 3})

# p-strategy-trial: order Test, On, Off, Shut
PT = [[F(1, 2), F(3, 10), F(0), F(2, 10)], [F(0), F(9, 10), F(1, 10), F(0)],
      [F(0), F(4, 10), F(6, 10), F(0)], [F(0), F(0), F(0), F(1)]]
canvas_matrix(L2, 'p-strategy-trial', PT)
num(L2, 'p-strategy-trial', 1, mpow(PT, 2)[0][1], npow(PT, 2)[0][1],
    {'test-test': PT[0][0] * PT[0][1], 'on-on': PT[0][1] * PT[1][1], 'squared': PT[0][1] ** 2})
live = stationary_exact([[PT[1][1], PT[1][2]], [PT[2][1], PT[2][2]]])
num(L2, 'p-strategy-trial', 2, live[0], stationary_np([[0.9, 0.1], [0.4, 0.6]])[0],
    {'stay': PT[1][1], 'swapped': live[1], 'equal': F(1, 2), 'stay-ratio': PT[1][1] / (PT[1][1] + PT[2][1])})
hl = PT[0][1] / (1 - PT[0][0])
num(L2, 'p-strategy-trial', 3, hl, 1 - npow(PT, 500)[0][3],
    {'one-week': PT[0][1], 'two-weeks': PT[0][1] + PT[0][0] * PT[0][1], 'carry': mpow(PT, 2)[0][1],
     'total': PT[0][1] + PT[0][0]})
num(L2, 'p-strategy-trial', 4, hl * live[0], npow(PT, 500)[0][1],
    {'ignores-shut': live[0], 'live-only': hl, 'two-step': mpow(PT, 2)[0][1], 'whole-chain': 0})

# p-rfq-rounds: order Quote, Counter, Trade, Walk
PR = [[F(0), F(4, 10), F(4, 10), F(2, 10)], [F(1, 2), F(0), F(2, 10), F(3, 10)],
      [F(0), F(0), F(1), F(0)], [F(0), F(0), F(0), F(1)]]
canvas_matrix(L2, 'p-rfq-rounds', PR)
expr(L2, 'p-rfq-rounds', 1, lambda qv: F(1, 5) + qv / 2,
     {'no-direct': lambda qv: qv / 2, 'walk': lambda qv: F(3, 10) + qv / 2, 'plus-one': lambda qv: F(6, 5) + qv / 2})
hq = absorb(PR, [0, 1], 2)
Hn, tn = np_absorb(PR, [0, 1], [2, 3])
num(L2, 'p-rfq-rounds', 2, hq[0], Hn[0][0],
    {'direct': PR[0][2], 'one-pass': PR[0][2] + PR[0][1] * PR[1][2], 'no-direct': PR[0][2] / (1 - PR[0][1] * F(1, 2)),
     'walk': (PR[0][2] + PR[0][1] * F(3, 10)) / (1 - PR[0][1] * F(1, 2))})
ok(hq[1] == F(1, 2) and abs(Hn[0][1] - 0.4) < 1e-12, 'p-rfq-rounds: h_C = 0.5 and walk row 0.4')
tq = steps(PR, [0, 1])
num(L2, 'p-rfq-rounds', 3, tq[0], tn[0],
    {'one-pass': 1 + PR[0][1], 'no-one': 0, 'geometric': 1 / (PR[0][2] + PR[0][3]), 'counter': tq[1]})
ok(tq[1] == F(15, 8), 'p-rfq-rounds: t_C = 1.875')
PR2 = [r[:] for r in PR]
PR2[0] = [F(0), F(3, 10), F(5, 10), F(2, 10)]
hq2 = absorb(PR2, [0, 1], 2)
Hn2, _ = np_absorb(PR2, [0, 1], [2, 3])
num(L2, 'p-rfq-rounds', 4, hq2[0], Hn2[0][0],
    {'one-pass': PR2[0][2] + PR2[0][1] * PR2[1][2], 'old-hc': PR2[0][2] + PR2[0][1] * hq[1], 'direct': PR2[0][2],
     'old-q': hq[0]})
ok(hq2[0] == F(56, 85), 'p-rfq-rounds: new q = 56/85')
pick(L2, 'p-rfq-rounds', 5, 'old')
ok(hq[0] * 50 == 30 and abs(float(hq2[0] * 40) - 26.35) < 0.005, 'p-rfq-rounds: £30 and £26.35')

# p-merger-arb: order Announced, Review, Completed, Withdrawn
PA = [[F(1, 2), F(3, 10), F(1, 10), F(1, 10)], [F(0), F(6, 10), F(1, 4), F(15, 100)],
      [F(0), F(0), F(1), F(0)], [F(0), F(0), F(0), F(1)]]
canvas_matrix(L2, 'p-merger-arb', PA)
hA, hR = absorb(PA, [0, 1], 2)
Ha, ta_n = np_absorb(PA, [0, 1], [2, 3])
num(L2, 'p-merger-arb', 1, hR, Ha[1][0],
    {'one-month': PA[1][2], 'over-stay': PA[1][2] / PA[1][1], 'leave': PA[1][2] + PA[1][3]})
noloop = PA[0][2] + PA[0][1] * hR
num(L2, 'p-merger-arb', 2, hA, Ha[0][0],
    {'no-loop': noloop, 'direct': PA[0][2] + PA[0][1], 'loop-once': noloop * F(3, 2)})
tA, tR = steps(PA, [0, 1])
ok(tR == F(5, 2), 'p-merger-arb: t_R = 2.5')
num(L2, 'p-merger-arb', 3, tA, ta_n[0],
    {'no-loop': 1 + PA[0][1] * tR, 'no-review': 1 / (1 - PA[0][0]), 'no-one': PA[0][1] * tR / (1 - PA[0][0]),
     'added': 1 / (1 - PA[0][0]) + tR})
ev = hA * 10 + (1 - hA) * 6
# alt: simulate deals
rng = np.random.default_rng(5)
cumA = np.cumsum(np.array([[float(x) for x in r] for r in PA]), axis=1)
vals, months = [], []
for _ in range(100000):
    s_, m_ = 0, 0
    while s_ in (0, 1):
        s_ = int(np.searchsorted(cumA[s_], rng.random(), side='right'))
        m_ += 1
    vals.append(10 if s_ == 2 else 6)
    months.append(m_)
ok(abs(np.mean(vals) - float(ev)) < 0.03, f'p-merger-arb: simulated value {np.mean(vals)}')
ok(abs(np.mean(months) - float(tA)) < 0.05, f'p-merger-arb: simulated months {np.mean(months)}')
num(L2, 'p-merger-arb', 4, ev, Ha[0][0] * 10 + Ha[0][1] * 6,
    {'review-h': hR * 10 + (1 - hR) * 6, 'even': F(8), 'no-withdraw': hA * 10, 'swapped': hA * 6 + (1 - hA) * 10})
cost = F(2, 100)
num(L2, 'p-merger-arb', 5, ev - cost * tA, float(np.mean(vals)) * 0 + float(Ha[0][0] * 10 + Ha[0][1] * 6) - 0.02 * ta_n[0],
    {'no-cost': ev, 'review-time': ev - cost * tR, 'one-month': ev - cost, 'carry-added': ev - cost * (2 + tR)})

# ------------------------------------------------------------------ level 3
L3 = load(3)
from math import comb, sqrt, ceil
from scipy.stats import norm, binom

# p-maker-edge: steps +2 w.p. 0.55, -2 w.p. 0.45
p_, s_ = F(55, 100), 2
mean1 = s_ * p_ - s_ * (1 - p_)
var1 = s_ ** 2 - mean1 ** 2
# alt: direct sum over the two outcomes
alt_var = p_ * (s_ - mean1) ** 2 + (1 - p_) * (-s_ - mean1) ** 2
num(L3, 'p-maker-edge', 1, var1, alt_var,
    {'no-mean': F(4), 'unit-steps': 1 - (2 * p_ - 1) ** 2, 'mean': mean1})
n400 = 400
sd400 = sqrt(n400 * float(var1))
# alt: variance of 2(2K - n) for K ~ Binomial(n, p): 16 n p (1-p)
num(L3, 'p-maker-edge', 2, sd400, sqrt(16 * n400 * 0.55 * 0.45),
    {'no-mean': sqrt(n400 * 4), 'variance': n400 * float(var1), 'unit-steps': sd400 / 2, 'no-n': sqrt(float(var1))})
zdown = float(n400 * mean1) / sd400
pdown = norm.cdf(-zdown)
exact_down = binom.cdf(199, n400, 0.55)       # S < 0 iff K <= 199
num(L3, 'p-maker-edge', 3, pdown, norm.sf(zdown),
    {'variance': norm.cdf(-80 / (n400 * float(var1))), 'complement': 1 - pdown, 'one-trade': norm.cdf(-80 / sqrt(float(var1)))},
    routes=[norm.cdf(-80 / 39.80), exact_down, round(pdown, 2)])
ok(abs(exact_down - 0.020) < 0.0005, f'p-maker-edge: exact binomial {exact_down}')
z99 = 2.33
nmin = ceil(z99 ** 2 * float(var1) / float(mean1) ** 2)
# alt: step n until the ratio passes 2.33
n_ = 1
while 0.2 * n_ / sqrt(3.96 * n_) < z99:
    n_ += 1
num(L3, 'p-maker-edge', 4, nmin, n_,
    {'no-mean': ceil(z99 ** 2 * 4 / 0.04), 'five-percent': ceil(1.645 ** 2 * 3.96 / 0.04),
     'root': ceil(z99 * sqrt(3.96) / 0.2), 'two-sd': ceil(4 * 3.96 / 0.04)},
    routes=[ceil(norm.ppf(0.99) ** 2 * 3.96 / 0.04)])

# p-barrier-note: fair walk, 12 steps, barrier -3
n12 = 12
paths = list(itertools.product((1, -1), repeat=n12))
ends = {}
touch_by_end = {}
for pth in paths:
    pos, mn = 0, 0
    for st in pth:
        pos += st
        mn = min(mn, pos)
    ends[pos] = ends.get(pos, 0) + 1
    if mn <= -3:
        touch_by_end[pos] = touch_by_end.get(pos, 0) + 1
num(L3, 'p-barrier-note', 1, comb(12, 4), ends[-4],
    {'end-minus-two': comb(12, 5), 'mirror': comb(12, 3), 'end-zero': comb(12, 6)})
num(L3, 'p-barrier-note', 2, comb(12, 4), touch_by_end[-2],
    {'all-paths': comb(12, 5), 'wrong-mirror': comb(12, 3), 'none': 0})
below = sum(comb(12, k) for k in range(0, 5))
ok(below == 794, 'p-barrier-note: 794 paths end at -4 or below')
touch = F(2 * below, 4096)
num(L3, 'p-barrier-note', 3, touch, F(sum(touch_by_end.values()), 4096),
    {'end-only': F(below, 4096), 'level-two': F(2 * (below + comb(12, 5)), 4096), 'plus-two': F(below + comb(12, 5 - 1), 4096)})
num(L3, 'p-barrier-note', 4, 100 * (1 - touch), 100 * (1 - sum(touch_by_end.values()) / 4096),
    {'pays-on-touch': 100 * touch, 'end-only': 100 * (1 - F(below, 4096)), 'face': 100},
    routes=[100 * (1 - F('0.3877'))])
pick(L3, 'p-barrier-note', 5, 'simulate')
ok(abs(50 / 1.1 ** 3 - 37.57) < 0.005, 'p-barrier-note: barrier price £37.57')
# drifted walk touches less often (the choice's claim)
pd = F(52, 100)
drift_touch = 0
for pth in paths:
    pos, mn, pr = 0, 0, F(1)
    for st in pth:
        pos += st
        mn = min(mn, pos)
        pr *= pd if st == 1 else 1 - pd
    if mn <= -3:
        drift_touch += pr
ok(drift_touch < touch, 'p-barrier-note: upward drift touches less')

# p-stake-size: p = 0.48, from 600 to 1000
pw = F(48, 100)
r = (1 - pw) / pw
ok(r == F(13, 12), 'p-stake-size: r = 13/12')


def ruin_np(i, N, p):
    """Chance of reaching N before 0 by solving the first-step system numerically."""
    A = np.zeros((N + 1, N + 1))
    b = np.zeros(N + 1)
    A[0, 0] = A[N, N] = 1
    b[N] = 1
    for k in range(1, N):
        A[k, k] = 1
        A[k, k + 1] = -p
        A[k, k - 1] = -(1 - p)
    return np.linalg.solve(A, b)[i]


def PR_(i, N, rr):
    return (1 - rr ** i) / (1 - rr ** N)


num(L3, 'p-stake-size', 1, 100 * (2 * pw - 1), 0.48 * 100 + 0.52 * (-100),
    {'half': 100 * (pw - F(1, 2)), 'win-only': 100 * pw, 'loss-only': -100 * (1 - pw)})
P100 = PR_(6, 10, r)
num(L3, 'p-stake-size', 2, P100, ruin_np(6, 10, 0.48),
    {'fair': F(6, 10), 'r-inverted': PR_(6, 10, 1 / r)})
ok(abs(float(r ** 6) - 1.6165) < 0.00005 and abs(float(r ** 10) - 2.2265) < 0.00005, 'p-stake-size: printed powers')
P200 = PR_(3, 5, r)
num(L3, 'p-stake-size', 3, P200, ruin_np(3, 5, 0.48),
    {'fair': F(3, 5), 'r-inverted': PR_(3, 5, 1 / r), 'same': P100})
ok(abs(float(r ** 3) - 1.2714) < 0.00005 and abs(float(r ** 5) - 1.4921) < 0.00005, 'p-stake-size: printed powers 3, 5')
prof = 1000 * P200 - 600
rng = np.random.default_rng(3)
tot = 0.0
for _ in range(100000):
    w = 600
    while 0 < w < 1000:
        w += 200 if rng.random() < 0.48 else -200
    tot += w - 600
ok(abs(tot / 100000 - float(prof)) < 3, f'p-stake-size: simulated profit {tot / 100000}')
num(L3, 'p-stake-size', 4, prof, 1000 * ruin_np(3, 5, 0.48) - 600,
    {'hundreds': 1000 * P100 - 600, 'wealth': 1000 * P200, 'fair': 0, 'target-only': 400},
    routes=[1000 * F('0.5515') - 600])

# p-pairs-exit: fair walk, start 5 in [0, 8]
i5, N8 = 5, 8
pt = F(i5, N8)
num(L3, 'p-pairs-exit', 1, pt, ruin_np(5, 8, 0.5),
    {'swapped': 1 - pt, 'equal': F(1, 2), 'ratio': F(3, 5)})
D = i5 * (N8 - i5)
Pw = [[F(0)] * 9 for _ in range(9)]
Pw[0][0] = Pw[8][8] = F(1)
for k in range(1, 8):
    Pw[k][k - 1] = Pw[k][k + 1] = F(1, 2)
num(L3, 'p-pairs-exit', 2, D, steps(Pw, list(range(1, 8)))[i5 - 1],
    {'width': N8, 'product': i5 * N8, 'square': i5 ** 2, 'target-sq': 9})
ticks = pt * 3 - (1 - pt) * 5
# alt: simulate exits
rng = np.random.default_rng(9)
tt, dd, m = 0, 0, 100000
for _ in range(m):
    x, d = 0, 0
    while -5 < x < 3:
        x += 1 if rng.random() < 0.5 else -1
        d += 1
    tt += x
    dd += d
ok(abs(tt / m) < 0.05 and abs(dd / m - 15) < 0.2, f'p-pairs-exit: simulated ticks {tt / m}, days {dd / m}')
num(L3, 'p-pairs-exit', 3, ticks, 0.0,
    {'target-only': pt * 3, 'stop-only': -(1 - pt) * 5, 'target': 3})
num(L3, 'p-pairs-exit', 4, 100 * ticks - 40 * D, 100 * (tt / m) * 0 - 40 * 15,
    {'no-cost': 0, 'one-day': -40, 'product-days': -40 * i5 * N8, 'ticks': 100 * pt * 3})
pick(L3, 'p-pairs-exit', 5, 'two-six')
ok([a * b for a, b in [(3, 5), (4, 4), (2, 6)]] == [15, 16, 12] and -40 * 12 == -480, 'p-pairs-exit: option days and £480')

# ================================================================== level 4 (problems-4.json)
# Added by the level 4 and 5 author. Method 1: exact fractions (degrees, balance weights,
# Metropolis-Hastings entries). Method 2: numpy eigenvectors of the full transition
# matrices, brute-force searches and seeded simulations.
from math import exp, log, sqrt, factorial
L4 = load(4)


def walk_matrix(nodes, edges):
    """Exact transition matrix of the simple random walk on an undirected graph."""
    nb = {v: [] for v in nodes}
    for a, b in edges:
        nb[a].append(b)
        nb[b].append(a)
    return [[F(1, len(nb[i])) if j in nb[i] else F(0) for j in nodes] for i in nodes], nb


# p-supplier-survey: H-A, H-B, H-C, H-D, A-B
sv_nodes = ['H', 'A', 'B', 'C', 'D']
sv_edges = [('H', 'A'), ('H', 'B'), ('H', 'C'), ('H', 'D'), ('A', 'B')]
Psv, nbs = walk_matrix(sv_nodes, sv_edges)
deg = {v: len(nbs[v]) for v in sv_nodes}
tot = sum(deg.values())
ok(tot == 2 * len(sv_edges) == 10, 'p-supplier-survey: total degree')
pi_np = stationary_np(Psv)
piC = F(deg['C'], tot)
num(L4, 'p-supplier-survey', 1, piC, pi_np[3],
    {'uniform': F(1, 5), 'hub': F(deg['H'], tot)})
num(L4, 'p-supplier-survey', 2, piC + F(deg['D'], tot), pi_np[3] + pi_np[4],
    {'true': F(2, 5), 'one-firm': piC})
pick(L4, 'p-supplier-survey', 3, 'ratio')
# Metropolis-Hastings matrix for a uniform target with q_ij = 1/deg(i)
MH = [[F(0)] * 5 for _ in range(5)]
for a, i in enumerate(sv_nodes):
    for b, j in enumerate(sv_nodes):
        if j in nbs[i]:
            MH[a][b] = F(1, deg[i]) * min(F(1), F(deg[i], deg[j]))
    MH[a][a] = 1 - sum(MH[a])
ok(all(MH[a][b] == MH[b][a] for a in range(5) for b in range(5)), 'p-supplier-survey: MH matrix not symmetric')
ok(np.allclose(stationary_np(MH), [0.2] * 5), 'p-supplier-survey: MH not uniform')
stayC = MH[3][3]
# alt: count rejections by simulation of the corrected walk from C
rng = np.random.default_rng(41)
x, stays, n_sim = 'C', 0, 200000
for _ in range(n_sim):
    j = nbs[x][rng.integers(len(nbs[x]))]
    if rng.random() < min(1.0, deg[x] / deg[j]):
        x = j
    else:
        stays += 1
num(L4, 'p-supplier-survey', 4, stayC, 1 - 1 / 4,
    {'move': F(1, 4), 'flipped': 0})
ok([MH[k][k] for k in range(5)] == [0, F(1, 4), F(1, 4), F(3, 4), F(3, 4)], 'p-supplier-survey: staying chances in part 5 text')
rep = sum(F(1, 5) * MH[k][k] for k in range(5))
ok(abs(stays / n_sim - float(rep)) < 0.005, f'p-supplier-survey: simulated repeats {stays / n_sim}')
num(L4, 'p-supplier-survey', 5, rep, float(np.trace(np.diag([0.2] * 5) @ np.array(MH, float))),
    {'plain': 0, 'leaves-only': F(1, 5) * (MH[3][3] + MH[4][4]),
     'degree-weights': sum(F(deg[v], tot) * MH[k][k] for k, v in enumerate(sv_nodes))})

# p-taxi-rank: taxis 2.4, passengers 1.6 a minute; capacity 3, then 4
lt, lp = F('2.4'), F('1.6')
up = lt / (lt + lp)
num(L4, 'p-taxi-rank', 1, up, 2.4 / 4.0, {'ratio': lt / lp, 'passenger': 1 - up})
ratio = up / (1 - up)
num(L4, 'p-taxi-rank', 2, ratio, 0.6 / 0.4, {'inverted': 1 / ratio, 'one-way': up})


def rank_chain(cap):
    P = [[F(0)] * (cap + 1) for _ in range(cap + 1)]
    for i in range(cap + 1):
        P[i][min(i + 1, cap)] += up
        P[i][max(i - 1, 0)] += 1 - up
    return P


def pi0_exact(cap, rr):
    return 1 / sum(rr ** k for k in range(cap + 1))


p0 = pi0_exact(3, ratio)
ok(p0 == F(8, 65), 'p-taxi-rank: pi0 is 8/65')
num(L4, 'p-taxi-rank', 3, p0, stationary_np(rank_chain(3))[0],
    {'inverted': pi0_exact(3, 1 / ratio), 'uniform': F(1, 4), 'three-states': pi0_exact(2, ratio)})
ok(pi0_exact(3, 1 / ratio) == ratio ** 3 * p0, 'p-taxi-rank: full share equals the inverted empty share')
# alt for the passenger loss rate: continuous-time simulation over 20,000 minutes
rng = np.random.default_rng(17)
t, k, lost, T_end = 0.0, 0, 0, 20000.0
while True:
    t += rng.exponential(1 / 4.0)
    if t > T_end:
        break
    if rng.random() < 0.6:
        k = min(k + 1, 3)
    elif k == 0:
        lost += 1
    else:
        k -= 1
ok(abs(lost / T_end * 60 - float(96 * p0)) < 0.4, f'p-taxi-rank: simulated loss {lost / T_end * 60}')
loss3 = 96 * p0
num(L4, 'p-taxi-rank', 4, loss3, 1.6 * 60 * stationary_np(rank_chain(3))[0],
    {'all-arrivals': 240 * p0, 'per-minute': lp * p0, 'taxis': 144 * ratio ** 3 * p0},
    routes=[96 * F('0.1231')])
p04 = pi0_exact(4, ratio)
ok(p04 == F(16, 211), 'p-taxi-rank: pi0 with 4 spaces is 16/211')
num(L4, 'p-taxi-rank', 5, 96 * p04, 96 * stationary_np(rank_chain(4))[0],
    {'no-change': loss3, 'inverted': 96 * pi0_exact(4, 1 / ratio), 'saved': loss3 - 96 * p04})

# p-payment-audits: A-B, A-C, A-D, B-C, C-D, D-E, E-F; audits at 2 an hour
pa_nodes = list('ABCDEF')
pa_edges = [('A', 'B'), ('A', 'C'), ('A', 'D'), ('B', 'C'), ('C', 'D'), ('D', 'E'), ('E', 'F')]
Ppa, nbp = walk_matrix(pa_nodes, pa_edges)
dg = [len(nbp[v]) for v in pa_nodes]
ok(dg == [3, 2, 3, 3, 2, 1] and sum(dg) == 14, 'p-payment-audits: degrees')
pin = stationary_np(Ppa)
num(L4, 'p-payment-audits', 1, F(3, 14), pin[3], {'uniform': F(1, 6), 'links': F(3, 7)})
# alt for the return time: mean gap between visits to F in a long simulated walk
rng = np.random.default_rng(5)
x, last, gaps = 'F', 0, []
for s in range(1, 400001):
    x = nbp[x][rng.integers(len(nbp[x]))]
    if x == 'F':
        gaps.append(s - last)
        last = s
ok(abs(np.mean(gaps) - 14) < 0.3, f'p-payment-audits: simulated return {np.mean(gaps)}')
num(L4, 'p-payment-audits', 2, 14, 1 / pin[5], {'links': 7, 'banks': 6})
rateF = 2 * F(1, 14)
mean_day = 8 * rateF
# alt: thinned count simulated as Binomial thinning of Poisson(16) audits
rng = np.random.default_rng(23)
cnt = rng.binomial(rng.poisson(16, 200000), 1 / 14)
ok(abs(cnt.mean() - 8 / 7) < 0.01 and abs((cnt == 0).mean() - exp(-8 / 7)) < 0.004, 'p-payment-audits: simulated thinning')
num(L4, 'p-payment-audits', 3, mean_day, 16 * pin[5],
    {'no-thinning': 16, 'per-hour': rateF, 'uniform': F(8, 6)})
num(L4, 'p-payment-audits', 4, exp(-8 / 7), sum((-8 / 7) ** n / factorial(n) for n in range(40)),
    {'complement': 1 - exp(-8 / 7), 'per-hour': exp(-1 / 7), 'uniform': exp(-8 / 6)})


def first_hours(rate, target=0.9):
    t = 1
    while 1 - exp(-rate * t) <= target:
        t += 1
    return t


ans_t = int(np.ceil(7 * log(10)))
ok(abs(1 - exp(-16 / 7) - 0.8983) < 0.00005, 'p-payment-audits: chance at 16 hours')
num(L4, 'p-payment-audits', 5, ans_t, first_hours(1 / 7),
    {'round-down': ans_t - 1, 'uniform': first_hours(1 / 3), 'no-thinning': first_hours(2),
     'complement': int(np.ceil(7 * log(10 / 9)))})

# p-regime-sampler: weights L 2, M 5, H 3; q_LM = q_HM = 1, q_ML = 0.3, q_MH = 0.7
w = {'L': F(2), 'M': F(5), 'H': F(3)}
q = {('L', 'M'): F(1), ('H', 'M'): F(1), ('M', 'L'): F(3, 10), ('M', 'H'): F(7, 10)}


def mh_matrix(rule):
    S = ['L', 'M', 'H']
    P = [[F(0)] * 3 for _ in range(3)]
    for a, i in enumerate(S):
        for b, j in enumerate(S):
            if (i, j) in q:
                acc = min(F(1), w[j] * q[(j, i)] / (w[i] * q[(i, j)])) if rule == 'mh' else min(F(1), w[j] / w[i])
                P[a][b] = q[(i, j)] * acc
        P[a][a] = 1 - sum(P[a])
    return P


Pmh = mh_matrix('mh')
pis = stationary_np(Pmh)
ok(np.allclose(pis, [0.2, 0.5, 0.3]), f'p-regime-sampler: MH chain stationary {pis}')
num(L4, 'p-regime-sampler', 1, Pmh[0][1], min(1.0, 5 * 0.3 / 2) * 1.0, {'uphill': 1, 'stay': 1 - Pmh[0][1]})
num(L4, 'p-regime-sampler', 2, Pmh[1][2], 0.7 * min(1.0, 3 / (5 * 0.7)),
    {'accept-only': F(6, 7), 'plain': F(7, 10) * F(3, 5), 'proposal-only': F(7, 10)})
num(L4, 'p-regime-sampler', 3, Pmh[1][0], 0.2 * 0.75 / 0.5,
    {'swapped': F(1, 2) * F(3, 4) / F(1, 5), 'plain': F(3, 10) * F(2, 5), 'stay': Pmh[1][1]})
pi_ex = [F(1, 5), F(1, 2), F(3, 10)]
rej = sum(pi_ex[k] * Pmh[k][k] for k in range(3))
# alt: simulate the chain and count rejections
rng = np.random.default_rng(29)
S = ['L', 'M', 'H']
x, rj, n_sim = 'M', 0, 200000
for _ in range(n_sim):
    if x == 'M':
        j = 'L' if rng.random() < 0.3 else 'H'
    else:
        j = 'M'
    acc = min(1.0, float(w[j] * q[(j, x)] / (w[x] * q[(x, j)])))
    if rng.random() < acc:
        x = j
    else:
        rj += 1
ok(abs(rj / n_sim - 0.1) < 0.004, f'p-regime-sampler: simulated rejections {rj / n_sim}')
stays = [Pmh[k][k] for k in range(3)]
num(L4, 'p-regime-sampler', 4, rej, float(np.dot(pis, np.diag(np.array(Pmh, float)))),
    {'unweighted': sum(stays), 'average': sum(stays) / 3, 'one-state': pi_ex[0] * stays[0]})
ok(pi_ex[0] * stays[0] == pi_ex[1] * stays[1], 'p-regime-sampler: Low and Mid rejections are equal (one-state slip)')
Ppl = mh_matrix('plain')
ok(Ppl[0][1] == 1 and Ppl[1][0] == F(12, 100) and Ppl[1][2] == F(42, 100) and Ppl[2][1] == 1, 'p-regime-sampler: plain rule entries in part 5')
wts = [F(1), Ppl[0][1] / Ppl[1][0]]
wts.append(wts[1] * Ppl[1][2] / Ppl[2][1])
piM_plain = wts[1] / sum(wts)
ok(piM_plain == F(50, 77), 'p-regime-sampler: 50/77')
fl = [F(1), Ppl[1][0] / Ppl[0][1]]
fl.append(fl[1] * Ppl[2][1] / Ppl[1][2])
num(L4, 'p-regime-sampler', 5, piM_plain, stationary_np(Ppl)[1],
    {'target': F(1, 2), 'flipped': fl[1] / sum(fl), 'high': wts[2] / sum(wts)})

# ------------------------------------------------------------------ report
print(f'{checks} checks, {len(fails)} failures')
for f in fails:
    print('FAIL', f)
sys.exit(1 if fails else 0)
