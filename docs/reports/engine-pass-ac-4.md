# Engine pass AC part 4: fixes from the first full CI run

Files: `.github/actions/zq-setup/action.yml`, `app/tools/playthrough.mjs`, `app/tools/test-drill-page.mjs`, `app/tools/fetch-local-cdn.sh`, `docs/CI.md`. No content, engine JS or CSS changed.

## 1. test-drill-page: Playwright not found (python leg)
- Cause: the test copies `app/` to the OS temp dir and spawned the copy's `tools/playthrough.mjs`. CI installs Playwright with `npm i --no-save` into the workspace root, so `import('playwright')` resolves for files under the workspace but not for a temp copy; the `npm root -g` and `NODE_PATH` fallbacks found nothing either (NODE_PATH unset).
- Fix: `test-drill-page.mjs` spawns the in-place `tools/playthrough.mjs` with `ZQ_APP_DIR=<copy>` (what `test-bank-code`, `test-playthrough-overflow`, `test-playthrough-tall` already do). The setup action now also exports `NODE_PATH=$GITHUB_WORKSPACE/node_modules` so the loaders' fallback works for any future copy-based caller.
- Other tests checked: `test-bank-code`, `test-planted-check`, `test-playthrough-*`, `test-drill-recursion`, `test-validate-near-miss` use `HERE` for the browser tool or spawn only `validate.mjs` (no Playwright). None has the fault.
- Checked: `test-drill-page.mjs` passes locally (8 cases, including the new one below). Only CI confirms the in-place resolution on the runner (it is the same path the other copy-based tests already take there).

## 2. Fluency "the same seed drew different questions"
- Cause, reproduced: the check compared `innerText` of the whole `.lsn-set-body`, which includes the answer widget. The expression widget shows "Loading the maths editor" until MathLive and the Compute Engine arrive. On the real CDN the first question of the first attempt can still be loading when read; the second attempt reads it loaded. The draw itself is deterministic (seeded, no time, no carried state; `gen.js` has no `Math.random`). Both sets use the expression widget, which is why only Fluency sets of that kind flaked, one viewport at a time.
- Reproduction: new `ZQ_CDN_DELAY_MS=1500` (each local-CDN file waits) made the old check fail on `like-terms` at question 1 with exactly that text; the old script (unmodified HEAD logic) failed, the new one passes.
- Fix: the check reads the question line (`.lsn-q`) only, not the widget; the failure line now names the first differing question and prints both lists. Not weakened: the question text is exactly what the seed controls.
- Checked: both sets, desktop and `--mobile`, with delays 1500 and 2500 ms: all pass. Not run: ten full repeats per set and viewport (35 s each); the race is deterministic under delay, so repeats add little.

## 3. Drills at 440 px: "the brief runs past the right edge: path"
- Cause: not real fonts. The element is the SVG `path` of a KaTeX radical (`svg < span.hide-tail`), whose geometry is 400000 units wide and clipped by its own overflow-hidden box by design; `getBoundingClientRect` reports the unclipped path (right 8016 against 283). The five drills have a `\sqrt` in the brief. Reproduced locally with and without real fonts, so the first local passes were not reflecting this check. Wide display maths already scrolls inside `.katex-display` (components.css), so no CSS change is needed.
- Fix: `briefClipped` skips `.katex svg` (the rest of a formula is still checked); its message now names the tag, ancestors and pixel overshoot. New case in `test-drill-page.mjs`: a brief with `\sqrt{252}` and a root of a fraction passes at 440 px, while the existing 40-term formula still fails.
- Real fonts locally: the sandbox reaches fonts.googleapis.com and fonts.gstatic.com. `fetch-local-cdn.sh` now fetches `fonts/fonts.css` and the woff2 files (optional, idempotent, `.complete` marker; fetched into the pkgs folder), and `playthrough.mjs --local-cdn` serves them when `fonts/fonts.css` exists, else the empty stub as before.
- Checked: all five drills, desktop and `--mobile`, real fonts: pass.

## 4. play 11: `review/research-int/review-1` timed checks time out
- Cause: a real harness fault, not runner slowness. It reproduces locally with `--set research-int/review-1` on a fresh profile. `timedChecks` and `timedPartsChecks` run before `playSet`, and only `playSet` unlocks the review's prerequisites, so a shard that holds the review without its lessons sees the locked card ("59 things to finish") and `ZQ.test` never appears (20 s wait).
- Fix: `timedChecks` calls `unlockRoute` first (`timedPartsChecks` runs after it). The two `threw` lines now include the hash, `ZQ.test.current()` and the page text, so a recurrence explains itself. The 20 s default is unchanged.
- Checked: the review now passes all three lines (timed, timed parts, play) locally.

## ZQ_LOCAL_CDN inheritance
- `delete process.env.ZQ_LOCAL_CDN` in `test-validate-band-rules.mjs` is sound: `cdn` is read from argv or the env on the line before the delete, and the "without" run spawns `validate.mjs` with the then-current environment. The test passes (41 of 41) with `--local-cdn` and with the variable set.
- Others: only band-rules also needs a CDN for its with-case. Other `test-validate-*` files spawn `validate.mjs` without a CDN, and `validate.mjs` reads `ZQ_LOCAL_CDN`, so locally an exported variable would change what they run; CI sets it inline on band-rules only (acceptance.yml line 188), so CI is not affected. Not changed.

## Verified
`validate.mjs` 0 errors (manifest unchanged); `ci-coverage` 49 files 0 problems; `test-drill-page`, `test-grade-all` (15), `test-validate-band-rules` (41), `test-playthrough-changed` pass; the five drills both viewports; the two Fluency sets both viewports.

## Only CI can confirm
Playwright resolution for `test-drill-page` on the runner; that the Fluency pair stops flaking against the real jsDelivr (the cause is reproduced and removed, but the load timing is the runner's); `play 11` on its shard; and that the drills pass with the runner's real Google Fonts (verified here with the same fonts fetched from Google).
