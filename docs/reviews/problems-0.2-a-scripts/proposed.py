"""The numbers of every fix proposed in review-problems-0.2-a.md, each worked twice, and a freshness grep for the new
lines and curves across the functions course and the exams.

Run from the repo root with the scratchpad venv python. Exit 0 when every check holds.
"""
import glob
import re
import sys
from fractions import Fraction as Fr

import sympy as sp

checks = fails = 0


def ok(cond, msg):
    global checks, fails
    checks += 1
    if not cond:
        fails += 1
        print('FAIL', msg)


x, t = sp.symbols('x t')

# finding 10: p-path-and-pipe renumbered. A(-2, 1), B(5, 29), D(12, 23)
A, B, D = (-2, 1), (5, 29), (12, 23)
m1 = Fr(B[1] - A[1], B[0] - A[0])
c1 = A[1] - m1 * A[0]
ok((m1, c1) == (4, 9), f'path: gradient and intercept {m1}, {c1}')
ok(m1 * B[0] + c1 == B[1], 'path: fits B')
ok(Fr(B[0] - A[0], B[1] - A[1]) == Fr(1, 4), 'part 1 flipped = 0.25')
ok(abs(28 / (5 - 2) - 9.333) < 0.005, 'part 1 lost-minus = 9.333')
ok(A[1] - 8 == -7, 'part 2 sign: c = 1 - 8 = -7')
ok(A[1] - Fr(1, 4) * A[0] == Fr(3, 2), 'part 2 flipped: 0.25x + 1.5')
m2 = -1 / m1
ok(m2 == Fr(-1, 4), 'part 3 pipe gradient -0.25')
c2 = D[1] - m2 * D[0]
ok(c2 == 26, f'part 4 pipe intercept {c2}')
ok(D[1] - 3 == 20, 'part 4 sign: c = 23 - 3 = 20')
ok(D[1] - Fr(1, 4) * D[0] == 20, 'part 4 reciprocal: 0.25x + 20')
X = sp.solve(4 * x + 9 - (-sp.Rational(1, 4) * x + 26), x)[0]
ux, uy = B[0] - A[0], B[1] - A[1]
tp = Fr((D[0] - A[0]) * ux + (D[1] - A[1]) * uy, ux * ux + uy * uy)
foot = (A[0] + tp * ux, A[1] + tp * uy)
ok(X == 4 and foot == (4, 25), f'part 5 meeting point x = {X}, foot {foot}')
ok(0 < tp < 1, 'the foot lies between A and B')
ok(abs(17 / 3.75 - 4.533) < 0.005, 'part 5 sign-x = 4.533')
ok(abs(35 / 4.25 - 8.235) < 0.005, 'part 5 constants = 8.235')

# finding 13: p-sledge-cyclist parts 1 and 2 at 5 seconds
s5 = sp.Rational(1, 2) * 5**2
ok(s5 == sp.Rational(25, 2) and 0.5 * 25 == 12.5, 'sledge: 12.5 m after 5 s')
ok((0.5 * 5, (0.5 * 5)**2, 5**2) == (2.5, 6.25, 25), 'sledge part 1 slips 2.5, 6.25, 25')
ok(s5 / 5 == sp.Rational(5, 2) and 12.5 * 5 == 62.5, 'sledge part 2: 2.5 m/s, slip 62.5')
ok(2.5 < 3, 'still slower than the cyclist on average')

# finding 14: p-track-cubic renumbered to x(x - 6)^2 on 0 <= x <= 8
h = x**3 - 12 * x**2 + 36 * x
ok(sp.expand(x * (x - 6)**2) == h, 'track: factorised form')
ok(h.subs(x, 4) == 16 and 64 - 192 + 144 == 16, 'part 1 h(4) = 16')
ok(64 + 192 + 144 == 400 and 12 - 192 + 144 == -36, 'part 1 slips 400 and -36')
ok(sorted(set(sp.solve(h, x))) == [0, 6], 'part 2 roots 0 and 6')
ok(sorted(sp.solve(sp.diff(h, x), x)) == [2, 6], 'part 3 turning points 2 and 6')
ok(h.subs(x, 2) == 32 and h.subs(x, 8) == 32 and 512 - 768 + 288 == 32, 'part 4 h(2) = h(8) = 32')
ok(sorted(set(sp.solve(h - 32, x))) == [2, 8], 'part 4 solutions 2 and 8')
v = [float(h.subs(x, sp.Rational(k, 100))) for k in range(0, 801)]
ok(all(v[i + 1] > v[i] for i in range(0, 200)) and all(v[i + 1] < v[i] for i in range(200, 600)) and all(v[i + 1] > v[i] for i in range(600, 800)), 'track: up to 2, down to 6, up to 8')

# finding 16: the two powers given in p-two-cultures part 4
ok(round(2**3.3, 3) == 9.849 and round(2**3.4, 3) == 10.556, 'powers 9.849 and 10.556')
ok(round(200 * 9.849) == 1970 and round(200 * 10.556) == 2111, 'N of about 1970 and 2111 from the rounded powers')

# finding 4: p-climbing-wall part 4 in pence
ok(max(p for p in range(2000) if 4500 + 35 * p <= 30000) == 728, 'wall part 4: 728 pence')

# finding 19: sledge part 3 wrong band
ok(abs(6**0.5 - 2.449) < 0.05 and abs(2 - 2.449) > 0.05 and abs(2.5 - 2.449) > 0.05, 'lost-t band 0.05 keeps 2.45, drops 2 and 2.5')

# freshness of the new numbers: the functions course (bar the three sets) and the exams
files = [f for f in glob.glob('app/content/courses/functions/*.json') if 'problems-' not in f] + glob.glob('app/content/exams/topic-0.2.json')
blob = '\n'.join(open(f).read() for f in files)
for name, rx in {'y = 4x + 9': r'4x ?\+ ?9\b', 'y = -0.25x + 26': r'0\.25x ?\+ ?26', 'x(x - 6)^2': r'x\(x ?- ?6\)\^2|x\^3 ?- ?12x\^2',
                 'sledge 12.5 m in 5 s': r'12\.5 (m\b|metres)'}.items():
    ok(not re.search(rx, blob), f'{name} already appears in the functions course or the 0.2 exam')

print(f'proposed.py: {checks} checks, {fails} failures')
sys.exit(1 if fails else 0)
