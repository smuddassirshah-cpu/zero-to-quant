"""Reader harness for the batch 14 Python code items (copied from harness12.py, with script mode added). Mirrors app/js/engine/widgets/code.js (JUDGE and harness):
the learner's source is carried as __learner_source__, then prelude, source and postlude run in one namespace,
then each case runs there in order (setup exec'd in that namespace first, cases share it, as in the worker).
equal compares lists and tuples alike, dicts by key set, NaN matches NaN, a DataFrame through to_numpy().tolist()
(with index and columns checked when expect is a DataFrame); isclose uses rel 1e-9, abs 1e-12, or the case's tol.
Each variant runs in its own process in a fresh empty working directory. Run with the venv Python (-I is fine), or
in Pyodide 0.27.7 (NumPy 2.0.2) through pyo12.mjs, where each variant runs inline in a fresh namespace."""
import json, math, time, pathlib, multiprocessing as mp, os, tempfile, sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
COURSES = ROOT / "app" / "content" / "courses"


def item(course, fname, iid):
    d = json.loads((COURSES / course / fname).read_text())
    for it in d["items"]:
        if it["id"] == iid:
            return it
    raise KeyError(iid)


def _flat(v):
    if hasattr(v, "to_numpy") and getattr(v, "ndim", 0) == 2:
        return v.to_numpy().tolist()
    return v.tolist() if hasattr(v, "tolist") and not isinstance(v, (int, float, complex, str)) else v


def _nan(v):
    try:
        return bool(v != v)
    except Exception:
        return False


def _same(x, y):
    x, y = _flat(x), _flat(y)
    if isinstance(x, dict) or isinstance(y, dict):
        return isinstance(x, dict) and isinstance(y, dict) and set(x) == set(y) and all(_same(x[k], y[k]) for k in x)
    if isinstance(x, (list, tuple)) or isinstance(y, (list, tuple)):
        return isinstance(x, (list, tuple)) and isinstance(y, (list, tuple)) and len(x) == len(y) and all(_same(p, q) for p, q in zip(x, y))
    if _nan(x) and _nan(y):
        return True
    return bool(x == y)


def _close(x, y, tol=None):
    x, y = _flat(x), _flat(y)
    if isinstance(x, dict) or isinstance(y, dict):
        return isinstance(x, dict) and isinstance(y, dict) and set(x) == set(y) and all(_close(x[k], y[k], tol) for k in x)
    if isinstance(x, (list, tuple)) or isinstance(y, (list, tuple)):
        return isinstance(x, (list, tuple)) and isinstance(y, (list, tuple)) and len(x) == len(y) and all(_close(p, q, tol) for p, q in zip(x, y))
    if isinstance(x, (str, bytes)) and not isinstance(y, (str, bytes)):
        return False
    if _nan(x) and _nan(y):
        return True
    try:
        if tol:
            return math.isclose(float(x), float(y), rel_tol=tol[0], abs_tol=tol[1])
        return math.isclose(float(x), float(y), rel_tol=1e-9, abs_tol=1e-12)
    except Exception:
        return x == y


def _frame(a, e):
    if hasattr(e, "columns") and hasattr(e, "index"):
        return hasattr(a, "columns") and hasattr(a, "index") and _same(list(a.index), list(e.index)) and _same(list(a.columns), list(e.columns))
    return True


def _tol(c):
    t = c.get("tol")
    if isinstance(t, dict):
        return (max(0.0, float(t.get("rel", 0) or 0)), max(0.0, float(t.get("abs", 0) or 0)))
    if isinstance(t, (int, float)):
        return (0.0, float(t))
    return None


def _run(src, pre, post, cases, q):
    d = tempfile.mkdtemp(prefix="zq14-")
    os.chdir(d)
    if d not in sys.path:
        sys.path.insert(0, d)
    g = {"__name__": "__main__", "__learner_source__": src}
    out = []
    import io, contextlib
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            if pre:
                exec(compile(pre, "<prelude>", "exec"), g)
            exec(compile(src, "solution.py", "exec"), g)
            if post:
                exec(compile(post, "<postlude>", "exec"), g)
    except Exception as e:
        q.put([("load-error", repr(e), 0.0)] * len(cases))
        return
    for c in cases:
        t0 = time.time()
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                if c.get("setup"):
                    exec(c["setup"], g)
                cmp = c.get("compare", "equal")
                if cmp == "raises":
                    try:
                        a = eval(c["call"], g)
                        ok, val = False, "no error " + repr(a)[:60]
                    except Exception as x:
                        ok = c["expect"].strip().strip("\"'") in [k.__name__ for k in type(x).__mro__]
                        val = "raised " + type(x).__name__
                else:
                    a = eval(c["call"], g)
                    e = eval(c["expect"], g)
                    val = repr(a)[:160]
                    if not _frame(a, e):
                        ok = False
                    elif cmp == "isclose":
                        ok = _close(a, e, _tol(c))
                    else:
                        ok = _same(a, e)
        except BaseException as x:
            ok, val = False, "error " + type(x).__name__ + ": " + str(x)[:100]
        out.append(("pass" if ok else "FAIL", val, time.time() - t0))
    q.put(out)


class _Q:
    def put(self, v):
        self.v = v


def run(widget, src, which="tests", timeout=300):
    cases = (widget.get("examples", []) if which in ("all", "examples") else []) + (widget.get("tests", []) if which in ("all", "tests") else [])
    if sys.platform == "emscripten":  # Pyodide (pyo12.mjs): no processes, so each variant runs inline in a fresh namespace
        q, here = _Q(), os.getcwd()
        try:
            _run(src, widget.get("prelude", ""), widget.get("postlude", ""), cases, q)
        finally:
            os.chdir(here)
        return q.v
    q = mp.Queue()
    p = mp.Process(target=_run, args=(src, widget.get("prelude", ""), widget.get("postlude", ""), cases, q))
    p.start()
    p.join(timeout)
    if p.is_alive():
        p.terminate()
        return [("timeout", "", timeout)] * len(cases)
    return q.get()


def summary(widget, src, label, which="tests", show=False):
    r = run(widget, src, which)
    fails = [i + 1 for i, x in enumerate(r) if x[0] != "pass"]
    tmax = max((x[2] for x in r), default=0)
    print(f"  {label:<52} fails {which} {fails if fails else 'none'}  (slowest case {tmax:.2f} s)")
    if show:
        for i, x in enumerate(r):
            if x[0] != "pass":
                print(f"      case {i + 1}: {x[0]} {x[1]}")
    return fails, r


def patched(src, *pairs):
    """src with each (old, new) replaced once; fails loudly if old is missing, so a planted bug never silently equals the solution."""
    for old, new in pairs:
        assert old in src, ("plant does not apply", old)
        src = src.replace(old, new, 1)
    return src


# ---- script mode (code.js __zq_case): a fresh namespace per case; prelude, code, postlude run there with that
# case's stdin; `printed` is the output's lines; stdout cases compare whitespace-normalised text, `match` a regex
# (re.M), `lines` an in-order subsequence; a call case is evaluated in that namespace after the run ----
import io as _io, re as _re, contextlib as _cl


def _norm(t):
    ls = [l.rstrip() for l in t.replace('\r\n', '\n').split('\n')]
    while ls and not ls[0]:
        ls.pop(0)
    while ls and not ls[-1]:
        ls.pop()
    return ls


def _script_case(src, pre, post, c):
    feed = _io.StringIO(c.get('stdin', ''))
    out = _io.StringIO()

    def _input(prompt=''):
        ln = feed.readline()
        if not ln:
            raise EOFError('EOF')
        return ln[:-1] if ln.endswith('\n') else ln
    ns = {'__name__': '__main__', 'input': _input, '__learner_source__': src}
    try:
        with _cl.redirect_stdout(out):
            if pre:
                exec(compile(pre, '<prelude>', 'exec'), ns)
            exec(compile(src, 'main.py', 'exec'), ns)
            if post:
                exec(compile(post, '<postlude>', 'exec'), ns)
    except SystemExit:
        pass
    except BaseException as x:
        return ('FAIL', 'error ' + type(x).__name__ + ': ' + str(x)[:80])
    txt = out.getvalue()
    ns['printed'] = txt.splitlines()
    cmp = c.get('compare', 'equal')
    if cmp == 'stdout':
        if c.get('match'):
            ok = bool(_re.search(c['match'], txt, _re.M))
        elif c.get('lines'):
            want, have, k = _norm(c['expect']), _norm(txt), 0
            for l in have:
                if k < len(want) and l == want[k]:
                    k += 1
            ok = k == len(want)
        elif c.get('exact'):
            ok = txt == c['expect']
        else:
            ok = _norm(txt) == _norm(c['expect'])
        return ('pass' if ok else 'FAIL', repr(txt)[:120])
    try:
        with _cl.redirect_stdout(_io.StringIO()):
            if c.get('setup'):
                exec(c['setup'], ns)
            a = eval(c['call'], ns)
        e = eval(c['expect'], ns)
        ok = _close(a, e, _tol(c)) if cmp == 'isclose' else _same(a, e)
        return ('pass' if ok else 'FAIL', repr(a)[:120])
    except BaseException as x:
        return ('FAIL', 'error ' + type(x).__name__ + ': ' + str(x)[:80])


def is_script(widget):
    cs = widget.get('tests', []) + widget.get('examples', [])
    return any(c.get('compare') == 'stdout' or 'stdin' in c or 'argv' in c for c in cs)


def grade(widget, src, which='tests'):
    """1-based failing case numbers, function mode or script mode as the widget's cases decide."""
    cases = widget.get(which, [])
    if is_script(widget):
        here = os.getcwd()
        res = []
        for c in cases:
            d = tempfile.mkdtemp(prefix='zq14s-')
            os.chdir(d)
            try:
                res.append(_script_case(src, widget.get('prelude', ''), widget.get('postlude', ''), c))
            finally:
                os.chdir(here)
        return [i + 1 for i, r in enumerate(res) if r[0] != 'pass'], res
    r = run(widget, src, which)
    return [i + 1 for i, x in enumerate(r) if x[0] != 'pass'], r
