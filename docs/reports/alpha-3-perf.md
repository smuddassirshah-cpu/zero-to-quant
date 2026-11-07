# alpha level 3: performance task

- `homework-3.json` item 9 of 9, `h-overlap-aloud`, appended (cap 12, nothing converted). Kind `aloud`, difficulty 5, pace 480 s, think 30 s, clock 120 s, three follow-ups.
- Objective (l9): "Explain why overlapping dates inflate the t statistic." The only L3 objective the verb rule matches.
- Why `aloud`, not `derivation`: the verb is explain (Stage 2), and the product is a chain of reasons a manager hears. The written variance calculation is already ordered in l9's derive screen and coded in `h-newey-west`; the model still derives it, each line justified.
- Rubric 2, 3, 2, 2, 1; row 2 (variance of the mean about 63 times $s^2/n$, standard error $\sqrt{63}$ too small) is `required`.

Gates:
1. `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors (expected perf-pending warning).
2. `VOICE_BASE=app/content/courses/alpha python3 docs/reviews/voice-scan.py 35`: 0 and 0.
3. `<venv>/bin/python docs/reports/alpha-3-perf-numbers.py`: exit 0. Closed forms against window counting and a seeded simulation (4,000 paths): correlation $1 - k/63$, variance factor 61.2 (63 before end effects), $\sqrt{63} = 7.94$, honest $t$ 1.20; finite-sample route gives 1.13, so "about 1.2".
4. `node tools/playthrough.mjs --set alpha/homework-3 --local-cdn <pkgs>` with and without `--mobile`: All passed. Display equation 265 px wide in a 356 px column at 440 px (scratch KaTeX render).

Freshness: `fresh-check.mjs --file` 1 hit, existing item 1 (`h-t-36`). Grep of 756, 9.5, value signal, 63-day, 62 of, 62 lags: no lesson or review hit.

Backlog: 0 bullets.
