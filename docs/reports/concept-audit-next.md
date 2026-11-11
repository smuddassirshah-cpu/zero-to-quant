# Concept audit: next (11 Nov 2026, audit session 6)

State: `docs/reports/concept-audit-log.md` (rounds), `concept-audit-notes.md` (decisions, issues). Branch `claude/fable-audit`; the content session merges it.

Closed: mental-pressure, puzzles, game-theory, brainteasers, coding-int, research-int, systems, pdes, pairs-rep, mental, number-sense, ito, measure-prob, numerics, odes L1 to L3, mm-games, recruiting L1 to L3, delta batch 1, and new this session counting-chance L1 to L3 (round 1).

Open, both with fix passes merged and gates green, each owing one more blind read:
- odes L4: round 1 found 3 `wrong` in one level. Round 2 owed.
- conditional L1 to L3: round 1 found 2 `wrong`, round 2 found 2 more. Round 3 owed.

Next: odes L4 round 2; conditional round 3; conditional L4 and L5; random-vars, limits-thm, markov; then the trader and developer closures, Stage 1 first. Eligible, not started: garch, stat-models, vector-calc. Delta batch 2 is owed: pdes, odes fluency sets, and number-sense once quiet. Tell every auditor to hand-check each claim and not template verdicts (see notes).

Miss rate: session 1, 39 levels, 132 audit-only findings, 12 `wrong`. Session 2, 6 levels, 20, 1. Session 3, 6 levels: 35, 7. Session 4, 6 levels: 64, 4. Session 5, 4 new levels plus 3 re-read: 45, 3. Session 6, 7 new levels: 47 audit-only, 6 `wrong`; conditional round 2: 9 more, 2 `wrong`.

## Verdict

Session 6, levels audited: 7 new (68 in all), plus conditional L1 to L3 round 2.
Serious audit-only findings: 6. All fixed.
- `odes/l18-four-decimal-places.json` screens[3]: an error under 5e-5 said to make four printed decimals agree (wrong).
- `counting-chance/l7-replacement.json` screens[4].explain; `homework-2.json` items[7], items[8]: independence defined as "chances never change" (imprecise).
- `conditional/l3-shrinking.json`: "at least one is a 5" with no protocol for the news; the wrong option 1/6 is right if a random die is reported (imprecise).
- `conditional/l12-many-hypotheses.json` generalise: "priors add to 1" without mutual exclusivity (imprecise).
- `conditional/l16-conditional-independence.json` summary.trap: "add before you multiply" gives the trap answer 0.25, not 0.34 (wrong).
- `conditional/l12-many-hypotheses.json` screens[3].explain, round 2: a hypothesis "lost a little" when it rose from 1/3 to 3/7 (wrong).
Minor: 52 audit-only (odes L4 9, counting-chance 14, conditional 20, conditional round 2 9), plus 8 from fix-pass reads. Fix-pass reads found 0 `wrong`.
Serious per three levels: 2.1 on the 7 new levels (5 serious), 1.8 on all 10 levels read (6 serious).
