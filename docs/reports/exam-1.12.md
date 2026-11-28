# Topic exam 1.12 (Neural networks from scratch)

`app/content/exams/topic-1.12.json`, built by `docs/briefs/exam-1.12-scripts/build.py`. 30 items at a ramp of 6, 15, 6 and 3. It has 7 items with parts and 2 code items. `minutes` is 100 (paces add to 92 min) and `pass` is 0.7. All 16 skills are on 2 to 4 items each.

Exit: items[21] asks for entropy and KL in bits for a pair. items[28] is a backward pass by hand in NumPy, checked by central differences below 1e-6. items[29] gives the bigram's dev loss (2.4514) against the MLP's (2.1609).

The code items carry 8 and 7 mutants, and each first fails its named test. Every `byKey` line is reachable. Of my own 14 variants, 3 pass by design (rounding, an equivalent formula), test 11 closes 1, and 10 fail.

Checks: validator 0 errors. Voice scan 0 and 0. `check_numbers.py` passes strict through the runner (853 checks, 0 uncovered). Fresh-check gives 0 hits, and same-course reuse names no exam error. `grade-all --code` has 0 failures. Playthrough is green, plain and `--mobile`.

Near twins: items[22] and [26] follow info problems-3 and makemore problems-1, with new data.
