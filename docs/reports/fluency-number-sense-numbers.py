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

for ref, fam, fn in JOBS:
    run(ref, fam, fn)
print(f"{len(JOBS)} families, {N} draws each, {count} checks")
lv.report()
