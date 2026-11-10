# Concept audit: next (10 Nov 2026, audit session 4)

State: `docs/reports/concept-audit-log.md` (rounds), `concept-audit-notes.md` (decisions, issues). Branch `claude/fable-audit`; the content session merges it.

Closed: mental-pressure, puzzles, game-theory, brainteasers, coding-int, research-int, systems, pdes, pairs-rep, mental, number-sense, odes L1 to L3, and new this session ito L4, measure-prob L4, numerics L4 with its delta read (ito, measure-prob and numerics are now fully closed).

Open, first for the next session: mm-games L1 to L3 round 2 (blind, fresh reader; round 1 found 2 `wrong`, fix pass and fix-pass read merged); odes L4 (eligible from 14:43 UTC, 11 Nov).

Next: mm-games L4; recruiting; counting-chance, conditional, random-vars, limits-thm, markov (quiet from 16:46 UTC, 11 Nov); the trader and developer closures, Stage 1 first; other route courses. One delta batch is owed for closed courses touched on 9 and 10 Nov. Eligible, not started: garch, stat-learning, stat-models, vector-calc.

For the content session: lesson numbers in learner text (lists in the three new audit files); numerics `course.json` l6 name (notes, session 3).

Miss rate: session 1, 39 levels, 132 audit-only findings, 12 `wrong`. Session 2, 6 levels, 20, 1. Session 3, 6 levels, round 1: 35, 7. Session 4, 6 levels: 64 audit-only (67 with the delta), 4 `wrong`.

## Verdict

Session 4, levels audited: 6 (57 in all), one round each.
Serious audit-only findings: 6. All fixed.
- `ito/l15-moments-quickly.json` screens[5].prose, screens[5].explain: symmetry rule backwards, "odd in total and nonzero" (wrong).
- `ito/l14-hitting-and-exit.json` screens[1].feedback.byKey.x1: optional stopping from "a bounded stopped value or a finite mean time" (imprecise).
- `ito/homework-4.json` items[0].feedback.byKey.x1: the same sentence (imprecise).
- `mm-games/l11-hedging.json` screens[1], [2], summary; `review-3.json` items[4]: hedge ratio from per cent deviations read as units per unit (imprecise).
- `mm-games/l13-full-game.json` screens[4]; `review-3.json`; `homework-3.json`: realised P&L labelled "edge" (imprecise).
- `mm-games/homework-3.json` items[0] `make_script`: hedge traded after the first card is shown; six test values recomputed (misleading, code).
measure-prob L4 and numerics L4: 0 serious.
Minor: 61 audit-only (ito 13, measure-prob 9, numerics 17 with 3 delta, mm-games 22), plus 11 from fix-pass reads. Serious per three levels: 3.0.
