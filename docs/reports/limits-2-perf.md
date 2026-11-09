# limits level 2: performance task (PLAN 2a Phase 3 retrofit)

- File: `app/content/courses/limits/homework-2.json`, item `h-prove-negative-powers`, index 9 (item 10 of 10; appended, nothing converted).
- Kind `derivation` (longform, empty box), difficulty 5, skills `lm-derivative`, `lm-rules`.
- Matched objective: l7 "Derive the power rule for whole powers and use it for any power." It is the only L2 objective that starts with derive, prove, write, build or code.
- Task: (a) the power rule for whole $n \ge 1$ from the definition; (b) $\frac{d}{dx}x^{-n} = -n x^{-n-1}$ from the definition, using (a), with $x \neq 0$ and $x + h \neq 0$ named; (c) $g = x^{-4}$: $g'(2) = -0.125$ against the quotients $-0.1235$ ($h = 0.01$) and $-0.1266$ ($h = -0.01$); optional $g'(-2) = 0.125$. Rigour: limits by substitution into a polynomial or a fraction whose bottom is not 0 (L1 l2, l3); no ε-δ (the course never teaches it).
- Rubric 3, 1, 3, 2, 1. Rows 1 to 4 `required` (9 points); row 5 is the part the prompt marks "Optional, one more point:". Rows 1 and 3 accept any route (binomial count, factorisation, induction). `rubric-passes.mjs`: the only minimal pass is rows 1 to 4; row 5 can be left out.
- Overlapping screens: l7 screen 7 (the binomial derivation of the power rule, put in order), l7 screens 3 and 5 and quiz 2 (negative powers by the rule, not from the definition), homework-2 `hw2-derive-reciprocal` (1/x from first principles, ordered), l6 screens 8 and 9. New: every negative whole power from the definition built on (a), the conditions $x \neq 0$ and $0 < |h| < |x|$, the numerical secant check at $x^{-4}$, and $g'(-2)$.
- Freshness grep (course folder, every hit read): `x^{-n}`, `x^{-4}`, `(x+h)^n`, `negative power`, `every whole`, `2.01`, `1.99`, `0.125`; `fresh-check.mjs --file content/courses/limits/homework-2.json --min-run 10`: 0 hits.

## Gates

1. Validator, `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors; expected warning "limits/L2: has a performance task, remove from perf-pending". Manifest restored before commit.
2. Voice, `VOICE_BASE=app/content/courses/limits python3 docs/reviews/voice-scan.py 35`: 0 and 0.
3. Numbers script, `<venv>/bin/python -I docs/reports/limits-2-perf-numbers.py`: exit 0, 79 checks. sympy limits of both quotients ($n$ to 15 and 12), each model line by sympy, exact rationals and floats for (c), a table for $h = 10^{-1}$ to $10^{-6}$ from both sides; passing tick sets listed.
4. Playthrough, `node tools/playthrough.mjs --set limits/homework-2 --local-cdn <pkgs>`: All passed. With `--mobile` the new item passes at 440 px (its (b) display was split); the run fails on the older `hw2-corners` (a display wider than its column at 440 px), left unedited as the brief says.

No backlog bullets. No course.json change.
