# pdes level 1: performance task

- File and item: `app/content/courses/pdes/homework-1.json`, item 8 of 8, `h-derive-lazy-walk`. It was appended; the homework had 7 items, so nothing was converted. Kind `derivation` (empty longform), difficulty 5, skill `pe-heat`, no tags.
- Objective (verb rule): l2 "Derive the heat equation from a random walk by Taylor expansion".
- Task: a lazy, biased walk (right $p$, left $q$, stay $r$). The learner derives $u_t + cu_x = Du_{xx}$ and states the scaling ($\Delta x^2/\Delta t$ fixed, $p - q \propto \Delta x$). They bound the time and space Taylor remainders, then check $D = 1$, $c = 2.5$, mean 2.5 and variance 1.975 against $2Dt = 2$ (gap $c^2\Delta t\,t = 0.025$). The lessons state the drift term; this item makes the learner derive it.
- Rubric: 1, 3 (required: the equation and its coefficients), 4 (scaling and bounds), 2 (check). Leave out the scaling row and the most a learner can score is 6, so the pass is lost.
- Gates:
  1. `cd app && node tools/validate.mjs`: 0 errors. Only the expected "remove from perf-pending" warning.
  2. `VOICE_BASE=app/content/courses/pdes python3 docs/reviews/voice-scan.py 35`: 0 and 0.
  3. `python3 -I docs/reports/pdes-1-perf-numbers.py`: exits 0. 77 checks with sympy in the venv; 63 without it, when the symbolic half is skipped.
  4. `node tools/playthrough.mjs --set pdes/homework-1 --local-cdn <pkgs>`: All passed, with and without `--mobile`. Two displays were split with `aligned` after a 356 px render showed them clipped.
- Freshness grep: lazy, stays, `p - q`, `p + q`, 0.004, 0.45, 0.35, 1.975, `u_{tt}`, `u_{xxx}`, remainder. No walk item is repeated.
