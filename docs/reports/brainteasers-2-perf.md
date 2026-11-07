# brainteasers level 2: performance task

- File: `app/content/courses/brainteasers/homework-2.json`, item `hw9-circle-hats` appended (index 8, item 9 of 9). Nothing converted; the homework had 8 items.
- Kind: `code` (Python). Difficulty 5, skills `bz-strategy`, `bz-invariant`, no `tags`.
- Objective (verb rule, "design"): l7 "Design a team strategy for hat-colour puzzles using parity." The only objective of the level that matches.
- Why `code`: the plan is a function of what each person sees, so it runs. A hidden postlude, `worst_case(n)`, plays every one of the $2^n$ colourings and every person in a shuffled order, so a plan that stores earlier calls cannot learn its own hat. A passing plan is therefore proved on every colouring of each size tested, which a self-marked proof cannot match.
- Task: a circle of $n$ in red or blue hats; each sees only the two neighbours; all guess at once. Guarantee $\lfloor n/2 \rfloor$ right for every colouring. The lesson's whole-team sum fails here (nobody sees everyone), so the learner must design the pairing: one partner bets the hats match, the other that they differ.
- Tests: 9 hidden (`worst_case(n)` for n = 2, 3, 4, 5, 7, 8, 9, 10, 12), 1 example (n = 6). The starter fails; 7 planted plans all fail (whole-circle parity, copy left, opposite of left, both partners bet match, wrong neighbour, guess only on agreement, partner picked by i % 3).
- Freshness grep: circle, neighbour, beside, partner, pair, match, differ, opposite, simultaneous. No hit in the course uses neighbour-only sight or the match and differ pair; `fresh-check --file` gives no hit on the item.

## Gates

1. `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors; "brainteasers/L2: has a performance task, remove from perf-pending" as expected.
2. `VOICE_BASE=app/content/courses/brainteasers python3 docs/reviews/voice-scan.py 35`: 0 and 0.
3. `python3 -I docs/reports/brainteasers-2-perf-numbers.py`: exit 0. It runs the item's solution, starter and planted plans through the item's postlude and tests. A second route counts right guesses directly for n = 2 to 12: fewest is $\lfloor n/2 \rfloor$, exactly $n/2$ on every colouring for even n, total $n 2^{n-1}$ (the explain's average). It also tries every plan for n = 2, 3 and 4: none guarantees more than $\lfloor n/2 \rfloor$.
4. `node tools/playthrough.mjs --set brainteasers/homework-2 --local-cdn <pkgs>`, with and without `--mobile`: All passed, "1 performance starter fail". The 440 px shot fits.

Backlog: 0 new bullets.
