# Engine pass AC part 5: the green-hash cache in CI

HEAD was not a descendant of `claude/amazing-wright-d4mx7i`; reset to it (38383c1) as instructed.

## Built

- `.github/workflows/acceptance.yml`: `play` and `extras` restore (`actions/cache/restore`), select with `--changed --list` (no browser), install Playwright only when K is above 0, run with `--changed --cache tools/.green-cache.json` (push or dispatch `changed`) or without `--changed` (`full`), then save with `actions/cache/save`. `plan` outputs `mode`. `workflow_dispatch` has `mode` (default `full`), plus a weekly `schedule` (Sunday 03:17 UTC, `full`). Each job uploads one `<job>: changed K of N` line; `acceptance` downloads them and prints mode, the lines and a total into `$GITHUB_STEP_SUMMARY`. Static, tests and validator jobs unchanged except `test-ci-cache-keys.mjs` added to `static`.
- `.github/actions/zq-playwright` (new): the Playwright install and browser cache, split out of `zq-setup` so the two jobs can call it conditionally; `zq-setup` calls it when `playwright: true` (the other jobs behave as before) and exports `ZQ_PLAYWRIGHT_VERSION=1.63.0`.
- `app/tools/ci-green.sh` (new): `select` (runs the `--changed --list`, parses `changed: K of N`, writes outputs and the job's line) and `dirty` (did the file grow since the restore).
- `app/tools/green-cache.mjs`: `playwrightVersion()` (installed package.json up the tree, NODE_PATH, global root, else the pin in `ZQ_PLAYWRIGHT_VERSION`, else `none`) is now in the engine hash.
- `app/tools/test-playthrough-changed.mjs`: 9 new checks (desktop cache not green for `--mobile` or `--tablet`; Playwright 1.63.0 to 1.64.0 stales everything; version resolution order). `app/tools/test-ci-cache-keys.mjs` (new, 20 checks): model of Actions cache with two jobs, a failed one and a cancelled one.
- `docs/CI.md`: the scheme, reasoning and schedule caveat.

## Key design (reasoning is in `docs/CI.md`)

Per-job file, `restore-keys: green-<job>-` (newest wins, trailing dash so shard 1 does not match 10), saved as `green-<job>-<run_id>-<run_attempt>`. Save steps use `!cancelled()`: a killed run has written batches but not done its final failure sweep, so a cancelled job saves nothing (greens lost, never wrongly kept); a failed job saves (file holds passes only). Full mode restores nothing, so it reseeds without stale cruft. No merge job, so no single point of failure and no wait for the slowest leg.

## Findings

- Mode is in each cache key and in the job id: desktop greens are never read at mobile (tested). Another branch cannot see this branch's caches, so it replays everything. Older engine hash means everything changed.
- The engine hash already covered `js/css/index.html/vendor`, `playthrough.mjs`, `green-cache.mjs` and the pinned CDN strings (MathLive, Compute Engine, Pyodide, YoWASP). It did not cover the Playwright version or so the Chromium build: added. Still not covered: the `ubuntu-24.04` image, Node 22 minor, content behind an unchanged CDN version string. The weekly full run is the net.
- The default branch is `main` and holds no `.github/` or `app/` (`git ls-tree origin/main`): the schedule will not fire until the workflow is merged there. Said so in `docs/CI.md`. A dispatch with `mode` full does the same job by hand.
- Residual risk: a `playthrough` that crashes outright (not killed) before its final sweep still counts as "not cancelled" and saves; the sweep drops late-error items only at normal exit. Playthrough catches at the top level, so this is believed rare; not tested.
- Unverified (cannot run Actions): `actions/download-artifact` with a pattern matching nothing (set `continue-on-error`), nested local composite action call (`zq-setup` uses `zq-playwright`), the first real `K of N` round trip, and the `0 of N` under a minute claim (the local `--changed --list` takes about 1 to 2 s; checkout, Node setup and cache restore add the rest).

## Verification

- All three YAML files parse. `node tools/ci-coverage.mjs`: 50 test files, 0 problems (static 17).
- Every select command of the workflow ran locally in its cheap form against an empty cache (play desktop and mobile shard 5/16: 129 of 129; extras problems, fluency, drills with `--session`, routes, both viewports); `ci-green.sh dirty` gave true and false as designed.
- `test-playthrough-changed.mjs --local-cdn <pkgs>`: all passed. `test-ci-cache-keys.mjs`: all passed.
