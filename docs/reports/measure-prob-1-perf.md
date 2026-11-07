# measure-prob level 1: performance task (PLAN 2a Phase 3 retrofit)

- File: `app/content/courses/measure-prob/homework-1.json`, item `h-build-space`, index 8 (item 9 of 9; nothing converted, the homework had 8 items).
- Kind `derivation` (longform, empty box, no tags), difficulty 5, skill `mt-sigma`.
- Objective matched: l3 "Build a probability space and prove continuity from above and below." It is the only rule-matched objective in the level.
- Task: build the space on the positive integers with $p_k = 1/(k(k+1))$, prove it is a probability measure (sigma-algebra, telescoping total, countable additivity by finite partial sums), prove both continuity results for any measure with their hypotheses, then find $P(\{n, n+1, \dots\}) = 1/n$ and its limit.
- Rubric 2, 2, 3, 2, 1. Row 3 (continuity from below) is `required`. Rows 1 and 4 open with "Tick only if".
- Overlap (fix pass): the continuity proofs repeat l3 screen 5 and `h-order` because the objective names them; the space and its additivity proof are the fresh part. Rows 2 and 3 are `required` (additivity of $P$, continuity from below).
- Fresh: the lessons and homework prove continuity on general sets (l3 order screen, `h-order`, `h-long`) and use length, uniform picks and counting measure (`r-counting`). The space, its additivity proof and $1/n$ tails are new. Grep terms: `k(k+1)`, `telescop`, `counting measure`, `positive integers`, `whole numbers`, `{n, n+1`.

## Gates

1. `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors; expected warning "measure-prob/L1: has a performance task, remove from perf-pending".
2. `VOICE_BASE=app/content/courses/measure-prob python3 docs/reviews/voice-scan.py 35`: 0 and 0.
3. `python3 docs/reports/measure-prob-1-perf-numbers.py` (venv with sympy): exit 0, 4,305 checks. Fractions against closed forms, brute-force finite additivity, residue-class partitions with tail bounds, sympy sums.
4. `node tools/playthrough.mjs --set measure-prob/homework-1 --local-cdn <pkgs>`, with and without `--mobile`: All passed (2 longform marked by the button). The 440 px shots were read. There are no display equations; the known coach tip covers the header (ENGINE-BACKLOG 683).

No backlog bullets. No course.json change.
