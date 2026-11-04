# Engine pass: CSS for the user's devices (items 507 to 511)

Branch `worktree-agent-adbb585f1ee871c2e`. Devices: iPhone 17 Pro Max (440 x 956), iPad Pro 13-inch (1032 x 1376 and 1376 x 1032). Faults came from `docs/reports/engine-viewports.md`. No content file was edited.

## Changes per fault
1. Code editor (item 508). Not a clip: the editor already scrolls sideways inside its own box (textarea `scrollWidth` 638 against 370 at 440; scrolled to the end, the long line shows whole). Nothing said so, and the screenshot never scrolls it. `js/engine/widgets/code.js` and `cpp-grade.js` set `has-more` on `.wd-ed` while text runs past the right edge (also on resize); `css/widgets.css` draws a 28px fade there. Room under the Check bar: the lesson, homework and exam scroll areas end 56px lower on a phone with `scroll-padding-bottom: 88px`, and `.wd-code` has `scroll-margin-bottom: 88px`, so the last editor line, hints and run output scroll clear of the bar (lesson scroll height 908 to 940 at 440).
2. Exam result at 440 (item 509). Timing, not truncation. The result reveals on timers (count-up 900 ms, tiles up to 2.1 s, `.exm-res.final`) and `shot()` waited only for CSS animations. The 1280 shot read "21 of 30" mid count. Fix is in `tools/playthrough.mjs` `shot()`: it also waits for no `.exm-res:not(.final)` (limit 4 s). After: the 440 result shows score, stamp, pass-mark line, pace line, XP, time and mastery tiles, Back to Review and the skills chart.
3. Side tab (item 510). It was the screens navigator (`.proto`, `js/core.js`), `position: fixed; top: 50%` on the left edge. It now sits in the bottom-left corner, 16px up (safe area respected). On a phone it is a 14 x 32px tab 4px up, clear of the lesson hint button and the centred tab bar. On the iPad and desktop frames it sits in the 32px margin outside the card.
4. Wider column (items 507, 511).
   - `--col` is 780px from 768px up, 540px below (`css/tokens.css`). The lesson, set, review, homework, exam and warm-up columns and every canvas (`.cv { max-width: var(--col) }`) follow it. Onboarding and the drill brief keep 540px (explicit values).
   - Prose (`.t-prose`) and Markdown tables stop at 70ch inside the column (`css/screens/lesson.css`); canvases, tables, widgets and code use the full width.
   - The lesson verdict chip sat in the left gutter at 1200px and up, sized from the column. With a 780px column the gutter is 250px, too narrow, so the chip now stays above the buttons at every width (the layout 768 to 1199 already used). This is a change at 1280 desktop too: there is no way to widen the column at 1376 and keep 540px at 1280 without a touch media query that the playthrough cannot show.
   - Homework model answer: the 110px break-out past the column at 1024px and up is gone (the column is already wide).
   - Set pages (review, practice, redo): the button group is left-aligned with the item's content from 768px up (item 511).
   - Docs: `docs/AUTHORING.md` section 4 (column width paragraph before the `canvas` description), both canvas READMEs ("Column width"), backlog 507 to 511 with a status block.

## Tests (from `app/`, `--local-cdn` scratchpad `pkgs`)
- `validate.mjs`: 0 errors, 541 warnings.
- `--routes-only --mobile --tablet`: All passed. `--routes-only --narrow`: All passed.
- `--lesson ito/l12-barrier-option --lesson series/l4-last-step --set number-sense/review-1 --exam topic-1.5 --drill sample-cpp-row-sums --no-routes --mobile --tablet --shots css-before` and `css-after`: lessons (15 and 14 checks, quiz 4/4), set 9 of 9, exam 30 of 30 pass both before and after. `series/l4-last-step` holds a `plane` canvas, a `table` canvas and an `order`-style recurrence ladder.
- `--all` (desktop only): see the final line below.

## Before and after (screenshots read at 440, 1032, 1376, 1280)
- l12 screen 6 at 1032: before, the column was 540px with 250px empty either side and lines cut at the editor edge; after, the editor and the share-price canvas use 780px, long lines run to the box edge with the fade, prose wraps at about 70 characters.
- Exam topic-1.5 result at 440: complete page (see item 2). At 1032 unchanged (its column is its own 768px).
- series/l4 at 1376: the table, plane canvas, slider and options use 780px; the plane canvas is about 530px tall, so its input sits below the fold at 1376 x 1032 and scrolls.
- number-sense/review-1 at 1376: question, input and Check share one left edge; the column is 780px.
- Lesson check state at 1280: the verdict chip now sits above the buttons inside the column, not in the left gutter.
- Navigator tab: bottom-left at 440, 1032, 1376 and 1280.

## Remaining faults
- `--drill sample-cpp-row-sums --mobile --tablet` throws `ReferenceError: ZQDrill is not defined` at 1032 and 1376 (440 passes). It happens with the unchanged code at HEAD too (checked in a copy of HEAD), and a hand-opened drill at 1032 is fine (`ZQDrill` present, status ready), so it is a playthrough or resize-sequence fault, not a CSS one. Not fixed: out of scope, and the cause was not isolated.
- At 1376 x 1032 (landscape) a tall plane canvas (about 530px) pushes the widget below the fold. Authors can cap it with `canvas.maxHeight`; no global cap added.
- Real touch (hover, `pointer: coarse`, address bar, keyboard) is still not emulated (see engine-viewports.md).
