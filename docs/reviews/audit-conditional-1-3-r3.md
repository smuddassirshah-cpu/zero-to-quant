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

Blind commit: `856507f0` (ledger, findings above and concepts script). Opened only after it: `docs/reviews/audit-conditional-1-3.md` (round 1 with its fix pass, fix-pass read and follow-up), `docs/reviews/audit-conditional-1-3-r2.md` (round 2 with its fix pass and fix-pass read), and searches of `docs/reviews/review-1.5.md` and `docs/reviews/review-problems-1.5-a.md` for the places of this round's findings. The earlier ledgers, concepts libraries and author reports were not used to change any verdict. No git history or diff of the course folder was read.

## Overlap with all earlier reads

Earlier conceptual findings on levels 1 to 3, as counted by rounds 1 and 2: 37 distinct (round 1 audit 23; round 1 fix-pass read 2; the two second-reader reviews 3 more, their fourth being round 1's finding 13; round 2 audit 9 more, its finding 5 being the class of round 1's finding 11). The round 2 fix-pass read raised none.

| | Count | Which |
|---|---|---|
| Found by this audit only | 3 | Finding 4 (l8 `screens[2]`, a rounded right answer graded as a slip), finding 5 (l17 `screens[5]` leaves) and finding 6 (the unstated convention that "independent" means mutually independent). See the notes below: two of the three were seen earlier and not raised as findings |
| Found by both | 3 | Findings 1, 2 and 3 are further places of one earlier class: round 1 finding 11 and round 2 finding 5 (evidence called plainly "independent" where independence given the hypothesis is needed). Those rounds fixed seven prose and summary places. The round 2 fixer listed these three places and left them "as shorthand"; the round 2 fix-pass read noted findings 1 and 2 as observations with no verdict |
| Found by earlier reads only | 36 | Every other earlier finding. All were fixed before this read, so the present text could not show them again |

`wrong` verdicts of this audit: 0. New `wrong` found by no earlier read: 0.

None of the 36 earlier findings has come back. Each of those places is a `correct` row in this ledger, read without knowing its history: the l3 and l16 `trap` lines (rows 29 and 238, with the l16 order of steps recomputed at row 156), the stated yes-or-no questions (rows 23, 27, 177, 194, 197, 218), l12 `screens[3]` "both dice gained" (row 117), the l11 `screens[8]` tree with leaves 0.245, 0.255, 0.045, 0.455 (row 111, and the script's generic tree check), l12 `screens[7]` (row 121), l1 `screens[6]` (row 6), l16 `quiz[2]` with its stated baseline (row 162), l15 "only a range" (row 145), l13 `quiz[1]` (row 133), l5 `screens[10]` (row 50), homework-2 `items[4]` and `items[6]` (rows 205 and 207), l17 `screens[6]` and `screens[10]` (rows 169 and 173). So both fix passes read as sound.

Where the reads touch:

- Finding 5. Round 2 saw the l17 `screens[5]` leaves and listed them under "Noted, not conceptual", because the prose says what they are. I weigh it differently: the canvas is what a learner looks at while answering, and round 2's own finding 2 was this use of `leaves` in l11. One caption sentence removes the clash. It stays `minor`.
- Finding 4. `review-problems-1.5-a` found the same class in problems-2 `items[3].parts[0]` (key 0.0582, slip 0.059, "Give a decimal") and it was fixed there by asking for 4 places. The l8 screen has the same numbers pattern and was not raised by any read.
- Finding 6. The round 2 fixer wrote that plain independence in l3, l14 and review-3 "is correct as written". I agree for each of those lines. The finding is that lesson 15 teaches two kinds for several events and never says which one the bare word means.
- Seen earlier and still present, read as `correct` here too: l8 `objectives[0]` ("See how a rare condition makes most positive tests false"), an aim line the lesson's own case bears out; homework-1 `items[4].explain.text` cites "Item 8" by position, which is right today.

Miss rate of a single read, on this evidence: after two reviews, two audits and two fix-pass reads, a third blind read finds no `wrong`, no `serious` finding and no graded key in doubt. It finds six `minor` points, of which four had been seen by an earlier reader and left.

Convergence: 0 new `wrong` in three levels is within the limit of one, so on this round levels 1 to 3 meet the closing rule in `docs/briefs/concept-audit.md`, once the fix pass for the six minor findings has had its fix-pass read.

## The two open minor notes from round 2

Both were weighed after the blind commit. Both were already findings of the blind read (1 and 2), reached before I knew they had been noted.

- `l11` `screens[8].feedback.byKey.one`, "The second independent call adds more." **Needs a fix.** The round 2 fix-pass read called it "true here". It is not: the two calls are dependent overall, P(both say up) = 0.29 against 0.5 × 0.5 = 0.25, and lesson 16 `screens[10]` teaches exactly that about two analysts. The line contradicts a later lesson of the same course. Text: "That is one analyst's call. The second call errs independently of the first, whichever way the stock goes, so it adds more."
- `review-2` `items[5].feedback.byKey.added`, "Independent ratios multiply, giving 9." **Worth a fix, lower priority.** It teaches nothing false about the key, but it attaches "independent" to the ratios, which is not a property a number can have, and it is the one line a learner sees after the adding slip. Text: "You added the ratios to get 6. The signals arise independently, battle or no battle, so their ratios multiply to give 9."

If only one of the two is taken, take the first.

## Gates

Run on the worktree after the blind commit, content unchanged. CPython 3 for every script.

- `cd app && node tools/validate.mjs 2>&1 | tail -5`: 0 errors, 4,666 warnings repo-wide. `content/manifest.json` unchanged.
- Number scripts, from the repo root: `fluency-conditional-numbers.py` exit 0 (2,000 checks over 3 families, 0 failures); `problems-conditional-numbers.py` exit 0 (1,177 checks, 0 failures); `conditional-2-perf-numbers.py` exit 0 (0 failures); `conditional-4-perf-numbers.py` exit 0 (0 failures; level 4, run because it matches the name pattern). The first two import `sympy`, which this sandbox lacked; they exit 1 on import until `pip install sympy` (an inbox bullet for that already exists under counting-chance).
- Earlier concepts scripts, run as gates only after the blind commit: round 1 `conditional-L1-concepts.py`, `-L2-`, `-L3-` exit 0 (145, 165, 155 checks); round 2 `conditional-L1-concepts-r2.py`, `-L2-`, `-L3-` exit 0 (706, 831, 714 checks); `conditional-L1-3-fixread-r2.py app/content/courses/conditional` exit 0.
- This round's `conditional-L1-3-concepts-r3.py`: 934 checks pass, 6 fail, exit 1. The six are findings 1 to 6 and stay failing until the content is fixed. Run time under 2 seconds.
- Playthrough with `--local-cdn` (Pyodide 0.27.7 from the scratchpad `pkgs` folder): all 17 lessons, `review-1` to `review-3`, `homework-1` to `homework-3`, `problems-1` to `problems-3` (`--problems`) and `fluency-l7-turning-around` (`--fluency`). Desktop: 27 of 27 ok, "All passed", exit 0, 0 browser relaunches. `--mobile`: 27 of 27 ok, "All passed", exit 0, 0 relaunches.
- No content JSON, engine file, `course.json` or state file was changed.

## Engine

No engine fault found. Numeric grading adds 1e-12 slack to a zero tolerance (`app/js/engine/widgets/_base.js`, `within`), so the exact keys of the fluency set are safe against floating-point noise. One tool item is added to `docs/BACKLOG-INBOX.md` under "Raised later (audit conditional):": a validator advisory for a slip value that equals the key rounded to one place fewer where the question names no places (finding 4; second sighting of the class).

## Fix pass

Fixer: Opus, 11 Nov 2026. Each finding verified before it was applied.

1. **fixed.** Basis: with 70% analysts and a 0.5 prior, P(A up) = P(B up) = 0.5 but P(both up) = 0.5(0.49) + 0.5(0.09) = 0.29, so the calls are dependent overall and independent only given the direction. Auditor's text applied.
2. **fixed.** Basis: the odds form multiplies ratios only when P(E1 and E2 | H) factorises, and the same given not H; independence is a property of events, not of numbers. Auditor's text applied.
3. **fixed.** Basis: both reports are likelier in a downgrade year, so they were dependent overall from the start; what multiplies ratios, and what the new fact breaks, is independence given the truth. Auditor's texts (a), (b), (c) applied. Part 3's key (2 reports) is unchanged: 54/17 × 3 = 9.53 < 19 and × 9 = 28.6 ≥ 19.
4. **fixed.** Option chosen: ask for 4 places; key and slip unchanged. Key recomputed twice: 0.01 × 0.9 + 0.99 × 0.05 = 0.0585, and 1 − (0.001 + 0.9405) = 0.0585. Slip 0.009 + 0.05 = 0.059. Key band [0.0583, 0.0587] and slip band [0.0589, 0.0591] are disjoint, so a right answer to 4 places can no longer be graded as the slip.
5. **fixed differently.** Instead of a caption saying the leaves are not path products, the tree now has a second level ("Book": 3 or more, Fewer) with the regime tails 0.3222 / 0.6778 and 0.0002 / 0.9998 as branch chances, and leaves that are path products: 0.06444, 0.13556, 0.00016, 0.79984 (sum 1 exactly). Leaf values start hidden (`values: false`) so the learner still multiplies, and the explanation shows them. Tails recomputed twice (1 − P(0, 1, 2) and the sum of P(3..10)): 0.32220 and 0.00022. Key 0.0646 ± 0.0001 and every slip value unchanged. Sentences on the screen rechecked against the new leaves: prose now says "The second branches show ..."; hint 2 "The recession path carries most of it" with highlight `r-t`; generic "Multiply along each path that ends in 3 or more, then add."; `avg` "You averaged the two regime tails equally"; explanation highlights `r-t` and `n-t`. The `0.2 × 0.3222 + 0.8 × 0.0002 = 0.0646` lines and "5.6 times" (0.0646 / 0.0115 = 5.62) stay true.
6. **fixed.** Basis: Grimmett and Stirzaker 1.5 define independence of a family by the product rule on every finite subfamily, which is mutual independence. Auditor's sentence added to `l15` `summary.formula.note`.

Script updated: `docs/reports/conditional-L3-concepts-r2.py` tested the old l17 `screens[5]` prose string and leaf keys `r`, `n`. It now checks the new prose string, reads the tails from the second-level branches, and runs the generic tree check on that tree (it no longer exempts it).

Gates: validator 0 errors (4,666 warnings, unchanged; manifest unchanged). Exit 0: `conditional-L1-3-concepts-r3.py` (942 checks), `fluency-conditional-numbers.py`, `problems-conditional-numbers.py`, `conditional-2-perf-numbers.py`, the three round 1 and three round 2 concepts scripts, `conditional-L1-3-fixread-r2.py`. Voice scan 35 on the course folder: 0 and 0. Playthrough with `--local-cdn` of l8, l11, l15, l17, review-2 (`--set`) and problems-2 (`--problems`): all passed, desktop and `--mobile`.
