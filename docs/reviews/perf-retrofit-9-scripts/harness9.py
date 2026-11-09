"""Reader harness for the batch 9 Python code items. Mirrors app/js/engine/widgets/code.js: the learner's source
is carried as __learner_source__, then prelude, source and postlude run in one namespace (__zq_load), then each case
is evaluated there in order (cases share the namespace, as in the worker). equal compares lists and tuples alike and
dicts by key set then value (_same); isclose uses rel 1e-9, abs 1e-12; raises by exception class.
Each variant runs in its own process, in a fresh empty working directory (the pytest items write files there).
Run from this folder with the venv Python."""
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
    return v.tolist() if hasattr(v, "tolist") and not isinstance(v, (int, float, complex, str)) else v


def _same(x, y):
    x, y = _flat(x), _flat(y)
    if isinstance(x, dict) or isinstance(y, dict):
        return isinstance(x, dict) and isinstance(y, dict) and set(x) == set(y) and all(_same(x[k], y[k]) for k in x)
    if isinstance(x, (list, tuple)) or isinstance(y, (list, tuple)):
        return isinstance(x, (list, tuple)) and isinstance(y, (list, tuple)) and len(x) == len(y) and all(_same(p, q) for p, q in zip(x, y))
    return bool(x == y)


def _close(x, y):
    x, y = _flat(x), _flat(y)
    if isinstance(x, (list, tuple)) or isinstance(y, (list, tuple)):
        return isinstance(x, (list, tuple)) and isinstance(y, (list, tuple)) and len(x) == len(y) and all(_close(p, q) for p, q in zip(x, y))
    if isinstance(x, (str, bytes)) and not isinstance(y, (str, bytes)):
        return False
    try:
        return math.isclose(float(x), float(y), rel_tol=1e-9, abs_tol=1e-12)
    except Exception:
        return x == y


def _run(src, pre, post, cases, q):
    d = tempfile.mkdtemp(prefix="zq9-")
    os.chdir(d)
    if d not in sys.path:
        sys.path.insert(0, d)
    g = {"__name__": "__main__", "__learner_source__": src}
    out = []
    try:
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
                val = repr(a)[:120]
                ok = _close(a, e) if cmp == "isclose" else _same(a, e)
        except BaseException as x:
            ok, val = False, "error " + type(x).__name__ + ": " + str(x)[:80]
        out.append(("pass" if ok else "FAIL", val, time.time() - t0))
    q.put(out)


def run(widget, src, which="tests", timeout=300):
    cases = (widget.get("examples", []) if which in ("all", "examples") else []) + (widget.get("tests", []) if which in ("all", "tests") else [])
    q = mp.Queue()
    p = mp.Process(target=_run, args=(src, widget.get("prelude", ""), widget.get("postlude", ""), cases, q))
    p.start()
    p.join(timeout)
    if p.is_alive():
        p.terminate()
        return [("timeout", "", timeout)] * len(cases)
    return q.get()


def summary(widget, src, label, which="tests"):
    r = run(widget, src, which)
    fails = [i + 1 for i, x in enumerate(r) if x[0] != "pass"]
    tmax = max((x[2] for x in r), default=0)
    print(f"  {label:<46} fails {which} {fails if fails else 'none'}  (slowest case {tmax:.2f} s)")
    return fails, r


def summary_each(widget, src, label, timeout=20):
    """Each test in its own process with its own limit, for slips that run for ever on the large cases
    (the engine stops a case at 5 s and reports it against that case)."""
    fails, tmax = [], 0.0
    for i, c in enumerate(widget.get("tests", [])):
        w1 = dict(widget, tests=[c], examples=[])
        r = run(w1, src, "tests", timeout=timeout)[0]
        tmax = max(tmax, r[2])
        if r[0] != "pass":
            fails.append(i + 1 if r[0] != "timeout" else f"{i + 1} (over {timeout} s)")
    print(f"  {label:<46} fails tests {fails if fails else 'none'}  (slowest case {tmax:.2f} s)")
    return fails
