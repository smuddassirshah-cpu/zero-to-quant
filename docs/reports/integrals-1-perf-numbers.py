"""integrals L1 performance task h-derive-falling-area: every stated number, computed twice.

Run from the repository root with the venv that has sympy and scipy:
    <venv>/bin/python -I docs/reports/integrals-1-perf-numbers.py
Route 1 is exact (Fractions, and sympy summation and limits); route 2 is numeric (float sums, scipy quad).
Without sympy or scipy those checks are reported as skipped; the Fraction and float routes still run.
"""
import itertools
import json
import os
import sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', '..', 'app', 'tools'))
from numbers_lib import Level  # noqa: E402

lv = Level("integrals", 1)
HW = os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'integrals', 'homework-1.json')
items = json.load(open(HW, encoding='utf-8'))['items']
idx = [i for i, it in enumerate(items) if it['id'] == 'h-derive-falling-area']
lv.claim(len(idx) == 1, "the item exists once")
I = idx[0]
it = items[I]
M, P = f"items[{I}].model", f"items[{I}].prompt"


def f(x):
    return 9 - x * x


def R_sum(n):            # right sum, exact, straight from the heights
    return sum(f(1 + F(2 * k, n)) * F(2, n) for k in range(1, n + 1))


def L_sum(n):            # left sum, exact
    return sum(f(1 + F(2 * k, n)) * F(2, n) for k in range(0, n))


def R_formula(n):        # the model's closed forms
    return F(28, 3) - F(8, n) - F(4, 3 * n * n)


def L_formula(n):
    return F(28, 3) + F(8, n) - F(4, 3 * n * n)


def R_unsimplified(n):   # the model's middle line, with the two sum formulas
    return 16 - F(4 * (n + 1), n) - F(4 * (n + 1) * (2 * n + 1), 3 * n * n)


def L_unsimplified(n):
    return 16 - F(4 * (n - 1), n) - F(4 * (n - 1) * (2 * n - 1), 3 * n * n)


# setting up: the height expansion, for every k and n tried
ok =all(f(1 + F(2 * k, n)) == 8 - F(4 * k, n) - F(4 * k * k, n * n) for n in range(1, 40) for k in range(0, n + 1))
lv.claim(ok, "height 9 - (1 + 2k/n)^2 = 8 - 4k/n - 4k^2/n^2, n < 40")
# (a) the pulled-out factors: sum of 16/n over n terms is 16; the 8/n^2 and 8/n^3 factors
ok = all(R_sum(n) == 16 - F(8, n * n) * sum(range(1, n + 1)) - F(8, n ** 3) * sum(k * k for k in range(1, n + 1)) for n in range(1, 60))
lv.claim(ok, "R_n = 16 - 8/n^2 sum k - 8/n^3 sum k^2, n < 60")
ok = all(sum(range(1, n + 1)) == n * (n + 1) // 2 and sum(k * k for k in range(1, n + 1)) == n * (n + 1) * (2 * n + 1) // 6 for n in range(1, 200))
lv.claim(ok, "the two sum formulas, n < 200")
ok = all(R_sum(n) == R_unsimplified(n) == R_formula(n) for n in range(1, 200))
lv.claim(ok, "R_n: direct sum = middle line = 28/3 - 8/n - 4/(3n^2), n < 200")
ok = all(F(4 * (n + 1), n) == 4 + F(4, n) and 4 * (n + 1) * (2 * n + 1) == 8 * n * n + 12 * n + 4
         and F(8 * n * n + 12 * n + 4, 3 * n * n) == F(8, 3) + F(4, n) + F(4, 3 * n * n) for n in range(1, 200))
lv.claim(ok, "the collecting steps 4(n+1)/n = 4 + 4/n and (8n^2 + 12n + 4)/(3n^2) = 8/3 + 4/n + 4/(3n^2)")
lv.claim(16 - 4 - F(8, 3) == F(28, 3), "16 - 4 - 8/3 = 28/3")
# (c) left sums and the gap
ok = all(L_sum(n) == L_unsimplified(n) == L_formula(n) for n in range(1, 200))
lv.claim(ok, "L_n: direct sum = middle line = 28/3 + 8/n - 4/(3n^2), n < 200")
ok = all(L_sum(n) - R_sum(n) == F(16, n) == abs(f(3) - f(1)) * F(2, n) for n in range(1, 200))
lv.claim(ok, "gap L_n - R_n = 16/n = |f(3) - f(1)| 2/n")
ok = all(R_sum(n) < F(28, 3) < L_sum(n) for n in range(1, 200))
lv.claim(ok, "R_n < 28/3 < L_n for every n < 200 (falling f)")
ok = all(f(1 + F(2 * k, n)) < f(1 + F(2 * (k - 1), n)) for n in range(1, 30) for k in range(1, n + 1))
lv.claim(ok, "f falls along the strip ends")
# other routes: 9*2 = 18, int_0^3 x^2 = 9 by right sums, int_0^1 x^2 = 1/3
R03 = lambda n: sum((F(3 * k, n)) ** 2 * F(3, n) for k in range(1, n + 1))
lv.claim(all(R03(n) == F(9 * (n + 1) * (2 * n + 1), 2 * n * n) for n in range(1, 80)), "right sums of x^2 on [0,3] = 9(n+1)(2n+1)/(2n^2) -> 9")
lv.claim(18 - (9 - F(1, 3)) == F(28, 3) and 9 - F(1, 3) == F(26, 3), "split route 18 - 26/3 = 28/3")
# (d) n = 4
heights_r = [f(F(x)) for x in (F(3, 2), 2, F(5, 2), 3)]
heights_l = [f(F(x)) for x in (1, F(3, 2), 2, F(5, 2))]
lv.claim(heights_r == [F(27, 4), 5, F(11, 4), 0], "right heights 6.75, 5, 2.75, 0")
lv.claim(heights_l == [8, F(27, 4), 5, F(11, 4)], "left heights 8, 6.75, 5, 2.75")
lv.claim(sum(heights_r) == F(29, 2) and F(1, 2) * F(29, 2) == F(29, 4) == R_sum(4) == R_formula(4), "R_4 = 0.5 x 14.5 = 7.25, three ways")
lv.claim(sum(heights_l) == F(45, 2) and F(1, 2) * F(45, 2) == F(45, 4) == L_sum(4) == L_formula(4), "L_4 = 0.5 x 22.5 = 11.25, three ways")
lv.claim(F(28, 3) - 2 - F(1, 12) == F(29, 4) and F(28, 3) + 2 - F(1, 12) == F(45, 4), "28/3 -+ 2 - 1/12 = 7.25 and 11.25")
lv.claim(F(16, 4) == 4 == F(45, 4) - F(29, 4), "gap at n = 4 is 4")
lv.claim(abs(28 / 3 - 9.333) < 5e-4 and 7.25 < 28 / 3 < 11.25, "28/3 = 9.333 lies between 7.25 and 11.25")
# route 2: floats
for n in (4, 10, 1000, 10 ** 5):
    h = 2 / n
    r = sum((9 - (1 + k * h) ** 2) * h for k in range(1, n + 1))
    l_ = sum((9 - (1 + k * h) ** 2) * h for k in range(0, n))
    lv.claim(abs(r - float(R_formula(n))) < 1e-9 and abs(l_ - float(L_formula(n))) < 1e-9, f"float sums match the formulas at n = {n}")
lv.claim(abs(sum((9 - (1 + (k + 0.5) * 2e-5) ** 2) * 2e-5 for k in range(10 ** 5)) - 28 / 3) < 1e-9, "midpoint sum at n = 1e5 gives 28/3")

# symbolic and numeric libraries
try:
    import sympy as sp
    n, k, x = sp.symbols('n k x', positive=True, integer=False)
    ni = sp.Symbol('n', positive=True, integer=True)
    ki = sp.Symbol('k', integer=True)
    Rs = sp.summation((9 - (1 + 2 * ki / ni) ** 2) * 2 / ni, (ki, 1, ni))
    Ls = sp.summation((9 - (1 + 2 * ki / ni) ** 2) * 2 / ni, (ki, 0, ni - 1))
    lv.claim(sp.simplify(Rs - (sp.Rational(28, 3) - 8 / ni - sp.Rational(4, 3) / ni ** 2)) == 0, "sympy: R_n closed form")
    lv.claim(sp.simplify(Ls - (sp.Rational(28, 3) + 8 / ni - sp.Rational(4, 3) / ni ** 2)) == 0, "sympy: L_n closed form")
    lv.claim(sp.limit(Rs, ni, sp.oo) == sp.Rational(28, 3) == sp.limit(Ls, ni, sp.oo), "sympy: both limits 28/3")
    lv.claim(sp.simplify(Ls - Rs - 16 / ni) == 0, "sympy: gap 16/n")
    lv.claim(sp.integrate(9 - x ** 2, (x, 1, 3)) == sp.Rational(28, 3), "sympy: antiderivative check 28/3")
except ImportError:
    print("sympy not available: symbolic checks skipped (run with the venv)")
    lv.claim(False, "sympy route ran")
try:
    from scipy.integrate import quad
    val, err = quad(lambda t: 9 - t * t, 1, 3)
    lv.claim(abs(val - 28 / 3) < 1e-10, f"scipy quad gives {val:.10f} = 28/3")
except ImportError:
    print("scipy not available: quad check skipped (run with the venv)")
    lv.claim(False, "scipy route ran")

# figures stated in the model and prompt
for v in [r"\tfrac{28}{3} - \tfrac{8}{n} - \tfrac{4}{3n^2}", r"\tfrac{28}{3} + \tfrac{8}{n} - \tfrac{4}{3n^2}", r"8 - \tfrac{4k}{n} - \tfrac{4k^2}{n^2}",
          r"8n^2 + 12n + 4", r"\tfrac83 + \tfrac4n + \tfrac{4}{3n^2}", r"\tfrac{16}{n}", r"18 - \tfrac{26}{3} = \tfrac{28}{3}", r"9 - \tfrac13",
          r"0.5 \times 14.5 = 7.25", r"0.5 \times 22.5 = 11.25", r"\tfrac{28}{3} - 2 - \tfrac{1}{12} = 7.25", r"\tfrac{28}{3} + 2 - \tfrac{1}{12} = 11.25",
          r"4 = \tfrac{16}{4}", r"\tfrac{28}{3} \approx 9.333", "6.75, 5, 2.75 and 0", "8, 6.75, 5 and 2.75"]:
    lv.expect("homework", M, v)

# rubric: sums to 10, required rows as designed, and no pass skips a named part
rub = it['rubric']
pts = [r['points'] for r in rub]
req = [bool(r.get('required')) for r in rub]
lv.claim(sum(pts) == 10 and 3 <= len(rub) <= 5, "rubric 3 to 5 rows summing to 10")
lv.claim(req == [True, True, True, False, True], "rows 1, 2, 3 and 5 required, row 4 (the optional left-sum part) optional")
named = {0: 'a', 1: 'b', 2: 'c', 4: 'd'}      # row index (from 0) -> the named part it carries
passes = [s for r in range(1, len(rub) + 1) for s in itertools.combinations(range(len(rub)), r)
          if sum(pts[i] for i in s) >= 7 and all(i in s for i in range(len(rub)) if req[i])]
print("passing tick sets (rows from 1):", [tuple(i + 1 for i in s) for s in passes])
lv.claim(passes == [(0, 1, 2, 4), (0, 1, 2, 3, 4)], "the only passes are rows 1, 2, 3, 5 and all five")
lv.claim(all({named[i] for i in s if i in named} == {'a', 'b', 'c', 'd'} for s in passes), "every pass covers (a), (b), (c) and (d)")
lv.claim(it.get('performance') == 'derivation' and it.get('kind') == 'longform', "kind")
lv.claim(not any(key in it for key in ('starter', 'steps', 'order', 'derive', 'hints', 'parts')), "empty box: no scaffold")
lv.claim(sum(1 for x in items if x.get('performance')) == 1, "one performance task in the homework")
lv.claim(6 <= len(items) <= 12 and any(x['difficulty'] == 5 for x in items), "homework limits")
blob = json.dumps(it, ensure_ascii=False)
lv.claim('!' not in blob and '—' not in blob and '–' not in blob, "no ! or dashes")

lv.check_wrongs()
lv.report()
