"""stat-learning L4 performance task h-kmeans: every number recomputed, and the tests shown to bite.

Run with the scratchpad venv (NumPy, scikit-learn 1.6.1). Exits 0 when
  - the shipped solution passes every example and hidden test (graded as app/js/engine/widgets/code.js does:
    isclose element by element at rel 1e-9, abs 1e-12 unless the case gives tol; equal otherwise),
  - an independent route gives every expected value: exact fractions for the six shares, a hand loop
    for the empty-cluster and one-step cases, scikit-learn KMeans(init=..., n_init=1) for the 60 shares,
  - the starter fails every test,
  - each planted wrong solution fails at least one hidden test.
"""
import json
import math
import os
import warnings
from fractions import Fraction as F

import numpy as np

warnings.filterwarnings('ignore')
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
HW = json.load(open(os.path.join(ROOT, 'app', 'content', 'courses', 'stat-learning', 'homework-4.json')))
ITEM = next(it for it in HW['items'] if it['id'] == 'h-kmeans')
W = ITEM['widget']
FAILS = []


def check(ok, msg):
    print(('ok   ' if ok else 'FAIL ') + msg)
    if not ok:
        FAILS.append(msg)


def flat(v):
    if hasattr(v, 'tolist'):
        v = v.tolist()
    if isinstance(v, tuple):
        v = list(v)
    if isinstance(v, list):
        return [flat(x) for x in v]
    return v


def same(a, e, how, tol):
    a, e = flat(a), flat(e)
    if isinstance(e, list):
        return isinstance(a, list) and len(a) == len(e) and all(same(x, y, how, tol) for x, y in zip(a, e))
    if how == 'isclose' and isinstance(e, (int, float)) and not isinstance(e, bool):
        if isinstance(a, bool) or not isinstance(a, (int, float)):
            return False
        return math.isclose(a, e, rel_tol=tol.get('rel', 0 if tol else 1e-9), abs_tol=tol.get('abs', 0 if tol else 1e-12))
    return a == e


def run(src, cases):
    ns = {'__learner_source__': src}
    try:
        exec(W['prelude'], ns)
        exec(src, ns)
    except Exception:
        return [False] * len(cases)
    out = []
    for t in cases:
        try:
            out.append(bool(same(eval(t['call'], ns), eval(t['expect']), t.get('compare', 'equal'), t.get('tol', {}))))
        except Exception:
            out.append(False)
    return out


tests, examples = W['tests'], W['examples']
check(len(tests) >= 3 and len(tests) > len(examples), f"{len(tests)} hidden tests, {len(examples)} example")
check(all(run(W['solution'], tests)) and all(run(W['solution'], examples)), "solution passes every test and example")
check(not any(run(W['starter'], tests)), "starter fails every test")

# ---- independent route
v = [F(10), F(12), F(14), F(30), F(32), F(40)]
ok2 = (sum(v[:3]) / 3, sum(v[3:]) / 3) == (12, 34) and sum((x - 12) ** 2 for x in v[:3]) + sum((x - 34) ** 2 for x in v[3:]) == 64
check(ok2, "six shares from 10, 12: centres 12, 34, inertia 64 (fractions)")
check(sum(v[1:]) / 5 == F(128, 5) and sum((x - F(128, 5)) ** 2 for x in v[1:]) == F(5872, 10), "one round (an assignment and its update): centre 25.6, inertia 587.2 (fractions)")
check("each round is one assignment and the update that follows it" in ITEM['prose'] and "`max_iter` assignments" not in ITEM['prose'], "the prose defines a round, so max_iter=1 includes the update")
check((v[1] + v[2]) / 2 == 13 and 0 + 1 + 1 + sum((x - 34) ** 2 for x in v[3:]) == 58, "bad start: 10, 13, 34, inertia 58 (fractions)")
# empty cluster by hand: E = 0, 1, 2, 10 from 0, 1, 100
E = [0.0, 1.0, 2.0, 10.0]; C = [0.0, 1.0, 100.0]; prev = None
while True:
    lab = [min(range(3), key=lambda j: (abs(x - C[j]), j)) for x in E]
    if lab == prev:
        break
    C = [sum(x for x, l in zip(E, lab) if l == j) / lab.count(j) if lab.count(j) else C[j] for j in range(3)]
    prev = lab
check(C == [1.0, 10.0, 100.0] and sum((x - C[l]) ** 2 for x, l in zip(E, lab)) == 2.0, "empty cluster: 1, 10, 100 kept, inertia 2 (hand loop)")
from sklearn.cluster import KMeans  # noqa: E402
from sklearn.preprocessing import StandardScaler  # noqa: E402
ns = {}
exec(W['prelude'], ns)
Z = ns['Z']
for rows in ([0, 1, 2], [0, 20, 40]):
    km = KMeans(3, init=Z[rows], n_init=1).fit(Z)
    check(round(km.inertia_, 4) == 14.1574 and sorted(np.bincount(km.labels_).tolist()) == [20, 20, 20], f"KMeans from rows {rows}: inertia 14.1574, groups of 20")

# ---- planted wrong solutions
BASE = W['solution']
PLANTED = {
    "no empty-cluster guard (mean of no rows)": BASE.replace("            if (labels == j).any():\n                C[j] = X[labels == j].mean(axis=0)", "            C[j] = X[labels == j].mean(axis=0)"),
    "one assign-update round only": BASE.replace("    for _ in range(max_iter):", "    for _ in range(1):"),
    "ignores max_iter": BASE.replace("    for _ in range(max_iter):", "    for _ in range(1000):"),
    "median instead of mean": BASE.replace("X[labels == j].mean(axis=0)", "np.median(X[labels == j], axis=0)"),
    "inertia about the old centres": BASE.replace("    for _ in range(max_iter):", "    old = C.copy()\n    for _ in range(max_iter):").replace("        for j in range(k):", "        old = C.copy()\n        for j in range(k):").replace("((X - C[labels]) ** 2)", "((X - old[labels]) ** 2)"),
    "plain distance in the inertia": BASE.replace("float(((X - C[labels]) ** 2).sum())", "float(np.sqrt(((X - C[labels]) ** 2).sum(axis=1)).sum())"),
    "ties to the higher index": BASE.replace("labels = d.argmin(axis=1)", "labels = len(C) - 1 - d[:, ::-1].argmin(axis=1)"),
    "assigns by absolute (Manhattan) distance": BASE.replace("d = ((X[:, None, :] - C[None, :, :]) ** 2).sum(axis=2)", "d = np.abs(X[:, None, :] - C[None, :, :]).sum(axis=2)"),
    "returns the centres from before the last update": BASE.replace("        for j in range(k):", "        keep = C.copy()\n        for j in range(k):").replace("    inertia = float", "    C = keep if max_iter == 1 else C\n    inertia = float"),
}
PLANTED["stops straight after the max_iter-th assignment (the reading the fix pass ruled out)"] = BASE.replace("        for j in range(k):", "        if _ == max_iter - 1:\n            break\n        for j in range(k):")
for slip, src in PLANTED.items():
    check(src != BASE, f"planted '{slip}' differs from the solution")
    res = run(src, tests)
    check(not all(res), f"planted '{slip}' fails {res.count(False)} of {len(res)} tests")

print(f"{len(FAILS)} failures")
raise SystemExit(1 if FAILS else 0)
