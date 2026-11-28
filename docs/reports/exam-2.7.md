# Topic exam 2.7 (Deep learning)

`app/content/exams/topic-2.7.json`, built by `docs/briefs/exam-2.7-scripts/build.py` (code items in `code_items.py`). 32 items at a ramp of 6, 16, 7 and 3; 9 items with parts and 2 code items. `minutes` is 105 (paces add to 94.8 min) and `pass` is 0.7. All 16 skills of `nn-train`, `cnn`, `sequence` and `representations` are on 2 or 3 items.

Exit: items[30] is the digits CNN forward in NumPy alone on the supplied exit weights, 532 of 540 held out (0.9852), checked at 0.95 and recomputed by `cnn_ops_l3`. items[31] is multi-head attention with causal and padding masks; a fully masked row gives zeros, as `seq_ops_l3.attention` does.

The code items carry 7 and 10 mutants; each first fails its named test, and every `byKey` line is reachable.

Checks: validator 0 errors. Voice scan 0 and 0. `check_numbers.py` passes strict through the runner (656 checks, 0 uncovered). Fresh-check 0 hits; same-course reuse names no exam error. `grade-all --code --strict-feedback` 0 failures. Playthrough green, plain and `--mobile`.

Notes: `cnn` states its exit bar as 0.98, so the exam says "this exam's check" for its 0.95. Padding masks are not taught in `sequence`; items[31] states the rule in full.
