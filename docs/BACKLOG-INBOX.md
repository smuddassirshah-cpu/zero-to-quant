# Engine backlog inbox

Content agents append their engine and canvas limitations here, under `Raised later (<course> level <n>):`, as bullets. An integration pass numbers them into `ENGINE-BACKLOG.md` and clears this file.


Cleared by engine pass 8 (items up to 1146 in `ENGINE-BACKLOG.md`); the previous text is in the commit before it.
Raised later (exam second item 1.3-1.4):
- No tool lists the (exam, essential skill) pairs with one auto item; each author recomputes them by hand from the exams, every `course.json` and its reviews. A validator warning per topic or stage exam (skill tagged on a level review of the exam's courses, fewer than two non-longform items) would stop a later edit, such as a reader's swap, from bringing a pair back.

Raised later (exam second item 1.5):
- Graph canvas (`markov: true`) at 440 px: a four-node chain in a row draws at about 330 px wide with small nodes, so the label on a short edge (topic-1.5 `e-floor-walk`, 2 to 3) sits tight between the nodes. A width-filling layout or a minimum node radius on phones would help.
