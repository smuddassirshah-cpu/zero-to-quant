# analysis level 1: performance task (PLAN 2a Phase 3 retrofit)

- File: `app/content/courses/analysis/homework-1.json`, item `h-prove-binary-dense`, index 9 (item 10 of 10; the homework had 9, nothing converted).
- Kind `derivation` (longform, empty box), difficulty 5, skill `an-reals`.
- Matched objective: l4 "Prove the Archimedean property and that the rationals are dense in the reals." It is the only objective of the level that starts with prove (l1, l5 show; l2 find; l3 state).
- Task: (a) from completeness alone, $\{2^k\}$ has no upper bound; (b) binary fractions $m/2^k$ are dense, with $k$ chosen from (a) and the least integer $m$ above $2^ka$ shown to exist; (c) $a = 1/3$, $b = 0.34$: the proof's $k = 8$, $m = 86$, and the smallest $k$ is 7.
- Rubric 3, 2, 3, 1, 1. Rows 1 to 4 `required` (9 points): one each for (a) and (c), and both rows of (b). `rubric-passes.mjs`: the only minimal pass is rows 1 to 4; row 5 (the smallest $k$) can be left out.
- Overlapping screens: l4 screens 1 to 4 (the Archimedean property from completeness, with $s - 1$), l4 screens 6 to 8 and 10 (the density recipe $n > 1/(b - a)$, $m = \lfloor na \rfloor + 1$), `h-density-root`, `r-density`, `r-inf-proof`, l1 quiz 3 (floats hold $m/2^k$). New: halving $s$ (needs $s > 0$), a power-of-two grid chosen from (a), the least integer proved to exist rather than the floor, and the smallest $k$ against the proof's.
- Freshness grep (course folder, every hit read): `dyadic`, `binary fraction`, `2^k`, `0.34`, `150`, `\inf`, `least element`; `fresh-check.mjs --file` 0 hits.

## Gates

1. `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors; expected warning "analysis/L1: has a performance task, remove from perf-pending". Manifest restored before commit.
2. `VOICE_BASE=app/content/courses/analysis python3 docs/reviews/voice-scan.py 35`: 0 and 0.
3. `python3 -I docs/reports/analysis-1-perf-numbers.py`: exit 0, 3,044 checks. $k$ by counting and by bit length, $m$ by floor and by the proof's finite search, on 3,000 random pairs; (c) in Fractions and floats; brute force over every numerator for $k \le 8$; passing tick sets listed.
4. `node tools/playthrough.mjs --set analysis/homework-1 --local-cdn <pkgs>`, with and without `--mobile`: All passed, 2 longform marked by the button. 440 px shots read: no display equations, nothing past the gutter.

No backlog bullets. No course.json change.
