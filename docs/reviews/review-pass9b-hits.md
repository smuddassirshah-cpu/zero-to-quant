# Review: triage of the hits of engine pass 9b

Reader of `docs/reports/engine-pass-9b-hits.md` at HEAD 745ce640. The list holds 54 hits and was made before a fix pass landed, so the hits were regenerated first (validator, and `voice-scan.py 35` over every course and the exams). 53 still fire. The one that is gone is the item 1182 hit, `validation/problems-1` `p-rent-seeds` part 2 against part 1's printed working: part 1 now prints $0.81 \times 0.05774$ and takes 0.0467 and 0.0468. No content, engine file or waiver was changed. Every part named was opened. Every number below is asserted in `docs/reviews/review-pass9b-hits-scripts/check.py` (run from the repo root with the venv Python; it reads the content files and exits 0). `dump.py` prints one problem with its bands and lines.

Bands are judged as the engine grades them (`app/js/engine/grade.js`, `within`): a typed value is taken when it is within `tol.abs + 1e-9` of the stored value, and a `%` field divides the typed number by 100. The 1e-9 means a neighbour that sits exactly on a band edge is taken every time, not by float luck.

## Counts

| rule | listed | still fire | faults | stands |
|---|---|---|---|---|
| `[carry-band]` | 13 | 12 | 1 | 11 |
| `[band-edge]` | 10 | 10 | 7 | 3 |
| `[later-key]` | 10 | 10 | 0 | 10 |
| doubled word (voice scan) | 10 | 10 | 0 | 10 |
| `[no-chain]` | 7 | 7 | 0 | 7 |
| `[slip-in-key-band]` | 2 | 2 | 0 | 2 |
| `[shown-arithmetic]` new shapes | 2 | 2 | 2 | 0 |
| all | 54 | 53 | 10 | 43 |

Files needing a fix pass (8): `analysis/problems-3`, `arma/problems-1`, `arma/problems-3`, `garch/problems-1`, `numerics/problems-3`, `ratio/problems-2`, `testing/homework-4`, `fin-ml/l11-deflated-sharpe`.

## Faults

Paths are JSON paths in the named file under `app/content/courses/`. No key changes. Faults 1 to 8 change one number each. After the pass the fixer runs the validator, each touched set's number script, `grade-all.mjs --file` on each touched file, and the playthrough of each touched file with and without `--mobile`. Expected validator change: the eight `[carry-band]` and `[band-edge]` lines of faults 1 to 8 and the two `[shown-arithmetic]` lines of faults 9 and 10 go, plus the `[shown-arithmetic]` line on `fin-ml/l11-deflated-sharpe` `screens[10].hints[1].text` (the same sum); nothing new appears. The narrowed bands should not meet `[tight-band]`, read from the rule's code and not run (this reader edits no content): each key is either stored at too few extra places for the half-unit branch or far from a tie, and every figure the feedback prints stays inside its band. If a line does appear, report it and leave the band at the value given here.

### `[carry-band]`: a slip line that cannot fire for the learner who follows the question

1. `arma/problems-1.json` | `p-gold-drift` part 2 | `items[3].parts[1].widget.wrong[0].tol.abs` (the entry with `id` "no-sqrt", `value` 20.661) | `0.01` becomes `0.025`. The question says "Take the mean of 4.55 bp from part 1". The slip divides by $110/500 = 0.22$: $4.55/0.22 = 20.68$. The stored slip is $4.5455/0.22 = 20.66$, band 20.651 to 20.671, so the learner who does as told types 20.68 and gets the generic line. New band 20.636 to 20.686: takes 20.66 and 20.68, refuses 20.63 and 20.69, and is far from the key 0.92. Not a wrong mark, only a silent slip line.

### `[band-edge]`: narrow the key's band to the key's own rounding

In each case the band takes the next rounding on one side only, and that neighbour has no honest route: it is the key truncated, or one unit up from an exact figure. It is marked right when it is wrong. The new band takes the key's rounding (and the stored key typed in full) and refuses both neighbours. No `wrong` band comes near any of the seven.

2. `ratio/problems-2.json` | `p-fund-six-months` part 4 | `items[3].parts[3].widget.tol.abs` | `0.0001` becomes `5e-05`. Key 2.4699%, asked to 2 places. Today 2.46% is taken (edge 2.4599) and 2.48% refused. $1/0.975896$, $52{,}000/50{,}746.60$ and $0.0241/0.9759$ all give 2.47. New band 2.4649% to 2.4749%.
3. `analysis/problems-3.json` | `p-cube-root-greedy` part 2 | `items[2].parts[1].widget.tol.abs` | `0.0001` becomes `5e-05`. Key $1 - 2^{-1/3} = 0.2062995$, asked to 4 places. Today 0.2062 is taken and 0.2064 refused. Both $1 - 0.7937$ and the unrounded value give 0.2063. New band 0.2062495 to 0.2063495.
4. `analysis/problems-3.json` | `p-cube-root-greedy` part 4 | `items[2].parts[3].widget.tol.abs` | `0.0001` becomes `5e-05`. Key 0.2697002. Today 0.2698 is taken and 0.2696 refused. $-0.4237 + 0.6934$, $-0.4237 + 3^{-1/3}$ and the unrounded sum all give 0.2697. New band 0.2696502 to 0.2697502, which still takes 0.26966 and 0.26974 typed at 5 places.
5. `arma/problems-3.json` | `p-smoothed-fund` part 3 | `items[0].parts[2].widget.tol.abs` | `6e-05` becomes `5e-05`. Key $1.96 \times 0.6 \times 4 = 4.704\%$ exactly, asked to 2 places. Today 4.71% is taken (on the edge) and 4.69% refused. New band 4.699% to 4.709%.
6. `arma/problems-3.json` | `p-inflation-arma` part 3 | `items[1].parts[2].widget.tol.abs` | `6e-05` becomes `5e-05`. Key $0.25 + 0.82 \times 0.222 = 0.43204$ exactly, asked to 4 places. Today 0.4321 is taken (on the edge) and 0.4319 refused. New band 0.43199 to 0.43209.
7. `garch/problems-1.json` | `p-eight-day-window` part 1 | `items[2].parts[0].widget.tol.abs` | `6e-06` becomes `5e-06`. Key $\sqrt{2.7975} = 1.6726\%$, asked to 3 places. Today 1.672% is taken (on the edge) and 1.674% refused. The stem gives the sum of squares exactly, so no carry reaches 1.672; it is the truncation. New band 1.6721% to 1.6731%, which still takes 1.6726.
8. `numerics/problems-3.json` | `p-rate-path-euler` part 3 | `items[2].parts[2].widget.tol.abs` | `6e-06` becomes `5e-06`. Key $0.855710 - 0.003656 = 0.852054$ exactly, asked to 5 places. Today 0.85206 is taken (on the edge) and 0.85204 refused. New band 0.852049 to 0.852059, which still takes 0.852054.

### `[shown-arithmetic]`: a printed sum that does not come to its printed result

9. `testing/homework-4.json` | `h-np-normal` | `items[6].feedback.correct`. The line rounds $c$ to 0.411 and then prints $(0.5 - 0.411)/(1/4)$ as 0.355; it is 0.356. With $c$ unrounded the sum is exact: $(0.5 - 0.41125)/0.25 = 0.355$.
   - old: `$c = \tfrac{1.645}{4} = 0.411$, and power $= \Phi\big(\tfrac{0.5 - 0.411}{1/4}\big) = \Phi(0.355) = 0.6387$.`
   - new: `$c = \tfrac{1.645}{4} = 0.41125$, and power $= \Phi\big(\tfrac{0.5 - 0.41125}{1/4}\big) = \Phi(0.355) = 0.6387$.`
   (In the JSON every backslash is doubled. `explain.text` keeps its 0.411: it goes on with $\Phi(2 - 1.645)$, which is right.)
10. `fin-ml/l11-deflated-sharpe.json` | screen 11, "The fund pitch" | three fields. The table's figures give $(0.1323 - 0.0976)/0.0464 = 0.748$ and $\Phi(0.748) = 0.773$, yet the hint and the accept line print 0.747 and 0.772 (the unrounded values: $E[\max] = 0.097624$, $z = 0.7468$, DSR 0.7724). A learner who checks the hint finds it false. One more place on $E[\max]$ makes the printed sum true: $(0.1323 - 0.09762)/0.0464 = 0.7474$. The string `0.0976` occurs three times in the file, all on this screen; replace each with `0.09762`:
    - `screens[10].canvas.params.rows[1][1]`: `"0.0976"` becomes `"0.09762"`.
    - `screens[10].widget.accept`: `0.772: $\Phi((0.1323 - 0.0976)/0.0464) = \Phi(0.747) = 0.772$.` becomes `0.772: $\Phi((0.1323 - 0.09762)/0.0464) = \Phi(0.747) = 0.772$.`
    - `screens[10].hints[1].text`: `$(0.1323 - 0.0976)/0.0464 = 0.747$.` becomes `$(0.1323 - 0.09762)/0.0464 = 0.747$.`
    The key 0.772 and its band (0.003) stay.

## Stands

### `[carry-band]` (11)

- **The slip does not use the carried figure (6).** `exp-log/problems-3` `p-savings-doubling` part 4, "halfway-pounds" and "midpoint": 10,800 and 7,200 are exact means of whole pounds. `markov/problems-1` `p-carry-pause` part 2, "stay-ratio" ($0.95/1.65$) and "used-stay" ($20/21.43$): neither uses the carried 3.33. `estimation/problems-3` `p-three-month-fund` part 4, "same": two equal SEs divide to exactly 1. `numerics/problems-2` `p-vol-curve-extension` part 5, "peak": the curve is flat at its peak, so 2.7639 for 2.763889 moves the value by $10^{-9}$.
- **The slip worked from the printed carry lands inside its band (5).** `markov/problems-1` `p-thin-book` part 4, "swapped": $6.67/10$ types as 0.6670, inside 0.6662 to 0.6672. `validation/problems-1` `p-rent-seeds` part 2, "worst" and "carried": 0.893 and 0.773 from the printed 0.0468 and 0.0209, and from the unrounded sds. `garch/problems-1` `p-stale-alarm` part 3, "percent": $19.2/0.0027 = 7111.11$ is the stored value. `stat-models/problems-2` `p-two-looks` part 3, "independent": 0.0417 from the printed carries and from the exact ones.

In all eleven the key's own band takes the answer worked from the printed carry.

### `[band-edge]` (3)

- **The neighbour is an honest answer, and the engine's 1e-9 takes the edge every time.** `trig/problems-1` `p-lake-markers` part 3: 47.1 follows from $\sin A \approx 0.733$, and `accept` says "47.1 is also accepted". `vector-calc/problems-2` `p-cycloid-arch` part 4: $\tfrac52 \times 3.142 = 7.855$, typed 7.86. `pdes/problems-2` `p-tent-rod` part 1: $0.1 \times (3.142/2)^2 = 0.2468$.

### `[later-key]` (10)

- **The line fires only for a learner who typed that figure (5).** `counting/problems-1` `p-ice-cream-van` part 1 "ordered" (2184); `proof/problems-2` `p-jobs-servers` part 1 "functions" (1296); `validation/problems-3` `p-fund-flows` part 1 "train" (1.7795); `ensembles/problems-1` `p-opening-gaps` part 2 "other" (0.163); `convex/problems-4` `p-curve-fit-backtrack` part 3 "below-inverse" (0.03125). The printed figure is the `wrong` entry's own value. The learner worked it out; the line only says what it is.
- **The figure is this part's own working (2).** `counting/problems-1` `p-tulip-bed` part 1 "divide-four": 1680 is the ordered count the learner divided by 4, and `feedback.correct` prints it too. `arma/problems-2` `p-etf-flows` part 2 "box-pierce": 0.1936 is $0.44^2$, which $Q(2)$ needs and `feedback.correct` prints.
- **The stem prints it (1).** `numerics/problems-4` `p-grid-node-budget` part 1 `generic`: 276 is the grid's upper end, in the problem's `prose`.
- **A coincidence of two different quantities (2).** `markov/problems-1` `p-carry-pause` part 2 "used-stay": $1/0.7 \approx 1.43$ is a spell length, and part 3's key $10/7$ is a P&L. `topology/problems-3` `p-coin-paths` part 1 "two-days": $2^{-3} = 0.125$ is a distance, and part 2's key is the bound $2 \times 2^{-4}$.

### Doubled word (10)

- **Correct English, the same word in two roles.** "a million million" (4: `exp-log/problems-2`, `number-sense/l14` three times), "Least squares squares the vertical gaps", "The gap between doubles doubles", "How far does the fly fly", "takes closes and returns returns", "as as reliable as", "Returns go in in %". None is a misprint. The last is clumsy but right; an author may prefer "Returns are entered in %".

### `[no-chain]` (7)

Nothing here marks a learner wrongly, and no later part needs a figure it is not given.

- **A real chain the rule cannot read (4).** `equations/problems-1` `p-food-van` and `proof/problems-3` `p-six-nine-lots`: later parts print the earlier expression keys, with spaces ("Using Saturday's $4.2n - 45$", "So $100 = 3(2x + 3y)$"). `ensembles/problems-2` `p-imbalance-stumps` and `ensembles/problems-3` `p-surprise-drift`: later parts restate small whole-number keys ("leaves $-3$ and 3", "Take the start 2 and the leaf values $+6$ and $-6$", "the forecasts 8 and $-4$").
- **The chain is carried in words or in a formula (2).** `proof/problems-1` `p-fund-thresholds`: part 3 opens "B(5) is false", the result of part 2. `ensembles/problems-2` `p-ipo-forest`: part 4 restates the two variance formulas whose values at $B = 50$ are parts 2 and 3. Its part 1 (0.3) feeds nothing.
- **Not a chain, left to the course author (1).** `topology/problems-2` `p-right-rays`: four separate questions on one topology. Each restates the fact it needs, so no learner is stuck, but no part uses an earlier answer. The set's lede promises that each step feeds the next. This needs a rewritten problem, not a fix pass.

### `[slip-in-key-band]` (2)

- **The slip is not rounding, and the unrounded value is refused and gets its line.** `number-sense/problems-2` `p-golf-card` part 3 (key 0.278, slip 0.277778) and `p-taxi-split` part 2 (key 2.83, slip 2.8333). Typed 0.2778, 0.27778, 2.833 or 2.8333 all miss the key's band and land in the slip's. A learner who rounds as asked has not made the slip.

## Rule verdicts

- **`[carry-band]`: 1 of 12, keep as a warning and make it exact.** No hit is a wrong mark; the one fault is a silent slip line. The rule cannot tell whether a slip uses the carry, and half the stands do not. Two changes: (a) skip a slip whose value is a whole number whatever its band (three stands); (b) where the entry has a `slip` expression (item 1029), evaluate it with the printed carry and with the stored key and report only when either result misses the band; with no `slip` expression, stay silent. The item 1182 branch (the carried figure against the earlier part's printed working) found a true fault and should stay as it is.
- **`[band-edge]`: 7 of 10, keep.** The best yield of today's rules. One refinement: stay silent when the part's `accept` names the neighbour ("47.1 is also accepted"). The message should drop "by a float margin": the engine adds 1e-9, so the neighbour is always taken. The question for the author is whether it should be.
- **`[later-key]`: 0 of 10, tighten hard.** Stay silent when (a) the printed figure is the `wrong` entry's own value, (b) the item's `prose` or canvas prints it, (c) the same part's `feedback.correct` prints it, (d) the match is at fewer than four significant digits or only after rounding ("1.43" against 1.4286). That leaves no hit today and still catches the case the rule was built for: a line that tells the learner to use a later answer shown nowhere else.
- **Doubled word: 0 of 10, keep with a waiver list.** The check is cheap and a real "the the" is a fault. Add "million" to `DOUBLE_OK` and waive the other six by file, path and word, so the count returns to 0 and the next misprint shows.
- **`[no-chain]`: 0 learner faults of 7, 1 true non-chain, tighten.** (a) Compare expression keys with spaces and LaTeX spacing removed. (b) Count a whole-number key as restated when a later question prints it after a cue ("Take", "Using", "the start", "leaves", "forecasts", "left by"). (c) Count "is false" or "is true" after a claim named in the earlier part. That removes five of the seven and keeps `p-right-rays`.
- **`[slip-in-key-band]`: 0 of 2, tighten.** Stay silent when the key is stored at exactly the asked places and equals the slip's value rounded to them: the entry is the key unrounded, and it is refused. Keep the rule for a slip from a different working that rounds onto the key.
- **`[shown-arithmetic]` new shapes: 2 of 2, keep.**

## For the fixer to know

- Faults 2 to 8 make each band exactly half a step. The number scripts read the content files; if one asserts an old band, change the script's constant, not the band.
- `p-right-rays` and the idle part 1 of `p-ipo-forest` are an author's call and are not in the fault list.
