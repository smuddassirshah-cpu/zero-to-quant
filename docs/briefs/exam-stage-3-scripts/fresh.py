"""Freshness grep for stage-3: each authored item's distinctive setup phrases, parameters and keys against every course,
exam, bank and drill file (except stage-3.json itself). Prints the hits per token; the report records the reading of each.
Tokens are matched on the raw JSON text, so LaTeX is written with doubled backslashes. Pass --stage3 to list only hits
in Stage 3 files (the courses of topics 3.1 to 3.5, topic-3.x exams, mocks and the bank), the scope of the freshness rule.
Run: python3 docs/briefs/exam-stage-3-scripts/fresh.py [--stage3]
"""
import glob
import json
import os
import re
import sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'app', 'content')
TOKENS = {
    'a-even-product': ['product of the faces is even', 'sum is even'],
    'a-repeat-roll': ['same face as the roll before', 'roll that shows the same face'],
    'a-lead-by-two': ['leads by two', 'lead of two', '0.6923', '3.8462'],
    'a-round-table': ['round table', 'desk heads', 'next to each other', '2}{9}'],
    'a-uniform-product': ['XY < \\\\tfrac12', 'P(XY', '0.8466'],
    'a-quote-game': ['quotes tight or wide', 'trades or waits', 'Tight | 2'],
    'a-six-or-nine': ['total of 9 or more', '18}{43}', '0.4186', '65}{108}'],
    'a-third-loss': ['third losing bet', 'third loss'],
    'a-all-pay': ['all-pay', 'licence', 'v^2/2'],
    'a-edge-hundred': ['100 independent £1 bets', 'finish down', '0.1346'],
    'a-two-flags': ['Two models each flag', 'regime break', '0.8686'],
    'a-informed-buyer': ['45 bid, 55 ask', '63.53', '8.53'],
    'r-backfill': ['loads its past returns', 'Backfill', 'backfill'],
    'r-same-month': ['rolling(6).sum()', 'rank_weights', '6% a month'],
    'r-closed-funds': ['still open at the year end', '200 funds', '4.8'],
    'r-june-book': ['end of June', 'fiscal year ends in March', 'March 2014'],
    'r-which-leak': ['January 2010', '2024 index', 'full-sample volatility'],
    'r-pairs-oos-order': ['2003 to 2024', 'tagged commit', 'Freeze the code'],
    'r-turnover-cost': ['£1.40 in all', 'wipes out the return', '0.79%'],
    'r-t-bar': ['0.45% a month', 'clear $t = 3$', '2.75'],
    'r-small-share': ['£0.05 billion', 'value-weighted', 'equal-weighted return', '1.07%'],
    'r-note-sentence': ['0.84% a month', '0.21% a month', 'value strategy'],
    'r-factor-alpha': ['short-term reversal factor', '0.90% a month', '0.41%'],
    'r-best-of-twenty': ['20 independent variants', '1/\\\\sqrt{5}', '0.2252', '0.23'],
    'r-false-share': ['300 candidate factors', 'expected $t$ of 3.5', '0.0465', '0.0039'],
    'r-as-of-code': ['as_of(', 'point-in-time join', 'period_end'],
    'r-oos-power': ['half its mean return survives', '1.41', '240 months'],
}
S3_COURSES = set()
cur = json.load(open(os.path.join(ROOT, 'curriculum.json')))
for st in cur['stages']:
    if st['id'] == 3:
        for tp in st['topics']:
            S3_COURSES.update(tp['courses'])


def stage3(rel):
    parts = rel.split(os.sep)
    if parts[0] == 'courses':
        return parts[1] in S3_COURSES
    if parts[0] == 'exams':
        return parts[1].startswith(('topic-3.', 'mock-'))
    return parts[0] == 'bank'


only3 = '--stage3' in sys.argv
files = [f for f in glob.glob(os.path.join(ROOT, '**', '*.json'), recursive=True)
         if os.path.basename(f) not in ('stage-3.json', 'manifest.json')]
text = {os.path.relpath(f, ROOT): open(f, encoding='utf8').read() for f in files}
for iid, toks in TOKENS.items():
    for t in toks:
        pat = re.compile(r'(?<![0-9.])' + re.escape(t) + r'(?![0-9])')
        hits = [f for f, s in text.items() if t in s and pat.search(s) and (stage3(f) or not only3)]
        print(f'{iid:20s} {t!r:36s} {len(hits):3d} ' + ', '.join(hits[:4]))
