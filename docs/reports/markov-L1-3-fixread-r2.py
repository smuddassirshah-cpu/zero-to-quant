#!/usr/bin/env python3
"""Fix-pass read, markov L1-3 round 2 (commit ac8f1d97). Exits 0 on correct content.

Recomputes every number the changed sentences state or rely on, and runs the
voice gate on the changed strings. The one wording finding (l12, "the walk"
against "the price") is printed as a note, not a failing check.
"""
import itertools, json, os, re, sys
from fractions import Fraction as F
from math import comb, erf, sqrt

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'content', 'courses', 'markov')
fails = []


def check(name, ok, detail=''):
    print(('ok   ' if ok else 'FAIL ') + name + (' | ' + str(detail) if detail != '' else ''))
    if not ok:
        fails.append(name)


def matmul(A, B):
    return [[sum(a * b for a, b in zip(r, c)) for c in zip(*B)] for r in A]


# ---- l2: ratings chain, 3-step paths A -> D
P = [[F(90, 100), F(9, 100), F(1, 100)], [F(5, 100), F(85, 100), F(10, 100)], [F(0), F(0), F(1)]]
paths = {}
for mid in itertools.product(range(3), repeat=2):
    seq = (0,) + mid + (2,)
    pr = F(1)
    for a, b in zip(seq, seq[1:]):
        pr *= P[a][b]
    if pr:
        paths[seq] = pr
check('l2 P^3_AD = 0.051895', sum(paths.values()) == F(51895, 1000000), float(sum(paths.values())))
check('l2 path A,D,D,D has chance 0.01', paths[(0, 2, 2, 2)] == F(1, 100))
check('l2 no 3-step A->D path has chance 0.01^3', F(1, 10**6) not in paths.values(),
      sorted(map(float, paths.values())))
# regime chain (bull, bear), 2-step paths from bear
R = [[F(9, 10), F(1, 10)], [F(2, 10), F(8, 10)]]
two = {k: R[1][k] * R[k][0] for k in range(2)}
check('l2 bear->bull in two = 0.34', sum(two.values()) == F(34, 100))
check('l2 routes 0.18 (via bull) and 0.16 (via bear)', two[0] == F(18, 100) and two[1] == F(16, 100))
allp = [R[1][a] * R[a][b] for a in range(2) for b in range(2)]
check('l2 no 2-step path from bear has chance 0.2^2', F(4, 100) not in allp, list(map(float, allp)))
# entrywise product of P^2 and P^3 against the terms of (P^2 P^3)_ij
P2 = matmul(P, P)
P3 = matmul(P2, P)
ok = True
for M in (P, R):
    n = len(M)
    M2 = matmul(M, M)
    M3 = matmul(M2, M)
    for i in range(n):
        for j in range(n):
            terms = [M2[i][k] * M3[k][j] for k in range(n)]
            h = M2[i][j] * M3[i][j]
            if i == j:
                ok &= (h == terms[i])
            elif h:
                ok &= (h not in terms)
check('l2 entrywise: diagonal = the route through middle i; off-diagonal matches no route', ok)


# ---- l5: closed classes
def limit(M):
    A = [[float(x) for x in r] for r in M]
    for _ in range(14):
        A = matmul(A, A)
    return A


L = limit([[0.97, 0.03], [0, 1]])
check('l5 one closed class takes all mass', abs(L[0][1] - 1) < 1e-9)
check('l5 0.97^100 ~ 0.048', abs(0.97**100 - 0.048) < 0.0005, round(0.97**100, 5))
L = limit([[0.5, 0.2, 0.3], [0, 1, 0], [0, 0, 1]])
check('l5 two closed classes: mass splits 0.4 / 0.6, so "only" is needed',
      abs(L[0][1] - 0.4) < 1e-9 and abs(L[0][2] - 0.6) < 1e-9)

# ---- l10: gambler's ruin, p = 0.49, i = 50, N = 100
p, q, i, N = 0.49, 0.51, 50, 100
r = q / p
Pi = (1 - r**i) / (1 - r**N)
check('l10 P_50 ~ 0.1192', abs(Pi - 0.1192) < 5e-5, round(Pi, 5))
D_formula = i / (q - p) - (N / (q - p)) * Pi
# second method: D_j = 1 + p D_{j+1} + q D_{j-1}, D_0 = D_N = 0, by elimination
a = [0.0] * (N + 1)
b = [0.0] * (N + 1)
for j in range(1, N):
    den = 1 - q * a[j - 1]
    a[j] = p / den
    b[j] = (1 + q * b[j - 1]) / den
D = [0.0] * (N + 1)
for j in range(N - 1, 0, -1):
    D[j] = a[j] * D[j + 1] + b[j]
check('l10 expected duration about 1,900 (formula and linear solve agree)',
      abs(D[50] - D_formula) < 1e-6 and 1850 < D[50] < 1950, round(D[50], 1))


# ---- l11: reflection count by enumeration
def touching(n, k, m):
    c = 0
    for steps in itertools.product((1, -1), repeat=n):
        s = 0
        mx = 0
        for x in steps:
            s += x
            mx = max(mx, s)
        if s == k and mx >= m:
            c += 1
    return c


ok = True
for n in range(1, 11):
    for m in range(1, n + 2):
        for k in range(-n, m + 1):
            if (n - k) % 2:
                continue
            top = (n + 2 * m - k) // 2
            ok &= touching(n, k, m) == (comb(n, top) if top <= n else 0)
check('l11 count formula for m > 0, k <= m, n <= 10 (enumerated)', ok)
check('l11 28 of 70 paths to (8,0) touch 2', touching(8, 0, 2) == 28 and comb(8, 4) == 70)


def touching_below(n, k, m):
    c = 0
    for steps in itertools.product((1, -1), repeat=n):
        s = 0
        hit = (m == 0)
        for x in steps:
            s += x
            hit = hit or s == m
        if s == k and hit:
            c += 1
    return c


check('l11 formula fails for m < 0 with k <= m, so the condition m > 0 is needed',
      touching_below(4, -2, -1) != comb(4, (4 + 2 * (-1) - (-2)) // 2),
      (touching_below(4, -2, -1), comb(4, 2)))


def barrier(n, level, pu, up):
    dist = {0: 1.0}
    hit = 0.0
    for _ in range(n):
        nd = {}
        for s, w in dist.items():
            for x, pr in ((1, pu), (-1, 1 - pu)):
                t = s + x
                if (t >= level) if up else (t <= level):
                    hit += w * pr
                else:
                    nd[t] = nd.get(t, 0) + w * pr
        dist = nd
    return hit


a4 = sum(comb(20, u) for u in range(21) if 2 * u - 20 <= -4) / 2**20
a6 = sum(comb(20, u) for u in range(21) if 2 * u - 20 <= -6) / 2**20
check('l11 P(S20<=-4) = 0.2517, P(S20<=-6) = 0.1316', abs(a4 - 0.2517) < 5e-5 and abs(a6 - 0.1316) < 5e-5,
      (round(a4, 5), round(a6, 5)))
hitp = barrier(20, -4, 0.5, False)
check('l11 touch chance 0.3833 = 0.2517 + 0.1316', abs(hitp - (a4 + a6)) < 1e-12 and abs(hitp - 0.3833) < 5e-5,
      round(hitp, 5))
check('l11 0.38 is half as much again as 0.25 (the chance of ending at or beyond)', 1.45 < hitp / a4 < 1.55,
      round(hitp / a4, 3))

# ---- l12
Phi = lambda z: 0.5 * (1 + erf(z / sqrt(2)))
check('l12 250-day: Phi(-0.79) ~ 0.21', abs(Phi(-12.5 / 15.81) - 0.21) < 0.005, round(Phi(-12.5 / 15.81), 4))
zd = -(12.5 / 250) / (15.81 / sqrt(250))
check('l12 one day, if normal: z ~ -0.05, Phi ~ 0.48', abs(zd + 0.05) < 0.001 and abs(Phi(zd) - 0.48) < 0.001,
      (round(zd, 4), round(Phi(zd), 4)))
check('l12 standard error with 20,000 trials ~ 0.003', abs(sqrt(0.34375 * 0.65625 / 20000) - 0.003) < 0.0005)
ge6 = sum(comb(20, u) for u in range(21) if 2 * u - 20 >= 6) / 2**20
touch = barrier(20, 5, 0.5, True)
check('l12 P(S20>=6) = 0.13159, touch = 0.26318, pay-out 100 x touch = 26.32',
      abs(ge6 - 0.13159) < 5e-6 and abs(touch - 2 * ge6) < 1e-12 and round(100 * touch, 2) == 26.32,
      (round(ge6, 5), round(touch, 5)))
refl = 2 * sum(comb(20, u) * 0.55**u * 0.45**(20 - u) for u in range(21) if 2 * u - 20 >= 5)
td = barrier(20, 5, 0.55, True)
check('l12 with p = 0.55 the reflection sum is not the touch chance', abs(td - refl) > 0.01,
      (round(td, 4), round(refl, 4)))
# Risk-neutral up-chance, r = 0 (Hull, "Binomial trees": p = (e^{r dt} - d) / (u - d)).
# Additive unit steps on the price: q = (0 - (-1)) / (1 - (-1)) = 1/2, the fair price walk.
# Multiplicative u, d = 1/u (the lesson's binomial model): q = (1 - d) / (u - d) = 1 / (1 + u) < 1/2,
# so the log-price walk is NOT fair under q. "The up-chance that makes the walk fair" is right
# only when "the walk" is the price itself.
check('l12 additive price walk, r = 0: risk-neutral q = 1/2', (0 - (-1)) / (1 - (-1)) == 0.5)
qs = []
for u in (1.01, 1.05, 1.2):
    d = 1 / u
    qm = (1 - d) / (u - d)
    qs.append(round(qm, 5))
    check('l12 multiplicative tree u = %s, r = 0: q = 1/(1+u) < 1/2 and E_q[price ratio] = 1' % u,
          abs(qm - 1 / (1 + u)) < 1e-12 and qm < 0.5 and abs(qm * u + (1 - qm) * d - 1) < 1e-12, round(qm, 5))
print('note l12 screens[9].explain: in the u, d = 1/u tree the risk-neutral up-chance is', qs,
      'not 0.5; see finding 1 of the fix-pass read')

# ---- voice gate on the changed strings (35 words, three sentences, no "!", no em-dash)
changed = {
    'l10-gamblers-ruin.json': ['because the average game lasts about 1,900 bets',
                               'Over about 1,900 bets on average the edge compounds',
                               'played about 1,900 times on average'],
    'l11-reflection.json': ['For a level above the start', 'chance of ending at or beyond the limit.'],
    'l12-price-paths.json': ["If one day's return is normal too", 'Set the 0.5 to 0.55 and the code finds',
                             'With a fair walk and no interest, the price is',
                             'so the fair price is the expected pay-out', 'gives the chance of a barrier event',
                             'A colleague finds a barrier chance'],
    'l2-transition-matrix.json': ['You cubed 0.01, which matches no path', 'You squared 0.2, which matches no path',
                                  'Entry by entry gives one route on the diagonal'],
    'l5-where-it-settles.json': ['Default is the only closed class'],
}


def strings(o):
    if isinstance(o, str):
        yield o
    elif isinstance(o, dict):
        for v in o.values():
            yield from strings(v)
    elif isinstance(o, list):
        for v in o:
            yield from strings(v)


for f, keys in changed.items():
    allstr = list(strings(json.load(open(os.path.join(ROOT, f), encoding='utf-8'))))
    for k in keys:
        hits = [s for s in allstr if k in s]
        if len(hits) != 1:
            check('voice: changed string found once: ' + k[:40], False, len(hits))
            continue
        plain = re.sub(r'\$\$.*?\$\$|\$[^$]*\$', 'X', hits[0], flags=re.S)
        sents = [x for x in re.split(r'(?<=[.?:;])\s+', plain) if x.strip()]
        full = [x for x in re.split(r'(?<=[.?])\s+', plain) if x.strip()]
        longest = max(len(x.split()) for x in full)
        bad = ('!' in plain) or ('—' in plain) or longest > 35 or len(full) > 3 \
            or bool(re.search(r'\blesson \d', plain, re.I))
        check('voice: ' + k[:44], not bad, 'sentences %d, longest %d words' % (len(full), longest))

print('\n%d failing' % len(fails))
sys.exit(1 if fails else 0)
