#!/usr/bin/env python3
"""Delta read AE-2: second-route recompute of the problems re-authored or re-keyed
by the three fix passes of session AE (stat-learning 1 to 3 with eigen p-crab-sizes,
ensembles 1 to 3, fin-ml 1 to 3).

Run with the scratchpad venv Python. Exit 0 on correct content. A row marked
FINDING fails while the content it describes is unchanged (see
docs/reviews/review-delta-ae-2.md). Rows marked PROPOSAL check the numbers of a
proposed fix and never depend on the content.
"""
import json
import math
import re
import sys
from fractions import Fraction as F
from pathlib import Path

import numpy as np
from scipy.optimize import minimize_scalar
from scipy.stats import norm

ROOT = Path(__file__).resolve().parents[2]
COURSES = ROOT / "app" / "content" / "courses"

checks = 0
fails = []


def ok(name, cond):
    global checks
    checks += 1
    if not cond:
        fails.append(name)
        print("FAIL", name)


def close(a, b, tol=1e-9):
    return abs(a - b) <= tol


def load(rel):
    return json.loads((COURSES / rel).read_text(encoding="utf-8"))


def item(rel, iid):
    for it in load(rel)["items"]:
        if it["id"] == iid:
            return it
    raise KeyError(iid)


EPS = 1e-9  # grade.js `within`: |value - answer| <= abs + 1e-9


def band(v, tol):
    return (v - tol - EPS, v + tol + EPS)


def inband(x, v, tol):
    return abs(x - v) <= tol + EPS


def check_numeric(tag, part, key, accepted, wrong):
    """key: expected answer. accepted: values the key band must take (the printed
    rounding and the unrounded value). wrong: {id: [values a learner reaches]}."""
    w = part["widget"]
    ok(f"{tag} kind numeric", w["kind"] == "numeric")
    tol = w.get("tol", {}).get("abs", 0)
    ok(f"{tag} key {key}", close(float(w["answer"]), key, 1e-12))
    for a in accepted:
        ok(f"{tag} key band takes {a}", inband(a, w["answer"], tol))
    entries = {e["id"]: e for e in w.get("wrong", [])}
    ok(f"{tag} wrong ids {sorted(wrong)}", sorted(entries) == sorted(wrong))
    bands = [("key", band(w["answer"], tol))]
    for wid, vals in wrong.items():
        e = entries.get(wid)
        if e is None:
            continue
        wt = e.get("tol", {}).get("abs", 0)
        for v in vals:
            ok(f"{tag} wrong[{wid}] takes {v}", inband(v, e["value"], wt))
            ok(f"{tag} key refuses {wid} {v}", not inband(v, w["answer"], tol))
        bands.append((wid, band(e["value"], wt)))
        ok(f"{tag} wrong[{wid}] has its own feedback", wid in part["feedback"].get("byKey", {}))
    for i in range(len(bands)):
        for j in range(i + 1, len(bands)):
            (na, (lo1, hi1)), (nb, (lo2, hi2)) = bands[i], bands[j]
            ok(f"{tag} bands {na} and {nb} disjoint", hi1 < lo2 or hi2 < lo1)


def has(tag, text, *needles):
    for n in needles:
        ok(f"{tag} prints {n!r}", n in text)


def all_text(part):
    out = [part.get("question", "")]
    fb = part.get("feedback", {})
    out += [fb.get("correct", ""), fb.get("generic", "")] + list(fb.get("byKey", {}).values())
    out.append(part.get("explain", {}).get("text", ""))
    for o in part.get("widget", {}).get("options", []):
        out += [o.get("text", ""), o.get("why", "")]
    return " ".join(out)


# ---------------------------------------------------------------------------
# 1. eigen/problems-3 p-crab-sizes
# ---------------------------------------------------------------------------
crab = item("eigen/problems-3.json", "p-crab-sizes")
nums = [int(x) for x in re.findall(r"\b\d+\b", crab["prose"])]
widths, claws = nums[0:5], nums[5:10]
ok("crab data read from prose", widths == [191, 151, 145, 139, 99] and claws == [88, 118, 85, 52, 82])
X = np.array([widths, claws], dtype=float).T
ok("crab means 145 and 85", close(X[:, 0].mean(), 145) and close(X[:, 1].mean(), 85))
S = np.cov(X.T, ddof=1)  # route 1: numpy
D = [(F(a) - 145, F(b) - 85) for a, b in zip(widths, claws)]  # route 2: exact
sxx = sum(d[0] ** 2 for d in D) / 4
sxy = sum(d[0] * d[1] for d in D) / 4
syy = sum(d[1] ** 2 for d in D) / 4
ok("crab Sigma exact 1076, 168, 549", (sxx, sxy, syy) == (1076, 168, 549))
ok("crab Sigma numpy", np.allclose(S, [[1076, 168], [168, 549]]))
p = crab["parts"]
raw = F(sum(a * b for a, b in zip(widths, claws)), 4)
check_numeric("crab p1", p[0], 168, [168], {"over-n": [float(sxy * 4 / 5)], "no-divide": [672], "raw": [float(raw)]})
has("crab p1", all_text(p[0]), "(46, 3)", "(6, 33)", "(-6, -33)", "(-46, -3)", "138 + 198 + 0 + 198 + 138 = 672", "672/4 = 168")
ok("crab p1 products", [int(d[0] * d[1]) for d in D] == [138, 198, 0, 198, 138])
vals, vecs = np.linalg.eigh(S)
ok("crab eigenvalues eigh 500, 1125", np.allclose(vals, [500, 1125]))
tr, det = sxx + syy, sxx * syy - sxy ** 2
ok("crab trace 1625, det 562500 = 590724 - 28224", tr == 1625 and det == 562500 and sxx * syy == 590724 and sxy ** 2 == 28224)
disc = tr ** 2 - 4 * det
ok("crab roots by the quadratic", math.isqrt(int(disc)) ** 2 == disc and {(tr + math.isqrt(int(disc))) / 2, (tr - math.isqrt(int(disc))) / 2} == {1125, 500})
w2 = p[1]["widget"]
ok("crab p2 key set", sorted(w2["answers"]) == [500, 1125] and w2.get("unordered") is True)
ok("crab p2 wrong diagonal, over-n", {e["id"]: e["value"] for e in w2["wrong"]} == {"diagonal": "1076, 549", "over-n": "900, 400"})
ok("crab p2 over-n = eigenvalues times 4/5", (1125 * 4 / 5, 500 * 4 / 5) == (900, 400))
has("crab p2", all_text(p[1]), "1625", "590724 - 28224 = 562500", "1125 \\times 500 = 562500")
ok("crab p2 restates 168", "168 from part 1" in p[1]["question"])
# part 3: the printed eigh output
m = re.search(r"vals = \[500\., 1125\.\]` and `vecs = \[\[(-?[\d.]+), (-?[\d.]+)\], \[(-?[\d.]+), (-?[\d.]+)\]\]", p[2]["question"])
ok("crab p3 printed vecs found", m is not None)
V = np.array([[float(m.group(1)), float(m.group(2))], [float(m.group(3)), float(m.group(4))]])
ok("crab p3 column 0 is an eigenvector for 500", np.allclose(S @ V[:, 0], 500 * V[:, 0]))
ok("crab p3 column 1 is an eigenvector for 1125", np.allclose(S @ V[:, 1], 1125 * V[:, 1]))
ok("crab p3 columns unit and orthogonal", np.allclose(V.T @ V, np.eye(2)))
pc1 = V[:, 1] * (1 if V[np.argmax(abs(V[:, 1])), 1] > 0 else -1)
ok("crab p3 sign rule gives (0.96, 0.28)", np.allclose(pc1, [0.96, 0.28]))
ok("crab p3 key and wrong", p[2]["widget"]["answer"] == "(0.96, 0.28)" and {e["id"]: e["tex"] for e in p[2]["widget"]["wrong"]} == {"first-column": "(-0.28, 0.96)", "no-flip": "(-0.96, -0.28)"})
ok("crab p3 first-column is vecs[:, 0], no-flip is vecs[:, -1]", np.allclose(V[:, 0], [-0.28, 0.96]) and np.allclose(V[:, 1], [-0.96, -0.28]))
ok("crab p3 accept forms equal the key", F(24, 25) == F("0.96") and F(7, 25) == F("0.28") and F("0.04") * 24 == F("0.96"))
scores = (X - X.mean(0)) @ np.array([0.96, 0.28])
ok("crab scores 45, 15, 0, -15, -45", np.allclose(scores, [45, 15, 0, -15, -45]))
check_numeric("crab p4", p[3], 45, [45], {"no-flip": [-45], "raw": [0.96 * 191 + 0.28 * 88], "pc2": [0.28 * 46 - 0.96 * 3], "first-column": [-0.28 * 46 + 0.96 * 3]})
has("crab p4", all_text(p[3]), "44.16 + 0.84 = 45", "(0.96, 0.28)$ from part 3")
ok("crab p4 parts 44.16 and 0.84", close(0.96 * 46, 44.16) and close(0.28 * 3, 0.84))
sd = scores.std(ddof=1)
ok("crab score variance 1125 (sample)", close(sd ** 2, 1125, 1e-6))
check_numeric("crab p5", p[4], 1.342, [45 / sd, round(45 / 33.541, 3)],
              {"variance": [45 / 1125], "total": [45 / math.sqrt(1625), round(45 / 40.311, 3)],
               "pc2-sd": [45 / math.sqrt(500), round(45 / 22.361, 3)]})
has("crab p5", all_text(p[4]), "33.541", "1125, the eigenvalue from part 2", "score 45 from part 4")
ok("crab sqrt(1125) = 33.541", round(math.sqrt(1125), 3) == 33.541)
# the slip of part 3 carried into part 4 (first column as PC1) gives -10, now listed as first-column (review finding 5, fixed)
ok("crab first-column carried gives -10", close(float((X - X.mean(0))[0] @ V[:, 0]), -10))
_fc = {w["id"]: w for w in p[3]["widget"]["wrong"]}
ok("FINDING 5 crab p4 first-column -10, tol 0, own byKey line, distinct from 45, -45, 208 and 10",
   _fc["first-column"]["value"] == -10 and _fc["first-column"]["tol"]["abs"] == 0 and "first-column" in p[3]["feedback"]["byKey"]
   and -10 not in (45, -45, 208, 10) and _fc["pc2"]["value"] == 10)

# every 2 by 2 matrix of the eigen course: none has (24, 7) or (7, -24) as an eigenvector
NUM = r"-?(?:\d+(?:\.\d+)?|\.\d+)"


def tonum(s):
    s = s.strip().replace("\\,", "").replace(" ", "").replace("−", "-")
    s = re.sub(r"^\\(?:t|d)?frac\{(-?[\d.]+)\}\{([\d.]+)\}$", r"\1/\2", s)
    s = re.sub(r"^-\\(?:t|d)?frac\{([\d.]+)\}\{([\d.]+)\}$", r"-\1/\2", s)
    s = re.sub(r"^\\(?:t|d)?frac(\d)(\d)$", r"\1/\2", s)
    s = re.sub(r"^-\\(?:t|d)?frac(\d)(\d)$", r"-\1/\2", s)
    if re.fullmatch(NUM, s):
        return float(s)
    mm = re.fullmatch(rf"({NUM})/({NUM})", s)
    if mm:
        return float(mm.group(1)) / float(mm.group(2))
    return None


def strings(o, skip_item=None):
    if isinstance(o, dict):
        if skip_item and o.get("id") == skip_item:
            return
        for v in o.values():
            yield from strings(v, skip_item)
    elif isinstance(o, list):
        for v in o:
            yield from strings(v, skip_item)
    elif isinstance(o, str):
        yield o


def matrices(text):
    for mm in re.finditer(r"\\begin\{[pbv]?matrix\}(.*?)\\end\{[pbv]?matrix\}", text, re.S):
        rows = [r.split("&") for r in re.split(r"\\\\", mm.group(1)) if r.strip()]
        if len(rows) == 2 and all(len(r) == 2 for r in rows):
            yield [tonum(c) for r in rows for c in r]
    for mm in re.finditer(rf"\[\s*\[\s*({NUM})\s*,\s*({NUM})\s*\]\s*,\s*\[\s*({NUM})\s*,\s*({NUM})\s*\]\s*\]", text):
        yield [float(g) for g in mm.groups()]


def json_matrices(o, skip_item=None):
    """2 by 2 numeric lists held as JSON data (canvas specs), not as text."""
    if isinstance(o, dict):
        if skip_item and o.get("id") == skip_item:
            return
        for v in o.values():
            yield from json_matrices(v, skip_item)
    elif isinstance(o, list):
        if (len(o) == 2 and all(isinstance(r, list) and len(r) == 2 and all(isinstance(c, (int, float)) and not isinstance(c, bool) for c in r) for r in o)):
            yield [float(c) for r in o for c in r]
        else:
            for v in o:
                yield from json_matrices(v, skip_item)


def is_eigvec(M, v):
    w = M @ v
    return abs(w[0] * v[1] - w[1] * v[0]) <= 1e-9 * max(1.0, np.abs(M).max()) * float(v @ v)


scanned = symbolic = scalar = 0
hits = []
files = sorted((COURSES / "eigen").glob("*.json"))
for fp in files:
    d = json.loads(fp.read_text(encoding="utf-8"))
    found = [ent for s in strings(d, skip_item="p-crab-sizes") for ent in matrices(s)] + list(json_matrices(d, "p-crab-sizes"))
    for ent in found:
        if True:
            if any(e is None for e in ent):
                symbolic += 1
                continue
            M = np.array(ent).reshape(2, 2)
            if abs(M[0, 1]) < 1e-12 and abs(M[1, 0]) < 1e-12 and abs(M[0, 0] - M[1, 1]) < 1e-12:
                scalar += 1  # a multiple of I: every vector is an eigenvector
                continue
            scanned += 1
            for Mx in (M, M.T):
                for v in (np.array([24.0, 7.0]), np.array([7.0, -24.0])):
                    if is_eigvec(Mx, v):
                        hits.append((fp.name, ent))
print(f"eigen scan: {len(files)} files, {scanned} numeric 2x2 matrices, {symbolic} symbolic, {scalar} multiples of I, {len(hits)} hits")
ok("eigen scan read at least 300 matrices", scanned >= 300)
ok("eigen: no matrix of the course (nor a transpose) has (24, 7) or (7, -24) as an eigenvector", not hits)
ok("eigen scan self-test: the crab matrix is caught", is_eigvec(np.array([[1076.0, 168.0], [168.0, 549.0]]), np.array([24.0, 7.0])))
ok("eigen scan self-test: a shift and scale of it is caught", is_eigvec(3 * np.array([[1076.0, 168.0], [168.0, 549.0]]) - 7 * np.eye(2), np.array([7.0, -24.0])))
# key numbers of the crab in the rest of the course
for n in ["1076", "549", "168", "1125", "562500", "1625", "672", "33.541", "15574"]:
    where = [fp.name for fp in files if fp.name != "problems-3.json" and re.search(rf"(?<![\d.]){re.escape(n)}(?![\d])", fp.read_text(encoding="utf-8"))]
    ok(f"eigen: {n} only in problems-3 (found {where})", not where)

# ---------------------------------------------------------------------------
# 2. stat-learning/problems-2 p-ice-cream-van (deckchair stall)
# ---------------------------------------------------------------------------
van = item("stat-learning/problems-2.json", "p-ice-cream-van")
van_text = " ".join([van["prose"]] + [all_text(x) for x in van["parts"]]).lower()
ok("stall: story words", "bike-hire stand" in van["prose"] and "deckchair" not in van_text and "ice-cream" not in van_text and "ice cream" not in van_text and "cone" not in van_text)
ok("stall: model in prose", "20 + 1.5x + 8w + 0.5xw" in van["prose"])


def yhat(x, w, inter=True, dummy=True):
    return 20 + 1.5 * x + (8 * w if dummy else 0) + (0.5 * x * w if inter else 0)


days = [(12, 1, 55), (10, 0, 33), (16, 0, 45), (6, 1, 38)]
pred = [yhat(x, w) for x, w, _ in days]
ok("stall forecasts 52, 35, 44, 40", pred == [52, 35, 44, 40])
q = van["parts"]
check_numeric("stall p1", q[0], 2.0, [2.0], {"weekday": [1.5], "interaction": [0.5]})
check_numeric("stall p2", q[1], 52, [52], {"no-interaction": [yhat(12, 1, inter=False)], "no-dummy": [yhat(12, 1, dummy=False)], "weekday": [yhat(12, 0)]})
mse = np.mean([(y - f) ** 2 for (_, _, y), f in zip(days, pred)])
mse_carried = np.mean([(y - yhat(x, w, inter=False)) ** 2 for x, w, y in days])
mae = np.mean([abs(y - f) for (_, _, y), f in zip(days, pred)])
check_numeric("stall p3", q[2], 4.5, [mse], {"carried": [mse_carried], "absolute": [mae], "sum": [mse * 4]})
ys = np.array([d[2] for d in days], dtype=float)
base = np.mean((ys - 40) ** 2)
base_test = np.mean((ys - ys.mean()) ** 2)
check_numeric("stall p4", q[3], 75.75, [base], {"test-mean": [base_test, 68.19], "absolute": [np.mean(abs(ys - 40))]})
ok("stall test mean 42.75", close(ys.mean(), 42.75))
check_numeric("stall p5", q[4], 0.941, [1 - mse / base, round(1 - 0.0594, 3)],
              {"ratio": [mse / base], "test-mean": [1 - 4.5 / 68.19, 1 - mse / base_test], "carried": [1 - mse_carried / base]})
has("stall p3", all_text(q[2]), "52, 35, 44 and 40", "3, -2, 1, -2", "18/4 = 4.5", "forecast 52 from part 2")
has("stall p4", all_text(q[3]), "15, -7, 5, -2", "225 + 49 + 25 + 4 = 303", "303/4 = 75.75", "42.75")
has("stall p5", all_text(q[4]), "4.5 from part 3 and 75.75 from part 4", "0.0594", "94.1%")
ok("bike-hire: a 6 degree Sunday is forecast 40 tens of bikes, plausible for bikes (review finding 7, fixed)", yhat(6, 1) == 40 and "bikes" in van["prose"])

# Session AF re-authored stat-learning p-futures-lasso and p-built-ridge (same ids, new problems) and
# p-renewals part 2; their old checks are removed here. The new items are checked in
# docs/reports/problems-stat-learning-numbers.py and docs/reports/delta-review-delta-af-1-numbers.py.

# ---------------------------------------------------------------------------
# 3. ensembles/problems-2 p-dividend-importance (re-authored: partial dependence)
# ---------------------------------------------------------------------------
dv = item("ensembles/problems-2.json", "p-dividend-importance")
d = dv["parts"]
trees = [F("0.60"), F("0.80"), F("0.70"), F("0.78")]
at20 = [sum(trees) / 4, F("0.84"), F("0.66"), F("0.14"), F("0.22"), F("0.12")]
at5 = [F("0.28"), F("0.36"), F("0.20"), F("0.10"), F("0.14"), F("0.12")]
ok("pd: tree values in the question", all(f"{float(t):.2f}" in d[0]["question"] for t in trees))
ok("pd: 20% values in the question", all(f"{float(t):.2f}" in d[1]["question"] for t in at20))
ok("pd: 5% values in the question", all(f"{float(t):.2f}" in d[2]["question"] for t in at5))
check_numeric("pd p1", d[0], 0.72, [float(sum(trees) / 4)], {"sum": [float(sum(trees))], "max": [float(max(trees))], "vote": [sum(t > F(1, 2) for t in trees) / 4]})
pd20, pd5 = sum(at20) / 6, sum(at5) / 6
check_numeric("pd p2", d[1], 0.45, [float(pd20)], {"sum": [float(sum(at20))], "first": [0.72], "five": [float(sum(at20[1:]) / 5), 0.40]})
ok("pd p2 five unrounded 0.396", sum(at20[1:]) / 5 == F("0.396"))
check_numeric("pd p3", d[2], 0.25, [float(pd20 - pd5)], {"start": [float(pd5)], "ratio": [float(pd20 / pd5)], "sum": [float(pd20 + pd5)]})
urg = (sum(at20[:3]) - sum(at5[:3])) / 3
calm = (sum(at20[3:]) - sum(at5[3:])) / 3
ok("pd calm rise 0.04, urgent rise 0.46, by the rows", calm == F("0.04") and urg == F("0.46"))
ok("pd urgent rise by the identity 2 x 0.25 - 0.04", 2 * (pd20 - pd5) - calm == urg)
check_numeric("pd p4", d[3], 0.46, [float(urg)], {"pd": [0.25], "double": [0.50], "added": [0.29]})
has("pd p4", all_text(d[3]), "0.84 at 5%", "2.22 at 20%", "1.38", "0.25 from part 3")
ok("pd p4 check sums", sum(at5[:3]) == F("0.84") and sum(at20[:3]) == F("2.22"))
has("pd p2", all_text(d[1]), "0.72 from part 1", "2.70", "2.70/6 = 0.45")
has("pd p3", all_text(d[2]), "0.45 from part 2", "1.20", "0.45 - 0.20 = 0.25")
opts = {o["id"]: o for o in d[4]["widget"]["options"]}
ok("pd p5 key urgent with 0.25, 0.46, 0.04", opts["urgent"].get("correct") and all(n in opts["urgent"]["text"] for n in ("0.25", "0.46", "0.04")))
ok("pd p5 every distractor has a why", all(o.get("why") for k, o in opts.items() if k != "urgent"))
# a real forest: predict_proba is the mean of the trees' probabilities (the claim of part 1)
from sklearn.ensemble import RandomForestClassifier  # noqa: E402
rng = np.random.default_rng(0)
Xr = rng.normal(size=(200, 3))
yr = (Xr[:, 0] + rng.normal(size=200) > 0).astype(int)
rf = RandomForestClassifier(n_estimators=4, max_depth=3, random_state=0).fit(Xr, yr)
ok("sklearn: forest probability is the mean of its trees'", np.allclose(rf.predict_proba(Xr)[:, 1], np.mean([t.predict_proba(Xr)[:, 1] for t in rf.estimators_], axis=0)))

# ---------------------------------------------------------------------------
# 4. ensembles/problems-3 p-futures-study (parts 3 and 4 new, choice reworded)
# ---------------------------------------------------------------------------
fs = item("ensembles/problems-3.json", "p-futures-study")
s = fs["parts"]
ok("study has 5 parts, 4 typed", len(s) == 5 and sum(x["widget"]["kind"] == "numeric" for x in s) == 4)
from sklearn.model_selection import TimeSeriesSplit  # noqa: E402
splits = list(TimeSeriesSplit(n_splits=4, test_size=60, gap=2).split(np.zeros(700)))
ok("study fold 1 test rows 460 to 519, training ends 457", splits[0][1][0] == 460 and splits[0][1][-1] == 519 and splits[0][0][-1] == 457)
ok("study four test blocks cover the last 240 days", sorted(np.concatenate([t for _, t in splits])) == list(range(460, 700)))
check_numeric("study p1", s[0], 457, [457], {"no-gap": [459], "gap-one": [458], "test-row": [460]})
hit, b0, n = F(138, 240), F(126, 240), 240
se = math.sqrt(float(b0 * (1 - b0)) / n)
tstat = float(hit - b0) / se
check_numeric("study p2", s[1], 1.55, [tstat, round(0.05 / 0.0322, 2)],
              {"fifty": [float(hit - F(1, 2)) / math.sqrt(0.25 / n)], "one-day": [float(hit - b0) / math.sqrt(float(b0 * (1 - b0)))],
               "hit-se": [float(hit - b0) / math.sqrt(float(hit * (1 - hit)) / n)]})
has("study p2", all_text(s[1]), "0.575", "0.525", "0.0322", "0.05/0.0322 = 1.55")
ok("study se 0.0322", round(se, 4) == 0.0322)
# review finding 6, fixed: the edge over 50% on the base-rate standard error is 2.33; fifty is now 2.325 +/- 0.006
_f = {e["id"]: e for e in s[1]["widget"]["wrong"]}["fifty"]
ok("FINDING 6 study p2 fifty at 2.325 +/- 0.006 takes 2.32, 2.3238, 2.3267 and 2.33 and stays off the key",
   _f["value"] == 2.325 and _f["tol"]["abs"] == 0.006
   and all(inband(v, 2.325, 0.006) for v in (2.32, 0.075 / math.sqrt(0.25 / 240), 0.075 / se, 2.33)) and not inband(1.5549, 2.325, 0.006))
move = F("0.008") * 2_000_000
gross = (138 * move - 102 * move) / 240  # route 2: the 240 days counted
ok("study gross by counting days = by (0.575 - 0.425) x 16000", gross == (hit - (1 - hit)) * move == 2400 and move == 16000)
check_numeric("study p3", s[2], 2400, [2400], {"edge-only": [float((hit - b0) * move)], "half": [float((hit - F(1, 2)) * move)], "hit-only": [float(hit * move)]})
has("study p3", all_text(s[2]), "hit rate 0.575 from part 2", "£16,000", "£800")
ok("study always-up expects 800", (b0 - (1 - b0)) * move == 800)
unit = F(7, 10000) * 2_000_000
net = gross - F(1, 4) * 2 * unit
ok("study cost by counting: 60 flips in 240 days at 2 x 1400", gross - F(60 * 2 * unit, 240) == net == 1700 and unit == 1400)
check_numeric("study p4", s[3], 1700, [1700], {"gross": [2400], "flip-one": [float(gross - F(1, 4) * unit)], "every-day": [float(gross - 2 * unit)]})
has("study p4", all_text(s[3]), "£2,400 a day from part 3", "7 bp", "£1{,}400", "£2{,}800", "£700", "£1,700", "costs take over a quarter")
ok("study p4 wrong values 2400, 2050, -400", (gross - unit / 4, gross - 2 * unit) == (2050, -400))
ok("study costs are 29% of gross", round(float(F(700) / gross), 2) == 0.29)
ok("study p5 at the base rate: gross 800, net 100; 240 days at 1700 is 408000",
   (b0 - (1 - b0)) * move == 800 and (b0 - (1 - b0)) * move - 700 == 100 and 240 * 1700 == 408000)
so = {o["id"]: o for o in s[4]["widget"]["options"]}
ok("study p5 key not-shown, four options", so["not-shown"].get("correct") is True and len(so) == 4 and sum(bool(o.get("correct")) for o in so.values()) == 1)
has("study p5", all_text(s[4]), "t = 1.55", "£1,700", "£100 a day", "£408,000", "£800", "£700")
ok("study p5 uses t from part 2 and the net from part 4 (the chain does not end at part 4)", "1.55" in s[4]["question"] and "1,700" in s[4]["question"])
ok("study p5 makes no label-overlap claim", "overlap" not in all_text(s[4]).lower())

# review findings 1 and 2, fixed: reuse inside ensembles level 3
rv3 = load("ensembles/review-3.json")
rv_pnl = next(it for it in rv3["items"] if it["id"] == "rv-pnl")
rv_txt = json.dumps(rv_pnl, ensure_ascii=False)
ok("FINDING 1 study p4: no £1,000 a unit or £2,000 a flip and no flip-one line of review-3 onecost",
   "£1{,}000" not in all_text(s[3]) and "£2{,}000" not in all_text(s[3]) and "Long to short is 2 units of £" not in all_text(s[3])
   and "£1,000" in rv_txt and "£2,000" in rv_txt)
l11 = json.dumps(load("ensembles/l11-gradient-boosting.json")["screens"][6], ensure_ascii=False)
rv_rand = json.dumps(next(it for it in rv3["items"] if it["id"] == "rv-random-val"), ensure_ascii=False)
t5 = all_text(s[4]).lower()
ok("FINDING 2 study p5: no random-validation scene and no 'stopping comes late' or 'later block' line of l11 and review-3",
   "random" not in t5 and "stopping" not in t5 and "later block" not in t5 and "comes late" not in t5
   and "stopping comes late" in l11 and "stopping came late" in rv_rand)
ens_l3 = " ".join((COURSES / "ensembles" / f).read_text(encoding="utf-8") for f in
                  ["l9-fixing-mistakes.json", "l10-small-steps.json", "l11-gradient-boosting.json", "l12-trees-on-returns.json", "review-3.json", "homework-3.json"])
ok("PROPOSAL study: £1,400, £2,800, £2,050 and £408,000 nowhere in ensembles level 3", not any(x in ens_l3 for x in ["£1,400", "£2,800", "£2,050", "£408,000", "£1{,}400", "£2{,}800"]))

# ---------------------------------------------------------------------------
# 5. fin-ml/problems-3 p-power-spread-cap (new) and p-futures-net-psr (re-banded)
# ---------------------------------------------------------------------------
pw = item("fin-ml/problems-3.json", "p-power-spread-cap")
k = pw["parts"]
pp, bb, cap = 0.70, 0.8, 0.20
ok("power: prose numbers", all(x in pw["prose"] for x in ("£0.80", "p = 0.70", "0.20 of capital")))


def g(f, win=bb, pw_=pp):
    return pw_ * math.log(1 + win * f) + (1 - pw_) * math.log(1 - f)


kelly = pp - (1 - pp) / bb
opt = minimize_scalar(lambda f: -g(f), bounds=(0.0, 0.99), method="bounded", options={"xatol": 1e-10})
ok("power Kelly 0.325 by formula and by maximising growth", close(kelly, 0.325) and abs(opt.x - 0.325) < 1e-5)
check_numeric("power p1", k[0], 0.325, [kelly], {"even-odds": [2 * pp - 1], "times-b": [pp - (1 - pp) * bb]})
has("power p1", all_text(k[0]), "0.375", "0.70 - 0.375 = 0.325")
gk = g(kelly)
check_numeric("power p2", k[1], 0.0439, [gk, round(0.1618 - 0.1179, 4)],
              {"even-payout": [g(kelly, win=1.0), round(0.7 * math.log(1.325), 4) - 0.1179],
               "swapped": [0.30 * math.log(1.26) + 0.70 * math.log(0.675)]})
has("power p2", all_text(k[1]), "Kelly 0.325 from part 1", "0.1618 - 0.1179 = 0.0439", "1.26", "0.675")
ok("power p2 terms 0.1618 and 0.1179", round(0.7 * math.log(1.26), 4) == 0.1618 and round(0.3 * math.log(0.675), 4) == -0.1179)
gc = g(cap)
check_numeric("power p3", k[2], 0.037, [gc, round(0.1039 - 0.0669, 4), 0.0370], {"uncapped": [gk, 0.0439], "even-payout": [g(cap, win=1.0), 0.0607]})
has("power p3", all_text(k[2]), "0.1039 - 0.0669 = 0.0370", "1.16", "0.0439")
ok("power p3 terms 0.1039 and 0.0669", round(0.7 * math.log(1.16), 4) == 0.1039 and round(0.3 * math.log(0.8), 4) == -0.0669)
ln2 = math.log(2)
check_numeric("power p4", k[3], 19, [math.ceil(ln2 / gc), math.ceil(ln2 / 0.0370)],
              {"kelly": [math.ceil(ln2 / gk), math.ceil(ln2 / 0.0439)], "round-down": [math.floor(ln2 / 0.0370)], "no-log": [math.ceil(1 / 0.0370)], "even-payout": [math.ceil(ln2 / 0.0607)]})
has("power p4", all_text(k[3]), "0.0370 a bet from part 3", "0.693/0.0370 = 18.7", "e^{18", "1.95", "15.8")
ok("power p4: 19 bets at the cap double, 18 do not; Kelly 16", math.exp(19 * gc) > 2 > math.exp(18 * gc) and math.ceil(ln2 / gk) == 16 and round(ln2 / gc, 2) == 18.76)
ko = {o["id"]: o for o in k[4]["widget"]["options"]}
ok("power p5 key sizing", ko["sizing"].get("correct") is True and len(ko) == 4)
l12 = json.dumps(load("fin-ml/l12-end-to-end.json")["screens"][0], ensure_ascii=False)
ok("power p5 order agrees with l12 screen 0", "calibration, sizing, costs, walk-forward with DSR, write-up" in l12)
# review finding 3, fixed: part 4 asks bets to double, no longer the share of growth kept (l9 screen 4, h-three-quarter)
l9 = load("fin-ml/l9-probability-to-position.json")["screens"]
h3 = next(it for it in load("fin-ml/homework-3.json")["items"] if it["id"] == "h-three-quarter")
share = re.compile(r"[Ww]hat share of .{0,30}growth.{0,40}keep")
ok("FINDING 3 power p4: no longer the share-kept question of l9 screen 4 and h-three-quarter", not share.search(k[3]["question"]) and share.search(l9[4]["question"]) and share.search(h3["question"]))
ok("FINDING 3 power p4: explain does not paraphrase 'flat near its peak'", "flat" not in k[3]["explain"]["text"] and "flat" not in k[4]["explain"]["text"])
ok("FINDING 3 power p5: explain no longer opens with l12 screen 0's 'each uses the one before'", "uses the one before" not in k[4]["explain"]["text"])
fin3 = " ".join((COURSES / "fin-ml" / f).read_text(encoding="utf-8") for f in
                ["l9-probability-to-position.json", "l10-costs-eat-edges.json", "l11-deflated-sharpe.json", "l12-end-to-end.json", "review-3.json", "homework-3.json"])
ok("PROPOSAL power p4: no doubling-time question in fin-ml level 3", "to double" not in fin3 and "doubling" not in fin3)

psr = item("fin-ml/problems-3.json", "p-futures-net-psr")
r = psr["parts"]
cost = 0.35 * 9
check_numeric("psr p1", r[0], 3.15, [cost], {"divided": [9 / 0.35], "both-ways": [2 * cost]})
sr_d = (6 - cost) / 75
check_numeric("psr p2", r[1], 0.6, [sr_d * math.sqrt(252), round(0.038 * 15.87, 2)], {"gross": [6 / 75 * math.sqrt(252)], "daily": [sr_d]})
has("psr p2", all_text(r[1]), "3.15 bp from part 1", "2.85", "15.87", "1.27")


def se_sr(sr, skew=-0.6, kurt=5.0, n_=750):
    return math.sqrt((1 - skew * sr + (kurt - 1) / 4 * sr ** 2) / (n_ - 1))


se3 = se_sr(0.038)
check_numeric("psr p3", r[2], 0.037, [se3, 0.0370],
              {"normal": [se_sr(0.038, 0, 3), 0.0366], "annual": [se_sr(0.60), se_sr(sr_d * math.sqrt(252)), 0.0479, 0.0480, 0.04792]})
has("psr p3", all_text(r[2]), "1.0242", "0.0228", "0.0014", "daily net Sharpe 0.038")
ok("psr p3 top 1.0242", round(1 + 0.6 * 0.038 + 0.038 ** 2, 4) == 1.0242)
psr_key = [norm.cdf(0.038 / 0.0370), norm.cdf(0.038 / se3), norm.cdf(1.03), 0.848, 0.849]
psr_normal = [norm.cdf(0.038 / 0.0366), norm.cdf(0.038 / se_sr(0.038, 0, 3)), norm.cdf(1.04), 0.850, 0.851]
check_numeric("psr p4", r[3], 0.848, psr_key, {"gross": [norm.cdf(0.08 / se_sr(0.08)), norm.cdf(0.08 / 0.0370)], "normal": psr_normal})
for v in psr_normal:
    ok(f"psr p4 key refuses the normal-error value {v:.4f}", not inband(v, 0.848, 0.0015))
has("psr p4", all_text(r[3]), "0.038 and the error 0.0370", "\\Phi(1.03) = 0.848", "0.984", "about 0.850")
ok("psr p4 z = 1.03", round(0.038 / 0.0370, 2) == 1.03)

# ---------------------------------------------------------------------------
# 6. fin-ml/problems-1 p-copper-breakout (threshold 0.55) and problems-2 p-shipping-z part 2
# ---------------------------------------------------------------------------
cu = item("fin-ml/problems-1.json", "p-copper-breakout")
rows = re.findall(r"\| (\d+) \| \$([+-]?\d)\$ \| \$([+-]?\d)\$ \| ([\d.]+) \|", cu["prose"])
ok("copper: 12 rows read", len(rows) == 12)
side = np.array([int(x[1]) for x in rows])
lab = np.array([int(x[2]) for x in rows])
prob = np.array([float(x[3]) for x in rows])
meta = (side * lab == 1).astype(int)
take = (prob >= 0.55).astype(int)
from sklearn.metrics import f1_score, precision_score, recall_score  # noqa: E402
c = cu["parts"]
check_numeric("copper p1", c[0], 5, [int(meta.sum())], {"price-up": [int((lab == 1).sum())], "time-wins": [int(meta.sum() + (lab == 0).sum())]})
check_numeric("copper p2", c[1], 0.4167, [meta.mean()], {"price-up": [4 / 12], "time-wins": [8 / 12]})
prec, rec, f1 = precision_score(meta, take), recall_score(meta, take), f1_score(meta, take)
ok("copper: 7 taken (1, 2, 3, 6, 8, 10, 12), 4 pay (1, 2, 6, 10), trade 7 missed",
   list(np.flatnonzero(take) + 1) == [1, 2, 3, 6, 8, 10, 12] and list(np.flatnonzero(take * meta) + 1) == [1, 2, 6, 10] and prob[6] == 0.52 and meta[6] == 1)
ok("copper exact 4/7, 4/5, 2/3", F(4, 7) == F(int((take * meta).sum()), int(take.sum())) and close(rec, 0.8) and 2 * F(4, 7) * F(4, 5) / (F(4, 7) + F(4, 5)) == F(2, 3))
check_numeric("copper p3", c[2], 0.5714, [prec], {"recall": [rec], "share-taken": [take.mean()]})
check_numeric("copper p4", c[3], 0.8, [rec], {"precision": [prec, 0.5714], "price-up": [((lab == 1) & (take == 1)).sum() / (lab == 1).sum()]})
check_numeric("copper p5", c[4], 0.6667, [f1, 2 * 0.5714 * 0.8 / (0.5714 + 0.8)], {"mean": [(prec + rec) / 2, (0.5714 + 0.8) / 2], "product": [prec * rec, 0.5714 * 0.8]})
has("copper p3", all_text(c[2]), "p \\ge 0.55", "1, 2, 3, 6, 8, 10 and 12", "4/7 = 0.5714", "7/12")
has("copper p4", all_text(c[3]), "5 paying calls from part 1", "p \\ge 0.55", "p = 0.52")
has("copper p5", all_text(c[4]), "\\tfrac47", "\\tfrac45", "32/35", "48/35", "0.4167 to 0.5714")
ok("copper: no 0.6 threshold left", "0.6$" not in json.dumps(cu) and "ge 0.6 " not in json.dumps(cu))
rv1 = json.dumps(load("fin-ml/review-1.json"), ensure_ascii=False)
ok("copper NOTE: base rate 5/12 still equals review-1 r-recall's 50/120; the threshold no longer does", "50/120 = 41.7" in rv1 and "threshold 0.6" in rv1 and F(5, 12) == F(50, 120))
lvl1 = " ".join((COURSES / "fin-ml" / f).read_text(encoding="utf-8") for f in
                ["l1-fixed-horizon.json", "l2-triple-barrier.json", "l3-meta-labelling.json", "l4-overlapping-labels.json", "review-1.json", "homework-1.json"])
ok("copper: 0.5714, 0.5833, 0.6857, 0.4571 nowhere in fin-ml level 1", not re.search(r"(?<![\d.])(0\.5714|0\.5833|0\.6857|0\.4571|58\.3|68\.6|45\.7)(?!\d)", lvl1))
ok("copper NOTE: 57.1% in l4 is the share of labels at the profit barrier, one number in another role", lvl1.count("57.1") == 1 and "57.1% of the series' 961 labels" in lvl1)

import statistics  # noqa: E402
sh = item("fin-ml/problems-2.json", "p-shipping-z")
h = sh["parts"]
win = [22, 21, 25]
sd_s, sd_p, mu = statistics.stdev(win), statistics.pstdev(win), statistics.mean(win)
check_numeric("shipping p1", h[0], 2.08, [sd_s], {"population": [sd_p], "variance": [sd_s ** 2]})
check_numeric("shipping p2", h[1], 1.12, [(25 - mu) / sd_s, (25 - 22.67) / 2.08],
              {"population": [(25 - mu) / sd_p, 2.33 / 1.70], "no-mean": [25 / sd_s, 25 / 2.08, 12.01, 12.02]})

print(f"{checks} checks, {len(fails)} failure(s)")
for f in fails:
    print(" -", f)
sys.exit(1 if fails else 0)
