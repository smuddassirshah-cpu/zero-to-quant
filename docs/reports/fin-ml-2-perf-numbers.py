"""fin-ml level 2 performance task `h-return-rank`: recompute every number and grade every route.

Run with a Python that has pandas 2.2.3 and NumPy (the session venv), from anywhere:
    <venv>/bin/python -I docs/reports/fin-ml-2-perf-numbers.py
Reads the item from app/content/courses/fin-ml/homework-2.json, then
1. runs the shipped solution against every test and checks each expect string;
2. runs an independent plain-loop solution (no groupby, no rank) and three other correct routes;
3. recomputes tests 1 and 2 by hand arithmetic;
4. runs the starter (must fail every test) and 25 planted bugs (each must fail a test),
   and checks that each bug's first failing test has a byKey line;
5. checks the counts the item states (14 tests, 1 example, the panel sizes, k, the 15th date).
Exits 1 on any failure.
"""
import json
import math
import pathlib
import warnings

warnings.simplefilter("ignore")
ROOT = pathlib.Path(__file__).resolve().parents[2]
HW = ROOT / "app/content/courses/fin-ml/homework-2.json"
item = next(i for i in json.loads(HW.read_text())["items"] if i["id"] == "h-return-rank")
W = item["widget"]
PRELUDE, SOLUTION, STARTER, TESTS = W["prelude"], W["solution"], W["starter"], W["tests"]
FAILS = []


def check(ok, what):
    print(("ok   " if ok else "FAIL ") + what)
    if not ok:
        FAILS.append(what)


def evaluate(code):
    """Mirror of the harness: prelude, learner code, setup, then call; compare repr with expect (==)."""
    got = []
    for t in TESTS:
        ns = {}
        try:
            exec(PRELUDE, ns)
            exec(code, ns)
            exec(t.get("setup", ""), ns)
            v = eval(t["call"], ns)
            exp = eval(t["expect"], ns)
            got.append((v == exp) is True)
        except Exception:
            got.append(False)
    return got


def failing(code):
    return [i + 1 for i, ok in enumerate(evaluate(code)) if not ok]


# 1. the shipped solution
check(failing(SOLUTION) == [], "solution passes all %d tests" % len(TESTS))
for t in TESTS:
    ns = {}
    exec(PRELUDE, ns); exec(SOLUTION, ns); exec(t["setup"], ns)
    check(repr(eval(t["call"], ns)) == t["expect"], "expect string matches solution: " + t["call"][:60])

# 2. independent routes
LOOP = '''import math
import pandas as pd

def return_rank(df, k):
    dates = sorted(set(df["date"]))
    pos = {d: i for i, d in enumerate(dates)}
    close = {(r.date, r.stock): r.close for r in df.itertuples()}
    ret = {}
    for (d, s), c in close.items():
        i = pos[d]
        if i < k:
            continue
        c0 = close[(dates[i - k], s)]
        if c == c and c0 == c0:
            ret[(d, s)] = c / c0 - 1
    out = {}
    for d in dates:
        items = [(v, s) for (dd, s), v in ret.items() if dd == d]
        n = len(items)
        for v, s in items:
            below = sum(1 for w, _ in items if w < v)
            equal = sum(1 for w, _ in items if w == v)
            avg = below + (equal + 1) / 2
            out[(d, s)] = 0.0 if n == 1 else 2 * (avg - 1) / (n - 1) - 1
    return pd.Series([out.get((r.date, r.stock), math.nan) for r in df.itertuples()], index=df.index)
'''
BODY = "import numpy as np\nimport pandas as pd\n\ndef return_rank(df, k):\n{}\n"


def mk(body):
    return BODY.format("\n".join("    " + l for l in body.strip().splitlines()))


SORT = 's = df.sort_values("date")\n'
RET = 'r = s["close"] / s.groupby("stock")["close"].shift(k) - 1'
TAIL = '''g = r.groupby(s["date"])
n = g.transform("count")
q = 2 * (g.rank() - 1) / (n - 1) - 1
q = q.where(n > 1, 0.0).where(r.notna())
return q.reindex(df.index)'''


def std(ret=RET, tail=TAIL, sort=SORT):
    return mk(sort + ret + "\n" + tail)


GOOD = {
    "plain loop, hand average rank": LOOP,
    "log return": std('r = np.log(s["close"]).groupby(s["stock"]).diff(k)'),
    "difference over the past close": std('p = s.groupby("stock")["close"].shift(k)\nr = (s["close"] - p) / p'),
    "pct_change with fill_method=None": std('r = s.groupby("stock")["close"].pct_change(k, fill_method=None)'),
}
for name, code in GOOD.items():
    check(failing(code) == [], "correct route passes every test: " + name)

# 3. hand arithmetic for tests 1 and 2 (toy, k = 1)
A = [10, 11, 12, 11, 13]; B = [20, 20, 22, math.nan, 24]; C = [5, 5, 6.5, 7, 7]; D = [40, 38, 45, 46, 41]
ns = {}; exec(PRELUDE, ns)
toy = ns["toy"]()
check([list(toy[toy.stock == s].close.fillna(-1)) == [x if x == x else -1 for x in v]
       for s, v in zip("ABCD", (A, B, C, D))] == [True] * 4, "toy closes are the ones used here")
check(toy.date.nunique() == 5 and toy.stock.nunique() == 4, "toy(): four shares on five dates")
# date 2: returns A 12/11 - 1 = 0.0909, B 22/20 - 1 = 0.1, C 6.5/5 - 1 = 0.3, D 45/38 - 1 = 0.1842
r2 = {"A": 12 / 11 - 1, "B": 22 / 20 - 1, "C": 6.5 / 5 - 1, "D": 45 / 38 - 1}
order = sorted(r2, key=r2.get)                       # A, B, D, C
check(order == ["A", "B", "D", "C"], "date 2 order lowest first: A, B, D, C")
s2 = {x: -1 + 2 * i / 3 for i, x in enumerate(order)}  # ranks 1..4 -> -1, -1/3, 1/3, 1
check([round(s2[x], 6) for x in "ABCD"] == eval(TESTS[0]["expect"]), "test 1 by hand: [-1, -1/3, 1, 1/3]")
# date 1: A 0.1, B 0, C 0, D -0.0526: D rank 1, B and C ranks 2 and 3 -> 2.5, A rank 4
avg = (2 + 3) / 2
s1 = {"D": -1.0, "B": 2 * (avg - 1) / 3 - 1, "C": 2 * (avg - 1) / 3 - 1, "A": 1.0}
check([round(s1[x], 6) for x in "ABCD"] == eval(TESTS[1]["expect"]), "test 2 by hand: tie at rank 2.5 scores 0")
# date 3: B has no close; A -0.0833, D 0.0222, C 0.0769 -> n = 3, scores -1, 0, 1
r3 = {"A": 11 / 12 - 1, "C": 7 / 6.5 - 1, "D": 46 / 45 - 1}
o3 = sorted(r3, key=r3.get)
check(o3 == ["A", "D", "C"] and eval(TESTS[2]["expect"]) == [-1.0, None, 1.0, 0.0], "test 3 by hand: n = 3, B none")
# test 7: D copies A; date 2 ties A and D at ranks 1 and 2 -> 1.5 -> 2(0.5)/3 - 1 = -2/3
check(round(2 * (1.5 - 1) / 3 - 1, 6) == -0.666667 and eval(TESTS[6]["expect"])[1][0] == -0.666667,
      "test 7 by hand: a tie at ranks 1 and 2 scores -2/3")
# test 11: count of scored rows by a second route (closes at t and t-5 both present, by stock)
p = ns["panel"](7).sort_values("date")
has = p.groupby("stock")["close"].apply(lambda c: int((c.notna() & c.shift(5).notna()).sum())).sum()
check(eval(TESTS[10]["expect"])[0] == has, "test 11: %d scored rows, counted per stock" % has)
check(ns["panel"](7).shape == (360, 3) and p.stock.nunique() == 12 and p.date.nunique() == 30,
      "panel(): 12 shares over 30 dates, 360 rows")
check(0.05 < p.close.isna().mean() < 0.15, "panel(): about one close in ten missing (%.3f)" % p.close.isna().mean())

# 4. starter and planted bugs
check(failing(STARTER) == list(range(1, len(TESTS) + 1)), "starter fails every test")
T = TAIL
BUGS = {
    "rank over time within each stock": mk(SORT + RET + '\ng = r.groupby(s["stock"])\nn = g.transform("count")\nq = (2 * (g.rank() - 1) / (n - 1) - 1).where(n > 1, 0.0).where(r.notna())\nreturn q.reindex(df.index)'),
    "ties by order (method first)": std(tail=T.replace("g.rank()", 'g.rank(method="first")')),
    "ties at the lowest rank (method min)": std(tail=T.replace("g.rank()", 'g.rank(method="min")')),
    "ties dense": std(tail=T.replace("g.rank()", 'g.rank(method="dense")')),
    "pct_change pads a missing close": std('r = s.groupby("stock")["close"].pct_change(k)'),
    "closes forward-filled first": std('c = s.groupby("stock")["close"].ffill()\nr = c / c.groupby(s["stock"]).shift(k) - 1'),
    "missing return ranked as 0": std(RET + '\nok = s.groupby("stock").cumcount() >= k\nr = r.where(ok).fillna(0).where(ok)'),
    "n counts shares with no feature (size)": std(tail=T.replace('transform("count")', 'transform("size")')),
    "n is every share in the table": std(tail=T.replace('g.transform("count")', 'pd.Series(df["stock"].nunique(), index=s.index)')),
    "scaled 0 to 1 (the lesson's range)": std(tail=T.replace("2 * (g.rank() - 1) / (n - 1) - 1", "(g.rank() - 1) / (n - 1)").replace("0.0)", "0.5)")),
    "2 * rank(pct=True) - 1": std(tail='q = 2 * r.groupby(s["date"]).rank(pct=True) - 1\nreturn q.reindex(df.index)'),
    "2 * rank / n - 1": std(tail=T.replace("2 * (g.rank() - 1) / (n - 1) - 1", "2 * g.rank() / n - 1")),
    "return upside down (past over today)": std('r = s.groupby("stock")["close"].shift(k) / s["close"] - 1'),
    "price level ranked": std('r = s["close"].where(s.groupby("stock")["close"].shift(k).notna())'),
    "rows not sorted by date": std(sort="s = df\n"),
    "shift across the whole table": std('r = s["close"] / s["close"].shift(k) - 1', sort='s = df.sort_values(["date", "stock"])\n'),
    "lone share left NaN": std(tail=T.replace("q.where(n > 1, 0.0).where(r.notna())", "q")),
    "lone share scores 1": std(tail=T.replace("q.where(n > 1, 0.0)", "q.where(n > 1, 1.0)")),
    "no feature scores 0 when n <= 1": std(tail=T.replace(".where(r.notna())", "")),
    "shift k - 1": std('r = s["close"] / s.groupby("stock")["close"].shift(k - 1) - 1'),
    "shift k + 1": std('r = s["close"] / s.groupby("stock")["close"].shift(k + 1) - 1'),
    "k calendar days": std('past = s.set_index(["date", "stock"])["close"]\nkey = pd.MultiIndex.from_arrays([s["date"] - pd.Timedelta(days=k), s["stock"]])\nr = pd.Series(s["close"].values / past.reindex(key).values - 1, index=s.index)'),
    "ranked highest first": std(tail=T.replace("g.rank()", "g.rank(ascending=False)")),
    "look-back by BDay offset (ignores a holiday)": mk(SORT + 'p = s.set_index(["date", "stock"])["close"]\nkey = pd.MultiIndex.from_arrays([s["date"] - pd.offsets.BDay(k), s["stock"]])\nr = pd.Series(s["close"].values / p.reindex(key).values - 1, index=s.index)\n' + TAIL),
    "result in date order, index reset": std(tail=T.replace("q.reindex(df.index)", "q.reset_index(drop=True)")),
}
bykey = item["feedback"]["byKey"]
for name, code in BUGS.items():
    f = failing(code)
    check(bool(f), "bug fails tests %s: %s" % (f, name))
    if f:
        check("test-%d" % f[0] in bykey, "  first failing test %d has a byKey line" % f[0])

# 5. stated counts
check(len(TESTS) == 14 and len(W["examples"]) == 1 and len(TESTS) > len(W["examples"]), "14 tests, 1 example")
check(W["examples"][0] in TESTS, "the example is test 1 and is also a hidden test")
check("14 hidden tests" in W["how"] and "12 shares" in W["how"], "`how` states 13 tests and 12 shares")
check("k = 5" in bykey["test-11"] and "return_rank(df, 5)" in TESTS[10]["call"], "test 11 uses k = 5")
check("15th date" in bykey["test-10"] and "[14]" in TESTS[9]["setup"], "test 10 changes closes after the 15th date")
check("`k = 2`" in bykey["test-5"] and "return_rank(df, 2)" in TESTS[4]["call"], "test 5 uses k = 2")
check(set(bykey) == {"test-%d" % i for i in range(1, 15)}, "a byKey line for each of the 14 tests")

print("checks failed:", len(FAILS))
raise SystemExit(1 if FAILS else 0)
