"""mock-oa-quant-data: the three Python data tasks, checked.

Run: python3 -I qd_tasks.py     (needs numpy and pandas for the references; the second method is pure Python with
Fractions, read straight from the decimal text in the CSV, so it is exact).  Run gen_qd_data.py first.

Local versions were numpy 2.5.3 and pandas 3.0.5; Pyodide 0.27.7 has numpy 2.0.2 and pandas 2.2.3.  The reference
code below uses only calls that mean the same in both (read_csv, drop_duplicates, dropna, sort_values, groupby,
log, diff, std, to_numpy, lstsq).  The mock author reruns every test in the real playthrough.
"""
import csv, inspect, json, math, os, statistics
from fractions import Fraction

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data")
os.chdir(DATA)  # the references open the files by bare name, as the hidden tests do


# =============================================================== task 1: clean prices, annual volatilities
def tidy_closes():
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


def t1_second():  # pure Python: csv, a set of rows, math.log, statistics.stdev
    seen, rows = set(), []
    with open("qd-prices.csv") as f:
        for row in csv.DictReader(f):
            key = (row["date"], row["ticker"], row["close"])
            if key in seen:
                continue
            seen.add(key)
            if row["close"] != "":
                rows.append((row["ticker"], row["date"], float(row["close"])))
    rows.sort()
    by = {}
    for t, d, c in rows:
        by.setdefault(t, []).append(c)
    vols = {t: statistics.stdev([math.log(b / a) for a, b in zip(cs, cs[1:])]) * math.sqrt(252) for t, cs in by.items()}
    return vols, {t: len(cs) for t, cs in by.items()}, len(rows)


# wrong versions the tests must catch
def t1_wrong_no_dedupe():
    df = pd.read_csv("qd-prices.csv").dropna(subset=["close"]).sort_values(["ticker", "date"])
    return {t: float(np.log(g["close"]).diff().dropna().std(ddof=1) * np.sqrt(252)) for t, g in df.groupby("ticker")}


def t1_wrong_across_tickers():  # diff on the stacked frame: the first row of each ticker gets a return from the ticker before
    df = tidy_closes()
    r = np.log(df["close"]).diff().dropna()
    df = df.iloc[1:].assign(r=r.values)
    return {t: float(g["r"].std(ddof=1) * np.sqrt(252)) for t, g in df.groupby("ticker")}


def t1_wrong_ddof0():
    df = tidy_closes()
    return {t: float(np.log(g["close"]).diff().dropna().std(ddof=0) * np.sqrt(252)) for t, g in df.groupby("ticker")}


def t1_wrong_unsorted():
    df = pd.read_csv("qd-prices.csv").drop_duplicates().dropna(subset=["close"])
    return {t: float(np.log(g["close"]).diff().dropna().std(ddof=1) * np.sqrt(252)) for t, g in df.groupby("ticker")}


# =============================================================== task 2: rolling beta with data errors dropped
def windowed_betas(window):
    df = pd.read_csv("qd-pair.csv")
    df = df[(df["asset"].abs() <= 0.25) & (df["mkt"].abs() <= 0.25)]
    x = df["mkt"].to_numpy()
    y = df["asset"].to_numpy()
    out = []
    for i in range(len(x) - window + 1):
        xs, ys = x[i:i + window], y[i:i + window]
        out.append(float(np.cov(xs, ys, ddof=1)[0, 1] / np.var(xs, ddof=1)))
    return out


def t2_second(window):  # exact: Fractions from the decimal text, centred sums per window
    xs, ys = [], []
    with open("qd-pair.csv") as f:
        for row in csv.DictReader(f):
            a, m = Fraction(row["asset"]), Fraction(row["mkt"])
            if abs(a) <= Fraction(1, 4) and abs(m) <= Fraction(1, 4):
                xs.append(m)
                ys.append(a)
    out = []
    for i in range(len(xs) - window + 1):
        wx, wy = xs[i:i + window], ys[i:i + window]
        mx, my = sum(wx) / window, sum(wy) / window
        sxy = sum((a - mx) * (b - my) for a, b in zip(wx, wy))
        sxx = sum((a - mx) ** 2 for a in wx)
        out.append(sxy / sxx)
    return out


def t2_wrong_keep_errors(window):
    df = pd.read_csv("qd-pair.csv")
    x, y = df["mkt"].to_numpy(), df["asset"].to_numpy()
    return [float(np.cov(x[i:i + window], y[i:i + window], ddof=1)[0, 1] / np.var(x[i:i + window], ddof=1)) for i in range(len(x) - window + 1)]


# =============================================================== task 3: out-of-sample report
def oos_scores(split):
    df = pd.read_csv("qd-signal.csv")
    X = np.column_stack([np.ones(len(df) - 1), df["x1"].to_numpy()[:-1], df["x2"].to_numpy()[:-1]])
    y = df["ret"].to_numpy()[1:]
    Xtr, ytr, Xte, yte = X[:split], y[:split], X[split:], y[split:]
    coef, *_ = np.linalg.lstsq(Xtr, ytr, rcond=None)
    train_r2 = 1 - np.sum((ytr - Xtr @ coef) ** 2) / np.sum((ytr - ytr.mean()) ** 2)
    oos_r2 = 1 - np.sum((yte - Xte @ coef) ** 2) / np.sum((yte - ytr.mean()) ** 2)
    return {"coef": [float(c) for c in coef], "train_r2": float(train_r2), "oos_r2": float(oos_r2)}


def solve(A, b):  # exact Gauss-Jordan on Fractions
    n = len(A)
    M = [row[:] + [bi] for row, bi in zip(A, b)]
    for c in range(n):
        p = next(r for r in range(c, n) if M[r][c] != 0)
        M[c], M[p] = M[p], M[c]
        M[c] = [v / M[c][c] for v in M[c]]
        for r in range(n):
            if r != c and M[r][c] != 0:
                f = M[r][c]
                M[r] = [a - f * b for a, b in zip(M[r], M[c])]
    return [M[i][n] for i in range(n)]


def t3_second(split):
    rows = list(csv.DictReader(open("qd-signal.csv")))
    x1 = [Fraction(r["x1"]) for r in rows]
    x2 = [Fraction(r["x2"]) for r in rows]
    ret = [Fraction(r["ret"]) for r in rows]
    X = [[Fraction(1), x1[t - 1], x2[t - 1]] for t in range(1, len(rows))]
    y = ret[1:]
    Xtr, ytr, Xte, yte = X[:split], y[:split], X[split:], y[split:]
    A = [[sum(r[i] * r[j] for r in Xtr) for j in range(3)] for i in range(3)]
    b = [sum(r[i] * v for r, v in zip(Xtr, ytr)) for i in range(3)]
    c = solve(A, b)
    pred = lambda r: sum(ci * ri for ci, ri in zip(c, r))
    mean_tr = sum(ytr) / len(ytr)
    tr = 1 - sum((v - pred(r)) ** 2 for r, v in zip(Xtr, ytr)) / sum((v - mean_tr) ** 2 for v in ytr)
    te = 1 - sum((v - pred(r)) ** 2 for r, v in zip(Xte, yte)) / sum((v - mean_tr) ** 2 for v in yte)
    return [float(v) for v in c], float(tr), float(te)


def t3_wrong_unlagged(split):
    df = pd.read_csv("qd-signal.csv")
    X = np.column_stack([np.ones(len(df)), df["x1"], df["x2"]])[1:]
    y = df["ret"].to_numpy()[1:]
    coef, *_ = np.linalg.lstsq(X[:split], y[:split], rcond=None)
    return 1 - np.sum((y[split:] - X[split:] @ coef) ** 2) / np.sum((y[split:] - y[:split].mean()) ** 2)


def t3_wrong_test_mean(split):  # baseline is the test mean, not the train mean
    df = pd.read_csv("qd-signal.csv")
    X = np.column_stack([np.ones(len(df) - 1), df["x1"].to_numpy()[:-1], df["x2"].to_numpy()[:-1]])
    y = df["ret"].to_numpy()[1:]
    coef, *_ = np.linalg.lstsq(X[:split], y[:split], rcond=None)
    return 1 - np.sum((y[split:] - X[split:] @ coef) ** 2) / np.sum((y[split:] - y[split:].mean()) ** 2)


def t3_wrong_whole_sample(split):  # fit on every row: the look-ahead the task is about
    df = pd.read_csv("qd-signal.csv")
    X = np.column_stack([np.ones(len(df) - 1), df["x1"].to_numpy()[:-1], df["x2"].to_numpy()[:-1]])
    y = df["ret"].to_numpy()[1:]
    coef, *_ = np.linalg.lstsq(X, y, rcond=None)
    return 1 - np.sum((y[split:] - X[split:] @ coef) ** 2) / np.sum((y[split:] - y[:split].mean()) ** 2)


def close(a, b, rel=1e-9):
    return abs(a - b) <= rel * max(abs(a), abs(b), 1e-300)


def main():
    out = {}
    md = []
    # ---------------- task 1
    vols = vol_by_ticker()
    sec, counts, nclean = t1_second()
    assert sorted(vols) == sorted(sec) == ["KAPPA", "LAMBDA", "MU"]
    for t in vols:
        assert close(vols[t], sec[t]), (t, vols[t], sec[t])
    assert len(tidy_closes()) == nclean == 773
    assert counts == {"KAPPA": 258, "LAMBDA": 257, "MU": 258}, counts
    raw = list(csv.reader(open("qd-prices.csv")))[1:]
    assert len(raw) == 783 and sum(1 for r in raw if r[2] == "") == 7 and len(raw) - len(set(map(tuple, raw))) == 3
    for fn in (t1_wrong_no_dedupe, t1_wrong_across_tickers, t1_wrong_ddof0, t1_wrong_unsorted):
        w = fn()
        assert any(not close(w[t], vols[t], 1e-7) for t in vols), fn.__name__
    t1_tests = [
        ("len(tidy_closes())", "773", "equal", None),
        ("int(tidy_closes()['close'].isna().sum())", "0", "equal", None),
        ("list(tidy_closes().columns)", "['date', 'ticker', 'close']", "equal", None),
        ("int(tidy_closes().duplicated().sum())", "0", "equal", None),
        ("tidy_closes().groupby('ticker').size().to_dict()", repr(counts), "equal", None),
        ("bool(tidy_closes().groupby('ticker')['date'].apply(lambda s: s.is_monotonic_increasing).all())", "True", "equal", None),
        ("sorted(vol_by_ticker())", "['KAPPA', 'LAMBDA', 'MU']", "equal", None),
    ] + [(f"vol_by_ticker()['{t}']", repr(vols[t]), "isclose", {"rel": 1e-9}) for t in ("KAPPA", "LAMBDA", "MU")]
    out["qd-returns"] = {"vols": vols, "counts": counts, "rows_clean": nclean, "tests": t1_tests}
    print("OK  task 1:", {t: round(v, 6) for t, v in vols.items()}, "rows", nclean, "returns", counts)

    # ---------------- task 2
    for w in (60, 120, 517):
        a, b = windowed_betas(w), t2_second(w)
        assert len(a) == len(b) == 517 - w + 1
        assert all(close(x, float(y)) for x, y in zip(a, b)), w
    df = pd.read_csv("qd-pair.csv")
    assert len(df) == 520 and int(((df["asset"].abs() > 0.25) | (df["mkt"].abs() > 0.25)).sum()) == 3
    r60, r120, r517 = windowed_betas(60), windowed_betas(120), windowed_betas(517)
    wrong = t2_wrong_keep_errors(60)
    assert len(wrong) == 461
    assert not close(sum(wrong), sum(r60), 1e-3) and len(wrong) != len(r60)
    assert windowed_betas(600) == []
    t2_tests = [
        ("len(windowed_betas(60))", "458", "equal", None),
        ("windowed_betas(60)[0]", repr(r60[0]), "isclose", {"rel": 1e-9}),
        ("windowed_betas(60)[-1]", repr(r60[-1]), "isclose", {"rel": 1e-9}),
        ("sum(windowed_betas(60))", repr(sum(r60)), "isclose", {"rel": 1e-9}),
        ("min(windowed_betas(120))", repr(min(r120)), "isclose", {"rel": 1e-9}),
        ("max(windowed_betas(120))", repr(max(r120)), "isclose", {"rel": 1e-9}),
        ("windowed_betas(600)", "[]", "equal", None),
        ("windowed_betas(517)[0]", repr(r517[0]), "isclose", {"rel": 1e-9}),
    ]
    out["qd-rolling-beta"] = {"first60": r60[0], "last60": r60[-1], "full": r517[0], "tests": t2_tests}
    print("OK  task 2: beta first/last (60)", round(r60[0], 6), round(r60[-1], 6), "full sample", round(r517[0], 6), "wrong len", len(wrong))

    # ---------------- task 3
    res = {s: oos_scores(s) for s in (300, 500, 600)}
    for s, rep in res.items():
        c, tr, te = t3_second(s)
        assert all(close(a, b, 1e-8) for a, b in zip(rep["coef"], c)), (s, rep["coef"], c)
        assert close(rep["train_r2"], tr, 1e-8) and close(rep["oos_r2"], te, 1e-7), (s, rep, tr, te)
    r500 = res[500]
    for fn in (t3_wrong_unlagged, t3_wrong_test_mean, t3_wrong_whole_sample):
        assert not close(fn(500), r500["oos_r2"], 1e-4), fn.__name__
    assert r500["train_r2"] > r500["oos_r2"] > 0 and r500["oos_r2"] < 0.2
    t3_tests = [
        ("sorted(oos_scores(500))", "['coef', 'oos_r2', 'train_r2']", "equal", None),
        ("oos_scores(500)['coef']", repr(r500["coef"]), "isclose", {"rel": 1e-8}),
        ("oos_scores(500)['train_r2']", repr(r500["train_r2"]), "isclose", {"rel": 1e-8}),
        ("oos_scores(500)['oos_r2']", repr(r500["oos_r2"]), "isclose", {"rel": 1e-8}),
        ("oos_scores(300)['coef']", repr(res[300]["coef"]), "isclose", {"rel": 1e-8}),
        ("oos_scores(300)['oos_r2']", repr(res[300]["oos_r2"]), "isclose", {"rel": 1e-8}),
        ("oos_scores(600)['oos_r2']", repr(res[600]["oos_r2"]), "isclose", {"rel": 1e-8}),
    ]
    out["qd-out-of-sample"] = {"coef500": r500["coef"], "train500": r500["train_r2"], "oos500": r500["oos_r2"], "oos300": res[300]["oos_r2"], "oos600": res[600]["oos_r2"],
                               "wrong_unlagged": t3_wrong_unlagged(500), "wrong_test_mean": t3_wrong_test_mean(500), "wrong_whole_sample": t3_wrong_whole_sample(500), "tests": t3_tests}
    print("OK  task 3: coef", [round(c, 6) for c in r500["coef"]], "train R2", round(r500["train_r2"], 5), "oos R2", round(r500["oos_r2"], 5))
    print("     wrong: unlagged", round(t3_wrong_unlagged(500), 5), "test-mean baseline", round(t3_wrong_test_mean(500), 5), "whole-sample fit", round(t3_wrong_whole_sample(500), 5))

    # ---------------- embeds
    for name, fns, title in (("qd-returns", (tidy_closes, vol_by_ticker), "Task 1"), ("qd-rolling-beta", (windowed_betas,), "Task 2"), ("qd-out-of-sample", (oos_scores,), "Task 3")):
        md.append(f"##### Reference for `{name}`\n\n```python\nimport numpy as np\nimport pandas as pd\n\n" + "\n".join(inspect.getsource(f) for f in fns) + "```\n")
        md.append("| # | Call | Expected | Compare |\n| --- | --- | --- | --- |")
        for i, (call, exp, cmp_, tol) in enumerate(out[name]["tests"], 1):
            e = exp if len(exp) < 70 else exp[:67] + "..."
            md.append(f"| {i} | `{call}` | `{e}` | {cmp_}{' (tol ' + json.dumps(tol) + ')' if tol else ''} |")
        md.append("")
    json.dump(out, open(os.path.join(HERE, "qd_tasks_tests.json"), "w"), indent=1)
    open(os.path.join(HERE, "qd_tasks_section.md"), "w").write("\n".join(md))
    print("ALL AGREE: 3 tasks")


if __name__ == "__main__":
    main()
