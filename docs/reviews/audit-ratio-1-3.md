# Concept audit: ratio, levels 1 to 3 (round 1, blind)

Course `ratio` (Ratio and Percentages, topic 0.1, Stage 0), commit f69104f4. Files read: 13 lessons, 3 review sets, 3 homework sets, 3 problem sets, 5 fluency files (27 content files). Reduced ledger depth: definitions, rules, "always / never / every / only" claims, conventions, and every graded key, wrong option and slip.

- Ledger: `docs/reports/audit-ratio-1-3-ledger.md`, 1053 rows: correct 1044, wrong 1, imprecise 8, misleading 0, unverified 0.
- Concepts script: `docs/reports/ratio-L1-3-concepts.py` (Python standard library only, no version-dependent figure).
- Sources: DfE GCSE mathematics subject content (2013), strand "Ratio, proportion and rates of change" (R1 to R16); CGP GCSE Maths Higher (9-1) revision guide, Section Four (Ratios, Direct and Inverse Proportion, Percentages, Compound Growth and Decay, Unit Conversions and Best Buys); derivations; sweeps and seeded Monte Carlo in the script.

## Verdict

The course is sound. No finding is serious: no definition, method, convention or graded key would leave a learner with a wrong idea. One line states a false place-value count (finding 1). Eight are imprecise: four universal sentences that the same lesson contradicts, one slip whose value does not match its named mistake, one explanation that reaches the right number by a reason pointing the other way, one derivation that marks a valid order wrong, and one stated value a penny off.

What was checked and holds, against the watch list:

- **The base of a percentage.** Every item that takes a fee, tax, discount or return says what it is a percentage of ("of the trade value", "taken from the balance", "on top", "of the price before tax"). Percentage change is always measured from the original, and the convention is stated where it first matters (l5 `screens[3]`, `screens[6]`).
- **Per cent against percentage points.** Defined in l3 `screens[6]` and used correctly in every later item (l3 quiz, review-1 `r-weight-points`, `r-win-rates`, homework-1 `h-fee-cut` and the long-form, problems-1 `p-phone-rise`, where "inflation plus 3.9 percentage points" is added correctly).
- **Successive percentages.** $(1+p)(1-p) = 1 - p^2 < 1$ for $p \neq 0$, in either order: swept over 1,000 values and 200,000 random swings. "Unequal percentages can cancel; equal ones cannot" holds ($1.25 \times 0.8 = 1$).
- **Reverse percentages.** Every item divides by the multiplier; every add-back, take-off-again and divide-by-the-cut slip carries the value that mistake gives.
- **Compound interest.** $P(1+r)^n$ against $P(1+nr)$: equal at $n = 1$, compound ahead for every $n \geq 2$ and $r > 0$ (swept). The quiz claim that 10% compound overtakes 11% simple at year 3 and then pulls away holds (gap $-0.01$, $-0.01$, $+0.001$, then increasing).
- **Ratio sharing, direct and inverse proportion, unit rates.** All keys and slips recomputed. The fixed-ratio and fixed-product tests are stated correctly, and the "neither" cases (taxi fare, fuel tank, gym bill) fail both tests as claimed.
- **Units, rounding and money.** Kilograms, minutes and pence are converted before dividing. £100 shared 1 : 2 gives £33.33 and £66.67. UK VAT at 20% (and 5% on a gas bill) and the £500 savings allowance at 40% match UK practice. One penny is off in problems-2 (finding 9).
- **Currencies.** Bureau buy and sell rates point the right way (fewer euros per pound sold to you, more euros per pound asked back). Inverse rates, chained rates and the three-currency loop are right.
- **Fluency.** All 13 families rebuilt from their meaning and swept over the whole range, 22,897 cases: every key is right, every slip equals its named mistake, no slip band meets the key or another active slip, and every printed price is a whole number of pence.
- **Plain words.** Drawdown, daily return, cumulative return, hedge ratio, index futures, spread and VAT are each explained where first used.

## Findings

1. `l1-out-of-a-hundred.json` | `screens[8].widget.options[id=three].why` | wrong, minor | The why-line for 850% says "You moved the point three places." From 0.085 to 850 the point moves four places. Three places give 85, which is the option beside it. | $0.085 \times 10^3 = 85$, $0.085 \times 10^4 = 850$ (script, part 4, failing check). review-1 `r-tiny-return` counts the same pattern correctly (0.0045 to 4.5% "three places", to 45% "four places"). | Replace the `why` with: `You moved the point four places. Multiplying by 100 moves it two.`

2. `l1-out-of-a-hundred.json` | `quiz[0]` (`q-seven-25ths`) `.widget.wrong[id=digits]` | imprecise, minor | The slip is stored as 0.725, which is a typed 72.5. Its line says "You wrote 7 and 25 side by side." Side by side they make 725. A learner who types 725 gets the generic line, and one who types 72.5 is told something they did not do. | The twin slip on `screens[4]` stores 0.34 for $\tfrac{3}{4}$, which is the two digits side by side. | Set `"value": 7.25` on the slip and add `"over100": true` to the widget (the validator asks for it when a per cent value is above 1). The line stays as it is.

3. `l2-building-percentages.json` | `screens[7].explain.text` | imprecise, minor | "The percentage multiplies a hundredth; it never divides the amount." The first screen of this lesson finds 10% by dividing the amount by 10, and 10 is the percentage. | $p\%$ of $A$ equals $A \div p$ exactly when $p^2 = 100$, so for $p = 10$. Also 20%, 25% and 50% are $A \div 5$, $A \div 4$ and $A \div 2$. | Replace the last sentence, so the text reads: `Dividing by 4 finds a quarter, which is 25%. 4% means 4 hundredths: 1% is £3, so 4% is £12. Divide by 100 to find 1%, then multiply by the percentage.`

4. `l3-what-percentage.json` | `summary.formula.note` | imprecise, minor | "The whole is every item, never just the other part." This fits a win rate. It does not fit `screens[5]` (the new £500 as a percentage of the old £400), `screens[6]` or the quiz item `q-rate-relative`, where the whole is the other amount. Read literally it gives $500 \div 900$. | The formula it annotates, part over whole, covers both kinds of comparison (DfE R9: express one quantity as a percentage of another). | Replace the note with: `When the parts make one total, the whole is the total, not the other part.`

5. `l10-scaling.json` | `quiz[0]` (`q-units`) `.explain.text` | imprecise, minor | "A ratio only compares like with like, so the units must match first." `screens[2]` of the same lesson speaks of "the same ratio of grams to people", and l12 builds rates from two different quantities. | True for a ratio of two amounts of the same kind, which is the case in this item. | Replace the explanation with: `In grams the ratio is 1,500 : 600. Both divide by 300, giving 5 : 2. Both amounts are weights, so put them in the same unit before you simplify.`

6. `l8-growth-on-growth.json` | `screens[9].explain.text` | imprecise, minor | "Adding returns ignores growth on growth, so here it overstates." The numbers are right (3.5% added against 3.32% compounded). The reason points the other way: `screens[6]` of this lesson says adding understates compound growth. Here the sum is too high because the 4% fall was taken from a higher price. | Cross terms: $0.05 \times (-0.04) + 0.05 \times 0.025 + (-0.04) \times 0.025 = -0.00175$. Monte Carlo (script, part 3): with every return positive the sum understates in 100,000 of 100,000 paths; with mixed signs the sum is above the compound return in 79.5% of 75,139 paths and below it in 20.5%. | Replace the last sentence, so the text reads: `$1.05 \times 0.96 \times 1.025 = 1.0332$, a **cumulative return** of 3.32%. The stock went from £200.00 to £206.64, which agrees. Adding misses that the 4% fall came off a higher price, so here it overstates.`

7. `l11-direct-or-inverse.json` | `screens[5].widget.options[id=direct].why` | imprecise, minor | "Direct proportion is a line through (0, 0) that rises." The lesson's own test is a fixed ratio $y/x = k$, and $y = kx$ with $k < 0$ passes it while falling. The reason the fuel line is not direct is that it misses (0, 0). | DfE R10 and R14: direct proportion is $y = kx$, a straight line through the origin. | Replace the `why` with: `Direct proportion is a straight line through (0, 0). This line starts at 40 litres, so it misses (0, 0).`

8. `l10-scaling.json` | `screens[7].widget` (order) | imprecise, minor | The lines `origin` ("At $x = 0$, $y = 0$") and `slope` ("Each extra unit of $x$ adds $k$") each follow from $y = kx$ alone. Only ratio, times, origin, slope is accepted, so the equally valid ratio, times, slope, origin is marked wrong. | `docs/AUTHORING.md`, `order`: `same` makes independent steps interchangeable, "a correct proof is never marked wrong". | Add `"same": [["origin", "slope"]]` to the widget. The hint and feedback lines stay true.

9. `problems-2.json` | `items[3]` (`p-fund-six-months`) `.parts[1]` `widget.accept`, `feedback.correct`, `explain.text` (and the figure carried into `parts[2]`) | imprecise, minor | The June value is stated as £50,746.60. The fund is worth $52{,}000 \times 0.91^3 \times 1.09^3 = 50{,}746.6075$, which is £50,746.61. The 60 comes from carrying March rounded to the penny, as the part asks. The key (50,746.605, tolerance 0.01) accepts both, so no learner is marked wrong. | Script, part 4: exact value by rational arithmetic. | Set `accept` to `£50,746.60, or £50,746.61 from unrounded working`. Replace `explain.text` with: `Each 9% rise multiplies by 1.09, so three of them multiply by $1.09^3 = 1.295029$. $39{,}185.69 \times 1.295029 \approx 50{,}746.60$. Without rounding March first the value is £50,746.61, and both are accepted.`

Counts: wrong 1 (serious 0, minor 1); imprecise 8 (serious 0, minor 8); misleading 0.

## Checks run

- Validator (`node tools/validate.mjs`): 0 errors.
- Number scripts (`node tools/run-number-scripts.mjs --only ratio`, venv Python first on PATH): 5 of 5 passed, 0 new failures.
- `node tools/grade-all.mjs --file <file> --local-cdn <pkgs>` on each of the 27 content files: 0 failures on every file. The course has no code widget.
- `docs/reports/ratio-L1-3-concepts.py`: 29,044 checks, 183 numeric and slider widgets each with a recomputed key and slips, 22,897 fluency cases, 1 fail (finding 1) and 8 notes (findings 2 to 9). Exit code 1 until finding 1 is fixed.
- No playthrough, as the brief sets.

## Overlap with earlier reads

Read after the ledger and findings were written: `docs/reviews/review-ratio-1-3.md` (39 findings and its fix pass) and `docs/reviews/review-problems-ratio-1-3.md` (15 findings and its fix pass). No earlier `audit-ratio*` file and no `docs/reports/ratio-*.md` author report exists at this commit. The three author number scripts were run, not read, before the findings were written.

Conceptual findings only (voice, layout, freshness and continuity findings of the earlier reads are left out):

| | count | which |
|---|---|---|
| This audit only | 9 | findings 1 to 9 above |
| Earlier reads only | 24 | review-ratio findings 1 to 17 (6 wrong slip values or lines, 11 misleading); review-problems findings 1, 2, 3, 7, 8, 12, 14 (slip bands, one why with two figures that disagreed, one why naming the wrong working). All were fixed before this commit, and each fixed value passes part 1 of the script. |
| Both | 0 | no earlier finding names the same defect as any of findings 1 to 9 |

New `wrong` not found by any earlier read: 1 (finding 1, minor). Convergence rule: at most one new `wrong` per three levels, so this round meets it once the fix pass and its read are done.

Two notes on the earlier reads. The earlier review fixed a sibling of finding 1 in the next lesson (l2 `screens[7]`, "4 lots of 10p") and the same pattern in l1 was not caught. Its finding 12 tightened "for any real swing" to "for any swing other than 0" in l7; findings 3, 4, 5 and 7 here are the same class (a universal sentence one case too wide) in four other lessons.

## Engine and tooling notes

Appended to `docs/BACKLOG-INBOX.md` under "Raised later (audit ratio):", three bullets (findings 1 and 2; finding 8; finding 9).

## Fix pass

Opus fixer, from c4268e7c. Each basis is my own working, not the audit's.

1. fixed. $0.085 \times 10^4 = 850$ and $0.085 \times 10^3 = 85$, so 850% is four places; the why now says four.
2. fixed. "7 and 25 side by side" is a typed 725, stored 7.25 (725/100, computed in the concepts row and the L1 number script); band clear of the key 0.28 and of `flipped` 3.5714. Slip value changed; `over100: true` added. Byline unchanged.
3. fixed. Screen 1 finds 10% as £240 ÷ 10, and $p\%$ of $A$ is $A \div p$ only for $p = 10$, so "never divides" is false; the last sentence now says divide by 100 for 1%, then multiply.
4. fixed. Screen 5 measures £500 against £400 (125%), where the whole is the other amount; the note now limits "the whole is the total" to parts that make one total.
5. fixed. Screen 2's "ratio of grams to people" is a ratio of unlike quantities; the reason now says both amounts are weights, so convert before simplifying.
6. fixed. Prices £200, £210, £201.60, £206.64: adding counts each move on £200 (+10, −8, +5), but the fall took £8.40 off £210 and the rise added £5.04, so the sum is 36p high; cross terms sum to −0.00175 and the triple term −0.00005. New sentence: the 4% fall came off £210, not £200.
7. fixed. $y = -2x$ keeps $y/x$ fixed and falls, so "rises" is not part of direct proportion; $40 - 5x$ gives 40 at $x = 0$, so it misses (0, 0). Why reworded.
8. fixed. `origin` and `slope` each use only $y = kx$; `"same": [["origin", "slope"]]` added (order.js item 201 swaps them in places 3 and 4). Also changed: `feedback.correct` ("Each line uses the one before it" is false for either order, as `slope` does not use `origin`) and the step hint, which now allows either order.
9. fixed differently. The part says "Using £39,185.69", and $39{,}185.69 \times 1.295029 = 50{,}746.6049$, so £50,746.60 is right as asked; unrounded, $52{,}000 \times 0.91^3 \times 1.09^3 = 50{,}746.6075$ (rational and float), £50,746.61. Key 50,746.605 ± 0.01 already accepts both and is unchanged. `accept` stays the plain figure, as `problems-ratio-numbers.py` requires; the explanation now names £50,746.61 and says both are accepted.

Scripts re-pointed (old text or old value only): `ratio-L1-3-concepts.py` (finding 2 skip removed and its row added, finding 6 note reads the text with the Monte Carlo split kept as a check, finding 9 note reads the explanation); `ratio-L1-numbers.py` line 83, slip value 7.25. Gates: validator 0 errors, voice scan 35 0 and 0, concepts script exit 0 (0 fail, 0 note), number scripts 5 of 5, grade-all 0 failures on all seven files, playthrough of all seven green desktop and `--mobile`.
