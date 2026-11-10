"""Index rows against files, and the other drills a cpp drill could repeat.

  python repeats.py
Prints: every index field that differs from its drill file; the other C++ drills (ci-cpp-, sample-cpp-)
with the head of their brief; and Python drills (py-, dsa-, ci-) whose name shares a task word with a
cpp drill, for a reader to judge.
"""
import glob, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(HERE, '..', '..', '..', 'app', 'content', 'drills')
WORDS = ('trim', 'split', 'pence', 'rank', 'tick', 'clip', 'high-water', 'water', 'mover', 'csv', 'rise', 'streak', 'run of',
         'cross', 'session', 'midnight', 'fee', 'curve', 'discount', 'small', 'range', 'low and high', 'bermudan', 'digital',
         'cash', 'running', 'variance', 'band', 'payoff', 'limit', 'fills')


def main():
    idx = json.load(open(os.path.join(D, 'index.json')))
    rows = idx if isinstance(idx, list) else idx.get('drills', idx)
    by = {r['id']: r for r in rows}
    diffs = 0
    files = {}
    for f in sorted(glob.glob(os.path.join(D, '*.json'))):
        if f.endswith('index.json'):
            continue
        d = json.load(open(f))
        files[d['id']] = d
    for i, d in files.items():
        if d.get('pack') == 'cpp':
            r = by.get(i)
            if r is None:
                print('NO INDEX ROW', i)
                diffs += 1
                continue
            for k in r:
                if k in d and r[k] != d[k]:
                    print('ROW DIFFERS', i, k, r[k], d[k])
                    diffs += 1
    print('index rows checked, differences:', diffs, '| row keys:', sorted(rows[-1].keys()))
    for i, d in files.items():
        if d.get('pack') != 'cpp' and (d.get('language') == 'cpp' or d.get('course') in ('cpp', 'cpp-pricing')):
            print('OTHER C++', i, '|', d['name'], '|', d['brief'][:160].replace('\n', ' '))
    for i, d in files.items():
        if d.get('pack') == 'cpp' or d.get('language') == 'cpp':
            continue
        n = d['name'].lower()
        if any(w in n for w in WORDS):
            print('PYTHON', i, '|', d['name'], '|', d['brief'][:200].replace('\n', ' '))


if __name__ == '__main__':
    main()
