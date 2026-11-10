# Concept audit log (rule: `docs/briefs/concept-audit.md`)

| Course | Levels | Round | Wrong | Imprecise | Misleading | Audit only | Review only | Both | Closed |
|---|---|---|---|---|---|---|---|---|---|
| mental-pressure | L1 to L3 | 1 | 0 | 6 | 0 | 6 | 7 (all fixed before the audit) | 0 | yes (fix pass 6 fixed, 0 disputed; gates green) |
| puzzles | L1 to L3 | 1 | 1 | 3 | 0 | 3 | 3 (all fixed before the audit) | 1 | yes (1 wrong is within the rule; fix pass 4 fixed, 0 disputed; gates green) |
| game-theory | L1 to L3 | 1 | 0 | 6 | 0 | 5 | 10 (all fixed before the audit) | 1 | yes (fix pass 6 fixed, 0 disputed; one key changed, l11 pot odds, recomputed by the orchestrator; gates green) |
| brainteasers | L1 to L3 | 1 | 0 | 4 | 0 | 4 | 13 (all fixed before the audit) | 0 | yes (fix pass 4 fixed, 0 disputed; gates green) |
| coding-int | L1 to L3 | 1 | 1 | 5 | 0 | 5 | 5 (all fixed before the audit) | 1 | yes (1 wrong is within the rule; fix pass 6 fixed, 0 disputed; gates green; perf numbers timer repaired by the orchestrator) |
| systems | L1 to L3 | 1 | 1 | 21 | 0 | 22 | 7 (all fixed before the audit) | 0 | yes (1 wrong is within the rule; fix pass 22 fixed, 0 disputed; gates green) |
| research-int | L1 to L3 | 1 | 0 | 8 | 2 | 10 | 4 (all fixed before the audit) | 0 | yes (fix pass 10 fixed, 0 disputed; gates green; review-1 timed playthrough is an open engine issue) |
| mental-pressure | L4 | 1 | 0 | 10 | 0 | 10 | 2 (all fixed before the audit) | 0 | yes (fix pass 10 fixed, 0 disputed; gates green; course fully closed) |
| puzzles | L4 to L5 | 1 | 2 | 2 | 1 | 5 | 4 (all fixed before the audit) | 0 | no: 2 wrong in 2 levels exceeds the rule; fix pass 5 fixed, 0 disputed, gates green; round 2 started |
| research-int | L4 | 1 | 0 | 5 | 4 | 9 | 6 (all fixed before the audit) | 0 | yes (fix pass 8 fixed, 0 disputed, 1 deferred: l20 four pound-typed rows, see notes; gates green; course fully closed) |
| systems | L4 | 1 | 2 | 7 | 2 | 10 | 0 | 1 | no: 2 wrong in 1 level exceeds the rule; fix pass 11 fixed, 0 disputed, gates green (l17 timing key 80 to 66.7, one-read bracket model now stated, recomputed by the orchestrator); round 2 started |
| coding-int | L4 | 1 | 0 | 4 | 1 | 5 | 11 (all fixed before the audit) | 0 | yes (fix pass 5 fixed, 0 disputed; gates green; course fully closed) |
| pairs-rep | L1 to L3 | 1 | 4 | 4 | 0 | 7 | 15 (all fixed before the audit) | 1 | no: 4 wrong in 3 levels exceeds the rule; fix pass 3 fixed, 5 disputed; third reader upheld 1, 2, 3, 8 (applied) and left 4 unverified (needs GGR §2.2); gates green; round 2 started |
| puzzles | L4 to L5 | 2 | 0 | 3 | 0 | 3 | 9 (all fixed before round 2) | 0 | yes (round 2: 0 new wrong; fix pass 3 fixed, 0 disputed; gates green; course fully closed) |
| systems | L4 | 2 | 0 | 7 | 1 | 7 | 10 (all fixed before round 2) | 1 | yes (round 2: 0 new wrong; fix pass 8 fixed, 0 disputed; q17-rank now names nearest rank, key unchanged; gates green; course fully closed) |
| ito | L1 to L3 | 1 | 1 | 5 | 1 | 7 | 14 (all fixed before the audit) | 0 | yes (1 wrong is within the rule; fix pass 7 fixed, 0 disputed; gates green; L4 not yet audited) |
| measure-prob | L1 to L3 | 1 | 0 | 4 | 0 | 3 | 18 (all fixed before the audit) | 1 | yes (fix pass 4 fixed, 0 disputed; gates green; L4 not yet audited) |
| pdes | L1 to L3 | 1 | 0 | 7 | 0 | 7 | 21 (all fixed before the audit) | 0 | yes (fix pass 7 fixed, 0 disputed; gates green; course fully closed) |
| pairs-rep | L1 to L3 | 2 | 0 | 2 | 3 | 4 | 22 (all fixed before round 2) | 1 | yes (round 2: 0 new wrong; fix pass 4 fixed, 1 disputed (finding 3, look-ahead effect; open for a third reader); three choice keys moved (l2 quiz[1], l10 screens[0], l10 quiz[0]); gates green) |
| pairs-rep | L1 to L3 | 2 (third read) | 0 | 1 | 0 | 0 | 0 | 0 | yes (9 Nov: round-2 finding 3 `upheld in part` by a fresh Fable reader, the look-ahead line is imprecise: it flatters on the course panel, +0.011 to +0.037 a cycle, and reverses when trading volatility doubles, −0.117; Opus fixer confirmed on its own run and applied l1 screens[5].explain; no graded key changed; gates green; course fully closed) |
| mental | L1 to L3 | 1 | 0 | 8 | 0 | 8 | 7 (all fixed before the audit) | 0 | yes (9 Nov: 230 ledger rows; 1 serious, l8 "strips always cancel" without "the same distance"; fix pass 8 fixed, 0 disputed, no graded key changed; gates green; course fully closed) |
| number-sense | L1 to L3 | 1 | 1 | 11 | 0 | 12 | 10 (all fixed before the audit) | 0 | yes (10 Nov: 240 ledger rows; 1 wrong is within the rule: l12 quiz[2].explain "Calculators and code follow the same rule" for −3², put there by the earlier review's own fix text; fix pass 12 fixed, 0 disputed, 3 text defects fixed, no graded key changed; gates green; course fully closed) |
