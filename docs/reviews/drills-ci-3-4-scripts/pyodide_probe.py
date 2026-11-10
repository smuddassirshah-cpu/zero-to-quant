"""Put candidates from wrong.py into a COPY of app/ as `planted`, to run them in Pyodide.

usage: pyodide_probe.py <copy of app> <fn__tag> [<fn__tag> ...] [--tests extra_tests.json]
Then, from the real app/:
  ZQ_APP_DIR=<copy> node tools/planted-check.mjs --drill <id> ... --local-cdn <pkgs>
A line "FAIL <id>: ..." there means the candidate passed every hidden test in the browser runtime.
With --tests, the proposed tests of extra_tests.json are appended to the copy's drills first.
Never point this at the real app/: it rewrites drill files.
"""
import glob
import inspect
import json
import os
import sys

here = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, here)
import wrong  # noqa: E402

HEAD = "import bisect\nimport heapq\nimport re\nimport sys\nfrom collections import Counter, deque\n\n"
app = sys.argv[1]
assert os.path.abspath(app) != os.path.abspath(os.path.join(here, "..", "..", "..", "app")), "use a copy"
names = [a for a in sys.argv[2:] if "__" in a]
extra = {}
if "--tests" in sys.argv:
    extra = json.load(open(sys.argv[sys.argv.index("--tests") + 1]))
by_fn = {}
for f in glob.glob(app + "/content/drills/ci-*.json"):
    d = json.load(open(f))
    if "fn" in d:
        by_fn[d["fn"]] = (f, d)
todo = {}
for name in names:
    todo.setdefault(name.split("__")[0], []).append(name)
for fn, cands in todo.items():
    f, d = by_fn[fn]
    d["planted"] = []
    for name in cands:
        src = inspect.getsource(getattr(wrong, name)).replace(name, fn)
        if "_kids(" in src:
            src = inspect.getsource(wrong._kids) + "\n" + src
        d["planted"].append({"code": HEAD + src, "slip": name})
    d["tests"] += extra.get(d["id"], [])
    json.dump(d, open(f, "w"), indent=2)
    print(d["id"], [p["slip"] for p in d["planted"]], len(d["tests"]), "tests")
