# Problem sets 1.5 (a): second-reader findings

Scope: `app/content/courses/counting-chance/problems-1.json` to `problems-3.json` and `app/content/courses/conditional/problems-1.json` to `problems-3.json` at commit 000ba0c: 24 problems, 105 parts.

Method: both authors' scripts run first (`problems-counting-chance-numbers.py`: 497 of 497, exit 0; `problems-conditional-numbers.py`: 572 checks, 0 failures). Every part then solved from its text before reading the answer, with exact fractions by hand and an independent Python pass (enumeration of the d8 and d4 grids, all 4,845 short-deck hands, all $3^8$ vote lists, the shard product stepped to 10 symbols, the poker counts by inclusion and exclusion, the two-filter and three-hypothesis posteriors by the joint route). Every `wrong` value re-derived from the slip its line names. Each numeric part was also tested against the engine's rule (`grade.js within`: `|v - answer| <= abs + 1e-9`) with the answer rounded to 2 and 3 places, and with any value its own feedback prints after `\approx`. Lessons opened for notation and for what is taught by each level (fair price in l2, De Morgan in l3, independent products in l4, union bound and monotonicity in l11, odds as "1 to 5" in l10, shared effect in l16).

No answer, `accept` text or explanation states a wrong value of the quantity asked. The three `wrong` findings are all grading: a learner who does what the question says, or types what the feedback prints, is marked wrong.

Tags: `wrong` = a learner is marked wrongly or told something false; `unclear` = the question can be read two ways or does not say the form wanted; `minor` = weak part, loose `wrong` entry, label or freshness.

## Findings

1. `wrong` | `counting-chance/problems-3.json` | `p-ace-and-king` | part 4.
   The question says "Using $P(A \cap K) \approx 0.100179$, how many of the 2,598,960 hands ...", with `tol` 0. $0.100179 \times 2{,}598{,}960 = 260{,}361.2$, so the stated route gives 260,361 and is marked wrong; the exact count is $2{,}598{,}960 - 2 \times 1{,}712{,}304 + 1{,}086{,}008 = 260{,}360$. `feedback.correct` says "$0.100179 \times 2{,}598{,}960 \approx 260{,}360$", which is false at the digits shown. The `from-product` entry has the same fault: $0.341158^2 \times 2{,}598{,}960 = 302{,}489.8$, stored as 302,492 with `tol` 5 (it only just holds the value).
   Fix: ask from counts, not from the rounded chance. Question: "There are 886,656 hands with at least one ace, the same number with at least one king, and $2{,}598{,}960 - 1{,}086{,}008 = 1{,}512{,}952$ in $A \cup K$. How many hands hold at least one ace and at least one king?" `feedback.correct`: "$886{,}656 + 886{,}656 - 1{,}512{,}952 = 260{,}360$, which is $0.1002$ of all hands, as part 3 found." `generic`: "Not quite. Rearrange inclusion and exclusion on the counts." `from-product`: value 302490, `tol` 5. Add a `from-chance` entry, value 260361, `tol` 1: "You multiplied the rounded chance by the number of hands. Use the exact counts."

2. `wrong` | `conditional/problems-2.json` | `p-bad-ticks` | part 5.
   "Give a decimal." with answer 0.0286 and `tol` 0.0002. The exact value is $39.2 / 1369.2 = 0.02863$; a learner who types 0.029 is marked wrong, and `feedback.correct` itself prints "$\approx 0.029$". The band cannot be widened, because the `over-errors` slip is 0.0295.
   Fix: question ends "Give a decimal to 4 places."; `feedback.correct`: "$\tfrac{39.2}{1{,}330 + 39.2} \approx 0.0286$, matching $1 - 0.9714$ from part 3."

3. `wrong` | `conditional/problems-3.json` | `p-three-loans` | part 4.
   "How many times the model's chance is the true chance?" has answer 5.536, `tol` 0.005 and no rounding asked. A learner who types 5.5 is marked wrong, and `feedback.correct` prints "$\approx 5.5$" (the explanation says "more than five times over").
   Fix: `tol` `{ "abs": 0.05 }` on the answer (the nearest slip is 0.1806) and add "Give one decimal place." to the question. Also see finding 13 for the `difference` entry.

4. `unclear` | both courses | rounding is not stated on 35 parts.
   These parts say "Give a fraction or a decimal", "Give a decimal", or nothing, with `tol` 0.0005 on an answer that does not terminate within 4 places. A fraction is always right, and 3 places passes, but the natural 2-place decimal is marked wrong (0.58 for $\tfrac{7}{12}$, 0.17 for $\tfrac{1}{6}$, 0.39 for $\tfrac{180}{456}$, 0.76 for $\tfrac{54}{71}$). The counting-chance author already writes "Give a decimal to 4 places" where no fraction is natural; the rest should match.
   Parts: counting-chance `problems-1` `p-d4-against-d6` 2, `p-octahedral-prize` 4; `problems-2` `p-relay-team` 3, 4, `p-breach-check` 1 to 4; `problems-3` `p-short-deck` 1, 2. Conditional `problems-1` `p-eight-sided` 1 to 4, `p-watchlist` 1 to 5, `p-dealer-calls` 1 to 3; `problems-2` `p-takeover-rumour` 3, 4, `p-downgrade-news` 1 to 3, `p-broker-algo` 2 to 4, `p-bad-ticks` 2, 3; `problems-3` `p-gap-days` 3, 4, `p-losing-week` 2.
   Fix: end each question with "Give a fraction, or a decimal to 4 places." (or "Give a decimal to 4 places." where the working is in decimals: takeover 3 and 4, downgrade 3, broker 4, bad-ticks 2 and 3, gap-days 3 and 4, losing-week 2). In conditional `problems-1` parts 2 onward of each item carry no form sentence at all; add it there too.

5. `unclear` | `conditional/problems-2.json` | `p-bad-ticks` | part 1.
   Answer 0.0582 with `tol` 0.0001, tighter than every other part. 0.058 is marked wrong although the question only says "Give a decimal." The tight band is needed to keep the `false-on-all` slip (0.059) apart.
   Fix: "Give a decimal to 4 places."

6. `unclear` | `conditional/problems-1.json` | `p-order-router` | prose and part 5.
   "An order that misses is re-sent once, to Y" does not say what happens to an order that first missed at Y, nor that the second try is independent of the first; part 3's $0.72 + 0.28 \times 0.8$ needs both. Part 5's option "The spread router, by 0.036" uses a name the item never introduces, and "spread" has another meaning on a trading desk.
   Fix: prose "An order that misses is re-sent once, to Y, even if Y was its first venue. The re-sent order fills with chance 0.8 whatever happened before." Option text: "The first router, by 0.036". Explain: "Within two tries the first router fills 0.944 of orders and the Z-first router 0.98."

7. `unclear` | `conditional/problems-2.json` | `p-downgrade-news` | parts 1 and 2.
   l10 writes odds as "1 to 5", and the numeric parser reads neither "3 to 17" nor "3:17" (`grade.js parseNum` takes a number, `a/b`, a mixed number or a percentage). Part 1 says "Give a fraction or a decimal" without saying which way up; part 2 gives no form.
   Fix: part 1 "What are the prior odds of a downgrade, as the chance of a downgrade over the chance of none? Give one number: a fraction, or a decimal to 4 places." Part 2 ends "Give one number, as in part 1."

8. `minor` | `counting-chance/problems-1.json` | `p-octahedral-prize` | part 3.
   The `exactly-one` value 16 is also $|A|$, the commoner slip (forgetting $B$). That learner is told "You left out the overlap altogether", which is not what they did.
   Fix: id `only-a`, line "That is $|A| = 16$ alone, or the outcomes in exactly one of the two. Add the 3 outcomes of $B$ that are not in $A$."

9. `minor` | `counting-chance/problems-1.json` | `p-tetra-eight` | part 5.
   The `adding` slip is stored as 8, from $\tfrac{n}{16} \ge \tfrac{1}{2}$. "More often than not" is strict, so the same slip gives $n = 9$ ($\tfrac{9}{16} > \tfrac{1}{2}$), which gets only the generic line.
   Fix: add `{ "id": "adding-strict", "value": 9 }`: "That solves $\tfrac{n}{16} > \tfrac{1}{2}$, which adds the chances. At $n = 9$ the bet wins with chance 0.4406." ($1 - (15/16)^9 = 0.4406$.)

10. `minor` | `counting-chance/problems-3.json` | `p-short-deck` | part 5.
    The `two-pair-ordered` entry (2520, from 720 two-pair hands) cannot be reached: the question hands the learner 360. The part itself is one subtraction of given numbers, thin for the last step of a difficulty 5 and for the only use of l12's hand classes.
    Fix: drop `two-pair-ordered`. Better, make the learner count one class: "Of the rest, 320 are three of a kind and 5 four of a kind. Two pair needs 2 of the 5 ranks and 2 of the 4 suits in each. All others are one pair. Using the 1,280 hands with four ranks, how many hands are one pair?" Then 2520 is a real slip, and add `no-two-pair` 3240 ($4845 - 1280 - 320 - 5$).

11. `minor` | `conditional/problems-1.json` | `p-eight-sided` | part 3.
    The question says "Part 1 found 7 outcomes with a total of 10, and 2 of them hold an 8." That is the answer, $\tfrac{2}{7}$, read off the question.
    Fix: "Now turn it round. Part 1 found 7 outcomes with a total of 10. Given the total is 10, what is the chance at least one die shows an 8?"

12. `minor` | `conditional/problems-2.json` | `p-bad-ticks` | part 3.
    The `odds` entry is 33.93 with `tol` 0.0005. The odds are $\tfrac{0.019}{0.0392} \times 70 = 33.9286$, so 33.9, 33.929 and 33.9286 all miss the band and the line never fires for a learner who rounds differently.
    Fix: value 33.93, `tol` `{ "abs": 0.05 }`.

13. `minor` | `conditional/problems-3.json` | `p-three-loans` | part 4.
    The `difference` entry is 0.004536 with `tol` 0.005, so every answer from 0 to 0.0095 (0.001, 0.005536, 0) is told "That is the difference."
    Fix: `tol` `{ "abs": 0.00001 }` on `difference`.

14. `minor` | `conditional/problems-2.json` | `p-bad-ticks` | part 4.
    "How many good prints are flagged by both filters?" has the answer 39.2 prints. A count that is not whole undoes the point of picturing prints (l9).
    Fix: picture 1,000,000 prints: answer 392, `tol` 0, `a-only` 39200, `all-prints` 400; part 5 becomes $\tfrac{392}{13{,}300 + 392}$, the same 0.0286.

15. `minor` | `conditional/problems-2.json` | `p-takeover-rumour` | part 4.
    The part uses no earlier result and restates none, so the chain stops at part 3.
    Fix: open with "Part 3 gave 0.395, under one half, so the fund does not trade at today's base rate of 0.08."

16. `minor` | freshness, two items.
    `counting-chance/problems-1.json` `p-d4-against-d6` part 4 is l2's bet ("pays £10 if the red die beats the blue die ... fair price") with one die changed. `conditional/problems-3.json` `p-odd-dice` is l15's two-coin example relabelled (first odd, second odd, total even for first heads, second heads, coins match), down to "$A$ and $B$ together settle $C$". Both pass the fresh-check gate; neither is a new setting.
    Fix: keep `p-d4-against-d6` but price a different event (for example a pay-out on a tie). Replace `p-odd-dice`'s setting, for example three desks where each pair shares one data feed.

17. `minor` | last parts that restate.
    `counting-chance/problems-2.json` `p-breach-check` part 5 and `counting-chance/problems-3.json` `p-ace-and-king` part 4 turn the previous part's chance into a count; `conditional/problems-3.json` `p-odd-dice` part 5 bolts eight rounds on after the result (part 4). The brief asks the last part for the result the problem is about.
    Fix: `p-breach-check` part 5: ask how many orders the checker must pick for the chance of at least one breach to pass 0.9 (6: $1 - \tfrac{\binom{11}{6}}{\binom{15}{6}} = 0.908$, against 0.846 at 5). `p-ace-and-king`: covered by finding 1. `p-odd-dice`: move part 5's l14 step into `p-gap-days` or accept it.

18. `minor` | difficulty labels.
    `counting-chance/problems-1.json` `p-tetra-eight` is the set's only 5, but its parts are $4 \times 4$, $\tfrac{1}{16}$, a power, a complement and one more multiplication; it is a 4. `p-octahedral-prize` (list six pairs, one union) is a 3. `conditional/problems-1.json` `p-dealer-calls` (5) is no harder than `p-watchlist` (4).
    Fix: either relabel and accept that these two level-1 sets have no true 5, or harden one part each: `p-tetra-eight` part 5 without the stepping hint (ask for the smallest $n$ with chance above 0.9: $n = 36$, since $(15/16)^{35} = 0.1045$ and $(15/16)^{36} = 0.0979$); `p-dealer-calls` part 4 conditioned on stopping on call 2 or later.

## Per set

- Coverage: every lesson of each level is drawn on, and each problem draws on at least two (checked against the reports' tables and the items). Each set has at least one item labelled 5 (see finding 18 for two of them).
- Chains: all 24 are real chains with the needed value restated in the later part, apart from findings 15 and 17. No opening prose gives away a part's answer; finding 11 is the one later part that states its own answer.
- Typed parts: 16 or 17 of 17 or 18 in every set; each `choice` part is a judgement.
- `wrong` entries: every value differs from its answer, no two bands overlap, every id has a `byKey` line; findings 8, 9, 10, 12 and 13 are the loose ones.
- Voice: British English, no exclamation marks (the hits are factorials), no em-dashes, £ throughout, no explanation over three sentences.

## Counts

| tag | count |
|---|---|
| wrong | 3 |
| unclear | 4 |
| minor | 11 |

Clean problems (no finding other than the form sentence of finding 4): counting-chance `p-two-feeds`, `p-relay-team`, `p-vote-tallies`, `p-feed-audit`, `p-shard-clash`, `p-three-downgrades`; conditional `p-watchlist`, `p-broker-algo`, `p-gap-days`, `p-losing-week`. Of these, `p-two-feeds`, `p-vote-tallies`, `p-feed-audit`, `p-shard-clash` and `p-three-downgrades` need no edit at all.
