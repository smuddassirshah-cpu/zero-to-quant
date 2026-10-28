# Report: analysis level 2, "Sequences"

Course `analysis` (topic 1.10, strand pure), level 2, from `## Level 2` of `docs/briefs/analysis.md`. Lesson ids, names, objectives and skills are those of `app/content/courses/analysis/course.json`: l6 and l7 and l9 carry `an-sequences`, and l8 and l10 carry `an-sequences` and `an-reals`. The content was authored and committed earlier (commit `820ef79`, "report pending"), but the authoring agent's report write was refused. This report was written afterwards from the committed files. Every stated number was recomputed twice and every code widget was re-run. Notation follows level 1 (`l2-least-upper-bound`, `l3-completeness`): $\varepsilon$, $n \ge N$, the supremum test, and completeness by name. Proofs end with $\blacksquare$. No topic exam was written.

## Files

All in `app/content/courses/analysis/`.

| File | Screens | Quiz / items | Canvases | Notes |
|---|---:|---:|---|---|
| `l6-epsilon-and-n.json` | 12 | 4 | plane (dots $(n, a_n)$, band $2 \pm \varepsilon$ as an `area` between `L + eps` and `L - eps`, `vlines` moved by `derive`, an $\varepsilon$ control), table, console | drag $N$ to 48 at $\varepsilon = 0.1$, slide $\varepsilon$, $|a_n - 2| = \tfrac{5}{n+3}$ `expression`, threshold $\tfrac5\varepsilon - 3$ `expression`, $N = 498$ `numeric`, trap "closer to 2.5 every step", 5-line `order` with two distractors, $N$-depends-on-$n$ flawed line `choice`, $\max(1, \tfrac5\varepsilon - 3)$ `expression`, negation for $(-1)^n$ `choice`, `smallest_n` code, binomial-tree transfer `numeric` 301 |
| `l7-limit-laws-proved.json` | 12 | 4 | plane, table | drag $N$ to 31 for $a_n + b_n$, slide $\varepsilon$ for $N_1$ and $N_2$ (`choice`: take the larger), table 21, 41, 41, $\min(N_1, N_2)$ trap (tap rows), boundedness `choice` and 4-line `order`, add-and-subtract `choice`, facts used `multi`, product numbers table 801, 401, 801, 101, product `order` with a `same` group and two distractors, bounded-not-convergent and quotient `choice`, position-value transfer `numeric` £500.20 |
| `l8-bounded-and-monotone.json` | 11 | 4 | plane (cobweb stepped by a frames control), table, console | guess the limit 2 `numeric`, induction `order`, why roots keep order `choice`, supremum step `choice`, monotone convergence `order`, root 2 not $-1$ `choice`, Babylonian floor by AM-GM `choice`, $(1 + \tfrac1n)^n$ `choice`, $L = 2L$ trap, `iterate_sqrt` and `first_within` code, moving-average transfer `numeric` day 15 |
| `l9-subsequences.json` | 12 | 4 | plane (tappable dots), table, number-line (tappable nested halves) | tap the even-indexed dots, two limits mean divergence `choice`, which lists are subsequences `multi`, $n_k \ge k$ `choice`, subsequence-limit `order`, keep a half three times (ordered taps on intervals), length $\tfrac4{1024}$ `numeric`, why a good half exists `choice`, Bolzano-Weierstrass `order`, "bounded so convergent" trap, unbounded with a settling strand `choice`, regime-switching transfer `choice` |
| `l10-cauchy.json` | 12 | 4 | plane (band of width $\tfrac1N$ stepped by a frames control), table, console | the band shrinks `choice`, comparison $\tfrac1{k(k-1)}$ `choice`, telescoping `choice`, $N = 100$ `numeric`, which pairs `choice`, convergent implies Cauchy `order`, Cauchy implies bounded `choice`, Cauchy implies convergent `order`, triangle-inequality step `choice`, harmonic trap `table`, `harmonic_gap` and `cauchy_n` code, optimiser stopping-rule transfer `choice` |
| `review-2.json` | | 9 | table | difficulties 3, 3, 3, 2, 3, 2, 2, 2, 4; covers l6 ($N = 150$ for $\tfrac{4n-1}{2n+1}$; threshold $\tfrac1\varepsilon - 1$), l7 (product flawed line; sum-law $N = 41$), l8 ($\sqrt{6 + a_n}$ argument; limit 4), l9 ($\cos\tfrac{n\pi}{2}$ subsequence), l10 (which is Cauchy; Cauchy plus a convergent strand) |
| `homework-2.json` | | 8 | console | difficulties 3, 3, 4, 4, 4, 5, 4, 5; threshold `expression` $\tfrac5\varepsilon - 2$ for $n^2$, $N = 23$ `numeric`, product proof's $N = 1201$, $a_{n+1} = a_n^2$ fixed-point trap, Cauchy implies convergent `order`, "every convergent strand agrees" `order`, `first_n` code, `longform` (limit from the definition plus the product law; five 2-point rubric lines, full model answer) |

The quiz items (4 per lesson, difficulties 2 to 3) are as follows. l6: quantifier order, a constant sequence, $N = 60$ for $\tfrac{3n}{n+1}$, $\tfrac{(-1)^n}{n} \to 0$. l7: sum-law $N = 31$, the $\tfrac\varepsilon5$ for $5a_n$, $M = 6$, $(-1)^n \cdot \tfrac1n$ outside the product law. l8: monotone but divergent, limit at most 5, $a_{n+1} = \tfrac12a_n + 3$ limit 6, why the theorem says nothing about $(-1)^n$. l9: which is a subsequence, odd-term limit $-1$, $a_{k^2} \to 5$, two cluster points. l10: truncations of $\sqrt2$ in $\mathbb{Q}$, $N = 500$, $\sqrt n$ not Cauchy, the negated Cauchy condition.

## Which widget grades each proof step

- $\tfrac{2n+1}{n+3} \to 2$ (l6): the gap `expression` `\frac{5}{n+3}`; the threshold `expression` `\frac{5}{\varepsilon}-3`; $N$ at 0.01 `numeric` (498); written proof `order`, 5 lines, distractors "let $\varepsilon = 0.1$" and "choose $N = n + 1$"; the floor of 1 `expression` `\max(1, \frac{5}{\varepsilon}-3)` (switch at $\varepsilon = 1.25$, inside the tested range 0.3 to 3); divergence of $(-1)^n$ by the negated definition `choice`; $N$ chosen from $n$ by `choice` on a numbered `table`.
- Convergent implies bounded (l7): why only finitely many terms escape `choice`; proof `order`, 4 lines, distractors "$M = \sup$" and "$M = \max$ over every term".
- Sum law (l7): $N_1 = 21$, $N_2 = 41$ and $N = 41$ by `table`; "take the larger" `choice`; $\min$ line by `tap-regions`.
- Product law (l7): add-and-subtract `choice`; facts used `multi` (triangle inequality, $|xy| = |x||y|$, boundedness); numbers by `table`; proof `order`, 6 lines, with `same: [[p2, p3]]` for the two independent choices of index, and distractors $|a_nb_n - ab| \le |a_n - a||b_n - b|$ (its `why` names the missing cross terms) and $N = \min(N_1, N_2)$.
- Monotone convergence (l8): $P(n)$: $a_n < a_{n+1} < 2$ by induction `order` (5 lines, two distractors); the root step `choice`; the supremum step `choice`; theorem `order` (5 lines, distractors "terms get closer, so $L$ exists" and "$a_n = a_N$"); which root `choice`; Babylonian floor `choice`.
- Subsequences keep the limit (l9): $n_k \ge k$ `choice`; proof `order`, 4 lines, two distractors.
- Bolzano-Weierstrass (l9): halves by ordered `tap-regions` on number-line intervals; length `numeric`; a good half exists `choice`; proof `order`, 5 lines, distractors "perhaps equal to $n_k$" and "so $a_n \to x$".
- Cauchy (l10): comparison and telescoping `choice`; $N$ `numeric`; convergent implies Cauchy `order` (4 lines, two distractors); Cauchy implies bounded `choice`; Cauchy implies convergent `order` (4 lines, two distractors); triangle-inequality step `choice`; harmonic counterexample `table`.
- Whole proofs written out: homework `order` for Cauchy implies convergent and for "every convergent strand agrees", and the `longform`, rubric 2 + 2 + 2 + 2 + 2 = 10.

`\epsilon` and `\varepsilon`: `app/js/engine/grade.js` (line 165, item 437) rewrites `\epsilon`, ε and ϵ to `\varepsilon` before an expression is compared, so a learner's `\epsilon` grades the same as the authored `\varepsilon`. This pass confirmed that by reading the grader. The playthrough enters only the authored answers, so an `\epsilon` form was not typed in the browser in this pass.

## Validator

`node tools/validate.mjs` from `app/`: **0 errors**, 364 warnings, none in a level 2 file. The only analysis warning is the course's "not yet written" line for levels 3 to 5. Run again after the two text fixes below: still 0 errors.

## Playthrough

With `--local-cdn` set to the scratchpad `pkgs` folder, after the text fixes.

| Target | Result |
|---|---|
| `--lesson analysis/l6-epsilon-and-n` | ok, 16 checks, quiz 4/4 |
| `--lesson analysis/l7-limit-laws-proved` | ok, 16 checks, quiz 4/4 |
| `--lesson analysis/l8-bounded-and-monotone` | ok, 15 checks, quiz 4/4 |
| `--lesson analysis/l9-subsequences` | ok, 16 checks, quiz 4/4 |
| `--lesson analysis/l10-cauchy` | ok, 16 checks, quiz 4/4 |
| `--set analysis/review-2` | ok, 9 items, recorded 9 of 9 |
| `--set analysis/homework-2` | ok, 8 items, marked 8 of 8 right, 37 of 37 marks |

No screenshots were taken in this pass. The original run's layout faults are the "Raised later (analysis level 2)" bullets already in `docs/BACKLOG-INBOX.md`: table cells clipping long formulas, table `wrong[]` ids refused as `byKey` keys, unshuffled options, log-axis labels, interval colours in one row, and the `derive` floor nudge. Each has its workaround in the files.

## Code widgets

Each solution and each starter was run against its hidden tests in CPython (`code_check.py`), and the playthrough ran the solutions in Pyodide. Every starter is a body of `...` and fails every test.

| Widget | Tests | Solution passes | Starter passes |
|---|---:|---:|---:|
| l6 `smallest_n(eps)` | 10 | 10 | 0 |
| l8 `iterate_sqrt(a1, n)`, `first_within(eps)` | 11 | 11 | 0 |
| l10 `harmonic_gap(n)`, `cauchy_n(eps)` | 12 | 12 | 0 |
| homework `first_n(eps)` | 7 | 7 | 0 |

Expected values, each also recomputed by a second method:

- `smallest_n`: $\tfrac1{10}$ → 48, $\tfrac1{100}$ → 498, $\tfrac12$ → 8, 1 → 3, 2 → 1, $\tfrac3{100}$ → 164, $\tfrac5{51}$ → 49 (the gap at 48 equals $\varepsilon$), $\tfrac1{1000}$ → 4998, $\tfrac73$ → 1. These were checked by a direct scan for the last bad index.
- `iterate_sqrt`: (1, 1) → 1, (1, 2) → $\sqrt3$, (1, 3) → 1.9318516525781366, (1, 5) → 1.995717846477207, (0, 3) → 1.8477590650225735, (3, 4) → 2.0144902648738445. These were checked in 50-digit `Decimal`.
- `first_within`: 0.1 → 3, 0.01 → 5, 0.001 → 7, $10^{-6}$ → 12, 1 → 2, 2 → 1. These were checked by scanning `Decimal` iterates.
- `harmonic_gap`: 1 → $\tfrac12$, 2 → $\tfrac7{12}$, 3 → $\tfrac{37}{60}$, 10 → $\tfrac{155685007}{232792560}$, and every gap for $n < 60$ is at least $\tfrac12$. These were checked as float differences $H_{2n} - H_n$.
- `cauchy_n`: $\tfrac1{100}$ → 100, $\tfrac13$ → 3, $\tfrac27$ → 4, 1 → 1, $\tfrac3{1000}$ → 334, $\tfrac1{500}$ → 500.
- `first_n`: $\tfrac1{100}$ → 23, $\tfrac1{10}$ → 7, 1 → 2, 2 → 1, $\tfrac5{27}$ → 6 (the gap at 5 equals $\varepsilon$), $\tfrac1{1000}$ → 71.

## Numbers, each computed twice

The scripts are in the scratchpad folder `analysis-reports`: `numbers_l2.py` (170 checks), `points.py` and `code_check.py`. Each check uses two independent routes. One is an exact `Fraction` formula. The other is a brute-force scan (for every "smallest $N$", the last index that fails up to a horizon, plus one), float or 50-digit `Decimal` arithmetic, a closed form against a recursion, or a fit to the plotted data. **170 numbers and 703 plotted points checked, 0 discrepancies.**

- l6: $a_n = \tfrac34, 1, \tfrac76, \tfrac97, \tfrac{11}8$; $|a_n - 2| = \tfrac{5}{n+3}$; $|a_{47} - 2| = 0.1$, $|a_{48} - 2| = 0.0980$, and 0.1163 at $n = 40$. The first good $N$ is 48 at 0.1, 498 at 0.01, 8 at 0.5, 98 at 0.05 and 18 at 0.25; the thresholds are 47 and 497. Wrong forms: 500 ($n \ge \tfrac5\varepsilon$), 501 ($n > \tfrac5\varepsilon$), 504. $\tfrac5{501} = 0.00998$. The gaps to 2.5 are 1.75, 1.5, 1.33, 1.21, equal to $0.5 + \tfrac{5}{n+3}$. At $\varepsilon = 2$ the threshold is $-0.5$, and the max switches at $\varepsilon = 1.25$. Transfer: $\tfrac3n < 0.01$ from $n = 301$ (wrong forms 30 and 30000). Quiz: $\tfrac{3n}{n+1}$ has $N = 60$ at 0.05 ($\tfrac3{61} = 0.0492$); $|\tfrac12 - 1| = \tfrac12$.
- l7: $a_n + b_n - 5 = \tfrac3n$, first inside $5 \pm 0.1$ at $n = 31$ ($\tfrac3{31} = 0.0968$), with 0.125 at $n = 24$. $N_1 = 11$ and $N_2 = 21$ at $\varepsilon = 0.2$; $\tfrac1{15} < 0.1 < \tfrac2{15}$. At $\varepsilon = 0.1$ the table holds 21, 41, 41. Trap at $n = 25$: $\tfrac2{25} = 0.08$, $\tfrac3{25} = 0.12$. $N_2 / N_1$ lies between 1.8 and 2.0 for every slider value (see the fixes). Product: $|a_nb_n - 6| = \tfrac1n + \tfrac1{n^2}$ (checked for $n < 50$), $|a_n| \le 4$, $\tfrac\varepsilon8 = 0.00125$, $\tfrac\varepsilon4 = 0.0025$; the indices are 801 and 401, the proof's $N$ is 801, and the direct first index is 101 (0.0101 at $n = 100$, 0.009999 at $n = 101$). $\tfrac{801}{101} = 7.93$. Transfer: $5010 \times 0.02 + 40 \times 10 = 500.20$, equal to the brief's $5000 \times 0.02 + 40 \times 10 + 10 \times 0.02$; the wrong forms are 500, 400, 100.20 and 0.20. Quiz: 11 and 31, so 31 (direct 21); $M = \max(6, 5, 1, 3) = 6$; $\tfrac\varepsilon5$.
- l8: terms 1, 1.7321, 1.9319, 1.9829, 1.9957, 1.9989, also checked against $2\cos\tfrac{\pi}{3 \cdot 2^{n-1}}$. $L^2 - L - 2 = 0$ has roots 2 and $-1$, and $\sqrt{2 + (-1)} = 1$. Babylonian: $2, \tfrac32, \tfrac{17}{12}, \tfrac{577}{408}$ with $x_n^2 - 2 = 2, \tfrac14, \tfrac1{144}, \tfrac1{166464}$. $\sqrt3 = 1.73$, $\sqrt2 + 1 = 2.41$. $(1 + \tfrac1n)^n = 2, 2.25, 2.3704, 2.5937, 2.7048$ at $n = 1, 2, 3, 10, 100$, and $e = 2.7183$. Doubling: 1, 2, 4, 8, 16, 32. The gaps $2 - a_n$ are 1, 0.268, 0.068, 0.017, 0.0043, shrinking by a factor near 4, so one decimal place costs $\tfrac{\ln 10}{\ln 4} = 1.66$ steps. EMA: 90, 92, 93.6, 94.88; the gap $10 \times 0.8^{n-1}$ was confirmed exactly against the recursion for $n \le 21$. $0.8^{13} = 0.0550$ and $0.8^{14} = 0.0440$, so the day-14 gap is £0.55 and the day-15 gap £0.44: day 15. The wrong form (within £1) is day 12. Quiz: 0, 3, 4.5, 5.25 with limit 6 and gaps 6, 3, 1.5, 0.75.
- l9: $a_n = -2, 1.5, -1.3333, 1.25, -1.2, 1.1667$, and every $|a_n| > 1$. Lengths are 4, 2, 1, 0.5, 0.25, and $\tfrac4{1024} = 0.00390625$ after 10 halvings (wrong forms $\tfrac4{512}$ and $\tfrac1{1024}$). Even terms: none in $[0, 1]$, one in $[1.5, 2]$, two in $[1.25, 1.5]$. $n(1 + (-1)^n) = 0, 4, 0, 8, 0, 12$. Transfer data: all 24 estimates lie in $[0.1, 0.5]$; the low weeks are $0.18 + \tfrac{0.04}{k}$ and the high weeks $0.41 - \tfrac{0.04}{k}$ to 4 decimal places, so the two subsequential limits are exactly 0.18 and 0.41. Quiz: the odd terms of $(-1)^n + \tfrac1n$ tend to $-1$.
- l10: $S_n$ = 1, 1.25, 1.361111, 1.423611, 1.463611, 1.491389 for $n = 1$ to 6, then 1.527422 ($n = 8$), 1.549768 (10), 1.58044 (15), 1.596163 (20), 1.61215 (30), 1.620244 (40). Every band holds its tail ($S_m - S_N < \tfrac1N$ for $N \le 40$, $m \le 400$). $S_{200} - S_{100} = 0.004963$ against the bound 0.005, and $S_{3000} - S_{100} = 0.009617$ against 0.009667. The telescoping sum was checked exactly. $N = 100$ at 0.01 (wrong form 10). $\tfrac1{25} > \tfrac1{32}$. $H_{2n} - H_n = \tfrac12, \tfrac7{12}, \tfrac{37}{60}$ (0.583333 and 0.616667), and 0.6688 at $n = 10$. Quiz: $N = 500$ at 0.002 (wrong form 23). Transfer: $\ln 10^8 + 0.5772 = 19.0$, and $H_{2n} - H_n \to \ln 2 = 0.69$. $\sqrt{4n} - \sqrt n = \sqrt n$. The truncations 1, 1.4, 1.41, 1.414, 1.4142 differ by less than $10^{1-N}$ past the $N$th.
- Review: $|\tfrac{4n-1}{2n+1} - 2| = \tfrac3{2n+1}$, $N = 150$, $\tfrac3{301} = 0.00997$, $\tfrac3{299} = 0.01003$. $\sqrt{6 + a_n}$: 2, 2.8284, 2.9713, 2.9952, 2.9992, and the roots are 3 and $-2$. $\cos\tfrac{n\pi}{2}$: 0, −1, 0, 1, with $a_{4k} = 1$ and $a_{4k-2} = -1$. Geometric tail below $\tfrac1{2^n}$; $\ln 2n - \ln n = 0.6931$. Threshold at 0.1: $N = 10$, $\tfrac1{11} = 0.091$. Sum law: 11 and 41, so 41 (direct 16). $\tfrac{a_n + 8}3$: $1, 3, \tfrac{11}3, \tfrac{35}9$, limit 4, gaps $3, 1, \tfrac13, \tfrac19$, wrong form $\tfrac83 = 2.6667$.
- Homework: $|a_n - 3| = \tfrac5{n^2 + 2}$; at 0.01, $n^2 > 498$ gives $N = 23$ ($22^2 = 484$, $23^2 = 529$, $\sqrt{498} = 22.3$, $\tfrac5{531} = 0.0094$, $\tfrac5{486} = 0.0103$). Product: $|a_n| \le 3$, and both requirements need $n > 1200$, so $N = 1201$. The wrong form $\tfrac\varepsilon{2|b|}$ gives 1001, and the direct index is 98 ($|a_nb_n - 10| = \tfrac1n - \tfrac2{n^2}$). Squaring: 2, 4, 16, 256, 65536, which is $2^{2^{n-1}}$. `first_n` as above, with $70^2 = 4900 < 4998$. Longform: $\sqrt{500} = 22.36$, so $N = 23$. The rubric totals 10.
- Canvas points (`points.py`): 703 points (l6 205, l7 366, l9 52, l10 80), each checked against its formula in floats and in fractions to $5 \times 10^{-7}$. None was off.

## Edits made in this pass

Two fixes to stated numbers, both in `l7-limit-laws-proved.json`:

- Screen 1 (explore) explanation said "Here $N_2 = 2N_1 - 1$". With $N_1 = \lfloor \tfrac2\varepsilon \rfloor + 1$ and $N_2 = \lfloor \tfrac4\varepsilon \rfloor + 1$, that fails on the slider at $\varepsilon = 0.3$ (7 and 14) and $\varepsilon = 0.35$ (6 and 12). It now reads "Here $N_2$ is about twice $N_1$". The ratio lies between 1.8 and 2.0 for every slider value.
- Screen 8 (product numbers) explanation called 801 "eight times the true first index 101"; the ratio is 7.93. It now reads "nearly eight times".

The validator and the lesson replay were green after both edits.

## Departures from the brief

- l6: the hook drags a point for $N$ (`drag-point`, graded at 48 with wrong regions at 47 and beyond 48) on a zoomed plane; a second plane with an $\varepsilon$ control then shows the dashed first-good line. The "$N$ depends on $n$" proof is a `choice` on a numbered table, not `tap-regions`. The constant sequence is a quiz item. The code tests add $\tfrac5{51}$, $\tfrac1{1000}$ and $\tfrac73$ to the brief's six values.
- l7: the three first indices at $\varepsilon = 0.1$ are one `table`, and "take the larger" is the explore screen's `choice`. The false inequality $|a_nb_n - ab| \le |a_n - a||b_n - b|$ is a `distractors` line in the product `order`, and the flawed-line spot of it is `review-2` item 2, not a lesson trap screen. The lesson trap is the $\min(N_1, N_2)$ line. Bounded-not-convergent and the quotient law share one `choice` screen. The transfer's bound is written $5010 \times 0.02 + 40 \times 10$, the same £500.20.
- l8: the two inductions ($a_n < 2$ and $a_n < a_{n+1}$) are one induction on $P(n)$: $a_n < a_{n+1} < 2$, with one `order`. The limit 2 is a `numeric` on the hook, and the later screen is a `choice` that rejects $-1$. The edge cases $a_n = n$ and $(-1)^n$ are quiz items. The code tests add $\varepsilon = 1$ and 2, and starts from 0 and 3.
- l9: as briefed. The repeated-index trap is a `multi` screen and a quiz item.
- l10: the $\sqrt2$ truncations and $\sqrt n$ are quiz items. The code tests add more `cauchy_n` values.
- Review: 9 items as listed. Homework: 8 items; besides the brief's items it adds a difficulty-5 `order` (bounded, and every convergent subsequence tends to $L$, gives $a_n \to L$) and the $a_{n+1} = a_n^2$ fixed-point trap. The longform model bounds $\tfrac5{n^2 + 2} < \tfrac5{n^2}$ and so takes $N > \sqrt{5/\varepsilon}$.

## Proposed course.json change

None.

## Backlog

No new bullets. The level 2 limits are already under "Raised later (analysis level 2):" in `docs/BACKLOG-INBOX.md`, and this pass found no other engine limit.

## Conventions

No datasets or seeds; the l9 transfer data follow $0.18 + \tfrac{0.04}k$ and $0.41 - \tfrac{0.04}k$. Money in £ (pence in the l6 transfer). $\varepsilon$ written `\varepsilon`; Abbott's form with $n \ge N$; partial sums $S_n$ and $H_n$; exact `Fraction` arithmetic where an answer is exact, `math.isclose` for `iterate_sqrt`.

The main session saved this report from the agent's returned text, because the harness refuses report-file writes from subagents.
