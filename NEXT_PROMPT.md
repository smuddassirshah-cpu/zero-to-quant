Read CLAUDE.md and the four state files; follow the SESSION PROTOCOL. Full standards apply (DECISIONS "Standards restored").

Task: PLAN.md 2a order item 4 (topic 3.3), part four, to close the topic. Every topic 3.3 level and the arith, sig and trader mocks are done.

Steps (own scratchpad subfolder each; build `bash app/tools/fetch-local-cdn.sh <scratchpad>/pkgs` first; checkpoint-commit as items turn green):
1. Briefs first, if missing: `docs/briefs/bank.md` (part 1: 200 items on engine E7, `content/bank/`, families from the `tags` already on drill and homework items; split into four sessions of 50) and a `## mock-superday-trader` section in `docs/briefs/mocks.md`. Sources: `interview-plan.md`, `docs/reports/engine-pass-b.md`.
2. In parallel, `content-author`s: bank part 1 session 1 (50 items); exam `topic-3.3` (30 items at most, pattern `exams/topic-2.1.json`); `mock-superday-trader` (may use `trade` games; see AUTHORING section 3).
3. Second readers for puzzles, mental-pressure, mm-games, brainteasers, game-theory (`docs/reviews/review-<course>.md`, pattern `review-1.5.md`), each running `voice-scan.py` with an absolute `VOICE_BASE` ending in a slash; clear the voice debt in KNOWN_ISSUES (mental-pressure L1 to L3, puzzles L1 to L3, mm-games l4-fermi and L1). Fix agents append `## Fix pass`.
4. Answer check on the session's new files (`docs/reviews/answers-<date>.md`, pattern `answers-2026-11-05.md`), replaying every `trade` game from its seed; a fixer fixes mismatches.

Context: `tags` and `pace` on drill, quiz, review, homework and bank items; firms only in recruiting l4, mocks and `prep.json`; `longform` in homework and exams only; `shuffle: true` on choices; numeric `wrong` values may sit either side of the key (DECISIONS 5 Nov). Known engine bug: multi-paper mocks show "Pass mark NaN%".

Acceptance, from `app/`: validate 0 errors; the new files green (`--set`, `--exam`, with and without `--mobile`); `--routes-only` green; voice scan 0 and 0 on all five courses; reports and reviews exist; PLAN ticks each item. Bank sessions 2 to 4 follow in later sessions.
