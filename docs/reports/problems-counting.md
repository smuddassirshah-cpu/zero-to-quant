# Problem sets: counting (brief `docs/briefs/chained.md`)

Files: `app/content/courses/counting/problems-1.json` to `problems-3.json`. Numbers: `docs/reports/problems-counting-numbers.py` (exits 0, 1754 checks). Generator kept in the scratchpad only; the JSON is the source.

## Sets

| set | item | parts (typed / choice) | lessons drawn on | difficulty |
|---|---|---|---|---|
| problems-1 | p-tulip-bed | 4 (4 / 0) | l1, l2, l3, l4 | 3 |
| problems-1 | p-team-photo | 4 (3 / 1) | l1, l2 | 5 |
| problems-1 | p-five-a-side | 4 (4 / 0) | l3, l4 (and l1) | 4 |
| problems-1 | p-ice-cream-van | 4 (4 / 0) | l1, l2, l3, l4 | 4 |
| problems-2 | p-signal-flags | 4 (4 / 0) | l5, l6, l7, l8 | 4 |
| problems-2 | p-leisure-centre | 4 (4 / 0) | l7, l8 (and l4) | 4 |
| problems-2 | p-balloon-blocks | 5 (5 / 0) | l5, l6, l7, l8 | 5 |
| problems-2 | p-quiz-team | 5 (5 / 0) | l7, l8 (and l4) | 4 |
| problems-3 | p-orienteering | 5 (5 / 0) | l9, l10, l11 | 3 |
| problems-3 | p-power-line | 5 (4 / 1) | l9, l10, l11, l12 | 4 |
| problems-3 | p-grain-merchant | 4 (4 / 0) | l10, l11, l13 | 4 |
| problems-3 | p-sail-ring | 5 (5 / 0) | l9, l10, l12 | 5 |

Typed parts: level 1 15 of 16, level 2 18 of 18, level 3 18 of 19. Every lesson of each level appears in at least one problem; every problem draws on at least two. The two choice parts are judgements: which way to count the twins once the captain fixes the middle place, and what $\overrightarrow{AC} = 2.5\,\overrightarrow{AB}$ tells the engineer.

Level 1. Tulips: choose 4 of 8, order them, rows as groups times orders ($P(8,4)$), then an edging stage. Photo: $7!$, captain fixed, then the glued block fails because the captain splits the row; 4 free pairs give 192 (slip 240). League: pairs, home and away as $P(8,2)$, $n(n-1) = 72$ gives 9 teams, then $\binom{9}{6} = \binom{9}{3}$. Ice cream: cups $\binom{11}{3}$, cones by $3!$, one item from either list adds, then a five-way topping stage.

Level 2. Flags: repeats, a glued pair that needs no doubling, apart by subtraction, then a chance checked by places. Leisure centre: inclusion and exclusion, complement, then two members as pairs over pairs. BALLOON: repeats, OO glued, apart, then Ls apart among the Os-apart rows (inclusion and exclusion), then the chance $\tfrac{11}{21}$. Quiz team: $\binom{11}{4}$, no girls, at least one girl, then at least one of each, then $\tfrac{31}{33}$.

Level 3. Orienteering: two legs end minus start, head to tail, route by Pythagoras, then the saving (lengths do not add). Power line: $k = 2.5$, the collinear judgement, then the cable as $2.5\,|\overrightarrow{AB}|$ in metres. Grain: P&L as a dot product, a trade added, Tuesday as $\mathbf{h}\cdot\mathbf{d} + \mathbf{t}\cdot\mathbf{d}$, then the angle (115°). Sail: $\overrightarrow{RS}$, $\overrightarrow{OM}$, $\overrightarrow{OX}$, $\overrightarrow{RX}$, then $k = \tfrac{2}{3}$ with $\overrightarrow{RN}$, so X is on RN (the centroid).

## Freshness

`node tools/fresh-check.mjs --file content/courses/counting/problems-<n>.json`: 0 hits for each set, also at `--min-run 8 --min-share 0`. Read by hand against the course's lessons, quizzes, reviews and homework and against `counting-chance` problems 1 to 3. Three first drafts were changed for shared numbers: tulips were 3 of 8 (56 and 336, the l4 trap screen), so 4 of 8; the quiz team was 7 girls and 5 boys ($\binom{12}{4} = 495$, homework-1 portfolios), so 6 and 5; ice cream was 7 flavours (210, the l3 $P(7,3)$ screen), so 11. The second read (0.3 a) found 11 reused in `homework-1` ($\binom{11}{3} = 165$), so the van now sells 14 flavours (364 cups, 2184 cones, 2548 items, 12740 purchases) and the team line-up moved from a team photo, the stage 0 exam's story, to a coach introducing players before a match. Orienteering moved off the 3-4-5 and 6-8-10 vectors of l11, and the grain move off a P&L of 30 (l13 hook). No dice, cards, grid routes, price paths, round tables, committees of traders, PINs or holdings in Alpha and Beta.

## Checks

| check | problems-1 | problems-2 | problems-3 |
|---|---|---|---|
| numbers script | 0 failures (1754 checks for the three sets) | same | same |
| validator | 0 errors, 0 warnings on the file | same | same |
| playthrough `--local-cdn` | green (16 parts) | green (18 parts) | green (19 parts) |
| playthrough `--mobile` | green; 440 px shots read, no fault | same | same |
| voice scan 35 (course folder) | 0 and 0 | 0 and 0 | 0 and 0 |

The script checks per numeric part: two methods agree (exact formulas; enumeration of every flag row, block row, team and photo line-up; an explicit list of 80 members; `hypot`, `atan2` and random numeric vectors); the key and the asked rounding are inside the band; the last number of `feedback.correct` is accepted; each `wrong` value is its named slip, has a `byKey` line, and clears the key and the other wrongs; every number stated in feedback, explain, `byKey` and `why` is computed or given. Expression parts are parsed with sympy. Fixes made from it: three `feedback.correct` lines that ended on a factor now end on the answer.

## Engine limits

Two bullets in `docs/BACKLOG-INBOX.md` under `Raised later (problems counting):`.
