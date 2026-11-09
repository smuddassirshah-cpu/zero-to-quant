"""sql level 1 performance task h-cash-bonds: every number recomputed twice.

Route A runs the item's own solution, starter and planted bugs in sqlite3, the way the
code widget does (code once, then each test's setup and call in order, sharing globals).
Route B filters and sorts the rows in plain Python, without SQL, and must agree with
every expect literal. Run from the repo root: python3 docs/reports/sql-1-perf-numbers.py
"""
import ast, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HW = os.path.join(ROOT, "app/content/courses/sql/homework-1.json")
hw = json.load(open(HW))
item = next(it for it in hw["items"] if it["id"] == "h-cash-bonds")
w = item["widget"]
fails = []
def check(ok, msg):
    print(("ok   " if ok else "FAIL ") + msg)
    if not ok: fails.append(msg)

# ---- shape -------------------------------------------------------------
check(item["performance"] == "code" and w["kind"] == "code", "code performance item")
check(len(w["tests"]) >= 3 and len(w["tests"]) > len(w["examples"]), f"{len(w['tests'])} tests > {len(w['examples'])} examples")
check(f"{len(w['tests'])} hidden tests" in w["how"], "how names the test count")
check(sum(1 for it in hw["items"] if it.get("performance")) == 1, "one performance item in homework-1")
check(6 <= len(hw["items"]) <= 12, f"homework has {len(hw['items'])} items (6 to 12)")

# ---- the harness (route A) ---------------------------------------------
def run(src, query_sql=None):
    """Returns the list of pass/fail per test; query_sql replaces the returned SQL."""
    if query_sql is not None:
        src = re.sub(r'def query\(\):\n(.|\n)*', 'def query():\n    return ' + json.dumps(query_sql) + '\n', src)
    ns = {}
    exec(src, ns)
    out = []
    for t in w["tests"]:
        try:
            if t.get("setup"): exec(t["setup"], ns)
            out.append(eval(t["call"], ns) == ast.literal_eval(t["expect"]))
        except Exception:
            out.append(False)
    return out

sol = run(w["solution"])
check(all(sol), f"solution passes {sum(sol)} of {len(sol)}")
st = run(w["starter"])
check(not any(st), f"starter fails {len(st) - sum(st)} of {len(st)}")
check(w["solution"].split("def query")[0] == w["starter"].split("def query")[0], "starter and solution build the same table")

# ---- route B: plain Python over the same rows --------------------------
ns = {}
exec(w["starter"].split("def query")[0], ns)
rows = ns["db"].execute("SELECT * FROM bonds").fetchall()
canvas = item["canvas"]["params"]["rows"]
def cell(v):
    return "NULL" if v is None else (f"{v:.2f}" if isinstance(v, float) else v)
check([[cell(v) for v in r] for r in rows] == canvas, "canvas rows equal the table the starter builds")

def by_hand(rs):
    keep = [r for r in rs if r[1] in ("AAA", "AA") and r[2] is not None]
    keep.sort(key=lambda r: -r[3])          # yield, highest first
    keep.sort(key=lambda r: r[2])           # stable sort: maturity, soonest first
    return [(r[0], r[2], r[3]) for r in keep[:4]]

state = list(rows)
for i, t in enumerate(w["tests"], 1):
    if t.get("setup"):
        m = re.search(r"VALUES \('([^']*)', '([^']*)', (NULL|'[^']*'), ([0-9.]+)\)", t["setup"])
        mat = None if m.group(3) == "NULL" else m.group(3).strip("'")
        state.append((m.group(1), m.group(2), mat, float(m.group(4))))
    if "fetchall" in t["call"]:
        check(by_hand(state) == ast.literal_eval(t["expect"]), f"test {i}: hand sort equals expect")
check(ast.literal_eval(w["tests"][1]["expect"]) == ["bond", "maturity", "yield"], "test 2 columns")

# the tie at the cut: in the base table two eligible bonds share the fourth date
elig = sorted([r for r in rows if r[1] in ("AAA", "AA") and r[2]], key=lambda r: r[2])
fourth = elig[3][2]
tied = [r[0] for r in elig if r[2] == fourth]
check(fourth == "2028-01-31" and sorted(tied) == ["TSY 28", "WB 28"], f"tie at the cut on {fourth}: {tied}")
check([r[0] for r in rows].index("WB 28") < [r[0] for r in rows].index("TSY 28"), "WB 28 stored before TSY 28, so no tie-break shows")

# ---- numbers in the words ---------------------------------------------
fb = item["feedback"]["byKey"]
setups = {re.search(r"'([^']*)'", t["setup"]).group(1): t["setup"] for t in w["tests"] if t.get("setup")}
check("'2028-01-31', 2.40" in setups["EFSF 28"] and "31 January 2028 at 2.40" in fb["test-3"], "test 3 words match its row")
check("'2028-01-31', 4.05" in setups["BNG 28"] and "31 January 2028 at 4.05" in fb["test-4"] and 4.05 > 3.82, "test 4 words match its row")
check("NULL" in setups["RABO PERP"], "test 5 row is a perpetual")
check("'2026-12-07'" in setups["TSY 26"] and "7 December 2026" in fb["test-6"], "test 6 words match its row")
t6 = ast.literal_eval(w["tests"][5]["expect"]); t4 = ast.literal_eval(w["tests"][3]["expect"])
check(t6[0][0] == "TSY 26" and "BNG 28" in [r[0] for r in t4] and "BNG 28" not in [r[0] for r in t6], "test 6: TSY 26 first, BNG 28 drops out")
check("WB 28 and TSY 28 tie on 31 January 2028" in item["explain"]["text"] and "TSY 28 is fourth" in item["explain"]["text"], "explain names the tie")
idx = {r[0]: i for i, r in enumerate(rows)}
check(sorted(item["explain"]["canvas"]["shade"]) == sorted(f"r{idx[b]}" for b, _, _ in ast.literal_eval(w["tests"][0]["expect"])), "explain shades the four answer rows")

# ---- planted wrong solutions: each must fail a hidden test ---------------
SEL = "SELECT bond, maturity, yield FROM bonds "
GOOD_W = "WHERE (rating = 'AAA' OR rating = 'AA') AND maturity IS NOT NULL "
bugs = {
    "no rating condition": SEL + "WHERE maturity IS NOT NULL ORDER BY maturity, yield DESC LIMIT 4",
    "AA only, AAA forgotten": SEL + "WHERE rating = 'AA' AND maturity IS NOT NULL ORDER BY maturity, yield DESC LIMIT 4",
    "LIKE 'A%' lets A in": SEL + "WHERE rating LIKE 'A%' AND maturity IS NOT NULL ORDER BY maturity, yield DESC LIMIT 4",
    "no NULL test": SEL + "WHERE (rating = 'AAA' OR rating = 'AA') ORDER BY maturity, yield DESC LIMIT 4",
    "maturity <> NULL": SEL + "WHERE (rating = 'AAA' OR rating = 'AA') AND maturity <> NULL ORDER BY maturity, yield DESC LIMIT 4",
    "no brackets, AAA first": SEL + "WHERE rating = 'AAA' OR rating = 'AA' AND maturity IS NOT NULL ORDER BY maturity, yield DESC LIMIT 4",
    "no brackets, AA first": SEL + "WHERE rating = 'AA' OR rating = 'AAA' AND maturity IS NOT NULL ORDER BY maturity, yield DESC LIMIT 4",
    "maturity DESC": SEL + GOOD_W + "ORDER BY maturity DESC, yield DESC LIMIT 4",
    "tie-break ascending": SEL + GOOD_W + "ORDER BY maturity, yield LIMIT 4",
    "no tie-break": SEL + GOOD_W + "ORDER BY maturity LIMIT 4",
    # no tie-break under either tie order SQLite might use: stored order, and reverse stored order
    "no tie-break, stored order": SEL + GOOD_W + "ORDER BY maturity, rowid LIMIT 4",
    "no tie-break, reverse stored order": SEL + GOOD_W + "ORDER BY maturity, rowid DESC LIMIT 4",
    "keys swapped": SEL + GOOD_W + "ORDER BY yield DESC, maturity LIMIT 4",
    "LIMIT 3": SEL + GOOD_W + "ORDER BY maturity, yield DESC LIMIT 3",
    "LIMIT 5": SEL + GOOD_W + "ORDER BY maturity, yield DESC LIMIT 5",
    "SELECT *": "SELECT * FROM bonds " + GOOD_W + "ORDER BY maturity, yield DESC LIMIT 4",
}
caught = 0
for name, q in bugs.items():
    r = run(w["solution"], q)
    first = r.index(False) + 1 if False in r else None
    check(first is not None, f"bug '{name}' fails test {first}")
    caught += first is not None
check(caught >= 3, f"{caught} planted bugs caught (3 or more needed)")
# the reverse-order slip passes test 1 (TSY 28 was stored after WB 28) and only a hidden test catches it
check(run(w["solution"], bugs["no tie-break, reverse stored order"]).index(False) + 1 == 3, "reverse stored order is caught by hidden test 3, not the example")

print(f"\n{len(fails)} failures")
sys.exit(1 if fails else 0)
