# Predict first and quiz redo line (ENGINE-BACKLOG 1211, 1212)

**1211.** `canvas.controlsAfter: "correct"` holds the canvas controls disabled (`disabled` plus `aria-disabled`) with the note "Answer first, then run it." until the widget is checked correct; `"check"` opens after any check. A revealed solution opens them. Implemented in `app/js/engine/player.js` (buildScreen), so it covers the bars `sim` chips and every control in `.cvb-extra` and `.lsn-controls`; a MutationObserver catches controls drawn later. Validator: value must be `"correct"` or `"check"`. Documented in AUTHORING and `canvas/README.md`. No content was edited, so `conditional/l3-shrinking` does not yet carry the flag; an author adds it to the simulate screen's canvas.

**1212.** `quizFinished` queues every wrong quiz item, so the wrong chip now shows "Added to your Redo queue."

**Tests.** `app/tools/test-predict-first.mjs` (fixture `tools/fixtures/predict-first`), added to the `ui` leg of acceptance.yml. Without the change 5 checks failed; with it all 10 pass, desktop and `--mobile`. Validator 0 errors; l3-shrinking playthrough green both widths.
