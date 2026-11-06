"""Build app/content/exams/mock-oa-strats.json (brief: docs/briefs/mocks.md, section mock-oa-strats).

Deterministic: no randomness except fixed integer formulas for the large code tests. Every maths key is asserted two
ways here (closed form, and enumeration, a series or a numerical method); mock-oa-strats_check.py is the independent
second route over the written file. Code items: the solution is run on every hidden test in CPython to fill `expect`,
and a second method must agree on each. Standard library only.
Run: python3 -I docs/briefs/mocks-scripts/mock-oa-strats_build.py
"""
import itertools
import json
import math
import os
from bisect import bisect_left
from fractions import Fraction as F
from itertools import groupby

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', '..', '..', 'app', 'content', 'exams', 'mock-oa-strats.json')


def close(a, b, tol=1e-9):
    assert abs(float(a) - float(b)) <= tol * max(1.0, abs(float(b))), (a, b)


def series_exp(x, terms=30):
    """e^x as an exact Fraction partial sum (x a Fraction)."""
    s, t = F(0), F(1)
    for k in range(terms):
        s += t
        t = t * x / (k + 1)
    return s


E2 = math.exp(2)

# ---------------------------------------------------------------- maths keys, each two ways
# Q1 f(x) = ln(1 + 3x^2), f'(1)
q1 = F(6 * 1, 1 + 3 * 1 ** 2)
h = 1e-6
close(q1, (math.log(1 + 3 * (1 + h) ** 2) - math.log(1 + 3 * (1 - h) ** 2)) / (2 * h), 1e-8)
assert q1 == F(3, 2)
q1_wrong = {'no-inner': F(1, 4), 'inside-only': F(6), 'value': math.log(4)}

# Q2 eigenvalues of [[5, 4], [1, 2]]
A = [[5, 4], [1, 2]]
tr, det = A[0][0] + A[1][1], A[0][0] * A[1][1] - A[0][1] * A[1][0]
disc = tr * tr - 4 * det
roots = sorted([(tr - math.isqrt(disc)) // 2, (tr + math.isqrt(disc)) // 2])
assert math.isqrt(disc) ** 2 == disc and roots == [1, 6]
for lam, v in ((6, (4, 1)), (1, (1, -1))):
    Av = (A[0][0] * v[0] + A[0][1] * v[1], A[1][0] * v[0] + A[1][1] * v[1])
    assert Av == (lam * v[0], lam * v[1])
assert (tr, det) == (7, 6)

# Q3 lim (e^{2x} - 1 - 2x) / x^2
q3 = F(2 ** 2, math.factorial(2))
xq = F(1, 10 ** 4)
quot = (series_exp(2 * xq, 12) - 1 - 2 * xq) / xq ** 2
close(quot, 2 + F(4, 3) * xq, 1e-7)
assert q3 == 2 and abs(quot - 2) < F(1, 1000)
q3_quot = float(quot)            # 2.000133..., stated as 2.0001

# Q4 Bayes on a probability tree
pA, pB, fA, fB = F(60, 100), F(40, 100), F(2, 100), F(5, 100)
q4 = pB * fB / (pA * fA + pB * fB)
nA, nB = 1000 * pA * fA, 1000 * pB * fB          # counts out of 1,000 trades
assert (nA, nB) == (12, 20) and q4 == nB / (nA + nB) == F(5, 8)
q4_wrong = {'other-branch': 1 - q4, 'rate-only': fB, 'rates-only': fB / (fA + fB)}
assert q4_wrong['other-branch'] == F(3, 8) and abs(float(q4_wrong['rates-only']) - 0.714) < 0.0005


# Q5 integral of ln(x) / x^2 over [1, e]
def anti5(x):
    return -math.log(x) / x - 1 / x


q5 = 1 - 2 / math.e
close(anti5(math.e) - anti5(1), q5)
n = 2000
hx = (math.e - 1) / n
simp = sum((1 if k in (0, n) else 4 if k % 2 else 2) * math.log(1 + k * hx) / (1 + k * hx) ** 2
           for k in range(n + 1)) * hx / 3
close(simp, q5, 1e-10)
q5_wrong = {'no-boundary': 1 - 1 / math.e, 'sign-v': 2 / math.e - 1, 'no-lower': -2 / math.e}
close((-1 / math.e) - (-1), q5_wrong['no-boundary'])           # only -1/x kept
close(-(anti5(math.e) - anti5(1)), q5_wrong['sign-v'])          # v = +1/x flips every sign
close(anti5(math.e), q5_wrong['no-lower'])
assert anti5(1) == -1


# Q6 y' = 2y + 4, y(0) = 1, y(1)
def rk4(f, y, t1, steps):
    hh, t = t1 / steps, 0.0
    for _ in range(steps):
        k1 = f(t, y); k2 = f(t + hh / 2, y + hh * k1 / 2); k3 = f(t + hh / 2, y + hh * k2 / 2); k4 = f(t + hh, y + hh * k3)
        y += hh * (k1 + 2 * k2 + 2 * k3 + k4) / 6
        t += hh
    return y


steady, C6 = F(-4, 2), 1 - F(-4, 2)
q6 = 3 * E2 - 2
assert (steady, C6) == (-2, 3)
close(rk4(lambda t, y: 2 * y + 4, 1.0, 1.0, 10000), q6, 1e-10)
q6_wrong = {'no-constant': E2, 'no-steady': 3 * E2, 'steady-4': 5 * E2 - 4}

# Q7 nine trades split at random into three books of three; three named trades (0, 1, 2) share a book
q7 = F(2, 8) * F(1, 7)
splits = set()
for t in set(itertools.permutations([0, 0, 0, 1, 1, 1, 2, 2, 2])):     # book label of each trade
    splits.add(tuple(sorted(tuple(i for i in range(9) if t[i] == bk) for bk in range(3))))
together = sum(1 for sp in splits if any({0, 1, 2} <= set(x) for x in sp))
assert len(splits) == 280 and together == 10 and q7 == F(together, len(splits)) == F(1, 28)
q7_wrong = {'independent': F(1, 3) ** 2, 'one-book': F(1, math.comb(9, 3)), 'two-only': F(2, 8)}
assert q7_wrong['one-book'] == F(1, 84) and q7_wrong['two-only'] == F(1, 4)

# Q8 smallest corr(X, Z) given 0.8 and 0.8
a = b = F(8, 10)


def det3(r):
    return 1 + 2 * a * b * r - a * a - b * b - r * r


q8 = a * b - F(36, 100)                          # sqrt((1 - 0.64)(1 - 0.64)) = 0.36 exactly
assert (1 - a * a) == F(36, 100) * 1 and F(6, 10) ** 2 == F(36, 100)
assert det3(q8) == 0 and det3(F(27, 100)) < 0 and det3(F(29, 100)) > 0 and det3(F(1)) == 0
close(math.cos(2 * math.acos(0.8)), q8)
q8_wrong = {'product': a * b, 'linear': a + b - 1, 'zero': F(0)}
ang = math.degrees(math.acos(0.8))               # 36.87, stated as 36.9; twice is 73.74, stated 73.7

# ---------------------------------------------------------------- code items


def net_positions(fills):
    net = {}
    for fill in fills:
        account, side, qty = fill.split()
        q = int(qty)
        net[account] = net.get(account, 0) + (q if side == "B" else -q)
    return [[acc, v] for acc, v in sorted(net.items()) if v != 0]


def net_positions_b(fills):                      # second method: sort by account, then group
    rows = sorted((f.split() for f in fills), key=lambda r: r[0])
    out = []
    for acc, grp in groupby(rows, key=lambda r: r[0]):
        s = sum(int(q) * (1 if side == 'B' else -1) for _, side, q in grp)
        if s:
            out.append([acc, s])
    return out


def longest_within(volumes, limit):
    best, left, total = 0, 0, 0
    for right, v in enumerate(volumes):
        total += v
        while total > limit:
            total -= volumes[left]
            left += 1
        best = max(best, right - left + 1)
    return best


def longest_within_b(volumes, limit):            # second method: prefix sums and a binary search per end
    pre = [0]
    for v in volumes:
        pre.append(pre[-1] + v)
    best = 0
    for j in range(1, len(pre)):
        i = bisect_left(pre, pre[j] - limit)     # the earliest start with pre[j] - pre[i] <= limit
        best = max(best, j - i)
    return best


C1_SOL = '''def net_positions(fills):
    net = {}
    for fill in fills:
        account, side, qty = fill.split()
        q = int(qty)
        net[account] = net.get(account, 0) + (q if side == "B" else -q)
    return [[a, n] for a, n in sorted(net.items()) if n != 0]
'''
C1_START = 'def net_positions(fills):\n    return []\n'
C2_SOL = '''def longest_within(volumes, limit):
    best, left, total = 0, 0, 0
    for right, v in enumerate(volumes):
        total += v
        while total > limit:
            total -= volumes[left]
            left += 1
        best = max(best, right - left + 1)
    return best
'''
C2_START = 'def longest_within(volumes, limit):\n    return 0\n'

C1_BIG = "F = ['A%05d %s %d' % (i % 50000, 'B' if i % 3 else 'S', i % 97 + 1) for i in range(100000)]"
C1_CASES = [
    (None, ["K7 B 300", "M2 S 100", "K7 S 120"]),
    (None, []),
    (None, ["A1 B 50", "A1 S 50"]),
    (None, ["Z9 B 5", "B3 B 7", "M4 B 1"]),
    (None, ["Q1 S 40"]),
    (None, ["X1 B 12", "X1 B 30"]),
    (None, ["AB B 10", "A B 3", "B S 2"]),
    (None, ["K1 B 1000000", "K1 S 1", "K2 S 999999", "K2 B 999999"]),
    (None, ["P1 B 5", "P2 B 5", "P1 S 5", "P3 S 9", "P2 S 2"]),
    (C1_BIG, 'len'),
    (C1_BIG, 'sum'),
]
C1_EXAMPLES = [
    ["K7 B 300", "M2 S 100", "K7 S 120"],
    ["H4 B 25", "H4 S 25", "D2 B 8"],
]
C2_BIG = "V = [(i * 7919) % 100 + 1 for i in range(200000)]"
C2_CASES = [
    (None, ([4, 1, 1, 6, 2, 3], 8)),
    (None, ([], 5)),
    (None, ([9], 9)),
    (None, ([9], 8)),
    (None, ([1, 2, 3], 6)),
    (None, ([1, 2, 3], 5)),
    (None, ([12, 1, 1, 1, 5], 3)),
    (None, ([3, 3, 3, 3], 7)),
    (None, ([2, 7, 1, 1, 1, 8], 9)),
    ('[1] * 200000', 150000),
    (C2_BIG, 5000),
    ('[10**6] + [1] * 199999', 199999),
]
C2_EXAMPLES = [([4, 1, 1, 6, 2, 3], 8), ([1, 2, 3], 5)]


def c1_test(setup, arg):
    if setup is None:
        call = f'[list(p) for p in net_positions({json.dumps(arg)})]'
        exp = net_positions(arg)
        assert exp == net_positions_b(arg)
        return {'call': call, 'expect': repr(exp), 'compare': 'equal'}
    g = {}
    exec(setup, g)
    res = net_positions(g['F'])
    assert res == net_positions_b(g['F'])
    if arg == 'len':
        return {'setup': setup, 'call': 'len(net_positions(F))', 'expect': repr(len(res)), 'compare': 'equal'}
    return {'setup': setup, 'call': 'sum(p[1] for p in net_positions(F))', 'expect': repr(sum(p[1] for p in res)), 'compare': 'equal'}


def c2_test(setup, arg):
    if setup is None:
        vols, target = arg
        exp = longest_within(vols, target)
        assert exp == longest_within_b(vols, target)
        return {'call': f'longest_within({json.dumps(vols)}, {target})', 'expect': repr(exp), 'compare': 'equal'}
    if setup.startswith('V ='):
        g = {}
        exec(setup, g)
        vols = g['V']
        exp = longest_within(vols, arg)
        assert exp == longest_within_b(vols, arg)
        return {'setup': setup, 'call': f'longest_within(V, {arg})', 'expect': repr(exp), 'compare': 'equal'}
    vols = eval(setup)
    exp = longest_within(vols, arg)
    assert exp == longest_within_b(vols, arg)
    return {'call': f'longest_within({setup}, {arg})', 'expect': repr(exp), 'compare': 'equal'}


c1_tests = [c1_test(s, a) for s, a in C1_CASES]
c2_tests = [c2_test(s, a) for s, a in C2_CASES]
c1_examples = [{'call': f'[list(p) for p in net_positions({json.dumps(x)})]', 'expect': repr(net_positions(x)), 'compare': 'equal'} for x in C1_EXAMPLES]
c2_examples = [{'call': f'longest_within({json.dumps(v)}, {t})', 'expect': repr(longest_within(v, t)), 'compare': 'equal'} for v, t in C2_EXAMPLES]
assert c2_tests[9]['expect'] == '150000' and c2_tests[11]['expect'] == '199999'
BIG_C1_LEN = int(c1_tests[9]['expect'])
BIG_C2 = int(c2_tests[10]['expect'])

# ---------------------------------------------------------------- the exam


def ch(iid, diff, skill, tag, pace, title, question, key, wrongs, correct, generic, explain):
    opts = [{'id': 'a', 'text': key, 'correct': True}]
    for k, (text, why) in enumerate(wrongs):
        opts.append({'id': 'bcde'[k], 'text': text, 'why': why})
    return {'id': iid, 'difficulty': diff, 'skills': [skill], 'tags': [tag], 'pace': pace, 'title': title,
            'question': question,
            'widget': {'kind': 'choice', 'layout': 'stack', 'shuffle': True, 'label': 'Answer options', 'options': opts},
            'feedback': {'correct': correct, 'generic': generic}, 'explain': {'text': explain}}


maths = [
    ch('m1-chain-rule', 2, 'lm-chain', 'chain-rule', 120, 'A slope through a logarithm',
       "Let $f(x) = \\ln(1 + 3x^2)$. What is $f'(1)$?",
       '$\\tfrac{3}{2}$',
       [('$\\tfrac{1}{4}$', 'You differentiated the logarithm and left out the inner derivative, $6x$.'),
        ('$6$', 'You differentiated only the inside, $6x$, and left out the factor $1/(1 + 3x^2)$.'),
        ('$\\ln 4$', 'You gave $f(1)$, the value of the function, not its slope.')],
       'Right: the outer derivative times the inner one.',
       'Differentiate the logarithm, then multiply by the derivative of $1 + 3x^2$.',
       "By the chain rule, $f'(x) = \\dfrac{6x}{1 + 3x^2}$. At $x = 1$ that is $\\tfrac{6}{4} = 1.5$. "
       'A central difference with a step of $10^{-6}$ gives 1.5 too.'),
    ch('m2-eigenvalues', 2, 'eg-eigen', 'eigenvalues-2x2', 120, 'Eigenvalues of a 2 by 2 matrix',
       'What are the eigenvalues of $A = \\begin{pmatrix} 5 & 4 \\\\ 1 & 2 \\end{pmatrix}$?',
       '$1$ and $6$',
       [('$2$ and $5$', 'You read the diagonal entries. They are the eigenvalues only of a triangular matrix.'),
        ('$-1$ and $-6$', 'You solved $\\lambda^2 + 7\\lambda + 6 = 0$. The trace enters with a minus sign.'),
        ('$6$ and $7$', 'You gave the determinant and the trace. The eigenvalues are the two numbers with that product and sum.')],
       'Right: the roots of the characteristic polynomial.',
       'Write $\\det(A - \\lambda I) = 0$ and solve the quadratic.',
       'The characteristic polynomial is $\\lambda^2 - 7\\lambda + 6 = (\\lambda - 1)(\\lambda - 6)$, so the eigenvalues are 1 and 6. '
       'Their sum is the trace, 7, and their product the determinant, 6. '
       'Check: $A(4, 1) = 6(4, 1)$ and $A(1, -1) = 1(1, -1)$.'),
    ch('m3-limit', 3, 'lm-limits', 'limit-series', 150, 'A limit from a series',
       'As $x$ tends to 0, what does $\\dfrac{e^{2x} - 1 - 2x}{x^2}$ tend to?',
       '$2$',
       [('$4$', 'You expanded $e^{2x}$ as $1 + 2x + (2x)^2$ and dropped the $\\tfrac{1}{2!}$.'),
        ('$\\tfrac{1}{2}$', 'You wrote the square term as $x^2/2$. It is $(2x)^2/2 = 2x^2$.'),
        ('$0$', 'You saw the first-order terms cancel and stopped. The $x^2$ term is what is left.')],
       'Right: the $x^2$ term of the series decides it.',
       'Expand $e^{2x}$ to the $x^2$ term, then divide by $x^2$.',
       'The series gives $e^{2x} = 1 + 2x + 2x^2 + O(x^3)$. So the top is $2x^2 + O(x^3)$, and the limit is 2. '
       'At $x = 10^{-4}$ the quotient is about 2.0001.'),
    ch('m4-probability-tree', 3, 'bayes', 'probability-tree', 150, 'Which route failed',
       '60% of a desk\'s trades settle through route A and 40% through route B. Of route A\'s trades, 2% fail. '
       'Of route B\'s, 5% fail. A trade fails. What is the chance it went through route B?',
       '$0.625$',
       [('$0.375$', 'You found the chance it went through route A, the other branch.'),
        ('$0.05$', 'You gave the failure rate of route B, not the chance of route B given a failure.'),
        ('$0.714$', 'You compared the failure rates, 5 against 2, and left out the 60% and 40% split.')],
       'Right: the failures from B over all the failures.',
       'Find the failures through each route, then take B\'s share of them.',
       'Failures through A are $0.6 \\times 0.02 = 0.012$, and through B $0.4 \\times 0.05 = 0.02$. '
       'So the chance is $0.02 / 0.032 = 0.625$. Out of 1,000 trades, 12 fail through A and 20 through B.'),
    ch('m5-by-parts', 3, 'in-techniques', 'by-parts', 180, 'An integral by parts',
       'What is $\\displaystyle\\int_1^e \\dfrac{\\ln x}{x^2}\\,dx$?',
       '$1 - \\tfrac{2}{e}$',
       [('$1 - \\tfrac{1}{e}$', 'You dropped the boundary term $-\\tfrac{\\ln x}{x}$ that parts gives, and kept only $-\\tfrac{1}{x}$.'),
        ('$\\tfrac{2}{e} - 1$', 'You took $v = \\tfrac{1}{x}$, so every sign flipped. The integral of $x^{-2}$ is $-x^{-1}$.'),
        ('$-\\tfrac{2}{e}$', 'You left out the lower limit. The antiderivative is $-1$ at $x = 1$, not 0.')],
       'Right: parts, then both limits.',
       'Integrate by parts with $u = \\ln x$, then evaluate at both limits.',
       'By parts with $u = \\ln x$ and $dv = x^{-2}\\,dx$, the antiderivative is $-\\tfrac{\\ln x}{x} - \\tfrac{1}{x}$. '
       'It is $-\\tfrac{2}{e}$ at $e$ and $-1$ at 1. '
       'So the integral is $1 - \\tfrac{2}{e} \\approx 0.264$.'),
    ch('m6-linear-ode', 3, 'de-first', 'linear-ode', 180, 'A first-order equation',
       "Solve $y' = 2y + 4$ with $y(0) = 1$. What is $y(1)$?",
       '$3e^2 - 2$',
       [('$e^2$', "You solved $y' = 2y$ and dropped the constant 4."),
        ('$3e^2$', 'You found $C = 3$ but left out the steady state, $-2$.'),
        ('$5e^2 - 4$', "You set the steady state to $-4$. Setting $y' = 0$ gives $2y + 4 = 0$, so it is $-2$.")],
       'Right: the steady state plus a decaying or growing term.',
       "Find the steady state from $y' = 0$, then fit the constant to $y(0) = 1$.",
       'The steady state solves $2y + 4 = 0$, so $y = -2 + Ce^{2x}$. '
       'Then $y(0) = 1$ gives $C = 3$. So $y(1) = 3e^2 - 2 \\approx 20.17$.'),
    ch('m7-shared-book', 4, 'cc-count', 'shared-book', 180, 'Three trades in one book',
       'Nine trades are split at random into three books of three trades each. '
       'What is the chance that three named trades all land in the same book?',
       '$\\tfrac{1}{28}$',
       [('$\\tfrac{1}{9}$', "You treated each trade's book as an independent pick of one in three. A book fills up, so the picks are not independent."),
        ('$\\tfrac{1}{84}$', 'You counted only one of the three books. Any of the three can hold the named trades.'),
        ('$\\tfrac{1}{4}$', 'You found the chance that two named trades share a book, and stopped before the third.')],
       'Right: place one trade, then fill the two places left in its book.',
       'Place the first named trade, then ask where the other two can go.',
       'Put the first named trade anywhere. The second joins its book with chance $\\tfrac{2}{8}$, and the third with chance $\\tfrac{1}{7}$. '
       'So the chance is $\\tfrac{2}{56} = \\tfrac{1}{28} \\approx 0.036$, and 10 of all 280 splits keep them together.'),
    ch('m8-correlation-bound', 4, 'eg-pd', 'correlation-bound', 210, 'How low can a correlation go',
       'The correlation of $X$ and $Y$ is 0.8, and the correlation of $Y$ and $Z$ is 0.8. '
       'What is the smallest possible correlation of $X$ and $Z$?',
       '$0.28$',
       [('$0.64$', 'You multiplied the two correlations. That is the value when $X$ and $Z$ are linked only through $Y$.'),
        ('$0.6$', 'You added the two and took off 1. That is not a bound: values down to 0.28 are possible.'),
        ('$0$', 'You assumed two positive links only rule out a negative one. The matrix forces more than that.')],
       'Right: the correlation matrix must stay positive semidefinite.',
       'Write the 3 by 3 correlation matrix with an unknown $r$ and ask when it is positive semidefinite.',
       'The correlation matrix must be positive semidefinite, and here that needs its determinant $-r^2 + 1.28r - 0.28$ to be at least 0. '
       'That holds for $r$ from 0.28 to 1. '
       'In angles, each pair is $36.9^\\circ$ apart, so $X$ and $Z$ are at most $73.7^\\circ$ apart, and $\\cos 73.7^\\circ \\approx 0.28$.'),
]
order = ['m1-chain-rule', 'm2-eigenvalues', 'm3-limit', 'm4-probability-tree', 'm5-by-parts', 'm6-linear-ode', 'm7-shared-book', 'm8-correlation-bound']
maths = sorted(maths, key=lambda it: order.index(it['id']))
assert [it['difficulty'] for it in maths] == [2, 2, 3, 3, 3, 3, 4, 4]

code_items = [
    {'id': 'c1-net-positions', 'difficulty': 2, 'skills': ['ds-hashing'], 'tags': ['net-positions'], 'pace': 720,
     'title': 'Net positions from fills',
     'question': 'Each fill is a string `"ACCOUNT SIDE QTY"`, such as `"K7 B 300"`. Side `B` adds the quantity to the '
                 "account's position, and side `S` takes it away. Write `net_positions(fills)`. It returns a list of "
                 '`[account, net]` pairs, sorted by account name. Leave out any account whose net is 0. Quantities '
                 'are whole numbers, and there may be 100,000 fills.',
     'widget': {'kind': 'code', 'language': 'python', 'starter': C1_START, 'examples': c1_examples, 'tests': c1_tests,
                'how': f'There are {len(c1_tests)} hidden tests. Each answer must equal the expected value. The last two use 100,000 fills.',
                'solution': C1_SOL},
     'feedback': {'correct': 'All the tests pass, including the 100,000 fills.',
                  'generic': 'A hidden test failed. Check the sign of a sale, the zero nets, the order and the large case.'},
     'explain': {'text': "A dictionary keeps each account's running net, in constant time per fill. "
                         'Sort the accounts once at the end and drop the zeros. '
                         'A search through a list of accounts is quadratic, and 100,000 fills stop it.'}},
    {'id': 'c2-longest-within', 'difficulty': 3, 'skills': ['ds-pointers'], 'tags': ['longest-within'], 'pace': 960,
     'title': 'The longest run of days within a volume',
     'question': '`volumes[i]` is the volume traded on day `i`, a positive whole number. Write '
                 '`longest_within(volumes, limit)`. It returns the most neighbouring days whose volumes add up to at '
                 'most `limit`. It returns 0 if every single day is over `limit`. `limit` is a positive whole '
                 'number, and there may be 200,000 days.',
     'widget': {'kind': 'code', 'language': 'python', 'starter': C2_START, 'examples': c2_examples, 'tests': c2_tests,
                'how': f'There are {len(c2_tests)} hidden tests. Each answer must equal the expected value. The last three use 200,000 days.',
                'solution': C2_SOL},
     'feedback': {'correct': 'All the tests pass, including the 200,000 days.',
                  'generic': 'A hidden test failed. Check a run that equals the limit, a limit below every day and the large cases.'},
     'explain': {'text': "Volumes are positive, so a run's sum grows as it widens and falls as it narrows. "
                         'Widen on the right, shrink from the left while the sum exceeds `limit`, and keep the longest run. '
                         'Each day enters and leaves once, so the work is $O(n)$.'}},
]

exam = {
    'id': 'mock-oa-strats',
    'name': 'Strats online assessment',
    'style': 'strats',
    'models': 'Reported, as of Nov 2026: the Goldman Sachs strats online test. A 30-minute coding paper, then 8 maths questions in 22 minutes.',
    'description': 'This is the reported format of a bank strats online test, as candidates described it by Nov 2026. '
                   'A 30-minute coding paper comes first, with two short Python problems. '
                   'Hidden tests include large inputs, so a slow answer fails them. '
                   'You pass the coding paper only with both problems; this line is illustrative, as firms do not publish cut-offs. '
                   'Then a 22-minute maths paper has eight multiple-choice questions. '
                   'They cover calculus, linear algebra and probability. '
                   'Reports give no calculator rule, so sit the maths paper with a pen and paper only. '
                   'Older reports give more questions over three hours. '
                   'Use no search engine and no notes.',
    'requires': ['ds/L2', 'eigen/L2'],
    'skills': {'ds-hashing': 'Hash maps', 'ds-pointers': 'Pointers and windows', 'lm-chain': 'Derivatives',
               'lm-limits': 'Limits', 'in-techniques': 'Integration', 'de-first': 'First-order equations',
               'eg-eigen': 'Eigenvalues', 'eg-pd': 'Positive definite matrices', 'bayes': "Bayes' rule",
               'cc-count': 'Counting'},
    'parts': [
        {'kind': 'paper', 'id': 'code', 'name': 'Software fundamentals', 'minutes': 30,
         'scoring': {'right': 1, 'wrong': 0, 'blank': 0}, 'pass': 1, 'items': code_items},
        {'kind': 'paper', 'id': 'maths', 'name': 'Maths', 'minutes': 22,
         'scoring': {'right': 1, 'wrong': 0, 'blank': 0}, 'pass': 0.625, 'items': maths},
        {'kind': 'check', 'id': 'no-calculator', 'name': 'I used no calculator on the maths paper',
         'detail': 'Tick this only if you worked every maths question by hand.'},
        {'kind': 'check', 'id': 'no-lookup', 'name': 'I used no search engine and no notes',
         'detail': 'Tick this only if you sat both papers without either.'},
    ],
}
assert sum(it['pace'] for it in code_items) == 1680 and sum(it['pace'] for it in maths) == 1290
assert len(exam['models']) <= 200

with open(OUT, 'w', encoding='utf8') as f:
    json.dump(exam, f, ensure_ascii=False, indent=1)
    f.write('\n')
print(f'wrote {os.path.relpath(OUT)}: 10 items; C1 large len {BIG_C1_LEN}, C2 large {BIG_C2}; '
      f'Q3 quotient {q3_quot:.6f}; Q8 angle {ang:.3f}')
print('ALL AGREE')
