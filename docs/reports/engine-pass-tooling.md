# Engine pass: tooling (items 570 to 572)

- 570 `mock-sample-draw`: the intermittent "scored 0" was the check's own assumption. The exam's papers are drawn, so the file lists no items and "an item with parts first" was never detected; when the draw put `sd-parts` first, the one answer (part 1 only) earned partial credit and no whole item, score 0. Fix in `tools/playthrough.mjs`: `drawnParts` from `ZQ.test.current().parts`, plus a wait for `state === 'engaged'` before zeroing the clock. 12 of 12 desktop and 3 of 3 `--mobile` runs green.
- 571 `tools/lint-dup-keys.mjs` and `tools/test-lint-dup-keys.mjs`: a first version that flagged every later `X.y =` gave 155 findings (local state objects); narrowed to function-for-function replacement, which is the shadowed-method class. It catches the historical `content.js` bug (checked on the file at 9c70a04^). `app/js` is clean, so no engine change.
- 572 `tools/test-check-first.mjs`: edge `proof` level 2 / `counting/L1`; 17 assertions, desktop and mobile.
- Commands: `node tools/test-lint-dup-keys.mjs`; `node tools/test-check-first.mjs [--mobile] --local-cdn <pkgs>`.
