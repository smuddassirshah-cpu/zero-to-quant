# Blind concept audit, round 2: markets levels 1 to 3

Auditor: fresh reader, blind to every earlier read until the ledger and the findings below were written.
Commit audited: `7bc79413`. Scope: `l1` to `l13`, `review-1` to `review-3`, `homework-1` to `homework-3` (no `problems-*` file exists for these levels).
Stage 1 course, so the full ledger: `docs/reports/audit-markets-1-3-r2-ledger.md`. Script: `docs/reports/markets-L1-3-concepts-r2.py`.

## Result

- Ledger: 2,440 rows. Verdicts: correct 2,431, wrong 2, imprecise 7 (five of them one finding), misleading 0, unverified 0.
- Findings: 5. `wrong` 2 (both minor), `imprecise` 3 (all minor). Serious 0, minor 5.
- No graded key is wrong. Every choice item has exactly one true option under its stated premises, including the two items whose premises a fix widened (`l4-npv` `q-different-rates` and `q-irr-bracket`).

## What was checked

- Every string of every file was read against the source named in the ledger. Hull section numbers are from the 10th edition.
- 203 script checks: every figure the audit relied on, every slip whose feedback names a mistake, and the empirical claims.
- The watch list, each read in every file where it arises:
  - Compounding and day counts: `l3` states nominal against effective once, where it first matters; 365 against 360 is said in `l3` screen 10 and is right (Hull §6.1).
  - Simple against log returns: `l8` screens 5 and 8 and `q-logs` are right.
  - Clean against dirty price: `l5` screen 11 is right for a purchase exactly halfway through a coupon period.
  - YTM, current yield and coupon rate: `l6` screens 3, 4 and 9 and `q-current` are right, with the order for a premium bond stated.
  - Macaulay against modified duration: `l6` screen 7 divides by $1 + y$, right for yearly compounding.
  - NPV against rate: every monotonicity claim carries the premise "an outlay followed by inflows". The script confirms it on 2,000 random streams, and shows a stream with two IRRs to confirm the premise is needed.
  - Forward bounds: `l10` prices only investment assets (a share, gold, a currency, an index). `homework-3` `h-airline-hedge` says cost of carry is only an upper limit for fuel (Hull §5.11). `h-carry-two-rates` derives a band and gets both ends right.
  - Forwards against futures: `l11` never says the two prices are equal; it says what daily settlement changes.
  - Short selling and dividends: `l12` screen 3 says the short pays the dividend and that the ex-dividend fall offsets it (Hull §5.2).
  - Margin and leverage: `l11`, `l13`, `review-3` and `homework-3` triggers and top-ups recomputed, long and short.

## Findings

1. `homework-1.json` | `items[6].feedback.byKey.simple` (`hw1-irr-quadratic`) | **wrong**, minor | The line says "6.67% solves $1000(1 + 2r) = 1100$". That equation gives $r = 0.05$, not 0.0667. A learner who types 6.67% is told they solved an equation whose root is a different number. | Evidence: $2r = 0.10$, so $r = 0.05$. The slip value 0.0667 is $0.10 / 1.5$: the £100.00 gain over £1,000.00, spread over the mean wait of 1.5 years. Script check "hw1 quadratic slip 'simple'" fails; the check beside it confirms $0.10/1.5$. | Fix, paste-ready: `"simple": "6.67% spreads the £100.00 gain over the average wait of 1.5 years: $0.10 \\div 1.5$. That is a simple-interest return. Compounding needs the quadratic."` Basis: the two payments wait 1 and 2 years, mean 1.5; $1000(1 + 1.5r) = 1100$ gives $r = 0.0667$.

2. `l8-measuring-returns.json` | `screens[5].widget.options[3].why` (option `up`, "It grew to £125") | **wrong**, minor | The line says "You applied the −50% to the original £100 and kept the +50% on top." That mistake gives $100 - 50 + 50 = £100$, which is option `flat`, not £125. No reading of the sentence gives £125. | Evidence: script check "l8 s5 option 'up'" fails (computed 100, content 125). £125 comes from $1 + 0.5 \times 0.5$, the two returns multiplied and read as a gain, or from $150 - 0.5 \times 50$, the loss taken off the gain alone. | Fix, paste-ready: `"why": "You multiplied the two returns, $0.5 \\times 0.5 = 0.25$, and read it as a gain. Multiply the growth factors instead: $1.5 \\times 0.5 = 0.75$."` Basis: BKM ch. 5, compounding of holding-period returns; $1 + 0.25 = 1.25$.

3. `l13-leverage.json` | `summary.ideas[2]` | **imprecise**, minor | "A fall of $1/L$ wipes out the equity" is true only with no interest. Screen 5 and quiz `q-wipe` both say so; the summary, which is what a learner keeps, does not, and the formula beside it includes interest. | Evidence: set $R_E = -1$ in $R_E = LR_A - (L-1)r$: $R_A = -\dfrac{1 - (L-1)r}{L}$. At $L = 2$, $r = 5\%$ the equity is gone after a 47.5% fall, not 50%. | Fix, paste-ready: `"Ignoring interest, a fall of $1/L$ wipes out the equity; a maintenance margin forces a sale before that."` Basis: the lesson's own formula; BKM ch. 3 §3.8.

4. `l5-pricing-a-bond.json` | `screens[3].prose` | **imprecise**, minor | "Most bonds, including UK government bonds, pay coupons half-yearly." The convention is by market: UK and US government bonds and US corporates pay half-yearly, while German, French and other euro-area government bonds and most eurobonds pay yearly. "Most" teaches a rule that fails for a large part of the market. | Basis: Fabozzi, *Bond Markets, Analysis and Strategies*, ch. 1 (coupon conventions) and ch. 2 (pricing with half-yearly coupons as the US convention). | Fix, paste-ready: `"Many bonds, including UK and US government bonds, pay coupons half-yearly. This 4% bond pays £2 every six months, and £102 at year 5. Its yield is 5% a year, compounded half-yearly: 2.5% per six months."`

5. `l4-npv.json` `screens[7]`, `l5-pricing-a-bond.json` `screens[9]`, `l8-measuring-returns.json` `screens[10]`, `homework-2.json` `items[3]`, `homework-1.json` `items[5]` | `feedback.byKey.error` | **imprecise**, minor | Each line says the code "stopped with an error" and to check that the `...` is replaced; the `homework-1` line adds "or ran too long". Under the page's grader neither case is keyed `error`. A starter left with `...` raises inside the first test and is keyed `test-1`. A loop that never ends is stopped per case and keyed `test-1`. The key `error` is given only when the code does not load, for example on a syntax error, where "check the `...`" is the wrong advice. | Evidence, Pyodide 0.27.7 through `app/tools/code-runner.mjs`: the `l4` starter gives `key: test-1` with a `TypeError` in row 0; a missing colon gives `key: error`; the `homework-1` starter with `pass` in the loop gives `test-1`; `if ...:` in `homework-2` runs, because `Ellipsis` is true, and gives `test-1`. | Fix, paste-ready, for the four `...` lines: `"error": "Your code could not be run. Check the syntax: brackets, colons and indentation."` For `homework-1` `items[5]`: the same `error` line, and add to `feedback.generic` the sentence `"If a test is stopped for running too long, check that the loop changes \`lo\` or \`hi\` every time."` The engine side is raised in the inbox.

## Code widgets

Six Python widgets. All were run under the page's Pyodide 0.27.7 through `app/tools/code-runner.mjs` (script kept in the scratch folder, 48 submissions).

| Widget | `byKey` line | Natural codings submitted | First failing test | Verdict |
|---|---|---|---|---|
| `l5` `bond_price` | `test-1` (describes its test) | coupon-rate discounting; face left out; face undiscounted; coupon not times face | 1, 1, 1, 1 | correct |
| `l5` `bond_price` | `test-2` | fixed 1.05 in both lines; in the coupon line; in the face line | 2, 2, 2 | correct |
| `l5` `bond_price` | `test-3` | face over a fixed 5 years, with `/ ... ** 5` and with `* ... ** -5`; loop and face both fixed at 5 | 3, 3, 3 | correct |
| `l8` `annualised` | `test-1` | arithmetic mean; total over $T$; total; root without −1 | 1, 1, 1, 1 | correct |
| `l8` `annualised` | `test-2` | root fixed at 3, with `**` and with `math.pow` | 2, 2 | correct |
| `l8` `annualised` | `test-6` | `math.log`; `math.log1p` | 6, 6 | correct |
| `homework-2` `ytm` | `test-1` | reversed `<`; `price > bond_price(...)`; compare with face | 1, 1, 1 | correct |

- A NumPy log coding of `annualised` returns −1 at the −100% year and passes every test. It is a correct program, so this is not a finding.
- Hidden tests reject the obvious wrong programs. `npv`: discounting from $t + 1$, simple discounting, multiplying, no discounting. `irr`: reversed bracket. `margin_calls`: top-up to maintenance, `<=` at maintenance (test 6), short sign ignored (test 3), margins not per contract (test 2), call not paid in, settling once at the end. No wrong program passed.
- No line is timing-dependent. The `error` lines are finding 5.

## Empirical claims, by simulation

| Claim | Check | Result |
|---|---|---|
| `l8` screen 12: "a few years of data could not tell them apart" (Sharpe 0.42 against 0.40) | 200,000 five-year records, normal returns | the lower-Sharpe fund ranks first in 49.1% (se 0.11%): indistinguishable |
| `l13` `q-recover`: "leverage makes 50% losses far more likely" | 1,000,000 years, mean 7%, volatility 15%, rate 5% | P(lose half) 0.00007 at $L = 1$, 0.088 at $L = 3$ |
| `l13` screen 9: a 15% market swings a 3 times account about 45% | same draws | sd of $R_E$ 0.4506 |
| `l8`: the arithmetic average overstates the annualised return | 20,000 random five-year records | average ≥ annualised in all |
| `l4`: NPV of an outlay followed by inflows falls as the rate rises | 2,000 random streams | monotone in all |
| `l6` screen 4: Newton reaches bisection's 20-step accuracy in three steps | run from 4%, 6% and 8% | at most 3 steps |

## Runs

- Validator: `0 errors, 4614 warnings`.
- `node tools/run-number-scripts.mjs --only markets`: 1 script, 1 passed, 0 new failures.
- `node tools/grade-all.mjs --file <each of the 19 files> --code --local-cdn <pkgs>`: 219 widgets checked, 6 Python code widgets run, 0 failures.
- `docs/reports/markets-L1-3-concepts-r2.py`: 203 checks, 2 failing, exit 1. The two failures are findings 1 and 2 and stay failing until the content is fixed.
- No playthrough, as the common rules set.
- The venv's NumPy and SciPy are newer than CI's pins. No figure depends on the version.

## Overlap with earlier reads

Read after the ledger and the findings above were written: `docs/reviews/review-1.7.md` (markets section, 20 findings, 13 of them conceptual), `docs/reviews/audit-markets-1-3.md` (round 1: 11 findings, its fix pass, and the fix-pass read with 1 more `wrong`), `docs/reports/markets-3-perf.md` and `docs/reports/concept-audit-notes.md`. The other review files that name markets cite it only for reuse or prerequisites.

All 25 earlier conceptual findings were fixed before this commit. Each fixed text has a ledger row here and all are verified correct, so "both" can only count a defect that survived its fix. None did.

| Conceptual findings | Count | Items |
|---|---:|---|
| This audit only | 5 | 1 to 5 above |
| Earlier reads only | 25 | review-1.7: 13; audit round 1: 11; its fix-pass read: 1. All fixed and verified in the ledger |
| Both | 0 | |

New `wrong` that no earlier read found: **2** (findings 1 and 2), both minor, one in level 1 (`homework-1`) and one in level 2 (`l8`). That is above the convergence rule's one new `wrong` per three levels.

Notes on the overlap:

- Findings 1 and 2 are the kind round 1's finding 10 was: a slip whose line names a mistake that does not give the slip's value. Round 1 recomputed the slips on numeric widgets with a `byKey` line; finding 2 sits on a choice option's `why`, and finding 1 on an equation quoted inside the line.
- Finding 5 is a new instance of a known engine fact (ENGINE-BACKLOG 1036), not raised on markets before. Round 1 swept the `test-N` lines (its findings 3, 6 and 7, all fixed and confirmed here by submission) but not the `error` lines.
- Round 1's serious findings (NPV monotonicity premise, the short's dividend, the fuel forward as an upper limit) are all sound now. The fix to `q-different-rates` that the fix-pass read sent back is also sound: under the added premise only "compute both at the same rate" is true.

## Inbox

One bullet added to `docs/BACKLOG-INBOX.md` under "Raised later (audit markets):" (finding 5, ENGINE-BACKLOG 1036 seen again).

## Fix pass

Fixer: Opus, from `2c72aeba`. Each basis below is the fixer's own, checked before the edit. No graded key, slip value, hidden test or solution changed.

1. **fixed differently**. `homework-1` `items[6]` `simple` now reads "6.67% solves $1000(1 + 1.5r) = 1100$: the £100.00 gain spread over the average wait of 1.5 years. That is simple interest. Compounding needs the quadratic." Basis: $0.10/1.5 = 0.06667$, and $(1100/1000 - 1)/1.5$ gives the same; the slip band 0.0667 ± 0.0001 stays clear of the key 0.065965 ± 0.00006. Simple discounting of each payment, $550/(1+r) + 550/(1+2r) = 1000$, gives 6.74% (brentq), outside the band, so the line names the mean-wait equation, not that one.
2. **fixed differently**. `l8` `screens[5]` option `up` why: "You halved only the £50 gain, leaving £125. Each year applies to the value at its start, so the fall halves all £150." Basis: $150 - 0.5 \times 50 = 125$; the old line's mistake gives $100 + 50 - 50 = 100$. Chosen over the product-of-returns reading as the slip a learner who tracks pounds makes.
3. **fixed**. `l13` `summary.ideas[2]` now starts "Ignoring interest,". Basis: $R_E = -1$ in $R_E = LR_A - (L-1)r$ gives $R_A = -(1 - (L-1)r)/L = -0.475$ at $L = 2$, $r = 5\%$.
4. **fixed differently**. `l5` `screens[3]` prose: "UK and US government bonds pay coupons half-yearly, though many euro-area bonds pay yearly." Basis: gilts (UK DMO) and Treasury notes and bonds (TreasuryDirect) pay every six months; Bunds, OATs and Bonos pay annually. "Most" is arguable by value outstanding, so the line names markets instead of a majority.
5. **fixed**. The five `byKey.error` lines now read "Your code could not be run. Check the syntax: brackets, colons and indentation."; `homework-1` `items[5]` `generic` gains "If a test is stopped for running too long, check that the loop changes `lo` or `hi` every time." Basis: own run through `app/tools/code-runner.mjs` (Pyodide 0.27.7, script `scratchpad/fix-mkts13r2/err.mjs`): every starter, including the `homework-1` loop that never ends and `pass` in its place, gives `test-1`; a missing colon (`l4`, `l5`, `homework-1`), a bad indent (`homework-1`) and an unclosed bracket (`homework-2`) give `error`; the solution gives none. The `generic` line now has three sentences.

Script: `docs/reports/markets-L1-3-concepts-r2.py` re-points the two checks that encoded the old text of findings 1 and 2 (docstring says so) and adds one text check: 204 checks, exit 0. `markets-L1-3-concepts.py` and `markets-L1-3-fixread.py` exit 0.

Gates: validator 0 errors; voice scan 35 on the six edited files 0 and 0; `run-number-scripts --only markets` 1 passed; `grade-all --code --file` on each edited file 0 failures; playthrough of `l4`, `l5`, `l8`, `l13`, `homework-1`, `homework-2`, desktop and `--mobile`, all passed.
