"""Freshness grep for topic-0.6: each item's distinctive parameters and keys against every course, exam, bank and
drill file (except topic-0.6.json itself). Tokens are matched against the decoded strings of each file, so TeX is
written as it reads ($\\cap$, not $\\\\cap$). Prints the hits per token; the report records the reading of each.
Run: python3 docs/briefs/exam-0.6-scripts/fresh.py
"""
import glob
import json
import os
import re

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'app', 'content')
TOKENS = {
    'e-five-letter-rows': ['five conditions', 'five letters'],
    'e-vacuous-rule': ['£2m', '£500,000'],
    'e-set-elements': ['\\{2, \\{2, 3\\}', '\\{3\\}, 2\\}'],
    'e-callable-floating': ['callable', '22 + 17'],
    'e-witness-solve': ['4x + 7'],
    'e-negate-desk': ['on call'],
    'e-converse-table': ['\\lnot P \\Rightarrow \\lnot Q', 'inverse'],
    'e-functions-count': ['4 venues', '4^3'],
    'e-injection-count': ['6 sectors', '6 \\times 5 \\times 4'],
    'e-fee-inverse': ['£14.50', '2.5 + 0.8n', '£0.80'],
    'e-exp-onto': ['g(x) = e^x'],
    'e-element-chase': ['(A \\cup B) \\cap C', '(A \\cap C) \\cup B'],
    'e-odd-direct': ['mn + m + n'],
    'e-quarters-contrapositive': ['four quarters', 'above 3%'],
    'e-rational-plus-irrational': ['$a + b$ is irrational', 's - a'],
    'e-step-no-base': ['n + 1 < n', 'k + 1 < k'],
    'e-proved-converse': ['$n^2$ is a multiple of 4', '16k^2'],
    'e-prime-formula': ['10n^2 + 1', '361', 'perfect square'],
    'e-base-case-seven': ['7n', '2^n \\ge 7n'],
    'e-log-contradiction': ['\\log_2 3', '2^p = 3^q'],
    'e-forwards-proof': ['x + \\tfrac{1}{x}', 'x + 1/x'],
    'e-product-sum': ['n(n + 1)(n + 2)', '3{,}080', '3,080', '3080'],
    'e-two-squares': ['4m + 3', 'sum of two squares'],
    'e-weighted-sum': ['2^{n + 1} + 2', 'n \\cdot 2^n', '98'],
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
         if os.path.basename(f) not in ('topic-0.6.json', 'manifest.json')]
text = {}
for f in files:
    with open(f, encoding='utf8') as fh:
        text[f] = '\n'.join(strings(json.load(fh)))
for iid, toks in TOKENS.items():
    for t in toks:
        pat = re.compile(r'(?<![0-9.])' + re.escape(t) + r'(?![0-9])')
        hits = [os.path.relpath(f, ROOT) for f, s in text.items() if pat.search(s)]
        print(f'{iid:26s} {t!r:30s} {len(hits):3d} ' + ', '.join(hits[:5]))
