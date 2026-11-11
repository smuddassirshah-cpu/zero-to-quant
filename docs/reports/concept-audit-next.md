# Concept audit: next (11 Nov 2026, audit session 5)

State: `docs/reports/concept-audit-log.md` (rounds), `concept-audit-notes.md` (decisions, issues). Branch `claude/fable-audit`; the content session merges it.

Closed: mental-pressure, puzzles, game-theory, brainteasers, coding-int, research-int, systems, pdes, pairs-rep, mental, number-sense, ito, measure-prob, numerics, odes L1 to L3, and new this session mm-games (L1 to L3 on round 2, L4 on round 1), recruiting L1 to L3, and delta batch 1 for eight courses (puzzles, game-theory, brainteasers, coding-int, research-int, systems, ito, measure-prob).

Open: nothing in a fix pass. odes L4 is eligible from 14:43 UTC, 11 Nov.

Next: odes L4; counting-chance, conditional, random-vars, limits-thm, markov (quiet from 16:46 UTC, 11 Nov, if untouched); then the trader and developer closures, Stage 1 first. Eligible, not started: garch, stat-learning, stat-models; vector-calc from 14:43 UTC. Delta batch 2 is owed: pdes (33 lines), number-sense and odes fluency sets.

For a human: recruiting has 33 firm, date and pay facts not checked at source. Six graded keys rest on Optiver's 8-month retake rule (list in the notes).

For the content session: order keys that reject valid orders were found three times; a validator rule is raised in `docs/BACKLOG-INBOX.md`.

Miss rate: session 1, 39 levels, 132 audit-only findings, 12 `wrong`. Session 2, 6 levels, 20, 1. Session 3, 6 levels, round 1: 35, 7. Session 4, 6 levels: 64, 4. Session 5, 4 new levels plus 3 re-read: 45 audit-only, 3 `wrong`; delta batch 9, 1 `wrong`.

## Verdict

Session 5, levels audited: 4 new (61 in all), plus mm-games L1 to L3 round 2 and one delta batch.
Serious audit-only findings: 7. All fixed.
- `mm-games/l15-arbitrage-in-a-book.json`, `l16-several-contracts.json`, `homework-4.json` items[0]: arbitrage defined as "payoffs cancel on every outcome"; `find_arb` returned 0 on a sure profit (imprecise, code).
- `mm-games/l15-arbitrage-in-a-book.json` screens[7], screens[9], summary; `review-4.json` items[4]: board rule for "exclusive outcomes" without "one must happen" (imprecise).
- `mm-games/homework-2.json` items[2]: `order` key rejected valid orders (imprecise, graded key).
- `mm-games/homework-3.json` items[2]: the same (imprecise, graded key).
- `mm-games/l13-full-game.json` quiz[0]: a distractor was true (imprecise, graded key).
- `recruiting/l3-the-calendar.json` screens[8]: US cycle taught as opening in July and August for all firms (imprecise; now a range, as reported).
- `recruiting/l7-projects-that-count.json` screens[10]; `homework-2.json` model: survivorship said to flatter a long-short result; either sign (imprecise).
Delta batch: 0 serious.
Minor: 47 audit-only (mm-games L4 10, mm-games round 2 11, recruiting 17, delta 9), plus 13 from fix-pass reads. Fix-pass reads found 0 `wrong`.
Serious per three levels: 3.0 on the 4 new levels (4 serious), 3.0 on all 7 levels read (7 serious).
