# Concept audit: exp-log levels 1 to 3 (round 1, blind)

Commit audited: `461a68d2`. Auditor brief: `docs/briefs/concept-audit.md`, Stage 0 ledger depth (exp-log is topic 0.3).
Files read in full: `l1` to `l13`, `review-1` to `review-3`, `homework-1` to `homework-3`, `problems-1` to `problems-3`, and the four fluency sets (`fluency-l3`, `fluency-l6`, `fluency-l8`, `fluency-l10`). 26 content files, no code widgets.

Ledger: `docs/reports/audit-exp-log-1-3-ledger.md`, 1,102 rows: correct 1,089, imprecise 9, misleading 3, wrong 1, unverified 0.
Script: `docs/reports/exp-log-L1-3-concepts.py`, 6,214 checks, 1 failing (finding 1), exit 1.

Sources used: Gelfand and Shen, *Algebra* (powers, negative and rational exponents); a standard A-level pure mathematics text (index and log laws, change of base, exponential models); Rudin, *Principles of Mathematical Analysis* 3.31 ($e$ as a limit); Hull, *Options, Futures and Other Derivatives* ch. 4 (compounding conventions) and ch. 15 (volatility and the square root of time); Tsay, *Analysis of Financial Time Series* sec. 1.1 (simple and log returns).

## What the watch list found

- Exponent laws and their domain: every general statement carries $a > 0$ (`l3` screens[7] and summary, `l4` screens[7], `l8` screens[7]). No item raises a negative base to a fractional power. Two loose sentences are in finding 7.
- Log laws: the log of a sum is handled by a trap, a review item and the l6 summary. Logs of zero and of negatives are called undefined wherever they arise (`l5`, `l8` screens[5], `l10` screens[4], `l11` screens[6]). The definition states $b > 0$, $b \neq 1$, $x > 0$. One summary note is loose (finding 6).
- Change of base: stated, proved and used with "the same base on top and bottom". Correct.
- ln against $\log_{10}$: `l7` says once that $\log$ with no base means $\log_{10}$ and repeats it in the summary. `l10` introduces $\ln = \log_e$ and adds that calculators have both keys and that Python's `math.log` is ln. The base-10 slip is a named wrong value where it matters. Correct and consistent.
- $e$ as a limit: $(1 + \tfrac{1}{n})^n$ shown increasing and bounded, values right to four places, the step to $e^r$ derived by substitution. Correct. One canvas number is wrong (finding 1).
- Compound against continuous growth, doubling time: $T = \ln 2 / k$ is tied to the continuous rate and $T = \ln 2 / \ln(1 + r)$ to the yearly rate. The rule of 72 is called an estimate each time, with the rate form (yearly, in percent), and 69.3 is kept for continuous rates. Correct.
- Simple against log returns: defined, converted both ways, additivity proved by telescoping, the failure of $\ln(1 + r) \approx r$ for large moves trapped, the total-loss edge case right. Correct.
- Percentage growth over several periods: factors multiply throughout; "ten falls of 10%" and "up 10% then down 10%" are both right.
- Money: every money item uses £.
- Fluency: all 14 families were enumerated over their whole variable range in the script (5,513 valid draws). Every key is right, and no slip band meets a key band. One slip line is in finding 2.
- Plain words: no Stage 0 problem found.

## Findings

1. `l9-compounding-more-often.json` | `screens[2].explain.canvas.points[id=P].y` | wrong, minor | The explained state places P at height 2.6916 for $n = 52$. | $(1 + \tfrac{1}{52})^{52} = 2.6926$ (script; hand check $52\ln\tfrac{53}{52} = 0.990506$, $e^{0.990506} = 2.6926$). The caption and the text say £2.69, which is right, and the canvas `derive` rule redraws P from $n$, so a learner sees the right height. The authored number is still false. Basis: direct computation. | Fix: `"y": 2.6926`.

2. `fluency-l8-solving-for-the-power.json` | `families[money-target].wrong[id=logs-too-soon].line`; `fluency-l10-natural-log.json` | `families[continuous-growth].wrong[id=logs-too-soon].line`; `homework-3.json` | `items[h-exact-time].feedback.byKey.ln-thousand` | misleading, minor | Each line says the learner "took logs before getting the power alone". That is not a mistake, and it does not give the slip's value. | The slip values are $\tfrac{\ln t}{\ln g}$, $\tfrac{\ln t}{k}$ and $\tfrac{\ln 1000}{0.08}$: the start amount was dropped. Logs taken first and done correctly give the key, since $\ln p + v\ln g = \ln t$ (script: true in all 261 money-target draws). `l8` screens[4] itself says "Taking logs straight away also works". `l8` screens[6] names the real slip correctly ("left out the 500"). Basis: product law of logarithms. | Fixes, paste-ready:
   - fluency-l8: `You left out the {p}: that solves ${g}^{v} = {t}$. Divide by {p} first.`
   - fluency-l10: `You left out the {p}: that solves $e^{{{k}t}} = {t}$. Divide by {p} first.`
   - homework-3: `You left out the 250: that solves $e^{0.08t} = 1000$. Divide by 250 first, to get $e^{0.08t} = 4$.`

3. `l10-natural-log.json` | `screens[10].explain.text`; `homework-3.json` | `items[h-two-bonds].prose`; `l12-doubling-time.json` | `screens[9].explain.text` | imprecise, minor | Three sentences state a desk convention as fact: "Rates desks quote zero-coupon yields this way", "Traders compare yields on a continuous basis", "Execution desks quote unwind speed this way". | Continuous compounding is the convention of pricing models, not of market quotes: bond and strip yields are quoted with annual or semi-annual compounding, deposits on money-market bases (Hull, ch. 4, "Measuring interest rates"). No source supports the unwind sentence; schedules are usually stated as a horizon or a participation rate. The arithmetic in all three items is right. | Fixes:
   - l10: replace the last sentence with `Pricing models often work with zero-coupon yields in this form.`
   - homework-3: replace the sentence with `To compare the two yields, put both on a continuous basis.`
   - l12: replace the last sentence with `A half-life is one plain way to state an unwind speed.`

4. `homework-3.json` | `items[h-unwind-rate].explain.text` | imprecise, minor | "The desk sells 23.10% of what it still holds per day, continuously." | $k = 0.2310$ is an instantaneous rate. Over one whole day the desk sells $1 - e^{-0.2310} = 20.63\%$ of the holding it started the day with (script). This is the same gap `l9` screens[6] teaches (6% continuous is 6.18% a year), so the sentence cuts against the course's own trap. | Fix: replace the last sentence with `The rate is continuous: over one whole day the desk sells $1 - e^{-0.2310} = 20.63\%$ of its holding.`

5. `l10-natural-log.json` | `screens[7].question` with `screens[7].explain.text`; `quiz[q-two-as-e].question` | imprecise, minor | The trap asks which formula gives "exactly the same growth" as $100 \times 3^t$ and keys $100e^{1.0986t}$; the explanation says the curve "lies exactly on" it. The quiz asks which "is the same as $2^t$" and keys $e^{0.6931t}$. | $e^{1.0986} = 2.99996$ and $e^{0.6931} = 1.99996$ (script): equal to four places only. The exact statement is $3^t = e^{t\ln 3}$, which the lesson gives two screens later. | Fixes: question `Which formula gives the same growth as $100 \times 3^t$, with the rate rounded to four places?`; in the explanation replace `lies exactly on` with `lies on`; quiz question `Which is the same as $2^t$, with the rate rounded to four places?`

6. `l5-how-many-doublings.json` | `summary.formula.note` | imprecise, minor | "Needs $b > 0$, $b \neq 1$ and $x > 0$. Numbers below 1 have negative logs." | The note sits beside the general definition, which allows $0 < b < 1$. There the sign flips: $\log_{1/2}\tfrac{1}{8} = 3$ (script). In the lesson body the same sentence is said of base 2 and is right. | Fix: `Needs $b > 0$, $b \neq 1$ and $x > 0$. For a base above 1, numbers between 0 and 1 have negative logs.`

7. `l3-strange-powers.json` | `quiz[q-half-neg].explain.text`; `l10-natural-log.json` | `screens[3].explain.text` | imprecise, minor | "A negative power of a number below 1 gives a number above 1." and "Any number to the power 0 is 1". | The first holds for $0 < a < 1$ only: $(-2)^{-1} = -0.5$. The second fails at 0: $0^0$ is left undefined (Gelfand and Shen define $a^0 = 1$ for $a \neq 0$). `l5` quiz already says "Any positive base". | Fixes: `A negative power of a number between 0 and 1 gives a number above 1.` and `Any number except 0 to the power 0 is 1, so $e^0 = 1$ and $\ln 1 = 0$.`

Totals: wrong 1, imprecise 5, misleading 1. Serious 0, minor 7.

No finding needs more than a sentence. No graded key is wrong, and no wrong option or slip value is right under another valid convention.

## Notes that are not findings

- `l2` screens[9] `gain2` feedback gives the second ten years' gain as £1,024.41. That is the difference of the two displayed balances; the unrounded gain is £1,024.40. A penny of rounding, left as is.
- `fluency-l10` `ln-from-two-values` computes the key from the two four-place logs, so it can differ from the true four-place value by up to 0.0004. The band of 0.0005 takes both in every draw (script), and `l10` screens[5] says so for $\ln 6$ and $\ln 8$.
- `l9` screens[8] derives $e^r$ with $m = n/r$, written for $r > 0$; the negative-rate quiz item then uses the result for $r < 0$, where it also holds. Fine at Stage 0.
- Finding 2's class (a slip line that names a mistake which does not produce the slip's value) now appears three times in this course. Under SESSION PROTOCOL 6 that makes it a candidate for a rule; see the inbox bullet.

## Checks run

- Validator: `cd app && node tools/validate.mjs`: 0 errors, 4,619 warnings.
- Number scripts: `node tools/run-number-scripts.mjs --only exp-log` with the venv Python: 5 of 5 passed.
- Grading: `node tools/grade-all.mjs --file <each of the 26 files> --local-cdn <pkgs>`: 0 failures in every file.
- Concepts script: `docs/reports/exp-log-L1-3-concepts.py`: 6,214 checks, 1 failing (finding 1), exit 1. It includes a Monte Carlo of the one statistical claim (`homework-3` `h-annual-vol`): 40,000 simulated years of 252 independent daily log returns, normal and $t_5$, give an annual standard deviation of 0.1905 against the negation 3.024. NumPy is the venv's version; no figure depends on it.
- No playthrough, as the common rules set.

## Overlap with earlier reads (read after the ledger and findings were written)

Earlier reads opened: `docs/reviews/review-exp-log-1-3.md` (48 findings, all fixed before the audited commit), `docs/reviews/review-problems-0.3-b.md` section A (12 findings on `problems-1` to `problems-3`, fixed), `docs/reviews/review-delta-problems-aa-3.md`, `docs/reviews/review-reuse-af-hits-reauthor-exp-log.md`, `docs/reports/fluency-exp-log.md` and `docs/reports/problems-exp-log.md`. There is no earlier `audit-exp-log*` file.

| Conceptual findings | Count |
|---|---|
| Found by this audit only | 7 (wrong 1, misleading 1, imprecise 5; all minor) |
| Found by the earlier reads only | 31 (review-exp-log-1-3: wrong 9, misleading 19; review-problems-0.3-b: wrong 1, unclear 2). All were fixed before this commit, so this audit could not find them again; the fixed text was read as ledger rows and is correct. |
| Found by both (same defect) | 0 |

New `wrong` that no earlier read found: 1 (finding 1, minor, an authored canvas number the engine does not show).

Nearest neighbours, not counted as "both": the earlier review's finding 38 fixed two feedback lines that read a continuous rate as a daily step (`l12` screens[9], `review-3` items[3]); finding 4 here is the same class in a third sentence (`homework-3` `h-unwind-rate` explain) that the earlier fix did not reach. The fluency report lists the `logs-too-soon` slip ids without questioning their lines (finding 2).

## Fix pass

Opus fixer, on `eba9ca3e`. Each basis is my own recomputation or source; scratch scripts in the session scratchpad (`fix-el13/range.py`).

1. Fixed. `"y": 2.6926`. Basis: $(53/52)^{52} = 2.692597$, twice (direct power and $e^{52\ln(53/52)}$).
2. Fixed (fluency-l10 and homework-3 lines also keep the "divide first" step). Basis: $\ln(p g^v) = \ln p + v\ln g$, so logs first done right gives the key; the slip value $\ln t/\ln g$ (or $\ln t/k$, $\ln 1000/0.08 = 86.35$) solves the equation with the start amount dropped. Checked over every valid draw (money-target 522 draws counting both letters, continuous-growth 301) by closed form and by bisection; slip bands stay clear of key bands. Slip values and ids unchanged.
3. Fixed, wording as proposed. Basis: Hull ch. 4, market zero and bond yields are quoted annual or semi-annual; continuous compounding is the modelling convention. No source for a quoted half-life convention, so the l12 sentence now claims only that it is one way to state speed.
4. Fixed differently: "This rate is continuous. Over one whole day the desk sells $1 - e^{-0.2310} = 20.63\%$ of its opening holding." (split to keep under 20 words). Basis: $1 - e^{-0.2310} = 0.20626$; with the exact $k$, $1 - 2^{-1/3} = 0.20630$.
5. Fixed, with "four decimal places". Basis: $e^{1.0986} = 2.999963$, $e^{0.6931} = 1.999906$ (the audit's 1.99996 is a slip of its own; the conclusion holds). No other option becomes right under the new wording.
6. Fixed, wording as proposed. Basis: $\log_{1/2}(1/8) = 3 > 0$.
7. Fixed, both sentences as proposed. Basis: $(-2)^{-1} = -0.5$; $a^0 = 1$ is defined for $a \neq 0$ (Gelfand and Shen), $0^0$ left undefined.

Gates: validator 0 errors (4,619 warnings, as before); voice-scan 35 on the eight edited files 0 and 0; concepts script 6,214 checks, 0 failing, exit 0 (no check re-pointed); number scripts exp-log 5 of 5; grade-all 0 failures on each edited file; playthrough of the five lessons, `homework-3` and both fluency sets, desktop and `--mobile`: all passed (8 items each).
