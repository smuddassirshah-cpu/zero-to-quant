"""Reader's own freshness pass, testing problems-1 to -3: grep the rest of the course and the exams for each
problem's story nouns, data and parameters (the set itself excluded, the other sets included).

Usage (repo root): python docs/reviews/review-problems-1.6-b-scripts/fresh.py [-v] [set]
Prints, per key, the files that hit. -v prints the passages (first three a file)."""
import glob
import re
import sys

COURSE = 'testing'
EXAMS = ['topic-1.6', 'stage-1']
KEYS = {
    'problems-1': [r'cereal', r'trading.standards', r'\b750\b', r'743', r'battery|phone', r'19\.5', r'15, 19, 20', r'wine|taster|tasting|\btea\b',
                   r'4096|2\^\{12\}', r'pizza|deliver', r'33\.5', r'9\.6', r'1\.753', r'1\.895', r'smallest .{0,40}reject'],
    'problems-2': [r'fertilis', r'wheat|plots?\b', r'2\.25', r'0\.7274', r'either rule|either reject', r'tyre|tread', r'0\.1587', r'running|shoe|runner',
                   r'-7, -3', r'6\.18', r'blood|marker|clinic|screen', r'prevalence|base rate', r'0\.0359', r'paired'],
    'problems-3': [r'\bgenes?\b', r'0\.8715|0\.95\^\{40\}', r'0\.00125', r'pension|fund manager|consultant', r'SR.{0,6}sqrt', r'0\.0125k',
                   r'checkout', r'id.k', r'0\.95\^\{1/', r'biomarker', r'0\.0455', r'0\.0027', r'hold.?out|fresh data',
                   r'false share|share of .{0,20}finds'],
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
