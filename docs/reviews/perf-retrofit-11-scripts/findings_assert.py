"""One line per finding in review-perf-retrofit-11: FAIL while the finding is open, ok once its fix is in the content.
Exits 1 while any finding is open (by design). Run with any Python 3: python3 findings_assert.py"""
import json, pathlib, re, sys
ROOT = pathlib.Path(__file__).resolve().parents[3]
C = ROOT / "app" / "content" / "courses"
def it(course, f, iid):
    return next(x for x in json.loads((C / course / f).read_text())["items"] if x["id"] == iid)
open_ = 0
def finding(fid, fixed, what):
    global open_
    print(("ok   " if fixed else "FAIL ") + fid + ": " + what)
    open_ += 0 if fixed else 1

cd2 = it("conditional", "homework-2.json", "h-two-filters")
finding("CD2-1", "optional" in cd2["prompt"].lower(), "the prompt marks the second-route check (rubric row 5) optional")
es2 = it("estimation", "homework-2.json", "hw2-pareto-tail")
finding("ES2-1", "density $\\alpha e^{-\\alpha y}$" in es2["rubric"][2]["text"], "row 3 accepts the density of ln X as well as its tail")
finding("ES2-2", "chance 1" in es2["model"].split("**(b)**")[0], "model (a) states that S > 0 is assumed (it holds with chance 1)")
lf = it("estimation", "homework-2.json", "hw2-longform")
finding("ES2-3", all("aligned" in m for m in re.findall(r"\$\$(.*?)\$\$", lf["model"], re.S) if "MSE" in m), "hw2-longform's MSE display is split with aligned")
np2 = it("numpy-pandas", "homework-2.json", "h-fills-report")
finding("NP2-1", any("ticker" in t["call"] for t in np2["widget"]["tests"]), "a hidden test reads the ticker column")
pl3 = it("plotting", "homework-3.json", "h-price-file-report")
finding("PL3-1", any("arrow_patch" in t["call"] for t in pl3["widget"]["tests"]), "a hidden test checks the annotation has an arrow")
finding("PL3-2", "all the returns (their sample standard deviation" in pl3["prose"], "the suptitle bullet says which standard deviation")
cd4 = it("conditional", "homework-4.json", "h-host-rules-code")
finding("CD4-1", "may not place" not in cd4["prose"], "the prose says the car need not be placed evenly")
l11 = json.loads((C / "regression" / "l11-assumptions-fail.json").read_text())["screens"][2]["explain"]["text"]
finding("RG-V1", len([s for s in re.split(r"(?<=[.?])\s+", l11.strip()) if s]) <= 3, "regression l11 screens[2] explain has at most three sentences")
h5 = json.loads((C / "conditional" / "homework-5.json").read_text())["items"][7]["model"]
finding("CD-V1", "stricter, all of which" not in h5, "conditional homework-5 items[7] model has no sentence over 35 words")
rs = (ROOT / "docs" / "reports" / "regression-2-perf-numbers.py").read_text()
finding("RG2-1", "close(got, want, 1e-12, 1e-12)" not in rs, "regression-2 numbers script compares expects at the test's 1e-9, so it passes on Pyodide's SciPy 1.14.1")
print("open findings:", open_)
sys.exit(1 if open_ else 0)
