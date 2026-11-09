# integrals level 1: performance task (PLAN 2a Phase 3 retrofit)

- File: `app/content/courses/integrals/homework-1.json`, item `h-derive-falling-area`, index 8 (item 9 of 9; the homework had 8, nothing converted).
- Kind `derivation` (longform, empty box), difficulty 5, skill `in-area`.
- Matched objective: l2 "Derive the exact area under $x^2$ on $[0, 1]$ from the limit of its sums." It is the only L1 objective that starts with derive, prove, write, build or code.
- Task: $\int_1^3 (9 - x^2)\,dx = \tfrac{28}{3}$ from Riemann sums: (a) a sum reduced to a formula in $n$, (b) its limit, (c) why the limit is the area and which sum is too big, (d) $R_4 = 7.25$, $L_4 = 11.25$ checked.
- Rubric 2, 3, 2, 2, 1; rows 2 to 5 `required`, one per named part (8 points). `rubric-passes.mjs`: the only minimal pass is rows 2 to 5; only row 1 (set-up) can be left out. Rows accept right or left sums, a split into 9 less $x^2$, and the squeeze, the gap $\tfrac{16}{n}$ or the continuous-function rule for (c).
- Overlapping screens: l2 screen 2 ($x^2$ on $[1, 3]$, the gap only), l2 screens 3, 4 and 7 (right and left sums of $x^2$ on $[0, 1]$ and the squeeze), l2 screen 5 ($1 - x^2$, which sum is too big), l2 screen 6 (the gap for a monotone $f$), `h-recip-right` (also on $[1, 3]$), `h-square-02`, `h-cube-limit`, `h-auction-ramp`, `r-left-line`. New: a falling function, so the right sum is the lower one; an interval not starting at 0, so $\sum k$ enters; the sum reduced from a blank box; both bounds or the gap; the $n = 4$ check.
- Freshness grep (course folder, every hit read): `9 - x^2`, `9 - x`, `4 - x^2`, `n(n+1)}{2}`, `sum_{k=1}^{n} k`, `[1, 3]`, `28`; `fresh-check.mjs --file` 0 hits (0 on the item at `--min-run 8 --min-share 0`).

## Gates

1. `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors; expected warning "integrals/L1: has a performance task, remove from perf-pending". Manifest restored before commit.
2. `VOICE_BASE=app/content/courses/integrals python3 docs/reviews/voice-scan.py 35`: 1 sentence over 35 and 3 explanations over three sentences, all present at the base commit and none in the new item (l1 screen 7 prose, 36, a display splitting two sentences; homework-4 item 2, l16 screens 6 and 11). Not edited: this pass adds one item only.
3. `<venv>/bin/python -I docs/reports/integrals-1-perf-numbers.py`: exit 0, 192 checks. Exact Fraction sums against the closed forms for $n < 200$, sympy summation and limits, float sums, scipy `quad`; passing tick sets listed.
4. `node tools/playthrough.mjs --set integrals/homework-1 --local-cdn <pkgs>`, with and without `--mobile`: All passed, 2 longform marked by the button. Model shot at 1280 and 440 px: 6 display equations, none scroll sideways, no page errors.

No backlog bullets. No course.json change.
