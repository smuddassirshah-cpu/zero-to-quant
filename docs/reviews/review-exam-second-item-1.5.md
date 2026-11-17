# Exam topic-1.5, second auto item: second-reader findings (session AG)

Scope: the seven new items and two removals of `app/content/exams/topic-1.5.json` named in `docs/reports/exam-second-item-1.5.md` (commit 77f49a05). No browser, no content edits.

Method: author's script run (74 checks, bad 0, exit 0). Own recompute in `docs/reports/exam-second-item-1.5-numbers-read.py` (142 checks, exit 0, 4 `FINDING` lines, all listed below). Other methods than the author's: enumeration over Fractions, a Venn count on 100 clients, $P(HH)/P(H)$ for the coin, a Gauss-Jordan solve of $(I - Q)t = 1$ and seeded simulations for the walk, `erfc` for the normal tail. Reuse read with a text search over the five topic courses and every exam, plus `fresh-check.mjs --file` (0 hits; 13 advisories, none on a new item).

Gates: validator 0 errors (one old O2 warning on `items[17]`, none on new items); voice scan at 35 prints nothing for the file; `grade-all.mjs --file` 35 widgets, 0 failures.

## Verdict

- Numbers: every key, `wrong` value, option value and printed number of the seven items recomputes. Bands take the printed and the exact value, refuse every `wrong` value, and no key sits on a rounding tie. No wrong number found.
- Pairs: 12 pairs and 25 triples before the pass, the same list as the report. Each of the 12 skills now has two auto items. No skill of the exam is below two auto items. 35 items, 70 minutes (60 × 35 / 30).
- Two-skill items, strict test (unanswerable without both): **2 pass** (`e-neither-market`, `e-fill-times`), **2 fail** (`e-ticket-pair`, `e-coin-again`), **1 weak** (`e-floor-walk`).
- Reuse: 6 clean, **1 reuse** (`e-coin-again` against `conditional/l22-gamblers-fallacy` screen 6).
- Removals: both counts hold. `dl-discrete` keeps `e-winning-days` (3) and `e-order-split` (3). `dl-continuous` keeps `e-beta-pair` (4) and `e-default-pair` (5), see finding 5.

Format: `N. file | JSON path | severity | problem | evidence | exact fix`. Severity: error = wrong number or wrong grading; warning = a tag the item does not enforce, reuse, or a teaching issue; note = small.

## Findings

File for all rows: `app/content/exams/topic-1.5.json`.

1. topic-1.5.json | `items[2]` (`e-ticket-pair`), `skills` | warning (misleading) | The item carries `cc-sample` and `cc-count` but needs neither count. | Five tickets give ten pairs. A learner lists them and ticks four, which is what `e-small-total` asks under `cc-sample` alone. The draw-by-draw route $\tfrac35 \cdot \tfrac24 + \tfrac25 \cdot \tfrac14 = \tfrac25$ uses neither skill. | Make the space too large to list and ask for the counts, so both the space and the count are graded. Replace the item body with:
   - `prose`: "A hat holds 15 tickets numbered 1 to 15. You draw two different tickets together, so their order does not matter."
   - `question`: "Fill in both counts."
   - `widget`: `{"kind": "table", "columns": ["Quantity", "Count"], "rows": [["(a) Outcomes in the sample space", {"edit": true, "answer": 105, "tol": {"abs": 0}}], ["(b) Outcomes with an even sum", {"edit": true, "answer": 49, "tol": {"abs": 0}}]]}`
   - `feedback.correct`: "Each outcome is an unordered pair, and 49 of the 105 have an even sum."
   - `feedback.generic`: "An outcome is a pair of tickets. An even sum needs two odd tickets or two even ones."
   - `feedback.byKey.r0c1`: "Count unordered pairs: $\\tfrac{15 \\times 14}{2}$. Ordered draws give 210, twice too many."
   - `feedback.byKey.r1c1`: "There are 8 odd tickets and 7 even ones. Count the pairs inside each group, then add."
   - `explain.text`: "The sample space holds $\\tbinom{15}{2} = 105$ pairs. Two odd tickets give $\\tbinom{8}{2} = 28$ pairs and two even ones give $\\tbinom{7}{2} = 21$. So 49 outcomes have an even sum."
   - Recomputed: 105 pairs, 28 + 21 = 49, ordered 210, 8 odd and 7 even (reader script, "fix 1"). No "numbered 1 to 15" elsewhere in the topic courses or exams.

2. topic-1.5.json | `items[10]` (`e-coin-again`), `skills` and `widget` | warning (misleading) | The item carries `bayes`, but the key needs no posterior. | $P(H_2 \mid H_1) = \tfrac{P(H_1 H_2)}{P(H_1)} = \tfrac{0.5 \cdot 0.25 + 0.5 \cdot 0.64}{0.65} = \tfrac{89}{130}$. That is total probability twice and one division, all `cond-mult`. | Grade the posterior as its own cell, as `e-fill-times` does for its two skills. Use the table in finding 3, which also clears the reuse.

3. topic-1.5.json | `items[10]` (`e-coin-again`), `prose` | warning (reuse) | Story and opening sentence shared with a lesson of the same course. | Exam: "A pocket holds two coins. One is fair, and the other lands heads with chance 0.8. You take one at random and toss it, and it lands heads." Lesson `courses/conditional/l22-gamblers-fallacy.json` `screens[6]`: "A box holds two coins. One is fair. The other lands tails with chance $\tfrac{3}{4}$. You pick one at random and toss it five times: five tails." Its explanation also gives the next-toss chance ("The next toss is then a tail with chance about 0.72"), so the exam task is the lesson's last line with new numbers. | Replace the item body with (numbers unchanged, so the author's checks on 0.65, 8/13 and 89/130 stay):
   - `title`: "The second call"
   - `prose`: "A new analyst is careful or careless, each with chance 0.5. A careful analyst’s call is right with chance 0.8 and a careless one’s with chance 0.5, independently from call to call. Her first call is right."
   - `question`: "Fill in both chances. Give decimals to 4 places."
   - `widget`: `{"kind": "table", "columns": ["Quantity", "Value"], "rows": [["(a) She is careful", {"edit": true, "answer": 0.6154, "tol": {"abs": 0.0005}}], ["(b) Her second call is right", {"edit": true, "answer": 0.6846, "tol": {"abs": 0.0005}}]]}`
   - `feedback.correct`: "Update on the first call, then average over the two kinds of analyst."
   - `feedback.generic`: "Find the chance of a right first call over both kinds. Then update, and use total probability again."
   - `feedback.byKey.r0c1`: "Divide the careful route, $0.5 \\times 0.8$, by the chance of a right first call, 0.65."
   - `feedback.byKey.r1c1`: "Weight 0.8 and 0.5 by the updated chances, $\\tfrac{8}{13}$ and $\\tfrac{5}{13}$, not by a half each."
   - `explain.text`: "The first call is right with chance $0.5 \\times 0.8 + 0.5 \\times 0.5 = 0.65$, so she is careful with chance $\\tfrac{0.4}{0.65} = \\tfrac{8}{13} \\approx 0.6154$. The second call is right with chance $\\tfrac{8}{13} \\times 0.8 + \\tfrac{5}{13} \\times 0.5 = \\tfrac{89}{130} \\approx 0.6846$."
   - Recomputed: 8/13 = 0.61538, 89/130 = 0.68462, cells 0.069 apart, no tie (reader script, "fix 2"). The fixer runs `fresh-check.mjs --file` on the new story; a search for "careless" and "careful analyst" finds nothing in the topic courses or exams. Note 0.6154 is also the key of `conditional/problems-1` `items[3]` from other inputs, a shared value and not a shared number set.

4. topic-1.5.json | `items[28]` (`e-floor-walk`), `skills`, `canvas` | note (misleading, weak) | Neither tag is strictly forced. | (i) With the chain drawn, three first-step equations give 9 with no walk knowledge. (ii) Mirroring the floor gives a fair walk from 3 on 0 to 6, and the duration formula $i(N - i)$ printed in `e-ruin-length` feedback gives $3 \times 3 = 9$ with no equations. Route (ii) is not taught in `markov` (level 3 reflects paths, not floors), so it is not a realistic way round. The course itself tags walk durations found by first-step with both skills (`homework-3` `h-duration-expr`, `h-roulette`), so the tagging follows the course. | Optional, to make the learner build the walk before solving it: delete the `canvas` key and the prose sentence " The chain is drawn below.". Key, `wrong` values and feedback are unchanged (E0 = 9, E1 = 8, E2 = 5; slips 3, 6, 8). This also retires the 440 px legibility bullet in the inbox. Otherwise leave as is.

5. topic-1.5.json | removed `e-uniform` (`dl-continuous`, difficulty 3) | note (continuity) | The count rule holds, but no plain continuous item is left. | `dl-continuous` is essential to `limits-thm` L2 and L4. Its two auto items are now `e-beta-pair` (difficulty 4, order statistic and Beta update) and `e-default-pair` (difficulty 5, four cells on a joint density), both level 4 material. The floor itself is no harder than before (one of two, against two of three). The report kept `e-two-days` for this same reason (`mc-chains`, "no basic test"). | Main session's call. To restore: put `e-uniform` back as it stood at 77f49a05^, in its old place; the exam then holds 36 items, the validator's cap, and stays at 70 minutes (60 × 36 / 30 = 72, rounded to 5). No change needed if the level 4 coverage is accepted.

6. topic-1.5.json | `items[24]` (`e-fill-times`), `prose` | note (continuity) | Actor and plan shared with a problem-set item on the same two skills. | Exam: "A broker times 64 independent order fills." `courses/limits-thm/problems-3.json` `items[2]` (`p-rejected-orders`, `dl-lln`, `dl-clt`): "A broker's count $X$ of rejected orders on a day is never negative", then Chebyshev and the normal on $\bar X_n$. The tasks differ (a chance at fixed $n$ against the least $n$) and no number is shared, so the ruling is clean. | Optional: `prose` first sentence to "An exchange times 64 independent order fills."

7. topic-1.5.json | `items[4]` (`e-neither-market`), `difficulty` | note | Rated 3 for two one-line steps. | $0.45 + 0.30 - 0.12 = 0.63$, then $1 - 0.63$. `e-total-four` and `e-multiple-four` are rated 2 for the same amount of work. | Optional: `"difficulty": 2`. The mix becomes 8 / 15 / 9 / 3.

## Skill test per two-skill item

| item | skills | without the first | without the second | ruling |
|---|---|---|---|---|
| `e-ticket-pair` | cc-sample, cc-count | draw-by-draw product gives 0.4 | ten pairs listed by hand | fail (1) |
| `e-neither-market` | cc-rules, cc-symmetry | no route: the union needs the overlap taken off once | no route: "neither" is only reachable as $1 - 0.63$ | pass |
| `e-coin-again` | bayes, cond-mult | $P(HH)/P(H)$ gives 0.6846 | no route: both steps weigh the two coins | fail (2) |
| `e-fill-times` | dl-lln, dl-clt | cell (a) is graded | cell (b) is graded; the table needs every cell | pass |
| `e-floor-walk` | mc-walks, mc-firststep | the drawn chain can be solved blind | mirror route, not taught | weak (4) |

Single-skill items: `e-multiple-four` tests `cond-shrink` (seven numbers left, two of them multiples of 3) and `e-distance-three` tests `rv-dist` (collecting faces into a pmf). Both sound.

## Reuse per item

| item | closest exam item | closest lesson screen | closest review, homework, problem set | ruling |
|---|---|---|---|---|
| `e-ticket-pair` | `e-small-total`: "Two fair dice are rolled. The grid shows every outcome with its total." | `counting-chance/l7-replacement` s0: "A bag holds 4 tokens numbered 1 to 4. You draw one, write its number down and put it back." (ordered, with replacement) | `counting-chance/review-1` i1 (faces 4 apart on two dice); `mock-oa-trader-3` b14 "Ten cards are numbered 1 to 10. Two are dealt. The larger number is 8." | clean |
| `e-neither-market` | `e-at-least-one-six`: "Four fair dice are rolled." | `counting-chance/l3-events-as-sets` s8: "$11 + 8 - 5 = 14$ ... The other 6 days are $A^c \cap B^c$." | `counting-chance/homework-3` i7 ($P(A) = 0.6$, $P(B) = 0.5$, overlap 0.05). Outside the topic: `counting/problems-2` i1, "$45 + 38 - 20 = 63$ members do at least one ... how many do neither?" shares 45 and 63 by chance | clean |
| `e-multiple-four` | `e-total-four`: "Two fair dice are rolled. You learn the total is 4." | `conditional/l3-shrinking` s5 (total of 10 given at least one 5) | `conditional/review-1` i6 (dice total); `counting-chance/homework-3` i0 counts multiples of 3, 5 or 7 to 1,000 | clean |
| `e-coin-again` | `e-screening` (1%, 95%, 10%) | `conditional/l22-gamblers-fallacy` s6: "A box holds two coins. One is fair. The other lands tails with chance $\tfrac34$. You pick one at random and toss it five times" | `conditional/review-2` i6 (two-headed coin, flipped twice) | **reuse** (3) |
| `e-distance-three` | `e-pmf`: "$X$ is the number of heads in three tosses of a fair coin." | `random-vars/l4-transforming` s3: "A volatility trader cares only about the size of the move, $Y = \lvert X \rvert$." (table on a given pmf) | `random-vars/problems-1` i2: "A straddle pays $Y = \lvert X \rvert$ pounds" (find $c$) | clean: same idea, new variable, die and form |
| `e-fill-times` | `e-chebyshev` (mean 50, sd 5, one $X$); `e-clt-pnl` (total of 100 days) | `limits-thm/l10-bound-that-holds` s7 ($P(\lvert X \rvert \ge 2)$ against Chebyshev at $k = 2$) | `limits-thm/problems-3` i2 `p-rejected-orders`; `review-3` i2 (Markov against Chebyshev, 0.04) | clean, see 6 |
| `e-floor-walk` | `e-ruin-length`: "You start with £2 and bet £1 on each toss of a fair coin." | `markov/l17-fair-bets` s0 (fair bets to a target); no floor walk in the course | `markov/homework-3` `h-duration-expr` (£0 or £20) | clean |

## Bands, ties, units, sources

- Numeric items state their form ("Give a decimal", "to 4 places"); `e-floor-walk` asks for minutes and takes "Exactly 9".
- Narrowest gaps: `e-coin-again` key 0.6846 against `no-update` 0.65 (0.035, tolerances 0.0005); `e-fill-times` cells 0.16 and 0.0124.
- $\Phi(2.5) = 0.99379$; the printed 0.9938 gives 0.0124 and the exact tail 0.012419 is inside the band. The value is printed in the prose, as in `e-clt-pnl`.
- No percentage answer, so no "%" unit is due. No money answer.
- Voice on the new items: no exclamation mark, no em-dash, longest sentence under 35 words, explanations of at most three sentences.

Note for the main session: commit 77f49a05 carries a `Co-Authored-By: Claude Opus 5.5` trailer, not the one in the brief.
