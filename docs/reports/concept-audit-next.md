# Concept audit: next (10 Nov 2026, audit session 2)

State: `docs/reports/concept-audit-log.md` (rounds), `concept-audit-notes.md` (decisions, issues). Branch `claude/fable-audit`; the content session merges it.

Closed: mental-pressure, puzzles, game-theory, brainteasers, coding-int, research-int, systems, pdes, pairs-rep (all levels; the round-2 finding 3 dispute is settled, `upheld in part`, fixed), ito L1 to L3, measure-prob L1 to L3, and new this session mental L1 to L3 and number-sense L1 to L3.

Open: ito L4, measure-prob L4, mm-games, recruiting and the topic 1.5 courses were not eligible (content commits on 9 Nov, 18:21 to 23:15 UTC, touched 69 of 79 course folders). Minor: number-sense l11 screens[8] root claim fails at 0 (notes).

Next, in order, as each passes 24 quiet hours: ito L4, measure-prob L4; mm-games; recruiting; counting-chance, conditional, random-vars, limits-thm, markov; the rest of the trader and developer closures, Stage 1 first; other route courses. Closed courses touched on 9 Nov (brainteasers, game-theory, puzzles, research-int, systems, coding-int, pdes) need a delta audit of the changed files. Run `git fetch --unshallow` before rebasing.

Miss rate: session 1, 39 levels, 132 audit-only findings, 12 `wrong`. Session 2, 6 levels, 20 audit-only findings, 1 `wrong`, overlap with the earlier read 0.

## Verdict

Session 2, levels audited: 6 (45 in all).
Serious audit-only findings: 2.
- `mental/l8-squaring.json` screens[4].explain, screens[6].prose, summary.ideas[2], objectives[2]: either-side shortcut stated without "the same distance" (imprecise).
- `number-sense/l12-which-first.json` quiz[2].explain.text: tools said to read −3² as −9; a spreadsheet gives 9 (wrong).
Minor: 18. Serious per three levels: 1.0.
