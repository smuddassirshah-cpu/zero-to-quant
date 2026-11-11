"""Where is each idea a set leans on taught? Counts regex hits per lesson file of the level (and named earlier lessons).

Usage (repo root): python docs/reviews/problems-1.3-c-scripts/taught.py
                   python docs/reviews/problems-1.3-c-scripts/taught.py --show COURSE LESSONPREFIX PATTERN   (prints each passage)
"""
import glob
import re
import sys

BASE = 'app/content/courses/'
Q = {
    ('limits', 'l13 l14 l15 l16'): [r'\\infty\}\{\\infty', r"second derivative|''", r'L.H.pital', r'again|twice|second time',
                                    r'closed interval|endpoint|\bends?\b', r'\\Delta|tangent', r'convex', r'quotient rule'],
    ('limits', 'l17 l18 l19 l20 l11'): [r'arctan', r'arcsin', r'mean value', r'inflection', r'concave|bends', r'inverse', r'logistic',
                                        r'at least|at most|bound|cannot exceed'],
    ('integrals', 'l14 l15 l16 l17 l11 l9'): [r'cover', r'divide first|long division|same degree|equal degree|divide', r'shell', r'disc',
                                              r'comparison|below a convergent|bound', r'arcsin', r'\\sin\s*\\theta', r'\\cos 2', r'\bodd\b',
                                              r'torus|ring|doughnut', r'1\s*-\s*p', r'\)\^2\}'],
    ('multivar', 'l13 l14 l15 l16'): [r'density', r'sqrt\{?\\pi', r'sigma', r'polar', r'r\\,dr', r'product|separ', r'strip', r'litre', r'P\('],
    ('multivar', 'l17 l18 l19 l20'): [r'iiint|triple', r'Jacobian|area factor', r'x_u', r'\\mu', r'\bedges?\b', r'corner', r'closed', r'average',
                                      r'short', r'ellipse', r'triangle'],
}
if '--show' in sys.argv:
    c, pre, pat = sys.argv[sys.argv.index('--show') + 1:][:3]
    for f in sorted(glob.glob(f'{BASE}{c}/{pre}*.json')):
        t = open(f).read()
        for m in re.finditer(pat, t, re.I):
            print(f.split('/')[-1], '...', t[max(0, m.start() - 160):m.end() + 200].replace('\n', ' '), '\n')
    sys.exit()
for (c, ls), pats in Q.items():
    print(f'== {c} {ls}')
    for p in pats:
        row = []
        for l in ls.split():
            n = sum(len(re.findall(p, open(f).read(), re.I)) for f in glob.glob(f'{BASE}{c}/{l}-*.json'))
            row.append(f'{l}:{n}')
        print('  ', ' '.join(row), ' <=', p)
