"""Recompute every number stated in algebra level 2 (l5 to l9, review-2, homework-2), each two ways, and check that it
appears in the JSON where it is stated (app/tools/numbers_lib.py). Method 1 is brute force (closures of generators,
coset enumeration, cycle walks, inversion counts, breadth-first search); method 2 is a formula or theorem (divisors,
Lagrange, lcm, (-1)^(n-c), n!/2, harmonic sums). It also runs every code widget of the level in CPython: the solution
must pass every test and the starter must fail at least one. Run: python3 docs/reports/algebra-L2-numbers.py (exit 0).
"""
import itertools, math, os, sys, random
from collections import deque
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level

lv = Level("algebra", 2)
bad = []
def two(name, a, b):
    if a != b and not (isinstance(a, float) and abs(a - b) < 1e-9):
        bad.append(f'{name}: {a} != {b}')
    return a

comp = lambda p, q: tuple(p[q[i]] for i in range(len(q)))
def closure(gens, n):
    e = tuple(range(n)); S = {e}; fr = [e]
    while fr:
        x = fr.pop()
        for g in gens:
            y = comp(g, x)
            if y not in S:
                S.add(y); fr.append(y)
    return frozenset(S)
inv_count = lambda p: sum(1 for i in range(len(p)) for j in range(i + 1, len(p)) if p[i] > p[j])
def cyc(p):
    seen, out = set(), []
    for s in range(len(p)):
        if s not in seen:
            c, k = [], s
            while k not in seen:
                seen.add(k); c.append(k); k = p[k]
            out.append(c)
    return out
sign_c = lambda p: (-1) ** (len(p) - len(cyc(p)))
sign_i = lambda p: (-1) ** inv_count(p)
order_p = lambda p: math.lcm(*[len(c) for c in cyc(p)])
def order_b(p):
    e, x, k = tuple(range(len(p))), tuple(p), 1
    while x != e:
        x = comp(p, x); k += 1
    return k

# ---------- D4 (corner perms, 0-based) ----------
E4, R, S = (0, 1, 2, 3), (1, 2, 3, 0), (1, 0, 3, 2)
D4 = closure([R, S], 4)
pw = lambda g, k: E4 if k == 0 else comp(g, pw(g, k - 1))
name = {E4: 'e', R: 'r', pw(R, 2): 'r²', pw(R, 3): 'r³', S: 's', comp(R, S): 'rs', comp(pw(R, 2), S): 'r²s', comp(pw(R, 3), S): 'r³s'}
el = {v: k for k, v in name.items()}
mul = lambda a, b: name[comp(el[a], el[b])]
names = ['e', 'r', 'r²', 'r³', 's', 'rs', 'r²s', 'r³s']
subs = {closure(g, 4) for k in (1, 2) for g in itertools.combinations(D4, k)}
hasse = lambda L: sum(1 for a in L for b in L if a < b and not any(a < c < b for c in L))
n_d4 = two('D4 subgroups', len(subs), 1 + 5 + 3 + 1); lv.expect("l5", "screens[7].prose", n_d4)
n2 = two('D4 size 2', sum(1 for H in subs if len(H) == 2), sum(1 for g in D4 if g != E4 and comp(g, g) == E4))
lv.expect("l5", "screens[7].widget.answer", n2); lv.expect("l5", "screens[7].explain.text", n2)
lv.expect("l5", "screens[7].explain.text", two('D4 hasse', hasse(list(subs)), 15))
two('D4 sizes', sorted(len(H) for H in subs), [1, 2, 2, 2, 2, 2, 4, 4, 4, 8])
two('D4 lattice nodes', len(lv._file("l5")[1]['screens'][7]['canvas']['params']['nodes']), n_d4)
two('D4 lattice edges', len(lv._file("l5")[1]['screens'][7]['canvas']['params']['edges']), 15)
z12 = {frozenset((g * k) % 12 for k in range(12)) for g in range(12)}
lv.expect("l5", "screens[6].widget.answer", two('Z12 subgroups', len(z12), sum(1 for d in range(1, 13) if 12 % d == 0)))
lv.expect("l5", "screens[6].explain.text", two('Z12 hasse', hasse(list(z12)), 7)); lv.expect("l5", "screens[6].widget.wrong[1].value", 7)
two('rot e cells', sorted(f'r{i + 1}c{j + 1}' for i in range(4) for j in range(4) if mul(names[i], names[j]) == 'e'), sorted(lv._file("l5")[1]['screens'][0]['widget']['answer']))
two('r.s escapes', mul('r', 's') in ('e', 'r', 's'), False)
lv.expect("l5", "screens[9].widget.answer", two('2+3', 2 + 3, next(k for k in range(1, 20) if k % 2 and k % 3 and k > 3)))
two('2Z cap 3Z', [k for k in range(1, 20) if k % 2 == 0 and k % 3 == 0][0], math.lcm(2, 3))
g = two('gcd 100 250', math.gcd(100, 250), min(abs(a * 100 + b * 250) for a in range(-5, 6) for b in range(-5, 6) if a * 100 + b * 250 != 0))
lv.expect("l5", "screens[10].widget.answer", g); two('3x100-250', 3 * 100 - 250, g); lv.expect("l5", "screens[10].explain.text", 50)
def gen12(gs):
    H = {0} | set(gs); fr = list(H)
    while fr:
        x = fr.pop()
        for y in gs:
            z = (x + y) % 12
            if z not in H:
                H.add(z); fr.append(z)
    return sorted(H)
two('<8>', gen12([8]), [0, 4, 8]); two('<4,6>', gen12([4, 6]), list(range(0, 12, math.gcd(4, 6))))
two('<9,6>', gen12([9, 6]), list(range(0, 12, math.gcd(9, 6)))); two('<5>', gen12([5]), list(range(12)))
two('<r>', len(closure([R], 4)), 4); two('<r,s>', len(closure([R, S], 4)), 8)

# ---------- l6 ----------
L6 = lv._file("l6")[1]
two('1+3Z', sorted(L6['screens'][0]['widget']['answer']), sorted(f'p{k + 6}' for k in range(-6, 7) if k % 3 == 1))
cos4 = sorted({tuple(sorted((a + h) % 12 for h in (0, 4, 8))) for a in range(12)})
two('cosets <4>', cos4, [tuple(range(k, 12, 4)) for k in range(4)])
for i, k in enumerate((1, 2, 3)):
    for j in range(3):
        lv.expect("l6", f"screens[1].widget.rows[{i + 1}][{j + 1}].answer", cos4[k][j])
part = [mul(gg, 's') for gg in ('r', 'r²', 'r³')]; two('gs partners', part, ['rs', 'r²s', 'r³s'])
for i, want in enumerate(part):
    two(f'l6 partner {i}', L6['screens'][2]['widget']['rows'][i + 1][2]['answer'], want)
two('r^-1 rs', mul('r³', 'rs'), 's'); two('Hr', sorted({mul(h, 'r') for h in ('e', 's')}), sorted(['r', 'r³s']))
two('rH', sorted({mul('r', h) for h in ('e', 's')}), sorted(['r', 'rs']))
two('1+5 escapes', (1 + 5) % 12 in (1, 5, 9), False)
lv.expect("l6", "screens[8].widget.answer", two('cosets <6>', len({tuple(sorted(((a + 0) % 12, (a + 6) % 12))) for a in range(12)}), 12 // 2))
lv.expect("l6", "screens[9].widget.answer", two('weekday class', sum(1 for d in range(250) if d % 5 == 0), 250 // 5))
lv.expect("l6", "quiz[2].widget.answer", two('cosets of {e} in D4', len({frozenset([x]) for x in D4}), len(D4)))

# ---------- l7 ----------
two('D4 has no subgroup of 3', any(len(H) == 3 for H in subs), False); two('r.r', mul('r', 'r'), 'r²'); two('s.r2', mul('s', 'r²'), 'r²s')
div12 = two('divisors 12', [d for d in range(1, 13) if 12 % d == 0], [1, 2, 3, 4, 6, 12])
L7 = lv._file("l7")[1]
two('multi 12', sorted(int(o['text']) for o in L7['screens'][5]['widget']['options'] if o.get('correct')), div12)
mord = lambda a, n: next(k for k in range(1, n + 1) if pow(a, k, n) == 1)
for i, (a, want) in enumerate([(2, 12), (3, 3), (5, 4), (12, 2)]):
    lv.expect("l7", f"screens[6].widget.rows[{i}][1].answer", two(f'ord {a} mod 13', mord(a, 13), want))
    two(f'ord {a} | 12', 12 % mord(a, 13), 0)
A4 = [p for p in itertools.permutations(range(4)) if sign_i(p) == 1]
two('|A4|', len(A4), math.factorial(4) // 2)
e4 = tuple(range(4))
has6 = any(all(comp(a, b) in H for a in H for b in H) for H in (set(c) | {e4} for c in itertools.combinations([p for p in A4 if p != e4], 5)))
two('A4 no order 6', has6, False); two('A4 orders', sorted({len(closure(gg, 4)) for k in (1, 2) for gg in itertools.combinations(A4, k)}), [1, 2, 3, 4, 12])
lv.expect("l7", "screens[9].widget.answer", two('Lehmer a=3', mord(3, 13), len({pow(3, k, 13) for k in range(12)})))
two('Lehmer a=2', mord(2, 13), 12)
p = 2 ** 31 - 1
two('p prime', all(p % d for d in range(2, math.isqrt(p) + 1)), True)
def pf(n):
    out, d = [], 2
    while d * d <= n:
        while n % d == 0:
            out.append(d); n //= d
        d += 1
    return out + ([n] if n > 1 else [])
two('p-1 factors', pf(p - 1), [2, 3, 3, 7, 11, 31, 151, 331]); two('16807', 7 ** 5, 16807)
two('ord 16807', all(pow(16807, (p - 1) // q, p) != 1 for q in set(pf(p - 1))) and pow(16807, p - 1, p) == 1, True)
lv.expect("l7", "screens[10].prose", p); lv.expect("l7", "screens[10].prose", p - 1); lv.expect("l7", "screens[10].prose", 16807)
two('seven checks', len(set(pf(p - 1))), 7)
lv.expect("l7", "quiz[0].widget.answer", two('index 24/6', 24 // 6, 4))

# ---------- l8 ----------
sig1 = {1: 5, 2: 3, 3: 8, 4: 1, 5: 4, 6: 7, 7: 6, 8: 2}
sig = tuple(sig1[k] - 1 for k in range(1, 9))
two('sigma cycles', [[x + 1 for x in c] for c in cyc(sig) if len(c) > 1], [[1, 5, 4], [2, 3, 8], [6, 7]])
lv.expect("l8", "screens[5].widget.answer", two('ord sigma', order_p(sig), order_b(sig))); lv.expect("l8", "screens[5].widget.wrong[0].value", 18)
two('|S8|', len(list(itertools.permutations(range(8)))), math.factorial(8)); lv.expect("l8", "screens[1].explain.text", 40320)
t12, t23 = (1, 0, 2), (0, 2, 1)
for i, pq in enumerate([comp(t12, t23), comp(t23, t12)]):
    for j in range(3):
        lv.expect("l8", f"screens[2].widget.rows[{i}][{j + 1}].answer", pq[j] + 1)
two('(12)(23)', comp(t12, t23), (1, 2, 0)); two('(23)(12)', comp(t23, t12), (2, 0, 1))
two('disjoint commute', comp((1, 0, 3, 2), (0, 1, 3, 2)) == comp((0, 1, 3, 2), (1, 0, 3, 2)), True)
lv.expect("l8", "screens[6].widget.rows[0][1].answer", two('(12)(345)', order_p((1, 0, 3, 4, 2)), order_b((1, 0, 3, 4, 2))))
lv.expect("l8", "screens[6].widget.rows[1][1].answer", two('(123)(45678)', order_p((1, 2, 0, 4, 5, 6, 7, 3)), order_b((1, 2, 0, 4, 5, 6, 7, 3))))
m7 = two('max S7', max(order_p(q) for q in itertools.permutations(range(7))), max(math.lcm(*pt) for pt in [[3, 4], [2, 5], [7], [1, 6], [2, 2, 3], [1, 2, 4], [1, 1, 5], [1, 3, 3]]))
lv.expect("l8", "screens[7].widget.answer", m7)
lv.expect("l8", "screens[7].explain.text", two('max S8', max(math.lcm(*pt) for pt in [[3, 5], [8], [1, 7], [2, 6], [1, 3, 4], [2, 3, 3], [1, 2, 5]]), 15))
tau = (1, 2, 3, 0, 5, 4)
lv.expect("l8", "screens[8].widget.answer", two('ord tau', order_p(tau), order_b(tau))); lv.expect("l8", "screens[8].widget.wrong[0].value", 8)
out8 = tuple(2 * k % 7 if k < 7 else 7 for k in range(8))
lv.expect("l8", "screens[9].widget.answer", two('out8', order_b(out8), mord(2, 7)))
two('out8 cycles', [c for c in cyc(out8) if len(c) > 1], [[1, 2, 4], [3, 6, 5]])
out52 = tuple(2 * k % 51 if k < 51 else 51 for k in range(52)); in52 = tuple((2 * k + 1) % 53 for k in range(52))
lv.expect("l8", "screens[10].widget.answer", two('out52', order_b(out52), mord(2, 51)))
two('in52', order_b(in52), mord(2, 53)); lv.expect("l8", "screens[10].feedback.byKey.deck", "in-shuffle")
two('2^7 mod 51', pow(2, 7, 51), 26); two('256', 5 * 51 + 1, 2 ** 8); lv.expect("l8", "screens[10].feedback.byKey.seven", 26)
lv.expect("l8", "quiz[3].widget.answer", two('|S5|', len(list(itertools.permutations(range(5)))), math.factorial(5)))

# ---------- l9 ----------
two('(13)(12)', comp((2, 1, 0), (1, 0, 2)), (1, 2, 0))
for j, want in enumerate([2, 3, 1]):
    lv.expect("l9", f"screens[2].widget.rows[{j}][1].answer", want)
lv.expect("l9", "screens[4].widget.answer", two('inv sigma', inv_count(sig), sum(sum(1 for b in sig[i + 1:] if b < a) for i, a in enumerate(sig))))
two('sign sigma', sign_c(sig), sign_i(sig)); two('n-c', 8 - len(cyc(sig)), 5)
start = (1, 2, 3, 4, 5, 0)
def nb(st, Rr, Cc):
    z = st.index(0); r_, c_ = divmod(z, Cc)
    for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        rr, cc = r_ + dr, c_ + dc
        if 0 <= rr < Rr and 0 <= cc < Cc:
            l = list(st); w = rr * Cc + cc; l[z], l[w] = l[w], l[z]; yield tuple(l)
seen = {start}; q = deque([start])
while q:
    x = q.popleft()
    for y in nb(x, 2, 3):
        if y not in seen:
            seen.add(y); q.append(y)
two('2x3 reach', len(seen), math.factorial(6) // 2); lv.expect("l9", "screens[7].explain.text", 360); lv.expect("l9", "screens[7].explain.text", 720)
f16 = math.factorial(16); lv.expect("l9", "screens[7].prose", f16)
two('16!/2', f16 // 2, math.prod(range(1, 17)) // 2); lv.expect("l9", "screens[7].widget.options[0].text", f16 // 2)
lv.expect("l9", "screens[9].widget.answer", two('|A4| again', len(A4), 12)); lv.expect("l9", "screens[9].explain.text", 60)
two('|A5|', sum(1 for pp in itertools.permutations(range(5)) if sign_i(pp) == 1), math.factorial(5) // 2)
ret = [2, 1, 4, 5, 3]
D = two('discordant', inv_count(ret), sum(1 for i in range(5) for j in range(i + 1, 5) if (i - j) * (ret[i] - ret[j]) < 0))
lv.expect("l9", "screens[10].widget.rows[0][1].answer", D)
tauk = two('kendall', 1 - 4 * D / 20, ((10 - D) - D) / 10); lv.expect("l9", "screens[10].widget.rows[1][1].answer", tauk)
two('3-cycle even', sign_c((1, 2, 0)), sign_i((1, 2, 0))); two('4-cycle odd', sign_c((1, 2, 3, 0)), -1)
der = [pp for pp in itertools.permutations(range(4)) if all(pp[i] != i for i in range(4))]
two('der4', len(der), round(math.factorial(4) * sum((-1) ** k / math.factorial(k) for k in range(5))))
c4 = two('4-cycles', sum(1 for pp in der if len(cyc(pp)) == 1), math.factorial(3)); dd = two('double', sum(1 for pp in der if len(cyc(pp)) == 2), 3)
lv.expect("l9", "quiz[0].widget.rows[0][1].answer", c4); lv.expect("l9", "quiz[0].widget.rows[1][1].answer", dd); lv.expect("l9", "quiz[0].widget.rows[2][1].answer", len(der))
two('out52 sign', sign_c(out52), sign_i(out52))

# ---------- review-2 ----------
two('Z10 subgroup', [Hs for Hs in ([0, 5], [0, 3, 6, 9], [1, 3, 5, 7, 9], [0, 1, 2]) if all((a - b) % 10 in Hs for a in Hs for b in Hs)], [[0, 5]])
c9 = sorted({tuple(sorted((a + h) % 9 for h in (0, 3, 6))) for a in range(9)})
for i in (1, 2):
    for j in range(3):
        lv.expect("review", f"items[1].widget.rows[{i - 1}][{j + 1}].answer", c9[i][j])
two('div 20', [d for d in (1, 4, 5, 10, 3, 8, 6) if 20 % d == 0], [1, 4, 5, 10])
rp = (2, 5, 0, 4, 3, 1)
two('review cycles', [[x + 1 for x in c] for c in cyc(rp) if len(c) > 1], [[1, 3], [2, 6], [4, 5]])
lv.expect("review", "items[5].widget.answer", two('lcm 3,2,4', order_b((1, 2, 0, 4, 3, 6, 7, 8, 5)), math.lcm(3, 2, 4)))
two('sign 5c2c', sign_c((1, 2, 3, 4, 0, 6, 5)), sign_i((1, 2, 3, 4, 0, 6, 5))); two('sign value', sign_c((1, 2, 3, 4, 0, 6, 5)), -1)
lv.expect("review", "items[7].widget.answer", two('[D4:<s>]', len({frozenset(comp(x, h) for h in (E4, S)) for x in D4}), 8 // 2))

# ---------- homework-2 ----------
pr = round(1 - sum(1 / k for k in range(51, 101)), 4)   # method 1: P(longest cycle = k) = 1/k for k > 50
two('prisoners via counting (method 2)', round(1 - sum(math.comb(100, k) * math.factorial(k - 1) * math.factorial(100 - k) for k in range(51, 101)) / math.factorial(100), 4), pr)
lv.expect("homework", "items[4].widget.answer", pr); lv.expect("homework", "items[4].widget.wrong[0].value", round(1 - pr, 4))
two('out8 sign', sign_c(out8), sign_i(out8)); two('out8 c', len(cyc(out8)), 4)
o2 = two('order 2 in S4', sum(1 for pp in itertools.permutations(range(4)) if order_b(pp) == 2), math.comb(4, 2) + 3)
lv.expect("homework", "items[6].widget.answer", o2)
lv.expect("homework", "items[7].widget.answer", two('cosets 5-cycle', math.factorial(5) // order_b((1, 2, 3, 4, 0)), 24))
two('subsets 462', math.comb(11, 5), 462); lv.expect("homework", "items[3].explain.text", 462)
random.seed(2026)
board = list(range(1, 16)) + [0]
def nb4(st):
    return [list(x) for x in nb(tuple(st), 4, 4)]
for _ in range(200):
    board = random.choice(nb4(board))
two('planted board', board, [1, 2, 3, 6, 9, 0, 10, 11, 8, 15, 14, 4, 5, 13, 7, 12])
# the parity rule, checked against a breadth-first search of every 2 by 3 board (the 4 by 4 boards above are built by legal slides)
seen = {start}; q = deque([start])
while q:
    x = q.popleft()
    for y in nb(x, 2, 3):
        if y not in seen:
            seen.add(y); q.append(y)
def rule23(bd):
    perm = [(t - 1) % 6 for t in bd]; z = bd.index(0); r_, c_ = divmod(z, 3)
    return sign_c(perm) == (-1) ** ((1 - r_) + (2 - c_))
two('parity rule on 2x3', all(rule23(bd) == (bd in seen) for bd in itertools.permutations(range(6))), True)

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
        if t.get('setup'):
            exec(t['setup'], ns)
        return eval(t['call'], ns) == eval(t['expect'], ns)
    except Exception:
        return False
for ref in ["l5", "l6", "l7", "l8", "l9", "review", "homework"]:
    for w in widgets(lv._file(ref)[1]):
        two(f'{ref} code solution', all(run(w['solution'], w, t) for t in w['tests'] + w.get('examples', [])), True)
        two(f'{ref} code starter fails one', not all(run(w['starter'], w, t) for t in w['tests']), True)

lv.check_wrongs()
if bad:
    print('two-way mismatches:', *bad, sep='\n  ')
    lv._rec(False, 'two-way checks', '; '.join(bad))
lv.report()
