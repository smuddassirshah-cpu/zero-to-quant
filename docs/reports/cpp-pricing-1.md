# cpp-pricing level 1 ("Numbers in C++"): report

## Files written

All in `app/content/courses/cpp-pricing/`:

- `l1-doubles.json`: 11 screens, 4 quiz items, skills `cx-numeric` and `cx-testing`.
- `l2-cmath.json`: 10 screens, 4 quiz items, skill `cx-numeric`.
- `l3-random-done-right.json`: 11 screens, 4 quiz items, skills `cx-numeric` and `cx-testing`.
- `l4-normal-cdf.json`: 11 screens, 4 quiz items, skills `cx-numeric` and `cx-testing`.
- `review-1.json`: 8 items, difficulty 2 to 4, covering all four lessons; one is a C++ `forward()` code item.
- `homework-1.json`: 8 items, difficulty 3 to 5.
  - Code: a difficulty-5 Black-Scholes script (reads S, K, r, σ, T from stdin; prints d1, d2, N(d1), N(d2); a tail test catches the erf form; it must exit non-zero when σ ≤ 0 or T ≤ 0), `mc_mean_se` (seeded mean and standard error), and `small_root` (the quadratic's bad root).
  - One `order` item: the steps from a seed to a repeatable published price.
  - One difficulty-5 `longform` review of a colleague's pricer (`1 / 2`, erf in the tails, reseeding in the loop, a hidden seed, a `==` test), with a 10-point rubric and a full model answer.
  - Three short items: the gap between doubles, a stop probability, and a NaN payoff.

The lesson ids, names, objectives and skills follow `course.json` exactly. Money is in £, and every `how` warns about the first compiler load.

## Validator

`node app/tools/validate.mjs`: 0 errors, 193 warnings, none in my files. The warnings come from other courses, and from cpp-pricing level 2 and 3 files that other agents are writing in the same folder.

## Playthrough

Run with `--local-cdn …/scratchpad/pkgs`. Every check passed and there were no console errors.

- l1-doubles: 15 checks, quiz 4/4.
- l2-cmath: 14 checks, quiz 4/4.
- l3-random-done-right: 15 checks, quiz 4/4.
- l4-normal-cdf: 14 checks, quiz 4/4.
- review-1: 8 of 8.
- homework-1: 8 of 8, 36 of 36 marks.

The screenshots showed four problems, all fixed:

- A clipped number-line label in l1.
- The l4 explore, where the shaded area did not follow the slider (the derive target is now `area.to`).
- Wrapped table cells in l1.
- Over-long code lines in the longform item.

## How the C++ cases were checked

Every expected value comes from the app's runtime, through a Node copy of the worker. Every solution passes all its cases, and every starter fails at least one.

The typical wrong versions fail where the feedback says they will:

- The erf-form `norm_cdf` fails at Φ(−5) (off by 3.9e-11, relative) and at Φ(−10) (it returns 0).
- Leaving out the √2 fails at Φ(1).

Values were cross-checked in Python (`math.erfc`, scipy, mpmath, NumPy) and against g++ with libstdc++.

## Proposed change to course.json

None.

## Runtime facts verified (clang 21, libc++)

- **`std::mt19937`.** The 10,000th output of a default-seeded engine is 4123659995. With seed 42 the first raw outputs are 1608637542, 3421126067 and 4083286876.
- **libc++ normal draws, seed 42.** The first six are 0.51543306969120128, −0.55023449442049355, 1.368450122216075, 0.47386085566622227, −0.12414717496435412 and −0.91682687324868972.
- **Seed-42 statistics.** 10,000 draws have mean 0.007305 and sd 1.004522.
- **libstdc++ (g++).** It makes the same pairs as libc++ but hands them out in the other order: −0.5502, 0.5154, 0.4739, 1.3685, and so on. `uniform_real_distribution` is swapped the same way (libc++ 0.7965…, libstdc++ 0.1834…).
- **NumPy.** It gives different numbers again: `default_rng(42)` gives 0.3047, −1.0400, 0.7505, and the legacy `seed(42)` gives 0.4967, −0.1383, 0.6477. l3 teaches this with a table.
- **Functions that work.** `std::chrono::steady_clock`, `std::erfc`, `std::erf`, `std::lgamma`, `std::isnan`, `std::nextafter`, `std::numeric_limits<double>::epsilon()`, `std::random_device`, `std::cbrt` and `std::copysign`. Nothing I needed failed.
- **Output of special values.** `std::cout` prints NaN as `-nan` and `std::log(0.0)` as `-inf`.
- **`RAND_MAX`.** It is 2147483647. The `rand() % 100` bias screen uses the Windows value, 32,767, and says so.
- **`erfc` accuracy.** The runtime's `erfc` matches Python's `math.erfc` to the last digit at every point tested.

## Engine and runtime limitations

These are also posted to `docs/BACKLOG-INBOX.md`.

1. **Braced lists in a range-for.** `for (double x : {…})` does not compile in libc++ unless `<initializer_list>` is included, directly or through another header. My tests avoid it.
2. **`isclose` cannot test tiny values.** The code widget's `isclose` passes any two numbers within 1e-12 of each other. To test norm_cdf tails to 12 digits relative, I wrote `f(x) / exact - 1` with expect 0, and I scaled other tiny results up first. A per-case relative or absolute tolerance would be cleaner.
3. **`fmtNum` rounds tiny numeric answers.** In `grade.js`, `fmtNum` rounds the test hook's and Show solution's numeric answer to 6 decimal places. An answer of 9.5e-7 is filled in as 0.000001 and fails its own tolerance. I reframed both tiny answers in units: "units of 10⁻¹⁶" and "millionths of a pound".
4. **A plane `area` cannot be a derive target by its id.** `A.to` does nothing; only `area.to` works.
5. **The `bars` sim uses the JavaScript generator.** It cannot show libc++ draws live. I precomputed real libc++ histograms for n = 10, 100, 1,000 and 10,000 and switched between them with a derive on a log-scale control.
