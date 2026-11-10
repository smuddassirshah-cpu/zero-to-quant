# Problem sets: markov (brief `docs/briefs/chained.md`)

Files: `app/content/courses/markov/problems-1.json` (more levels below). Numbers: `docs/reports/problems-markov-numbers.py` (exits 0). The course writes distributions as row vectors, $\boldsymbol{\pi}_{k} = \boldsymbol{\pi}_0\mathbf{P}^k$, with rows of $\mathbf{P}$ adding to 1; every set follows that.

Every numeric part ends with a form sentence ("Give a decimal to 2 places.", "Give a fraction, or a decimal to 4 places."), its `tol` accepts that rounding, and the numbers script checks that the value printed in `feedback.correct` is accepted by the part's own `tol`. Where a part hands the learner a rounded value (3.33 months, 6.67 minutes), the script also checks that the answer from the rounded value is accepted.

## Level 1

File: `problems-1.json` ("Problems: chains, paths and regimes", 45 minutes).

| set | item | parts (typed / choice) | lessons drawn on | difficulty |
|---|---|---|---|---|
| problems-1 | p-thin-book | 4 (4 / 0) | l2, l4 | 3 |
| problems-1 | p-two-losses | 4 (4 / 0) | l1, l2, l3 | 4 |
| problems-1 | p-margin-calls | 4 (3 / 1) | l1, l3 | 4 |
| problems-1 | p-carry-pause | 5 (5 / 0) | l2, l4 | 5 |

Typed parts 16 of 17. Every lesson appears in at least one problem, and every problem draws on two or more.

Chains. p-thin-book: a matrix estimated from transition counts ($\hat p_{TT} = 0.7$), a two-step chance from it (0.535), the mean Thin spell (3.33 minutes), then the long-run Thin share from the spell lengths ($\tfrac13$, which the record's 20 of 60 moves confirms). p-two-losses: a rule that stops a trader after two losses in a row, written as a chain with an absorbing stop; one path (0.0216), stopped by trade 2 (0.18), by trade 3 (0.306, cumulative absorption), then the stop on trade 4 exactly (0.1098). p-margin-calls: a first return within two days (0.65, against $(\mathbf{P}^2)_{MH} = 0.6$ as a `wrong` value), ever back ($\tfrac57$), $f_H = \tfrac{34}{35}$, then the judgement that every account is liquidated in the end because only X is closed. p-carry-pause: a stressed spell (3.33 months), the calm share ($\tfrac67$ from run lengths, as l4 teaches), the long-run P&L of a carry trade (£1.43m a month), the expected month after stress (−£4.7m), then a rule that trades only after calm months (£2.1m a month). Each later part restates the value it needs, and its `wrong` list holds the value from the commonest slip before it (0.535 in place of 0.7; 0.65 in place of $\tfrac57$; a stressed spell of 1.43 months).

Level 1 teaches no $\boldsymbol{\pi}\mathbf{P} = \boldsymbol{\pi}$ (that is l5), so the long-run shares come from mean run lengths, as in l4, and the hitting chances from the return argument of l3 and homework-1.

Checks (level 1):

| check | result |
|---|---|
| numbers script | 361 checks, 0 failures |
| validator | 0 errors, 0 warnings on the file |
| playthrough `--local-cdn` | green (4 problems, 17 parts) |
| playthrough `--mobile` | green; 440 px shots read, no fault |
| voice scan 35 (course folder) | 0 and 0 |

Fresh-check: 0 hits at the gate. At triage settings (`--min-run 8 --min-share 0`) one hit, "give a decimal to # places using # how many", against `counting-chance/problems-3.json` items[2], share 0.06: the form sentence, stock phrasing. The settings are new to the course: no lesson, review or homework uses a Deep and Thin order book, a two-loss stop, margin calls or a paused carry trade. The bull and bear numbers, the A, B, Default ratings and the weather chain of the lessons are not reused.
