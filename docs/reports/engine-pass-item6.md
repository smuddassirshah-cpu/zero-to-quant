# Engine pass, item 6 (PLAN 2c item 6, F05.6 and F05.7) and perf gating

ENGINE-BACKLOG 546 to 549.

- 546: the draw is unseen-first across the whole pool (it was balanced by family first, so a seen problem could still win). Seen means verified in the drill library or drawn in an earlier sitting. The paper, start card and results label seen problems with the reason; the attempt stores `seen`. Library stays open.
- 547: `versionOf` on fixed mock versions; Prepare groups "Version 1, 2, 3" and offers the next unsat one. Validator rules and 5 scratch cases.
- 548: `examLocked` ignored advisory references; mock-oa-code locked a non-developer with "0 things to finish". Fixed.
- 549: only rule-matched levels gate on a performance task (manifest `gates`). proof/L3 is now practice only.

Tests: test-met-rule 17 of 17, test-validate-perf 33 of 33, test-validate-versions 5 of 5, readiness-sums exit 0. Playthrough on a scratch copy with the content script applied: `--exam mock-oa-code` and `--routes-only`, desktop and mobile (results in the hand-back).

Main session commands, from the repo root:
1. `node app/tools/apply-item6-content.mjs` (mock-oa-code pass 1 and description; versionOf on four files; idempotent)
2. `cd app && node tools/validate.mjs | tail -1` (0 errors; regenerates manifest.json with `gates`)
3. `node tools/readiness-sums.mjs; node tools/test-met-rule.mjs; node tools/test-validate-versions.mjs`
