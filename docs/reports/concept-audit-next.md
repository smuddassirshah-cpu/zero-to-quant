# Concept audit: next (26 Nov 2026, audit session 13)

State: `concept-audit-log.md`, `concept-audit-notes.md`. Work is on the harness branch, merged to `claude/amazing-wright-d4mx7i`.

Closed: contests L1 to L3 and L4 (round 3), number-sense L4, markov L4 and L5 (round 2), delta batch 2026-11-26-3 (11 courses).

Open: ds L4 (5 `wrong` in round 1; round 2 owed).

Not started: problem sets added since close in nine closed courses (about 12,000 lines); number-sense L1 to L3 and markov fluency sets.

Next: ds L4 round 2; graphs-dp L4, cpp L4 and L5, markets; then the problem sets. Agent worktrees start on the initial commits: begin each prompt with `git checkout -B <own branch> <commit>`. Code courses: sweep every `test-N` line by submission and add `mutants`.

Miss rate, session 13: 4 new levels, 44 audit-only findings, 9 `wrong`; 9 level re-reads, 23 findings, 4 `wrong`.

## Verdict

Levels audited: 4 new (109 in all), 9 re-reads, one delta batch.
Serious audit-only findings: 4, all fixed.
- `number-sense/l15` screens[4]: two unkeyed options were also true.
- `markov/l22` screens[6]: Wald justified by the wrong reason.
- `markov/l19` screens[7] (re-read): Wald without its hypotheses.
- `ds/l18` screens[9]: no time priority passed every hidden test.
Minor: 41 new levels, 3 delta, 22 re-reads, 8 fix-pass rows (1 `wrong`).
Serious per three levels: 2.25 new, 0.33 re-reads.
