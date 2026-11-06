"""Freshness grep for stage-2: each authored item's distinctive parameters and keys against every course, exam, bank and
drill file (except stage-2.json itself). Prints the hits per token; the report records the reading of each.
Setups are compared by tools/fresh-check.mjs (run: node tools/fresh-check.mjs --exam stage-2 from app/); this script checks
the numbers. Tokens are matched on the raw JSON text, so LaTeX is written with doubled backslashes.
Run: python3 docs/briefs/exam-stage-2-scripts/fresh.py
"""
import glob
import os
import re

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'app', 'content')
TOKENS = {
    'a-shrink-mean': ['0.0909', '0.0004'],
    'a-review-threshold': ['£160'],
    'a-purged-fold': ['830', 'rows 601 to 720'],
    'a-leak-steps': ['120 features'],
    'a-curves-meet': ['1.02', '1.05'],
    'a-tree-split': ['-14, -9, -2, 5, 7, 18', '504.17'],
    'a-block-bootstrap': ['15.99', '25 monthly blocks'],
    'a-boost-leaf': ['13 up days', '0.6648'],
    'a-shap-sum': ['0.5548', '$0.48$'],
    'a-lasso-entry': ['12.4, -18.6, 7.2, 15.0', '0.0744'],
    'a-frac-weight': ['d = 0.35', '0.0626'],
    'a-label-uniqueness': ['5 to 7 and 6 to 9', '2.36'],
    'a-bet-size': ['0.1953', '0.62 probability'],
    'a-psr': ['0.9217', '156 weeks'],
    'a-lambda-honest': ['4.10 | 3.95', '3.88'],
    'a-walk-forward-ridge': ['factor-days', 'nested_walk_forward'],
    'b-returns-not-prices': ['unit root, so their mean and variance drift'],
    'b-ar1-spread': ['0.3 + 0.6s_{t-1}', '0.025'],
    'b-ljung-box': ['0.12, -0.05', '5.91'],
    'b-ar2-root': ['1.1x_{t-1} - 0.3x_{t-2}'],
    'b-yule-walker': ['0.45$ and $\\\\hat\\\\rho_2 = 0.05', '-0.1912'],
    'b-ma-forecast': ['0.0008 + \\\\varepsilon_t + 0.35', '0.0057'],
    'b-arch-lm': ['0.0188', '14.1'],
    'b-garch-longrun': ['\\\\omega = 3 \\\\times 10^{-6}', '0.1944'],
    'b-ewma-update': ['0.01268', '-0.028'],
    'b-es-normal': ['£3,000,000', '98,188'],
    'b-spurious-read': ['t = 11.4'],
    'b-df-hand': ['0.40, 0.25, 0.05, 0.12', '-3.20'],
    'b-eg-pair': ['pair-closes', 'adf1_spread', '5.16'],
    'b-hedge-notional': ['1.6\\\\ln B', '£800,000'],
    'b-pair-pnl': ['48.20', '40,614'],
    'c-float32-fees': ['7.8125', '£100,000'],
    'c-condition-digits': ['0.999 \\\\\\\\ 0.999', '3.30'],
    'c-newton-yield': ['0.0769', 'costs 95'],
    'c-simpson-kink': ['strike falls between two nodes'],
    'c-error-rates': ['four times the paths'],
    'c-three-pricers': ['fd_call', 'quad_call', 'mc_cv_call', 'S_T^2', '5\\\\sigma\\\\sqrt T'],
    'c-kkt-hand': ['0.5571', '0.0204'],
    'c-kkt-code': ['mv_weights'],
    'c-dedication-lp': ['233.10', '0.9074'],
    'c-convex-functions': ['worst loss over five scenarios'],
    'c-projected-step': ['(0.6, 0.3, 0.1)', '(0.2, -0.6, 0.5)'],
    'c-poisson-offset': ['8.263', '6.5-hour'],
    'c-irls-two': ['irls_grouped_logit', 'poisson_irls_se', 'fill-buckets', 'jump-days'],
    'c-factorial-interaction': ['12.0 and the new one 9.5'],
    'c-signed-rank': ['1.4, -0.6, 2.2', '1.40'],
    'c-gamma-waits': ['5.2, 7.9, 3.4', '7.42'],
    'c-batch-means': ['0.212, 0.198', '0.0047'],
    'c-partial-pooling': ['4.2 over 9 trades', '2.04'],
    'c-mcmc-check': ['gibbs_normal', 'chains.csv'],
    'd-sortino': ['0.021, -0.012', '0.663'],
    'd-participation-fill': ['50.1717', '120,000, 80,000'],
    'd-survivors': ['400 that still trade', '0.012'],
    'd-held-out': ['2012 to 2025'],
    'd-sharpe-interval': ['0.35 over 60 months', '0.309'],
    'd-universe-date': ['31 December 2024'],
    'd-reversal-weights': ['0.05, -0.02, 0.01, -0.04', '0.3194'],
    'd-fundamental-law': ['0.025 on 400 shares', '0.953'],
    'd-net-sharpe': ['1.404', '12 basis points of the value traded'],
    'd-signal-report': ['signal-panel', 'ic_and_turnover'],
    'd-gamma-pnl': ['K = 84', '0.1105'],
    'd-butterfly-density': ['12.45, 8.35 and 4.10', '-0.006'],
    'd-parity-fit': ['parity_fit', '100.75'],
    'd-atm-vol': ['9.80', '0.1965'],
    'd-audit-ids': ['214,285', 'by 6 or by 14'],
    'd-sum-runs': ['2, -1, 3, 1, -2, 2, 1, -3, 3'],
    'd-constraints': ['200{,}000'],
    'd-rating-odds': ['0.2403', '1600'],
}
files = [f for f in glob.glob(os.path.join(ROOT, '**', '*.json'), recursive=True)
         if os.path.basename(f) not in ('stage-2.json', 'manifest.json')]
text = {f: open(f, encoding='utf8').read() for f in files}
for iid, toks in TOKENS.items():
    for t in toks:
        pat = re.compile(r'(?<![0-9.])' + re.escape(t) + r'(?![0-9])')
        hits = [os.path.relpath(f, ROOT) for f, s in text.items() if t in s and pat.search(s)]
        print(f'{iid:24s} {t!r:44s} {len(hits):3d} ' + ', '.join(hits[:4]))
