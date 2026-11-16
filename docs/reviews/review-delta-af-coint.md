# Delta read AF, coint problem sets 1 to 3: the re-authored problems and the fix pass

Counts: `wrong` 0, `misleading` 4 (findings 1, 2, 4, 5), `continuity` 3 (3, 6, 7), `reuse` 0, `re-author` 0, `voice` 0, `other` 0. No key, `wrong` value or printed number is mistaken. All three new problems are ruled clean on reuse. Every finding is a line or a number of wording weight; none blocks a level.

Scope, at commit e588808f (fix pass b3b6908d, f8928550, de5856c3 over the second read b1feb91a), found by a leaf-by-leaf diff of the three sets against b1feb91a:

- new: `problems-1` `p-screen-real-share`, `problems-2` `p-smelter-tls`, `problems-3` `p-glassmaker-borrow`;
- changed: `p-paper-mill-multiple` prose, part 1 (new key 0.0036), part 2 question; `p-cocoa-chip-levels` part 1 lines, part 3 question, part 4 key option and lines; `p-lessor-window` part 1 and part 3 lines; `p-three-distributors` part 1 lines, part 4 `no-mean`; `p-tyre-vecm` part 1 lines, part 3 `one-over-b`; `p-housebuilder-trading-years` part 3 question and lines, part 4 question and `tol`; the titles of sets 1 and 2.

Method. Each part in scope was solved from its text before its key was read. No browser, no content or engine edit.

- `docs/reports/delta-review-delta-af-coint-numbers.py` (scratchpad venv Python) imports no earlier script. Routes: Fractions and 20,000 simulated screens for the pair counts; a hand-built Engle-Granger statistic for the powers the stem supposes; a 200-day data set built to have the stem's covariance matrix, then an SVD line, `np.std` of the spread and a perpendicular-distance check; 21 daily fee charges and a grid search for the long entry; a simulated walk for the paper mills; repeated multiplication for $0.92^8$ and $0.92^9$. Each band is rebuilt with the engine's rule ($|x - a| \le \text{tol} + 10^{-9}$, `grade.js`) and fed what a learner types in the form asked.
- Reuse. Every string of the course (12 lessons, 3 reviews, 3 homework files, the other problems) and of `exams/topic-2.2.json` and `exams/stage-2.json` was put in one file, 8,102 lines, and searched for each idea, noun, slip phrase and key number of the three new problems and for the phrases of every replaced line. No mock exam holds an item with a coint skill (`co-` occurs only in `topic-2.2` and `stage-2`); all of `exams/` was searched for the three stories.
- Each fix below was applied to the three files in place, tested, and the files restored with `git checkout`.

## Tool results

| check | as committed | with the seven fixes applied |
|---|---|---|
| `delta-review-delta-af-coint-numbers.py` | 399 checks, 0 failed, 7 FINDING rows, exit 0 | 399 checks, 0 failed, 0 FINDING rows |
| `problems-coint-numbers.py` (author) | 826 checks, 0 failures | 4 failures, all `p-smelter-tls` part 4 (finding 6 changes its numbers; the fixer updates the script) |
| `problems-coint-numbers-read.py` (reader) | 641 checks, 0 FINDING lines | the same |
| validator | 0 errors, 4,585 warnings, two on the sets (long sentences in the first reader's text) | the same |
| voice scan 35, course folder | 0 and 0 | 0 and 0 |
| `fresh-check.mjs --file` | 0 hits each; 3, 2 and 1 advisories, as the author lists | the same |
| `grade-all.mjs --file` | 0 failures on each set | 0 failures on each set |

## Verdict per item

| item | numbers | reuse | chain | findings |
|---|---|---|---|---|
| `p-screen-real-share` (new) | clean | clean | holds; part 5 restates 34.5% | 3, 4 |
| `p-smelter-tls` (new) | clean | clean | holds | 6 |
| `p-glassmaker-borrow` (new) | clean | clean | holds | 1, 2, 7 |
| `p-paper-mill-multiple` prose, parts 1 and 2 | clean | clean, fix as given | part 2 now uses part 1 | 5 |
| `p-cocoa-chip-levels` parts 1, 3, 4 | clean | clean, fix as given | part 3 restates 13.78 | none |
| `p-lessor-window` parts 1, 3 | clean | clean, fix as given | holds | see 6 |
| `p-three-distributors` parts 1, 4 | clean | clean, fix as given | holds | none |
| `p-tyre-vecm` parts 1, 3 | clean | clean, fix as given | holds | none |
| `p-housebuilder-trading-years` parts 3, 4 | clean | clean, fix as given | part 4 follows part 3's ratio | none |

Each of the eleven line fixes was compared, string for string, with the text the second read gave: all were applied exactly. None of the replaced lines shares a phrase with a lesson, review, homework item or exam item (searched: "No log has been taken", "keeps its sign", "hands back", "gives ground", "goes underneath", "settled the matter", "cannot be read", "times over", "clears its critical value", "where its square belongs", "scales its variance").

### Reuse, the three new problems, with both texts

`p-screen-real-share`: clean.

- Lesson: l2 `screens[11]`, "A desk covers 500 shares ... The desk then tests each of the 2,000 for cointegration at 5%." / "If none of the 2,000 were truly cointegrated, about how many would still pass at 5%?" / "$2{,}000 \times 0.05 = 100$ false passes." Ours: "A desk tests 1,200 pairs of mid-cap shares for cointegration ... Suppose 36 of the pairs, 3%, are truly tied and the other 1,164 are not." The lesson's count is the middle step of our part 2 ("$1{,}164 \times 0.05 = 58.2$ false passes"): the level's standard step, with its own numbers, inside a chain no file has. Quiz: l2 `quiz[3]` ("44,850 tests, so about 2,242 false passes at 5% if nothing is cointegrated") and l4 `quiz[1]` ("`coint` rejects at 5% for 29 of them. What is the test's power here" / "Power is the share of true ties the test detects"), against ours "The test's power, 0.40, is its chance of catching a real tie."
- Review: `review-1` `items[7]`, "A screen tests 2,000 pairs of unrelated shares ... How many more false pairs does the ADF value let through". Homework: `homework-1` `items[6]` (screen code; "a few false passes at 5% are also possible"), `items[7]` rubric "Allows for multiple testing if the pair came from a screen".
- Other set problem: `p-cable-sample-length` (same set) turns $\phi$ into a sample length; it holds no count of pairs.
- Exams: `topic-2.2` `items[7]` ("It is only a lack of evidence, and the test has low power on 400 days"); `stage-2` none. Outside the scope, `topic-3.1` has "A researcher tests every pair of 120 shares for cointegration at the 1% level. Suppose no pair is cointegrated", again the all-false count.
- No file mixes tied and untied pairs, or asks what share of the passes is real. A learner meets the false-pass count for the fourth time, but as one step of five.

`p-smelter-tls`: clean.

- Lesson: l5 `screens[6]`, "Its line is the first principal component of the centred pair. That is the covariance eigenvector with the larger eigenvalue, from the Eigen course." / "Complete `tls_ratio(y, x)`." / "The slope of the eigenvector is its $y$ entry over its $x$ entry." Ours, part 1: "Total least squares follows the eigenvector of the covariance matrix with the larger eigenvalue. What is that eigenvalue?" The lesson does it in code on a data set; ours does it by hand from three moments, a task no file has. l5 `screens[9]`: "Total least squares falls between them", which our part 2 confirms with numbers ($0.736 < 0.785 < 0.870$). l6 `screens[2]`: "On day 773, $s = £1.81$ ... Divide the distance from the mean by the sd."
- Review: `review-2` `items[8]` (TLS and units, "TLS depends on the units, unlike either OLS slope"), `items[1]` (a z). Homework: `homework-2` `items[6]` rubric "Mentions total least squares or Johansen as direction-free checks".
- Exam: `topic-2.2` `items[10]`, "the prices have sds of £3.90 for $y$ and £4.50 for $x$, and their correlation is 0.85. A colleague regresses $x$ on $y$. He inverts his slope". Ours starts from a covariance matrix, inverts no slope and prints no correlation; its `other-ratio` slip (1.274, "the vector read the other way up") is the eigenvector's reciprocal, not a regression's. `stage-2` `parts[2].items[1]` (eigenvalues $1 \pm r$ of a correlation matrix, a condition number) shares only the word.
- Other set problems: `p-lessor-window` part 3 and `p-three-distributors` part 4 are also a z from a mean and an sd; see finding 6.

`p-glassmaker-borrow`: clean.

- Lesson: l10 `screens[11]`, option `why`: "Both legs cross a spread, and the short leg also pays a stock loan fee (the Markets course's lesson 12)." This is the course's one mention of the fee; nothing is computed from it. l10 `screens[4]`: "Open a long spread: buy one $y$ at £80.00 and sell $\beta = 1.5$ shares of $x$ at £50.00. Both shares have a 10 bp bid-ask spread." l9 `screens[2]` explain: "A long buys $y$ and sells $\beta$ shares of $x$". Ours: "A long buys one $y$ and sells 1.15 shares of $x$, so it borrows $1.15 \times £36.00 = £41.40$ of $x$." The legs of a long are the course's definition; pricing the sold leg, charging it for 21 days and moving the entry are in no file.
- Review and homework: `review-3` `items[1]` (leg P&L), `items[3]` (costs at 15 bp); `homework-3` `items[1]`, "Each side of each leg costs 4 bp of the pounds traded." No shared number, slip or sentence.
- Exams: `topic-2.2` `items[13]` (positions from a z list), `stage-2` `b-pair-pnl` (bp costs on four fills). Neither has a fee that runs with time.
- Other course, outside the scope: Markets l12, "The stock loan fee is 3% a year on the £50,000.00 sale value", three months. The rule is the same as ours; the story and numbers are not.

### The author's question: is the fee rule stated well enough, and is it right?

Enough: yes. The stem gives all a learner needs: a sold share is borrowed, the fee is a yearly rate on the pounds borrowed, the two rates, 252 days a year and a 21-day holding. Right: yes, as a stated simplification, and it is the rule the curriculum already teaches (Markets l12, a yearly rate on the sale value for a part of a year). Real loans accrue on calendar days and on the marked value; part 2's `calendar-days` line says "The fee here runs on 252 trading days", which is honest. Three things need a touch: one sentence of the stem contradicts part 5 (finding 1), the last line of part 5 claims more than the part shows (finding 2), and the stem does not use the name the course and the Markets course give the fee (finding 7). The author's report says "borrowing fees are not in the course"; l10 `screens[11]` names the stock loan fee once.

## Findings

1. `coint/problems-3.json` | `items[p-glassmaker-borrow].prose` | misleading | "Take a year as 252 trading days and the prices as fixed while a trade is open." Part 5 then earns $2 \times 0.50 = £1.00$ from the spread moving two units of $z$ while the trade is open. Read as written, fixed prices mean a fixed spread and no P&L. The intent is only that the fee is charged on the stem's prices. | Script FINDING 1. | Replace that sentence with: "Take a year as 252 trading days, and charge each fee on these prices for the whole trade." (17 words. No number changes.)

2. `coint/problems-3.json` | `items[p-glassmaker-borrow].parts[4].explain.text` | misleading | "A desk that ignores borrowing fees opens its longs too early." The part shows where a long must open to net what a short nets; it does not show that −2 is too early. A long from −2 still nets $1.00 - 0.207 = £0.793$, a profit. | Script FINDING 2 (0.793 recomputed). | Replace the last sentence, so the text reads: "From −2.37 to 0 a long earns $2.374 \times 0.50 = £1.187$, and its fees take £0.207, leaving £0.98. Opened at −2 it would net only $1.00 - 0.207 = £0.793$."

3. `coint/problems-1.json` | `items[p-screen-real-share].parts[4].question` | continuity | "Compared with 34.5% in part 4, what share of the passes is truly tied now?" The opening asks for a comparison and the question for a share. A learner who answers the comparison types the change, $66.8 - 34.5 = 32.3$ points, which falls to the generic line (the nearest band, `false-share`, is 33.2). The clause is there only to restate part 4. | Script FINDING 3. | Question → "The desk also moves to the 1% level, where four years catch a true tie with chance 0.65. Part 4 gave 34.5% at the 5% level. What share of the passes is truly tied now? Give a percentage to 1 decimal place."

4. `coint/problems-1.json` | `items[p-screen-real-share].parts[2].explain.text` | misleading | "The 5% level caps the false passes per untied pair." A level fixes the chance that an untied pair passes; it caps no count, and "false passes per untied pair" is not a quantity. | Script FINDING 4. | Replace the sentence, so the text reads: "Only 14.4 of the 72.6 passes are tied, 19.8%. The 5% level holds each untied pair's chance of passing at 0.05. But the 1,164 untied pairs outnumber the 36 tied ones about 32 to 1."

5. `coint/problems-1.json` | `items[p-paper-mill-multiple].parts[0].explain.text` | misleading | "so one day adds an sd of $0.15 \times 0.40 = £0.06$. Its square, 0.0036, is the variance each day adds." Sds do not add from day to day; the part's point is that variances do, and the `neither-squared` slip is the learner who adds £0.06. The line is the second read's own text, applied exactly. | Script FINDING 5. | "The walk part moves by 0.15 times each shock, so one day's move has an sd of $0.15 \times 0.40 = £0.06$. Its square, 0.0036, is the variance each day adds. The true gap gains nothing: it stays at $u_t$."

6. `coint/problems-2.json` | `items[p-smelter-tls]` prose and `parts[3]` | continuity | The new problem's last key is 2.29 and the next problem's part 3 key is −2.29 (`p-lessor-window`, $-0.80/0.35$). Both `explain` lines end the same way since the fix pass: "That is 2.29 sds, beyond +2." and "that is $z = -2.29$, beyond −2." A learner meets the same number as the result of two problems in a row. Set 2 also has three z parts (with `p-three-distributors` part 4), each with a `no-mean` slip; that is the level's standard step and is left. | Script FINDING 6. | Move today's $y$ by 10p. Prose: "$y = £24.60$" → "$y = £24.50$". Part 4: `answer` 2.16; `wrong` `no-mean` 0.21, `variance` 2.725, `no-hedge` 3.15 (tolerances unchanged). `feedback.correct` → "Today's spread is $24.50 - 0.785 \times 31.00 = £0.165$ and its mean $22.00 - 0.785 \times 30.00 = -£1.55$. So $z = 1.715/0.793 = 2.16$." `no-mean` → "0.21 measures today's spread from zero. A z-score measures it from the window's mean, −£1.55." `no-hedge` → "3.15 scores $y$'s own move, $24.50 - 22.00$. The spread nets off $0.785x$ on both days." `explain.text` → "Today the spread stands $0.165 - (-1.55) = £1.715$ above its window mean. That is 2.16 sds, beyond +2." Recomputed: $1.715/0.793 = 2.1627$, 2.1616 from the unrounded sd, 2.1619 from the unrounded ratio; $0.165/0.793 = 0.208$; $1.715/0.629 = 2.727$ and 2.725 from the unrounded variance, so the stored 2.725 takes 2.72 and 2.73 as the present 2.885 takes 2.88 and 2.89; $2.5/0.793 = 3.153$. 2.16 and £24.50 occur nowhere else in set 2. The author's script needs the four values. If the main session prefers to leave the twin, nothing else depends on it.

7. `coint/problems-3.json` | `items[p-glassmaker-borrow].prose` | continuity | The fee has a name in the curriculum: l10 `screens[11]` says "the short leg also pays a stock loan fee (the Markets course's lesson 12)", and Markets l12 teaches it with the same rule. The stem calls it "a fee" and the parts "borrowing fees", so a learner cannot tell it is the thing already met. | Script FINDING 7. | "A share sold short must be borrowed, and the lender charges a fee on the pounds borrowed." → "A share sold short must be borrowed, and the lender charges a fee on the pounds borrowed, the stock loan fee of the Markets course." (24 words; under the gate of 35, voice scan 0 and 0 with it applied.)

## Verified with no finding

- `p-screen-real-share`. $36/1{,}200 = 3\%$; 14.4, 58.2, 72.6 exactly and as the means of 20,000 simulated screens; 19.8% ($14.4/72.6 = 0.19835$), 34.5% ($30.6/88.8 = 0.34459$), 66.8% ($23.4/35.04 = 0.66781$). All 17 `wrong` values rebuilt from their slips (19.4, 80.2, 24.7; 33.8, 42.1, 65.5; 72.4, 28.7, 33.2) and each reaches its own id when typed to 1 decimal place; no band meets a key band. "more than doubles" ($30.6 > 28.8$), "7.2 real passes", "46.56 false ones", "32 to 1" (32.3), "two passes in three" hold. Unit "%" on parts 3 to 5, each asked as a percentage. Part 4's band is 0.001, twice parts 3 and 5: the key lies 0.0095 points from the tie at 34.45, and the validator's `tight-band` rule warns at 0.0005, so the wider band is right. Claims: untied pairs pass a 5% test with chance 0.05 at any sample length (simulated on 504 days: about 5% fall below −3.34 and about 1% below −3.90). The three supposed powers can hold together: a mix of ties, 80% with $\phi = 0.97$ and 20% with 0.99, gives 0.37, 0.81 and 0.60 against the stem's 0.40, 0.85 and 0.65. One $\phi$ alone would put four years nearer 0.93, so "Suppose" is the right word and nothing in the stem says the pairs are alike.
- `p-smelter-tls`. Correlation $4.60/(2.5 \times 2.0) = 0.92$. Eigenvalues 9.8606 and 0.3894 from the SVD of a built window and from the quadratic (10.25, 3.84, 89.7025). Ratio 0.78491, and 0.78478 from the printed 9.86, both 0.785; it minimises the summed perpendicular distance on the window, and lies between 0.736 and 0.870. Spread sd 0.79335 with 0.785 and 0.79333 unrounded, also $\sqrt{0.3894 \times (1 + 0.785^2)}$; 7.222, 3.851, 0.629. Least squares sd 0.7838 is the minimum, and the cost is 0.95p: "under a penny" holds. $z = 2.2888$ from the rounded figures, 2.2878 and 2.2879 unrounded: no tie. Slips: 0.39, 10.25, 7.55; 0.736, 1.274, −1.274; 0.629, 2.802, 3.882; 0.33, 2.88 and 2.89, 3.28. The stored 3.8825 and 2.885 sit on a half step and take the typed 3.882, 2.88 and 2.89 only through the engine's $10^{-9}$; they do, and `grade-all` agrees. "shares of $x$ per share of $y$" is the course's unit for a hedge ratio (l5 `screens[11]`, `topic-2.2` `items[10]`).
- `p-glassmaker-borrow`. £41.40; 21 daily charges of $41.40 \times 0.06/252$ make £0.2070; the short's fee £0.0200; gap £0.187; ratio 10.35, "over ten times"; a short nets £0.98; a grid search over entries puts the long at −2.374, and $2.374 \times 0.50 = £1.187$. Slips: 48, 36, 55.20; 0.143, 0.010, 2.484, 0.017; 0.020, 0.227, −0.033; 2.37, −0.37, −2.19, −1.63. Each reaches its id in the form asked. The key of part 4 is the only option that carries figures; it is a judgement part and the three distractors are real misreadings, so it is left.
- `p-paper-mill-multiple`. $0.15^2 \times 0.40^2 = 0.0036$ exactly and by simulation; slips 0.009, 0.024, 0.06; day 500 sd $\sqrt{2.05} = 1.43$ by simulation; day 209 still follows. No line of the removed AR(1) design is left in the item.
- `p-cocoa-chip-levels`. 13.78, 30.63, 0.7975; $13.78/1.96 = 7.03$; $13.78\sqrt{1{,}498/748} = 19.50$, inside the band. The key option and both lines now say "no evidence of a tie".
- `p-lessor-window`. $0.92^8 = 0.5132$ and $0.92^9 = 0.4722$ straddle a half; $1/0.08 = 12.5$; 8.31; $-0.80/0.35 = -2.29$.
- `p-three-distributors`. $41.7 - 29.80 = 11.9$, $15.49 - 9.8 = 5.69$; rank 1 by walking the rows; $2.35/0.20 = 11.75$.
- `p-tyre-vecm`. −0.09, 0.03; $1/0.09 = 11.11$; 7.35.
- `p-housebuilder-trading-years`. 0.707; 1.53 from $1.08/0.707$ and from $1.08\sqrt 2$; 2.16, 0.76, 2.65. Part 4's band 3.42 to 3.44 takes 3.43, 3.42 (from $1.85^2 = 3.4225$) and 3.4294, and refuses 1.85, 0.29 and 3.70. "that ratio" in part 4 points at part 3's result.

## Engine

- No tool reports one key number, up to sign, in two problems of a set (finding 6: 2.29 and −2.29 in consecutive problems of `coint/problems-2`). `fresh-check --file` could list equal keys within the target file as an advisory.
- `fresh-check --file` now reads the topic exam (advisory against `topic-2.2` `items[9]`), but nothing links a quantity to the name an earlier course teaches it under (finding 7: "borrowing fee" against "stock loan fee" in l10 and Markets l12). A glossary of taught terms would let a checker ask for the taught name.

Both are in `docs/BACKLOG-INBOX.md` under `Raised later (review-delta-af-coint):`.

## Fix pass

1. fixed: `p-glassmaker-borrow` prose, sentence replaced exactly as given.
2. fixed: `p-glassmaker-borrow` part 5 explain, last sentence replaced; $1.00 - 0.207 = 0.793$ recomputed.
3. fixed: `p-screen-real-share` part 5 question replaced exactly.
4. fixed: `p-screen-real-share` part 3 explain, sentence replaced exactly.
5. fixed: `p-paper-mill-multiple` part 1 explain, "one day's move has an sd of" (the rest of the reader's line was already in place).
6. fixed: `p-smelter-tls` y = £24.50; key 2.16 (1.715/0.793 = 2.1627); wrong 0.21 (0.165/0.793 = 0.208), 2.725 (1.715/0.629 = 2.727, unrounded 2.725, band takes 2.72 and 2.73), 3.15 (2.50/0.793 = 3.153); feedback and explain as given. 24.50 and 2.16 appear nowhere else in set 2.
7. fixed: `p-glassmaker-borrow` prose, "the stock loan fee of the Markets course" added.

Numbers script: four smelter values plus the spread, distance and variance-slip checks updated.

Gates: `problems-coint-numbers.py` 826 checks 0 failures; `problems-coint-numbers-read.py` 0 FINDING lines; `delta-review-delta-af-coint-numbers.py` 399 checks, 0 FINDING rows, exit 0; validator 0 errors; voice scan 35 0 and 0; fresh-check 0 hits on each set; grade-all 0 failures on each set; playthrough problems-1 to 3 green with and without `--mobile`.
