"""Where does the course teach an idea? Prints short contexts per level.
Run from the repo root:
python3 docs/reviews/review-problems-number-sense-1-3-scripts/taught.py LEVELS REGEX [max]
LEVELS is e.g. 1 or 12 or 123 (lessons of those levels, with reviews and homework)."""
import glob
import json
import re
import sys

BASE = 'app/content/courses/number-sense/'
LESSONS = {1: range(1, 6), 2: range(6, 10), 3: range(10, 15), 4: range(15, 20)}
levels = [int(c) for c in sys.argv[1]]
rx = re.compile(sys.argv[2], re.I)
cap = int(sys.argv[3]) if len(sys.argv) > 3 else 5


def strings(o, path=''):
    if isinstance(o, str):
        yield path, o
    elif isinstance(o, dict):
        for k, v in o.items():
            yield from strings(v, path + '.' + k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from strings(v, f'{path}[{i}]')


for lv in levels:
    files = []
    for n in LESSONS[lv]:
        files += sorted(glob.glob(f'{BASE}l{n}-*.json'))
    files += [f'{BASE}review-{lv}.json', f'{BASE}homework-{lv}.json']
    for f in files:
        d = json.load(open(f))
        hits = [(p, s) for p, s in strings(d) if rx.search(s)]
        print(f'L{lv} {f[len(BASE):]}: {len(hits)} hit(s)')
        for p, s in hits[:cap]:
            m = rx.search(s)
            a, b = max(0, m.start() - 70), min(len(s), m.end() + 70)
            print('    ', p[:45], '|', s[a:b].replace('\n', ' '))
