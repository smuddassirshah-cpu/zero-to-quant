"""measure-prob L3 performance task h-prove-urn: every number and claim in the item, model and rubric, checked twice.
Route 1: exact enumeration of every string of draws (the atoms of F_n) with Fractions, up to n = 12.
Route 2: sympy algebra for the martingale step, and the known law of R_n (uniform on 1..n+1), plus a seeded simulation.
Run: python3 docs/reports/measure-prob-3-perf-numbers.py (sympy optional). Exits 0 when all agree."""
import json, os, random, sys, itertools
from fractions import Fraction as F
HERE = os.path.dirname(os.path.abspath(__file__))
HW = os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'measure-prob', 'homework-3.json')
fails = 0; checks = 0
def ok(cond, what):
    global fails, checks
    checks += 1
    if not cond:
        fails += 1; print('FAIL', what)

def path_prob(s):            # chance of a draw string s (tuple of 1 red / 0 blue), and R_n at its end
    r, p = 1, F(1)
    for i, d in enumerate(s):
        tot = i + 2
        p *= F(r, tot) if d else F(tot - r, tot)
        r += d
    return p, r

for n in range(0, 13):
    atoms = list(itertools.product((0, 1), repeat=n))
    tot = F(0); EM = F(0); Pred = F(0); law = {}
    for s in atoms:
        p, r = path_prob(s)
        tot += p
        ok(p > 0, f'atom {s} has positive chance')
        ok(r == 1 + sum(s) and 1 <= r <= n + 1, f'R_n = 1 + sum D and 1 <= R_n <= n+1 on {s}')
        M = F(r, n + 2)
        ok(0 < M < 1, f'0 < M_n < 1 on {s}')
        pr, rr = path_prob(s + (1,)); pb, rb = path_prob(s + (0,))
        ok(pr + pb == p, f'children of {s} add up')
        cond_red = pr / p
        ok(cond_red == M, f'P(red next | atom) = M_n on {s}')
        nxt = cond_red * F(rr, n + 3) + (pb / p) * F(rb, n + 3)
        ok(nxt == M, f'E[M_(n+1) | atom] = M_n on {s}')
        ok(F(r + M, n + 3) == M and F((n + 2) * M + M, n + 3) == M, f'lines 2 and 3 of the step on {s}')
        eR = cond_red * rr + (pb / p) * rb
        ok(eR == r + M and eR > r, f'E[R_(n+1) | atom] = R_n + M_n > R_n on {s}')
        EM += p * M; Pred += pr
        law[r] = law.get(r, F(0)) + p
    ok(tot == 1, f'atoms of F_{n} have total chance 1')
    ok(EM == F(1, 2), f'E[M_{n}] = 1/2')
    ok(Pred == F(1, 2), f'P(draw {n + 1} red) = 1/2')
    ok(all(law[r] == F(1, n + 1) for r in range(1, n + 2)), f'R_{n} uniform on 1..{n + 1} (route 2 for E[M_n])')
    ok(sum((F(r, n + 2) * F(1, n + 1) for r in range(1, n + 2)), F(0)) == F(1, 2), f'uniform law gives E[M_{n}] = 1/2')
    ok(len(atoms) == 2 ** n, f'{2 ** n} atoms')

# the check on one atom: red, red
p, r = path_prob((1, 1))
ok(r == 3 and F(r, 4) == F(3, 4), 'after red, red: R_2 = 3, M_2 = 3/4')
ok(path_prob((1, 1, 1))[1] == 4 and F(4, 5) == F(path_prob((1, 1, 1))[1], 5), 'M_3 = 4/5 after a third red')
ok(path_prob((1, 1, 0))[1] == 3 and F(3, 5) == F(path_prob((1, 1, 0))[1], 5), 'M_3 = 3/5 after a blue')
ok(path_prob((1, 1, 1))[0] / p == F(3, 4) and path_prob((1, 1, 0))[0] / p == F(1, 4), 'chances 3/4 and 1/4')
ok(F(3, 4) * F(4, 5) == F(12, 20) and F(1, 4) * F(3, 5) == F(3, 20) and F(12, 20) + F(3, 20) == F(3, 4), '12/20 + 3/20 = 3/4')
ok(F(1, 2) == F(1, 1 + 1), 'M_0 = R_0/2 = 1/2')

# seeded simulation of the urn (independent of the enumeration)
random.seed(7)
T, n = 200000, 6; sM = 0.0; sRed = 0
for _ in range(T):
    r = 1
    for i in range(n):
        if random.random() < r / (i + 2): r += 1
    sM += r / (n + 2)
    sRed += random.random() < r / (n + 2)
ok(abs(sM / T - 0.5) < 0.003 and abs(sRed / T - 0.5) < 0.005, 'simulation: E[M_6] and P(draw 7 red) near 1/2')

try:
    import sympy as sp
    R, n_ = sp.symbols('R n', positive=True)
    M = R / (n_ + 2)
    step = (M * (R + 1) + (1 - M) * R) / (n_ + 3)
    ok(sp.simplify(step - M) == 0, 'sympy: E[M_(n+1) | F_n] = M_n')
    ok(sp.simplify((R + M) / (n_ + 3) - M) == 0, 'sympy: (R_n + M_n)/(n+3) = M_n')
    ok(sp.simplify(M * (R + 1) + (1 - M) * R - (R + M)) == 0, 'sympy: E[R_(n+1) | F_n] = R_n + M_n')
except ImportError:
    print('sympy not found: symbolic half skipped')

d = json.load(open(HW)); items = d['items']
it = [i for i in items if i['id'] == 'h-prove-urn']
ok(len(it) == 1, 'one h-prove-urn'); it = it[0]
ok(items.index(it) == 8, 'index 8')
ok(it['performance'] == 'derivation' and it['kind'] == 'longform', 'kind')
ok(sum(r['points'] for r in it['rubric']) == 10 and 3 <= len(it['rubric']) <= 5, 'rubric 10 points in 3 to 5 rows')
# fix pass MP3-1: rows 2 (adapted, integrable) and 3 (the step) are required
ok([k for k, r in enumerate(it['rubric']) if r.get('required')] == [1, 2], 'required rows 2 and 3: the conditions and the step')
ok(not any(x in it for x in ('starter', 'steps', 'order', 'derive', 'hints', 'parts')), 'no scaffold')
ok(sum(1 for i in items if i.get('performance')) == 1 and 6 <= len(items) <= 12 and any(i['difficulty'] == 5 for i in items), 'homework limits')
txt = json.dumps(it, ensure_ascii=False)
ok('—' not in txt and '–' not in txt and '!' not in txt, 'no dashes or exclamation marks')
for s in (r'M_2 = \tfrac34', r'M_3 = \tfrac45', r'\tfrac{12}{20} + \tfrac{3}{20} = \tfrac34', r'E[M_n] = M_0 = \tfrac12', r'R_n + M_n', r'1 \le R_n \le n + 1'):
    ok(s in it['model'], 'stated in model: ' + s)
print(f'{checks} checks, {fails} failures')
sys.exit(1 if fails else 0)
