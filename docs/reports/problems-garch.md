# Problem sets: garch levels 1 to 3 (brief `docs/briefs/chained.md`, `docs/briefs/chained-prompts.md`)

Files: `app/content/courses/garch/problems-1.json` to `problems-3.json`. Numbers: `docs/reports/problems-garch-numbers.py` (exits 0). Scratch generators: `<scratchpad>/author-garch/gen<n>.py`.

## Level 1 (Clustering: l1 to l4)

| item | parts (typed / choice) | lessons drawn on | difficulty |
|---|---|---|---|
| p-two-regime-tails | 4 (4 / 0) | l1, l4, l3 | 5 |
| p-stale-prices-scaling | 4 (4 / 0) | l2, l4 | 4 |
| p-eight-day-window | 4 (4 / 0) | l4, l3 | 3 |
| p-big-day-indicator | 4 (4 / 0) | l1, l2 | 5 |

16 parts, all typed. Every lesson appears, every problem draws on two or more. Skills: `gv-clustering`, plus `gv-forecast` where l4 is drawn on.

Chains: P1 spell lengths, then the long-run Turbulent share, then the mixed variance annualised, then the mixture's excess kurtosis from those shares and that variance. P2 band, then the weekly variance of a sum with lag-1 covariances, then the annual one, then the ratio to the $\sqrt{252}$ figure. P3 mean square, then the sample sd from it, then annualised, then excess kurtosis with $\tfrac78 s^2$. P4 conditional chance, then the indicator's lag-1 autocorrelation, then $LM = (n-1)R^2$, then the smallest count of 75 that rejects.

### Gates (level 1)

- Validator: 0 errors; no warning on `problems-1.json`.
- Voice scan 35 on the course folder: 0 and 0.
- Number script: exit 0 (250 direct checks, 103 numbers_lib checks for level 1).
- `fresh-check --file`: 0 hits after one fix (a `retold` error: the byKey line "Excess kurtosis subtracts the normal's 3." matched the l3 quiz and review wording; reworded in P1 and P3).
- `grade-all --file`: 0 failures (16 numeric widgets).
- Playthrough `--problems garch/problems-1 --local-cdn <pkgs>`: green with `--why` (40 typed slips routed) and with `--mobile`. Part shots at 440 px read: no overflow.

### Closest course material, and why each problem is not a walk through it (level 1)

- **p-two-regime-tails.** Closest: l1 screen 5 (Calm and Storm Markov cartoon, 0.98 and 0.95, storm length 20), review-1 item 0 (storm length with 0.97), l3 screen 7 (a mixture of calm and stormy normals fattens tails, B's theoretical 1.43). Only part 1 is the l1 task (mean spell length), with its own sentence: the lesson's explain "A run that ends with chance ... lasts 1/... days" was not reused (a first draft paraphrased it and was rewritten to a geometric-mean sentence). Parts 2 to 4 are new steps: the long-run share from two spell lengths, the mixed variance, and the mixture kurtosis computed from $3\sigma^4$; no screen computes a mixture's kurtosis. Verdict: clean.
- **p-stale-prices-scaling.** Closest: l4 screen 10 (order the $\sqrt{252}$ derivation, covariances dropped), l4 screen 8 (annualise 1% daily), l2 quiz 0 (band for 1,000 days). The lesson drops the covariance terms; this problem keeps one lag and counts neighbouring pairs (8 for a week, 502 for a year), a calculation no screen makes. Its setting (thin trading, positive lag-1 ACF) is new to the course. Verdict: clean.
- **p-eight-day-window.** Closest: l4 screen 3 (zero-mean against sample sd on B's 5 days, a table read), l3 screen 2 (kurtosis of eight returns $0, \pm 2$), review-1 item 2 and l3 quiz 0 (kurtosis of 10 and 4 symmetric values). Here the data are eight uneven returns with a non-zero mean; the sample sd is built from the mean square of part 1 through $\tfrac{n}{n-1}(\overline{r^2} - \bar r^2)$, which no screen uses, and the kurtosis divides by $\tfrac78 s^2$. Verdict: clean.
- **p-big-day-indicator.** Closest: l1 screen 4 (table of next-day shares after big moves in B, 27.8% against 4.5%), l2 screen 7 and quiz 2 (ARCH-LM, $LM = (n - q)R^2$), review-1 item 5 (LM with 10 lags). Part 1 is a conditional share from counts, which l1 reads off a table; parts 2 to 4 turn it into an indicator autocorrelation, an LM statistic and an inverted threshold count, a chain no screen follows. Verdict: clean.

Own-course grep (course folder, lessons, reviews and homework): 15.36, 4.54, 2.93% weekly, 21.20, 22.38, 28.33, 59.96 and the nouns Quiet, Turbulent, copper, crude, stale: 0 hits. 0.99, 0.96, 0.936, 1.673, 1.785 and 1,500 appear only inside canvas data arrays or as other quantities (a 99% VaR, day 1,500 of a crash): different roles.
