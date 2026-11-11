# Concept audit: next (11 Nov 2026, audit session 7)

State: `docs/reports/concept-audit-log.md` (rounds), `concept-audit-notes.md` (decisions, issues). Branch `claude/fable-audit`; the content session merges it.

Closed: mental-pressure, puzzles, game-theory, brainteasers, coding-int, research-int, systems, pdes, pairs-rep, mental, number-sense, ito, measure-prob, numerics, mm-games, recruiting L1 to L3, counting-chance L1 to L3, delta batch 1, and new this session odes (L4 round 2, course fully closed) and conditional (L1 to L3 round 3, L4 and L5 round 1, course fully closed).

Open, fix pass merged and gates green, owing one more blind read:
- random-vars L1 to L3: round 1 found 2 `wrong`, both serious. Round 2 owed.

Next: random-vars L1 to L3 round 2; random-vars L4 and L5; limits-thm, markov; then the trader and developer closures, Stage 1 first. Eligible, not started: garch, stat-models, vector-calc. Delta batch 2 is owed: pdes, odes fluency sets, number-sense once quiet. Tell every auditor to hand-check each claim, and to look for independence stated as necessary and for puzzles with no stated protocol (see notes). If the audit branch has unmerged commits, merge the content branch; do not rebase.

Miss rate: session 1, 39 levels, 132 audit-only findings, 12 `wrong`. Session 2, 6 levels, 20, 1. Session 3, 6 levels: 35, 7. Session 4, 6 levels: 64, 4. Session 5, 4 new plus 3 re-read: 45, 3. Session 6, 7 new: 47, 6; conditional round 2: 9, 2. Session 7, 5 new levels: 21 audit-only, 3 `wrong`; two re-reads (4 levels): 7 more, 1 `wrong`.

## Verdict

Session 7, levels audited: 5 new (73 in all), plus re-reads of odes L4 and conditional L1 to L3.
Serious audit-only findings: 9, all on the new levels. All fixed.
- `conditional/l18-monty-hall.json` screens[1], [6], [7]: "the host could never open door 1, so nothing new", against the lesson's own lazy-host quiz; no "always", no tie-break (misleading).
- `conditional/review-4.json` items[0]: key 1/3 with no tie-break rule (imprecise).
- `conditional/l19-bertrands-box.json` screens[7], quiz[3]: clerk's rule unstated; 2/3 marked wrong (imprecise).
- `conditional/l20-two-children.json` screens[2], [3], [6], [9], with l21, review-4, homework-4: "you learn at least one" with no protocol; 1/2 marked wrong (imprecise).
- `conditional/l21-tuesday-boy.json` screens[9]: 10:17 report; 0.43 marked wrong, right under the natural reading (imprecise).
- `conditional/l24-simpsons-paradox.json` screens[5], summary.trap: "always compare like with like" with no causal condition (imprecise).
- `random-vars/l7-linearity.json` screens[2].explain: argument said to use no independence when it did (wrong).
- `random-vars/l7-linearity.json` quiz[2].explain; `homework-2.json` items[6]: product rule "fails for dependent variables" (wrong).
- `random-vars/l11-moving-together.json` summary.trap: scaling leaves ρ unchanged, without "positive" (imprecise).
Minor: 19 audit-only (conditional L4 and L5 5, random-vars 7, odes L4 round 2 4, conditional round 3 3), plus 4 from fix-pass reads. Fix-pass reads found 0 `wrong`.
Serious per three levels: 5.4 on the 5 new levels; 3.0 on all 9 levels read.
