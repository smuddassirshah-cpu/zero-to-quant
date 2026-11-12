"""Second read, eigen problems-1 to -3: freshness aids for reading by hand.

Corpus: every eigen file but the problem sets, the other 1.4 courses (vectors, elimination, least-squares: every file, problem
sets included), exam topic-1.4, the stage exams and the mock papers. Three searches:
  (1) every matrix of each problem, as its rows with spacing removed, and every vector with three or more digits;
  (2) the same matrix up to a row or column swap, a transpose or a common factor (2 by 2 and 3 by 3 with whole or decimal
      entries), found by reading every pmatrix of the corpus: `fresh-check` cannot see these;
  (3) --nouns: the story nouns; --nums: the key numbers of each problem.
Small vectors recur by chance, so the output is a reading list, not a verdict.

Run from the repo root:  python3 docs/reviews/review-problems-1.4-c-scripts/fresh.py [--nouns] [--nums]
"""
import glob
import itertools
import json
import re
import sys
from fractions import Fraction as Fr

NOUNS = ['warp', 'sketch', 'drawing', 'garden', 'path', 'slab', 'pave', 'tiling', 'tile', 'domino', 'bike', 'station', 'hill', 'river',
         'frog', 'lily', 'pad', 'lazy', 'pond', 'oval', 'gauge', 'thermometer', 'tank', 'branch', 'shop', 'crab', 'claw', 'shell',
         'weather', 'anomal', 'site', 'temperature']
NUMS = {'p-sketch-warp': ['(50, 17)', '(5, 2)'], 'p-garden-path': ['35839', '59049', 't_{n+1}', '6t_'], 'p-hill-bikes': ['0.55', '321', '0.15'],
        'p-lazy-frog': ['0.3125', '(1, -2, 1)', '(1, 0, -1)'], 'p-oval-pond': ['5x^2', '4xy', '18.85', '6\\pi'], 'p-river-gauges': ['0.28', '1.28', '0.8 &'],
        'p-tank-thermometers': ['1.76', '(0.5, 0.3, 0.2)', '\\tfrac53'], 'p-branch-sales': ['0.862', '50/58', '(0.8, 0.6, 0)'],
        'p-crab-sizes': ['182.5', '62.5', '15625', '(0.6, 0.8)'], 'p-site-anomalies': ['1170', '[30, 15, 6, 3]', '0.962', '37.5']}


def norm(s):
    s = re.sub(r'\\(?:left|right|,|;|!|quad|qquad)', '', s)
    return re.sub(r'\s+', '', s)


def corpus():
    files = [f for f in glob.glob('app/content/courses/eigen/*.json') if '/problems-' not in f and not f.endswith('course.json')]
    for c in ('vectors', 'elimination', 'least-squares'):
        files += [f for f in glob.glob(f'app/content/courses/{c}/*.json') if not f.endswith('course.json')]
    files += ['app/content/exams/topic-1.4.json'] + glob.glob('app/content/exams/stage-*.json') + glob.glob('app/content/exams/mock-*.json')
    out = {}
    for f in sorted(set(files)):
        d = json.load(open(f))
        units = d.get('screens') or d.get('items') or d.get('parts') or []
        if not units:
            units = [d]
        for i, u in enumerate(units):
            out[(f.split('courses/')[-1].split('exams/')[-1], i, u.get('id', '') if isinstance(u, dict) else '')] = json.dumps(u, ensure_ascii=False).replace('\\\\', '\\')
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
    return found


def matrices(text):
    """every pmatrix with numeric entries, as a tuple of tuples of Fractions"""
    out = []
    for m in re.finditer(r'\\begin\{pmatrix\}(.*?)\\end\{pmatrix\}', text):
        try:
            rows = tuple(tuple(Fr(norm(e).replace('−', '-')) for e in r.split('&')) for r in m.group(1).split('\\\\') if r.strip())
        except (ValueError, ZeroDivisionError):
            continue
        if len(rows) >= 2 and len({len(r) for r in rows}) == 1 and len(rows[0]) >= 2:
            out.append(rows)
    return out


def canon(mat):
    """a key shared by a matrix, its transpose, its row and column permutations and its positive multiples"""
    best = None
    for M in (mat, tuple(zip(*mat))):
        for rp in itertools.permutations(range(len(M))):
            for cp in itertools.permutations(range(len(M[0]))):
                flat = [M[i][j] for i in rp for j in cp]
                lead = next((abs(v) for v in flat if v != 0), None)
                if lead is None:
                    continue
                k = tuple(v / lead for v in flat) + (len(M), len(M[0]))
                if best is None or k < best:
                    best = k
    return best


C = corpus()
CN = {k: norm(v) for k, v in C.items()}
name = lambda k: k[0] + (':' + k[2] if k[2] else f'[{k[1]}]')
mode = 'nouns' if '--nouns' in sys.argv else 'nums' if '--nums' in sys.argv else 'lit'
CM = {}
if mode == 'lit':
    for k, v in C.items():
        for m in matrices(v):
            if len(m) <= 3 and len(m[0]) <= 3:
                CM.setdefault(canon(m), set()).add(name(k))
for n in (1, 2, 3):
    d = json.load(open(f'app/content/courses/eigen/problems-{n}.json'))
    for it in d['items']:
        text = it['prose'] + ' ' + ' '.join(p['question'] for p in it['parts'])
        print(f'== problems-{n} {it["id"]}')
        if mode == 'nouns':
            for w in NOUNS:
                if re.search(r'\b' + w, text, re.I):
                    hits = sorted({name(k) for k, v in C.items() if re.search(r'\b' + w, v, re.I)})
                    if hits:
                        print(f'   noun {w!r}: {len(hits)} units: {", ".join(hits[:8])}{" ..." if len(hits) > 8 else ""}')
            continue
        if mode == 'nums':
            for s in NUMS[it['id']]:
                hits = sorted({name(k) for k, v in CN.items() if norm(s) in v})
                print(f'   {s}: {len(hits)} units{": " + ", ".join(hits[:8]) if hits else ""}{" ..." if len(hits) > 8 else ""}')
            continue
        for lit in sorted(literals(text)):
            key = norm(lit)
            if len(re.findall(r'-?\d', key)) < 3 and '&' not in key:
                continue
            hits = sorted({name(k) for k, v in CN.items() if key in v})
            if hits:
                print(f'   {lit}: {", ".join(hits[:7])}{" ..." if len(hits) > 7 else ""}')
        for m in matrices(text):
            hits = sorted(CM.get(canon(m), ()))
            if hits:
                print(f'   matrix {[[str(e) for e in r] for r in m]} up to swaps, transpose and scale: {", ".join(hits[:7])}{" ..." if len(hits) > 7 else ""}')
