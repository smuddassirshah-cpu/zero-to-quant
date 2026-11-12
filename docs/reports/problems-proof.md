# Problem sets: proof, levels 1 to 3

Brief: `docs/briefs/chained.md` (PLAN 2d item M). Files: `app/content/courses/proof/problems-1.json`, `problems-2.json`, `problems-3.json`. Number script: `docs/reports/problems-proof-numbers.py`. Pattern: `ratio/problems-1.json`.

## Sets

| Set | Item | Parts (typed / choice) | Lessons drawn on | Difficulty |
|---|---|---|---|---|
| problems-1 | p-leverage-calls | 4 (3 / 1) | l2, l3, l4, l5 | 3 |
| problems-1 | p-spread-signal | 4 (3 / 1) | l1, l2, l3 | 4 |
| problems-1 | p-fund-thresholds | 4 (3 / 1) | l4, l5 | 5 |
| problems-2 | p-multiples-forty | 5 (5 / 0) | l6, l7 | 3 |
| problems-2 | p-jobs-servers | 5 (4 / 1) | l8, l9 (product rule from counting L1) | 4 |
| problems-2 | p-rule-and-domain | 4 (3 / 1) | l8, l9 | 4 |
| problems-2 | p-shift-images | 4 (3 / 1) | l7, l8, l9 | 5 |
| problems-3 | p-two-odd-squares | 4 (3 / 1) | l10, l14 (converse from l3) | 3 |
| problems-3 | p-step-three-sum | 4 (4 / 0) | l13, l14 | 5 |
| problems-3 | p-six-nine-lots | 4 (3 / 1) | l12, l10, l15 | 4 |
| problems-3 | p-even-test-contra | 4 (2 / 2) | l11, l15 | 3 |

12, 18 and 16 parts; typed 9 of 12, 15 of 18, 12 of 16 (36 of 46). Every lesson of each level is in at least one problem, each problem draws on two or more, each set has a 5. Choice parts are the judgement steps (which negation, which contrapositive, which opening, which reason). Each later part restates the value it uses. Typed answers are counts and brackets: no widget grades a logic formula (inbox).

## Checks

1. `problems-proof-numbers.py` (venv python): 575 checks, 0 failures, exit 0; numbers_lib `check_wrongs` 19, 29 and 16 of 16, all passed. Method 2 is brute force throughout (the 40 accounts built, the truth table enumerated, every threshold scanned, all 1296 functions listed, integer pairs searched in a 601 by 601 box, sums term by term).
2. Validator: 0 errors, no warnings on the three files.
3. Playthrough `--problems proof/problems-<n> --local-cdn <pkgs>`, desktop and `--mobile`: all green (sets 2 and 3 replayed after the last edits). Shots at 440 px read: no layout faults; the step fractions moved to `\dfrac` for size.
4. Voice scan 35 on the course folder: 0 and 0.
5. `grade-all --file`: 0 failures on each set.

## Freshness

`fresh-check --file ... --cross-numbers`: 0 hits on all three. One advisory on `p-step-three-sum` against `l13` screen 4, the shared template $\tfrac{(k+1)(\square)}{2}$: the standard induction-step task with another sum ($k(3k-1)/2$ against $k(k+1)/2$). Kept.

Own grep per problem (key numbers and setting; own course folder first, then all of `app/content/`, the three new files left out):
- p-leverage-calls (40 accounts, 12/15/9, leverage over 5, margin call): own 0; all: "margin call" in markets and backtest margin lessons, other settings. Clean.
- p-spread-signal (£8.40 vs £8.25, 2.6 million, 3 million shares, 4 pence, $(P \lor Q) \land \lnot R$): own 0; £8.40 and £8.25 occur in unrelated items; "20-day average" in markov and backtest. Clean.
- p-fund-thresholds (the 4 by 4 grid, A($t$), B(5)): own 0; all 0 for the grid. Clean.
- p-multiples-forty ($U = \{1, \dots, 40\}$, multiples of 4 and 6, 12, 24, 36): own 0; `number-sense/l16` has multiples of 4 and 6 meeting at 12 in a months setting. Different task. Clean.
- p-jobs-servers (4 jobs, 6 servers, 1296, 360, 936): own 0; 1296 and 936 occur as dice and decimal figures elsewhere. Clean.
- p-rule-and-domain ($9 - 3x$, $f^{-1}(-6)$): own 0, all 0.
- p-shift-images (two to a desk, $\{1, 2, 3, 5\}$, $\{2, 4, 6, 7\}$): own 0, all 0.
- p-two-odd-squares ($m^2 + n^2$, $4(j^2 + j + k^2 + k) + 2$, 7 and 11, 42): own 0; all: `trig` fluency uses $m^2 + n^2$ for triangle sides. Clean. **Replaced draft:** the first item 1 (odd $n$, $n^2 - 1$ a multiple of 8) repeated `exams/stage-0.json` claim for claim; caught by grep, not by fresh-check (inbox), and rewritten.
- p-step-three-sum ($1 + 4 + 7$, $3n - 2$, $4n - 3$, 145, 2380, 118): own 0; 2380 elsewhere is a slip value in `exams/topic-0.3` (money) and 0.2380 in `trees`. Clean.
- p-six-nine-lots ($6x + 9y = 100$, 102, 14): own 0, all 0 for the equation.
- p-even-test-contra ($n^2 + 6n + 1$, $n = -3$, $-8$): own 0, all 0. The first draft used $n^2 + 4n + 1$, whose bracket $2k^2 + 4k$ appears in `exams/topic-0.6` (this course's topic exam) inside another claim; changed to keep clear.

## Inbox

Two bullets under `Raised later (problems proof):` in `docs/BACKLOG-INBOX.md`.

## Course.json

No proposal.
