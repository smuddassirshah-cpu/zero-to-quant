# trees level 1: performance task

- File `app/content/courses/trees/homework-1.json`, item `h-derive-one-step`, index 9, kind `derivation`.
- Matched objective: l3 "Derive risk-neutral probabilities and price by discounted expectation."
- Task: one step with cash at $e^{r\Delta t}$, any payoff. (a) copy and both trades; (b) $q$, the only weight; (c) $d < e^{r\Delta t} < u$, its equivalence with $0 < q < 1$, a trade per failure; (d) a £64 straddle two ways; (e) optional bounds. Rubric 3, 2, 2, 2, 1, `rubric-passes`: only row 5 optional.
- Overlapping screens: l1 screens 4, 5, 7, 8; l2 screens 7, 8; l3 screens 6, 7 (all with 1 + r); homework-1 `h-order-q`, `h-down-weight`, `h-long-client`. New: continuous interest, a general payoff, uniqueness, the converse, a copy that lends, the bounds.
- Gates: (1) validator `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors. (2) voice `VOICE_BASE=app/content/courses/trees python3 docs/reviews/voice-scan.py 35`: 0 and 0. (3) numbers script `venv/bin/python -I docs/reports/trees-1-perf-numbers.py`: 1,816 checks, 0 failures. (4) playthrough `node tools/playthrough.mjs --set trees/homework-1 --local-cdn <pkgs>`, with and without `--mobile`: All passed; one display split with `aligned`.
- Freshness grep: straddle, `e^{r\Delta t}`, £64, `f_u`, determinant, "weighted average". `fresh-check --file`: 0 hits.
