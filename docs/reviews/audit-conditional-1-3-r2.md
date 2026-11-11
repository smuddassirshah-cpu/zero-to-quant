# Concept audit, round 2: conditional levels 1 to 3

Auditor: blind Fable reader, round 2. Scope: `app/content/courses/conditional/` files `l1` to `l17`, `review-1` to `review-3`, `homework-1` to `homework-3` (with the performance task `h-two-filters`), `problems-1` to `problems-3` and `fluency-l7-turning-around`. Levels 4 and 5 are out of scope. Topic 1.5 is Stage 1, so the ledger has full depth.

Blind rule: the ledger, the findings below and the three concepts scripts were written and committed (commit `74967a24`) before any earlier audit, review, ledger, concepts script, author report, git history or diff of the course folder was opened. The overlap table, the gate results and the inbox bullet were added afterwards.

Ledger: `docs/reports/audit-conditional-1-3-r2-ledger.md` (459 rows: correct 443, wrong 3, imprecise 13, misleading 0, unverified 0).

Scripts, run from the repo root, with the shared helper `docs/reports/conditional_concepts_r2_lib.py`:

- `docs/reports/conditional-L1-concepts-r2.py`: 706 checks, 0 failed, exit 0.
- `docs/reports/conditional-L2-concepts-r2.py`: 829 checks, 6 failed, exit 1. The six failing checks are findings 1 and 2 and stay failing until the content is fixed.
- `docs/reports/conditional-L3-concepts-r2.py`: 714 checks, 0 failed, exit 0.

They recompute every graded key, every slip value and every stated number by exact enumeration with fractions or by a closed form. They confirm the main results by seeded Monte Carlo, check every tree canvas (branches add to 1, each leaf is the product along its path), and execute both Python solutions against their hidden tests (the starters fail).

## Findings

Pattern: `N. file | JSON path | severity | serious or minor | problem | evidence and basis | exact fix`.

1. `l12-many-hypotheses.json` | `screens[3].explain.text` | wrong | serious | "The 6-sided die gained and the 8-sided die lost a little." The 8-sided die gained. | Its chance went from 1/3 to 3/7 (0.333 to 0.429); the bars on the same screen show `b8` 0.3333 and `a8` 0.4286. A hypothesis gains exactly when its likelihood beats the total chance of the evidence: 1/8 against P(5) = 7/72. Both surviving dice gain because the 4-sided die's 1/3 is shared out. The sentence teaches that the less favoured hypothesis must lose, which is false whenever a third hypothesis is ruled out. Basis: exact posterior and Monte Carlo 0.429 in the L2 script (check stays failing); Blitzstein and Hwang 2.3. | `explain.text`: "Normalised, the chances are 0, $\tfrac{4}{7}$ and $\tfrac{3}{7}$, which add to 1. Both dice gained, because the 4-sided die's $\tfrac{1}{3}$ was shared out. The 6-sided die gained more: it explains a 5 better."

2. `l11-updating-twice.json` | `screens[8].canvas.params.leaves`, `screens[8].widget.wrong` (`joint`), `screens[8].feedback.byKey.joint`, `screens[8].explain.text` | wrong | minor | The tree's leaves are 0.49, 0.51, 0.09 and 0.91. Those are the second-stage branch chances again, not path chances, and they add to 2. The slip feedback then says 0.49 "is up with both calls up, out of everything". | The path chances are 0.5 × 0.49 = 0.245, 0.255, 0.045 and 0.455. P(up and both say up) is 0.245; 0.49 is P(both say up given up). Every other tree in the three levels states path products as leaves (generic check `trees()`), and l5 teaches "the leaves of a tree add to 1" as a check, which this tree fails once the explanation shows its values. The key 49/58 is right, and the ratio 0.49/0.58 is right only because the prior is 50%. A learner who enters the true joint, 0.245, gets no targeted feedback. Basis: multiplication rule; L2 script (five checks stay failing). | `canvas.params.leaves`: `{"u-b": "0.245", "u-n": "0.255", "d-b": "0.045", "d-n": "0.455"}`. `widget.wrong`: change `joint` to `{"id": "joint", "value": 0.245, "tol": {"abs": 0.001}}` and add `{"id": "likelihood", "value": 0.49, "tol": {"abs": 0.001}}`. `feedback.byKey.joint`: "That is up with both calls up, out of everything. Divide by every way both say up, 0.29." `feedback.byKey.likelihood`: "That is the chance both say up when the stock goes up. Weigh it against 0.09, the chance when it goes down." `explain.text`: "Each call has likelihood ratio $\tfrac{0.7}{0.3} = \tfrac{7}{3}$. Two calls: odds $1 \times \tfrac{49}{9}$, so $p = \tfrac{49}{58} \approx 0.845$. The tree gives the same: $0.245 / 0.29$."

3. `l16-conditional-independence.json` | `quiz[2].question`, `quiz[2].widget.options` (`same`) | imprecise | minor | "The fund lost money, and you learn there was a crash. What happens to the chance of a bad call?" The key "It falls" is right only against the chance just after the loss. Against the chance before any news the answer is "unchanged", which is a listed wrong option. | With a loss exactly when there is a bad call or a crash, P(bad given loss and crash) = P(bad given crash) = P(bad), by the independence the item states. So the chance falls from P(bad given loss) and equals the prior (L3 script, nine parameter pairs). The item does not say which baseline it means; the lesson's own screen 8 does ("The alert fired. Then you learn the market did drop."). Basis: explaining away, Pearl (1988) ch. 2. | `question`: "The fund lost money. Then you learn there was a crash. Compared with just after the loss, what happens to the chance of a bad call?" `widget.options` (`same`) `why`: "Before any news they are independent. Given the loss, learning one cause changes the chance of the other."

4. `l1-what-changes.json` | `screens[6].explain.text` | imprecise | minor | "News changes a chance only when it removes outcomes unevenly." Read with the sentence before it ("removed one even face and one odd face"), this says that removing equal numbers from A and from not-A leaves the chance alone. That holds only when the chance was 1/2. | Counter-example on the same die: A = {1, 2}, news removes the faces 1 and 6 (one in A, one not). The chance moves from 1/3 to 1/4 (L1 script). The true condition: the share of A among the removed outcomes equals the share of A before. | `explain.text`: "You counted 2 and 4 among the four faces left: $\tfrac{2}{4} = \tfrac{1}{2}$. The faces removed, 5 and 6, were half even, the same share as the whole die, so the chance did not move. News changes a chance only when the share among the outcomes it removes is different."

5. `l11-updating-twice.json`, `review-2.json`, `homework-2.json` | l11 `screens[8].prose`, l11 `quiz[0].prose`, l11 `quiz[1].prose`, review-2 `items[5].prose`, homework-2 `items[2].prose` | imprecise | minor | The evidence is called plainly "independent" ("they work independently", "a second, independent report", "a later, independent rumour", "two independent news signals", "B, run independently"). The ratios multiply only when the pieces are independent given the hypothesis and given its opposite. Plain independence is a different property, and for two informative signals about one hypothesis it is in general false. | l11 `screens[0]`, `screens[7]` and the formula note state the condition in full, and l16 `screens[10]` shows two such analysts are dependent overall (0.5833 against 0.45) yet independent given the truth. After level 3 a learner who rereads these five items with the level 3 definition has the wrong property. All five keys are right under the intended reading (L2 script). Basis: Blitzstein and Hwang 2.5 (conditional independence) and 2.6. | l11 `screens[8].prose`: "Two analysts call a stock's direction. Each is right 70% of the time, whichever way it goes. Whichever way it goes, one analyst's mistake tells you nothing about the other's. You start at 50%. Both say up." l11 `quiz[0].prose`: "You give a takeover a 20% chance. One report has likelihood ratio 2 and a second has likelihood ratio 3. Takeover or not, the two reports err independently." l11 `quiz[1].prose`: "You give a stock a 30% chance of a dividend cut. One rumour has likelihood ratio 4. A later rumour has likelihood ratio $\tfrac{1}{4}$. Cut or no cut, the two rumours arise independently." review-2 `items[5].prose`: "You start at 10% that a stock is in a takeover battle. Two news signals arrive, each with likelihood ratio 3. Battle or no battle, the two signals arise independently." homework-2 `items[2].prose`: "A condition has prior 5%. Test A catches 95% of cases and false-alarms on 10% of healthy people. Test B catches 80% and false-alarms on 2%. A is positive and B is negative. With or without the condition, the two tests err independently."

6. `l13-knowing-nothing.json` | `quiz[1].feedback.byKey.disjoint` | imprecise | minor | "Independent events can, and usually do, happen together." For independent events with positive chances the joint chance is always positive, so "usually" understates it. Read as a frequency, "usually happen together" is false here: they do so with chance 0.2. | P(A∩B) = P(A)P(B) = 0.2 > 0 (L3 script). The only independent events that cannot happen together are those where one has chance 0 (l15 `screens[8]`). | `feedback.byKey.disjoint`: "You treated independent as disjoint. Independent events with positive chances can always happen together: here with chance 0.2."

7. `l15-pairwise.json` | `summary.ideas[2]`, `screens[8].feedback.correct` | imprecise | minor | "Mutual independence implies pairwise independence, never the other way round." The implication fails in general, but pairwise independent events are often mutually independent as well (three separate coins). "Never" reads as a rule that they cannot be. | The lesson's own definition makes mutual a stronger property, not an exclusive one; `summary.formula.note` says it correctly ("Neither part implies the other: check both"). Basis: Blitzstein and Hwang 2.5; Grimmett and Stirzaker 1.5. | `summary.ideas[2]`: "Mutual independence implies pairwise independence, but pairwise does not imply mutual. Joint risk can hide from every pairwise check." `screens[8].feedback.correct`: "Mutual gives pairwise, but pairwise does not give mutual; a chance-0 event is independent of everything."

8. `l13-knowing-nothing.json` | `screens[9].prose` | imprecise | minor | "Many models assume the pairs are independent." The screen then tests whether today's sign is independent of yesterday's inside a pair. The 20 pairs themselves overlap (each day is "today" in one pair and "yesterday" in the next), so the pairs cannot be the independent objects. | The 20 rows chain as consecutive days (L3 script), and screen 10 states the claim correctly ("Independence of the signs"). | `screens[9].prose`: "A dataset of 21 daily returns gives 20 pairs of signs: yesterday's and today's. Many models assume today's sign is independent of yesterday's. Before trusting that, tally the pairs."

9. `l12-many-hypotheses.json` | `screens[5].prose` | imprecise | minor | "The second roll, a 3, is the 4-sided die's best roll." Every face of a fair 4-sided die has chance 1/4, so it has no best roll. The intended point is the comparison across dice. | P(3 given 4-sided) = 1/4 against 1/6 and 1/8, and the same holds for a 1, 2 or 4. | `screens[5].prose`: "The second roll, a 3, suits the 4-sided die best. It shows a 3 one time in 4, more often than the other dice do."

10. `homework-1.json` | `items[0].widget.options[3].why` | imprecise | minor | "Only six totals reach 10." Six outcomes have a total of 10 or more; the totals that do are three (10, 11 and 12). | Enumeration: (4, 6), (5, 5), (6, 4), (5, 6), (6, 5), (6, 6) (L1 script). | `why`: "You divided by all 36 outcomes. Only six outcomes have a total of 10 or more."

Counts: 10 findings. wrong 2 (1 serious, 1 minor), imprecise 8 (all minor), misleading 0. No graded key is wrong. One graded key is right under one of two natural readings (finding 3).

## Noted, not conceptual

- `l17-correlated-defaults.json` `screens[5]`: the tree's two leaves are conditional tails (0.3222, 0.0002), not path chances. The prose says so ("The leaves show P(3 or more defaults) in each regime"), so it is not a finding; the check is exempted by declaration in the L3 script. It is the same use of `leaves` that finding 2 is about, there without the declaration.
- `homework-1.json` `items[4].explain.text` cites "Item 8" by position. It is right today (the eighth item is `h-order-three`), and it breaks if the set is reordered.

## What was checked with particular care and held

- P(A given B) against P(B given A): l7 throughout, l3 `quiz[0]` (reversed slip 2/11), homework-1 `items[3]`, problems-1 item 1 parts 2 and 3, review-2 `items[0]`, the fluency set's `inverse` slips. Every "inverse" slip value is the true reversed conditional.
- Conditions. P(B) > 0: l3 `summary.formula.note`, l7 `screens[8]` ("which is not 0"), l13 `screens[7]`, l16 `screens[9]`, homework-1 `items[7]` and `items[11]`, homework-2 `items[6]` and the performance task all state the condition they use. Partition: l6 `screens[7]` ("cover every case without overlap") and l12 `screens[7]` ("cannot overlap and whose priors add to 1") state exclusive and exhaustive. Independent trials: l14 `summary.formula.note` ("needs independence and the same p").
- Independence against conditional independence: l16 and l17 separate them correctly and in both directions (shared cause, shared effect). The only slips are the plain "independent" wordings of finding 5, all in level 2.
- Odds against probability: l10 is consistent (odds in favour, p/(1 − p)); "3 to 1 on" is the right UK betting term for odds of 3; every `probs` slip is the probability multiplied by the ratio.
- Sampling protocol. Where the answer depends on how the news was obtained, the item says so: l3 `screens[3]` and `screens[7]`, review-1 `items[3]`, homework-1 `items[2]` and `items[6]`, problems-1 item 0 part 2 all have the learner ask one yes or no question. l1 and l3 `screens[2]` use a plain report ("they tell you the result is even", "tells you the first die shows 5"), read as the answer to a fixed question; l3 then contrasts the two.
- Summaries and `trap` lines against the lesson bodies: all 17 agree with their lessons, except the "never the other way round" line of finding 7.
- Empirical and finance claims: adverse selection on limit orders (l5), false discoveries in backtests (l8, l14), natural frequencies (l9), Cromwell's rule (l12), explaining away (l16), correlated defaults and senior tranches in 2008 (l17). Each is stated at a level the named sources support, and the sample claims in l13 and homework-3 are hedged to the sample.
- "Always" claims that needed proof: a recession mix with the same mean never lowers P(3 or more) or P(no defaults) (l17 `screens[1]`, `quiz[0]`); pairwise independence leaves P(all three) anywhere in [0, 1/4] (l15 `screens[6]`); the shared-factor excess q(1 − q)(p_b − p_g)² (homework-3). All hold.

## Overlap with earlier reads

Opened only after commit `74967a24`: `docs/reviews/audit-conditional-1-3.md` (audit round 1 with its fix pass, fix-pass read and follow-up), `docs/reports/audit-conditional-1-3-ledger.md` (searched for the rows of this round's findings), `docs/reviews/review-1.5.md` (conditional section and fix pass) and `docs/reviews/review-problems-1.5-a.md` (conditional `problems-1` to `problems-3`). The round 1 concepts scripts and the author reports were not used. `git log -S` was run on the two `wrong` sentences only.

Conceptual findings, levels 1 to 3:

| | Count | Which |
|---|---|---|
| Found by this audit only | 9 | Findings 1 to 4 and 6 to 10. Both `wrong` findings are here |
| Found by both | 1 | Finding 5 is the class of round 1 finding 11 (evidence called plainly "independent" where independence given the hypothesis is needed). Round 1 named and fixed two places (l10 `screens[8]`, l11 `screens[0]`). The five places of finding 5 were not named and still read that way |
| Found by audit round 1 only | 22 | Round 1 findings 1 to 10 and 12 to 23. All were fixed before this read, so a blind read of the present text could not find them again |
| Found by the round 1 fix-pass read only | 2 | homework-2 `items[4].explain.text` and l5 `screens[10].prose`; both fixed |
| Found by the earlier reviews only | 4 | As counted by round 1: l7 "agree only when P(A) = P(B)" (also round 1 finding 13 at a third place), l7 "hit rate", l12 `screens[6]` prose, problems-1 `p-order-router`. All fixed |

None of the 28 earlier findings has come back. Each of those places reads `correct` in the round 2 ledger: the l3 and l16 `trap` lines (round 1's two `wrong`), the stated yes or no questions, l12 `screens[7]` ("cannot overlap and whose priors add to 1"), the l8 "much rarer than the false-positive rate" lines, l15 `screens[6]` ("only a range"), homework-2 `items[4]` and `items[6]`, l5 `screens[10]`, l17 `screens[6]` and `screens[10]`.

`wrong` verdicts of this audit: 2.

- Finding 1 (l12 `screens[3].explain.text`, the 8-sided die "lost a little"): found by no earlier read. Not fix-pass text: `git log -S` puts the sentence in commit `4181221a` (20 October 2026); the round 1 fix pass (`c4ec159e`) changed only `screens[7].prose` in that file. The round 1 ledger has this row as `correct` (its line 1970).
- Finding 2 (l11 `screens[8]` leaves and the `joint` feedback): found by no earlier read. Not fix-pass text: both strings date from commit `43e79a98` (20 October 2026); the fix pass changed `screens[0].prose`, `screens[9].explain.text` and `summary.ideas[2]` in that file. The round 1 ledger has `screens[8].feedback.byKey.joint` as `correct` (its line 1886, basis "slip reproduces its value"). The value 0.49 does reproduce; the quantity it is named as does not.

Convergence: two new `wrong` in three levels is over the limit of one, so by the rule in `docs/briefs/concept-audit.md` the course does not close on this round. It needs a fix pass and another blind read.

Where the reads touch:

- Finding 3 is in l16 `quiz[2]`. Round 1 finding 19 reworded the last sentence of that item's explanation and its ledger marks the key and the `same` option's `why` as `correct`; the unstated baseline was not raised.
- Finding 4 (l1 `screens[6].explain.text`) and finding 6 are on rows the round 1 ledger marks `correct`.
- Finding 7: round 1 finding 18 reworded l15 `summary.trap`; the "never the other way round" line beside it in `summary.ideas[2]` was not raised.
- Finding 2's canvas would be caught by a validator rule (inbox bullet below). l17 `screens[5]` uses leaves the same way with a declaration in the prose.
- Seen by the round 1 fix-pass read and not raised here: l8 `objectives[0]`, "See how a rare condition makes most positive tests false", is looser than the corrected screens. It is still in the text. It is an aim line and the lesson's own case bears it out, so this audit read it as `correct`.
- review-1.5 corrected homework-1 "Item 7" to "Item 8"; the reference is still by position (noted above).

Miss rate of a single read, on this evidence: after two reviews, one audit and its fix-pass read, a fresh blind read still found 10 findings in 17 lessons and 10 sets. Two are `wrong` (one serious), neither a graded key. Round 1's ledger had 3,284 rows and passed both sentences with a basis written for the key, not for the sentence.

## Gates

Run on the worktree at commit `74967a24`, content unchanged.

- `node tools/validate.mjs 2>&1 | tail -5` (from `app/`): 0 errors, 4,667 warnings repo-wide. `content/manifest.json` was not changed by the run.
- Number scripts, from the repo root: `conditional-2-perf-numbers.py` 0 failures, exit 0; `fluency-conditional-numbers.py` 2,000 checks, 0 failures, exit 0; `problems-conditional-numbers.py` 1,177 checks, 0 failures, exit 0.
- Round 2 concepts scripts: L1 706 checks, exit 0. L2 829 checks, 6 failed, exit 1 (findings 1 and 2; they stay failing until the content is fixed). L3 714 checks, exit 0.
- Playthrough with `--local-cdn` (Pyodide 0.27.7 from the scratchpad `pkgs` folder), desktop and `--mobile`: all 17 lessons, `review-1` to `review-3`, `homework-1` to `homework-3`, `problems-1` to `problems-3` (`--problems`) and `fluency-l7-turning-around` (`--fluency`). 54 file runs in 8 invocations, every one "All passed", exit 0, 0 browser relaunches.
- `VOICE_BASE=app/content/courses/conditional python3 docs/reviews/voice-scan.py 35`: 15,592 sentences, 0 over 35 words, 0 explanations over three sentences. The fix texts above were written to the same limits.
- No content JSON, engine file, `course.json` or state file was changed.

## Engine

No engine fault found. One tool item is added to `docs/BACKLOG-INBOX.md` under the existing line "Raised later (audit conditional):": a validator warning for a `tree` canvas whose stated leaves are not its path products, with an opt-out for declared leaves (finding 2; a working check is `trees()` in `docs/reports/conditional_concepts_r2_lib.py`).

## Fix pass

Fixer: Opus, round 2. Each basis below was worked out before the auditor's evidence column was used.

1. fixed. Basis: posterior ∝ prior × likelihood; products 0, 1/18, 1/24 over 7/72 give 0, 4/7, 3/7, and 3/7 > 1/3, so the 8-sided die gained (a hypothesis gains exactly when its likelihood beats P(E) = 7/72; 1/8 > 7/72). Text now says both dice gained because the 4-sided die's share was shared out, the 6-sided more.
2. fixed. Basis: multiplication rule, leaf = 0.5 × branch: 0.245, 0.255, 0.045, 0.455 (sum 1); 0.245 + 0.045 = 0.29 and 0.245/0.29 = 49/58. Graded slips and canvas changed: tree leaves; slip `joint` 0.49 → 0.245 with feedback naming 0.29; new slip `likelihood` 0.49 with its own feedback; explain's tree route now 0.245 / 0.29. Key 49/58, hints and highlight unchanged and still consistent. L2 r2 script: the `A(... screens[8])` call now checks joint = 0.245 and likelihood = 0.49, and the finding 2 check now compares the actual `joint` slip value (as written it tested two constants and could never pass with "out of everything" in the text); it fails on the old content.
3. fixed. Basis: loss = bad ∪ crash, so P(bad | loss, crash) = P(bad | crash) = P(bad) < P(bad)/P(loss) = P(bad | loss). The question now fixes the baseline as just after the loss; the `same` why says before any news; the explanation now says the chance falls back to where it was before any news.
4. fixed. Basis: P(A | B) = P(A) iff A's share of the removed outcomes equals its share of the whole (for 0 < P(B) < 1); counter-example A = {1, 2}, remove {1, 6}: 1/3 → 1/4. Second sentence shortened to "half even, like the whole die, so the chance held" to keep it under 20 words.
5. fixed. Basis: Blitzstein and Hwang 2.5 and 2.6; ratios multiply when P(E1 ∩ E2 | H) = P(E1 | H)P(E2 | H) and likewise given ¬H. All five places now state independence given each hypothesis. Grep of in-scope files for the same class found and fixed: homework-2 `items[5].prose` ("an independent out-of-sample test"), l11 `summary.ideas[1]`, `objectives[1]` and `objectives[2]`, `quiz[2].feedback.correct`, `screens[9].widget.options[3].why` (now "adds weight only when the second call tells you something new", which is the general condition). Left as shorthand where the same item already states the conditional form: l11 `screens[8].feedback.byKey.one`, `quiz[2].widget.options[1].text`, review-2 `items[5].feedback.byKey.added`, homework-2 `items[7]` option, problems-2 item 1 parts 2 to 4. Plain independence of events with no hypothesis (l3, l14, review-3) is correct as written.
6. fixed. Basis: P(A ∩ B) = P(A)P(B) = 0.4 × 0.5 = 0.2 > 0 whenever both chances are positive.
7. fixed. Basis: three tosses of a fair coin give events that are mutually, hence pairwise, independent, so "never" is false as a rule; the two-coin example shows pairwise does not imply mutual. Both lines now say "pairwise does not imply (give) mutual".
8. fixed. Basis: row i's "Today" equals row i + 1's "Yesterday" for all 19 joins, so the pairs overlap; the testable claim is today's sign independent of yesterday's.
9. fixed. Basis: a fair 4-sided die gives each face 1/4; 1/4 > 1/6 > 1/8 for a 3, so the comparison is across dice.
10. fixed. Basis: enumeration of totals 10 to 12 gives six outcomes but three totals.

Counts: 10 fixed, 0 fixed differently, 0 disputed.

Gates (worktree, after the fixes):

- `node tools/validate.mjs` (from `app/`): 0 errors, 4,667 warnings; `content/manifest.json` unchanged.
- From the repo root, all exit 0: `conditional-L1-concepts-r2.py` (706 checks), `conditional-L2-concepts-r2.py` (831 checks, 0 failed), `conditional-L3-concepts-r2.py` (714), `conditional-L1-concepts.py`, `conditional-L2-concepts.py`, `conditional-L3-concepts.py`, `conditional-2-perf-numbers.py`, `fluency-conditional-numbers.py`, `problems-conditional-numbers.py`. No round 1 check needed changing.
- `VOICE_BASE=app/content/courses/conditional/ python3 docs/reviews/voice-scan.py 35`: 0 sentences over 35 words, 0 explanations over three sentences.
- Playthrough with `--local-cdn`, desktop and `--mobile`: l1, l11, l12, l13, l15, l16, review-2, homework-1, homework-2, all "All passed", exit 0, 0 relaunches.
