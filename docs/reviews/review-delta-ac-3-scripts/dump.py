"""Print items as they stand. Run from the repo root:
   python docs/reviews/review-delta-ac-3-scripts/dump.py <file under app/content, no .json> [id ...]
   With no id, lists the item ids of the file."""
import json
import sys


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


def load(f):
    return json.load(open(f"app/content/{f}.json"))


if __name__ == "__main__":
    d = load(sys.argv[1])
    for pid in sys.argv[2:]:
        print("=" * 20, sys.argv[1], pid)
        print(json.dumps(find(d, pid), indent=1, ensure_ascii=False))
    if not sys.argv[2:]:
        items = d.get("items") or d.get("screens") or []
        print([i.get("id") for i in items])
