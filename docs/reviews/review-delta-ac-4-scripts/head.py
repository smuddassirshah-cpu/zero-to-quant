"""Everything of an item but its parts (prose, tables, figures), and the non-text keys of each part.
   python docs/reviews/review-delta-ac-4-scripts/head.py <file under app/content, no .json> <id> [<id> ...]"""
import json
import sys

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from dump import find, load  # noqa: E402

d = load(sys.argv[1])
for pid in sys.argv[2:]:
    it = find(d, pid)
    print("=" * 10, pid)
    print(json.dumps({k: v for k, v in it.items() if k != "parts"}, ensure_ascii=False))
    for i, p in enumerate(it.get("parts", []), 1):
        rest = {k: v for k, v in p.items() if k not in ("widget", "feedback", "explain", "question")}
        if rest:
            print(f" [{i}]", json.dumps(rest, ensure_ascii=False))
