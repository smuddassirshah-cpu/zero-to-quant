# ds level 4: performance task

`homework-4.json`, `h4-save-tree`, item 8 of 8 (added). Kind `code` (Python).

Matched objective: l14-binary-trees "Write traversals that handle the empty tree" (the level's only verb-rule objective).

Task: `save_tree` writes pre-order with `#` for every empty child; `load_tree` rebuilds the tree. The course never saves or rebuilds a tree.

Tests: 11 hidden, 2 examples. Twelve planted slips fail value tests first: empty tree as `''` (2); string values, global reading position (3); split into characters, 0 read as empty, right side first, BST insert (5); in-order, level-order, missing marks, `", "` (1). A `pop(0)` load passes in CPython (0.011 s) and Pyodide (scratch swap).

Gates:
1. `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors.
2. `VOICE_BASE=app/content/courses/ds python3 docs/reviews/voice-scan.py 35`: 0 and 0.
3. `python3 -I docs/reports/ds-4-perf-numbers.py`: exit 0.
4. `node tools/playthrough.mjs --set ds/homework-4 --local-cdn <pkgs>`, with and without `--mobile`: All passed; starter fails; no display equations.

Freshness grep: save, load, serial, encode, decode, rebuild, `'#'`, pre-order; `fresh-check --file`: `to_list` only (hidden prelude helper).

Overlapping screens: l14-binary-trees screens[2] (pre-order order) and [6] (`preorder`); new: the marks, the line format, rebuilding from it, two-digit, negative and 0 tokens.
