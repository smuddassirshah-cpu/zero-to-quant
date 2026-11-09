"""Reader harness for Python code items: mirrors app/js/engine/widgets/code.js __zq_cmp
(isclose element by element through tolist(), equal by ==, raises by exception class).
Run from this folder with the venv Python."""
import json, math, time, pathlib, multiprocessing as mp

ROOT = pathlib.Path(__file__).resolve().parents[3]
COURSES = ROOT / "app" / "content" / "courses"


def item(course, fname, iid):
    d = json.loads((COURSES / course / fname).read_text())
    for it in d["items"]:
        if it["id"] == iid:
            return it
    raise KeyError(iid)


def _flat(v):
    return v.tolist() if hasattr(v, "tolist") and not isinstance(v, (int, float, complex, str)) else v


def _close(x, y, tol):
    x, y = _flat(x), _flat(y)
    if isinstance(x, (list, tuple)) or isinstance(y, (list, tuple)):
        return isinstance(x, (list, tuple)) and isinstance(y, (list, tuple)) and len(x) == len(y) and all(_close(p, q, tol) for p, q in zip(x, y))
    if isinstance(x, (str, bytes)) and not isinstance(y, (str, bytes)):
        return False
    try:
        if tol:
            return math.isclose(float(x), float(y), rel_tol=tol[0], abs_tol=tol[1])
        return math.isclose(float(x), float(y), rel_tol=1e-9, abs_tol=1e-12)
    except Exception:
        return x == y


def _tol(c):
    t = c.get("tol")
    if isinstance(t, dict):
        return [max(0, float(t.get("rel", 0) or 0)), max(0, float(t.get("abs", 0) or 0))]
    if isinstance(t, (int, float)) and t >= 0:
        return [0, float(t)]
    return None


def _run(src, pre, cases, q):
    g = {"__name__": "__main__"}
    out = []
    try:
        if pre:
            exec(compile(pre, "<prelude>", "exec"), g)
        exec(compile(src, "solution.py", "exec"), g)
    except Exception as e:
        q.put([("load-error", repr(e), 0.0)] * len(cases))
        return
    for c in cases:
        t0 = time.time()
        try:
            if c.get("setup"):
                exec(c["setup"], g)
            cmp = c.get("compare", "equal")
            if cmp == "raises":
                try:
                    a = eval(c["call"], g)
                    ok = False
                    val = "no error " + repr(a)
                except Exception as x:
                    ok = c["expect"].strip().strip("\"'") in [k.__name__ for k in type(x).__mro__]
                    val = "raised " + type(x).__name__
            else:
                a = eval(c["call"], g)
                e = eval(c["expect"], g)
                val = repr(a)[:120]
                if cmp == "isclose":
                    ok = _close(a, e, _tol(c))
                else:
                    try:
                        ok = bool(_flat(a) == _flat(e))
                    except Exception:
                        ok = False
        except Exception as x:
            ok, val = False, "error " + type(x).__name__ + ": " + str(x)[:80]
        out.append(("pass" if ok else "FAIL", val, time.time() - t0))
    q.put(out)


def run(widget, src, which="all", timeout=120):
    cases = (widget.get("examples", []) if which in ("all", "examples") else []) + (widget.get("tests", []) if which in ("all", "tests") else [])
    q = mp.Queue()
    p = mp.Process(target=_run, args=(src, widget.get("prelude", ""), cases, q))
    p.start()
    p.join(timeout)
    if p.is_alive():
        p.terminate()
        return [("timeout", "", timeout)] * len(cases)
    return q.get()


def summary(widget, src, label):
    """Returns the list of failing test numbers (1-based over tests) and the max case time."""
    r = run(widget, src, "tests")
    fails = [i + 1 for i, x in enumerate(r) if x[0] != "pass"]
    tmax = max((x[2] for x in r), default=0)
    print(f"  {label:<44} fails tests {fails if fails else 'none'}  (slowest case {tmax:.2f} s)")
    return fails, r
