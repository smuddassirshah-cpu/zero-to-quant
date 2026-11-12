# Problem sets 0.1, number-sense levels 1 to 3: second-reader findings

Scope: `app/content/courses/number-sense/problems-1.json`, `-2`, `-3`: 10 problems, 40 parts (38 numeric, 2 choice), 92 `wrong` values. Rules: `docs/briefs/chained.md`, `docs/briefs/second-read-reader-brief.md`. Pattern: `review-problems-1.4-c.md`.

Method. The author's script was run first. Each problem was read whole (`show.py` prints a set for reading) beside the 14 lessons, three reviews and three homework sets of the levels (`taught.py` prints where the course teaches a word or a sum). Every part was solved by hand from its text and again in `mine.py`, which imports nothing from the author's script and types every quantity from the prose. Route 1 is exact (`fractions`, `Decimal` rounding). Route 2 is another method: beds counted one by one, flour in twenty-fourths of a kilogram, a batch of 72 sheets, cordial in 144ths of a litre, temperatures in whole tenths, the 18 holes written out, money in pence, loops for the cube and the square, whole-number division for the probe. Every `wrong` value was rebuilt from the slip its line names, and every number printed in a `feedback`, `byKey`, `why` or `explain` string was recomputed while reading (the ones that carry an argument are asserted in `mine.py`). Every numeric part then went through the engine's own grader in node (`grade-probe.mjs`, `numGrade` of `app/js/engine/grade.js`): the key, each `wrong` value on its own id, and 215 strings of my own (fraction against decimal, a mixed number, an unreduced fraction, a true minus sign, a unit, thousands commas, more places, the answer one step short or one step ahead). `grade-probe.mjs --fix` applies the fixes below to in-memory copies and grades them; `proposed.py` computes their numbers twice. Reuse was read by hand, helped by `fresh.py` (key numbers and story nouns across all 2,452 content files) and `taught.py` (the sums themselves inside the course).

Tags: `wrong` = a learner is marked wrongly or told something false; `unclear` = the question can be read two ways, does not say the form wanted, uses a word the level has not taught, or refuses a sensible entry; `minor` = weak part, loose band, slip with no line, wording or reuse.

## Tool results

| check | result |
|---|---|
| author's script (scratchpad venv) | `problems-number-sense-numbers.py` 928 checks, 0 failures, exit 0 |
| `mine.py` (reader's keys, slips, stated numbers, bands, set shape) | 725 checks, 0 failures, exit 0 |
| `grade-probe.mjs` (engine grader, 38 numeric parts) | 345 checks, 215 reader rows, 0 failures; 18 rows held to be faults (findings 4, 5, 8, 10, 11, 12, 14) |
| `grade-probe.mjs --fix` (fixes of findings 1, 2, 4, 5, 8, 10, 11, 12, 14, 15 on in-memory copies) | 242 checks, 104 reader rows, 0 failures |
| `proposed.py` (numbers of the fixes, new numbers fresh in the course) | 31 checks, 0 failures; 2 notes read by hand |
| `grade-all.mjs --file`, three sets | 17, 12 and 11 widgets, 0 failures each |
| validator | 0 errors; no warning on the three files; `manifest.json` unchanged |
| voice scan 35, course folder | 0 and 0; no exclamation mark, no em-dash, British spelling, £ for money |
| `fresh-check.mjs --file`, three sets | 0 hits each (it cannot see findings 1, 2 and 15, which share numbers, not runs of words) |
| browser, `playthrough.mjs` | not run, as instructed |

Result. All 38 numeric keys and both choice keys agree with mine, and so do all 92 `wrong` values and every number in a feedback or explanation string. Every `wrong` value lands on its own id, no `wrong` band reaches a key band and no two overlap. No part marks a right answer wrong and no line states something false in its own setting, so no finding is tagged `wrong`. Three are `unclear`: a unit the question names is not read (8), a word taught two levels later (9), and a calculator question the lesson itself says has two answers (12). The 13 `minor` findings are three reuses of course numbers (one with a sentence shared word for word), two rounding parts that accept the value before rounding, five slips or forms with no line, and wording.

Counts: `problems-1` 0 wrong, 0 unclear, 7 minor. `problems-2` 0 wrong, 2 unclear, 2 minor. `problems-3` 0 wrong, 1 unclear, 4 minor.

## Findings

| id | file#item.part | tag | what is wrong | fix |
|---|---|---|---|---|
| 1 | `problems-1#p-garden-beds.1` | minor | same sum and numbers as l1 quiz 4 ($\tfrac{2}{5}$ of 20 is 8) | ask for the beans; text in A1 |
| 2 | `problems-1#p-rye-loaves` (part 3) | minor | $\tfrac{5}{6} - \tfrac{3}{4}$ is `homework-1` item 3, with one sentence word for word | loaf of $\tfrac{1}{5}$ kg; text in A2 |
| 3 | `problems-1#p-squash-jugs.2` | minor | the question hands over both renamed fractions; the judgement left is 16 against 15 | new question; A3 |
| 4 | `problems-1#p-squash-jugs.1` | minor | `16/36` typed whole gets the generic line, which names the step just done | one `wrong` entry; A4 |
| 5 | `problems-1#p-two-printers.3`, `.4` | minor | the right time in the other unit has no line | two `wrong` entries; A5 |
| 6 | `problems-1#p-squash-jugs` prose | minor | "hold" can be the size of the jug, not what is in it | new prose; A6 |
| 7 | `problems-1#p-rye-loaves.2` | minor | `carried` names one of the two part 1 slips that give 0 | new line; A7 |
| 8 | `problems-2#p-moor-weather.1`, `.4`, `p-taxi-split.3` (and all three sets) | unclear | no part has a `unit`; `1.3 °C` and `-2p` are not read as numbers | add `unit`; list in B8 |
| 9 | `problems-2#p-golf-card.2` | unclear | "mean" is first taught in l19 (level 4); level 2 says "average" | four strings; B9 |
| 10 | `problems-2#p-golf-card.3`, `p-taxi-split.2` | minor | the value before rounding is marked correct on a rounding part | tighter `tol` and an `unrounded` entry; B10 |
| 11 | `problems-2#p-taxi-split.2`, `.4` | minor | the answer in pence has no line | two `wrong` entries; B11 |
| 12 | `problems-3#p-stationery-bill.3` | unclear | l12 opens with two calculators that disagree; a left-to-right one shows 67.93 here | say which calculator; C12 |
| 13 | `problems-3#p-cube-tub` prose, part 1 | minor | "She" has no one to refer to | name her; C13 |
| 14 | `problems-3#p-comet-probe.3` | minor | 3.3 or 3.33 gets the generic line, which names the step just done | one `wrong` entry; C14 |
| 15 | `problems-3#p-cube-tub` | minor | 1,500 is the number of `homework-3` item 3 ($\sqrt{1{,}500}$), and the story is l11 quiz 5 | 2,169 cubes; text in C15 |
| 16 | `problems-3#p-comet-probe.1` | minor | generic line says "standard form", the question asks for the number in full | new line; C16 |

Paths below are JSON paths in the file. Fixes of findings 1, 2 and 15 change keys, so the fix agent also updates `docs/reports/problems-number-sense-numbers.py` for those items.

## A. `problems-1`

A1 (finding 1). `items[0].parts[0]`. l1 `quiz[3]` asks "How much is $\tfrac{2}{5}$ of £20?", key 8, slip 4. Part 1 asks the same sum on 20 beds, key 8, slip 4. Ask for the beans, which part 2 needs as well.
- `question`: "How many beds are beans?"
- `widget`: `answer` 5, `accept` "5", `wrong` `[{"id":"flipped","value":80,"tol":{"abs":0}},{"id":"three-quarters","value":15,"tol":{"abs":0}}]`
- `feedback.correct`: "One quarter of 20 beds is $20 \div 4 = 5$ beds."
- `feedback.generic`: "Not quite. Split the 20 beds into 4 equal groups, then take 1 of the groups."
- `feedback.byKey`: `flipped` "You worked out $20 \times 4$. A quarter of 20 is less than 20: $20 \div 4 = 5$." `three-quarters` "15 beds is the other three quarters. Beans fill one quarter: $20 \div 4 = 5$ beds."
- `explain.text`: "Cut the 20 beds into 4 equal groups of 5. One of those groups is beans. That is 5 beds."
- `items[0].parts[1].explain.text`: "One bed is $\tfrac{1}{20}$ of the garden. Beans take 5 beds and potatoes take $20 \div 5 \times 2 = 8$ beds. Together that is $\tfrac{8}{20} + \tfrac{5}{20} = \tfrac{13}{20}$."

A2 (finding 2). `items[1]`. `homework-1` `items[2]` is "What is $\tfrac{5}{6} - \tfrac{3}{4}$?", key $\tfrac{1}{12}$, slip `tops-bottoms` 1, with the explanation "Twelfths fit both: $\tfrac{5}{6} = \tfrac{10}{12}$ and $\tfrac{3}{4} = \tfrac{9}{12}$." Part 3 is the same subtraction with the same slip, and its explanation holds that sentence word for word. A loaf of $\tfrac{1}{5}$ kg keeps the story and every step (`proposed.py`; no sum of it is in the course):
- `prose`: "A baker has $\tfrac{5}{6}$ kg of rye flour. Each rye loaf needs $\tfrac{1}{5}$ kg of flour."
- Part 1. `question` "How many fifths of a kilogram fit into $\tfrac{5}{6}$ kg? Give an exact fraction or a mixed number." `answer` 4.166667, `accept` "Any form equal to $\tfrac{25}{6} = 4\tfrac{1}{6}$", `wrong` `multiplied` 0.166667, `wrong-flip` 0.24 (bands 0.0005 as now). `correct` "$\tfrac{5}{6} \div \tfrac{1}{5} = \tfrac{5}{6} \times 5 = \tfrac{25}{6} = 4\tfrac{1}{6}$." `generic` "Not quite. Count how many fifths fit: divide by $\tfrac{1}{5}$, which is the same as multiplying by 5." `multiplied` "You multiplied, which gives a fifth of the flour. To count how many fifths fit, divide: $\tfrac{5}{6} \times 5 = \tfrac{25}{6}$." `wrong-flip` "You flipped $\tfrac{5}{6}$ instead of $\tfrac{1}{5}$. Flip the fraction you divide by: $\tfrac{5}{6} \times \tfrac{5}{1}$." `explain` "Dividing by $\tfrac{1}{5}$ counts fifths, and each whole holds 5 of them. So $\tfrac{5}{6} \div \tfrac{1}{5} = \tfrac{5}{6} \times 5 = \tfrac{25}{6}$. That is $4\tfrac{1}{6}$."
- Part 2. `question` "Using $4\tfrac{1}{6}$ loaves' worth of flour, how many whole loaves can she bake?" `answer` 4, `accept` "4", `wrong` `rounded-up` 5, `carried` 0. `correct` "$4\tfrac{1}{6}$ is 4 wholes and a sixth more, so she can bake 4 whole loaves." `generic` "Not quite. A loaf needs a whole fifth of a kilogram, so only the whole part counts." `rounded-up` "A fifth loaf needs a full $\tfrac{1}{5}$ kg, but only a sixth of that is left. She bakes 4." `carried` "That follows from a part 1 answer below 1, such as $\tfrac{1}{6}$. Using $4\tfrac{1}{6}$, she has enough for 4 whole loaves." `explain` "$4\tfrac{1}{6}$ means 4 whole loaves' worth and $\tfrac{1}{6}$ of another. A sixth of a loaf's flour cannot make a loaf. She bakes 4."
- Part 3. `question` "Using 4 loaves, how much flour is left over, in kg? Give an exact fraction." `answer` 0.033333, `accept` "Any form equal to $\tfrac{1}{30}$", `wrong` `one-loaf` 0.633333, `tops-bottoms` 1, and `loaf-third` renamed `loaf-sixth` with value 0.166667. `correct` "4 loaves use $\tfrac{4}{5}$ kg. In thirtieths, $\tfrac{25}{30} - \tfrac{24}{30} = \tfrac{1}{30}$ kg." `generic` "Not quite. Find the flour the 4 loaves use, then take it from $\tfrac{5}{6}$ kg in thirtieths." `one-loaf` "You took away one loaf's $\tfrac{1}{5}$ kg. Four loaves use $\tfrac{4}{5}$ kg, which leaves $\tfrac{1}{30}$ kg." `tops-bottoms` "You took tops from tops and bottoms from bottoms: $\tfrac{5 - 4}{6 - 5}$. Rename in thirtieths: $\tfrac{25}{30} - \tfrac{24}{30}$." `loaf-sixth` "$\tfrac{1}{6}$ is the part of a loaf left over, not kilograms. A sixth of $\tfrac{1}{5}$ kg is $\tfrac{1}{30}$ kg." `explain` "Four loaves use $4 \times \tfrac{1}{5} = \tfrac{4}{5}$ kg. In thirtieths that is $\tfrac{24}{30}$, and $\tfrac{5}{6} = \tfrac{25}{30}$. So $\tfrac{1}{30}$ kg is left."
- Part 4. `question` "Using $\tfrac{1}{30}$ kg left over, what fraction of her starting $\tfrac{5}{6}$ kg is that? Give an exact fraction." `answer` 0.04, `accept` "Any form equal to $\tfrac{1}{25}$", `wrong` `multiplied` 0.027778, `flipped` 25, `carried` 0.76. `correct` "$\tfrac{1}{30} \div \tfrac{5}{6} = \tfrac{1}{30} \times \tfrac{6}{5} = \tfrac{6}{150} = \tfrac{1}{25}$." `generic` "Not quite. Ask how many times $\tfrac{5}{6}$ fits into $\tfrac{1}{30}$: divide, by flipping and multiplying." `multiplied` "You multiplied $\tfrac{1}{30}$ by $\tfrac{5}{6}$. To compare with the start, divide: $\tfrac{1}{30} \times \tfrac{6}{5} = \tfrac{1}{25}$." `flipped` unchanged but for the fraction: "You worked out $\tfrac{5}{6} \div \tfrac{1}{30}$. The leftover is the small part, so divide it by the start." `carried` "That is $\tfrac{19}{30} \div \tfrac{5}{6}$, from taking away one loaf. With $\tfrac{1}{30}$ kg left, the share is $\tfrac{1}{25}$." `explain` "A fraction of the start means the leftover divided by the start. So $\tfrac{1}{30} \div \tfrac{5}{6} = \tfrac{1}{30} \times \tfrac{6}{5} = \tfrac{6}{150}$. That is $\tfrac{1}{25}$ of her flour."
- If the orchestrator keeps the item, the least change is the shared sentence: part 3 `explain.text` "Three loaves use $3 \times \tfrac{1}{4} = \tfrac{3}{4}$ kg. In twelfths that is $\tfrac{9}{12}$, and $\tfrac{5}{6} = \tfrac{10}{12}$. So $\tfrac{1}{12}$ kg is left."

A3 (finding 3). `items[3].parts[1].question`. It gives $\tfrac{5}{12} = \tfrac{15}{36}$ and $\tfrac{16}{36}$, so the part asks whether 16 beats 15. Let the learner rename jug B, as part 1 taught: "Using $\tfrac{16}{36}$ for jug A, rename jug B's $\tfrac{5}{12}$ in thirty-sixths too. Which jug has the stronger mix?" The `why` lines, feedback and explanation already show $\tfrac{15}{36}$ and need no change.

A4 (finding 4). `items[3].parts[0]`. "How many thirty-sixths is it?" answered `16/36` is read as 0.444 and gets "Find what 9 is multiplied by to make 36, then multiply the top by the same number", which the learner has done. Add to `wrong`: `{"id":"whole-fraction","value":0.444444,"tol":{"abs":0.0005}}`, and `byKey.whole-fraction`: "That is the whole fraction, which still equals $\tfrac{4}{9}$. Type only the count of thirty-sixths: 16."

A5 (finding 5). `items[2].parts[2]` asks for hours and `parts[3]` for minutes. $46\tfrac{2}{3}$ on part 3 and $1\tfrac{7}{9}$ on part 4 are the right times in the other unit and get the generic line.
- Part 3 `wrong` add `{"id":"minutes","value":46.666667,"tol":{"abs":0.0005}}`; `byKey.minutes`: "That is the time in minutes. The question asks for hours: $\tfrac{7}{9}$ of an hour."
- Part 4 `wrong` add `{"id":"hours","value":1.777778,"tol":{"abs":0.0005}}`; `byKey.hours`: "That is the whole time in hours, $1\tfrac{7}{9}$. In minutes it is $60 + 46\tfrac{2}{3} = 106\tfrac{2}{3}$."

A6 (finding 6). `items[3].prose`. Part 3 needs the jug to be full. "A café mixes squash in two jugs. Each jug is full and holds $\tfrac{3}{4}$ litre. In jug A, $\tfrac{4}{9}$ of the drink is cordial. In jug B, $\tfrac{5}{12}$ of the drink is cordial."

A7 (finding 7). `items[1].parts[1].feedback.byKey.carried`. The value 0 also follows from $\tfrac{3}{10}$, the `wrong-flip` slip of part 1, and that learner is told they had $\tfrac{5}{24}$. "That follows from a part 1 answer below 1, such as $\tfrac{5}{24}$. Using $3\tfrac{1}{3}$, she has enough for 3 whole loaves." (Finding 2's text already has this form.)

## B. `problems-2`

B8 (finding 8). None of the 38 numeric widgets has a `unit`; `problems-4` (7 parts) and `review-2` (5 items) give one to measured answers, and the field then shows the unit beside it. Without it the grader drops only a unit of two letters or more. `items[0].parts[0]` asks for the reading "in °C": `1.3 °C` and `1.3°C` give no number, so Check stays unavailable (`grade-probe.mjs`); the same for `-7.8 °C` on part 4 and for `-2p` on `items[2].parts[2]`, which asks "in pence". With the unit set all of these are read (`--fix`). Add `"unit"` to the widgets:
- `problems-2`: moor parts 1 and 4 `"°C"`, parts 2 and 3 `"degrees"`; taxi parts 1, 2 and 4 `"£"`, part 3 `"p"`.
- `problems-1`: garden part 1 `"beds"`; rye part 2 `"loaves"`, part 3 `"kg"`; printers part 3 `"hours"`, part 4 `"minutes"`; squash parts 3 and 4 `"litres"`.
- `problems-3`: cube tub parts 1 to 3 `"cubes"`; stationery parts 1 to 4 `"£"`; comet parts 1 and 2 `"hours"`, parts 3 and 4 `"years"`.

B9 (finding 9). `items[1].parts[1]`. "Mean" is introduced in l19 screen 3 (level 4). Levels 1 and 2 never use it; l7 screen 12 and `review-2` say "average".
- `question`: "Using $-1$ for this round, her four rounds this week are $-1$, $+2$, $-6$ and $-3$. What is her average score a round, the total shared equally over the four rounds?"
- `feedback.byKey.plus-as-minus`: "You took the $+2$ as $-2$. With it added, the total is $-8$ and the average $-2$."
- `feedback.byKey.total`: "$-8$ is the total for the week. The average shares it over 4 rounds: $-8 \div 4 = -2$."
- `explain.text`: "Adding the rounds gives $-1 + 2 - 6 - 3 = -8$. Sharing $-8$ equally over 4 rounds gives $-8 \div 4$. A negative divided by a positive is negative, so the average is $-2$."

B10 (finding 10). Two parts whose whole step is the rounding accept the value before it.
- `items[1].parts[2]` ("Write $\tfrac{5}{18}$ as a decimal to 3 decimal places"): `5/18` typed back is 0.27778, inside $0.278 \pm 0.0005$, and is marked correct; so is 0.2778. Set `tol` to `{"abs":0.0001}`, add `wrong` `{"id":"unrounded","value":0.277778,"tol":{"abs":0.0001}}` and `byKey.unrounded`: "That is $\tfrac{5}{18}$ to more than 3 places. The 4th decimal is 7, so round the 3rd up: 0.278." `truncated` (0.277, band 0) still lands on its own line.
- `items[2].parts[1]` ("Using £2.8333, what is each share to the nearest penny?"): 2.8333, the value the question gives, is inside $2.83 \pm 0.005$ and is marked correct. Set `tol` to `{"abs":0.0005}`, add `wrong` `{"id":"unrounded","value":2.8333,"tol":{"abs":0.0005}}` and `byKey.unrounded`: "That is the share before rounding. The nearest penny keeps 2 decimal places: £2.83." l7 screen 12 has the same `unrounded` line.
- Both new entries hold more places than the question asks for, on purpose, so the validator's advisory `[wrong-band]` may fire on them (not run here, since content is not edited by the reader). If it does, record the two lines as judged; the band must stay narrow to keep 2.83 and 0.278 out.
- Read and left alone: `problems-3` stationery part 4 and comet part 4 take 67.9333 and 3.42. There the step is the division and the extra places are an honest answer.

B11 (finding 11). `items[2].parts[1]` and `parts[3]` ask for pounds straight after a part in pence; 283 and 285 get the generic line.
- Part 2 `wrong` add `{"id":"pence","value":283,"tol":{"abs":0}}`; `byKey.pence`: "That is in pence. The question asks for pounds: £2.83."
- Part 4 `wrong` add `{"id":"pence","value":285,"tol":{"abs":0}}`; `byKey.pence`: "That is in pence. In pounds the sixth friend pays £2.85."

## C. `problems-3`

C12 (finding 12). `items[1].parts[2]`. l12 screen 1 opens: "One calculator says $2 + 3 \times 4 = 20$. Another says 14." A learner who has just met that will ask which calculator the clerk has. One that works left to right shows $(38 \times 4.85 + 19.50) \div 3 = 67.93$; that entry lands on `intended`, which says "The calculator divides only the 19.50 by 3".
- `question`: "A clerk keys $38 \times 4.85 + 19.50 \div 3$ into a calculator that follows the order of operations, to find one office's share. What does the calculator show? Give the value in pounds."
- `feedback.generic`: "Not quite. This calculator follows the order of operations: × and ÷ before +."
- `feedback.byKey.intended`: "That is what the clerk meant. This calculator divides only the 19.50 by 3, so it shows 190.80."

C13 (finding 13). `items[0]`. The prose names a tub and part 1 begins "She glues". If finding 15 is not taken: `prose` "Asha's craft tub holds 1,500 small wooden cubes, all the same size." and `parts[0].question` "Asha glues cubes into the largest solid cube she can. How many small cubes long is each edge?"

C14 (finding 14). `items[2].parts[2]`. 3.3 and 3.33 get "Divide the hours by the hours in a year", which the learner did. Add `wrong` `{"id":"unrounded","value":3.33,"tol":{"abs":0.04}}` and `byKey.unrounded`: "You divided correctly: $30{,}000 \div 9{,}000 = 3.33\ldots$ Now round to 1 significant figure: 3."

C15 (finding 15). `items[0]`. `homework-3` `items[2]` is "What is $\sqrt{1{,}500}$ to one decimal place?" (38.7), and this problem's `square-root` slip is that answer. l11 `quiz[4]` is "A cube is built from 8,000 small cubes. How many small cubes run along one edge?" The story is the plain model of a cube and can stay; the number should change. 2,169 cubes give edge 12, 441 left and a square of side 21 (`proposed.py`):
- `prose`: "Asha's craft tub holds 2,169 small wooden cubes, all the same size."
- Part 1. `question` "Asha glues cubes into the largest solid cube she can. How many small cubes long is each edge?" `answer` 12, `accept` "12", `wrong` `rounded-up` 13, `square-root` 46 (band 1), `thirds` 723. `correct` "$12^3 = 1{,}728$ and $13^3 = 2{,}197$, so 2,169 cubes reach an edge of 12 but not 13." `generic` "Not quite. Find the two cube numbers either side of 2,169." `rounded-up` "$13^3 = 2{,}197$, more than the 2,169 in the tub. The edge is 12." `square-root` "You took the square root. A solid cube needs $n^3$ cubes, and $12^3 = 1{,}728$." `thirds` unchanged. `explain` "A cube with edge $n$ holds $n^3$ small cubes. Since $12^3 = 1{,}728 < 2{,}169 < 2{,}197 = 13^3$, the cube root of 2,169 is between 12 and 13. The largest solid cube has edge 12."
- Part 2. `question` "Using an edge of 12, how many small cubes are left over?" `answer` 441, `accept` "441", `wrong` `squared` 2025, `carried-up` -28, `times-three` 2133. `correct` "$12^3 = 12 \times 12 \times 12 = 1{,}728$, and $2{,}169 - 1{,}728 = 441$." `generic` "Not quite. Work out $12^3$, then take it from 2,169." `squared` "You took away $12^2 = 144$. The cube uses $12^3 = 1{,}728$, leaving 441." `carried-up` "That uses an edge of 13, which needs more cubes than the tub holds. With 12, 441 are left." `times-three` "You worked out $12 \times 3$. The power means $12 \times 12 \times 12 = 1{,}728$." `explain` "The cube uses $12^3$ small cubes. That is $12 \times 12 = 144$, then $144 \times 12 = 1{,}728$. So $2{,}169 - 1{,}728 = 441$ are left over."
- Part 3. `question` "She lays the 441 left-over cubes flat as one square layer, with none spare. How many cubes long is each side of the square?" `answer` 21, `accept` "21", `wrong` `halved` 220.5 (band 0.5), `quartered` 110.25 (band 0.25). `correct` "$21^2 = 441$, so $\sqrt{441} = 21$." `generic` "Not quite. Find the number that squared gives 441." `halved` "You halved 441. The side of a square is the number that, squared, gives the area: $\sqrt{441} = 21$." `quartered` "You divided by 4, as if counting round the edge. The layer is a full square: $21 \times 21 = 441$." `explain` "A square layer with side $s$ holds $s^2$ cubes. Since $20^2 = 400$ and $22^2 = 484$, the side lies between them. $21^2 = 441$ exactly, so each side is 21 cubes."

C16 (finding 16). `items[2].parts[0].feedback.generic`. The question says "Give the number in full". "Not quite. Divide 1.2 by 4, subtract the indices, then write the number out in full."

## Engine

A numeric widget grades by value, so it cannot ask for a decimal: on `problems-2` taxi part 1 ("Give a decimal to 4 decimal places") the entry `17/6` is marked correct, and no band can part it from 2.8333. Finding 10 works round this where the gap is wide enough. Not added to `docs/BACKLOG-INBOX.md` by this reader, whose brief names one output file.

## Verified

- Keys and slips: 40 keys and 92 `wrong` values by two routes each, all in agreement with the files. Each `wrong` value follows from the working its line describes, and each carried slip from the slip of the earlier part it names (0.6667 and 0.3333 from $\tfrac{3}{9}$; 0.7 from $\tfrac{7}{12}$; 137.14 from $\tfrac{9}{7}$; 1.5069 from $\tfrac{43}{36}$; 3.5 from $-8.5$; 4 pence from £2.84; $-228$ from edge 12; 308.43 from £925.30; 4 from 8,000; 34.2 from 300,000).
- Stated numbers and claims: $\tfrac{4}{11}$ is less than $\tfrac{3}{8}$; $\tfrac{7}{24}$ is a little under a third; $\tfrac{6}{19}$ is less than $\tfrac{1}{3}$; $\tfrac{31}{72}$ lies between $\tfrac{15}{36}$ and $\tfrac{16}{36}$; $\tfrac{1}{3}$ litre is less than both $\tfrac{4}{9}$ and $\tfrac{3}{4}$; the card has 18 holes, 5 under par, 6 shots under and 5 over; 2 pm to 11 pm is 9 hours and 4 hours on is 3 am; $17 \div 6$ runs 2 remainder 5, then 8 remainder 2, then 3 remainder 2; 0.28 exceeds $0.2777\ldots$ by about 0.002; $220 \div 3 \approx 73$; $24 \times 365 = 8{,}760$; $30{,}000 \div 24 = 1{,}250$.
- Bands: every key band takes the key, the value its `correct` line prints and the forms tried (fraction, unreduced fraction, mixed number, decimal, true minus sign, `£`, thousands comma). Fraction parts say "exact fraction" and refuse a 2-place decimal (3.33, 106.67), as stated. The widest `wrong` bands (38 ± 1, 84.5 ± 0.5, 42.25 ± 0.25, 3.3 ± 0.04) take only their own slip.
- Chain: each later part restates the value it uses, and a learner with a wrong earlier answer can still get it right. Two problems hold two short chains in place of one (golf parts 1 to 2 and 3 to 4; squash parts 1 to 2 and 3 to 5); read and judged acceptable, since each last part gives the result the problem is about.
- Level: every method is taught at or below its level (`taught.py`): a quotient that is not whole and a fraction divided by a fraction (l5 screens 4 and 5), mixed numbers (l3 screen 6), rounding a recurring decimal (l7), division with a negative (l9 screen 7), cube roots between whole numbers (l11 screen 6), 1 significant figure (l13), division in standard form (l14 quiz 4, `review-3`). "One amount as a fraction of another is a division" (rye part 4, squash part 5) is a step past l5 and is carried by the parts' own explanations; acceptable at difficulty 4 and 5. Only "mean" is untaught (finding 9).
- Shape: 4, 3 and 3 problems of 3 to 5 parts; difficulty 3 to 5 with a 5 in each set; typed parts 16 of 17, 11 of 12 and 11 of 11; every `skills` id is in `course.json`; every lesson of each level is drawn on and every problem draws on two or more.
- Voice: no sentence over 35 words, no explanation over three sentences, British spelling, no exclamation mark or em-dash, £ throughout.
- Reuse read by hand and judged acceptable (shapes, not numbers or sentences): a temperature crossing zero (l8 screen 2 and quiz 3, `review-2` item 3; here decimals and a rate); money shared equally and rounded to the penny (l7 quiz 4 with £100 and 3, `review-2` item 5 with £20 and 7; here £17 and 6, then the shortfall); two shares added and the rest found (`review-1` item 7 with $\tfrac{1}{4}$ and $\tfrac{1}{3}$ of £60). Chance matches of a single value: $\tfrac{7}{40} = 0.175$ in l7 screen 10, $\tfrac{5}{12} = \tfrac{15}{36}$ in l16 screen 7 (level 4), $\tfrac{5}{18} \approx 0.278$ in `bank/mental-4` and `conditional/problems-1`, $\tfrac{13}{20}$ and $\tfrac{31}{72}$ in two probability lessons. No story noun of the ten problems (garden beds, rye, printers, cordial, moor, golf, taxi, craft tub, stationery, comet) is used as a setting anywhere else in the course.
