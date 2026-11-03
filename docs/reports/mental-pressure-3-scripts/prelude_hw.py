import re as _re, math as _math
from fractions import Fraction as _F

_MIX = {"addsub": 15, "mul": 15, "div": 10, "dec": 12, "frac": 10, "pct": 10, "seq": 8}


def _n(s):
    return _F(s.replace(',', ''))


def _next(t):
    d = [b - a for a, b in zip(t, t[1:])]
    if len(d) >= 2 and len(set(d)) == 1:
        return t[-1] + d[0]
    d2 = [b - a for a, b in zip(d, d[1:])]
    if len(d2) >= 2 and len(set(d2)) == 1:
        return t[-1] + d[-1] + d2[0]
    if len(t) >= 4 and t[1] != t[0]:
        r = (t[2] - t[1]) / (t[1] - t[0])
        c = t[1] - r * t[0]
        if all(b == r * a + c for a, b in zip(t, t[1:])):
            return r * t[-1] + c
    return None


def _read(text):
    t = str(text).replace('−', '-').replace('×', '*').replace('÷', '/').strip()
    if t.endswith('?'):
        terms = [_n(x) for x in _re.split(r',\s+', t[:-1].strip().rstrip(',')) if x]
        return 'seq', _next(terms)
    m = _re.fullmatch(r'([\d.,]+)% of ([\d.,]+)', t)
    if m:
        return 'pct', _n(m[1]) * _n(m[2]) / 100
    m = _re.fullmatch(r'(\d+)/(\d+) ([+-]) (\d+)/(\d+)', t)
    if m:
        a, b = _F(int(m[1]), int(m[2])), _F(int(m[4]), int(m[5]))
        return 'frac', a + b if m[3] == '+' else a - b
    m = _re.fullmatch(r'([\d.,]+) ([+*/x-]) ([\d.,]+)', t)
    if m:
        a, op, b = _n(m[1]), m[2], _n(m[3])
        v = {'+': a + b, '-': a - b, '*': a * b, 'x': a * b, '/': a / b}[op]
        if '.' in m[1] or '.' in m[3]:
            return 'dec', v
        return {'+': 'addsub', '-': 'addsub', '*': 'mul', 'x': 'mul', '/': 'div'}[op], v
    return None, None


def _close(a, b):
    try:
        return _math.isclose(float(a), float(b), rel_tol=1e-9, abs_tol=1e-9)
    except (TypeError, ValueError):
        return False


def _shape_ok(items):
    return isinstance(items, list) and len(items) > 0 and all(
        isinstance(it, (tuple, list)) and len(it) == 3 and isinstance(it[0], str) and len(it[1]) == 4 for it in items)


def _counts(items):
    out = {}
    for it in items or []:
        k = _read(it[0])[0]
        out[k] = out.get(k, 0) + 1
    return out


def _answers_ok(items):
    if not _shape_ok(items):
        return False
    for text, opts, ans in items:
        k, v = _read(text)
        if v is None or not _close(ans, v):
            return False
    return True


def _answer_once(items):
    if not _shape_ok(items):
        return False
    for text, opts, ans in items:
        if sum(_close(o, ans) for o in opts) != 1:
            return False
        if any(_close(a, b) for i, a in enumerate(opts) for b in opts[i + 1:]):
            return False
    return True


def _near_ok(items):
    if not _shape_ok(items):
        return False
    for text, opts, ans in items:
        a = float(ans)
        if a <= 0 or any(not (a / 10 - 1e-9 <= float(o) <= a * 10 + 1e-9) for o in opts):
            return False
    return True


def _whole_div(items):
    divs = [it for it in items if _read(it[0])[0] == 'div'] if _shape_ok(items) else []
    return len(divs) > 0 and all(_close(it[2], round(float(it[2]))) for it in divs)


def _key(items):
    return [(t, [float(o) for o in os], float(x)) for t, os, x in items]


def _same(a, b):
    return _shape_ok(a) and _shape_ok(b) and _key(a) == _key(b)


def _differ(a, b):
    return _shape_ok(a) and _shape_ok(b) and [it[0] for it in a] != [it[0] for it in b]
