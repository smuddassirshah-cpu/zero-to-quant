# Concept audit: next (12 Nov 2026, audit session 10)

State: `docs/reports/concept-audit-log.md` (rounds), `concept-audit-notes.md` (decisions, issues). Branch `claude/fable-audit`; the content session merges it.

Closed: mental-pressure, puzzles, game-theory, brainteasers, coding-int, research-int, systems, pdes, pairs-rep, mental, number-sense, ito, measure-prob, numerics, mm-games, recruiting L1 to L3, counting-chance L1 to L3, odes, conditional, random-vars, limits-thm L1 to L3, markov L1 to L3, delta batch 1, and new this session py-found L4 and delta batch 2 (eight courses).

Open: limits-thm L4 (round 2 owed), micro L1 to L3 (round 2 owed: 3 `wrong`), py-found L1 to L3 (round 2 owed: 5 `wrong`, all minor). Fix passes and fix-pass reads are merged, gates green.

Next: the three round 2 reads; markov L4 and L5 (check for a second read first); delta batch 3 (pairs-rep, pdes, ito, numerics, random-vars, mental-pressure, research-int, number-sense, limits-thm and markov L1 to L3, as each settles); then contests, algo-think, ds, graphs-dp, cpp. limits-thm and markov were blocked today by the content session's slip sweeps (44 and 104 lines against the 40-line rule); see the notes for a proposed exemption. Tell agents to fast-forward their worktree to `claude/fable-audit` first.

Miss rate: sessions 1 to 9 as logged (82 levels). Session 10, 7 new levels: 58 audit-only findings, 9 `wrong`; the delta added 5, 0 `wrong`.

## Verdict

Session 10, levels audited: 7 new (89 in all), plus a delta read of eight closed courses.
Serious audit-only findings: 4. All fixed.
- `micro/l6-impact.json` quiz[0].widget.answer: graded key 20.03 where the item's data give 20.0233 (wrong; a right answer was marked wrong).
- `micro/l7-where-is-the-price.json` summary.ideas[1], screens[3], screens[8], quiz[3]: "the microprice predicts the next mid better", false in the lesson's own book (imprecise).
- `py-found/l8-who-changes-the-list.json` screens[8].explain: "copy first" with no word that the copy is one level deep (imprecise).
- `py-found/homework-4.json` items[6] (`h4-debug`) model and rubric: a newest-first file "gives 0% drawdown" (imprecise).
Minor: 54 audit-only on the new levels, 5 on the delta, plus 6 from fix-pass reads. Fix-pass reads found 0 `wrong`.
Serious per three levels: 1.7 on the 7 new levels; 0 on the delta.
