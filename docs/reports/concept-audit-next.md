# Concept audit: next (13 Nov 2026, audit session 11)

State: `docs/reports/concept-audit-log.md` (rounds), `concept-audit-notes.md` (decisions, issues). Branch `claude/fable-audit`; the content session merges it.

Closed: all of session 10's list, and new this session micro L1 to L3 and py-found L1 to L3 (round 2 each), algo-think L1 to L3 (three rounds), ds L1 to L3 (two), graphs-dp L1 to L3 (three), cpp L1 to L3 (three). Every course started this session is closed.

Open: limits-thm L4 (round 2 owed; blocked by the 40-line rule until about 20:31 UTC on 13 Nov).

Next: limits-thm L4 round 2; markov L4 and L5 (check for a second read first); delta batch 3 (pairs-rep, pdes, ito, numerics, random-vars, mental-pressure, research-int, number-sense, limits-thm and markov L1 to L3, as each settles); then ds L4, graphs-dp L4, cpp L4 and L5, markets, contests. For code courses, tell the auditor to run each `test-N` line's named mistake as a submission, and give the page facts: recursion limit 3,000, wasm32, `error` shows only when the runner fails. Merge the content branch; do not rebase.

For the content session: 73 of 344 `test-N` feedback lines swept in three courses named a cause that cannot show them. See the notes; it needs a validator rule.

Miss rate: sessions 1 to 10 as logged (89 levels). Session 11, 12 new levels: 75 audit-only findings, 22 `wrong`; nine re-reads added 79, 13 `wrong`.

## Verdict

Session 11, levels audited: 12 new (101 in all), plus re-reads of 18 levels.
Serious audit-only findings: 6, all on new levels, all fixed.
- `algo-think/l3-memory.json` screens[0] program A: the O(1)-memory example copied the list (wrong).
- `algo-think/l13-quicksort.json` screens[7] key text, screens[4]: random pivot "on every input" (imprecise).
- `ds/l8-best-day.json` screens[9].explain: look-ahead "can beat" the perfect-foresight bound (wrong).
- `ds/l8-best-day.json` screens[5], `homework-2.json` items[7]: drawdown in pounds, unsaid (imprecise).
- `graphs-dp/l5-tasks-in-order.json` screens[4], summary.trap, `homework-1.json` items[7]: pre-order trap blamed on the start node (misleading).
- `cpp/homework-1.json` items[6].model, rubric[5]: warnings no compiler prints (wrong).
Minor: 69 on new levels, 79 on re-reads, 12 from fix-pass reads (0 `wrong`).
Serious per three levels: 1.5 on the 12 new levels; 0 on re-reads.
