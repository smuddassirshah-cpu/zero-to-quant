"""Freshness of the re-authored items: search every content file (courses, exams, Fluency sets) for the new
numbers, formulae and story words. Formulae are matched with spaces removed. The item's own set is left out.

Run from the repo root: python docs/reviews/delta-problems-aa-3-scripts/fresh.py [--all]
Default: hits in the four courses of topic 0.3 (counting, exp-log, series, trig) and every non-course file (exams, drills, bank). --all: every course.
"""
import glob
import json
import re
import sys

ALL = '--all' in sys.argv
T03 = ['counting', 'exp-log', 'series', 'trig']
TOPIC = {'exp-log': T03, 'series': T03, 'trig': T03}
# (own course, own file, label, needles); a needle starting with "w:" is a whole word, case-insensitive
NEEDLES = [
    ('exp-log', 'exp-log/problems-2.json', 'p-forty-doublings 4', ['10^{16}', '2^{54}', '2^{53}', 'w:9091', 'w:8192', '13.15', 'w:further doublings']),
    ('exp-log', 'exp-log/problems-2.json', 'p-drawdown-recovery', ['w:11%', '1.11^', '0.04532', 'w:4.28', 'w:48,578', '48{,}578', 'w:53,922', 'w:drawdown', '1.25^2', 'w:56.25']),
    ('exp-log', 'exp-log/problems-2.json', 'p-app-users 2', ['\\log_{1.3}', '\\log25}{\\log1.3}', '\\log\\dfrac{25}{1.3}', 'w:Which is equal to', '\\log25-\\log1.3']),
    ('exp-log', 'exp-log/problems-3.json', 'p-weekly-target 3-5', ['w:41.76', 'w:0.0747', 'w:0.0249', 'w:2.52%', '45}{41.76}']),
    ('exp-log', 'exp-log/problems-3.json', 'p-log-chart-line dates', ['w:2017', 'w:2025', 'w:£135']),
    ('series', 'series/problems-2.json', 'p-tin-display', ['w:tins', 'w:tin', '5k+3', 'w:305', 'w:266', 'a=8', 'd=5', 'k=4}^{10}', '8+13+18', 'w:53 tins', 'w:rows 4 to 10', '(8+53)', '8,13,18']),
    ('series', 'series/problems-3.json', 'p-pizza-toppings', ['w:pizza', 'w:pizzas', 'w:toppings', '\\binom{11}{4}', '\\binom{11}{7}', '\\binom{12}{4}', '\\binom{11}{3}', 'w:330', 'w:495', 'w:4096', '2^{12}', 'w:7920', '1,12,66,220', 'w:165', 'w:660']),
    ('series', 'series/problems-3.json', 'p-bracket-estimate 5', ['0.807983', '0.80798', '0.97^7']),
    ('trig', 'trig/problems-1.json', 'p-hexagon-tile', ['w:hexagon', '4\\sqrt{3}', '8\\sqrt{3}', '\\sqrt{48}', '\\sqrt{192}', 'w:8 cm', '8^2-4^2', 'w:256']),
    ('trig', 'trig/problems-1.json', 'p-desk-lamp 3 ratios', ['\\tan^{-1}0.75', '\\tfrac{30}{40}', '\\tfrac{30}{50}']),
    ('trig', 'trig/problems-3.json', 'p-two-angles', ['{28}{53}', '{45}{53}', '28,45,53', 'w:357', 'w:1276', 'w:1325', 'w:164.4', 'w:148.1', '{24}{25}', '{7}{25}', '7,24,25', 'w:0.28', 'w:0.96']),
    ('trig', 'trig/problems-3.json', 'p-daylight-model 4-5', ['w:9.8 hours', 'w:daylight', '-0.5', '-\\tfrac{1}{2}', '-\\frac{1}{2}', '7\\pi}{6}', '-\\tfrac{\\pi}{6}', 'w:14.2', '4.4\\sin']),
    ('trig', 'trig/problems-3.json', 'p-garden-bed', ['{5}{13}', '{12}{13}', '5,12,13', '5/13', '12/13', '65\\sin', 'w:22.62', 'w:157.38', 'w:509', 'w:22.56', 'w:10 m and 13 m', 'w:garden', 'w:flower', 'w:25 m', 'w:0.3846', 'w:0.9231', '\\sqrt{29}', 'w:269']),
]


def strings(o):
    if isinstance(o, str):
        yield o
    elif isinstance(o, dict):
        for v in o.values():
            yield from strings(v)
    elif isinstance(o, list):
        for v in o:
            yield from strings(v)


files = sorted(glob.glob('app/content/**/*.json', recursive=True))
files = [f for f in files if not f.endswith('manifest.json')]
cache = {}
for f in files:
    try:
        cache[f] = list(strings(json.load(open(f))))
    except Exception as e:  # not JSON content
        print('skip', f, e)

total = 0
for course, own, label, needles in NEEDLES:
    scope = TOPIC[course]
    print(f'\n== {label} ({own})')
    for nd in needles:
        hits = []
        for f, strs in cache.items():
            if f.endswith(own):
                continue
            rel = f.split('app/content/')[1]
            top = rel.split('/')
            in_scope = top[0] != 'courses' or top[1] in scope
            if not (ALL or in_scope):
                continue
            for s in strs:
                if nd.startswith('w:'):
                    m = re.search(r'(?<![\w.])' + re.escape(nd[2:]) + r'(?![\w])', s, re.I)
                    found = bool(m)
                    pos = m.start() if m else 0
                else:
                    z = s.replace(' ', '')
                    pos = z.find(nd)
                    found = pos >= 0
                    s = z
                if found:
                    hits.append((rel, s[max(0, pos - 60):pos + 70].replace('\n', ' ')))
        total += len(hits)
        if hits:
            print(f'  "{nd}": {len(hits)} hit(s)')
            for rel, snip in hits[:6]:
                print(f'      {rel}: ...{snip}...')
            if len(hits) > 6:
                print(f'      and {len(hits) - 6} more: ' + ', '.join(sorted({h[0] for h in hits[6:]}))[:300])
print(f'\nfresh.py: {total} hits over {len(cache)} files; each is judged in the review')
