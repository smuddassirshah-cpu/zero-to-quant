#!/usr/bin/env python3
"""Second read of topology problems-1 to -3: the reader's own recomputation.

Imports nothing from problems-topology-numbers.py. Every setting is typed from the prose and every key is
found by a route that needs no closed form: direction scans, grid scans, bisection, brute force over subsets
and bijections, loops for the "smallest n", plain iteration of each map. Standard library only, so no solver
of another SciPy build can change the result. Each wrong[] value is rebuilt from the slip its line names.

Exit 0 always. A failing check prints a FINDING line (CI reads them); a NOTE line is a judgement of the
reader that the review explains.
    <scratchpad>/venv/bin/python docs/reports/problems-topology-numbers-read.py
"""
import itertools
import json
import math
import os
import random
import re

HERE = os.path.dirname(os.path.abspath(__file__))
COURSE = os.path.join(HERE, '..', '..', 'app', 'content', 'courses', 'topology')
SETS = {n: json.load(open(os.path.join(COURSE, 'problems-%d.json' % n), encoding='utf-8')) for n in (1, 2, 3)}
checks = 0
findings = 0


def check(ok, label):
    global checks, findings
    checks += 1
    if not ok:
        findings += 1
        print('FINDING %s' % label)


def note(label):
    print('NOTE %s' % label)


def part(n, item, k):
    for it in SETS[n]['items']:
        if it['id'] == item:
            return it['parts'][k - 1]
    raise KeyError(item)


def bisect(f, lo, hi, it=200):
    flo = f(lo)
    for _ in range(it):
        mid = (lo + hi) / 2
        if (f(mid) > 0) == (flo > 0):
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def num(n, item, k, mine, slips, dp=None):
    """Key against mine; each wrong value against the slip I rebuilt; bands; the printed rounding."""
    p = part(n, item, k)
    w = p['widget']
    tag = 'problems-%d %s part %d' % (n, item, k)
    check(w['kind'] == 'numeric', tag + ': numeric widget')
    tol = w['tol']['abs']
    check(abs(w['answer'] - mine) <= max(tol, 1e-9) / 2 + 1e-12, tag + ': key %r, reader %r' % (w['answer'], mine))
    if dp is not None:
        shown = round(mine, dp)
        check(abs(shown - w['answer']) <= tol, tag + ': the %d-place value %r is outside the key band' % (dp, shown))
        for coarser in (dp - 1,):
            pass
        txt = json.dumps(p['feedback'], ensure_ascii=False) + p['explain']['text']
        s = ('%.' + str(dp) + 'f') % mine
        check(s in txt or s.rstrip('0').rstrip('.') in txt, tag + ': %s is not printed in the feedback or explanation' % s)
        check(abs(mine * 10 ** dp - math.floor(mine * 10 ** dp) - 0.5) > 1e-6, tag + ': key on a rounding tie')
    wrong = {x['id']: x for x in w.get('wrong', [])}
    check(set(wrong) == set(slips), tag + ': wrong ids %s, reader expected %s' % (sorted(wrong), sorted(slips)))
    for wid, val in slips.items():
        if wid not in wrong:
            continue
        x = wrong[wid]
        wt = x['tol']['abs']
        check(abs(x['value'] - val) <= max(wt, 5e-5) + 1e-12, tag + ': wrong %s is %r, the slip gives %r' % (wid, x['value'], val))
        check(abs(x['value'] - w['answer']) > tol + wt, tag + ': wrong %s band meets the key band' % wid)
        check(wid in p['feedback'].get('byKey', {}), tag + ': wrong %s has no line' % wid)
    return p


def texcheck(n, item, k, table, key, samples):
    """An expression part: every tex string is one the reader typed as a function; the key and accepts agree
    with the reader's function at the samples and each wrong form differs from it."""
    p = part(n, item, k)
    w = p['widget']
    tag = 'problems-%d %s part %d' % (n, item, k)
    check(w['kind'] == 'expression', tag + ': expression widget')
    forms = [(w['answer'], True)] + [(a, True) for a in w.get('accept', [])] + [(x['tex'], False) for x in w.get('wrong', [])]
    for tex, good in forms:
        if tex not in table:
            check(False, tag + ': form %s not known to the reader' % tex)
            continue
        same = all(abs(table[tex](s) - key(s)) < 1e-9 for s in samples)
        check(same == good, tag + ': form %s %s the reader\'s answer' % (tex, 'differs from' if good else 'equals'))
    for x in w.get('wrong', []):
        check(x['id'] in p['feedback'].get('byKey', {}), tag + ': wrong %s has no line' % x['id'])


def printed(n, item, k, strings):
    p = part(n, item, k)
    txt = p['question'] + json.dumps(p['feedback'], ensure_ascii=False) + p['explain']['text']
    for s in strings:
        check(s in txt, 'problems-%d %s part %d: expected to find %s in the text' % (n, item, k, s))


# ---------------------------------------------------------------- set shape
LEVEL_LESSONS = {1: ['l1-many-distances', 'l2-open-balls', 'l3-closure-interior-boundary', 'l4-continuity-by-open-sets'],
                 2: ['l5-topologies', 'l6-bases-and-subspaces', 'l7-homeomorphisms', 'l8-connectedness'],
                 3: ['l9-open-covers', 'l10-compact-images', 'l11-complete-spaces', 'l12-contraction-mapping',
                     'l13-fixed-point-iteration']}
for n, d in SETS.items():
    skills = set()
    for l in LEVEL_LESSONS[n]:
        skills |= set(json.load(open(os.path.join(COURSE, l + '.json'), encoding='utf-8')).get('skills', []))
    check(3 <= len(d['items']) <= 5, 'problems-%d: 3 to 5 items' % n)
    check(any(it['difficulty'] == 5 for it in d['items']), 'problems-%d: one item of difficulty 5' % n)
    typed = total = 0
    for it in d['items']:
        check(3 <= len(it['parts']) <= 5, 'problems-%d %s: 3 to 5 parts' % (n, it['id']))
        check(set(it['skills']) <= skills, 'problems-%d %s: skills %s not all carried by the level\'s lessons %s'
              % (n, it['id'], it['skills'], sorted(skills)))
        for j, p in enumerate(it['parts']):
            total += 1
            typed += p['widget']['kind'] in ('numeric', 'expression')
            if j:
                check(re.search(r'[Uu]sing', p['question']) is not None,
                      'problems-%d %s part %d does not restate an earlier result' % (n, it['id'], j + 1))
            sentences = [s for s in re.split(r'(?<=[.])\s+(?=[A-Z$])', p['explain']['text']) if s]
            check(len(sentences) <= 3, 'problems-%d %s part %d: explanation over three sentences' % (n, it['id'], j + 1))
    check(3 * typed >= 2 * total, 'problems-%d: typed parts %d of %d' % (n, typed, total))

# ================================================================ problems-1
# ---- p-plotter-zone: d_w = 2|a| + |b|, f = 3 x1 + x2, y = (2.5, 0.5), U = {f < 12}
dirs = [(math.cos(2 * math.pi * i / 200000), math.sin(2 * math.pi * i / 200000)) for i in range(200000)]
L = max(abs(3 * a + b) / (2 * abs(a) + abs(b)) for a, b in dirs)
check(abs(L - 1.5) < 1e-6, 'plotter: best constant L = %r' % L)
eps = [0.3, 1.0, 2.7, 9.0]
texcheck(1, 'p-plotter-zone', 1, {
    '\\frac{2\\varepsilon}{3}': lambda e: 2 * e / 3, '2\\varepsilon/3': lambda e: 2 * e / 3,
    '\\frac{\\varepsilon}{1.5}': lambda e: e / 1.5, '\\frac{\\varepsilon}{4}': lambda e: e / 4,
    '\\frac{\\varepsilon}{3}': lambda e: e / 3, '\\frac{\\varepsilon}{6}': lambda e: e / 6}, lambda e: e / L, eps)
fy = 3 * 2.5 + 0.5
gap = 12 - fy
check(fy == 8 and gap == 4, 'plotter: f(y) = 8 and the gap is 4')
r = gap / L
# the ball B_w(y, r) really stays in U and no larger one does: sup of f over the ball is f(y) + L r
check(abs(fy + L * r - 12) < 1e-9, 'plotter: sup of f on B_w(y, r) reaches 12')
num(1, 'p-plotter-zone', 2, r, {'sum-coeffs': gap / 4, 'no-weight': gap / 3, 'times-weight': gap / 6, 'whole-bound': 12 / L}, 4)
cw = max(2 * abs(a) + abs(b) for a, b in dirs)          # largest d_w length of a Euclidean unit step
check(abs(cw - math.sqrt(5)) < 1e-6, 'plotter: sup of d_w on the unit circle is root 5')
s = r / cw
num(1, 'p-plotter-zone', 3, s, {'used-three': r / 3, 'max-weight': r / 2, 'multiplied': r * cw, 'no-change': r}, 4)
# true distance to the line 3 x1 + x2 = 12: minimise along the line, x1 = t
dist = min(math.hypot(t - 2.5, (12 - 3 * t) - 0.5) for t in [3 + i * 1e-5 for i in range(100001)])
p4 = num(1, 'p-plotter-zone', 4, dist, {'no-root': gap / 10, 'taxicab-normal': gap / 4, 'horizontal': gap / 3}, 4)
check(dist > s, 'plotter: the true distance exceeds the floor of part 3')
check(abs(3 * 3.7 + 0.9 - 12) < 1e-12 and abs(math.hypot(1.2, 0.4) - dist) < 1e-6, 'plotter: nearest point (3.7, 0.9)')
check(abs(3 * 23 / 6 + 0.5 - 12) < 1e-12, 'plotter: the horizontal point (23/6, 0.5) is on the line')
# a slip made from the 4-place value restated in the stem must land in its own band
for item, k, wid, restated, f in (('p-plotter-zone', 3, 'multiplied', 2.6667, lambda v: v * math.sqrt(5)),
                                  ('p-diagonal-sphere', 4, 'times-root', 0.0808, lambda v: v * math.sqrt(2)),
                                  ('p-diagonal-sphere', 4, 'half', 0.0808, lambda v: v / 2)):
    x = [q for q in part(1, item, k)['widget']['wrong'] if q['id'] == wid][0]
    typed_val = round(f(restated), 4)
    check(abs(typed_val - x['value']) <= x['tol']['abs'] + 1e-9,      # the engine's band is closed, with float slack
          'problems-1 %s part %d: the slip %s worked from the 4-place value %s is %s, outside its band %s +- %s'
          % (item, k, wid, restated, typed_val, x['value'], x['tol']['abs']))

# ---- p-cubic-band: h = x^3 - 27x, A = h^{-1}((0, 54])
h = lambda x: x ** 3 - 27 * x
for x in (-7.3, -1.1, 0.4, 2.2, 9.9):
    check(abs(h(x) - x * (x * x - 27)) < 1e-9 and abs(h(x) - 54 - (x + 3) ** 2 * (x - 6)) < 1e-9, 'cubic: factorisations at %s' % x)
step = 1e-4
inA = lambda x: 0 < h(x) <= 54
xs = [-10 + i * step for i in range(200001)]
mem = [inA(x) for x in xs]
length = sum(mem) * step
num(1, 'p-cubic-band', 1, round(length, 2), {'right-only': 6 - 3 * math.sqrt(3), 'left-only': 3 * math.sqrt(3)})
flips = [xs[i] for i in range(1, len(xs)) if mem[i] != mem[i - 1]]
check(len(flips) == 4, 'cubic: %d membership changes on the grid' % len(flips))
for got, want in zip(flips, (-3 * math.sqrt(3), 0, 3 * math.sqrt(3), 6)):
    check(abs(got - want) < 2 * step, 'cubic: boundary point near %s' % want)
num(1, 'p-cubic-band', 2, len(flips), {'with-touch': 5, 'drop-member': 3})
top = [x for x in (-3, 6) if h(x) == 54]                # exact integers: h = 54 only here (double root at -3)
check(top == [-3, 6] and all(h(x) < 54 for x in xs if inA(x) and abs(x + 3) > step and abs(x - 6) > step), 'cubic: h = 54 at -3 and 6 only')
interior_missed = [x for x in top if inA(x - 1e-6) and inA(x + 1e-6)]
num(1, 'p-cubic-band', 3, len(interior_missed), {'both-ends': 2, 'equal': 0})
rr = bisect(lambda q: 1 if all(inA(-3 + q * u) for u in (-0.999999, 0.999999, -0.5, 0.5)) else -1, 0.1, 4)
num(1, 'p-cubic-band', 4, rr, {'far-end': 3, 'to-root': 3 * math.sqrt(3), 'half-piece': 1.5 * math.sqrt(3)}, 4)

# ---- p-diagonal-sphere: z = (0.65, 0.65)
dp_ = lambda p: (0.65 ** p + 0.65 ** p) ** (1 / p)
pstar = bisect(lambda p: dp_(p) - 1, 1, 5)
num(1, 'p-diagonal-sphere', 1, pstar, {'inverted': 1 / pstar, 'sign': -pstar}, 4)
printed(1, 'p-diagonal-sphere', 1, ['%.6f' % math.log(2), '%.6f' % math.log(1 / 0.65)])
inside = [p for p in (1, 1.5, 2, 3, 4) if dp_(p) < 1] + (['inf'] if max(0.65, 0.65) < 1 else [])
num(1, 'p-diagonal-sphere', 2, len(inside), {'reversed': 6 - len(inside), 'finite-only': len(inside) - 1})
s2 = 1 - dp_(2)
num(1, 'p-diagonal-sphere', 3, s2, {'coordinate': 1 - 0.65, 'distance': dp_(2)}, 4)
t = bisect(lambda q: 1 - math.hypot(0.65 + q, 0.65 + q), 0, 0.3)   # the far corner of the square reaches the rim
num(1, 'p-diagonal-sphere', 4, t, {'times-root': s2 * math.sqrt(2), 'same': s2, 'half': s2 / 2}, 4)
check(round(0.0808 / math.sqrt(2), 4) == round(t, 4), 'diagonal: 0.0808 / root 2 rounds to the key')

# ---- p-reciprocal-room: f = 1/x near 0.5
lo = bisect(lambda x: 1 / x - 2.5, 0.2, 0.5)
hi = bisect(lambda x: 1 / x - 1.5, 0.5, 1.5)
num(1, 'p-reciprocal-room', 1, hi - lo, {'length-v': 1.0, 'linear': 1 / 4}, 4)
num(1, 'p-reciprocal-room', 2, min(0.5 - lo, hi - 0.5), {'far-side': hi - 0.5, 'half-length': (hi - lo) / 2, 'linear': 0.5 / 4})


def delta_room(e):
    left = 0.5 - 1 / (2 + e)
    right = (1 / (2 - e) - 0.5) if e < 2 else float('inf')
    return min(left, right)


es = [0.1, 0.5, 1.3, 1.99, 2.0, 7.0, 400.0]
texcheck(1, 'p-reciprocal-room', 3, {
    '\\frac{\\varepsilon}{2(2+\\varepsilon)}': lambda e: e / (2 * (2 + e)), '\\frac{\\varepsilon}{4+2\\varepsilon}': lambda e: e / (4 + 2 * e),
    '0.5-\\frac{1}{2+\\varepsilon}': lambda e: 0.5 - 1 / (2 + e),
    '\\frac{\\varepsilon}{2(2-\\varepsilon)}': lambda e: e / (2 * (2 - e)) if e != 2 else float('inf'),
    '\\frac{\\varepsilon}{4}': lambda e: e / 4, '\\frac{\\varepsilon}{2+\\varepsilon}': lambda e: e / (2 + e)}, delta_room, es)
check(abs(delta_room(0.5) - 0.1) < 1e-12 and abs(0.5 / 4 - 0.125) < 1e-12 and abs(0.5 / 2.5 - 0.2) < 1e-12, 'reciprocal: the values quoted at 0.5')
num(1, 'p-reciprocal-room', 4, round(delta_room(1e12), 9), {'no-half': 1.0})

# ================================================================ problems-2
# ---- p-four-point-line
X = frozenset('abcd')
basis = [frozenset('a'), frozenset('c'), frozenset('abc'), frozenset('cd')]
tau = set()
for k in range(len(basis) + 1):
    for combo in itertools.combinations(basis, k):
        tau.add(frozenset().union(*combo))
for U in tau:
    for V in tau:
        check(U & V in tau and U | V in tau, 'four-point: tau closed under union and intersection')
num(2, 'p-four-point-line', 1, len(tau), {'pieces-only': len(basis), 'no-empty': len(tau) - 1, 'all-subsets': 16})


def sub(tau_, Y):
    return {U & Y for U in tau_}


def connected(tau_, Y):
    t_ = sub(tau_, Y)
    return not any(U and U != Y and (Y - U) in t_ for U in t_)


Y = X - {'c'}
num(2, 'p-four-point-line', 2, len(sub(tau, Y)), {'no-merging': len(tau), 'inside-only': len([U for U in tau if U <= Y])})
cuts = [x for x in sorted(X) if not connected(tau, X - {x})]
check(cuts == ['b', 'c'], 'four-point: cut points %s' % cuts)
num(2, 'p-four-point-line', 3, len(cuts), {'only-c': 1, 'every-point': 4})
homeos = [perm for perm in itertools.permutations(sorted(X))
          if {frozenset(dict(zip(sorted(X), perm))[x] for x in U) for U in tau} == tau]
num(2, 'p-four-point-line', 4, len(homeos), {'reversal': 2, 'every-bijection': 24})
check(homeos == [tuple('abcd')], 'four-point: the one homeomorphism is the identity')
listed = re.findall(r'\\\{[a-d, ]*\\\}|\\varnothing|\$X\$', part(2, 'p-four-point-line', 2)['question'].split('how many')[0])
check(len(listed) >= 8, 'four-point part 2 lists the 8 open sets')

# ---- p-bond-yield-map: re-authored as p-signal-bands in the fix pass; its checks are removed (the delta reader checks the new problem)

# ---- p-gapped-domain: Y = [0, 1) u (1, 2] u {4}
g_ = 1000
Ypts = [i / g_ for i in range(0, g_)] + [i / g_ for i in range(g_ + 1, 2 * g_ + 1)] + [4.0]
cands = {'[0,1)': lambda x: 0 <= x < 1, '{4}': lambda x: x == 4, '(1,2]': lambda x: 1 < x <= 2,
         '[0,0.5]': lambda x: 0 <= x <= 0.5, '(1.5,2]': lambda x: 1.5 < x <= 2}


inY = lambda x: 0 <= x < 1 or 1 < x <= 2 or x == 4


def open_in_Y(W):
    """Every point of W has a small interval whose points of Y all lie in W (probe at 1e-9 on both sides)."""
    return all(all(W(y) for y in (x - 1e-9, x + 1e-9) if inY(y)) for x in Ypts + [0.5, 1.5] if W(x))


n_open = [name for name, W in cands.items() if open_in_Y(W)]
check('[0,0.5]' not in n_open, 'gapped: [0, 0.5] is not open in Y')
num(2, 'p-gapped-domain', 1, len(n_open), {'open-in-r': 0, 'no-singleton': len(n_open) - 1})
srt = sorted(Ypts)
comps = 1 + sum(1 for a, b in zip(srt, srt[1:]) if b - a > 1.5 / g_)
num(2, 'p-gapped-domain', 2, comps, {'joined': comps - 1, 'one': 1})
data = {0: -1, 0.9: 2, 1.5: -3, 2: 1, 4: 5}
pieces = [[x for x in data if 0 <= x < 1], [x for x in data if 1 < x <= 2], [x for x in data if x == 4]]
forced = [(min(data[x] for x in pc), max(data[x] for x in pc)) for pc in pieces]
zeros = sum(1 for a, b in forced if a < 0 < b)
num(2, 'p-gapped-domain', 3, zeros, {'across-gap': zeros + 1, 'one-zero': 1})
fine = [-10 + i * 1e-3 for i in range(20001)]
flen = sum(1 for v in fine if any(a <= v <= b for a, b in forced)) * 1e-3
num(2, 'p-gapped-domain', 4, round(flen, 1), {'one-interval': 8, 'added': sum(b - a for a, b in forced)})
q2 = part(2, 'p-gapped-domain', 2)['question']
if all(sx in q2 for sx in ('$[0, 1)$', '$(1, 2]$', '$\\{4\\}$')) and 'complement' in q2:
    note('problems-2 p-gapped-domain part 2: the stem lists the three clopen pieces, so the key 3 is their count (review finding)')

# ---- p-right-rays
A_pts = [1 + i / 1000 for i in range(1, 1000)] + [5.0]
num(2, 'p-right-rays', 1, max(A_pts), {'ignore-point': 2})
inB = lambda x: 3 <= x <= 8 or x > 10
left = min(tt for tt in [i / 10 for i in range(0, 200)] if all(inB(x) for x in [tt + j / 100 for j in range(1, 3000)]))
num(2, 'p-right-rays', 2, left, {'usual': 3, 'closed-end': 8})
maps = {'2x+1': lambda x: 2 * x + 1, '-x': lambda x: -x, 'x^3': lambda x: x ** 3, 'e^x': lambda x: math.exp(x), 'x+1': lambda x: x + 1}
pts = [-30 + i * 0.01 for i in range(6001)]


def ray_homeo(f):
    vals = [f(x) for x in pts]
    increasing = all(b > a for a, b in zip(vals, vals[1:]))
    onto = vals[0] < -25 and vals[-1] > 25             # unbounded both ways on a wide window
    return increasing and onto


good = [name for name, f in maps.items() if ray_homeo(f)]
check(good == ['2x+1', 'x^3', 'x+1'], 'right rays: homeomorphisms %s' % good)
num(2, 'p-right-rays', 3, len(good), {'with-flip': len(good) + 1})
opts = part(2, 'p-right-rays', 4)['widget']['options']
check([o['id'] for o in opts if o.get('correct')] == ['conn-not-haus'], 'right rays part 4: the correct option')
check(all('why' in o for o in opts if not o.get('correct')), 'right rays part 4: each wrong option has a why line')

# ================================================================ problems-3
# ---- p-quadratic-iteration, p-input-output, p-dyadic-points: re-authored in the fix pass as p-kernel-equation,
# p-trapping-interval and p-coin-paths; their checks are removed (the delta reader checks the new problems)

# ---- p-cube-delta: f = x^3 on K = [-1, 2]
sets_ = {'[-1,2]': (True, True), '[-1,2)': (False, True), '[-1,inf)': (True, False), '[-1,0]u{2}': (True, True)}   # (closed, bounded)
n_compact = sum(1 for c, b_ in sets_.values() if c and b_)
num(3, 'p-cube-delta', 1, n_compact, {'bounded': sum(1 for c, b_ in sets_.values() if b_), 'intervals-only': 1})
kx = [-1 + i * 3 / 3000 for i in range(3001)]
img = [x ** 3 for x in kx]
num(3, 'p-cube-delta', 2, max(img) - min(img), {'positive-only': 8, 'cube-gap': 7})
big = max(abs(a_ * a_ + a_ * b_ + b_ * b_) for a_ in kx[::10] for b_ in kx[::10])
check(abs(big - 12) < 1e-9, 'cube: the factor peaks at %r' % big)
texcheck(3, 'p-cube-delta', 3, {
    '\\frac{\\varepsilon}{12}': lambda e: e / 12, '\\varepsilon/12': lambda e: e / 12, '\\frac{\\varepsilon}{9}': lambda e: e / 9,
    '\\frac{\\varepsilon}{8}': lambda e: e / 8, '\\frac{\\varepsilon}{3}': lambda e: e / 3}, lambda e: e / big, eps)
# part 4 as fixed (finding 12): part 3's own delta at epsilon = 1
dl = 1 / 12
root2 = bisect(lambda x: (x + dl) ** 3 - x ** 3 - 1, 0, 50)
num(3, 'p-cube-delta', 4, root2, {'slope-only': math.sqrt(1 / (3 * dl))}, 4)
check(abs(root2 - 1.9582) < 5e-5 and root2 + dl > 2 and abs(math.sqrt(1 / (3 * dl)) - 2) < 1e-12, 'proposed cube part 4: root %r' % root2)
check(abs(3 * dl - 0.25) < 1e-12 and abs(3 * dl * dl - 1 / 48) < 1e-12 and abs(dl ** 3 - 1 / 1728) < 1e-15, 'proposed cube part 4: coefficients')
check(abs((root2 + dl) - 2.0415) < 5e-5, 'proposed cube part 4: x + 1/12 = %r' % (root2 + dl))
# ---- same-course style: lesson references in code spans
ticks = sum(len(re.findall(r'`l\d+`', json.dumps(d, ensure_ascii=False))) for d in SETS.values())
check(ticks == 0, 'the three sets write %d lesson references as code spans (`l4`); the course\'s lessons write l4 bare' % ticks)

print('problems-topology-numbers-read: %d checks, %d FINDING line(s)' % (checks, findings))
