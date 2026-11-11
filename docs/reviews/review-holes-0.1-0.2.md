# Syllabus holes 0.1 and 0.2: second-reader findings

Read at commit ef15de0. A full second read of content written in session AB and not read before. Pattern: `review-problems-0.2-a.md`.

Tags: `wrong` = a learner is marked wrongly or told something false; `unclear` = the question can be read two ways, does not give what the learner needs, or refuses a sensible entry; `minor` = weak part, loose chain, loose `wrong` entry, wording, freshness, tagging or tooling.

Scope.

- Exams: the six new items of `app/content/exams/topic-0.1.json` (`e-feed-updates`, `e-prime-table`, `e-plan-hall`, `e-pit-area`, `e-partner-number`, `e-five-counts`) and the four of `topic-0.2.json` (`e-surd-difference`, `e-two-desks`, `e-diameter-ends`, `e-cubic-remainder`, two parts).
- Skills: `ns-measures` and `quad-rational`, on every lesson, review, homework, problem and exam item of level 4 of `number-sense` and `quadratics`.
- Problem sets: `number-sense/problems-4.json` (4 problems, 16 parts) and `quadratics/problems-4.json` (3 problems, 15 parts), against `docs/briefs/chained.md`.
- Fluency: all nine new sets, 32 families (number-sense l15 to l19, 18 families; quadratics l14 to l17, 14 families), 20 draws a family, 640 draws.

Method. The six authors' scripts were run first. Every graded key and every `wrong` value was then worked by hand from the item's text and again in `review-holes-0.1-0.2-scripts/mine.py` (sympy or fractions, then a second route: search, substitution, the story's own arithmetic), with no import from the authors' scripts. Every fluency draw was recomputed from its prompt text alone (`fluency-read.py`: regex on the sentence the learner reads, never the draw's `vars` or `lets`). Every typed part then went through the engine's own graders in node (`grade-probe.mjs` and `fluency-probe.mjs`: `numGrade`, `numSetGrade`, `exprGrade` of `app/js/engine/grade.js` with the local Compute Engine): the answer, each `accept` form, each `wrong` entry on its own key, and typed strings of my own for what a learner who is right would type (other orders, a letter and `=` in front, fractions for decimals, units, $\pi \approx 3.14$ and $\tfrac{22}{7}$, the factorised or multiplied-out twin) and what a learner one step short would type (the question typed back, a fraction not cancelled, the whole fraction where the top is asked, one root of two, the value in the wrong unit). The lessons were searched for each idea an item leans on.

Tool results.

| check | result |
|---|---|
| authors' number scripts (scratchpad venv) | `exam-0.1-holes` 90 of 90; `exam-0.2-holes` 58 of 58; `problems-number-sense` 275 checks, 0 failures; `problems-quadratics` 857, 0; `fluency-number-sense` 55,164 of 55,164; `fluency-quadratics` 55,533 of 55,533; all exit 0 |
| `mine.py` (reader's own keys and slips) | 313 checks, 0 failures |
| `fluency-read.py` (640 draws from the prompt text) | 3,612 checks, 0 failures, 75 notes read (findings 15 to 21) |
| `grade-probe.mjs` (engine graders, problems and exam items) | 546 checks over 38 parts, 0 failures, 17 rows held to be faults (findings 9, 11, 12) |
| `fluency-probe.mjs` (engine graders, every draw) | 2,757 checks, 0 failures, 3 classes of row against the reader (findings 16, 17) |
| `windy-form.mjs` (sizes finding 12, tries the fixes of 11 and 13) | table under finding 12 |
| `shares.py` (200 draws of eight families) | shares quoted in findings 16 to 21 |
| `proposed.py` (numbers of the fixes below) | all pass |
| `try-fixes.py` (the fluency fixes of findings 15 to 21 on copies, drawn with `fluency-sample.mjs --file --stats`) | each patched family draws 200 seeds: `table-mean` 200 distinct prompts, `quotient` 194, `add-tops` 200, `subtract-tops` 199, `conjugate-bottom` 184, `other-number` 163, `count-factors` 113 |
| `skills.py` (every skill tag of the two levels and exams) | 0 unknown tags |
| validator | 0 errors; no warning on any file in scope (the two `topic-0.2` warnings are on the older `e-formula` and `e-gap-table`); `manifest.json` unchanged |
| playthrough `--problems` both sets, `--exam topic-0.1` and `topic-0.2`, `--local-cdn` | all passed, desktop and `--mobile` |
| voice scan 35, `number-sense`, `quadratics`, `exams` | 0 and 0 each |
| `fresh-check.mjs --file`, gate and triage, both sets; `--exam` both | 0 hits; 3 advisories read (a shared $2^2 \times 3^3$ that is 72's distractor in l15, three small numbers shared with a mock, $x^2 + 5x + 6$ in l15 s1): none a copy. Two reuses the tool missed are findings 6 and 7 |

Result. No key, `accept` form, feedback line or explanation states a wrong value: every number agrees with mine, in all 31 problem parts, 10 exam items and 640 fluency draws. Every `wrong` value is the slip its line describes and lands on its own key. No exam item repeats a fault of `review-number-sense-4.md` or `review-quadratics-4.md`: `e-pit-area` takes 199 with 3.14, 3.142 and $\tfrac{22}{7}$ and with the radius kept to 2 decimal places; the circle Fluency bands take the 3.14 and $\tfrac{22}{7}$ values at every size the families can draw (radius at most 8 for areas, diameter at most 30 for the distance round); no per cent, no "growth factor", no "multiplied by 3.6", no digit-sum test, no always or never rule. Two faults of `review-quadratics-4.md` do come back outside the exams: finding 8 there (the whole fraction typed where the top is asked) in findings 13 and 18 here, and finding 19 there (an uncancelled form passes) in finding 12.

The known open fault is confirmed and sized in finding 12. There is no `wrong` finding; four are `unclear`.

Claims checked beyond the keys: 127 and 149 are the only primes of the six, and 2, 3, 5, 7 and 11 are enough because the largest size, 161, is under $13^2$; 56 is the only number from 1 to 2,000 with HCF 8 and LCM 168 against 24; $(3, 8, 9, 10, 10)$ is the only sorted five of whole numbers from 0 to 40 with mean 8, median 9, only mode 10 and range 7; both ends of the diameter are 10 from $(1, 10)$; the tangent $y = x + 5 + 10\sqrt2$ is 10 m from the pond's centre; the ride of 2 hours out and 1.5 home makes 3.5; the 12 tile sides run from 1 cm to 108 cm; the painted teeth first meet after 144 teeth by direct search.

## A. Exam items and skill tags

1. `unclear` | `exams/topic-0.2.json` | `e-diameter-ends` | `prose`.
   The item needs the point halfway between two points on a grid. No lesson, review or homework of `equations`, `functions` or `quadratics` finds one: "halfway" is only ever between two numbers on one axis (quadratics l11, functions l11), and "diameter" appears once in quadratics level 4, in a distractor line of l18. A learner who knows the radius rule has no taught way to the centre.
   Fix: `prose` "The points $(-5, 2)$ and $(7, 18)$ are the two ends of a diameter of a circle. The centre is halfway along the diameter." Key, `wrong` and feedback unchanged (midpoint $(1, 10)$, ends 20 apart; `proposed.py`).

2. `minor` | `exams/topic-0.1.json` | `e-pit-area` | `widget.wrong`.
   A learner who rounds the radius $7.958$ to 8 before squaring gets $\pi \times 8^2 = 201.06$ and types 201 (200.96 with 3.14). The generic line then tells them to "find the radius from the distance round, then use area $= \pi r^2$", which they did.
   Fix: add `{ "id": "rounded-radius", "value": 201, "tol": { "abs": 0.5 } }` and `byKey` `"rounded-radius": "You rounded the radius to 8 m before squaring. Keep 7.96 and round only at the end."` The band 200.5 to 201.5 is clear of 199 ± 0.5.
   Note, no change asked: finding a radius from the distance round is practised nowhere in level 4 (l18, review-4 and homework-4 all go from the radius or the distance across). It is fair transfer at difficulty 3 with a calculator, and the generic line gives the step.

3. `minor` | `exams/topic-0.1.json` | `e-feed-updates` | `widget.wrong`.
   The units item has no entry for reading 6.5 hours as 6 hours 50 minutes, the slip a decimal time invites: $15 \times 24{,}600 = 369{,}000$.
   Fix: add `{ "id": "six-fifty", "value": 369000, "tol": { "abs": 0.5 } }` and `byKey` `"six-fifty": "You read 6.5 hours as 6 hours 50 minutes. Half an hour is 30 minutes, so the session is $6.5 \\times 3{,}600$ seconds."`

4. `minor` | `exams/topic-0.1.json` | `e-five-counts` | `title`.
   "Four averages, five days." The range is not an average: l19 says it "measures spread", and `number-sense/problems-4` `p-cycle-commute` part 3 marks "the range" wrong for that reason.
   Fix: `title` "Four summaries, five days".

5. `minor` | `courses/quadratics/course.json`, `courses/number-sense/course.json`, and the `skills` maps of `exams/topic-0.2.json` and `exams/topic-0.1.json` | skill names.
   The re-tagging itself is honest. Every item now under `ns-measures` is about perimeter, area, circles, units or averages (l17, l18, l19; review `r-l-shape`, `r-triangle`, `r-circle-14`, `r-54`, `r-freq-mean`, `r-remove`; homework `h-semicircle`, `h-speed`, `h-freq`, `h-leaver`, `h-long-leaflet`; the four exam items). Every item under `quad-rational` is about surds, algebraic fractions or polynomial division, and the five that keep `quad-solve` beside it do solve a quadratic (l16, `r4-reject`, `hw4-fraction-equation`, `hw4-find-the-errors`, `e-two-desks`). No item of either level is left on a placeholder tag.
   Two older names no longer describe what sits under them, and the learner sees the name on the skills screen. `quad-graph` is named "Parabolas" and now carries the circle work: l18, l19, `r4-distance`, `hw4-circle-line`, `hw4-tangent-circle`, `hw4-tangency-proof`, `p-park-pond` and the new exam item `e-diameter-ends`. `ns-powers` is named "Powers and roots" and carries primes, HCF and LCM: l15, l16, `r-primes-180`, `r-count-180`, `r-lcm-36-60`, `h-90-126`, `h-euclid`, `h-2520`, and the new exam items `e-prime-table` and `e-partner-number`.
   Fix (names only; ids stay, both courses stay at six skills): `quad-graph` "Parabolas and circles" in `quadratics/course.json` and `topic-0.2.json`; `ns-powers` "Powers, roots and primes" in `number-sense/course.json` and `topic-0.1.json`. Those four files are the only ones that hold the two names.

## B. `number-sense/problems-4.json`

Chain, restated values, forms, tolerances and coverage hold: every later part carries the value it needs; each rounded part names its places; each band takes the value its feedback prints and the 3.14 and $\tfrac{22}{7}$ values; l15 to l19 each appear (l15 by the factor count, l16 by HCF and LCM, l17 by rectangle areas, l18 by circles and unit changes, l19 by `p-cycle-commute`); 15 of 16 parts are typed.

6. `minor` | `p-lawn-pond` | freshness.
   "A circular pond 6 m across", area to 2 decimal places, first slip "squared the distance across": this is l18's trap screen ("A circular pond is 10 m across", line 1376, and the lesson's `summary.trap`) with a new number. The lawn is homework-4 `h-semicircle` ("A lawn is a 10 m by 6 m rectangle with a semicircle", radius 3, as here). `fresh-check` reports neither.
   Fix, story only, every number kept: `prose` "A rectangular courtyard is 12 m by 9 m. A round basin 6 m across is set into the middle of its paving." Then swap through the item: pond to basin, lawn to courtyard, grass to paving, "Grass seed comes in boxes that each cover 20 m²" to "Sealant comes in tins that each cover 20 m²", boxes to tins, "how much grass is left" to "how much paving is left", `whole-lawn` line "That seals all 108 m², basin included. Only 79.73 m² is paving." None of courtyard, paving, sealant or basin is used in `number-sense` or `topic-0.1`. Keep the item id.

7. `minor` | `p-hall-tiles` | freshness against the exam.
   "A hall floor is a rectangle ... what is the floor's area in square metres" sits beside the new exam item `e-plan-hall` ("The server hall is a rectangle ... real floor area of the hall, in square metres"). The brief asks for no story from an exam of the course.
   Fix: "A kitchen floor is a rectangle 432 cm by 540 cm." ("kitchen" is unused in the course). Keep the item id.

8. `minor` | `p-hall-tiles` | `difficulty` 5, and l15's main skill.
   This is the set's only 5, and it is the easiest problem to start: the prose hands over both prime factorisations, part 2 hands over $108 = 2^2 \times 3^3$, and each part is then one step. `p-meshing-gears` (4) gives its factorisations too, so no part of the set asks the learner to split a number into primes, the skill l15 is named for.
   Fix: drop the last sentence of the `prose` ("In primes, ..."), so part 1 starts from 432 and 540. Part 1 `explain`: "In primes, $432 = 2^4 \\times 3^3$ and $540 = 2^2 \\times 3^3 \\times 5$. The tile side is a common factor, and the largest is the HCF. The two share two 2s and three 3s, so it is $2^2 \\times 3^3 = 108$ cm." `feedback.generic`: "Not quite. Split both lengths into primes, then take the primes the two share." Keys unchanged.

9. `minor` | both problem sets and two exam items | a unit typed after the number.
   The numeric field strips a unit only when the part has a `unit` or the unit has two letters. So "45 m" (`p-meshing-gears` part 4, "to the nearest metre"), "10 m" (`quadratics` `p-park-pond` part 1), "23.328 m²", "28.27 m²", "89.375 m^3", and on the exams "234 m²", "234 square metres" (the placeholder's own words) and "199 m²" do not parse: the field shows "Type a number, a fraction ..." and will not submit (11 probe rows). "108 cm", "20 km/h" and "8 km/h" pass. Nothing is marked wrong, but the learner is stopped with a line that does not name the cause. The Fluency families set `unit` and take all of these.
   Fix: add `"unit"` to the widget: `"m"` on `p-meshing-gears` part 4 and `p-park-pond` part 1; `"cm"` on `p-hall-tiles` part 1; `"m²"` on `p-hall-tiles` part 4, `p-lawn-pond` parts 1 and 2, `e-plan-hall` and `e-pit-area`; `"m³"` on `p-storage-crate` part 5; `"km/h"` on `p-cycle-commute` part 4 and `p-windy-ride` part 3; `"m/s"` on `p-cycle-commute` part 5. On the two exam items change `placeholder` to "a number". See Engine for words such as "square metres".

10. `minor` | `p-meshing-gears` | part 4, chain.
    Part 4 says "Using 240 turns a minute". No part asks for 240: it appears only inside part 3's feedback, and part 4 uses none of the three graded answers before it. The last part is a side branch, not the result the problem is about (the meetings a minute, part 3).
    Fix, least change: part 4 `question` "The small gear turns 4 times a second, so $4 \\times 60 = 240$ times a minute. It is 6 cm across. How far does a tooth tip travel in a minute? Give the distance to the nearest metre." A fuller fix swaps parts 3 and 4, so the turns a minute are graded first and the meetings a minute close the problem; the numbers allow it but the `-carried` entries would need rewriting.

## C. `quadratics/problems-4.json`

Coverage holds: l14 (surd form, `p-park-pond` part 4), l15 (dividing and cancelling), l16 (adding and solving, the rejected root), l17 (factor theorem, division), l18 (distance, circle equation), l19 (line meets circle, tangent by the discriminant). All 15 parts are typed. Every later part of `p-park-pond` and `p-storage-crate` carries what it needs.

11. `unclear` | `p-storage-crate` | part 2 | `question` and `form`.
    "Divide $V(x)$ by $(x + 2)$ and give the quotient." A learner who gives the quotient as `(x+3)(x-1)` is refused with "That is equal, but give the quotient multiplied out". The question names no form, and part 3 then asks for exactly that factorising.
    Fix: `question` "Using $V(-2) = 0$, $(x + 2)$ is a factor. Divide $V(x)$ by $(x + 2)$ and give the quotient, multiplied out." (`form` stays; with no `form` the division typed back would pass, `windy-form.mjs`.)

12. `minor` (known fault, sized) | `p-windy-ride` | part 4 | no `form`.
    Confirmed. The part asks for "one fraction in $v$, in its simplest form" and grades by value only, so every equal expression passes (`windy-form.mjs`):

    | typed | now | with `form: "simplified"` |
    |---|---|---|
    | `\frac{9}{v-2}\div\frac{16}{v}` (the division of the question) | correct | correct |
    | `\frac{\frac{9}{v-2}}{\frac{16}{v}}` | correct | correct |
    | `\frac{9}{v-2}\times\frac{v}{16}` (flipped, not multiplied) | correct | correct |
    | `\frac{18v}{32(v-2)}`, `\frac{144v}{256(v-2)}` (not lowest terms) | correct | correct |
    | `\frac{9v^2}{16v(v-2)}`, `\frac{9v(v-2)}{16(v-2)^2}` (not cancelled) | correct | `form` |
    | `\frac{9v}{16(v-2)}`, `\frac{9v}{16v-32}`, `\frac{9}{16}\cdot\frac{v}{v-2}` | correct | correct |

    Size: one part of 15. A learner who divides is graded rightly, and the two real slips (`not-flipped`, `upside-down`) land on their keys. But the part can be passed with no work at all by typing the two times with a division sign, and "flip and multiply" can stop before any multiplying. `simplified` closes two of the seven unfinished forms; `factorised`, `fraction` and `expanded` refuse the key itself. No form closes the rest (Engine; already in the inbox from the author).
    Fix now: add `"form": "simplified"` and `byKey` `"form": "That is equal, but cancel what the top and bottom share and write one fraction."` Restate what the part needs, which it does not at present: `question` "The time out is $\\dfrac{16}{v}$ hours and the time home is $\\dfrac{9}{v - 2}$ hours. Write the time home divided by the time out as one fraction in $v$, in its simplest form."

13. `minor` | `p-windy-ride` | part 1 | the whole fraction.
    "Type the top, simplified." A learner who types the whole fraction, `\frac{25v-32}{v(v-2)}`, gets "Not quite. Multiply each top by the bracket its fraction lacks, then add", which they did. This is finding 8 of `review-quadratics-4.md`, fixed in l16 and review-4 with a `whole` entry.
    Fix: add to `wrong` `{ "id": "whole", "tex": "\\frac{25v-32}{v(v-2)}" }` and `byKey` `"whole": "That is the whole fraction, and it is right. Type only the top."` Tried in `windy-form.mjs`: the whole fraction, with the bottom in either form or the top not collected, lands on `whole`; `25v-32` still grades correct.

14. `minor` | `p-windy-ride` | parts 4 and 5 | chain.
    The problem is about the speed, which part 3 gives. Parts 4 and 5 are added to draw on l15, and part 5 ("how many times as long") needs neither: $1.5 \div 2 = 0.75$ from part 3's speeds, as the part's own explanation checks. So the last part is not the result the problem is about, and part 4 uses no earlier answer.
    Fix: none needed if finding 12's question is taken, which at least ties part 4 to part 1's two fractions. A fuller fix moves the ratio first (parts: ratio as one fraction, total time over a common bottom, both values of $v$, the speed, the ratio at that speed), which keeps every key.

Freshness note, no change asked: `p-park-pond` and the new exam item `e-diameter-ends` both end on a radius of 10 and a right side of 100, from 6, 8, 10 and 12, 16, 20. The settings and centres differ.

## D. Fluency sets

All 640 answers agree with mine from the prompt text; every `wrong` value is the slip its line names; a dropped `wrong` entry is dropped only where it would sit on the answer or on another entry (checked draw by draw). Shapes can exist: every slant side is longer than the height. Typing the question back is refused in every `divide-and-cancel`, `multiply-and-cancel`, `cancel-common-bracket` and `quotient` draw.

15. `unclear` | `number-sense/fluency-l19-one-number-for-many.json` | family `table-mean` | `prompt`.
    "Calls counted over $19$ hours: 0 in $5$ hours, 1 in $1$, 2 in $7$, 3 in $3$ and 4 in $3$." "2 in 7" reads as 2 calls in 7 hours as readily as 7 hours with 2 calls each, and "1 in 1" is hard to read at all. The table of the lesson is gone and nothing says which number is the value and which the count.
    Fix: `prompt` "{tcap} {one}, counted over ${n}$ {unit}: ${f0}$ {unit} had 0, ${f1}$ had 1, ${f2}$ had 2, ${f3}$ had 3 and ${f4}$ had 4. Find the mean number of {thing} {one}, to 2 decimal places." (reads "Calls an hour, counted over 19 hours: 5 hours had 0, 1 had 1, 7 had 2, ...").

16. `unclear` | `quadratics/fluency-l17-dividing-polynomials.json` | family `quotient` | `prompt` and `form`.
    The same fault as finding 11. "What is the quotient?" with `form: "expanded"`: where the quotient factorises over the whole numbers (31 of 200 draws; 2 of the 20 read, such as $x^2 - 3x - 4$), `(x-4)(x+1)` is refused.
    Fix: `prompt` "Divide ${poly(v; 1, b2, b1, b0)}$ by $({v}{na:+})$. Give the quotient multiplied out."

17. `minor` | `quadratics/fluency-l16-adding-and-solving.json` | families `add-tops` and `subtract-tops` | `form: "simplified"`.
    The top has a common whole-number factor in 88 and 90 of 200 draws. Typed with the factor taken out, it is graded unevenly: `8(y-3)` passes for $8y - 24$, while `2(4x-13)` for $8x - 26$ and `3(2t-3)` for $6t - 9$ get "That is equal, but simplify" (6 of 10 such draws of `add-tops`, 3 of 5 of `subtract-tops`). Both are simplified in any sense the prompt gives.
    Fix in content: `prompt` ends "Type the top, simplified, with no brackets." in both families, so the refusal matches what was asked. The uneven verdict itself is an engine matter (Engine).

18. `minor` | the same two families | the whole fraction.
    As finding 13: the whole fraction typed gets the generic line. `cancel-common-bracket` in the l15 set already has a `whole` entry.
    Fix: add to `wrong` in both `{ "id": "whole", "tex": "\\frac{{{poly(v; m, c0)}}}{{({v}{a:+})({v}{b:+})}}", "line": "That is the whole fraction. Type only the top." }`

19. `minor` | `quadratics/fluency-l14-roots-that-stay.json` | family `conjugate-bottom` | `prompt` and `where`.
    "What whole number is the new bottom?" The answer is below 0 in 17 of 200 draws ($2 - \sqrt{13}$ gives $-9$): 9 of the 64 pairs. The course uses "whole number" for counts, and a learner may well give 9.
    Fix: add `"p*p > q"` to `where` (55 pairs stay, every bottom 1 or more; `proposed.py`). Or keep the draws and end the prompt "What number is the new bottom? It may be below zero."

20. `minor` | `number-sense/fluency-l16-shared-factors.json` | family `other-number` | `where`.
    In 56 of 200 draws the given number is the HCF itself ("The HCF of $15$ and another number is $15$, and their LCM is $180$"), so the answer is the LCM printed in the prompt and no step is needed. That is more than a quarter of the family.
    Fix: add `"a > 1"` to `where`. The pairs with `a` equal to 1 stay in `hcf` and `lcm`, where one number dividing the other is a case worth meeting (47 and 51 of 200).

21. `minor` | `number-sense/fluency-l15-building-blocks.json` | family `count-factors` | `wrong` `no-plus-one`.
    When every index is 1 (34 of 200 draws, such as $78 = 2 \times 3 \times 13$) the entry's value is 1 and its line says "You multiplied the indices of $2 \times 3 \times 13$". No learner answers that a number has one factor, and no index is on show. The entry is dead in those draws.
    Fix: add `"when": "mul > 1"` to the entry.

Notes, no change asked. `find-k`: the `sign` slip gives a value of $k$ that is not whole in 3 of 20 draws ($-\tfrac{13}{3}$); its band of 0.01 takes $-4.33$ and `-13/3`. `collect-surds`: $k$ is below 0 in 5 of 20 draws ($\sqrt{20} - \sqrt{125} = -3\sqrt5$), which is sound and worth practising. `mean`: 9 of 20 draws hold two losses and `loss-added` flips the one its line names. `reject-root` prints a top such as $-9x$, which is correct. `circle-area` with the radius given has one `wrong` entry only.

## Engine

- The typed-back division of finding 12 needs a `form` for one algebraic fraction with no factor shared by top and bottom. Already raised by the author under "Raised later (fluency and problems quadratics 4)"; this read adds the table of what `simplified` does and does not close.
- `form: "simplified"` gives two verdicts for the same shape: a whole number times a bracket passes or fails by the node count of the Compute Engine's own simplification (`8(y-3)` passes, `2(4x-13)` does not). Finding 17.
- A numeric field with no `unit` will not submit a number followed by a one-letter unit, a unit with a power, or unit words ("45 m", "23.328 m²", "89.375 m^3", "234 square metres"), and its help line does not say why. Finding 9.
- `fresh-check.mjs` passed the two story reuses of findings 6 and 7 (a pond a given distance across; a hall's floor area): it matches runs of words, and both reuses change every number and most words.

All four are appended to `docs/BACKLOG-INBOX.md` under "Raised later (review holes 0.1 and 0.2)", the first as a cross-reference, with the candidate validator rules of the Counts section as a fifth bullet.

## Counts

| group | wrong | unclear | minor |
|---|---|---|---|
| A. exam items and skill tags (findings 1 to 5) | 0 | 1 | 4 |
| B. `number-sense/problems-4` (6 to 10; 9 also touches `quadratics/problems-4` and two exam items) | 0 | 0 | 5 |
| C. `quadratics/problems-4` (11 to 14) | 0 | 1 | 3 |
| D. Fluency sets (15 to 21) | 0 | 2 | 5 |
| total | 0 | 4 | 17 |

Finding classes seen three times or more:

- The `form` check and the question's words disagree, five times: an entry in a form the question never ruled out is refused (11, 16, 17), or an unfinished entry passes (12, and finding 19 of `review-quadratics-4.md`). Candidate validator rule: an `expression` with `form: "expanded"` whose prompt has none of "multiplied out", "expand" or "no brackets"; and a prompt with "simplest form" or "one fraction" on an `expression` with no `form`.
- The whole fraction typed where only the top is asked gets the generic line, three times here (13, and both families of 18) after four in `review-quadratics-4.md` finding 8. Candidate rule: a prompt with "Type the top" needs a `wrong` entry with id `whole`.
- A unit after the number stops the field, on 8 parts (9). Candidate rule: a numeric part or item whose question names a unit ("in metres", "in m²", "km an hour") and has no `unit`.
- Story reuse the freshness tool cannot see, three times (6 twice over, 7).

## Fix pass

Fix agent, Sonnet. Every changed number was recomputed twice before it was written (the author's scripts, now updated, run two routes each; `mine-after.py`, the reader's `mine.py` retyped for the new items, is a third). Directions from the main session replaced the reader's wording where they differ; each such line says so. Disputed: none.

Findings, one line each.

1. `e-diameter-ends` fixed, by a different route from the reader's. The item no longer needs a midpoint: the prose gives the ends $A(-4, -6)$, $B(6, 18)$ and the centre $C(1, 6)$, and the learner types the circle's equation (radius from the distance rule, then $(x - a)^2 + (y - b)^2 = r^2$, both taught in quadratics l18). New numbers as well (5-12-13, radius 13, so the radius and 100 of `p-park-pond` are no longer shared): $\sqrt{5^2 + 12^2} = 13$, and half of $\sqrt{10^2 + 24^2} = 26$; $A$ and $B$ satisfy $(x - 1)^2 + (y - 6)^2 = 169$. The three table cells became one `expression` with `accept` `x^2+y^2-2x-12y-132=0` ($1 + 36 - 169 = -132$, checked on a lattice) and wrong entries `signs`, `radius-not-squared` (13) and `full-diameter` (676, 26 squared). Skill `quad-graph`, title and id kept.
2. `e-pit-area` fixed: `rounded-radius` 201 (band 200.5 to 201.5; $\pi \times 8^2 = 201.06$, 200.96 with 3.14) with its `byKey` line.
3. `e-feed-updates` fixed: `six-fifty` 369,000 ($15 \times (6 \times 3600 + 50 \times 60)$, and by counting seconds) with its line.
4. `e-five-counts` fixed: title "Four summaries, five days".
5. Names: not edited (`course.json` is out of scope). Proposed for the main session, ids unchanged: `quad-graph` "Parabolas and circles" in `quadratics/course.json` and the `skills` map of `topic-0.2.json`; `ns-powers` "Powers, roots and primes" in `number-sense/course.json` and the `skills` map of `topic-0.1.json`. The four files must change together.
6. `p-lawn-pond` fixed with a new setting and new numbers: a 14 m by 11 m courtyard with a round basin 5 m across, sealant in tins of 15 m². Basin area $\pi \times 2.5^2 = 19.63$ (3.14 gives 19.625, 22/7 gives 19.64, all inside 0.02); paving $154 - 19.63 = 134.37$; $134.37 \div 15 = 8.96$, so 9 tins (9 tins cover 135). Wrong values: diameter slip 78.54, circumference 15.71, circumference carried 138.29 (10 tins), perimeter slip 30.37, rounded down 8, whole courtyard 154 (11 tins). The words are not used elsewhere in the course (searched).
7. `p-hall-tiles` fixed, new setting and numbers: a kitchen floor 360 cm by 600 cm (HCF 120, LCM 1,800, 16 sides, 15 tiles, 21.6 m²). Part 1 `missing-prime` 24 (drops the shared 5), part 2 wrongs 3, 8, 36, part 3 wrongs 8 and 375 (24 cm tiles), part 4 wrongs 2,160 and 216,000. Part 4 now asks for the area "as a decimal" (21.6 is exact, so the 3 decimal places went).
8. `p-hall-tiles` fixed: the prose no longer gives the prime forms; part 1's `explain` splits 360 and 600 into primes, and its `generic` says so. The difficulty stays 5.
9. Units fixed, with `unit`: `m` on `p-meshing-gears` 4 and `p-park-pond` 1; `cm` on `p-hall-tiles` 1; `m²` on `p-hall-tiles` 4, `p-lawn-pond` 1 and 2, `e-plan-hall`, `e-pit-area`; `m³` on `p-storage-crate` 5; `km/h` on `p-cycle-commute` 4 and `p-windy-ride` 3; `m/s` on `p-cycle-commute` 5. Both exam placeholders are now "a number". Closed for "234 m²", "45 m", "10 m", "89.375 m³", "20 km/h" (`grade-probe-after.mjs`). Still open, engine only: a unit with a caret or in words ("m^2", "m^3", "234 square metres", "234 sq m") still stops the field, 9 probe rows; a placeholder no longer invites it. Already in the inbox (Engine, third bullet).
10. `p-meshing-gears` fixed, least change: part 4 now reads "The small gear turns 4 times a second, so $4 \times 60 = 240$ times a minute." The part swap was not made.
11. `p-storage-crate` part 2 fixed: "Divide $V(x)$ by $(x + 2)$ and give the quotient, multiplied out." `form` stays `expanded`, so `(x+3)(x-1)` is refused for a reason the question gives.
12. `p-windy-ride` part 4 fixed, by the main session's route. No existing `form` can check one fraction in lowest terms, so the part asks for the top alone: "Divide the time home by the time out and write it as one fraction with bottom $16(v - 2)$. Type the top." Key $9v$ (`accept` `9*v`). Typed back, the division, the fraction over a fraction, the flipped product and the unfinished fractions are all refused (probe: key `whole`); only an expression equal to $9v$ passes. Entries `not-flipped` (144), `dropped-v` (9) and `whole`, each with a line. The top by sympy and at five points ($v$ = 3, 5, 8, 11 and 1/3). No `form`.
13. `p-windy-ride` part 1 fixed: `whole` entry and line (lands on `whole` for the bottom as $v(v - 2)$ or $v^2 - 2v$, or the top uncollected); `25v-32` still correct.
14. `p-windy-ride` chain: taken as the reader allows. Part 4 restates the two times from part 1 and the division of them; the order of the parts is not changed.
15. `table-mean` fixed: "Calls an hour, counted over 19 hours: 5 hours had 0, 1 had 1, 7 had 2, ...". The author's script now reads the five counts back from the prompt text.
16. `quotient` fixed: "... Give the quotient multiplied out." The reader's probe still lists `(x-4)(x+1)` refused; that is what the prompt now asks for.
17. `add-tops` and `subtract-tops` fixed in content: the prompt ends "Type the top, simplified, with no brackets." The uneven verdict of `form: "simplified"` (`8(y-3)` passes, `2(4x-13)` does not) is an engine matter, deferred, already in the inbox.
18. `add-tops` and `subtract-tops` fixed: `whole` entry and line in both; the probe no longer lists the whole fraction.
19. `conjugate-bottom` fixed: `where` gains `p*p > q` (every new bottom is 1 or more; 55 pairs stay).
20. `other-number` fixed: `where` gains `a > 1` (the given number is never the HCF itself, so the LCM printed is never the answer).
21. `count-factors` fixed: `no-plus-one` gets `when: mul > 1`.

Counts: 21 findings read; 20 fixed in the files; 1 (finding 5, names) proposed only, as `course.json` is out of scope; 0 disputed; deferred to the engine: the residual unit spellings (finding 9) and the uneven `simplified` verdict (finding 17).

Graded answers, tolerances and forms that changed (the whole list):

- `p-hall-tiles`: all four keys, from 108, 12, 20 and 23.328 to 120, 16, 15 and 21.6 (new story and numbers, finding 7). Part 4 tolerance stays 0.0005. Wrong ids and values replaced as in finding 7. `unit` `cm` and `m²` added.
- `p-lawn-pond`: all three keys, from 28.2743, 79.73 and 4 to 19.635, 134.37 and 9 (new story and numbers, finding 6). Tolerances 0.02, 0.02 and 0, as before. Wrong id `whole-lawn` renamed `whole-courtyard`; values replaced. `unit` `m²` on parts 1 and 2.
- `p-windy-ride` part 4: the graded answer changed from the fraction $\dfrac{9v}{16(v - 2)}$ (accept `\frac{9v}{16v-32}`) to the top $9v$ (accept `9*v`); `upside-down` entry removed, `dropped-v` and `whole` added, `not-flipped` now 144; no `form` before or after. Part 1 gains `whole`. Part 3 gains `unit` `km/h`.
- `p-storage-crate` part 2: question wording only, `form` `expanded` unchanged. Part 5 gains `unit` `m³`.
- `p-park-pond` part 1, `p-meshing-gears` part 4, `p-cycle-commute` parts 4 and 5: `unit` added (`m`, `m`, `km/h`, `m/s`); keys and bands unchanged.
- `e-diameter-ends`: the table of three numeric cells (1, 10, 10) became one `expression` keyed `(x-1)^2+(y-6)^2=169`, `accept` `x^2+y^2-2x-12y-132=0`; wrong entries `signs`, `radius-not-squared`, `full-diameter`; no `form`.
- `e-plan-hall` and `e-pit-area`: `unit` `m²` added, placeholder "a number". `e-pit-area` gains wrong `rounded-radius` 201 (band 0.5). `e-feed-updates` gains wrong `six-fifty` 369,000 (band 0.5).
- Fluency: `quotient` prompt now says "multiplied out" (`form` `expanded` unchanged); `add-tops` and `subtract-tops` prompt now says "with no brackets" (`form` `simplified` unchanged) and each gains `whole`; `conjugate-bottom` and `other-number` draw fewer pairs (`where`); `count-factors` `no-plus-one` is dropped when every index is 1; `table-mean` prompt reworded (answer and bands unchanged).

Gates.

- Number scripts, scratchpad venv, all exit 0: `exam-0.1-holes` 101 of 101; `exam-0.2-holes` 57 of 57; `problems-number-sense` 286 checks, 0 failures; `problems-quadratics` 874, 0; `fluency-number-sense` 55,829 of 55,829; `fluency-quadratics` 57,931 of 57,931. Each script now checks the new values (a reverted fix fails) and the new prompts and units.
- Reader's scripts rerun. `grade-probe.mjs` and `mine.py` hold the old values of the items rewritten above, so they were rerun as retyped copies (`grade-probe-after.mjs` and `mine-after.py` in the scratchpad `fix/` folder, not committed; new rows for every changed part): `mine-after.py` 329 checks, 0 failures; `grade-probe-after.mjs` 579 checks, 0 findings, 9 rows refused only for the unit spellings of finding 9. `fluency-probe.mjs` over fresh draws (`draw.sh`): 2,793 checks, 0 failures; the whole-fraction rows are gone, and the only classes left are those the prompts now justify (`quotient` typed factorised, `add-tops` with a bracketed factor) and the engine item. `fluency-read.py`: 3,504 checks; its only failures are its own old regexes (the `table-mean` wording, and the `no-plus-one` key it expects on draws where the entry is now dropped); the `other-number` and `conjugate-bottom` notes are gone.
- Validator: 0 errors; no warning on any file in scope beyond the two old ones on `topic-0.2` (`e-formula`, `e-gap-table`); `manifest.json` unchanged.
- Playthrough with `--local-cdn`, desktop and `--mobile`: `--exam topic-0.1`, `--exam topic-0.2`, `--problems number-sense/problems-4`, `--problems quadratics/problems-4`, and `--fluency` for l15, l16, l19 (number-sense) and l14, l16, l17 (quadratics): all passed. `node tools/test-fluency.mjs --local-cdn`: 1470 of 1470.
- Voice scan 35: 0 sentences over 35 words, 0 explanations over three sentences. `fresh-check.mjs`: 0 hits on both sets and both exams; advisories are the shared prime form $2^3 \times 3 \times 5$ (a distractor of `r-primes-180`), "600 120" in an unrelated estimate screen of l13, 3 numbers shared with a mock, and $x^2 + 5x + 6$ in l15 (as before).
