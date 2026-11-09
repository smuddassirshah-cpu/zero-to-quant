# limits level 4: performance task (PLAN 2a Phase 3 retrofit)

- File: `app/content/courses/limits/homework-4.json`, item `h-build-cable-route`, index 9 (item 10 of 10; appended, nothing converted).
- Kind `derivation` (longform, empty box), difficulty 5, skill `lm-optimise`.
- Matched objective: l14 "Build the function from a constraint, then check the type and the ends". It is the only L4 objective that starts with a rule verb. The verb table gives `code` for build, but this product is a written function and its checks, in a course with no code widgets, so `derivation` (precedent: measure-prob L2 "Build expectation...", accepted in `review-perf-retrofit-2.md`). Backlog bullet raised.
- Task: a fibre cable from A across a 3 km river to B, 8 km downstream; £500,000 per km under water, £300,000 along the bank. (a) $C(x) = 500\sqrt{9 + x^2} + 300(8 - x)$ (£ thousand) from Pythagoras and the bank constraint, range $0 \le x \le 8$ argued; (b) $x = 2.25$, minimum by the sign of $C'$, ends 3,900 and 4,272, least cost £3,600,000; (c) B' at 2 km: no stationary point inside, the end $x = 2$ wins, about £1,803,000 against £2,100,000; optional: lands short exactly when $d > 2.25$.
- Rubric 2, 3, 2, 2, 1. Rows 1 to 4 `required` (9 points), one each for (a), the stationary point, type and ends, and (c); row 5 is marked "Optional, one more point:". `rubric-passes.mjs`: the only minimal pass is rows 1 to 4; row 5 can be left out.
- Overlapping screens: l14 screens 0 to 8 (fence against a wall, the card box, the open box of fixed volume, type and ends, the trap where a short wall makes the end win, the method summary), l14 quiz 3 `q-end-wins` (an end wins on a range), l13 screen 6 and quiz 2, review-4 `r-endpoint-cubic`, homework-4 `h-box-general`. New: a cost built with Pythagoras, a square-root cost (chain rule), why squaring is safe, the sign of $C'$ through $16x^2 - 81$, the range argued from the geometry, the same derivative giving an end point when B moves, and the threshold in $d$.
- Freshness grep (course folder, every hit read): `river`, `cable`, `fibre`, `shore`, `Pythag`, `route`, `landing`, `sqrt{9`, `2.25`, `3.75`; only unrelated hits. `fresh-check.mjs --file content/courses/limits/homework-4.json --min-run 10`: no hit on the new item (older items 5 and 6 only).

## Gates

1. Validator, `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors; expected warning "limits/L4: has a performance task, remove from perf-pending". Manifest restored before commit.
2. Voice, `VOICE_BASE=app/content/courses/limits python3 docs/reviews/voice-scan.py 35`: 0 and 0.
3. Numbers script, `<venv>/bin/python -I docs/reports/limits-4-perf-numbers.py`: exit 0, 86 checks. sympy derivative, exact solve, $C''$, limit and exact values; a numerical table of $C'$ and a brute-force search over landing points (also outside the range, and for 48 values of $d$); passing tick sets listed.
4. Playthrough, `node tools/playthrough.mjs --set limits/homework-4 --local-cdn <pkgs>`, with and without `--mobile`: the new item passes at 1280 and 440 px (its (b) display was split with `aligned`); all 10 items marked right, 2 longform marked by the button. Both runs fail only on the older `h-long-kelly`, whose $G(0.1) = 0.55\ln 1.1 + \dots$ display is wider than its column at 1280 and at 440 px; left unedited as the brief says.

One backlog bullet (build verb in a maths course). No course.json change.
