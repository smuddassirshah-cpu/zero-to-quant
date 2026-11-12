# CI: the acceptance suite

`.github/workflows/acceptance.yml` runs the session's acceptance suite on GitHub Actions, on the real jsDelivr (Pyodide, YoWASP and MathLive are not served locally).

**What runs**
- `static`: `validate.mjs` (0 errors), `readiness-sums.mjs`, `ci-coverage.mjs` (fails if a `tools/test-*` file is in no job or in two), `grade-all.mjs` (keys, bands and slip routing of all content, no browser), and the 16 tests that need no browser.
- `tests-browser`: three legs, `grading` (answer forms, engine runtime desktop and `--mobile`, problems, fluency; they get a lean local copy of the Compute Engine and MathLive), `ui` (check-first and today-tested-out desktop and `--mobile`, the overflow and tall-shot tests) and `python` (bank code, drill page, drill recursion, planted check: Python 3.12 packages, Pyodide and YoWASP from the CDN).
- `validate-tests`: the 19 `test-validate-*` files, each called by name with no flags (band-rules is given the Compute Engine through `ZQ_LOCAL_CDN`).
- `play`: `playthrough.mjs --all --shard i/N --no-routes`, N shards (default 16) times desktop and `--mobile`. `extras`: `--problems all` (2 shards), `--fluency-all` (4), the drills (3, by naming them with `--drill`, the session play in part 1) and `--routes-only`, each desktop and `--mobile`.
- `acceptance`: needs all of the above and fails unless each succeeded. Read this one status; its job summary lists every job.

**How to trigger**: push to `claude/amazing-wright-d4mx7i` touching `app/**` or `.github/**`, or Actions, acceptance, Run workflow with `shards` (1 to 64) and `suite` (`full`, `static`, `tests`, `play`, `extras`). A newer run on the same ref cancels the older.

**How to read a failure**: open `acceptance`, find the red job, open its log. Each step ends with the last 40 lines; `ci-run.sh` prints a group per command and a table of `ok` and `FAIL` lines with seconds; play and extras then print their `FAIL` lines again. Re-run the failed leg once before treating it as yours. To reproduce locally, run the command shown in the group from `app/` (add `--local-cdn <pkgs>` if the network is closed).

**Expected minutes** (estimates from timings in a slow sandbox, not measured on Actions): one play leg 20 to 25 (128 items at about 10 s), extras legs 8 to 12, `static` 12, `validate-tests` 10 to 15, `tests-browser` legs 10 to 25, first-run Playwright download 1 more. Wall clock about 25 to 30 minutes; about 1000 runner minutes a full run (the repo is private, so metered). `--drills` has no `--shard`, hence the `--drill` split; the unsplit run would be about 25 minutes desktop. `--all` already includes the problem and Fluency sets, so `extras` plays those a second time in their own profile by design.

**Slot for `--changed --cache`**: the commented block in the `play` job shows where `actions/cache` for `app/tools/.green-cache.json` and the flags go. Not wired.

**Reproducing CI locally (engine pass AC part 4)**: `tools/fetch-local-cdn.sh <pkgs>` also fetches the Google Fonts stylesheet and woff2 files into `<pkgs>/fonts/` when the network allows; `playthrough.mjs --local-cdn <pkgs>` then serves them instead of empty CSS, so text widths match CI. `ZQ_CDN_DELAY_MS=1500` makes every local-CDN file wait that long, to mimic a slow jsDelivr (it reproduces the Fluency "Loading the maths editor" race). Tests that play a temporary copy of `app/` run `playthrough.mjs` from `tools/` in place with `ZQ_APP_DIR` set, because a copy in the OS temp dir cannot resolve the workspace `node_modules`; the setup action also exports `NODE_PATH` for the loaders' fallback.
