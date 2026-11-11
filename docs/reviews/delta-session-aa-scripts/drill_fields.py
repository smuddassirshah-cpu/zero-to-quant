"""Print chosen fields of drills in full: drill_fields.py field,field,... <drill id> ..."""
import json
import sys

fields = sys.argv[1].split(',')
for i in sys.argv[2:]:
    d = json.load(open(f'app/content/drills/{i}.json'))
    print('=' * 20, i)
    for k in fields:
        if k not in d:
            continue
        v = d[k]
        if isinstance(v, list):
            print(f'{k}:')
            for n, x in enumerate(v):
                print(f'  [{n}] ' + (x if isinstance(x, str) else json.dumps(x, ensure_ascii=False)))
        else:
            print(f'{k}: {v}')
