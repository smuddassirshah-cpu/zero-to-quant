Read CLAUDE.md and the four state files; follow the SESSION PROTOCOL. Full standards apply (DECISIONS "Standards restored").

Task: PLAN.md 2a order item 4 (topic 3.3), part five, to close the topic: bank part 1 sessions 2, 3 and 4. Everything else in topic 3.3 is done.

Steps (own scratchpad subfolder each; build `bash app/tools/fetch-local-cdn.sh <scratchpad>/pkgs` first; checkpoint-commit as items turn green):
1. In parallel, three `content-author`s, one per session (50 items each), from `docs/briefs/bank.md` (binding, including "Changes after session 1": families `every-coupon` and `hats`; 3p05 needs new numbers; rubric shape 2, 2, 2, 2, 1, 1). Pattern: session 1 files `app/content/bank/*-1.json` and `docs/reports/bank-1-1.md`. Each writes only its own `bank/*-<n>.json`, `docs/reports/bank-1-<n>.md` and inbox bullets. Each greps courses, exams and bank for duplicate numbers (DECISIONS "Duplicates (6 Nov)").
2. When all three are green, one `engine-dev`: remove `bank/sample.json` (KNOWN_ISSUES Session D), update AUTHORING and the `--routes-only` bank check, full `--routes-only` green.
3. Answer check on the 150 new items (`docs/reviews/answers-<date>.md`, pattern `answers-2026-11-06.md`); a fixer fixes mismatches.
4. Closing commit for topic 3.3: tick PLAN 2a item 4 and the phase 1 bank line.

Context: `tags` (first tag is the family) and `pace` (at most 180 s) on every bank item; `requires` only on difficulty 4 and 5; no firm names in bank items; `shuffle: true` on choices; numeric `wrong` values with a `why`, either side of the key; no playthrough flag plays one bank file, so authors use the scratch deck loop described in the brief.

Files likely touched: `app/content/bank/`, `docs/reports/bank-1-*.md`, `docs/BACKLOG-INBOX.md`, `docs/AUTHORING.md`, `app/tools/playthrough.mjs`, state files.

Acceptance, from `app/`: validate 0 errors; `--routes-only` green with and without `--mobile`; every new item played by the deck loop; `VOICE_BASE=/home/user/zero-to-quant/app/content/bank/ python3 ../docs/reviews/voice-scan.py --summary` 0 and 0; reports exist; PLAN ticks. Next after that: topic 3.5 (PLAN 2a item 5).
