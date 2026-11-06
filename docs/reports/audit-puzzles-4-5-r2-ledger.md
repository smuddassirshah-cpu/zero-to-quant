# Claim ledger: puzzles L4 to L5, concept audit round 2

One row per claim-bearing line (prose, hints, feedback lines, graded option texts, option and line `why`s, derive lines, explain, summary ideas, formula note and trap, `accept`, `how`, longform model and rubric) of l19 to l30, review-4, review-5, homework-4 and homework-5. Verdicts: correct, wrong, imprecise, misleading, unverified. Basis: each file section opens with a basis table keyed by screen or item; a row's basis is that key (`B:<key>`) unless the row carries its own text. Bases are a named source with chapter or section, a derivation, or `sim: <script>:<check name>` where the scripts are `docs/reports/puzzles-L4-concepts-r2.py` (`L4`) and `puzzles-L5-concepts-r2.py` (`L5`) and the check name is the text of the assert message. Written during the blind phase, before any earlier review was read.


## l19-who-wins.json

### Bases

| key | basis |
|---|---|
| screens[0] | reading list, not a claim |
| screens[1] | Berlekamp, Conway and Guy, Winning Ways vol. 1 ch. 2 (subtraction games, P-positions); sim: puzzles-L4-concepts-r2.py:losing piles with takes 1..3 are the multiples of 4; from 21 take 1; from 17 take 1 |
| screens[2] | Berlekamp, Conway and Guy, Winning Ways vol. 1 ch. 2 (subtraction games, P-positions); sim: puzzles-L4-concepts-r2.py:losing piles with takes 1..3 are the multiples of 4; from 21 take 1; from 17 take 1 |
| quiz[1] | Berlekamp, Conway and Guy, Winning Ways vol. 1 ch. 2 (subtraction games, P-positions); sim: puzzles-L4-concepts-r2.py:losing piles with takes 1..3 are the multiples of 4; from 21 take 1; from 17 take 1 |
| screens[3] | Ross, A First Course in Probability ch. 3 (conditioning on the first trial); derivation x = 1/6 + (25/36)x; sim: puzzles-L4-concepts-r2.py:first six wins: 6/11; MC two players |
| quiz[2] | Ross, A First Course in Probability ch. 3 (conditioning on the first trial); derivation x = 1/6 + (25/36)x; sim: puzzles-L4-concepts-r2.py:first six wins: 6/11; MC two players |
| screens[4] | derivation x = 1/2 + x/4; sim: puzzles-L4-concepts-r2.py:first head wins: 2/3 |
| screens[5] | Berlekamp, Conway and Guy, Winning Ways vol. 1 ch. 2 (subtraction games, P-positions); sim: puzzles-L4-concepts-r2.py:20 loses for the mover; copying fails: 18 winning, 16 losing |
| screens[6] | Berlekamp, Conway and Guy, Winning Ways vol. 1 ch. 2 (subtraction games, P-positions); sim: puzzles-L4-concepts-r2.py:losing piles with takes 1..k are multiples of k+1; p/(1-(1-p)^2) = 1/(2-p) |
| screens[7] | derivation; sim: puzzles-L4-concepts-r2.py:1/(2-p) > 1/2 for every p in (0,1]; g'' sign not needed |
| screens[8] | Berlekamp, Conway and Guy, Winning Ways vol. 1 ch. 2 (subtraction games, P-positions); sim: puzzles-L4-concepts-r2.py:30 with takes 1..4 loses whatever you take |
| screens[9] | sim: puzzles-L4-concepts-r2.py:first 1 or 2 wins: 3/5; duel 1/2 vs 1/3: 3/4; from 23 take 3 |
| screens[10] | derivation x = (1/6)/(1-(5/6)^3); sim: puzzles-L4-concepts-r2.py:three players first six: 36/91; B 30/91, C 25/91; MC; stretch 1/(3-p) = 0.3529 |
| screens[11] | Vickrey (1961); Krishna, Auction Theory ch. 2 (truthful bidding weakly dominant under private values, stated "worth £100 to you"); sim: puzzles-L4-concepts-r2.py:second-price auction grid 0..200 |
| summary | Berlekamp, Conway and Guy, Winning Ways vol. 1 ch. 2 (subtraction games, P-positions); sim: puzzles-L4-concepts-r2.py:four players 216/671 (n-player formula) |
| quiz[0] | symmetry under swapping players; sim: puzzles-L4-concepts-r2.py:simultaneous roll 15/36 per roll, 1/2 overall |
| quiz[3] | sim: puzzles-L4-concepts-r2.py:24 loses with takes 1..5; 20, 25, 28 do not |

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l19-who-wins.json | `.screens[0].prose` | Games reward one habit: work back from the end. The same books, easiest first: - Mosteller, *Fifty Challenging Problems… | correct | B:screens[0] |
| l19-who-wins.json | `.screens[1].prose` | Two players take turns to remove 1, 2 or 3 matches from a pile. Whoever takes the last match wins. Work up from small p… | correct | B:screens[1] |
| l19-who-wins.json | `.screens[1].hints[0].text` | With 1, 2 or 3 matches you take them all and win. | correct | B:screens[1] |
| l19-who-wins.json | `.screens[1].hints[1].text` | With 4, every move leaves 1, 2 or 3 for your rival. | correct | B:screens[1] |
| l19-who-wins.json | `.screens[1].hints[2].text` | A pile loses when every move leads to a winning pile. Check 5 to 8, then 9 to 12. | correct | B:screens[1] |
| l19-who-wins.json | `.screens[1].feedback.correct` | 4, 8 and 12: the multiples of 4. | correct | B:screens[1] |
| l19-who-wins.json | `.screens[1].feedback.generic` | Not quite right. Label 1 to 3 first, then work upwards. | correct | B:screens[1] |
| l19-who-wins.json | `.screens[1].feedback.byKey.evens` | You marked every even pile. From 2 you take both matches and win. | correct | B:screens[1] |
| l19-who-wins.json | `.screens[1].feedback.byKey.r1c2` | From 2 you take both matches and win. | correct | B:screens[1] |
| l19-who-wins.json | `.screens[1].feedback.byKey.r2c1` | From 5 you take 1 and hand your rival 4. | correct | B:screens[1] |
| l19-who-wins.json | `.screens[1].explain.text` | From 4, every move leaves 1, 2 or 3, and your rival takes the rest. From 5, 6 or 7 you move to 4 and win. The pattern r… | correct | B:screens[1] |
| l19-who-wins.json | `.screens[2].prose` | Now the pile holds 21 matches, with the same rules. You move first. | correct | B:screens[2] |
| l19-who-wins.json | `.screens[2].hints[0].text` | Which losing pile can you hand your rival? | correct | B:screens[2] |
| l19-who-wins.json | `.screens[2].hints[1].text` | 20 is a multiple of 4. | correct | B:screens[2] |
| l19-who-wins.json | `.screens[2].hints[2].text` | Take 1. After any take of $x$, reply with $4 - x$. | correct | B:screens[2] |
| l19-who-wins.json | `.screens[2].feedback.correct` | Take 1 and leave 20. | correct | B:screens[2] |
| l19-who-wins.json | `.screens[2].feedback.generic` | Not quite right. Find the multiple of 4 just below 21. | correct | B:screens[2] |
| l19-who-wins.json | `.screens[2].feedback.byKey.three` | Taking 3 leaves 18. Your rival takes 2 and hands you 16. | correct | B:screens[2] |
| l19-who-wins.json | `.screens[2].feedback.byKey.two` | Taking 2 leaves 19. Your rival takes 3 and hands you 16. | correct | B:screens[2] |
| l19-who-wins.json | `.screens[2].explain.text` | Taking 1 leaves 20, a losing pile for your rival. After each take of $x$ you take $4 - x$, so the pile runs 20, 16, 12 … | correct | B:screens[2] |
| l19-who-wins.json | `.screens[3].prose` | Two players take turns to roll a fair die, A first. The first to roll a six wins. Label the states and look one round a… | correct | B:screens[3] |
| l19-who-wins.json | `.screens[3].widget.accept` | 6/11, about 0.5455 | correct | B:screens[3] |
| l19-who-wins.json | `.screens[3].hints[0].text` | Let $x = P(\text{A wins})$, from the state where A rolls. | correct | B:screens[3] |
| l19-who-wins.json | `.screens[3].hints[1].text` | A wins now with $\tfrac16$. Both miss with $\tfrac{25}{36}$, and we are back at the start. | correct | B:screens[3] |
| l19-who-wins.json | `.screens[3].hints[2].text` | $x = \tfrac16 + \tfrac{25}{36}x$, so $x = \tfrac{6}{11}$. | correct | B:screens[3] |
| l19-who-wins.json | `.screens[3].feedback.correct` | $x = \tfrac{6}{11} \approx 0.5455$. | correct | B:screens[3] |
| l19-who-wins.json | `.screens[3].feedback.generic` | Not quite right. Write one equation for a round: A hits, or both miss and it restarts. | correct | B:screens[3] |
| l19-who-wins.json | `.screens[3].feedback.byKey.half` | You split it evenly. A rolls first, so A has the first chance in every round. | correct | B:screens[3] |
| l19-who-wins.json | `.screens[3].feedback.byKey.once` | That is A's chance on the first roll only. If both miss, A rolls again. | correct | B:screens[3] |
| l19-who-wins.json | `.screens[3].feedback.byKey.b` | That is B's chance, $\tfrac{5}{11}$. | correct | B:screens[3] |
| l19-who-wins.json | `.screens[3].explain.text` | A wins at once with $\tfrac16$, or both miss with $\tfrac{25}{36}$ and the game restarts. So $x = \tfrac16 + \tfrac{25}… | correct | B:screens[3] |
| l19-who-wins.json | `.screens[4].prose` | The same chain with a coin: players flip in turn, and the first head wins. You may choose your seat. | correct | B:screens[4] |
| l19-who-wins.json | `.screens[4].widget.accept` | 2/3, about 0.6667 | correct | B:screens[4] |
| l19-who-wins.json | `.screens[4].hints[0].text` | Use the same one-round argument. | correct | B:screens[4] |
| l19-who-wins.json | `.screens[4].hints[1].text` | The first player wins now with $\tfrac12$. Both miss with $\tfrac14$. | correct | B:screens[4] |
| l19-who-wins.json | `.screens[4].hints[2].text` | $x = \tfrac12 + \tfrac14 x$, so $x = \tfrac23$. | correct | B:screens[4] |
| l19-who-wins.json | `.screens[4].feedback.correct` | $\tfrac23$: take the first seat. | correct | B:screens[4] |
| l19-who-wins.json | `.screens[4].feedback.generic` | Not quite right. Write $x$ = win now, plus both miss times $x$. | correct | B:screens[4] |
| l19-who-wins.json | `.screens[4].feedback.byKey.half` | You split it evenly. The first player has the first chance in every round. | correct | B:screens[4] |
| l19-who-wins.json | `.screens[4].feedback.byKey.second` | That is the second seat's chance. | correct | B:screens[4] |
| l19-who-wins.json | `.screens[4].explain.text` | $x = \tfrac12 + \tfrac14 x$ gives $x = \tfrac23$. The first seat is worth twice the second. Value both seats before you… | correct | B:screens[4] |
| l19-who-wins.json | `.screens[5].prose` | Trading firms ask this one. The take-away game starts from 20 matches, with takes of 1, 2 or 3. The last match wins. | correct | B:screens[5] |
| l19-who-wins.json | `.screens[5].widget.options[0].text` | Second: 20 is a multiple of 4, so the mover loses | correct | B:screens[5] |
| l19-who-wins.json | `.screens[5].widget.options[1].why` | You carried over the coin game. Here every first move leaves 17, 18 or 19, and your rival hands back 16. | correct | B:screens[5] |
| l19-who-wins.json | `.screens[5].widget.options[2].why` | Copying fails: after takes of 1 and 1 the pile is 18. The first player takes 2 and leaves 16. The reply that works is $… | correct | B:screens[5] |
| l19-who-wins.json | `.screens[5].widget.options[3].why` | There is no luck here. Best play decides it, and 20 loses for the mover. | correct | B:screens[5] |
| l19-who-wins.json | `.screens[5].hints[0].text` | Value both seats before choosing. | correct | B:screens[5] |
| l19-who-wins.json | `.screens[5].hints[1].text` | Is 20 a winning or a losing pile for the mover? | correct | B:screens[5] |
| l19-who-wins.json | `.screens[5].hints[2].text` | 20 is a multiple of 4, so the mover loses. | correct | B:screens[5] |
| l19-who-wins.json | `.screens[5].feedback.correct` | Second. Answer each take of $x$ with $4 - x$. | correct | B:screens[5] |
| l19-who-wins.json | `.screens[5].feedback.generic` | Not quite right. Label the pile of 20 for the player to move. | correct | B:screens[5] |
| l19-who-wins.json | `.screens[5].feedback.byKey.b` | You carried over the coin game, where the first seat won. Here every first move hands your rival a winning pile. | correct | B:screens[5] |
| l19-who-wins.json | `.screens[5].feedback.byKey.c` | Copying fails: after 1 and 1 the pile is 18, and the first player leaves you 16. The working reply is $4 - x$. | correct | B:screens[5] |
| l19-who-wins.json | `.screens[5].explain.text` | From 20, every move leaves a pile your rival turns into 16. So the second seat wins, replying $4 - x$ each time. The se… | correct | B:screens[5] |
| l19-who-wins.json | `.screens[6].prose` | Every answer came from the end of the game. This is **backward induction**: a position loses for the mover when every m… | correct | B:screens[6] |
| l19-who-wins.json | `.screens[6].widget.options[0].text` | Multiples of 6 | correct | B:screens[6] |
| l19-who-wins.json | `.screens[6].widget.options[1].why` | You used the largest take. From 5 you take all five and win. | correct | B:screens[6] |
| l19-who-wins.json | `.screens[6].widget.options[2].why` | That is the rule for takes of 1 to 3. | correct | B:screens[6] |
| l19-who-wins.json | `.screens[6].hints[0].text` | Piles 1 to 5 win: you take them all. | correct | B:screens[6] |
| l19-who-wins.json | `.screens[6].hints[1].text` | From 6, every move leaves 1 to 5. | correct | B:screens[6] |
| l19-who-wins.json | `.screens[6].hints[2].text` | So 6, 12, 18 and so on lose. | correct | B:screens[6] |
| l19-who-wins.json | `.screens[6].feedback.correct` | Multiples of 6: answer a take of $x$ with $6 - x$. | correct | B:screens[6] |
| l19-who-wins.json | `.screens[6].feedback.generic` | Not quite right. Label piles 1 to 6 first. | correct | B:screens[6] |
| l19-who-wins.json | `.screens[6].explain.text` | With takes of 1 to $k$, the losing piles are the multiples of $k + 1$. You answer a take of $x$ with $k + 1 - x$. | correct | B:screens[6] |
| l19-who-wins.json | `.screens[7].prose` | Players alternate, and each turn succeeds with chance $p$. Derive the first player's chance $x$, one justified line at … | correct | B:screens[7] |
| l19-who-wins.json | `.screens[7].widget.lines[0].text` | Look at one round, from the first player's turn. | correct | B:screens[7] |
| l19-who-wins.json | `.screens[7].widget.lines[1].text` | The first player succeeds at once with chance $p$. | correct | B:screens[7] |
| l19-who-wins.json | `.screens[7].widget.lines[2].text` | Both miss with chance $(1 - p)^2$, and the game starts afresh. | correct | B:screens[7] |
| l19-who-wins.json | `.screens[7].widget.lines[3].text` | So $x = p + (1 - p)^2 x$. | correct | B:screens[7] |
| l19-who-wins.json | `.screens[7].widget.lines[4].text` | Collect $x$: $x\,[1 - (1 - p)^2] = p$, and $1 - (1 - p)^2 = p(2 - p)$. | correct | B:screens[7] |
| l19-who-wins.json | `.screens[7].widget.lines[5].text` | So $x = \dfrac{1}{2 - p}$, which gives $\tfrac{6}{11}$ at $p = \tfrac16$. | correct | B:screens[7] |
| l19-who-wins.json | `.screens[7].widget.lines[6].text` | Turns alternate, so each player wins with chance $\tfrac12$. | correct | B:screens[7] |
| l19-who-wins.json | `.screens[7].widget.lines[6].why` | That is the blurted answer. The first player has the first chance in every round. | correct | B:screens[7] |
| l19-who-wins.json | `.screens[7].hints[0].text` | Start from one round. | correct | B:screens[7] |
| l19-who-wins.json | `.screens[7].hints[1].text` | A round ends in a win now, or it restarts. | correct | B:screens[7] |
| l19-who-wins.json | `.screens[7].hints[2].text` | Round, two cases, equation, algebra, answer. | correct | B:screens[7] |
| l19-who-wins.json | `.screens[7].feedback.correct` | One round, one equation, one answer: $\tfrac{1}{2 - p}$. | correct | B:screens[7] |
| l19-who-wins.json | `.screens[7].feedback.generic` | Not quite right. Begin with the round and its two cases. | correct | B:screens[7] |
| l19-who-wins.json | `.screens[7].feedback.byKey.d1` | Alternating turns are not a fair split. The first player has the first chance in every round. | correct | B:screens[7] |
| l19-who-wins.json | `.screens[7].feedback.byKey.left-out` | Every line except the even split belongs. | correct | B:screens[7] |
| l19-who-wins.json | `.screens[7].feedback.byKey.s6` | The answer comes last. | correct | B:screens[7] |
| l19-who-wins.json | `.screens[7].explain.text` | A round either ends the game or resets it. That gives one linear equation in $x$. Its solution $\tfrac{1}{2 - p}$ is ab… | correct | B:screens[7] |
| l19-who-wins.json | `.screens[8].prose` | Drill: about 3 minutes a puzzle, as interviews allow. Keep your own time and say each argument aloud. A pile holds 30 m… | correct | B:screens[8] |
| l19-who-wins.json | `.screens[8].widget.options[0].why` | Taking 1 leaves 29. Your rival takes 4 and hands you 25, a multiple of 5. | correct | B:screens[8] |
| l19-who-wins.json | `.screens[8].widget.options[1].why` | Taking 2 leaves 28. Your rival takes 3 and hands you 25. | correct | B:screens[8] |
| l19-who-wins.json | `.screens[8].widget.options[2].why` | Taking 3 leaves 27. Your rival takes 2 and hands you 25. | correct | B:screens[8] |
| l19-who-wins.json | `.screens[8].widget.options[3].why` | Taking 4 leaves 26. Your rival takes 1 and hands you 25. | correct | B:screens[8] |
| l19-who-wins.json | `.screens[8].widget.options[4].text` | No move wins: 30 is a multiple of 5, so you lose against best play | correct | B:screens[8] |
| l19-who-wins.json | `.screens[8].hints[0].text` | With takes of 1 to 4, which piles lose? | correct | B:screens[8] |
| l19-who-wins.json | `.screens[8].hints[1].text` | Multiples of 5 lose for the mover. | correct | B:screens[8] |
| l19-who-wins.json | `.screens[8].hints[2].text` | 30 is a multiple of 5. | correct | B:screens[8] |
| l19-who-wins.json | `.screens[8].feedback.correct` | No move wins: 30 is a losing pile. | correct | B:screens[8] |
| l19-who-wins.json | `.screens[8].feedback.generic` | Not quite right. Find the losing piles for takes of 1 to 4. | correct | B:screens[8] |
| l19-who-wins.json | `.screens[8].explain.text` | With takes of 1 to 4 the losing piles are the multiples of 5. 30 is one, so every move hands your rival a winning pile.… | correct | B:screens[8] |
| l19-who-wins.json | `.screens[9].prose` | Three more, at about 3 minutes each. Give four decimal places. | correct | B:screens[9] |
| l19-who-wins.json | `.screens[9].hints[0].text` | Each is one round and one equation, or a pile size against $k + 1$. | correct | B:screens[9] |
| l19-who-wins.json | `.screens[9].hints[1].text` | In the duel, a round ends with nobody hit with chance $\tfrac12 \times \tfrac23 = \tfrac13$. | correct | B:screens[9] |
| l19-who-wins.json | `.screens[9].hints[2].text` | $\tfrac{1/3}{1 - 4/9}$, then $\tfrac{1/2}{1 - 1/3}$, then $23 = 5 \times 4 + 3$. | correct | B:screens[9] |
| l19-who-wins.json | `.screens[9].feedback.correct` | $0.6$, $0.75$ and $3$. | correct | B:screens[9] |
| l19-who-wins.json | `.screens[9].feedback.generic` | Not quite right. Check the first answer that is marked. | correct | B:screens[9] |
| l19-who-wins.json | `.screens[9].feedback.byKey.r0c1` | Check the dice: $p = \tfrac13$, so $x = \tfrac{1}{2 - 1/3}$. | correct | B:screens[9] |
| l19-who-wins.json | `.screens[9].feedback.byKey.r1c1` | Check the duel: $x = \tfrac12 + \tfrac13 x$. | correct | B:screens[9] |
| l19-who-wins.json | `.screens[9].feedback.byKey.r2c1` | Check the pile: leave a multiple of 4. | correct | B:screens[9] |
| l19-who-wins.json | `.screens[9].explain.text` | For the dice, $\tfrac{1}{2 - 1/3} = \tfrac35$. The duel gives $\tfrac{1/2}{2/3} = \tfrac34$. From 23, take 3 to leave 2… | correct | B:screens[9] |
| l19-who-wins.json | `.screens[10].prose` | You gave $\tfrac{6}{11}$ for two players. The interviewer adds a third. A, B and C roll in turn, and the first six wins. | correct | B:screens[10] |
| l19-who-wins.json | `.screens[10].widget.accept` | 36/91, about 0.3956 | correct | B:screens[10] |
| l19-who-wins.json | `.screens[10].hints[0].text` | One round is now three rolls. | correct | B:screens[10] |
| l19-who-wins.json | `.screens[10].hints[1].text` | A round ends with no six with chance $(\tfrac56)^3 = \tfrac{125}{216}$. | correct | B:screens[10] |
| l19-who-wins.json | `.screens[10].hints[2].text` | $x = \tfrac16 + \tfrac{125}{216}x$, so $x = \tfrac{36}{91}$. | correct | B:screens[10] |
| l19-who-wins.json | `.screens[10].feedback.correct` | $\tfrac{36}{91} \approx 0.3956$. | correct | B:screens[10] |
| l19-who-wins.json | `.screens[10].feedback.generic` | Not quite right. Redo the round with three rolls. | correct | B:screens[10] |
| l19-who-wins.json | `.screens[10].feedback.byKey.third` | You split it evenly. Each seat is worth $\tfrac56$ of the seat before it. | correct | B:screens[10] |
| l19-who-wins.json | `.screens[10].feedback.byKey.two` | That is the two-player answer. A third player takes a share. | correct | B:screens[10] |
| l19-who-wins.json | `.screens[10].feedback.byKey.stretch` | You stretched $\tfrac{1}{2 - p}$ to $\tfrac{1}{3 - p}$. Redo the round: it ends with no six with chance $(\tfrac56)^3$. | correct | B:screens[10] |
| l19-who-wins.json | `.screens[10].explain.text` | A round ends with no six with chance $\tfrac{125}{216}$. So $x = \tfrac{1/6}{91/216} = \tfrac{36}{91} \approx 0.3956$. … | correct | B:screens[10] |
| l19-who-wins.json | `.screens[11].prose` | A bank sells a block of bonds by sealed bids. The highest bid wins and pays the second-highest bid. The block is worth … | correct | B:screens[11] |
| l19-who-wins.json | `.screens[11].widget.options[0].text` | £100, your value | correct | B:screens[11] |
| l19-who-wins.json | `.screens[11].widget.options[1].why` | Your bid only decides whether you win; the price is the other bid. Shading it loses auctions you would have won at a pr… | correct | B:screens[11] |
| l19-who-wins.json | `.screens[11].widget.options[2].why` | The extra wins come when the other bid is above £100. Then you pay more than the block is worth. | correct | B:screens[11] |
| l19-who-wins.json | `.screens[11].widget.options[3].why` | You tried to read the rival. Your bid does not set your price, so the guess gains nothing. | correct | B:screens[11] |
| l19-who-wins.json | `.screens[11].hints[0].text` | What does your bid change, and what sets the price? | correct | B:screens[11] |
| l19-who-wins.json | `.screens[11].hints[1].text` | Your bid decides whether you win. The price is the other bid. | correct | B:screens[11] |
| l19-who-wins.json | `.screens[11].hints[2].text` | Check the cases: the other bid below £100, and above it. | correct | B:screens[11] |
| l19-who-wins.json | `.screens[11].feedback.correct` | Bid your value, £100. | correct | B:screens[11] |
| l19-who-wins.json | `.screens[11].feedback.generic` | Not quite right. Compare your bid with £100 for each possible rival bid. | correct | B:screens[11] |
| l19-who-wins.json | `.screens[11].feedback.byKey.b` | Shading your bid never lowers your price. It only loses auctions you would have won at a profit. | correct | B:screens[11] |
| l19-who-wins.json | `.screens[11].explain.text` | Go through every rival bid, as you went through every reply in the take-away game. Bidding £100 wins exactly when the p… | correct | B:screens[11] |
| l19-who-wins.json | `.summary.ideas[0]` | Work back from the end: a position loses for the mover when every move leads to a winning one. | correct | B:summary |
| l19-who-wins.json | `.summary.ideas[1]` | In take-away with takes of 1 to $k$, the multiples of $k + 1$ lose for the mover. | correct | B:summary |
| l19-who-wins.json | `.summary.ideas[2]` | When turns alternate, one round gives one equation: the first player wins with $\tfrac{1}{2 - p}$. | correct | B:summary |
| l19-who-wins.json | `.summary.formula.note` | With $n$ players in turn, $x = \dfrac{p}{1 - (1 - p)^n}$. | correct | B:summary |
| l19-who-wins.json | `.summary.trap` | Answering $\tfrac12$ because turns alternate. The first seat has the first chance in every round. | correct | B:summary |
| l19-who-wins.json | `.quiz[0].prose` | Two players roll a die at the same time. The higher roll wins, and a tie means both roll again. | correct | B:quiz[0] |
| l19-who-wins.json | `.quiz[0].widget.options[0].text` | $\tfrac12$ | correct | B:quiz[0] |
| l19-who-wins.json | `.quiz[0].widget.options[1].why` | That is the chance of winning one roll. Ties roll again, so divide by $\tfrac{30}{36}$. | correct | B:quiz[0] |
| l19-who-wins.json | `.quiz[0].widget.options[2].why` | That formula is for turns. Here both roll at once, so the seats are the same. | correct | B:quiz[0] |
| l19-who-wins.json | `.quiz[0].feedback.correct` | $\tfrac12$: the seat does not matter. | correct | B:quiz[0] |
| l19-who-wins.json | `.quiz[0].feedback.generic` | Not quite right. Swap the two players: what changes? | correct | B:quiz[0] |
| l19-who-wins.json | `.quiz[0].explain.text` | Swap the players and nothing changes, so each wins with $\tfrac12$. Directly, $\tfrac{15/36}{30/36} = \tfrac12$. This i… | correct | B:quiz[0] |
| l19-who-wins.json | `.quiz[1].prose` | Takes of 1 to 3 from 17 matches, and the last match wins. You move first. | correct | B:quiz[1] |
| l19-who-wins.json | `.quiz[1].feedback.correct` | Take 1 and leave 16. | correct | B:quiz[1] |
| l19-who-wins.json | `.quiz[1].feedback.generic` | Not quite right. Leave a multiple of 4. | correct | B:quiz[1] |
| l19-who-wins.json | `.quiz[1].feedback.byKey.three` | Taking 3 leaves 14. Your rival takes 2 and hands you 12. | correct | B:quiz[1] |
| l19-who-wins.json | `.quiz[1].explain.text` | $17 = 4 \times 4 + 1$. Take 1 to leave 16, then answer each $x$ with $4 - x$. | correct | B:quiz[1] |
| l19-who-wins.json | `.quiz[2].prose` | Players alternate rolls of a die, and the first six wins. | correct | B:quiz[2] |
| l19-who-wins.json | `.quiz[2].widget.accept` | 5/11, about 0.4545 | correct | B:quiz[2] |
| l19-who-wins.json | `.quiz[2].feedback.correct` | $\tfrac{5}{11} \approx 0.4545$. | correct | B:quiz[2] |
| l19-who-wins.json | `.quiz[2].feedback.generic` | Not quite right. Find the first player's chance, then take it from 1. | correct | B:quiz[2] |
| l19-who-wins.json | `.quiz[2].feedback.byKey.half` | Alternating is not an even split. The first player has the first chance each round. | correct | B:quiz[2] |
| l19-who-wins.json | `.quiz[2].feedback.byKey.first` | That is the first player's chance. | correct | B:quiz[2] |
| l19-who-wins.json | `.quiz[2].explain.text` | The first player has $\tfrac{6}{11}$, so the second has $\tfrac{5}{11} \approx 0.4545$. The second seat is worth $\tfra… | correct | B:quiz[2] |
| l19-who-wins.json | `.quiz[3].prose` | Takes of 1 to 5, and the last match wins. | correct | B:quiz[3] |
| l19-who-wins.json | `.quiz[3].widget.options[0].text` | 24 | correct | B:quiz[3] |
| l19-who-wins.json | `.quiz[3].widget.options[1].why` | From 25 you take 1 and leave 24. | correct | B:quiz[3] |
| l19-who-wins.json | `.quiz[3].widget.options[2].why` | 20 is a multiple of 5, but with takes of 1 to 5 the losing piles are multiples of 6. | correct | B:quiz[3] |
| l19-who-wins.json | `.quiz[3].widget.options[3].why` | From 28 you take 4 and leave 24. | correct | B:quiz[3] |
| l19-who-wins.json | `.quiz[3].feedback.correct` | 24, a multiple of 6. | correct | B:quiz[3] |
| l19-who-wins.json | `.quiz[3].feedback.generic` | Not quite right. Use the multiples of $k + 1$. | correct | B:quiz[3] |
| l19-who-wins.json | `.quiz[3].explain.text` | With takes of 1 to 5 the losing piles are the multiples of 6. 24 is one; from each of the others you can reach 24. | correct | B:quiz[3] |

## l20-betting-on-sequences.json

### Bases

| key | basis |
|---|---|
| screens[0] | Feller vol. 1 XIII.7 (recurrent patterns, waiting times) and GKP Concrete Mathematics 8.4 (Penney, Conway leading numbers); sim: puzzles-L4-concepts-r2.py:P(TH before HH) = 3/4; biased coin TH before HH 5/9; MC biased |
| screens[8] | Feller vol. 1 XIII.7 (recurrent patterns, waiting times) and GKP Concrete Mathematics 8.4 (Penney, Conway leading numbers); sim: puzzles-L4-concepts-r2.py:P(TH before HH) = 3/4; biased coin TH before HH 5/9; MC biased |
| screens[1] | Feller vol. 1 XIII.7 (recurrent patterns, waiting times) and GKP Concrete Mathematics 8.4 (Penney, Conway leading numbers); sim: puzzles-L4-concepts-r2.py:P(THH before HHT) = 3/4 |
| screens[2] | Ross, A First Course in Probability ch. 3 (conditioning on the first trial); node equations x_HH=1, x_HT=x_0/2, x_0=x_H; sim: puzzles-L4-concepts-r2.py:P(HHT before HTH) = 2/3 (automaton and Conway); MC; P(HHT before HTT) = 2/3 |
| screens[5] | Ross, A First Course in Probability ch. 3 (conditioning on the first trial); node equations x_HH=1, x_HT=x_0/2, x_0=x_H; sim: puzzles-L4-concepts-r2.py:P(HHT before HTH) = 2/3 (automaton and Conway); MC; P(HHT before HTT) = 2/3 |
| quiz[1] | Ross, A First Course in Probability ch. 3 (conditioning on the first trial); node equations x_HH=1, x_HT=x_0/2, x_0=x_H; sim: puzzles-L4-concepts-r2.py:P(HHT before HTH) = 2/3 (automaton and Conway); MC; P(HHT before HTT) = 2/3 |
| screens[3] | Feller vol. 1 XIII.7 (recurrent patterns, waiting times) and GKP Concrete Mathematics 8.4 (Penney, Conway leading numbers); sim: puzzles-L4-concepts-r2.py:HTH waits 10, HHT 8; even money on HTH loses 1/3 per £1; 2 to 1 is fair |
| screens[4] | Feller vol. 1 XIII.7 (recurrent patterns, waiting times) and GKP Concrete Mathematics 8.4 (Penney, Conway leading numbers) (Conway formula, odds B:A = (AA-AB):(BB-BA)); sim: puzzles-L4-concepts-r2.py:HTH.HTH=5, HHT.HHT=4, HHT.HTH=2, HTH.HHT=1; all 21 pairs agree with the automaton |
| summary | Feller vol. 1 XIII.7 (recurrent patterns, waiting times) and GKP Concrete Mathematics 8.4 (Penney, Conway leading numbers) (Conway formula, odds B:A = (AA-AB):(BB-BA)); sim: puzzles-L4-concepts-r2.py:HTH.HTH=5, HHT.HHT=4, HHT.HTH=2, HTH.HHT=1; all 21 pairs agree with the automaton |
| screens[6] | sim: puzzles-L4-concepts-r2.py:solution passes all 10 hidden tests; seed 1 share 0.6640; SE sqrt(2/9/20000)=0.0033; tolerance 0.0092 is three SE |
| screens[7] | sim: puzzles-L4-concepts-r2.py:P(HTT before TTH) = 3/4; P(THH before HHH) = 7/8; odds against HTH 2 to 1 |
| screens[9] | Hoehn and Niven (1985) and Gardner, Penney-ante (Sci. Am. 1974); sim: puzzles-L4-concepts-r2.py:choose-second rule wins at least 2/3 against every three-flip pattern; HHT beats THT 5/8; HTH vs THT 1/2; TTT vs THT 2/5; £3.33 a game |
| quiz[0] | symmetry H<->T; sim: puzzles-L4-concepts-r2.py:P(HT before TH) = 1/2 |
| quiz[2] | sim: puzzles-L4-concepts-r2.py:fair odds on HH are 3 to 1 (expected gain 0) |

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l20-betting-on-sequences.json | `.screens[0].prose` | Flip a fair coin until HH or TH appears. Each node records how much of a pattern you have built. Follow the arrows. | correct | B:screens[0] |
| l20-betting-on-sequences.json | `.screens[0].widget.accept` | 3/4 | correct | B:screens[0] |
| l20-betting-on-sequences.json | `.screens[0].hints[0].text` | What happens once the first T appears? | correct | B:screens[0] |
| l20-betting-on-sequences.json | `.screens[0].hints[1].text` | From T, the first H completes TH. HH would need two heads. | correct | B:screens[0] |
| l20-betting-on-sequences.json | `.screens[0].hints[2].text` | HH wins only if flips 1 and 2 are both heads: $\tfrac14$. | correct | B:screens[0] |
| l20-betting-on-sequences.json | `.screens[0].feedback.correct` | $\tfrac34$: TH wins unless the game opens HH. | correct | B:screens[0] |
| l20-betting-on-sequences.json | `.screens[0].feedback.generic` | Not quite right. Follow the arrows out of node T. | correct | B:screens[0] |
| l20-betting-on-sequences.json | `.screens[0].feedback.byKey.half` | Both patterns have chance $\tfrac14$ in two flips, but this is a race. Once a T shows, TH must come first. | correct | B:screens[0] |
| l20-betting-on-sequences.json | `.screens[0].feedback.byKey.quarter` | That is HH's chance. | correct | B:screens[0] |
| l20-betting-on-sequences.json | `.screens[0].explain.text` | HH can only win on flips 1 and 2. Any T before that means the next H completes TH first. So TH wins with $1 - \tfrac14 … | correct | B:screens[0] |
| l20-betting-on-sequences.json | `.screens[1].prose` | Now the race is HHT against THH. The chain has more nodes, but the same idea works. | correct | B:screens[1] |
| l20-betting-on-sequences.json | `.screens[1].widget.accept` | 3/4 | correct | B:screens[1] |
| l20-betting-on-sequences.json | `.screens[1].hints[0].text` | Once HH appears, what must happen next? | correct | B:screens[1] |
| l20-betting-on-sequences.json | `.screens[1].hints[1].text` | From HH, heads keep you at HH and the first T completes HHT. | correct | B:screens[1] |
| l20-betting-on-sequences.json | `.screens[1].hints[2].text` | So HHT wins only if flips 1 and 2 are HH. Any earlier T hands the race to THH. | correct | B:screens[1] |
| l20-betting-on-sequences.json | `.screens[1].feedback.correct` | $\tfrac34$ again. | correct | B:screens[1] |
| l20-betting-on-sequences.json | `.screens[1].feedback.generic` | Not quite right. Ask when HHT can still win. | correct | B:screens[1] |
| l20-betting-on-sequences.json | `.screens[1].feedback.byKey.half` | Same length is not the same chance. Any T before HH means THH completes first. | correct | B:screens[1] |
| l20-betting-on-sequences.json | `.screens[1].feedback.byKey.quarter` | That is HHT's chance. | correct | B:screens[1] |
| l20-betting-on-sequences.json | `.screens[1].explain.text` | Once HH appears, HHT is certain: the next T completes it. So HH must come on flips 1 and 2, or a T came first and THH w… | correct | B:screens[1] |
| l20-betting-on-sequences.json | `.screens[2].prose` | HHT against HTH is harder: neither pattern wins at a stroke. Let $x_s$ be HHT's chance from node $s$. | correct | B:screens[2] |
| l20-betting-on-sequences.json | `.screens[2].widget.accept` | 2/3, about 0.6667 | correct | B:screens[2] |
| l20-betting-on-sequences.json | `.screens[2].hints[0].text` | From HH, HHT is certain: $x_{HH} = 1$. | correct | B:screens[2] |
| l20-betting-on-sequences.json | `.screens[2].hints[1].text` | $x_H = \tfrac12 + \tfrac12 x_{HT}$ and $x_{HT} = \tfrac12 x_H$, since the start acts like H. | correct | B:screens[2] |
| l20-betting-on-sequences.json | `.screens[2].hints[2].text` | $x_H = \tfrac12 + \tfrac14 x_H$, so $x_H = \tfrac23$. | correct | B:screens[2] |
| l20-betting-on-sequences.json | `.screens[2].feedback.correct` | $\tfrac23$: fair odds are 2 to 1 on HHT. | correct | B:screens[2] |
| l20-betting-on-sequences.json | `.screens[2].feedback.generic` | Not quite right. Write an equation for each node, then solve. | correct | B:screens[2] |
| l20-betting-on-sequences.json | `.screens[2].feedback.byKey.half` | Same length is not the same chance. HTH can be cut off by the T that completes HHT. | correct | B:screens[2] |
| l20-betting-on-sequences.json | `.screens[2].feedback.byKey.third` | That is HTH's chance. | correct | B:screens[2] |
| l20-betting-on-sequences.json | `.screens[2].explain.text` | From HT, an H wins for HTH and a T sends you back to the start. Solving the node equations gives $\tfrac23$. So a fair … | correct | B:screens[2] |
| l20-betting-on-sequences.json | `.screens[3].prose` | A colleague offers you even money on HTH against HHT, first to appear. You would back HTH. | correct | B:screens[3] |
| l20-betting-on-sequences.json | `.screens[3].widget.options[0].text` | No: HHT comes first two times in three, so you lose on average | correct | B:screens[3] |
| l20-betting-on-sequences.json | `.screens[3].widget.options[1].why` | That is the chance at a fixed place. First to appear is a race, and HHT wins it 2 to 1. | correct | B:screens[3] |
| l20-betting-on-sequences.json | `.screens[3].widget.options[2].why` | Self-overlap slows a pattern down: HTH waits 10 flips on average and HHT 8. | correct | B:screens[3] |
| l20-betting-on-sequences.json | `.screens[3].widget.options[3].why` | The waits differ and so do the chances: HHT wins 2 times in 3. | correct | B:screens[3] |
| l20-betting-on-sequences.json | `.screens[3].hints[0].text` | Equal chances at a fixed place are not equal chances to come first. | correct | B:screens[3] |
| l20-betting-on-sequences.json | `.screens[3].hints[1].text` | Use the chain from the last screen. | correct | B:screens[3] |
| l20-betting-on-sequences.json | `.screens[3].hints[2].text` | HHT first with $\tfrac23$. | correct | B:screens[3] |
| l20-betting-on-sequences.json | `.screens[3].feedback.correct` | Not fair: you lose a third of your stake on average. | correct | B:screens[3] |
| l20-betting-on-sequences.json | `.screens[3].feedback.generic` | Not quite right. Recall the race from the last screen. | correct | B:screens[3] |
| l20-betting-on-sequences.json | `.screens[3].feedback.byKey.b` | You used the chance at a fixed place, $\tfrac18$ each. The race is different: HHT wins 2 times in 3. | correct | B:screens[3] |
| l20-betting-on-sequences.json | `.screens[3].explain.text` | At even money your expected gain per £1 is $\tfrac13 - \tfrac23 = -\tfrac13$. Fair odds would pay you £2 per £1. Every … | correct | B:screens[3] |
| l20-betting-on-sequences.json | `.screens[4].prose` | Each node is the longest end of the flips that starts a pattern. **First-step analysis** on these joint states gives ea… | correct | B:screens[4] |
| l20-betting-on-sequences.json | `.screens[4].hints[0].text` | Compare HTH's last $k$ letters with its first $k$, for $k = 3, 2, 1$. | correct | B:screens[4] |
| l20-betting-on-sequences.json | `.screens[4].hints[1].text` | $k = 3$ matches (4) and $k = 2$ does not: TH is not HT. | correct | B:screens[4] |
| l20-betting-on-sequences.json | `.screens[4].hints[2].text` | $k = 1$: H equals H, adding 1. | correct | B:screens[4] |
| l20-betting-on-sequences.json | `.screens[4].feedback.correct` | $4 + 1 = 5$. | correct | B:screens[4] |
| l20-betting-on-sequences.json | `.screens[4].feedback.generic` | Not quite right. Check $k = 3$, $2$ and $1$ in turn. | correct | B:screens[4] |
| l20-betting-on-sequences.json | `.screens[4].feedback.byKey.four` | You counted only the full match. The last H also equals the first H, adding 1. | correct | B:screens[4] |
| l20-betting-on-sequences.json | `.screens[4].feedback.byKey.seven` | You counted $k = 2$ too, but TH is not HT. | correct | B:screens[4] |
| l20-betting-on-sequences.json | `.screens[4].explain.text` | Matches at $k = 3$ and $k = 1$ give $4 + 1 = 5$. With A = HHT and B = HTH the formula gives $(4 - 2) : (5 - 1)$. So HTH… | correct | B:screens[4] |
| l20-betting-on-sequences.json | `.screens[5].prose` | Interviewers want the equations, not only the answer. Solve HHT against HTH with one justified line per step. | correct | B:screens[5] |
| l20-betting-on-sequences.json | `.screens[5].widget.lines[0].text` | Let $x_s$ be HHT's chance of coming first from node $s$. | correct | B:screens[5] |
| l20-betting-on-sequences.json | `.screens[5].widget.lines[1].text` | From HH, a T completes HHT and an H keeps HH: $x_{HH} = 1$. | correct | B:screens[5] |
| l20-betting-on-sequences.json | `.screens[5].widget.lines[2].text` | From HT, an H completes HTH and a T restarts: $x_{HT} = \tfrac12 x_{\varnothing}$. | correct | B:screens[5] |
| l20-betting-on-sequences.json | `.screens[5].widget.lines[3].text` | From the start a T changes nothing, so $x_{\varnothing} = x_H$. | correct | B:screens[5] |
| l20-betting-on-sequences.json | `.screens[5].widget.lines[4].text` | From H: $x_H = \tfrac12 x_{HH} + \tfrac12 x_{HT} = \tfrac12 + \tfrac14 x_H$. | correct | B:screens[5] |
| l20-betting-on-sequences.json | `.screens[5].widget.lines[5].text` | So $x_H = \tfrac23$, and HHT comes first with chance $\tfrac23$. | correct | B:screens[5] |
| l20-betting-on-sequences.json | `.screens[5].widget.lines[6].text` | Each pattern has chance $\tfrac18$ in three flips, so $x = \tfrac12$. | correct | B:screens[5] |
| l20-betting-on-sequences.json | `.screens[5].widget.lines[6].why` | That is the chance at a fixed place. The race needs the node equations. | correct | B:screens[5] |
| l20-betting-on-sequences.json | `.screens[5].hints[0].text` | Define the unknowns first. | correct | B:screens[5] |
| l20-betting-on-sequences.json | `.screens[5].hints[1].text` | The three node facts can go in any order. | correct | B:screens[5] |
| l20-betting-on-sequences.json | `.screens[5].hints[2].text` | Define, three node facts, the equation for H, the answer. | correct | B:screens[5] |
| l20-betting-on-sequences.json | `.screens[5].feedback.correct` | Define, state each node, solve: $\tfrac23$. | correct | B:screens[5] |
| l20-betting-on-sequences.json | `.screens[5].feedback.generic` | Not quite right. Start by naming $x_s$. | correct | B:screens[5] |
| l20-betting-on-sequences.json | `.screens[5].feedback.byKey.d1` | You used the chance at a fixed place. The race needs the node equations. | correct | B:screens[5] |
| l20-betting-on-sequences.json | `.screens[5].feedback.byKey.left-out` | Every line except the $\tfrac18$ argument belongs. | correct | B:screens[5] |
| l20-betting-on-sequences.json | `.screens[5].feedback.byKey.s6` | The answer comes last. | correct | B:screens[5] |
| l20-betting-on-sequences.json | `.screens[5].explain.text` | The node equations have one solution with $x_{HH} = 1$. Substituting the HT and start lines into the H line leaves one … | correct | B:screens[5] |
| l20-betting-on-sequences.json | `.screens[6].prose` | Write `first_to_appear(a, b)`: the exact chance that `a` comes before `b` with a fair coin. A hidden helper `solve(rows… | correct | B:screens[6] |
| l20-betting-on-sequences.json | `.screens[6].widget.how` | Check runs 10 hidden tests. Tests 1 to 7 need an exact `Fraction`. Tests 8 and 9 accept a simulated share within three … | correct | B:screens[6] |
| l20-betting-on-sequences.json | `.screens[6].hints[0].text` | For each node $s$ and flip $c$, find where $s + c$ goes. | correct | B:screens[6] |
| l20-betting-on-sequences.json | `.screens[6].hints[1].text` | If $s + c$ ends with `a`, add $\tfrac12$ to the right side; if it ends with `b`, add nothing. | correct | B:screens[6] |
| l20-betting-on-sequences.json | `.screens[6].hints[2].text` | Otherwise drop letters from the front until the string is a node, and subtract $\tfrac12$ in that column. | correct | B:screens[6] |
| l20-betting-on-sequences.json | `.screens[6].feedback.correct` | Exact and simulated chances agree within the noise. | correct | B:screens[6] |
| l20-betting-on-sequences.json | `.screens[6].feedback.generic` | Not quite right. Look at the first failing test. | correct | B:screens[6] |
| l20-betting-on-sequences.json | `.screens[6].feedback.byKey.test-1` | Check the row for each node: a 1 on the diagonal, minus $\tfrac12$ for each flip that stays in play. | correct | B:screens[6] |
| l20-betting-on-sequences.json | `.screens[6].feedback.byKey.test-8` | The simulated share is far from $\tfrac23$. Check that each game stops at the first pattern to appear. | correct | B:screens[6] |
| l20-betting-on-sequences.json | `.screens[6].explain.text` | Each node gives one equation: $x_s = \tfrac12 x_{s+H} + \tfrac12 x_{s+T}$, with wins worth 1 and losses 0. With seed 1 … | correct | B:screens[6] |
| l20-betting-on-sequences.json | `.screens[7].prose` | Three puzzles at about 3 minutes each; keep your own time and say each argument aloud. Give four decimal places. | correct | B:screens[7] |
| l20-betting-on-sequences.json | `.screens[7].hints[0].text` | Ask when each pattern can still win. | correct | B:screens[7] |
| l20-betting-on-sequences.json | `.screens[7].hints[1].text` | TTH needs TT first; HHH needs three heads at the very start. | correct | B:screens[7] |
| l20-betting-on-sequences.json | `.screens[7].hints[2].text` | $\tfrac34$, then $\tfrac{2/3}{1/3}$, then $1 - \tfrac18$. | correct | B:screens[7] |
| l20-betting-on-sequences.json | `.screens[7].feedback.correct` | $0.75$, $2$ and $0.875$. | correct | B:screens[7] |
| l20-betting-on-sequences.json | `.screens[7].feedback.generic` | Not quite right. Check the first answer that is marked. | correct | B:screens[7] |
| l20-betting-on-sequences.json | `.screens[7].feedback.byKey.r0c1` | Check the first: TTH can only win if flips 1 and 2 are TT. | correct | B:screens[7] |
| l20-betting-on-sequences.json | `.screens[7].feedback.byKey.r1c1` | Check the odds: HTH comes first with $\tfrac13$, so the odds against are $\tfrac23 : \tfrac13$. | correct | B:screens[7] |
| l20-betting-on-sequences.json | `.screens[7].feedback.byKey.r2c1` | Check the last: any T before HHH means THH completes first. | correct | B:screens[7] |
| l20-betting-on-sequences.json | `.screens[7].explain.text` | TTH needs TT at the start, else an H came first and HTT wins: $\tfrac34$. HTH comes first with $\tfrac13$, so the odds … | correct | B:screens[7] |
| l20-betting-on-sequences.json | `.screens[8].prose` | You gave $\tfrac34$ for TH against HH. The interviewer now uses a coin that lands heads with chance $\tfrac23$. | correct | B:screens[8] |
| l20-betting-on-sequences.json | `.screens[8].widget.accept` | 5/9, about 0.5556 | correct | B:screens[8] |
| l20-betting-on-sequences.json | `.screens[8].hints[0].text` | Does the argument from the first screen still hold? | correct | B:screens[8] |
| l20-betting-on-sequences.json | `.screens[8].hints[1].text` | Once a T appears, TH still wins. | correct | B:screens[8] |
| l20-betting-on-sequences.json | `.screens[8].hints[2].text` | HH wins only with two opening heads: $(\tfrac23)^2$. | correct | B:screens[8] |
| l20-betting-on-sequences.json | `.screens[8].feedback.correct` | $1 - \tfrac49 = \tfrac59 \approx 0.5556$. | correct | B:screens[8] |
| l20-betting-on-sequences.json | `.screens[8].feedback.generic` | Not quite right. Find HH's chance first. | correct | B:screens[8] |
| l20-betting-on-sequences.json | `.screens[8].feedback.byKey.fair` | That is the fair-coin answer. Heads are now more likely, so HH opens more often. | correct | B:screens[8] |
| l20-betting-on-sequences.json | `.screens[8].feedback.byKey.hh` | That is HH's chance. | correct | B:screens[8] |
| l20-betting-on-sequences.json | `.screens[8].feedback.byKey.tails` | You used the chance of a tail. TH also needs the opening to avoid HH. | correct | B:screens[8] |
| l20-betting-on-sequences.json | `.screens[8].explain.text` | Once a T shows, TH still wins. HH needs two opening heads, chance $\tfrac49$. So TH wins with $\tfrac59$, even with a c… | correct | B:screens[8] |
| l20-betting-on-sequences.json | `.screens[9].prose` | An interviewer offers Penney's game for £10. They pick a pattern of three flips, then you pick yours. First to appear w… | correct | B:screens[9] |
| l20-betting-on-sequences.json | `.screens[9].widget.options[0].text` | TTH | correct | B:screens[9] |
| l20-betting-on-sequences.json | `.screens[9].widget.options[1].why` | HHT does beat THT, with $\tfrac58$, but TTH does better at $\tfrac23$. | correct | B:screens[9] |
| l20-betting-on-sequences.json | `.screens[9].widget.options[2].why` | Mirroring gives an even race, $\tfrac12$. You can do better. | correct | B:screens[9] |
| l20-betting-on-sequences.json | `.screens[9].widget.options[3].why` | TTT needs three tails in a row and wins only $\tfrac25$. | correct | B:screens[9] |
| l20-betting-on-sequences.json | `.screens[9].hints[0].text` | Put a letter in front of their first two letters. | correct | B:screens[9] |
| l20-betting-on-sequences.json | `.screens[9].hints[1].text` | Their first two letters are TH; you want to finish just before THT can. | correct | B:screens[9] |
| l20-betting-on-sequences.json | `.screens[9].hints[2].text` | TTH: the opposite of their middle letter, then TH. | correct | B:screens[9] |
| l20-betting-on-sequences.json | `.screens[9].feedback.correct` | TTH, which wins with $\tfrac23$. | correct | B:screens[9] |
| l20-betting-on-sequences.json | `.screens[9].feedback.generic` | Not quite right. Build your pattern from the front of theirs. | correct | B:screens[9] |
| l20-betting-on-sequences.json | `.screens[9].feedback.byKey.b` | HHT wins $\tfrac58$ against THT. TTH wins $\tfrac23$. | correct | B:screens[9] |
| l20-betting-on-sequences.json | `.screens[9].explain.text` | Take the opposite of their middle letter, then their first two letters: T, then TH. TTH beats THT with chance $\tfrac23… | correct | B:screens[9] |
| l20-betting-on-sequences.json | `.summary.ideas[0]` | Same length is not the same chance: TH beats HH 3 to 1, and HHT beats HTH 2 to 1. | correct | B:summary |
| l20-betting-on-sequences.json | `.summary.ideas[1]` | First-step analysis on joint nodes gives every race exactly; Conway's leading numbers give it fast. | correct | B:summary |
| l20-betting-on-sequences.json | `.summary.ideas[2]` | Choosing second wins: put the opposite of their middle letter in front of their first two. | correct | B:summary |
| l20-betting-on-sequences.json | `.summary.formula.note` | $A \cdot B$ adds $2^{k-1}$ for each $k$ where A's end equals B's start. | correct | B:summary |
| l20-betting-on-sequences.json | `.summary.trap` | Treating every pattern of the same length as equally likely to come first. That is true at a fixed place, not in a race. | correct | B:summary |
| l20-betting-on-sequences.json | `.quiz[0].prose` | Flip a fair coin until HT or TH appears. | correct | B:quiz[0] |
| l20-betting-on-sequences.json | `.quiz[0].widget.options[0].text` | $\tfrac12$ | correct | B:quiz[0] |
| l20-betting-on-sequences.json | `.quiz[0].widget.options[1].why` | You used the HH against TH argument. Here swapping H and T swaps the patterns. | correct | B:quiz[0] |
| l20-betting-on-sequences.json | `.quiz[0].widget.options[2].why` | HT does not need the first two flips. Whichever letter comes first, its pattern wins. | correct | B:quiz[0] |
| l20-betting-on-sequences.json | `.quiz[0].feedback.correct` | $\tfrac12$, by symmetry. | correct | B:quiz[0] |
| l20-betting-on-sequences.json | `.quiz[0].feedback.generic` | Not quite right. Swap heads and tails: what happens? | correct | B:quiz[0] |
| l20-betting-on-sequences.json | `.quiz[0].explain.text` | Swapping H and T turns HT into TH, so the race is symmetric. Indeed whichever letter comes first, the first change comp… | correct | B:quiz[0] |
| l20-betting-on-sequences.json | `.quiz[1].prose` | HHT against HTT, with a fair coin. | correct | B:quiz[1] |
| l20-betting-on-sequences.json | `.quiz[1].widget.accept` | 2/3 | correct | B:quiz[1] |
| l20-betting-on-sequences.json | `.quiz[1].feedback.correct` | $\tfrac23$. | correct | B:quiz[1] |
| l20-betting-on-sequences.json | `.quiz[1].feedback.generic` | Not quite right. Write the node equations from H. | correct | B:quiz[1] |
| l20-betting-on-sequences.json | `.quiz[1].feedback.byKey.half` | Same length is not the same chance. | correct | B:quiz[1] |
| l20-betting-on-sequences.json | `.quiz[1].feedback.byKey.third` | That is HTT's chance. | correct | B:quiz[1] |
| l20-betting-on-sequences.json | `.quiz[1].explain.text` | From HH, HHT is certain. From HT, a T wins for HTT and an H gives node H again. So $x_H = \tfrac12 + \tfrac14 x_H$, giv… | correct | B:quiz[1] |
| l20-betting-on-sequences.json | `.quiz[2].prose` | TH comes before HH with chance $\tfrac34$. | correct | B:quiz[2] |
| l20-betting-on-sequences.json | `.quiz[2].feedback.correct` | 3 to 1. | correct | B:quiz[2] |
| l20-betting-on-sequences.json | `.quiz[2].feedback.generic` | Not quite right. Compare the chances against and for HH. | correct | B:quiz[2] |
| l20-betting-on-sequences.json | `.quiz[2].feedback.byKey.third` | You inverted the odds. The bet on HH is the long shot, so it pays more than £1. | correct | B:quiz[2] |
| l20-betting-on-sequences.json | `.quiz[2].feedback.byKey.one` | Even money assumes equal chances. HH comes first only a quarter of the time. | correct | B:quiz[2] |
| l20-betting-on-sequences.json | `.quiz[2].explain.text` | HH comes first with $\tfrac14$. Fair odds against it are $\tfrac34 : \tfrac14 = 3$ to 1. Then a £1 bet has expected gai… | correct | B:quiz[2] |

## l21-kelly.json

### Bases

| key | basis |
|---|---|
| screens[0] | Kelly (1956); Thorp, The Kelly criterion in blackjack, sports betting and the stock market (2006) s. 2 to 4 (growth rate g(f) = E ln(1+fX), a.s. by the SLLN); sim: puzzles-L4-concepts-r2.py:peak of g at f = 0.2; growth turns negative past 0.39; MC median growth 0.2 beats 0.1 beats 0.4; a 40% loss needs a 67% gain |
| screens[1] | Kelly (1956); Thorp, The Kelly criterion in blackjack, sports betting and the stock market (2006) s. 2 to 4 (growth rate g(f) = E ln(1+fX), a.s. by the SLLN); sim: puzzles-L4-concepts-r2.py:peak of g at f = 0.2; growth turns negative past 0.39; MC median growth 0.2 beats 0.1 beats 0.4; a 40% loss needs a 67% gain |
| screens[2] | Kelly (1956); Thorp, The Kelly criterion in blackjack, sports betting and the stock market (2006) s. 2 to 4; sim: puzzles-L4-concepts-r2.py:g(0.2)=0.0201; median of Bin(200,0.6) is 120 so the median path grows e^4.03 = 56 times; mean path 1.04^200 = 2,550 |
| screens[3] | Kelly (1956); Thorp, The Kelly criterion in blackjack, sports betting and the stock market (2006) s. 2 to 4 (Thorp s. 4, fractional Kelly: g(f*/2) = 3/4 g(f*) to second order); sim: puzzles-L4-concepts-r2.py:half Kelly keeps about 75%; sd of log wealth ratio 0.495 |
| quiz[2] | Kelly (1956); Thorp, The Kelly criterion in blackjack, sports betting and the stock market (2006) s. 2 to 4 (Thorp s. 4, fractional Kelly: g(f*/2) = 3/4 g(f*) to second order); sim: puzzles-L4-concepts-r2.py:half Kelly keeps about 75%; sd of log wealth ratio 0.495 |
| screens[4] | Kelly (1956); Thorp, The Kelly criterion in blackjack, sports betting and the stock market (2006) s. 2 to 4; sim: puzzles-L4-concepts-r2.py:g(0.4) = -0.0024; MC double Kelly median log wealth negative after 4000 bets |
| screens[5] | Kelly (1956); Thorp, The Kelly criterion in blackjack, sports betting and the stock market (2006) s. 2 to 4; expected wealth (1+f(p-q))^n is maximised at f=1; sim: puzzles-L4-concepts-r2.py:survival 0.6^10 = 0.006; MC all-in; all-in mean 1.2^n |
| summary | Kelly (1956); Thorp, The Kelly criterion in blackjack, sports betting and the stock market (2006) s. 2 to 4; expected wealth (1+f(p-q))^n is maximised at f=1; sim: puzzles-L4-concepts-r2.py:survival 0.6^10 = 0.006; MC all-in; all-in mean 1.2^n |
| screens[6] | derivation by sympy; sim: puzzles-L4-concepts-r2.py:f* = p - q/b from g'(f) = 0; g'' < 0 so the zero of g' is the peak |
| screens[7] | Kelly (1956); Thorp, The Kelly criterion in blackjack, sports betting and the stock market (2006) s. 2 to 4 (f* = (bp - q)/b, zero when the edge is gone); sim: puzzles-L4-concepts-r2.py:Kelly 0.1, 0.25, 0.25, 1/15; no edge at 2 to 1 with p=0.3; 0.4; evens stake passes half only when p > 3/4 |
| screens[10] | Kelly (1956); Thorp, The Kelly criterion in blackjack, sports betting and the stock market (2006) s. 2 to 4 (f* = (bp - q)/b, zero when the edge is gone); sim: puzzles-L4-concepts-r2.py:Kelly 0.1, 0.25, 0.25, 1/15; no edge at 2 to 1 with p=0.3; 0.4; evens stake passes half only when p > 3/4 |
| screens[9] | Kelly (1956); Thorp, The Kelly criterion in blackjack, sports betting and the stock market (2006) s. 2 to 4 (f* = (bp - q)/b, zero when the edge is gone); sim: puzzles-L4-concepts-r2.py:Kelly 0.1, 0.25, 0.25, 1/15; no edge at 2 to 1 with p=0.3; 0.4; evens stake passes half only when p > 3/4 |
| quiz[0] | Kelly (1956); Thorp, The Kelly criterion in blackjack, sports betting and the stock market (2006) s. 2 to 4 (f* = (bp - q)/b, zero when the edge is gone); sim: puzzles-L4-concepts-r2.py:Kelly 0.1, 0.25, 0.25, 1/15; no edge at 2 to 1 with p=0.3; 0.4; evens stake passes half only when p > 3/4 |
| quiz[1] | Kelly (1956); Thorp, The Kelly criterion in blackjack, sports betting and the stock market (2006) s. 2 to 4 (f* = (bp - q)/b, zero when the edge is gone); sim: puzzles-L4-concepts-r2.py:Kelly 0.1, 0.25, 0.25, 1/15; no edge at 2 to 1 with p=0.3; 0.4; evens stake passes half only when p > 3/4 |
| screens[8] | sim: puzzles-L4-concepts-r2.py:solution passes all 13 hidden tests; growth 0.0050 and 0.0589 |
| screens[11] | Kelly (1956); Thorp, The Kelly criterion in blackjack, sports betting and the stock market (2006) s. 2 to 4 (b = payoff ratio); sim: puzzles-L4-concepts-r2.py:Kelly(0.55, 1.5) = 0.25; at a true hit rate 0.5 full Kelly is about 0.167; half Kelly keeps 75% |

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l21-kelly.json | `.screens[0].prose` | Three bettors start with £100 and back the same 200 coin flips. Each bet pays evens and wins with chance 0.6. Each stak… | correct | B:screens[0] |
| l21-kelly.json | `.screens[0].widget.options[0].text` | $f = 0.2$ | correct | B:screens[0] |
| l21-kelly.json | `.screens[0].widget.options[1].why` | Bigger stakes win more per win, but losses bite harder. Its line drifts down, though every bet favours it. | correct | B:screens[0] |
| l21-kelly.json | `.screens[0].widget.options[2].why` | It grows steadily, but it leaves growth unused. | correct | B:screens[0] |
| l21-kelly.json | `.screens[0].widget.options[3].why` | The edge is the same, but the stake changes how losses compound. The lines part. | correct | B:screens[0] |
| l21-kelly.json | `.screens[0].hints[0].text` | Read the slopes on the log scale. | correct | B:screens[0] |
| l21-kelly.json | `.screens[0].hints[1].text` | A steeper straight climb is a faster growth rate. | correct | B:screens[0] |
| l21-kelly.json | `.screens[0].hints[2].text` | The 0.2 line climbs fastest; the 0.4 line ends below £100. | correct | B:screens[0] |
| l21-kelly.json | `.screens[0].feedback.correct` | $f = 0.2$ grows fastest. | correct | B:screens[0] |
| l21-kelly.json | `.screens[0].feedback.generic` | Not quite right. Compare the slopes of the three lines. | correct | B:screens[0] |
| l21-kelly.json | `.screens[0].feedback.byKey.b` | Staking more is not growing more. A 40% loss needs a 67% gain to recover. | correct | B:screens[0] |
| l21-kelly.json | `.screens[0].explain.text` | The 0.2 line climbs fastest. The 0.4 line ends below £100, though every bet favoured it. On this scale a steady slope i… | correct | B:screens[0] |
| l21-kelly.json | `.screens[1].prose` | The curve is the average log growth per bet, $g(f) = 0.6\ln(1 + f) + 0.4\ln(1 - f)$. Drag the point along it. | correct | B:screens[1] |
| l21-kelly.json | `.screens[1].feedback.correct` | The peak is at $f = 0.2$. | correct | B:screens[1] |
| l21-kelly.json | `.screens[1].feedback.generic` | Not quite right. Watch the growth in the caption as you drag. | correct | B:screens[1] |
| l21-kelly.json | `.screens[1].feedback.byKey.p1` | Not at the top yet. Move until the growth stops rising. | correct | B:screens[1] |
| l21-kelly.json | `.screens[1].explain.text` | The growth rises, peaks at $f = 0.2$ and turns negative past $f \approx 0.39$. The peak is the stake that grows wealth … | correct | B:screens[1] |
| l21-kelly.json | `.screens[2].prose` | The fraction at the peak is the **Kelly fraction** $f^*$. Here $f^* = 0.2$, which is $p - q$. | correct | B:screens[2] |
| l21-kelly.json | `.screens[2].widget.accept` | 0.6 ln 1.2 + 0.4 ln 0.8, about 0.0201 | correct | B:screens[2] |
| l21-kelly.json | `.screens[2].hints[0].text` | Put $f = 0.2$ into $g$. | correct | B:screens[2] |
| l21-kelly.json | `.screens[2].hints[1].text` | $\ln 1.2 \approx 0.1823$ and $\ln 0.8 \approx -0.2231$. | correct | B:screens[2] |
| l21-kelly.json | `.screens[2].hints[2].text` | $0.6 \times 0.1823 - 0.4 \times 0.2231 \approx 0.0201$. | correct | B:screens[2] |
| l21-kelly.json | `.screens[2].feedback.correct` | $g(0.2) \approx 0.0201$ a bet. | correct | B:screens[2] |
| l21-kelly.json | `.screens[2].feedback.generic` | Not quite right. Weight the log of each outcome by its chance. | correct | B:screens[2] |
| l21-kelly.json | `.screens[2].feedback.byKey.ev` | That is the mean return, $f(p - q) = 0.04$. Growth is the mean of the log, which is lower. | correct | B:screens[2] |
| l21-kelly.json | `.screens[2].feedback.byKey.lnonly` | You took $\ln 1.2$ alone. Losses happen 40% of the time and count too. | correct | B:screens[2] |
| l21-kelly.json | `.screens[2].explain.text` | Typical wealth grows like $e^{0.0201n}$, about 2% a bet. Over 200 bets the median path grows $e^{4.03} \approx 56$ time… | correct | B:screens[2] |
| l21-kelly.json | `.screens[3].prose` | Many desks stake half the Kelly fraction. Here that is $f = 0.1$. | correct | B:screens[3] |
| l21-kelly.json | `.screens[3].widget.accept` | 0.6 ln 1.1 + 0.4 ln 0.9, about 0.0150 | correct | B:screens[3] |
| l21-kelly.json | `.screens[3].hints[0].text` | Put $f = 0.1$ into $g$. | correct | B:screens[3] |
| l21-kelly.json | `.screens[3].hints[1].text` | $\ln 1.1 \approx 0.0953$ and $\ln 0.9 \approx -0.1054$. | correct | B:screens[3] |
| l21-kelly.json | `.screens[3].hints[2].text` | $0.6 \times 0.0953 - 0.4 \times 0.1054 \approx 0.0150$. | correct | B:screens[3] |
| l21-kelly.json | `.screens[3].feedback.correct` | $g(0.1) \approx 0.0150$. | correct | B:screens[3] |
| l21-kelly.json | `.screens[3].feedback.generic` | Not quite right. Recompute $g$ at $f = 0.1$. | correct | B:screens[3] |
| l21-kelly.json | `.screens[3].feedback.byKey.half` | You halved the growth. Near the peak the curve is flat, so half the stake keeps more than half the growth. | correct | B:screens[3] |
| l21-kelly.json | `.screens[3].feedback.byKey.ev` | That is the mean return, $0.1 \times 0.2$. | correct | B:screens[3] |
| l21-kelly.json | `.screens[3].explain.text` | Half Kelly keeps $0.0150/0.0201 \approx 75\%$ of the growth. The spread of log wealth halves, since it scales with $f$.… | correct | B:screens[3] |
| l21-kelly.json | `.screens[4].prose` | Now stake twice the Kelly fraction, $f = 0.4$. | correct | B:screens[4] |
| l21-kelly.json | `.screens[4].widget.accept` | 0.6 ln 1.4 + 0.4 ln 0.6, about −0.0024 | correct | B:screens[4] |
| l21-kelly.json | `.screens[4].hints[0].text` | Put $f = 0.4$ into $g$. | correct | B:screens[4] |
| l21-kelly.json | `.screens[4].hints[1].text` | $\ln 1.4 \approx 0.3365$ and $\ln 0.6 \approx -0.5108$. | correct | B:screens[4] |
| l21-kelly.json | `.screens[4].hints[2].text` | $0.6 \times 0.3365 - 0.4 \times 0.5108 \approx -0.0024$. | correct | B:screens[4] |
| l21-kelly.json | `.screens[4].feedback.correct` | $g(0.4) \approx -0.0024$: negative. | correct | B:screens[4] |
| l21-kelly.json | `.screens[4].feedback.generic` | Not quite right. Watch the sign of the loss term. | correct | B:screens[4] |
| l21-kelly.json | `.screens[4].feedback.byKey.positive` | Check the sign. The loss term, $0.4 \ln 0.6$, is larger. | correct | B:screens[4] |
| l21-kelly.json | `.screens[4].feedback.byKey.ev` | That is the mean return. The log growth is below zero. | correct | B:screens[4] |
| l21-kelly.json | `.screens[4].explain.text` | The growth is about $-0.0024$ a bet. Every bet has positive expectation, yet wealth shrinks in the long run. Overbettin… | correct | B:screens[4] |
| l21-kelly.json | `.screens[5].prose` | Each bet still wins with chance 0.6 at evens. A candidate says the expected value is positive, so stake the whole bankr… | correct | B:screens[5] |
| l21-kelly.json | `.screens[5].widget.options[0].text` | One loss ruins them, and ruin is almost certain within a few bets | correct | B:screens[5] |
| l21-kelly.json | `.screens[5].widget.options[1].why` | The mean, $1.2^n$, rests on a tiny chance of never losing: $0.6^n$. | correct | B:screens[5] |
| l21-kelly.json | `.screens[5].widget.options[2].why` | That is the mean return of the all-in bet. After any loss the wealth is 0. | correct | B:screens[5] |
| l21-kelly.json | `.screens[5].widget.options[3].why` | The growth depends on the stake. At $f = 1$ one loss sends $\ln(1 - f)$ to minus infinity. | correct | B:screens[5] |
| l21-kelly.json | `.screens[5].hints[0].text` | What is wealth after one loss at $f = 1$? | correct | B:screens[5] |
| l21-kelly.json | `.screens[5].hints[1].text` | It is 0, and stays 0. | correct | B:screens[5] |
| l21-kelly.json | `.screens[5].hints[2].text` | Survival for $n$ bets has chance $0.6^n$. | correct | B:screens[5] |
| l21-kelly.json | `.screens[5].feedback.correct` | Ruin is almost certain. | correct | B:screens[5] |
| l21-kelly.json | `.screens[5].feedback.generic` | Not quite right. Follow one loss. | correct | B:screens[5] |
| l21-kelly.json | `.screens[5].feedback.byKey.b` | You maximised the expected value. That stakes everything, and one loss ends the game. | correct | B:screens[5] |
| l21-kelly.json | `.screens[5].feedback.byKey.c` | The 20% is the mean return. The typical path is ruined. | correct | B:screens[5] |
| l21-kelly.json | `.screens[5].explain.text` | Staking everything maximises expected wealth, but that mean rests on never losing. Surviving 10 bets has chance $0.6^{1… | correct | B:screens[5] |
| l21-kelly.json | `.screens[6].prose` | Derive the Kelly fraction for an even-money bet, one justified line at a time. | correct | B:screens[6] |
| l21-kelly.json | `.screens[6].widget.lines[0].text` | Each bet multiplies wealth by $1 + f$ with chance $p$, or by $1 - f$ with chance $q$. | correct | B:screens[6] |
| l21-kelly.json | `.screens[6].widget.lines[1].text` | So the expected log growth per bet is $g(f) = p\ln(1 + f) + q\ln(1 - f)$. | correct | B:screens[6] |
| l21-kelly.json | `.screens[6].widget.lines[2].text` | Differentiate: $g'(f) = \dfrac{p}{1 + f} - \dfrac{q}{1 - f}$. | correct | B:screens[6] |
| l21-kelly.json | `.screens[6].widget.lines[3].text` | At the peak $g'(f) = 0$, so $p(1 - f) = q(1 + f)$. | correct | B:screens[6] |
| l21-kelly.json | `.screens[6].widget.lines[4].text` | Expand: $p - pf = q + qf$, so $f(p + q) = p - q$. | correct | B:screens[6] |
| l21-kelly.json | `.screens[6].widget.lines[5].text` | Since $p + q = 1$, $f^* = p - q$, which is $0.2$ at $p = 0.6$. | correct | B:screens[6] |
| l21-kelly.json | `.screens[6].widget.lines[6].text` | Expected wealth $1 + f(p - q)$ rises with $f$, so $f^* = 1$. | correct | B:screens[6] |
| l21-kelly.json | `.screens[6].widget.lines[6].why` | That maximises the mean, not the growth, and it stakes everything. | correct | B:screens[6] |
| l21-kelly.json | `.screens[6].hints[0].text` | Start from what one bet does to wealth. | correct | B:screens[6] |
| l21-kelly.json | `.screens[6].hints[1].text` | Take logs, average, then differentiate. | correct | B:screens[6] |
| l21-kelly.json | `.screens[6].hints[2].text` | Outcomes, $g$, $g'$, set to zero, expand, use $p + q = 1$. | correct | B:screens[6] |
| l21-kelly.json | `.screens[6].feedback.correct` | $f^* = p - q$. | correct | B:screens[6] |
| l21-kelly.json | `.screens[6].feedback.generic` | Not quite right. Start from one bet's two outcomes. | correct | B:screens[6] |
| l21-kelly.json | `.screens[6].feedback.byKey.d1` | That maximises expected wealth, which stakes everything. Kelly maximises the expected log. | correct | B:screens[6] |
| l21-kelly.json | `.screens[6].feedback.byKey.left-out` | Every line except the expected-wealth argument belongs. | correct | B:screens[6] |
| l21-kelly.json | `.screens[6].feedback.byKey.s6` | The answer comes last. | correct | B:screens[6] |
| l21-kelly.json | `.screens[6].explain.text` | $g''(f) = -\tfrac{p}{(1 + f)^2} - \tfrac{q}{(1 - f)^2} < 0$, so the zero of $g'$ is the peak. The algebra gives $f^* = … | correct | B:screens[6] |
| l21-kelly.json | `.screens[7].prose` | At odds of $b$ to 1, a win multiplies wealth by $1 + bf$. The same steps give $$f^* = p - \frac{q}{b},$$ the rule from … | correct | B:screens[7] |
| l21-kelly.json | `.screens[7].widget.accept` | 0.4 − 0.6/2 = 0.1 | correct | B:screens[7] |
| l21-kelly.json | `.screens[7].hints[0].text` | Here $p = 0.4$, $q = 0.6$ and $b = 2$. | correct | B:screens[7] |
| l21-kelly.json | `.screens[7].hints[1].text` | $q/b = 0.3$. | correct | B:screens[7] |
| l21-kelly.json | `.screens[7].hints[2].text` | $f^* = 0.4 - 0.3$. | correct | B:screens[7] |
| l21-kelly.json | `.screens[7].feedback.correct` | $f^* = 0.1$. | correct | B:screens[7] |
| l21-kelly.json | `.screens[7].feedback.generic` | Not quite right. Use $p - q/b$. | correct | B:screens[7] |
| l21-kelly.json | `.screens[7].feedback.byKey.evens` | You used $p - q$, the evens rule. At 2 to 1, divide $q$ by 2. | correct | B:screens[7] |
| l21-kelly.json | `.screens[7].feedback.byKey.ev` | That is the edge per £1, $2 \times 0.4 - 0.6$. Kelly divides the edge by the odds. | correct | B:screens[7] |
| l21-kelly.json | `.screens[7].explain.text` | $f^* = 0.4 - 0.6/2 = 0.1$. The bet loses more often than it wins, yet it has an edge of 0.2 per £1. Kelly stakes the ed… | correct | B:screens[7] |
| l21-kelly.json | `.screens[8].prose` | Write `kelly(p, b)`, the Kelly fraction for a bet paying `b` to 1 that wins with chance `p`, never below 0. Then write … | correct | B:screens[8] |
| l21-kelly.json | `.screens[8].widget.how` | Check runs 13 hidden tests, each within 1e-9 of the exact value. Two bets have no edge, so `kelly` must return 0 for th… | correct | B:screens[8] |
| l21-kelly.json | `.screens[8].hints[0].text` | A win multiplies wealth by $1 + bf$. | correct | B:screens[8] |
| l21-kelly.json | `.screens[8].hints[1].text` | `kelly` is $p - q/b$, floored at 0 with `max`. | correct | B:screens[8] |
| l21-kelly.json | `.screens[8].hints[2].text` | `growth` is `p * log(1 + b*f) + (1 - p) * log(1 - f)`. | correct | B:screens[8] |
| l21-kelly.json | `.screens[8].feedback.correct` | Both functions match to 9 places. | correct | B:screens[8] |
| l21-kelly.json | `.screens[8].feedback.generic` | Not quite right. Look at the first failing test. | correct | B:screens[8] |
| l21-kelly.json | `.screens[8].feedback.byKey.test-5` | This bet has no edge: $0.3 - 0.7/2 < 0$. Return 0, not a negative stake. | correct | B:screens[8] |
| l21-kelly.json | `.screens[8].feedback.byKey.test-11` | A win multiplies wealth by $1 + bf$, not $1 + f$. | correct | B:screens[8] |
| l21-kelly.json | `.screens[8].explain.text` | `kelly` floors the stake at 0, the edge case where the bet has no edge. `growth(0.6, 1, 0.2)` returns 0.0201355, the pe… | correct | B:screens[8] |
| l21-kelly.json | `.screens[9].prose` | Three puzzles at about 3 minutes each; keep your own time and say each argument aloud. Give four decimal places. | correct | B:screens[9] |
| l21-kelly.json | `.screens[9].hints[0].text` | Use $f^* = p - q/b$ and $g = p\ln(1 + bf) + q\ln(1 - f)$. | correct | B:screens[9] |
| l21-kelly.json | `.screens[9].hints[1].text` | $0.7/3 \approx 0.2333$; $\ln 1.1 \approx 0.0953$, $\ln 0.9 \approx -0.1054$. | correct | B:screens[9] |
| l21-kelly.json | `.screens[9].hints[2].text` | $0.1$, then $0.3 - 0.2333$, then $0.0524 - 0.0474$. | correct | B:screens[9] |
| l21-kelly.json | `.screens[9].feedback.correct` | $0.1$, $0.0667$ and $0.0050$. | correct | B:screens[9] |
| l21-kelly.json | `.screens[9].feedback.generic` | Not quite right. Check the first answer that is marked. | correct | B:screens[9] |
| l21-kelly.json | `.screens[9].feedback.byKey.r0c1` | At evens, $f^* = p - q = 0.55 - 0.45$. | correct | B:screens[9] |
| l21-kelly.json | `.screens[9].feedback.byKey.r1c1` | At 3 to 1, $f^* = 0.3 - 0.7/3$. | correct | B:screens[9] |
| l21-kelly.json | `.screens[9].feedback.byKey.r2c1` | Weight the logs: $0.55 \ln 1.1 + 0.45 \ln 0.9$. | correct | B:screens[9] |
| l21-kelly.json | `.screens[9].explain.text` | At evens $f^* = 0.1$. At 3 to 1, $0.3 - 0.7/3 = \tfrac{1}{15} \approx 0.0667$. The growth at $p = 0.55$ is only about 0… | correct | B:screens[9] |
| l21-kelly.json | `.screens[10].prose` | You gave $f^* = 0.2$ for $p = 0.6$ at evens. The interviewer offers a fair coin instead, paying 2 to 1. | correct | B:screens[10] |
| l21-kelly.json | `.screens[10].widget.accept` | 1/2 − (1/2)/2 = 1/4 | correct | B:screens[10] |
| l21-kelly.json | `.screens[10].hints[0].text` | $p = q = \tfrac12$ and $b = 2$. | correct | B:screens[10] |
| l21-kelly.json | `.screens[10].hints[1].text` | $q/b = \tfrac14$. | correct | B:screens[10] |
| l21-kelly.json | `.screens[10].hints[2].text` | $f^* = \tfrac12 - \tfrac14$. | correct | B:screens[10] |
| l21-kelly.json | `.screens[10].feedback.correct` | $f^* = \tfrac14$. | correct | B:screens[10] |
| l21-kelly.json | `.screens[10].feedback.generic` | Not quite right. Use $p - q/b$ with $b = 2$. | correct | B:screens[10] |
| l21-kelly.json | `.screens[10].feedback.byKey.evens` | That is the evens answer for a fair coin. At 2 to 1 there is an edge. | correct | B:screens[10] |
| l21-kelly.json | `.screens[10].feedback.byKey.ev` | That is the edge per £1, $2 \times \tfrac12 - \tfrac12$. Divide it by the odds. | correct | B:screens[10] |
| l21-kelly.json | `.screens[10].explain.text` | $f^* = \tfrac12 - \tfrac{1/2}{2} = \tfrac14$. The edge is 0.5 per £1 and Kelly stakes edge over odds. A fair coin is wo… | correct | B:screens[10] |
| l21-kelly.json | `.screens[11].prose` | A strategy's trades win 55% of the time, and each win makes 1.5 times what a loss costs. The hit rate comes from a shor… | correct | B:screens[11] |
| l21-kelly.json | `.screens[11].widget.accept` | half of 0.55 − 0.45/1.5, so 0.125 | correct | B:screens[11] |
| l21-kelly.json | `.screens[11].hints[0].text` | The payoff ratio is the odds: $b = 1.5$. | correct | B:screens[11] |
| l21-kelly.json | `.screens[11].hints[1].text` | Full Kelly is $0.55 - 0.45/1.5$. | correct | B:screens[11] |
| l21-kelly.json | `.screens[11].hints[2].text` | Full Kelly is 0.25; halve it. | correct | B:screens[11] |
| l21-kelly.json | `.screens[11].feedback.correct` | $0.125$, half of $0.25$. | correct | B:screens[11] |
| l21-kelly.json | `.screens[11].feedback.generic` | Not quite right. Find full Kelly with $b = 1.5$, then halve it. | correct | B:screens[11] |
| l21-kelly.json | `.screens[11].feedback.byKey.full` | That is full Kelly. The desk halves it. | correct | B:screens[11] |
| l21-kelly.json | `.screens[11].feedback.byKey.evens` | You used $p - q$, as if wins and losses were equal in size. | correct | B:screens[11] |
| l21-kelly.json | `.screens[11].explain.text` | Full Kelly is $0.55 - 0.45/1.5 = 0.25$, so half Kelly is $0.125$. If the true hit rate were 0.5, full Kelly would be ab… | correct | B:screens[11] |
| l21-kelly.json | `.summary.ideas[0]` | Kelly stakes the fraction that maximises expected log wealth, not expected wealth. | correct | B:summary |
| l21-kelly.json | `.summary.ideas[1]` | $f^* = p - q/b$, the edge per £1 divided by the odds; with no edge, stake nothing. | correct | B:summary |
| l21-kelly.json | `.summary.ideas[2]` | Half Kelly keeps about three quarters of the growth with half the spread; double Kelly can shrink wealth. | correct | B:summary |
| l21-kelly.json | `.summary.formula.note` | If $p - q/b \le 0$, $f^* = 0$. | correct | B:summary |
| l21-kelly.json | `.summary.trap` | Staking the whole bankroll because the expected value is positive. One loss ends it. | correct | B:summary |
| l21-kelly.json | `.quiz[0].prose` | A bet pays 2 to 1 and wins with chance 0.3. | correct | B:quiz[0] |
| l21-kelly.json | `.quiz[0].widget.options[0].text` | 0: do not bet | correct | B:quiz[0] |
| l21-kelly.json | `.quiz[0].widget.options[1].why` | You may not stake a negative amount on this bet. A negative Kelly fraction means no edge. | correct | B:quiz[0] |
| l21-kelly.json | `.quiz[0].widget.options[2].why` | That is the win chance, not a stake. The payout must beat the losses first. | correct | B:quiz[0] |
| l21-kelly.json | `.quiz[0].feedback.correct` | Nothing: the bet has no edge. | correct | B:quiz[0] |
| l21-kelly.json | `.quiz[0].feedback.generic` | Not quite right. Compute $p - q/b$ first. | correct | B:quiz[0] |
| l21-kelly.json | `.quiz[0].explain.text` | $p - q/b = 0.3 - 0.35 = -0.05 \le 0$. The edge per £1 is $0.6 - 0.7 = -0.1$. This is the edge case: no edge, no bet. | correct | B:quiz[0] |
| l21-kelly.json | `.quiz[1].prose` | An even-money bet wins with chance 0.7. | correct | B:quiz[1] |
| l21-kelly.json | `.quiz[1].widget.accept` | 0.7 − 0.3 = 0.4 | correct | B:quiz[1] |
| l21-kelly.json | `.quiz[1].feedback.correct` | $f^* = 0.4$. | correct | B:quiz[1] |
| l21-kelly.json | `.quiz[1].feedback.generic` | Not quite right. At evens, $f^* = p - q$. | correct | B:quiz[1] |
| l21-kelly.json | `.quiz[1].feedback.byKey.p` | That is the win chance. Subtract the loss chance. | correct | B:quiz[1] |
| l21-kelly.json | `.quiz[1].feedback.byKey.all` | Staking everything is ruined by one loss. | correct | B:quiz[1] |
| l21-kelly.json | `.quiz[1].explain.text` | $f^* = 0.7 - 0.3 = 0.4$. At evens the stake is $2p - 1$, so it passes half the bankroll only when $p$ exceeds $\tfrac34… | correct | B:quiz[1] |
| l21-kelly.json | `.quiz[2].prose` | At evens with $p = 0.6$, half Kelly stakes 0.1 instead of 0.2. | correct | B:quiz[2] |
| l21-kelly.json | `.quiz[2].widget.options[0].text` | About three quarters | correct | B:quiz[2] |
| l21-kelly.json | `.quiz[2].widget.options[1].why` | Growth is not proportional to the stake. Near the peak the curve is flat. | correct | B:quiz[2] |
| l21-kelly.json | `.quiz[2].widget.options[2].why` | That would be a steep curve. Near its peak $g$ is flat. | correct | B:quiz[2] |
| l21-kelly.json | `.quiz[2].feedback.correct` | About three quarters: $0.0150/0.0201$. | correct | B:quiz[2] |
| l21-kelly.json | `.quiz[2].feedback.generic` | Not quite right. Compare $g(0.1)$ with $g(0.2)$. | correct | B:quiz[2] |
| l21-kelly.json | `.quiz[2].explain.text` | $g(0.1) \approx 0.0150$ against $g(0.2) \approx 0.0201$, a share of about 75%. Near its peak the growth curve is flat, … | correct | B:quiz[2] |

## l22-when-to-hedge.json

### Bases

| key | basis |
|---|---|
| screens[0] | replication: equate the two outcomes; sim: puzzles-L4-concepts-r2.py:hedge 300 locks 200; at 2 to 1 hedge 200 locks 300; hedges 100/50, 50/30 |
| screens[1] | replication: equate the two outcomes; sim: puzzles-L4-concepts-r2.py:hedge 300 locks 200; at 2 to 1 hedge 200 locks 300; hedges 100/50, 50/30 |
| screens[7] | replication: equate the two outcomes; sim: puzzles-L4-concepts-r2.py:hedge 300 locks 200; at 2 to 1 hedge 200 locks 300; hedges 100/50, 50/30 |
| quiz[2] | replication: equate the two outcomes; sim: puzzles-L4-concepts-r2.py:hedge 300 locks 200; at 2 to 1 hedge 200 locks 300; hedges 100/50, 50/30 |
| screens[2] | replication by backward induction at evens (risk-neutral p = 1/2 for pricing, independent of the true chance); sim: puzzles-L4-concepts-r2.py:best-of-seven bets 31.25, 37.5 at 1-1, 25 at 3-1, 100 at 3-3; best-of-5 37.5, best-of-3 50; binomial formula equals the backward-induction bet in every state; the bets replicate +-100 exactly for a true game chance of 0.3, 0.5, 0.8 |
| screens[3] | replication by backward induction at evens (risk-neutral p = 1/2 for pricing, independent of the true chance); sim: puzzles-L4-concepts-r2.py:best-of-seven bets 31.25, 37.5 at 1-1, 25 at 3-1, 100 at 3-3; best-of-5 37.5, best-of-3 50; binomial formula equals the backward-induction bet in every state; the bets replicate +-100 exactly for a true game chance of 0.3, 0.5, 0.8 |
| screens[8] | replication by backward induction at evens (risk-neutral p = 1/2 for pricing, independent of the true chance); sim: puzzles-L4-concepts-r2.py:best-of-seven bets 31.25, 37.5 at 1-1, 25 at 3-1, 100 at 3-3; best-of-5 37.5, best-of-3 50; binomial formula equals the backward-induction bet in every state; the bets replicate +-100 exactly for a true game chance of 0.3, 0.5, 0.8 |
| quiz[1] | replication by backward induction at evens (risk-neutral p = 1/2 for pricing, independent of the true chance); sim: puzzles-L4-concepts-r2.py:best-of-seven bets 31.25, 37.5 at 1-1, 25 at 3-1, 100 at 3-3; best-of-5 37.5, best-of-3 50; binomial formula equals the backward-induction bet in every state; the bets replicate +-100 exactly for a true game chance of 0.3, 0.5, 0.8 |
| summary | replication by backward induction at evens (risk-neutral p = 1/2 for pricing, independent of the true chance); sim: puzzles-L4-concepts-r2.py:best-of-seven bets 31.25, 37.5 at 1-1, 25 at 3-1, 100 at 3-3; best-of-5 37.5, best-of-3 50; binomial formula equals the backward-induction bet in every state; the bets replicate +-100 exactly for a true game chance of 0.3, 0.5, 0.8 |
| screens[4] | expectation; sim: puzzles-L4-concepts-r2.py:unhedged 260, full hedge 200, cost 60 |
| screens[5] | log utility (Kelly) one-shot; sympy: sim: puzzles-L4-concepts-r2.py:log-optimal hedge 60 at p=0.6; expected log 7.109, 7.110, 7.090; stationary point is a maximum |
| screens[6] | replication: value = average, bet = half the gap; sim: puzzles-L4-concepts-r2.py:node value 20, bet 30 |
| screens[9] | Hull, Options, Futures and Other Derivatives ch. 13 (one-step binomial, delta); sim: puzzles-L4-concepts-r2.py:delta = (10-0)/(110-90) = 0.5 |
| quiz[0] | a zero-expectation bet changes variance only; sim: puzzles-L4-concepts-r2.py:at p=1/2 the hedge changes variance not expectation: 200 either way |

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l22-when-to-hedge.json | `.screens[0].prose` | You backed a team at 5 to 1 for £100: you win £500 or lose £100. Now you can bet on the other side at evens. Drag the p… | correct | B:screens[0] |
| l22-when-to-hedge.json | `.screens[0].hints[0].text` | A hedge of $h$ costs $h$ if your team wins and pays $h$ if it loses. | correct | B:screens[0] |
| l22-when-to-hedge.json | `.screens[0].hints[1].text` | You want $500 - h = h - 100$. | correct | B:screens[0] |
| l22-when-to-hedge.json | `.screens[0].hints[2].text` | That is where the two lines cross: $h = 300$. | correct | B:screens[0] |
| l22-when-to-hedge.json | `.screens[0].feedback.correct` | £300 locks in £200 either way. | correct | B:screens[0] |
| l22-when-to-hedge.json | `.screens[0].feedback.generic` | Not quite right. Find where the two lines cross. | correct | B:screens[0] |
| l22-when-to-hedge.json | `.screens[0].feedback.byKey.p1` | The two outcomes still differ. Move to where the lines cross. | correct | B:screens[0] |
| l22-when-to-hedge.json | `.screens[0].explain.text` | At $h = 300$ you make $500 - 300 = 200$ if your team wins and $-100 + 300 = 200$ if it loses. The hedge turns a bet int… | correct | B:screens[0] |
| l22-when-to-hedge.json | `.screens[1].prose` | Same bet, but the other side is now offered at 2 to 1. A hedge of $h$ pays $2h$ if your team loses. | correct | B:screens[1] |
| l22-when-to-hedge.json | `.screens[1].hints[0].text` | Find $h$ with $500 - h = 2h - 100$. | correct | B:screens[1] |
| l22-when-to-hedge.json | `.screens[1].hints[1].text` | $3h = 600$. | correct | B:screens[1] |
| l22-when-to-hedge.json | `.screens[1].hints[2].text` | $h = 200$, so the profit is $500 - 200$. | correct | B:screens[1] |
| l22-when-to-hedge.json | `.screens[1].feedback.correct` | £300 either way, with a £200 hedge. | correct | B:screens[1] |
| l22-when-to-hedge.json | `.screens[1].feedback.generic` | Not quite right. Equate the two outcomes with the new price. | correct | B:screens[1] |
| l22-when-to-hedge.json | `.screens[1].feedback.byKey.old` | That is the evens answer. A better price on the hedge locks in more. | correct | B:screens[1] |
| l22-when-to-hedge.json | `.screens[1].explain.text` | Equating $500 - h$ with $2h - 100$ gives $h = 200$. Both outcomes then pay £300. A better hedge price costs less and lo… | correct | B:screens[1] |
| l22-when-to-hedge.json | `.screens[2].prose` | You want £100 on a best-of-seven series: +£100 if your team wins it, −£100 if not. You can only bet game by game at eve… | correct | B:screens[2] |
| l22-when-to-hedge.json | `.screens[2].hints[0].text` | At fair odds a node is worth the average of its two children. | imprecise | finding 1: the replication needs bets at evens, not odds that are fair to the true chance; sim: puzzles-L4-concepts-r2.py:the bets replicate +-100 exactly for a true game chance of 0.3, 0.5, 0.8 |
| l22-when-to-hedge.json | `.screens[2].hints[1].text` | After a win in game 1 you need +£31.25, the average of +£62.50 and £0. After a loss you need −£31.25. | correct | B:screens[2] |
| l22-when-to-hedge.json | `.screens[2].hints[2].text` | Bet £31.25: a win takes £0 to +£31.25 and a loss to −£31.25. | correct | B:screens[2] |
| l22-when-to-hedge.json | `.screens[2].feedback.correct` | £31.25. | correct | B:screens[2] |
| l22-when-to-hedge.json | `.screens[2].feedback.generic` | Not quite right. Average the leaves to value each node after game 1. | correct | B:screens[2] |
| l22-when-to-hedge.json | `.screens[2].feedback.byKey.whole` | Betting £100 on game 1 is far more than the series bet. One game rarely decides a best-of-seven. | correct | B:screens[2] |
| l22-when-to-hedge.json | `.screens[2].feedback.byKey.seventh` | You spread £100 over seven games. The bets depend on the score. | correct | B:screens[2] |
| l22-when-to-hedge.json | `.screens[2].feedback.byKey.half` | That is the best-of-three bet. Seven games dilute game 1 more. | correct | B:screens[2] |
| l22-when-to-hedge.json | `.screens[2].explain.text` | Each node is worth the average of its children: ±£31.25 after game 1. Game 1 must move you from £0 to those values, so … | correct | B:screens[2] |
| l22-when-to-hedge.json | `.screens[3].prose` | The score is 1–1. Imagine games 4 to 7 played whatever happens. Game 3 matters only if it decides the series. | correct | B:screens[3] |
| l22-when-to-hedge.json | `.screens[3].hints[0].text` | Game 3 decides the series when the other four games split evenly. | correct | B:screens[3] |
| l22-when-to-hedge.json | `.screens[3].hints[1].text` | Games 4 to 7 split 2–2 with chance $\binom42/2^4 = \tfrac{6}{16}$. | correct | B:screens[3] |
| l22-when-to-hedge.json | `.screens[3].hints[2].text` | Bet $100 \times \tfrac{6}{16} = 37.5$. | correct | B:screens[3] |
| l22-when-to-hedge.json | `.screens[3].feedback.correct` | £37.50. | correct | B:screens[3] |
| l22-when-to-hedge.json | `.screens[3].feedback.generic` | Not quite right. Find the chance that game 3 decides the series. | correct | B:screens[3] |
| l22-when-to-hedge.json | `.screens[3].feedback.byKey.half` | That is the bet when two wins are needed by each side, at 2–2. | correct | B:screens[3] |
| l22-when-to-hedge.json | `.screens[3].explain.text` | If games 4 to 7 split 2–2, game 3 decides the series; otherwise it does not matter. That has chance $\tfrac{6}{16}$, so… | correct | B:screens[3] |
| l22-when-to-hedge.json | `.screens[4].prose` | You backed a team at 5 to 1 for £100, and you believe it now wins with chance 0.6. The other side is offered at evens. … | correct | B:screens[4] |
| l22-when-to-hedge.json | `.screens[4].widget.options[0].text` | £60 of expected profit: £260 unhedged against £200 locked | correct | B:screens[4] |
| l22-when-to-hedge.json | `.screens[4].widget.options[1].why` | At these odds the hedge bets against your edge. It costs £60 of expected profit. | correct | B:screens[4] |
| l22-when-to-hedge.json | `.screens[4].widget.options[2].why` | Removing risk does not add expectation. It swaps £260 of expected profit for a certain £200. | correct | B:screens[4] |
| l22-when-to-hedge.json | `.screens[4].hints[0].text` | Find the expected profit unhedged. | correct | B:screens[4] |
| l22-when-to-hedge.json | `.screens[4].hints[1].text` | $0.6 \times 500 - 0.4 \times 100$. | correct | B:screens[4] |
| l22-when-to-hedge.json | `.screens[4].hints[2].text` | £260 unhedged against £200 locked. | correct | B:screens[4] |
| l22-when-to-hedge.json | `.screens[4].feedback.correct` | £60 of expected profit. | correct | B:screens[4] |
| l22-when-to-hedge.json | `.screens[4].feedback.generic` | Not quite right. Compare the expected profit with the locked £200. | correct | B:screens[4] |
| l22-when-to-hedge.json | `.screens[4].feedback.byKey.b` | You called the hedge free. It bets on the side you think is the underdog, at evens. | correct | B:screens[4] |
| l22-when-to-hedge.json | `.screens[4].feedback.byKey.c` | A hedge cannot add expectation here. It trades £60 of it for certainty. | correct | B:screens[4] |
| l22-when-to-hedge.json | `.screens[4].explain.text` | Unhedged you expect $0.6 \times 500 - 0.4 \times 100 = £260$. The full hedge locks £200, giving back £60 of edge. Hedge… | correct | B:screens[4] |
| l22-when-to-hedge.json | `.screens[5].prose` | You hold that bet with a bankroll of £1,000 and believe $p = 0.6$. Use the log rule from l21 to size the hedge. | correct | B:screens[5] |
| l22-when-to-hedge.json | `.screens[5].widget.lines[0].text` | Unhedged, wealth ends at £1,500 with chance 0.6 or £900 with chance 0.4. | correct | B:screens[5] |
| l22-when-to-hedge.json | `.screens[5].widget.lines[1].text` | A hedge of $h$ at evens moves these to $1500 - h$ and $900 + h$. | correct | B:screens[5] |
| l22-when-to-hedge.json | `.screens[5].widget.lines[2].text` | Kelly picks $h$ to maximise $0.6\ln(1500 - h) + 0.4\ln(900 + h)$. | correct | B:screens[5] |
| l22-when-to-hedge.json | `.screens[5].widget.lines[3].text` | Set the derivative to zero: $\dfrac{0.6}{1500 - h} = \dfrac{0.4}{900 + h}$. | correct | B:screens[5] |
| l22-when-to-hedge.json | `.screens[5].widget.lines[4].text` | Cross-multiply: $540 + 0.6h = 600 - 0.4h$, so $h = 60$. | correct | B:screens[5] |
| l22-when-to-hedge.json | `.screens[5].widget.lines[5].text` | Hedge £60: wealth ends at £1,440 or £960. | correct | B:screens[5] |
| l22-when-to-hedge.json | `.screens[5].widget.lines[6].text` | Hedge £300 to lock in £1,200, since a certain amount beats a gamble. | correct | B:screens[5] |
| l22-when-to-hedge.json | `.screens[5].widget.lines[6].why` | A certain £1,200 has a lower expected log than the bet unhedged. | correct | B:screens[5] |
| l22-when-to-hedge.json | `.screens[5].hints[0].text` | Start from wealth in each outcome. | correct | B:screens[5] |
| l22-when-to-hedge.json | `.screens[5].hints[1].text` | Then add the hedge, take expected logs and differentiate. | correct | B:screens[5] |
| l22-when-to-hedge.json | `.screens[5].hints[2].text` | Outcomes, hedge, objective, derivative, solve, conclude. | correct | B:screens[5] |
| l22-when-to-hedge.json | `.screens[5].feedback.correct` | Hedge £60, not £300. | correct | B:screens[5] |
| l22-when-to-hedge.json | `.screens[5].feedback.generic` | Not quite right. Start from the two unhedged outcomes. | correct | B:screens[5] |
| l22-when-to-hedge.json | `.screens[5].feedback.byKey.d1` | A sure £1,200 has log 7.090, below the unhedged 7.109. Hedging fully gives away edge. | correct | B:screens[5] |
| l22-when-to-hedge.json | `.screens[5].feedback.byKey.left-out` | Every line except the full hedge belongs. | correct | B:screens[5] |
| l22-when-to-hedge.json | `.screens[5].feedback.byKey.s6` | The conclusion comes last. | correct | B:screens[5] |
| l22-when-to-hedge.json | `.screens[5].explain.text` | The expected log is 7.109 unhedged, 7.110 at $h = 60$ and 7.090 fully hedged. A small hedge trims the risk your bankrol… | correct | B:screens[5] |
| l22-when-to-hedge.json | `.screens[6].prose` | Each hedge copied the payoff you wanted with bets you could make, working back from the end. At evens a node is worth t… | correct | B:screens[6] |
| l22-when-to-hedge.json | `.screens[6].hints[0].text` | The bet is half the gap between the children. | correct | B:screens[6] |
| l22-when-to-hedge.json | `.screens[6].hints[1].text` | The gap is $50 - (-10) = 60$. | correct | B:screens[6] |
| l22-when-to-hedge.json | `.screens[6].hints[2].text` | Bet £30. | correct | B:screens[6] |
| l22-when-to-hedge.json | `.screens[6].feedback.correct` | £30. | correct | B:screens[6] |
| l22-when-to-hedge.json | `.screens[6].feedback.generic` | Not quite right. Halve the gap between the two values. | correct | B:screens[6] |
| l22-when-to-hedge.json | `.screens[6].feedback.byKey.gap` | That is the whole gap. A win adds the bet and a loss takes it away, so the bet is half the gap. | correct | B:screens[6] |
| l22-when-to-hedge.json | `.screens[6].feedback.byKey.avg` | That is the node's value. The bet is half the gap. | correct | B:screens[6] |
| l22-when-to-hedge.json | `.screens[6].explain.text` | The node is worth $\tfrac12(50 - 10) = £20$. A £30 bet takes it to £50 on a win or −£10 on a loss. So the bet is half t… | correct | B:screens[6] |
| l22-when-to-hedge.json | `.screens[7].prose` | Four puzzles at about 3 minutes each; keep your own time and say each argument aloud. Evens on every hedge. | correct | B:screens[7] |
| l22-when-to-hedge.json | `.screens[7].hints[0].text` | Equate the two outcomes; for the series, ask when a game decides it. | correct | B:screens[7] |
| l22-when-to-hedge.json | `.screens[7].hints[1].text` | $150 - h = h - 50$. | correct | B:screens[7] |
| l22-when-to-hedge.json | `.screens[7].hints[2].text` | Hedge £100 to lock £50. Game 1 is decisive with chance $\tfrac12$, and so is game 2 at 1–0. | correct | B:screens[7] |
| l22-when-to-hedge.json | `.screens[7].feedback.correct` | £100, £50, £50 and £50. | correct | B:screens[7] |
| l22-when-to-hedge.json | `.screens[7].feedback.generic` | Not quite right. Check the first answer that is marked. | correct | B:screens[7] |
| l22-when-to-hedge.json | `.screens[7].feedback.byKey.r0c1` | Solve $150 - h = h - 50$. | correct | B:screens[7] |
| l22-when-to-hedge.json | `.screens[7].feedback.byKey.r1c1` | Lock in $150 - 100$. | correct | B:screens[7] |
| l22-when-to-hedge.json | `.screens[7].feedback.byKey.r2c1` | Game 1 decides a best-of-three when games 2 and 3 split: chance $\tfrac12$. | correct | B:screens[7] |
| l22-when-to-hedge.json | `.screens[7].feedback.byKey.r3c1` | At 1–0, game 2 matters only if game 3 would be lost: chance $\tfrac12$. | correct | B:screens[7] |
| l22-when-to-hedge.json | `.screens[7].explain.text` | The hedge of £100 locks in £50 either way. Game 1 of a best-of-three decides it with chance $\tfrac12$, so bet £50. At … | correct | B:screens[7] |
| l22-when-to-hedge.json | `.screens[8].prose` | You found £31.25 for game 1 of a best-of-seven. The interviewer asks about a best-of-five, still £100 on the series. | correct | B:screens[8] |
| l22-when-to-hedge.json | `.screens[8].hints[0].text` | Imagine games 2 to 5 played. | correct | B:screens[8] |
| l22-when-to-hedge.json | `.screens[8].hints[1].text` | Game 1 decides the series when they split 2–2. | correct | B:screens[8] |
| l22-when-to-hedge.json | `.screens[8].hints[2].text` | $100 \times \binom42/2^4 = 37.5$. | correct | B:screens[8] |
| l22-when-to-hedge.json | `.screens[8].feedback.correct` | £37.50. | correct | B:screens[8] |
| l22-when-to-hedge.json | `.screens[8].feedback.generic` | Not quite right. Find the chance that games 2 to 5 split 2–2. | correct | B:screens[8] |
| l22-when-to-hedge.json | `.screens[8].feedback.byKey.seven` | That is the best-of-seven bet. A shorter series makes game 1 matter more. | correct | B:screens[8] |
| l22-when-to-hedge.json | `.screens[8].feedback.byKey.half` | That is the best-of-three bet. | correct | B:screens[8] |
| l22-when-to-hedge.json | `.screens[8].feedback.byKey.fifth` | You spread £100 over five games. The bet depends on how often game 1 decides it. | correct | B:screens[8] |
| l22-when-to-hedge.json | `.screens[8].explain.text` | Games 2 to 5 split 2–2 with chance $\binom42/2^4 = \tfrac38$. So bet $100 \times \tfrac38 = £37.50$ on game 1. Shorter … | correct | B:screens[8] |
| l22-when-to-hedge.json | `.screens[9].prose` | A share trades at £100 and will move to £110 or £90. A call option with strike £100 then pays £10 or £0. You sold the c… | correct | B:screens[9] |
| l22-when-to-hedge.json | `.screens[9].hints[0].text` | Match the call's two payoffs with shares. | correct | B:screens[9] |
| l22-when-to-hedge.json | `.screens[9].hints[1].text` | The call's payoff gap is £10; the share's gap is £20. | correct | B:screens[9] |
| l22-when-to-hedge.json | `.screens[9].hints[2].text` | Hold $10/20 = 0.5$ shares. | correct | B:screens[9] |
| l22-when-to-hedge.json | `.screens[9].feedback.correct` | Half a share per call. | correct | B:screens[9] |
| l22-when-to-hedge.json | `.screens[9].feedback.generic` | Not quite right. Divide the gap in the call's payoff by the gap in the share price. | correct | B:screens[9] |
| l22-when-to-hedge.json | `.screens[9].feedback.byKey.one` | One share moves £20 between the outcomes, twice the call's £10 gap. | correct | B:screens[9] |
| l22-when-to-hedge.json | `.screens[9].feedback.byKey.tenth` | You divided £10 by £100. Use the gap between the share's two prices. | correct | B:screens[9] |
| l22-when-to-hedge.json | `.screens[9].explain.text` | The call's payoff changes by £10 when the share's price changes by £20, so hold 0.5 shares. That is the series bet agai… | correct | B:screens[9] |
| l22-when-to-hedge.json | `.summary.ideas[0]` | To lock a profit, size the hedge so both outcomes pay the same. | correct | B:summary |
| l22-when-to-hedge.json | `.summary.ideas[1]` | At evens the bet is half the gap between the next two values: stake times the chance this game decides. | correct | B:summary |
| l22-when-to-hedge.json | `.summary.ideas[2]` | A fair hedge cuts variance, not expectation; a worse one gives back edge. Hedge only what the bankroll needs. | correct | B:summary |
| l22-when-to-hedge.json | `.summary.formula.note` | $r$ and $s$ are the wins each side still needs; $S$ is the series stake. | correct | B:summary |
| l22-when-to-hedge.json | `.summary.trap` | Hedging every bet, or calling a hedge at bad odds free. It gives back the edge. | correct | B:summary |
| l22-when-to-hedge.json | `.quiz[0].prose` | You backed a team at 5 to 1 for £100, and its true chance is now $\tfrac12$. You hedge £300 at evens. | correct | B:quiz[0] |
| l22-when-to-hedge.json | `.quiz[0].widget.options[0].text` | It stays £200: the hedge cuts the spread, not the expectation | correct | B:quiz[0] |
| l22-when-to-hedge.json | `.quiz[0].widget.options[1].why` | Removing risk does not add expectation. Unhedged you also expect $250 - 50 = £200$. | correct | B:quiz[0] |
| l22-when-to-hedge.json | `.quiz[0].widget.options[2].why` | At fair odds the hedge has zero expected value, so it costs nothing. | correct | B:quiz[0] |
| l22-when-to-hedge.json | `.quiz[0].feedback.correct` | It stays at £200. | correct | B:quiz[0] |
| l22-when-to-hedge.json | `.quiz[0].feedback.generic` | Not quite right. Compute the expected profit unhedged. | correct | B:quiz[0] |
| l22-when-to-hedge.json | `.quiz[0].explain.text` | Unhedged: $\tfrac12 \times 500 - \tfrac12 \times 100 = £200$. Hedged: a certain £200. This is the edge case: a hedge at… | correct | B:quiz[0] |
| l22-when-to-hedge.json | `.quiz[1].prose` | £100 on a best-of-seven, game by game at evens. The score is 3–3. | correct | B:quiz[1] |
| l22-when-to-hedge.json | `.quiz[1].feedback.correct` | £100: the decider is the series. | correct | B:quiz[1] |
| l22-when-to-hedge.json | `.quiz[1].feedback.generic` | Not quite right. Does game 7 decide the series? | correct | B:quiz[1] |
| l22-when-to-hedge.json | `.quiz[1].feedback.byKey.half` | That is the bet at 2–2. At 3–3 game 7 settles everything. | correct | B:quiz[1] |
| l22-when-to-hedge.json | `.quiz[1].explain.text` | At 3–3 game 7 decides the series for certain. So the game bet equals the whole series bet, £100. | correct | B:quiz[1] |
| l22-when-to-hedge.json | `.quiz[2].prose` | You backed £20 at 4 to 1. The other side is offered at evens. | correct | B:quiz[2] |
| l22-when-to-hedge.json | `.quiz[2].feedback.correct` | £30, with a £50 hedge. | correct | B:quiz[2] |
| l22-when-to-hedge.json | `.quiz[2].feedback.generic` | Not quite right. Solve $80 - h = h - 20$. | correct | B:quiz[2] |
| l22-when-to-hedge.json | `.quiz[2].feedback.byKey.hedge` | That is the hedge. The locked profit is $80 - 50$. | correct | B:quiz[2] |
| l22-when-to-hedge.json | `.quiz[2].feedback.byKey.eighty` | That is the unhedged win. The hedge costs £50 of it. | correct | B:quiz[2] |
| l22-when-to-hedge.json | `.quiz[2].explain.text` | $80 - h = h - 20$ gives $h = 50$. Both outcomes then pay £30. | correct | B:quiz[2] |

## l23-doubling-up.json

### Bases

| key | basis |
|---|---|
| screens[0] | derivation E = (1-q^n) - q^n(2^n - 1) = 1 - (2q)^n; sim: puzzles-L4-concepts-r2.py:fair doubling cycle has expected gain 0 for every n; 2^-10, 2^-7, 2^-4; bankrolls 255, 15, 511; European red 6 doublings -0.1735 |
| screens[2] | derivation E = (1-q^n) - q^n(2^n - 1) = 1 - (2q)^n; sim: puzzles-L4-concepts-r2.py:fair doubling cycle has expected gain 0 for every n; 2^-10, 2^-7, 2^-4; bankrolls 255, 15, 511; European red 6 doublings -0.1735 |
| screens[6] | derivation E = (1-q^n) - q^n(2^n - 1) = 1 - (2q)^n; sim: puzzles-L4-concepts-r2.py:fair doubling cycle has expected gain 0 for every n; 2^-10, 2^-7, 2^-4; bankrolls 255, 15, 511; European red 6 doublings -0.1735 |
| screens[7] | derivation E = (1-q^n) - q^n(2^n - 1) = 1 - (2q)^n; sim: puzzles-L4-concepts-r2.py:fair doubling cycle has expected gain 0 for every n; 2^-10, 2^-7, 2^-4; bankrolls 255, 15, 511; European red 6 doublings -0.1735 |
| quiz[1] | derivation E = (1-q^n) - q^n(2^n - 1) = 1 - (2q)^n; sim: puzzles-L4-concepts-r2.py:fair doubling cycle has expected gain 0 for every n; 2^-10, 2^-7, 2^-4; bankrolls 255, 15, 511; European red 6 doublings -0.1735 |
| screens[1] | shape of the doubler's P&L: +1 with chance 1-2^-n, -(2^n-1) otherwise; sim: puzzles-L4-concepts-r2.py:fair doubling cycle expected gain 0 |
| screens[3] | sim: puzzles-L4-concepts-r2.py:European red 10 doublings -0.3056, 7 doublings -0.2052; q^n values; MC 400,000 cycles agrees within noise; per £ staked the edge is unchanged, per cycle larger |
| screens[9] | sim: puzzles-L4-concepts-r2.py:European red 10 doublings -0.3056, 7 doublings -0.2052; q^n values; MC 400,000 cycles agrees within noise; per £ staked the edge is unchanged, per cycle larger |
| screens[4] | sim: puzzles-L4-concepts-r2.py:at least one failure in 1,000 cycles: 0.6236; gambler's fallacy: flips independent (Feller vol. 1 VIII.4) |
| screens[5] | Williams, Probability with Martingales 10.10 (optional stopping, bounded T; non-negative supermartingale and Fatou) (bounded T: E[X_T] = X_0; finite bankroll makes wealth a non-negative supermartingale so E[X_T] <= X_0 for every T, Fatou); sim: puzzles-L4-concepts-r2.py:stop at +5 or after 100 bets: expected gain exactly 0; finite bankroll stop when ahead or ruined: 0; every stopping rule on a 4-step tree with a bankroll has mean <= 0 (exhaustive); unlimited doubler: expected stake and expected loss before the win diverge; MC a head eventually comes |
| summary | Williams, Probability with Martingales 10.10 (optional stopping, bounded T; non-negative supermartingale and Fatou) (bounded T: E[X_T] = X_0; finite bankroll makes wealth a non-negative supermartingale so E[X_T] <= X_0 for every T, Fatou); sim: puzzles-L4-concepts-r2.py:stop at +5 or after 100 bets: expected gain exactly 0; finite bankroll stop when ahead or ruined: 0; every stopping rule on a 4-step tree with a bankroll has mean <= 0 (exhaustive); unlimited doubler: expected stake and expected loss before the win diverge; MC a head eventually comes |
| quiz[0] | Williams, Probability with Martingales 10.10 (optional stopping, bounded T; non-negative supermartingale and Fatou) (bounded T: E[X_T] = X_0; finite bankroll makes wealth a non-negative supermartingale so E[X_T] <= X_0 for every T, Fatou); sim: puzzles-L4-concepts-r2.py:stop at +5 or after 100 bets: expected gain exactly 0; finite bankroll stop when ahead or ruined: 0; every stopping rule on a 4-step tree with a bankroll has mean <= 0 (exhaustive); unlimited doubler: expected stake and expected loss before the win diverge; MC a head eventually comes |
| screens[8] | shape comparison; sim: puzzles-L4-concepts-r2.py:option seller break-even L = 49,000; Kelly keeps losses proportional (MC double Kelly negative but no ruin) |
| screens[10] | sim: puzzles-L4-concepts-r2.py:L = 49,000 and 0.98^30 = 0.55 |
| quiz[2] | sim: puzzles-L4-concepts-r2.py:at least one failure in 1,000 cycles: 0.6236; (1023/1024)^1000 = 0.376 |

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l23-doubling-up.json | `.screens[0].prose` | You hold £7 and bet £1 on a fair coin. After a loss you double the stake; after a win you stop. £7 funds stakes of £1, … | correct | B:screens[0] |
| l23-doubling-up.json | `.screens[0].hints[0].text` | A win at any stage leaves you £1 up. | correct | B:screens[0] |
| l23-doubling-up.json | `.screens[0].hints[1].text` | You lose all £7 only if all three bets lose: chance $\tfrac18$. | correct | B:screens[0] |
| l23-doubling-up.json | `.screens[0].hints[2].text` | $\tfrac78 \times 1 - \tfrac18 \times 7$. | correct | B:screens[0] |
| l23-doubling-up.json | `.screens[0].feedback.correct` | Zero: the cycle is a fair bet. | correct | B:screens[0] |
| l23-doubling-up.json | `.screens[0].feedback.generic` | Not quite right. Weight each outcome by its chance. | correct | B:screens[0] |
| l23-doubling-up.json | `.screens[0].feedback.byKey.one` | You counted only the wins. One cycle in eight loses £7. | correct | B:screens[0] |
| l23-doubling-up.json | `.screens[0].feedback.byKey.p` | That is the chance of winning £1, not the expected gain. | correct | B:screens[0] |
| l23-doubling-up.json | `.screens[0].explain.text` | You win £1 with chance $\tfrac78$ and lose £7 with chance $\tfrac18$. The expected gain is $\tfrac78 - \tfrac78 = 0$. T… | correct | B:screens[0] |
| l23-doubling-up.json | `.screens[1].prose` | Now a doubler starts with £63 and plays cycle after cycle on a fair coin. The top panel is the coin; the bottom panel i… | correct | B:screens[1] |
| l23-doubling-up.json | `.screens[1].widget.options[0].text` | Small steady gains, then a rare sharp drop | correct | B:screens[1] |
| l23-doubling-up.json | `.screens[1].widget.options[1].why` | Watch longer: a run of losses takes the whole doubled stake at once. | correct | B:screens[1] |
| l23-doubling-up.json | `.screens[1].widget.options[2].why` | The gains are small and frequent; the losses are rare and large. The shape is lopsided. | correct | B:screens[1] |
| l23-doubling-up.json | `.screens[1].hints[0].text` | Follow one bankroll path. | correct | B:screens[1] |
| l23-doubling-up.json | `.screens[1].hints[1].text` | Most steps add £1 over a cycle. | correct | B:screens[1] |
| l23-doubling-up.json | `.screens[1].hints[2].text` | A run of six losses costs £63 in one go. | correct | B:screens[1] |
| l23-doubling-up.json | `.screens[1].feedback.correct` | Small gains, rare large losses. | correct | B:screens[1] |
| l23-doubling-up.json | `.screens[1].feedback.generic` | Not quite right. Look at the bottom panel over several runs. | correct | B:screens[1] |
| l23-doubling-up.json | `.screens[1].explain.text` | Each cycle usually adds £1, so the bankroll creeps up. A run of losses then removes many cycles' gains at once. On aver… | correct | B:screens[1] |
| l23-doubling-up.json | `.screens[2].prose` | Now start with £1,023 and double from £1 after each loss. The ledger shows what each bet costs. | correct | B:screens[2] |
| l23-doubling-up.json | `.screens[2].hints[0].text` | The cycle fails only if all ten bets lose. | correct | B:screens[2] |
| l23-doubling-up.json | `.screens[2].hints[1].text` | That has chance $2^{-10} = \tfrac{1}{1024}$, and costs £1,023. | correct | B:screens[2] |
| l23-doubling-up.json | `.screens[2].hints[2].text` | $\tfrac{1023}{1024} \times 1 - \tfrac{1}{1024} \times 1023 = 0$. | correct | B:screens[2] |
| l23-doubling-up.json | `.screens[2].feedback.correct` | $\tfrac{1}{1024}$ and £0. | correct | B:screens[2] |
| l23-doubling-up.json | `.screens[2].feedback.generic` | Not quite right. Check the first answer that is marked. | correct | B:screens[2] |
| l23-doubling-up.json | `.screens[2].feedback.byKey.r0c1` | Ten fair losses in a row have chance $(\tfrac12)^{10} = \tfrac{1}{1024}$. | correct | B:screens[2] |
| l23-doubling-up.json | `.screens[2].feedback.byKey.r1c1` | Weight the £1 win by $\tfrac{1023}{1024}$ and the £1,023 loss by $\tfrac{1}{1024}$. | correct | B:screens[2] |
| l23-doubling-up.json | `.screens[2].explain.text` | The cycle loses with chance $\tfrac{1}{1024} \approx 0.000977$. Then it costs £1,023, which exactly cancels the £1 won … | correct | B:screens[2] |
| l23-doubling-up.json | `.screens[3].prose` | The same ten doublings, betting on red at a European wheel. Red wins with chance $\tfrac{18}{37}$ and pays evens. | correct | B:screens[3] |
| l23-doubling-up.json | `.screens[3].widget.accept` | 1 − 1024(19/37)¹⁰, about −0.3056 | correct | B:screens[3] |
| l23-doubling-up.json | `.screens[3].hints[0].text` | The cycle loses with chance $q^{10}$, where $q = \tfrac{19}{37}$. | correct | B:screens[3] |
| l23-doubling-up.json | `.screens[3].hints[1].text` | $q^{10} \approx 0.001275$. | correct | B:screens[3] |
| l23-doubling-up.json | `.screens[3].hints[2].text` | $(1 - q^{10}) - 1023\,q^{10} = 1 - 1024\,q^{10} \approx -0.3056$. | correct | B:screens[3] |
| l23-doubling-up.json | `.screens[3].feedback.correct` | About $-£0.31$ a cycle. | correct | B:screens[3] |
| l23-doubling-up.json | `.screens[3].feedback.generic` | Not quite right. Use $q = \tfrac{19}{37}$ for a loss. | correct | B:screens[3] |
| l23-doubling-up.json | `.screens[3].feedback.byKey.fair` | That is the fair-coin answer. Each red bet loses slightly more often than it wins. | correct | B:screens[3] |
| l23-doubling-up.json | `.screens[3].feedback.byKey.one` | That is the edge on one £1 bet. A cycle stakes up to £1,023. | correct | B:screens[3] |
| l23-doubling-up.json | `.screens[3].feedback.byKey.pos` | Check the sign. The rare loss outweighs the wins. | correct | B:screens[3] |
| l23-doubling-up.json | `.screens[3].explain.text` | $q^{10} = (\tfrac{19}{37})^{10} \approx 0.001275$, so the gain is $1 - 1024 \times 0.001275 \approx -0.3056$. A simulat… | correct | B:screens[3] |
| l23-doubling-up.json | `.screens[4].prose` | A friend plays the £1,023 doubling on a fair coin. He says ten losses in a row are so rare that the strategy is safe mo… | correct | B:screens[4] |
| l23-doubling-up.json | `.screens[4].widget.options[0].text` | The rare loss is sized to cancel the steady wins, so the expectation stays 0 | correct | B:screens[4] |
| l23-doubling-up.json | `.screens[4].widget.options[1].why` | Its size is £1,023, a thousand cycles of winnings. Rare and large still counts. | correct | B:screens[4] |
| l23-doubling-up.json | `.screens[4].widget.options[2].why` | That is the gambler's fallacy. The tenth flip is still fair. | correct | B:screens[4] |
| l23-doubling-up.json | `.screens[4].widget.options[3].why` | Every bet is a fair coin, whatever the stake. | correct | B:screens[4] |
| l23-doubling-up.json | `.screens[4].hints[0].text` | Multiply the chance by the size. | correct | B:screens[4] |
| l23-doubling-up.json | `.screens[4].hints[1].text` | $\tfrac{1}{1024} \times 1023$. | correct | B:screens[4] |
| l23-doubling-up.json | `.screens[4].hints[2].text` | That cancels the $\tfrac{1023}{1024} \times 1$ won. | correct | B:screens[4] |
| l23-doubling-up.json | `.screens[4].feedback.correct` | Rare, but sized to match. | correct | B:screens[4] |
| l23-doubling-up.json | `.screens[4].feedback.generic` | Not quite right. Weigh the loss by its size, not only its chance. | correct | B:screens[4] |
| l23-doubling-up.json | `.screens[4].feedback.byKey.b` | You looked only at the chance. The loss is £1,023, so it carries as much weight as all the wins. | correct | B:screens[4] |
| l23-doubling-up.json | `.screens[4].feedback.byKey.c` | That is the gambler's fallacy from conditional l22. Each flip is fair. | correct | B:screens[4] |
| l23-doubling-up.json | `.screens[4].explain.text` | The loss has chance $\tfrac{1}{1024}$ and size £1,023, exactly cancelling the steady £1 wins. Over 1,000 cycles the cha… | correct | B:screens[4] |
| l23-doubling-up.json | `.screens[5].prose` | Every doubler met the same wall. **Optional stopping**: in a fair game with a finite bankroll, no rule for when to stop… | correct | B:screens[5] |
| l23-doubling-up.json | `.screens[5].widget.options[0].text` | £0 | correct | B:screens[5] |
| l23-doubling-up.json | `.screens[5].widget.options[1].why` | He reaches £5 up only some of the time; the other runs end below. | correct | B:screens[5] |
| l23-doubling-up.json | `.screens[5].widget.options[2].why` | Stopping when ahead feels like an edge, but the runs that end behind cancel it. | correct | B:screens[5] |
| l23-doubling-up.json | `.screens[5].hints[0].text` | Is the game fair, and is the time bounded? | correct | B:screens[5] |
| l23-doubling-up.json | `.screens[5].hints[1].text` | Both: fair bets and at most 100 of them. | correct | B:screens[5] |
| l23-doubling-up.json | `.screens[5].hints[2].text` | So the expected gain stays at £0. | correct | B:screens[5] |
| l23-doubling-up.json | `.screens[5].feedback.correct` | £0. | correct | B:screens[5] |
| l23-doubling-up.json | `.screens[5].feedback.generic` | Not quite right. Apply optional stopping. | correct | B:screens[5] |
| l23-doubling-up.json | `.screens[5].explain.text` | The game is fair and stops within 100 bets, so the expected gain is £0. With unlimited money and time the doubler wins … | correct | B:screens[5] |
| l23-doubling-up.json | `.screens[6].prose` | Show that any doubling cycle on a fair coin has expected gain 0. It starts at £1 and allows $n$ bets. | correct | B:screens[6] |
| l23-doubling-up.json | `.screens[6].widget.lines[0].text` | A win at any of the $n$ bets leaves you £1 up: each stake covers the earlier losses plus £1. | correct | B:screens[6] |
| l23-doubling-up.json | `.screens[6].widget.lines[1].text` | The cycle fails only if all $n$ bets lose, with chance $2^{-n}$. | correct | B:screens[6] |
| l23-doubling-up.json | `.screens[6].widget.lines[2].text` | Then you have lost $1 + 2 + \dots + 2^{n-1} = 2^n - 1$. | correct | B:screens[6] |
| l23-doubling-up.json | `.screens[6].widget.lines[3].text` | So $E[\text{gain}] = (1 - 2^{-n}) \times 1 - 2^{-n}(2^n - 1)$. | correct | B:screens[6] |
| l23-doubling-up.json | `.screens[6].widget.lines[4].text` | Expand: $1 - 2^{-n} - 1 + 2^{-n} = 0$, for every $n$. | correct | B:screens[6] |
| l23-doubling-up.json | `.screens[6].widget.lines[5].text` | The chance of failing tends to 0 as $n$ grows, so the gain tends to £1. | correct | B:screens[6] |
| l23-doubling-up.json | `.screens[6].widget.lines[5].why` | The loss grows as fast as its chance shrinks. Their product is $1 - 2^{-n}$, exactly the chance of winning £1. | correct | B:screens[6] |
| l23-doubling-up.json | `.screens[6].hints[0].text` | Find the win, the failure chance and the failure size. | correct | B:screens[6] |
| l23-doubling-up.json | `.screens[6].hints[1].text` | The failure chance and size can go in either order. | correct | B:screens[6] |
| l23-doubling-up.json | `.screens[6].hints[2].text` | Win, failure, size, expectation, algebra. | correct | B:screens[6] |
| l23-doubling-up.json | `.screens[6].feedback.correct` | Zero for every $n$. | correct | B:screens[6] |
| l23-doubling-up.json | `.screens[6].feedback.generic` | Not quite right. Start from what a win gives. | correct | B:screens[6] |
| l23-doubling-up.json | `.screens[6].feedback.byKey.d1` | The failure chance halves and the loss about doubles, so their product is $1 - 2^{-n}$, not 1. That is exactly the chan… | correct | B:screens[6] |
| l23-doubling-up.json | `.screens[6].feedback.byKey.left-out` | Every line except the limit argument belongs. | correct | B:screens[6] |
| l23-doubling-up.json | `.screens[6].feedback.byKey.s5` | The algebra comes last. | correct | B:screens[6] |
| l23-doubling-up.json | `.screens[6].explain.text` | The failure chance halves with each extra bet, and the failure cost doubles. So their product, $2^{-n}(2^n - 1)$, cance… | correct | B:screens[6] |
| l23-doubling-up.json | `.screens[7].prose` | Three puzzles at about 3 minutes each; keep your own time and say each argument aloud. Give four decimal places. | correct | B:screens[7] |
| l23-doubling-up.json | `.screens[7].hints[0].text` | £63 funds six bets: $1 + 2 + \dots + 32$. | correct | B:screens[7] |
| l23-doubling-up.json | `.screens[7].hints[1].text` | On red, $q = \tfrac{19}{37}$ and $q^6 \approx 0.01834$. | correct | B:screens[7] |
| l23-doubling-up.json | `.screens[7].hints[2].text` | $\tfrac{1}{128}$, then $0$, then $1 - 64q^6$. | correct | B:screens[7] |
| l23-doubling-up.json | `.screens[7].feedback.correct` | $0.0078$, $0$ and $-0.1735$. | correct | B:screens[7] |
| l23-doubling-up.json | `.screens[7].feedback.generic` | Not quite right. Check the first answer that is marked. | correct | B:screens[7] |
| l23-doubling-up.json | `.screens[7].feedback.byKey.r0c1` | $(\tfrac12)^7 = \tfrac{1}{128}$. | correct | B:screens[7] |
| l23-doubling-up.json | `.screens[7].feedback.byKey.r1c1` | A fair cycle has expected gain 0 whatever the bankroll. | correct | B:screens[7] |
| l23-doubling-up.json | `.screens[7].feedback.byKey.r2c1` | $1 - 64 \times (\tfrac{19}{37})^6$. | correct | B:screens[7] |
| l23-doubling-up.json | `.screens[7].explain.text` | Seven losses have chance $\tfrac{1}{128} \approx 0.0078$. A fair cycle is worth £0 for any bankroll. On red the £63 cyc… | correct | B:screens[7] |
| l23-doubling-up.json | `.screens[8].prose` | One more, about a minute. A fund sells options that rarely pay out. Most months it keeps a small premium; now and then … | correct | B:screens[8] |
| l23-doubling-up.json | `.screens[8].widget.options[0].text` | Doubling after each loss | correct | B:screens[8] |
| l23-doubling-up.json | `.screens[8].widget.options[1].why` | That is the mirror image: small steady losses and rare large gains. | correct | B:screens[8] |
| l23-doubling-up.json | `.screens[8].widget.options[2].why` | Kelly sizing keeps losses in proportion to wealth. It has no hidden cliff. | correct | B:screens[8] |
| l23-doubling-up.json | `.screens[8].widget.options[3].why` | A fair hedge removes variance. It does not create a rare large loss. | correct | B:screens[8] |
| l23-doubling-up.json | `.screens[8].hints[0].text` | Describe the profit and loss in words. | correct | B:screens[8] |
| l23-doubling-up.json | `.screens[8].hints[1].text` | Small, frequent gains; rare, large losses. | correct | B:screens[8] |
| l23-doubling-up.json | `.screens[8].hints[2].text` | Which strategy in this lesson looked like that? | correct | B:screens[8] |
| l23-doubling-up.json | `.screens[8].feedback.correct` | Doubling: small steady gains and a rare large loss. | correct | B:screens[8] |
| l23-doubling-up.json | `.screens[8].feedback.generic` | Not quite right. Match small steady gains with a rare large loss. | correct | B:screens[8] |
| l23-doubling-up.json | `.screens[8].feedback.byKey.b` | You flipped the shape. Lottery tickets lose a little often and win big rarely. | correct | B:screens[8] |
| l23-doubling-up.json | `.screens[8].explain.text` | Selling options that rarely pay out collects small premiums and sometimes pays a large sum. That is the doubler's bankr… | correct | B:screens[8] |
| l23-doubling-up.json | `.screens[9].prose` | You found $-0.3056$ for ten doublings on European red. The interviewer asks about £127, enough for seven doublings. | correct | B:screens[9] |
| l23-doubling-up.json | `.screens[9].widget.accept` | 1 − 128(19/37)⁷, about −0.2052 | correct | B:screens[9] |
| l23-doubling-up.json | `.screens[9].hints[0].text` | £127 funds stakes of £1 to £64: seven bets. | correct | B:screens[9] |
| l23-doubling-up.json | `.screens[9].hints[1].text` | $q^7 = (\tfrac{19}{37})^7 \approx 0.009416$. | correct | B:screens[9] |
| l23-doubling-up.json | `.screens[9].hints[2].text` | $1 - 128\,q^7 \approx -0.2052$. | correct | B:screens[9] |
| l23-doubling-up.json | `.screens[9].feedback.correct` | About $-£0.21$ a cycle. | correct | B:screens[9] |
| l23-doubling-up.json | `.screens[9].feedback.generic` | Not quite right. Use seven bets and $q = \tfrac{19}{37}$. | correct | B:screens[9] |
| l23-doubling-up.json | `.screens[9].feedback.byKey.fair` | That is the fair-coin answer. | correct | B:screens[9] |
| l23-doubling-up.json | `.screens[9].feedback.byKey.ten` | That is the ten-doubling answer. Seven doublings risk less per cycle. | correct | B:screens[9] |
| l23-doubling-up.json | `.screens[9].feedback.byKey.pos` | Check the sign. The rare loss outweighs the wins. | correct | B:screens[9] |
| l23-doubling-up.json | `.screens[9].explain.text` | $q^7 \approx 0.009416$, so the gain is $1 - 128 \times 0.009416 \approx -0.2052$. A simulation of 400,000 cycles agrees… | correct | B:screens[9] |
| l23-doubling-up.json | `.screens[10].prose` | A fund sells options each month. With chance 0.98 it keeps a £1,000 premium. With chance 0.02 the options pay out and t… | correct | B:screens[10] |
| l23-doubling-up.json | `.screens[10].hints[0].text` | Set $0.98 \times 1000 - 0.02L = 0$. | correct | B:screens[10] |
| l23-doubling-up.json | `.screens[10].hints[1].text` | $0.02L = 980$. | correct | B:screens[10] |
| l23-doubling-up.json | `.screens[10].hints[2].text` | $L = 49{,}000$. | correct | B:screens[10] |
| l23-doubling-up.json | `.screens[10].feedback.correct` | £49,000. | correct | B:screens[10] |
| l23-doubling-up.json | `.screens[10].feedback.generic` | Not quite right. Equate the expected premium with the expected loss. | correct | B:screens[10] |
| l23-doubling-up.json | `.screens[10].feedback.byKey.fifty` | You used $1000/0.02$. The premium comes only in the good months, with chance 0.98. | correct | B:screens[10] |
| l23-doubling-up.json | `.screens[10].feedback.byKey.prem` | That is the premium. The loss must be far larger to balance it. | correct | B:screens[10] |
| l23-doubling-up.json | `.screens[10].feedback.byKey.twenty` | Check the arithmetic: $980/0.02$. | correct | B:screens[10] |
| l23-doubling-up.json | `.screens[10].explain.text` | $0.98 \times 1000 = 980$, so $L = 980/0.02 = £49{,}000$. Thirty good months in a row have chance $0.98^{30} \approx 0.5… | correct | B:screens[10] |
| l23-doubling-up.json | `.summary.ideas[0]` | Doubling wins a small amount often and loses a large amount rarely; on a fair coin they cancel exactly. | correct | B:summary |
| l23-doubling-up.json | `.summary.ideas[1]` | Optional stopping: with a finite bankroll, no stopping rule can raise a fair game's expectation, and one that must end … | correct | B:summary |
| l23-doubling-up.json | `.summary.ideas[2]` | On an unfair game doubling enlarges the loss per cycle. Selling rarely paying options has the same shape. | correct | B:summary |
| l23-doubling-up.json | `.summary.formula.note` | Zero when $q = \tfrac12$; negative when $q > \tfrac12$. | correct | B:summary |
| l23-doubling-up.json | `.summary.trap` | Calling the strategy safe because ten losses in a row are rare. The loss is sized to cancel the wins. | correct | B:summary |
| l23-doubling-up.json | `.quiz[0].prose` | A doubler has unlimited money and unlimited time, on a fair coin. | correct | B:quiz[0] |
| l23-doubling-up.json | `.quiz[0].widget.options[0].text` | He wins £1 for sure, but the expected stake he must risk is infinite | correct | B:quiz[0] |
| l23-doubling-up.json | `.quiz[0].widget.options[1].why` | It needs unlimited money. With any real bankroll the expected gain is 0. | correct | B:quiz[0] |
| l23-doubling-up.json | `.quiz[0].widget.options[2].why` | On a fair coin each bet is fair. The trouble is the size of the risk, not a negative mean. | correct | B:quiz[0] |
| l23-doubling-up.json | `.quiz[0].feedback.correct` | A sure £1, at an infinite expected risk. | correct | B:quiz[0] |
| l23-doubling-up.json | `.quiz[0].feedback.generic` | Not quite right. Ask what the guarantee needs. | correct | B:quiz[0] |
| l23-doubling-up.json | `.quiz[0].explain.text` | With no limit, a head eventually comes and he is £1 up. The money he must risk before then has infinite expectation. Th… | correct | B:quiz[0] |
| l23-doubling-up.json | `.quiz[1].prose` | A doubler holds £15 and plays one cycle on a fair coin. | correct | B:quiz[1] |
| l23-doubling-up.json | `.quiz[1].widget.accept` | 1/16 | correct | B:quiz[1] |
| l23-doubling-up.json | `.quiz[1].feedback.correct` | $\tfrac{1}{16} = 0.0625$. | correct | B:quiz[1] |
| l23-doubling-up.json | `.quiz[1].feedback.generic` | Not quite right. Count the bets £15 funds. | correct | B:quiz[1] |
| l23-doubling-up.json | `.quiz[1].feedback.byKey.eighth` | That is three bets. £15 funds four: 1 + 2 + 4 + 8. | correct | B:quiz[1] |
| l23-doubling-up.json | `.quiz[1].feedback.byKey.fifteen` | You took $\tfrac{1}{15}$. Count bets, not pounds. | correct | B:quiz[1] |
| l23-doubling-up.json | `.quiz[1].explain.text` | £15 funds stakes of £1, £2, £4 and £8: four bets. All four lose with chance $\tfrac{1}{16}$. | correct | B:quiz[1] |
| l23-doubling-up.json | `.quiz[2].prose` | A doubler with £1,023 plays 1,000 cycles on a fair coin, topping up after any loss. | correct | B:quiz[2] |
| l23-doubling-up.json | `.quiz[2].widget.accept` | 1 − (1023/1024)¹⁰⁰⁰, about 0.6236 | correct | B:quiz[2] |
| l23-doubling-up.json | `.quiz[2].feedback.correct` | About $0.6236$. | correct | B:quiz[2] |
| l23-doubling-up.json | `.quiz[2].feedback.generic` | Not quite right. Find the chance that all 1,000 cycles succeed. | correct | B:quiz[2] |
| l23-doubling-up.json | `.quiz[2].feedback.byKey.tiny` | That is the chance for one cycle. Over 1,000 cycles it adds up. | correct | B:quiz[2] |
| l23-doubling-up.json | `.quiz[2].feedback.byKey.approx` | You multiplied $\tfrac{1}{1024}$ by 1,000. Use the chance that none fail instead. | correct | B:quiz[2] |
| l23-doubling-up.json | `.quiz[2].explain.text` | Every cycle succeeds with chance $\tfrac{1023}{1024}$, so all 1,000 succeed with $(\tfrac{1023}{1024})^{1000} \approx 0… | correct | B:quiz[2] |

## l24-mixed-set.json

### Bases

| key | basis |
|---|---|
| screens[0] | linearity, first-step analysis, Bayes, fair ruin, order statistics; sim: puzzles-L4-concepts-r2.py:coupon 5H5 = 137/12; 1 hat; 2.25 HH places; two sixes in a row = 42; Bayes 19/117; fair ruin from 4 to 12: 1/3; E[max of 4 uniforms] = 4/5 |
| screens[1] | ghost (pass-through) argument; sim: puzzles-L4-concepts-r2.py:ants: every direction set clears the stick within one minute |
| screens[2] | Bayes then predictive; sim: puzzles-L4-concepts-r2.py:P(two-headed \| HH) = 4/5, next head 0.9; MC 200,000 picks |
| screens[3] | Williams, Probability with Martingales 10.10 (optional stopping, bounded T; non-negative supermartingale and Fatou); sim: puzzles-L4-concepts-r2.py:bankrolls 255 (8 bets); fair doubling cycle expected gain 0 |
| screens[4] | Berlekamp, Conway and Guy, Winning Ways vol. 1 ch. 2 (subtraction games, P-positions); sim: puzzles-L4-concepts-r2.py:from 40 with takes 1..5 take 4 |
| screens[5] | scale invariance; sim: puzzles-L4-concepts-r2.py:MC uniforms on [0,2] exceeding 2: ~e; sum 1/n! = e |
| screens[6] | geometric probability; sim: puzzles-L4-concepts-r2.py:meeting 7/16 |
| screens[7] | Laplace rule of succession (s+1)/(n+2) under a uniform (Beta(1,1)) prior; sim: puzzles-L4-concepts-r2.py:Laplace 3/4 exact for finite urns with a uniform prior on the mix; 3R1B gives 1/2, 9R1B gives 7/8 |
| screens[8] | sim: puzzles-L4-concepts-r2.py:five points in a semicircle 5/16; meeting 5/9; Buffon 1/pi; expected distance on [0,3] is 1; 4-sided die first 1: 4/7; Kelly 0.3 |
| screens[9] | backward induction; sim: puzzles-L4-concepts-r2.py:three rolls of an 8-sided die: 4.5, 5.5, 97/16; MC 200,000 games |
| screens[10] | Hoehn and Niven (1985) and Gardner, Penney-ante (Sci. Am. 1974); sim: puzzles-L4-concepts-r2.py:P(HHT before HTT) = 2/3; THT vs HTT 1/2; TTH vs HTT 1/4; HHH vs HTT 2/5 |
| screens[11] | sim: puzzles-L4-concepts-r2.py:hedge 100 locks 60 |
| summary | formulas checked above: nH_n, 1/(2-p), p - q/b, k/N, e |
| quiz[0] | linearity of expectation needs no independence; sim: puzzles-L4-concepts-r2.py:expected faces seen 3.9906 |
| quiz[1] | sim: puzzles-L4-concepts-r2.py:Kelly(0.3, 4) = 0.125 |
| quiz[2] | two protocols; sim: puzzles-L4-concepts-r2.py:1/3 or 1/2 depending on how the boy was revealed |

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l24-mixed-set.json | `.screens[0].prose` | Twenty unlabelled puzzles from every level, in three styles: short, multi-stage and strategic. Give each short one abou… | correct | B:screens[0] |
| l24-mixed-set.json | `.screens[0].hints[0].text` | Name each family before you compute. | correct | B:screens[0] |
| l24-mixed-set.json | `.screens[0].hints[1].text` | Coupons, hats, indicators, a pattern wait, Bayes, ruin, a maximum. | correct | B:screens[0] |
| l24-mixed-set.json | `.screens[0].hints[2].text` | $5H_5$, 1, $9 \times \tfrac14$, $6 + 36$, $\tfrac{0.019}{0.019 + 0.098}$, $\tfrac4{12}$, $\tfrac45$. | correct | B:screens[0] |
| l24-mixed-set.json | `.screens[0].feedback.correct` | $11.4167$, $1$, $2.25$, $42$, $0.1624$, $0.3333$ and $0.8$. | correct | B:screens[0] |
| l24-mixed-set.json | `.screens[0].feedback.generic` | Not quite right. Check the first answer that is marked. | correct | B:screens[0] |
| l24-mixed-set.json | `.screens[0].feedback.byKey.r0c1` | Not $5^2$: the waits for each new face are $\tfrac55 + \tfrac54 + \dots + \tfrac51 = \tfrac{137}{12}$. | correct | B:screens[0] |
| l24-mixed-set.json | `.screens[0].feedback.byKey.r1c1` | Each coat comes back with chance $\tfrac{1}{12}$, and there are 12. | correct | B:screens[0] |
| l24-mixed-set.json | `.screens[0].feedback.byKey.r2c1` | There are 9 adjacent pairs in 10 flips, each HH with chance $\tfrac14$. | correct | B:screens[0] |
| l24-mixed-set.json | `.screens[0].feedback.byKey.r3c1` | Not 36: a miss after one six restarts the wait, so $6 + 36 = 42$. | correct | B:screens[0] |
| l24-mixed-set.json | `.screens[0].feedback.byKey.r4c1` | Not 0.95: divide the true flags, 0.019, by all flags, 0.117. | correct | B:screens[0] |
| l24-mixed-set.json | `.screens[0].feedback.byKey.r5c1` | A fair game keeps the mean at £4: $12P = 4$. | correct | B:screens[0] |
| l24-mixed-set.json | `.screens[0].feedback.byKey.r6c1` | The largest of $n$ uniforms has mean $\tfrac{n}{n + 1}$. | correct | B:screens[0] |
| l24-mixed-set.json | `.screens[0].explain.text` | Each answer is one line once the family is named. The coupon wait is $\tfrac{137}{12}$ and the Bayes answer $\tfrac{19}… | correct | B:screens[0] |
| l24-mixed-set.json | `.screens[1].prose` | Recognising the family is half the answer. Five ants on a one-metre stick walk at 1 m a minute in random directions. Tw… | correct | B:screens[1] |
| l24-mixed-set.json | `.screens[1].widget.options[0].text` | Pretend the ants pass through each other | correct | B:screens[1] |
| l24-mixed-set.json | `.screens[1].widget.options[1].why` | The state space is huge. The swap trick removes it. | correct | B:screens[1] |
| l24-mixed-set.json | `.screens[1].widget.options[2].why` | Indicators give expected counts, not the longest time. | correct | B:screens[1] |
| l24-mixed-set.json | `.screens[1].widget.options[3].why` | There is no choice to make. The motion is fixed once directions are set. | correct | B:screens[1] |
| l24-mixed-set.json | `.screens[1].hints[0].text` | What changes if two meeting ants swap labels? | correct | B:screens[1] |
| l24-mixed-set.json | `.screens[1].hints[1].text` | Nothing you can see: the set of positions is the same. | correct | B:screens[1] |
| l24-mixed-set.json | `.screens[1].hints[2].text` | So each ant falls within one minute. | correct | B:screens[1] |
| l24-mixed-set.json | `.screens[1].feedback.correct` | Pass-through symmetry: at most one minute. | correct | B:screens[1] |
| l24-mixed-set.json | `.screens[1].feedback.generic` | Not quite right. Ignore the labels on the ants. | correct | B:screens[1] |
| l24-mixed-set.json | `.screens[1].explain.text` | Swapping labels at each meeting leaves the positions unchanged. So the ants behave like ghosts walking straight on. The… | correct | B:screens[1] |
| l24-mixed-set.json | `.screens[2].prose` | About 4 minutes. A bag holds a fair coin and a two-headed coin. You pick one at random and flip it twice: two heads. | correct | B:screens[2] |
| l24-mixed-set.json | `.screens[2].widget.accept` | 4/5 + 1/5 × 1/2 = 9/10 | correct | B:screens[2] |
| l24-mixed-set.json | `.screens[2].hints[0].text` | Stage one: update the chance it is the two-headed coin. | correct | B:screens[2] |
| l24-mixed-set.json | `.screens[2].hints[1].text` | $\tfrac{1/2}{1/2 + 1/8} = \tfrac45$. | correct | B:screens[2] |
| l24-mixed-set.json | `.screens[2].hints[2].text` | Stage two: $\tfrac45 \times 1 + \tfrac15 \times \tfrac12$. | correct | B:screens[2] |
| l24-mixed-set.json | `.screens[2].feedback.correct` | $\tfrac{9}{10}$. | correct | B:screens[2] |
| l24-mixed-set.json | `.screens[2].feedback.generic` | Not quite right. Update the coin first, then predict. | correct | B:screens[2] |
| l24-mixed-set.json | `.screens[2].feedback.byKey.prior` | You skipped the update. Two heads make the two-headed coin likelier. | correct | B:screens[2] |
| l24-mixed-set.json | `.screens[2].feedback.byKey.post` | That is the chance of the two-headed coin. A fair coin can still give a head. | correct | B:screens[2] |
| l24-mixed-set.json | `.screens[2].feedback.byKey.half` | You treated the coin as fair. The two heads are evidence. | correct | B:screens[2] |
| l24-mixed-set.json | `.screens[2].explain.text` | Two heads have chance $\tfrac12$ with the two-headed coin and $\tfrac18$ with the fair one, so its chance is $\tfrac45$… | correct | B:screens[2] |
| l24-mixed-set.json | `.screens[3].prose` | A gambler with £255 bets £1 on a fair coin and doubles after each loss. He stops at the first win. | correct | B:screens[3] |
| l24-mixed-set.json | `.screens[3].widget.options[0].text` | Optional stopping | correct | B:screens[3] |
| l24-mixed-set.json | `.screens[3].widget.options[1].why` | Kelly sizes a bet with an edge. Here there is no edge to size. | correct | B:screens[3] |
| l24-mixed-set.json | `.screens[3].widget.options[2].why` | Symmetry shows each flip is fair, but not what the doubling does. | correct | B:screens[3] |
| l24-mixed-set.json | `.screens[3].widget.options[3].why` | That only unrolls the cycle. Optional stopping finishes it at once. | correct | B:screens[3] |
| l24-mixed-set.json | `.screens[3].hints[0].text` | Is the game fair, and must the cycle end within a fixed number of bets? | correct | B:screens[3] |
| l24-mixed-set.json | `.screens[3].hints[1].text` | Yes and yes: eight bets at most. | correct | B:screens[3] |
| l24-mixed-set.json | `.screens[3].hints[2].text` | So the expected gain is 0. | correct | B:screens[3] |
| l24-mixed-set.json | `.screens[3].feedback.correct` | Optional stopping: the expected gain is 0. | correct | B:screens[3] |
| l24-mixed-set.json | `.screens[3].feedback.generic` | Not quite right. Ask what a stopping rule can do to a fair game. | correct | B:screens[3] |
| l24-mixed-set.json | `.screens[3].explain.text` | The bankroll funds eight bets, so the cycle loses £255 with chance $\tfrac{1}{256}$. That cancels the £1 won otherwise.… | correct | B:screens[3] |
| l24-mixed-set.json | `.screens[4].prose` | About 3 minutes. Two players take 1 to 5 matches in turn from a pile of 40. Whoever takes the last match wins. You move… | correct | B:screens[4] |
| l24-mixed-set.json | `.screens[4].hints[0].text` | Which piles lose for the mover? | correct | B:screens[4] |
| l24-mixed-set.json | `.screens[4].hints[1].text` | With takes of 1 to 5, the multiples of 6. | correct | B:screens[4] |
| l24-mixed-set.json | `.screens[4].hints[2].text` | $40 = 6 \times 6 + 4$. | correct | B:screens[4] |
| l24-mixed-set.json | `.screens[4].feedback.correct` | Take 4 and leave 36. | correct | B:screens[4] |
| l24-mixed-set.json | `.screens[4].feedback.generic` | Not quite right. Leave a multiple of 6. | correct | B:screens[4] |
| l24-mixed-set.json | `.screens[4].feedback.byKey.five` | Taking 5 leaves 35. Your rival takes 5 and hands you 30. | correct | B:screens[4] |
| l24-mixed-set.json | `.screens[4].feedback.byKey.one` | Taking 1 leaves 39. Your rival takes 3 and hands you 36. | correct | B:screens[4] |
| l24-mixed-set.json | `.screens[4].explain.text` | With takes of 1 to 5, multiples of 6 lose for the mover. Take 4 to leave 36. Then answer each take of $x$ with $6 - x$. | correct | B:screens[4] |
| l24-mixed-set.json | `.screens[5].prose` | About a minute. Draw uniform numbers on $[0, 2]$ and add them up until the total exceeds 2. | correct | B:screens[5] |
| l24-mixed-set.json | `.screens[5].widget.options[0].text` | $e \approx 2.718$ | correct | B:screens[5] |
| l24-mixed-set.json | `.screens[5].widget.options[1].why` | That is the quick answer: each draw averages 1. But after two draws the total is often still below 2. | correct | B:screens[5] |
| l24-mixed-set.json | `.screens[5].widget.options[2].why` | Three is too many. Sometimes two draws suffice, and the mean sits between. | correct | B:screens[5] |
| l24-mixed-set.json | `.screens[5].widget.options[3].why` | Scaling the draws and the target by 2 changes nothing. The answer is the same as on $[0, 1]$. | correct | B:screens[5] |
| l24-mixed-set.json | `.screens[5].hints[0].text` | Divide everything by 2. | correct | B:screens[5] |
| l24-mixed-set.json | `.screens[5].hints[1].text` | Now it is uniforms on $[0, 1]$ exceeding 1. | correct | B:screens[5] |
| l24-mixed-set.json | `.screens[5].hints[2].text` | That expected count is $e$. | correct | B:screens[5] |
| l24-mixed-set.json | `.screens[5].feedback.correct` | $e$: scaling changes nothing. | correct | B:screens[5] |
| l24-mixed-set.json | `.screens[5].feedback.generic` | Not quite right. Rescale to uniforms on $[0, 1]$. | correct | B:screens[5] |
| l24-mixed-set.json | `.screens[5].feedback.byKey.b` | You took the quick answer: two draws of mean 1. Two draws stay below 2 half the time, so more are needed. | correct | B:screens[5] |
| l24-mixed-set.json | `.screens[5].explain.text` | Halve every draw and the target: the puzzle becomes uniforms on $[0, 1]$ exceeding 1. Its answer is $\sum 1/n! = e$. A … | correct | B:screens[5] |
| l24-mixed-set.json | `.screens[6].prose` | Two traders arrive at random times within the same hour. Each waits 15 minutes for the other. | correct | B:screens[6] |
| l24-mixed-set.json | `.screens[6].widget.options[0].text` | Shade an area in the unit square | correct | B:screens[6] |
| l24-mixed-set.json | `.screens[6].widget.options[1].why` | Nothing is being updated. The two times form a point in a square. | correct | B:screens[6] |
| l24-mixed-set.json | `.screens[6].widget.options[2].why` | There is no chain of states here. It is one random point. | correct | B:screens[6] |
| l24-mixed-set.json | `.screens[6].widget.options[3].why` | That gives expected counts. This asks for one chance. | correct | B:screens[6] |
| l24-mixed-set.json | `.screens[6].hints[0].text` | Draw both arrival times as one point. | correct | B:screens[6] |
| l24-mixed-set.json | `.screens[6].hints[1].text` | They meet when the times differ by at most a quarter of the hour. | correct | B:screens[6] |
| l24-mixed-set.json | `.screens[6].hints[2].text` | That is a band about the diagonal: $1 - (\tfrac34)^2$. | correct | B:screens[6] |
| l24-mixed-set.json | `.screens[6].feedback.correct` | An area: $1 - (\tfrac34)^2 = \tfrac{7}{16}$. | correct | B:screens[6] |
| l24-mixed-set.json | `.screens[6].feedback.generic` | Not quite right. Picture both times as one point. | correct | B:screens[6] |
| l24-mixed-set.json | `.screens[6].explain.text` | The two times are a uniform point in the unit square. They meet in the band $\|x - y\| \le \tfrac14$, of area $1 - (\tf… | correct | B:screens[6] |
| l24-mixed-set.json | `.screens[7].prose` | About a minute. A bag holds red and blue balls. You draw two at random and both are red. | correct | B:screens[7] |
| l24-mixed-set.json | `.screens[7].widget.options[0].text` | Ask how many balls there are and how the bag was filled | correct | B:screens[7] |
| l24-mixed-set.json | `.screens[7].widget.options[1].why` | You assumed equal numbers. The puzzle never said so. | correct | B:screens[7] |
| l24-mixed-set.json | `.screens[7].widget.options[2].why` | That rule assumes every mix was equally likely to begin with. Nobody said so; ask. | correct | B:screens[7] |
| l24-mixed-set.json | `.screens[7].widget.options[3].why` | Two reds do not rule out blue balls. | correct | B:screens[7] |
| l24-mixed-set.json | `.screens[7].hints[0].text` | What would you need to compute the chance? | correct | B:screens[7] |
| l24-mixed-set.json | `.screens[7].hints[1].text` | The number of each colour, or how the mix was chosen. | correct | B:screens[7] |
| l24-mixed-set.json | `.screens[7].hints[2].text` | Without it, the honest answer is a question. | correct | B:screens[7] |
| l24-mixed-set.json | `.screens[7].feedback.correct` | Ask for the missing facts. | correct | B:screens[7] |
| l24-mixed-set.json | `.screens[7].feedback.generic` | Not quite right. Can the chance be computed from what you were told? | correct | B:screens[7] |
| l24-mixed-set.json | `.screens[7].explain.text` | With 3 red and 1 blue the next is red with $\tfrac12$; with 9 red and 1 blue, $\tfrac78$. Without a count or a prior, a… | correct | B:screens[7] |
| l24-mixed-set.json | `.screens[8].prose` | Six more short ones, about a minute each, on your own clock. Say the family first. Four decimal places. | correct | B:screens[8] |
| l24-mixed-set.json | `.screens[8].hints[0].text` | Semicircle, meeting, Buffon, distance, who wins, Kelly. | correct | B:screens[8] |
| l24-mixed-set.json | `.screens[8].hints[1].text` | $\tfrac{n}{2^{n-1}}$, $1 - (\tfrac23)^2$, $\tfrac{2L}{\pi d}$, $\tfrac{L}{3}$, $\tfrac{1}{2 - p}$, $p - q$. | correct | B:screens[8] |
| l24-mixed-set.json | `.screens[8].hints[2].text` | $\tfrac{5}{16}$, $\tfrac59$, $\tfrac1\pi$, $1$, $\tfrac47$, $0.3$. | correct | B:screens[8] |
| l24-mixed-set.json | `.screens[8].feedback.correct` | $0.3125$, $0.5556$, $0.3183$, $1$, $0.5714$ and $0.3$. | correct | B:screens[8] |
| l24-mixed-set.json | `.screens[8].feedback.generic` | Not quite right. Check the first answer that is marked. | correct | B:screens[8] |
| l24-mixed-set.json | `.screens[8].feedback.byKey.r1c1` | The meeting band has area $1 - (\tfrac23)^2$, not $\tfrac13$. | correct | B:screens[8] |
| l24-mixed-set.json | `.screens[8].feedback.byKey.r4c1` | Alternating is not even: the first player wins with $\tfrac{1}{2 - p}$. | correct | B:screens[8] |
| l24-mixed-set.json | `.screens[8].feedback.byKey.r0c1` | $\tfrac{n}{2^{n-1}}$ with $n = 5$. | correct | B:screens[8] |
| l24-mixed-set.json | `.screens[8].feedback.byKey.r2c1` | $\tfrac{2L}{\pi d} = \tfrac{2}{2\pi}$. | correct | B:screens[8] |
| l24-mixed-set.json | `.screens[8].feedback.byKey.r3c1` | On $[0, L]$ the mean distance is $\tfrac{L}{3}$. | correct | B:screens[8] |
| l24-mixed-set.json | `.screens[8].feedback.byKey.r5c1` | At evens $f^* = p - q$. | correct | B:screens[8] |
| l24-mixed-set.json | `.screens[8].explain.text` | Each is a one-line formula once the family is named. The semicircle gives $\tfrac{5}{16}$ and the meeting $\tfrac59$. B… | correct | B:screens[8] |
| l24-mixed-set.json | `.screens[9].prose` | About 4 minutes. Roll an 8-sided die up to three times. After each roll you may stop and take its value in pounds. | correct | B:screens[9] |
| l24-mixed-set.json | `.screens[9].widget.accept` | 97/16 = 6.0625 | correct | B:screens[9] |
| l24-mixed-set.json | `.screens[9].hints[0].text` | Work back from the last roll, worth 4.5. | correct | B:screens[9] |
| l24-mixed-set.json | `.screens[9].hints[1].text` | With two rolls left, stop on 5 or more: $\tfrac12 \times 6.5 + \tfrac12 \times 4.5 = 5.5$. | correct | B:screens[9] |
| l24-mixed-set.json | `.screens[9].hints[2].text` | With three left, stop on 6 or more: $\tfrac38 \times 7 + \tfrac58 \times 5.5$. | correct | B:screens[9] |
| l24-mixed-set.json | `.screens[9].feedback.correct` | $\tfrac{97}{16} = £6.0625$. | correct | B:screens[9] |
| l24-mixed-set.json | `.screens[9].feedback.generic` | Not quite right. Value the last roll first, then step back. | correct | B:screens[9] |
| l24-mixed-set.json | `.screens[9].feedback.byKey.two` | That is the two-roll value. A third roll raises the bar to 6. | correct | B:screens[9] |
| l24-mixed-set.json | `.screens[9].feedback.byKey.one` | That is one roll. | correct | B:screens[9] |
| l24-mixed-set.json | `.screens[9].feedback.byKey.eight` | You cannot count on an 8. Stop when a roll beats the value of rolling on. | correct | B:screens[9] |
| l24-mixed-set.json | `.screens[9].explain.text` | The last roll is worth 4.5 and two rolls 5.5. With three, stop on 6, 7 or 8: $\tfrac38 \times 7 + \tfrac58 \times 5.5 =… | correct | B:screens[9] |
| l24-mixed-set.json | `.screens[10].prose` | About 3 minutes. Penney's game: the interviewer picks HTT, then you pick a pattern of three flips. First to appear wins. | correct | B:screens[10] |
| l24-mixed-set.json | `.screens[10].widget.options[0].text` | HHT | correct | B:screens[10] |
| l24-mixed-set.json | `.screens[10].widget.options[1].why` | THT against HTT is an even race. You can do better. | correct | B:screens[10] |
| l24-mixed-set.json | `.screens[10].widget.options[2].why` | TTH loses three times in four: HTT needs only the H that must come first. | correct | B:screens[10] |
| l24-mixed-set.json | `.screens[10].widget.options[3].why` | HHH wins only $\tfrac25$. Three heads in a row is slow. | correct | B:screens[10] |
| l24-mixed-set.json | `.screens[10].hints[0].text` | Take the opposite of their middle letter. | correct | B:screens[10] |
| l24-mixed-set.json | `.screens[10].hints[1].text` | Their middle letter is T, so start with H. | correct | B:screens[10] |
| l24-mixed-set.json | `.screens[10].hints[2].text` | Then their first two letters: H, HT, giving HHT. | correct | B:screens[10] |
| l24-mixed-set.json | `.screens[10].feedback.correct` | HHT, winning $\tfrac23$. | correct | B:screens[10] |
| l24-mixed-set.json | `.screens[10].feedback.generic` | Not quite right. Build your pattern from the front of theirs. | correct | B:screens[10] |
| l24-mixed-set.json | `.screens[10].feedback.byKey.c` | TTH is beaten: any H before TT lets HTT finish first. | correct | B:screens[10] |
| l24-mixed-set.json | `.screens[10].explain.text` | The opposite of their middle letter, then their first two letters, gives HHT. It beats HTT with chance $\tfrac23$. The … | correct | B:screens[10] |
| l24-mixed-set.json | `.screens[11].prose` | Practise this aloud. Interviewer: "You bought £40 of a team at 4 to 1. The other side now trades at evens. What do you … | correct | B:screens[11] |
| l24-mixed-set.json | `.screens[11].hints[0].text` | You win £160 or lose £40 unhedged. | correct | B:screens[11] |
| l24-mixed-set.json | `.screens[11].hints[1].text` | Solve $160 - h = h - 40$. | correct | B:screens[11] |
| l24-mixed-set.json | `.screens[11].hints[2].text` | $h = 100$, so the profit is £60. | correct | B:screens[11] |
| l24-mixed-set.json | `.screens[11].feedback.correct` | £60, with a £100 hedge. | correct | B:screens[11] |
| l24-mixed-set.json | `.screens[11].feedback.generic` | Not quite right. Equate the two outcomes after a hedge of $h$. | correct | B:screens[11] |
| l24-mixed-set.json | `.screens[11].feedback.byKey.hedge` | That is the hedge. The locked profit is $160 - 100$. | correct | B:screens[11] |
| l24-mixed-set.json | `.screens[11].feedback.byKey.win` | That is the unhedged win. The hedge costs £100 of it. | correct | B:screens[11] |
| l24-mixed-set.json | `.screens[11].explain.text` | Hedging £100 gives $160 - 100 = 60$ or $-40 + 100 = 60$. Then say whether you would hedge at all, given your view of th… | correct | B:screens[11] |
| l24-mixed-set.json | `.summary.ideas[0]` | Name the family first; the method follows from it. | correct | B:summary |
| l24-mixed-set.json | `.summary.ideas[1]` | Say the argument aloud as you go: interviewers mark the reasoning, not only the number. | correct | B:summary |
| l24-mixed-set.json | `.summary.ideas[2]` | When a puzzle lacks a fact, ask for it rather than assume one. | correct | B:summary |
| l24-mixed-set.json | `.summary.formula.note` | Coupons, alternating turns, Kelly, fair ruin, uniforms exceeding one. | correct | B:summary |
| l24-mixed-set.json | `.summary.trap` | Giving the quick answer: $\tfrac12$ for alternating turns, 2 for uniforms exceeding a target, $n^2$ for coupons. | correct | B:summary |
| l24-mixed-set.json | `.quiz[0].prose` | Roll a die six times. | correct | B:quiz[0] |
| l24-mixed-set.json | `.quiz[0].widget.options[0].text` | One indicator per face, and linearity | correct | B:quiz[0] |
| l24-mixed-set.json | `.quiz[0].widget.options[1].why` | That works, but it takes six equations. Indicators take one line. | correct | B:quiz[0] |
| l24-mixed-set.json | `.quiz[0].widget.options[2].why` | Symmetry tells you each face is alike, which indicators then use. Alone it gives no number. | correct | B:quiz[0] |
| l24-mixed-set.json | `.quiz[0].feedback.correct` | Indicators: $6(1 - (\tfrac56)^6) \approx 3.99$. | correct | B:quiz[0] |
| l24-mixed-set.json | `.quiz[0].feedback.generic` | Not quite right. Ask what each face contributes. | correct | B:quiz[0] |
| l24-mixed-set.json | `.quiz[0].explain.text` | Face $k$ appears with chance $1 - (\tfrac56)^6$. Adding six of these gives about 3.9906. Linearity needs no independenc… | correct | B:quiz[0] |
| l24-mixed-set.json | `.quiz[1].prose` | A bet pays 4 to 1 and wins with chance 0.3. | correct | B:quiz[1] |
| l24-mixed-set.json | `.quiz[1].widget.accept` | 0.3 − 0.7/4 = 0.125 | correct | B:quiz[1] |
| l24-mixed-set.json | `.quiz[1].feedback.correct` | $0.125$. | correct | B:quiz[1] |
| l24-mixed-set.json | `.quiz[1].feedback.generic` | Not quite right. Use $p - q/b$. | correct | B:quiz[1] |
| l24-mixed-set.json | `.quiz[1].feedback.byKey.evens` | You used the evens rule. Divide $q$ by the odds. | correct | B:quiz[1] |
| l24-mixed-set.json | `.quiz[1].feedback.byKey.ev` | That is the edge per £1. Divide it by the odds. | correct | B:quiz[1] |
| l24-mixed-set.json | `.quiz[1].explain.text` | $0.3 - 0.7/4 = 0.125$. The edge is $4 \times 0.3 - 0.7 = 0.5$ per £1, and $0.5/4 = 0.125$. | correct | B:quiz[1] |
| l24-mixed-set.json | `.quiz[2].prose` | An interviewer asks: "A family has two children and one is a boy. What is the chance both are boys?" | correct | B:quiz[2] |
| l24-mixed-set.json | `.quiz[2].widget.options[0].text` | Ask how we learned that one is a boy | correct | B:quiz[2] |
| l24-mixed-set.json | `.quiz[2].widget.options[1].why` | That holds if a particular child was seen to be a boy. The wording does not say. | correct | B:quiz[2] |
| l24-mixed-set.json | `.quiz[2].widget.options[2].why` | That holds if a parent said 'at least one is a boy'. The wording does not say. | correct | B:quiz[2] |
| l24-mixed-set.json | `.quiz[2].feedback.correct` | Ask how the fact was learned. | correct | B:quiz[2] |
| l24-mixed-set.json | `.quiz[2].feedback.generic` | Not quite right. Which answer depends on facts not given? | correct | B:quiz[2] |
| l24-mixed-set.json | `.quiz[2].explain.text` | The answer is $\tfrac13$ or $\tfrac12$ depending on how the boy was revealed. Saying so, then answering both cases, is … | correct | B:quiz[2] |

## review-4.json

### Bases

| key | basis |
|---|---|
| items[0] | Berlekamp, Conway and Guy, Winning Ways vol. 1 ch. 2 (subtraction games, P-positions); sim: puzzles-L4-concepts-r2.py:from 26 take 2 |
| items[1] | sim: puzzles-L4-concepts-r2.py:double six first: 36/71; 1/(2-p) -> 1/2 as p -> 0 |
| items[2] | Feller vol. 1 XIII.7 (recurrent patterns, waiting times) and GKP Concrete Mathematics 8.4 (Penney, Conway leading numbers); sim: puzzles-L4-concepts-r2.py:P(HTH before HHH) = 3/5; Conway numbers 5, 1, 7, 1 |
| items[3] | Kelly (1956); Thorp, The Kelly criterion in blackjack, sports betting and the stock market (2006) s. 2 to 4; sim: puzzles-L4-concepts-r2.py:Kelly 0.04, 0.0625 |
| items[4] | Kelly (1956); Thorp, The Kelly criterion in blackjack, sports betting and the stock market (2006) s. 2 to 4; sim: puzzles-L4-concepts-r2.py:Kelly 0.04, 0.0625 |
| items[5] | sim: puzzles-L4-concepts-r2.py:hedge 100 locks 80 |
| items[6] | sim: puzzles-L4-concepts-r2.py:bet 25 at 3-1; game 5 decides only if both later games are lost: 1/4 |
| items[7] | sim: puzzles-L4-concepts-r2.py:European red 4 doublings -0.1126 |
| items[8] | linearity; sim: puzzles-L4-concepts-r2.py:expected faces seen 3.9906 |

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| review-4.json | `.items[0].prose` | Takes of 1 to 3 from a pile of 26 matches. Whoever takes the last match wins, and you move first. | correct | B:items[0] |
| review-4.json | `.items[0].feedback.correct` | Take 2 and leave 24. | correct | B:items[0] |
| review-4.json | `.items[0].feedback.generic` | Not quite right. Leave a multiple of 4. | correct | B:items[0] |
| review-4.json | `.items[0].feedback.byKey.one` | Taking 1 leaves 25. Your rival takes 1 and hands you 24. | correct | B:items[0] |
| review-4.json | `.items[0].feedback.byKey.three` | Taking 3 leaves 23. Your rival takes 3 and hands you 20. | correct | B:items[0] |
| review-4.json | `.items[0].explain.text` | $26 = 6 \times 4 + 2$, so take 2 to leave 24. Then answer each take of $x$ with $4 - x$. | correct | B:items[0] |
| review-4.json | `.items[1].prose` | Two players take turns to roll two dice. The first to roll a double six wins. | correct | B:items[1] |
| review-4.json | `.items[1].widget.accept` | 36/71, about 0.5070 | correct | B:items[1] |
| review-4.json | `.items[1].feedback.correct` | $\tfrac{36}{71} \approx 0.5070$. | correct | B:items[1] |
| review-4.json | `.items[1].feedback.generic` | Not quite right. Use $\tfrac{1}{2 - p}$ with $p = \tfrac{1}{36}$. | correct | B:items[1] |
| review-4.json | `.items[1].feedback.byKey.half` | Close, but the first seat still has the first chance each round. | correct | B:items[1] |
| review-4.json | `.items[1].feedback.byKey.once` | That is the chance on the first throw only. | correct | B:items[1] |
| review-4.json | `.items[1].explain.text` | With $p = \tfrac{1}{36}$, the first player wins with $\tfrac{1}{2 - 1/36} = \tfrac{36}{71}$. A rare success makes the f… | correct | B:items[1] |
| review-4.json | `.items[2].prose` | Flip a fair coin until HTH or HHH appears. | correct | B:items[2] |
| review-4.json | `.items[2].widget.accept` | 3/5 | correct | B:items[2] |
| review-4.json | `.items[2].feedback.correct` | $\tfrac35$. | correct | B:items[2] |
| review-4.json | `.items[2].feedback.generic` | Not quite right. Use Conway's leading numbers or the node equations. | correct | B:items[2] |
| review-4.json | `.items[2].feedback.byKey.half` | Same length is not the same chance. | correct | B:items[2] |
| review-4.json | `.items[2].feedback.byKey.hhh` | That is HHH's chance. | correct | B:items[2] |
| review-4.json | `.items[2].explain.text` | Take A = HTH and B = HHH. Conway's numbers are $A \cdot A = 5$, $A \cdot B = 1$, $B \cdot B = 7$ and $B \cdot A = 1$. S… | correct | B:items[2] |
| review-4.json | `.items[3].prose` | An even-money bet wins with chance 0.52. | correct | B:items[3] |
| review-4.json | `.items[3].widget.accept` | 0.52 − 0.48 = 0.04 | correct | B:items[3] |
| review-4.json | `.items[3].feedback.correct` | $0.04$. | correct | B:items[3] |
| review-4.json | `.items[3].feedback.generic` | Not quite right. At evens $f^* = p - q$. | correct | B:items[3] |
| review-4.json | `.items[3].feedback.byKey.p` | That is the win chance. Subtract the loss chance. | correct | B:items[3] |
| review-4.json | `.items[3].feedback.byKey.half` | That is half Kelly. | correct | B:items[3] |
| review-4.json | `.items[3].explain.text` | $f^* = 0.52 - 0.48 = 0.04$. A thin edge earns a small stake. | correct | B:items[3] |
| review-4.json | `.items[4].prose` | A bet pays 4 to 1 and wins with chance 0.25. | correct | B:items[4] |
| review-4.json | `.items[4].widget.accept` | 0.25 − 0.75/4 = 0.0625 | correct | B:items[4] |
| review-4.json | `.items[4].feedback.correct` | $0.0625$. | correct | B:items[4] |
| review-4.json | `.items[4].feedback.generic` | Not quite right. Use $p - q/b$. | correct | B:items[4] |
| review-4.json | `.items[4].feedback.byKey.evens` | You used $p - q$. At 4 to 1, divide $q$ by 4. | correct | B:items[4] |
| review-4.json | `.items[4].feedback.byKey.edge` | That is the edge per £1. Divide it by the odds. | correct | B:items[4] |
| review-4.json | `.items[4].explain.text` | $0.25 - 0.75/4 = 0.0625$. The edge is $4 \times 0.25 - 0.75 = 0.25$ per £1, divided by the odds 4. | correct | B:items[4] |
| review-4.json | `.items[5].prose` | You backed a team for £20 at 9 to 1. The other side is now offered at evens. | correct | B:items[5] |
| review-4.json | `.items[5].feedback.correct` | £80, with a £100 hedge. | correct | B:items[5] |
| review-4.json | `.items[5].feedback.generic` | Not quite right. Solve $180 - h = h - 20$. | correct | B:items[5] |
| review-4.json | `.items[5].feedback.byKey.hedge` | That is the hedge. The locked profit is $180 - 100$. | correct | B:items[5] |
| review-4.json | `.items[5].feedback.byKey.win` | That is the unhedged win. | correct | B:items[5] |
| review-4.json | `.items[5].explain.text` | $180 - h = h - 20$ gives $h = 100$. Both outcomes then pay £80. | correct | B:items[5] |
| review-4.json | `.items[6].prose` | You want £100 on a best-of-seven series, betting game by game at evens. Your team leads 3–1. | correct | B:items[6] |
| review-4.json | `.items[6].feedback.correct` | £25. | correct | B:items[6] |
| review-4.json | `.items[6].feedback.generic` | Not quite right. Find the chance that game 5 decides the series. | correct | B:items[6] |
| review-4.json | `.items[6].feedback.byKey.half` | That is the bet at 2–2. Leading 3–1, most later results win anyway. | correct | B:items[6] |
| review-4.json | `.items[6].feedback.byKey.all` | Game 5 decides the series only if games 6 and 7 would both be lost. | correct | B:items[6] |
| review-4.json | `.items[6].explain.text` | Imagine games 6 and 7 played. Game 5 decides the series only if your team would lose both, chance $\tfrac14$. So bet $1… | correct | B:items[6] |
| review-4.json | `.items[7].prose` | A doubler holds £15 and bets on red at a European wheel, where red wins with chance $\tfrac{18}{37}$. He doubles from £… | correct | B:items[7] |
| review-4.json | `.items[7].widget.accept` | 1 − 16(19/37)⁴, about −0.1126 | correct | B:items[7] |
| review-4.json | `.items[7].feedback.correct` | About $-£0.11$ a cycle. | correct | B:items[7] |
| review-4.json | `.items[7].feedback.generic` | Not quite right. £15 funds four bets; use $1 - 16q^4$. | correct | B:items[7] |
| review-4.json | `.items[7].feedback.byKey.fair` | That is the fair-coin answer. Red loses slightly more often than it wins. | correct | B:items[7] |
| review-4.json | `.items[7].feedback.byKey.pos` | Check the sign. The rare loss outweighs the wins. | correct | B:items[7] |
| review-4.json | `.items[7].explain.text` | £15 funds stakes of £1, £2, £4 and £8. With $q = \tfrac{19}{37}$, $q^4 \approx 0.06954$, so the gain is $1 - 16 \times … | correct | B:items[7] |
| review-4.json | `.items[8].prose` | An interviewer asks for the expected number of different faces in six rolls of a die. | correct | B:items[8] |
| review-4.json | `.items[8].widget.options[0].text` | One indicator per face, then linearity | correct | B:items[8] |
| review-4.json | `.items[8].widget.options[1].why` | There is no decision to make, so there is nothing to work back from. | correct | B:items[8] |
| review-4.json | `.items[8].widget.options[2].why` | Nothing is stopped. Optional stopping is for fair games and stopping rules. | correct | B:items[8] |
| review-4.json | `.items[8].feedback.correct` | Indicators: $6(1 - (\tfrac56)^6) \approx 3.99$. | correct | B:items[8] |
| review-4.json | `.items[8].feedback.generic` | Not quite right. Ask what each face contributes. | correct | B:items[8] |
| review-4.json | `.items[8].explain.text` | Each face appears with chance $1 - (\tfrac56)^6$. Six indicators add to about 3.9906. Naming the family first saves the… | correct | B:items[8] |

## homework-4.json

### Bases

| key | basis |
|---|---|
| items[0] | Feller vol. 1 XIII.7 (recurrent patterns, waiting times) and GKP Concrete Mathematics 8.4 (Penney, Conway leading numbers); sim: puzzles-L4-concepts-r2.py:all eight pairs agree between automaton and Conway; solution passes all 9 hidden tests |
| items[1] | CLT for a sum of iid steps (median near mean); sim: puzzles-L4-concepts-r2.py:seeds 1..4 give 20.14, 15.04, -9.79, 30.14; seed 1 median path won exactly 600; tolerances are three SE of the median; solution passes all 6 tests |
| items[2] | Kelly (1956); Thorp, The Kelly criterion in blackjack, sports betting and the stock market (2006) s. 2 to 4; SLLN; sympy: sim: puzzles-L4-concepts-r2.py:f* = p - q/b; g'' < 0; g = 0 near twice Kelly |
| items[3] | Kelly (1956); Thorp, The Kelly criterion in blackjack, sports betting and the stock market (2006) s. 2 to 4; sim: puzzles-L4-concepts-r2.py:survival 0.6^10; half Kelly 75%; g(0.4) < 0; at a true p=0.55, f=0.2 is double Kelly with growth about 0; overbetting by d costs more growth than underbetting by d (g''' < 0) |
| items[4] | sim: puzzles-L4-concepts-r2.py:four players: 216/671; MC three/two players |
| items[5] | sim: puzzles-L4-concepts-r2.py:best-of-9 27.34 |
| items[6] | sim: puzzles-L4-concepts-r2.py:bankroll 511 (9 bets); European red 9 doublings -0.2713 |
| items[7] | log utility; sympy: sim: puzzles-L4-concepts-r2.py:log-optimal hedge 180 at p=0.55; grid search over whole pounds gives 180 |
| items[8] | Hoehn and Niven (1985) and Gardner, Penney-ante (Sci. Am. 1974); sim: puzzles-L4-concepts-r2.py:P(TTH before THH) = 2/3; HHT vs THH 1/4; HTH vs THH 1/2; TTT vs THH 2/5 |

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| homework-4.json | `.items[0].prose` | Write `first_to_appear(a, b)` for any two H/T patterns, neither inside the other. It returns the exact chance, as a `Fr… | correct | B:items[0] |
| homework-4.json | `.items[0].widget.how` | Check runs 9 hidden tests. Tests 1 to 8 need the exact `Fraction` for pairs of lengths 2 to 4, some of unequal length. … | correct | B:items[0] |
| homework-4.json | `.items[0].feedback.correct` | Exact on all eight pairs, unequal lengths included. | correct | B:items[0] |
| homework-4.json | `.items[0].feedback.generic` | Not quite right. Look at the first failing test. | correct | B:items[0] |
| homework-4.json | `.items[0].feedback.byKey.test-3` | Four-letter patterns need every prefix as a node, '' included. | correct | B:items[0] |
| homework-4.json | `.items[0].feedback.byKey.test-4` | Patterns of unequal length share the same automaton: take the prefixes of both. | correct | B:items[0] |
| homework-4.json | `.items[0].explain.text` | The nodes are the prefixes of either pattern; each flip moves to the longest suffix that is still a node. One equation … | correct | B:items[0] |
| homework-4.json | `.items[1].prose` | Write `kelly_sim(p, b, f, bets, paths, seed)`. Each path starts at log-wealth 0 and makes `bets` bets at stake `f`. Eac… | correct | B:items[1] |
| homework-4.json | `.items[1].widget.how` | Check runs 6 hidden tests. Tests 1, 2 and 4 accept a median within three standard errors of $n\,g(f)$. Test 3 needs a n… | correct | B:items[1] |
| homework-4.json | `.items[1].feedback.correct` | The medians sit on $n\,g(f)$, and double Kelly shrinks. | correct | B:items[1] |
| homework-4.json | `.items[1].feedback.generic` | Not quite right. Look at the first failing test. | correct | B:items[1] |
| homework-4.json | `.items[1].feedback.byKey.test-1` | Add $\ln(1 + bf)$ on a win and $\ln(1 - f)$ on a loss, then take the median of the finals. | correct | B:items[1] |
| homework-4.json | `.items[1].feedback.byKey.test-3` | At $f = 0.4$ the growth is negative, so the median should fall below 0. | correct | B:items[1] |
| homework-4.json | `.items[1].explain.text` | Log-wealth is a sum of independent steps, so its median sits near $n\,g(f)$. Seeds 1 and 2 give $n\,g(f)$ exactly, 20.1… | correct | B:items[1] |
| homework-4.json | `.items[2].prose` | A bet pays $b$ to 1 and wins with chance $p$. Derive its Kelly fraction, one justified line at a time. | correct | B:items[2] |
| homework-4.json | `.items[2].widget.lines[0].text` | One bet multiplies wealth by $1 + bf$ with chance $p$, or by $1 - f$ with chance $q$. | correct | B:items[2] |
| homework-4.json | `.items[2].widget.lines[1].text` | Log-wealth after $n$ bets is a sum of $n$ such logs. By the law of large numbers, its growth per bet tends to $g(f) = p… | correct | B:items[2] |
| homework-4.json | `.items[2].widget.lines[2].text` | Differentiate: $g'(f) = \dfrac{pb}{1 + bf} - \dfrac{q}{1 - f}$. | correct | B:items[2] |
| homework-4.json | `.items[2].widget.lines[3].text` | $g''(f) < 0$, so a zero of $g'$ is the maximum. | correct | B:items[2] |
| homework-4.json | `.items[2].widget.lines[4].text` | Set $g'(f) = 0$: $pb(1 - f) = q(1 + bf)$. | correct | B:items[2] |
| homework-4.json | `.items[2].widget.lines[5].text` | Expand: $pb - pbf = q + qbf$, so $bf(p + q) = pb - q$. | correct | B:items[2] |
| homework-4.json | `.items[2].widget.lines[6].text` | Since $p + q = 1$, $f^* = p - \dfrac{q}{b}$, or 0 when that is negative. | correct | B:items[2] |
| homework-4.json | `.items[2].widget.lines[7].text` | Expected wealth $1 + f(pb - q)$ rises with $f$, so $f^* = 1$. | correct | B:items[2] |
| homework-4.json | `.items[2].widget.lines[7].why` | That maximises the mean, which stakes everything. Kelly maximises the expected log. | correct | B:items[2] |
| homework-4.json | `.items[2].widget.lines[8].text` | Set $g(f) = 0$ and solve for $f$. | correct | B:items[2] |
| homework-4.json | `.items[2].widget.lines[8].why` | That finds where growth hits zero, near twice Kelly, not the peak. | correct | B:items[2] |
| homework-4.json | `.items[2].feedback.correct` | $f^* = p - q/b$, line by line. | correct | B:items[2] |
| homework-4.json | `.items[2].feedback.generic` | Not quite right. Start from what one bet does to wealth. | correct | B:items[2] |
| homework-4.json | `.items[2].feedback.byKey.d1` | You maximised expected wealth. That stakes everything; Kelly maximises the expected log. | correct | B:items[2] |
| homework-4.json | `.items[2].feedback.byKey.d2` | Setting $g = 0$ finds the stake where growth vanishes, not where it peaks. | correct | B:items[2] |
| homework-4.json | `.items[2].feedback.byKey.left-out` | Every line except the two flawed ones belongs. | correct | B:items[2] |
| homework-4.json | `.items[2].explain.text` | The law of large numbers turns repeated bets into the growth rate $g(f)$. It is concave, so its stationary point is the… | correct | B:items[2] |
| homework-4.json | `.items[3].model` | **Expectation.** Per £1 staked I win £1 with chance 0.6 and lose £1 with chance 0.4. The expected gain is $0.6 - 0.4 = … | correct | B:items[3] |
| homework-4.json | `.items[3].rubric[0].text` | States the expected gain, £0.20 per £1, and so takes the bet | correct | B:items[3] |
| homework-4.json | `.items[3].rubric[1].text` | Explains that repeated bets compound, so the aim is the expected log of wealth, and that staking everything risks ruin | correct | B:items[3] |
| homework-4.json | `.items[3].rubric[2].text` | Derives or states $f^* = p - q = 0.2$, with the growth rate of about 0.02 a bet | correct | B:items[3] |
| homework-4.json | `.items[3].rubric[3].text` | Recommends fractional Kelly: about three quarters of the growth for half the spread. Notes that overbetting turns growt… | correct | B:items[3] |
| homework-4.json | `.items[3].rubric[4].text` | Names estimation error in $p$: at a true 0.55 the stake of 0.2 is double Kelly, so shade it down | correct | B:items[3] |
| homework-4.json | `.items[4].prose` | Four players roll a die in turn, and the first six wins. | correct | B:items[4] |
| homework-4.json | `.items[4].widget.accept` | 216/671, about 0.3219 | correct | B:items[4] |
| homework-4.json | `.items[4].feedback.correct` | $\tfrac{216}{671} \approx 0.3219$. | correct | B:items[4] |
| homework-4.json | `.items[4].feedback.generic` | Not quite right. A round is now four rolls. | correct | B:items[4] |
| homework-4.json | `.items[4].feedback.byKey.quarter` | You split it evenly. Each seat is worth $\tfrac56$ of the one before. | correct | B:items[4] |
| homework-4.json | `.items[4].feedback.byKey.three` | That is the three-player answer. | correct | B:items[4] |
| homework-4.json | `.items[4].explain.text` | A round ends with no six with chance $(\tfrac56)^4 = \tfrac{625}{1296}$. So $x = \tfrac{1/6}{671/1296} = \tfrac{216}{67… | correct | B:items[4] |
| homework-4.json | `.items[5].prose` | You want £100 on a best-of-nine series, betting game by game at evens. | correct | B:items[5] |
| homework-4.json | `.items[5].feedback.correct` | £27.34. | correct | B:items[5] |
| homework-4.json | `.items[5].feedback.generic` | Not quite right. Find the chance that games 2 to 9 split 4–4. | correct | B:items[5] |
| homework-4.json | `.items[5].feedback.byKey.seven` | That is the best-of-seven bet. | correct | B:items[5] |
| homework-4.json | `.items[5].feedback.byKey.ninth` | You spread £100 over nine games. The bet is the chance game 1 decides it. | correct | B:items[5] |
| homework-4.json | `.items[5].explain.text` | Game 1 decides the series when games 2 to 9 split 4–4, chance $\binom84/2^8 = \tfrac{70}{256}$. So bet $100 \times \tfr… | correct | B:items[5] |
| homework-4.json | `.items[6].prose` | A doubler bets on red at a European wheel, where red wins with chance $\tfrac{18}{37}$. He starts at £1, and the table'… | correct | B:items[6] |
| homework-4.json | `.items[6].widget.accept` | 1 − 512(19/37)⁹, about −0.2713 | correct | B:items[6] |
| homework-4.json | `.items[6].feedback.correct` | About $-£0.27$ a cycle. | correct | B:items[6] |
| homework-4.json | `.items[6].feedback.generic` | Not quite right. Count the bets: £1 to £256 is nine. | correct | B:items[6] |
| homework-4.json | `.items[6].feedback.byKey.fair` | That is the fair-coin answer. | correct | B:items[6] |
| homework-4.json | `.items[6].feedback.byKey.ten` | That is ten bets. The table limit stops him at nine. | correct | B:items[6] |
| homework-4.json | `.items[6].explain.text` | Stakes £1 to £256 make nine bets, losing £511 if all fail. With $q = \tfrac{19}{37}$, the gain is $1 - 512\,q^9 \approx… | correct | B:items[6] |
| homework-4.json | `.items[7].prose` | Your bankroll would end at £1,500 if your team wins and £900 if it loses. You believe it wins with chance 0.55. You may… | correct | B:items[7] |
| homework-4.json | `.items[7].feedback.correct` | £180. | correct | B:items[7] |
| homework-4.json | `.items[7].feedback.generic` | Not quite right. Set the derivative of $0.55\ln(1500 - h) + 0.45\ln(900 + h)$ to zero. | correct | B:items[7] |
| homework-4.json | `.items[7].feedback.byKey.full` | A full hedge locks £1,200, but it gives up your edge. | correct | B:items[7] |
| homework-4.json | `.items[7].feedback.byKey.none` | With only a small edge, some hedge pays: the bankroll swings too much unhedged. | correct | B:items[7] |
| homework-4.json | `.items[7].feedback.byKey.sixty` | That is the hedge at $p = 0.6$. A thinner edge calls for more hedging. | correct | B:items[7] |
| homework-4.json | `.items[7].explain.text` | $\tfrac{0.55}{1500 - h} = \tfrac{0.45}{900 + h}$ gives $495 + 0.55h = 675 - 0.45h$, so $h = 180$. Wealth then ends at £… | correct | B:items[7] |
| homework-4.json | `.items[8].prose` | Penney's game: the interviewer picks THH, and you pick a pattern of three flips. First to appear wins. | correct | B:items[8] |
| homework-4.json | `.items[8].widget.options[0].text` | TTH | correct | B:items[8] |
| homework-4.json | `.items[8].widget.options[1].why` | HHT cannot beat THH's lead: any T before HH lets THH finish first. It wins only $\tfrac14$. | correct | B:items[8] |
| homework-4.json | `.items[8].widget.options[2].why` | HTH against THH is an even race. | correct | B:items[8] |
| homework-4.json | `.items[8].widget.options[3].why` | TTT needs three tails in a row and loses most races. | correct | B:items[8] |
| homework-4.json | `.items[8].feedback.correct` | TTH, winning $\tfrac23$. | correct | B:items[8] |
| homework-4.json | `.items[8].feedback.generic` | Not quite right. Put the opposite of their middle letter in front of their first two. | correct | B:items[8] |
| homework-4.json | `.items[8].explain.text` | Their middle letter is H, so start with T, then their first two letters TH: TTH. It beats THH with chance $\tfrac23$. A… | correct | B:items[8] |

## l25-fair-from-biased.json

### Bases

| key | basis |
|---|---|
| screens[0] | reading list, not a claim |
| screens[1] | von Neumann (1951); independence gives P(HT) = P(TH) = pq; sim: puzzles-L5-concepts-r2.py:HT = TH = 2/9; sympy pq = qp |
| screens[7] | von Neumann (1951); independence gives P(HT) = P(TH) = pq; sim: puzzles-L5-concepts-r2.py:HT = TH = 2/9; sympy pq = qp |
| quiz[0] | von Neumann (1951); independence gives P(HT) = P(TH) = pq; sim: puzzles-L5-concepts-r2.py:HT = TH = 2/9; sympy pq = qp |
| screens[2] | geometric wait 1/(2pq) rounds of two flips (Wald); sim: puzzles-L5-concepts-r2.py:flips 9/2, 25/6, 4, 100/9, 25/4; MC flips per fair bit at p=0.6; at p=1 no round succeeds |
| screens[3] | geometric wait 1/(2pq) rounds of two flips (Wald); sim: puzzles-L5-concepts-r2.py:flips 9/2, 25/6, 4, 100/9, 25/4; MC flips per fair bit at p=0.6; at p=1 no round succeeds |
| screens[6] | geometric wait 1/(2pq) rounds of two flips (Wald); sim: puzzles-L5-concepts-r2.py:flips 9/2, 25/6, 4, 100/9, 25/4; MC flips per fair bit at p=0.6; at p=1 no round succeeds |
| summary | geometric wait 1/(2pq) rounds of two flips (Wald); sim: puzzles-L5-concepts-r2.py:flips 9/2, 25/6, 4, 100/9, 25/4; MC flips per fair bit at p=0.6; at p=1 no round succeeds |
| screens[11] | geometric wait 1/(2pq) rounds of two flips (Wald); sim: puzzles-L5-concepts-r2.py:flips 9/2, 25/6, 4, 100/9, 25/4; MC flips per fair bit at p=0.6; at p=1 no round succeeds |
| screens[4] | rejection sampling: 3 x 8/6 = 4 flips; sim: puzzles-L5-concepts-r2.py:die from a coin 4 flips, three people 8/3; 2pq = 0.42 at p=0.7; 100/9 at p=0.9 |
| screens[9] | rejection sampling: 3 x 8/6 = 4 flips; sim: puzzles-L5-concepts-r2.py:die from a coin 4 flips, three people 8/3; 2pq = 0.42 at p=0.7; 100/9 at p=0.9 |
| screens[5] | sim: puzzles-L5-concepts-r2.py:HH has chance 4/9, not 1/2 |
| screens[8] | sim: puzzles-L5-concepts-r2.py:solution passes all 10 hidden tests; kept bits are heads with chance 1/2 at p=0.8 (MC); a pair is kept with 2pq = 0.32; tolerances about three SE |
| screens[10] | sim: puzzles-L5-concepts-r2.py:HTT/THT/TTH each pq^2 = 0.096, flips 125/12, 2.5 times the two-way wait |
| quiz[1] | sim: puzzles-L5-concepts-r2.py:at p=1 no round succeeds |
| quiz[2] | two independent fair bits name one of four uniformly; sim: puzzles-L5-concepts-r2.py:two bits 25/3 |

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l25-fair-from-biased.json | `.screens[0].prose` | Level 5 holds the puzzles interviewers keep asking. Work the same books, easiest first: - Mosteller, *Fifty Challenging… | correct | B:screens[0] |
| l25-fair-from-biased.json | `.screens[1].prose` | A bent coin lands heads with chance $\tfrac23$. You need a fair 50-50 decision. Flip it twice and look at the four outc… | correct | B:screens[1] |
| l25-fair-from-biased.json | `.screens[1].hints[0].text` | Multiply along each path. | correct | B:screens[1] |
| l25-fair-from-biased.json | `.screens[1].hints[1].text` | HT is $\tfrac23 \times \tfrac13$. Which other path uses the same two numbers? | correct | B:screens[1] |
| l25-fair-from-biased.json | `.screens[1].hints[2].text` | TH is $\tfrac13 \times \tfrac23$: the same product, $\tfrac29$. | correct | B:screens[1] |
| l25-fair-from-biased.json | `.screens[1].feedback.correct` | HT and TH: each has chance $\tfrac29$. | correct | B:screens[1] |
| l25-fair-from-biased.json | `.screens[1].feedback.generic` | Not quite right. Work out the chance of each path by multiplying. | correct | B:screens[1] |
| l25-fair-from-biased.json | `.screens[1].feedback.byKey.repeats` | You picked HH and TT. HH has $\tfrac49$ and TT has $\tfrac19$, so they differ. | correct | B:screens[1] |
| l25-fair-from-biased.json | `.screens[1].feedback.byKey.h-h` | HH has chance $\tfrac49$, more than any other path. | correct | B:screens[1] |
| l25-fair-from-biased.json | `.screens[1].feedback.byKey.t-t` | TT has chance $\tfrac19$, less than any other path. | correct | B:screens[1] |
| l25-fair-from-biased.json | `.screens[1].explain.text` | HT has chance $\tfrac23 \times \tfrac13 = \tfrac29$ and TH has $\tfrac13 \times \tfrac23 = \tfrac29$. The same two fact… | correct | B:screens[1] |
| l25-fair-from-biased.json | `.screens[2].prose` | The pairing you just found is **von Neumann's trick**. Keep HT as heads and TH as tails, and start again on HH or TT. A… | correct | B:screens[2] |
| l25-fair-from-biased.json | `.screens[2].widget.accept` | 9/2, so 4.5 | correct | B:screens[2] |
| l25-fair-from-biased.json | `.screens[2].hints[0].text` | Count rounds first, then flips. | correct | B:screens[2] |
| l25-fair-from-biased.json | `.screens[2].hints[1].text` | A round succeeds with chance $\tfrac49$, so the wait is $\tfrac94$ rounds. | correct | B:screens[2] |
| l25-fair-from-biased.json | `.screens[2].hints[2].text` | Each round is two flips: $2 \times \tfrac94$. | correct | B:screens[2] |
| l25-fair-from-biased.json | `.screens[2].feedback.correct` | $\tfrac92 = 4.5$ flips. | correct | B:screens[2] |
| l25-fair-from-biased.json | `.screens[2].feedback.generic` | Not quite right. Find the expected number of rounds, then double it. | correct | B:screens[2] |
| l25-fair-from-biased.json | `.screens[2].feedback.byKey.two` | Two flips is one round. Rounds of HH or TT are thrown away, so you need more. | correct | B:screens[2] |
| l25-fair-from-biased.json | `.screens[2].feedback.byKey.rounds` | That is the number of rounds, $\tfrac94$. Each round costs two flips. | correct | B:screens[2] |
| l25-fair-from-biased.json | `.screens[2].feedback.byKey.one-path` | You used $\tfrac29$, one kept outcome. A round succeeds on HT or TH, $\tfrac49$. | correct | B:screens[2] |
| l25-fair-from-biased.json | `.screens[2].explain.text` | A round of two flips succeeds with chance $\tfrac49$, so we wait $\tfrac94$ rounds on average. That is $2 \times \tfrac… | correct | B:screens[2] |
| l25-fair-from-biased.json | `.screens[3].prose` | Drag the point along the curve. It shows the expected flips of the trick for each chance of heads $p$. | correct | B:screens[3] |
| l25-fair-from-biased.json | `.screens[3].widget.accept` | 25/6, about 4.1667 | correct | B:screens[3] |
| l25-fair-from-biased.json | `.screens[3].hints[0].text` | A round succeeds with chance $2pq$. | correct | B:screens[3] |
| l25-fair-from-biased.json | `.screens[3].hints[1].text` | At $p = 0.6$, $2pq = 2 \times 0.6 \times 0.4 = 0.48$. | correct | B:screens[3] |
| l25-fair-from-biased.json | `.screens[3].hints[2].text` | Rounds: $\tfrac{1}{0.48}$. Flips: $\tfrac{2}{0.48} = \tfrac{1}{pq}$. | correct | B:screens[3] |
| l25-fair-from-biased.json | `.screens[3].feedback.correct` | $\tfrac{1}{0.24} = \tfrac{25}{6} \approx 4.1667$ flips. | correct | B:screens[3] |
| l25-fair-from-biased.json | `.screens[3].feedback.generic` | Not quite right. Use $\tfrac{2}{2pq} = \tfrac{1}{pq}$ with $p = 0.6$. | correct | B:screens[3] |
| l25-fair-from-biased.json | `.screens[3].feedback.byKey.two` | Two flips is one round. Some rounds are thrown away. | correct | B:screens[3] |
| l25-fair-from-biased.json | `.screens[3].feedback.byKey.rounds` | That is the number of rounds, $\tfrac{1}{0.48}$. Double it for flips. | correct | B:screens[3] |
| l25-fair-from-biased.json | `.screens[3].feedback.byKey.fair` | That is the fair coin, $\tfrac{1}{0.25}$. Here $pq = 0.24$. | correct | B:screens[3] |
| l25-fair-from-biased.json | `.screens[3].explain.text` | HT and TH each have chance $pq = 0.24$, so a round succeeds with 0.48. The trick takes $\tfrac{2}{0.48} = \tfrac{25}{6}… | correct | B:screens[3] |
| l25-fair-from-biased.json | `.screens[4].prose` | Now the coin is fair, and you need a fair choice among six. Three flips give eight equally likely strings. Label six of… | correct | B:screens[4] |
| l25-fair-from-biased.json | `.screens[4].widget.accept` | 4 exactly: 3 flips a round, $\tfrac86$ rounds | correct | B:screens[4] |
| l25-fair-from-biased.json | `.screens[4].hints[0].text` | Each round is three flips. How often does a round succeed? | correct | B:screens[4] |
| l25-fair-from-biased.json | `.screens[4].hints[1].text` | Six of the eight strings are kept, so a round succeeds with chance $\tfrac68$. | correct | B:screens[4] |
| l25-fair-from-biased.json | `.screens[4].hints[2].text` | Rounds: $\tfrac86$. Flips: $3 \times \tfrac86$. | correct | B:screens[4] |
| l25-fair-from-biased.json | `.screens[4].feedback.correct` | $3 \times \tfrac86 = 4$ flips. | correct | B:screens[4] |
| l25-fair-from-biased.json | `.screens[4].feedback.generic` | Not quite right. Multiply the flips per round by the expected rounds. | correct | B:screens[4] |
| l25-fair-from-biased.json | `.screens[4].feedback.byKey.three` | Three flips is one round. A quarter of rounds land on TTH or TTT and restart. | correct | B:screens[4] |
| l25-fair-from-biased.json | `.screens[4].feedback.byKey.rounds` | That is the number of rounds, $\tfrac86$. Each round is three flips. | correct | B:screens[4] |
| l25-fair-from-biased.json | `.screens[4].feedback.byKey.six` | You allowed one flip per face. Three flips already give eight strings. | correct | B:screens[4] |
| l25-fair-from-biased.json | `.screens[4].explain.text` | A round of three flips succeeds with chance $\tfrac68 = \tfrac34$, so we expect $\tfrac43$ rounds. That is $3 \times \t… | correct | B:screens[4] |
| l25-fair-from-biased.json | `.screens[5].prose` | A candidate answers at once: flip the $\tfrac23$ coin twice. Call HH heads and anything else tails, because two flips a… | correct | B:screens[5] |
| l25-fair-from-biased.json | `.screens[5].widget.options[0].text` | $\tfrac49$ | correct | B:screens[5] |
| l25-fair-from-biased.json | `.screens[5].widget.options[1].why` | You trusted the averaging. Nothing in two flips cancels a bias: HH has chance $p^2$. | correct | B:screens[5] |
| l25-fair-from-biased.json | `.screens[5].widget.options[2].why` | That is HH for a fair coin. This coin lands heads with $\tfrac23$. | correct | B:screens[5] |
| l25-fair-from-biased.json | `.screens[5].widget.options[3].why` | That is HT, one of the outcomes the pairing trick keeps. | correct | B:screens[5] |
| l25-fair-from-biased.json | `.screens[5].hints[0].text` | Multiply along the HH path. | correct | B:screens[5] |
| l25-fair-from-biased.json | `.screens[5].hints[1].text` | HH has chance $\tfrac23 \times \tfrac23$. | correct | B:screens[5] |
| l25-fair-from-biased.json | `.screens[5].hints[2].text` | That is $\tfrac49$, not $\tfrac12$. | correct | B:screens[5] |
| l25-fair-from-biased.json | `.screens[5].feedback.correct` | $\tfrac49$: the rule is not fair. | correct | B:screens[5] |
| l25-fair-from-biased.json | `.screens[5].feedback.generic` | Not quite right. Find the chance of HH for this coin. | correct | B:screens[5] |
| l25-fair-from-biased.json | `.screens[5].feedback.byKey.b` | You trusted the averaging. HH has chance $p^2 = \tfrac49$, so heads is called too rarely. | correct | B:screens[5] |
| l25-fair-from-biased.json | `.screens[5].explain.text` | HH has chance $p^2 = \tfrac49$, so the rule calls heads 44% of the time. Only outcomes with equal chances for every $p$… | correct | B:screens[5] |
| l25-fair-from-biased.json | `.screens[6].prose` | Every round used one fact. Independent flips give $P(HT) = pq = qp = P(TH)$, whatever $p$ is. So keep HT and TH, and fl… | correct | B:screens[6] |
| l25-fair-from-biased.json | `.screens[6].widget.options[0].text` | Any coin with $0 < p < 1$ | correct | B:screens[6] |
| l25-fair-from-biased.json | `.screens[6].widget.options[1].why` | The bit is exactly fair for any $p$. A strong bias only costs more flips. | correct | B:screens[6] |
| l25-fair-from-biased.json | `.screens[6].widget.options[2].why` | With $p = 1$ every round is HH, so no round ever succeeds. | correct | B:screens[6] |
| l25-fair-from-biased.json | `.screens[6].hints[0].text` | When does a round succeed? | correct | B:screens[6] |
| l25-fair-from-biased.json | `.screens[6].hints[1].text` | A round needs one head and one tail. | correct | B:screens[6] |
| l25-fair-from-biased.json | `.screens[6].hints[2].text` | At $p = 0$ or $p = 1$ that never happens. | correct | B:screens[6] |
| l25-fair-from-biased.json | `.screens[6].feedback.correct` | Any coin that can land both ways. | correct | B:screens[6] |
| l25-fair-from-biased.json | `.screens[6].feedback.generic` | Not quite right. Check $p = 1$: what does every round show? | correct | B:screens[6] |
| l25-fair-from-biased.json | `.screens[6].explain.text` | The bit is fair for every $p$ strictly between 0 and 1. The edge case is $p = 0$ or $p = 1$: the coin never shows both … | correct | B:screens[6] |
| l25-fair-from-biased.json | `.screens[7].prose` | Put the argument in order, one justified line at a time. | correct | B:screens[7] |
| l25-fair-from-biased.json | `.screens[7].widget.lines[0].text` | The two flips are independent. | correct | B:screens[7] |
| l25-fair-from-biased.json | `.screens[7].widget.lines[1].text` | So $P(HT) = P(H)\,P(T) = pq$. | correct | B:screens[7] |
| l25-fair-from-biased.json | `.screens[7].widget.lines[2].text` | And $P(TH) = P(T)\,P(H) = qp$. | correct | B:screens[7] |
| l25-fair-from-biased.json | `.screens[7].widget.lines[3].text` | Since $pq = qp$, a kept round is heads or tails with chance $\tfrac12$ each. | correct | B:screens[7] |
| l25-fair-from-biased.json | `.screens[7].widget.lines[4].text` | A round keeps a result with chance $2pq$, so we wait $\tfrac{1}{2pq}$ rounds. | correct | B:screens[7] |
| l25-fair-from-biased.json | `.screens[7].widget.lines[5].text` | Each round is two flips, so $E[\text{flips}] = \tfrac{1}{pq}$. | correct | B:screens[7] |
| l25-fair-from-biased.json | `.screens[7].widget.lines[6].text` | The coin is fair on average, so HT and TH balance. | correct | B:screens[7] |
| l25-fair-from-biased.json | `.screens[7].widget.lines[6].why` | The coin is not fair. Independence alone makes the two chances equal. | correct | B:screens[7] |
| l25-fair-from-biased.json | `.screens[7].hints[0].text` | Start from what the flips have in common. | correct | B:screens[7] |
| l25-fair-from-biased.json | `.screens[7].hints[1].text` | Independence lets you multiply. | correct | B:screens[7] |
| l25-fair-from-biased.json | `.screens[7].hints[2].text` | Independence, two products, equality, rounds, flips. | correct | B:screens[7] |
| l25-fair-from-biased.json | `.screens[7].feedback.correct` | Independence gives two equal products, then the geometric wait gives the flips. | correct | B:screens[7] |
| l25-fair-from-biased.json | `.screens[7].feedback.generic` | Not quite right. Begin with independence. | correct | B:screens[7] |
| l25-fair-from-biased.json | `.screens[7].feedback.byKey.d1` | You used fairness. The coin is biased; independence does the work. | correct | B:screens[7] |
| l25-fair-from-biased.json | `.screens[7].feedback.byKey.left-out` | Every line except the fairness claim belongs. | correct | B:screens[7] |
| l25-fair-from-biased.json | `.screens[7].feedback.byKey.s6` | The flip count comes last, after the rounds. | correct | B:screens[7] |
| l25-fair-from-biased.json | `.screens[7].explain.text` | Independence makes both kept outcomes a product of $p$ and $q$. Equal products make the bit fair. A geometric wait of $… | correct | B:screens[7] |
| l25-fair-from-biased.json | `.screens[8].prose` | Write `von_neumann(flips)` for a string of `'H'` and `'T'`. Read it in pairs: keep `'H'` for HT and `'T'` for TH. Drop … | correct | B:screens[8] |
| l25-fair-from-biased.json | `.screens[8].widget.how` | Check runs 10 hidden tests. Tests 1 to 4 compare the string of bits. Test 5 feeds in 20,000 flips with $p = 0.8$. It ne… | correct | B:screens[8] |
| l25-fair-from-biased.json | `.screens[8].hints[0].text` | Step through the string two characters at a time. | correct | B:screens[8] |
| l25-fair-from-biased.json | `.screens[8].hints[1].text` | `range(0, len(flips) - 1, 2)` gives the start of each full pair. | correct | B:screens[8] |
| l25-fair-from-biased.json | `.screens[8].hints[2].text` | Keep the first flip of a pair when the two differ. For the wait, `1 / (p * (1 - p))` with `p` a `Fraction`. | correct | B:screens[8] |
| l25-fair-from-biased.json | `.screens[8].feedback.correct` | Pairs in, fair bits out, and the exact wait. | correct | B:screens[8] |
| l25-fair-from-biased.json | `.screens[8].feedback.generic` | Not quite right. Look at the first failing test. | correct | B:screens[8] |
| l25-fair-from-biased.json | `.screens[8].feedback.byKey.test-5` | The bits are not close to fair. Keep only pairs whose two flips differ. | correct | B:screens[8] |
| l25-fair-from-biased.json | `.screens[8].feedback.byKey.test-7` | Return a `Fraction`: `1 / (p * (1 - p))` keeps it exact when `p` is one. | correct | B:screens[8] |
| l25-fair-from-biased.json | `.screens[8].explain.text` | At $p = 0.8$ a pair is kept with chance $2pq = 0.32$, so 20,000 flips give about 3,200 bits. Each kept bit is heads wit… | correct | B:screens[8] |
| l25-fair-from-biased.json | `.screens[9].prose` | Drill: about 3 minutes a puzzle, as interviews allow. Keep your own time and say each argument aloud. Give four decimal… | correct | B:screens[9] |
| l25-fair-from-biased.json | `.screens[9].hints[0].text` | Each answer uses $2pq$, or the share of strings kept. | correct | B:screens[9] |
| l25-fair-from-biased.json | `.screens[9].hints[1].text` | At 0.9, $pq = 0.09$. At 0.7, $2pq = 2 \times 0.7 \times 0.3$. | correct | B:screens[9] |
| l25-fair-from-biased.json | `.screens[9].hints[2].text` | $\tfrac{1}{0.09}$, then $0.42$, then $2 \times \tfrac43$. | correct | B:screens[9] |
| l25-fair-from-biased.json | `.screens[9].feedback.correct` | $\tfrac{100}{9} \approx 11.1111$, $0.42$ and $\tfrac83 \approx 2.6667$. | correct | B:screens[9] |
| l25-fair-from-biased.json | `.screens[9].feedback.generic` | Not quite right. Check the first answer that is marked. | correct | B:screens[9] |
| l25-fair-from-biased.json | `.screens[9].feedback.byKey.r0c1` | Check the first: flips are $\tfrac{1}{pq}$ with $pq = 0.09$. | correct | B:screens[9] |
| l25-fair-from-biased.json | `.screens[9].feedback.byKey.r1c1` | Check the second: a round is kept on HT or TH, $2pq$. | correct | B:screens[9] |
| l25-fair-from-biased.json | `.screens[9].feedback.byKey.r2c1` | Check the third: three of four strings are kept, so $\tfrac43$ rounds of two flips. | correct | B:screens[9] |
| l25-fair-from-biased.json | `.screens[9].explain.text` | At $p = 0.9$, $\tfrac{1}{0.09} = \tfrac{100}{9} \approx 11.1111$ flips. At 0.7 a round is kept with $2 \times 0.21 = 0.… | correct | B:screens[9] |
| l25-fair-from-biased.json | `.screens[10].prose` | The interviewer extends it: a fair choice among three people, with the 0.6 coin. Flip three times. Keep only HTT, THT a… | correct | B:screens[10] |
| l25-fair-from-biased.json | `.screens[10].widget.accept` | 125/12, about 10.4167 | correct | B:screens[10] |
| l25-fair-from-biased.json | `.screens[10].hints[0].text` | Why are the three strings equally likely? | correct | B:screens[10] |
| l25-fair-from-biased.json | `.screens[10].hints[1].text` | Each has one head and two tails: chance $pq^2 = 0.6 \times 0.16 = 0.096$. | correct | B:screens[10] |
| l25-fair-from-biased.json | `.screens[10].hints[2].text` | A round succeeds with $3pq^2 = 0.288$, so the flips are $\tfrac{3}{0.288}$. | correct | B:screens[10] |
| l25-fair-from-biased.json | `.screens[10].feedback.correct` | $\tfrac{3}{3pq^2} = \tfrac{1}{pq^2} = \tfrac{125}{12} \approx 10.4167$. | correct | B:screens[10] |
| l25-fair-from-biased.json | `.screens[10].feedback.generic` | Not quite right. Find the chance a round succeeds, then multiply rounds by three flips. | correct | B:screens[10] |
| l25-fair-from-biased.json | `.screens[10].feedback.byKey.one-string` | You used one kept string, $pq^2$. A round succeeds on any of the three. | correct | B:screens[10] |
| l25-fair-from-biased.json | `.screens[10].feedback.byKey.fair` | That is a fair coin, $\tfrac{3}{3/8}$. This coin has $pq^2 = 0.096$. | correct | B:screens[10] |
| l25-fair-from-biased.json | `.screens[10].feedback.byKey.two-way` | That is the two-way answer. Three people need three equal strings. | correct | B:screens[10] |
| l25-fair-from-biased.json | `.screens[10].explain.text` | HTT, THT and TTH each have chance $pq^2$, so they tie for every $p$. A round succeeds with $3pq^2 = 0.288$, giving $\tf… | correct | B:screens[10] |
| l25-fair-from-biased.json | `.screens[11].prose` | Two desks must split a scarce bond allocation by a fair toss. The only random source is a counterparty's feed of up-tic… | correct | B:screens[11] |
| l25-fair-from-biased.json | `.screens[11].widget.accept` | 25/4 = 6.25 | correct | B:screens[11] |
| l25-fair-from-biased.json | `.screens[11].hints[0].text` | A pair of ticks is kept on up-down or down-up. | correct | B:screens[11] |
| l25-fair-from-biased.json | `.screens[11].hints[1].text` | A pair is kept with chance $2 \times 0.8 \times 0.2 = 0.32$. | correct | B:screens[11] |
| l25-fair-from-biased.json | `.screens[11].hints[2].text` | Ticks: $\tfrac{1}{0.8 \times 0.2}$. | correct | B:screens[11] |
| l25-fair-from-biased.json | `.screens[11].feedback.correct` | $\tfrac{1}{0.16} = 6.25$ ticks. | correct | B:screens[11] |
| l25-fair-from-biased.json | `.screens[11].feedback.generic` | Not quite right. Use $\tfrac{1}{pq}$ with $p = 0.8$. | correct | B:screens[11] |
| l25-fair-from-biased.json | `.screens[11].feedback.byKey.two` | Two ticks is one pair. Most pairs are up-up and get thrown away. | correct | B:screens[11] |
| l25-fair-from-biased.json | `.screens[11].feedback.byKey.rounds` | That is the number of pairs, $\tfrac{1}{0.32}$. Each pair is two ticks. | correct | B:screens[11] |
| l25-fair-from-biased.json | `.screens[11].feedback.byKey.fair` | That is the wait for a fair source. This feed is biased. | correct | B:screens[11] |
| l25-fair-from-biased.json | `.screens[11].explain.text` | A pair is kept with chance 0.32, so 68% of pairs are thrown away. That rejection rate is the price: $\tfrac{1}{0.16} = … | correct | B:screens[11] |
| l25-fair-from-biased.json | `.summary.ideas[0]` | For independent flips, HT and TH both have chance $pq$, so keeping only them gives a fair bit. | correct | B:summary |
| l25-fair-from-biased.json | `.summary.ideas[1]` | A round of two flips succeeds with chance $2pq$, so a fair bit takes $\tfrac{1}{pq}$ flips on average. | correct | B:summary |
| l25-fair-from-biased.json | `.summary.ideas[2]` | Run it in reverse to make any fair choice: keep equally likely strings and start again on the rest. | correct | B:summary |
| l25-fair-from-biased.json | `.summary.formula.note` | Needs $0 < p < 1$; three equal strings of one head cost $\tfrac{1}{pq^2}$. | correct | B:summary |
| l25-fair-from-biased.json | `.summary.trap` | Calling HH heads: its chance is $p^2$, not $\tfrac12$. Two flips do not cancel a bias. | correct | B:summary |
| l25-fair-from-biased.json | `.quiz[0].prose` | Von Neumann's trick keeps HT as heads and TH as tails. | correct | B:quiz[0] |
| l25-fair-from-biased.json | `.quiz[0].widget.options[0].text` | The flips are independent, so both chances are $p \times q$ | correct | B:quiz[0] |
| l25-fair-from-biased.json | `.quiz[0].widget.options[1].why` | You assumed fairness. The coin is biased, and the trick works anyway. | correct | B:quiz[0] |
| l25-fair-from-biased.json | `.quiz[0].widget.options[2].why` | Throwing outcomes away does not equalise the rest. The two kept outcomes are equal because each is $p \times q$. | correct | B:quiz[0] |
| l25-fair-from-biased.json | `.quiz[0].widget.options[3].why` | That is the law of averages. Each kept round is fair on its own. | correct | B:quiz[0] |
| l25-fair-from-biased.json | `.quiz[0].feedback.correct` | Independence: both are $pq$. | correct | B:quiz[0] |
| l25-fair-from-biased.json | `.quiz[0].feedback.generic` | Not quite right. Write out the chance of HT and of TH. | correct | B:quiz[0] |
| l25-fair-from-biased.json | `.quiz[0].explain.text` | Independence gives $P(HT) = pq$ and $P(TH) = qp$. These are equal, so the kept bit is fair. Fairness of the coin is nev… | correct | B:quiz[0] |
| l25-fair-from-biased.json | `.quiz[1].prose` | A coin lands heads every time ($p = 1$). You run the trick. | correct | B:quiz[1] |
| l25-fair-from-biased.json | `.quiz[1].widget.options[0].text` | It never gives one: every round is HH | correct | B:quiz[1] |
| l25-fair-from-biased.json | `.quiz[1].widget.options[1].why` | Every round shows HH and is thrown away. | correct | B:quiz[1] |
| l25-fair-from-biased.json | `.quiz[1].widget.options[2].why` | That is the fair-coin wait, $\tfrac{1}{2pq}$ at $p = \tfrac12$. Here $pq = 0$, so no round ever succeeds. | correct | B:quiz[1] |
| l25-fair-from-biased.json | `.quiz[1].feedback.correct` | Never: the edge case. | correct | B:quiz[1] |
| l25-fair-from-biased.json | `.quiz[1].feedback.generic` | Not quite right. What does every round show? | correct | B:quiz[1] |
| l25-fair-from-biased.json | `.quiz[1].explain.text` | With $p = 1$ every round is HH, so no round succeeds. The formula $\tfrac{1}{pq}$ blows up as $pq$ reaches 0. The trick… | correct | B:quiz[1] |
| l25-fair-from-biased.json | `.quiz[2].prose` | A coin lands heads with chance 0.6. You need a fair choice among four people, so you make two fair bits with the trick. | correct | B:quiz[2] |
| l25-fair-from-biased.json | `.quiz[2].widget.accept` | 25/3, about 8.3333 | correct | B:quiz[2] |
| l25-fair-from-biased.json | `.quiz[2].feedback.correct` | $2 \times \tfrac{25}{6} = \tfrac{25}{3} \approx 8.3333$. | correct | B:quiz[2] |
| l25-fair-from-biased.json | `.quiz[2].feedback.generic` | Not quite right. Find the flips for one bit, then double it. | correct | B:quiz[2] |
| l25-fair-from-biased.json | `.quiz[2].feedback.byKey.one-bit` | That is one bit. Four people need two bits. | correct | B:quiz[2] |
| l25-fair-from-biased.json | `.quiz[2].feedback.byKey.fair` | That is a fair coin, $2 \times 4$. Here $pq = 0.24$. | correct | B:quiz[2] |
| l25-fair-from-biased.json | `.quiz[2].explain.text` | One bit costs $\tfrac{1}{0.24} = \tfrac{25}{6}$ flips. Two bits name one of four people, so $\tfrac{25}{3} \approx 8.33… | correct | B:quiz[2] |

## l26-estimating-n.json

### Bases

| key | basis |
|---|---|
| screens[0] | method of moments for one draw: E[X] = (N+1)/2 so 2X-1 is unbiased; sim: puzzles-L5-concepts-r2.py:estimates 119 |
| screens[1] | Casella and Berger ch. 7 (Lehmann-Scheffe, UMVUE of a uniform endpoint) and Goodman (1954) serial-number estimation (m + m/k - 1 is the UMVUE); sim: puzzles-L5-concepts-r2.py:m + m/k - 1 and 2*mean - 1 are both unbiased (exhaustive); gaps 18, 20, 1, 17; estimates 74, 973.4 |
| screens[9] | Casella and Berger ch. 7 (Lehmann-Scheffe, UMVUE of a uniform endpoint) and Goodman (1954) serial-number estimation (m + m/k - 1 is the UMVUE); sim: puzzles-L5-concepts-r2.py:m + m/k - 1 and 2*mean - 1 are both unbiased (exhaustive); gaps 18, 20, 1, 17; estimates 74, 973.4 |
| quiz[0] | Casella and Berger ch. 7 (Lehmann-Scheffe, UMVUE of a uniform endpoint) and Goodman (1954) serial-number estimation (m + m/k - 1 is the UMVUE); sim: puzzles-L5-concepts-r2.py:m + m/k - 1 and 2*mean - 1 are both unbiased (exhaustive); gaps 18, 20, 1, 17; estimates 74, 973.4 |
| screens[2] | exchangeable gaps; sim: puzzles-L5-concepts-r2.py:E[max] = 14 (k=2, N=20), 8.8 (exhaustive) |
| quiz[1] | exchangeable gaps; sim: puzzles-L5-concepts-r2.py:E[max] = 14 (k=2, N=20), 8.8 (exhaustive) |
| screens[3] | Casella and Berger ch. 7 (Lehmann-Scheffe, UMVUE of a uniform endpoint) and Goodman (1954) serial-number estimation; sim: puzzles-L5-concepts-r2.py:mean-based estimate has twice the variance of the max-based one at k=4 (exhaustive); variance ratio (k+2)/3; the largest seen is never above N; the MLE is m |
| screens[4] | Casella and Berger ch. 7 (Lehmann-Scheffe, UMVUE of a uniform endpoint) and Goodman (1954) serial-number estimation; gap symmetry (Feller vol. 1 II.?: spacings exchangeable); sim: puzzles-L5-concepts-r2.py:E[m] = k(N+1)/(k+1) (exhaustive at five (N,k)); unbiased (exhaustive); estimate 10 when all seen |
| screens[5] | Casella and Berger ch. 7 (Lehmann-Scheffe, UMVUE of a uniform endpoint) and Goodman (1954) serial-number estimation; gap symmetry (Feller vol. 1 II.?: spacings exchangeable); sim: puzzles-L5-concepts-r2.py:E[m] = k(N+1)/(k+1) (exhaustive at five (N,k)); unbiased (exhaustive); estimate 10 when all seen |
| summary | Casella and Berger ch. 7 (Lehmann-Scheffe, UMVUE of a uniform endpoint) and Goodman (1954) serial-number estimation; gap symmetry (Feller vol. 1 II.?: spacings exchangeable); sim: puzzles-L5-concepts-r2.py:E[m] = k(N+1)/(k+1) (exhaustive at five (N,k)); unbiased (exhaustive); estimate 10 when all seen |
| screens[6] | sim: puzzles-L5-concepts-r2.py:solution passes all 8 hidden tests; seed 1 gives 99.94; mean maximum 84.17; tolerance 0.36 is three SE; MC |
| screens[7] | Casella and Berger ch. 7 (Lehmann-Scheffe, UMVUE of a uniform endpoint) and Goodman (1954) serial-number estimation (uniform [0, theta]: (k+1)/k X_(k) unbiased); sympy: sim: puzzles-L5-concepts-r2.py:E[max of k uniforms] = k/(k+1) theta; 1.2 and 2.5; E[max] = 15.75 |
| quiz[2] | Casella and Berger ch. 7 (Lehmann-Scheffe, UMVUE of a uniform endpoint) and Goodman (1954) serial-number estimation (uniform [0, theta]: (k+1)/k X_(k) unbiased); sympy: sim: puzzles-L5-concepts-r2.py:E[max of k uniforms] = k/(k+1) theta; 1.2 and 2.5; E[max] = 15.75 |
| screens[8] | E[R] = E[max] - E[min] = (k-1)(N+1)/(k+1); sim: puzzles-L5-concepts-r2.py:E[R] exhaustive at N=50 and 12; the range estimate averages exactly 50; 202/3 |

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l26-estimating-n.json | `.screens[0].prose` | The cabs in a town are numbered 1 to $N$. You see one cab, chosen at random: number 60. Interviewers ask for your best … | correct | B:screens[0] |
| l26-estimating-n.json | `.screens[0].hints[0].text` | One number from 1 to $N$ averages $\tfrac{N + 1}{2}$. | correct | B:screens[0] |
| l26-estimating-n.json | `.screens[0].hints[1].text` | Set $\tfrac{N + 1}{2} = 60$. | correct | B:screens[0] |
| l26-estimating-n.json | `.screens[0].hints[2].text` | So $N = 2 \times 60 - 1 = 119$. | correct | B:screens[0] |
| l26-estimating-n.json | `.screens[0].feedback.correct` | $N = 119$: then the average cab is exactly 60. | correct | B:screens[0] |
| l26-estimating-n.json | `.screens[0].feedback.generic` | Not quite right. Watch the caption: move $N$ until the average reads 60.0. | correct | B:screens[0] |
| l26-estimating-n.json | `.screens[0].feedback.byKey.max` | You stopped near the number seen. One random number sits near the middle of 1 to $N$, not the top. | correct | B:screens[0] |
| l26-estimating-n.json | `.screens[0].feedback.byKey.double` | Close: 120 is twice 60. The average of 1 to $N$ is $\tfrac{N + 1}{2}$, so take one off. | correct | B:screens[0] |
| l26-estimating-n.json | `.screens[0].feedback.byKey.est` | Read the caption: the average must come to 60.0. | correct | B:screens[0] |
| l26-estimating-n.json | `.screens[0].explain.text` | One random number from 1 to $N$ has mean $\tfrac{N + 1}{2}$. Setting that to 60 gives $N = 119$. The number seen is a m… | correct | B:screens[0] |
| l26-estimating-n.json | `.screens[1].prose` | Now you see four cabs: 19, 40, 42 and 60. The largest, 60, cannot be above $N$. The four numbers leave gaps of unseen n… | correct | B:screens[1] |
| l26-estimating-n.json | `.screens[1].widget.accept` | 74 exactly | correct | B:screens[1] |
| l26-estimating-n.json | `.screens[1].hints[0].text` | Count the unseen numbers below 60. | correct | B:screens[1] |
| l26-estimating-n.json | `.screens[1].hints[1].text` | Below 60 there are $60 - 4 = 56$ unseen numbers, in four gaps. | correct | B:screens[1] |
| l26-estimating-n.json | `.screens[1].hints[2].text` | The average gap is $\tfrac{56}{4} = 14$, so estimate $60 + 14$. | correct | B:screens[1] |
| l26-estimating-n.json | `.screens[1].feedback.correct` | $60 + 14 = 74$. | correct | B:screens[1] |
| l26-estimating-n.json | `.screens[1].feedback.generic` | Not quite right. Find the average size of the four gaps below 60. | correct | B:screens[1] |
| l26-estimating-n.json | `.screens[1].feedback.byKey.max` | You stopped at the largest number. The top gap is hidden, not empty. | correct | B:screens[1] |
| l26-estimating-n.json | `.screens[1].feedback.byKey.mean-based` | That is twice the mean less one. It is a fair estimate too, but we asked for the largest plus the average gap. | correct | B:screens[1] |
| l26-estimating-n.json | `.screens[1].feedback.byKey.no-minus-one` | You added $\tfrac{60}{4} = 15$. The gaps hold $60 - 4$ numbers, so the average is 14. | correct | B:screens[1] |
| l26-estimating-n.json | `.screens[1].explain.text` | The gaps below 60 hold 18, 20, 1 and 17 unseen numbers: 56 in all, 14 on average. Adding one average gap above the larg… | correct | B:screens[1] |
| l26-estimating-n.json | `.screens[2].prose` | Two numbers are drawn from 1 to 20 without replacement. Bar $m$ shows the chance that the larger is $m$: it rises in a … | correct | B:screens[2] |
| l26-estimating-n.json | `.screens[2].hints[0].text` | Use gaps rather than the bars. | correct | B:screens[2] |
| l26-estimating-n.json | `.screens[2].hints[1].text` | 18 numbers go unseen. The two draws cut them into three gaps of equal mean. | correct | B:screens[2] |
| l26-estimating-n.json | `.screens[2].hints[2].text` | Each gap averages 6, so the top gap is 6 and the larger averages $20 - 6 = 14$. | correct | B:screens[2] |
| l26-estimating-n.json | `.screens[2].feedback.correct` | The bars balance at 14. | correct | B:screens[2] |
| l26-estimating-n.json | `.screens[2].feedback.generic` | Not quite right. Work out the mean of the gap above the larger number. | correct | B:screens[2] |
| l26-estimating-n.json | `.screens[2].feedback.byKey.middle` | You balanced at the middle of 1 to 20. That is the mean of one draw; the larger of two sits higher. | correct | B:screens[2] |
| l26-estimating-n.json | `.screens[2].feedback.byKey.top` | The larger is often below 20. The gap above it averages 6. | correct | B:screens[2] |
| l26-estimating-n.json | `.screens[2].feedback.byKey.pivot` | The top gap averages $\tfrac{18}{3} = 6$. Balance the bars 6 below 20. | correct | B:screens[2] |
| l26-estimating-n.json | `.screens[2].explain.text` | The 18 unseen numbers fall into three gaps, and by symmetry each has mean 6. So the larger number averages $20 - 6 = 14… | correct | B:screens[2] |
| l26-estimating-n.json | `.screens[3].prose` | Back to the four cabs: 19, 40, 42 and 60. Three candidates give three different estimates of $N$. | correct | B:screens[3] |
| l26-estimating-n.json | `.screens[3].widget.options[0].text` | 74, the largest plus the average gap | correct | B:screens[3] |
| l26-estimating-n.json | `.screens[3].widget.options[1].why` | The largest number seen is never above $N$, so on average it is too low. | correct | B:screens[3] |
| l26-estimating-n.json | `.screens[3].widget.options[2].why` | It is unbiased too, but it varies more. With four numbers its variance is twice that of 74. | correct | B:screens[3] |
| l26-estimating-n.json | `.screens[3].widget.options[3].why` | That is the one-number rule. With four numbers the largest is much closer to $N$. | correct | B:screens[3] |
| l26-estimating-n.json | `.screens[3].hints[0].text` | Ask which estimates are right on average, then which varies less. | correct | B:screens[3] |
| l26-estimating-n.json | `.screens[3].hints[1].text` | The largest seen is always at most $N$. | correct | B:screens[3] |
| l26-estimating-n.json | `.screens[3].hints[2].text` | The max-based estimate and the mean-based one are both fair; the max-based one has half the variance at $k = 4$. | correct | B:screens[3] |
| l26-estimating-n.json | `.screens[3].feedback.correct` | 74: fair on average and the least noisy. | imprecise | finding 2: the raw maximum has lower variance (ratio (k/(k+1))^2 = 0.64 at k=4); least noisy among UNBIASED estimates only (UMVUE); sim: puzzles-L5-concepts-r2.py:EXPECTED_FAIL the max-based estimate is not less noisy than the raw maximum |
| l26-estimating-n.json | `.screens[3].feedback.generic` | Not quite right. Compare each estimate with $N$ on average. | correct | B:screens[3] |
| l26-estimating-n.json | `.screens[3].feedback.byKey.b` | You quoted the largest number seen. It can never be above $N$, so it is always low on average. | correct | B:screens[3] |
| l26-estimating-n.json | `.screens[3].feedback.byKey.c` | Twice the mean less one is fair too, but it varies more. The largest number carries more information. | correct | B:screens[3] |
| l26-estimating-n.json | `.screens[3].explain.text` | The largest number seen sits below $N$ on average, so 60 is biased low. Twice the mean less one is fair but noisy, as i… | correct | B:screens[3] |
| l26-estimating-n.json | `.screens[4].prose` | Every estimate added one average gap to the largest number seen, $m$. With $k$ numbers seen, the gaps below $m$ hold $m… | correct | B:screens[4] |
| l26-estimating-n.json | `.screens[4].widget.options[0].text` | 10 | correct | B:screens[4] |
| l26-estimating-n.json | `.screens[4].widget.options[1].why` | Here $\tfrac{m}{k} = 1$, and the $-1$ cancels it. With nothing unseen, there is no gap to add. | correct | B:screens[4] |
| l26-estimating-n.json | `.screens[4].widget.options[2].why` | That is the one-number rule, $2m - 1$. Here $k = 10$. | correct | B:screens[4] |
| l26-estimating-n.json | `.screens[4].hints[0].text` | Put $m = 10$ and $k = 10$ into the formula. | correct | B:screens[4] |
| l26-estimating-n.json | `.screens[4].hints[1].text` | $\tfrac{m}{k} = 1$. | correct | B:screens[4] |
| l26-estimating-n.json | `.screens[4].hints[2].text` | $10 + 1 - 1 = 10$. | correct | B:screens[4] |
| l26-estimating-n.json | `.screens[4].feedback.correct` | 10: when every number is seen, the formula returns $N$ exactly. | correct | B:screens[4] |
| l26-estimating-n.json | `.screens[4].feedback.generic` | Not quite right. Substitute $m = k = 10$. | correct | B:screens[4] |
| l26-estimating-n.json | `.screens[4].explain.text` | With $k = N$ the largest seen is $N$ and every gap is empty. The formula gives $N + 1 - 1 = N$. This is the edge case: … | correct | B:screens[4] |
| l26-estimating-n.json | `.screens[5].prose` | Put the gap argument in order, one justified line at a time. | correct | B:screens[5] |
| l26-estimating-n.json | `.screens[5].widget.lines[0].text` | The $k$ numbers seen leave $N - k$ unseen numbers. | correct | B:screens[5] |
| l26-estimating-n.json | `.screens[5].widget.lines[1].text` | They fall into $k + 1$ gaps: below the smallest, between neighbours, and above the largest. | correct | B:screens[5] |
| l26-estimating-n.json | `.screens[5].widget.lines[2].text` | By symmetry each gap has the same mean, $\tfrac{N - k}{k + 1}$. | correct | B:screens[5] |
| l26-estimating-n.json | `.screens[5].widget.lines[3].text` | The top gap runs from $m + 1$ to $N$, so $E[N - m] = \tfrac{N - k}{k + 1}$. | correct | B:screens[5] |
| l26-estimating-n.json | `.screens[5].widget.lines[4].text` | So $E[m] = N - \tfrac{N - k}{k + 1} = \tfrac{k(N + 1)}{k + 1}$. | correct | B:screens[5] |
| l26-estimating-n.json | `.screens[5].widget.lines[5].text` | Solving, $N = \tfrac{k + 1}{k}E[m] - 1$, so $m + \tfrac{m}{k} - 1$ has mean $N$. | correct | B:screens[5] |
| l26-estimating-n.json | `.screens[5].widget.lines[6].text` | The largest number is the most likely value of $N$, so it is unbiased. | correct | B:screens[5] |
| l26-estimating-n.json | `.screens[5].widget.lines[6].why` | Most likely is not the same as right on average. The largest never exceeds $N$, so its mean is below $N$. | correct | B:screens[5] |
| l26-estimating-n.json | `.screens[5].hints[0].text` | Start with the numbers you did not see. | correct | B:screens[5] |
| l26-estimating-n.json | `.screens[5].hints[1].text` | There are $k + 1$ gaps, all alike by symmetry. | correct | B:screens[5] |
| l26-estimating-n.json | `.screens[5].hints[2].text` | Unseen, gaps, equal means, top gap, $E[m]$, solve. | correct | B:screens[5] |
| l26-estimating-n.json | `.screens[5].feedback.correct` | Gaps of equal mean give $E[m]$, and solving gives the estimate. | correct | B:screens[5] |
| l26-estimating-n.json | `.screens[5].feedback.generic` | Not quite right. Begin with the unseen numbers and their gaps. | correct | B:screens[5] |
| l26-estimating-n.json | `.screens[5].feedback.byKey.d1` | You used "most likely". The largest is never above $N$, so its average is below $N$. | correct | B:screens[5] |
| l26-estimating-n.json | `.screens[5].feedback.byKey.left-out` | Every line except the "most likely" claim belongs. | correct | B:screens[5] |
| l26-estimating-n.json | `.screens[5].explain.text` | Check at $k = 3$, $N = 20$: $E[m] = \tfrac{3 \times 21}{4} = 15.75$, which matches counting all 1,140 triples. The esti… | correct | B:screens[5] |
| l26-estimating-n.json | `.screens[6].prose` | Write `tank_estimate(serials)`, returning $m + \tfrac{m}{k} - 1$ as a `Fraction`. Then write `tank_sim(N, k, trials, se… | correct | B:screens[6] |
| l26-estimating-n.json | `.screens[6].widget.how` | Check runs 8 hidden tests. Tests 1 to 5 need an exact `Fraction`. Tests 6 and 7 run 20,000 samples. They accept a mean … | correct | B:screens[6] |
| l26-estimating-n.json | `.screens[6].hints[0].text` | `Fraction(m, k)` keeps $\tfrac{m}{k}$ exact. | correct | B:screens[6] |
| l26-estimating-n.json | `.screens[6].hints[1].text` | `rng.sample(range(1, N + 1), k)` draws without replacement. | correct | B:screens[6] |
| l26-estimating-n.json | `.screens[6].hints[2].text` | Add up each sample's estimate and maximum, then divide both by `trials`. | correct | B:screens[6] |
| l26-estimating-n.json | `.screens[6].feedback.correct` | Exact estimates, and a simulation that centres on $N$. | correct | B:screens[6] |
| l26-estimating-n.json | `.screens[6].feedback.generic` | Not quite right. Look at the first failing test. | correct | B:screens[6] |
| l26-estimating-n.json | `.screens[6].feedback.byKey.test-1` | Return a `Fraction`: `m + Fraction(m, k) - 1`. | correct | B:screens[6] |
| l26-estimating-n.json | `.screens[6].feedback.byKey.test-6` | The mean estimate is far from 100. Check that each sample draws without replacement. | correct | B:screens[6] |
| l26-estimating-n.json | `.screens[6].explain.text` | With $N = 100$ and $k = 5$, 20,000 samples pin the mean estimate within 0.35 of 100. Seed 1 gives about 99.94. The mean… | correct | B:screens[6] |
| l26-estimating-n.json | `.screens[7].prose` | Drill: about 3 minutes a puzzle, as interviews allow. Keep your own time and say each argument aloud. Give four decimal… | correct | B:screens[7] |
| l26-estimating-n.json | `.screens[7].hints[0].text` | Each is the largest plus an average gap. | correct | B:screens[7] |
| l26-estimating-n.json | `.screens[7].hints[1].text` | $E[m] = \tfrac{k(N + 1)}{k + 1}$; for uniforms, $E[m] = \tfrac{k}{k + 1}\theta$. | correct | B:screens[7] |
| l26-estimating-n.json | `.screens[7].hints[2].text` | $100 + 20 - 1$, then $\tfrac{3 \times 21}{4}$, then $\tfrac43 \times 0.9$. | correct | B:screens[7] |
| l26-estimating-n.json | `.screens[7].feedback.correct` | 119, 15.75 and 1.2. | correct | B:screens[7] |
| l26-estimating-n.json | `.screens[7].feedback.generic` | Not quite right. Check the first answer that is marked. | correct | B:screens[7] |
| l26-estimating-n.json | `.screens[7].feedback.byKey.r0c1` | Check the first: $m + \tfrac{m}{k} - 1$ with $m = 100$, $k = 5$. | correct | B:screens[7] |
| l26-estimating-n.json | `.screens[7].feedback.byKey.r1c1` | Check the second: 17 unseen numbers in four gaps; the top gap averages 4.25. | correct | B:screens[7] |
| l26-estimating-n.json | `.screens[7].feedback.byKey.r2c1` | Check the third: three uniforms leave four equal gaps, so $E[m] = \tfrac34\theta$. | correct | B:screens[7] |
| l26-estimating-n.json | `.screens[7].explain.text` | $100 + 20 - 1 = 119$. Three numbers from 20 leave four gaps of mean 4.25, so $E[m] = 15.75$. Three uniforms cut $[0, \t… | correct | B:screens[7] |
| l26-estimating-n.json | `.screens[8].prose` | The interviewer extends it: the numbers run from an unknown start, $a + 1$ to $a + N$. You see 23, 41, 57 and 64. Use t… | correct | B:screens[8] |
| l26-estimating-n.json | `.screens[8].widget.accept` | 202/3, about 67.3333 | correct | B:screens[8] |
| l26-estimating-n.json | `.screens[8].hints[0].text` | Solve the mean of $R$ for $N$. | correct | B:screens[8] |
| l26-estimating-n.json | `.screens[8].hints[1].text` | $N = R\,\tfrac{k + 1}{k - 1} - 1$. | correct | B:screens[8] |
| l26-estimating-n.json | `.screens[8].hints[2].text` | $R = 64 - 23 = 41$, so $41 \times \tfrac53 - 1$. | correct | B:screens[8] |
| l26-estimating-n.json | `.screens[8].feedback.correct` | $41 \times \tfrac53 - 1 = \tfrac{202}{3} \approx 67.3333$. | correct | B:screens[8] |
| l26-estimating-n.json | `.screens[8].feedback.generic` | Not quite right. Solve $E[R] = \tfrac{(k - 1)(N + 1)}{k + 1}$ for $N$, then put in $R = 41$. | correct | B:screens[8] |
| l26-estimating-n.json | `.screens[8].feedback.byKey.no-minus-one` | You found $N + 1$. Take one off. | correct | B:screens[8] |
| l26-estimating-n.json | `.screens[8].feedback.byKey.from-one` | That assumes the numbers start at 1. Here the start is unknown, so use the range. | correct | B:screens[8] |
| l26-estimating-n.json | `.screens[8].feedback.byKey.range` | The range is shorter than $N$: two end gaps are hidden. | correct | B:screens[8] |
| l26-estimating-n.json | `.screens[8].explain.text` | Solving $E[R] = \tfrac{(k - 1)(N + 1)}{k + 1}$ gives $\hat N = R\,\tfrac{k + 1}{k - 1} - 1$. With $R = 41$ and $k = 4$ … | correct | B:screens[8] |
| l26-estimating-n.json | `.screens[9].prose` | A counterparty's order ids run 1, 2, 3 and upwards through the day. Five of their orders reach you at random, with ids … | correct | B:screens[9] |
| l26-estimating-n.json | `.screens[9].widget.accept` | 4867/5 = 973.4 | correct | B:screens[9] |
| l26-estimating-n.json | `.screens[9].hints[0].text` | This is the serial-number problem. | correct | B:screens[9] |
| l26-estimating-n.json | `.screens[9].hints[1].text` | $m = 812$ and $k = 5$. | correct | B:screens[9] |
| l26-estimating-n.json | `.screens[9].hints[2].text` | $812 + \tfrac{812}{5} - 1$. | correct | B:screens[9] |
| l26-estimating-n.json | `.screens[9].feedback.correct` | $812 + 162.4 - 1 = 973.4$ orders. | correct | B:screens[9] |
| l26-estimating-n.json | `.screens[9].feedback.generic` | Not quite right. Use $m + \tfrac{m}{k} - 1$. | correct | B:screens[9] |
| l26-estimating-n.json | `.screens[9].feedback.byKey.max` | The largest id seen is a lower bound, low on average. | correct | B:screens[9] |
| l26-estimating-n.json | `.screens[9].feedback.byKey.no-minus-one` | You added $\tfrac{m}{k}$ but not the $-1$. | correct | B:screens[9] |
| l26-estimating-n.json | `.screens[9].feedback.byKey.double` | That doubles the largest, the rule for one id. You have five. | correct | B:screens[9] |
| l26-estimating-n.json | `.screens[9].explain.text` | The ids are serial numbers, so the largest plus the average gap applies. $812 + \tfrac{812}{5} - 1 = 973.4$, about 970 … | correct | B:screens[9] |
| l26-estimating-n.json | `.summary.ideas[0]` | The largest serial number seen is never above $N$, so on its own it is too low on average. | correct | B:summary |
| l26-estimating-n.json | `.summary.ideas[1]` | The $k$ numbers seen cut the unseen ones into $k + 1$ gaps of equal mean. Add one gap to the largest. | correct | B:summary |
| l26-estimating-n.json | `.summary.ideas[2]` | When the start is unknown, use the range, which hides two end gaps instead of one. | correct | B:summary |
| l26-estimating-n.json | `.summary.formula.note` | Unknown start: $\hat N = R\,\tfrac{k + 1}{k - 1} - 1$. | correct | B:summary |
| l26-estimating-n.json | `.summary.trap` | Quoting the largest number seen: it is always at most $N$, so it is biased low. | correct | B:summary |
| l26-estimating-n.json | `.quiz[0].prose` | Two serial numbers are seen: 30 and 50. | correct | B:quiz[0] |
| l26-estimating-n.json | `.quiz[0].widget.accept` | 74 exactly | correct | B:quiz[0] |
| l26-estimating-n.json | `.quiz[0].feedback.correct` | $50 + 25 - 1 = 74$. | correct | B:quiz[0] |
| l26-estimating-n.json | `.quiz[0].feedback.generic` | Not quite right. Use $m + \tfrac{m}{k} - 1$. | correct | B:quiz[0] |
| l26-estimating-n.json | `.quiz[0].feedback.byKey.max` | The largest seen is low on average. | correct | B:quiz[0] |
| l26-estimating-n.json | `.quiz[0].feedback.byKey.no-minus-one` | You added $\tfrac{m}{k}$ but not the $-1$. | correct | B:quiz[0] |
| l26-estimating-n.json | `.quiz[0].explain.text` | Below 50 there are 48 unseen numbers in two gaps, 24 on average. So $50 + 24 = 74$. | correct | B:quiz[0] |
| l26-estimating-n.json | `.quiz[1].prose` | Four numbers are drawn from 1 to 10 without replacement. | correct | B:quiz[1] |
| l26-estimating-n.json | `.quiz[1].widget.accept` | 44/5 = 8.8 | correct | B:quiz[1] |
| l26-estimating-n.json | `.quiz[1].feedback.correct` | $\tfrac{4 \times 11}{5} = 8.8$. | correct | B:quiz[1] |
| l26-estimating-n.json | `.quiz[1].feedback.generic` | Not quite right. Count the unseen numbers and the gaps. | correct | B:quiz[1] |
| l26-estimating-n.json | `.quiz[1].feedback.byKey.ten` | The largest is often below 10. | correct | B:quiz[1] |
| l26-estimating-n.json | `.quiz[1].feedback.byKey.one-draw` | That is the mean of one draw. The largest of four sits higher. | correct | B:quiz[1] |
| l26-estimating-n.json | `.quiz[1].explain.text` | Six numbers go unseen, in five gaps of mean 1.2. The top gap averages 1.2, so $E[m] = 10 - 1.2 = 8.8$. | correct | B:quiz[1] |
| l26-estimating-n.json | `.quiz[2].prose` | Four draws are uniform on $[0, \theta]$. The largest is 2. | correct | B:quiz[2] |
| l26-estimating-n.json | `.quiz[2].widget.accept` | 5/2 = 2.5 | correct | B:quiz[2] |
| l26-estimating-n.json | `.quiz[2].feedback.correct` | $\tfrac54 \times 2 = 2.5$. | correct | B:quiz[2] |
| l26-estimating-n.json | `.quiz[2].feedback.generic` | Not quite right. Four draws cut $[0, \theta]$ into five equal gaps on average. | correct | B:quiz[2] |
| l26-estimating-n.json | `.quiz[2].feedback.byKey.max` | The largest draw is below $\theta$ on average. | correct | B:quiz[2] |
| l26-estimating-n.json | `.quiz[2].feedback.byKey.double` | Doubling suits one draw. Four draws leave a smaller top gap. | correct | B:quiz[2] |
| l26-estimating-n.json | `.quiz[2].explain.text` | Four uniforms leave five gaps of equal mean, so $E[m] = \tfrac45\theta$. Then $\hat\theta = \tfrac54 \times 2 = 2.5$. | correct | B:quiz[2] |

## l27-given-the-total.json

### Bases

| key | basis |
|---|---|
| screens[0] | Grimmett and Stirzaker, Probability and Random Processes 4.13 problem 4 (Bertrand) and 1.4 (conditional probability) (P(A\|B) = \|A and B\|/\|B\| for equally likely outcomes); sim: puzzles-L5-concepts-r2.py:five rolls total 8; both even 3/5; total 12 forces (6,6); double given 8: 1/5 |
| screens[1] | Grimmett and Stirzaker, Probability and Random Processes 4.13 problem 4 (Bertrand) and 1.4 (conditional probability) (P(A\|B) = \|A and B\|/\|B\| for equally likely outcomes); sim: puzzles-L5-concepts-r2.py:five rolls total 8; both even 3/5; total 12 forces (6,6); double given 8: 1/5 |
| screens[5] | Grimmett and Stirzaker, Probability and Random Processes 4.13 problem 4 (Bertrand) and 1.4 (conditional probability) (P(A\|B) = \|A and B\|/\|B\| for equally likely outcomes); sim: puzzles-L5-concepts-r2.py:five rolls total 8; both even 3/5; total 12 forces (6,6); double given 8: 1/5 |
| quiz[1] | Grimmett and Stirzaker, Probability and Random Processes 4.13 problem 4 (Bertrand) and 1.4 (conditional probability) (P(A\|B) = \|A and B\|/\|B\| for equally likely outcomes); sim: puzzles-L5-concepts-r2.py:five rolls total 8; both even 3/5; total 12 forces (6,6); double given 8: 1/5 |
| screens[2] | sim: puzzles-L5-concepts-r2.py:E[max \| total 10] = 17/3; unconditional 161/36 |
| screens[3] | sim: puzzles-L5-concepts-r2.py:nine rolls with max 5; both 5 with 1/9; given max 5 the other die is 5 with 1/9 and each of 1..4 with 2/9: not uniform; dependent given a total or a maximum |
| screens[4] | sim: puzzles-L5-concepts-r2.py:nine rolls with max 5; both 5 with 1/9; given max 5 the other die is 5 with 1/9 and each of 1..4 with 2/9: not uniform; dependent given a total or a maximum |
| summary | sim: puzzles-L5-concepts-r2.py:nine rolls with max 5; both 5 with 1/9; given max 5 the other die is 5 with 1/9 and each of 1..4 with 2/9: not uniform; dependent given a total or a maximum |
| screens[6] | sim: puzzles-L5-concepts-r2.py:E[total \| max 5] = 70/9; unconditional 7 |
| screens[7] | sim: puzzles-L5-concepts-r2.py:solution passes all 9 hidden tests; ten-sided dice total 11 give mean larger 8 |
| screens[8] | sim: puzzles-L5-concepts-r2.py:2/5, 36/11, 1/3; three dice total 5 in six ways, three with a 3 |
| screens[9] | sim: puzzles-L5-concepts-r2.py:2/5, 36/11, 1/3; three dice total 5 in six ways, three with a 3 |
| screens[10] | sim: puzzles-L5-concepts-r2.py:n-sided dice total n+1: E[max] = (3n+2)/4 = 5, 8, 75.5 (exhaustive) |
| screens[11] | sim: puzzles-L5-concepts-r2.py:two-day P&L: 1/2 given +1, 0 given +2, unconditional 0.64 |
| quiz[0] | sim: puzzles-L5-concepts-r2.py:both hearts given same colour: 78/650 = 0.12 |
| quiz[2] | symmetry of the two dice given the total; sim: puzzles-L5-concepts-r2.py:first die given 9: 4.5 |

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l27-given-the-total.json | `.screens[0].prose` | Roll two fair dice. A friend peeks and tells you the total is 8. Each cell shows the total of one of the 36 equally lik… | correct | B:screens[0] |
| l27-given-the-total.json | `.screens[0].hints[0].text` | Find every cell showing 8. | correct | B:screens[0] |
| l27-given-the-total.json | `.screens[0].hints[1].text` | The 8s run along a diagonal. | correct | B:screens[0] |
| l27-given-the-total.json | `.screens[0].hints[2].text` | There are five: (2, 6), (3, 5), (4, 4), (5, 3) and (6, 2). | correct | B:screens[0] |
| l27-given-the-total.json | `.screens[0].feedback.correct` | Five rolls total 8. | correct | B:screens[0] |
| l27-given-the-total.json | `.screens[0].feedback.generic` | Not quite right. Tap every cell that shows 8, and nothing else. | correct | B:screens[0] |
| l27-given-the-total.json | `.screens[0].feedback.byKey.unordered` | You counted (2, 6) but not (6, 2). They are different rolls: the first die differs. | correct | B:screens[0] |
| l27-given-the-total.json | `.screens[0].explain.text` | Five cells show 8, from (2, 6) to (6, 2). The other 31 rolls contradict what you were told, so they drop out. The five … | correct | B:screens[0] |
| l27-given-the-total.json | `.screens[1].prose` | The five rolls that total 8 are now the whole sample space. This is the **reduced sample space**: the condition throws … | correct | B:screens[1] |
| l27-given-the-total.json | `.screens[1].widget.accept` | 3/5 = 0.6 | correct | B:screens[1] |
| l27-given-the-total.json | `.screens[1].hints[0].text` | Count the even pairs inside the five cells. | correct | B:screens[1] |
| l27-given-the-total.json | `.screens[1].hints[1].text` | (2, 6), (4, 4) and (6, 2) are both even. | correct | B:screens[1] |
| l27-given-the-total.json | `.screens[1].hints[2].text` | 3 of 5. | correct | B:screens[1] |
| l27-given-the-total.json | `.screens[1].feedback.correct` | $\tfrac35 = 0.6$. | correct | B:screens[1] |
| l27-given-the-total.json | `.screens[1].feedback.generic` | Not quite right. Count inside the five shaded cells only. | correct | B:screens[1] |
| l27-given-the-total.json | `.screens[1].feedback.byKey.unconditional` | That is the chance before the condition, $\tfrac{9}{36}$. The total of 8 changes it. | correct | B:screens[1] |
| l27-given-the-total.json | `.screens[1].feedback.byKey.unordered` | You listed {2, 6}, {3, 5} and {4, 4} once each. But (2, 6) and (6, 2) are two rolls, while (4, 4) is one. | correct | B:screens[1] |
| l27-given-the-total.json | `.screens[1].explain.text` | Three of the five rolls are both even: (2, 6), (4, 4) and (6, 2). So the chance is $\tfrac35$, up from $\tfrac14$. An e… | correct | B:screens[1] |
| l27-given-the-total.json | `.screens[2].prose` | Now each cell shows the larger of the two dice. You are told the total is 10. | correct | B:screens[2] |
| l27-given-the-total.json | `.screens[2].widget.accept` | 17/3, about 5.6667 | correct | B:screens[2] |
| l27-given-the-total.json | `.screens[2].hints[0].text` | Read the larger die in each shaded cell. | correct | B:screens[2] |
| l27-given-the-total.json | `.screens[2].hints[1].text` | The cells (4, 6), (5, 5) and (6, 4) show 6, 5 and 6. | correct | B:screens[2] |
| l27-given-the-total.json | `.screens[2].hints[2].text` | $\tfrac{6 + 5 + 6}{3}$. | correct | B:screens[2] |
| l27-given-the-total.json | `.screens[2].feedback.correct` | $\tfrac{17}{3} \approx 5.6667$. | correct | B:screens[2] |
| l27-given-the-total.json | `.screens[2].feedback.generic` | Not quite right. Average the larger die over the three shaded cells. | correct | B:screens[2] |
| l27-given-the-total.json | `.screens[2].feedback.byKey.each-die` | That is the mean of either die, $\tfrac{10}{2}$. The larger die is at least that. | correct | B:screens[2] |
| l27-given-the-total.json | `.screens[2].feedback.byKey.unordered` | You averaged {4, 6} and {5, 5} once each. (4, 6) and (6, 4) are two rolls. | correct | B:screens[2] |
| l27-given-the-total.json | `.screens[2].feedback.byKey.unconditional` | That is the larger die with no condition, $\tfrac{161}{36}$. | correct | B:screens[2] |
| l27-given-the-total.json | `.screens[2].explain.text` | Three rolls total 10, and their larger dice are 6, 5 and 6. The mean is $\tfrac{17}{3} \approx 5.67$. A conditional mea… | correct | B:screens[2] |
| l27-given-the-total.json | `.screens[3].prose` | A twist: you are told the larger die is 5, not the total. The cells still show the larger die. | correct | B:screens[3] |
| l27-given-the-total.json | `.screens[3].hints[0].text` | Look for every cell showing 5. | correct | B:screens[3] |
| l27-given-the-total.json | `.screens[3].hints[1].text` | They form an L: row 5 and column 5, up to (5, 5). | correct | B:screens[3] |
| l27-given-the-total.json | `.screens[3].hints[2].text` | 5 in row 5 plus 4 more in column 5: nine cells. | correct | B:screens[3] |
| l27-given-the-total.json | `.screens[3].feedback.correct` | Nine rolls: an L of $2 \times 5 - 1$ cells. | correct | B:screens[3] |
| l27-given-the-total.json | `.screens[3].feedback.generic` | Not quite right. Tap every cell that shows 5. | correct | B:screens[3] |
| l27-given-the-total.json | `.screens[3].feedback.byKey.cross` | You took all of row 5 and column 5. (5, 6) and (6, 5) have larger die 6. | correct | B:screens[3] |
| l27-given-the-total.json | `.screens[3].feedback.byKey.row` | You fixed the first die at 5. The second die can be the 5 instead. | correct | B:screens[3] |
| l27-given-the-total.json | `.screens[3].explain.text` | The larger die is 5 when one die is 5 and the other at most 5. That is row 5 and column 5 up to (5, 5): $2 \times 5 - 1… | correct | B:screens[3] |
| l27-given-the-total.json | `.screens[4].prose` | Given that the larger die is 5, a candidate says: one die is a 5, and the other is fair. So both are 5 with chance $\tf… | correct | B:screens[4] |
| l27-given-the-total.json | `.screens[4].widget.options[0].text` | $\tfrac19$ | correct | B:screens[4] |
| l27-given-the-total.json | `.screens[4].widget.options[1].why` | You kept the other die uniform. The condition changes it: (5, 5) is one cell of nine. | correct | B:screens[4] |
| l27-given-the-total.json | `.screens[4].widget.options[2].why` | You listed the other die as 1 to 5, equally likely. But (5, 2) and (2, 5) are two cells, while (5, 5) is one. | correct | B:screens[4] |
| l27-given-the-total.json | `.screens[4].widget.options[3].why` | That is the chance before the condition. | correct | B:screens[4] |
| l27-given-the-total.json | `.screens[4].hints[0].text` | Count inside the shaded L. | correct | B:screens[4] |
| l27-given-the-total.json | `.screens[4].hints[1].text` | The L has nine equally likely cells. | correct | B:screens[4] |
| l27-given-the-total.json | `.screens[4].hints[2].text` | Only one of them is (5, 5). | correct | B:screens[4] |
| l27-given-the-total.json | `.screens[4].feedback.correct` | $\tfrac19$: one cell of nine. | correct | B:screens[4] |
| l27-given-the-total.json | `.screens[4].feedback.generic` | Not quite right. Count the cells of the L and the cells where both are 5. | correct | B:screens[4] |
| l27-given-the-total.json | `.screens[4].feedback.byKey.b` | You treated the other die as still fair. Given the maximum, the other die is not uniform. | correct | B:screens[4] |
| l27-given-the-total.json | `.screens[4].feedback.byKey.c` | You split the other die evenly over 1 to 5. A 5 alongside is one roll; a 2 alongside is two. | correct | B:screens[4] |
| l27-given-the-total.json | `.screens[4].explain.text` | Nine rolls have larger die 5, and only (5, 5) has both. So the chance is $\tfrac19$. The other die is not fair after th… | correct | B:screens[4] |
| l27-given-the-total.json | `.screens[5].prose` | Each answer kept only the rolls that agree with the condition $B$, each still equally likely, and counted inside them: … | correct | B:screens[5] |
| l27-given-the-total.json | `.screens[5].widget.options[0].text` | 1 | correct | B:screens[5] |
| l27-given-the-total.json | `.screens[5].widget.options[1].why` | That is before the condition. A total of 12 leaves one roll. | correct | B:screens[5] |
| l27-given-the-total.json | `.screens[5].widget.options[2].why` | You kept one die uniform. A total of 12 forces both dice. | correct | B:screens[5] |
| l27-given-the-total.json | `.screens[5].hints[0].text` | List the rolls with total 12. | correct | B:screens[5] |
| l27-given-the-total.json | `.screens[5].hints[1].text` | Only (6, 6). | correct | B:screens[5] |
| l27-given-the-total.json | `.screens[5].hints[2].text` | One roll of one. | correct | B:screens[5] |
| l27-given-the-total.json | `.screens[5].feedback.correct` | 1: a total of 12 leaves nothing uncertain. | correct | B:screens[5] |
| l27-given-the-total.json | `.screens[5].feedback.generic` | Not quite right. How many rolls total 12? | correct | B:screens[5] |
| l27-given-the-total.json | `.screens[5].explain.text` | The edge case: a total of 2 or 12 leaves one roll. Then every conditional chance is 0 or 1. | correct | B:screens[5] |
| l27-given-the-total.json | `.screens[6].prose` | Given the larger die is 5, find the expected total. Put the working in order, one justified line at a time. | correct | B:screens[6] |
| l27-given-the-total.json | `.screens[6].widget.lines[0].text` | The rolls with larger die 5 are $(5, b)$ for $b \le 5$ and $(a, 5)$ for $a \le 4$. | correct | B:screens[6] |
| l27-given-the-total.json | `.screens[6].widget.lines[1].text` | That is $5 + 4 = 9$ equally likely rolls. | correct | B:screens[6] |
| l27-given-the-total.json | `.screens[6].widget.lines[2].text` | The rolls $(5, b)$ have totals 6 to 10, which add to 40. | correct | B:screens[6] |
| l27-given-the-total.json | `.screens[6].widget.lines[3].text` | The rolls $(a, 5)$ have totals 6 to 9, which add to 30. | correct | B:screens[6] |
| l27-given-the-total.json | `.screens[6].widget.lines[4].text` | So $E[\text{total} \mid \max = 5] = \tfrac{70}{9} \approx 7.7778$. | correct | B:screens[6] |
| l27-given-the-total.json | `.screens[6].widget.lines[5].text` | Each die is uniform on 1 to 5, so the expected total is 6. | correct | B:screens[6] |
| l27-given-the-total.json | `.screens[6].widget.lines[5].why` | The condition is not "both at most 5". One die must be a 5. | correct | B:screens[6] |
| l27-given-the-total.json | `.screens[6].hints[0].text` | List the rolls in the L first. | correct | B:screens[6] |
| l27-given-the-total.json | `.screens[6].hints[1].text` | Split the L into its row and its column, without counting (5, 5) twice. | correct | B:screens[6] |
| l27-given-the-total.json | `.screens[6].hints[2].text` | Rolls, count, two partial sums, mean. | correct | B:screens[6] |
| l27-given-the-total.json | `.screens[6].feedback.correct` | $\tfrac{70}{9} \approx 7.7778$. | correct | B:screens[6] |
| l27-given-the-total.json | `.screens[6].feedback.generic` | Not quite right. Begin by listing the rolls in the L. | correct | B:screens[6] |
| l27-given-the-total.json | `.screens[6].feedback.byKey.d1` | You treated both dice as uniform on 1 to 5. One of them is 5 for certain. | correct | B:screens[6] |
| l27-given-the-total.json | `.screens[6].feedback.byKey.left-out` | Every line except the uniform claim belongs. | correct | B:screens[6] |
| l27-given-the-total.json | `.screens[6].explain.text` | The row gives totals 6 to 10 (sum 40) and the column gives 6 to 9 (sum 30). Over nine rolls the mean is $\tfrac{70}{9} … | correct | B:screens[6] |
| l27-given-the-total.json | `.screens[7].prose` | Write `conditional(event, given, n_dice=2, faces=6)`. List every roll and keep those where `given(roll)` is true. Retur… | correct | B:screens[7] |
| l27-given-the-total.json | `.screens[7].widget.how` | Check runs 9 hidden tests, each an exact `Fraction`: five chances and four conditional means. One uses three dice and o… | correct | B:screens[7] |
| l27-given-the-total.json | `.screens[7].hints[0].text` | Filter first: `kept = [r for r in rolls if given(r)]`. | correct | B:screens[7] |
| l27-given-the-total.json | `.screens[7].hints[1].text` | Count inside `kept` only. | correct | B:screens[7] |
| l27-given-the-total.json | `.screens[7].hints[2].text` | `Fraction(count, len(kept))` for a chance; `Fraction(sum(f(r) for r in kept), len(kept))` for a mean. | correct | B:screens[7] |
| l27-given-the-total.json | `.screens[7].feedback.correct` | Filter, then count: the reduced sample space in code. | correct | B:screens[7] |
| l27-given-the-total.json | `.screens[7].feedback.generic` | Not quite right. Look at the first failing test. | correct | B:screens[7] |
| l27-given-the-total.json | `.screens[7].feedback.byKey.test-1` | Divide by the number of kept rolls, not by all 36. | correct | B:screens[7] |
| l27-given-the-total.json | `.screens[7].feedback.byKey.test-6` | Average `f` over the kept rolls only. | correct | B:screens[7] |
| l27-given-the-total.json | `.screens[7].explain.text` | The filter is the condition and the count is the event. With 36 or 216 rolls, enumeration is instant and exact. Ten-sid… | correct | B:screens[7] |
| l27-given-the-total.json | `.screens[8].prose` | Drill: about 3 minutes a puzzle, as interviews allow. Keep your own time and say each argument aloud. Give four decimal… | correct | B:screens[8] |
| l27-given-the-total.json | `.screens[8].hints[0].text` | List the rolls that meet each condition. | correct | B:screens[8] |
| l27-given-the-total.json | `.screens[8].hints[1].text` | Total 6: five rolls. Larger 6: eleven rolls. Three dice total 5: six rolls. | correct | B:screens[8] |
| l27-given-the-total.json | `.screens[8].hints[2].text` | $\tfrac25$; then $\tfrac{21 + 15}{11}$; then (1, 1, 3) in three orders out of six. | correct | B:screens[8] |
| l27-given-the-total.json | `.screens[8].feedback.correct` | $\tfrac25 = 0.4$, $\tfrac{36}{11} \approx 3.2727$ and $\tfrac12$. | correct | B:screens[8] |
| l27-given-the-total.json | `.screens[8].feedback.generic` | Not quite right. Check the first answer that is marked. | correct | B:screens[8] |
| l27-given-the-total.json | `.screens[8].feedback.byKey.r0c1` | Check the first: (1, 5) and (5, 1) of five rolls. | correct | B:screens[8] |
| l27-given-the-total.json | `.screens[8].feedback.byKey.r1c1` | Check the second: the smaller dice are 1 to 6 in row 6 and 1 to 5 in column 6. | correct | B:screens[8] |
| l27-given-the-total.json | `.screens[8].feedback.byKey.r2c1` | Check the third: (1, 1, 3) and (1, 2, 2) each come in three orders. | correct | B:screens[8] |
| l27-given-the-total.json | `.screens[8].explain.text` | Total 6 leaves five rolls, two with a 1. Larger 6 leaves eleven rolls whose smaller dice add to 36. Three dice total 5 … | correct | B:screens[8] |
| l27-given-the-total.json | `.screens[9].prose` | One more at the same pace. Two dice total 7. | correct | B:screens[9] |
| l27-given-the-total.json | `.screens[9].widget.options[0].text` | $\tfrac13$ | correct | B:screens[9] |
| l27-given-the-total.json | `.screens[9].widget.options[1].why` | That is the chance of a six with no condition. The total of 7 changes it. | correct | B:screens[9] |
| l27-given-the-total.json | `.screens[9].widget.options[2].why` | You kept one die uniform. Either die can be the six, and the condition reshapes both. | correct | B:screens[9] |
| l27-given-the-total.json | `.screens[9].widget.options[3].why` | You split "a six" and "no six" as if equally likely. Count the six rolls. | correct | B:screens[9] |
| l27-given-the-total.json | `.screens[9].hints[0].text` | List the rolls with total 7. | correct | B:screens[9] |
| l27-given-the-total.json | `.screens[9].hints[1].text` | There are six: (1, 6) to (6, 1). | correct | B:screens[9] |
| l27-given-the-total.json | `.screens[9].hints[2].text` | Two of them hold a six. | correct | B:screens[9] |
| l27-given-the-total.json | `.screens[9].feedback.correct` | $\tfrac26 = \tfrac13$. | correct | B:screens[9] |
| l27-given-the-total.json | `.screens[9].feedback.generic` | Not quite right. Count the rolls with total 7 that include a six. | correct | B:screens[9] |
| l27-given-the-total.json | `.screens[9].feedback.byKey.b` | You used the chance before the condition. | correct | B:screens[9] |
| l27-given-the-total.json | `.screens[9].feedback.byKey.c` | You treated one die as still fair. Count the six rolls instead. | correct | B:screens[9] |
| l27-given-the-total.json | `.screens[9].explain.text` | Six rolls total 7, and (1, 6) and (6, 1) hold a six. So the chance is $\tfrac13$, a little above $\tfrac{11}{36}$. | correct | B:screens[9] |
| l27-given-the-total.json | `.screens[10].prose` | The interviewer extends it: two fair $n$-sided dice total $n + 1$. What is the expected larger die? Work out two cases,… | correct | B:screens[10] |
| l27-given-the-total.json | `.screens[10].hints[0].text` | Total $n + 1$ gives the rolls $(a, n + 1 - a)$ for $a = 1$ to $n$. | correct | B:screens[10] |
| l27-given-the-total.json | `.screens[10].hints[1].text` | For $n = 6$ the larger dice are 6, 5, 4, 4, 5, 6. | correct | B:screens[10] |
| l27-given-the-total.json | `.screens[10].hints[2].text` | Each value from $\tfrac{n}{2} + 1$ to $n$ appears twice, so the mean is $\tfrac{3n + 2}{4}$ for even $n$. | correct | B:screens[10] |
| l27-given-the-total.json | `.screens[10].feedback.correct` | 5, 8 and 75.5: the mean is $\tfrac{3n + 2}{4}$ for even $n$. | correct | B:screens[10] |
| l27-given-the-total.json | `.screens[10].feedback.generic` | Not quite right. Check the first answer that is marked. | correct | B:screens[10] |
| l27-given-the-total.json | `.screens[10].feedback.byKey.r0c1` | Check six-sided dice: average 6, 5, 4, 4, 5, 6. | correct | B:screens[10] |
| l27-given-the-total.json | `.screens[10].feedback.byKey.r1c1` | Check ten-sided dice: average 10, 9, 8, 7, 6, 6, 7, 8, 9, 10. | correct | B:screens[10] |
| l27-given-the-total.json | `.screens[10].feedback.byKey.r2c1` | Check the pattern: the values 51 to 100, each twice. | correct | B:screens[10] |
| l27-given-the-total.json | `.screens[10].explain.text` | The larger die runs over the top half of the faces, each value twice. Its mean is the middle of $\tfrac{n}{2} + 1$ and … | correct | B:screens[10] |
| l27-given-the-total.json | `.screens[11].prose` | A strategy's daily P&L is one of $-2, -1, 0, +1$ or $+2$, in £k. Each is equally likely, independently of other days. I… | correct | B:screens[11] |
| l27-given-the-total.json | `.screens[11].widget.accept` | 1/2 = 0.5 | correct | B:screens[11] |
| l27-given-the-total.json | `.screens[11].hints[0].text` | Shade the cells with total +1. | correct | B:screens[11] |
| l27-given-the-total.json | `.screens[11].hints[1].text` | They are (−1, +2), (0, +1), (+1, 0) and (+2, −1). | correct | B:screens[11] |
| l27-given-the-total.json | `.screens[11].hints[2].text` | Two of the four include a losing day. | correct | B:screens[11] |
| l27-given-the-total.json | `.screens[11].feedback.correct` | $\tfrac24 = 0.5$. | correct | B:screens[11] |
| l27-given-the-total.json | `.screens[11].feedback.generic` | Not quite right. Count inside the four cells with total +1. | correct | B:screens[11] |
| l27-given-the-total.json | `.screens[11].feedback.byKey.unconditional` | That is the chance with no condition, $1 - (\tfrac35)^2$. | correct | B:screens[11] |
| l27-given-the-total.json | `.screens[11].feedback.byKey.none` | A positive total does not rule out a loss: (−1, +2) is possible. | correct | B:screens[11] |
| l27-given-the-total.json | `.screens[11].explain.text` | Four day pairs total $+1$, and two of them hold a losing day. So the chance is $\tfrac12$, below the unconditional 0.64… | correct | B:screens[11] |
| l27-given-the-total.json | `.summary.ideas[0]` | A condition keeps only the outcomes that agree with it, and those keep equal chances. | correct | B:summary |
| l27-given-the-total.json | `.summary.ideas[1]` | Count the event inside the condition, or average the quantity over it. | correct | B:summary |
| l27-given-the-total.json | `.summary.ideas[2]` | After conditioning on a total or a maximum, the dice are no longer independent or uniform. | imprecise | finding 3: given a total each die stays uniform on its feasible range (exactly uniform on 1..6 for total 7); only given the maximum is the other die non-uniform; sim: puzzles-L5-concepts-r2.py:EXPECTED_FAIL given total 7 each die is still uniform on 1..6 |
| l27-given-the-total.json | `.summary.formula.note` | Ordered rolls: (2, 6) and (6, 2) are two outcomes; (4, 4) is one. | correct | B:summary |
| l27-given-the-total.json | `.summary.trap` | Treating the other die as still fair. Given the larger die is 5, both are 5 with chance $\tfrac19$, not $\tfrac16$. | correct | B:summary |
| l27-given-the-total.json | `.quiz[0].prose` | Two cards are drawn from a shuffled deck. You learn they are the same colour. | correct | B:quiz[0] |
| l27-given-the-total.json | `.quiz[0].widget.accept` | 78/650 = 3/25 = 0.12 | correct | B:quiz[0] |
| l27-given-the-total.json | `.quiz[0].feedback.correct` | $\tfrac{78}{650} = 0.12$. | correct | B:quiz[0] |
| l27-given-the-total.json | `.quiz[0].feedback.generic` | Not quite right. Count the same-colour pairs, then the heart pairs among them. | correct | B:quiz[0] |
| l27-given-the-total.json | `.quiz[0].feedback.byKey.unconditional` | That is the chance before the condition, $\tfrac{78}{1326}$. | correct | B:quiz[0] |
| l27-given-the-total.json | `.quiz[0].feedback.byKey.half` | You took $\tfrac12 \times \tfrac12$ for two hearts among red pairs. Red pairs are only half the same-colour pairs. | correct | B:quiz[0] |
| l27-given-the-total.json | `.quiz[0].explain.text` | There are $2\binom{26}{2} = 650$ same-colour pairs and $\binom{13}{2} = 78$ heart pairs. So the chance is $\tfrac{78}{6… | correct | B:quiz[0] |
| l27-given-the-total.json | `.quiz[1].prose` | Two dice total 8. | correct | B:quiz[1] |
| l27-given-the-total.json | `.quiz[1].widget.accept` | 1/5 = 0.2 | correct | B:quiz[1] |
| l27-given-the-total.json | `.quiz[1].feedback.correct` | $\tfrac15$: only (4, 4). | correct | B:quiz[1] |
| l27-given-the-total.json | `.quiz[1].feedback.generic` | Not quite right. Count the five rolls that total 8. | correct | B:quiz[1] |
| l27-given-the-total.json | `.quiz[1].feedback.byKey.unconditional` | That is the chance of a double with no condition. | correct | B:quiz[1] |
| l27-given-the-total.json | `.quiz[1].feedback.byKey.unordered` | You counted {2, 6}, {3, 5} and {4, 4} once each. There are five ordered rolls. | correct | B:quiz[1] |
| l27-given-the-total.json | `.quiz[1].explain.text` | Five rolls total 8, and only (4, 4) is a double. So the chance is $\tfrac15$. | correct | B:quiz[1] |
| l27-given-the-total.json | `.quiz[2].prose` | Two dice total 9. | correct | B:quiz[2] |
| l27-given-the-total.json | `.quiz[2].widget.accept` | 9/2 = 4.5 | correct | B:quiz[2] |
| l27-given-the-total.json | `.quiz[2].feedback.correct` | $\tfrac92 = 4.5$. | correct | B:quiz[2] |
| l27-given-the-total.json | `.quiz[2].feedback.generic` | Not quite right. By symmetry, the two dice share the total. | correct | B:quiz[2] |
| l27-given-the-total.json | `.quiz[2].feedback.byKey.unconditional` | That is the mean with no condition. A total of 9 pushes both dice up. | correct | B:quiz[2] |
| l27-given-the-total.json | `.quiz[2].explain.text` | The rolls (3, 6), (4, 5), (5, 4) and (6, 3) total 9. By symmetry each die averages half the total, $\tfrac92$. | correct | B:quiz[2] |

## l28-duels.json

### Bases

| key | basis |
|---|---|
| screens[0] | Ross, A First Course in Probability ch. 3 (conditioning on the first trial); derivation x = p + (1-p)(1-q)x; sim: puzzles-L5-concepts-r2.py:duels 1/2, 4/7, 2/3, 3/7, 1; 10/19; the first move is an asset: x > p/(p+q) |
| screens[5] | Ross, A First Course in Probability ch. 3 (conditioning on the first trial); derivation x = p + (1-p)(1-q)x; sim: puzzles-L5-concepts-r2.py:duels 1/2, 4/7, 2/3, 3/7, 1; 10/19; the first move is an asset: x > p/(p+q) |
| screens[6] | Ross, A First Course in Probability ch. 3 (conditioning on the first trial); derivation x = p + (1-p)(1-q)x; sim: puzzles-L5-concepts-r2.py:duels 1/2, 4/7, 2/3, 3/7, 1; 10/19; the first move is an asset: x > p/(p+q) |
| screens[8] | Ross, A First Course in Probability ch. 3 (conditioning on the first trial); derivation x = p + (1-p)(1-q)x; sim: puzzles-L5-concepts-r2.py:duels 1/2, 4/7, 2/3, 3/7, 1; 10/19; the first move is an asset: x > p/(p+q) |
| summary | Ross, A First Course in Probability ch. 3 (conditioning on the first trial); derivation x = p + (1-p)(1-q)x; sim: puzzles-L5-concepts-r2.py:duels 1/2, 4/7, 2/3, 3/7, 1; 10/19; the first move is an asset: x > p/(p+q) |
| quiz[0] | Ross, A First Course in Probability ch. 3 (conditioning on the first trial); derivation x = p + (1-p)(1-q)x; sim: puzzles-L5-concepts-r2.py:duels 1/2, 4/7, 2/3, 3/7, 1; 10/19; the first move is an asset: x > p/(p+q) |
| screens[1] | sympy: sim: puzzles-L5-concepts-r2.py:the duel is even when q = p/(1-p); q = 1/3 at p = 1/4; at q=1/4 A has 4/7; at q=1/2 B is the favourite |
| screens[2] | Mosteller, Fifty Challenging Problems, no. 20 (three-cornered duel) and no. 25 (random chord) (three-cornered duel, shooting order A, B, C, deliberate miss allowed); sim: puzzles-L5-concepts-r2.py:independent equilibrium solver: A air 25/63, 8/21, 2/9; aims at C 59/189; at B 50/189; air is A's best move; B->C and C->B are best responses; MC truel |
| screens[3] | Mosteller, Fifty Challenging Problems, no. 20 (three-cornered duel) and no. 25 (random chord) (three-cornered duel, shooting order A, B, C, deliberate miss allowed); sim: puzzles-L5-concepts-r2.py:independent equilibrium solver: A air 25/63, 8/21, 2/9; aims at C 59/189; at B 50/189; air is A's best move; B->C and C->B are best responses; MC truel |
| screens[4] | Mosteller, Fifty Challenging Problems, no. 20 (three-cornered duel) and no. 25 (random chord) (three-cornered duel, shooting order A, B, C, deliberate miss allowed); sim: puzzles-L5-concepts-r2.py:independent equilibrium solver: A air 25/63, 8/21, 2/9; aims at C 59/189; at B 50/189; air is A's best move; B->C and C->B are best responses; MC truel |
| screens[9] | Mosteller, Fifty Challenging Problems, no. 20 (three-cornered duel) and no. 25 (random chord) (three-cornered duel, shooting order A, B, C, deliberate miss allowed); sim: puzzles-L5-concepts-r2.py:independent equilibrium solver: A air 25/63, 8/21, 2/9; aims at C 59/189; at B 50/189; air is A's best move; B->C and C->B are best responses; MC truel |
| screens[11] | Mosteller, Fifty Challenging Problems, no. 20 (three-cornered duel) and no. 25 (random chord) (three-cornered duel, shooting order A, B, C, deliberate miss allowed); sim: puzzles-L5-concepts-r2.py:independent equilibrium solver: A air 25/63, 8/21, 2/9; aims at C 59/189; at B 50/189; air is A's best move; B->C and C->B are best responses; MC truel |
| quiz[2] | Mosteller, Fifty Challenging Problems, no. 20 (three-cornered duel) and no. 25 (random chord) (three-cornered duel, shooting order A, B, C, deliberate miss allowed); sim: puzzles-L5-concepts-r2.py:independent equilibrium solver: A air 25/63, 8/21, 2/9; aims at C 59/189; at B 50/189; air is A's best move; B->C and C->B are best responses; MC truel |
| screens[7] | sim: puzzles-L5-concepts-r2.py:solution passes all 8 hidden tests; with p_C = 0.9 A's chance is 165/406 |
| screens[10] | sim: puzzles-L5-concepts-r2.py:A at 1/2: air 17/30 beats aiming at C 23/60 |
| quiz[1] | sim: puzzles-L5-concepts-r2.py:(2/3) x duel(1/2, 1/3) = 1/2 |

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l28-duels.json | `.screens[0].prose` | Two players take turns to shoot, A first, until one is hit. A hits with chance $\tfrac13$ and B with $\tfrac12$. | correct | B:screens[0] |
| l28-duels.json | `.screens[0].widget.accept` | 1/2 = 0.5 | correct | B:screens[0] |
| l28-duels.json | `.screens[0].hints[0].text` | Let $x = P(\text{A wins})$ from A's turn. | correct | B:screens[0] |
| l28-duels.json | `.screens[0].hints[1].text` | A wins at once with $\tfrac13$. Both miss with $\tfrac23 \times \tfrac12 = \tfrac13$, and the duel restarts. | correct | B:screens[0] |
| l28-duels.json | `.screens[0].hints[2].text` | $x = \tfrac13 + \tfrac13 x$, so $x = \tfrac12$. | correct | B:screens[0] |
| l28-duels.json | `.screens[0].feedback.correct` | $x = \tfrac12$: firing first cancels the gap in skill. | correct | B:screens[0] |
| l28-duels.json | `.screens[0].feedback.generic` | Not quite right. Write one equation for a round: A hits, or both miss and it restarts. | correct | B:screens[0] |
| l28-duels.json | `.screens[0].feedback.byKey.first-shot` | That is A's first shot only. If both miss, A fires again. | correct | B:screens[0] |
| l28-duels.json | `.screens[0].feedback.byKey.ratio` | You split it as $\tfrac{p}{p + q}$. That ignores who fires first. | correct | B:screens[0] |
| l28-duels.json | `.screens[0].feedback.byKey.b` | You used B's miss alone, $\tfrac12$, as the restart chance. Both must miss: $\tfrac23 \times \tfrac12 = \tfrac13$. | correct | B:screens[0] |
| l28-duels.json | `.screens[0].explain.text` | A wins now with $\tfrac13$, or both miss with $\tfrac13$ and we are back at the start. So $x = \tfrac13 + \tfrac13 x$ a… | correct | B:screens[0] |
| l28-duels.json | `.screens[1].prose` | Now A hits with $\tfrac14$ and still fires first. Slide B's accuracy $q$ and watch A's chance on the curve. | correct | B:screens[1] |
| l28-duels.json | `.screens[1].hints[0].text` | Set $\tfrac{p}{1 - (1 - p)(1 - q)} = \tfrac12$ with $p = \tfrac14$. | correct | B:screens[1] |
| l28-duels.json | `.screens[1].hints[1].text` | That gives $2p = p + q - pq$, so $q = \tfrac{p}{1 - p}$. | correct | B:screens[1] |
| l28-duels.json | `.screens[1].hints[2].text` | $q = \tfrac{1/4}{3/4} = \tfrac13$. | correct | B:screens[1] |
| l28-duels.json | `.screens[1].feedback.correct` | $q = \tfrac13$: B must be a third better than A to break even. | correct | B:screens[1] |
| l28-duels.json | `.screens[1].feedback.generic` | Not quite right. Move $q$ until the caption reads 0.500. | correct | B:screens[1] |
| l28-duels.json | `.screens[1].feedback.byKey.quarter` | Equal skill favours the shooter who fires first: at $q = \tfrac14$, A wins with $\tfrac47$. | correct | B:screens[1] |
| l28-duels.json | `.screens[1].feedback.byKey.half` | At $q = \tfrac12$ B is the favourite. The even point is lower. | correct | B:screens[1] |
| l28-duels.json | `.screens[1].explain.text` | The duel is even when $q = \tfrac{p}{1 - p}$, here $\tfrac13$. Below that, A's first shot is worth more than B's extra … | correct | B:screens[1] |
| l28-duels.json | `.screens[2].prose` | A third player joins. A hits with $\tfrac13$, B with $\tfrac23$, and C never misses. They fire in turn A, B, C. B and C… | correct | B:screens[2] |
| l28-duels.json | `.screens[2].widget.accept` | 25/63, about 0.3968 | correct | B:screens[2] |
| l28-duels.json | `.screens[2].hints[0].text` | Value each end state for A first. | correct | B:screens[2] |
| l28-duels.json | `.screens[2].hints[1].text` | A wins the duel against B, firing first, with $\tfrac{1/3}{1 - \frac23 \cdot \frac13} = \tfrac37$. A wins a single shot… | correct | B:screens[2] |
| l28-duels.json | `.screens[2].hints[2].text` | $\tfrac23 \times \tfrac37 + \tfrac13 \times \tfrac13$. | correct | B:screens[2] |
| l28-duels.json | `.screens[2].feedback.correct` | $\tfrac27 + \tfrac19 = \tfrac{25}{63} \approx 0.3968$. | correct | B:screens[2] |
| l28-duels.json | `.screens[2].feedback.generic` | Not quite right. Weight the two end states by their chances. | correct | B:screens[2] |
| l28-duels.json | `.screens[2].feedback.byKey.one-shot` | That is only the branch where C survives B. B hits C two times in three. | correct | B:screens[2] |
| l28-duels.json | `.screens[2].feedback.byKey.duel-only` | That is the duel against B alone. B misses C a third of the time. | correct | B:screens[2] |
| l28-duels.json | `.screens[2].feedback.byKey.half-tree` | You dropped the branch where B misses, C kills B and A gets one shot. | correct | B:screens[2] |
| l28-duels.json | `.screens[2].explain.text` | B kills C with $\tfrac23$, leaving A to fire first against B: $\tfrac37$. Otherwise C kills B, and A has one shot at C:… | correct | B:screens[2] |
| l28-duels.json | `.screens[3].prose` | Same truel. Now A's first shot aims at C. If it hits, A faces B, and B fires first. If it misses, we are in the positio… | correct | B:screens[3] |
| l28-duels.json | `.screens[3].widget.accept` | 59/189, about 0.3122 | correct | B:screens[3] |
| l28-duels.json | `.screens[3].hints[0].text` | Value the duel where B fires first. | correct | B:screens[3] |
| l28-duels.json | `.screens[3].hints[1].text` | B hits first with $\tfrac23$. Otherwise A fires first against B, worth $\tfrac37$: $\tfrac13 \times \tfrac37 = \tfrac17… | correct | B:screens[3] |
| l28-duels.json | `.screens[3].hints[2].text` | $\tfrac13 \times \tfrac17 + \tfrac23 \times \tfrac{25}{63}$. | correct | B:screens[3] |
| l28-duels.json | `.screens[3].feedback.correct` | $\tfrac{1}{21} + \tfrac{50}{189} = \tfrac{59}{189} \approx 0.3122$. | correct | B:screens[3] |
| l28-duels.json | `.screens[3].feedback.generic` | Not quite right. Value the hit branch, then weight both branches. | correct | B:screens[3] |
| l28-duels.json | `.screens[3].feedback.byKey.a-first` | You let A fire first after killing C. The turn passes to B. | correct | B:screens[3] |
| l28-duels.json | `.screens[3].feedback.byKey.hit-only` | That is only the hit branch. Add the miss branch, worth $\tfrac{25}{63}$. | correct | B:screens[3] |
| l28-duels.json | `.screens[3].feedback.byKey.air` | That is the miss branch alone. Hitting C changes it. | correct | B:screens[3] |
| l28-duels.json | `.screens[3].explain.text` | Hitting C hands B the first shot in a duel A wins only $\tfrac17$ of the time. So aiming at C gives $\tfrac13 \cdot \tf… | correct | B:screens[3] |
| l28-duels.json | `.screens[4].prose` | Trading firms ask this one, and most candidates answer at once: shoot the best shooter. A has three first moves: aim at… | correct | B:screens[4] |
| l28-duels.json | `.screens[4].widget.options[0].text` | Fire into the air | correct | B:screens[4] |
| l28-duels.json | `.screens[4].widget.options[1].why` | Hitting C leaves A facing B with B firing first. That branch is worth only $\tfrac17$, so aiming at C gives $\tfrac{59}… | correct | B:screens[4] |
| l28-duels.json | `.screens[4].widget.options[2].why` | If A hits B, C fires next and never misses. A dies. | correct | B:screens[4] |
| l28-duels.json | `.screens[4].hints[0].text` | Value each move with the numbers you have. | correct | B:screens[4] |
| l28-duels.json | `.screens[4].hints[1].text` | Into the air is the miss branch, $\tfrac{25}{63}$. | correct | B:screens[4] |
| l28-duels.json | `.screens[4].hints[2].text` | Aim at C: $\tfrac{59}{189}$. Aim at B: $\tfrac23 \times \tfrac{25}{63} = \tfrac{50}{189}$. | correct | B:screens[4] |
| l28-duels.json | `.screens[4].feedback.correct` | Into the air: $\tfrac{25}{63} = \tfrac{75}{189}$ beats $\tfrac{59}{189}$ and $\tfrac{50}{189}$. | correct | B:screens[4] |
| l28-duels.json | `.screens[4].feedback.generic` | Not quite right. Compare the three values. | correct | B:screens[4] |
| l28-duels.json | `.screens[4].feedback.byKey.b` | You shot the best shooter. A hit hands B the first shot at you, so a miss is better for A. | correct | B:screens[4] |
| l28-duels.json | `.screens[4].explain.text` | Firing into the air is worth $\tfrac{75}{189}$, aiming at C $\tfrac{59}{189}$ and aiming at B $\tfrac{50}{189}$. A does… | correct | B:screens[4] |
| l28-duels.json | `.screens[5].prose` | Each answer conditioned on one round and valued the positions it leads to. In a duel where A hits with $p$, B with $q$,… | correct | B:screens[5] |
| l28-duels.json | `.screens[5].widget.options[0].text` | 1 | correct | B:screens[5] |
| l28-duels.json | `.screens[5].widget.options[1].why` | You used the alternating formula for equal shooters. Here $p = 1$: the first shot ends it. | correct | B:screens[5] |
| l28-duels.json | `.screens[5].widget.options[2].why` | B never gets to fire. A hits at once. | correct | B:screens[5] |
| l28-duels.json | `.screens[5].hints[0].text` | Put $p = 1$ into the formula. | correct | B:screens[5] |
| l28-duels.json | `.screens[5].hints[1].text` | The denominator is $1 - 0 = 1$. | correct | B:screens[5] |
| l28-duels.json | `.screens[5].hints[2].text` | $x = 1$. | correct | B:screens[5] |
| l28-duels.json | `.screens[5].feedback.correct` | 1: a perfect shooter who fires first wins at once. | correct | B:screens[5] |
| l28-duels.json | `.screens[5].feedback.generic` | Not quite right. Substitute $p = 1$. | correct | B:screens[5] |
| l28-duels.json | `.screens[5].explain.text` | With $p = 1$ the formula gives $\tfrac11 = 1$. This is the edge case: the first shot settles the duel, so skill after i… | correct | B:screens[5] |
| l28-duels.json | `.screens[6].prose` | Derive A's chance $x$ in a duel, A first, one justified line at a time. | correct | B:screens[6] |
| l28-duels.json | `.screens[6].widget.lines[0].text` | Look at one round, from A's turn. | correct | B:screens[6] |
| l28-duels.json | `.screens[6].widget.lines[1].text` | A hits at once with chance $p$. | correct | B:screens[6] |
| l28-duels.json | `.screens[6].widget.lines[2].text` | Both miss with chance $(1 - p)(1 - q)$, and the duel starts again. | correct | B:screens[6] |
| l28-duels.json | `.screens[6].widget.lines[3].text` | So $x = p + (1 - p)(1 - q)\,x$. | correct | B:screens[6] |
| l28-duels.json | `.screens[6].widget.lines[4].text` | So $x = \dfrac{p}{1 - (1 - p)(1 - q)}$, which is $\tfrac12$ at $p = \tfrac13$, $q = \tfrac12$. | correct | B:screens[6] |
| l28-duels.json | `.screens[6].widget.lines[5].text` | Each round, A wins with $p$ and B with $q$, so $x = \tfrac{p}{p + q}$. | correct | B:screens[6] |
| l28-duels.json | `.screens[6].widget.lines[5].why` | B only fires if A misses, so B wins a round with $(1 - p)q$, not $q$. | correct | B:screens[6] |
| l28-duels.json | `.screens[6].hints[0].text` | Start from one round. | correct | B:screens[6] |
| l28-duels.json | `.screens[6].hints[1].text` | A round ends with A hitting, or it restarts. | correct | B:screens[6] |
| l28-duels.json | `.screens[6].hints[2].text` | Round, two cases, equation, answer. | correct | B:screens[6] |
| l28-duels.json | `.screens[6].feedback.correct` | One round, one equation, one answer. | correct | B:screens[6] |
| l28-duels.json | `.screens[6].feedback.generic` | Not quite right. Begin with the round and its cases. | correct | B:screens[6] |
| l28-duels.json | `.screens[6].feedback.byKey.d1` | You gave B a chance $q$ each round. B fires only after A misses. | correct | B:screens[6] |
| l28-duels.json | `.screens[6].feedback.byKey.left-out` | Every line except the ratio belongs. | correct | B:screens[6] |
| l28-duels.json | `.screens[6].explain.text` | A round either ends with A's hit, ends with B's hit, or restarts. Only the restart feeds back into $x$, giving one line… | correct | B:screens[6] |
| l28-duels.json | `.screens[7].prose` | Write `duel(p, q)`, A's exact chance with A first. Then write `truel_air(pa, pb, pc)`: A always fires into the air whil… | correct | B:screens[7] |
| l28-duels.json | `.screens[7].widget.how` | Check runs 8 hidden tests, all exact `Fraction`s. Four are duels. Three compare the three truel chances, one with $p_C … | correct | B:screens[7] |
| l28-duels.json | `.screens[7].hints[0].text` | Once B or C falls, A fires first in a duel: use `duel`. | correct | B:screens[7] |
| l28-duels.json | `.screens[7].hints[1].text` | A round ends with B hitting ($p_B$) or with B missing and C hitting ($(1 - p_B)p_C$). | correct | B:screens[7] |
| l28-duels.json | `.screens[7].hints[2].text` | Divide each branch by $1 - (1 - p_B)(1 - p_C)$, the chance the round ends. | correct | B:screens[7] |
| l28-duels.json | `.screens[7].feedback.correct` | The duel formula, and the truel built from it. | correct | B:screens[7] |
| l28-duels.json | `.screens[7].feedback.generic` | Not quite right. Look at the first failing test. | correct | B:screens[7] |
| l28-duels.json | `.screens[7].feedback.byKey.test-1` | Return `p / (1 - (1 - p) * (1 - q))` with `Fraction` inputs. | correct | B:screens[7] |
| l28-duels.json | `.screens[7].feedback.byKey.test-7` | When C can miss, the round may repeat. Divide by the chance that it ends. | correct | B:screens[7] |
| l28-duels.json | `.screens[7].explain.text` | After B or C falls, A fires first, so each branch is a call to `duel`. With C perfect the round always ends, giving $\t… | correct | B:screens[7] |
| l28-duels.json | `.screens[8].prose` | Drill: about 3 minutes a puzzle, as interviews allow. Keep your own time and say each argument aloud. A fires first in … | correct | B:screens[8] |
| l28-duels.json | `.screens[8].hints[0].text` | Use $x = \tfrac{p}{1 - (1 - p)(1 - q)}$. | correct | B:screens[8] |
| l28-duels.json | `.screens[8].hints[1].text` | The restart chances are $\tfrac{9}{16}$, $\tfrac14$ and $\tfrac29$. | correct | B:screens[8] |
| l28-duels.json | `.screens[8].hints[2].text` | $\tfrac{1/4}{7/16}$, $\tfrac{1/2}{3/4}$ and $\tfrac{1/3}{7/9}$. | correct | B:screens[8] |
| l28-duels.json | `.screens[8].feedback.correct` | $\tfrac47$, $\tfrac23$ and $\tfrac37$. | correct | B:screens[8] |
| l28-duels.json | `.screens[8].feedback.generic` | Not quite right. Check the first answer that is marked. | correct | B:screens[8] |
| l28-duels.json | `.screens[8].feedback.byKey.r0c1` | Check the first: both miss with $\tfrac{9}{16}$. | correct | B:screens[8] |
| l28-duels.json | `.screens[8].feedback.byKey.r1c1` | Check the second: both miss with $\tfrac14$. | correct | B:screens[8] |
| l28-duels.json | `.screens[8].feedback.byKey.r2c1` | Check the third: both miss with $\tfrac23 \times \tfrac13 = \tfrac29$. | correct | B:screens[8] |
| l28-duels.json | `.screens[8].explain.text` | $\tfrac{1/4}{7/16} = \tfrac47$ and $\tfrac{1/2}{3/4} = \tfrac23$. With A at $\tfrac13$ against $\tfrac23$, $\tfrac{1/3}… | correct | B:screens[8] |
| l28-duels.json | `.screens[9].prose` | One more at the same pace. The truel again: A hits with $\tfrac13$, B with $\tfrac23$, C never misses, and everyone pla… | correct | B:screens[9] |
| l28-duels.json | `.screens[9].widget.options[0].text` | A, the weakest shot | correct | B:screens[9] |
| l28-duels.json | `.screens[9].widget.options[1].why` | You picked the best shooter. C is the target of B, so C survives only $\tfrac29$ of the time. | correct | B:screens[9] |
| l28-duels.json | `.screens[9].widget.options[2].why` | B's chance is $\tfrac{8}{21} = \tfrac{24}{63}$, just below A's $\tfrac{25}{63}$. | correct | B:screens[9] |
| l28-duels.json | `.screens[9].widget.options[3].why` | The chances are $\tfrac{25}{63}$, $\tfrac{24}{63}$ and $\tfrac{14}{63}$. | correct | B:screens[9] |
| l28-duels.json | `.screens[9].hints[0].text` | A fires into the air, so use the values from that branch. | correct | B:screens[9] |
| l28-duels.json | `.screens[9].hints[1].text` | A has $\tfrac{25}{63}$. B survives only by hitting C and then winning the duel: $\tfrac23 \times \tfrac47$. | correct | B:screens[9] |
| l28-duels.json | `.screens[9].hints[2].text` | C survives only if B misses and A then misses: $\tfrac13 \times \tfrac23$. | correct | B:screens[9] |
| l28-duels.json | `.screens[9].feedback.correct` | A, with $\tfrac{25}{63}$. | correct | B:screens[9] |
| l28-duels.json | `.screens[9].feedback.generic` | Not quite right. Work out B and C from the air branch. | correct | B:screens[9] |
| l28-duels.json | `.screens[9].feedback.byKey.b` | You chose the perfect shot. Being the strongest makes C the first target. | correct | B:screens[9] |
| l28-duels.json | `.screens[9].explain.text` | A survives with $\tfrac{25}{63}$, B with $\tfrac{8}{21} = \tfrac{24}{63}$ and C with $\tfrac29 = \tfrac{14}{63}$. The t… | correct | B:screens[9] |
| l28-duels.json | `.screens[10].prose` | The interviewer extends it: A's accuracy rises to $\tfrac12$. B is still $\tfrac23$ and C never misses. Does firing int… | correct | B:screens[10] |
| l28-duels.json | `.screens[10].hints[0].text` | Redo both branches with $p_A = \tfrac12$. | correct | B:screens[10] |
| l28-duels.json | `.screens[10].hints[1].text` | A first against B: $\tfrac{1/2}{1 - \frac12 \cdot \frac13} = \tfrac35$. B first against A: $\tfrac13 \times \tfrac35 = … | correct | B:screens[10] |
| l28-duels.json | `.screens[10].hints[2].text` | Air: $\tfrac23 \cdot \tfrac35 + \tfrac13 \cdot \tfrac12$. At C: $\tfrac12 \cdot \tfrac15 + \tfrac12 \times \text{air}$. | correct | B:screens[10] |
| l28-duels.json | `.screens[10].feedback.correct` | Air $\tfrac{17}{30} \approx 0.5667$ beats aiming at C, $\tfrac{23}{60} \approx 0.3833$. | correct | B:screens[10] |
| l28-duels.json | `.screens[10].feedback.generic` | Not quite right. Check the first answer that is marked. | correct | B:screens[10] |
| l28-duels.json | `.screens[10].feedback.byKey.r0c1` | Check the air branch: B kills C with $\tfrac23$, then A fires first and wins with $\tfrac35$. | correct | B:screens[10] |
| l28-duels.json | `.screens[10].feedback.byKey.r1c1` | Check the hit branch: B fires first and A wins only $\tfrac15$. | correct | B:screens[10] |
| l28-duels.json | `.screens[10].explain.text` | Firing into the air gives $\tfrac25 + \tfrac16 = \tfrac{17}{30}$. Aiming at C gives $\tfrac{1}{10} + \tfrac{17}{60} = \… | correct | B:screens[10] |
| l28-duels.json | `.screens[11].prose` | Three firms sell the same product. B and C, the two largest, are cutting prices to knock each other out. A, the smalles… | correct | B:screens[11] |
| l28-duels.json | `.screens[11].widget.options[0].text` | Stay out and keep its margin while B and C fight | correct | B:screens[11] |
| l28-duels.json | `.screens[11].widget.options[1].why` | That is aiming at C. If it works, A faces B alone, and B moves first. | correct | B:screens[11] |
| l28-duels.json | `.screens[11].widget.options[2].why` | That is aiming at B. If B falls, A faces the leader alone. | correct | B:screens[11] |
| l28-duels.json | `.screens[11].widget.options[3].why` | Fighting both makes A the target, and the weakest loses a straight fight. | correct | B:screens[11] |
| l28-duels.json | `.screens[11].hints[0].text` | Map each move to the truel. | correct | B:screens[11] |
| l28-duels.json | `.screens[11].hints[1].text` | Staying out is firing into the air. | correct | B:screens[11] |
| l28-duels.json | `.screens[11].hints[2].text` | In the truel, the air was worth $\tfrac{25}{63}$ against $\tfrac{59}{189}$ for aiming at C. | correct | B:screens[11] |
| l28-duels.json | `.screens[11].feedback.correct` | Stay out: the weakest gains while the two strongest fight. | correct | B:screens[11] |
| l28-duels.json | `.screens[11].feedback.generic` | Not quite right. Ask which move is firing into the air. | correct | B:screens[11] |
| l28-duels.json | `.screens[11].feedback.byKey.b` | You attacked the leader. A win hands B the first move against a weakened A. | correct | B:screens[11] |
| l28-duels.json | `.screens[11].explain.text` | Staying out is firing into the air: B and C weaken each other, then A meets the survivor. In the model that is $\tfrac{… | correct | B:screens[11] |
| l28-duels.json | `.summary.ideas[0]` | Condition on one round: a duel restarts only when both miss, which gives one linear equation. | correct | B:summary |
| l28-duels.json | `.summary.ideas[1]` | Firing first is an asset: A at $\tfrac13$ breaks even against B at $\tfrac12$. | correct | B:summary |
| l28-duels.json | `.summary.ideas[2]` | In a truel the weakest player may do best by firing into the air while the two strongest fight. | correct | B:summary |
| l28-duels.json | `.summary.formula.note` | Even when $q = \tfrac{p}{1 - p}$. | correct | B:summary |
| l28-duels.json | `.summary.trap` | Shooting the best shooter: a hit hands the next rival the first shot at you. | correct | B:summary |
| l28-duels.json | `.quiz[0].prose` | A duel: A hits with $\tfrac25$, B with $\tfrac35$, and A fires first. | correct | B:quiz[0] |
| l28-duels.json | `.quiz[0].widget.accept` | 10/19, about 0.5263 | correct | B:quiz[0] |
| l28-duels.json | `.quiz[0].feedback.correct` | $\tfrac{2/5}{1 - \frac35 \cdot \frac25} = \tfrac{10}{19} \approx 0.5263$. | correct | B:quiz[0] |
| l28-duels.json | `.quiz[0].feedback.generic` | Not quite right. Both miss with $\tfrac35 \times \tfrac25 = \tfrac{6}{25}$. | correct | B:quiz[0] |
| l28-duels.json | `.quiz[0].feedback.byKey.ratio` | You used $\tfrac{p}{p + q}$ or the first shot alone. Firing first counts in every round. | correct | B:quiz[0] |
| l28-duels.json | `.quiz[0].explain.text` | A round restarts with chance $\tfrac{6}{25}$, so $x = \tfrac{2/5}{19/25} = \tfrac{10}{19}$. A is the weaker shot but th… | correct | B:quiz[0] |
| l28-duels.json | `.quiz[1].prose` | A hits with $\tfrac12$ and B with $\tfrac13$, but B fires first. | correct | B:quiz[1] |
| l28-duels.json | `.quiz[1].widget.accept` | 1/2 = 0.5 | correct | B:quiz[1] |
| l28-duels.json | `.quiz[1].feedback.correct` | $\tfrac23 \times \tfrac34 = \tfrac12$. | correct | B:quiz[1] |
| l28-duels.json | `.quiz[1].feedback.generic` | Not quite right. B misses first, then A fires first in the duel. | correct | B:quiz[1] |
| l28-duels.json | `.quiz[1].feedback.byKey.a-first` | That is the duel with A first. B shoots first here. | correct | B:quiz[1] |
| l28-duels.json | `.quiz[1].feedback.byKey.miss-only` | That is B's first miss alone. A must then win the duel. | correct | B:quiz[1] |
| l28-duels.json | `.quiz[1].explain.text` | B misses with $\tfrac23$, and then A fires first and wins with $\tfrac34$. So A's chance is $\tfrac12$. | correct | B:quiz[1] |
| l28-duels.json | `.quiz[2].prose` | The truel: A hits with $\tfrac13$, B with $\tfrac23$, C never misses. A fires into the air; B and C aim at each other. | correct | B:quiz[2] |
| l28-duels.json | `.quiz[2].widget.accept` | 8/21, about 0.3810 | correct | B:quiz[2] |
| l28-duels.json | `.quiz[2].feedback.correct` | $\tfrac23 \times \tfrac47 = \tfrac{8}{21} \approx 0.3810$. | correct | B:quiz[2] |
| l28-duels.json | `.quiz[2].feedback.generic` | Not quite right. B must hit C first, then win the duel with A firing first. | correct | B:quiz[2] |
| l28-duels.json | `.quiz[2].feedback.byKey.hit-only` | That is B hitting C. B must then survive A, who fires first. | correct | B:quiz[2] |
| l28-duels.json | `.quiz[2].feedback.byKey.duel` | That is B winning the duel. Multiply by B hitting C first. | correct | B:quiz[2] |
| l28-duels.json | `.quiz[2].explain.text` | B survives only by hitting C ($\tfrac23$) and then beating A, who fires first ($\tfrac47$). That gives $\tfrac{8}{21}$.… | correct | B:quiz[2] |

## l29-random-chords.json

### Bases

| key | basis |
|---|---|
| screens[0] | Grimmett and Stirzaker, Probability and Random Processes 4.13 problem 4 (Bertrand) and 1.4 (conditional probability); Mosteller, Fifty Challenging Problems, no. 20 (three-cornered duel) and no. 25 (random chord); sympy: sim: puzzles-L5-concepts-r2.py:endpoints 1/3, 1/2, 2/3; MC endpoints |
| quiz[1] | Grimmett and Stirzaker, Probability and Random Processes 4.13 problem 4 (Bertrand) and 1.4 (conditional probability); Mosteller, Fifty Challenging Problems, no. 20 (three-cornered duel) and no. 25 (random chord); sympy: sim: puzzles-L5-concepts-r2.py:endpoints 1/3, 1/2, 2/3; MC endpoints |
| screens[1] | Grimmett and Stirzaker, Probability and Random Processes 4.13 problem 4 (Bertrand) and 1.4 (conditional probability); sim: puzzles-L5-concepts-r2.py:radius 1/2; 0.7071; 0.866; MC radius |
| quiz[2] | Grimmett and Stirzaker, Probability and Random Processes 4.13 problem 4 (Bertrand) and 1.4 (conditional probability); sim: puzzles-L5-concepts-r2.py:radius 1/2; 0.7071; 0.866; MC radius |
| screens[2] | Grimmett and Stirzaker, Probability and Random Processes 4.13 problem 4 (Bertrand) and 1.4 (conditional probability) (Bertrand 1889); sim: puzzles-L5-concepts-r2.py:midpoint 1/4; uniform midpoint has P(d < r) = r^2; MC midpoint |
| screens[7] | Grimmett and Stirzaker, Probability and Random Processes 4.13 problem 4 (Bertrand) and 1.4 (conditional probability) (Bertrand 1889); sim: puzzles-L5-concepts-r2.py:midpoint 1/4; uniform midpoint has P(d < r) = r^2; MC midpoint |
| summary | Grimmett and Stirzaker, Probability and Random Processes 4.13 problem 4 (Bertrand) and 1.4 (conditional probability) (Bertrand 1889); sim: puzzles-L5-concepts-r2.py:midpoint 1/4; uniform midpoint has P(d < r) = r^2; MC midpoint |
| screens[3] | Bertrand's paradox: the answer depends on the selection method (Jaynes 1973 aside); sim: puzzles-L5-concepts-r2.py:average of the three 0.36 |
| screens[4] | two envelopes with a proper prior (e.g. Christensen and Utts 1992): condition on the amount seen; sim: puzzles-L5-concepts-r2.py:always keep = always switch = 22.5; seeing 20 worth 25; at 80 keep, at 40 switch for 50 |
| screens[5] | two envelopes with a proper prior (e.g. Christensen and Utts 1992): condition on the amount seen; sim: puzzles-L5-concepts-r2.py:always keep = always switch = 22.5; seeing 20 worth 25; at 80 keep, at 40 switch for 50 |
| screens[6] | two envelopes with a proper prior (e.g. Christensen and Utts 1992): condition on the amount seen; sim: puzzles-L5-concepts-r2.py:always keep = always switch = 22.5; seeing 20 worth 25; at 80 keep, at 40 switch for 50 |
| quiz[0] | two envelopes with a proper prior (e.g. Christensen and Utts 1992): condition on the amount seen; sim: puzzles-L5-concepts-r2.py:always keep = always switch = 22.5; seeing 20 worth 25; at 80 keep, at 40 switch for 50 |
| screens[8] | sim: puzzles-L5-concepts-r2.py:solution passes all 5 hidden tests; d = U in the midpoint branch gives 1/2 |
| screens[9] | sympy: sim: puzzles-L5-concepts-r2.py:expected lengths 4/pi, pi/2, 4/3; radius procedure has the smallest mean distance from the centre |
| screens[10] | sim: puzzles-L5-concepts-r2.py:sqrt2 threshold: endpoints 1/2, radius 0.7071, midpoint 1/2 |
| screens[11] | length-biased sampling; sim: puzzles-L5-concepts-r2.py:random day 40, random trade -230 |

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l29-random-chords.json | `.screens[0].prose` | Pick a chord of the unit circle by choosing two points on it at random. Fix the first at $P$; by symmetry that loses no… | correct | B:screens[0] |
| l29-random-chords.json | `.screens[0].widget.options[0].text` | $\tfrac13$ | correct | B:screens[0] |
| l29-random-chords.json | `.screens[0].widget.options[1].why` | You measured where the chord is shorter. It is longer only on the arc opposite $P$. | correct | B:screens[0] |
| l29-random-chords.json | `.screens[0].widget.options[2].why` | You split the circle in half. The long chords end on one arc of 120 degrees. | correct | B:screens[0] |
| l29-random-chords.json | `.screens[0].widget.options[3].why` | That belongs to a different way of drawing the chord. | correct | B:screens[0] |
| l29-random-chords.json | `.screens[0].hints[0].text` | Drag $Q$ until the chord is exactly a side of the triangle. | correct | B:screens[0] |
| l29-random-chords.json | `.screens[0].hints[1].text` | That happens at the two far corners, 120 degrees from $P$ each way. | correct | B:screens[0] |
| l29-random-chords.json | `.screens[0].hints[2].text` | The chord is longer while $Q$ is on the arc between them: 120 of 360 degrees. | correct | B:screens[0] |
| l29-random-chords.json | `.screens[0].feedback.correct` | $\tfrac13$: $Q$ must land on the far third of the circle. | correct | B:screens[0] |
| l29-random-chords.json | `.screens[0].feedback.generic` | Not quite right. Find where the chord equals a side, then measure the arc beyond. | correct | B:screens[0] |
| l29-random-chords.json | `.screens[0].explain.text` | The chord equals $\sqrt3$ when $Q$ is at a far corner of the triangle. It is longer when $Q$ lies on the arc between th… | correct | B:screens[0] |
| l29-random-chords.json | `.screens[1].prose` | A second procedure: pick a radius, then a point $M$ uniform along it. Draw the chord through $M$ at right angles to the… | correct | B:screens[1] |
| l29-random-chords.json | `.screens[1].widget.accept` | 1/2 = 0.5 | correct | B:screens[1] |
| l29-random-chords.json | `.screens[1].hints[0].text` | Find the distance $d$ at which the chord is exactly $\sqrt3$. | correct | B:screens[1] |
| l29-random-chords.json | `.screens[1].hints[1].text` | The chord is $2\sqrt{1 - d^2}$; it equals $\sqrt3$ at $d = \tfrac12$. | correct | B:screens[1] |
| l29-random-chords.json | `.screens[1].hints[2].text` | $M$ is uniform on $[0, 1]$, so $P(d < \tfrac12) = \tfrac12$. | correct | B:screens[1] |
| l29-random-chords.json | `.screens[1].feedback.correct` | $\tfrac12$: the chord is long when $M$ is in the inner half of the radius. | correct | B:screens[1] |
| l29-random-chords.json | `.screens[1].feedback.generic` | Not quite right. Find the cut-off distance, then the share of the radius inside it. | correct | B:screens[1] |
| l29-random-chords.json | `.screens[1].feedback.byKey.endpoints` | That is the two-endpoint answer. This procedure draws chords differently. | correct | B:screens[1] |
| l29-random-chords.json | `.screens[1].feedback.byKey.area` | That treats $M$ as uniform over the disc. Here $M$ is uniform along a radius. | correct | B:screens[1] |
| l29-random-chords.json | `.screens[1].feedback.byKey.half-chord` | You solved for the wrong cut-off. The chord is $\sqrt3$ at $d = \tfrac12$, not at $\tfrac{\sqrt3}{2}$. | correct | B:screens[1] |
| l29-random-chords.json | `.screens[1].explain.text` | By Pythagoras the chord at distance $d$ is $2\sqrt{1 - d^2}$, longer than $\sqrt3$ exactly when $d < \tfrac12$. With $M… | correct | B:screens[1] |
| l29-random-chords.json | `.screens[2].prose` | A third procedure: pick the chord's midpoint $M$ uniformly from the whole disc. The dashed circle has radius $\tfrac12$… | correct | B:screens[2] |
| l29-random-chords.json | `.screens[2].widget.accept` | 1/4 = 0.25 | correct | B:screens[2] |
| l29-random-chords.json | `.screens[2].hints[0].text` | The cut-off is the same as before: $d < \tfrac12$. | correct | B:screens[2] |
| l29-random-chords.json | `.screens[2].hints[1].text` | Now $M$ is uniform over the area of the disc. | correct | B:screens[2] |
| l29-random-chords.json | `.screens[2].hints[2].text` | The inner disc has $(\tfrac12)^2 = \tfrac14$ of the area. | correct | B:screens[2] |
| l29-random-chords.json | `.screens[2].feedback.correct` | $\tfrac14$: the inner disc holds a quarter of the area. | correct | B:screens[2] |
| l29-random-chords.json | `.screens[2].feedback.generic` | Not quite right. Compare the area of the dashed disc with the whole. | correct | B:screens[2] |
| l29-random-chords.json | `.screens[2].feedback.byKey.radius` | That is the radius answer. A uniform point in the disc is more often far out, where there is more area. | correct | B:screens[2] |
| l29-random-chords.json | `.screens[2].feedback.byKey.endpoints` | That is the two-endpoint answer. | correct | B:screens[2] |
| l29-random-chords.json | `.screens[2].explain.text` | The chord is long when its midpoint is inside the dashed circle. A uniform midpoint lands there with chance $\tfrac{\pi… | correct | B:screens[2] |
| l29-random-chords.json | `.screens[3].prose` | Banks and trading firms both ask it. A chord of a unit circle is chosen at random: what is the chance it is longer than… | correct | B:screens[3] |
| l29-random-chords.json | `.screens[3].widget.options[0].text` | Ask how the chord is drawn: endpoints give $\tfrac13$, a radius point $\tfrac12$, a midpoint $\tfrac14$ | correct | B:screens[3] |
| l29-random-chords.json | `.screens[3].widget.options[1].why` | Each procedure feels natural to someone. Without one, "random" has no single answer. | correct | B:screens[3] |
| l29-random-chords.json | `.screens[3].widget.options[2].why` | Picking the middle answer is a guess. Each answer belongs to its own procedure. | correct | B:screens[3] |
| l29-random-chords.json | `.screens[3].widget.options[3].why` | Averaging the procedures is a fourth procedure. Ask which one the interviewer means. | correct | B:screens[3] |
| l29-random-chords.json | `.screens[3].hints[0].text` | Recall the three screens you just did. | correct | B:screens[3] |
| l29-random-chords.json | `.screens[3].hints[1].text` | Each procedure gave a different answer. | correct | B:screens[3] |
| l29-random-chords.json | `.screens[3].hints[2].text` | So the question is not finished until the procedure is stated. | correct | B:screens[3] |
| l29-random-chords.json | `.screens[3].feedback.correct` | State the procedure, then answer it. | correct | B:screens[3] |
| l29-random-chords.json | `.screens[3].feedback.generic` | Not quite right. Which of the three procedures did the question name? | correct | B:screens[3] |
| l29-random-chords.json | `.screens[3].feedback.byKey.b` | You answered one procedure as if it were the only one. The interviewer wants to hear you ask. | correct | B:screens[3] |
| l29-random-chords.json | `.screens[3].explain.text` | The three procedures are all uniform in something, and they disagree. So the right first move is a question: how is the… | correct | B:screens[3] |
| l29-random-chords.json | `.screens[4].prose` | One envelope holds twice the other. The pair is (£10, £20) or (£20, £40), each equally likely, and you open one at rand… | correct | B:screens[4] |
| l29-random-chords.json | `.screens[4].hints[0].text` | Look down the "You see" column. | correct | B:screens[4] |
| l29-random-chords.json | `.screens[4].hints[1].text` | Two rows show £20. | correct | B:screens[4] |
| l29-random-chords.json | `.screens[4].hints[2].text` | Rows 2 and 3: one from each pair. | correct | B:screens[4] |
| l29-random-chords.json | `.screens[4].feedback.correct` | Two cases: the other holds £10 or £40, equally likely. | correct | B:screens[4] |
| l29-random-chords.json | `.screens[4].feedback.generic` | Not quite right. Tap the rows where you see £20. | correct | B:screens[4] |
| l29-random-chords.json | `.screens[4].feedback.byKey.pair` | You tapped a whole pair. In the £40 row you see £40, not £20. | correct | B:screens[4] |
| l29-random-chords.json | `.screens[4].explain.text` | Seeing £20 leaves two equally likely cases, so switching is worth $\tfrac{10 + 40}{2} = \text{£}25$. Here switching pay… | correct | B:screens[4] |
| l29-random-chords.json | `.screens[5].prose` | A candidate argues: whatever I see, call it $x$; the other holds $2x$ or $\tfrac{x}{2}$, worth $1.25x$. So always switc… | correct | B:screens[5] |
| l29-random-chords.json | `.screens[5].hints[0].text` | Average over all four rows. | correct | B:screens[5] |
| l29-random-chords.json | `.screens[5].hints[1].text` | Keeping gets the "You see" column; switching gets the "Other holds" column. | correct | B:screens[5] |
| l29-random-chords.json | `.screens[5].hints[2].text` | Both columns hold 10, 20, 20 and 40. | correct | B:screens[5] |
| l29-random-chords.json | `.screens[5].feedback.correct` | £22.50 each: always switching gains nothing. | correct | B:screens[5] |
| l29-random-chords.json | `.screens[5].feedback.generic` | Not quite right. Average each column over the four equally likely rows. | correct | B:screens[5] |
| l29-random-chords.json | `.screens[5].feedback.byKey.r0c1` | Check keeping: $\tfrac{10 + 20 + 20 + 40}{4}$. | correct | B:screens[5] |
| l29-random-chords.json | `.screens[5].feedback.byKey.r1c1` | Check switching: the other column holds the same four amounts. | correct | B:screens[5] |
| l29-random-chords.json | `.screens[5].explain.text` | Keeping and switching are each worth $\tfrac{10 + 20 + 20 + 40}{4} = \text{£}22.50$. The $1.25x$ argument treats $x$ as… | correct | B:screens[5] |
| l29-random-chords.json | `.screens[6].prose` | Before computing, ask how the random object is drawn. For a chord at distance $d$ from the centre, $$L = 2\sqrt{1 - d^2… | correct | B:screens[6] |
| l29-random-chords.json | `.screens[6].widget.options[0].text` | Keep: £80 can only be the larger amount | correct | B:screens[6] |
| l29-random-chords.json | `.screens[6].widget.options[1].why` | No pair holds £160, so the other envelope is £40 for certain. | correct | B:screens[6] |
| l29-random-chords.json | `.screens[6].widget.options[2].why` | It matters once you look. At £80 the other is £40. | correct | B:screens[6] |
| l29-random-chords.json | `.screens[6].hints[0].text` | Which pairs contain £80? | correct | B:screens[6] |
| l29-random-chords.json | `.screens[6].hints[1].text` | Only (£40, £80). | correct | B:screens[6] |
| l29-random-chords.json | `.screens[6].hints[2].text` | So the other envelope holds £40. | correct | B:screens[6] |
| l29-random-chords.json | `.screens[6].feedback.correct` | Keep: the largest amount ends the doubt. | correct | B:screens[6] |
| l29-random-chords.json | `.screens[6].feedback.generic` | Not quite right. List the pairs that hold £80. | correct | B:screens[6] |
| l29-random-chords.json | `.screens[6].explain.text` | The edge case: with a largest amount in the prior, seeing it means never switch. At £40 you would switch, for $\tfrac{2… | correct | B:screens[6] |
| l29-random-chords.json | `.screens[7].prose` | Derive the midpoint answer, one justified line at a time. | correct | B:screens[7] |
| l29-random-chords.json | `.screens[7].widget.lines[0].text` | A chord at distance $d$ from the centre has half-length $\sqrt{1 - d^2}$, by Pythagoras. | correct | B:screens[7] |
| l29-random-chords.json | `.screens[7].widget.lines[1].text` | So $L > \sqrt3 \iff 1 - d^2 > \tfrac34 \iff d < \tfrac12$. | correct | B:screens[7] |
| l29-random-chords.json | `.screens[7].widget.lines[2].text` | A uniform midpoint in the unit disc has $P(d < r) = r^2$, its share of the area. | correct | B:screens[7] |
| l29-random-chords.json | `.screens[7].widget.lines[3].text` | So the chance is $(\tfrac12)^2 = \tfrac14$. | correct | B:screens[7] |
| l29-random-chords.json | `.screens[7].widget.lines[4].text` | $d$ is uniform on $[0, 1]$, so $P(d < \tfrac12) = \tfrac12$. | correct | B:screens[7] |
| l29-random-chords.json | `.screens[7].widget.lines[4].why` | That is the radius procedure. A uniform point in the disc is more often far out: $P(d < r) = r^2$. | correct | B:screens[7] |
| l29-random-chords.json | `.screens[7].hints[0].text` | Start from the length of a chord. | correct | B:screens[7] |
| l29-random-chords.json | `.screens[7].hints[1].text` | Then turn the length condition into a distance condition. | correct | B:screens[7] |
| l29-random-chords.json | `.screens[7].hints[2].text` | Length, cut-off, area share, answer. | correct | B:screens[7] |
| l29-random-chords.json | `.screens[7].feedback.correct` | Length, cut-off, area, answer: $\tfrac14$. | correct | B:screens[7] |
| l29-random-chords.json | `.screens[7].feedback.generic` | Not quite right. Begin with the chord length. | correct | B:screens[7] |
| l29-random-chords.json | `.screens[7].feedback.byKey.d1` | You made $d$ uniform. That is the radius procedure, not the midpoint one. | correct | B:screens[7] |
| l29-random-chords.json | `.screens[7].feedback.byKey.left-out` | Every line except the uniform distance belongs. | correct | B:screens[7] |
| l29-random-chords.json | `.screens[7].explain.text` | The first two lines hold for every procedure. Only the third line, the law of $d$, depends on how the chord is drawn. T… | correct | B:screens[7] |
| l29-random-chords.json | `.screens[8].prose` | Write `chord_sim(method, trials, seed)` with `random.Random(seed)`. For `'endpoints'` draw two uniform angles; for `'ra… | correct | B:screens[8] |
| l29-random-chords.json | `.screens[8].widget.how` | Check runs 5 hidden tests. Tests 1 to 3 accept a share within three standard errors of $\tfrac13$, $\tfrac12$ and $\tfr… | correct | B:screens[8] |
| l29-random-chords.json | `.screens[8].hints[0].text` | Two angles $a, b$ give a chord of length $2\|\sin\tfrac{a - b}{2}\|$. | correct | B:screens[8] |
| l29-random-chords.json | `.screens[8].hints[1].text` | A distance $d$ from the centre gives $2\sqrt{1 - d^2}$. | correct | B:screens[8] |
| l29-random-chords.json | `.screens[8].hints[2].text` | A uniform point in the disc has $d = \sqrt{U}$ for $U$ uniform on $[0, 1]$. | correct | B:screens[8] |
| l29-random-chords.json | `.screens[8].feedback.correct` | Three procedures, three shares: $\tfrac13$, $\tfrac12$ and $\tfrac14$. | correct | B:screens[8] |
| l29-random-chords.json | `.screens[8].feedback.generic` | Not quite right. Look at the first failing test. | correct | B:screens[8] |
| l29-random-chords.json | `.screens[8].feedback.byKey.test-3` | The midpoint share is off. A uniform point in the disc needs $d = \sqrt{U}$, not $d = U$. | correct | B:screens[8] |
| l29-random-chords.json | `.screens[8].explain.text` | Each branch draws a chord by its own rule, then tests the same length. Drawing $d = U$ in the midpoint branch gives $\t… | correct | B:screens[8] |
| l29-random-chords.json | `.screens[9].prose` | Drill: about 3 minutes a puzzle, as interviews allow. Keep your own time and say each argument aloud. Find the expected… | correct | B:screens[9] |
| l29-random-chords.json | `.screens[9].hints[0].text` | Write the length in terms of the random quantity. | correct | B:screens[9] |
| l29-random-chords.json | `.screens[9].hints[1].text` | Endpoints: $2\sin\tfrac{\theta}{2}$, $\theta$ uniform on $[0, 2\pi]$. Radius: $2\sqrt{1 - d^2}$, $d$ uniform. Midpoint:… | correct | B:screens[9] |
| l29-random-chords.json | `.screens[9].hints[2].text` | $\tfrac{4}{\pi}$; then $2 \times \tfrac{\pi}{4}$; then $\int_0^1 2\sqrt{1 - d^2}\,2d\,dd = \tfrac43$. | correct | B:screens[9] |
| l29-random-chords.json | `.screens[9].feedback.correct` | $\tfrac4\pi \approx 1.2732$, $\tfrac\pi2 \approx 1.5708$ and $\tfrac43 \approx 1.3333$. | correct | B:screens[9] |
| l29-random-chords.json | `.screens[9].feedback.generic` | Not quite right. Check the first answer that is marked. | correct | B:screens[9] |
| l29-random-chords.json | `.screens[9].feedback.byKey.r0c1` | Check the endpoints: the mean of $2\sin\tfrac{\theta}{2}$ over $[0, 2\pi]$ is $\tfrac4\pi$. | correct | B:screens[9] |
| l29-random-chords.json | `.screens[9].feedback.byKey.r1c1` | Check the radius: $\int_0^1 \sqrt{1 - d^2}\,dd$ is a quarter circle, $\tfrac\pi4$. | correct | B:screens[9] |
| l29-random-chords.json | `.screens[9].feedback.byKey.r2c1` | Check the midpoint: weight $2\sqrt{1 - d^2}$ by the density $2d$. | correct | B:screens[9] |
| l29-random-chords.json | `.screens[9].explain.text` | The radius procedure favours chords near the centre, so its chords are longest on average. The three means are $\tfrac4… | correct | B:screens[9] |
| l29-random-chords.json | `.screens[10].prose` | The interviewer extends it: the same three procedures, now with the side of the inscribed square, $\sqrt2$, as the thre… | correct | B:screens[10] |
| l29-random-chords.json | `.screens[10].hints[0].text` | Redo the cut-off: $2\sqrt{1 - d^2} > \sqrt2$. | correct | B:screens[10] |
| l29-random-chords.json | `.screens[10].hints[1].text` | That is $d < \tfrac{1}{\sqrt2}$; for endpoints, a central angle above 90 degrees. | correct | B:screens[10] |
| l29-random-chords.json | `.screens[10].hints[2].text` | Endpoints: half the circle. Radius: $\tfrac{1}{\sqrt2}$. Midpoint: $(\tfrac{1}{\sqrt2})^2$. | correct | B:screens[10] |
| l29-random-chords.json | `.screens[10].feedback.correct` | $\tfrac12$, $\tfrac{1}{\sqrt2} \approx 0.7071$ and $\tfrac12$. | correct | B:screens[10] |
| l29-random-chords.json | `.screens[10].feedback.generic` | Not quite right. Check the first answer that is marked. | correct | B:screens[10] |
| l29-random-chords.json | `.screens[10].feedback.byKey.r0c1` | Check the endpoints: the chord beats $\sqrt2$ when the central angle is between 90 and 270 degrees. | correct | B:screens[10] |
| l29-random-chords.json | `.screens[10].feedback.byKey.r1c1` | Check the radius: $P(d < \tfrac{1}{\sqrt2})$ with $d$ uniform. | correct | B:screens[10] |
| l29-random-chords.json | `.screens[10].feedback.byKey.r2c1` | Check the midpoint: the area share is $d^2 = \tfrac12$. | correct | B:screens[10] |
| l29-random-chords.json | `.screens[10].explain.text` | The cut-off moves to $d < \tfrac{1}{\sqrt2}$. Endpoints and midpoints happen to agree at $\tfrac12$, while the radius g… | correct | B:screens[10] |
| l29-random-chords.json | `.screens[11].prose` | A backtest has 10 days. On 9 quiet days the strategy trades once and makes £100. On 1 busy day it trades 11 times and l… | correct | B:screens[11] |
| l29-random-chords.json | `.screens[11].hints[0].text` | The second rule weights each day by its trades. | correct | B:screens[11] |
| l29-random-chords.json | `.screens[11].hints[1].text` | There are 20 trades: 9 on quiet days and 11 on the busy day. | correct | B:screens[11] |
| l29-random-chords.json | `.screens[11].hints[2].text` | $\tfrac{9 \times 100 - 500}{10}$, then $\tfrac{9 \times 100 + 11 \times (-500)}{20}$. | correct | B:screens[11] |
| l29-random-chords.json | `.screens[11].feedback.correct` | £40 against −£230. | correct | B:screens[11] |
| l29-random-chords.json | `.screens[11].feedback.generic` | Not quite right. Check the first answer that is marked. | correct | B:screens[11] |
| l29-random-chords.json | `.screens[11].feedback.byKey.r0c1` | Check the first: each of the 10 days has weight $\tfrac{1}{10}$. | correct | B:screens[11] |
| l29-random-chords.json | `.screens[11].feedback.byKey.r1c1` | Check the second: the busy day carries 11 of the 20 trades. | correct | B:screens[11] |
| l29-random-chords.json | `.screens[11].explain.text` | A random day gives $\tfrac{900 - 500}{10} = \text{£}40$. A random trade lands on the busy day 11 times in 20, giving $\… | correct | B:screens[11] |
| l29-random-chords.json | `.summary.ideas[0]` | "Random" is not a procedure: ask how the object is drawn before computing. | correct | B:summary |
| l29-random-chords.json | `.summary.ideas[1]` | Bertrand's chord is longer than $\sqrt3$ with chance $\tfrac13$, $\tfrac12$ or $\tfrac14$, by endpoints, radius or midp… | correct | B:summary |
| l29-random-chords.json | `.summary.ideas[2]` | In the two envelopes, the rule that fills them decides when to switch; always switching gains nothing. | correct | B:summary |
| l29-random-chords.json | `.summary.formula.note` | Uniform $d$ gives $\tfrac12$; a uniform midpoint gives $d^2$, so $\tfrac14$. | correct | B:summary |
| l29-random-chords.json | `.summary.trap` | Answering $\tfrac13$ for a "random chord" without asking how it is drawn. | correct | B:summary |
| l29-random-chords.json | `.quiz[0].prose` | The pairs are (£10, £20), (£20, £40) and (£40, £80), equally likely. You open one envelope at random and see £40. | correct | B:quiz[0] |
| l29-random-chords.json | `.quiz[0].widget.accept` | £50 | correct | B:quiz[0] |
| l29-random-chords.json | `.quiz[0].feedback.correct` | $\tfrac{20 + 80}{2} = \text{£}50$. | correct | B:quiz[0] |
| l29-random-chords.json | `.quiz[0].feedback.generic` | Not quite right. List the cases in which you see £40. | correct | B:quiz[0] |
| l29-random-chords.json | `.quiz[0].feedback.byKey.keep` | That is keeping. The other holds £20 or £80, equally likely. | correct | B:quiz[0] |
| l29-random-chords.json | `.quiz[0].explain.text` | You see £40 in (£20, £40) and in (£40, £80), equally often. Switching gives £20 or £80, worth £50. Here it matches $1.2… | correct | B:quiz[0] |
| l29-random-chords.json | `.quiz[1].prose` | Choose a chord of the unit circle by two uniform endpoints. | correct | B:quiz[1] |
| l29-random-chords.json | `.quiz[1].widget.accept` | 2/3, about 0.6667 | correct | B:quiz[1] |
| l29-random-chords.json | `.quiz[1].feedback.correct` | $\tfrac23$. | correct | B:quiz[1] |
| l29-random-chords.json | `.quiz[1].feedback.generic` | Not quite right. Find the central angle at which the chord equals 1. | correct | B:quiz[1] |
| l29-random-chords.json | `.quiz[1].feedback.byKey.sqrt3` | That is the threshold $\sqrt3$. A chord of length 1 needs a central angle of only 60 degrees. | correct | B:quiz[1] |
| l29-random-chords.json | `.quiz[1].feedback.byKey.half` | You split the circle in half. Measure the arc where the angle exceeds 60 degrees. | correct | B:quiz[1] |
| l29-random-chords.json | `.quiz[1].explain.text` | A chord of length 1 has central angle 60 degrees, since $2\sin 30^\circ = 1$. It is longer when the angle is between 60… | correct | B:quiz[1] |
| l29-random-chords.json | `.quiz[2].prose` | Choose a chord by a uniform point on a radius, as before. | correct | B:quiz[2] |
| l29-random-chords.json | `.quiz[2].widget.accept` | $\sqrt3/2$, about 0.8660 | correct | B:quiz[2] |
| l29-random-chords.json | `.quiz[2].feedback.correct` | $\tfrac{\sqrt3}{2} \approx 0.8660$. | correct | B:quiz[2] |
| l29-random-chords.json | `.quiz[2].feedback.generic` | Not quite right. Solve $2\sqrt{1 - d^2} > 1$ for $d$. | correct | B:quiz[2] |
| l29-random-chords.json | `.quiz[2].feedback.byKey.area` | That is the midpoint procedure, $d^2 = \tfrac34$. Here $d$ is uniform. | correct | B:quiz[2] |
| l29-random-chords.json | `.quiz[2].feedback.byKey.half` | That is the $\sqrt3$ threshold. | correct | B:quiz[2] |
| l29-random-chords.json | `.quiz[2].explain.text` | $2\sqrt{1 - d^2} > 1$ means $d^2 < \tfrac34$, so $d < \tfrac{\sqrt3}{2}$. With $d$ uniform on $[0, 1]$, the chance is $… | correct | B:quiz[2] |

## l30-follow-ups.json

### Bases

| key | basis |
|---|---|
| screens[0] | sim: puzzles-L5-concepts-r2.py:P(max = m) = (2m-1)/n^2; E[max] = (n+1)(4n-1)/(6n) exhaustive at n = 1, 6, 10, 20, 100; sympy sum; 161/36, 553/40, 143/20, 67.165; H_12; continuous shortcut 66.67 |
| screens[1] | sim: puzzles-L5-concepts-r2.py:P(max = m) = (2m-1)/n^2; E[max] = (n+1)(4n-1)/(6n) exhaustive at n = 1, 6, 10, 20, 100; sympy sum; 161/36, 553/40, 143/20, 67.165; H_12; continuous shortcut 66.67 |
| screens[5] | sim: puzzles-L5-concepts-r2.py:P(max = m) = (2m-1)/n^2; E[max] = (n+1)(4n-1)/(6n) exhaustive at n = 1, 6, 10, 20, 100; sympy sum; 161/36, 553/40, 143/20, 67.165; H_12; continuous shortcut 66.67 |
| screens[6] | sim: puzzles-L5-concepts-r2.py:P(max = m) = (2m-1)/n^2; E[max] = (n+1)(4n-1)/(6n) exhaustive at n = 1, 6, 10, 20, 100; sympy sum; 161/36, 553/40, 143/20, 67.165; H_12; continuous shortcut 66.67 |
| screens[8] | sim: puzzles-L5-concepts-r2.py:P(max = m) = (2m-1)/n^2; E[max] = (n+1)(4n-1)/(6n) exhaustive at n = 1, 6, 10, 20, 100; sympy sum; 161/36, 553/40, 143/20, 67.165; H_12; continuous shortcut 66.67 |
| screens[11] | sim: puzzles-L5-concepts-r2.py:P(max = m) = (2m-1)/n^2; E[max] = (n+1)(4n-1)/(6n) exhaustive at n = 1, 6, 10, 20, 100; sympy sum; 161/36, 553/40, 143/20, 67.165; H_12; continuous shortcut 66.67 |
| summary | sim: puzzles-L5-concepts-r2.py:P(max = m) = (2m-1)/n^2; E[max] = (n+1)(4n-1)/(6n) exhaustive at n = 1, 6, 10, 20, 100; sympy sum; 161/36, 553/40, 143/20, 67.165; H_12; continuous shortcut 66.67 |
| screens[2] | optimal stopping with recall-free rerolls, Bellman V = E[max(X, V-c)]; sim: puzzles-L5-concepts-r2.py:reroll values by value iteration and threshold rules agree for ten (faces, cost) cases; one-step lookahead is worth 4.25 < 4.5 at c = 0.5; keep >= n - c is worth 3.5 < 4; thresholds V - c = 3, 2.25, 4.5, 14.17; solution passes all 11 tests |
| screens[7] | optimal stopping with recall-free rerolls, Bellman V = E[max(X, V-c)]; sim: puzzles-L5-concepts-r2.py:reroll values by value iteration and threshold rules agree for ten (faces, cost) cases; one-step lookahead is worth 4.25 < 4.5 at c = 0.5; keep >= n - c is worth 3.5 < 4; thresholds V - c = 3, 2.25, 4.5, 14.17; solution passes all 11 tests |
| screens[10] | optimal stopping with recall-free rerolls, Bellman V = E[max(X, V-c)]; sim: puzzles-L5-concepts-r2.py:reroll values by value iteration and threshold rules agree for ten (faces, cost) cases; one-step lookahead is worth 4.25 < 4.5 at c = 0.5; keep >= n - c is worth 3.5 < 4; thresholds V - c = 3, 2.25, 4.5, 14.17; solution passes all 11 tests |
| quiz[0] | optimal stopping with recall-free rerolls, Bellman V = E[max(X, V-c)]; sim: puzzles-L5-concepts-r2.py:reroll values by value iteration and threshold rules agree for ten (faces, cost) cases; one-step lookahead is worth 4.25 < 4.5 at c = 0.5; keep >= n - c is worth 3.5 < 4; thresholds V - c = 3, 2.25, 4.5, 14.17; solution passes all 11 tests |
| screens[3] | sim: puzzles-L5-concepts-r2.py:6/11, 36/91, 4/7, 8/15 |
| quiz[1] | sim: puzzles-L5-concepts-r2.py:6/11, 36/91, 4/7, 8/15 |
| screens[4] | sim: puzzles-L5-concepts-r2.py:(2n+1)/3 fails at n=6, passes n=1, has the right growth 2n/3; the larger of two uniforms on [0,n] averages 2n/3 |
| screens[9] | Feller vol. 1 XIII.7 (recurrent patterns, waiting times) and GKP Concrete Mathematics 8.4 (Penney, Conway leading numbers); first-step analysis: sim: puzzles-L5-concepts-r2.py:run waits 57/8, 30, 14, 42; run formula sum 1/p^j |
| quiz[2] | Feller vol. 1 XIII.7 (recurrent patterns, waiting times) and GKP Concrete Mathematics 8.4 (Penney, Conway leading numbers); first-step analysis: sim: puzzles-L5-concepts-r2.py:run waits 57/8, 30, 14, 42; run formula sum 1/p^j |

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l30-follow-ups.json | `.screens[0].prose` | In l1 you priced a bet paying the larger of two dice at $\tfrac{161}{36}$. The interviewer asks at once: and with $n$-s… | correct | B:screens[0] |
| l30-follow-ups.json | `.screens[0].hints[0].text` | Find every cell showing 4. | correct | B:screens[0] |
| l30-follow-ups.json | `.screens[0].hints[1].text` | They form an L: row 4 and column 4, up to (4, 4). | correct | B:screens[0] |
| l30-follow-ups.json | `.screens[0].hints[2].text` | 4 in the row plus 3 more in the column: 7. | correct | B:screens[0] |
| l30-follow-ups.json | `.screens[0].feedback.correct` | Seven cells: $2 \times 4 - 1$. | correct | B:screens[0] |
| l30-follow-ups.json | `.screens[0].feedback.generic` | Not quite right. Tap every cell that shows 4. | correct | B:screens[0] |
| l30-follow-ups.json | `.screens[0].feedback.byKey.cross` | You took all of row 4 and column 4. (4, 6) has larger face 6. | correct | B:screens[0] |
| l30-follow-ups.json | `.screens[0].explain.text` | The larger face is $m$ in an L of $2m - 1$ cells, here 7. That count does not depend on the number of faces. So on $n$-… | correct | B:screens[0] |
| l30-follow-ups.json | `.screens[1].prose` | Summing $m \cdot \tfrac{2m - 1}{n^2}$ over $m$ gives $E[\max] = \tfrac{(n + 1)(4n - 1)}{6n}$. Before using it, **check,… | correct | B:screens[1] |
| l30-follow-ups.json | `.screens[1].hints[0].text` | Substitute $n$ into $\tfrac{(n + 1)(4n - 1)}{6n}$. | correct | B:screens[1] |
| l30-follow-ups.json | `.screens[1].hints[1].text` | At $n = 6$: $\tfrac{7 \times 23}{36}$. At $n = 20$: $\tfrac{21 \times 79}{120}$. | correct | B:screens[1] |
| l30-follow-ups.json | `.screens[1].hints[2].text` | $\tfrac{161}{36} \approx 4.4722$ matches l1, so trust it: $\tfrac{1659}{120} = 13.825$. | correct | B:screens[1] |
| l30-follow-ups.json | `.screens[1].feedback.correct` | 4.4722 matches l1, so 13.825 can be trusted. | correct | B:screens[1] |
| l30-follow-ups.json | `.screens[1].feedback.generic` | Not quite right. Check the first answer that is marked. | correct | B:screens[1] |
| l30-follow-ups.json | `.screens[1].feedback.byKey.r0c1` | Check $n = 6$: $\tfrac{7 \times 23}{36} = \tfrac{161}{36}$. | correct | B:screens[1] |
| l30-follow-ups.json | `.screens[1].feedback.byKey.r1c1` | Check $n = 20$: $\tfrac{21 \times 79}{120}$. | correct | B:screens[1] |
| l30-follow-ups.json | `.screens[1].explain.text` | At $n = 6$ the formula gives $\tfrac{161}{36}$, the answer you already had. That check costs ten seconds and catches mo… | correct | B:screens[1] |
| l30-follow-ups.json | `.screens[2].prose` | Back to l1's reroll game: roll one die and keep the face in £, or pay $c$ to roll again. You may reroll as often as you… | correct | B:screens[2] |
| l30-follow-ups.json | `.screens[2].hints[0].text` | Each bar is a threshold rule. The value is the tallest bar. | correct | B:screens[2] |
| l30-follow-ups.json | `.screens[2].hints[1].text` | Keeping faces of at least $t$: $V = \tfrac{\text{sum of kept faces} - (t - 1)c}{7 - t}$. | correct | B:screens[2] |
| l30-follow-ups.json | `.screens[2].hints[2].text` | At £0.50, keep 4 or more: $\tfrac{15 - 1.5}{3}$. At £2, reroll only a 1: $\tfrac{20 - 2}{5}$. At £3, never reroll. | correct | B:screens[2] |
| l30-follow-ups.json | `.screens[2].feedback.correct` | £4.50, £3.60 and £3.50. | correct | B:screens[2] |
| l30-follow-ups.json | `.screens[2].feedback.generic` | Not quite right. Check the first answer that is marked. | correct | B:screens[2] |
| l30-follow-ups.json | `.screens[2].feedback.byKey.r0c1` | Check £0.50: keeping 4, 5 or 6 gives $\tfrac{15 - 3 \times 0.5}{3} = 4.5$. | correct | B:screens[2] |
| l30-follow-ups.json | `.screens[2].feedback.byKey.r1c1` | Check £2: rerolling only a 1 gives $\tfrac{20 - 2}{5} = 3.6$. | correct | B:screens[2] |
| l30-follow-ups.json | `.screens[2].feedback.byKey.r2c1` | Check £3: every reroll rule is worth less than keeping the first face, £3.50. | correct | B:screens[2] |
| l30-follow-ups.json | `.screens[2].explain.text` | At £0.50 you keep 4 or more (a 4 is a tie), worth £4.50. At £2 you reroll only a 1, worth £3.60. From £2.50 up the opti… | correct | B:screens[2] |
| l30-follow-ups.json | `.screens[3].prose` | In l19, two players rolled in turn and the first six won: $\tfrac{6}{11}$ for the first. With $k$ players, one round gi… | correct | B:screens[3] |
| l30-follow-ups.json | `.screens[3].hints[0].text` | Put $p = \tfrac16$ and $k = 2$, then $k = 3$. | correct | B:screens[3] |
| l30-follow-ups.json | `.screens[3].hints[1].text` | $(\tfrac56)^2 = \tfrac{25}{36}$ and $(\tfrac56)^3 = \tfrac{125}{216}$. | correct | B:screens[3] |
| l30-follow-ups.json | `.screens[3].hints[2].text` | $\tfrac{1/6}{11/36} = \tfrac{6}{11}$, then $\tfrac{1/6}{91/216} = \tfrac{36}{91}$. | correct | B:screens[3] |
| l30-follow-ups.json | `.screens[3].feedback.correct` | $\tfrac{6}{11}$ checks out, so $\tfrac{36}{91} \approx 0.3956$. | correct | B:screens[3] |
| l30-follow-ups.json | `.screens[3].feedback.generic` | Not quite right. Check the first answer that is marked. | correct | B:screens[3] |
| l30-follow-ups.json | `.screens[3].feedback.byKey.r0c1` | Check two players: $\tfrac{1/6}{1 - 25/36}$. | correct | B:screens[3] |
| l30-follow-ups.json | `.screens[3].feedback.byKey.r1c1` | Check three players: a round ends with no six with $\tfrac{125}{216}$. | correct | B:screens[3] |
| l30-follow-ups.json | `.screens[3].explain.text` | The formula returns $\tfrac{6}{11}$ at $k = 2$, the case you knew. At $k = 3$ it gives $\tfrac{36}{91} \approx 0.3956$,… | correct | B:screens[3] |
| l30-follow-ups.json | `.screens[4].prose` | Under time, a candidate offers $\tfrac{2n + 1}{3}$ for the mean of the larger of two $n$-sided dice. It gives 1 at $n =… | correct | B:screens[4] |
| l30-follow-ups.json | `.screens[4].widget.options[0].text` | Test it at $n = 6$: it gives $\tfrac{13}{3}$, not $\tfrac{161}{36}$, so reject it | correct | B:screens[4] |
| l30-follow-ups.json | `.screens[4].widget.options[1].why` | One check at a trivial case is weak: many wrong formulas give 1 at $n = 1$. | correct | B:screens[4] |
| l30-follow-ups.json | `.screens[4].widget.options[2].why` | The right size is not the right answer. At $n = 6$ it misses $\tfrac{161}{36}$. | correct | B:screens[4] |
| l30-follow-ups.json | `.screens[4].widget.options[3].why` | That works but burns the time you saved. The known case tests the formula in seconds. | correct | B:screens[4] |
| l30-follow-ups.json | `.screens[4].hints[0].text` | Which case do you already know exactly? | correct | B:screens[4] |
| l30-follow-ups.json | `.screens[4].hints[1].text` | At $n = 6$ the answer is $\tfrac{161}{36} \approx 4.47$. | correct | B:screens[4] |
| l30-follow-ups.json | `.screens[4].hints[2].text` | $\tfrac{2 \times 6 + 1}{3} = \tfrac{13}{3} \approx 4.33$. | correct | B:screens[4] |
| l30-follow-ups.json | `.screens[4].feedback.correct` | Reject it: it fails the case you solved. | correct | B:screens[4] |
| l30-follow-ups.json | `.screens[4].feedback.generic` | Not quite right. Test the formula on the case you know. | correct | B:screens[4] |
| l30-follow-ups.json | `.screens[4].feedback.byKey.b` | You checked only $n = 1$. Test a case that carries information, such as $n = 6$. | correct | B:screens[4] |
| l30-follow-ups.json | `.screens[4].explain.text` | At $n = 6$ the candidate's formula gives $\tfrac{13}{3} \approx 4.33$, not $\tfrac{161}{36} \approx 4.47$. So it is wro… | correct | B:screens[4] |
| l30-follow-ups.json | `.screens[5].prose` | Every follow-up here went the same way. Solve the general case, check it on the case you solved, then substitute: $$E[\… | correct | B:screens[5] |
| l30-follow-ups.json | `.screens[5].widget.options[0].text` | 1 | correct | B:screens[5] |
| l30-follow-ups.json | `.screens[5].widget.options[1].why` | You dropped the $n + 1$: $\tfrac36 = \tfrac12$. | correct | B:screens[5] |
| l30-follow-ups.json | `.screens[5].widget.options[2].why` | That is $\tfrac{2n}{3}$, the continuous answer, at $n = 1$. | correct | B:screens[5] |
| l30-follow-ups.json | `.screens[5].hints[0].text` | Put $n = 1$ into $\tfrac{(n + 1)(4n - 1)}{6n}$. | correct | B:screens[5] |
| l30-follow-ups.json | `.screens[5].hints[1].text` | The numerator is $2 \times 3$. | correct | B:screens[5] |
| l30-follow-ups.json | `.screens[5].hints[2].text` | $\tfrac66 = 1$. | correct | B:screens[5] |
| l30-follow-ups.json | `.screens[5].feedback.correct` | 1: a one-sided die always shows 1. | correct | B:screens[5] |
| l30-follow-ups.json | `.screens[5].feedback.generic` | Not quite right. Substitute $n = 1$ carefully. | correct | B:screens[5] |
| l30-follow-ups.json | `.screens[5].explain.text` | The edge case $n = 1$ must give 1, and it does. A general answer should pass every case you can check in your head. Try… | correct | B:screens[5] |
| l30-follow-ups.json | `.screens[6].prose` | Derive the mean of the larger of two $n$-sided dice, one justified line at a time. | correct | B:screens[6] |
| l30-follow-ups.json | `.screens[6].widget.lines[0].text` | The larger is $m$ in an L of $2m - 1$ cells, so $P(\max = m) = \tfrac{2m - 1}{n^2}$. | correct | B:screens[6] |
| l30-follow-ups.json | `.screens[6].widget.lines[1].text` | So $E[\max] = \tfrac{1}{n^2}\sum_{m=1}^{n} m(2m - 1) = \tfrac{1}{n^2}\left(2\sum m^2 - \sum m\right)$. | correct | B:screens[6] |
| l30-follow-ups.json | `.screens[6].widget.lines[2].text` | Use $\sum m^2 = \tfrac{n(n + 1)(2n + 1)}{6}$ and $\sum m = \tfrac{n(n + 1)}{2}$. | correct | B:screens[6] |
| l30-follow-ups.json | `.screens[6].widget.lines[3].text` | Then $2\sum m^2 - \sum m = \tfrac{n(n + 1)(4n - 1)}{6}$, so $E[\max] = \tfrac{(n + 1)(4n - 1)}{6n}$. | correct | B:screens[6] |
| l30-follow-ups.json | `.screens[6].widget.lines[4].text` | Check: $n = 6$ gives $\tfrac{7 \times 23}{36} = \tfrac{161}{36}$. | correct | B:screens[6] |
| l30-follow-ups.json | `.screens[6].widget.lines[5].text` | The larger of two uniforms on $[0, n]$ averages $\tfrac{2n}{3}$, so $E[\max] = \tfrac{2n}{3}$. | correct | B:screens[6] |
| l30-follow-ups.json | `.screens[6].widget.lines[5].why` | That is the continuous answer. Dice are discrete: $\tfrac{2 \times 6}{3} = 4$, not $\tfrac{161}{36}$. | correct | B:screens[6] |
| l30-follow-ups.json | `.screens[6].hints[0].text` | Start from the chance of each value of the larger. | correct | B:screens[6] |
| l30-follow-ups.json | `.screens[6].hints[1].text` | Then write the mean as a sum and split it. | correct | B:screens[6] |
| l30-follow-ups.json | `.screens[6].hints[2].text` | Chances, sum, standard sums, algebra, check. | correct | B:screens[6] |
| l30-follow-ups.json | `.screens[6].feedback.correct` | Chances, sum, algebra, then the check against l1. | correct | B:screens[6] |
| l30-follow-ups.json | `.screens[6].feedback.generic` | Not quite right. Begin with $P(\max = m)$. | correct | B:screens[6] |
| l30-follow-ups.json | `.screens[6].feedback.byKey.d1` | You used the continuous answer. It is the large-$n$ limit, not the exact mean. | correct | B:screens[6] |
| l30-follow-ups.json | `.screens[6].feedback.byKey.left-out` | Every line except the continuous shortcut belongs. | correct | B:screens[6] |
| l30-follow-ups.json | `.screens[6].explain.text` | Each line rests on the L of $2m - 1$ cells and two standard sums. The last line checks the result against $\tfrac{161}{… | correct | B:screens[6] |
| l30-follow-ups.json | `.screens[7].prose` | Write `max_of_two(n)` and `reroll_value(faces, cost)`, both returning a `Fraction`. For the reroll game, try every rule… | correct | B:screens[7] |
| l30-follow-ups.json | `.screens[7].widget.how` | Check runs 11 hidden tests, each an exact `Fraction`. Four test the larger of two dice. Seven test reroll games, with c… | correct | B:screens[7] |
| l30-follow-ups.json | `.screens[7].hints[0].text` | `max_of_two` is one line from the formula. | correct | B:screens[7] |
| l30-follow-ups.json | `.screens[7].hints[1].text` | For a threshold $t$, solve $nV = \text{kept} + (t - 1)(V - c)$ for $V$. | correct | B:screens[7] |
| l30-follow-ups.json | `.screens[7].hints[2].text` | That gives $V = \tfrac{\text{kept} - (t - 1)c}{n - t + 1}$; take the largest over $t$. | correct | B:screens[7] |
| l30-follow-ups.json | `.screens[7].feedback.correct` | Both general answers, exact. | correct | B:screens[7] |
| l30-follow-ups.json | `.screens[7].feedback.generic` | Not quite right. Look at the first failing test. | correct | B:screens[7] |
| l30-follow-ups.json | `.screens[7].feedback.byKey.test-1` | Return `Fraction((n + 1) * (4 * n - 1), 6 * n)`. | correct | B:screens[7] |
| l30-follow-ups.json | `.screens[7].feedback.byKey.test-5` | At cost £1 the best rule keeps 3 or more, worth £4. | correct | B:screens[7] |
| l30-follow-ups.json | `.screens[7].explain.text` | Each threshold rule gives one linear equation in $V$, and the best rule gives the value. A 10-sided die at £1 keeps 6 o… | correct | B:screens[7] |
| l30-follow-ups.json | `.screens[8].prose` | Drill: about 3 minutes a puzzle, as interviews allow. Keep your own time and say each argument aloud. Each extends a le… | correct | B:screens[8] |
| l30-follow-ups.json | `.screens[8].hints[0].text` | Use the general answers from l1 and l2. | correct | B:screens[8] |
| l30-follow-ups.json | `.screens[8].hints[1].text` | $\tfrac{(n + 1)(4n - 1)}{6n}$ and $n H_n$. | correct | B:screens[8] |
| l30-follow-ups.json | `.screens[8].hints[2].text` | $\tfrac{11 \times 39}{60}$, and $12(1 + \tfrac12 + \dots + \tfrac{1}{12})$. | correct | B:screens[8] |
| l30-follow-ups.json | `.screens[8].feedback.correct` | $\tfrac{143}{20} = 7.15$ and $12H_{12} \approx 37.2385$. | correct | B:screens[8] |
| l30-follow-ups.json | `.screens[8].feedback.generic` | Not quite right. Check the first answer that is marked. | correct | B:screens[8] |
| l30-follow-ups.json | `.screens[8].feedback.byKey.r0c1` | Check the dice: $\tfrac{11 \times 39}{60} = 7.15$. | correct | B:screens[8] |
| l30-follow-ups.json | `.screens[8].feedback.byKey.r1c1` | Check the coupons: $H_{12} \approx 3.1032$. | correct | B:screens[8] |
| l30-follow-ups.json | `.screens[8].explain.text` | Both are one substitution once the general case is in hand. $\tfrac{11 \times 39}{60} = 7.15$, and $12 H_{12} = \tfrac{… | correct | B:screens[8] |
| l30-follow-ups.json | `.screens[9].prose` | Two more at the same pace. Each extends a puzzle from l3 or l19. Give four decimal places. | correct | B:screens[9] |
| l30-follow-ups.json | `.screens[9].hints[0].text` | Use $\tfrac{p}{1 - (1 - p)^k}$ and the run formula. | correct | B:screens[9] |
| l30-follow-ups.json | `.screens[9].hints[1].text` | For a run of $r$ heads, $E = \tfrac1p + \tfrac{1}{p^2} + \dots + \tfrac{1}{p^r}$. | correct | B:screens[9] |
| l30-follow-ups.json | `.screens[9].hints[2].text` | $\tfrac{1/2}{7/8} = \tfrac47$, and $\tfrac32 + \tfrac94 + \tfrac{27}{8}$. | correct | B:screens[9] |
| l30-follow-ups.json | `.screens[9].feedback.correct` | $\tfrac47 \approx 0.5714$ and $\tfrac{57}{8} = 7.125$. | correct | B:screens[9] |
| l30-follow-ups.json | `.screens[9].feedback.generic` | Not quite right. Check the first answer that is marked. | correct | B:screens[9] |
| l30-follow-ups.json | `.screens[9].feedback.byKey.r0c1` | Check the coin game: a round of three flips has no head with $\tfrac18$. | correct | B:screens[9] |
| l30-follow-ups.json | `.screens[9].feedback.byKey.r1c1` | Check the run: $\tfrac1p = \tfrac32$, then square and cube it. | correct | B:screens[9] |
| l30-follow-ups.json | `.screens[9].explain.text` | The turn formula gives $\tfrac{1/2}{1 - 1/8} = \tfrac47$. The run formula gives $\tfrac32 + \tfrac94 + \tfrac{27}{8} = … | correct | B:screens[9] |
| l30-follow-ups.json | `.screens[10].prose` | The interviewer's third question on the reroll game: an $n$-sided die, and a cost $c$ a reroll. State the rule in one s… | correct | B:screens[10] |
| l30-follow-ups.json | `.screens[10].widget.options[0].text` | Keep any face of at least $V - c$, where $V$ solves $V = E[\max(X, V - c)]$ | correct | B:screens[10] |
| l30-follow-ups.json | `.screens[10].widget.options[1].why` | That ignores the cost. At $c = 0$ you would reroll until $n$. | correct | B:screens[10] |
| l30-follow-ups.json | `.screens[10].widget.options[2].why` | That looks one roll ahead. You may reroll again, so compare with $V - c$, not with one roll. | correct | B:screens[10] |
| l30-follow-ups.json | `.screens[10].widget.options[3].why` | That fails at $n = 6$, $c = 1$: it says keep 5 or more, but the best rule keeps 3 or more. | correct | B:screens[10] |
| l30-follow-ups.json | `.screens[10].hints[0].text` | What do you get if you reroll? | correct | B:screens[10] |
| l30-follow-ups.json | `.screens[10].hints[1].text` | A reroll costs $c$ and puts you back at the start, worth $V$. | correct | B:screens[10] |
| l30-follow-ups.json | `.screens[10].hints[2].text` | So keep $x$ exactly when $x \ge V - c$. | correct | B:screens[10] |
| l30-follow-ups.json | `.screens[10].feedback.correct` | Keep $x$ when $x \ge V - c$. | correct | B:screens[10] |
| l30-follow-ups.json | `.screens[10].feedback.generic` | Not quite right. Compare a face with what rerolling is worth. | correct | B:screens[10] |
| l30-follow-ups.json | `.screens[10].feedback.byKey.c` | You looked one roll ahead. The option to reroll again is part of what a reroll is worth. | correct | B:screens[10] |
| l30-follow-ups.json | `.screens[10].explain.text` | Rerolling costs $c$ and restarts a game worth $V$, so a face $x$ is kept when $x \ge V - c$. At $n = 6$, $c = 1$, that … | correct | B:screens[10] |
| l30-follow-ups.json | `.screens[11].prose` | A market-making interviewer has your price for the larger of two dice, $\tfrac{161}{36}$. Now they want a fair price fo… | correct | B:screens[11] |
| l30-follow-ups.json | `.screens[11].widget.accept` | 13433/200 = 67.165 | correct | B:screens[11] |
| l30-follow-ups.json | `.screens[11].hints[0].text` | You already have the general case. | correct | B:screens[11] |
| l30-follow-ups.json | `.screens[11].hints[1].text` | Check $\tfrac{(n + 1)(4n - 1)}{6n}$ at $n = 6$ first. | correct | B:screens[11] |
| l30-follow-ups.json | `.screens[11].hints[2].text` | $\tfrac{101 \times 399}{600}$. | correct | B:screens[11] |
| l30-follow-ups.json | `.screens[11].feedback.correct` | $\tfrac{101 \times 399}{600} = \text{£}67.165$. | correct | B:screens[11] |
| l30-follow-ups.json | `.screens[11].feedback.generic` | Not quite right. Substitute $n = 100$ into the checked formula. | correct | B:screens[11] |
| l30-follow-ups.json | `.screens[11].feedback.byKey.continuous` | That is $\tfrac{2n}{3}$, the continuous limit. It is close, but the bet pays whole faces. | correct | B:screens[11] |
| l30-follow-ups.json | `.screens[11].feedback.byKey.mean` | That is the mean of one die. The larger of two sits higher. | correct | B:screens[11] |
| l30-follow-ups.json | `.screens[11].explain.text` | Stating the general case first turned the follow-up into one substitution: $\tfrac{40299}{600} = \text{£}67.165$. The c… | correct | B:screens[11] |
| l30-follow-ups.json | `.summary.ideas[0]` | Interviewers extend a solved puzzle at once, so solve the general case. | correct | B:summary |
| l30-follow-ups.json | `.summary.ideas[1]` | Check the general answer on the case you solved, and on $n = 1$, before you substitute. | correct | B:summary |
| l30-follow-ups.json | `.summary.ideas[2]` | A cost per reroll keeps the threshold rule: keep $x$ when $x \ge V - c$. | correct | B:summary |
| l30-follow-ups.json | `.summary.formula.note` | Check: $n = 6$ gives $\tfrac{161}{36}$. | correct | B:summary |
| l30-follow-ups.json | `.summary.trap` | Trusting a general formula you have not tested on the case you already solved. | correct | B:summary |
| l30-follow-ups.json | `.quiz[0].prose` | L1's reroll game with a six-sided die, at a cost of £1.50 a reroll. | correct | B:quiz[0] |
| l30-follow-ups.json | `.quiz[0].widget.accept` | 15/4 = 3.75 | correct | B:quiz[0] |
| l30-follow-ups.json | `.quiz[0].feedback.correct` | £3.75: reroll only a 1 or a 2. | correct | B:quiz[0] |
| l30-follow-ups.json | `.quiz[0].feedback.generic` | Not quite right. Try each threshold rule. | correct | B:quiz[0] |
| l30-follow-ups.json | `.quiz[0].feedback.byKey.one` | That is the £1 game. A dearer reroll lowers the value. | correct | B:quiz[0] |
| l30-follow-ups.json | `.quiz[0].feedback.byKey.never` | At £1.50 rerolling a 1 or a 2 still pays. | correct | B:quiz[0] |
| l30-follow-ups.json | `.quiz[0].explain.text` | Keeping 3 or more gives $\tfrac{18 - 2 \times 1.5}{4} = \text{£}3.75$. Rerolling only a 1 gives £3.70. The threshold is… | correct | B:quiz[0] |
| l30-follow-ups.json | `.quiz[1].prose` | Four players flip a fair coin in turn, and the first head wins. | correct | B:quiz[1] |
| l30-follow-ups.json | `.quiz[1].widget.accept` | 8/15, about 0.5333 | correct | B:quiz[1] |
| l30-follow-ups.json | `.quiz[1].feedback.correct` | $\tfrac{1/2}{1 - 1/16} = \tfrac{8}{15}$. | correct | B:quiz[1] |
| l30-follow-ups.json | `.quiz[1].feedback.generic` | Not quite right. Use $\tfrac{p}{1 - (1 - p)^k}$ with $k = 4$. | correct | B:quiz[1] |
| l30-follow-ups.json | `.quiz[1].feedback.byKey.quarter` | You split it evenly. The first seat has the first chance every round. | correct | B:quiz[1] |
| l30-follow-ups.json | `.quiz[1].feedback.byKey.two` | That is two players. | correct | B:quiz[1] |
| l30-follow-ups.json | `.quiz[1].explain.text` | A round of four flips has no head with $\tfrac{1}{16}$. So $x = \tfrac{1/2}{15/16} = \tfrac{8}{15} \approx 0.5333$. | correct | B:quiz[1] |
| l30-follow-ups.json | `.quiz[2].prose` | A fair coin is flipped until four heads in a row. | correct | B:quiz[2] |
| l30-follow-ups.json | `.quiz[2].widget.accept` | 30 exactly | correct | B:quiz[2] |
| l30-follow-ups.json | `.quiz[2].feedback.correct` | $2 + 4 + 8 + 16 = 30$. | correct | B:quiz[2] |
| l30-follow-ups.json | `.quiz[2].feedback.generic` | Not quite right. Extend the run formula by one term. | correct | B:quiz[2] |
| l30-follow-ups.json | `.quiz[2].feedback.byKey.sixteen` | That is $\tfrac{1}{p^4}$ alone. Add the shorter runs too. | correct | B:quiz[2] |
| l30-follow-ups.json | `.quiz[2].feedback.byKey.hhh` | That is HHH. One more head adds 16. | correct | B:quiz[2] |
| l30-follow-ups.json | `.quiz[2].explain.text` | For a run of $r$ heads, $E = \tfrac1p + \dots + \tfrac{1}{p^r}$. With $p = \tfrac12$ and $r = 4$ that is 30. It checks … | correct | B:quiz[2] |

## review-5.json

### Bases

| key | basis |
|---|---|
| items[0] | sim: puzzles-L5-concepts-r2.py:five people 24/5 |
| items[1] | Casella and Berger ch. 7 (Lehmann-Scheffe, UMVUE of a uniform endpoint) and Goodman (1954) serial-number estimation; sim: puzzles-L5-concepts-r2.py:estimates 59 |
| items[2] | sim: puzzles-L5-concepts-r2.py:E[R] exhaustive; 84.5 |
| items[3] | sim: puzzles-L5-concepts-r2.py:16/7, 5/6 |
| items[4] | sim: puzzles-L5-concepts-r2.py:16/7, 5/6 |
| items[5] | sim: puzzles-L5-concepts-r2.py:duel(1/5, 1/4) = 1/2; even when q = p/(1-p) |
| items[6] | sim: puzzles-L5-concepts-r2.py:A air 25/63, 8/21, 2/9 (independent solver) |
| items[7] | sim: puzzles-L5-concepts-r2.py:seeing 10: switching worth 12.5; at 40 keep |
| items[8] | sim: puzzles-L5-concepts-r2.py:midpoint 3/4 for a chord longer than 1 |
| items[9] | sim: puzzles-L5-concepts-r2.py:reroll 8-sided at cost 1: value 11/2; threshold 4.5 |

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| review-5.json | `.items[0].prose` | A fair coin, and a fair choice among five people. You flip three times, give five of the eight strings one person each,… | correct | B:items[0] |
| review-5.json | `.items[0].widget.accept` | 24/5 = 4.8 | correct | B:items[0] |
| review-5.json | `.items[0].feedback.correct` | $3 \times \tfrac85 = 4.8$ flips. | correct | B:items[0] |
| review-5.json | `.items[0].feedback.generic` | Not quite right. Multiply three flips by the expected number of rounds. | correct | B:items[0] |
| review-5.json | `.items[0].feedback.byKey.three` | Three flips is one round. Three strings in eight start again. | correct | B:items[0] |
| review-5.json | `.items[0].feedback.byKey.rounds` | That is the number of rounds, $\tfrac85$. Each is three flips. | correct | B:items[0] |
| review-5.json | `.items[0].explain.text` | A round succeeds with chance $\tfrac58$, so we expect $\tfrac85$ rounds of three flips. That is $\tfrac{24}{5} = 4.8$ f… | correct | B:items[0] |
| review-5.json | `.items[1].prose` | Three serial numbers are seen: 10, 33 and 45, drawn at random from 1 to $N$. | correct | B:items[1] |
| review-5.json | `.items[1].widget.accept` | 59 exactly | correct | B:items[1] |
| review-5.json | `.items[1].feedback.correct` | $45 + 15 - 1 = 59$. | correct | B:items[1] |
| review-5.json | `.items[1].feedback.generic` | Not quite right. Use $m + \tfrac{m}{k} - 1$. | correct | B:items[1] |
| review-5.json | `.items[1].feedback.byKey.max` | The largest seen is low on average: the top gap is hidden. | correct | B:items[1] |
| review-5.json | `.items[1].feedback.byKey.no-minus-one` | You added $\tfrac{m}{k}$ but not the $-1$. | correct | B:items[1] |
| review-5.json | `.items[1].explain.text` | Below 45 there are 42 unseen numbers in three gaps, 14 on average. Add one gap: $45 + 14 = 59$. | correct | B:items[1] |
| review-5.json | `.items[2].prose` | Fund numbers run from an unknown start, $a + 1$ to $a + N$. You see five: 105, 120, 131, 150 and 162. | correct | B:items[2] |
| review-5.json | `.items[2].widget.accept` | 169/2 = 84.5 | correct | B:items[2] |
| review-5.json | `.items[2].feedback.correct` | $57 \times \tfrac64 - 1 = 84.5$. | correct | B:items[2] |
| review-5.json | `.items[2].feedback.generic` | Not quite right. Use the range: $\hat N = R\,\tfrac{k + 1}{k - 1} - 1$. | correct | B:items[2] |
| review-5.json | `.items[2].feedback.byKey.from-one` | That assumes the numbers start at 1. The start is unknown, so use the range. | correct | B:items[2] |
| review-5.json | `.items[2].feedback.byKey.no-minus-one` | You found $N + 1$. Take one off. | correct | B:items[2] |
| review-5.json | `.items[2].feedback.byKey.range` | The range misses two end gaps. | correct | B:items[2] |
| review-5.json | `.items[2].explain.text` | The range is $162 - 105 = 57$, and $E[R] = \tfrac{(k - 1)(N + 1)}{k + 1}$. Solving with $k = 5$ gives $\hat N = 57 \tim… | correct | B:items[2] |
| review-5.json | `.items[3].prose` | The larger of two dice is 4. | correct | B:items[3] |
| review-5.json | `.items[3].widget.accept` | 16/7, about 2.2857 | correct | B:items[3] |
| review-5.json | `.items[3].feedback.correct` | $\tfrac{16}{7} \approx 2.2857$. | correct | B:items[3] |
| review-5.json | `.items[3].feedback.generic` | Not quite right. List the seven rolls with larger die 4. | correct | B:items[3] |
| review-5.json | `.items[3].feedback.byKey.uniform` | You took the other die as uniform on 1 to 4. (4, 4) is one roll, but (4, 1) and (1, 4) are two. | correct | B:items[3] |
| review-5.json | `.items[3].explain.text` | The rolls are $(4, b)$ for $b \le 4$ and $(a, 4)$ for $a \le 3$: seven in all. Their smaller dice add to $10 + 6 = 16$,… | correct | B:items[3] |
| review-5.json | `.items[4].prose` | Two dice total at least 10. | correct | B:items[4] |
| review-5.json | `.items[4].widget.accept` | 5/6, about 0.8333 | correct | B:items[4] |
| review-5.json | `.items[4].feedback.correct` | $\tfrac56$. | correct | B:items[4] |
| review-5.json | `.items[4].feedback.generic` | Not quite right. List the six rolls with a total of 10 or more. | correct | B:items[4] |
| review-5.json | `.items[4].feedback.byKey.unconditional` | That is the chance before the condition, $\tfrac{11}{36}$. | correct | B:items[4] |
| review-5.json | `.items[4].explain.text` | The rolls are (4, 6), (5, 5), (6, 4), (5, 6), (6, 5) and (6, 6). Only (5, 5) lacks a six, so the chance is $\tfrac56$. | correct | B:items[4] |
| review-5.json | `.items[5].prose` | A duel: A hits with $\tfrac15$, B with $\tfrac14$, and A fires first. | correct | B:items[5] |
| review-5.json | `.items[5].widget.accept` | 1/2 = 0.5 | correct | B:items[5] |
| review-5.json | `.items[5].feedback.correct` | $\tfrac{1/5}{1 - \frac45 \cdot \frac34} = \tfrac12$. | correct | B:items[5] |
| review-5.json | `.items[5].feedback.generic` | Not quite right. Both miss with $\tfrac45 \times \tfrac34 = \tfrac35$. | correct | B:items[5] |
| review-5.json | `.items[5].feedback.byKey.ratio` | You used $\tfrac{p}{p + q}$. That ignores who fires first. | correct | B:items[5] |
| review-5.json | `.items[5].feedback.byKey.first-shot` | That is A's first shot alone. | correct | B:items[5] |
| review-5.json | `.items[5].explain.text` | A round restarts with chance $\tfrac35$, so $x = \tfrac{1/5}{2/5} = \tfrac12$. Indeed $q = \tfrac{p}{1 - p} = \tfrac14$… | correct | B:items[5] |
| review-5.json | `.items[6].prose` | The truel: A hits with $\tfrac13$, B with $\tfrac23$, C never misses. A fires into the air, and B and C aim at each oth… | correct | B:items[6] |
| review-5.json | `.items[6].widget.accept` | 2/9, about 0.2222 | correct | B:items[6] |
| review-5.json | `.items[6].feedback.correct` | $\tfrac13 \times \tfrac23 = \tfrac29$. | correct | B:items[6] |
| review-5.json | `.items[6].feedback.generic` | Not quite right. C must survive B, then survive A. | correct | B:items[6] |
| review-5.json | `.items[6].feedback.byKey.b-miss` | That is B missing. Then C kills B, and A still has one shot at C. | correct | B:items[6] |
| review-5.json | `.items[6].feedback.byKey.best` | C never misses, but C is shot at first. | correct | B:items[6] |
| review-5.json | `.items[6].explain.text` | C survives only if B misses ($\tfrac13$) and then A misses ($\tfrac23$). So $\tfrac29$: the best shot has the worst cha… | correct | B:items[6] |
| review-5.json | `.items[7].prose` | The envelope pairs are (£5, £10), (£10, £20) and (£20, £40), equally likely. You open one at random and see £10. | correct | B:items[7] |
| review-5.json | `.items[7].widget.accept` | £12.50 | correct | B:items[7] |
| review-5.json | `.items[7].feedback.correct` | $\tfrac{5 + 20}{2} = \text{£}12.50$. | correct | B:items[7] |
| review-5.json | `.items[7].feedback.generic` | Not quite right. List the cases in which you see £10. | correct | B:items[7] |
| review-5.json | `.items[7].feedback.byKey.keep` | That is keeping. The other holds £5 or £20, equally likely. | correct | B:items[7] |
| review-5.json | `.items[7].explain.text` | You see £10 in (£5, £10) and in (£10, £20), equally often. So switching gives £5 or £20, worth £12.50. At £40 you would… | correct | B:items[7] |
| review-5.json | `.items[8].prose` | A chord of the unit circle has its midpoint uniform in the disc. | correct | B:items[8] |
| review-5.json | `.items[8].widget.accept` | 3/4 = 0.75 | correct | B:items[8] |
| review-5.json | `.items[8].feedback.correct` | $\tfrac34$. | correct | B:items[8] |
| review-5.json | `.items[8].feedback.generic` | Not quite right. Solve $2\sqrt{1 - d^2} > 1$, then take the area share. | correct | B:items[8] |
| review-5.json | `.items[8].feedback.byKey.radius` | That is the radius procedure, $d$ uniform. A uniform midpoint gives $d^2$. | correct | B:items[8] |
| review-5.json | `.items[8].feedback.byKey.sqrt3` | That is the $\sqrt3$ threshold. | correct | B:items[8] |
| review-5.json | `.items[8].explain.text` | $2\sqrt{1 - d^2} > 1$ means $d < \tfrac{\sqrt3}{2}$. A uniform midpoint has $P(d < r) = r^2 = \tfrac34$. | correct | B:items[8] |
| review-5.json | `.items[9].prose` | L1's reroll game with an eight-sided die: keep the face in £, or pay £1 to roll again. You may reroll as often as you l… | correct | B:items[9] |
| review-5.json | `.items[9].widget.accept` | 11/2 = 5.5 | correct | B:items[9] |
| review-5.json | `.items[9].feedback.correct` | £5.50: keep 5 or more. | correct | B:items[9] |
| review-5.json | `.items[9].feedback.generic` | Not quite right. Try each threshold rule. | correct | B:items[9] |
| review-5.json | `.items[9].feedback.byKey.d6` | That is the six-sided game. | correct | B:items[9] |
| review-5.json | `.items[9].feedback.byKey.no-reroll` | That is never rerolling, $\tfrac92$. A £1 reroll pays on low faces. | correct | B:items[9] |
| review-5.json | `.items[9].explain.text` | Keeping 5 or more gives $\tfrac{5 + 6 + 7 + 8 - 4 \times 1}{4} = \text{£}5.50$. Then $V - c = 4.5$, so 5 is kept and 4 … | correct | B:items[9] |

## homework-5.json

### Bases

| key | basis |
|---|---|
| items[0] | Mosteller, Fifty Challenging Problems, no. 20 (three-cornered duel) and no. 25 (random chord); backward induction with each player best-responding; sim: puzzles-L5-concepts-r2.py:all six truel tests agree with the independent equilibrium solver; no tie between A's moves; chances add to 1; solution passes all 7 tests |
| items[1] | Casella and Berger ch. 7 (Lehmann-Scheffe, UMVUE of a uniform endpoint) and Goodman (1954) serial-number estimation; sim: puzzles-L5-concepts-r2.py:solution passes all 7 hidden tests; the range estimate averages exactly N (exhaustive); R itself is biased low |
| items[2] | gap symmetry; sim: puzzles-L5-concepts-r2.py:E[R] = (k-1)(N+1)/(k+1) exhaustive at N=50 and 12; R itself biased low |
| items[3] | von Neumann (1951); sim: puzzles-L5-concepts-r2.py:flips 9/2, 25/6, 4; 125/12; two bits with restart 100/9; direct method beats two bits |
| items[4] | sim: puzzles-L5-concepts-r2.py:weak B: air 11/40, aim at C 59/200; a hit on C leaves B first and A wins 3/8 |
| items[5] | Wald: 2 bits x 25/6 flips x 4/3 rounds; sim: puzzles-L5-concepts-r2.py:two bits with a restart 100/9; direct method 125/12 is faster |
| items[6] | sim: puzzles-L5-concepts-r2.py:102/11 |
| items[7] | sim: puzzles-L5-concepts-r2.py:three dice total 10: 27 rolls, 9 with a six, 1/3; unconditional 0.4213 |
| items[8] | sim: puzzles-L5-concepts-r2.py:switch unless 80: 125/3; always keep 35; the rule is the prior-optimal one |
| items[9] | sim: puzzles-L5-concepts-r2.py:reroll 20-sided at cost 1: value 91/6; threshold 14.17 |

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| homework-5.json | `.items[0].prose` | Write `truel(pa, pb, pc)` for the truel with best play. They fire in turn A, B, C. C never misses ($p_C = 1$ in every t… | correct | B:items[0] |
| homework-5.json | `.items[0].widget.how` | Check runs 7 hidden tests. Six compare the whole tuple exactly, including A's move. In two of them A should aim at C. T… | correct | B:items[0] |
| homework-5.json | `.items[0].feedback.correct` | Backward induction through the three turns, with every player choosing. | correct | B:items[0] |
| homework-5.json | `.items[0].feedback.generic` | Not quite right. Look at the first failing test. | correct | B:items[0] |
| homework-5.json | `.items[0].feedback.byKey.test-1` | Work backwards: value C's turn first, then B's, then A's. Each value is a triple of chances. | correct | B:items[0] |
| homework-5.json | `.items[0].feedback.byKey.test-5` | When B is weak, A may do better by aiming at C. Compare all three of A's moves. | correct | B:items[0] |
| homework-5.json | `.items[0].explain.text` | Work backwards: C kills the stronger rival, then B and A each pick their best move. At $(\tfrac15, \tfrac14, 1)$ A aims… | correct | B:items[0] |
| homework-5.json | `.items[1].prose` | Write `tank_estimates(serials)`, returning two unbiased estimates of $N$ as `Fraction`s. The first, $m + \tfrac{m}{k} -… | correct | B:items[1] |
| homework-5.json | `.items[1].widget.how` | Check runs 7 hidden tests. Five compare exact `Fraction`s, one on serials shifted by 100. One averages both estimates o… | correct | B:items[1] |
| homework-5.json | `.items[1].feedback.correct` | Both estimates, exact and unbiased. | correct | B:items[1] |
| homework-5.json | `.items[1].feedback.generic` | Not quite right. Look at the first failing test. | correct | B:items[1] |
| homework-5.json | `.items[1].feedback.byKey.test-1` | Check both formulas: $64 + 16 - 1 = 79$ and $41 \times \tfrac53 - 1 = \tfrac{202}{3}$. | correct | B:items[1] |
| homework-5.json | `.items[1].feedback.byKey.test-7` | The range needs two serials: raise `ValueError` when `len(serials) < 2`. | correct | B:items[1] |
| homework-5.json | `.items[1].explain.text` | The max-based estimate adds one average gap above the largest; the range-based one adds two, one at each end. Averaged … | correct | B:items[1] |
| homework-5.json | `.items[2].prose` | The numbers run from $a + 1$ to $a + N$, and you see $k$ of them. Derive the mean of the range $R$, one justified line … | correct | B:items[2] |
| homework-5.json | `.items[2].widget.lines[0].text` | The $k$ numbers seen leave $N - k$ unseen numbers, in $k + 1$ gaps. | correct | B:items[2] |
| homework-5.json | `.items[2].widget.lines[1].text` | By symmetry each gap has mean $\tfrac{N - k}{k + 1}$. | correct | B:items[2] |
| homework-5.json | `.items[2].widget.lines[2].text` | The range is the full span less the two end gaps: $R = (N - 1) - G_{\text{low}} - G_{\text{high}}$. | correct | B:items[2] |
| homework-5.json | `.items[2].widget.lines[3].text` | So $E[R] = N - 1 - \tfrac{2(N - k)}{k + 1} = \tfrac{(k - 1)(N + 1)}{k + 1}$. | correct | B:items[2] |
| homework-5.json | `.items[2].widget.lines[4].text` | Solving, $\hat N = R\,\tfrac{k + 1}{k - 1} - 1$ has mean $N$, whatever $a$ is. | correct | B:items[2] |
| homework-5.json | `.items[2].widget.lines[5].text` | The start $a$ cancels in $R$, so $R$ itself is unbiased for $N$. | correct | B:items[2] |
| homework-5.json | `.items[2].widget.lines[5].why` | The start cancels, but $R$ still misses the two end gaps, so it is too small on average. | correct | B:items[2] |
| homework-5.json | `.items[2].feedback.correct` | Gaps, equal means, two end gaps off, then solve. | correct | B:items[2] |
| homework-5.json | `.items[2].feedback.generic` | Not quite right. Begin with the unseen numbers and their gaps. | correct | B:items[2] |
| homework-5.json | `.items[2].feedback.byKey.d1` | You took $R$ as unbiased. It loses an average gap at each end. | correct | B:items[2] |
| homework-5.json | `.items[2].feedback.byKey.left-out` | Every line except the "R is unbiased" claim belongs. | correct | B:items[2] |
| homework-5.json | `.items[2].explain.text` | $R$ is the span from $a + 1$ to $a + N$ less the gap below the smallest and the gap above the largest. Each has mean $\… | correct | B:items[2] |
| homework-5.json | `.items[3].model` | **The pairing.** Flip the coin twice. If it shows HT, call it heads; if TH, call it tails. On HH or TT, throw the pair … | correct | B:items[3] |
| homework-5.json | `.items[3].rubric[0].text` | States the pairing: HT is heads, TH is tails, HH and TT start again | correct | B:items[3] |
| homework-5.json | `.items[3].rubric[1].text` | Explains fairness by independence: both kept outcomes have chance $pq$, whatever $p$ is | correct | B:items[3] |
| homework-5.json | `.items[3].rubric[2].text` | Gives the expected flips, $\tfrac{1}{pq}$ (4 for a fair coin), and the edge case $p = 0$ or 1 | correct | B:items[3] |
| homework-5.json | `.items[3].rubric[3].text` | Extends to three people with three equally likely strings (or bits), and states the cost, such as $\tfrac{1}{pq^2}$ | correct | B:items[3] |
| homework-5.json | `.items[3].rubric[4].text` | Speaks clearly: the method first, then why, then the cost, in under 5 minutes | correct | B:items[3] |
| homework-5.json | `.items[4].prose` | The truel again: they fire in turn A, B, C, and C never misses. Now A hits with $\tfrac15$ and B with $\tfrac14$. B and… | correct | B:items[4] |
| homework-5.json | `.items[4].widget.options[0].text` | Aim at C | correct | B:items[4] |
| homework-5.json | `.items[4].widget.options[1].why` | You carried over the last answer. With B this weak, C usually kills B, and A gets one shot at C. The air is worth only … | correct | B:items[4] |
| homework-5.json | `.items[4].widget.options[2].why` | If A hits B, C fires next and never misses. | correct | B:items[4] |
| homework-5.json | `.items[4].feedback.correct` | Aim at C: $\tfrac{59}{200}$ beats the air's $\tfrac{55}{200}$. | correct | B:items[4] |
| homework-5.json | `.items[4].feedback.generic` | Not quite right. Value all three moves with these accuracies. | correct | B:items[4] |
| homework-5.json | `.items[4].feedback.byKey.b` | You reused the answer for $(\tfrac13, \tfrac23)$. Recompute: here a hit on C leaves B firing first, and A still wins $\… | correct | B:items[4] |
| homework-5.json | `.items[4].explain.text` | Into the air: $\tfrac14 \cdot \tfrac{1/5}{2/5} + \tfrac34 \cdot \tfrac15 = \tfrac{11}{40}$. Aiming at C adds a hit bran… | correct | B:items[4] |
| homework-5.json | `.items[5].prose` | A coin lands heads with chance 0.6. To choose fairly among three people, you make two fair bits with the pairing trick.… | correct | B:items[5] |
| homework-5.json | `.items[5].widget.accept` | 100/9, about 11.1111 | correct | B:items[5] |
| homework-5.json | `.items[5].feedback.correct` | $2 \times \tfrac{25}{6} \times \tfrac43 = \tfrac{100}{9} \approx 11.1111$. | correct | B:items[5] |
| homework-5.json | `.items[5].feedback.generic` | Not quite right. Find the flips per bit, the bits per round, and the rounds. | correct | B:items[5] |
| homework-5.json | `.items[5].feedback.byKey.direct` | That is the three-flip method with exactly one head, $\tfrac{1}{pq^2}$. This method is slower. | correct | B:items[5] |
| homework-5.json | `.items[5].feedback.byKey.no-restart` | That is two bits once. A quarter of the rounds land on 11 and start again. | correct | B:items[5] |
| homework-5.json | `.items[5].explain.text` | Each fair bit costs $\tfrac{1}{0.24} = \tfrac{25}{6}$ flips, and a round uses two bits. Rounds succeed with $\tfrac34$,… | correct | B:items[5] |
| homework-5.json | `.items[6].prose` | The larger of two dice is 6. | correct | B:items[6] |
| homework-5.json | `.items[6].widget.accept` | 102/11, about 9.2727 | correct | B:items[6] |
| homework-5.json | `.items[6].feedback.correct` | $\tfrac{102}{11} \approx 9.2727$. | correct | B:items[6] |
| homework-5.json | `.items[6].feedback.generic` | Not quite right. List the eleven rolls with larger die 6. | correct | B:items[6] |
| homework-5.json | `.items[6].feedback.byKey.uniform` | You took the other die as uniform on 1 to 6. (6, 6) is one roll; (6, 2) and (2, 6) are two. | correct | B:items[6] |
| homework-5.json | `.items[6].explain.text` | Row 6 has totals 7 to 12, adding to 57. Column 6 above it has totals 7 to 11, adding to 45. Over eleven rolls the mean … | correct | B:items[6] |
| homework-5.json | `.items[7].prose` | Three dice total 10. | correct | B:items[7] |
| homework-5.json | `.items[7].widget.accept` | 1/3, about 0.3333 | correct | B:items[7] |
| homework-5.json | `.items[7].feedback.correct` | $\tfrac{9}{27} = \tfrac13$. | correct | B:items[7] |
| homework-5.json | `.items[7].feedback.generic` | Not quite right. Count the ordered rolls with total 10, then those with a six. | correct | B:items[7] |
| homework-5.json | `.items[7].feedback.byKey.unconditional` | That is the chance of a six with no condition, $1 - (\tfrac56)^3$. | correct | B:items[7] |
| homework-5.json | `.items[7].explain.text` | Total 10 comes up in 27 ordered rolls. Those with a six are the orders of (6, 1, 3) and (6, 2, 2): $6 + 3 = 9$. So the … | correct | B:items[7] |
| homework-5.json | `.items[8].prose` | The envelope pairs are (£10, £20), (£20, £40) and (£40, £80), equally likely. You open one at random. Your rule: switch… | correct | B:items[8] |
| homework-5.json | `.items[8].widget.accept` | 125/3, about £41.6667 | correct | B:items[8] |
| homework-5.json | `.items[8].feedback.correct` | $\tfrac{250}{6} = \tfrac{125}{3} \approx \text{£}41.67$. | correct | B:items[8] |
| homework-5.json | `.items[8].feedback.generic` | Not quite right. Go through all six equally likely cases. | correct | B:items[8] |
| homework-5.json | `.items[8].feedback.byKey.keep` | That is always keeping (or always switching). The rule gains by keeping only at £80. | correct | B:items[8] |
| homework-5.json | `.items[8].explain.text` | The six cases pay 20, 10, 40, 20, 80 and 80 under the rule. That averages $\tfrac{250}{6} \approx \text{£}41.67$, again… | correct | B:items[8] |
| homework-5.json | `.items[9].prose` | The reroll game with a 20-sided die: keep the face in £, or pay £1 to roll again. You may reroll as often as you like. | correct | B:items[9] |
| homework-5.json | `.items[9].widget.accept` | 91/6, about 15.1667 | correct | B:items[9] |
| homework-5.json | `.items[9].feedback.correct` | $\tfrac{91}{6} \approx \text{£}15.17$: keep 15 or more. | correct | B:items[9] |
| homework-5.json | `.items[9].feedback.generic` | Not quite right. Find the threshold $t$ with the largest value. | correct | B:items[9] |
| homework-5.json | `.items[9].feedback.byKey.no-reroll` | That is never rerolling. A £1 reroll pays on low faces. | correct | B:items[9] |
| homework-5.json | `.items[9].feedback.byKey.free` | That is a free reroll. At £1 you stop well below 20. | correct | B:items[9] |
| homework-5.json | `.items[9].explain.text` | Keeping 15 or more gives $\tfrac{105 - 14}{6} = \tfrac{91}{6}$. Then $V - c \approx 14.17$, so 15 is kept and 14 reroll… | correct | B:items[9] |

## Verdict counts

- correct: 2059
- wrong: 0
- imprecise: 3
- misleading: 0
- unverified: 0
- total rows: 2062
