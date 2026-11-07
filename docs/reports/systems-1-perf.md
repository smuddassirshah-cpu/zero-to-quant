# systems level 1: performance task (PLAN 2a Phase 3)

- File: `app/content/courses/systems/homework-1.json`, item `h1-branch-aloud`, index 7 (item 8 of 8; was 7, nothing converted).
- Kind `aloud` (120 s, 30 s think, 3 follow-ups). Objective: l5 "Explain branch prediction and remove a branch from a hot loop."
- Why not `code`: hidden tests grade behaviour, so a loop that keeps its branch passes; l5 itself says clang emits a conditional move at `-O1`, so timing cannot tell either. Why not l3 (pages, TLB, page fault): the same homework already holds an aloud model on exactly that (`h1-a-i-aloud`), so it would not be fresh.
- Task: a filter loop with a conditional store (`out[k++]`), 10,000,000 prices, 30% kept at random. New against l5, whose loops are running sums with a mask.
- Rubric: 3 (predictor, required) + 2 (15 ms against 10 ms) + 3 (always-store rewrite, room for `n`, required) + 2 (when it does not help, measure). A pass needs both required rows and one more.
- Gates: (1) `cd app && node tools/validate.mjs`: 0 errors (expected perf-pending warning). (2) `VOICE_BASE=app/content/courses/systems python3 docs/reviews/voice-scan.py 35`: 0 and 0. (3) `python3 -I docs/reports/systems-1-perf-numbers.py`: exit 0 (closed forms and the exact two-bit rate 210/580, against a seeded simulation and a native run of both loops). (4) `node tools/playthrough.mjs --set systems/homework-1 --local-cdn <pkgs>`, with and without `--mobile`: All passed; 440 px shots checked.
- Freshness grep: `k++`, `out[`, compact, filter, cmov, conditional move (l5 only, running sum). `fresh-check --file`: 0 hits.
