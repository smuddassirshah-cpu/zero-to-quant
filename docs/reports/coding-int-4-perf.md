# coding-int level 4: performance task

`homework-4.json`, `h4-pairs-aloud`, item 9 of 9 (added; cap 12). Kind `aloud`, `seconds` 600, `think` 60, 3 follow-ups.

Objective: l18 "Explain the plan and its trade-offs aloud while writing the code", the only rule-matched objective in L4. `aloud`, not `code`: the product named is the spoken plan and trade-offs, which no hidden test can grade; the level's code is already auto-graded in `h4-zero-sum-cpp`.

Task: talk through `count_pairs(sizes, target)` while typing it; fresh against `h4-aloud` and l18.

Rubric: 2 + 2 + 3 + 2 + 1. Row 3 (dict versus sort and two pointers, time and memory, a choice) is `required`; row 5 marks follow-up 1. Model justifies each step.

Gates:
1. `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors; only the expected perf-pending warnings.
2. `VOICE_BASE=app/content/courses/coding-int python3 docs/reviews/voice-scan.py 35`: 0 and 0.
3. `python3 -I docs/reports/coding-int-4-perf-numbers.py`: exit 0 (model code run against brute force, two pointers and the follow-up 2 formula on 3,000 lists; 19,999,900,000 and the `int` limit two ways).
4. `node tools/playthrough.mjs --set coding-int/homework-4 --local-cdn <pkgs>`, with and without `--mobile`: All passed; marked by the button. Shots read cleanly.

Freshness grep: `pair`, `target`, `two pointer`, `sums to`, `complement`, `trade-off`, `median`.

Overlapping screens: l18-talking-while-coding screens[1] (say the problem back), [2] (name the brute force), [4] (plan as comments, then code), [7] (the order of a spoken answer) and [9] (say the complexity), all on products of the other entries; homework-4 `h4-aloud`; new parts: `count_pairs(sizes, target)` with equal sizes making pairs, a dictionary against sorting and two pointers with time and memory, the sorted-input follow-up, many targets on one list, and the C++ type for the answer.
