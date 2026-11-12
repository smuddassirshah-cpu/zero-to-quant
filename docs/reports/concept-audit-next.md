# Concept audit: next (12 Nov 2026, audit session 8)

State: `docs/reports/concept-audit-log.md` (rounds), `concept-audit-notes.md` (decisions, issues). Branch `claude/fable-audit`; the content session merges it.

Closed: mental-pressure, puzzles, game-theory, brainteasers, coding-int, research-int, systems, pdes, pairs-rep, mental, number-sense, ito, measure-prob, numerics, mm-games, recruiting L1 to L3, counting-chance L1 to L3, odes, conditional, delta batch 1, and new this session random-vars L1 to L3 (round 2, 0 `wrong`).

Open, fix pass merged, fix-pass read done and gates green, each owing a round 2 blind read:
- random-vars L4 and L5: round 1 found 3 `wrong` (all minor), 1 serious.
- limits-thm L1 to L3: 2 `wrong` (both minor), 1 serious.
- markov L1 to L3: 2 `wrong` (1 serious), 2 serious in all.

Next: the three round 2 reads; then limits-thm L4, markov L4 and L5; then the trader and developer closures, Stage 1 first. Eligible, not started: garch, stat-models, vector-calc. Delta batch 2 is owed: pdes, odes fluency sets, number-sense once quiet. Tell auditors and fixers to hand-check, and name the independence class and slip feedback against its value. Merge the content branch; do not rebase.

Miss rate: sessions 1 to 7 as logged (73 levels). Session 8, 8 new levels: 63 audit-only findings, 7 `wrong`; one re-read (3 levels): 10 more, 0 `wrong`.

## Verdict

Session 8, levels audited: 8 new (81 in all), plus a re-read of random-vars L1 to L3.
Serious audit-only findings: 4, all on the new levels. All fixed.
- `random-vars/l18-random-sums.json` summary.ideas[2], screens[8], quiz[2]: random-sum formulas "fail" if N depends on the terms (imprecise).
- `limits-thm/l12-skill-or-luck.json` screens[5]: Sharpe ratio defined with no risk-free rate (imprecise).
- `markov/l6-always-settle.json` summary.ideas[1], screens[6].feedback.byKey.unique: a reducible chain has many stationary distributions (wrong).
- `markov/problems-3.json` items[1].parts[3]: expected pay-out called a "fair price" (misleading).
Minor: 69 audit-only (59 on new levels, 10 on the re-read), plus 2 from fix-pass reads. Fix-pass reads found 0 `wrong`.
Serious per three levels: 1.5 on the 8 new levels; 1.1 on all 11 levels read.
