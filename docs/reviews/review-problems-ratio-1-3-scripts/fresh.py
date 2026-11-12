#!/usr/bin/env python3
"""Second read, ratio problems-1 to -3: where else in app/content the story nouns and key numbers of each problem appear.
Prints, for each pattern, the files (other than the three sets) that hold it and a short context from the first match,
so the reader can judge each by eye. `--course` limits the search to the ratio course (lessons, quizzes, reviews, homework).

  python3 docs/reviews/review-problems-ratio-1-3-scripts/fresh.py [--course]        (from the repo root)"""
import glob, re, sys

ROOT = 'app/content/courses/ratio/' if '--course' in sys.argv else 'app/content/'
OWN = {f'app/content/courses/ratio/problems-{n}.json' for n in (1, 2, 3)}
PATTERNS = {
    'p-pension-split': [r'pension', r'9,600', r'three eighths|\\tfrac\{3\}\{8\}|37\.5%', r'bonds', r'4,140|5,760|9,900'],
    'p-platform-fee': [r'platform', r'0\.35%', r'8,400', r'29\.40', r'0\.9965'],
    'p-phone-rise': [r'phone contract|SIM', r'percentage points', r'3\.9', r'32\.13', r'1\.071'],
    'p-savings-tax': [r'allowance', r'tax-free', r'18,000', r'4\.6%', r'131\.20|696\.80'],
    'p-share-week': [r'small-cap', r'72\.50|84\.10', r'16%', r'0\.9744', r'70\.64'],
    'p-laptop-sale': [r'laptop', r'561', r'660', r'0\.935'],
    'p-fund-two-years': [r'6,250', r'7,840', r'1\.2544', r'[Ss]imple interest', r'11,014'],
    'p-fund-six-months': [r'52,000', r'0\.91\b', r'1\.09\b', r'0\.9919', r'39,185|50,746'],
    'p-partners-profit': [r'partner', r'3 : 4 : 5', r'11,400|2,850|11,900', r'18,000 : 24,000'],
    'p-print-run': [r'leaflet', r'press(es)?\b', r'press-hour', r'36,000', r'23\.33'],
    'p-coffee-suppliers': [r'coffee|beans', r'CHF', r'1\.10\b', r'1\.20\b', r'27\.50|29\.40|441'],
    'p-villa-split': [r'villa', r'1\.125', r'405', r'3,240', r'nights'],
}
files = sorted(f for f in glob.glob(ROOT + '**/*.json', recursive=True) if f not in OWN and not f.endswith('manifest.json'))
texts = {f: open(f, encoding='utf-8').read() for f in files}
for item, pats in PATTERNS.items():
    print(f'== {item}')
    for p in pats:
        rx = re.compile(p)
        hits = [(f, rx.search(t)) for f, t in texts.items()]
        hits = [(f, m) for f, m in hits if m]
        print(f'  /{p}/  {len(hits)} file(s)')
        for f, m in hits[: (40 if '--course' in sys.argv else 6)]:
            t = texts[f]
            ctx = re.sub(r'\s+', ' ', t[max(0, m.start() - 70): m.end() + 70])
            print(f'      {f.replace("app/content/", "")}: ...{ctx}...')
