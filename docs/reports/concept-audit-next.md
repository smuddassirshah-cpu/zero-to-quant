# Concept audit: next (10 Nov 2026, audit session 3)

State: `docs/reports/concept-audit-log.md` (rounds), `concept-audit-notes.md` (decisions, issues). Branch `claude/fable-audit`; the content session merges it.

Closed: mental-pressure, puzzles, game-theory, brainteasers, coding-int, research-int, systems, pdes, pairs-rep, mental L1 to L3, number-sense L1 to L3, ito L1 to L3, measure-prob L1 to L3, and new this session odes L1 to L3 and numerics L1 to L3 (three rounds each; round 3 found 0 `wrong`).

Open, first for the next session: odes L4; numerics L4 with a delta read of the four code widgets the round-3 fix pass rewrote (numerics l5, l6, l10, homework-2; notes).

Next, as each passes 24 quiet hours (content commits of 9 Nov ran 14:47 to 23:15 UTC): ito L4, measure-prob L4; mm-games; recruiting; counting-chance, conditional, random-vars, limits-thm, markov; the trader and developer closures, Stage 1 first; other route courses. Delta audits owed for closed courses touched on 9 Nov. Eligible but not started: garch, stat-learning, stat-models, vector-calc.

For the content session: numerics `course.json` still names l6 "A root finder that never fails" (notes). Merge the content branch, do not rebase, when audit commits are already pushed (notes).

Miss rate: session 1, 39 levels, 132 audit-only findings, 12 `wrong`. Session 2, 6 levels, 20, 1 `wrong`. Session 3, 6 levels: round 1, 35 audit-only, 7 `wrong`; round 2, 21 audit-only, 4 `wrong`; round 3, 14 audit-only, 0 `wrong`.

## Verdict

Session 3, levels audited: 6 (51 in all), three rounds each.
Serious audit-only findings: 11 (round 1: 10; round 2: 1; round 3: 0). All fixed.
- `odes/l1-equations-about-rates.json` screens[9].prose, `homework-1.json` items[3]: uniqueness without its smoothness hypothesis (imprecise).
- `odes/l7-characteristic-equation.json` screens[4], [5], `l9` screens[2]: envelope e^{-t} stated and drawn without the amplitude (wrong).
- `odes/l8-forcing.json` screens[8].prose: "multiply the guess by t" fails at y''+y'=t and double roots (imprecise).
- `odes/l12-stability.json` screens[5], [7]: "stable" in two senses (imprecise).
- `numerics/homework-1.json` items[8].rubric[2]: rubric credits "variance is well conditioned"; κ ≈ 5e8 (wrong).
- `numerics/l4-stability.json` screens[4], `review-1.json` items[3]: QR "loses log10 κ digits" without the small-residual condition (imprecise).
- `numerics/l5-bisection-and-newton.json` screens[5]: Newton order 2 without a simple root (imprecise).
- `numerics/l5` summary.ideas[0], `l6` screens[3]: sign change without continuity (imprecise).
- `numerics/l7-interpolation.json` screens[5]: Runge blamed on an exploding node product, for all equal spacing (wrong).
- `numerics/l9-quadrature.json` screens[6], [9]: "put kinks on nodes"; an odd node keeps order 2 (wrong).
- Round 2, `numerics/l5` screens[8], `l6` screens[7]: bracket test `flo * fhi > 0` loses a root at an endpoint and underflows (wrong, code).
Also serious, found by both reads: `numerics/l6` "36: the guaranteed cap" (the solution returned a non-root after 102 calls).
Minor: 59 (round 1: 25; round 2: 20; round 3: 14). Serious per three levels: 5.0 on round 1, 0.5 on round 2, 0 on round 3.
