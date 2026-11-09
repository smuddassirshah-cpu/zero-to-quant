"""Fluency sets of the integrals course: every drawn answer and every named slip, computed twice.

Run from the repository root with the venv that has sympy:
    <venv>/bin/python -I docs/reports/fluency-integrals-numbers.py
For each family it reads 200 draws from `node tools/fluency-sample.mjs --set integrals/<set> --family <id> --n 200 --json`.
Route 1 is the engine's resolved answer. Route 2 is sympy, working from the drawn variable values only (never the lets
or the printed answer): it builds the integrand, integrates it (or evaluates the definite integral exactly), and then
  - an expression answer must differ from sympy's antiderivative by a constant (checked at five points), and every
    `wrong` tex must not;
  - a numeric answer must equal sympy's exact value, and every `wrong` value must lie outside the key's tolerance and
    equal the slip recomputed here from the variables.
For partial fractions the prompt's numerator is also read back and split with sympy's apart.
Exit 0 when every check passes.
"""
import json
import os
import re
import subprocess
import sys

import sympy as sp

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
APP = os.path.join(ROOT, 'app')
N = 200
X = sp.Symbol('X', real=True)
POINTS = [sp.Rational(37, 100), sp.Rational(91, 100), sp.Rational(161, 100), sp.Rational(223, 100), sp.Rational(283, 100)]
fails = []
checks = 0


def check(ok, msg):
    global checks
    checks += 1
    if not ok:
        fails.append(msg)


def sample(set_id, fam):
    out = subprocess.run(['node', 'tools/fluency-sample.mjs', '--set', f'integrals/{set_id}', '--family', fam,
                          '--n', str(N), '--json'], cwd=APP, capture_output=True, text=True, check=True).stdout
    return json.loads(out)['items']


# ---------- a small LaTeX reader for the shapes these sets print ----------
def _group(s, i):
    """s[i] == '{': return (inside, index after the closing brace)"""
    depth = 0
    for j in range(i, len(s)):
        if s[j] == '{':
            depth += 1
        elif s[j] == '}':
            depth -= 1
            if depth == 0:
                return s[i + 1:j], j + 1
    raise ValueError('unbalanced braces in ' + s)


def to_py(s):
    out, i = '', 0
    while i < len(s):
        if s.startswith('\\frac', i):
            a, j = _group(s, i + 5)
            b, j = _group(s, j)
            out += f'(({to_py(a)})/({to_py(b)}))'
            i = j
        elif s.startswith('\\ln|', i):
            j = s.index('|', i + 4)
            out += f' log(Abs({to_py(s[i + 4:j])}))'
            i = j + 1
        elif s.startswith('\\ln', i) or s.startswith('\\sin', i) or s.startswith('\\cos', i):
            name = 'log' if s.startswith('\\ln', i) else s[i + 1:i + 4]
            i += 3 if name == 'log' else 4
            while i < len(s) and s[i] == ' ':
                i += 1
            if s[i] == '(':
                out += ' ' + name
            else:   # \ln x: one letter
                out += f' {name}({s[i]})'
                i += 1
        elif s.startswith('e^', i):
            if s[i + 2] == '{':
                a, j = _group(s, i + 2)
            else:
                a, j = s[i + 2], i + 3
            out += f' exp({to_py(a)})'
            i = j
        elif s[i] == '^':
            if s[i + 1] == '{':
                a, j = _group(s, i + 1)
            else:
                a, j = s[i + 1], i + 2
            out += f'**({to_py(a)})'
            i = j
        elif s[i].isalpha():
            out += ' ' + s[i] + ' '
            i += 1
        else:
            out += s[i]
            i += 1
    return out


TRANS = sp.parsing.sympy_parser.standard_transformations + (sp.parsing.sympy_parser.implicit_multiplication_application,)


def parse(tex, letter):
    py = to_py(tex)
    return sp.parsing.sympy_parser.parse_expr(py, local_dict={letter: X, 'log': sp.log, 'exp': sp.exp, 'sin': sp.sin,
                                                               'cos': sp.cos, 'Abs': sp.Abs}, transformations=TRANS)


def diffs(expr, ref):
    return [sp.N((expr - ref).subs(X, p), 30) for p in POINTS]


def same_up_to_constant(expr, ref):
    d = diffs(expr, ref)
    return all(abs(complex(v - d[0])) < 1e-12 for v in d)


def expr_family(set_id, fam, integrand, antideriv=None):
    """integrand(vars) -> sympy in X; antideriv(vars) optional (else sympy integrate)"""
    items = sample(set_id, fam)
    for it in items:
        v = it['vars']
        letter = v.get('v', 'x')
        f = integrand(v)
        ref = antideriv(v) if antideriv else sp.integrate(f, X)
        check(sp.simplify(sp.diff(ref, X) - f) == 0 or all(abs(complex(sp.N((sp.diff(ref, X) - f).subs(X, p)))) < 1e-12 for p in POINTS),
              f'{set_id}/{fam} seed {it["seed"]}: reference antiderivative wrong')
        key = parse(it['answer'], letter)
        check(it.get('upToConstant') is True, f'{set_id}/{fam}: upToConstant not set')
        check(same_up_to_constant(key, ref), f'{set_id}/{fam} seed {it["seed"]}: key {it["answer"]} is not an antiderivative of {f}')
        for w in it['wrong']:
            wexpr = parse(w['tex'], letter)
            check(not same_up_to_constant(wexpr, ref), f'{set_id}/{fam} seed {it["seed"]}: wrong {w["id"]} {w["tex"]} equals the key')
        ws = [parse(w['tex'], letter) for w in it['wrong']]
        for i in range(len(ws)):
            for j in range(i + 1, len(ws)):
                check(not same_up_to_constant(ws[i], ws[j]), f'{set_id}/{fam} seed {it["seed"]}: two wrongs coincide')
    return len(items)


def num_family(set_id, fam, exact, slips):
    """exact(vars) -> Rational; slips(vars) -> {wrong id: Rational}"""
    items = sample(set_id, fam)
    for it in items:
        v = it['vars']
        e = sp.nsimplify(exact(v))
        got = sp.Rational(str(it['answer'])) if re.fullmatch(r'-?\d+(/\d+)?', str(it['answer'])) else sp.nsimplify(float(it['answer']), rational=True, tolerance=1e-12)
        check(abs(float(got) - float(e)) < 1e-9, f'{set_id}/{fam} seed {it["seed"]}: answer {it["answer"]} but sympy gives {e}')
        tol = (it.get('tol') or {}).get('abs', 0)
        mine = slips(v)
        seen = []
        for w in it['wrong']:
            wv = float(w['value'])
            check(w['id'] in mine, f'{set_id}/{fam}: wrong {w["id"]} not recomputed here')
            if w['id'] in mine:
                check(abs(wv - float(mine[w['id']])) < 1e-9, f'{set_id}/{fam} seed {it["seed"]}: wrong {w["id"]} {wv} but here {mine[w["id"]]}')
            check(abs(wv - float(e)) > tol + 1e-9, f'{set_id}/{fam} seed {it["seed"]}: wrong {w["id"]} inside the key tolerance')
            for s in seen:
                check(abs(wv - s) > tol + 1e-9, f'{set_id}/{fam} seed {it["seed"]}: two wrongs coincide')
            seen.append(wv)
    return len(items)


R = sp.Rational
I = lambda f, p, q: sp.integrate(f, (X, p, q))   # noqa: E731
counts = {}

# ---------- fluency-l6-working-backwards ----------
S = 'fluency-l6-working-backwards'
counts[S + '/power'] = expr_family(S, 'power', lambda v: v['a'] * X**v['k'])
counts[S + '/polynomial'] = expr_family(S, 'polynomial', lambda v: 3 * v['p'] * X**2 + 2 * v['q'] * X + v['c'])
counts[S + '/negative-power'] = expr_family(S, 'negative-power', lambda v: v['m'] * (v['k'] - 1) * X**(-v['k']))


def fixc(v):
    f = v['m'] * (v['k'] + 1) * X**v['k']
    F = sp.integrate(f, X)
    C = v['q0'] - F.subs(X, v['p'])
    return F.subs(X, v['r']) + C


def fixc_slips(v):
    f = v['m'] * (v['k'] + 1) * X**v['k']
    F = sp.integrate(f, X)
    nodiv = f * X   # raised the power, kept the coefficient
    return {'no-constant': F.subs(X, v['r']), 'no-divide': v['q0'] + nodiv.subs(X, v['r']) - nodiv.subs(X, v['p'])}


counts[S + '/fix-constant'] = num_family(S, 'fix-constant', fixc, fixc_slips)

# ---------- fluency-l7-evaluating ----------
S = 'fluency-l7-evaluating'


def pw(v):
    return I(v['m'] * (v['k'] + 1) * X**v['k'], v['p'], v['q'])


counts[S + '/power'] = num_family(S, 'power', pw, lambda v: {
    'limits-swapped': I(v['m'] * (v['k'] + 1) * X**v['k'], v['q'], v['p']),
    'no-divide': (v['m'] * (v['k'] + 1) * X**(v['k'] + 1)).subs(X, v['q']) - (v['m'] * (v['k'] + 1) * X**(v['k'] + 1)).subs(X, v['p'])})


def quad_f(v):
    return v['a'] * X**2 + 2 * v['h'] * X + v['c']


def quad_nodiv(v):
    G = v['a'] * X**3 + 2 * v['h'] * X**2 + v['c'] * X
    return G.subs(X, v['q']) - G.subs(X, v['p'])


counts[S + '/quadratic'] = num_family(S, 'quadratic', lambda v: I(quad_f(v), v['p'], v['q']),
                                      lambda v: {'limits-swapped': I(quad_f(v), v['q'], v['p']), 'no-divide': quad_nodiv(v)})
counts[S + '/reciprocal-square'] = num_family(S, 'reciprocal-square', lambda v: I(v['c'] / X**2, v['p'], v['q']), lambda v: {
    'sign-lost': I(v['c'] / X**2, v['q'], v['p']),
    'power-lowered': (-v['c'] / (3 * X**3)).subs(X, v['q']) - (-v['c'] / (3 * X**3)).subs(X, v['p'])})

# ---------- fluency-l9-undo-chain ----------
S = 'fluency-l9-undo-chain'
counts[S + '/power-inside'] = expr_family(S, 'power-inside', lambda v: v['k'] * X * (X**2 + v['b'])**v['n'])
counts[S + '/exp-inside'] = expr_family(S, 'exp-inside', lambda v: v['k'] * X * sp.exp(v['a'] * X**2))
counts[S + '/log-inside'] = expr_family(S, 'log-inside', lambda v: v['k'] * X / (X**2 + v['b']))
U = sp.Symbol('U')


def defpow(v):
    return I(2 * v['m'] * X * (X**2 + v['b'])**v['n'], v['p'], v['q'])


def defpow_kept(v):   # the u integral with the x limits left unchanged
    return sp.integrate(v['m'] * U**v['n'], (U, v['p'], v['q']))


counts[S + '/definite-power'] = num_family(S, 'definite-power', defpow, lambda v: {'limits-kept': defpow_kept(v)})

# ---------- fluency-l10-undo-product ----------
S = 'fluency-l10-undo-product'
counts[S + '/parts-exp'] = expr_family(S, 'parts-exp', lambda v: v['a'] * X * sp.exp(v['k'] * X))
counts[S + '/parts-cos'] = expr_family(S, 'parts-cos', lambda v: v['a'] * X * sp.cos(v['k'] * X))
counts[S + '/parts-sin'] = expr_family(S, 'parts-sin', lambda v: v['a'] * X * sp.sin(v['k'] * X))
XP = sp.Symbol('XP', positive=True)
counts[S + '/parts-log'] = expr_family(S, 'parts-log', lambda v: v['a'] * X**v['n'] * sp.log(X),
                                       lambda v: sp.integrate(v['a'] * XP**v['n'] * sp.log(XP), XP).subs(XP, X))

# ---------- fluency-l14-splitting-fractions ----------
S = 'fluency-l14-splitting-fractions'


def prompt_numerator(prompt, letter):
    m = re.search(r'\\frac\{([^{}]*)\}\{\(', prompt)
    return parse(m.group(1), letter)


def cover_items():
    items = sample(S, 'cover-up')
    for it in items:
        v = it['vars']
        a, b = v['a'], v['b']
        num = prompt_numerator(it['prompt'], 'x')
        f = num / ((X - a) * (X - b))
        parts = sp.apart(sp.together(f), X)
        A = sp.limit((X - a) * parts, X, a)
        B = sp.limit((X - b) * parts, X, b)
        check(sp.simplify(parts - (A / (X - a) + B / (X - b))) == 0, f'{S}/cover-up seed {it["seed"]}: not two simple pieces')
        check(int(it['answer']) == A, f'{S}/cover-up seed {it["seed"]}: answer {it["answer"]} but apart gives A = {A}')
        mine = {'other-factor': B, 'no-divide': num.subs(X, a)}
        vals = []
        for w in it['wrong']:
            check(int(w['value']) == mine[w['id']], f'{S}/cover-up seed {it["seed"]}: wrong {w["id"]} {w["value"]} but here {mine[w["id"]]}')
            check(int(w['value']) != A, f'{S}/cover-up seed {it["seed"]}: wrong {w["id"]} equals the key')
            vals.append(int(w['value']))
        check(len(set(vals)) == len(vals), f'{S}/cover-up seed {it["seed"]}: two wrongs coincide')
    return len(items)


counts[S + '/cover-up'] = cover_items()


def split_ref(v):
    a, b = v['a'], v['a'] + v['d']
    # the numerator is rebuilt from the vars; apart must return the same two coefficients
    f = (v['ca'] * (X - b) + v['cb'] * (X - a)) / ((X - a) * (X - b))
    parts = sp.apart(sp.together(f), X)
    A = sp.limit((X - a) * parts, X, a)
    B = sp.limit((X - b) * parts, X, b)
    return A * sp.log(sp.Abs(X - a)) + B * sp.log(sp.Abs(X - b))


def split_f(v):
    a, b = v['a'], v['a'] + v['d']
    return (v['ca'] * (X - b) + v['cb'] * (X - a)) / ((X - a) * (X - b))


counts[S + '/split-integrate'] = expr_family(S, 'split-integrate', split_f, split_ref)

for k, n in counts.items():
    print(f'{k}: {n} draws')
print(f'{checks} checks, {len(fails)} failures')
for m in fails[:30]:
    print('FAIL', m)
sys.exit(1 if fails else 0)
