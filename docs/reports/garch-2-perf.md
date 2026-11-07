# garch level 2: performance task (perf retrofit)

- `app/content/courses/garch/homework-2.json`, `h-garch-nll`, index 9 (10 of 10), appended. Kind `code` (Python), difficulty 5.
- Objective: l7 "Write its log-likelihood by hand and know how far to trust a fit". Test 3 (β = 0) is l6's ARCH(1).
- Product: `garch_nll(theta, r)` from a stub. 12 tests, 1 example, values by loop, lfilter plus `norm.logpdf`, exact fractions. 19 planted slips all fail, among them the sample-variance start, today's residual, no ½, no ln 2π, mean ignored, no constraint check.
- Overlap: l7 screens 4, 5 and 7 and quiz q4, l8 screens 2 and 10, homework-2 `h-mle-steps`. New: μ in the likelihood, start at the parameters' own long run, `math.inf` outside the region (α = 0, β = 0 inside), no scaffold, share C.
- Gates: (1) `cd app && node tools/validate.mjs`: 0 errors. (2) `VOICE_BASE=app/content/courses/garch python3 docs/reviews/voice-scan.py 35`: 0 and 0. (3) `venv/bin/python docs/reports/garch-2-perf-numbers.py`: exit 0, 99 checks. (4) `node tools/playthrough.mjs --set garch/homework-2 --local-cdn <pkgs>`, with and without `--mobile`: All passed.
- Freshness: grep of `neg_loglik`, `garch_variance`, `math.inf`, `np.inf`, `log-likelihood`, `long-run`, `mu`; `fresh-check --file` (also `--min-run 8 --min-share 0`): no hit on the item.
- Backlog: 1 bullet.
