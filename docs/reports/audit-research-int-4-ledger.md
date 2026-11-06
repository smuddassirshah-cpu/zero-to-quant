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
