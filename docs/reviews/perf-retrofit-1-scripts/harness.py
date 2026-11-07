"""Shared harness for the second read of the retrofit performance tasks.

Loads an item, runs code against its examples and hidden tests the way
app/js/engine/widgets/code.js does (postlude after the code; equal, or
isclose element by element with rel 1e-9 and abs 1e-12, None must be None),
and times each case in CPython against the engine's 5 s limit.
"""
import json
import math
import os
import time

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
LIMIT = 5.0
FAILS = []


def item(course, hw, item_id):
    path = os.path.join(ROOT, 'app', 'content', 'courses', course, hw + '.json')
    with open(path) as f:
        d = json.load(f)
    for it in d['items']:
        if it['id'] == item_id:
            return d, it
    raise SystemExit('item not found: ' + item_id)


def _flat(v):
    return v.tolist() if hasattr(v, 'tolist') and not isinstance(v, (int, float, complex, str)) else v


def _close(x, y):
    x, y = _flat(x), _flat(y)
    if isinstance(x, (list, tuple)) or isinstance(y, (list, tuple)):
        return (isinstance(x, (list, tuple)) and isinstance(y, (list, tuple)) and len(x) == len(y)
                and all(_close(p, q) for p, q in zip(x, y)))
    if isinstance(x, (str, bytes)) and not isinstance(y, (str, bytes)):
        return False
    try:
        return math.isclose(float(x), float(y), rel_tol=1e-9, abs_tol=1e-12)
    except Exception:
        return x == y


def run(code, widget, cases):
    """Return a list of (passed, seconds, value-or-error) for each case."""
    ns = {}
    exec(code, ns)
    if widget.get('postlude'):
        exec(widget['postlude'], ns)
    out = []
    for c in cases:
        t0 = time.perf_counter()
        try:
            got = eval(c['call'], ns)
            want = eval(c['expect'], ns)
            ok = _close(got, want) if c.get('compare') == 'isclose' else bool(_flat(got) == _flat(want))
        except Exception as e:  # an exception is a failure
            got, ok = 'raised ' + type(e).__name__, False
        dt = time.perf_counter() - t0
        out.append((ok and dt <= LIMIT, dt, got))
    return out


def check(ok, msg):
    print(('ok   ' if ok else 'FAIL ') + msg)
    if not ok:
        FAILS.append(msg)


def finish():
    print('failures:', len(FAILS))
    raise SystemExit(1 if FAILS else 0)
