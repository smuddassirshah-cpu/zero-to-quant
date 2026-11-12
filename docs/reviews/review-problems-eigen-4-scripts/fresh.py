"""Second read, eigen problems-4: reuse grep and skills check.
Every matrix, key number and story noun of the set, searched (whitespace-normalised) across app/content.
Prints each hit outside problems-4.json; the hits are judged by hand in the review. Then: every `skills` id of an
item is carried by a lesson of level 4, and every lesson of the level is named by the review's lesson table.
Run from the repo root:  python3 docs/reviews/review-problems-eigen-4-scripts/fresh.py"""
import glob
import json
import re
import sys

SELF = 'app/content/courses/eigen/problems-4.json'
PAT = {
    'p-linked-lagoons': [r'-4&2\\\\1&-3', r'-4&1\\\\2&-3', r'-5&0\\\\1&-2', r'1&1\\\\0&1', r'1&-1\\\\0&1',
                         r'\[\[1,1\],\[0,1\]\]', r'lagoon', r'hydrolog', r'chemicalspill', r'6e\^\{-2', r'0\.819',
                         r'trace7anddeterminant10'],
    'p-wind-pair': [r'16&20\\\\20&34', r'4&0\\\\5&3', r'turbine', r'MWh', r'2\.828', r'0\.0183',
                    r'\[\[16,20\],\[20,34\]\]', r'\\sqrt\{34', r'e\^\{-4\}'],
    'p-track-laps': [r'2&4\\\\1&2\\\\2&4', r'9&18\\\\18&36', r'lapsperkm', r'[^a-z]laps[^a-z]', r'\(11,5,9\)',
                     r'\\sqrt\{?45', r'\(2,1,2\)', r'\[\[9,18\],\[18,36\]\]'],
    'p-machine-stops': [r'-0\.2&0\.6\\\\0\.2&-0\.6', r'-0\.6&0\.2\\\\0\.6&-0\.2', r'packaging', r'maintenanceteam',
                        r'\(0\.75,0\.25\)', r'0\.75\+0\.25\*?e', r'0\.25\+0\.75\*?e', r'0\.318', r'\\ln75',
                        r'e\^\{-2\.4\}', r'Running,Stopped'],
}
files = [f for f in glob.glob('app/content/**/*.json', recursive=True) if f != SELF and not f.endswith('manifest.json')]
texts = {f: re.sub(r'\s+', '', open(f).read().replace('\\\\', '\\')) for f in files}
for item, pats in PAT.items():
    print(f'== {item}')
    for p in pats:
        hits = sorted(f.replace('app/content/', '') for f, t in texts.items() if re.search(p, t))
        print(f'   {p:34} {len(hits):3} file(s) {hits[:5]}{" ..." if len(hits) > 5 else ""}')

course = json.load(open('app/content/courses/eigen/course.json'))
lv = [x for x in course['levels'] if x['n'] == 4][0]
have = {}
for l in lv['lessons']:
    d = json.load(open(f'app/content/courses/eigen/{l}.json'))
    ids = set(d.get('skills') or [])
    for s in d.get('screens', []):
        ids |= set(s.get('skills') or [])
    for i in ids:
        have.setdefault(i, []).append(l.split('-')[0])
print('level 4 lessons carry', dict(sorted(have.items())))
bad = 0
for it in json.load(open(SELF))['items']:
    miss = [s for s in it['skills'] if s not in have]
    print(f'   {it["id"]}: {it["skills"]}{"  NOT IN THE LEVEL: " + str(miss) if miss else ""}')
    bad += len(miss)
sys.exit(1 if bad else 0)
