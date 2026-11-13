# Concept audit: next (13 Nov 2026, audit session 12)

State: `docs/reports/concept-audit-log.md` (rounds), `concept-audit-notes.md` (decisions, issues). Branch `claude/fable-audit`; the content session merges it.

Closed this session: limits-thm L4 (round 2, 0 new `wrong`). All earlier closures stand.

Open: contests L1 to L3 (round 1 fixed and read; round 2 owed), contests L4 (rounds 1 and 2 fixed and read; round 3 owed). Both are open on `test-N` feedback lines only.

Not started: markov L4 and L5 have no second read on record, so scope rule (a) bars them; the content session must rule. Delta batch 3 was blocked by the 40-line rule until 20:31 UTC.

Next: contests L4 round 3 and L1 to L3 round 2 (tell the auditor to sweep every `test-N` line with two or three codings of the named mistake, and to run C++ on the page's clang); delta batch 3 (pairs-rep, pdes, ito, numerics, random-vars, mental-pressure, research-int, number-sense, limits-thm and markov L1 to L3); then ds L4, graphs-dp L4, cpp L4 and L5, markets. Merge the content branch; do not rebase. Agent worktrees start stale: fast-forward first.

Miss rate: sessions 1 to 11 as logged (101 levels). Session 12, 4 new levels: 36 audit-only findings, 20 `wrong`; two re-reads added 24, 2 `wrong`.

## Verdict

Session 12, levels audited: 4 new (105 in all), plus re-reads of 2 levels.
Serious audit-only findings: 2, both on new levels, both fixed.
- `contests/l14-which-first.json` screens[11]: no decay stated, so a wrong option earned the key's £15,000 (imprecise).
- `contests/l8-invariants.json` prose, summary, screens[5], `homework-2.json` model: a monovariant "proves" termination with no bound (imprecise).
Minor: 34 on new levels, 24 on re-reads, 7 from fix-pass reads (0 `wrong`).
Serious per three levels: 1.5 on the 4 new levels; 0 on re-reads.
