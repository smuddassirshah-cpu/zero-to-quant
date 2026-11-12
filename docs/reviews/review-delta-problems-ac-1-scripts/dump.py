"""Print the changed items as they stand. Run from the repo root:
   python docs/reviews/review-delta-problems-ac-1-scripts/dump.py [id ...]"""
import json
import sys

ITEMS = [
    ("elimination/problems-1", "p-courier-rounds"),
    ("elimination/problems-2", "p-tilted-gantry"),
    ("elimination/problems-2", "p-futures-packages"),
    ("elimination/problems-3", "p-vinyl-cutter"),
    ("least-squares/problems-3", "p-gas-hubs"),
    ("eigen/problems-2", "p-river-gauges"),
    ("eigen/problems-2", "p-tank-thermometers"),
    ("eigen/problems-3", "p-crab-sizes"),
    ("testing/problems-3", "p-gene-screen"),
]


def load(f):
    return json.load(open(f"app/content/courses/{f}.json"))


def find(d, pid):
    if isinstance(d, dict):
        if d.get("id") == pid:
            return d
        for v in d.values():
            r = find(v, pid)
            if r:
                return r
    elif isinstance(d, list):
        for v in d:
            r = find(v, pid)
            if r:
                return r
    return None


def item(pid):
    for f, p in ITEMS:
        if p == pid:
            return find(load(f), pid)
    raise KeyError(pid)


if __name__ == "__main__":
    want = sys.argv[1:]
    for f, pid in ITEMS:
        if want and pid not in want:
            continue
        print("=" * 20, f, pid)
        print(json.dumps(find(load(f), pid), indent=1, ensure_ascii=False))
