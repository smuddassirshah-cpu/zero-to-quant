"""Recompute every Fluency answer and every named slip in the number-sense sets from the drawn variable values alone.

Method 1 is the engine's own arithmetic (the set's `let` expressions, resolved by tools/fluency-sample.mjs --json).
Method 2 is this script: exact fractions (Python's Fraction) rebuild each prompt's maths from the vars, work the
answer out again, and rebuild each slip from what the learner would have done. For every draw it checks
  - the prompt is the expression the vars describe (rebuilt here as text);
  - the engine's key equals the key worked out here, and a fraction key is written in lowest terms;
  - the slips offered are exactly the ones whose condition holds here, each equal to the slip worked out here,
    each different from the key (outside its tolerance) and from the other slips.
Run:  <scratchpad>/venv/bin/python docs/reports/fluency-number-sense-numbers.py   (exit 0 = pass; FLUENCY_N sets draws)
"""
import json, os, re, subprocess, sys
from fractions import Fraction as F
from math import gcd

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
from numbers_lib import Level

APP = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app')
N = int(os.environ.get('FLUENCY_N', '200'))
lv = Level("number-sense", 1)
count = 0


def check(ok, label):
    global count
    count += 1
    lv.claim(bool(ok), label)


def draws(ref, fam):
    out = subprocess.run(['node', 'tools/fluency-sample.mjs', '--set', ref, '--family', fam, '--n', str(N), '--json'],
                         cwd=APP, capture_output=True, text=True, check=True).stdout
    return json.loads(out)['items']


def num(x):
    """A value printed by the sampler (number, or text such as '7/12' or '\\frac{7}{12}') as an exact fraction."""
    if isinstance(x, (int, float)):
        return F(x).limit_denominator(10 ** 9) if isinstance(x, float) else F(x)
    s = str(x).replace(' ', '')
    m = re.fullmatch(r'(-?)\\frac\{(-?\d+)\}\{(-?\d+)\}', s)
    if m:
        return (-1 if m.group(1) else 1) * F(int(m.group(2)), int(m.group(3)))
    return F(s)


def lowest(tex):
    m = re.fullmatch(r'-?\\frac\{(\d+)\}\{(\d+)\}', tex)
    if m:
        return gcd(int(m.group(1)), int(m.group(2))) == 1 and int(m.group(2)) > 1
    return re.fullmatch(r'-?\d+', tex) is not None


def br(x):
    """A signed number as the prompt writes it: brackets round a negative."""
    return f'({x})' if x < 0 else f'{x}'


def item(it, prompt, key, slips, tol=0, fraction=False):
    tag = f"{it['family']} seed {it['seed']}"
    check(it['prompt'] == prompt, f"{tag}: prompt {it['prompt']!r} is {prompt!r}")
    got = num(it['answer'])
    check(got == key, f"{tag}: key {it['answer']} equals {key}")
    if fraction:
        check(lowest(it['answer']), f"{tag}: key {it['answer']} is a whole number or a fraction in lowest terms")
    ids = [w['id'] for w in it['wrong']]
    check(sorted(ids) == sorted(slips), f"{tag}: slips offered {ids} are {sorted(slips)}")
    vals = {}
    for w in it['wrong']:
        v = num(w.get('tex', w.get('value')))
        wt = F((w.get('tol') or {}).get('abs', 0)).limit_denominator(10 ** 6)
        vals[w['id']] = v
        if w['id'] in slips:
            check(abs(v - slips[w['id']]) <= F(1, 10 ** 6), f"{tag}: slip {w['id']} = {v} is {slips[w['id']]}")
        check(abs(v - key) > F(tol).limit_denominator(10 ** 6) + wt, f"{tag}: slip {w['id']} differs from the key")
    vs = list(vals.items())
    for i in range(len(vs)):
        for j in range(i + 1, len(vs)):
            check(abs(vs[i][1] - vs[j][1]) > F(1, 100), f"{tag}: slips {vs[i][0]} and {vs[j][0]} differ")


def run(ref, fam, fn):
    for it in draws(ref, fam):
        V = {k: (F(x) if not isinstance(x, str) else x) for k, x in it['vars'].items()}
        fn(it, V)


def fr(a, b):
    return f"\\tfrac{{{a}}}{{{b}}}"


# ---- l3-adding-pieces -------------------------------------------------------------------------------
def l3_add(it, V):
    a, b, c, d = (int(V[k]) for k in 'abcd')
    check(b != d and a < b and c < d and gcd(a, b) == 1 and gcd(c, d) == 1, f"add seed {it['seed']}: proper, lowest, unlike")
    L = b * d // gcd(b, d)
    key = F(a, b) + F(c, d)
    check(key == F(a * (L // b) + c * (L // d), L), f"add seed {it['seed']}: renamed tops add to the key")
    item(it, f"Work out ${fr(a, b)} + {fr(c, d)}$ as a fraction in its lowest terms.", key,
         {'tops-and-bottoms': F(a + c, b + d), 'tops-not-renamed': F(a + c, L)}, fraction=True)


def l3_sub(it, V):
    a, b, c, d = (int(V[k]) for k in 'abcd')
    L = b * d // gcd(b, d)
    key = F(a, b) - F(c, d)
    check(key > 0, f"subtract seed {it['seed']}: the answer is positive")
    slips = {}
    if a > c and b > d and F(a - c, b - d) != key:
        slips['tops-and-bottoms'] = F(a - c, b - d)
    if F(a - c, L) != key:
        slips['tops-not-renamed'] = F(a - c, L)
    item(it, f"Work out ${fr(a, b)} - {fr(c, d)}$ as a fraction in its lowest terms.", key, slips, fraction=True)


# ---- l5-how-many-halves -----------------------------------------------------------------------------
def l5_whole(it, V):
    n, a, b = int(V['n']), int(V['a']), int(V['b'])
    key = n / F(a, b)
    check(key * F(a, b) == n, f"whole seed {it['seed']}: key times the divisor gives {n}")
    slips = {'multiplied': n * F(a, b)}
    if a > 1:
        slips['bottom-only'] = F(n * b)
    item(it, f"Work out ${n} \\div {fr(a, b)}$, as a whole number or a fraction in its lowest terms.", key, slips, fraction=True)


def l5_frac(it, V):
    a, b, c, d = (int(V[k]) for k in 'abcd')
    key = F(a, b) / F(c, d)
    check(key * F(c, d) == F(a, b), f"fraction seed {it['seed']}: key times the divisor gives the first fraction")
    item(it, f"Work out ${fr(a, b)} \\div {fr(c, d)}$, as a whole number or a fraction in its lowest terms.", key,
         {'multiplied': F(a, b) * F(c, d), 'flipped-first': F(b, a) * F(c, d)}, fraction=True)


# ---- l8-below-zero ----------------------------------------------------------------------------------
def l8_add(it, V):
    a, m, s = int(V['a']), int(V['m']), int(V['s'])
    b = s * m
    key = a + b
    check(V['dir'] == ('left' if b < 0 else 'right'), f"add seed {it['seed']}: direction word matches the sign")
    slips = {'wrong-way': F(a - b)}
    if abs(a) + m not in (a - b, a + b):
        slips['dropped-signs'] = F(abs(a) + m)
    item(it, f"Work out ${a} + {br(b)}$.", F(key), slips)


def l8_sub(it, V):
    a, m, s = int(V['a']), int(V['m']), int(V['s'])
    b = s * m
    check(V['dir'] == ('right' if b < 0 else 'left'), f"subtract seed {it['seed']}: direction word matches the move")
    item(it, f"Work out ${a} - {br(b)}$.", F(a - b), {'added': F(a + b), 'reversed': F(b - a)})


# ---- l9-negative-times-negative ---------------------------------------------------------------------
def l9_mul(it, V):
    a, b = int(V['a']), int(V['b'])
    check(a < 0 or b < 0, f"multiply seed {it['seed']}: a negative appears")
    slips = {'sign-flipped': F(-a * b)}
    if a < 0 and b < 0 and a + b != -a * b:
        slips['added'] = F(a + b)
    item(it, f"Work out ${br(a)} \\times {br(b)}$.", F(a * b), slips)


def l9_div(it, V):
    q, b = int(V['q']), int(V['b'])
    a = q * b
    item(it, f"Work out ${br(a)} \\div {br(b)}$.", F(a, b), {'sign-flipped': F(-a, b), 'upside-down': F(b, a)})


def l9_three(it, V):
    a, b, c = int(V['a']), int(V['b']), int(V['c'])
    item(it, f"Work out ${br(a)} \\times {br(b)} \\times {br(c)}$.", F(a * b * c), {'sign-flipped': F(-a * b * c), 'first-pair-only': F(a * b)})


# ---- l12-which-first: evaluate the prompt with Python's own order of operations ----------------------
def ev(tex):
    s = tex.replace('\\times', '*').replace('\\div', '/').replace('^', '**')
    return F(eval(s, {'__builtins__': {}}, {'F': F})) if '/' not in s else F(eval(re.sub(r'(\d+)', r'F(\1)', s), {'__builtins__': {}}, {'F': F}))


def l12_times(it, V):
    a, b, c, o = int(V['a']), int(V['b']), int(V['c']), V['o']
    expr = f"{a} {o} {b} \\times {c}"
    key = ev(expr)
    slips = {'left-to-right': ev(f"({a} {o} {b}) \\times {c}")}
    if key < 0 and -key != slips['left-to-right']:
        slips['lost-sign'] = -key
    item(it, f"Work out ${expr}$.", key, slips)


def l12_powers(it, V):
    a, b, c, o = int(V['a']), int(V['b']), int(V['c']), V['o']
    expr = f"{a} {o} {b} \\times {c}^2"
    slips = {'multiplied-then-squared': ev(f"{a} {o} ({b} \\times {c})^2")}
    if c != 2:
        slips['doubled'] = ev(f"{a} {o} {b} \\times {c} \\times 2")
    item(it, f"Work out ${expr}$.", ev(expr), slips)


def l12_brackets(it, V):
    a, b, d, g = int(V['a']), int(V['b']), int(V['d']), int(V['g'])
    c = d + g
    expr = f"{a} + {b} \\times ({c} - {d})^2"
    item(it, f"Work out ${expr}$.", ev(expr),
         {'added-first': ev(f"({a} + {b}) \\times ({c} - {d})^2"), 'multiplied-then-squared': ev(f"{a} + ({b} \\times ({c} - {d}))^2")})


def l12_ltr(it, V):
    b, m, c, o1, o2 = int(V['b']), int(V['m']), int(V['c']), V['o1'], V['o2']
    a = b * m
    expr = f"{a} {o1} {b} {o2} {c}"
    slips = {'right-pair-first': ev(f"{a} {o1} ({b} {o2} {c})")}
    if o1 == '-':
        slips['minus-lost'] = ev(f"{a} + {b} + {c}")
    item(it, f"Work out ${expr}$.", ev(expr), slips, tol=0)


JOBS = [
    ('number-sense/fluency-l3-adding-pieces', 'add-unlike', l3_add),
    ('number-sense/fluency-l3-adding-pieces', 'subtract-unlike', l3_sub),
    ('number-sense/fluency-l5-how-many-halves', 'whole-by-fraction', l5_whole),
    ('number-sense/fluency-l5-how-many-halves', 'fraction-by-fraction', l5_frac),
    ('number-sense/fluency-l8-below-zero', 'add-signed', l8_add),
    ('number-sense/fluency-l8-below-zero', 'subtract-signed', l8_sub),
    ('number-sense/fluency-l9-negative-times-negative', 'multiply-two', l9_mul),
    ('number-sense/fluency-l9-negative-times-negative', 'divide-two', l9_div),
    ('number-sense/fluency-l9-negative-times-negative', 'multiply-three', l9_three),
    ('number-sense/fluency-l12-which-first', 'times-before-plus', l12_times),
    ('number-sense/fluency-l12-which-first', 'powers-next', l12_powers),
    ('number-sense/fluency-l12-which-first', 'brackets-first', l12_brackets),
    ('number-sense/fluency-l12-which-first', 'left-to-right', l12_ltr),
]


# ==== Level 4 (fluency and problems number-sense 4) =================================================
# Method 2 here is sympy (factorint, divisor_count, igcd, ilcm) and exact fractions, worked from the drawn
# vars alone; the circle families are also probed with pi = 3.14 and 22/7 at the asked rounding.
import sympy as sp
from math import pi as PI

SETS4 = {}


def wtol(ref, fam, wid):
    """A wrong entry's own tol, read from the set file (the sampler does not print it)."""
    if ref not in SETS4:
        SETS4[ref] = json.load(open(os.path.join(APP, 'content', 'courses', *ref.split('/')) + '.json'))
    f = next(x for x in SETS4[ref]['families'] if x['id'] == fam)
    w = next(x for x in f['wrong'] if x['id'] == wid)
    return float((w.get('tol') or {}).get('abs', 0))


def item4(it, ref, key, slips, tol=0.0, text_has=()):
    """key and slips worked here; slips: {id: value or None when the slip must not be offered}."""
    tag = f"{it['family']} seed {it['seed']}"
    check(abs(float(num(it['answer'])) - float(key)) <= 1e-9 * max(1, abs(float(key))), f"{tag}: key {it['answer']} is {float(key)}")
    want = {k for k, v in slips.items() if v is not None}
    got = {w['id']: float(num(w['value'])) for w in it['wrong']}
    check(set(got) == want, f"{tag}: slips offered {sorted(got)} are {sorted(want)}")
    for wid, v in got.items():
        wt = wtol(ref, it['family'], wid)
        if wid in want:
            check(abs(v - float(slips[wid])) <= 1e-9 * max(1, abs(v)), f"{tag}: slip {wid} = {v} is {float(slips[wid])}")
        check(abs(v - float(key)) > tol + wt, f"{tag}: slip {wid} lies outside the key band")
    ids = list(got)
    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            a, b = ids[i], ids[j]
            check(abs(got[a] - got[b]) > wtol(ref, it['family'], a) + wtol(ref, it['family'], b),
                  f"{tag}: slips {a} and {b} do not overlap")
    for s in text_has:
        check(s in it['prompt'] or any(s in x for x in it['solution']), f"{tag}: {s!r} appears in the prompt or working")


R15 = 'number-sense/fluency-l15-building-blocks'


def n15(V):
    n = int(V['nn'])
    fa = sp.factorint(n)
    exps = {p: int(V['e' + str(p)]) for p in (2, 3, 5, 7, 11, 13)}
    check({p: e for p, e in exps.items() if e} == fa, f"l15 {n}: tuple indices are the prime factors {fa}")
    tex = ' \\times '.join(f'{p}^{e}' if e > 1 else f'{p}' for p, e in sorted(fa.items()))
    check(V['ptex'] == tex, f"l15 {n}: index form {V['ptex']} is {tex}")
    return n, fa


def l15_largest(it, V):
    n, fa = n15(V)
    lp, spf = max(fa), min(fa)
    big = n // spf
    pp = lp ** fa[lp]
    item4(it, R15, lp, {'largest-factor': big, 'prime-power': pp if fa[lp] > 1 and pp != big else None},
          text_has=[f"{n} = {V['ptex']}"])


def l15_from_primes(it, V):
    n, fa = n15(V)
    key = sp.divisor_count(n)
    mul = int(sp.prod(fa.values()))
    add = sum(e + 1 for e in fa.values())
    check(key == len(sp.divisors(n)), f"l15 {n}: divisor count by listing")
    item4(it, R15, key, {'indices-multiplied': mul if mul != add else None, 'indices-added': add if add != key else None})


def l15_count(it, V):
    n, fa = n15(V)
    key = len([d for d in range(1, n + 1) if n % d == 0])
    check(key == sp.divisor_count(n), f"l15 {n}: trial division agrees with sympy")
    pairs = (key + 1) // 2
    check(pairs == len([d for d in range(1, n + 1) if n % d == 0 and d * d <= n]), f"l15 {n}: factor pairs counted")
    mul = int(sp.prod(fa.values()))
    item4(it, R15, key, {'pairs': pairs if pairs != mul else None, 'no-plus-one': mul})


R16 = 'number-sense/fluency-l16-shared-factors'


def n16(V):
    g, p, a, b = int(V['g']), int(V['p']), int(V['a']), int(V['b'])
    check(p == min(sp.factorint(g)) and sp.igcd(a, b) == 1 and a < b, f"l16 g={g}: smallest prime {p}, a and b coprime")
    m, n = g * a, g * b
    check(sp.igcd(m, n) == g and sp.ilcm(m, n) == g * a * b, f"l16 {m},{n}: HCF {g}, LCM {g * a * b}")
    return g, p, m, n


def l16_hcf(it, V):
    g, p, m, n = n16(V)
    key = max(d for d in range(1, m + 1) if m % d == 0 and n % d == 0)
    item4(it, R16, key, {'lcm': sp.ilcm(m, n), 'one-prime': p if g != p else None}, text_has=[f"${m}$ and ${n}$"])


def l16_lcm(it, V):
    g, p, m, n = n16(V)
    key = next(k for k in range(n, m * n + 1, n) if k % m == 0)
    item4(it, R16, key, {'product': m * n, 'hcf': g}, text_has=[f"${m}$ and ${n}$"])


def l16_other(it, V):
    g, p, m, n = n16(V)
    l = sp.ilcm(m, n)
    cands = [x for x in range(1, g * l + 1) if sp.igcd(m, x) == g and sp.ilcm(m, x) == l]
    check(cands == [n], f"l16 other {m}: the only number with HCF {g} and LCM {l} is {n} ({cands})")
    a, b = m // g, n // g
    item4(it, R16, n, {'lcm-over-hcf': l // g if a != g else None, 'product': g * l}, text_has=[f"${m}$", f"${g}$", f"${l}$"])


R17 = 'number-sense/fluency-l17-around-and-inside'


def shoelace(pts):
    return abs(sum(F(x1) * y2 - F(x2) * y1 for (x1, y1), (x2, y2) in zip(pts, pts[1:] + pts[:1]))) / 2


def l17_tri(it, V):
    b, h, k = (int(V[x]) for x in 'bhk')
    s = h + k
    key = F(b * h, 2)
    shoe = shoelace([(0, 0), (b, 0), (F(b, 3), h)])
    check(shoe == key, f"tri {b},{h}: shoelace area {shoe}")
    item4(it, R17, key, {'no-half': b * h, 'sloping-side': F(b * s, 2) if s != 2 * h else None},
          text_has=[f"base ${b}$ cm", f"side of ${s}$ cm", f"height ${h}$ cm"])


def l17_para(it, V):
    b, h, k = (int(V[x]) for x in 'bhk')
    s = h + k
    shoe = shoelace([(0, 0), (b, 0), (b + 2, h), (2, h)])
    check(shoe == b * h, f"para {b},{h}: shoelace area {shoe}")
    item4(it, R17, b * h, {'slant-side': b * s, 'halved': F(b * h, 2)}, text_has=[f"base ${b}$ cm", f"slant side ${s}$ cm"])


def l17_trap(it, V):
    a, d, h = (int(V[x]) for x in 'adh')
    c = a + d
    key = F((a + c) * h, 2)
    shoe = shoelace([(0, 0), (c, 0), (a + 1, h), (1, h)])
    check(shoe == key, f"trap {a},{c},{h}: shoelace {shoe}")
    item4(it, R17, key, {'no-half': (a + c) * h, 'longer-side': c * h}, text_has=[f"${a}$ m and ${c}$ m"])


def l17_l(it, V):
    w, t, p, q = (int(V[x]) for x in 'wtpq')
    cells = sum(1 for i in range(w) for j in range(t) if not (i >= w - p and j >= t - q))
    check(cells == w * t - p * q, f"L {w}x{t} cut {p}x{q}: {cells} unit squares")
    item4(it, R17, cells, {'corner-kept': w * t, 'corner-added': w * t + p * q})


R18 = 'number-sense/fluency-l18-circles-and-units'


def pi_probe(tag, true, tol, dp, f):
    for approx in (3.14, 22 / 7):
        v = round(f(approx), dp)
        check(abs(v - true) <= tol, f"{tag}: the value with pi = {approx:.4f}, {v}, is accepted")
    check(abs(round(true, dp) - true) <= tol, f"{tag}: the value at {dp} dp is accepted")


def l18_circ(it, V):
    k, m = int(V['k']), int(V['m'])
    d = F(2 * m) if k == 1 else F(m)
    r = d / 2
    key = sp.N(sp.pi * sp.Rational(d), 15)
    tag = f"circ {V['word']} {m}"
    check(abs(float(key) - 2 * PI * float(r)) < 1e-9, f"{tag}: pi d is 2 pi r")
    pi_probe(tag, float(key), 0.15, 1, lambda P: P * float(d))
    area = PI * float(r) ** 2
    swap = PI * (m if k == 1 else 2 * m)
    item4(it, R18, float(key), {'area-rule': area if abs(area - float(key)) > 1 and abs(area - swap) > 1 else None,
                                 'radius-diameter': swap}, tol=0.15)


def l18_area(it, V):
    k, m = int(V['k']), int(V['m'])
    r = F(m) if k == 1 else F(m, 2)
    key = float(sp.N(sp.pi * sp.Rational(r) ** 2, 15))
    tag = f"area {V['word']} {m}"
    pi_probe(tag, key, 0.2, 1, lambda P: P * float(r) ** 2)
    circ = 2 * PI * float(r)
    item4(it, R18, key, {'diameter-squared': PI * m * m if k == 2 else None,
                         'circumference': circ if abs(key - circ) > 1 else None}, tol=0.2)


def l18_speed(it, V):
    x, dr = int(V['x']), int(V['dir'])
    if dr == 1:
        key = sp.Rational(x * 1000, 3600)
        check(abs(float(key) - x / 3.6) < 1e-9, f"speed {x}: x / 3.6")
        slips = {'wrong-way': sp.Rational(x * 36, 10), 'minutes': sp.Rational(x * 1000, 60)}
    else:
        key = sp.Rational(x * 3600, 1000)
        check(abs(float(key) - x * 3.6) < 1e-9, f"speed {x}: x * 3.6")
        slips = {'wrong-way': sp.Rational(x * 1000, 3600), 'minutes': sp.Rational(x * 60, 1000)}
    check(abs(round(float(key), 1) - float(key)) <= 0.05, f"speed {x}: 1 dp value accepted")
    item4(it, R18, key, slips, tol=0.05)


def l18_units(it, V):
    n = int(V['n'])
    a = F(n, 10)
    key = a * 100 * 100
    check(key == n * 1000, f"units {n}: {a} m2 is {n * 1000} cm2")
    check(f"${n}{{,}}000$" in it['solution'][1], f"units {n}: working writes {n},000")
    item4(it, R18, key, {'length-only': a * 100, 'divided': a / 10000})


R19 = 'number-sense/fluency-l19-one-number-for-many'


def shown_list(it):
    return [F(int(z)) for z in re.findall(r'\$(-?\d+)\$', it['prompt'])]


def l19_mean(it, V):
    vals = shown_list(it)
    check(len(vals) == 5 and sum(1 for v in vals if v < 0) >= 1, f"mean seed {it['seed']}: five values, a loss among them")
    key = sum(vals) / 5
    check(key == int(V['m']), f"mean seed {it['seed']}: mean {key}")
    a = F(int(V['a']))
    pos = (sum(vals) - 2 * a) / 5
    item4(it, R19, key, {'divided-by-four': sum(vals) / 4, 'loss-added': pos if pos != sum(vals) / 4 else None})


def l19_median(it, V):
    vals = shown_list(it)
    check(len(vals) == 5 and len(set(vals)) == 5, f"median seed {it['seed']}: five different values")
    key = sorted(vals)[2]
    mean = sum(vals) / 5
    item4(it, R19, key, {'unsorted': vals[2] if vals[2] != key else None,
                         'mean': mean if mean != key and mean != vals[2] else None})


def l19_range(it, V):
    vals = shown_list(it)
    check(len(vals) == 5 and min(vals) < 0 < max(vals), f"range seed {it['seed']}: a loss and a profit")
    key = max(vals) - min(vals)
    fl = abs(vals[4] - vals[0])
    lost = max(vals) + min(vals)
    item4(it, R19, key, {'first-last': fl if fl != key and fl != lost else None, 'sign-lost': lost if lost != key else None})


def l19_table(it, V):
    f = [int(V['f' + str(i)]) for i in range(5)]
    data = [v for v in range(5) for _ in range(f[v])]
    key = F(sum(data), len(data))
    check(f"${len(data)}$" in it['prompt'], f"table seed {it['seed']}: the count {len(data)} is stated")
    check(abs(round(float(key), 2) - float(key)) <= 0.01, f"table seed {it['seed']}: 2 dp accepted")
    item4(it, R19, key, {'values-only': F(2), 'rows': F(sum(data), 5)}, tol=0.01)


JOBS += [
    (R15, 'largest-prime', l15_largest), (R15, 'count-from-primes', l15_from_primes), (R15, 'count-factors', l15_count),
    (R16, 'hcf', l16_hcf), (R16, 'lcm', l16_lcm), (R16, 'other-number', l16_other),
    (R17, 'triangle-area', l17_tri), (R17, 'parallelogram-area', l17_para), (R17, 'trapezium-area', l17_trap), (R17, 'l-shape-area', l17_l),
    (R18, 'circumference', l18_circ), (R18, 'circle-area', l18_area), (R18, 'speed-units', l18_speed), (R18, 'area-units', l18_units),
    (R19, 'mean', l19_mean), (R19, 'median', l19_median), (R19, 'range', l19_range), (R19, 'table-mean', l19_table),
]

for ref, fam, fn in JOBS:
    run(ref, fam, fn)
print(f"{len(JOBS)} families, {N} draws each, {count} checks")
lv.report()
