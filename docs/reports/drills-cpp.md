# Drills, pack `cpp` (topic 1.9: C++ foundations and C++ for pricing)

Brief: `docs/briefs/drills-1.1-1.9.md`, pack `cpp`, on top of `docs/briefs/drills-1.8.md` and `docs/briefs/drills-ci-packs.md` (planted solutions, `notes`). Twenty-five C++ drills in `app/content/drills/`, each `"pack": "cpp"`, `"language": "cpp"`, with a row appended to `drills/index.json`: 17 for course `cpp`, 8 for `cpp-pricing`. No `pattern` (none of the fixed vocabulary fits a day-to-day program of this kind); the idea is in `tags`. Skills are the skills the named lesson declares.

## Drills

| id | course / lesson drawn on | tags (idea) | difficulty | pace (s) | hidden tests | planted |
| --- | --- | --- | --- | --- | --- | --- |
| `cpp-clip-returns` | `cpp/l5-value-or-reference` | pass-by-reference, out-parameter | 1 | 420 | 10 | 3 |
| `cpp-fee-pence` | `cpp/l2-fixed-types` | integer-rounding, long-long | 1 | 420 | 12 | 3 |
| `cpp-high-water` | `cpp/l14-vector` | running-maximum, reserve | 1 | 420 | 9 | 3 |
| `cpp-longest-rise` | `cpp/l3-branches-and-loops` | streaks, loops | 1 | 420 | 12 | 3 |
| `cpp-tick-log` | `cpp/l10-invariants` | class-invariant, refuse-bad-input | 1 | 480 | 11 | 3 |
| `cpp-tick-round` | `cpp/l4-functions-and-headers` | default-argument, rounding | 1 | 360 | 12 | 3 |
| `cpp-crossings` | `cpp/l13-templates` | function-template, signal | 2 | 660 | 11 | 3 |
| `cpp-drop-small` | `cpp/l14-vector` | erase-in-loop, iterators | 2 | 600 | 11 | 3 |
| `cpp-fee-tier` | `cpp/l6-const` | const-method, tier-lookup | 2 | 600 | 7 | 3 |
| `cpp-range-out` | `cpp/l7-addresses` | pointer-out-parameter, nullptr | 2 | 540 | 12 | 3 |
| `cpp-session-time` | `cpp/l12-operators` | operator-overloading, modulo | 2 | 660 | 14 | 3 |
| `cpp-temp-limit` | `cpp/l11-creation-destruction` | raii, destructor, reference-member | 2 | 660 | 12 | 3 |
| `cpp-trimmed-mean` | `cpp/l16-algorithms` | sort-and-accumulate, integer-division | 2 | 600 | 12 | 3 |
| `cpp-fill-csv` | `cpp/l3-branches-and-loops` | parsing, strings, long-long | 3 | 1080 | 13 | 3 |
| `cpp-mean-ranks` | `cpp/l16-algorithms` | sort-indices, ties | 3 | 1020 | 11 | 3 |
| `cpp-movers` | `cpp/l15-maps` | map-first-and-last, sort-with-ties | 3 | 1080 | 12 | 3 |
| `cpp-take-all` | `cpp/l19-moving-not-copying` | move-semantics, rvalue-reference | 3 | 900 | 8 | 3 |
| `cpp-compound-df` | `cpp-pricing/l2-cmath` | discounting, compounding | 1 | 420 | 10 | 3 |
| `cpp-prob-between` | `cpp-pricing/l4-normal-cdf` | normal-cdf, erfc | 1 | 480 | 10 | 3 |
| `cpp-cash-or-nothing` | `cpp-pricing/l7-black-scholes-cpp` | black-scholes, digital-option | 2 | 720 | 10 | 3 |
| `cpp-curve-df` | `cpp-pricing/l2-cmath` | discount-curve, interpolation | 2 | 900 | 13 | 3 |
| `cpp-scaled-payoff` | `cpp-pricing/l5-payoff-classes` | payoff-hierarchy, decorator | 2 | 720 | 10 | 3 |
| `cpp-bermudan-put` | `cpp-pricing/l6-binomial-cpp` | binomial-tree, early-exercise | 3 | 1200 | 12 | 3 |
| `cpp-cash-split` | `cpp-pricing/l1-doubles` | fixed-point, rounding, allocation | 3 | 1020 | 15 | 3 |
| `cpp-running-stats` | `cpp-pricing/l8-monte-carlo` | welford, accumulator | 3 | 1140 | 14 | 3 |

Mix: `cpp` 6 / 7 / 4 and `cpp-pricing` 2 / 3 / 3 at difficulties 1 / 2 / 3, so 8 / 10 / 7 in all, as the brief asks. 283 hidden tests, 75 planted solutions. The brief's list is covered: references and const (`clip-returns`, `fee-tier`), vector and string (`high-water`, `drop-small`, `fill-csv`), classes with invariants (`tick-log`), RAII (`temp-limit`), templates (`crossings`), map and algorithms (`movers`, `trimmed-mean`, `mean-ranks`), iterators (`drop-small`), move (`take-all`); for pricing a payoff hierarchy (`scaled-payoff`), a discount curve lookup (`curve-df`), a binomial step (`bermudan-put`), a running statistics accumulator (`running-stats`) and a fixed-point money type (`cash-split`). Class drills are graded through hidden `postlude` helpers that drive the class and return a vector, so examples read as one call with JSON arguments; three drills also carry a `compiles` case (a deleted copy, an `explicit` constructor).

Not repeated: the lesson tasks of both courses were listed first (every code screen, review and homework item) and avoided, in particular `count_up_days`, `max_drawdown`, `vwap`, `average`, `accrue`, `RiskLimit`, `SessionRange`, `Fixed`, `Money`, `Connection`, `Straddle`, `CappedCall`, `Strangle`, `step_back`, `american_put` and `discount`. Two earlier drafts were dropped for being too close: a move-only "slot holder" (lesson l11's `Connection`) and a band class with `width` and `contains` (homework 3's `SessionRange`). The two `sample-cpp-` drills and the `ci-cpp-` drills share no task.

## Planted solutions

Each drill has three, written to the brief's classic slips: integer division (`fee-pence`, `trimmed-mean`, `mean-ranks`), an off-by-one on `size()` (`high-water`, `range-out`, `longest-rise`), a copy where a reference was needed (`clip-returns` twice, `drop-small`, `temp-limit`, `take-all`), wrong start values for an accumulator (`high-water`, `range-out`, `running-stats`), plus an `int` overflow, `%` of a negative, a missing `const`, a non-template overload, a naive sum of squares, `1 + erf` in a far tail and the American-for-Bermudan exercise rule. A truly uninitialised accumulator was not planted: it is undefined behaviour, and at `-O1` it often reads 0 and passes, so no test could be sure to catch it.

On the first `planted-check --require` run all 75 failed at least one hidden test; none passed, so no test had to be added for a planted solution. Two tests were added before that run on purpose: the far-out-of-the-money case of `cpp-cash-or-nothing` (catches `1 + erf`, with `tol` `{rel: 1e-9, abs: 1e-30}`, since the default absolute 1e-12 would accept it) and the `{5, 9, 7}` case of `cpp-tick-log` (catches comparing with the first time).

## Checks

1. `docs/reports/drills-cpp-check.py` (scratchpad venv Python): exit 0, "25 drills, 333 cases compared, errors: 0". The builder computed each `expect` with one Python model; the script holds a second, written apart and by another method where one exists (Fractions for exact rounding and ties, mpmath at 40 digits for the pricing drills, a memoised recursion over tree nodes for the Bermudan put, the pairwise variance formula, Python classes for the payoffs, a hand value with its working for each C++ lambda call). It also checks the brief's worked answer is in the brief, recomputes 15 rounded numbers stated in briefs and notes, the `how` counts, that every example is also a hidden test, the index rows, the pace range, the 8 / 10 / 7 mix and no exclamation marks or dashes in prose.
2. `node tools/validate.mjs`: 0 errors; the warning count (4269) is the same as before the pack, so these files add none.
3. `node tools/playthrough.mjs --drill <id> ... --local-cdn <pkgs>` for all 25: green, model passes every test, starter fails; again with `--mobile`: green. Shots at 440 px of `fill-csv`, `temp-limit`, `bermudan-put`, `movers` and `scaled-payoff` were read; two layout faults were fixed (a markdown list in a brief renders as one paragraph; inline code spans longer than about 42 characters run off a 440 px screen) and every span is now at most 42 characters.
4. `node tools/planted-check.mjs --drill <each of 25> --require --local-cdn <pkgs>`: "25 drills checked, 75 planted solutions, 0 failures".
5. Voice: `voice-scan.py 35` on a copy of the 25 files: 0 explanations over three sentences, 0 sentences over 35 words of 1,417. One sentence (`cash-split` brief, 40 words) was split.
6. `node tools/fresh-check.mjs --drill <id>` for all 25: 0 hits. Two hits on the first run were function names already used by lesson code widgets (`digital_call` in `ito/l16`, `trimmed_mean` in `stat-models/l13`); the functions are now `cash_call` and `latency_trimmed_mean`. At triage settings the only shared run is the boilerplate "can pass 2,147,483,647 ... Each test has a 5-second limit".

No test data comes from a website or book: every list, price and curve was made up for these drills.

## Left open

- `cpp-take-all` counts copies with a `Fill` type that counts its own copy constructor, not with `allocCheck`, which drills do not pass through (inbox).
- `cpp-range-out` cannot plant "writes through `nullptr`": the runner does not trap a write to address 0, so that slip passes every test. The constraints tell the learner to check each pointer.
