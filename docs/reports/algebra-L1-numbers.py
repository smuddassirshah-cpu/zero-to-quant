"""Recompute every number stated in algebra level 1 (l1 to l4, review-1, homework-1), each two ways, and check
that it appears in the JSON where it is stated (app/tools/numbers_lib.py). Method 1 is brute force (matrices,
corner permutations, residues by enumeration); method 2 is a formula (counting rule, gcd, Euclid, lcm, cos/sin).
It also runs every code widget of the level in CPython: the solution must pass every test and the starter must
fail at least one. Run: python3 docs/reports/algebra-L1-numbers.py   (exits 0 when every check passes)
"""
import json, math, os, sys, itertools
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level

lv = Level("algebra", 1)
bad = []


def two(name, a, b):
    if a != b and not (isinstance(a, float) and abs(a - b) < 1e-9):
        bad.append(f'{name}: {a} != {b}')
    return a


# ---------- D4 by 2x2 matrices (method 1) and by corner permutations (method 2) ----------
def mm(a, b):
    return tuple(tuple(sum(a[i][k] * b[k][j] for k in range(2)) for j in range(2)) for i in range(2))
r = ((0, -1), (1, 0)); s = ((-1, 0), (0, 1)); I = ((1, 0), (0, 1))
pw = lambda m, k: I if k == 0 else mm(m, pw(m, k - 1))
names = ['e', 'r', 'r²', 'r³', 's', 'rs', 'r²s', 'r³s']
M = dict(zip(names, [I, r, pw(r, 2), pw(r, 3), s, mm(r, s), mm(pw(r, 2), s), mm(pw(r, 3), s)]))
nameof = {v: k for k, v in M.items()}
corner = {1: (1, 1), 2: (-1, 1), 3: (-1, -1), 4: (1, -1)}; cinv = {v: k for k, v in corner.items()}
def perm(m):
    return tuple(cinv[(m[0][0] * x + m[0][1] * y, m[1][0] * x + m[1][1] * y)] for (x, y) in (corner[k] for k in (1, 2, 3, 4)))
P = {n: perm(m) for n, m in M.items()}
pname = {v: k for k, v in P.items()}
comp = lambda p, q: tuple(p[q[i] - 1] for i in range(4))           # p after q
mul1 = lambda a, b: nameof[mm(M[a], M[b])]
mul2 = lambda a, b: pname[comp(P[a], P[b])]
tab = {(a, b): two(f'D4 {a}{b}', mul1(a, b), mul2(a, b)) for a in names for b in names}
det = lambda m: m[0][0] * m[1][1] - m[0][1] * m[1][0]

# all symmetries of the square as rigid corner maps keeping neighbours adjacent (brute force over S4)
adj = lambda p: all(abs(p[i] - p[(i + 1) % 4]) % 2 == 1 for i in range(4))
n_sym = two('|D4|', sum(1 for p in itertools.permutations((1, 2, 3, 4)) if adj(p)), 4 * 2)
lv.expect("l1", "screens[2].widget.lines[3].text", n_sym)
lv.expect("l1", "screens[2].widget.lines[4].text", 12); two('wrong 4x3', 4 * 3, 12)
flips = two('flips', sum(1 for n in names if det(M[n]) == -1), 4)
lv.expect("l1", "screens[1].widget.answer", flips); lv.expect("l1", "screens[1].explain.text", flips)
lv.expect("l1", "screens[1].widget.wrong[0].value", 8); lv.expect("l1", "screens[1].widget.wrong[1].value", 2)
# hook: sr = r^3 s is [[0,1],[1,0]] and fixes corners 1 and 3; rs fixes 2 and 4
two('sr', mul1('s', 'r'), 'r³s'); two('sr matrix', M['r³s'], ((0, 1), (1, 0))); two('rs matrix', M['rs'], ((0, -1), (-1, 0)))
two('sr fixes', [k for k in (1, 2, 3, 4) if P['r³s'][k - 1] == k], [1, 3]); two('rs fixes', [k for k in (1, 2, 3, 4) if P['rs'][k - 1] == k], [2, 4])
lv.expect("l1", "screens[0].explain.text", r"\begin{pmatrix}0&1\\1&0\end{pmatrix}")
lv.expect("l1", "screens[6].explain.text", r"\begin{pmatrix}0&-1\\-1&0\end{pmatrix}")
lv.expect("l1", "screens[0].widget.target", "r3s")
# Cayley cells filled in s3 and every grid in the level
for (a, b), want in [(('r', 'r³'), 'e'), (('s', 's'), 'e'), (('r', 's'), 'rs'), (('s', 'r'), 'r³s')]:
    two(f'{a}.{b}', tab[(a, b)], want)
d = lv._file("l1")[1]
cells = d['screens'][4]['canvas']['params']['cells']
for i, a in enumerate(names):
    for j, b in enumerate(names):
        two(f'grid {a}{b}', cells[i][j], tab[(a, b)])
ecells = sorted(f'r{i + 1}c{j + 1}' for i, a in enumerate(names) for j, b in enumerate(names) if tab[(a, b)] == 'e')
two('e cells', sorted(d['screens'][4]['widget']['answer']), ecells)
two('rs ≠ sr', mul1('r', 's') != mul1('s', 'r'), True)
# triangle: corners and the 120 degree turn; 6 symmetries
c120, s120 = math.cos(2 * math.pi / 3), math.sin(2 * math.pi / 3)
two('tri corner 2', (round(-s120 * 1, 4), round(c120, 4)), (-0.866, -0.5))
lv.expect("l1", "screens[5].prose", 0.866); lv.expect("l1", "screens[5].prose", -0.5)
tri = two('|D3|', sum(1 for p in itertools.permutations((1, 2, 3))), 3 * 2)       # every bijection of a triangle's corners is a symmetry
lv.expect("l1", "screens[5].widget.answer", tri); lv.expect("l1", "screens[5].explain.text", tri)
lv.expect("l1", "screens[5].widget.wrong[0].value", 3); lv.expect("l1", "screens[5].widget.wrong[1].value", 9)
# rectangle 1.5 by 0.8: symmetries are the D4 matrices mapping its corner set to itself
rc = {(1.5, 0.8), (-1.5, 0.8), (-1.5, -0.8), (1.5, -0.8)}
keep = [n for n in names if {(M[n][0][0] * x + M[n][0][1] * y, M[n][1][0] * x + M[n][1][1] * y) for (x, y) in rc} == rc]
two('rect', keep, ['e', 'r²', 's', 'r²s']); two('rect self-inverse', all(tab[(k, k)] == 'e' for k in keep), True)
lv.expect("l1", "screens[7].widget.answer", len(keep)); lv.expect("l1", "screens[7].explain.text", 4)
# payoff mirror S -> 200 - S
pay = {'str': lambda x: abs(x - 100), 'fly': lambda x: max(x - 90, 0) - 2 * max(x - 100, 0) + max(x - 110, 0),
       'call': lambda x: max(x - 100, 0), 'rr': lambda x: max(x - 110, 0) - max(90 - x, 0)}
sym = {k: all(abs(f(x) - f(200 - x)) < 1e-12 for x in range(50, 151)) for k, f in pay.items()}
two('rr mirror is negative', all(abs(pay['rr'](200 - x) + pay['rr'](x)) < 1e-12 for x in range(50, 151)), True)
opts = {o['id']: bool(o.get('correct')) for o in d['screens'][9]['widget']['options']}
two('payoff symmetric set', opts, sym)
# quiz: pentagon 10
pent = two('pentagon', sum(1 for p in itertools.permutations(range(5)) if all((p[(i + 1) % 5] - p[i]) % 5 in (1, 4) for i in range(5))), 5 * 2)
lv.expect("l1", "quiz[1].widget.answer", pent); lv.expect("l1", "quiz[1].widget.wrong[1].value", 20)

# ---------- l2 ----------
lv.expect("l2", "screens[0].widget.answer", two('5-(3-1)', 5 - (3 - 1), 3)); lv.expect("l2", "screens[0].question", (5 - 3) - 1)
lv.expect("l2", "screens[3].canvas", two('det', 1 * 4 - 2 * 2, 0))
inv5 = {a: next(b for b in range(1, 5) if a * b % 5 == 1) for a in range(1, 5)}
two('inv5', inv5, {a: pow(a, 3, 5) for a in range(1, 5)})
lv.expect("l2", "screens[4].explain.text", "1, 3, 2, 4")
comb = two('10% then -10%', round(1.10 * 0.90 - 1, 10), round(math.exp(math.log(1.1) + math.log(0.9)) - 1, 10))
lv.expect("l2", "screens[9].widget.answer", comb); lv.expect("l2", "screens[9].canvas", 0.99)
inv = two('undo -20%', round(-(-0.2) / (1 - 0.2), 10), round(1 / 0.8 - 1, 10))
lv.expect("l2", "screens[10].widget.answer", inv); lv.expect("l2", "screens[10].widget.wrong[0].value", 0.2)
lv.expect("l2", "screens[10].feedback.byKey.same", round(0.8 * 1.2, 10)); lv.expect("l2", "screens[10].feedback.byKey.same", 4)
two('(rs)^-1', next(x for x in names if tab[('rs', x)] == 'e'), 'rs'); two('s r^3', tab[('s', 'r³')], 'rs')
two('r^-1 s^-1', tab[('r³', 's')], 'r³s'); two('rs then r3s', tab[('r³s', 'rs')], 'r²')

# ---------- l3 ----------
lv.expect("l3", "screens[0].widget.answer", two('7+9 mod 12', (7 + 9) % 12, 16 - 12))
L3 = lv._file("l3")[1]
units10 = two('units 10', [a for a in range(10) if any(a * b % 10 == 1 for b in range(10))], [a for a in range(10) if math.gcd(a, 10) == 1])
two('ones', sorted(L3['screens'][1]['widget']['answer']), sorted(f'r{a + 1}c{b + 1}' for a in range(10) for b in range(10) if a * b % 10 == 1))
lv.expect("l3", "screens[2].widget.answer", two('phi10', len(units10), sum(1 for a in range(1, 11) if math.gcd(a, 10) == 1)))
two('2x=4', [x for x in range(10) if 2 * x % 10 == 4], [2, 7]); two('3x=4', [x for x in range(10) if 3 * x % 10 == 4], [8])
lv.expect("l3", "screens[3].widget.rows[0][1].answer", 2); lv.expect("l3", "screens[3].widget.rows[1][1].answer", 7); lv.expect("l3", "screens[3].widget.rows[2][1].answer", 8)
two('bezout 3,10', 3 * 7 + 10 * (-2), 1)
rems = []; a_, b_ = 26, 7
while b_:
    rems.append(a_ % b_); a_, b_ = b_, a_ % b_
two('euclid 26 7', rems[:3], [5, 2, 1]); two('back-sub', 3 * 26 - 11 * 7, 1)
for k, v in enumerate([5, 2, 1, 11]):
    lv.expect("l3", f"screens[7].widget.rows[{k}][1].answer", v)
inv7 = two('7^-1 mod 26', next(x for x in range(26) if 7 * x % 26 == 1), (-11) % 26)
lv.expect("l3", "screens[8].widget.answer", inv7); lv.expect("l3", "screens[8].explain.text", 105)
lv.expect("l3", "screens[8].widget.wrong[0].value", two('7^24 mod 26', pow(7, 24, 26), 1))
two('7*11 mod 26', 7 * 11 % 26, 25)
for k, u in enumerate([1, 5, 7, 11]):
    lv.expect("l3", f"screens[9].widget.rows[{k}][1].answer", two(f'{u}^2 mod 12', u * u % 12, 1))
two('units 12', [a for a in range(12) if math.gcd(a, 12) == 1], [1, 5, 7, 11])
day = two('90 mod 7', 90 % 7, 90 - 12 * 7)
wk = ['Fri', 'Sat', 'Sun', 'Mon', 'Tue', 'Wed', 'Thu']
two('weekday', wk[day], 'Thu'); lv.expect("l3", "screens[10].explain.text", day); lv.expect("l3", "quiz[0].widget.answer", day)
lv.expect("l3", "quiz[3].widget.answer", two('phi12', sum(1 for a in range(12) if math.gcd(a, 12) == 1), 12 * (1 - 1 / 2) * (1 - 1 / 3)))
two('17^-1 mod 3120', next(x for x in range(3120) if 17 * x % 3120 == 1), pow(17, -1, 3120))

# ---------- l4 ----------
def walk(n, g):
    seen, x = {0}, g % n
    while x != 0:
        seen.add(x); x = (x + g) % n
    return len(seen)
lv.expect("l4", "screens[0].widget.answer", two('Z6 step 2', walk(6, 2), 6 // math.gcd(2, 6)))
img4 = two('z^4 images', len({round(math.cos(2 * math.pi * 4 * j / 12), 9) + 1j * round(math.sin(2 * math.pi * 4 * j / 12), 9) for j in range(12)}), 12 // math.gcd(4, 12))
lv.expect("l4", "screens[1].widget.answer", img4)
two('z^5 images', len({(5 * j) % 12 for j in range(12)}), 12 // math.gcd(5, 12))
for k, (g, want) in enumerate([(8, 3), (9, 4), (6, 2)]):
    lv.expect("l4", f"screens[3].widget.rows[{k}][1].answer", two(f'ord {g}', walk(12, g), 12 // math.gcd(g, 12)))
L4 = lv._file("l4")[1]
gens = two('gens Z12', [g for g in range(12) if walk(12, g) == 12], [g for g in range(12) if math.gcd(g, 12) == 1])
two('gens multi', sorted(int(o['text']) for o in L4['screens'][4]['widget']['options'] if o.get('correct')), gens)
z = complex(math.cos(math.pi / 3), math.sin(math.pi / 3))
two('zeta', (round(z.real, 4), round(z.imag, 4)), (0.5, round(math.sqrt(3) / 2, 4)))
two('zeta^3', round((z ** 3).real, 9), -1.0)
o_z2 = two('ord zeta^2', next(k for k in range(1, 7) if abs(z ** (2 * k) - 1) < 1e-9), 6 // math.gcd(2, 6))
lv.expect("l4", "quiz[3].widget.answer", o_z2)
mord = lambda a, n: next(k for k in range(1, n) if pow(a, k, n) == 1)
for k, (a, n, want) in enumerate([(3, 8, 2), (5, 8, 2), (7, 8, 2), (2, 7, 3), (3, 7, 6)]):
    lv.expect("l4", f"screens[6].widget.rows[{k}][1].answer", two(f'ord {a} mod {n}', mord(a, n), want))
lv.expect("l4", "screens[7].widget.answer", two('ord 8 trap', walk(12, 8), 3)); lv.expect("l4", "screens[7].widget.wrong[0].value", 12 / 8)
lv.expect("l4", "screens[8].widget.answer", two('quarterly', walk(12, 3), 12 // math.gcd(3, 12)))
lcm = two('lcm', math.lcm(8, 12), next(d for d in range(1, 97) if d % 8 == 0 and d % 12 == 0))
lv.expect("l4", "screens[9].widget.answer", lcm); lv.expect("l4", "screens[9].widget.wrong[0].value", 96); lv.expect("l4", "screens[9].widget.wrong[1].value", math.gcd(8, 12))
two('step 5 months', walk(12, 5), 12)

# ---------- review-1 ----------
two('picture r2s', M['r²s'], ((1, 0), (0, -1)))
two('max inverses', [a for a in range(3) if any(max(a, b) == 0 for b in range(3))], [0])
two('(r r2s)^-1', next(x for x in names if tab[(tab[('r', 'r²s')], x)] == 'e'), tab[('r²s', 'r³')]); two('r3 r2s', tab[('r³', 'r²s')], 'rs')
two('unit mod 15', [a for a in (8, 5, 6, 10) if math.gcd(a, 15) == 1], [8])
i740 = two('7^-1 mod 40', next(x for x in range(40) if 7 * x % 40 == 1), (-17) % 40)
lv.expect("review", "items[4].widget.answer", i740); two('3*40-17*7', 3 * 40 - 17 * 7, 1)
lv.expect("review", "items[4].widget.wrong[1].value", pow(7, 38, 40)); two('7*9 mod 40', 7 * 9 % 40, 23)
lv.expect("review", "items[5].widget.answer", two('ord 18 in Z30', walk(30, 18), 30 // math.gcd(18, 30)))
lv.expect("review", "items[5].widget.wrong[0].value", round(30 / 18, 4))
two('Z9 units', [a for a in range(9) if math.gcd(a, 9) == 1], [1, 2, 4, 5, 7, 8])
two('ord 2 mod 9', mord(2, 9), 6); two('ord 4,7,8 mod 9', [mord(a, 9) for a in (4, 7, 8)], [3, 3, 2])
lv.expect("review", "items[7].widget.answer", two('hexagon', 6 * 2, sum(1 for p in itertools.permutations(range(6)) if all((p[(i + 1) % 6] - p[i]) % 6 in (1, 5) for i in range(6)))))

# ---------- homework-1 ----------
two('Z8 squares', [u * u % 8 for u in (1, 3, 5, 7)], [1, 1, 1, 1]); two('D4 r^2 != e', tab[('r', 'r')] != 'e', True)
lv.expect("homework", "items[4].explain.text", "c, e, a, b")
lv.expect("homework", "items[5].widget.answer", two('ord 2 mod 11', mord(2, 11), 10)); two('2^5 mod 11', pow(2, 5, 11), 10)
lv.expect("homework", "items[6].widget.answer", two('identity', next(e for e in range(-5, 5) if all(a + e + 1 == a for a in range(-3, 4))), -1))
sols = [x for x in range(15) if 6 * x % 15 == 9]
lv.expect("homework", "items[7].widget.answer", two('6x=9 mod 15', len(sols), math.gcd(6, 15))); two('sols', sols, [4, 9, 14])
def cyc_units(n):
    U = [a for a in range(1, n) if math.gcd(a, n) == 1]
    return any(mord(g, n) == len(U) for g in U) if n > 2 else True
theory = lambda n: n in (1, 2, 4) or any((n % p == 0 or n % (2 * p) == 0) and all(q == p for q in pf(n // (2 if n % 2 == 0 and p != 2 else 1))) for p in pf(n) if p > 2)
def pf(n):
    out, p = [], 2
    while n > 1:
        while n % p == 0:
            out.append(p); n //= p
        p += 1
    return out
for n, v in [(2, True), (7, True), (9, True), (10, True), (18, True), (25, True), (27, True), (8, False), (12, False), (15, False), (20, False)]:
    two(f'cyclic units {n}', cyc_units(n), v); two(f'theory {n}', theory(n), v)

# ---------- code widgets ----------
def widgets(o):
    if isinstance(o, dict):
        if o.get('kind') == 'code':
            yield o
        for v in o.values():
            yield from widgets(v)
    elif isinstance(o, list):
        for v in o:
            yield from widgets(v)
def run(src, w, t):
    ns = {}
    try:
        exec(w.get('prelude', ''), ns); exec(src, ns)
        if t.get('compare') == 'raises':
            try:
                eval(t['call'], ns); return False
            except Exception as ex:
                return type(ex).__name__ == t['expect']
        return eval(t['call'], ns) == eval(t['expect'], ns)
    except Exception:
        return False
for ref in ["l1", "l2", "l3", "l4", "review", "homework"]:
    for w in widgets(lv._file(ref)[1]):
        sol = [run(w['solution'], w, t) for t in w['tests'] + w.get('examples', [])]
        st = [run(w['starter'], w, t) for t in w['tests']]
        two(f'{ref} code solution', all(sol), True); two(f'{ref} code starter fails one', not all(st), True)

lv.check_wrongs()
if bad:
    print('two-way mismatches:', *bad, sep='\n  ')
    lv._rec(False, 'two-way checks', '; '.join(bad))
lv.report()
