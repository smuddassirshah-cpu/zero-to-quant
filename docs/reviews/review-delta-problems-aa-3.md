# Delta read: fix passes of problems 0.3 b and 0.3 c

Scope: only what the two fix passes changed, read at commit ecfe85b. `changed.py` lists 24 items and 47 parts in 9 files, and confirms no file has changed since its fix pass.

- Fix pass 0.3 b (8ffebdc, c5142a8): `exp-log/problems-1` to `-3`. 10 items, 15 parts. Record: `review-problems-0.3-b.md`, "Fix pass".
- Fix pass 0.3 c (b282993, 46c1b3a, fffad27): `series/problems-1` to `-3`, `trig/problems-1` to `-3`. 14 items, 32 parts. Record: `review-problems-0.3-c.md`, "Fix pass".

Method. Each of the 24 changed items was read whole as it now stands (`dump.py`). The re-keyed and re-authored items (forty doublings part 4, drawdown parts 3 and 4, app users part 2, weekly target parts 3 to 5, tins, pizzas, hexagon, two angles, daylight parts 4 and 5, garden bed) were solved by hand from the text before the key was read. `recompute.py` then recomputes every changed answer, band and `wrong` value twice: exactly (fractions, sympy, whole-number arithmetic) and by a second route (a loop over doublings, bisection on $1.11^n$, $1.3^n$ and $41.76e^x$, stepping the strategy month by month, the series for $e^x$, direct summation of the rows of tins, enumeration of every set of toppings and every on/off pattern, the hexagon and the garden bed by coordinates, a 12,000-step scan of the daylight model). For each part it checks that the band takes the value the feedback prints and the sensible roundings in the stated form, refuses the neighbours and every `wrong` value, and that each slip as a learner would type it lands on its own entry. It searches each re-authored item for numbers of its old version, and tests the bands of all 121 single-value numeric parts of the nine files against each other. `grade.mjs` runs the engine's own graders (`grade.js` with the local Compute Engine, the grading steps of `numeric.js`, and `expression.js` with its own `simplified` check) on every answer, `accept` form and `wrong` entry of the 24 items and on 386 typed strings. `fresh.py` searches all 2,300 content files for the new numbers, formulae and story words; I then read what it pointed at in the lessons, quizzes, reviews, homework, Fluency sets and other problem sets of the four courses of topic 0.3 and in `topic-0.3` and `stage-0` (`context.py`). Authors' scripts, the validator, the voice scan, `fresh-check` and the playthrough were run.

Scripts: `docs/reviews/delta-problems-aa-3-scripts/`, run from the repo root: `changed.py [--dump]`; `dump.py <file> [item ...]`; `recompute.py` (scratchpad venv Python); `grade.mjs --local-cdn <pkgs> [--show]`; `fresh.py [--all]`; `context.py '<glob>' '<regex>'`.

Tags: `wrong` = a learner is marked wrongly or told something false; `unclear` = a statement reads two ways; `minor` = otherwise.

## Tool results

- `recompute.py`: 2,206 checks, 0 failures; 1 note (the hexagon's `half` band inside the later `radians` band, below).
- `grade.mjs`: 1,127 checks, 0 failures; 7 FINDING rows (findings c3, c4, c5). Every answer and `accept` form grades correct and every `wrong` entry lands on its own key.
- `fresh.py`: 720 hits, judged under findings c1 and c2 and in "Verified clean".
- Authors' scripts, all 0 failures: exp-log numbers 1,213 and grade 690; series 1,475 and 692; trig 1,055 and 912.
- `node tools/validate.mjs`: 0 errors. On the nine files: five `[wrong-band]` advisories and one overlap note, judged below.
- `voice-scan.py 35`: 0 and 0. `fresh-check.mjs --file` on the nine sets: 0 hits each.
- `playthrough --problems` on all nine sets, with and without `--mobile`: all 18 runs passed.
- No changed answer, band or `wrong` value is wrong. No two bands meet, bar the one the widget resolves by first match.

## The two parts where the fixer went beyond the reader

- `p-forty-doublings` part 4 (answer 14, target £$10^{16}$). Right, and better than the reader's version. Four routes agree: a whole-number loop ($2^{53} < 10^{16} < 2^{54}$), the question's own figures ($\tfrac{10^{16}}{1.10 \times 10^{12}} \approx 9091$, $\tfrac{3.9586}{0.30103} = 13.15$), $\tfrac{16}{0.30103} - 40 = 13.15$, and part 1's 12.0412. The value 13.15 is far from a whole number, so no rounding of the given logs moves the key. Nearest rounding gives 13, which is `rounded-down`; $2^{13} = 8192 < 9091$ as its line says. `tenfold-steps` 4 and `total` 54 are the slips their lines name. No $10^{15}$, 909 or 9.83 is left in the item.
- `p-drawdown-recovery` parts 3 and 4 (11% a month). Right. $n = \tfrac{2\log 1.25}{\log 1.11}$ is 4.2764 exactly and 4.2767 from the given logs; the band takes 4.28 and both long forms and refuses 4.27 and 4.29. Month 4 holds £48,578 and month 5 £53,922, so 5; nearest rounding of 4.28 gives 4, which is `rounded-down`. The five slips of part 3 (2.14, 0.23, 5.11, 3.22, 1.41) and two of part 4 (4, 7) recompute. $\log 1.11 = 0.04532$ is right to the places given. No 8%, 1.08 or 5.80 is left. The fixer's refusal to change forty doublings part 2 (a floor by definition) is sound.

## The validator advisories

- `trig/problems-1` hexagon part 4: `half` (0.5, ±0.0005) is narrower than a whole number, and sits inside the later `radians` band. Stands. A wider `half` would take the true radian value 0.5236. First match sends 0.5 to `half`, whose line covers both readings ("It is $\sin CAD$, or a calculator's answer in another unit"). See finding c5 for the `radians` band itself.
- Lamp part 3: `ratio-tan` (0.75, ±0.0005) narrower than 1 decimal place. Stands. The tangent to 1 place is 0.8, which is also $\cos AOB = \tfrac{40}{50}$ exactly, so a wider band would tell a learner who typed the cosine that it is the tangent. 0.8 gets the generic line.
- Lamp part 3: `radians` (0.6435, ±0.005) narrower than 1 decimal place. Stands. The radian value to 1 place is 0.6, which lands on `ratio-sin`, and that line names both readings.
- `exp-log/problems-3` weekly target part 5 and monthly deposit part 2: `decimal` (±5e-7) narrower than 2 decimal places. Stands: the narrow band is what finding 7 of the first read asked for, and a decimal rounded to 2 places (0.03, 0.05) cannot be told from any other slip. The fix pass's gate line says only "validator 0 errors"; these two advisories are new with it and were not reported.

## Rulings asked for

1. `p-desk-lamp` part 5, $5(4\sqrt{3} - 3)$: finding c4. The first reader cut this `accept` form knowingly, so it is a choice, not an oversight. My view: leave it, since the question says "Starting from the elbow height $20\sqrt{3}$ cm" and shows the form wanted. The engine row for a `form` line an author can word would cure the line.
2. Whether a part that is number for number in another course's problem set of the same topic counts against "fresh": findings c1 (pizzas against `counting/problems-2`). The brief names only the item's own course.

## Fix pass 0.3 b: findings

b1. `minor` | `exp-log/problems-3.json` | `p-weekly-target` part 4 | band one step wide each side.
   "Give 4 decimal places" with answer 0.0249 and `tol` 0.0001 takes 0.0248 and 0.0250 (`grade.mjs`). No route from 0.0747 or 0.0748 gives either: $0.074724 \div 3 = 0.024908$ and $0.0748 \div 3 = 0.024933$. The first reader set this `tol`; it was "loose but harmless" on the old key too.
   Fix: `tol` `{"abs": 0.00005}` (takes 0.0249, 0.02490, 0.024908 and 0.024933; refuses 0.0248 and 0.0250).

All twelve findings of the first read are fixed as its "Fix pass" section says. Checked one by one: the yeast line (3,002 against 6,000), the weekly target re-key to the values the questions name, the bridge sentence of the deposit, forty doublings, the drawdown, the coin's band (takes 1397 to 1398.5, refuses 1399 and 1396), the two `decimal` bands (0.0252 and 0.02521, 0.0479 and 0.04793 land on `decimal`; 0.0249, 0.0259, 0.048 and 0.0491 do not), `simple` 80, `years` 2606.4 ($2400e^{0.0825} = 2606.40$ by sympy and by the series), the change-of-base choice, "in the y-axis", and the dates 2017, 2021, 2025.

## Fix pass 0.3 c: findings

c1. `minor` | `series/problems-3.json` | `p-pizza-toppings` parts 1, 3 and 4 | freshness: the new numbers are used in the sister course and the topic exam.
   The first reader checked 11 and 12 against the series files only.
   - Part 1 is `counting/problems-2` `p-quiz-team` part 1 number for number: four chosen from 11, answer 330, `ordered` 7920, `times` 44, and the same working ("$11 \times 10 \times 9 \times 8 = 7920$ ... $4! = 24$ times ... $7920 \div 24 = 330$").
   - Part 3's $\binom{12}{4} = \tfrac{11880}{24} = 495$ is `counting/homework-1` `h-long-portfolios` (a), and its with-ham branch $\binom{11}{3} = 165$ is that item's (d), the flagship stock held fixed. `topic-0.3` `e-tech-pick` also prints $\binom{12}{4} = 495$.
   - Part 4 prints row 12 ("1, 12, 66, 220, 495"). An l10 screen is $(a + b)^{12}$ with $\binom{12}{9} = \binom{12}{3} = 220$, the symmetry of part 2 on the same row, with $\binom{12}{4}$ as a wrong option.
   Fix: 15 toppings and a 16th (numbers in `recompute.py`, "proposed"; $\binom{15}{4}$, $\binom{16}{4}$, 1365, 455, 2730 and 65536 are in no file of the four courses or the two exams; 1820 is only a `wrong` value of `review-2`, a slip in a geometric sum). Part 1: 1365; `ordered` 32760, `times` 60, `three-orders` 5460. Part 2: 4 or 11 toppings, 2730; `one-size` 1365. Part 3: $\binom{15}{3} = 455$, answer 1820; `one-more` 1380, `doubled` 2730, `ordered` 43680. Part 4: row 16 begins 1, 16, 120, 560, 1820; answer 65536; `no-plain` 65535, `row-fifteen` 32768.

c2. `minor` | `trig/problems-3.json` | `p-daylight-model` parts 4 and 5 | freshness: the fix moved from one l13 screen to its neighbour.
   Finding 17 of the first read moved the level from $\sin = +0.5$ to $\sin = -0.5$. l13 has that screen too: "Setting $D(t) = 400$ gives $\sin\big(\tfrac{\pi}{6}(t - 10)\big) = -0.5$ ... The calculator gives $u = -\tfrac{\pi}{6}$. Symmetry gives $\pi + \tfrac{\pi}{6} = \tfrac{7\pi}{6}$", with the slip "You solved $\sin u = +0.5$". Part 4's working is that screen with a shift of 3 for 10. Part 5's answer, 8 months, is the wrong option of l13's transfer ("Eight months is the time below 460"). Finding 20 of the first read said it: a yearly cycle with $\tfrac{\pi}{6}$ and a level at half the amplitude is used up.
   Fix: a level that is not half the amplitude from the midline. With 10 hours (`recompute.py`, "proposed"): $\sin = \tfrac{10 - 12}{4.4} = -\tfrac{5}{11}$, the calculator gives $-0.4719$, so $t \approx 2.10$ and $t \approx 9.90$, to 2 decimal places; part 5 "to 1 decimal place", 7.8 months. Slips: `no-shift` "6.90, 11.10"; `above` "3.90, 8.10"; part 5 `outside` 4.2.

c3. `minor` | `series/problems-1.json` | `p-shop-orders` part 4 | one true plain-text form is still refused.
   Finding 2 of the first read listed `96(1.5)^(n-2)` among the strings marked wrong in the plain-text field. Its fix added bracketed-base spellings for the 64 form only. `96(1.5)^(n-2)` and `96*(1.5)^(n-2)` still get the generic line, while `96*1.5^(n-2)` passes (`grade.mjs`).
   Fix: add `96(1.5)^{n-2}` and `96\cdot(1.5)^{n-2}` to `accept`.

c4. `minor` | `trig/problems-1.json` | `p-desk-lamp` part 5 | the `simplified` check refuses a worked value and passes an unworked one.
   $5(4\sqrt{3} - 3)$ is exact and fully worked. It is marked wrong with the engine's line "That is equal, but not simplified: collect like terms and cancel", and nothing is left to collect or cancel. `20\sqrt{3}-\frac{30}{2}` passes. The four `simplified` parts have no line of their own; the engine prints its fixed one.
   Fix: none in content unless ruled (ruling 1). Engine: let `feedback.byKey.form` word the line.

c5. `minor` | `trig/problems-1.json` | `p-hexagon-tile` part 4 | finding 8 is fixed for the sine only.
   The `radians` band is still 0.5236 ± 0.5. It takes 0.87 and 0.866, which is $\cos CAD = \tfrac{\sqrt{3}}{2}$ (the explanation's own check), and 0.58, the tangent, and tells each "Your calculator is set to radians". The lamp's `radians` band was narrowed to ± 0.005 in the same fix; this one was not.
   Fix: `radians` `tol` `{"abs": 0.005}` (takes 0.52, 0.524, 0.5236). Add `radians-whole` value 1, `tol` 0, with the same line, for the radian value rounded to a whole number as asked. Then `half` no longer sits inside another band and two validator notes go.

Of the 20 findings of the first read, 18 are fixed in content as its "Fix pass" section says, bar the residues above (2: c3; 8: c5; 17: c2; 6: c1). Checked one by one, among them: shop part 4 has two `wrong` entries and $64 \times 1.5^n = 96 \times 1.5^{n-1}$; the tablet restates $u_3 = 374.4$ and $g_3 = 25.6$; the bracket's band takes 0.80795, 0.80796 and 0.807955 and sends 0.80798 and 0.807983 to `calculator`; the three `radians` lines name level 2; the water wheel restates $128.9^\circ$ and 4.87 m; two angles part 4 restates all four ratios and part 1 takes $-0.849$ and refuses $-0.85$; the quadratic's part 4 says "with no $x =$ in front" (`x=\frac{5\pi}{6}` is still refused, the engine row).

## Verified clean

- Tins: 53, 305, 7, 266 by the formula and by summing 8, 13, ..., 53; row $k$ is $5k + 3$; rows 1 to 3 hold 39 and rows 1 to 4 hold 62; all eleven slips. Fresh: no tins, no $5k + 3$, no 305 or 266 in the course or the exams. Notes: l2 has $u_n = 5n + 4$ ($a = 9$, $d = 5$) and l5's trap is $\sum_{k=4}^{12}$, the same lower limit. Neither is the setting or the numbers.
- Pizzas: 330, 660, 495, 4096 by `math.comb` and by enumeration; every slip. The numbers are right; only their freshness is in question (c1).
- Hexagon: sides, $4\sqrt{3}$, $AC = 8\sqrt{3}$, $AD = 16$, 256 and $30^\circ$ by coordinates; slips $\sqrt{80}$, $8\sqrt{3}$, $4\sqrt{2}$; $4\sqrt{3}$, 8, 16; 88, 174.85, 200. The engine takes `4\sqrt{3}`, `\sqrt{48}`, `4sqrt(3)`, `8\sqrt{3}`, `\sqrt{192}` and refuses `\sqrt{8^2-4^2}`, `8\sin(60^\circ)`, `2\sqrt{12}`, `2\cdot4\sqrt{3}` and the decimals. Fresh: no hexagon in the course; $4\sqrt{3}$ is one option of an l4 screen.
- Lamp: `20\sqrt{3}`, `\sqrt{1200}` pass and the unworked lines of part 1 are refused; 0.75, 3/4, 0.6, 3/5, 0.64, 0.644 and 0.6435 each land on their own entry; 0.65, 0.7 and 0.8 get the generic line.
- Two angles: $-\tfrac{45}{53}$, $\tfrac{357}{1325}$, $-\tfrac{1276}{1325}$, $164.37^\circ$ exactly and from the angles themselves ($148.11^\circ + 16.26^\circ$); $357^2 + 1276^2 = 1325^2$; all twelve slips. 28, 45, 53 is in no trig or exam file.
- Daylight: $t = 2$ and 10 by `solveset` and by the scan; `no-shift` 7, 11; `above` 4, 8 (14.2 hours); 8 months, slips 4 and 9. Right; freshness under c2.
- Garden bed: $65\sin C$; $22.62^\circ$ and $157.38^\circ$; $-\tfrac{12}{13}$; $\sqrt{509} = 22.561$ by the rule and by coordinates; area 25 for both beds by coordinates; all twelve slips; `65\sin C`, `65sin(C)`, `\frac{130\sin C}{2}` pass. The 5, 12, 13 triple stands by the main session's ruling; 10 m, 13 m, 25 m$^2$, 509 and 22.56 are in no other file of the course.
- `accept` additions: `80*(0.9)^(n-1)`, `80(0.9)^(n-1)`, `160(0.4)^(n-1)`, `160*(0.4)^(n-1)`, `64(1.5)^(n-1)`, `64*(1.5)^(n-1)` and the LaTeX spellings pass; `80*(0.9)^n`, `160(0.4)^n`, `160*(0.6)^(n-1)` are refused; `64(1.5)^n` lands on `month-two-start`. Fraction bases in plain text (`80(9/10)^(n-1)`) stay refused, the engine row.
- Exp-log freshness: 11%, $1.11^n$, 0.04532, 4.28 and £$10^{16}$ are in no exp-log file and in neither exam (11% appears once in `series/review-3`, as the size of an error). `homework-2` `h-drawdown` is a strategy losing 15% a month, solved for the first month below a level: the same family as before the fix, other numbers. App users part 2 is l7's judgement ("$\log_5 200$" as a quotient of logs, and the trap "a quotient of logs is not the log of a quotient") with new numbers, as finding 10 asked.
- Weekly target: $\ln\tfrac{45}{41.76} = 0.074724$ by sympy and by bisection; $e^{0.0249} - 1 = 0.0252126$; parts 4 and 5 print no 0.0748.
- Note outside the delta: `p-two-angles` part 2 was not changed and is l10's worked screen with the ratios swapped ($\sin\theta = 0.28$, $1 - 0.0784 = 0.9216$, 0.96, and the trap $1 - 0.28$). No fix asked; a later pass on this item might move B to another triple.

## Counts

- Fix pass 0.3 b: `wrong` 0, `unclear` 0, `minor` 1 (b1).
- Fix pass 0.3 c: `wrong` 0, `unclear` 0, `minor` 5 (c1 to c5).

Both fix passes can stand as merged. c1 and c2 are the two worth a pass: each re-authored for freshness and landed on numbers the topic already uses.

## Fix pass

All 6 findings applied (b1, c1 to c5), with one deviation from ruling (a): the pizza pair 15 and 16 was dropped for 18 and 19 because the new numbers were not absent. 16 x 15 x 14 x 13 = 43680 is printed in `topic-0.3` (a code count) and is part 3's `ordered` slip; $\binom{16}{4} = 1820$ is a `wrong` value in `series/review-2`; $\binom{16}{3} = 560$ is a printed portfolio count in `counting/homework-2` and `l8`. 18 and 19 appear nowhere in `counting`, `series`, `trig`, `topic-0.3` or `stage-0` (every printed value searched as a whole number, with and without a comma). Verified: validator 0 errors; voice scan 0 and 0; the three numbers scripts (series 1,481, trig 1,086, exp-log 1,217 checks) and three grade scripts (series 704, trig 938, exp-log 695) all exit 0 with 0 failures; `--problems` playthrough on `series/problems-1`, `series/problems-3`, `trig/problems-1`, `trig/problems-3`, `exp-log/problems-3`, each with and without `--mobile`: all passed.

- b1 fixed: `p-weekly-target` part 4 `tol` 0.00005. Takes 0.0249, 0.02490, 0.024907, 0.024908, 0.024933; refuses 0.0248 and 0.0250. The `carried` wrong band (0.0259 +- 0.00005) does not meet it.
- c1 fixed (deviation above): `p-pizza-toppings` re-keyed to 18 toppings and a 19th, every answer, `wrong` value and printed line recomputed by formula and by `itertools` enumeration.
- c2 fixed: `p-daylight-model` parts 4 and 5 re-keyed to a level of 10 hours (sine -5/11); exact and by `bisect` and a 12,000-step scan.
- c3 fixed: `p-shop-orders` part 4 `accept` gains `96(1.5)^{n-2}` and `96\cdot(1.5)^{n-2}`. The grade script proves the engine takes the plain-text `96(1.5)^(n-2)` and `96*(1.5)^(n-2)` as well as both bracketed LaTeX forms, and still refuses `96(1.5)^(n-1)` and `96(1.5)^(n-3)`.
- c4 fixed by ruling: `5(4\sqrt{3}-3)` stays refused. `p-desk-lamp` part 5 now has `feedback.byKey.form`: "That is equal, but not in the form asked. Multiply out any bracket and work out any fraction, to give a multiple of $\sqrt{3}$ minus a whole number." The player shows `byKey[key]` before the engine's stock line (`player.js` `notYetLine`), and the widget returns key `form` for this typing, so the learner sees this line. `20\sqrt{3}-\frac{30}{2}` is still accepted (as the reader found); no engine edit.
- c5 fixed: `p-hexagon-tile` part 4 `radians` `tol` 0.005 (takes 0.52, 0.524, 0.5236) and a new `radians-whole` (1, `tol` 0) with the `radians` line. 0.87, 0.866, 0.58 and 0.577 now fall in no band. `half` (0.5) no longer sits inside another band.
- Standing advisories: no edit, as ruled.

Changed graded values (old to new, with the working):

- Pizzas, 18 toppings (old 11). P1: 330 to 3060 = (18 x 17 x 16 x 15)/4! = 73440/24; `ordered` 7920 to 73440; `times` 44 to 72 = 18 x 4; `three-orders` 1320 to 12240 = 73440/6.
- P2 (4 or 14 toppings, old 4 or 7): 660 to 6120 = 2 x 3060 (C(18,14) = C(18,4)); `one-size` 330 to 3060.
- P3 (19th topping, old 12th): 495 to 3876 = 3060 + C(18,3) = 3060 + 816, and C(19,4) = 93024/24 = 3876; `one-more` 341 to 3078 = 3060 + 18; `doubled` 660 to 6120; `ordered` 11880 to 93024 = 19 x 18 x 17 x 16. Printed 165 to 816 = 4896/6.
- P4 (row 19 begins 1, 19, 171, 969, 3876): 4096 to 524288 = 2^19; `no-plain` 4095 to 524287; `row-eleven` 2048 renamed `row-eighteen`, 262144 = 2^18.
- Daylight, level 10 hours (old 9.8). sin(pi/6 (t - 3)) = (10 - 12)/4.4 = -5/11; asin(5/11) = 0.4719; t = 3 - 6(0.4719)/pi = 2.0988 and t = 3 + 6(pi + 0.4719)/pi = 9.9012.
- Part 4: answers 2 and 10 to 2.1 and 9.9 (`tol` 0.01 unchanged; takes 2.10, 9.90, 2.0988, 9.9012; refuses 2, 10). `no-shift` "7, 11" to "6.9, 11.1": 6(pi + 0.4719)/pi = 6.9012 and 6(2pi - 0.4719)/pi = 11.0988. `above` "4, 8" to "3.9, 8.1": sine +5/11 gives t = 3 + 0.9012 = 3.9012 and 3 + 6(pi - 0.4719)/pi = 8.0988 (14 hours: 12 + 4.4 x 5/11).
- Part 5: answer 8 to 7.8, `tol` 0 to 0.05 ("1 decimal place"): 9.9012 - 2.0988 = 7.8024; `outside` 4 to 4.2 (12 - 7.8, `tol` 0.05); `counted` 9 renamed `whole-months` and set to 8 (`tol` 0.05; the crossings rounded to 2 and 10 give 10 - 2).
- Weekly target part 4: answer 0.0249 unchanged, `tol` 0.0001 to 0.00005 (0.0747/3 = 0.0249, 0.074724/3 = 0.024908, 0.0748/3 = 0.024933).
- Hexagon part 4: answer 30 unchanged. `radians` `tol` 0.5 to 0.005 around 0.5236 = pi/6; new `radians-whole` value 1 = round(0.5236). 0.866 = cos 30 and 0.577 = tan 30 are now unbanded.
- Shop part 4 and lamp part 5: no graded value changed (`accept` forms and a `form` line only).
