"""Count, per lesson of a level, how often each idea a problem set leans on appears.

A zero across a whole level means the set may use an idea the level never taught;
each such row was then read by hand (see the review). Run from the repo root.
"""
import glob
import json
import os
import re

BASE = 'app/content/courses'
LEVELS = {
    'limits L1': ('limits', [1, 2, 3, 4], [
        r'squeez|sandwich|trapped', r'\\sin', r'asymptote', r'hole', r'jump',
        r'leading coefficient|highest power', r'table']),
    'limits L2': ('limits', [5, 6, 7, 8], [
        r'corner', r'secant', r'difference quotient', r'\^\{-1\}|negative power',
        r'continuous', r'slope graph', r'average rate']),
    'limits L3': ('limits', [9, 10, 11, 12], [
        r'implicit', r'\\ln y', r'growth rate', r'e\^\{-?[0-9.k]+ ?[tx]\}', r'\\cos',
        r'quotient rule', r'product rule', r'factoris']),
    'integrals L1': ('integrals', [1, 2, 3, 4], [
        r'midpoint', r'gap', r'\(2n ?\+ ?1\)', r'int_[a-z0-9]\^0|revers|backwards|swap',
        r'net ', r'running total', r'triangle']),
    'integrals L2': ('integrals', [5, 6, 7, 8], [
        r'e\^\{-?[0-9.k]+ ?[tx]\}', r'local max|maximum|peak', r'accumulation',
        r'top minus bottom', r'cross', r'\+ ?C']),
    'integrals L3': ('integrals', [9, 10, 11, 12, 13], [
        r'density', r'median', r'E\[', r'E\[g|curved|bends|Jensen', r'trapezium', r'h\^2',
        r'uniform', r'tail', r'e\^\{-x\}', r'\\ln x', r'average value|average']),
}
for name, (course, nums, pats) in LEVELS.items():
    print(f'\n== {name}')
    files = []
    for n in nums:
        files += glob.glob(f'{BASE}/{course}/l{n}-*.json')
    texts = {os.path.basename(f)[:-5].split('-')[0]: json.dumps(json.load(open(f)), ensure_ascii=False)
             for f in files}
    for p in pats:
        row = ' '.join(f'{k}:{len(re.findall(p, t, flags=re.I))}' for k, t in texts.items())
        print(f'  {row}   <- {p}')
