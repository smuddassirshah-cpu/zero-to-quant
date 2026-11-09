# eigen level 4: performance task

- `app/content/courses/eigen/homework-4.json`, item `h-replicate-svd`, index 10 (appended; cap 12). Kind `code` (Python, NumPy), difficulty 5, `eg-svd`.
- Matched objective (l17): "Build $\mathbf{A}^+$ from the SVD and use it for least squares when $\mathbf{A}^T\mathbf{A}$ is singular." The only verb-rule objective of the level.
- From a stub, `replicate_payoff(PAY, y, tol)` returns the shortest least-squares weights on a five-state option table (bond, stock, call and put at 100, tied by put-call parity), the residual $\mathbf{y} - \text{PAY}\,\mathbf{w}$ and the count of singular values kept, built from `np.linalg.svd`.
- 13 hidden tests, 1 example: straddle, covered call, a digital no weights reach, a two-state wide table, a put keyed as 10.01 (singular value 0.00008). Fourteen planted bugs each fail one or more (normal equations, no cut-off, absolute cut-off, residual sign, rank as `len(s)` or `matrix_rank`, a dropped column, no division, `full_matrices`, NumPy's pseudoinverse, and others); a second correct route passes.
- Overlapping screens: l17 screens[3] to [6], [8] (`pinv_svd`), [9] (`hedge_min_norm`), [10]; `h-code-lstsq`, `h-pinv1`; review-4 `r-cut`, `r-pinv`. New: option replication, the residual and rank returned, the parity direction as the null space, a wide table, a typo that a relative cut-off absorbs.

## Gates

1. Validator, `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors (expected perf-pending warning).
2. Voice, `VOICE_BASE=app/content/courses/eigen python3 docs/reviews/voice-scan.py 35`: 0 and 0.
3. Numbers script, `<venv>/bin/python -I docs/reports/eigen-4-perf-numbers.py`: exit 0 (SymPy exact pseudoinverse and mpmath 50-digit SVD against Fractions normal equations on the solution line and NumPy; solution, starter and bugs run on every test).
4. Playthrough, `node tools/playthrough.mjs --set eigen/homework-4 --local-cdn <pkgs>`, with and without `--mobile`: All passed; 440 px shots read.

Freshness: `fresh-check.mjs --file`: 0 hits. Grep: `straddle`, `put-call`, `parity`, `digital`, `replicat`, `residual`, `10.01`, `lstsq`, `shortest`. Backlog: 0 bullets.
