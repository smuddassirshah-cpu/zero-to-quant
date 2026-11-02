# Report: mental-pressure (Mental Maths Under Pressure, topic 3.3), level 1 "Speed"

## Files written

All in `app/content/courses/mental-pressure/`. Nothing else was edited except this report and `docs/BACKLOG-INBOX.md`; the validator rewrote `content/manifest.json`. `course.json` was not touched (a planning agent has since appended level 4 to it; level 1 ids are unchanged).

| File | Screens / items | Quiz | Code |
|---|---|---|---|
| `l1-towards-fifty.json` | 12 screens (hook, explore, the second target, the log, error analysis, 2 ladders, trap, generalise, derive, code, transfer) | 4 | `seconds_by_op`, `slowest` |
| `l2-two-by-two.json` | 12 screens (hook, explore, name, 3 ladders, trap, generalise, derive, code, 15-product drill, transfer) | 4 | `cross_multiply` |
| `l3-big-division.json` | 12 screens (same shape, 12-division drill) | 4 | `estimate_and_correct` |
| `l4-decimals-fast.json` | 12 screens (same shape, 15-decimal drill) | 4 | `decimal_places`, `scale_divide` |
| `review-1.json` | 10 items, difficulty 2 to 4, two or three per lesson | | |
| `homework-1.json` | 8 items, difficulty 3 to 5 (two at 5): 20-question drill table, 2 code items (`pace_needed` + `score_at` at 4; `error_report` at 5), an `order` derivation (cross multiplication of 76 × 58 with reasons and a dropped-carry distractor), 3 numeric, a 10-point `longform` error analysis | | 2 |

Skills: `mp-speed` on every lesson, plus `mp-formats` on l1 (as the brief says). Names and objectives from `course.json`. £ throughout.

Coordinator addition (interview plan, section (a)) is in l1: the hook names Zetamac 50 (Stage 3 and the topic exit) and the Today warm-up; screen 3, "The second target", names the 80-in-8 test "set by some trading firms, Optiver among them. As reported in 2026: 80 four-option questions in 8 minutes, +1 right, −1 wrong, no skipping. About 55 net is the reported mark", with a net-score task (64 answered, 5 wrong: 54). The transfer points to the Today warm-up for daily practice. review-1 has a net-scoring item (A 70 answered, 12 wrong, 46 net; B 60 answered, 3 wrong, 54 net). Note: the plan's "Firm facts" decision says firm facts belong in `recruiting` l4 and other courses say "trading firms"; I followed the coordinator's explicit "Optiver-style" instruction once, in plain text with "as reported". If the main session prefers the plan's rule, delete "Optiver among them" from l1 screen 3 prose.

Generators and helpers: `/tmp/claude-0/-home-user-zero-to-quant/9fb26fd5-8508-5986-8a3a-66bc5f67acde/scratchpad/mental-pressure-1/` (`lib.py`, `seedlog.py`, `ref.py`, `gen_l1.py` to `gen_l4.py`, `gen_sets.py`, `checkcode.py`). Every stated number is asserted in the generators by a second method (fractions or `Decimal`, `divmod`, Python's `*`) against the hand working in the prose.

## Validator

`node tools/validate.mjs` from `app/`: 0 errors. No warnings on mental-pressure files except the course-level "not yet written" line for levels 2 to 4.

## Playthrough

All with `--local-cdn .../scratchpad/pkgs --mobile`, and lessons also with `--why`:

- l1-towards-fifty: ok, 16 checks, quiz 4/4. l2-two-by-two: ok, 16 checks, quiz 4/4. l3-big-division: ok, 16 checks, quiz 4/4. l4-decimals-fast: ok, 16 checks, quiz 4/4.
- review-1: ok, recorded 10 of 10. homework-1: ok, marked 8 of 8 right, 38 of 38 marks.
- `checkcode.py` (CPython, same tests): every solution passes all its tests; every starter fails all of them, except l3's starter, which passes the one `n < d` case (`18 ÷ 24` returns `([], 0, 18)` before the loop) and fails the other six.
- Screenshots (desktop and 390 px, with Why? sheets): `.../mental-pressure-1/final/` and `.../l4fix/`. Fixes made from them: l1 log's ✓/✗ marks read as ×, replaced by "right"/"wrong"; l1 means table cut off at 390 px with 4 columns, cut to 3; l1 trap's correct option gave its numbers away, rewritten; l2 shortcut card's examples wrapped into 4 lines, shortened; l3 trap's log line had no tick labels, added; l4 explore's Why? sheet showed the opening state (derive overwrote the patch), fixed by patching the control value.

## Numbers and their sources

Pace: 120 ÷ 25 = 4.8, 120 ÷ 50 = 2.4, 120 ÷ 40 = 3, 120 ÷ 2.3 = 52.2 (about two points per 0.1 s near 50). Net: 59 − 5 = 54. Mix: 0.25 × 6 + 0.75 × 2 = 3 → 40; 0.25 × 3 + 0.75 × 2 = 2.25 → 120 ÷ 2.25 = 53.3 → 53 (brief's figures, recomputed). Trap: Ana 0.25 × 6 + 0.25 × 1.6 + 0.5 × 2 = 2.9 → 41; Ben 0.25 × 4.8 + 0.75 × 2 = 2.7 → 44. Generalise: base 3.25 → 36; division 5 s → 2.75 → 43; three fast kinds 1.5 s → 2.875 → 41; addition 1 s → 3.0 → 40. Derive: (2.4 − 1.5) × 4 = 3.6. Quiz: 15/4 = 3.75 → 32; 2 + 0.25 × 3 = 2.75; (3 − 1.875) × 4 = 4.5.

l1 seeded log (seed 50): 30 answers, 115.5 s; addition 8, 19.3 s, mean 2.4125; subtraction 3, 7.6 s, 2.5333; multiplication 9, 32.4 s, 3.6; division 10, 56.2 s, 5.62; division's share 56.2 ÷ 115.5 = 0.4866 (49%). Sums checked row by row by hand and by `Fraction`.

l2: 47 × 36 = 1,200 + 450 + 42 = 1,692; 53 × 24 = 1,272; 38 × 27 = 1,026 (cross 37); 64 × 53 = 3,392 (38); 29 × 76 = 2,204 (75); 40 × 36 = 1,440 (24); 97 × 94 = 9,118; 52 × 48 = 2,496; 65² = 4,225; 24 × 25 = 600; 68 × 57 = 3,876 (slips 3,076 and 3,826); 83 × 47 = 3,901 (cross 68); 73 × 67 = 4,891; 85² = 7,225; 98 × 93 = 9,114; 15 drill products all checked against `x * y` and cross multiplication. Brief deviation: the brief's trap figure "47 × 36 written 1,592" is not a middle-carry error (dropping the cross term's carry gives 1,292; dropping the units carry gives 1,652). The trap uses 68 × 57 keyed with both carry slips, and its byKey line cites 47 × 36 → 1,292; the transfer (£47 × 36 = £1,692) keys 1,292 and 1,652.

l3: 864 ÷ 24 = 36; 2,592 ÷ 32 = 81; 1,350 ÷ 25 = 54; 1,008 ÷ 12 = 84; 1,170 ÷ 15 = 78; 4,761 ÷ 69 = 69 (69² = 4,761); 1,000 ÷ 37 = 27.027 (37 × 27 = 999); 6,048 ÷ 24 = 252; 7 ÷ 16 = 0.4375; 18 ÷ 24 = 0.75; drill answers checked by division; quiz 1,575 ÷ 25 = 63, 2,000 ÷ 37 = 54.05, 9 ÷ 16 = 0.5625, 7,236 ÷ 36 = 201. Transfer changed slightly from the brief: the £4,761 fee over 69 accounts is £69 each, and the task asks for three accounts (£207), because 4,761 ÷ 69 is already the ladder's question.

l4: 0.3 × 0.07 = 0.021; 0.75 ÷ 0.025 = 30 (explore, instead of the brief's 0.48 ÷ 0.012, which is kept for the trap: 40, keyed 4 and 400); 4.5 × 0.6 = 2.7; 0.8 × 0.05 = 0.04; 0.25 × 0.4 = 0.1 (edge case, keyed 0.01); 0.36 ÷ 0.04 = 9; 2.4 ÷ 0.006 = 400; 0.07 × 600 = 42; known decimals 3/8, 5/6, 2/7, 4/9, 3/11 (tol 0.0002, so building from 4-place unit fractions passes); £2.35 × 12 = £28.20; 0.006 × 0.5 = 0.003; 0.35% of £12,000 = £42. All products by counted places and by `Decimal`, quotients by scaling and by `Decimal`.

Review: 120 ÷ 45 = 2.67; 58 × 34 = 1,972; 1,176 ÷ 28 = 42; 0.09 × 0.4 = 0.036; mean of 2, 2.4, 3.6, 6 = 3.5 → 34; 34 × 26 = 884; 3,000 ÷ 64 = 46.875; 0.042 ÷ 0.0007 = 60; £1.85 × 24 = £44.40; nets 46 and 54.

Homework: 20 drill answers checked by `Fraction`; 76 × 58 = 3,500 + 860 + 48 = 4,408; 7,488 ÷ 36 = 208; 0.125% of £48,000 = £60; 500 ÷ 13 = 38.46. `error_report` drill picks (rule: error rate 0.25 or more first, else largest share of time): seed 50 division, seed 51 multiplication (share 38%, although division's mean is higher), seed 52 subtraction (2 wrong in 7). Longform (seed 54): 110.5 s; means 2.57, 2.83, 4.36, 4.54; shares 16%, 15%, 35%, 33%; five wrong first tries costing 25.7 s; the target (multiplication 3 s, division 3.5 s) gives 90 s for 30 answers, pace 3, score 40.

## Seeds and generators

`seedlog.make_log(seed, n=30)` with `random.Random(seed)`: operation by `rng.choice` of the four Zetamac kinds, Zetamac's ranges (2 to 100 plus 2 to 100; 2 to 12 by 2 to 100; subtraction and division as the reverses), no repeat of the previous question; seconds uniform per kind (addition 1.5 to 3.0, subtraction 1.5 to 3.0, multiplication 2.5 to 5.0, division 2.5 to 7.0, one decimal), a wrong first try with chance 0.05, 0.25, 0.08, 0.08, adding 1.5 to 3.0 s. Seed 50 is the l1 log (embedded as `LOG` in the l1 code prelude); seeds 50, 51, 52 test `error_report` (the prelude holds `make_log` verbatim); seed 54 is the homework longform log. The division range was narrowed from the brief's "3 to 8 s" example so that seed 50's 30 answers fit in 120 s.

## Proposed course.json changes

None.

## Notes for exam authors

A timed 80-question, 8-minute paper (four-option items, +1 and −1, as reported) is a natural part for the topic 3.3 or Stage 3 exam on the exam timer. Level 1's drills (cross multiplication, two-digit division, decimals) and review items are suitable sources. No exam file was written.

## Backlog bullets

Five bullets under "Raised later (mental-pressure level 1)" in `docs/BACKLOG-INBOX.md`: timed table sets (item 129), the warm-up's missing per-question log, no one-operation or 80-in-8 warm-up mode, the validator refusing `byKey` for table-cell `wrong[]` ids, and derive overwriting an explanation patch on derived points.
