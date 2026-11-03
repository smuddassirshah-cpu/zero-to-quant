# Engine: bank close

- Removed `app/content/bank/sample.json`. No engine, validator or manifest code referenced it (manifest rebuilt by validate; remaining "sample" hits are `mock-sample`, `mock-trade-sample`, an estimation lesson). Nothing needed repointing.
- `app/tools/playthrough.mjs` routes `#bank` check: counts come from the files (drawable = items without `requires`, locked = the rest, unique uids, `bankStatus` total, locked and fresh must match). Pace assertion unchanged and green. Old-save probe uid renamed from `bank/sample/x` to `bank/x/x`. Result: 115 drawable of 200 in 20 files, 85 locked.
- New `--bank <file>` (repeatable, `all`), ENGINE-BACKLOG 462. Imports a save with the file's `requires` lessons done, clears the bank schedule, schedules other drawable items 30 days out, deals decks via the bank page, answers each item right from its key, prints pass or fail per item. `--bank all`: 200 of 200 items passed in 20 files.
- Docs: AUTHORING bank section (real files as pattern, how routes counts, `--bank`); KNOWN_ISSUES sample bullets removed/trimmed; ENGINE-BACKLOG 462 to 466 (463 answerWrong, 464 `--dups`, 465 shuffle seed left open; 466 sample removal). Inbox untouched.
- Tests: validate 0 errors (392 warnings); `--routes-only` and `--routes-only --mobile` all passed.
