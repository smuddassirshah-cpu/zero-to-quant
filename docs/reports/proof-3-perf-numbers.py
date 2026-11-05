"""Recompute every number in the proof level 3 performance task (h-prove-cube-minus-n).
Run from the repo root: python3 docs/reports/proof-3-perf-numbers.py  (exits 0 when all checks pass)
Each identity is checked two ways: polynomial coefficients expanded by hand-rolled
multiplication, and evaluation at many integer points. The claim is brute-forced.
"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
HW = os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'proof', 'homework-3.json')
fails = []
def check(ok, msg):
    if not ok:
        fails.append(msg)

# 1. The statement, by brute force over a range (and beyond the claim, to negatives).
check(all((n**3 - n) % 3 == 0 for n in range(1, 100001)), 'claim fails for some 1 <= n <= 100000')
check(all((n**3 - n) % 3 == 0 for n in range(-1000, 1)), 'claim fails for some -1000 <= n <= 0')
# Second way: n^3 - n = (n-1) n (n+1), and one of three consecutive numbers is a multiple of 3.
check(all((n - 1) * n * (n + 1) == n**3 - n for n in range(-500, 501)), 'factorisation wrong')
check(all(any(x % 3 == 0 for x in (n - 1, n, n + 1)) for n in range(-500, 501)), 'consecutive triple lacks a multiple of 3')

# Polynomials as coefficient lists, lowest power first.
def mul(p, q):
    r = [0] * (len(p) + len(q) - 1)
    for i, a in enumerate(p):
        for j, b in enumerate(q):
            r[i + j] += a * b
    return r
def add(p, q):
    n = max(len(p), len(q))
    return [(p[i] if i < len(p) else 0) + (q[i] if i < len(q) else 0) for i in range(n)]
def scale(c, p):
    return [c * a for a in p]
def trim(p):
    while len(p) > 1 and p[-1] == 0:
        p = p[:-1]
    return p
def cube(p):
    return mul(mul(p, p), p)
def ev(p, x):
    return sum(a * x**i for i, a in enumerate(p))

# 2. The three cases (n = 3m + r), each stated cube, each n^3 - n, each bracket.
cases = {
    0: dict(cube=[0, 0, 0, 27], diff=[0, -3, 0, 27], bracket=[0, -1, 0, 9]),
    1: dict(cube=[1, 9, 27, 27], diff=[0, 6, 27, 27], bracket=[0, 2, 9, 9]),
    2: dict(cube=[8, 36, 54, 27], diff=[6, 33, 54, 27], bracket=[2, 11, 18, 9]),
}
for r, c in cases.items():
    n = [r, 3]                      # n = 3m + r
    cu = trim(cube(n))
    df = trim(add(cu, scale(-1, n)))
    check(cu == c['cube'], f'case {r}: cube coefficients {cu}')
    check(df == c['diff'], f'case {r}: n^3 - n coefficients {df}')
    check(trim(scale(3, c['bracket'])) == df, f'case {r}: 3 * bracket != n^3 - n')
    for m in range(0, 2001):        # second way: evaluate
        nv = 3 * m + r
        check(nv**3 == ev(c['cube'], m), f'case {r}, m={m}: cube value')
        check(nv**3 - nv == 3 * ev(c['bracket'], m), f'case {r}, m={m}: bracket value')

# 3. The induction step: (k+1)^3 - (k+1) = k^3 + 3k^2 + 3k + 1 - k - 1 = (k^3 - k) + 3(k^2 + k).
k1 = [1, 1]
lhs = trim(add(cube(k1), scale(-1, k1)))
check(lhs == [0, 2, 3, 1], f'induction lhs coefficients {lhs}')
rhs = trim(add([0, -1, 0, 1], scale(3, [0, 1, 1])))
check(lhs == rhs, 'induction regrouping wrong')
for k in range(1, 5001):
    a = (k**3 - k) // 3
    check((k + 1)**3 - (k + 1) == k**3 + 3 * k**2 + 3 * k + 1 - k - 1, f'k={k}: expansion')
    check((k + 1)**3 - (k + 1) == 3 * (a + k**2 + k), f'k={k}: 3(a + k^2 + k)')

# 4. Checks quoted in the model.
check(1**3 - 1 == 0 == 3 * 0, 'n = 1 base case')
check(2**3 - 2 == 8 - 2 == 6 == 3 * 2, 'n = 2 gives 6 = 3 x 2')
check(3**3 - 3 == 27 - 3 == 24 == 3 * 8, 'n = 3 gives 24 = 3 x 8')

# 5. The file states what was checked, and the rubric is well formed.
d = json.load(open(HW))
item = next(i for i in d['items'] if i['id'] == 'h-prove-cube-minus-n')
m = item['model']
for s in ['27m^3 - 3m = 3(9m^3 - m)',
          '27m^3 + 27m^2 + 9m + 1', '$n^3 - n = 27m^3 + 27m^2 + 6m$, which is $3(9m^3 + 9m^2 + 2m)$',
          '27m^3 + 54m^2 + 36m + 8', '$n^3 - n = 27m^3 + 54m^2 + 33m + 6$, which is $3(9m^3 + 18m^2 + 11m + 2)$',
          '1^3 - 1 = 0 = 3 \\times 0', '8 - 2 = 6 = 3 \\times 2', '27 - 3 = 24 = 3 \\times 8',
          'k^3 + 3k^2 + 3k + 1 - k - 1', '3a + 3(k^2 + k)', '3(a + k^2 + k)', '(n - 1)n(n + 1)']:
    check(s in m, f'model does not state: {s}')
check(item['performance'] == 'derivation' and item['kind'] == 'longform', 'kind')
check(len(item['rubric']) >= 3, 'rubric under 3 criteria')
check(sum(r['points'] for r in item['rubric']) == 10, 'rubric does not sum to 10')
check(sum(r['points'] for r in item['rubric']) == 2 + 3 + 3 + 2, 'rubric points 2, 3, 3, 2')
check(not any(k in item for k in ('starter', 'steps', 'order', 'derive', 'hints', 'parts')), 'scaffold field present')
check(len(d['items']) <= 12, 'homework over 12 items')
check(sum(1 for i in d['items'] if 'performance' in i) == 1, 'more than one performance item')

# 6. The edited exit-longform remark: n^2 - n + 11 for n = 0..10 and the failure at 11.
def is_prime(x):
    return x >= 2 and all(x % p for p in range(2, int(x**0.5) + 1))
vals = [n * n - n + 11 for n in range(11)]
check(vals == [11, 11, 13, 17, 23, 31, 41, 53, 67, 83, 101], f'n^2 - n + 11 values {vals}')
check(all(is_prime(v) for v in vals), 'a value for n = 0..10 is not prime')
check(11 * 11 - 11 + 11 == 121 == 11 * 11 and not is_prime(121), 'n = 11 gives 121')

if fails:
    print('FAIL', len(fails))
    for f in fails[:20]:
        print(' -', f)
    sys.exit(1)
print('proof-3-perf numbers: all checks passed')
