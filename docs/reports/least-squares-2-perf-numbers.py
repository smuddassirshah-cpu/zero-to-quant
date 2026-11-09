"""least-squares level 2 performance task: every number recomputed twice, and the code graded.

Item: app/content/courses/least-squares/homework-2.json#h-factor-neutral (performance: code).
Run: <venv>/bin/python -I docs/reports/least-squares-2-perf-numbers.py   (numpy and sympy; exits 0 when all checks pass)

Route 1: sympy exact arithmetic, P = F (F^T F)^{-1} F^T.
Route 2: sympy exact Gram-Schmidt, P = sum of q q^T over an orthonormal basis of C(F).
Route 3: numpy lstsq, fitted = F x with x from lstsq.
Then a harness that mirrors code.js (source run once, setup and call in the same namespace, isclose element by element
with the case tol and NaN-aware, equal exact, raises by exception class) grades the shipped solution, three other correct
solutions, the starter and twelve planted slips. Pyodide's NumPy returns nan for an exactly singular solve or inverse
(AUTHORING section 3); the harness patches np.linalg.solve and inv to do the same, and also runs the CPython behaviour.
"""
import json, math, os, sys
import numpy as np
import sympy as sp

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HW = os.path.join(ROOT, "app", "content", "courses", "least-squares", "homework-2.json")
doc = json.load(open(HW, encoding="utf-8"))
item = [i for i in doc["items"] if i["id"] == "h-factor-neutral"][0]
W = item["widget"]
fails = 0
checks = 0


def check(cond, msg):
    global fails, checks
    checks += 1
    if not cond:
        fails += 1
        print("FAIL", msg)


# ---------- structure ----------
check(item["performance"] == "code" and W["kind"] == "code" and W["language"] == "python", "kind")
check(len(W["tests"]) == 13 and len(W["examples"]) == 1 and len(W["tests"]) > len(W["examples"]), "13 tests, 1 example")
check(W["examples"][0] == W["tests"][0], "example is test 1")
check(6 <= len(doc["items"]) <= 12, "homework size")
check(any(i.get("difficulty") == 5 for i in doc["items"]), "a difficulty 5")
check(any(i.get("kind") == "longform" for i in doc["items"]), "a longform")
check(sum(1 for i in doc["items"] if i.get("performance")) == 1, "one performance item")
check("13 hidden tests" in W["how"] and "eight small factor sets" in W["how"], "how counts")

# ---------- the data, parsed back from the tests ----------
def parse_setup(setup):
    g = {}
    exec(setup.replace("import numpy as np; ", "").split("; P =")[0], {}, g)
    return g["F"], g["s"]

sets = [parse_setup(t["setup"]) for t in W["tests"]]
distinct = []
for F, s in sets:
    if (F, s) not in distinct:
        distinct.append((F, s))
check(len({json.dumps(F) for F, s in distinct}) == 8, "eight factor sets")


def Q(v):
    return sp.nsimplify(v)


def route1(F, s):
    A = sp.Matrix([[Q(v) for v in r] for r in F]); b = sp.Matrix([Q(v) for v in s])
    P = A * (A.T * A).inv() * A.T
    return P, P * b, b - P * b


def route2(F, s):
    A = sp.Matrix([[Q(v) for v in r] for r in F]); b = sp.Matrix([Q(v) for v in s])
    qs = []
    for j in range(A.shape[1]):
        v = A[:, j]
        for q in qs:
            v = v - (q.dot(A[:, j])) * q
        qs.append(v / sp.sqrt(v.dot(v)))
    P = sp.zeros(A.shape[0], A.shape[0])
    for q in qs:
        P += q * q.T
    P = sp.simplify(P)
    return P, P * b, b - P * b


def route3(F, s):
    A = np.array(F, float); b = np.array(s, float)
    x = np.linalg.lstsq(A, b, rcond=None)[0]
    return A @ x, b - A @ x


def rank_exact(F):
    return sp.Matrix([[Q(v) for v in r] for r in F]).rank()


def fl(M):
    return np.array([[float(v) for v in M.row(i)] for i in range(M.shape[0])]) if M.shape[1] > 1 else np.array([float(v) for v in M])


def flat(v):
    v = v.tolist() if hasattr(v, "tolist") else v
    return np.array([float(x) for x in sum(([y] if not isinstance(y, list) else flat(y).tolist() for y in v), [])]) if isinstance(v, list) else np.array([float(v)])


expect = {}
for idx, t in enumerate(W["tests"], 1):
    F, s = sets[idx - 1]
    k = len(F[0])
    if t["compare"] == "raises":
        check(rank_exact(F) < k, f"test {idx}: exact rank below {k}")
        continue
    P1, f1, e1 = route1(F, s)
    P2, f2, e2 = route2(F, s)
    check(sp.simplify(P1 - P2) == sp.zeros(*P1.shape), f"test {idx}: two exact routes agree on P")
    f3, e3 = route3(F, s)
    check(np.allclose(fl(f1), f3, atol=1e-9) and np.allclose(fl(e1), e3, atol=1e-9), f"test {idx}: lstsq agrees")
    A = sp.Matrix([[Q(v) for v in r] for r in F])
    check(A.T * e1 == sp.zeros(k, 1), f"test {idx}: F^T neutral = 0 exactly")
    check(P1 * P1 == P1 and P1.T == P1, f"test {idx}: P idempotent and symmetric")
    exp = eval(t["expect"])
    c = t["call"]
    if c == "project_out(F, s)[2]":
        got = fl(e1)
    elif c == "project_out(F, s)[1]":
        got = fl(f1)
    elif c == "project_out(F, s)[0]":
        got = fl(P1)
    elif "for v in project_out" in c:
        got = [fl(P1).tolist(), fl(e1).tolist()]
        check(P1 == sp.eye(len(F)) and e1 == sp.zeros(len(F), 1), f"test {idx}: square F gives I and 0")
    elif ".T @" in c:
        got = [0.0] * k
    else:
        got = [[len(F), len(F)], True, True]
    ok = (got == exp) if "shape" in c else np.allclose(flat(got), flat(exp), rtol=0, atol=1e-12)
    check(ok,
          f"test {idx}: stored expect {t['expect'][:60]}")

# numbers quoted in prose, feedback and explain
bk = item["feedback"]["byKey"]
P1, f1, e1 = route1(*sets[0])
check(list(e1) == [1, -1, 2, -2] and list(f1) == [2, 2, 3, 3], "test-1/2 feedback: (1,-1,2,-2) and (2,2,3,3)")
check(all(P1[i, j] == (sp.Rational(1, 2) if i // 2 == j // 2 else 0) for i in range(4) for j in range(4)), "test-3: 1/2 blocks")
F1, s1 = sets[0]
check([sum(v for v, r in zip(s1, F1) if r[1] == g) / sum(1 for r in F1 if r[1] == g) for g in (1, 0)] == [2, 3], "sector means 2 and 3")
P2, f2, e2 = route1(*sets[3])
check(list(f2) == [4, 3, sp.Rational(7, 2), sp.Rational(3, 2), sp.Rational(1, 2), sp.Rational(5, 2)], "test-5: fitted")
check(list(e2) == [0, -2, 2, -1, 1, 0], "test-4 neutral")
s7 = sets[11][1]
check(abs(sum(s7) / len(s7) - 0.1) < 1e-12 and sum(Q(v) for v in s7) / 5 == sp.Rational(1, 10), "test-12: mean 0.1 two ways")
P8, f8, e8 = route1(*sets[12])
check(list(e8) == [1, -1, -1, 1], "test-13: (1,-1,-1,1)")
check("(1, -1, 2, -2)" in bk["test-1"] and "(2, 2, 3, 3)" in bk["test-2"] and "(4, 3, 3.5, 1.5, 0.5, 2.5)" in bk["test-5"], "byKey text")
check("(1, -1, -1, 1)" in bk["test-13"] and "0.1" in bk["test-12"], "byKey text 2")
F5 = sets[9][0]
check(all(abs(r[2] - r[1] / 100) < 1e-15 for r in F5), "test-10: third column is the second over 100")
F4 = sets[8][0]
check(all(r[1] + r[2] == r[0] for r in F4), "test-9: the two flags add to the ones")
F8 = np.array(sets[12][0], float)
sv = np.linalg.svd(F8, compute_uv=False)
check(sv[-1] > 1e-3 and np.linalg.matrix_rank(F8) == 2, "test-13: independent, smallest singular value %.4g" % sv[-1])
check(abs(np.corrcoef(F8[:, 1], F8[:, 1])[0, 1]) > 0.99, "corr")
check(np.linalg.matrix_rank(np.array(F5, float)) == 2, "matrix_rank sees the decimal copy")
print("det(F^T F) for the decimal copy, as stored:", np.linalg.det(np.array(F5, float).T @ np.array(F5, float)))

# ---------- grading harness ----------
def _nan(v):
    return isinstance(v, float) and math.isnan(v)


def _tolist(v):
    if hasattr(v, "tolist"):
        return v.tolist()
    if isinstance(v, tuple):
        return [_tolist(x) for x in v]
    if isinstance(v, list):
        return [_tolist(x) for x in v]
    return v


def close(a, e, tol):
    a = _tolist(a)
    if isinstance(e, (list, tuple)):
        return isinstance(a, (list, tuple)) and len(a) == len(e) and all(close(x, y, tol) for x, y in zip(a, e))
    if isinstance(a, (list, tuple, dict)) or a is None or isinstance(a, str):
        return False
    try:
        a = float(a)
    except Exception:
        return False
    if _nan(a) or _nan(float(e)):
        return _nan(a) and _nan(float(e))
    return math.isclose(a, float(e), rel_tol=tol.get("rel", 0), abs_tol=tol.get("abs", 0))


def same(a, e):
    return _tolist(a) == e


def grade(src, pyodide=True):
    g = {}
    if pyodide:
        exec("import numpy as _np\n_os, _oi = _np.linalg.solve, _np.linalg.inv\n"
             "def _s(a, b):\n    a = _np.asarray(a, float)\n"
             "    if _np.linalg.matrix_rank(a) < a.shape[0]:\n        return _np.full(_np.shape(b), _np.nan)\n    return _os(a, b)\n"
             "def _i(a):\n    a = _np.asarray(a, float)\n"
             "    if _np.linalg.matrix_rank(a) < a.shape[0]:\n        return _np.full(a.shape, _np.nan)\n    return _oi(a)\n"
             "_np.linalg.solve, _np.linalg.inv = _s, _i\n", g)
    try:
        exec(compile(src, "main.py", "exec"), g)
        res = []
        for c in W["tests"]:
            try:
                exec(c["setup"], g)
                if c["compare"] == "raises":
                    try:
                        eval(c["call"], g)
                        res.append(False)
                    except Exception as ex:
                        res.append(type(ex).__name__ == c["expect"] or isinstance(ex, ValueError) and c["expect"] == "ValueError")
                    continue
                a = eval(c["call"], g)
                e = eval(c["expect"])
                res.append(close(a, e, c.get("tol", {"rel": 1e-9, "abs": 1e-12})) if c["compare"] == "isclose" else same(a, e))
            except Exception:
                res.append(False)
        return res
    finally:
        if pyodide:
            exec("_np.linalg.solve, _np.linalg.inv = _os, _oi\n", g)


HEAD = 'import numpy as np\n\ndef project_out(F, s):\n    F = np.array(F, dtype=float)\n    s = np.array(s, dtype=float)\n    n, k = F.shape\n'
TAIL = '    neutral = s - fitted\n    return P, fitted, neutral\n'
RANK = '    if np.linalg.matrix_rank(F) < k:\n        raise ValueError("dependent")\n'
QR = '    Qm, R = np.linalg.qr(F)\n    P = Qm @ Qm.T\n    fitted = P @ s\n'
FORM = '    P = F @ np.linalg.inv(F.T @ F) @ F.T\n    fitted = P @ s\n'

correct = {
    "shipped (QR)": W["solution"],
    "formula with rank check": HEAD + RANK + FORM + TAIL,
    "lstsq with its rank": HEAD + '    x, _, r, _ = np.linalg.lstsq(F, s, rcond=None)\n    if r < k:\n        raise ValueError("dependent")\n'
                           '    P = F @ np.linalg.solve(F.T @ F, F.T)\n    fitted = F @ x\n' + TAIL,
    "Gram-Schmidt by hand": HEAD + '    qs = []\n    for j in range(k):\n        v = F[:, j].copy()\n        for q in qs:\n            v = v - (q @ F[:, j]) * q\n'
                            '        if np.linalg.norm(v) <= 1e-10 * max(1.0, np.linalg.norm(F[:, j])):\n            raise ValueError("dependent")\n'
                            '        qs.append(v / np.linalg.norm(v))\n    P = sum(np.outer(q, q) for q in qs)\n    fitted = P @ s\n' + TAIL,
    "rank of the Gram matrix": HEAD + '    if np.linalg.matrix_rank(F.T @ F) < k:\n        raise ValueError("dependent")\n' + FORM + TAIL,
}
plants = {
    "no rank check, formula (silent)": (HEAD + FORM + TAIL, None),
    "no rank check, QR (silent)": (HEAD + QR + TAIL, None),
    "no rank check, lstsq/pinv (silent)": (HEAD + '    P = F @ np.linalg.pinv(F)\n    fitted = P @ s\n' + TAIL, None),
    "rank check by det == 0": (HEAD + '    if np.linalg.det(F.T @ F) == 0:\n        raise ValueError("dependent")\n' + FORM + TAIL, None),
    "refuses near-collinear (det < 1e-3)": (HEAD + '    if n < k or abs(np.linalg.det(F.T @ F)) < 1e-3:\n        raise ValueError("dependent")\n' + FORM + TAIL, None),
    "rank against rows, not columns": (HEAD + '    if np.linalg.matrix_rank(F) < n:\n        raise ValueError("dependent")\n' + FORM + TAIL, None),
    "Q.T @ Q (transpose on the wrong side)": (HEAD + RANK + '    Qm, R = np.linalg.qr(F)\n    P = Qm.T @ Qm\n    fitted = Qm @ (Qm.T @ s)\n' + TAIL, None),
    "last transpose missing": (HEAD + RANK + '    P = F @ np.linalg.inv(F.T @ F) @ F\n    fitted = P @ s\n' + TAIL, None),
    "sum of line projections": (HEAD + RANK + '    P = sum(np.outer(F[:, j], F[:, j]) / (F[:, j] @ F[:, j]) for j in range(k))\n    fitted = P @ s\n' + TAIL, None),
    "Gram-Schmidt without normalising": (HEAD + RANK + '    qs = []\n    for j in range(k):\n        v = F[:, j].copy()\n        for q in qs:\n            v = v - (q @ F[:, j]) / (q @ q) * q\n        qs.append(v)\n'
                                         '    P = sum(np.outer(q, q) for q in qs)\n    fitted = P @ s\n' + TAIL, None),
    "neutral = fitted - s (sign)": (HEAD + RANK + QR + '    neutral = fitted - s\n    return P, fitted, neutral\n', None),
    "inverse left out: s - F (F^T s)": (HEAD + RANK + QR + '    neutral = s - F @ (F.T @ s)\n    return P, fitted, neutral\n', None),
    "fitted and neutral swapped": (HEAD + RANK + QR + '    neutral = s - fitted\n    return P, neutral, fitted\n', None),
}

for name, src in correct.items():
    for py in (True, False):
        r = grade(src, py)
        check(all(r), f"correct '{name}' ({'Pyodide' if py else 'CPython'}) fails tests {[i + 1 for i, x in enumerate(r) if not x]}")
r = grade(W["starter"])
check(not any(r), f"starter passes some test: {[i + 1 for i, x in enumerate(r) if x]}")
print("starter fails", sum(1 for x in r if not x), "of", len(r))
for name, (src, _) in plants.items():
    r = grade(src, True)
    caught = [i + 1 for i, x in enumerate(r) if not x]
    rc = grade(src, False)
    caught_c = [i + 1 for i, x in enumerate(rc) if not x]
    check(len(caught) > 0 and len(caught_c) > 0, f"plant '{name}' passes every test")
    print(f"plant {name}: fails tests {caught} (Pyodide), {caught_c} (CPython)")

print(f"{checks} checks, {fails} failures")
sys.exit(1 if fails else 0)
