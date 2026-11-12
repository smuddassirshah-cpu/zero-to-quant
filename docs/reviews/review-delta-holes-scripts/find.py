"""Count and show the content strings that match a regex: find.py '<glob under app/content>' '<regex>' [max rows]
python3 docs/reviews/review-delta-holes-scripts/find.py 'courses/quadratics/*.json' '\\b289\\b'"""
import glob
import json
import re
import sys


def strings(o, path=''):
    if isinstance(o, str):
        yield path, o
    elif isinstance(o, dict):
        for k, v in o.items():
            yield from strings(v, f'{path}.{k}' if path else k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            idv = v.get('id') if isinstance(v, dict) else None
            yield from strings(v, f'{path}[{idv or i}]')
    elif isinstance(o, (int, float)) and not isinstance(o, bool):
        yield path, str(o)


pat = re.compile(sys.argv[2])
cap = int(sys.argv[3]) if len(sys.argv) > 3 else 12
n = 0
for f in sorted(glob.glob('app/content/' + sys.argv[1], recursive=True)):
    for path, s in strings(json.load(open(f))):
        m = pat.search(s)
        if m:
            n += 1
            if n <= cap:
                print(f'{f[12:]} {path[:70]}: ...{s[max(0, m.start() - 70):m.end() + 70]}...'.replace('\n', ' '))
print(f'{n} hit(s)')
