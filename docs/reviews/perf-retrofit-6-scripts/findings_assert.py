"""One check per finding in review-perf-retrofit-6.md. Exits 1 while any finding is open (by design);
each FAIL line names its finding and turns to ok when the fix lands. Python 3, from this folder."""
import json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
C = ROOT / "app" / "content" / "courses"
R = ROOT / "docs" / "reports"
fails = 0

def item(course, f, iid):
    return next(i for i in json.loads((C / course / f).read_text())["items"] if i["id"] == iid)

def check(fid, ok, what):
    global fails
    print(("ok   " if ok else "FAIL ") + f"{fid}: {what}")
    fails += not ok

due = item("contests", "homework-3.json", "hw3-due-order")["widget"]
rows = [r["text"] for r in due["rubric"]]
check("CON-1", "inversion" in rows[1] and "inversion" in rows[3],
      "rubric rows 2 and 4 accept the adjacent-inversion route")
check("CON-2", "never waits, which" in due["model"] or "never-wait rule, which" in due["model"],
      "the model says what the rule that never waits does")

ens = item("ensembles", "homework-2.json", "hw-floor-derive")["widget"]
check("ENS-1", "one mean" in ens["rubric"][0]["text"],
      "rubric row 1 asks for one mean, one variance and one correlation, not identical laws alone")
check("ENS-2", "training sample as random" in ens["prompt"],
      "the prompt says the training sample is random as well as the growing draws")

fm = item("fin-ml", "homework-2.json", "h-return-rank")["widget"]
check("FM2-1", any("unique()[2]].reset_index" in (t.get("setup") or "") for t in fm["tests"]),
      "a hidden test drops a business day, so a BDay look-back fails")

al = item("alpha", "homework-4.json", "h-neutral-book")
check("AL4-1", "a Series of the book" in al["question"], "the question names split_pnl's return type")

for rep in ("alpha-4", "contests-3", "ensembles-2"):
    t = (R / f"{rep}-perf.md").read_text()
    check("REP-1", bool(re.search(r"^(#+ *|- *|\*\*)?Overlapping screens", t, re.M)), f"{rep}-perf.md has an Overlapping screens line")
check("OD4-1", "verb rule" in (R / "opt-dash-4-perf.md").read_text(), "opt-dash-4 report says why the kind is code")

print("FAILS", fails)
sys.exit(1 if fails else 0)
