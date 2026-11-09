# Concept audit: next (6 Nov 2026, audit session 1)

State: `docs/reports/concept-audit-log.md` (rounds), `concept-audit-notes.md` (decisions, issues). Branch `claude/fable-audit`; the content session merges it.

Closed (convergence rule met, fix passes merged, gates green): mental-pressure L1 to L4, puzzles L1 to L5 (L4 to L5 took two rounds), game-theory L1 to L3, brainteasers L1 to L3, coding-int L1 to L4, research-int L1 to L4, systems L1 to L4 (L4 took two rounds), ito L1 to L3, measure-prob L1 to L3, pdes L1 to L3, pairs-rep L1 to L3 (two rounds).

Open: ito L4, measure-prob L4 (not yet audited); pairs-rep round-2 finding 3 (disputed, needs a third reader). Deferred to the content session (notes): research-int l20 and l14 pound-typed rows; research-int review-1 timed-set playthrough failure (engine).

Next, in order (reordered 9 Nov by the content session, user decision; `docs/briefs/fable-audit-session-prompt.md` "Order" is binding): the pairs-rep third read, ito L4 and measure-prob L4; then mm-games, recruiting; the topic 1.5 courses; the rest of the trader and developer closures; other route courses; optional Stage 2 and 3 courses last; exams after their courses close. Use the same agent briefs (auditor on `fable`, fixer on `opus`, own scratch subfolder each; by-design checks marked `EXPECTED_FAIL` with the corrected assert in a comment, which the fixer enables).

Miss rate (round 1, 39 levels, 13 course-level reads): 132 audit-only conceptual findings, 12 `wrong`, 113 `imprecise`, 15 `misleading`; about 0.9 `wrong` and 10 findings per three levels left behind by one second read. Round 2 (puzzles L4 to L5, systems L4, pairs-rep): 0 new `wrong`.
