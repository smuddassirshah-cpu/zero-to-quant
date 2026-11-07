# coding-int level 3: performance task

`homework-3.json`, `h3-notes-drive`, item 9 of 9 (added; cap 12). Kind `code` (Python).

Objective: l12 "Design classes for a small file system...". Chosen over l14: the homework already has three rate-limit items and no file-system item.

Task: seven-method stub; `rm`, `mv` with refusals, replacing `write` and an O(path) `size` are not solved in l12.

Tests: 10 hidden, 2 examples. Twelve planted wrong solutions each fail their named test (script), including a `size` of a file that gives 0 (test 3) and a `mkdir` that replaces a folder (test 5). Walking `size`: 0.24 s against 17.1 s in CPython; stopped at 5 s on test 10 in Pyodide (scratch copy).

Gates:
1. `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors; only the expected perf-pending warning.
2. `VOICE_BASE=app/content/courses/coding-int python3 docs/reviews/voice-scan.py 35`: 0 and 0.
3. `python3 -I docs/reports/coding-int-3-perf-numbers.py`: exit 0 (solution and a flat dict reference).
4. `node tools/playthrough.mjs --set coding-int/homework-3 --local-cdn <pkgs>`, with and without `--mobile`: All passed; starter fails. Shots read cleanly.

Freshness grep: `mv(`, `rm(`, `rename`, `move`, `size(`, `NotesDrive` (was `FileSystem`), `file system`, `total`.

Fix pass notes:
- `mkdir`, `read` and `ls` keep l12's behaviour on purpose; `write` now replaces, and `rm`, `mv` and path-cost `size` are new. The class is `NotesDrive` and the harness `run_drive`, so the code names no longer match l12's.
- `fresh-check --file` hits: `FileSystem` and `run_fs` (l12 screens 4 and 7, now renamed) and `big_case`, a hidden postlude helper shared with research-int and coding-int homework-1.
