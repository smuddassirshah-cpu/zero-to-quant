"""Reader's own freshness pass: for each problem, grep the rest of its course (and the exams) for its key nouns, functions and numbers.

Usage (repo root): python docs/reviews/problems-1.3-c-scripts/fresh-grep.py [-v]
Prints, per key, the files that hit (the set itself excluded). -v prints the passages.
"""
import glob
import re
import sys

KEYS = {
    ('limits', 'problems-4'): [r'half-spread', r'900s', r'\(2\s*\+\s*s\)', r'60\\\\ln', r'signal', r'barbell', r'zero-coupon', r'e\^\{-8u\}',
                               r'annuity', r'1 - e\^\{-10r\}', r'e\^\{-10r\}', r'spread evenly'],
    ('limits', 'problems-5'): [r'camera', r'arctan\\\\left\(\\\\d?frac\{x\}\{30\}', r'9e\^\{-t\}', r'1000 - N', r'adoption|users',
                               r'frac\{q\}\{500\}', r'price impact|impact', r'radar|lighthouse|searchlight'],
    ('integrals', 'problems-4'): [r'kernel', r'\(2 \+ \\\\sqrt\{t\}\)', r'\(1 \+ u\)\(2 \+ u\)', r'horn|trumpet|flare', r'\(1 - x\^2\)\^\{-1/4\}',
                                  r'\(x \+ 1\)\(x \+ 2\)', r'dish|spindle', r'seal|torus|doughnut|\bring\b', r'\(x - 3\)\^2', r'6\\\\pi\^2',
                                  r'pi\^2\}\{2\}', r'2\\\\ln 2'],
    ('multivar', 'problems-4'): [r'xy\^2', r'sprinkler|garden', r'9 - r\^2|9r - r\^3', r'drone|landing', r'/8\}', r'8\\\\pi', r'quarter disc',
                                 r'Y \\\\le 2X', r'litre'],
    ('multivar', 'problems-5'): [r'3x \+ 2y \+ z', r'strateg', r'tent|dome', r'x\^2 \+ 4y\^2', r'x = 2u', r'triangular|field', r'x = 4u',
                                 r'64\}\{27\}', r'no share|short'],
}
verbose = '-v' in sys.argv
for (course, own), keys in KEYS.items():
    files = [f for f in sorted(glob.glob(f'app/content/courses/{course}/*.json') + glob.glob('app/content/exams/*.json'))
             if not f.endswith(f'{course}/{own}.json') and not f.endswith('course.json')]
    print(f'== {course}/{own}')
    for k in keys:
        hits = {}
        for f in files:
            t = open(f).read()
            ms = list(re.finditer(k, t, re.I))
            if ms:
                hits[f.split('courses/')[-1].split('content/')[-1]] = ms, t
        print(f'  {k!r}: ' + (', '.join(f'{f}({len(m[0])})' for f, m in hits.items()) or 'none'))
        if verbose:
            for f, (ms, t) in hits.items():
                for m in ms[:2]:
                    print('      ', f, '|', t[max(0, m.start() - 120):m.end() + 120].replace('\n', ' '))
