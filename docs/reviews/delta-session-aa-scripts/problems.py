"""Delta read, session AA: every number the problems fix pass (d) changed, by two methods.

Run from the repo root with the scratchpad venv Python. Exits 1 on any failure.
"""
import itertools
import json
import math
import sys
from fractions import Fraction as F

import numpy as np

C = 'app/content/courses/'
fails = 0


def check(name, ok, detail=''):
    global fails
    print(('ok   ' if ok else 'FAIL ') + name + (' | ' + str(detail) if detail else ''))
    if not ok:
        fails += 1


def item(path, pid):
    d = json.load(open(C + path))
    return next(p for p in d.get('problems', d.get('items')) if p['id'] == pid)


def bands_disjoint(w):
    """No slip band meets the answer band or another slip band."""
    a, t = w['answer'], w['tol']['abs']
    bands = [(a - t, a + t, 'answer')]
    for s in w.get('wrong', []):
        bands.append((s['value'] - s['tol']['abs'], s['value'] + s['tol']['abs'], s['id']))
    bad = []
    for (lo1, hi1, n1), (lo2, hi2, n2) in itertools.combinations(bands, 2):
        if lo1 <= hi2 and lo2 <= hi1:
            bad.append((n1, n2))
    return bad


# ---------- A1: supplier walk, four acceptance rules ----------
deg = {'H': 4, 'A': 2, 'B': 2, 'C': 1, 'D': 1}
nb = {'H': 'ABCD', 'A': 'HB', 'B': 'HA', 'C': 'H', 'D': 'H'}
names = 'HABCD'
rules = {
    'ratio': lambda i, j: min(1, F(deg[i], deg[j])),
    'flipped': lambda i, j: min(1, F(deg[j], deg[i])),
    'always': lambda i, j: F(1),
    'inverse (1/deg i)': lambda i, j: F(1, deg[i]),
    'old inverse (1/deg j)': lambda i, j: F(1, deg[j]),
}


def matrix(rule):
    P = [[F(0)] * 5 for _ in range(5)]
    for a, i in enumerate(names):
        for j in nb[i]:
            P[a][names.index(j)] = F(1, deg[i]) * rule(i, j)
        P[a][a] = 1 - sum(P[a])
    return P


def stationary_exact(P):
    # method 1: detailed balance along a spanning tree from H (the chain is reversible for
    # each rule, which is then verified on every edge and by pi P = pi)
    pi = {0: F(1)}
    for a in range(1, 5):
        pi[a] = pi[0] * P[0][a] / P[a][0]
    tot = sum(pi.values())
    pi = [pi[a] / tot for a in range(5)]
    for b in range(5):
        assert sum(pi[a] * P[a][b] for a in range(5)) == pi[b]
    return pi


def stationary_eig(P):
    # method 2: left eigenvector of the float matrix
    M = np.array([[float(x) for x in r] for r in P])
    w, v = np.linalg.eig(M.T)
    k = int(np.argmin(abs(w - 1)))
    x = np.real(v[:, k])
    return x / x.sum()


uniform = []
for name, rule in rules.items():
    P = matrix(rule)
    pe, pf = stationary_exact(P), stationary_eig(P)
    check(f'supplier {name}: two methods agree', np.allclose([float(x) for x in pe], pf, atol=1e-12),
          [str(x) for x in pe])
    if all(x == F(1, 5) for x in pe):
        uniform.append(name)
check('supplier: uniform under ratio and the OLD 1/deg(j) only', uniform == ['ratio', 'old inverse (1/deg j)'], uniform)
check('supplier: 1/deg(i) puts 16/26 at H', stationary_exact(matrix(rules['inverse (1/deg i)']))[0] == F(16, 26))
P = matrix(rules['ratio'])
check('supplier parts 4, 5: stay chances 0, .25, .25, .75, .75 and repeat share 0.4',
      [P[a][a] for a in range(5)] == [0, F(1, 4), F(1, 4), F(3, 4), F(3, 4)]
      and sum(F(1, 5) * P[a][a] for a in range(5)) == F(2, 5))
sp = item('markov/problems-4.json', 'p-supplier-survey')['parts'][2]['widget']['options']
check('supplier: exactly one option keyed, inverse text is 1/deg(i)',
      sum(1 for o in sp if o.get('correct')) == 1 and 'deg(i)' in sp[3]['text'] and 'deg(j)' not in sp[3]['text'])

# ---------- A2, A3: taxi rank ----------
def pi0(spaces):
    w = [F(3, 2) ** k for k in range(spaces + 1)]
    return w[0] / sum(w)


check('taxi: pi0 = 8/65, 16/211', pi0(3) == F(8, 65) and pi0(4) == F(16, 211))
check('taxi: lost an hour 11.8154 and 7.2796, saving 4.5358',
      abs(96 * pi0(3) - 11.8154) < 5e-5 and abs(96 * pi0(4) - 7.2796) < 5e-5
      and abs(float(96 * (pi0(3) - pi0(4))) - 4.5358) < 5e-5)
# method 2 and the Poisson claim: continuous-time simulation, hourly loss counts
rng = np.random.default_rng(20261110)
hours = 20000
n = int(4 * 60 * hours * 1.02)
gaps = rng.exponential(1 / 4, n)
t = np.cumsum(gaps)
is_taxi = rng.random(n) < 0.6
state, lost_times = 0, []
for k in range(n):
    if is_taxi[k]:
        state = min(3, state + 1)
    elif state == 0:
        lost_times.append(t[k])
    else:
        state -= 1
lost_times = np.array(lost_times)
lost_times = lost_times[lost_times < 60 * hours]
counts = np.bincount((lost_times // 60).astype(int), minlength=hours)
check('taxi: simulated loss rate near 11.82', abs(counts.mean() - 11.8154) < 0.15, round(counts.mean(), 3))
check('taxi: hourly losses are over-dispersed (not Poisson)', counts.var() / counts.mean() > 2,
      round(counts.var() / counts.mean(), 2))

# ---------- A4: regime sampler, plain rule ----------
w = {'L': F(2), 'M': F(5), 'H': F(3)}
q = {('L', 'M'): F(1), ('H', 'M'): F(1), ('M', 'L'): F(3, 10), ('M', 'H'): F(7, 10)}
plain = {k: q[k] * min(1, w[k[1]] / w[k[0]]) for k in q}
mh = {k: q[k] * min(1, w[k[1]] * q[(k[1], k[0])] / (w[k[0]] * q[k])) for k in q}
check('regime: plain moves 1, 0.12, 0.42, 1',
      [plain[k] for k in [('L', 'M'), ('M', 'L'), ('M', 'H'), ('H', 'M')]] == [1, F(3, 25), F(21, 50), 1])
wt = [F(1), plain[('L', 'M')] / plain[('M', 'L')]]
wt.append(wt[1] * plain[('M', 'H')] / plain[('H', 'M')])
check('regime: plain rule gives Mid 50/77', wt[1] / sum(wt) == F(50, 77))
Pm = np.array([[0, 1, 0], [0.12, 0.46, 0.42], [0, 1, 0]])
check('regime: matrix power agrees', abs(np.linalg.matrix_power(Pm, 400)[0, 1] - 50 / 77) < 1e-12)
check('regime: MH moves 0.75, 0.3, 0.6, 1 and reject share 0.1',
      [mh[k] for k in [('L', 'M'), ('M', 'L'), ('M', 'H'), ('H', 'M')]] == [F(3, 4), F(3, 10), F(3, 5), 1]
      and F(1, 5) * F(1, 4) + F(1, 2) * F(1, 10) == F(1, 10))

# ---------- A7: ticket stages slip ----------
s = 0.2
check('ticket: 0.5/(0.5 - s) = 1/(1 - 2s), not 1/(1 - 0.5s)',
      abs(0.5 / (0.5 - s) - 1 / (1 - 2 * s)) < 1e-12 and abs(0.5 / (0.5 - s) - 1 / (1 - 0.5 * s)) > 0.1)

# ---------- A6: machine faults ----------
# f(x, g) = exp(-x - g); P(G > 2) = exp(-2); second method: integrate the wedge numerically
from scipy import integrate
val, _ = integrate.dblquad(lambda y, x: math.exp(-y), 0, 60, lambda x: x + 2, lambda x: 80)
check('faults: P(G > 2) = exp(-2) = 0.1353', abs(val - math.exp(-2)) < 1e-7 and round(math.exp(-2), 4) == 0.1353)

# ---------- A9: file retry ----------
def retry_mean(err_add, to_add):
    # m = 0.5*1 + 0.3*(err_add + m) + 0.2*(to_add + m)
    return (F(1, 2) + F(3, 10) * err_add + F(2, 10) * to_add) / (1 - F(1, 2))


check('retry: m = 4.2; carried 3; carried-both 1',
      retry_mean(2, 5) == F(21, 5) and retry_mean(0, 5) == 3 and retry_mean(0, 0) == 1)
# method 2: series for m, sum over number of failures
m = sum((0.5 ** k) * 0.5 * (1 + k * 3.2) for k in range(200))
check('retry: series gives 4.2', abs(m - 4.2) < 1e-12)
wd = item('random-vars/problems-4.json', 'p-file-retry')['parts'][1]['widget']
check('retry: bands disjoint, carried-both = 1 with a byKey line',
      not bands_disjoint(wd) and any(s['id'] == 'carried-both' and s['value'] == 1 for s in wd['wrong'])
      and 'carried-both' in item('random-vars/problems-4.json', 'p-file-retry')['parts'][1]['feedback']['byKey'])

# ---------- A10: start-up rounds ----------
lr = [math.log(1.5), math.log(0.6)]
mu = sum(lr) / 2
var = sum((x - mu) ** 2 for x in lr) / 2
EN, VN = 4, 2
check('startup: E ln R = -0.0527, Var = 0.2099', round(mu, 4) == -0.0527 and round(var, 4) == 0.2099)
exact = EN * var + VN * mu ** 2
# method 2: enumerate N and the number of up rounds
m1 = m2 = 0.0
for nn, pn in [(2, .25), (4, .5), (6, .25)]:
    for k in range(nn + 1):
        p = pn * math.comb(nn, k) / 2 ** nn
        x = k * lr[0] + (nn - k) * lr[1]
        m1 += p * x
        m2 += p * x * x
check('startup: Var(ln W) = 0.8452 both ways', abs(exact - (m2 - m1 * m1)) < 1e-12 and abs(exact - 0.8452) < 0.0005, exact)  # exact 0.84514; the key 0.8452 uses the rounded values the question hands over
slip_a = 16 * 0.2099
slip_b = 16 * 0.2099 + 2 * 0.0527 ** 2
slip_c = 16 * var + 2 * mu ** 2
wd = item('random-vars/problems-5.json', 'p-startup-rounds')['parts'][2]['widget']
cs = next(s for s in wd['wrong'] if s['id'] == 'count-squared')
lo, hi = cs['value'] - cs['tol']['abs'], cs['value'] + cs['tol']['abs']
check('startup: count-squared band takes 3.3584, 3.3640 and the unrounded route',
      all(lo <= round(v, 4) <= hi for v in (slip_a, slip_b, slip_c)), (round(slip_a, 4), round(slip_b, 4), round(slip_c, 4), lo, hi))
check('startup: bands disjoint', not bands_disjoint(wd), bands_disjoint(wd))

# ---------- A11: courier vans ----------
Pj = {(1, 0): F(36, 100), (1, 1): F(18, 100), (1, 2): F(6, 100), (2, 0): F(12, 100), (2, 1): F(20, 100), (2, 2): F(8, 100)}
EY = sum(p * y for (x, y), p in Pj.items())
py1 = Pj[(1, 1)] + Pj[(2, 1)]
py2 = Pj[(1, 2)] + Pj[(2, 2)]
check('vans: P(Y=1) = 0.38, column check 0.38 + 2(0.14) = 0.66, bill 3.96',
      py1 == F(38, 100) and py1 + 2 * py2 == EY == F(66, 100) and 6 * EY == F(396, 100)
      and F(6, 10) * F(1, 2) + F(4, 10) * F(9, 10) == EY)

# ---------- A12: two-loss cut ----------
def pattern_wait(pat, pl=F(3, 10)):
    pr = lambda s: math.prod(pl if c == 'L' else 1 - pl for c in s)
    return sum(1 / pr(pat[:k]) for k in range(1, len(pat) + 1) if pat[:k] == pat[-k:])


def pattern_wait_linear(pat, pl=0.3):
    # method 2: first-step equations on the prefix automaton
    n = len(pat)
    A = np.zeros((n, n))
    b = np.ones(n)
    for st in range(n):
        A[st, st] += 1
        for c, p in (('L', pl), ('W', 1 - pl)):
            s2 = pat[:st] + c
            while s2 and not pat.startswith(s2):
                s2 = s2[1:]
            if len(s2) < n:
                A[st, len(s2)] -= p
    return np.linalg.solve(A, b)[0]


check('cut: LL wait 130/9', pattern_wait('LL') == F(130, 9) and abs(pattern_wait_linear('LL') - 130 / 9) < 1e-9)
tw = pattern_wait('LWL')
check('cut: LWL wait 19.2063 both ways', abs(float(tw) - 19.2063) < 5e-5 and abs(pattern_wait_linear('LWL') - float(tw)) < 1e-9, float(tw))
wd = item('markov/problems-5.json', 'p-two-loss-cut')['parts'][4]['widget']
a, tol = wd['answer'], wd['tol']['abs']
routes = {'exact': 60 * float(tw), 'nearest pound': 1152, 'from 19.21': round(60 * 19.21), 'from 19.2': 60 * 19.2,
          'from 3.33 + 15.87': 60 * (3.33 + 15.87)}
check('cut: answer 1152.38, tol 1 takes 1152 and 1153', a == 1152.38 and tol == 1
      and all(abs(v - a) <= tol for k, v in routes.items() if k != 'from 19.2'), routes)
check('cut: bands disjoint', not bands_disjoint(wd))
check('cut: slips 952.38 and 866.67', abs(60 / 0.063 - 952.38) < 0.005 and abs(60 * 130 / 9 - 866.67) < 0.005)

# ---------- B1: token draw ----------
hands = list(itertools.combinations('GGGSSSSSSS', 4))  # 210 hands by position
idx = list(itertools.combinations(range(10), 4))
g = [sum(1 for i in h if i < 3) for h in idx]
p2 = F(sum(1 for x in g if x >= 2), 210)
p3 = F(sum(1 for x in g if x >= 3), 210)
check('token: hands give 1/3 and 1/30, price 43.50', p2 == F(1, 3) and p3 == F(1, 30) and 38 + 15 * (p2 + p3) == F(87, 2))
b2 = 1 - F(7, 10) ** 4 - 4 * F(3, 10) * F(7, 10) ** 3
b3 = 4 * F(3, 10) ** 3 * F(7, 10) + F(3, 10) ** 4
# method 2: enumerate 10^4 ordered draws with replacement
cnt2 = cnt3 = 0
for d in itertools.product(range(10), repeat=4):
    k = sum(1 for i in d if i < 3)
    cnt2 += k >= 2
    cnt3 += k >= 3
check('token: with replacement 0.3483 and 0.0837 both ways', b2 == F(cnt2, 10 ** 4) == F(3483, 10000) and b3 == F(cnt3, 10 ** 4) == F(837, 10000))
check('token: carried 44.48, carried-half 43.7245',
      38 + 15 * (b2 + b3) == F(4448, 100) and 38 + 15 * (b2 + p3) == F(437245, 10000))
wd = item('random-vars/problems-2.json', 'p-token-draw')['parts'][4]['widget']
ch = next(s for s in wd['wrong'] if s['id'] == 'carried-half')
check('token: carried-half band takes 43.72 and 43.7245; bands disjoint',
      all(abs(v - ch['value']) <= ch['tol']['abs'] for v in (43.72, 43.7245)) and not bands_disjoint(wd), bands_disjoint(wd))

# ---------- every wrong id of the six files has its byKey line, and the files parse ----------
for f in ['limits-thm/problems-4.json', 'markov/problems-4.json', 'markov/problems-5.json',
          'random-vars/problems-2.json', 'random-vars/problems-4.json', 'random-vars/problems-5.json']:
    d = json.load(open(C + f))
    miss = []
    for p in d.get('problems', d.get('items')):
        for k, part in enumerate(p['parts']):
            wdg = part['widget']
            ids = [s['id'] for s in wdg.get('wrong', [])]
            bk = part['feedback'].get('byKey', {})
            if sorted(ids) != sorted(bk):
                miss.append((p['id'], k + 1))
            if wdg['kind'] == 'numeric' and bands_disjoint(wdg):
                miss.append((p['id'], k + 1, 'bands', bands_disjoint(wdg)))
    check(f'{f}: byKey ids match and no bands meet', not miss, miss)

print('failures:', fails)
sys.exit(1 if fails else 0)
