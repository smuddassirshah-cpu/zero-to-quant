# mock-oa-strats: report

Brief: `docs/briefs/mocks.md`, section `## mock-oa-strats` (written for this mock, from `prep.json` `firm-goldman-sachs` and `oa-strats`, `asOf` 2026-10, and `docs/briefs/interview-gaps.md`; no web search). Build: `docs/briefs/mocks-scripts/mock-oa-strats_build.py`. Second route: `docs/briefs/mocks-scripts/mock-oa-strats_check.py`. Both run with `python3 -I`, standard library plus SymPy 1.14 and NumPy 2.5.3 for the check.

## Files
- `app/content/exams/mock-oa-strats.json` (one file, fixed items, no versions: the bank has no calculus or linear algebra families to draw from).
- `docs/briefs/mocks.md` (section appended), the two scripts, this report, `docs/BACKLOG-INBOX.md`.
- `docs/readiness.md`: the two `mock-oa-strats` rows changed from "gap: not yet written" to "exists", and the strats evidence line lost "(gap)". `readiness-sums.mjs` failed on those hand rows; `--write` then regenerated only the mock lists in `app/content/readiness.json` (4 lines). No other block changed.

## Items
10 items, 52 minutes, two papers and two checks (`no-calculator`, `no-lookup`). Scoring 1, 0, 0, free navigation.

| Paper | Minutes | Items | Pass | Pace sum |
| --- | --- | --- | --- | --- |
| `code` Software fundamentals | 30 | C1 `net-positions` (d2, `ds-hashing`), C2 `fewest-days` (d3, `ds-pointers`) | 0.5 | 1,680 s |
| `maths` Maths | 22 | 8 `choice`, d2 x2, d3 x4, d4 x2 | 0.625 | 1,290 s |

Maths families: `chain-rule`, `eigenvalues-2x2`, `limit-series`, `probability-tree`, `by-parts`, `linear-ode`, `shared-book`, `correlation-bound`. Every choice shuffles, has four options of similar length and a `why` on each distractor starting "You".

## Numbers (route A in build, route B in check; every pair agreed)
- M1 $f'(1) = 3/2$ for $\ln(1+3x^2)$: exact quotient and a central difference; SymPy `diff`. Slips 1/4, 6, $\ln 4$.
- M2 eigenvalues 1 and 6 of [[5, 4], [1, 2]]: integer roots and $Av = \lambda v$ for (4, 1), (1, −1); SymPy `eigenvals`. Slips 2 and 5, −1 and −6, 6 and 7.
- M3 limit 2: series coefficient and a 12-term exact series at $10^{-4}$ (2.000133, stated 2.0001); SymPy `limit`. Slips 4, 1/2, 0.
- M4 0.625: Bayes in `Fraction`s and counts of 1,000 trades (12 and 20 fail); route B counts a listed population. Slips 0.375, 0.05, 0.714 (5/7).
- M5 $1 - 2/e \approx 0.264$: antiderivative and Simpson with 2,000 strips; SymPy `integrate`. Slips $1 - 1/e$, $2/e - 1$, $-2/e$.
- M6 $3e^2 - 2 \approx 20.17$: steady state and RK4 with 10,000 steps; SymPy `dsolve`. Slips $e^2$, $3e^2$, $5e^2 - 4$.
- M7 1/28: $\tfrac28 \times \tfrac17$ and 10 of 280 unordered splits; route B counts all 9! seatings. Slips 1/9, 1/84, 1/4.
- M8 0.28: $\rho^2 - (1-\rho^2)$, determinant roots 0.28 and 1, $\cos(2\arccos 0.8)$; route B scans the smallest eigenvalue on a 0.01 grid. Slips 0.64, 0.6, 0.
- C1: 11 tests; large case 50,000 accounts. C2: 12 tests; large cases 150,000, 98 and 1. Every small expectation equals a brute force; the solution passes every test and example in CPython (slowest 73 ms); starters fail 9 of 11 and 9 of 12; five planted wrong versions each fail at least one test.
- The check's last pass reads every number in every learner-visible string; all match route B. `check_wrongs()` then `report()`: 189 of 189 checks passed, exit 0.

## Gates
- Validator: 0 errors, no warning on this file.
- Voice scan (`VOICE_BASE` on a copy of the file): 0 explanations over three sentences, 0 sentences over 20 words (202 scanned).
- `fresh-check --exam mock-oa-strats --min-run 10`: 0 hits after rewrites. First drafts hit `limits` l16 (limit skeleton), `mock-oa-trader-2` (four dice, and its "highest face is 3" setup) and, by a literal search, `eigen` l1 to l3 (the matrix [[4, 1], [2, 3]]), `integrals` l10 ($x e^{2x}$, $x \ln x$, $x^2 e^x$) and `integrals` l15 ($\ln(1+x^2)$). Each was replaced, and the brief table carries the final items.
- Playthrough with `--local-cdn`: green (10 of 10, passed; mock checks ok), and green with `--mobile`.
- Screenshots (1280 and 440): start card, code item, choice item, results. Nothing overlaps; options fit.
- `readiness-sums.mjs`: OK after the `readiness.md` rows above.

## Proposals
- `prep.json`: none.

## Backlog
2 bullets under `Raised later (mock mock-oa-strats):` in `docs/BACKLOG-INBOX.md`.
