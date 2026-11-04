# Engine pass: playthrough viewports (items 504 to 506)

Branch `worktree-agent-adfd9efa7c51d1465`. Files: `app/tools/playthrough.mjs`, `docs/AUTHORING.md`, `docs/LEVEL-BRIEF.md`, `docs/ENGINE-BACKLOG.md` (status block), `docs/BACKLOG-INBOX.md`.

## Changes
- 504 `--mobile` now runs 440 x 956 (iPhone 17 Pro Max) everywhere it was used: screenshots (`-440`), drills and the session, gating (locked card, Refresh chip), Prepare for, and every `wide()` check.
- 505 `--narrow` runs the old 390 x 844 pass (`-390`). It works alone or beside `--mobile`.
- 506 `--tablet` runs 1032 x 1376 and 1376 x 1032 (`-1032`, `-1376`) wherever `--mobile` adds a pass. `--mobile --tablet` runs desktop, phone and both orientations.
- Item 4: one `setVp(view)` helper sets width and height for every pass (the old code fixed height at 844 and restored 860). Each pass uses its device height.
- Messages name the width actually used (`${curVp.w} px`); the gating line lists the widths run. `grep 390` now finds only the `--narrow` definition and help text. Help text states touch is not emulated.
- Added: a screenshot at an extra width prints a `note` line if the page is wider than the window (not a failure).
- Drills and the session repeat once per extra viewport.
- Real touch pass (inbox bullet, not built): needs a separate context per device with `viewport`, `deviceScaleFactor`, `isMobile: true`, `hasTouch: true` and an iOS user agent, `page.tap()` and touch drags, no hover, and a visual-viewport check for the address bar and keyboard.

## Tests (from `app/`, local packages)
- `validate.mjs`: 0 errors, 544 warnings.
- `--routes-only --mobile --tablet`: All passed (gating at 1280, 440, 1032, 1376).
- `--routes-only --narrow`: All passed (gating at 1280, 390).
- `--lesson ito/l12-barrier-option --set number-sense/review-1 --exam topic-1.5 --no-routes --mobile --tablet --shots <scratchpad>/viewport-shots`: All passed (lesson 15 checks, set 9 of 9, exam 30 of 30). No `note` overflow lines. 129+ PNGs read in part.
- Not run: the full `--all` (the engine items change only test-tool behaviour; the machine was heavily shared and one exam pass at three extra widths took over an hour).

## Layout observations (viewed: l12 barrier lessons, review-1, topic-1.5)
No sideways scroll at 440, 1032 or 1376. Not fixed, listed for the orchestrator:
- `#exam/topic-1.5` result at 440: the result page shows only the score and stamp, with no pass-mark line, time-used or XP tiles that appear at 1032. Either the page is still fading in when the resized shot is taken, or it truncates at 440. Needs a check.
- Lesson and set screens at 1032 and 1376: the content column stays about 540 px wide, leaving wide empty margins; at 1032 portrait the screen is more than half empty below the content.
- `#set/number-sense/review-1` items at 1376: the Check button is centred while the question and input are left aligned.
- Lesson code editor (`ito/l12` screen 06) at 440 and 1032: code lines are cut at the right edge (the editor scrolls sideways); at 440 the editor runs under the fixed Check bar.
- The left-edge side tab (grid icon) floats mid-screen at every width and, at 440, sits over the content margin.
