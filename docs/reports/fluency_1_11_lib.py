"""Shared reader and checker for the topic 1.11 Fluency recompute scripts (complex, odes, vector-calc).

Each course script gives, per family, a function derive(V) -> (key, {wrong_id: slip}) computed from the drawn
variables alone (never from the printed answer or the lets). This module samples the engine with
`node tools/fluency-sample.mjs --json`, reads the LaTeX it prints, and compares: the key with the engine's answer,
the offered wrong ids with the expected ones (so every `when` is checked), each slip with the engine's wrong text,
and each slip against the key (it must differ). Keys may be sympy expressions, numbers, lists (a set answer,
compared in any order) or tuples (a vector, compared entry by entry).
"""
import json
import os
import subprocess
import sys

import sympy as sp
from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application

APP = os.environ.get('FLUENCY_APP') or os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app')
N = int(sys.argv[sys.argv.index('--n') + 1]) if '--n' in sys.argv else 200
x, y, z, t = sp.symbols('x y z t', real=True)
SYM = {'x': x, 'y': y, 'z': z, 't': t, 'I': sp.I, 'pi': sp.pi}
FUNCS = {'exp': sp.exp, 'sqrt': sp.sqrt, 'cos': sp.cos, 'sin': sp.sin}


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
    for a, b in (('\\left', ''), ('\\right', ''), ('\\,', ' '), ('\\cdot', '*'), ('\\times', '*')):
        s = s.replace(a, b)
    out, i = [], 0
    while i < len(s):
        if s.startswith('\\dfrac', i) or s.startswith('\\frac', i):
            i += 6 if s.startswith('\\dfrac', i) else 5
            a, i = _group(s, i)
            b, i = _group(s, i)
            out.append(' ((%s)/(%s)) ' % (tex2py(a), tex2py(b)))
        elif s.startswith('\\sqrt', i):
            i += 5
            a, i = _group(s, i)
            out.append(' sqrt(%s) ' % tex2py(a))
        elif s.startswith('\\pi', i):
            i += 3
            out.append(' pi ')
        elif s.startswith('\\cos', i) or s.startswith('\\sin', i):
            out.append(' %s' % s[i + 1:i + 4])
            i += 4
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
        elif s[i] == 'i' and not (i + 1 < len(s) and s[i + 1].isalpha()):
            out.append(' I ')
            i += 1
        else:
            c = s[i]
            out.append(' %s ' % c if c.isalpha() else c)
            i += 1
    return ''.join(out)


def parse(s):
    return parse_expr(tex2py(s), local_dict=dict(SYM, **FUNCS),
                      transformations=standard_transformations + (implicit_multiplication_application,))


def split_top(s):
    """Split 'a, b, c' at top-level commas (a set answer or a vector's entries)."""
    parts, depth, cur = [], 0, ''
    for ch in s:
        if ch in '({[':
            depth += 1
        elif ch in ')}]':
            depth -= 1
        if ch == ',' and depth == 0:
            parts.append(cur)
            cur = ''
        else:
            cur += ch
    parts.append(cur)
    return [p.strip() for p in parts]


def same(a, b):
    if isinstance(a, tuple) or isinstance(b, tuple):
        return isinstance(a, tuple) and isinstance(b, tuple) and len(a) == len(b) and all(same(p, q) for p, q in zip(a, b))
    if isinstance(a, list) or isinstance(b, list):
        if not (isinstance(a, list) and isinstance(b, list) and len(a) == len(b)):
            return False
        rest = list(b)
        for p in a:
            hit = next((k for k, q in enumerate(rest) if same(p, q)), None)
            if hit is None:
                return False
            rest.pop(hit)
        return True
    d = sp.simplify(sp.expand(sp.sympify(a) - sp.sympify(b)))
    if d == 0:
        return True
    try:
        return abs(complex(sp.N(d))) < 1e-9
    except TypeError:
        return False


def read_expr(text):
    text = text.strip()
    if text.startswith('(') and text.endswith(')') and len(split_top(text[1:-1])) > 1:
        return tuple(parse(p) for p in split_top(text[1:-1]))
    return parse(text)


def read_item(it):
    """The engine's key as the course scripts return it."""
    if it['kind'] == 'numeric':
        if 'answers' in it:
            return [sp.nsimplify(v, rational=True) for v in it['answers']]
        return float(it['answer'])
    if 'answers' in it:
        return [read_expr(a) for a in it['answers']]
    return read_expr(it['answer'])


def read_wrong(it, w):
    if it['kind'] == 'numeric':
        v = str(w['value'])
        if 'answers' in it:
            return [sp.nsimplify(float(p), rational=True) for p in split_top(v)]
        return float(v)
    if 'answers' in it:
        return [read_expr(p) for p in split_top(w['tex'])]
    return read_expr(w['tex'])


def num_close(a, b, tol):
    return abs(float(a) - float(b)) <= tol


class Checker:
    def __init__(self, course):
        self.course = course
        self.fails = []
        self.checked = 0
        self.families = 0

    def sample(self, set_id, fam):
        out = subprocess.run(['node', 'tools/fluency-sample.mjs', '--set', '%s/%s' % (self.course, set_id), '--family', fam,
                              '--n', str(N), '--json'], cwd=APP, capture_output=True, text=True, check=True).stdout
        return json.loads(out)['items']

    def check(self, set_id, fam, derive):
        self.families += 1
        items = self.sample(set_id, fam)
        assert len(items) == N, (set_id, fam, len(items))
        for it in items:
            V = {k: (sp.nsimplify(v, rational=True) if isinstance(v, (int, float)) else v) for k, v in it['vars'].items()}
            key, wrongs = derive(V)
            label = '%s/%s seed %s' % (set_id, fam, it['seed'])
            eng = read_item(it)
            tol = (it.get('tol') or {}).get('abs', 0)
            numeric_single = it['kind'] == 'numeric' and 'answers' not in it
            ok = num_close(eng, key, 1e-8) if numeric_single else same(eng, key)
            self.checked += 1
            if not ok:
                self.fails.append('%s: key %s, engine %s' % (label, key, it.get('answer', it.get('answers'))))
            if set(w['id'] for w in it['wrong']) != set(wrongs):
                self.fails.append('%s: offered %s, expected %s' % (label, sorted(w['id'] for w in it['wrong']), sorted(wrongs)))
                continue
            for w in it['wrong']:
                want = wrongs[w['id']]
                got = read_wrong(it, w)
                if numeric_single:
                    okw = num_close(got, want, 1e-8) and abs(float(got) - float(key)) > tol
                else:
                    okw = same(got, want) and not same(got, key)
                self.checked += 1
                if not okw:
                    self.fails.append('%s: wrong %s, expected %s, engine %s' % (label, w['id'], want, w.get('tex', w.get('value'))))

    def finish(self):
        for f in self.fails[:30]:
            print('FAIL', f)
        print('%s: %d checks over %d families, %d failures' % (self.course, self.checked, self.families, len(self.fails)))
        sys.exit(1 if self.fails else 0)
