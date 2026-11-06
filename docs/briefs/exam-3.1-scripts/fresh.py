"""Freshness grep for topic-3.1: each item's distinctive parameters and keys against every course, exam, bank and
drill file (except topic-3.1.json itself). Prints the hits per token; the report records the reading of each.
Run: python3 docs/briefs/exam-3.1-scripts/fresh.py
"""
import glob
import os
import re

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'app', 'content')
TOKENS = {
    'e-pair-count': ['9,730', '9730', '19,460'],
    'e-survival-share': ['1.15%', '40.0%'],
    'e-root-k': ['6.30'],
    'e-crash-beta': ['12.6%', 'beta 1.6'],
    'e-sixteen-cells': ['0.9545^{16}', '0.0455'],
    'e-ssd-sd': ['1.04, 1.02, 1.07', '0.0232'],
    'e-lowest-match': ['0.22%'],
    'e-capital-split': ['£0.88', '0.88 / 20'],
    'e-plan-checks': ['9.8%', '0.0200'],
    'e-dead-losers': ['2.92', '4.12'],
    'e-one-trade': ['1.011', '0.0649'],
    'e-month-counts': ['347', '9/4'],
    'e-bounce-share': ['1.18%', '19.5%'],
    'e-gap-in-se': ['5.90%', '0.68%'],
    'e-lead-cell': ['0.79%', '1.25%'],
    'e-convergence-pooled': ['73 / 120', '60.8%'],
    'e-chance-passes': ['7,140', '71.4'],
    'e-lock-count': ['1,764', '1764', '1,386'],
    'e-nw-hand': ['32.8', '2.16'],
    'e-after-pub': ['36.4%', '0.613'],
    'e-break-even-net': ['5.2%', '0.72%'],
    'e-hedge-ratio': ['1.0918', '0.0418', '1.8 \\ln'],
    'e-skip-event': ['0.37 points', '0.025'],
    'e-capital-code': ['cycle_capital'],
    'e-composite-code': ['jt_composite'],
    'e-survival-note': ['0.31%', '0.16%'],
}
files = [f for f in glob.glob(os.path.join(ROOT, '**', '*.json'), recursive=True)
         if os.path.basename(f) not in ('topic-3.1.json', 'manifest.json')]
text = {f: open(f, encoding='utf8').read() for f in files}
for iid, toks in TOKENS.items():
    for t in toks:
        pat = re.compile(r'(?<![0-9.])' + re.escape(t) + r'(?![0-9])')
        hits = [os.path.relpath(f, ROOT) for f, s in text.items() if pat.search(s)]
        print(f'{iid:22s} {t!r:22s} {len(hits):3d} ' + ', '.join(hits[:5]))
