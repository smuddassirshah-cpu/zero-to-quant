# markets level 3: performance task (perf retrofit)

- `app/content/courses/markets/homework-3.json`, item `h-carry-two-rates`, index 9 (10 of 10), appended, nothing converted. Kind `derivation`, difficulty 5, `fi-forwards`.
- Matched objective (l10): "Derive the forward price from the cost of carry." The level's only derive objective.
- Task: borrow 7%, deposit 3%, £0.50 stock loan fee, so a band: cash and carry gives 67.2387, reverse 64.2021; one rate and no fee, they meet at £65.97 (5%). Optional: a £67.80 quote, £0.56.
- Rubric 3, 3, 3, 1; rows 1 to 3 `required` (one per part, worded by result); row 4 optional. `rubric-passes.mjs`: only row 4 can be left out.
- Overlapping screens: l10 screens[0] to [4], [6], [7], quiz 3; l12 screens[2], [3]; homework-3 `h-derive-dividend`, `h-carry-arb`, `h-airline-hedge`; review-3 items 2, 7. New: two rates, a band, the fee, the cheapest dividend funding, the collapse.
- Freshness grep: deposit, borrow at, lend at, two rates, band, spread, stock loan fee, bound figures. `fresh-check --file`: 0 hits.
- `homework-2#h-bond-and-share` (a) split with `aligned`, wording unchanged.

## Gates

1. Validator, `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors (expected perf-pending warning); manifest restored.
2. Voice, `VOICE_BASE=app/content/courses/markets python3 docs/reviews/voice-scan.py 35`: 0 and 0.
3. Numbers script, `python3 -I docs/reports/markets-3-perf-numbers.py`: exit 0, 740 checks (closed forms against a Decimal ledger with bisection).
4. Playthrough, `node tools/playthrough.mjs --set markets/homework-3 --local-cdn <pkgs>` and `markets/homework-2`, with and without `--mobile`: All passed in all four runs (homework-3 10 of 10, 2 longform marked by the button); 1280 and 440 px shots read, no sideways display. No older homework-3 item needed `aligned`.

No backlog bullets. No course.json change.
