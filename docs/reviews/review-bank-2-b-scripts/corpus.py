"""Build a one-line-per-task index of the courses, drills and bank part 1, for freshness reading with grep.
Usage: corpus.py <out.tsv> course [course ...]   (also adds content/drills and the part 1 bank files)
Each line: source <tab> prose + question + code names, on one line."""
import json, os, sys, glob, re

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'app', 'content')
out = open(sys.argv[1], 'w')
PART2 = re.compile(r'(statistics|finance|coding)-\d|behavioural-[5-8]')


def one(s):
    return re.sub(r'\s+', ' ', s or '')


def walk(o, src, path=''):
    if isinstance(o, dict):
        if ('question' in o or 'prose' in o) and isinstance(o.get('question', ''), str):
            w = o.get('widget') or {}
            extra = ''
            if isinstance(w, dict):
                extra = ' || ' + one(str(w.get('starter', '')))[:200] + ' ' + one(str(w.get('prompt', '')))[:200]
            out.write(f"{src}{path}\t{one(o.get('prose'))} ?? {one(o.get('question'))}{extra}\n")
        for k, v in o.items():
            walk(v, src, path + ('#' + str(o['id']) if k in ('widget',) and 'id' in o else ''))
    elif isinstance(o, list):
        for x in o:
            walk(x, src, path)


for c in sys.argv[2:]:
    for f in sorted(glob.glob(os.path.join(ROOT, 'courses', c, '*.json'))):
        if f.endswith('course.json'):
            continue
        walk(json.load(open(f)), f'{c}/{os.path.basename(f)[:-5]}')
for f in sorted(glob.glob(os.path.join(ROOT, 'drills', '*.json'))):
    d = json.load(open(f))
    if isinstance(d, dict) and 'brief' in d:
        txt = ' '.join(one(str(d.get(k, ''))) for k in ('name', 'fn', 'pattern', 'brief'))
        out.write(f"drill/{os.path.basename(f)[:-5]}\t{txt[:600]}\n")
    else:
        walk(d, f'drill/{os.path.basename(f)[:-5]}')
for f in sorted(glob.glob(os.path.join(ROOT, 'bank', '*.json'))):
    b = os.path.basename(f)[:-5]
    if PART2.match(b):
        continue
    for it in json.load(open(f))['items']:
        out.write(f"bank/{b}#{it['id']}\t{one(it.get('prose'))} ?? {one(it.get('question'))}\n")
out.close()
