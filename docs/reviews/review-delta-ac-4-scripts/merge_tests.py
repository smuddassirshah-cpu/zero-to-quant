"""Delta read AC-4, small item 2: bank/coding-2 `ds-pointers-merge-ticks` has 11 hidden tests; docs/briefs/bank-2.md rule 12
allows six to ten. Which test can go?
Every recorded candidate-wrong solution is run on the 11 tests: the first reader's (review-bank-2-b-scripts/cands_2.py),
the delta reader's (review-delta-bank-2-scripts/cands.py), delta AC-2's extras (review-delta-ac-2-scripts/bank_code.py EXTRA)
and its `alias-when-no-shared-time` (proposed_code.py). A test is NEEDED when some wrong candidate fails that test alone;
a test no candidate needs, and that repeats another test's case, is redundant. For each removable test the script then
checks that with it dropped the model passes, the starter fails and every wrong candidate still fails.
Judge and timer: review-delta-bank-2-scripts/code_run_lib.py (the rule of __zq_judge in widgets/code.js).
Run from the repo root with the venv Python:  python docs/reviews/review-delta-ac-4-scripts/merge_tests.py"""
import ast
import importlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REV = os.path.join(HERE, "..")
sys.path.insert(0, os.path.join(REV, "review-delta-bank-2-scripts"))
sys.path.insert(0, os.path.join(REV, "review-bank-2-b-scripts"))
from code_run_lib import run  # noqa: E402
from cands import C  # noqa: E402

IID = "ds-pointers-merge-ticks"
it = next(i for i in json.load(open("app/content/bank/coding-2.json"))["items"] if i["id"] == IID)
w = it["widget"]
tests = w["tests"]

tree = ast.parse(open(os.path.join(REV, "review-delta-ac-2-scripts", "bank_code.py")).read())
EXTRA = next(ast.literal_eval(n.value) for n in tree.body if isinstance(n, ast.Assign) and n.targets[0].id == "EXTRA")
ALIAS = ("alias-when-no-shared-time", "ac-2 proposed_code.py",
         "def merge_ticks(a, b):\n    shared = {t for t, _ in a} & {t for t, _ in b}\n    if not shared:\n        out = a\n        out += b\n"
         "        return sorted(out)\n    d = dict(a)\n    for t, p in b: d[t] = (d[t] + p) / 2 if t in d else p\n    return sorted(d.items())\n")
first = importlib.import_module("cands_2").CANDS[IID]["wrong"]
pool = [("first", *c) for c in first] + [("delta", *c) for c in C[IID]] + [("ac2", *c) for c in EXTRA[IID] if c[2]] + [("ac2", *ALIAS)]

print(f"{IID}: {len(tests)} hidden tests; `how`: {w['how']}")
for i, t in enumerate(tests, 1):
    print(f"  [{i}] {t.get('setup', '')[:70]}{' ; ' if t.get('setup') else ''}{t['call'][:80]}")
model = run(w["solution"], tests)
assert all(x[0] for x in model), "model fails"
starter = [i + 1 for i, x in enumerate(run(w["starter"], tests)) if not x[0]]
print(f"model passes all {len(tests)}; starter fails {len(starter)}")

fails = {}
for src_pool, nm, why, src in pool:
    if nm.startswith("alt:"):
        continue
    r = run(src, tests)
    if all("NameError" in x[2] for x in r):
        continue  # written for the statement before the restating
    f = [i + 1 for i, x in enumerate(r) if not x[0]]
    fails[(src_pool, nm)] = f
    print(f"  {src_pool:5} {nm:28} fails {f}")
ok = all(fails.values())
print(f"wrong candidates run: {len(fails)}; each fails at least one test: {ok}")

needed = {k: [nm for (p, nm), f in fails.items() if f == [k]] for k in range(1, len(tests) + 1)}
for k in range(1, len(tests) + 1):
    without = [t for i, t in enumerate(tests, 1) if i != k]
    survive = [nm for (p, nm), f in fails.items() if set(f) <= {k}]
    print(f"  drop [{k}]: {'NEEDED by ' + ', '.join(needed[k]) if needed[k] else 'no candidate needs it'}"
          f"{'' if not survive else '  -> would pass: ' + ', '.join(survive)}; tests left {len(without)}")
free = [k for k in needed if not needed[k]]
print("removable without letting a recorded candidate through:", free)
dup = [(i + 1, j + 1) for i in range(len(tests)) for j in range(i + 1, len(tests)) if tests[i] == tests[j]]
print("identical tests:", dup)
ex = [i + 1 for i, t in enumerate(tests) if any(t["call"] == e["call"] for e in w["examples"])]
print("tests that repeat a visible example:", ex)
sys.exit(0 if ok else 1)
