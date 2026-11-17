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

Raised later (problems ito):
- Playthrough at 440 px passes a part whose inline maths overflows the page: one KaTeX span holding a comma list (`$W = 0, 0.3, -0.2, 0.4, 0.6$`) does not wrap, widened the whole card and clipped the question text, yet `--problems ito/problems-2 --shots` was green. Fail a part when `document.documentElement.scrollWidth` exceeds the viewport, as the homework `-marked` shot already does for `.katex-display`.
- `retold` learns stock sentences from committed content, so an instruction line repeated across new sets ("Read $\Phi$ from software or a normal table, and give 4 decimal places.", the wording `[table-source]` asks for) fires as a retelling between the new sets themselves. Treat a sentence that only meets `[table-source]` or `[answer-form]` as stock, or list such lines in the stoplist.

Raised later (problems algebra):
- `playthrough.mjs --problems <course>/problems-<n>` on a new set fails as "the level review's card ... has no Problem set row" and "the set opened in state empty" when `content/manifest.json` was restored with `git checkout` (as the commit rule asks) after the last validator run. The fix is to rerun `validate.mjs` first; the playthrough could say "set not in manifest.json: run tools/validate.mjs" instead.

Raised later (problems measure-prob):
- `fresh-check` same-course reuse warns when a choice option names the four modes of convergence in the usual order ("almost surely, in probability, in mean square and in distribution"), which any modes item must say. Workaround: problems-2 `p-root-of-uniform` part 5 reworded its options. A list of fixed course vocabulary that does not count towards a shared run would stop these warnings.
- After `git checkout app/content/manifest.json` (the commit rule), `playthrough.mjs --problems <set>` fails with "the set opened in state empty, not its start card" and a 20 s timeout until the validator rewrites the manifest. The playthrough could rebuild the manifest itself, or say that the set is missing from it.

Raised later (problems pdes):
- `fresh-check.mjs` reports a `rate` reuse error for a universal constant: the Gibbs overshoot fraction (8.95% of the jump, 0.0895 in `pdes` l7 screen 1, with 1.179 in both) was flagged on a new problem about a different function. Constants such as the Gibbs fraction, $\Phi^{-1}(0.975) = 1.96$ or $\ln 2$ should not count as a shared rate; a short allow-list would do. Workaround: the part was rewritten to end on a different result.
- `playthrough.mjs --problems` on a new set after `git checkout app/content/manifest.json` (as the brief asks before each commit) fails with "the level review's card on the course page has no Problem set row" and "opened in state empty", because the manifest no longer lists the set. Have the playthrough say "set missing from manifest.json: run tools/validate.mjs first", or rebuild the manifest itself.

Raised later (problems topology):
- `playthrough.mjs --problems ... --mobile` stays green when one long inline KaTeX span (a list of eight finite open sets in a problem's `prose` and a part's `question`) runs past the right edge at 440 px; the 440 px shots showed the text clipped. Have the mobile check measure KaTeX spans against their column, or have the validator warn on one maths span over about 45 characters in set text.
- `fresh-check.mjs --file` reports a hit in another course (`analysis` l17, `limits` l17: $x^3 - 3x$ with its interval) under the label `[same-course-reuse] error`. The label should say cross-course, or the rule should say whether other courses count.
