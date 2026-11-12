# Bands pass AC (session AC task 5)

Branch `worktree-agent-ad77cfa686b537052`, four commits (parts A to D). Merge note: this worktree started from an unrelated initial commit, so `git merge claude/amazing-wright-d4mx7i` needed `--allow-unrelated-histories` (README.md, docs/curriculum.md, .gitignore: took the project branch's side). Scripts and the number check are in `docs/reports/bands-pass-ac-scripts/` (`check.py` passes: 0 failures; `partA.mjs`, `partB.mjs`, `partD.mjs`, `jsonscan.mjs` make the text-level edits so each file keeps its own formatting).

Counts, before to after: `[percent-form]` 74 to 3, `[tight-band]` 26 to 17, `[wrong-band]` 87 to 87 (not in the task; untouched), validator 0 errors, `grade-all` 0 failures on every edited file, `--exam stage-3` passes with and without `--mobile` (117 of 117).

## A. percent-form (71 of 74 done)

An engine fact changes how this part was done. With `unit: "%"` the key is the fraction (grade.js `numValue` divides what is typed by 100), so setting the unit on these widgets means re-keying every one (6 to 0.06, with the tol and every wrong value). The brief says never to change a key, so I took the other route the rule offers: a `wrong[]` entry for the decimal form and its `byKey` line, no key, tol or unit touched. A typed `0.5%` reads as 0.005 and meets the same entry, so the typed % sign gets the line too.

- Added `decimal` (key over 100) on 47 widgets; key over 10,000 ("returns written as decimals") on the 24 whose question asks for %². Band: the key's tol scaled, at least 2 per cent of the value, and at least half a unit where the question asks for decimal places (so no new `[wrong-band]`).
- Line patterns: "0.06 is 6% written as a decimal. The field asks for the number of per cent, so type 6 without a % sign." For %²: "... is the answer with the returns written as decimals. The question asks for %², so multiply by 10,000 and type ...". For percentage points: "... is 6 points written as a decimal. Type the number of percentage points, 6."
- Left, with reason (3): `estimation/l4-bias-against-variance` screens[3] (decimal 0.000025 falls inside the existing `var-only` 0 slip, band 0.0001); `linear-maps/l14-orthogonal-complements` screens[11] (0.0001 inside `zero`, band 0.002 wide); `linear-maps/l16-self-adjoint` screens[11] (key 0, no decimal form).
- Content fault (key is a decimal while the prompt asks for per cent): none found. If the lead still wants `unit: "%"` on the genuine per cent figures (labels "in per cent": regression/l1, estimation/l9 to l11, momentum-rep, stat-models), each needs its key, tol and wrong values divided by 100: a separate re-key task.
- Tool limit to raise: `PERCENT_ASKED` fires on "in %²", "in $\%^2$" and "with rates in per cent" (numerics/l8-splines screens[2]); none of those ask for a percentage. 24 of the 71 are of that kind. The decimal slip is still a real slip there (returns written as 0.02, variance 0.0004), so the entries stay.
- Graded values changed: none. Every key, tol and unit is as before. Each new entry lies outside the answer band and every other wrong band (check.py).

## B. tight-band (7 widened; 2 handed to C; 17 left)

Rule used: widen to one unit of the last place asked, only where the stored answer has more places than asked and no wrong value meets the wider band. Where the printed figure in the explanation is the only complaint and the question asks for more places than that figure shows, the band is already wider than one unit, so nothing to widen.

Widened (tol.abs old to new; key unchanged): `series/problems-2` items[2].parts[0] 0.005 to 0.01; `integrals/problems-4` items[2].parts[1] 0.0005 to 0.001 and parts[3] 0.5 to 1 (accept lines updated: "2.048 ± 0.001", "any value from 13.55 to 15.55"); `exams/stage-3` items[6] 0.00005 to 0.0001 (unit %, so 0.01 per cent) , items[8].parts[1] 0.00005 to 0.0001 (unit %), items[14].parts[0] 0.005 to 0.01; `exams/topic-0.2` items[22] 0.005 to 0.01.
Accepted ranges now: 7.414 to 7.434; 2.0475 to 2.0495; 13.55 to 15.55 (14 and 15 both); 0.776 to 0.796 per cent; 1.0555 to 1.0755 per cent; 1.404 to 1.424; 2.7556 to 2.7756.

Left, with reason (17):
- `mental-pressure/l8-square-roots` quiz[0]: wrong `bracket` (9, band 0.005) lies inside 8.9443 ± 0.1. Deliberate slip.
- `exams/topic-3.1` items[21]: wrong `unweighted` (2.17732, band 0.005) meets 2.16401 ± 0.01. The natural 2.17 is that slip.
- Printed figure coarser than the places asked (harmless, form asked is accepted): `puzzles/l2-every-coupon` quiz[0], `puzzles/l4-indicator-tricks` quiz[2], `puzzles/review-1` items[2], `mm-games/l3-how-wide` quiz[0], `mm-games/review-1` items[2] and [5], `mm-games/homework-1` items[6], `mm-games/homework-3` items[7], `mm-games/l17-options-on-a-game` quiz[2] (all ask four places or a fraction, bands already ± 0.0005, wider than one unit); `random-vars/homework-2` items[1] (asks three places, prints 0.17; 0.17 is two places); `bank/probability-2` items[8] (four places or a fraction, prints 0.52).
- Fraction asked, decimal printed: `counting-chance/review-2` items[7] ("Give a fraction", prints 0.0005), `analysis/l4-archimedes` quiz[2] (fraction m/n; 3/7 accepted).
- Tool limit: `counting-chance/l9-double-counting` quiz[1] and [2] ("0 decimal places" read from prose about whole numbers drawn; the answer is a probability).

## C. exams/stage-3 `r-t-bar` and `r-best-of-twenty`

Both are accepted by band; the item still tests the same thing.
- `r-t-bar` (items[7].parts[0]): key 2.754242 = 0.45 / (3.1 / sqrt 360) (and 0.45 sqrt 360 / 3.1). Keeping the standard error to the 0.163 the explanation prints gives 0.45 / 0.163 = 2.7607. Band ± 0.005 to ± 0.01 (old to new), now taking 2.75 and 2.76. The explanation says so: "so t ≈ 2.75 (2.76 if you keep the rounded 0.163)". Wrong slips 0.145161 and 0.795081 stay clear.
- `r-best-of-twenty` (items[11]): key 0.225156 = 1 - (1 - 0.012674)^20 (checked by erfc, by erf and by log1p). Tables at z = 2.24 give 1 - 0.9875^20 = 0.2224, and 1 - 0.775 = 0.225, so 0.22 is as reasonable as 0.23. Band ± 0.005 to ± 0.006, taking 0.22 and 0.23 but not 0.21 or 0.24; `added-chances` (0.253473) stays clear. Explanation now ends "about 0.23 (0.22 from table values)".
- Graded values changed: r-t-bar now also accepts 2.744 to 2.764 (was 2.749 to 2.759); r-best-of-twenty also accepts 0.219 to 0.231 (was 0.220 to 0.230).

## D. wrong-misrouted (10 of 10 fixed, all content faults; none was the grader)

| item | cause | fix |
| --- | --- | --- |
| ds/review-4 items[2] | `none0` and `nodes` both 4, `none0` had no line | removed `none0`; `nodes` line now names both slips (nodes on the path, or `height(None)` returning 0) |
| estimation/homework-3 items[1] | `one-pseudo` (n+1)/(n+1) is 1, equal to `mle` | removed `one-pseudo`; `mle` line says (n+1)/(n+1) is the same number and why the bottom is n + 2 |
| limits/homework-5 items[3] | `unsimplified` x²/(1+x²) equals `no-chain` 1/(1+1/x²) | removed `unsimplified`; `no-chain` line gives the simplified form |
| multivar/homework-5 items[0] | `noJ` and `area` both 3 (both recomputed: integral without Jacobian 3, area 3) | removed `area`; `noJ` line names both |
| markov/l20 screens[5] | `win` 1 ± 0.001 swallowed `most` 0.999 | `win` tol 0.001 to 0.0004, `most` 0.001 to 0.0005 |
| multivar/l4 screens[8] | `rates` 0 ± 0.5 swallowed `per-option` 0.14 | `rates` tol 0.5 to 0.1 |
| numerics/l12 screens[0] | `exact` 0.052253 ± 0.0002 swallowed `small` 0.052222 | `exact` tol 0.0002 to 0.00002 (Euler h = 0.02, h = 0.04 and the exact value recomputed in check.py) |
| stat-learning/review-2 items[0] | `pos` 0.0222 and `flip` 0.0217, both ± 0.0005, overlap | `pos` 0.0005 to 0.0003, `flip` 0.0005 to 0.00015 (values recomputed: 9.2/9 - 1 and 1 - 9/9.2) |
| taylor/l2 screens[10] | `zero` 0 ± 0.5 swallowed `per-contract` 0.5 | `zero` tol 0.5 to 0.1 |
| trees/l13 screens[7] | `rule` 8 ± 0.05 swallowed `atm` 7.97 | `rule` tol 0.05 to 0.01, `atm` 0.05 to 0.015 |

Graded values changed: narrowed catch bands only (a learner typing within the old wider band but outside the new now gets the generic line instead of a slip line): markov win/most, multivar `rates`, numerics `exact` (5.2253 ± 0.02 per cent to ± 0.002), stat-learning `pos`/`flip`, taylor `zero`, trees `rule`/`atm`. No key, no accepted answer changed. Removed entries `none0`, `one-pseudo`, `unsimplified`, `area` never fired (a duplicate was first-matched away).
The trees `atm` 7.97 and `rule` 8 are authored values taken from the lesson's curve; `check.py` verifies only that the bands no longer meet.
No inbox bullet written: no cause was in the grader.
