"""Print a problem set compactly for reading.
Run from the repo root: python3 docs/reviews/review-problems-complex-1-3-scripts/show.py <n> [item-index]"""
import json
import sys

n = sys.argv[1]
d = json.load(open(f"app/content/courses/complex/problems-{n}.json"))
sel = int(sys.argv[2]) if len(sys.argv) > 2 else None


def dump(o, ind=0):
    p = "  " * ind
    if isinstance(o, dict):
        for k, v in o.items():
            if isinstance(v, (dict, list)):
                print(f"{p}{k}:")
                dump(v, ind + 1)
            else:
                print(f"{p}{k}: {v}")
    elif isinstance(o, list):
        for i, v in enumerate(o):
            if isinstance(v, (dict, list)):
                print(f"{p}[{i}]")
                dump(v, ind + 1)
            else:
                print(f"{p}- {v}")


print({k: v for k, v in d.items() if k != "items"})
for i, it in enumerate(d["items"]):
    if sel is not None and i != sel:
        continue
    print("=" * 30, i)
    dump(it)
