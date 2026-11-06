"""Freshness grep for topic-2.6: each item's distinctive parameters and keys against every course, exam, bank and
drill file (except topic-2.6.json itself). Tokens are matched against the decoded strings of each file, so TeX is
written as it reads ($\\cap$, not $\\\\cap$). Prints the hits per token; the report records the reading of each.
Run: python3 docs/briefs/exam-0.6-scripts/fresh.py
"""
import glob
import json
import os
import re

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'app', 'content')
TOKENS = {
    'e-fill-time-family': ['block trade', 'daily volume'],
    'e-pd-at-leverage': ['-4.2', '23.15%', '0.2315'],
    'e-algo-f': ['SSB = 18', 'SSW = 105'],
    'e-u-share': ['U_X = 99', '99 / 180', '99/180'],
    'e-fill-posterior': ['Beta(4, 6)', 'Beta(22, 38)', '0.3667'],
    'e-trades-offset': ['0.045v', '18.28', '- 0.9 + 0.045'],
    'e-working-response': ['-2.6363', '\\mu = 0.2$'],
    'e-deviance-two': ['412.6', '405.1', '0.0235'],
    'e-orders-per-arm': ['\\sigma = 9', '318'],
    'e-design-confound': ['through January', 'large orders'],
    'e-u-from-days': ['0.4, 1.2', '-0.5$, 0.6, 0.2'],
    'e-perm-p': ['B = 299', '0.0700', '0.0669'],
    'e-silverman-250': ['1.75%', '0.3896', '250 daily returns'],
    'e-sign-test-ties': ['14 of 18', '0.0309', '4,048', '4{,}048'],
    'e-default-rate': ['Gamma(3, rate 2)', 'Gamma(10, 7)', '1.4286'],
    'e-alpha-prior': ['N(0, 1.5^2)', 'estimated at 8%', '1.6%'],
    'e-metropolis-log': ['-14.2', '-15.1', '1.20'],
    'e-ess-sticky': ['\\phi = 0.75', '857.1'],
    'e-broker-anova': ['2, 3, 3, 4', '5, 7, 8, 8', '14.4'],
    'e-takeover-week': ['7.9 was a takeover', '0.5930', '0.2, $-0.1$, 0.9'],
    'e-no-defaults-next': ['Gamma(12', '0.3244', '0.3347', 'outage'],
    'e-hit-rate-shrink': ['Beta(18, 22)', '33 of', '0.51'],
    'e-walsh-median': ['walsh', 'Walsh', 'Hodges'],
    'e-rejections-dispersion': ['588', '0.072', '0.028'],
    'e-kruskal-h': ['kruskal', 'Kruskal'],
}


def strings(x):
    if isinstance(x, str):
        yield x
    elif isinstance(x, dict):
        for v in x.values():
            yield from strings(v)
    elif isinstance(x, list):
        for v in x:
            yield from strings(v)


files = [f for f in glob.glob(os.path.join(ROOT, '**', '*.json'), recursive=True)
         if os.path.basename(f) not in ('topic-2.6.json', 'manifest.json')]
text = {}
for f in files:
    with open(f, encoding='utf8') as fh:
        text[f] = '\n'.join(strings(json.load(fh)))
for iid, toks in TOKENS.items():
    for t in toks:
        pat = re.compile(r'(?<![0-9.])' + re.escape(t) + r'(?![0-9])')
        hits = [os.path.relpath(f, ROOT) for f, s in text.items() if pat.search(s)]
        print(f'{iid:26s} {t!r:30s} {len(hits):3d} ' + ', '.join(hits[:5]))
