# Review: triage of the hits of engine pass 9

Reader of `docs/reports/engine-pass-9-hits.md` at HEAD 74f4f090: 105 validator warnings on problem sets, 3 voice-scan hits and one mobile overflow. No content, engine file or waiver was changed. Every part named in the list was opened. Every number was recomputed in `docs/reviews/review-pass9-hits-scripts/check.py` (run from the repo root with the venv Python; it asserts every figure below and exits 0). `slip_bands.py` is the mechanical band check of the 63 slips, `compact.py` and `dump.py` print the parts, `voice_mobile.py` prints the voice and overflow passages. The overflow was read from a 440 px screenshot of the unchanged set (`playthrough.mjs --problems measure-prob/problems-2 --mobile --shots`).

## Counts

| rule | hits | faults | stands |
|---|---|---|---|
| `[rounding-tie]` slip past places | 63 | 0 | 63 |
| `[rounding-tie]` key near a tie | 9 | 4 | 5 |
| `[working-band]` span re-evaluated | 4 | 1 | 3 |
| `[key-in-question]` | 29 | 2 | 27 |
| voice scan, lesson id in a code span | 3 | 3 | 0 |
| mobile text overflow (one item, two parts) | 1 | 1 | 0 |
| all | 109 | 11 | 98 |

One listed `[key-in-question]` hit does not reproduce: the validator at HEAD gives 28, and `pdes/problems-3` `p-grid-budget` part 1 is not among them (stands 27 includes it).

Files needing a fix pass (10, eight problem sets and two written sets): `coding-int/homework-2`, `coding-int/review-2`, `convex/problems-3`, `exp-log/problems-3`, `ito/problems-2`, `limits-thm/problems-2`, `markov/problems-3`, `measure-prob/problems-2`, `validation/problems-1`, `validation/problems-3`.

## Faults

Paths are JSON paths in the named file under `app/content/courses/`. No key changes. After the pass the fixer runs the validator, each touched set's number script, `grade-all.mjs --file` on each touched file, and the playthrough of each touched file with and without `--mobile`.

### `[rounding-tie]`, key near a tie: widen the key's band

In each case a learner who carries an intermediate value at the precision of the answer lands on the other side of the tie and is refused. The new band takes both neighbours of the tie and nothing else.

1. `convex/problems-3.json` | `p-style-fit` part 5 | `items[1].parts[4].widget.tol.abs` | `5e-06` becomes `6e-06`. The key is $\sqrt{11/12} = 0.957427$ per cent, asked to 3 places, a tie at 0.9575. A learner who carries $11/12 \approx 0.917$ (the figure the `no-root` line itself prints) gets $\sqrt{0.917} = 0.95760$ and types 0.958, refused. New band, as typed: 0.956827 to 0.958027. It takes 0.957 and 0.958 and refuses 0.956 and 0.959. The `wrong` values (3.317, 0.917, 2.236) are far off.
2. `exp-log/problems-3.json` | `p-log-chart-line` part 1 | `items[2].parts[0].widget.tol.abs` | `5e-05` becomes `6e-05`. The key is $\ln 9/8 = 27.4653\%$, asked to 2 places. The part's own `explain.text` prints $2.1972/8$, which is 27.465 exactly, a tie. With $\ln 9 \approx 2.197$ a learner gets 27.4625 and types 27.46, refused by 0.0003. New band, as typed: 27.4593 to 27.4713. It takes 27.46 and 27.47 and refuses 27.45 and 27.48. No text changes; `accept` stays "27.47%".
3. `ito/problems-2.json` | `p-cable-inverse` part 3 | `items[0].parts[2].widget.tol.abs` | `5e-05` becomes `6e-05`. The key is $e^{0.0432} = 1.044147$, asked to 4 places. A learner who multiplies the two means to 4 places, $1.3273 \times 0.7867 = 1.04419$, types 1.0442, refused. That working uses part 2's own keyed answer, 0.7867. New band: 1.044087 to 1.044207. It takes 1.0441 and 1.0442 and refuses 1.0440 and 1.0443; `median-y` (1.0218) and `one` (1) are far off.
4. `validation/problems-3.json` | `p-carry-lookbacks` part 1 | `items[3].parts[0].widget.tol.abs` | `5e-05` becomes `6e-05`. The key is $1/\sqrt 6 = 0.408248$, asked to 4 places. With $\sqrt 6 \approx 2.449$ a learner gets 0.408330 and types 0.4083, refused; 2.4495 and 2.45 both give 0.4082. New band: 0.408188 to 0.408308. It takes 0.4082 and 0.4083 and refuses 0.4081 and 0.4084.

### `[working-band]`

5. `validation/problems-1.json` | `p-rent-seeds` part 1 | three fields. The printed working, $0.81 \times 0.0577$, comes to 0.046737, which rounds to 0.0467; the key is $0.81\sqrt{2/600} = 0.046765$, band 0.046715 to 0.046815, so 0.0467 is refused. The feedback also prints $0.81 \times 0.0577 \approx 0.0468$, which is not true of those figures.
   - `items[3].parts[0].widget.tol.abs`: `5e-05` becomes `7e-05`. New band 0.046695 to 0.046835: takes 0.0467 and 0.0468, refuses 0.0466 and 0.0469. The `wrong` values (0.0209, 0.052, 0.0331) are far off.
   - `items[3].parts[0].feedback.correct`: old `$0.81\sqrt{2/600} = 0.81 \times 0.0577 \approx 0.0468$.` new `$0.81\sqrt{2/600} = 0.81 \times 0.05774 \approx 0.0468$.` ($\sqrt{2/600} = 0.057735$; $0.81 \times 0.05774 = 0.046769$.)
   - `items[3].parts[0].explain.text`: old first sentence `$\sqrt{2/600} = 0.0577$, so one split's test MSE has sd about 0.0468 around 0.81.` new `$\sqrt{2/600} = 0.05774$, so one split's test MSE has sd about 0.0468 around 0.81.` The second sentence is unchanged.
   Part 2 already carries "the sd 0.0468 from part 1", so nothing downstream moves.

### `[key-in-question]`

6. `limits-thm/problems-2.json` | `p-digital-share` part 3 | the only table value the question gives is the key, 0.5596. Offer a second value so that the learner has to find $z$, and name the slip it belongs to. Recomputed: $\ln(84.95/80) = 0.0600$, $z = (0.06 - 0.015)/0.3 = 0.15$, $\Phi(0.15) = 0.5596$, $\Phi(0.2) = 0.5793$.
   - `items[1].parts[2].question`: old `Use $\Phi(0.15) = 0.5596$. Give a decimal to 4 places.` new `You are told $\Phi(0.15) = 0.5596$ and $\Phi(0.2) = 0.5793$. Give a decimal to 4 places.` The text before it is unchanged.
   - `items[1].parts[2].widget.wrong`: append `{"id": "no-centre", "value": 0.5793, "tol": {"abs": 0.0001}}`.
   - `items[1].parts[2].feedback.byKey`: add `"no-centre": "That is $\\Phi(0.06/0.3)$, which leaves out the centre of the log price. Take off the log drift 0.015 first: $z = 0.045/0.3 = 0.15$."`
   The rule will still report the part after this (0.5596 is still printed); it then stands as a choice between two table values, like `p-fertiliser-trials`.
7. `markov/problems-3.json` | `p-barrier-note` part 2 | the question tells the learner to use "the 495 from part 1", and 495 is the answer: nothing is done to it. The reflection step, that the mirror of $-2$ in $-3$ is $-4$, is the whole part. $\binom{12}{4} = 495$, and the part can be done without part 1.
   - `items[1].parts[1].question`: old `How many of the paths that end at $-2$ touch $-3$ on the way? Use reflection and the 495 from part 1. Give a whole number.` new `How many of the paths that end at $-2$ touch $-3$ on the way? Use reflection in the level $-3$. Give a whole number.`
   - `items[1].parts[1].widget.placeholder`: `decimal` becomes `a whole number` (the answer is a count).

### Voice scan: a lesson named by its title

8. `coding-int/homework-2.json` | `items[3].widget.prompt` | old ``Explain how you read the statement of `l8-simulating-the-rules`.`` new `Explain how you read the statement of the lesson "Simulating the rules".`
9. `coding-int/homework-2.json` | `items[6].prose` | old ``Events, in the format of `l10-matching-engine`:`` new `Events, in the format of the lesson "A matching engine":`
10. `coding-int/review-2.json` | `items[6].prose` | old ``The bot of `l8-simulating-the-rules`:`` new `The bot of the lesson "Simulating the rules":`

The titles are those of `l8-simulating-the-rules.json` and `l10-matching-engine.json`. In the JSON the quotation marks are written `\"`.

### Mobile overflow

11. `measure-prob/problems-2.json` | `p-boom-bust` part 4 | `items[2].parts[3].question`. The screenshot shows one inline span, about 465 px wide in a 400 px column, that does not wrap: inline maths never breaks inside a span in this app. Part 5 fails only because part 4 stays on the page above it, so one change settles both. Split the span at the inequality; the two halves measure about 296 px and 170 px and wrap between them. The mathematics is unchanged.
    - old `The union bound with part 2's inequality gives $P(M_n > 0.01 \text{ for some } n \ge 200) \le \sum_{n \ge 200} 0.9^{n/2}/\sqrt{0.01}$. Find this bound. Give 5 decimal places.`
    - new `The union bound with part 2's inequality gives $P(M_n > 0.01 \text{ for some } n \ge 200)$ $\le \sum_{n \ge 200} 0.9^{n/2}/\sqrt{0.01}$. Find this bound. Give 5 decimal places.`
    - If the fixer's mobile playthrough of the set still fails, use this wording, whose longest span is the summand: `Apply part 2's inequality with $\varepsilon = 0.01$ on each day from 200 on, and add the bounds as the union bound allows. The chance that $M_n > 0.01$ on some day $n \ge 200$ is then at most the sum of $0.9^{n/2}/\sqrt{0.01}$ over $n \ge 200$. Find this bound. Give 5 decimal places.`
    I could not play either wording, since that needs the content changed. The widths are read from the screenshot.

## Stands

### `[rounding-tie]`, slip past places: all 63

One reason covers all of them. A value stored one place past the asked places, whose last digit is not 5, lies within half a step of its nearer rounding. So a band of half a step always takes what a learner who makes the slip types. `check.py` part A recomputes each slip from the part's own figures, rounds it as asked, and finds that both the rounded and the unrounded slip land on the slip's own line, never on the key or another line. Each feedback line was read against its recomputed slip and names it correctly. The other rounding, which the rule warns about, is reached only by truncating; it gets the generic line and is never marked right.

Each line: set, item, part, `wrong` id, the recomputed slip, the value typed at the asked places (in the stored unit: a percentage of 43.1 shows as 0.431).

- `arma/problems-2` `p-trust-discount` 2 `constant`: slip 1.38, typed 1.4
- `coint/problems-2` `p-smelter-tls` 3 `variance`: slip 0.629406, typed 0.629
- `coint/problems-3` `p-glassmaker-borrow` 2 `y-rate`: slip 0.01725, typed 0.017
- `coint/problems-3` `p-glassmaker-borrow` 5 `sign`: slip 2.374, typed 2.37
- `coint/problems-3` `p-glassmaker-borrow` 5 `shift-only`: slip -0.374, typed -0.37
- `coint/problems-3` `p-glassmaker-borrow` 5 `pounds`: slip -2.187, typed -2.19
- `coint/problems-3` `p-glassmaker-borrow` 5 `wrong-way`: slip -1.626, typed -1.63
- `conditional/problems-3` `p-three-loans` 4 `reciprocal`: slip 0.180636, typed 0.181
- `conditional/problems-5` `p-doubling-desk` 3 `unweighted`: slip -10.598, typed -10.6
- `convex/problems-4` `p-variance-log` 1 `ratio`: slip 0.765625, typed 0.766
- `convex/problems-4` `p-variance-log` 1 `one-minus`: slip 0.234375, typed 0.234
- `counting/problems-2` `p-balloon-blocks` 5 `carried`: slip 0.428571, typed 0.429
- `counting/problems-2` `p-balloon-blocks` 5 `os-only`: slip 0.714286, typed 0.714
- `counting/problems-2` `p-quiz-team` 5 `girl-only`: slip 0.984848, typed 0.985
- `counting/problems-2` `p-quiz-team` 5 `bottom`: slip 0.953846, typed 0.954
- `counting/problems-2` `p-quiz-team` 5 `carried`: slip 0.924242, typed 0.924
- `counting/problems-2` `p-signal-flags` 4 `together`: slip 0.285714, typed 0.286
- `counting/problems-2` `p-signal-flags` 4 `carried`: slip 0.428571, typed 0.429
- `counting/problems-3` `p-sail-ring` 5 `third`: slip 0.333333, typed 0.333
- `eigen/problems-1` `p-garden-path` 4 `sign`: slip 35019.8, typed 35020
- `eigen/problems-3` `p-site-anomalies` 1 `unsquared`: slip 1.8, typed 2
- `equations/problems-2` `p-interest-split` 3 `rhs`: slip 31173.6, typed 31174
- `estimation/problems-1` `p-reference-mass` 5 `carried-72`: slip 0.527046, typed 0.53
- `estimation/problems-1` `p-reference-mass` 5 `no-root`: slip 0.131579, typed 0.13
- `estimation/problems-2` `p-tank-sensor` 4 `sd-not-squared`: slip 53.146, typed 53.15
- `estimation/problems-3` `p-email-clicks` 3 `ninety`: slip 0.135325, typed 0.135
- `estimation/problems-3` `p-email-clicks` 3 `upper`: slip 0.1894, typed 0.189
- `estimation/problems-3` `p-routing-test` 3 `added-se`: slip -0.474, typed -0.47
- `exp-log/problems-1` `p-rare-coin` 4 `mid-value`: slip 2768.3, typed 2768
- `functions/problems-1` `p-sapling-log` 4 `no-c`: slip 14.4, typed 14
- `ito/problems-4` `p-band-wait` 3 `squared-level`: slip 1.6, typed 2
- `least-squares/problems-2` `p-power-line` 4 `total`: slip 6.7082, typed 6.71
- `least-squares/problems-3` `p-gas-hubs` 5 `ratio`: slip 0.666667, typed 0.667
- `limits/problems-5` `p-camera-pan` 3 `half-sweep`: slip 0.261799, typed 0.262
- `limits/problems-5` `p-camera-pan` 3 `per-metre`: slip 0.0261799, typed 0.026
- `markov/problems-3` `p-stake-size` 4 `hundreds`: slip -97.4, typed -97.4
- `markov/problems-5` `p-cash-machine` 4 `four-hours`: slip 376.298, typed 376
- `measure-prob/problems-1` `p-no-double-four` 2 `square`: slip 0.962361, typed 0.962
- `measure-prob/problems-2` `p-boom-bust` 4 `one-day`: slip 0.000265614, typed 0.00027
- `measure-prob/problems-2` `p-boom-bust` 4 `no-root`: slip 0.000517598, typed 0.00052
- `measure-prob/problems-2` `p-compounding` 3 `no-phi`: slip 2.2663, typed 2.266
- `measure-prob/problems-4` `p-premium-weight` 5 `cash-once`: slip -4.544, typed -4.54
- `pdes/problems-1` `p-two-level-bar` 2 `no-base`: slip 53.826, typed 53.8
- `pdes/problems-2` `p-grid-modes` 4 `absolute`: slip 0.0032, typed 0.003
- `ratio/problems-1` `p-pension-split` 5 `old-total`: slip 0.43125, typed 0.431
- `ratio/problems-1` `p-pension-split` 5 `bonds-base`: slip 0.71875, typed 0.719
- `regression/problems-2` `p-freight-summary` 3 `carried`: slip 0.262346, typed 0.262
- `regression/problems-2` `p-sunny-cones` 3 `carried-n`: slip 1.69731, typed 1.7
- `regression/problems-3` `p-overlap-signal` 3 `no-root`: slip 58.3333, typed 58.3
- `stat-models/problems-3` `p-spread-day-tail` 4 `classic-normal`: slip 1.02913, typed 1
- `stat-models/problems-4` `p-quality-six-markets` 1 `divisor-5`: slip 0.552, typed 0.55
- `stat-models/problems-4` `p-quality-six-markets` 2 `from-divisor-5`: slip 0.302, typed 0.3
- `testing/problems-3` `p-checkout-designs` 2 `thousands`: slip 3.6, typed 4
- `testing/problems-4` `p-website-signups` 3 `sd`: slip 0.612372, typed 0.612
- `validation/problems-1` `p-rent-seeds` 2 `worst`: slip 0.892649, typed 0.893
- `validation/problems-1` `p-rent-seeds` 3 `by-best`: slip 0.114168, typed 0.114
- `validation/problems-1` `p-van-prices` 2 `ddof-one`: slip 0.166283, typed 0.166
- `validation/problems-2` `p-spread-blocks` 4 `by-purged`: slip 0.166667, typed 0.167
- `validation/problems-3` `p-closed-funds` 2 `survivors`: slip 0.933333, typed 0.933
- `validation/problems-3` `p-closed-funds` 2 `added`: slip 1.21333, typed 1.213
- `validation/problems-3` `p-closed-funds` 2 `whole-gap`: slip -0.622222, typed -0.622
- `validation/problems-3` `p-closed-funds` 3 `note`: slip 0.438439, typed 0.438
- `vectors/problems-1` `p-drone-crosswind` 2 `swapped`: slip -5.8, typed -6

Three notes, none a fault. `functions/problems-1` `no-c`: a learner who divides 72 by 5 and answers "week 15" gets the generic line. `pdes/problems-2` `absolute`: a learner who types the raw gap 0.0032 in the percentage box gets the generic line; 0.3 and 0.32 land on the slip's line. `markov/problems-3` `hundreds` is stored from the unrounded chance ($-97.36$); the carried 0.5026 gives $-97.4$, inside its band.

### `[rounding-tie]`, key near a tie: 5

- The givens are exact and the answer is one quotient of them, so no rounded intermediate exists: `number-sense/problems-4` `p-cycle-commute` part 5 ($20{,}000/3{,}600 = 5.5556$, typed 5.56); `random-vars/problems-2` `p-reversal-days` part 5 ($45.6/9.88 = 4.6154$, typed 4.62).
- The carried and the printed figures all land on the keyed rounding: `markov/problems-4` `p-taxi-rank` part 4 ($96 \times 8/65 = 11.8154$; with part 3's 0.1231 it is 11.8176; both 11.82); `markov/problems-5` `p-two-loss-cut` part 2 ($130/9 = 14.4444$; $11.11 + 3.33$ and $11.111 + 3.333$ both give 14.44); `markov/problems-5` `p-signal-trial` part 5 (key $-1219.51$, band 0.5; the question's own $-200 \times 6.10$ and the two-ends working both give $-1220$, inside by 0.01).

### `[working-band]`: 3

- The printed figure is rounded up to a whole number on purpose, and the feedback prints the key straight after it: `coint/problems-1` `p-cable-sample-length` part 4 (1,104.4, "first reach", so 1,105); `numerics/problems-4` `p-grid-node-budget` part 2 (321.39, "smallest whole $N$", so 322; 321 has its own line); `validation/problems-1` `p-rent-seeds` part 4 (3,898.4, "bring it under", so 3,899).

### `[key-in-question]`: 27

- A given of one or two digits that equals the key by coincidence, in another role (19): `algebra/problems-3` `p-affine-five` 1 (the 2 of $h(x) = 2x$); `algebra/problems-4` `p-sixteen-factorial` 3 (the 16 of $16!$); `analysis/problems-4` `p-quartic-roots` 5 ($h(0) = 3$); `functions/problems-2` `p-path-and-pipe` 5 (the gradient 4); `integrals/problems-1` `p-falling-parabola` 5 (the 16 of $R_n$; taking the limit is the task); `integrals/problems-2` `p-turnover-decay` 2 (the coefficient $-16$); `limits/problems-1` `p-fit-the-constants` 1 (the limit 2; $a$ equals it only because the bottom's leading coefficient is 1); `limits/problems-2` `p-inventory-penalty` 3 (the carried left slope; the part tests that a line's slope is $m$); `linear-maps/problems-1` `p-hedge-baskets` 2 ($w_1 = 2w_4$); `linear-maps/problems-2` `p-curve-report` 3 ($4 - 2 = 2$); `multivar/problems-5` `p-dome-tent` 1 ($x = 2u$); `proof/problems-2` `p-rule-and-domain` 1 ($c(a - b) = 0$); `proof/problems-3` `p-two-odd-squares` 4 ($m = 4$); `quadratics/problems-4` `p-windy-ride` 3 (a choice between the two roots); `taylor/problems-3` `p-big-gain` 1 ($x = 1.8$; the ratio tends to it); `testing/problems-2` `p-running-shoes` 3 ($\bar d = -4$ and $s_d/\sqrt n = 1$); `vectors/problems-3` `p-engraver-dial` 3 ($2 - k$); `vectors/problems-3` `p-paint-tints` 4 ($p = 3$); `functions/problems-3` `p-two-cultures` 4 (a choice between the trial values 3.3 and 3.4, which needs the two evaluations).
- The sign differs, so the printed figure is not the key (1): `integrals/problems-1` `p-subscriptions` 4 (the question prints 10, the key is $-10$).
- A choice among two or three printed table values (3): `stat-models/problems-4` `p-quality-six-markets` 5; `testing/problems-2` `p-fertiliser-trials` 2 and 4.
- A choice between two carried values (1): `analysis/problems-2` `p-sum-law-band` 4 ($\max(423, 200)$).
- The carried value is an input to the working and the lesson is that it comes back unchanged (2): `conditional/problems-4` `p-dark-fills` 2 (Bayes with equal likelihoods returns the prior 0.6667); `limits-thm/problems-1` `p-fund-record` 3 ($0.65^{12}/0.0754$, no memory).
- Not reproduced at HEAD (1): `pdes/problems-3` `p-grid-budget` 1 (the key is 22.29 and the question prints no such figure).

## Rule verdicts

- **`[rounding-tie]` slip past places: 0 of 63, withdraw it.** With one extra stored digit that is not 5, the nearer rounding is always inside a half-step band, so the rule cannot find a fault; a last digit of 5 is the exact tie the older rule already reports. Nothing of it is worth keeping. The useful check on slips is the one not built (item 1175): recompute nothing, but report a `wrong` whose rounding at the asked places falls outside its own band or inside another band. `slip_bands.py` is that check; it is silent on all 63.
- **`[rounding-tie]` key near a tie: 4 of 9, keep as it is.** Nine hits is a fair cost and nearly half are faults. One refinement would remove two of the five that stand: stay silent when the question prints two exact figures whose quotient or product is the key (`p-cycle-commute`, `p-reversal-days`).
- **`[working-band]` span re-evaluated: 1 of 4, keep and tighten.** Stay silent when the band is 0, the key is a whole number, the key is the printed result rounded up or down, and the same feedback prints the key after the span. That removes the three ceilings and keeps `p-rent-seeds`.
- **`[key-in-question]`: 2 of 29, tighten.** Three changes leave 5 hits with both faults among them. (a) Read keys of three or more significant digits only; all 21 one- and two-digit hits stand, and the "after `=`" path found no fault. (b) Compare with the sign, so that a printed 10 does not match a key of $-10$. (c) Stay silent when the question prints two or more values of the key's form after `\Phi(...) =`, since that is a choice. What stays: 423, 0.6667, 0.0754, 0.5596 and 495. The `pdes/problems-3` line of the hit list should be traced, since the validator at HEAD does not give it.
- **Voice scan, lesson id in a code span: 3 of 3, keep.**
- **Mobile text overflow: 1 of 1, keep.** The failure message names the stem paragraph (`p.t-prose "A strategy's capital..."`), not the span that is too wide; naming the widest maths span would save the author the screenshot. The long-maths validator warning that was not built would catch this without a browser: an inline span as long as this one (about 465 px at the question's size) cannot fit a 400 px column.

## What a fixer cannot settle

- Fix 11 is unplayed. The fixer must run the mobile playthrough of `measure-prob/problems-2` and fall back to the second wording if the first fails.
- Fix 6 adds a `wrong` value and a feedback line; the set's number script may list the part's figures and need the new 0.5793.

## Fix pass

Fixer on Sonnet. Every figure was already recomputed in `check.py`; no dispute. No key changed. Validator 0 errors; voice scan 0 and 0 on the nine courses; number scripts pass (`docs/reports/problems-limits-thm-numbers.py` updated for fix 6); `grade-all.mjs --file` 0 failures on every edited file.

1. `convex/problems-3` `p-style-fit` part 5: applied as written (`tol.abs` 6e-06).
2. `exp-log/problems-3` `p-log-chart-line` part 1: applied as written (`tol.abs` 6e-05).
3. `ito/problems-2` `p-cable-inverse` part 3: applied as written (`tol.abs` 6e-05).
4. `validation/problems-3` `p-carry-lookbacks` part 1: applied as written (`tol.abs` 6e-05).
5. `validation/problems-1` `p-rent-seeds` part 1: applied as written (band 7e-05, 0.05774 in the `correct` line and the explanation).
6. `limits-thm/problems-2` `p-digital-share` part 3: applied as written (question, `no-centre` wrong value 0.5793, `byKey` line). The number script's slip list gained `no-centre`; it did not need a new printed value.
7. `markov/problems-3` `p-barrier-note` part 2: applied as written (question wording, placeholder "a whole number").
8. `coding-int/homework-2` `items[3].widget.prompt`: applied as written.
9. `coding-int/homework-2` `items[6].prose`: applied as written.
10. `coding-int/review-2` `items[6].prose`: applied as written.
11. `measure-prob/problems-2` `p-boom-bust` part 4: applied with the first wording (span split at the inequality); the mobile playthrough passes, so the fallback was not needed.

Engine item 1024: `"form": "simplified"` added to `analysis/problems-1` `items[1].parts[1]` and `analysis/problems-2` `items[0].parts[0]`. grade-all: stored answers and accepts still pass (0 failures). A temporary `wrong` entry holding the question's own text, `5 - \frac{5n - 4}{n + 1}`, is refused with key `form` (the file was restored afterwards).
