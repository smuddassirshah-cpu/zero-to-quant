"""Reader's own freshness pass, vectors problems-1 to -3: grep the rest of the course and the exams for each
problem's story nouns, vectors, matrices and parameters (the set itself excluded, the other sets included).

Usage (repo root): python docs/reviews/review-problems-1.4-a-scripts/fresh.py [-v] [set]
Prints, per key, the files that hit. -v prints the passages (first three a file)."""
import glob
import re
import sys

COURSE = 'vectors'
EXAMS = ['topic-1.4', 'stage-1']
KEYS = {
    'problems-1': [r'robot|charger|warehouse', r'= \(3, 1\)', r'= \(1, 2\)', r'45°', r'benchmark|active weight', r'drone|wind|depot',
                   r'\(12, 16\)|\(0\.6, 0\.8\)', r'scenario|stress|crash|hedged', r'gilt|gold', r'\(0\.6, 0\.3, 0\.1\)', r'central case'],
    'problems-2': [r'italic|slant|font|letter', r'site|survey|borehole|pipe', r'0\.8 *& *-0\.6', r'R\}\^T\\\\mathbf\{R\}', r'loadings?', r'size factor',
                   r'0\.0225', r'exposures?', r'bakery|loaf|loaves|cake|flour|butter|ingredient|recipe', r'Q\}\^T|B\}\^T'],
    'problems-3': [r'goat|pellet|protein|fibre|blend', r'0\.4 *& *0\.1', r'paint|tint|concentrate|litre', r'matrix_rank', r'sensor|pixel|camera|leak|channel',
                   r'0\.8 *& *0\.3', r'Minv|inv\(M\)', r'engrav|laser|dial', r'8 *& *3', r'terms of \$k'],
}
args = [a for a in sys.argv[1:] if a != '-v']
verbose = '-v' in sys.argv
for own, keys in KEYS.items():
    if args and own not in args:
        continue
    files = [f for f in sorted(glob.glob(f'app/content/courses/{COURSE}/*.json') + [f'app/content/exams/{e}.json' for e in EXAMS])
             if not f.endswith(f'{COURSE}/{own}.json') and not f.endswith('course.json')]
    print(f'== {COURSE}/{own}')
    for k in keys:
        hits = {}
        for f in files:
            t = open(f).read()
            ms = list(re.finditer(k, t, re.I))
            if ms:
                hits[f.split('courses/')[-1].split('content/')[-1].replace('.json', '')] = (ms, t)
        print(f'  {k!r}: ' + (', '.join(f'{f}({len(m[0])})' for f, m in hits.items()) or 'none'))
        if verbose:
            for f, (ms, t) in hits.items():
                for m in ms[:3]:
                    print('      ', f, '|', t[max(0, m.start() - 130):m.end() + 130].replace('\n', ' '))
