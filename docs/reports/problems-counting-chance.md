# Problem sets: counting-chance (docs/briefs/chained.md)

Files: `app/content/courses/counting-chance/problems-1.json`, `problems-2.json`, `problems-3.json`. Number script: `docs/reports/problems-counting-chance-numbers.py` (run with the scratchpad venv Python; exits 0, 497 of 497 checks).

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
| problems-3 | p-shard-clash | 4 | l10, l11 | 4 | no clash for 5 symbols 0.8136 → clash 0.1864 → smallest $n = 9$ by stepping the product on → union bound at $n = 9$: $36/50 = 0.72$ |
| problems-3 | p-three-downgrades | 4 | l9, l11 | 5 | $P(A \cup B) = 0.15$ → $P(A \cup B \cup C) = 0.175 + t$ (`expression`) → monotonicity caps $t \le 0.015$ → largest $P(\text{at least one}) = 0.19$ |
| problems-3 | p-ace-and-king | 4 | l12, l9 (and l11) | 4 | $\binom{44}{5} = 1{,}086{,}008$ → $P(A \cup K) = 0.5821$ (De Morgan, complement) → $P(A \cap K) = 0.1002$ → 260,360 hands |
| problems-3 | p-short-deck | 5 | l10, l12, l11 | 5 | $16/19$ → $32/57$ → $256/969$ (birthday-style dealing) → 1,280 hands of four ranks → 2,880 one-pair hands (disjoint classes add to 4,845) |

- Level 1: 4 items, 18 parts, all `numeric`. Every lesson appears in at least two problems.
- Level 2: 4 items, 17 parts, 16 typed and 1 `choice` (the judgement whether tallies are equally likely). Every lesson appears; l5 to l7 in at least two.
- Level 3: 4 items, 17 parts, 16 `numeric` and 1 `expression`. Every lesson appears in at least two problems (l11 in three).
- Each set has difficulty 3 to 5 with at least one 5, items of 4 or 5 parts, and every later part restates the value it uses ("Using $\tfrac{11}{21}$ for the first two, ..."). Each part's `wrong` list includes the value that follows from the commonest slip of the part before where one exists (for example `from-added`, `from-squared`, `from-your-shard`, `from-exactly`). The script checks the typed share and the difficulty rule.

## Checks

| Check | problems-1 | problems-2 | problems-3 |
|---|---|---|---|
| 1. Numbers script | pass | pass | pass |
| 2. Validator | 0 errors, 0 warnings on the file | 0 errors, 0 warnings (five long-sentence advisories fixed) | 0 errors, 0 warnings (one advisory fixed) |
| 3. Playthrough `--local-cdn` | green; green `--mobile` | green; green `--mobile` | green; green `--mobile` |
| 4. Voice scan 35 (course folder) | 0 and 0 | 0 and 0 | 0 and 0 |
| 5. Fresh-check | 0 at the gate; 4 loose hits | 0 at the gate; 0 loose hits | 0 at the gate; 10 loose hits |

Numbers script: each answer by an exact method (fractions or sympy) and a second method: enumeration of the sample space (dice pairs, line-ups, pick lists, all $3^8$ vote lists, all 4,845 short-deck hands with their classes), a sum over ace and king counts, a grid search over feasible Venn regions for $t$, a binomial sum, or a seeded simulation. Every wrong value is recomputed from the slip its `byKey` line names, and `lv.check_wrongs` confirms each lies outside the answer's tolerance. Its "check by hand" lines (19, 29 and 26 per set) are `byKey` texts that quote the inputs of a slip, not its value; each was read. The independence slip in p-ace-and-king part 4 has a band of ±5 around 302,492, so it catches both 302,490 (exact square) and the value from the rounded square.

Fresh-check, loose triage (`--min-run 8 --min-share 0`), judged: all hits are stock phrasing, kept. Set 1: "how many outcomes are in the sample space", "what is its fair price, the average payout per roll", "give a decimal to 4 places". Set 3: "what upper limit does the union bound give for the chance" (l11 quiz), "what is the chance of at least one clash" (l10), "cards are dealt from a standard 52-card deck" (six items in conditional and counting).

Screenshots: 1280 and 440 shots of each set (course row, a wrong part, the done page) looked at; no overlap, overflow or clipped maths.

## Judgements

- p-tetra-eight has the shape of the Chevalier de Méré bets (l4 transfer, homework-1): "at least one in $n$ tries" is the level's subject. The dice, target, numbers and last step (smallest $n$ by stepping on from $n = 10$) are new.
- p-vote-tallies carries the l1 and l2 lesson (merged outcomes are not equally likely) into stars and bars. It uses only $3^8$ (l5) for the vote lists, not a multinomial coefficient, which the course does not teach.
- p-feed-audit is the hypergeometric count without the name, built in stages (l5) from combinations (l6) of a draw without replacement (l7).
- p-ace-and-king: the prerequisite course `counting` (homework-2) counts five-card hands with at least one ace (886,656). Part 3 states $P(A)$ rather than asking for it again; the chain's new step is the intersection by inclusion and exclusion.
- p-three-downgrades: with $t = 0.015$ every Venn region is 0 or more (the region $B \cap C$ outside $A$ is exactly 0), so the bound is attained; the script checks all seven regions.
- Each set uses only ideas taught up to the end of its level; independence is used as l4 teaches it (independent chances multiply).

## Engine limits

Three bullets to `docs/BACKLOG-INBOX.md` under "Raised later (problems counting-chance):".
