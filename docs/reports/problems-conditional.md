# Problem sets: conditional (brief `docs/briefs/chained.md`)

Files: `app/content/courses/conditional/problems-1.json`, `problems-2.json`, `problems-3.json`. Numbers: `docs/reports/problems-conditional-numbers.py` (exits 0).

## Sets

| set | item | parts (typed / choice) | lessons drawn on | difficulty |
|---|---|---|---|---|
| problems-1 | p-eight-sided | 4 (4 / 0) | l1, l3, l4 | 3 |
| problems-1 | p-watchlist | 5 (5 / 0) | l2, l3, l4, l5 | 4 |
| problems-1 | p-order-router | 5 (4 / 1) | l4, l5, l6 | 4 |
| problems-1 | p-dealer-calls | 4 (4 / 0) | l2, l3, l4, l5, l6 | 5 |
| problems-2 | p-takeover-rumour | 4 (4 / 0) | l7, l8, l9 | 3 |
| problems-2 | p-downgrade-news | 5 (4 / 1) | l10, l11 | 4 |
| problems-2 | p-broker-algo | 4 (4 / 0) | l11, l12 | 4 |
| problems-2 | p-bad-ticks | 5 (5 / 0) | l7, l8, l9, l10, l11 | 5 |
| problems-3 | p-gap-days | 4 (3 / 1) | l13, l14 | 3 |
| problems-3 | p-losing-week | 4 (3 / 1) | l13, l16 | 4 |
| problems-3 | p-three-loans | 4 (4 / 0) | l14, l16, l17 | 5 |
| problems-3 | p-odd-dice | 5 (4 / 1) | l13, l14, l15 | 4 |

Typed parts: level 1 17 of 18, level 2 17 of 18, level 3 14 of 17 (at least two thirds each). Every lesson of each level appears in at least one problem, and every problem draws on at least two.

Chains. p-eight-sided: a count, the count under news, the condition turned round inside level 1's counting, then the multiplication rule from both. p-watchlist: two picks, the third given them, the path, three paths, then the share of one path inside the news. p-order-router: one path, total probability, a re-send, a rival router, the choice between them. p-dealer-calls: stopping on call 2, call 3, within three, then the first call's share given a stop. Each later part restates the value it uses, and its `wrong` list holds the value that follows from the commonest slip in the part before (with-replacement chances, the equal average, the double-counted cell).

Level 2 chains: p-takeover-rumour runs natural frequencies to a posterior, then the base rate at which a rumour is an even bet. p-downgrade-news goes prior odds, one ratio, a second ratio, the number of further reports to reach 0.95, then the judgement that dependent news double counts. p-broker-algo updates three hypotheses twice and ends with the chance of the next fill. p-bad-ticks runs two filters by probability, then checks the posterior by counting 100,000 prints.

Level 3 chains: p-gap-days tests independence in a 400-day tally, then uses the rate as independent trials. p-losing-week finds the chance of a failure given a loss, then given the loss and a squeeze, and ends on the judgement that a shared effect links independent causes. p-three-loans weights regimes for one loan and for all three, sets that against the independent model and gives the ratio, 5.536. p-odd-dice shows pairwise independence, finds that $A$ and $B$ settle $C$, and carries $P(A \cap B \cap C) = \tfrac{1}{4}$ into eight rounds; the $\tfrac{1}{8}$ slip has its own `wrong` value there.

Level 1 teaches no Bayes, so no part turns a likelihood into a posterior; conditioning inside a news event uses only $P(A \mid B) = P(A \cap B)/P(B)$ from l3.

## Checks

| check | problems-1 | problems-2 | problems-3 |
|---|---|---|---|
| numbers script | 0 failures | 0 failures | 0 failures (572 checks in all) |
| validator | 0 errors, 0 warnings on the file | same | same |
| playthrough `--local-cdn` | green (18 parts) | green (18 parts) | green (17 parts) |
| playthrough `--mobile` | green; 440 px shots read, no fault | same | same |
| voice scan 35 (course folder) | 0 and 0 | 0 and 0 | 0 and 0 |

## Fresh-check

`node tools/fresh-check.mjs --file content/courses/conditional/problems-1.json`: 0 hits at the gate. At triage settings (`--min-run 8 --min-share 0`) one hit: "what is the chance the total is # now" against `l3-shrinking` screens[2], share 0.09. Stock phrasing; the setup (an eight-sided die, totals of 10) is new. problems-2: 0 hits at the gate and 0 at triage settings. problems-3: 0 hits at the gate; at triage settings two hits on p-odd-dice, "two fair dice are rolled let # be the first die", against `homework-1` items[3] and `random-vars/l1-number-per-outcome` quiz[3] (share 0.1). Stock phrasing: those items use other events (a 6, totals of 7 and 8). An earlier draft of p-three-loans matched `review-3` r-two-loans on its prose ("a recession comes with chance # each loan then defaults"); the prose was rewritten and the hit is gone. The regime model itself is the level's own (l17), with new numbers and a new question (three loans against the independent model).

## Engine limits

Three bullets in `docs/BACKLOG-INBOX.md` under "Raised later (problems conditional)": the playthrough shoots only part 1 of a problem set; the result page labels problems by their whole prose; the done page says "Well done.". None blocked a problem.

## Level 4

File: `app/content/courses/conditional/problems-4.json` ("Problems: puzzles that fool experts", 45 minutes). The numbers script now also checks level 4 (and level 5 once it exists).

| set | item | parts (typed / choice) | lessons drawn on | difficulty |
|---|---|---|---|---|
| problems-4 | p-marble-bags | 4 (4 / 0) | l18, l19 | 4 |
| problems-4 | p-two-strategies | 4 (4 / 0) | l18, l20 | 3 |
| problems-4 | p-two-flags | 5 (5 / 0) | l20, l21 | 4 |
| problems-4 | p-dated-coins | 5 (5 / 0) | l19, l21 | 5 |

Typed parts 18 of 18 (two are `expression`). Each lesson appears in two problems, and every problem draws on two.

Chains. p-marble-bags: the chance of a black draw (0.5), the chance the partner is black (0.4, counting marbles, not bags), a dealer who shows black from a mixed bag with chance $h$ ($\tfrac{1}{1+3h}$), then the $h$ that makes his black as telling as a random draw (0.5). p-two-strategies: at least one winner (0.91), the letter naming B (0.455), both won given the letter ($\tfrac{7}{13}$, equal to the "at least one" answer), then a manager with a habit ($\tfrac{7}{22}$). p-two-flags: "at least one long" ($\tfrac13$), the 23 pairs that fit a long in energy, $\tfrac{11}{23}$, a trade shown at random ($\tfrac12$), then the fewest sectors that bring the "at least one" answer within 0.01 of it (13). p-dated-coins: a drawn gold coin (0.8), a gold box holding a 1987 coin (0.19), the assistant's report ($\tfrac{19}{24}$), the likelihood ratio $2 - \tfrac{1}{k}$, and its limit 0.8, the drawn-coin answer. Each later part restates the value it uses, and its `wrong` list holds the value from the commonest slip before it (0.8 in place of 0.5 gives 0.25; 24 pairs gives $\tfrac{12}{24}$; 0.2 in place of 0.19 gives 0.8).

Settings are new to the course: no lesson, review, homework or earlier problem set uses marble bags of this make-up, two strategies with a named winner, flagged trades by sector, or dated coins. The dealer's rate $h$ echoes homework-4's host with a habit $q$ on purpose (l18's host's rule), in a new setting with new numbers and a new question.

Checks: numbers script 0 failures (790 checks with levels 1 to 4); validator 0 errors, 0 warnings on the file; playthrough `--local-cdn` green (18 parts), `--mobile` green, 440 px shots read with no fault; voice scan 35 on the course folder 0 and 0.

Fresh-check: 0 hits at the gate. At triage settings (`--min-run 8 --min-share 0`) three hits, all stock phrasing at shares of 0.07 or less: "what is the chance both won give a decimal" against homework-4 items[3] (a trader at 0.55, a different report), and "what is the chance the other coin is gold" against l19 screens[5] and review-4 items[1] (different boxes: two GG, one GS, one SS here).

Engine limits: none new. The first bullet of "Raised later (problems conditional)" applies again: the playthrough shoots only part 1, so the two `expression` parts were graded but not shot.

## Level 5

File: `app/content/courses/conditional/problems-5.json` ("Problems: reasoning in the wild", 45 minutes).

| set | item | parts (typed / choice) | lessons drawn on | difficulty |
|---|---|---|---|---|
| problems-5 | p-warning-screen | 4 (3 / 1) | l23, l26 | 4 |
| problems-5 | p-two-houses | 4 (3 / 1) | l24, l25 | 3 |
| problems-5 | p-signal-streak | 5 (5 / 0) | l22, l26 | 5 |
| problems-5 | p-doubling-desk | 4 (3 / 1) | l22, l25 | 4 |

Typed parts 14 of 17 (at least two thirds). Every lesson of the level appears in at least one problem (l22, l25 and l26 in two), and every problem draws on two. The three choice parts are judgements: which conditional the vendor's 2% is, why a house that loses in both groups leads overall, and what a survivors' newsletter shows.

Chains. p-warning-screen: a flag gives 0.3125 (18 true flags against 39.6 false), the brochure's 2% is the prosecutor's swap, a second independent screen takes the chance to $\tfrac{40}{51}$, and Kelly stakes $\tfrac{29}{51}$ on an even-money contract (nothing on one flag). p-two-houses: House R's 4.4% over all launches, House S's survivorship gap of 5 points, the reversal read as Simpson's paradox with survival as the hidden variable, then R ahead by 1.4 points where survivors put S ahead by 1. p-signal-streak: a good call is still right with chance 0.6 after four misses (no right call is due), the ratio $0.8^4$, the chance the call is good ($\tfrac{256}{881}$), tomorrow's chance 0.529, and a Kelly stake of 0.058 against 0.1 before the streak. p-doubling-desk: a round averages £0, $(\tfrac{31}{32})^{20} \approx 0.530$ of traders finish, a quitter averages −£22.55 by total probability for averages, and the newsletter of survivors is survivorship bias. Each later part restates the value it uses, and its `wrong` list holds the slip before it (0.9 for 0.3125 gives 0.9863; 3 for the gap gives −0.6; $1.2^4$ for $0.8^4$ gives 0.6747).

Settings are new to the course: profit-warning screens, two fund houses compared over survivors and closed funds, a vendor's call of unknown quality, and a desk of traders on a five-loss doubling cap. l22 used caps of six and four bets and homework-5 three; the fair-or-useless call echoes l22's unknown coin with new numbers and a Kelly ending.

Checks: numbers script 0 failures (979 checks with levels 1 to 5); validator 0 errors, 0 warnings on the file; playthrough `--local-cdn` green (17 parts), `--mobile` green, 440 px shots read with no fault in the files; voice scan 35 on the course folder 0 and 0.

Fresh-check: 0 hits at the gate. At triage settings seven hits, all question stock at shares of 0.08 or less: "what fraction of capital does the Kelly rule" (l26 quiz[3]), "by how many percentage points does the survivors" (homework-5 items[3], `alpha/l3-including-the-dead`), "give a decimal using # from part # what is the chance the" (problems-2 items[2]) and "what is the expected profit of one round in pounds" (l22 screens[9], review-5 items[5]). The settings and numbers differ in each.

Engine limits: one new bullet in `docs/BACKLOG-INBOX.md` under "Raised later (problems conditional)", for levels 4 and 5: the 440 px course-row shot does not show the problem-set row.
