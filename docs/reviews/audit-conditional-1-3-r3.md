# Concept audit, round 3: conditional (topic 1.5), levels 1 to 3

Auditor: Fable, blind read, 11 Nov 2026. Scope: `l1` to `l17`, `review-1` to `review-3`, `homework-1` to `homework-3` (with the performance task `h-two-filters`), `problems-1` to `problems-3`, `fluency-l7-turning-around`. Levels 4 and 5 are out of scope.

Ledger: `docs/reports/audit-conditional-1-3-r3-ledger.md` (243 hand-judged rows: 235 correct, 0 wrong, 7 imprecise, 1 misleading, 0 unverified).
Script: `docs/reports/conditional-L1-3-concepts-r3.py` (own helper code; exact enumeration with fractions, a generic tree check, both code widgets run under CPython 3 with the standard library only, and seeded Monte Carlo for the empirical claims). It exits 1 while the findings below are open: 934 checks pass, 6 fail, one per finding.

## Result in one paragraph

I found no `wrong` claim in these 27 files. Every graded key, every slip value, every tree, every summary `trap` line and every direction word I read agrees with the item's own numbers and with the standard sources. What is left is six findings, all `minor`: five `imprecise` and one `misleading`. Four concern the bare word "independent" where the kind matters, one a rounding collision in a graded key, and one a tree canvas whose leaves are not path products.

## What was checked with special care

- **Direction words.** Each "rose", "fell", "up from", "down from" and "back to" was read against the two numbers it joins (ledger row 239). All agree, including the l11 positive-then-negative screen (0.0188, above the 0.01 base rate) and the l16 explaining-away screen (0.714 falls to 0.2).
- **Summary `trap` lines.** All 17 read against their trap screens (row 238). All agree.
- **Tree canvases.** The script walks every tree in scope: branches out of each node add to 1, shown leaves equal the path products, and leaves add to 1. One exception, finding 5.
- **Conditioning protocol.** Every "at least one" item says the learner asked a stated yes-or-no question and heard yes (l3 screens 3 and 7, review-1 items[3], homework-1 items[2] and [6], problems-1 items[0] part 2). The Monte Carlo check separates 1/11 from 1/6 for the dice.
- **Kinds of independence.** See findings 1, 2, 3 and 6. The lessons themselves (l10 screens[8], l11 screens[0], [7], [8] prose, summary) state independence given the hypothesis and given its negation.
- **Exclusive and exhaustive hypotheses.** l6 screens[7] and l12 screens[7] state both conditions; every prior list in scope adds to 1.
- **Odds against probability, and counts against rates.** No mismatch found (rows 242, 243).

## Findings

Pattern: `N. file | JSON path | severity | problem | evidence and basis | exact fix`.

1. `l11-updating-twice.json` | `screens[8].feedback.byKey.one` | imprecise, minor | The line says "The second independent call adds more." The two calls are not independent. They are independent only given the stock's direction, which is what the screen's prose says. | P(A says up) = P(B says up) = 0.5, but P(both say up) = 0.5 × 0.49 + 0.5 × 0.09 = 0.29, not 0.25 (script, "basis for F1"). Lesson 16 of the same course later teaches that calls like these are "correlated overall, yet independent given the truth". Blitzstein and Hwang 2.5. | Replace with: "That is one analyst's call. The second call errs independently of the first, whichever way the stock goes, so it adds more."

2. `review-2.json` | `items[5].feedback.byKey.added` | imprecise, minor | "Independent ratios multiply, giving 9." A ratio is a number and cannot be independent. What lets the ratios multiply is that the signals arise independently given a battle and given no battle, as the item's prose says. | Odds form for two pieces of evidence needs P(E1∩E2 given H) = P(E1 given H)P(E2 given H) and the same given not H (Blitzstein and Hwang 2.6). | Replace with: "You added the ratios to get 6. The signals arise independently, battle or no battle, so their ratios multiply to give 9."

3. `problems-2.json` | `items[1].parts[2].feedback.byKey.ratio-sum`, `items[1].parts[3].question`, `items[1].parts[4].feedback.correct` | imprecise, minor | Three lines of one item use the bare word. (a) "Independent evidence multiplies". (b) "how many more independent reports, each with ratio 3". (c) "The exit was not independent of the delay". The item's prose defines the right kind: "Given the truth, the two arise independently." In (c) the bare word is false as a contrast: the exit and the delay were never independent overall, since both are likelier in a downgrade year. What the new fact breaks is independence given the truth. | With the item's rates, P(delay) = 0.26 and P(exit) = 0.0875, but P(both) = 0.15 × 0.18 + 0.85 × 0.01 = 0.0355, not 0.02275. So the two were dependent overall from the start. | (a) Replace with: "You added the two ratios, 3 + 6, and applied 9 to the prior. Given the truth the two reports arise independently, so their ratios multiply: $3 \times 6 = 18$." (b) Replace the question with: "The desk cuts its holding once the chance of a downgrade reaches 0.95. Each further report has ratio 3, like the delay, and arises independently of the others given the truth. From odds of $\tfrac{54}{17}$, how many more does it need?" (c) Replace with: "Given the truth, the exit no longer arises independently of the delay, so its ratio of 6 double counts."

4. `l8-base-rates.json` | `screens[2].question` with `screens[2].widget.wrong[1]` (`unweighted`, 0.059 ± 0.0001) | imprecise, minor | The question says "Give a decimal." The key is 0.0585 ± 0.0002. A learner who works it correctly and rounds to three places enters 0.059. That value is graded wrong and told "You added 5% without weighting it by the 99% who are healthy". So a right method gets a wrong diagnosis. | 0.01 × 0.9 + 0.99 × 0.05 = 0.0585, which rounds half up to 0.059; the slip 0.009 + 0.05 is also 0.059. The sister item `problems-2` `items[3].parts[0]` avoids this by asking for 4 places. | Replace the question with: "What is $P(+)$, the chance a random person tests positive? Give a decimal to 4 places."

5. `l17-correlated-defaults.json` | `screens[5].canvas` (`leaves` and `state.caption`) | misleading, minor | The tree shows leaves 0.3222 and 0.0002 under branches 0.2 and 0.8. They are each regime's chance of 3 or more defaults, not path products, and they add to 0.3224. Lesson 5 taught that a leaf is the product along its path and that "the leaves of a tree add to 1". The prose above the canvas does say what the leaves show, and the hint says to multiply each leaf by its branch, so the key is safe. The canvas alone breaks the convention the course set. | Path products would be 0.0644 and 0.00016 (script, generic tree check: this is the one tree in scope that fails it). | Replace `state.caption` with: "Each leaf is that regime's chance of 3 or more defaults, not a path product. Recession: 10 trials at 0.2. Normal: 10 trials at 0.0125."

6. `l15-pairwise.json` | `summary.formula.note` (nothing in the lesson states the convention) | imprecise, minor | Lesson 15 teaches that pairwise independence is not mutual independence. The course uses the bare word for three or more events before and after it: "Three independent trade ideas" (l14 screens[6]), "Three independent alerts" (l14 quiz[1]), "Four independent signals" and "Four independent trades" (review-3 items[2], [3]), "Assume months are independent" (homework-3 items[1]), "Ten borrowers ... independently" (l17). Each key needs mutual independence. That is the standard reading, but the course never says so, and a learner fresh from lesson 15 has reason to ask which kind is meant. | Convention: a family of events is called independent when the product rule holds for every finite subfamily (Grimmett and Stirzaker 1.5; Ross 3.4). The audit brief asks that a convention be said once where it first matters. | Replace `summary.formula.note` with: "Neither part implies the other: check both. When several events are called independent with no other word, mutually independent is meant." One sentence fixes every use; no other file needs a change.

### Severity tally

wrong 0; imprecise 5 (findings 1, 2, 3, 4, 6); misleading 1 (finding 5). Serious 0, minor 6.

## Things I checked and judge correct, though a reader might pause

- `l11` `screens[3].explain`: "The positive and negative nearly cancel, leaving you just above the 1% base rate." The product of the two ratios is 36/19, about 1.9, so the odds nearly double. On the log-odds line the jumps are +2.89 and −2.25. "Nearly cancel" is fair there, and the `base` feedback states the 1.9 outright.
- `l4` `screens[9].explain`: "That understates the clustering by a third." What is understated by a third is the chance of two fills from A in a row (0.16 against 0.24). The sentence follows that sum directly, so the meaning is clear.
- `l3` `summary.formula.note`: "you cannot condition on something impossible." Exact for the finite sample spaces of this stage.
- `l14`, `l17`, `review-3`: the bare word "independent" for several trials. Correct by convention; finding 6 asks only that the convention be stated once.
- `homework-2` `items[6]` part (c): "Independent repeat tests". Part (d) asks the learner to name the assumption, and the model answers with independence given H and given not H. The bare word is the prompt for that question, so I leave it.
- `l16` `summary.ideas[1]`: "A shared cause makes events dependent overall." For a two-valued cause that moves both events the same way this always holds: the gap is q(1 − q)(a₁ − a₀)(b₁ − b₀), the identity homework-3 proves.

## After the blind commit

The sections below were added after the ledger, findings and script were committed.
