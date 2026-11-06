# Concept audit: decisions and issues (audit session, 6 Nov 2026)

Decisions
- Eligibility (6 Nov): the base branch history is squashed at ff41b0f (6 Nov 07:31), so every course is "touched in the last day" by that root commit. The session reads the rule as commits after the root: excluded are the session U unread list plus algebra, alpha, analysis, arma, eigen, garch, linear-maps, mm-games, odes, topology.
- Wave 1 (interview courses, 3.3): brainteasers L1 to L3, game-theory L1 to L3, puzzles L1 to L3, mental-pressure L1 to L3. Wave 2 planned: coding-int L1 to L3, research-int L1 to L3, systems L1 to L3, then the leftover levels (puzzles L4 to L5, mental-pressure L4, coding-int L4, research-int L4, systems L4) and Stage 3 (pairs-rep, ito, measure-prob, pdes).
- Auditors run as `general-purpose` agents on model `fable` in their own worktrees, from docs/briefs/concept-audit.md plus a per-course domain note; fixers on `opus`.
- The audit's scripts need scipy, statsmodels and sympy; the container had only numpy, so the session ran `python3 -m pip install scipy pandas statsmodels scikit-learn sympy`. A setup note for later sessions.

Issues
- Miss rate after the first three courses (mental-pressure, puzzles, game-theory, L1 to L3 each, 9 levels): audit-only conceptual findings 6, 3 and 5, so 4.7 per three levels, of which `wrong` 0, 1 and 0 (1 per 9 levels); the rest `imprecise`. The earlier reads had found 7, 3 and 10 conceptual findings, all fixed before the audit, so "review only" measures what the first read caught and the audit could not re-find, not a miss by the audit. "Both" is 0, 1 and 1. Reading: a single second read left about five imprecise claims and one wrong claim per nine levels in these courses, below the session V rate of 6 to 11 wrong per three levels for first reads of unreviewed courses.
