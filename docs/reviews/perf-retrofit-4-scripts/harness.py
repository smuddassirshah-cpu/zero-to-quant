"""Reader harness for retrofit batch 4: runs a code item's examples and tests the way
app/js/engine/widgets/code.js does (function mode: prelude, learner code and postlude in one
namespace; each case runs its setup, evals its call, compares as __zq_cmp does).
CPython only; Pyodide is several times slower, so each case's time is reported."""
import json, math, cmath, time, os, sys, io, contextlib
from fractions import Fraction

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
COURSES = os.path.join(ROOT, 'app', 'content', 'courses')


def item(course, setfile, item_id):
    d = json.load(open(os.path.join(COURSES, course, setfile)))
    for it in d['items']:
        if it['id'] == item_id:
            return it
    raise KeyError(item_id)


def _flat(v):
    return v.tolist() if hasattr(v, 'tolist') and not isinstance(v, (int, float, complex, str)) else v


def _close(x, y, tol):
    x, y = _flat(x), _flat(y)
    if isinstance(x, (list, tuple)) or isinstance(y, (list, tuple)):
        return isinstance(x, (list, tuple)) and isinstance(y, (list, tuple)) and len(x) == len(y) and all(_close(p, q, tol) for p, q in zip(x, y))
    if isinstance(x, (str, bytes)) and not isinstance(y, (str, bytes)):
        return False
    if any(isinstance(v, complex) or type(v).__name__.startswith('complex') for v in (x, y)):
        try:
            rt, at = (tol if tol else (1e-9, 1e-12))
            return cmath.isclose(complex(x), complex(y), rel_tol=rt, abs_tol=at)
        except Exception:
            return x == y
    try:
        rt, at = (tol if tol else (1e-9, 1e-12))
        return math.isclose(float(x), float(y), rel_tol=float(rt), abs_tol=float(at))
    except Exception:
        return x == y


def _tol(c):
    t = c.get('tol')
    if isinstance(t, dict):
        return (max(0, float(t.get('rel', 0) or 0)), max(0, float(t.get('abs', 0) or 0)))
    if isinstance(t, (int, float)):
        return (0, float(t))
    return None


def cases(it):
    w = it['widget']
    return [('example', i + 1, c) for i, c in enumerate(w.get('examples', []))] + \
           [('test', i + 1, c) for i, c in enumerate(w.get('tests', []))]


def run(it, src, which=('example', 'test'), quiet=True, time_limit=None):
    """Returns (list of (kind, n, ok, seconds, note)). A load error fails every case."""
    w = it['widget']
    ns = {'__name__': '__zq__', '__learner_source__': src}
    out = []
    buf = io.StringIO()
    cwd = os.getcwd()
    try:
        with contextlib.redirect_stdout(buf):
            if w.get('prelude'):
                exec(compile(w['prelude'], '<prelude>', 'exec'), ns)
            exec(compile(src, 'solution.py', 'exec'), ns)
            if w.get('postlude'):
                exec(compile(w['postlude'], '<postlude>', 'exec'), ns)
    except BaseException as e:
        return [(k, n, False, 0.0, 'load: %s: %s' % (type(e).__name__, e)) for k, n, c in cases(it) if k in which]
    for k, n, c in cases(it):
        if k not in which:
            continue
        t0 = time.perf_counter()
        note = ''
        try:
            with contextlib.redirect_stdout(buf):
                if c.get('setup'):
                    exec(c['setup'], ns)
                cmp = c.get('compare', 'equal')
                if cmp == 'raises':
                    try:
                        eval(c['call'], ns)
                        ok = False
                        note = 'no error'
                    except Exception as e:
                        ok = c['expect'].strip().strip('"\'') in [q.__name__ for q in type(e).__mro__]
                        note = 'raised ' + type(e).__name__
                else:
                    a = eval(c['call'], ns)
                    e = eval(c['expect'], ns)
                    if cmp == 'fraction':
                        ok = isinstance(a, Fraction) and a == e
                    elif cmp == 'isclose':
                        ok = _close(a, e, _tol(c))
                    else:
                        try:
                            ok = bool(_flat(a) == _flat(e))
                        except Exception:
                            ok = False
                    if not ok:
                        note = repr(a)[:120]
        except BaseException as ex:
            ok = False
            note = '%s: %s' % (type(ex).__name__, str(ex)[:100])
        dt = time.perf_counter() - t0
        out.append((k, n, bool(ok), dt, note))
    os.chdir(cwd)
    return out


def failing(res, kind='test'):
    return [n for k, n, ok, dt, note in res if k == kind and not ok]


def report(label, res):
    ft = failing(res, 'test'); fe = failing(res, 'example')
    slow = max((dt for *_, dt, _n in res), default=0)
    print('%-46s examples failing %-8s tests failing %-30s slowest %.3f s' % (label, fe or '-', ft or '-', slow))
    return fe, ft
