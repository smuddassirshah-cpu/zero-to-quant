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
