# Engine 698: rubric-passes

`app/tools/rubric-passes.mjs` enumerates every tick set of a longform rubric (flat `rubric` or `widget.rubric`), using the engine's rule from `longform.js` (`PASS = 7` points, every `required: true` row ticked). It prints the numbered rows, the minimal passing sets and "can be left out" per row; `--json` gives the same as data; exit 0 always. Modes: `--item file#id`, `--course`, `--all`.

Test: `node tools/test-rubric-passes.mjs` (five fixtures: none, one, three, all required, points summing to 12) passes.

Summaries:
- research-int: 2 items, both aloud; minimal set is rows 1, 2, 3 (all required); row 4 can be left out.
- measure-prob: 3 derivation items; each has 3 to 5 minimal sets of 3 rows (7 to 8 points) and four of five rows can be left out, so a pass can skip a named part.

AUTHORING section 5 paragraph added; backlog 698 marked Done.
