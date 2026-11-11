# Engine pass AA 1 (PLAN 2d item 3)

Step 1: the inbox from "Raised later (fluency trig, widening pass)" to the end was numbered 861 to 916 in `docs/ENGINE-BACKLOG.md` (56 items; bullets already covered by 844, 852, 853 and 855 to 860 are not repeated; duplicates merged: raw-LaTeX Accepted line 915, feedback bar at 440 px 914, fresh-check form sentences 892). Committed alone as eb5154a. `docs/BACKLOG-INBOX.md` was not edited.

Step 2: A (861 to 865) and B (866) are built, with 867 (prelude order documented). One shared judge now compares drill results; the drill page runs `setup` and `raises`; briefs render lists; long code spans wrap and `--mobile` fails on a clipped brief; `allocCheck` reaches the C++ widget. `constraints` may hold objects (type, len, range, of, sorted, distinct, nonEmpty, pattern) that the validator checks every example and test against (error), with `[no-constraints]` (warning) on a drill with none: all 210 existing drills carry it, 0 errors. A bug found on the way: the harness case table held `null` tolerances, which is not Python, so it is loaded with `json.loads`.

Not done: the "Accepted:" per-test rule (868) and items 869 to 916, open in the backlog.

| Item | Change | Test |
| --- | --- | --- |
| 861 | `__zq_judge` in `code.js`, `ZQ.widgets.codeJudge`, `drill.js` uses it | `test-drill-page.mjs` (15 judge cases, real Python) |
| 862 | `setup`, `raises` in the drill harness | `test-drill-page.mjs` fixture, desktop and `--mobile` |
| 863 | lists in `block()` (`drill-lib.js`), `.drl-list` | `test-drill-page.mjs` (4 render cases) |
| 864 | long spans wrap; `briefClipped` in `playthrough.mjs` | `test-drill-page.mjs` (wide fixture fails `--mobile`, passes desktop) |
| 865 | `allocCheck` pass-through | `test-drill-page.mjs` (source check) |
| 866 | `drill-constraints.mjs`, validator rules, AUTHORING section 5 | `test-drill-constraints.mjs` (36 checks) |
| 867 | AUTHORING section 5 | none (text) |

Results: validate 0 errors; test-drill-page, test-drill-constraints, test-validate-drill-index, test-planted-check (no C++), test-engine-runtime all pass; `playthrough --drills` green (all drills and the sample session); a 20-drill sample passes `--mobile` (the brief check first flagged hidden KaTeX MathML, now skipped). No drill newly fails.
