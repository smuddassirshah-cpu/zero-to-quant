# Problem sets: functions (brief `docs/briefs/chained.md`)

Files: `app/content/courses/functions/problems-1.json` to `problems-3.json`. Numbers: `docs/reports/problems-functions-numbers.py` (exits 0, 774 checks).

## Sets

| set | item | parts (typed / choice) | lessons drawn on | difficulty |
|---|---|---|---|---|
| problems-1 | p-exchange-kiosk | 4 (4 / 0) | l1, l2 | 3 |
| problems-1 | p-van-fuel | 5 (4 / 1) | l1, l2, l3 | 4 |
| problems-1 | p-stone-throw | 5 (4 / 1) | l1, l3, l4 (and l2) | 5 |
| problems-1 | p-sapling-log | 4 (3 / 1) | l1, l2, l4 | 4 |
| problems-2 | p-candle-burn | 4 (3 / 1) | l5, l6, l7 | 3 |
| problems-2 | p-path-and-pipe | 5 (5 / 0) | l6, l8, l9 | 5 |
| problems-2 | p-two-gyms | 4 (4 / 0) | l6, l7, l8, l9 | 4 |
| problems-2 | p-two-savers | 4 (3 / 1) | l5, l6, l7, l9 | 3 |
| problems-3 | p-bakery-trays | 5 (4 / 1) | l10, l11 | 4 |
| problems-3 | p-sledge-cyclist | 5 (4 / 1) | l10, l12, l13 | 5 |
| problems-3 | p-two-cultures | 5 (4 / 1) | l10, l13 | 4 |
| problems-3 | p-track-cubic | 4 (3 / 1) | l10, l11, l13 | 4 |

Typed parts: level 1 15 of 18, level 2 15 of 17, level 3 15 of 19. Every lesson of each level appears in at least one problem, and every problem draws on at least two. Settings are everyday (a kiosk, a van, a candle, two gyms, a bakery, a sledge) to suit a learner from GCSE; no broker fees, which the course's lessons, reviews and homework already use often.

Level 1 chains. p-exchange-kiosk: climb per £1 from a table, the rule, a value, then undoing it for a target. p-van-fuel: a value, the empty tank, the domain it fixes, the range on it, then the range on a smaller domain. p-stone-throw: $h(0)$ with the negative-bracket trap of l1, the landing time (parts 2 and 4 now give the step $(t - 2)^2 = 9$ and $= 1$, so no new algebra is assumed), the range (the top lies inside the domain), the two times at 40 m, then why height to time is not a function. p-sapling-log: a log with one week twice (not a function), the rate from the kept rows, the rule, then undoing it.

Level 2 chains. p-candle-burn: gradient, intercept, burn-out time, then the axis point $(10.4, 0)$. p-path-and-pipe: path $A(-2, 1)$, $B(5, 29)$ gives gradient 4 and $y = 4x + 9$, the perpendicular gradient $-0.25$, the pipe from $D(12, 23)$, $y = -0.25x + 26$, then where they meet, $(4, 25)$ (renumbered in the fix pass, for freshness). p-two-gyms: rate and fee from two statements, the break-even month, then the 12-month saving. p-two-savers: a table value, rate and start from two points, then parallel lines that never meet (the last part restates Asha's £130 and Ben's £110).

Level 3 chains. p-bakery-trays: y-intercept, roots, turning point halfway between them, where the curve rises, then the top (parts 4 and 5 swapped in the fix pass, so the greatest profit is last). p-sledge-cyclist: $0.5t^2$ at 5 seconds (12.5 m), the average speed (2.5 m/s), the crossing with $3t$, the distance, then which is faster at the crossing (gradient against height). p-two-cultures: $200 \times 2^t$ against $1000 + 300t$, the lead at 3 hours, one crossing, an estimate to 1 decimal place (3.32), then the count there. p-track-cubic: $h(x) = x(x - 6)^2$ on $0 \le x \le 8$: $h(4) = 16$, roots 0 and 6, where it falls ($2 < x < 6$), then $h(x) = 32$ with the flat line through the top, $x = 2$ and $8$ (renumbered in the fix pass, for freshness).

Each later part restates the value it uses, and the slip that follows from the commonest slip in the part before has its own `wrong` (for example `46x-1797`, `10w+7`, a candle 16 cm tall, 700 cells from $N = 1200$).

## Faults of the 1.3 readers, checked

- Bands: estimates keep the explanation's figures inside the band (3.3 ± 0.05 takes 3.32; 2000 ± 50 takes 1990 and 1970; `accept` says so).
- `accept` lines name numbers only, no forms the field cannot read.
- No % units; `wrong` bands are 0 to 0.5 wide and never cover the small numbers of another slip. One broad entry (gyms `rates-sum`, 0.21 to 1.21) was dropped.
- Every `why` was read against the item's own numbers; no last part contradicts an earlier one.
- Engine graders: a scratch copy of the 1.3-b `grade-check.mjs` with 85 typed strings (roundings, fractions, `£200`, `t = 1, t = 3`, `2 \pm 1`, one value for two) gave 334 checks, 0 failures.

## Checks

| check | result |
|---|---|
| number script | exit 0, 774 checks, 0 failures |
| validator | 0 errors; no warnings on the three files |
| playthrough, desktop and `--mobile`, `--local-cdn` | green for all three sets; shots at 440 px read, no layout faults |
| voice scan 35 on the course folder | 0 and 0 |
| fresh-check `--file` | 0 hits per set |

Fresh-check triage (`--min-run 8 --min-share 0`): 10 hits, all the required sentences "Type only what comes after the $=$ sign" and "Give a whole number. Using ...". No setup, function or numbers are shared. By hand I also checked each set against the course's quizzes, reviews, homework and the 0.2 topic exam: the nearest are `hw3-min-value` (turning point halfway between roots, other roots and story) and `r-undo-square` (squaring not undone by a function, here two times for one height). Both are the idea, not the setup, so they stand.
