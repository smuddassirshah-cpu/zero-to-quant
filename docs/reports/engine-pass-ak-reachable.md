# Engine pass AK: reachable feedback (item 1269)

(a) Done: `grade-all.mjs --code` warns `feedback-unreachable` (a `byKey["test-N"]` line no mutant first fails) and `feedback-missing` (a test a mutant first fails, no line); `--strict-feedback` fails them. Reads the `feedback` of the item holding the widget, ai courses only, widgets with mutants only. AI topic exams are not under `courses/`, so `--strand ai` never reaches them.
(b) Skipped: a slip's wrong value cannot be recomputed by the validator, so any rule would be noisy.
(c) Four new cases in `tools/test-grade-code.mjs` (20 pass).
Current AI content, 471 warnings, 300 widgets: ai-basics 35 (15 unreachable, 20 missing), ai-use 2, backprop 72 (13, 59), cnn 24 (8, 16), gpt 24 (11, 13), info 46 (20, 26), makemore 38 (2, 36), nn-train 89 (0, 89), representations 26 (15, 11), rl 83 (0, 83), sequence 32 (6, 26).
CI stays at warn (count is not 0).
Checks: validate 0 errors; ci-coverage 0 problems; grade-all --code --strand ai 0 failures.
