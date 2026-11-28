# Engine pass AK: item 1267, numbers_lib coverage of on-screen numbers

`numbers_lib.Level.report()` now lists on-screen numbers (prose, question, hints, explain, how, why, model answers, byKey, summary, canvas labels, table cells) that no check compared against. Covered by `expect`, `check_wrongs` (answers, wrong values), `slip`, `claim(..., covers=[...])`, `literal(value, why=...)`. Years, list numbers, `lesson 3` ids, exponents, subscripts and code are ignored; matching is by value to the stated precision (sign ignored, `%` also x100). Default warns only; `coverage="strict"` or `ZQ_NUMBERS_STRICT=1` fails; `coverage="off"` skips.

Uncovered counts (all 22 AI-strand scripts still exit 0, run with the venv): ai-basics L1-L4 79, 229, 42, 107; ai-use L1-L3 30, 246, 75; info L1-L3 181, 151, 309; backprop L1-L4 103, 28, 278, 145; rl L1-L5 232, 185, 114, 152, 76; gpt L1 322; cnn L1-L2 146, 111.

Time cost: the coverage pass takes 0.01 to 0.02 s per level; script runs are dominated by their own Python (0.05 to 11 s).

Caveats: counts include small integers and label digits, so a first strict run needs many `literal` calls or added `expect`s; `covers` and `literal` are by value, not by place.

## Follow-up: narrower claim filter

Only claims count: decimals, fractions, percentages, money, units, whole numbers in arithmetic or over 100, and words for fractions and multiples as values. Bare whole numbers, axis, node and frame labels and table headers are skipped; a figure repeated on a screen or across screens counts once; `model` answers are now read; a fraction or word must be covered in its own file.

Counts now (were): ai-basics L1-4 33, 118, 16, 53 (79, 229, 42, 107); ai-use L1-3 17, 108, 43 (30, 246, 75); info L1-3 105, 101, 152 (181, 151, 309); backprop L1-4 52, 14, 171, 108 (103, 28, 278, 145); rl L1-5 112, 112, 77, 94, 39 (232, 185, 114, 152, 76); gpt L1 165 (322); cnn L1-2 85, 78 (146, 111). Median about 90 (was about 145): the target of 15 is not met. What remains is mostly real working figures (0.7776, 0.2875) that the scripts never check. Screen-level matching was tried and tripled the counts.

Pre-fix files, current scripts: caught ai-basics l8 "0.22, 19.84", info l7 "a third", cnn l2 "4/3", cnn homework-2 "12,500" (after reading `model`). Not caught: cnn l3 "4 + 4 + 0" giving 4, because 4 and 0 are covered by value elsewhere in the level.
