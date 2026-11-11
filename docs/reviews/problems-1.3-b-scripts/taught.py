"""Count, per lesson of a level, how often each idea a problem set leans on appears.

A zero across a whole level means the set may use an idea the level never taught; each such row was then read by hand
(see the review). With --show <course> <lesson-number> <regex> it prints the passages that match. Run from the repo root.
"""
import glob
import json
import os
import re
import sys

BASE = 'app/content/courses'
LEVELS = {
    'taylor L1': ('taylor', [1, 2, 3, 4], [
        r"f''\(a\)|\\tfrac12 f''|\\frac\{1\}\{2\} ?f''", r'h\^2', r'Newton', r'DV01|basis point', r'modified duration|D = -', r'above (its|the|each|every) tangent|lies above|bends up|convex',
        r'overshoot|falls short|too soon|same side', r'x_\{n ?\+ ?1\}|x_1', r'loan|repay', r'cube root|\\sqrt\[3\]', r'digits? (roughly )?doubl']),
    'taylor L2': ('taylor', [5, 6, 7, 8], [
        r'k!', r'\(x - a\)\^|about \$?a', r'f\'\'\'', r'convexity', r"P''", r'-1 < x', r'geometric', r'\\ln\(1 \+ x\)', r'term by term|differentiat\w+ the series',
        r'\\Delta y\)\^2', r'centre', r'works (only )?for|converges for|fails']),
    'taylor L3': ('taylor', [9, 10, 11, 12], [
        r'ratio test', r'compar', r'radius', r'Lagrange', r'alternat', r'first (term )?(left out|omitted|unused|missing)', r'endpoint|at the ends|each end|both ends',
        r'\{1\}\{n\^2\}', r'log return', r'absolute|sizes', r'tail', r'M ?\\|largest', r'c_\{n ?\+ ?1\}']),
    'multivar L1': ('multivar', [1, 2, 3, 4], [
        r'contour', r'ellipse', r'f_\{xy\}', r'f_\{yx\}', r'chain rule', r"x'\(t\)|\\frac\{dx\}\{dt\}", r'along a contour|stays? (fixed|constant|level)', r'delta|exchange|currency',
        r'slope changes|how the .*slope']),
    'multivar L2': ('multivar', [5, 6, 7, 8], [
        r'unit (arrow|vector)', r'\\cos', r'right angles|perpendicular', r'tangent plane', r'square of|quarter|h\^2', r'step size', r'zigzag|overshoot', r'1 - 2s|multipli',
        r'degrees|\^\\circ', r'steepest']),
    'multivar L3': ('multivar', [9, 10, 11, 12], [
        r'saddle', r'pit', r'D = ', r'\\lambda', r'per unit|shadow|relax|extra', r'2\\sigma|twice', r'correlation|\\rho', r'budget', r'stationary', r'No verdict|silent|says nothing|D = 0']),
}
if '--show' in sys.argv:
    course, num, pat = sys.argv[sys.argv.index('--show') + 1:][:3]
    for f in glob.glob(f'{BASE}/{course}/l{num}-*.json'):
        def walk(o, path=''):
            if isinstance(o, dict):
                for kk, v in o.items():
                    walk(v, path + '.' + kk)
            elif isinstance(o, list):
                for i, v in enumerate(o):
                    walk(v, f'{path}[{i}]')
            elif isinstance(o, str) and re.search(pat, o, flags=re.I):
                print(f'{os.path.basename(f)} {path[:60]}: {o[:420]}')
        walk(json.load(open(f)))
    sys.exit(0)
for name, (course, nums, pats) in LEVELS.items():
    print(f'\n== {name}')
    files = []
    for n in nums:
        files += glob.glob(f'{BASE}/{course}/l{n}-*.json')
    texts = {os.path.basename(f)[:-5].split('-')[0]: json.dumps(json.load(open(f)), ensure_ascii=False).replace('\\\\', '\\')
             for f in sorted(files, key=lambda s: int(re.search(r'/l(\d+)-', s).group(1)))}
    for p in pats:
        row = ' '.join(f'{k}:{len(re.findall(p, t, flags=re.I))}' for k, t in texts.items())
        print(f'  {row}   <- {p}')
