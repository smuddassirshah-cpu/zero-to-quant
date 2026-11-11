"""Print a content file compactly for reading: dump.py <file> [item ids...]"""
import json
import sys

d = json.load(open(sys.argv[1]))
ids = set(sys.argv[2:])
items = d.get('items') or d.get('screens') or []


def show(o, ind=0):
    pad = '  ' * ind
    if isinstance(o, dict):
        for k, v in o.items():
            flat = not isinstance(v, (dict, list)) or not v or (
                isinstance(v, list) and all(not isinstance(x, (dict, list)) for x in v))
            if flat:
                print(f"{pad}{k}: {json.dumps(v, ensure_ascii=False)}")
            else:
                print(f"{pad}{k}:")
                show(v, ind + 1)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            if isinstance(v, (dict, list)):
                print(f"{pad}[{i}]")
                show(v, ind + 1)
            else:
                print(f"{pad}- {json.dumps(v, ensure_ascii=False)}")


for it in items:
    if ids and it.get('id') not in ids:
        continue
    print('=' * 70)
    show(it)
