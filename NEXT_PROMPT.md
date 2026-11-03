Read CLAUDE.md and the four state files; follow the SESSION PROTOCOL. Full standards apply (DECISIONS "Standards restored").

Task: PLAN.md 2a order item 4 (topic 3.3), part three. Done already: engine passes B (bank, timing) and D (`trade`, `carry`); mental-pressure L1 to L4 and mock-oa-arith (that course's close); puzzles L1 to L5; brainteasers L1 to L3; mm-games L1, L2; game-theory L1.

Steps (own scratchpad subfolder each; build `bash app/tools/fetch-local-cdn.sh <scratchpad>/pkgs` first; checkpoint-commit as items turn green):
1. In parallel, `content-author`s, each from its brief section:
   - mm-games L3 (`docs/briefs/mm-games.md` `## Level 3`, rewritten for the `trade` widget; read `docs/reports/engine-pass-d.md` and AUTHORING section 3), then mm-games L4 once L3 is green.
   - game-theory L2, then L3 once L2 is green (`docs/briefs/game-theory.md`).
   - mock-oa-sig and mock-oa-trader, three fixed versions each (`docs/briefs/mocks.md`; files `-2`, `-3`; `prep.json` names version 1 only).
2. An answer-check agent recomputes every keyed answer in this session's new files (`docs/reviews/answers-2026-11-05.md`, pattern `answers-2026-11-03-b.md`); every `trade` game is replayed in Python from its seed; a fixer fixes mismatches.

Context: `tags` and `pace` on drill, quiz, review and homework items; firms only in recruiting l4, mocks and `prep.json`; `longform` in homework and exams only; `shuffle: true` on choices; 4-column tables scroll at 390 px; lessons hold at most 12 screens. Run `voice-scan.py` with an absolute `VOICE_BASE` ending in a slash; new files 0 and 0. Re-run a validator error once if it is in another agent's file.

Acceptance, from `app/`: validate 0 errors; new lessons green with and without `--mobile`, sets with `--set`, each mock with `--exam`; `--routes-only` green; reports exist; PLAN ticks each item.

NEXT_PROMPT then names bank part 1 (200 items on E7, four sessions), exam topic-3.3, mock-superday-trader, and the second reads and fix passes for puzzles, mental-pressure, mm-games, brainteasers and game-theory (including the voice debt in KNOWN_ISSUES).
