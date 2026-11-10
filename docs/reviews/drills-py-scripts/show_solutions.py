"""Print the model solution of each code task that defines one of the named functions.
Run from the repo root: python docs/reviews/drills-py-scripts/show_solutions.py <course> <name> [<name> ...]"""
import json, re, sys, glob, os

course, names = sys.argv[1], set(sys.argv[2:])


def walk(o, base):
    if isinstance(o, dict):
        sol = o.get('solution') if isinstance(o.get('solution'), str) else (o.get('code') if isinstance(o.get('code'), str) else None)
        if sol:
            found = set(re.findall(r'(?:def|class)\s+([A-Za-z_]\w*)', sol + str(o.get('starter', ''))))
            if (found & names) or ('ALL' in names):
                print(f'--- {base} {sorted(found)}')
                print(sol.strip()[:900])
        for v in o.values():
            walk(v, base)
    elif isinstance(o, list):
        for v in o:
            walk(v, base)


for f in sorted(glob.glob(f'app/content/courses/{course}/*.json')):
    walk(json.load(open(f)), os.path.basename(f)[:-5])
