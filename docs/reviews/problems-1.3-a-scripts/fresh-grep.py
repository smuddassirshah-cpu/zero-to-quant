"""Freshness by key formula and noun: where else in app/content does each problem's setup appear?

fresh-check.mjs compares word runs; this looks for the function or story itself. Run from the repo root.
Prints, per key, the files other than the six sets under review that hold it (course lessons, reviews, homework, exams).
"""
import glob
import json
import re

KEYS = {
    'limits': [r'2 \+ 0\.5x', r'commission', r'2x\^2 - 2x - 12', r'x\^2 - 9\b', r'ax\^2 \+ bx', r'\\sin t\}\{t\}', r'\\sin x\}\{x\}',
               r'3t\^2 \+ 4t', r'2t\^3 - 9t\^2 \+ 12t', r'0\.5q\^2', r'perpetuity', r'\\dfrac\{5\}\{r\}', r'e\^\{0\.06t\}',
               r'\(50 - p\)', r'subscriber', r'market maker', r'x\^\{0\.8\}', r'therm', r'seasonal', r'penalty', r'index'],
    'integrals': [r'9 - x\^2', r'12 - 4t', r'subscription', r't\^2 - 4\b', r't\^2 - 6t \+ 8', r'8e\^\{-0\.5t\}', r'turnover',
                  r'2x\^2', r'x \+ 3\b', r'12t - 3t\^2', r'ETF', r'\(1 \+ x\^2\)\^2', r'x\\,e\^\{-x\}|x e\^\{-x\}|xe\^\{-x\}',
                  r'time to fill|unfilled', r'\\ln x\\,dx', r'log return', r'e\^\{-t\^2/8\}', r'signal', r'median', r'\[0\.5, 1\.5\]'],
}
UNDER = {f'app/content/courses/{c}/problems-{n}.json' for c in KEYS for n in (1, 2, 3)}
files = [f for f in glob.glob('app/content/**/*.json', recursive=True) if f not in UNDER and not f.endswith('manifest.json')]
texts = {}
for f in files:
    try:
        texts[f] = json.dumps(json.load(open(f)), ensure_ascii=False).replace('\\\\', '\\')
    except Exception:
        pass
for course, keys in KEYS.items():
    print(f'== {course}')
    for kx in keys:
        hits = {}
        for f, tx in texts.items():
            c = len(re.findall(kx, tx))
            if c and (f'/courses/{course}/' in f or '/exams/' in f):
                hits[f.replace('app/content/', '').replace('courses/', '')] = c
        print(f'  {kx}: ' + (', '.join(f'{a}:{b_}' for a, b_ in sorted(hits.items())[:9]) or 'none'))
