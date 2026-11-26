"""Fix-pass read of commit 4e6ca54e (counting l3, l9, l10, l11, l12). Exits 0 when every check holds."""
import itertools, json, math, os, random, sys
from fractions import Fraction as F

R = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'content', 'courses', 'counting')
J = lambda f: json.load(open(os.path.join(R, f)))
bad = []


def ck(name, cond, info=''):
    print(('ok   ' if cond else 'FAIL ') + name, info)
    if not cond:
        bad.append(name)


# --- l3 screens[9]: PIN count and slips, by brute force and by formula
D = '0123456789'
allp = [''.join(p) for p in itertools.product(D, repeat=4)]
distinct = [p for p in allp if len(set(p)) == 4]
slips = {
    'key': (len(distinct), 10 * 9 * 8 * 7),
    'repeats': (len(allp), 10 ** 4),
    'groups': (len({frozenset(p) for p in distinct}), math.comb(10, 4)),
    'added': (sum([10, 9, 8, 7]), 34),
    'no-zero': (len([p for p in distinct if '0' not in p]), 9 * 8 * 7 * 6),
    'no-zero-first': (len([p for p in distinct if p[0] != '0']), 9 * 9 * 8 * 7),
}
s9 = J('l3-choosing-in-order.json')['screens'][9]
w = s9['widget']
ck('l3 key 5040', slips['key'] == (5040, 5040) and w['answer'] == 5040 and '0193' in distinct and '1123' not in distinct)
vals = {x['id']: x for x in w['wrong']}
for k in ('repeats', 'groups', 'added', 'no-zero', 'no-zero-first'):
    a, b = slips[k]
    ck('l3 slip ' + k, a == b == vals[k]['value'], (a, b, vals[k]['value']))
bands = [(w['answer'], w['tol']['abs'])] + [(x['value'], x['tol']['abs']) for x in w['wrong']]
ck('l3 bands disjoint', all(abs(p[0] - q[0]) > p[1] + q[1] for p, q in itertools.combinations(bands, 2)))
ck('l3 no-zero-first second route', 5040 - 9 * 8 * 7 == 4536)  # all allowed PINs minus those starting with 0
ck('l3 every slip has a line', set(s9['feedback']['byKey']) == set(vals))

# --- l11 summary.ideas[1]: atan(u2/u1) against atan2; angle anticlockwise from +x, compared mod 360
res = {}
for x in range(-6, 7):
    for y in range(-6, 7):
        if (x, y) == (0, 0):
            continue
        if x == 0:
            res.setdefault('y-axis', set()).add('undefined')
            continue
        t = math.degrees(math.atan2(y, x)) % 360
        c = math.degrees(math.atan(y / x))
        diff = round((t - c) % 360, 9) % 360
        if y == 0:
            q = '+x-axis' if x > 0 else '-x-axis'
        else:
            q = 'Q1' if x > 0 and y > 0 else 'Q2' if x < 0 and y > 0 else 'Q3' if x < 0 else 'Q4'
        res.setdefault(q, set()).add(diff)
print('   atan minus atan2 by region (degrees, mod 360):', {k: sorted(v, key=str) for k, v in sorted(res.items())})
ck('l11 Q1 exact', res['Q1'] == {0.0})
ck('l11 Q2, Q3 and the negative x-axis are 180 out', res['Q2'] == res['Q3'] == res['-x-axis'] == {180.0})
ck('l11 Q4 and positive x-axis give the same direction', res['Q4'] == {0.0} and res['+x-axis'] == {0.0})
ck('l11 never out by anything but 0 or 180', all(v <= {0.0, 180.0} for k, v in res.items() if k != 'y-axis'))


# --- swap lines, and which options are truly parallel
def par(a, b):
    return a[0] * b[1] - a[1] * b[0] == 0 and any(a) and any(b)


def swap_sizes_keep_signs(v):
    sg = lambda t: -1 if t < 0 else 1
    return (sg(v[0]) * abs(v[1]), sg(v[1]) * abs(v[0]))


cases = [
    ('l10 screens[4] d', (2, -1), (1, -2), {'a': (4, -2), 'b': (-6, 3), 'c': (1, F(-1, 2)), 'd': (1, -2), 'e': (2, 1)}, {'a', 'b', 'c'}),
    ('l10 quiz[2] b', (6, -4), (4, -6), {'a': (-3, 2), 'b': (4, -6), 'c': (6, 4), 'd': (3, -1)}, {'a'}),
    ('l12 quiz[2] c', (4 - 1, 2 - 4), (2, -3), {'a': (-6, 4), 'b': (3, 2), 'c': (2, -3), 'd': (4, 2)}, {'a'}),
]
for name, base, opt, opts, keyed in cases:
    ck(name + ' sizes swapped, signs kept', swap_sizes_keep_signs(base) == opt, (base, opt))
    ck(name + ' differs from the plain component swap', (base[1], base[0]) != opt, (base[1], base[0]))
    ck(name + ' not parallel', not par(base, opt))
    ck(name + ' parallel set equals key', {k for k, v in opts.items() if par(base, v)} == keyed)

l10 = J('l10-adding-arrows.json')
l12 = J('l12-proving-with-vectors.json')
l9 = J('l9-arrows.json')
for nm, wd, keyed in [('l10 s4', l10['screens'][4]['widget'], {'a', 'b', 'c'}), ('l10 q2', l10['quiz'][2]['widget'], {'a'}),
                      ('l12 q2', l12['quiz'][2]['widget'], {'a'}), ('l9 q3', l9['quiz'][3]['widget'], {'a'})]:
    ck(nm + ' keyed ids in content', {o['id'] for o in wd['options'] if o.get('correct')} == keyed)

# --- l9 quiz[3]: parallelogram ABCD in order; only DC equals AB. The diagonal AC can be shorter than AB.
random.seed(1)
shorter = n = 0
okp = True
for _ in range(20000):
    A = (random.randint(-9, 9), random.randint(-9, 9))
    p = (random.randint(-9, 9), random.randint(-9, 9))
    q = (random.randint(-9, 9), random.randint(-9, 9))
    if p[0] * q[1] - p[1] * q[0] == 0:
        continue
    n += 1
    B = (A[0] + p[0], A[1] + p[1])
    C = (B[0] + q[0], B[1] + q[1])
    Dp = (A[0] + q[0], A[1] + q[1])
    v = lambda P, Q: (Q[0] - P[0], Q[1] - P[1])
    AB = v(A, B)
    eq = (v(Dp, C) == AB, v(C, Dp) == AB, v(B, C) == AB, v(A, C) == AB)
    if eq != (True, False, False, False):
        okp = False
    if math.hypot(*v(A, C)) < math.hypot(*AB):
        shorter += 1
ck('l9 only DC equals AB', okp, n)
ck('l9 diagonal AC can be shorter than AB', shorter > 0, shorter)

print('FAILED: ' + ', '.join(bad) if bad else 'all checks pass')
sys.exit(1 if bad else 0)
