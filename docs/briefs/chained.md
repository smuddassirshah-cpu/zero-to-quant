# Brief: chained problems (PLAN 2d item M; gap file row M and order of work 3)

Exams and interviews set problems of several steps where each step feeds the next. The app has few: 3% of items. This adds a problem set to every maths, probability and statistics level: three to five chained problems, each intermediate answer graded.

## Home (decided session Z, DECISIONS "Chained problems")

A new per-level file `problems-<n>.json` beside `review-<n>.json`: `{ "id": "problems-<n>", "course", "level": n, "items": [3 to 5] }`. Not homework (fixed 45 minutes, capped at 12, not drawn by the weekly review) and not the review (capped at 10, a gate). Engine: ENGINE-BACKLOG 845 to 851, `docs/reports/engine-problems.md`; AUTHORING section 5 holds the binding shape.

## Rules for a problem

- Every item uses `parts` (AUTHORING "Follow-up parts"): three to five parts, each a typed or chosen answer the engine grades. No `longform` part, no self-marking.
- A real chain: part k + 1 uses the result of part k (a probability, a root, a derivative, a fitted value). Because a wrong part never blocks the next, each later part restates the value it needs ("Using $P(A) = \tfrac{3}{10}$ from part 1, ...") so one slip does not sink the whole item.
- One setting per problem, stated once in the item's `prose`. Each part asks one thing. The last part asks for the result the problem is about, not a restatement.
- A set covers the level: each problem draws on at least two lessons of the level, and every lesson of the level appears in at least one problem. Only ideas taught up to the end of the level.
- Difficulty 3 to 5; at least one 5 a set. `skills` from the level's lessons. Typed answers (`numeric`, `expression`) for at least two thirds of parts; `choice` only where the step is a judgement (which test, which rule).
- Fresh: no setup, numbers or story from any lesson, quiz, review, homework or exam of the course (`node tools/fresh-check.mjs`, judge each hit).
- Each part has `feedback` and an `explain` of at most three sentences giving the working with the item's numbers, and `wrong` entries for the slips a learner really makes, including the answer that follows from the commonest slip in the part before.
- Voice as AUTHORING section 6. £ for money.

## Checks (all required before hand-back)

1. `docs/reports/problems-<course>-numbers.py`, run with `<scratchpad>/venv/bin/python`: every stated number and every part's answer computed twice by different methods (exact with sympy or fractions, then numerically or by simulation or enumeration), and each `wrong` value shown to differ from the answer. Exit 0.
2. From `app/`: validator 0 errors, no new warnings on your files.
3. `node tools/playthrough.mjs --problems <course>/problems-<n> --local-cdn <pkgs>` for every set, and with `--mobile`: green.
4. Voice scan `docs/reviews/voice-scan.py 35` on the course folder: 0 and 0.
5. Report `docs/reports/problems-<course>.md`: table of set, item, parts, lessons drawn on, difficulty; fresh-check hits and your judgement. Engine limits to `docs/BACKLOG-INBOX.md` under `Raised later (problems <course>):`.

One agent per course, up to three levels at a time, committing per level. Do not edit engine files, `course.json`, lessons, reviews, homework or other courses. Never push.

## Order

Topic 1.5 first (`counting-chance`, `conditional`, `random-vars`, `limits-thm`, `markov`), then 1.3 (`limits`, `integrals`, `taylor`, `multivar`), 0.2 (`equations`, `functions`, `quadratics`), 0.3 (`counting`, `exp-log`, `series`, `trig`). Each set gets a second read (protocol 5).
