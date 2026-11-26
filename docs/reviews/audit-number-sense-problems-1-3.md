# Concept audit: number-sense problems-1 to problems-3 (blind)

Scope: the chained problem sets `app/content/courses/number-sense/problems-1.json`, `problems-2.json` and `problems-3.json` at commit c4f38a8c (problems-4 was audited with level 4). Stage 0 ledger depth. Read blind: no earlier review, audit or author report on number-sense was opened before the ledger and the findings below were written.

Ledger: `docs/reports/audit-number-sense-problems-1-3-ledger.md`, 253 rows (243 correct, 10 imprecise, 0 wrong, 0 misleading, 0 unverified). Script: `docs/reports/number-sense-problems-concepts.py`, exit 0.

## What was checked

- All 40 parts (38 numeric, 2 choice): every key recomputed in exact fractions from the prose alone.
- All 100 numeric slips: each stored value equals the value its named mistake gives, and each slip window is clear of the answer window, so no slip can be marked right and no right answer is caught by a slip. The engine tests the key before the slips (`grade.js` `numGrade`).
- All 4 wrong choice options: wrong under every reading.
- 23 carried values: the figure each later question tells the learner to use equals the earlier key.
- 38 stated rules and comparisons in feedback and explanations (for example "less than A prints alone", "sits between the two jugs' shares", "a little more than the estimate").
- Alternative conventions that a careful learner could defend (half-even rounding, product rounded again, 365.25-day year, 2 s.f. year in the estimate, share plus shortfall): all land on the key, none on a slip.

Nothing in these sets is empirical, so the script has no Monte Carlo.

## Findings

1. `problems-2.json` | `items[1].parts[3].question` (and `widget.options[2]`) | imprecise, minor | The rival is "under par on 0.28 of her holes", read as an exact share. No whole number of holes in an 18-hole round gives 0.28 (0.28 × 18 = 5.04), and the part before has just taught that $\tfrac{5}{18}$ is 0.278 to 3 places, which is 0.28 to 2 places. A learner can fairly read 0.28 as a rounded share of 18 holes, which is 5 holes, the same as the golfer; the key "The rival" then rests on an unstated convention that 0.28 is exact. | 5/18 = 0.2777…, 0.28 = 7/25, gap 1/450; 7/25 needs a multiple of 25 holes. Script rows `problems-2 items[1].parts[3]`. | Replace the first sentence of the question with: `Over a longer run of holes her rival was under par on exactly 0.28 of them, 7 holes in every 25.` Keep the rest. The options, feedback and explanation then stand as written.

2. `problems-1.json` | `items[1].parts[0]`, `items[1].parts[2]`, `items[2].parts[0..3]`, `items[3].parts[2..4]` (`widget.tol`, `feedback.generic`) | imprecise, minor | These nine parts ask for "an exact fraction" and have a non-terminating key. The window `abs 0.0005` marks the 3-place decimal right (0.708 for $\tfrac{17}{24}$, 0.333 for $\tfrac{1}{3}$), which is not exact, yet sends the 2-place decimal (0.71, 0.33, 106.67) to the generic line, which names a method fault ("Rename both in twenty-fourths", "Turn the part hour into minutes, then add the first hour"). The stated convention and the graded one differ, and a learner with the right method and a rounded answer is told the method is wrong. | `within(0.71, 0.708333, 0.0005)` is false and no slip is near; `within(0.708, …)` is true. Nine ledger rows marked imprecise. | Add to each of the nine parts a slip placed after the existing ones, with the key's value and a wide window, for example for `items[2].parts[0]`: `{"id": "rounded", "value": 0.708333, "tol": {"abs": 0.01}}` and `"rounded": "That is the right amount, rounded. Type the exact fraction instead, such as 17/24."` The key is tested first, so the slip only catches near misses. Values and lines for the other eight: 25/6 (4.166667), 1/30 (0.033333, window 0.005), 7/24 (0.291667), 7/9 (0.777778), 320/3 (106.666667, window 0.05), 1/3 (0.333333), 31/48 (0.645833), 31/72 (0.430556). If the validator refuses a slip that overlaps the key, this is the engine item raised in the inbox.

No `wrong` and no `misleading` finding. Both findings are minor: neither changes a definition, rule, method or key.

## Notes that are not findings

- `problems-1` `items[3].parts[4].feedback.byKey.shares-added`: "the share is half of that" is true only because the two jugs hold the same amount; the line says "the bowl holds two jugs" and the prose gives both as $\tfrac{3}{4}$ litre, so the condition is stated.
- `problems-3` `items[2].parts[3].explain`: "a little more than the estimate of 3, as 8,760 is less than 9,000". The estimate 3 is 3.33… rounded down, so two effects push the same way; the stated reason is true and the direction is right.
- `problems-2` `items[2].parts[3]`: the window `abs 0.005` on a money key of £2.85 is wider than a penny needs, but no slip or defensible value falls inside it.
- `problems-3` `items[2].parts[2]`: a learner who carries the 2 s.f. year (8,800) still gets 3, so the chain forgives that slip; harmless.

## Overlap with earlier reads

Earlier reads, opened only after the ledger and findings were written: `docs/reviews/review-problems-number-sense-1-3.md` (16 findings, all fixed before this audit's commit) and the author report `docs/reports/problems-number-sense.md`. Of the earlier 16, three are conceptual in this brief's sense (9: "mean" used before it is taught; 10: an unrounded value marked right on a rounding part; 12: a calculator convention left unstated). The other 13 are reuse, wording, units and missing slip lines. This audit read the fixed text, so it could not re-find them; all three fixes hold (rows `problems-2 items[1].parts[1]`, `items[1].parts[2]`, `items[2].parts[1]`, `problems-3 items[1].parts[2]`).

| conceptual findings | count |
|---|---|
| this audit only | 2 (both minor, imprecise) |
| earlier review only | 3 (fixed before this read) |
| both | 0 |
| new `wrong` | 0 |

Finding 2 was seen by the earlier reader and held to be intended ("Fraction parts say exact fraction and refuse a 2-place decimal, as stated", its Verified section). It is kept here because the same window takes a 3-place decimal, so the stated rule is not the graded one; a fixer may fairly rule it a design choice. Finding 1 appears in neither earlier read.

## Checks run

| check | result |
|---|---|
| `docs/reports/number-sense-problems-concepts.py` (venv Python) | 253 rows, 0 failures, exit 0 |
| validator | 0 errors (4,615 warnings in all); `manifest.json` unchanged |
| `run-number-scripts.mjs --only number-sense` | 7 scripts, 7 passed, 0 new failures |
| `grade-all.mjs --file`, three sets, `--local-cdn` | 17, 12 and 11 widgets, 0 failures each |
| playthrough | not run, as the auditor rules say |

No content, engine or state file was edited.
