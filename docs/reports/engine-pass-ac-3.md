# Engine pass AC part 3: CI workflow and grade-all

## Files

- `.github/workflows/acceptance.yml`, `.github/actions/zq-setup/action.yml` and `requirements.txt` (shared setup: Node 22, Playwright 1.63.0 with the Chromium headless shell cached in `~/.cache/ms-playwright`, Python 3.12 with pip cache, a lean local CDN).
- `app/tools/ci-run.sh` (runs a command list, `tail -40` and exit code per command, table of seconds), `app/tools/ci-coverage.mjs` (every `tools/test-*` file in exactly one job; in `static`), `app/tools/grade-all.mjs`, `app/tools/test-grade-all.mjs`, `docs/CI.md`, one paragraph in `docs/AUTHORING.md` after "Grader regression".
- Not touched: `playthrough.mjs`, `validate.mjs`, `test-validate-*`, `app/content/`, the backlog and inbox.

## A. Workflow

Verified: both YAML files parse (`yaml.safe_load`); `ci-coverage.mjs` reports 47 test files, 0 problems (static 16, tests-browser 12, validate-tests 19; the count against `/dev/null` is 47 missing); `--list` forms of the playthrough commands (`--all --shard 3/16 --no-routes --mobile`, `--problems all --shard 1/2`, `--fluency-all --shard 4/4`) accepted; the drill split (93, 92, 92 ids) and `--drill a --drill b --session` run green locally (30 s for two drills and the session); `ci-run.sh` keeps going after a failing command and exits 1. Actions itself could not be run.

Jobs: `plan` (1 min), `static`, `tests-browser` x 3 legs (grading, ui, python), `validate-tests`, `play` 16 shards x 2 viewports = 32, `extras` 10 parts x 2 viewports = 20, `acceptance`. Triggers, `concurrency`, `permissions: contents: read`, `timeout-minutes` everywhere and `fail-fast: false` as briefed. One deviation: `paths` also lists `.github/actions/**`, because the shared setup lives there.

`--shard` support (read in `playthrough.mjs` lines 293 to 305): `--all`, `--problems all` and `--fluency-all` honour it (their items are in the sharded list; `--all` already contains the 88 problem sets and 102 Fluency sets, so `extras` plays them a second time in their own profile, as briefed). `--drills` does NOT honour `--shard`: it plays all 278 drill files and the session in one process, about 25 minutes desktop here (5 s a drill), more on C++. Not over 40, but split anyway by naming drills with `--drill <id>` in three parts, `--session` in part 1 (equivalent to `--drills`; `playthrough.mjs` untouched). `--routes-only` is not shardable (routes run as shard 1 of `--all`); the play legs pass `--no-routes` so shard 1 is not heavier. Routes took over 110 s locally and did not finish in the test window; budget 8 to 12 minutes, unmeasured.

Runner minutes (estimates, from a slow sandbox where a lesson takes about 10 s): play leg about 21 (128 items), 32 legs about 670; extras about 190; tests-browser about 40; validate-tests about 12; static about 12; setup overhead about 1 to 1.5 per job over 60 jobs. About 1000 runner minutes and 25 to 30 minutes wall clock per full run. First run downloads Chromium (cache after). The `--changed --cache` slot is the commented block in `play`.

### Test files on a real CDN (no `--local-cdn`)

Every browser test routes jsDelivr to a local folder only when a local CDN is given, so with none they use the network. Three behave differently:

- Need the Compute Engine as a file and exit 2 without: `test-answer-forms` (its part 5 also needs MathLive as a file), `test-expr-equations`, `test-grade-ab3`. Cannot run on the bare CDN. They run in CI against a lean local copy (Compute Engine 0.30.2 and MathLive 0.105.0 tarballs from the npm registry, about 2 s, no Pyodide).
- Skip their expression part without it, with a note: `test-engine-runtime` (unit tests), `test-fluency` (expression families unit part), `test-problems` (part B), `test-validate-band-rules` (value comparison). Given the lean copy so nothing is dropped (band-rules through `ZQ_LOCAL_CDN`, no flag).
- Everything else (`check-first`, `today-tested-out`, `bank-code`, `drill-page`, `drill-recursion`, `planted-check`, `playthrough-overflow`, `playthrough-tall`, `test-validate-*` other than band-rules) runs on the real network. Locally verified with the lean copy: answer-forms 361/361 (24 s), engine-runtime 45 s, problems 19/19 (16 s). `test-fluency` did not finish in 100 s here (its length in CI is unknown; the grading leg has a 45 minute limit). The Pyodide and C++ tests could not be run against the real CDN from the sandbox (jsDelivr is blocked); they were run in earlier passes with `--local-cdn`.

## B. grade-all

Widget code run in a fake DOM (real `grade.js`, `_base.js`, expression, numeric, choice, multi, table; routing checked by the key each value gets). Covered: expression and numeric (single and set answers), choice, multi, table cells (answers, text `accept`, cell `wrong[]`), generated Fluency items (2 seeds, drawn with `gen.generate` and `gen.playerItem`; a wrong draw that coincides with another wrong id is a note). Not covered (the grade needs a real DOM or canvas): order, tap-regions, place, drag-point, sketch, manipulate, balance, slider, sliders, trade (DOM or canvas), code (Pyodide, C++), longform (self-graded). Kinds: `key-refused`, `accept-refused`, `wrong-grades-right`, `wrong-misrouted`, `wrong-unrouted`, `choice-key`, `error`. Options: `--file` (repeatable), `--jobs`, `--shard i/n`, `--fluency-seeds`, `--local-cdn`; with no local copy it fetches the Compute Engine from the app's own CDN URL (or `ZQ_CE_URL`, `file:` allowed) and caches it in the temp folder; checked with a `file:` URL, and the closed-network failure message is clear.

Run on all content: 25,276 widgets, 10 failures, all `wrong-misrouted`; about 220 s serial-equivalent in this one-core sandbox (the 16 shards summed), so about 1 to 2 minutes on a 2 to 4 core runner. `test-grade-all.mjs`: 15 of 15, 1.4 s.

One tool fault found and fixed on the way: typing wrong values at 10 significant figures turned 1125899906842624 into 1125899907000000 and reported four `wrong-unrouted` (trees/l8-python-pricer quiz[0], numerics/homework-1 items[1], contests/l5-modulo screens[11]). Values are now typed as written (a percentage at 15 figures). `grade-regression.mjs` keeps its 10 figures (untouched).

### Content faults (not edited; for the main session)

Each is a `wrong[]` value that a learner would type and that routes to another slip's line, so the intended line never shows.

| file | widget | wrong entry | goes to |
| --- | --- | --- | --- |
| courses/ds/review-4.json | items[2].widget | `none0` (value 4) | `nodes` (also value 4, identical entry) |
| courses/estimation/homework-3.json | items[1].widget | `one-pseudo` (`\frac{n+1}{n+1}`, equals 1) | `mle` (tex 1) |
| courses/limits/homework-5.json | items[3].widget | `unsimplified` (`\frac{x^2}{1+x^2}`) | `no-chain` (`\frac{1}{1+1/x^2}`, the same function) |
| courses/markov/l20-when-stopping-fails.json | screens[5].widget | `most` (0.999, tol 0.001) | `win` (1, tol 0.001) |
| courses/multivar/homework-5.json | items[0].widget | `area` (3) | `noJ` |
| courses/multivar/l4-chain-two-inputs.json | screens[8].widget | `per-option` (0.14) | `rates` |
| courses/numerics/l12-stiff-equations.json | screens[0].widget | `small` (5.2222) | `exact` (band reaches it) |
| courses/stat-learning/review-2.json | items[0].widget | `flip` (0.0217) | `pos` |
| courses/taylor/l2-how-wrong.json | screens[10].widget | `per-contract` (0.5) | `zero` |
| courses/trees/l13-rules-of-thumb.json | screens[7].widget | `atm` (7.97) | `rule` (8.0, tol 0.05) |

The browser playthrough is green because it types the key, not each wrong value. Fix by narrowing the earlier band, moving the value, or merging the two entries (two cases, ds/review-4 and the equal expressions, are one slip written twice).

## Owed

- The Pyodide, C++ and fluency test lengths on a real runner are unknown; first Actions run will show them (`tests-browser` legs have 45 minute limits; split `grading` if `test-fluency` is long).
- `playthrough.mjs --drills` has no `--shard`; if the other agent adds one, the extras drill split can use `--drills --shard`.
- grade-all cannot see order, tap-regions, place, drag-point, sketch, manipulate, balance, sliders, trade, code or longform.
