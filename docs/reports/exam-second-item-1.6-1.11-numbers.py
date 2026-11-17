"""Recompute every key, wrong value and printed number of the second auto items in topic exams 1.6 to 1.11.

Run from anywhere: python3 docs/reports/exam-second-item-1.6-1.11-numbers.py (exit 0 when every check passes).
Each figure is computed here from the item's own inputs and compared with the widget field and with the printed text.
"""
import itertools, json, math, os, re, sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
EXAMS = os.path.join(HERE, '..', '..', 'app', 'content', 'exams')
fails, n = [], 0


def item(exam, iid):
    d = json.load(open(os.path.join(EXAMS, exam + '.json'), encoding='utf-8'))
    return next(i for i in d['items'] if i['id'] == iid)


def check(ok, label):
    global n
    n += 1
    if not ok:
        fails.append(label)
        print('FAIL', label)


def near(a, b, tol, label):
    check(abs(a - b) <= tol, f'{label}: {a} vs {b}')


def text(o):
    return json.dumps(o, ensure_ascii=False)


def printed(o, s, label):
    check(s in text(o).replace('\\\\', '\\'), f'{label}: "{s}" printed')


def wrong(w, wid):
    return next(x['value'] for x in w['wrong'] if x['id'] == wid)


def bands(w, label):
    """every wrong value lies outside the key's band and outside every other slip's band"""
    a, t = w['answer'], w['tol']['abs']
    vals = [(x['id'], x['value'], x.get('tol', {}).get('abs', 1e-9)) for x in w['wrong']]
    for i, v, tv in vals:
        check(abs(v - a) > t + tv, f'{label} {i} clear of key')
    for (i, v, tv), (j, u, tu) in itertools.combinations(vals, 2):
        check(abs(v - u) > tv + tu, f'{label} {i}/{j} apart')


# ---------------------------------------------------------------- topic 1.6 s-three-traders
it = item('topic-1.6', 's-three-traders')
a, b = 22, 18
check(F(a, a + b) == F(55, 100), 'prior mean 55%')
recs = {'ash': (9, 10), 'bea': (46, 60), 'cal': (101, 150)}
post = {k: (a + w, b + t - w) for k, (w, t) in recs.items()}
mean = {k: F(p, p + q) for k, (p, q) in post.items()}
check(post['ash'] == (31, 19) and post['bea'] == (68, 32) and post['cal'] == (123, 67), 'posteriors')
check(mean['ash'] == F(62, 100) and mean['bea'] == F(68, 100), 'means 0.62, 0.68')
check(f'{float(mean["cal"]):.3f}' == '0.647', 'Cal mean 0.647')
top = max(mean, key=mean.get)
check([o['id'] for o in it['widget']['options'] if o.get('correct')] == [top], 'key is Bea')
mle = {k: F(w, t) for k, (w, t) in recs.items()}
check(max(mle, key=mle.get) == 'ash', 'raw rate picks Ash')
check(max(recs, key=lambda k: recs[k][1]) == 'cal', 'longest record is Cal')
check(round(float(mle['bea']) * 100) == 77, "Bea's 77%")
for s in ['31/50 = 0.62', '123/190 = 0.647', '0.62, 0.68 and 0.647', 'Beta}(68, 32)', 'Beta}(31, 19)', 'Beta}(123, 67)', '77%', '90%']:
    printed(it, s, 's-three-traders')

# ---------------------------------------------------------------- topic 1.7 e-ratio-spread
it = item('topic-1.7', 'e-ratio-spread')
cost = 5.40 - 2 * 1.90
pay = lambda S: max(S - 80, 0) - 2 * max(S - 90, 0)
near(cost, 1.60, 1e-9, 'net cost')
p1, p2 = it['parts'][0]['widget'], it['parts'][1]['widget']
near(p1['answer'], pay(95) - cost, 1e-9, 'profit at 95')
near(wrong(p1, 'one-short'), (95 - 80) - (95 - 90) - cost, 1e-9, 'one-short')
near(wrong(p1, 'no-premium'), pay(95), 1e-9, 'no-premium')
near(wrong(p1, 'added-premiums'), pay(95) - (5.40 + 3.80), 1e-9, 'added-premiums')
upper = 100 - cost                                   # (S - 80) - 2(S - 90) - cost = 0
near(pay(upper) - cost, 0, 1e-9, 'upper break-even solves')
near(p2['answer'], upper, 1e-9, 'upper break-even key')
near(wrong(p2, 'payoff-zero'), 100, 1e-9, 'payoff-zero')
near(wrong(p2, 'lower'), 80 + cost, 1e-9, 'lower break-even')
near(pay(80 + cost) - cost, 0, 1e-9, 'lower solves')
near(wrong(p2, 'plus-cost'), 100 + cost, 1e-9, 'plus-cost')
check(pay(130) - cost < pay(110) - cost < 0, 'loss grows above break-even')
bands(p1, 'ratio p1'); bands(p2, 'ratio p2')
for s in ['5.40 - 2 \\times 1.90 = 1.60', '98.40 - S', '100 - S', '£3.40', '£98.40', '£15.00', '£10.00', '£1.60', '£3.80', '£5.00']:
    printed(it, s, 'e-ratio-spread')

# ---------------------------------------------------------------- topic 1.7 e-capped-copy
it = item('topic-1.7', 'e-capped-copy')
S0, Su, Sd, r, cap = 40, 50, 35, 0.025, 44
vu, vd = min(Su, cap), min(Sd, cap)
delta = (vu - vd) / (Su - Sd)
cash_T = vd - delta * Sd                             # owed (negative) or received (positive) in a year
lend = cash_T / (1 + r)
near(delta, 0.6, 1e-12, 'delta 0.6')
near(cash_T, 14, 1e-9, 'cash 14 in a year')
check(f'{lend:.2f}' == '13.66', f'lend 13.66 ({lend})')
price = delta * S0 + lend
check(f'{price:.2f}' == '37.66', f'price 37.66 ({price})')
q = ((1 + r) * S0 - Sd) / (Su - Sd)
near((q * vu + (1 - q) * vd) / (1 + r), price, 1e-9, 'price by q agrees')
near(delta * Su + cash_T, vu, 1e-9, 'copy up state'); near(delta * Sd + cash_T, vd, 1e-9, 'copy down state')
opts = {o['id']: o['text'] for o in it['widget']['options']}
check(opts['a'] == f'Hold {delta:g} shares and lend £{lend:.2f}', 'key text')
check(opts['b'] == f'Hold {delta:g} shares and lend £{cash_T:.2f}', 'undiscounted')
check(1 * Su != vu, 'whole share overpays up')
check(opts['d'] == f'Hold {delta:g} shares and borrow £{lend:.2f}', 'sign slip')
near(delta * Sd, 21, 1e-9, 'shares worth 21 down'); near(delta * Su, 30, 1e-9, 'shares worth 30 up')
for s in ['14/1.025 = 13.66', '(44 - 35)/(50 - 35) = 0.6', '0.6 \\times 40 + 13.66 = 37.66', '£21.00', '£30.00', '£9.00 over £15.00', '£14.00']:
    printed(it, s, 'e-capped-copy')

# ---------------------------------------------------------------- topic 1.7 e-zero-yield
it = item('topic-1.7', 'e-zero-yield')
y = (100 / 70) ** (1 / 8) - 1
y2 = math.exp(math.log(100 / 70) / 8) - 1            # second route, by logs
near(y, y2, 1e-12, 'yield two ways')
w1, w2 = it['parts'][0]['widget'], it['parts'][1]['widget']
near(w1['answer'], y, 1e-6, 'yield key')
check(f'{y * 100:.2f}' == '4.56' and abs(y * 100 - 4.565) > 0.002, 'yield prints 4.56, no tie')
check(abs(w1['answer'] - 0.0456) <= w1['tol']['abs'], 'typed 4.56 accepted')
near(wrong(w1, 'simple'), 30 / 70 / 8, 1e-6, 'simple')
near(wrong(w1, 'on-face'), 30 / 100 / 8, 1e-9, 'on-face')
near(wrong(w1, 'inverted'), 1 - 0.7 ** (1 / 8), 1e-6, 'inverted')
p_next = 100 / (1 + y) ** 7
near(p_next, 70 * (1 + y), 1e-9, 'price in a year two ways')
check(f'{p_next:.2f}' == '73.19' and abs(w2['answer'] - p_next) <= w2['tol']['abs'], 'price key 73.19')
check(abs(100 / 1.0456 ** 7 - w2['answer']) <= w2['tol']['abs'], 'rounded yield also accepted')
check(f'{100 / 1.0456 ** 7:.2f}' in ('73.19',), 'printed 100/1.0456^7 = 73.19')
near(wrong(w2, 'still-eight'), 100 / (1 + y) ** 8, 1e-6, 'still-eight')
near(wrong(w2, 'straight-line'), 70 + 30 / 8, 1e-9, 'straight-line')
bands(w1, 'zero p1'); bands(w2, 'zero p2')
for s in ['4.56%', '73.19', '5.36\\%', '70 \\times 1.0456']:
    printed(it, s, 'e-zero-yield')

# ---------------------------------------------------------------- topic 1.7 e-just-paid
it = item('topic-1.7', 'e-just-paid')
D0, g, rr = 1.50, 0.04, 0.10
D1 = D0 * (1 + g)
P = D1 / (rr - g)
P2 = sum(D0 * (1 + g) ** t / (1 + rr) ** t for t in range(1, 4000))   # second route: the series summed
near(P, 26, 1e-9, 'value 26'); near(P2, 26, 1e-6, 'series agrees')
w = it['widget']
near(w['answer'], P, 1e-9, 'key')
near(wrong(w, 'last-div'), D0 / (rr - g), 1e-9, 'last-div')
near(wrong(w, 'no-growth'), D1 / rr, 1e-9, 'no-growth')
near(wrong(w, 'plus-g'), round(D1 / (rr + g), 2), 1e-9, 'plus-g')
check(abs(D1 / (rr + g) * 100 % 1 - 0.5) > 0.05, 'plus-g no rounding tie')
bands(w, 'just-paid')
for s in ['1.50 \\times 1.04 = 1.56', '1.56/0.06 = 26.00', '1.56/(0.10 - 0.04) = 26.00', '£1.56', 'r - g = 0.06']:
    printed(it, s, 'e-just-paid')

# ---------------------------------------------------------------- topic 1.8 e-venue-split
it = item('topic-1.8', 'e-venue-split')
edges = {(e['from'], e['to']) for e in it['canvas']['params']['edges']}
E = {tuple(sorted((int(a), int(b)))) for a, b in edges}
check(E == {(1, 2), (1, 4), (1, 5), (2, 4), (2, 6), (3, 6), (4, 6)}, 'edge list')
link = lambda u, v: tuple(sorted((u, v))) in E
sols, greedy = [], None


def walk(col):
    v = len(col) + 1
    if v == 7:
        sols.append(', '.join(col)); return
    for c in 'ABC':
        if all(not link(u, v) or col[u - 1] != c for u in range(1, v)):
            walk(col + [c])


walk([])
col = []                                             # greedy first choices, to the dead end
for v in range(1, 7):
    free = [c for c in 'ABC' if all(not link(u, v) or col[u - 1] != c for u in range(1, v))]
    if not free:
        break
    col.append(free[0])
check(col == ['A', 'B', 'A', 'C', 'B'] and len(col) == 5, 'greedy stuck at order 6')
brute = sum(1 for t in itertools.product('ABC', repeat=6) if all(t[a - 1] != t[b - 1] for a, b in E))
opts = {o['id']: o['text'] for o in it['parts'][0]['widget']['options']}
check(opts['a'] == sols[0] == 'A, B, B, C, B, A', 'first assignment')
check(opts['first'] == next(s for s in sols if s.startswith('B')), 'first with order 1 changed')
check(opts['neighbour'] == next(s for s in sols if s.startswith('A, C')), 'first with order 2 changed')
check(opts['later'] == sols[1], 'second assignment found')
check(all(o in sols for k, o in opts.items() if k != 'none'), 'every listed split is valid')
w = it['parts'][1]['widget']
check(w['answer'] == len(sols) == brute == 6 * 1 * 2 * 2 == 24, 'count 24 three ways')
check(wrong(w, 'all-leaves') == 3 ** 6 == 729, '729')
check(wrong(w, 'up-to-names') == 24 // 6 == 4, '4')
for s in ['3 \\times 2 \\times 1 = 6', '6 \\times 2 \\times 2 = 24', '3^6 = 729', 'A, B, A, C, B', 'B, A and C']:
    printed(it, s, 'e-venue-split')

# ---------------------------------------------------------------- topic 1.9 e-swapped-d
it = item('topic-1.9', 'e-swapped-d')
N = lambda x: 0.5 * math.erfc(-x / math.sqrt(2))
Nb = lambda x: 0.5 * (1 + math.erf(x / math.sqrt(2)))      # second route for the normal cdf


def call(S, K, r, s, T, swap=False, cdf=N):
    d1 = (math.log(S / K) + (r + s * s / 2) * T) / (s * math.sqrt(T)); d2 = d1 - s * math.sqrt(T)
    if swap:
        d1, d2 = d2, d1
    return S * cdf(d1) - K * math.exp(-r * T) * cdf(d2)


def put(S, K, r, s, T):
    d1 = (math.log(S / K) + (r + s * s / 2) * T) / (s * math.sqrt(T)); d2 = d1 - s * math.sqrt(T)
    return K * math.exp(-r * T) * N(-d2) - S * N(-d1)


good, bad = call(100, 100, .05, .2, 1), call(100, 100, .05, .2, 1, True)
near(good, call(100, 100, .05, .2, 1, cdf=Nb), 1e-12, 'call two cdfs')
check(f'{good:.4f}' == '10.4506', 'correct call 10.4506')
check(f'{bad:.2f}' == '-4.62', f'swapped call -4.62 ({bad})')
near(100 * N(0.15) - 100 * math.exp(-0.05) * N(0.35), bad, 1e-9, 'printed formula')
check(f'{100 * math.exp(-0.05):.2f}' == '95.12', '95.12')
fwd = 100 - 100 * math.exp(-0.05)
res = {
    'known': abs(bad - 10.4506) > 1e-4,
    'parity': abs(bad - put(100, 100, .05, .2, 1) - fwd) > 1e-9,
    'bounds': not (0 <= bad <= 100),
    'limit': abs(call(100, 100, .05, 1e-8, 1, True) - fwd) > 1e-6,
    'finite': not math.isfinite(bad),
}
ok_good = {
    'known': abs(good - 10.4506) <= 1e-4, 'parity': abs(good - put(100, 100, .05, .2, 1) - fwd) <= 1e-9,
    'bounds': 0 <= good <= 100, 'limit': abs(call(100, 100, .05, 1e-8, 1) - fwd) <= 1e-6, 'finite': math.isfinite(good)}
check(all(ok_good.values()), 'every test passes on the correct call')
keys = {o['id'] for o in it['widget']['options'] if o.get('correct')}
check(keys == {k for k, v in res.items() if v}, f'correct set {keys}')
for s in ['d_1 = 0.35', 'd_2 = 0.15', '95.12N(0.35) = -4.62', '£10.4506', '-4.62']:
    printed(it, s, 'e-swapped-d')

# ---------------------------------------------------------------- topic 1.10 e-integral-weights
it = item('topic-1.10', 'e-integral-weights')
nodes = [0, 1, 3]


def integ(coeffs, a=0, b=3):                       # coeffs: c0 + c1 x + c2 x^2
    return sum(F(c) * (F(b) ** (k + 1) - F(a) ** (k + 1)) / (k + 1) for k, c in enumerate(coeffs))


def lagrange(k):                                   # coefficients of ell_k
    others = [m for m in nodes if m != k]
    den = F(1)
    for m in others:
        den *= (k - m)
    p, q = F(others[0]), F(others[1])
    return [p * q / den, -(p + q) / den, F(1) / den]


c = {k: integ(lagrange(k)) for k in nodes}
check(c == {0: F(0), 1: F(9, 4), 3: F(3, 4)}, 'weights from Lagrange')
# second route: solve the moment equations sum c_k k^j = int_0^3 x^j
A = [[F(k) ** j for k in nodes] for j in range(3)]
rhs = [F(3) ** (j + 1) / (j + 1) for j in range(3)]
M = [row[:] + [v] for row, v in zip(A, rhs)]
for i in range(3):
    piv = next(r_ for r_ in range(i, 3) if M[r_][i] != 0); M[i], M[piv] = M[piv], M[i]
    M[i] = [x / M[i][i] for x in M[i]]
    for r_ in range(3):
        if r_ != i:
            M[r_] = [x - M[r_][i] * y for x, y in zip(M[r_], M[i])]
check([M[i][3] for i in range(3)] == [c[0], c[1], c[3]], 'moment equations agree')
rows = it['widget']['rows']
for (lab, cell), k in zip(rows, nodes):
    near(cell['answer'], float(c[k]), 1e-12, f'cell c_{k}')
    check(abs(1 - cell['answer']) > cell['tol']['abs'] + 0.001, f'equal slip clear on c_{k}')
check(lagrange(0) == [F(1), F(-4, 3), F(1, 3)], 'ell_0 = (x-1)(x-3)/3')
check(lagrange(1) == [F(0), F(3, 2), F(-1, 2)], 'ell_1 = -x(x-3)/2')
check(lagrange(3) == [F(0), F(-1, 6), F(1, 6)], 'ell_3 = x(x-1)/6')
check(sum(F(1) for _ in nodes) == 3 and sum(F(k) for k in nodes) == 4 and integ([0, 1]) == F(9, 2), 'equal weights give 4, not 4.5')
check(c[1] * 1 + c[3] * 9 == integ([0, 0, 1]) == 9, 'check on x^2')
for s in ['0, 2.25 and 0.75', '2.25 \\times 1 + 0.75 \\times 9 = 9', 'they give 4', '= 4.5']:
    printed(it, s, 'e-integral-weights')

# ---------------------------------------------------------------- topic 1.11 e-square-root-parts
it = item('topic-1.11', 'e-square-root-parts')
w = it['widget']
z = complex(4, -1)
check(z * z == complex(15, -8), '(4 - i)^2 = 15 - 8i')
check((-z) * (-z) == complex(15, -8), 'and its negative')
import cmath
check(abs(cmath.sqrt(complex(15, -8)) - z) < 1e-12, 'principal root is 4 - i')
roots = sorted(a for a in range(-20, 21) if a != 0 and a ** 4 - 15 * a ** 2 - 16 == 0)
check(roots == [-4, 4] and 16 * 16 - 15 * 16 - 16 == 0 and 1 + 15 - 16 == 0, 'a^4 - 15a^2 - 16 = 0 gives a^2 = 16 or -1')
check(complex(4, 1) ** 2 == complex(15, 8), 'conjugate squares to 15 + 8i')
check(complex(1, -4) ** 2 == complex(-15, -8), 'swapped squares to -15 - 8i')
check(w['answer'] == '4-i' and {x['id']: x['tex'] for x in w['wrong']} == {'conjugate': '4+i', 'negative': '-4+i', 'swapped': '1-4i'}, 'key and slips')
for s in ['16 - 8i + i^2 = 15 - 8i', '15 + 8i', '-15 - 8i', 'a^2 = 16', 'b = -4/a', 'ab = -4', '2ab = -8']:
    printed(it, s, 'e-square-root-parts')

print(f'{n - len(fails)} of {n} checks passed')
sys.exit(1 if fails else 0)
