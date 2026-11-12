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

## Fix pass

Fixer: Opus, own basis per finding (sources named, or a derivation recomputed with sympy and scipy in a scratch run, not with the auditor's script).

1. `review-2` `r-pareto-mean` slip `half`: fixed. Changed the slip value (0.5 to 0.6667, id and tol kept) and the feedback to the auditor's text, so the named route gives the slip. Basis: $\int_1^\infty 2x^{-4}\,dx = [-\tfrac{2}{3}x^{-3}]_1^\infty = \tfrac23$, sympy `2/3` and `quad` 0.66667; no route to 0.5 is natural, so the value moved, not the route. 0.6667 is clear of the key 2 and the slip 1.
2. `l1` `screens[7]`: fixed. Basis: Bienaymé, $\operatorname{Var}(\sum I_i) = \sum \operatorname{Var} I_i + \sum_{i \ne j} \operatorname{Cov}$; zero covariance suffices (Ross, A First Course in Probability, 7.4).
3. `l8` `screens[0]` `drop`: fixed. Basis: $\tfrac12(100 + 50) = 75$, the mean move size; $\tfrac12(100 - 50) = 25$ is the true mean move.
4. `l10` `screens[3]` `flipped`: fixed. Basis: Markov's $E[X]/a$ exceeds 1 whenever $a < E[X]$ and is then valid but empty (here $10/2 = 5$).
5. `l10` `summary.trap`: fixed. Basis: $X \ge 0$ is sufficient; $X = \pm 1$ equally likely breaks it at $a = 1$ (0.5 against 0), while $N(1, 1)$ at $a = 3$ keeps it (0.0228 against 0.333).
6. `l7` `screens[4]`: fixed. Basis: $\Phi(-0.5)/\Phi(-2) = 0.30854/0.02275 = 13.56$.
7. `l3` `screens[4]` `zero`: fixed. Basis: $e^{-1.5} = 0.2231 > 0.2$, one in 4.48.
8. `problems-3` `p-maker-days` part 3 `why`: fixed. Basis: Lindeberg-Lévy needs only iid with finite variance (Durrett, Probability: Theory and Examples, 3.4.1); $np(1 - p) = 250 \times 0.02275 \times 0.97725 = 5.56$, below 10.
9. `problems-3` part 1 explain: fixed with different text: `One trade alone loses often; a whole day loses only about one day in 44.` "Once in 44" left the unit implicit. Basis: $1/0.02275 = 43.96$; 5.69 days in 250.
10. `l9` `screens[0]`: fixed. Basis: $\bar X_n - 3.5 = \tfrac1n \sum (X_i - 3.5)$ with the sum of sd $1.708\sqrt n$, so the miss shrinks like $1/\sqrt n$; small steps alone do not converge (harmonic sum).
11. `l11` `screens[8]` third sentence: fixed. Basis: $t_2$ has $\int_{|x|<u} x^2 f \sim 2 \ln u$, slowly varying, so it lies in the normal domain of attraction with infinite variance (Feller vol. 2, IX.8 and XVII.5).

Siblings: none of the eleven errors repeats in review, homework or problems echoes (grep over levels 1 to 3). "The binomial needs independence" (`l1`) left: it states the model's assumption, not a theorem's hypothesis.

### Unverified market remarks

- `l9` `screens[7]`: softened to a hypothetical, `A P&L with a tail this fat would behave the same way.` Basis: for iid draws with $E|X| = \infty$ the average does not converge (Durrett 2.4, converse of the strong law).
- `l9` `screens[8]`: replaced with arithmetic, `Over 20 trades the average is fuzzy by about 0.45%, enough to hide an edge of 0.1% a trade.` Basis: $2/\sqrt{20} = 0.447$, so 0.1% is under a quarter of one sd. ("return" dropped to meet the 20-word target.)
- `l10` `screens[3]`: softened to a condition, `If volume seldom strays far from 2 million, the true chance is much smaller.` Basis: Chebyshev, sd 1 million gives at most $1/64$.
- `l10` `screens[8]`: replaced with a computed model, `A fat-tailed model sits between: a Student $t$ with 4 degrees of freedom expects about 3.` Basis: unit-sd $t_4$, $2\,P(T_4 > 3\sqrt2) = 0.01324$, times 250 is 3.3 (scipy); $t_3$ and $t_5$ give 3.5 and 2.9.

### l11 `screens[8]`, "summing 20 days thins the tails"

Condition stated: the first sentence now reads `In real returns, summing 20 days thins the tails, so monthly returns look more normal than daily ones.`, and the sibling `why` of option `further` reads `In real returns, summing pulls the shape towards the bell.` Basis: the auditor's note holds on my own run, a normal-shock GARCH(1,1) (0.02, 0.08, 0.90) over 2 million days gives excess kurtosis 1.32 daily, 1.67 at 20 days. For real data it is Cont (2001), Quantitative Finance 1, stylised fact 4 (aggregational Gaussianity). The key is unchanged.

### Gates

- `limits-thm-L1-3-concepts-r2.py` exit 0 (226 checks, 0 failed); `limits-thm-L1-3-concepts.py`, `problems-limits-thm-numbers.py`, `fluency-limits-thm-numbers.py` and the three perf scripts exit 0. No assertion needed changing.
- Validator 0 errors, 5024 warnings (one new O2 warning: the 28-word `l9` `screens[0]` sentence, kept whole because splitting it would make four sentences). `content/manifest.json` unchanged.
- Voice scan 35: 0 and 0.
- Playthrough with `--local-cdn`, desktop and `--mobile`: `l1`, `l3`, `l7`, `l8`, `l9`, `l10`, `l11`, `--set review-2`, `--problems problems-3`, all "All passed", 0 relaunches.

## Fix-pass read

Commit read: `d1f59ba8` ("limits-thm L1-3 audit round 2: fix pass"), course folder only, nine files, 17 changed lines. Read blind: the audit, its ledger, the concepts scripts and the earlier reviews were not opened. Each changed string was read in its screen or item as it now stands. Figures were recomputed in `docs/reports/limits-thm-L1-3-fixread-r2.py` (exit 0, 0 failed), which also runs the voice gate on the changed strings (no exclamation mark, em-dash or lesson number; longest sentence 28 words; no explanation over three sentences).

| # | File | JSON path | Claim | Verdict | Basis |
|---|---|---|---|---|---|
| 1 | l1-counting-successes | `screens[7].explain.text` | Without independence the covariances can be non-zero, and then the sum $20p(1-p)$ is wrong | correct | $\operatorname{Var}(\sum I_i) = \sum \operatorname{Var}(I_i) + 2\sum_{i<j}\operatorname{Cov}(I_i, I_j)$ (Casella and Berger, Thm 4.5.6). "Can" is right, since uncorrelated dependent trials keep the sum. Covariances of mixed sign could cancel exactly; too fine to matter here. Agrees with the summary trap. |
| 2 | l10-bound-that-holds | `screens[3].feedback.byKey.flipped` | $10/2 = 5$; a bound of 5 says nothing since no probability exceeds 1; Markov is $2/10$ | correct | Slip value 5 = threshold over mean. A bound above 1 is true but vacuous, which is what "says nothing" states. Key 0.2 matches. Three sentences. |
| 3 | l10-bound-that-holds | `screens[3].explain.text` | If volume seldom strays far from 2 million, the true chance is much smaller than 0.2 | correct | Now a conditional. Markov is attained only by the two-point law on 0 and 10 (chance 0.2 at 10); any law concentrated near 2 puts far less mass at 10. "Safe, not sharp" still follows. |
| 4 | l10-bound-that-holds | `screens[8].explain.text` | A Student $t$ with 4 degrees of freedom expects about 3 such days | correct | The screen fixes the event (more than 3 sd from the mean, so the model's own sd, two-sided) and 250 days. sd of $t_4$ is $\sqrt 2$; $250 \times P(\lvert T\rvert > 3\sqrt2) = 3.31$ (scipy; simulation of 4m draws 3.31). Rounds to 3. Reading "3" as scale units would give 10.0, but the screen says sd. |
| 5 | l10-bound-that-holds | `screens[8].explain.text` | "A fat-tailed model sits between" the normal's 0.7 and the cap's 27.8 | imprecise | Below the cap always (Chebyshev). Above the normal is not general: by own sd, $t_\nu$ gives 3.46, 3.31, 2.60 for $\nu = 3, 4, 6$, but 0.60 at $\nu = 2.05$ and 0.13 at $\nu = 2.01$, under the normal's 0.7. Very heavy tails inflate the sd itself. See finding 1. |
| 6 | l10-bound-that-holds | `summary.trap` | Markov can fail for variables that can be negative | correct | $X = -3$ or $5$, each with chance $\tfrac12$: $E[X] = 1$, $P(X \ge 5) = 0.5 > 1/5$. It need not fail (shift a non-negative variable slightly), so "can" is right. Agrees with the formula note "needs $X \ge 0$". |
| 7 | l11-sums-look-normal | `screens[8].widget.options[2].why` | In real returns, summing pulls the shape towards the bell | correct | Cont (2001), "Empirical properties of asset returns", section 2, fact 4 (aggregational Gaussianity). Stated as an observation about data, not as the theorem. |
| 8 | l11-sums-look-normal | `screens[8].explain.text` (sentence 1) | In real returns, summing 20 days thins the tails, so monthly returns look more normal than daily ones | correct | Same source; also Campbell, Lo and MacKinlay, section 1.4.2 (kurtosis falls from daily to monthly). "Look more normal" does not claim monthly returns are normal, so no overclaim. Simulation: clustered fat-tailed days have excess kurtosis 3.1 daily, 2.0 over 20 days, 0.15 if the days are shuffled, which also supports the unchanged sentence 2. |
| 9 | l11-sums-look-normal | `screens[8].explain.text` (sentence 3) | Fat tails with infinite variance can block it entirely | correct | Stable laws with index below 2 keep their shape under summing (Feller vol. 2, ch. XVII; Cauchy check in the script). "Can" is right: a law with infinite variance can still lie in the normal domain of attraction under another scaling. Matches the summary's "can block". |
| 10 | l3-rare-events | `screens[4].feedback.byKey.zero` | More than one module in five is clean | correct | $e^{-1.5} = 0.2231 > 0.2$. |
| 11 | l7-bell-curve | `screens[4].explain.text` | Dividing by 16 makes losing years look nearly 14 times likelier | correct | $\Phi(-0.5)/\Phi(-2) = 0.30854/0.02275 = 13.56$; from the displayed figures $0.3085/0.0228 = 13.53$. |
| 12 | l8-lognormal | `screens[0].feedback.byKey.drop` | 75 is the average size of the two moves, $\tfrac12(100 + 50)$, not a price | correct | Moves are $+100$ and $-50$; mean absolute move 75. Key $\tfrac12(200 + 50) = 125$. Slips 100 and 75 are distinct from the key. |
| 13 | l9-averages-settle | `screens[0].explain.text` | Misses above and below 3.5 partly cancel and the average divides what is left by $n$ | correct | $\bar X_n - 3.5 = \tfrac1n\sum (X_i - 3.5)$; the sum is of order $\sqrt n$ (simulated mean absolute sum 42.9 at $n = 1000$ against 1,500 with no cancelling). Caption figures 4.50, 2.60, 3.70 and 3.56, 3.43, 3.50 match the canvas data. One sentence of 28 words, under the gate. |
| 14 | l9-averages-settle | `screens[7].explain.text` | A P&L with a tail this fat would behave the same way | correct | Hypothetical. St Petersburg has $P(X \ge x) \approx 1/x$ and no finite mean; the law of large numbers for iid draws needs $E\lvert X\rvert < \infty$ (Durrett, Thm 2.4.1). Agrees with the summary note. |
| 15 | l9-averages-settle | `screens[8].explain.text` | Fuzz of about 0.45% over 20 trades is enough to hide an edge of 0.1% a trade | correct | $2\%/\sqrt{20} = 0.447\%$; the edge is 0.22 sd of the average, and a normal average would come out at or below zero about 41% of the time. $2\%/\sqrt{2000} = 0.0447\%$; ratio 10. |
| 16 | problems-3 | `items[0].parts[1].explain.text` | A whole day loses only about one day in 44 | correct | $1/0.0228 = 43.9$; $1/\Phi(-2) = 44.0$. "About" covers the normal approximation. The wording is slightly awkward (a day losing a day) but not wrong. |
| 17 | problems-3 | `items[0].parts[3].widget.options[2].why` | The theorem is a limit, and at this $n$ the bell still fits poorly | correct | $np(1-p) = 5.57 < 10$; skew of $\text{Bin}(250, 0.0228)$ is 0.40; normal 0.0537 against exact 0.0626 and Poisson 0.0648. No longer states spread as a condition of the theorem. Agrees with the part's explanation. |
| 18 | review-2 | `items[4].widget.wrong[1].value` (`r-pareto-mean`, id `half`) | Slip value 0.6667 | correct | $\int_1^\infty 2x^{-4}\,dx = \left[-\tfrac{2}{3x^3}\right]_1^\infty = \tfrac23$. Key $\int_1^\infty 2x^{-2}\,dx = 2$; slip `area` $\int_1^\infty 2x^{-3}\,dx = 1$. Values 2, 1 and 0.6667 are pairwise further apart than the 0.005 tolerances. The id `half` no longer describes the value, but ids are not shown to learners. |
| 19 | review-2 | `items[4].feedback.byKey.half` | "You divided by $x$: $\int_1^\infty \tfrac{2}{x^4}\,dx = \tfrac23$. Multiply by $x$ instead, giving $\tfrac{2}{x^2}$." | correct | $f(x)/x = 2/x^4$, integral $\tfrac23$, which is this slip's value; $x f(x) = 2/x^2$ is the key's integrand. Agrees with the `accept` text and the explanation. |

Counts: 19 rows. `correct` 18, `imprecise` 1, `wrong` 0, `misleading` 0, `unverified` 0.

Sweeps with nothing to report: frequency phrases against their numbers (rows 10, 11, 16); sufficient-as-necessary and dropped conditions (rows 1, 6, 9, 14, 17); bounds above 1 (row 2); contradiction with the same screen or the summary; voice rules. No changed sentence touches lognormal mean against median.

### Findings

1. l10-bound-that-holds.json | `screens[8].explain.text` | imprecise | minor | "A fat-tailed model sits between" reads as a rule for every fat-tailed model, and the lower half of it is not general. | The count of 3 sd days is measured in the model's own sd, and very heavy tails inflate that sd. A Student $t$ with $\nu$ degrees of freedom expects 3.46, 3.31 and 2.60 days in 250 for $\nu = 3, 4, 6$, but 0.60 for $\nu = 2.05$ and 0.13 for $\nu = 2.01$, both under the normal's 0.7 (`250 * 2 * t.sf(3 * sqrt(nu/(nu-2)), nu)`, printed by the script). The example itself is right: 3.31 rounds to 3. | Replace the second sentence with: `A fat-tailed model can sit between: a Student $t$ with 4 degrees of freedom expects about 3.` The explanation stays at three sentences.
