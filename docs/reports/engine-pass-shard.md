# Engine pass: playthrough shard and browser relaunch (item 550)

File changed: `app/tools/playthrough.mjs` (plus usage text, `docs/AUTHORING.md` "Long runs", `docs/ENGINE-BACKLOG.md` item 550). Item 550 was taken here because another agent numbers in parallel. The "7d" closure block was not touched.

## Sharding
- `--shard i/n`: 1-based, `1 <= i <= n`, otherwise a usage error (exit 2). The full ordered list is lessons, then sets, then exams (after `--lesson`, `--set`, `--exam`, `--sets`, `--exams` selection). Shard i keeps indexes with `index % n === i-1`. Prints `shard i/n: K of N items`.
- Routes and their checks (bank, drills, samples, gating, provenance, holdout, versions, pace) run in shard 1 only. Choice for `--routes-only`: not sharded, so shard 1 runs it and other shards have no work and pass.
- `--list` prints `lesson/<id>`, `set/<id>`, `exam/<id>` for the run and exits before any browser or server starts.

## Relaunch
- Browser, context and page are now `let` and built by `openBrowser()` (same viewport, downloads, local-cdn routes, listeners); setup is `freshSetup()`.
- Each lesson, set and exam runs under `guarded`. If it throws or records a failure matching "Target page, context or browser has been closed" (or similar), or the `disconnected` event fired, failures and console errors from that attempt are dropped, Chromium is relaunched, setup is redone and the item runs once more. A disconnect seen before an item relaunches first. Ordinary failures are never retried (the older `playSet` reload retry is unchanged).
- Summary prints `browser relaunches: R`.
- Test hook: `ZQ_TEST_CLOSE_AFTER=k` closes the context after the k-th item.
- Not covered: a close during the routes block or `--bank`, `--drill` runs (not item loops).

## Evidence (from `app/`, local CDN)
- `node tools/validate.mjs`: 0 errors.
- Partition script (scratchpad `shardcheck.mjs`): 1584 items; n = 1, 2, 3, 4, 7, 400 each give overlap 0, missing 0, total 1584; 4 shards are 396 each.
- Malformed `5/4`, `x`, `0/3`, `2`: usage error.
- `--all --shard 37/400`: 4 items, green, 0 relaunches.
- `ZQ_TEST_CLOSE_AFTER=2` on the same shard: item 3 failed "threw", relaunch 1, item 3 passed, `browser relaunches: 1`.
- `--routes-only`: see the hand-back line.
