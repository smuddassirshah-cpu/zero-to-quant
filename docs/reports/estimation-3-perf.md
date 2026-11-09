# estimation level 3: performance task

- `homework-3.json` item `h-bump-interval`, index 8 (9 of 9; appended, nothing converted). Kind `code` (Python, standard library), difficulty 4.
- Matched objective: l10 "Build a 95% confidence interval and say exactly what the 95% means." (chosen over l11's bootstrap, which `h-bootstrap-code` already grades).
- Task: delays uniform on $[0, \theta]$, independent. `bump_interval` returns the exact equal-tailed interval from the maximum, $M/(1 - a/2)^{1/n}$ to $M/(a/2)^{1/n}$; `bump_coverage` replays seeded trials and returns the share that contain $\theta$ (exactly `level`).
- Tests: 9 hidden, 1 example. Thirteen planted slips fail (shortest interval, $a$ not halved, ends swapped, power $n$, last delay, normal approximation, misses counted, count returned, draws on $[0, 1)$, reseeding); four valid variants pass.
- Overlapping screens: l10 screens 1, 2, 7, 8 (z interval, coverage by simulation); l11 screens 4, 9 (bootstrap code; the maximum misleads it); `h-bootstrap-code`, `h-long-trader` (b). New: the uniform model, the pivot $M/\theta$, an asymmetric interval exact at every $n$, coverage in code.
- Freshness grep, hits read: `uniform`, `largest`, `max(`, `coverage`, `random.Random`, `speed`, `1 / n`. `fresh-check.mjs --file`: no hit on the item.

Gates:
1. Validator, `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors, expected perf-pending warning; manifest restored.
2. Voice, `VOICE_BASE=app/content/courses/estimation python3 docs/reviews/voice-scan.py 35`: 0 and 0.
3. Numbers script, `<venv>/bin/python -I docs/reports/estimation-3-perf-numbers.py`: exit 0, 73 checks (two routes per test, sympy coverage, seeded simulation, endpoint margins).
4. Playthrough, `node tools/playthrough.mjs --set estimation/homework-3 --local-cdn <pkgs>`, with and without `--mobile`: All passed, starter fails; shots clean.

Backlog: 0 bullets. No course.json change.
