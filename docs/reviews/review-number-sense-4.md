# number-sense level 4 (Factors, measures and averages): second-reader findings

Scope: `l15-building-blocks`, `l16-shared-factors`, `l17-around-and-inside`, `l18-circles-and-units`, `l19-one-number-for-many`, `review-4`, `homework-4` in `app/content/courses/number-sense/`. Continuity skim: the level map in `course.json`, the cross-references to levels 1 and 2, topic exam `topic-0.1`.

Method: every screen and item worked from its text before its answer was read. Every key, `wrong[]` value and number in prose, hints, feedback and explanations recomputed by a second route in `docs/reviews/number-sense-4-scripts/read-numbers.py` (trial division and factor lists, set intersections for HCF and LCM, the shoelace formula on the drawn vertices, the expanded frequency lists, integer and `Fraction` arithmetic). The same script probes every π item with the values a learner gets from π ≈ 3.14, 3.142 and 22/7, using the engine's own tolerance test (`grade.js` `within`). `dump.py` in the same folder is the reader used to print each file.

Format: `N. file | screen or item | tag | what is wrong | fix`. Tags: `wrong` = a wrong number, a false statement or wrong grading; `unclear` = teaching that misleads or uses something not yet taught; `minor` = wording, coverage, freshness.

## Tool results

- Author script `docs/reports/number-sense-L4-numbers.py`: exit 0, 452 of 452 checks.
- Reader script `docs/reviews/number-sense-4-scripts/read-numbers.py`: 101 of 106 checks pass; exit 1. The five failing checks are findings 1, 2, 3, 5 and 6 below and pass once those are fixed. It prints one note for finding 9.
- Validator: 0 errors; no warning names a level 4 file.
- Voice scan (`voice-scan.py 35`): 0 explanations over three sentences, 0 sentences over 35 words. No exclamation mark, em-dash or en-dash; spelling British.
- Playthrough with `--local-cdn`: all five lessons, `review-4` and `homework-4` pass, with and without `--mobile`. Screenshots at 440 px read for l15 s5, l16 s3, l17 s8, l18 s2, l19 s0 and s9: no layout fault.

## Definitions (checked across lessons, review and homework)

All exact and consistent: a prime has exactly two factors, so 1 is not prime and 2 is the only even prime (l15 s3, s6, summary); factor against multiple (l15 s1); HCF as the overlap and LCM as every region once, with the edge cases 8 and 15, 6 and 18 (l16, quiz); HCF × LCM = product for two numbers (l16 s9, review, homework); the height at right angles for triangle, parallelogram and trapezium (l17); π as round ÷ across, 22/7 as an approximation that recurs, π neither ending nor recurring (l18 s1, quiz); 1 m² = 10,000 cm² (l17 s7, l18 s6); mean, median of an even count as the mean of the middle two, two modes and no mode, range with a negative smallest value (l19, quiz); frequency-table mean and median by counting days (l19 s6, review, homework). No algebra is asked for; letters appear only as labels after the words.

## Findings

1. `l18-circles-and-units.json` | `screens[7]` trap, `widget.wrong[2]` `two-r` (62.83) and `feedback.byKey.two-r` | wrong | The feedback says "You doubled the radius instead of squaring it. $5^2 = 25$." Doubling the radius gives $\pi \times 10 = 31.42$, which is the `circumference` entry. 62.83 is $2 \times \pi \times 10$: the circumference rule with the diameter used as the radius. The learner is told they did something they did not. | Keep the value; replace the text with: "You worked out $2 \times \pi \times 10$: the distance-round rule, with the diameter in place of the radius. For the area, halve 10 and square it: $\pi \times 5^2$."

2. `l19-one-number-for-many.json` | `quiz[3]` `q-range`, `widget.wrong[1]` `first-last` (55) | wrong | The feedback says "You used the first and last values listed." The first and last are $-15$ and 25, which give $25 - (-15) = 40$. The value 55 is $40 - (-15)$, the largest minus the first loss listed. So the described slip (40) gets the generic message and 55 gets a false description. | Set `"value": 40` and keep the text.

3. `review-4.json` | `items[6]` `r-circle-14`, `widget.tol` | wrong | The key 153.94 with `tol.abs` 0.01 rejects 153.86 (π ≈ 3.14, which l18 s1 says "is fine") and 154 (22/7 on a diameter of 14, the value the lesson's "handy fraction" invites). Both get "Halve the diameter, square it, multiply by π", which is what the learner did. Every other π item accepts the 3.14 value (script probe). | `"tol": {"abs": 0.1}`; `"accept": "153.94 cm²: $49\\pi$. 153.86 from $\\pi \\approx 3.14$ and 154 from $\\tfrac{22}{7}$ are accepted."`; widen the two wrong entries so the same learner still gets their message: `diameter` `"tol": {"abs": 0.35}` (615.44 and 616), `circ` `"tol": {"abs": 0.05}` (43.96 and 44).

4. `l16-shared-factors.json` | `screens[9]` derive, `widget.same` | unclear | The order `c84, c120, def, prod, same, end` is a valid argument (the definition line is needed only by `same`), yet it is marked wrong, because `same` only lets `c84` and `c120` swap. | Replace `"same": [["c84", "c120"]]` with `"after": {"prod": ["c84", "c120"], "same": ["def"], "end": ["prod", "same"]}` (AUTHORING, `order`, item 616). `answer` stays as it is and satisfies the rules.

5. `homework-4.json` | `items[5]` `h-euclid`, line `bad` | unclear | "1,071 take away one 462 leaves 609, so carry on with 462 and 609" is true and still reaches the HCF (the HCF of 609 and 462 is 21). It is slower, not a line that "does not follow", and a learner who knows subtraction keeps common factors is right to keep it. | Replace the line with a false one. Text: "The first remainder is 147, so the HCF of 1,071 and 462 is 147." `why`: "147 does not divide 462: $3 \\times 147 = 441$ leaves 21. Carry on until nothing is left." `feedback.byKey.bad`: "147 is only the first remainder. It does not divide 462."

6. `homework-4.json` | `items[6]` `h-long-leaflet`, `model`, first paragraph | unclear | "So months that differ by 15% look as if one is about 60% bigger." Per cent is not taught until `ratio` level 1 (the brief rules it out), and it is the only per cent sign in the level. | "So a month that is 1.15 times another looks 1.6 times as big." (23 ÷ 20 = 1.15; drawn heights 8 ÷ 5 = 1.6; both recomputed.)

7. `l15-building-blocks.json` | `screens[6].hints[1]`, `quiz[1]` option `odd` `why`, `quiz[1].explain` | unclear | The digit-sum test for 3 is used as a reason ("Its digits add to 15, so 3 divides it") and is taught nowhere in levels 1 to 4. | Hint: "A number divides by 3 when its digits add to a multiple of 3: $5 + 1 = 6$ and $5 + 7 = 12$." Option `why`: "Being odd only rules out 2. Try 3: $3 \\times 29 = 87$." Explain: "Dividing by 3 works: $87 = 3 \\times 29$. So 87 is composite, although it is odd and not in the 7 times table."

8. `l16-shared-factors.json` | `screens[3].prose` | unclear | "Each prime of 84 or 120 goes in the diagram once" contradicts the diagram, where 2 appears three times. The rule for repeated primes is what the learner needs to read the overlap. | "For bigger numbers, use prime factors. Write out the primes of each number, repeats included. Each prime the two numbers share is paired off into the overlap; the rest stay on their own side."

9. `l19-one-number-for-many.json` | `screens[6]` frequency table, row `Median` | minor | With the brief's data the commonest slip (take the middle row of the table, 2) gives the key, and so does giving the mode. The data are the brief's, so keep them; make the method visible. | `feedback.correct`: "37 trades, mean 1.85, median 2, mode 2. The median comes from counting days, not rows: the 10th and 11th days." `homework-4` `h-freq` already separates the two (median 3, middle rows 2.5).

10. `l19-one-number-for-many.json` and `homework-4.json` | l19 `screens[4].explain`; homework `items[6]` model and `rubric[4]` | minor | The homework uses "outlier" twice; the lesson never names it (it says "extreme day"). | l19 `screens[4].explain`, third sentence: "One extreme day, an **outlier**, moves the mean a lot and the median not at all."

11. `l17-around-and-inside.json` | `summary.trap` | minor | "Cutting a corner out of a rectangle leaves its perimeter the same" is true for a rectangular notch only; a slanted cut shortens it. LEVEL-BRIEF asks rules to carry their conditions. | "Cutting a rectangular corner out of a rectangle leaves its perimeter the same: the L-shape is still 32 m round."

12. `l17-around-and-inside.json` | `screens[8].feedback.byKey.added` | minor | "You added the two growth factors" uses a term not taught before `ratio`. | "You added 1.1 and 1.1. Both sides grew, so multiply: $1.1 \\times 1.1$."

13. `l18-circles-and-units.json`, `review-4.json`, `homework-4.json` | l18 `screens[5].feedback.byKey.wrong-way`, `quiz[2]` `wrong-way`; review `items[7]` `wrong-way`; homework `items[2]` `wrong-way` | minor | "You multiplied by 3.6" names a number the lesson never forms. | l18 s5: "You multiplied by 3,600 and divided by 1,000. Turn both round: multiply by 1,000, divide by 3,600." Quiz and review: "You multiplied by 3,600 and divided by 1,000. Turn both round." Homework: "You divided by 3,600 and multiplied by 1,000. Turn both round."

14. `l18-circles-and-units.json` | `screens[2].canvas.left.state.shade` | minor | The circle shows its right-hand half in blue, four neighbouring wedges, while the strip alternates green and orange wedges. Nothing links the two pictures, and the shaded half is not the set of "up" wedges. | Remove `"shade": {"half": 0.5}` from the left canvas, or change the caption to "The wedges, laid head to tail: half point up, half point down."

15. `l19-one-number-for-many.json` | quiz (coverage against the brief) | minor | Two brief items are missing from the level: the trap "taking the middle of the unsorted list as the median" (every median screen shows sorted data) and reading a line chart. | Add a fifth quiz item `q-unsorted`, difficulty 2: prose "Five daily profits in pounds, in the order they happened: 70, $-20$, 10, 90, 30."; question "What is the median?"; `numeric`, answer 30, `tol.abs` 0, unit £; `wrong`: `unsorted` 10 ("10 is the middle of the list as written. Sort first: $-20$, 10, 30, 70, 90."), `mean` 36 ("36 is the mean, $180 \\div 5$. The median is the middle value after sorting."); explain "Sorted, the profits are $-20$, 10, 30, 70, 90. The middle one is 30, so the median is £30." The line chart needs a canvas decision and can wait for the problem set.

16. `review-4.json` | `items[3]` `r-cancel`, option `sub` ($\tfrac{3}{4}$) | minor | "You took 27 off the top and 38 off the bottom" is not a slip anyone makes. | Option text `$\\dfrac{1}{7}$`, `why`: "You divided the bottom by 6 but the top by 30. Divide both by 6." (matches l16 s5's `tops` slip).

17. `homework-4.json` and `review-4.json` | homework `items[2]` `h-speed`, `items[4]` `h-leaver`; review `items[4]` `r-l-shape` | minor | Freshness. `h-speed` (25 m/s to 90 km/h) is l18 quiz `q-90` run backwards with the same two numbers. `h-leaver` is review `r-remove` with the same answer digits (38 and 38,000). `r-l-shape` redraws l17 s5's figure with new lengths, which is fair practice and can stay. | `h-speed`: 35 metres a second, answer 126, `accept` "126 km/h: $35 \\times 3{,}600 \\div 1{,}000$", wrongs `wrong-way` 9.72, `minutes` 2.1, `no-km` 126000, and 35 and 126 in prose, question, feedback and explain. `h-leaver`: largest bonus £87,000, answer 39000 ($273{,}000 \\div 7$), wrongs `unchanged` 45000, `eight` 34125, `old-total` 51429; explain "Without the £87,000, seven bonuses total £273,000, so their mean is $273{,}000 \\div 7 = 39{,}000$ pounds."

18. `l15-building-blocks.json` | `screens[8]` line `small` | minor | "Times the smaller number by itself" uses "times" as a verb. | "Multiply the smaller number by itself: that is at most the smaller times the larger, which is 97."

19. `l16-shared-factors.json` | `screens[3].feedback.byKey.just-two` (value 2) | minor | "You used only the 2s you saw first" does not describe the value, which is a single 2. | "You used one 2 only. Multiply everything in the overlap: $2 \\times 2 \\times 3$."

20. `l18-circles-and-units.json` | `quiz[1]` `q-area-3`, `widget.tol` | minor | The key 28.27 with `tol.abs` 0.01 accepts 28.26 (3.14) but rejects 28.29 (22/7), the one π quiz value the lesson's own fraction fails. | `"tol": {"abs": 0.02}`.

## Counts

- wrong: 3 (findings 1 to 3)
- unclear: 5 (findings 4 to 8)
- minor: 12 (findings 9 to 20)

## Verdict by file

- `l15-building-blocks.json`: sound. One untaught rule used as a reason (7) and one wording point (18).
- `l16-shared-factors.json`: sound numbers. The derive screen marks a valid order wrong (4); one prose line contradicts its diagram (8); one feedback line (19).
- `l17-around-and-inside.json`: sound. Two wording points (11, 12).
- `l18-circles-and-units.json`: one wrong feedback entry (1); otherwise sound, with three minor points (13, 14, 20).
- `l19-one-number-for-many.json`: one wrong `wrong[]` value in the quiz (2); two brief items not covered (15); two minor points (9, 10).
- `review-4.json`: meets the counts (10 items, difficulty 2 to 4, `pass` 0.8, each lesson twice). One tolerance that marks a taught method wrong (3); two minor points (16, and 13).
- `homework-4.json`: meets the counts (8 items, difficulty 3 to 5 with two at 5, an `order` item, a longform with a 10-point rubric and full model). A distractor that is a valid step (5), a per cent sign (6), and freshness (17).

Freshness against `topic-0.1`: no exam item shares a setup or a number with the level. The level makes the four planned exam items answerable.

## Engine

- `numbers_lib` or the validator could probe π items: where a key is a multiple of π rounded to n places, warn when the value from π ≈ 3.14 or 22/7 falls outside the tolerance and matches no `wrong` entry (finding 3 was the one item of ten).
- `area` with `shape: "circle"` and `sectors` can shade a fraction of the disc but cannot colour alternate wedges, so the cut circle in l18 s2 cannot match the up and down wedges of the strip beside it (finding 14).
