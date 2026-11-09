"""One line per open finding of review-perf-retrofit-13: FAIL while the finding is open, ok once its fix is in.
Exits 1 while any finding is open (by design at the time of the read). Run with any Python 3."""
import json, pathlib, sys
C = pathlib.Path(__file__).resolve().parents[3] / "app" / "content" / "courses"


def item(course, n, iid):
    return next(x for x in json.loads((C / course / f"homework-{n}.json").read_text())["items"] if x["id"] == iid)


eg2, eg4 = item("eigen", 2, "hw-sigma-code"), item("eigen", 4, "h-replicate-svd")
ls3 = item("least-squares", 3, "h-derive-hedge")
ty1, ty2 = item("taylor", 1, "h-prove-newton-error"), item("taylor", 2, "h2-prove-perpetuity-series")
checks = [
    ("LS3-1 row 4 accepts any valid route to the hedge", "another valid route" in ls3["rubric"][3]["text"]),
    ("TY2-1 model (a) states where the series equals f(h)", "|h| < 0.05$ (the optional part" in ty2["model"]),
    ("TY2-1 rubric row 1 names the series, not an unconditional f(h) =", "Second, the Maclaurin series $100" in ty2["rubric"][0]["text"]),
    ("EG2-1 question glosses |w| = 1 as length, not the budget rule", "not the budget rule" in eg2["question"]),
    ("EG2-2 explain says weighted average", "weighted by" in eg2["explain"]["text"]),
    ("EG4-1 the cut-off governs 'nearest' and 'shortest'", eg4["question"].count("Treating a singular value below") == 1),
    ("TY1-1 (b) carries the hypothesis f'' continuous", "(b) Suppose $f''$ is continuous" in ty1["prompt"] and "Since $f''$ is continuous" in ty1["model"]),
    ("TY1-2 sign rule names f' > 0 and the side", "$f' > 0$ and $f'' > 0$" in ty1["model"] and "at or to the right of the root" in ty1["model"]),
]
bad = 0
for name, ok in checks:
    print(("ok   " if ok else "FAIL ") + name)
    bad += not ok
sys.exit(1 if bad else 0)
