"""Second read, linear-maps problems-1 to -3: is any matrix of the three sets used elsewhere?

Every matrix of the sets (those printed, and those a problem holds without printing: constraint rows,
basis matrices, maps, Gram matrices, data columns) is typed below. Every matrix of the course's lessons,
reviews and homework, of `exams/topic-1.10.json` and of the `eigen`, `vectors` and `elimination` courses
is read from the JSON: pmatrix / bmatrix / vmatrix text, `[[a, b], [c, d]]` strings and nested numeric
lists (canvas rows). Two matrices match when one is the other up to a non-zero scalar, a transpose and
any reordering of rows and of columns. Identity-like and one-line matrices are not searched.

Also searched, as exact tuples up to a scalar: the vectors of the sets with three or more entries, and
the polynomials' coefficient lists.

Run from the repo root:  python3 docs/reviews/review-problems-linear-maps-1-3-scripts/matrices.py [--all]
(--all searches every file under app/content, not only the scope above)
"""
import glob
import itertools
import json
import re
import sys
from fractions import Fraction as Fr

ALL = "--all" in sys.argv
OWN = {f"app/content/courses/linear-maps/problems-{n}.json" for n in (1, 2, 3)}
if ALL:
    FILES = sorted(set(glob.glob("app/content/**/*.json", recursive=True)) - OWN)
else:
    FILES = sorted(set(glob.glob("app/content/courses/linear-maps/*.json")) - OWN) \
        + ["app/content/exams/topic-1.10.json"] \
        + sorted(glob.glob("app/content/courses/eigen/*.json")) \
        + sorted(glob.glob("app/content/courses/vectors/*.json")) \
        + sorted(glob.glob("app/content/courses/elimination/*.json"))
FILES = [f for f in FILES if not f.endswith("manifest.json")]

F = Fr
MINE = {
    # problems-1
    "p-hedge-baskets rules of U": [[1, 1, 1, 1], [1, 0, 0, -2]],
    "p-hedge-baskets rules of W": [[1, 1, 1, 1], [0, 1, -1, 0]],
    "p-hedge-baskets rules of U cap W": [[1, 1, 1, 1], [1, 0, 0, -2], [0, 1, -1, 0]],
    "p-hedge-baskets basis of U": [[2, 0], [-1, 1], [-2, -1], [1, 0]],
    "p-hedge-curves coefficient columns p1 p2 p3": [[3, 0, 1], [1, 1, 0], [1, -2, 1]],
    "p-hedge-curves p2 p3": [[0, 1], [1, 0], [-2, 1]],
    "p-hedge-curves p2 p3 x^2": [[0, 1, 0], [1, 0, 0], [-2, 1, 1]],
    "p-scenario-space u v": [[4, 5], [30, 60]],
    "p-scenario-space moves": [[1, 2], [-10, 20]],
    # problems-2
    "p-curve-report matrix of T": [[1, 2, 4, 8], [0, 1, 4, 12]],
    "p-curve-report wrong unevaluated": [[1, 2, 4, 8], [0, 1, 2, 3]],
    "p-curve-report wrong carried": [[1, 2, 4, 8], [0, 1, 4, 6]],
    "p-curve-report T on lines": [[1, 2], [0, 1]],
    "p-futures-exposure A": [[1, 2], [-1, 4]],
    "p-futures-exposure P": [[1, 2], [1, 3]],
    "p-futures-exposure [T]_B": [[3, 4], [0, 2]],
    "p-futures-exposure [T]_B inverse": [[F(1, 3), F(-2, 3)], [0, F(1, 2)]],
    "p-futures-exposure adjugate": [[2, -4], [0, 3]],
    "p-futures-exposure wrong entrywise": [[F(1, 3), F(1, 4)], [0, F(1, 2)]],
    "p-futures-exposure wrong sign": [[F(1, 3), F(2, 3)], [0, F(1, 2)]],
    "p-futures-exposure A inverse": [[F(2, 3), F(-1, 3)], [F(1, 6), F(1, 6)]],
    "p-slope-adjusted matrix of T": [[1, -1, 0], [0, 1, -2], [0, 0, 1]],
    "p-slope-adjusted matrix of T inverse": [[1, 1, 2], [0, 1, 2], [0, 0, 1]],
    # problems-3
    "p-currency-duals basis": [[5, 4], [1, 1]],
    "p-currency-duals dual basis rows": [[1, -4], [-1, 5]],
    "p-currency-duals T": [[2, -1], [1, 3]],
    "p-currency-duals weights": [[2, 0], [0, 1]],
    "p-index-beta a b": [[1, 3], [-1, 0], [0, -2], [1, 2], [-1, -3]],
    "p-index-beta Gram (covariance)": [[1, 2], [2, F(13, 2)]],
    "p-two-signal-fit u1 u2": [[1, 2], [1, 1], [0, 1], [1, 3]],
    "p-two-signal-fit Gram": [[3, 6], [6, 15]],
    "p-two-signal-fit u1 f2": [[1, 0], [1, -1], [0, 1], [1, 1]],
    "p-two-signal-fit u1 u2 v": [[1, 2, 4], [1, 1, 2], [0, 1, 5], [1, 3, 3]],
}
VECS = {
    "p-hedge-baskets b1": [2, -1, -2, 1], "p-hedge-baskets b2": [0, 1, -1, 0], "p-hedge-baskets w": [4, 3, -9, 2],
    "p-hedge-baskets U cap W": [4, -3, -3, 2],
    "p-hedge-curves p1": [3, 1, 1], "p-hedge-curves q": [5, -1, 4], "p-hedge-curves key": [-1, 5, -3],
    "p-hedge-curves fourth, k = -1": [4, -1, 6],
    "p-curve-report key": [7, -5, 2], "p-slope-adjusted T(3x^2+x)": [-1, -5, 3], "p-slope-adjusted key": [5, 2, 1],
    "p-index-beta a": [1, -1, 0, 1, -1], "p-index-beta b": [3, 0, -2, 2, -3], "p-index-beta r": [1, 2, -2, 0, -1],
    "p-two-signal-fit v": [4, 2, 5, 3], "p-two-signal-fit u1": [1, 1, 0, 1], "p-two-signal-fit u2": [2, 1, 1, 3],
    "p-two-signal-fit f2": [0, -1, 1, 1], "p-two-signal-fit P_U v": [3, 1, 2, 5], "p-two-signal-fit residual": [1, 1, 3, -2],
}


def scale(m):
    flat = [e for r in m for e in r]
    lead = next((e for e in flat if e != 0), None)
    if lead is None:
        return None
    return tuple(tuple(Fr(e) / lead for e in r) for r in m)


def canon(m):
    """Least form over transpose, row order, column order and scale."""
    m = [[Fr(e) for e in r] for r in m]
    best = None
    for mm in (m, [list(c) for c in zip(*m)]):
        nr, nc = len(mm), len(mm[0])
        if nr > 5 or nc > 5:
            rows_perms = [tuple(range(nr))]
            cols_perms = [tuple(range(nc))]
        else:
            rows_perms = list(itertools.permutations(range(nr)))
            cols_perms = list(itertools.permutations(range(nc)))
        for rp in rows_perms:
            for cp in cols_perms:
                s = scale([[mm[i][j] for j in cp] for i in rp])
                if s is not None and (best is None or (len(s), len(s[0]), s) < best):
                    best = (len(s), len(s[0]), s)
    return best


def trivial(m):
    nr, nc = len(m), len(m[0])
    if nr < 2 or nc < 2:
        return True
    nz = [(i, j) for i in range(nr) for j in range(nc) if m[i][j] != 0]
    # a scaled permutation of the identity: one non-zero per row and column, all equal
    if len(nz) <= min(nr, nc) and len({i for i, _ in nz}) == len(nz) and len({j for _, j in nz}) == len(nz) \
            and len({m[i][j] for i, j in nz}) <= 1:
        return True
    return False


NUM = re.compile(r"^\s*(-?)\s*(?:\\[td]?frac\{(\d+)\}\{(\d+)\}|(\d+(?:\.\d+)?)(?:/(\d+))?)\s*$")


def entry(s):
    s = s.replace("\\,", "").replace("\\phantom{-}", "").replace("−", "-").strip()
    s = re.sub(r"^\{(.*)\}$", r"\1", s)
    m = NUM.match(s)
    if not m:
        m2 = re.match(r"^\s*\\[td]?frac\{(-?\d+)\}\{(\d+)\}\s*$", s)
        if m2:
            return Fr(int(m2.group(1)), int(m2.group(2)))
        return None
    sign = -1 if m.group(1) else 1
    if m.group(2):
        return sign * Fr(int(m.group(2)), int(m.group(3)))
    v = Fr(m.group(4))
    if m.group(5):
        v /= int(m.group(5))
    return sign * v


TEXM = re.compile(r"\\begin\{([pbvB]?matrix|array)\}(?:\{[^}]*\})?(.*?)\\end\{\1\}", re.S)
LISTM = re.compile(r"\[\s*\[[^\[\]]*\](?:\s*,\s*\[[^\[\]]*\])+\s*\]")


def from_string(s):
    out = []
    for m in TEXM.finditer(s):
        rows = [r for r in re.split(r"\\\\", m.group(2)) if r.strip()]
        mat = [[entry(c) for c in r.split("&")] for r in rows]
        if mat and all(len(r) == len(mat[0]) for r in mat) and all(e is not None for r in mat for e in r):
            out.append(mat)
    for m in LISTM.finditer(s):
        rows = re.findall(r"\[([^\[\]]*)\]", m.group(0)[1:-1])
        mat = [[entry(c) for c in r.split(",")] for r in rows]
        if mat and all(len(r) == len(mat[0]) for r in mat) and all(e is not None for r in mat for e in r):
            out.append(mat)
    return out


def is_num(e):
    return isinstance(e, (int, float)) and not isinstance(e, bool)


def walk(o, path, out, vecs):
    if isinstance(o, str):
        for m in from_string(o):
            out.append((path, m))
        for m in re.finditer(r"\(((?:\s*-?\d+(?:\.\d+)?\s*,){2,}\s*-?\d+(?:\.\d+)?\s*)\)", o):
            vecs.append((path, [Fr(c.strip()) for c in m.group(1).split(",")]))
    elif isinstance(o, list):
        if len(o) >= 2 and all(isinstance(r, list) and len(r) >= 2 and all(is_num(e) for e in r) for r in o) \
                and len({len(r) for r in o}) == 1:
            out.append((path, [[Fr(str(e)) for e in r] for r in o]))
        elif len(o) >= 3 and all(is_num(e) for e in o):
            vecs.append((path, [Fr(str(e)) for e in o]))
        for i, e in enumerate(o):
            walk(e, f"{path}[{i}]", out, vecs)
    elif isinstance(o, dict):
        for k_, e in o.items():
            walk(e, f"{path}.{k_}", out, vecs)


def vcanon(v):
    lead = next((e for e in v if e != 0), None)
    return None if lead is None else tuple(Fr(e) / lead for e in v)


index, vindex, n_m = {}, {}, 0
for f in FILES:
    try:
        d = json.load(open(f))
    except Exception:
        continue
    found, vecs = [], []
    walk(d, "", found, vecs)
    for path, m in found:
        if trivial(m):
            continue
        n_m += 1
        index.setdefault(canon(m), []).append((f.replace("app/content/", ""), path, m))
    for path, v in vecs:
        c = vcanon(v)
        if c is not None:
            vindex.setdefault(c, []).append((f.replace("app/content/", ""), path))

# the sets' own printed matrices must all be in MINE (so none is missed)
own_printed, own_canon = 0, {canon(m) for m in MINE.values()}
for f in sorted(OWN):
    found, vecs = [], []
    walk(json.load(open(f)), "", found, vecs)
    for path, m in found:
        if not trivial(m):
            own_printed += 1
            if canon(m) not in own_canon:
                print("NOT TYPED in MINE:", f, path, m)

fmt = lambda m: "[" + ", ".join("[" + ", ".join(str(e) for e in r) + "]" for r in m) + "]"
print(f"scope: {len(FILES)} files, {n_m} non-trivial matrices, {len(vindex)} distinct vectors (3 or more entries, up to scale)")
print(f"own: {len(MINE)} matrices typed ({own_printed} printed in the sets, all covered), {len(VECS)} vectors")
hits = 0
for name, m in MINE.items():
    got = index.get(canon(m), [])
    if got:
        hits += 1
        print(f"MATCH {name} {fmt(m)}: {len(got)} place(s)")
        seen = set()
        for f, path, mm in got:
            if (f, fmt(mm)) in seen:
                continue
            seen.add((f, fmt(mm)))
            if len(seen) > 8:
                print("    ...")
                break
            print(f"    {f} {path[:70]} {fmt(mm)}")
vh = 0
for name, v in VECS.items():
    got = vindex.get(vcanon(v), [])
    if got:
        vh += 1
        fs = sorted({f for f, _ in got})
        print(f"VECTOR {name} {tuple(str(e) for e in v)}: {len(got)} place(s) in {fs[:6]}")
print(f"\nmatrices.py: {hits} of {len(MINE)} matrices matched, {vh} of {len(VECS)} vectors matched")
