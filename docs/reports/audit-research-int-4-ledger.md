# Claim ledger: research-int level 4 (concept audit, blind read)

Files: `app/content/courses/research-int/` l16 to l20, review-4, homework-4. Script: `docs/reports/research-int-L4-concepts.py` (`sim: concepts:<check name>` below). Sources: Wooldridge, *Introductory Econometrics* (W); Efron and Tibshirani, *An Introduction to the Bootstrap* (ET); Haykin, *Adaptive Filter Theory* (H, ch. 10 RLS); Higham, *Accuracy and Stability of Numerical Algorithms* (Hi, ch. 1.9 and 4); Lopez de Prado, *Advances in Financial Machine Learning* (LdP); pandas and numpy documentation (pd, np). Verdicts: correct, wrong, imprecise, misleading, unverified.

## l16-interpolating.json

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l16 | summary.ideas[0] | Sort, merge repeated x by their mean, drop missing values before interpolating | correct | convention stated; np.interp needs increasing xp (np docs); sim: concepts:L16 hand bisection equals np.interp |
| l16 | summary.ideas[1] | Bracket by bisection, add the fraction of the rise; past the ends hold the nearest value | correct | derivation (equal slopes); np.interp default left/right = fp[0], fp[-1] (np docs) |
| l16 | summary.ideas[2] | pandas fills by position unless you ask for the index; uneven stamps need method="index" | correct | pd docs Series.interpolate: linear "ignores the index"; sim: concepts:L16 default linear fills by position |
| l16 | summary.formula | y = y0 + (y1 - y0)(x - x0)/(x1 - x0) for x0 <= x <= x1 | correct | derivation screens[8] |
| l16 | summary.trap | A default fill right on even spacing is wrong on uneven stamps | correct | sim: concepts:L16 default linear ignores a DatetimeIndex too |
| l16 | screens[0].hints, feedback.byKey.half, carry | Two gaps and the landing make three equal steps; half splits over two; carry ignores 112 | correct | derivation 12/3 = 4 |
| l16 | screens[0].explain | Straight-line fill is linear interpolation | correct | definition |
| l16 | screens[1].hints[1] | If points arrive in any order, sort by x first | correct | np.interp requires increasing xp (np docs) |
| l16 | screens[1].feedback.byKey.rise, unit | rise forgets to add y0; unit adds x as if the rise were 1 per unit | correct | derivation |
| l16 | screens[2].explain, byKey.listed | Sorted, the bracket of 2.5 is (2, 25), (3, 30); using the first two listed is wrong | correct | sim: concepts:L16 formula keys |
| l16 | screens[3].prose, explain | Past the largest x hold the nearest value; at x = 0 the same rule returns 10 | correct | convention stated; np.interp default (np docs); sim: concepts:L16 np.interp ends and one point |
| l16 | screens[3].byKey.extend | Extending the last segment is extrapolation, not interpolation | correct | definition |
| l16 | screens[4].prose, explain | Merge repeats by their mean, then interpolate | correct | convention stated; derivation 15 to 30 halfway 22.5 |
| l16 | screens[5].explain, byKey.position | By time, 1 is a quarter of 0 to 4 so 103; by position 106 | correct | derivation; sim: concepts:L16 formula keys |
| l16 | screens[6].prose, canvas | pd.Series([100, nan, 112], index=[0, 1, 4]).interpolate() gives 106 | correct | sim: concepts:L16 default linear fills by position |
| l16 | screens[6].options.pos | By position; method="index" uses the stamps | correct | pd docs; sim: concepts:L16 method=index fills by stamp |
| l16 | screens[6].options.dates.why | The default linear treats the values as evenly spaced, even on dates | correct | sim: concepts:L16 default linear ignores a DatetimeIndex too |
| l16 | screens[6].options.near.why | method="nearest" copies a value; the default draws a line | correct | pd docs (nearest is a scipy method on the index); sim explore |
| l16 | screens[6].options.mean.why | The default uses the two neighbours, not a global mean | correct | pd docs |
| l16 | screens[6].feedback.byKey.dates | Without method="index" or "time" the stamps are ignored | imprecise | 'values', 'slinear', 'polynomial', 'nearest', 'quadratic', 'cubic' and 'spline' all read the index (pd docs: scipy methods use the index); sim: concepts:L16 q16-method (EXPECTED_FAIL) |
| l16 | screens[6].explain | The default treats points as evenly spaced; say method="index" or interpolate by hand | correct | pd docs |
| l16 | screens[7].options.raise, explain | Empty input: raise or return NaN and say which; one point: its value everywhere | correct | np.interp raises ValueError on empty xp and returns fp[0] for one point (np docs); sim: concepts:L16 np.interp ends and one point |
| l16 | screens[7].options.zero, last, line why | Zero is an invented price; no last value exists; nothing to extrapolate from | correct | reasoning |
| l16 | screens[8].widget.lines a to d | Equal slopes, clear the denominator, add y0; the fraction across the gap weights the rise | correct | derivation (W App. A, line through two points) |
| l16 | screens[8].lines.x.why | Dropping the division gives 350 at 2.5 and depends on the units of x | correct | 100 + 100 x 2.5 = 350 |
| l16 | screens[9].options.full | Sort, average repeats, drop gaps, bisect, hold the ends | correct | method summary |
| l16 | screens[9].options.poly.why | A global polyfit line is a regression; an interpolator passes through each point | correct | definition |
| l16 | screens[9].options.ffill.why | Carrying forward ignores the later point and makes steps | misleading | true, but the later point is the future: a forward fill is the one fill that is look-ahead free for a feature series, while linear interpolation reads y1 at t1 > t (derivation from the formula; LdP ch. 7 on leakage); sim: concepts:L16 linear fill reads the later point, ffill reads only the past |
| l16 | screens[9].options.extend.why, explain | Past the ends we hold; bisection needs sorted x | correct | convention; bisect precondition |
| l16 | screens[10].prose, explain | 312 quotes, 15 blank, 12 seconds twice; dropping blanks leaves 297, merging 11 pairs leaves 286 | correct | sim: concepts:L16 ticks counts (one duplicated second has a blank copy) |
| l16 | screens[10].solution | dropna, groupby mean, sort; bisect_right bracket; np.interp agrees | correct | harness: solution 11/11, starter 1/11; sim: concepts:L16 hand bisection equals np.interp |
| l16 | screens[10].explain | numpy.interp needs the times in increasing order | correct | np docs ("xp must be increasing") |
| l16 | screens[11].options.vec, explain | Sort once, then searchsorted or np.interp vectorises every query | correct | np docs; algorithmic |
| l16 | screens[11].options.loop.why | The cost is the interpreter, not the algorithm | correct | bisection is O(log n) per query; the loop is per-row Python overhead |
| l16 | screens[11].options.spline.why | A spline is not faster and changes the answers | correct | spline evaluation is also a bracket search plus a cubic; it does not pass straight lines between points |
| l16 | screens[11].options.sort.why | Re-sorting costs n log n per query | correct | sort complexity |
| l16 | quiz[0] | (0,10),(4,50) at 1 gives 20; unit slip 11 | correct | sim: concepts:L16 formula keys |
| l16 | quiz[1] | One point: its value held everywhere | correct | np.interp one point (np docs); sim |
| l16 | quiz[2] | Times 0, 3, 4: 16 by time, 14 by position | correct | sim: concepts:L16 formula keys |
| l16 | quiz[3].options | s.interpolate(method="index") fills by time; default by position; ffill and nearest draw no line | correct | pd docs; sim |
| l16 | quiz[3].explain | Only method="index" or "time" uses the stamps as the x values | imprecise | false as an "only": values, slinear, polynomial, nearest, quadratic, cubic and spline use the index; time needs a DatetimeIndex (pd docs); sim: concepts:L16 q16-method (EXPECTED_FAIL) |

## l17-regression-by-group.json

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l17 | summary.ideas[0] | Split by group, fit each with cov over var or polyfit, gather the slopes | correct | OLS slope = cov/var with one divisor (W 2.2, eq. 2.19); sim: concepts:L17 three routes agree |
| l17 | summary.ideas[1] | Fewer than 3 rows gives NaN; a two-point line cannot look steepest | correct | convention stated; two points leave 0 df for sigma |
| l17 | summary.ideas[2], formula | Slope = sum((x - xbar)(y - ybar))/Sxx; SE = sigma/sqrt(Sxx) | correct | W Thm 2.2 (eq. 2.57), homoskedastic independent errors; sim: concepts:L17 SE of slope (MC 200k) |
| l17 | summary.formula.note | For days 1 to n, Sxx = n(n^2 - 1)/12 | correct | derivation sum of squares about the mean of 1..n; sim: concepts:L17 Sxx closed form |
| l17 | summary.trap | The steepest slope may rest on two rows | correct | screens[5] data |
| l17 | screens[0].hints, explain | Centre days at 2.5, products sum 4.5, Sxx 5, slope 0.9; Marsh -0.6, Plain 0 | correct | sim: concepts:L17 hand slopes |
| l17 | screens[0].byKey.ends | Last minus first over three days ignores the middle days | correct | (13 - 10)/3 = 1.0 is not the LS slope |
| l17 | screens[1].solution | groupby('town').apply with a < 3 guard, polyfit slope | correct | harness: solution 6/6, starter 0/6; pd docs include_groups (2.2) |
| l17 | screens[1].explain | The guard turns Wick's two rows into NaN | correct | data: Wick has 2 rows (sim: concepts:L17 Wick two rows) |
| l17 | screens[2].explain | Four slopes below zero; whether Deal cools is a question about standard errors | correct | sim: concepts:L17 four negative slopes |
| l17 | screens[3].prose | Noise 1.5, 100 days, Sxx = 83,325 | correct | sim: concepts:L17 Sxx closed form |
| l17 | screens[3].hints, feedback | SE = sigma/sqrt(Sxx) = 0.0052; Deal and Elgin within two of it | correct | W Thm 2.2 with sigma known; sim: concepts:L17 SE of slope; concepts:L17 four negative slopes (two inside) |
| l17 | screens[3].byKey.sd, n | Dividing by sqrt(100) or by 100 ignores the spread of the days | correct | derivation: the divisor is sqrt(Sxx) |
| l17 | screens[3].explain | Two SE is 0.0104; Deal and Elgin inside, the other ten outside | correct | sim: concepts:L17 four negative slopes |
| l17 | screens[4].prose | Cov over var, polyfit and statsmodels agree to ten decimals; R^2 from 0.0001 (Deal) to 0.8023 (Leith) | correct | sim: concepts:L17 three routes agree, concepts:L17 R2 runs |
| l17 | screens[4].options.same, explain | All three solve the same least-squares problem, which has one minimiser; cov/var is its closed form | correct | W 2.2: the normal equations have a unique solution when Sxx > 0 |
| l17 | screens[4].options.lib, clean, round why | Separate code paths; agreement on messy data too; ten decimals is not rounding | correct | sim: 1.8e-16 disagreement on the towns file |
| l17 | screens[5].prose | Unguarded, Wick's two readings give 0.3 per day, three times Leith | correct | sim: concepts:L17 Wick two rows give 0.3 |
| l17 | screens[5].options.two, explain | Two rows fit any line exactly, so the slope carries no evidence | correct | 0 residual df, no sigma estimate; under the lesson's sigma SE = 1.5/sqrt(0.5) = 2.12, so 0.3 is 0.14 SE from zero (sim: concepts:L17 Wick slope is 0.14 SE) |
| l17 | screens[5].options.big.why | A slope with no standard error is not evidence | correct | as above |
| l17 | screens[5].options.bug.why | polyfit is right: two points make a line; the meaning is the problem | correct | exact fit |
| l17 | screens[6].prose | Cov over var needs the variance of the days, undefined for one day | correct | sample variance has n - 1 = 0 in the divisor |
| l17 | screens[6].hints[1] | A slope needs two different days; a check on noise needs three | correct | Sxx > 0 needs two distinct x; sigma needs n - 2 >= 1 (W 2.5) |
| l17 | screens[6].options.nan, explain | Return NaN and report the skips; zero is a direction, the level is not a rate, dropping hides | correct | reasoning |
| l17 | screens[7].lines.a | Slope = sum((x - xbar) y)/Sxx, weights (x - xbar)/Sxx | correct | W eq. 2.49 (sum((x - xbar) ybar) = 0) |
| l17 | screens[7].lines.b, c | Independent y with variance sigma^2 gives Var = sigma^2 sum((x - xbar)^2)/Sxx^2 = sigma^2/Sxx | correct | W Thm 2.2 proof; sim: concepts:L17 SE of slope (MC 200k) |
| l17 | screens[7].lines.d | Sxx = 100 x 9,999/12 = 83,325; SE 0.0052 | correct | sim: concepts:L17 Sxx closed form |
| l17 | screens[7].lines.x.why | sigma^2/n is the variance of a mean, not a slope | correct | derivation; MC separates 0.0052 from 0.15 |
| l17 | screens[7].explain | Wider spread of days shrinks the SE; longer samples pin slopes down | correct | Sxx grows as n^3 for daily data |
| l17 | screens[8].prose, options.split | Split, fit with cov/var, guard under 3 rows, combine | correct | method summary; convention |
| l17 | screens[8].options.pool.why | Pooling reports one slope for groups with different slopes | correct | reasoning (pooled slope is a weighted mix, W 7.4 interaction) |
| l17 | screens[8].options.loop, eye why | Row-by-row refits keep only the last; dropping by eye has no stated rule | correct | reasoning |
| l17 | screens[9].prose, explain | Beta = cov(return, market)/var(market) = 1.3; a rolling beta is that slope per window | correct | CAPM beta as OLS slope (W 2.2); sim: concepts:L17 beta |
| l17 | screens[9].byKey.inv | var over cov is the inverse | correct | 0.000180/0.000234 = 0.769 |
| l17 | screens[10].options.vec, explain | groupby sums sum x, sum y, sum xy, sum xx, n give every slope in one vector expression | correct | normal equations in sums (W App. 2A); sim: concepts:L17 vectorised sums equal polyfit |
| l17 | screens[10].options.sm.why | statsmodels per group is slower and the slope is identical | correct | same minimiser; sim: concepts:L17 three routes agree |
| l17 | screens[10].options.loop, sample why | A Python loop slices 5,000 times; fitting 100 drops groups silently | correct | reasoning |
| l17 | quiz[0] | (1,5),(2,5),(3,8),(4,6): products 3, Sxx 5, slope 0.6; ends slip 0.333 | correct | sim: concepts:L17 hand slopes |
| l17 | quiz[1] | Noise 3.0 doubles the SE to 0.0104 | correct | SE is linear in sigma (W Thm 2.2) |
| l17 | quiz[2] | groupby.apply with a scalar per group returns a Series indexed by town; transform gives one per row | correct | pd docs GroupBy.apply; sim: concepts:L17 apply returns a Series per group |
| l17 | quiz[3] | A two-row fit has R^2 = 1 and says nothing about the slope | correct | zero residuals; sim: concepts:L17 two-point R2 is 1 |

## l18-updating-a-fit.json

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l18 | summary.ideas[0] | A straight-line fit needs only five running sums; a row in is addition, out is subtraction | correct | normal equations in sums (W App. 2A); sim: concepts:L18 sums equal polyfit, concepts:L18 running-sum keys |
| l18 | summary.ideas[1] | With several predictors keep (X'X)^-1; Sherman-Morrison updates it at p^2 a row | correct | Sherman-Morrison identity (H ch. 10, RLS); O(p^2) per rank-one update; sim: concepts:L18 rank-one update equals refit |
| l18 | summary.ideas[2], trap | Raw sums of squares lose digits on large numbers, so centre x before summing | correct | Hi 1.9 (cancellation) and 4.2; sim: concepts:L18 naive variance 1e9 case is 0.0 |
| l18 | summary.formula | m = (n sum xy - sum x sum y)/(n sum xx - (sum x)^2); add a row to update, subtract to downdate | correct | W App. 2A; sim: concepts:L18 running-sum keys |
| l18 | screens[0].explain | Five numbers are all a straight-line fit needs; the points can be thrown away | correct | for the coefficients (the SE would also need sum y^2); W App. 2A |
| l18 | screens[1].hints, explain, byKey.ratio | Slope 0.8 from (156 - 140)/(120 - 100); intercept 1.5; sum xy / sum xx skips the centring | correct | sim: concepts:L18 running-sum keys; sum xy / sum xx is the through-origin slope |
| l18 | screens[2].explain, byKey | Adding (5, 8) to each sum gives 1.3, intercept 0.5, at no refit cost; old sums and the point alone are wrong | correct | sim: concepts:L18 running-sum keys, concepts:L18 rank-one update equals refit |
| l18 | screens[3].explain, byKey.kept | Removal is addition run backwards; slope 1.4, intercept 0.1, equal to refitting the four points | correct | sim: concepts:L18 running-sum keys |
| l18 | screens[4].prose | Keep P = (X'X)^-1; a new row divides by 1 + x'Px | correct | Sherman-Morrison: (A + xx')^-1 = A^-1 - A^-1 x x' A^-1/(1 + x'A^-1 x) |
| l18 | screens[4].hints, feedback | Px = (-1, 0.5), x'Px = 1.5, denominator 2.5; new inverse P - Px(Px)'/2.5 | correct | sim: concepts:L18 P and 1 + x'Px = 2.5 |
| l18 | screens[4].byKey.big | x'x = 26 forgets P in the middle | correct | 1 + 25 = 26 |
| l18 | screens[4].explain | Innovation 8 - x'beta = 2.5 moves beta to (0.5, 1.3), equal to a full refit | correct | RLS gain K = P_new x, beta += K (y - x'beta) (H ch. 10); sim: concepts:L18 rank-one update equals refit |
| l18 | screens[5].starter docstring | coef returns [nan, nan] with fewer than 2 rows or when every x is equal | imprecise | the solution tests den == 0, exact only when the sums are exact; for repeated non-integer x about 28% of cases return a number (sim: concepts:L18 OnlineLine 'NaN when every x is equal', EXPECTED_FAIL); Hi 2.2 |
| l18 | screens[5].solution | Five sums, remove as the reverse of add, slope and intercept from the sums | misleading | harness: solution 8/8, starter 0/8, so it passes; but the class keeps raw sums, which the lesson's own trap and derive then show failing on large x, and nothing ties the class back to the fix (sim: concepts:L18 raw-sum class fails on x near 1e9) |
| l18 | screens[5].explain | Each call touches five numbers; a rolling fit over 250 days costs no more than one over 25 | correct | O(1) per update |
| l18 | screens[6].prose, hints | Squares near 1e18 exceed float64's exact range; the two big terms differ by 2, below the rounding step of 512; they round to the same number | correct | Hi 2.1 (ulp at 3e18 is 512); sim: concepts:L18 rounding step, concepts:L18 naive variance 1e9 case is 0.0 |
| l18 | screens[6].widget.answer, explain | The formula returns exactly 0.0 against a true 1; float64 holds about 16 digits, the squares need 19 | correct | sim: concepts:L18 naive variance 1e9 case is 0.0; 53-bit mantissa is 15.95 decimal digits |
| l18 | screens[7].options.silent, explain | Sums cannot tell a real row from a made-up one; the sums then describe no dataset | correct | sim: concepts:L18 removing (7, 9) never added |
| l18 | screens[7].options.raise.why | n goes negative only after many wrong removals | correct | n is a count decremented by one |
| l18 | screens[7].options.same, refit why | The row does not cancel; there was no such point | correct | reasoning |
| l18 | screens[8].prose, lines a to c | Subtracting c from x leaves the slope unchanged and shifts the intercept to a' - mc | correct | algebra: cov(x - c, y) = cov(x, y), var(x - c) = var(x) |
| l18 | screens[8].lines.d | For 1e9 + 1..3 and y = 1, 3, 2 with c = 1e9: m = 0.5, a' = 1, a = -499,999,999 | correct | sim: concepts:L18 centre-first numbers |
| l18 | screens[8].lines.x.why, byKey.x | "Subtract c from y as well" leaves the huge x^2 sums where the cancellation happens | imprecise | the option says "as well": with x also shifted no large x^2 sum remains and the fit is exact (sim: concepts:L18 derive distractor x, EXPECTED_FAIL); the why describes shifting y instead of x |
| l18 | screens[8].explain | Fitting on small numbers keeps every sum exact enough | correct | Hi 1.9 |
| l18 | screens[9].prose, options.cheap | An update costs p^2 a row; a refit about n p^2; for n = 1e6, p = 10 the gap is 1e6 | correct | forming X'X is O(np^2), the solve O(p^3) extra; Sherman-Morrison O(p^2) |
| l18 | screens[9].options.approx.why, explain | Sherman-Morrison equals the refit, exact up to rounding | correct | identity; sim: concepts:L18 rank-one update equals refit |
| l18 | screens[9].options.solve, same why | A refit also reads every row | correct | O(np^2) to form the normal equations |
| l18 | screens[10].hints, explain, byKey.addonly | Add the entering day, subtract the leaving one, n stays 250; beta 1.24; add-only gives 1.2419 | correct | sim: concepts:L18 running-sum keys |
| l18 | screens[11].options.decay, explain | Old sums are multiplied by lambda before each new row; a row k days old carries weight lambda^k | correct | exponentially weighted RLS (H 10.2); sim: concepts:L18 forgetting factor equals WLS |
| l18 | screens[11].options.window, newrow, same why | A fixed window is a hard cut; the new row keeps full weight; without decay old rows never fade | correct | H 10.2 |
| l18 | quiz[0] | Sums 3, 6, 9, 14, 19 give 0.5; sum xy / sum xx is 1.357 | correct | sim: concepts:L18 running-sum keys |
| l18 | quiz[1] | Adding (4, 8) gives sums 4, 10, 17, 30, 51 and slope 1.7 | correct | sim: concepts:L18 running-sum keys |
| l18 | quiz[2].options | Centre x first is the cure; float32 loses sooner; rounding discards digits; summation order leaves the cancellation | correct | Hi 1.9 and 4.2 (cancellation between two near-equal totals is order-independent) |
| l18 | quiz[3] | n p^2 / p^2 = n = 10,000 | correct | sim: concepts:L18 update is n times cheaper |

## l19-timed-data-task.json

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l19 | summary.ideas[0], trap | List the problems, clean in a fixed order (text, repeated ids, bad prices); dropping odd rows first loses good rows | correct | repairs before drops is the stated rule; sim: concepts:L19 15 repeated ids, 12 exact copies before text cleaning |
| l19 | summary.ideas[1], formula | VWAP = sum pq / sum q; slip = s (p - m)/m x 1e4 with s = +1 buy, -1 sell | correct | definition of VWAP; sign derivation screens[8] |
| l19 | summary.ideas[2] | Write down every count so a reviewer can check | correct | reproducibility practice (l20) |
| l19 | screens[0].question, byKey.firstcopy | For the repeated id, drop the later copy (keep the first) | correct | convention stated; pandas drop_duplicates keep='first' (pd docs) |
| l19 | screens[1].prose, explain | 15 ids repeat; 12 are exact copies; drop_duplicates() before text cleaning misses 3; or drop by order_id alone | correct | sim: concepts:L19 15 repeated ids, 12 exact copies before text cleaning, 15 after; pd docs subset |
| l19 | screens[2].prose | Clean in a fixed order: text, then repeated ids, then bad prices | imprecise | ids before prices is a convention the main file does not need (570 either way, sim: concepts:L19 600 -> 585 -> 570) and only the tiny test enforces it |
| l19 | screens[2].how, tests[6] | The first copy of an id must be the one kept, even when its price is bad | misleading | the tiny case keeps order 7's blank-price copy and drops the order although a later copy has a valid price, against the trap's own rule "repair, drop only bad rows" (sim: concepts:L19 load_clean tiny case, EXPECTED_FAIL) |
| l19 | screens[2].solution | strip and upper the symbol; remove commas and astype(int); drop_duplicates('order_id'); keep notna and > 0 | correct | harness: solution 8/8, starter 0/8; pd docs str.replace (regex False since 2.0) |
| l19 | screens[2].explain | 600 - 15 repeats = 585; 10 blank and 5 of -999 leave 570; ALPHA 230, BRAVO 206, CHARLIE 134 | correct | sim: concepts:L19 600 -> 585 -> 570; harness test 2 |
| l19 | screens[3].prose, solution | VWAP weights each price by its quantity: sum(price x qty) / sum(qty) per symbol | correct | definition; harness: solution 4/4, starter 0/4 |
| l19 | screens[3].explain | VWAPs 50.0152, 120.0146, 8.0005; leaving in -999 and repeats drags ALPHA to 46.3874 | correct | sim: concepts:L19 VWAPs (the 46.3874 is the file with only blanks removed) |
| l19 | screens[3].tests[3], how | The VWAP is not the simple mean of prices | correct | sim: concepts:L19 VWAP is not the simple mean |
| l19 | screens[4].prose, starter | A buyer above mid loses, a seller below mid loses; regress the loss on ln(qty/100) | correct | sign derivation screens[8]; dividing qty by 100 only shifts the intercept |
| l19 | screens[4].solution, hints[2] | polyfit returns slope then intercept; R^2 is the squared correlation | correct | np docs polyfit; R^2 = corr^2 in simple regression with intercept (W 2.3, eq. 2.38 and the note after it); sim: concepts:L19 slope 1.2421 |
| l19 | screens[4].explain | Slope 1.2421 bp per unit of ln(qty/100), SE 0.0486 against a planted 1.2; R^2 0.5346; mean 3.795 bp | correct | sim: concepts:L19 slope 1.2421, SE 0.0486 (statsmodels); 1.2 is 0.87 SE away |
| l19 | screens[5].hints, byKey | 3,200 shares: ln 32 = 3.4657, cost 4.642 bp; 32 without the log gives 40.08; ln 3200 gives 10.362 | correct | sim: concepts:L19 predictions |
| l19 | screens[5].feedback.correct | 4.642 bp is 0.046% of the order's value | correct | 1 bp = 0.01% |
| l19 | screens[6].options.fix, explain | Repair the text, drop only bad rows, count each step: 600, 585, 570 | correct | sim: concepts:L19 600 -> 585 -> 570 |
| l19 | screens[6].options.safe.why | A comma in 1,200 is still 1,200, so dropping odd rows loses good orders | correct | reasoning |
| l19 | screens[6].options.ids, keep why | -999 and blank prices wreck a VWAP; a regression takes impossible prices at face value | correct | sim: concepts:L19 VWAPs (46.39 against 50.02) |
| l19 | screens[7].options.drop, explain | A zero price is impossible; test price > 0 and report the count | correct | reasoning; a zero price gives slippage of 1e4 bp in size (sim: concepts:L19 sign of slippage) |
| l19 | screens[7].options.keep.why | Zero gives a slippage of 10,000 bp in size | correct | s(0 - m)/m x 1e4 = -s x 1e4 |
| l19 | screens[7].options.mean.why | An imputed price has no (real) slippage | correct | the number would measure the imputation, not a trade |
| l19 | screens[7].options.nan.why | A NaN row still counts in the quantity totals | correct | pandas sum skips NaN in the numerator but the qty denominator keeps the row; sim: concepts:L19 NaN price biases the VWAP down |
| l19 | screens[8].lines a to d | Buyer cost p - m, seller cost m - p, both s(p - m); divide by m and scale by 1e4 | correct | derivation; sim: concepts:L19 sign of slippage |
| l19 | screens[8].lines.x.why, explain | p - m for both sides makes a seller below mid look like a gain; a seller at 49.80 against 50 loses 40 bp | correct | sim: concepts:L19 sign of slippage |
| l19 | screens[9].options | Read, list, clean in order, model, record counts; a plot will not show a comma; no trail cannot be checked | correct | reasoning |
| l19 | screens[10].hints, explain, byKey | VWAP 31.225 over 4,000 shares; with the repeat 31.2727 (about 4.8p high); mean of prices 31.1333 | correct | sim: concepts:L19 fills VWAP |
| l19 | screens[11].options.sym, time, side | Split by symbol, time of day and side to test whether one slope fits all | correct | heterogeneity checks; W 7.4 (interactions by group) |
| l19 | screens[11].options.cubic.why | Adding terms until R^2 passes 0.9 tunes on the same data | correct | in-sample selection (ET ch. 17; LdP ch. 11 backtest overfitting) |
| l19 | screens[11].options.big.why | Dropping the largest orders drops data for being large, not wrong | correct | reasoning; size is the regressor |
| l19 | quiz[0] | 900 - 25 - 12 = 863 with no overlap | correct | arithmetic under the stated no-overlap hypothesis |
| l19 | quiz[1] | (2,000 + 6,240)/800 = 10.30; the mean of prices 10.20 ignores the share counts | correct | sim: concepts:L19 fills VWAP |
| l19 | quiz[2] | drop_duplicates compares every column by default, finds non-adjacent rows, needs no sort | correct | pd docs DataFrame.drop_duplicates; sim: concepts:L19 drop_duplicates semantics |
| l19 | quiz[3] | A seller at 49.80 against 50.00: -1 x (49.80 - 50)/50 x 1e4 = +40 bp | correct | sim: concepts:L19 sign of slippage |
