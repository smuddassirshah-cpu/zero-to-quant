"""Freshness grep for the 0.6 and 0.7 additions to stage-0: each new item's distinctive statement and key against every
course, exam, bank and drill file (except stage-0.json itself). Prints the hits per token; the report records the reading.
Tokens are matched on the raw JSON text, so LaTeX is written with doubled backslashes.
Run: python3 docs/briefs/exam-stage-0-scripts/fresh.py
"""
import glob
import os
import re

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'app', 'content')
TOKENS = {
    'p-direct-proof': ['n^2 - 1$ is divisible by 8', '4k(k + 1)'],
    'p-direct-step': ['n = 13', '168'],
    'p-contrapositive-proof': ['n^3 + 5', '8k^3 + 12k^2 + 6k + 6'],
    'p-contrapositive-form': ['ab > 9'],
    'p-contradiction-proof': ['\\\\log_2 5$ is irrational', '2^p = 5^q', '2.321928'],
    'p-euclid-number': ['510{,}511', '26{,}869', '2, 3, 5, 7, 11, 13 and 17'],
    'p-induction-proof': ['3^n > n^3', '\\\\tfrac54\\\\right)^3'],
    'p-induction-base': ['3^n > n^3'],
    'p-counterexample-proof': ['divides $bc$', 'divides $b$ or $a$ divides $c$'],
    'p-first-failure': ['2n^2 + 29', '1,711'],
    'p-negate-quantifiers': ['profit on every day'],
    'p-onto-function': ['\\\\left\\\\lceil \\\\tfrac{n}{2}', '\\\\left\\\\lfloor \\\\tfrac{n^2}{2}'],
}
files = [f for f in glob.glob(os.path.join(ROOT, '**', '*.json'), recursive=True)
         if os.path.basename(f) not in ('stage-0.json', 'manifest.json')]
text = {f: open(f, encoding='utf8').read() for f in files}
for iid, toks in TOKENS.items():
    for t in toks:
        pat = re.compile(r'(?<![0-9.])' + re.escape(t) + r'(?![0-9])')
        hits = [os.path.relpath(f, ROOT) for f, s in text.items() if t in s and pat.search(s)]
        print(f'{iid:24s} {t!r:40s} {len(hits):3d} ' + ', '.join(hits[:4]))
