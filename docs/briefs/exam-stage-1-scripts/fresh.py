"""Freshness grep for stage-1: each authored item's distinctive parameters and keys against every course, exam, bank and
drill file (except stage-1.json itself). Prints the hits per token; the report records the reading of each.
Tokens are matched on the raw JSON text, so LaTeX is written with doubled backslashes.
Run: python3 docs/briefs/exam-stage-1-scripts/fresh.py
"""
import glob
import os
import re

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'app', 'content')
TOKENS = {
    'a-chain-power': ['(x^3 + 2x)^4', '540'],
    'a-ftc-log': ['2x + \\\\tfrac{1}{x}', '9.0986'],
    'a-desk-profit': ['90 - 2q', '80q - 2q^2'],
    'a-parts-exp': ['x e^{3x}', '4.5746'],
    'a-taylor-product': ['e^x \\\\cos x', '1+x-\\\\frac{x^3}{3}'],
    'a-directional': ['xy^2 + 2x', '(2, 1)'],
    'a-lagrange-product': ['x + 4y = 32'],
    'a-triangle-integral': ['0 \\\\le y \\\\le x \\\\le 3', '13.5'],
    'a-cos-limit': ['1 - \\\\cos 4x'],
    'a-det-three': ['2 & 1 & 0 \\\\\\\\ 1 & 3 & 1'],
    'a-nullity': ['1 & 2 & 0 & 1 & 3'],
    'a-line-distance': ['(4, 1, 3)', '3.1623'],
    'a-eigvec': ['6 & 2 \\\\\\\\ 2 & 3'],
    'a-singular': ['2 & 0 \\\\\\\\ 3 & 4', '5.1569'],
    'a-ls-pca-code': ['[1.2, 1.9, 3.1, 4.8]', '[0.01, 0.012]'],
    'b-fraud-flag': ['0.0608', '0.5263'],
    'b-regime-share': ['0.85', '0.625'],
    'b-many-bets': ['350 independent', '0.1304'],
    'b-var-combo': ['2X - 3Y'],
    'b-ruin-target': ['171}{211', '0.8104'],
    'b-mle-rate': ['0.8, 1.7, 0.4', '0.7692'],
    'b-interval-width': ['2.94'],
    'b-pvalue-mean': ['0.07%', '484 days'],
    'b-forty-tests': ['0.8715', '0.95^{40}'],
    'b-ols-table': ['[2.1, 2.9, 4.2, 4.8, 7.1]', '0.42', '2.8'],
    'b-parity-put': ['7.20', '10.12'],
    'b-two-step': ['1.02 per step', '3.998', '3.9985'],
    'b-book-orders': ['99.98', '100.026'],
    'b-crr-python': ['crr_put', 'dividend yield'],
    'c-price-file': ['2026-03-04,102.0', '312.4', '63.75'],
    'c-log-axis': ['£2.50'],
    'c-broadcast-shape': ['(5, 1)'],
    'c-desk-sum': ['| credit | 210 |'],
    'c-sql-having': ['10.5', 'HAVING COUNT(*) >= 2'],
    'c-git-branch': ['fix-vol'],
    'c-pytest-catch': ['(new - old) / new'],
    'c-complexity-table': ['heapify'],
    'c-coin-ways': ['50p'],
    'c-close-pairs': ['count_close_pairs'],
    'c-crr-cpp': ['crr_price'],
    'c-by-reference': ['bump_ref'],
    'c-halvings': ['4,000,000 prices'],
    'd-eps-n': ['3n + 2}{n + 1}', '0.004'],
    'd-which-converges': ['4^n}{n!}', 'n}{5n - 1}'],
    'd-delta-square': ['0.07', '|x + 3| \\\\le 7'],
    'd-mvt-cubic': ['x^3 + 4x', '2.6458'],
    'd-rank-nullity-proof': ['\\\\mathbf{u}_1, \\\\dots, \\\\mathbf{u}_k'],
    'd-spectral-proof': ['\\\\mathbf{q}^T\\\\mathbf{x} = 0'],
    'd-poly-angle': ['0.8660'],
    'd-diff-image': ['degree at most 4'],
    'd-compact-set': ['\\\\{0\\\\} \\\\cup'],
    'd-complex-power': ['-1 + i\\\\sqrt{3}'],
    'd-residue': ['cos z}{z - 1}', '3.3948'],
    'd-green-square': ['x^2 y\\\\,dx'],
    'd-damped-value': ['4y\' + 13y'],
    'd-rk4-rate': ['1.5(0.04 - r)'],
    'd-laplace-shift': ['e^{2t}\\\\sin 3t'],
}
files = [f for f in glob.glob(os.path.join(ROOT, '**', '*.json'), recursive=True)
         if os.path.basename(f) not in ('stage-1.json', 'manifest.json')]
text = {f: open(f, encoding='utf8').read() for f in files}
for iid, toks in TOKENS.items():
    for t in toks:
        pat = re.compile(r'(?<![0-9.])' + re.escape(t) + r'(?![0-9])')
        hits = [os.path.relpath(f, ROOT) for f, s in text.items() if t in s and pat.search(s)]
        print(f'{iid:22s} {t!r:40s} {len(hits):3d} ' + ', '.join(hits[:4]))
