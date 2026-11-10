# Fluency: trig (brief `docs/briefs/fluency.md`, agent 3)

Four sets, 15 families. Each set uses its lesson's wording: "short sides" and "hypotenuse" with $a^2 + b^2 = c^2$ (l1), calculator values given as "Use $\sin 40^\circ \approx 0.6428$" (l3), the half-square and half-equilateral triangle (l4), and $\pi$ radians $= 180^\circ$ with $s = r\theta$ (l7). No set uses an idea from a later lesson.

| Set | Family | Distinct prompts in 200 | `form` | Slips (`wrong` ids) |
| --- | --- | --- | --- | --- |
| fluency-l1-squares-on-sides | hypotenuse-whole (numeric) | 67 | none | forgot-the-root, added-the-sides |
| | short-side-whole (numeric) | 62 | none | added-the-squares, took-away-sides |
| | hypotenuse-2-dp (numeric) | 85 | none | forgot-the-root, added-the-sides |
| | short-side-2-dp (numeric) | 105 | none | added-the-squares, forgot-the-root |
| fluency-l3-sides-and-angles | side-from-hypotenuse (numeric) | 192 | none | other-ratio, divided-by-ratio |
| | hypotenuse-from-side (numeric) | 193 | none | multiplied-by-ratio, other-ratio |
| | height-with-tan (numeric) | 196 | none | used-sine, divided-by-tan |
| fluency-l4-exact-values | side-from-hypotenuse (exact) | 75 | simplified | other-ratio, divided-by-ratio |
| | height-with-tan (exact) | 73 | simplified | used-sine, divided-by-tan |
| | forty-five-triangle (exact) | 73 | simplified | halved, times-root-two |
| | combine-values (exact) | 168 | simplified | swapped-values, dropped-halves |
| fluency-l7-arc-length | degrees-to-radians (numeric $k$ in $k\pi$) | 66 | none | upside-down, used-a-full-turn |
| | radians-to-degrees (numeric) | 72 | none | used-a-full-turn, dropped-pi |
| | radians-to-degrees-1-dp (numeric) | 92 | none | wrong-way-round, used-a-full-turn |
| | arc-length (numeric, 2 dp) | 174 | none | used-degrees, wrong-way-round |

## Exact values (l4)

Exact keys are constants, graded by value, so a typed-back `27\sin 60^\circ` would score. I probed with `test-fluency.mjs`: with `form: "simplified"`, `27\sin 60^\circ`, `27\sin(60^\circ)`, `27\cos 30^\circ`, `\tan 30^\circ`, `\frac{\sin 30^\circ}{\cos 30^\circ}` and the prompt `4\sin 30^\circ+6\cos 30^\circ` are all refused, while `\frac{1}{\sqrt{3}}`, `\frac{\sqrt{3}}{3}` and `\sqrt{3}/3` pass. Every l4 family therefore sets `form: "simplified"`, and the test confirms the prompt typed back fails at 50 seeds. Keys are written with `poly(r; ...)`, where `r` is a text var holding `\sqrt{3}` or `\sqrt{2}`.

## Values in `let`

l3 gives the sine, cosine and tangent in the prompt, to 4 dp, as the lesson does. They come from a Taylor series in `let` (the evaluator has no `sin`), and the key is worked from the given values. The number script checks each given value against sympy's exact `sin` and that the true answer also lies inside the tolerance. A `where` keeps that true for hypotenuse-from-side, where dividing by a small sine had pushed six draws in 200 outside it. l7 writes $\pi$ as `3.14159265358979`.

## Checks

1. `docs/reports/fluency-trig-numbers.py` (sympy venv), 200 draws of every family. It rebuilds each key from the vars alone: `sympy.solve` for Pythagoras, sympy's exact `sin`, `cos`, `tan` and `pi`, and the triple parameters for the whole-number families. It also checks each `wrong` is the named slip and outside the key's tolerance, each `accept` string, and the prompt text. Result: 20,000 of 20,000 checks pass, exit 0.
2. Validator: 0 errors, no warning on these files. `test-fluency.mjs --local-cdn` per set: 278, 274, 278 and 278, all pass.
3. Playthrough `--fluency` for all 4 sets, with and without `--mobile`: all green. Screenshots of l3 and l4 (wrong answer) at 440 px looked right, with no overflow.
4. Voice scan 35 on trig: 0 and 0.
5. I read 20 draws of every family as a learner would (300 items), with the same pattern scan as exp-log: no `1x`, `+-`, `x^1`, `0x`, double minus, unreduced fraction or float artefact. No prompt gives the answer away. Fixed while reading: a fractional coefficient printed as `3.5\sqrt{3}` (hypotenuses are now even), a `sqrt` of a negative number in short-side-2-dp, and "$180 \times 1 \div 12$" in radians-to-degrees.

## Skipped (raised in BACKLOG-INBOX under "Raised later (fluency exp-log trig)")

- l7 "Write ${d}^\circ$ in radians, exactly" as an expression: `form: "simplified"` lets `15^\circ` and `\frac{15\pi}{180}` pass for `\frac{\pi}{12}`. Asked instead as "Write ${d}^\circ$ as $k\pi$ radians. What is $k$?"

## Widening pass

Entries worked: the `let` work-rounds now use the evaluator's own functions, and the skipped exact-radians family is added with `form: "exact-angle"`.

| Set | Family | Distinct prompts in 200 | `form` | Slips (`wrong` ids) |
| --- | --- | --- | --- | --- |
| fluency-l3-sides-and-angles | side-from-hypotenuse (changed `let`) | 192 | none | other-ratio, divided-by-ratio |
| | hypotenuse-from-side (changed `let`) | 193 | none | multiplied-by-ratio, other-ratio |
| | height-with-tan (changed `let`) | 196 | none | used-sine, divided-by-tan |
| fluency-l7-arc-length | degrees-to-radians-exact (new) | 64 | exact-angle | upside-down, used-a-full-turn |
| | radians-to-degrees, radians-to-degrees-1-dp, arc-length (changed `let`) | 72, 92, 174 | none | as before |

In l3 the Taylor series for sine and cosine (and their quotient for tangent) became `round(sin(x), 4)`, `round(cos(x), 4)` and `round(tan(x), 4)`, and `sin(x)`, `cos(x)` in the unrounded `exact`, with `x = t*pi/180`; in l7 every `3.14159265358979` became `pi`. I drew 200 items of every trig set on seed 1 before and after: the same vars, prompts, solutions and wrong values in all 800, and keys equal to within 1e-8. The new family asks "Write $55^\circ$ in radians, exactly." with key $\frac{11\pi}{36}$; $\frac{11}{36}\pi$ is accepted, and the retyped `55^\circ` is refused by the form. The numeric "What is $k$?" family stays as it was.

Checks: (1) `fluency-trig-numbers.py` now covers 16 families (new `l7_d2r_exact`, and its parser reads `\pi`), 21,600 of 21,600 checks, exit 0. (2) Validator 0 errors, no warning on trig fluency files; `test-fluency.mjs --local-cdn`: l3 304 of 304, l7 312 of 312. (3) Playthrough `--fluency` of l3 and l7 with and without `--mobile`: green. (4) `voice-scan.py 35` on trig: 0 and 0. (5) I read 20 draws of the new family and of the changed l3 families: no `1\pi`, `+-`, double minus or unreduced key, and no prompt gives the answer away. (6) This section.

Still blocked: none of this course's listed entries. l4 keeps whole coefficients (even hypotenuses) because `poly` still writes a terminating coefficient as a decimal (`3.5\sqrt{3}`); raised again in the inbox.
