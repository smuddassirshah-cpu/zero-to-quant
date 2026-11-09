# research-int level 2: performance task (PLAN 2a Phase 3 retrofit)

- File: `app/content/courses/research-int/homework-2.json`, item `h2-pca-aloud`, index 8 (item 9 of 9; nothing converted, the cap is 12).
- Kind `aloud`, difficulty 5, skills `rq-ml`, `rq-linalg`, 120 s clock, pace 420, three follow-ups.
- Objective matched: l9 "Explain what principal components are, how to choose how many, and when they mislead." l6 and l7 also match, but the homework already carries a written bias-variance answer (`h2-bv-longform`) and two lasso items, so PCA gives the freshest product. The task asks for all three parts, on a new 50-stock case where an 80% rule keeps 23 components.
- Rubric 3, 3, 3, 1. Row 2 (how many: noise edge 1.73, three real, 20 kept are noise, choose by held-out error) is `required`.
- Freshness grep over the course folder: `50 stocks`, `500 days`, `20.6`, `1.73`, `noise edge`, `80%`, `sell-off`, `1 + 49`, `loadings`, `rolling`. Hits are l9 screens on the noise edge idea (other numbers) and l4 power at 80%; nothing repeats.

## Gates

1. `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors; expected warning "research-int/L2: has a performance task, remove from perf-pending".
2. `VOICE_BASE=app/content/courses/research-int python3 docs/reviews/voice-scan.py 35`: 0 and 0.
3. `python3 docs/reports/research-int-2-perf-numbers.py` (venv): exit 0; shares, the 23-component count, the edge (formula and seeded simulation), the scaled bar 0.88, $1 + 49\rho$ (formula and eigvalsh), rubric and homework shape.
4. `node tools/playthrough.mjs --set research-int/homework-2 --local-cdn <pkgs>`, with and without `--mobile`: All passed. Shots at 440 px read: no sideways scroll.

No backlog bullets. No course.json change.

Overlapping screens: l9-pca-questions screens[0] and [1] (the first and second components), [3] (keep 90%?), [5] (noise has eigenvalues too), [6] (say it aloud), [8] (the yield curve) and [9] (how many components do you keep), homework-2 `h2-pca-table` and `h2-pca-parts`; new parts: one spoken answer to all three questions on a 50-stock case where an 80% rule keeps 23 components, the noise edge 1.73, three real components, 20 kept ones that are noise, and choosing by held-out error.
