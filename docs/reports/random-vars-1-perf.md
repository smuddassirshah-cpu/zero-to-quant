# random-vars L1 performance task

- File: `random-vars/homework-1.json`, item `h-build-pmf` appended (index 8).
- Kind: `code`. Matched objective: l2 "Build a probability mass function and check that it sums to one."
- Task: `pmf_of(space, X)` from a stub, for unequal chances, raising `ValueError` on a negative chance or a total off 1 by over `1e-9`.
- Tests: 10 hidden, 1 example; the starter fails all 10; 11 planted bugs each fail one or more.
- Overlapping screens: l2 screens 0, 3, 4, 6, 7, 8; l4 screens 2, 3, 6; l5 screen 8 (a pmf dict). New: code from blank, unequal chances, both checks under float rounding, chance-0 values, four new variables.
- Freshness grep: `pmf_of`, product, longest run, spinner, without replacement, `ValueError`; `fresh-check --file`: no hit.

## Gates
1. Validator `node tools/validate.mjs`: 0 errors.
2. Voice `VOICE_BASE=app/content/courses/random-vars python3 docs/reviews/voice-scan.py 35`: 0 and 0.
3. Numbers script `python3 -I docs/reports/random-vars-1-perf-numbers.py`: 109 checks, exit 0 (two exact Fraction routes, seeded simulation).
4. Playthrough `--set random-vars/homework-1 --local-cdn <pkgs>`, with and without `--mobile`: All passed; starter docstring split for 440 px.

Backlog: 2 bullets.
