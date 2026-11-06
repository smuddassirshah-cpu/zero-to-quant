# mock-oa-strats: second-reader findings

Scope: `app/content/exams/mock-oa-strats.json` (two papers and two checks: `code` 30 min, 2 Python `code` items, `pass: 0.5`; `maths` 22 min, 8 `choice` items, `pass: 0.625`; checks `no-calculator` and `no-lookup`), read in full against `docs/briefs/mocks.md` (`### Shared rules for the mocks` and `## mock-oa-strats`), `docs/reports/exam-mock-oa-strats.md`, `docs/AUTHORING.md` section 5 (mock assessment, paper fields, mock pass marks), the `code` widget section and section 6, `docs/briefs/interview-gaps.md` row "Goldman Sachs, strats summer analyst", `content/prep.json` paths `oa-strats` and `firm-goldman-sachs`, and the engine's per-case limit (`widgets/code.js`: 5 s plus the case's `budget`, setup included).

Method: recomputed every key and every distractor by my own route (central difference, trace and determinant, `expm1` quotient at $10^{-4}$, `Fraction` Bayes, Simpson with 20,000 strips, RK4 with 10,000 steps, enumeration of all 1,680 labelled splits, determinant and smallest eigenvalue of the correlation matrix at 0.27, 0.28 and 0.29); wrote my own reference for each code item (a `defaultdict` for C1, prefix sums with `bisect` for C2) and ran it, the author's solution, the starter and eleven wrong versions on every example and hidden test in CPython, each in its own process with a 15 s cap; timed the author's solution and the borderline versions on the large tests in Pyodide 0.27.7 under node (the scratchpad `pkgs` copy); grepped every setup across lessons, reviews, homework, drills, bank, exams and mocks; scanned voice on every learner-visible string.

Scratch scripts (not committed): `/tmp/claude-0/-home-user-zero-to-quant/563c2e64-8acc-5553-b27e-d47f109c8bd3/scratchpad/rev-oa2/` (`sols.py`, `run_py.py`, `pyo.mjs`, `mkjobs.py`, `voice.py`, `c2_alt.py`).

Format: `n. item [paper, index] path | severity | problem | evidence | fix`. Severities: wrong, misleading, coverage, design, voice, layout.

## Script results

- `python3 -I docs/briefs/mocks-scripts/mock-oa-strats_check.py`: 189 of 189, exit 0.
- Validator (`node tools/validate.mjs`, from `app/`): `0 errors, 3983 warnings`; no line names `mock-oa-strats`.
- `node tools/fresh-check.mjs --exam mock-oa-strats --min-run 10`: 0 hits.
- My recompute: every key and every distractor value agrees (M1 1.5, slips 0.25, 6, $\ln 4$; M2 1 and 6; M3 2.000133 at $10^{-4}$; M4 5/8, 3/8, 5/7; M5 0.264241, slips 0.632, −0.264, −0.736; M6 20.16717 by RK4 and closed form; M7 1/28 from 60 of 1,680 labelled splits, 10 of 280 unordered, one book 1/84; M8 determinant −0.0073 at 0.27, 0 at 0.28, +0.0071 at 0.29). Each `why` names the action that gives its value.
- Code items: the author's solution and my reference pass all 13 and 14 cases. Starters fail 11 of 13 and 10 of 14. Every wrong version fails at least one case: C1 list search (both large cases time out), sell adds (9), zeros kept (4), insertion order (2), sorted by net (5); C2 "more than" (8), brute force with early break and brute force bounded by the best so far (both stop on tests 10 and 12), no-block returns `len + 1` (4), whole list never counted (2). A sort-then-group C1 at $O(n \log n)$ passes, as it should.
- Pyodide timings, author's solution: C1 large cases 0.26 s and 0.27 s including setup; C2 large cases 0.05 s, 0.12 s, 0.16 s. All far inside the 5 s limit, and the quadratic versions run past 15 s in CPython.
- Voice (my scan): 214 sentences, none of 20 words or more, no explanation over three sentences, no exclamation mark, no dash, no American spelling. No firm name outside `models` and `description`; `models` is marked "Reported, as of Nov 2026".

## The brief section

The `## mock-oa-strats` section matches its sources. `interview-gaps.md` gives the 30-minute Software Fundamentals challenge, the 22-minute maths challenge, the one report of 8 multiple-choice items on calculus, linear algebra and probability, and the older 2 coding and 9 maths in 3 hours; the brief marks them "reported, Nov 2026", says no report gives negative marking, a pass mark or a calculator rule, and keeps the firm name to `models`. The mock matches the brief on minutes, items, pass rules, free navigation, `1, 0, 0` scoring, checks, tags, paces and every keyed value.

## What the author's script does not check

- That the large tests stop a slow but correct solution: it times the reference only. I ran quadratic versions of both items (above); both are stopped.
- Freshness of a setup against lessons (finding 1): the literal search covered the maths setups, not the window problem.
- Whether the pass line and the `requires` gate fit the items (findings 2 and 3).

## Findings

1. `c2-fewest-days` [code, 1] `parts[0].items[1]` | design | The problem is the worked example of a prerequisite lesson, so it tests recall, not transfer. | `ds` l6-sliding-window screens 3 and 4 trace "the shortest run of days whose sum is at least 7. Every number is positive."; `ds` review-2 `r-min-window` asks the same for `[1, 4, 2, 3, 5]`; `ds` homework-2 `h-negatives` names "the shortest run of minute volumes summing to at least 5,000 shares", and C2's seeded test is volumes with target 5,000. The brief rewrites reused setups ("Freshness"), and this one was missed because fresh-check matches runs of words, not the task. | Keep the pattern and turn it round: "the most neighbouring days whose volumes add up to at most `limit`". Function `longest_within(volumes, limit)`, `limit` a positive whole number, 0 when every single day is over `limit`. Solution: grow on the right, shrink from the left while the total is over `limit`, keep `right - left + 1`. Keys I computed twice (window and an early-break brute force): `([4, 1, 1, 6, 2, 3], 8)` 3, `([], 5)` 0, `([9], 9)` 1, `([9], 8)` 0, `([1, 2, 3], 6)` 3, `([1, 2, 3], 5)` 2, `([12, 1, 1, 1, 5], 3)` 3, `([3, 3, 3, 3], 7)` 2, `([2, 7, 1, 1, 1, 8], 9)` 3; large `[1] * 200000` with 150,000 gives 150,000, the same seeded `V` with 5,000 gives 99 (also by prefix sums and `bisect`), `[10**6] + [1] * 199999` with 199,999 gives 199,999. The early-break brute force needs about $10^{10}$ steps on the first and last large cases. Rename the tag (`longest-within`), the title, the explanation and the brief row; the `([9], 9)` and `([9], 8)` pair catches "less than" in place of "at most". Recheck with the build script before committing.
2. `code` paper [code] `parts[0].pass` | design | `pass: 0.5` lets a learner pass the coding paper on the difficulty-2 dictionary task alone, so the window problem and its large tests never decide the result. | C1 is difficulty 2 with a 720 s pace; C2 is difficulty 3 with 960 s; the paper is 30 minutes. `mock-oa-code` sets `pass: 1` for two harder problems in 60 minutes. | Either set `pass: 1` (both problems; the paces sum to 1,680 s of 1,800 s, so tighten them to 600 and 900 if the line feels harsh) and say in `description` that the line is illustrative, or keep 0.5 and add "You pass the coding paper with one problem of the two." to `description` so the learner knows the bar. Change the brief's parts table to match.
3. top level `requires` | design | The gate is `eigen/L1`, but M8 needs positive semidefinite correlation matrices, which `eigen` teaches in level 2. | `eigen/course.json`: level 1 is l1 to l4; l7-covariance-psd is level 2. The brief cites l7-covariance-psd as M8's prerequisite. A learner who has only met the gate meets M8 cold. | Set `"requires": ["ds/L2", "eigen/L2"]` and change the brief's `requires` line and its "(cited; `requires` gates only ...)" sentence to match.

## Notes (no change needed)

- The `oa-strats` path in `prep.json` lists `series/level-3` because "Binomial expansions turn up in maths multiple choice". No item uses the binomial theorem; the brief takes it from the older reports only, and the 2026 report's three areas are all covered. Leave as is unless a ninth family is wanted later.
- The engine shows the checks after the papers; `no-calculator` covers only the maths paper, which the label says.

Counts: wrong 0, misleading 0, coverage 0, design 3, voice 0, layout 0 (layout not checked: no screenshots taken; the report's 1280 and 440 px screenshots were not reread).

## Fix pass

- 1 fixed. `c2-fewest-days` replaced by `c2-longest-within`, `longest_within(volumes, limit)`: the most neighbouring days with a sum of at most `limit`, 0 when every day is over. Twelve tests (9 small, 3 large), keys as the reviewer gave them, each recomputed by a window, by prefix sums with `bisect` and by an all-runs brute force: 3, 0, 1, 0, 3, 2, 3, 2, 3, then 150,000, 99 and 199,999. Planted wrong versions ("less than", shortest in place of longest, days under the limit, no window moves left) each fail at least one test; the starter fails 10 of 12. Title, tag, question, feedback, explanation and brief row renamed; the brief's "catches" sentence rewritten.
- 2 fixed. `parts[0].pass` is now 1 (both problems), so the difficulty-2 item alone cannot pass the code paper. The description says the line is illustrative. The pace sum stays 1,680 s of 1,800 s. Brief parts table updated; the check script asserts it.
- 3 fixed. `requires` is `["ds/L2", "eigen/L2"]`; the brief's `requires` line and "cited" sentence updated; the check script asserts it.

Gates: validator 0 errors, no line names `mock-oa-strats`; voice scan on the learner strings 0 sentences of 20 words or more and 0 dashes or exclamation marks (one 20-word explanation sentence was shortened); `mock-oa-strats_build.py` ALL AGREE and `_check.py` 193 of 193, exit 0; `fresh-check --exam mock-oa-strats --min-run 10` 0 hits; playthrough green with and without `--mobile` (10 of 10, passed); `readiness-sums.mjs` OK.
