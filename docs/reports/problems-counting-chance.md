# Problem sets: counting-chance (docs/briefs/chained.md)

Files: `app/content/courses/counting-chance/problems-1.json`, `problems-2.json`. Number script: `docs/reports/problems-counting-chance-numbers.py` (run with the scratchpad venv Python; exits 0).

## Sets

| Set | Item | Parts | Lessons drawn on | Difficulty | Chain |
|---|---|---|---|---|---|
| problems-1 | p-d4-against-d6 | 4 | l1, l2, l3, l4 | 3 | $\|S\| = 24$ → $P(s > f) = 7/12$ → $P(f > s) = 1/4$ (disjoint events, complement) → fair price £3 |
| problems-1 | p-octahedral-prize | 5 | l1, l2, l3 | 4 | $\|B\| = 6$ → $\|A \cap B\| = 3$ → $\|A \cup B\| = 19$ → $P = 19/64$ → fair price £4.75 |
| problems-1 | p-two-feeds | 4 | l3, l4 | 4 | $P(\text{both fail}) = 0.004$ → $P(\text{at least one works}) = 0.996$ → $0.996^{20}$ → $1 - 0.996^{20} = 0.0770$ |
| problems-1 | p-tetra-eight | 5 | l1, l2, l4 | 5 | 16 outcomes → $1/16$ → $(15/16)^{10}$ → win 0.4755 → smallest $n = 11$ |
| problems-2 | p-relay-team | 4 | l5, l6 | 3 | $\binom{9}{4} = 126$ teams → $126 \times 4! = 3024$ line-ups → $P(\text{both fastest in}) = 1/6$ → $P(\text{they run legs 3 and 4}) = 1/36$ |
| problems-2 | p-breach-check | 5 | l5, l6, l7 (and l4) | 4 | $11/15$ → $11/21$ → $33/91$ → at least one breach $58/91$ → 290 of $\binom{15}{3} = 455$ samples |
| problems-2 | p-vote-tallies | 4 | l8, l5 (and l2) | 4 | 45 tallies → 24 with an empty proposal → tallies not equally likely (choice) → $P(\text{unanimous}) = 3/3^8 = 1/2187$ |
| problems-2 | p-feed-audit | 4 | l6, l5, l7 (and l4) | 5 | $\binom{30}{5} = 142{,}506$ → exactly 3 of yours $3000/142{,}506$ → at least 3 $3126/142{,}506$ → in at least one of 4 quarters 0.0849 |

Level 1: 4 items, 18 parts, every part `numeric` (typed); every lesson of the level appears in at least two problems.
Level 2: 4 items, 17 parts, 16 typed and 1 `choice` (the judgement whether the tallies are equally likely); every lesson of the level appears in at least one problem, l5 to l7 in at least two.

## Checks

| Check | problems-1 | problems-2 |
|---|---|---|
| 1. Numbers script | exit 0, 171 of 171 checks; each answer by an exact method and by enumeration, a closed form or a seeded simulation; every wrong value recomputed from its slip and outside the tolerance | the same script, exit 0 (323 checks for sets 1 and 2); enumeration of every line-up, pick list and vote list, a seeded simulation for the audit |
| 2. Validator | 0 errors; 0 warnings on the file | 0 errors; 0 warnings (five long-sentence advisories fixed) |
| 3. Playthrough (`--local-cdn`) | green, and green with `--mobile`; shots at 1280 and 440 looked at, no layout faults | green, and green with `--mobile` |
| 4. Voice scan 35 | 0 and 0 on the course folder | 0 and 0 |
| 5. Fresh-check | 0 hits at the gate; at `--min-run 8 --min-share 0`, 4 hits, all stock phrasing ("how many outcomes are in the sample space", "what is its fair price, the average payout per roll", "give a decimal to 4 places"): kept | 0 hits at the gate and 0 at `--min-run 8 --min-share 0` |

`lv.check_wrongs` prints "check by hand" on 19 `byKey` lines in set 1 and 29 in set 2 that quote the inputs of a slip rather than its value; each was read and each names the slip its value comes from.

## Judgements

- p-tetra-eight has the shape of the Chevalier de Méré bets (l4 transfer and homework-1): "at least one in $n$ tries" is the level's subject. The dice, the target, the numbers and the last step (smallest $n$ by stepping on from $n = 10$) are new.
- p-vote-tallies takes the l1 and l2 lesson (merged outcomes are not equally likely) into stars and bars: l8 counts tallies, and part 3 asks whether those counts can be turned into chances. It uses only $3^8$ (l5) for the vote lists, not a multinomial coefficient, which the course does not teach.
- p-feed-audit is the hypergeometric count without the name; the counts are built in stages (l5) from combinations (l6) of a draw without replacement (l7).
- In set 1, independence is used as l4 teaches it (chances of independent days multiply); no idea from level 2 or later. Each set uses only ideas taught up to the end of its level.
