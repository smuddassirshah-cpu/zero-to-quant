# ai-basics level 1 (Models from data): report

## Files

| File | Screens or items | Quiz |
|---|---|---|
| `l1-rules-or-examples.json` | 9 screens (problem tap rows, explore with rule frames, problem tap graph, problem place, ladder, trap, ladder edge case, generalise, transfer), 12 min | 3 |
| `l2-features-and-labels.json` | 9 screens (problem place, problem, 3 ladder, trap, ladder edge case, generalise, transfer), 12 min | 3 |
| `l3-learning-a-rule.json` | 10 screens (explore plane with draggable $t$, problem bars, 3 ladder, trap, ladder edge case, 2 code, transfer), 14 min | 3 |
| `l4-unseen-questions.json` | 10 screens (problem, problem table widget, 4 ladder, trap, generalise, transfer), 13 min | 3 |
| `review-1.json` | 10 items, difficulty 2 to 4, `pass: 0.8`, every item `ab-models`, all four lessons interleaved | |
| `homework-1.json` | 7 items, difficulty 3 to 5: code `accuracy` (4), code `split_train_test` (4), code `fit_and_score` (5), order with a distractor (3), numeric ties (3), choice leak (4), longform "the 100% app" (5, 10-point rubric) | |
| `problems-1.json` | 3 chained problems, 15 parts: loans (4, l3 and l4), café (3, l1 to l4), desk signal (5, l3 and l4) | |

Skill `ab-models` throughout; objectives copied from `course.json`. Stage 0 is outside the verb rule, so no performance task.

## Self-check (SESSION PROTOCOL 4)

1. `node tools/validate.mjs`: 0 errors. Warnings left on level 1 files: four "problem screen without a canvas" (l1 screens[3] and [4], l4 screens[1] and [4]; text-only judgements and a table widget). None on review, homework or problems.
2. `VOICE_BASE=app/content/courses/ai-basics python3 docs/reviews/voice-scan.py 35 --summary`: 0 over 35 words, 0 lesson ids in code spans, 0 doubled words, 0 explanations over three sentences.
3. `docs/reports/ai-basics-L1-numbers.py` with the scratchpad venv: exit 0, 262 of 262 checks. The 30 "check by hand" lines were read; each byKey names its slip and the numbers it states are the working, not the slip value.
4. Playthrough with `--local-cdn <scratchpad>/aitiming/pkgs`, desktop and `--mobile`, all green: l1 12 checks, l2 12, l3 13, l4 13 (quizzes 3/3); review-1 10 of 10; homework-1 7 of 7 with the longform marked by the button; problems-1 15 parts, with `--why` every typed slip routed to its own line. `grade-all.mjs --code` on the seven files: 71 widgets, 5 code widgets, 0 failures. `fresh-check.mjs --file problems-1.json`: 0 hits.

Screenshots read at 1280 and 440. Two layouts were replaced after a 440 shot: the `boxes` sort of five job cards (labels ran over the cards and the containers ran off the column) became a `place` with interchangeable chips; a `pair` of two ten-row tables stacked into a canvas taller than the phone, so the memoriser and the rule now share one four-column table.

## Data and numbers (all recomputed in the script, method A counts agreements, method B counts false alarms and misses)

- Course data as the brief: links `[0, 1, 1, 2, 3, 4, 5, 6, 7, 9]`, spam `[0, 0, 0, 1, 0, 0, 1, 1, 1, 1]`; counts for $t$ = 0 to 10 are 5, 6, 8, 7, 8, 9, 8, 7, 6, 6, 5; $t$ = 5 unique best, 9 of 10 (90%); $t$ = 3 gives 7, $t$ = 6 gives 8. Test emails `[0, 2, 4, 5, 8, 10]`: the rule 5 of 6 (83.3%); the memoriser answers 4 and gets 2 right; tuning on the test set gives 6 of 6 at $t$ = 3 and 4.
- Added "says free" column `[0, 0, 1, 1, 0, 0, 0, 1, 0, 1]`: the rule "links at least 5 or says free" also scores 9 (fixes email 4, breaks email 3).
- l1 six emails (A to F): "says free" is wrong on C, D, F; the explore frames give 3, 2, 0, 3 mistakes for free, links ≥ 1, ≥ 5, ≥ 8.
- Tie inbox (links 0 to 5, spam `[0, 0, 1, 0, 1, 1]`): counts 3, 4, 5, 4, 5, 4, 3; $t$ = 2 and 4 tie at 5, the midpoint 3 gets 4.
- l3 transfer, desk signal on 8 days: cut-offs 0.5, 1.0, 1.5 score 5, 7, 5.
- Trap: the brief named "the median, 3" as the split-in-half threshold. The median of the link counts is 3.5 and $t$ = 3 puts 4 and 6 either side; $t$ = 4 is the threshold that splits 5 and 5, so the trap uses $t$ = 4 (8 right) with the mean 3.8 as a second distractor.
- Review: 3 right at $t$ = 4 on links 1, 2, 4, 6, 8; 87.5%; memoriser answers 2 of 4; 50% test score.
- Homework: `fit_and_score` tests on planted data (best $t$ 4 then 3 test right; and three more cases computed both ways); thresholds 0 to 7 on x = 0, 2, 4, 6 with labels 0, 1, 0, 1 score 2, 3, 3, 2, 2, 3, 3, 2, so 4 tie.
- Problems: loans (missed payments `[0, 1, 2, 3, 4, 6, 7, 9]`, defaults `[0, 1, 0, 0, 1, 1, 0, 1]`): $t$ = 3 gives 5, best $t$ = 4 with 6 (75%), test loans 2, 5, 8, 10 give 50%, memoriser answers 1. Café: 3 features, 17 of 20 = 85%. Signal: 0.2, 0.5, 0.8 score 6, 7, 6 on ten days and 4, 2, 3 on five kept-back days; honest 40%, tuned 80%.

Every code widget: the script runs its `solution` in CPython (all tests pass) and its starter (fails at least one), and recomputes each expected value by method B.

## Conventions

Rules use "at least $t$" (`>=`) for whole-number features and "above" (`>`) for decimal signals, so no case sits on a boundary. Percent answers use `unit: "%"` with the key as a fraction. Ties in code break towards the smaller threshold. Money in £.

## Proposed course.json change

None.
