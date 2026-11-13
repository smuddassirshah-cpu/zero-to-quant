# Fix pass: number scripts (engine pass AD part 1 findings)

Source: `docs/reports/number-scripts-ad.md`. Two findings, both fixed. Graded answers changed: none (the new item is additive).

## Finding 1, garch l7 (`app/content/courses/garch/l7-garch11.json`): fixed

- `screens[8].explain.text`: the unreproducible figures ($\hat\alpha = 0.17$, $\hat\beta = 0.08$) are gone; it now says where a desktop SciPy stops depends on its version.
- `screens[10].canvas.params.rows`: row 4 ("A, desktop SciPy") deleted. `screens[10].canvas.highlight.rows` in the explain went from [2, 3] to [2]. No graded key depended on the row (the widget is a multi with option ids `short`, `react`, `beta`, `recent`; none read a cell of row 4).
- Prose and text that referred to the row, updated: `screens[10].prose` ("The last row is what desktop SciPy returns for A..." now says fits of A stop at a version-specific point, so a run may differ from the table); option `beta` `why` lost "the desktop says 1.0"; the explain's "the two platforms disagree" became "different platforms can disagree". Grep for "desktop" now leaves only the unrelated `arch` package remark (screen 6 prose) and the explain sentence above.
- `docs/reports/garch-L2-numbers.py`: the two E lines on 0.17 and 0.08 and the two E lines on `rows[3]` are removed; the "CPython fit of A" claim is replaced by two claims (the table has three rows; the explain no longer states the desktop figures). Exit 0, 653 checks.
- Line removed from `app/tools/number-scripts-known-failing.txt`.
- Not done: SciPy is still unpinned in `requirements.txt` (the report's note); the lesson no longer depends on it.

## Finding 2, `app/content/exams/stage-2.json` Paper A: fixed

New item `a-spline-columns`, placed before `a-lambda-honest`; difficulty 3, skills `["sl-flexible"]`, numeric, pace 150, answer form: a whole number (tol abs 0).

Text. Prose: "A bond-spread model takes three continuous inputs: duration, issue size and years since issue. Each goes through `SplineTransformer(n_knots=6, degree=3)`. Two 0/1 flags, secured and callable, pass through unchanged. All the columns then go to `LinearRegression`." Question: "How many columns does `LinearRegression` receive?"

Key: 26. Slips (each with a `byKey` line): `knots-only` 20 (6 per input), `no-constant` 23 (K + 3 = 7 per input), `no-flags` 24.

Working, two methods. (1) scikit-learn: `ColumnTransformer` with `SplineTransformer(n_knots=6, degree=3)` on three columns and `passthrough` for two 0/1 columns gives `.transform(X).shape[1] = 26`. (2) Lesson formula: K = 6 - 2 = 4 interior knots, K + 4 = 8 basis functions per input, 3 x 8 + 2 = 26. Slips: 3 x 6 + 2 = 20; 3 x 7 + 2 = 23; 3 x 8 = 24.

Taught by `stat-learning/l18-bending-the-line` screen 3 (K + 4 basis functions, `n_knots` counts the boundary knots). Fresh: the lesson uses n_knots=5 (7 columns, 14 in all) and `review-4` has option text on few rows; the setting (bond spreads, flags, ColumnTransformer passthrough), the number 26 and all three slips are new.

Reuse greps: `grep -rln "bond-spread\|secured and callable\|years since issue" app/content` returns only `exams/stage-2.json`; `n_knots=6` appears nowhere else in `app/content`; `SplineTransformer` appears only in stat-learning l18, l19, homework-4 and the new item. `fresh-check.mjs --file content/exams/stage-2.json`: 0 hits on the new item (the 1 hit and 2 advisories are older items, parts[3].items[4] and [12]).

Exam-level rules: the file states no item count, marks total, time allowance per item or pass mark that the item changes (Paper A is 90 minutes with pass 0.7, neither tied to an item count); `check_numbers.py` asserts no counts. Its Paper A section now has the item's key, three slips, both routes and an `allow` list; exit 0, 790 checks. Line removed from the known-failing list (now empty apart from comments).

Note: `docs/briefs/exam-stage-2-scripts/build.py` generates the exam file and does not contain the new item; rerunning it would drop the item (not edited here, a content-file-only fix).

## Gates

- `node tools/validate.mjs`: 0 errors; no warning on the new item; the garch l7 warnings listed are on screens this fix did not touch.
- `node tools/run-number-scripts.mjs --python <venv> --only` each script: 1 of 1 passed, 0 known failing, 0 new failures, 0 stale lines.
- `grade-all.mjs --file` garch l7 (13 widgets) and stage-2 (60 widgets): 0 failures.
- Playthrough with `--local-cdn`: `--lesson garch/l7-garch11` and `--exam stage-2`, each with and without `--mobile`: All passed.
