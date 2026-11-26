# Blind concept audit: ito problem sets 1 to 4

Scope: `app/content/courses/ito/problems-1.json` to `problems-4.json` (12 chained problems, 49 parts), at commit 151f63f2 (tip of `claude/sleepy-heisenberg-bhwkqw`). Lessons were read only where a problem leans on them (l3, l4, l5, l10, l12, l13). Read blind: no earlier review, audit or author report on ito was opened before the ledger and the findings below were written.

Ledger: `docs/reports/audit-ito-problems-1-4-ledger.md`, 545 rows: correct 541, imprecise 4, wrong 0, misleading 0, unverified 0.

Script: `docs/reports/ito-problems-concepts.py`, 386 checks, exit 0. It recomputes every key and every slip value from the mistake its feedback names, checks each slip sits outside the key's band, checks that rounded carried values still grade, and simulates every SDE or path claim.

## What was checked and how

- Every key, every `wrong[]` value and every number quoted in feedback or explanations: recomputed from the item's data, twice where a second route exists (drift of the ratio by logs and by the quotient rule; the touch note by the equation and by the hitting-time transform; the conditional exit times by the cubic martingale and by the boundary-value formula).
- Chaining: each part was regraded with the rounded figure the question hands forward (0.7867, 0.3031, 0.6920, 0.3837, 0.2385, 118.2134, 0.006805). All land inside the key's band.
- Conventions. Drift of the log price is `mu - sigma^2/2` throughout, and every "median against mean" slip is the right size. Real-world against risk-neutral drift is kept apart in `p-twin-shares` (0.84% under P, -2.16% under Q) and `p-bridge-closes` (Q drift of ln S is 0.0058, not 0). Itô sums are left-point; the right-point and ordinary-calculus values are slips. `(dX)^2 = 4 dt` for a volatility of 2. Annualisation uses 252 days, said in the item.
- Simulations (Euler-Maruyama unless stated): mean, median and tail of the conditional GBM in `p-quarter-rally`; sampling sd of realised variance over 84 days; `E[1/X_3]`, `E[X]E[Y]` and the martingale drift in `p-cable-inverse`; L2 convergence of `sum W_k (dW_k)^2` to `int W dt`, and of the cubed moves to 0; variance, median and tail under two-stage volatility; the perpetual touch note under Q (exact log steps with a bridge test, 150 years, 40,000 paths: 0.693, se 0.002, against 0.692); the ratio's mean under P and under Q and the note price; the pinned touch chance between two closes at two very different drifts (0.493 and 0.496 against 0.494, so the drift has no effect); exit probabilities and both conditional waits on a lattice walk that hits the edges exactly (133.9 and 174.4 against 133.3 and 175); `E[S_1 S_2]` under Q; and a delta hedge of the prepaid claim with a dividend yield under a real-world drift (the book ends at 0.000 with the dividend term, at -1.89 without it).
- Choice parts: every wrong option is wrong under every convention, and each `why` names the mistake that picks it.

## Findings

No finding is `wrong` or `misleading`. Three are `imprecise`, all minor: no key, slip or method changes.

1. problems-1.json | items[0] (`p-maker-tally`) parts[2].question, with parts[1].feedback.byKey.variance | imprecise, minor | Part 2's slip line tells the learner that the day's variance is 999,804 and that 1,000,000 is something else. Part 3 then sets the model's `sigma^2` to 1,000,000 "from part 2" and its explanation uses it as the variance per day. Nothing says which of the two the model matches, or that they differ by 0.02%. | The walk's quadratic variation is 1,000,000 on every path and its variance is `625(1600 - 0.56^2) = 999,804`. A Brownian motion with drift has quadratic variation `sigma^2 t`, so matching quadratic variation is correct (Shreve II 3.4.2), and the week's sd is 2,236.07 against 2,235.85. Both round to the key; the script checks this. | Replace the first two sentences of parts[2].question with: "Model the P&L as $X_t = 350t + \sigma W_t$, with $t$ in trading days. Match its quadratic variation to the walk's, so $\sigma^2 = 1{,}000{,}000$ from part 2. The walk's daily variance, 999,804, is within 0.02% of that." The rest of the question stays.

2. problems-3.json | items[2] (`p-bridge-closes`) parts[3].question | imprecise, minor | "discounted at $r = 4.5\%$" does not say over what fraction of a year. The feedback uses `4/252`. Interest runs on calendar time, so a learner may as well use `4/365`, and part 2 set `1/252` for the variance only. | `e^{-0.045 x 4/252} = 0.999286` gives 3.6044; `4/365` gives 3.6052. Both are inside the key's band of 0.01 (script), so only the stated convention is at issue. A one-clock simulation is a fair simplification if it is said. | In parts[3].question replace "discounted at $r = 4.5\%$." with "discounted at $r = 4.5\%$ over $4/252$ of a year, the simulation's clock."

3. problems-2.json | items[2] (`p-results-vol`) parts[0].feedback.correct and parts[0].explain.text | imprecise, minor | "A fixed integrand gives a normal" and "For a fixed integrand". Lesson 5 calls this a deterministic integrand. "Fixed" reads as constant, and the integrand here is not constant: it steps from 0.40 to 0.15. | Shreve II Thm 4.4.9: the Itô integral of a deterministic (non-random) integrand is normal with variance `int sigma(t)^2 dt`. The result fails for a random integrand, so the hypothesis is the one word that matters. | feedback.correct: "A deterministic integrand gives a normal with variance $\int_0^1\sigma(t)^2\,dt = 0.16(0.25) + 0.0225(0.75) = 0.056875$." explain.text, first sentence: "For a deterministic integrand the integral is normal with variance $\int_0^1\sigma(t)^2\,dt$."

Noted, not raised as findings (all verified correct):

- `p-maker-tally` part 4 is a normal approximation to a binomial. The exact chance of a losing week is 0.2169 to four places, the same as the key.
- `p-dividend-hedge` part 3 asks for `V_t` without a unit; it is pounds a year. The key is unambiguous.
- `p-band-wait` part 2 justifies optional stopping by a bounded rate and finite `E[tau]`. That is sufficient: the stopped process is bounded by `125,000 + 600 tau`, which is integrable.
- `p-touch-note` assumes no dividends, as lesson 9's equation does.

## Tool runs

- Validator: 0 errors.
- `node tools/run-number-scripts.mjs --only ito`: 9 of 436 scripts, 9 passed, 0 new failures.
- `node tools/grade-all.mjs --file` on each of the four files: 12, 12, 12 and 13 widgets, 0 failures.
- `docs/reports/ito-problems-concepts.py`: 386 checks, exit 0 (about two minutes; NumPy and SciPy from the scratchpad venv, no figure depends on the version).
- No playthrough, as the auditor rules say. No code widgets in these files, so the `test-N` sweep does not apply.

## Overlap with earlier reads

Read after the ledger and findings were written: `docs/reviews/review-problems-ito-1-3.md`, `review-problems-ito-4.md`, `review-delta-ag-ito.md`, `review-delta-ag-ito-4.md` and `docs/reports/problems-ito.md`. The lesson audits (`audit-ito-1-3.md`, `audit-ito-4.md`) do not cover the problem sets.

Those reads were mostly about reuse, continuity and grading bands. Their conceptual findings on these four files, all fixed before this audit, were three: the dividend yield used without a definition (`review-problems-ito-4` finding 3), optional stopping used with no condition (same file, finding 5), and "the stopped process keeps its starting value" (`review-delta-ag-ito-4` finding 2). Six more were `misleading` on a tolerance or a part passable from its printed target, not on a concept. This audit confirms the fixed text of all of them as correct.

| Conceptual findings | Count |
|---|---|
| This audit only | 3 (all imprecise, minor) |
| Earlier reads only | 3 (all fixed before this audit) |
| Both | 0 |
| New `wrong` | 0 |

Finding 1 here is not counted as "both", but the first read saw the same fact: its notes say `p-maker-tally` part 3 takes $\sigma^2$ from the sum of squares while the day's variance differs, and it asked for no change. This audit asks for one sentence, because part 2's own slip line now tells the learner the two numbers are different things.

Convergence: 0 new `wrong` over four problem sets, so these files are within the rule.

Engine: no engine limit met; nothing added to `docs/BACKLOG-INBOX.md`.

## Fix pass

Opus fixer, content commit 1fade7ab. No key, slip, test or method changed.

1. Fixed (`p-maker-tally` part 3 question). Basis: a walk of 625 moves of ±40 has quadratic variation 625 × 1600 = 1,000,000 on every path, and $X_t = 350t + \sigma W_t$ has quadratic variation $\sigma^2 t$ because the drift has finite variation (Shreve II Thm 3.4.3). The variance is $625(1600 - 0.56^2) = 999{,}804$, a gap of 0.0196%. Week sd: 2,236.07 against 2,235.85, both within the key's 0.5. The question now says the model matches quadratic variation, and gives the variance with the 0.02% gap.
2. Fixed (`p-bridge-closes` part 4 question). Basis: the feedback discounts by $e^{-0.045 \times 4/252} = 0.999286$, giving £3.6042; a $4/365$ clock gives £3.6050. Both sit inside the key's 0.01, so only the convention needed stating. The question now says "over $4/252$ of a year, the simulation's clock".
3. Fixed (`p-results-vol` part 1 feedback.correct and explain.text). Basis: Shreve II Thm 4.4.9 needs a nonrandom integrand for the normal law with variance $\int \sigma(t)^2\,dt$; lesson 5 says "deterministic". The integrand here steps from 0.40 to 0.15, so "fixed" read as constant. Both sentences now say "deterministic"; $0.16(0.25) + 0.0225(0.75) = 0.056875$ is unchanged.

Gates: validator 0 errors; voice scan 35 on the three files 0 and 0; `ito-problems-concepts.py` 386 checks, exit 0 (no check encodes the old text, so nothing re-pointed); `run-number-scripts --only ito` 9 of 9 passed; `grade-all --file` 12, 12 and 12 widgets, 0 failures; playthrough `--problems ito/problems-1`, `-2`, `-3` desktop and `--mobile`, all passed. problems-4 untouched.
