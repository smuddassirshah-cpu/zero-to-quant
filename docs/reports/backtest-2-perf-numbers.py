"""backtest level 2 performance task (h2-never-peeks): every number recomputed.

Run with a Python that has numpy and pandas 2.2 (the scratch venv):
    python docs/reports/backtest-2-perf-numbers.py
Runs the model test, the starter and nine plausible wrong tests through every
hidden case; checks each engine's leak by a second route; checks the model test
on other data lengths and seeds. Exits 0 when every check passes.
"""
import json, os, sys
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HW = os.path.join(ROOT, "app/content/courses/backtest/homework-2.json")
FAIL = []

def check(name, ok):
    print(("ok   " if ok else "FAIL ") + name)
    if not ok:
        FAIL.append(name)

doc = json.load(open(HW, encoding="utf-8"))
item = next(i for i in doc["items"] if i["id"] == "h2-never-peeks")
w = item["widget"]

def namespace(src):
    ns = {"__learner_source__": src, "__name__": "__main__"}
    exec(w["prelude"], ns)
    exec(src, ns)
    return ns

def results(src):
    out = []
    for case in w["tests"]:
        try:
            ns = namespace(src)
            out.append(eval(case["call"], ns) == eval(case["expect"], ns))
        except Exception:
            out.append(False)
    return out

# ---- shape and stated counts ----
tests, examples = w["tests"], w["examples"]
check("9 hidden tests, as `how` says", len(tests) == 9 and "9 hidden tests" in w["how"])
check("examples are tests 1 and 2, fewer than tests", examples == tests[:2] and len(tests) > len(examples))
honest = [c for c in tests if c["expect"] == "'passed'"]
check("three honest engines, six leaky (how)", len(honest) == 3 and len(tests) - len(honest) == 6
      and "three keep the contract" in w["how"] and "six break it" in w["how"])
check("25 s per test = 5 s + caseBudget 20000 ms", w["caseBudget"] == 20000 and "up to 25 s" in w["how"])
check("homework has 6 to 12 items, one performance item",
      6 <= len(doc["items"]) <= 12 and sum(1 for i in doc["items"] if i.get("performance")) == 1)

# ---- model solution and starter ----
check("solution passes every test", all(results(w["solution"])))
st = results(w["starter"])
check("starter fails", not all(st))
print("     starter passes tests", [k + 1 for k, ok in enumerate(st) if ok])

# ---- plausible wrong tests: each must fail at least one hidden case ----
HEAD = "import numpy as np\nimport pandas as pd\n\n\ndef test_never_peeks(engine):\n"
def body(code):
    return HEAD + "".join("    " + line + "\n" for line in code.strip("\n").split("\n"))

def method(cuts="range(1, len(bars))", n=200, keep_open=True, settled=True, rows_upto=False, truncate=True, noise=True):
    return body(f"""
bars = daily_bars({n})
full = engine(bars)
rng = np.random.default_rng(0)
for cut in {cuts}:
    if {truncate}:
        part = engine(bars.iloc[:cut])
        assert np.allclose(part.to_numpy(), full.iloc[:cut].to_numpy(), rtol=0, atol=1e-9)
    if {noise}:
        alt = bars.copy()
        alt.iloc[cut:] = bars.iloc[cut:].to_numpy() * np.exp(0.05 * rng.standard_normal((len(bars) - cut, 5)))
        if {keep_open}:
            alt.iloc[cut, 0] = bars['open'].iloc[cut]
        run = engine(alt)
        upto = cut + 1 if {rows_upto} else cut
        assert np.allclose(run.iloc[:upto].to_numpy(), full.iloc[:upto].to_numpy(), rtol=0, atol=1e-9)
        if {settled}:
            assert np.allclose(run[['shares', 'cash']].iloc[cut].to_numpy(), full[['shares', 'cash']].iloc[cut].to_numpy(), rtol=0, atol=1e-9)
""")

wrong = {
    "lesson-style: three cuts, rows before the cut only": method(cuts="(50, 100, 150)", keep_open=False, settled=False),
    "every cut, rows before the cut only": method(keep_open=False, settled=False),
    "too strict: row cut compared in every column": method(rows_upto=True, settled=False),
    "settled check, but bar cut's open changed too": method(keep_open=False),
    "every fifth cut, full method": method(cuts="range(5, len(bars), 5)"),
    "cut form only, every cut": method(noise=False),
    "full method on 12 bars": method(n=12),
    "Sharpe below 2": body("""
eq = engine(daily_bars(250))['equity']
r = eq.pct_change().dropna()
assert (252 ** 0.5) * r.mean() / r.std() < 2
"""),
    "compares with clean_engine": body("""
bars = daily_bars(200)
assert np.allclose(engine(bars).to_numpy(), clean_engine(bars).to_numpy())
"""),
}
first = {}
for name, src in wrong.items():
    r = results(src)
    first[name] = next((k + 1 for k, ok in enumerate(r) if not ok), None)
    check(f"wrong test caught: {name} (first failing case {first[name]})", first[name] is not None)
check("the full method written this way passes every case (harness sanity)", all(results(method())))

# byKey lines: the slip named fails that case
r = {name: results(src) for name, src in wrong.items()}
check("byKey test-3: comparing with clean_engine fails case 3", not r["compares with clean_engine"][2])
check("byKey test-5: every fifth cut misses the rare leak (case 5)", not r["every fifth cut, full method"][4]
      and all(r["every fifth cut, full method"][k] for k in range(9) if k != 4))
check("byKey test-8, test-9: rows-before-only tests miss same-close and cost leaks",
      not r["every cut, rows before the cut only"][7] and not r["every cut, rows before the cut only"][8]
      and not r["cut form only, every cut"][7] and not r["cut form only, every cut"][8])

# ---- second route: each engine's leak, measured directly ----
ns = namespace(w["solution"])
bars = ns["daily_bars"](120, 3)
def cut_moves(e, cut):
    a = e(bars.iloc[:cut]).to_numpy()
    b = e(bars).iloc[:cut].to_numpy()
    return not np.allclose(a, b, rtol=0, atol=1e-9)
def close_moves(e, t):
    alt = bars.copy()
    alt.iloc[t, alt.columns.get_loc("close")] *= 1.01
    a, b = e(alt), e(bars)
    return not np.allclose(a[["shares", "cash"]].iloc[t].to_numpy(), b[["shares", "cash"]].iloc[t].to_numpy(), rtol=0, atol=1e-9)
names = ["clean_engine", "_fade", "_slow", "leaky_engine", "_rare", "_vol", "_gap", "_same", "_cost"]
cut_hit = {k: [c for c in range(2, len(bars)) if cut_moves(ns[k], c)] for k in names}
close_hit = {k: [t for t in range(1, len(bars)) if close_moves(ns[k], t)] for k in names}
for k in ["clean_engine", "_fade", "_slow"]:
    check(f"{k} honest: no cut moves it, no close moves its settled row", not cut_hit[k] and not close_hit[k])
for k, lb in (("leaky_engine", 10), ("_vol", 3), ("_gap", 20)):
    check(f"{k}: every cut past its lookback of {lb} catches it ({len(cut_hit[k])} of 118 cuts)",
          cut_hit[k] == list(range(lb + 1, len(bars))))
check("_rare: only cuts 14, 39, 64, 89, 114 catch it (rows 13 mod 25)", cut_hit["_rare"] == [14, 39, 64, 89, 114])
check("_rare: no multiple of 5 among them", all(c % 5 for c in cut_hit["_rare"]))
for k in ["_same", "_cost"]:
    check(f"{k}: no cut catches it, but its settled row moves with the close ({len(close_hit[k])} bars)",
          not cut_hit[k] and len(close_hit[k]) > 100)

# ---- the model test is not tied to its own data ----
src = w["solution"]
for n, seed in ((60, 1), (120, 2), (300, 9)):
    s2 = src.replace("bars = daily_bars(200)", f"bars = daily_bars({n}, {seed})")
    check(f"model test on daily_bars({n}, {seed}) still passes every case", all(results(s2)))

print("\n%d failure(s)" % len(FAIL))
sys.exit(1 if FAIL else 0)
