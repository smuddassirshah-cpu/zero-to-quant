"""Shared reader for the topic 1.4 Fluency number scripts (vectors, elimination, eigen, least-squares).

Each course script imports this file, gives a `derive(V)` per family that works the key and every slip out again from the
drawn `vars` alone (never from the printed answer or lets), and calls `run(course, checks)`. For every draw it checks:
the engine's key equals the derived key; the offered wrong ids are the ones expected for that draw; each wrong equals the
derived slip; each wrong differs from the key (numeric: by more than the key's tolerance); and no two offered wrongs
coincide. Keys are exact: a Fraction, a tuple of Fractions (a vector), a sorted tuple marked as a set, or a sympy
polynomial in lambda.
"""
import json
import os
import re
import subprocess
import sys
from fractions import Fraction as F

import sympy as sp

APP = os.environ.get('FLUENCY_APP') or os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app')
N = int(sys.argv[sys.argv.index('--n') + 1]) if '--n' in sys.argv else 200
LAM = sp.Symbol('L')


class Set(tuple):
    """An unordered set answer: compared as a sorted tuple."""
    def __new__(cls, xs):
        return super().__new__(cls, sorted(F(x) for x in xs))


def num(s):
    """A number from engine output: int, float, '7/3', '-\\frac{3}{5}', '2.5'."""
    if isinstance(s, (int,)):
        return F(s)
    if isinstance(s, float):
        return F(s).limit_denominator(10 ** 6)
    s = s.strip().replace(' ', '')
    m = re.fullmatch(r'(-?)\\frac\{(-?\d+)\}\{(\d+)\}', s)
    if m:
        v = F(int(m.group(2)), int(m.group(3)))
        return -v if m.group(1) else v
    return F(s).limit_denominator(10 ** 6) if '.' in s else F(s)


def vec(tex):
    t = tex.strip()
    assert t[0] == '(' and t[-1] == ')', tex
    return tuple(num(x) for x in t[1:-1].split(','))


def poly(tex):
    t = tex.replace('\\lambda', 'L')
    t = re.sub(r'(\d)L', r'\1*L', t).replace('^', '**')
    return sp.expand(sp.sympify(t, locals={'L': LAM}))


def read(kind, it, text):
    """Turn an engine answer or wrong text into the comparable type."""
    if kind == 'set':
        return Set(num(x) for x in str(text).split(','))
    if kind == 'vec':
        return vec(text)
    if kind == 'poly':
        return poly(text)
    return num(text)


def same(kind, a, b, tol=0):
    if kind == 'poly':
        return sp.expand(a - b) == 0
    if kind == 'num':
        return abs(float(a) - float(b)) <= tol + 1e-12
    if kind == 'set':
        return len(a) == len(b) and all(abs(float(x) - float(y)) <= tol + 1e-12 for x, y in zip(a, b))
    return tuple(a) == tuple(b)


def sample(course, set_id, fam):
    out = subprocess.run(['node', 'tools/fluency-sample.mjs', '--set', '%s/%s' % (course, set_id), '--family', fam,
                          '--n', str(N), '--json'], cwd=APP, capture_output=True, text=True, check=True).stdout
    return json.loads(out)['items']


def run(course, checks):
    """checks: list of (set_id, family_id, kind, derive). derive(V) -> (key, {wrong_id: value})."""
    fails, count = [], 0
    for set_id, fam, kind, derive in checks:
        items = sample(course, set_id, fam)
        assert len(items) == N, (set_id, fam, len(items))
        for it in items:
            V = {k: (F(v).limit_denominator(10 ** 6) if isinstance(v, (int, float)) else v) for k, v in it['vars'].items()}
            key, wrongs = derive(V)
            label = '%s/%s seed %s' % (set_id, fam, it['seed'])
            tol = (it.get('tol') or {}).get('abs', 0) if it['kind'] == 'numeric' else 0
            got = Set(num(x) for x in it['answers']) if kind == 'set' else read(kind, it, it['answer'])
            count += 1
            if not same(kind, got, key):
                fails.append('%s: key %s, engine %s' % (label, key, got))
            offered = [w['id'] for w in it['wrong']]
            if set(offered) != set(wrongs):
                fails.append('%s: offered %s, expected %s' % (label, offered, sorted(wrongs)))
                continue
            seen = []
            for w in it['wrong']:
                wv = read(kind, it, w.get('tex', w.get('value')))
                wtol = max(tol, (w.get('tol') or {}).get('abs', 0))
                count += 1
                if not same(kind, wv, wrongs[w['id']], 1e-9):
                    fails.append('%s: wrong %s engine %s, derived %s' % (label, w['id'], wv, wrongs[w['id']]))
                if same(kind, wv, key, wtol):
                    fails.append('%s: wrong %s equals the key %s' % (label, w['id'], key))
                for oid, ov in seen:
                    if same(kind, wv, ov, wtol):
                        fails.append('%s: wrongs %s and %s coincide' % (label, oid, w['id']))
                seen.append((w['id'], wv))
        print('checked %s/%s: %d draws' % (set_id, fam, len(items)))
    for f in fails[:40]:
        print('FAIL', f)
    print('%d checks, %d failures' % (count, len(fails)))
    sys.exit(1 if fails else 0)
