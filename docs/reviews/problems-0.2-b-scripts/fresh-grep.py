"""Reader's own freshness pass: each problem's setting (nouns) and formulae (numbers), searched across its own course
(lessons, fluency, reviews, homework, the other problem sets), the other two 0.2 courses and the exams.
Prints pattern, file, count and the first hit in context. The file under read is skipped.

Usage (repo root): python3 docs/reviews/problems-0.2-b-scripts/fresh-grep.py [--wide]   (--wide searches every course)
"""
import glob
import json
import re
import sys

PAT = {
    ('quadratics', 1): {
        'p-cinema-block': [r'cinema', r'\bseats?\b', r'x\^2 ?\+ ?11x', r'\(x ?\+ ?3\)\(x ?\+ ?8\)', r'\(x ?\+ ?2\)\(x ?\+ ?9\)', r'x\^2 ?\+ ?11x ?\+ ?(24|18)'],
        'p-allotment-plots': [r'allotment', r'\bplots?\b', r'x\^2 ?\+ ?9x ?\+ ?20', r'2x\^2 ?\+ ?15x ?\+ ?28', r'3\(x ?\+ ?4\)', r'\(x ?\+ ?4\)\(x ?\+ ?5\)'],
        'p-steel-plates': [r'steel', r'\bplates?\b', r'\bhole\b', r'36x\^2', r'4x\^2 ?- ?1\b', r'\(6x ?\+ ?5\)', r'\(2x ?\+ ?1\)\(2x ?- ?1\)'],
    },
    ('quadratics', 2): {
        'p-cliff-stone': [r'\bstone\b', r'cliff', r'15 ?\+ ?10t', r'5t\^2', r'\(t ?- ?1\)\^2'],
        'p-bus-chase': [r'\bbus\b', r'runs after', r't\^2 ?- ?6t', r'\(t ?- ?3\)\^2', r'6t ?- ?10', r'x\^2 ?- ?6x ?\+ ?(10|7)\b'],
        'p-can-stack': [r'\bcans?\b', r'triang', r'n\(n ?\+ ?1\)', r'n\^2 ?\+ ?n\b', r'\bstack', r'801', r'x\^2 ?\+ ?x ?- ?(240|200)'],
    },
    ('quadratics', 3): {
        'p-canal-arch': [r'\barch', r'canal', r'bridge', r'barge', r'-0\.2x', r'\(x ?- ?10\)\^2', r'x\(x ?- ?20\)'],
        'p-bike-hire': [r'bike', r'\bhires?\b', r'150 ?- ?5p', r'\(p ?- ?8\)', r'\(p ?- ?19\)', r'1125', r'605'],
        'p-sprinkler-bank': [r'sprinkler', r'\bbank\b', r'3x ?- ?0\.5x\^2', r'2\.5x', r'\bhose\b', r'fountain'],
    },
    ('equations', 4): {
        'p-rowing-current': [r'\brow', r'current', r'river', r'still water', r'launch', r'b ?\+ ?c ?= ?14', r'[a-z] ?\+ ?[a-z] ?= ?14', r'[a-z] ?- ?[a-z] ?= ?10'],
        'p-seedling-trays': [r'seedling', r'\btrays?\b', r'garden centre', r'florist', r'5x ?\+ ?3y', r'x ?\+ ?8\b', r'= ?168'],
        'p-remote-cars': [r'remote', r'[Cc]ar A', r'= ?7t', r't\^2 ?= ?7t', r'marker post', r'x\^2 ?= ?7x', r'speeds up'],
        'p-salt-solutions': [r'\bsalt', r'solution of|% solution|% salt', r'0\.15x', r'\bmix', r'x ?\+ ?y ?= ?500', r'technician', r'25%'],
    },
}
wide = '--wide' in sys.argv
exams = glob.glob('app/content/exams/*.json')


def texts(o):
    if isinstance(o, str):
        yield o
    elif isinstance(o, dict):
        for v in o.values():
            yield from texts(v)
    elif isinstance(o, list):
        for v in o:
            yield from texts(v)


for (course, n), items in PAT.items():
    own = f'app/content/courses/{course}/problems-{n}.json'
    files = sorted(glob.glob('app/content/courses/*/*.json') if wide else
                   [f for c in ('equations', 'functions', 'quadratics') for f in glob.glob(f'app/content/courses/{c}/*.json')]) + exams
    blobs = {f: ' \n '.join(texts(json.load(open(f)))) for f in files if f != own and not f.endswith('course.json')}
    for item, pats in items.items():
        print(f'\n== {course} {n} {item}')
        for p in pats:
            rx = re.compile(p)
            hits = []
            for f, blob in blobs.items():
                ms = list(rx.finditer(blob))
                if ms:
                    m = ms[0]
                    ctx = blob[max(0, m.start() - 60):m.end() + 60].replace('\n', ' ')
                    hits.append((f.replace('app/content/', ''), len(ms), ctx))
            print(f'  /{p}/  {len(hits)} file(s)')
            for f, k, ctx in hits[:12]:
                print(f'      {f} x{k}: ...{ctx}...')
