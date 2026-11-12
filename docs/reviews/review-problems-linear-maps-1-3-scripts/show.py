"""Print a problem set for reading. Run from the repo root: python show.py <n>"""
import json
import sys

n = sys.argv[1]
d = json.load(open(f"app/content/courses/linear-maps/problems-{n}.json"))
print({k: v for k, v in d.items() if k != "items"})
for i, it in enumerate(d["items"]):
    print("=" * 100)
    print(f"ITEM {i}", {k: v for k, v in it.items() if k not in ("parts", "prose")})
    print("PROSE:", it.get("prose"))
    for j, p in enumerate(it["parts"]):
        print("-" * 60)
        print(f"PART {j + 1}")
        print(json.dumps(p, indent=1, ensure_ascii=False))
