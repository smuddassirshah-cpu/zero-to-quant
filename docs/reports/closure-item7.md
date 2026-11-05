# PLAN 2c item 7: dependency rationale and closures (5 Nov, session Q)

Engine: ENGINE-BACKLOG 551 to 555 (`docs/reports/engine-pass-item7.md`). Content: `app/tools/apply-item7-content.mjs` (idempotent), reading the Sonnet draft `docs/reports/closure-item7-proposal.json` with the main session's review as overrides in the script. Closures from `app/tools/closure.mjs`.

## Result
- 248 cross-course edges reviewed. After review: 204 kept as gates, 21 diagnostics (`gate: false`, "Check first"), 11 retargeted to the level actually used, 6 moved to the dependent course's later level that uses them, 6 cut, 3 new edges (2 diagnostics, 1 gate). 245 cross-course edges now, 0 without `why`; the validator errors on a missing `why` (`--lax-why` relaxes it).
- Route limitation: pdes reaches unwritten `odes` L1, L2 and `complex` L1 (pdes/L3 also `numerics` L4); Learn and Prepare show "Route limited". `complex` was not in the user's "write before 2b" answer: decide whether it joins `odes` and `numerics`.

## Closures (levels; courses; mapped lessons)
| Target | Before | After |
|---|---|---|
| mock-superday-trader | 107; 35; 470 | 106; 35; 465 |
| role trader (union of its mocks) | 109; 35; 479 | 108; 35; 474 |
| mock-superday-research | 89; 32; 375 | 83; 31; 350 |
| role researcher | 109; 39; 463 | 99; 37; 421 |
| mock-oa-code (developer, strats, derivatives) | 38; 16; 163 | 32; 14; 138 |
| coding-int/L1 | 27; 10; 115 | 23; 9; 99 |
| systems/L1 | 55; 20; 231 | 4; 2; 17 |
| research-int/L1, puzzles/L1, brainteasers/L1 | 61, 27, 7 levels | unchanged |
| pdes/L1 | 91; 32; 385 | 33; 13; 141 |

Trader: the closure barely moves. The six courses the review named (ds, graphs-dp, algo-think, contests, integrals, multivar) each have a concrete `why` now. The residual cost is two edges: `game-theory/L2 -> graphs-dp/L4` (backward-induction recursion) and `brainteasers/L2 -> graphs-dp/L3` (two-egg DP). Making both diagnostics takes the trader superday closure to 96 levels, 32 courses, 422 lessons (measured on a scratch copy). That is a user lever, not taken: both reasons are real and the Strict default stands.

## Review of the draft (main session)
The draft (keep 182, diagnostic 50, retarget 9, cut 7) was not applied as written:
1. 13 first levels would have lost every gate (coding-int, py-found, numpy-pandas, cpp-pricing, systems among them), so a fresh learner could open them cold. Rule applied: every L1 that had a gate keeps one, retargeted to the minimal level used (systems/L1 now needs cpp/L2, not cpp-pricing/L3; cpp-pricing/L1 needs cpp/L1).
2. Diagnostics were measured by closure impact. The research-int edges into regression L3, testing L3, ensembles L3, validation L3 and fin-ml L2 took the research superday from 375 to 130 lessons; an interview course asks across the whole topic, so they are gates again. Also restored: coding-int/L1 to graphs-dp/L4 (the OA pool has decodings and critical-path problems), limits-thm/L4 to integrals/L4, game-theory/L2 to limits/L4; algo-think/L1 and pytest/L1 keep a Python gate at py-found/L1.
3. The stat-learning/L1 cut removed the research route's only Python gate (all four L1 lessons use NumPy); retargeted to numpy-pandas/L1.
4. Rejected retargets: brainteasers/L1 to counting-chance/L3 (widens a trader gate for one named idea); three measure-prob lesson refs turned into whole levels (a lesson ref is the narrower gate).
5. contests: graph algorithms appear only in the L4 virtual contest, so `graphs-dp/L2` moved from L1 to L4, and L1 gets `py-found/L2` (every L1 lesson writes Python functions). Without this a trader learnt Dijkstra before last-digit puzzles.

## Changes by edge (besides keeps)
Retarget: algo-think/L1 py-found/L2 to L1; analysis/L2 limits/L2 to L1; arma/L1 regression/L3 to L1; cpp/L1 terminal/L3 to L2; cpp-pricing/L1 cpp/L2 to L1 (cpp/L2 diagnostic added); markets/L1 series/L3 to L2; markov/L4 limits-thm/L4 to L2; pdes/L1 odes/L4 to L2; pytest/L1 py-found/L2 to L1; stat-learning/L1 numpy-pandas/L3 to L1; systems/L1 cpp-pricing/L3 to cpp/L2 (cpp-pricing/L3 diagnostic added).
Move: alpha/L1 to alpha/L3 (fin-ml/L3); backtest/L1 to backtest/L2 (fin-ml/L3); contests/L1 to contests/L4 (graphs-dp/L2); integrals/L1 to integrals/L2 (limits/L2); pdes/L1 to pdes/L3 (ito/L3); regression/L1 to regression/L3 (least-squares/L3).
Cut: linear-maps/L2 least-squares/L1 (covered by L3's least-squares/L2); measure-prob/L1 ito/L1; proof/L3 quadratics/L2 and counting/L3; research-int/L4 fin-ml/L3; trees/L1 options/L3.
Diagnostics (23: 21 from the draft, 2 added) are listed by `node app/tools/closure.mjs --target <t> --edges` and in course.json as `"gate": false`.

## Checks
Validator 0 errors (245 edges, 0 without why); `readiness-sums.mjs` 0 after `--write` (conflict tables lose contests, graphs-dp and cpp-pricing rows); `apply-item7-content.mjs` second run changes 0 files; `--routes-only --local-cdn` desktop and mobile: see PLAN line.
Open: the 23 diagnostics' `why` lines come from the draft unedited apart from the overrides; a second reader should sample them. No DOM test of the "Check first" card (engine report).
