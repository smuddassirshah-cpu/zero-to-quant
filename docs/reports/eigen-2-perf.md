# eigen level 2: performance task

- `app/content/courses/eigen/homework-2.json`, item `hw-sigma-code`, index 9 (appended; cap 12). Kind `code` (Python, NumPy), difficulty 5, `eg-pd`.
- Matched objective (l7): "Build $\boldsymbol{\Sigma}$ from returns and read portfolio variances from it." (l5's "Write ... $\mathbf{Q}\boldsymbol{\Lambda}\mathbf{Q}^T$" is already asked by hand in `hw-risk-analysis`.)
- From a stub, `risk_from_returns(R, W)` returns $\boldsymbol{\Sigma}$ (demeaned, over $n$), each column's $\mathbf{w}^T\boldsymbol{\Sigma}\mathbf{w}$, and the least variance at $|\mathbf{w}| = 1$ ($\lambda_{\min}$).
- 8 hidden tests, 1 example, three tables. Eleven planted bugs each fail one or more (no demeaning, $n - 1$, `np.cov` defaults, no cross terms, rows of `W`, largest eigenvalue, least asset, least given portfolio, and others); a second correct route passes.
- Overlapping screens: l7 screens[2] to [5] and [8], l2 screens[8], `hw-build-sigma`, `hw-risk-analysis` part 3, review-2 `r-covariance-entry`, `r-zero-eigenvalue`. New: code for any size, many portfolios at once, $\lambda_{\min}$ beside a shorter portfolio's 0.6, a fund that is half A plus half B.
- Layout: the older `hw-risk-analysis` model display ran past 440 px; split with `aligned`.

## Gates

1. Validator, `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors (expected perf-pending warning).
2. Voice, `VOICE_BASE=app/content/courses/eigen python3 docs/reviews/voice-scan.py 35`: 0 and 0.
3. Numbers script, `<venv>/bin/python -I docs/reports/eigen-2-perf-numbers.py`: exit 0 (SymPy exact $\boldsymbol{\Sigma}$ and roots against Fractions series variances and a NumPy sphere search; solution, starter and bugs run on every test).
4. Playthrough, `node tools/playthrough.mjs --set eigen/homework-2 --local-cdn <pkgs>`, with and without `--mobile`: All passed; 440 px shots read.

Freshness: `fresh-check.mjs --file`: one hit, older items[4]. Grep: `risk_from_returns`, `eigvalsh`, `np.cov`, `least variance`, `demean`, `half of`. Backlog: 0 bullets.
