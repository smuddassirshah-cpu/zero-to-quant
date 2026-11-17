# Fix pass: review-pass8-hits, group 2

Sets: `limits/problems-3`, `stat-learning/problems-2`, `-3`, `-4`, `testing/problems-3`, `-4`, `trig/problems-1`, `-2`. No key was changed. Bands changed: `trig/problems-1` `p-desk-lamp` part 3 `ratio-tan` 0.0005 to 0.051; `trig/problems-2` `p-water-wheel` part 2 `wrong-way` 0.05 to 0.005; `testing/problems-3` `p-fund-managers` part 1 `over-root` 0.3 to 0.108 and `times-t` 8.1 to 13.5 (bands 0.0005 unchanged).

- List A row 3 (`trig/problems-1` `p-hexagon-tile` `half`): stands, no edit.
- List A row 4 (`p-desk-lamp` `ratio-tan`): fixed, `tol.abs` 0.051 and the line "You gave a ratio, not the angle: ...". Band [0.699, 0.801] takes 0.7, 0.75, 0.8 and refuses 0.6, 0.6435, 36.87, 53.13, 48.59 (checked in the trig numbers script).
- List A row 20 (`p-water-wheel` `wrong-way`): fixed, `tol.abs` 0.005. Takes 0.039 and 0.04, refuses 0, 0.1, 2.25, 128.92, 405 (checked in script).
- Row 9 (`testing/problems-3` `p-fund-managers`, renumber 0.54 over 25 years): fixed. Prose, part 1 correct, `over-root` and `times-t` lines, explain, values 0.54/5 = 0.108 and 0.54 x 25 = 13.5, key 2.7 unchanged. Parts 2 and 3 hold (t = 2.7). Grep of `testing` and the exams: no Sharpe of 0.54, no 25-year record with a Sharpe (l11 has "25 years" once, as a no-skill standard error). The stock line "You doubled the tail." stays, so the exam-reuse warning on `s-sharpe-p` may still fire: needs the waiver the review lists.
- Row 10 (`testing/problems-4` `p-bakery-loaves` part 2): fixed, `no-divide` and `over-observed` lines as written (256 = 4 x 64; 64/50 + 64/40 + 64/20 + 64/40 = 7.68).
- Row 14 (`limits/problems-3` `p-relative-strength` part 2 `rates`): fixed (2.1/75 = 0.028).
- Row 15 (`stat-learning/problems-2` `p-rent-ridge` part 2): fixed `subtracted` and `on-top` (90/80 = 1.125, 110/100 = 1.1, 90/120 = 0.75).
- Rows 16 and 17 (`stat-learning/problems-3` `p-price-spikes` part 2): fixed, `swapped` line (18,000/24,000 = 0.75; 6,000/24,000 = 0.25). Row 16 cleared by it.
- Row 18 (`stat-learning/problems-4` `p-order-sizes` part 3): fixed `unsquared` (12) and the `averaged` line (40/6 = 6.67), both as the reader wrote.
- Row 26, 30 (`stands`): no edit.

## Gates

- Number scripts exit 0: `problems-testing-numbers.py` (updated to 0.54 over 25 years, three values), `problems-limits-numbers.py`, `problems-stat-learning-numbers.py`, `problems-stat-learning-numbers-read.py`, `problems-trig-numbers.py` (two band checks added).
- Validator: 0 errors; the fixed rounding-tie and wide-wrong-tol warnings no longer print for these sets (remaining warnings on them are other rules, not in this review's fix list).
- Voice scan 35: 0 and 0 for limits, stat-learning, trig. Testing prints 1 sentence over 35 words, `testing/homework-3.json` items.8.widget.prompt, a file not edited here.
- `fresh-check.mjs`: 0 hits on all 8 sets (advisories only).
- `grade-all.mjs --file`: 0 failures on all 8 sets.
- Playthrough with and without `--mobile`: All passed on all 8 sets.
