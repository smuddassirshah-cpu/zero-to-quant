# Problem sets: conditional (brief `docs/briefs/chained.md`)

Files: `app/content/courses/conditional/problems-1.json`. Numbers: `docs/reports/problems-conditional-numbers.py` (exits 0).

## Sets

| set | item | parts (typed / choice) | lessons drawn on | difficulty |
|---|---|---|---|---|
| problems-1 | p-eight-sided | 4 (4 / 0) | l1, l3, l4 | 3 |
| problems-1 | p-watchlist | 5 (5 / 0) | l2, l3, l4, l5 | 4 |
| problems-1 | p-order-router | 5 (4 / 1) | l4, l5, l6 | 4 |
| problems-1 | p-dealer-calls | 4 (4 / 0) | l2, l3, l4, l5, l6 | 5 |

Chains. p-eight-sided: a count, the count under news, the condition turned round inside level 1's counting, then the multiplication rule from both. p-watchlist: two picks, the third given them, the path, three paths, then the share of one path inside the news. p-order-router: one path, total probability, a re-send, a rival router, the choice between them. p-dealer-calls: stopping on call 2, call 3, within three, then the first call's share given a stop. Each later part restates the value it uses, and its `wrong` list holds the value that follows from the commonest slip in the part before (with-replacement chances, the equal average, the double-counted cell).

Level 1 teaches no Bayes, so no part turns a likelihood into a posterior; conditioning inside a news event uses only $P(A \mid B) = P(A \cap B)/P(B)$ from l3.

## Checks

| check | problems-1 |
|---|---|
| numbers script | 0 failures |
| validator | 0 errors, 0 warnings on the file |
| playthrough `--local-cdn` | green (18 parts) |
| playthrough `--mobile` | green; 440 px shots read, no layout fault |
| voice scan 35 (course folder) | 0 and 0 |

## Fresh-check

`node tools/fresh-check.mjs --file content/courses/conditional/problems-1.json`: 0 hits at the gate. At triage settings (`--min-run 8 --min-share 0`) one hit: "what is the chance the total is # now" against `l3-shrinking` screens[2], share 0.09. Stock phrasing; the setup (an eight-sided die, totals of 10) is new.

## Engine limits

None met in level 1.
