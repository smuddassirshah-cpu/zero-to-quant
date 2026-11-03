# Report: puzzles level 3 (Continuous and geometric)

Author: content agent, 3 November 2026. Brief: `docs/briefs/puzzles.md` section "Level 3", with the orchestrator's additions (a follow-up screen per lesson, a pace, `tags` on drill and homework items, no firm names, `longform` only in homework, `shuffle: true` on choices, the stated engine limits).

## Files written

All in `app/content/courses/puzzles/`. Ids, titles, objectives and skills are those of `course.json` (`pz-geometry` on every lesson, `pz-symmetry` also on l14, `pz-expectation` also on l15 and l18).

| File | Screens | Quiz / items | Skills | Notes |
|---|---|---|---|---|
| `l13-broken-stick.json` | 12 | 3 | pz-geometry | title (the four books and *Probability and Markets*), drag-point hook on the unit square (derive caption with the three pieces), tap the two of eight triangles, break-the-longer curve with its area, coin version, ambiguity trap, edge case (a piece of exactly ½ has chance 0), `order` derivation of 2 ln 2 − 1, drill, follow-up (four pieces), risk-budget transfer |
| `l14-semicircle.json` | 11 | 3 | pz-geometry, pz-symmetry | `plane` circle with derive-driven points on angle controls and a `sector` half from the starting point; two points, fixed half, any start, four points, centre-in-triangle edge case, coin-flip trap, disjointness generalise, `expression` n/2^{n−1}, drill, sphere follow-up, 24-hour clock transfer |
| `l15-exceeding-one.json` | 11 | 3 | pz-geometry, pz-expectation | drag hook under u₁ + u₂ = 1, slice slider for the corner 1/6, table of 1/n!, `series` sim running mean to e, trap (2), generalise with the edge case e^{1/2}, `order` derivation, `code` exceed_one_sim, drill, Wald follow-up, parent-order transfer |
| `l16-meeting.json` | 10 | 3 | pz-geometry | tap the meeting band, draggable arrivals with live caption on 15, 10 and 10/20-minute bands, trap (30 of 60), edge case (one waits the hour, one not at all), `expression` 1 − (1 − w)², drill, two-hour follow-up, crossing-orders transfer |
| `l17-buffon.json` | 11 | 3 | pz-geometry | hook names "bank final rounds"; stacked `pair` (floor with the needle, angle-distance rectangle with a draggable drop), area 2/π, length ½, `bars` sim with `exact` and a π estimate from counts, set-up trap, edge case (l > d) in the generalise, `expression` 2l/π, `code` buffon_estimate, drill, noodle follow-up, cost-of-a-digit transfer |
| `l18-expected-distance.json` | 12 | 3 | pz-geometry, pz-expectation | drag hook with `contour` lines of \|x − y\|, pyramid volumes for 1/3, slider on a fixed point (edge case: from the end, ½), `series` sims checking the two stated closed forms, trap (\|E X − E Y\| = 0), max − min generalise, `expression` E\|X − y\|, `code` mean_distance_sim, drill, range follow-up, slippage transfer |
| `review-3.json` | | 10 items (difficulty 3, 2, 3, 4, 3, 2, 4, 2, 3, 3) | all three used skills | every lesson at least once; `timed: { "seconds": 1800 }` (3 minutes an item, a guide clock, no lock) |
| `homework-3.json` | | 9 items (5, 4, 4, 4, 4, 4, 5, 4, 3) | | two `code` (stick_triangle at 5, semicircle_prob and semicircle_sim at 4), one `order` (the semicircle argument, with a distractor), one `longform` (why "break at random" is ambiguous, 10-point rubric, full model), five numeric |

Interview form, per lesson: one `Drill` screen (a two-column `table` of three new puzzles, prose stating "about 3 minutes each, 9 in all; keep your own time") carrying `"tags": ["<family>"]`; one screen titled "Follow-up: ..." with the interviewer's next question on the worked puzzle. Tags (`broken-stick`, `semicircle`, `exceeding-one`, `meeting`, `buffon`, `expected-distance`) are on every drill screen, on quiz items that are drill puzzles, and on every review and homework item. Every `choice` has `shuffle: true`. No `longform` in lessons. No firm names: Buffon is "a puzzle reported in bank final rounds"; *Probability and Markets* is "a free guide from a trading firm", as in level 2.

Edge cases: l13 a piece of exactly ½ (generalise), and breaking the shorter piece (quiz); l14 the centre in the triangle (ladder) and a fixed half (quiz); l15 passing ½, e^{1/2} (generalise); l16 one waits the whole hour, one not at all (generalise); l17 a needle longer than the gap (generalise); l18 the distance from an end, ½ (ladder).

## Validator

`node tools/validate.mjs` from `app/`: **0 errors**, 385 warnings, none in a level-3 puzzles file (the only puzzles warning is the course's own count of unwritten lessons: 12 of 30, 2 of 5 reviews, 2 of 5 homework). Other agents' files were being written at the same time; no transient errors appeared in my runs.

## Playthrough

`node tools/playthrough.mjs --lesson puzzles/<id> --local-cdn <pkgs>`, each lesson alone, with and without `--mobile`; sets with `--set`:

| File | Plain | `--mobile` (with 390 px shots) |
|---|---|---|
| l13-broken-stick | ok, 14 checks, quiz 3/3 | ok, 14 checks, quiz 3/3 |
| l14-semicircle | ok, 14 checks, quiz 3/3 (replayed after the last edit: ok) | ok, 14 checks, quiz 3/3 (replayed: ok) |
| l15-exceeding-one | ok, 14 checks (code run in Pyodide), quiz 3/3 | ok, 14 checks, quiz 3/3 |
| l16-meeting | ok, 13 checks, quiz 3/3 | ok, 13 checks, quiz 3/3 |
| l17-buffon | ok, 14 checks (code run in Pyodide), quiz 3/3 | ok, 14 checks, quiz 3/3 |
| l18-expected-distance | ok, 15 checks (code run in Pyodide), quiz 3/3 | ok, 15 checks, quiz 3/3 |
| review-3 (`--set`) | ok, recorded 10 of 10 | (run with `--mobile --why`) |
| homework-3 (`--set`) | ok, marked 9 of 9 right, 43 of 43 marks (both code items run in Pyodide) | (run with `--mobile --why`) |

Screenshots (1280 px with `--why`, and 390 px) are in the scratchpad `puzzles-3/shots`, `puzzles-3/shots2`, `puzzles-3/shots3` and `puzzles-3/shots-sets`. Faults found and fixed from them: neutral triangles and the axis titles overlapping on the unit square (ranges widened to 1.1 in l13, l15); a KaTeX function label drawn large over the axis (l15, removed; the prose names the line); the `series` explanation showing only the first 10% of the run (explain patch now reveals it all); the l17 `pair` drawn side by side with 7 px text on the right (now `stack: true`, prose says "the lower chart"); a semicircle shaded when no semicircle holds the points (l14, a derive now hides it); `contour` lines running past the square in l18 (ranges back to [0, 1]); the title-screen canvas in l13, which the player does not draw (removed; backlog bullet).

The starters of the five code widgets return `None` (or raise nothing), so they fail their tests; the solutions pass (checked by the playthrough in Pyodide).

## Numbers

Every number was computed exactly (closed forms, Python `fractions`) and by seeded simulation: NumPy `default_rng(20261102)`, 2,000,000 trials unless stated (`puzzles-3/check.py`, output `check.out`), and pure Python `random.Random(2026)` for the extra quiz checks (`check2.py`). Every simulated value is within 3 standard errors of the exact one (the largest gap, z = −2.88 for the length-2 needle's crossings, was rerun with three more seeds of 4,000,000: 1.27342, 1.27338, 1.27354 against 1.27324, all within 1 se). Code-test values are from `codes.py` (CPython; Pyodide uses the same Mersenne Twister).

| Where | Quantity | Exact | Decimal | Simulation (se) |
|---|---|---|---|---|
| l13 | triangle from two uniform breaks | 1/4 | 0.25 | 0.25008 (0.00031) |
| l13 | break the longer piece | 2 ln 2 − 1 | 0.3863 | 0.38627 (0.00034) |
| l13 | coin picks the piece | ln 2 − 1/2 | 0.1931 | 0.19305 (0.00028) |
| l13 drill | E longest; E shortest; middle piece longest | 11/18; 1/9; 1/3 | 0.6111; 0.1111; 0.3333 | 0.61112 (0.0001); 0.11112 (0.00006); 0.33367 (0.00033) |
| l13 follow-up | four pieces form a quadrilateral, 1 − 4/8 | 1/2 | 0.5 | 0.50025 (0.00035) |
| l13 transfer | some desk over £6m of £9m, 3(1/3)²; E largest share × £9m | 1/3; 11/2 | 0.3333; £5.5m | 0.33353 (0.00033) |
| l13 quiz | all pieces over 1/4; some piece over 1/2; always break the shorter | 1/16; 3/4; 0 | 0.0625; 0.75; 0 | 0.06259; 0.74992; 0 of 100,000 (Python) |
| l14 | 2, 3, 4, 5, 6, 7 points in a semicircle, n/2^{n−1} | 1, 3/4, 1/2, 5/16, 3/16, 7/64 | | 1, 0.74976, 0.49974, 0.31206, 0.18731, 0.10954 (se 0.0002 to 0.00035) |
| l14 | B and C in the half starting at A | 1/4 | 0.25 | 0.24968 |
| l14 | triangle holds the centre (= acute); obtuse | 1/4; 3/4 | | 0.25053; 0.74947 (angles from dot products); 0.24964 (Python) |
| l14 drill | quadrilateral holds the centre | 1/2 | | 0.49956 |
| l14 follow-up | tetrahedron holds the centre; four points in a hemisphere (Wendel 7/8) | 1/8; 7/8 | 0.125; 0.875 | 0.12410 (0.00052), 400,000 trials by barycentric solve |
| l14 transfer | some 12-hour window holds three trades; fixed halves | 3/4; 1/4 | | 0.24991 for the fixed halves |
| l14 quiz | six points; three in the top half | 3/16; 1/8 | 0.1875; 0.125 | 0.18731; 0.12481 |
| l15 | P(U₁ + U₂ ≤ 1); three draws; P(N > 4); P(N > 5) | 1/2; 1/6; 1/24; 1/120 | 0.5; 0.1667; 0.0417; 0.0083 | 0.50008; 0.16668; 0.04153; 0.00832 |
| l15 | E[N] | e | 2.7183 | 2.71820 (0.00062) |
| l15 generalise | to pass 1/2 | e^{1/2} | 1.6487 | 1.64843 (0.00054) |
| l15 drill | P(N = 2); P(N = 3); Var(N) = 3e − e² (E[N²] = Σ(2n + 1)/n! = 3e, summed) | 1/2; 1/3; 3e − e² | 0.5; 0.3333; 0.7658 | 0.49992; 0.33339; 0.76498; 3 × 2.718282 − 7.389056 = 0.765790 |
| l15 follow-up | E[S_N] (Wald) | e/2 | 1.3591 | 1.35909 (0.00017) |
| l15 transfer | fills uniform on 0 to 12,500, order 10,000: t = 0.8 | e^{0.8} | 2.2255 | 2.22578 (0.00065) |
| l15 quiz | P(U₁ + U₂ ≤ 1/2) | 1/8 | 0.125 | 0.12558 (Python) |
| l15 code | `exceed_one_sim(20000, 1)`, `(20000, 2)`, `(50000, 3)` | e | | 2.71575, 2.72095, 2.72072; bands 0.0186, 0.0186, 0.0118 (3 se, sd 0.8751) |
| l16 | 15-minute waits; 10-minute | 7/16; 11/36 | 0.4375; 0.3056 | 0.43748; 0.30566 |
| l16 | A waits 10, B 20: 1 − (50² + 40²)/7200 | 31/72 | 0.4306 | 0.43065 |
| l16 generalise | one waits the hour, one not at all | 1/2 | | 0.49983 |
| l16 drill | three people 15 min, 3a² − 2a³ at a = 1/4; trains 10 min; 20-minute waits | 5/32; 11/36; 5/9 | 0.15625; 0.3056; 0.5556 | 0.15639; 0.30566; 0.55562 |
| l16 follow-up | 15 minutes in two hours | 15/64 | 0.2344 | 0.23446 |
| l16 transfer | 6 minutes in 30 | 9/25 | 0.36 | 0.36001 |
| l16 quiz | 30-minute waits; A waits 15, B none; 15 in 45 minutes | 3/4; 7/32; 5/9 | 0.75; 0.2188; 0.5556 | 0.75029; 0.21852; 0.55562 |
| l17 | unit needle, gap 1; length 1/2 | 2/π; 1/π | 0.6366; 0.3183 | 0.63693 (0.00034); 0.31804 (0.00033) |
| l17 | π from 6,366 of 10,000 | 20000/6366 | 3.1417 | arithmetic, twice |
| l17 drill | length 1/3; crossings of length 2; square grid, (4l − l²)/π | 2/(3π); 4/π; 3/π | 0.2122; 1.2732; 0.9549 | 0.21176 (0.00029); 1.27176 (0.00051), rerun 1.27342; 0.95489 (0.00015) |
| l17 follow-up | circle of diameter 1, 2L/(πd) with L = π | 2 | | every drop meets one line in two points |
| l17 transfer | se of π̂ at 10,000; at 1,000,000 | | 0.0237; 0.0024 | π√(p(1 − p)/n)/p with p = 2/π |
| l17 quiz | gap 2; crossings of length 3 | 1/π; 6/π | 0.3183; 1.9099 | 0.31851; 1.90912 |
| l17 code | `buffon_estimate(100000, 1, 1, 1)`, `(…, 0.5, 1, 2)`, `(…, 1, 2, 3)`, `(…, 0.6, 1, 6)` | π | | 3.13991, 3.15776, 3.13440, 3.14845; bands 0.0225, 0.0436, 0.0436, 0.0379 (3 se) |
| l18 | E\|X − Y\|; P(\|X − Y\| > 1/2) | 1/3; 1/4 | | 0.33335; 0.25029 |
| l18 | from an end; from the midpoint | 1/2; 1/4 | | 0.49997; 0.25010 |
| l18 | to the centre of the square (stated) | (√2 + ln(1 + √2))/6 | 0.3826 | 0.38264 (0.0001) |
| l18 | two points in the square (stated); × 10 | (2 + √2 + 5 ln(1 + √2))/15 | 0.5214; 5.2141 | 0.52141 (0.00018) |
| l18 derive | E\|X − y\| = (y² + (1 − y)²)/2 at y = 0.2, 0.5, 0.9 | 0.34, 0.25, 0.41 | | 0.34036, 0.25005, 0.41034 (Python) |
| l18 drill | E(X − Y)²; on [0, 10]; chord on the unit circle | 1/6; 10/3; 4/π | 0.1667; 3.3333; 1.2732 | 0.16670; 3.33349; 1.27329 |
| l18 follow-up | range of 3 (and 4, 5) uniforms, (n − 1)/(n + 1) | 1/2 (3/5, 2/3) | | 0.50023 (0.60006, 0.66660) |
| l18 transfer | \|fill − £100\|, fill uniform on £99.90 to £100.10 | 1/20 | £0.05 | 0.049995 |
| l18 quiz | on [0, 6]; doubling the side | 2; × 2 | 1.0428 for side 2 | 2.0001 |
| l18 code | `mean_distance_sim(1, 20000, 1)`, `(2, 20000, 2)`, `(3, 20000, 3)`; cube value is Robbins' constant 0.661707 | 1/3, 0.521405, 0.661707 | | 0.33525, 0.51957, 0.66068; bands 0.0050, 0.0053, 0.0053; cube by NumPy 0.66193 (0.00018) |
| review | pieces over 1/5; middle piece; seven points; first n below 1%; P(N = 4); 6-minute waits; waits 5 and 25 (1 − (55² + 35²)/7200); needle 0.8; π from 4,780 of 10,000 at l = 3/4; range of four | 4/25; 1/3; 7/64; 12; 1/8; 19/100; 59/144; 1.6/π; 15000/4780; 3/5 | 0.16; 0.3333; 0.1094; 11/1024 = 0.0107, 12/2048 = 0.0059; 0.125; 0.19; 0.4097; 0.5093; 3.1381; 0.6 | 0.15976; 0.33334; 0.10954; exact table; 0.12515; 0.19020; 0.41002; 0.50968; expected 4,774.6 crossings; 0.60006 |
| homework code | `stick_triangle` on seeds 1, 2, 3 (40,000); `semicircle_sim(3, 20000, 1)`, `(5, 20000, 3)`; `semicircle_prob(10)` | 1/4, 2 ln 2 − 1, ln 2 − 1/2; 3/4, 5/16; 5/256 | | 0.25260, 0.38740, 0.19273 (bands 0.0065, 0.0073, 0.0059); 0.74785, 0.31255 (bands 0.0092, 0.0098) |
| homework | five pieces form a pentagon; three people 10 min (a = 1/6); uniforms to pass 2, Σ(2ⁿ − n)/n!; unit needle on a square grid of gap 2, (4ld − l²)/(πd²); squared distance in the square | 11/16; 2/27; e² − e; 7/(4π); 1/3 | 0.6875; 0.0741; 4.6708; 0.5570; 0.3333 | 0.68755; 0.07420; 4.67095 (0.00088); 0.55717; 0.33328 |
| homework longform | the model's two procedures | 1/4, 2 ln 2 − 1, ln 2 − 1/2 | 0.25, 0.386, 0.193 | as l13 |

Wrong-answer values in `wrong[]` were computed the same way (for example 0.6137 = 2 − 2 ln 2, 0.4219 = (3/4)³, 0.2917 = 7/16 × 2/3, 0.0934 = (11/36)², 5.4366 = 2e, 2.6667 = 1 + 1 + 1/2 + 1/6, 4.1841 = 20000/4780, 2.0921 = 10000/4780).

## Seeds and conventions

- Canvas pictures use the engine's own seeded streams (`series` sims seeds 7, 11, 12; `bars` seed 17); no answer is read from a canvas simulation. The Buffon `bars` sim draws its angle from a uniform point in the quarter disc (rejection via `filter`), so no π goes in; the caption explains the discards.
- Code tests use pure Python `random.Random(seed)`; simulated tests accept three standard errors of the exact value, stated in each `how`; the model solutions sit within about one standard error on the test seeds.
- Answers to four decimal places with `tol` 0.0005; counts with `tol` 0; money in £.
- The two closed forms in l18 (the centre of the square, two points in the square) and Robbins' constant for the cube are stated and checked by simulation, not derived, as the brief says.

## Proposed change to course.json

None.

## Backlog

Seven bullets appended to `docs/BACKLOG-INBOX.md` under "Raised later (puzzles level 3):" (sim outcomes without trigonometry, the discarded count, no first-passage loop in sims, the one-point `circle`, the ignored title canvas, side-by-side plane pairs, unclipped contours).
