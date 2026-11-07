# coding-int level 3: performance task (retrofit)

File `app/content/courses/coding-int/homework-3.json`, item `h3-notes-drive`, item 9 of 9 (added; homework was 8, cap 12). Kind `code` (Python).

Objective: l12 "Design classes for a small file system with paths, folders and files." Chosen over l14 (rate limiter) because the homework already holds three rate-limit items (`h3-hit-counter`, `h3-rate-limit-aloud`, `h3-boundary`) and none on the file system. Design that runs, so `code`.

Task: from a seven-method stub, `mkdir`, `write` (replaces), `read`, `ls`, `rm`, `mv` (refusals) and `size`, every method but `ls` in time proportional to path length. Lesson l12 solves only `mkdir`, append-`write`, `read`, `ls` and a walking `size`; `rm`, `mv`, replacing writes and a cached total are new.

Tests: 10 hidden, 2 examples. Planted wrong solutions (10, in the script) each fail their named test: append or wrong delta (3), parents made before refusals (6), string-prefix "inside" (7), `mv` or `rm` leaving totals (2, 4), `rm /` clearing (4), overwrite on `mv` (6), `ls` of a file (1). Walking `size`: 0.24 s against 17.1 s (CPython); in Pyodide it stopped at 5 s on test 10 (scratch copy, restored).

Gates:
1. `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors; expected "coding-int/L3: has a performance task, remove from perf-pending"; no warning on item 9.
2. `VOICE_BASE=app/content/courses/coding-int python3 docs/reviews/voice-scan.py 35`: 0 and 0.
3. `python3 -I docs/reports/coding-int-3-perf-numbers.py`: 0 failures, exit 0 (two routes: solution and a flat dict reference).
4. `node tools/playthrough.mjs --set coding-int/homework-3 --local-cdn <pkgs>`, with and without `--mobile`: All passed, starter fails. Shots at 1280 and 440 read cleanly.

Freshness grep: `mv(`, `rm(`, `rename`, `move`, `size(`, `FileSystem`, `file system`, `total`.
