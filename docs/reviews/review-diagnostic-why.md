# Second read: diagnostic `why` lines (KNOWN_ISSUES item 7)

Session S, 5 Nov. Scope: every `requires` entry with `gate: false` in `content/courses/*/course.json`. KNOWN_ISSUES says 23; the source has 25 (the item 8 lever in session R added two). Each line shows on the learner's card as "Check first: <level>" followed by the `why` (ENGINE-BACKLOG 552).

Method: all 25 read for voice and fit to the card; truth checked against the lesson files for 1, 3, 16, 23 and 25 (reflection is markov L3, `l11-reflection`; brainteasers `l9-egg-drop` objective names dynamic programming; odes Euler and Runge-Kutta orders do come from the Taylor remainder).

## Finding D1: ten lines argue against the check they introduce

The lines were drafted to justify downgrading an edge, so they tell the auditor the prerequisite is not needed. On a card headed "Check first" that reads as a contradiction: the learner is told to check something and, in the same breath, that it is not used. No line is false; the problem is audience.

| # | Edge | Current `why` | Problem | Proposed `why` |
|---|---|---|---|---|
| 2 | analysis needs least-squares/L1 | Length from the dot product and perpendicularity help with norms in metric examples; only a little is used. | "only a little is used" | Metric examples use length from the dot product and perpendicularity. |
| 4 | coding-int needs contests/L3 | Bitmasks and difference arrays overlap with the XOR, mask and sweep patterns, but this level teaches them itself. | "teaches them itself" | XOR, mask and sweep patterns go faster if bitmasks and difference arrays are familiar. |
| 5 | coding-int needs contests/L4 | ... overlap with triage and partial credit, but are not required. | "not required" | Triage and partial credit build on contest timing habits: ordering problems and debugging fast. |
| 6 | cpp needs first-python/L3 | ... are easier after Python functions and scripts; the level does not need them. | "does not need them" | C++ functions, headers and loops are easier after Python functions and scripts. |
| 8 | eigen needs multivar/L4 | Bivariate normal density may use double integrals, but no lesson objective visibly needs them. | auditor voice ("visibly") | The bivariate normal density is easier to read with double integrals in hand. |
| 9 | ensembles needs stat-learning/L3 | Trees are introduced as yes-no classifiers; logistic regression and ROC are only needed from later levels. | names what is not needed here | Later levels compare trees with logistic regression and use ROC curves. |
| 18 | options needs markets/L2 | Option payoffs need only shares and prices from markets; bonds, yields and returns are not used. | lists what is not used | Option payoffs use share prices and the vocabulary of trading shares. |
| 20 | research-int needs pytest/L2 | ... touch test design lightly; pytest's edge cases help but are not required. | "not required" | Take-home reports and edge-case interpolators reuse pytest's habit of testing edge cases. |
| 22 | stat-models needs limits-thm/L4 | ... use densities and sums of variables lightly; no joint-density use is visible. | auditor voice | Kernel density estimates and permutation tests use densities and sums of variables. |
| 15 | momentum-rep needs alpha/L4 | Level 1 only reads the paper; the long-short, turnover and cost machinery from alpha is needed when replicating. | says level 1 does not need it | Replicating the paper uses the long-short, turnover and cost machinery from alpha. |

Lines 11, 12, 13, 16, 19, 21 and 24 carry a softer form ("only a small part", "a fraction of the level"). These read acceptably as a reason the check is advisory and can stay.

## Lines that hold as written

1, 3, 7, 10, 11, 12, 13, 14, 16, 17, 19, 21, 23, 24, 25: specific, learner-facing, and true where checked.

## Recommendation

A Sonnet fix pass on the ten `course.json` lines above (fix agents may edit `course.json`; content authors may not). Raise as a validator warning only if the class recurs: a `why` on a `gate: false` edge that contains "not required", "not needed", "does not need" or "not used" (protocol 6 threshold not yet met: seen once).

## Fix pass

D1: fixed 10, disputed 0, deferred 0. Each old line matched the file in full; each Proposed `why` applied unchanged (lesson files for the named ideas spot-checked: bit tricks, intervals, ROC and logistic, turnover, bivariate normal, shares). Edits are in `course.json` only, formatting kept.

| Course | Edge | Old | New |
|---|---|---|---|
| analysis | least-squares/L1 | Length from the dot product and perpendicularity help with norms in metric examples; only a little is used. | Metric examples use length from the dot product and perpendicularity. |
| coding-int | contests/L3 | Bitmasks and difference arrays overlap with the XOR, mask and sweep patterns, but this level teaches them itself. | XOR, mask and sweep patterns go faster if bitmasks and difference arrays are familiar. |
| coding-int | contests/L4 | Contest timing habits (ordering problems, debugging fast) overlap with triage and partial credit, but are not required. | Triage and partial credit build on contest timing habits: ordering problems and debugging fast. |
| cpp | first-python/L3 | C++ functions, headers and loops are easier after Python functions and scripts; the level does not need them. | C++ functions, headers and loops are easier after Python functions and scripts. |
| eigen | multivar/L4 | Bivariate normal density may use double integrals, but no lesson objective visibly needs them. | The bivariate normal density is easier to read with double integrals in hand. |
| ensembles | stat-learning/L3 | Trees are introduced as yes-no classifiers; logistic regression and ROC are only needed from later levels. | Later levels compare trees with logistic regression and use ROC curves. |
| options | markets/L2 | Option payoffs need only shares and prices from markets; bonds, yields and returns are not used. | Option payoffs use share prices and the vocabulary of trading shares. |
| research-int | pytest/L2 | Take-home reports and edge-case interpolators touch test design lightly; pytest's edge cases help but are not required. | Take-home reports and edge-case interpolators reuse pytest's habit of testing edge cases. |
| stat-models | limits-thm/L4 | Kernel density estimates and permutation tests use densities and sums of variables lightly; no joint-density use is visible. | Kernel density estimates and permutation tests use densities and sums of variables. |
| momentum-rep | alpha/L4 | Level 1 only reads the paper; the long-short, turnover and cost machinery from alpha is needed when replicating. | Replicating the paper uses the long-short, turnover and cost machinery from alpha. |

Gates: validate 0 errors, 2104 warnings (text-only edits, no new warning sources); test-check-first all passed; closure mock-superday-trader reads 96 levels, 32 courses, 422 lessons.
