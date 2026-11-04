# Topic 3.5 exams: second-reader findings

Scope: `app/content/exams/mock-oa-code.json` (with the eight `oa` drills), `mock-superday-research.json`, `mock-oa-quant-data.json` (with `app/content/data/qd/`) and `topic-3.5.json`. Read only. Arithmetic is covered by the answer checks and is not repeated.
Method: every file read in full; hidden tests, starters and conventions read against the engine's comparison code (`code.js` `__zq_cmp`, `numeric.js`, `grade.js` `parseNum`); the mocks compared with `docs/briefs/mocks.md`, `docs/reports/exam-3.5.md`, `docs/reports/prereq-mapping-mocks.md` and the course maps; playthrough run with `--shots --local-cdn` at 1280 and with `--mobile` for each of the four exams (8 runs, all green); a separate script played each exam through the test hook and took the start card, every item (after Check) and the results page at 1280 and 390 px (the stock playthrough names its start shot `start--1`, which for the superday is the last-part checks page, and photographs the results page mid-animation); voice scan in `docs/reviews/voice-3.5-exams.txt`.

## Counts

| Exam | Items | Authored / drawn | Papers and clock | Pass | Pace sum |
| --- | --- | --- | --- | --- | --- |
| mock-oa-code | 2 drawn (pool 8: four at d3, four at d4) | 0 / 2 | 1 paper, 60 min, 2 checks | 1 of 2 and both checks | 3,000 s of 3,600 |
| mock-superday-research | 18 (22 with parts counted as one each: 4 `parts` items) | 14 / 4 drawn from `bank/probability` (30 candidates) | 45, 30, 45, 45 min, 2 checks | 60, 65, 50, 50% per paper | 2,240, 1,740, 2,700, 2,700 s |
| mock-oa-quant-data | 13 (10 statistics incl. 2 `multi`, 1 `parts`; 3 Python data tasks on 3 CSV files) | 13 / 0 | 40 and 80 min, 1 check | 60% each | 2,280 and 4,500 s |
| topic-3.5 | 30 (13 numeric, 6 choice, 3 multi, 2 order, 1 table, 1 tap-regions, 1 parts, 3 code) | 30 / 0 | 90 min | 70% (21 of 30) | 5,310 s |

Playthrough: all green desktop and mobile. Validator not re-run (other agents write content). Voice: 2 sentences over 20 words, nothing else (see the voice file).

## Findings

Format: file | item | severity | finding | fix.

### Realism and timing

1. mock-superday-research | papers 3 and 4, and paper 2 | warning | `pace` sums equal the clock (coding 2,700 s of 2,700 s, case 2,700 s of 2,700 s, ML 1,740 of 1,800). The clock also pays for Pyodide loading and for typing a 250-word answer, so a learner working at pace fails the paper. `mock-oa-code` leaves ten minutes spare; the others do not. | Cut pace by about 10% on C1, C2, K1 and K2 (for example 1,350, 1,080, 1,080, 1,350), or raise the two papers to 50 minutes and say so in the description.
2. topic-3.5 | whole exam | warning | Pace sum 88.5 of 90 minutes and it holds three code items, one of them C++ (compiler load is long). Other topic exams with code run 60 to 90 minutes for 25 to 30 items with no pace sum. A learner at pace has 90 seconds spare. | Raise `minutes` to 100, or trim the code paces (480, 480, 600) by a quarter.
3. mock-oa-code | description, `models` | note | "Two problems in 60 minutes" is the JP Morgan-style format; Two Sigma's online test is reported as more problems in a longer slot. The `models` line lists three firms as one format. | Add to the description: "Other reports give three or four problems in 70 to 90 minutes." Keep the mock as is.
4. mock-oa-code | paper `pass` | note | `pass: 0.5` passes with one problem of two, while the description says the second is harder and a reported platform needs most test groups on both. The stated plan was one of two, so this is a choice, not a bug. | Keep, or set `pass: 1` so that the mock passes only on both, which matches how l15 and l17 teach planning. Decide once and say it in the description.
5. mock-superday-research | `models` | warning | One 27-word sentence with two colons; the brief asked for two sentences under 20 words. Voice scan flags it (it is shown on the start card). | "Reported, as of Nov 2026: quant research final rounds at Two Sigma, Citadel and JP Morgan. They cover probability and statistics, machine learning, coding and an open prediction case."
6. mock-superday-research | m6-boosting-round explain | note | 21-word sentence. | "Splitting after the second point leaves a residual sum of squares of 10, against 40.7 and 26 elsewhere."
7. mock-superday-research | k1 and k2 rubrics | warning | The mock forbids a calculator, but the rubrics award 2 of 10 points for "standard error 1.58 and z about 1.45" (k1) and for "t of 1.27" with an interval of -0.02 to 0.10 (k2). A candidate cannot take $\sqrt{998}$ or a Fisher transform by hand. The model answers are fine; the marks reward calculator output. | Reword the rubric lines to the reasoning with an approximate figure: "Gives the standard error as about 1.6 points and z as about 1.5"; "Gives t as about 1.3, below 2". Keep the exact values in the model answer only.
8. mock-oa-quant-data | q1 to q10 | note | Realism is good: ten items in 40 minutes with two `select all` items, then three data tasks in 80 minutes. Difficulty ramps 2, 2, 3, 3, 3, 3, 3, 4, 4, 5. No change. | None.

### Grading of alternative correct forms and tolerances

9. mock-superday-research | m1-ridge-shrinkage | warning | Answer 1.3333, `tol` 0.001, no number of decimals asked. "1.33" (a normal interview answer) is marked wrong with no `byKey` match; "4/3" is accepted. | `tol: { abs: 0.005 }` (the nearest wrong value is 1.0), and say "to two decimals" in the question or placeholder.
10. mock-superday-research | m4-pca-share | warning | Answer 0.7945, `tol` 0.0005, placeholder "a decimal". "0.79" and "79%" (the share is a percentage in everyday speech, and the unit is not set) are rejected. | Ask "Give four decimals" like q5 and q8 of the other mock, or widen to `abs: 0.005` and accept a percentage with `unit: "%"`.
11. topic-3.5 | e-first-component (16) and e-persistence-gain (25) | warning | Both are `unit: "%"` with `abs: 0.0005` on a fraction, that is 0.05 points. A learner who types "73" (after 72.7) or "20.0" is fine, but "73%" is rejected, and the question does not ask for one decimal. | `tol: { abs: 0.005 }` for item 16 (nearest slip is 0.6364, far away) and say "to one decimal place" on both, or widen.
12. mock-oa-quant-data | q7-portfolio-sd | warning | `unit: "%"`, key 14.2, `abs` 0.05 points, question says only "in %". "14" is wrong; "0.142" (a plausible answer, since the volatilities were given as 20% and 30%) becomes 0.142% and is wrong with no hint. | Ask "to one decimal place", widen to `abs: 0.001` (0.1 point), and add a `wrong` entry 0.00142 with "You typed the fraction. The box takes a percentage."
13. mock-oa-quant-data | q3-t-statistic | warning | The mean is 1.8 and the standard error is exactly 1, so the key equals the given mean. A learner who forgets to divide by anything gets it right. The second `wrong` (9.0) is a slip nobody makes and the check in the explanation is circular. | Use mean 3.0, s = 10, n = 25 (SE 2, t = 1.5), with `wrong` 15 (divided by $s/n$, 3.0 / 0.2) and 0.3 (divided by $s$). Recompute twice. |
14. mock-oa-quant-data | code tasks d1 to d3 | note | Conventions are handled well by the engine: lists, tuples, NumPy arrays and Series compare by `tolist`, so a returned array or a tuple is accepted, and `raises` accepts subclasses. Data order is checked against files already in date order (checked: `qd-pair.csv` and `qd-signal.csv` sorted, unique dates). No change. | None.
15. mock-oa-quant-data | d1 to d3 feedback | note | Code items give one generic line; the only specific feedback is the results panel's failed test row. Fine for an assessment, but the three tests that most separate common errors (d1 per-ticker returns, d2 data error in the market column, d3 baseline) fail silently on a total. | Add to each `how` one sentence naming the mistake that the last test exposes, for example d3: "The last test fails a score that uses the test mean."
16. topic-3.5 | e-newest-first (30) | warning | The statement says "return them all" when fewer than `k` are held, but no test has `k` larger than the number held after the ring has wrapped (20 pushes, 8 slots, `k` 12 should give 8 values). An answer that reads `k` slots backwards from the counter, ignoring capacity, returns stale or duplicate values and passes all six tests. | Add a seventh test: `newest_first([1..20], 8, 12)` expecting `[20, 19, 18, 17, 16, 15, 14, 13]` (the cap is 6 tests in the brief; merge test 4 (capacity 1) into it or raise the cap with a note).
17. topic-3.5 | e-active-symbols (26) | note | Sound: edge, repeat, return, idle and a 100,000-call test. The statement promises "constant time on average" while the large test only checks an answer within 5 s; an O(distinct symbols) per call solution that is still fast enough would pass. Acceptable. | None.
18. topic-3.5 | pass mark and code | warning | `pass: 0.7` is 21 of 30 and the three code items are 3 marks. A learner can skip all code and pass (27 non-code items), so passing "tests out" of `coding-int` and `systems` L4 without writing a function. Same for every earlier topic exam, so it is a house pattern, not a defect of this file. | Note only. If wanted, ask the engine for a "code items must pass" flag (inbox).

### Pool practice (mock-oa-code)

19. mock-oa-code | draw from `drills/oa` | warning | The eight problems are listed on `#drill` and a learner can solve all of them there first (and l15 and l17 name the drill library). The mock draws two of eight, so after practice it is a replay, and after three or four sittings it repeats anyway (16 possible pairs). The description already says the pool is in the library but does not say what to do. Judgement: it does matter, because the mock's value is a cold read of an unseen statement; but the cost of withholding the pool is higher (the drills are the practice the course sells). | (a) Say it plainly in the description: "To use this as a cold test, do not open the pack `oa` in the drill library first." (b) Raise the pool to six per difficulty by widening the draw to `drills/ci` Python drills (needs the `language` filter already in the inbox, since the `ci` pack mixes C++) or by authoring four more `oa` drills. (c) Engine: draw unseen-first by whether the learner has solved the drill, not only by earlier mock draws. (a) now, (b) and (c) as backlog.
20. mock-oa-code | `oa-*` drills `how` | warning | Every drill says "Submit runs N hidden tests", but in the exam the button and the line above it say "Check" (screenshot: "Check runs the hidden tests. ... Submit runs 12 hidden tests."). Two verbs in two adjacent lines. | Reword the eight `how` lines to "There are N hidden tests. Each answer must equal the expected value." (neutral for drill and exam).
21. mock-oa-code | oa-remove-digits tests 11 and 12 | note | The expected value is `True` (a long string compared inside the call), so a failing row shows only `False`. | Acceptable for hidden large tests; add "The last two tests compare long strings" to `how`.
22. mock-oa-code | oa pool | note | All eight statements pin their conventions (empty input, modulus, loop returns -1, strict increase, "0" for nothing left); tests are small then large; the starter fails 7 to 13 tests; a valid answer in any other style (a deque, an array, a `heapq` or two queues) passes. No error found. | None.

### Prerequisites

23. mock-superday-research | `requires` | warning | `["coding-int/L4", "recruiting/L3", "research-int/L4"]` gives the largest closure (116). Paper 3 is two research data tasks (`rq-data`, taught in research-int L4), not the content of coding-int L3 and L4 (design, `two-in-sixty`, talking aloud); `recruiting/L3` is held only for the self-ticked story check. The mapping note itself says "a level that no item tests" is a reason to drop. Nothing in the papers needs either. | `["research-int/L4"]` (closure 89). If the behavioural check is to be gated, gate on `recruiting/L3` alone in `mock-superday-trader`, where a paper uses it.
24. mock-oa-quant-data | `requires` | note | `research-int/L4` is right and minimal. | None.
25. mock-oa-code | `requires` | note | `coding-int/L2` is right: the pool's patterns come from `coding-int/L1`'s own requires (`graphs-dp/L4`, `algo-think/L3`, `contests/L3`), strings and `ci-timed` from L2. Not over-gated. | None.
26. topic-3.5 | `requires` | note | None, as the rule says for topic exams. | None.

### Coherence of the topic exam with the levels

27. topic-3.5 | skills and coverage | note | All 13 skills are in the map and tested; every level has an item on its own lesson; items are on lessons of l1 to l17 and the heavy ones sit on the later levels. Not tested directly: research-int l6, l8, l12, l14, l15, l20; coding-int l5, l6, l9, l12, l13, l18, l19; systems l8 to l10, l14, l15, l18. That is normal for 30 items over 57 lessons and the skills still cover. | None.
28. topic-3.5 | no `longform` | note | Every other topic exam from 1.1 to 2.4 carries one `longform` item with a rubric; this one has none, though `rq-case` ("say it aloud") and `ci-timed` are spoken skills. AUTHORING section 5 does not require it. The case is tested by an `order` item and a numeric item. | Optional: swap one difficulty-3 item for a short `longform` on a case framing, with a ten-point rubric, if the house pattern should hold.
29. topic-3.5 | e-sixty-five-minutes (21) | note | The id says 65, the budget is 70 minutes (the report says it was changed from l15's 65). | Rename to `e-seventy-minutes`. The id is new, so no progress key breaks.
30. topic-3.5 | e-two-slopes, e-third-correlation, e-rank-one-det, e-first-component | note | Same families as mock items by design (the brief allows it); numbers differ. Item 16 (first component 8/11) and the mock's M4 (0.7945) test the same step with different matrices. Fine. | None.

### Layout (1280 and 390 px)

31. all four | start card | note | Checked from my own shots: name, description, models line, paper list with minutes and pass marks, checks, rules list; no overlap at 390. The mock cards read well. The stock playthrough shot named `start--1` is not the start card (for the superday it is the last-part checks page). | Playthrough (inbox already has the shot-naming bullet): name the start shot `start`.
32. mock-oa-quant-data | d1 to d3 at 390 | warning | Code lines scroll sideways inside the editor (line 7 of the d1 starter is cut at "reset_index("), as the topic-3.5 report also noted. The prose above the editor is set in bold in this item kind (the whole stem), which makes a 100-word data task heavy to read at both widths. | Shorten the starter solution lines in the `starter` fields to under 45 characters; ask for normal weight on a code item's stem (inbox).
33. topic-3.5 | table (item 17), tap-regions (12), order (19, 20), multi (18, 22, 23), parts (28), code (26, 27, 30) | note | Fit at 390 px; the table's two columns wrap their labels but stay legible; no horizontal page scroll. | None.
34. results pages | all four | warning | At 1280 the mock-superday-research By skill chart shows skills the mock never defines ("Conditioning puzzles", "Expected value puzzles", "First-step analysis") because drawn bank items bring their own skills (already in the inbox); the oa-code results page lists only "1 of 2" and its two drawn problems, with no skill split. The score trend and part-by-part list render correctly and the per-paper pass marks show. | Inbox bullet exists. For the mock, give each drawn problem a visible family name on the results line (already shown as the drill title). No file change.

## Themes

1. Tolerances and decimals: five numeric items reject a natural rounding (m1, m4, topic 16 and 25, q7). One-line fixes.
2. Pace equals clock on the superday papers 3 and 4 and on the topic exam.
3. No-calculator mocks whose rubrics and numbers need a calculator (k1, k2).
4. The `oa` pool can be practised first; say so and widen it.
5. The superday `requires` list is the heaviest and gates on levels no item tests.

## Fix pass

Fix pass of 4 Nov 2026 on `mock-oa-code`, `mock-superday-research`, `mock-oa-quant-data`, `topic-3.5` and the eight `oa` drills, with `answers-2026-11-04-exam-3.5.md` and the open items of `recheck-2026-11-04-a.md`. Scripts are in `/tmp/claude-0/-home-user-zero-to-quant/024bfe09-7a97-56c3-837c-b47a15727adf/scratchpad/fix-exams-3.5/`; the repeatable changes are in `docs/briefs/exam-3.5-scripts/second_read_patch.py` (called by `build.py`, which reproduces the shipped file) and in `docs/briefs/mocks-scripts/`. Result: validator 0 errors; voice scan (20 or more words, over 3 sentences) 0 and 0 on the four files and the `oa` drills; `--exam` for all four, desktop and `--mobile`, all passed; `--drills`: all eight `oa` drills pass (model solution passes all, starter fails); `rq-clean-frame-py` and `rq-group-slopes-py` fail under `--local-cdn` and are untouched by this pass.

1. Fixed: superday C1 1,350, C2 1,080, K1 1,080, K2 1,350 s (2,430 of 2,700 each); ML M5 360 and M6 300 s (1,620 of 1,800).
2. Fixed: topic code paces cut by a quarter (360, 360, 450 s); pace sum 4,920 s = 82 of 90 minutes.
3. Fixed: `mock-oa-code` description adds "Other reports give three or four problems in 70 to 90 minutes."
4. Fixed by decision: `pass` stays 0.5; the description now says "You pass the paper with one problem of the two."
5. Fixed: superday `models` is two sentences (18 and 19 words).
6. Fixed: M6 explain second sentence is "The best split is after the second point: its residual sum of squares is 10, against 40.7 and 26." (19 words; 10, 40.7 and 26 recomputed from residuals -5, -3, 2, 6).
7. Fixed: K1 rubric "standard error as about 1.6 points and z as about 1.5", "p well above 0.05 (about 0.15)"; K2 rubric "t as about 1.3, below 2", "an interval around 0.04 spans zero". Model answers keep 1.58, 1.45, 1.27 and -0.02 to 0.10.
8. No change needed.
9. Fixed: M1 `tol` abs 0.005, "Give two decimals", placeholder and accept line updated. 1.33 and 4/3 pass; 1.0 stays a named slip.
10. Fixed: M4 `tol` abs 0.005, "Give two decimals". 0.79 and 79% pass; 0.5714 and 0.5 stay slips.
11. Fixed: `e-first-component` `tol` abs 0.005 (0.5 points) with "Give one decimal place"; 73 and 72.7 pass, 63.6 stays a slip. `e-persistence-gain` `tol` abs 0.005; 20, 20.0 and 20% pass, 36, 40, 80 stay slips.
12. Fixed: Q7 asks "Give one decimal place", `tol` abs 0.001 (0.1 points); new `wrong` `typed-fraction` 0.00142 ("You typed the fraction. The box takes a percentage."). sqrt(0.02016) = 0.14199 and weights 0.6, 0.4 recomputed.
13. Fixed, with a dispute on the slip: Q3 is mean 3.0, s 10, n 25, key 1.5 (SE 10/5 = 2; 3.0 x 5/10 = 1.5). The reader's slip of 15 is wrong for these numbers: dividing by s/n = 0.4 gives 7.5, so `wrong-se` is 7.5 and `s-only` is 3.0/10 = 0.3. The circular check is now "the mean is one and a half standard errors from zero, below the 5% cut-off of about 2.06 for 24 degrees of freedom".
14. No change needed.
15. Fixed: each data task's `how` names the mistake a late test exposes (d1 a date-only sort, d2 an error in the market column, d3 a test-mean baseline, checked against the wrong variants in `oa_quant_data_build.py`).
16. Fixed: `e-newest-first` (function now `latest_values`) has 7 tests: the wrapped test now has `k` 12 over 8 held, and a new test `[1..10], 4, 6` expects `[10, 9, 8, 7]`. Compiled with g++ -O1: reference 7 of 7, starter fails 6, no-cap and take-`k` variants fail tests 3 and 5, bad mask fails 5. The brief cap of 6 is raised to 7 and noted in `docs/reports/exam-3.5.md`.
17. No change needed.
18. Skipped, as the reader said: note only. Engine: an optional "code items must pass" flag for topic exams.
19. Fixed (a): the description says "For a cold test, do not open the pack `oa` there first." Skipped (b), authoring four more `oa` drills or drawing from `drills/ci`: too large for a fix pass, and `drills/ci` mixes C++. Engine change needed for (b) and (c): a `language` filter on `draw` (already in the inbox) and unseen-first draws by whether the learner has solved the drill.
20. Fixed: all eight `oa` drill `how` lines read "There are N hidden tests. Each answer must equal the expected value." The superday and data-task `how` lines that began "Submit runs" use the same form.
21. Fixed: `oa-remove-digits` `how` adds "The last two tests compare long strings."
22. No change needed.
23. Fixed: superday `requires` is `["research-int/L4"]` (closure 89); `docs/reports/prereq-mapping-mocks.md` updated (the largest closure is now `mock-superday-trader`, 107).
24 to 26. No change needed.
27. No change needed.
28. Skipped: a `longform` swap would drop a difficulty-3 item and change the ramp 6, 15, 6, 3; AUTHORING section 5 does not require it.
29. Fixed: `e-sixty-five-minutes` is `e-seventy-minutes`.
30. No change needed.
31. Skipped: playthrough shot naming is an engine tool item (inbox).
32. Fixed: the three starter docstrings are under 45 characters. Skipped: normal weight on a code item's stem is an engine item (inbox).
33. No change needed.
34. Skipped: inbox bullets exist and no file change was asked.

Counts of the 34 findings: 20 fixed (1 to 7, 9 to 13, 15, 16, 20, 21, 23, 29, and the fixable parts of 19 and 32), 4 skipped whole (18, 28, 31, 34), 10 needing no change (8, 14, 17, 22, 24 to 27, 30, 33). Skipped parts: 19(b) and (c), 32 stem weight. The two recheck items (superday `models`, `m6-boosting-round`) are findings 5 and 6 and are fixed. Voice: the recheck items (superday `models` and `m6-boosting-round`) are closed; the scan at 20 or more words also caught seven further 20-word sentences in `topic-3.5.json`, now under 20.

Changed keys: Q3 key 1.8 to 1.5 (slips 9.0 and 0.36 to 7.5 and 0.3). Tolerances: M1, M4, `e-first-component`, `e-persistence-gain`, Q7. New items: `e-six-looks` (key `a`; $0.05/6 \approx 0.0083$, $6 \times 0.012 = 0.072$) and `e-next-higher-steps` (order s1 to s4; checked on closes 5, 3, 4, 7 giving 3, 2, 3, none). `e-weekly-hit-case` answer is s1 to s6 with s3 and s4 interchangeable. Changed tests: `e-newest-first` (above), `e-costliest-desk` (below).
