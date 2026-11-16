"""Second reader's recompute of app/content/courses/numerics/problems-4.json.

Imports nothing from the author's script. Each key and each `wrong` value is typed from the prose and rebuilt
here by a route of its own: the implicit matrix from sigma, r and the step through a general theta-scheme
assembly and a dense solve; exact fractions for the sweep with the restated rounded values; brute searches
for every "smallest" count; a real explicit march and a real Crank-Nicolson march of the put against the
Black-Scholes formula; the pair's joint table by enumeration and by a seeded simulation.
Bands: the value rounded as the part asks is accepted, each `wrong` value lies outside the key band, and
the value the part's own printed working gives is accepted. Stated figures of feedback and explain lines
are checked as numbers.

A check that fails on wrong content prints a FINDING line and stays failing; the script still exits 0
(CI runs every script in docs/reports).
Run: <scratchpad>/venv/bin/python docs/reports/problems-numerics-4-numbers-read.py
"""
import json, math, os
from fractions import Fraction as F
import numpy as np
from scipy.stats import norm

HERE = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'numerics', 'problems-4.json')
D = json.load(open(PATH, encoding='utf8'))
IT = {it['id']: it for it in D['items']}
n_checks = 0
findings = []


def chk(cond, msg):
    global n_checks
    n_checks += 1
    if not cond:
        findings.append(msg)
        print('FINDING', msg)


def W(pid, k):
    return IT[pid]['parts'][k - 1]['widget']


def key(pid, k, mine, typed=()):
    """mine: my value. typed: values a learner types at the rounding asked, all of which must pass."""
    w = W(pid, k)
    a, tol = w['answer'], w['tol']['abs']
    chk(abs(a - mine) <= max(tol * 0.5, 1e-9), f'{pid} part {k}: key {a} against mine {mine}')
    for t in typed:
        chk(abs(t - a) <= tol + 1e-12, f'{pid} part {k}: typed {t} refused by key {a} tol {tol}')
    for x in w.get('wrong', []):
        chk(abs(x['value'] - a) > tol + x['tol']['abs'], f"{pid} part {k}: wrong {x['id']} band meets the key band")
    ids = [x['id'] for x in w.get('wrong', [])]
    for i, x in enumerate(w.get('wrong', [])):
        for y in w['wrong'][i + 1:]:
            chk(abs(x['value'] - y['value']) > x['tol']['abs'] + y['tol']['abs'],
                f"{pid} part {k}: wrong {x['id']} and {y['id']} bands meet")
    return ids


def wrong(pid, k, wid, mine, typed=()):
    w = W(pid, k)
    e = [x for x in w.get('wrong', []) if x['id'] == wid]
    chk(len(e) == 1, f'{pid} part {k} wrong {wid}: entry missing')
    if not e:
        return
    v, tol = e[0]['value'], e[0]['tol']['abs']
    chk(abs(v - mine) <= max(tol * 0.2, 1e-9), f'{pid} part {k} wrong {wid}: {v} against mine {mine}')
    for t in typed:
        chk(abs(t - v) <= tol + 1e-12, f'{pid} part {k} wrong {wid}: typed {t} misses its band {v} tol {tol}')


def all_wrong_seen(pid, k, seen):
    ids = [x['id'] for x in W(pid, k).get('wrong', [])]
    chk(sorted(ids) == sorted(seen), f'{pid} part {k}: wrong ids {ids} against the ones recomputed {seen}')


def says(pid, k, field, *subs):
    p = IT[pid]['parts'][k - 1]
    txt = p['question'] if field == 'question' else p['explain']['text'] if field == 'explain' else \
        p['feedback'][field] if field in p['feedback'] else p['feedback']['byKey'][field]
    for s in subs:
        chk(s in txt, f'{pid} part {k} {field}: expected to print "{s}"')


def prose_says(pid, *subs):
    for s in subs:
        chk(s in IT[pid]['prose'], f'{pid} prose: expected "{s}"')


# ---------------------------------------------------------------------------------------------------
# shared: Black-Scholes put, theta-scheme put on [0, Smax]
def bs_put(S, K, r, sig, T):
    d1 = (math.log(S / K) + (r + sig * sig / 2) * T) / (sig * math.sqrt(T))
    d2 = d1 - sig * math.sqrt(T)
    return K * math.exp(-r * T) * norm.cdf(-d2) - S * norm.cdf(-d1)


def theta_put(S0, K, r, sig, T, Smax, M, N, theta, implicit_start=0):
    """The course's scheme (l13 screen 4, l14 screens 2 and 10, l17 screen 9), written from the PDE."""
    j = np.arange(M + 1)
    al = 0.5 * (sig ** 2 * j ** 2 - r * j)
    be = -(sig ** 2 * j ** 2 + r)
    ga = 0.5 * (sig ** 2 * j ** 2 + r * j)
    dt = T / N
    S = j * Smax / M
    V = np.maximum(K - S, 0.0)
    for n in range(N):
        th = 1.0 if n < implicit_start else theta
        tau1 = (n + 1) * dt
        LV = al[1:-1] * V[:-2] + be[1:-1] * V[1:-1] + ga[1:-1] * V[2:]
        rhs = V[1:-1] + (1 - th) * dt * LV
        lo, hi = K * math.exp(-r * tau1), 0.0
        if th == 0.0:
            V[1:-1] = rhs
        else:
            a = -th * dt * al[1:-1]
            b = 1 - th * dt * be[1:-1]
            c = -th * dt * ga[1:-1]
            rhs[0] += th * dt * al[1] * lo
            rhs[-1] += th * dt * ga[M - 1] * hi
            # banded solve by numpy on the dense matrix for small M, by a sweep otherwise
            m = M - 1
            if m <= 8:
                A = np.diag(b) + np.diag(a[1:], -1) + np.diag(c[:-1], 1)
                V[1:-1] = np.linalg.solve(A, rhs)
            else:
                bp, dp = b.copy(), rhs.copy()
                for i in range(1, m):
                    w = a[i] / bp[i - 1]
                    bp[i] -= w * c[i - 1]
                    dp[i] -= w * dp[i - 1]
                x = np.empty(m)
                x[-1] = dp[-1] / bp[-1]
                for i in range(m - 2, -1, -1):
                    x[i] = (dp[i] - c[i] * x[i + 1]) / bp[i]
                V[1:-1] = x
        V[0], V[-1] = lo, hi
    return V, S


# ---------------------------------------------------------------------------------------------------
# 1. p-hand-implicit-put
pid = 'p-hand-implicit-put'
K, sig, r, dt = 30.0, 0.5, 0.04, 0.5
# the printed matrix and right side, rebuilt from the scheme
jj = np.array([1, 2, 3])
sub = -0.5 * dt * (sig ** 2 * jj ** 2 - r * jj)
dia = 1 + dt * (sig ** 2 * jj ** 2 + r)
sup = -0.5 * dt * (sig ** 2 * jj ** 2 + r * jj)
chk(np.allclose(dia, [1.145, 1.52, 2.145]) and np.allclose(sub[1:], [-0.23, -0.5325]) and np.allclose(sup[:2], [-0.0725, -0.27]),
    f'{pid}: printed matrix against the scheme {dia} {sub} {sup}')
rhs1 = 20 + 0.5 * dt * (sig ** 2 - r) * K * math.exp(-r * dt)
chk(abs(rhs1 - 21.5438) < 5e-5, f'{pid}: first right side {rhs1} against 21.5438')
prose_says(pid, '1.145 & -0.0725 & 0', '-0.23 & 1.52 & -0.27', '0 & -0.5325 & 2.145', '21.5438', '(30, 20, 10, 0, 0)')
V, S = theta_put(20, K, r, sig, 0.5, 40, 4, 1, 1.0)
A = np.array([[1.145, -0.0725, 0], [-0.23, 1.52, -0.27], [0, -0.5325, 2.145]])
x = np.linalg.solve(A, np.array([21.5438, 10, 0]))
chk(np.allclose(V[1:4], x, atol=2e-5), f'{pid}: scheme values {V[1:4]} against the printed system {x}')

# part 1
w1 = 1 - dt * (sig ** 2 * 9 + r)
key(pid, 1, w1, typed=[-0.145])
wrong(pid, 1, 'no-r', 1 - dt * sig ** 2 * 9, [-0.125])
wrong(pid, 1, 'no-dt', 1 - (sig ** 2 * 9 + r), [-1.29])
wrong(pid, 1, 'diag', 1 + dt * (sig ** 2 * 9 + r), [2.145])
wrong(pid, 1, 'no-square', 1 - dt * (sig ** 2 * 3 + r), [0.605])
wrong(pid, 1, 'sign', -w1, [0.145])
all_wrong_seen(pid, 1, ['no-r', 'no-dt', 'diag', 'no-square', 'sign'])
says(pid, 1, 'correct', '-0.145')
says(pid, 1, 'no-r', '2.29')
says(pid, 1, 'explain', '2.29', '-0.145', '2.145')
chk(abs(sig ** 2 * 9 + r - 2.29) < 1e-12 and abs(dt * 2.29 - 1.145) < 1e-12, f'{pid} part 1: bracket 2.29, term 1.145')

# part 2 (exact fractions)
a2, b1, c1, b2, d1, d2 = F(-23, 100), F(1145, 1000), F(-725, 10000), F(152, 100), F(215438, 10000), F(10)
m2 = a2 / b1
b2p = b2 - m2 * c1
d2p = d2 - m2 * d1
key(pid, 2, float(b2p), typed=[1.5054])
wrong(pid, 2, 'plus', float(b2 + m2 * c1), [1.5346])
wrong(pid, 2, 'wrong-c', float(b2 - m2 * F(-27, 100)), [1.4658])
all_wrong_seen(pid, 2, ['plus', 'wrong-c'])
chk(round(float(m2), 5) == -0.20087 and round(float(b2p), 4) == 1.5054 and round(float(d2p), 4) == 14.3276,
    f'{pid} part 2: m2 {float(m2)}, pivot {float(b2p)}, right side {float(d2p)}')
chk(round(float(m2 * c1), 4) == 0.0146, f'{pid} part 2 plus: product {float(m2 * c1)} against 0.0146')
says(pid, 2, 'correct', '-0.20087', '1.5054')
says(pid, 2, 'explain', '-0.20087', '1.5054', '14.3276')
# the value the printed working gives
chk(abs((1.52 - 0.20087 * 0.0725) - W(pid, 2)['answer']) <= W(pid, 2)['tol']['abs'], f'{pid} part 2: printed working refused')

# part 3 from the restated 1.5054 and 14.3276
b2r, d2r = F(15054, 10000), F(143276, 10000)
m3 = F(-5325, 10000) / b2r
b3p = F(2145, 1000) - m3 * F(-27, 100)
d3p = 0 - m3 * d2r
V3 = d3p / b3p
key(pid, 3, float(V3), typed=[2.473, round(x[2], 3)])
wrong(pid, 3, 'no-pivot', float(d3p / F(2145, 1000)), [2.363])
wrong(pid, 3, 'zero', 0.0, [0.0])
all_wrong_seen(pid, 3, ['no-pivot', 'zero'])
chk(round(float(m3), 5) == -0.35373 and round(float(b3p), 4) == 2.0495 and round(float(d3p), 4) == 5.0681,
    f'{pid} part 3: m3 {float(m3)}, pivot {float(b3p)}, right side {float(d3p)}')
chk(abs(5.0681 / 2.0495 - W(pid, 3)['answer']) <= W(pid, 3)['tol']['abs'], f'{pid} part 3: printed working refused')
chk(abs(0.35373 * 14.3276 - 5.0681) < 5e-5 and abs(2.145 - 0.35373 * 0.27 - 2.0495) < 5e-5, f'{pid} part 3: printed products')
says(pid, 3, 'question', '1.5054', '14.3276')
says(pid, 3, 'correct', '-0.35373', '2.0495', '5.0681', '2.473')
says(pid, 3, 'explain', '-0.35373', '2.0495', '5.0681', '2.473')

# part 4 from the restated 2.4728
V3r = F(24728, 10000)
num = d2r + F(27, 100) * V3r
V2 = num / b2r
key(pid, 4, float(V2), typed=[9.96, round(x[1], 2)])
wrong(pid, 4, 'sign', float((d2r - F(27, 100) * V3r) / b2r), [9.07])
wrong(pid, 4, 'skip', float(d2r / b2r), [9.52])
wrong(pid, 4, 'no-div', float(num), [15.00, 14.99])
all_wrong_seen(pid, 4, ['sign', 'skip', 'no-div'])
chk(round(float(num), 4) == 14.9953, f'{pid} part 4: numerator {float(num)}')
V1 = (21.5438 + 0.0725 * float(V2)) / 1.145
chk(round(V1, 2) == 19.45 and round(x[0], 2) == 19.45, f'{pid} part 4: V1 {V1}, {x[0]} against 19.45')
put20 = bs_put(20, K, r, sig, 0.5)
chk(round(put20, 2) == 10.00, f'{pid} part 4: formula put {put20} against 10.00')
chk(round(100 * (put20 - float(V2))) == 4, f'{pid} part 4: gap {put20 - float(V2)} against 4p')
says(pid, 4, 'question', '2.4728')
says(pid, 4, 'explain', '14.9953', '9.96', '19.45', '10.00', '4p')

# ---------------------------------------------------------------------------------------------------
# 2. p-pilot-control
pid = 'p-pilot-control'
vy, vx, cov, b = F(64), F(100), F(77), F(77, 100)
prose_says(pid, '64.0', '100.0', '77.0', '0.77', '1.3 times')
chk(cov / vx == b, f'{pid}: b-hat {float(cov / vx)}')
chk(cov * cov < vx * vy, f'{pid}: the stem covariance breaks Cauchy-Schwarz')
Sig = np.array([[64.0, 77.0], [77.0, 100.0]])
u = np.array([1.0, -0.77])
res = float(u @ Sig @ u)
chk(abs(res - float(vy - cov * cov / vx)) < 1e-9, f'{pid}: quadratic form {res} against Var(Y)(1 - rho^2)')
key(pid, 1, res, typed=[4.71])
wrong(pid, 1, 'b-one', float(np.array([1, -1.0]) @ Sig @ np.array([1, -1.0])), [10.0])
wrong(pid, 1, 'plus', 64 + 2 * 0.77 * 77 + 0.77 ** 2 * 100, [241.87])
rho = 77 / math.sqrt(64 * 100)
wrong(pid, 1, 'one-minus-rho', 64 * (1 - rho), [2.4])
all_wrong_seen(pid, 1, ['b-one', 'plus', 'one-minus-rho'])
chk(abs(rho - 0.9625) < 1e-12 and round(rho ** 2, 4) == 0.9264 and round(1 - rho ** 2, 4) == 0.0736, f'{pid} part 1: rho {rho}')
chk(abs(2 * 0.77 * 77 - 118.58) < 1e-9 and abs(0.77 ** 2 * 100 - 59.29) < 1e-9, f'{pid} part 1: cross terms')
says(pid, 1, 'correct', '118.58', '59.29', '4.71')
says(pid, 1, 'one-minus-rho', '0.9625', '0.9264', '0.0736')
says(pid, 1, 'explain', '4.71', '77/80 = 0.9625')


def smallest_n(var, half, zq, lo=1):
    n = max(lo, int(zq * zq * var / half ** 2) - 3)
    while zq * math.sqrt(var / n) > half * (1 + 1e-12):
        n += 1
    return n


n_c = smallest_n(4.71, 0.02, 1.96)
key(pid, 2, n_c, typed=[45235])
wrong(pid, 2, 'no-196', smallest_n(4.71, 0.02, 1.0))
wrong(pid, 2, 'two', smallest_n(4.71, 0.02, 2.0))
n_p = smallest_n(64.0, 0.02, 1.96)
wrong(pid, 2, 'plain', n_p)
wrong(pid, 2, 'no-square', math.ceil(round(1.96 * 4.71 / 0.02 ** 2, 6)))
all_wrong_seen(pid, 2, ['no-196', 'two', 'plain', 'no-square'])
chk(n_p == 614656, f'{pid} part 2: plain paths {n_p}')
# the whole-number key depends on the normal point: 1.96 gives 45,235, the exact 97.5% point gives 45,234
n_exact_z = smallest_n(4.71, 0.02, norm.ppf(0.975))
chk(n_exact_z == n_c or '1.96' in IT[pid]['parts'][1]['question'],
    f'{pid} part 2: the question does not state 1.96; the exact normal point {norm.ppf(0.975):.6f} gives {n_exact_z}, which the key {n_c} with tol 0 refuses')
chk(abs(1.96 ** 2 * 4.71 / 0.0004 - 45234.84) < 0.01 and abs(1.96 ** 2 - 3.8416) < 1e-12, f'{pid} part 2: 45,234.8')
says(pid, 2, 'question', '4.71')
says(pid, 2, 'correct', '45{,}234.8', '45,235')
says(pid, 2, 'explain', '3.8416', '45{,}234.8', '614{,}656')

gain = 614656 / (1.3 * 45235)
key(pid, 3, gain, typed=[10.45])
wrong(pid, 3, 'no-cost', 614656 / 45235, [13.59])
wrong(pid, 3, 'times', 1.3 * 614656 / 45235, [17.66])
all_wrong_seen(pid, 3, ['no-cost', 'times'])
chk(abs(1.3 * 45235 - 58805.5) < 1e-6, f'{pid} part 3: controlled cost')
says(pid, 3, 'question', '614,656', '45,235', '1.3')
says(pid, 3, 'explain', '58{,}805.5', '10.45', '13.59')

be = 64 / 4.71
# brute search for the largest cost, in hundredths, at which the control still wins
cmax = max(c for c in range(1, 3000) if (c / 100) * 4.71 < 64) / 100
key(pid, 4, be, typed=[13.59, round(be, 2)])
chk(abs(cmax - 13.58) < 1e-9, f'{pid} part 4: largest winning cost in hundredths {cmax}')
wrong(pid, 4, 'se', math.sqrt(be), [3.69])
wrong(pid, 4, 'gain', gain, [10.45])
all_wrong_seen(pid, 4, ['se', 'gain'])
says(pid, 4, 'explain', '13.59')
# the part prints its own key in the question: a learner copies it (finding, stays failing)
chk(not ('13.59' in IT[pid]['parts'][3]['question'] and abs(W(pid, 4)['answer'] - 13.59) < 1e-9),
    f'{pid} part 4: the question prints "64/4.71 = 13.59" and the key is 13.59, so the part is passed by copying')

# ---------------------------------------------------------------------------------------------------
# 3. p-grid-node-budget
pid = 'p-grid-node-budget'
S0, K, sig, r, T, Smax = 76, 92, 0.30, 0.03, 0.75, 276
prose_says(pid, '$S_0 = 76$', '$K = 92$', '30\\%', '3\\%', '[0, 276]', '0.002', 'nine-month')
on_nodes = [M for M in range(1, 600) if (F(S0 * M, Smax)).denominator == 1 and (F(K * M, Smax)).denominator == 1]
key(pid, 1, on_nodes[0], typed=[69])
chk(on_nodes[:4] == [69, 138, 207, 276], f'{pid} part 1: node-keeping M {on_nodes[:4]}')
wrong(pid, 1, 'half', Smax // 2)
wrong(pid, 1, 'pound', Smax)
all_wrong_seen(pid, 1, ['half', 'pound'])
chk(S0 // 4 == 19 and K // 4 == 23, f'{pid} part 1: node numbers')
says(pid, 1, 'explain', 'node 19', 'node 23')


def min_N(M, T=T):
    bound = F(9, 100) * M * M + F(3, 100)
    N = 1
    while F(T).limit_denominator(1000) / N > 1 / bound:
        N += 1
    return N


N69 = min_N(69)
key(pid, 2, N69, typed=[322])
wrong(pid, 2, 'no-T', min_N(69, 1.0))
wrong(pid, 2, 'down', N69 - 1)
wrong(pid, 2, 'no-square', math.ceil(0.75 * (0.09 * 69 + 0.03)))
all_wrong_seen(pid, 2, ['no-T', 'down', 'no-square'])
chk(abs(0.09 * 4761 + 0.03 - 428.52) < 1e-9 and round(0.75 * 428.52, 2) == 321.39, f'{pid} part 2: 428.52 and 321.39')
says(pid, 2, 'correct', '4{,}761', '321.39', '322')
says(pid, 2, 'explain', '428.52', '321.39', '-0.0219')

exact = bs_put(S0, K, r, sig, T)


def err_explicit(M, N):
    V, S = theta_put(S0, K, r, sig, T, Smax, M, N, 0.0)
    return V[round(S0 * M / Smax)] - exact


e69 = err_explicit(69, N69)
chk(round(e69, 4) == -0.0219, f'{pid} part 2: explicit error at M = 69, N = 322 is {e69}, printed -0.0219')
ks = [k for k in range(1, 12) if 0.0219 / k ** 2 < 0.002]
key(pid, 3, 69 * ks[0], typed=[276])
wrong(pid, 3, 'linear', 69 * min(k for k in range(1, 40) if 0.0219 / k < 0.002))
kx = math.sqrt(0.0219 / 0.002)
wrong(pid, 3, 'off-node', math.ceil(69 * kx))
wrong(pid, 3, 'k3', 69 * 3)
all_wrong_seen(pid, 3, ['linear', 'off-node', 'k3'])
chk(round(kx, 2) == 3.31 and round(kx * kx, 2) == 10.95, f'{pid} part 3: k {kx}')
chk(round(0.0219 / 9, 5) == 0.00243 and round(0.0219 / 16, 5) == 0.00137, f'{pid} part 3: predictions')
N207, N276 = min_N(207), min_N(276)
e207, e276 = err_explicit(207, N207), err_explicit(276, N276)
chk(abs(e207) > 0.002 and round(e207, 5) == -0.00243, f'{pid} part 3: explicit error at M = 207 is {e207}')
chk(abs(e276) < 0.002 and round(e276, 5) == -0.00137, f'{pid} part 3: explicit error at M = 276 is {e276}, printed -0.00137')
says(pid, 3, 'question', '0.0219', '0.002')
says(pid, 3, 'correct', '10.95')
says(pid, 3, 'k3', '0.00243')
says(pid, 3, 'off-node', '3.31')
says(pid, 3, 'explain', '0.00243', '0.00137', '-0.00137')

key(pid, 4, N276, typed=[5142])
wrong(pid, 4, 'scaled', 16 * N69)
wrong(pid, 4, 'no-T', min_N(276, 1.0))
wrong(pid, 4, 'down', N276 - 1)
all_wrong_seen(pid, 4, ['scaled', 'no-T', 'down'])
chk(276 ** 2 == 76176 and abs(0.09 * 76176 + 0.03 - 6855.87) < 1e-9 and round(0.75 * 6855.87, 1) == 5141.9, f'{pid} part 4: bound')
says(pid, 4, 'correct', '76{,}176', '5{,}141.9')
says(pid, 4, 'explain', '6{,}855.87', '5{,}141.9')

ratio = (276 * N276) / (3 * 276 * 100)
key(pid, 5, ratio, typed=[17.14])
wrong(pid, 5, 'no-cost', N276 / 100, [51.42])
wrong(pid, 5, 'scaled', 16 * N69 / 300, [17.17])
all_wrong_seen(pid, 5, ['no-cost', 'scaled'])
chk(276 * 5142 == 1419192 and 3 * 276 * 100 == 82800, f'{pid} part 5: unit counts')
Vcn, Scn = theta_put(S0, K, r, sig, T, Smax, 276, 100, 0.5, implicit_start=2)
ecn = Vcn[S0] - exact
chk(abs(ecn) < 0.002 and round(ecn, 4) == -0.0015, f'{pid} part 5: Crank-Nicolson error at M = 276, N = 100 is {ecn}, printed -0.0015')
says(pid, 5, 'question', '5{,}142')
says(pid, 5, 'explain', '1{,}419{,}192', '82{,}800', '17.14', '-0.0015')

# ---------------------------------------------------------------------------------------------------
# 4. p-digital-pairs
pid = 'p-digital-pairs'
p, pay = F(1, 5), 50 * F(96, 100)
prose_says(pid, '£50', '$p = 0.2$', '0.96', '£48')
chk(pay == 48, f'{pid}: discounted payoff {pay}')
mean = pay * p
var = pay ** 2 * p - mean ** 2
s = math.sqrt(var)
key(pid, 1, s, typed=[19.2])
wrong(pid, 1, 'no-disc', 50 * math.sqrt(p * (1 - p)), [20.0])
wrong(pid, 1, 'p-only', 48 * math.sqrt(p), [21.47])
wrong(pid, 1, 'var', float(var), [368.64])
all_wrong_seen(pid, 1, ['no-disc', 'p-only', 'var'])
chk(float(mean) == 9.6, f'{pid} part 1: price {float(mean)}')
says(pid, 1, 'explain', '0.16', '368.64', '19.20', '9.60')

se = s / math.sqrt(25600)
key(pid, 2, se, typed=[0.12])
wrong(pid, 2, 'no-disc', 20 / 160, [0.125])
wrong(pid, 2, 'by-n', 19.2 / 25600, [0.001])
wrong(pid, 2, 'var', 368.64 / 160, [2.304])
all_wrong_seen(pid, 2, ['no-disc', 'by-n', 'var'])
chk(round(1.96 * se, 2) == 0.24, f'{pid} part 2: half-width {1.96 * se}')
says(pid, 2, 'question', '19.2', '25,600')
says(pid, 2, 'explain', '160', '0.120', '0.24', '9.60')

# joint table of (B1, B2) for the draws z and -z: B1 = 1 on the top fifth, B2 = 1 on the bottom fifth
joint = {(1, 0): p, (0, 1): p, (0, 0): 1 - 2 * p, (1, 1): F(0)}
E1 = sum(q * a for (a, bb), q in joint.items())
E12 = sum(q * a * bb for (a, bb), q in joint.items())
covB = E12 - E1 * E1
varB = E1 - E1 * E1
rho = covB / varB
key(pid, 3, float(rho), typed=[-0.25])
wrong(pid, 3, 'minus-p', -float(p), [-0.2])
wrong(pid, 3, 'sign', -float(rho), [0.25])
wrong(pid, 3, 'cov', float(covB), [-0.04])
all_wrong_seen(pid, 3, ['minus-p', 'sign', 'cov'])
chk(rho == -p / (1 - p), f'{pid} part 3: rho against -p/(1 - p)')
rng = np.random.default_rng(20261116)
z = rng.standard_normal(2_000_000)
c = norm.ppf(0.8)
y1, y2 = 48.0 * (z > c), 48.0 * (-z > c)
rsim = np.corrcoef(y1, y2)[0, 1]
chk(abs(rsim + 0.25) < 0.005 and float((y1 * y2).max()) == 0.0, f'{pid} part 3: simulated pair correlation {rsim}')
says(pid, 3, 'correct', '-0.04', '0.16', '-0.25')

eff = 1 / (1 + float(rho))
pair_var = float(var) * (1 + float(rho)) / 2
chk(abs(np.var((y1 + y2) / 2) - pair_var) / pair_var < 0.01, f'{pid} part 4: simulated pair-mean variance')
key(pid, 4, (float(var) / 2) / pair_var, typed=[1.33])
wrong(pid, 4, 'vrf', 1 / (1 - float(rho) ** 2), [1.07])
wrong(pid, 4, 'inverted', 1 + float(rho), [0.75])
wrong(pid, 4, 'one-minus', 1 / (1 - float(rho)), [0.8])
all_wrong_seen(pid, 4, ['vrf', 'inverted', 'one-minus'])
says(pid, 4, 'question', '-0.25')
says(pid, 4, 'correct', '1.33')

pairs = 1
target = 0.05
pairs = next(n for n in range(55000, 56000) if math.sqrt(pair_var / n) <= target * (1 + 1e-12))
key(pid, 5, pairs, typed=[55296])
wrong(pid, 5, 'payoffs', 2 * pairs)
wrong(pid, 5, 'plain', round(float(var) / target ** 2))
wrong(pid, 5, 'one-minus', round(float(var) * (1 - float(rho)) / 2 / target ** 2))
all_wrong_seen(pid, 5, ['payoffs', 'plain', 'one-minus'])
chk(abs(pair_var - 138.24) < 1e-9 and F(110592, 147456) == F(3, 4), f'{pid} part 5: pair variance and the quarter')
says(pid, 5, 'question', '19.2', '-0.25', '0.05')
says(pid, 5, 'correct', '138.24', '55{,}296')
says(pid, 5, 'explain', '138.24', '55{,}296', '110,592', '147,456', '1.33')

# ---------------------------------------------------------------------------------------------------
# forms: every part names its rounding; no percentage part without a unit
for it in D['items']:
    for k, part in enumerate(it['parts'], 1):
        q = part['question']
        chk(any(t in q for t in ('decimal places', 'whole number', 'smallest whole')), f"{it['id']} part {k}: no form stated")
        chk(not ('percent' in q.lower() and part['widget'].get('unit') != '%'), f"{it['id']} part {k}: percentage with no unit")
        if k > 1:
            chk('Using' in q or any(ch.isdigit() for ch in q), f"{it['id']} part {k}: restates no value")

print(f'{n_checks - len(findings)} of {n_checks} checks passed; {len(findings)} FINDING line(s)')
