# Engine pass 1213: correct-option canvas patch

Item 1213 (done). A correct `choice` option's `canvas` patch is now applied after a correct check and stays on the solved screen; `multi` applies the patches of the correct options the learner kept. Before, only a wrong pick applied a patch (`showWhy`).

Files: `app/js/engine/widgets/choice.js` and `multi.js` (`showSolved`), `app/js/engine/player.js` (`mark` calls it when `r.ok`), `docs/AUTHORING.md` section 3, `docs/ENGINE-BACKLOG.md`.
The patch is held by the same undo handle as a wrong-pick patch, so Try again and Start over revert it; Continue and the verdict do not. Nothing applies before the check.

Test: `app/tools/test-predict-first.mjs` block 3 with `tools/fixtures/predict-first/l2-correct-patch.json`. Before the player change the two correct-pick checks fail (the bar stays at 0.0); after, all pass at desktop and `--mobile`.

Content affected (existing correct-option patches, found by a script over `app/content`):
- `fin-ml/l1-fixed-horizon` screens[9]: adds the 62.9 "always +1" bar; right after a correct answer.
- `limits/l17-somewhere-in-between` screens[5]: draws the two tangents at the corner; right after a correct answer.
- `conditional/l3-shrinking` quiz[0] (dice question, no canvas): inert. The stocks patch the brief describes is NOT on the "Two stocks" screen (`screens[7]`, option `right`) in the committed file; it sits on the quiz[0] option instead, so the stocks grid still does not shrink. Content fix needed (not made here). With the patch placed on `screens[7]` in a scratch copy, the after-correct shot shows the grid with "Both down" dimmed and the caption "Three equally likely outcomes left, each 1/3" at desktop and 440 px (`correct-patch/stocks-after-correct*.png` in the scratchpad).
