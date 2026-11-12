"""Second read, elimination and least-squares problems-1 to -3: freshness aids for reading by hand.

For each problem: (1) every vector `(a, b, ...)` and every matrix (as its rows) in the prose and the questions,
searched, with spaces and LaTeX spacing removed, in the lessons, reviews, homework and fluency sets of both courses,
in every `vectors` file, in the `regression` problem sets and in exams `topic-1.4` and `stage-1`; (2) story nouns.
Small vectors recur by chance, so the output is a reading list, not a verdict.

Run from the repo root:  python3 docs/reviews/review-problems-1.4-b-scripts/fresh.py [--nouns]
"""
import glob
import json
import re
import sys

NOUNS = ['florist', 'bouquet', 'courier', 'roaster', 'coffee', 'ethanol', 'chemist', 'gantry', 'printer', 'motor', 'futures',
         'butterfly', 'spread', 'coin', 'hopper', 'vinyl', 'dial', 'logo', 'deform', 'football', 'draw', 'bet', 'drone',
         'station', 'code', 'crystal', 'rotor', 'pixel', 'grey', 'power line', 'cable', 'solar', 'panel', 'dye',
         'wavelength', 'runner', 'heart', 'ramp', 'ball', 'gas', 'temperature', 'hub']


def norm(s):
    s = re.sub(r'\\(?:left|right|,|;|!|quad|qquad)', '', s)
    return re.sub(r'\s+', '', s)


def corpus():
    files = []
    for c in ('elimination', 'least-squares'):
        files += [f for f in glob.glob(f'app/content/courses/{c}/*.json') if '/problems-' not in f and not f.endswith('course.json')]
    files += glob.glob('app/content/courses/vectors/*.json')
    files += glob.glob('app/content/courses/regression/problems-*.json')
    files += ['app/content/exams/topic-1.4.json', 'app/content/exams/stage-1.json']
    out = {}
    for f in sorted(set(files)):
        d = json.load(open(f))
        units = d.get('screens') or d.get('items') or d.get('parts') or []
        for i, u in enumerate(units):
            out[(f.split('courses/')[-1].split('exams/')[-1], i, u.get('id', '') if isinstance(u, dict) else '')] = json.dumps(u, ensure_ascii=False)
    return out


def literals(text):
    found = set()
    for m in re.finditer(r'\(([^()$]*?,[^()$]*?)\)', text):
        body = m.group(1)
        if re.fullmatch(r'[-\d.,\s\\a-z{}/]+', body) and re.search(r'\d', body) and len(body.split(',')) >= 2:
            found.add('(' + norm(body) + ')')
    for m in re.finditer(r'\\begin\{pmatrix\}(.*?)\\end\{pmatrix\}', text):
        rows = [norm(r) for r in m.group(1).split('\\\\')]
        if len(rows) >= 2:
            found.add('\\\\'.join(rows))
            for r in rows:
                if r.count('&') >= 2:
                    found.add(r)
    for m in re.finditer(r'\\begin\{array\}\{[^}]*\}(.*?)\\end\{array\}', text):
        for r in m.group(1).split('\\\\'):
            if r.count('&') >= 2:
                found.add(norm(r))
    return found


C = corpus()
CN = {k: norm(v.encode().decode('unicode_escape', 'ignore') if False else v.replace('\\\\', '\\')) for k, v in C.items()}
nouns = '--nouns' in sys.argv
for course in ('elimination', 'least-squares'):
    for n in (1, 2, 3):
        d = json.load(open(f'app/content/courses/{course}/problems-{n}.json'))
        for it in d['items']:
            text = it['prose'] + ' ' + ' '.join(p['question'] for p in it['parts'])
            print(f'== {course} problems-{n} {it["id"]}')
            if nouns:
                for w in NOUNS:
                    if re.search(r'\b' + w, text, re.I):
                        hits = sorted({k[0] + (':' + k[2] if k[2] else f'[{k[1]}]') for k, v in C.items() if re.search(r'\b' + w, v, re.I)})
                        if hits:
                            print(f'   noun {w!r}: {len(hits)} units: {", ".join(hits[:8])}{" ..." if len(hits) > 8 else ""}')
                continue
            for lit in sorted(literals(text.replace('\\\\', '\\\\'))):
                key = norm(lit)
                if len(re.findall(r'-?\d', key)) < 3 and '&' not in key:
                    continue
                hits = sorted({k[0] + (':' + k[2] if k[2] else f'[{k[1]}]') for k, v in CN.items() if key in v})
                if hits:
                    print(f'   {lit}: {", ".join(hits[:7])}{" ..." if len(hits) > 7 else ""}')
