# Concept audit: next (12 Nov 2026, audit session 9)

State: `docs/reports/concept-audit-log.md` (rounds), `concept-audit-notes.md` (decisions, issues). Branch `claude/fable-audit`; the content session merges it.

Closed: mental-pressure, puzzles, game-theory, brainteasers, coding-int, research-int, systems, pdes, pairs-rep, mental, number-sense, ito, measure-prob, numerics, mm-games, recruiting L1 to L3, counting-chance L1 to L3, odes, conditional, delta batch 1, random-vars (all five levels, new this session), and new this session limits-thm L1 to L3 and markov L1 to L3 (round 2 each: 1 new `wrong`, minor; 0 `wrong` in fix-pass reads).

Open: limits-thm L4. Round 1 found 10 `wrong` in one level (3 serious). Fix pass merged, fix-pass read done, gates green. It owes a round 2 blind read. The level had no second read of its lessons, review or homework before the audit.

Next: limits-thm L4 round 2; markov L4 and L5 (check first whether a second read is on record; expect the limits-thm L4 pattern if not); then the trader and developer closures, Stage 1 first. Eligible, not started: garch, stat-models, vector-calc. Delta batch 2 is owed: pdes, odes fluency sets, number-sense once quiet. Tell auditors and fixers to hand-check, to check auditor fix text as a claim, to name slip feedback against its value, and to use their own temp folder. Merge the content branch; do not rebase.

Miss rate: sessions 1 to 8 as logged (81 levels). Session 9, 1 new level: 22 audit-only findings, 10 `wrong`; three re-reads (8 levels): 30 more, 3 `wrong`.

## Verdict

Session 9, levels audited: 1 new (82 in all), plus round 2 re-reads of 8 levels.
Serious audit-only findings: 3, all on the new level. All fixed.
- `limits-thm/l19-generating-functions.json` screens[6].explain: independence stated as necessary for the MGF product rule (wrong).
- `limits-thm/review-4.json` items[4].explain (`r-best10`): P(result given no skill) read as the chance the result is luck (wrong).
- `limits-thm/problems-4.json` items[2].parts[4].explain (`p-dealer-quotes`): wrong event named, right only by symmetry at 0.5 (wrong).
Minor: 49 audit-only (19 on the new level, 30 on the re-reads), plus 3 from fix-pass reads (one, markov l12 screens[9], tagged serious by its reader; it was the fixer's sentence, fixed before close). Fix-pass reads found 0 `wrong`.
Serious per three levels: 9 on the 1 new level; 0 on the 8 re-read levels; 1.0 on all 9 levels read.
