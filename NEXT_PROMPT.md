NEXT_PROMPT: after DONE (session AJ or later)

The build is complete. `DONE` exists; acceptance run 43 at 529f3c3a is green (full suite, full mode). Read CLAUDE.md, then `docs/reports/final-report-ai.md`, KNOWN_ISSUES "session AI close" and DECISIONS "Session AI". Run the census; if it disagrees with the figures below, fix the state files first.

Nothing below reopens DONE. Every change still passes the SESSION PROTOCOL checks (validator 0 errors, voice scan, number scripts, playthrough `--changed`, a green acceptance run before a push counts as finished). Lesson ids are never renamed. Push to the branch the harness assigns and to `claude/amazing-wright-d4mx7i` (CI), only when no run is in progress there.

Default track, unless the user picks another: the concept audit.

1. Concept audit (PLAN 5b). Brief `docs/briefs/concept-audit.md`, log `docs/reports/concept-audit-log.md`, branch `claude/fable-audit`. One course per Fable auditor, then one fix pass on Sonnet. Merge the audit branch into the CI branch at start and close; run `same-course-reuse.mjs --all` and the number scripts. A course closes under the convergence rule (at most one new `wrong` per three levels).
2. Post-completion engine work: the last section of `docs/ENGINE-BACKLOG.md` (every [Could], E15 to E19, 34 [Should]); the two bullets in `docs/BACKLOG-INBOX.md`; gated `controlsAfter` buttons not visibly dimmed; item 1036 (documented, not built); `grade-all --code` over all content; the pkg3 duplicate-line test not shown to fail; `read-numbers.py` (stat-learning 4) to compare with Pyodide values, not widened bands.
3. Small content leftovers: `ensembles/problems-2` `p-ipo-forest` part 1 feeds nothing; the gallery's 27-leaf tree labels at 440 px.

The pilot (PLAN task 12) is human-owned and never ticked by a session; help prepare its materials only when asked.

Expected census: lessons 1,236; levels 283; reviews 283 (items 2,558); exams 29 topic, 4 stage, 16 mock; drills 270; Fluency 100 (families 318); problem sets 167 (items 617); bank 36 files, 400 items; hours 3,695, gap 0; edges 266; validator 0 errors (4,606 warnings); same-course reuse 0 errors, 44 waived; number scripts 436; ENGINE-BACKLOG 0 lines "status: open".
