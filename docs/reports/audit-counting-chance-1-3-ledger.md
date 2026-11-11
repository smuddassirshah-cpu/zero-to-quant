# Claim ledger: counting-chance levels 1 to 3 (concept audit, round 1)

One row per claim-bearing string, read blind: every prose and question line, graded key, wrong value, option and its why, hint, feedback line, explanation, summary line, model answer and rubric line. Per-cell feedback lines of one grid screen share a row. Paths are JSON paths in the named file. Verdicts are those of `docs/briefs/concept-audit.md`. The basis is a named source with its section, a derivation, or the check in the concepts scripts (`docs/reports/counting-chance-L1-concepts.py`, `-L2-`, `-L3-`, cited as L1, L2 and L3 script). "Ross" is Ross, *A First Course in Probability* (9th edition), cited by section. Code starters, solutions and hidden tests have no row of their own: the L3 script executes them and the rows of the code screens cite it. Rows that are not `correct` carry their finding number from `docs/reviews/audit-counting-chance-1-3.md`.

Rows: 3931. correct 3911, imprecise 19, wrong 1.


## l1-every-outcome.json

| file | JSON path | claim (short) | verdict | basis |
|---|---|---|---|---|
| l1 | `screens[0].prose` | Roll two fair dice, one red and one blue. Each cell is one result: the row is the red die, th... | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[0].canvas.state.caption` | Every result of one roll | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[0].question` | Shade every result where the total is 7. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[0].widget.answer` | ["r1c6", "r2c5", "r3c4", "r4c3", "r5c2", "r6c1"] | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[0].widget.wrong[0].set` | ["r1c6", "r2c5", "r3c4"] | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[0].widget.wrong[1].set` | ["r4c3", "r5c2", "r6c1"] | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[0].hints[0].text` | If the red die shows 1, what must the blue die show? | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[0].hints[1].text` | The sevens run along one diagonal, starting at the top right. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[0].hints[2].text` | Red 1 needs blue 6, red 2 needs blue 5, and so on up to red 6. That is one cell in every row. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[0].feedback.correct` | Six of the 36 results add to 7, one in every row. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[0].feedback.generic` | Not quite right. Try every red result from 1 to 6, and check that each shaded pair adds to 7. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[0].feedback.byKey.r4c3` | You missed (4, 3). Red 4 with blue 3 is a different roll from red 3 with blue 4. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[0].feedback.byKey.r5c2` | You missed (5, 2). Red 5 with blue 2 is a different roll from red 2 with blue 5. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[0].feedback.byKey.r6c1` | You missed (6, 1). Red 6 with blue 1 is a different roll from red 1 with blue 6. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[0].feedback.byKey.r1c6` | You missed (1, 6). Every row has exactly one cell that adds to 7. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[0].feedback.byKey.r2c5` | You missed (2, 5). Every row has exactly one cell that adds to 7. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[0].feedback.byKey.r3c4` | You missed (3, 4). Every row has exactly one cell that adds to 7. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[0].feedback.byKey.one-order` | You shaded (3, 4) but not (4, 3). Red 3 with blue 4 and red 4 with blue 3 are different rolls. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[0].feedback.byKey.one-order-b` | You shaded (4, 3) but not (3, 4). Red 3 with blue 4 and red 4 with blue 3 are different rolls. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[0].explain.text` | You shaded six cells, from (1, 6) down to (6, 1). (3, 4) and (4, 3) are different cells: the ... | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[1].prose` | Now toss a coin three times. Each path from the start to the end is one full result, such as ... | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[1].question` | Tap every path with exactly two heads. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[1].widget.answer` | ["h-h-t", "h-t-h", "t-h-h"] | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[1].widget.wrong[0].set` | ["h-h-t", "h-t-h", "t-h-h", "h-h-h"] | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[1].widget.wrong[1].set` | ["h-h-t"] | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[1].hints[0].text` | Exactly two heads means exactly one tail. Where can the tail go? | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[1].hints[1].text` | Here is one such path. Find the others. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[1].feedback.correct` | HHT, HTH and THH: three of the eight paths. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[1].feedback.generic` | Not quite right. Exactly two heads means one tail, in any of the three places. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[1].feedback.byKey.h-h-h` | HHH has three heads, not two. Exactly two means two and no more. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[1].feedback.byKey.h-t-t` | HTT has only one head. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[1].feedback.byKey.t-h-t` | THT has only one head. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[1].feedback.byKey.t-t-h` | TTH has only one head. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[1].feedback.byKey.t-t-t` | TTT has no heads at all. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[1].feedback.byKey.h-h-t` | You missed HHT. The tail can come last. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[1].feedback.byKey.h-t-h` | You missed HTH. The tail can come in the middle. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[1].feedback.byKey.t-h-h` | You missed THH. The tail can come first. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[1].feedback.byKey.with-hhh` | HHH has three heads, not two. Exactly two means two and no more. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[1].feedback.byKey.one-path` | HHT is one way to get two heads. The tail can also come first or second. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[1].explain.text` | Exactly two heads means one tail, and it can come first, second or third. So three of the eig... | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[2].prose` | The full list of possible results is the **sample space**, written $S$. For three tosses, $S$... | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[2].question` | Which is the event “exactly two heads”, written as a set? | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[2].widget.options[0].text` | $\{\text{HHT}\}$ | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[2].widget.options[0].why` | That holds one order only. The tail can sit in any of the three tosses. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[2].widget.options[1].text` | $\{2\}$ | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[2].widget.options[1].why` | 2 is the number of heads, not an outcome. An event lists outcomes from $S$. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[2].widget.options[2].text` | $\{\text{HHT}, \text{HTH}, \text{THH}\}$ | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[2].widget.options[2].correct` | true | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[2].widget.options[3].text` | $\{\text{HHT}, \text{HTH}, \text{THH}, \text{HHH}\}$ | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[2].widget.options[3].why` | That is “at least two heads”. HHH has three heads, not two. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[2].hints[0].text` | An event lists outcomes, and each outcome is a whole path. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[2].hints[1].text` | These are the paths you tapped. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[2].hints[2].text` | Write each tapped path as three letters, inside curly brackets. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[2].feedback.correct` | Three outcomes, each a full path of three tosses. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[2].feedback.generic` | Not quite right. List every path with exactly two heads, each as a full result. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[2].explain.text` | An event is a set of outcomes, so we list whole paths: $E = \{\text{HHT}, \text{HTH}, \text{T... | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[3].prose` | Same three tosses. Event $F$: the first and last tosses match. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[3].question` | Tap every path in $F$. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[3].widget.answer` | ["h-h-h", "h-t-h", "t-h-t", "t-t-t"] | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[3].widget.wrong[0].set` | ["h-h-h", "h-t-h"] | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[3].widget.wrong[1].set` | ["h-h-h", "t-t-t"] | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[3].hints[0].text` | Look only at the first and third letters of each path. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[3].hints[1].text` | HTH is in $F$: it starts and ends with H. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[3].hints[2].text` | The first toss can be H or T, the middle anything, and the last must copy the first. That is ... | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[3].feedback.correct` | HHH, HTH, THT and TTT: four of the eight paths. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[3].feedback.generic` | Not quite right. Keep each path whose first and third letters agree. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[3].feedback.byKey.only-heads` | You kept only paths that start and end with H. Two tails match too. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[3].feedback.byKey.all-same` | You kept paths where all three tosses match. Only the first and last must agree; the middle i... | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[3].feedback.byKey.h-h-t` | HHT starts with H but ends with T. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[3].feedback.byKey.h-t-t` | HTT starts with H but ends with T. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[3].feedback.byKey.t-h-h` | THH starts with T but ends with H. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[3].feedback.byKey.t-t-h` | TTH starts with T but ends with H. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[3].feedback.byKey.h-h-h` | You missed HHH. It starts and ends with H. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[3].feedback.byKey.h-t-h` | You missed HTH. The middle toss can be anything. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[3].feedback.byKey.t-h-t` | You missed THT. The middle toss can be anything. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[3].feedback.byKey.t-t-t` | You missed TTT. It starts and ends with T. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[3].explain.text` | $F = \{\text{HHH}, \text{HTH}, \text{THT}, \text{TTT}\}$, so $/F/ = 4$. The middle toss is fr... | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[4].prose` | Back to the two dice. Event $B$: the red die shows more than the blue die. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[4].canvas.state.caption` | 36 outcomes | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[4].question` | How many outcomes are in $B$? | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[4].widget.answer` | 15 | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[4].widget.accept` | 15 exactly: $0 + 1 + 2 + 3 + 4 + 5$. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[4].widget.wrong[0].value` | 21 | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[4].widget.wrong[1].value` | 18 | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[4].widget.wrong[2].value` | 30 | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[4].hints[0].text` | Go row by row. If red shows 4, which blue results are lower? | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[4].hints[1].text` | The cells below the diagonal have the red die higher. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[4].hints[2].text` | Row 1 has 0 such cells, row 2 has 1, row 3 has 2, and so on: $0 + 1 + 2 + 3 + 4 + 5$. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[4].feedback.correct` | 15 cells, all below the diagonal. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[4].feedback.generic` | Not quite right. Count the cells where the row number beats the column number. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[4].feedback.byKey.ties` | You included the doubles. On (3, 3) the red die does not show more. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[4].feedback.byKey.half` | Half of 36 assumes no ties. The 6 doubles sit in neither half. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[4].feedback.byKey.differ` | That counts every roll where the dice differ. In half of those the blue die is higher. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[4].explain.text` | The cells below the diagonal have red higher: $0 + 1 + 2 + 3 + 4 + 5 = 15$. The 6 doubles sit... | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[5].prose` | Two more events for the dice. $C$: the total is 13. $D$: the total is at most 12. Each cell n... | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[5].canvas.state.caption` | Each cell shows the total | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[5].question` | Which statement is right? | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[5].widget.options[0].text` | $C$ is not an event, because it can never happen. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[5].widget.options[0].why` | You dropped $C$ because it never happens. Any set of outcomes is an event, and the empty set ... | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[5].widget.options[1].text` | $C$ holds one outcome, the total 13. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[5].widget.options[1].why` | 13 is a total, not an outcome. No cell adds to 13, so $C$ holds no outcomes. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[5].widget.options[2].text` | $C$ is the empty event $\varnothing$, and $D$ is the whole space $S$. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[5].widget.options[2].correct` | true | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[5].widget.options[3].text` | $D$ is not an event, because it always happens. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[5].widget.options[3].why` | An event may hold every outcome. $D$ holds all 36 cells, so $D = S$. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[5].hints[0].text` | Find the largest total on the grid. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[5].hints[1].text` | The largest total is 12, in one corner. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[5].hints[2].text` | No cell reaches 13, and every cell is 12 or less. So $C$ holds 0 cells and $D$ holds all 36. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[5].feedback.correct` | $C$ holds no outcomes and $D$ holds all 36. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[5].feedback.generic` | Not quite right. Count the cells in $C$ and in $D$, then name each set. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[5].explain.text` | No cell adds to 13, so $C = \varnothing$ and $P(C) = 0$. Every cell is at most 12, so $D = S$... | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[5].explain.canvas.caption` | $D = S$: all 36 cells | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[6].prose` | Sam lists two dice without caring which die is which: $\{1,1\}, \{1,2\}, \dots, \{6,6\}$. He ... | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[6].canvas.state.caption` | Sam's 21 outcomes | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[6].question` | What is the chance of a total of 7? | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[6].widget.options[0].text` | $\dfrac{3}{21} = \dfrac{1}{7}$ | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[6].widget.options[0].why` | You used Sam's list. It merges (3, 4) and (4, 3), which are different rolls. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[6].widget.options[1].text` | $\dfrac{6}{36} = \dfrac{1}{6}$ | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[6].widget.options[1].correct` | true | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[6].widget.options[2].text` | $\dfrac{3}{36} = \dfrac{1}{12}$ | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[6].widget.options[2].why` | You kept Sam's three pairs but used all 36 cells. Each pair has a mirror cell, so 7 has six c... | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[6].widget.options[3].text` | $\dfrac{6}{21} = \dfrac{2}{7}$ | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[6].widget.options[3].why` | You counted six cells for 7 but kept Sam's 21 below. Top and bottom must come from the same l... | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[6].hints[0].text` | Is red 3 with blue 4 the same roll as red 4 with blue 3? | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[6].hints[1].text` | Sam's list hides these three cells. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[6].hints[2].text` | Keep the dice apart: 36 cells, and 6 of them total 7. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[6].feedback.correct` | Six ordered pairs out of 36. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[6].feedback.generic` | Not quite right. Keep the red and blue dice apart, then count. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[6].feedback.byKey.sam` | You used Sam's 21. His $\{3,4\}$ hides two different rolls, (3, 4) and (4, 3). | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[6].explain.text` | Sam's $\{3,4\}$ covers two rolls, (3, 4) and (4, 3), but his $\{3,3\}$ covers one. So his 21 ... | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[6].explain.canvas.caption` | 36 outcomes, 6 of them total 7 | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[7].prose` | Here is what you did. List every outcome once, keeping dice and tosses apart: that list is $S... | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[7].question` | Three dice: red, blue and green. How many outcomes are in $S$? | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[7].widget.answer` | 216 | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[7].widget.accept` | 216 exactly: $6 \times 6 \times 6$. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[7].widget.wrong[0].value` | 56 | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[7].widget.wrong[1].value` | 18 | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[7].widget.wrong[2].value` | 36 | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[7].hints[0].text` | Each outcome is a triple: red, blue, green. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[7].hints[1].text` | Each die has 6 faces, and every combination is a different outcome. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[7].hints[2].text` | $6 \times 6 \times 6$. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[7].feedback.correct` | $6^3 = 216$ ordered triples. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[7].feedback.generic` | Not quite right. Keep the three dice apart and count every triple. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[7].feedback.byKey.unordered` | You ignored which die is which, as Sam did. Keep the dice apart: 6 choices for each. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[7].feedback.byKey.added` | You added 6 three times. Each red result pairs with every blue and green result, so multiply. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[7].feedback.byKey.two-dice` | That is two dice. The third die multiplies by 6 again. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[7].explain.text` | Each die has 6 faces, and every combination is one outcome: $6 \times 6 \times 6 = 216$. Merg... | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[8].prose` | A share trades at £50.00. Each day it moves up £1.00, stays flat, or moves down £1.00. We wat... | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[8].canvas.state.caption` | Start £50.00. U: up £1.00, F: flat, D: down £1.00. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[8].question` | Shade every outcome where the share ends above £50.00. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[8].widget.answer` | ["r1c1", "r1c2", "r2c1"] | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[8].widget.wrong[0].set` | ["r1c1"] | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[8].widget.wrong[1].set` | ["r1c1", "r1c2"] | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[8].widget.wrong[2].set` | ["r1c1", "r1c2", "r2c1", "r1c3", "r3c1", "r2c2"] | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[8].hints[0].text` | Add the two moves. Which pairs give a net rise? | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[8].hints[1].text` | Two up days, or one up day and one flat day. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[8].hints[2].text` | Up, up ends at £52.00. Up, flat and flat, up end at £51.00. Every other outcome ends at £50.0... | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[8].feedback.correct` | Three of the nine outcomes end above £50.00. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[8].feedback.generic` | Not quite right. Add the two moves for each cell and keep the ones that end above £50.00. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[8].feedback.byKey.only-uu` | You missed up, flat and flat, up. One rise with no fall is enough. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[8].feedback.byKey.one-order` | You missed flat, up. It is a different path from up, flat, just like (4, 3) and (3, 4). | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[8].feedback.byKey.at-or-above` | You included outcomes that end at exactly £50.00. Above means strictly more. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[8].feedback.byKey.r1c3` | Up then down ends at £50.00, not above it. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[8].feedback.byKey.r3c1` | Down then up ends at £50.00, not above it. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[8].feedback.byKey.r2c2` | Flat twice ends at £50.00, not above it. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[8].feedback.byKey.r2c3` | Flat then down ends at £49.00. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[8].feedback.byKey.r3c2` | Down then flat ends at £49.00. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[8].feedback.byKey.r3c3` | Down twice ends at £48.00. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[8].feedback.byKey.r1c2` | You missed up, flat. It ends at £51.00. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[8].feedback.byKey.r2c1` | You missed flat, up. It ends at £51.00. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[8].feedback.byKey.r1c1` | You missed up, up. It ends at £52.00. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[8].explain.text` | The sample space has $3 \times 3 = 9$ outcomes, one per pair of moves. Three end above £50.00... | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `summary.ideas` | ["The sample space $S$ lists every outcome once. Keep the dice, coins and days apart.", "An e... | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `summary.formula.name` | Sample space of two dice | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `summary.formula.tex` | S = \{(r, b) : r, b \in \{1, \dots, 6\}\}, \quad /S/ = 36 | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `summary.formula.note` | An event $E$ is a subset: $\varnothing \subseteq E \subseteq S$, and $/E/$ counts its outcomes. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `summary.trap` | Merging (3, 4) and (4, 3) gives 21 outcomes. Chances worked out from that list come out wrong. | imprecise | finding 9: the 21 unordered outcomes form a valid sample space; chances go wrong only when its outcomes are counted as equally likely (Ross 2.2, 2.5) |
| l1 | `quiz[0].prose` | A coin is tossed and a die is rolled. One outcome is (H, 4). | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `quiz[0].question` | How many outcomes are in the sample space? | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `quiz[0].widget.answer` | 12 | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `quiz[0].widget.accept` | 12 exactly: $2 \times 6$. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `quiz[0].widget.wrong[0].value` | 8 | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `quiz[0].widget.wrong[1].value` | 6 | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `quiz[0].feedback.correct` | 2 coin results times 6 die results. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `quiz[0].feedback.generic` | Not quite right. Pair each coin result with each die result. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `quiz[0].feedback.byKey.added` | You added 2 and 6. Each coin result pairs with all 6 die results, so multiply. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `quiz[0].feedback.byKey.die` | That is the die alone. Each face comes with H or with T. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `quiz[0].explain.text` | Each of H and T pairs with each of the 6 faces. So $/S/ = 2 \times 6 = 12$, from (H, 1) to (T... | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `quiz[1].prose` | Two limit orders, A and B, are each filled (F) or not (N) by the close. An outcome lists A fi... | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `quiz[1].question` | Which set is the event “exactly one order fills”? | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `quiz[1].widget.options[0].text` | $\{\text{FN}\}$ | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `quiz[1].widget.options[0].why` | That is A filling alone. B can be the one that fills: NF. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `quiz[1].widget.options[1].text` | $\{\text{FN}, \text{NF}\}$ | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `quiz[1].widget.options[1].correct` | true | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `quiz[1].widget.options[2].text` | $\{\text{FN}, \text{NF}, \text{FF}\}$ | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `quiz[1].widget.options[2].why` | That is “at least one fills”. FF has two fills. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `quiz[1].widget.options[3].text` | $\{1\}$ | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `quiz[1].widget.options[3].why` | 1 is a count of fills, not an outcome. List the outcomes. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `quiz[1].feedback.correct` | FN and NF: one fill each. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `quiz[1].feedback.generic` | Not quite right. List the outcomes with exactly one F. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `quiz[1].explain.text` | The sample space is $\{\text{FF}, \text{FN}, \text{NF}, \text{NN}\}$. Exactly one fill picks ... | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `quiz[2].prose` | A price moves up, flat or down on each of two days. Ana lists the outcomes by net move: −2, −... | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `quiz[2].question` | How many outcomes does the full sample space hold? | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `quiz[2].widget.answer` | 9 | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `quiz[2].widget.accept` | 9 exactly: $3 \times 3$. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `quiz[2].widget.wrong[0].value` | 5 | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `quiz[2].widget.wrong[1].value` | 6 | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `quiz[2].feedback.correct` | Nine pairs of moves. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `quiz[2].feedback.generic` | Not quite right. An outcome is a pair of moves, one for each day. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `quiz[2].feedback.byKey.ana` | You listed net moves, as Ana did. A net move of 0 comes from three different paths. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `quiz[2].feedback.byKey.added` | You added 3 and 3. Each first-day move pairs with each second-day move. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `quiz[2].explain.text` | An outcome is a pair of moves, so $/S/ = 3 \times 3 = 9$. Ana's net move of 0 merges up then ... | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `quiz[3].prose` | Two dice are rolled. Event $E$: both dice show an odd number, and the total is odd. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `quiz[3].question` | How many outcomes are in $E$? | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `quiz[3].widget.answer` | 0 | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `quiz[3].widget.accept` | 0: $E$ is the empty event. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `quiz[3].widget.wrong[0].value` | 9 | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `quiz[3].widget.wrong[1].value` | 18 | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `quiz[3].feedback.correct` | None: $E = \varnothing$. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `quiz[3].feedback.generic` | Not quite right. Add two odd numbers and look at the total. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `quiz[3].feedback.byKey.both-odd` | Those 9 rolls have two odd dice, but every one has an even total. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `quiz[3].feedback.byKey.odd-total` | Those 18 rolls have an odd total, but each has one even die. | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `quiz[3].explain.text` | Odd plus odd is always even. So no roll has two odd dice and an odd total, and $E = \varnothi... | correct | Ross 2.2 (sample space, events); 36 ordered rolls and 8 toss paths, enumerated, L1 script |
| l1 | `screens[0].feedback.byKey.r*c*` | 30 per-cell lines of the form "(a, b) adds to n, not t" | correct | each sum and cell id recomputed by the ledger build |

## l2-equally-likely.json

| file | JSON path | claim (short) | verdict | basis |
|---|---|---|---|---|
| l2 | `screens[0].prose` | Roll two fair dice and record the total. There are 11 possible totals, from 2 to 12. Predict ... | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[0].canvas.state.caption` | Run some rolls and watch the bars. | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[0].question` | After 1,000 rolls, which total comes up most often? | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[0].widget.options[0].text` | 2 | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[0].widget.options[0].why` | A total of 2 needs a 1 on both dice. Only one roll does that. | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[0].widget.options[1].text` | 7 | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[0].widget.options[1].correct` | true | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[0].widget.options[2].text` | 12 | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[0].widget.options[2].why` | A total of 12 needs a 6 on both dice. Only one roll does that. | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[0].widget.options[3].text` | All about equally often | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[0].widget.options[3].why` | You treated the 11 totals as equally likely. Run 1,000 rolls and compare the 2 bar with the 7... | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[0].hints[0].text` | Run 1,000 rolls and look for the tallest bar. | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[0].hints[1].text` | Compare these end bars with the bars in the middle. | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[0].feedback.correct` | In the long run 7 comes up six times as often as 2 or 12. | imprecise | finding 8: 7 has six rolls, 2 has one and 12 has one; '2 or 12' as one event has two rolls, so the ratio reads as 6 or as 3 |
| l2 | `screens[0].feedback.generic` | Not quite right. Run 1,000 rolls and find the tallest bar. | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[0].explain.text` | The 7 bar towers over the 2 and 12 bars. So the 11 totals are not equally likely, and $\tfrac... | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[1].prose` | Here is why. Each cell is one of the 36 rolls, and every roll is equally likely. The number i... | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[1].canvas.state.caption` | 36 rolls, each equally likely | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[1].question` | Shade every roll with a total of 10. | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[1].widget.answer` | ["r4c6", "r5c5", "r6c4"] | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[1].widget.wrong[0].set` | ["r4c6", "r6c4"] | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[1].widget.wrong[1].set` | ["r4c6", "r5c5"] | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[1].widget.wrong[2].set` | ["r5c5", "r6c4"] | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[1].hints[0].text` | Which pairs of faces add to 10? | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[1].hints[1].text` | Tens sit on one short diagonal at the bottom right. | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[1].hints[2].text` | 4 and 6, 5 and 5, 6 and 4. That is three cells. | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[1].feedback.correct` | Three of the 36 rolls total 10. | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[1].feedback.generic` | Not quite right. Find every cell that shows 10. | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[1].feedback.byKey.r4c6` | You missed (4, 6): red 4 and blue 6. | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[1].feedback.byKey.r6c4` | You missed (6, 4). Red 6 with blue 4 differs from red 4 with blue 6. | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[1].feedback.byKey.r5c5` | You missed (5, 5). A double is one roll, and it counts. | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[1].feedback.byKey.no-double` | You missed (5, 5). A double is one roll, and it counts. | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[1].feedback.byKey.one-order` | You missed (6, 4). Red 6 with blue 4 differs from red 4 with blue 6. | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[1].feedback.byKey.one-order-b` | You missed (4, 6). Red 4 with blue 6 differs from red 6 with blue 4. | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[1].explain.text` | Three rolls total 10, but six total 7 and only one totals 2. Each total is a group of rolls, ... | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[2].prose` | The 36 rolls are equally likely outcomes, as in the counting course: each has chance $\tfrac{... | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[2].canvas.state.caption` | 36 equally likely rolls, grouped by total | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[2].question` | What is $P(\text{total is } 7)$? Give a fraction or a decimal. | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[2].widget.answer` | 0.166667 | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[2].widget.accept` | Any form equal to $\tfrac{1}{6}$, or 0.1667 to 4 places. | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[2].widget.wrong[0].value` | 0.090909 | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[2].widget.wrong[1].value` | 0.5 | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[2].widget.wrong[2].value` | 0.194444 | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[2].widget.wrong[3].value` | 0.027778 | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[2].hints[0].text` | How many of the 36 rolls total 7? | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[2].hints[1].text` | Read the height of the 7 bar. | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[2].hints[2].text` | Six rolls total 7, out of 36. | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[2].feedback.correct` | Six of the 36 equally likely rolls: $\tfrac{6}{36} = \tfrac{1}{6}$. | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[2].feedback.generic` | Not quite right. Count the rolls in the event, then divide by the 36 rolls in $S$. | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[2].feedback.byKey.eleven` | You divided by the 11 totals. They are not equally likely, so count rolls, not totals. | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[2].feedback.byKey.half` | You split into 7 and not 7. Those two are not equally likely: 6 rolls against 30. | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[2].feedback.byKey.seven` | You used the total itself as the count. Six rolls total 7. | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[2].feedback.byKey.one` | That is the chance of one particular roll, such as (3, 4). Six rolls total 7. | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[2].explain.text` | You counted 6 rolls in the event and 36 in $S$: $P = \tfrac{6}{36} = \tfrac{1}{6}$. Counting ... | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[3].prose` | A bet pays out when the total is 10 or more. | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[3].canvas.state.caption` | 36 equally likely rolls, grouped by total | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[3].question` | What is $P(\text{total} \ge 10)$? Give a fraction or a decimal. | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[3].widget.answer` | 0.166667 | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[3].widget.accept` | Any form equal to $\tfrac{6}{36} = \tfrac{1}{6}$, or 0.1667. | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[3].widget.wrong[0].value` | 0.272727 | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[3].widget.wrong[1].value` | 0.083333 | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[3].hints[0].text` | Which totals count, and how many rolls give each? | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[3].hints[1].text` | Add the heights of these three bars. | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[3].hints[2].text` | $3 + 2 + 1 = 6$ rolls out of 36. | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[3].feedback.correct` | Six rolls: three for 10, two for 11, one for 12. | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[3].feedback.generic` | Not quite right. Add the rolls behind 10, 11 and 12, then divide by 36. | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[3].feedback.byKey.totals` | You took 3 of the 11 totals. Totals are not equally likely; count the rolls behind each. | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[3].feedback.byKey.one-each` | You gave each total one roll. 10 has three rolls, 11 has two, and 12 has one. | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[3].explain.text` | You added the rolls behind each total: $3 + 2 + 1 = 6$. So $P(\text{total} \ge 10) = \tfrac{6... | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[4].prose` | A bent coin lands heads with chance 0.6. Its sample space is still $\{\text{H}, \text{T}\}$: ... | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[4].canvas.state.caption` | A bent coin | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[4].question` | What is $P(\text{H})$, and where does it come from? | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[4].widget.options[0].text` | $\tfrac{1}{2}$, since H is 1 of 2 outcomes. | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[4].widget.options[0].why` | You counted outcomes. That works only when they are equally likely, and this coin favours heads. | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[4].widget.options[1].text` | 0.6, from the coin itself. H and T are not equally likely, so counting does not apply. | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[4].widget.options[1].correct` | true | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[4].widget.options[2].text` | Either 0.6 or $\tfrac{1}{2}$, depending on the method. | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[4].widget.options[2].why` | An event has one chance. Counting gives $\tfrac{1}{2}$ only by wrongly treating H and T as eq... | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[4].widget.options[3].text` | It cannot be known, since the outcomes are not equally likely. | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[4].widget.options[3].why` | Unequal outcomes still have chances. We cannot get them by counting, but here we are told 0.6. | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[4].hints[0].text` | What does $\tfrac{/E/}{/S/}$ assume about the outcomes? | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[4].hints[1].text` | Compare the two bars. | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[4].hints[2].text` | Counting needs every outcome to have the same chance. These two do not. | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[4].feedback.correct` | Counting needs equal chances, and this coin's two faces do not have them. | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[4].feedback.generic` | Not quite right. Check whether H and T are equally likely before you count. | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[4].explain.text` | $\tfrac{/E/}{/S/}$ would give $\tfrac{1}{2}$, which is wrong for this coin. The rule needs eq... | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[5].prose` | Alex argues: “Either the total is 7 or it is not. That is two outcomes, so $P(7) = \tfrac{1}{... | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[5].canvas.state.caption` | The rolls that total 7 | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[5].question` | What is wrong with Alex's argument? | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[5].widget.options[0].text` | Nothing: two outcomes, one of them a 7, so $\tfrac{1}{2}$. | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[5].widget.options[0].why` | You accepted two outcomes as equally likely without checking. The grid shows 6 rolls for 7 an... | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[5].widget.options[1].text` | He should use the 11 totals, so $P(7) = \tfrac{1}{11}$. | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[5].widget.options[1].why` | That swaps one unequal list for another. The 11 totals are no more equally likely than “7” an... | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[5].widget.options[2].text` | His two outcomes are not equally likely: 6 rolls give 7 and 30 do not. | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[5].widget.options[2].correct` | true | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[5].widget.options[3].text` | “Not 7” is not an outcome, so it cannot be counted. | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[5].widget.options[3].why` | “Not 7” is a fine event. The trouble is that it holds 30 rolls, not 1. | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[5].hints[0].text` | Count the rolls behind each of Alex's two outcomes. | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[5].hints[1].text` | These are the rolls that total 7. | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[5].hints[2].text` | Six rolls total 7 and the other 30 do not. Chances of $\tfrac{6}{36}$ and $\tfrac{30}{36}$ ar... | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[5].feedback.correct` | One side holds 6 rolls, the other 30. | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[5].feedback.generic` | Not quite right. Count how many rolls sit behind “7” and behind “not 7”. | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[5].feedback.byKey.nothing` | You accepted two outcomes as equally likely without checking. The grid shows 6 rolls for 7 an... | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[5].explain.text` | Alex split $S$ into two events, but one holds 6 rolls and the other 30. Counting outcomes giv... | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[5].explain.canvas.caption` | 6 rolls against 30 | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[6].prose` | You counted rolls and divided by 36. Why does that work? Suppose $S$ has $n$ equally likely o... | correct | Ross 2.5: derivation from P(S) = 1 and additivity over n equally likely outcomes |
| l2 | `screens[6].question` | Put the lines of the argument in order. | correct | Ross 2.5: derivation from P(S) = 1 and additivity over n equally likely outcomes |
| l2 | `screens[6].widget.lines[0].text` | Every outcome has the same chance; call it $c$. | correct | Ross 2.5: derivation from P(S) = 1 and additivity over n equally likely outcomes |
| l2 | `screens[6].widget.lines[1].text` | The $n$ chances add up to $P(S) = 1$, so $nc = 1$. | correct | Ross 2.5: derivation from P(S) = 1 and additivity over n equally likely outcomes |
| l2 | `screens[6].widget.lines[2].text` | So each outcome has chance $c = \tfrac{1}{n}$. | correct | Ross 2.5: derivation from P(S) = 1 and additivity over n equally likely outcomes |
| l2 | `screens[6].widget.lines[3].text` | $E$ holds $k$ outcomes, so $P(E) = k \cdot \tfrac{1}{n} = \tfrac{/E/}{/S/}$. | correct | Ross 2.5: derivation from P(S) = 1 and additivity over n equally likely outcomes |
| l2 | `screens[6].widget.answer` | ["name", "sum", "solve", "event"] | correct | Ross 2.5: derivation from P(S) = 1 and additivity over n equally likely outcomes |
| l2 | `screens[6].hints[0].text` | Start by naming the common chance. | correct | Ross 2.5: derivation from P(S) = 1 and additivity over n equally likely outcomes |
| l2 | `screens[6].hints[1].text` | All the outcomes together make up $S$, and $P(S) = 1$. | correct | Ross 2.5: derivation from P(S) = 1 and additivity over n equally likely outcomes |
| l2 | `screens[6].hints[2].text` | Name $c$, use $P(S) = 1$ to find it, then add up $k$ copies of it. | correct | Ross 2.5: derivation from P(S) = 1 and additivity over n equally likely outcomes |
| l2 | `screens[6].feedback.correct` | Equal chances that add to 1 must each be $\tfrac{1}{n}$. | correct | Ross 2.5: derivation from P(S) = 1 and additivity over n equally likely outcomes |
| l2 | `screens[6].feedback.generic` | Not quite right. Find the chance of one outcome before the chance of $E$. | correct | Ross 2.5: derivation from P(S) = 1 and additivity over n equally likely outcomes |
| l2 | `screens[6].explain.text` | Equal chances that add to 1 must each be $\tfrac{1}{n}$, and $E$ collects $k$ of them. If the... | correct | Ross 2.5: derivation from P(S) = 1 and additivity over n equally likely outcomes |
| l2 | `screens[7].prose` | A trader says: “Each day the index goes up or down. Two outcomes, so $P(\text{up}) = \tfrac{1... | correct | relative frequency as an estimate; exact binomial tail in the L1 script |
| l2 | `screens[7].canvas.state.caption` | Ten trading days | correct | relative frequency as an estimate; exact binomial tail in the L1 script |
| l2 | `screens[7].question` | What is the best response? | correct | relative frequency as an estimate; exact binomial tail in the L1 script |
| l2 | `screens[7].widget.options[0].text` | She is right: two outcomes, so $\tfrac{1}{2}$. | correct | relative frequency as an estimate; exact binomial tail in the L1 script |
| l2 | `screens[7].widget.options[0].why` | You counted outcomes without checking they are equally likely. Indices often rise on more day... | correct | stylised fact: equity indices have positive drift and close up on a little over half of trading days (S&P 500 about 53%, 1950 to 2020); not recomputed from data here |
| l2 | `screens[7].widget.options[1].text` | The log proves $P(\text{up}) = 0.6$ exactly. | correct | relative frequency as an estimate; exact binomial tail in the L1 script |
| l2 | `screens[7].widget.options[1].why` | Ten days is a small sample. 0.6 is an estimate, and another ten days could give 0.4 or 0.8. | correct | relative frequency as an estimate; exact binomial tail in the L1 script |
| l2 | `screens[7].widget.options[2].text` | Up and down need not be equally likely. The log suggests about 0.6, so counting cannot justif... | imprecise | finding 6: the reason counting fails is the missing symmetry, not the log; P(6 or more ups in 10 at p = 0.5) = 0.377 (L1 script), so ten days do not separate 0.6 from 0.5 |
| l2 | `screens[7].widget.options[2].correct` | true | correct | relative frequency as an estimate; exact binomial tail in the L1 script |
| l2 | `screens[7].widget.options[3].text` | Add a third outcome, flat, so $P(\text{up}) = \tfrac{1}{3}$. | correct | relative frequency as an estimate; exact binomial tail in the L1 script |
| l2 | `screens[7].widget.options[3].why` | Adding flat does not fix it. Three outcomes are no more equally likely than two. | correct | relative frequency as an estimate; exact binomial tail in the L1 script |
| l2 | `screens[7].hints[0].text` | Count the up days in the log. | correct | relative frequency as an estimate; exact binomial tail in the L1 script |
| l2 | `screens[7].hints[1].text` | Six of the ten days were up. | correct | relative frequency as an estimate; exact binomial tail in the L1 script |
| l2 | `screens[7].hints[2].text` | Counting needs equally likely outcomes, and nothing says up and down are. Measure the chance ... | correct | relative frequency as an estimate; exact binomial tail in the L1 script |
| l2 | `screens[7].feedback.correct` | Measure the chance; do not count it. | correct | relative frequency as an estimate; exact binomial tail in the L1 script |
| l2 | `screens[7].feedback.generic` | Not quite right. Ask whether up and down are equally likely before you count. | correct | relative frequency as an estimate; exact binomial tail in the L1 script |
| l2 | `screens[7].explain.text` | Counting gives $\tfrac{1}{2}$ only if up and down are equally likely, and nothing guarantees ... | correct | relative frequency as an estimate; exact binomial tail in the L1 script |
| l2 | `screens[8].prose` | A bet on two fair dice pays £10 if the red die beats the blue die, and nothing otherwise. Its... | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[8].canvas.state.caption` | 36 equally likely rolls | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[8].question` | What is the fair price to play once, in pounds? | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[8].widget.answer` | 4.1667 | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[8].widget.accept` | £4.17, within 1p: $\text{£}10 \times \tfrac{15}{36}$. | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[8].widget.wrong[0].value` | 5 | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[8].widget.wrong[1].value` | 3.3333 | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[8].widget.wrong[2].value` | 10 | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[8].hints[0].text` | Red beats blue and blue beats red are mirror images. How many ties are there? | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[8].hints[1].text` | The diagonal holds the ties. | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[8].hints[2].text` | $36 - 6 = 30$ rolls have a winner, and half of them have red higher: 15. Over 36 rolls the be... | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[8].feedback.correct` | £150 over 36 rolls is about £4.17 a roll. | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[8].feedback.generic` | Not quite right. Count the rolls where red wins, then share the total payout over all 36. | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[8].feedback.byKey.half` | You split the rolls into win and lose. The 6 ties pay nothing, so red wins only 15 of 36. | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[8].feedback.byKey.third` | You treated win, lose and tie as equally likely. Ties hold 6 rolls, while wins and losses hol... | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[8].feedback.byKey.all` | That is the payout, not its average. The bet pays on only 15 of the 36 rolls. | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[8].explain.text` | Swapping the dice turns each red win into a blue win, so both hold the same number of rolls. ... | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `summary.ideas` | ["With equally likely outcomes, a chance is a count: $P(E) = \\tfrac{/E/}{/S/}$.", "Check the... | imprecise | finding 7: unequal outcomes can also be computed from a finer equally likely list, as this lesson does for the totals of two dice |
| l2 | `summary.formula.name` | Equally likely outcomes | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `summary.formula.tex` | P(E) = \dfrac{/E/}{/S/} | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `summary.formula.note` | Only when every outcome in $S$ has the same chance, $\tfrac{1}{/S/}$. | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `summary.trap` | Two outcomes are not always a 50:50 split. “It happens or it does not” gives $\tfrac{1}{2}$ o... | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `quiz[0].prose` | Two fair dice are rolled. | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `quiz[0].question` | What is $P(\text{total is } 4)$? Give a fraction or a decimal. | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `quiz[0].widget.answer` | 0.083333 | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `quiz[0].widget.accept` | Any form equal to $\tfrac{3}{36} = \tfrac{1}{12}$, or 0.0833. | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `quiz[0].widget.wrong[0].value` | 0.090909 | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `quiz[0].widget.wrong[1].value` | 0.055556 | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `quiz[0].feedback.correct` | (1, 3), (2, 2) and (3, 1): 3 of 36. | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `quiz[0].feedback.generic` | Not quite right. List the rolls that total 4, keeping the dice apart. | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `quiz[0].feedback.byKey.eleven` | You divided by the 11 totals. They are not equally likely; count rolls. | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `quiz[0].feedback.byKey.one-order` | You missed one roll. (1, 3) and (3, 1) are both there, and so is (2, 2). | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `quiz[0].explain.text` | Three rolls total 4: (1, 3), (2, 2) and (3, 1). So $P = \tfrac{3}{36} = \tfrac{1}{12}$. | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `quiz[1].prose` | Two fair coins are tossed. Kim says the outcomes are no heads, one head and two heads, so one... | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `quiz[1].question` | What is the chance of exactly one head? Give a fraction or a decimal. | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `quiz[1].widget.answer` | 0.5 | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `quiz[1].widget.accept` | Any form equal to $\tfrac{1}{2}$. | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `quiz[1].widget.wrong[0].value` | 0.333333 | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `quiz[1].widget.wrong[1].value` | 0.25 | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `quiz[1].feedback.correct` | HT and TH: 2 of 4 equally likely outcomes. | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `quiz[1].feedback.generic` | Not quite right. List the outcomes with the coins kept apart. | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `quiz[1].feedback.byKey.kim` | You used Kim's list. One head covers HT and TH, while two heads covers only HH. | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `quiz[1].feedback.byKey.quarter` | You counted HT but not TH. Either coin can be the head. | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `quiz[1].explain.text` | Keep the coins apart: HH, HT, TH and TT are equally likely. One head covers HT and TH. So the... | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `quiz[2].prose` | A bet pays £12 if two fair dice total 7, and nothing otherwise. | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `quiz[2].question` | What is its fair price, the average payout per roll, in pounds? | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `quiz[2].widget.answer` | 2 | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `quiz[2].widget.accept` | £2.00: $\text{£}12 \times \tfrac{6}{36}$. | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `quiz[2].widget.wrong[0].value` | 1.0909 | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `quiz[2].widget.wrong[1].value` | 6 | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `quiz[2].widget.wrong[2].value` | 0.3333 | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `quiz[2].feedback.correct` | £72 over 36 rolls is £2.00 a roll. | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `quiz[2].feedback.generic` | Not quite right. Count the winning rolls out of 36, then share the payout. | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `quiz[2].feedback.byKey.eleven` | You gave 7 a chance of $\tfrac{1}{11}$. The 11 totals are not equally likely. | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `quiz[2].feedback.byKey.half` | You split into 7 and not 7. Only 6 of the 36 rolls win. | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `quiz[2].feedback.byKey.one` | You counted one winning roll. Six rolls total 7. | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `quiz[2].explain.text` | Six of the 36 rolls win, so over 36 rolls the bet pays $6 \times \text{£}12 = \text{£}72$. Sh... | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `quiz[3].prose` | Counting works only on a list of equally likely outcomes. | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `quiz[3].question` | Which list is equally likely? | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `quiz[3].widget.options[0].text` | The number of heads in two fair tosses: 0, 1, 2 | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `quiz[3].widget.options[0].why` | 1 head happens two ways, HT and TH, while 0 and 2 happen one way each. | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `quiz[3].widget.options[1].text` | The total of two fair dice: 2 to 12 | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `quiz[3].widget.options[1].why` | 7 comes from six rolls and 2 from one. The totals are not equally likely. | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `quiz[3].widget.options[2].text` | The ordered results of two fair tosses: HH, HT, TH, TT | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `quiz[3].widget.options[2].correct` | true | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `quiz[3].widget.options[3].text` | Tomorrow's move of an index: up or down | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `quiz[3].widget.options[3].why` | Nothing makes up and down equally likely. That chance has to be measured. | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `quiz[3].feedback.correct` | Each ordered result has chance $\tfrac{1}{4}$. | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `quiz[3].feedback.generic` | Not quite right. Look for the list where no item hides several ways of happening. | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `quiz[3].explain.text` | HH, HT, TH and TT each have chance $\tfrac{1}{4}$. The other lists group outcomes unevenly, o... | correct | Ross 2.5 (equally likely outcomes); enumerated, L1 script, Monte Carlo of the totals |
| l2 | `screens[1].feedback.byKey.r*c*` | 33 per-cell lines of the form "(a, b) adds to n, not t" | correct | each sum and cell id recomputed by the ledger build |

## l3-events-as-sets.json

| file | JSON path | claim (short) | verdict | basis |
|---|---|---|---|---|
| l3 | `screens[0].prose` | Two dice again. The shaded rows are event $A$: the red die is even. Event $B$: the total is 8... | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[0].canvas.state.caption` | Shaded: event $A$ | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[0].question` | Tap every roll that is in both $A$ and $B$. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[0].widget.answer` | ["r2c6", "r4c4", "r4c5", "r4c6", "r6c2", "r6c3", "r6c4", "r6c5", "r6c6"] | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[0].widget.wrong[0].set` | ["r2c6", "r3c5", "r3c6", "r4c4", "r4c5", "r4c6", "r5c3", "r5c4", "r5c5", "r5c6", "r6c2", "r6c... | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[0].widget.wrong[1].set` | ["r2c1", "r2c2", "r2c3", "r2c4", "r2c5", "r2c6", "r4c1", "r4c2", "r4c3", "r4c4", "r4c5", "r4c... | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[0].hints[0].text` | Stay inside the shaded rows. Which of their cells total 8 or more? | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[0].hints[1].text` | In row 4, the total reaches 8 from (4, 4) onwards. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[0].hints[2].text` | Row 2 needs blue 6, row 4 needs blue 4 or more, and row 6 needs blue 2 or more. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[0].feedback.correct` | Nine rolls are in both events. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[0].feedback.generic` | Not quite right. Keep only shaded cells whose total is 8 or more. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[0].feedback.byKey.r1c1` | (1, 1) is in neither event. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[0].feedback.byKey.r1c2` | (1, 2) is in neither event. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[0].feedback.byKey.r1c3` | (1, 3) is in neither event. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[0].feedback.byKey.r1c4` | (1, 4) is in neither event. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[0].feedback.byKey.r1c5` | (1, 5) is in neither event. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[0].feedback.byKey.r1c6` | (1, 6) is in neither event. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[0].feedback.byKey.r2c1` | (2, 1) is in $A$, but its total is 3, under 8. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[0].feedback.byKey.r2c2` | (2, 2) is in $A$, but its total is 4, under 8. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[0].feedback.byKey.r2c3` | (2, 3) is in $A$, but its total is 5, under 8. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[0].feedback.byKey.r2c4` | (2, 4) is in $A$, but its total is 6, under 8. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[0].feedback.byKey.r2c5` | (2, 5) is in $A$, but its total is 7, under 8. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[0].feedback.byKey.r2c6` | You missed (2, 6): red 2 is even and the total is 8. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[0].feedback.byKey.r3c1` | (3, 1) is in neither event. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[0].feedback.byKey.r3c2` | (3, 2) is in neither event. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[0].feedback.byKey.r3c3` | (3, 3) is in neither event. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[0].feedback.byKey.r3c4` | (3, 4) is in neither event. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[0].feedback.byKey.r3c5` | (3, 5) totals 8, but its red die is odd, so it is not in $A$. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[0].feedback.byKey.r3c6` | (3, 6) totals 9, but its red die is odd, so it is not in $A$. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[0].feedback.byKey.r4c1` | (4, 1) is in $A$, but its total is 5, under 8. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[0].feedback.byKey.r4c2` | (4, 2) is in $A$, but its total is 6, under 8. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[0].feedback.byKey.r4c3` | (4, 3) is in $A$, but its total is 7, under 8. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[0].feedback.byKey.r4c4` | You missed (4, 4): red 4 is even and the total is 8. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[0].feedback.byKey.r4c5` | You missed (4, 5): red 4 is even and the total is 9. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[0].feedback.byKey.r4c6` | You missed (4, 6): red 4 is even and the total is 10. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[0].feedback.byKey.r5c1` | (5, 1) is in neither event. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[0].feedback.byKey.r5c2` | (5, 2) is in neither event. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[0].feedback.byKey.r5c3` | (5, 3) totals 8, but its red die is odd, so it is not in $A$. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[0].feedback.byKey.r5c4` | (5, 4) totals 9, but its red die is odd, so it is not in $A$. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[0].feedback.byKey.r5c5` | (5, 5) totals 10, but its red die is odd, so it is not in $A$. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[0].feedback.byKey.r5c6` | (5, 6) totals 11, but its red die is odd, so it is not in $A$. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[0].feedback.byKey.r6c1` | (6, 1) is in $A$, but its total is 7, under 8. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[0].feedback.byKey.r6c2` | You missed (6, 2): red 6 is even and the total is 8. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[0].feedback.byKey.r6c3` | You missed (6, 3): red 6 is even and the total is 9. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[0].feedback.byKey.r6c4` | You missed (6, 4): red 6 is even and the total is 10. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[0].feedback.byKey.r6c5` | You missed (6, 5): red 6 is even and the total is 11. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[0].feedback.byKey.r6c6` | You missed (6, 6): red 6 is even and the total is 12. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[0].feedback.byKey.all-b` | You shaded all of $B$. Rolls with an odd red die are not in $A$. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[0].feedback.byKey.all-a` | You shaded all of $A$. Some of those rolls total less than 8. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[0].explain.text` | You found 9 rolls: (2, 6), then (4, 4) to (4, 6), then (6, 2) to (6, 6). Each is in $A$ and i... | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[1].prose` | A Venn diagram sorts the same 36 rolls into four regions. Each number counts the rolls in its... | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[1].question` | Tap every region that lies inside $A$. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[1].widget.answer` | ["A", "AB"] | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[1].widget.wrong[0].set` | ["A"] | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[1].hints[0].text` | $A$ is the whole left circle, overlap included. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[1].hints[1].text` | The overlap is inside the left circle too. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[1].feedback.correct` | $A$ is the whole left circle: $9 + 9 = 18$ rolls. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[1].feedback.generic` | Not quite right. Select every part of the left circle. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[1].feedback.byKey.a-only` | You tapped only the part of $A$ outside $B$. The overlap is inside $A$ too. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[1].feedback.byKey.B` | That region is $B$ without $A$: rolls with an odd red die. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[1].feedback.byKey.none` | That region is outside both circles. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[1].feedback.byKey.AB` | You missed the overlap. Rolls in both events are still in $A$. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[1].explain.text` | $A$ is the whole left circle: 9 rolls in $A$ only and 9 in the overlap. That makes $/A/ = 18$... | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[2].prose` | Your 9 rolls from the grid sit in the overlap: in $A$ **and** in $B$. That region is the **in... | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[2].question` | Tap every region of $A \cup B$. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[2].widget.answer` | ["A", "AB", "B"] | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[2].widget.wrong[0].set` | ["A", "B"] | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[2].widget.wrong[1].set` | ["AB"] | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[2].hints[0].text` | A roll is in $A \cup B$ if it is in at least one of the circles. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[2].hints[1].text` | This region is in both, so it is in at least one. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[2].hints[2].text` | Select all three regions inside the circles. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[2].feedback.correct` | Everything inside either circle: $9 + 9 + 6 = 24$ rolls. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[2].feedback.generic` | Not quite right. Select every region inside at least one circle. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[2].feedback.byKey.xor` | You left out the overlap. “Or” includes rolls in both. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[2].feedback.byKey.and` | That is $A \cap B$, both at once. The union needs only one of them. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[2].feedback.byKey.none` | The outside region holds rolls in neither event. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[2].explain.text` | $A \cup B$ is everything inside either circle: $9 + 9 + 6 = 24$ rolls. $A \cap B$ is only the... | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[3].prose` | The rolls where $A$ does **not** happen form the **complement** of $A$, written $A^c$. Here $... | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[3].question` | Tap every region of $A^c$. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[3].widget.answer` | ["B", "none"] | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[3].widget.wrong[0].set` | ["none"] | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[3].widget.wrong[1].set` | ["B"] | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[3].hints[0].text` | $A^c$ is everything outside the left circle. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[3].hints[1].text` | This region is outside the left circle. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[3].hints[2].text` | Select the part of $B$ outside $A$, and the region outside both. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[3].feedback.correct` | Everything outside $A$: $6 + 12 = 18$ rolls. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[3].feedback.generic` | Not quite right. Select every region outside the left circle. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[3].feedback.byKey.outside` | You tapped only the outside. Rolls in $B$ but not $A$ are also outside $A$. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[3].feedback.byKey.b-only` | You missed the outside region. Rolls in neither event are not in $A$ either. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[3].feedback.byKey.A` | That region is inside $A$. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[3].feedback.byKey.AB` | The overlap is inside $A$. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[3].explain.text` | $A^c$ is everything outside the left circle: $6 + 12 = 18$ rolls. $A$ and $A^c$ cover all 36 ... | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[4].prose` | The shaded region is “neither $A$ nor $B$”: outside both circles. That is the complement of t... | correct | Ross 2.2 (De Morgan); all 256 pairs of subsets checked, L1 script |
| l3 | `screens[4].question` | Which other expression names the same region? | correct | Ross 2.2 (De Morgan); all 256 pairs of subsets checked, L1 script |
| l3 | `screens[4].widget.options[0].text` | $A^c \cup B^c$ | correct | Ross 2.2 (De Morgan); all 256 pairs of subsets checked, L1 script |
| l3 | `screens[4].widget.options[0].why` | You took both complements but kept the union. $A^c \cup B^c$ also holds $A$ only and $B$ only. | correct | Ross 2.2 (De Morgan); all 256 pairs of subsets checked, L1 script |
| l3 | `screens[4].widget.options[1].text` | $A^c \cap B^c$ | correct | Ross 2.2 (De Morgan); all 256 pairs of subsets checked, L1 script |
| l3 | `screens[4].widget.options[1].correct` | true | correct | Ross 2.2 (De Morgan); all 256 pairs of subsets checked, L1 script |
| l3 | `screens[4].widget.options[2].text` | $(A \cap B)^c$ | correct | Ross 2.2 (De Morgan); all 256 pairs of subsets checked, L1 script |
| l3 | `screens[4].widget.options[2].why` | That removes only the overlap. It still holds $A$ only and $B$ only. | correct | Ross 2.2 (De Morgan); all 256 pairs of subsets checked, L1 script |
| l3 | `screens[4].widget.options[3].text` | $A^c$ | correct | Ross 2.2 (De Morgan); all 256 pairs of subsets checked, L1 script |
| l3 | `screens[4].widget.options[3].why` | $A^c$ also holds $B$ only. “Neither” means outside $B$ too. | correct | Ross 2.2 (De Morgan); all 256 pairs of subsets checked, L1 script |
| l3 | `screens[4].hints[0].text` | “Neither” means not in $A$, and also not in $B$. | correct | Ross 2.2 (De Morgan); all 256 pairs of subsets checked, L1 script |
| l3 | `screens[4].hints[1].text` | Where is $A^c$? Where is $B^c$? Find where they meet. | correct | Ross 2.2 (De Morgan); all 256 pairs of subsets checked, L1 script |
| l3 | `screens[4].hints[2].text` | $A^c$ is outside the left circle and $B^c$ outside the right. Both hold only in the outside r... | correct | Ross 2.2 (De Morgan); all 256 pairs of subsets checked, L1 script |
| l3 | `screens[4].feedback.correct` | Not in $A$ and not in $B$: the outside region. | correct | Ross 2.2 (De Morgan); all 256 pairs of subsets checked, L1 script |
| l3 | `screens[4].feedback.generic` | Not quite right. Shade $A^c$ and $B^c$ in your head, and find where both hold. | correct | Ross 2.2 (De Morgan); all 256 pairs of subsets checked, L1 script |
| l3 | `screens[4].explain.text` | Not in $A$ and not in $B$ is the same as not in $A \cup B$: $(A \cup B)^c = A^c \cap B^c$. Li... | correct | Ross 2.2 (De Morgan); all 256 pairs of subsets checked, L1 script |
| l3 | `screens[5].prose` | New events. $A$: the total is 7. $B$: the dice match, a double. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[5].question` | What is $P(A \cup B)$? Give a fraction or a decimal. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[5].widget.answer` | 0.333333 | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[5].widget.accept` | Any form equal to $\tfrac{12}{36} = \tfrac{1}{3}$. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[5].widget.wrong[0].value` | 0.305556 | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[5].widget.wrong[1].value` | 0.166667 | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[5].widget.wrong[2].value` | 0 | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[5].hints[0].text` | Can a double total 7? | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[5].hints[1].text` | The overlap is empty. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[5].hints[2].text` | A double totals 2, 4, 6, 8, 10 or 12, never 7. So $/A \cup B/ = 6 + 6$. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[5].feedback.correct` | $\tfrac{6 + 6}{36} = \tfrac{1}{3}$, with nothing to take away. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[5].feedback.generic` | Not quite right. Count the rolls in either circle, then divide by 36. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[5].feedback.byKey.subtract` | You took away an overlap of 1. No double totals 7, so the overlap is empty. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[5].feedback.byKey.one` | That is one event alone. The union holds the rolls of both. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[5].feedback.byKey.both` | That is $P(A \cap B)$, which is 0 here. The union holds 12 rolls. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[5].explain.text` | A double always has an even total, so no roll is in both: $A \cap B = \varnothing$. Events li... | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[6].prose` | Back to $A$, red die even, and $B$, total 8 or more. A bet pays if $A$ or $B$ happens. Jo cou... | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[6].question` | On how many of the 36 rolls does the bet pay? | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[6].widget.answer` | 24 | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[6].widget.accept` | 24 exactly: $9 + 9 + 6$, or $18 + 15 - 9$. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[6].widget.wrong[0].value` | 15 | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[6].widget.wrong[1].value` | 33 | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[6].widget.wrong[2].value` | 9 | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[6].widget.wrong[3].value` | 36 | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[6].hints[0].text` | Does the bet pay on a roll that is in both $A$ and $B$? | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[6].hints[1].text` | Jo left this region out. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[6].hints[2].text` | Add all three regions inside the circles: $9 + 9 + 6$. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[6].feedback.correct` | All three regions inside the circles: 24 rolls. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[6].feedback.generic` | Not quite right. The bet pays on every roll inside either circle. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[6].feedback.byKey.xor` | You counted Jo's way and left out the overlap. “Or” includes rolls in both, so add the 9 there. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[6].feedback.byKey.double` | You added $/A/ = 18$ and $/B/ = 15$. The 9 overlap rolls are in both, so you counted them twice. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[6].feedback.byKey.and` | That is $A \cap B$. The bet also pays on rolls in just one event. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[6].feedback.byKey.all` | The 12 rolls outside both circles do not pay. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[6].explain.text` | In probability “or” is inclusive, so the bet pays in all three regions: $9 + 9 + 6 = 24$ roll... | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[7].prose` | Your fix was to take the overlap away once. Let us turn that into a rule for any two events $... | correct | Ross 2.4 Prop. 4.3 by counting; all pairs of subsets checked, L1 script |
| l3 | `screens[7].question` | Put the lines of the argument in order. | correct | Ross 2.4 Prop. 4.3 by counting; all pairs of subsets checked, L1 script |
| l3 | `screens[7].widget.lines[0].text` | $/A \cup B/ = /A \text{ only}/ + /A \cap B/ + /B \text{ only}/$: three regions that do not ov... | correct | Ross 2.4 Prop. 4.3 by counting; all pairs of subsets checked, L1 script |
| l3 | `screens[7].widget.lines[1].text` | $/A/ + /B/ = /A \text{ only}/ + 2/A \cap B/ + /B \text{ only}/$: the overlap sits in both cir... | correct | Ross 2.4 Prop. 4.3 by counting; all pairs of subsets checked, L1 script |
| l3 | `screens[7].widget.lines[2].text` | Subtract the two lines: $/A \cup B/ = /A/ + /B/ - /A \cap B/$. | correct | Ross 2.4 Prop. 4.3 by counting; all pairs of subsets checked, L1 script |
| l3 | `screens[7].widget.lines[3].text` | Divide by $/S/$: $P(A \cup B) = P(A) + P(B) - P(A \cap B)$. | correct | Ross 2.4 Prop. 4.3 by counting; all pairs of subsets checked, L1 script |
| l3 | `screens[7].widget.answer` | ["split", "twice", "subtract", "divide"] | correct | Ross 2.4 Prop. 4.3 by counting; all pairs of subsets checked, L1 script |
| l3 | `screens[7].hints[0].text` | Start by splitting the union into its regions. | correct | Ross 2.4 Prop. 4.3 by counting; all pairs of subsets checked, L1 script |
| l3 | `screens[7].hints[1].text` | Then compare that with what $/A/ + /B/$ counts: this region is in both circles. | correct | Ross 2.4 Prop. 4.3 by counting; all pairs of subsets checked, L1 script |
| l3 | `screens[7].hints[2].text` | Union first, then $/A/ + /B/$, then subtract, then divide by $/S/$. | correct | Ross 2.4 Prop. 4.3 by counting; all pairs of subsets checked, L1 script |
| l3 | `screens[7].feedback.correct` | The overlap is counted twice, so it comes off once. | correct | Ross 2.4 Prop. 4.3 by counting; all pairs of subsets checked, L1 script |
| l3 | `screens[7].feedback.generic` | Not quite right. Write both counts in terms of the three regions before you subtract. | correct | Ross 2.4 Prop. 4.3 by counting; all pairs of subsets checked, L1 script |
| l3 | `screens[7].explain.text` | $/A/ + /B/$ counts the overlap twice, so we subtract it once. Dividing by $/S/$ turns counts ... | correct | Ross 2.4 Prop. 4.3 by counting; all pairs of subsets checked, L1 script |
| l3 | `screens[8].prose` | Twenty trading days of one stock. Event $A$: it closes above £50. Event $B$: volume is above ... | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[8].canvas.state.caption` | $A$: close above £50. $B$: volume above 1 million shares. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[8].question` | On how many of the 20 days did $A$ or $B$ happen? | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[8].widget.answer` | 14 | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[8].widget.accept` | 14 exactly: $11 + 8 - 5$. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[8].widget.wrong[0].value` | 19 | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[8].widget.wrong[1].value` | 9 | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[8].widget.wrong[2].value` | 5 | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[8].widget.wrong[3].value` | 6 | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[8].hints[0].text` | Count the $A$ days, the $B$ days, and the days with both. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[8].hints[1].text` | These five days had both. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[8].hints[2].text` | $/A/ = 11$, $/B/ = 8$ and $/A \cap B/ = 5$. So $/A \cup B/ = 11 + 8 - 5$. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[8].feedback.correct` | $11 + 8 - 5 = 14$ days. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[8].feedback.generic` | Not quite right. Count $/A/$, $/B/$ and $/A \cap B/$, then take the overlap away once. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[8].feedback.byKey.double` | You added 11 and 8. The 5 days with both were counted twice. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[8].feedback.byKey.xor` | You counted days with exactly one event. Days with both count too. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[8].feedback.byKey.and` | That is $A \cap B$. The union also holds days with just one event. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[8].feedback.byKey.neither` | That is the days in neither event, $(A \cup B)^c$. Take it from 20. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `screens[8].explain.text` | 11 days closed above £50 and 8 had high volume, but 5 days had both. So $/A \cup B/ = 11 + 8 ... | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `summary.ideas` | ["“And” is the intersection $A \\cap B$, “or” is the union $A \\cup B$, and “not” is the comp... | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `summary.formula.name` | Union by counting | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `summary.formula.tex` | /A \cup B/ = /A/ + /B/ - /A \cap B/ | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `summary.formula.note` | Disjoint events have $A \cap B = \varnothing$, so their counts simply add. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `summary.trap` | Reading “$A$ or $B$” as “exactly one of them” leaves out the overlap, where both happen. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `quiz[0].prose` | Over 50 trading days, signal X fired on 18 days and signal Y on 14. Both fired on 6 of those ... | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `quiz[0].question` | What fraction of the days had X or Y firing? Give a fraction or a decimal. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `quiz[0].widget.answer` | 0.52 | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `quiz[0].widget.accept` | Any form equal to $\tfrac{26}{50} = 0.52$. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `quiz[0].widget.wrong[0].value` | 0.64 | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `quiz[0].widget.wrong[1].value` | 0.4 | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `quiz[0].widget.wrong[2].value` | 0.12 | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `quiz[0].feedback.correct` | $\tfrac{18 + 14 - 6}{50} = \tfrac{26}{50}$. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `quiz[0].feedback.generic` | Not quite right. Add the two counts, then take the overlap away once. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `quiz[0].feedback.byKey.double` | You added 18 and 14. The 6 days with both were counted twice. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `quiz[0].feedback.byKey.xor` | You left out the 6 days with both. “Or” includes them. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `quiz[0].feedback.byKey.and` | That is the share with both signals. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `quiz[0].explain.text` | $/X \cup Y/ = 18 + 14 - 6 = 26$ days. So the share is $\tfrac{26}{50} = 0.52$. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `quiz[1].prose` | $A$ and $B$ are two events in the same sample space. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `quiz[1].question` | Which set is “neither $A$ nor $B$”? | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `quiz[1].widget.options[0].text` | $A^c \cup B^c$ | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `quiz[1].widget.options[0].why` | That is “not both”. It also holds outcomes in exactly one of $A$ and $B$. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `quiz[1].widget.options[1].text` | $(A \cap B)^c$ | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `quiz[1].widget.options[1].why` | That is “not both” again, the same as $A^c \cup B^c$. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `quiz[1].widget.options[2].text` | $A^c \cap B$ | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `quiz[1].widget.options[2].why` | That is $B$ without $A$. Neither means outside $B$ as well. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `quiz[1].widget.options[3].text` | $(A \cup B)^c$ | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `quiz[1].widget.options[3].correct` | true | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `quiz[1].feedback.correct` | Outside the union: $(A \cup B)^c = A^c \cap B^c$. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `quiz[1].feedback.generic` | Not quite right. Neither means outside both circles. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `quiz[1].explain.text` | Neither $A$ nor $B$ means outside both circles. That is the complement of the union, $(A \cup... | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `quiz[2].prose` | A stock closes up, flat or down. $P(\text{up}) = 0.45$ and $P(\text{down}) = 0.4$. Up and dow... | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `quiz[2].question` | What is $P(\text{flat})$? Give a decimal. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `quiz[2].widget.answer` | 0.15 | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `quiz[2].widget.accept` | 0.15: $1 - (0.45 + 0.4)$. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `quiz[2].widget.wrong[0].value` | 0.85 | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `quiz[2].widget.wrong[1].value` | 0.55 | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `quiz[2].widget.wrong[2].value` | 0.6 | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `quiz[2].feedback.correct` | Flat is the complement of up or down: $1 - 0.85$. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `quiz[2].feedback.generic` | Not quite right. Find $P(\text{up or down})$ first. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `quiz[2].feedback.byKey.up-or-down` | That is $P(\text{up or down})$. Flat is everything else. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `quiz[2].feedback.byKey.not-up` | That is $P(\text{not up})$, which includes down days. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `quiz[2].feedback.byKey.not-down` | That is $P(\text{not down})$, which includes up days. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `quiz[2].explain.text` | Up and down share no outcome, so $P(\text{up or down}) = 0.45 + 0.4 = 0.85$. Flat is the comp... | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `quiz[3].prose` | Two fair dice. $A$: the total is 10 or more, 6 rolls. $B$: a double, 6 rolls. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `quiz[3].question` | What is $P(A \cup B)$? Give a fraction or a decimal. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `quiz[3].widget.answer` | 0.277778 | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `quiz[3].widget.accept` | Any form equal to $\tfrac{10}{36} = \tfrac{5}{18}$. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `quiz[3].widget.wrong[0].value` | 0.333333 | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `quiz[3].widget.wrong[1].value` | 0.222222 | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `quiz[3].widget.wrong[2].value` | 0.055556 | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `quiz[3].feedback.correct` | $\tfrac{6 + 6 - 2}{36} = \tfrac{10}{36}$. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `quiz[3].feedback.generic` | Not quite right. Find the rolls in both events first. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `quiz[3].feedback.byKey.double` | You added 6 and 6. (5, 5) and (6, 6) are in both, so they were counted twice. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `quiz[3].feedback.byKey.xor` | You left out (5, 5) and (6, 6), the rolls in both. | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `quiz[3].feedback.byKey.and` | That is $P(A \cap B)$: just (5, 5) and (6, 6). | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |
| l3 | `quiz[3].explain.text` | The doubles with a total of 10 or more are (5, 5) and (6, 6), so $/A \cap B/ = 2$. Then $/A \... | correct | Ross 2.2 (union, intersection, complement); enumerated, L1 script |

## l4-does-not-happen.json

| file | JSON path | claim (short) | verdict | basis |
|---|---|---|---|---|
| l4 | `screens[0].prose` | Toss a fair coin three times. Each of the 8 paths is equally likely. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[0].question` | Tap every path with at least one head. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[0].widget.answer` | ["h-h-h", "h-h-t", "h-t-h", "h-t-t", "t-h-h", "t-h-t", "t-t-h"] | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[0].widget.wrong[0].set` | ["h-t-t", "t-h-t", "t-t-h"] | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[0].widget.wrong[1].set` | ["h-h-t", "h-t-h", "h-t-t", "t-h-h", "t-h-t", "t-t-h"] | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[0].hints[0].text` | “At least one head” means one, two or three heads. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[0].hints[1].text` | Only one path has no head at all. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[0].hints[2].text` | Tap every path except TTT. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[0].feedback.correct` | Seven paths: every path except TTT. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[0].feedback.generic` | Not quite right. Tap each path that has an H anywhere in it. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[0].feedback.byKey.exactly-one` | Those have exactly one head. “At least one” also takes two or three. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[0].feedback.byKey.no-hhh` | You missed HHH. Three heads is at least one head. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[0].feedback.byKey.t-t-t` | TTT has no heads at all. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[0].feedback.byKey.h-h-h` | You missed HHH. Three heads is at least one head. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[0].feedback.byKey.h-h-t` | You missed HHT. Two heads is at least one. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[0].feedback.byKey.h-t-h` | You missed HTH. Two heads is at least one. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[0].feedback.byKey.t-h-h` | You missed THH. Two heads is at least one. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[0].feedback.byKey.h-t-t` | You missed HTT. One head is enough. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[0].feedback.byKey.t-h-t` | You missed THT. One head is enough. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[0].feedback.byKey.t-t-h` | You missed TTH. One head is enough. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[0].explain.text` | You tapped 7 paths, and only TTT was left out. So $P(\text{at least one head}) = \tfrac{7}{8}... | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[1].prose` | Now roll one fair die again and again. Move the slider to change the number of rolls. The dot... | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[1].question` | What is the smallest number of rolls that makes at least one six more likely than not? | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[1].widget.answer` | 4 | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[1].widget.accept` | 4: the chance is 0.4213 at 3 rolls and 0.5177 at 4. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[1].widget.wrong[0].value` | 3 | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[1].widget.wrong[1].value` | 6 | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[1].hints[0].text` | Move the slider one roll at a time and read the caption. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[1].hints[1].text` | Compare the dot with the dashed line at $\tfrac{1}{2}$. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[1].hints[2].text` | At 3 rolls the chance is 0.4213; at 4 it is 0.5177. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[1].feedback.correct` | Four rolls: the chance first passes $\tfrac{1}{2}$ at 0.5177. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[1].feedback.generic` | Not quite right. Find the first number of rolls where the dot is above the dashed line. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[1].feedback.byKey.adding` | You may have added $\tfrac{1}{6}$ per roll: $3 \times \tfrac{1}{6} = \tfrac{1}{2}$. The dot a... | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[1].feedback.byKey.six` | Six rolls give 0.6651, above $\tfrac{1}{2}$, but fewer rolls already do it. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[1].explain.text` | The chance passes $\tfrac{1}{2}$ at 4 rolls, with 0.5177. It keeps climbing but never reaches... | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[2].prose` | In the coin tree, “no heads” held the one path you skipped. It is the complement of “at least... | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[2].question` | Four fair tosses. What is $P(\text{at least one head})$? Give a fraction or a decimal. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[2].widget.answer` | 0.9375 | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[2].widget.accept` | Any form equal to $\tfrac{15}{16}$, or 0.9375. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[2].widget.wrong[0].value` | 0.0625 | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[2].widget.wrong[1].value` | 2 | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[2].widget.wrong[2].value` | 0.875 | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[2].widget.wrong[3].value` | 0.5 | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[2].hints[0].text` | How many paths have no head at all? | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[2].hints[1].text` | Only this path has no head. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[2].hints[2].text` | 16 paths, and one has no head: $1 - \tfrac{1}{16}$. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[2].feedback.correct` | $1 - \tfrac{1}{16} = \tfrac{15}{16}$. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[2].feedback.generic` | Not quite right. Find $P(\text{no heads})$ first, then take it from 1. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[2].feedback.byKey.none` | That is the chance of no heads, TTTT. Take it from 1. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[2].feedback.byKey.adding` | You added $\tfrac{1}{2}$ four times and passed 1. A chance can never exceed 1. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[2].feedback.byKey.three` | That is three tosses. Four tosses give 16 paths, and only TTTT has no head. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[2].feedback.byKey.half` | That is the chance for one toss. More tosses make a head more likely. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[2].explain.text` | Four tosses make $2^4 = 16$ equally likely paths, and only TTTT has no head. So $P(\text{at l... | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[3].prose` | Back to the die, rolled four times. An outcome is a list of four faces, such as 3, 6, 1, 6. T... | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[3].canvas.state.caption` | Faces each roll can show | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[3].question` | How many of the 1296 outcomes contain no six? | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[3].widget.answer` | 625 | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[3].widget.accept` | 625 exactly: $5^4$. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[3].widget.wrong[0].value` | 671 | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[3].widget.wrong[1].value` | 20 | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[3].widget.wrong[2].value` | 1292 | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[3].widget.wrong[3].value` | 1080 | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[3].hints[0].text` | With no six allowed, how many faces can each roll show? | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[3].hints[1].text` | Read the No six row. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[3].hints[2].text` | $5 \times 5 \times 5 \times 5 = 5^4$. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[3].feedback.correct` | $5^4 = 625$ outcomes have no six. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[3].feedback.generic` | Not quite right. Each roll has 5 faces left, and the choices multiply. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[3].feedback.byKey.at-least` | That counts outcomes with at least one six. We want the ones with none. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[3].feedback.byKey.added` | You added 5 four times. Each roll's 5 faces pair with every choice on the others, so multiply. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[3].feedback.byKey.minus-four` | You took away only 4 outcomes, one per roll. Hundreds of outcomes contain a six. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[3].feedback.byKey.minus-one-roll` | You took away the $6^3 = 216$ outcomes with a six on one roll. A six can be on any roll. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[3].explain.text` | Each roll can show 1 to 5, so $5^4 = 625$ outcomes have no six. That leaves $1296 - 625 = 671... | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[4].prose` | So 625 of the 1296 equally likely outcomes have no six. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[4].canvas.state.caption` | Faces each roll can show | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[4].question` | What is $P(\text{at least one six in four rolls})$? Give a fraction or a decimal to 4 places. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[4].widget.answer` | 0.517747 | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[4].widget.accept` | Any form equal to $\tfrac{671}{1296}$, or 0.5177 to 4 places. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[4].widget.wrong[0].value` | 0.482253 | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[4].widget.wrong[1].value` | 0.666667 | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[4].widget.wrong[2].value` | 0.166667 | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[4].hints[0].text` | What is $P(\text{no six})$? | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[4].hints[1].text` | 625 of the 1296 outcomes have no six. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[4].hints[2].text` | $1 - \tfrac{625}{1296} = \tfrac{671}{1296}$. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[4].feedback.correct` | $1 - \tfrac{625}{1296} = \tfrac{671}{1296} \approx 0.5177$. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[4].feedback.generic` | Not quite right. Find $P(\text{no six})$, then take it from 1. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[4].feedback.byKey.none` | That is $P(\text{no six}) = \tfrac{625}{1296}$. Take it from 1. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[4].feedback.byKey.adding` | You added $\tfrac{1}{6}$ four times. The next screen shows why that overcounts. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[4].feedback.byKey.one` | That is the chance for one roll. Four rolls give more chances of a six. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[4].explain.text` | $P(\text{no six}) = \tfrac{625}{1296} = \left(\tfrac{5}{6}\right)^4$. So $P(\text{at least on... | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[5].prose` | Sam says each roll gives a six with chance $\tfrac{1}{6}$, so four rolls give $4 \times \tfra... | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[5].canvas.state.caption` | Row 6: a six first. Column 6: a six second. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[5].question` | Sam's method gives $\tfrac{2}{6} = \tfrac{12}{36}$ for two rolls. What is the true $P(\text{a... | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[5].widget.options[0].text` | $\dfrac{12}{36}$ | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[5].widget.options[0].why` | You added the row and the column. The cell (6, 6) is in both, so it was counted twice. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[5].widget.options[1].text` | $\dfrac{11}{36}$ | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[5].widget.options[1].correct` | true | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[5].widget.options[2].text` | $\dfrac{25}{36}$ | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[5].widget.options[2].why` | That is the chance of no six: the unshaded cells. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[5].widget.options[3].text` | $\dfrac{1}{6}$ | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[5].widget.options[3].why` | That is one roll. The second roll adds more ways to see a six. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[5].hints[0].text` | How many shaded cells are there, counting each cell once? | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[5].hints[1].text` | This cell is in the row and in the column. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[5].hints[2].text` | Row 6 has 6 cells and column 6 has 6. They share (6, 6), so $6 + 6 - 1 = 11$. Or: $36 - 25 = ... | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[5].feedback.correct` | 11 cells, with (6, 6) counted once. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[5].feedback.generic` | Not quite right. Count the shaded cells, each one once. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[5].feedback.byKey.sam` | You added the row and the column, as Sam did. The cell (6, 6) is in both, so it was counted t... | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[5].explain.text` | Adding $\tfrac{1}{6}$ per roll counts (6, 6) twice, so it overshoots. With four rolls it over... | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[6].prose` | On the curve, the chance climbed towards 1 but never reached it. When is “at least one” certain? | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[6].canvas.state.caption` | Rolls: 24. Chance of at least one six: 0.9874 | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[6].question` | For which of these is $P(\text{at least one}) = 1$ exactly? | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[6].widget.options[0].text` | At least one six in 100 rolls of a fair die | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[6].widget.options[0].why` | Very close, but $P(\text{no six}) = \left(\tfrac{5}{6}\right)^{100}$ is above 0. So the chanc... | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[6].widget.options[1].text` | At least one six in 6 rolls of a fair die | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[6].widget.options[1].why` | Adding $\tfrac{1}{6}$ six times says 1. The true chance is $1 - \left(\tfrac{5}{6}\right)^6 \... | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[6].widget.options[2].text` | At least one head in 3 tosses of a coin with heads on both sides | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[6].widget.options[2].correct` | true | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[6].widget.options[3].text` | At least one up day in 20 days, when each day is up with chance 0.6 | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[6].widget.options[3].why` | $P(\text{no up day}) = 0.4^{20}$ is tiny but not 0. The chance is about 0.99999999. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[6].hints[0].text` | At least one is certain only when none is impossible. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[6].hints[1].text` | Which case has $P(\text{none}) = 0$? | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[6].hints[2].text` | A two-headed coin can never show tails, so “no heads” has chance 0. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[6].feedback.correct` | Only the two-headed coin makes “none” impossible. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[6].feedback.generic` | Not quite right. Look for the case where “none” cannot happen at all. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[6].explain.text` | $P(\text{at least one}) = 1$ exactly when $P(\text{none}) = 0$. A two-headed coin never lands... | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[7].prose` | Now the rule behind the curve. Roll a fair die $n$ times: $S$ has $6^n$ equally likely outcom... | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[7].question` | Write $P(\text{at least one six in } n \text{ rolls})$ in terms of $n$. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[7].widget.answer` | 1-\left(\frac{5}{6}\right)^n | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[7].widget.accept` | ["1-(5/6)^n", "1 - (5/6)^n", "1-5^n/6^n", "(6^n-5^n)/6^n", "1-(5^n)/(6^n)"] | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[7].widget.wrong[0].tex` | \left(\frac{5}{6}\right)^n | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[7].widget.wrong[1].tex` | \frac{n}{6} | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[7].widget.wrong[2].tex` | 1-\left(\frac{1}{6}\right)^n | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[7].hints[0].text` | “At least one six” is the complement of which event? | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[7].hints[1].text` | Use $P(\text{at least one}) = 1 - P(\text{none})$. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[7].hints[2].text` | Take $\left(\tfrac{5}{6}\right)^n$ from 1. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[7].feedback.correct` | $1 - \left(\tfrac{5}{6}\right)^n$: the curve you moved along. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[7].feedback.generic` | Not quite right. Write the complement of “no six”. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[7].feedback.byKey.none` | That is $P(\text{no six})$. Take it from 1. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[7].feedback.byKey.adding` | That adds $\tfrac{1}{6}$ per roll, which counts outcomes with several sixes more than once. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[7].feedback.byKey.all-six` | $\left(\tfrac{1}{6}\right)^n$ is the chance of all sixes. The complement of at least one six ... | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[7].explain.text` | “At least one six” and “no six” share no outcome and cover $S$. So $P(\text{at least one six}... | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[8].prose` | A trader has a losing day with chance 0.4, independently each day. For independent days, chan... | imprecise | finding 5: 'independently' is used with the product rule before its meaning is given anywhere in the course (first gloss is l7 screen 4); Ross 3.4 |
| l4 | `screens[8].canvas.state.caption` | Each day is independent of the others | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[8].question` | What is $P(\text{at least one losing day})$? Give a decimal to 4 places. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[8].widget.answer` | 0.92224 | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[8].widget.accept` | 0.9222: $1 - 0.6^5 = 0.92224$. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[8].widget.wrong[0].value` | 2.0 | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[8].widget.wrong[1].value` | 0.07776 | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[8].widget.wrong[2].value` | 0.01024 | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[8].widget.wrong[3].value` | 0.98976 | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[8].hints[0].text` | What is the complement of “at least one losing day”? | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[8].hints[1].text` | No losing day means five days that are not losing. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[8].hints[2].text` | $P(\text{none}) = 0.6^5 = 0.07776$, so take it from 1. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[8].feedback.correct` | $1 - 0.6^5 = 0.92224$. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[8].feedback.generic` | Not quite right. Find the chance of no losing day, then take it from 1. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[8].feedback.byKey.adding` | You added 0.4 five times and passed 1. A chance cannot exceed 1. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[8].feedback.byKey.none` | That is $0.6^5$, the chance of no losing day. Take it from 1. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[8].feedback.byKey.all` | That is $0.4^5$, five losing days in a row. At least one is far more likely. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[8].feedback.byKey.wrong-comp` | You took the complement of five losing days. The complement of at least one losing day is no ... | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[8].explain.text` | No losing day needs five days that are not losing: $0.6^5 = 0.07776$. So $P(\text{at least on... | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[9].prose` | You place 10 limit orders in different stocks. Each fills with chance 0.2, independently of t... | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[9].canvas.state.caption` | One order | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[9].question` | What is the chance that none of the 10 orders fills? Give a decimal to 4 places. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[9].widget.answer` | 0.107374 | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[9].widget.accept` | 0.1074: $0.8^{10} = 0.10737\ldots$ | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[9].widget.wrong[0].value` | 0.892626 | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[9].widget.wrong[1].value` | 0.8 | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[9].widget.wrong[2].value` | 0.0 | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[9].hints[0].text` | None fills means every order misses. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[9].hints[1].text` | One order misses with chance 0.8. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[9].hints[2].text` | Ten independent misses: $0.8^{10}$. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[9].feedback.correct` | $0.8^{10} \approx 0.1074$. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[9].feedback.generic` | Not quite right. Multiply the chance of a miss once for each order. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[9].feedback.byKey.at-least` | That is the chance at least one fills, the complement. The question asks for none. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[9].feedback.byKey.one` | That is the chance one order misses. All ten must miss. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[9].feedback.byKey.all` | That is the chance all ten fill. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[9].explain.text` | Each order misses with chance 0.8, so all ten miss with chance $0.8^{10} \approx 0.1074$. The... | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `screens[10].prose` | In the 1650s the Chevalier de Méré made two even-money bets. Bet 1: at least one six in 4 rol... | correct | Pascal to Fermat, 29 July 1654 (de Mere); exact powers and Monte Carlo, L1 script |
| l4 | `screens[10].canvas.state.caption` | One roll of two dice: 1 double six in 36 | correct | Pascal to Fermat, 29 July 1654 (de Mere); exact powers and Monte Carlo, L1 script |
| l4 | `screens[10].question` | What is the chance of winning bet 2? Give a decimal to 4 places. | correct | Pascal to Fermat, 29 July 1654 (de Mere); exact powers and Monte Carlo, L1 script |
| l4 | `screens[10].widget.answer` | 0.491404 | correct | Pascal to Fermat, 29 July 1654 (de Mere); exact powers and Monte Carlo, L1 script |
| l4 | `screens[10].widget.accept` | 0.4914: $1 - \left(\tfrac{35}{36}\right)^{24}$. | correct | Pascal to Fermat, 29 July 1654 (de Mere); exact powers and Monte Carlo, L1 script |
| l4 | `screens[10].widget.wrong[0].value` | 0.666667 | correct | Pascal to Fermat, 29 July 1654 (de Mere); exact powers and Monte Carlo, L1 script |
| l4 | `screens[10].widget.wrong[1].value` | 0.508596 | correct | Pascal to Fermat, 29 July 1654 (de Mere); exact powers and Monte Carlo, L1 script |
| l4 | `screens[10].widget.wrong[2].value` | 0.517747 | correct | Pascal to Fermat, 29 July 1654 (de Mere); exact powers and Monte Carlo, L1 script |
| l4 | `screens[10].hints[0].text` | What is the chance one roll of two dice is not a double six? | correct | Pascal to Fermat, 29 July 1654 (de Mere); exact powers and Monte Carlo, L1 script |
| l4 | `screens[10].hints[1].text` | One cell of the 36 is a double six. | correct | Pascal to Fermat, 29 July 1654 (de Mere); exact powers and Monte Carlo, L1 script |
| l4 | `screens[10].hints[2].text` | $P(\text{no double six in 24 rolls}) = \left(\tfrac{35}{36}\right)^{24} \approx 0.5086$. Take... | correct | Pascal to Fermat, 29 July 1654 (de Mere); exact powers and Monte Carlo, L1 script |
| l4 | `screens[10].feedback.correct` | $1 - \left(\tfrac{35}{36}\right)^{24} \approx 0.4914$, just under one half. | correct | Pascal to Fermat, 29 July 1654 (de Mere); exact powers and Monte Carlo, L1 script |
| l4 | `screens[10].feedback.generic` | Not quite right. Use the complement: no double six in any of the 24 rolls. | correct | Pascal to Fermat, 29 July 1654 (de Mere); exact powers and Monte Carlo, L1 script |
| l4 | `screens[10].feedback.byKey.adding` | You added $\tfrac{1}{36}$ twenty-four times. That counts rolls with several double sixes more... | correct | Pascal to Fermat, 29 July 1654 (de Mere); exact powers and Monte Carlo, L1 script |
| l4 | `screens[10].feedback.byKey.none` | That is the chance of no double six. Take it from 1. | correct | Pascal to Fermat, 29 July 1654 (de Mere); exact powers and Monte Carlo, L1 script |
| l4 | `screens[10].feedback.byKey.bet-one` | That is bet 1. Bet 2 uses two dice, with $\tfrac{35}{36}$ for no double six on each roll. | correct | Pascal to Fermat, 29 July 1654 (de Mere); exact powers and Monte Carlo, L1 script |
| l4 | `screens[10].explain.text` | $1 - \left(\tfrac{35}{36}\right)^{24} \approx 0.4914$, just under one half, so bet 2 loses in... | correct | Pascal to Fermat, 29 July 1654 (de Mere); exact powers and Monte Carlo, L1 script |
| l4 | `summary.ideas` | ["An event and its complement share no outcome and cover $S$, so $P(E^c) = 1 - P(E)$.", "For ... | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `summary.formula.name` | The complement rule | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `summary.formula.tex` | P(\text{at least one}) = 1 - P(\text{none}) | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `summary.formula.note` | For $n$ rolls of a fair die: $P(\text{at least one six}) = 1 - \left(\tfrac{5}{6}\right)^n$. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `summary.trap` | Adding $\tfrac{1}{6}$ per roll counts outcomes with several sixes more than once, and passes ... | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `quiz[0].prose` | A fair coin is tossed five times. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `quiz[0].question` | What is $P(\text{at least one head})$? Give a fraction or a decimal. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `quiz[0].widget.answer` | 0.96875 | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `quiz[0].widget.accept` | Any form equal to $\tfrac{31}{32}$, or 0.9688. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `quiz[0].widget.wrong[0].value` | 0.03125 | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `quiz[0].widget.wrong[1].value` | 2.5 | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `quiz[0].feedback.correct` | $1 - \tfrac{1}{32} = \tfrac{31}{32}$. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `quiz[0].feedback.generic` | Not quite right. Only one of the 32 paths has no head. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `quiz[0].feedback.byKey.none` | That is the chance of no heads. Take it from 1. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `quiz[0].feedback.byKey.adding` | You added $\tfrac{1}{2}$ five times and passed 1. A chance cannot exceed 1. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `quiz[0].explain.text` | Five tosses give $2^5 = 32$ equally likely paths, and only TTTTT has no head. So the chance i... | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `quiz[1].prose` | A strategy triggers a margin call on any day with chance 0.03, independently of other days. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `quiz[1].question` | What is the chance of no margin call in 20 trading days? Give a decimal to 4 places. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `quiz[1].widget.answer` | 0.543794 | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `quiz[1].widget.accept` | 0.5438: $0.97^{20} = 0.54379\ldots$ | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `quiz[1].widget.wrong[0].value` | 0.4 | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `quiz[1].widget.wrong[1].value` | 0.456206 | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `quiz[1].feedback.correct` | $0.97^{20} \approx 0.5438$. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `quiz[1].feedback.generic` | Not quite right. Multiply the chance of a quiet day once for each day. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `quiz[1].feedback.byKey.adding` | You took $20 \times 0.03$ from 1. Adding the daily chances overcounts; multiply the quiet day... | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `quiz[1].feedback.byKey.at-least` | That is the chance of at least one margin call. The question asks for none. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `quiz[1].explain.text` | Each day is quiet with chance 0.97, so 20 quiet days have chance $0.97^{20} \approx 0.5438$. ... | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `quiz[2].prose` | A fair die is rolled three times. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `quiz[2].question` | Which expression equals $P(\text{at least one six})$? | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `quiz[2].widget.options[0].text` | $3 \times \dfrac{1}{6}$ | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `quiz[2].widget.options[0].why` | You added $\tfrac{1}{6}$ per roll. That counts outcomes with two or three sixes more than once. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `quiz[2].widget.options[1].text` | $\left(\dfrac{1}{6}\right)^3$ | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `quiz[2].widget.options[1].why` | That is the chance of three sixes, not at least one. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `quiz[2].widget.options[2].text` | $1 - \left(\dfrac{5}{6}\right)^3$ | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `quiz[2].widget.options[2].correct` | true | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `quiz[2].widget.options[3].text` | $1 - \left(\dfrac{1}{6}\right)^3$ | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `quiz[2].widget.options[3].why` | That is the complement of three sixes. The complement of at least one six is no six. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `quiz[2].feedback.correct` | $1 - \tfrac{125}{216} = \tfrac{91}{216} \approx 0.4213$. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `quiz[2].feedback.generic` | Not quite right. Write the complement of “no six”. | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |
| l4 | `quiz[2].explain.text` | No six in three rolls has chance $\left(\tfrac{5}{6}\right)^3 = \tfrac{125}{216}$. So $P(\tex... | correct | Ross 2.4 Prop. 4.1 (complement); 6^n outcomes counted; enumerated, L1 script |

## review-1.json

| file | JSON path | claim (short) | verdict | basis |
|---|---|---|---|---|
| review-1 | `items[0].prose` | Three trades are each filled (F) or not (N) by the close. An outcome lists the trades in orde... | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[0].question` | How many outcomes are in the sample space? | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[0].widget.answer` | 8 | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[0].widget.accept` | 8 exactly: $2^3$. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[0].widget.wrong[0].value` | 6 | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[0].widget.wrong[1].value` | 4 | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[0].widget.wrong[2].value` | 5 | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[0].feedback.correct` | $2 \times 2 \times 2 = 8$ paths. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[0].feedback.generic` | Not quite right. Each trade doubles the number of paths. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[0].feedback.byKey.multiply-wrong` | You multiplied 2 by 3. Each of the 3 trades has 2 results, so multiply 2 three times. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[0].feedback.byKey.fills` | You counted the possible numbers of fills, 0 to 3. FNN and NFN are different outcomes with on... | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[0].feedback.byKey.added` | You added the choices. Each result of one trade pairs with every result of the others. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[0].explain.text` | Each trade has 2 results and every combination is a path. So $/S/ = 2^3 = 8$, from FFF to NNN. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[1].prose` | Two dice, one red and one blue. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[1].question` | Shade every roll where the two dice differ by exactly 4. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[1].widget.answer` | ["r1c5", "r2c6", "r5c1", "r6c2"] | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[1].widget.wrong[0].set` | ["r1c5", "r2c6"] | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[1].widget.wrong[1].set` | ["r5c1", "r6c2"] | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[1].feedback.correct` | (1, 5), (5, 1), (2, 6) and (6, 2). | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[1].feedback.generic` | Not quite right. Find each pair of faces 4 apart, in both orders. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[1].feedback.byKey.one-order` | You shaded the blue-higher rolls only. (5, 1) and (6, 2) also differ by 4. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[1].feedback.byKey.one-order-b` | You shaded the red-higher rolls only. (1, 5) and (2, 6) also differ by 4. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[1].explain.text` | Faces 4 apart are 1 and 5, or 2 and 6. Each pair gives two rolls, one for each order. So the ... | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[2].prose` | Two fair dice are rolled. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[2].question` | What is $P(\text{total is } 9)$? Give a fraction or a decimal. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[2].widget.answer` | 0.111111 | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[2].widget.accept` | Any form equal to $\tfrac{4}{36} = \tfrac{1}{9}$, or 0.1111. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[2].widget.wrong[0].value` | 0.090909 | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[2].widget.wrong[1].value` | 0.055556 | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[2].feedback.correct` | (3, 6), (4, 5), (5, 4) and (6, 3): 4 of 36. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[2].feedback.generic` | Not quite right. List every roll that totals 9, keeping the dice apart. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[2].feedback.byKey.eleven` | You divided by the 11 totals. They are not equally likely; count rolls. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[2].feedback.byKey.one-order` | You counted each pair once. (3, 6) and (6, 3) are different rolls. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[2].explain.text` | Four rolls total 9: (3, 6), (4, 5), (5, 4) and (6, 3). So $P = \tfrac{4}{36} = \tfrac{1}{9}$. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[3].prose` | Three fair coins are tossed. Lee lists four outcomes, 0, 1, 2 or 3 heads, and gives each chan... | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[3].question` | What is the true chance of exactly two heads? | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[3].widget.options[0].text` | $\dfrac{1}{4}$ | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[3].widget.options[0].why` | You used Lee's list. Two heads covers three paths, HHT, HTH and THH, while 3 heads covers one. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[3].widget.options[1].text` | $\dfrac{1}{8}$ | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[3].widget.options[1].why` | You counted HHT only. The tail can also come first or second. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[3].widget.options[2].text` | $\dfrac{3}{8}$ | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[3].widget.options[2].correct` | true | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[3].widget.options[3].text` | $\dfrac{1}{2}$ | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[3].widget.options[3].why` | That is the chance of at least two heads. Exactly two excludes HHH. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[3].feedback.correct` | HHT, HTH and THH: 3 of 8 equally likely paths. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[3].feedback.generic` | Not quite right. List the 8 paths with the coins kept apart. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[3].explain.text` | Keep the coins apart: the 8 paths are equally likely. Exactly two heads covers HHT, HTH and T... | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[4].prose` | $A$ and $B$ are events in the same sample space. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[4].question` | Tap every region of $(A \cap B)^c$. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[4].widget.answer` | ["A", "B", "none"] | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[4].widget.wrong[0].set` | ["none"] | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[4].widget.wrong[1].set` | ["A", "B"] | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[4].widget.wrong[2].set` | ["AB"] | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[4].feedback.correct` | Everything except the overlap. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[4].feedback.generic` | Not quite right. $(A \cap B)^c$ is everything outside the overlap. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[4].feedback.byKey.neither` | That is $(A \cup B)^c$, neither event. Not both also includes outcomes in exactly one. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[4].feedback.byKey.xor` | You missed the outside region. Outcomes in neither event are not in both either. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[4].feedback.byKey.overlap` | That is $A \cap B$ itself. Its complement is everything else. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[4].feedback.byKey.AB` | The overlap is $A \cap B$, so it is not in the complement. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[4].explain.text` | $(A \cap B)^c$ is everything outside the overlap: $A$ only, $B$ only and the outside. By De M... | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[5].prose` | A backtest covers 120 days. A momentum signal fired on 50 days and a value signal on 40. Both... | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[5].question` | On what share of days did at least one signal fire? Give a fraction or a decimal. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[5].widget.answer` | 0.625 | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[5].widget.accept` | Any form equal to $\tfrac{75}{120} = 0.625$. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[5].widget.wrong[0].value` | 0.75 | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[5].widget.wrong[1].value` | 0.5 | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[5].widget.wrong[2].value` | 0.375 | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[5].feedback.correct` | $\tfrac{50 + 40 - 15}{120} = \tfrac{75}{120}$. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[5].feedback.generic` | Not quite right. Add the two counts and take the overlap away once. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[5].feedback.byKey.double` | You added 50 and 40. The 15 days with both were counted twice. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[5].feedback.byKey.xor` | You counted days with exactly one signal. Days with both count too. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[5].feedback.byKey.neither` | That is the share with neither signal, the complement. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[5].explain.text` | At least one signal is the union: $50 + 40 - 15 = 75$ days. So the share is $\tfrac{75}{120} ... | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[6].prose` | A fair die is rolled three times. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[6].question` | What is $P(\text{at least one six})$? Give a fraction or a decimal to 4 places. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[6].widget.answer` | 0.421296 | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[6].widget.accept` | Any form equal to $\tfrac{91}{216}$, or 0.4213. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[6].widget.wrong[0].value` | 0.5 | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[6].widget.wrong[1].value` | 0.578704 | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[6].widget.wrong[2].value` | 0.00463 | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[6].feedback.correct` | $1 - \tfrac{125}{216} = \tfrac{91}{216}$. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[6].feedback.generic` | Not quite right. Count the outcomes with no six first. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[6].feedback.byKey.adding` | You added $\tfrac{1}{6}$ three times. That counts outcomes with two or three sixes more than ... | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[6].feedback.byKey.none` | That is the chance of no six. Take it from 1. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[6].feedback.byKey.all` | That is three sixes in a row. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[6].explain.text` | No six leaves 5 faces per roll: $5^3 = 125$ of the 216 outcomes. So $P(\text{at least one six... | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[7].prose` | A portfolio holds 5 positions. Each loses money this month with chance 0.3, independently of ... | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[7].question` | What is the chance that at least one position loses? Give a decimal to 4 places. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[7].widget.answer` | 0.83193 | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[7].widget.accept` | 0.8319: $1 - 0.7^5 = 0.83193$. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[7].widget.wrong[0].value` | 1.5 | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[7].widget.wrong[1].value` | 0.16807 | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[7].widget.wrong[2].value` | 0.00243 | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[7].widget.wrong[3].value` | 0.99757 | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[7].feedback.correct` | $1 - 0.7^5 = 0.83193$. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[7].feedback.generic` | Not quite right. Find the chance that no position loses, then take it from 1. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[7].feedback.byKey.adding` | You added 0.3 five times and passed 1. A chance cannot exceed 1. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[7].feedback.byKey.none` | That is $0.7^5$, the chance no position loses. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[7].feedback.byKey.all` | That is $0.3^5$, every position losing. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[7].feedback.byKey.wrong-comp` | You took the complement of all five losing. The complement of at least one loss is no loss. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[7].explain.text` | No loss needs all five to avoid one: $0.7^5 = 0.16807$. So $P(\text{at least one loss}) = 1 -... | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[8].prose` | Two fair dice are rolled. Look at the larger of the two numbers. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[8].question` | What is $P(\text{the larger number is } 5)$? Give a fraction or a decimal. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[8].widget.answer` | 0.25 | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[8].widget.accept` | Any form equal to $\tfrac{9}{36} = \tfrac{1}{4}$. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[8].widget.wrong[0].value` | 0.277778 | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[8].widget.wrong[1].value` | 0.166667 | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[8].widget.wrong[2].value` | 0.694444 | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[8].feedback.correct` | Nine cells: row 5 and column 5 up to 5, with (5, 5) once. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[8].feedback.generic` | Not quite right. Count the cells showing 5, each once. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[8].feedback.byKey.double` | You counted (5, 5) twice: once in its row and once in its column. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[8].feedback.byKey.one-die` | That is one die showing 5. Here either die can be the larger, and the other must be 5 or less. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[8].feedback.byKey.at-most` | That is the chance the larger is at most 5. Take away the cases at most 4. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| review-1 | `items[8].explain.text` | The larger is at most 5 in $5^2 = 25$ cells, and at most 4 in $4^2 = 16$. The difference, $25... | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |

## homework-1.json

| file | JSON path | claim (short) | verdict | basis |
|---|---|---|---|---|
| homework-1 | `items[0].prose` | A share moves up £1, stays flat, or moves down £1 on each of three days. An outcome is the li... | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[0].question` | How many of the outcomes leave the share where it started? | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[0].widget.answer` | 7 | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[0].widget.accept` | 7 exactly: flat, flat, flat, plus the 6 orders of up, flat and down. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[0].widget.wrong[0].value` | 1 | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[0].widget.wrong[1].value` | 6 | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[0].widget.wrong[2].value` | 2 | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[0].feedback.correct` | Seven of the 27 outcomes. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[0].feedback.generic` | Not quite right. The moves must cancel: list every way, in every order. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[0].feedback.byKey.flat-only` | Flat three times is one way. One up, one down and one flat also cancel, in any order. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[0].feedback.byKey.no-flat` | You found the 6 orders of up, flat and down. Flat, flat, flat also ends where it started. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[0].feedback.byKey.one-order` | You counted each mix once. Up, flat, down and down, flat, up are different paths. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[0].explain.text` | The moves must sum to 0. Either all three are flat, 1 way, or there is one up, one down and o... | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[1].prose` | Two fair dice are rolled. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[1].question` | What is $P(\text{the larger number is } 4)$? Give a fraction or a decimal. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[1].widget.answer` | 0.194444 | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[1].widget.accept` | Any form equal to $\tfrac{7}{36}$, or 0.1944. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[1].widget.wrong[0].value` | 0.222222 | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[1].widget.wrong[1].value` | 0.166667 | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[1].widget.wrong[2].value` | 0.444444 | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[1].feedback.correct` | $4^2 - 3^2 = 7$ cells out of 36. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[1].feedback.generic` | Not quite right. Count rolls with both dice at most 4, then take away those with both at most 3. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[1].feedback.byKey.double` | You counted (4, 4) twice, once as each die. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[1].feedback.byKey.one-die` | That is one die showing 4. The other die must also be 4 or less. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[1].feedback.byKey.at-most` | That is the chance the larger is at most 4. Take away the 9 rolls with both dice at most 3. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[1].explain.text` | Both dice at most 4 gives $4^2 = 16$ rolls, and both at most 3 gives $3^2 = 9$. The larger is... | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[2].prose` | A bet pays £18 if two fair dice show a double, and nothing otherwise. Sam prices it with his ... | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[2].question` | What is the fair price, the average payout per roll, in pounds? | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[2].widget.answer` | 3 | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[2].widget.accept` | £3.00: $\text{£}18 \times \tfrac{6}{36}$. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[2].widget.wrong[0].value` | 5.1429 | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[2].widget.wrong[1].value` | 0.5 | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[2].widget.wrong[2].value` | 9 | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[2].feedback.correct` | Six doubles in 36 rolls: £18 × 6 / 36 = £3.00. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[2].feedback.generic` | Not quite right. Count the doubles among the 36 equally likely rolls. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[2].feedback.byKey.sam` | You used Sam's 21 pairs. A double is one roll but a mixed pair is two, so his pairs are not e... | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[2].feedback.byKey.one` | You counted one double. There are six: (1, 1) to (6, 6). | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[2].feedback.byKey.half` | You split into double or not. Only 6 of the 36 rolls are doubles. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[2].explain.text` | Six of the 36 equally likely rolls are doubles. Over 36 rolls the bet pays $6 \times \text{£}... | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[3].prose` | Three events on one trading day. $A$: the momentum signal fires. $B$: the value signal fires.... | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[3].question` | Tap every region of $(A \cup B) \cap C^c$: at least one signal fires on a calm day. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[3].widget.answer` | ["A", "B", "AB"] | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[3].widget.wrong[0].set` | ["A", "B", "AB", "AC", "BC", "ABC"] | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[3].widget.wrong[1].set` | ["A", "B"] | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[3].widget.wrong[2].set` | ["AC", "BC", "ABC"] | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[3].feedback.correct` | The parts of $A \cup B$ outside $C$. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[3].feedback.generic` | Not quite right. Shade $A \cup B$ first, then remove everything inside $C$. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[3].feedback.byKey.with-c` | You shaded all of $A \cup B$. The regions inside $C$ are high-volatility days, so remove them. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[3].feedback.byKey.xor` | You missed the region where both signals fire on a calm day. “Or” includes both. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[3].feedback.byKey.c-part` | That is $(A \cup B) \cap C$, the volatile days. We want the calm ones. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[3].explain.text` | $A \cup B$ is every region inside the $A$ or $B$ circles. Intersecting with $C^c$ keeps only ... | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[4].prose` | $A$ and $B$ are events in the same sample space. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[4].question` | Which sets equal $A^c \cup B^c$? Select all that apply. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[4].widget.options[0].text` | $(A \cap B)^c$ | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[4].widget.options[0].correct` | true | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[4].widget.options[1].text` | $(A \cap B^c) \cup (A^c \cap B) \cup (A \cup B)^c$ | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[4].widget.options[1].correct` | true | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[4].widget.options[2].text` | $A^c \cap B^c$ | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[4].widget.options[2].why` | That is neither event, only the outside region. $A^c \cup B^c$ also holds $A$ only and $B$ only. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[4].widget.options[3].text` | $(A \cup B)^c$ | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[4].widget.options[3].why` | That is neither event again. A complement turns a union into an intersection, not into a union. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[4].feedback.correct` | Both name “not both”: everything outside the overlap. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[4].feedback.generic` | Not quite right. Shade $A^c$ and $B^c$, then take every region in at least one. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[4].explain.text` | $A^c \cup B^c$ holds every outcome missing $A$ or missing $B$, so everything but the overlap.... | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[5].prose` | Each limit order you place fills with chance 0.2, independently of the others. You want at le... | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[5].question` | What is the smallest number of orders that does it? | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[5].widget.answer` | 14 | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[5].widget.accept` | 14: $1 - 0.8^{13} \approx 0.9450$ falls short, and $1 - 0.8^{14} \approx 0.9560$ clears 0.95. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[5].widget.wrong[0].value` | 5 | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[5].widget.wrong[1].value` | 13 | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[5].feedback.correct` | 14 orders: $1 - 0.8^{14} \approx 0.956$. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[5].feedback.generic` | Not quite right. Find the smallest $n$ with $0.8^n \le 0.05$. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[5].feedback.byKey.adding` | You added 0.2 per order until you passed 0.95. Five orders give only $1 - 0.8^5 \approx 0.672$. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[5].feedback.byKey.thirteen` | Close: $0.8^{13} \approx 0.0550$, so 13 orders give about 0.945. One more is needed. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[5].explain.text` | We need $1 - 0.8^n \ge 0.95$, so $0.8^n \le 0.05$. Then $n \ge \tfrac{\ln 0.05}{\ln 0.8} \app... | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[6].prose` | A desk runs three independent strategies. Each has a losing month with chance 0.25, 0.3 and 0... | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[6].question` | What is the chance at least one strategy has a losing month? Give a decimal to 3 places. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[6].widget.answer` | 0.685 | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[6].widget.accept` | 0.685: $1 - 0.75 \times 0.7 \times 0.6$. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[6].widget.wrong[0].value` | 0.95 | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[6].widget.wrong[1].value` | 0.03 | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[6].widget.wrong[2].value` | 0.315 | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[6].feedback.correct` | $1 - 0.75 \times 0.7 \times 0.6 = 1 - 0.315 = 0.685$. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[6].feedback.generic` | Not quite right. Find the chance all three avoid a loss, then take it from 1. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[6].feedback.byKey.adding` | You added the three chances. Months where two strategies lose are counted twice. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[6].feedback.byKey.all` | That is $0.25 \times 0.3 \times 0.4$, all three losing together. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[6].feedback.byKey.none` | That is the chance no strategy loses. Take it from 1. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[6].explain.text` | No losing month needs all three to avoid a loss: $0.75 \times 0.7 \times 0.6 = 0.315$. So at ... | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[7].prose` | We want $P(\text{at least one double six in } n \text{ rolls of two dice})$. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[7].question` | Put the lines of the derivation in order. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[7].widget.lines[0].text` | One roll of two dice has 36 equally likely outcomes, and 35 of them are not a double six. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[7].widget.lines[1].text` | $n$ rolls have $36^n$ equally likely outcomes, and $35^n$ of them contain no double six. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[7].widget.lines[2].text` | So $P(\text{no double six}) = \dfrac{35^n}{36^n} = \left(\dfrac{35}{36}\right)^n$. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[7].widget.lines[3].text` | At least one double six is the complement of none: $P = 1 - \left(\dfrac{35}{36}\right)^n$. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[7].widget.answer` | ["s1", "s2", "s3", "s4"] | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[7].feedback.correct` | Count one roll, count $n$ rolls, divide, then take the complement. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[7].feedback.generic` | Not quite right. Start with a single roll and build up to $n$ rolls before the complement. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[7].explain.text` | The choices multiply across rolls, giving $36^n$ outcomes and $35^n$ without a double six. Di... | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[8].prompt` | In the 1650s the Chevalier de Méré made two even-money bets. Bet 1: at least one six in 4 rol... | imprecise | finding 15: de Mere's recorded argument is a proportion, 4 is to 6 as 24 is to 36 (Pascal to Fermat, 29 July 1654); the losing-money story is legend (Ore 1960, Amer. Math. Monthly 67) |
| homework-1 | `items[8].model` | **(a)** Four rolls of a die have $6^4 = 1296$ equally likely outcomes. An outcome with no six... | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[8].rubric[0].text` | Counts $6^4 = 1296$ outcomes and $5^4 = 625$ with no six, and uses the complement. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[8].rubric[1].text` | Reaches $\tfrac{671}{1296} \approx 0.5177$ and says bet 1 wins in the long run. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[8].rubric[2].text` | Uses $P(\text{no double six}) = \left(\tfrac{35}{36}\right)^{24}$ with a reason (35 of 36 out... | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[8].rubric[3].text` | Reaches about 0.4914 and says bet 2 loses in the long run. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[8].rubric[4].text` | Explains that adding counts outcomes with several sixes more than once, with a count (864 aga... | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |
| homework-1 | `items[8].rubric[5].text` | Finds $n = 25$ and checks both 24 and 25 rolls. | correct | Ross 2.2, 2.4, 2.5; enumerated, L1 script |

## problems-1.json

| file | JSON path | claim (short) | verdict | basis |
|---|---|---|---|---|
| problems-1 | `items[0].prose` | A fair four-sided die, faces 1 to 4, and a fair six-sided die are rolled together. An outcome... | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[0].parts[0].question` | How many outcomes are in the sample space $S$? | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[0].parts[0].widget.answer` | 24 | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[0].parts[0].widget.accept` | 24 exactly: $4 \times 6$. | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[0].parts[0].widget.wrong[0].value` | 10 | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[0].parts[0].widget.wrong[1].value` | 36 | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[0].parts[0].feedback.correct` | $4 \times 6 = 24$ pairs, from $(1, 1)$ to $(4, 6)$. | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[0].parts[0].feedback.generic` | Not quite. Each face of one die pairs with every face of the other. | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[0].parts[0].feedback.byKey.added` | You added the faces. Each face of one die pairs with every face of the other, so multiply. | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[0].parts[0].feedback.byKey.two-sixes` | That is two six-sided dice. One die here has only 4 faces. | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[0].parts[0].explain.text` | Each of the 4 faces of $f$ pairs with each of the 6 faces of $s$. So $/S/ = 4 \times 6 = 24$,... | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[0].parts[1].question` | Using $/S/ = 24$, what is $P(s > f)$, the chance the six-sided die shows more? Give an exact ... | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[0].parts[1].widget.answer` | 0.583333 | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[0].parts[1].widget.accept` | Any form equal to $\tfrac{14}{24} = \tfrac{7}{12}$, or 0.5833. | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[0].parts[1].widget.wrong[0].value` | 0.75 | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[0].parts[1].widget.wrong[1].value` | 0.388889 | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[0].parts[1].widget.wrong[2].value` | 0.5 | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[0].parts[1].feedback.correct` | For $f = 1, 2, 3, 4$ the six-sided die wins on $5 + 4 + 3 + 2 = 14$ faces, so $\tfrac{14}{24}... | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[0].parts[1].feedback.generic` | Not quite. For each value of $f$, count the faces of $s$ above it. | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[0].parts[1].feedback.byKey.ties-in` | You counted the ties as wins, 18 outcomes. On a tie neither die shows more. | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[0].parts[1].feedback.byKey.thirty-six` | You divided by 36. This sample space has 24 outcomes. | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[0].parts[1].feedback.byKey.half` | You assumed each die is as likely to win. The six-sided die has higher faces, so it wins more... | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[0].parts[1].explain.text` | For each $f$, count the faces $s > f$: $5 + 4 + 3 + 2 = 14$. With 24 equally likely outcomes,... | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[0].parts[2].question` | Using $P(s > f) = \tfrac{7}{12}$, what is $P(f > s)$? A tie counts for neither die. Give a fr... | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[0].parts[2].widget.answer` | 0.25 | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[0].parts[2].widget.accept` | Any form equal to $\tfrac{6}{24} = \tfrac{1}{4}$, or 0.25. | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[0].parts[2].widget.wrong[0].value` | 0.416667 | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[0].parts[2].widget.wrong[1].value` | 0.166667 | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[0].parts[2].feedback.correct` | The three events $s > f$, a tie and $f > s$ are disjoint and cover $S$: $1 - \tfrac{14}{24} -... | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[0].parts[2].feedback.generic` | Not quite. Three disjoint events cover $S$: the six-sided die higher, a tie, and the four-sid... | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[0].parts[2].feedback.byKey.no-ties` | You took $\tfrac{7}{12}$ from 1 and left the ties in. The ties, 4 of 24, belong to neither die. | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[0].parts[2].feedback.byKey.tie` | That is the chance of a tie, $\tfrac{4}{24}$. Take it and $\tfrac{7}{12}$ from 1. | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[0].parts[2].explain.text` | The ties are $(1, 1)$ to $(4, 4)$, 4 outcomes. The three events are disjoint and cover $S$, s... | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[0].parts[3].question` | A game pays £12 unless the four-sided die shows more, so it pays on a tie too. Using $P(f > s... | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[0].parts[3].widget.answer` | 9 | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[0].parts[3].widget.accept` | £9: $12 \times \tfrac{3}{4}$. | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[0].parts[3].widget.wrong[0].value` | 7 | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[0].parts[3].widget.wrong[1].value` | 6 | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[0].parts[3].widget.wrong[2].value` | 3 | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[0].parts[3].feedback.correct` | It pays £12 unless $f > s$, which has chance $\tfrac{1}{4}$, so it pays on three quarters of ... | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[0].parts[3].feedback.generic` | Not quite. The game pays on every outcome except those where the four-sided die shows more. | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[0].parts[3].feedback.byKey.forgot-ties` | That is $12 \times \tfrac{7}{12}$, which pays only when the six-sided die wins. The game pays... | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[0].parts[3].feedback.byKey.half` | You priced it as an even chance. The game pays on three quarters of rolls. | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[0].parts[3].feedback.byKey.wrong-way` | That is $12 \times \tfrac{1}{4}$, the price of a bet on the four-sided die. This game pays on... | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[0].parts[3].explain.text` | The game pays £12 with chance $1 - \tfrac{1}{4} = \tfrac{3}{4}$ and £0 otherwise. On average ... | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[1].prose` | A fair eight-sided die, faces 1 to 8, is rolled twice. An outcome is the ordered pair $(a, b)... | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[1].parts[0].question` | How many outcomes are in $B$? | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[1].parts[0].widget.answer` | 6 | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[1].parts[0].widget.accept` | 6 exactly: $(1, 7), (7, 1), (2, 8), (8, 2), (1, 8), (8, 1)$. | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[1].parts[0].widget.wrong[0].value` | 3 | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[1].parts[0].widget.wrong[1].value` | 4 | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[1].parts[0].feedback.correct` | Differences of 6 give $(1, 7), (2, 8)$ and differences of 7 give $(1, 8)$, each in both order... | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[1].parts[0].feedback.generic` | Not quite. List the pairs that differ by 6 or by 7, in both orders. | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[1].parts[0].feedback.byKey.one-order` | You listed each pair once. $(1, 7)$ and $(7, 1)$ are different outcomes. | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[1].parts[0].feedback.byKey.exactly-six` | You counted a difference of exactly 6. A difference of 7, from 1 and 8, counts too. | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[1].parts[0].explain.text` | A difference of 6 needs $\{1, 7\}$ or $\{2, 8\}$, and a difference of 7 needs $\{1, 8\}$. Eac... | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[1].parts[1].question` | Using the 6 outcomes of $B$, how many outcomes are in $A \cap B$? | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[1].parts[1].widget.answer` | 3 | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[1].parts[1].widget.accept` | 3 exactly: $(7, 1), (8, 2), (8, 1)$. | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[1].parts[1].widget.wrong[0].value` | 0 | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[1].parts[1].widget.wrong[1].value` | 6 | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[1].parts[1].feedback.correct` | Of the 6, the ones with first roll 7 or 8 are $(7, 1), (8, 2), (8, 1)$: 3 outcomes. | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[1].parts[1].feedback.generic` | Not quite. Go through the 6 outcomes of $B$ and keep those with $a \ge 7$. | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[1].parts[1].feedback.byKey.one-order` | You kept only the orders with the smaller roll first. $(7, 1)$, $(8, 2)$ and $(8, 1)$ are in ... | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[1].parts[1].feedback.byKey.all-b` | That is all of $B$. Keep only the outcomes whose first roll is 7 or more. | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[1].parts[1].explain.text` | The intersection keeps outcomes in both events. Of $B$, only $(7, 1)$, $(8, 2)$ and $(8, 1)$ ... | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[1].parts[2].question` | Using $/B/ = 6$ and $/A \cap B/ = 3$, how many outcomes are in $A \cup B$? | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[1].parts[2].widget.answer` | 19 | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[1].parts[2].widget.accept` | 19 exactly: $16 + 6 - 3$. | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[1].parts[2].widget.wrong[0].value` | 22 | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[1].parts[2].widget.wrong[1].value` | 16 | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[1].parts[2].feedback.correct` | $A$ holds $2 \times 8 = 16$ outcomes, so $/A \cup B/ = 16 + 6 - 3 = 19$. | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[1].parts[2].feedback.generic` | Not quite. Count $A$, add $B$, then take the overlap away once. | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[1].parts[2].feedback.byKey.no-overlap` | You added $/A/ = 16$ and $/B/ = 6$. The 3 outcomes in both were counted twice. | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[1].parts[2].feedback.byKey.only-a` | That is $/A/ = 16$ alone, or the outcomes in exactly one of the two. Add the 3 outcomes of $B... | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[1].parts[2].explain.text` | $A$ has 2 choices of first roll and 8 of second, so $/A/ = 16$. Adding $/B/$ counts the overl... | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[1].parts[3].question` | Using $/A \cup B/ = 19$, what is the chance the stall pays the prize? Give an exact fraction,... | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[1].parts[3].widget.answer` | 0.296875 | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[1].parts[3].widget.accept` | Any form equal to $\tfrac{19}{64}$, or 0.2969. | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[1].parts[3].widget.wrong[0].value` | 0.34375 | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[1].parts[3].widget.wrong[1].value` | 0.527778 | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[1].parts[3].widget.wrong[2].value` | 1.1875 | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[1].parts[3].feedback.correct` | $8 \times 8 = 64$ equally likely outcomes, 19 of them pay: $\tfrac{19}{64}$. | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[1].parts[3].feedback.generic` | Not quite. Divide the paying outcomes by the size of the sample space. | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[1].parts[3].feedback.byKey.no-overlap` | That is $\tfrac{22}{64}$, with the overlap counted twice. | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[1].parts[3].feedback.byKey.unordered` | You divided by 36, the unordered pairs. The 64 ordered pairs are the equally likely outcomes. | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[1].parts[3].feedback.byKey.sixteen` | You divided by 16, the size of $A$. Divide by all 64 outcomes; a chance cannot exceed 1. | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[1].parts[3].explain.text` | The sample space holds $8 \times 8 = 64$ ordered pairs, all equally likely. So $P(A \cup B) =... | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[1].parts[4].question` | Using $P(A \cup B) = \tfrac{19}{64}$, what is the fair price of one play, the average payout ... | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[1].parts[4].widget.answer` | 4.75 | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[1].parts[4].widget.accept` | £4.75: $16 \times \tfrac{19}{64}$. | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[1].parts[4].widget.wrong[0].value` | 5.5 | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[1].parts[4].widget.wrong[1].value` | 8 | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[1].parts[4].widget.wrong[2].value` | 16 | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[1].parts[4].feedback.correct` | $16 \times \tfrac{19}{64} = \tfrac{19}{4} = £4.75$. | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[1].parts[4].feedback.generic` | Not quite. Multiply the prize by the chance it is paid. | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[1].parts[4].feedback.byKey.no-overlap` | That is $16 \times \tfrac{22}{64}$, which pays the overlap twice. | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[1].parts[4].feedback.byKey.half` | You priced it as an even chance. The prize is paid on 19 of 64 outcomes. | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[1].parts[4].feedback.byKey.per-hit` | That is the prize itself. The fair price weights it by the chance it is paid. | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[1].parts[4].explain.text` | The stall pays £16 with chance $\tfrac{19}{64}$ and nothing otherwise. The average payout is ... | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[2].prose` | A desk takes prices from a primary feed and a backup feed. On any day the primary fails with ... | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[2].parts[0].question` | What is the chance a given day is a blackout day? Give a decimal. | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[2].parts[0].widget.answer` | 0.004 | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[2].parts[0].widget.accept` | 0.004: $0.05 \times 0.08$. | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[2].parts[0].widget.wrong[0].value` | 0.13 | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[2].parts[0].widget.wrong[1].value` | 0.126 | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[2].parts[0].feedback.correct` | Independent, so $0.05 \times 0.08 = 0.004$. | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[2].parts[0].feedback.generic` | Not quite. Both feeds must fail on the same day. | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[2].parts[0].feedback.byKey.added` | You added the two chances. Both must fail, and for independent feeds the chances multiply. | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[2].parts[0].feedback.byKey.union` | That is the chance at least one feed fails. A blackout needs both. | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[2].parts[0].explain.text` | “Both fail” is the intersection of two independent events. Its chance is the product, $0.05 \... | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[2].parts[1].question` | Using $P(\text{blackout}) = 0.004$, what is the chance that at least one feed works on a give... | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[2].parts[1].widget.answer` | 0.996 | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[2].parts[1].widget.accept` | 0.996: $1 - 0.004$. | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[2].parts[1].widget.wrong[0].value` | 0.87 | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[2].parts[1].widget.wrong[1].value` | 0.874 | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[2].parts[1].widget.wrong[2].value` | 0.004 | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[2].parts[1].feedback.correct` | “At least one works” is the complement of “both fail”: $1 - 0.004 = 0.996$. | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[2].parts[1].feedback.generic` | Not quite. Which event is the opposite of a blackout? | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[2].parts[1].feedback.byKey.from-added` | That is $1 - 0.13$, which follows from adding the chances in part 1. A blackout has chance 0.... | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[2].parts[1].feedback.byKey.both-work` | That is $0.95 \times 0.92$, both feeds working. One working feed is enough. | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[2].parts[1].feedback.byKey.same` | That is the blackout chance itself. Take it from 1. | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[2].parts[1].explain.text` | By De Morgan, “not both fail” is “at least one works”. So the chance is $1 - 0.004 = 0.996$. | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[2].parts[2].question` | Using $0.996$ for a day without a blackout, what is the chance of no blackout day in 20 tradi... | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[2].parts[2].widget.answer` | 0.922968 | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[2].parts[2].widget.accept` | 0.9230: $0.996^{20} = 0.92297$. | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[2].parts[2].widget.wrong[0].value` | 0.92 | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[2].parts[2].widget.wrong[1].value` | 0.067644 | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[2].parts[2].widget.wrong[2].value` | 19.92 | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[2].parts[2].feedback.correct` | Independent days, so $0.996^{20} \approx 0.9230$. | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[2].parts[2].feedback.generic` | Not quite. Every one of the 20 independent days must be free of a blackout. | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[2].parts[2].feedback.byKey.linear` | That is $1 - 20 \times 0.004$, which adds the daily chances. Days are independent, so multipl... | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[2].parts[2].feedback.byKey.from-both-work` | That is $0.874^{20}$, every day with both feeds up. A day is safe when at least one feed works. | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[2].parts[2].feedback.byKey.twenty-times` | You multiplied by 20 instead of raising to the 20th power. A chance cannot exceed 1. | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[2].parts[2].explain.text` | Each day avoids a blackout with chance 0.996, independently. All 20 do so with chance $0.996^... | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[2].parts[3].question` | Using $0.996^{20} \approx 0.92297$, what is the chance of at least one blackout day in the 20... | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[2].parts[3].widget.answer` | 0.077032 | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[2].parts[3].widget.accept` | 0.0770: $1 - 0.996^{20} = 0.07703$. | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[2].parts[3].widget.wrong[0].value` | 0.08 | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[2].parts[3].widget.wrong[1].value` | 0.922968 | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[2].parts[3].feedback.correct` | $1 - 0.92297 = 0.07703$. | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[2].parts[3].feedback.generic` | Not quite. “At least one blackout day” is the complement of “none”. | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[2].parts[3].feedback.byKey.adding` | That is $20 \times 0.004$, which counts runs with two blackout days twice. It is close here o... | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[2].parts[3].feedback.byKey.none` | That is the chance of no blackout day. Take it from 1. | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[2].parts[3].explain.text` | “At least one” is the complement of “none”. So the chance is $1 - 0.996^{20} \approx 1 - 0.92... | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[3].prose` | Two fair four-sided dice, faces 1 to 4, one red and one blue, are rolled together; that is on... | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[3].parts[0].question` | How many equally likely outcomes does one throw have? | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[3].parts[0].widget.answer` | 16 | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[3].parts[0].widget.accept` | 16 exactly: $4 \times 4$. | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[3].parts[0].widget.wrong[0].value` | 10 | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[3].parts[0].widget.wrong[1].value` | 8 | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[3].parts[0].widget.wrong[2].value` | 7 | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[3].parts[0].feedback.correct` | $4 \times 4 = 16$ ordered pairs. | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[3].parts[0].feedback.generic` | Not quite. Pair every face of the red die with every face of the blue die. | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[3].parts[0].feedback.byKey.unordered` | You merged $(1, 2)$ and $(2, 1)$. The red and blue dice keep them apart, so there are 16. | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[3].parts[0].feedback.byKey.added` | You added the faces. Each face of the red die pairs with every face of the blue die. | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[3].parts[0].feedback.byKey.totals` | You counted the totals 2 to 8. They are not equally likely outcomes. | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[3].parts[0].explain.text` | An outcome is a pair (red, blue), and each of 4 faces pairs with each of 4. So one throw has ... | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[3].parts[1].question` | Using the 16 outcomes, what is the chance one throw totals 8? Give a fraction or a decimal. | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[3].parts[1].widget.answer` | 0.0625 | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[3].parts[1].widget.accept` | Any form equal to $\tfrac{1}{16}$, or 0.0625. | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[3].parts[1].widget.wrong[0].value` | 0.142857 | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[3].parts[1].widget.wrong[1].value` | 0.1 | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[3].parts[1].feedback.correct` | Only $(4, 4)$ totals 8: $\tfrac{1}{16}$. | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[3].parts[1].feedback.generic` | Not quite. List the outcomes that total 8. | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[3].parts[1].feedback.byKey.totals` | You gave each of the 7 totals the same chance. Only $(4, 4)$ totals 8, one outcome of 16. | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[3].parts[1].feedback.byKey.unordered` | That is 1 of 10, from the merged pairs. The 16 ordered pairs are the equally likely ones. | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[3].parts[1].explain.text` | A total of 8 needs 4 on both dice, a single outcome. So the chance is $\tfrac{1}{16} = 0.0625$. | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[3].parts[2].question` | Using $\tfrac{1}{16}$ for one throw, what is the chance that no throw totals 8 in a run of 10... | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[3].parts[2].widget.answer` | 0.52446 | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[3].parts[2].widget.accept` | 0.5245: $\left(\tfrac{15}{16}\right)^{10} = 0.52446$. | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[3].parts[2].widget.wrong[0].value` | 0.375 | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[3].parts[2].widget.wrong[1].value` | 0.348678 | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[3].parts[2].widget.wrong[2].value` | 0.214058 | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[3].parts[2].feedback.correct` | Each throw misses with chance $\tfrac{15}{16}$, so ten misses have chance $\left(\tfrac{15}{1... | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[3].parts[2].feedback.generic` | Not quite. Each of the 10 independent throws must miss. | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[3].parts[2].feedback.byKey.linear` | That is $1 - \tfrac{10}{16}$, which adds the chances. Multiply $\tfrac{15}{16}$ ten times. | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[3].parts[2].feedback.byKey.from-unordered` | That is $0.9^{10}$, from the chance $\tfrac{1}{10}$. One throw totals 8 with chance $\tfrac{1... | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[3].parts[2].feedback.byKey.from-totals` | That is $\left(\tfrac{6}{7}\right)^{10}$, from treating the 7 totals as equally likely. | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[3].parts[2].explain.text` | One throw misses 8 with chance $1 - \tfrac{1}{16} = \tfrac{15}{16}$. The throws are independe... | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[3].parts[3].question` | Using $\left(\tfrac{15}{16}\right)^{10} \approx 0.52446$, what is the chance the bet wins wit... | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[3].parts[3].widget.answer` | 0.47554 | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[3].parts[3].widget.accept` | 0.4755: $1 - 0.52446 = 0.47554$. | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[3].parts[3].widget.wrong[0].value` | 0.625 | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[3].parts[3].widget.wrong[1].value` | 0.52446 | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[3].parts[3].feedback.correct` | $1 - 0.52446 = 0.47554$: just under an even chance. | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[3].parts[3].feedback.generic` | Not quite. Winning is the complement of “no throw totals 8”. | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[3].parts[3].feedback.byKey.adding` | That is $\tfrac{10}{16}$, which adds $\tfrac{1}{16}$ per throw. Runs with two 8s are counted ... | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[3].parts[3].feedback.byKey.none` | That is the chance no throw totals 8. Take it from 1. | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[3].parts[3].explain.text` | The bet wins unless every throw misses. So $P(\text{win}) = 1 - 0.52446 = 0.4755$, a little u... | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[3].parts[4].question` | Each throw misses with chance $\tfrac{15}{16}$, so $n$ throws all miss with chance $\left(\tf... | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[3].parts[4].widget.answer` | 36 | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[3].parts[4].widget.accept` | 36 exactly: $1 - \left(\tfrac{15}{16}\right)^{36} \approx 0.9021$, while $n = 35$ gives 0.8955. | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[3].parts[4].widget.wrong[0].value` | 15 | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[3].parts[4].widget.wrong[1].value` | 11 | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[3].parts[4].widget.wrong[2].value` | 35 | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[3].parts[4].feedback.correct` | At 36 throws, $1 - \left(\tfrac{15}{16}\right)^{36} \approx 0.9021$. At 35 it is 0.8955, so 3... | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[3].parts[4].feedback.generic` | Not quite. Find the smallest $n$ with $\left(\tfrac{15}{16}\right)^n < 0.1$, by trying values. | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[3].parts[4].feedback.byKey.adding` | That solves $\tfrac{n}{16} > 0.9$, which adds the chances. At $n = 15$ the bet wins with chan... | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[3].parts[4].feedback.byKey.half` | That is the $n$ for a win more often than not. At $n = 11$ the chance is 0.5083, well short o... | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[3].parts[4].feedback.byKey.one-short` | At $n = 35$ the chance is 0.8955, just under 0.9. | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |
| problems-1 | `items[3].parts[4].explain.text` | The bet wins with chance above 0.9 when $\left(\tfrac{15}{16}\right)^n < 0.1$. Trying values,... | correct | Ross 2.4, 2.5, 3.4; enumerated, L1 script and Monte Carlo of the feed model |

## l5-in-stages.json

| file | JSON path | claim (short) | verdict | basis |
|---|---|---|---|---|
| l5 | `screens[0].prose` | A set lunch is one starter followed by one main. The kitchen offers 3 starters and 4 mains. E... | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[0].canvas.state.caption` | One path from the left to the right is one meal | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[0].question` | Tap every complete meal, one leaf at a time, to count them. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[0].widget.answer` | ["s-f", "s-b", "s-r", "s-c", "l-f", "l-b", "l-r", "l-c", "p-f", "p-b", "p-r", "p-c"] | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[0].widget.wrong[0].set` | ["s", "l", "p"] | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[0].hints[0].text` | A meal ends at a main on the far right. How many mains hang off Soup? | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[0].hints[1].text` | Soup alone leads to 4 meals. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[0].hints[2].text` | Each of the 3 starters leads to the same 4 mains. Tap all 12 leaves. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[0].feedback.correct` | Twelve meals: every starter goes with every main. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[0].feedback.generic` | Not quite right. Tap each leaf on the far right once, under every starter. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[0].feedback.byKey.starters` | You tapped the 3 starters. A meal is a whole path, so tap the mains at the far right. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[0].feedback.byKey.s` | You tapped the Soup branch itself. Tap the mains to its right instead: each is one meal. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[0].feedback.byKey.l` | You tapped the Salad branch itself. Tap the mains to its right instead: each is one meal. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[0].feedback.byKey.p` | You tapped the Pâté branch itself. Tap the mains to its right instead: each is one meal. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[0].explain.text` | You tapped 3 groups of 4 leaves, one group per starter. That is $3 \times 4 = 12$ meals. Seve... | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[1].prose` | The same menu as a table: each row is a starter, each column a main, and each cell one meal. ... | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[1].canvas.state.caption` | 3 starters × 4 mains = 12 meals | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[1].question` | Start at 3 starters and 4 mains. Add one starter. How many new meals appear? | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[1].widget.options[0].text` | 1 new meal | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[1].widget.options[0].why` | You added one dish. But the new starter pairs with every main, so it brings a whole row. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[1].widget.options[1].text` | 4 new meals | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[1].widget.options[1].correct` | true | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[1].widget.options[2].text` | 3 new meals | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[1].widget.options[2].why` | You counted the starters. The new row holds one meal per main, and there are 4 mains. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[1].widget.options[3].text` | 12 new meals | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[1].widget.options[3].why` | That doubles the menu. One more starter adds one row, not a copy of the table. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[1].hints[0].text` | Set Starters to 4 and watch the table. What appears? | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[1].feedback.correct` | The new starter brings a full row of 4 meals. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[1].feedback.generic` | Not quite right. Move Starters from 3 to 4 and count the cells in the new row. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[1].feedback.byKey.one` | You added one dish. But the new starter pairs with every main, so it brings a whole row. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[1].feedback.byKey.twelve` | That doubles the menu. One more starter adds one row, not a copy of the table. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[1].explain.text` | The fourth starter adds a row, and the row has one cell per main. So the count goes from $3 \... | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[1].explain.canvas.caption` | 4 starters × 4 mains = 16 meals | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[2].prose` | Multiplying the choices at each stage is the **multiplication rule**. It works whenever every... | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[2].canvas.state.caption` | Only the Soup branch is drawn in full | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[2].question` | How many three-course meals are there? | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[2].widget.answer` | 24 | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[2].widget.accept` | 24 exactly: $3 \times 4 \times 2$. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[2].widget.wrong[0].value` | 9 | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[2].widget.wrong[1].value` | 14 | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[2].widget.wrong[2].value` | 8 | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[2].hints[0].text` | Count the leaves under Soup first. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[2].hints[1].text` | Soup leads to 4 mains, and each main splits into 2 desserts. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[2].hints[2].text` | Soup gives $4 \times 2 = 8$ meals. Salad and Pâté give 8 each as well. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[2].feedback.correct` | Three stages: $3 \times 4 \times 2 = 24$. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[2].feedback.generic` | Not quite right. Count the meals under Soup, then remember the other two starters. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[2].feedback.byKey.added` | You added the dishes, $3 + 4 + 2$. Each meal is a path, and the paths multiply. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[2].feedback.byKey.plus-two` | You added 2 desserts to 12 meals. Each old meal splits into 2, so the count doubles. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[2].feedback.byKey.soup` | That is the Soup branch only. Salad and Pâté lead to 8 meals each as well. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[2].explain.text` | Under Soup there are $4 \times 2 = 8$ meals, and each starter has the same 8. So the rule giv... | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[2].explain.canvas.caption` | Each starter leads to 8 meals | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[3].prose` | Five horses, A to E, run a race. A forecast names the 1st, 2nd and 3rd horse in order. A hors... | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[3].canvas.state.caption` | Only A first, then A–B, is drawn in full | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[3].question` | How many different forecasts are possible? | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[3].widget.answer` | 60 | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[3].widget.accept` | 60 exactly: $5 \times 4 \times 3$. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[3].widget.wrong[0].value` | 125 | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[3].widget.wrong[1].value` | 12 | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[3].widget.wrong[2].value` | 10 | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[3].hints[0].text` | How many horses could finish 1st? Once that is fixed, how many could finish 2nd? | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[3].hints[1].text` | After A wins, only 4 horses are left for 2nd. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[3].hints[2].text` | 5 choices for 1st, then 4 for 2nd, then 3 for 3rd. Multiply. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[3].feedback.correct` | $5 \times 4 \times 3 = 60$ forecasts. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[3].feedback.generic` | Not quite right. Each place has one fewer horse to choose from than the place before. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[3].feedback.byKey.repeats` | You let a horse fill two places, $5 \times 5 \times 5$. Once a horse is placed, it is gone. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[3].feedback.byKey.added` | You added $5 + 4 + 3$. Each choice for 1st carries all of the later choices, so multiply. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[3].feedback.byKey.unordered` | You counted groups of 3 horses. A forecast also says who came 1st, 2nd and 3rd. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[3].explain.text` | The tree shows 5 branches, then 4 under A, then 3 under A–B. The second stage depends on the ... | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[4].prose` | Now the forecast names all five places, 1st to 5th. The tree draws one branch in full at each... | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[4].canvas.state.caption` | One branch per stage drawn in full | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[4].question` | In how many orders can the five horses finish? | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[4].widget.answer` | 120 | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[4].widget.accept` | 120 exactly: $5 \times 4 \times 3 \times 2 \times 1$. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[4].widget.wrong[0].value` | 15 | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[4].widget.wrong[1].value` | 3125 | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[4].widget.wrong[2].value` | 60 | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[4].hints[0].text` | Count the branches at each stage of the drawn path. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[4].hints[1].text` | The stages offer 5, 4, 3, 2 and then 1 choice. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[4].hints[2].text` | Multiply $5 \times 4 \times 3 \times 2 \times 1$. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[4].feedback.correct` | $5 \times 4 \times 3 \times 2 \times 1 = 120$. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[4].feedback.generic` | Not quite right. Multiply the number of choices at each of the five stages. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[4].feedback.byKey.added` | You added $5 + 4 + 3 + 2 + 1$. The stages multiply, as before. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[4].feedback.byKey.repeats` | You let a horse finish in more than one place. Each stage has one fewer horse. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[4].feedback.byKey.three` | That stops after 3rd place. The last two places still give $2 \times 1$ orders. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[4].explain.text` | The drawn path offers 5, 4, 3, 2 and 1 choices. A product that runs down to 1 is a **factoria... | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[5].prose` | Back to the lunch menu. Late in the day the ice cream runs out. Every meal still has three co... | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[5].canvas.state.caption` | Only the Soup branch is drawn in full | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[5].question` | How many three-course meals are there now? | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[5].widget.answer` | 12 | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[5].widget.accept` | 12 exactly: $3 \times 4 \times 1$. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[5].widget.wrong[0].value` | 8 | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[5].widget.wrong[1].value` | 13 | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[5].widget.wrong[2].value` | 24 | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[5].widget.wrong[3].value` | 0 | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[5].hints[0].text` | Does a dessert with only one choice split any path? | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[5].hints[1].text` | Each main now leads to exactly one dessert. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[5].hints[2].text` | Multiply $3 \times 4 \times 1$. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[5].feedback.correct` | A stage with one choice multiplies by 1. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[5].feedback.generic` | Not quite right. Each meal from the two-course menu now gets one dessert, the tart. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[5].feedback.byKey.added` | You added $3 + 4 + 1$. The stages still multiply. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[5].feedback.byKey.plus-one` | You added 1 for the tart. A forced choice extends each meal; it does not add a new one. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[5].feedback.byKey.old` | That still counts the ice cream. Only one dessert is left. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[5].feedback.byKey.none` | A stage with one choice still lets every meal through. Only a stage with no choices gives 0. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[5].explain.text` | Each of the 12 two-course meals gains the same tart, so no path splits. That is $3 \times 4 \... | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[5].explain.canvas.caption` | 12 meals, each ending in the tart | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[6].prose` | You roll a fair die and toss a fair coin. Sam says there are 6 faces and 2 sides, so 8 outcom... | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[6].canvas.state.caption` | Every path is equally likely | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[6].question` | What is the chance of a 6 and heads? | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[6].widget.options[0].text` | $\dfrac{1}{8}$ | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[6].widget.options[0].why` | You added 6 faces and 2 sides. Each face splits into 2 paths, so there are 12 outcomes. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[6].widget.options[1].text` | $\dfrac{1}{12}$ | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[6].widget.options[1].correct` | true | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[6].widget.options[2].text` | $\dfrac{2}{3}$ | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[6].widget.options[2].why` | You added $\tfrac{1}{6}$ and $\tfrac{1}{2}$. Both must happen, which is one path of 12. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[6].widget.options[3].text` | $\dfrac{1}{6}$ | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[6].widget.options[3].why` | That is the chance of a 6 alone. The coin then splits the 6 into two paths. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[6].hints[0].text` | Count the leaves at the bottom of the tree. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[6].hints[1].text` | The 6 branch splits into heads and tails. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[6].hints[2].text` | There are $6 \times 2 = 12$ equally likely paths. One of them is 6 then heads. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[6].feedback.correct` | One path of the 12. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[6].feedback.generic` | Not quite right. Count every path, then count the paths that give a 6 and heads. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[6].feedback.byKey.added` | You added 6 faces and 2 sides. Each face splits into 2 paths, so there are 12 outcomes. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[6].feedback.byKey.sum` | You added the two chances. Both must happen, which is one path of 12. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[6].explain.text` | Sam counted 8 things, not 8 outcomes: an outcome is a whole path, a face and a side. Six face... | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[6].explain.canvas.caption` | 12 paths; 6 then heads is one | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[7].prose` | Each time, you multiplied the choices at every stage. If stage $i$ has $n_i$ choices, whateve... | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[7].question` | A desk names a lead trader and a different backup from 7 people. How many ways? | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[7].widget.options[0].text` | $7 \times 7 = 49$ | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[7].widget.options[0].why` | You let the same person be lead and backup. The backup must be one of the other 6. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[7].widget.options[1].text` | $7 \times 6 = 42$ | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[7].widget.options[1].correct` | true | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[7].widget.options[2].text` | $7 + 6 = 13$ | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[7].widget.options[2].why` | You added the stage counts. Each lead goes with each of 6 backups, so multiply. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[7].widget.options[3].text` | $\dfrac{7 \times 6}{2} = 21$ | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[7].widget.options[3].why` | You treated lead and backup as the same job. Swapping them gives a different choice. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[7].feedback.correct` | Two stages, with 7 and then 6 choices: $\tfrac{7!}{5!} = 42$. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[7].feedback.generic` | Not quite right. Count the choices for lead, then for backup, then multiply. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[7].explain.text` | Lead has 7 choices and backup has the 6 people left. The rule multiplies them: $7 \times 6 = ... | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[8].prose` | Forecasts of 3 places from $n$ horses gave $\tfrac{n!}{(n-3)!}$. Write $n!$ as its top three ... | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[8].question` | Cancel the $(n-3)!$. What is left? | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[8].widget.answer` | n(n-1)(n-2) | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[8].widget.accept` | ["n(n-1)(n-2)", "n*(n-1)*(n-2)", "n^3-3n^2+2n"] | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[8].widget.wrong[0].tex` | n^3 | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[8].widget.wrong[1].tex` | 3n-3 | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[8].widget.wrong[2].tex` | \frac{n(n-1)(n-2)}{6} | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[8].hints[0].text` | The same factor sits on the top and the bottom. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[8].hints[1].text` | Dividing $(n-3)!$ by itself leaves 1. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[8].hints[2].text` | What remains is the three factors $n$, $n-1$ and $n-2$, multiplied. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[8].feedback.correct` | Three stages: $n$, then $n-1$, then $n-2$. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[8].feedback.generic` | Not quite right. Cancel the $(n-3)!$ on the top with the one on the bottom. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[8].feedback.byKey.repeats` | You wrote $n^3$, which lets a horse fill two places. Each stage has one fewer. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[8].feedback.byKey.added` | You added the three factors. The stages multiply. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[8].feedback.byKey.unordered` | You divided by the $3! = 6$ orders. A forecast keeps the order, so do not. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[8].explain.text` | Cancelling leaves $n(n-1)(n-2)$, the three stages you multiplied for the race. With $n = 5$ i... | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[9].prose` | An execution test sends a sequence of 4 trades, one leg after another. Each leg uses one of 6... | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[9].question` | How many different 4-leg sequences can the test send? | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[9].widget.answer` | 360 | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[9].widget.accept` | 360 exactly: $6 \times 5 \times 4 \times 3 = \tfrac{6!}{2!}$. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[9].widget.wrong[0].value` | 1296 | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[9].widget.wrong[1].value` | 15 | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[9].widget.wrong[2].value` | 18 | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[9].widget.wrong[3].value` | 24 | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[9].hints[0].text` | How many instruments could the first leg use? And the second? | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[9].hints[1].text` | Each leg removes one instrument from the pool. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[9].hints[2].text` | The legs offer 6, 5, 4 and 3 choices. Multiply them. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[9].feedback.correct` | $6 \times 5 \times 4 \times 3 = 360$ sequences. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[9].feedback.generic` | Not quite right. Count the choices for each leg in turn, one fewer each time, and multiply. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[9].feedback.byKey.repeats` | You let an instrument appear twice, $6^4$. Each leg has one fewer to choose from. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[9].feedback.byKey.unordered` | You counted sets of 4 instruments. The legs are in order, so each set gives 24 sequences. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[9].feedback.byKey.added` | You added $6 + 5 + 4 + 3$. Each first leg carries all of the later choices, so multiply. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[9].feedback.byKey.orders` | You counted the orders of one set of 4 instruments. There are also 15 sets to choose from. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[9].explain.text` | Leg 1 has 6 instruments, leg 2 has 5 left, then 4, then 3. So there are $6 \times 5 \times 4 ... | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `screens[9].explain.canvas.caption` | One of the 360: Gold, FTSE, Bund, GBP | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `summary.ideas` | ["When every choice at one stage leaves the same number at the next, multiply the stage count... | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `summary.formula.name` | Multiplication rule | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `summary.formula.tex` | N = n_1 \times n_2 \times \cdots \times n_k | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `summary.formula.note` | Each $n_i$ counts the choices at stage $i$, whatever happened before. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `summary.trap` | Adding the stage counts (3 + 4 = 7) counts dishes, not meals. An outcome is a whole path. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `quiz[0].prose` | A login code is either 4 lower-case letters (26 choices each) or 8 digits (10 choices each). ... | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `quiz[0].question` | Which kind of code has more possibilities? | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `quiz[0].widget.options[0].text` | 8 digits: $10^8 = 100{,}000{,}000$, against $26^4 = 456{,}976$ | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `quiz[0].widget.options[0].correct` | true | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `quiz[0].widget.options[1].text` | 4 letters, because 26 choices beat 10 | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `quiz[0].widget.options[1].why` | You compared the alphabets. Each extra character multiplies the count, and 8 characters beat 4. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `quiz[0].widget.options[2].text` | 4 letters: $4 \times 26 = 104$ beats $8 \times 10 = 80$ | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `quiz[0].widget.options[2].why` | You multiplied length by alphabet size. Each character is a stage, so raise the alphabet size... | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `quiz[0].feedback.correct` | Length multiplies again with every character. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `quiz[0].feedback.generic` | Not quite right. Each character is a stage: multiply its choices once per character. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `quiz[0].explain.text` | Four letters give $26 \times 26 \times 26 \times 26 = 456{,}976$ codes. Eight digits give $10... | imprecise | finding 10: not a general rule: 10^5 = 100,000 is below 26^4 = 456,976 (L2 script) |
| l5 | `quiz[1].prose` | Four stocks can be ranked in $4! = 24$ orders. The formula $\tfrac{n!}{(n-k)!}$ with $n = k =... | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `quiz[1].question` | What value must $0!$ take for the formula to give 24? | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `quiz[1].widget.answer` | 1 | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `quiz[1].widget.accept` | 1 exactly. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `quiz[1].widget.wrong[0].value` | 0 | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `quiz[1].feedback.correct` | $0! = 1$, so $\tfrac{4!}{0!} = 24$. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `quiz[1].feedback.generic` | Not quite right. Solve $\tfrac{24}{0!} = 24$. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `quiz[1].feedback.byKey.zero` | With $0! = 0$ the formula would divide by zero. It must be the value that leaves 24 unchanged. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `quiz[1].explain.text` | We need $\tfrac{24}{0!} = 24$, so $0! = 1$. That is a choice made so the formula works when e... | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `quiz[2].prose` | An analyst ranks her top 3 picks, in order, from a watchlist of 8 stocks. No stock appears tw... | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `quiz[2].question` | How many different rankings are possible? | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `quiz[2].widget.answer` | 336 | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `quiz[2].widget.accept` | 336 exactly: $8 \times 7 \times 6$. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `quiz[2].widget.wrong[0].value` | 512 | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `quiz[2].widget.wrong[1].value` | 56 | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `quiz[2].widget.wrong[2].value` | 21 | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `quiz[2].feedback.correct` | $8 \times 7 \times 6 = 336$. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `quiz[2].feedback.generic` | Not quite right. Count the choices for 1st, 2nd and 3rd, one fewer each time. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `quiz[2].feedback.byKey.repeats` | You let a stock take two places, $8^3$. Each place has one fewer stock. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `quiz[2].feedback.byKey.unordered` | You counted sets of 3 stocks. A ranking also orders them, 6 ways per set. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `quiz[2].feedback.byKey.added` | You added $8 + 7 + 6$. The stages multiply. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `quiz[2].explain.text` | First place has 8 choices, second has 7, third has 6. The rule multiplies them: $8 \times 7 \... | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `quiz[3].prose` | You toss a fair coin and roll two fair dice. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `quiz[3].question` | What is the chance of heads and a double six? Give a fraction. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `quiz[3].widget.answer` | 0.013888888888888888 | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `quiz[3].widget.accept` | any form equal to $\tfrac{1}{72}$. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `quiz[3].widget.wrong[0].value` | 0.07142857142857142 | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `quiz[3].widget.wrong[1].value` | 0.027777777777777776 | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `quiz[3].widget.wrong[2].value` | 0.08333333333333333 | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `quiz[3].feedback.correct` | One outcome of $2 \times 6 \times 6 = 72$. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `quiz[3].feedback.generic` | Not quite right. Count every outcome of the three stages, then the ones you want. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `quiz[3].feedback.byKey.added` | You added $2 + 6 + 6 = 14$. The three stages multiply to 72 outcomes. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `quiz[3].feedback.byKey.no-coin` | That is a double six alone. The coin splits each roll into two outcomes. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `quiz[3].feedback.byKey.one-die` | That uses only one die. Both dice must show a six. | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |
| l5 | `quiz[3].explain.text` | The coin, the first die and the second die are three stages: $2 \times 6 \times 6 = 72$ equal... | correct | Ross 1.2 (basic principle of counting), 1.3 (permutations); itertools enumerated, L2 script |

## l6-does-order-matter.json

| file | JSON path | claim (short) | verdict | basis |
|---|---|---|---|---|
| l6 | `screens[0].prose` | You can hold two of four stocks, A, B, C and D, in equal amounts. Holding A and B is the same... | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[0].question` | How many different pairs of stocks could you hold? | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[0].widget.answer` | 6 | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[0].widget.accept` | 6 exactly. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[0].widget.wrong[0].value` | 12 | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[0].widget.wrong[1].value` | 16 | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[0].widget.wrong[2].value` | 4 | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[0].widget.wrong[3].value` | 8 | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[0].hints[0].text` | List the pairs that include A. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[0].hints[1].text` | A can go with B, C or D. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[0].hints[2].text` | A gives 3 pairs. B gives 2 new ones, with C or D. Then C with D. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[0].feedback.correct` | Six pairs: AB, AC, AD, BC, BD and CD. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[0].feedback.generic` | Not quite right. List the pairs, and count A with B only once. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[0].feedback.byKey.ordered` | You counted A then B and B then A as different. They are the same holding. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[0].feedback.byKey.square` | You paired a stock with itself. A pair needs two different stocks. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[0].feedback.byKey.four` | You counted the stocks. Each pair is two of them together. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[0].feedback.byKey.added` | You added 4 and 4. Count the pairs themselves: AB, AC and so on. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[0].explain.text` | A pairs with 3 others, B with 2 new ones, and C with 1 more: $3 + 2 + 1 = 6$. The pair AB is ... | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[0].explain.canvas.caption` | AB, AC, AD, BC, BD, CD | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[1].prose` | Now pick one stock first and then a second. Each cell is an ordered pick: row B, column A mea... | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[1].question` | Tap every cell that ends with you holding A and B. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[1].widget.answer` | ["r1c2", "r2c1"] | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[1].hints[0].text` | A and B can be picked in two orders. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[1].hints[1].text` | Look in row A and in row B. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[1].feedback.correct` | AB and BA both leave you holding A and B. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[1].feedback.generic` | Not quite right. Find A then B, and B then A. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[1].feedback.byKey.r2c1` | You found B then A. A then B, in row A, gives the same holding. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[1].feedback.byKey.r1c2` | You found A then B. B then A, in row B, gives the same holding. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[1].explain.text` | The 12 cells off the diagonal are the ordered picks, $4 \times 3$. Every pair fills two of th... | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[1].explain.canvas.caption` | Each pair once above the diagonal, and again below it | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[2].prose` | A choice where order does not matter is a **combination**. We write $\binom{4}{2}$, read 4 ch... | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[2].canvas.state.caption` | 24 ordered picks, sorted by holding | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[2].question` | What is $\binom{4}{3}$, the number of different holdings of 3 stocks? | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[2].widget.answer` | 4 | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[2].widget.accept` | 4 exactly: $24 \div 6$. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[2].widget.wrong[0].value` | 24 | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[2].widget.wrong[1].value` | 12 | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[2].widget.wrong[2].value` | 8 | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[2].widget.wrong[3].value` | 2 | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[2].hints[0].text` | How many ordered picks does one holding have? | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[2].hints[1].text` | The holding A, B, C has 6 ordered picks. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[2].hints[2].text` | Each holding appears 6 times among the 24 picks. Divide 24 by 6. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[2].feedback.correct` | $24 \div 6 = 4$ holdings. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[2].feedback.generic` | Not quite right. Count how often one holding appears among the 24 ordered picks, then divide. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[2].feedback.byKey.ordered` | You counted the ordered picks. Each holding appears 6 times among them. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[2].feedback.byKey.halved` | You divided by 2, as for pairs. Three stocks can be ordered in $3! = 6$ ways. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[2].feedback.byKey.thirds` | You divided by 3. Three stocks have $3 \times 2 \times 1 = 6$ orders. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[2].feedback.byKey.rows-shown` | Those are the rows drawn so far. The table stops early: work out how many rows it needs. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[2].explain.text` | Each holding of 3 can be picked in $3! = 6$ orders. So the 24 ordered picks hold each holding... | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[3].prose` | Each time, you divided the ordered picks by the orders of one group. The table collects your ... | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[3].canvas.state.caption` | Groups = ordered picks ÷ orders of one group | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[3].question` | What is $\binom{5}{3}$? | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[3].widget.answer` | 10 | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[3].widget.accept` | 10 exactly: $\tfrac{5 \times 4 \times 3}{3!} = \tfrac{60}{6}$. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[3].widget.wrong[0].value` | 60 | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[3].widget.wrong[1].value` | 30 | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[3].widget.wrong[2].value` | 20 | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[3].hints[0].text` | How many ordered picks of 3 from 5 are there? | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[3].hints[1].text` | The last row already gives 60 ordered picks. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[3].hints[2].text` | Each holding of 3 has 6 orders. Divide 60 by 6. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[3].feedback.correct` | $60 \div 6 = 10$. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[3].feedback.generic` | Not quite right. Divide the ordered picks by the orders of one group of 3. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[3].feedback.byKey.ordered` | You counted ordered picks. A holding ignores order, so divide by its 6 orders. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[3].feedback.byKey.halved` | You divided by 2. A group of 3 has $3! = 6$ orders. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[3].feedback.byKey.thirds` | You divided by 3. A group of 3 has $3 \times 2 \times 1 = 6$ orders. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[3].explain.text` | There are $5 \times 4 \times 3 = 60$ ordered picks, and each holding appears $3! = 6$ times. ... | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[3].explain.canvas.caption` | $\binom{5}{3} = 60 \div 6 = 10$ | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[4].prose` | Here are the counts $\binom{5}{0}$ to $\binom{5}{5}$, and below them $\binom{6}{0}$ to $\bino... | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[4].canvas.state.caption` | Row $n$ lists $\binom{n}{0}, \binom{n}{1}, \dots, \binom{n}{n}$ | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[4].question` | What is $\binom{6}{2}$, the missing entry? | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[4].widget.answer` | 15 | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[4].widget.accept` | 15 exactly: $5 + 10$. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[4].widget.wrong[0].value` | 20 | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[4].widget.wrong[1].value` | 10 | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[4].widget.wrong[2].value` | 30 | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[4].widget.wrong[3].value` | 50 | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[4].hints[0].text` | Which two entries sit just above the gap? | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[4].hints[1].text` | The gap sits under 5 and 10. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[4].hints[2].text` | Add them: $\binom{6}{2} = \binom{5}{1} + \binom{5}{2}$. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[4].feedback.correct` | $5 + 10 = 15$. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[4].feedback.generic` | Not quite right. Add the two entries just above the gap. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[4].feedback.byKey.middle` | That is $\binom{6}{3}$, the middle entry. The gap is one place to its left. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[4].feedback.byKey.copied` | You copied the entry above. Each lower entry adds the two above it. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[4].feedback.byKey.ordered` | That is $6 \times 5$, the ordered picks. Halve it, or add the two entries above. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[4].feedback.byKey.multiplied` | You multiplied 5 by 10. The rule adds the two entries above. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[4].explain.text` | Pairs from 6 stocks either include stock F or not. With F, pick 1 more from 5: $\binom{5}{1} ... | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[5].prose` | Each row reads the same from both ends: $\binom{6}{2} = \binom{6}{4} = 15$. Choosing 2 stocks... | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[5].question` | How many ways can you choose all 6 stocks? And how many ways to choose none? | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[5].widget.options[0].text` | 6 ways, and 0 ways | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[5].widget.options[0].why` | You counted one way per stock. Taking all 6 is one holding; taking none is one empty holding. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[5].widget.options[1].text` | 1 way, and 1 way | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[5].widget.options[1].correct` | true | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[5].widget.options[2].text` | 720 ways, and 1 way | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[5].widget.options[2].why` | 720 is $6!$, the orders of all six. A holding ignores order, so all six is one holding. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[5].widget.options[3].text` | 1 way, and 0 ways | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[5].widget.options[3].why` | Choosing nothing is still a choice: the empty holding. There is exactly one. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[5].hints[0].text` | Look at the first and last entries of each row. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[5].hints[1].text` | Every row starts and ends with 1. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[5].hints[2].text` | Taking everything leaves no choice. Taking nothing also leaves no choice: one way each. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[5].feedback.correct` | $\binom{6}{6} = \binom{6}{0} = 1$. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[5].feedback.generic` | Not quite right. Read the ends of the lower row. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[5].feedback.byKey.six-zero` | You counted one way per stock. Taking all 6 is one holding; taking none is one empty holding. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[5].feedback.byKey.none-impossible` | Choosing nothing is still a choice: the empty holding. There is exactly one. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[5].explain.text` | Holding all six stocks is a single holding, and holding none is the single empty holding. The... | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[6].prose` | From 8 analysts, a fund makes two choices. A risk committee of 3 has equal votes. A podium aw... | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[6].question` | Which pair of counts is right? | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[6].widget.options[0].text` | Committee 336, podium 336 | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[6].widget.options[0].why` | That is Kim's answer. The podium is ordered, so 336 fits it. A committee ignores order, so it... | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[6].widget.options[1].text` | Committee 336, podium 56 | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[6].widget.options[1].why` | You swapped the two methods. The committee ignores order and the podium does not. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[6].widget.options[2].text` | Committee 56, podium 336 | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[6].widget.options[2].correct` | true | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[6].widget.options[3].text` | Committee 56, podium 56 | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[6].widget.options[3].why` | The committee is right. But swapping gold and silver changes the podium, so order counts there. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[6].hints[0].text` | Does swapping two people change the committee? Does it change the podium? | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[6].hints[1].text` | Gold to Ana and silver to Ben differs from the swap. A committee of Ana and Ben does not. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[6].hints[2].text` | Ordered picks: $8 \times 7 \times 6 = 336$. The committee divides by $3! = 6$. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[6].feedback.correct` | Order matters on the podium, not on the committee. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[6].feedback.generic` | Not quite right. Ask, for each choice, whether swapping two people makes a different outcome. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[6].feedback.byKey.kim` | You used ordered picks for both, as Kim did. A committee ignores order, so 336 counts each co... | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[6].feedback.byKey.swapped` | You used ordered picks for the committee and unordered ones for the podium. It is the other w... | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[6].explain.text` | Swapping two medallists changes the podium, so it keeps all $8 \times 7 \times 6 = 336$ order... | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[6].explain.canvas.caption` | Committee: 56 ways. Podium: 336 ways | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[7].prose` | Each time, you divided the ordered picks by the $k!$ orders of the chosen group. $$\binom{n}{... | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[7].question` | Which equals $\binom{9}{7}$? | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[7].widget.options[0].text` | $\dfrac{9!}{7!} = 72$ | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[7].widget.options[0].why` | That counts ordered picks of 2. Divide by the $2!$ orders as well. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[7].widget.options[1].text` | $\binom{7}{9}$ | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[7].widget.options[1].why` | You swapped top and bottom. You cannot choose 9 items from 7. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[7].widget.options[2].text` | $\binom{9}{2} = 36$ | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[7].widget.options[2].correct` | true | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[7].widget.options[3].text` | $\binom{7}{2} = 21$ | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[7].widget.options[3].why` | You took 2 from 7. Leaving 2 out of 9 is the same as keeping 7 of 9. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[7].feedback.correct` | Keeping 7 of 9 is leaving out 2: $\binom{9}{2} = 36$. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[7].feedback.generic` | Not quite right. Choosing 7 to keep is the same as choosing the 2 to leave out. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[7].explain.text` | Every choice of 7 to keep leaves exactly 2 out, and the other way round. So $\binom{9}{7} = \... | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[8].prose` | We derive $\binom{n}{k} = \dfrac{n!}{k!\,(n-k)!}$ the way you counted: ordered picks, then di... | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[8].question` | Put the lines of the derivation in order. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[8].widget.lines[0].text` | Ordered picks of $k$ from $n$: $\dfrac{n!}{(n-k)!}$, by the multiplication rule | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[8].widget.lines[1].text` | Each group of $k$ appears $k!$ times among them, once per order of its members | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[8].widget.lines[2].text` | So $\dfrac{n!}{(n-k)!} = \binom{n}{k} \times k!$, counting the same picks group by group | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[8].widget.lines[3].text` | $\binom{n}{k} = \dfrac{n!}{k!\,(n-k)!}$, dividing both sides by $k!$ | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[8].widget.answer` | ["ordered", "each", "equation", "divide"] | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[8].hints[0].text` | Start from something you can count directly. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[8].hints[1].text` | The ordered picks come first; the groups come from them. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[8].hints[2].text` | Count ordered picks, say how often each group appears, write the equation, then divide. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[8].feedback.correct` | Count in order, then divide out the orders. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[8].feedback.generic` | Not quite right. Begin with the ordered picks and end by dividing. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[8].feedback.byKey.divide` | Dividing by $k!$ is the last step. It needs the equation first. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[8].feedback.byKey.equation` | The equation uses the fact that each group appears $k!$ times. State that first. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[8].explain.text` | You counted ordered picks, noticed each group appears $k!$ times, and divided. With $n = 5$ a... | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[9].prose` | A risk team checks the correlation of every pair of assets in a 20-asset portfolio. The grid ... | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[9].canvas.state.caption` | 6 assets: 15 pairs above the diagonal | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[9].question` | How many pairs must the team check for all 20 assets? | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[9].widget.answer` | 190 | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[9].widget.accept` | 190 exactly: $\binom{20}{2} = \tfrac{20 \times 19}{2}$. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[9].widget.wrong[0].value` | 380 | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[9].widget.wrong[1].value` | 400 | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[9].widget.wrong[2].value` | 210 | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[9].widget.wrong[3].value` | 20 | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[9].hints[0].text` | Is the pair (asset 3, asset 7) different from (asset 7, asset 3)? | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[9].hints[1].text` | Correlation is symmetric, so order does not matter. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[9].hints[2].text` | Count ordered picks, $20 \times 19$, then halve. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[9].feedback.correct` | $\binom{20}{2} = 190$ pairs. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[9].feedback.generic` | Not quite right. Count pairs of two different assets, each pair once. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[9].feedback.byKey.ordered` | You counted both orders. The correlation of 3 with 7 is that of 7 with 3, so halve. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[9].feedback.byKey.whole` | You counted the whole $20 \times 20$ grid, diagonal and both halves. Keep one half. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[9].feedback.byKey.diagonal` | You kept the diagonal. An asset's correlation with itself is always 1, so skip it. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[9].feedback.byKey.assets` | That is the number of assets. Each one pairs with 19 others. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[9].explain.text` | Each pair is one cell above the diagonal. There are $20 \times 19 = 380$ ordered picks, and e... | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[10].prose` | A screen picks 3 stocks at random from a shortlist of 10 to build a basket. Every basket of 3... | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[10].question` | What is the chance the basket holds both miners? Give a fraction. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[10].widget.answer` | 0.06666666666666667 | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[10].widget.accept` | any form equal to $\tfrac{1}{15}$, such as $\tfrac{8}{120}$. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[10].widget.wrong[0].value` | 0.011111111111111112 | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[10].widget.wrong[1].value` | 0.2 | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[10].widget.wrong[2].value` | 0.01 | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[10].hints[0].text` | How many baskets are there in all? How many hold both miners? | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[10].hints[1].text` | There are $\binom{10}{3} = 120$ baskets. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[10].hints[2].text` | A basket with both miners needs 1 more stock from the other 8. So 8 baskets of 120. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[10].feedback.correct` | 8 of the 120 baskets: $\tfrac{1}{15}$. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[10].feedback.generic` | Not quite right. Count all baskets, then the baskets that contain both miners. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[10].feedback.byKey.ordered` | You counted the good baskets unordered but all baskets in order. Use the same kind of count f... | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[10].feedback.byKey.one-miner` | That is the chance of one particular pick being a miner. Both must end up in the basket. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[10].feedback.byKey.square` | You multiplied $\tfrac{1}{10}$ by itself, as if the picks were put back. Count baskets instead. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[10].explain.text` | All baskets: $\binom{10}{3} = 120$. Baskets with both miners: choose the third stock from the... | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `screens[10].explain.canvas.caption` | One of the 8 baskets with both miners | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `summary.ideas` | ["Ordered picks count each group once per order of its members, so divide by $k!$ to count gr... | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `summary.formula.name` | Combinations | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `summary.formula.tex` | \binom{n}{k} = \dfrac{n!}{k!\,(n-k)!} | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `summary.formula.note` | Ordered picks $\tfrac{n!}{(n-k)!}$ divided by the $k!$ orders of each group. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `summary.trap` | Ask whether swapping two chosen items gives a different outcome. A committee: no, use $\binom... | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `quiz[0].prose` | A fund builds an equal-weighted basket of 3 stocks from a shortlist of 10. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `quiz[0].question` | How many different baskets are possible? | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `quiz[0].widget.answer` | 120 | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `quiz[0].widget.accept` | 120 exactly: $\binom{10}{3}$. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `quiz[0].widget.wrong[0].value` | 720 | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `quiz[0].widget.wrong[1].value` | 1000 | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `quiz[0].widget.wrong[2].value` | 30 | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `quiz[0].feedback.correct` | $\tfrac{10 \times 9 \times 8}{3!} = 120$. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `quiz[0].feedback.generic` | Not quite right. Count ordered picks, then divide by the orders of one basket. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `quiz[0].feedback.byKey.ordered` | You counted ordered picks. The weights are equal, so the order of picking does not matter: di... | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `quiz[0].feedback.byKey.repeats` | You allowed a stock twice and kept order, $10^3$. Neither applies to a basket. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `quiz[0].feedback.byKey.thirty` | You multiplied 10 by 3. Count the picks stage by stage, then divide by $3!$. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `quiz[0].explain.text` | Ordered picks: $10 \times 9 \times 8 = 720$. Each basket appears $3! = 6$ times among them. S... | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `quiz[1].prose` | A league table of 10 strategies awards 1st, 2nd and 3rd place by return. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `quiz[1].question` | How many different top-three results are possible? | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `quiz[1].widget.answer` | 720 | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `quiz[1].widget.accept` | 720 exactly: $10 \times 9 \times 8$. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `quiz[1].widget.wrong[0].value` | 120 | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `quiz[1].widget.wrong[1].value` | 1000 | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `quiz[1].feedback.correct` | Order matters: $10 \times 9 \times 8 = 720$. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `quiz[1].feedback.generic` | Not quite right. Does swapping 1st and 2nd give a different result? | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `quiz[1].feedback.byKey.unordered` | You used a combination. Swapping 1st and 2nd changes the result, so keep all the orders. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `quiz[1].feedback.byKey.repeats` | A strategy cannot take two places. Each place has one fewer to choose from. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `quiz[1].explain.text` | First place has 10 choices, second 9, third 8. The places are different, so we keep every ord... | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `quiz[2].prose` | A desk keeps 13 of its 15 signals and drops the rest. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `quiz[2].question` | How many ways can it choose the 13 to keep? | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `quiz[2].widget.answer` | 105 | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `quiz[2].widget.accept` | 105 exactly: $\binom{15}{13} = \binom{15}{2}$. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `quiz[2].widget.wrong[0].value` | 210 | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `quiz[2].widget.wrong[1].value` | 15 | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `quiz[2].feedback.correct` | $\binom{15}{13} = \binom{15}{2} = 105$. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `quiz[2].feedback.generic` | Not quite right. Choosing 13 to keep is choosing 2 to drop. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `quiz[2].feedback.byKey.ordered-two` | You counted the 2 dropped signals in order, $15 \times 14$. Dropping A and B is the same as d... | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `quiz[2].feedback.byKey.fifteen` | That counts dropping one signal. Two are dropped. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `quiz[2].explain.text` | Each choice of 13 to keep fixes the 2 to drop. So $\binom{15}{13} = \binom{15}{2} = \tfrac{15... | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `quiz[3].prose` | You pick 2 of 6 stocks at random. Every pair is equally likely. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `quiz[3].question` | What is the chance that one particular stock, BP, is in your pair? Give a fraction. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `quiz[3].widget.answer` | 0.3333333333333333 | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `quiz[3].widget.accept` | any form equal to $\tfrac{1}{3}$, such as $\tfrac{5}{15}$. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `quiz[3].widget.wrong[0].value` | 0.16666666666666666 | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `quiz[3].feedback.correct` | 5 of the 15 pairs contain BP. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `quiz[3].feedback.generic` | Not quite right. Count all pairs, then the pairs that contain BP. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `quiz[3].feedback.byKey.one-pick` | That is the chance for one pick. You make two picks, so BP has two chances to be chosen. | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |
| l6 | `quiz[3].explain.text` | There are $\binom{6}{2} = 15$ pairs. BP pairs with each of the other 5 stocks, so 5 pairs con... | correct | Ross 1.4 (combinations, identity 4.1); itertools enumerated, L2 script |

## l7-replacement.json

| file | JSON path | claim (short) | verdict | basis |
|---|---|---|---|---|
| l7 | `screens[0].prose` | A bag holds 4 tokens numbered 1 to 4. You draw one, write its number down and put it back. Th... | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[0].canvas.state.caption` | Row: first draw. Column: second draw | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[0].question` | How many ordered results are possible? | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[0].widget.answer` | 16 | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[0].widget.accept` | 16 exactly: $4 \times 4$. | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[0].widget.wrong[0].value` | 12 | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[0].widget.wrong[1].value` | 8 | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[0].widget.wrong[2].value` | 10 | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[0].hints[0].text` | After the token goes back, how many tokens can the second draw give? | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[0].hints[1].text` | Every row has 4 cells, one for each second draw. | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[0].hints[2].text` | 4 choices, then 4 again: $4 \times 4$. | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[0].feedback.correct` | $4 \times 4 = 16$: the token goes back, so a repeat is possible. | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[0].feedback.generic` | Not quite right. Count every cell: any first draw, then any second draw. | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[0].feedback.byKey.no-repeats` | You removed the repeats such as (2, 2). The token goes back, so it can come out again. | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[0].feedback.byKey.added` | You added $4 + 4$. Each first draw pairs with all 4 second draws. | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[0].feedback.byKey.unordered` | You treated (1, 2) and (2, 1) as one result. The draws happen in order, first then second. | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[0].explain.text` | Putting the token back restores the bag, so the second draw has all 4 tokens again. Every cel... | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[1].prose` | New rule: the first token stays out of the bag. Then you draw the second from the 3 tokens left. | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[1].canvas.state.caption` | 16 cells: which can still happen? | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[1].question` | Tap every result that can no longer happen. | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[1].widget.answer` | ["r1c1", "r2c2", "r3c3", "r4c4"] | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[1].widget.wrong[0].set` | ["r1c1", "r1c2", "r1c3", "r1c4"] | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[1].hints[0].text` | If the first draw is 2, can the second draw be 2? | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[1].hints[1].text` | The impossible results repeat a number. | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[1].feedback.correct` | The four repeats are gone: 12 results remain. | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[1].feedback.generic` | Not quite right. A result is impossible when it needs the same token twice. | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[1].feedback.byKey.one-row` | You removed a whole row. Only the repeat in that row is impossible. | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[1].explain.text` | Keeping the token out rules out the diagonal: (1, 1), (2, 2), (3, 3) and (4, 4). That leaves ... | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[1].explain.canvas.caption` | 12 results left: $4 \times 3$ | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[2].prose` | Putting the item back is drawing **with replacement**. Keeping it out is drawing **without re... | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[2].canvas.state.caption` | Without replacement: 5 balls, then 4 | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[2].question` | What chance belongs on the branch marked ?, a second red after a first red? | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[2].widget.answer` | 0.5 | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[2].widget.accept` | any form equal to $\tfrac{2}{4} = \tfrac{1}{2}$. | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[2].widget.wrong[0].value` | 0.6 | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[2].widget.wrong[1].value` | 0.4 | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[2].widget.wrong[2].value` | 0.75 | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[2].hints[0].text` | After a red comes out, how many balls are left? How many are red? | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[2].hints[1].text` | The branch starts after one red has gone. | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[2].hints[2].text` | 4 balls are left, and 2 of them are red: $\tfrac{2}{4}$. | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[2].feedback.correct` | Two reds among the four left: $\tfrac{2}{4}$. | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[2].feedback.generic` | Not quite right. Update both counts: the reds left and the balls left. | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[2].feedback.byKey.fixed` | That is the chance on the first draw. One red ball is gone, so both counts change. | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[2].feedback.byKey.top-only` | You took one red off the top but kept 5 balls on the bottom. Only 4 balls are left. | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[2].feedback.byKey.bottom-only` | You took one ball off the bottom but kept 3 reds on top. The ball removed was red. | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[2].explain.text` | After a red, the bag holds 2 red and 2 blue, so the branch carries $\tfrac{2}{4}$. The second... | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[3].prose` | Same bag and the same two draws without replacement. A path's chance is the product of the ch... | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[3].canvas.state.caption` | Without replacement | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[3].question` | What is the chance both balls are red? | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[3].widget.answer` | 0.3 | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[3].widget.accept` | any form equal to $\tfrac{3}{10}$, such as $\tfrac{6}{20}$. | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[3].widget.wrong[0].value` | 0.36 | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[3].widget.wrong[1].value` | 0.24 | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[3].widget.wrong[2].value` | 1.1 | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[3].hints[0].text` | Follow the path Red then Red. | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[3].hints[1].text` | The path carries $\tfrac{3}{5}$ and then $\tfrac{2}{4}$. | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[3].hints[2].text` | Multiply: $\tfrac{3}{5} \times \tfrac{2}{4}$. | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[3].feedback.correct` | $\tfrac{3}{5} \times \tfrac{2}{4} = \tfrac{6}{20} = \tfrac{3}{10}$. | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[3].feedback.generic` | Not quite right. Multiply the two chances along the Red–Red path. | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[3].feedback.byKey.replaced` | That is $\tfrac{3}{5} \times \tfrac{3}{5}$, which puts the ball back. Use the second branch's... | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[3].feedback.byKey.fixed-denominator` | You used $\tfrac{3}{5} \times \tfrac{2}{5}$. The second draw has 4 balls, not 5. | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[3].feedback.byKey.added` | You added the chances, which gives more than 1. Both must happen, so multiply. | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[3].explain.text` | You multiplied along the path: $\tfrac{3}{5} \times \tfrac{2}{4} = \tfrac{3}{10}$. Counting a... | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[4].prose` | Now each ball goes back before the next draw. The bag is the same every time, so every branch... | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[4].canvas.state.caption` | With replacement: 5 balls every time | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[4].question` | What is the chance of red, then blue? | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[4].widget.answer` | 0.24 | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[4].widget.accept` | any form equal to $\tfrac{6}{25}$. | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[4].widget.wrong[0].value` | 0.3 | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[4].widget.wrong[1].value` | 0.48 | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[4].widget.wrong[2].value` | 1.0 | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[4].hints[0].text` | Which path is red, then blue? | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[4].hints[1].text` | Its branches carry $\tfrac{3}{5}$ and $\tfrac{2}{5}$. | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[4].hints[2].text` | Multiply: $\tfrac{3}{5} \times \tfrac{2}{5}$. | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[4].feedback.correct` | $\tfrac{3}{5} \times \tfrac{2}{5} = \tfrac{6}{25}$. | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[4].feedback.generic` | Not quite right. Multiply the chances on the Red–Blue path. | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[4].feedback.byKey.kept-out` | That is $\tfrac{3}{5} \times \tfrac{2}{4}$, the chance without replacement. Here the red goes... | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[4].feedback.byKey.either-order` | That counts blue then red as well. The question asks for red first. | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[4].feedback.byKey.added` | You added the chances. Both draws must happen, so multiply. | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[4].explain.text` | With replacement the second branch carries $\tfrac{2}{5}$ whatever came first. So the chance ... | imprecise | finding 1: independence means no result changes the chances of the others (Ross 3.4); without replacement the chance of red on draw 2 is also 3/5 before draw 1 is seen, yet the draws are dependent (L2 script) |
| l7 | `screens[5].prose` | A smaller bag: 2 red and 3 blue. You draw three balls without replacement. Follow the tree af... | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[5].canvas.state.caption` | Only the first-red branch is drawn in full | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[5].question` | What is the chance all three balls are red? | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[5].widget.answer` | 0 | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[5].widget.accept` | 0 exactly. | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[5].widget.wrong[0].value` | 0.064 | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[5].widget.wrong[1].value` | 0.1 | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[5].hints[0].text` | How many reds are in the bag? | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[5].hints[1].text` | After Red, Red the tree has only one branch. | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[5].hints[2].text` | Two reds cannot give three. The third red has no ball to come from. | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[5].feedback.correct` | Three reds from a bag with two is impossible. | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[5].feedback.generic` | Not quite right. Count the reds left after two red draws. | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[5].feedback.byKey.replaced` | That is $(\tfrac{2}{5})^3$, which puts each ball back. Without replacement the reds run out. | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[5].feedback.byKey.stopped` | That is the chance of two reds. The third draw still needs a red, and none are left. | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[5].explain.text` | After two reds the bag holds 3 blue balls, so the only branch is Blue with $\tfrac{3}{3}$. Re... | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[5].explain.canvas.caption` | After two reds, only blue is left | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[6].prose` | Jo draws two cards from a shuffled 52-card deck without putting the first back. The deck has ... | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[6].canvas.state.caption` | Without replacement | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[6].question` | Which working gives the chance both cards are aces? | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[6].widget.options[0].text` | $\dfrac{4}{52} \times \dfrac{3}{52} = \dfrac{3}{676}$ | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[6].widget.options[0].why` | That is Jo's working. It takes the ace off the top but keeps 52 cards below. The second draw ... | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[6].widget.options[1].text` | $\dfrac{4}{52} \times \dfrac{3}{51} = \dfrac{1}{221}$ | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[6].widget.options[1].correct` | true | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[6].widget.options[2].text` | $\dfrac{4}{52} \times \dfrac{4}{52} = \dfrac{1}{169}$ | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[6].widget.options[2].why` | That puts the first ace back. Without replacement, 3 aces remain among 51 cards. | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[6].widget.options[3].text` | $\dfrac{4}{52} + \dfrac{3}{51}$ | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[6].widget.options[3].why` | You added the chances. Both cards must be aces, so multiply along the path. | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[6].hints[0].text` | After one ace is drawn, how many aces are left? How many cards? | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[6].hints[1].text` | The marked branch starts after an ace has gone. | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[6].hints[2].text` | 3 aces among 51 cards. Multiply $\tfrac{4}{52}$ by $\tfrac{3}{51}$. | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[6].feedback.correct` | Both counts drop by one: $\tfrac{4}{52} \times \tfrac{3}{51}$. | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[6].feedback.generic` | Not quite right. After an ace, update the aces left and the cards left. | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[6].feedback.byKey.fixed` | That keeps the denominator at 52. The first card is gone, so the second draw has 51 cards. | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[6].feedback.byKey.replaced` | That puts the first ace back. Without replacement, 3 aces remain among 51 cards. | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[6].explain.text` | Drawing the first ace removes one ace and one card, so the branch is $\tfrac{3}{51}$. Then $\... | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[7].prose` | You counted two ways. With replacement each of $k$ draws has all $n$ items: $$n^k \text{ orde... | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[7].question` | You draw 3 of 10 numbered tokens without replacement, in order. How many ordered outcomes? | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[7].widget.options[0].text` | $10^3 = 1000$ | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[7].widget.options[0].why` | That puts each token back. Without replacement each draw has one fewer token. | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[7].widget.options[1].text` | $10 \times 9 \times 8 = 720$ | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[7].widget.options[1].correct` | true | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[7].widget.options[2].text` | $\binom{10}{3} = 120$ | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[7].widget.options[2].why` | That ignores the order of the draws. The question counts ordered outcomes. | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[7].widget.options[3].text` | $10 + 9 + 8 = 27$ | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[7].widget.options[3].why` | You added the draws. Each first token pairs with every later choice, so multiply. | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[7].feedback.correct` | Ten, then nine, then eight. | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[7].feedback.generic` | Not quite right. Without replacement, each draw has one token fewer than the last. | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[7].explain.text` | The first draw has 10 tokens, the second 9 and the third 8. So there are $10 \times 9 \times ... | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[8].prose` | The tree gave two aces a chance of $\tfrac{1}{221}$. Counting unordered hands must agree. Eac... | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[8].question` | Put the lines in order, from the ordered count to the answer. | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[8].widget.lines[0].text` | $P = \dfrac{4 \times 3}{52 \times 51}$: ordered ace pairs over ordered pairs, all equally likely | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[8].widget.lines[1].text` | $= \dfrac{(4 \times 3)/2}{(52 \times 51)/2}$: divide top and bottom by the 2 orders of each pair | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[8].widget.lines[2].text` | $= \dfrac{\binom{4}{2}}{\binom{52}{2}} = \dfrac{6}{1326}$: each count over 2 is a combination | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[8].widget.lines[3].text` | $= \dfrac{1}{221}$: cancel the 6 | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[8].widget.answer` | ["ordered", "halve", "binom", "cancel"] | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[8].hints[0].text` | Start from ordered draws: that is the tree's product. | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[8].hints[1].text` | The middle steps remove the order from both counts. | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[8].hints[2].text` | Ordered count, divide both by 2, name the combinations, then cancel. | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[8].feedback.correct` | Ordered or unordered, the chance is the same. | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[8].feedback.generic` | Not quite right. Start with the ordered counts, remove the order from both, then simplify. | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[8].feedback.byKey.binom` | The combinations appear only after dividing both counts by 2. Put that step first. | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[8].feedback.byKey.cancel` | Cancelling is the last step. | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[8].explain.text` | Dividing both counts by the same 2 orders leaves the fraction unchanged. So $\tfrac{\binom{4}... | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[9].prose` | A backtest has 20 trading days. A reviewer checks a random sample of 5 different days, every ... | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[9].canvas.state.caption` | 20 days; day 12 was the worst | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[9].question` | What is the chance the sample contains the worst day? Give a fraction. | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[9].widget.answer` | 0.25 | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[9].widget.accept` | any form equal to $\tfrac{1}{4}$, such as $1 - \tfrac{11628}{15504}$. | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[9].widget.wrong[0].value` | 0.2262 | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[9].widget.wrong[1].value` | 0.05 | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[9].widget.wrong[2].value` | 0.75 | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[9].hints[0].text` | Use the complement: how many samples leave the worst day out? | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[9].hints[1].text` | Samples without day 12 choose all 5 days from the other 19. | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[9].hints[2].text` | $1 - \tfrac{\binom{19}{5}}{\binom{20}{5}} = 1 - \tfrac{11628}{15504}$. | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[9].feedback.correct` | $1 - \tfrac{15}{20} = \tfrac{1}{4}$. | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[9].feedback.generic` | Not quite right. Count the samples that miss the worst day, then take the complement. | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[9].feedback.byKey.replaced` | That is $1 - (\tfrac{19}{20})^5$, which lets a day be picked twice. The sample has 5 differen... | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[9].feedback.byKey.one-draw` | That is the chance for one draw. The sample makes 5 draws. | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[9].feedback.byKey.complement` | That is the chance the sample misses the worst day. Take 1 minus it. | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[9].explain.text` | Samples that miss day 12: $\binom{19}{5} = 11628$ of $\binom{20}{5} = 15504$, which is $\tfra... | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `screens[10].prose` | A bootstrap resamples the same 20 days **with replacement**: 20 draws, each any of the 20 day... | correct | Efron and Tibshirani (1993), An Introduction to the Bootstrap (resampling with replacement; a point is left out with chance (1 - 1/n)^n); (19/20)^20 exact, Monte Carlo and the seeded run, L2 script |
| l7 | `screens[10].canvas.state.caption` | Each resample: 20 draws with replacement | correct | Efron and Tibshirani (1993), An Introduction to the Bootstrap (resampling with replacement; a point is left out with chance (1 - 1/n)^n); (19/20)^20 exact, Monte Carlo and the seeded run, L2 script |
| l7 | `screens[10].question` | Of 1,000 resamples, about how many leave out the worst day completely? | correct | Efron and Tibshirani (1993), An Introduction to the Bootstrap (resampling with replacement; a point is left out with chance (1 - 1/n)^n); (19/20)^20 exact, Monte Carlo and the seeded run, L2 script |
| l7 | `screens[10].widget.answer` | 358 | correct | Efron and Tibshirani (1993), An Introduction to the Bootstrap (resampling with replacement; a point is left out with chance (1 - 1/n)^n); (19/20)^20 exact, Monte Carlo and the seeded run, L2 script |
| l7 | `screens[10].widget.accept` | any whole number from 333 to 383. Exact: $1000 \times (\tfrac{19}{20})^{20} \approx 358.5$. | correct | Efron and Tibshirani (1993), An Introduction to the Bootstrap (resampling with replacement; a point is left out with chance (1 - 1/n)^n); (19/20)^20 exact, Monte Carlo and the seeded run, L2 script |
| l7 | `screens[10].widget.wrong[0].value` | 0 | correct | Efron and Tibshirani (1993), An Introduction to the Bootstrap (resampling with replacement; a point is left out with chance (1 - 1/n)^n); (19/20)^20 exact, Monte Carlo and the seeded run, L2 script |
| l7 | `screens[10].widget.wrong[1].value` | 950 | correct | Efron and Tibshirani (1993), An Introduction to the Bootstrap (resampling with replacement; a point is left out with chance (1 - 1/n)^n); (19/20)^20 exact, Monte Carlo and the seeded run, L2 script |
| l7 | `screens[10].widget.wrong[2].value` | 50 | correct | Efron and Tibshirani (1993), An Introduction to the Bootstrap (resampling with replacement; a point is left out with chance (1 - 1/n)^n); (19/20)^20 exact, Monte Carlo and the seeded run, L2 script |
| l7 | `screens[10].hints[0].text` | What is the chance one draw misses the worst day? | correct | Efron and Tibshirani (1993), An Introduction to the Bootstrap (resampling with replacement; a point is left out with chance (1 - 1/n)^n); (19/20)^20 exact, Monte Carlo and the seeded run, L2 script |
| l7 | `screens[10].hints[1].text` | One draw misses it with chance $\tfrac{19}{20}$, and the 20 draws are independent. | correct | Efron and Tibshirani (1993), An Introduction to the Bootstrap (resampling with replacement; a point is left out with chance (1 - 1/n)^n); (19/20)^20 exact, Monte Carlo and the seeded run, L2 script |
| l7 | `screens[10].hints[2].text` | All 20 must miss: $(\tfrac{19}{20})^{20} \approx 0.358$. Multiply by 1,000. | correct | Efron and Tibshirani (1993), An Introduction to the Bootstrap (resampling with replacement; a point is left out with chance (1 - 1/n)^n); (19/20)^20 exact, Monte Carlo and the seeded run, L2 script |
| l7 | `screens[10].feedback.correct` | About 36% of resamples never see the worst day. Run them to check. | correct | Efron and Tibshirani (1993), An Introduction to the Bootstrap (resampling with replacement; a point is left out with chance (1 - 1/n)^n); (19/20)^20 exact, Monte Carlo and the seeded run, L2 script |
| l7 | `screens[10].feedback.generic` | Not quite right. Every one of the 20 independent draws must miss the worst day. | correct | Efron and Tibshirani (1993), An Introduction to the Bootstrap (resampling with replacement; a point is left out with chance (1 - 1/n)^n); (19/20)^20 exact, Monte Carlo and the seeded run, L2 script |
| l7 | `screens[10].feedback.byKey.split` | That holds for a split, which uses every day once. A bootstrap draws with replacement, so a d... | correct | Efron and Tibshirani (1993), An Introduction to the Bootstrap (resampling with replacement; a point is left out with chance (1 - 1/n)^n); (19/20)^20 exact, Monte Carlo and the seeded run, L2 script |
| l7 | `screens[10].feedback.byKey.one-draw` | That is one draw: it misses 19 times in 20. All 20 draws must miss, so multiply 20 times. | correct | Efron and Tibshirani (1993), An Introduction to the Bootstrap (resampling with replacement; a point is left out with chance (1 - 1/n)^n); (19/20)^20 exact, Monte Carlo and the seeded run, L2 script |
| l7 | `screens[10].feedback.byKey.hit-once` | That is $1000 \times \tfrac{1}{20}$, the chance one draw hits the worst day. Ask for every dr... | correct | Efron and Tibshirani (1993), An Introduction to the Bootstrap (resampling with replacement; a point is left out with chance (1 - 1/n)^n); (19/20)^20 exact, Monte Carlo and the seeded run, L2 script |
| l7 | `screens[10].explain.text` | Draws with replacement are independent, each missing with chance $\tfrac{19}{20}$. All 20 mis... | correct | Efron and Tibshirani (1993), An Introduction to the Bootstrap (resampling with replacement; a point is left out with chance (1 - 1/n)^n); (19/20)^20 exact, Monte Carlo and the seeded run, L2 script |
| l7 | `summary.ideas` | ["With replacement, $k$ draws from $n$ give $n^k$ ordered outcomes, and the draws are indepen... | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `summary.formula.name` | Two aces, both ways | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `summary.formula.tex` | \dfrac{4}{52} \cdot \dfrac{3}{51} = \dfrac{1}{221} \quad \text{vs} \quad \dfrac{4}{52} \cdot ... | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `summary.formula.note` | Without replacement, then with. | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `summary.trap` | Without replacement, both counts drop: the items of the kind you drew and the items left. Kee... | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `quiz[0].prose` | You draw 2 tokens from 10 numbered tokens, putting the first back before the second draw. Ord... | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `quiz[0].question` | How many ordered outcomes are there? | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `quiz[0].widget.answer` | 100 | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `quiz[0].widget.accept` | 100 exactly: $10^2$. | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `quiz[0].widget.wrong[0].value` | 90 | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `quiz[0].widget.wrong[1].value` | 20 | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `quiz[0].widget.wrong[2].value` | 45 | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `quiz[0].feedback.correct` | $10 \times 10 = 100$. | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `quiz[0].feedback.generic` | Not quite right. With replacement, the second draw has all 10 tokens again. | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `quiz[0].feedback.byKey.without` | That keeps the first token out. Here it goes back, so the second draw has 10 choices. | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `quiz[0].feedback.byKey.added` | You added the draws. Each first token pairs with every second token. | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `quiz[0].feedback.byKey.unordered` | That counts unordered pairs without repeats. Here order matters and repeats are allowed. | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `quiz[0].explain.text` | Putting the token back restores all 10 for the second draw. So there are $10 \times 10 = 100$... | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `quiz[1].prose` | You draw two cards from a shuffled 52-card deck without replacement. The deck has 13 hearts. | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `quiz[1].question` | What is the chance both are hearts? Give a fraction. | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `quiz[1].widget.answer` | 0.058823529411764705 | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `quiz[1].widget.accept` | any form equal to $\tfrac{1}{17}$, such as $\tfrac{156}{2652}$. | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `quiz[1].widget.wrong[0].value` | 0.0625 | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `quiz[1].widget.wrong[1].value` | 0.057692307692307696 | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `quiz[1].feedback.correct` | $\tfrac{13}{52} \times \tfrac{12}{51} = \tfrac{1}{17}$. | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `quiz[1].feedback.generic` | Not quite right. After a heart, 12 hearts remain among 51 cards. | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `quiz[1].feedback.byKey.replaced` | That is $(\tfrac{1}{4})^2$, which puts the first heart back. | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `quiz[1].feedback.byKey.fixed` | You kept 52 cards for the second draw. Only 51 are left. | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `quiz[1].explain.text` | The first card is a heart with chance $\tfrac{13}{52}$. Then 12 hearts remain among 51 cards.... | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `quiz[2].prose` | A desk's watchlist has 3 banks and 4 miners. A screen picks 4 of the 7 stocks at random, with... | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `quiz[2].question` | What is the chance all 4 picks are banks? | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `quiz[2].widget.answer` | 0 | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `quiz[2].widget.accept` | 0 exactly. | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `quiz[2].widget.wrong[0].value` | 0.033735943356934604 | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `quiz[2].widget.wrong[1].value` | 0.02857142857142857 | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `quiz[2].feedback.correct` | Four banks from three is impossible. | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `quiz[2].feedback.generic` | Not quite right. How many banks are there to pick? | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `quiz[2].feedback.byKey.replaced` | That is $(\tfrac{3}{7})^4$, which lets a bank be picked twice. Without replacement, the banks... | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `quiz[2].feedback.byKey.three` | That is the chance the first three picks are banks. The fourth then has no bank left. | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `quiz[2].explain.text` | There are only 3 banks, and without replacement no stock is picked twice. So 4 banks cannot h... | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `quiz[3].prose` | Two draws are made from a bag of 3 red and 2 blue balls. | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `quiz[3].question` | In which case does the chance of red on the second draw not depend on the first? | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `quiz[3].widget.options[0].text` | Without replacement | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `quiz[3].widget.options[0].why` | Without replacement, the first ball changes the bag. The second chance is $\tfrac{2}{4}$ or $... | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `quiz[3].widget.options[1].text` | With replacement | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `quiz[3].widget.options[1].correct` | true | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `quiz[3].widget.options[2].text` | In both cases | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `quiz[3].widget.options[2].why` | Without replacement the bag changes, so the second chance depends on the first ball. | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `quiz[3].feedback.correct` | Putting the ball back restores the bag. | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `quiz[3].feedback.generic` | Not quite right. Ask whether the bag looks the same before the second draw. | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |
| l7 | `quiz[3].explain.text` | With replacement the bag is the same at every draw, so red always has chance $\tfrac{3}{5}$: ... | correct | Ross 2.5 (sampling with and without replacement), 3.4 (independence); exact enumerated, L2 script |

## fluency-l7-replacement.json

| file | JSON path | claim (short) | verdict | basis |
|---|---|---|---|---|
| fluency-l7-replacement | `families[0].prompt` | A bag holds {r} {c1} and {b} {c2} {it}. You draw two without replacement. What is the chance ... | correct | every r, b enumerated exactly, L2 script |
| fluency-l7-replacement | `families[0].widget.answer` | {key} | correct | every r, b enumerated exactly, L2 script |
| fluency-l7-replacement | `families[0].widget.accept` | ${key:frac}$, or an equal fraction | correct | every r, b enumerated exactly, L2 script |
| fluency-l7-replacement | `families[0].wrong[0].value` | {wrep} | correct | every r, b enumerated exactly, L2 script |
| fluency-l7-replacement | `families[0].wrong[0].line` | You used {r} out of {n} on both draws. Without replacement the second draw has one {c1} fewer... | correct | every r, b enumerated exactly, L2 script |
| fluency-l7-replacement | `families[0].wrong[1].value` | {keep} | correct | every r, b enumerated exactly, L2 script |
| fluency-l7-replacement | `families[0].wrong[1].line` | You took one off the {c1} count but kept {n} on the bottom. The bag holds {n - 1} items for t... | correct | every r, b enumerated exactly, L2 script |
| fluency-l7-replacement | `families[1].prompt` | A bag holds {r} {c1} and {b} {c2} {it}. You draw one, put it back, then draw again. What is t... | correct | every r, b enumerated exactly, L2 script |
| fluency-l7-replacement | `families[1].widget.answer` | {key} | correct | every r, b enumerated exactly, L2 script |
| fluency-l7-replacement | `families[1].widget.accept` | ${key:frac}$, or an equal fraction | correct | every r, b enumerated exactly, L2 script |
| fluency-l7-replacement | `families[1].wrong[0].value` | {nrep} | correct | every r, b enumerated exactly, L2 script |
| fluency-l7-replacement | `families[1].wrong[0].line` | You took one off the bottom for the second draw. The item went back, so the bag holds {n} ite... | correct | every r, b enumerated exactly, L2 script |
| fluency-l7-replacement | `families[1].wrong[1].value` | {both} | correct | every r, b enumerated exactly, L2 script |
| fluency-l7-replacement | `families[1].wrong[1].line` | You counted {c2} then {c1} as well. The question asks for {c1} first, then {c2}. | correct | every r, b enumerated exactly, L2 script |
| fluency-l7-replacement | `families[2].prompt` | A bag holds {r} {c1} and {b} {c2} {it}. You draw three without replacement. What is the chanc... | correct | every r, b enumerated exactly, L2 script |
| fluency-l7-replacement | `families[2].widget.answer` | {key} | correct | every r, b enumerated exactly, L2 script |
| fluency-l7-replacement | `families[2].widget.accept` | ${key:frac}$, or an equal fraction | correct | every r, b enumerated exactly, L2 script |
| fluency-l7-replacement | `families[2].wrong[0].value` | {wrep} | correct | every r, b enumerated exactly, L2 script |
| fluency-l7-replacement | `families[2].wrong[0].line` | You used {r} out of {n} on every draw. Without replacement each draw has one {c1} fewer and o... | correct | every r, b enumerated exactly, L2 script |
| fluency-l7-replacement | `families[2].wrong[1].value` | {keep} | correct | every r, b enumerated exactly, L2 script |
| fluency-l7-replacement | `families[2].wrong[1].line` | You took {c1} items off the top but kept {n} on the bottom. The bag shrinks by one each draw. | correct | every r, b enumerated exactly, L2 script |

## l8-stars-and-bars.json

| file | JSON path | claim (short) | verdict | basis |
|---|---|---|---|---|
| l8 | `screens[0].prose` | A jar holds 5 identical sweets. You share all of them among Amy, Ben and Cal. Ben gets none, ... | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[0].question` | Drag the sweets to share them that way. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[0].widget.count.amy` | 3 | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[0].widget.count.ben` | 0 | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[0].widget.count.cal` | 2 | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[0].hints[0].text` | Amy and Cal share all 5 sweets between them. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[0].hints[1].text` | Try giving Cal 2. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[0].hints[2].text` | Cal 2 and Amy 3 makes 5, and 3 is one more than 2. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[0].feedback.correct` | Amy 3, Ben 0, Cal 2. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[0].feedback.generic` | Not quite right. Use all 5 sweets, give Ben none, and give Amy one more than Cal. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[0].feedback.byKey.count-amy` | Amy should have one more than Cal, with all 5 sweets shared between those two. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[0].feedback.byKey.count-cal` | Cal should have one fewer than Amy, with all 5 sweets shared between those two. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[0].feedback.byKey.count-ben` | Ben gets none this time. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[0].explain.text` | You gave Amy 3, Ben 0 and Cal 2. The sweets are identical, so only the numbers matter. Writte... | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[0].explain.canvas.caption` | As a row: ●●● / / ●● | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[1].prose` | Every sharing of 5 sweets among 3 children is a row of 7 places: 5 sweets and 2 bars. Sweets ... | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[1].canvas.state.caption` | Tap two places to be bars; the rest are sweets | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[1].question` | Tap the 2 places for the bars that give Amy 0, Ben 4 and Cal 1. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[1].widget.answer` | ["c1", "c6"] | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[1].hints[0].text` | Amy gets nothing, so where must the first bar go? | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[1].hints[1].text` | The first bar comes before any sweet. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[1].feedback.correct` | / ●●●● / ●: Amy 0, Ben 4, Cal 1. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[1].feedback.generic` | Not quite right. Count the sweets before, between and after your two bars. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[1].feedback.byKey.c2` | A bar at place 2 leaves a sweet before it, so Amy would get 1. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[1].feedback.byKey.c5` | A bar at place 5 leaves Ben 3 sweets. He needs 4. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[1].feedback.byKey.c7` | A bar at the end leaves Cal nothing. He needs 1. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[1].explain.text` | Bars at places 1 and 6 give / ●●●● / ●. Each choice of 2 bar places out of 7 is exactly one s... | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[1].explain.canvas.caption` | / ●●●● / ● is Amy 0, Ben 4, Cal 1 | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[2].prose` | This way of coding a sharing is called **stars and bars**. The row below is Amy 3, Ben 0, Cal... | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[2].canvas.state.caption` | ●●● / / ●● is Amy 3, Ben 0, Cal 2 | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[2].question` | How many ways can the 5 sweets be shared among the 3 children? | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[2].widget.answer` | 21 | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[2].widget.accept` | 21 exactly: $\binom{7}{2}$. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[2].widget.wrong[0].value` | 243 | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[2].widget.wrong[1].value` | 10 | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[2].widget.wrong[2].value` | 42 | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[2].hints[0].text` | A sharing is fixed once you know where the 2 bars go. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[2].hints[1].text` | Choose 2 places out of 7 for the bars. The two bars look alike. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[2].hints[2].text` | $\binom{7}{2} = \tfrac{7 \times 6}{2} = 21$. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[2].feedback.correct` | $\binom{7}{2} = 21$ sharings. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[2].feedback.generic` | Not quite right. Count the ways to choose 2 of the 7 places for the bars. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[2].feedback.byKey.distinct` | That is $3^5$: each sweet picks a child. It counts sweets as different, but they are identical. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[2].feedback.byKey.five-places` | You chose 2 of 5 places. The row has 7 places: 5 sweets and 2 bars. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[2].feedback.byKey.ordered-bars` | You counted the bars in order. The bars look alike, so halve it. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[2].explain.text` | A sharing is a choice of 2 bar places out of 7, so there are $\binom{7}{2} = 21$. Empty share... | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[3].prose` | Now the jar holds 8 identical sweets for the same 3 children. One possible row is drawn: Amy ... | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[3].canvas.state.caption` | 8 stars and 2 bars: 10 places | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[3].question` | How many ways can the 8 sweets be shared? | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[3].widget.answer` | 45 | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[3].widget.accept` | 45 exactly: $\binom{10}{2}$. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[3].widget.wrong[0].value` | 6561 | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[3].widget.wrong[1].value` | 28 | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[3].widget.wrong[2].value` | 90 | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[3].widget.wrong[3].value` | 36 | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[3].hints[0].text` | How many places does the row have? | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[3].hints[1].text` | 8 stars and 2 bars make 10 places. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[3].hints[2].text` | Choose 2 of 10 for the bars: $\tfrac{10 \times 9}{2}$. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[3].feedback.correct` | $\binom{10}{2} = 45$. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[3].feedback.generic` | Not quite right. Count the places in the row, then choose 2 for the bars. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[3].feedback.byKey.distinct` | That is $3^8$, which treats the sweets as different. They are identical. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[3].feedback.byKey.eight-places` | You chose 2 of 8 places. The bars take places too: 10 in all. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[3].feedback.byKey.ordered-bars` | You counted the bars in order. They look alike, so halve it. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[3].feedback.byKey.nine-places` | You used 9 places. There are 8 stars and 2 bars, so 10. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[3].explain.text` | The row has $8 + 2 = 10$ places, and any 2 can be bars. So there are $\binom{10}{2} = 45$ sha... | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[4].prose` | Back to 5 sweets and 3 children, but now each child must get at least one. Line up the 5 star... | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[4].canvas.state.caption` | 5 stars with 4 gaps between them | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[4].question` | How many sharings give every child at least one sweet? | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[4].widget.answer` | 6 | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[4].widget.accept` | 6 exactly: $\binom{4}{2}$. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[4].widget.wrong[0].value` | 21 | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[4].widget.wrong[1].value` | 10 | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[4].widget.wrong[2].value` | 3 | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[4].hints[0].text` | How many gaps between the stars could take a bar? | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[4].hints[1].text` | There are 4 gaps, at places 2, 4, 6 and 8. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[4].hints[2].text` | Choose 2 of the 4 gaps: $\binom{4}{2} = 6$. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[4].feedback.correct` | $\binom{4}{2} = 6$. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[4].feedback.generic` | Not quite right. Choose 2 of the 4 gaps for the bars. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[4].feedback.byKey.any` | That allows empty shares. Each child needs at least one sweet. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[4].feedback.byKey.stars` | You chose 2 of the 5 stars. Bars go in the 4 gaps between stars. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[4].feedback.byKey.children` | You counted the children. Count the ways to choose 2 gaps of 4. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[4].explain.text` | One bar per gap keeps every group non-empty, so choose 2 of the 4 gaps: $\binom{4}{2} = 6$. A... | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[4].explain.canvas.caption` | ● ● / ● ● / ● is 2, 2, 1 | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[5].prose` | A fund has 12 identical lots to place, and only one broker. With $k = 1$ child there are $k -... | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[5].canvas.state.caption` | 12 stars, no bars | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[5].question` | How many ways can the 12 lots be shared with one broker? | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[5].widget.answer` | 1 | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[5].widget.accept` | 1 exactly: $\binom{12}{0}$. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[5].widget.wrong[0].value` | 12 | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[5].widget.wrong[1].value` | 13 | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[5].widget.wrong[2].value` | 0 | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[5].hints[0].text` | Can the single broker get anything other than all 12? | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[5].hints[1].text` | With no bars, the row is fixed. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[5].hints[2].text` | The formula gives $\binom{12 + 1 - 1}{0} = \binom{12}{0} = 1$. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[5].feedback.correct` | One way: everything to the one broker. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[5].feedback.generic` | Not quite right. With one broker, every lot must go to that broker. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[5].feedback.byKey.lots` | You counted the lots. They are identical, and all must go to the one broker: one sharing. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[5].feedback.byKey.places` | You counted places for a bar. With one broker there are no bars to place. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[5].feedback.byKey.none` | There is a sharing: the broker gets all 12. That is one way, not none. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[5].explain.text` | With one broker, all 12 lots go to that broker, so there is exactly one sharing. The formula ... | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[6].prose` | Sam shares 5 identical £1 coins among Amy, Ben and Cal, empty shares allowed. Sam says each c... | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[6].question` | How many different sharings are there? | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[6].widget.options[0].text` | 243 | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[6].widget.options[0].why` | That is Sam's count. It treats coin 1 to Amy and coin 2 to Ben as different from the swap. Id... | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[6].widget.options[1].text` | 21 | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[6].widget.options[1].correct` | true | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[6].widget.options[2].text` | 125 | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[6].widget.options[2].why` | That is $5^3$, as if each child picks a number from 5. The amounts must also add to 5. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[6].widget.options[3].text` | 10 | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[6].widget.options[3].why` | That is $\binom{5}{2}$, bars among the coins only. The bars need places of their own: 7 in all. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[6].hints[0].text` | Does it matter which £1 coin Amy gets? | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[6].hints[1].text` | Only the amounts each child gets matter: Amy 2, Ben 2, Cal 1 is one sharing. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[6].hints[2].text` | Use stars and bars: 5 stars, 2 bars, $\binom{7}{2}$. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[6].feedback.correct` | Identical coins: $\binom{7}{2} = 21$. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[6].feedback.generic` | Not quite right. Only the number of coins each child gets matters. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[6].feedback.byKey.distinct` | That is Sam's count. It treats coin 1 to Amy and coin 2 to Ben as different from the swap. Id... | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[6].explain.text` | $3^5 = 243$ counts coins that can be told apart, such as 5 different bonds. With identical co... | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[6].explain.canvas.caption` | Amy 2, Ben 2, Cal 1 is one sharing, whichever coins go where | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[7].prose` | Each time, you placed $k - 1$ bars among $n$ identical stars. So $n$ identical items go to $k... | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[7].question` | How many ways can 6 identical sweets go to 4 children, empty shares allowed? | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[7].widget.options[0].text` | $4^6 = 4096$ | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[7].widget.options[0].why` | That treats the sweets as different. Identical sweets need stars and bars. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[7].widget.options[1].text` | $\binom{9}{4} = 126$ | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[7].widget.options[1].why` | You chose 4 places, one per child. Four children need only 3 bars. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[7].widget.options[2].text` | $\binom{9}{3} = 84$ | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[7].widget.options[2].correct` | true | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[7].widget.options[3].text` | $\binom{5}{3} = 10$ | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[7].widget.options[3].why` | That makes every child get at least one. Here empty shares are allowed. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[7].feedback.correct` | 6 stars and 3 bars: $\binom{9}{3} = 84$. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[7].feedback.generic` | Not quite right. Use $n = 6$ stars and $k - 1 = 3$ bars. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[7].explain.text` | Six stars and three bars make 9 places, and any 3 can be bars. So there are $\binom{9}{3} = 8... | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[8].prose` | For 3 children the count is $\binom{n+2}{2}$, the ways to place 2 bars among $n + 2$ places. ... | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[8].question` | Simplify: write the number of sharings among 3 children in terms of $n$. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[8].widget.answer` | \frac{(n+2)(n+1)}{2} | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[8].widget.accept` | ["(n+2)(n+1)/2", "(n^2+3n+2)/2", "\\frac{n^2+3n+2}{2}"] | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[8].widget.wrong[0].tex` | 3^n | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[8].widget.wrong[1].tex` | (n+2)(n+1) | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[8].widget.wrong[2].tex` | \frac{n(n-1)}{2} | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[8].hints[0].text` | Simplify $n + 2 - 1$ first. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[8].hints[1].text` | $n + 2 - 1 = n + 1$. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[8].hints[2].text` | So the count is $(n+2)(n+1)$ over 2. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[8].feedback.correct` | $\tfrac{(n+2)(n+1)}{2}$: with $n = 5$ it gives 21. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[8].feedback.generic` | Not quite right. Replace $n + 2 - 1$ by $n + 1$ and keep the division by 2. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[8].feedback.byKey.distinct` | $3^n$ treats the items as different. Identical items give the stars and bars count. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[8].feedback.byKey.no-half` | You kept the ordered pairs of bar places. The bars look alike, so divide by 2. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[8].feedback.byKey.n-places` | That places the bars among $n$ places only. The bars add 2 places, so use $n + 2$. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[8].explain.text` | $n + 2 - 1 = n + 1$, so the count is $\tfrac{(n+2)(n+1)}{2}$. Check: $n = 5$ gives $\tfrac{7 ... | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[9].prose` | You split £10,000 across 4 funds in whole £1,000 units. A fund may get nothing. Only the amou... | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[9].canvas.state.caption` | Each ball is one £1,000 unit | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[9].question` | How many different allocations are possible? | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[9].widget.answer` | 286 | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[9].widget.accept` | 286 exactly: $\binom{13}{3}$. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[9].widget.wrong[0].value` | 1048576 | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[9].widget.wrong[1].value` | 120 | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[9].widget.wrong[2].value` | 715 | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[9].widget.wrong[3].value` | 84 | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[9].hints[0].text` | How many stars, and how many bars? | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[9].hints[1].text` | 10 units are the stars; 4 funds need 3 bars. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[9].hints[2].text` | Choose 3 of 13 places: $\binom{13}{3} = \tfrac{13 \times 12 \times 11}{6}$. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[9].feedback.correct` | $\binom{13}{3} = 286$ allocations. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[9].feedback.generic` | Not quite right. Use 10 stars and 3 bars, and choose the bar places. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[9].feedback.byKey.distinct` | That is $4^{10}$, which treats each £1,000 unit as different. Only the amounts matter. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[9].feedback.byKey.no-bar-places` | You chose 3 of 10 places. The 3 bars need places too: 13 in all. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[9].feedback.byKey.k-bars` | You used 4 bars. Four funds need only 3 bars to separate them. | imprecise | finding 11: 715 = C(13,4) chooses 4 of the 13 places; a row with 4 bars has 14 places, C(14,4) = 1001 |
| l8 | `screens[9].feedback.byKey.at-least-one` | That gives every fund at least £1,000. Here a fund may get nothing. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[9].explain.text` | Ten £1,000 units are stars and 3 bars split them into 4 funds. Choosing 3 of the 13 places gi... | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `screens[9].explain.canvas.caption` | One allocation: £4k, £3k, £0, £3k | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `summary.ideas` | ["A sharing of $n$ identical items among $k$ people is a row of $n$ stars and $k - 1$ bars.",... | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `summary.formula.name` | Stars and bars | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `summary.formula.tex` | \binom{n + k - 1}{k - 1} | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `summary.formula.note` | $n$ identical items, $k$ people, empty shares allowed. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `summary.trap` | $k^n$ lets each item pick a person, which counts items as different. Identical items need sta... | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `quiz[0].prose` | A desk allocates 20 identical lots across 5 brokers. A broker may get none. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `quiz[0].question` | How many allocations are possible? | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `quiz[0].widget.answer` | 10626 | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `quiz[0].widget.accept` | 10,626 exactly: $\binom{24}{4}$. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `quiz[0].widget.wrong[0].value` | 4845 | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `quiz[0].widget.wrong[1].value` | 42504 | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `quiz[0].widget.wrong[2].value` | 3876 | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `quiz[0].feedback.correct` | 20 stars, 4 bars: $\binom{24}{4} = 10{,}626$. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `quiz[0].feedback.generic` | Not quite right. Use $\binom{n + k - 1}{k - 1}$ with $n = 20$ and $k = 5$. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `quiz[0].feedback.byKey.no-bar-places` | You chose 4 of 20 places. The bars add 4 places: 24 in all. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `quiz[0].feedback.byKey.k-bars` | You chose 5 bar places. Five brokers need only 4 bars. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `quiz[0].feedback.byKey.at-least-one` | That gives every broker at least one lot. Here a broker may get none. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `quiz[0].explain.text` | The 20 lots are stars and 4 bars split them among 5 brokers. That is $\binom{24}{4} = 10{,}62... | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `quiz[1].prose` | Seven identical client orders are routed to 3 desks. Every desk must get at least one order. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `quiz[1].question` | How many routings are possible? | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `quiz[1].widget.answer` | 15 | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `quiz[1].widget.accept` | 15 exactly: $\binom{6}{2}$. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `quiz[1].widget.wrong[0].value` | 36 | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `quiz[1].widget.wrong[1].value` | 21 | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `quiz[1].feedback.correct` | Bars in 2 of the 6 gaps: 15. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `quiz[1].feedback.generic` | Not quite right. Put the 2 bars in the 6 gaps between the 7 orders. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `quiz[1].feedback.byKey.empty-allowed` | That allows a desk with nothing. Each desk needs at least one order. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `quiz[1].feedback.byKey.seven-gaps` | 7 stars have 6 gaps between them, not 7. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `quiz[1].explain.text` | Seven stars have 6 gaps between them. Two bars in different gaps give every desk at least one... | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `quiz[2].prose` | Now the items are different: 5 different bonds go into 3 portfolios, and a portfolio may stay... | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `quiz[2].question` | How many assignments are possible? | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `quiz[2].widget.options[0].text` | $\binom{7}{2} = 21$ | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `quiz[2].widget.options[0].why` | Stars and bars counts identical items. Different bonds can be told apart, so who gets which b... | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `quiz[2].widget.options[1].text` | $3^5 = 243$ | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `quiz[2].widget.options[1].correct` | true | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `quiz[2].widget.options[2].text` | $5^3 = 125$ | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `quiz[2].widget.options[2].why` | You let each portfolio pick a bond. Each bond picks a portfolio: 3 choices, 5 times. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `quiz[2].feedback.correct` | Each bond picks one of 3 portfolios. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `quiz[2].feedback.generic` | Not quite right. Each of the 5 bonds is a stage with 3 choices. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `quiz[2].explain.text` | Each of the 5 different bonds goes to one of 3 portfolios, so the multiplication rule gives $... | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `quiz[3].prose` | Count the solutions of $x_1 + x_2 + x_3 + x_4 = 3$, where each $x_i$ is a whole number 0 or m... | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `quiz[3].question` | How many solutions are there? | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `quiz[3].widget.answer` | 20 | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `quiz[3].widget.accept` | 20 exactly: $\binom{6}{3}$. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `quiz[3].widget.wrong[0].value` | 4 | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `quiz[3].widget.wrong[1].value` | 64 | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `quiz[3].widget.wrong[2].value` | 15 | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `quiz[3].feedback.correct` | 3 stars and 3 bars: $\binom{6}{3} = 20$. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `quiz[3].feedback.generic` | Not quite right. Each $x_i$ is a child's share of 3 identical stars. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `quiz[3].feedback.byKey.three-bars-wrong` | That is $\binom{4}{3}$, bars among the 4 variables. Use 3 stars and 3 bars: 6 places. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `quiz[3].feedback.byKey.distinct` | That is $4^3$, as if the 3 units were different. They are identical. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `quiz[3].feedback.byKey.four-bars` | You chose 4 bar places, one per variable. Four variables need only 3 bars: $\binom{6}{3}$. | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |
| l8 | `quiz[3].explain.text` | Each solution shares 3 identical units among 4 variables. Stars and bars: 3 stars and 3 bars,... | correct | Ross 1.6 Props. 6.1 and 6.2 (integer solutions); brute force over all sharings, L2 script |

## review-2.json

| file | JSON path | claim (short) | verdict | basis |
|---|---|---|---|---|
| review-2 | `items[0].prose` | You roll a fair die three times. | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[0].question` | What is the chance all three rolls are different? Give a fraction. | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[0].widget.answer` | 0.5555555555555556 | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[0].widget.accept` | any form equal to $\tfrac{5}{9}$, such as $\tfrac{120}{216}$. | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[0].widget.wrong[0].value` | 1.0 | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[0].widget.wrong[1].value` | 0.09259259259259259 | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[0].widget.wrong[2].value` | 0.8333333333333334 | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[0].feedback.correct` | $\tfrac{6 \times 5 \times 4}{6^3} = \tfrac{120}{216} = \tfrac{5}{9}$. | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[0].feedback.generic` | Not quite right. Count the ordered rolls with no repeat, over all $6^3$ ordered rolls. | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[0].feedback.byKey.repeats` | You counted every roll as different. Rolls like (2, 2, 5) repeat a face. | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[0].feedback.byKey.unordered` | You counted unordered sets of faces, $\binom{6}{3} = 20$, over ordered rolls. Use ordered cou... | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[0].feedback.byKey.one-pair` | That is the chance the first two rolls differ. The third must differ from both. | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[0].explain.text` | All $6^3 = 216$ ordered rolls are equally likely. Rolls with no repeat: $6 \times 5 \times 4 ... | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[1].prose` | Nine traders each shake hands once with every other trader. | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[1].question` | How many handshakes are there? | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[1].widget.answer` | 36 | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[1].widget.accept` | 36 exactly: $\binom{9}{2}$. | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[1].widget.wrong[0].value` | 72 | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[1].widget.wrong[1].value` | 81 | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[1].widget.wrong[2].value` | 9 | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[1].feedback.correct` | $\binom{9}{2} = 36$. | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[1].feedback.generic` | Not quite right. A handshake is an unordered pair of two different traders. | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[1].feedback.byKey.ordered` | You counted A with B and B with A. That is one handshake, so halve it. | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[1].feedback.byKey.square` | You counted a trader shaking their own hand, and each pair twice. | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[1].feedback.byKey.nine` | That counts traders. Each one shakes 8 hands, and each handshake has two people. | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[1].explain.text` | Each handshake is a pair of traders, with no order. There are $9 \times 8 = 72$ ordered pairs... | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[2].prose` | A bag holds 4 red and 6 blue balls. You draw two without replacement. | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[2].question` | What is the chance both balls are the same colour? Give a fraction. | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[2].widget.answer` | 0.4666666666666667 | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[2].widget.accept` | any form equal to $\tfrac{7}{15}$, such as $\tfrac{42}{90}$. | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[2].widget.wrong[0].value` | 0.52 | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[2].widget.wrong[1].value` | 0.13333333333333333 | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[2].widget.wrong[2].value` | 0.42 | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[2].feedback.correct` | $\tfrac{4}{10}\cdot\tfrac{3}{9} + \tfrac{6}{10}\cdot\tfrac{5}{9} = \tfrac{7}{15}$. | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[2].feedback.generic` | Not quite right. Add the two paths: red then red, and blue then blue. | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[2].feedback.byKey.replaced` | That is $0.4^2 + 0.6^2$, which puts the first ball back. | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[2].feedback.byKey.red-only` | That is red then red only. Blue then blue is also the same colour. | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[2].feedback.byKey.fixed` | You kept 10 balls for the second draw. Only 9 are left. | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[2].explain.text` | Red, red: $\tfrac{4}{10} \times \tfrac{3}{9} = \tfrac{12}{90}$. Blue, blue: $\tfrac{6}{10} \t... | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[3].prose` | A desk shares 9 identical bonus units of £1,000 among 3 traders. Each trader gets at least on... | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[3].question` | How many ways can the units be shared? | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[3].widget.answer` | 28 | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[3].widget.accept` | 28 exactly: $\binom{8}{2}$. | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[3].widget.wrong[0].value` | 55 | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[3].widget.wrong[1].value` | 19683 | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[3].widget.wrong[2].value` | 36 | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[3].feedback.correct` | Bars in 2 of 8 gaps: $\binom{8}{2} = 28$. | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[3].feedback.generic` | Not quite right. Put 2 bars into the 8 gaps between 9 stars. | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[3].feedback.byKey.empty-allowed` | That is $\binom{11}{2}$, which lets a trader get nothing. | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[3].feedback.byKey.distinct` | That is $3^9$, as if the units were different. Only the amounts matter. | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[3].feedback.byKey.nine-gaps` | Nine stars have 8 gaps between them, not 9. | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[3].explain.text` | Each trader needs at least one unit, so the 2 bars go in different gaps between the 9 stars. ... | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[4].prose` | Each choice below picks 3 items from 10. | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[4].question` | Which are counted by $\binom{10}{3} = 120$? Select all that apply. | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[4].widget.options[0].text` | 3 stocks for an equal-weighted basket | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[4].widget.options[0].correct` | true | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[4].widget.options[1].text` | Gold, silver and bronze for 3 of 10 strategies | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[4].widget.options[1].why` | The medals differ, so order matters: $10 \times 9 \times 8 = 720$. | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[4].widget.options[2].text` | A 3-person committee with equal votes | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[4].widget.options[2].correct` | true | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[4].widget.options[3].text` | A 3-digit code where digits may repeat | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[4].widget.options[3].why` | Order matters and repeats are allowed: $10^3 = 1000$. | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[4].feedback.correct` | The basket and the committee ignore order. | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[4].feedback.generic` | Not quite right. Ask whether swapping two chosen items gives a different outcome. | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[4].explain.text` | The basket and the committee stay the same when two members swap, so $\binom{10}{3}$ counts t... | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[5].prose` | You draw a card from a 52-card deck, put it back and shuffle, then draw again. | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[5].question` | What is the chance both cards are aces? Give a fraction. | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[5].widget.answer` | 0.005917159763313609 | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[5].widget.accept` | any form equal to $\tfrac{1}{169}$. | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[5].widget.wrong[0].value` | 0.004524886877828055 | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[5].widget.wrong[1].value` | 0.15384615384615385 | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[5].feedback.correct` | $\tfrac{4}{52} \times \tfrac{4}{52} = \tfrac{1}{169}$. | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[5].feedback.generic` | Not quite right. With replacement, the second draw sees the full deck again. | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[5].feedback.byKey.without` | That is the chance without replacement. Here the first card goes back. | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[5].feedback.byKey.added` | You added the chances. Both draws must be aces, so multiply. | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[5].explain.text` | Putting the card back restores 4 aces in 52 cards. The draws are independent, so multiply: $\... | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[6].prose` | Four funds receive whole numbers of identical units, $x_1 + x_2 + x_3 + x_4 = 6$, each $x_i \... | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[6].question` | How many solutions are there? | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[6].widget.answer` | 84 | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[6].widget.accept` | 84 exactly: $\binom{9}{3}$. | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[6].widget.wrong[0].value` | 126 | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[6].widget.wrong[1].value` | 20 | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[6].widget.wrong[2].value` | 4096 | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[6].widget.wrong[3].value` | 10 | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[6].feedback.correct` | 6 stars and 3 bars: $\binom{9}{3} = 84$. | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[6].feedback.generic` | Not quite right. Use 6 stars and 3 bars. | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[6].feedback.byKey.k-bars` | You used 4 bars. Four funds need 3 bars. | imprecise | finding 11: 126 = C(9,4) chooses 4 of the 9 places; a row with 4 bars has 10 places, C(10,4) = 210 |
| review-2 | `items[6].feedback.byKey.no-bar-places` | You chose 3 of 6 places. The bars add 3 places: 9. | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[6].feedback.byKey.distinct` | That is $4^6$, as if the units were different. | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[6].feedback.byKey.at-least-one` | That forces every $x_i \ge 1$. Zero is allowed here. | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[6].explain.text` | Each solution is a row of 6 stars and 3 bars. Choosing the 3 bar places of 9 gives $\binom{9}... | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[7].prose` | You are dealt 5 cards from a shuffled 52-card deck, every hand equally likely. | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[7].question` | What is the chance all 5 are hearts? Give a fraction. | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[7].widget.answer` | 0.0004951980792316927 | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[7].widget.accept` | any form equal to $\tfrac{33}{66640}$, such as $\tfrac{1287}{2598960}$, about 0.000495. | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[7].widget.wrong[0].value` | 0.0009765625 | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[7].widget.wrong[1].value` | 4.126650660264106e-06 | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[7].feedback.correct` | $\tfrac{\binom{13}{5}}{\binom{52}{5}} = \tfrac{1287}{2598960}$. | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[7].feedback.generic` | Not quite right. Count hands of 5 hearts over all hands of 5, both unordered. | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[7].feedback.byKey.replaced` | That is $(\tfrac{1}{4})^5$, which puts each card back. Hearts run down as you deal. | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[7].feedback.byKey.mixed` | You counted heart hands unordered but all hands in order. Use the same kind of count on both ... | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |
| review-2 | `items[7].explain.text` | Heart hands: $\binom{13}{5} = 1287$. All hands: $\binom{52}{5} = 2{,}598{,}960$. So the chanc... | correct | Ross 1.2 to 1.6, 2.5; enumerated, L2 script |

## homework-2.json

| file | JSON path | claim (short) | verdict | basis |
|---|---|---|---|---|
| homework-2 | `items[0].prose` | A trading app uses a 6-digit PIN. The firm bans repeated digits, so 112233 is not allowed but... | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[0].question` | How many PINs are allowed? | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[0].widget.answer` | 151200 | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[0].widget.accept` | 151,200 exactly: $\tfrac{10!}{4!}$. | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[0].widget.wrong[0].value` | 1000000 | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[0].widget.wrong[1].value` | 210 | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[0].widget.wrong[2].value` | 30240 | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[0].feedback.correct` | $10 \times 9 \times 8 \times 7 \times 6 \times 5 = 151{,}200$. | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[0].feedback.generic` | Not quite right. Count the choices for each digit in turn, one fewer each time. | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[0].feedback.byKey.repeats` | That is $10^6$, which allows repeats. | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[0].feedback.byKey.unordered` | That is $\binom{10}{6}$, which ignores order. 019283 and 910283 are different PINs. | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[0].feedback.byKey.five-stages` | That stops after 5 digits. A PIN has 6. | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[0].explain.text` | The digits are 6 stages with 10, 9, 8, 7, 6 and 5 choices. So there are $\tfrac{10!}{4!} = 15... | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[1].prose` | A screen picks 4 of 12 stocks at random for a portfolio, every set of 4 equally likely. | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[1].question` | What is the chance that both AZN and GSK are picked? Give a fraction. | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[1].widget.answer` | 0.09090909090909091 | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[1].widget.accept` | any form equal to $\tfrac{1}{11}$, such as $\tfrac{45}{495}$. | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[1].widget.wrong[0].value` | 0.3333333333333333 | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[1].widget.wrong[1].value` | 0.1111111111111111 | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[1].widget.wrong[2].value` | 0.003787878787878788 | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[1].feedback.correct` | $\tfrac{\binom{10}{2}}{\binom{12}{4}} = \tfrac{45}{495} = \tfrac{1}{11}$. | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[1].feedback.generic` | Not quite right. Count the sets with both stocks, over all sets of 4. | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[1].feedback.byKey.one` | That is the chance AZN alone is picked. GSK must be picked too. | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[1].feedback.byKey.square` | That is $(\tfrac{1}{3})^2$, as if the two picks were independent. Without replacement they ar... | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[1].feedback.byKey.ordered-mix` | You counted all portfolios in order but the good ones without. Use one kind of count. | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[1].explain.text` | Sets with both: fix AZN and GSK, then choose 2 more from the other 10: $\binom{10}{2} = 45$. ... | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[2].prose` | Three cards are dealt from a shuffled 52-card deck without replacement. | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[2].question` | What is the chance all three share a suit? Give a fraction. | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[2].widget.answer` | 0.05176470588235294 | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[2].widget.accept` | any form equal to $\tfrac{22}{425}$, about 0.0518. | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[2].widget.wrong[0].value` | 0.012941176470588235 | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[2].widget.wrong[1].value` | 0.0625 | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[2].widget.wrong[2].value` | 0.04881656804733728 | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[2].feedback.correct` | $\tfrac{12}{51} \times \tfrac{11}{50} = \tfrac{22}{425}$. | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[2].feedback.generic` | Not quite right. The first card sets the suit; the next two must match it. | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[2].feedback.byKey.one-suit` | That is the chance all three are hearts. Any of the 4 suits will do. | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[2].feedback.byKey.replaced` | That is $(\tfrac{1}{4})^2$, which puts the cards back. | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[2].feedback.byKey.fixed` | You kept 52 cards on every draw. The deck shrinks to 51, then 50. | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[2].explain.text` | The first card can be anything. The second matches its suit with chance $\tfrac{12}{51}$, the... | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[3].prose` | Each of 4 desks must get at least one of $n$ identical orders, with $n \ge 4$. The count is $... | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[3].question` | Write the number of routings as a polynomial expression in $n$. | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[3].widget.answer` | \frac{(n-1)(n-2)(n-3)}{6} | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[3].widget.accept` | ["(n-1)(n-2)(n-3)/6", "\\frac{n^3-6n^2+11n-6}{6}", "(n^3-6n^2+11n-6)/6"] | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[3].widget.wrong[0].tex` | \frac{(n+3)(n+2)(n+1)}{6} | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[3].widget.wrong[1].tex` | (n-1)(n-2)(n-3) | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[3].widget.wrong[2].tex` | 4^n | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[3].feedback.correct` | $\tfrac{(n-1)(n-2)(n-3)}{6}$: with $n = 7$ it gives 20. | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[3].feedback.generic` | Not quite right. Put $m = n - 1$ into $\tfrac{m(m-1)(m-2)}{6}$. | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[3].feedback.byKey.empty-allowed` | That is $\binom{n+3}{3}$, which lets a desk get nothing. | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[3].feedback.byKey.no-divide` | You kept the ordered picks of bar places. Divide by $3! = 6$. | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[3].feedback.byKey.distinct` | That treats the orders as different. They are identical. | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[3].explain.text` | Substituting $m = n - 1$ gives $\tfrac{(n-1)(n-2)(n-3)}{6}$. Checks: $n = 4$ gives 1, one ord... | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[4].prose` | Ten identical lots go to brokers A, B and C. Broker A has a minimum order of 2 lots; B and C ... | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[4].question` | How many allocations are possible? | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[4].widget.answer` | 45 | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[4].widget.accept` | 45 exactly: $\binom{10}{2}$. | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[4].widget.wrong[0].value` | 66 | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[4].widget.wrong[1].value` | 55 | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[4].widget.wrong[2].value` | 15 | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[4].feedback.correct` | Give A 2 first, then share 8 freely: $\binom{10}{2} = 45$. | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[4].feedback.generic` | Not quite right. Hand A its 2 lots first, then share what is left with stars and bars. | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[4].feedback.byKey.ignore-min` | That is $\binom{12}{2}$, which ignores A's minimum. | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[4].feedback.byKey.subtract-one` | You gave A only 1 lot first. The minimum is 2. | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[4].feedback.byKey.all-min` | You gave every broker 2 first. Only A has a minimum. | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[4].explain.text` | Give A its 2 lots first. The other 8 lots are shared freely among 3 brokers: 8 stars and 2 ba... | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[5].prose` | A backtest has 20 trading days. An auditor samples 5 different days at random, every set of 5... | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[5].question` | What is the chance the sample contains both the best and the worst day? Give a fraction. | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[5].widget.answer` | 0.05263157894736842 | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[5].widget.accept` | any form equal to $\tfrac{1}{19}$, such as $\tfrac{816}{15504}$. | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[5].widget.wrong[0].value` | 0.05117506423837901 | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[5].widget.wrong[1].value` | 0.0625 | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[5].widget.wrong[2].value` | 0.25 | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[5].feedback.correct` | $\tfrac{\binom{18}{3}}{\binom{20}{5}} = \tfrac{816}{15504} = \tfrac{1}{19}$. | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[5].feedback.generic` | Not quite right. Count the samples that hold both days, then divide by all samples. | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[5].feedback.byKey.replaced` | You used draws with replacement and treated the two days as independent. The sample has 5 dif... | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[5].feedback.byKey.independent` | That is $\tfrac{1}{4} \times \tfrac{1}{4}$. Once the best day is in, only 4 of the other 19 d... | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[5].feedback.byKey.one-day` | That is the chance for one of the two days. Both must be in the sample. | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[5].explain.text` | Fix both days in the sample and choose the other 3 from 18: $\binom{18}{3} = 816$. All sample... | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[6].prose` | Prove Pascal's rule, $\binom{n}{k} = \binom{n-1}{k-1} + \binom{n-1}{k}$, for $1 \le k \le n -... | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[6].question` | Put the lines of the proof in order. | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[6].widget.lines[0].text` | Fix one of the $n$ items and call it $x$; $\binom{n}{k}$ counts all groups of $k$ | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[6].widget.lines[1].text` | Groups containing $x$ need $k - 1$ more from the other $n - 1$: $\binom{n-1}{k-1}$ of them | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[6].widget.lines[2].text` | The remaining groups avoid $x$, so all $k$ come from the other $n - 1$: $\binom{n-1}{k}$ | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[6].widget.lines[3].text` | Every group falls in exactly one of these two lists, so the lists add up to all groups | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[6].widget.lines[4].text` | Therefore $\binom{n}{k} = \binom{n-1}{k-1} + \binom{n-1}{k}$ | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[6].widget.answer` | ["fix", "with", "without", "split", "done"] | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[6].feedback.correct` | Split the groups by whether they contain $x$, then add. | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[6].feedback.generic` | Not quite right. Fix an item, count the two kinds of group, check they do not overlap, then add. | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[6].feedback.byKey.without` | The groups that avoid $x$ are "the remaining" ones, so they come after the groups containing ... | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[6].feedback.byKey.split` | The two lists must be counted before you can say they cover everything once. | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[6].explain.text` | Every group of $k$ either contains $x$ or not, never both. With $x$ we choose $k - 1$ more fr... | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[7].prompt` | A strategy has 20 daily returns, one of them the worst day of the year. (a) A bootstrap resam... | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[7].model` | **(a) Bootstrap resamples.** Each of the 20 draws can be any of the 20 days, since the drawn ... | imprecise | finding 4: part (d) repeats 'the chance never changes, so independent'; the rest of the model is correct by enumeration (L2 script) |
| homework-2 | `items[7].rubric[0].text` | (a) Uses the multiplication rule with replacement: $20^{20}$ | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[7].rubric[1].text` | (b) Uses an unordered choice: $\binom{20}{10} = 184{,}756$ | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[7].rubric[2].text` | (c) Bootstrap: multiplies 20 independent misses, $(\tfrac{19}{20})^{20} \approx 0.358$ | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[7].rubric[3].text` | (c) Split: $\binom{19}{10} / \binom{20}{10} = \tfrac{1}{2}$, with a counting or symmetry argu... | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[7].rubric[4].text` | (d) Says bootstrap draws are independent and split draws dependent. Links this to resamples t... | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[8].prose` | Each process below makes two draws. | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[8].question` | In which are the two draws independent? Select all that apply. | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[8].widget.options[0].text` | Rolling a fair die twice | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[8].widget.options[0].correct` | true | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[8].widget.options[1].text` | Dealing two cards from one deck | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[8].widget.options[1].why` | The first card leaves the deck, so the second draw's chances change. | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[8].widget.options[2].text` | Two draws of a bootstrap resample | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[8].widget.options[2].correct` | true | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[8].widget.options[3].text` | Picking two different analysts for a committee | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[8].widget.options[3].why` | The first analyst cannot be picked again, so the second pick depends on the first. | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[8].feedback.correct` | Independent draws see the same set of outcomes every time. | imprecise | finding 3: the same set of outcomes each time is neither needed nor enough for independence (die then coin; second card of a deal has the same 52 possible cards) |
| homework-2 | `items[8].feedback.generic` | Not quite right. Ask whether the first draw changes what the second can be. | correct | Ross 1.2 to 1.6, 2.5, 3.4; enumerated, L2 script |
| homework-2 | `items[8].explain.text` | A die and a bootstrap both restore everything before the next draw, so the chances never chan... | imprecise | finding 3: as above; the criterion is that no result changes the chances of the next draw |

## problems-2.json

| file | JSON path | claim (short) | verdict | basis |
|---|---|---|---|---|
| problems-2 | `items[0].prose` | A running club has 9 sprinters. It picks a relay team of 4 and then a running order for the 4... | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[0].parts[0].question` | How many different teams of 4, ignoring the running order, can the club pick? | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[0].parts[0].widget.answer` | 126 | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[0].parts[0].widget.accept` | 126 exactly: $\binom{9}{4}$. | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[0].parts[0].widget.wrong[0].value` | 3024 | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[0].parts[0].widget.wrong[1].value` | 36 | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[0].parts[0].feedback.correct` | $\binom{9}{4} = \tfrac{9 \times 8 \times 7 \times 6}{4!} = \tfrac{3024}{24} = 126$. | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[0].parts[0].feedback.generic` | Not quite. Swapping two sprinters gives the same team. | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[0].parts[0].feedback.byKey.ordered` | That counts ordered picks, $9 \times 8 \times 7 \times 6$. A team is the same 4 sprinters wha... | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[0].parts[0].feedback.byKey.times` | You multiplied 9 by 4. Count the ordered picks, then divide by the $4!$ orders of each team. | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[0].parts[0].explain.text` | There are $9 \times 8 \times 7 \times 6 = 3024$ ordered picks. Each team appears once per ord... | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[0].parts[1].question` | Using the 126 teams, how many line-ups are there: a team together with its running order? | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[0].parts[1].widget.answer` | 3024 | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[0].parts[1].widget.accept` | 3024 exactly: $126 \times 4!$. | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[0].parts[1].widget.wrong[0].value` | 504 | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[0].parts[1].widget.wrong[1].value` | 150 | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[0].parts[1].feedback.correct` | $126 \times 24 = 3024$, the same as $9 \times 8 \times 7 \times 6$. | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[0].parts[1].feedback.generic` | Not quite. Each team can run in $4!$ orders. | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[0].parts[1].feedback.byKey.times-four` | You multiplied by 4. A team of 4 can run in $4! = 24$ orders. | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[0].parts[1].feedback.byKey.added` | You added the 24 orders. Each team pairs with each of its orders, so multiply. | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[0].parts[1].explain.text` | Each of the 126 teams runs in $4! = 24$ orders, so there are $126 \times 24 = 3024$ line-ups.... | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[0].parts[2].question` | Using the 126 teams, what is the chance that both Ada and Bea are in the team? Give an exact ... | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[0].parts[2].widget.answer` | 0.166667 | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[0].parts[2].widget.accept` | Any form equal to $\tfrac{21}{126} = \tfrac{1}{6}$, or 0.1667. | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[0].parts[2].widget.wrong[0].value` | 0.444444 | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[0].parts[2].widget.wrong[1].value` | 0.197531 | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[0].parts[2].feedback.correct` | Teams with both fill the other 2 places from 7: $\binom{7}{2} = 21$, and $\tfrac{21}{126} = \... | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[0].parts[2].feedback.generic` | Not quite. Put Ada and Bea in, then count the ways to fill the other places. | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[0].parts[2].feedback.byKey.one-named` | That is $\tfrac{4}{9}$, the chance one named sprinter is in. Both must be in. | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[0].parts[2].feedback.byKey.squared` | That is $\left(\tfrac{4}{9}\right)^2$, which treats the two picks as independent. Once Ada is... | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[0].parts[2].explain.text` | With Ada and Bea in, the other 2 places come from the other 7 sprinters: $\binom{7}{2} = 21$ ... | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[0].parts[3].question` | Using $P(\text{both in}) = \tfrac{1}{6}$, what is the chance that Ada and Bea run the last tw... | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[0].parts[3].widget.answer` | 0.027778 | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[0].parts[3].widget.accept` | Any form equal to $\tfrac{84}{3024} = \tfrac{1}{36}$, or 0.0278. | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[0].parts[3].widget.wrong[0].value` | 0.013889 | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[0].parts[3].widget.wrong[1].value` | 0.166667 | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[0].parts[3].widget.wrong[2].value` | 0.032922 | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[0].parts[3].feedback.correct` | Given both are in, they take legs 3 and 4 in $2 \times 2$ of the 24 orders: $\tfrac{1}{6} \ti... | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[0].parts[3].feedback.generic` | Not quite. Take a team holding both. Count its orders with Ada and Bea on legs 3 and 4. | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[0].parts[3].feedback.byKey.one-order` | That is $\tfrac{1}{72}$, with Bea on the last leg only. Either order counts, so double it. | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[0].parts[3].feedback.byKey.in-team` | That is the chance both are in the team. They must also take legs 3 and 4. | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[0].parts[3].feedback.byKey.from-squared` | That is $\left(\tfrac{4}{9}\right)^2 \times \tfrac{1}{6}$, from the independent picks of part... | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[0].parts[3].explain.text` | In a team holding both, Ada and Bea take legs 3 and 4 in 2 ways. The others take legs 1 and 2... | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[1].prose` | A batch holds 15 orders, and 4 of them breach a risk limit. A checker picks 3 different order... | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[1].parts[0].question` | What is the chance that the first order picked does not breach? Give an exact fraction, or a ... | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[1].parts[0].widget.answer` | 0.733333 | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[1].parts[0].widget.accept` | Any form equal to $\tfrac{11}{15}$, or 0.7333. | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[1].parts[0].widget.wrong[0].value` | 0.266667 | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[1].parts[0].feedback.correct` | 11 of the 15 orders are clean: $\tfrac{11}{15}$. | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[1].parts[0].feedback.generic` | Not quite. Count the orders that do not breach. | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[1].parts[0].feedback.byKey.breach` | That is $\tfrac{4}{15}$, the chance it does breach. | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[1].parts[0].explain.text` | Of 15 orders, $15 - 4 = 11$ are clean. The first pick is equally likely to be any order, so t... | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[1].parts[1].question` | Using $\tfrac{11}{15}$ for the first pick, what is the chance that the first two orders are b... | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[1].parts[1].widget.answer` | 0.52381 | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[1].parts[1].widget.accept` | Any form equal to $\tfrac{11}{15} \times \tfrac{10}{14} = \tfrac{11}{21}$, or 0.5238. | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[1].parts[1].widget.wrong[0].value` | 0.537778 | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[1].parts[1].widget.wrong[1].value` | 0.488889 | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[1].parts[1].widget.wrong[2].value` | 0.57619 | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[1].parts[1].feedback.correct` | $\tfrac{11}{15} \times \tfrac{10}{14} = \tfrac{110}{210} = \tfrac{11}{21}$. | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[1].parts[1].feedback.generic` | Not quite. After a clean first pick, how many orders and how many clean ones are left? | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[1].parts[1].feedback.byKey.replace` | That is $\left(\tfrac{11}{15}\right)^2$, as if the first order went back. It stays out, so 14... | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[1].parts[1].feedback.byKey.fixed-bottom` | You took one clean order off the top but kept 15 on the bottom. The batch has 14 left. | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[1].parts[1].feedback.byKey.fixed-top` | You took one order off the bottom but kept 11 clean on the top. Only 10 clean ones are left. | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[1].parts[1].explain.text` | After a clean first pick, 14 orders are left and 10 of them are clean. Multiply along the bra... | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[1].parts[2].question` | Using $\tfrac{11}{21}$ for the first two, what is the chance that all three orders are clean?... | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[1].parts[2].widget.answer` | 0.362637 | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[1].parts[2].widget.accept` | Any form equal to $\tfrac{11}{21} \times \tfrac{9}{13} = \tfrac{33}{91}$, or 0.3626. | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[1].parts[2].widget.wrong[0].value` | 0.39437 | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[1].parts[2].widget.wrong[1].value` | 0.293333 | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[1].parts[2].feedback.correct` | $\tfrac{11}{21} \times \tfrac{9}{13} = \tfrac{99}{273} = \tfrac{33}{91}$. | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[1].parts[2].feedback.generic` | Not quite. After two clean picks, 13 orders are left and 9 of them are clean. | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[1].parts[2].feedback.byKey.replace` | That is $\left(\tfrac{11}{15}\right)^3$, drawing with replacement. Each pick leaves one order... | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[1].parts[2].feedback.byKey.fixed-bottom` | That is $\tfrac{11 \times 10 \times 9}{15^3}$, with 15 kept on the bottom. The batch shrinks ... | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[1].parts[2].explain.text` | After two clean picks, 13 orders are left, 9 of them clean. So the chance is $\tfrac{11}{21} ... | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[1].parts[3].question` | Using $P(\text{all clean}) = \tfrac{33}{91}$, what is the chance the checker finds at least o... | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[1].parts[3].widget.answer` | 0.637363 | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[1].parts[3].widget.accept` | Any form equal to $\tfrac{58}{91}$, or 0.6374. | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[1].parts[3].widget.wrong[0].value` | 0.362637 | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[1].parts[3].widget.wrong[1].value` | 0.60563 | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[1].parts[3].widget.wrong[2].value` | 0.8 | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[1].parts[3].feedback.correct` | $1 - \tfrac{33}{91} = \tfrac{58}{91} \approx 0.6374$. | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[1].parts[3].feedback.generic` | Not quite. “At least one breach” is the complement of “all clean”. | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[1].parts[3].feedback.byKey.none` | That is the chance of no breach. Take it from 1. | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[1].parts[3].feedback.byKey.replace` | That is $1 - \left(\tfrac{11}{15}\right)^3$, with replacement. Without replacement the chance... | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[1].parts[3].feedback.byKey.adding` | That is $3 \times \tfrac{4}{15}$, which adds a chance per pick. Samples with two breaches are... | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[1].parts[3].explain.text` | “At least one breach” is the complement of “all three clean”. So the chance is $1 - \tfrac{33... | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[1].parts[4].question` | The checker may keep picking, still without replacement. Three clean picks have chance $\tfra... | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[1].parts[4].widget.answer` | 6 | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[1].parts[4].widget.accept` | 6 exactly: $1 - \tfrac{\binom{11}{6}}{\binom{15}{6}} = 1 - \tfrac{462}{5005} \approx 0.9077$. | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[1].parts[4].widget.wrong[0].value` | 5 | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[1].parts[4].widget.wrong[1].value` | 4 | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[1].parts[4].widget.wrong[2].value` | 8 | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[1].parts[4].feedback.correct` | Each pick multiplies by the clean orders left over the orders left. The breach chance is 0.75... | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[1].parts[4].feedback.generic` | Not quite. Multiply $\tfrac{33}{91}$ by $\tfrac{8}{12}$, then $\tfrac{7}{11}$, and so on, and... | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[1].parts[4].feedback.byKey.five` | At 5 picks the chance of at least one breach is 0.8462, still under 0.9. | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[1].parts[4].feedback.byKey.adding` | That solves $\tfrac{4n}{15} > 0.9$, which adds a chance per pick. At 4 picks the true chance ... | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[1].parts[4].feedback.byKey.replace` | That is the answer if each order went back after the pick. Without replacement the clean orde... | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[1].parts[4].explain.text` | After the three picks, each further pick multiplies the all-clean chance by $\tfrac{8}{12}$, ... | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[2].prose` | Eight members of a pricing committee each cast one vote for one of three proposals, X, Y and ... | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[2].parts[0].question` | How many different tallies are possible? | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[2].parts[0].widget.answer` | 45 | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[2].parts[0].widget.accept` | 45 exactly: $\binom{10}{2}$, 8 stars and 2 bars. | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[2].parts[0].widget.wrong[0].value` | 6561 | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[2].parts[0].widget.wrong[1].value` | 21 | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[2].parts[0].widget.wrong[2].value` | 28 | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[2].parts[0].feedback.correct` | A tally is a row of 8 votes and 2 bars: $\binom{10}{2} = 45$. | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[2].parts[0].feedback.generic` | Not quite. Code a tally as 8 stars and 2 bars. | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[2].parts[0].feedback.byKey.distinct` | That is $3^8$, which lists who voted for what. The tally keeps only the counts, so the votes ... | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[2].parts[0].feedback.byKey.at-least-one` | That is $\binom{7}{2}$, with every proposal getting a vote. A proposal may get none. | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[2].parts[0].feedback.byKey.stars-only` | You put the 2 bars among 8 places. The row has $8 + 2 = 10$ places. | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[2].parts[0].explain.text` | A tally shares 8 identical votes among 3 proposals. That is a row of 8 stars and 2 bars, so t... | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[2].parts[1].question` | Using the 45 tallies, how many leave at least one proposal with no votes? | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[2].parts[1].widget.answer` | 24 | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[2].parts[1].widget.accept` | 24 exactly: $45 - \binom{7}{2}$. | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[2].parts[1].widget.wrong[0].value` | 21 | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[2].parts[1].widget.wrong[1].value` | 3 | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[2].parts[1].feedback.correct` | Every proposal gets a vote in $\binom{7}{2} = 21$ tallies, so $45 - 21 = 24$ leave one empty. | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[2].parts[1].feedback.generic` | Not quite. Count the tallies where every proposal gets a vote, then use the complement. | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[2].parts[1].feedback.byKey.all-voted` | That is $\binom{7}{2}$, the tallies where every proposal gets a vote. Take it from 45. | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[2].parts[1].feedback.byKey.unanimous` | Those are the tallies with two empty proposals. Tallies such as 5, 3, 0 have one empty proposal. | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[2].parts[1].explain.text` | With at least one vote each, the 2 bars go in the 7 gaps between the votes: $\binom{7}{2} = 2... | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[2].parts[2].question` | Each member now votes independently, choosing each proposal with chance $\tfrac{1}{3}$. Are t... | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[2].parts[2].widget.options[0].text` | No. The tally 3, 3, 2 comes from many lists of votes; 8, 0, 0 comes from only one. | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[2].parts[2].widget.options[0].correct` | true | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[2].parts[2].widget.options[1].text` | Yes. Each tally has chance $\tfrac{1}{45}$ because the proposals are alike. | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[2].parts[2].widget.options[1].why` | You gave every tally the same chance. The equally likely outcomes are the $3^8$ lists of vote... | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[2].parts[2].widget.options[2].text` | Yes. The votes are identical, so each sharing is one outcome. | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[2].parts[2].widget.options[2].why` | Identical votes make tallies the right thing to count, not equally likely things to count. Me... | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[2].parts[2].widget.options[3].text` | No. The tally 8, 0, 0 is the most likely, since members agree. | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[2].parts[2].widget.options[3].why` | You assumed the members agree. Each votes independently, so a split tally holds far more vote... | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[2].parts[2].feedback.correct` | The equally likely outcomes are the $3^8$ lists of who voted for what. A tally such as 3, 3, ... | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[2].parts[2].feedback.generic` | Not quite. Ask how many lists of votes give each tally. | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[2].parts[2].explain.text` | Each member has 3 equally likely choices, so the $3^8 = 6561$ vote lists are the equally like... | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[2].parts[3].question` | Using the $3^8 = 6561$ equally likely vote lists, what is the chance the vote is unanimous, a... | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[2].parts[3].widget.answer` | 0.000457247 | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[2].parts[3].widget.accept` | Any form equal to $\tfrac{3}{6561} = \tfrac{1}{2187}$, or 0.000457. | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[2].parts[3].widget.wrong[0].value` | 0.066667 | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[2].parts[3].widget.wrong[1].value` | 0.000152416 | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[2].parts[3].feedback.correct` | Three vote lists are unanimous, one for each proposal: $\tfrac{3}{6561} = \tfrac{1}{2187}$. | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[2].parts[3].feedback.generic` | Not quite. Count the vote lists in which all 8 votes match. | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[2].parts[3].feedback.byKey.tallies` | That is $\tfrac{3}{45}$, treating the 45 tallies as equally likely. Part 3 showed they are not. | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[2].parts[3].feedback.byKey.one-proposal` | That is $\tfrac{1}{6561}$, all 8 for X only. Y and Z can be unanimous too. | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[2].parts[3].explain.text` | A unanimous vote is all X, all Y or all Z: 3 of the 6561 lists. So the chance is $\tfrac{3}{6... | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[3].prose` | A data vendor runs 30 feeds. Each quarter an audit picks 5 different feeds at random, every s... | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[3].parts[0].question` | How many different sets of 5 feeds can the audit pick? | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[3].parts[0].widget.answer` | 142506 | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[3].parts[0].widget.accept` | 142,506 exactly: $\binom{30}{5}$. | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[3].parts[0].widget.wrong[0].value` | 17100720 | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[3].parts[0].widget.wrong[1].value` | 24300000 | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[3].parts[0].feedback.correct` | $\binom{30}{5} = \tfrac{17{,}100{,}720}{120} = 142{,}506$. | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[3].parts[0].feedback.generic` | Not quite. Count ordered picks without repeats, then divide by the orders of a set. | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[3].parts[0].feedback.byKey.ordered` | That is $30 \times 29 \times 28 \times 27 \times 26$, ordered picks. Divide by the $5!$ order... | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[3].parts[0].feedback.byKey.power` | That is $30^5$, picks with repeats in order. The audit picks 5 different feeds, as a set. | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[3].parts[0].explain.text` | There are $30 \times 29 \times 28 \times 27 \times 26 = 17{,}100{,}720$ ordered picks. Each s... | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[3].parts[1].question` | Using the 142,506 sets, what is the chance that exactly 3 of the audited feeds are your team'... | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[3].parts[1].widget.answer` | 0.021052 | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[3].parts[1].widget.accept` | 0.02105: $\tfrac{\binom{5}{3}\binom{25}{2}}{142{,}506} = \tfrac{3000}{142{,}506}$. | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[3].parts[1].widget.wrong[0].value` | 7.02e-05 | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[3].parts[1].widget.wrong[1].value` | 0.042103 | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[3].parts[1].feedback.correct` | $\binom{5}{3} = 10$ ways for your 3 and $\binom{25}{2} = 300$ for the other 2: $\tfrac{3000}{... | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[3].parts[1].feedback.generic` | Not quite. Choose 3 of your 5 feeds, then 2 of the other 25, and multiply. | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[3].parts[1].feedback.byKey.no-others` | That is $\tfrac{10}{142{,}506}$, which picks your 3 feeds but not the other 2. Multiply by $\... | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[3].parts[1].feedback.byKey.others-ordered` | You picked the other 2 feeds in order, $25 \times 24$. They form a set, so halve it: 300. | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[3].parts[1].explain.text` | In stages: choose 3 of your 5 feeds, $\binom{5}{3} = 10$, then 2 of the other 25, $\binom{25}... | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[3].parts[2].question` | Using the 3000 sets with exactly 3, find the chance that at least 3 audited feeds are yours. ... | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[3].parts[2].widget.answer` | 0.021936 | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[3].parts[2].widget.accept` | 0.02194: $\tfrac{3000 + 125 + 1}{142{,}506} = \tfrac{3126}{142{,}506}$. | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[3].parts[2].widget.wrong[0].value` | 0.021052 | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[3].parts[2].widget.wrong[1].value` | 0.022813 | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[3].parts[2].feedback.correct` | With 4 of yours: $\binom{5}{4}\binom{25}{1} = 125$; with 5: 1. So $\tfrac{3126}{142{,}506} \a... | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[3].parts[2].feedback.generic` | Not quite. “At least 3” is exactly 3, 4 or 5 of your feeds. | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[3].parts[2].feedback.byKey.exactly` | That is the chance of exactly 3. Add the sets with 4 and with 5 of yours. | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[3].parts[2].feedback.byKey.double-four` | You counted the 4-feed sets as $\binom{5}{4} \times \binom{25}{1} \times 2 = 250$. There are ... | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[3].parts[2].explain.text` | Exactly 4 of yours gives $\binom{5}{4}\binom{25}{1} = 125$ sets and exactly 5 gives 1. These ... | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[3].parts[3].question` | Let $p \approx 0.021936$ be the chance of at least 3 of yours in a quarter, from part 3. Find... | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[3].parts[3].widget.answer` | 0.084899 | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[3].parts[3].widget.accept` | 0.0849: $1 - (1 - 0.021936)^4 = 0.08490$. | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[3].parts[3].widget.wrong[0].value` | 0.087744 | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[3].parts[3].widget.wrong[1].value` | 0.081585 | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[3].parts[3].widget.wrong[2].value` | 0.915101 | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[3].parts[3].feedback.correct` | $1 - (1 - 0.021936)^4 = 1 - 0.91510 = 0.0849$. | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[3].parts[3].feedback.generic` | Not quite. Find the chance it happens in no quarter, then take it from 1. | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[3].parts[3].feedback.byKey.adding` | That is $4 \times 0.021936$, which adds a chance per quarter. Runs with two such quarters are... | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[3].parts[3].feedback.byKey.from-exactly` | That is $1 - (1 - 0.021052)^4$, from the exactly 3 chance. Use the at least 3 chance from par... | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[3].parts[3].feedback.byKey.none` | That is $(1 - 0.021936)^4$, the chance it never happens. Take it from 1. | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |
| problems-2 | `items[3].parts[3].explain.text` | The quarters are independent, so it happens in none with chance $(1 - 0.021936)^4 \approx 0.9... | correct | Ross 1.4, 1.6, 2.5 (hypergeometric counts); enumerated, L2 script, 6,561 vote lists enumerated |

## l9-double-counting.json

| file | JSON path | claim (short) | verdict | basis |
|---|---|---|---|---|
| l9 | `screens[0].prose` | This builds on Events as sets, where you met unions and overlaps. Draw one card from a standa... | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[0].canvas.state.caption` | 13 hearts, 12 face cards | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[0].question` | A friend says $13 + 12 = 25$ cards are a heart or a face card. Tap the region the friend coun... | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[0].widget.answer` | ["AB"] | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[0].hints[0].text` | Which cards are in the 13 and also in the 12? | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[0].hints[1].text` | The middle region holds cards that belong to both circles. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[0].hints[2].text` | The jack, queen and king of hearts are hearts and face cards. Both counts include them. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[0].feedback.correct` | The jack, queen and king of hearts sit in both counts. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[0].feedback.generic` | Not quite right. Find the cards that are in the 13 hearts and also in the 12 face cards. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[0].feedback.byKey.A` | Those 10 hearts are not face cards. They are in the 13 only, so they were counted once. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[0].feedback.byKey.B` | Those 9 face cards are not hearts. They are in the 12 only, so they were counted once. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[0].feedback.byKey.none` | Those 30 cards are in neither count. The friend left them out, and rightly so. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[0].explain.text` | The 13 hearts include the 3 heart face cards, and so do the 12 face cards. Adding 13 and 12 c... | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[0].explain.canvas.caption` | 3 cards counted twice | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[1].prose` | Now build the event “a heart or a face card” yourself. A card counts if it is a heart, a face... | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[1].canvas.state.caption` | Tap a region to select it, tap again to clear it | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[1].question` | Tap every region whose cards are a heart or a face card. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[1].widget.answer` | ["A", "AB", "B"] | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[1].widget.wrong[0].set` | ["AB"] | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[1].widget.wrong[1].set` | ["A", "AB", "B", "none"] | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[1].hints[0].text` | Does a heart that is not a face card count? | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[1].hints[1].text` | Three regions sit inside at least one circle. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[1].hints[2].text` | Take the hearts only, the overlap and the face cards only. Leave the outside alone. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[1].feedback.correct` | Three regions: 10, 3 and 9 cards, each card counted once. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[1].feedback.generic` | Not quite right. Take every card inside at least one circle. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[1].feedback.byKey.and-only` | You took only the cards that are both. “Or” also takes cards that are just one of the two. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[1].feedback.byKey.everything` | The 30 cards outside both circles are neither a heart nor a face card. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[1].feedback.byKey.none` | The 30 cards outside both circles are neither a heart nor a face card. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[1].feedback.byKey.A` | The 10 hearts that are not face cards still count. A heart is enough. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[1].feedback.byKey.B` | The 9 face cards that are not hearts still count. A face card is enough. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[1].feedback.byKey.AB` | The 3 heart face cards count too. “Or” includes both. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[1].explain.text` | Your three regions hold $10 + 3 + 9 = 22$ cards. Each card is counted once, because the regio... | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[1].explain.canvas.caption` | Heart or face card: 22 cards | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[2].prose` | As in Events as sets, your regions form the union $H \cup F$. The overlap is the intersection... | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[2].canvas.state.caption` | $/H \cup F/ = 13 + 12 - 3 = 22$ | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[2].question` | What is $P(H \cup F)$, the chance one card drawn is a heart or a face card? | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[2].widget.answer` | 0.4231 | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[2].widget.accept` | Any form equal to $\tfrac{22}{52} = \tfrac{11}{26}$, or $0.4231 \pm 0.0005$ | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[2].widget.wrong[0].value` | 0.4808 | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[2].widget.wrong[1].value` | 0.3654 | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[2].widget.wrong[2].value` | 0.0577 | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[2].widget.wrong[3].value` | 22 | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[2].hints[0].text` | How many of the 52 cards are in the union? | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[2].hints[1].text` | You counted them on the last screen. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[2].hints[2].text` | 22 of the 52 equally likely cards are a heart or a face card. Divide 22 by 52. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[2].feedback.correct` | 22 of the 52 cards, so $\tfrac{11}{26}$. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[2].feedback.generic` | Not quite right. Count the cards in the union once each, then divide by 52. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[2].feedback.byKey.added` | You used 25 cards: $13 + 12$. The 3 heart face cards were counted twice. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[2].feedback.byKey.twice` | You took the 3 shared cards away twice, leaving 19. Take them away once. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[2].feedback.byKey.both` | That is the intersection, cards that are both. The union also has cards that are only one. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[2].feedback.byKey.count` | 22 is the number of cards. The chance is that count out of 52. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[2].explain.text` | We counted $13 + 12 - 3 = 22$ cards, so $P(H \cup F) = \tfrac{22}{52} = \tfrac{11}{26} \appro... | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[3].prose` | Now chances instead of counts. Roll two fair dice. $A$ is “the first die shows 6” and $B$ is ... | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[3].canvas.state.caption` | Only the overlap is filled in | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[3].question` | What is $P(A \cup B)$, the chance of at least one six? | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[3].widget.answer` | 0.3056 | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[3].widget.accept` | Any form equal to $\tfrac{11}{36}$, or $0.3056 \pm 0.0005$ | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[3].widget.wrong[0].value` | 0.3333 | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[3].widget.wrong[1].value` | 0.2778 | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[3].widget.wrong[2].value` | 0.0278 | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[3].hints[0].text` | Which roll is in both $A$ and $B$? | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[3].hints[1].text` | The double six is in both events. Its chance is $\tfrac{1}{36}$. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[3].hints[2].text` | Add $\tfrac{1}{6} + \tfrac{1}{6}$, then take away $\tfrac{1}{36}$ once for the double six. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[3].feedback.correct` | $\tfrac{6}{36} + \tfrac{6}{36} - \tfrac{1}{36} = \tfrac{11}{36}$. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[3].feedback.generic` | Not quite right. Add the two chances, then take the overlap away once. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[3].feedback.byKey.added` | You added $\tfrac{1}{6} + \tfrac{1}{6}$. The double six is in both, so it was counted twice. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[3].feedback.byKey.twice` | You took $\tfrac{1}{36}$ away twice, so the double six is not counted at all. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[3].feedback.byKey.both` | That is the chance of a double six, the intersection. You want at least one six. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[3].explain.text` | You added $\tfrac{6}{36} + \tfrac{6}{36}$ and removed the double six once: $\tfrac{11}{36}$. ... | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[4].prose` | Back to one card. This time $H$ is “a heart” and $S$ is “a spade”. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[4].canvas.state.caption` | No card is in the overlap | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[4].question` | What is $P(H \cup S)$? | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[4].widget.options[0].text` | $\dfrac{1}{2}$ | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[4].widget.options[0].correct` | true | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[4].widget.options[1].text` | $\dfrac{25}{52}$ | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[4].widget.options[1].why` | You took $\tfrac{1}{52}$ away for an overlap. No card is a heart and a spade, so nothing was ... | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[4].widget.options[2].text` | $\dfrac{1}{16}$ | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[4].widget.options[2].why` | You multiplied the two chances. That would be a chance of both, and one card cannot be both. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[4].widget.options[3].text` | $\dfrac{1}{4}$ | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[4].widget.options[3].why` | That is the chance of a heart alone. A spade also counts. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[4].hints[0].text` | How many cards are both a heart and a spade? | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[4].hints[1].text` | The overlap holds 0 cards. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[4].hints[2].text` | With nothing counted twice, add: $\tfrac{13}{52} + \tfrac{13}{52}$. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[4].feedback.correct` | 26 of 52 cards: the overlap is empty. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[4].feedback.generic` | Not quite right. Count the cards in the overlap first. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[4].feedback.byKey.ghost` | You took $\tfrac{1}{52}$ away for an overlap. No card is a heart and a spade, so nothing was ... | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[4].explain.text` | No card is both a heart and a spade, so $P(H \cap S) = 0$. Events like these are **disjoint**... | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[5].prose` | Roll a fair die. $A$ is “at most 4”, so $P(A) = \tfrac{4}{6}$. $B$ is “even”, so $P(B) = \tfr... | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[5].canvas.state.caption` | Each face has chance $\tfrac{1}{6}$ | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[5].question` | What is $P(A \cup B)$? | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[5].widget.options[0].text` | $\dfrac{7}{6}$ | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[5].widget.options[0].why` | You added the two chances and got more than 1. That is the giveaway: 2 and 4 were counted twice. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[5].widget.options[1].text` | $\dfrac{5}{6}$ | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[5].widget.options[1].correct` | true | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[5].widget.options[2].text` | $1$ | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[5].widget.options[2].why` | You capped the sum at 1. The face 5 is in neither event, so the union misses it. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[5].widget.options[3].text` | $\dfrac{3}{6}$ | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[5].widget.options[3].why` | You took the overlap away twice. Take $\tfrac{2}{6}$ away once. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[5].hints[0].text` | Can any chance be bigger than 1? | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[5].hints[1].text` | Faces 2 and 4 are in both events. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[5].hints[2].text` | $\tfrac{4}{6} + \tfrac{3}{6} - \tfrac{2}{6}$. Or count the faces inside the circles. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[5].feedback.correct` | Five faces, 1, 2, 3, 4 and 6, are in the union. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[5].feedback.generic` | Not quite right. Add the chances, then take the overlap away once. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[5].feedback.byKey.added` | You added the two chances and got more than 1. That is the giveaway: 2 and 4 were counted twice. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[5].feedback.byKey.capped` | You capped the sum at 1. The face 5 is in neither event, so the union misses it. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[5].explain.text` | Adding gives $\tfrac{7}{6}$, which no chance can be. The faces 2 and 4 sit in both events, so... | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[6].prose` | With three events we add the singles $/A/ + /B/ + /C/$, subtract the three pair overlaps, the... | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[6].canvas.state.caption` | One card in $A$ and $B$ only; one card in all three | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[6].question` | Fill in how many times a card in each region is counted. Net is singles minus pairs plus triple. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[6].widget.rows[0]` | ["$A$ only", "1", "0", "0", "1"] | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[6].widget.rows[1][0]` | $A \cap B$ only | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[6].widget.rows[1][1]` | 2 | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[6].widget.rows[1][2].edit` | true | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[6].widget.rows[1][2].answer` | 1 | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[6].widget.rows[1][3]` | 0 | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[6].widget.rows[1][4].edit` | true | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[6].widget.rows[1][4].answer` | 1 | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[6].widget.rows[2][0]` | all three | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[6].widget.rows[2][1].edit` | true | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[6].widget.rows[2][1].answer` | 3 | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[6].widget.rows[2][2].edit` | true | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[6].widget.rows[2][2].answer` | 3 | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[6].widget.rows[2][3].edit` | true | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[6].widget.rows[2][3].answer` | 1 | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[6].widget.rows[2][4].edit` | true | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[6].widget.rows[2][4].answer` | 1 | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[6].hints[0].text` | A card in all three circles is in $A$, in $B$ and in $C$. How many of the three counts includ... | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[6].hints[1].text` | A card in all three is in every pair overlap: $A \cap B$, $A \cap C$ and $B \cap C$. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[6].hints[2].text` | All three: counted 3 times, subtracted 3 times, added back once, net 1. $A$ and $B$ only: 2, ... | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[6].feedback.correct` | Every card in the union ends up counted exactly once. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[6].feedback.generic` | Not quite right. For each card, count how many of the terms contain it. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[6].feedback.byKey.r1c2` | A card in $A$ and $B$ but not $C$ is in one pair overlap, $A \cap B$, only. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[6].feedback.byKey.r1c4` | Net is $2 - 1 + 0$. Check the pair column first. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[6].feedback.byKey.r2c1` | A card in all three is in $A$, in $B$ and in $C$: three counts. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[6].feedback.byKey.r2c2` | A card in all three is in all three pair overlaps, so it is subtracted 3 times. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[6].feedback.byKey.r2c3` | The triple term counts the cards in $A \cap B \cap C$ once. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[6].feedback.byKey.r2c4` | Net is $3 - 3 + 1$. Without the triple term the card would vanish. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[6].explain.text` | Each row nets to 1, so every card in the union is counted once. The triple region is the deli... | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[6].explain.canvas.caption` | Every region nets to 1 | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[7].prose` | Your counts give the rule of **inclusion and exclusion**. Add the singles, subtract the pairs... | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[7].canvas.state.caption` | A stock screen with three filters | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[7].question` | Of 100 stocks, 40 pass momentum, 35 value and 30 quality. The pairs pass together 12, 10 and ... | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[7].widget.answer` | 80 | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[7].widget.accept` | 80 exactly: $40 + 35 + 30 - 12 - 10 - 8 + 5$ | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[7].widget.wrong[0].value` | 105 | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[7].widget.wrong[1].value` | 75 | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[7].widget.wrong[2].value` | 70 | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[7].hints[0].text` | Start with $40 + 35 + 30$. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[7].hints[1].text` | Subtract the three pair counts, then add the triple once. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[7].hints[2].text` | $105 - 30 + 5 = 80$. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[7].feedback.correct` | $105 - 30 + 5 = 80$ stocks. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[7].feedback.generic` | Not quite right. Add the singles, subtract the pairs, add the triple. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[7].feedback.byKey.added` | You added the three filters. Stocks passing two or three filters were counted more than once. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[7].feedback.byKey.no-triple` | You stopped after the pairs. The 5 stocks passing all three were then removed completely; add... | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[7].feedback.byKey.minus-triple` | You subtracted the triple. The signs alternate: the triple is added back. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[7].explain.text` | $40 + 35 + 30 - 12 - 10 - 8 + 5 = 80$. The diagram now shows each region; they add to 80 insi... | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[8].prose` | A trend signal looks at a stock's close against two moving averages. Over its history the clo... | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[8].canvas.state.caption` | Overlap: both on 45% of days | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[8].question` | On a random day, what is the chance the close is above at least one of the two averages? | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[8].widget.answer` | 0.65 | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[8].widget.accept` | 0.65, or 65% | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[8].widget.wrong[0].value` | 1.1 | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[8].widget.wrong[1].value` | 0.2 | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[8].widget.wrong[2].value` | 0.45 | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[8].widget.wrong[3].value` | 0.35 | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[8].hints[0].text` | What happens if you simply add 0.6 and 0.5? | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[8].hints[1].text` | The 45% of days above both averages are in both numbers. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[8].hints[2].text` | $0.6 + 0.5 - 0.45$. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[8].feedback.correct` | $0.6 + 0.5 - 0.45 = 0.65$. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[8].feedback.generic` | Not quite right. Add the two chances, then take away the days above both once. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[8].feedback.byKey.added` | You added 0.6 and 0.5 and got more than 1. The days above both averages were counted twice. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[8].feedback.byKey.one-only` | That is the chance of being above exactly one average. Days above both also count. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[8].feedback.byKey.both` | That is the chance of being above both. “At least one” is bigger. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[8].feedback.byKey.neither` | That is the chance of being above neither: $1 - 0.65$. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[8].explain.text` | $0.6 + 0.5 - 0.45 = 0.65$. The regions show it: 0.15 above the 50-day only, 0.45 above both, ... | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[9].prose` | A desk has three risk limits, and bad days breach several at once. Limits 1, 2 and 3 are brea... | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[9].canvas.state.caption` | Breaches tend to come together on bad days | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[9].question` | What is the chance at least one limit is breached on a given day? | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[9].widget.answer` | 0.15 | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[9].widget.accept` | 0.15, or 15% | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[9].widget.wrong[0].value` | 0.23 | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[9].widget.wrong[1].value` | 0.14 | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[9].widget.wrong[2].value` | 0.13 | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[9].hints[0].text` | Start from $0.10 + 0.08 + 0.05 = 0.23$. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[9].hints[1].text` | Subtract the three pairs, $0.04 + 0.03 + 0.02$, then deal with the triple. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[9].hints[2].text` | $0.23 - 0.09 + 0.01 = 0.15$. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[9].feedback.correct` | $0.23 - 0.09 + 0.01 = 0.15$. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[9].feedback.generic` | Not quite right. Singles, minus pairs, plus the triple. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[9].feedback.byKey.added` | You added the three limits. Days that breach two or three limits were counted more than once. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[9].feedback.byKey.no-triple` | You stopped after the pairs. Days that breach all three were then removed completely; add the... | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[9].feedback.byKey.minus-triple` | You subtracted the triple. Its sign is plus. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `screens[9].explain.text` | $0.10 + 0.08 + 0.05 - 0.04 - 0.03 - 0.02 + 0.01 = 0.15$. The seven regions inside the circles... | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `summary.ideas` | ["Adding two counts takes the overlap twice, so take it away once.", "For three events: add t... | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `summary.formula.name` | Inclusion and exclusion | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `summary.formula.tex` | P(A \cup B) = P(A) + P(B) - P(A \cap B) | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `summary.formula.note` | For disjoint events the last term is 0. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `summary.trap` | Adding the chances of overlapping events counts the overlap twice. A total above 1 is the giv... | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `quiz[0].prose` | Two events have $P(A) = 0.5$ and $P(B) = 0.4$. You are told $P(A \cup B) = 0.7$. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `quiz[0].question` | What is $P(A \cap B)$? | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `quiz[0].widget.answer` | 0.2 | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `quiz[0].widget.accept` | 0.2 exactly | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `quiz[0].widget.wrong[0].value` | 0.9 | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `quiz[0].widget.wrong[1].value` | 0.3 | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `quiz[0].widget.wrong[2].value` | 0.1 | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `quiz[0].feedback.correct` | $0.5 + 0.4 - 0.7 = 0.2$. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `quiz[0].feedback.generic` | Not quite right. Rearrange $P(A \cup B) = P(A) + P(B) - P(A \cap B)$. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `quiz[0].feedback.byKey.sum` | You added $P(A)$ and $P(B)$. The overlap is how far that sum overshoots the union. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `quiz[0].feedback.byKey.a-only` | You worked out $0.7 - 0.4$, the chance of $A$ without $B$. The overlap is the rest of $A$. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `quiz[0].feedback.byKey.gap` | You subtracted $0.4$ from $0.5$. The union is needed to find the overlap. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `quiz[0].explain.text` | Rearranging the rule gives $P(A \cap B) = P(A) + P(B) - P(A \cup B)$. That is $0.9 - 0.7 = 0.... | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `quiz[1].prose` | A whole number from 1 to 100 is picked at random, each equally likely. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `quiz[1].question` | What is the chance it is divisible by 2 or by 5? | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `quiz[1].widget.answer` | 0.6 | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `quiz[1].widget.accept` | Any form equal to $\tfrac{60}{100}$, or 0.6 | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `quiz[1].widget.wrong[0].value` | 0.7 | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `quiz[1].widget.wrong[1].value` | 0.5 | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `quiz[1].widget.wrong[2].value` | 0.1 | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `quiz[1].feedback.correct` | $50 + 20 - 10 = 60$ numbers out of 100. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `quiz[1].feedback.generic` | Not quite right. Count multiples of 2, of 5, and of both. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `quiz[1].feedback.byKey.added` | You added 50 and 20. The 10 multiples of 10 were counted twice. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `quiz[1].feedback.byKey.twice` | You took the 10 multiples of 10 away twice. Take them away once. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `quiz[1].feedback.byKey.both` | That is the chance of being divisible by both, that is by 10. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `quiz[1].explain.text` | There are 50 even numbers and 20 multiples of 5. The 10 multiples of 10 are in both counts. S... | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `quiz[2].prose` | A whole number from 1 to 30 is picked at random, each equally likely. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `quiz[2].question` | What is the chance it is divisible by 2, 3 or 5? | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `quiz[2].widget.answer` | 0.7333 | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `quiz[2].widget.accept` | Any form equal to $\tfrac{22}{30} = \tfrac{11}{15}$, or $0.7333 \pm 0.0005$ | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `quiz[2].widget.wrong[0].value` | 1.0333 | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `quiz[2].widget.wrong[1].value` | 0.7 | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `quiz[2].widget.wrong[2].value` | 0.6667 | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `quiz[2].feedback.correct` | $15 + 10 + 6 - 5 - 3 - 2 + 1 = 22$ numbers out of 30. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `quiz[2].feedback.generic` | Not quite right. Singles, minus pairs, plus the triple. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `quiz[2].feedback.byKey.added` | You added 15, 10 and 6 and got more than 30 numbers. Multiples of 6, 10 and 15 were counted t... | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `quiz[2].feedback.byKey.no-triple` | You stopped after the pairs. The number 30 was then removed completely; add it back. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `quiz[2].feedback.byKey.minus-triple` | You subtracted the triple. Its sign is plus. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `quiz[2].explain.text` | Singles: 15 multiples of 2, 10 of 3, 6 of 5. Pairs: 5 multiples of 6, 3 of 10, 2 of 15. The t... | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `quiz[3].prose` | Two events have $P(A) = 0.7$ and $P(B) = 0.6$. Nothing else is known. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `quiz[3].question` | What is the smallest $P(A \cap B)$ can be? | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `quiz[3].widget.options[0].text` | $0.3$ | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `quiz[3].widget.options[0].correct` | true | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `quiz[3].widget.options[1].text` | $0$ | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `quiz[3].widget.options[1].why` | You let the events be disjoint. Then $P(A \cup B)$ would be $1.3$, above 1. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `quiz[3].widget.options[2].text` | $0.42$ | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `quiz[3].widget.options[2].why` | You multiplied the chances, which assumes independence. Nothing says they are independent. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `quiz[3].widget.options[3].text` | $0.6$ | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `quiz[3].widget.options[3].why` | That is the largest the overlap can be, when $B$ sits inside $A$. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `quiz[3].feedback.correct` | The union can be at most 1, so the overlap is at least $1.3 - 1$. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `quiz[3].feedback.generic` | Not quite right. Use $P(A \cup B) \le 1$ in the rule. | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |
| l9 | `quiz[3].explain.text` | The rule gives $P(A \cap B) = 1.3 - P(A \cup B)$. The union is at most 1, so the overlap is a... | correct | Ross 2.4 Props. 4.3 and 4.4 (inclusion and exclusion); 52 cards and random set triples, L3 script |

## l10-birthday.json

| file | JSON path | claim (short) | verdict | basis |
|---|---|---|---|---|
| l10 | `screens[0].prose` | Picture a planet whose year has 6 days, each equally likely as a birthday. Two people meet. E... | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[0].canvas.state.caption` | 36 equally likely pairs of birthdays | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[0].question` | Tap every cell where the two people share a birthday. | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[0].widget.answer` | ["r1c1", "r2c2", "r3c3", "r4c4", "r5c5", "r6c6"] | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[0].widget.wrong[0].set` | ["r1c1"] | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[0].hints[0].text` | A shared birthday means both people have the same day. Which cells are (3, 3) and its kind? | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[0].hints[1].text` | The matches lie on one diagonal, from the top left corner. | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[0].hints[2].text` | Tap (1, 1), (2, 2) and so on up to (6, 6). | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[0].feedback.correct` | Six of the 36 cells are matches: a chance of $\tfrac{1}{6}$. | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[0].feedback.generic` | Not quite right. A match is a cell whose two days are equal, and there is one for every day. | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[0].feedback.byKey.one-day` | Day 1 is one way to match. Any of the 6 days can be the shared one. | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[0].explain.text` | The matches are the 6 cells on the diagonal, so two people share with chance $\tfrac{6}{36} =... | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[1].prose` | A third person joins, still in the six-day year. Person 2 avoids person 1's day with chance $... | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[1].canvas.state.caption` | Six-day year: each person either lands on a new day or shares | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[1].question` | What is the chance at least two of the three share a birthday? | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[1].widget.answer` | 0.4444 | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[1].widget.accept` | Any form equal to $\tfrac{4}{9} = \tfrac{16}{36}$, or $0.4444 \pm 0.0005$ | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[1].widget.wrong[0].value` | 0.5 | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[1].widget.wrong[1].value` | 0.3056 | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[1].widget.wrong[2].value` | 0.5556 | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[1].hints[0].text` | It is easier to find the chance that all three birthdays differ. | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[1].hints[1].text` | All different means the path New day, then New day. | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[1].hints[2].text` | $\tfrac{5}{6} \times \tfrac{4}{6} = \tfrac{20}{36}$ for all different. Take that from 1. | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[1].feedback.correct` | $1 - \tfrac{5}{6} \cdot \tfrac{4}{6} = \tfrac{16}{36} = \tfrac{4}{9}$. | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[1].feedback.generic` | Not quite right. Find the chance all three differ along the tree, then use the complement. | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[1].feedback.byKey.pairs-added` | You added $\tfrac{1}{6}$ for each of the 3 pairs. The pairs overlap, so adding counts some ou... | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[1].feedback.byKey.one-day` | You let person 3 avoid only one day. Two days are taken by then, so the chance is $\tfrac{4}{... | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[1].feedback.byKey.all-diff` | $\tfrac{5}{9}$ is the chance all three differ. You want the other side. | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[1].explain.text` | All different needs New day twice: $\tfrac{5}{6} \cdot \tfrac{4}{6} = \tfrac{20}{36}$. Each f... | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[2].prose` | Now a real year of 365 days. Each new person must avoid every day already taken: $$P(\text{no... | imprecise | finding 12: the product needs equally likely days and unlinked birthdays, stated only on screen 5; 'a real year' suggests real birth dates, which are not uniform |
| l10 | `screens[2].question` | What is the smallest room where a shared birthday is more likely than not? | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[2].widget.answer` | 23 | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[2].widget.accept` | 23 people: the chance is 0.5073. At 22 it is 0.4757. | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[2].widget.wrong[0].value` | 183 | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[2].widget.wrong[1].value` | 22 | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[2].widget.wrong[2].value` | 366 | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[2].hints[0].text` | Slide until the curve crosses the dashed line at one half. | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[2].hints[1].text` | The crossing is in the low twenties. | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[2].hints[2].text` | At 22 people the chance is 0.4757; at 23 it is 0.5073. | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[2].feedback.correct` | 23 people give 0.5073, just over a half. | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[2].feedback.generic` | Not quite right. Read off where the curve first rises above the dashed line. | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[2].feedback.byKey.half-year` | Half of 365 is the guess most people make. The curve crosses one half far sooner. | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[2].feedback.byKey.just-below` | At 22 the chance is 0.4757, still below a half. One more person tips it over. | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[2].feedback.byKey.certain` | 366 makes a match certain. A half needs far fewer people. | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[2].explain.text` | The curve passes one half at 23 people, with 0.5073. It reaches 0.9704 at 50 and 0.9992 at 70... | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[3].prose` | Intuition compares 23 people with 365 days. But a match can happen between any two people in ... | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[3].canvas.state.caption` | 23 people: 0.5073 | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[3].question` | How many different pairs of people are there among 23? | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[3].widget.answer` | 253 | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[3].widget.accept` | 253 exactly: $\binom{23}{2} = \tfrac{23 \cdot 22}{2}$ | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[3].widget.wrong[0].value` | 23 | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[3].widget.wrong[1].value` | 22 | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[3].widget.wrong[2].value` | 506 | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[3].hints[0].text` | Each pair is a choice of 2 people from 23, where order does not matter. | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[3].hints[1].text` | Use $\binom{23}{2}$. | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[3].hints[2].text` | $\binom{23}{2} = \tfrac{23 \times 22}{2}$. | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[3].feedback.correct` | $\binom{23}{2} = 253$ pairs. | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[3].feedback.generic` | Not quite right. Choose 2 of the 23 people, and do not count a pair twice. | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[3].feedback.byKey.people` | That counts people. Matches happen between pairs of people. | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[3].feedback.byKey.others` | 22 is the number of pairs that include you. Other pairs can match too. | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[3].feedback.byKey.ordered` | You counted each pair twice, as (Ann, Ben) and (Ben, Ann). Divide by 2. | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[3].explain.text` | There are $\binom{23}{2} = 253$ pairs, each a 1 in 365 chance of a match. Pairs grow like $\t... | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[4].prose` | You join a room of 23 other people. Two questions sound alike. Will one of them share **your*... | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[4].canvas.state.caption` | Shared birthday among 23 people | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[4].question` | What is the chance that at least two of the 23 share a birthday? | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[4].widget.options[0].text` | $0.0630$ | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[4].widget.options[0].why` | You divided 23 by 365. That ignores the 253 pairs, and it is not the chance of any event here. | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[4].widget.options[1].text` | $0.0612$ | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[4].widget.options[1].why` | That is $1 - (\tfrac{364}{365})^{23}$, the chance someone shares **your** birthday. Any of th... | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[4].widget.options[2].text` | $0.5073$ | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[4].widget.options[2].correct` | true | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[4].widget.options[3].text` | $0.6932$ | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[4].widget.options[3].why` | You added $\tfrac{1}{365}$ for each of the 253 pairs. The pairs overlap, so adding counts out... | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[4].hints[0].text` | Is this about your birthday, or any pair at all? | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[4].hints[1].text` | Read the curve at 23. | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[4].hints[2].text` | Any pair counts, so use the product: $1 - \prod_{i=0}^{22} \tfrac{365 - i}{365}$. | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[4].feedback.correct` | 0.5073: any of the 253 pairs may match. | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[4].feedback.generic` | Not quite right. The question allows any two of the 23 to match. | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[4].feedback.byKey.you` | That is $1 - (\tfrac{364}{365})^{23}$, the chance someone shares **your** birthday. Any of th... | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[4].explain.text` | Someone matching you has chance $1 - (\tfrac{364}{365})^{23} = 0.0612$, the dashed curve. Any... | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[5].prose` | Write the product out in general. Assume 365 equally likely days, no leap day, and birthdays ... | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[5].question` | Put the lines of the derivation in order. | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[5].widget.lines[0].text` | Person 1 can have any birthday: chance $\tfrac{365}{365}$. | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[5].widget.lines[1].text` | Person 2 must avoid 1 taken day: chance $\tfrac{364}{365}$. | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[5].widget.lines[2].text` | Person $i + 1$ must avoid the $i$ taken days: chance $\tfrac{365 - i}{365}$. | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[5].widget.lines[3].text` | Each factor is given the ones before, so multiply: $P(\text{no shared}) = \prod_{i=0}^{n-1} \... | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[5].widget.lines[4].text` | Take the complement: $P(\text{shared}) = 1 - \prod_{i=0}^{n-1} \tfrac{365 - i}{365}$. | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[5].widget.answer` | ["s1", "s2", "s3", "s4", "s5"] | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[5].hints[0].text` | Start with the first person, who cannot clash with anyone. | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[5].hints[1].text` | The general line for person $i + 1$ comes after the two examples. | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[5].hints[2].text` | People one by one, then the product, then the complement. | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[5].feedback.correct` | One factor per person, multiplied, then the complement. | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[5].feedback.generic` | Not quite right. Add people in order, multiply, and only then take the complement. | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[5].feedback.byKey.s5` | The complement needs the full product first, so it comes last. | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[5].explain.text` | Each line adds one person and counts the days still free. Multiplying is the rule for stages,... | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[6].prose` | Turn the product into a function. Loop over the people, multiply in each new factor, then tak... | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[6].question` | Complete `p_shared(n)` so it returns the chance that at least two of `n` people share a birth... | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[6].hints[0].text` | Person $i + 1$ avoids the $i$ taken days with chance $\tfrac{365 - i}{365}$. | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[6].hints[1].text` | Inside the loop, multiply `p_none` by `(365 - i) / 365`. | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[6].hints[2].text` | `p_none = p_none * (365 - i) / 365`, then `return 1 - p_none`. | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[6].feedback.correct` | The loop builds the product one person at a time. | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[6].feedback.generic` | Some tests failed. Multiply in one factor per person, then return the complement. | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[6].feedback.byKey.error` | Your code stopped with an error. Check that both `...` are replaced. | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[6].feedback.byKey.test-1` | For 23 people the answer should be about 0.5073. Check the factor and the complement. | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[6].explain.text` | `range(n)` gives `i` from 0 to $n - 1$, one factor per person. At $n = 366$ the factor for $i... | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[7].prose` | At 70 people the chance is 0.9992: close to certain, but not certain. Some room size makes a ... | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[7].canvas.state.caption` | 70 people: 0.9992 | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[7].question` | What is the smallest number of people that guarantees a shared birthday? | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[7].widget.answer` | 366 | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[7].widget.accept` | 366 exactly | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[7].widget.wrong[0].value` | 365 | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[7].widget.wrong[1].value` | 183 | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[7].widget.wrong[2].value` | 70 | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[7].hints[0].text` | Could 365 people all have different birthdays? | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[7].hints[1].text` | With 365 people, every day could be used exactly once. | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[7].hints[2].text` | The next person has nowhere new to go: 366. | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[7].feedback.correct` | 366 people: the factor $\tfrac{365 - 365}{365}$ is 0. | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[7].feedback.generic` | Not quite right. Find the first room where different birthdays run out of days. | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[7].feedback.byKey.days` | 365 people can still all differ, one per day. One more person forces a match. | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[7].feedback.byKey.half` | 183 already makes a match almost certain, but not certain. | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[7].feedback.byKey.seventy` | At 70 the chance is 0.9992, not 1. Different birthdays are still possible. | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[7].explain.text` | With 365 people every day can be used once, so no match is forced. Person 366 has no free day... | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[8].prose` | A strategy sends 30 trades in one minute. The log stamps each trade to the second, so there a... | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[8].canvas.state.caption` | 60 slots instead of 365 days | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[8].question` | What is the chance at least two of the 30 trades share a timestamp? | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[8].widget.options[0].text` | $0.5$ | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[8].widget.options[0].why` | You divided 30 by 60. That ignores the 435 pairs of trades. | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[8].widget.options[1].text` | $0.7063$ | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[8].widget.options[1].why` | That is the birthday answer for 30 people and 365 days. Here there are only 60 seconds. | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[8].widget.options[2].text` | $0.3858$ | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[8].widget.options[2].why` | That is $1 - (\tfrac{59}{60})^{29}$, the chance some trade shares a second with one given trade. | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[8].widget.options[3].text` | $0.9999$ | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[8].widget.options[3].correct` | true | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[8].hints[0].text` | This is the birthday problem with 60 days and 30 people. | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[8].hints[1].text` | $P(\text{no shared}) = \prod_{i=0}^{29} \tfrac{60 - i}{60}$. | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[8].hints[2].text` | Ten trades already give 0.5475. Thirty trades leave almost no room. | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[8].feedback.correct` | $1 - \prod_{i=0}^{29} \tfrac{60 - i}{60} = 0.99986$. | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[8].feedback.generic` | Not quite right. Use the product with 60 slots and 30 trades. | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[8].feedback.byKey.one-trade` | That is the chance some trade shares a second with one given trade. Any of the 435 pairs can ... | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[8].explain.text` | With 60 slots the chance passes a half at just 10 trades, 0.5475. At 30 trades it is 0.99986.... | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[9].prose` | A small broker tags each order with a random 4-digit code, so 10,000 codes are possible. It s... | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[9].canvas.state.caption` | Each pair clashes with chance $\tfrac{1}{10000}$ | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[9].question` | What is the chance of at least one clash in a day of 100 orders? | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[9].widget.options[0].text` | $0.01$ | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[9].widget.options[0].why` | You divided 100 by 10,000. That ignores the 4,950 pairs. | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[9].widget.options[1].text` | $0.0099$ | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[9].widget.options[1].why` | That is the chance some order clashes with one given order. Any pair can clash. | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[9].widget.options[2].text` | $0.3914$ | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[9].widget.options[2].correct` | true | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[9].widget.options[3].text` | $0.495$ | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[9].widget.options[3].why` | You added $\tfrac{1}{10000}$ for each of the 4,950 pairs. The pairs overlap, so the sum overc... | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[9].hints[0].text` | This is the birthday problem with 10,000 days and 100 people. | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[9].hints[1].text` | $1 - \prod_{i=0}^{99} \tfrac{10000 - i}{10000}$. | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[9].hints[2].text` | The pair count, 4,950, is near half of 10,000, so expect a chance well above 1%. | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[9].feedback.correct` | $1 - \prod_{i=0}^{99} \tfrac{10000 - i}{10000} = 0.3914$. | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[9].feedback.generic` | Not quite right. Use the birthday product with 10,000 codes. | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[9].feedback.byKey.summed` | You added $\tfrac{1}{10000}$ for each of the 4,950 pairs. The pairs overlap, so the sum overc... | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `screens[9].explain.text` | The product gives 0.3914, about 2 days in 5. Collisions arrive near $\sqrt{10000} = 100$ draw... | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `summary.ideas` | ["Find the chance that nobody shares, one person at a time, then take the complement.", "With... | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `summary.formula.name` | Shared birthday among $n$ people | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `summary.formula.tex` | P(\text{shared}) = 1 - \prod_{i=0}^{n-1} \frac{365 - i}{365} | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `summary.formula.note` | 23 people give 0.5073, 50 give 0.9704, 70 give 0.9992; 366 make it certain. | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `summary.trap` | $1 - (\tfrac{364}{365})^n$ is the chance someone shares **your** birthday. Any pair can match... | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `quiz[0].prose` | A room holds 30 people. | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `quiz[0].question` | How many pairs of people could share a birthday? | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `quiz[0].widget.answer` | 435 | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `quiz[0].widget.accept` | 435 exactly: $\binom{30}{2}$ | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `quiz[0].widget.wrong[0].value` | 870 | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `quiz[0].widget.wrong[1].value` | 29 | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `quiz[0].feedback.correct` | $\binom{30}{2} = 435$. | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `quiz[0].feedback.generic` | Not quite right. Choose 2 of the 30, without order. | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `quiz[0].feedback.byKey.ordered` | You counted each pair twice, once in each order. | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `quiz[0].feedback.byKey.others` | 29 is the number of pairs including one person. Count every pair. | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `quiz[0].explain.text` | A pair is 2 people chosen from 30 without order: $\tfrac{30 \times 29}{2} = 435$. So 30 peopl... | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `quiz[1].prose` | Roll four fair dice. | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `quiz[1].question` | What is the chance that at least two of them show the same number? | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `quiz[1].widget.answer` | 0.7222 | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `quiz[1].widget.accept` | Any form equal to $\tfrac{13}{18}$, or $0.7222 \pm 0.0005$ | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `quiz[1].widget.wrong[0].value` | 1 | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `quiz[1].widget.wrong[1].value` | 0.4213 | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `quiz[1].widget.wrong[2].value` | 0.2778 | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `quiz[1].feedback.correct` | $1 - \tfrac{6 \cdot 5 \cdot 4 \cdot 3}{6^4} = 1 - \tfrac{5}{18} = \tfrac{13}{18}$. | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `quiz[1].feedback.generic` | Not quite right. Find the chance all four differ first. | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `quiz[1].feedback.byKey.pairs` | You added $\tfrac{1}{6}$ for each of the 6 pairs and got 1. Pairs overlap, so that overcounts. | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `quiz[1].feedback.byKey.one-die` | That is $1 - (\tfrac{5}{6})^3$, a match with the first die only. | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `quiz[1].feedback.byKey.all-diff` | That is the chance all four differ. Take it from 1. | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `quiz[1].explain.text` | All different has chance $\tfrac{6}{6} \cdot \tfrac{5}{6} \cdot \tfrac{4}{6} \cdot \tfrac{3}{... | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `quiz[2].prose` | Roll a fair die 7 times. | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `quiz[2].question` | What is the chance that some number appears at least twice? | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `quiz[2].widget.options[0].text` | $1$ | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `quiz[2].widget.options[0].correct` | true | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `quiz[2].widget.options[1].text` | $0.9846$ | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `quiz[2].widget.options[1].why` | That is the answer for 6 rolls. With 7 rolls and 6 faces, a repeat is forced. | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `quiz[2].widget.options[2].text` | $\dfrac{1}{6}$ | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `quiz[2].widget.options[2].why` | You treated it like one pair of rolls. Seven rolls make 21 pairs. | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `quiz[2].widget.options[3].text` | $0.9999$ | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `quiz[2].widget.options[3].why` | Close, but the product has a factor $\tfrac{6 - 6}{6} = 0$, so the chance is exactly 1. | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `quiz[2].feedback.correct` | Seven rolls cannot all differ with six faces. | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `quiz[2].feedback.generic` | Not quite right. Can seven rolls all be different? | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |
| l10 | `quiz[2].explain.text` | Six faces can be used once each in 6 rolls; the seventh must repeat one. In the product, the ... | correct | Ross 2.5 (birthday example); exact product, Monte Carlo and executed code, L3 script |

## l11-axioms.json

| file | JSON path | claim (short) | verdict | basis |
|---|---|---|---|---|
| l11 | `screens[0].prose` | Four pundits give chances for tomorrow's match. Exactly one result will happen: a home win, a... | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[0].canvas.state.caption` | Exactly one of the three results will happen | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[0].question` | Tap every pundit whose numbers could be real probabilities. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[0].widget.answer` | ["r0"] | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[0].hints[0].text` | Add each pundit's three numbers. What must they add to? | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[0].hints[1].text` | Also look for a number no chance can be. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[0].hints[2].text` | Ben adds to 1.1 and Dee to 0.6. Cal adds to 1, but one of Cal's chances is negative. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[0].feedback.correct` | Only Ana's numbers are all at least 0 and add to 1. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[0].feedback.generic` | Not quite right. Check two things in each row: the sum, and the sign of each number. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[0].feedback.byKey.r1` | Ben's chances add to 1.1. The three results cover everything exactly once, so they must add t... | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[0].feedback.byKey.r2` | Cal's add to 1, but an away win gets −0.1. No chance can be negative. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[0].feedback.byKey.r3` | Dee's add to 0.6. One result is certain to happen, so the three must add to 1. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[0].feedback.byKey.r0` | Ana's row passes both checks: no negatives, and a total of 1. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[0].explain.text` | Ana's numbers are all at least 0 and add to 1. Ben's add to 1.1 and Dee's to 0.6, but somethi... | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[1].prose` | Build your own forecast. Move the home win and draw sliders. The away win gets whatever is le... | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[1].question` | With the home win at 0.55, what is the largest chance the draw can have? | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[1].widget.answer` | 0.45 | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[1].widget.accept` | 0.45 | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[1].widget.wrong[0].value` | 1 | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[1].widget.wrong[1].value` | 0.55 | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[1].widget.wrong[2].value` | 0.225 | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[1].hints[0].text` | Push the draw up and watch the away bar. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[1].hints[1].text` | The away bar must not go below 0. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[1].hints[2].text` | Away is $1 - 0.55 - \text{draw}$, so the draw can reach $0.45$. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[1].feedback.correct` | A draw of 0.45 leaves the away win at exactly 0. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[1].feedback.generic` | Not quite right. Raise the draw until the away bar would dip below zero. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[1].feedback.byKey.whole` | A draw of 1 leaves the away win at −0.55. No chance can be negative. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[1].feedback.byKey.same` | A draw of 0.55 pushes the away win to −0.1, below zero. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[1].feedback.byKey.half` | You split what is left evenly. The draw can take all of it if the away win gets 0. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[1].explain.text` | With the home win at 0.55, the draw and away win share 0.45. The away bar cannot go below zer... | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[2].prose` | You used rules that every probability obeys. They are the **axioms**, for a sample space $S$:... | imprecise | finding 13: the axiom needs a list (countably many events); the dart screen argues by monotonicity and does not use the fractions; all points of [0, 1] cannot be listed (Ross 2.3, 2.6) |
| l11 | `screens[2].canvas.state.caption` | Ana's forecast | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[2].question` | Using Ana's forecast, what is the chance the home side does not lose? | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[2].widget.answer` | 0.8 | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[2].widget.accept` | 0.8 | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[2].widget.wrong[0].value` | 0.5 | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[2].widget.wrong[1].value` | 0.15 | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[2].widget.wrong[2].value` | 0.2 | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[2].hints[0].text` | Not losing means a home win or a draw. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[2].hints[1].text` | A home win and a draw cannot both happen, so they are disjoint. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[2].hints[2].text` | Axiom 3: $0.5 + 0.3$. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[2].feedback.correct` | Axiom 3: $0.5 + 0.3 = 0.8$. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[2].feedback.generic` | Not quite right. Name the results where the home side does not lose, then use axiom 3. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[2].feedback.byKey.home` | That is a home win only. A draw is also not a loss. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[2].feedback.byKey.product` | You multiplied. The results are disjoint, so their chances add. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[2].feedback.byKey.away` | That is the chance the home side loses. You want the rest. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[2].explain.text` | A home win and a draw are disjoint, so axiom 3 adds them: $0.5 + 0.3 = 0.8$. The complement g... | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[3].prose` | The empty event $\emptyset$ contains no outcomes. Show from the axioms that $P(\emptyset) = 0$. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[3].question` | Put the lines in order. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[3].widget.lines[0].text` | $S$ and $\emptyset$ share no outcome, so they are disjoint, and $S \cup \emptyset = S$. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[3].widget.lines[1].text` | Axiom 3: $P(S \cup \emptyset) = P(S) + P(\emptyset)$. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[3].widget.lines[2].text` | The left side is $P(S)$, so $P(S) = P(S) + P(\emptyset)$. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[3].widget.lines[3].text` | Subtract $P(S)$ from both sides: $P(\emptyset) = 0$. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[3].widget.answer` | ["s1", "s2", "s3", "s4"] | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[3].hints[0].text` | Axiom 3 needs two disjoint events. Which two? | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[3].hints[1].text` | Use $S$ and $\emptyset$ themselves. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[3].hints[2].text` | Disjoint first, then axiom 3, then replace $S \cup \emptyset$ by $S$, then subtract. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[3].feedback.correct` | Each line uses only the axioms and the line before. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[3].feedback.generic` | Not quite right. Check the events are disjoint before using axiom 3. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[3].feedback.byKey.s2` | Axiom 3 applies only once you know the events are disjoint. Show that first. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[3].explain.text` | Adding the empty event to $S$ changes nothing, yet axiom 3 adds $P(\emptyset)$. The only way ... | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[4].prose` | Now derive the complement rule from the axioms. One line of the chain is missing. $$\begin{al... | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[4].question` | Which line fills the gap? | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[4].widget.options[0].text` | $P(E \cup E^c) = P(S) = 1$, by axiom 1. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[4].widget.options[0].correct` | true | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[4].widget.options[1].text` | $P(E \cap E^c) = 0$, since the events are disjoint. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[4].widget.options[1].why` | That is true, but it says nothing about the sum on the right. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[4].widget.options[2].text` | $P(E^c) \ge 0$, by axiom 2. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[4].widget.options[2].why` | That is true, but it does not turn $P(E \cup E^c)$ into a number. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[4].widget.options[3].text` | $P(E) = P(E^c) = \tfrac{1}{2}$, by symmetry. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[4].widget.options[3].why` | Nothing makes $E$ and $E^c$ equally likely. A die gives $P(\text{six}) = \tfrac{1}{6}$. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[4].hints[0].text` | The last line has a 1 in it. Where can a 1 come from? | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[4].hints[1].text` | $E \cup E^c$ is the whole sample space. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[4].hints[2].text` | Axiom 1 says $P(S) = 1$. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[4].feedback.correct` | Axiom 1 supplies the 1. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[4].feedback.generic` | Not quite right. The gap must turn $P(E \cup E^c)$ into a number. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[4].feedback.byKey.pos` | That is true, but it does not turn $P(E \cup E^c)$ into a number. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[4].explain.text` | Since $E \cup E^c = S$, axiom 1 makes the sum equal to 1. Rearranging gives $P(E^c) = 1 - P(E... | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[5].prose` | Suppose $A \subseteq B$: whenever $A$ happens, $B$ happens. Then $B$ splits into $A$ and the ... | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[5].question` | Put the lines in order. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[5].widget.lines[0].text` | Since $A \subseteq B$, $B$ is the union of $A$ and $B \setminus A$, which are disjoint. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[5].widget.lines[1].text` | Axiom 3: $P(B) = P(A) + P(B \setminus A)$. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[5].widget.lines[2].text` | Axiom 2: $P(B \setminus A) \ge 0$, so $P(B) \ge P(A)$. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[5].widget.answer` | ["s1", "s2", "s3"] | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[5].hints[0].text` | Which axiom turns a split into a sum? | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[5].hints[1].text` | The split must come before axiom 3 can add. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[5].hints[2].text` | Split $B$, add with axiom 3, then drop a term that is at least 0. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[5].feedback.correct` | Split, add, then use that no chance is negative. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[5].feedback.generic` | Not quite right. Start with the split of $B$. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[5].feedback.byKey.s3` | The inequality needs the sum from axiom 3 first. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[5].explain.text` | $B$ is $A$ plus an extra piece, and that piece has chance at least 0. So $P(B)$ can only be l... | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[6].prose` | Linda is 31, outspoken and very bright. She studied philosophy and campaigned against discrim... | correct | Tversky and Kahneman (1983), Psychological Review 90: conjunction fallacy; monotonicity |
| l11 | `screens[6].canvas.state.caption` | Shaded: feminist bank tellers | correct | Tversky and Kahneman (1983), Psychological Review 90: conjunction fallacy; monotonicity |
| l11 | `screens[6].question` | Which statement must be at least as probable as the other? | correct | Tversky and Kahneman (1983), Psychological Review 90: conjunction fallacy; monotonicity |
| l11 | `screens[6].widget.options[0].text` | (a) Linda is a bank teller | correct | Tversky and Kahneman (1983), Psychological Review 90: conjunction fallacy; monotonicity |
| l11 | `screens[6].widget.options[0].correct` | true | correct | Tversky and Kahneman (1983), Psychological Review 90: conjunction fallacy; monotonicity |
| l11 | `screens[6].widget.options[1].text` | (b) Linda is a bank teller and a feminist | correct | Tversky and Kahneman (1983), Psychological Review 90: conjunction fallacy; monotonicity |
| l11 | `screens[6].widget.options[1].why` | The description fits a feminist, so (b) feels likely. But every feminist bank teller is a ban... | correct | Tversky and Kahneman (1983), Psychological Review 90: conjunction fallacy; monotonicity |
| l11 | `screens[6].widget.options[2].text` | Neither: it depends on the description | correct | Tversky and Kahneman (1983), Psychological Review 90: conjunction fallacy; monotonicity |
| l11 | `screens[6].widget.options[2].why` | The description moves both chances, but (b) always sits inside (a). No description can revers... | correct | Tversky and Kahneman (1983), Psychological Review 90: conjunction fallacy; monotonicity |
| l11 | `screens[6].hints[0].text` | Is every case of (b) also a case of (a)? | correct | Tversky and Kahneman (1983), Psychological Review 90: conjunction fallacy; monotonicity |
| l11 | `screens[6].hints[1].text` | (b) is the shaded overlap; (a) is the whole bank teller circle. | correct | Tversky and Kahneman (1983), Psychological Review 90: conjunction fallacy; monotonicity |
| l11 | `screens[6].hints[2].text` | $A \cap B \subseteq A$, so monotonicity gives $P(A \cap B) \le P(A)$. | correct | Tversky and Kahneman (1983), Psychological Review 90: conjunction fallacy; monotonicity |
| l11 | `screens[6].feedback.correct` | $P(A \cap B) \le P(A)$ always. | correct | Tversky and Kahneman (1983), Psychological Review 90: conjunction fallacy; monotonicity |
| l11 | `screens[6].feedback.generic` | Not quite right. Compare the shaded overlap with the whole bank teller circle. | correct | Tversky and Kahneman (1983), Psychological Review 90: conjunction fallacy; monotonicity |
| l11 | `screens[6].feedback.byKey.conj` | The description fits a feminist, so (b) feels likely. But every feminist bank teller is a ban... | correct | Tversky and Kahneman (1983), Psychological Review 90: conjunction fallacy; monotonicity |
| l11 | `screens[6].explain.text` | Most people pick (b) when first asked: the **conjunction fallacy**. But (b) is the overlap, w... | correct | Tversky and Kahneman (1983), Psychological Review 90: conjunction fallacy; monotonicity |
| l11 | `screens[7].prose` | Two events have $P(A) = 0.3$ and $P(B) = 0.25$. Nobody tells you how much they overlap. Use m... | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[7].question` | Which values could $P(A \cup B)$ take? Select all that apply. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[7].widget.options[0].text` | $0.2$ | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[7].widget.options[0].why` | The union contains $A$, so by monotonicity it is at least $0.3$. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[7].widget.options[1].text` | $0.3$ | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[7].widget.options[1].correct` | true | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[7].widget.options[2].text` | $0.45$ | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[7].widget.options[2].correct` | true | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[7].widget.options[3].text` | $0.55$ | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[7].widget.options[3].correct` | true | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[7].widget.options[4].text` | $0.6$ | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[7].widget.options[4].why` | The union is at most $P(A) + P(B) = 0.55$, since the overlap term is at least 0. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[7].hints[0].text` | How small can the union be? It always contains $A$. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[7].hints[1].text` | How large can it be? Inclusion and exclusion subtracts an overlap that is at least 0. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[7].hints[2].text` | Anything from $0.3$, when $B$ sits inside $A$, up to $0.55$, when they are disjoint. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[7].feedback.correct` | Anything from 0.3 up to 0.55. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[7].feedback.generic` | Not quite right. Find the smallest and largest the union can be. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[7].explain.text` | The union contains $A$, so it is at least $0.3$. Inclusion and exclusion subtracts $P(A \cap ... | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[8].prose` | From three axioms we derived: $$P(\emptyset) = 0, \qquad P(E^c) = 1 - P(E), \qquad 0 \le P(E)... | correct | Ross ch. 5 (continuous law: P(X = a) = 0); monotonicity |
| l11 | `screens[8].canvas.state.caption` | Chance of an interval = its length | correct | Ross ch. 5 (continuous law: P(X = a) = 0); monotonicity |
| l11 | `screens[8].question` | Is landing exactly on 0.5 impossible? | correct | Ross ch. 5 (continuous law: P(X = a) = 0); monotonicity |
| l11 | `screens[8].widget.options[0].text` | No. It can happen, but its probability is 0. | correct | Ross ch. 5 (continuous law: P(X = a) = 0); monotonicity |
| l11 | `screens[8].widget.options[0].correct` | true | correct | Ross ch. 5 (continuous law: P(X = a) = 0); monotonicity |
| l11 | `screens[8].widget.options[1].text` | Yes. Probability 0 means it cannot happen. | correct | Ross ch. 5 (continuous law: P(X = a) = 0); monotonicity |
| l11 | `screens[8].widget.options[1].why` | With finitely many outcomes that is true. Here every point has probability 0, yet the dart la... | correct | Ross ch. 5 (continuous law: P(X = a) = 0); monotonicity |
| l11 | `screens[8].widget.options[2].text` | No. Its probability is a tiny positive number. | correct | Ross ch. 5 (continuous law: P(X = a) = 0); monotonicity |
| l11 | `screens[8].widget.options[2].why` | Any tiny number fails: a shorter interval around 0.5 still contains it, and monotonicity caps... | correct | Ross ch. 5 (continuous law: P(X = a) = 0); monotonicity |
| l11 | `screens[8].feedback.correct` | Probability 0 is not the same as impossible here. | correct | Ross ch. 5 (continuous law: P(X = a) = 0); monotonicity |
| l11 | `screens[8].feedback.generic` | Not quite right. Every single point has length 0, and the dart must land on one. | correct | Ross ch. 5 (continuous law: P(X = a) = 0); monotonicity |
| l11 | `screens[8].explain.text` | By monotonicity the point's chance is at most any interval around it, however short. So it is... | correct | Ross ch. 5 (continuous law: P(X = a) = 0); monotonicity |
| l11 | `screens[9].prose` | A risk report sets out three scenarios for next quarter. Exactly one will happen: recession 0... | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[9].canvas.state.caption` | Total: 1.10 | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[9].question` | What is wrong with the report? | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[9].widget.options[0].text` | The scenarios are disjoint and cover every outcome, so their chances must add to 1. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[9].widget.options[0].correct` | true | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[9].widget.options[1].text` | Nothing: each number lies between 0 and 1. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[9].widget.options[1].why` | Each number is fine alone. Disjoint scenarios covering everything must add to exactly 1, and ... | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[9].widget.options[2].text` | Nothing: scenarios can overlap, so the total may pass 1. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[9].widget.options[2].why` | The report says exactly one scenario happens, so they are disjoint. Disjoint chances cannot a... | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[9].widget.options[3].text` | Growth is too high and should be cut to 0.35. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[9].widget.options[3].why` | The axioms cannot tell which number is wrong, only that the total is. Any fix needs the analy... | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[9].hints[0].text` | Exactly one scenario will happen. What does that say about the total? | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[9].hints[1].text` | Axioms 1 and 3 together force the total. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[9].hints[2].text` | Disjoint scenarios that cover everything add to $P(S) = 1$. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[9].feedback.correct` | Axioms 1 and 3 force a total of 1; the report says 1.1. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[9].feedback.generic` | Not quite right. Add the three chances and compare with $P(S)$. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[9].feedback.byKey.overlap` | The report says exactly one scenario happens, so they are disjoint. Disjoint chances cannot a... | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[9].explain.text` | By axioms 3 and 1, disjoint scenarios covering everything add to $P(S) = 1$. A total of 1.1 m... | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[10].prose` | A trading firm runs 10 systems. Each fails on a given day with chance 0.002. Failures can be ... | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[10].canvas.state.caption` | Each system: 0.002 a day | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[10].question` | What upper limit does the union bound give for the chance that at least one system fails? | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[10].widget.answer` | 0.02 | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[10].widget.accept` | 0.02, or 2% | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[10].widget.wrong[0].value` | 0.002 | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[10].widget.wrong[1].value` | 0.0198 | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[10].widget.wrong[2].value` | 1e-27 | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[10].hints[0].text` | The union bound works for any number of events. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[10].hints[1].text` | $P(E_1 \cup \dots \cup E_{10}) \le P(E_1) + \dots + P(E_{10})$. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[10].hints[2].text` | $10 \times 0.002$. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[10].feedback.correct` | $10 \times 0.002 = 0.02$. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[10].feedback.generic` | Not quite right. Add the ten chances. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[10].feedback.byKey.one` | That is one system. Any of the ten failing counts. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[10].feedback.byKey.indep` | $1 - 0.998^{10} \approx 0.0198$ assumes the failures are independent. The bound needs no such... | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[10].feedback.byKey.all` | That is the chance all ten fail at once, if independent. You want at least one. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `screens[10].explain.text` | The union bound gives at most $10 \times 0.002 = 0.02$, whatever the links. Linked failures o... | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `summary.ideas` | ["Three axioms: the whole sample space has chance 1, no chance is negative, and disjoint chan... | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `summary.formula.name` | Monotonicity | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `summary.formula.tex` | A \subseteq B \;\Rightarrow\; P(A) \le P(B) | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `summary.formula.note` | So $P(A \cap B) \le P(A)$: “and” is never more likely than either part. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `summary.trap` | A detailed story can make “bank teller and feminist” feel likelier than “bank teller”. It nev... | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `quiz[0].prose` | An analyst says: $P(\text{the stock falls more than } 5\%) = 0.4$ and $P(\text{the stock fall... | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `quiz[0].question` | Can both numbers be right? | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `quiz[0].widget.options[0].text` | No: a fall of more than 5% is a fall, so its chance cannot be larger. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `quiz[0].widget.options[0].correct` | true | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `quiz[0].widget.options[1].text` | Yes: both are between 0 and 1. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `quiz[0].widget.options[1].why` | Each is fine alone. But one event sits inside the other, so monotonicity orders them. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `quiz[0].widget.options[2].text` | No: they add to 0.7, not 1. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `quiz[0].widget.options[2].why` | The two events are not disjoint and do not cover everything, so they need not add to 1. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `quiz[0].feedback.correct` | Monotonicity: the smaller event cannot be more likely. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `quiz[0].feedback.generic` | Not quite right. Does one event sit inside the other? | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `quiz[0].explain.text` | Every fall of more than 5% is a fall, so the first event is a subset of the second. Monotonic... | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `quiz[1].prose` | Two disjoint events are given chances $P(A) = 0.45$ and $P(B) = 0.6$. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `quiz[1].question` | Is this possible? | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `quiz[1].widget.options[0].text` | No: axiom 3 would give $P(A \cup B) = 1.05$. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `quiz[1].widget.options[0].correct` | true | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `quiz[1].widget.options[1].text` | Yes: both chances are between 0 and 1. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `quiz[1].widget.options[1].why` | Each is fine alone. But disjoint chances add, and the total passes 1. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `quiz[1].widget.options[2].text` | Yes, as long as the overlap is 0.05. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `quiz[1].widget.options[2].why` | Disjoint means the overlap is empty, so there is no 0.05 to take away. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `quiz[1].feedback.correct` | A union of disjoint events would have chance 1.05. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `quiz[1].feedback.generic` | Not quite right. Add the two chances with axiom 3. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `quiz[1].explain.text` | Axiom 3 gives $P(A \cup B) = 0.45 + 0.6 = 1.05$. But every chance is at most 1, so the number... | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `quiz[2].prose` | A model gives $P(\text{up today}) = 0.55$. It also gives $P(\text{up today and volume above a... | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `quiz[2].question` | Which rule does the model break? | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `quiz[2].widget.options[0].text` | $P(A \cap B) \le P(A)$ | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `quiz[2].widget.options[0].correct` | true | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `quiz[2].widget.options[1].text` | $P(E^c) = 1 - P(E)$ | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `quiz[2].widget.options[1].why` | No complement appears here. The issue is an “and” event beating one of its parts. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `quiz[2].widget.options[2].text` | $P(A \cup B) \le P(A) + P(B)$ | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `quiz[2].widget.options[2].why` | That bound is about “or”. Here an “and” event is larger than one of its parts. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `quiz[2].widget.options[3].text` | No rule: the events are different | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `quiz[2].widget.options[3].why` | Different events, but one sits inside the other. That orders their chances. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `quiz[2].feedback.correct` | An “and” event lies inside each of its parts. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `quiz[2].feedback.generic` | Not quite right. Compare the “and” event with “up today”. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `quiz[2].explain.text` | Up with high volume is a subset of up. Monotonicity gives $P(A \cap B) \le P(A)$, so 0.6 cann... | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `quiz[3].prose` | Five strategies each breach their loss limit on a given day with chance 0.01. Breaches may be... | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `quiz[3].question` | What upper limit does the union bound give for the chance that at least one breaches? | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `quiz[3].widget.answer` | 0.05 | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `quiz[3].widget.accept` | 0.05 | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `quiz[3].widget.wrong[0].value` | 0.01 | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `quiz[3].widget.wrong[1].value` | 0.049 | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `quiz[3].feedback.correct` | $5 \times 0.01 = 0.05$. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `quiz[3].feedback.generic` | Not quite right. Add the five chances. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `quiz[3].feedback.byKey.one` | That is one strategy. Any of the five counts. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `quiz[3].feedback.byKey.indep` | $1 - 0.99^5 \approx 0.049$ assumes independence. The bound does not need it. | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |
| l11 | `quiz[3].explain.text` | The union bound gives $P(\text{any}) \le 5 \times 0.01 = 0.05$. It holds however the breaches... | correct | Ross 2.3 (axioms), 2.4 Props. 4.1 and 4.2, and the Boole inequality; derivation and Monte Carlo, L3 script |

## l12-poker-hands.json

| file | JSON path | claim (short) | verdict | basis |
|---|---|---|---|---|
| l12 | `screens[0].prose` | A poker hand is 5 cards dealt from a standard 52-card deck. The order they arrive in does not... | imprecise | finding 14: count over C(52,5) needs every hand equally likely (well-shuffled deck), not stated in the lesson (Ross 2.5) |
| l12 | `screens[0].canvas.state.caption` | One of the possible hands | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[0].question` | How many different 5-card hands are there? | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[0].widget.options[0].text` | $311{,}875{,}200$ | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[0].widget.options[0].why` | That is $52 \times 51 \times 50 \times 49 \times 48$. It counts each hand once per order of d... | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[0].widget.options[1].text` | $2{,}598{,}960$ | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[0].widget.options[1].correct` | true | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[0].widget.options[2].text` | $380{,}204{,}032$ | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[0].widget.options[2].why` | That is $52^5$. It lets the same card be dealt twice, but the deck has one of each. | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[0].widget.options[3].text` | $1{,}287$ | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[0].widget.options[3].why` | That is $\binom{13}{5}$, five cards from one suit only. | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[0].hints[0].text` | Does the order of the five cards matter? | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[0].hints[1].text` | Choose 5 cards from 52 without order. | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[0].hints[2].text` | $\binom{52}{5} = \tfrac{52 \times 51 \times 50 \times 49 \times 48}{5!}$. | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[0].feedback.correct` | $\binom{52}{5} = 2{,}598{,}960$ hands. | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[0].feedback.generic` | Not quite right. Choose 5 of 52 cards, where order does not matter. | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[0].feedback.byKey.ordered` | That is $52 \times 51 \times 50 \times 49 \times 48$. It counts each hand once per order of d... | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[0].explain.text` | Dealing in order gives $52 \times 51 \times 50 \times 49 \times 48$ sequences. Each hand appe... | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[1].prose` | A **full house** is three cards of one rank and two of another. You hold the four shaded card... | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[1].canvas.state.caption` | Shaded: three kings and the queen of spades | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[1].question` | Tap every card that would complete a full house as your fifth card. | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[1].widget.answer` | ["r2c12", "r3c12", "r4c12"] | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[1].widget.wrong[0].set` | ["r2c12", "r3c12", "r4c12", "r4c13"] | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[1].hints[0].text` | You have the three already. What do you need for the two? | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[1].hints[1].text` | A second queen pairs with your queen of spades. | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[1].hints[2].text` | The queens of hearts, diamonds and clubs each make a pair of queens. | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[1].feedback.correct` | Any of the three other queens makes kings full of queens. | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[1].feedback.generic` | Not quite right. Look for cards that pair with your queen. | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[1].feedback.byKey.fourth-king` | The king of clubs makes four kings: four of a kind, a different hand. | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[1].feedback.byKey.r4c13` | The king of clubs makes four kings: four of a kind, a different hand. | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[1].feedback.byKey.r1c13` | That card is already in your hand. | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[1].feedback.byKey.r2c13` | That card is already in your hand. | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[1].feedback.byKey.r3c13` | That card is already in your hand. | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[1].feedback.byKey.r1c12` | That card is already in your hand. | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[1].explain.text` | Three kings and a pair of queens is a full house, so any of the other three queens completes ... | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[2].prose` | **Four of a kind** is all four cards of one rank plus any fifth card. Count it in stages: fir... | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[2].canvas.state.caption` | Four queens: the fifth card can be any other card | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[2].question` | How many four-of-a-kind hands are there? | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[2].widget.answer` | 624 | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[2].widget.accept` | 624 exactly: $13 \times 48$ | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[2].widget.wrong[0].value` | 13 | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[2].widget.wrong[1].value` | 676 | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[2].widget.wrong[2].value` | 14976 | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[2].hints[0].text` | How many ranks could the four be? | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[2].hints[1].text` | Once four queens are in the hand, 48 cards are left for the fifth. | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[2].hints[2].text` | $13 \times 48$. | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[2].feedback.correct` | $13 \times 48 = 624$ hands. | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[2].feedback.generic` | Not quite right. Choose the rank, then the fifth card from those left. | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[2].feedback.byKey.no-fifth` | You counted the ranks only. Each four of a kind still needs a fifth card. | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[2].feedback.byKey.any-fifth` | You let the fifth card be any of 52, but four are already in the hand. | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[2].feedback.byKey.ordered` | You counted the four cards in order, $4! = 24$ ways each. They are all of that rank, so there... | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[2].explain.text` | 13 ranks for the four, then 48 cards for the fifth: $13 \times 48 = 624$. As a chance that is... | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[3].prose` | Now count full houses the same way. Each stage multiplies the count. Fill in the number of wa... | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[3].canvas.state.caption` | Kings full of queens | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[3].question` | Fill in the table. | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[3].widget.rows[0][0]` | Rank of the three | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[3].widget.rows[0][1].edit` | true | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[3].widget.rows[0][1].answer` | 13 | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[3].widget.rows[1][0]` | Suits of the three, $\binom{4}{3}$ | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[3].widget.rows[1][1].edit` | true | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[3].widget.rows[1][1].answer` | 4 | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[3].widget.rows[2][0]` | Rank of the pair | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[3].widget.rows[2][1].edit` | true | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[3].widget.rows[2][1].answer` | 12 | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[3].widget.rows[3][0]` | Suits of the pair, $\binom{4}{2}$ | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[3].widget.rows[3][1].edit` | true | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[3].widget.rows[3][1].answer` | 6 | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[3].widget.rows[4][0]` | Full houses: the product | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[3].widget.rows[4][1].edit` | true | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[3].widget.rows[4][1].answer` | 3744 | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[3].hints[0].text` | The pair's rank must differ from the three's rank. | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[3].hints[1].text` | 12 ranks are left for the pair once the three's rank is chosen. | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[3].hints[2].text` | $13 \times 4 \times 12 \times 6 = 3{,}744$. | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[3].feedback.correct` | $13 \times 4 \times 12 \times 6 = 3{,}744$ full houses. | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[3].feedback.generic` | Not quite right. Check each stage, then multiply. | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[3].feedback.byKey.r2c1` | The pair needs a rank different from the three: 12 are left. | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[3].feedback.byKey.r1c1` | Choose 3 of the 4 suits: $\binom{4}{3} = 4$. | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[3].feedback.byKey.r3c1` | Choose 2 of the 4 suits: $\binom{4}{2} = 6$. | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[3].feedback.byKey.r4c1` | Multiply the four stages: $13 \times 4 \times 12 \times 6$. | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[3].explain.text` | Rank of the three, its suits, rank of the pair, its suits: $13 \times 4 \times 12 \times 6 = ... | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[4].prose` | A friend counts full houses differently: “pick the 2 ranks with $\binom{13}{2}$, then the sui... | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[4].canvas.state.caption` | Kings full of queens. Swap the roles and you get queens full of kings. | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[4].question` | What is wrong with the friend's count? | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[4].widget.options[0].text` | It counts half the hands: the two ranks play different roles, so the order of the ranks matters. | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[4].widget.options[0].correct` | true | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[4].widget.options[1].text` | Nothing: ranks are unordered, so $\binom{13}{2}$ is right. | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[4].widget.options[1].why` | One rank is the three and the other is the pair. Swapping them makes a new hand, so $\binom{1... | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[4].widget.options[1].canvas.caption` | Queens full of kings: a different hand | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[4].widget.options[2].text` | The ranks should be $13 \times 13$. | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[4].widget.options[2].why` | The pair cannot share the three's rank. That would need five cards of one rank. | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[4].widget.options[3].text` | It double counts, so the true answer is 936. | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[4].widget.options[3].why` | It undercounts. Each pair of ranks gives two full houses, and the friend kept one. | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[4].hints[0].text` | Is kings full of queens the same hand as queens full of kings? | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[4].hints[1].text` | $\binom{13}{2}$ treats {K, Q} as one choice. How many full houses use those two ranks? | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[4].hints[2].text` | {K, Q} gives KKKQQ and QQQKK. So $13 \times 12$ ordered choices, not 78. | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[4].feedback.correct` | $13 \times 12 = 156$ ordered rank choices: twice 78. | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[4].feedback.generic` | Not quite right. Ask whether swapping the two ranks gives the same hand. | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[4].feedback.byKey.fine` | One rank is the three and the other is the pair. Swapping them makes a new hand, so $\binom{1... | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[4].explain.text` | Kings full of queens and queens full of kings are different hands. $\binom{13}{2}$ counts the... | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[4].explain.canvas.caption` | Queens full of kings: a different hand | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[5].prose` | A **flush** is five cards of one suit. A flush that is also five ranks in a row is a **straig... | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[5].canvas.state.caption` | A heart flush: the 2, 5, 9, jack and king of hearts | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[5].question` | How many flushes are there, leaving out the straight flushes? | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[5].widget.answer` | 5108 | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[5].widget.accept` | 5,108 exactly: $4 \binom{13}{5} - 40$ | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[5].widget.wrong[0].value` | 5148 | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[5].widget.wrong[0].canvas.caption` | 5 to 9 of hearts is a straight flush | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[5].widget.wrong[1].value` | 1287 | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[5].widget.wrong[2].value` | 1277 | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[5].hints[0].text` | Choose the suit, then 5 of its 13 ranks. | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[5].hints[1].text` | $4 \times \binom{13}{5} = 5{,}148$ hands have one suit. Some of them are straight flushes. | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[5].hints[2].text` | Take away $4 \times 10 = 40$ straight flushes: $5{,}148 - 40$. | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[5].feedback.correct` | $4 \times 1{,}287 - 40 = 5{,}108$ flushes. | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[5].feedback.generic` | Not quite right. Count all one-suit hands, then remove the straight flushes. | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[5].feedback.byKey.with-sf` | You kept the 40 straight flushes. They are a separate hand, so take them away. | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[5].feedback.byKey.one-suit` | That is one suit. Any of the 4 suits can make the flush. | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[5].feedback.byKey.one-suit-less` | You removed the straight flushes from one suit only. Use all 4 suits. | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[5].explain.text` | All one-suit hands number $4 \times \binom{13}{5} = 5{,}148$. Forty of them are straight flus... | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[6].prose` | **Two pair** is two cards of one rank, two of another, and a fifth card of a third rank. This... | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[6].canvas.state.caption` | Kings and queens with a seven | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[6].question` | How many two-pair hands are there? | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[6].widget.options[0].text` | $\binom{13}{2} \times 6 \times 6 \times 44 = 123{,}552$ | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[6].widget.options[0].correct` | true | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[6].widget.options[1].text` | $13 \times 12 \times 6 \times 6 \times 44 = 247{,}104$ | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[6].widget.options[1].why` | You ordered the two pairs. Kings and queens is the same hand as queens and kings, so use $\bi... | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[6].widget.options[2].text` | $\binom{13}{2} \times 6 \times 6 \times 48 = 134{,}784$ | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[6].widget.options[2].why` | Four of those 48 fifth cards match a pair, which makes a full house. The fifth card has 44 ch... | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[6].widget.options[3].text` | $\binom{13}{2} \times 6 \times 44 = 20{,}592$ | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[6].widget.options[3].why` | You chose suits for one pair only. Each pair picks 2 of its 4 suits. | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[6].hints[0].text` | Do the two pairs play different roles, as in a full house? | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[6].hints[1].text` | Swapping kings and queens gives the same hand, so choose the ranks with $\binom{13}{2}$. | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[6].hints[2].text` | Ranks $\binom{13}{2} = 78$, suits $6 \times 6$, and a fifth card from the 44 cards of other r... | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[6].feedback.correct` | $78 \times 36 \times 44 = 123{,}552$. | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[6].feedback.generic` | Not quite right. Count the ranks, the suits of each pair, then the fifth card. | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[6].feedback.byKey.ordered` | You ordered the two pairs. Kings and queens is the same hand as queens and kings, so use $\bi... | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[6].explain.text` | Here the pairs are interchangeable, so $\binom{13}{2}$ is right, unlike the full house. The f... | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[7].prose` | A **straight** is five ranks in a row, A-2-3-4-5 up to 10-J-Q-K-A, in mixed suits. The chart ... | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[7].canvas.state.caption` | Each step up the axis is 10 times more likely | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[7].question` | How many straights are there, leaving out the straight flushes? | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[7].widget.answer` | 10200 | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[7].widget.accept` | 10,200 exactly: $10 \times 4^5 - 40$ | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[7].widget.wrong[0].value` | 10240 | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[7].widget.wrong[1].value` | 9176 | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[7].widget.wrong[2].value` | 10 | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[7].hints[0].text` | How many runs of five ranks are there? | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[7].hints[1].text` | 10 runs, and each of the 5 cards can be any of 4 suits. | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[7].hints[2].text` | $10 \times 4^5 = 10{,}240$, minus the 40 straight flushes. | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[7].feedback.correct` | $10 \times 1{,}024 - 40 = 10{,}200$ straights. | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[7].feedback.generic` | Not quite right. Count the runs, the suit choices, then remove the straight flushes. | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[7].feedback.byKey.with-sf` | You kept the 40 straight flushes. They are a separate hand. | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[7].feedback.byKey.nine` | You missed one run. The ace can be low, A-2-3-4-5, or high, 10-J-Q-K-A: 10 runs. | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[7].feedback.byKey.no-suits` | That counts runs only. Each of the 5 cards can be any of 4 suits. | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[7].explain.text` | $10 \times 4^5 - 40 = 10{,}200$ straights: about twice as many as the 5,108 flushes. So a flu... | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[8].prose` | Every count was a product of stages, divided by the number of hands. $$P(\text{hand}) = \frac... | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[8].question` | How many hands are “nothing”: no pair, no straight and no flush? | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[8].widget.answer` | 1302540 | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[8].widget.accept` | 1,302,540 exactly | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[8].widget.wrong[0].value` | 1500720 | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[8].widget.wrong[1].value` | 2598960 | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[8].widget.wrong[2].value` | 1302580 | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[8].hints[0].text` | Use the complement: all hands minus every class you know. | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[8].hints[1].text` | The eight known counts add to 1,296,420. | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[8].hints[2].text` | $2{,}598{,}960 - 1{,}296{,}420$. | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[8].feedback.correct` | $2{,}598{,}960 - 1{,}296{,}420 = 1{,}302{,}540$. | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[8].feedback.generic` | Not quite right. Subtract all eight known counts from 2,598,960. | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[8].feedback.byKey.one-left` | You subtracted one pair only. Every other class must come off too. | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[8].feedback.byKey.all` | That is every hand. Take away the hands that make something. | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[8].feedback.byKey.no-sf` | You left out the 40 straight flushes. They are a class too. | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[8].explain.text` | The known classes total 1,296,420, so 1,302,540 hands make nothing. That is about half of all... | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[9].prose` | A risk model says a daily loss beyond £5m has chance 1 in 4,165: the chance of being dealt fo... | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[9].canvas.state.caption` | A 1-in-4,165 day, over longer and longer spans | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[9].question` | What is the chance of at least one such day in 10 years, or 2,520 trading days? | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[9].widget.answer` | 0.454 | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[9].widget.accept` | Any form equal to $1 - (\tfrac{4164}{4165})^{2520} \approx 0.4540$, within 0.0005 | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[9].widget.wrong[0].value` | 0.605 | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[9].widget.wrong[1].value` | 0.00024 | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[9].widget.wrong[2].value` | 0.0587 | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[9].hints[0].text` | Find the chance of no such day first. | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[9].hints[1].text` | Each day misses with chance $\tfrac{4164}{4165}$. | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[9].hints[2].text` | $1 - (\tfrac{4164}{4165})^{2520}$. | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[9].feedback.correct` | $1 - (\tfrac{4164}{4165})^{2520} \approx 0.4540$. | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[9].feedback.generic` | Not quite right. Use the complement: no such day on any of 2,520 days. | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[9].feedback.byKey.added` | You added $\tfrac{1}{4165}$ for each day. That is the union bound, a cap; it counts runs with... | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[9].feedback.byKey.one-day` | That is the chance on a single day. | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[9].feedback.byKey.one-year` | That is one year of 252 days. The question asks about ten. | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `screens[9].explain.text` | No such day has chance $(\tfrac{4164}{4165})^{2520} \approx 0.546$, so at least one has chanc... | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `summary.ideas` | ["Count a hand in stages: ranks first, then suits, then the leftover cards. Divide by $\\bino... | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `summary.formula.name` | Full house | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `summary.formula.tex` | 13 \times \binom{4}{3} \times 12 \times \binom{4}{2} = 3{,}744 | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `summary.formula.note` | Four of a kind: $13 \times 48 = 624$. Flush: $4\binom{13}{5} - 40 = 5{,}108$. | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `summary.trap` | $\binom{13}{2}$ for a full house halves the count: kings full of queens is not queens full of... | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `quiz[0].prose` | **Three of a kind** is three cards of one rank and two more cards of two other, different ranks. | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `quiz[0].question` | How many three-of-a-kind hands are there? | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `quiz[0].widget.options[0].text` | $13 \times 4 \times \binom{12}{2} \times 4 \times 4 = 54{,}912$ | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `quiz[0].widget.options[0].correct` | true | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `quiz[0].widget.options[1].text` | $13 \times 4 \times 12 \times 11 \times 4 \times 4 = 109{,}824$ | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `quiz[0].widget.options[1].why` | You ordered the two extra ranks. They play the same role, so use $\binom{12}{2}$. | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `quiz[0].widget.options[2].text` | $13 \times 4 \times \binom{48}{2} = 58{,}656$ | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `quiz[0].widget.options[2].why` | Some of those pairs of extra cards share a rank, which makes a full house. | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `quiz[0].widget.options[3].text` | $13 \times 4 \times \binom{49}{2} = 61{,}152$ | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `quiz[0].widget.options[3].why` | Choosing 2 of the other 49 cards lets in the fourth card of that rank, and pairs too. | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `quiz[0].feedback.correct` | $13 \times 4 \times 66 \times 16 = 54{,}912$. | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `quiz[0].feedback.generic` | Not quite right. The two extra cards need two different new ranks. | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `quiz[0].explain.text` | Rank and suits of the three: $13 \times 4$. Two different other ranks: $\binom{12}{2} = 66$, ... | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `quiz[1].prose` | There are 1,098,240 one-pair hands among the 2,598,960 possible hands. | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `quiz[1].question` | What is the chance a dealt hand is exactly one pair? Give a decimal to 4 places. | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `quiz[1].widget.answer` | 0.4226 | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `quiz[1].widget.accept` | $0.4226 \pm 0.0001$, or the fraction $\tfrac{1098240}{2598960}$ | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `quiz[1].widget.wrong[0].value` | 2.3665 | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `quiz[1].feedback.correct` | $\tfrac{1{,}098{,}240}{2{,}598{,}960} \approx 0.4226$. | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `quiz[1].feedback.generic` | Not quite right. Divide the count by the number of hands. | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `quiz[1].feedback.byKey.flipped` | You divided the hands by the count. A chance is the count over all hands. | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `quiz[1].explain.text` | $\tfrac{1{,}098{,}240}{2{,}598{,}960} \approx 0.4226$. Exactly one pair turns up in about 42%... | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `quiz[2].prose` | Four of a kind has chance $\tfrac{1}{4165}$ per deal. You play 4,165 independent deals. | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `quiz[2].question` | What is the chance you see at least one four of a kind? | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `quiz[2].widget.options[0].text` | $1$ | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `quiz[2].widget.options[0].why` | 4,165 deals give one four of a kind on average, not for certain. Some runs have none. | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `quiz[2].widget.options[1].text` | $0.632$ | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `quiz[2].widget.options[1].correct` | true | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `quiz[2].widget.options[2].text` | $0.5$ | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `quiz[2].widget.options[2].why` | No symmetry makes it a half. Use the complement. | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `quiz[2].widget.options[3].text` | $0.00024$ | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `quiz[2].widget.options[3].why` | That is the chance for a single deal. | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `quiz[2].feedback.correct` | $1 - (\tfrac{4164}{4165})^{4165} \approx 0.632$. | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `quiz[2].feedback.generic` | Not quite right. Find the chance of no four of a kind in all 4,165 deals. | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |
| l12 | `quiz[2].explain.text` | No four of a kind in 4,165 deals has chance $(\tfrac{4164}{4165})^{4165} \approx 0.368$. So a... | correct | Ross 2.5 (poker examples: straight, full house); all 2,598,960 hands enumerated, L3 script |

## review-3.json

| file | JSON path | claim (short) | verdict | basis |
|---|---|---|---|---|
| review-3 | `items[0].prose` | Two events have $P(A) = 0.35$, $P(B) = 0.25$ and $P(A \cap B) = 0.1$. | correct | Ross 2.4, 2.5; enumerated, L3 script |
| review-3 | `items[0].question` | What is $P(A \cup B)$? | correct | Ross 2.4, 2.5; enumerated, L3 script |
| review-3 | `items[0].widget.answer` | 0.5 | correct | Ross 2.4, 2.5; enumerated, L3 script |
| review-3 | `items[0].widget.accept` | 0.5 | correct | Ross 2.4, 2.5; enumerated, L3 script |
| review-3 | `items[0].widget.wrong[0].value` | 0.6 | correct | Ross 2.4, 2.5; enumerated, L3 script |
| review-3 | `items[0].widget.wrong[1].value` | 0.4 | correct | Ross 2.4, 2.5; enumerated, L3 script |
| review-3 | `items[0].feedback.correct` | $0.35 + 0.25 - 0.1 = 0.5$. | correct | Ross 2.4, 2.5; enumerated, L3 script |
| review-3 | `items[0].feedback.generic` | Not quite right. Add the two chances and take the overlap away once. | correct | Ross 2.4, 2.5; enumerated, L3 script |
| review-3 | `items[0].feedback.byKey.added` | You added the two chances. The overlap, 0.1, was counted twice. | correct | Ross 2.4, 2.5; enumerated, L3 script |
| review-3 | `items[0].feedback.byKey.twice` | You took the overlap away twice. Once is enough. | correct | Ross 2.4, 2.5; enumerated, L3 script |
| review-3 | `items[0].explain.text` | Inclusion and exclusion: $0.35 + 0.25 - 0.1 = 0.5$. The regions agree: $0.25 + 0.1 + 0.15 = 0... | correct | Ross 2.4, 2.5; enumerated, L3 script |
| review-3 | `items[1].prose` | A trading floor has 40 people. Assume 365 equally likely birthdays. | correct | Ross 2.4, 2.5; enumerated, L3 script |
| review-3 | `items[1].question` | What is the chance that at least two of them share a birthday? | correct | Ross 2.4, 2.5; enumerated, L3 script |
| review-3 | `items[1].widget.options[0].text` | $0.1096$ | correct | Ross 2.4, 2.5; enumerated, L3 script |
| review-3 | `items[1].widget.options[0].why` | You divided 40 by 365. That ignores the 780 pairs. | correct | Ross 2.4, 2.5; enumerated, L3 script |
| review-3 | `items[1].widget.options[1].text` | $0.1039$ | correct | Ross 2.4, 2.5; enumerated, L3 script |
| review-3 | `items[1].widget.options[1].why` | That is $1 - (\tfrac{364}{365})^{40}$, the chance someone shares one particular birthday. | correct | Ross 2.4, 2.5; enumerated, L3 script |
| review-3 | `items[1].widget.options[2].text` | $0.8912$ | correct | Ross 2.4, 2.5; enumerated, L3 script |
| review-3 | `items[1].widget.options[2].correct` | true | correct | Ross 2.4, 2.5; enumerated, L3 script |
| review-3 | `items[1].widget.options[3].text` | $2.137$ | correct | Ross 2.4, 2.5; enumerated, L3 script |
| review-3 | `items[1].widget.options[3].why` | You added $\tfrac{1}{365}$ for each of the 780 pairs and got more than 1. Pairs overlap. | correct | Ross 2.4, 2.5; enumerated, L3 script |
| review-3 | `items[1].feedback.correct` | $1 - \prod_{i=0}^{39} \tfrac{365 - i}{365} \approx 0.8912$. | correct | Ross 2.4, 2.5; enumerated, L3 script |
| review-3 | `items[1].feedback.generic` | Not quite right. Use the product of “avoid every taken day” chances. | correct | Ross 2.4, 2.5; enumerated, L3 script |
| review-3 | `items[1].feedback.byKey.you` | That is $1 - (\tfrac{364}{365})^{40}$, the chance someone shares one particular birthday. | correct | Ross 2.4, 2.5; enumerated, L3 script |
| review-3 | `items[1].explain.text` | No shared birthday has chance $\prod_{i=0}^{39} \tfrac{365 - i}{365} \approx 0.1088$. So a sh... | correct | Ross 2.4, 2.5; enumerated, L3 script |
| review-3 | `items[2].prose` | A model of two coin tosses gives $P(\text{at least one head}) = 0.75$ and $P(\text{two heads}... | correct | Ross 2.4, 2.5; enumerated, L3 script |
| review-3 | `items[2].question` | Which rule shows the model is wrong? | correct | Ross 2.4, 2.5; enumerated, L3 script |
| review-3 | `items[2].widget.options[0].text` | Two heads is a case of at least one head, so its chance cannot be larger. | correct | Ross 2.4, 2.5; enumerated, L3 script |
| review-3 | `items[2].widget.options[0].correct` | true | correct | Ross 2.4, 2.5; enumerated, L3 script |
| review-3 | `items[2].widget.options[1].text` | The two chances add to more than 1. | correct | Ross 2.4, 2.5; enumerated, L3 script |
| review-3 | `items[2].widget.options[1].why` | The events overlap, so their chances need not add to at most 1. | correct | Ross 2.4, 2.5; enumerated, L3 script |
| review-3 | `items[2].widget.options[2].text` | Nothing is wrong: both chances lie between 0 and 1. | correct | Ross 2.4, 2.5; enumerated, L3 script |
| review-3 | `items[2].widget.options[2].why` | Each is fine alone, but one event sits inside the other. | correct | Ross 2.4, 2.5; enumerated, L3 script |
| review-3 | `items[2].feedback.correct` | Monotonicity: a subset cannot be more likely. | correct | Ross 2.4, 2.5; enumerated, L3 script |
| review-3 | `items[2].feedback.generic` | Not quite right. Does one event sit inside the other? | correct | Ross 2.4, 2.5; enumerated, L3 script |
| review-3 | `items[2].explain.text` | Two heads implies at least one head, so the first event is a subset of the second. Monotonici... | correct | Ross 2.4, 2.5; enumerated, L3 script |
| review-3 | `items[3].prose` | Five cards are dealt from a standard deck. | imprecise | finding 14: equally likely hands not stated |
| review-3 | `items[3].question` | What is the chance of a full house? Give a fraction or a decimal to 5 places. | correct | Ross 2.4, 2.5; enumerated, L3 script |
| review-3 | `items[3].widget.answer` | 0.00144 | correct | Ross 2.4, 2.5; enumerated, L3 script |
| review-3 | `items[3].widget.accept` | Any form equal to $\tfrac{3744}{2598960} = \tfrac{6}{4165}$, or $0.00144$ | correct | Ross 2.4, 2.5; enumerated, L3 script |
| review-3 | `items[3].widget.wrong[0].value` | 0.00072 | correct | Ross 2.4, 2.5; enumerated, L3 script |
| review-3 | `items[3].feedback.correct` | $\tfrac{13 \times 4 \times 12 \times 6}{2{,}598{,}960} = \tfrac{6}{4165} \approx 0.00144$. | correct | Ross 2.4, 2.5; enumerated, L3 script |
| review-3 | `items[3].feedback.generic` | Not quite right. Count full houses in stages, then divide by $\binom{52}{5}$. | correct | Ross 2.4, 2.5; enumerated, L3 script |
| review-3 | `items[3].feedback.byKey.half` | You chose the two ranks with $\binom{13}{2}$. The three and the pair play different roles, so... | correct | Ross 2.4, 2.5; enumerated, L3 script |
| review-3 | `items[3].explain.text` | Full houses: $13 \times \binom{4}{3} \times 12 \times \binom{4}{2} = 3{,}744$. Divided by 2,5... | correct | Ross 2.4, 2.5; enumerated, L3 script |
| review-3 | `items[4].prose` | Three trading signals each fire on 30% of days. Each pair fires together on 10% of days, and ... | correct | Ross 2.4, 2.5; enumerated, L3 script |
| review-3 | `items[4].question` | On what share of days does at least one signal fire? Give a decimal. | correct | Ross 2.4, 2.5; enumerated, L3 script |
| review-3 | `items[4].widget.answer` | 0.65 | correct | Ross 2.4, 2.5; enumerated, L3 script |
| review-3 | `items[4].widget.accept` | 0.65, or 65% | correct | Ross 2.4, 2.5; enumerated, L3 script |
| review-3 | `items[4].widget.wrong[0].value` | 0.9 | correct | Ross 2.4, 2.5; enumerated, L3 script |
| review-3 | `items[4].widget.wrong[1].value` | 0.6 | correct | Ross 2.4, 2.5; enumerated, L3 script |
| review-3 | `items[4].widget.wrong[2].value` | 0.55 | correct | Ross 2.4, 2.5; enumerated, L3 script |
| review-3 | `items[4].feedback.correct` | $0.9 - 0.3 + 0.05 = 0.65$. | correct | Ross 2.4, 2.5; enumerated, L3 script |
| review-3 | `items[4].feedback.generic` | Not quite right. Singles, minus pairs, plus the triple. | correct | Ross 2.4, 2.5; enumerated, L3 script |
| review-3 | `items[4].feedback.byKey.added` | You added the three chances. Days when two or three fire were counted more than once. | correct | Ross 2.4, 2.5; enumerated, L3 script |
| review-3 | `items[4].feedback.byKey.no-triple` | You stopped after the pairs. Days when all three fire were then removed completely. | correct | Ross 2.4, 2.5; enumerated, L3 script |
| review-3 | `items[4].feedback.byKey.minus-triple` | You subtracted the triple. Its sign is plus. | correct | Ross 2.4, 2.5; enumerated, L3 script |
| review-3 | `items[4].explain.text` | $3 \times 0.3 - 3 \times 0.1 + 0.05 = 0.65$. Each signal alone fires on $0.3 - 0.05 - 0.05 - ... | correct | Ross 2.4, 2.5; enumerated, L3 script |
| review-3 | `items[5].prose` | Signal $A$ calls the direction right on 90% of days and signal $B$ on 85%. Nothing is known a... | correct | Ross 2.4, 2.5; enumerated, L3 script |
| review-3 | `items[5].question` | What is the smallest possible chance that both are right on the same day? | correct | Ross 2.4, 2.5; enumerated, L3 script |
| review-3 | `items[5].widget.answer` | 0.75 | correct | Ross 2.4, 2.5; enumerated, L3 script |
| review-3 | `items[5].widget.accept` | 0.75 | correct | Ross 2.4, 2.5; enumerated, L3 script |
| review-3 | `items[5].widget.wrong[0].value` | 0.765 | correct | Ross 2.4, 2.5; enumerated, L3 script |
| review-3 | `items[5].widget.wrong[1].value` | 0 | correct | Ross 2.4, 2.5; enumerated, L3 script |
| review-3 | `items[5].widget.wrong[2].value` | 0.85 | correct | Ross 2.4, 2.5; enumerated, L3 script |
| review-3 | `items[5].feedback.correct` | $P(A \cap B) \ge 0.9 + 0.85 - 1 = 0.75$. | correct | Ross 2.4, 2.5; enumerated, L3 script |
| review-3 | `items[5].feedback.generic` | Not quite right. Use inclusion and exclusion with $P(A \cup B) \le 1$. | correct | Ross 2.4, 2.5; enumerated, L3 script |
| review-3 | `items[5].feedback.byKey.product` | You multiplied, which assumes independence. The question asks for the smallest possible value. | correct | Ross 2.4, 2.5; enumerated, L3 script |
| review-3 | `items[5].feedback.byKey.zero` | If they were never both right, $P(A \cup B)$ would be 1.75, above 1. | correct | Ross 2.4, 2.5; enumerated, L3 script |
| review-3 | `items[5].feedback.byKey.smaller` | That is the largest possible overlap, when $B$ sits inside $A$. | correct | Ross 2.4, 2.5; enumerated, L3 script |
| review-3 | `items[5].explain.text` | Inclusion and exclusion gives $P(A \cap B) = 0.9 + 0.85 - P(A \cup B)$. The union is at most ... | correct | Ross 2.4, 2.5; enumerated, L3 script |
| review-3 | `items[6].prose` | **One pair** is two cards of one rank and three cards of three other, different ranks. | correct | Ross 2.4, 2.5; enumerated, L3 script |
| review-3 | `items[6].question` | Which count of one-pair hands is right? | correct | Ross 2.4, 2.5; enumerated, L3 script |
| review-3 | `items[6].widget.options[0].text` | $13 \times \binom{4}{2} \times \binom{12}{3} \times 4^3 = 1{,}098{,}240$ | correct | Ross 2.4, 2.5; enumerated, L3 script |
| review-3 | `items[6].widget.options[0].correct` | true | correct | Ross 2.4, 2.5; enumerated, L3 script |
| review-3 | `items[6].widget.options[1].text` | $13 \times \binom{4}{2} \times 12 \times 11 \times 10 \times 4^3 = 6{,}589{,}440$ | correct | Ross 2.4, 2.5; enumerated, L3 script |
| review-3 | `items[6].widget.options[1].why` | You ordered the three extra ranks. That gives more hands than the 2,598,960 that exist. | correct | Ross 2.4, 2.5; enumerated, L3 script |
| review-3 | `items[6].widget.options[2].text` | $13 \times \binom{4}{2} \times \binom{48}{3} = 1{,}349{,}088$ | correct | Ross 2.4, 2.5; enumerated, L3 script |
| review-3 | `items[6].widget.options[2].why` | Some of those three extra cards share a rank, which makes two pair or a full house. | correct | Ross 2.4, 2.5; enumerated, L3 script |
| review-3 | `items[6].widget.options[3].text` | $13 \times \binom{4}{2} \times \binom{12}{3} \times 4 = 68{,}640$ | correct | Ross 2.4, 2.5; enumerated, L3 script |
| review-3 | `items[6].widget.options[3].why` | Each of the three extra cards picks its own suit: $4^3$, not 4. | correct | Ross 2.4, 2.5; enumerated, L3 script |
| review-3 | `items[6].feedback.correct` | $13 \times 6 \times 220 \times 64 = 1{,}098{,}240$. | correct | Ross 2.4, 2.5; enumerated, L3 script |
| review-3 | `items[6].feedback.generic` | Not quite right. The three extra ranks play the same role, and each card picks a suit. | correct | Ross 2.4, 2.5; enumerated, L3 script |
| review-3 | `items[6].explain.text` | Pair rank and suits: $13 \times 6$. Three different other ranks, unordered: $\binom{12}{3} = ... | correct | Ross 2.4, 2.5; enumerated, L3 script |
| review-3 | `items[7].prose` | Five analysts each joined the firm in a month. Treat the 12 months as equally likely and inde... | correct | Ross 2.4, 2.5; enumerated, L3 script |
| review-3 | `items[7].question` | What is the chance at least two joined in the same month? Give a fraction or a decimal. | correct | Ross 2.4, 2.5; enumerated, L3 script |
| review-3 | `items[7].widget.answer` | 0.6181 | correct | Ross 2.4, 2.5; enumerated, L3 script |
| review-3 | `items[7].widget.accept` | Any form equal to $\tfrac{89}{144}$, or $0.6181 \pm 0.0005$ | correct | Ross 2.4, 2.5; enumerated, L3 script |
| review-3 | `items[7].widget.wrong[0].value` | 0.3819 | correct | Ross 2.4, 2.5; enumerated, L3 script |
| review-3 | `items[7].widget.wrong[1].value` | 0.4167 | correct | Ross 2.4, 2.5; enumerated, L3 script |
| review-3 | `items[7].widget.wrong[2].value` | 0.2939 | correct | Ross 2.4, 2.5; enumerated, L3 script |
| review-3 | `items[7].feedback.correct` | $1 - \tfrac{12 \cdot 11 \cdot 10 \cdot 9 \cdot 8}{12^5} = \tfrac{89}{144}$. | correct | Ross 2.4, 2.5; enumerated, L3 script |
| review-3 | `items[7].feedback.generic` | Not quite right. Find the chance all five months differ, then take the complement. | correct | Ross 2.4, 2.5; enumerated, L3 script |
| review-3 | `items[7].feedback.byKey.all-diff` | That is the chance all five months differ. Take it from 1. | correct | Ross 2.4, 2.5; enumerated, L3 script |
| review-3 | `items[7].feedback.byKey.ratio` | You divided 5 by 12. That ignores the 10 pairs. | correct | Ross 2.4, 2.5; enumerated, L3 script |
| review-3 | `items[7].feedback.byKey.one-person` | That is a match with one particular analyst only. Any pair can match. | correct | Ross 2.4, 2.5; enumerated, L3 script |
| review-3 | `items[7].explain.text` | All different has chance $\tfrac{12 \cdot 11 \cdot 10 \cdot 9 \cdot 8}{12^5} = \tfrac{55}{144... | correct | Ross 2.4, 2.5; enumerated, L3 script |

## homework-3.json

| file | JSON path | claim (short) | verdict | basis |
|---|---|---|---|---|
| homework-3 | `items[0].prose` | Count the whole numbers from 1 to 1,000 that are divisible by 3, by 5 or by 7. | correct | Ross 2.4, 2.5; enumerated, L3 script, code executed |
| homework-3 | `items[0].question` | How many are there? | correct | Ross 2.4, 2.5; enumerated, L3 script, code executed |
| homework-3 | `items[0].widget.answer` | 543 | correct | Ross 2.4, 2.5; enumerated, L3 script, code executed |
| homework-3 | `items[0].widget.accept` | 543 exactly | correct | Ross 2.4, 2.5; enumerated, L3 script, code executed |
| homework-3 | `items[0].widget.wrong[0].value` | 675 | correct | Ross 2.4, 2.5; enumerated, L3 script, code executed |
| homework-3 | `items[0].widget.wrong[1].value` | 534 | correct | Ross 2.4, 2.5; enumerated, L3 script, code executed |
| homework-3 | `items[0].widget.wrong[2].value` | 525 | correct | Ross 2.4, 2.5; enumerated, L3 script, code executed |
| homework-3 | `items[0].feedback.correct` | $333 + 200 + 142 - 66 - 47 - 28 + 9 = 543$. | correct | Ross 2.4, 2.5; enumerated, L3 script, code executed |
| homework-3 | `items[0].feedback.generic` | Not quite right. Singles, minus pairs, plus the triple; each count is a floor of 1,000 divide... | correct | Ross 2.4, 2.5; enumerated, L3 script, code executed |
| homework-3 | `items[0].feedback.byKey.added` | You added the three counts. Multiples of 15, 21 and 35 were counted twice. | correct | Ross 2.4, 2.5; enumerated, L3 script, code executed |
| homework-3 | `items[0].feedback.byKey.no-triple` | You stopped after the pairs. The 9 multiples of 105 were then removed completely. | correct | Ross 2.4, 2.5; enumerated, L3 script, code executed |
| homework-3 | `items[0].feedback.byKey.minus-triple` | You subtracted the 9 multiples of 105. Their sign is plus. | correct | Ross 2.4, 2.5; enumerated, L3 script, code executed |
| homework-3 | `items[0].explain.text` | Singles: $\lfloor 1000/3 \rfloor = 333$, 200 and 142. Pairs (multiples of 15, 21 and 35) give... | correct | Ross 2.4, 2.5; enumerated, L3 script, code executed |
| homework-3 | `items[1].prose` | Four letters are put into four addressed envelopes at random, all $4! = 24$ orders equally li... | correct | Ross 2.5 (matching problem); 24 orders enumerated, L3 script |
| homework-3 | `items[1].question` | What is the chance at least one letter reaches its own envelope? | correct | Ross 2.5 (matching problem); 24 orders enumerated, L3 script |
| homework-3 | `items[1].widget.answer` | 0.625 | correct | Ross 2.5 (matching problem); 24 orders enumerated, L3 script |
| homework-3 | `items[1].widget.accept` | Any form equal to $\tfrac{5}{8}$, or 0.625 | correct | Ross 2.5 (matching problem); 24 orders enumerated, L3 script |
| homework-3 | `items[1].widget.wrong[0].value` | 1 | correct | Ross 2.5 (matching problem); 24 orders enumerated, L3 script |
| homework-3 | `items[1].widget.wrong[1].value` | 0.6836 | correct | Ross 2.5 (matching problem); 24 orders enumerated, L3 script |
| homework-3 | `items[1].widget.wrong[2].value` | 0.5 | correct | Ross 2.5 (matching problem); 24 orders enumerated, L3 script |
| homework-3 | `items[1].widget.wrong[3].value` | 0.6667 | correct | Ross 2.5 (matching problem); 24 orders enumerated, L3 script |
| homework-3 | `items[1].feedback.correct` | $1 - \tfrac{1}{2} + \tfrac{1}{6} - \tfrac{1}{24} = \tfrac{5}{8}$. | correct | Ross 2.5 (matching problem); 24 orders enumerated, L3 script |
| homework-3 | `items[1].feedback.generic` | Not quite right. Use inclusion and exclusion with four events. $P(E_i \cap E_j) = \tfrac{2!}{... | correct | Ross 2.5 (matching problem); 24 orders enumerated, L3 script |
| homework-3 | `items[1].feedback.byKey.added` | You added $\tfrac{1}{4}$ four times. The events overlap, so that sum overcounts. | correct | Ross 2.5 (matching problem); 24 orders enumerated, L3 script |
| homework-3 | `items[1].feedback.byKey.indep` | $1 - (\tfrac{3}{4})^4$ treats the letters as independent. Once one letter is placed, the othe... | correct | Ross 2.5 (matching problem); 24 orders enumerated, L3 script |
| homework-3 | `items[1].feedback.byKey.two-terms` | You stopped after the pairs. Add the triples and subtract the quadruple. | correct | Ross 2.5 (matching problem); 24 orders enumerated, L3 script |
| homework-3 | `items[1].feedback.byKey.three-terms` | You stopped after the triples. The quadruple term, $\tfrac{1}{24}$, is subtracted. | correct | Ross 2.5 (matching problem); 24 orders enumerated, L3 script |
| homework-3 | `items[1].explain.text` | $\sum P(E_i) = 4 \cdot \tfrac{1}{4} = 1$. Pairs: $\binom{4}{2} \cdot \tfrac{2!}{24} = \tfrac{... | correct | Ross 2.5 (matching problem); 24 orders enumerated, L3 script |
| homework-3 | `items[2].prose` | A system draws codes from `d` equally likely values. Write `smallest_n(d, target)`: the small... | correct | Ross 2.4, 2.5; enumerated, L3 script, code executed |
| homework-3 | `items[2].question` | Complete `smallest_n(d, target)` in plain Python. | correct | Ross 2.4, 2.5; enumerated, L3 script, code executed |
| homework-3 | `items[2].feedback.correct` | The loop adds one draw at a time until the chance reaches the target. | correct | Ross 2.4, 2.5; enumerated, L3 script, code executed |
| homework-3 | `items[2].feedback.generic` | Some tests failed. Multiply in the factor for draw `n + 1`, $\tfrac{d - n}{d}$, before counti... | correct | Ross 2.4, 2.5; enumerated, L3 script, code executed |
| homework-3 | `items[2].feedback.byKey.error` | Your code stopped with an error. Check that both `...` are replaced. | correct | Ross 2.4, 2.5; enumerated, L3 script, code executed |
| homework-3 | `items[2].explain.text` | Draw $n + 1$ avoids the $n$ codes already seen with chance $\tfrac{d - n}{d}$. Stop as soon a... | correct | Ross 2.4, 2.5; enumerated, L3 script, code executed |
| homework-3 | `items[3].prose` | We know the union bound for two events: $P(E \cup F) \le P(E) + P(F)$. Extend it to three eve... | correct | Ross 2.4, 2.5; enumerated, L3 script, code executed |
| homework-3 | `items[3].question` | Put the lines of the proof in order. | correct | Ross 2.4, 2.5; enumerated, L3 script, code executed |
| homework-3 | `items[3].widget.lines[0].text` | Group the first two events: $A \cup B \cup C = (A \cup B) \cup C$. | correct | Ross 2.4, 2.5; enumerated, L3 script, code executed |
| homework-3 | `items[3].widget.lines[1].text` | Two-event bound with $E = A \cup B$, $F = C$: $P(A \cup B \cup C) \le P(A \cup B) + P(C)$. | correct | Ross 2.4, 2.5; enumerated, L3 script, code executed |
| homework-3 | `items[3].widget.lines[2].text` | Two-event bound again: $P(A \cup B) \le P(A) + P(B)$. | correct | Ross 2.4, 2.5; enumerated, L3 script, code executed |
| homework-3 | `items[3].widget.lines[3].text` | Substitute: $P(A \cup B \cup C) \le P(A) + P(B) + P(C)$. | correct | Ross 2.4, 2.5; enumerated, L3 script, code executed |
| homework-3 | `items[3].widget.answer` | ["s1", "s2", "s3", "s4"] | correct | Ross 2.4, 2.5; enumerated, L3 script, code executed |
| homework-3 | `items[3].feedback.correct` | Group, bound, bound again, substitute. | correct | Ross 2.4, 2.5; enumerated, L3 script, code executed |
| homework-3 | `items[3].feedback.generic` | Not quite right. Group two events into one first, so the two-event bound applies. | correct | Ross 2.4, 2.5; enumerated, L3 script, code executed |
| homework-3 | `items[3].explain.text` | Treating $A \cup B$ as one event lets the two-event bound apply. Bounding $P(A \cup B)$ the s... | correct | Ross 2.4, 2.5; enumerated, L3 script, code executed |
| homework-3 | `items[4].prose` | Five cards are dealt from a standard deck. | imprecise | finding 14: equally likely hands not stated |
| homework-3 | `items[4].question` | What is the chance all five cards have different ranks? Give a decimal to 4 places. | correct | Ross 2.4, 2.5; enumerated, L3 script, code executed |
| homework-3 | `items[4].widget.answer` | 0.5071 | correct | Ross 2.4, 2.5; enumerated, L3 script, code executed |
| homework-3 | `items[4].widget.accept` | $\tfrac{\binom{13}{5} 4^5}{\binom{52}{5}} = \tfrac{1317888}{2598960} \approx 0.5071$ | correct | Ross 2.4, 2.5; enumerated, L3 script, code executed |
| homework-3 | `items[4].widget.wrong[0].value` | 0.5012 | correct | Ross 2.4, 2.5; enumerated, L3 script, code executed |
| homework-3 | `items[4].widget.wrong[1].value` | 0.0005 | correct | Ross 2.4, 2.5; enumerated, L3 script, code executed |
| homework-3 | `items[4].feedback.correct` | $\tfrac{1{,}287 \times 1{,}024}{2{,}598{,}960} \approx 0.5071$. | correct | Ross 2.4, 2.5; enumerated, L3 script, code executed |
| homework-3 | `items[4].feedback.generic` | Not quite right. Choose 5 different ranks, then a suit for each card. | correct | Ross 2.4, 2.5; enumerated, L3 script, code executed |
| homework-3 | `items[4].feedback.byKey.nothing` | That is “nothing” only. Straights, flushes and straight flushes also have five different ranks. | correct | Ross 2.4, 2.5; enumerated, L3 script, code executed |
| homework-3 | `items[4].feedback.byKey.one-suit` | Each card picks its own suit: $4^5$ choices, not 1. | correct | Ross 2.4, 2.5; enumerated, L3 script, code executed |
| homework-3 | `items[4].explain.text` | Ranks: $\binom{13}{5} = 1{,}287$; suits: $4^5 = 1{,}024$; so 1,317,888 hands. That matches $1... | correct | Ross 2.4, 2.5; enumerated, L3 script, code executed |
| homework-3 | `items[5].prose` | Five cards are dealt from a standard deck. Let $M_s$ be “suit $s$ is missing from the hand”, ... | imprecise | finding 14: equally likely hands not stated |
| homework-3 | `items[5].question` | What is the chance the hand contains all four suits? Give a decimal to 4 places. | correct | Ross 2.4, 2.5; enumerated, L3 script, code executed |
| homework-3 | `items[5].widget.answer` | 0.2637 | correct | Ross 2.4, 2.5; enumerated, L3 script, code executed |
| homework-3 | `items[5].widget.accept` | $\tfrac{685464}{2598960} = \tfrac{2197}{8330} \approx 0.2637$ | correct | Ross 2.4, 2.5; enumerated, L3 script, code executed |
| homework-3 | `items[5].widget.wrong[0].value` | 0.1139 | correct | Ross 2.4, 2.5; enumerated, L3 script, code executed |
| homework-3 | `items[5].widget.wrong[1].value` | 0.2658 | wrong | finding 2: (C(52,5) - 4 C(39,5) + 6 C(26,5)) / C(52,5) = 690,612 / 2,598,960 = 0.265726, which is 0.2657 to 4 places (L3 script, failing check) |
| homework-3 | `items[5].widget.wrong[2].value` | 0.5275 | correct | Ross 2.4, 2.5; enumerated, L3 script, code executed |
| homework-3 | `items[5].feedback.correct` | $2{,}598{,}960 - (4 \cdot 575{,}757 - 6 \cdot 65{,}780 + 4 \cdot 1{,}287) = 685{,}464$ hands. | correct | Ross 2.4, 2.5; enumerated, L3 script, code executed |
| homework-3 | `items[5].feedback.generic` | Not quite right. Count hands missing at least one suit with inclusion and exclusion, then tak... | correct | Ross 2.4, 2.5; enumerated, L3 script, code executed |
| homework-3 | `items[5].feedback.byKey.one-term` | You subtracted $4\binom{39}{5}$ only. Hands missing two suits were taken away twice; add them... | correct | Ross 2.4, 2.5; enumerated, L3 script, code executed |
| homework-3 | `items[5].feedback.byKey.two-terms` | You stopped after the pairs. Hands missing three suits need the third term. | correct | Ross 2.4, 2.5; enumerated, L3 script, code executed |
| homework-3 | `items[5].feedback.byKey.direct-double` | You chose the doubled suit's two cards in order. Use $\binom{13}{2}$ for them. | correct | Ross 2.4, 2.5; enumerated, L3 script, code executed |
| homework-3 | `items[5].explain.text` | Missing a given suit: $\binom{39}{5}$; two given suits: $\binom{26}{5}$; three: $\binom{13}{5... | correct | Ross 2.4, 2.5; enumerated, L3 script, code executed |
| homework-3 | `items[6].prose` | An exchange gateway gives each order a random id from 1,000,000 values. A busy session sends ... | correct | Ross 2.4, 2.5; enumerated, L3 script, code executed |
| homework-3 | `items[6].question` | What is the chance two of the 500 orders get the same id? | correct | Ross 2.4, 2.5; enumerated, L3 script, code executed |
| homework-3 | `items[6].widget.options[0].text` | $0.0005$ | correct | Ross 2.4, 2.5; enumerated, L3 script, code executed |
| homework-3 | `items[6].widget.options[0].why` | You divided 500 by a million. That ignores the 124,750 pairs. | correct | Ross 2.4, 2.5; enumerated, L3 script, code executed |
| homework-3 | `items[6].widget.options[1].text` | $0.1173$ | correct | Ross 2.4, 2.5; enumerated, L3 script, code executed |
| homework-3 | `items[6].widget.options[1].correct` | true | correct | Ross 2.4, 2.5; enumerated, L3 script, code executed |
| homework-3 | `items[6].widget.options[2].text` | $0.1248$ | correct | Ross 2.4, 2.5; enumerated, L3 script, code executed |
| homework-3 | `items[6].widget.options[2].why` | You added one in a million for each pair. That is the union bound, a cap, not the exact chance. | correct | Ross 2.4, 2.5; enumerated, L3 script, code executed |
| homework-3 | `items[6].widget.options[3].text` | $0.000001$ | correct | Ross 2.4, 2.5; enumerated, L3 script, code executed |
| homework-3 | `items[6].widget.options[3].why` | That is the chance one given pair clashes. | correct | Ross 2.4, 2.5; enumerated, L3 script, code executed |
| homework-3 | `items[6].feedback.correct` | $1 - \prod_{i=0}^{499} \tfrac{10^6 - i}{10^6} \approx 0.1173$. | correct | Ross 2.4, 2.5; enumerated, L3 script, code executed |
| homework-3 | `items[6].feedback.generic` | Not quite right. This is the birthday product with a million days and 500 people. | correct | Ross 2.4, 2.5; enumerated, L3 script, code executed |
| homework-3 | `items[6].explain.text` | 500 orders make $\binom{500}{2} = 124{,}750$ pairs. The product gives a clash chance of about... | correct | Ross 2.4, 2.5; enumerated, L3 script, code executed |
| homework-3 | `items[7].prose` | A report states $P(A) = 0.6$, $P(B) = 0.5$ and $P(A \cap B) = 0.05$. | correct | Ross 2.4, 2.5; enumerated, L3 script, code executed |
| homework-3 | `items[7].question` | Can all three numbers be right? | correct | Ross 2.4, 2.5; enumerated, L3 script, code executed |
| homework-3 | `items[7].widget.options[0].text` | No: they force $P(A \cup B) = 1.05$, above 1. | correct | Ross 2.4, 2.5; enumerated, L3 script, code executed |
| homework-3 | `items[7].widget.options[0].correct` | true | correct | Ross 2.4, 2.5; enumerated, L3 script, code executed |
| homework-3 | `items[7].widget.options[1].text` | Yes: each is between 0 and 1, and the overlap is below both. | correct | Ross 2.4, 2.5; enumerated, L3 script, code executed |
| homework-3 | `items[7].widget.options[1].why` | Each check passes, but inclusion and exclusion gives a union of 1.05. | correct | Ross 2.4, 2.5; enumerated, L3 script, code executed |
| homework-3 | `items[7].widget.options[2].text` | No: the overlap must be $0.6 \times 0.5 = 0.3$. | correct | Ross 2.4, 2.5; enumerated, L3 script, code executed |
| homework-3 | `items[7].widget.options[2].why` | Only independent events have that overlap. Nothing says these are independent. | correct | Ross 2.4, 2.5; enumerated, L3 script, code executed |
| homework-3 | `items[7].feedback.correct` | $0.6 + 0.5 - 0.05 = 1.05 > 1$. | correct | Ross 2.4, 2.5; enumerated, L3 script, code executed |
| homework-3 | `items[7].feedback.generic` | Not quite right. Work out $P(A \cup B)$ from the three numbers. | correct | Ross 2.4, 2.5; enumerated, L3 script, code executed |
| homework-3 | `items[7].explain.text` | Inclusion and exclusion gives $P(A \cup B) = 0.6 + 0.5 - 0.05 = 1.05$. No chance exceeds 1, s... | correct | Ross 2.4, 2.5; enumerated, L3 script, code executed |
| homework-3 | `items[8].prompt` | Using only the two-event rule $P(E \cup F) = P(E) + P(F) - P(E \cap F)$ and set algebra, prov... | correct | Ross 2.4, 2.5; enumerated, L3 script, code executed |
| homework-3 | `items[8].model` | **Step 1.** Group: $A \cup B \cup C = (A \cup B) \cup C$. Apply the two-event rule with $E = ... | correct | Ross 2.4, 2.5; enumerated, L3 script, code executed |
| homework-3 | `items[8].rubric[0].text` | Groups $A \cup B$ as one event and applies the two-event rule with $C$. | correct | Ross 2.4, 2.5; enumerated, L3 script, code executed |
| homework-3 | `items[8].rubric[1].text` | Expands $P(A \cup B)$ with the two-event rule. | correct | Ross 2.4, 2.5; enumerated, L3 script, code executed |
| homework-3 | `items[8].rubric[2].text` | Writes $(A \cup B) \cap C = (A \cap C) \cup (B \cap C)$, with a reason (distributivity). | correct | Ross 2.4, 2.5; enumerated, L3 script, code executed |
| homework-3 | `items[8].rubric[3].text` | Applies the two-event rule to that union, using $(A \cap C) \cap (B \cap C) = A \cap B \cap C$. | correct | Ross 2.4, 2.5; enumerated, L3 script, code executed |
| homework-3 | `items[8].rubric[4].text` | Substitutes with the signs handled correctly, reaching the stated formula. | correct | Ross 2.4, 2.5; enumerated, L3 script, code executed |
| homework-3 | `items[8].rubric[5].text` | Computes 0.15 for the risk limits. | correct | Ross 2.4, 2.5; enumerated, L3 script, code executed |
| homework-3 | `items[8].rubric[6].text` | States the union bound 0.23 and explains why it is larger. | correct | Ross 2.4, 2.5; enumerated, L3 script, code executed |

## problems-3.json

| file | JSON path | claim (short) | verdict | basis |
|---|---|---|---|---|
| problems-3 | `items[0].prose` | A market data system stores each new symbol on one of 50 shards. Each symbol lands on a shard... | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[0].parts[0].question` | Five new symbols arrive. What is the chance that no two of them share a shard? Give a decimal... | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[0].parts[0].widget.answer` | 0.813604 | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[0].parts[0].widget.accept` | 0.8136: $\tfrac{50}{50} \cdot \tfrac{49}{50} \cdot \tfrac{48}{50} \cdot \tfrac{47}{50} \cdot ... | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[0].parts[0].widget.wrong[0].value` | 0.922368 | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[0].parts[0].widget.wrong[1].value` | 0.92 | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[0].parts[0].feedback.correct` | Each new symbol avoids the shards already taken: $\tfrac{49}{50} \cdot \tfrac{48}{50} \cdot \... | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[0].parts[0].feedback.generic` | Not quite. Add the symbols one at a time; each must miss every shard already used. | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[0].parts[0].feedback.byKey.your-shard` | That is $\left(\tfrac{49}{50}\right)^4$, the chance no symbol joins the first one. Every pair... | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[0].parts[0].feedback.byKey.last-only` | That is $\tfrac{46}{50}$, the last factor alone. Multiply all the factors, one per symbol. | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[0].parts[0].explain.text` | Symbol 2 avoids 1 used shard with chance $\tfrac{49}{50}$, symbol 3 avoids 2 with $\tfrac{48}... | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[0].parts[1].question` | Using $P(\text{no clash}) \approx 0.81360$ for five symbols, what is the chance of at least o... | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[0].parts[1].widget.answer` | 0.186396 | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[0].parts[1].widget.accept` | 0.1864: $1 - 0.81360$. | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[0].parts[1].widget.wrong[0].value` | 0.813604 | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[0].parts[1].widget.wrong[1].value` | 0.077632 | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[0].parts[1].widget.wrong[2].value` | 0.2 | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[0].parts[1].feedback.correct` | $1 - 0.81360 = 0.18640$. | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[0].parts[1].feedback.generic` | Not quite. A clash is the complement of “no clash”. | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[0].parts[1].feedback.byKey.none` | That is the chance of no clash. Take it from 1. | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[0].parts[1].feedback.byKey.from-your-shard` | That is $1 - \left(\tfrac{49}{50}\right)^4$, a clash with the first symbol only. Any pair of ... | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[0].parts[1].feedback.byKey.pairs` | That is $\tfrac{10}{50}$, the 10 pairs times $\tfrac{1}{50}$. It counts runs with two clashes... | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[0].parts[1].explain.text` | “At least one clash” is the complement of “no clash”. So the chance is $1 - 0.81360 \approx 0... | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[0].parts[2].question` | Using $0.81360$ for five symbols, add symbols one at a time. What is the smallest number of s... | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[0].parts[2].widget.answer` | 9 | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[0].parts[2].widget.accept` | 9 exactly: $P(\text{clash}) \approx 0.4458$ at 8 and $0.5345$ at 9. | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[0].parts[2].widget.wrong[0].value` | 25 | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[0].parts[2].widget.wrong[1].value` | 8 | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[0].parts[2].widget.wrong[2].value` | 7 | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[0].parts[2].feedback.correct` | Multiply on: 0.73224 at 6, 0.64437 at 7, 0.55416 at 8 and 0.46550 at 9. So 9 symbols pass one... | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[0].parts[2].feedback.generic` | Not quite. Multiply $0.81360$ by $\tfrac{45}{50}$, then $\tfrac{44}{50}$, and so on, and watc... | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[0].parts[2].feedback.byKey.half` | That is half of 50 shards. A clash can happen between any pair, and pairs grow much faster th... | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[0].parts[2].feedback.byKey.union-bound` | That solves $\tfrac{\binom{n}{2}}{50} \ge \tfrac{1}{2}$, the union bound. At 8 the true chanc... | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[0].parts[2].feedback.byKey.root` | That is about $\sqrt{50}$, a rough guide only. At 7 the chance is 0.3556. | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[0].parts[2].explain.text` | Multiply in $\tfrac{45}{50}, \tfrac{44}{50}, \tfrac{43}{50}, \tfrac{42}{50}$: no clash falls ... | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[0].parts[3].question` | Using $n = 9$ symbols, what upper limit does the union bound give for the chance of a clash? ... | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[0].parts[3].widget.answer` | 0.72 | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[0].parts[3].widget.accept` | 0.72: $\binom{9}{2} \times \tfrac{1}{50} = \tfrac{36}{50}$. | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[0].parts[3].widget.wrong[0].value` | 0.16 | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[0].parts[3].widget.wrong[1].value` | 0.534504 | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[0].parts[3].widget.wrong[2].value` | 1.44 | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[0].parts[3].feedback.correct` | There are $\binom{9}{2} = 36$ pairs, each clashing with chance $\tfrac{1}{50}$: at most $\tfr... | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[0].parts[3].feedback.generic` | Not quite. Count the pairs, then add a chance of $\tfrac{1}{50}$ for each. | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[0].parts[3].feedback.byKey.one-symbol` | That is $\tfrac{8}{50}$, the pairs of one symbol only. Each of the $\binom{9}{2}$ pairs can c... | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[0].parts[3].feedback.byKey.exact` | That is the exact chance. The union bound adds the pair chances, which gives more. | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[0].parts[3].feedback.byKey.ordered-pairs` | You counted ordered pairs, $9 \times 8 = 72$. Each pair is one event, so there are 36. | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[0].parts[3].explain.text` | A clash is the union of 36 pair events, each with chance $\tfrac{1}{50}$. The union bound nee... | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[1].prose` | A lender tracks three borrowers, $A$, $B$ and $C$, each of which may be downgraded within the... | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[1].parts[0].question` | What is $P(A \cup B)$, the chance that $A$ or $B$ is downgraded? Give a decimal. | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[1].parts[0].widget.answer` | 0.15 | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[1].parts[0].widget.accept` | 0.15: $0.10 + 0.08 - 0.03$. | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[1].parts[0].widget.wrong[0].value` | 0.18 | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[1].parts[0].widget.wrong[1].value` | 0.03 | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[1].parts[0].feedback.correct` | $0.10 + 0.08 - 0.03 = 0.15$. | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[1].parts[0].feedback.generic` | Not quite. Add the two chances, then take the overlap away once. | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[1].parts[0].feedback.byKey.no-overlap` | You added $P(A)$ and $P(B)$. The 0.03 where both are downgraded was counted twice. | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[1].parts[0].feedback.byKey.both` | That is $P(A \cap B)$, both downgraded. “Or” includes either one. | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[1].parts[0].explain.text` | Adding $P(A)$ and $P(B)$ counts $A \cap B$ twice. So $P(A \cup B) = 0.10 + 0.08 - 0.03 = 0.15$. | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[1].parts[1].question` | Using $P(A \cup B) = 0.15$, write $P(A \cup B \cup C)$ in terms of $t$. | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[1].parts[1].widget.answer` | 0.175+t | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[1].parts[1].widget.accept` | ["0.175+t", "t+0.175", "0.24-0.065+t", "0.15+0.06-0.035+t"] | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[1].parts[1].widget.wrong[0].tex` | 0.175-t | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[1].parts[1].widget.wrong[1].tex` | 0.21-t | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[1].parts[1].widget.wrong[2].tex` | 0.175 | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[1].parts[1].feedback.correct` | Split $C$ off: $0.15 + 0.06 - (0.02 + 0.015 - t) = 0.175 + t$. | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[1].parts[1].feedback.generic` | Not quite. Use $P(A \cup B) + P(C) - P((A \cup B) \cap C)$, and find the last term by the two... | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[1].parts[1].feedback.byKey.minus-t` | You took $t$ away. It is subtracted inside the bracket, so it comes back with a plus sign. | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[1].parts[1].feedback.byKey.whole-overlap` | You took $t$ as the whole of $(A \cup B) \cap C$. That event is $(A \cap C) \cup (B \cap C)$,... | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[1].parts[1].feedback.byKey.no-t` | That leaves out the triple overlap. After the pairs are taken away, the outcomes in all three... | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[1].parts[1].explain.text` | $(A \cup B) \cap C$ is $(A \cap C) \cup (B \cap C)$, with chance $0.02 + 0.015 - t$. So $P(A ... | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[1].parts[2].question` | In $0.175 + t$, the value of $t = P(A \cap B \cap C)$ is unknown. What is the largest value $... | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[1].parts[2].widget.answer` | 0.015 | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[1].parts[2].widget.accept` | 0.015: $A \cap B \cap C \subseteq B \cap C$, so $t \le 0.015$. | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[1].parts[2].widget.wrong[0].value` | 0.03 | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[1].parts[2].widget.wrong[1].value` | 0.06 | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[1].parts[2].widget.wrong[2].value` | 0.00048 | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[1].parts[2].feedback.correct` | $A \cap B \cap C$ lies inside $B \cap C$, so by monotonicity $t \le 0.015$. | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[1].parts[2].feedback.generic` | Not quite. The triple overlap is a subset of every pair overlap. | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[1].parts[2].feedback.byKey.largest-pair` | That is $P(A \cap B)$. The triple sits inside every pair, so it is capped by the smallest pair. | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[1].parts[2].feedback.byKey.smallest-single` | That is $P(C)$. The triple sits inside each pair too, and the pairs are smaller. | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[1].parts[2].feedback.byKey.product` | That is $0.10 \times 0.08 \times 0.06$, which assumes independence. Nothing says the downgrad... | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[1].parts[2].explain.text` | Monotonicity: $A \cap B \cap C \subseteq B \cap C$, so $t \le P(B \cap C) = 0.015$. With $t =... | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[1].parts[3].question` | Using $0.175 + t$ with the largest $t = 0.015$, what is the largest possible chance that at l... | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[1].parts[3].widget.answer` | 0.19 | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[1].parts[3].widget.accept` | 0.19: $0.175 + 0.015$. | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[1].parts[3].widget.wrong[0].value` | 0.24 | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[1].parts[3].widget.wrong[1].value` | 0.175 | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[1].parts[3].widget.wrong[2].value` | 0.205 | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[1].parts[3].feedback.correct` | $0.175 + 0.015 = 0.19$, so the chance lies between 0.175 and 0.19. | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[1].parts[3].feedback.generic` | Not quite. Put the largest $t$ into $0.175 + t$. | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[1].parts[3].feedback.byKey.singles` | That is $0.10 + 0.08 + 0.06$, the union bound. The reported pairs pull the true chance below it. | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[1].parts[3].feedback.byKey.smallest` | That is the value at $t = 0$, the smallest possible. The largest comes with the largest $t$. | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[1].parts[3].feedback.byKey.from-largest-pair` | That is $0.175 + 0.03$, from taking $t$ up to the largest pair. The triple cannot exceed 0.015. | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[1].parts[3].explain.text` | The chance rises with $t$, so its largest value is $0.175 + 0.015 = 0.19$. With $t$ between 0... | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[2].prose` | Five cards are dealt from a standard 52-card deck, every one of the $\binom{52}{5} = 2{,}598{... | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[2].parts[0].question` | How many hands hold no ace and no king? | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[2].parts[0].widget.answer` | 1086008 | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[2].parts[0].widget.accept` | 1,086,008 exactly: $\binom{44}{5}$. | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[2].parts[0].widget.wrong[0].value` | 1712304 | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[2].parts[0].widget.wrong[1].value` | 2118760 | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[2].parts[0].feedback.correct` | Take the 4 aces and 4 kings out: $\binom{44}{5} = 1{,}086{,}008$ hands. | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[2].parts[0].feedback.generic` | Not quite. Deal all 5 cards from the deck with every ace and king removed. | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[2].parts[0].feedback.byKey.no-ace-only` | That is $\binom{48}{5}$, which removes only the aces. Take the 4 kings out as well. | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[2].parts[0].feedback.byKey.one-each` | That is $\binom{50}{5}$, which removes one ace and one king. All 8 must go. | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[2].parts[0].explain.text` | A hand with no ace and no king takes all 5 cards from the other $52 - 8 = 44$. So there are $... | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[2].parts[1].question` | Using the 1,086,008 hands, what is $P(A \cup K)$, the chance of at least one ace or at least ... | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[2].parts[1].widget.answer` | 0.582137 | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[2].parts[1].widget.accept` | 0.5821: $1 - \tfrac{1{,}086{,}008}{2{,}598{,}960} = 0.58214$. | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[2].parts[1].widget.wrong[0].value` | 0.417863 | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[2].parts[1].widget.wrong[1].value` | 0.682316 | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[2].parts[1].feedback.correct` | The complement of $A \cup K$ is “no ace and no king”: $1 - 0.41786 = 0.58214$. | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[2].parts[1].feedback.generic` | Not quite. By De Morgan, “not ($A$ or $K$)” is “no ace and no king”. | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[2].parts[1].feedback.byKey.none` | That is the chance of no ace and no king. Take it from 1. | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[2].parts[1].feedback.byKey.added` | That is $P(A) + P(K)$, which counts hands with an ace and a king twice. | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[2].parts[1].explain.text` | By De Morgan, $(A \cup K)^c = A^c \cap K^c$, the hands with no ace and no king. So $P(A \cup ... | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[2].parts[2].question` | One hand in about three holds an ace: $P(A) = P(K) = 1 - \tfrac{\binom{48}{5}}{\binom{52}{5}}... | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[2].parts[2].widget.answer` | 0.100179 | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[2].parts[2].widget.accept` | 0.1002: $2 \times 0.341158 - 0.582137 = 0.10018$. | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[2].parts[2].widget.wrong[0].value` | 0.116389 | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[2].parts[2].widget.wrong[1].value` | 0.240979 | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[2].parts[2].feedback.correct` | Rearrange $P(A \cup K) = P(A) + P(K) - P(A \cap K)$: $0.682316 - 0.582137 = 0.10018$. | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[2].parts[2].feedback.generic` | Not quite. Rearrange inclusion and exclusion for $P(A \cap K)$. | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[2].parts[2].feedback.byKey.product` | That is $0.341158^2$, which treats $A$ and $K$ as independent. An ace in the hand leaves fewe... | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[2].parts[2].feedback.byKey.once` | That is $0.582137 - 0.341158$, with only one of the two singles. Inclusion and exclusion uses... | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[2].parts[2].explain.text` | Inclusion and exclusion gives $P(A \cap K) = P(A) + P(K) - P(A \cup K)$. That is $0.341158 + ... | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[2].parts[3].question` | There are 886,656 hands with at least one ace, the same number with at least one king, and $2... | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[2].parts[3].widget.answer` | 260360 | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[2].parts[3].widget.accept` | 260,360 exactly: $2 \times 886{,}656 - 1{,}512{,}952$. | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[2].parts[3].widget.wrong[0].value` | 1512952 | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[2].parts[3].widget.wrong[1].value` | 302490 | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[2].parts[3].widget.wrong[2].value` | 260361 | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[2].parts[3].feedback.correct` | $886{,}656 + 886{,}656 - 1{,}512{,}952 = 260{,}360$, which is $0.1002$ of all hands, as part ... | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[2].parts[3].feedback.generic` | Not quite. Rearrange inclusion and exclusion on the counts. | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[2].parts[3].feedback.byKey.union` | That is the count of hands with an ace or a king. Both must be present. | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[2].parts[3].feedback.byKey.from-product` | That is about $0.341158^2 \times 2{,}598{,}960 \approx 302{,}490$, from treating $A$ and $K$ ... | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[2].parts[3].feedback.byKey.from-chance` | You multiplied the rounded chance by the number of hands. Use the exact counts. | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[2].parts[3].explain.text` | Each count is the chance times 2,598,960: $/A/ = /K/ = 886{,}656$ and $/A \cup K/ = 1{,}512{,... | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[3].prose` | A short deck holds 20 cards: the ranks 10, J, Q, K and A in each of 4 suits. Four cards are d... | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[3].parts[0].question` | What is the chance the second card has a different rank from the first? Give an exact fractio... | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[3].parts[0].widget.answer` | 0.842105 | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[3].parts[0].widget.accept` | Any form equal to $\tfrac{16}{19}$, or 0.8421. | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[3].parts[0].widget.wrong[0].value` | 0.8 | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[3].parts[0].widget.wrong[1].value` | 0.157895 | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[3].parts[0].feedback.correct` | 19 cards are left, and 3 share the first card's rank: $\tfrac{16}{19}$. | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[3].parts[0].feedback.generic` | Not quite. After the first card, how many cards are left, and how many have another rank? | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[3].parts[0].feedback.byKey.replace` | That is $\tfrac{16}{20}$, with the first card put back. It stays out, so 19 cards are left. | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[3].parts[0].feedback.byKey.same` | That is $\tfrac{3}{19}$, the chance the ranks match. | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[3].parts[0].explain.text` | After the first card, 19 cards remain and 3 of them share its rank. So the second card has a ... | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[3].parts[1].question` | Using $\tfrac{16}{19}$ for the second card, what is the chance the first three cards have thr... | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[3].parts[1].widget.answer` | 0.561404 | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[3].parts[1].widget.accept` | Any form equal to $\tfrac{16}{19} \cdot \tfrac{12}{18} = \tfrac{32}{57}$, or 0.5614. | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[3].parts[1].widget.wrong[0].value` | 0.48 | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[3].parts[1].widget.wrong[1].value` | 0.531856 | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[3].parts[1].feedback.correct` | Two ranks are now taken, 8 cards, so 12 of the 18 left are new: $\tfrac{16}{19} \cdot \tfrac{... | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[3].parts[1].feedback.generic` | Not quite. The third card must avoid both ranks already dealt. | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[3].parts[1].feedback.byKey.replace` | That is $\tfrac{16}{20} \cdot \tfrac{12}{20}$, as if each card went back. The deck shrinks by... | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[3].parts[1].feedback.byKey.fixed-bottom` | That is $\tfrac{16}{19} \cdot \tfrac{12}{19}$, with 19 kept on the bottom. After two cards, 1... | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[3].parts[1].explain.text` | As in the birthday problem, each new card must avoid every rank already taken. Two ranks hold... | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[3].parts[2].question` | Using $\tfrac{32}{57}$ for three cards, what is the chance all four cards have different rank... | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[3].parts[2].widget.answer` | 0.26419 | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[3].parts[2].widget.accept` | Any form equal to $\tfrac{32}{57} \cdot \tfrac{8}{17} = \tfrac{256}{969}$, or 0.2642. | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[3].parts[2].widget.wrong[0].value` | 0.192 | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[3].parts[2].widget.wrong[1].value` | 0.223939 | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[3].parts[2].feedback.correct` | Three ranks hold 12 cards, so 8 of the 17 left are safe: $\tfrac{32}{57} \cdot \tfrac{8}{17} ... | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[3].parts[2].feedback.generic` | Not quite. The fourth card must avoid three ranks, 12 cards. | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[3].parts[2].feedback.byKey.replace` | That is $\tfrac{16}{20} \cdot \tfrac{12}{20} \cdot \tfrac{8}{20}$, dealing with replacement. ... | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[3].parts[2].feedback.byKey.fixed-bottom` | That is $\tfrac{16 \cdot 12 \cdot 8}{19^3}$, with 19 kept on the bottom. The deck has 17 left... | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[3].parts[2].explain.text` | With three ranks taken, 12 cards are ruled out, so 8 of the 17 cards left are safe. So the ch... | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[3].parts[3].question` | There are $\binom{20}{4} = 4845$ hands, all equally likely. Using $\tfrac{256}{969}$, how man... | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[3].parts[3].widget.answer` | 1280 | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[3].parts[3].widget.accept` | 1,280 exactly: $4845 \times \tfrac{256}{969}$, or $\binom{5}{4} \times 4^4$. | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[3].parts[3].widget.wrong[0].value` | 256 | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[3].parts[3].widget.wrong[1].value` | 30720 | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[3].parts[3].feedback.correct` | $4845 \times \tfrac{256}{969} = 1280$, which matches $\binom{5}{4} \times 4^4 = 5 \times 256$. | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[3].parts[3].feedback.generic` | Not quite. Multiply the 4845 hands by the chance. | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[3].parts[3].feedback.byKey.suits-only` | That is $4^4$, the suits for one set of four ranks. There are $\binom{5}{4} = 5$ sets of ranks. | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[3].parts[3].feedback.byKey.ordered` | That counts ordered deals, 1,280 times $4!$. A hand is the set of 4 cards. | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[3].parts[3].explain.text` | Every hand is equally likely, so the count is $4845 \times \tfrac{256}{969} = 1280$. In stage... | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[3].parts[4].question` | Of the rest, 320 are three of a kind and 5 four of a kind. Two pair needs 2 of the 5 ranks an... | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[3].parts[4].widget.answer` | 2880 | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[3].parts[4].widget.accept` | 2,880 exactly: $4845 - 1280 - 360 - 320 - 5$, with $\binom{5}{2}\binom{4}{2}^2 = 360$ two-pai... | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[3].parts[4].widget.wrong[0].value` | 3565 | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[3].parts[4].widget.wrong[1].value` | 2885 | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[3].parts[4].widget.wrong[2].value` | 2520 | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[3].parts[4].widget.wrong[3].value` | 3240 | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[3].parts[4].feedback.correct` | Two pair is $\binom{5}{2}\binom{4}{2}^2 = 360$, so $4845 - 1280 - 360 - 320 - 5 = 2880$, the ... | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[3].parts[4].feedback.generic` | Not quite. Count the two-pair hands, then take every other class from 4845. | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[3].parts[4].feedback.byKey.at-least-pair` | That is $4845 - 1280$, every hand with a repeated rank. Take off the other classes too. | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[3].parts[4].feedback.byKey.no-quads` | You left out the 5 four-of-a-kind hands. Every hand lies in exactly one class. | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[3].parts[4].feedback.byKey.two-pair-ordered` | You took 720 two-pair hands, counting the two pairs in order. The two pairs play the same rol... | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[3].parts[4].feedback.byKey.no-two-pair` | You left out the two-pair hands. They number $\binom{5}{2}\binom{4}{2}^2 = 360$ and belong to... | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
| problems-3 | `items[3].parts[4].explain.text` | Two pair picks 2 of the 5 ranks and 2 of the 4 suits for each: $10 \times 6 \times 6 = 360$. ... | correct | Ross 2.4, 2.5; enumerated, L3 script, short deck and all hands enumerated |
