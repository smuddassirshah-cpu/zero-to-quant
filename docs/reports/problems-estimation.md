# Problem sets: estimation (brief `docs/briefs/chained.md`)

Files: `app/content/courses/estimation/problems-1.json`, `problems-2.json`, `problems-3.json`. Numbers: `docs/reports/problems-estimation-numbers.py` (exit 0, 884 checks, 0 failures). Commits: f73605b (level 1), d95515b (level 2), ce56825 (level 3), then this report.

Lessons read first: every screen and quiz of l1 to l12, and review-1 to 3 and homework-1 to 3, for settings to avoid.

## Sets

| set | item | parts (typed / choice) | lessons drawn on | difficulty |
|---|---|---|---|---|
| problems-1 | p-ping-latency | 4 (4 / 0) | l1, l2, l3 | 3 |
| problems-1 | p-route-delays | 4 (4 / 0) | l2, l4 | 4 |
| problems-1 | p-sulphur-labs | 5 (5 / 0, one `expression`) | l1, l2, l4 | 5 |
| problems-1 | p-reference-mass | 5 (4 / 1) | l1, l2, l3 | 4 |
| problems-2 | p-robot-deliveries | 4 (4 / 0, one `expression`) | l5, l6, l7 | 3 |
| problems-2 | p-tank-sensor | 4 (4 / 0) | l5, l6, l7 | 4 |
| problems-2 | p-currency-vol | 5 (5 / 0) | l6, l8 | 4 |
| problems-2 | p-ride-waits | 4 (4 / 0, one `expression`) | l5, l6, l7 | 5 |
| problems-3 | p-email-clicks | 4 (3 / 1) | l9, l10 | 3 |
| problems-3 | p-three-month-fund | 4 (4 / 0) | l9, l11 | 4 |
| problems-3 | p-ticket-bot | 4 (4 / 0) | l9, l12 | 5 |
| problems-3 | p-routing-test | 4 (3 / 1) | l9, l10 | 4 |

Typed parts: level 1 17 of 18, level 2 17 of 17, level 3 14 of 16. Each choice part is a judgement: why the known mean allows dividing by $n$, whether the old click rate is ruled out, whether the test shows A slips more.

Chains. Level 1: pings to $\bar x$, $s^2$, the standard error and the pings for 1 microsecond; delays to $\operatorname{Var}(\bar X)$, the bias and MSE of $\tfrac12\bar X$, then the cut-off $\mu < \sqrt{3v}$ where shrinking wins; two labs to $\mathrm{MSE}(w)$, its best weight $\tfrac89$ and the blended MSE $\tfrac49$, below both labs; a reference mass to $SS$, the known-mean variance 76 and 19 readings. Level 2: a robot's likelihood, MLE, the boundary MLE under a claim and the ratio 3.03; a tank's MLE, a log-likelihood gap, the ratio $e^{1.125}$ and the tenth-likelihood range; weekly FX volatility to annual, its standard error and 123 weeks; exponential waits with a censored rider, whose tail chance doubles. Level 3: a click rate's SE, interval and verdict; the exact bootstrap SE of three returns, $\sqrt{2/3}$ of $s/\sqrt n$ (checked over all 27 resamples); a beta posterior's weight, the $n = 580$ that brings it within 0.01 of the MLE, and that gap in SEs; two routers' difference interval. Each later part restates the value it uses, and its `wrong` list holds the value the commonest slip in the part before gives (`carried`, or the named slip).

Judgement calls a reader may question: `p-reference-mass` part 4 (choice) feeds no number to part 5; it is the reason part 5 may use 76. `p-ticket-bot` is labelled 5 for the inequality in $n$ with the prior's size; part 3 states $w = n/(n + 20)$, which makes it gentler. l11 is drawn on through the exact bootstrap distribution, not a percentile interval, since a problem set has no code part.

Form. Every non-whole numeric part names its form ("Give your answer to n decimal places.", "Give a fraction, or a decimal to 4 places.", "Give a whole number."). Where a part restates a rounded value the key is what that value gives and the band also takes the exact route (7.84 from $\hat\sigma = 1.0874$ and from 1.09; 0.131 from SE 0.0150 and exact; $-0.10$ from 0.461; 123 weeks from 7.84 and from the unrounded 7.8414). The script checks those.

## Checks

| check | problems-1 | problems-2 | problems-3 |
|---|---|---|---|
| numbers script | 0 failures | 0 failures | 0 failures (884 checks in all) |
| validator | 0 errors; no warning on the file but `O2-long-sentence` (advisory, under 35 words) | same | same |
| playthrough `--local-cdn` | green (18 parts) | green (17 parts) | green (16 parts) |
| playthrough `--mobile` | green; 440 px shots read, no layout fault | same | same |
| voice scan 35 (course folder) | 0 and 0 | 0 and 0 | 0 and 0 |

## Fresh-check

At the gate: 0 hits on all three sets. Advisories: `SS = \sum(x_i - \bar x)^2`, `\sum(x_i - \mu)^2` and `\hat\sigma/\sqrt{2n}` shared with l3, l4, l6, l7, l9, l10 (taught formulas); 47, 32 and 48 shared with `exams/mock-oa-trader` a05 (a number sequence, coincidence). At `--min-run 8 --min-share 0`: 18, 25 and 22 hits, all form sentences ("give a fraction or a decimal to # places using # from part") or stock questions ("what is the lower end of the # confidence interval for the true", review-3 items[1], a different setting). The settings (pings, rail delays, two sulphur labs, a reference mass, a delivery robot, a tank sensor, weekly FX returns, censored ride waits, an email offer, a three-month fund, a ticket bot, two routers) are new to the course.

## Engine limits

Two bullets in `docs/BACKLOG-INBOX.md` under "Raised later (problems estimation)". None blocked a problem.
