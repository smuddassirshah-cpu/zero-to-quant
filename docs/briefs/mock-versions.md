# Brief: fresh mock versions (PLAN 2d; critical review 3.1)

Fault: `mock-oa-sig-2` and `-3` are the same 17 templates as version 1, in the same order, with changed parameters (`docs/briefs/mocks.md` asked for shared positions and families). A learner who has sat version 1 meets recall, not an unseen paper. The trader versions (`mock-oa-trader-2`, `-3`) are suspected of the same.

A template is a setup plus the method that solves it. Two items share a template when the worked solution of one, with numbers swapped, solves the other.

## Task

1. Build a template table: for every item of versions 1, 2 and 3, one line (position, topic, setup in six words, method in six words). Put it in the report.
2. Re-author every item of versions 2 and 3 that shares a template with any item of version 1, or with the other version. Version 1 is not edited.
3. Keep what makes it a mock of that test: the file's `id`, `versionOf`, `style`, `models`, `minutes`, `pass`, the number of items, the rise in difficulty, and the same topic weights (so each version still covers the topics version 1 covers, by different problems). New items get new item ids; no surviving item id changes.
4. Answer type: keep the widget kind the real test uses per `docs/briefs/mocks.md`. Where that brief does not say the real test is multiple choice, prefer `numeric` over `choice` for a new item.
5. Fresh against the whole app as AUTHORING "Exam freshness" (lines about 577 to 582): no setup from a lesson, quiz, review, homework, bank item or other exam. Run `node tools/fresh-check.mjs` as that section says and judge each hit.
6. Scope stays inside the mock's closure: an item may need only ideas its prerequisite courses teach (`node tools/closure.mjs --target <mock id>`).

## Checks (all required before hand-back)

- A committed script `docs/reports/exam-<base>-versions-numbers.py`, run with `<scratchpad>/venv/bin/python`, that recomputes every key of both versions twice: exactly (fractions or sympy) and by a second method (enumeration or a seeded simulation with a stated tolerance). It also checks each `wrong` or distractor value differs from the key. Exit 0.
- From `app/`: validator 0 errors; `node tools/playthrough.mjs --exam <id> --local-cdn <pkgs>` for both versions, and with `--mobile`: green.
- Voice rules of AUTHORING section 6 (35-word gate, no exclamation marks, no em-dashes, British English, £).
- Report `docs/reports/exam-<base>-versions.md`: the template table before and after, items replaced, fresh-check hits and your judgement. One line appended to the mock's section in `docs/briefs/mocks.md` saying versions no longer share templates (session Y). One bullet in `docs/BACKLOG-INBOX.md` under `Raised later (mock versions <base>):` if you see a way for `fresh-check.mjs` to flag same-template items across versions.

Do not edit engine files, `prep.json`, `readiness.json` or version 1. Commit in your worktree with the mock id in the message; never push.
