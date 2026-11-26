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

## Fix pass

Opus fixer, from commit bf378b59. Files: `problems-1.json`, `problems-2.json`, `docs/reports/number-sense-problems-concepts.py`, `docs/reports/problems-number-sense-numbers.py`.

1. Fixed. Basis: $0.28 \times 18 = 5.04$, so no 18-hole count gives 0.28 exactly, while $\tfrac{5}{18} = 0.2777\ldots$ is 0.28 to 2 d.p.; $0.28 = \tfrac{7}{25}$ exactly, and $\tfrac{7}{25} - \tfrac{5}{18} = \tfrac{1}{450} > 0$. The question now opens "Her rival played a longer run of holes. The rival was under par on exactly 0.28 of them, 7 holes in every 25." (two sentences, to stay under the 20-word target). Options, feedback and explanation unchanged; the key "The rival" now rests on a stated exact share.

2. Fixed differently. Basis: in `grade.js`, `numGrade` tests the key window ($\pm 0.0005$) before `matchWrong`, and the validator refuses a slip that overlaps the key window, so the auditor's centred slip at the key value could not ship. Each of the nine parts keeps its key and tolerance, and gains two bands either side of the key window: `decimal-low` from the value cut at 2 d.p. up to the window, `decimal-high` from the window up to the value rounded up at 2 d.p. (gap 1e-6 to 2e-6 from the window, clear of every other slip). Both carry the line "Your method is right, but this decimal is rounded or cut short, so it is not exact. The question asks for an exact fraction: type ...", naming the exact form. Probed with the real `numGrade`: 0.71, 0.70, 0.7 and 0.709 for $\tfrac{17}{24}$ now reach the band line; $\tfrac{17}{24}$ and 0.708 stay right; 0.43 for $\tfrac{31}{72}$ (0.000556 below the key) reaches `decimal-low`; every existing slip still fires. The 3-place acceptance is left as it is, a design choice (the window was not to be changed); the correct line shows the exact fraction.

No key, tolerance or existing slip changed; 18 slips added (two per part, nine parts). Scripts: the concepts script was re-pointed (its docstring says so): finding 1's `imprecise` row is now a claim on the new wording, and finding 2's nine `imprecise` key rows are now `correct`, with rows checking both bands and their lines (298 rows, exit 0). The author number script's `frac_part` now requires both bands on any key with no terminating decimal and checks their edges (1,183 checks, 0 failures).

Gates: validator 0 errors (4,615 warnings, unchanged); voice scan 35 on both sets 0 and 0; `run-number-scripts --only number-sense` 7 passed; `grade-all --file` 17 and 12 widgets, 0 failures; playthrough `--problems number-sense/problems-1` and `problems-2`, desktop and `--mobile`, all passed.

## Fix-pass read

Fresh reader, blind to this file and to the course's reports and scripts until the rows below were written. Read: `git show 9bdcea62 -- app/content/courses` (number-sense `problems-1.json`, `problems-2.json`). Script: `docs/reports/number-sense-problems-1-2-fixread.mjs` (run from the repo root: `node docs/reports/number-sense-problems-1-2-fixread.mjs app`, exit 0, "18 slips checked, 0 failures"). It loads the real `app/js/engine/grade.js` and calls `numGrade` on each part's widget. `node tools/grade-all.mjs --file` on both files: 0 failures (17 and 12 widgets).

Scope note: all 18 new slips are in `problems-1.json`. The commit's only change to `problems-2.json` is the golf question.

How the grader reads these parts (`grade.js` `numGrade`, `within`): the key is tried first, `|v - answer| <= 0.0005 + 1e-9`; only then the `wrong[]` entries, in order, each with its own `tol`. So a band can never take a value from the key window, whatever its numbers.

Each key was derived twice: by hand from the question, and with exact `Fraction` arithmetic. Cut and rounded-up 2-place values come from integer arithmetic on the numerator and denominator. "Recurs" means the lowest-terms denominator has a prime factor other than 2 and 5, so no finite decimal equals the key and the line's "not exact" is true for every decimal that can be typed.

### Rows 1 to 18: the slips (`problems-1.json`, `items[i].parts[j].widget.wrong[decimal-low | decimal-high]` and its `feedback.byKey` line)

| # | path | key (derivation) | key window | band | 2-place cut / up | grader probe | verdict |
|---|---|---|---|---|---|---|---|
| 1 | items[1].parts[0] decimal-low | 5/6 ÷ 1/5 = 25/6 = 4.1666…, recurs (6 = 2 × 3) | [4.166167, 4.167167] | [4.160000, 4.166166] | 4.16 / 4.17 | 4.16 and 4.166 give decimal-low; 25/6, `4 1/6`, 50/12, 4.167 correct | correct |
| 2 | items[1].parts[0] decimal-high | same | same | [4.167168, 4.170000] | | 4.17 gives decimal-high | correct |
| 3 | items[1].parts[2] decimal-low | 5/6 − 4/5 = 25/30 − 24/30 = 1/30 = 0.0333…, recurs | [0.032833, 0.033833] | [0.030000, 0.032832] | 0.03 / 0.04 | 0.03 gives decimal-low; 1/30, 2/60, 0.033 correct | correct |
| 4 | items[1].parts[2] decimal-high | same | same | [0.033834, 0.040000] | | 0.034, 0.04 give decimal-high | correct (see note A) |
| 5 | items[2].parts[0] decimal-low | 3/8 + 1/3 = 9/24 + 8/24 = 17/24 = 0.70833…, recurs | [0.707833, 0.708833] | [0.700000, 0.707832] | 0.70 / 0.71 | 0.70, 0.7, 0.705 give decimal-low; 17/24, 0.708 correct | correct |
| 6 | items[2].parts[0] decimal-high | same | same | [0.708834, 0.710000] | | 0.71, 0.709 give decimal-high | correct |
| 7 | items[2].parts[1] decimal-low | 1 − 17/24 = 7/24 = 0.29166…, recurs | [0.291167, 0.292167] | [0.290000, 0.291166] | 0.29 / 0.30 | 0.29, 0.291 give decimal-low; 7/24, 0.292 correct | correct |
| 8 | items[2].parts[1] decimal-high | same | same | [0.292168, 0.300000] | | 0.30 and 0.3 (the 1-place rounding) give decimal-high | correct |
| 9 | items[2].parts[2] decimal-low | 7/24 ÷ 3/8 = 56/72 = 7/9 = 0.7777…, recurs | [0.777278, 0.778278] | [0.770000, 0.777276] | 0.77 / 0.78 | 0.77, 0.777 give decimal-low; 7/9, 14/18, 0.778 correct | correct |
| 10 | items[2].parts[2] decimal-high | same | same | [0.778280, 0.780000] | | 0.78 gives decimal-high | correct |
| 11 | items[2].parts[3] decimal-low | 60 + 7/9 × 60 = 60 + 46 2/3 = 320/3 = 106.666…, recurs | [106.666167, 106.667167] | [106.660000, 106.666166] | 106.66 / 106.67 | 106.66, 106.666 give decimal-low; 320/3, `106 2/3`, 106.667 correct | correct |
| 12 | items[2].parts[3] decimal-high | same | same | [106.667168, 106.670000] | | 106.67 gives decimal-high | correct |
| 13 | items[3].parts[2] decimal-low | 4/9 × 3/4 = 12/36 = 1/3 = 0.333…, recurs | [0.332833, 0.333833] | [0.330000, 0.332832] | 0.33 / 0.34 | 0.33 gives decimal-low; 1/3, 2/6, 0.333 correct | correct |
| 14 | items[3].parts[2] decimal-high | same | same | [0.333834, 0.340000] | | 0.334, 0.34 give decimal-high | correct (see note A) |
| 15 | items[3].parts[3] decimal-low | 1/3 + 5/16 = 16/48 + 15/48 = 31/48 = 0.64583…, recurs | [0.645333, 0.646333] | [0.640000, 0.645332] | 0.64 / 0.65 | 0.64, 0.645 give decimal-low; 31/48, 0.646 correct | correct |
| 16 | items[3].parts[3] decimal-high | same | same | [0.646334, 0.650000] | | 0.65 gives decimal-high | correct |
| 17 | items[3].parts[4] decimal-low | 31/48 ÷ 3/2 = 62/144 = 31/72 = 0.43055…, recurs (72 = 8 × 9) | [0.430056, 0.431056] | [0.430000, 0.430054] | 0.43 / 0.44 | 0.43, 0.430 give decimal-low; 31/72, 0.431 correct | correct |
| 18 | items[3].parts[4] decimal-high | same | same | [0.431058, 0.440000] | | 0.44, 0.435 give decimal-high | correct (see note A) |

Checks that hold for all 18 (script, a sweep of every 6-place value from cut − 0.005 to up + 0.005 through `within`):

- Each low band starts at the 2-place cut value and each high band ends at the 2-place rounded-up value, to 1e-9. The rounded 2-place value a learner would type (4.17, 0.03, 0.71, 0.29, 0.78, 106.67, 0.33, 0.65, 0.43) is caught in every part.
- No value matches the key and a band, and no value matches two `wrong[]` entries. The nearest older slip to any band is `loaf-sixth` 0.166667 against the 1/30 bands, far outside.
- Values 0.001 and 0.01 outside [cut, up] get the generic line or an older slip, never a decimal line.
- A one-step search over the part's given numbers (add, subtract, multiply, divide either way, tops-and-bottoms) finds no wrong-method value inside a band, except 1/25 in the 1/30 high band and 7/16 in the 31/72 high band; neither comes from a natural slip on that part's two numbers. So "Your method is right" holds for the answers these bands will in fact see.
- Each line names its own part's key: 25/6 or 4 1/6, 1/30, 17/24, 7/24, 7/9, 106 2/3, 1/3, 31/48, 31/72. The parts that say "or a mixed number" in the line are the two whose question says it. Voice: plain words, sentences of 18 and at most 17 words, no banned punctuation.

### Row 19: the golf question (`problems-2.json`, `p-golf-card`, part 4 question)

| # | claim | verdict | basis |
|---|---|---|---|
| 19 | "Her rival played a longer run of holes. The rival was under par on exactly 0.28 of them, 7 holes in every 25. Using 5/18 = 0.2777…, who was under par on the larger share of holes?" | correct | 7/25 = 28/100 = 0.28 exactly. A share of 7 in 25 needs a multiple of 25 holes, so more than 18: "longer run" is consistent, and the old wording's 0.28 of 18 holes (5.04 holes) is gone. 7/25 − 5/18 = (126 − 125)/450 = 1/450 ≈ 0.0022 > 0, so "The rival" is the one true option; "The golfer" and "equal" are both false. The unchanged lines still fit ("less than 0.28 by about 0.002"; "match to 2 places"). grade-all: keyed option grades correct, 0 failures. |

### Counts

19 rows: 19 correct, 0 wrong, 0 imprecise, 0 misleading, 0 unverified. No fix is required.

### Notes for the orchestrator (not findings on the diff)

- A. The three high bands on keys that round down at 2 places (1/30, 1/3, 31/72) reach up to 0.04, 0.34 and 0.44. No right-method learner rounds 0.0333 up to 0.04 (20% above the key), so the top of those bands is nearly unused; a learner who does land there is told the method is right. I found no natural wrong method that lands there, so the rows stand. If a tighter band is wanted, end each of the three at the 3-place rounded-up value instead: 1/30 `{"value": 0.033917, "tol": {"abs": 0.000083}}`, 1/3 `{"value": 0.333917, "tol": {"abs": 0.000083}}`, 31/72 `{"value": 0.431529, "tol": {"abs": 0.000471}}` (bands [0.033834, 0.034], [0.333834, 0.334], [0.431058, 0.432]).
- B. Older than this commit: the key tolerance of 0.0005 grades the 3-place rounded decimal correct in all nine parts (4.167, 0.033, 0.708, 0.292, 0.778, 106.667, 0.333, 0.646, 0.431), while the question asks for an exact fraction and the new lines tell a 2-place typist the decimal "is not exact". The 3-place cut value (4.166, 0.291, 0.777, 106.666, 0.645, 0.430) gets the decimal line. Each line is true as written; the grading is uneven between 4.166 and 4.167. Closing it means an exact key (`tol` 0.0000005 on the 6-place answer) with the bands widened to meet it, which is an authoring decision, not a correction.
- C. A right method with 2-place working can fall outside a band and get the generic line: 0.83 × 5 = 4.15 in the loaves part, 0.78 × 60 + 60 = 106.8 in the minutes part. The generic lines there restate the method, so nothing false is said.
- D. Two parts leave a seam one millionth wide between band and key (7/9 at 0.777277 and 0.778279; 31/72 at 0.430055 and 0.431057). Those four 6-place values get the generic line. No learner types them.
