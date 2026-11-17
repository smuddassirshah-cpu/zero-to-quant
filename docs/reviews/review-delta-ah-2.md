# Delta read AH 2: `p-spread-blocks` re-authored, `p-daylight-model` renumbered

Counts: `wrong` 0, `misleading` 0, `weak` 6 (findings 1 to 6), `voice` 0. No key, band, slip value or printed number is mistaken. No fix changes a key or a graded answer.

Scope, read at `4a1a2786` (session head `claude/session-ah-engine-pass-1nzn58`):

- `validation/problems-2` `p-spread-blocks`, all four parts (re-authored in `4a1a2786`);
- `trig/problems-3` `p-daylight-model`, all five parts (renumbered in `07215554`).

No browser, no content or engine edit.

## Method

- Each part was solved from its question before its key, feedback or explanation was read, then again in `docs/reviews/review-delta-ah-2-scripts/check.py` (standard library only, imports no other script): 370 checks, 0 failed, exit 0.
- Bands were rebuilt from each widget's `answer` and `tol`. Every slip band was tested against every key band and every other slip band.

## Tool results

| check | result |
|---|---|
| `run-number-scripts --only validation` | 4 scripts, 4 passed, 0 new failures |
| `run-number-scripts --only trig` | 5 scripts, 5 passed, 0 new failures |
| `grade-all --file` validation `problems-2` | 18 widgets, 0 failures |
| `grade-all --file` trig `problems-3` | 18 widgets, 0 failures |
| `fresh-check --file`, both files | 0 hits each (1 and 7 advisories, none on these two problems) |
| voice scan 35 | 0 and 0 |
| `review-delta-ah-2-scripts/check.py` | 370 checks, 0 failed |

## Keys confirmed

`p-spread-blocks` (label of row $t$ = changes of days $t+1$ to $t+8$):

| part | key | exact route | second route |
|---|---|---|---|
| 1 | 0.625 | sets of days: rows $t$, $t+3$ share days $t+4$ to $t+8$, covariance $5\sigma^2$ over variance $8\sigma^2$ | 400,000 simulated independent changes: sample correlation 0.6241 at lag 3 (0.4986, 0.3731, 0.1240, −0.0003 at lags 4, 5, 7, 8) |
| 2 | 11.2 | 14 rows within 7 either side, times $\tfrac45$ | a true shuffled 5-fold of 1,800 rows: exact $14 \times \tfrac{1440}{1799} = 11.206$; 300 simulated shuffles give 11.209 for interior rows |
| 3 | 4 | $\tfrac{7 - g}{8} < 0.4$ first holds at $g = 4$ (0.5 at $g = 3$, 0.375 at $g = 4$) | scan of $g$ from 0; distance $g + 1$ rebuilt from the slicing rule `train = rows[: test_start - gap]` |
| 4 | 25 | rows $s$, $s+8$, …, $s+192$; $\lceil 200/8 \rceil$ | dynamic programme for the largest 8-separated set, checked against brute force on blocks of 1 to 16 rows |

Slips, all outside every band: part 1 0.375, 0.75; part 2 12.8, 5.6, 14 (the unlisted miscounts 15 and 13 rows give 12.0 and 10.4, also outside); part 3 5, 7; part 4 26, 29.

`p-daylight-model`: $a = 5.6$, $d = 12$, range 11.2; $b = \tfrac{\pi}{6}$; $c = 3$ (model checked at $t = 0, 3, 6, 9, 12$); sine $-\tfrac{5}{14}$, angles $-0.3652$ and $3.5068$, $t - 3 = -0.70$ and $6.70$, roots 2.30251 and 9.69749 (by `asin` and by a sign scan: exactly two in $0 \le t \le 12$); part 5 7.39499, 7.4 from the printed roots, complement 4.6. Slips 11.2, 17.6, 12; 6, 9, 12; "6.7, 11.3"; "3.7, 8.3" (both are 14 hours); 4.6, 8: each recomputed, each clear of the bands.

## Modelling assumptions tested (`p-spread-blocks`)

- **Independent, equal-variance daily changes.** Given these, the correlation is exactly shared days over 8. The prose says "close to independent", then states the rule, so the rule is the given. One answer.
- **"Share a label day" at the ends.** End rows have fewer neighbours (simulated mean 8.0 for the 14 end rows). The question says "far from the ends", so this does not arise. The last 8 rows have no full label; no part depends on it.
- **Exact or approximate in part 2.** The question fixes the chance at $\tfrac45$, so 11.2 is exact on the stated model. The true figure for 1,800 rows, 11.206, also rounds to 11.2 and sits inside the band. One answer.
- **Off-by-one in part 3.** The question states the distance $g + 1$; "below 0.4" and "at most 0.4" give the same $g$, since no step lands on 0.4.
- **Off-by-one in part 4.** "8 or more apart share no day" is stated in the question; 25 is the maximum, not only a count of one layout (checked by the dynamic programme).
- **Part 4's explanation.** "About as much evidence as 25 independent ones" holds: the variance of the mean of 200 overlapping labels equals that of 25.3 independent ones.

## Reuse

- `p-spread-blocks` does not walk the sources of `review-pkg3-reuse-hits.md` fault 2. No part counts sandwiched test days (l5 screens[1]), later training days of a block (l5 screens[7]), rows left after a purge and embargo (`h-count`), or a percentage rise in error (l7 screens[5]). It uses the taught ideas (overlap of $h - 1$ rows, the meaning of `gap`) on new questions: a label correlation, an expected count under a shuffle, a threshold gap, a packing count. Each part needs the prose rule, and parts 2 to 4 lean on part 1. Answerable from levels l5 to l7 plus the stated rule.
- `p-daylight-model` no longer mirrors `h3-demand-model`. The old pair (16.4, 7.6) was the homework's (820, 380) divided by 50, which made the same sine of $\pm\tfrac12$ structure one scale away. The new pair is on no common scale, and the sine is $-\tfrac{5}{14}$, which needs a calculator and the negative branch, against the homework's exact $+\tfrac12$. The peak month, the shift and the side of the midline also differ.

## Findings

Format: `N. severity | file | problem, part, field | text at fault | exact replacement`. Texts are the decoded strings; in the JSON each backslash is doubled.

1. weak | `app/content/courses/validation/problems-2.json` | `p-spread-blocks`, `prose` | "So two labels correlate by the share of their 8 days they have in common."
   Every part rests on this rule, and "correlate by the share" does not say that the correlation equals the share.
   Replace with: "So the correlation between two labels is the share of their 8 days that they have in common."

2. weak | same file | `p-spread-blocks`, `prose` | "A credit desk forecasts a CDS index spread from 1,800 trading days of data."
   "CDS" is used nowhere else in the validation course and is not explained.
   Replace with: "A credit desk forecasts the spread of a credit index from 1,800 trading days of data."

3. weak | same file | `p-spread-blocks`, part 2, `question` | "Using part 1, how many training rows, on average, share a label day with it?"
   Part 1's answer (0.625) is not used, and "share a label day" is a new phrase the learner must decode.
   Replace with: "How many training rows, on average, have a label that shares at least one day with its label?"

4. weak | same file | `p-spread-blocks`, part 3, `explain.text` | "The smallest gap is $g = 4$."
   The part rewards a gap that still leaves a correlation of 0.375, and only the `full-purge` slip line says that it still leaks.
   Replace with: "The smallest gap is $g = 4$, and only $g = 7$ leaves no shared day."

5. weak | same file | `p-spread-blocks`, part 3, `feedback.byKey.full-purge` | "The desk asked only for a correlation below 0.4."
   The question never says the desk asked for this.
   Replace with: "The question asks only for a correlation below 0.4."

6. weak | `app/content/courses/trig/problems-3.json` | `p-daylight-model`, part 4, `question` | "Give both, in months, separated by a comma."
   Not caused by the renumber: no precision is asked, while the band is 0.01 and the roots are 2.3025 and 9.6975.
   Replace with: "Give both, in months to 1 decimal place, separated by a comma."

## For the fixer

- All six are text edits in `prose`, `question`, `explain` or `feedback`. No `answer`, `tol`, `wrong` value or number script changes.
- After editing run, from `app/`: `node tools/validate.mjs 2>&1 | tail -5`, `node tools/grade-all.mjs --file` on each file, `node tools/fresh-check.mjs --file` on each file, the voice scan, and `python3 docs/reviews/review-delta-ah-2-scripts/check.py` from the repo root (it also checks sentence length and the three-sentence limit on these two problems).
- If the validator objects to finding 6 (a stated number of places against the keys 2.3 and 9.7), drop finding 6; it is optional.

## Nothing a fixer cannot settle

No open question. Every fix is a fixed string.
