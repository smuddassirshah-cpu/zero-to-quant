# Runs every problem in the cpp level 5 brief (g++ and clang++, c++17 and c++20, -O1 -fno-exceptions).
# Usage: python3 run_all.py [problem-module ...]   (default: all)
import sys, os, importlib, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from harness import run
MODS = sys.argv[1:] or ["problems_l19", "problems_l20", "problems_l21", "problems_l22", "problems_l23", "problems_hw", "problems_exam"]
ok = True
for m in MODS:
    mod = importlib.import_module(m)
    for P in mod.PROBLEMS if hasattr(mod, "PROBLEMS") else [mod.P]:
        ok &= run(P)
        # write the files the brief refers to
        here = os.path.dirname(os.path.abspath(__file__))
        open(f"{here}/{P['id']}_starter.cpp", "w").write(P["starter"])
        open(f"{here}/{P['id']}_solution.cpp", "w").write(P["solution"])
        json.dump({k: P[k] for k in P if k in ("prelude", "postlude", "tests", "alloc", "leak")}, open(f"{here}/{P['id']}_tests.json", "w"), indent=1)
print("ALL PROBLEMS OK" if ok else "SOME PROBLEM")
