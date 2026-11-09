# Engine 701: full-height marked shots and display-overflow check

- `app/tools/playthrough.mjs`: the `-marked` shot is an element screenshot of `.hw-item` (whole card, 440 px: 400 x 2335 and taller). After marking, every `.katex-display` in the card is checked at desktop and each extra viewport, with or without `--shots`; failure line `<file>#<id>: display wider than its column at <w>px: <TeX 40 chars>`. New env `ZQ_APP_DIR` serves a copy of the app.
- Test: `app/tools/test-playthrough-overflow.mjs` with `app/tools/fixtures/overflow/homework-2.json` (one over-wide, one clean longform), desktop and `--mobile`: passes.
- Flagged displays (content not touched):
  - `ito/homework-2#h-why-not-chain` at 440px (`d(\ln S) = \frac{dS}{S} - \tfrac12\sigma...`), mobile only.
  - `analysis/homework-3`: none (desktop, mobile). `ito/homework-2` desktop: none.
- Docs: AUTHORING section 5, LEVEL-BRIEF, ENGINE-BACKLOG 701 Done.
