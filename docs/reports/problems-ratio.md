# Problem sets: ratio, levels 1 to 3

Brief: `docs/briefs/chained.md` (PLAN 2d item M). Files: `app/content/courses/ratio/problems-1.json`, `problems-2.json`, `problems-3.json`. Number script: `docs/reports/problems-ratio-numbers.py`.

## Sets

| Set | Item | Parts (typed / choice) | Lessons drawn on | Difficulty |
|---|---|---|---|---|
| problems-1 | p-pension-split | 5 (5 / 0) | l1, l2, l4, l3 | 4 |
| problems-1 | p-platform-fee | 4 (4 / 0) | l1, l2, l4, l3 | 3 |
| problems-1 | p-phone-rise | 4 (4 / 0) | l1, l4, l3 | 3 |
| problems-1 | p-savings-tax | 4 (3 / 1) | l2, l3 | 5 |
| problems-2 | p-share-week | 4 (4 / 0) | l5, l7, l6 | 4 |
| problems-2 | p-laptop-sale | 3 (3 / 0) | l6, l5, l7 | 3 |
| problems-2 | p-fund-two-years | 4 (4 / 0) | l5, l8 (square root from number-sense L3) | 4 |
| problems-2 | p-fund-six-months | 4 (4 / 0) | l8, l7, l5, l6 | 5 |
| problems-3 | p-partners-profit | 4 (4 / 0) | l10, l9 | 3 |
| problems-3 | p-print-run | 4 (3 / 1) | l11, l12, l10 | 4 |
| problems-3 | p-coffee-suppliers | 4 (4 / 0) | l12, l13, l10 | 4 |
| problems-3 | p-villa-split | 4 (4 / 0) | l11, l13, l9 | 5 |

17, 15 and 16 parts; 46 of 48 typed. Every lesson of each level appears in at least one problem; each set has a 5. Each later part restates the value it uses.

## Checks

1. `problems-ratio-numbers.py` (venv python): 981 checks, 0 failures, exit 0; numbers_lib `check_wrongs` 29 of 29.
2. Validator: 0 errors, no warnings on the three files (`over100: true` on the four widgets whose slips exceed 100%).
3. Playthrough `--problems ratio/problems-<n> --local-cdn <pkgs>`, desktop and `--mobile`: all green. Shots at 440 px read: no layout faults.
4. Voice scan 35 on the course folder: 0 and 0.
5. `grade-all --file`: 0 failures on each set.

## Fresh-check (`--file ... --cross-numbers`)

0 hits. Advisories judged:
- `markets/review-2` item 3 (21% over two years is 10% a year): a real reuse in the first draft of `p-fund-two-years`. Renumbered to £6,250, £7,840 and 12%.
- `quadratics/l4` screen 8 (a stock up 8% then down 8%): the first draft of `p-fund-six-months` used 8%. Moved to 9% and £52,000 to keep clear.
- The rest share one or two common figures by chance in other settings (equations van and interest sets, markets margin, `ratio/review-1` 35% of £120, `ratio/l13` slip values 0.84 and 0.16): kept.

## Inbox

Two bullets under `Raised later (problems ratio):` in `docs/BACKLOG-INBOX.md`.
