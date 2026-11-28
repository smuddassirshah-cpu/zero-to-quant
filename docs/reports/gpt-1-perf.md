# gpt level 1: performance task

`homework-1.json`, `h-bpe-class`, item 1 of 6. Kind `code` (Python).

Matched objective: l2-merging-pairs "Write the byte-pair encoding training loop and run its first merges by hand." (also l3 "Build an encoder and decoder from a list of merges, and measure bytes per token.").

Task: a byte-level BPE tokeniser class, `BPETokenizer`, with `train(text, n_merges)` (merges in `self.merges`), `encode(text)` and `decode(ids)`, from a stub starter (`class BPETokenizer: ...`).

Tests: 11 hidden, 2 examples. Toy merges, encode and decode; the tie in `toto koko` (first-seen rule, against an alphabetical rule); a cap of 2 merges; no repeated pair; empty text; a run of a's; round trips with £, € and an emoji; a second `train` replacing the first; 50 merges on the first 20,000 Shakespeare characters scored on the last 5,000 (round trip, more than 1.4 bytes per token against 1.4434 measured, and the ids of `there whether`, which a frequency-order encoder gets wrong). Mutants (ENGINE-BACKLOG 1263): smallest-pair tie (fails test 4), merges kept across `train` calls (test 10), frequency-order encoding (test 11). Solution time in Pyodide 0.27.7 (node, `tools/code-runner.mjs`): 485 ms for the Shakespeare case, under 3 ms for each other case; that case has `budget` 6000.

Gates:
1. `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors.
2. `VOICE_BASE=app/content/courses/gpt/ python3 docs/reviews/voice-scan.py 35`: 0 and 0.
3. `<venv>/bin/python docs/reports/gpt-L1-numbers.py`: exit 0, 251 of 251 checks.
4. `node tools/playthrough.mjs --set gpt/homework-1 --local-cdn <pkgs>`, with and without `--mobile`: all passed, the starter fails; `grade-all.mjs --file ... --code`: 0 failures (solution, starter, mutants).

Overlapping screens: l2-merging-pairs screens[8] to [10] (`pair_counts`, `merge`, `train_bpe`) and l3-encode-and-decode screens[8] (`encode`, `decode`). New here: one class holding state across calls, retraining, the tie in a fresh text, and held-out compression as a threshold. `fresh-check.mjs --file homework-1.json` reports the shared method name `encode` with l3 screens[8]: the class method is the same operation by design (the task assembles the level's parts), so the name is kept.
