# Claim ledger: series, levels 1 to 3 (audit series-1-3, round 1)

Stage 0 depth: definitions, rules, always / never / every / only claims, conventions, and every graded key, wrong option and slip. Script: `docs/reports/series-L1-3-concepts.py` (parts A to E).

Rows: 1182. correct 1174, imprecise 6, misleading 2, unverified 0.

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l1-spotting-the-rule | screens[2].prose | term; term-to-term rule takes each term to the next | correct | Pearson Edexcel A level Pure Year 2 ch. 3 s3.1 (school usage) |
| l1-spotting-the-rule | screens[3].explain | position-to-term rule reaches term 50 without the 49 before | correct | derivation: 4*50+3 |
| l1-spotting-the-rule | screens[5].explain | two terms alone could never fix the rule (3, 6 fits add 3 and double) | correct | derivation: both rules fit two terms |
| l1-spotting-the-rule | screens[6].prose | a sequence is a list of terms that follows a rule | correct | school definition (Pearson Edexcel A level Pure Year 2 ch. 3 s3.1); Spivak ch. 22 allows any function on the naturals, not needed at Stage 0 |
| l1-spotting-the-rule | screens[8].explain | halving: the position never reaches zero | correct | derivation: 8000/2^n > 0 |
| l1-spotting-the-rule | summary.ideas | two kinds of rule; test every pair of neighbours | correct | as above |
| l1-spotting-the-rule | quiz[1].explain | a constant list adds a fixed step (0) and multiplies by a fixed number (1) | correct | derivation |
| l1-spotting-the-rule | screens[0].widget.answer | key 21 | correct | script A: recomputed |
| l1-spotting-the-rule | screens[0].widget.wrong[plus-five] | slip 22: You added 5, the first number. The bars grow by 4 each time: 9 − 5 = 4. | correct | script A: slip value equals the named mistake |
| l1-spotting-the-rule | screens[0].widget.wrong[copy] | slip 17: You matched bar 4. The list keeps growing, so bar 5 is taller. | correct | script A: slip value equals the named mistake |
| l1-spotting-the-rule | screens[0].widget.wrong[plus-three] | slip 20: You added 3. Check a gap: 13 − 9 = 4, not 3. | correct | script A: slip value equals the named mistake |
| l1-spotting-the-rule | screens[1].widget.answer | key 5 | correct | script A: recomputed |
| l1-spotting-the-rule | screens[1].widget.wrong[six] | slip 6: You counted six positions. From position 1 to position 6 there are only five steps. | correct | script A: slip value equals the named mistake |
| l1-spotting-the-rule | screens[1].widget.wrong[one] | slip 1: Only one step changed size, but position 6 uses that step five times. | correct | script A: slip value equals the named mistake |
| l1-spotting-the-rule | screens[2].widget.answer | key -5 | correct | script A: recomputed |
| l1-spotting-the-rule | screens[2].widget.wrong[fifth] | slip -2: That is the term in position 5. Subtract 3 once more for position 6. | correct | script A: slip value equals the named mistake |
| l1-spotting-the-rule | screens[2].widget.wrong[stop] | slip 0: The rule does not stop at zero. Subtracting 3 from 1 gives −2. | correct | script A: slip value equals the named mistake |
| l1-spotting-the-rule | screens[2].widget.wrong[sign] | slip 5: You dropped the minus sign. The list keeps falling below zero: 1, −2, −5. | correct | script A: slip value equals the named mistake |
| l1-spotting-the-rule | screens[2].widget.wrong[extra] | slip -8: You subtracted 3 three times after the 1. Position 6 is only two steps after position 4. | correct | script A: slip value equals the named mistake |
| l1-spotting-the-rule | screens[3].widget.answer | key 203 | correct | script A: recomputed |
| l1-spotting-the-rule | screens[3].widget.wrong[no-three] | slip 200: You multiplied 50 by 4 but left off the 3. Check position 1: $4 \times 1 + 3 = 7$. | correct | script A: slip value equals the named mistake |
| l1-spotting-the-rule | screens[3].widget.wrong[fifty-steps] | slip 207: You added fifty 4s to the first term. Position 50 is only 49 steps after position 1. | correct | script A: slip value equals the named mistake |
| l1-spotting-the-rule | screens[3].widget.wrong[add-four] | slip 54: You added 4 to the position. The rule multiplies the position by 4, then adds 3. | correct | script A: slip value equals the named mistake |
| l1-spotting-the-rule | screens[4].widget.answer | key 144 | correct | script A: recomputed |
| l1-spotting-the-rule | screens[4].widget.wrong[double] | slip 24: You doubled 12. The rule multiplies the position by itself, not by 2. | correct | script A: slip value equals the named mistake |
| l1-spotting-the-rule | screens[4].widget.wrong[eleventh] | slip 121: That is $11 \times 11$, the term in position 11. Use 12. | correct | script A: slip value equals the named mistake |
| l1-spotting-the-rule | screens[4].widget.wrong[next-gap] | slip 36: You added the next gap, 11, to 25. That gives position 6, not position 12. | correct | script A: slip value equals the named mistake |
| l1-spotting-the-rule | screens[5].widget.options[first-two] | wrong option: 27 / You read the rule from the first two terms, add 3. From 6 to 12 adds 6, so add 3 fails. | correct | wrong under every reading; why line checked |
| l1-spotting-the-rule | screens[5].widget.options[second-gap] | wrong option: 30 / You added 6, the second gap. The gaps change: 3, 6, then 12. | correct | wrong under every reading; why line checked |
| l1-spotting-the-rule | screens[5].widget.options[last-gap] | wrong option: 36 / You added 12, the last gap. Each gap doubles too, so the next gap is 24. | correct | wrong under every reading; why line checked |
| l1-spotting-the-rule | screens[5].widget.options[double] | key: 48 | correct | derivation on reading; figures in script A or C |
| l1-spotting-the-rule | screens[6].widget.options[pos] | key: Term $= 10 - 2n$ | correct | derivation on reading; figures in script A or C |
| l1-spotting-the-rule | screens[6].widget.options[add] | wrong option: Subtract 2 from the last term / That says how to get the next term from this one. It is a term-t | correct | wrong under every reading; why line checked |
| l1-spotting-the-rule | screens[6].widget.options[double] | wrong option: Double the last term / That needs the term before. A position-to-term rule needs only the positi | correct | wrong under every reading; why line checked |
| l1-spotting-the-rule | screens[6].widget.options[list] | wrong option: 8, 6, 4, 2, … / That is the sequence itself. A rule says how its terms are made. | correct | wrong under every reading; why line checked |
| l1-spotting-the-rule | screens[7].widget.answer | key 48.25 | correct | script A: recomputed |
| l1-spotting-the-rule | screens[7].widget.wrong[eight-steps] | slip 48.0: You took eight steps of £0.25. The 8th order is seven steps below the 1st. | correct | script A: slip value equals the named mistake |
| l1-spotting-the-rule | screens[7].widget.wrong[up] | slip 51.75: The orders fall. Subtract the steps from £50.00 rather than adding them. | correct | script A: slip value equals the named mistake |
| l1-spotting-the-rule | screens[7].widget.wrong[up8] | slip 52.0: The orders fall, and the 8th is only seven steps from the 1st. | correct | script A: slip value equals the named mistake |
| l1-spotting-the-rule | screens[8].widget.answer | key 1000 | correct | script A: recomputed |
| l1-spotting-the-rule | screens[8].widget.wrong[first-gap] | slip -2000: You subtracted £4,000.00, the first gap. The second gap is only £2,000.00, so the rule is not subt | correct | script A: slip value equals the named mistake |
| l1-spotting-the-rule | screens[8].widget.wrong[last-gap] | slip 0: You subtracted £2,000.00, the last gap. The gaps halve too, so the rule is halve. | correct | script A: slip value equals the named mistake |
| l1-spotting-the-rule | screens[8].widget.wrong[quarter] | slip 500: You halved twice. Trade 4 comes one loss after trade 3. | correct | script A: slip value equals the named mistake |
| l1-spotting-the-rule | quiz[0].widget.answer | key 30 | correct | script A: recomputed |
| l1-spotting-the-rule | quiz[0].widget.wrong[add-two] | slip 25: You added 2, the first term. The gap between neighbours is 7. | correct | script A: slip value equals the named mistake |
| l1-spotting-the-rule | quiz[0].widget.wrong[seven] | slip 7: 7 is the step. Add it to the last term, 23. | correct | script A: slip value equals the named mistake |
| l1-spotting-the-rule | quiz[1].widget.options[add0] | key: Add 0 | correct | derivation on reading; figures in script A or C |
| l1-spotting-the-rule | quiz[1].widget.options[times1] | key: Multiply by 1 | correct | derivation on reading; figures in script A or C |
| l1-spotting-the-rule | quiz[1].widget.options[add7] | wrong option: Add 7 / Adding 7 to 7 gives 14. The terms never change, so nothing is added. | correct | wrong under every reading; why line checked |
| l1-spotting-the-rule | quiz[1].widget.options[times7] | wrong option: Multiply by 7 / Multiplying 7 by 7 gives 49. Only multiplying by 1 keeps 7. | correct | wrong under every reading; why line checked |
| l1-spotting-the-rule | quiz[2].widget.answer | key -5 | correct | script A: recomputed |
| l1-spotting-the-rule | quiz[2].widget.wrong[bracket] | slip 35: You worked out $(10 - 3) \times 5$. The rule multiplies $n$ by 3 first, then subtracts from 10. | correct | script A: slip value equals the named mistake |
| l1-spotting-the-rule | quiz[2].widget.wrong[sign] | slip 5: $10 - 15$ is below zero: −5, not 5. | correct | script A: slip value equals the named mistake |
| l1-spotting-the-rule | quiz[2].widget.wrong[fourth] | slip -2: That is position 4. Put $n = 5$. | correct | script A: slip value equals the named mistake |
| l1-spotting-the-rule | quiz[3].widget.options[add10] | wrong option: 55 / You used add 10 from the first two terms. From 15 to 45 adds 30, so add 10 fails. | correct | wrong under every reading; why line checked |
| l1-spotting-the-rule | quiz[3].widget.options[add30] | wrong option: 75 / You added 30, the last gap. The gaps grow too, so add 30 fails next time. | correct | wrong under every reading; why line checked |
| l1-spotting-the-rule | quiz[3].widget.options[times3] | key: 135 | correct | derivation on reading; figures in script A or C |
| l1-spotting-the-rule | quiz[3].widget.options[add45] | wrong option: 90 / You doubled 45. Check the first pair: 5 doubled is 10, not 15. | correct | wrong under every reading; why line checked |
| l2-any-term | screens[2].prose | u_n notation, first term a, common difference d, arithmetic | correct | Pearson Edexcel A level Pure Year 2 ch. 3 s3.1 |
| l2-any-term | screens[4].explain | positions are whole numbers, so 100 (n = 32 2/3) is not a term | correct | derivation |
| l2-any-term | screens[6].explain | always test a formula at n = 1; a + nd is one step too far | correct | derivation: u_1 must equal a |
| l2-any-term | screens[7].widget | derivation u_n = a + (n-1)d = dn + (a-d) | correct | Pearson Edexcel A level Pure Year 2 ch. 3 s3.1 |
| l2-any-term | summary.ideas[1] | u_n = a + (n-1)d, first term index 1 | correct | Pearson Edexcel A level Pure Year 2 ch. 3 s3.1; convention stated (u_1 = a) |
| l2-any-term | summary.ideas[2] | a number is a term only when solving for n gives a whole number | imprecise | necessary but not sufficient: n must be a positive whole number (n = 0 gives 2 for 3n + 2, which is no term). Finding 8 |
| l2-any-term | screens[8].prose | savings pot: £1,500 at end of month 1, £200 at each later month end (payment timing stated) | correct | convention stated in the item |
| l2-any-term | screens[0].widget.answer | key 5 | correct | script A: recomputed |
| l2-any-term | screens[0].widget.wrong[six] | slip 6: You counted six bars. Between six bars there are only five gaps, so five 3s. | correct | script A: slip value equals the named mistake |
| l2-any-term | screens[0].widget.wrong[nineteen] | slip 19: 19 is the term itself. Count how many 3s took 4 up to 19. | correct | script A: slip value equals the named mistake |
| l2-any-term | screens[1].widget.answer | key 121 | correct | script A: recomputed |
| l2-any-term | screens[1].widget.wrong[forty] | slip 124: You added forty 3s. The caption always adds one fewer 3 than the position. | correct | script A: slip value equals the named mistake |
| l2-any-term | screens[1].widget.wrong[times] | slip 120: You multiplied 40 by 3 and lost the start. The terms begin at 4. | correct | script A: slip value equals the named mistake |
| l2-any-term | screens[1].widget.wrong[plus] | slip 43: You added 3 to the position. Each step after the first adds another 3. | correct | script A: slip value equals the named mistake |
| l2-any-term | screens[2].widget.answer | key 65 | correct | script A: recomputed |
| l2-any-term | screens[2].widget.wrong[ten-steps] | slip 71: You added ten 6s. Position 10 is nine steps after position 1. | correct | script A: slip value equals the named mistake |
| l2-any-term | screens[2].widget.wrong[no-start] | slip 60: You multiplied 10 by 6 and dropped the first term, 11. | correct | script A: slip value equals the named mistake |
| l2-any-term | screens[2].widget.wrong[swap] | slip 105: You swapped the start and the step: $6 + 9 \times 11$. The start is 11 and the step is 6. | correct | script A: slip value equals the named mistake |
| l2-any-term | screens[3].widget.answer | key -6 | correct | script A: recomputed |
| l2-any-term | screens[3].widget.wrong[fifteen] | slip -10: You took fifteen steps. $u_{15}$ is fourteen steps after $u_1$. | correct | script A: slip value equals the named mistake |
| l2-any-term | screens[3].widget.wrong[sign] | slip 106: You added 56. The common difference is −4, so the terms fall. | correct | script A: slip value equals the named mistake |
| l2-any-term | screens[3].widget.wrong[sign15] | slip 110: You added fifteen 4s. The steps are −4, and there are fourteen of them. | correct | script A: slip value equals the named mistake |
| l2-any-term | screens[3].widget.wrong[drop] | slip 6: $50 - 56$ is below zero: −6, not 6. | correct | script A: slip value equals the named mistake |
| l2-any-term | screens[4].widget.options[u32] | wrong option: Yes, it is $u_{32}$ / Check it: $u_{32} = 3 \times 32 + 2 = 98$. That is 2 short of 100. | correct | wrong under every reading; why line checked |
| l2-any-term | screens[4].widget.options[u33] | wrong option: Yes, it is $u_{33}$ / You rounded $98 \div 3$ up. But $u_{33} = 101$, and a term must equal 100  | correct | wrong under every reading; why line checked |
| l2-any-term | screens[4].widget.options[u20] | wrong option: Yes, it is $u_{20}$ / You divided 100 by the first term, 5. Check: $u_{20} = 3 \times 20 + 2 = 6 | correct | wrong under every reading; why line checked |
| l2-any-term | screens[4].widget.options[no] | key: No, it is not a term | correct | derivation on reading; figures in script A or C |
| l2-any-term | screens[5].widget.answer | key 5 | correct | script A: recomputed |
| l2-any-term | screens[5].widget.wrong[no-divide] | slip 25: 25 is the whole rise from $u_3$ to $u_8$. It is shared over several steps. | correct | script A: slip value equals the named mistake |
| l2-any-term | screens[5].widget.wrong[terms] | slip 4.1667: You divided by 6, the number of terms shown. Six terms have five gaps. | correct | script A: slip value equals the named mistake |
| l2-any-term | screens[5].widget.wrong[eight] | slip 3.125: You divided by 8. Only positions 3 to 8 are involved: five steps. | correct | script A: slip value equals the named mistake |
| l2-any-term | screens[6].widget.options[a-nd] | wrong option: $4 + 3n$ / You added $n$ steps of 3 to the first term. At $n = 1$ that gives 7, which is $u_2$.  | correct | wrong under every reading; why line checked |
| l2-any-term | screens[6].widget.options[swap] | wrong option: $4n + 3$ / You multiplied $n$ by the first term and added the difference. The step of 3 should m | correct | wrong under every reading; why line checked |
| l2-any-term | screens[6].widget.options[add-d] | wrong option: $n + 3$ / You added the difference to $n$. Each step adds 3, so $n$ must be multiplied by 3. | correct | wrong under every reading; why line checked |
| l2-any-term | screens[6].widget.options[right] | key: $3n + 1$ | correct | derivation on reading; figures in script A or C |
| l2-any-term | screens[8].widget.answer | key 6100 | correct | script A: recomputed |
| l2-any-term | screens[8].widget.wrong[a-nd] | slip 6300: You added 24 deposits. Month 24 is 23 deposits after month 1. | correct | script A: slip value equals the named mistake |
| l2-any-term | screens[8].widget.wrong[no-start] | slip 4800: You counted only the £200.00 payments. Add them to the £1,500.00 already there. | correct | script A: slip value equals the named mistake |
| l2-any-term | screens[8].widget.wrong[no-start2] | slip 4600: You left out the first £1,500.00. The pot starts there. | correct | script A: slip value equals the named mistake |
| l2-any-term | screens[9].widget.answer | key 44 | correct | script A: recomputed |
| l2-any-term | screens[9].widget.wrong[m43] | slip 43: Month 43 holds $1500 + 42 \times 200 = 9900$. That is still £100.00 short. | correct | script A: slip value equals the named mistake |
| l2-any-term | screens[9].widget.wrong[m50] | slip 50: You divided £10,000.00 by £200.00. The pot already starts with £1,500.00. | correct | script A: slip value equals the named mistake |
| l2-any-term | screens[9].widget.wrong[m42] | slip 42: You found $n - 1 = 42.5$ and rounded down. You need $n - 1 = 43$ steps, so $n = 44$. | correct | script A: slip value equals the named mistake |
| l2-any-term | quiz[0].widget.options[a-nd] | wrong option: $9 + 5n$ / You added $n$ steps to the first term. At $n = 1$ it gives 14, which is $u_2$. | correct | wrong under every reading; why line checked |
| l2-any-term | quiz[0].widget.options[right] | key: $5n + 4$ | correct | derivation on reading; figures in script A or C |
| l2-any-term | quiz[0].widget.options[swap] | wrong option: $9n + 5$ / You multiplied $n$ by the first term. The difference, 5, multiplies $n$. | correct | wrong under every reading; why line checked |
| l2-any-term | quiz[0].widget.options[add] | wrong option: $n + 5$ / You added the difference to $n$. At $n = 1$ that gives 6, not 9. | correct | wrong under every reading; why line checked |
| l2-any-term | quiz[1].widget.answer | key -13 | correct | script A: recomputed |
| l2-any-term | quiz[1].widget.wrong[twelve] | slip -16: You took twelve steps. $u_{12}$ is eleven steps after $u_1$. | correct | script A: slip value equals the named mistake |
| l2-any-term | quiz[1].widget.wrong[sign] | slip 53: You added 33. The difference is −3, so the terms fall. | correct | script A: slip value equals the named mistake |
| l2-any-term | quiz[1].widget.wrong[sign2] | slip 13: d is negative, so 11 × (−3) is −33, and 20 − 33 is below zero. A positive 13 takes 33 − 20, the wrong | correct | script A: slip value equals the named mistake |
| l2-any-term | quiz[2].widget.answer | key 5 | correct | script A: recomputed |
| l2-any-term | quiz[2].widget.wrong[whole] | slip 20: 20 is the whole rise. It is shared over $9 - 5 = 4$ steps. | correct | script A: slip value equals the named mistake |
| l2-any-term | quiz[2].widget.wrong[terms] | slip 4: You divided by 5, the number of terms from $u_5$ to $u_9$. There are only 4 gaps. | correct | script A: slip value equals the named mistake |
| l2-any-term | quiz[3].widget.answer | key 20 | correct | script A: recomputed |
| l2-any-term | quiz[3].widget.wrong[steps] | slip 19: 19 is the number of steps from 7 to 102. The position is one more: 20. | correct | script A: slip value equals the named mistake |
| l2-any-term | quiz[3].widget.wrong[over] | slip 21: $u_{21} = 107$. Solve $5n + 2 = 102$ exactly. | correct | script A: slip value equals the named mistake |
| l3-multiplying-each-time | screens[1].explain | gaps match only at multiplier 1; away from 1 the dots always curve | correct | derivation: gaps a r^k (r-1), equal iff r = 1 (slider 0.5 to 1.5) |
| l3-multiplying-each-time | screens[2].prose | geometric: multiply by the same common ratio r | correct | Pearson Edexcel A level Pure Year 2 ch. 3 s3.3 |
| l3-multiplying-each-time | screens[2].explain | a curve hints at multiplying, only a common ratio proves it | correct | derivation |
| l3-multiplying-each-time | screens[5].explain | any ratio between -1 and 0 zigzags in to 0 | correct | Spivak, Calculus ch. 22 (r^n -> 0 for |r| < 1) |
| l3-multiplying-each-time | screens[6].explain | power applies to r alone; powers before multiplication | correct | order of operations |
| l3-multiplying-each-time | screens[7].explain | u_n = a r^(n-1), check n = 1 gives a | correct | Pearson Edexcel A level Pure Year 2 ch. 3 s3.3; first term index 1, as the course defines it |
| l3-multiplying-each-time | screens[8].explain | a 5% rise multiplies by 1.05: dividends geometric | correct | derivation |
| l3-multiplying-each-time | summary.ideas | arithmetic dots on a line, geometric dots curve | correct | true for r != 1, shown on screen 1 |
| l3-multiplying-each-time | quiz[0].explain | halving shrinks towards zero but never reaches it | correct | derivation |
| l3-multiplying-each-time | screens[0].widget.answer | key 162 | correct | script A: recomputed |
| l3-multiplying-each-time | screens[0].widget.wrong[add-gap] | slip 90: You added 36, the last gap. The gaps grow too: 4, 12, 36, then 108. | correct | script A: slip value equals the named mistake |
| l3-multiplying-each-time | screens[0].widget.wrong[double] | slip 108: You doubled 54. Each bar is three times the one before. | correct | script A: slip value equals the named mistake |
| l3-multiplying-each-time | screens[1].widget.options[one] | key: Only at 1, where the dots are flat | correct | derivation on reading; figures in script A or C |
| l3-multiplying-each-time | screens[1].widget.options[all] | wrong option: At every multiplier / At 1.5 the rises are 2, 3 and 4.5. Growing rises bend the dots into a curv | correct | wrong under every reading; why line checked |
| l3-multiplying-each-time | screens[1].widget.options[above] | wrong option: At any multiplier above 1 / Above 1 each rise is bigger than the last, so the dots curve upwards | correct | wrong under every reading; why line checked |
| l3-multiplying-each-time | screens[1].widget.options[below] | wrong option: At any multiplier below 1 / Below 1 each fall is smaller than the last, so the dots flatten out  | correct | wrong under every reading; why line checked |
| l3-multiplying-each-time | screens[2].widget.options[b] | key: B | correct | derivation on reading; figures in script A or C |
| l3-multiplying-each-time | screens[2].widget.options[a] | wrong option: A / A's rises are all the same, 3 each time. A fixed rise is a common difference, so A is arithm | correct | wrong under every reading; why line checked |
| l3-multiplying-each-time | screens[2].widget.options[neither] | wrong option: Neither: geometric sequences double / The ratio need not be 2. B multiplies by 1.5 each time. | correct | wrong under every reading; why line checked |
| l3-multiplying-each-time | screens[2].widget.options[both] | wrong option: Both, since both climb / Climbing is not the test. A adds 3 each step; only B multiplies. | correct | wrong under every reading; why line checked |
| l3-multiplying-each-time | screens[3].widget.answer | key 1.5 | correct | script A: recomputed |
| l3-multiplying-each-time | screens[3].widget.wrong[diff] | slip 1: You subtracted: $3 - 2 = 1$. That is a gap, and B's gaps change. Divide instead. | correct | script A: slip value equals the named mistake |
| l3-multiplying-each-time | screens[3].widget.wrong[flip] | slip 0.6667: You divided the wrong way: $2 \div 3$. Divide each term by the one before it. | correct | script A: slip value equals the named mistake |
| l3-multiplying-each-time | screens[4].widget.answer | key 384 | correct | script A: recomputed |
| l3-multiplying-each-time | screens[4].widget.wrong[eight] | slip 768: You doubled eight times. Position 8 is seven steps after position 1. | correct | script A: slip value equals the named mistake |
| l3-multiplying-each-time | screens[4].widget.wrong[seven] | slip 192: That is $u_7$. Double once more. | correct | script A: slip value equals the named mistake |
| l3-multiplying-each-time | screens[4].widget.wrong[add] | slip 24: You added 3 each time, the first gap. Each term doubles, so the gaps grow. | correct | script A: slip value equals the named mistake |
| l3-multiplying-each-time | screens[5].widget.answer | key -0.5 | correct | script A: recomputed |
| l3-multiplying-each-time | screens[5].widget.wrong[sign] | slip 0.5: The ratio is negative, so the sign flips every step. $u_5 = 1$ is positive, so $u_6$ is negative. | correct | script A: slip value equals the named mistake |
| l3-multiplying-each-time | screens[5].widget.wrong[u5] | slip 1: That is $u_5$. Multiply by −0.5 once more. | correct | script A: slip value equals the named mistake |
| l3-multiplying-each-time | screens[5].widget.wrong[add] | slip -14: You subtracted the last gap, 6, twice: $-2 - 6 - 6 = -14$. The gaps shrink and flip sign: each term  | correct | script A: slip value equals the named mistake |
| l3-multiplying-each-time | screens[5].widget.wrong[times-two] | slip -8: You multiplied by $-2$: $-2 \times (-2) = 4$, then $4 \times (-2) = -8$. Dividing, $-8 \div 16 = -0.5 | correct | script A: slip value equals the named mistake |
| l3-multiplying-each-time | screens[6].widget.options[right] | key: $3 \times 2^4$ | correct | derivation on reading; figures in script A or C |
| l3-multiplying-each-time | screens[6].widget.options[bracket] | wrong option: $(3 \times 2)^4$ / You multiplied 3 by 2 first, then raised the result. Only $r$ is repeated: th | correct | wrong under every reading; why line checked |
| l3-multiplying-each-time | screens[6].widget.options[extra] | wrong option: $3 \times 2^5$ / You used the position as the power. That gives 96, one doubling too many. | correct | wrong under every reading; why line checked |
| l3-multiplying-each-time | screens[6].widget.options[arith] | wrong option: $3 + 4 \times 2$ / You used the arithmetic rule, adding 2 each time. This sequence multiplies by | correct | wrong under every reading; why line checked |
| l3-multiplying-each-time | screens[7].widget.answer | key 5\cdot3^{n-1} and accept list | correct | derivation: tested at n or x = 1, 2, 3 |
| l3-multiplying-each-time | screens[7].widget.wrong[power-n] | slip 5\cdot3^{n}: You used $n$ factors of 3. At $n = 1$ that gives 15, which is $u_2$. | correct | derivation: not equal to the key; feedback value checked |
| l3-multiplying-each-time | screens[7].widget.wrong[bracket] | slip 15^{n-1}: You raised $5 \times 3$ to the power. Only the 3 is repeated; the 5 appears once. | correct | derivation: not equal to the key; feedback value checked |
| l3-multiplying-each-time | screens[7].widget.wrong[arith] | slip 5+3(n-1): That adds 3 each step. This sequence multiplies by 3. | correct | derivation: not equal to the key; feedback value checked |
| l3-multiplying-each-time | screens[8].widget.answer | key 1.69 | correct | script A: recomputed |
| l3-multiplying-each-time | screens[8].widget.wrong[eight] | slip 1.77: You applied eight rises. Year 8 is seven years after year 1. | correct | script A: slip value equals the named mistake |
| l3-multiplying-each-time | screens[8].widget.wrong[simple] | slip 1.62: You added 6p a year, 5% of £1.20. Each rise is 5% of the latest dividend, so the rises grow. | correct | script A: slip value equals the named mistake |
| l3-multiplying-each-time | screens[9].widget.answer | key 136.5 | correct | script A: recomputed |
| l3-multiplying-each-time | screens[9].widget.wrong[same] | slip 0: You treated 1% as a fixed £200.00 a month. Each 1% is of a bigger balance than the last. | correct | script A: slip value equals the named mistake |
| l3-multiplying-each-time | screens[9].widget.wrong[gain] | slip 2536.5: That is B's whole gain. Subtract A's balance, £22,400.00, from B's. | correct | script A: slip value equals the named mistake |
| l3-multiplying-each-time | quiz[0].widget.answer | key 500 | correct | script A: recomputed |
| l3-multiplying-each-time | quiz[0].widget.wrong[three] | slip 1000: That is three halvings. Halve once more. | correct | script A: slip value equals the named mistake |
| l3-multiplying-each-time | quiz[0].widget.wrong[five] | slip 250: That is five halvings: one loss too many. | correct | script A: slip value equals the named mistake |
| l3-multiplying-each-time | quiz[0].widget.wrong[subtract] | slip 0: You took off £2,000.00 a time. Each loss halves what is left, so the cuts shrink. | correct | script A: slip value equals the named mistake |
| l3-multiplying-each-time | quiz[1].widget.answer | key 0.75 | correct | script A: recomputed |
| l3-multiplying-each-time | quiz[1].widget.wrong[diff] | slip -16: You subtracted. The gaps are −16 then −12, so they change. Divide instead. | correct | script A: slip value equals the named mistake |
| l3-multiplying-each-time | quiz[1].widget.wrong[flip] | slip 1.3333: You divided the wrong way. Divide each term by the one before: $48 \div 64$. | correct | script A: slip value equals the named mistake |
| l3-multiplying-each-time | quiz[2].widget.options[right] | key: They alternate in sign and close in on 0 | correct | derivation on reading; figures in script A or C |
| l3-multiplying-each-time | quiz[2].widget.options[grow] | wrong option: They alternate in sign and grow / Multiplying by −0.5 halves the size each step, so the terms sh | correct | wrong under every reading; why line checked |
| l3-multiplying-each-time | quiz[2].widget.options[neg] | wrong option: They all become negative / Each multiplication by a negative number flips the sign, so the signs | correct | wrong under every reading; why line checked |
| l3-multiplying-each-time | quiz[2].widget.options[settle] | wrong option: They settle at −5 / −5 is only $u_2$. The next term is 2.5, then −1.25. | correct | wrong under every reading; why line checked |
| l3-multiplying-each-time | quiz[3].widget.options[geo] | key: $2, 6, 18, 54$ | correct | derivation on reading; figures in script A or C |
| l3-multiplying-each-time | quiz[3].widget.options[arith] | wrong option: $2, 6, 10, 14$ / This adds 4 each time: a common difference, so it is arithmetic. | correct | wrong under every reading; why line checked |
| l3-multiplying-each-time | quiz[3].widget.options[squares] | wrong option: $1, 4, 9, 16$ / These are square numbers. $4 \div 1 = 4$ but $9 \div 4 = 2.25$, so there is no c | correct | wrong under every reading; why line checked |
| l3-multiplying-each-time | quiz[3].widget.options[first-two] | wrong option: $3, 6, 9, 12$ / 6 is double 3, but 9 is not double 6. This adds 3 each time. | correct | wrong under every reading; why line checked |
| l4-last-step | screens[2].prose | recurrence relation u_(n+1) = 2u_n - 3 with u_1 | correct | Pearson Edexcel A level Pure Year 2 ch. 3 s3.6 |
| l4-last-step | screens[2].explain | a recurrence cannot jump ahead; needs a starting term | correct | definition |
| l4-last-step | screens[3].explain | arithmetic: u_(n+1) = u_n + d; geometric: u_(n+1) = r u_n; either needs u_1 | correct | Pearson Edexcel A level Pure Year 2 ch. 3 s3.6 |
| l4-last-step | screens[4].explain | 0.6u + 12: every term moves 40% of the way to 30, without passing it | correct | derivation: gap x 0.6, same sign |
| l4-last-step | screens[5].prose | fixed point: a value the rule leaves alone | correct | definition |
| l4-last-step | screens[5].widget.options[any] | a fixed point is always the limit: false | correct | derivation: gap doubles for 2u - 10 |
| l4-last-step | screens[7].widget | if terms settle at L then L = 0.5L + 10 | correct | Spivak, Calculus ch. 22 (limit of u_(n+1) equals limit of u_n; rule continuous) |
| l4-last-step | screens[7].explain | L = f(L) finds where terms would settle; the gap check says whether they do | correct | derivation |
| l4-last-step | screens[8].prose | loan: interest added first, then payment; B_0 = 5000 | correct | convention stated |
| l4-last-step | screens[9].explain | 1.01B - 200 pushes terms away from its fixed point 20000 | correct | derivation: gap x 1.01 |
| l4-last-step | summary.ideas[1] | if terms settle at L the sequence converges to L and L = f(L) | correct | Spivak, Calculus ch. 22; needs f continuous, true of every rule in the course |
| l4-last-step | summary.ideas[2] | terms settle only when each step shrinks the gap; otherwise they run away | imprecise | a = -1 neither settles nor runs away (script E3); a start at L settles for any a. Finding 3 |
| l4-last-step | summary.formula | u_(n+1) = a u_n + b gives L = b/(1-a); towards L only when -1 < a < 1 | correct | derivation: gap_n = gap_1 a^(n-1) |
| l4-last-step | quiz[3].explain | unless they start at the fixed point, terms settle only when the multiplier is between -1 and 1 | correct | derivation |
| l4-last-step | screens[0].widget.rows | table key 60, 40, 30 | correct | derivation: halve then add 10 |
| l4-last-step | screens[1].widget.answer | key 20 | correct | script A: recomputed |
| l4-last-step | screens[1].widget.wrong[add] | slip 10: 10 is the amount added each step. The terms settle higher than that. | correct | script A: slip value equals the named mistake |
| l4-last-step | screens[1].widget.wrong[zero] | slip 0: Halving alone would shrink to 0. The add of 10 keeps the terms up. | correct | script A: slip value equals the named mistake |
| l4-last-step | screens[1].widget.wrong[half] | slip 50: 50 is half of the top start. Slide the start and watch term 10. | correct | script A: slip value equals the named mistake |
| l4-last-step | screens[2].widget.answer | key 19 | correct | script A: recomputed |
| l4-last-step | screens[2].widget.wrong[u3] | slip 11: That is $u_3$. Apply the rule once more. | correct | script A: slip value equals the named mistake |
| l4-last-step | screens[2].widget.wrong[n-in] | slip 3: You put $n = 3$ into the rule. The rule takes the last term, $u_3 = 11$, not its position. | correct | script A: slip value equals the named mistake |
| l4-last-step | screens[2].widget.wrong[order] | slip -2: You subtracted 3 before doubling: $2 \times (5 - 3) = 4$, then 2, then $-2$. The rule doubles first,  | correct | script A: slip value equals the named mistake |
| l4-last-step | screens[2].widget.wrong[u5] | slip 35: That is $u_5$: one step too many. | correct | script A: slip value equals the named mistake |
| l4-last-step | screens[3].widget.options[right] | key: $u_{n+1} = u_n + 4$, with $u_1 = 7$ | correct | derivation on reading; figures in script A or C |
| l4-last-step | screens[3].widget.options[no-start] | wrong option: $u_{n+1} = u_n + 4$ / That rule also makes 1, 5, 9, 13. Without a starting term it fits many seq | correct | wrong under every reading; why line checked |
| l4-last-step | screens[3].widget.options[times] | wrong option: $u_{n+1} = 4u_n + 3$, with $u_1 = 7$ / You used the position formula's numbers. From 7 this give | correct | wrong under every reading; why line checked |
| l4-last-step | screens[3].widget.options[swap] | wrong option: $u_{n+1} = u_n + 7$, with $u_1 = 4$ / You swapped the start and the step. That gives 4, 11, 18. | correct | wrong under every reading; why line checked |
| l4-last-step | screens[4].widget.answer | key 30 | correct | script A: recomputed |
| l4-last-step | screens[4].widget.wrong[add] | slip 12: 12 is the amount added each step. The dots climb well past 12. | correct | script A: slip value equals the named mistake |
| l4-last-step | screens[4].widget.wrong[divide] | slip 20: You divided 12 by 0.6. Test it: $0.6 \times 20 + 12 = 24$, not 20. | correct | script A: slip value equals the named mistake |
| l4-last-step | screens[4].widget.wrong[last] | slip 29.6: That is about where term 10 is. The terms keep creeping up towards an exact value. | correct | script A: slip value equals the named mistake |
| l4-last-step | screens[5].widget.options[no] | key: No: the gap from 10 doubles every step | correct | derivation on reading; figures in script A or C |
| l4-last-step | screens[5].widget.options[later] | wrong option: Yes, after enough terms / The gaps from 10 are 2, 4, 8, 16. They grow, so the terms never come b | correct | wrong under every reading; why line checked |
| l4-last-step | screens[5].widget.options[any] | wrong option: Yes: a number the rule leaves alone is always the limit / That holds only when the terms move to | correct | wrong under every reading; why line checked |
| l4-last-step | screens[5].widget.options[nearly] | wrong option: They start near 10, so they stay near it / They start 2 away, but each step doubles that gap. | correct | wrong under every reading; why line checked |
| l4-last-step | screens[6].widget.answer | key 32 | correct | script A: recomputed |
| l4-last-step | screens[6].widget.wrong[n-in] | slip 5: You put the position, 2, into the rule: $3 \times 2 - 1 = 5$. The rule takes the previous term, $u_2$, | correct | script A: slip value equals the named mistake |
| l4-last-step | screens[6].widget.wrong[u2] | slip 11: That is $u_2$. Apply the rule once more, to 11. | correct | script A: slip value equals the named mistake |
| l4-last-step | screens[6].widget.wrong[skip] | slip 35: You left out the −1 on the first step: $3 \times 4 = 12$. Apply the whole rule each time: $u_2 = 11$. | correct | script A: slip value equals the named mistake |
| l4-last-step | screens[8].widget.answer | key 4698.5 | correct | script A: recomputed |
| l4-last-step | screens[8].widget.wrong[no-interest] | slip 4600: You took off two payments but added no interest. Each month adds 1% first. | correct | script A: slip value equals the named mistake |
| l4-last-step | screens[8].widget.wrong[simple] | slip 4700: You charged 1% of £5,000.00 both months. Month 2's interest is 1% of £4,850.00, the new balance. | correct | script A: slip value equals the named mistake |
| l4-last-step | screens[8].widget.wrong[pay-first] | slip 4694.48: You paid before adding interest. The rule adds 1% first, then takes £200.00. | correct | script A: slip value equals the named mistake |
| l4-last-step | screens[8].widget.wrong[month1] | slip 4850: That is $B_1$. Apply the rule once more. | correct | script A: slip value equals the named mistake |
| l4-last-step | screens[9].widget.answer | key 20000 | correct | script A: recomputed |
| l4-last-step | screens[9].widget.wrong[year] | slip 2400: You took a year of payments, $12 \times 200$. You need the balance whose 1% interest is £200.00. | correct | script A: slip value equals the named mistake |
| l4-last-step | screens[9].widget.wrong[tenth] | slip 2000: You divided by 0.1. One percent is 0.01, so $L = 200 \div 0.01$. | correct | script A: slip value equals the named mistake |
| l4-last-step | screens[9].widget.wrong[big] | slip 200000: You divided by 0.001. One percent is 0.01, so $L = 200 \div 0.01 = 20000$. | correct | script A: slip value equals the named mistake |
| l4-last-step | quiz[0].widget.answer | key 20 | correct | script A: recomputed |
| l4-last-step | quiz[0].widget.wrong[u5] | slip 26: That is $u_5$: four steps of 6. $u_4$ is three steps after $u_1$. | correct | script A: slip value equals the named mistake |
| l4-last-step | quiz[0].widget.wrong[n-in] | slip 9: You added 6 to the position 3. The rule adds 6 to the last term. | correct | script A: slip value equals the named mistake |
| l4-last-step | quiz[1].widget.answer | key 8 | correct | script A: recomputed |
| l4-last-step | quiz[1].widget.wrong[add] | slip 4: 4 is the amount added. Test it: $0.5 \times 4 + 4 = 6$, so 4 moves. | correct | script A: slip value equals the named mistake |
| l4-last-step | quiz[1].widget.wrong[half] | slip 2: You halved 4. Solve $L = 0.5L + 4$ instead: $0.5L = 4$. | correct | script A: slip value equals the named mistake |
| l4-last-step | quiz[2].widget.answer | key 15 | correct | script A: recomputed |
| l4-last-step | quiz[2].widget.wrong[n-in] | slip 5: You put the position, 2, into the rule. The rule doubles the last term, $u_2 = 7$. | correct | script A: slip value equals the named mistake |
| l4-last-step | quiz[2].widget.wrong[u2] | slip 7: That is $u_2$. Apply the rule once more. | correct | script A: slip value equals the named mistake |
| l4-last-step | quiz[3].widget.options[right] | key: $u_{n+1} = 0.9u_n + 1$ | correct | derivation on reading; figures in script A or C |
| l4-last-step | quiz[3].widget.options[grow] | wrong option: $u_{n+1} = 1.1u_n + 1$ / Multiplying by 1.1 grows the gap from its fixed point each step, so the | correct | wrong under every reading; why line checked |
| l4-last-step | quiz[3].widget.options[add] | wrong option: $u_{n+1} = u_n + 1$ / Adding 1 for ever climbs without limit: 0, 1, 2, 3, …. | correct | wrong under every reading; why line checked |
| l4-last-step | quiz[3].widget.options[double] | wrong option: $u_{n+1} = 2u_n + 1$ / Doubling doubles the gap from its fixed point, −1, each step. The terms r | correct | wrong under every reading; why line checked |
| review-1 | items[1].explain | two terms cannot tell arithmetic from geometric | correct | derivation |
| review-1 | items[0].widget.answer | key 11 | correct | script A: recomputed |
| review-1 | items[0].widget.wrong[sign] | slip 21: You added 5. The terms fall by 5 each time. | correct | script A: slip value equals the named mistake |
| review-1 | items[0].widget.wrong[six] | slip 10: You subtracted 6. Check a gap: $31 - 26 = 5$. | correct | script A: slip value equals the named mistake |
| review-1 | items[1].widget.options[right] | key: Arithmetic 20, geometric 36 | correct | derivation on reading; figures in script A or C |
| review-1 | items[1].widget.options[swap] | wrong option: Arithmetic 36, geometric 20 / You swapped them. Adding the gap of 8 gives 20; multiplying by 3 g | correct | wrong under every reading; why line checked |
| review-1 | items[1].widget.options[double] | wrong option: Arithmetic 20, geometric 24 / You doubled 12. The ratio is $12 \div 4 = 3$, so the geometric thi | correct | wrong under every reading; why line checked |
| review-1 | items[1].widget.options[same] | wrong option: Both 20: two terms fix the rule / Two terms fit both kinds of rule. The ratio reading gives $12  | correct | wrong under every reading; why line checked |
| review-1 | items[2].widget.options[right] | key: $15 - 3n$ | correct | derivation on reading; figures in script A or C |
| review-1 | items[2].widget.options[a-nd] | wrong option: $12 - 3n$ / You took $n$ steps from the first term. At $n = 1$ this gives 9, which is $u_2$. | correct | wrong under every reading; why line checked |
| review-1 | items[2].widget.options[sign] | wrong option: $3n + 9$ / You dropped the minus sign. This climbs: 12, 15, 18. | correct | wrong under every reading; why line checked |
| review-1 | items[2].widget.options[swap] | wrong option: $12n - 3$ / You multiplied $n$ by the first term. The difference, −3, multiplies $n$. | correct | wrong under every reading; why line checked |
| review-1 | items[3].widget.answer | key 6 | correct | script A: recomputed |
| review-1 | items[3].widget.wrong[power] | slip 5: 5 is the power of 3. The power is $n - 1$, so $n = 6$. | correct | script A: slip value equals the named mistake |
| review-1 | items[3].widget.wrong[half] | slip 243: 243 is $486 \div 2$. Now write it as a power of 3. | correct | script A: slip value equals the named mistake |
| review-1 | items[4].widget.answer | key 14 | correct | script A: recomputed |
| review-1 | items[4].widget.wrong[n-in] | slip 7: You put the position, 2, into the rule. It takes the last term, $u_2 = 16$. | correct | script A: slip value equals the named mistake |
| review-1 | items[4].widget.wrong[u2] | slip 16: That is $u_2$. Apply the rule once more. | correct | script A: slip value equals the named mistake |
| review-1 | items[5].widget.answer | key 20 | correct | script A: recomputed |
| review-1 | items[5].widget.wrong[add] | slip 5: 5 is the amount added. Test it: $0.75 \times 5 + 5 = 8.75$, so 5 moves. | correct | script A: slip value equals the named mistake |
| review-1 | items[5].widget.wrong[divide] | slip 6.6667: You divided 5 by 0.75. Subtract $0.75L$ first: $0.25L = 5$. | correct | script A: slip value equals the named mistake |
| review-1 | items[6].widget.answer | key -25.6 | correct | script A: recomputed |
| review-1 | items[6].widget.wrong[sign] | slip 25.6: Three negative factors make a negative. The sign flips each step: 50, −40, 32, −25.6. | correct | script A: slip value equals the named mistake |
| review-1 | items[6].widget.wrong[four] | slip 20.48: You multiplied by −0.8 four times: that is $u_5$. | correct | script A: slip value equals the named mistake |
| review-1 | items[7].widget.answer | key 15 | correct | script A: recomputed |
| review-1 | items[7].widget.wrong[m14] | slip 14: Trade 14 leaves $350 + 13 \times 125 = 1975$ shares. That is 25 short. | correct | script A: slip value equals the named mistake |
| review-1 | items[7].widget.wrong[m16] | slip 16: You divided 2,000 by 125. The desk already held 350 shares. | correct | script A: slip value equals the named mistake |
| review-1 | items[7].widget.wrong[m13] | slip 13: You found $n - 1 = 13.2$ and rounded down. You need $n - 1 = 14$. | correct | script A: slip value equals the named mistake |
| review-1 | items[8].widget.answer | key 7 | correct | script A: recomputed |
| review-1 | items[8].widget.wrong[y6] | slip 6: Day 6 trades $0.80 \times 1.04^5 \approx 0.97$ million. Day 6 is only five rises after day 1. | correct | script A: slip value equals the named mistake |
| review-1 | items[8].widget.wrong[simple] | slip 8: You added 0.032 million a day, 4% of day 1's volume. Each rise is 4% of the latest volume, so it gets  | correct | script A: slip value equals the named mistake |
| homework-1 | items[6].widget | gap u_n - L is geometric with ratio a | correct | derivation (script C) |
| homework-1 | items[6].explain | the gap shrinks to 0 exactly when -1 < a < 1 | imprecise | also when u_1 = L (gap 0 for every a). Finding 4 |
| homework-1 | items[8].model | B_n = 12000 - 2000 x 1.01^n; withdrawal £100 keeps £10,000 | correct | script C: closed form equals recurrence |
| homework-1 | items[0].widget.answer | key 21-4n and accept list | correct | derivation: tested at n or x = 1, 2, 3 |
| homework-1 | items[0].widget.wrong[a-nd] | slip 17-4n: You took $n$ steps from the first term. At $n = 1$ this gives 13, which is $u_2$. | correct | derivation: not equal to the key; feedback value checked |
| homework-1 | items[0].widget.wrong[sign] | slip 4n+13: The terms fall, so $d = -4$, not 4. | correct | derivation: not equal to the key; feedback value checked |
| homework-1 | items[1].widget.answer | key 96\cdot0.5^{n-1} and accept list | correct | derivation: tested at n or x = 1, 2, 3 |
| homework-1 | items[1].widget.wrong[power-n] | slip 96\cdot0.5^{n}: You used $n$ factors of 0.5. At $n = 1$ this gives 48, which is $u_2$. | correct | derivation: not equal to the key; feedback value checked |
| homework-1 | items[1].widget.wrong[bracket] | slip 48^{n-1}: You raised $96 \times 0.5$ to the power. Only $r$ is repeated. | correct | derivation: not equal to the key; feedback value checked |
| homework-1 | items[2].widget.answer | key 32 | correct | script A: recomputed |
| homework-1 | items[2].widget.wrong[add-last] | slip 30: You repeated the last gap, 8. The gaps grow by 2 each time, so the next is 10. | correct | script A: slip value equals the named mistake |
| homework-1 | items[2].widget.wrong[double] | slip 44: You read doubling from 2, 4, 8. But 8 to 14 is not doubling, so the rule is something else. | correct | script A: slip value equals the named mistake |
| homework-1 | items[3].widget.answer | key -25 | correct | script A: recomputed |
| homework-1 | items[3].widget.wrong[ten] | slip -28: You took ten steps from $u_{11}$. $u_{20}$ is nine steps on. | correct | script A: slip value equals the named mistake |
| homework-1 | items[3].widget.wrong[eight] | slip -22: You took eight steps from $u_{11}$. $u_{20}$ is nine steps on. | correct | script A: slip value equals the named mistake |
| homework-1 | items[3].widget.wrong[sign] | slip 25: The sequence falls by 3 each step, so u₂₀ = 2 − 27, and 27 is bigger than 2. A positive 25 takes 27 − | correct | script A: slip value equals the named mistake |
| homework-1 | items[4].widget.answer | key 2916 | correct | script A: recomputed |
| homework-1 | items[4].widget.wrong[u8] | slip 8748: That is $u_8$: three steps after $u_5$. $u_7$ is two steps on. | correct | script A: slip value equals the named mistake |
| homework-1 | items[4].widget.wrong[u6] | slip 972: That is $u_6$. Multiply by 3 once more. | correct | script A: slip value equals the named mistake |
| homework-1 | items[4].widget.wrong[arith] | slip 532: You treated it as arithmetic, adding 104 each step. Three multiplications by $r$ take 12 to 324, not | correct | script A: slip value equals the named mistake |
| homework-1 | items[5].widget.answer | key 11728.65 | correct | script A: recomputed |
| homework-1 | items[5].widget.wrong[no-int] | slip 11550: You took off three payments but added no interest. | correct | script A: slip value equals the named mistake |
| homework-1 | items[5].widget.wrong[simple] | slip 11730: You charged 0.5% of £12,000.00 every month. Each month's interest is on the new balance. | correct | script A: slip value equals the named mistake |
| homework-1 | items[5].widget.wrong[two] | slip 11819.55: That is after 2 months. Apply the rule once more. | correct | script A: slip value equals the named mistake |
| homework-1 | items[7].widget.answer | key 40 | correct | script A: recomputed |
| homework-1 | items[7].widget.wrong[gain] | slip 22: You found when B's monthly gain first passes £300.00. B is still £1,140.20 behind then, after many mo | correct | script A: slip value equals the named mistake |
| homework-1 | items[7].widget.wrong[before] | slip 39: At month 39, B holds £21,647.45 and A £21,700.00. B is still £52.55 behind. | correct | script A: slip value equals the named mistake |
| homework-1 | items[7].widget.wrong[never] | slip 0: B starts slower, gaining only £200.00 in month 1. But its gains grow, so it overtakes. | correct | script A: slip value equals the named mistake |
| homework-1 | items[8].model | longform model answer and rubric | correct | script C recomputes every figure |
| problems-1 | items[2].parts[2].explain | gap 400 - u_n is geometric, ratio 0.4 | correct | derivation |
| problems-1 | items[3].parts[2].explain | two terms fit both an arithmetic and a geometric rule | correct | derivation |
| problems-1 | items[0].parts[0].widget.answer | key 36 | correct | script A: recomputed |
| problems-1 | items[0].parts[0].widget.wrong[seven-steps] | slip 39: That adds 7 steps of 3 to row 1. Row 7 is only 6 steps after row 1: $18 + 6 \times 3 = 36$. | correct | script A: slip value equals the named mistake |
| problems-1 | items[0].parts[0].widget.wrong[next-row] | slip 30: 30 seats is row 5, the next row after row 4. Two more steps of 3 reach row 7: 36. | correct | script A: slip value equals the named mistake |
| problems-1 | items[0].parts[1].widget.answer | key 3n+15 and accept list | correct | derivation: tested at n or x = 1, 2, 3 |
| problems-1 | items[0].parts[1].widget.wrong[n-steps] | slip 18+3n: That gives 21 seats in row 1. Row $n$ is only $n - 1$ steps after row 1, so $u_n = 18 + 3(n - 1) = | correct | derivation: not equal to the key; feedback value checked |
| problems-1 | items[0].parts[1].widget.wrong[swapped] | slip 18n+3: You swapped the first row and the step. The step 3 multiplies $n$: $u_n = 3n + 15$. | correct | derivation: not equal to the key; feedback value checked |
| problems-1 | items[0].parts[1].widget.wrong[step-only] | slip 3n: $3n$ gives only 3 seats in row 1. Add 15 so that row 1 has 18: $u_n = 3n + 15$. | correct | derivation: not equal to the key; feedback value checked |
| problems-1 | items[0].parts[2].widget.answer | key 90 | correct | script A: recomputed |
| problems-1 | items[0].parts[2].widget.wrong[n-steps] | slip 93: That is $18 + 3 \times 25$, which counts 25 steps after row 1. Row 25 is 24 steps on: $18 + 72 = 90$. | correct | script A: slip value equals the named mistake |
| problems-1 | items[0].parts[2].widget.wrong[step-only] | slip 75: 75 is $3 \times 25$ alone. Add the 15 from the rule: 90. | correct | script A: slip value equals the named mistake |
| problems-1 | items[0].parts[3].widget.answer | key 10 | correct | script A: recomputed |
| problems-1 | items[0].parts[3].widget.wrong[halfway] | slip 12.5: Halfway back is not half the seats: rows 12 and 13 have 51 and 54. Solve $3n + 15 \ge 45$ instead,  | correct | script A: slip value equals the named mistake |
| problems-1 | items[0].parts[3].widget.wrong[divided] | slip 15: $45 \div 3 = 15$ leaves out the 15 in the rule. Solve $3n + 15 \ge 45$: $3n \ge 30$, so $n \ge 10$. | correct | script A: slip value equals the named mistake |
| problems-1 | items[0].parts[3].widget.wrong[steps] | slip 9: 9 is the number of steps of 3 from 18 up to 45. Row 1 plus 9 steps is row 10. | correct | script A: slip value equals the named mistake |
| problems-1 | items[1].parts[0].widget.options[ratio] | key: Multiply by 0.9 | correct | derivation on reading; figures in script A or C |
| problems-1 | items[1].parts[0].widget.options[minus-eight] | wrong option: Subtract 8 / That fits the first pair only: $72 - 8 = 64$, not 64.8. | correct | wrong under every reading; why line checked |
| problems-1 | items[1].parts[0].widget.options[minus-second] | wrong option: Subtract 7.2 / That fits the second pair only: $80 - 7.2 = 72.8$, not 72. | correct | wrong under every reading; why line checked |
| problems-1 | items[1].parts[0].widget.options[ratio-eight] | wrong option: Multiply by 0.8 / $80 \times 0.8 = 64$, not 72. The ratio is $72 \div 80 = 0.9$. | correct | wrong under every reading; why line checked |
| problems-1 | items[1].parts[1].widget.answer | key 80\cdot0.9^{n-1} and accept list | correct | derivation: tested at n or x = 1, 2, 3 |
| problems-1 | items[1].parts[1].widget.wrong[power-n] | slip 80\cdot0.9^{n}: That gives 72 cm for swing 1. Swing $n$ has $n - 1$ factors of 0.9: $80 \times 0.9^{n-1}$ | correct | derivation: not equal to the key; feedback value checked |
| problems-1 | items[1].parts[1].widget.wrong[bracket] | slip 72^{n-1}: You raised $80 \times 0.9$ to the power. Only the 0.9 is repeated: $80 \times 0.9^{n-1}$. | correct | derivation: not equal to the key; feedback value checked |
| problems-1 | items[1].parts[1].widget.wrong[arith] | slip 88-8n: That takes 8 cm off every swing, which gives 64 for swing 3. The swings multiply by 0.9: $80 \time | correct | derivation: not equal to the key; feedback value checked |
| problems-1 | items[1].parts[2].widget.answer | key 47.2392 | correct | script A: recomputed |
| problems-1 | items[1].parts[2].widget.wrong[power-n] | slip 42.515: That is $80 \times 0.9^6$, which is swing 7. Swing 6 has $6 - 1 = 5$ factors: $80 \times 0.9^5 \a | correct | script A: slip value equals the named mistake |
| problems-1 | items[1].parts[2].widget.wrong[swing-five] | slip 52.488: That is $80 \times 0.9^4$, which is swing 5. Swing 6 has five factors of 0.9: about 47.2 cm. | correct | script A: slip value equals the named mistake |
| problems-1 | items[1].parts[2].widget.wrong[arith] | slip 40: That takes 8 cm off each swing. Each swing is 0.9 of the last, so the losses shrink: $80 \times 0.9^5 | correct | script A: slip value equals the named mistake |
| problems-1 | items[1].parts[3].widget.answer | key 8 | correct | script A: recomputed |
| problems-1 | items[1].parts[3].widget.wrong[seven] | slip 7: Swing 7 is about $47.2 \times 0.9 \approx 42.5$ cm, still over 40. One more swing gives about 38.3 cm. | correct | script A: slip value equals the named mistake |
| problems-1 | items[1].parts[3].widget.wrong[six] | slip 6: Swing 6 is about 47.2 cm, well over 40. Taking 8 cm off each time would reach 40 there, but the swings | correct | script A: slip value equals the named mistake |
| problems-1 | items[2].parts[0].widget.answer | key 374.4 | correct | script A: recomputed |
| problems-1 | items[2].parts[0].widget.wrong[no-clearing] | slip 720: That adds three tablets with nothing cleared. Each morning only 40% is left: $0.4 \times 240 + 240 = | correct | script A: slip value equals the named mistake |
| problems-1 | items[2].parts[0].widget.wrong[tablet-two] | slip 336: 336 mg is $u_2$, just after tablet 2. One more step: $0.4 \times 336 + 240 = 374.4$. | correct | script A: slip value equals the named mistake |
| problems-1 | items[2].parts[0].widget.wrong[kept-sixty] | slip 470.4: That keeps 60% each day. Clearing 60% leaves 40%: $u_2 = 0.4 \times 240 + 240 = 336$. | correct | script A: slip value equals the named mistake |
| problems-1 | items[2].parts[1].widget.answer | key 400 | correct | script A: recomputed |
| problems-1 | items[2].parts[1].widget.wrong[kept-sixty] | slip 600: 600 solves $L = 0.6L + 240$, which keeps 60%. The body keeps 40%: $0.6L = 240$ gives $L = 400$. | correct | script A: slip value equals the named mistake |
| problems-1 | items[2].parts[1].widget.wrong[sign] | slip 171.43: You added $0.4L$ to both sides. Take it away: $L - 0.4L = 0.6L = 240$, so $L = 400$. | correct | script A: slip value equals the named mistake |
| problems-1 | items[2].parts[2].widget.answer | key 160\cdot0.4^{n-1} and accept list | correct | derivation: tested at n or x = 1, 2, 3 |
| problems-1 | items[2].parts[2].widget.wrong[power-n] | slip 160\cdot0.4^{n}: That gives 64 for $g_1$. The first gap is 160, so $g_n = 160 \times 0.4^{n-1}$. | correct | derivation: not equal to the key; feedback value checked |
| problems-1 | items[2].parts[2].widget.wrong[cleared] | slip 160\cdot0.6^{n-1}: 0.6 is the share cleared. The gap keeps 40% each day: $64 = 160 \times 0.4$. | correct | derivation: not equal to the key; feedback value checked |
| problems-1 | items[2].parts[2].widget.wrong[level] | slip 400\cdot0.4^{n-1}: 400 is the level, not the first gap. Just after tablet 1 the gap is $400 - 240 = 160$. | correct | derivation: not equal to the key; feedback value checked |
| problems-1 | items[2].parts[3].widget.answer | key 5 | correct | script A: recomputed |
| problems-1 | items[2].parts[3].widget.wrong[power-n] | slip 4: After tablet 4 the gap is $160 \times 0.4^3 = 10.24$, so $u_4 = 389.76$ mg. That is still below 395. | correct | script A: slip value equals the named mistake |
| problems-1 | items[2].parts[3].widget.wrong[kept-sixty] | slip 3: That keeps 60% each day, which runs on towards 600. With 40% kept, the amount passes 395 only after ta | correct | script A: slip value equals the named mistake |
| problems-1 | items[3].parts[0].widget.answer | key 60 | correct | script A: recomputed |
| problems-1 | items[3].parts[0].widget.wrong[no-halve] | slip 120: 120 is the rise over two months. One month is half of it: 60. | correct | script A: slip value equals the named mistake |
| problems-1 | items[3].parts[0].widget.wrong[three-steps] | slip 40: Months 2, 3 and 4 are three months but only two steps. So $d = 120 \div 2 = 60$. | correct | script A: slip value equals the named mistake |
| problems-1 | items[3].parts[1].widget.answer | key 1.5 | correct | script A: recomputed |
| problems-1 | items[3].parts[1].widget.wrong[no-root] | slip 2.25: 2.25 is the multiple over two months, $r^2$. One month is its square root: 1.5. | correct | script A: slip value equals the named mistake |
| problems-1 | items[3].parts[1].widget.wrong[halved] | slip 1.125: You halved 2.25. Two steps multiply, so take the square root: $\sqrt{2.25} = 1.5$. | correct | script A: slip value equals the named mistake |
| problems-1 | items[3].parts[1].widget.wrong[inverted] | slip 0.6667: You divided 96 by 216. The orders grow, so $r^2 = 216 \div 96 = 2.25$ and $r = 1.5$. | correct | script A: slip value equals the named mistake |
| problems-1 | items[3].parts[2].widget.options[geom] | key: Times 1.5 each month | correct | derivation on reading; figures in script A or C |
| problems-1 | items[3].parts[2].widget.options[arith] | wrong option: Add 60 each month / That gives $96 + 60 = 156$ in month 3, not 144. | correct | wrong under every reading; why line checked |
| problems-1 | items[3].parts[2].widget.options[both] | wrong option: Both rules fit / They agree in months 2 and 4 but not in month 3: 156 against 144. | correct | wrong under every reading; why line checked |
| problems-1 | items[3].parts[2].widget.options[neither] | wrong option: Neither rule fits / $96 \times 1.5 = 144$ and $144 \times 1.5 = 216$, so multiplying fits. | correct | wrong under every reading; why line checked |
| problems-1 | items[3].parts[3].widget.answer | key 64\cdot1.5^{n-1} and accept list | correct | derivation: tested at n or x = 1, 2, 3 |
| problems-1 | items[3].parts[3].widget.wrong[month-two-start] | slip 96\cdot1.5^{n-1}: That gives 96 for month 1, the same as $64 \times 1.5^{n}$. The 96 is month 2, so month | correct | derivation: not equal to the key; feedback value checked |
| problems-1 | items[3].parts[3].widget.wrong[arith] | slip 60n-24: That is the adding rule, which month 3 ruled out. The orders multiply by 1.5: $64 \times 1.5^{n-1 | correct | derivation: not equal to the key; feedback value checked |
| problems-1 | items[3].parts[4].widget.answer | key 8 | correct | script A: recomputed |
| problems-1 | items[3].parts[4].widget.wrong[power-n] | slip 7: Month 7 has $64 \times 1.5^6 = 729$ orders, below 1,000. Month 8 has about 1,094. | correct | script A: slip value equals the named mistake |
| problems-1 | items[3].parts[4].widget.wrong[arith] | slip 18: Adding 60 a month passes 1,000 only in month 18. The records fit multiplying by 1.5, which gets there | correct | script A: slip value equals the named mistake |
| fluency-l2-any-term | families[term-from-list].widget.answer | key {u} over the whole range | correct | script B: brute-force sweep of every admissible case |
| fluency-l2-any-term | families[term-from-list].wrong[k-steps] | You added {k} steps of {d}, but $u_{{{k}}}$ is only {km} steps after $u_1$. | correct | script B: value equals the named mistake, never the key |
| fluency-l2-any-term | families[term-from-list].wrong[difference-sign] | Check the sign of $d$: it is ${t2} - {a:()} = {d}$. | correct | script B: value equals the named mistake, never the key |
| fluency-l2-any-term | families[nth-term-formula].widget.answer | key {poly(n; d, c)} over the whole range | correct | script B: brute-force sweep of every admissible case |
| fluency-l2-any-term | families[nth-term-formula].wrong[n-steps] | You added $n$ steps to the first term. At $n = 1$ that gives {t2}, which is $u_2$. | correct | script B: value equals the named mistake, never the key |
| fluency-l2-any-term | families[nth-term-formula].wrong[first-term-times-n] | You multiplied $n$ by the first term. The difference, {d}, multiplies $n$. | correct | script B: value equals the named mistake, never the key |
| fluency-l2-any-term | families[difference-from-two-terms].widget.answer | key {d} over the whole range | correct | script B: brute-force sweep of every admissible case |
| fluency-l2-any-term | families[difference-from-two-terms].wrong[whole-rise] | That is the whole change from $u_{{{p}}}$ to $u_{{{q}}}$. Share it over the {g} steps. | correct | script B: value equals the named mistake, never the key |
| fluency-l2-any-term | families[difference-from-two-terms].wrong[counted-terms] | You shared the change over {gt} terms, but there are {g} steps between them. | correct | script B: value equals the named mistake, never the key |
| fluency-l2-any-term | families[which-term].widget.answer | key {m} over the whole range | correct | script B: brute-force sweep of every admissible case |
| fluency-l2-any-term | families[which-term].wrong[steps-not-position] | You gave the number of steps of {d}. The position is one more than the steps. | correct | script B: value equals the named mistake, never the key |
| fluency-l2-any-term | families[which-term].wrong[one-too-many] | You added one too many. Term $n$ is $n - 1$ steps after the first. | correct | script B: value equals the named mistake, never the key |
| fluency-l3-multiplying-each-time | families[geometric-term].widget.answer | key {u} over the whole range | correct | script B: brute-force sweep of every admissible case |
| fluency-l3-multiplying-each-time | families[geometric-term].wrong[k-factors] | You used {k} factors of $r$, but $u_{{{k}}}$ has only {km}. | correct | script B: value equals the named mistake, never the key |
| fluency-l3-multiplying-each-time | families[geometric-term].wrong[added-the-step] | You added the same step each time. This sequence multiplies by the same number. | correct | script B: value equals the named mistake, never the key |
| fluency-l3-multiplying-each-time | families[common-ratio].widget.answer | key {r} over the whole range | correct | script B: brute-force sweep of every admissible case |
| fluency-l3-multiplying-each-time | families[common-ratio].wrong[upside-down] | You divided the first term by the second. Divide each term by the one before. | correct | script B: value equals the named mistake, never the key |
| fluency-l3-multiplying-each-time | families[common-ratio].wrong[difference] | You took the difference of two terms. A geometric sequence has a common ratio, not a difference. | correct | script B: value equals the named mistake, never the key |
| fluency-l3-multiplying-each-time | families[geometric-formula].widget.answer | key {a} \times {r:()}^{{n-1}} over the whole range | correct | script B: brute-force sweep of every admissible case |
| fluency-l3-multiplying-each-time | families[geometric-formula].wrong[n-factors] | You used $n$ factors of $r$. At $n = 1$ that gives {t2}, which is $u_2$. | correct | script B: value equals the named mistake, never the key |
| fluency-l3-multiplying-each-time | families[geometric-formula].wrong[ratio-and-first-swapped] | You swapped the first term and the ratio. The ratio, {r}, is the number raised to a power. | correct | script B: value equals the named mistake, never the key |
| fluency-l3-multiplying-each-time | families[geometric-formula].wrong[arithmetic-rule] | That is the arithmetic rule through the first two terms. This sequence multiplies by {r} each time. | correct | script B: value equals the named mistake, never the key |
| l5-sigma | screens[3].prose | series = adding the terms of a sequence; partial sum; sigma notation | correct | Pearson Edexcel A level Pure Year 2 ch. 3 s3.5; Spivak, Calculus ch. 23 |
| l5-sigma | screens[6].explain | a sum from k = m to k = n has n - m + 1 terms | correct | counting |
| l5-sigma | screens[7].prose | S_n = S_(n-1) + a_n | correct | definition |
| l5-sigma | screens[8].widget | telescoping: sum of (p_k - p_(k-1)) = p_5 - p_0 | correct | derivation |
| l5-sigma | screens[9].explain | cumulative P&L equals the change in book value, by telescoping | correct | derivation |
| l5-sigma | screens[6].prose | bond coupon at the end of each year, years 4 to 12 | correct | convention stated |
| l5-sigma | screens[1].widget.answer | key 15 | correct | script A: recomputed |
| l5-sigma | screens[1].widget.wrong[term] | slip 7: £7.00 is week 3's saving on its own, $a_3$. The total also holds weeks 1 and 2. | correct | script A: slip value equals the named mistake |
| l5-sigma | screens[1].widget.wrong[times] | slip 21: You multiplied week 3's £7.00 by 3. The earlier weeks saved less than £7.00. | correct | script A: slip value equals the named mistake |
| l5-sigma | screens[1].widget.wrong[skip] | slip 10: You added weeks 1 and 3 and missed week 2's £5.00. | correct | script A: slip value equals the named mistake |
| l5-sigma | screens[1].widget.wrong[four] | slip 24: £24.00 is the total after four weeks. Stop at week 3. | correct | script A: slip value equals the named mistake |
| l5-sigma | screens[2].widget.options[right] | key: $S_4$ and $S_5$ only | correct | derivation on reading; figures in script A or C |
| l5-sigma | screens[2].widget.options[one] | wrong option: $S_4$ only / You watched the bar next to $a_4$. $S_5$ adds week 4 as well, so it moves by the sa | correct | wrong under every reading; why line checked |
| l5-sigma | screens[2].widget.options[all] | wrong option: All five totals / $S_1$, $S_2$ and $S_3$ were complete before week 4. They hold weeks 1 to 3 onl | correct | wrong under every reading; why line checked |
| l5-sigma | screens[2].widget.options[none] | wrong option: None of them / Move the slider again and watch $S_4$. It rises £1.00 for each £1.00 you add to w | correct | wrong under every reading; why line checked |
| l5-sigma | screens[3].widget.options[right] | key: $3 + 5 + 7 + 9 + 11$ | correct | derivation on reading; figures in script A or C |
| l5-sigma | screens[3].widget.options[zero] | wrong option: $1 + 3 + 5 + 7 + 9$ / You started at $k = 0$. The bottom of the sigma says $k = 1$, so the first | correct | wrong under every reading; why line checked |
| l5-sigma | screens[3].widget.options[noone] | wrong option: $2 + 4 + 6 + 8 + 10$ / You doubled each $k$ and dropped the $+1$. Each term is $2k + 1$. | correct | wrong under every reading; why line checked |
| l5-sigma | screens[3].widget.options[five] | wrong option: $11 + 11 + 11 + 11 + 11$ / You put $k = 5$ into every term. $k$ takes each value 1, 2, 3, 4, 5 i | correct | wrong under every reading; why line checked |
| l5-sigma | screens[4].widget.answer | place key null | correct | derivation on reading |
| l5-sigma | screens[5].widget.answer | key 30 | correct | script A: recomputed |
| l5-sigma | screens[5].widget.wrong[square-total] | slip 100: You added $1 + 2 + 3 + 4 = 10$ and squared the total. The sigma squares each $k$ first, then adds. | correct | script A: slip value equals the named mistake |
| l5-sigma | screens[5].widget.wrong[last] | slip 16: 16 is the last term, $4^2$. The sum adds all four terms. | correct | script A: slip value equals the named mistake |
| l5-sigma | screens[5].widget.wrong[no-square] | slip 10: You added $1 + 2 + 3 + 4$ without squaring. The term is $k^2$. | correct | script A: slip value equals the named mistake |
| l5-sigma | screens[5].widget.wrong[double] | slip 20: You doubled each $k$ instead of squaring it. | correct | script A: slip value equals the named mistake |
| l5-sigma | screens[6].widget.answer | key 45 | correct | script A: recomputed |
| l5-sigma | screens[6].widget.wrong[gap] | slip 40: You took $12 - 4 = 8$ terms. That counts the gaps between years. Years 4 and 12 both pay, so there ar | correct | script A: slip value equals the named mistake |
| l5-sigma | screens[6].widget.wrong[from-one] | slip 60: You counted 12 coupons from year 1. The sigma starts at $k = 4$, so years 1 to 3 pay nothing. | correct | script A: slip value equals the named mistake |
| l5-sigma | screens[6].widget.wrong[one] | slip 5: £5.00 is one coupon. The sigma adds one 5 for each $k$ from 4 to 12. | correct | script A: slip value equals the named mistake |
| l5-sigma | screens[6].widget.wrong[eleven] | slip 55: You counted 11 terms. List the years 4, 5, ..., 12 and count them again. | correct | script A: slip value equals the named mistake |
| l5-sigma | screens[7].widget.answer | key 14 | correct | script A: recomputed |
| l5-sigma | screens[7].widget.wrong[gap] | slip 13: $20 - 7 = 13$ counts the gaps. Add 1 to count the terms. | correct | script A: slip value equals the named mistake |
| l5-sigma | screens[7].widget.wrong[top] | slip 20: That counts from $k = 1$. This sum starts at $k = 7$. | correct | script A: slip value equals the named mistake |
| l5-sigma | screens[9].widget.answer | key 50 | correct | script A: recomputed |
| l5-sigma | screens[9].widget.wrong[day] | slip -1500: −£1,500.00 is day 4's P&L alone, $a_4$. The cumulative figure adds days 1 to 4. | correct | script A: slip value equals the named mistake |
| l5-sigma | screens[9].widget.wrong[abs] | slip 3950: You added the sizes and dropped the signs. A loss subtracts from the total. | correct | script A: slip value equals the named mistake |
| l5-sigma | screens[9].widget.wrong[five] | slip 400: £400.00 is the total after all five days. Stop at day 4. | correct | script A: slip value equals the named mistake |
| l5-sigma | screens[9].widget.wrong[three] | slip 1550: £1,550.00 is the total after day 3. Day 4's loss still has to come off. | correct | script A: slip value equals the named mistake |
| l5-sigma | quiz[0].widget.answer | key 30 | correct | script A: recomputed |
| l5-sigma | quiz[0].widget.wrong[sign] | slip 50: You added $k$ to 10. The term is $10 - k$, so each term is smaller than 10. | correct | script A: slip value equals the named mistake |
| l5-sigma | quiz[0].widget.wrong[ten] | slip 40: You added four 10s and forgot to take each $k$ away. | correct | script A: slip value equals the named mistake |
| l5-sigma | quiz[0].widget.wrong[one] | slip 9: 9 is the first term only. Add all four. | correct | script A: slip value equals the named mistake |
| l5-sigma | quiz[1].widget.options[right] | key: $n + 1$ | correct | derivation on reading; figures in script A or C |
| l5-sigma | quiz[1].widget.options[n] | wrong option: $n$ / You counted from 1 to $n$. The term $a_0$ comes first, which adds one more. | correct | wrong under every reading; why line checked |
| l5-sigma | quiz[1].widget.options[nm1] | wrong option: $n - 1$ / You subtracted one too many. From 0 to $n$ there are $n - 0 + 1$ terms. | correct | wrong under every reading; why line checked |
| l5-sigma | quiz[2].widget.options[right] | key: $\sum_{k=1}^{20} 2k$ | correct | derivation on reading; figures in script A or C |
| l5-sigma | quiz[2].widget.options[top40] | wrong option: $\sum_{k=1}^{40} 2k$ / You put the last term, 40, on top. Then $k = 40$ would give 80. The top i | correct | wrong under every reading; why line checked |
| l5-sigma | quiz[2].widget.options[plain] | wrong option: $\sum_{k=2}^{40} k$ / That adds every whole number from 2 to 40, odd ones too. | correct | wrong under every reading; why line checked |
| l5-sigma | quiz[2].widget.options[odd] | wrong option: $\sum_{k=1}^{20} (2k - 1)$ / That gives $1 + 3 + \dots + 39$, the odd numbers. | correct | wrong under every reading; why line checked |
| l5-sigma | quiz[3].widget.answer | key 9 | correct | script A: recomputed |
| l5-sigma | quiz[3].widget.wrong[sum] | slip 91: You added the two totals. $S_6$ already contains $S_5$, so subtract instead. | correct | script A: slip value equals the named mistake |
| l5-sigma | quiz[3].widget.wrong[total] | slip 50: 50 is the total after six months. The question asks for month 6 alone. | correct | script A: slip value equals the named mistake |
| l5-sigma | quiz[3].widget.wrong[avg] | slip 8.33: You averaged $S_6$ over six months. Month 6 is the step from $S_5$ to $S_6$. | correct | script A: slip value equals the named mistake |
| l6-gauss | screens[0].prose | Gauss and the sum 1 to 100 | correct | traditional anecdote (Sartorius 1856); told as a story |
| l6-gauss | screens[5].explain | the pairing trick never needs an even number of terms | correct | derivation: 2S = n(a + l) for any n |
| l6-gauss | screens[6].explain | number of terms = steps + 1 | correct | counting |
| l6-gauss | screens[7].widget | S = n/2 (a + l) | correct | Pearson Edexcel A level Pure Year 2 ch. 3 s3.2 |
| l6-gauss | screens[8].prose | S_n = n/2 (2a + (n-1)d) | correct | Pearson Edexcel A level Pure Year 2 ch. 3 s3.2 |
| l6-gauss | quiz[1].explain | the first n odd numbers always add to n^2 | correct | derivation: n/2 (1 + 2n - 1) |
| l6-gauss | screens[1].widget.options[right] | key: Exactly half | correct | derivation on reading; figures in script A or C |
| l6-gauss | screens[1].widget.options[less] | wrong option: Less than half / You may have judged by the empty top-right corner. Count the empty cells: $5 +  | correct | wrong under every reading; why line checked |
| l6-gauss | screens[1].widget.options[more] | wrong option: More than half / The bottom row looks full, but it holds 5 of 6 cells. The empty cells total 15, | correct | wrong under every reading; why line checked |
| l6-gauss | screens[2].widget.answer | tap-regions key ["c12", "c13", "c14", "c15", "c23", "c24", "c25", "c34", "c35", "c45"] | correct | derivation on reading |
| l6-gauss | screens[3].widget.answer | key 7 | correct | script A: recomputed |
| l6-gauss | screens[3].widget.wrong[six] | slip 6: 6 is the last term. Each column adds a term to its partner from the other end. | correct | script A: slip value equals the named mistake |
| l6-gauss | screens[3].widget.wrong[total] | slip 21: 21 is the whole sum. The question asks for one column. | correct | script A: slip value equals the named mistake |
| l6-gauss | screens[4].widget.answer | key 5050 | correct | script A: recomputed |
| l6-gauss | screens[4].widget.wrong[no-half] | slip 10100: 10,100 is both rows together. Each number is written twice, so halve it. | correct | script A: slip value equals the named mistake |
| l6-gauss | screens[4].widget.wrong[fifty] | slip 5000: You used 50 pairs of 100. Each pair adds to 101, not 100. | correct | script A: slip value equals the named mistake |
| l6-gauss | screens[4].widget.wrong[fiftyone] | slip 5100: You used 51 pairs of 100. There are 50 pairs, each adding to 101. | correct | script A: slip value equals the named mistake |
| l6-gauss | screens[4].widget.wrong[one-col] | slip 101: 101 is one column. There are 100 columns, and then we halve. | correct | script A: slip value equals the named mistake |
| l6-gauss | screens[5].widget.answer | key 45 | correct | script A: recomputed |
| l6-gauss | screens[5].widget.wrong[drop-middle] | slip 36: You added the two pairs and dropped the 9. It is still a term, so it counts. | correct | script A: slip value equals the named mistake |
| l6-gauss | screens[5].widget.wrong[three-pairs] | slip 54: You counted the middle as a full pair of 18. On its own it is 9, half a pair. | correct | script A: slip value equals the named mistake |
| l6-gauss | screens[5].widget.wrong[no-half] | slip 90: 90 counts each term twice, once in each row. Halve it. | correct | script A: slip value equals the named mistake |
| l6-gauss | screens[6].widget.answer | key 440 | correct | script A: recomputed |
| l6-gauss | screens[6].widget.wrong[fifteen] | slip 412.5: You used 15 terms, from $(50 - 5) \div 3 = 15$. That counts the steps. 15 steps join 16 terms, lik | correct | script A: slip value equals the named mistake |
| l6-gauss | screens[6].widget.wrong[no-half] | slip 880: 880 is 16 columns of 55, which counts each term twice. Halve it. | correct | script A: slip value equals the named mistake |
| l6-gauss | screens[6].widget.wrong[seventeen] | slip 467.5: You counted 17 terms. From 5 to 50 is 15 steps of 3, which join 16 terms. | correct | script A: slip value equals the named mistake |
| l6-gauss | screens[6].widget.wrong[fifteen-no-half] | slip 825: You used 15 terms and forgot to halve. There are 16 terms, and the columns count each one twice. | correct | script A: slip value equals the named mistake |
| l6-gauss | screens[8].widget.answer | key 650 | correct | script A: recomputed |
| l6-gauss | screens[8].widget.wrong[nd] | slip 680: You used $20 \times 3$ for the rises. The 20th term is 19 steps after the first, so it is $4 + 19 \t | correct | script A: slip value equals the named mistake |
| l6-gauss | screens[8].widget.wrong[no-half] | slip 1300: You used $n$ instead of $\tfrac{n}{2}$. Each column counts two terms. | correct | script A: slip value equals the named mistake |
| l6-gauss | screens[8].widget.wrong[last] | slip 61: 61 is the 20th term. The sum adds all twenty. | correct | script A: slip value equals the named mistake |
| l6-gauss | screens[9].widget.answer | key 5800 | correct | script A: recomputed |
| l6-gauss | screens[9].widget.wrong[seven] | slip 5075: You counted 7 levels from $(100.07 - 100.00) \div 0.01$. That counts the price steps; there are 8 l | correct | script A: slip value equals the named mistake |
| l6-gauss | screens[9].widget.wrong[no-half] | slip 11600: 11,600 counts every level twice. Halve it. | correct | script A: slip value equals the named mistake |
| l6-gauss | screens[9].widget.wrong[n-not-n1] | slip 6400: You took the deepest level as $200 + 8 \times 150 = 1400$. It is 7 steps above the best ask: $200 + | correct | script A: slip value equals the named mistake |
| l6-gauss | screens[9].widget.wrong[first] | slip 1600: 1,600 is 8 levels of 200, as if every level matched the best ask. The sizes grow by 150 a level. | correct | script A: slip value equals the named mistake |
| l6-gauss | quiz[0].widget.answer | key 1275 | correct | script A: recomputed |
| l6-gauss | quiz[0].widget.wrong[no-half] | slip 2550: 2,550 is 50 columns of 51, which counts each number twice. | correct | script A: slip value equals the named mistake |
| l6-gauss | quiz[0].widget.wrong[fifty] | slip 1250: You paired to make 50. Each pair is $1 + 50 = 51$. | correct | script A: slip value equals the named mistake |
| l6-gauss | quiz[1].widget.answer | key 100 | correct | script A: recomputed |
| l6-gauss | quiz[1].widget.wrong[no-half] | slip 200: 200 counts each term twice. Halve it. | correct | script A: slip value equals the named mistake |
| l6-gauss | quiz[1].widget.wrong[nine] | slip 90: You used 9 terms. $1, 3, \dots, 19$ has $\tfrac{19 - 1}{2} + 1 = 10$. | correct | script A: slip value equals the named mistake |
| l6-gauss | quiz[1].widget.wrong[evens] | slip 110: 110 is the sum of the first ten even numbers, $2 + 4 + \dots + 20$. | correct | script A: slip value equals the named mistake |
| l6-gauss | quiz[2].widget.options[right] | key: 17 | correct | derivation on reading; figures in script A or C |
| l6-gauss | quiz[2].widget.options[steps] | wrong option: 16 / 16 is the number of steps of 3 from 12 to 60. The terms are one more than the steps. | correct | wrong under every reading; why line checked |
| l6-gauss | quiz[2].widget.options[eighteen] | wrong option: 18 / You added 2 to the steps. Steps plus 1 gives the terms. | correct | wrong under every reading; why line checked |
| l6-gauss | quiz[2].widget.options[diff] | wrong option: 48 / 48 is $60 - 12$, the distance. Each step covers 3 of it. | correct | wrong under every reading; why line checked |
| l6-gauss | quiz[3].widget.answer | key 1100 | correct | script A: recomputed |
| l6-gauss | quiz[3].widget.wrong[no-half] | slip 2200: 2,200 counts each term twice. Halve it. | correct | script A: slip value equals the named mistake |
| l6-gauss | quiz[3].widget.wrong[diff] | slip 900: You used $80 - 8$. Pairs add the ends, they do not subtract them. | correct | script A: slip value equals the named mistake |
| l7-shifted-copy | screens[2].prose | geometric series; multiply by r and shift | correct | Pearson Edexcel A level Pure Year 2 ch. 3 s3.4 |
| l7-shifted-copy | screens[5].explain | exponent of the last term is n - 1, not n | correct | first term a r^0 |
| l7-shifted-copy | screens[6].widget | S = a(r^n - 1)/(r - 1), dividing allowed when r != 1 | correct | Pearson Edexcel A level Pure Year 2 ch. 3 s3.4 |
| l7-shifted-copy | screens[7].prose | two forms of S_n; at r = 1 the sum is na | correct | derivation |
| l7-shifted-copy | screens[8].prose | annuity: payment at the end of each year; value today C/1.04^k | correct | Hull, Options, Futures and Other Derivatives ch. 4; convention stated |
| l7-shifted-copy | summary.formula | geometric series formula, r != 1 | correct | Pearson Edexcel A level Pure Year 2 ch. 3 s3.4 |
| l7-shifted-copy | screens[0].widget.answer | key 255 | correct | script A: recomputed |
| l7-shifted-copy | screens[0].widget.wrong[last] | slip 128: £128.00 is the round 8 stake alone. The total adds all eight rounds. | correct | script A: slip value equals the named mistake |
| l7-shifted-copy | screens[0].widget.wrong[next] | slip 256: £256.00 would be the round 9 stake. The eight stakes add to £1.00 less. | correct | script A: slip value equals the named mistake |
| l7-shifted-copy | screens[0].widget.wrong[seven] | slip 127: You added seven rounds and left out the last stake. Include round 8's £128.00. | correct | script A: slip value equals the named mistake |
| l7-shifted-copy | screens[0].widget.wrong[eight-times] | slip 1024: You multiplied the last stake by 8. The earlier stakes are much smaller than £128.00. | correct | script A: slip value equals the named mistake |
| l7-shifted-copy | screens[1].widget.options[right] | key: It is the seventh stake minus the first stake | correct | derivation on reading; figures in script A or C |
| l7-shifted-copy | screens[1].widget.options[equal] | wrong option: It equals the seventh stake / Look at the caption with a first stake of £1.00: the total is £63. | correct | wrong under every reading; why line checked |
| l7-shifted-copy | screens[1].widget.options[half] | wrong option: It is half the seventh stake / Half the seventh stake is the sixth stake. The total is nearly tw | correct | wrong under every reading; why line checked |
| l7-shifted-copy | screens[1].widget.options[six] | wrong option: It is six times the first stake / You treated the stakes as equal. They double each round, so si | correct | wrong under every reading; why line checked |
| l7-shifted-copy | screens[2].widget.options[right] | key: $32 - 1$ | correct | derivation on reading; figures in script A or C |
| l7-shifted-copy | screens[2].widget.options[no-one] | wrong option: $32$ / You cancelled the matching terms but dropped the 1. The top line's 1 has no partner below | correct | wrong under every reading; why line checked |
| l7-shifted-copy | screens[2].widget.options[short] | wrong option: $16 - 1$ / You stopped at the last term of $S$. The bottom line ends at 32, one place further ri | correct | wrong under every reading; why line checked |
| l7-shifted-copy | screens[2].widget.options[first] | wrong option: $2 - 1$ / You subtracted the first column only. Every column takes part, and the middle ones can | correct | wrong under every reading; why line checked |
| l7-shifted-copy | screens[3].widget.answer | key 242 | correct | script A: recomputed |
| l7-shifted-copy | screens[3].widget.wrong[no-divide] | slip 484: 484 is $3S - S$, which is $2S$. Halve it to get $S$. | correct | script A: slip value equals the named mistake |
| l7-shifted-copy | screens[3].widget.wrong[next] | slip 486: 486 is the next term. The sum is less than that. | correct | script A: slip value equals the named mistake |
| l7-shifted-copy | screens[3].widget.wrong[triple] | slip 726: 726 is $3S$, the shifted line. The question asks for $S$. | correct | script A: slip value equals the named mistake |
| l7-shifted-copy | screens[4].widget.answer | key 93 | correct | script A: recomputed |
| l7-shifted-copy | screens[4].widget.wrong[no-double] | slip 46.5: 46.5 is $S - \tfrac12 S$, which is half of $S$. Double it. | correct | script A: slip value equals the named mistake |
| l7-shifted-copy | screens[4].widget.wrong[forever] | slip 96: 96 is what the total approaches if the halving goes on forever. This sum stops after five terms. | correct | script A: slip value equals the named mistake |
| l7-shifted-copy | screens[4].widget.wrong[ends] | slip 49.5: You added the two leftover ends. The 1.5 is taken away, not added. | correct | script A: slip value equals the named mistake |
| l7-shifted-copy | screens[5].widget.answer | key 1533 | correct | script A: recomputed |
| l7-shifted-copy | screens[5].widget.wrong[eight] | slip 765: You used 8 terms because $768 = 3 \times 2^8$. The powers run from $2^0$ to $2^8$: that is nine stak | correct | script A: slip value equals the named mistake |
| l7-shifted-copy | screens[5].widget.wrong[next] | slip 1536: £1,536.00 is $2 \times 768$, the next stake. Shift and subtract leaves that minus the first stake,  | correct | script A: slip value equals the named mistake |
| l7-shifted-copy | screens[5].widget.wrong[ten] | slip 3069: You used 10 stakes. Powers 0 to 8 give nine. | correct | script A: slip value equals the named mistake |
| l7-shifted-copy | screens[5].widget.wrong[last] | slip 768: £768.00 is the last stake alone. | correct | script A: slip value equals the named mistake |
| l7-shifted-copy | screens[7].widget.options[right] | key: 60 | correct | derivation on reading; figures in script A or C |
| l7-shifted-copy | screens[7].widget.options[none] | wrong option: There is no sum: the formula gives $\tfrac{0}{0}$ / The formula fails at $r = 1$ because its las | correct | wrong under every reading; why line checked |
| l7-shifted-copy | screens[7].widget.options[zero] | wrong option: 0 / You put $r = 1$ into the top of the formula only. Twelve 5s cannot add to 0. | correct | wrong under every reading; why line checked |
| l7-shifted-copy | screens[7].widget.options[five] | wrong option: 5 / That is one term. There are twelve. | correct | wrong under every reading; why line checked |
| l7-shifted-copy | screens[8].widget.answer | key 4055.45 | correct | script A: recomputed |
| l7-shifted-copy | screens[8].widget.wrong[no-discount] | slip 5000: £5,000.00 adds the payments at face value. A payment in the future is worth less today. | correct | script A: slip value equals the named mistake |
| l7-shifted-copy | screens[8].widget.wrong[due] | slip 4217.67: £4,217.67 treats the first payment as paid today. Here it arrives after one year, so it is worth | correct | script A: slip value equals the named mistake |
| l7-shifted-copy | screens[8].widget.wrong[nine] | slip 3717.67: You used 9 payments. Years 1 to 10 make 10. | correct | script A: slip value equals the named mistake |
| l7-shifted-copy | screens[8].widget.wrong[end] | slip 3377.82: You discounted all £5,000.00 by ten years. The early payments lose less value than the late ones | correct | script A: slip value equals the named mistake |
| l7-shifted-copy | quiz[0].widget.answer | key 364 | correct | script A: recomputed |
| l7-shifted-copy | quiz[0].widget.wrong[no-divide] | slip 728: 728 is $3S - S = 2S$. Halve it. | correct | script A: slip value equals the named mistake |
| l7-shifted-copy | quiz[0].widget.wrong[seven] | slip 1093: You used 7 terms. $3^0$ to $3^5$ is six. | correct | script A: slip value equals the named mistake |
| l7-shifted-copy | quiz[0].widget.wrong[next] | slip 729: 729 is the next term, $3^6$. | correct | script A: slip value equals the named mistake |
| l7-shifted-copy | quiz[1].widget.options[right] | key: $\tfrac{63}{32}$ | correct | derivation on reading; figures in script A or C |
| l7-shifted-copy | quiz[1].widget.options[two] | wrong option: 2 / 2 is what the total approaches if the halving goes on forever. This sum stops after six term | correct | wrong under every reading; why line checked |
| l7-shifted-copy | quiz[1].widget.options[five] | wrong option: $\tfrac{31}{16}$ / That is the sum of the first five terms. The $\tfrac{1}{32}$ is a sixth. | correct | wrong under every reading; why line checked |
| l7-shifted-copy | quiz[1].widget.options[seven] | wrong option: $\tfrac{127}{64}$ / That has seven terms. Count from 1 to $\tfrac{1}{32}$ again. | correct | wrong under every reading; why line checked |
| l7-shifted-copy | quiz[2].widget.answer | key 1023 | correct | script A: recomputed |
| l7-shifted-copy | quiz[2].widget.wrong[nine] | slip 511: You used 9 terms. $k = 0, 1, \dots, 9$ is ten. | correct | script A: slip value equals the named mistake |
| l7-shifted-copy | quiz[2].widget.wrong[eleven] | slip 2047: You used 11 terms. $k$ stops at 9. | correct | script A: slip value equals the named mistake |
| l7-shifted-copy | quiz[2].widget.wrong[power] | slip 1024: 1024 is $2^{10}$, the next term. The sum is 1 less. | correct | script A: slip value equals the named mistake |
| l7-shifted-copy | quiz[3].widget.answer | key 44 | correct | script A: recomputed |
| l7-shifted-copy | quiz[3].widget.wrong[all-plus] | slip 124: You dropped the minus signs. The ratio is $-2$, so the terms alternate. | correct | script A: slip value equals the named mistake |
| l7-shifted-copy | quiz[3].widget.wrong[no-divide] | slip -132: You stopped at $a(r^n - 1) = -132$. Divide by $r - 1 = -3$. | correct | script A: slip value equals the named mistake |
| l8-adding-forever | screens[0].explain | adding forever can give a finite answer | correct | Spivak, Calculus ch. 23 |
| l8-adding-forever | screens[1].widget.options[right] | partial sums of 1 + r + r^2 ... settle exactly for -1 < r < 1 | correct | Spivak, Calculus ch. 23 (geometric series) |
| l8-adding-forever | screens[1].feedback.correct | only -1 < r < 1 makes the terms shrink to nothing (given as the test for settling) | misleading | true for geometric series only; shrinking terms do not make a series settle (harmonic, script D). Finding 2 |
| l8-adding-forever | screens[1].explain | settling needs the terms to shrink | correct | Spivak, Calculus ch. 23 (vanishing condition, necessary) |
| l8-adding-forever | screens[2].explain | sum to infinity = level the partial sums settle on; converges | correct | Spivak, Calculus ch. 23 definition |
| l8-adding-forever | screens[5].explain | the shift assumes S is a finite number; needs -1 < r < 1 | correct | Spivak, Calculus ch. 23 |
| l8-adding-forever | screens[6].prose | /r/ < 1: S = a/(1-r); /r/ >= 1: diverges | correct | Pearson Edexcel A level Pure Year 2 ch. 3 s3.5; Spivak, Calculus ch. 23 (a != 0) |
| l8-adding-forever | screens[7].widget | S_n = a/(1-r) - a r^n/(1-r) -> a/(1-r) | correct | Spivak, Calculus ch. 23 |
| l8-adding-forever | screens[8].explain | perpetuity paying c at rate i is worth c/i; first payment in one year | correct | Hull, Options, Futures and Other Derivatives ch. 4; convention stated |
| l8-adding-forever | screens[8].explain | finite value because each payment is worth 1/1.04 of the last | correct | geometric ratio below 1 |
| l8-adding-forever | summary.ideas | a series has a sum when its partial sums settle; geometric settles exactly when -1 < r < 1 | correct | Spivak, Calculus ch. 23 |
| l8-adding-forever | quiz[2].widget.options[zero] | a sum that depends on grouping has no value | correct | Spivak, Calculus ch. 23 (a convergent series keeps its sum under grouping) |
| l8-adding-forever | quiz[1].widget | 0.333... is exactly 1/3 | correct | a/(1-r) = 0.3/0.9 |
| l8-adding-forever | screens[0].widget.options[right] | key: No: it gets as close to 1 as you like, but never passes it | correct | derivation on reading; figures in script A or C |
| l8-adding-forever | screens[0].widget.options[passes] | wrong option: Yes: adding forever must eventually pass any number / You assumed endless adding means an endles | correct | wrong under every reading; why line checked |
| l8-adding-forever | screens[0].widget.options[stops] | wrong option: No, because it stops growing after a few steps / It never stops growing: each step adds a little | correct | wrong under every reading; why line checked |
| l8-adding-forever | screens[0].widget.options[reaches] | wrong option: Yes: after enough steps it reaches 1 and then goes past / Every step leaves an unshaded piece, h | correct | wrong under every reading; why line checked |
| l8-adding-forever | screens[1].widget.options[right] | key: When $r$ is strictly between −1 and 1 | correct | derivation on reading; figures in script A or C |
| l8-adding-forever | screens[1].widget.options[positive] | wrong option: For every positive $r$ / At $r = 1$ every term is 1, so the sums climb 1, 2, 3, ... and never se | correct | wrong under every reading; why line checked |
| l8-adding-forever | screens[1].widget.options[pos-only] | wrong option: Only when $r$ is between 0 and 1 / At $r = -0.5$ the sums zigzag, but the zigzag shrinks onto 0. | correct | wrong under every reading; why line checked |
| l8-adding-forever | screens[1].widget.options[all] | wrong option: For every $r$ on the slider / At $r = -1$ the sums flip 1, 0, 1, 0 for ever. At $r = 1$ they cli | correct | wrong under every reading; why line checked |
| l8-adding-forever | screens[2].widget.answer | key 1.5 | correct | script A: recomputed |
| l8-adding-forever | screens[2].widget.wrong[no-scale] | slip 1: 1 is $S - \tfrac13 S$, which is two thirds of $S$. Divide by $\tfrac23$. | correct | script A: slip value equals the named mistake |
| l8-adding-forever | screens[2].widget.wrong[flip] | slip 3: You divided 1 by $\tfrac13$. The bottom of the fraction is $1 - \tfrac13$. | correct | script A: slip value equals the named mistake |
| l8-adding-forever | screens[2].widget.wrong[third] | slip 0.6667: You multiplied by $\tfrac23$ instead of dividing by it. | correct | script A: slip value equals the named mistake |
| l8-adding-forever | screens[3].widget.answer | key 9 | correct | script A: recomputed |
| l8-adding-forever | screens[3].widget.wrong[by-r] | slip 18: You divided 6 by $\tfrac13$. The shift leaves $(1 - \tfrac13)S = 6$. | correct | script A: slip value equals the named mistake |
| l8-adding-forever | screens[3].widget.wrong[plus] | slip 4.5: You divided by $1 + \tfrac13$. The copy is taken away, so it is $1 - \tfrac13$. | correct | script A: slip value equals the named mistake |
| l8-adding-forever | screens[3].widget.wrong[no-a] | slip 1.5: 1.5 is the sum when the first term is 1. Here every term is 6 times bigger. | correct | script A: slip value equals the named mistake |
| l8-adding-forever | screens[4].widget.answer | key 5.3333 | correct | script A: recomputed |
| l8-adding-forever | screens[4].widget.wrong[no-sign] | slip 16: 16 is $8 + 4 + 2 + \dots$, with every sign made positive. The minus signs pull the sum down. | correct | script A: slip value equals the named mistake |
| l8-adding-forever | screens[4].widget.wrong[first] | slip 8: 8 is the first term. The next term takes 4 away. | correct | script A: slip value equals the named mistake |
| l8-adding-forever | screens[4].widget.wrong[half] | slip 4: 4 is $S_2$, the second dot. The zigzag keeps going and settles higher. | correct | script A: slip value equals the named mistake |
| l8-adding-forever | screens[5].widget.options[claim] | wrong option: $-1$, as the working shows / You trusted the working. It treats $S$ as a number, but the partial | correct | wrong under every reading; why line checked |
| l8-adding-forever | screens[5].widget.options[right] | key: It has no finite value | correct | derivation on reading; figures in script A or C |
| l8-adding-forever | screens[5].widget.options[last] | wrong option: About 63, where the dots stop / The picture stops at six terms, but the sums keep doubling: 127, | correct | wrong under every reading; why line checked |
| l8-adding-forever | screens[5].widget.options[two] | wrong option: 2, since the ratio is 2 / The ratio is how each term compares with the last. It is not the total | correct | wrong under every reading; why line checked |
| l8-adding-forever | screens[6].widget.options[shrink] | key: $5 + 4 + 3.2 + 2.56 + \dots$ | correct | derivation on reading; figures in script A or C |
| l8-adding-forever | screens[6].widget.options[alt] | key: $10 - 9 + 8.1 - 7.29 + \dots$ | correct | derivation on reading; figures in script A or C |
| l8-adding-forever | screens[6].widget.options[minus-one] | wrong option: $1 - 1 + 1 - 1 + \dots$ / Here $r = -1$. The partial sums flip between 1 and 0 for ever, so ther | correct | wrong under every reading; why line checked |
| l8-adding-forever | screens[6].widget.options[one] | wrong option: $3 + 3 + 3 + \dots$ / Here $r = 1$. The sums grow by 3 each time without limit. | correct | wrong under every reading; why line checked |
| l8-adding-forever | screens[6].widget.options[grow] | wrong option: $2 + 3 + 4.5 + 6.75 + \dots$ / Here $r = 1.5$. Each term is bigger than the last, so the sums gr | correct | wrong under every reading; why line checked |
| l8-adding-forever | screens[8].widget.answer | key 125 | correct | script A: recomputed |
| l8-adding-forever | screens[8].widget.wrong[today] | slip 130: £130.00 counts a payment today as well. The first payment comes after one year, so $a = \tfrac{5}{1. | correct | script A: slip value equals the named mistake |
| l8-adding-forever | screens[8].widget.wrong[one] | slip 4.81: £4.81 is the first payment alone. The bond pays every year, forever. | correct | script A: slip value equals the named mistake |
| l8-adding-forever | screens[8].widget.wrong[extra] | slip 120.19: You discounted the whole sum by one more year. $a = \tfrac{5}{1.04}$ already does that once. | correct | script A: slip value equals the named mistake |
| l8-adding-forever | quiz[0].widget.answer | key 24 | correct | script A: recomputed |
| l8-adding-forever | quiz[0].widget.wrong[plus] | slip 8: You divided by $1 + 0.5$. The formula has $1 - r$ on the bottom. | correct | script A: slip value equals the named mistake |
| l8-adding-forever | quiz[0].widget.wrong[first] | slip 12: 12 is the first term. The rest add another 12. | correct | script A: slip value equals the named mistake |
| l8-adding-forever | quiz[1].widget.options[right] | key: $\tfrac13$ | correct | derivation on reading; figures in script A or C |
| l8-adding-forever | quiz[1].widget.options[under] | wrong option: Just under $\tfrac13$ / You stopped adding at some point. Forever, the 3s never end and the sum  | correct | wrong under every reading; why line checked |
| l8-adding-forever | quiz[1].widget.options[first] | wrong option: $\tfrac{3}{10}$ / That is the first term only. | correct | wrong under every reading; why line checked |
| l8-adding-forever | quiz[1].widget.options[plus] | wrong option: $\tfrac{3}{11}$ / You divided by $1 + \tfrac{1}{10}$. The bottom is $1 - \tfrac{1}{10}$. | correct | wrong under every reading; why line checked |
| l8-adding-forever | quiz[2].widget.options[right] | key: It has none | correct | derivation on reading; figures in script A or C |
| l8-adding-forever | quiz[2].widget.options[half] | wrong option: $\tfrac12$ / You put $r = -1$ into $\tfrac{a}{1 - r}$. The formula needs $-1 < r < 1$; here the  | correct | wrong under every reading; why line checked |
| l8-adding-forever | quiz[2].widget.options[zero] | wrong option: 0 / You grouped it as $(1 - 1) + (1 - 1) + \dots$. Grouping as $1 + (-1 + 1) + \dots$ gives 1. A | correct | wrong under every reading; why line checked |
| l8-adding-forever | quiz[2].widget.options[one] | wrong option: 1 / That is one way of grouping. Another gives 0, so neither is the sum. | correct | wrong under every reading; why line checked |
| l8-adding-forever | quiz[3].widget.answer | key 13.3333 | correct | script A: recomputed |
| l8-adding-forever | quiz[3].widget.wrong[no-sign] | slip 40: 40 is the sum with every sign positive. The ratio is $-0.5$. | correct | script A: slip value equals the named mistake |
| l8-adding-forever | quiz[3].widget.wrong[first] | slip 20: 20 is the first term. The next term takes 10 away. | correct | script A: slip value equals the named mistake |
| l8-adding-forever | quiz[3].widget.wrong[half] | slip 10: 10 is the second partial sum. The zigzag settles higher. | correct | script A: slip value equals the named mistake |
| review-2 | items[6].widget | 0.999... is exactly 1 | correct | a/(1-r) = 0.9/0.9; Spivak, Calculus ch. 23 |
| review-2 | items[0].widget.answer | key 58 | correct | script A: recomputed |
| review-2 | items[0].widget.wrong[from-one] | slip 60: You started at $k = 1$. The sigma starts at $k = 2$. | correct | script A: slip value equals the named mistake |
| review-2 | items[0].widget.wrong[no-one] | slip 54: You added the squares and dropped the $+1$ in every term. | correct | script A: slip value equals the named mistake |
| review-2 | items[0].widget.wrong[one-once] | slip 55: You added the 1 only once. Every one of the four terms has its own $+1$. | correct | script A: slip value equals the named mistake |
| review-2 | items[1].widget.answer | key 26 | correct | script A: recomputed |
| review-2 | items[1].widget.wrong[gap] | slip 25: $30 - 5 = 25$ counts the steps between months. Add 1 for the terms. | correct | script A: slip value equals the named mistake |
| review-2 | items[1].widget.wrong[top] | slip 30: 30 counts from month 1. The sum starts at month 5. | correct | script A: slip value equals the named mistake |
| review-2 | items[2].widget.answer | key 10100 | correct | script A: recomputed |
| review-2 | items[2].widget.wrong[half-terms] | slip 5050: 5,050 is $1 + 2 + \dots + 100$. Each even number is twice one of those, so the sum is doubled. | correct | script A: slip value equals the named mistake |
| review-2 | items[2].widget.wrong[no-half] | slip 20200: 20,200 counts each term twice. Halve it. | correct | script A: slip value equals the named mistake |
| review-2 | items[2].widget.wrong[hundred-hundred] | slip 10000: You used 100 terms of 100 each. The average term is $\tfrac{2 + 200}{2} = 101$. | correct | script A: slip value equals the named mistake |
| review-2 | items[3].widget.answer | key 1090 | correct | script A: recomputed |
| review-2 | items[3].widget.wrong[nineteen] | slip 1035.5: You used 19 terms, from $(102 - 7) \div 5$. That counts the steps; there are 20 terms. | correct | script A: slip value equals the named mistake |
| review-2 | items[3].widget.wrong[no-half] | slip 2180: 2,180 counts each term twice. Halve it. | correct | script A: slip value equals the named mistake |
| review-2 | items[3].widget.wrong[twentyone] | slip 1144.5: You used 21 terms. Steps plus 1 is $19 + 1 = 20$. | correct | script A: slip value equals the named mistake |
| review-2 | items[4].widget.answer | key 5465 | correct | script A: recomputed |
| review-2 | items[4].widget.wrong[six] | slip 1820: You used 6 terms because the last power is 6. Powers 0 to 6 make 7 terms. | correct | script A: slip value equals the named mistake |
| review-2 | items[4].widget.wrong[no-divide] | slip 10930: 10,930 is $3S - S = 2S$. Halve it. | correct | script A: slip value equals the named mistake |
| review-2 | items[4].widget.wrong[eight] | slip 16400: You used 8 terms. Powers 0 to 6 make 7. | correct | script A: slip value equals the named mistake |
| review-2 | items[5].widget.answer | key 1268.25 | correct | script A: recomputed |
| review-2 | items[5].widget.wrong[simple] | slip 1200: £1,200.00 charges £100.00 every month. Each charge is 1% of a growing loan, so the charges grow. | correct | script A: slip value equals the named mistake |
| review-2 | items[5].widget.wrong[balance] | slip 11268.25: £11,268.25 is the loan after a year. The interest is that minus the £10,000.00 borrowed. | correct | script A: slip value equals the named mistake |
| review-2 | items[5].widget.wrong[eleven] | slip 1156.68: You used 11 months. Months 1 to 12 make 12 charges. | correct | script A: slip value equals the named mistake |
| review-2 | items[6].widget.options[right] | key: Exactly 1 | correct | derivation on reading; figures in script A or C |
| review-2 | items[6].widget.options[under] | wrong option: Just under 1 / You stopped adding at some point. With the nines going on forever, the sum is exa | correct | wrong under every reading; why line checked |
| review-2 | items[6].widget.options[first] | wrong option: $\tfrac{9}{10}$ / That is the first term only. | correct | wrong under every reading; why line checked |
| review-2 | items[6].widget.options[none] | wrong option: It has no sum, since there are infinitely many terms / Infinitely many terms can have a finite s | correct | wrong under every reading; why line checked |
| review-2 | items[7].widget.answer | key 6.25 | correct | script A: recomputed |
| review-2 | items[7].widget.wrong[two] | slip 4.0: 4.0 adds the first two minutes only. The moves go on forever, shrinking. | correct | script A: slip value equals the named mistake |
| review-2 | items[7].widget.wrong[by-r] | slip 4.1667: You divided by 0.6. The bottom of the formula is $1 - 0.6 = 0.4$. | correct | script A: slip value equals the named mistake |
| review-2 | items[7].widget.wrong[plus] | slip 1.5625: You divided by $1 + 0.6$. The formula has $1 - r$ on the bottom. | correct | script A: slip value equals the named mistake |
| review-2 | items[8].widget.options[right] | key: None | correct | derivation on reading; figures in script A or C |
| review-2 | items[8].widget.options[formula] | wrong option: $-6$ / You put $r = 1.5$ into $\tfrac{a}{1 - r}$. That formula needs $-1 < r < 1$; positive term | correct | wrong under every reading; why line checked |
| review-2 | items[8].widget.options[six] | wrong option: 6 / You dropped the sign from $\tfrac{3}{-0.5}$. The series has no sum at all, since each term i | correct | wrong under every reading; why line checked |
| review-2 | items[8].widget.options[first] | wrong option: 3 / 3 is the first term. The others add more. | correct | wrong under every reading; why line checked |
| homework-2 | items[5].widget | perpetuity proof: (1+i)V = c + V, V = c/i; shift safe since 1/(1+i) < 1 | correct | derivation; convergence stated |
| homework-2 | items[7].model | annuity A £15,372.45, perpetuity B £20,000, difference = B discounted 30 years | correct | script C |
| homework-2 | items[4].prose | loan payment: first payment one month away | correct | convention stated |
| homework-2 | items[0].widget.answer | key 4k+1 and accept list | correct | derivation: tested at n or x = 1, 2, 3 |
| homework-2 | items[0].widget.wrong[no-start] | slip 4k: $4k$ gives 4, 8, ..., 40: one less than each term. | correct | derivation: not equal to the key; feedback value checked |
| homework-2 | items[0].widget.wrong[swap] | slip k+4: $k + 4$ rises by 1 each time. These terms rise by 4. | correct | derivation: not equal to the key; feedback value checked |
| homework-2 | items[0].widget.wrong[five] | slip 4k+5: $4k + 5$ gives 9 at $k = 1$. It starts one term too late. | correct | derivation: not equal to the key; feedback value checked |
| homework-2 | items[1].widget.answer | key 0.99 | correct | script A: recomputed |
| homework-2 | items[1].widget.wrong[forever] | slip 1: 1 is the sum to infinity. Stopping at $k = 99$ leaves $-\tfrac{1}{100}$ uncancelled. | correct | script A: slip value equals the named mistake |
| homework-2 | items[1].widget.wrong[hundred] | slip 0.990099: That is $1 - \tfrac{1}{101}$, the sum up to $k = 100$. The last term here is $\tfrac{1}{99} - \ | correct | script A: slip value equals the named mistake |
| homework-2 | items[1].widget.wrong[first] | slip 0.5: 0.5 is the first term, $\tfrac{1}{1 \times 2}$. | correct | script A: slip value equals the named mistake |
| homework-2 | items[2].widget.answer | key 23 | correct | script A: recomputed |
| homework-2 | items[2].widget.wrong[short] | slip 22: 22 terms give $22 \times 45 = 990$, still below 1,000. | correct | script A: slip value equals the named mistake |
| homework-2 | items[2].widget.wrong[terms] | slip 250: You found the term near 1,000. The question is about the running total. | correct | script A: slip value equals the named mistake |
| homework-2 | items[3].widget.answer | key 9 | correct | script A: recomputed |
| homework-2 | items[3].widget.wrong[last-only] | slip 10: The tenth stake, £2,560.00, is below £5,000.00 on its own. But the first nine stakes have already cos | correct | script A: slip value equals the named mistake |
| homework-2 | items[3].widget.wrong[divide] | slip 1000: You divided £5,000.00 by £5.00. The stakes double, so they use the money up far faster. | correct | script A: slip value equals the named mistake |
| homework-2 | items[3].widget.wrong[eight] | slip 8: Eight losses cost £1,275.00. A ninth stake of £1,280.00 still fits. | correct | script A: slip value equals the named mistake |
| homework-2 | items[4].widget.answer | key 443.21 | correct | script A: recomputed |
| homework-2 | items[4].widget.wrong[no-interest] | slip 416.67: £416.67 is £10,000.00 split into 24 parts, with no interest. | correct | script A: slip value equals the named mistake |
| homework-2 | items[4].widget.wrong[simple] | slip 466.67: £466.67 adds 0.5% of £10,000.00 for each of 24 months and splits it. Interest falls as the loan i | correct | script A: slip value equals the named mistake |
| homework-2 | items[4].widget.wrong[due] | slip 441.0: That treats the first payment as made today. It comes one month from now. | correct | script A: slip value equals the named mistake |
| homework-2 | items[6].widget.answer | key \frac{3}{11} and accept list | correct | derivation: tested at n or x = 1, 2, 3 |
| homework-2 | items[6].widget.wrong[first] | slip \frac{27}{100}: That is the first term only. The 27s go on forever. | correct | derivation: not equal to the key; feedback value checked |
| homework-2 | items[6].widget.wrong[plus] | slip \frac{27}{101}: You divided by $1 + \tfrac{1}{100}$. The bottom is $1 - \tfrac{1}{100}$. | correct | derivation: not equal to the key; feedback value checked |
| homework-2 | items[7].model | longform model answer and rubric | correct | script C recomputes every figure |
| problems-2 | items[2].parts[3] | ball travels 5 + 2 x 7.5 = 20 m before rest | correct | derivation (idealised bounces) |
| problems-2 | items[3].parts[4].explain | payments shrinking by a fixed ratio can add up to less than what is owed | correct | S_inf = 2000 < 3000 |
| problems-2 | items[0].parts[0].widget.answer | key 53 | correct | script A: recomputed |
| problems-2 | items[0].parts[0].widget.wrong[n-steps] | slip 58: That adds 10 steps of 5. Row 10 is 9 steps below row 1: $8 + 45 = 53$. | correct | script A: slip value equals the named mistake |
| problems-2 | items[0].parts[0].widget.wrong[step-only] | slip 50: 50 is $10 \times 5$ alone. Start from the 8 in the top row: $8 + 9 \times 5 = 53$. | correct | script A: slip value equals the named mistake |
| problems-2 | items[0].parts[1].widget.answer | key 305 | correct | script A: recomputed |
| problems-2 | items[0].parts[1].widget.wrong[no-halve] | slip 610: 610 is two copies of the display. Halve it: $\tfrac{10}{2}(8 + 53) = 305$. | correct | script A: slip value equals the named mistake |
| problems-2 | items[0].parts[1].widget.wrong[last-only] | slip 265: That is $\tfrac{10}{2} \times 53$, which leaves out the top row's 8. Each pair adds to $8 + 53 = 61$ | correct | script A: slip value equals the named mistake |
| problems-2 | items[0].parts[1].widget.wrong[n-steps] | slip 330: That uses $2a + nd = 16 + 50$. The formula has $n - 1$ steps: $\tfrac{10}{2}(16 + 9 \times 5) = 305$ | correct | script A: slip value equals the named mistake |
| problems-2 | items[0].parts[2].widget.answer | key 7 | correct | script A: recomputed |
| problems-2 | items[0].parts[2].widget.wrong[subtract] | slip 6: $10 - 4 = 6$ leaves out one end. Rows 4 to 10 are $10 - 4 + 1 = 7$ rows. | correct | script A: slip value equals the named mistake |
| problems-2 | items[0].parts[2].widget.wrong[top] | slip 10: 10 is where $k$ stops, not how many terms there are. The sum starts at $k = 4$: $10 - 4 + 1 = 7$. | correct | script A: slip value equals the named mistake |
| problems-2 | items[0].parts[3].widget.answer | key 266 | correct | script A: recomputed |
| problems-2 | items[0].parts[3].widget.wrong[six-rows] | slip 228: That pairs 6 rows. The stand has 7 rows: $\tfrac{7}{2}(23 + 53) = 266$. | correct | script A: slip value equals the named mistake |
| problems-2 | items[0].parts[3].widget.wrong[four-left] | slip 243: You took away rows 1 to 4, 62 tins. Row 4 stays on the stand: take away rows 1 to 3, which is 39. | correct | script A: slip value equals the named mistake |
| problems-2 | items[0].parts[3].widget.wrong[full] | slip 305: 305 is the full display of 10 rows. The stand has only rows 4 to 10. | correct | script A: slip value equals the named mistake |
| problems-2 | items[1].parts[0].widget.answer | key 12500 | correct | script A: recomputed |
| problems-2 | items[1].parts[0].widget.wrong[power-n] | slip 62500: That is $4 \times 5^6$, which is day 7. Day 6 has five factors of 5: 12500. | correct | script A: slip value equals the named mistake |
| problems-2 | items[1].parts[0].widget.wrong[day-five] | slip 2500: 2500 is day 5. One more day multiplies it by 5: 12500. | correct | script A: slip value equals the named mistake |
| problems-2 | items[1].parts[1].widget.answer | key 15624 | correct | script A: recomputed |
| problems-2 | items[1].parts[1].widget.wrong[no-divide-4] | slip 62496: 62496 is $5S - S$, which is $4S$. Divide by 4: $S = 15624$. | correct | script A: slip value equals the named mistake |
| problems-2 | items[1].parts[1].widget.wrong[no-first] | slip 15625: You left out the first term. $5S - S$ is the new last term $62500$ minus the first term 4, which i | correct | script A: slip value equals the named mistake |
| problems-2 | items[1].parts[2].widget.answer | key 5^{n}-1 and accept list | correct | derivation: tested at n or x = 1, 2, 3 |
| problems-2 | items[1].parts[2].widget.wrong[no-divide] | slip 4\cdot5^{n}-4: That is $5S_n - S_n$, which is $4S_n$. Divide by $r - 1 = 4$: $S_n = 5^n - 1$. | correct | derivation: not equal to the key; feedback value checked |
| problems-2 | items[1].parts[2].widget.wrong[power-n-1] | slip 5^{n-1}-1: The shifted copy ends at $4 \times 5^n$, one power past the last term. So $S_n = 5^n - 1$, and | correct | derivation: not equal to the key; feedback value checked |
| problems-2 | items[1].parts[2].widget.wrong[sign] | slip 1-5^{n}: That is below 0 for every $n$. With $r = 5$ use $\dfrac{a(r^n - 1)}{r - 1}$, which is $5^n - 1$. | correct | derivation: not equal to the key; feedback value checked |
| problems-2 | items[1].parts[3].widget.answer | key 8 | correct | script A: recomputed |
| problems-2 | items[1].parts[3].widget.wrong[one-day] | slip 9: Day 9 is when one day's new users pass 350,000. The total passes it a day sooner: $S_8 = 390624$. | correct | script A: slip value equals the named mistake |
| problems-2 | items[1].parts[3].widget.wrong[day-before] | slip 7: $S_7 = 5^7 - 1 = 78124$, well short of 350,000. Day 8 gives 390,624. | correct | script A: slip value equals the named mistake |
| problems-2 | items[2].parts[0].widget.answer | key 7.42442 | correct | script A: recomputed |
| problems-2 | items[2].parts[0].widget.wrong[forever] | slip 7.5: 7.5 m is the total of all the rises, forever. Nine rises leave out a little: $7.5(1 - 0.6^9) \approx | correct | script A: slip value equals the named mistake |
| problems-2 | items[2].parts[0].widget.wrong[ten] | slip 7.45467: That adds 10 rises. With $n = 9$: $7.5(1 - 0.6^9) \approx 7.42$. | correct | script A: slip value equals the named mistake |
| problems-2 | items[2].parts[0].widget.wrong[eight] | slip 7.37403: That adds 8 rises. With $n = 9$: $7.5(1 - 0.6^9) \approx 7.42$. | correct | script A: slip value equals the named mistake |
| problems-2 | items[2].parts[1].widget.answer | key 19.84884 | correct | script A: recomputed |
| problems-2 | items[2].parts[1].widget.wrong[once] | slip 12.42: That counts each rise once. The ball goes up and comes back down: $5 + 2 \times 7.42 = 19.84$. | correct | script A: slip value equals the named mistake |
| problems-2 | items[2].parts[1].widget.wrong[no-drop] | slip 14.84884: That leaves out the first 5 m fall. Add it: $5 + 14.84 = 19.84$. | correct | script A: slip value equals the named mistake |
| problems-2 | items[2].parts[1].widget.wrong[double-drop] | slip 24.84884: The first 5 m is fallen once, not climbed. Only the rises are doubled: $5 + 2 \times 7.42 = 19. | correct | script A: slip value equals the named mistake |
| problems-2 | items[2].parts[2].widget.answer | key 7.5 | correct | script A: recomputed |
| problems-2 | items[2].parts[2].widget.wrong[whole] | slip 12.5: That is $\tfrac{5}{0.4}$, which starts from the 5 m drop. The rises start at 3 m: $\tfrac{3}{0.4} = | correct | script A: slip value equals the named mistake |
| problems-2 | items[2].parts[2].widget.wrong[divide-r] | slip 5: You divided by $r$. The sum to infinity divides by $1 - r = 0.4$: $\tfrac{3}{0.4} = 7.5$. | correct | script A: slip value equals the named mistake |
| problems-2 | items[2].parts[2].widget.wrong[second] | slip 4.5: That starts from the second rise, 1.8 m. The first rise is 3 m: $\tfrac{3}{0.4} = 7.5$. | correct | script A: slip value equals the named mistake |
| problems-2 | items[2].parts[3].widget.answer | key 20 | correct | script A: recomputed |
| problems-2 | items[2].parts[3].widget.wrong[once] | slip 12.5: That counts each rise once. The ball goes up and down each time: $5 + 2 \times 7.5 = 20$. | correct | script A: slip value equals the named mistake |
| problems-2 | items[2].parts[3].widget.wrong[no-drop] | slip 15: That leaves out the first 5 m fall. Add it: $5 + 15 = 20$. | correct | script A: slip value equals the named mistake |
| problems-2 | items[2].parts[3].widget.wrong[double-drop] | slip 25: The first 5 m is fallen once, not climbed. Only the rises are doubled: $5 + 15 = 20$. | correct | script A: slip value equals the named mistake |
| problems-2 | items[3].parts[0].widget.answer | key 5n^2+45n and accept list | correct | derivation: tested at n or x = 1, 2, 3 |
| problems-2 | items[3].parts[0].widget.wrong[last-term] | slip 5n^2+50n: That uses $50 + 10n$ as the last payment. Month $n$ pays $50 + 10(n - 1)$, so $S_n = 5n^2 + 45n | correct | derivation: not equal to the key; feedback value checked |
| problems-2 | items[3].parts[0].widget.wrong[no-halve] | slip 10n^2+90n: That is two copies of the total. Halve it: $S_n = 5n^2 + 45n$. | correct | derivation: not equal to the key; feedback value checked |
| problems-2 | items[3].parts[0].widget.wrong[one-month] | slip 10n+40: $10n + 40$ is the payment in month $n$ alone. The question asks for the total so far. | correct | derivation: not equal to the key; feedback value checked |
| problems-2 | items[3].parts[1].widget.answer | key 21 | correct | script A: recomputed |
| problems-2 | items[3].parts[1].widget.wrong[twenty] | slip 20: $S_{20} = 2900$, still £100 short. The debt is cleared during month 21. | correct | script A: slip value equals the named mistake |
| problems-2 | items[3].parts[1].widget.wrong[flat] | slip 60: That is $3000 \div 50$, as if every payment were £50. The payments rise by £10 a month, so it takes 2 | correct | script A: slip value equals the named mistake |
| problems-2 | items[3].parts[2].widget.answer | key 2000 | correct | script A: recomputed |
| problems-2 | items[3].parts[2].widget.wrong[ar] | slip 1800: That starts from month 2's £180. The first payment is £200: $\tfrac{200}{0.1} = 2000$. | correct | script A: slip value equals the named mistake |
| problems-2 | items[3].parts[2].widget.wrong[divide-r] | slip 222.22: You divided by $r$. Divide by $1 - r = 0.1$: $\tfrac{200}{0.1} = 2000$. | correct | script A: slip value equals the named mistake |
| problems-2 | items[3].parts[2].widget.wrong[plus] | slip 105.26: You divided by $1 + r$. The sum to infinity divides by $1 - r = 0.1$: 2000. | correct | script A: slip value equals the named mistake |
| problems-2 | items[3].parts[3].widget.answer | key 1781.16 | correct | script A: recomputed |
| problems-2 | items[3].parts[3].widget.wrong[twenty] | slip 1756.85: That adds 20 payments. Month 21 is the 21st: $2000(1 - 0.9^{21}) \approx 1781$. | correct | script A: slip value equals the named mistake |
| problems-2 | items[3].parts[3].widget.wrong[forever] | slip 2000: £2,000 is the total forever. By month 21 a little is still to come: $2000(1 - 0.9^{21}) \approx 178 | correct | script A: slip value equals the named mistake |
| problems-2 | items[3].parts[3].widget.wrong[left] | slip 218.84: That is $2000 \times 0.9^{21}$, what plan B pays after month 21. By month 21 it has paid $2000 -  | correct | script A: slip value equals the named mistake |
| problems-2 | items[3].parts[4].widget.answer | key 1218.84 | correct | script A: recomputed |
| problems-2 | items[3].parts[4].widget.wrong[forever] | slip 1000: £1,000 is what plan B never repays, even forever. At month 21 it still owes $3000 - 1781 = 1219$. | correct | script A: slip value equals the named mistake |
| problems-2 | items[3].parts[4].widget.wrong[twenty] | slip 1243.15: That uses 20 months of plan B. At month 21 it still owes $3000 - 1781 = 1219$. | correct | script A: slip value equals the named mistake |
| problems-2 | items[3].parts[4].widget.wrong[paid] | slip 1781.16: £1,781 is what plan B has repaid. The question asks what is still owed: $3000 - 1781 = 1219$. | correct | script A: slip value equals the named mistake |
| fluency-l6-gauss | families[one-to-n].widget.answer | key {sum} over the whole range | correct | script B: brute-force sweep of every admissible case |
| fluency-l6-gauss | families[one-to-n].wrong[not-halved] | You added the sum forwards and backwards. That counts every term twice, so halve it. | correct | script B: value equals the named mistake, never the key |
| fluency-l6-gauss | families[one-to-n].wrong[one-term-short] | You worked out $\dfrac{{{m} \times {mm}}}{{2}}$. Each pair is $1 + {m} = {mp}$, not {mm}. | correct | script B: value equals the named mistake, never the key |
| fluency-l6-gauss | families[first-n-terms].widget.answer | key {sum} over the whole range | correct | script B: brute-force sweep of every admissible case |
| fluency-l6-gauss | families[first-n-terms].wrong[not-halved] | You forgot to halve. Forwards plus backwards counts the sum twice. | correct | script B: value equals the named mistake, never the key |
| fluency-l6-gauss | families[first-n-terms].wrong[k-steps] | You used {k} steps of $d$. The last of {k} terms is only {km} steps after the first. | imprecise | value right, but equals the not-halved slip when 2a + (k-2)d = 0 (53 of 9,708 cases), so the wrong line shows. Finding 7 |
| fluency-l6-gauss | families[up-to-last-term].widget.answer | key {sum} over the whole range | correct | script B: brute-force sweep of every admissible case |
| fluency-l6-gauss | families[up-to-last-term].wrong[counted-steps] | You used {km} terms, which is the number of steps. There are {k} terms, one more than the steps. | correct | script B: value equals the named mistake, never the key |
| fluency-l6-gauss | families[up-to-last-term].wrong[not-halved] | You forgot to halve. Forwards plus backwards counts the sum twice. | correct | script B: value equals the named mistake, never the key |
| fluency-l7-shifted-copy | families[first-n-terms].widget.answer | key {sum} over the whole range | correct | script B: brute-force sweep of every admissible case |
| fluency-l7-shifted-copy | families[first-n-terms].wrong[one-term-short] | You used $r^{{{km}}}$, which adds only {km} terms. For {k} terms the power is {k}. | correct | script B: value equals the named mistake, never the key |
| fluency-l7-shifted-copy | families[first-n-terms].wrong[sign-flipped] | You mixed the two forms of $S_n$. Use $r^n - 1$ over $r - 1$, or $1 - r^n$ over $1 - r$. | correct | script B: value equals the named mistake, never the key |
| fluency-l7-shifted-copy | families[up-to-last-term].widget.answer | key {sum} over the whole range | correct | script B: brute-force sweep of every admissible case |
| fluency-l7-shifted-copy | families[up-to-last-term].wrong[counted-steps] | You left out the last term, {l}. The last term is $ar^{{{km}}}$, so there are {k} terms. | correct | script B: value equals the named mistake, never the key |
| fluency-l7-shifted-copy | families[up-to-last-term].wrong[sign-flipped] | You mixed the two forms of $S_n$. Use $r^n - 1$ over $r - 1$, or $1 - r^n$ over $1 - r$. | correct | script B: value equals the named mistake, never the key |
| fluency-l7-shifted-copy | families[sigma-powers].widget.answer | key {sum} over the whole range | correct | script B: brute-force sweep of every admissible case |
| fluency-l7-shifted-copy | families[sigma-powers].wrong[stopped-early] | You stopped one term early. The top limit, $k = {t}$, is included. | correct | script B: value equals the named mistake, never the key |
| fluency-l7-shifted-copy | families[sigma-powers].wrong[one-term-extra] | You added one term too many. $k$ runs from {b} to {t}, which is {cnt} terms. | correct | script B: value equals the named mistake, never the key |
| fluency-l8-adding-forever | families[from-the-terms].widget.answer | key {sum} over the whole range | correct | script B: brute-force sweep of every admissible case |
| fluency-l8-adding-forever | families[from-the-terms].wrong[sign-of-r] | You divided by $1 + r$. The rule is $\dfrac{{a}}{{1 - r}}$, and here $r = {r:frac}$. | correct | script B: value equals the named mistake, never the key |
| fluency-l8-adding-forever | families[from-the-terms].wrong[first-term-left-out] | You worked out $\dfrac{{1}}{{1 - r}}$. Multiply it by the first term, {a}. | correct | script B: value equals the named mistake, never the key |
| fluency-l8-adding-forever | families[from-a-and-r].widget.answer | key {sum} over the whole range | correct | script B: brute-force sweep of every admissible case |
| fluency-l8-adding-forever | families[from-a-and-r].wrong[sign-of-r] | You divided by $1 + r$. The rule is $\dfrac{{a}}{{1 - r}}$, and here $r = {r:frac}$. | correct | script B: value equals the named mistake, never the key |
| fluency-l8-adding-forever | families[from-a-and-r].wrong[first-term-left-out] | You worked out $\dfrac{{1}}{{1 - r}}$. Multiply it by the first term, {a}. | correct | script B: value equals the named mistake, never the key |
| fluency-l8-adding-forever | families[perpetual-bond].widget.answer | key {val} over the whole range | correct | script B: brute-force sweep of every admissible case |
| fluency-l8-adding-forever | families[perpetual-bond].wrong[payment-today] | You counted a payment today. The first payment is a year away, so the first term is $\tfrac{{{c}}}{{{g}}}$. | correct | script B: value equals the named mistake, never the key |
| fluency-l8-adding-forever | families[perpetual-bond].wrong[per-cent-not-decimal] | You divided by {i}. The rate is {i}%, which is {ir} as a decimal. | correct | script B: value equals the named mistake, never the key |
| fluency-l8-adding-forever | families[recurring-decimal].widget.answer | key {key:frac} over the whole range | correct | script B: brute-force sweep of every admissible case |
| fluency-l8-adding-forever | families[recurring-decimal].wrong[first-term-only] | That is only the first term, $0.{t}{u}$: the pair of digits repeats forever. | correct | script B: value equals the named mistake, never the key |
| fluency-l8-adding-forever | families[recurring-decimal].wrong[sign-of-r] | You divided by $1 + r$. Here $r = 0.01$, so divide by $1 - r = 0.99$. | correct | script B: value equals the named mistake, never the key |
| l9-pascal | screens[0].explain | (a+b)^2 = a^2 + 2ab + b^2 | correct | Pearson Edexcel A level Pure Year 1 ch. 8 s8.1 |
| l9-pascal | screens[1].explain | (a+b)^3 = a^3 + 3a^2b + 3ab^2 + b^3 | correct | Pearson Edexcel A level Pure Year 1 ch. 8 s8.1 |
| l9-pascal | screens[2].explain | each number is the sum of the two above; row 0 is (a+b)^0 = 1 | correct | Pearson Edexcel A level Pure Year 1 ch. 8 s8.1 |
| l9-pascal | screens[5].explain | row n starts 1, n and has n + 1 numbers | correct | C(n,1) = n (n >= 1) |
| l9-pascal | screens[6].prose | (a+b)^n = a^n + n a^(n-1) b + ... + b^n; n + 1 terms | correct | Pearson Edexcel A level Pure Year 1 ch. 8 s8.3 |
| l9-pascal | screens[7].widget | why adding the two above works | correct | derivation |
| l9-pascal | summary.formula.note | row n numbers add to 2^n | correct | (1+1)^n |
| l9-pascal | quiz[1].explain | each row adds to twice the row above | correct | derivation |
| l9-pascal | screens[0].widget.answer | tap-regions key ["c12", "c21"] | correct | derivation on reading |
| l9-pascal | screens[1].widget.answer | tap-regions key ["c12", "c21"] | correct | derivation on reading |
| l9-pascal | screens[2].widget.answer | key 6 | correct | script A: recomputed |
| l9-pascal | screens[2].widget.wrong[copy] | slip 3: You copied a 3 from row 3. The rows grow, so the middle of row 4 is bigger. | correct | script A: slip value equals the named mistake |
| l9-pascal | screens[2].widget.wrong[product] | slip 9: You multiplied the two 3s. Try adding: $1 + 2$ made each 3 in row 3. | correct | script A: slip value equals the named mistake |
| l9-pascal | screens[2].widget.wrong[second] | slip 4: 4 is the second number of row 4, $1 + 3$. The middle number sits under the two 3s. | correct | script A: slip value equals the named mistake |
| l9-pascal | screens[3].widget.answer | tap-regions key ["r6c3"] | correct | derivation on reading |
| l9-pascal | screens[4].widget.answer | key 20 | correct | script A: recomputed |
| l9-pascal | screens[4].widget.wrong[copy] | slip 10: You copied a 10 from row 5. The middle of row 6 is the sum of the two 10s. | correct | script A: slip value equals the named mistake |
| l9-pascal | screens[4].widget.wrong[neighbour] | slip 15: 15 is $5 + 10$, one place to the left. The middle sits under the two 10s. | correct | script A: slip value equals the named mistake |
| l9-pascal | screens[4].widget.wrong[product] | slip 100: You multiplied $10 \times 10$. Add the two numbers above instead. | correct | script A: slip value equals the named mistake |
| l9-pascal | screens[5].widget.options[fourth] | wrong option: $1, 3, 3, 1$ / You counted the top 1 as row 1. That 1 is $(a + b)^0$, so the fourth row down is  | correct | wrong under every reading; why line checked |
| l9-pascal | screens[5].widget.options[right] | key: $1, 4, 6, 4, 1$ | correct | derivation on reading; figures in script A or C |
| l9-pascal | screens[5].widget.options[six] | wrong option: $1, 4, 6, 6, 4, 1$ / You gave $(a + b)^4$ six terms. It has five, from $a^4$ down to $b^4$. | correct | wrong under every reading; why line checked |
| l9-pascal | screens[5].widget.options[fifth] | wrong option: $1, 5, 10, 10, 5, 1$ / That row starts 1, 5, so it is $(a + b)^5$. The second number of row $n$  | correct | wrong under every reading; why line checked |
| l9-pascal | screens[6].widget.options[two] | wrong option: 2 / You kept only $a^7$ and $b^7$. The mixed terms, from $a^6b$ to $ab^6$, are there too. | correct | wrong under every reading; why line checked |
| l9-pascal | screens[6].widget.options[seven] | wrong option: 7 / You counted the powers of $a$ from 7 down to 1. The last term, $b^7$, has $a^0$ and counts t | correct | wrong under every reading; why line checked |
| l9-pascal | screens[6].widget.options[right] | key: 8 | correct | derivation on reading; figures in script A or C |
| l9-pascal | screens[6].widget.options[fourteen] | wrong option: 14 / You doubled 7. Each row has just one more number than the row above. | correct | wrong under every reading; why line checked |
| l9-pascal | screens[8].widget.answer | key 6 | correct | script A: recomputed |
| l9-pascal | screens[8].widget.wrong[all] | slip 16: That is every path. Only paths with 2 up days and 2 down days end at £100.00. | correct | script A: slip value equals the named mistake |
| l9-pascal | screens[8].widget.wrong[four] | slip 4: 4 counts the paths with exactly one up day. To end level you need two. | correct | script A: slip value equals the named mistake |
| l9-pascal | screens[8].widget.wrong[two] | slip 2: You counted up, up, down, down and its reverse. The 2 up days can be any 2 of the 4. | correct | script A: slip value equals the named mistake |
| l9-pascal | screens[8].widget.wrong[one] | slip 1: You counted one order. The 2 up days can fall on any 2 of the 4 days. | correct | script A: slip value equals the named mistake |
| l9-pascal | quiz[0].widget.answer | key 21 | correct | script A: recomputed |
| l9-pascal | quiz[0].widget.wrong[copy] | slip 15: 15 is the third number of row 6. Row 7 adds the 6 and the 15 above it. | correct | script A: slip value equals the named mistake |
| l9-pascal | quiz[0].widget.wrong[next] | slip 35: 35 is $15 + 20$, the fourth number of row 7. | correct | script A: slip value equals the named mistake |
| l9-pascal | quiz[0].widget.wrong[product] | slip 90: You multiplied 6 and 15. Add them instead. | correct | script A: slip value equals the named mistake |
| l9-pascal | quiz[1].widget.options[square] | wrong option: 36 / You squared 6. Add the seven numbers instead. | correct | wrong under every reading; why line checked |
| l9-pascal | quiz[1].widget.options[middle] | wrong option: 20 / That is the middle number alone. Add all seven. | correct | wrong under every reading; why line checked |
| l9-pascal | quiz[1].widget.options[right] | key: 64 | correct | derivation on reading; figures in script A or C |
| l9-pascal | quiz[1].widget.options[double] | wrong option: 12 / You doubled 6. Each row adds to double the row above, and row 5 adds to 32. | correct | wrong under every reading; why line checked |
| l9-pascal | quiz[2].widget.options[right] | key: 10 | correct | derivation on reading; figures in script A or C |
| l9-pascal | quiz[2].widget.options[five] | wrong option: 5 / 5 goes in front of $a^4b$ and $ab^4$. With $b^3$, take the fourth number. | correct | wrong under every reading; why line checked |
| l9-pascal | quiz[2].widget.options[product] | wrong option: 6 / You multiplied the powers 2 and 3. Read the number from row 5. | correct | wrong under every reading; why line checked |
| l9-pascal | quiz[2].widget.options[power] | wrong option: 3 / You used the power of $b$ alone. The number comes from row 5. | correct | wrong under every reading; why line checked |
| l9-pascal | quiz[3].widget.options[grow] | wrong option: $210, 252, 210$ / You expected the numbers to keep growing. A row rises to the middle, then fall | correct | wrong under every reading; why line checked |
| l9-pascal | quiz[3].widget.options[short] | wrong option: $84, 36, 9$ / You stopped one short. Row 9 has 10 numbers and ends with 1. | correct | wrong under every reading; why line checked |
| l9-pascal | quiz[3].widget.options[right] | key: $36, 9, 1$ | correct | derivation on reading; figures in script A or C |
| l9-pascal | quiz[3].widget.options[copy] | wrong option: $1, 9, 36$ / That is the start in the same order. The end reads the start backwards. | correct | wrong under every reading; why line checked |
| l10-counting-paths | screens[2].prose | n choose k notation; order does not matter | correct | Pearson Edexcel A level Pure Year 1 ch. 8 s8.2 |
| l10-counting-paths | screens[3].explain | 3! = 3 x 2 x 1 orders | correct | definition |
| l10-counting-paths | screens[5].explain | C(10,8) = C(10,2) = 45; counts rise to the middle then fall | correct | symmetry |
| l10-counting-paths | screens[6].prose | C(n,k) = n(n-1)...(n-k+1)/k! | correct | Pearson Edexcel A level Pure Year 1 ch. 8 s8.2 |
| l10-counting-paths | screens[7].widget | C(n,k) = n!/(k!(n-k)!) | correct | Pearson Edexcel A level Pure Year 1 ch. 8 s8.2 |
| l10-counting-paths | screens[8].prose | 5 independent trades at chance 0.5: 32 equally likely sequences | correct | script D Monte Carlo |
| l10-counting-paths | summary.formula.note | 0! = 1 so C(n,0) = C(n,n) = 1 | correct | convention, Pearson Edexcel A level Pure Year 1 ch. 8 s8.2 |
| l10-counting-paths | screens[0].widget.answer | tap-regions key ["a-a-b", "a-b-a", "b-a-a"] | correct | derivation on reading |
| l10-counting-paths | screens[0].widget.wrong[two-b] | slip set: You tapped the paths with two $b$s. Those make $ab^2$. We want exactly one $b$. | correct | derivation on reading |
| l10-counting-paths | screens[1].widget.answer | tap-regions key ["r1c3", "r3c1"] | correct | derivation on reading |
| l10-counting-paths | screens[2].widget.answer | key 6 | correct | script A: recomputed |
| l10-counting-paths | screens[2].widget.wrong[ordered] | slip 12: 12 counts the cells off the diagonal. Each pick appears twice, once in each order. | correct | script A: slip value equals the named mistake |
| l10-counting-paths | screens[2].widget.wrong[all] | slip 16: 16 counts every cell, including the diagonal, where one bracket gives $b$ twice. | correct | script A: slip value equals the named mistake |
| l10-counting-paths | screens[2].widget.wrong[half-all] | slip 8: You halved all 16 cells. Take out the 4 diagonal cells first. | correct | script A: slip value equals the named mistake |
| l10-counting-paths | screens[2].widget.wrong[four] | slip 4: You counted the brackets. We want pairs of brackets. | correct | script A: slip value equals the named mistake |
| l10-counting-paths | screens[3].widget.answer | key 6 | correct | script A: recomputed |
| l10-counting-paths | screens[3].widget.wrong[three] | slip 3: You counted the first picks only. Each first pick leaves 2 orders for the rest. | correct | script A: slip value equals the named mistake |
| l10-counting-paths | screens[3].widget.wrong[nine] | slip 9: You multiplied 3 by 3. After the first pick only 2 brackets are left, then 1. | correct | script A: slip value equals the named mistake |
| l10-counting-paths | screens[3].widget.wrong[two] | slip 2: You counted the orders after one first pick. There are 3 first picks. | correct | script A: slip value equals the named mistake |
| l10-counting-paths | screens[4].widget.answer | key 10 | correct | script A: recomputed |
| l10-counting-paths | screens[4].widget.wrong[ordered] | slip 60: 60 counts each set 6 times, once for each order. | correct | script A: slip value equals the named mistake |
| l10-counting-paths | screens[4].widget.wrong[third] | slip 20: You divided by 3. Each set has $3! = 6$ orders, not 3. | correct | script A: slip value equals the named mistake |
| l10-counting-paths | screens[4].widget.wrong[half] | slip 30: You divided by 2, as for pairs. A set of three has 6 orders. | correct | script A: slip value equals the named mistake |
| l10-counting-paths | screens[4].widget.wrong[product] | slip 15: You multiplied 5 by 3. Count the ordered picks, then divide by the orders. | correct | script A: slip value equals the named mistake |
| l10-counting-paths | screens[5].widget.options[more] | wrong option: $\binom{10}{8}$, because 8 is more picks / You expected more picks to mean more ways. Picking 8  | correct | wrong under every reading; why line checked |
| l10-counting-paths | screens[5].widget.options[fewer] | wrong option: $\binom{10}{2}$, because 8 picks are harder to arrange / You expected the bigger pick to be rare | correct | wrong under every reading; why line checked |
| l10-counting-paths | screens[5].widget.options[right] | key: They are equal | correct | derivation on reading; figures in script A or C |
| l10-counting-paths | screens[6].widget.options[right] | key: 15 | correct | derivation on reading; figures in script A or C |
| l10-counting-paths | screens[6].widget.options[ordered] | wrong option: 30 / You stopped at $6 \times 5$. Divide by $2! = 2$ for the two orders. | correct | wrong under every reading; why line checked |
| l10-counting-paths | screens[6].widget.options[times] | wrong option: 12 / You multiplied 6 by 2. The top is $6 \times 5$: two factors counting down. | correct | wrong under every reading; why line checked |
| l10-counting-paths | screens[6].widget.options[divide] | wrong option: 3 / You divided 6 by 2. The top is $6 \times 5$, not 6. | correct | wrong under every reading; why line checked |
| l10-counting-paths | screens[8].widget.answer | key 0.3125 | correct | script A: recomputed |
| l10-counting-paths | screens[8].widget.wrong[count] | slip 10: 10 is the number of sequences. Divide by the 32 equally likely sequences. | correct | script A: slip value equals the named mistake |
| l10-counting-paths | screens[8].widget.wrong[share] | slip 0.6: You took 3 out of 5. Count the win-loss sequences with 3 wins instead. | correct | script A: slip value equals the named mistake |
| l10-counting-paths | screens[8].widget.wrong[cube] | slip 0.125: You worked out $0.5^3$ for the 3 wins alone. The 2 losses and the order count too. | correct | script A: slip value equals the named mistake |
| l10-counting-paths | screens[8].widget.wrong[one-seq] | slip 0.03125: That is one sequence, such as win, win, win, loss, loss. There are $\binom{5}{3} = 10$ of them. | correct | script A: slip value equals the named mistake |
| l10-counting-paths | quiz[0].widget.answer | key 21 | correct | script A: recomputed |
| l10-counting-paths | quiz[0].widget.wrong[ordered] | slip 42: 42 counts each pair twice, once in each order. Divide by 2. | correct | script A: slip value equals the named mistake |
| l10-counting-paths | quiz[0].widget.wrong[times] | slip 14: You multiplied 7 by 2. The top is $7 \times 6$. | correct | script A: slip value equals the named mistake |
| l10-counting-paths | quiz[0].widget.wrong[square] | slip 49: You picked from 7 twice, allowing the same bracket twice. The second pick has only 6 choices. | correct | script A: slip value equals the named mistake |
| l10-counting-paths | quiz[1].widget.options[zero] | wrong option: 0 / You counted no ways. Taking $a$ from every bracket is one way: it gives the $a^6$ term. | correct | wrong under every reading; why line checked |
| l10-counting-paths | quiz[1].widget.options[right] | key: 1 | correct | derivation on reading; figures in script A or C |
| l10-counting-paths | quiz[1].widget.options[six] | wrong option: 6 / 6 counts the ways to pick exactly one bracket. Picking none can be done only one way. | correct | wrong under every reading; why line checked |
| l10-counting-paths | quiz[1].widget.options[fact] | wrong option: 720 / 720 is $6!$, the orders of all six brackets. Picking none leaves nothing to order. | correct | wrong under every reading; why line checked |
| l10-counting-paths | quiz[2].widget.options[right] | key: $\binom{12}{3}$ | correct | derivation on reading; figures in script A or C |
| l10-counting-paths | quiz[2].widget.options[nine] | wrong option: $\binom{9}{3}$ / You changed the 12 as well. The pick is still from all 12 brackets. | correct | wrong under every reading; why line checked |
| l10-counting-paths | quiz[2].widget.options[four] | wrong option: $\binom{12}{4}$ / Leaving 9 for $b$ leaves $12 - 9 = 3$ for $a$, not 4. | correct | wrong under every reading; why line checked |
| l10-counting-paths | quiz[2].widget.options[ordered] | wrong option: $\dfrac{12!}{9!}$ / That is $12 \times 11 \times 10$, the ordered picks of 3. Divide by $3!$ as  | correct | wrong under every reading; why line checked |
| l10-counting-paths | quiz[3].widget.answer | key 0.375 | correct | script A: recomputed |
| l10-counting-paths | quiz[3].widget.wrong[half] | slip 0.5: You took 2 heads out of 4 flips. Count the head-tail sequences with 2 heads instead. | correct | script A: slip value equals the named mistake |
| l10-counting-paths | quiz[3].widget.wrong[square] | slip 0.25: You worked out $0.5^2$ for the two heads alone. The two tails and the order count too. | correct | script A: slip value equals the named mistake |
| l10-counting-paths | quiz[3].widget.wrong[one-seq] | slip 0.0625: That is one sequence, such as HHTT. There are $\binom{4}{2} = 6$ of them. | correct | script A: slip value equals the named mistake |
| l11-powers-of-a-bracket | screens[2].prose | general term C(n,k) a^(n-k) b^k | correct | Pearson Edexcel A level Pure Year 1 ch. 8 s8.3 |
| l11-powers-of-a-bracket | screens[6].explain | (a+b)^n always has mixed terms once n >= 2 | correct | as a polynomial identity |
| l11-powers-of-a-bracket | screens[7].prose | binomial theorem in sigma notation | correct | Pearson Edexcel A level Pure Year 1 ch. 8 s8.3 |
| l11-powers-of-a-bracket | screens[8].widget | justification of the general term by counting picks | correct | derivation |
| l11-powers-of-a-bracket | screens[9].explain | simple interest is the first two pieces of 1000(1.04)^3 | correct | derivation |
| l11-powers-of-a-bracket | screens[0].widget.answer | tap-regions key ["x-x-two", "x-two-x", "two-x-x"] | correct | derivation on reading |
| l11-powers-of-a-bracket | screens[0].widget.wrong[x-once] | slip set: Those paths pick $x$ once and 2 twice. They make $4x$, not an $x^2$ term. | correct | derivation on reading |
| l11-powers-of-a-bracket | screens[1].widget.options[x3] | wrong option: $x^3$ / $x^3$ has 1 in front: only one path picks $x$ every time. | correct | wrong under every reading; why line checked |
| l11-powers-of-a-bracket | screens[1].widget.options[x2] | wrong option: $6x^2$ / You expected the middle of the row to win. The powers of 2 grow too: $3 \times 4 = 12$  | correct | wrong under every reading; why line checked |
| l11-powers-of-a-bracket | screens[1].widget.options[right] | key: $12x$ | correct | derivation on reading; figures in script A or C |
| l11-powers-of-a-bracket | screens[1].widget.options[eight] | wrong option: $8$ / 8 is $2^3$, but only one path makes it. | correct | wrong under every reading; why line checked |
| l11-powers-of-a-bracket | screens[2].widget.answer | key x^3+9x^2+27x+27 and accept list | correct | derivation: tested at n or x = 1, 2, 3 |
| l11-powers-of-a-bracket | screens[2].widget.wrong[no-count] | slip x^3+3x^2+9x+27: You used the powers of 3 but dropped the counts. Three paths give $x^2$, so it is $3 \tim | correct | derivation: not equal to the key; feedback value checked |
| l11-powers-of-a-bracket | screens[2].widget.wrong[ends] | slip x^3+27: You kept only $x^3$ and $3^3$. The six mixed paths give $9x^2 + 27x$. | correct | derivation: not equal to the key; feedback value checked |
| l11-powers-of-a-bracket | screens[3].widget.answer | key 24 | correct | script A: recomputed |
| l11-powers-of-a-bracket | screens[3].widget.wrong[no-square] | slip 12: You used $2x^2$ for $(2x)^2$. The 2 is squared too: $(2x)^2 = 4x^2$. | correct | script A: slip value equals the named mistake |
| l11-powers-of-a-bracket | screens[3].widget.wrong[no-count] | slip 4: You found $(2x)^2 = 4x^2$ but dropped the count. Six paths give this term. | correct | script A: slip value equals the named mistake |
| l11-powers-of-a-bracket | screens[3].widget.wrong[cubed] | slip 48: You used $(2x)^3$. The $x^2$ term takes $2x$ from just 2 brackets. | correct | script A: slip value equals the named mistake |
| l11-powers-of-a-bracket | screens[3].widget.wrong[count] | slip 6: 6 is the count alone. Each of those paths is worth $4x^2$. | correct | script A: slip value equals the named mistake |
| l11-powers-of-a-bracket | screens[4].widget.answer | key -108 | correct | script A: recomputed |
| l11-powers-of-a-bracket | screens[4].widget.wrong[sign] | slip 108: You dropped the sign. An odd power of $-3$ is negative: $(-3)^3 = -27$. | correct | script A: slip value equals the named mistake |
| l11-powers-of-a-bracket | screens[4].widget.wrong[square] | slip 36: You used $(-3)^2 = 9$. This term takes $-3$ from three brackets. | correct | script A: slip value equals the named mistake |
| l11-powers-of-a-bracket | screens[4].widget.wrong[no-count] | slip -27: You found $(-3)^3 = -27$ but dropped the count. Four paths give this term. | correct | script A: slip value equals the named mistake |
| l11-powers-of-a-bracket | screens[4].widget.wrong[sq-neg] | slip -36: You used $3^2$ with a minus. This term takes $-3$ from three brackets: $(-3)^3$. | correct | script A: slip value equals the named mistake |
| l11-powers-of-a-bracket | screens[5].widget.answer | key 24 | correct | script A: recomputed |
| l11-powers-of-a-bracket | screens[5].widget.wrong[no-power] | slip 12: You used 2 for $\left(\tfrac{2}{x}\right)^2$. The 2 is squared as well: 4. | correct | script A: slip value equals the named mistake |
| l11-powers-of-a-bracket | screens[5].widget.wrong[count] | slip 6: 6 is the count alone. Each path is worth $x^2 \times \tfrac{4}{x^2} = 4$. | correct | script A: slip value equals the named mistake |
| l11-powers-of-a-bracket | screens[5].widget.wrong[all-twos] | slip 16: You took $2^4$, as if every bracket gave $\tfrac{2}{x}$. Then $x^{-4}$ is left over. | correct | script A: slip value equals the named mistake |
| l11-powers-of-a-bracket | screens[5].widget.wrong[wrong-k] | slip 32: You used $k = 3$: $\binom{4}{3} \times 2^3 = 32$, but that term is $\tfrac{32}{x^2}$. The powers of $ | correct | script A: slip value equals the named mistake |
| l11-powers-of-a-bracket | screens[6].widget.options[nothing] | wrong option: Nothing: a power shares out over a sum / You raised each part to the power on its own. That keep | correct | wrong under every reading; why line checked |
| l11-powers-of-a-bracket | screens[6].widget.options[counts] | wrong option: $3x^2 + 3x$ / You counted the mixed paths but forgot their 2s. Each $x^2$ path is $2x^2$ and eac | correct | wrong under every reading; why line checked |
| l11-powers-of-a-bracket | screens[6].widget.options[one-middle] | wrong option: $6x$, a middle term as in a square / You expected one middle term. A cube has two mixed kinds: $ | correct | wrong under every reading; why line checked |
| l11-powers-of-a-bracket | screens[6].widget.options[right] | key: $6x^2 + 12x$ | correct | derivation on reading; figures in script A or C |
| l11-powers-of-a-bracket | screens[7].widget.options[copy] | wrong option: 3 / You copied the power of $b$. The two powers add to 7. | correct | wrong under every reading; why line checked |
| l11-powers-of-a-bracket | screens[7].widget.options[right] | key: 4 | correct | derivation on reading; figures in script A or C |
| l11-powers-of-a-bracket | screens[7].widget.options[seven] | wrong option: 7 / Each term has 7 factors in all, shared between $a$ and $b$. | correct | wrong under every reading; why line checked |
| l11-powers-of-a-bracket | screens[7].widget.options[sum] | wrong option: 10 / You added 7 and 3. The powers add to 7, so $a$ gets $7 - 3$. | correct | wrong under every reading; why line checked |
| l11-powers-of-a-bracket | screens[9].widget.answer | key 4.864 | correct | script A: recomputed |
| l11-powers-of-a-bracket | screens[9].widget.wrong[total] | slip 124.864: That is all the interest. Simple interest already pays £120.00 of it. | correct | script A: slip value equals the named mistake |
| l11-powers-of-a-bracket | screens[9].widget.wrong[no-cube] | slip 4.8: You left out the $(0.04)^3$ piece, interest on interest on interest. It adds about £0.06. | correct | script A: slip value equals the named mistake |
| l11-powers-of-a-bracket | screens[9].widget.wrong[no-three] | slip 1.664: You used $(0.04)^2$ once. It comes with a count of 3: $\binom{3}{2} = 3$. | correct | script A: slip value equals the named mistake |
| l11-powers-of-a-bracket | screens[9].widget.wrong[all] | slip 1124.864: That is the whole balance. Give only the part beyond simple interest. | correct | script A: slip value equals the named mistake |
| l11-powers-of-a-bracket | quiz[0].widget.answer | key 40 | correct | script A: recomputed |
| l11-powers-of-a-bracket | quiz[0].widget.wrong[no-power] | slip 10: 10 is the count alone. Each path also carries $2^2 = 4$. | correct | script A: slip value equals the named mistake |
| l11-powers-of-a-bracket | quiz[0].widget.wrong[once] | slip 20: You used 2 once. Two brackets give 2, so the factor is $2^2 = 4$. | correct | script A: slip value equals the named mistake |
| l11-powers-of-a-bracket | quiz[0].widget.wrong[cubed] | slip 80: You used $2^3$. With $x^3$, only $5 - 3 = 2$ brackets give 2. | correct | script A: slip value equals the named mistake |
| l11-powers-of-a-bracket | quiz[1].widget.options[right] | key: $1 - 4x + 6x^2 - 4x^3 + x^4$ | correct | derivation on reading; figures in script A or C |
| l11-powers-of-a-bracket | quiz[1].widget.options[all-neg] | wrong option: $1 - 4x - 6x^2 - 4x^3 - x^4$ / You made every term negative. Even powers of $-x$ are positive. | correct | wrong under every reading; why line checked |
| l11-powers-of-a-bracket | quiz[1].widget.options[no-sign] | wrong option: $1 + 4x + 6x^2 + 4x^3 + x^4$ / You dropped the minus. Odd powers of $-x$ are negative. | correct | wrong under every reading; why line checked |
| l11-powers-of-a-bracket | quiz[1].widget.options[sam] | wrong option: $1 - x^4$ / You raised each part to the fourth power. The mixed terms are missing, and $(-x)^4 = | correct | wrong under every reading; why line checked |
| l11-powers-of-a-bracket | quiz[2].widget.answer | key 160 | correct | script A: recomputed |
| l11-powers-of-a-bracket | quiz[2].widget.wrong[count] | slip 20: 20 is the count alone. Each path also carries $(2x)^3 = 8x^3$. | correct | script A: slip value equals the named mistake |
| l11-powers-of-a-bracket | quiz[2].widget.wrong[once] | slip 40: You used 2 once. The $2x$ is cubed, so the factor is 8. | correct | script A: slip value equals the named mistake |
| l11-powers-of-a-bracket | quiz[2].widget.wrong[all] | slip 64: You took $2^6$, as if every bracket gave $2x$. Then $x^6$ is left over. | correct | script A: slip value equals the named mistake |
| l11-powers-of-a-bracket | quiz[3].widget.answer | key 270 | correct | script A: recomputed |
| l11-powers-of-a-bracket | quiz[3].widget.wrong[wrong-power] | slip 90: You used $3^2$. The 3 comes from the brackets that do not give $x$: $5 - 2 = 3$ of them. | correct | script A: slip value equals the named mistake |
| l11-powers-of-a-bracket | quiz[3].widget.wrong[once] | slip 30: You used 3 once. Three brackets give 3, so the factor is $3^3 = 27$. | correct | script A: slip value equals the named mistake |
| l11-powers-of-a-bracket | quiz[3].widget.wrong[count] | slip 10: 10 is the count alone. Each path also carries $3^3 = 27$. | correct | script A: slip value equals the named mistake |
| l12-small-x | screens[2].prose | (1+x)^n ~ 1 + nx, close when x is near 0, either side | correct | Pearson Edexcel A level Pure Year 1 ch. 8 s8.5 |
| l12-small-x | screens[3].explain | each term we keep shrinks the error | imprecise | true for the small x of the screen; false for (1 - 0.5)^10 (script D: errors 1.0, 4.0, 7.2). Finding 6 |
| l12-small-x | screens[4].explain | the approximation needs each power of x to shrink the next term | correct | derivation |
| l12-small-x | screens[5].explain | the rule needs nx small, not just x | correct | script C: 1.01^100 = 2.7048 |
| l12-small-x | screens[6].prose | error of 1 + nx is about n(n-1)/2 x^2 when nx is small; halving x quarters it | correct | script C |
| l12-small-x | summary.ideas | fails near x = 1 and for large n | correct | as above |
| l12-small-x | screens[0].widget.options[same] | wrong option: $1.01$ / You treated the power as doing nothing. Each 1% step adds a little more. | correct | wrong under every reading; why line checked |
| l12-small-x | screens[0].widget.options[right] | key: $1.05$ | correct | derivation on reading; figures in script A or C |
| l12-small-x | screens[0].widget.options[shift] | wrong option: $1.5$ / You added 0.1 five times. Each step adds about 0.01, so five steps add about 0.05. | correct | wrong under every reading; why line checked |
| l12-small-x | screens[0].widget.options[times] | wrong option: $5.05$ / You multiplied 1.01 by 5. A power multiplies by 1.01 five times over. | correct | wrong under every reading; why line checked |
| l12-small-x | screens[1].widget.options[right] | key: Near $x = 0$ | correct | derivation on reading; figures in script A or C |
| l12-small-x | screens[1].widget.options[right-end] | wrong option: At the right end, $x = 0.3$ / The gap is largest there, about 1.21. The extra terms grow quickly | correct | wrong under every reading; why line checked |
| l12-small-x | screens[1].widget.options[left-end] | wrong option: At the left end, $x = -0.3$ / The gap there is about 0.67. Slide towards 0 and it shrinks. | correct | wrong under every reading; why line checked |
| l12-small-x | screens[1].widget.options[same] | wrong option: The gap is the same everywhere / Slide to each end and to 0. The gap is near 0 in the middle and | correct | wrong under every reading; why line checked |
| l12-small-x | screens[2].widget.answer | key 0.92 | correct | script A: recomputed |
| l12-small-x | screens[2].widget.wrong[sign] | slip 1.08: You took $x = +0.02$. 0.98 is below 1, so $x = -0.02$. | correct | script A: slip value equals the named mistake |
| l12-small-x | screens[2].widget.wrong[no-n] | slip 0.98: You left out the power. Four steps of $-2\%$ take off about 0.08. | correct | script A: slip value equals the named mistake |
| l12-small-x | screens[2].widget.wrong[times] | slip 3.92: You multiplied 0.98 by 4. The power multiplies 0.98 by itself four times. | correct | script A: slip value equals the named mistake |
| l12-small-x | screens[3].widget.answer | key 1.218 | correct | script A: recomputed |
| l12-small-x | screens[3].widget.wrong[two] | slip 1.2: That is the two-term estimate. Add the third term, $45 \times 0.0004 = 0.018$. | correct | script A: slip value equals the named mistake |
| l12-small-x | screens[3].widget.wrong[no-half] | slip 1.236: You used $10 \times 9 = 90$. $\binom{10}{2}$ divides by 2: it is 45. | correct | script A: slip value equals the named mistake |
| l12-small-x | screens[3].widget.wrong[n-squared] | slip 1.24: You used $10^2 = 100$ for the count. $\binom{10}{2} = \tfrac{10 \times 9}{2} = 45$. | correct | script A: slip value equals the named mistake |
| l12-small-x | screens[4].widget.options[right] | key: The dropped terms are not small | correct | derivation on reading; figures in script A or C |
| l12-small-x | screens[4].widget.options[row] | wrong option: We used the wrong row of Pascal’s triangle / Row 10 is right: 1, 10, 45. The trouble is the term | correct | wrong under every reading; why line checked |
| l12-small-x | screens[4].widget.options[one-more] | wrong option: One more term would fix it / The next term is $120x^3 = 120$, giving 176. That is still far belo | correct | wrong under every reading; why line checked |
| l12-small-x | screens[5].widget.options[small-x] | wrong option: Yes: $x = 0.01$ is small, so $1 + nx$ is accurate / You checked $x$ alone. The $x^2$ term is $\b | correct | wrong under every reading; why line checked |
| l12-small-x | screens[5].widget.options[right] | key: No: $nx = 1$ is not small, so the $x^2$ term, about 0.5, matters | correct | derivation on reading; figures in script A or C |
| l12-small-x | screens[5].widget.options[big-x] | wrong option: No: 0.01 is too big for the rule / 0.01 is small. The trouble is the 100, which makes $nx$ and $ | correct | wrong under every reading; why line checked |
| l12-small-x | screens[6].widget.options[right] | key: It falls to a quarter | correct | derivation on reading; figures in script A or C |
| l12-small-x | screens[6].widget.options[half] | wrong option: It halves / The error grows like $x^2$, not like $x$. Halving $x$ divides $x^2$ by 4. | correct | wrong under every reading; why line checked |
| l12-small-x | screens[6].widget.options[same] | wrong option: It stays the same / The error depends on $x$: it is about $\tfrac{n(n-1)}{2}x^2$. | correct | wrong under every reading; why line checked |
| l12-small-x | screens[6].widget.options[double] | wrong option: It doubles / A smaller $x$ gives a smaller error, not a larger one. | correct | wrong under every reading; why line checked |
| l12-small-x | screens[7].widget.answer | key 1-10x+40x^2 and accept list | correct | derivation: tested at n or x = 1, 2, 3 |
| l12-small-x | screens[7].widget.wrong[no-square] | slip 1-10x+20x^2: You used $-2x^2$ or $2x^2$ for $(-2x)^2$. Square the 2 as well: $4x^2$. | correct | derivation: not equal to the key; feedback value checked |
| l12-small-x | screens[7].widget.wrong[sign] | slip 1-10x-40x^2: $(-2x)^2$ is positive: a square of a negative is positive. | correct | derivation: not equal to the key; feedback value checked |
| l12-small-x | screens[7].widget.wrong[no-count] | slip 1-2x+4x^2: You left out the counts $\binom{5}{1} = 5$ and $\binom{5}{2} = 10$. | correct | derivation: not equal to the key; feedback value checked |
| l12-small-x | screens[8].widget.answer | key 160 | correct | script A: recomputed |
| l12-small-x | screens[8].widget.wrong[no-count] | slip 16: You used $(0.04)^2$ once. It comes with $\binom{5}{2} = 10$. | correct | script A: slip value equals the named mistake |
| l12-small-x | screens[8].widget.wrong[n-squared] | slip 400: You used $5^2 = 25$ for the count. $\binom{5}{2} = 10$. | correct | script A: slip value equals the named mistake |
| l12-small-x | screens[8].widget.wrong[no-half] | slip 320: You used $5 \times 4 = 20$. $\binom{5}{2}$ divides by 2: it is 10. | correct | script A: slip value equals the named mistake |
| l12-small-x | screens[8].widget.wrong[whole] | slip 2166.53: That is all the interest. Simple interest already pays £2,000.00 of it. | correct | script A: slip value equals the named mistake |
| l12-small-x | quiz[0].widget.answer | key 51 | correct | script A: recomputed |
| l12-small-x | quiz[0].widget.wrong[one-day] | slip 50.1: That is one day's rise. Ten days add about $10 \times 0.2\% = 2\%$. | correct | script A: slip value equals the named mistake |
| l12-small-x | quiz[0].widget.wrong[percent] | slip 60: You used $x = 0.02$ a day. 0.2% is 0.002. | correct | script A: slip value equals the named mistake |
| l12-small-x | quiz[0].widget.wrong[gain] | slip 1: That is the gain alone. Add it to the £50.00. | correct | script A: slip value equals the named mistake |
| l12-small-x | quiz[1].widget.options[right] | key: $0.82$ | correct | derivation on reading; figures in script A or C |
| l12-small-x | quiz[1].widget.options[sign] | wrong option: $1.18$ / You took $x = +0.03$. 0.97 is below 1, so $x = -0.03$. | correct | wrong under every reading; why line checked |
| l12-small-x | quiz[1].widget.options[gap] | wrong option: $0.18$ / That is the size of $nx$ alone. Start from 1 and take it off. | correct | wrong under every reading; why line checked |
| l12-small-x | quiz[1].widget.options[same] | wrong option: $0.97$ / You left out the power. Six steps of $-3\%$ take off about 0.18. | correct | wrong under every reading; why line checked |
| l12-small-x | quiz[2].widget.options[tiny] | wrong option: $x = 0.01$ / There the error is about $3(0.01)^2 = 0.0003$, very small. | correct | wrong under every reading; why line checked |
| l12-small-x | quiz[2].widget.options[neg] | wrong option: $x = -0.05$ / There the error is about $3(0.05)^2 = 0.0075$, still small. | correct | wrong under every reading; why line checked |
| l12-small-x | quiz[2].widget.options[tenth] | wrong option: $x = 0.1$ / There the error is $0.031$. It is much bigger further from 0. | correct | wrong under every reading; why line checked |
| l12-small-x | quiz[2].widget.options[right] | key: $x = 0.9$ | correct | derivation on reading; figures in script A or C |
| l12-small-x | quiz[3].widget.answer | key 1.2652 | correct | script A: recomputed |
| l12-small-x | quiz[3].widget.wrong[two] | slip 1.24: That is the two-term estimate. Add $28 \times 0.0009 = 0.0252$. | correct | script A: slip value equals the named mistake |
| l12-small-x | quiz[3].widget.wrong[no-half] | slip 1.2904: You used $8 \times 7 = 56$. $\binom{8}{2} = 28$. | correct | script A: slip value equals the named mistake |
| l13-stream-of-payments | screens[0].explain | discounting: divide by 1.05 per year | correct | Hull, Options, Futures and Other Derivatives ch. 4 |
| l13-stream-of-payments | screens[1].explain | a higher rate shrinks every payment, later ones most (5 years, rates 0 to 20%) | correct | derivation: t(1+r)^-(t+1) rises in t for t < 1/ln 1.2 = 5.5 |
| l13-stream-of-payments | screens[2].prose | present value; ratio 1/1.05 | correct | Hull, Options, Futures and Other Derivatives ch. 4 |
| l13-stream-of-payments | screens[5].explain | finite value because 1.05^-n shrinks to 0 (limit of the partial sums) | correct | Spivak, Calculus ch. 23 |
| l13-stream-of-payments | screens[6].explain | payments at the start of the year: 1.05 x the end-of-year value | correct | script C (annuity due) |
| l13-stream-of-payments | screens[7].widget | S = C/r (1 - (1+r)^-n), first payment in a year | correct | Hull, Options, Futures and Other Derivatives ch. 4; derivation |
| l13-stream-of-payments | screens[8].explain | bond price above 100 because the 5% coupon beats the 4% yield | correct | Hull, Options, Futures and Other Derivatives ch. 4 |
| l13-stream-of-payments | summary.ideas[2] | a never-ending stream has a finite value because the terms shrink to 0 | misleading | wrong reason: terms shrinking to 0 does not give a sum (harmonic series, Spivak, Calculus ch. 23; script D). Finding 1 |
| l13-stream-of-payments | summary.formula.note | for n payments of C, the first one year from today | correct | convention stated |
| l13-stream-of-payments | quiz[3].explain | bond prices fall when yields rise | correct | Hull, Options, Futures and Other Derivatives ch. 4 |
| l13-stream-of-payments | screens[0].widget.answer | key 95.238 | correct | script A: recomputed |
| l13-stream-of-payments | screens[0].widget.wrong[minus] | slip 95: You took 5% off £100.00. But £95.00 grows to only £99.75. Divide by 1.05 instead. | correct | script A: slip value equals the named mistake |
| l13-stream-of-payments | screens[0].widget.wrong[grow] | slip 105: You grew the £100.00 for a year. We want to go back to today, so divide. | correct | script A: slip value equals the named mistake |
| l13-stream-of-payments | screens[0].widget.wrong[same] | slip 100: £100.00 today would grow to £105.00. Money later is worth less than money now. | correct | script A: slip value equals the named mistake |
| l13-stream-of-payments | screens[1].widget.options[first] | wrong option: The year 1 payment / The year 1 payment is divided by $1 + r$ just once. The year 5 payment is d | correct | wrong under every reading; why line checked |
| l13-stream-of-payments | screens[1].widget.options[right] | key: The year 5 payment | correct | derivation on reading; figures in script A or C |
| l13-stream-of-payments | screens[1].widget.options[same] | wrong option: They all lose the same / Each payment is £100.00, but they are discounted different numbers of t | correct | wrong under every reading; why line checked |
| l13-stream-of-payments | screens[2].widget.options[right] | key: $\dfrac{1}{1.05}$ | correct | derivation on reading; figures in script A or C |
| l13-stream-of-payments | screens[2].widget.options[growth] | wrong option: $1.05$ / You used the growth factor. Each later payment is worth less, so the terms shrink. | correct | wrong under every reading; why line checked |
| l13-stream-of-payments | screens[2].widget.options[rate] | wrong option: $0.05$ / 0.05 is the rate. The ratio is what turns one term into the next. | correct | wrong under every reading; why line checked |
| l13-stream-of-payments | screens[2].widget.options[minus] | wrong option: $0.95$ / You took 5% off each time. Dividing by 1.05 multiplies by about 0.952, not 0.95. | correct | wrong under every reading; why line checked |
| l13-stream-of-payments | screens[3].widget.answer | key 432.948 | correct | script A: recomputed |
| l13-stream-of-payments | screens[3].widget.wrong[none] | slip 500: That is $5 \times \text{£}100.00$ with no discounting. Each payment is worth less today. | correct | script A: slip value equals the named mistake |
| l13-stream-of-payments | screens[3].widget.wrong[once] | slip 476.19: You divided all £500.00 by 1.05 once. Later payments are divided more times. | correct | script A: slip value equals the named mistake |
| l13-stream-of-payments | screens[3].widget.wrong[last] | slip 391.76: You discounted all £500.00 by five years. Only the last payment waits that long. | correct | script A: slip value equals the named mistake |
| l13-stream-of-payments | screens[4].widget.options[double] | wrong option: £865.90, twice the five-year value / You doubled the five-year value. Payments 6 to 10 come late | correct | wrong under every reading; why line checked |
| l13-stream-of-payments | screens[4].widget.options[right] | key: £772.17 | correct | derivation on reading; figures in script A or C |
| l13-stream-of-payments | screens[4].widget.options[none] | wrong option: £1,000.00 / That is ten payments with no discounting. | correct | wrong under every reading; why line checked |
| l13-stream-of-payments | screens[4].widget.options[last] | wrong option: £613.91 / You discounted all £1,000.00 by ten years. Only the last payment waits that long. | correct | wrong under every reading; why line checked |
| l13-stream-of-payments | screens[5].widget.answer | key 2000 | correct | script A: recomputed |
| l13-stream-of-payments | screens[5].widget.wrong[due] | slip 2100: You counted a payment today as well. The first one is a year away. | correct | script A: slip value equals the named mistake |
| l13-stream-of-payments | screens[5].widget.wrong[pct] | slip 20: You divided by 5, not 0.05. In the maths, 5% is 0.05. | correct | script A: slip value equals the named mistake |
| l13-stream-of-payments | screens[5].widget.wrong[five] | slip 432.95: That is five years of payments. This stream never stops. | correct | script A: slip value equals the named mistake |
| l13-stream-of-payments | screens[6].widget.options[formula] | wrong option: £432.95 / You used the formula as before. It assumes the first payment is a year away; here it i | correct | wrong under every reading; why line checked |
| l13-stream-of-payments | screens[6].widget.options[right] | key: £454.60 | correct | derivation on reading; figures in script A or C |
| l13-stream-of-payments | screens[6].widget.options[none] | wrong option: £500.00 / That is five payments with no discounting. Four of them are still in the future. | correct | wrong under every reading; why line checked |
| l13-stream-of-payments | screens[6].widget.options[once] | wrong option: £476.19 / You divided all £500.00 by 1.05 once. The first payment is not discounted, and later o | correct | wrong under every reading; why line checked |
| l13-stream-of-payments | screens[8].widget.answer | key 102.775 | correct | script A: recomputed |
| l13-stream-of-payments | screens[8].widget.wrong[none] | slip 115: That adds the cash with no discounting. Each payment is worth less today. | correct | script A: slip value equals the named mistake |
| l13-stream-of-payments | screens[8].widget.wrong[coupons] | slip 13.88: That is the coupons alone. Add the £100.00 repaid in year 3, discounted. | correct | script A: slip value equals the named mistake |
| l13-stream-of-payments | screens[8].widget.wrong[face] | slip 88.9: That is the £100.00 repayment alone. Add the three coupons. | correct | script A: slip value equals the named mistake |
| l13-stream-of-payments | screens[8].widget.wrong[end] | slip 102.23: You discounted every payment by three years. The first two coupons come sooner. | correct | script A: slip value equals the named mistake |
| l13-stream-of-payments | quiz[0].widget.answer | key 184.911 | correct | script A: recomputed |
| l13-stream-of-payments | quiz[0].widget.wrong[simple] | slip 184: You took 8% off. Discounting divides by $1.04^2 = 1.0816$. | correct | script A: slip value equals the named mistake |
| l13-stream-of-payments | quiz[0].widget.wrong[once] | slip 192.31: You discounted for one year. The payment is two years away. | correct | script A: slip value equals the named mistake |
| l13-stream-of-payments | quiz[0].widget.wrong[grow] | slip 216.32: You grew the £200.00 for two years. We want its value today, so divide. | correct | script A: slip value equals the named mistake |
| l13-stream-of-payments | quiz[1].widget.answer | key 2000 | correct | script A: recomputed |
| l13-stream-of-payments | quiz[1].widget.wrong[times] | slip 1.25: You multiplied by the rate. Divide by it. | correct | script A: slip value equals the named mistake |
| l13-stream-of-payments | quiz[1].widget.wrong[pct] | slip 20: You divided by 2.5. In the maths, 2.5% is 0.025. | correct | script A: slip value equals the named mistake |
| l13-stream-of-payments | quiz[1].widget.wrong[due] | slip 2050: You added a payment today. The first payment is a year away. | correct | script A: slip value equals the named mistake |
| l13-stream-of-payments | quiz[2].widget.answer | key 929.275 | correct | script A: recomputed |
| l13-stream-of-payments | quiz[2].widget.wrong[none] | slip 1000: That is $4 \times \text{£}250.00$ with no discounting. | correct | script A: slip value equals the named mistake |
| l13-stream-of-payments | quiz[2].widget.wrong[once] | slip 970.87: You divided all £1,000.00 by 1.03 once. Later payments are divided more times. | correct | script A: slip value equals the named mistake |
| l13-stream-of-payments | quiz[2].widget.wrong[last] | slip 888.49: You discounted all £1,000.00 by four years. Only the last payment waits that long. | correct | script A: slip value equals the named mistake |
| l13-stream-of-payments | quiz[3].widget.options[right] | key: £421.24 | correct | derivation on reading; figures in script A or C |
| l13-stream-of-payments | quiz[3].widget.options[rise] | wrong option: £444.95 / You expected a higher rate to raise the value. A higher rate discounts each payment mo | correct | wrong under every reading; why line checked |
| l13-stream-of-payments | quiz[3].widget.options[same] | wrong option: £432.95 / The payments are the same, but each is now divided by 1.06, not 1.05. | correct | wrong under every reading; why line checked |
| l13-stream-of-payments | quiz[3].widget.options[last] | wrong option: £373.63 / You discounted all £500.00 by five years at 6%. Only the last payment waits that long. | correct | wrong under every reading; why line checked |
| review-3 | items[8].explain | far-off payments gain the most from the cut | imprecise | true in proportion only; the gain in pounds peaks near year 23 and then falls to 0 (script D). Finding 5 |
| review-3 | items[4].explain | C/r is an upper bound for the 20-year pension | correct | derivation |
| review-3 | items[0].widget.answer | key 56 | correct | script A: recomputed |
| review-3 | items[0].widget.wrong[copy] | slip 35: 35 is the fourth number of row 7. Row 8 adds the 21 and the 35 above it. | correct | script A: slip value equals the named mistake |
| review-3 | items[0].widget.wrong[middle] | slip 70: 70 is $35 + 35$, the middle of row 8. The fourth number is one place earlier. | correct | script A: slip value equals the named mistake |
| review-3 | items[0].widget.wrong[third] | slip 28: 28 is $7 + 21$, the third number of row 8. | correct | script A: slip value equals the named mistake |
| review-3 | items[1].widget.answer | key 126 | correct | script A: recomputed |
| review-3 | items[1].widget.wrong[ordered] | slip 3024: 3,024 counts each basket once per order. A basket is the same in any order, so divide by $4! = 24$. | correct | script A: slip value equals the named mistake |
| review-3 | items[1].widget.wrong[times] | slip 36: You multiplied 9 by 4. The ordered picks are $9 \times 8 \times 7 \times 6$. | correct | script A: slip value equals the named mistake |
| review-3 | items[1].widget.wrong[power] | slip 6561: $9^4$ lets the same share be picked four times. | correct | script A: slip value equals the named mistake |
| review-3 | items[2].widget.options[right] | key: $216$ | correct | derivation on reading; figures in script A or C |
| review-3 | items[2].widget.options[sign] | wrong option: $-216$ / You kept the minus. $(-2)^2 = +4$: an even power of a negative is positive. | correct | wrong under every reading; why line checked |
| review-3 | items[2].widget.options[no-two] | wrong option: $54$ / You left out $(-2)^2$. The term takes $-2$ from the other 2 brackets. | correct | wrong under every reading; why line checked |
| review-3 | items[2].widget.options[no-three] | wrong option: $24$ / You left out $3^2$. The 3 is squared with the $x$. | correct | wrong under every reading; why line checked |
| review-3 | items[3].widget.answer | key 1.1048 | correct | script A: recomputed |
| review-3 | items[3].widget.wrong[two] | slip 1.1: That is the two-term estimate. Add $300 \times 0.000016 = 0.0048$. | correct | script A: slip value equals the named mistake |
| review-3 | items[3].widget.wrong[no-half] | slip 1.1096: You used $25 \times 24 = 600$. $\binom{25}{2}$ divides by 2: it is 300. | correct | script A: slip value equals the named mistake |
| review-3 | items[3].widget.wrong[n-squared] | slip 1.11: You used $25^2 = 625$ for the count. $\binom{25}{2} = 300$. | correct | script A: slip value equals the named mistake |
| review-3 | items[4].widget.answer | key 17852.97 | correct | script A: recomputed |
| review-3 | items[4].widget.wrong[none] | slip 24000: That is $20 \times \text{£}1{,}200.00$ with no discounting. | correct | script A: slip value equals the named mistake |
| review-3 | items[4].widget.wrong[forever] | slip 40000: That is $\tfrac{C}{r}$, for payments that never stop. This pension stops after 20 years. | correct | script A: slip value equals the named mistake |
| review-3 | items[4].widget.wrong[last] | slip 13288.22: You discounted all £24,000.00 by 20 years. Only the last payment waits that long. | correct | script A: slip value equals the named mistake |
| review-3 | items[5].widget.answer | key 0.3125 | correct | script A: recomputed |
| review-3 | items[5].widget.wrong[half] | slip 0.5: You took 3 heads out of 6 flips. Count the sequences with 3 heads instead. | correct | script A: slip value equals the named mistake |
| review-3 | items[5].widget.wrong[cube] | slip 0.125: You worked out $0.5^3$ for the heads alone. The tails and the order count too. | correct | script A: slip value equals the named mistake |
| review-3 | items[5].widget.wrong[one-seq] | slip 0.015625: That is one sequence, such as HHHTTT. There are $\binom{6}{3} = 20$ of them. | correct | script A: slip value equals the named mistake |
| review-3 | items[6].widget.options[zero] | wrong option: $0$ / You treated $(x + y)^2$ as $x^2 + y^2$. The two mixed terms are missing. | correct | wrong under every reading; why line checked |
| review-3 | items[6].widget.options[one] | wrong option: $xy$ / There are two $xy$ terms: $x$ from the first bracket with $y$ from the second, and the re | correct | wrong under every reading; why line checked |
| review-3 | items[6].widget.options[right] | key: $2xy$ | correct | derivation on reading; figures in script A or C |
| review-3 | items[6].widget.options[product] | wrong option: $x^2y^2$ / You multiplied the squares. The mixed terms are $xy$, picked once each way. | correct | wrong under every reading; why line checked |
| review-3 | items[7].widget.options[right] | key: $1.001^{50}$ | correct | derivation on reading; figures in script A or C |
| review-3 | items[7].widget.options[long] | wrong option: $1.01^{200}$ / $x$ is small, but $nx = 2$. The estimate 3 is far from the true 7.32. | correct | wrong under every reading; why line checked |
| review-3 | items[7].widget.options[big-x] | wrong option: $1.5^2$ / $x = 0.5$ is not small. The estimate 2 misses the true 2.25 by 11%. | correct | wrong under every reading; why line checked |
| review-3 | items[7].widget.options[negative] | wrong option: $0.9^{30}$ / $nx = -3$, so the estimate is $-2$, which is not even positive. The true value is 0 | correct | wrong under every reading; why line checked |
| review-3 | items[8].widget.answer | key 500 | correct | script A: recomputed |
| review-3 | items[8].widget.wrong[one-pct] | slip 1: That is 1% of £100.00. Value the whole stream at each rate first. | correct | script A: slip value equals the named mistake |
| review-3 | items[8].widget.wrong[pct] | slip 5: You divided by 4 and by 5, not 0.04 and 0.05: $25 - 20 = 5$. | correct | script A: slip value equals the named mistake |
| review-3 | items[8].widget.wrong[payment] | slip 100: That is one payment. The rate change reprices the whole stream. | correct | script A: slip value equals the named mistake |
| homework-3 | items[5].explain | putting x = 1 turns every term into its coefficient | correct | derivation |
| homework-3 | items[6].widget | Pascal rule from factorials | correct | derivation |
| homework-3 | items[8].explain | term ratio (10-k)/(k+1) x 0.5; terms rise to k = 3 | correct | script A, C |
| homework-3 | items[9].model | three-term estimate trusted while nx well below 1; error about (nx)^3/6 of principal | correct | script C |
| homework-3 | items[0].widget.answer | key 16x^4-32x^3+24x^2-8x+1 and accept list | correct | derivation: tested at n or x = 1, 2, 3 |
| homework-3 | items[0].widget.wrong[no-sign] | slip 16x^4+32x^3+24x^2+8x+1: You dropped the signs. Odd powers of $-1$ are negative. | correct | derivation: not equal to the key; feedback value checked |
| homework-3 | items[0].widget.wrong[no-power] | slip 2x^4-8x^3+12x^2-8x+1: You did not raise the 2 to the power. $(2x)^4 = 16x^4$ and $(2x)^3 = 8x^3$. | correct | derivation: not equal to the key; feedback value checked |
| homework-3 | items[0].widget.wrong[ends] | slip 16x^4+1: You raised each part to the fourth power. The three mixed terms are missing. | correct | derivation: not equal to the key; feedback value checked |
| homework-3 | items[1].widget.answer | key 1792 | correct | script A: recomputed |
| homework-3 | items[1].widget.wrong[count] | slip 56: 56 is the count alone. Each path also carries $2^5 = 32$. | correct | script A: slip value equals the named mistake |
| homework-3 | items[1].widget.wrong[wrong-power] | slip 448: You used $2^3$. The power of 2 matches the power of $x$: $(2x)^5$. | correct | script A: slip value equals the named mistake |
| homework-3 | items[1].widget.wrong[once] | slip 112: You used 2 once. The 2 is raised to the fifth power with the $x$. | correct | script A: slip value equals the named mistake |
| homework-3 | items[2].widget.answer | key 240 | correct | script A: recomputed |
| homework-3 | items[2].widget.wrong[sign] | slip -240: $(-2)^4 = +16$: an even power of a negative is positive. | correct | script A: slip value equals the named mistake |
| homework-3 | items[2].widget.wrong[square] | slip 60: You used $(-2)^2$. The no-$x$ term takes $-\tfrac{2}{x}$ from 4 brackets. | correct | script A: slip value equals the named mistake |
| homework-3 | items[2].widget.wrong[wrong-k] | slip -160: You used $k = 3$, which leaves $x^3$. Solve $12 - 3k = 0$ for $k$. | correct | script A: slip value equals the named mistake |
| homework-3 | items[3].widget.answer | key 0.3456 | correct | script A: recomputed |
| homework-3 | items[3].widget.wrong[one-seq] | slip 0.03456: That is one sequence, such as win, win, win, loss, loss. There are $\binom{5}{3} = 10$ of them. | correct | script A: slip value equals the named mistake |
| homework-3 | items[3].widget.wrong[fair] | slip 0.3125: That is the answer for a 50% strategy. With 60% wins, each sequence has chance $0.6^3 \times 0.4^ | correct | script A: slip value equals the named mistake |
| homework-3 | items[3].widget.wrong[wins-only] | slip 0.216: You worked out $0.6^3$ for the wins alone. The two losses and the count matter too. | correct | script A: slip value equals the named mistake |
| homework-3 | items[3].widget.wrong[no-count] | slip 0.6: You took 3 out of 5 trades. Use the chances of win and loss instead. | correct | script A: slip value equals the named mistake |
| homework-3 | items[4].widget.answer | key 81.6968 | correct | script A: recomputed |
| homework-3 | items[4].widget.wrong[two] | slip 81.68: That is the two-term estimate. The third term adds $210 \times 0.000001 \times 80 \approx \text{£} | correct | script A: slip value equals the named mistake |
| homework-3 | items[4].widget.wrong[no-half] | slip 81.7136: You used $21 \times 20 = 420$. $\binom{21}{2} = 210$. | correct | script A: slip value equals the named mistake |
| homework-3 | items[4].widget.wrong[gain] | slip 1.6968: That is the gain. Add it to the £80.00. | correct | script A: slip value equals the named mistake |
| homework-3 | items[5].widget.answer | key 32 | correct | script A: recomputed |
| homework-3 | items[5].widget.wrong[leading] | slip 243: 243 is the first coefficient, $3^5$. The others are negative or positive in turn. | correct | script A: slip value equals the named mistake |
| homework-3 | items[5].widget.wrong[rows] | slip 1024: That is $4^5$, as if every term were positive. The signs alternate. | correct | script A: slip value equals the named mistake |
| homework-3 | items[5].widget.wrong[neg] | slip -32: $(3 - 1)^5 = 2^5$ is positive. | correct | script A: slip value equals the named mistake |
| homework-3 | items[7].widget.answer | key 2373.96 | correct | script A: recomputed |
| homework-3 | items[7].widget.wrong[no-rate] | slip 2000: That repays the £10,000.00 with no interest. | correct | script A: slip value equals the named mistake |
| homework-3 | items[7].widget.wrong[simple] | slip 2600: You added a year's interest, £600.00, to £2,000.00. Interest falls as the loan is paid down. | correct | script A: slip value equals the named mistake |
| homework-3 | items[7].widget.wrong[once] | slip 2120: You added 6% to £2,000.00. Set the present value of the payments equal to the loan instead. | correct | script A: slip value equals the named mistake |
| homework-3 | items[8].widget.answer | key 15 | correct | script A: recomputed |
| homework-3 | items[8].widget.wrong[middle] | slip 7.875: That is the $k = 5$ term, where the count peaks. The powers of 0.5 pull the peak earlier. | correct | script A: slip value equals the named mistake |
| homework-3 | items[8].widget.wrong[before] | slip 11.25: That is the $k = 2$ term. The next term is bigger: the ratio is $\tfrac{8}{3} \times 0.5 > 1$. | correct | script A: slip value equals the named mistake |
| homework-3 | items[8].widget.wrong[after] | slip 13.125: That is the $k = 4$ term. It is smaller than the one before: the ratio is $\tfrac{7}{4} \times 0. | correct | script A: slip value equals the named mistake |
| homework-3 | items[8].widget.wrong[coef] | slip 252: 252 is the largest count, $\binom{10}{5}$. Each term also carries $(0.5)^k$. | correct | script A: slip value equals the named mistake |
| homework-3 | items[9].model | longform model answer and rubric | correct | script C recomputes every figure |
| problems-3 | items[3].parts[0].explain | digits of 11^4 are row 4 because no entry is 10 or more | correct | derivation |
| problems-3 | items[2].prose | gym: £100 at the end of each month; savings earn 0.5% a month | correct | convention stated |
| problems-3 | items[0].parts[0].widget.answer | key 3060 | correct | script A: recomputed |
| problems-3 | items[0].parts[0].widget.wrong[ordered] | slip 73440: 73440 counts each pizza once for every order its toppings were picked in. Divide by $4! = 24$: 306 | correct | script A: slip value equals the named mistake |
| problems-3 | items[0].parts[0].widget.wrong[times] | slip 72: $18 \times 4$ does not count picks. Use $\binom{18}{4} = \tfrac{18 \times 17 \times 16 \times 15}{4!} | correct | script A: slip value equals the named mistake |
| problems-3 | items[0].parts[0].widget.wrong[three-orders] | slip 12240: You divided by $3! = 6$. Four toppings can be picked in $4! = 24$ orders: $73440 \div 24 = 3060$. | correct | script A: slip value equals the named mistake |
| problems-3 | items[0].parts[1].widget.answer | key 6120 | correct | script A: recomputed |
| problems-3 | items[0].parts[1].widget.wrong[one-size] | slip 3060: 3060 is one size only. Choosing 14 toppings to put on is choosing 4 to leave off, so there are 3060 | correct | script A: slip value equals the named mistake |
| problems-3 | items[0].parts[2].widget.answer | key 3876 | correct | script A: recomputed |
| problems-3 | items[0].parts[2].widget.wrong[one-more] | slip 3078: That adds 18, one pizza for each old topping with ham. Ham needs 3 more toppings, in $\binom{18}{3} | correct | script A: slip value equals the named mistake |
| problems-3 | items[0].parts[2].widget.wrong[doubled] | slip 6120: That counts the old pizzas twice. With ham, the other 3 toppings come from 18 in 816 ways: $3060 +  | correct | script A: slip value equals the named mistake |
| problems-3 | items[0].parts[2].widget.wrong[ordered] | slip 93024: 93024 is $19 \times 18 \times 17 \times 16$, the ordered picks. Divide by $4! = 24$: 3876. | correct | script A: slip value equals the named mistake |
| problems-3 | items[0].parts[3].widget.answer | key 524288 | correct | script A: recomputed |
| problems-3 | items[0].parts[3].widget.wrong[no-plain] | slip 524287: That leaves out the plain pizza, the 1 at the start of the row. With it the total is 524288. | correct | script A: slip value equals the named mistake |
| problems-3 | items[0].parts[3].widget.wrong[row-eighteen] | slip 262144: 262144 is row 18, for the old 18 toppings. Each row adds to twice the row above: 524288. | correct | script A: slip value equals the named mistake |
| problems-3 | items[1].parts[0].widget.answer | key 189 | correct | script A: recomputed |
| problems-3 | items[1].parts[0].widget.wrong[not-squared] | slip 63: You squared $x$ but not the 3. The second part is $-3x$, so square all of it: $(-3x)^2 = 9x^2$. | correct | script A: slip value equals the named mistake |
| problems-3 | items[1].parts[0].widget.wrong[sign] | slip -189: A minus squared is a plus: $(-3)^2 = 9$. So the number is $21 \times 9 = 189$. | correct | script A: slip value equals the named mistake |
| problems-3 | items[1].parts[0].widget.wrong[no-count] | slip 9: That leaves out the count $\binom{7}{2} = 21$. There are 21 ways to pick $-3x$ from 2 of the 7 bracket | correct | script A: slip value equals the named mistake |
| problems-3 | items[1].parts[1].widget.answer | key 1-21x+189x^2 and accept list | correct | derivation: tested at n or x = 1, 2, 3 |
| problems-3 | items[1].parts[1].widget.wrong[sign] | slip 1+21x+189x^2: The $x$ term carries the minus: $7 \times (-3x) = -21x$. | correct | derivation: not equal to the key; feedback value checked |
| problems-3 | items[1].parts[1].widget.wrong[square-sign] | slip 1-21x-189x^2: $(-3x)^2$ is positive, so the $x^2$ term is $+189x^2$. | correct | derivation: not equal to the key; feedback value checked |
| problems-3 | items[1].parts[1].widget.wrong[no-count] | slip 1-3x+9x^2: That leaves out the counts 7 and 21. The terms are $7(-3x) = -21x$ and $21(9x^2) = 189x^2$. | correct | derivation: not equal to the key; feedback value checked |
| problems-3 | items[1].parts[2].widget.answer | key 0.8089 | correct | script A: recomputed |
| problems-3 | items[1].parts[2].widget.wrong[linear] | slip 0.79: 0.79 keeps only $1 - 21x$. The third term adds $189 \times 0.0001 = 0.0189$: 0.8089. | correct | script A: slip value equals the named mistake |
| problems-3 | items[1].parts[2].widget.wrong[square-sign] | slip 0.7711: The $x^2$ term is $+189x^2$, so add 0.0189: $1 - 0.21 + 0.0189 = 0.8089$. | correct | script A: slip value equals the named mistake |
| problems-3 | items[1].parts[2].widget.wrong[x-three] | slip 0.5401: You put in $x = 0.03$. The bracket is $1 - 3x$, so $0.97$ needs $x = 0.01$. | correct | script A: slip value equals the named mistake |
| problems-3 | items[1].parts[2].widget.wrong[calculator] | slip 0.808: That is $0.97^7$ itself, from a calculator. The question asks for the three-term estimate, 0.8089. | correct | script A: slip value equals the named mistake |
| problems-3 | items[1].parts[3].widget.answer | key -945 | correct | script A: recomputed |
| problems-3 | items[1].parts[3].widget.wrong[sign] | slip 945: A minus cubed stays a minus: $(-3)^3 = -27$. So the number is $-945$. | correct | script A: slip value equals the named mistake |
| problems-3 | items[1].parts[3].widget.wrong[not-cubed] | slip -105: You cubed $x$ but not the 3. $(-3x)^3 = -27x^3$, so the number is $35 \times (-27) = -945$. | correct | script A: slip value equals the named mistake |
| problems-3 | items[1].parts[3].widget.wrong[no-count] | slip -27: That leaves out the count $\binom{7}{3} = 35$. The number is $35 \times (-27) = -945$. | correct | script A: slip value equals the named mistake |
| problems-3 | items[1].parts[4].widget.answer | key 0.807955 | correct | script A: recomputed |
| problems-3 | items[1].parts[4].widget.wrong[calculator] | slip 0.807983: That is $0.97^7$ itself, from a calculator. The question asks for the estimate with the $x^3$ t | correct | script A: slip value equals the named mistake |
| problems-3 | items[1].parts[4].widget.wrong[added] | slip 0.809845: The dropped term is negative, $-0.000945$. Take it off: $0.8089 - 0.000945 = 0.807955$. | correct | script A: slip value equals the named mistake |
| problems-3 | items[1].parts[4].widget.wrong[square] | slip 0.7144: You used $x^2 = 0.0001$. The term is $-945x^3$, and $x^3 = 0.000001$. | correct | script A: slip value equals the named mistake |
| problems-3 | items[2].parts[0].widget.answer | key 1.06165 | correct | script A: recomputed |
| problems-3 | items[2].parts[0].widget.wrong[linear] | slip 1.06: 1.06 keeps only $1 + nx$. The third term adds $66 \times 0.000025 = 0.00165$. | correct | script A: slip value equals the named mistake |
| problems-3 | items[2].parts[0].widget.wrong[calculator] | slip 1.06168: That is $1.005^{12}$ from a calculator. The question asks for the three-term estimate, 1.06165. | correct | script A: slip value equals the named mistake |
| problems-3 | items[2].parts[0].widget.wrong[no-half] | slip 1.0633: You used $12 \times 11 = 132$. The count is $\binom{12}{2} = \tfrac{12 \times 11}{2} = 66$. | correct | script A: slip value equals the named mistake |
| problems-3 | items[2].parts[1].widget.answer | key 0.9419 | correct | script A: recomputed |
| problems-3 | items[2].parts[1].widget.wrong[grown] | slip 1.0617: 1.0617 is what £1 today grows to. Going back in time divides: $\tfrac{1}{1.0617} \approx 0.9419$. | correct | script A: slip value equals the named mistake |
| problems-3 | items[2].parts[1].widget.wrong[subtract] | slip 0.9383: You took 0.0617 off 1. Divide instead: $\tfrac{1}{1.0617} \approx 0.9419$. | correct | script A: slip value equals the named mistake |
| problems-3 | items[2].parts[1].widget.wrong[one-month] | slip 0.995: That is £1 paid in 1 month, $\tfrac{1}{1.005}$. Twelve months divide by $1.005^{12}$. | correct | script A: slip value equals the named mistake |
| problems-3 | items[2].parts[2].widget.answer | key 1161.89 | correct | script A: recomputed |
| problems-3 | items[2].parts[2].widget.wrong[undiscounted] | slip 1200: £1,200 adds the payments at face value. Later pounds are worth less today: $20000(1 - 0.9419) = 116 | correct | script A: slip value equals the named mistake |
| problems-3 | items[2].parts[2].widget.wrong[no-one-minus] | slip 18838: That is $20000 \times 0.9419$. The bracket is $1 - 0.9419 = 0.0581$: $20000 \times 0.0581 = 1162$. | correct | script A: slip value equals the named mistake |
| problems-3 | items[2].parts[2].widget.wrong[one-payment] | slip 94.19: That is the last payment alone, $100 \times 0.9419$. Add all 12 present values with the formula: 1 | correct | script A: slip value equals the named mistake |
| problems-3 | items[2].parts[3].widget.answer | key 11.89 | correct | script A: recomputed |
| problems-3 | items[2].parts[3].widget.wrong[undiscounted] | slip 50: £50 compares £1,200 at face value with £1,150. In today's money the monthly plan costs £1,162, so the | correct | script A: slip value equals the named mistake |
| problems-3 | items[2].parts[3].widget.wrong[sign] | slip -11.89: Paying today costs less, so the saving is positive: $1162 - 1150 = 12$. | correct | script A: slip value equals the named mistake |
| problems-3 | items[3].parts[0].widget.answer | key 14641 | correct | script A: recomputed |
| problems-3 | items[3].parts[0].widget.wrong[share] | slip 10001: That is $10^4 + 1^4$, a power shared out over a sum. The middle terms $4000 + 600 + 40$ are missin | correct | script A: slip value equals the named mistake |
| problems-3 | items[3].parts[0].widget.wrong[no-count] | slip 11111: That leaves out the numbers in front, 4, 6 and 4. With them: $10000 + 4000 + 600 + 40 + 1$. | correct | script A: slip value equals the named mistake |
| problems-3 | items[3].parts[1].widget.answer | key 161051 | correct | script A: recomputed |
| problems-3 | items[3].parts[1].widget.wrong[digits] | slip 15101051: You wrote the row as digits. The 10s carry: $10 \times 10^3 = 10000$ and $10 \times 10^2 = 1000 | correct | script A: slip value equals the named mistake |
| problems-3 | items[3].parts[1].widget.wrong[times-ten] | slip 146410: That is $14641 \times 10$. $11^5$ is $14641 \times 11 = 161051$. | correct | script A: slip value equals the named mistake |
| problems-3 | items[3].parts[1].widget.wrong[share] | slip 100001: That is $10^5 + 1$, a power shared out over a sum. Row 5 puts 5, 10, 10 and 5 in the middle. | correct | script A: slip value equals the named mistake |
| problems-3 | items[3].parts[2].widget.answer | key 1.61051 | correct | script A: recomputed |
| problems-3 | items[3].parts[2].widget.wrong[shift] | slip 16.1051: That divides by $10^4$. Five factors of $\tfrac{1}{10}$ divide by $10^5$: 1.61051. | correct | script A: slip value equals the named mistake |
| problems-3 | items[3].parts[2].widget.wrong[too-far] | slip 0.161051: That divides by $10^6$. Five factors of $\tfrac{1}{10}$ divide by $10^5$: 1.61051. | correct | script A: slip value equals the named mistake |
| problems-3 | items[3].parts[2].widget.wrong[linear] | slip 1.5: 1.5 is the estimate $1 + nx$. The exact value is $\tfrac{161051}{100000} = 1.61051$. | correct | script A: slip value equals the named mistake |
| problems-3 | items[3].parts[3].widget.answer | key 0.11051 | correct | script A: recomputed |
| problems-3 | items[3].parts[3].widget.wrong[three-term] | slip 0.01051: That is the shortfall of the three-term estimate, 1.6. The linear estimate is 1.5: $1.61051 - 1. | correct | script A: slip value equals the named mistake |
| problems-3 | items[3].parts[3].widget.wrong[dropped] | slip 0.1: 0.1 is the first dropped term, $\binom{5}{2}(0.1)^2$. It is most of the shortfall, but the exact gap | correct | script A: slip value equals the named mistake |
| problems-3 | items[3].parts[3].widget.wrong[sign] | slip -0.11051: The estimate is below the true value, so the shortfall is positive: 0.11051. | correct | script A: slip value equals the named mistake |
| fluency-l11-powers-of-a-bracket | families[x-plus-b].widget.answer | key {key} over the whole range | correct | script B: brute-force sweep of every admissible case |
| fluency-l11-powers-of-a-bracket | families[x-plus-b].wrong[count-only] | That is only the count of paths. Each path also multiplies {ne} copies of {b}. | correct | script B: value equals the named mistake, never the key |
| fluency-l11-powers-of-a-bracket | families[x-plus-b].wrong[power-swapped] | You raised {b} to the power {e}. The ${v}^{{{e}}}$ term takes {b} from the other {ne} brackets. | correct | script B: value equals the named mistake, never the key |
| fluency-l11-powers-of-a-bracket | families[ax-plus-b].widget.answer | key {key} over the whole range | correct | script B: brute-force sweep of every admissible case |
| fluency-l11-powers-of-a-bracket | families[ax-plus-b].wrong[a-not-raised] | You used {a} once. Each of the {e} brackets that gives ${a}{v}$ gives a {a}, so you need ${a}^{{{e}}}$. | correct | script B: value equals the named mistake, never the key |
| fluency-l11-powers-of-a-bracket | families[ax-plus-b].wrong[a-left-out] | You left out the {a} in ${a}{v}$. The power of ${a}{v}$ is ${a}^{{{e}}}{v}^{{{e}}}$. | correct | script B: value equals the named mistake, never the key |
| fluency-l11-powers-of-a-bracket | families[term-with-no-x].widget.answer | key {key} over the whole range | correct | script B: brute-force sweep of every admissible case |
| fluency-l11-powers-of-a-bracket | families[term-with-no-x].wrong[count-only] | That is only the count of paths. Each path also multiplies the numbers in the two parts. | correct | script B: value equals the named mistake, never the key |
| fluency-l11-powers-of-a-bracket | families[term-with-no-x].wrong[powers-only] | You left out the count. $\binom{{{n}}}{{{h}}}$ paths each give this term. | correct | script B: value equals the named mistake, never the key |
