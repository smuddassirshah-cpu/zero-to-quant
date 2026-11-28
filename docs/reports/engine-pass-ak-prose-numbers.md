# Engine pass AK: item 1267, numbers_lib coverage of on-screen numbers

`numbers_lib.Level.report()` now lists on-screen numbers (prose, question, hints, explain, how, why, model answers, byKey, summary, canvas labels, table cells) that no check compared against. Covered by `expect`, `check_wrongs` (answers, wrong values), `slip`, `claim(..., covers=[...])`, `literal(value, why=...)`. Years, list numbers, `lesson 3` ids, exponents, subscripts and code are ignored; matching is by value to the stated precision (sign ignored, `%` also x100). Default warns only; `coverage="strict"` or `ZQ_NUMBERS_STRICT=1` fails; `coverage="off"` skips.

Uncovered counts (all 22 AI-strand scripts still exit 0, run with the venv): ai-basics L1-L4 79, 229, 42, 107; ai-use L1-L3 30, 246, 75; info L1-L3 181, 151, 309; backprop L1-L4 103, 28, 278, 145; rl L1-L5 232, 185, 114, 152, 76; gpt L1 322; cnn L1-L2 146, 111.

Time cost: the coverage pass takes 0.01 to 0.02 s per level; script runs are dominated by their own Python (0.05 to 11 s).

Caveats: counts include small integers and label digits, so a first strict run needs many `literal` calls or added `expect`s; `covers` and `literal` are by value, not by place.
