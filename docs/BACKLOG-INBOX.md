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
