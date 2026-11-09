"""One line per finding in review-perf-retrofit-12: FAIL while the finding is open, ok once its fix is in the content.
Exits 1 while any finding is open. Run with any Python 3: python3 findings_assert.py"""
import json, pathlib, re, subprocess, sys
ROOT = pathlib.Path(__file__).resolve().parents[3]
C = ROOT / "app" / "content" / "courses"
def it(course, f, iid):
    return next(x for x in json.loads((C / course / f).read_text())["items"] if x["id"] == iid)
open_ = 0
def finding(fid, fixed, what):
    global open_
    print(("ok   " if fixed else "FAIL ") + fid + ": " + what)
    open_ += 0 if fixed else 1

rg = it("algo-think", "homework-3.json", "h-ring-search")
w = rg["widget"]
finding("AT3-1", "class Looks" in w.get("prelude", "") and "W.looks <= 400" in w["tests"][12]["call"] and "ring_sweep()" == w["tests"][13]["call"]
        and "test-14" in rg["feedback"]["byKey"] and "Check runs 14 hidden tests" in w["how"], "a hidden test counts the slots read (Looks, at most 400); the sweep is test 14")
bc = it("vectors", "homework-3.json", "h-bond-curve")
finding("VC3-2", "exactly when $\\mathbf{C}$ is square" not in bc["explain"]["text"] and "With one bond per year" in bc["explain"]["text"], "explain no longer says square is needed")
finding("VC3-1", "exactly singular" in bc["question"], "the question says exactly singular and that rounding can hide one")
dv = it("micro", "homework-3.json", "h-derive-tilted-quotes")
finding("MI3-1", "0 < \\alpha < 1" in dv["prompt"] and "at least $\\tfrac12\\alpha > 0$" in dv["model"], "alpha is bounded away from 0 and the denominator is shown positive")
finding("MI3-2", "ignores it, so the chances multiply" in dv["model"] and "An informed buyer costs" not in dv["model"], "both loose model lines tightened")
rv = it("random-vars", "homework-1.json", "h-build-pmf")
finding("RV1-1", "added one at a time" in rv["explain"]["text"], "the explain says ten 0.1s added one at a time")
sp = it("algo-think", "homework-2.json", "h-split-feed")
finding("AT2-1", "$n \\ge 1$" in sp["explain"]["text"], "the explain restricts n to at least 1")
v = subprocess.run([sys.executable, "-I", str(ROOT / "docs/reviews/voice-scan.py"), "35"], cwd=ROOT, env={"VOICE_BASE": str(C / "micro"), "PATH": "/usr/bin:/bin"}, capture_output=True, text=True).stdout
finding("MI-V1", "over 35 words: 0" in v and "over three sentences: 0" in v, "micro voice scan 0 and 0")
print("open findings:", open_)
sys.exit(1 if open_ else 0)
