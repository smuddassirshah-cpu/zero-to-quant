"""mock-oa-quant-data: builds app/content/exams/mock-oa-quant-data.json and checks every keyed number twice.

Run: python3 -I oa_quant_data_build.py [scratch dir for the Pyodide case file]   (standard library only).
Needs qd_tasks_tests.json (from qd_tasks.py) and data/qd-*.csv (from gen_qd_data.py) beside it.

Paper 1: each number is computed in closed form and again by a second route (an exact enumeration, a linear solve,
a series), as Fractions, and the script asserts they agree.  Paper 2: the hidden tests come from qd_tasks_tests.json;
this script re-derives every expected value from the decimal text of the CSVs in pure Python (Fractions) as a
second method, builds the three small worked examples, and writes the code variants (starters, reference solutions,
alternative right solutions, wrong versions) for the Pyodide run (pyo_run.mjs).
Ends with ALL AGREE.
"""
import csv, json, math, os, random, re, statistics, sys
from fractions import Fraction as F

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
OUT = os.path.join(ROOT, "app", "content", "exams", "mock-oa-quant-data.json")
DATA = os.path.join(HERE, "data")
SCRATCH = sys.argv[1] if len(sys.argv) > 1 else None
NOTES = []


def two(label, a, b, tol=0):
    ok = (a == b) if tol == 0 else abs(float(a) - float(b)) <= tol
    assert ok, f"DISAGREE {label}: {a} vs {b}"
    NOTES.append(f"OK  {label}: A={float(a):.6g}  B={float(b):.6g}")


# ============================================================================== paper 1 numbers, each twice
def paper1_numbers():
    two("Q1 half-width 1.96 s / sqrt(n)", F(196, 100) * 12 / 6, F(98, 25))
    two("Q1 via sqrt(s^2 / n) x 1.96", F(math.sqrt(144 / 36)).limit_denominator(100) * F(196, 100), F(98, 25))
    two("Q1 wrong: s x 1.96 (no root n)", F(196, 100) * 12, F(2352, 100))
    two("Q3 t = mean / (s / sqrt n)", F(18, 10) / (F(5) / 5), F(9, 5))
    two("Q3 t^2 = n mean^2 / s^2", F(25) * F(18, 10) ** 2 / 25, F(9, 5) ** 2)
    two("Q3 wrong: mean / (s / n)", F(18, 10) / (F(5) / 25), F(9))
    two("Q3 wrong: mean / s", F(18, 10) / 5, F(36, 100))
    adj = 1 - (1 - F(2, 5)) * F(49, 45)
    two("Q5 adjusted R^2", adj, F(2, 5) - (1 - F(2, 5)) * F(4, 45))
    two("Q5 value 26/75", adj, F(26, 75))
    assert round(float(adj), 4) == 0.3467
    wrong_nk = 1 - (1 - F(2, 5)) * F(49, 46)
    assert round(float(wrong_nk), 4) == 0.3609
    # Q6
    mx, my, sx, sy, rho, x = F(1), F(4), F(3), F(2), F(3, 5), F(5)
    cm = my + rho * sy / sx * (x - mx)
    cov = rho * sx * sy
    two("Q6 p1 E[Y|X=5] slope form vs matrix form", cm, my + cov / (sx * sx) * (x - mx))
    two("Q6 p1 value 28/5", cm, F(28, 5))
    cv = sy ** 2 * (1 - rho ** 2)
    two("Q6 p2 Var[Y|X=5] vs Syy - Syx^2/Sxx", cv, sy ** 2 - cov * cov / (sx * sx))
    two("Q6 p2 sd 1.6 since 1.6^2 = 2.56", cv, F(16, 10) ** 2)
    assert my + rho * (x - mx) == F(32, 5)  # the 6.4 slip: correlation used as the slope
    assert rho * sy == F(6, 5)  # the 1.2 slip
    # Q7
    w, s, c = [F(3, 5), F(2, 5)], [F(1, 5), F(3, 10)], F(-3, 10)
    v1 = w[0] ** 2 * s[0] ** 2 + w[1] ** 2 * s[1] ** 2 + 2 * w[0] * w[1] * c * s[0] * s[1]
    S = [[s[0] ** 2, c * s[0] * s[1]], [c * s[0] * s[1], s[1] ** 2]]
    two("Q7 variance expanded vs w'Sw", v1, sum(w[i] * S[i][j] * w[j] for i in range(2) for j in range(2)))
    two("Q7 variance 0.02016", v1, F(2016, 100000))
    assert abs(math.sqrt(v1) - 0.1420) < 5e-5 and round(math.sqrt(v1) * 100, 1) == 14.2
    assert w[0] * s[0] + w[1] * s[1] == F(6, 25)  # 24.0 slip
    assert round(math.sqrt(w[0] ** 2 * s[0] ** 2 + w[1] ** 2 * s[1] ** 2) * 100, 1) == 17.0  # 17.0 slip
    # Q8
    a, b, cc = F(1, 16), F(1, 25), F(3, 10) * F(1, 4) * F(1, 5)
    assert cc == F(3, 200)
    wt = (b - cc) / (a + b - 2 * cc)
    var = lambda t: t * t * a + (1 - t) ** 2 * b + 2 * t * (1 - t) * cc
    best = min([F(i, 290) for i in range(291)], key=var)
    two("Q8 min-variance weight closed form vs exact grid argmin", wt, best)
    two("Q8 value 10/29", wt, F(10, 29))
    assert round(float(wt), 4) == 0.3448
    two("Q8 wrong: inverse variance", (1 / a) / (1 / a + 1 / b), F(16, 41))
    assert round(16 / 41, 4) == 0.3902
    # Q10
    lam, mu, sd = 4, 10, 5
    closed = lam * (sd ** 2 + mu ** 2)
    pn = lambda k: math.exp(-lam) * lam ** k / math.factorial(k)
    ES = sum(pn(k) * k * mu for k in range(80))
    ES2 = sum(pn(k) * (k * sd ** 2 + (k * mu) ** 2) for k in range(80))
    two("Q10 variance of the total, closed form vs sum over N", closed, ES2 - ES ** 2, 1e-9)
    assert (closed, lam * sd ** 2, lam * mu ** 2, lam * mu) == (500, 100, 400, 40)
    # Q4
    xs, ys = [F(v) for v in (1, 2, 4, 5, 8)], [F(v) for v in (3, 4, 8, 7, 13)]
    n = len(xs)
    mxx, myy = sum(xs) / n, sum(ys) / n
    bb = sum((p - mxx) * (q - myy) for p, q in zip(xs, ys)) / sum((p - mxx) ** 2 for p in xs)
    aa = myy - bb * mxx
    two("Q4 residuals of a 5-point fit sum to zero", sum(q - aa - bb * p for p, q in zip(xs, ys)), 0)
    two("Q4 the line passes through the point of means", aa + bb * mxx, myy)

    def sse(cols, y):  # exact normal equations by Gauss-Jordan; None if collinear
        X = [[F(1)] + [col[i] for col in cols] for i in range(len(y))]
        k = len(X[0])
        A = [[sum(r[i] * r[j] for r in X) for j in range(k)] + [sum(r[i] * v for r, v in zip(X, y))] for i in range(k)]
        for c0 in range(k):
            piv = next((r for r in range(c0, k) if A[r][c0] != 0), None)
            if piv is None:
                return None
            A[c0], A[piv] = A[piv], A[c0]
            A[c0] = [v / A[c0][c0] for v in A[c0]]
            for r in range(k):
                if r != c0 and A[r][c0] != 0:
                    f = A[r][c0]
                    A[r] = [u - f * v for u, v in zip(A[r], A[c0])]
        beta = [A[i][k] for i in range(k)]
        return sum((v - sum(bi * xi for bi, xi in zip(beta, r))) ** 2 for r, v in zip(X, y))

    rng = random.Random(3501)
    fits = fell = 0
    for _ in range(2000):
        m = 8
        y = [F(rng.randint(0, 9)) for _ in range(m)]
        c1 = [F(rng.randint(0, 9)) for _ in range(m)]
        c2 = [F(rng.randint(0, 9)) for _ in range(m)]
        s1, s2 = sse([c1], y), sse([c1, c2], y)
        sst = sum((v - sum(y) / m) ** 2 for v in y)
        if s1 is None or s2 is None or sst == 0:
            continue
        fits += 1
        assert s2 <= s1
        if 1 - (s2 / (m - 3)) / (sst / (m - 1)) < 1 - (s1 / (m - 2)) / (sst / (m - 1)):
            fell += 1
    assert fits > 1500 and fell > 50
    NOTES.append(f"OK  Q4 SSE never rose in {fits} exact fits; adjusted R^2 fell in {fell} of them")
    return {"q4_fits": fits, "q4_fell": fell}


# ============================================================================== paper 2: second method, from the text
def read(name):
    return list(csv.DictReader(open(os.path.join(DATA, name))))


def pure_task1(rows):
    seen, keep = set(), []
    for r in rows:
        k = (r["date"], r["ticker"], r["close"])
        if k in seen:
            continue
        seen.add(k)
        if r["close"] != "":
            keep.append((r["ticker"], r["date"], float(r["close"])))
    keep.sort()
    by = {}
    for t, d, c in keep:
        by.setdefault(t, []).append(c)
    return {t: statistics.stdev([math.log(q / p) for p, q in zip(cs, cs[1:])]) * math.sqrt(252) for t, cs in by.items()}, {t: len(cs) for t, cs in by.items()}, len(keep)


def pure_betas(pairs, w):  # pairs: (asset, mkt) as Fractions, errors already dropped
    out = []
    for i in range(len(pairs) - w + 1):
        win = pairs[i:i + w]
        mx, my = sum(p[1] for p in win) / w, sum(p[0] for p in win) / w
        out.append(sum((p[1] - mx) * (p[0] - my) for p in win) / sum((p[1] - mx) ** 2 for p in win))
    return out


def solve(A, b):
    n = len(A)
    M = [r[:] + [v] for r, v in zip(A, b)]
    for c in range(n):
        p = next(r for r in range(c, n) if M[r][c] != 0)
        M[c], M[p] = M[p], M[c]
        M[c] = [v / M[c][c] for v in M[c]]
        for r in range(n):
            if r != c and M[r][c] != 0:
                f = M[r][c]
                M[r] = [u - f * v for u, v in zip(M[r], M[c])]
    return [M[i][n] for i in range(n)]


def pure_oos(rows, split):
    x1, x2, ret = [F(r["x1"]) for r in rows], [F(r["x2"]) for r in rows], [F(r["ret"]) for r in rows]
    X = [[F(1), x1[t - 1], x2[t - 1]] for t in range(1, len(rows))]
    y = ret[1:]
    return fit_score(X, y, split)


def fit_score(X, y, split):
    Xtr, ytr, Xte, yte = X[:split], y[:split], X[split:], y[split:]
    A = [[sum(r[i] * r[j] for r in Xtr) for j in range(3)] for i in range(3)]
    b = [sum(r[i] * v for r, v in zip(Xtr, ytr)) for i in range(3)]
    c = solve(A, b)
    pred = lambda r: sum(ci * ri for ci, ri in zip(c, r))
    mtr = sum(ytr) / len(ytr)
    tr = 1 - sum((v - pred(r)) ** 2 for r, v in zip(Xtr, ytr)) / sum((v - mtr) ** 2 for v in ytr)
    te = 1 - sum((v - pred(r)) ** 2 for r, v in zip(Xte, yte)) / sum((v - mtr) ** 2 for v in yte)
    return c, tr, te


def isc(a, b, rel):
    return abs(a - b) <= rel * max(abs(a), abs(b), 1e-300)


def small_examples():
    """Three worked examples, each on a tiny file the example writes over the real one for that run only."""
    ex = {}
    # task 1: AAA has a repeated row, BBB a blank on the first day; BBB then appears again with a close
    prices = "date,ticker,close\\n2025-01-03,AAA,11\\n2025-01-02,AAA,10\\n2025-01-02,AAA,10\\n2025-01-02,BBB,\\n2025-01-02,BBB,20\\n2025-01-03,BBB,22\\n2025-01-06,BBB,21\\n2025-01-06,AAA,12\\n"
    rows = list(csv.DictReader(prices.replace("\\n", "\n").splitlines()))
    vols, counts, n = pure_task1(rows)
    assert counts == {"AAA": 3, "BBB": 3} and n == 6
    ex["t1"] = [
        {"setup": f"open('qd-prices.csv', 'w').write('{prices}')", "call": "tidy_closes()['close'].tolist()", "expect": "[10.0, 11.0, 12.0, 20.0, 22.0, 21.0]", "compare": "equal"},
        {"setup": f"open('qd-prices.csv', 'w').write('{prices}')", "call": "vol_by_ticker()['BBB']", "expect": repr(vols["BBB"]), "compare": "isclose", "tol": {"rel": 1e-9}},
    ]
    two("T1 example BBB volatility, pure Python vs closed form", F(vols["BBB"]).limit_denominator(10 ** 9), F(statistics.stdev([math.log(22 / 20), math.log(21 / 22)]) * math.sqrt(252)).limit_denominator(10 ** 9), 1e-9)
    # task 2: six rows, one error (0.31) in the asset column
    mkt = ["0.01", "0.02", "0.03", "0.04", "0.05", "0.06"]
    ast = ["0.02", "0.05", "0.31", "0.07", "0.08", "0.13"]
    body = "".join(f"2025-01-0{i + 1},{a},{m}\\n" for i, (a, m) in enumerate(zip(ast, mkt)))
    pairs = [(F(a), F(m)) for a, m in zip(ast, mkt) if abs(F(a)) <= F(1, 4) and abs(F(m)) <= F(1, 4)]
    assert len(pairs) == 5
    b3 = [float(v) for v in pure_betas(pairs, 3)]
    ex["t2"] = [{"setup": f"open('qd-pair.csv', 'w').write('date,asset,mkt\\n{body}')", "call": "windowed_betas(3)", "expect": repr(b3), "compare": "isclose", "tol": {"rel": 1e-9}}]
    # a hidden test with the error in the market column only (the real file has none there)
    ast2 = ["0.03", "0.05", "0.04", "0.07", "0.09", "0.12"]
    mkt2 = ["0.01", "0.02", "-0.28", "0.04", "0.05", "0.06"]
    body2 = "".join(f"2025-01-0{i + 1},{a},{m}\\n" for i, (a, m) in enumerate(zip(ast2, mkt2)))
    pairs2 = [(F(a), F(m)) for a, m in zip(ast2, mkt2) if abs(F(a)) <= F(1, 4) and abs(F(m)) <= F(1, 4)]
    assert len(pairs2) == 5
    b3x = [float(v) for v in pure_betas(pairs2, 3)]
    ex["t2x"] = {"setup": f"open('qd-pair.csv', 'w').write('date,asset,mkt\\n{body2}')", "call": "windowed_betas(3)", "expect": repr(b3x), "compare": "isclose", "tol": {"rel": 1e-9}}
    # task 3: the target is exactly 0.01 + 0.5 x1 - 0.25 x2 of the day before, so the fit recovers it and the score is 1
    x1 = [F(v, 10) for v in (1, 2, 0, 3, 1, 2, 0, 1)]
    x2 = [F(v, 10) for v in (0, 1, 2, 0, 1, 3, 1, 0)]
    ret = [F(0)] + [F(1, 100) + F(1, 2) * x1[t - 1] - F(1, 4) * x2[t - 1] for t in range(1, 8)]
    dec = lambda f: f"{float(f):.4f}"
    body = "".join(f"2025-01-{i + 1:02d},{dec(a)},{dec(b)},{dec(c)}\\n" for i, (a, b, c) in enumerate(zip(x1, x2, ret)))
    rows3 = list(csv.DictReader(("date,x1,x2,ret\n" + body.replace("\\n", "\n")).splitlines()))
    c, tr, te = pure_oos(rows3, 5)
    assert [float(v) for v in c] == [0.01, 0.5, -0.25] and tr == 1 and te == 1, (c, tr, te)
    ex["t3"] = [
        {"setup": f"open('qd-signal.csv', 'w').write('date,x1,x2,ret\\n{body}')", "call": "[round(c, 6) for c in oos_scores(5)['coef']]", "expect": "[0.01, 0.5, -0.25]", "compare": "equal"},
        {"setup": f"open('qd-signal.csv', 'w').write('date,x1,x2,ret\\n{body}')", "call": "round(oos_scores(5)['oos_r2'], 6)", "expect": "1.0", "compare": "equal"},
    ]
    NOTES.append(f"OK  examples: T1 {counts}, T2 betas {[round(v, 4) for v in b3]}, T3 coef {[float(v) for v in c]} R2 {te}")
    return ex


# ============================================================================== code text
IMP = "import numpy as np\nimport pandas as pd\n\n"
T1_STARTER = IMP + 'def tidy_closes():\n    """Tidy rows of qd-prices.csv."""\n    ...\n\n\ndef vol_by_ticker():\n    """Annualised volatility per ticker."""\n    ...\n'
T1_SOL = IMP + '''def tidy_closes():
    df = pd.read_csv("qd-prices.csv")
    df = df.drop_duplicates().dropna(subset=["close"])
    return df.sort_values(["ticker", "date"]).reset_index(drop=True)


def vol_by_ticker():
    df = tidy_closes()
    out = {}
    for ticker, g in df.groupby("ticker"):
        r = np.log(g["close"]).diff().dropna()
        out[ticker] = float(r.std(ddof=1) * np.sqrt(252))
    return out
'''
T1_ALT = IMP + '''def tidy_closes():
    df = pd.read_csv("qd-prices.csv").drop_duplicates()
    df = df[df["close"].notna()].sort_values(["ticker", "date"])
    return df.reset_index(drop=True)


def vol_by_ticker():
    s = tidy_closes().groupby("ticker")["close"].apply(lambda c: np.log(c).diff().std() * np.sqrt(252))
    return s.to_dict()
'''
T1_WRONG = {
    "no repeat removal": T1_SOL.replace("df.drop_duplicates().dropna", "df.dropna"),
    "return across tickers": T1_SOL.replace('''    out = {}
    for ticker, g in df.groupby("ticker"):
        r = np.log(g["close"]).diff().dropna()
        out[ticker] = float(r.std(ddof=1) * np.sqrt(252))
    return out''', '''    df["r"] = np.log(df["close"]).diff()
    df = df.dropna(subset=["r"])
    return {t: float(g["r"].std(ddof=1) * np.sqrt(252)) for t, g in df.groupby("ticker")}'''),
    "ddof 0": T1_SOL.replace("ddof=1", "ddof=0"),
    "no sort": T1_SOL.replace('    return df.sort_values(["ticker", "date"]).reset_index(drop=True)', "    return df.reset_index(drop=True)"),
    "blank closes kept as zero": T1_SOL.replace('.drop_duplicates().dropna(subset=["close"])', '.drop_duplicates().fillna(0)'),
}
T2_STARTER = IMP + 'def windowed_betas(window):\n    """Slope of asset on mkt per window."""\n    ...\n'
T2_SOL = IMP + '''def windowed_betas(window):
    df = pd.read_csv("qd-pair.csv")
    df = df[(df["asset"].abs() <= 0.25) & (df["mkt"].abs() <= 0.25)]
    x = df["mkt"].to_numpy()
    y = df["asset"].to_numpy()
    out = []
    for i in range(len(x) - window + 1):
        xs, ys = x[i:i + window], y[i:i + window]
        out.append(float(np.cov(xs, ys, ddof=1)[0, 1] / np.var(xs, ddof=1)))
    return out
'''
T2_ALTS = {
    "alt polyfit": IMP + '''def windowed_betas(window):
    df = pd.read_csv("qd-pair.csv")
    df = df[(df["asset"].abs() <= 0.25) & (df["mkt"].abs() <= 0.25)].reset_index(drop=True)
    return [float(np.polyfit(df["mkt"][i:i + window], df["asset"][i:i + window], 1)[0]) for i in range(len(df) - window + 1)]
''',
    "alt pandas rolling": IMP + '''def windowed_betas(window):
    df = pd.read_csv("qd-pair.csv")
    df = df[(df["asset"].abs() <= 0.25) & (df["mkt"].abs() <= 0.25)].reset_index(drop=True)
    b = df["asset"].rolling(window).cov(df["mkt"]) / df["mkt"].rolling(window).var()
    return b.dropna().tolist()
''',
}
T2_WRONG = {"keeps the errors": T2_SOL.replace('    df = df[(df["asset"].abs() <= 0.25) & (df["mkt"].abs() <= 0.25)]\n', ""),
            "drops the error in asset only": T2_SOL.replace('(df["asset"].abs() <= 0.25) & (df["mkt"].abs() <= 0.25)', '(df["asset"].abs() <= 0.25)'),
            "windows of window minus one": T2_SOL.replace("x[i:i + window], y[i:i + window]", "x[i:i + window - 1], y[i:i + window - 1]")}
T3_STARTER = IMP + 'def oos_scores(split):\n    """Fit, then score the later rows."""\n    ...\n'
T3_SOL = IMP + '''def oos_scores(split):
    df = pd.read_csv("qd-signal.csv")
    X = np.column_stack([np.ones(len(df) - 1), df["x1"].to_numpy()[:-1], df["x2"].to_numpy()[:-1]])
    y = df["ret"].to_numpy()[1:]
    Xtr, ytr, Xte, yte = X[:split], y[:split], X[split:], y[split:]
    coef, *_ = np.linalg.lstsq(Xtr, ytr, rcond=None)
    train_r2 = 1 - np.sum((ytr - Xtr @ coef) ** 2) / np.sum((ytr - ytr.mean()) ** 2)
    oos_r2 = 1 - np.sum((yte - Xte @ coef) ** 2) / np.sum((yte - ytr.mean()) ** 2)
    return {"coef": [float(c) for c in coef], "train_r2": float(train_r2), "oos_r2": float(oos_r2)}
'''
T3_ALTS = {"alt normal equations": T3_SOL.replace("coef, *_ = np.linalg.lstsq(Xtr, ytr, rcond=None)", "coef = np.linalg.solve(Xtr.T @ Xtr, Xtr.T @ ytr)")}
T3_WRONG = {
    "unlagged features": T3_SOL.replace('X = np.column_stack([np.ones(len(df) - 1), df["x1"].to_numpy()[:-1], df["x2"].to_numpy()[:-1]])', 'X = np.column_stack([np.ones(len(df) - 1), df["x1"].to_numpy()[1:], df["x2"].to_numpy()[1:]])'),
    "test mean as baseline": T3_SOL.replace("(yte - ytr.mean())", "(yte - yte.mean())"),
    "fit on every row": T3_SOL.replace("np.linalg.lstsq(Xtr, ytr, rcond=None)", "np.linalg.lstsq(X, y, rcond=None)"),
    "split before lagging": T3_SOL.replace("Xtr, ytr, Xte, yte = X[:split], y[:split], X[split:], y[split:]", "Xtr, ytr, Xte, yte = X[:split - 1], y[:split - 1], X[split - 1:], y[split - 1:]"),
}


# ============================================================================== widget helpers
def num(answer, tol, wrong, accept, unit=None, placeholder="a number"):
    w = {"kind": "numeric", "answer": answer, "tol": {"abs": tol}}
    if unit:
        w["unit"] = unit
    w.update({"placeholder": placeholder, "label": "Your answer", "wrong": [{"id": i, "value": v, "tol": {"abs": t}} for i, v, t in wrong], "accept": accept})
    return w


def options(kind, rows):
    opts = []
    for i, (text, why) in enumerate(rows):
        o = {"id": "abcdef"[i], "text": text}
        if why is None:
            o["correct"] = True
        else:
            o["why"] = why
        opts.append(o)
    return {"kind": kind, "layout": "stack", "shuffle": True, "label": "Answer options", "options": opts}


def item(id_, diff, skills, tag, pace, title, **kw):
    d = {"id": id_, "difficulty": diff, "skills": skills, "tags": [tag], "pace": pace, "title": title}
    d.update(kw)
    return d


def fb(correct, generic, **by):
    d = {"correct": correct, "generic": generic}
    if by:
        d["byKey"] = by
    return d


def paper1():
    S, L, M = ["rq-stats"], ["rq-linalg"], ["rq-ml"]
    items = [
        item("q1-standard-error", 2, S, "standard-error", 150, "An interval for a mean",
             question="36 daily returns have a sample standard deviation of 12 basis points. Use 1.96 as the multiplier. What is the half-width of a 95% interval for the mean return, in basis points?",
             widget=num(3.92, 0.005, [("se-only", 2.0, 0.005), ("no-root-n", 23.52, 0.005)], "3.92 (within 0.005)"),
             feedback=fb(r"The multiplier applies to the standard error of the mean, $s/\sqrt n$.", "Find the standard error of the mean first. Then scale it by 1.96.",
                         **{"se-only": "You gave the standard error. The interval half-width multiplies it by 1.96.",
                            "no-root-n": r"You did not divide by $\sqrt n$. The spread of the mean is $12/6$, not 12."}),
             explain={"text": r"The standard error is $12/\sqrt{36} = 2$. The half-width is $1.96 \times 2 = 3.92$ basis points. Check: $1.96\sqrt{144/36}$ gives the same."}),
        item("q2-p-value-meaning", 2, S, "p-value-meaning", 120, "What a p-value says",
             question="A test reports $p = 0.018$ for the average daily profit of a trading rule. What does that mean?",
             widget=options("choice", [
                 ("With a true average profit of zero, results this extreme occur about 1.8% of the time.", None),
                 ("There is a 1.8% chance that the rule makes no money at all, given the data.", "You read the p-value as the chance of the hypothesis. It assumes the hypothesis and asks about the data."),
                 ("There is a 98.2% chance that the rule makes real money, given the data.", "You turned the p-value into the chance an edge exists. It is not a probability of the hypothesis."),
                 ("The rule's average daily profit is 1.8%, which is large enough to trade on.", "You read the p-value as an effect size. It says how surprising the data are, not how big the effect is."),
             ]),
             feedback=fb("A p-value assumes the null and asks how surprising the data are.", "Say what the p-value assumes, then what it measures."),
             explain={"text": "A p-value is the chance of a result at least this extreme if the true average were zero. It is not the chance the hypothesis is true, and it gives no effect size. Here, 1.8% is how rare the data would be under no edge."}),
        item("q3-t-statistic", 3, S, "t-statistic", 180, "A t-statistic",
             question="The mean excess return is 3.0 basis points a day. The sample standard deviation is 10, over 25 days, and the null mean is zero. What is the t-statistic?",
             widget=num(1.5, 0.005, [("wrong-se", 7.5, 0.005), ("s-only", 0.3, 0.005)], "1.5 (within 0.005)"),
             feedback=fb(r"The standard error is $10/\sqrt{25} = 2$, so $t$ is the mean over 2.", "Divide the mean by its standard error, not by the standard deviation.",
                         **{"wrong-se": r"You divided by $s/n$, not $s/\sqrt n$. The standard error is 2, not 0.4.",
                            "s-only": r"You divided by $s$ alone. The mean's own spread is $s/\sqrt n$."}),
             explain={"text": r"The standard error is $10/\sqrt{25} = 2$, so $t = 3.0/2 = 1.5$. Check: the mean is one and a half standard errors from zero. That is below the 5% cut-off of about 2.06 for 24 degrees of freedom."}),
        item("q4-ols-facts", 3, S, "ols-facts", 240, "What always holds in a fit",
             question="Select all that apply: which statements about least squares with an intercept always hold in the sample?",
             widget=options("multi", [
                 ("The residuals sum to zero.", None),
                 ("The fitted line passes through the point of the means.", None),
                 (r"$R^2$ cannot fall when a predictor is added.", None),
                 ("The residuals are normally distributed.", "You treated an assumption about errors as a fact of the fit. Residuals can take any shape."),
                 ("The slope's t-test is valid whatever the errors are.", "You dropped the assumptions. The usual t-test needs errors that are roughly independent and equal in spread."),
                 (r"Adjusted $R^2$ cannot fall when a predictor is added.", r"You gave adjusted $R^2$ the property of $R^2$. Its penalty for a predictor can outweigh a small gain."),
             ]),
             feedback=fb("Those three follow from the normal equations. The others need assumptions or are false.", "Ask which statements are algebra of the fit and which need assumptions about the errors."),
             explain={"text": r"The normal equations force the residuals to sum to zero and the line through the means. Adding a column can only lower the sum of squared residuals, so $R^2$ cannot fall. Adjusted $R^2$ charges for the column, so it can fall."}),
        item("q5-adjusted-r2", 3, S, "adjusted-r2", 210, "Adjusted R squared",
             question=r"A regression has 50 observations and 4 predictors, plus an intercept. $R^2$ is 0.40. What is the adjusted $R^2$? Give four decimals.",
             widget=num(0.3467, 0.0005, [("raw-r2", 0.4, 0.0005), ("n-minus-k", 0.3609, 0.0005)], "0.3467 (within 0.0005)", placeholder="four decimals"),
             feedback=fb(r"Adjusted $R^2$ is $1 - (1 - R^2)(n-1)/(n-k-1)$, which is $1 - 0.6 \times 49/45$.", r"Scale the unexplained share $1 - R^2$ by $(n-1)/(n-k-1)$."),
             explain={"text": r"Adjusted $R^2 = 1 - 0.6 \times 49/45 = 26/75 = 0.3467$. Check: $0.4 - 0.6 \times 4/45$ gives the same."}),
    ]
    items[4]["feedback"]["byKey"] = {"raw-r2": r"You gave the reported $R^2$. Adjusting for 4 predictors lowers it.",
                                     "n-minus-k": r"You used $n - k$. With an intercept the divisor is $n - k - 1 = 45$."}
    items.append(item("q6-bivariate-normal", 3, S, "bivariate-normal", 300, "Y given X",
                      prose=r"$X$ has mean 1 and standard deviation 3. $Y$ has mean 4 and standard deviation 2. They are jointly normal with correlation 0.6.",
                      parts=[
                          {"question": r"What is $E[Y \mid X = 5]$?",
                           "widget": num(5.6, 0.005, [("unconditional", 4.0, 0.005), ("rho-slope", 6.4, 0.005)], "5.6 (within 0.005)"),
                           "feedback": fb(r"The slope of $Y$ on $X$ is $\rho\sigma_y/\sigma_x = 0.4$, and $X$ is 4 above its mean.", "Move the mean of $Y$ along the regression line of $Y$ on $X$.",
                                          **{"unconditional": "You gave the mean of $Y$. Knowing $X = 5$ moves it along the regression line.",
                                             "rho-slope": r"You used 0.6 as the slope. The slope is $\rho\sigma_y/\sigma_x = 0.4$."}),
                           "explain": {"text": r"The conditional mean is $4 + 0.6 \times (2/3) \times (5 - 1) = 5.6$. Check: $\mu_y + \Sigma_{yx}\Sigma_{xx}^{-1}(x - \mu_x)$ with $\Sigma_{yx} = 3.6$ and $\Sigma_{xx} = 9$ gives the same."}},
                          {"question": r"What is the standard deviation of $Y$ given $X = 5$?",
                           "widget": num(1.6, 0.005, [("unconditional", 2.0, 0.005), ("rho-sigma", 1.2, 0.005)], "1.6 (within 0.005)"),
                           "feedback": fb(r"Conditioning leaves $\sigma_y\sqrt{1-\rho^2}$, whatever $X$ is.", r"The spread left over after $X$ is known depends on $\rho$ but not on the value of $X$.",
                                          **{"unconditional": r"You gave the spread of $Y$ with $X$ unknown. Knowing $X$ shrinks it by $\sqrt{1-\rho^2}$.",
                                             "rho-sigma": r"You gave $\rho\sigma_y$, the spread that $X$ explains. The leftover is $\sigma_y\sqrt{1-\rho^2}$."}),
                           "explain": {"text": r"The conditional variance is $4(1 - 0.36) = 2.56$, so the standard deviation is 1.6. Check: $\Sigma_{yy} - \Sigma_{yx}^2/\Sigma_{xx} = 4 - 12.96/9 = 2.56$."}},
                      ]))
    items.append(item("q7-portfolio-sd", 3, S, "portfolio-sd", 240, "Two assets together",
                      question="Two assets have volatility 20% and 30% a year and correlation $-0.3$. You hold 60% in the first and 40% in the second. What is the portfolio volatility, in %? Give one decimal place.",
                      widget=num(0.142, 0.001, [("weighted-vols", 0.24, 0.001), ("no-covariance", 0.17, 0.001), ("typed-fraction", 0.00142, 0.0001)], "14.2% (within 0.1 points)", unit="%"),
                      feedback=fb(r"The variance has two squared terms and a covariance term, $w^T \Sigma w$.", "Volatilities do not average. Work with variances and the covariance.",
                                  **{"weighted-vols": "You weighted the volatilities. That is correct only when the correlation is 1.",
                                     "no-covariance": "You left out the covariance term. With correlation $-0.3$ it lowers the variance.",
                                     "typed-fraction": "You typed the fraction. The box takes a percentage."}),
                      explain={"text": r"The variance is $0.0144 + 0.0144 - 0.00864 = 0.02016$. Its square root is 0.1420, so the volatility is 14.2%. Check: $w^T \Sigma w$ with the covariance matrix gives the same."}))
    items.append(item("q8-min-variance-weight", 4, L, "min-variance-weight", 270, "The quietest mix",
                      question="Two assets have volatility 25% and 20% and correlation 0.3. The weights sum to 1. What weight in the 25% asset gives the minimum-variance portfolio? Give four decimals.",
                      widget=num(0.3448, 0.0005, [("inverse-variance", 0.3902, 0.0005), ("equal", 0.5, 0.0005)], "0.3448 (within 0.0005)", placeholder="four decimals"),
                      feedback=fb(r"The weight is $(\sigma_2^2 - c)/(\sigma_1^2 + \sigma_2^2 - 2c)$ with covariance $c = 0.015$.", "Set the derivative of the portfolio variance to zero. The covariance must appear.",
                                  **{"inverse-variance": "You weighted by inverse variance. That ignores the correlation, which here is 0.3.",
                                     "equal": "You split the money equally. The 20% asset is steadier, so it earns more than half."}),
                      explain={"text": r"With $c = 0.015$, the weight is $(0.04 - 0.015)/(0.0625 + 0.04 - 0.03) = 0.025/0.0725 = 10/29$. That is 0.3448. Check: on a grid in steps of $1/290$, the exact variance is lowest at $100/290$."}))
    items.append(item("q9-cv-leakage", 4, M, "cv-leakage", 270, "Cross-validating returns",
                      question="You cross-validate a return-prediction model. Select all that apply: which choices avoid leakage?",
                      widget=options("multi", [
                          ("Train on earlier rows and test on later rows.", None),
                          ("Fit the scaler on the training fold only.", None),
                          ("Leave a gap between training and test when labels overlap.", None),
                          ("Shuffle the rows before splitting them into folds.", "You let later rows into training. A shuffled split tests on days the model has seen around."),
                          ("Keep the model with the best test-fold score after many tries.", "You tuned on the test fold, so it became training data for the choice. Its score is now too hopeful."),
                          ("Standardise every feature with the whole sample.", "You let the test rows set the mean and spread. That leaks the future into the training rows."),
                      ]),
                      feedback=fb("Each correct choice keeps future rows away from the fit.", "For each choice, ask whether the model sees anything from after the forecast date."),
                      explain={"text": "A model may use only what was known when the forecast was made. A time-ordered split, a scaler fitted on training rows and a gap for overlapping labels all keep to that. Shuffling, tuning on the test fold and whole-sample scaling let the future in."}))
    items.append(item("q10-compound-poisson", 5, S, "compound-poisson", 300, "Total size of an hour's trades",
                      question="Trades arrive as a Poisson process, 4 an hour. Each size has mean 10 and standard deviation 5, independent of the others and of the count. What is the variance of the total size in an hour?",
                      widget=num(500, 0, [("size-only", 100, 0), ("count-only", 400, 0), ("mean", 40, 0)], "500"),
                      feedback=fb(r"Use the law of total variance: $\lambda(\sigma^2 + \mu^2)$.", "The total varies for two reasons: each size varies, and so does the count.",
                                  **{"size-only": r"You counted only the size variance, $4 \times 25$. The varying count adds $4 \times 100$ more.",
                                     "count-only": r"You counted only the spread from the count, $4 \times 100$. Each trade also has its own size variance, $4 \times 25$.",
                                     "mean": "You gave the mean of the total. The question asks for its variance."}),
                      explain={"text": r"By the law of total variance, the variance of the total is $\lambda(\sigma^2 + \mu^2) = 4 \times (25 + 100) = 500$. The count adds spread through $\mu^2$ as well as the sizes through $\sigma^2$. Check: summing over counts from 0 to 79 gives the same."}))
    return items


def code_item(id_, diff, skills, tag, pace, title, question, data, starter, examples, tests, how, solution, feedback, explain):
    return {"id": id_, "difficulty": diff, "skills": skills, "tags": [tag], "pace": pace, "title": title, "question": question,
            "widget": {"kind": "code", "language": "python", "data": {data: f"content/data/qd/{data}"}, "starter": starter,
                       "examples": examples, "tests": tests, "how": how, "solution": solution},
            "feedback": feedback, "explain": explain}


def mk_tests(spec, cap=None):
    out = []
    for call, exp, cmp_, tol in spec:
        t = {"call": call, "expect": exp, "compare": cmp_}
        if tol:
            t["tol"] = tol
        out.append(t)
    return out


def paper2(ex, tj):
    t1, t2, t3 = (mk_tests(tj[k]["tests"]) for k in ("qd-returns", "qd-rolling-beta", "qd-out-of-sample"))
    t2.append(ex["t2x"])
    t1.append({"call": "[tidy_closes()['ticker'].iloc[258], float(tidy_closes()['close'].iloc[258])]", "expect": "['LAMBDA', 122.15]", "compare": "equal"})
    return [
        code_item("d1-return-table", 3, ["rq-data"], "return-table", 1200, "A return table from messy closes",
                  "`qd-prices.csv` has one close a day for three tickers. The rows are not in date order. Some closes are blank, and some rows repeat. Write `tidy_closes()` and `vol_by_ticker()`. `tidy_closes()` returns a frame with the columns `date`, `ticker` and `close`. It drops repeated rows and blank closes, and sorts by ticker, then date. `vol_by_ticker()` returns a dict from ticker to annualised volatility. Use the sample standard deviation (`ddof=1`) of the daily log returns within each ticker, times $\\sqrt{252}$. Where a blank was dropped, the return spans two rows.",
                  "qd-prices.csv", T1_STARTER, ex["t1"], t1,
                  "There are 11 hidden tests. Counts, columns and order must match exactly. Volatilities are accepted within a relative 1e-9. The last test fails a sort by date alone.", T1_SOL,
                  fb("All eleven tests pass: the rows are tidy and each volatility uses returns within one ticker.", "A hidden test failed. Open the first failed row. Check the repeats, the blanks, the order and that returns stay within a ticker."),
                  {"text": "Drop the repeats and blank closes, sort by ticker and date, then take the log returns inside each ticker. A `diff` on the stacked frame gives the first row of each ticker a return from the ticker before. Check: a pure-Python pass over the file gives the same three volatilities."}),
        code_item("d2-rolling-beta", 4, ["rq-data", "rq-stats"], "hedge-ratio", 1500, "A rolling hedge ratio",
                  "`qd-pair.csv` has daily returns for an asset and the market. Three asset returns were typed as whole percents. A return with size above 0.25 in either column is a data error: drop that row. Then write `windowed_betas(window)`. It returns one least-squares slope of `asset` on `mkt` per window of `window` neighbouring remaining rows. Use date order and full windows only.",
                  "qd-pair.csv", T2_STARTER, ex["t2"], t2,
                  "There are 9 hidden tests. Each slope is accepted within a relative 1e-9. The last test has a data error in the market column, so it fails a check of the asset column alone.", T2_SOL,
                  fb("All nine tests pass: the errors are gone and every window is a full one.", "A hidden test failed. Check both columns for data errors, then count the full windows."),
                  {"text": "A return of 0.31 is a whole percent typed in, so drop the row before windowing. The 517 rows left give 458 windows of 60. Keeping the errors gives 461 windows and a different sum."}),
        code_item("d3-out-of-sample", 5, ["rq-data", "rq-ml", "rq-case"], "out-of-sample", 1800, "An honest out-of-sample score",
                  "`qd-signal.csv` has two signals and the return of each day. Predict a day's return from the signals of the day before. Write `oos_scores(split)`. Row $t$ has the features of row $t - 1$ and the target `ret` of row $t$, for $t = 1$ to 799. Fit least squares with an intercept on the first `split` of these rows. Return a dict with `coef` (intercept, then the two slopes), `train_r2` and `oos_r2`. The out-of-sample score uses the remaining rows. Its baseline is the training mean of the target.",
                  "qd-signal.csv", T3_STARTER, ex["t3"], t3,
                  "There are 7 hidden tests. Each number is accepted within a relative 1e-8. The out-of-sample tests fail a score that uses the test mean as its baseline.", T3_SOL,
                  fb("All seven tests pass: the fit saw only the first rows and the score used the training mean.", "A hidden test failed. Check the lag, which rows the fit sees, and the baseline of the out-of-sample score."),
                  {"text": "Lag the features so each row predicts forward. Fit on the first rows only, and score the rest against the training mean. A fit on every row, or a test-set baseline, borrows from the future."}),
    ]


def main():
    extra = paper1_numbers()
    tj = json.load(open(os.path.join(HERE, "qd_tasks_tests.json")))
    # ---- second method for the expected values of paper 2, from the decimal text
    prices = read("qd-prices.csv")
    vols, counts, nclean = pure_task1(prices)
    assert len(prices) == 783 and nclean == 773 and counts == {"KAPPA": 258, "LAMBDA": 257, "MU": 258}
    for t, v in vols.items():
        assert isc(v, tj["qd-returns"]["vols"][t], 1e-9), t
    pair = read("qd-pair.csv")
    pairs = [(F(r["asset"]), F(r["mkt"])) for r in pair if abs(F(r["asset"])) <= F(1, 4) and abs(F(r["mkt"])) <= F(1, 4)]
    assert len(pair) == 520 and len(pairs) == 517
    b60, b120 = pure_betas(pairs, 60), pure_betas(pairs, 120)
    assert len(b60) == 458 and len(pure_betas(pairs, 600)) == 0
    tt = {c: (e, cm) for c, e, cm, _ in tj["qd-rolling-beta"]["tests"]}
    two("T2 first beta (60)", F(float(b60[0])).limit_denominator(10 ** 12), F(float(tt["windowed_betas(60)[0]"][0])).limit_denominator(10 ** 12), 1e-9)
    assert isc(float(b60[0]), float(tt["windowed_betas(60)[0]"][0]), 1e-9) and isc(float(b60[-1]), float(tt["windowed_betas(60)[-1]"][0]), 1e-9)
    assert isc(float(sum(b60)), float(tt["sum(windowed_betas(60))"][0]), 1e-9)
    assert isc(float(min(b120)), float(tt["min(windowed_betas(120))"][0]), 1e-9) and isc(float(max(b120)), float(tt["max(windowed_betas(120))"][0]), 1e-9)
    assert isc(float(pure_betas(pairs, 517)[0]), float(tt["windowed_betas(517)[0]"][0]), 1e-9)
    sig = read("qd-signal.csv")
    assert len(sig) == 800
    t3t = {c: e for c, e, _, _ in tj["qd-out-of-sample"]["tests"]}
    for s, key in ((500, "oos_scores(500)"), (300, "oos_scores(300)")):
        c, tr, te = pure_oos(sig, s)
        assert all(isc(float(a), b, 1e-8) for a, b in zip(c, json.loads(t3t[key + "['coef']"]))), s
        assert isc(float(te), float(t3t[key + "['oos_r2']"]), 1e-7), s
    c5, tr5, te5 = pure_oos(sig, 500)
    assert isc(float(tr5), float(t3t["oos_scores(500)['train_r2']"]), 1e-8)
    assert isc(float(pure_oos(sig, 600)[2]), float(t3t["oos_scores(600)['oos_r2']"]), 1e-7)
    NOTES.append(f"OK  paper 2: rows {nclean}, windows {len(b60)}, coef500 {[round(float(v), 6) for v in c5]}, train R2 {float(tr5):.4f}, oos R2 {float(te5):.4f}")
    ex = small_examples()

    # ---- the exam
    desc = ("This is the reported format of an online quant assessment, as candidates described it by Nov 2026. It has two papers and takes 120 minutes. "
            "The first has 10 statistics and applied maths questions, and some ask you to select all that apply. The second has three Python data tasks that read CSV files. "
            "Hidden tests check each task, so run your code before you move on. Use only the standard documentation of the libraries. Use no search engine and no notes.")
    models = "Reported, as of Nov 2026: online tests for quant research and finance interns at Morgan Stanley and Two Sigma. Statistics and applied maths questions, then Python data tasks."
    assert len(models) <= 200, len(models)
    exam = {
        "id": "mock-oa-quant-data", "name": "Quantitative data assessment", "style": "research", "models": models, "description": desc,
        "skills": {"rq-stats": "Statistics questions", "rq-linalg": "Linear algebra questions", "rq-ml": "Machine learning questions", "rq-case": "Applied cases", "rq-data": "Data tasks"},
        "parts": [
            {"kind": "paper", "id": "stats", "name": "Statistics and applied maths", "minutes": 40, "scoring": {"right": 1, "wrong": 0, "blank": 0}, "pass": 0.6, "items": paper1()},
            {"kind": "paper", "id": "data", "name": "Python data tasks", "minutes": 80, "scoring": {"right": 1, "wrong": 0, "blank": 0}, "pass": 0.6, "items": paper2(ex, tj)},
            {"kind": "check", "id": "no-lookup", "name": "I used no search engine and no notes", "detail": "Tick this only if you sat both papers without either."},
        ],
    }
    p1, p2 = exam["parts"][0]["items"], exam["parts"][1]["items"]
    assert sum(i["pace"] for i in p1) == 2280 and sum(i["pace"] for i in p2) == 4500
    assert [i["difficulty"] for i in p1] == [2, 2, 3, 3, 3, 3, 3, 4, 4, 5]
    # ---- key not visibly longer than the distractors
    for it in p1:
        w = it.get("widget")
        if w and w["kind"] in ("choice", "multi"):
            keys = [len(o["text"]) for o in w["options"] if o.get("correct")]
            bad = [len(o["text"]) for o in w["options"] if not o.get("correct")]
            assert max(keys) <= 1.15 * (sum(bad) / len(bad)) + 10 and max(keys) <= max(bad) * 1.15, (it["id"], keys, bad)
    # ---- voice
    problems = voice(exam)
    assert not problems, problems
    json.dump(exam, open(OUT, "w"), indent=2, ensure_ascii=False)
    open(OUT, "a").write("\n")
    # ---- Pyodide cases
    if SCRATCH:
        os.makedirs(SCRATCH, exist_ok=True)
        cases = []
        for name, sol, alts, wrongs, starter, tests in (
                ("task 1", T1_SOL, {"alt groupby apply": T1_ALT}, T1_WRONG, T1_STARTER, p2[0]["widget"]["tests"]),
                ("task 2", T2_SOL, T2_ALTS, T2_WRONG, T2_STARTER, p2[1]["widget"]["tests"]),
                ("task 3", T3_SOL, T3_ALTS, T3_WRONG, T3_STARTER, p2[2]["widget"]["tests"])):
            cases.append({"name": f"{name} starter", "code": starter, "tests": tests, "expectPass": False})
            cases.append({"name": f"{name} reference", "code": sol, "tests": tests, "expectPass": True})
            for k, v in alts.items():
                cases.append({"name": f"{name} {k}", "code": v, "tests": tests, "expectPass": True})
            for k, v in wrongs.items():
                assert v != sol, (name, k)
                cases.append({"name": f"{name} wrong: {k}", "code": v, "tests": tests, "expectPass": False})
        # the worked examples must pass for the reference solutions
        for name, sol, exs in (("task 1", T1_SOL, ex["t1"]), ("task 2", T2_SOL, ex["t2"]), ("task 3", T3_SOL, ex["t3"])):
            cases.append({"name": f"{name} examples with the reference", "code": sol, "tests": exs, "expectPass": True})
        for name, st, exs in (("task 1", T1_STARTER, ex["t1"]), ("task 2", T2_STARTER, ex["t2"]), ("task 3", T3_STARTER, ex["t3"])):
            cases.append({"name": f"{name} examples fail on the starter", "code": st, "tests": exs, "expectPass": False})
        json.dump(cases, open(os.path.join(SCRATCH, "pyo_cases.json"), "w"))
        print(f"wrote {len(cases)} Pyodide cases to {SCRATCH}")
    print("\n".join(NOTES))
    print(f"wrote {OUT}: {len(p1)} + {len(p2)} items; Q4 stats {extra}")
    print("ALL AGREE")


# ============================================================================== voice
def words(s):
    s = re.sub(r"`[^`]*`", "X", s)
    s = re.sub(r"\$[^$]*\$", "X", s)
    return len(s.split())


def sentences(t):
    t = re.sub(r"\s+", " ", t)
    return [x for x in re.split(r"(?<=[.?:;])\s+", t) if x.strip()]


def voice(exam):
    bad = []
    US = ["color", "center", "favorite", "analyze", "optimize", "behavior", "modeling", "labeled", "math class"]

    def check(label, text, limit_sentences=None):
        if "!" in text:
            bad.append((label, "!"))
        if "—" in text or "–" in text:
            bad.append((label, "dash"))
        for w_ in US:
            if re.search(r"\b" + w_.strip(), text.lower()):
                bad.append((label, "US spelling " + w_))
        ss = sentences(text)
        for s in ss:
            if words(s) >= 20:
                bad.append((label, f"{words(s)} words: {s[:60]}"))
        n = len([x for x in re.split(r"(?<=[.?])\s+", re.sub(r"\s+", " ", text)) if x.strip()])
        if limit_sentences and n > limit_sentences:
            bad.append((label, f"{n} sentences"))

    def walk(o, label):
        if isinstance(o, dict):
            for k, v in o.items():
                if k in ("starter", "solution", "setup", "call", "expect", "data", "how", "tags", "id", "kind", "label", "placeholder", "accept", "layout", "unit"):
                    continue
                if k == "explain":
                    check(label + ".explain", v["text"], 3)
                elif isinstance(v, str) and k in ("question", "prose", "title", "text", "why", "correct", "generic", "name", "detail", "description"):
                    check(f"{label}.{k}", v)
                elif k == "byKey":
                    for kk, vv in v.items():
                        check(f"{label}.byKey.{kk}", vv)
                else:
                    walk(v, f"{label}.{k}")
        elif isinstance(o, list):
            for i, v in enumerate(o):
                walk(v, f"{label}[{i}]")

    walk(exam, exam["id"])
    check("models", exam["models"])
    return bad


if __name__ == "__main__":
    main()
