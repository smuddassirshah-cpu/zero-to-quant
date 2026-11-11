# Problem sets: number-sense (brief `docs/briefs/chained.md`)

File: `app/content/courses/number-sense/problems-4.json` (level 4 only; levels 1 to 3 have no set yet). Numbers: `docs/reports/problems-number-sense-numbers.py` (exits 0, 275 checks).

## Set

| set | item | parts (typed / choice) | lessons drawn on | difficulty |
|---|---|---|---|---|
| problems-4 | p-hall-tiles | 4 (4 / 0) | l15, l16, l17, l18 | 5 |
| problems-4 | p-lawn-pond | 3 (3 / 0) | l17, l18 | 3 |
| problems-4 | p-cycle-commute | 5 (4 / 1) | l18, l19 | 4 |
| problems-4 | p-meshing-gears | 4 (4 / 0) | l16, l18 | 4 |

Typed parts: 15 of 16. Every lesson appears in at least one problem and every problem draws on at least two. The one choice part is a judgement: whether the mean or the median describes a usual ride when one day is extreme.

Hall tiles: the largest tile side from the shared primes of 432 and 540 (108 cm), the number of tile sides that fit as the factor count of $108 = 2^2 \times 3^3$ (12), the tiles needed (20), then the floor area in m² (23.328, checked against $4.32 \times 5.4$). Lawn and pond: the pond's area to 2 dp, the grass left, then the boxes of seed (rounded up). Cycle commute: mean and median of five times with a puncture day, the judgement, the speed from the median, then metres a second. Meshing gears: the LCM of 48 and 18 teeth, the small gear's turns between meetings, meetings a minute, then a tooth tip's distance in a minute to the nearest metre.

Each later part restates the value it uses ("Using tiles of side 108 cm", "Using a pond area of 28.27 m²", "Using her median time of 27 minutes", "Using 240 turns a minute"), and carries a `wrong` for the answer that follows from the commonest slip before it: 40 sides from the LCM 2,160; 320 tiles from 27 cm tiles; 89.15 m² and 5 boxes from the circumference; 16.875 km an hour from the mean; 48 turns from 864 teeth; 80 meetings from the large gear.

## Checks

| check | result |
|---|---|
| numbers script | 275 checks, 0 failures: two methods for every part (sympy against listing, a tile or tooth count, sorting, or floats); every key, rounding, printed figure, `accept` line and `wrong` band; the values from $\pi \approx 3.14$ and $\tfrac{22}{7}$ accepted on both $\pi$ parts and still matched by each $\pi$ slip; `check_wrongs` clean. Its 18 "check by hand" lines are byKey lines that explain a slip by its cause: read, all right |
| validator | 0 errors; no warning on the file (4,664 in all, as before; no `[tight-band]`, `[wide-wrong-band]`, `[answer-form]` or long sentence) |
| playthrough `--local-cdn` | green (16 parts) |
| playthrough `--mobile` | green; 440 px shots of every part (`--shots`) read, no fault |
| voice scan 35 (course folder) | 0 and 0 |

## Review-4 faults avoided

- Every $\pi$ answer takes the 3.14 and $\tfrac{22}{7}$ values (pond area band 0.02 on 28.2743; grass band 0.02; the gear distance asks for the nearest metre), and the slips' bands take them too.
- No per cent, no algebra, no rule not taught: the factor count, the HCF from shared primes, the LCM, $\pi r^2$, unit fractions worth 1, the median of an odd list.
- Every slip's byKey line names what the learner did with this item's numbers.

## Fresh-check

`node tools/fresh-check.mjs --file content/courses/number-sense/problems-4.json`: 0 hits at the gate and 0 at `--min-run 8 --min-share 0`. Two advisory lines, both judged acceptable: the formula $2^2 \times 3^3$ also appears in l15 quiz `q-72` (as an option for 72; here it is 108, a different number); 31, 27 and 28 also occur in `mock-oa-trader` (chance: there a timetable, here ride times).

Read by hand against the course's lessons, quizzes, reviews and homework: they use a trading desk, data feeds, bonds, a fence pen, a pond 10 m across, a flower bed, a train and a car. This set uses a hall floor, a lawn with a 6 m pond, a cycle commute and two gears. Shapes that recur, judged acceptable: a circular pond (l18's trap has one 10 m across for the radius slip; here 6 m inside a lawn, with the grass left and the seed); km an hour to metres a second (l18 s5 and quiz with 72 and 90; here 20, from a computed speed).

## Engine limits

None new for the problem set. The Fluency limits are in the fluency report.
