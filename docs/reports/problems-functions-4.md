# Problem set: functions level 4 (brief `docs/briefs/chained.md`)

File: `app/content/courses/functions/problems-4.json` ("Problems: building new functions", 40 minutes). Numbers: `docs/reports/problems-functions-4-numbers.py` (exits 0, 444 checks). Engine graders: `docs/reports/problems-functions-4-grade.mjs` (247 checks, 0 failures). Sets 1 to 3 and their script and report are untouched; this set's checks live in their own files while a fix pass runs on those.

## Set

| set | item | parts (typed / choice) | lessons drawn on | difficulty |
|---|---|---|---|---|
| problems-4 | p-photo-mount | 5 (5 / 0) | l16, l17 | 4 |
| problems-4 | p-fountain-jet | 4 (3 / 1) | l15, l14 | 4 |
| problems-4 | p-car-park | 5 (4 / 1) | l18, l17, l14 | 4 |
| problems-4 | p-ticket-bonus | 4 (4 / 0) | l18, l16, l17, l15 | 5 |

Typed parts 16 of 18 (11 numeric, one of them a two-value set; 5 expression). Every lesson of the level appears: l14 (car park part 4 and 5, fountain part 2), l15 (fountain parts 2 to 4, bonus part 4), l16 (photo parts 1, 2 and 5, bonus part 2), l17 (photo parts 3 and 4, car park part 3, bonus parts 1 and 3), l18 (car park parts 1 to 3, bonus prose and part 1). Settings are everyday (a print shop, a garden fountain, a car park, a theatre bonus); no option, share or broker fee, which the level's lessons, review and homework already use.

Chains (every part's result is used by a later part).
- p-photo-mount: $m(e(12)) = 22$, the composite $1.5x + 4$ (checked against 22), its inverse $\tfrac{x - 4}{1.5}$, the photo for a 31 cm print (18), then that photo done in the other order, $e(m(18)) = 33$.
- p-fountain-jet: the top $h(6) = 5.4$, the rule that widens the jet to land at 15 with that top ($h(0.8x)$), the new top at 7.5, then the two points 4.05 m high, 3.75 m either side of 7.5.
- p-car-park: $C(4.5) = 9.25$, the rising piece $2.5t - 2$ (checked against 9.25), the stay for a £12.75 receipt (5.9 hours), the Monday rule $C(t - 1)$, then the 5.9-hour stay under it (£10.25).
- p-ticket-bonus: the kink at 20 tickets, $B(T(n)) = 5n - 100$ for $n > 20$, its inverse $\tfrac{b + 100}{5}$, then the tickets for £60 after a stretch by 1.5 (28).

Each later part restates the value or rule it uses. Carried slips: `carried` 4.7 (car park part 3, from part 2's `2.5t+1`), `earlier` 15.25 (part 5, from the choice's $C(t + 1)$), `top-plus-three` 4.5 and 10.5 (fountain part 4, 3 m from part 3's top), `wrong-order` in photo parts 3 and 4, `old-rate` 32 (bonus part 4, part 3's £60 at 20%).

## Faults of the latest readers, checked

- False general rules: each `why` and explanation was checked against the numbers (`h(1.25x)` lands at 9.6; `1.25h(x)` tops at 6.75; $C(t) - 2.5$ matches the Monday price only above 3 hours and charges 50p below 2; a vertical stretch keeps the zero at 20 tickets). "Swapping the order of two machines usually changes the output" is l16's own claim.
- Forms the prose prints: no number over 999 is printed, so no thousands comma reaches an expression field; `12,500` in a numeric field parses and is told it is the `times` slip.
- Taught by the end of the level: the top halfway between where the jet leaves and lands is stated in the question; widths times $\tfrac{1}{b}$ is l15; $C(t - 1)$ is l14's "minus inside moves right"; the cases display and $\max$ are l18; inverses by reversing steps are l17. No part needs a square undone or a root read from brackets.
- Bands: every key is exact (no rounding asked), with `tol` 0.001 on decimals so 5.4, 7.5, 5.9, 9.25 and 10.25 take trailing zeros; the set takes 3.75 and 11.25 as exact decimals, as the question says. `wrong` bands are 0 to 0.5, never more than a fifth of the slip's own value, and none overlaps the key or another slip; the 0.5 bands on non-whole slips of whole-number parts take a learner who rounds the slip.
- Expression keys are LaTeX only (`\frac`), and the grade check ran each key, `accept`, `wrong[].tex` and 114 typed strings: `y=1.5x+4`, `C=2.5t-2`, `n=\frac{b+100}{5}`, `3x/2+4`, `(x-4)\div1.5`, `0.2(25n-500)`, `5(n-20)`, `15/2`, `7 1/2`, `£9.25`, `x = 3.75, x = 11.25`, `3.75 and 11.25` all grade correct; each `wrong[].tex` lands on its own key.
- Freshness: `fresh-check --file` 0 hits. With `--min-run 8 --min-share 0`, 5 hits, all the sentence "Type only what comes after the $=$ sign". By hand I grepped the course, the 0.2 topic exam and stage 0 for each rule and value (`1.5x`, `0.15x`, `2.5t`, `5n - 100`, `25n`, `0.8x`, 12.75, 9.25, 4.05, 5.4) and the nouns (car park, fountain, photo, bonus): the only matches are the candle's $26 - 2.5t$ (set 2), a 9.25 in an l2 table and a £5.40 in `homework-2`, none a shared setting. The nearest ideas are `homework-4`'s tiered lot fee (a rate that drops, not a fixed fee then a rate) and its 50-call long-form (shift, stretch, inverse on a call; here the stretch is a bonus rate and the composite is new).

## Checks

| check | result |
|---|---|
| number script `problems-functions-4-numbers.py` | exit 0, 444 checks, 0 failures |
| grade check `problems-functions-4-grade.mjs --local-cdn` | 247 checks, 0 failures |
| validator | 0 errors; 0 warnings on `problems-4.json` (two `[wrong-band]` and one long-sentence warning fixed) |
| playthrough `--problems functions/problems-4 --local-cdn` | green, 4 problems, 18 parts |
| the same with `--mobile` | green |
| shots at 440 px | read; the cases display, the choice stacks and the fraction keys fit; one "£ $b$" line break fixed by writing "$b$ pounds" |
| voice scan 35, course folder | 0 and 0 |
| fresh-check `--file` | 0 hits |

Engine limits: two "Met again" bullets in `docs/BACKLOG-INBOX.md` under `Raised later (problems functions):` (raw LaTeX in the Accepted line; no form that refuses an unexpanded rule but takes a factorised one).
