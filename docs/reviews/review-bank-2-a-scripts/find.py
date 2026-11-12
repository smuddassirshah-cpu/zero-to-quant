"""Freshness search. Usage: find.py '<regex>' [<regex2> ...]   (all regexes must match the same item, case-insensitive)
Searches items (screens, questions, set items) of the courses and exams named below and part 1 of the bank,
and prints file, item id and a snippet around the first match."""
import json, os, re, sys, glob
HERE = os.path.dirname(os.path.abspath(__file__))
C = os.path.join(HERE, '..', '..', '..', 'app', 'content')
COURSES = ['estimation', 'testing', 'regression', 'arma', 'garch', 'stat-models', 'recruiting', 'research-int', 'coint', 'limits-thm']
files = []
for c in COURSES: files += sorted(glob.glob(os.path.join(C, 'courses', c, '*.json')))
files += sorted(glob.glob(os.path.join(C, 'exams', '*.json')))
P1 = re.compile(r'(probability|brainteasers|mental|market-making|behavioural)-[1-4]\.json$')
files += [f for f in sorted(glob.glob(os.path.join(C, 'bank', '*.json'))) if P1.search(f)]
if os.environ.get('ALSO_BANK2'):
    files += [f for f in sorted(glob.glob(os.path.join(C, 'bank', '*.json'))) if re.search(r'(statistics-\d|behavioural-[5-8]|finance-\d|coding-\d)\.json$', f)]
rx = [re.compile(a, re.I) for a in sys.argv[1:]]
def text(o):
    if isinstance(o, str): return o
    if isinstance(o, list): return ' '.join(text(x) for x in o)
    if isinstance(o, dict): return ' '.join(text(v) for k, v in o.items() if k not in ('id', 'skills', 'tags', 'requires'))
    return str(o) if isinstance(o, (int, float)) else ''
def units(o, path=''):
    """yield (id, node) for the smallest dicts that have an id and a question, prompt or body"""
    if isinstance(o, dict):
        kids = False
        for k, v in o.items():
            if isinstance(v, (list, dict)):
                for u in units(v, path): kids = True; yield u
        if not kids and ('id' in o or 'question' in o): yield (o.get('id', '?'), o)
    elif isinstance(o, list):
        for x in o:
            for u in units(x, path): yield u
n = 0
for f in files:
    try: d = json.load(open(f))
    except Exception: continue
    items = []
    for k, v in d.items():
        if isinstance(v, list) and v and isinstance(v[0], dict): items += v
        elif isinstance(v, dict): items.append(v)
    if not items:
        items = [d]
    for it in items:
        t = text(it)
        if all(r.search(t) for r in rx):
            m = rx[0].search(t); s = max(0, m.start() - 130)
            print('%s | %s | ...%s...' % (os.path.relpath(f, C), it.get('id', '?') if isinstance(it, dict) else '?', t[s:m.end() + 170].replace('\n', ' ')))
            n += 1
            if n > 25: print('(more)'); sys.exit(0)
print(n, 'hits')
