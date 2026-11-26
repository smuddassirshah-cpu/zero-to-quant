# Concept audit: series, levels 1 to 3 (round 1)

Auditor: blind Fable read at commit e1c0aa6f. Stage 0 course (topic 0.3), so the ledger uses the reduced depth: definitions, rules, always / never / every / only claims, conventions, and every graded key, wrong option and slip.

Scope read in full: lessons l1 to l13, review-1 to 3, homework-1 to 3, problems-1 to 3, and the six fluency sets. The course has no code widgets.

Sources: Pearson Edexcel A level Pure Mathematics Year 2 ch. 3 (sequences and series) and Year 1 ch. 8 (binomial expansion); Spivak, *Calculus*, ch. 22 (infinite sequences) and ch. 23 (infinite series); Hull, *Options, Futures and Other Derivatives*, ch. 4, for present values.

## Result

- Ledger: `docs/reports/audit-series-1-3-ledger.md`, 1,182 rows: correct 1,174, imprecise 6, misleading 2, wrong 0, unverified 0.
- Findings: 8. Wrong 0. Misleading 2 (1 serious, 1 minor). Imprecise 6 (all minor).
- Every one of the 173 numeric and slider keys, and every slip value, recomputes from the mistake its feedback names (script part A).
- All 20 fluency families hold over their whole range, 121,058 cases: keys by brute force, each wrong value equal to its named mistake and never equal to the key (part B). One family has two slips that share a value in 53 cases (finding 7).

## What was checked against the watch list

- First term index. The course defines $u_1 = a$, so $u_n = a + (n-1)d$ and $u_n = ar^{n-1}$, and says so where each first appears (l2 screen 7, l3 screen 7). Every key and every "n steps" or "n factors" slip matches that convention.
- Sum formulas and conditions. $S_n$ for a geometric series carries $r \ne 1$ with the $r = 1$ case handled (l7 screen 7). $S_\infty = \tfrac{a}{1-r}$ carries $-1 < r < 1$ every time it is stated, with $r = 1$, $r = -1$ and $r = 2$ shown to fail (l8 screens 1, 5, 6).
- Off-by-one counts. Steps against terms, powers 0 to $n-1$, and $n - m + 1$ terms are right everywhere, in keys and in slips.
- Payment timing. Every annuity, loan, perpetuity and savings item states when the payment falls. The start-of-year case is taught as a trap (l13 screen 6) and its value, £454.60, is right.
- Compound interest as a geometric sequence: right throughout.
- "The terms go to 0, so the sum converges". The course never states the harmonic series, and two lines give shrinking terms as the reason a sum exists (findings 1 and 2).
- Recurrences: fixed points, the gap argument and the loan recurrences are right; two lines state the convergence condition too broadly (findings 3 and 4).
- £ for money and plain words: no issue found.

## Findings

1. `l13-stream-of-payments.json` | `summary.ideas[2]` | misleading, serious | The summary says a never-ending stream has a finite value "because the terms shrink to 0". The value is right, the reason is not: terms that shrink to 0 do not give a sum. | $1 + \tfrac12 + \tfrac13 + \dots$ has terms that shrink to 0, yet its partial sums pass 5 at $n = 83$, 10 at $n = 12{,}367$ and 14 at $n = 675{,}214$ (script part D; Spivak ch. 23, the harmonic series). The stream has a sum because each term is a fixed fraction $\tfrac{1}{1+r} < 1$ of the one before. This is the last summary of the course, so it is the rule a learner keeps. | Replace the idea with: `A stream that never ends has a finite value, $\\tfrac{C}{r}$, because each payment is worth the same fraction, $\\tfrac{1}{1 + r}$, of the one before.`

2. `l8-adding-forever.json` | `screens[1].feedback.correct` | misleading, minor | The question asks when the partial sums settle, and the feedback answers "Only $-1 < r < 1$ makes the terms shrink to nothing." That makes shrinking terms the test for a sum. It is the right test for a geometric series only. | Same basis as finding 1. The explain on this screen ("Settling needs the terms to shrink") is a necessary condition and is correct; the feedback line reads as a sufficient one. The lesson's own derivation (screen 7) rests on $r^n \to 0$ in the formula for $S_n$, which is the sound reason. | Replace with: `Only $-1 < r < 1$ makes $r^n$ shrink to nothing, and then the sums level off.` A fuller fix is one added line where the course can afford it, for example as the third sentence of the l8 summary trap: `Shrinking terms are not enough in general: $1 + \\tfrac12 + \\tfrac13 + \\dots$ grows past every number.` That needs no new screen.

3. `l4-last-step.json` | `summary.ideas[2]` | imprecise, minor | "Terms settle only when each step shrinks the gap to $L$; otherwise they run away." Two cases break it. With multiplier $-1$ the terms neither settle nor run away. A start at $L$ settles for any multiplier. | $u_{n+1} = -u_n + 6$ from $u_1 = 5$ gives 5, 1, 5, 1, ... for ever (script part E3). The lesson's own quiz explain (quiz[3]) has the careful wording "Unless they start at the fixed point". | Replace with: `Unless they start at $L$, terms settle only when each step shrinks the gap to $L$. If each step grows the gap, they run away.`

4. `homework-1.json` | `items[6].explain.text` (h-gap-proof) | imprecise, minor | "It shrinks to 0 exactly when $-1 < a < 1$." The gap is $(u_1 - L)a^{n-1}$, so it is also 0 for every $a$ when $u_1 = L$. | Derivation from the item's own line s5. | Replace the last sentence with: `Unless $u_1 = L$, it shrinks to 0 exactly when $-1 < a < 1$.`

5. `review-3.json` | `items[8].explain.text` (r3-rate-cut) | imprecise, minor | "Far-off payments gain the most from the cut." True in proportion only. In pounds, the gain of the payment $t$ years away is $100(1.04^{-t} - 1.05^{-t})$, which peaks near year 23 at £8.02 and then falls towards 0 (£0.03 at year 200). | Script part D. The proportional gain $(1.05/1.04)^t$ does rise without limit. | Replace the sentence with: `In proportion, far-off payments gain the most from the cut.`

6. `l12-small-x.json` | `screens[3].explain.text` | imprecise, minor | "Each term we keep shrinks the error." True for the small $x$ of this screen. As a rule it fails: for $(1 - 0.5)^{10}$ the errors with one, two and three terms are 1.0, 4.0 and 7.2. | Script part D. The next screen shows the estimate failing at $x = 1$, but there more terms still help, so the learner is never shown this sentence failing. | Replace with: `Here each term we keep shrinks the error.`

7. `fluency-l6-gauss.json` | `families[first-n-terms].wrong` | imprecise, minor | The slips `not-halved`, $k(2a + (k-1)d)$, and `k-steps`, $\tfrac{k}{2}(2a + kd)$, have the same value when $2a + (k-2)d = 0$. That is 53 of the 9,708 admissible cases, for example $a = 3$, $d = -1$, $k = 8$: both give $-8$. A learner who used $k$ steps is then told they forgot to halve. | Script part B (collision count). | Add to `where`: `"2*a + (k - 2)*d != 0"`.

8. `l2-any-term.json` | `summary.ideas[2]` | imprecise, minor | "A number is a term only when solving for $n$ gives a whole number." The condition needed is a positive whole number. For $5, 8, 11, \dots$ with $u_n = 3n + 2$, the number 2 gives $n = 0$ and $-1$ gives $n = -1$; neither is a term. | Derivation. Positions start at 1 in this course (l2 screen 2). | Replace with: `A number is a term only when solving for $n$ gives a positive whole number.`

No finding needs a screen rewritten.

## Checks run

- `python docs/reports/series-L1-3-concepts.py` (scratchpad venv, standard library only): 1,499 checks pass, 0 unexpected failures, 8 finding checks fail as intended, exit 1. The eight are the findings above; each passes once its fix is applied (finding 7 once the collision count is 0).
- Monte Carlo, 400,000 replications each: exactly 3 of 5 at 0.5 (0.3125), 2 of 4 (0.375), 3 of 6 (0.3125), 3 of 5 at 0.6 (0.3456). Each is within four standard errors of the key and more than ten from the nearest slip.
- `node tools/validate.mjs`: 0 errors.
- `node tools/run-number-scripts.mjs --only series`: 5 of 5 pass.
- `node tools/grade-all.mjs --file <each of the 28 files>`: 0 failures in every file.
- No playthrough, as the common rules set.

## Overlap with the earlier reads

Read after the ledger and findings were written: `docs/reviews/review-series-1-3.md` (lessons, reviews, homework; 38 findings, of which 19 are conceptual: 8 `wrong` and 11 `misleading`, all fixed before this commit) and section A of `docs/reviews/review-problems-0.3-c.md` (the three problem sets; 7 minor findings on series, none conceptual). No earlier audit of series exists.

| | count |
|---|---|
| Conceptual findings by this audit only | 8 |
| By the earlier reads only | 19 (plus 7 minor, non-conceptual, on the problem sets) |
| By both (same defect) | 0 |
| New `wrong` in this audit | 0 |

Notes on near overlaps, not counted as "both":

- Earlier finding 9 fixed l4 `quiz[3].explain.text` for a start at the fixed point. Findings 3 and 4 here are the same omission left in two other sentences (l4 summary, homework-1 h-gap-proof), plus the $a = -1$ case, which the earlier read did not raise.
- Earlier finding 13 separated "terms" from "totals" in l7. Findings 1 and 2 here are a different defect: shrinking terms given as the reason a sum exists.
- Earlier findings 2 to 6 were slip values that did not match their lines. Part A of the script finds none left in 173 widgets.

## Inbox

One bullet added to `docs/BACKLOG-INBOX.md` under "Raised later (audit series):" (a sweep rule for fluency slips that share a value).
