"""Recompute every Fluency family of the taylor course from the drawn variables alone (docs/briefs/fluency.md check 1).

Run from anywhere with a Python that has sympy:
    <scratchpad>/venv/bin/python docs/reports/fluency-taylor-numbers.py [--n 200]
For each family it reads `node tools/fluency-sample.mjs --set taylor/<set> --family <id> --n N --json`, derives the key
again with sympy from `vars` only (never from the printed answer or lets), checks it equals the engine's resolved
answer, and checks each `wrong` equals the slip recomputed from the vars and differs from the key (numeric: by more
than the key's tolerance). Exit 0 when all agree.
"""
import json
import math
import os
import subprocess
import sys

import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

APP = os.environ.get('FLUENCY_APP') or os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app')
N = int(sys.argv[sys.argv.index('--n') + 1]) if '--n' in sys.argv else 200
x, t = sp.symbols('x t')
SYM = {'x': x, 't': t}
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
    out = subprocess.run(['node', 'tools/fluency-sample.mjs', '--set', 'taylor/' + set_id, '--family', fam,
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
        assert set(w['id'] for w in it['wrong']) == set(wrongs), (label, [w['id'] for w in it['wrong']])
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


# ---- fluency-l1-tangent-approx ----
def l1_line(V):
    f = V['p'] * x ** 3 + V['q'] * x ** 2 + V['r'] * x + V['s']
    a = V['a']
    fa, fpa = f.subs(x, a), sp.diff(f, x).subs(x, a)
    L = sp.expand(fa + fpa * (x - a))
    return L, {'slope-at-x': fa + sp.diff(f, x) * (x - a), 'swapped': fpa + fa * (x - a)}


def l1_power(V):
    f = V['c'] * x ** V['n']
    a, h = V['a'], V['h']
    fa, fpa = f.subs(x, a), sp.diff(f, x).subs(x, a)
    return fa + fpa * h, {'calculator': f.subs(x, a + h), 'no-step': fa, 'used-x': fa + fpa * (a + h)}


def l1_root(V):
    s, h = V['s'], V['h']
    a, x0 = s ** 2, s ** 2 + R(h, 20)
    slope = sp.diff(sp.sqrt(x), x).subs(x, a)
    key = sp.sqrt(a) + slope * (x0 - a)
    return key, {'calculator': math.sqrt(float(x0)), 'no-step': sp.sqrt(a), 'slope-not-halved': sp.sqrt(a) + 2 * slope * (x0 - a)}


# ---- fluency-l6-matching-derivatives: c_k = f^(k)(a)/k!, from sympy's k-th derivative ----
def taylor_coeff(f, v, a, k):
    return sp.diff(f, v, k).subs(v, a) / sp.factorial(k)


def l6_exp(V):
    v = SYM[V['v']]
    c, m, k = V['c'], V['m'], V['k']
    f = c * sp.exp(m * v)
    key = taylor_coeff(f, v, 0, k)
    assert key == sp.series(f, v, 0, k + 1).removeO().coeff(v, k)
    return key, {'no-factorial': sp.diff(f, v, k).subs(v, 0), 'chain-forgotten': taylor_coeff(c * sp.exp(v), v, 0, k)}


def l6_trig(V):
    v = SYM[V['v']]
    c, m, k = V['c'], V['m'], V['k']
    g = {'sin': sp.sin, 'cos': sp.cos}[V['fn']]
    assert (V['fn'] == 'sin') == (k % 2 == 1)
    f = c * g(m * v)
    key = taylor_coeff(f, v, 0, k)
    assert key == sp.series(f, v, 0, k + 1).removeO().coeff(v, k)
    return key, {'no-factorial': sp.diff(f, v, k).subs(v, 0), 'sign-lost': -key,
                 'chain-forgotten': taylor_coeff(c * g(v), v, 0, k)}


def l6_cubic(V):
    a = V['a']
    f = V['p'] * x ** 3 + V['q'] * x ** 2 + V['r'] * x + V['s']
    key = taylor_coeff(f, x, a, 2)
    y = sp.symbols('y')
    assert key == sp.expand(f.subs(x, y + a)).coeff(y, 2)
    return key, {'not-halved': sp.diff(f, x, 2).subs(x, a), 'at-zero': taylor_coeff(f, x, 0, 2)}


def l6_exp_a(V):
    v = SYM[V['v']]
    c, a, k = V['c'], V['a'], V['k']
    f = c * sp.exp(v)
    key = taylor_coeff(f, v, a, k)
    return key, {'at-x': sp.diff(f, v, k) / sp.factorial(k), 'no-factorial': sp.diff(f, v, k).subs(v, a)}


FAMILIES = [
    ('fluency-l6-matching-derivatives', 'exponential-coefficient', l6_exp),
    ('fluency-l6-matching-derivatives', 'trig-coefficient', l6_trig),
    ('fluency-l6-matching-derivatives', 'centred-cubic', l6_cubic),
    ('fluency-l6-matching-derivatives', 'exponential-about-a', l6_exp_a),
    ('fluency-l1-tangent-approx', 'write-the-line', l1_line),
    ('fluency-l1-tangent-approx', 'estimate-a-power', l1_power),
    ('fluency-l1-tangent-approx', 'estimate-a-root', l1_root),
]

if __name__ == '__main__':
    for set_id, fam, fn in FAMILIES:
        check(set_id, fam, fn)
    for f in fails[:30]:
        print('FAIL', f)
    print('%d checks over %d families, %d failures' % (checked, len(FAMILIES), len(fails)))
    sys.exit(1 if fails else 0)
