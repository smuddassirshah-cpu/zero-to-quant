# Review: triage of the hits of engine pass 8 on the 149 problem sets

Reader of `docs/reports/engine-pass-8-hits.md` (list A, 21 validator hits) and of the warnings of `cd app && node tools/same-course-reuse.mjs --all --pairs` (list B). No content, engine file or waiver was changed, and no browser was used. Every band of list A was recomputed and tested against the printed value, its roundings and the other `wrong` values of its part (`triage-8/assemble.py` in the scratch folder, 12 bands, all pass). For list B the pairs of every hit were read; for every exam hit, every `reuse` verdict and every hit with more than a slip line, both items were read in full.

## Counts

List A, 21 hits: `fix` 19, `stands` 2.

| rule | hits | fix | stands |
|---|---|---|---|
| `[working-band]` | 2 | 1 | 1 |
| `[rounding-tie]` | 2 | 1 | 1 |
| `[table-source]` | 6 | 6 | 0 |
| `[wide-wrong-tol]` | 10 | 10 | 0 |
| `[escaped-apostrophe]` | 1 | 1 | 0 |

List B, regenerated at HEAD 348e7df5: 189 warnings (188 `retold`, 1 `text`), 28 waived, 0 errors. The filed list had 188. Two exam hits are gone, since their exam items changed this session (`regression/problems-2` `p-grocer-beta` against `topic-1.6` `items[8]`, `stat-learning/problems-3` `p-order-fill` against `topic-2.1` `items[20]`). Three are new, all on the line "You multiplied matching entries." against the new `topic-1.4` item `a-undo-two-steps` (`vectors/problems-2` `p-site-plan`, `vectors/problems-3` `p-colour-sensor` and `p-engraver-dial`). Exam sources: 13 (12 before).

| verdict | `[slip-line]` course source | `[exam-reuse]` | all |
|---|---|---|---|
| `stands` | 171 | 11 | 182 |
| `reuse` | 5 | 2 | 7 |
| all | 176 | 13 | 189 |

The 182 `stands` by class: a stock slip line with no number or story 80; a slip named in stock words with the part's own numbers 69; the carry line's fixed form 10; ruled singly with a reason 12; exam source 11.

The 7 `reuse` hits lie in six parts of six sets: `limits/problems-3` (`p-relative-strength` part 2), `stat-learning/problems-2` (`p-rent-ridge` part 2), `stat-learning/problems-3` (`p-price-spikes` part 2, two hits, one line), `stat-learning/problems-4` (`p-order-sizes` part 3), `testing/problems-3` (`p-fund-managers` parts 1 and 2, a renumber) and `testing/problems-4` (`p-bakery-loaves` part 2). Five are rewordings of feedback lines with no key touched; `p-fund-managers` changes two `wrong` values and the stem.

Sets needing a fix pass, lists A and B together (17): `arma/problems-3`, `coint/problems-1`, `elimination/problems-1`, `estimation/problems-3`, `fin-ml/problems-3`, `garch/problems-1`, `garch/problems-2`, `garch/problems-3`, `limits/problems-3`, `numerics/problems-1`, `stat-learning/problems-2`, `stat-learning/problems-3`, `stat-learning/problems-4`, `testing/problems-3`, `testing/problems-4`, `trig/problems-1`, `trig/problems-2`. `stat-learning/problems-1` (list A, `stands`) needs nothing.

## Verdicts

- List A `fix`: the exact text or band follows; every key is unchanged. `stands`: the reason, and an engine bullet where the rule misfires.
- List B `stands`: a line a learner would not know as a repeat. It is waived in the block at the end. `reuse`: the exact replacement, checked against the course and its exams for a new collision (no line of the replacements stands in either).
- Rule for list B, in the spirit of the rulings of sessions AC to AF. A slip line stands when it names the slip in the plain words anyone would use, with no number or with the part's own numbers. It is reuse when the whole feedback of a slip, every sentence, is a source's feedback word for word; when it carries a source's numbers; or when an exam item is the same step with a shared parameter. The item-level freshness of these sets was read before (`review-reuse-af-hits.md`, the delta reads); this triage rules on the lines.

## List A: validator hits

1. coint/problems-1.json | `items[2].parts[3].explain.text` (`p-cable-sample-length`) | [working-band] | fix | the working stops at $n = 1{,}104.4$ and never states the key 1,105; a learner who copies the last figure types 1104 and is refused (band 0). Recomputed twice: $(3.34\sqrt{0.0396}/0.02)^2 = 1{,}104.40$, and 1,104.43 with the rounded 0.1990; the first whole day is 1,105 | second sentence becomes: "That reaches −3.34 at $n = 1{,}104.4$, so $n = 1{,}105$ days, over four years of daily closes." Key, band 0 and the `wrong` values 1094, 2187 and 558 are unchanged; none is 1105
2. stat-learning/problems-1.json | `items[3].parts[3].explain.text` (`p-heat-demand`) | [working-band] | stands | the working prints the key first ("Degree 2 falls from 1.80 to 1.476") and then the floor, $1.20 + 0.24 = 1.44$, which is the limit as the days grow and not the answer. `feedback.correct` ends on 1.476. Recomputed: $1.20 + 0.24 + 0.36/10 = 1.476$ | false hit: the rule reads the last figure only (engine bullet 3)
3. trig/problems-1.json | `items[1].parts[3].widget.wrong[2]` (`p-hexagon-tile`, `half`) | [rounding-tie] | stands | 0.5 is $\sin CAD$ typed as it stands, not an angle rounded to a whole degree. Its roundings are 1, which `radians-whole` (value 1, band 0) already takes with a line that fits, and 0, which nobody types for an angle. The band the rule asks for, $\pm 0.5$, would swallow `radians` (0.5236) and `radians-whole` | keep $\pm 0.0005$ (engine bullet 4)
4. trig/problems-1.json | `items[3].parts[2].widget.wrong[2]` (`p-desk-lamp`, `ratio-tan`) | [rounding-tie] | fix | the question asks for 1 decimal place, so a learner who stops at $\tan AOB = 0.75$ types 0.8 (or 0.7) and gets the generic line | `tol.abs` 0.0005 to 0.051 (0.05 fails on 0.8 in floating point). The band $[0.699, 0.801]$ takes 0.7, 0.75 and 0.8 and refuses `ratio-sin` 0.6, `radians` 0.6435 (its band ends at 0.6485), the key 36.87 and the two angles 53.13 and 48.59. As 0.8 is also $\cos AOB$, the line becomes: "You gave a ratio, not the angle: $\tan AOB = 0.75$. Use the inverse tangent: $\tan^{-1} 0.75 \approx 36.9^\circ$."
5. arma/problems-3.json | `items[2].parts[2].question` (`p-swap-spread-hold`) | [table-source] | fix | the part needs $P(Z > 1.084)$ and names no source. Recomputed: $z = 6.17/5.69 = 1.0844$, tail 0.1391; a 2-place table gives 0.1401 at 1.08. The band $0.139485 \pm 0.0008$ takes 0.139, 0.1391, 0.140 and 0.1401 and refuses the slips 0.0570, 0.1521 and 0.8605 | append to the question, before "Give a decimal to 3 places.": "Read the normal tail from software or a table." Band unchanged
6. arma/problems-3.json | `items[2].parts[3].question` (`p-swap-spread-hold`) | [table-source] | fix | needs $P(Z > 1.5) = 0.0668$ and names no source; band $0.066807 \pm 0.0006$ takes 0.067 and 0.0668, refuses 0.1336 and 0.4013 | after "Using the method of part 3," the question is unchanged; append before "Give a decimal to 3 places.": "Read the tail from software or a table, as in part 3." Band unchanged
7. fin-ml/problems-3.json | `items[1].parts[1].question` (`p-trial-log-dsr`) | [table-source] | fix | needs $\Phi^{-1}(0.8) = 0.8416$ and $\Phi^{-1}(0.9264) = 1.4497$ and names no source. Recomputed: bracket 1.1926, annual 0.5336; from a table (0.84, 1.45) 0.5333. Band $0.53 \pm 0.006$ takes both, refuses 0.62 and 0.03 | append before "What is it as an annual Sharpe?": "Read the two quantiles from software or a normal table." Band unchanged
8. fin-ml/problems-3.json | `items[1].parts[3].question` (`p-trial-log-dsr`) | [table-source] | fix | needs $\Phi(1.69) = 0.9545$ and names no source; a table at 1.69 or 1.70 gives 0.9545 or 0.9554, both inside $0.954 \pm 0.002$; 0.933 and 0.998 are refused | append before "Give 3 decimal places.": "Read $\Phi$ from software or a normal table." Band unchanged
9. fin-ml/problems-3.json | `items[2].parts[3].question` (`p-futures-net-psr`) | [table-source] | fix | needs $\Phi(1.03)$ and names no source. Recomputed: $0.038/0.0370 = 1.027$, $\Phi = 0.8478$; a table at 1.03 gives 0.8485. Band $0.848 \pm 0.0015$ takes both and stops at 0.8495, below the `normal` band (from 0.8499); 0.984 is refused | append before "Give 3 decimal places.": "Read $\Phi$ from software or a normal table." Band unchanged
10. garch/problems-1.json | `items[0].parts[1]` (`p-stale-alarm`) | [table-source] | fix | needs $2(1 - \Phi(1.305))$ and names no source, and the band refuses a table reader. Recomputed: $z = 2.74/2.1 = 1.3048$, both tails 0.19197 (19.2%). A 2-place table gives 19.4% at 1.30 and 19.0% at 1.31; the band $0.191974 \pm 0.0006$ takes neither | `question`: append before "Give a percentage to 1 decimal place.": "Read $\Phi$ from software or a normal table." `widget.tol.abs` 0.0006 to 0.0025: the band $[0.1895, 0.1945]$ takes 19.0, 19.2 and 19.4 and refuses `one-tail` 0.0960, `normal` 0.0027 and `inside` 0.8080
11. estimation/problems-3.json | `items[1].parts[1].widget.wrong[3]` (`p-three-month-fund`, `decimal`) | [wide-wrong-tol] | fix | value 0.00086667 ($26/3/10{,}000$), band $\pm 0.005$: 0 and any answer under 0.0059 land on the decimals line | `tol.abs` 0.005 to 0.00005. Takes 0.00086667, 0.000867, 0.00087 and 0.0009; refuses 0, 0.001, the key 8.6667 and the slips 13, 26 and 2.9439
12. garch/problems-2.json | `items[1].parts[0].widget.wrong[3]` (`p-weekly-gas-arch`, `decimal`) | [wide-wrong-tol] | fix | value 0.00092308 ($6.0/0.65/10{,}000$), band $\pm 0.005$ | `tol.abs` 0.005 to 0.00005. Takes 0.00092308, 0.00092 and 0.0009; refuses 0, 0.001, the key 9.2308 and 6.0, 17.1429, 2.1
13. garch/problems-2.json | `items[1].parts[2].widget.wrong[3]` (`p-weekly-gas-arch`, `decimal`) | [wide-wrong-tol] | fix | value 0.002574 ($25.74/10{,}000$; $9.2308 + 0.35 \times 47.1692 = 25.74$), band $\pm 0.005$ | `tol.abs` 0.005 to 0.0005. Takes 0.002574, 0.0026 and 0.003; refuses 0, 0.01, part 1's 0.00092, the key 25.74 and 56.4, 15.009, 9.2308
14. garch/problems-2.json | `items[1].parts[4].widget.wrong[3]` (`p-weekly-gas-arch`, `decimal`) | [wide-wrong-tol] | fix | value 0.00254031 ($0.7385 + 17.28 + 7.3846 = 25.4031$, over 10,000), band $\pm 0.005$ | `tol.abs` 0.005 to 0.0005. Takes 0.00254031, 0.0025 and 0.003; refuses 0, 0.01, the key 25.4031 and 18.0185, 117.0462, 56.4
15. garch/problems-2.json | `items[2].parts[2].widget.wrong[2]` (`p-silver-moment-fit`, `decimal`) | [wide-wrong-tol] | fix | value 0.00001156 ($2.89 \times 0.04/10{,}000$), band $\pm 0.00005$ | `tol.abs` 0.00005 to 0.000002. Takes 0.00001156, 0.000012 and 0.00001; refuses 0, 0.0001, the key 0.1156 and 2.7744, 2.89
16. garch/problems-3.json | `items[0].parts[1].widget.wrong[2]` (`p-forecasts-to-parameters`, `decimal`) | [wide-wrong-tol] | fix | value 0.000049 ($0.49/10{,}000$), band $\pm 0.005$ | `tol.abs` 0.005 to 0.000005. Takes 0.000049 and 0.00005; refuses 0, 0.0001, 0.00049, the key 0.49 and 0.6763, 0.2
17. garch/problems-3.json | `items[3].parts[0].widget.wrong[3]` (`p-monthly-sleeve`, `decimal`) | [wide-wrong-tol] | fix | value 0.00433484 ($43.3484/10{,}000$), band $\pm 0.005$ | `tol.abs` 0.005 to 0.0005. Takes 0.00433484, 0.0043 and 0.004; refuses 0, 0.01, the key 43.3484 and 53.76, 17.01, 42.4266
18. garch/problems-3.json | `items[3].parts[2].widget.wrong[3]` (`p-monthly-sleeve`, `decimal`) | [wide-wrong-tol] | fix | value 0.00294742 ($29.4742/10{,}000$), band $\pm 0.005$ | `tol.abs` 0.005 to 0.0005. Takes 0.00294742, 0.0029 and 0.003; refuses 0, 0.01, the key 29.4742 and 42.428, 20.515, 29.927
19. numerics/problems-1.json | `items[2].parts[1].widget.wrong[1]` (`p-netting-sum`, `no-kappa`) | [wide-wrong-tol] | fix | value 0.004657 ($2^{22} \times 2^{-53} = 2^{-31} = 4.657 \times 10^{-10}$, times $10^7$), band $\pm 0.005$ | `tol.abs` 0.005 to 0.0005. Takes 0.004657, 0.0047 and 0.005; refuses 0, 0.01, 0.0466, the key 3.7206 and `eps` 7.4412
20. trig/problems-2.json | `items[0].parts[1].widget.wrong[0]` (`p-water-wheel`, `wrong-way`) | [wide-wrong-tol] | fix | value 0.0393 ($2.25\pi/180 = 0.03927$), band $\pm 0.05$ | `tol.abs` 0.05 to 0.005. Takes 0.0393, 0.03927, 0.039 and 0.04; refuses 0, 0.1, 2.25, the key 128.92 and `no-pi` 405
21. elimination/problems-1.json | `items[1].parts[1].question` (`p-three-lines`) | [escaped-apostrophe] | fix | the JSON string holds `Monday\\'s`, so the page shows a backslash | the question opens "Monday's order is $\mathbf{b} = (12, 41, 18)$." (the apostrophe alone); the rest is unchanged

## List B: same-course reuse warnings

Hit numbers in brackets are the order of the fresh run (1 to 189). Rows 1 to 13 are the exam sources, each ruled singly with both texts. Rows 14 to 18 are the `reuse` verdicts with a course source. Rows 19 to 30 are `stands` ruled singly. From row 31 on, one row per distinct line of a course, with its count.

1. (hit 43) estimation/problems-2.json | `items[2].parts[2]` | [exam-reuse] retold, source `exams/topic-1.6.json:items[23] (exam item `s-vol-annual`)` | stands | "You multiplied the sd by 52." <- "You multiplied the sd by 252." | stock annualising slip with its own number (52 against 252). Noted: both items annualise a normal MLE volatility, the standard task of the skill, with other data, period and key (7.84% against 22.45%)
2. (hit 47) fin-ml/problems-3.json | `items[3].parts[0]` | [exam-reuse] text, source `exams/topic-2.1.json:items[3] (exam item `e-kelly-odds`)` | stands | 10 shared words: "a win pays # per # staked and a loss costs the" | the shared words are the given of a bet with odds in its natural words ("a win pays £b per £1 staked and a loss costs the £1"); own $p = 0.70$ and $b = 0.8$ against 0.5 and 1.5; parts 2 to 5 (log growth, cap, doubling time, plan stage) are not in the exam item. Same ruling as `review-delta-ae-4.md` on `l9` and `r-kelly-odds`
3. (hit 53) functions/problems-2.json | `items[0].parts[0]` | [exam-reuse] retold, source `exams/topic-0.2.json:items[2] (exam item `e-gradient`)` | stands | "You divided the run by the rise." (identical) | stock slip line of the course (it stands in six units); no number, no story
4. (hit 59) functions/problems-2.json | `items[1].parts[0]` | [exam-reuse] retold, source `exams/topic-0.2.json:items[2] (exam item `e-gradient`)` | stands | "You divided the run by the rise." (identical) | as 53
5. (hit 89) multivar/problems-3.json | `items[2].parts[0]` | [exam-reuse] retold, source `exams/topic-1.3.json:items[23] (exam item `c-min-variance`)` | stands | "Asset A has volatility 40% and asset B 25%, with correlation 0.3." <- "Asset 1 has volatility 30% and asset 2 has 15%, with correlation 0.25."; "You dropped the correlation term $0.06w(1 - w)$." <- "You dropped the covariance term." | the stem is the given of a two-asset problem in its natural words with own numbers (40%, 25%, 0.3 against 30%, 15%, 0.25; key 0.2 against 0.125); the slip lines differ in wording. Closest call of the exam hits: parts 1 to 3 are the exam's task with scaffolding, parts 4 and 5 ($\lambda$, a budget of 1.02) are not in it. The item was re-authored and delta-read (`review-delta-problems-1.3-ab.md`)
6. (hit 152) testing/problems-1.json | `items[0].parts[3]` | [exam-reuse] retold, source `exams/topic-1.6.json:items[4] (exam item `s-sharpe-p`)` | stands | "You doubled the tail." (identical) | stock slip line of the course (12 hits); the exam item is a Sharpe p-value, this part a z test on cereal boxes
7. (hit 155) testing/problems-1.json | `items[1].parts[4]` | [exam-reuse] retold, source `exams/topic-1.6.json:items[28] (exam item `s-trades-needed`)` | stands | "You used 2.365, the two-sided cut-off." <- "You used 1.96, the two-sided cut-off." | stock slip with its own cut-off (2.365 against 1.96); the tasks differ (smallest advert rejected against a sample size)
8. (hit 159) testing/problems-1.json | `items[3].parts[1]` | [exam-reuse] retold, source `exams/topic-1.6.json:items[4] (exam item `s-sharpe-p`)` | stands | "You doubled the tail." (identical) | as 152; own tail $1 - 0.9599$
9. (hit 162) testing/problems-3.json | `items[1].parts[1]` | [exam-reuse] retold, source `exams/topic-1.6.json:items[4] (exam item `s-sharpe-p`)` | reuse | **exam** `s-sharpe-p`: "A strategy shows an annualised Sharpe ratio of 0.6 over 9 years ... What is the one-sided p-value? Give 4 decimal places." with `two-sided` "You doubled the tail. $H_1$ points one way ..." and $\Phi(1.8)$ given. Problem: "Manager H has a Sharpe ratio of 0.9 over 9 years", part 1 $t = 0.9\sqrt 9$, part 2 "what is H's one-sided p-value? Give 4 decimal places." with `two-sided` "You doubled the tail. ..." and $\Phi(2.7)$ given. Parts 1 and 2 are the exam item with one number changed and the same 9 years (also `testing` has "0.8 over 9 years. What is its $t$ statistic?") | renumber the record, keeping $t = 2.7$ so parts 2 and 3 hold: `items[1].prose` last sentence: "Manager H has a Sharpe ratio of 0.54 over 25 years." `parts[0].feedback.correct`: "$t = \mathrm{SR}\sqrt T = 0.54 \times \sqrt{25} = 2.7$." `parts[0].widget.wrong`: `over-root` 0.3 to 0.108, `times-t` 8.1 to 13.5 (bands unchanged). `byKey.over-root`: "You divided by $\sqrt{25}$. The standard error of a Sharpe ratio is $\tfrac{1}{\sqrt T}$, so $t$ multiplies by $\sqrt T$." `byKey.times-t`: "You multiplied by 25 years. The $t$ statistic grows with $\sqrt T = 5$." `parts[0].explain.text`: "Over 25 years the Sharpe ratio has standard error $\tfrac{1}{5}$. So 0.54 sits $0.54 \times 5 = 2.7$ standard errors above 0." Recomputed: $0.54 \times 5 = 2.7$, $0.54/5 = 0.108$, $0.54 \times 25 = 13.5$; key 2.7 and its band refuse both. No Sharpe of 0.54 and no 25-year record with a Sharpe in `testing` or its exams (25 years stands once, as a no-skill standard error). The set's number script needs the same three values. The stock line "You doubled the tail." stays, so the hit still fires after the fix: waive it then (second block below)
10. (hit 167) testing/problems-4.json | `items[2].parts[1]` | [exam-reuse] retold, source `exams/topic-1.6.json:items[20] (exam item `s-chi-order-mix`)` | reuse | **exam** `s-chi-order-mix` part 1: `over-observed` "You divided by the observed counts. Pearson's statistic divides by the expected counts, 100 and 60." and `no-divide` "You added the squared gaps, $196 + 196$, without dividing each by its expected count." Problem part 2: `over-observed` "You divided by the observed counts. Pearson's statistic divides by the expected counts." and `no-divide` "You added the squared gaps, $4 \times 64$, without dividing each by its expected count." Two slip lines of one exam part, word for word but the numbers | `feedback.byKey.no-divide`: "256 is $4 \times 64$, the squared gaps alone. Divide each 64 by its cell's expected count, then add." `feedback.byKey.over-observed`: "You put the sold counts underneath: $\tfrac{64}{50} + \tfrac{64}{40} + \tfrac{64}{20} + \tfrac{64}{40} = 7.68$. The expected counts go there." Recomputed: the four cells 8 out sold 50, 40, 20 and 40; $1.28 + 1.6 + 3.2 + 1.6 = 7.68$, the `over-observed` value; $4 \times 64 = 256$. No such line in `testing` or its exams
11. (hit 183) vectors/problems-2.json | `items[1].parts[1]` | [exam-reuse] retold, source `exams/topic-1.4.json:items[7] (exam item `a-undo-two-steps`)` | stands | "You multiplied matching entries." (identical) | stock slip line for a matrix product (it stands in three units of the course); no number, no story
12. (hit 186) vectors/problems-3.json | `items[2].parts[0]` | [exam-reuse] retold, source `exams/topic-1.4.json:items[7] (exam item `a-undo-two-steps`)` | stands | "You multiplied matching entries." (identical) | as 183
13. (hit 189) vectors/problems-3.json | `items[3].parts[0]` | [exam-reuse] retold, source `exams/topic-1.4.json:items[7] (exam item `a-undo-two-steps`)` | stands | "You multiplied matching entries." (identical) | as 183
14. (hit 73) limits/problems-3.json | `items[0].parts[1]` | [slip-line] retold, source `limits/l9-products-quotients.json:screens[10]` | reuse | whole feedback of `rates` is the lesson's `tops-bottoms` line word for word ("You divided $u'$ by $v'$. The derivative of a quotient is not the quotient of the derivatives.") | `feedback.byKey.rates`: "0.028 is $P'(0)/I'(0) = 2.1/75$, one rate over the other. The quotient rule also needs $P(0)$ and $I(0)$: $\tfrac{u'v - uv'}{v^2}$." Recomputed: $2.1/75 = 0.028$, the `rates` value. No such line in `limits` or its exams
15. (hit 127) stat-learning/problems-2.json | `items[1].parts[1]` | [slip-line] retold, source `stat-learning/l7-shrinking.json:screens[1]` | reuse | `on-top` is the lesson's `top` line word for word and `subtracted` is its `minus` line less one clause; with `ols` the part carries all three slip lines of `l7` screen 1 | `feedback.byKey.subtracted`: "That is $90/(100 - 20)$. The penalty makes the denominator larger: $100 + 20$." `feedback.byKey.on-top`: "That is $(90 + 20)/100$. The 20 joins $\sum x^2$ underneath: $90/120$." Recomputed: $90/80 = 1.125$, $110/100 = 1.1$, $90/120 = 0.75$. No such line in `stat-learning` or its exams
16. (hit 132) stat-learning/problems-3.json | `items[3].parts[1]` | [slip-line] retold, source `stat-learning/homework-3.json:items[5]` | reuse | first sentence of `swapped` is `h-cost-t`'s whole `swap` line | cleared by the fix of row 133 (same line)
17. (hit 133) stat-learning/problems-3.json | `items[3].parts[1]` | [slip-line] retold, source `stat-learning/review-3.json:items[2]` | reuse | whole feedback of `swapped` is `r-threshold`'s `swap` line word for word ("You put the miss cost on top. The threshold is the false-alarm cost over the total.") | `feedback.byKey.swapped`: "That is $18{,}000/24{,}000$, with the spike cost on top. The wasted hedge, £6,000, belongs there." Recomputed: $18{,}000/24{,}000 = 0.75$, the `swapped` value; $6{,}000/24{,}000 = 0.25$, the key. No such line in `stat-learning` or its exams
18. (hit 137) stat-learning/problems-4.json | `items[1].parts[2]` | [slip-line] retold, source `stat-learning/l16-groups-nobody-labelled.json:screens[2]` | reuse | the line carries the lesson's number run: "$2 + 0 + 2 + 4 + 0 + 4$. Inertia squares them." against "$2 + 0 + 2 + 4 + 2 + 6$. Inertia squares them." (four of six terms and the closing sentence) | `feedback.byKey.unsquared`: "12 is the sum of the distances themselves. Square each one first: $4 + 0 + 4 + 16 + 0 + 16$." Recomputed: $2 + 0 + 2 + 4 + 0 + 4 = 12$, the `unsquared` value; the squares add to 40, the key. Same part, not flagged but the lesson's `var` line with one noun changed: `feedback.byKey.averaged`: "6.67 is $40/6$. Inertia adds the squares and does not average them." ($40/6 = 6.667$). The data (2, 4, 6 and 18, 22, 26 against the lesson's shares) stand as a toy of the method; only the line is reuse
19. (hit 31) elimination/problems-3.json | `items[0].parts[0]` | [slip-line] retold, source `elimination/l9-area-scale.json:quiz[0]` | stands | "You added $bc$. The determinant is $ad - bc = 12 - 4 = 8$." <- "You added $bc$: $12 + 2 = 14$. The determinant is $12 - 2 = 10$."; "What is the area of the cut logo?" <- "What is the area of the image?" | the slip line carries its own numbers ($12 - 4 = 8$ against $12 - 2 = 10$); "What is the area of ..." is the task's plain question. Noted: $\mathbf T$ at $k = 2$ shares three entries with `r-area`'s matrix; the dial $k$ and parts 2 to 4 are new (re-authored and delta-read in `review-delta-problems-ac-1.md`)
20. (hit 32) elimination/problems-3.json | `items[0].parts[0]` | [slip-line] retold, source `elimination/review-3.json:items[0]` | stands | "You added $bc$. The determinant is $ad - bc = 12 - 4 = 8$." <- "You added $bc$: $12 + 2 = 14$. The determinant is $12 - 2 = 10$."; "What is the area of the cut logo?" <- "What is the area of the image?" | the slip line carries its own numbers ($12 - 4 = 8$ against $12 - 2 = 10$); "What is the area of ..." is the task's plain question. Noted: $\mathbf T$ at $k = 2$ shares three entries with `r-area`'s matrix; the dial $k$ and parts 2 to 4 are new (re-authored and delta-read in `review-delta-problems-ac-1.md`)
21. (hit 87) multivar/problems-2.json | `items[0].parts[1]` | [slip-line] retold, source `multivar/l5-steepest-climb.json:screens[3]` | stands | "You added the components." (identical); "Using $\nabla f = (12, 9)$, how steep is the steepest climb from P?" <- "How steep is the steepest climb from P?" | "You added the components." is stock; the question and the explain line state the fact $|\nabla f|$ is the steepest slope in its natural words, with own gradient (12, 9)
22. (hit 88) multivar/problems-2.json | `items[0].parts[1]` | [slip-line] retold, source `multivar/review-2.json:items[0]` | stands | "You added the components." (identical); "The steepest climb runs along $\nabla f$, with slope $|\nabla f| = \sqrt{144 + 81} = 15$." <- "The steepest climb is along (4, 3) with slope $\sqrt{4^2 + 3^2} = 5$." | "You added the components." is stock; the question and the explain line state the fact $|\nabla f|$ is the steepest slope in its natural words, with own gradient (12, 9)
23. (hit 90) multivar/problems-3.json | `items[2].parts[1]` | [slip-line] retold, source `multivar/l12-min-variance.json:screens[3]` | stands | "You solved $0.1625w - 0.065 = 0$. The derivative of $0.1625w^2$ is $0.325w$." <- "You solved $0.038w_1 = 0.008$. The derivative of $0.038w_1^2$ is $0.076w_1$." | the factor-of-two slip in its plain words with this parabola's own coefficients
24. (hit 120) regression/problems-1.json | `items[3].parts[2]` | [slip-line] retold, source `regression/problems-3.json:items[3]` | stands | "You left out the intercept $-21.4$." <- "You left out the intercept, 0.05."; "A residual is actual minus fitted, $36 - 39.4$, so it is negative." <- "A residual is actual minus fitted." | both lines are stock (an intercept left out; the definition of a residual) with own numbers
25. (hit 126) stat-learning/problems-1.json | `items[1].parts[1]` | [slip-line] retold, source `stat-learning/homework-1.json:items[3]` | stands | "You divided by 4 for the variance." <- "You divided by 3 for the variance."; "You divided by 4 for the variance. Here the variance divides by 5." <- "You divided by 3 for the variance. Here the variance divides by 4." | the divisor slip with its own divisor (5 against 4), and a stock line
26. (hit 130) stat-learning/problems-3.json | `items[0].parts[2]` | [slip-line] retold, source `stat-learning/review-3.json:items[1]` | stands | "You multiplied the probability by 0.407." <- "You multiplied the probability by $e^{0.3}$."; "The factor applies to the odds, $p/(1 - p)$." <- "The factor applies to the odds." | the odds slip with its own factor 0.407; "the factor applies to the odds" is the fact in its natural words
27. (hit 153) testing/problems-1.json | `items[1].parts[0]` | [slip-line] retold, source `testing/problems-2.json:items[2]` | stands | "You divided the total, 144, by 7." <- "You divided the total, $-36$, by 8."; "You divided by $s$ itself." <- "You divided by $s_d$ itself."; "You used $s = 1.871$, from dividing by 8." <- "You used $s_d = 2.828$, from dividing by 9."; "You used $s = 1.871$, from dividing by 8. With $s = 2$ the statistic is $-2.121$." <- "You used $s_d = 2.828$, from dividing by 9. With $s_d = 3$ the statistic is $-4$."; "Using $\bar x = 18$ and $s = 2$, what is the $t$ statistic for $H_0: \mu = 19.5$?" <- "Using $\bar d = -4$ and $s_d = 3$, what is the paired $t$ statistic?"; "$-2.121$ is below $-1.895$, the one-sided cut-off of $t_7$" <- "The one-sided 5% cut-off of $t_8$ is 1.860."; "Using $t = -2.121$ from part 3, which conclusion is right at 5%?" <- "Using $p = 0.0118$ from part 3, which statement is right?" | seven pairs, all between the one-sample test of level 1 and the paired test of level 2. A paired test is the one-sample test on the differences, so mean, sd and $t$ and their slips are the method. Data, story, null and cut-off differ, and `p-running-shoes` parts 4 and 5 (pairing against Welch, power) are new
28. (hit 157) testing/problems-1.json | `items[3].parts[1]` | [slip-line] retold, source `testing/problems-3.json:items[1]` | stands | "You doubled the tail." (identical); "The upper tail beyond 1.75 holds $1 - 0.9599 = 0.0401$." <- "The upper tail beyond 2.7 holds 0.0035." | stock line, and "the upper tail beyond" is the standard phrase for a one-sided p-value (waived before for this course)
29. (hit 160) testing/problems-2.json | `items[2].parts[0]` | [slip-line] retold, source `testing/problems-1.json:items[1]` | stands | "You divided the total, $-36$, by 8." <- "You divided the total, 144, by 7."; "You divided by $s_d$ itself." <- "You divided by $s$ itself."; "You used $s_d = 2.828$, from dividing by 9." <- "You used $s = 1.871$, from dividing by 8."; "You used $s_d = 2.828$, from dividing by 9. With $s_d = 3$ the statistic is $-4$." <- "You used $s = 1.871$, from dividing by 8. With $s = 2$ the statistic is $-2.121$."; "Using $\bar d = -4$ and $s_d = 3$, what is the paired $t$ statistic?" <- "Using $\bar x = 18$ and $s = 2$, what is the $t$ statistic for $H_0: \mu = 19.5$?"; "The one-sided 5% cut-off of $t_8$ is 1.860." <- "$-2.121$ is below $-1.895$, the one-sided cut-off of $t_7$"; "The mean of 9 differences has standard error $\tfrac{3}{\sqrt 9} = 1$." <- "The mean of $n$ boxes has standard error $\tfrac{\sigma}{\sqrt n}$." | seven pairs, all between the one-sample test of level 1 and the paired test of level 2. A paired test is the one-sample test on the differences, so mean, sd and $t$ and their slips are the method. Data, story, null and cut-off differ, and `p-running-shoes` parts 4 and 5 (pairing against Welch, power) are new
30. (hit 161) testing/problems-3.json | `items[1].parts[1]` | [slip-line] retold, source `testing/problems-1.json:items[3]` | stands | "You doubled the tail." (identical); "The upper tail beyond 2.7 holds 0.0035." <- "The upper tail beyond 1.75 holds $1 - 0.9599 = 0.0401$." | stock line, and "the upper tail beyond" is the standard phrase for a one-sided p-value (waived before for this course)
31. coint/problems-1.json | problems-1 `items[0].parts[0]` | [slip-line] retold | stands | 2 hits (1, 2): "You multiplied by 0.15 instead of $0.15^2$." <- "You multiplied by $r^2 = 0.09$ instead of $r = 0.3$." / "You multiplied by $r^2 = 0.25$ instead of $r = 0.5$.". Sources: l1-two-walks, review-1 | slip named in stock words with this part's own numbers; the source carries other numbers and another story
32. coint/problems-1.json | problems-1 `items[3].parts[0]` | [slip-line] retold | stands | 1 hit (3): "You applied 0.40 to all 1,200 pairs." <- "You applied 5% to all 124,750 pairs.". Sources: l2-not-correlation | slip named in stock words with this part's own numbers; the source carries other numbers and another story
33. complex/problems-1.json | problems-1 `items[0].parts[0]` | [slip-line] retold | stands | 1 hit (4): "You multiplied real by real and imaginary by imaginary only." (identical in the source). Sources: l1-square-root-of-minus-one | stock slip line: it names a common slip in its plain words and carries no number or story; a learner would not know it as a repeat
34. complex/problems-1.json | problems-1 `items[0].parts[2]`; problems-1 `items[1].parts[1]`; problems-1 `items[3].parts[3]` | [slip-line] retold | stands | 3 hits (5, 7, 11): "You added the two parts." (identical in the source). Sources: l2-points-in-a-plane | stock slip line: it names a common slip in its plain words and carries no number or story; a learner would not know it as a repeat
35. complex/problems-1.json, complex/problems-2.json | problems-1 `items[0].parts[4]`; problems-1 `items[1].parts[2]`; problems-1 `items[3].parts[4]`; problems-2 `items[0].parts[3]` | [slip-line] retold | stands | 4 hits (6, 8, 12, 13): "You took the real part over the imaginary part." (identical in the source). Sources: problems-1, problems-2 | stock slip line: it names a common slip in its plain words and carries no number or story; a learner would not know it as a repeat
36. complex/problems-1.json | problems-1 `items[3].parts[0]` | [slip-line] retold | stands | 2 hits (9, 10): "You swapped cosine and sine." (identical in the source). Sources: l8-exp-and-log, review-1 | stock slip line: it names a common slip in its plain words and carries no number or story; a learner would not know it as a repeat
37. complex/problems-2.json | problems-2 `items[1].parts[4]`; problems-2 `items[2].parts[0]` | [slip-line] retold | stands | 4 hits (14, 15, 16, 17): "You added the sizes of the parts." (identical in the source); further pairs of the same feedback: "You added the sizes of the parts. The modulus is $\sqrt{5^2 + 2^2}$." <- "You added the sizes of the parts. The modulus is $\sqrt{(-2)^2 + 2^2}$."; "You added the sizes of the parts. The modulus is $\sqrt{8^2 + 15^2}$." <- "You added the sizes of the parts. The modulus is $\sqrt{(-2)^2 + 2^2}$.". Sources: l2-points-in-a-plane, review-1 | stock slip line: it names a common slip in its plain words and carries no number or story; a learner would not know it as a repeat
38. conditional/problems-2.json | problems-2 `items[1].parts[1]` | [slip-line] retold | stands | 4 hits (18, 19, 20, 21): "You multiplied the probability 0.15 by 3." <- "You multiplied the probability 0.2 by 6." / "You multiplied the probability 0.25 by 4." / "You multiplied the probability 0.55 by 1.5."; further pairs of the same feedback: "The ratio multiplies the odds, $\tfrac{3}{17}$." <- "The ratio multiplies the old odds of 1 to 3."; "The ratio multiplies the odds, $\tfrac{3}{17}$." <- "The ratio multiplies the old odds of 1 to 4.". Sources: l10-odds-form, l11-updating-twice, l26-trading-signal, review-2 | slip named in stock words with this part's own numbers; the source carries other numbers and another story
39. conditional/problems-3.json | problems-3 `items[0].parts[0]` | [slip-line] retold | stands | 1 hit (22): "You divided by the 260 up days." <- "You divided by the 120 up days.". Sources: l1-what-changes | slip named in stock words with this part's own numbers; the source carries other numbers and another story
40. counting/problems-1.json, counting/problems-2.json | problems-1 `items[3].parts[0]`; problems-2 `items[3].parts[0]` | [slip-line] retold | stands | 2 hits (23, 25): "You multiplied 11 by 4. Choosing 4 of 11 is $\binom{11}{4}$." / "You multiplied 14 by 3. Choosing 3 of 14 is $\binom{14}{3}$." <- "You multiplied 11 by 4. Choosing 4 of 11 is $\binom{11}{4}$." / "You multiplied 14 by 3. Choosing 3 of 14 is $\binom{14}{3}$.". Sources: problems-1, problems-2 | slip named in stock words with this part's own numbers; the source carries other numbers and another story
41. counting/problems-2.json | problems-2 `items[1].parts[0]` | [slip-line] retold | stands | 1 hit (24): "You took the 20 away twice." <- "You took the 9 away twice.". Sources: l7-what-you-do-not-want | slip named in stock words with this part's own numbers; the source carries other numbers and another story
42. counting/problems-3.json | problems-3 `items[0].parts[0]` | [slip-line] retold | stands | 3 hits (26, 27, 28): "You took start minus end." (identical in the source). Sources: l12-proving-with-vectors, l9-arrows, review-3 | stock slip line: it names a common slip in its plain words and carries no number or story; a learner would not know it as a repeat
43. counting/problems-3.json | problems-3 `items[1].parts[2]` | [slip-line] retold | stands | 1 hit (29): "You subtracted the components." (identical in the source). Sources: l11-how-long | stock slip line: it names a common slip in its plain words and carries no number or story; a learner would not know it as a repeat
44. elimination/problems-1.json | problems-1 `items[1].parts[0]` | [slip-line] retold | stands | 1 hit (30): "You put the multipliers above the diagonal." (identical in the source). Sources: l3-factorisation | stock slip line: it names a common slip in its plain words and carries no number or story; a learner would not know it as a repeat
45. ensembles/problems-2.json | problems-2 `items[1].parts[0]` | [slip-line] retold | stands | 1 hit (33): "You used $\sqrt{10} = 3.16$ before rounding down." <- "You used $\sqrt{30} = 5.48$ before rounding down."; further pairs of the same feedback: "scikit-learn offers 3 features." <- "scikit-learn uses 5 features.". Sources: l6-random-forest | slip named in stock words with this part's own numbers; the source carries other numbers and another story
46. equations/problems-1.json | problems-1 `items[0].parts[0]` | [slip-line] retold | stands | 1 hit (34): "You took $a$ away from 5." <- "You took 4 away from 12.". Sources: l4-putting-brackets-back | slip named in stock words with this part's own numbers; the source carries other numbers and another story
47. equations/problems-1.json | problems-1 `items[2].parts[1]` | [slip-line] retold | stands | 1 hit (35): "You divided only $2n$ by 2." <- "You divided only $C$ by 2.". Sources: l13-changing-the-subject | slip named in stock words with this part's own numbers; the source carries other numbers and another story
48. equations/problems-2.json | problems-2 `items[0].parts[0]` | [slip-line] retold | stands | 1 hit (36): "You swapped the two charges." (identical in the source). Sources: l1-letters-for-numbers | stock slip line: it names a common slip in its plain words and carries no number or story; a learner would not know it as a repeat
49. equations/problems-4.json | problems-4 `items[2].parts[2]` | [slip-line] retold | stands | 1 hit (37): "You squared 81. Here $t^2 = 81$, so undo the square instead." <- "You squared 4. Here $x^2 = 4$, so undo the square instead.". Sources: l15-swapping-in | slip named in stock words with this part's own numbers; the source carries other numbers and another story
50. equations/problems-4.json | problems-4 `items[3].parts[1]` | [slip-line] retold | stands | 1 hit (38): "You multiplied 50 by 0.25. Divide instead: $50 \div 0.25 = 200$." <- "You multiplied 120 by 0.04. Divide instead: $120 \div 0.04 = 3000$.". Sources: homework-1 | slip named in stock words with this part's own numbers; the source carries other numbers and another story
51. estimation/problems-1.json | problems-1 `items[1].parts[2]` | [slip-line] retold | stands | 1 hit (39): "You added the bias, 1.5, without squaring it." <- "You added the bias, −0.4, without squaring it.". Sources: homework-1 | slip named in stock words with this part's own numbers; the source carries other numbers and another story
52. estimation/problems-1.json, estimation/problems-2.json | problems-1 `items[3].parts[0]`; problems-2 `items[2].parts[0]` | [slip-line] retold | stands | 2 hits (40, 41): "You dropped the minus signs." (identical in the source). Sources: problems-1, problems-2 | stock slip line: it names a common slip in its plain words and carries no number or story; a learner would not know it as a repeat
53. estimation/problems-2.json | problems-2 `items[2].parts[2]` | [slip-line] retold | stands | 1 hit (42): "You multiplied the sd by 52." <- "You multiplied the sd by 252.". Sources: l8-volatility-mle | slip named in stock words with this part's own numbers; the source carries other numbers and another story
54. exp-log/problems-1.json, exp-log/problems-2.json | problems-1 `items[0].parts[0]`; problems-2 `items[3].parts[0]` | [slip-line] retold | stands | 2 hits (44, 46): "You raised $2000 \times 1.3$ to the power." / "You raised $3000 \times 2$ to the power." <- "You raised $2000 \times 1.3$ to the power." / "You raised $3000 \times 2$ to the power.". Sources: problems-1, problems-2 | slip named in stock words with this part's own numbers; the source carries other numbers and another story
55. exp-log/problems-2.json | problems-2 `items[0].parts[1]` | [slip-line] retold | stands | 1 hit (45): "You multiplied the logs, $5 \times 11$." <- "You multiplied the logs, $2 \times 3$.". Sources: review-2 | slip named in stock words with this part's own numbers; the source carries other numbers and another story
56. functions/problems-2.json | problems-2 `items[0].parts[0]`; problems-2 `items[1].parts[0]` | [slip-line] retold | stands | 10 hits (48, 49, 50, 51, 52, 54, 55, 56, 57, 58): "You divided the run by the rise." (identical in the source); further pairs of the same feedback: "You divided the run by the rise. The gradient is rise over run: $-7.5 \div 3$." <- "You divided the run by the rise. The gradient is rise over run: $3 \div 6$."; "You divided the run by the rise. The gradient is rise over run: $28 \div 7$." <- "You divided the run by the rise. The gradient is rise over run: $3 \div 6$.". Sources: homework-2, l6-how-steep, l7-slope-and-start, l8-line-through-two-points, review-2 | stock slip line: it names a common slip in its plain words and carries no number or story; a learner would not know it as a repeat
57. garch/problems-2.json, garch/problems-3.json | problems-2 `items[0].parts[0]`; problems-3 `items[0].parts[1]` | [slip-line] retold | stands | 2 hits (60, 66): "You worked in decimals." (identical in the source). Sources: problems-2, problems-3 | stock slip line: it names a common slip in its plain words and carries no number or story; a learner would not know it as a repeat
58. garch/problems-2.json | problems-2 `items[1].parts[4]` | [slip-line] retold | stands | 1 hit (61): "You gave 0.80 to the squared return." <- "You gave 0.94 to the squared return.". Sources: review-2 | slip named in stock words with this part's own numbers; the source carries other numbers and another story
59. garch/problems-2.json, garch/problems-3.json | problems-2 `items[1].parts[4]`; problems-2 `items[3].parts[0]`; problems-3 `items[3].parts[0]` | [slip-line] retold | stands | 3 hits (62, 65, 67): "You gave it in decimals." (identical in the source); further pairs of the same feedback: "Everything here is in %, so the variance is 2.9495 %²." <- "Everything here is in %, so the variance is 43.35 %²."; "Everything here is in %, so the variance is 43.35 %²." <- "Everything here is in %, so the variance is 2.9495 %²."; "You gave it in decimals. Everything here is in %, so the variance is 2.9495 %²." <- "You gave it in decimals. Everything here is in %, so the variance is 43.35 %²."; "You gave it in decimals. Everything here is in %, so the variance is 43.35 %²." <- "You gave it in decimals. Everything here is in %, so the variance is 2.9495 %².". Sources: problems-2, problems-3 | stock slip line: it names a common slip in its plain words and carries no number or story; a learner would not know it as a repeat
60. garch/problems-2.json | problems-2 `items[2].parts[3]` | [slip-line] retold | stands | 2 hits (63, 64): "You used $0.13 \times 4.5$ rather than $0.13 \times 4.5^2$." <- "You used 2 rather than $2^2 = 4$." / "You used 3 rather than $3^2 = 9$.". Sources: l6-arch, review-2 | slip named in stock words with this part's own numbers; the source carries other numbers and another story
61. integrals/problems-2.json | problems-2 `items[2].parts[1]` | [slip-line] retold | stands | 1 hit (68): "You took parabola minus line." (identical in the source). Sources: review-2 | stock slip line: it names a common slip in its plain words and carries no number or story; a learner would not know it as a repeat
62. integrals/problems-3.json | problems-3 `items[0].parts[0]` | [slip-line] retold | stands | 1 hit (69): "You lowered the power." (identical in the source). Sources: l6-working-backwards | stock slip line: it names a common slip in its plain words and carries no number or story; a learner would not know it as a repeat
63. integrals/problems-3.json | problems-3 `items[1].parts[0]` | [slip-line] retold | stands | 2 hits (70, 71): "You took $v = e^{-x}$. Its derivative is $-e^{-x}$, so $v = -e^{-x}$." <- "You took $v = \cos x$. Its derivative is $-\sin x$, so $v = -\cos x$." / "You took $v = e^{2x}$. Its derivative is $2e^{2x}$, so $v = \tfrac{1}{2}e^{2x}$.". Sources: l10-undo-product, review-3 | slip named in stock words with this part's own numbers; the source carries other numbers and another story
64. limits/problems-2.json, limits/problems-5.json | problems-2 `items[2].parts[0]`; problems-5 `items[2].parts[0]` | [slip-line] retold | stands | 2 hits (72, 78): "You dropped the 0.5 in front of $q^2$." / "You dropped the 2 in front of $\arctan$." <- "You dropped the 0.5 in front of $q^2$." / "You dropped the 2 in front of $\arctan$.". Sources: problems-2, problems-5 | slip named in stock words with this part's own numbers; the source carries other numbers and another story
65. limits/problems-3.json | problems-3 `items[1].parts[0]`; problems-3 `items[3].parts[0]` | [slip-line] retold | stands | 2 hits (74, 76): "You left out the inside's derivative, $-1$." / "You left out the inside's derivative, $\tfrac{\pi}{6}$." <- "You left out the inside's derivative, 5.". Sources: l11-standard-derivatives | slip named in stock words with this part's own numbers; the source carries other numbers and another story
66. limits/problems-3.json | problems-3 `items[1].parts[1]`; problems-3 `items[3].parts[2]` | [slip-line] retold | stands | 2 hits (75, 77): "You multiplied the two derivatives, $1 \times (-60)$." / "You multiplied the two derivatives, $5 \times (-0.05\pi)$." <- "You multiplied the two derivatives, $1 \times \frac{1}{2\sqrt{x}}$.". Sources: l7-power-rule | slip named in stock words with this part's own numbers; the source carries other numbers and another story
67. limits-thm/problems-2.json | problems-2 `items[1].parts[3]` | [slip-line] retold | stands | 3 hits (79, 80, 81): "You used $0.06 + 0.045$ as the log drift." <- "You used $m = 0.05$ as the log drift." / "You used $mT = 0.16$ as the log drift." / "You used 0.05 as the log drift.". Sources: homework-2, l8-lognormal, review-2 | slip named in stock words with this part's own numbers; the source carries other numbers and another story
68. limits-thm/problems-3.json | problems-3 `items[1].parts[2]` | [slip-line] retold | stands | 1 hit (82): "You added 12 chances of 0.0606." <- "You added 20 chances of 0.0455.". Sources: l12-skill-or-luck | slip named in stock words with this part's own numbers; the source carries other numbers and another story
69. limits-thm/problems-3.json | problems-3 `items[2].parts[0]` | [slip-line] retold | stands | 1 hit (83): "You divided the threshold by the mean." (identical in the source). Sources: l10-bound-that-holds | stock slip line: it names a common slip in its plain words and carries no number or story; a learner would not know it as a repeat
70. limits-thm/problems-3.json | problems-3 `items[3].parts[1]` | [slip-line] retold | stands | 1 hit (84): "You divided the standard error by the average." (identical in the source). Sources: l12-skill-or-luck | stock slip line: it names a common slip in its plain words and carries no number or story; a learner would not know it as a repeat
71. linear-maps/problems-1.json | problems-1 `items[2].parts[1]` | [slip-line] retold | stands | 1 hit (85): "You took the usual zero." (identical in the source). Sources: l1-axioms | stock slip line: it names a common slip in its plain words and carries no number or story; a learner would not know it as a repeat
72. linear-maps/problems-2.json | problems-2 `items[1].parts[1]` | [slip-line] retold | stands | 1 hit (86): "You wrote the coordinates as rows." (identical in the source). Sources: homework-2 | stock slip line: it names a common slip in its plain words and carries no number or story; a learner would not know it as a repeat
73. multivar/problems-4.json, multivar/problems-5.json | problems-4 `items[1].parts[0]`; problems-5 `items[1].parts[1]` | [slip-line] retold | stands | 2 hits (91, 93): "You wrote $(2u)^2$ as $2u^2$. It is $4u^2$." / "You wrote $x^2 + y^2$ as $r$. It is $r^2$." <- "You wrote $(2u)^2$ as $2u^2$. It is $4u^2$." / "You wrote $x^2 + y^2$ as $r$. It is $r^2$.". Sources: problems-4, problems-5 | slip named in stock words with this part's own numbers; the source carries other numbers and another story
74. multivar/problems-4.json | problems-4 `items[2].parts[1]` | [slip-line] retold | stands | 1 hit (92): "You added the two single integrals." (identical in the source). Sources: l13-volume | stock slip line: it names a common slip in its plain words and carries no number or story; a learner would not know it as a repeat
75. number-sense/problems-1.json | problems-1 `items[0].parts[1]` | [slip-line] retold | stands | 2 hits (94, 95): "You added the tops and the bottoms to get $\tfrac{3}{9}$." <- "You added the tops and the bottoms to get $\tfrac{2}{7}$." / "You added the tops and the bottoms to get $\tfrac{3}{7}$.". Sources: l3-adding-pieces, review-1 | slip named in stock words with this part's own numbers; the source carries other numbers and another story
76. number-sense/problems-1.json | problems-1 `items[3].parts[0]` | [slip-line] retold | stands | 2 hits (96, 97): "You added 27 to the top and the bottom." <- "You added 1 to the top and the bottom.". Sources: homework-1, l2-same-amount | slip named in stock words with this part's own numbers; the source carries other numbers and another story
77. number-sense/problems-1.json | problems-1 `items[3].parts[2]` | [slip-line] retold | stands | 2 hits (98, 99): "You added the two fractions." (identical in the source); further pairs of the same feedback: "multiply the tops and the bottoms." <- "Multiply the tops and multiply the bottoms.". Sources: l4-fraction-of-fraction, review-1 | stock slip line: it names a common slip in its plain words and carries no number or story; a learner would not know it as a repeat
78. number-sense/problems-3.json | problems-3 `items[0].parts[0]` | [slip-line] retold | stands | 1 hit (100): "You took the square root." (identical in the source). Sources: l11-undoing-a-square | stock slip line: it names a common slip in its plain words and carries no number or story; a learner would not know it as a repeat
79. number-sense/problems-3.json | problems-3 `items[2].parts[0]` | [slip-line] retold | stands | 4 hits (101, 102, 103, 104): "You added the indices." (identical in the source). Sources: homework-4, l10-repeated-multiplication, l14-very-big-very-small, review-3 | stock slip line: it names a common slip in its plain words and carries no number or story; a learner would not know it as a repeat
80. number-sense/problems-4.json | problems-4 `items[0].parts[1]` | [slip-line] retold | stands | 1 hit (105): "You multiplied the indices, $3 \times 1 \times 1$." <- "You multiplied the indices, $2 \times 2 \times 1$.". Sources: review-4 | slip named in stock words with this part's own numbers; the source carries other numbers and another story
81. number-sense/problems-4.json | problems-4 `items[2].parts[4]` | [slip-line] retold | stands | 2 hits (106, 107): "You multiplied by 3,600 and divided by 1,000." (identical in the source). Sources: l18-circles-and-units, review-4 | slip named in stock words with this part's own numbers; the source carries other numbers and another story
82. odes/problems-3.json | problems-3 `items[1].parts[0]` | [slip-line] retold | stands | 1 hit (108): "You swapped the coordinates." (identical in the source). Sources: l13-linearising | stock slip line: it names a common slip in its plain words and carries no number or story; a learner would not know it as a repeat
83. quadratics/problems-1.json | problems-1 `items[0].parts[0]` | [slip-line] retold | stands | 1 hit (109): "You added 4 and 11 for the corner." <- "You added 6 and 2 for the corner.". Sources: l1-two-brackets | slip named in stock words with this part's own numbers; the source carries other numbers and another story
84. random-vars/problems-1.json, random-vars/problems-3.json | problems-1 `items[2].parts[1]`; problems-3 `items[1].parts[3]` | [slip-line] retold | stands | 2 hits (110, 113): "You used $E[AB] = 2.0$ from part 3's slip." / "You used $c = 0.85$ from part 1's slip." <- "You used $E[AB] = 2.0$ from part 3's slip." / "You used $c = 0.85$ from part 1's slip."; further pairs of the same feedback: "You used $E[AB] = 2.0$ from part 3's slip. With $\operatorname{Cov} = 1.68$ the answer is 0.5833." <- "You used $c = 0.85$ from part 1's slip. With $c = 0.15$ the answer is 0.25."; "You used $c = 0.85$ from part 1's slip. With $c = 0.15$ the answer is 0.25." <- "You used $E[AB] = 2.0$ from part 3's slip. With $\operatorname{Cov} = 1.68$ the answer is 0.5833.". Sources: problems-1, problems-3 | the carry line's fixed form ("You used x, part k's slip") with this problem's own value
85. random-vars/problems-2.json | problems-2 `items[1].parts[0]` | [slip-line] retold | stands | 1 hit (111): "You treated up and down as equally likely." (identical in the source). Sources: l8-indicators | stock slip line: it names a common slip in its plain words and carries no number or story; a learner would not know it as a repeat
86. random-vars/problems-3.json | problems-3 `items[0].parts[2]` | [slip-line] retold | stands | 1 hit (112): "You multiplied the sd by 100." <- "You multiplied the sd by 4.". Sources: l10-scaling-and-adding | slip named in stock words with this part's own numbers; the source carries other numbers and another story
87. random-vars/problems-4.json, random-vars/problems-5.json | problems-4 `items[3].parts[2]`; problems-5 `items[3].parts[1]` | [slip-line] retold | stands | 2 hits (114, 115): "You used $\ln 1.05$, part 1's slip." / "You used $m = 2.1$, part 2's slip." <- "You used $\ln 1.05$, part 1's slip." / "You used $m = 2.1$, part 2's slip."; further pairs of the same feedback: "You used $\ln 1.05$, part 1's slip. With $E[\ln R] = -0.0527$ the answer is $-0.2108$." <- "You used $m = 2.1$, part 2's slip. With $m = 4.2$ the answer is 7.4."; "You used $m = 2.1$, part 2's slip. With $m = 4.2$ the answer is 7.4." <- "You used $\ln 1.05$, part 1's slip. With $E[\ln R] = -0.0527$ the answer is $-0.2108$.". Sources: problems-4, problems-5 | the carry line's fixed form ("You used x, part k's slip") with this problem's own value
88. ratio/problems-1.json | problems-1 `items[1].parts[0]`; problems-1 `items[2].parts[0]` | [slip-line] retold | stands | 2 hits (116, 117): "You moved the point one place." (identical in the source). Sources: l1-out-of-a-hundred | stock slip line: it names a common slip in its plain words and carries no number or story; a learner would not know it as a repeat
89. ratio/problems-3.json | problems-3 `items[0].parts[2]` | [slip-line] retold | stands | 2 hits (118, 119): "You treated £2,850 as one part." <- "You treated £1,260 as one part." / "You treated £18 as one part.". Sources: homework-3, l9-sharing | slip named in stock words with this part's own numbers; the source carries other numbers and another story
90. regression/problems-2.json | problems-2 `items[0].parts[1]` | [slip-line] retold | stands | 1 hit (121): "You divided by 64 itself." <- "You divided by 82.5 itself.". Sources: l5-how-sure | slip named in stock words with this part's own numbers; the source carries other numbers and another story
91. regression/problems-3.json | problems-3 `items[3].parts[0]` | [slip-line] retold | stands | 1 hit (122): "You left out the intercept, 0.05." <- "You left out the intercept $-21.4$.". Sources: problems-1 | slip named in stock words with this part's own numbers; the source carries other numbers and another story
92. series/problems-1.json | problems-1 `items[1].parts[1]` | [slip-line] retold | stands | 2 hits (123, 124): "You raised $80 \times 0.9$ to the power." <- "You raised $5 \times 3$ to the power." / "You raised $96 \times 0.5$ to the power.". Sources: homework-1, l3-multiplying-each-time | slip named in stock words with this part's own numbers; the source carries other numbers and another story
93. stat-learning/problems-1.json | problems-1 `items[1].parts[1]` | [slip-line] retold | stands | 1 hit (125): "You left out the noise." (identical in the source). Sources: review-1 | stock slip line: it names a common slip in its plain words and carries no number or story; a learner would not know it as a repeat
94. stat-learning/problems-2.json, stat-learning/problems-3.json | problems-2 `items[3].parts[3]`; problems-3 `items[3].parts[4]` | [slip-line] retold | stands | 4 hits (128, 129, 134, 135): "You used 0.515, part 3's slip." / "You used £1,080, part 4's slip." <- "You used $\hat y = 9$, part 1's slip." / "You used 0.515, part 3's slip." / "You used £1,080, part 4's slip.". Sources: problems-2, problems-3, problems-4 | the carry line's fixed form ("You used x, part k's slip") with this problem's own value
95. stat-learning/problems-3.json, stat-learning/problems-4.json | problems-3 `items[2].parts[2]`; problems-4 `items[0].parts[4]`; problems-4 `items[3].parts[2]` | [slip-line] retold | stands | 3 hits (131, 136, 141): "You compared with a coin's 0.5." (identical in the source). Sources: problems-3, problems-4 | slip named in stock words with this part's own numbers; the source carries other numbers and another story
96. stat-learning/problems-4.json | problems-4 `items[1].parts[3]` | [slip-line] retold | stands | 1 hit (138): "You left out the hinge." (identical in the source). Sources: l18-bending-the-line | stock slip line: it names a common slip in its plain words and carries no number or story; a learner would not know it as a repeat
97. stat-learning/problems-4.json | problems-4 `items[2].parts[1]` | [slip-line] retold | stands | 2 hits (139, 140): "You used $\hat y = 9$, part 1's slip." <- "You used 0.515, part 3's slip." / "You used £1,080, part 4's slip.". Sources: problems-2, problems-3 | the carry line's fixed form ("You used x, part k's slip") with this problem's own value
98. taylor/problems-2.json | problems-2 `items[0].parts[3]`; problems-2 `items[1].parts[1]`; problems-2 `items[3].parts[3]` | [slip-line] retold | stands | 3 hits (142, 143, 144): "You divided by 3. The coefficient divides by $3! = 6$." <- "You divided by $k = 4$. The coefficient divides by $4! = 24$.". Sources: l6-matching-derivatives | slip named in stock words with this part's own numbers; the source carries other numbers and another story
99. taylor/problems-3.json | problems-3 `items[1].parts[1]`; problems-3 `items[3].parts[1]` | [slip-line] retold | stands | 2 hits (145, 146): "You divided by $3! = 6$, as for $e^x$." / "You divided by $k!$, as for $e^x$." <- "You divided by 64, as for $h^3$.". Sources: l2-how-wrong | slip named in stock words with this part's own numbers; the source carries other numbers and another story
100. testing/problems-1.json | problems-1 `items[0].parts[1]` | [slip-line] retold | stands | 2 hits (147, 148): "You divided by 36. The standard error divides by $\sqrt{36} = 6$." <- "You divided by $\sigma\sqrt n$. The standard error divides by $\sqrt n$." / "You divided by $s/n$. The standard error divides by $\sqrt n$.". Sources: l2-measuring-surprise, l4-t-test | slip named in stock words with this part's own numbers; the source carries other numbers and another story
101. testing/problems-1.json, testing/problems-3.json | problems-1 `items[0].parts[3]`; problems-1 `items[3].parts[1]`; problems-3 `items[1].parts[1]` | [slip-line] retold | stands | 7 hits (149, 150, 151, 156, 158, 163, 164): "You doubled the tail." (identical in the source). Sources: homework-1, problems-3, review-1 | stock slip line: it names a common slip in its plain words and carries no number or story; a learner would not know it as a repeat
102. testing/problems-1.json | problems-1 `items[1].parts[4]` | [slip-line] retold | stands | 1 hit (154): "You used 2.365, the two-sided cut-off." <- "You used 1.96, the two-sided cut-off.". Sources: review-1 | slip named in stock words with this part's own numbers; the source carries other numbers and another story
103. testing/problems-4.json | problems-4 `items[1].parts[3]` | [slip-line] retold | stands | 2 hits (165, 166): "You divided the variance by the bound." (identical in the source). Sources: homework-4, l16-best-possible-precision | stock slip line: it names a common slip in its plain words and carries no number or story; a learner would not know it as a repeat
104. trig/problems-1.json | problems-1 `items[0].parts[0]`; problems-1 `items[3].parts[1]` | [slip-line] retold | stands | 6 hits (168, 169, 170, 171, 172, 173): "You subtracted the squares." (identical in the source). Sources: homework-1, l1-squares-on-sides, review-1 | stock slip line: it names a common slip in its plain words and carries no number or story; a learner would not know it as a repeat
105. trig/problems-2.json | problems-2 `items[0].parts[4]` | [slip-line] retold | stands | 1 hit (174): "You used $s = r\theta$ with $\theta$ in degrees." (identical in the source). Sources: review-2 | slip named in stock words with this part's own numbers; the source carries other numbers and another story
106. trig/problems-2.json, trig/problems-3.json | problems-2 `items[2].parts[1]`; problems-3 `items[2].parts[1]` | [slip-line] retold | stands | 2 hits (175, 176): "You turned the fraction upside down." (identical in the source); further pairs of the same feedback: "You turned the fraction upside down. From $\tfrac{2\pi}{b} = 12$, $b = \tfrac{2\pi}{12}$." <- "You turned the fraction upside down. From $\tfrac{2\pi}{b} = 20$, $b = \tfrac{2\pi}{20}$."; "You turned the fraction upside down. From $\tfrac{2\pi}{b} = 20$, $b = \tfrac{2\pi}{20}$." <- "You turned the fraction upside down. From $\tfrac{2\pi}{b} = 12$, $b = \tfrac{2\pi}{12}$.". Sources: problems-2, problems-3 | stock slip line: it names a common slip in its plain words and carries no number or story; a learner would not know it as a repeat
107. vector-calc/problems-1.json | problems-1 `items[0].parts[2]` | [slip-line] retold | stands | 3 hits (177, 178, 179): "You left out the speed $|\mathbf r'(t)| = 6$." <- "You left out the speed $\sqrt 2$:" / "You left out the speed $\sqrt2$:" / "You left out the speed $|(6, 8)| = 10$.". Sources: homework-1, l2-line-integrals, review-1 | slip named in stock words with this part's own numbers; the source carries other numbers and another story
108. vector-calc/problems-1.json | problems-1 `items[0].parts[2]` | [slip-line] retold | stands | 1 hit (180): "You integrated $|\mathbf F|^2 = 180$ instead of $|\mathbf F| = 6\sqrt5$." <- "You integrated 1 instead of $1 - t$.". Sources: l12-stokes | slip named in stock words with this part's own numbers; the source carries other numbers and another story
109. vectors/problems-2.json, vectors/problems-3.json | problems-2 `items[1].parts[1]`; problems-3 `items[2].parts[0]`; problems-3 `items[3].parts[0]` | [slip-line] retold | stands | 6 hits (181, 182, 184, 185, 187, 188): "You multiplied matching entries." (identical in the source). Sources: l7-one-after-another, problems-2, problems-3 | stock slip line: it names a common slip in its plain words and carries no number or story; a learner would not know it as a repeat

## Check of the replacements

- Every printed number of a replacement was computed twice (by hand and in Python): $2.1/75 = 0.028$; $90/80 = 1.125$, $110/100 = 1.1$, $90/120 = 0.75$; $18{,}000/24{,}000 = 0.75$; $2 + 0 + 2 + 4 + 0 + 4 = 12$, $4 + 0 + 4 + 16 + 0 + 16 = 40$, $40/6 = 6.67$; $64/50 + 64/40 + 64/20 + 64/40 = 7.68$, $4 \times 64 = 256$; $0.54 \times 5 = 2.7$, $0.54/5 = 0.108$, $0.54 \times 25 = 13.5$.
- Collision check: a search of `limits`, `stat-learning`, `testing` and every exam for the new phrases ("one rate over the other", "makes the denominator larger", "wasted hedge", "distances themselves", "squared gaps alone", "counts underneath", a Sharpe of 0.54, $\sqrt{25}$) finds none outside the lines they replace.
- The waiver block was tested in the scratch folder: with it merged into a copy of `same-course-waivers.json` (`ZQ_WAIVERS`), `same-course-reuse.mjs --all` gives 0 errors, 7 warnings and 210 waived. The 7 are the `reuse` hits.

## Engine

1. `same-course-reuse.mjs` and `retold-reuse.mjs`, `[slip-line]`: a slip line with no number, maths or story word ("You doubled the tail.", "You divided the run by the rise.", "You multiplied matching entries.", "You added the two parts.") is stock. 79 of the 189 warnings rest on one pair that is such a line (33 distinct lines; eight of them make 48 hits), and every one is waived by hand here. Do not warn when such a line is the only pair of a hit; a list in `tools/stock-slip-lines.json`, or the test "no digit, no maths, at most eight words", would do it. The same holds with an exam source: 7 of the 13 exam hits are these lines.
2. `[slip-line]` with numbers: 69 warnings pair a line with the same line in other numbers ("You multiplied the sd by 52." against "by 252."), plus 10 of the carry form "You used x, part k's slip". None is reuse. Warn only when the two lines share a number of two or more figures or a run of numbers (`p-order-sizes`: "$2 + 0 + 2 + 4$"), or when every sentence of the feedback is equal with no number masked (`p-relative-strength`, `p-rent-ridge`, `p-price-spikes`). Those three tests find all five course-source `reuse` verdicts of this list.
3. `[working-band]`: do not fire when `explain.text` prints the key at the asked places before its last figure (`stat-learning/problems-1` `p-heat-demand`: "falls from 1.80 to 1.476 but no further than $1.20 + 0.24 = 1.44$"). Keep it when the key is nowhere in the text (`coint/problems-1`: the text stops at 1,104.4 and the key is 1,105).
4. `[rounding-tie]` on a `wrong` value: skip when the band it asks for would meet another `wrong` band of the part, or when one rounding is already a `wrong` value (`trig/problems-1` `p-hexagon-tile`: 0.5 rounds to 1, which is `radians-whole`).
5. `[table-source]` reads only the words; it does not test that the key's band takes a 2-place table reading. `garch/problems-1` `p-stale-alarm` refuses both table readings (19.0% and 19.4% against a band of 19.14% to 19.26%). A check "the band takes the tail at $z$ rounded to 2 places" would find such parts.
6. A waiver keyed by line: a `source` object takes `text`, which is how the block below pins each waiver to its line. A top-level `text` on a waiver with no `source` file (clear this line of this item against any source) would make each entry one line and one reason.
7. The same-course checker does not see a shared parameter across a problem and an exam item when the story is told in other words: `p-fund-managers` (0.9 over 9 years) against `s-sharpe-p` (0.6 over 9 years) fired on the stock line alone. A `numbers` test on "x over n years" style givens of one skill would have caught it.

## Waivers for the main session

For every `stands` of list B: entries in the format of `app/tools/same-course-waivers.json`, one per set, item and kind, each source pinned to its line by `text` (the exam item by `item` for the one `text` hit). 106 entries cover the 182 hits. The file itself was not edited.

```json
[
  {
    "file": "courses/coint/problems-1.json",
    "item": "p-paper-mill-multiple",
    "kind": "retold",
    "source": [
      {
        "file": "courses/coint/l1-two-walks.json",
        "text": "You multiplied by 0.15 instead of $0.15^2$."
      },
      {
        "file": "courses/coint/review-1.json",
        "text": "You multiplied by 0.15 instead of $0.15^2$."
      }
    ],
    "reason": "stands: slip named in stock words with this part's own numbers; the source carries other numbers and another story (review-pass8-hits)"
  },
  {
    "file": "courses/coint/problems-1.json",
    "item": "p-screen-real-share",
    "kind": "retold",
    "source": {
      "file": "courses/coint/l2-not-correlation.json",
      "text": "You applied 0.40 to all 1,200 pairs."
    },
    "reason": "stands: slip named in stock words with this part's own numbers; the source carries other numbers and another story (review-pass8-hits)"
  },
  {
    "file": "courses/complex/problems-1.json",
    "item": "p-parallel-branches",
    "kind": "retold",
    "source": [
      {
        "file": "courses/complex/l1-square-root-of-minus-one.json",
        "text": "You multiplied real by real and imaginary by imaginary only."
      },
      {
        "file": "courses/complex/l2-points-in-a-plane.json",
        "text": "You added the two parts."
      },
      {
        "file": "courses/complex/problems-2.json",
        "text": "You took the real part over the imaginary part."
      }
    ],
    "reason": "stands: stock slip line: it names a common slip in its plain words and carries no number or story; a learner would not know it as a repeat (review-pass8-hits)"
  },
  {
    "file": "courses/complex/problems-1.json",
    "item": "p-turning-frames",
    "kind": "retold",
    "source": [
      {
        "file": "courses/complex/l2-points-in-a-plane.json",
        "text": "You added the two parts."
      },
      {
        "file": "courses/complex/problems-2.json",
        "text": "You took the real part over the imaginary part."
      }
    ],
    "reason": "stands: stock slip line: it names a common slip in its plain words and carries no number or story; a learner would not know it as a repeat (review-pass8-hits)"
  },
  {
    "file": "courses/complex/problems-1.json",
    "item": "p-neutral-wire",
    "kind": "retold",
    "source": [
      {
        "file": "courses/complex/l8-exp-and-log.json",
        "text": "You swapped cosine and sine."
      },
      {
        "file": "courses/complex/review-1.json",
        "text": "You swapped cosine and sine."
      },
      {
        "file": "courses/complex/l2-points-in-a-plane.json",
        "text": "You added the two parts."
      },
      {
        "file": "courses/complex/problems-2.json",
        "text": "You took the real part over the imaginary part."
      }
    ],
    "reason": "stands: stock slip line: it names a common slip in its plain words and carries no number or story; a learner would not know it as a repeat (review-pass8-hits)"
  },
  {
    "file": "courses/complex/problems-2.json",
    "item": "p-mesh-map",
    "kind": "retold",
    "source": {
      "file": "courses/complex/problems-1.json",
      "text": "You took the real part over the imaginary part."
    },
    "reason": "stands: stock slip line: it names a common slip in its plain words and carries no number or story; a learner would not know it as a repeat (review-pass8-hits)"
  },
  {
    "file": "courses/complex/problems-2.json",
    "item": "p-plate-heat",
    "kind": "retold",
    "source": [
      {
        "file": "courses/complex/l2-points-in-a-plane.json",
        "text": "You added the sizes of the parts."
      },
      {
        "file": "courses/complex/review-1.json",
        "text": "You added the sizes of the parts."
      }
    ],
    "reason": "stands: stock slip line: it names a common slip in its plain words and carries no number or story; a learner would not know it as a repeat (review-pass8-hits)"
  },
  {
    "file": "courses/complex/problems-2.json",
    "item": "p-log-branches",
    "kind": "retold",
    "source": [
      {
        "file": "courses/complex/l2-points-in-a-plane.json",
        "text": "You added the sizes of the parts."
      },
      {
        "file": "courses/complex/review-1.json",
        "text": "You added the sizes of the parts."
      }
    ],
    "reason": "stands: stock slip line: it names a common slip in its plain words and carries no number or story; a learner would not know it as a repeat (review-pass8-hits)"
  },
  {
    "file": "courses/conditional/problems-2.json",
    "item": "p-downgrade-news",
    "kind": "retold",
    "source": [
      {
        "file": "courses/conditional/l10-odds-form.json",
        "text": "You multiplied the probability 0.15 by 3."
      },
      {
        "file": "courses/conditional/l11-updating-twice.json",
        "text": "You multiplied the probability 0.15 by 3."
      },
      {
        "file": "courses/conditional/l26-trading-signal.json",
        "text": "You multiplied the probability 0.15 by 3."
      },
      {
        "file": "courses/conditional/review-2.json",
        "text": "You multiplied the probability 0.15 by 3."
      }
    ],
    "reason": "stands: slip named in stock words with this part's own numbers; the source carries other numbers and another story (review-pass8-hits)"
  },
  {
    "file": "courses/conditional/problems-3.json",
    "item": "p-gap-days",
    "kind": "retold",
    "source": {
      "file": "courses/conditional/l1-what-changes.json",
      "text": "You divided by the 260 up days."
    },
    "reason": "stands: slip named in stock words with this part's own numbers; the source carries other numbers and another story (review-pass8-hits)"
  },
  {
    "file": "courses/counting/problems-1.json",
    "item": "p-ice-cream-van",
    "kind": "retold",
    "source": {
      "file": "courses/counting/problems-2.json",
      "text": "You multiplied 14 by 3. Choosing 3 of 14 is $\\binom{14}{3}$."
    },
    "reason": "stands: slip named in stock words with this part's own numbers; the source carries other numbers and another story (review-pass8-hits)"
  },
  {
    "file": "courses/counting/problems-2.json",
    "item": "p-leisure-centre",
    "kind": "retold",
    "source": {
      "file": "courses/counting/l7-what-you-do-not-want.json",
      "text": "You took the 20 away twice."
    },
    "reason": "stands: slip named in stock words with this part's own numbers; the source carries other numbers and another story (review-pass8-hits)"
  },
  {
    "file": "courses/counting/problems-2.json",
    "item": "p-quiz-team",
    "kind": "retold",
    "source": {
      "file": "courses/counting/problems-1.json",
      "text": "You multiplied 11 by 4. Choosing 4 of 11 is $\\binom{11}{4}$."
    },
    "reason": "stands: slip named in stock words with this part's own numbers; the source carries other numbers and another story (review-pass8-hits)"
  },
  {
    "file": "courses/counting/problems-3.json",
    "item": "p-orienteering",
    "kind": "retold",
    "source": [
      {
        "file": "courses/counting/l12-proving-with-vectors.json",
        "text": "You took start minus end."
      },
      {
        "file": "courses/counting/l9-arrows.json",
        "text": "You took start minus end."
      },
      {
        "file": "courses/counting/review-3.json",
        "text": "You took start minus end."
      }
    ],
    "reason": "stands: stock slip line: it names a common slip in its plain words and carries no number or story; a learner would not know it as a repeat (review-pass8-hits)"
  },
  {
    "file": "courses/counting/problems-3.json",
    "item": "p-power-line",
    "kind": "retold",
    "source": {
      "file": "courses/counting/l11-how-long.json",
      "text": "You subtracted the components."
    },
    "reason": "stands: stock slip line: it names a common slip in its plain words and carries no number or story; a learner would not know it as a repeat (review-pass8-hits)"
  },
  {
    "file": "courses/elimination/problems-1.json",
    "item": "p-three-lines",
    "kind": "retold",
    "source": {
      "file": "courses/elimination/l3-factorisation.json",
      "text": "You put the multipliers above the diagonal."
    },
    "reason": "stands: stock slip line: it names a common slip in its plain words and carries no number or story; a learner would not know it as a repeat (review-pass8-hits)"
  },
  {
    "file": "courses/elimination/problems-3.json",
    "item": "p-vinyl-cutter",
    "kind": "retold",
    "source": [
      {
        "file": "courses/elimination/l9-area-scale.json",
        "text": "You added $bc$. The determinant is $ad - bc = 12 - 4 = 8$."
      },
      {
        "file": "courses/elimination/review-3.json",
        "text": "You added $bc$. The determinant is $ad - bc = 12 - 4 = 8$."
      }
    ],
    "reason": "stands: the slip line carries its own numbers ($12 - 4 = 8$ against $12 - 2 = 10$); \"What is the area of ...\" is the task's plain question (review-pass8-hits)"
  },
  {
    "file": "courses/ensembles/problems-2.json",
    "item": "p-ipo-forest",
    "kind": "retold",
    "source": {
      "file": "courses/ensembles/l6-random-forest.json",
      "text": "You used $\\sqrt{10} = 3.16$ before rounding down."
    },
    "reason": "stands: slip named in stock words with this part's own numbers; the source carries other numbers and another story (review-pass8-hits)"
  },
  {
    "file": "courses/equations/problems-1.json",
    "item": "p-family-tickets",
    "kind": "retold",
    "source": {
      "file": "courses/equations/l4-putting-brackets-back.json",
      "text": "You took $a$ away from 5."
    },
    "reason": "stands: slip named in stock words with this part's own numbers; the source carries other numbers and another story (review-pass8-hits)"
  },
  {
    "file": "courses/equations/problems-1.json",
    "item": "p-number-trick",
    "kind": "retold",
    "source": {
      "file": "courses/equations/l13-changing-the-subject.json",
      "text": "You divided only $2n$ by 2."
    },
    "reason": "stands: slip named in stock words with this part's own numbers; the source carries other numbers and another story (review-pass8-hits)"
  },
  {
    "file": "courses/equations/problems-2.json",
    "item": "p-climbing-wall",
    "kind": "retold",
    "source": {
      "file": "courses/equations/l1-letters-for-numbers.json",
      "text": "You swapped the two charges."
    },
    "reason": "stands: stock slip line: it names a common slip in its plain words and carries no number or story; a learner would not know it as a repeat (review-pass8-hits)"
  },
  {
    "file": "courses/equations/problems-4.json",
    "item": "p-remote-cars",
    "kind": "retold",
    "source": {
      "file": "courses/equations/l15-swapping-in.json",
      "text": "You squared 81. Here $t^2 = 81$, so undo the square instead."
    },
    "reason": "stands: slip named in stock words with this part's own numbers; the source carries other numbers and another story (review-pass8-hits)"
  },
  {
    "file": "courses/equations/problems-4.json",
    "item": "p-salt-solutions",
    "kind": "retold",
    "source": {
      "file": "courses/equations/homework-1.json",
      "text": "You multiplied 50 by 0.25. Divide instead: $50 \\div 0.25 = 200$."
    },
    "reason": "stands: slip named in stock words with this part's own numbers; the source carries other numbers and another story (review-pass8-hits)"
  },
  {
    "file": "courses/estimation/problems-1.json",
    "item": "p-route-delays",
    "kind": "retold",
    "source": {
      "file": "courses/estimation/homework-1.json",
      "text": "You added the bias, 1.5, without squaring it."
    },
    "reason": "stands: slip named in stock words with this part's own numbers; the source carries other numbers and another story (review-pass8-hits)"
  },
  {
    "file": "courses/estimation/problems-1.json",
    "item": "p-reference-mass",
    "kind": "retold",
    "source": {
      "file": "courses/estimation/problems-2.json",
      "text": "You dropped the minus signs."
    },
    "reason": "stands: stock slip line: it names a common slip in its plain words and carries no number or story; a learner would not know it as a repeat (review-pass8-hits)"
  },
  {
    "file": "courses/estimation/problems-2.json",
    "item": "p-currency-vol",
    "kind": "retold",
    "source": [
      {
        "file": "courses/estimation/problems-1.json",
        "text": "You dropped the minus signs."
      },
      {
        "file": "courses/estimation/l8-volatility-mle.json",
        "text": "You multiplied the sd by 52."
      },
      {
        "file": "exams/topic-1.6.json",
        "text": "You multiplied the sd by 52."
      }
    ],
    "reason": "stands: stock slip line: it names a common slip in its plain words and carries no number or story; a learner would not know it as a repeat; slip named in stock words with this part's own numbers; the source carries other numbers and another story; exam source: stock annualising slip with its own number (52 against 252) (review-pass8-hits)"
  },
  {
    "file": "courses/exp-log/problems-1.json",
    "item": "p-yeast-culture",
    "kind": "retold",
    "source": {
      "file": "courses/exp-log/problems-2.json",
      "text": "You raised $3000 \\times 2$ to the power."
    },
    "reason": "stands: slip named in stock words with this part's own numbers; the source carries other numbers and another story (review-pass8-hits)"
  },
  {
    "file": "courses/exp-log/problems-2.json",
    "item": "p-fault-search",
    "kind": "retold",
    "source": {
      "file": "courses/exp-log/review-2.json",
      "text": "You multiplied the logs, $5 \\times 11$."
    },
    "reason": "stands: slip named in stock words with this part's own numbers; the source carries other numbers and another story (review-pass8-hits)"
  },
  {
    "file": "courses/exp-log/problems-2.json",
    "item": "p-app-users",
    "kind": "retold",
    "source": {
      "file": "courses/exp-log/problems-1.json",
      "text": "You raised $2000 \\times 1.3$ to the power."
    },
    "reason": "stands: slip named in stock words with this part's own numbers; the source carries other numbers and another story (review-pass8-hits)"
  },
  {
    "file": "courses/fin-ml/problems-3.json",
    "item": "p-power-spread-cap",
    "kind": "text",
    "source": {
      "file": "exams/topic-2.1.json",
      "item": "e-kelly-odds"
    },
    "reason": "stands: exam source: the shared words are the given of a bet with odds in its natural words (\"a win pays £b per £1 staked and a loss costs the £1\"); own $p = 0.70$ and $b = 0.8$ against 0.5 and 1.5; parts 2 to 5 (log growth, cap, doubling time, plan stage) are not in the exam item (review-pass8-hits)"
  },
  {
    "file": "courses/functions/problems-2.json",
    "item": "p-candle-burn",
    "kind": "retold",
    "source": [
      {
        "file": "courses/functions/homework-2.json",
        "text": "You divided the run by the rise."
      },
      {
        "file": "courses/functions/l6-how-steep.json",
        "text": "You divided the run by the rise."
      },
      {
        "file": "courses/functions/l7-slope-and-start.json",
        "text": "You divided the run by the rise."
      },
      {
        "file": "courses/functions/l8-line-through-two-points.json",
        "text": "You divided the run by the rise."
      },
      {
        "file": "courses/functions/review-2.json",
        "text": "You divided the run by the rise."
      },
      {
        "file": "exams/topic-0.2.json",
        "text": "You divided the run by the rise."
      }
    ],
    "reason": "stands: stock slip line: it names a common slip in its plain words and carries no number or story; a learner would not know it as a repeat; exam source: stock slip line of the course (it stands in six units); no number, no story (review-pass8-hits)"
  },
  {
    "file": "courses/functions/problems-2.json",
    "item": "p-path-and-pipe",
    "kind": "retold",
    "source": [
      {
        "file": "courses/functions/homework-2.json",
        "text": "You divided the run by the rise."
      },
      {
        "file": "courses/functions/l6-how-steep.json",
        "text": "You divided the run by the rise."
      },
      {
        "file": "courses/functions/l7-slope-and-start.json",
        "text": "You divided the run by the rise."
      },
      {
        "file": "courses/functions/l8-line-through-two-points.json",
        "text": "You divided the run by the rise."
      },
      {
        "file": "courses/functions/review-2.json",
        "text": "You divided the run by the rise."
      },
      {
        "file": "exams/topic-0.2.json",
        "text": "You divided the run by the rise."
      }
    ],
    "reason": "stands: stock slip line: it names a common slip in its plain words and carries no number or story; a learner would not know it as a repeat; exam source: stock slip line of the course (it stands in six units); no number, no story (review-pass8-hits)"
  },
  {
    "file": "courses/garch/problems-2.json",
    "item": "p-two-filters-one-score",
    "kind": "retold",
    "source": {
      "file": "courses/garch/problems-3.json",
      "text": "You worked in decimals."
    },
    "reason": "stands: stock slip line: it names a common slip in its plain words and carries no number or story; a learner would not know it as a repeat (review-pass8-hits)"
  },
  {
    "file": "courses/garch/problems-2.json",
    "item": "p-weekly-gas-arch",
    "kind": "retold",
    "source": [
      {
        "file": "courses/garch/review-2.json",
        "text": "You gave 0.80 to the squared return."
      },
      {
        "file": "courses/garch/problems-3.json",
        "text": "You gave it in decimals."
      }
    ],
    "reason": "stands: slip named in stock words with this part's own numbers; the source carries other numbers and another story; stock slip line: it names a common slip in its plain words and carries no number or story; a learner would not know it as a repeat (review-pass8-hits)"
  },
  {
    "file": "courses/garch/problems-2.json",
    "item": "p-silver-moment-fit",
    "kind": "retold",
    "source": [
      {
        "file": "courses/garch/l6-arch.json",
        "text": "You used $0.13 \\times 4.5$ rather than $0.13 \\times 4.5^2$."
      },
      {
        "file": "courses/garch/review-2.json",
        "text": "You used $0.13 \\times 4.5$ rather than $0.13 \\times 4.5^2$."
      }
    ],
    "reason": "stands: slip named in stock words with this part's own numbers; the source carries other numbers and another story (review-pass8-hits)"
  },
  {
    "file": "courses/garch/problems-2.json",
    "item": "p-crash-then-quiet",
    "kind": "retold",
    "source": {
      "file": "courses/garch/problems-3.json",
      "text": "You gave it in decimals."
    },
    "reason": "stands: stock slip line: it names a common slip in its plain words and carries no number or story; a learner would not know it as a repeat (review-pass8-hits)"
  },
  {
    "file": "courses/garch/problems-3.json",
    "item": "p-forecasts-to-parameters",
    "kind": "retold",
    "source": {
      "file": "courses/garch/problems-2.json",
      "text": "You worked in decimals."
    },
    "reason": "stands: stock slip line: it names a common slip in its plain words and carries no number or story; a learner would not know it as a repeat (review-pass8-hits)"
  },
  {
    "file": "courses/garch/problems-3.json",
    "item": "p-monthly-sleeve",
    "kind": "retold",
    "source": {
      "file": "courses/garch/problems-2.json",
      "text": "You gave it in decimals."
    },
    "reason": "stands: stock slip line: it names a common slip in its plain words and carries no number or story; a learner would not know it as a repeat (review-pass8-hits)"
  },
  {
    "file": "courses/integrals/problems-2.json",
    "item": "p-line-and-parabola",
    "kind": "retold",
    "source": {
      "file": "courses/integrals/review-2.json",
      "text": "You took parabola minus line."
    },
    "reason": "stands: stock slip line: it names a common slip in its plain words and carries no number or story; a learner would not know it as a repeat (review-pass8-hits)"
  },
  {
    "file": "courses/integrals/problems-3.json",
    "item": "p-order-size-tail",
    "kind": "retold",
    "source": {
      "file": "courses/integrals/l6-working-backwards.json",
      "text": "You lowered the power."
    },
    "reason": "stands: stock slip line: it names a common slip in its plain words and carries no number or story; a learner would not know it as a repeat (review-pass8-hits)"
  },
  {
    "file": "courses/integrals/problems-3.json",
    "item": "p-time-to-fill",
    "kind": "retold",
    "source": [
      {
        "file": "courses/integrals/l10-undo-product.json",
        "text": "You took $v = e^{-x}$. Its derivative is $-e^{-x}$, so $v = -e^{-x}$."
      },
      {
        "file": "courses/integrals/review-3.json",
        "text": "You took $v = e^{-x}$. Its derivative is $-e^{-x}$, so $v = -e^{-x}$."
      }
    ],
    "reason": "stands: slip named in stock words with this part's own numbers; the source carries other numbers and another story (review-pass8-hits)"
  },
  {
    "file": "courses/limits/problems-2.json",
    "item": "p-inventory-penalty",
    "kind": "retold",
    "source": {
      "file": "courses/limits/problems-5.json",
      "text": "You dropped the 0.5 in front of $q^2$."
    },
    "reason": "stands: slip named in stock words with this part's own numbers; the source carries other numbers and another story (review-pass8-hits)"
  },
  {
    "file": "courses/limits/problems-3.json",
    "item": "p-research-price",
    "kind": "retold",
    "source": [
      {
        "file": "courses/limits/l11-standard-derivatives.json",
        "text": "You left out the inside's derivative, $-1$."
      },
      {
        "file": "courses/limits/l7-power-rule.json",
        "text": "You multiplied the two derivatives, $1 \\times (-60)$."
      }
    ],
    "reason": "stands: slip named in stock words with this part's own numbers; the source carries other numbers and another story (review-pass8-hits)"
  },
  {
    "file": "courses/limits/problems-3.json",
    "item": "p-gas-season",
    "kind": "retold",
    "source": [
      {
        "file": "courses/limits/l11-standard-derivatives.json",
        "text": "You left out the inside's derivative, $\\tfrac{\\pi}{6}$."
      },
      {
        "file": "courses/limits/l7-power-rule.json",
        "text": "You multiplied the two derivatives, $5 \\times (-0.05\\pi)$."
      }
    ],
    "reason": "stands: slip named in stock words with this part's own numbers; the source carries other numbers and another story (review-pass8-hits)"
  },
  {
    "file": "courses/limits/problems-5.json",
    "item": "p-impact-curve",
    "kind": "retold",
    "source": {
      "file": "courses/limits/problems-2.json",
      "text": "You dropped the 2 in front of $\\arctan$."
    },
    "reason": "stands: slip named in stock words with this part's own numbers; the source carries other numbers and another story (review-pass8-hits)"
  },
  {
    "file": "courses/limits-thm/problems-2.json",
    "item": "p-digital-share",
    "kind": "retold",
    "source": [
      {
        "file": "courses/limits-thm/homework-2.json",
        "text": "You used $0.06 + 0.045$ as the log drift."
      },
      {
        "file": "courses/limits-thm/l8-lognormal.json",
        "text": "You used $0.06 + 0.045$ as the log drift."
      },
      {
        "file": "courses/limits-thm/review-2.json",
        "text": "You used $0.06 + 0.045$ as the log drift."
      }
    ],
    "reason": "stands: slip named in stock words with this part's own numbers; the source carries other numbers and another story (review-pass8-hits)"
  },
  {
    "file": "courses/limits-thm/problems-3.json",
    "item": "p-direction-calls",
    "kind": "retold",
    "source": {
      "file": "courses/limits-thm/l12-skill-or-luck.json",
      "text": "You added 12 chances of 0.0606."
    },
    "reason": "stands: slip named in stock words with this part's own numbers; the source carries other numbers and another story (review-pass8-hits)"
  },
  {
    "file": "courses/limits-thm/problems-3.json",
    "item": "p-rejected-orders",
    "kind": "retold",
    "source": {
      "file": "courses/limits-thm/l10-bound-that-holds.json",
      "text": "You divided the threshold by the mean."
    },
    "reason": "stands: stock slip line: it names a common slip in its plain words and carries no number or story; a learner would not know it as a repeat (review-pass8-hits)"
  },
  {
    "file": "courses/limits-thm/problems-3.json",
    "item": "p-fund-months",
    "kind": "retold",
    "source": {
      "file": "courses/limits-thm/l12-skill-or-luck.json",
      "text": "You divided the standard error by the average."
    },
    "reason": "stands: stock slip line: it names a common slip in its plain words and carries no number or story; a learner would not know it as a repeat (review-pass8-hits)"
  },
  {
    "file": "courses/linear-maps/problems-1.json",
    "item": "p-scenario-space",
    "kind": "retold",
    "source": {
      "file": "courses/linear-maps/l1-axioms.json",
      "text": "You took the usual zero."
    },
    "reason": "stands: stock slip line: it names a common slip in its plain words and carries no number or story; a learner would not know it as a repeat (review-pass8-hits)"
  },
  {
    "file": "courses/linear-maps/problems-2.json",
    "item": "p-futures-exposure",
    "kind": "retold",
    "source": {
      "file": "courses/linear-maps/homework-2.json",
      "text": "You wrote the coordinates as rows."
    },
    "reason": "stands: stock slip line: it names a common slip in its plain words and carries no number or story; a learner would not know it as a repeat (review-pass8-hits)"
  },
  {
    "file": "courses/multivar/problems-2.json",
    "item": "p-slopes-around",
    "kind": "retold",
    "source": [
      {
        "file": "courses/multivar/l5-steepest-climb.json",
        "text": "You added the components."
      },
      {
        "file": "courses/multivar/review-2.json",
        "text": "You added the components."
      }
    ],
    "reason": "stands: \"You added the components.\" is stock; the question and the explain line state the fact $|\\nabla f|$ is the steepest slope in its natural words, with own gradient (12, 9) (review-pass8-hits)"
  },
  {
    "file": "courses/multivar/problems-3.json",
    "item": "p-min-variance-pair",
    "kind": "retold",
    "source": [
      {
        "file": "exams/topic-1.3.json",
        "text": "Asset A has volatility 40% and asset B 25%, with correlation 0.3."
      },
      {
        "file": "courses/multivar/l12-min-variance.json",
        "text": "You solved $0.1625w - 0.065 = 0$. The derivative of $0.1625w^2$ is $0.325w$."
      }
    ],
    "reason": "stands: exam source: the stem is the given of a two-asset problem in its natural words with own numbers (40%, 25%, 0.3 against 30%, 15%, 0.25; key 0.2 against 0.125); the slip lines differ in wording; the factor-of-two slip in its plain words with this parabola's own coefficients (review-pass8-hits)"
  },
  {
    "file": "courses/multivar/problems-4.json",
    "item": "p-corner-sprinkler",
    "kind": "retold",
    "source": {
      "file": "courses/multivar/problems-5.json",
      "text": "You wrote $x^2 + y^2$ as $r$. It is $r^2$."
    },
    "reason": "stands: slip named in stock words with this part's own numbers; the source carries other numbers and another story (review-pass8-hits)"
  },
  {
    "file": "courses/multivar/problems-4.json",
    "item": "p-drone-landing",
    "kind": "retold",
    "source": {
      "file": "courses/multivar/l13-volume.json",
      "text": "You added the two single integrals."
    },
    "reason": "stands: stock slip line: it names a common slip in its plain words and carries no number or story; a learner would not know it as a repeat (review-pass8-hits)"
  },
  {
    "file": "courses/multivar/problems-5.json",
    "item": "p-dome-tent",
    "kind": "retold",
    "source": {
      "file": "courses/multivar/problems-4.json",
      "text": "You wrote $(2u)^2$ as $2u^2$. It is $4u^2$."
    },
    "reason": "stands: slip named in stock words with this part's own numbers; the source carries other numbers and another story (review-pass8-hits)"
  },
  {
    "file": "courses/number-sense/problems-1.json",
    "item": "p-garden-beds",
    "kind": "retold",
    "source": [
      {
        "file": "courses/number-sense/l3-adding-pieces.json",
        "text": "You added the tops and the bottoms to get $\\tfrac{3}{9}$."
      },
      {
        "file": "courses/number-sense/review-1.json",
        "text": "You added the tops and the bottoms to get $\\tfrac{3}{9}$."
      }
    ],
    "reason": "stands: slip named in stock words with this part's own numbers; the source carries other numbers and another story (review-pass8-hits)"
  },
  {
    "file": "courses/number-sense/problems-1.json",
    "item": "p-squash-jugs",
    "kind": "retold",
    "source": [
      {
        "file": "courses/number-sense/homework-1.json",
        "text": "You added 27 to the top and the bottom."
      },
      {
        "file": "courses/number-sense/l2-same-amount.json",
        "text": "You added 27 to the top and the bottom."
      },
      {
        "file": "courses/number-sense/review-1.json",
        "text": "You added the two fractions."
      },
      {
        "file": "courses/number-sense/l4-fraction-of-fraction.json",
        "text": "You added the two fractions."
      }
    ],
    "reason": "stands: slip named in stock words with this part's own numbers; the source carries other numbers and another story; stock slip line: it names a common slip in its plain words and carries no number or story; a learner would not know it as a repeat (review-pass8-hits)"
  },
  {
    "file": "courses/number-sense/problems-3.json",
    "item": "p-cube-tub",
    "kind": "retold",
    "source": {
      "file": "courses/number-sense/l11-undoing-a-square.json",
      "text": "You took the square root."
    },
    "reason": "stands: stock slip line: it names a common slip in its plain words and carries no number or story; a learner would not know it as a repeat (review-pass8-hits)"
  },
  {
    "file": "courses/number-sense/problems-3.json",
    "item": "p-comet-probe",
    "kind": "retold",
    "source": [
      {
        "file": "courses/number-sense/homework-4.json",
        "text": "You added the indices."
      },
      {
        "file": "courses/number-sense/l10-repeated-multiplication.json",
        "text": "You added the indices."
      },
      {
        "file": "courses/number-sense/l14-very-big-very-small.json",
        "text": "You added the indices."
      },
      {
        "file": "courses/number-sense/review-3.json",
        "text": "You added the indices."
      }
    ],
    "reason": "stands: stock slip line: it names a common slip in its plain words and carries no number or story; a learner would not know it as a repeat (review-pass8-hits)"
  },
  {
    "file": "courses/number-sense/problems-4.json",
    "item": "p-hall-tiles",
    "kind": "retold",
    "source": {
      "file": "courses/number-sense/review-4.json",
      "text": "You multiplied the indices, $3 \\times 1 \\times 1$."
    },
    "reason": "stands: slip named in stock words with this part's own numbers; the source carries other numbers and another story (review-pass8-hits)"
  },
  {
    "file": "courses/number-sense/problems-4.json",
    "item": "p-cycle-commute",
    "kind": "retold",
    "source": [
      {
        "file": "courses/number-sense/l18-circles-and-units.json",
        "text": "You multiplied by 3,600 and divided by 1,000."
      },
      {
        "file": "courses/number-sense/review-4.json",
        "text": "You multiplied by 3,600 and divided by 1,000."
      }
    ],
    "reason": "stands: slip named in stock words with this part's own numbers; the source carries other numbers and another story (review-pass8-hits)"
  },
  {
    "file": "courses/odes/problems-3.json",
    "item": "p-liquidity-arbitrage",
    "kind": "retold",
    "source": {
      "file": "courses/odes/l13-linearising.json",
      "text": "You swapped the coordinates."
    },
    "reason": "stands: stock slip line: it names a common slip in its plain words and carries no number or story; a learner would not know it as a repeat (review-pass8-hits)"
  },
  {
    "file": "courses/quadratics/problems-1.json",
    "item": "p-cinema-block",
    "kind": "retold",
    "source": {
      "file": "courses/quadratics/l1-two-brackets.json",
      "text": "You added 4 and 11 for the corner."
    },
    "reason": "stands: slip named in stock words with this part's own numbers; the source carries other numbers and another story (review-pass8-hits)"
  },
  {
    "file": "courses/random-vars/problems-1.json",
    "item": "p-straddle-days",
    "kind": "retold",
    "source": {
      "file": "courses/random-vars/problems-3.json",
      "text": "You used $c = 0.85$ from part 1's slip."
    },
    "reason": "stands: the carry line's fixed form (\"You used x, part k's slip\") with this problem's own value (review-pass8-hits)"
  },
  {
    "file": "courses/random-vars/problems-2.json",
    "item": "p-reversal-days",
    "kind": "retold",
    "source": {
      "file": "courses/random-vars/l8-indicators.json",
      "text": "You treated up and down as equally likely."
    },
    "reason": "stands: stock slip line: it names a common slip in its plain words and carries no number or story; a learner would not know it as a repeat (review-pass8-hits)"
  },
  {
    "file": "courses/random-vars/problems-3.json",
    "item": "p-quote-trades",
    "kind": "retold",
    "source": {
      "file": "courses/random-vars/l10-scaling-and-adding.json",
      "text": "You multiplied the sd by 100."
    },
    "reason": "stands: slip named in stock words with this part's own numbers; the source carries other numbers and another story (review-pass8-hits)"
  },
  {
    "file": "courses/random-vars/problems-3.json",
    "item": "p-fund-hedge",
    "kind": "retold",
    "source": {
      "file": "courses/random-vars/problems-1.json",
      "text": "You used $E[AB] = 2.0$ from part 3's slip."
    },
    "reason": "stands: the carry line's fixed form (\"You used x, part k's slip\") with this problem's own value (review-pass8-hits)"
  },
  {
    "file": "courses/random-vars/problems-4.json",
    "item": "p-file-retry",
    "kind": "retold",
    "source": {
      "file": "courses/random-vars/problems-5.json",
      "text": "You used $m = 2.1$, part 2's slip."
    },
    "reason": "stands: the carry line's fixed form (\"You used x, part k's slip\") with this problem's own value (review-pass8-hits)"
  },
  {
    "file": "courses/random-vars/problems-5.json",
    "item": "p-startup-rounds",
    "kind": "retold",
    "source": {
      "file": "courses/random-vars/problems-4.json",
      "text": "You used $\\ln 1.05$, part 1's slip."
    },
    "reason": "stands: the carry line's fixed form (\"You used x, part k's slip\") with this problem's own value (review-pass8-hits)"
  },
  {
    "file": "courses/ratio/problems-1.json",
    "item": "p-platform-fee",
    "kind": "retold",
    "source": {
      "file": "courses/ratio/l1-out-of-a-hundred.json",
      "text": "You moved the point one place."
    },
    "reason": "stands: stock slip line: it names a common slip in its plain words and carries no number or story; a learner would not know it as a repeat (review-pass8-hits)"
  },
  {
    "file": "courses/ratio/problems-1.json",
    "item": "p-phone-rise",
    "kind": "retold",
    "source": {
      "file": "courses/ratio/l1-out-of-a-hundred.json",
      "text": "You moved the point one place."
    },
    "reason": "stands: stock slip line: it names a common slip in its plain words and carries no number or story; a learner would not know it as a repeat (review-pass8-hits)"
  },
  {
    "file": "courses/ratio/problems-3.json",
    "item": "p-partners-profit",
    "kind": "retold",
    "source": [
      {
        "file": "courses/ratio/homework-3.json",
        "text": "You treated £2,850 as one part."
      },
      {
        "file": "courses/ratio/l9-sharing.json",
        "text": "You treated £2,850 as one part."
      }
    ],
    "reason": "stands: slip named in stock words with this part's own numbers; the source carries other numbers and another story (review-pass8-hits)"
  },
  {
    "file": "courses/regression/problems-1.json",
    "item": "p-stopping-distances",
    "kind": "retold",
    "source": {
      "file": "courses/regression/problems-3.json",
      "text": "You left out the intercept $-21.4$."
    },
    "reason": "stands: both lines are stock (an intercept left out; the definition of a residual) with own numbers (review-pass8-hits)"
  },
  {
    "file": "courses/regression/problems-2.json",
    "item": "p-sunny-cones",
    "kind": "retold",
    "source": {
      "file": "courses/regression/l5-how-sure.json",
      "text": "You divided by 64 itself."
    },
    "reason": "stands: slip named in stock words with this part's own numbers; the source carries other numbers and another story (review-pass8-hits)"
  },
  {
    "file": "courses/regression/problems-3.json",
    "item": "p-bond-fund-weeks",
    "kind": "retold",
    "source": {
      "file": "courses/regression/problems-1.json",
      "text": "You left out the intercept, 0.05."
    },
    "reason": "stands: slip named in stock words with this part's own numbers; the source carries other numbers and another story (review-pass8-hits)"
  },
  {
    "file": "courses/series/problems-1.json",
    "item": "p-pendulum-swings",
    "kind": "retold",
    "source": [
      {
        "file": "courses/series/homework-1.json",
        "text": "You raised $80 \\times 0.9$ to the power."
      },
      {
        "file": "courses/series/l3-multiplying-each-time.json",
        "text": "You raised $80 \\times 0.9$ to the power."
      }
    ],
    "reason": "stands: slip named in stock words with this part's own numbers; the source carries other numbers and another story (review-pass8-hits)"
  },
  {
    "file": "courses/stat-learning/problems-1.json",
    "item": "p-loaves-k",
    "kind": "retold",
    "source": [
      {
        "file": "courses/stat-learning/review-1.json",
        "text": "You left out the noise."
      },
      {
        "file": "courses/stat-learning/homework-1.json",
        "text": "You divided by 4 for the variance."
      }
    ],
    "reason": "stands: stock slip line: it names a common slip in its plain words and carries no number or story; a learner would not know it as a repeat; the divisor slip with its own divisor (5 against 4), and a stock line (review-pass8-hits)"
  },
  {
    "file": "courses/stat-learning/problems-2.json",
    "item": "p-built-ridge",
    "kind": "retold",
    "source": [
      {
        "file": "courses/stat-learning/problems-3.json",
        "text": "You used 0.515, part 3's slip."
      },
      {
        "file": "courses/stat-learning/problems-4.json",
        "text": "You used 0.515, part 3's slip."
      }
    ],
    "reason": "stands: the carry line's fixed form (\"You used x, part k's slip\") with this problem's own value (review-pass8-hits)"
  },
  {
    "file": "courses/stat-learning/problems-3.json",
    "item": "p-order-fill",
    "kind": "retold",
    "source": {
      "file": "courses/stat-learning/review-3.json",
      "text": "You multiplied the probability by 0.407."
    },
    "reason": "stands: the odds slip with its own factor 0.407; \"the factor applies to the odds\" is the fact in its natural words (review-pass8-hits)"
  },
  {
    "file": "courses/stat-learning/problems-3.json",
    "item": "p-sterling-calls",
    "kind": "retold",
    "source": {
      "file": "courses/stat-learning/problems-4.json",
      "text": "You compared with a coin's 0.5."
    },
    "reason": "stands: slip named in stock words with this part's own numbers; the source carries other numbers and another story (review-pass8-hits)"
  },
  {
    "file": "courses/stat-learning/problems-3.json",
    "item": "p-price-spikes",
    "kind": "retold",
    "source": [
      {
        "file": "courses/stat-learning/problems-2.json",
        "text": "You used £1,080, part 4's slip."
      },
      {
        "file": "courses/stat-learning/problems-4.json",
        "text": "You used £1,080, part 4's slip."
      }
    ],
    "reason": "stands: the carry line's fixed form (\"You used x, part k's slip\") with this problem's own value (review-pass8-hits)"
  },
  {
    "file": "courses/stat-learning/problems-4.json",
    "item": "p-spam-filter",
    "kind": "retold",
    "source": {
      "file": "courses/stat-learning/problems-3.json",
      "text": "You compared with a coin's 0.5."
    },
    "reason": "stands: slip named in stock words with this part's own numbers; the source carries other numbers and another story (review-pass8-hits)"
  },
  {
    "file": "courses/stat-learning/problems-4.json",
    "item": "p-order-sizes",
    "kind": "retold",
    "source": {
      "file": "courses/stat-learning/l18-bending-the-line.json",
      "text": "You left out the hinge."
    },
    "reason": "stands: stock slip line: it names a common slip in its plain words and carries no number or story; a learner would not know it as a repeat (review-pass8-hits)"
  },
  {
    "file": "courses/stat-learning/problems-4.json",
    "item": "p-one-unit",
    "kind": "retold",
    "source": [
      {
        "file": "courses/stat-learning/problems-2.json",
        "text": "You used $\\hat y = 9$, part 1's slip."
      },
      {
        "file": "courses/stat-learning/problems-3.json",
        "text": "You used $\\hat y = 9$, part 1's slip."
      }
    ],
    "reason": "stands: the carry line's fixed form (\"You used x, part k's slip\") with this problem's own value (review-pass8-hits)"
  },
  {
    "file": "courses/stat-learning/problems-4.json",
    "item": "p-renewals",
    "kind": "retold",
    "source": {
      "file": "courses/stat-learning/problems-3.json",
      "text": "You compared with a coin's 0.5."
    },
    "reason": "stands: slip named in stock words with this part's own numbers; the source carries other numbers and another story (review-pass8-hits)"
  },
  {
    "file": "courses/taylor/problems-2.json",
    "item": "p-three-halves",
    "kind": "retold",
    "source": {
      "file": "courses/taylor/l6-matching-derivatives.json",
      "text": "You divided by 3. The coefficient divides by $3! = 6$."
    },
    "reason": "stands: slip named in stock words with this part's own numbers; the source carries other numbers and another story (review-pass8-hits)"
  },
  {
    "file": "courses/taylor/problems-2.json",
    "item": "p-square-geometric",
    "kind": "retold",
    "source": {
      "file": "courses/taylor/l6-matching-derivatives.json",
      "text": "You divided by 3. The coefficient divides by $3! = 6$."
    },
    "reason": "stands: slip named in stock words with this part's own numbers; the source carries other numbers and another story (review-pass8-hits)"
  },
  {
    "file": "courses/taylor/problems-2.json",
    "item": "p-log-two",
    "kind": "retold",
    "source": {
      "file": "courses/taylor/l6-matching-derivatives.json",
      "text": "You divided by 3. The coefficient divides by $3! = 6$."
    },
    "reason": "stands: slip named in stock words with this part's own numbers; the source carries other numbers and another story (review-pass8-hits)"
  },
  {
    "file": "courses/taylor/problems-3.json",
    "item": "p-two-months",
    "kind": "retold",
    "source": {
      "file": "courses/taylor/l2-how-wrong.json",
      "text": "You divided by $3! = 6$, as for $e^x$."
    },
    "reason": "stands: slip named in stock words with this part's own numbers; the source carries other numbers and another story (review-pass8-hits)"
  },
  {
    "file": "courses/taylor/problems-3.json",
    "item": "p-big-gain",
    "kind": "retold",
    "source": {
      "file": "courses/taylor/l2-how-wrong.json",
      "text": "You divided by $k!$, as for $e^x$."
    },
    "reason": "stands: slip named in stock words with this part's own numbers; the source carries other numbers and another story (review-pass8-hits)"
  },
  {
    "file": "courses/testing/problems-1.json",
    "item": "p-cereal-boxes",
    "kind": "retold",
    "source": [
      {
        "file": "courses/testing/l2-measuring-surprise.json",
        "text": "You divided by 36. The standard error divides by $\\sqrt{36} = 6$."
      },
      {
        "file": "courses/testing/l4-t-test.json",
        "text": "You divided by 36. The standard error divides by $\\sqrt{36} = 6$."
      },
      {
        "file": "courses/testing/homework-1.json",
        "text": "You doubled the tail."
      },
      {
        "file": "courses/testing/problems-3.json",
        "text": "You doubled the tail."
      },
      {
        "file": "courses/testing/review-1.json",
        "text": "You doubled the tail."
      },
      {
        "file": "exams/topic-1.6.json",
        "text": "You doubled the tail."
      }
    ],
    "reason": "stands: slip named in stock words with this part's own numbers; the source carries other numbers and another story; stock slip line: it names a common slip in its plain words and carries no number or story; a learner would not know it as a repeat; exam source: stock slip line of the course (12 hits); the exam item is a Sharpe p-value, this part a z test on cereal boxes (review-pass8-hits)"
  },
  {
    "file": "courses/testing/problems-1.json",
    "item": "p-phone-battery",
    "kind": "retold",
    "source": [
      {
        "file": "courses/testing/problems-2.json",
        "text": "You divided the total, 144, by 7."
      },
      {
        "file": "courses/testing/review-1.json",
        "text": "You used 2.365, the two-sided cut-off."
      },
      {
        "file": "exams/topic-1.6.json",
        "text": "You used 2.365, the two-sided cut-off."
      }
    ],
    "reason": "stands: seven pairs, all between the one-sample test of level 1 and the paired test of level 2. A paired test is the one-sample test on the differences, so mean, sd and $t$ and their slips are the method. Data, story, null and cut-off differ, and `p-running-shoes` parts 4 and 5 (pairing against Welch, power) are new; slip named in stock words with this part's own numbers; the source carries other numbers and another story; exam source: stock slip with its own cut-off (2.365 against 1.96); the tasks differ (smallest advert rejected against a sample size) (review-pass8-hits)"
  },
  {
    "file": "courses/testing/problems-1.json",
    "item": "p-pizza-delivery",
    "kind": "retold",
    "source": [
      {
        "file": "courses/testing/homework-1.json",
        "text": "You doubled the tail."
      },
      {
        "file": "courses/testing/problems-3.json",
        "text": "You doubled the tail."
      },
      {
        "file": "courses/testing/review-1.json",
        "text": "You doubled the tail."
      },
      {
        "file": "exams/topic-1.6.json",
        "text": "You doubled the tail."
      }
    ],
    "reason": "stands: stock slip line: it names a common slip in its plain words and carries no number or story; a learner would not know it as a repeat; stock line, and \"the upper tail beyond\" is the standard phrase for a one-sided p-value (waived before for this course); exam source: stock slip line of the course (12 hits); the exam item is a Sharpe p-value, this part a z test on cereal boxes (review-pass8-hits)"
  },
  {
    "file": "courses/testing/problems-2.json",
    "item": "p-running-shoes",
    "kind": "retold",
    "source": {
      "file": "courses/testing/problems-1.json",
      "text": "You divided the total, $-36$, by 8."
    },
    "reason": "stands: seven pairs, all between the one-sample test of level 1 and the paired test of level 2. A paired test is the one-sample test on the differences, so mean, sd and $t$ and their slips are the method. Data, story, null and cut-off differ, and `p-running-shoes` parts 4 and 5 (pairing against Welch, power) are new (review-pass8-hits)"
  },
  {
    "file": "courses/testing/problems-3.json",
    "item": "p-fund-managers",
    "kind": "retold",
    "source": [
      {
        "file": "courses/testing/problems-1.json",
        "text": "You doubled the tail."
      },
      {
        "file": "courses/testing/homework-1.json",
        "text": "You doubled the tail."
      },
      {
        "file": "courses/testing/review-1.json",
        "text": "You doubled the tail."
      }
    ],
    "reason": "stands: stock line, and \"the upper tail beyond\" is the standard phrase for a one-sided p-value (waived before for this course); stock slip line: it names a common slip in its plain words and carries no number or story; a learner would not know it as a repeat (review-pass8-hits)"
  },
  {
    "file": "courses/testing/problems-4.json",
    "item": "p-website-signups",
    "kind": "retold",
    "source": [
      {
        "file": "courses/testing/homework-4.json",
        "text": "You divided the variance by the bound."
      },
      {
        "file": "courses/testing/l16-best-possible-precision.json",
        "text": "You divided the variance by the bound."
      }
    ],
    "reason": "stands: stock slip line: it names a common slip in its plain words and carries no number or story; a learner would not know it as a repeat (review-pass8-hits)"
  },
  {
    "file": "courses/trig/problems-1.json",
    "item": "p-zip-wire",
    "kind": "retold",
    "source": [
      {
        "file": "courses/trig/homework-1.json",
        "text": "You subtracted the squares."
      },
      {
        "file": "courses/trig/l1-squares-on-sides.json",
        "text": "You subtracted the squares."
      },
      {
        "file": "courses/trig/review-1.json",
        "text": "You subtracted the squares."
      }
    ],
    "reason": "stands: stock slip line: it names a common slip in its plain words and carries no number or story; a learner would not know it as a repeat (review-pass8-hits)"
  },
  {
    "file": "courses/trig/problems-1.json",
    "item": "p-desk-lamp",
    "kind": "retold",
    "source": [
      {
        "file": "courses/trig/homework-1.json",
        "text": "You subtracted the squares."
      },
      {
        "file": "courses/trig/l1-squares-on-sides.json",
        "text": "You subtracted the squares."
      },
      {
        "file": "courses/trig/review-1.json",
        "text": "You subtracted the squares."
      }
    ],
    "reason": "stands: stock slip line: it names a common slip in its plain words and carries no number or story; a learner would not know it as a repeat (review-pass8-hits)"
  },
  {
    "file": "courses/trig/problems-2.json",
    "item": "p-water-wheel",
    "kind": "retold",
    "source": {
      "file": "courses/trig/review-2.json",
      "text": "You used $s = r\\theta$ with $\\theta$ in degrees."
    },
    "reason": "stands: slip named in stock words with this part's own numbers; the source carries other numbers and another story (review-pass8-hits)"
  },
  {
    "file": "courses/trig/problems-2.json",
    "item": "p-observation-wheel",
    "kind": "retold",
    "source": {
      "file": "courses/trig/problems-3.json",
      "text": "You turned the fraction upside down."
    },
    "reason": "stands: stock slip line: it names a common slip in its plain words and carries no number or story; a learner would not know it as a repeat (review-pass8-hits)"
  },
  {
    "file": "courses/trig/problems-3.json",
    "item": "p-daylight-model",
    "kind": "retold",
    "source": {
      "file": "courses/trig/problems-2.json",
      "text": "You turned the fraction upside down."
    },
    "reason": "stands: stock slip line: it names a common slip in its plain words and carries no number or story; a learner would not know it as a repeat (review-pass8-hits)"
  },
  {
    "file": "courses/vector-calc/problems-1.json",
    "item": "p-bead-semicircle",
    "kind": "retold",
    "source": [
      {
        "file": "courses/vector-calc/homework-1.json",
        "text": "You left out the speed $|\\mathbf r'(t)| = 6$."
      },
      {
        "file": "courses/vector-calc/l2-line-integrals.json",
        "text": "You left out the speed $|\\mathbf r'(t)| = 6$."
      },
      {
        "file": "courses/vector-calc/review-1.json",
        "text": "You left out the speed $|\\mathbf r'(t)| = 6$."
      },
      {
        "file": "courses/vector-calc/l12-stokes.json",
        "text": "You integrated $|\\mathbf F|^2 = 180$ instead of $|\\mathbf F| = 6\\sqrt5$."
      }
    ],
    "reason": "stands: slip named in stock words with this part's own numbers; the source carries other numbers and another story (review-pass8-hits)"
  },
  {
    "file": "courses/vectors/problems-2.json",
    "item": "p-site-plan",
    "kind": "retold",
    "source": [
      {
        "file": "courses/vectors/l7-one-after-another.json",
        "text": "You multiplied matching entries."
      },
      {
        "file": "courses/vectors/problems-3.json",
        "text": "You multiplied matching entries."
      },
      {
        "file": "exams/topic-1.4.json",
        "text": "You multiplied matching entries."
      }
    ],
    "reason": "stands: stock slip line: it names a common slip in its plain words and carries no number or story; a learner would not know it as a repeat; exam source: stock slip line for a matrix product (it stands in three units of the course); no number, no story (review-pass8-hits)"
  },
  {
    "file": "courses/vectors/problems-3.json",
    "item": "p-colour-sensor",
    "kind": "retold",
    "source": [
      {
        "file": "courses/vectors/l7-one-after-another.json",
        "text": "You multiplied matching entries."
      },
      {
        "file": "courses/vectors/problems-2.json",
        "text": "You multiplied matching entries."
      },
      {
        "file": "exams/topic-1.4.json",
        "text": "You multiplied matching entries."
      }
    ],
    "reason": "stands: stock slip line: it names a common slip in its plain words and carries no number or story; a learner would not know it as a repeat; exam source: stock slip line for a matrix product (it stands in three units of the course); no number, no story (review-pass8-hits)"
  },
  {
    "file": "courses/vectors/problems-3.json",
    "item": "p-engraver-dial",
    "kind": "retold",
    "source": [
      {
        "file": "courses/vectors/l7-one-after-another.json",
        "text": "You multiplied matching entries."
      },
      {
        "file": "courses/vectors/problems-2.json",
        "text": "You multiplied matching entries."
      },
      {
        "file": "exams/topic-1.4.json",
        "text": "You multiplied matching entries."
      }
    ],
    "reason": "stands: stock slip line: it names a common slip in its plain words and carries no number or story; a learner would not know it as a repeat; exam source: stock slip line for a matrix product (it stands in three units of the course); no number, no story (review-pass8-hits)"
  }
]
```

To add only after the renumber of `p-fund-managers` (row 9, hit 162) has landed, since the stock line stays in the part:

```json
[
  {
    "file": "courses/testing/problems-3.json",
    "item": "p-fund-managers",
    "kind": "retold",
    "source": {
      "file": "exams/topic-1.6.json",
      "text": "You doubled the tail."
    },
    "reason": "stands: stock slip line of the course, left after the renumber of review-pass8-hits row 162 (review-pass8-hits)"
  }
]
```
