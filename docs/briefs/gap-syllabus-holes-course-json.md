# Syllabus holes (PLAN 2d): `course.json` edits and the figures that move

For the main session. Four new levels, 22 new lessons, no lesson id renamed or removed. The level briefs are `docs/briefs/gap-number-sense.md`, `gap-quadratics.md`, `gap-testing.md` and `gap-stat-learning.md`. The planner applied exactly the JSON below in a scratch state of its worktree, ran the tools, recorded the figures and reverted; nothing but the five brief files is committed.

Result of that trial: `node tools/validate.mjs` 0 errors (warnings up by 5: four "not yet written" lines, one for each course, and one "`number-sense/L4` has no written lesson yet" on the quadratics edge); no cycle; `Requires: 266 cross-course edges, 0 without why`.

## Rulings wanted

1. **Skills.** The validator allows 3 to 6 skills per course and errors on any topic skill the topic exam does not cover (`topic skill "x" is not covered by the exam`). A first trial with new skills gave 16 errors. So the JSON below adds **no skill**, and the briefs map every new lesson to existing skills. The fit is poor in places (Fisher information under `ht-setup`, clustering under `sl-setup`). Option B, if you want honest labels: when each topic exam is extended, add the skills listed per course below **in the same commit as one exam item per new skill**, and re-tag the new lessons' `skills` arrays then (lesson ids do not change). The briefs already tell the author which skill to use in either case.
2. **Home of the 1.6 level: `testing` level 4**, not `estimation` level 4 (reasons in `gap-testing.md`: the last two lessons need `testing/L2`, and `testing/L1` already requires `estimation/L3`). It requires `testing/L2`, not `L3`: multiple testing is not used.
3. **Surds are l14 of `quadratics` level 4**, not in `number-sense` level 4. No lesson of topic 0.1 or 0.2 teaches them today.
4. **`quadratics/L4` gates on the new `number-sense/L4`** (prime factors for surds, the HCF for cancelling). Until number-sense level 4 is written, quadratics level 4 shows "Route limited". Author number-sense level 4 first, or in the same wave and merge it first. If you would rather not gate, make that entry `"gate": false`.
5. **Two diagnostic edges** (`"gate": false`): `testing/L4` to `random-vars/L5` (the multinomial and Cauchy–Schwarz by name) and `stat-learning/L4` to `multivar/L2` (one gradient step). Gating the second would pull eight multivariable lessons into the closure of a level ISLP teaches without them.
6. **Exam caps.** `topic-2.1` already holds 30 items, the validator's maximum, so its extension must replace items. `topic-0.1` holds 23, `topic-0.2` 27, `topic-1.6` 27.
7. **A drift found on the way** (not caused by this work): `node tools/curriculum-hours.mjs --check` fails today with 21 prose mismatches in `docs/curriculum.md` (the opening says 625 h in the app and 3,111 h outside; the source gives 667 and 3,069; stages 0 and 1 likewise). Record it in `KNOWN_ISSUES.md` or fix the prose when the block is regenerated below.

## 1. `app/content/courses/number-sense/course.json`

Append to `levels` (after level 3):

```json
    {
      "n": 4,
      "name": "Factors, measures and averages",
      "lessons": [
        "l15-building-blocks",
        "l16-shared-factors",
        "l17-around-and-inside",
        "l18-circles-and-units",
        "l19-one-number-for-many"
      ],
      "review": "review-4",
      "homework": "homework-4"
    }
```

No `requires`: the level implicitly requires `number-sense/L3`, and uses nothing outside the course (no algebra, no percentages).

Add to `lessonNames`:

```json
    "l15-building-blocks": "The building blocks of a number",
    "l16-shared-factors": "Shared factors and shared multiples",
    "l17-around-and-inside": "Around a shape and inside it",
    "l18-circles-and-units": "Round shapes and changing units",
    "l19-one-number-for-many": "One number for many"
```

Add to `lessonObjectives`:

```json
    "l15-building-blocks": "Find the factors and multiples of a number, recognise primes, and write a number as a product of primes.",
    "l16-shared-factors": "Find the highest common factor and lowest common multiple of two numbers from their prime factors.",
    "l17-around-and-inside": "Find the perimeter and area of rectangles, triangles, parallelograms and shapes built from them.",
    "l18-circles-and-units": "Find the circumference and area of a circle, and convert between units of length, area and time.",
    "l19-one-number-for-many": "Find the mean, median, mode and range of a data set, and read them from a table or a chart."
```

Suggested `description` (course.json and the `courses` entry of `curriculum.json`): "Work with fractions, decimals, negatives and powers until each one feels like an amount, then with factors, measures and averages." Option B skill (one, making six): `"ns-measures": "Measures and averages"` for l17 to l19.

## 2. `app/content/courses/quadratics/course.json`

Append to `levels` (after level 3):

```json
    {
      "n": 4,
      "name": "Algebraic fractions and polynomials",
      "lessons": [
        "l14-roots-that-stay",
        "l15-fractions-with-letters",
        "l16-adding-and-solving",
        "l17-dividing-polynomials",
        "l18-circles-on-a-grid",
        "l19-line-meets-curve"
      ],
      "review": "review-4",
      "homework": "homework-4",
      "requires": [
        "quadratics/L3",
        { "ref": "equations/L4", "why": "Substitutes a line into a curve, as simultaneous equations with one linear and one quadratic do." },
        { "ref": "number-sense/L4", "why": "Uses prime factors and highest common factors to simplify surds and cancel fractions." }
      ]
    }
```

`functions/L2` (gradients, perpendicular lines) and `functions/L3` are already in the closure through `quadratics/L3`, so they are not listed. `functions/L4` is not required and the brief does not lean on it.

Add to `lessonNames`:

```json
    "l14-roots-that-stay": "Roots that stay as roots",
    "l15-fractions-with-letters": "Fractions with letters in them",
    "l16-adding-and-solving": "Adding fractions and solving with them",
    "l17-dividing-polynomials": "Dividing polynomials",
    "l18-circles-on-a-grid": "Circles on a grid",
    "l19-line-meets-curve": "Where a line meets a curve"
```

Add to `lessonObjectives`:

```json
    "l14-roots-that-stay": "Simplify surds, add and multiply them, and rationalise a denominator.",
    "l15-fractions-with-letters": "Simplify, multiply and divide algebraic fractions by factorising and cancelling common factors.",
    "l16-adding-and-solving": "Add and subtract algebraic fractions over a common denominator, and solve equations that contain them.",
    "l17-dividing-polynomials": "Divide a polynomial by a linear factor, and use the factor theorem to factorise a cubic.",
    "l18-circles-on-a-grid": "Find the distance between two points, and write and read the equation of a circle.",
    "l19-line-meets-curve": "Find where a line meets a parabola or a circle, and use the discriminant to tell crossing from touching from missing."
```

Suggested `description`: "Factorise, solve and sketch quadratics, find the price that maximises revenue, then work with surds, algebraic fractions, cubics and circles." Option B skill (one, making six): `"quad-rational": "Surds, algebraic fractions and polynomials"` for l14 to l17.

## 3. `app/content/courses/testing/course.json`

Append to `levels` (after level 3):

```json
    {
      "n": 4,
      "name": "Theory of estimation and tests",
      "lessons": [
        "l13-matching-moments",
        "l14-what-data-can-forget",
        "l15-sharpness-of-the-peak",
        "l16-best-possible-precision",
        "l17-ratio-of-likelihoods",
        "l18-counts-against-expectations"
      ],
      "review": "review-4",
      "homework": "homework-4",
      "requires": [
        "testing/L2",
        { "ref": "limits-thm/L4", "why": "Uses the chi-square, Gamma and t distributions and joint densities for information and test statistics." },
        { "ref": "random-vars/L5", "why": "The multinomial and Cauchy-Schwarz appear in two derivations; a quick check helps.", "gate": false }
      ]
    }
```

Add to `lessonNames`:

```json
    "l13-matching-moments": "Matching moments",
    "l14-what-data-can-forget": "What the data can forget",
    "l15-sharpness-of-the-peak": "How sharp is the peak?",
    "l16-best-possible-precision": "The best possible precision",
    "l17-ratio-of-likelihoods": "A ratio of likelihoods",
    "l18-counts-against-expectations": "Counts against expectations"
```

Add to `lessonObjectives`:

```json
    "l13-matching-moments": "Estimate parameters by the method of moments and compare the result with maximum likelihood.",
    "l14-what-data-can-forget": "Recognise a sufficient statistic with the factorisation theorem, and improve an estimator by conditioning on it.",
    "l15-sharpness-of-the-peak": "Compute the Fisher information of a model and use it for the standard error of a maximum likelihood estimate.",
    "l16-best-possible-precision": "Derive the Cramér-Rao bound and decide whether an unbiased estimator attains it.",
    "l17-ratio-of-likelihoods": "Build the most powerful test of two simple hypotheses, and use the chi-squared limit for a likelihood-ratio test.",
    "l18-counts-against-expectations": "Run chi-squared tests of goodness of fit and of independence, with the right degrees of freedom."
```

"Derive" and "Build" are deliberate: a Stage 1 level whose lesson objectives start with those verbs is rule-matched, and the brief specifies its performance task (a blank-page derivation in `homework-4.json`, report `docs/reports/testing-4-perf.md`). Option B skills (two, making six): `"ht-theory": "Estimation theory"` for l13 to l16 and `"ht-likelihood": "Likelihood-ratio and chi-squared tests"` for l17 and l18. Suggested `description` addition: "... then the theory behind estimators and tests: moments, sufficiency, information, likelihood ratios and chi-squared tests."

## 4. `app/content/courses/stat-learning/course.json`

Append to `levels` (after level 3):

```json
    {
      "n": 4,
      "name": "Other learners",
      "lessons": [
        "l15-widest-street",
        "l16-groups-nobody-labelled",
        "l17-a-small-network",
        "l18-bending-the-line",
        "l19-which-learner"
      ],
      "review": "review-4",
      "homework": "homework-4",
      "requires": [
        "stat-learning/L3",
        { "ref": "multivar/L2", "why": "One gradient step on a network uses partial derivatives and gradient descent; a quick check helps.", "gate": false }
      ]
    }
```

Add to `lessonNames`:

```json
    "l15-widest-street": "The widest street",
    "l16-groups-nobody-labelled": "Groups nobody labelled",
    "l17-a-small-network": "A small neural network",
    "l18-bending-the-line": "Bending the line",
    "l19-which-learner": "Which learner, when?"
```

Add to `lessonObjectives`:

```json
    "l15-widest-street": "Fit a support vector machine, read its margin and support vectors, and bend the boundary with a kernel.",
    "l16-groups-nobody-labelled": "Cluster data with $k$-means and with hierarchical clustering, and choose the number of groups.",
    "l17-a-small-network": "Build a network with one hidden layer, follow one gradient step, and fit one with scikit-learn.",
    "l18-bending-the-line": "Fit splines and an additive model, and choose the number of knots on held-out data.",
    "l19-which-learner": "Compare learners on one table of test scores, and choose one from the shape, size and noise of the data."
```

"Build" in l17 makes this Stage 2 level rule-matched; the brief specifies a `code` performance task (k-means from a stub; report `docs/reports/stat-learning-4-perf.md`). Option B skill (one, making six): `"sl-flexible": "Margins, clusters, networks and splines"` for l15 to l18.

## Hours

Stored topic hours live in `curriculum.json` and do not move unless you change them: 0.1 stays 60, 0.2 180, 1.6 120, 2.1 200, and the stage and full-path totals stay 555, 1,650, 940 and 3,695. The planner recommends leaving them: each topic's outside-study allowance already covers this material in its named course (Khan, DeGroot and Schervish, ISLP), and the new lessons move hours from "outside" to "in the app".

In-app minutes each level adds while unwritten (14 a lesson, 20 for the review, 45 for the homework; the authored minutes replace the 14s later): number-sense 5 × 14 + 65 = 135 min (2.25 h); quadratics 6 × 14 + 65 = 149 min (2.48 h); testing 149 min (2.48 h); stat-learning 135 min (2.25 h). Total 568 min, 9.5 h.

## Derived figures that move (before, then after the four `course.json` edits, before any lesson is written)

Census (`node app/tools/census.mjs`):

| Line | Before | After |
| --- | --- | --- |
| number-sense | 14/14, L 3/3 | 14/19, L 3/4, rev 3/4, hw 3/4 |
| quadratics | 13/13, L 3/3 | 13/19, L 3/4, rev 3/4, hw 3/4 |
| testing | 12/12, L 3/3 | 12/18, L 3/4, rev 3/4, hw 3/4 |
| stat-learning | 14/14, L 3/3 | 14/19, L 3/4, rev 3/4, hw 3/4 |
| Stage 0 lessons | 193/193 | 193/204 (missing 11) |
| Stage 1 lessons | 560/560 | 560/566 (missing 6) |
| Stage 2 lessons | 202/202 | 202/207 (missing 5) |
| Total lessons | 1214/1214 | 1214/1236 (missing 22) |
| Levels fully written | 279/279 | 279/283 |
| Cross-course requires edges | 261 | 266 (0 without why) |
| Reviews, homework | 279/279 each | 279/283 each |

When all four levels are written the census should read 1236/1236, levels 283/283, reviews and homework 283/283, review items 2519 plus the four new reviews' items; fluency sets (83), problem sets (62), exams (49) and drills (210) do not move in this pass.

`node tools/curriculum-hours.mjs` (run with `--write` to regenerate the block in `docs/curriculum.md`):

| Row | In the app | Outside study | Lessons mapped |
| --- | --- | --- | --- |
| 0.1 Number | 13 to 15 | 47 to 45 | 27 to 32 |
| 0.2 Algebra | 30 to 33 | 150 to 147 | 48 to 54 |
| 1.6 Statistics | 19 to 21 | 101 to 99 | 36 to 42 |
| 2.1 Machine learning | 27 to 29 | 173 to 171 | 50 to 55 |
| Stage 0 | 111 to 116 | 444 to 439 | quant path 104 to 108 in the app, 411 to 407 outside |
| Stage 1 | 314 to 317 | 1,336 to 1,333 | quant path 285 to 288, 1,201 to 1,199 |
| Stage 2 | 111 to 114 | 829 to 826 | quant path 111 to 114, 829 to 826 |
| All stages | 667 to 678 | 3,069 to 3,058 | quant path 614 to 624, 2,901 to 2,892; still 57 months |

The stage headings and the opening paragraph of `docs/curriculum.md` quote these totals in prose and need the same figures (see ruling 7). Its section 0.1, 0.2, 1.6 and 2.1 `Cover` lines, the stage 0 table rows, and the `cover` strings of `curriculum.json` should each gain the new material: 0.1 "factors and primes, measures, averages"; 0.2 "surds, algebraic fractions, polynomial division, circles"; 1.6 "method of moments, sufficiency, Fisher information, likelihood-ratio and chi-squared tests"; 2.1 "support vector machines, clustering, a small neural network, splines".

`node tools/readiness-sums.mjs` (it fails with "out of date" until run with `--write`, which rewrites `app/content/readiness.json` and the generated blocks of `docs/readiness.md`). Header totals per role, lessons then stored hours then in-app and outside hours:

| Role | Lessons | Unwritten | Hours | In the app | Outside |
| --- | --- | --- | --- | --- | --- |
| trader | 630 to 647 | 0 to 17 | 1,804 to 1,803 | 356 to 362 | 1,448 to 1,442 |
| researcher | 874 to 896 | 0 to 22 | unchanged | 489 to 499 | 2,271 to 2,261 |
| developer | 476 to 487 | 0 to 11 | 1,516 to 1,515 | 267 to 271 | 1,249 to 1,245 |
| strats | 792 to 814 | 0 to 22 | 2,278 to 2,286 | 443 to 453 | 1,843 to 1,842 |
| strats-deriv | 874 to 896 | 0 to 22 | 2,397 to 2,405 | 488 to 498 | unchanged |
| undecided | 252 to 263 | 0 to 11 | 719 to 718 | 150 to 154 | 569 to 564 |

The required and recommended rows inside each role move too (for example trader required 442 to 453 lessons, recommended 188 to 194); a role's stored hours shift by a few hours because a topic's hours are shared across its courses by lesson count, and these four courses now hold a larger share of their topics. `hoursUnwritten` returns to 0 as the levels are written. Every surface that quotes "Trader route: 630 lessons, about 313 h in the app..." style lines reads the regenerated file.

Closures (`node tools/closure.mjs --target <course>/L4`): `number-sense/L4` 3 levels, 1 course, 14 lessons; `quadratics/L4` 14 levels, 4 courses, 62 lessons (57 written until number-sense level 4 exists, shown as "Route limited"); `testing/L4` 56 levels, 18 courses, 242 lessons (it adds `multivar` through `limits-thm/L4`); `stat-learning/L4` 65 levels, 26 courses, 276 lessons. The role closures (`--role`) do not move: no mock requires these levels.

Prep paths (`app/content/prep.json`): three paths name a whole course and so gain its new lessons with no edit: `oa-research` (`testing`), `interview-research` (`testing`, `stat-learning`) and `superday-research` (`stat-learning`). The level refs `number-sense/level-3` and `stat-learning/level-2` are unaffected. Decide whether six theory lessons belong in an online-assessment path; if not, change `oa-research`'s `testing` ref to its three level refs. No path needs a new entry. `capstones.json` names none of the four courses.

Exams: no exam file lists levels or carries a `requires` on these courses, so nothing breaks. Later, each topic exam gains the items its brief lists (`topic-0.1`, `topic-0.2`, `topic-1.6`; `topic-2.1` by replacement), and `stage-0`, `stage-1` and `stage-2` may each take one or two. `manifest.json` `perf` gains `testing/L4` and `stat-learning/L4` once their homework is written, each needing its `-perf.md` report for `node tools/perf-reports.mjs`.

## Order of work

1. Apply the four edits; run `node tools/validate.mjs` (0 errors), `readiness-sums.mjs --write`, `curriculum-hours.mjs --write`, the census; update PLAN, the `cover` lines and KNOWN_ISSUES.
2. Wave: number-sense level 4, testing level 4 and stat-learning level 4 can run together (different courses, no shared files). Quadratics level 4 reads `number-sense/l15` and `l16` for shared wording, so run it in the same wave only if you accept that its author works from the number-sense brief instead; otherwise after.
3. Second reads and fix passes per SESSION PROTOCOL 4 and 5; then the exam extensions, and the Option B skills with them if ruled.

## The planner's checks

Every number in the four briefs was computed twice with `/tmp/claude-0/-home-user-zero-to-quant/d9d8264b-af41-5ec5-990f-6b37bb65aa6c/scratchpad/venv/bin/python`. The scripts are in `/tmp/claude-0/-home-user-zero-to-quant/d9d8264b-af41-5ec5-990f-6b37bb65aa6c/scratchpad/gap-briefs/`: `nums.py` (topics 0.1, 0.2 and 1.6: integer and fraction arithmetic against brute force, sympy against substitution, closed forms against SciPy and 200,000 to 400,000-run simulations; it exits 0) and `ml.py` (topic 2.1, run in CPython with scikit-learn 1.6.1 and, through `run-pyodide.mjs`, in the local Pyodide 0.27.7 build; the two agree to 4 places except on `MLPClassifier`, as `gap-stat-learning.md` says). The scratchpad is not part of the repository; each level's author commits its own number script.
