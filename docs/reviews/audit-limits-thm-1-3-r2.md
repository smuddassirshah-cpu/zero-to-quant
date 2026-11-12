# Concept audit, round 2 (blind): limits-thm levels 1 to 3

Auditor: fresh Fable reader, blind to every earlier review, report and script of this course until the ledger and the findings below were committed (commit "WIP: limits-thm L1-3 round 2 ledger and findings").

Scope read in full: lessons `l1-counting-successes` to `l13-approximating-binomial`, `review-1` to `review-3`, `homework-1` to `homework-3`, `problems-1` to `problems-3`, `fluency-l1-counting-successes`, `fluency-l7-bell-curve`. Every screen, item, hint, `why`, `byKey` line, `explain`, model answer, rubric, wrong option, slip value and code solution.

- Ledger: `docs/reports/audit-limits-thm-1-3-r2-ledger.md`, 507 hand-judged rows: 492 correct, 1 wrong, 9 imprecise, 1 misleading, 4 unverified.
- Script: `docs/reports/limits-thm-L1-3-concepts-r2.py`, 226 checks. It recomputes the graded keys and slip values the ledger marks "script", runs the four code solutions against their hidden tests (and checks each starter fails), reads the embedded chart data that the prose quotes, and runs Monte Carlo checks for the empirical claims.

## Findings

Pattern: `N. file | JSON path | severity, tag | problem | evidence and basis | exact fix`.

1. `review-2.json` | `items[4]` (`r-pareto-mean`) `widget.wrong[1]` (`half`, value 0.5) with `feedback.byKey.half` | wrong, minor | The feedback says "You integrated $\tfrac{2}{x^3}$ times $\tfrac{1}{x}$", but that integral is not 0.5. | $\int_1^\infty \tfrac{2}{x^3}\cdot\tfrac{1}{x}\,dx = \left[-\tfrac{2}{3x^3}\right]_1^\infty = \tfrac23$. So a learner who divides by $x$ types 0.6667 and gets only the generic line, and a learner who types 0.5 is told a route that does not give 0.5. Basis: direct integration; script check KNOWN F1. | Change `widget.wrong[1].value` from `0.5` to `0.6667` (keep `"tol": {"abs": 0.005}` and the id), and set `feedback.byKey.half` to: `You divided by $x$: $\int_1^\infty \tfrac{2}{x^4}\,dx = \tfrac23$. Multiply by $x$ instead, giving $\tfrac{2}{x^2}$.`

2. `l1-counting-successes.json` | `screens[7].explain.text`, third sentence | imprecise, minor | "Without independence the covariances stay and this sum is wrong" states independence as necessary for variances to add. It is only sufficient. | $\operatorname{Var}(\sum I_i) = \sum \operatorname{Var}(I_i) + \sum_{i \ne j}\operatorname{Cov}(I_i, I_j)$, so zero covariances are enough, and dependent variables can have zero covariance (C&B section 4.5: $X$ and $X^2$ for symmetric $X$). Tagged minor because the same explain names the true mechanism, zero covariances, one sentence earlier. Script check KNOWN F2. | Replace the third sentence with: `Without independence the covariances can be non-zero, and then this sum is wrong.`

3. `l8-lognormal.json` | `screens[0].feedback.byKey.drop` (slip value 75) | imprecise, minor | "You averaged the gain and the loss as $+100$ and $-50$, then took off 50" is not a route a learner takes. Averaging $+100$ and $-50$ gives $+25$, which is the right route to £125. | 75 is $\tfrac12(100 + 50)$, the average size of the two moves, or $100 - 25$. The line reaches 75 only as $100 + 25 - 50$. Basis: arithmetic; script check KNOWN F3. | Set the line to: `75 is the average size of the two moves, $\tfrac12(100 + 50)$, not a price. Average the prices: $\tfrac12(200 + 50)$.`

4. `l10-bound-that-holds.json` | `screens[3].feedback.byKey.flipped` | imprecise, minor | "A probability bound cannot exceed 1" is false as a rule. Markov's bound $E[X]/a$ exceeds 1 whenever $a < E[X]$; it is then valid and says nothing. | With mean 2 and $a = 1$ the bound is 2. The quiz and the problem set use the true form, "a probability cannot exceed 1". Basis: Ross section 8.2; script check KNOWN F4. | Set the line to: `You divided the threshold by the mean. A bound of 5 says nothing, since no probability exceeds 1. Markov is $2/10$.`

5. `l10-bound-that-holds.json` | `summary.trap` | imprecise, minor | "Markov fails for variables that can be negative" states a failure that is only possible. The bound is not guaranteed; for many such variables it still holds. | Screen 5 has it right ("the bound fails here", for one example). Basis: the hypothesis $X \ge 0$ is sufficient, not necessary; script check KNOWN F5. | Set `summary.trap` to: `Markov can fail for variables that can be negative, and a bound is a ceiling, not the probability.`

6. `l7-bell-curve.json` | `screens[4].explain.text`, third sentence | imprecise, minor | "13 times likelier" truncates the ratio. | $\Phi(-0.5)/\Phi(-2) = 0.3085/0.02275 = 13.56$. Script check KNOWN F6. | Replace the third sentence with: `Dividing by 16 would make losing years look nearly 14 times likelier.`

7. `l3-rare-events.json` | `screens[4].feedback.byKey.zero` | imprecise, minor | "About one module in five is clean" for a chance of 0.2231, which is one in 4.5. | $e^{-1.5} = 0.2231$. Script check KNOWN F7. | Set the line to: `A mean of 1.5 does not force a bug. More than one module in five is clean.`

8. `problems-3.json` | `items[0].parts[3].widget.options[2].why` | imprecise, minor | "The theorem needs enough spread" turns a rule of thumb about a finite-sample approximation into a condition of the central limit theorem. The theorem holds for these draws; the fit at $n = 250$ is what is poor. | Lindeberg-Lévy needs only iid draws with finite variance (Durrett 3.4.1). Lesson 13 says "rule of thumb" each time. Script check KNOWN F8. | Set the `why` to: `The theorem is a limit, and at this $n$ the bell still fits poorly. With $p = 0.0228$ the bars lean against 0, and $np(1 - p)$ is below the usual 10.`

9. `problems-3.json` | `items[0].parts[1].explain.text`, third sentence | misleading, minor | "the day almost never does" for a chance of 0.0228. The next part counts 5.7 losing days a year on that chance. | $1/0.0228 \approx 44$ days. Script check KNOWN F9. | Replace the third sentence with: `One trade alone loses often; a whole day loses about once in 44.`

10. `l9-averages-settle.json` | `screens[0].explain.text`, third sentence | imprecise, minor | "Each new roll moves a long average very little, so the lines settle near $3.5$" reaches the right result by an argument that does not give it. Small steps alone do not make a sequence converge, and they say nothing about where. | Steps of size about $1/n$ can sum without limit; the St Petersburg average in screen 8 also moves little on most games and does not settle. The real reason is that the misses cancel: the sum of misses grows like $\sqrt n$ and is divided by $n$ (screen 6 of the same lesson). Script check KNOWN F10. | Replace the third sentence with: `The misses above and below 3.5 partly cancel and the average divides what is left by $n$, so the lines settle near $3.5$, the mean of one roll.`

11. `l11-sums-look-normal.json` | `screens[8].explain.text`, third sentence | imprecise, minor | "Fat tails with infinite variance would block it entirely" states as certain what is only possible. Some infinite-variance laws are still attracted to the normal, with a scaling other than $\sigma\sqrt n$. | Student $t$ with 2 degrees of freedom has infinite variance, and its sums divided by $\sqrt{n \ln n}$ tend to a normal (Feller vol. 2, XVII.5). The script simulates sums of 20,000 such draws and finds normal quantile ratios. The lesson's own summary says "can block". Script check KNOWN F11. | Replace the third sentence with: `Fat tails with infinite variance can block it entirely.`

Severity count: 1 wrong, 9 imprecise, 1 misleading. Tags: 0 serious, 11 minor.

## Unverified (not passed, no fix proposed)

These are empirical remarks about markets that I could not establish without data. None is a definition, method or graded answer.

- `l9-averages-settle.json` `screens[7].explain.text`: "Some fat-tailed P&Ls behave like this."
- `l9-averages-settle.json` `screens[8].explain.text`: a fuzz of 0.45% is "more than most real edges".
- `l10-bound-that-holds.json` `screens[3].explain.text`: "Real volume is far less spread, so the true chance is much smaller."
- `l10-bound-that-holds.json` `screens[8].explain.text`: "Real returns sit between, often a few a year."

## Notes on checks

- Checks that fail on purpose: the eleven `KNOWN F1` to `KNOWN F11` checks, one per finding. Each tests for the exact string or value quoted above, so it passes once the fix is applied. Every other check passes: the script prints `226 checks, 11 failed` and exits 1 today, and will exit 0 after the fix pass.
- Aggregational normality (`l11` screen 9). The lesson's claim, that 20-day returns look closer to normal than daily ones and that clustering slows the approach, is the documented stylised fact (Cont 2001, facts 4 and 6). My first simulation used a GARCH(1,1) with normal shocks, and there the 20-day excess kurtosis (about 0.84 to 1.1) is above the daily one (0.78): clustering alone can fatten the tails of sums before it thins them. With fat-tailed daily shocks ($t_8$), the realistic case, the claim holds clearly (daily excess kurtosis falls by more than 30% at 20 days, and stays well above the shuffled series). The script checks the fat-tailed case and prints the normal-shock figures as a note. No finding: the lesson describes real returns, which are fat-tailed day by day.
- Recomputed by hand or script: every graded key, every `wrong[]` value and every option figure in scope. No slip value collides with its key or with another slip within tolerance.
- Conditions of the limit theorems: the weak law is stated for iid draws with a finite mean, with "weaker conditions also give the law" in the summary note; the central limit theorem is stated for iid draws with finite variance, with "other forms relax the first two". Chebyshev is stated with a finite mean and variance, Markov with $X \ge 0$. The Sharpe ratio is defined on excess returns with the risk-free rate set to 0 and said so; VaR is a positive loss from today's value and said so in each item; the $t$-ratio uses a known $\sigma$ with the sample sd noted once.

## Gates

- Validator, from `app/`: `node tools/validate.mjs` gives `0 errors, 5023 warnings`. `content/manifest.json` restored afterwards.
- Number scripts: `problems-limits-thm-numbers.py` exit 0 (1,539 checks, 0 failures); `fluency-limits-thm-numbers.py` exit 0 (3,537 checks, 0 failures); `limits-thm-1-perf-numbers.py` exit 0 (41 of 41); `limits-thm-2-perf-numbers.py` exit 0 (64 of 64); `limits-thm-3-perf-numbers.py` exit 0 (67 of 67).
- Concepts script: `limits-thm-L1-3-concepts-r2.py` exit 1, 226 checks, the 11 on-purpose failures only.
- Playthrough with `--local-cdn`, selectors only: 13 lessons, 6 review and homework sets (`--set`), 3 problem sets (`--problems`), 2 fluency sets (`--fluency`). Desktop: all three runs exit 0, "All passed" (19 lesson and set lines, 3 problem sets, 2 fluency sets). `--mobile`: the same three runs exit 0, "All passed". Browser relaunches: 0.

## Overlap with earlier reads

Read after the WIP commit (`2a840cd3`): `docs/reviews/audit-limits-thm-1-3.md` with its Fix pass, Fix-pass read and Follow-up; `docs/reviews/review-1.5.md` (limits-thm section and fix pass); `docs/reviews/review-problems-1.5-c.md` and `-d.md` (sets 1 to 3); `docs/reviews/review-perf-retrofit-9.md` (the three derivation items); the round 1 ledger and concepts script. Only conceptual findings are counted, as in round 1.

| | count | findings |
|---|---|---|
| This round only | 11 | all 11 above (1 wrong, 9 imprecise, 1 misleading; all minor) |
| Both | 0 | none |
| Earlier reads only | 40 | round 1 audit 28; its fix-pass read 1 (with one sibling, 4a); earlier reviews 11. All were fixed before this read, so none could be found here |

For each `wrong` of this round, whether an earlier read found it:

- Finding 1 (`review-2` `r-pareto-mean`, slip `half`): no earlier read found it. `review-1.5.md` does not mention the item; the round 1 ledger has no row for this slip, and no number script recomputes it (`grep pareto` over `docs/reports/limits-thm*` and the round 1 ledger returns nothing). Round 1 states that every `wrong[]` value and slip line was recomputed; this one was missed.

New `wrong` that no earlier read found: 1 (minor) in three levels.

Other points from the comparison.

- None of the 11 strings was written by a fix pass. `git log -S` puts each at the original authoring commits (20 Oct for the lessons and `review-2`; 10 Nov for `problems-3`).
- The 40 earlier findings were re-read here as ordinary ledger rows, and every fixed text holds: for example `l4` `screens[7]` (first factor 0.8), `l7` `screens[3]` (once every two months), `l12` `screens[5]` (excess return, rate taken as 0), `l11` `screens[4]` ("this form assumes"), `l9` `summary.formula.note`, `l13` `screens[9]` (`nocc` 0.0119), `problems-2` `p-default-drag` slips 0.5438 and 0.5173, homework-3 `items[9]` exact figures (checked here to $n = 600$).
- Neighbouring gaps. Round 1 finding 13 corrected the second sentence of `l11` `screens[8].explain`; finding 11 here is the third sentence of the same explain. Round 1 findings 4, 5 and 11 removed "needs" from the limit theorems; findings 2, 5 and 11 here are the same class (a sufficient condition written as necessary) in `l1`, `l10` and `l11`. Round 1 finding 2 was a frequency phrase; findings 6, 7 and 9 here are the same class.
- The round 1 fix-pass read simulated the clustering claim with normal shocks (20-day excess kurtosis 1.03 against 0.07 shuffled) and so checked only "slower than for independent days". Neither earlier read tested "summing 20 days thins the tails" against the daily figure; the note above records that it holds for fat-tailed daily shocks and not for normal ones.

## Inbox

Bullets for the orchestrator to file; `docs/BACKLOG-INBOX.md` is not edited here.

- Number scripts: the review sets of limits-thm levels 1 to 3 have no number script (`problems-limits-thm-numbers.py`, the fluency script and the three perf scripts cover problems, fluency and the derivation items only). `review-2` `r-pareto-mean` `half` (0.5 against a named route worth 2/3) passed every gate and two reads. Add review and homework slip values to a course number script, each recomputed from the route its `byKey` line names. This is the slip-naming class again.
- Lint, warning only: flag "without independence", "needs independence", "only for independent", "fails for" and "would block" in content strings for a manual read. Three of this round's findings (2, 5, 11) are a sufficient condition written as a necessary one.
