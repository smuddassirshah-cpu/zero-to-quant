"""Freshness grep for topic-2.5: each item's distinctive parameters and keys against every course, exam, bank and
drill file (except topic-2.5.json itself). Prints the hits per token; the report records the reading of each.
Tokens are matched on the raw JSON text, so LaTeX is written with doubled backslashes.
Run: python3 docs/briefs/exam-2.5-scripts/fresh.py
"""
import glob
import os
import re

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'app', 'content')
TOKENS = {
    'e-lp-corner': ['x + 2y \\\\le 8', '3x + 2y \\\\le 12'],
    'e-duality-sandwich': ['earning 8.4', 'cost is 9.6'],
    'e-step-limit': ['5.2&4.8', '0.4 and 10'],
    'e-double-gap': ['3{,}000{,}000', '2^{-31}', '4.656612873077393e-10'],
    'e-bisection-count': ['[1, 3]$ and halves', '2 \\\\times 10^6'],
    'e-mc-error': ['£12.30', '0.0615'],
    'e-convex-sets': ['xy \\\\ge 1,\\\\ x > 0', '\\\\max(|x|, |y|) \\\\le 1', '|x| \\\\ge 1'],
    'e-hessian-threshold': ['3xy + ky^2', '4k - 9'],
    'e-linprog-bounds': ['bounds=(None, None)', 'linprog(-c, A_ub=A, b_ub=b)'],
    'e-dual-function': ['(x + 1)^2 + \\\\lambda(2 - x)', '3\\\\lambda - \\\\tfrac{\\\\lambda^2}{4}'],
    'e-slsqp-sign': ['0.02 - w @ S @ w'],
    'e-rate-from-kappa': ['0.5 and 12', '{23}{25}', '165.7'],
    'e-newton-minimise': ['e^x - 3x', '\\\\tfrac3e', '1.1036'],
    'e-cancel-rewrite': ['\\\\sqrt{x^2 + 1} - x', '10^{16} + 1'],
    'e-log-condition': ['50.50', '\\\\ln 1.02'],
    'e-log1p-blame': ['3.0000446571375978', 'log(1 + 3e-12)'],
    'e-three-point-poly': ['(0, 1)$, $(1, 3)$ and $(3, 2)', '{10}{3}'],
    'e-richardson-three': ['8B - A', '8B-A'],
    'e-gauss-two-point': ['int_0^4 x^4', '199.11'],
    'e-explicit-step': ['400.02', '1600.02', '0.002500'],
    'e-control-variate': ['19.95', '10.26', '2.2167'],
    'e-projection-kkt': ['(x - 4)^2 + (y - 1)^2', 'x + 2y \\\\le 3', '(3.4, -0.2)', '1.682'],
    'e-long-only-kkt': ['0.01, 0.04 and 0.09', '0.02, 0.06 and 0.10', '(0, 0.5, 0.5)'],
    'e-local-global-proof': ['theta\\\\mathbf y + (1 - \\\\theta)\\\\mathbf x^*'],
    'e-normal-equations': ['2 \\\\times 10^6', '4 \\\\times 10^{12}', '4.4 \\\\times 10^{-4}'],
    'e-natural-spline': ['(0, 0)$, $(1, 2)$ and $(2, 1)', '-4.5', '1.28125'],
    'e-log-sum-exp': ['log_sum_exp', '1.8 \\\\times 10^{308}'],
    'e-solver-certificate': ['x^2 + 3y^2', '(3.02, 0.98)', '11.9967', '12.0016'],
    'e-error-budget': ['7.9620', '7.9680', '56{,}250{,}000'],
    'e-stiff-implicit': ['-200e', 'h = 0.05', '-0.6667'],
}
files = [f for f in glob.glob(os.path.join(ROOT, '**', '*.json'), recursive=True)
         if os.path.basename(f) not in ('topic-2.5.json', 'manifest.json')]
text = {f: open(f, encoding='utf8').read() for f in files}
for iid, toks in TOKENS.items():
    for t in toks:
        pat = re.compile(r'(?<![0-9.])' + re.escape(t) + r'(?![0-9])')
        hits = [os.path.relpath(f, ROOT) for f, s in text.items() if t in s and pat.search(s)]
        print(f'{iid:24s} {t!r:34s} {len(hits):3d} ' + ', '.join(hits[:5]))
