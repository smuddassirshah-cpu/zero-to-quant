# Topic 2.6 exam: second-reader findings

Scope: `app/content/exams/topic-2.6.json` (id `topic-2.6`, 75 minutes, pass 0.7, 25 items over `stat-models` L1 to L4), read in full against `docs/reports/exam-2.6.md`, `docs/AUTHORING.md` sections 5 and 6, `stat-models/course.json` and every lesson's `skills`, and the engine's numeric grading (`%` unit, `accept` rendering through `grade.js` `inline`) and `code` tests.

Method: ran the author's scripts; flattened the exam and read every string; recomputed every key, every `wrong` value and every stated number by a second route (SciPy `chi2`, `binom`, `norm`, `f` and `rankdata`, Python `statistics`, Monte Carlo with 2 to 4 million gamma draws for the predictive); ran both code items' solutions and starters on every example and hidden test in CPython, and checked the rank $H$ against `scipy.stats.kruskal`; checked typed answers from rounded intermediate steps against each band; measured option lengths; ran a fuzzy match of every exam string against every `stat-models` lesson, review and homework string; ran the validator and the voice scan on a scratch copy.

Scratch scripts (not committed): `/tmp/claude-0/-home-user-zero-to-quant/563c2e64-8acc-5553-b27e-d47f109c8bd3/scratchpad/rev0626/` (`flat.py`, `recompute26.py`, `codecheck.py`, `opts.py`, `near.py`, `grepc.py`).

Format: `n. item [index] path | severity | problem | evidence | fix`. Severities: wrong, misleading, coverage, voice, layout.

## Script results

- `python3 -I docs/briefs/exam-2.6-scripts/check_numbers.py`: 215 of 215, exit 0. It prints 7 "check by hand" lines. All 7 recompute: 0.3012, 76.85%, 2.74, 0.0120, 4%, 6.4%, 3,428.6.
- `python3 -I docs/briefs/exam-2.6-scripts/fresh.py`: runs, 68 lines. No keyed number recurs in `stat-models`. Hits elsewhere are common numbers in unrelated courses; `kruskal` hits are Kruskal's spanning-tree algorithm in `graphs-dp`.
- My recompute: 60 of 60 checks pass. Code: both solutions pass all 7 hidden tests and the example; both starters fail all 7 hidden tests and pass only the visible example. $H$ matches `scipy.stats.kruskal` (tie-corrected) on every hand-checkable test and on `SLIP`.
- Validator: `0 errors, 2311 warnings`; no line names topic-2.6.
- Voice scan (copy of the exam only): 474 sentences, 0 over 20 words, 0 explanations over three sentences. No `!`, em-dash, en-dash or American spelling.

## What the author's scripts do not check

- One item's prose giving away another item's key (finding 1).
- Freshness by setup or wording (findings 2 and 3). `fresh.py` searches numbers, so it misses a copied outcome row and a copied question.
- A common slip whose value lands inside the answer band (finding 4), and typed answers built from rounded steps the explanation itself shows (findings 5 and 6).
- Option wording and length in the multi item (finding 7), how `accept` lines render (finding 8), and hypotheses on general claims (finding 9).

## Findings

1. `e-no-defaults-next` [20] `prose` | misleading | The prose gives away [14]'s key. [14] asks for the posterior of Gamma(3, rate 2) after 7 defaults in 5 years; [20] opens with "posterior Gamma(10, rate 7)" and its why and explain state $\lambda = 10/7$. A learner who reads ahead types 1.4286 in [14] without the update. | [14] `answer` 1.4286, `feedback.correct` "Gamma(10, 7), with mean $10/7$"; [20] prose "A loan book's default rate has posterior Gamma(10, rate 7)"; [20] `parts[1].options[1].why` "Both use the same mean, $10/7$". | Give [20] its own book and ask for a count the lesson did not ask (this also clears finding 2). Prose: "Another loan book's default rate has posterior Gamma(12, rate 8). Next year's count is Poisson($\lambda$). Its predictive is negative binomial: $P(j) = \binom{11 + j}{j}\left(\tfrac89\right)^{12}\left(\tfrac19\right)^j$." Part 0 question: "What is the predictive chance of exactly one default next year? Give 4 decimal places." `answer` 0.3244 (exact 0.3244206), `tol.abs` 0.0005, label "P(one default)". Wrongs, each `tol.abs` 0.0005: `plug-in` 0.3347 ("You plugged in $\lambda = 1.5$, giving $1.5e^{-1.5} = 0.3347$. That ignores the doubt about $\lambda$."); `zero` 0.2433 ("That is $P(0) = (8/9)^{12}$. The question asks for exactly one default."); `no-coef` 0.0270 ("You left out $\binom{12}{1} = 12$, giving 0.0270."). `feedback.correct`: "$12 \times (8/9)^{12} \times \tfrac19 = 0.3244$." `feedback.generic`: "Put $j = 1$ into $P(j)$. The coefficient is $\binom{12}{1} = 12$." Part 1 question: "Why is the predictive chance below the plug-in's 0.3347?" Key `doubt`: "Doubt about $\lambda$ spreads the predictive, moving chance from middle counts to both tails." `prior` why: "You blamed the mean. Both use the same mean, $12/8 = 1.5$; the predictive adds spread." `bias` unchanged. `rounding` why: "You dismissed the gap. 0.3244 against 0.3347 differ in the second decimal." Part 1 `feedback.correct`: "Same mean, more spread: one default sits in the middle, so it loses chance to the tails." Explain: "The plug-in fixes $\lambda = 1.5$ and gives $1.5e^{-1.5} = 0.3347$. The predictive averages $\lambda e^{-\lambda}$ over the posterior, giving 0.3244. Doubt about $\lambda$ moves chance from the middle counts to the tails." Recomputed: $12 (8/9)^{12}/9 = 0.32442$; Monte Carlo $E[\lambda e^{-\lambda}]$ over 4 million Gamma(12, rate 8) draws 0.32445; plug-in 0.33470; $P(0)$ 0.24332 (Monte Carlo 0.24334); no-coef 0.02704. Bands do not overlap (key 0.3239 to 0.3249, plug-in 0.3342 to 0.3352). No "Gamma(12", 0.3244 or 0.3347 in `stat-models`. Update `check_numbers.py`.

2. `e-no-defaults-next` [20] `parts[0]` | coverage | Not fresh: part 0 is l15 quiz 3 with new numbers. Same question text, the same plug-in distractor, and the prose hands over $P(0)$, so a d4 part is one power. | `l15-posterior-predictive.json` quiz[3]: "The default posterior is Gamma(17, rate 6). Its predictive is negative binomial with $r = 17$, $p = 6/7$." Question "What is the predictive chance of no defaults next year?", wrong `pois` $e^{-2.8333}$. Fuzzy ratio 0.83 to the exam question. | Fixed by finding 1's rewrite (exactly one default, coefficient 12, answer below the plug-in).

3. `e-fill-time-family` [0] whole item | coverage | Not fresh: the outcome is l1's table row and the options are the l1 and review-1 option set. | `l1-beyond-normal-errors.json` screens[3] row "Seconds until a limit order fills", "positive, skewed right", keyed Gamma with log; l1 quiz[0] and review-1 item 0 use the same four "family with a link" options and the same question "Which family and link suit this outcome?". | Change the outcome. Title "Block trade sizes". Prose: "A desk models the size, in £m, of each block trade against the stock's daily volume. Sizes are positive and right-skewed, and their spread grows with their mean." Options unchanged. `poisson` why: "You matched "positive and skewed" to counts. Poisson is for whole-number counts, not continuous sizes." `binomial` why: "You picked the 0/1 family. Whether a block trade happens is binary, but its size is not." Explain sentence 1: "A size is continuous and positive." No "block trade" in `stat-models`.

4. `e-perm-p` [11] `widget` | misleading | The commonest slip is marked correct. With $B = 999$, adding 1 to the count only gives $13/999 = 0.013013$, which is 1.3e-5 from the key and inside `tol.abs` 5e-5. Adding 1 to $B$ only gives $12/1000 = 0.0120$, which lands in `raw` and gets "You divided 12 by 999". | Key 0.013, band 0.01295 to 0.01305. | Use $B = 299$ and $c = 20$, where each slip separates at 4 places. Prose: "A permutation test of a signal's edge runs $B = 299$ shuffles of the signal days. 20 shuffles give an edge at least as large as the real one." `answer` 0.07, `tol.abs` 5e-5. Wrongs, each `tol.abs` 5e-5: `raw` 0.0669 ($20/299 = 0.066890$; "You divided 20 by 299, giving 0.0669. Add the real data to both counts: $(c + 1)/(B + 1)$."); `top-only` 0.0702 ($21/299 = 0.070234$; "You added 1 to the count but not to $B$, giving 0.0702. The real labelling joins both counts."); `bottom-only` 0.0667 ($20/300$; "You added 1 to $B$ but not to the count, giving 0.0667. The real labelling is at least as large as itself."). `feedback.correct`: "$(20 + 1)/(299 + 1) = 0.0700$." Explain sentence 2: "That gives $(20 + 1)/(299 + 1) = 0.0700$, never below the floor $1/300$." Bands 0.06995 to 0.07005, 0.07018 to 0.07028, 0.06684 to 0.06694 and 0.06662 to 0.06672 do not overlap. l11 quiz 0 uses $B = 199$ and review-3 $B = 499$; no 299 in a permutation setting in `stat-models`.

5. `e-ess-sticky` [17] `widget.tol` | misleading | The band rejects the route the explanation shows. Explain sentence 2 works $(1 - 0.75)/(1 + 0.75) = 0.1429$; then $6{,}000 \times 0.1429 = 857.4$, which is 0.26 from the key and outside `tol.abs` 0.05. | Key 857.14, band 857.09 to 857.19. | Set `tol.abs` to 0.5 (band 856.64 to 857.64): 857.1 and 857.4 pass. Wrongs 1,500 and 3,428.57 stay far outside. Add the 857.4 case to `check_numbers.py`.

6. `e-rejections-dispersion` [23] `parts[2].widget.tol` | misleading | A learner who rounds $z$ to 2 places for a normal table is marked wrong. $z = 1.4846$; $z = 1.48$ gives $p = 0.1389$ and $z = 1.49$ gives 0.1362, both outside the band. | Key 0.1376, `tol.abs` 0.0005, band 0.1371 to 0.1381. | Set `parts[2].widget.tol.abs` to 0.0015 (band 0.1361 to 0.1391). The `poisson` wrong 0.0101 stays far outside.

7. `e-design-confound` [9] `widget.options[1]` (`block`) | misleading | Two problems. The wording randomises timing, not assignment: "with a random choice of which goes first" leaves open which order goes to which algorithm. And this key is 91 visible characters against at most 64 for any distractor, a length cue. | Option as quoted; visible lengths coin 48, block 91, choose 55, time 46, size 64. | Text: "Each stock-day has two orders, and a coin flip picks which one goes to A." (73). Explain unchanged.

8. `e-pd-at-leverage` [1] `widget.accept` and `e-deviance-two` [7] `widget.accept` | layout | The accepted-answer lines show raw braces. `inline` renders KaTeX only between `$` signs, and these strings have none, so the learner sees "e^{1.2}" and "e^{-3.75}". | `topic-2.6.json`: `"accept": "1 / (1 + e^{1.2}) = 23.15%"` and `"accept": "P(chi-square with 2 df > 7.5) = e^{-3.75} = 0.0235"`; `grade.js` `inline` matches only `$...$`, `$$...$$` and backticks. | [1]: `"$1/(1 + e^{1.2}) = 23.15\\%$"`. [7]: `"$P(\\chi^2_2 > 7.5) = e^{-3.75} = 0.0235$"`. For consistency, [15]: `"$(8/9)/(4/9 + 1/9) = 1.6\\%$"`.

9. `e-kruskal-h` [24] `explain.text` sentence 3 | misleading | A general claim without its hypothesis. "Refer $H$ to $\chi^2$ with $k - 1$ df" holds only for groups of about five or more; the item's own tests have groups of 2. | Explain as quoted; tests [0] and [6] use groups of two. | "With about five or more orders per group, refer $H$ to $\chi^2$ with $k - 1$ df."

10. `e-walsh-median` [22] and `e-kruskal-h` [24] | coverage | Neither method is taught in `stat-models`: no lesson, review or homework mentions Hodges-Lehmann, Walsh averages or Kruskal-Wallis. Both prompts define the method in full, so they are fair transfer items for d4 and d5 code. But the report says L3 covers "Hodges-Lehmann", which reads as taught. | grep `Hodges|Walsh|Kruskal` over `stat-models`: 0 hits (l10 teaches the sign, Mann-Whitney and signed-rank tests; l13 the median of slopes). | No exam change. In `docs/reports/exam-2.6.md` say "Hodges-Lehmann and a rank ANOVA, defined in the prompts".

11. whole exam | coverage | Near relatives with new numbers, all acceptable. No change. [1] vs l2's PD and its odds slip; [2] vs l6 (MSB 9 again, with new sums of squares); [3] uses l10's question text with $U_X = 99$ of 180; [4] vs review-4's Beta prior; [5] vs l3 and homework-1 offsets; [7] vs l5 (2 df tail $e^{-x/2}$, drop 6 there, 7.5 here); [15] vs l14's alpha prior; [16] vs l16 and review-4; [17] vs l17 and review-4 (9,000 draws at $\phi = 0.8$); [19] vs l13's raw-MAD slip; [21] vs l18's shrinkage; [23] parts 0 and 1 vs l5 screen 2 and review-1 item 8 (SE times $\sqrt{\hat\phi}$ with the same `phi` and `div` slips). [23] is a d5 item whose first two parts are d3 steps from the course; only the $p$-value is new. | `near.py` fuzzy matches above 0.7, each read. | None. The author may want [23] part 1 on a quantity the course has not asked, but it is not required.

## Checks with no finding

- Every key and every `wrong` recomputes: 0.2315, 0.3012, 0.7685; 1.8, 0.1714, 1.9714, 1.3714; 0.55, 0.45, 3.6667; 0.3667, 0.36, 0.4, 0.6; 18.2786, 0.9139, 2.7379; $-2.6363$, $-1.5863$, $-1.4183$; 0.0235, 0.0062; 318, 159, 251; 15, 25, 5; 0.013, 0.0120; 0.3896, 0.4773, 1.1754; 0.0309, 0.0154, 0.1153, 4,048; 1.4286, 5, 1.4; 1.6, 4, 6.4; accept at $\ln 0.35 = -1.0498 < -0.9$; 857.14, 1,500, 3,428.57; 32, 16, 14.4, 10, 1.1111, 0.9091, 3.2, 42, cut 4.2565; 0.3, 1.2714, 0.4, 0.5930, 2.9702; 0.2631, 0.2397 (Monte Carlo 0.2630); 0.6, 0.4, 0.51, 0.55, 0.45; 3.0, 2.94, 0.0485, 0.084, 0.0162, 0.1376, 0.0101.
- Rounded routes: [12] with 1.3060 and 0.3314 gives 0.3895, inside the band; [6] with $\eta = -1.386$ gives $-2.636$, inside; [8] with 1.96 and 0.84 gives 317.5, so 318. The `%` unit divides typed values by 100, so 23.15 and 1.6 hit, and 30.12 and 76.85 hit their slips. Exceptions: findings 4 to 6.
- No wrong band overlaps its answer band (except finding 4's unlisted slip).
- Choice and multi: all `shuffle: true`; every distractor has a `why` naming an action; no explanation names an option by place. Only finding 7 is a length cue.
- Code: `walsh_median` tests separate $i \le j$ from $i < j$ (tests 0, 1, 2, 5 and 6) and from all ordered pairs (tests 0, 2, 5 and 6; test 2 gives 0.85 against 1.175). `kruskal_h` tests separate ranks from raw values (tests 3, 5, 6) and need average ranks for ties (tests 1 and 3). Both `how` lines name 7 tests, as there are.
- Coverage: the six skills equal `stat-models/course.json`; each is on an auto-graded item (`sm-hier` on [21]). Levels L1 6, L2 5, L3 7 with [24], L4 7, and every lesson from l1 to l18 has an item. Ramp 5, 13, 5, 2 (20, 52, 20, 8%).
- Pace: 3,420 s = 57 minutes of 75; the two code items take 360 and 480 s.
- Statistics and hypotheses: the LR test is stated as roughly $\chi^2$; Gamma variance $\phi\mu^2$; the conjugate updates; Silverman's rule as a rule; $(N - 1)\text{SSB}/\text{SST}$ on ranks equals the tie-corrected Kruskal-Wallis $H$; the predictive at 0 exceeds the plug-in by convexity of $e^{-\lambda}$.

## Counts

- Wrong: 0.
- Misleading: 6 (findings 1, 4, 5, 6, 7 and 9).
- Coverage: 4 (findings 2, 3, 10 and 11; 10 and 11 need no exam change, and 2 is fixed by 1).
- Voice: 0. Layout: 1 (finding 8).
- Author's scripts: `check_numbers.py` 215 of 215, exit 0, 7 by-hand lines all recompute; `fresh.py` clean in `stat-models` by number. Validator 0 errors, no topic-2.6 warning. No engine change needed.

## Fix pass

Edits by `docs/briefs/exam-2.6-scripts/build.py`, regenerated into `app/content/exams/topic-2.6.json`; `check_numbers.py` and `fresh.py` updated for each change. Every changed key and slip recomputed.

1. fixed: [20] rewritten as proposed (Gamma(12, rate 8), exactly one event, answer 0.3244, slips 0.3347, 0.2433, 0.0270), recomputed by quadrature and 4 million Monte Carlo draws. Departure: the story is a venue's outages per month, not a loan book, so it shares no setup with l15 or with [14].
2. fixed: by the same rewrite (new question, coefficient 12 needed, answer below the plug-in).
3. fixed: [0] now block trade sizes in £m; options unchanged, two whys reworded. No "block trade" or "outage" in `stat-models`.
4. fixed: [11] now $B = 299$, $c = 20$, answer 0.0700; slips 0.0669, 0.0702, 0.0667. The script asserts that no band overlaps.
5. fixed: [17] `tol.abs` 0.5; the script checks 857.1 and 857.4 pass and the slips fail.
6. fixed: [23] part 2 `tol.abs` 0.0015; the script checks $p$ from $z$ = 1.48, 1.49, 1.485 passes and the Poisson slip fails.
7. fixed: [9] `block` option reworded to a coin flip assigning algorithm A.
8. fixed: [1], [7] and [15] `accept` lines now in `$...$`.
9. fixed: [24] explanation states the group-size condition.
10. deferred: the one-line change to `docs/reports/exam-2.6.md` (Hodges-Lehmann and rank ANOVA "defined in the prompts") is outside the two exams and their scripts; the exam is unchanged.
11. no change needed, as the review says.

Gates: validator 0 errors, no warning naming topic-2.6; voice scan on a copy 0 long sentences, 0 long explanations, no `!` or dashes; `check_numbers.py` 233 of 233, exit 0 (`check_wrongs()` then `report()`); `fresh.py` runs, new items clean in `stat-models`; playthrough `--exam topic-2.6` green (25 of 25) with and without `--mobile`.
