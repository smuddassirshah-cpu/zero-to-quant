# Problem sets: counting-chance (docs/briefs/chained.md)

Files: `app/content/courses/counting-chance/problems-1.json`. Number script: `docs/reports/problems-counting-chance-numbers.py` (run with the scratchpad venv Python; exits 0).

## Sets

| Set | Item | Parts | Lessons drawn on | Difficulty | Chain |
|---|---|---|---|---|---|
| problems-1 | p-d4-against-d6 | 4 | l1, l2, l3, l4 | 3 | $\|S\| = 24$ → $P(s > f) = 7/12$ → $P(f > s) = 1/4$ (disjoint events, complement) → fair price £3 |
| problems-1 | p-octahedral-prize | 5 | l1, l2, l3 | 4 | $\|B\| = 6$ → $\|A \cap B\| = 3$ → $\|A \cup B\| = 19$ → $P = 19/64$ → fair price £4.75 |
| problems-1 | p-two-feeds | 4 | l3, l4 | 4 | $P(\text{both fail}) = 0.004$ → $P(\text{at least one works}) = 0.996$ → $0.996^{20}$ → $1 - 0.996^{20} = 0.0770$ |
| problems-1 | p-tetra-eight | 5 | l1, l2, l4 | 5 | 16 outcomes → $1/16$ → $(15/16)^{10}$ → win 0.4755 → smallest $n = 11$ |

Level 1: 4 items, 18 parts, every part `numeric` (typed); every lesson of the level appears in at least two problems.

## Checks

| Check | problems-1 |
|---|---|
| 1. Numbers script | exit 0, 171 of 171 checks; each answer by an exact method and by enumeration, a closed form or a seeded simulation; every wrong value recomputed from its slip and outside the tolerance |
| 2. Validator | 0 errors; 0 warnings on the file |
| 3. Playthrough (`--local-cdn`) | green, and green with `--mobile`; shots at 1280 and 440 looked at, no layout faults |
| 4. Voice scan 35 | 0 and 0 on the course folder |
| 5. Fresh-check | 0 hits at the gate; at `--min-run 8 --min-share 0`, 4 hits, all stock phrasing ("how many outcomes are in the sample space", "what is its fair price, the average payout per roll", "give a decimal to 4 places"): kept |

`lv.check_wrongs` prints "check by hand" on 19 `byKey` lines that quote the inputs of a slip rather than its value; each was read and each names the slip its value comes from.

## Judgements

- p-tetra-eight has the shape of the Chevalier de Méré bets (l4 transfer and homework-1): "at least one in $n$ tries" is the level's subject. The dice, the target, the numbers and the last step (smallest $n$ by stepping on from $n = 10$) are new.
- Independence is used as l4 teaches it (chances of independent days multiply); no idea from level 2 or later.
