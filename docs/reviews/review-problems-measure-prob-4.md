# Problem set 3.2, measure-prob level 4: second-reader findings

Scope: `app/content/courses/measure-prob/problems-4.json`: 4 problems, 18 parts (13 numeric, 1 `expression`, 4 choice), 34 `wrong` entries. Rules: `docs/briefs/wave-c-reader-ag.md`, `docs/briefs/chained-prompts.md`, `docs/briefs/chained.md`, `docs/briefs/wave-c-author-ag.md`. Pattern: `review-problems-analysis-1-3.md`.

## Verdict per problem

| problem | closest lesson screen | closest quiz item | closest review item | closest homework item | closest other set problem | closest exam item | verdict |
|---|---|---|---|---|---|---|---|
| `p-recovery-reweight` | l14 screen 5 "Two normals" (write $\tfrac{dQ}{dP}(x)$ for two densities) | l14 quiz 2 ($\tfrac{dP}{dQ}$ for two uniforms) | `r-ac` (which way $\ll$ holds) | `h-expect` ($Z$, then $E_Q$ on four outcomes) | none in sets 1 to 3 | `e-is-weight` (one normal weight) | `clean` |
| `p-share-numeraire` | l16 screen 4 ($Z_3$ on a path) and l17 screen 1 (discounted prices) | l16 quiz 4 ($Z_3$ on H, H, T) | `r-twostep` ($Z_2$, then a call by $E_P$) | `h-tree` (put by $E_P[Z_2 \cdot]$) | none | `e-tree-price` ($q$, a call) | `clean` |
| `p-ten-trades` | l15 screen 3 (fair coin against a 0.6 coin on H, H, T) and screen 9 (draws, plain against importance) | l15 quiz 2 (one normal weight) | `r-n` (plain draws from $\sqrt{(1 - p)/p}$) | `h-is` part 3 (draws at 10%) | none | `e-is-weight` | `clean` |
| `p-premium-weight` | l14 screen 10 "State prices on the one-step tree" and screen 8 (the gap is a covariance) | l17 quiz 1 ($q$), then l14 quiz 4 ($Z$ after a down move) | `r-q` ($q$ only) | `h-tree`, `h-long` | none | `e-tree-price` part 1 | `reuse` (one line, finding 6) |

No problem is ruled `re-author`. Both texts for each pairing are in section C.

Method. The author's script was run first. Lessons l14 to l17 (screens and quizzes), `review-4`, `homework-4` and the five `exams/topic-3.2.json` items that carry `mt-change` or `mt-martingale` were read in full through a text dump (`SCRATCH/read-measure-prob/l4/taught.py`). No other exam carries an `mt-` skill. Every part was solved by hand from its text and again in `docs/reports/problems-measure-prob-4-numbers-read.py`, which imports nothing from the author's script. Route 1 is exact fractions with antiderivatives typed by hand. Route 2 is a midpoint rule for each integral, a walk over all 8 three-step paths, all 4 two-step paths and all 1,024 trade sequences with exact path weights, the $Q^S$ measure built path by path from $Q \times Z_3$ (not from $qu/1.02$), the contract priced under $Q$ against $48\,Q^S(S_3 > 50)$, and both covariances from the definition against the difference of means. Each `wrong` value was rebuilt from the slip its line names, each printed working figure recomputed, and each rounded input a part hands on (0.1455, 0.00676, 1.12, 0.5208, 0.7619, 1.3571) checked to give the same key. Every typed part then went through the engine's own graders in node (`SCRATCH/read-measure-prob/l4/probe4.mjs`: 138 rows of the key at the asked places, one place more and less, fractions, a pound sign, a true minus sign, each `wrong` entry and my own strings). The story check covered `app/content` for each key number and noun, and by keyword the 23 `exams/mock-*.json` files and the `puzzles` and `brainteasers` courses.

## Tool results

| check | result |
|---|---|
| author's script (scratch venv) | `problems-measure-prob-4-numbers.py` 267 checks, 0 failures, exit 0 |
| reader's script | `problems-measure-prob-4-numbers-read.py` 392 checks, exit 0, 3 `FINDING` lines (findings 1, 2, 3) |
| `probe4.mjs` (engine graders, 14 typed parts) | 138 rows; 1 row is finding 2; 2 rows were my own wrong guesses (0.457 and 1.357 are 3 places where 4 are asked, and are refused) |
| validator | 0 errors, 4567 warnings, none on `problems-4`; `manifest.json` restored |
| voice scan 35, course folder | 0 and 0 |
| `fresh-check.mjs --files problems-4 --pairs` | 0 hits |
| `grade-all.mjs --file --local-cdn` | 18 widgets (expression 1, numeric 13, choice 4), 0 failures |
| browser, `playthrough.mjs` | not run (reader rule) |

Result. All 14 typed keys and the 4 choice keys agree with mine, and so do all 34 `wrong` values and every printed figure. No learner with the right answer is marked wrong. Every claim was read: $Q \ll P$ and $P \ll Q$ in the recovery problem (both densities positive on $(0, 1]$), the infinite mean square ($\int_0^1 dx/x$), unbiasedness under $P \ll Q$, $E_Q[Z_3] = 1$ by the martingale property, $Z_3 < 2$ (top path 1.8405), equivalence from $Z_3 > 0$, the product form of $Q^S$ (checked on all eight paths), $E_Q[Y^2] = E_P[\mathbf{1}_A \tfrac{dP}{dQ}]$, the plain relative error $\sqrt{(1 - P(A))/P(A)}$, $E_Q[Z_1] = E_P[Z_1^2] \approx 1.085$, and the premium identity for any traded price. All hold. Definitions match the lessons' wording (density, equivalent measures, likelihood ratio, relative error per draw). One part needs a condition the text does not give (finding 1). One slip sits on a rounding tie (finding 2). One restatement credits the wrong part (finding 3). Two choice parts can be picked by matching words (findings 4, 5). One `explain` line retells a lesson sentence (finding 6).

Chain and cover. Each later part restates what it uses. Lessons drawn on: l14 (problems 1, 2, 4), l15 (1, 3), l16 (2, 3, 4), l17 (2, 4). Nothing beyond level 4 is needed: the share measure of problem 2 is built in the prose from a density, and each step uses l14 and l16 facts. Typed parts 14 of 18. Difficulty 3, 5, 4, 4. Skills `mt-change` and `mt-martingale` are carried by level 4 lessons.

## A. Findings

1. `misleading` | `measure-prob/problems-4.json` | `items[3].prose`, `items[3].parts[4].question` | the two-step tree is not given.
   The prose gives one step in pounds: "A share at £40 moves to £48 or £34 over a step". Part 5 says "The same one-step weights apply at each step" and its key needs $E_P[S_2] = 40 \times 1.06^2 = 44.944$, so the share must move by the factors 1.2 and 0.85 again. Nothing says so. Equal weights fix $q$ only, and $qu + (1 - q)d = 1.01$ does not fix $u$ and $d$. A learner who reads the step as £8 up or £6 down gets $E_P[S_2] = 44.8$ and $40.804 - 44.8 = -4.00$, which lands in the `doubled` band and is told "That doubles the one-step covariance".
   Fix, `items[3].parts[4].question`: "At each step the share moves in the same proportions, so the same one-step weights apply and $Z_2$ is their product. Using the step from part 4 over two steps, find $\mathrm{Cov}_P(Z_2, S_2)$. Give a decimal to 2 places."
   Key, `wrong` values and all lines stay ($-4.14$; $-4$, $4.14$, $-4.544$).

2. `misleading` | `measure-prob/problems-4.json` | `items[2].parts[1].widget.wrong[0]` (`no-weight`) | a slip on a rounding tie (reader rule 2).
   The slip is $P(A) = \tfrac{7}{128} = 0.0546875$ exactly, a tie at the 5 places asked. It is stored as 0.054688 with `tol.abs` 5e-06, so the band takes 0.05469 and refuses 0.05468. Engine probe: "0.05468" gets the generic line; "0.05469", "0.0546875" and "7/128" get `no-weight`. The validator rule `[rounding-tie]` reads the stored value and so does not see the tie (Engine note 1).
   Fix: `"value": 0.0546875, "tol": { "abs": 1e-05 }`. The band is then $[0.0546775, 0.0546975]$, which takes both roundings; the key 0.006759 and `eight-only` 0.006395 are far from it. The author's script needs the new value.

3. `continuity` | `measure-prob/problems-4.json` | `items[1].parts[4].question` | the restatement credits part 3 with part 4's result.
   "Using price $= 48\,Q^S(S_3 > 50)$ and $q^S = \tfrac{25}{48}$ from part 3". Part 3 found $q^S$; the price line is part 4's.
   Fix: "Using price $= 48\,Q^S(S_3 > 50)$ from part 4 and $q^S = \tfrac{25}{48}$ from part 3, what is the contract worth? Give your answer in £ to 2 decimal places."

4. `misleading` | `measure-prob/problems-4.json` | `items[1].parts[3]` | passable by matching words (reader rule 3).
   The question ends "Using $Z_3$ from the stem, which line rewrites the price with $Q^S$?" The correct option is the only one that contains $Z_3$, and the only one written as a chain of two forms. A learner can pick it without the step $S_3/1.02^3 = 48Z_3$.
   Fix, question: "A contract pays $S_3$ at step 3 if $S_3 > 50$ and nothing otherwise. Its price is $E_Q[S_3\mathbf{1}_{\{S_3 > 50\}}]/1.02^3$. Which expression equals that price?"
   Fix, option `qs` text: "$48\,Q^S(S_3 > 50)$". The other three options, the `why` lines, `feedback` and `explain` stay; `feedback.correct` already gives the middle step.

5. `misleading` | `measure-prob/problems-4.json` | `items[3].parts[3].widget.options[0].text` | passable by matching words (reader rule 3).
   The question asks which step holds "for any traded price $X$". The correct option alone ends ", for any traded $X$".
   Fix, option `any` text: "$E_P[Z_1X_1] = E_Q[X_1] = 1.01X_0$ and $E_P[Z_1] = 1$". Nothing else changes.

6. `reuse` | `measure-prob/problems-4.json` | `items[3].parts[1].explain.text` | a lesson sentence retold.
   l16 screen 3 "One step", prose: "The weight on each outcome is its new chance over its old one." The explain line opens: "A one-step density is the new chance of the outcome over its old chance." Same sentence with "density" for "weight". `fresh-check` does not report it.
   Fix, `explain.text`: "$Z_1$ takes one value for each move. After an up move it is $\tfrac{16/35}{0.6} = \tfrac{16}{21}$. After a down move it is $\tfrac{19/35}{0.4} = \tfrac{19}{14} \approx 1.3571$."

## B. Notes, no change asked

- Key bands. Six parts that ask 4 places carry `tol.abs` 0.0001, so a neighbour of the right rounding passes (0.8511 for 0.8510, 0.5209 for 0.5208, 0.1456 for 0.1455). `p-recovery-reweight` part 2 uses 5e-05. Each band takes the printed working and every accepted form and refuses each `wrong` value, so rule 2 is met; the looser band is the course's habit in sets 1 to 3 as well.
- `p-recovery-reweight` part 4 restates $\mathrm{Var}_P(Z) = \tfrac13$ as a contrast; the step does not compute with it. `p-share-numeraire` part 3 works from the stem, not from part 1 or 2. Parts 4 and 5 of each problem do use the earlier results, so the chains stand.
- `p-recovery-reweight` part 4, `explain`: "the error does not shrink like $\tfrac{1}{\sqrt n}$" is right for an average the weights near 0 enter (the weight has tail $P(W > w) = \tfrac{1}{4w^2}$, the borderline case, error of order $\sqrt{\ln n / n}$).
- `p-share-numeraire` part 5 can be done under $Q$ without $Q^S$; both routes give 25.4991, as the `explain` says.

## C. Reuse: both texts

- `p-recovery-reweight`. l14 screen 5: "Let $P$ be $N(0, 1)$ and $Q$ be $N(\theta, 1)$ ... Write $\tfrac{dQ}{dP}(x)$ in terms of $x$ and $\theta$." Ours: "Its base model $P$ has density $2x$. A rival model $Q$ has density $4x^3$ ... Write the weight $\tfrac{dQ}{dP}(x)$." Same standard task, other densities; the chain then goes to a chance through the weight, the weight's variance and a sampler with infinite mean square, none of which a screen, quiz, review, homework or exam item does. "Recovery" occurs in `exams/topic-1.6.json` as a likelihood fit, with no shared number. `clean`.
- `p-share-numeraire`. l16 screen 4: "With $p = \tfrac35$ and $q = \tfrac12$, find $Z_3$ on the path HHT." Ours, part 1: "Find $Z_3$ on the path up, down, down", with $Z_3$ a share over cash, not a product of chance ratios. `r-twostep`: "What is the call worth, as $E_P[Z_2(S_2 - 100)^+]/1.03^2$?" Ours changes from $Q$ to a share measure and prices by one chance. "Asset-or-nothing" appears in `trees/l15-digitals`, `ito/l16-pricing-in-a-minute` and `ito/review-4` as the $S_0\Phi(d_1)$ leg, with no tree, no density and no shared number. No content file has "numeraire" or $Q^S$. `clean`.
- `p-ten-trades`. l15 screen 3: "Let $P$ be the fair coin and $Q$ the coin with $p = 0.6$. On this sequence, $\tfrac{dP}{dQ}$ is the ratio of the two chances. Find $P(\text{HHT}) / Q(\text{HHT})$." Ours, part 1: "A sampled sequence has 8 wins and 2 losses. What weight $\tfrac{dP}{dQ}$ does it carry?" The same standard task with ten trades and 0.8. `r-n`: "The relative error per draw is $\sqrt{(1 - p)/p}$ ... How many draws give a 5% relative error?" Ours, part 4, quotes the same taught formula and asks for a ratio of two samplers. Parts 2 and 3 (the exact mean square over 56 sequences, the relative error from it) have no counterpart: the lesson reads its errors from a caption and a table. The lesson's order (weight, error per draw, draws) is the order of any importance-sampling question; I judge it the standard task, not a retelling. `stat-models/problems-2` `p-two-looks` and `testing/l17` have ten fair trials with a count of wins, in a sign test, another course and another question. `clean`.
- `p-premium-weight`. l14 screen 10: "£100 goes to £120 or £80 at $r = 5\%$, and $q = 0.625$. A forecaster says the real up chance is $p = 0.7$. The weight ... is $Z = q/p$ after an up move. After a down move it is $\tfrac{1-q}{1-p}$." l17 quiz 1: "What is $q$, to four decimal places?" l14 quiz 4: "What is $Z$ after a down move?" Ours, parts 1 and 2, ask those two things in that order on a £40 share. They are two standard steps and the problem is about neither: parts 3 to 5 find $\mathrm{Cov}_P(Z, S)$, the identity for any asset and the two-step value. l14 screen 8 says in one line "The gap to 3.5 is the covariance of $Z$ with the face, $0.7$"; the problem builds that remark into a chain on a tree. Two opening steps do not make a walk through several items, so not `re-author`. One `explain` line retells l16 (finding 6): `reuse`.
- Mock exams, `puzzles`, `brainteasers`: no item with a density ratio, a share measure, importance sampling, a count of wins under two win chances, or a covariance with a weight. The nearest keyword hits are Kelly staking over 10 bets (`puzzles/homework-4`) and a tree pricer in code (`mock-superday-strats`); neither shares a story or a number.

## Engine

1. `[rounding-tie]` reads the stored `wrong[].value`. A slip stored one digit past the asked places hides its tie (0.0546875 stored as 0.054688, finding 2).
2. No tool lists a choice part whose correct option alone repeats a phrase or symbol of the question (findings 4, 5).

Both are in `docs/BACKLOG-INBOX.md` under `Raised later (review problems measure-prob):`.

## Fix pass

1. Fixed. `items[3].parts[4].question` replaced with the reader's text; key -4.14 and `wrong` values unchanged (recomputed by the author's script).
2. Fixed. `no-weight` is now `0.0546875` with `tol.abs` 1e-05 (band [0.0546775, 0.0546975]); the author's script line 259 takes the exact value. The validator did not print `[rounding-tie]` on `measure-prob/problems-4` before the fix; one bullet added to `docs/BACKLOG-INBOX.md` under `Raised later (fix pass problems measure-prob 4):`.
3. Fixed. `items[1].parts[4].question` now credits the price line to part 4 and `q^S` to part 3.
4. Fixed. `items[1].parts[3]` question and option `qs` text replaced as given. The reader's script check on "restatement" now also accepts "Its price is", since the new question restates the price itself.
5. Fixed. Option `any` text lost ", for any traded $X$".
6. Fixed. `explain.text` of `items[3].parts[1]` replaced as given (16/21 and 19/14 ≈ 1.3571 rechecked).

Gates: validator 0 errors (4568 warnings, one on the set is the usual O2 long-sentence note on the finding 1 text, no pass 8 warning); voice scan 35: 0 and 0; `fresh-check` 0 hits; `grade-all` 18 widgets, 0 failures; author script 267 checks 0 failures; reader script 392 checks, 0 FINDING lines; playthrough with and without `--mobile` both passed.
