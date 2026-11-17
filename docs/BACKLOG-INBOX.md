# Engine backlog inbox

Content agents append their engine and canvas limitations here, under `Raised later (<course> level <n>):`, as bullets. An integration pass numbers them into `ENGINE-BACKLOG.md` and clears this file.


Cleared by engine pass 8 (items up to 1146 in `ENGINE-BACKLOG.md`); the previous text is in the commit before it.
Raised later (exam second item 1.3-1.4):
- No tool lists the (exam, essential skill) pairs with one auto item; each author recomputes them by hand from the exams, every `course.json` and its reviews. A validator warning per topic or stage exam (skill tagged on a level review of the exam's courses, fewer than two non-longform items) would stop a later edit, such as a reader's swap, from bringing a pair back.

Raised later (exam second item 1.5):
- Graph canvas (`markov: true`) at 440 px: a four-node chain in a row draws at about 330 px wide with small nodes, so the label on a short edge (topic-1.5 `e-floor-walk`, 2 to 3) sits tight between the nodes. A width-filling layout or a minimum node radius on phones would help.
Raised later (exam second item stage0):
- A numeric `answers` set (unordered) draws the same narrow field as a single number: at 440 px a placeholder of 26 characters ("angles, separated by commas") was cut off, and four angles typed with commas fill the box. Workaround: placeholder "angles, with commas" on `topic-0.3` `e-double-angle-roots`. Widen the field for a set, or size it to the expected count.

Raised later (exam second item 1.6-1.11):
- An `expression` set (`answers` with `unordered`) cannot take `form`, so a set of complex roots accepts the prompt typed back (`\sqrt{15-8i}, -\sqrt{15-8i}` grades right by value). Allow `form: "rectangular"` per value in a set; topic-1.11 `e-square-root-parts` asks for one root with `form` instead.
- A fenced code block inside a `multi` or `choice` option neither wraps nor scrolls at 440 px: lines past about 36 characters are clipped (seen on topic-1.9 `e-swapped-d` before rewrapping). Give option code blocks `overflow-x: auto`, or have the validator warn on option code lines over 34 characters.

Raised later (triage pass 8 hits):
- `same-course-reuse.mjs` and `retold-reuse.mjs`, `[slip-line]`: a slip line with no number, maths or story word ("You doubled the tail.", "You divided the run by the rise.", "You multiplied matching entries.", "You added the two parts.") is stock. 79 of the 189 warnings rest on one pair that is such a line (33 distinct lines; eight of them make 48 hits), and every one is waived by hand here. Do not warn when such a line is the only pair of a hit; a list in `tools/stock-slip-lines.json`, or the test "no digit, no maths, at most eight words", would do it. The same holds with an exam source: 7 of the 13 exam hits are these lines.
- `[slip-line]` with numbers: 69 warnings pair a line with the same line in other numbers ("You multiplied the sd by 52." against "by 252."), plus 10 of the carry form "You used x, part k's slip". None is reuse. Warn only when the two lines share a number of two or more figures or a run of numbers (`p-order-sizes`: "$2 + 0 + 2 + 4$"), or when every sentence of the feedback is equal with no number masked (`p-relative-strength`, `p-rent-ridge`, `p-price-spikes`). Those three tests find all five course-source `reuse` verdicts of this list.
- `[working-band]`: do not fire when `explain.text` prints the key at the asked places before its last figure (`stat-learning/problems-1` `p-heat-demand`: "falls from 1.80 to 1.476 but no further than $1.20 + 0.24 = 1.44$"). Keep it when the key is nowhere in the text (`coint/problems-1`: the text stops at 1,104.4 and the key is 1,105).
- `[rounding-tie]` on a `wrong` value: skip when the band it asks for would meet another `wrong` band of the part, or when one rounding is already a `wrong` value (`trig/problems-1` `p-hexagon-tile`: 0.5 rounds to 1, which is `radians-whole`).
- `[table-source]` reads only the words; it does not test that the key's band takes a 2-place table reading. `garch/problems-1` `p-stale-alarm` refuses both table readings (19.0% and 19.4% against a band of 19.14% to 19.26%). A check "the band takes the tail at $z$ rounded to 2 places" would find such parts.
- A waiver keyed by line: a `source` object takes `text`, which is how the waiver block of `docs/reviews/review-pass8-hits.md` pins each waiver to its line. A top-level `text` on a waiver with no `source` file (clear this line of this item against any source) would make each entry one line and one reason.
- The same-course checker does not see a shared parameter across a problem and an exam item when the story is told in other words: `p-fund-managers` (0.9 over 9 years) against `s-sharpe-p` (0.6 over 9 years) fired on the stock line alone. A `numbers` test on "x over n years" style givens of one skill would have caught it.
