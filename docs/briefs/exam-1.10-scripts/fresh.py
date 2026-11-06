"""Freshness grep for topic-1.10: each item's distinctive parameters and keys against every course, exam, bank and
drill file (except topic-1.10.json itself). Prints the hits per token; the report records the reading of each.
Tokens are matched on the raw JSON text, so LaTeX is written with doubled backslashes.
Run: python3 docs/briefs/exam-1.10-scripts/fresh.py
"""
import glob
import os
import re

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'app', 'content')
TOKENS = {
    'e-sup-rising': ['2n + 1}{n + 4}', '{7}{n + 4}'],
    'e-diagonal-digits': ['0.5544', '0.4454', '0.4554'],
    'e-telescope-gap-three': ['n(n + 3)', '{11}{18}', '0.6111'],
    'e-halvings-width': ['f(3)', '2^n > 3000', '3}{2^{12}'],
    'e-taxicab': ['(-1, 3)', '(5, -5)'],
    'e-subspace-r3': ['x_1 = 2x_3', 'x_1x_2 = 0'],
    'e-rational-between': ['0.495', '20}{41}', '19.27'],
    'e-n-for-quotient': ['4n + 3}{2n - 1}', '125.5', '5}{2n - 1}'],
    'e-root-recursion': ['3a_n + 10', '3L + 10'],
    'e-which-converge': ['n^3}{2^n}', 'cos^2 n', '(n + 1)!}{4^n}', '2n}{5n + 1}'],
    'e-cube-delta': ['x^3 - 8', 'x^2 + 2x + 4', '0.38'],
    'e-mvt-quartic': ['x^4 + x$', '1.2599', '4x^3 + 1'],
    'e-upper-sum-square': ['3.75', '8}{n}', '801'],
    'e-ftc-both-limits': ['{3}{85}', '0.0353', '{4}{17}'],
    'e-closed-sets': ['2^{-n} : n', '1 + \\\\tfrac1n'],
    'e-coords-new-basis': ['x + x^2', '(3, -1, 6)'],
    'e-antisym-map': ['A} - \\\\mathbf{A}^T', '4 \\\\times 4'],
    'e-matrix-of-map': ["p' + p(0)", '0&1&0\\\\\\\\0&0&2\\\\\\\\1&0&0'],
    'e-dual-basis-pair': ['(3, 2)', '2x-3y', '-4x+5y', '2x - y)'],
    'e-weighted-adjoint': ['3x_1y_1', '1&1\\\\\\\\3&2'],
    'e-jordan-from-kernels': ['2, 4, 5', 'T + I'],
    'e-uniform-peak': ['1 + nx^2', '2\\\\sqrt{n}', '2501'],
    'e-compact-bounded': ['d(x_n, p)', 'B(p, n)'],
    'e-idempotent-split': ['T^2 = T', 'T^2\\\\mathbf{v}'],
    'e-hedge-residual': ['0.00068', '2.61%', '0.0005'],
    'e-symmetric-power': ['7&2\\\\\\\\2&4', '104{,}566', '104566', '261{,}415'],
    'e-chain-response': ['0.85', '2.662', '5.67'],
    'e-three-one-rearrange': ['1.2425', 'H_{6m}', '\\\\tfrac12 \\\\ln 3'],
    'e-contraction-proof': ['k^n}{1 - k}', '1 - \\\\tfrac x2', 'x_{n+1} = f(x_n)'],
    'e-rayleigh-proof': ['0.04, 0.01', 'lambda_i c_i^2'],
}
files = [f for f in glob.glob(os.path.join(ROOT, '**', '*.json'), recursive=True)
         if os.path.basename(f) not in ('topic-1.10.json', 'manifest.json')]
text = {f: open(f, encoding='utf8').read() for f in files}
for iid, toks in TOKENS.items():
    for t in toks:
        pat = re.compile(r'(?<![0-9.])' + re.escape(t) + r'(?![0-9])')
        hits = [os.path.relpath(f, ROOT) for f, s in text.items() if t in s and pat.search(s)]
        print(f'{iid:24s} {t!r:34s} {len(hits):3d} ' + ', '.join(hits[:5]))
