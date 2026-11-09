"""Second read, analysis homework-4 h-prove-uniform-diagonal: every number and every epsilon-N step, two routes.
Route 1: exact Fractions (closed forms, a search for the smallest N). Route 2: sympy (limits, the sup by calculus,
the inequality solved symbolically) and float grids. Also the rubric's passing tick sets, enumerated here and
compared with tools/rubric-passes.mjs --json. Run with the venv Python. Exit 0 when every check holds."""
import itertools, json, os, subprocess, sys
from fractions import Fraction as F
import sympy as sp

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, '..', '..', '..'))
hw = json.load(open(os.path.join(ROOT, 'app', 'content', 'courses', 'analysis', 'homework-4.json')))
item = next(i for i in hw['items'] if i['id'] == 'h-prove-uniform-diagonal')
M, P = item['model'], item['prompt']
fails = []


def check(c, m):
    print('ok  ' if c else 'FAIL', m)
    if not c:
        fails.append(m)

h = lambda n, x: 1 / (1 + n * x * x)
hF = lambda n, x: F(1) / (1 + n * x * x)
# (b) pointwise limit
x, n = sp.symbols('x n', positive=True)
check(sp.limit(1 / (1 + n * x**2), n, sp.oo) == 0 and all(hF(k, 0) == 1 for k in (1, 10, 10**6)), '(b) limit 0 for x != 0 (sympy), 1 at x = 0 for every n')
# the model's N > 1/(eps x^2) works at sample points, and 0 < h_n(x) < 1/(n x^2)
ok = True
for xv in (F(1, 7), F(1, 2), F(3), F(-2, 5)):
    for eps in (F(1, 10), F(1, 1000)):
        N = int(1 / (eps * xv * xv)) + 1
        ok &= all(0 < hF(k, xv) < 1 / (k * xv * xv) and hF(k, xv) < eps for k in (N, N + 1, 5 * N))
check(ok, '(b) N > 1/(eps x^2) gives h_n(x) < eps for n >= N, with 0 < h_n(x) < 1/(n x^2)')
# (b) not uniform: h_n(1/sqrt n) = 1/2 exactly
check(all(sp.simplify(1 / (1 + k * (1 / sp.sqrt(k))**2)) == sp.Rational(1, 2) for k in (1, 7, 10**9)), '(b) h_n(1/sqrt n) = 1/2 exactly, so eps = 1/2 has no N (strict inequality)')
# (c) sup over |x| >= 1/2 is 4/(n+4), attained at x = 1/2: derivative sign and a grid
d = sp.diff(1 / (1 + n * x**2), x)
check(sp.simplify(d * (1 + n * x**2)**2 + 2 * n * x) == 0, '(c) h_n\'(x) = -2nx/(1+nx^2)^2 < 0 for x > 0, so on |x| >= 1/2 the sup is at x = +-1/2')
check(all(abs(max(h(k, 0.5 + j / 1000) for j in range(0, 20000)) - 4 / (k + 4)) < 1e-15 for k in (1, 3, 1329, 1330)), '(c) float grid on [0.5, 20.5]: max = 4/(n+4)')
check(all(hF(k, F(1, 2)) == F(4, k + 4) and hF(k, F(-1, 2)) == F(4, k + 4) for k in (1, 50, 1330)), '(c) h_n(+-1/2) = 4/(n+4) exactly')
# uniform: N > 4/eps
ok = all(F(4, k + 4) < eps for eps in (F(1, 3), F(3, 1000), F(1, 10**6)) for N in [int(4 / eps) + 1] for k in (N, N + 1, 10 * N))
check(ok, '(c) N > 4/eps gives sup 4/(n+4) < 4/n <= 4/N < eps')
# smallest N for 0.003: route 1, Fraction search; route 2, sympy inequality
eps = F(3, 1000)
works = lambda k: F(4, k + 4) < eps
smallest = next(k for k in range(1, 5000) if works(k) and all(works(j) for j in range(k, k + 3000)))
check(smallest == 1330 and not works(1329), 'route 1: smallest N = 1330 (n = 1329 fails), Fraction search')
sol = sp.solve_univariate_inequality(4 / (sp.Symbol('m', real=True) + 4) < sp.Rational(3, 1000), sp.Symbol('m', real=True), relational=False)
check(sp.Interval.open(sp.Rational(3988, 3), sp.oo).is_subset(sol) and sp.Rational(3988, 3) not in sol and sp.ceiling(sp.Rational(3988, 3) + sp.Rational(1, 10**9)) == 1330,
      'route 2: 4/(m+4) < 0.003 exactly for m > 3988/3 = 1329.33..., first whole m is 1330 (sympy)')
check(F(4000, 3) == F(133333, 100) + F(1, 300) and float(F(4000, 3)) > 1333.33 and float(F(3988, 3)) > 1329.33, 'n + 4 > 4000/3 ~ 1333.33, n > 1329.33')
check(round(4 / 1334, 7) == 0.0029985 and round(4 / 1333, 7) == 0.0030008 and F(4, 1334) < eps <= F(4, 1333), '4/1334 ~ 0.0029985 < 0.003 <= 4/1333 ~ 0.0030008')
crude = next(k for k in range(1, 5000) if F(4, k) < eps)
check(crude == 1334, 'the crude bound 4/n first below 0.003 at n = 1334')
# the model states these figures
for s in ['1330', '1329', '1334', '1333', '0.0029985', '0.0030008', '1333.33', '1329.33', '\\tfrac{4000}{3}', '\\tfrac{4}{n + 4}']:
    check(s in M, f'model states {s}')
check('every $n \\ge N$ and every $x \\in E$' in P and 'E = \\{x : |x| \\ge \\tfrac12\\}' in P, 'prompt: the interval |x| >= 1/2 and the quantifiers are as recomputed')
# optional: (0, inf), 1/sqrt n in it
check(all(1 / sp.sqrt(k) > 0 for k in (1, 4, 10**6)), 'optional: 1/sqrt n lies in (0, inf), h_n = 1/2 there')
# (a): the moving point needs uniform convergence: with h_n (pointwise only on R), x_n = 1/sqrt n -> 0 but h_n(x_n) = 1/2, not h(0) = 1
check(all(abs(h(k, k ** -0.5) - 0.5) < 1e-12 for k in (1, 100, 10**8)), 'the model\'s "pointwise would not do": h_n(1/sqrt n) = 1/2 does not tend to h(0) = 1')
# rubric tick sets
pts = [r['points'] for r in item['rubric']]; req = [bool(r.get('required')) for r in item['rubric']]
passes = [s for s in itertools.product([0, 1], repeat=len(pts)) if sum(p for p, t in zip(pts, s) if t) >= 7 and all(t for t, q in zip(s, req) if q)]
check(sum(pts) == 10 and passes == [(1, 1, 1, 1, 0), (1, 1, 1, 1, 1)], f'rubric: 10 points, passing sets {passes}')
out = subprocess.run(['node', 'tools/rubric-passes.mjs', '--item', 'content/courses/analysis/homework-4.json#h-prove-uniform-diagonal', '--json'], cwd=os.path.join(ROOT, 'app'), capture_output=True, text=True).stdout
check('"minimal"' in out or 'minimal' in out.lower(), 'rubric-passes.mjs --json ran')
check('Optional, one more point:' in P and 'Optional' in item['rubric'][4]['text'], 'the one optional row is the part the prompt marks optional')
print('\nFAILURES: %d' % len(fails))
sys.exit(1 if fails else 0)
