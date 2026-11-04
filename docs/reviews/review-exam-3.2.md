# Topic 3.2 exam: second-reader findings

Scope: `app/content/exams/topic-3.2.json` (id `topic-3.2`), read in full against `docs/briefs/exam-3.2.md`, `docs/reports/exam-3.2.md`, `docs/AUTHORING.md` section 5, the three course maps and the engine's grading and scoring code (`numeric.js`, `order.js`, `expression.js`, `table.js`, `mock.js` `tally`, `screens/exam.js`). Read only; arithmetic is in `docs/reviews/answers-3.2-exam.md` and is not repeated.
Method: coverage computed from the lesson files (skills first met per level, against the exam's `skills` tags); voice by `VOICE_BASE=<worktree>/app/content/exams python3 docs/reviews/voice-scan.py` and by a second script over every prose, feedback, `why` and `explain` string; layout by `node tools/playthrough.mjs --exam topic-3.2 --mobile --tablet --why --shots ... --local-cdn <pkgs>` (passed, 37 questions, 30 of 30, no sideways scroll) and by looking at the 440, 1032 and 1376 screenshots of the order, table, parts, expression, multi and code items and of the results page at all three widths. Scratch files are in the scratchpad folder `ac-exam32`.

## Counts

| Item | Value |
| --- | --- |
| Items and questions | 30 items; 37 sittable questions (6 `parts` items hold 13 sub-asks); scored out of 30 with equal credit per part |
| Ramp | 6 at d2, 15 at d3, 6 at d4, 3 at d5 (the 20, 50, 20, 10 target); file order by difficulty, courses interleaved |
| Courses | `ito` 11 items (14 questions), `measure-prob` 11 (13), `pdes` 8 (10): 37%, 35%, 27% of questions against 37%, 37%, 26% of lessons |
| Clock | 90 minutes against a pace sum of 4,875 s = 81.25 minutes (8.75 minutes, 10%, spare) |
| Pass | 70% = 21 of 30 |
| Voice | the repository scan reports 0 hits for topic-3.2; the second script finds 0 sentences over 20 words, 0 exclamation marks, 0 dashes, 0 US spellings, 0 explanations over three sentences, 1 sentence of exactly 20 words (finding 9) |

## Findings

Format: number | severity | item id | what is wrong | exact fix.

### Coverage and balance

1. note | whole exam | Coverage holds. All 14 skills are in the map and tested; every one of the 11 levels with a skill of its own is tested through a skill first met there (checked against the lesson files: `ito` l1 `it-bm` and `it-calculus`, l2 `it-martingale` (l8), l3 `it-pricing`; `measure-prob` `mt-sigma`, `mt-integral`, `mt-condexp` and `mt-martingale`, `mt-change`; `pdes` `pe-heat`, `pe-fourier`, `pe-bs`, `pe-fk`, `pe-fd`). `ito` level 2 is the thinnest: its first-met skill `it-martingale` is tested by three items, but its lessons l5 to l7 (Itô integral, Itô's lemma, solving GBM) count only through the shared `it-calculus` and `it-bm` (`e-drift-t2w2`, `e-gbm-below`). That is the right trade, since both items are genuine l6 and l7 skills. | None.
2. note | `ito` level 4 | Counting only through shared skills is acceptable and no item should move. Level 4 has no first-met skill, but four of its five lessons have a dedicated item (`e-sixth-repair` l13, `e-exit-drift` l14, `e-moment-and-isometry` l15, `e-cubed-claim` l16) and l17 (derive Black-Scholes aloud) is tested by `e-theta-from-pde`. Moving an item would take a mark from a level with a skill of its own. Same treatment as `coding-int` level 3 in exam 3.5. | None. Optional: say in `description` that `ito` level 4 counts through shared skills.
3. note | `pdes` level 3 | The three first-met skills each have a single item (`e-heat-change`, `e-fk-square`, `e-explicit-code`). Each is one question or sub-ask pair, so a learner who misses one shows that skill at 0 of 1. Acceptable for a 30-item cap; the by-skill chart at 440 px shows them as 1 of 1 bars. | None.

### Difficulty, time and pass mark

4. warning | `e-explicit-code` and the pass mark | The pass mark is 21 of 30 and every item is worth one mark, so the only `pe-fd` item (a 480 s code task) is worth 3.3% and a learner can skip it, all three d5 items and five more and still pass (the by-skill bars then show 0 of 1 for `pe-fd`, `mt-condexp` at d5 and `it-pricing` at d5, but the headline says Pass). Exam 3.5 raised the same (its review finding 18). | Keep the structure, since the engine weights items equally. Add to `description`: "The code task is one mark of 30. A pass with the code task blank still leaves the finite-difference skill unchecked." Or leave as the house pattern and record the decision in `DECISIONS.md`.
5. note | `e-moment-and-isometry` | A d3 item with `pace` 240, the same as the d4 `e-exit-drift` and longer than `e-daily-touch` (210) and `e-coefficient-k` (180). Two parts, one 90 s Wick split and one 90 s isometry, plus reading. Plausible, but it makes the d3 band look heavier than the d4 band in the pace column. | `"pace": 210`. The pace sum becomes 4,845 s (80.75 minutes).
6. note | timing | 81.25 of 90 minutes is a sound margin (exam 3.5 had 88.5 of 90 and a finding). The playthrough clock reads 1:18 used because it answers at once, so it says nothing about pace. The code item (480 s) pays for Pyodide loading in the first run only. No change.
7. note | difficulty ramp | The d3 band is wide (15 items): `e-theta-from-pde`, `e-ruin-by-martingale` and `e-fk-square` are one-formula items that read as d2 to d3, while `e-pick-martingales`, `e-adapted-predictable` and `e-rod-centre` need several steps. The 6, 15, 6, 3 split is met exactly and the order within d3 is mixed by course, so the ramp holds. No change.

### Items: answers a learner can reach and feedback that misleads

8. warning | `e-variance-split` | `same: [["s5", "s6"]]` is the only freedom, but `s5` and `s6` need only `s2`, so a proof that states the two squares before the cross-term lines is valid and is marked wrong (see `answers-3.2-exam.md` mismatch 1). | Start `s5` with "With the cross term gone," and `s6` with "With the cross term gone,", as written there.
9. note | `e-variance-split` | `d2.why` is a 20-word sentence by a count that treats each maths span as one word ("Taking out what is known leaves the conditional mean $E[X - Y \mid \mathcal G]$, not the plain mean, and the product stays inside $E$."). The repository scan does not flag it. | "Taking out what is known leaves $E[X - Y \mid \mathcal G]$, not the plain mean, and the product stays inside $E$."
10. warning | `e-swap-limits` | Option `e` has infinite means on both sides, so a careful learner may leave it unticked and be marked wrong (`answers-3.2-exam.md` mismatch 2). | Replace option `e` with $\min(n, U^{-1/2})$ and the matching `explain` line, as written there.
11. warning | `e-pick-martingales`, `e-swap-limits`, `e-sigma-families` | `feedback.correct` and `explain` refer to options by letter ("A, C and E") or position ("the first family"). Options are shuffled and carry no letters on screen (440 px screenshot of question 13 shows none), so the sentences cannot be read against the list. | Name the options by content, as written in `answers-3.2-exam.md` mismatch 3.
12. note | `e-cubed-claim`, `e-exit-drift`, `e-moment-and-isometry` | Three feedback lines name a slip that the value does not show (`no-convexity` uses $n$ for $m$ and its value is $8e^{-0.36}$; `driftless` 2.0 is the standard Brownian $ab$, the driftless value for $\sigma = 0.9$ being 2.4691; `odd-power-zero` says the total power is odd when it is 4). | Lines as written in `answers-3.2-exam.md` mismatches 4, 5 and 6.
13. note | `e-tree-price` part 3 | Distractor `d` ("It matters for a call, but not for a put, by put-call parity") is weak: nobody holds the belief it states, so the item is a three-way choice. | Replace with "It matters only when the share pays no dividend, so it drops out here." with `why` "Dividends have no link to the replication argument. The price is a replication cost with or without them." Length stays under the key's 1.2 times limit (the key is 60 characters, the new option about 76).
14. note | `e-jump-gibbs` part 2 and similar | The prompt says "Give three decimal places" and `accept` shows "7.537 within 0.01"; `tol` 0.01 is wider than the three places asked for, so 7.53 and 7.54 are accepted. Intentional, since the Gibbs value is a limit (7.5369) and learners round the percentage. No change.

### Wording and voice

15. note | voice | Repository scan: 0 hits for topic-3.2 (22 lines in all, from other files in `app/content/exams`). Second script: no sentence over 20 words in any prose, `feedback`, `why`, `explain` or `how` string; the longest are 19 (`e-jump-gibbs` part 2 question and explain, `e-daily-touch` prose, `e-explicit-code` question). No exclamation marks, em-dashes or en-dashes; British spellings throughout ("standardised"); explanations at most three sentences (`e-variance-split` and `e-explicit-code` have three). Shares of money carry no £ because the items are unit-free prices. No change.
16. note | choice and multi items | All three `multi` items and the one `choice` carry `shuffle: true`; no key is longer than any distractor (multi: longest key 41 characters against 59, 27 against 33, 14 against 32; choice: 60 against 80); every distractor has a `why`. Meets the rule. No change.

### Layout (440, 1032 and 1376 px)

17. note | all items | No sideways scroll at 440, 1032 or 1376 (the playthrough asserts it). At 440 the table (question 14), the order item (question 29, lines wrap in three or four lines, the cross buttons stay inside), the parts item (question 26), the multi (question 13) and the expression (question 27) read cleanly. At 1376 the order lines are single lines and the question rail shows 30 of 30. The results page is correct at all three widths: Pass stamp, "30 of 30", pass mark 70%, time line, XP, mastery and the by-skill bars with a "Show as table" link; the 1376 shot shows a hover tooltip over the Black-Scholes bar, which is the playthrough's pointer and not a bug.
18. note | `e-explicit-code` starter | At 440 px two starter lines are cut at the editor's right edge: line 2 of the docstring ("ends fixed at 0." clips) and line 13 (`new[i] = u[i] + lam * (u[i + 1] - 2...`). The editor scrolls sideways inside its box, which the page does not. | Docstring line 2: `Explicit scheme, ends fixed at 0.`; split line 13 into `new[i] = u[i] + lam * (` / `    u[i + 1] - 2 * u[i] + u[i - 1])` (keep the starter failing: it still uses `int(T / dt_max)`).
19. note | results page | "Slowest families: risk-neutral-tree 6 s, gibbs 4 s, quick-pricing 4 s" shows the raw `tags` as family names. They are legible and the paced line is correct ("Every paced question was inside its pace (30)"). No change.

## What was checked and is fine

The `skills` map equals the three `course.json` labels; no `requires`; 30 items (validator cap); every item has `id`, `difficulty`, `skills`, `tags` and `pace`; the title field of each item is plain or maths text; `parts` items carry a stem and per-part `feedback`; expression items carry `integers` only where `(-1)^k` is used; the table has `accept` forms `y` and `n`; the order item lists every line once across `answer` and `distractors` and each distractor has a `why`; the code item has 8 tests inside the 6 to 8 cap pattern of exam 3.5 plus one example, and the `how` sentence tells the learner what the tests hold.

## Fix pass

Scope: `app/content/exams/topic-3.2.json` only, by targeted edits (script in the scratchpad `fix-exam32/`). Covers the 9 findings of `docs/reviews/answers-3.2-exam.md` (A1 to A9) and the 19 of this file (R1 to R19). Each correction recomputed before writing: $E[\min(n, U^{-1/2})] = n \cdot n^{-2} + 2(1 - 1/n) = 2 - 1/n \to 2 = E[U^{-1/2}]$; $8e^{-0.36} = 5.5814$ and $8e^{1.08 - 1.44}$ agree; $ab/\sigma^2 = 2/0.81 = 2.4691$; $e^{4.875} = 130.974$, $e^{-8} = 0.000335$. After each key change the file was grepped for the old value. New number 2 (mean of the capped $U^{-1/2}$) is a bare fact, not a parameter set; `U^{-1/2}` appears nowhere else in `app/content`.

- A1 / R8 Fixed: `e-variance-split` s5 and s6 now open "With the cross term gone,", so both need s3 and s4 first and the only freedom is the existing `same: [["s5", "s6"]]` swap. Order s1 s2 s5 s6 s3 s4 s7 now reads as invalid, as it should. Every valid order is accepted and no invalid one.
- A2 / R10 Fixed: `e-swap-limits` option e is now $\min(n, U^{-1/2})$ (finite mean 2 on both sides); key a, c, e unchanged; `explain` rewritten.
- A3 / R11 Fixed: `e-pick-martingales`, `e-swap-limits` and `e-sigma-families` feedback and explain name the options by content, no letters or "first".
- A4 Fixed: `e-cubed-claim` `no-convexity` line uses $m$ and states $8e^{-0.36} = 5.5814$.
- A5 / R12 Fixed: `e-exit-drift` part 2 id `driftless` renamed `standard-bm`, line rewritten (part 1 `driftless` stays: $b/(a+b)$ ignores $\sigma$). Grep shows no other use of the old id in part 2.
- A6 / R12 Fixed: `e-moment-and-isometry` `odd-power-zero` line no longer claims the total power is odd.
- A7 Fixed: `e-is-weight` wrong values 130.97 and 0.000335 (tolerances kept; neither meets the key 0.007635 or the other).
- A8 Disputed (no change): `e-daily-touch` key 0.6956 against the exact walk 0.6957 is 0.0001 apart with `abs` 0.004; the reader says no change and no wrong value is near it.
- A9 Disputed (no change): the rounded-term sums differ from the keys by one unit in the last place, inside `tol` (0.02, and the 9.19314 price within 0.0006).
- R1, R3, R6, R7 Disputed (no change): reader notes that conclude "no change"; coverage, the thin skills and the 81.25 minute clock rechecked in the file (pace sum before the R5 edit 4,875 s).
- R2 Disputed: the optional line for `description` cannot be written. A topic exam has no `description` field (AUTHORING section 5, topic exam shape: id, topic, name, minutes, pass, skills, items), and the validator would not read it.
- R4 Disputed (pass mark, no change). Comparison: `topic-3.5.json` has three code items (3 marks of 30) and its review finding 18 reached the same warning; its fix pass skipped it as a house pattern, with an engine flag "code items must pass" as the only remedy. `topic-3.3.json` has no code item (its one non-auto item kind is `longform`), so it offers no precedent for a single code item. AUTHORING section 5 gives a topic exam one `pass` share of all marks; per-item weights and a section pass exist only on stage-exam papers (`parts` of `kind: "paper"`) and mock papers, with `scoring` marks equal for every item. A weight or section pass would need an engine change, which a content pass may not make. Pass stays 0.7 (21 of 30); the by-skill chart still shows `pe-fd` at 0 of 1 for a learner who skips the code task.
- R5 Fixed: `e-moment-and-isometry` `pace` 240 to 210 (pace sum 4,845 s, 80.75 minutes).
- R9 Fixed: `e-variance-split` d2 `why` is now "Taking out what is known leaves $E[X - Y \mid \mathcal G]$, not the plain mean, and the product stays inside $E$."
- R13 Fixed: `e-tree-price` part 3 option d replaced as proposed (key 60 characters against 70).
- R14, R15, R16, R17, R19 Disputed (no change): each states "no change" (intentional wide tolerance on the Gibbs limit; voice clean; every choice shuffled with a `why`; layout clean; raw tags are legible family names).
- R18 Fixed: starter docstring line is "Explicit scheme, ends fixed at 0." and the update line is split over two lines; the starter still uses `int(T / dt_max)` and still fails. Checked at 440 px: no clipped line.

Counts: 15 fixed (A1 to A7, R5, R9, R13, R18 and the shared R8, R10, R11, R12), 13 disputed or no change (A8, A9, R1 to R4, R6, R7, R14 to R17, R19). Graded answers changed: none (the key of `e-swap-limits` is still a, c, e, with a new option e).

### Changed keys

- `e-swap-limits` option `e` text: `\min(n, 1/U)` to `\min(n, U^{-1/2})` (still correct).
- `e-exit-drift` part 2 `wrong` id and `byKey`: `driftless` to `standard-bm` (value 2.0 unchanged).
- `e-is-weight` `wrong` values: `upside-down` 130.9 to 130.97; `no-half-theta-squared` 0.0003 to 0.000335.
- `e-variance-split` lines `s5` and `s6` text; `d2` why (order key and `same` unchanged).
- `e-cubed-claim` part 1 `byKey.no-convexity` text (value 5.5814 unchanged).
- `e-moment-and-isometry` `pace` 240 to 210; `byKey.odd-power-zero` text.
- `e-tree-price` part 3 option `d` text and `why`.
- `e-explicit-code` starter text only.

### Checks

Validator: 0 errors, no warning for `topic-3.2`. Playthrough `--exam topic-3.2` green (37 questions, 30 of 30), and with `--mobile --tablet --why` green; shots of items 23, 25, 29 and 30 read at 440, 1032 and 1376. Voice scan: 0 lines for `topic-3.2`.
