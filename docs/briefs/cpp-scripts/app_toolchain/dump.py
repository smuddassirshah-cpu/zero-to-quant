# Dumps every problem of ../problems_*.py to probs.json for run.mjs (the app-toolchain runner).
import sys, os, importlib, json
H = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
sys.path.insert(0, H)
sys.dont_write_bytecode = True
out = {}
for m in ["problems_l19", "problems_l20", "problems_l21", "problems_l22", "problems_l23", "problems_hw", "problems_exam"]:
    mod = importlib.import_module(m)
    for P in mod.PROBLEMS if hasattr(mod, "PROBLEMS") else [mod.P]:
        out[P['id']] = {k: P[k] for k in P if k in ('id', 'starter', 'solution', 'mutants', 'uncaught', 'alts', 'prelude', 'postlude', 'tests', 'alloc', 'leak')}
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'probs.json'), 'w'), indent=1)
print({k: (len(v.get('mutants', {})), len(v['tests'])) for k, v in out.items()})
