# Problem sets: fin-ml levels 1 to 3 (brief `docs/briefs/chained.md`, prompts `docs/briefs/chained-prompts.md`)

Files: `app/content/courses/fin-ml/problems-1.json` to `problems-3.json`. Numbers: `docs/reports/problems-fin-ml-numbers.py` (paths from `__file__`; exits 0). Every lesson, review and homework of each level was read first and its numbers, windows, prices and stories noted; each setting below was grepped against the course folder and `app/content/` before writing.

## Level 1 (labels)

| set | item | parts (typed / choice) | lessons drawn on | difficulty |
|---|---|---|---|---|
| problems-1 | p-index-fund-day | 5 (4 / 1) | l1, l2 | 3 |
| problems-1 | p-copper-breakout | 5 (5 / 0) | l2, l3 | 4 |
| problems-1 | p-silver-windows | 5 (5 / 0) | l2, l3, l4 | 4 |
| problems-1 | p-bond-sign-model | 5 (5 / 0) | l1, l4 | 5 |

Typed parts 19 of 20. The one choice is the `first_touch` result, a reading of the walk. The chain in each: bar, label, barrier, exit, loss; meta-labels, base rate, precision, recall, F1; concurrency, weight, $n_{\text{eff}}$, weighted hit rate, honest error; middle-label uniqueness, covered days, $n_{\text{eff}} = 409/10$ exactly, error, $t$ against the majority baseline.

Checks: number script exit 0; validator 0 errors and no warning on the file (a long-sentence, `negative-key`, `shuffle-false` and three `O2-explain-answer` warnings met while drafting were fixed); `grade-all --file` 0 failures (20 widgets); playthrough `--problems fin-ml/problems-1 --local-cdn` green with `--why` (34 typed slips routed) and with `--mobile`; 440 px shots read, the 12-row table and the choice grid fit. Voice scan 35 on the course folder: 0 and 0.

Freshness: `fresh-check --file`: 0 hits and 0 advisories after two edits. The first run gave one text warning (11 shared words with l4's "a label's window runs from its entry day to its ...", rewritten) and two shared-formula advisories ($\sqrt{p(1-p)/n_{\text{eff}}}$ printed in two questions, the l4 formula; the formula was taken out of the questions). Own-course grep of £64.00, 65.28, 61.95, 61.90, 0.7273, 2.5583, 0.6111, 0.0764, 409 and the windows A 0 to 2, B 1 to 5, C 2 to 4, D 4 to 7, E 6 to 8: no shared setting (l4 has a window 0 to 3 and the homework 0 to 4, 2 to 6, 5 to 9, 5 to 6). The stories (index fund, copper miner breakout, silver fund, bond future) appear in fin-ml nowhere; "copper miner", "breakout rule" and "bond future" occur once each in other courses (coint, backtest, linear-maps) in unrelated tasks.
