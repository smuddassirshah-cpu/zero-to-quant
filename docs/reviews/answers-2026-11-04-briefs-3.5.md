# Answer check, topic 3.5 briefs, fix-pass changes (4 November 2026)

Independent recomputation of every keyed answer, test expectation and stated number that the fix passes added or changed in `docs/briefs/research-int.md`, `systems.md` and `coding-int.md`. The authors' and fixers' scripts in `docs/briefs/*-scripts/` were not used. Briefs not edited.

## Scope

| Brief | Diff range | Changed lines | Items checked |
| --- | --- | --- | --- |
| research-int | `28bceed..HEAD` | 77 (word-diffed) | about 45: 12 stated numbers recomputed with NumPy 2.5.3, SciPy 1.14.1, scikit-learn 1.6.1, statsmodels 0.15.0 (duplicated-data t and p, mse_divisor and best_divisor cases, z and p, boosting rounds, forest importances and seeds, PCA eigenvalues, weak-signal t curve and n, `futures-daily.csv` leak row counts and correlations, `spread-daily.csv` baselines and AR(1) figures, `houses.csv` coefficients, standard error, VIF, bootstrap ends, `ticks-gaps.csv` row counts and interpolated price, stable slope, `towns-temp.csv` Wick slope); the six data files are byte-identical to the authors' (md5), so the data were not regenerated independently |
| systems | `28bceed..HEAD` | 172 | 18 C++ problems and drills rebuilt from the brief text (reference and starter against every stated test, g++ `-std=c++20 -O1 -fno-exceptions`, 193 test rows in all), with the alloc-counting harness stood in; claimed test counts and starter fail counts for all 18; E13 counts (U6, U7, broken ring, U11, 34,650), cache-set and sweep figures, branch-predictor run (5,064 and 2), SB outcomes, review and homework keys (frames, ring slots, mean and p99, sizing, pooled p99) |
| coding-int | `44c1d93..HEAD` | 609 | 138 added table rows run through an independent oracle (Python, brute force or closed form); all 41 Python problems' reference and starter run against their printed rows (claimed fail counts compared); C++ pairs for 1.1, 4.1, 10.1, 11.1, 17.1 and H4.3 (references pass, starters fail, non-normalised `%` variant returns 1 not 3 on case 9); 16.1 mutants and coverage table; 16.2 testkit stand-in (model solution passes, every bug caught, starter fails 4 of 6); about 70 lesson, review and homework keyed numbers (window maxima, medians, heap sizes, strategy, LRU, TTL, file system, limiter, bucket, calendar, plan DP, counts) |

## Mismatches

| Brief | Location | Stated | Recomputed | Which is right |
| --- | --- | --- | --- | --- |
| coding-int | Problem 6.1 header, starter fail count | "fails 4 of 8" | 3 of 8 (rows 1, 7, 8). After the fix changed rows 1 and 2, the exact-copy starter passes row 2 (`'babcab'`, `'bab'` gives `[0]`) | Recomputed; the count is stale |
| coding-int | Problem H2.3 header, starter fail count | "fails 5 of 10" | 6 of 10 (rows 2, 4, 5, 6, 8, 10). Row 2 changed to `')(()())('` (expected 6), which `count('()') * 2` now fails | Recomputed; the count is stale |
| systems | Level 4 homework item 2(e) (`feed-handler-design`) | "does it fit a 32 KiB L1, yes" | The pool alone is 36,000 bytes (above 32,768); pool plus ring is 42,144 bytes (41.2 KiB). Only the 6,144-byte ring fits | Recomputed unless (e) is meant for the ring alone; the item does not say, so key or wording needs fixing (the line was touched by the fix pass, the sentence predates it) |
| coding-int | Problem 15.1 row 10 layout | Row shows `...; ps.append([...]); best_plan(ps, 600)` with the call indented inside the `for` body | The call runs 60 times inside the loop. The value after the loop is 2724 (matches the stated expectation by independent memoised recursion) | Value right; row as printed is ill-formed for a "setup; call" split (call must be dedented) |

No numeric mismatch was found in any other changed item.

## Choice items: key visibly longer than distractors

| Brief | Item | Observation |
| --- | --- | --- |
| research-int | Level 4 lesson l14 (and its homework twin) bedrooms item: "its standard error is about 2.4, so 9 is within one error, and collinearity with area (r = 0.76) is why the error is that large" | Key about 25 words; the only distractor given ("collinearity biases the coefficient down, a typo price") is a fragment. Key is clearly the longest and the most hedged |
| research-int | R4.4 groupby expression | Key is a 90-character lambda; listed distractors are 3 to 6 words each. Obvious by length |
| coding-int | Review-4 item 8 (`longest_zero_sum_subarray` tests) | Key `[6, -2, 1, 1, 7, -3, -4, 5]` (8 values) against `[2, -2, 2, -2]`, `[0, 0]`, `[1, 2]`. Longest by a wide margin; inherent to the question but a tell. Consider distractors of similar length (for example `[4, -4, 3, -3, 5, -5, 2, 7]`) |
| coding-int | l17 screen 7 (first or latest sighting) | Key is given with its rationale ("The first: the longest stretch starts at the earliest sighting ..."); distractors are one to two words. Fine if only "the first sighting" becomes the option text; author should keep the rationale out of the option |
| systems | Homework 2 item 2 and others changed to `parts` | Option texts are not listed in the brief, so length could not be compared |

## Notes

- research-int, forest importances: the stated 0.47, 0.47, 0.03, 0.03 (impurity) and 0.37, 0.39, 0.00, 0.00 (permutation) reproduce only with the draw order x, integer noise column, normal noise column, then the residual noise e (0.467, 0.469, 0.032, 0.032; 0.373, 0.387). Other orders give 0.46, 0.48 and 0.374, 0.396. The brief says "do not regenerate; paste the arrays" and lists the construction without the draw order, so a level agent rebuilding it may get digits that round differently. State the order or the printed arrays. The noise-sd-1 figures (about 0.39, 0.41, 0.10, 0.10) hold.
- research-int, bootstrap ends: seed 99 gives 24.87 and 34.22 exactly as stated; seeds 1 to 4 give 24.9 to 25.1 and 34.1 to 34.3, consistent with "about £25k to £34k". Paired t 6.28, gain 6,353.7, interval 4,486.9 to 8,445.0 confirmed. VIF: 2.40 on the training pair (1.549 root) and 2.43 (1.56 root) on the full model, as the added note says.
- research-int, `spread-daily.csv`: out-of-sample R² -0.0091 confirmed; its delta-method standard error is 0.020, matching "about 0.02". True coefficient 0.06 is in `gen_data.py`.
- systems: all 18 problems pass every reference test and fail the stated starter counts (test counts 15 for P-struct-size, 13 for P-find-gaps, 12 for P-lock-cycle and 10 for P-cache-sim confirmed after the fix-pass edits). P-format-price starter fails 6: five on text and the `alloc_count()` one, as stated. The brief's sorted-branch figure of 2 and random figure of 5,064 need the update-then-use order of the LCG (use-then-update gives 5,063); the brief states the order correctly.
- systems: the checks used the g++ in this sandbox, not the app's clang 21 (as the brief itself says), and a stand-in `alloc_count()` harness. The P-format-price text failures were confirmed at `-O1` only.
- coding-int, C++ timing: the H4.3 starter took 40.9 s on case 10 here against the stated 25.96 s (hardware differs; 8 times the 5 s limit against "about five times"). The 17.1 starter did not finish in 40 s here (stated "not finished after 60 s"). Both are far past the limit, so the design holds; the exact figures are machine-bound.
- coding-int, 16.1 trap: "lengths from 0 to 10 about one list in twelve is empty" is 1 in 11 for uniform lengths. Harmless. Random lists of length 5 to 50 miss `m2` in 100 of 100 trials of 1,000 lists, as stated.
- coding-int, claimed `fails n of m` counts that match: 3.1 (9 of 11), 4.1 (2 of 7), 4.2, 5.1, 5.2 (5 of 8), 7.1 (2 of 15), 14.2, H1.1 to H1.4, H2.1, H2.2, H3.1, H3.2, 11.1 C++ (6 of 7), 1.1 C++ (6 of 10), 10.1 C++ (10 of 12), calendar stages (4 of 6, 7 of 8, 11 of 13).
- Row 7 of Problem 5.1 (`single_number(xs)`, 54321) was not in the oracle; it is the XOR of every value and equals 54321 by construction.
