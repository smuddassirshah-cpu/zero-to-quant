"""Fix-pass read, graphs-dp level 4 (content commit f9c90ba2). Recomputes every changed number two ways.
Exits 0 when the content agrees. Run with the venv Python from the repo root; no arguments."""
import itertools
import json
import math
import os
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
C = os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'graphs-dp')
J = lambda f: json.load(open(os.path.join(C, f + '.json')))
fails = []


def check(name, cond, detail=''):
    print(('ok   ' if cond else 'FAIL ') + name + (' ' + str(detail) if detail else ''))
    if not cond:
        fails.append(name)


# ---------- l17 screens[9]: bond sale, slip first-best ----------
bids = [F(990, 10), F(992, 10), F(995, 10), F(999, 10)]
s9 = J('l17-dice-stopping')['screens'][9]
wrong9 = {w['id']: w['value'] for w in s9['widget']['wrong']}


def policy_value(accept_sets):
    """Exact value by enumerating all 4^3 bid triples. accept_sets[k] is the set of bids dealer k's bid is taken at; the last takes all."""
    tot = F(0)
    for triple in itertools.product(bids, repeat=3):
        for k, b in enumerate(triple):
            if k == 2 or b in accept_sets[k]:
                tot += b
                break
    return tot / 64


v1 = sum(bids) / 4
v2 = sum(max(b, v1) for b in bids) / 4
v3 = sum(max(b, v2) for b in bids) / 4
best = max(policy_value([set(a), set(b)]) for r1 in range(5) for a in itertools.combinations(bids, r1)
           for r2 in range(5) for b in itertools.combinations(bids, r2))
check('l17 s9 key 99.6375 by backward induction and by all 256 policies', v3 == best == F(996375, 10000) and s9['widget']['answer'] == 99.6375, float(v3))
slip_formula = (bids[2] + bids[3]) / 4 + F(2, 4) * v2            # accept 99.5 and 99.9 from the first dealer, then play on optimally
slip_enum = policy_value([{bids[2], bids[3]}, {bids[2], bids[3]}])  # the same policy, enumerated
check('l17 s9 slip first-best = 99.625 (formula and enumeration)', slip_formula == slip_enum == F(99625, 1000) and wrong9['first-best'] == 99.625, float(slip_enum))
check('l17 s9 slip bands (0.0005) do not touch the key or each other',
      all(abs(a - b) > 0.001 for a, b in itertools.combinations([99.6375] + list(wrong9.values()), 2)))
check('l17 s9 feedback: 99.5 < 99.55 = value with two dealers left', bids[2] < v2 == F(9955, 100))

# ---------- homework-4 items[2]: grid routes, slip edge ----------
h = J('homework-4')['items']
it2 = h[2]
cells = it2['canvas']['params']['cells']
blocked = [[c == '■' for c in row] for row in cells]
R, Cn = len(blocked), len(blocked[0])


def table(first_col_ones=False, blocked_cell_one=False):
    w = [[0] * Cn for _ in range(R)]
    for i in range(R):
        for j in range(Cn):
            if blocked[i][j] and not (first_col_ones and blocked_cell_one and j == 0):
                continue
            if i == 0 and j == 0:
                w[i][j] = 1
            elif first_col_ones and j == 0:
                w[i][j] = 1
            else:
                w[i][j] = (w[i - 1][j] if i else 0) + (w[i][j - 1] if j else 0)
    return w


def brute():
    n = 0
    for moves in set(itertools.permutations('D' * (R - 1) + 'R' * (Cn - 1))):
        i = j = 0
        ok = not blocked[0][0]
        for m in moves:
            i, j = (i + 1, j) if m == 'D' else (i, j + 1)
            ok = ok and not blocked[i][j]
        n += ok
    return n


key = table()[-1][-1]
check('hw4 items[2] key 9 (table and brute force over 70 routes)', key == brute() == it2['widget']['answer'] == 9, key)
edge_all = table(first_col_ones=True, blocked_cell_one=True)   # whole first column prefilled with 1s, its block ignored
edge_below = table(first_col_ones=True)                        # blocked cell 0, but the cell below it left at 1
edge = it2['widget']['wrong'][0]['value']
check('hw4 items[2] slip edge = 11: first column all 1s, its blocked cell included', edge == edge_all[-1][-1] == 11, edge_all[3:])
check('hw4 items[2] the cell below the block does not matter: 1 there alone still gives 9 (it is cut off by the block in row 5)', edge_below[-1][-1] == 9)


def brute_ignoring(cell):
    n = 0
    for moves in set(itertools.permutations('D' * (R - 1) + 'R' * (Cn - 1))):
        i = j = 0
        ok = True
        for m in moves:
            i, j = (i + 1, j) if m == 'D' else (i, j + 1)
            ok = ok and (not blocked[i][j] or (i, j) == cell)
        n += ok
    return n


check('hw4 items[2] slip 11 a second way: routes when the block at row 4, column 1 is treated as open', brute_ignoring((3, 0)) == 11)
check('hw4 items[2] no single ignored block, and no ignoring of all blocks, gives the old value 12',
      12 not in [brute_ignoring(c) for c in [(1, 1), (2, 3), (3, 0), (4, 2)]], [brute_ignoring(c) for c in [(1, 1), (2, 3), (3, 0), (4, 2)]])

# ---------- homework-4 items[0]: knapsack 5 kg, slip ratio ----------
it0 = h[0]
wts, vals, cap = [2, 3, 4, 5], [3, 4, 5, 6], 5
subsets = [(sum(vals[i] for i in s), s) for r in range(5) for s in itertools.combinations(range(4), r) if sum(wts[i] for i in s) <= cap]
dp = [0] * (cap + 1)
for wt, v in zip(wts, vals):
    for w in range(cap, wt - 1, -1):
        dp[w] = max(dp[w], dp[w - wt] + v)
check('hw4 items[0] key 7 (subsets and table)', max(subsets)[0] == dp[cap] == it0['widget']['answer'] == 7)
order = sorted(range(4), key=lambda i: -F(vals[i], wts[i]))
room, got = cap, 0
for i in order:
    if wts[i] <= room:
        room -= wts[i]
        got += vals[i]
check('hw4 items[0] value-per-kg packing gives the key 7, not 3', got == 7 and order[0] == 0, got)
check('hw4 items[0] 3 = the best value-per-kg item alone (2 kg, £1.50 a kg), also the lightest item alone', vals[order[0]] == 3 == vals[wts.index(min(wts))])
print('     feasible pack values:', sorted({v for v, _ in subsets}))

# ---------- l16 screens[9]: no-down slip ----------
s = J('l16-grid-paths')['screens'][9]
check('l16 s9 no-down 0.1664 = 0.55^3; key 0.2995 = 4 * 0.55^3 * 0.45', round(0.55 ** 3, 4) == 0.1664 and round(math.comb(4, 3) * 0.55 ** 3 * 0.45, 4) == 0.2995
      and {w['id']: w['value'] for w in s['widget']['wrong']}['no-down'] == 0.1664)

# ---------- l17: dice values and thresholds used in the changed lines ----------
V = [None, F(7, 2)]
for n in range(2, 201):
    V.append(sum(max(F(f), V[-1]) for f in range(1, 7)) / 6)
thr = lambda n: 1 if n == 1 else min(f for f in range(1, 7) if f >= V[n - 1])
check('l17 V2..V4 = 4.25, 4.6667, 4.9444', [round(float(V[n]), 4) for n in (2, 3, 4)] == [4.25, 4.6667, 4.9444])
check('l17 thresholds: n=3 -> 5, n=5 -> 5, n=6 -> 6, and 6 for every n >= 6', thr(3) == 5 and thr(5) == 5 and all(thr(n) == 6 for n in range(6, 201)) and thr(2) == 4)
check('l17 s6: V_n < 6 for every n, V_n <= 6 - (5/6)^n', all(V[n] <= 6 - F(5, 6) ** n for n in range(1, 201)))
check('l17 s6: V_n strictly rising; V10 = 5.65, V50 = 5.9998', all(V[n] < V[n + 1] for n in range(1, 200)) and round(float(V[10]), 2) == 5.65 and round(float(V[50]), 4) == 5.9998)
check('l17 test-3 symptom 4.25: rule applied once, or always against 3.5', sum(max(f, 3.5) for f in range(1, 7)) / 6 == 4.25)
emax = lambda k: sum(F(f) * (F(f, 6) ** k - F(f - 1, 6) ** k) for f in range(1, 7))
check('l17 test-9: the hindsight bar E[max of 4 rolls] = 5.2446 would give 6 at n = 5 (and passes n = 2, 3)',
      [min(f for f in range(1, 7) if f >= emax(n - 1)) for n in (2, 3, 5)] == [4, 5, 6], round(float(emax(4)), 4))


# ---------- l17 quiz q-secretary: best rule's chance, exact ----------
def secretary(n):
    """Best chance over cut-off rules (reject r, then take the first record); the optimal rule is of this form (Ferguson 1989, s.2)."""
    best = F(1, n)
    for r in range(1, n):
        best = max(best, F(r, n) * sum(F(1, k) for k in range(r, n)))
    return best


def secretary_dp(n):
    """The same by backward induction on the relative-rank problem, no rule form assumed."""
    cont = F(0)  # value of continuing past candidate n
    for k in range(n, 0, -1):
        # candidate k is a record with chance 1/k; stopping on a record wins with chance k/n
        cont = F(1, k) * max(F(k, n), cont) + F(k - 1, k) * cont
    return cont


inv_e = 1 / math.e
ps = [secretary(n) for n in range(1, 301)]
check('secretary: cut-off formula equals backward induction, n = 1..300', all(ps[n - 1] == secretary_dp(n) for n in range(1, 301)))
check('secretary: best chance above 1/e for every n (to 300), non-increasing, 0.371 at n = 100',
      all(float(p) > inv_e for p in ps) and all(a >= b for a, b in zip(ps, ps[1:])) and round(float(ps[99]), 3) == 0.371)
check('secretary: best chance is exactly 1/2 at n = 2 and 3, below 1/2 from n = 4', ps[1] == ps[2] == F(1, 2) and all(p < F(1, 2) for p in ps[3:]))

# ---------- l14 / l15 / l16 symptoms quoted in the rewritten test-N lines ----------
def knap_nofit(ws, vs, cap):
    n = len(ws)
    b = [[0] * (cap + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for w in range(cap + 1):
            b[i][w] = max(b[i - 1][w], b[i - 1][w - ws[i - 1]] + vs[i - 1])
    return b[n][cap]


check('l14 s6 test-1: no fit check gives 170 on the lesson bag', knap_nofit([1, 3, 4, 5], [10, 40, 50, 70], 7) == 170)


def ed(a, b, col=True, row=True, match_plus=False, diag=True):
    m, n = len(a), len(b)
    d = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        d[i][0] = i if col else 0
    for j in range(n + 1):
        d[0][j] = j if row else 0
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if a[i - 1] == b[j - 1] and not match_plus:
                d[i][j] = d[i - 1][j - 1]
            else:
                c = [d[i - 1][j], d[i][j - 1]] + ([d[i - 1][j - 1]] if diag or a[i - 1] == b[j - 1] else [])
                d[i][j] = 1 + min(c)
    return d[m][n]


check('l15 s9 test-1: 2 true; 1 with no first column; 5 adding 1 on a match; 3 with no substitution',
      [ed('HEDGE', 'EDGY'), ed('HEDGE', 'EDGY', col=False), ed('HEDGE', 'EDGY', match_plus=True), ed('HEDGE', 'EDGY', diag=False)] == [2, 1, 5, 3])


def mpc(c, missing=None, start=True):
    rows, cols = len(c), len(c[0])
    b = [[0] * cols for _ in range(rows)]
    for i in range(rows):
        for j in range(cols):
            if i == 0 and j == 0:
                b[i][j] = c[0][0] if start else 0
                continue
            up = b[i - 1][j] if i else missing
            left = b[i][j - 1] if j else missing
            b[i][j] = min(x for x in (up, left) if x is not None) + c[i][j]
    return b[-1][-1]


g1 = [[3, 1, 4, 2], [2, 5, 1, 3], [6, 2, 2, 1]]
check('l16 s7 test-1: 12 true; 6 with a missing neighbour as 0; 9 without the start fee', [mpc(g1), mpc(g1, missing=0), mpc(g1, start=False)] == [12, 6, 9])
g7 = [[1, 9, 9], [1, 9, 9], [1, 1, 1]]
routes7 = []
for moves in set(itertools.permutations('DDRR')):
    i = j = 0
    tot = g7[0][0]
    for mv in moves:
        i, j = (i + 1, j) if mv == 'D' else (i, j + 1)
        tot += g7[i][j]
    routes7.append((tot, ''.join(moves)))
check('l16 s7 test-7: 5 by the left edge then the bottom; every other route costs 13 or more', sorted(routes7)[0] == (5, 'DDRR') and sorted(routes7)[1][0] >= 13 and mpc(g7) == 5, sorted(routes7)[:2])

# ---------- homework-4 items[8] longform: the changed sentence ----------
check('hw4 items[8]: £2,000,000 in pence is 2e8 columns; in £10,000 units it is 200', 2_000_000 * 100 == 2 * 10 ** 8 and 2_000_000 // 10_000 == 200)
# rounding each risk up keeps any plan that fits the coarse budget inside the true budget, and can lose the optimum: a small case
r, p, B, unit = [6, 6, 11], [5, 5, 9], 12, 10       # true optimum takes trades 0 and 1 (risk 12, profit 10)
up = [math.ceil(x / unit) for x in r]                # 1, 1, 2 coarse units; budget 12 // 10 = 1 unit
plans = [s for k in range(4) for s in itertools.combinations(range(3), k)]
true_best = max(sum(p[i] for i in s) for s in plans if sum(r[i] for i in s) <= B)
coarse = [s for s in plans if sum(up[i] for i in s) <= B // unit]
check('hw4 items[8]: rounded-up plans all fit the true budget, and can miss the best plan',
      all(sum(r[i] for i in s) <= B for s in coarse) and max(sum(p[i] for i in s) for s in coarse) < true_best)

print('\n%d failed' % len(fails))
raise SystemExit(1 if fails else 0)
