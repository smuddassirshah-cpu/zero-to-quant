"""Delta read AH: independent recompute. Standard library only, imports no other script.
Run from the repo root: python3 docs/reviews/review-delta-ah-scripts/check.py"""
import itertools
import json
import math
import sys
from fractions import Fraction as F

n_ok = 0
bad = []


def ok(c, msg):
    global n_ok
    if c:
        n_ok += 1
    else:
        bad.append(msg)
        print('FAIL', msg)


def load(path, pid):
    d = json.load(open(path))
    key = [k for k in d if isinstance(d[k], list)][0]
    return [p for p in d[key] if p['id'] == pid][0]


def takes(w, x):
    return abs(x - w['answer']) <= w['tol'].get('abs', 0) + 1e-12


def slip_takes(s, x):
    return abs(x - s['value']) <= s['tol'].get('abs', 0) + 1e-12


def trunc(x, d):
    return math.floor(x * 10**d) / 10**d


def Phi(z):
    return 0.5 * math.erfc(-z / math.sqrt(2))


# ---------- 1. topology p-signal-bands ----------
tp = load('app/content/courses/topology/problems-2.json', 'p-signal-bands')
# part 1: a set is a list of pieces (lo, hi, lo_closed, hi_closed)
sets1 = {'(-2,2)': [(-2, 2, 0, 0)], '(0,3)': [(0, 3, 0, 0)], '(-3,-1)u(1,3)': [(-3, -1, 0, 0), (1, 3, 0, 0)],
         '[-1,1]': [(-1, 1, 1, 1)], '(-2,1)': [(-2, 1, 0, 0)]}


def is_open(s):
    return all(not a[2] and not a[3] for a in s)


def mirror(s):
    return sorted((-b, -a, hc, lc) for a, b, lc, hc in s)


in_tau = [k for k, s in sets1.items() if is_open(s) and mirror(s) == sorted(s)]
ok(len(in_tau) == tp['parts'][0]['widget']['answer'] == 2, 'topology p1 key 2')
ok(sum(is_open(s) for s in sets1.values()) == 4 and sum(mirror(s) == sorted(s) for s in sets1.values()) == 3,
   'topology p1 slips 4, 3')


# part 2: h is continuous into tau iff |h| is continuous; look for jumps of |h| at every quarter point of [-4, 4]
def sgn(t):
    return 1 if t >= 0 else -1


maps = {'t': lambda t: t, 's': sgn, 'floor': math.floor, 't+s': lambda t: t + sgn(t), '2+s': lambda t: 2 + sgn(t)}


def jumps(g):
    e = 1e-9
    return any(abs(g(c - e) - g(c)) > 1e-6 or abs(g(c + e) - g(c)) > 1e-6 for c in [i / 4 for i in range(-16, 17)])


cont_tau = [k for k, h in maps.items() if not jumps(lambda t, h=h: abs(h(t)))]
cont_usual = [k for k, h in maps.items() if not jumps(h)]
ok(sorted(cont_tau) == ['s', 't', 't+s'] and tp['parts'][1]['widget']['answer'] == 3, 'topology p2 key 3')
ok(cont_usual == ['t'], 'topology p2 slip usual 1')
ok(all(abs(abs(t + sgn(t)) - (1 + abs(t))) < 1e-12 for t in [i / 7 for i in range(-30, 31)]), '|t+s(t)| = 1+|t|')


# part 3: A is connected in tau_A iff |A| is connected in [0, inf)
def absimg(piece):
    a, b, lc, hc = piece
    if a >= 0:
        return (a, b, lc, hc)
    if b <= 0:
        return (-b, -a, hc, lc)
    return (0, max(-a, b), 1, lc if -a > b else hc)


def connected(pieces):
    ps = sorted(set(pieces))
    cur = ps[0]
    for q in ps[1:]:
        if q[0] < cur[1] or (q[0] == cur[1] and (q[2] or cur[3])):
            cur = (cur[0], max(cur[1], q[1]), cur[2], q[3] if q[1] >= cur[1] else cur[3])
        else:
            return False
    return True


A = {'{-2,2}': [(-2, -2, 1, 1), (2, 2, 1, 1)], '{1,2}': [(1, 1, 1, 1), (2, 2, 1, 1)],
     '(-1,0)u(0,1)': [(-1, 0, 0, 0), (0, 1, 0, 0)], '[-3,-2]u[1,2]': [(-3, -2, 1, 1), (1, 2, 1, 1)],
     '[-4,-3]u[1,2]': [(-4, -3, 1, 1), (1, 2, 1, 1)], '[-1,2]': [(-1, 2, 1, 1)]}
conn_tau = [k for k, v in A.items() if connected([absimg(p) for p in v])]
conn_usual = [k for k, v in A.items() if connected(v)]
ok(len(conn_tau) == tp['parts'][2]['widget']['answer'] == 4 and '{1,2}' not in conn_tau
   and '[-4,-3]u[1,2]' not in conn_tau, 'topology p3 key 4')
ok(conn_usual == ['[-1,2]'], 'topology p3 slip usual 1')

# the lemma "A connected iff |A| connected" by brute force on a finite model:
# points -2..2, a topology Ws on the sizes 0, 1, 2, and its pullback under |x|
pts = [-2, -1, 0, 1, 2]
Ws = [frozenset(), frozenset({0}), frozenset({0, 1}), frozenset({0, 1, 2}), frozenset({2}), frozenset({0, 2})]
ok(all((a | b) in Ws and (a & b) in Ws for a in Ws for b in Ws), 'model family is a topology')


def conn_sub(points, opens):
    tr = {frozenset(o & points) for o in opens}
    return not any(u and v and not (u & v) and (u | v) == points for u in tr for v in tr)


up = [frozenset(x for x in pts if abs(x) in w) for w in Ws]
for rr in range(1, 6):
    for sub in itertools.combinations(pts, rr):
        Aset = frozenset(sub)
        ok(conn_sub(Aset, up) == conn_sub(frozenset(abs(x) for x in Aset), Ws), 'lemma on finite model %s' % (sub,))


# part 4 counterexamples
def p_zero(t):
    return -3 - 2 * t if t < 0.5 else 3 + 2 * t


def p_four(t):
    return -3 - 2 * t if t < 1 else 5


grid = [i / 1000 for i in range(1001)]
for nm, p in (('zero', p_zero), ('four', p_four)):
    ok(p(0) == -3 and p(1) == 5 and all(abs(abs(p(t)) - (3 + 2 * t)) < 1e-12 for t in grid),
       'p4 %s: ends and size 3+2t' % nm)
ok(all(p_zero(t) != 0 for t in grid) and all(p_four(t) != 4 for t in grid) and p_four(0.5) == -4,
   'p4 counterexamples miss 0 and 4')
ok([o['id'] for o in tp['parts'][3]['widget']['options'] if o.get('correct')] == ['size-four'],
   'topology p4 choice size-four')

# ---------- 2. pdes p-grid-budget ----------
gb = load('app/content/courses/pdes/problems-3.json', 'p-grid-budget')


def cn(S, K, r, sig, T, nx, L=1.0):
    """Crank-Nicolson on u_tau = u_xx, x in [-L, L], nt = nx/5; u = 0 at -L, the far-field heat solution at +L."""
    k = 2 * r / sig**2
    tmax = 0.5 * sig**2 * T
    nt = nx // 5
    h = 2 * L / nx
    dt = tmax / nt
    lam = dt / h**2
    xs = [-L + i * h for i in range(nx + 1)]
    a, b = 0.5 * (k - 1), 0.5 * (k + 1)
    u = [max(math.exp(b * x) - math.exp(a * x), 0.0) for x in xs]

    def right(t):
        return math.exp(b * L + b * b * t) - math.exp(a * L + a * a * t)

    m = nx - 1
    dg, off = 1 + lam, -0.5 * lam
    for j in range(1, nt + 1):
        t = j * dt
        rhs = [(1 - lam) * u[i] + 0.5 * lam * (u[i - 1] + u[i + 1]) for i in range(1, nx)]
        rhs[-1] += 0.5 * lam * right(t)
        cp = [0.0] * m
        dp = [0.0] * m
        cp[0] = off / dg
        dp[0] = rhs[0] / dg
        for i in range(1, m):
            den = dg - off * cp[i - 1]
            cp[i] = off / den
            dp[i] = (rhs[i] - off * dp[i - 1]) / den
        sol = [0.0] * m
        sol[-1] = dp[-1]
        for i in range(m - 2, -1, -1):
            sol[i] = dp[i] - cp[i] * sol[i + 1]
        u = [0.0] + sol + [right(t)]
    x0 = math.log(S / K)
    i0 = int(round((x0 + L) / h))
    return K * math.exp(-a * x0 - b * b * tmax) * u[i0]


runs = {n: cn(120, 120, 0.045, 0.18, 1.25, n) for n in (200, 300, 400, 600, 1200, 2400)}
print('CN runs', {n: round(v, 7) for n, v in runs.items()})
ok(abs(runs[200] - 12.9963192) < 5e-8, 'printed 200 run 12.9963192, mine %.7f' % runs[200])
ok(abs(runs[300] - 12.9975576) < 5e-8, 'printed 300 run 12.9975576, mine %.7f' % runs[300])
# The limit: the grid ratios drift under 4 (3.86, 3.74 on 1200 to 9600 in a side run), so a Richardson step on
# two runs undershoots. The closed form is used as the limit here only, to test the two explain sentences;
# the 2,400 run must sit just under it.
_s, _T, _r = 0.18, 1.25, 0.045
_d1 = (_r + _s * _s / 2) * _T / (_s * math.sqrt(_T))
limit = 120 * Phi(_d1) - 120 * math.exp(-_r * _T) * Phi(_d1 - _s * math.sqrt(_T))
ok(0 < limit - runs[2400] < 2e-5 and runs[1200] < runs[2400], 'runs rise to the closed form %.9f' % limit)
gap400, gap600 = (limit - runs[400]) * 1e6, (limit - runs[600]) * 1e6
print('limit %.8f gap400 %.2f gap600 %.2f' % (limit, gap400, gap600))
gap = F('12.9975576') - F('12.9963192')
C = gap / (F(1, 100)**2 - F(1, 150)**2)
ok(gap == F('0.0012384') and C == F('22.2912'), 'C = 22.2912 exactly')
w = [p['widget'] for p in gb['parts']]
keys = [float(C), float(C * F(1, 200)**2 * 10**6), float(C * F(1, 200)**2 * 10**6 / F(9, 4)), float(F(9, 4)**2)]
ok([round(x, 6) for x in keys] == [22.2912, 557.28, 247.68, 5.0625], 'keys %s' % keys)
for i in range(4):
    ok(abs(w[i]['answer'] - keys[i]) < 1e-9, 'grid p%d stored key' % (i + 1))
slips = [{'n-not-h': gap / (F(1, 200)**2 - F(1, 300)**2), 'no-square': gap / (F(1, 100) - F(1, 150)),
          'one-run': gap / F(1, 100)**2},
         {'unit-length': F('22.29') * F(1, 400)**2 * 10**6, 'wrong-run': F('22.29') * F(1, 150)**2 * 10**6},
         {'per-interval': F('557.28') / F(9, 4)**2, 'first-order': F('557.28') / F(3, 2)},
         {'linear': F(9, 4), 'root': F(3, 2)}]
for i in range(4):
    for sl in w[i]['wrong']:
        ok(abs(sl['value'] - float(slips[i][sl['id']])) < 1e-3,
           'grid p%d slip %s value %s vs %s' % (i + 1, sl['id'], sl['value'], float(slips[i][sl['id']])))
# bands: rounded and truncated at the asked places, and the answer the carried (printed) figures give
asked = [2, 0, 2, 2]
carried = [round(x, 9) for x in (18000 * 0.0012384, 22.29 * 0.000025 * 1e6, 557.28 / 2.25, (557.28 / 247.68)**2)]
for i in range(4):
    kk = keys[i]
    for nm, x in (('rounded', round(kk, asked[i])), ('truncated', trunc(kk, asked[i])), ('carried', carried[i]),
                  ('carried rounded', round(carried[i], asked[i])), ('carried truncated', trunc(carried[i], asked[i]))):
        ok(takes(w[i], x), 'grid p%d band takes %s %s' % (i + 1, nm, x))
    step = 10**-asked[i]
    for x in (round(kk, asked[i]) + step, round(kk, asked[i]) - step):
        ok(not takes(w[i], x), 'grid p%d band refuses neighbour %s' % (i + 1, x))
# every slip (stored, true, rounded and truncated at its part's places) against every part's key band
for i in range(4):
    for sl in w[i]['wrong']:
        true = float(slips[i][sl['id']])
        forms = (sl['value'], true, round(true, asked[i])) + ((trunc(true, asked[i]),) if asked[i] else ())
        for j in range(4):
            for x in forms:
                ok(not takes(w[j], x), 'slip %s of p%d (%s) falls in key band of p%d' % (sl['id'], i + 1, x, j + 1))
        for x in forms:
            ok(slip_takes(sl, x), 'slip %s of p%d does not take its own figure %s' % (sl['id'], i + 1, x))
# slip with the unrounded C in part 2 (a learner who kept 22.2912)
for sid, x in (('unit-length', 22.2912 / 160000 * 1e6), ('wrong-run', 22.2912 / 22500 * 1e6)):
    sl = [q for q in w[1]['wrong'] if q['id'] == sid][0]
    ok(slip_takes(sl, x) and slip_takes(sl, round(x)), 'p2 slip %s takes unrounded-C figure %s' % (sid, x))
# no part prints its own key
for i, p in enumerate(gb['parts']):
    for form in {('%.4f' % keys[i]).rstrip('0').rstrip('.'), '%.2f' % keys[i]}:
        ok(form not in p['question'], 'grid p%d question prints its own key %s' % (i + 1, form))
ok(gap400 > 557.28 and abs(gap400 / 557.28 - 1) < 0.02,
   'explain p2: 400 gap about 1%% higher (mine %.2f, %.2f%%)' % (gap400, (gap400 / 557.28 - 1) * 100))
ok(abs(gap600 - 253) < 0.5, 'explain p3: 600 run about 253e-6 below the limit (mine %.2f)' % gap600)
ordr = math.log(gap400 / gap600) / math.log(1.5)
print('gap400 over prediction %.2f%%, observed order 400 to 600 %.4f' % ((gap400 / 557.28 - 1) * 100, ordr))
ok(1.9 < ordr < 2, 'observed order a little under 2 (mine %.4f)' % ordr)
ok(2.25 / 5.0625 < 0.5, 'p4 explain: work factor under half the path factor')

# ---------- 3a. algebra p-units-133 part 2, p-affine-five part 3 ----------
un = load('app/content/courses/algebra/problems-3.json', 'p-units-133')
G = [x for x in range(1, 133) if math.gcd(x, 133) == 1]


def order(y, m):
    k, z = 1, y % m
    while z != 1:
        z = z * y % m
        k += 1
    return k


ok(len(G) == 108, '|G| 108')
ker = [x for x in G if x % 19 == 1]
ord3 = [x for x in G if order(x % 19, 19) == 3]
ok(len(ker) == 6 and len(ord3) == 12 == un['parts'][1]['widget']['answer'], 'units p2 key 12')
ok(sorted({x % 19 for x in ord3}) == [7, 11] and 7**3 == 18 * 19 + 1 and 49 % 19 == 11, 'residues 7, 11')
ok(len([x for x in G if pow(x, 3, 19) == 1]) == 18 and len([x for x in range(133) if x % 19 == 7]) == 7
   and all(len([x for x in range(133) if x % 19 == y and x % 7 == 0]) == 1 for y in (7, 11)),
   'slips 18, 14 and the seven-each line')
ok(len([x for x in G if pow(x, 3, 133) == 1]) == 9 == un['parts'][2]['widget']['answer'], 'units p3 key 9')
ok({s['value'] for s in un['parts'][1]['widget']['wrong']} == {2, 18, 6, 14}, 'units p2 slip values')
af = load('app/content/courses/algebra/problems-3.json', 'p-affine-five')


def comp(f, g):
    return (f[0] * g[0] % 5, (f[0] * g[1] + f[1]) % 5)


f = (2, 3)
pw = [f]
for _ in range(3):
    pw.append(comp(f, pw[-1]))
ok(pw[3] == (1, 0) and af['parts'][2]['widget']['answer'] == 0 and all(q != (1, 0) for q in pw[:3]),
   'affine p3 key 0, order 4')
c = 3
cs = [3]
for _ in range(3):
    c = 2 * c + 3
    cs.append(c)
ok(cs == [3, 9, 21, 45] and 3 * (8 + 4 + 2 + 1) == 45 == 3 * (2**4 - 1) and 12 % 5 == 2 and 45 % 5 == 0,
   'affine constants 3, 9, 21, 45')


def aord(g):
    k, q = 1, g
    while q != (1, 0):
        q = comp(g, q)
        k += 1
    return k


grp = [(a, b) for a in range(1, 5) for b in range(5)]
ok(sum(aord(g) == 4 for g in grp) == 10 == af['parts'][3]['widget']['answer']
   and all(aord(g) == order(g[0], 5) for g in grp if g[0] != 1), 'affine p4 key 10; order equals multiplier order')

# ---------- 3b. pdes p-log-contract part 4 ----------
lc = load('app/content/courses/pdes/problems-3.json', 'p-log-contract')
sig, r, T = 0.28, 0.02, 1.5
k = 2 * r / sig**2
tau = 0.5 * sig**2 * T
mean, var = (k - 1) * tau, 2 * tau
ok(abs(mean + 0.0288) < 1e-12 and abs(var - 0.1176) < 1e-12 and abs(mean - (r - sig**2 / 2) * T) < 1e-15,
   'log p4 mean, variance')
z = -mean / math.sqrt(var)
pr = 1 - Phi(z)
d2 = (r - sig**2 / 2) * T / (sig * math.sqrt(T))
print('log p4: sd %.6f z %.6f chance %.7f Phi(0.0840) %.6f' % (math.sqrt(var), z, pr, Phi(0.0840)))
w4 = lc['parts'][3]['widget']
ok(abs(pr - w4['answer']) < 1e-6 and abs(Phi(d2) - pr) < 1e-12, 'log p4 key 0.466535 = Phi(d2)')
ok(round(math.sqrt(var), 5) == 0.34293 and round(0.0288 / 0.34293, 4) == 0.0840 and round(Phi(0.0840), 4) == 0.5335,
   'log p4 printed working')
for x in (0.4665, round(pr, 4), trunc(pr, 4), 1 - 0.5335):
    ok(takes(w4, x), 'log p4 band takes %s' % x)
for x in (0.4664, 0.4666, 0.5335, 0.5):
    ok(not takes(w4, x), 'log p4 band refuses %s' % x)
for sl in w4['wrong']:
    ok(slip_takes(sl, {'wrong-side': 1 - pr, 'no-drift': 0.5}[sl['id']]), 'log p4 slip %s' % sl['id'])
# the upper tail by midpoint quadrature of the normal density
N = 200000
hi = mean + 12 * math.sqrt(var)
hs = hi / N
quad = sum(math.exp(-(((i + 0.5) * hs - mean)**2) / (2 * var)) for i in range(N)) * hs / math.sqrt(2 * math.pi * var)
ok(abs(quad - pr) < 1e-7, 'log p4 chance by quadrature %.7f' % quad)
ok(abs(1000 * math.exp(-k * tau) - 970.45) < 0.005 and abs(1000 * math.exp(-k * tau) * mean + 27.95) < 0.005,
   'log p2, p3 carried 970.45, -27.95')

# ---------- 3c. measure-prob p-settlement-fails part 5 ----------
sf = load('app/content/courses/measure-prob/problems-2.json', 'p-settlement-fails')


def pk(j):
    return F(64, 100) * (j + 1) * F(1, 5)**j


ok(abs(float(sum(pk(j) for j in range(400))) - 1) < 1e-15, 'pmf sums to 1')


def Gs(s_, n=1500):
    return float(sum(pk(j) * F(s_)**j for j in range(n)))


ok(abs(Gs(F(5, 4)) - 256 / 225) < 1e-12 and abs(Gs(F(4)) - 16) < 1e-6, 'G(1.25) = 256/225; closed form holds below 5')
terms = [pk(j) * 6**j for j in range(60)]
ok(all(terms[j] == F(64, 100) * (j + 1) * F(6, 5)**j for j in range(60))
   and all(terms[j + 1] > terms[j] for j in range(59)) and sum(terms) > 10**5,
   'E[6^N] terms 0.64(k+1)1.2^k grow; partial sums unbounded')
ok(16 / (5 - 6)**2 == 16 and abs(6**0.5 - 2.45) < 0.005, 'distractors 16 and 2.45')
ok([o['id'] for o in sf['parts'][4]['widget']['options'] if o.get('correct')] == ['inf'], 'settlement p5 choice inf')
EN = float(sum(j * pk(j) for j in range(400)))
EN2 = float(sum(j * j * pk(j) for j in range(400)))
ok(abs(EN - 0.5) < 1e-12 and abs(EN2 - 0.875) < 1e-12, 'E[N] 0.5, E[N^2] 0.875')

print('%d checks passed, %d failed' % (n_ok, len(bad)))
sys.exit(1 if bad else 0)
