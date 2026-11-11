"""Freshness of the four re-authored items: search every JSON file of the
course (lessons, quizzes, reviews, homework, other problem sets) and every
exam for the item's formula, numbers and nouns. Prints each hit outside the
item itself, cut to a short window, for a judgement by eye.

Run from the repo root: python fresh.py
"""
import glob
import json
import re

ITEMS = {
    ('integrals', 'problems-1', 'p-falling-parabola'): [
        r'12\s*-\s*3x\^2', r'3x\^2', r'falling (curve|parabola)', r'gap rule', r'18\.75', r'12\.75',
        r'\\tfrac\{2k\}\{n\}', r'n\(n\s*\+\s*1\)\(2n\s*\+\s*1\)',
    ],
    ('limits', 'problems-3', 'p-relative-strength'): [
        r'30e\^', r'1500e\^', r'e\^\{0\.07', r'e\^\{0\.05t', r'\bindex\b', r'\bratio\b.{0,60}(share|index|price)',
        r'relative strength', r'0\.0004',
    ],
    ('taylor', 'problems-1', 'p-cube-root-27'): [
        r'sqrt\[4\]', r'x\^\{1/4\}', r'x\^\{\\t?frac\{?1\}?\{?4', r'fourth root', r'16\.32', r'\b2\.01\b',
        r'x\^\{-3/4\}', r'a = 16\b',
    ],
    ('multivar', 'problems-3', 'p-min-variance-pair'): [
        r'40%.{0,40}25%', r'25%.{0,40}40%', r'correlation 0\.3\b', r'\\rho = 0\.3\b', r'0\.16w', r'0\.0625',
        r'minimum[- ]variance', r'0\.056\b', r'0\.112\b', r'102%', r'1\.02\b',
    ],
}


def strings(o, path=''):
    if isinstance(o, str):
        yield path, o
    elif isinstance(o, dict):
        for k, v in o.items():
            yield from strings(v, f'{path}.{k}')
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from strings(v, f'{path}[{i}]')


for (course, pset, iid), pats in ITEMS.items():
    print('=' * 20, course, pset, iid)
    files = sorted(glob.glob(f'app/content/courses/{course}/*.json')) + sorted(glob.glob('app/content/exams/*.json'))
    for pat in pats:
        hits = []
        for f in files:
            d = json.load(open(f))
            if f.endswith(f'{course}/{pset}.json'):
                d = {'items': [i for i in d['items'] if i['id'] != iid]}
            for path, s in strings(d):
                for m in re.finditer(pat, s):
                    a, b = max(0, m.start() - 70), min(len(s), m.end() + 70)
                    hits.append((f.split('content/')[1], path, s[a:b].replace('\n', ' ')))
        seen = set()
        print(f'-- {pat}: {len(hits)} hits')
        for f, path, s in hits:
            if (f, s) in seen:
                continue
            seen.add((f, s))
            if len(seen) > 8:
                print('   ...')
                break
            print(f'   {f} {path[:60]} | {s}')
