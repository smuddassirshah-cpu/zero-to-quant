"""Recompute every Fluency family of the multivar course from the drawn variables alone (docs/briefs/fluency.md check 1).

Run from anywhere with a Python that has sympy:
    <scratchpad>/venv/bin/python docs/reports/fluency-multivar-numbers.py [--n 200]
For each family it reads `node tools/fluency-sample.mjs --set multivar/<set> --family <id> --n N --json`, derives the key
again with sympy from `vars` only (never from the printed answer or lets), checks it equals the engine's resolved
answer, and checks each `wrong` equals the slip recomputed from the vars and differs from the key (numeric: by more
than the key's tolerance). Exit 0 when all agree.
"""
import json
import os
import subprocess
import sys

import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

APP = os.environ.get('FLUENCY_APP') or os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app')
N = int(sys.argv[sys.argv.index('--n') + 1]) if '--n' in sys.argv else 200
x, y = sp.symbols('x y')
SYM = {'x': x, 'y': y}
R = sp.Rational
fails = []
checked = 0


# ---- a small LaTeX reader for the shapes these sets print ----
def _group(s, i):
    assert s[i] == '{', (s, i)
    depth, j = 0, i
    while True:
        if s[j] == '{':
            depth += 1
        elif s[j] == '}':
            depth -= 1
            if depth == 0:
                return s[i + 1:j], j + 1
        j += 1


def tex2py(s):
    out, i = [], 0
    while i < len(s):
        if s.startswith('\\dfrac', i) or s.startswith('\\frac', i):
            i += 6 if s.startswith('\\dfrac', i) else 5
            a, i = _group(s, i)
            b, i = _group(s, i)
            out.append(' ((%s)/(%s)) ' % (tex2py(a), tex2py(b)))
        elif s.startswith('e^', i):
            i += 2
            if s[i] == '{':
                a, i = _group(s, i)
            else:
                a, i = s[i], i + 1
            out.append(' exp(%s) ' % tex2py(a))
        elif s[i] == '^':
            i += 1
            if s[i] == '{':
                a, i = _group(s, i)
            else:
                a, i = s[i], i + 1
            out.append('**(%s) ' % tex2py(a))
        elif s[i] == '{':
            a, i = _group(s, i)
            out.append('(%s)' % tex2py(a))
        else:
            c = s[i]
            out.append(' %s ' % c if c.isalpha() else c)
            i += 1
    return ''.join(out)


def parse(s):
    return parse_expr(tex2py(s), local_dict=dict(SYM, exp=sp.exp),
                      transformations=standard_transformations + (implicit_multiplication_application,))


def same(a, b):
    return sp.simplify(sp.expand(a - b)) == 0


def sample(set_id, fam):
    out = subprocess.run(['node', 'tools/fluency-sample.mjs', '--set', 'multivar/' + set_id, '--family', fam,
                          '--n', str(N), '--json'], cwd=APP, capture_output=True, text=True, check=True).stdout
    return json.loads(out)['items']


def check(set_id, fam, derive):
    """derive(vars) -> (key, {wrong_id: value}). Expression keys are sympy expressions; numeric keys are numbers."""
    global checked
    items = sample(set_id, fam)
    assert len(items) == N, (set_id, fam, len(items))
    for it in items:
        V = {k: (sp.nsimplify(v, rational=True) if isinstance(v, (int, float)) else v) for k, v in it['vars'].items()}
        key, wrongs = derive(V)
        label = '%s/%s seed %s' % (set_id, fam, it['seed'])
        if it['kind'] == 'numeric':
            tol = (it.get('tol') or {}).get('abs', 0)
            ok = abs(float(it['answer']) - float(key)) <= 1e-8
        else:
            tol = None
            ok = same(parse(it['answer']), key)
        checked += 1
        if not ok:
            fails.append('%s: key %s, engine %s' % (label, key, it['answer']))
        if set(w['id'] for w in it['wrong']) != set(wrongs):
            fails.append('%s: offered %s, expected %s' % (label, [w['id'] for w in it['wrong']], sorted(wrongs)))
            continue
        for w in it['wrong']:
            want = wrongs[w['id']]
            if it['kind'] == 'numeric':
                wv = float(w['value'])
                okw = abs(wv - float(want)) <= 1e-8 and abs(wv - float(key)) > tol
            else:
                wv = parse(w['tex'])
                okw = same(wv, want) and not same(wv, key)
            checked += 1
            if not okw:
                fails.append('%s: wrong %s, expected %s, engine %s' % (label, w['id'], want, w.get('tex', w.get('value'))))


# ---- fluency-l1-two-inputs ----
def l1_level(V):
    a, b, e, p, q = V['a'], V['b'], V['e'], V['p'], V['q']
    f = lambda X, Y: a * X ** 2 + b * X * Y + e * Y ** 2
    # the slip: a negative coordinate squared to a negative number, -(|p|^2)
    sq = lambda z: -(z * z) if z < 0 else z * z
    return f(p, q), {'negative-square': a * sq(p) + b * p * q + e * sq(q), 'swapped': f(q, p)}


def l1_walk(V):
    a, b, d = V['a'], V['b'], V['d']
    dy = sp.symbols('dy')
    r = sp.solve(sp.Eq(a * d + b * dy, 0), dy)[0]
    assert sp.expand(a * (x + d) + b * (y + r) - (a * x + b * y)) == 0
    return r, {'sign-lost': -r, 'upside-down': sp.solve(sp.Eq(b * d + a * dy, 0), dy)[0]}


def l1_point(V):
    aa, bb, k, p = V['aa'], V['bb'], V['k'], V['p']
    f = y + aa * x ** 2 + bb * x
    Y = sp.solve(sp.Eq(f.subs(x, p), k), y)[0]
    return Y, {'signs-not-changed': k + aa * p ** 2 + bb * p, 'one-term-moved': k - aa * p ** 2}


# ---- fluency-l3-second-partials ----
def l3_first(V):
    f = V['c'] * x ** V['m'] * y ** V['n'] + V['b'] * x ** V['p'] + V['e'] * y ** V['q']
    fy = sp.diff(f, y)
    return fy, {'x-term-differentiated': fy + sp.diff(V['b'] * x ** V['p'], x),
                'x-factor-dropped': sp.diff(f, y).subs(x, 1)}


def l3_bend(V):
    f = V['c'] * x ** 3 * y ** V['n'] + V['b'] * x ** 4 + V['e'] * y ** V['q']
    pt = {x: V['x0'], y: V['y0']}
    return sp.diff(f, x, 2).subs(pt), {'stopped-at-first': sp.diff(f, x).subs(pt),
                                      'mixed-instead': sp.diff(f, x, y).subs(pt)}


def l3_mixed(V):
    f = V['c'] * x ** V['m'] * y ** V['n'] + V['b'] * x ** V['p'] + V['e'] * y ** V['q']
    fxy = sp.diff(f, x, y)
    assert fxy == sp.diff(f, y, x)
    term = V['c'] * x ** V['m'] * y ** V['n']
    return fxy, {'product-of-partials': sp.diff(f, x) * sp.diff(f, y),
                 'pure-term-kept': fxy + sp.diff(V['b'] * x ** V['p'], x),
                 'power-not-lowered': sp.diff(term, x, y) * y}


# ---- fluency-l2-slicing (widening pass): hold one input fixed and differentiate in the other ----
def l2_fx(V):
    f = V['c'] * x ** V['m'] * y ** V['n'] + V['b'] * x ** V['p'] + V['e'] * y ** V['q']
    fx = sp.diff(f, x)
    return fx, {'y-term-kept': fx + V['e'] * y ** V['q'], 'y-dropped': fx.subs(y, 1)}


def l2_point(V):
    f = V['c'] * x ** V['m'] * y ** V['n'] + V['b'] * x ** V['p'] + V['e'] * y ** V['q']
    pt = {x: V['x0'], y: V['y0']}
    key = sp.diff(f, y).subs(pt)
    slips = {}
    if sp.diff(f, x).subs(pt) != key:
        slips['f-x'] = sp.diff(f, x).subs(pt)
    if f.subs(pt) != key:
        slips['height'] = f.subs(pt)
    return key, slips


def l2_exp(V):
    f = V['c'] * sp.exp(V['k'] * x ** V['m'] * y ** V['n'])
    return sp.diff(f, x), {'no-chain': f, 'wrong-variable': sp.diff(f, y)}


def l2_log(V):
    f = sp.log(V['a'] * x ** 2 + V['b'] * y ** 2)
    pt = {x: V['x0'], y: V['y0']}
    key = sp.diff(f, y).subs(pt)
    slips = {}
    fxv = sp.diff(f, x).subs(pt)
    nochain = (1 / (V['a'] * x ** 2 + V['b'] * y ** 2)).subs(pt)
    if abs(fxv - key) > R(1, 1000):
        slips['f-x'] = fxv
    if abs(nochain - key) > R(1, 1000):
        slips['no-chain'] = nochain
    return key, slips


FAMILIES = [
    ('fluency-l2-slicing', 'partial-x', l2_fx),
    ('fluency-l2-slicing', 'partial-y-at-a-point', l2_point),
    ('fluency-l2-slicing', 'exponential-x', l2_exp),
    ('fluency-l2-slicing', 'log-at-a-point', l2_log),
    ('fluency-l1-two-inputs', 'contour-through-a-point', l1_level),
    ('fluency-l1-two-inputs', 'walk-along-a-contour', l1_walk),
    ('fluency-l1-two-inputs', 'point-on-a-contour', l1_point),
    ('fluency-l3-second-partials', 'first-partial', l3_first),
    ('fluency-l3-second-partials', 'bend-at-a-point', l3_bend),
    ('fluency-l3-second-partials', 'mixed-partial', l3_mixed),
]

if __name__ == '__main__':
    for set_id, fam, fn in FAMILIES:
        check(set_id, fam, fn)
    for f in fails[:30]:
        print('FAIL', f)
    print('%d checks over %d families, %d failures' % (checked, len(FAMILIES), len(fails)))
    sys.exit(1 if fails else 0)
