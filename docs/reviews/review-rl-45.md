# rl (Reinforcement learning) L4 and L5: second-reader findings

Scope: the level 4 and 5 files in `app/content/courses/rl/` at 77cbc217 (lessons l13 to l20, `review-4`, `-5`, `homework-4`, `-5`, `problems-4`, `-5`) and the new frozen module `app/content/data/ai/rl_ops_l4.py`.
Method: gradient-checked `rl_ops_l4.log_softmax` myself in float64 (six shapes up to 3-D, logits with sd up to 1,000, rows at ±1e300, a node used twice, and `grad_check` through `policy_logits`); compared `autograd.py` and `rl_ops_l3.py` with their frozen hashes and with git; ran `docs/reports/rl-L4-numbers.py` and `-L5-` with the venv (253 and 172 checks, exit 0); `grade-all.mjs --file <f> --code --local-cdn <pkgs>` on all 14 files, one at a time (0 failures); timed every graded case of the 12 Python code widgets through `tools/code-runner.mjs` (Pyodide, the page's limits), three runs each with one worker and nothing else running; graded 58 hand-written wrong solutions through the same runner (appendix); recomputed every stated number with my own code (corridor values, scores, variances and best baselines by hand formulas; an own policy-network trainer with a one-hot loss on the module's batches over seeds 0 to 9, times 100 and normalised; an own corridor learner for the homework ratio over seeds 0 to 19; an exact Nim win chance; my own tic-tac-toe walk, alpha-beta in both orders and position count; the l19 visit counts at 20 to 1,000 iterations; every UCT score); derived each distractor from its `why`; read every screen for teaching; `voice-scan.py 35` plus an em-dash, exclamation and American-spelling grep.
Format: `path | screen/item | severity | what is wrong | fix`. Severity: error = wrong number, false claim or wrong grading; warning = weak test, loose claim or teaching issue; note = style or minor.

Counts: 7 errors, 11 warnings, 10 notes.

Worst finding: l17 screens[5] test 1 runs 6.2 to 6.4 s on a desktop against its 9 s limit (margin 1.4x), so a correct solution fails on a phone and failed for the author under load. Second: the KL leash in l16 is taught as "keeps each update small", which is not what the fixed-reference penalty that `post-train` L2 builds on does.

## Level 4 (Policy gradients)

- app/content/courses/rl/l16-a-policy-network.json | screens[7] prose and explain, quiz[2] option 'leash', summary.ideas[2] | error | The leash is a KL to a fixed reference, but the text says it "keeps the new policy close to the old one" and "keeps each update small; training language models from feedback uses exactly this leash", and the quiz keys "It keeps each update close to the reference policy". A penalty on $\mathrm{KL}(\pi \| \pi_{\text{ref}})$ with $\pi_{\text{ref}}$ fixed (the model before tuning, as in RLHF) bounds how far the policy drifts in total, not each step; a per-step limit is a KL to the previous policy (TRPO, or PPO's clip). `post-train` L2 states the fixed-reference objective $\max_\pi E_\pi[r] - \beta\,\mathrm{KL}(\pi \| \pi_{\text{ref}})$ with optimum $\pi^* \propto \pi_{\text{ref}} e^{r/\beta}$ and cites this screen, so the per-step reading would trip it. | Prose: "...from a fixed reference policy $\pi_{\text{ref}}$, such as the policy training started from, which keeps the trained policy close to it." Explain: "Here it is 0.0201. Subtracting $\beta$ times it from the objective stops the policy drifting far from $\pi_{\text{ref}}$, however many steps it takes; training language models from feedback uses exactly this leash, with $\pi_{\text{ref}}$ the model before tuning." Title "A leash to a reference"; quiz option "It keeps the policy close to the reference policy"; summary "a KL penalty keeps the policy close to a reference policy".
- app/content/courses/rl/l14-reinforce.json | screens[6] code (7 hidden tests) | warning | REINFORCE without the reward-to-go (the whole return on every move) passes all 7 tests, as does a reward-to-go that leaves out the move's own reward. Screen 5 and the prose teach reward-to-go, and the brief names it; tests 6 and 7 only check a band and a zero learning rate. | Add test 8 `reinforce_corridor(3, 0.01, 0)` expect `0.6208427163388979` (isclose); the whole return gives 0.7705 and the off-by-one 0.6019. Add the whole-return mutant with test 8.
- app/content/courses/rl/l16-a-policy-network.json | screens[4] code (7 hidden tests) | warning | A loop that never zeroes the gradients passes all 7 tests (`sgd_step` does not zero them, hint 2 asks for it, and AUTHORING section 9 names this bug for the strand). Weighting every step by the whole episode's advantage (no reward-to-go) also passes. Tests 6 and 7 are thresholds a sloppy learner still clears. | Add test 8 `train_policy(64, 0)[3].data.tolist()` expect `[-0.33355627478136485, 0.03646686415318586, 0.29708941062817906]` (isclose; two batches, about 5 ms); never zeroing gives `[-0.6422, 0.0511, 0.5911]`, the whole-episode advantage `[-0.2715, 0.1599, 0.1116]`. Add the no-zero mutant with test 8.
- app/content/courses/rl/homework-4.json | items[0] prose, solution and mutants[0] symptom | warning | The prescribed order updates $b$ after each step inside the episode, so $b$ at step $t$ has seen $G_{t-1} = G_t - 1$, which depends on this move. Unrolled, $b_t = 0.9^t b_0 + (1 - 0.9^t) G_t - \text{const}$, so the expected step-$t$ term is $0.9^t E[G_t s_t]$: the action-dependent baseline that l15's trap and items[4] option 'g' call biased. Mutant 0's symptom ("has seen this step's return") names as the bug what the solution also does. Measured at fixed $p$ (200,000 episodes): at $p = 0.55$ the baselined mean is 0.405 against the plain 0.888, while a baseline held fixed through the episode gives 0.862. On this corridor the zero stays near 0.5858, so the tests pass. `post-train` L2 uses this level's learned baseline. | Update $b$ once the dials have stepped: after the update, `for t: b += 0.1 * (G_t - b)`. Re-record tests 1 to 3 and the explain's ratio range (my "held fixed" variant in the appendix gives `(0.5016899025385794, 3.144907792241889)` for test 1), and drop or reword mutant 0.
- app/content/courses/rl/homework-4.json | items[1] prose and `variance_with` | warning | "Since the score has mean 0 in expectation, that is also the variance there" is loose: the mean of $(G - b)s$ is the gradient, not 0. And `variance_with` is the centred sample variance, whose minimiser on test 6's sample is $\mathrm{Cov}(Gs, s)/\mathrm{Var}(s) = 8.775$, not $b^* = 8.0426$ (variances 2.2023 and 2.3424). The mean return 8 gives 2.3592, so test 6 passes by 0.7%. | Prose: "Its mean, the gradient, does not depend on $b$, so in expectation $b^*$ also minimises the variance; on a finite sample the centred variance has a slightly different minimiser." Or define `variance_with` as the mean square and keep test 6.
- app/content/courses/rl/l15-baselines.json | screens[5] explain, summary.ideas[2] | warning | "Learning $V$ by TD, as in level 3, while the policy learns is actor-critic: the critic is the TD learner." A learned $V(s)$ subtracted from the Monte Carlo return is REINFORCE with a baseline; Sutton and Barto (section 13.5) keep "actor-critic" for methods whose critic bootstraps, with the TD error $r + \gamma V(s') - V(s)$ in place of $G_t - V(s)$. `post-train` names PPO, an actor-critic method. | "When the TD error $r + V(s') - V(s)$ replaces $G_t - V(s)$, the critic stands in for the rest of the return: that is **actor-critic**." Summary: "...and using $V$'s TD error in place of $G - V(s)$ is actor-critic."
- app/content/courses/rl/l13-a-policy-with-dials.json | screens[6] trap, screens[9] transfer | warning | The trap keys "deterministic is best when the agent can tell every state apart". Two screens later the rival game has full information and a coin still wins, because an opponent reacts to the rule; the explain says "As in the corridor", but the corridor's reason was aliasing. The lesson never says the two reasons differ. | Trap option 'full': "When the agent can tell every state apart and the world does not react to its rule". Transfer explain: "Here the reason is a rival who reads the rule, not states that look alike."
- app/content/courses/rl/l13-a-policy-with-dials.json | quiz[2] option 'eps' why | warning | "A larger $\varepsilon$ only moves the two reachable chances towards 0.5 together": so with greedy right and $\varepsilon = 2\sqrt2 - 2 = 0.8284$ the chance of right is exactly 0.5858. "Its $\varepsilon$ is too small" is then not wrong as the why argues it. | "With $\varepsilon = 0.83$ it would reach 0.5858, but only because you set $\varepsilon$ by hand to the answer; learning values never moves it there."
- app/content/courses/rl/l15-baselines.json | screens[6] code | note | Updating $b$ before the estimate is recorded and used passes all 9 tests (it scales each step by 0.9, so it is harmless, but hint 3 asks for the other order). | Optional test 10 `reinforce_with_baseline([10, 11], 3, 0.1, 0)` expect `([0.13065221552923528, 0.8693477844707648], 1.2045235277646982)`.
- app/content/courses/rl/l13-a-policy-with-dials.json | screens[5] code | note | A softmax that subtracts the smallest dial passes: test 1's dials (1000, 1001) are 1 apart. | Add `softmax([0.0, 1000.0])` expect `[0.0, 1.0]` (the min shift overflows).
- app/content/courses/rl/l16-a-policy-network.json | screens[4] how; train_policy docstring | note | "(a few seconds)": tests 6 and 7 take 43 to 108 ms in Pyodide here. Separately, the batch-mean baseline includes the episode's own return, so it depends on the action by a factor $1/32$ (it scales the step by 31/32, unbiased in direction); `post-train` may want the leave-one-out form. | "(well under a second)". Optional sentence in screens[8]: "The batch mean includes each episode's own return; leaving it out makes the baseline independent of the action."
- app/content/courses/rl/l13-a-policy-with-dials.json, l14-reinforce.json, l15-baselines.json | l13 screens[4] 'sign', l14 screens[2] 'sign' and screens[5] 'sign', l15 screens[0] 'sign' | note | Wrong values with no `byKey` line, so the keyed misconception gets only the generic line. | Add one line each, as the other 'sign' keys have.

## Level 5 (Search and self-play)

- app/content/courses/rl/l17-minimax.json | screens[5] code, test 1 | error | `[n for n in range(30) if nim_losing(n)]` with the solution's unmemoised recursion (about $1.84^n$ calls) takes 6,177, 6,443 and 6,423 ms in Pyodide on a desktop, alone, against a 9 s limit (5 s plus the widget's 4 s `budget`): margin 1.4x. On a phone (3 to 5 times slower) it needs 19 to 32 s, so a correct learner fails with "Stopped after 9 s"; this is the `solution-fails` the author saw with a playthrough running alongside. It also breaks the timing rule (1 s per case without an explicit case budget). Every other graded case in L4 and L5 has at least 28x margin (table below). | Put `@lru_cache(maxsize=None)` above `def nim_losing` in the starter and the solution (the memoised variant passes every test, appendix), or test `range(20)`. Either way test 1 then costs milliseconds.
- app/content/courses/rl/l17-minimax.json | screens[6] trap, prose and canvas | error | "O to move on this board" with `XX.OO....`: two marks each means X is to move under the course's own rule (X moves first; homework-5 items[0] "X is to move when the counts are equal"; l19 screens[1] uses the same board with X to move and X winning). The position cannot arise with O to move. | Use `XX.OO.X..` (X in the bottom-left cell): O is to move and wins at once at cell 5, as homework-5 test 9 already uses. Canvas row 3: `["X", "", ""]`.
- app/content/courses/rl/l20-self-play.json | screens[6] prose | error | "Silver et al. (2016) put two networks inside MCTS for Go ... a value network (level 3's idea) scores positions instead of random playouts." AlphaGo (2016) scored a leaf by mixing the value network with the result of a fast rollout policy's playout (weight one half each); the playout was dropped only in AlphaGo Zero (2017) and AlphaZero (2018). | "...a value network (level 3's idea) scores positions; AlphaGo still mixed it with fast playouts. AlphaGo beat Lee Sedol 4 games to 1 in 2016. AlphaZero (2018) dropped the playouts and learned Go, chess and shogi from self-play alone."
- app/content/courses/rl/l20-self-play.json, homework-5.json | l20 screens[6] prose "A **policy network** (this level's idea)"; homework-5 items[5] model "(this level's policy idea)" | error | Policy networks are level 4's idea (l16); this is level 5. | "(level 4's idea)" and "(level 4's policy idea)".
- app/content/courses/rl/l19-tree-search.json | screens[2] wrong 'noroot' (2.1323) | error | The why "You left out the square root in the bonus" gives $0.6667 + \sqrt2 \times \ln 4/3 = 1.3202$, the same slip review-5 and problems-5 key; 2.1323 matches no slip I can find. | Value 1.3202.
- app/content/courses/rl/l19-tree-search.json | quiz[0] wrong 'nosq' (2.1365) | error | The why "You left out the square root over $\ln N / n$" gives $0.75 + \sqrt2 \times \ln 16/4 = 1.7303$. 2.1365 is near $0.75 + 2 \ln 16/4 = 2.1363$ (the root dropped over $c^2$ too), a different slip from review-5 and problems-5. | Value 1.7303.
- app/content/courses/rl/l19-tree-search.json | screens[5] code (7 hidden tests) | warning | Playing the root child with the best average instead of the most visited passes all 7 tests: that is this lesson's trap (screens[6], summary.trap, quiz[2]). Using the child's own $n$ as the parent count in UCT, backing up draws as 0, and ignoring the `c` argument also pass. | Add test 8 `[mcts('X...O....', 'X', 40, s) for s in range(4)]` expect `[2, 6, 6, 3]` (budget not needed, about 5 ms): best average gives `[2, 6, 7, 3]`, own-$n$ parent count `[2, 2, 3, 3]`, draws as 0 `[2, 1, 1, 3]`. Add the best-average mutant with test 8.
- app/content/courses/rl/homework-5.json | items[1] `mcts_nim` (5 hidden tests) | warning | UCT with exploitation and exploration swapped ($c \cdot w/n + \sqrt{\ln N/n}$) and playing the best average both pass: every test asks for the right Nim take after 1,000 or 2,000 iterations, which almost any search finds. | Add test 6 `[mcts_nim(9, 40, s) for s in range(4)]` expect `[1, 3, 1, 1]` (both mutants give `[1, 1, 1, 1]`), with `how` saying a short seeded search pins the rule and may still miss. Add both mutants.
- app/content/courses/rl/l20-self-play.json | screens[4] code; screens[7] option 'none' why | warning | Greedy self-play ($\varepsilon$ ignored) passes all 5 tests, as does breaking ties to the most sticks. Random starting piles and zero starting values already spread the visits, so screen 7's keyed reason, "Greedy play repeats the same lines and leaves other values untouched", is not true of the setup the learner just coded. | Why: "Without exploring, nothing makes sure every move is tried; here random starts happen to cover the table." Add test 6 `self_play_nim(30, 0.5, 0.2, 0)[(5, 1)]` expect `0.779296875` ($\varepsilon$ ignored gives 0.828125, most-sticks ties 0.6943359375).
- app/content/courses/rl/l17-minimax.json, homework-5.json | l17 screens[5]; homework-5 items[0] | warning | Checking for a full board before checking for a win (so a last move that fills the board and wins scores 0) passes every hidden test in both widgets. | l17 test 9 `minimax('XXOXXOOO.', 'X')` expect `1` (the mutant gives 0). homework-5 test 10 `_after('OX......X', best_move('OX......X'))` expect `0` (the mutant plays cell 3 and loses: 1).
- app/content/courses/rl/l18-pruning-the-tree.json | screens[4] how | note | A strict cut (`alpha > beta`) is still exact but reads 146,120 nodes from the empty board, so it fails test 2's 20,000 ceiling. The prose asks for `alpha >= beta`, so this is fair, but `how` gives no reason. | How: "...node counts below ceilings, with the cut at `alpha >= beta`: under 20,000 from the empty board...".
- app/content/courses/rl/l17-minimax.json | screens[7] prose | note | "one wins now, one wins three moves later" with the depth-3 question: X's wins come at odd depths, and "three moves later" reads as depth 4. | "one wins now (depth 1), the other at depth 3".
- app/content/courses/rl/l18-pruning-the-tree.json | screens[8] wrong 'all' (9); screens[6] wrong 'three' (3) | note | The prose never says how many scenarios B has, so 9 comes from nowhere; 'three' has no `byKey` line and matches no slip. | Prose: "B has 10 scenarios." Drop 'three' or give it a why.
- app/content/courses/rl/l20-self-play.json | screens[1] explain | note | "The untrained table wins 0.43 of games" is seed 0's 200-game sample (the text says so). The exact chance for always taking 1 from 21 against the random player is 0.3894 (a 200-game rate has sd 0.035). | Optional: "...wins 0.43 of these 200 games (0.39 in the long run)".
- app/content/courses/rl/homework-5.json | items[5] model; items[3] explain | note | "AlphaGo was judged in matches against Lee Sedol (reading: Silver et al. 2016, 2018)": the 2016 paper reports the Fan Hui match; the Lee Sedol match came after it, and the 2018 paper is AlphaZero's. "about the square root of the work": 17 is about twice $\sqrt{81}$. | "AlphaGo was judged in matches against Fan Hui and Lee Sedol; AlphaZero against the strongest chess and shogi programs (reading)." "about twice the square root of the work".

## Shared code and briefs

- app/content/data/ai/rl_ops_l4.py | `log_softmax` | (no finding) | Gradient-checked: against the analytic gradient $W - \pi \sum W$ within 4.4e-16 for six shapes (1-D to 3-D, logit sd 1 to 1,000); against central differences within 7.1e-7 at sd 1,000 (finite-difference noise) and 8.7e-10 at sd 1; forward equal to a NumPy reference to 0.0; rows with $\pm 10^{300}$ give finite values and gradient; a node used twice accumulates correctly (1.3e-15); float64 throughout; `grad_check` through `policy_logits` 4.0e-11. Treating the row maximum as a constant is exact, since log-softmax does not change under a shift. | None.
- docs/briefs/rl.md | "Shared code files" | note | Lists only `rl_ops_l3.py`; `rl_ops_l4.py` (softmax, `grad_log_softmax`, `sample`, `log_softmax`, the execution task and its network) is recorded only in `docs/reports/rl-4.md`. `post-train` L2 will look here. | Main session: add a bullet for `rl_ops_l4.py` with the contract in `docs/reports/rl-4.md`.

## Downstream: what `post-train` L2 would trip on

The KL screen (l16 screens[7], error above) is the one that conflicts with post-train's fixed-reference objective. Two more matter there: l15's "actor-critic" wording (warning), since post-train names PPO; and the homework's within-episode baseline (warning), if post-train copies it as "REINFORCE with a learned baseline". The log-derivative trick (l14 screens[3]) and the baseline as a control variate (l15) are stated cleanly and in the words post-train's brief expects. `rl_ops_l4` gives `softmax`, `grad_log_softmax`, `sample` and `log_softmax`, enough for a four-answer REINFORCE without retyping; it has no generic REINFORCE step, which is fine.

## Timing of graded cases (Pyodide, desktop, one worker, three runs)

| Widget | Slowest case | Time (ms) | Limit (ms) | Margin |
|---|---|---|---|---|
| l17 screens[5] | test 1 (`nim_losing` below 30) | 6,177 to 6,443 | 9,000 | **1.4x** |
| l14 screens[6] | test 6 (corridor, 10 seeds) | 310 to 315 | 9,000 | 28.5x |
| homework-5 items[1] | test 5 (`mcts_nim(9, 2000)`, 3 seeds) | 145 to 151 | 8,000 | 52.8x |
| homework-4 items[0] | test 5 (10 seeds) | 98 to 101 | 10,000 | 99x |
| l16 screens[4] | test 7 (seeds 1 and 2) | 82 to 108 | 15,000 | 139x |
| l19 screens[5] | test 5 | 4 to 5 | 8,000 | 1,685x |
| l18, l20, l15, l13, homework-5 items[0], homework-4 items[1] | | under 60 | 5,000 to 35,000 | over 160x |

Only l17 test 1 is under the 3x margin. The widgets with NumPy (l13, l16) also get the 30 s package allowance in their limits.

## Automated checks (no finding)

- Frozen files: `autograd.py` SHA-256 5917d4ec91f7... and `rl_ops_l3.py` eba4d2b39835... match the hashes in `docs/reports/rl-3.md` and `rl-4.md`; `git diff --stat f9759b58 77cbc217 -- app/content/data/ai/` shows only `rl_ops_l4.py` added. l16 ships both through the widget `data` map by path, so the page gets the frozen text.
- Number scripts: `rl-L4-numbers.py` 253 of 253 (2 s here), `rl-L5-numbers.py` 172 of 172 (11 s), exit 0. They read the lesson JSON at each path, recompute by a second route, rerun each solution against its tests and check every distractor sits outside its answer's tolerance, so they check what is on screen. Neither checks a distractor against its `why` (they list 47 and 25 such lines "to check by hand"), which is how the two l19 UCT distractors got through.
- grade-all: 0 failures on all 14 files, run one at a time; every solution passes, every starter fails, all 33 authored mutants fail their named tests first.
- Recomputed and matching: $J(p)$ at 0.05, 0.25, 0.5, 0.5858, 0.6, 0.7, 0.95 (linear solve and closed form); gap $\ln\sqrt2 = 0.3466$; scores and estimates (−0.25, 5, −5.5, −0.2, 0.6667, 6, 84, −10, 0.7, −9, −0.6, −2.4); variances 27.5625, 0.0625, 0.5625, 6, 29.04, 0.96 and the share 0.0331; $b^*$ 10.2, 6, 3, 11 (and $b = 11$ giving zero variance); 76; losses 0.3466, 2.7726, −0.6931; normalised 1.3887; KL 0.0201 and reverse 0.0204; schedules £31, £32.5, £33 and the optimum 1, 1, 1, 1, 0 by enumeration of all 243; the new $p$ 0.6070. Network: untrained seed 0 £28.21, 960 episodes £32.885 to £32.979 on seeds 0 to 9 (my trainer, own one-hot loss), rewards times 100 collapse to £31 on seeds 1, 7 and 9 exactly, normalised pence and pounds agree within 7e-15. Homework ratio 0.1730 to 0.3225 on seeds 0 to 19. Tic-tac-toe: 549,946 nodes, 255,168 games, 5,478 positions, alpha-beta 18,297 (cells 0 to 8) and 7,275 (centre, corners, edges), value 0. Hand trees (l17, l18, review-5, problems-5) and leaves read (6, 9, 6, 7, 5). UCT 1.6280, 2.6651, 1.9274, 1.3845, 1.7597, 1.8230, 2.1460. MCTS visits from `XX.OO....` seed 0: (9, 4, 3, 2, 2), (26, 11, 5, 4, 4), (140, 25, 13, 11, 11), (898, 47, 21, 17, 17). Knuth and Moore's 17. All other distractors match their `why`.
- Facts: the policy gradient and log-derivative trick (l14 screens[3]), $E[\nabla \log \pi] = 0$ and the baseline as a control variate (l15), the softmax score $\mathbf e_a - \boldsymbol\pi$, and Sutton and Barto's Example 13.1 are stated correctly. AlphaGo beat Lee Sedol 4 to 1 in March 2016 and AlphaZero (Silver et al. 2018) learned Go, chess and shogi from self-play: both right; the 2016 rollout point is the error above.
- Seeded results are stated as those seeds' results, except the 0.43 note above.
- Voice: `voice-scan.py 35` with `VOICE_BASE` the rl folder: 0 sentences over 35 words, 0 explanations over three sentences; no em-dashes, exclamation marks or American spellings in the L4 and L5 files ("percent" appears only as a canvas `format` value).
- Finding classes from `review-rl.md`: a distractor whose `why` gives another value recurs (the two l19 UCT distractors). Hidden tests that cannot see the bug the screen teaches also recur (six warnings here: l14, l16, l19, homework-5 MCTS, l20, and the full-board order; five such findings in review-rl). That is the third review with this class, so under SESSION PROTOCOL 6 it should become a rule: for example, every AI-strand code widget that teaches a learning loop carries one exact seeded test of a short run. The tie-rule, terminal-mask and `math.isclose` formatting classes do not recur.

## Appendix: wrong solutions tried, per code widget

Each entry gives the whole source, the 1-based hidden tests it fails (the first is the `test` a `mutants` entry would name) and a symptom. Entries marked SURVIVES pass every hidden test: they are the test gaps in the findings above, not mutants to paste until a test is added. Results are from `tools/code-runner.mjs` (Pyodide 0.27.7, the page's own harness and limits), run with four workers in parallel. A failure "by time" means the case hit its limit.

### l13-a-policy-with-dials.json `.screens[5].widget` (9 hidden tests)

- **softmax subtracts the smallest dial, not the largest**: SURVIVES every hidden test.
```python
import math
import numpy as np

def softmax(theta):
    """Chances from a list of dials; safe for large dials."""
    m = min(theta)
    e = [math.exp(t - m) for t in theta]
    total = sum(e)
    return [x / total for x in e]

def corridor_value(p):
    """J(p): solve the Bellman equations of S, B and C."""
    # V = -1 + P V; rows S, B, C; reaching G ends the walk
    P = np.array([[1 - p, p, 0.0],
                  [p, 0.0, 1 - p],
                  [0.0, 1 - p, 0.0]])
    V = np.linalg.solve(np.eye(3) - P, -np.ones(3))
    return float(V[0])

def best_p(grid):
    """The p in grid with the largest corridor_value."""
    return max(grid, key=corridor_value)
```
- **softmax with no shift at all**: first fails test 1 (fails 1). Symptom: raises OverflowError: math range error.
```python
import math
import numpy as np

def softmax(theta):
    """Chances from a list of dials; safe for large dials."""
    m = max(theta)
    e = [math.exp(t) for t in theta]
    total = sum(e)
    return [x / total for x in e]

def corridor_value(p):
    """J(p): solve the Bellman equations of S, B and C."""
    # V = -1 + P V; rows S, B, C; reaching G ends the walk
    P = np.array([[1 - p, p, 0.0],
                  [p, 0.0, 1 - p],
                  [0.0, 1 - p, 0.0]])
    V = np.linalg.solve(np.eye(3) - P, -np.ones(3))
    return float(V[0])

def best_p(grid):
    """The p in grid with the largest corridor_value."""
    return max(grid, key=corridor_value)
```
- **C does not lead to G: right from C goes back to B**: first fails test 4 (fails 4, 5, 6, 7, 8, 9). Symptom: test 4 gets `nan`.
```python
import math
import numpy as np

def softmax(theta):
    """Chances from a list of dials; safe for large dials."""
    m = max(theta)
    e = [math.exp(t - m) for t in theta]
    total = sum(e)
    return [x / total for x in e]

def corridor_value(p):
    """J(p): solve the Bellman equations of S, B and C."""
    # V = -1 + P V; rows S, B, C; reaching G ends the walk
    P = np.array([[1 - p, p, 0.0],
                  [p, 0.0, 1 - p],
                  [0.0, 1.0, 0.0]])
    V = np.linalg.solve(np.eye(3) - P, -np.ones(3))
    return float(V[0])

def best_p(grid):
    """The p in grid with the largest corridor_value."""
    return max(grid, key=corridor_value)
```
- **best_p returns the best value, not the best p**: first fails test 8 (fails 8, 9). Symptom: test 8 gets `-11.65770979743696`.
```python
import math
import numpy as np

def softmax(theta):
    """Chances from a list of dials; safe for large dials."""
    m = max(theta)
    e = [math.exp(t - m) for t in theta]
    total = sum(e)
    return [x / total for x in e]

def corridor_value(p):
    """J(p): solve the Bellman equations of S, B and C."""
    # V = -1 + P V; rows S, B, C; reaching G ends the walk
    P = np.array([[1 - p, p, 0.0],
                  [p, 0.0, 1 - p],
                  [0.0, 1 - p, 0.0]])
    V = np.linalg.solve(np.eye(3) - P, -np.ones(3))
    return float(V[0])

def best_p(grid):
    """The p in grid with the largest corridor_value."""
    return max(corridor_value(p) for p in grid)
```
- **softmax not normalised**: first fails test 1 (fails 1, 2, 3). Symptom: test 1 gets `[0.36787944117144233, 1.0]`.
```python
import math
import numpy as np

def softmax(theta):
    """Chances from a list of dials; safe for large dials."""
    m = max(theta)
    e = [math.exp(t - m) for t in theta]
    total = sum(e)
    return e

def corridor_value(p):
    """J(p): solve the Bellman equations of S, B and C."""
    # V = -1 + P V; rows S, B, C; reaching G ends the walk
    P = np.array([[1 - p, p, 0.0],
                  [p, 0.0, 1 - p],
                  [0.0, 1 - p, 0.0]])
    V = np.linalg.solve(np.eye(3) - P, -np.ones(3))
    return float(V[0])

def best_p(grid):
    """The p in grid with the largest corridor_value."""
    return max(grid, key=corridor_value)
```
### l14-reinforce.json `.screens[6].widget` (7 hidden tests)

- **REINFORCE without the return-to-go: the whole return weights every move**: SURVIVES every hidden test.
```python
import math
import random

def softmax(theta):
    m = max(theta)
    e = [math.exp(t - m) for t in theta]
    total = sum(e)
    return [x / total for x in e]

def pull(pi, rng):
    """An index drawn with chances pi, from one rng.random()."""
    u, c = rng.random(), 0.0
    for i, p in enumerate(pi):
        c += p
        if u < c:
            return i
    return len(pi) - 1

def corridor_move(s, right):
    """S = 0, B = 1 (moves swapped), C = 2, G = 3."""
    if s == 0:
        return 1 if right else 0
    if s == 1:
        return 0 if right else 2
    return 3 if right else 1

def grad_log_softmax(theta, a):
    """d log pi(a) / d theta: one entry per dial."""
    pi = softmax(theta)
    return [(1.0 if b == a else 0.0) - pi[b] for b in range(len(theta))]

def reinforce_bandit(rewards, steps, lr, seed):
    """Dials from 0; each step pull a, then theta += lr * r * score."""
    rng = random.Random(seed)
    theta = [0.0] * len(rewards)
    for _ in range(steps):
        a = pull(softmax(theta), rng)
        g = grad_log_softmax(theta, a)
        theta = [t + lr * rewards[a] * x for t, x in zip(theta, g)]
    return softmax(theta)

def reinforce_corridor(episodes, lr, seed):
    """Dials [left, right] from 0; after each episode add
    lr * sum over steps of G_t * score_t. Return the final p."""
    rng = random.Random(seed)
    theta = [0.0, 0.0]
    for _ in range(episodes):
        p = softmax(theta)[1]
        s, acts = 0, []
        while s != 3:
            a = 1 if rng.random() < p else 0
            acts.append(a)
            s = corridor_move(s, a == 1)
        step = [0.0, 0.0]
        for t, a in enumerate(acts):
            G = -len(acts)           # whole return
            g = grad_log_softmax(theta, a)
            step = [x + G * y for x, y in zip(step, g)]
        theta = [x + lr * y for x, y in zip(theta, step)]
    return softmax(theta)[1]
```
- **reward-to-go that leaves out the move's own reward**: SURVIVES every hidden test.
```python
import math
import random

def softmax(theta):
    m = max(theta)
    e = [math.exp(t - m) for t in theta]
    total = sum(e)
    return [x / total for x in e]

def pull(pi, rng):
    """An index drawn with chances pi, from one rng.random()."""
    u, c = rng.random(), 0.0
    for i, p in enumerate(pi):
        c += p
        if u < c:
            return i
    return len(pi) - 1

def corridor_move(s, right):
    """S = 0, B = 1 (moves swapped), C = 2, G = 3."""
    if s == 0:
        return 1 if right else 0
    if s == 1:
        return 0 if right else 2
    return 3 if right else 1

def grad_log_softmax(theta, a):
    """d log pi(a) / d theta: one entry per dial."""
    pi = softmax(theta)
    return [(1.0 if b == a else 0.0) - pi[b] for b in range(len(theta))]

def reinforce_bandit(rewards, steps, lr, seed):
    """Dials from 0; each step pull a, then theta += lr * r * score."""
    rng = random.Random(seed)
    theta = [0.0] * len(rewards)
    for _ in range(steps):
        a = pull(softmax(theta), rng)
        g = grad_log_softmax(theta, a)
        theta = [t + lr * rewards[a] * x for t, x in zip(theta, g)]
    return softmax(theta)

def reinforce_corridor(episodes, lr, seed):
    """Dials [left, right] from 0; after each episode add
    lr * sum over steps of G_t * score_t. Return the final p."""
    rng = random.Random(seed)
    theta = [0.0, 0.0]
    for _ in range(episodes):
        p = softmax(theta)[1]
        s, acts = 0, []
        while s != 3:
            a = 1 if rng.random() < p else 0
            acts.append(a)
            s = corridor_move(s, a == 1)
        step = [0.0, 0.0]
        for t, a in enumerate(acts):
            G = -(len(acts) - t - 1)
            g = grad_log_softmax(theta, a)
            step = [x + G * y for x, y in zip(step, g)]
        theta = [x + lr * y for x, y in zip(theta, step)]
    return softmax(theta)[1]
```
- **gradient sign flipped in the corridor (descent on J)**: first fails test 6 (fails 6, 7). Symptom: test 6 runs out of time.
```python
import math
import random

def softmax(theta):
    m = max(theta)
    e = [math.exp(t - m) for t in theta]
    total = sum(e)
    return [x / total for x in e]

def pull(pi, rng):
    """An index drawn with chances pi, from one rng.random()."""
    u, c = rng.random(), 0.0
    for i, p in enumerate(pi):
        c += p
        if u < c:
            return i
    return len(pi) - 1

def corridor_move(s, right):
    """S = 0, B = 1 (moves swapped), C = 2, G = 3."""
    if s == 0:
        return 1 if right else 0
    if s == 1:
        return 0 if right else 2
    return 3 if right else 1

def grad_log_softmax(theta, a):
    """d log pi(a) / d theta: one entry per dial."""
    pi = softmax(theta)
    return [(1.0 if b == a else 0.0) - pi[b] for b in range(len(theta))]

def reinforce_bandit(rewards, steps, lr, seed):
    """Dials from 0; each step pull a, then theta += lr * r * score."""
    rng = random.Random(seed)
    theta = [0.0] * len(rewards)
    for _ in range(steps):
        a = pull(softmax(theta), rng)
        g = grad_log_softmax(theta, a)
        theta = [t + lr * rewards[a] * x for t, x in zip(theta, g)]
    return softmax(theta)

def reinforce_corridor(episodes, lr, seed):
    """Dials [left, right] from 0; after each episode add
    lr * sum over steps of G_t * score_t. Return the final p."""
    rng = random.Random(seed)
    theta = [0.0, 0.0]
    for _ in range(episodes):
        p = softmax(theta)[1]
        s, acts = 0, []
        while s != 3:
            a = 1 if rng.random() < p else 0
            acts.append(a)
            s = corridor_move(s, a == 1)
        step = [0.0, 0.0]
        for t, a in enumerate(acts):
            G = -(len(acts) - t)   # reward-to-go: -1 a step left
            g = grad_log_softmax(theta, a)
            step = [x + G * y for x, y in zip(step, g)]
        theta = [x - lr * y for x, y in zip(theta, step)]
    return softmax(theta)[1]
```
- **gradient sign flipped in the bandit**: first fails test 4 (fails 4, 5). Symptom: test 4 gets `False`.
```python
import math
import random

def softmax(theta):
    m = max(theta)
    e = [math.exp(t - m) for t in theta]
    total = sum(e)
    return [x / total for x in e]

def pull(pi, rng):
    """An index drawn with chances pi, from one rng.random()."""
    u, c = rng.random(), 0.0
    for i, p in enumerate(pi):
        c += p
        if u < c:
            return i
    return len(pi) - 1

def corridor_move(s, right):
    """S = 0, B = 1 (moves swapped), C = 2, G = 3."""
    if s == 0:
        return 1 if right else 0
    if s == 1:
        return 0 if right else 2
    return 3 if right else 1

def grad_log_softmax(theta, a):
    """d log pi(a) / d theta: one entry per dial."""
    pi = softmax(theta)
    return [(1.0 if b == a else 0.0) - pi[b] for b in range(len(theta))]

def reinforce_bandit(rewards, steps, lr, seed):
    """Dials from 0; each step pull a, then theta += lr * r * score."""
    rng = random.Random(seed)
    theta = [0.0] * len(rewards)
    for _ in range(steps):
        a = pull(softmax(theta), rng)
        g = grad_log_softmax(theta, a)
        theta = [t - lr * rewards[a] * x for t, x in zip(theta, g)]
    return softmax(theta)

def reinforce_corridor(episodes, lr, seed):
    """Dials [left, right] from 0; after each episode add
    lr * sum over steps of G_t * score_t. Return the final p."""
    rng = random.Random(seed)
    theta = [0.0, 0.0]
    for _ in range(episodes):
        p = softmax(theta)[1]
        s, acts = 0, []
        while s != 3:
            a = 1 if rng.random() < p else 0
            acts.append(a)
            s = corridor_move(s, a == 1)
        step = [0.0, 0.0]
        for t, a in enumerate(acts):
            G = -(len(acts) - t)   # reward-to-go: -1 a step left
            g = grad_log_softmax(theta, a)
            step = [x + G * y for x, y in zip(step, g)]
        theta = [x + lr * y for x, y in zip(theta, step)]
    return softmax(theta)[1]
```
- **log-probability of the wrong action in the corridor (the move not taken)**: first fails test 6 (fails 6, 7). Symptom: test 6 runs out of time.
```python
import math
import random

def softmax(theta):
    m = max(theta)
    e = [math.exp(t - m) for t in theta]
    total = sum(e)
    return [x / total for x in e]

def pull(pi, rng):
    """An index drawn with chances pi, from one rng.random()."""
    u, c = rng.random(), 0.0
    for i, p in enumerate(pi):
        c += p
        if u < c:
            return i
    return len(pi) - 1

def corridor_move(s, right):
    """S = 0, B = 1 (moves swapped), C = 2, G = 3."""
    if s == 0:
        return 1 if right else 0
    if s == 1:
        return 0 if right else 2
    return 3 if right else 1

def grad_log_softmax(theta, a):
    """d log pi(a) / d theta: one entry per dial."""
    pi = softmax(theta)
    return [(1.0 if b == a else 0.0) - pi[b] for b in range(len(theta))]

def reinforce_bandit(rewards, steps, lr, seed):
    """Dials from 0; each step pull a, then theta += lr * r * score."""
    rng = random.Random(seed)
    theta = [0.0] * len(rewards)
    for _ in range(steps):
        a = pull(softmax(theta), rng)
        g = grad_log_softmax(theta, a)
        theta = [t + lr * rewards[a] * x for t, x in zip(theta, g)]
    return softmax(theta)

def reinforce_corridor(episodes, lr, seed):
    """Dials [left, right] from 0; after each episode add
    lr * sum over steps of G_t * score_t. Return the final p."""
    rng = random.Random(seed)
    theta = [0.0, 0.0]
    for _ in range(episodes):
        p = softmax(theta)[1]
        s, acts = 0, []
        while s != 3:
            a = 1 if rng.random() < p else 0
            acts.append(a)
            s = corridor_move(s, a == 1)
        step = [0.0, 0.0]
        for t, a in enumerate(acts):
            G = -(len(acts) - t)   # reward-to-go: -1 a step left
            g = grad_log_softmax(theta, 1 - a)
            step = [x + G * y for x, y in zip(step, g)]
        theta = [x + lr * y for x, y in zip(theta, step)]
    return softmax(theta)[1]
```
- **log-probability of the wrong arm in the bandit**: first fails test 4 (fails 4, 5). Symptom: test 4 gets `False`.
```python
import math
import random

def softmax(theta):
    m = max(theta)
    e = [math.exp(t - m) for t in theta]
    total = sum(e)
    return [x / total for x in e]

def pull(pi, rng):
    """An index drawn with chances pi, from one rng.random()."""
    u, c = rng.random(), 0.0
    for i, p in enumerate(pi):
        c += p
        if u < c:
            return i
    return len(pi) - 1

def corridor_move(s, right):
    """S = 0, B = 1 (moves swapped), C = 2, G = 3."""
    if s == 0:
        return 1 if right else 0
    if s == 1:
        return 0 if right else 2
    return 3 if right else 1

def grad_log_softmax(theta, a):
    """d log pi(a) / d theta: one entry per dial."""
    pi = softmax(theta)
    return [(1.0 if b == a else 0.0) - pi[b] for b in range(len(theta))]

def reinforce_bandit(rewards, steps, lr, seed):
    """Dials from 0; each step pull a, then theta += lr * r * score."""
    rng = random.Random(seed)
    theta = [0.0] * len(rewards)
    for _ in range(steps):
        a = pull(softmax(theta), rng)
        g = grad_log_softmax(theta, (a + 1) % len(theta))
        theta = [t + lr * rewards[a] * x for t, x in zip(theta, g)]
    return softmax(theta)

def reinforce_corridor(episodes, lr, seed):
    """Dials [left, right] from 0; after each episode add
    lr * sum over steps of G_t * score_t. Return the final p."""
    rng = random.Random(seed)
    theta = [0.0, 0.0]
    for _ in range(episodes):
        p = softmax(theta)[1]
        s, acts = 0, []
        while s != 3:
            a = 1 if rng.random() < p else 0
            acts.append(a)
            s = corridor_move(s, a == 1)
        step = [0.0, 0.0]
        for t, a in enumerate(acts):
            G = -(len(acts) - t)   # reward-to-go: -1 a step left
            g = grad_log_softmax(theta, a)
            step = [x + G * y for x, y in zip(step, g)]
        theta = [x + lr * y for x, y in zip(theta, step)]
    return softmax(theta)[1]
```
- **dials updated inside the episode, chance not held fixed (reward-to-go known only at the end, so applied per step afterwards with the live dials)**: first fails test 6 (fails 6, 7). Symptom: test 6 runs out of time.
```python
import math
import random

def softmax(theta):
    m = max(theta)
    e = [math.exp(t - m) for t in theta]
    total = sum(e)
    return [x / total for x in e]

def pull(pi, rng):
    """An index drawn with chances pi, from one rng.random()."""
    u, c = rng.random(), 0.0
    for i, p in enumerate(pi):
        c += p
        if u < c:
            return i
    return len(pi) - 1

def corridor_move(s, right):
    """S = 0, B = 1 (moves swapped), C = 2, G = 3."""
    if s == 0:
        return 1 if right else 0
    if s == 1:
        return 0 if right else 2
    return 3 if right else 1

def grad_log_softmax(theta, a):
    """d log pi(a) / d theta: one entry per dial."""
    pi = softmax(theta)
    return [(1.0 if b == a else 0.0) - pi[b] for b in range(len(theta))]

def reinforce_bandit(rewards, steps, lr, seed):
    """Dials from 0; each step pull a, then theta += lr * r * score."""
    rng = random.Random(seed)
    theta = [0.0] * len(rewards)
    for _ in range(steps):
        a = pull(softmax(theta), rng)
        g = grad_log_softmax(theta, a)
        theta = [t + lr * rewards[a] * x for t, x in zip(theta, g)]
    return softmax(theta)

def reinforce_corridor(episodes, lr, seed):
    """Dials [left, right] from 0; after each episode add
    lr * sum over steps of G_t * score_t. Return the final p."""
    rng = random.Random(seed)
    theta = [0.0, 0.0]
    for _ in range(episodes):
        p = softmax(theta)[1]
        s, acts = 0, []
        while s != 3:
            a = 1 if rng.random() < p else 0
            acts.append(a)
            s = corridor_move(s, a == 1)
        step = [0.0, 0.0]
        for t, a in enumerate(acts):
            G = -(len(acts) - t)   # reward-to-go: -1 a step left
            g = grad_log_softmax(theta, a)
            theta = [x + lr * G * y for x, y in zip(theta, g)]
    return softmax(theta)[1]
```
### l15-baselines.json `.screens[6].widget` (9 hidden tests)

- **a baseline that depends on the action: one running mean per arm**: first fails test 8 (fails 8). Symptom: test 8 gets `False`.
```python
import math
import random
import statistics

def softmax(theta):
    m = max(theta)
    e = [math.exp(t - m) for t in theta]
    total = sum(e)
    return [x / total for x in e]

def pull(pi, rng):
    u, c = rng.random(), 0.0
    for i, p in enumerate(pi):
        c += p
        if u < c:
            return i
    return len(pi) - 1

def score_estimates(pi, rewards, b, k=0):
    """Estimate for dial k after pulling each arm: (r_a - b) * score."""
    return [(r - b) * ((1.0 if a == k else 0.0) - pi[k]) for a, r in enumerate(rewards)]

def variance_of_estimate(pi, rewards, b, k=0):
    """Exact variance when arm a is pulled with chance pi[a]."""
    est = score_estimates(pi, rewards, b, k)
    mean = sum(p * x for p, x in zip(pi, est))
    return sum(p * x * x for p, x in zip(pi, est)) - mean * mean

def reinforce_with_baseline(rewards, steps, lr, seed, beta=0.1):
    """Return (final chances, variance ratio for dial 0)."""
    rng = random.Random(seed)
    theta = [0.0] * len(rewards)
    b = [0.0] * len(rewards)
    plain, based = [], []
    for _ in range(steps):
        pi = softmax(theta)
        a = pull(pi, rng)
        r = rewards[a]
        g = [(1.0 if j == a else 0.0) - pi[j] for j in range(len(theta))]
        plain.append(r * g[0])
        based.append((r - b[a]) * g[0])
        theta = [t + lr * (r - b[a]) * x for t, x in zip(theta, g)]
        b[a] += beta * (r - b[a])   # after the step: b never sees this r first
    ratio = statistics.pvariance(based) / statistics.pvariance(plain)
    return softmax(theta), ratio
```
- **baseline updated before the estimate is recorded and used**: SURVIVES every hidden test.
```python
import math
import random
import statistics

def softmax(theta):
    m = max(theta)
    e = [math.exp(t - m) for t in theta]
    total = sum(e)
    return [x / total for x in e]

def pull(pi, rng):
    u, c = rng.random(), 0.0
    for i, p in enumerate(pi):
        c += p
        if u < c:
            return i
    return len(pi) - 1

def score_estimates(pi, rewards, b, k=0):
    """Estimate for dial k after pulling each arm: (r_a - b) * score."""
    return [(r - b) * ((1.0 if a == k else 0.0) - pi[k]) for a, r in enumerate(rewards)]

def variance_of_estimate(pi, rewards, b, k=0):
    """Exact variance when arm a is pulled with chance pi[a]."""
    est = score_estimates(pi, rewards, b, k)
    mean = sum(p * x for p, x in zip(pi, est))
    return sum(p * x * x for p, x in zip(pi, est)) - mean * mean

def reinforce_with_baseline(rewards, steps, lr, seed, beta=0.1):
    """Return (final chances, variance ratio for dial 0)."""
    rng = random.Random(seed)
    theta = [0.0] * len(rewards)
    b = 0.0
    plain, based = [], []
    for _ in range(steps):
        pi = softmax(theta)
        a = pull(pi, rng)
        r = rewards[a]
        g = [(1.0 if j == a else 0.0) - pi[j] for j in range(len(theta))]
        b += beta * (r - b)
        plain.append(r * g[0])
        based.append((r - b) * g[0])
        theta = [t + lr * (r - b) * x for t, x in zip(theta, g)]
    ratio = statistics.pvariance(based) / statistics.pvariance(plain)
    return softmax(theta), ratio
```
- **baseline measured but not used in the step**: first fails test 9 (fails 9). Symptom: test 9 gets `False`.
```python
import math
import random
import statistics

def softmax(theta):
    m = max(theta)
    e = [math.exp(t - m) for t in theta]
    total = sum(e)
    return [x / total for x in e]

def pull(pi, rng):
    u, c = rng.random(), 0.0
    for i, p in enumerate(pi):
        c += p
        if u < c:
            return i
    return len(pi) - 1

def score_estimates(pi, rewards, b, k=0):
    """Estimate for dial k after pulling each arm: (r_a - b) * score."""
    return [(r - b) * ((1.0 if a == k else 0.0) - pi[k]) for a, r in enumerate(rewards)]

def variance_of_estimate(pi, rewards, b, k=0):
    """Exact variance when arm a is pulled with chance pi[a]."""
    est = score_estimates(pi, rewards, b, k)
    mean = sum(p * x for p, x in zip(pi, est))
    return sum(p * x * x for p, x in zip(pi, est)) - mean * mean

def reinforce_with_baseline(rewards, steps, lr, seed, beta=0.1):
    """Return (final chances, variance ratio for dial 0)."""
    rng = random.Random(seed)
    theta = [0.0] * len(rewards)
    b = 0.0
    plain, based = [], []
    for _ in range(steps):
        pi = softmax(theta)
        a = pull(pi, rng)
        r = rewards[a]
        g = [(1.0 if j == a else 0.0) - pi[j] for j in range(len(theta))]
        plain.append(r * g[0])
        based.append((r - b) * g[0])
        theta = [t + lr * r * x for t, x in zip(theta, g)]
        b += beta * (r - b)   # after the step: b never sees this r first
    ratio = statistics.pvariance(based) / statistics.pvariance(plain)
    return softmax(theta), ratio
```
- **gradient sign flipped**: first fails test 8 (fails 8). Symptom: test 8 gets `False`.
```python
import math
import random
import statistics

def softmax(theta):
    m = max(theta)
    e = [math.exp(t - m) for t in theta]
    total = sum(e)
    return [x / total for x in e]

def pull(pi, rng):
    u, c = rng.random(), 0.0
    for i, p in enumerate(pi):
        c += p
        if u < c:
            return i
    return len(pi) - 1

def score_estimates(pi, rewards, b, k=0):
    """Estimate for dial k after pulling each arm: (r_a - b) * score."""
    return [(r - b) * ((1.0 if a == k else 0.0) - pi[k]) for a, r in enumerate(rewards)]

def variance_of_estimate(pi, rewards, b, k=0):
    """Exact variance when arm a is pulled with chance pi[a]."""
    est = score_estimates(pi, rewards, b, k)
    mean = sum(p * x for p, x in zip(pi, est))
    return sum(p * x * x for p, x in zip(pi, est)) - mean * mean

def reinforce_with_baseline(rewards, steps, lr, seed, beta=0.1):
    """Return (final chances, variance ratio for dial 0)."""
    rng = random.Random(seed)
    theta = [0.0] * len(rewards)
    b = 0.0
    plain, based = [], []
    for _ in range(steps):
        pi = softmax(theta)
        a = pull(pi, rng)
        r = rewards[a]
        g = [(1.0 if j == a else 0.0) - pi[j] for j in range(len(theta))]
        plain.append(r * g[0])
        based.append((r - b) * g[0])
        theta = [t - lr * (r - b) * x for t, x in zip(theta, g)]
        b += beta * (r - b)   # after the step: b never sees this r first
    ratio = statistics.pvariance(based) / statistics.pvariance(plain)
    return softmax(theta), ratio
```
- **score uses the pulled arm's chance for every dial**: first fails test 6 (fails 6, 7). Symptom: test 6 gets `[-0.2, 1.0, -1.2]`.
```python
import math
import random
import statistics

def softmax(theta):
    m = max(theta)
    e = [math.exp(t - m) for t in theta]
    total = sum(e)
    return [x / total for x in e]

def pull(pi, rng):
    u, c = rng.random(), 0.0
    for i, p in enumerate(pi):
        c += p
        if u < c:
            return i
    return len(pi) - 1

def score_estimates(pi, rewards, b, k=0):
    """Estimate for dial k after pulling each arm: (r_a - b) * score."""
    return [(r - b) * ((1.0 if a == k else 0.0) - pi[a]) for a, r in enumerate(rewards)]

def variance_of_estimate(pi, rewards, b, k=0):
    """Exact variance when arm a is pulled with chance pi[a]."""
    est = score_estimates(pi, rewards, b, k)
    mean = sum(p * x for p, x in zip(pi, est))
    return sum(p * x * x for p, x in zip(pi, est)) - mean * mean

def reinforce_with_baseline(rewards, steps, lr, seed, beta=0.1):
    """Return (final chances, variance ratio for dial 0)."""
    rng = random.Random(seed)
    theta = [0.0] * len(rewards)
    b = 0.0
    plain, based = [], []
    for _ in range(steps):
        pi = softmax(theta)
        a = pull(pi, rng)
        r = rewards[a]
        g = [(1.0 if j == a else 0.0) - pi[j] for j in range(len(theta))]
        plain.append(r * g[0])
        based.append((r - b) * g[0])
        theta = [t + lr * (r - b) * x for t, x in zip(theta, g)]
        b += beta * (r - b)   # after the step: b never sees this r first
    ratio = statistics.pvariance(based) / statistics.pvariance(plain)
    return softmax(theta), ratio
```
- **ratio upside down**: first fails test 9 (fails 9). Symptom: test 9 gets `False`.
```python
import math
import random
import statistics

def softmax(theta):
    m = max(theta)
    e = [math.exp(t - m) for t in theta]
    total = sum(e)
    return [x / total for x in e]

def pull(pi, rng):
    u, c = rng.random(), 0.0
    for i, p in enumerate(pi):
        c += p
        if u < c:
            return i
    return len(pi) - 1

def score_estimates(pi, rewards, b, k=0):
    """Estimate for dial k after pulling each arm: (r_a - b) * score."""
    return [(r - b) * ((1.0 if a == k else 0.0) - pi[k]) for a, r in enumerate(rewards)]

def variance_of_estimate(pi, rewards, b, k=0):
    """Exact variance when arm a is pulled with chance pi[a]."""
    est = score_estimates(pi, rewards, b, k)
    mean = sum(p * x for p, x in zip(pi, est))
    return sum(p * x * x for p, x in zip(pi, est)) - mean * mean

def reinforce_with_baseline(rewards, steps, lr, seed, beta=0.1):
    """Return (final chances, variance ratio for dial 0)."""
    rng = random.Random(seed)
    theta = [0.0] * len(rewards)
    b = 0.0
    plain, based = [], []
    for _ in range(steps):
        pi = softmax(theta)
        a = pull(pi, rng)
        r = rewards[a]
        g = [(1.0 if j == a else 0.0) - pi[j] for j in range(len(theta))]
        plain.append(r * g[0])
        based.append((r - b) * g[0])
        theta = [t + lr * (r - b) * x for t, x in zip(theta, g)]
        b += beta * (r - b)   # after the step: b never sees this r first
    ratio = statistics.pvariance(plain) / statistics.pvariance(based)
    return softmax(theta), ratio
```
### l16-a-policy-network.json `.screens[4].widget` (7 hidden tests)

- **log-probability of the wrong action: always action 0**: first fails test 1 (fails 1, 2, 6, 7). Symptom: test 1 gets `-0.03428658388538486`.
```python
import numpy as np
from autograd import Tensor, sgd_step
import rl_ops_l4 as ops

def policy_loss(logits, actions, advantages):
    """-(1/n) sum_i A_i log pi(a_i | s_i): a Tensor of shape ()."""
    n = len(actions)
    lp = ops.log_softmax(logits)
    picked = lp[(np.arange(n), np.zeros(n, dtype=int))]
    return -(picked * np.asarray(advantages, dtype=float)).sum() / n

def train_policy(episodes, seed, batch=32, lr=0.5):
    """REINFORCE; baseline = the batch's mean reward-to-go
    at the same step."""
    params = ops.init_policy(seed)
    rng = np.random.default_rng(seed + 1000)
    for _ in range(episodes // batch):
        X, A, G, totals = ops.run_batch(params, batch, rng)
        adv = (G - G.mean(axis=0)).reshape(-1)
        for p in params:
            p.zero_grad()
        loss = policy_loss(ops.policy_logits(params, X), A, adv)
        loss.backward()
        sgd_step(params, lr)
    return params
```
- **gradient sign flipped in training**: first fails test 6 (fails 6, 7). Symptom: test 6 gets `np.False_`.
```python
import numpy as np
from autograd import Tensor, sgd_step
import rl_ops_l4 as ops

def policy_loss(logits, actions, advantages):
    """-(1/n) sum_i A_i log pi(a_i | s_i): a Tensor of shape ()."""
    n = len(actions)
    lp = ops.log_softmax(logits)
    picked = lp[(np.arange(n), np.asarray(actions))]
    return -(picked * np.asarray(advantages, dtype=float)).sum() / n

def train_policy(episodes, seed, batch=32, lr=0.5):
    """REINFORCE; baseline = the batch's mean reward-to-go
    at the same step."""
    params = ops.init_policy(seed)
    rng = np.random.default_rng(seed + 1000)
    for _ in range(episodes // batch):
        X, A, G, totals = ops.run_batch(params, batch, rng)
        adv = (G - G.mean(axis=0)).reshape(-1)
        for p in params:
            p.zero_grad()
        loss = policy_loss(ops.policy_logits(params, X), A, adv)
        loss.backward()
        sgd_step(params, -lr)
    return params
```
- **no baseline: advantages are the raw reward-to-go**: first fails test 6 (fails 6). Symptom: test 6 gets `np.False_`.
```python
import numpy as np
from autograd import Tensor, sgd_step
import rl_ops_l4 as ops

def policy_loss(logits, actions, advantages):
    """-(1/n) sum_i A_i log pi(a_i | s_i): a Tensor of shape ()."""
    n = len(actions)
    lp = ops.log_softmax(logits)
    picked = lp[(np.arange(n), np.asarray(actions))]
    return -(picked * np.asarray(advantages, dtype=float)).sum() / n

def train_policy(episodes, seed, batch=32, lr=0.5):
    """REINFORCE; baseline = the batch's mean reward-to-go
    at the same step."""
    params = ops.init_policy(seed)
    rng = np.random.default_rng(seed + 1000)
    for _ in range(episodes // batch):
        X, A, G, totals = ops.run_batch(params, batch, rng)
        adv = G.reshape(-1)
        for p in params:
            p.zero_grad()
        loss = policy_loss(ops.policy_logits(params, X), A, adv)
        loss.backward()
        sgd_step(params, lr)
    return params
```
- **no reward-to-go: every step weighted by the whole episode's advantage**: SURVIVES every hidden test.
```python
import numpy as np
from autograd import Tensor, sgd_step
import rl_ops_l4 as ops

def policy_loss(logits, actions, advantages):
    """-(1/n) sum_i A_i log pi(a_i | s_i): a Tensor of shape ()."""
    n = len(actions)
    lp = ops.log_softmax(logits)
    picked = lp[(np.arange(n), np.asarray(actions))]
    return -(picked * np.asarray(advantages, dtype=float)).sum() / n

def train_policy(episodes, seed, batch=32, lr=0.5):
    """REINFORCE; baseline = the batch's mean reward-to-go
    at the same step."""
    params = ops.init_policy(seed)
    rng = np.random.default_rng(seed + 1000)
    for _ in range(episodes // batch):
        X, A, G, totals = ops.run_batch(params, batch, rng)
        adv = np.repeat((G[:, 0] - G[:, 0].mean())[:, None], G.shape[1], axis=1).reshape(-1)
        for p in params:
            p.zero_grad()
        loss = policy_loss(ops.policy_logits(params, X), A, adv)
        loss.backward()
        sgd_step(params, lr)
    return params
```
- **gradients never zeroed**: SURVIVES every hidden test.
```python
import numpy as np
from autograd import Tensor, sgd_step
import rl_ops_l4 as ops

def policy_loss(logits, actions, advantages):
    """-(1/n) sum_i A_i log pi(a_i | s_i): a Tensor of shape ()."""
    n = len(actions)
    lp = ops.log_softmax(logits)
    picked = lp[(np.arange(n), np.asarray(actions))]
    return -(picked * np.asarray(advantages, dtype=float)).sum() / n

def train_policy(episodes, seed, batch=32, lr=0.5):
    """REINFORCE; baseline = the batch's mean reward-to-go
    at the same step."""
    params = ops.init_policy(seed)
    rng = np.random.default_rng(seed + 1000)
    for _ in range(episodes // batch):
        X, A, G, totals = ops.run_batch(params, batch, rng)
        adv = (G - G.mean(axis=0)).reshape(-1)
        loss = policy_loss(ops.policy_logits(params, X), A, adv)
        loss.backward()
        sgd_step(params, lr)
    return params
```
- **a baseline that depends on the action: mean reward-to-go of rows with the same action at the same step**: first fails test 6 (fails 6, 7). Symptom: test 6 gets `np.False_`.
```python
import numpy as np
from autograd import Tensor, sgd_step
import rl_ops_l4 as ops

def policy_loss(logits, actions, advantages):
    """-(1/n) sum_i A_i log pi(a_i | s_i): a Tensor of shape ()."""
    n = len(actions)
    lp = ops.log_softmax(logits)
    picked = lp[(np.arange(n), np.asarray(actions))]
    return -(picked * np.asarray(advantages, dtype=float)).sum() / n

def train_policy(episodes, seed, batch=32, lr=0.5):
    """REINFORCE; baseline = the batch's mean reward-to-go
    at the same step."""
    params = ops.init_policy(seed)
    rng = np.random.default_rng(seed + 1000)
    for _ in range(episodes // batch):
        X, A, G, totals = ops.run_batch(params, batch, rng)
        A2 = A.reshape(G.shape)
        Bm = np.zeros_like(G)
        for t in range(G.shape[1]):
            for k in range(3):
                m = A2[:, t] == k
                if m.any():
                    Bm[m, t] = G[m, t].mean()
        adv = (G - Bm).reshape(-1)
        for p in params:
            p.zero_grad()
        loss = policy_loss(ops.policy_logits(params, X), A, adv)
        loss.backward()
        sgd_step(params, lr)
    return params
```
### homework-4.json `.items[0].widget` (6 hidden tests)

- **a baseline that depends on the action: one running mean per action**: first fails test 1 (fails 1, 2, 3, 5). Symptom: test 1 gets `(0.5012757724668515, 2.6831033375841384)`.
```python
import math
import random
import statistics

def train_corridor(episodes, seed):
    rng = random.Random(seed)
    theta = [0.0, 0.0]          # dials for left and right
    b = [0.0, 0.0]              # the learned baseline
    plain, based = [], []
    for _ in range(episodes):
        m = max(theta)
        e = [math.exp(t - m) for t in theta]
        p = e[1] / (e[0] + e[1])
        s, acts = 0, []         # S = 0, B = 1, C = 2, G = 3
        while s != 3:
            a = 1 if rng.random() < p else 0
            acts.append(a)
            if s == 0:
                s = 1 if a else 0
            elif s == 1:
                s = 0 if a else 2
            else:
                s = 3 if a else 1
        gp = gb = 0.0
        for t, a in enumerate(acts):
            G = -(len(acts) - t)
            score = (1.0 if a == 1 else 0.0) - p   # right dial
            gp += G * score
            gb += (G - b[a]) * score
            b[a] += 0.1 * (G - b[a])
        plain.append(gp)
        based.append(gb)
        theta = [theta[0] - 0.001 * gb, theta[1] + 0.001 * gb]
    m = max(theta)
    e = [math.exp(t - m) for t in theta]
    ratio = statistics.pvariance(based) / statistics.pvariance(plain)
    return e[1] / (e[0] + e[1]), ratio
```
- **gradient sign flipped**: first fails test 1 (fails 1, 2, 3, 4, 5, 6). Symptom: test 1 gets `(0.49784831858682876, 7.992434866377681)`; test 4 later runs out of time.
```python
import math
import random
import statistics

def train_corridor(episodes, seed):
    rng = random.Random(seed)
    theta = [0.0, 0.0]          # dials for left and right
    b = 0.0                     # the learned baseline
    plain, based = [], []
    for _ in range(episodes):
        m = max(theta)
        e = [math.exp(t - m) for t in theta]
        p = e[1] / (e[0] + e[1])
        s, acts = 0, []         # S = 0, B = 1, C = 2, G = 3
        while s != 3:
            a = 1 if rng.random() < p else 0
            acts.append(a)
            if s == 0:
                s = 1 if a else 0
            elif s == 1:
                s = 0 if a else 2
            else:
                s = 3 if a else 1
        gp = gb = 0.0
        for t, a in enumerate(acts):
            G = -(len(acts) - t)
            score = (1.0 if a == 1 else 0.0) - p   # right dial
            gp += G * score
            gb += (G - b) * score
            b += 0.1 * (G - b)
        plain.append(gp)
        based.append(gb)
        theta = [theta[0] + 0.001 * gb, theta[1] - 0.001 * gb]
    m = max(theta)
    e = [math.exp(t - m) for t in theta]
    ratio = statistics.pvariance(based) / statistics.pvariance(plain)
    return e[1] / (e[0] + e[1]), ratio
```
- **score of the wrong action (the left dial's entry used for right)**: first fails test 1 (fails 1, 2, 3, 4, 5, 6). Symptom: test 1 gets `(0.49784831858682876, 7.992434866377673)`; test 4 later runs out of time.
```python
import math
import random
import statistics

def train_corridor(episodes, seed):
    rng = random.Random(seed)
    theta = [0.0, 0.0]          # dials for left and right
    b = 0.0                     # the learned baseline
    plain, based = [], []
    for _ in range(episodes):
        m = max(theta)
        e = [math.exp(t - m) for t in theta]
        p = e[1] / (e[0] + e[1])
        s, acts = 0, []         # S = 0, B = 1, C = 2, G = 3
        while s != 3:
            a = 1 if rng.random() < p else 0
            acts.append(a)
            if s == 0:
                s = 1 if a else 0
            elif s == 1:
                s = 0 if a else 2
            else:
                s = 3 if a else 1
        gp = gb = 0.0
        for t, a in enumerate(acts):
            G = -(len(acts) - t)
            score = (1.0 if a == 0 else 0.0) - (1 - p)
            gp += G * score
            gb += (G - b) * score
            b += 0.1 * (G - b)
        plain.append(gp)
        based.append(gb)
        theta = [theta[0] - 0.001 * gb, theta[1] + 0.001 * gb]
    m = max(theta)
    e = [math.exp(t - m) for t in theta]
    ratio = statistics.pvariance(based) / statistics.pvariance(plain)
    return e[1] / (e[0] + e[1]), ratio
```
- **baseline held fixed through the episode and updated after it (a valid baseline)**: first fails test 1 (fails 1, 2, 3, 4). Symptom: test 1 gets `(0.5016899025385794, 3.144907792241889)`.
```python
import math
import random
import statistics

def train_corridor(episodes, seed):
    rng = random.Random(seed)
    theta = [0.0, 0.0]          # dials for left and right
    b = 0.0                     # the learned baseline
    plain, based = [], []
    for _ in range(episodes):
        m = max(theta)
        e = [math.exp(t - m) for t in theta]
        p = e[1] / (e[0] + e[1])
        s, acts = 0, []         # S = 0, B = 1, C = 2, G = 3
        while s != 3:
            a = 1 if rng.random() < p else 0
            acts.append(a)
            if s == 0:
                s = 1 if a else 0
            elif s == 1:
                s = 0 if a else 2
            else:
                s = 3 if a else 1
        gp = gb = 0.0
        for t, a in enumerate(acts):
            G = -(len(acts) - t)
            score = (1.0 if a == 1 else 0.0) - p   # right dial
            gp += G * score
            gb += (G - b) * score
        for t in range(len(acts)):
            b += 0.1 * (-(len(acts) - t) - b)
        plain.append(gp)
        based.append(gb)
        theta = [theta[0] - 0.001 * gb, theta[1] + 0.001 * gb]
    m = max(theta)
    e = [math.exp(t - m) for t in theta]
    ratio = statistics.pvariance(based) / statistics.pvariance(plain)
    return e[1] / (e[0] + e[1]), ratio
```
### homework-4.json `.items[1].widget` (6 hidden tests)

- **b* weighted by s, not s squared, in numerator and denominator**: first fails test 1 (fails 1, 2, 3, 6). Symptom: raises ZeroDivisionError: float division by zero.
```python
def best_baseline(scores, returns):
    """b* = sum(s^2 G) / sum(s^2) over the samples."""
    num = sum(s * g for s, g in zip(scores, returns))
    den = sum(s for s in scores)
    return num / den

def variance_with(scores, returns, b):
    """Population variance of (G - b) * s over the samples."""
    xs = [(g - b) * s for s, g in zip(scores, returns)]
    m = sum(xs) / len(xs)
    return sum((x - m) ** 2 for x in xs) / len(xs)
```
- **variance with the baseline added, not subtracted**: first fails test 5 (fails 5, 6). Symptom: test 5 gets `110.25`.
```python
def best_baseline(scores, returns):
    """b* = sum(s^2 G) / sum(s^2) over the samples."""
    num = sum(s * s * g for s, g in zip(scores, returns))
    den = sum(s * s for s in scores)
    return num / den

def variance_with(scores, returns, b):
    """Population variance of (G - b) * s over the samples."""
    xs = [(g + b) * s for s, g in zip(scores, returns)]
    m = sum(xs) / len(xs)
    return sum((x - m) ** 2 for x in xs) / len(xs)
```
### l17-minimax.json `.screens[5].widget` (8 hidden tests)

- **minimax without alternating: the player never changes**: first fails test 3 (fails 3, 6). Symptom: test 3 gets `1`.
```python
from functools import lru_cache

LINES = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6),
         (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]

def winner(board):
    """'X' or 'O' if a line is full of one mark, else None."""
    for a, b, c in LINES:
        if board[a] != '.' and board[a] == board[b] == board[c]:
            return board[a]
    return None

def other(player):
    return 'O' if player == 'X' else 'X'

def nim_losing(n):
    """True when the player to move with n sticks loses
    against best play (take 1, 2 or 3; last stick wins)."""
    # every move leaves the opponent in a winning position
    return all(not nim_losing(n - k) for k in (1, 2, 3) if k <= n)

@lru_cache(maxsize=None)
def minimax(board, player):
    """Value for X with best play: 1 X wins, -1 O wins, 0 draw.
    board is a 9-character string of 'X', 'O' and '.'."""
    w = winner(board)
    if w:
        return 1 if w == 'X' else -1
    if '.' not in board:
        return 0
    vals = [minimax(board[:i] + player + board[i + 1:], player)
            for i in range(9) if board[i] == '.']
    return max(vals) if player == 'X' else min(vals)

def count_positions():
    """Boards reachable from the empty board, play stopping at a
    win or a full board, the empty board included."""
    seen, stack = set(), [('.' * 9, 'X')]
    while stack:
        board, player = stack.pop()
        if board in seen:
            continue
        seen.add(board)
        if winner(board) or '.' not in board:
            continue
        for i in range(9):
            if board[i] == '.':
                stack.append((board[:i] + player + board[i + 1:], other(player)))
    return len(seen)
```
- **full board checked before a win: a winning last move scores 0**: SURVIVES every hidden test.
```python
from functools import lru_cache

LINES = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6),
         (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]

def winner(board):
    """'X' or 'O' if a line is full of one mark, else None."""
    for a, b, c in LINES:
        if board[a] != '.' and board[a] == board[b] == board[c]:
            return board[a]
    return None

def other(player):
    return 'O' if player == 'X' else 'X'

def nim_losing(n):
    """True when the player to move with n sticks loses
    against best play (take 1, 2 or 3; last stick wins)."""
    # every move leaves the opponent in a winning position
    return all(not nim_losing(n - k) for k in (1, 2, 3) if k <= n)

@lru_cache(maxsize=None)
def minimax(board, player):
    """Value for X with best play: 1 X wins, -1 O wins, 0 draw.
    board is a 9-character string of 'X', 'O' and '.'."""
    if '.' not in board:
        return 0
    w = winner(board)
    if w:
        return 1 if w == 'X' else -1
    vals = [minimax(board[:i] + player + board[i + 1:], other(player))
            for i in range(9) if board[i] == '.']
    return max(vals) if player == 'X' else min(vals)

def count_positions():
    """Boards reachable from the empty board, play stopping at a
    win or a full board, the empty board included."""
    seen, stack = set(), [('.' * 9, 'X')]
    while stack:
        board, player = stack.pop()
        if board in seen:
            continue
        seen.add(board)
        if winner(board) or '.' not in board:
            continue
        for i in range(9):
            if board[i] == '.':
                stack.append((board[:i] + player + board[i + 1:], other(player)))
    return len(seen)
```
- **count_positions does not stop at a win**: first fails test 8 (fails 8). Symptom: test 8 gets `6046`.
```python
from functools import lru_cache

LINES = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6),
         (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]

def winner(board):
    """'X' or 'O' if a line is full of one mark, else None."""
    for a, b, c in LINES:
        if board[a] != '.' and board[a] == board[b] == board[c]:
            return board[a]
    return None

def other(player):
    return 'O' if player == 'X' else 'X'

def nim_losing(n):
    """True when the player to move with n sticks loses
    against best play (take 1, 2 or 3; last stick wins)."""
    # every move leaves the opponent in a winning position
    return all(not nim_losing(n - k) for k in (1, 2, 3) if k <= n)

@lru_cache(maxsize=None)
def minimax(board, player):
    """Value for X with best play: 1 X wins, -1 O wins, 0 draw.
    board is a 9-character string of 'X', 'O' and '.'."""
    w = winner(board)
    if w:
        return 1 if w == 'X' else -1
    if '.' not in board:
        return 0
    vals = [minimax(board[:i] + player + board[i + 1:], other(player))
            for i in range(9) if board[i] == '.']
    return max(vals) if player == 'X' else min(vals)

def count_positions():
    """Boards reachable from the empty board, play stopping at a
    win or a full board, the empty board included."""
    seen, stack = set(), [('.' * 9, 'X')]
    while stack:
        board, player = stack.pop()
        if board in seen:
            continue
        seen.add(board)
        if '.' not in board:
            continue
        for i in range(9):
            if board[i] == '.':
                stack.append((board[:i] + player + board[i + 1:], other(player)))
    return len(seen)
```
- **nim_losing with takes of 1 or 2 only**: first fails test 1 (fails 1, 2). Symptom: test 1 gets `[0, 3, 6, 9, 12, 15, 18, 21, 24, 27]`.
```python
from functools import lru_cache

LINES = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6),
         (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]

def winner(board):
    """'X' or 'O' if a line is full of one mark, else None."""
    for a, b, c in LINES:
        if board[a] != '.' and board[a] == board[b] == board[c]:
            return board[a]
    return None

def other(player):
    return 'O' if player == 'X' else 'X'

def nim_losing(n):
    """True when the player to move with n sticks loses
    against best play (take 1, 2 or 3; last stick wins)."""
    # every move leaves the opponent in a winning position
    return all(not nim_losing(n - k) for k in (1, 2) if k <= n)

@lru_cache(maxsize=None)
def minimax(board, player):
    """Value for X with best play: 1 X wins, -1 O wins, 0 draw.
    board is a 9-character string of 'X', 'O' and '.'."""
    w = winner(board)
    if w:
        return 1 if w == 'X' else -1
    if '.' not in board:
        return 0
    vals = [minimax(board[:i] + player + board[i + 1:], other(player))
            for i in range(9) if board[i] == '.']
    return max(vals) if player == 'X' else min(vals)

def count_positions():
    """Boards reachable from the empty board, play stopping at a
    win or a full board, the empty board included."""
    seen, stack = set(), [('.' * 9, 'X')]
    while stack:
        board, player = stack.pop()
        if board in seen:
            continue
        seen.add(board)
        if winner(board) or '.' not in board:
            continue
        for i in range(9):
            if board[i] == '.':
                stack.append((board[:i] + player + board[i + 1:], other(player)))
    return len(seen)
```
- **nim_losing memoised (a correct, faster variant)**: SURVIVES every hidden test.
```python
from functools import lru_cache

LINES = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6),
         (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]

def winner(board):
    """'X' or 'O' if a line is full of one mark, else None."""
    for a, b, c in LINES:
        if board[a] != '.' and board[a] == board[b] == board[c]:
            return board[a]
    return None

def other(player):
    return 'O' if player == 'X' else 'X'

@lru_cache(maxsize=None)
def nim_losing(n):
    """True when the player to move with n sticks loses
    against best play (take 1, 2 or 3; last stick wins)."""
    # every move leaves the opponent in a winning position
    return all(not nim_losing(n - k) for k in (1, 2, 3) if k <= n)

@lru_cache(maxsize=None)
def minimax(board, player):
    """Value for X with best play: 1 X wins, -1 O wins, 0 draw.
    board is a 9-character string of 'X', 'O' and '.'."""
    w = winner(board)
    if w:
        return 1 if w == 'X' else -1
    if '.' not in board:
        return 0
    vals = [minimax(board[:i] + player + board[i + 1:], other(player))
            for i in range(9) if board[i] == '.']
    return max(vals) if player == 'X' else min(vals)

def count_positions():
    """Boards reachable from the empty board, play stopping at a
    win or a full board, the empty board included."""
    seen, stack = set(), [('.' * 9, 'X')]
    while stack:
        board, player = stack.pop()
        if board in seen:
            continue
        seen.add(board)
        if winner(board) or '.' not in board:
            continue
        for i in range(9):
            if board[i] == '.':
                stack.append((board[:i] + player + board[i + 1:], other(player)))
    return len(seen)
```
### l18-pruning-the-tree.json `.screens[4].widget` (7 hidden tests)

- **minimax without alternating sign: the player never changes**: first fails test 1 (fails 1, 2, 4, 6). Symptom: test 1 gets `1`.
```python
LINES = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6),
         (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]

def winner(board):
    """'X' or 'O' if a line is full of one mark, else None."""
    for a, b, c in LINES:
        if board[a] != '.' and board[a] == board[b] == board[c]:
            return board[a]
    return None

def other(player):
    return 'O' if player == 'X' else 'X'

def alphabeta(board, player, alpha, beta):
    """Minimax value for X with pruning, moves tried in cell order
    0 to 8. Return (value, nodes), counting every call."""
    w = winner(board)
    if w:
        return (1 if w == 'X' else -1), 1
    if '.' not in board:
        return 0, 1
    nodes = 1
    best = -2 if player == 'X' else 2
    for i in range(9):
        if board[i] != '.':
            continue
        child = board[:i] + player + board[i + 1:]
        v, n = alphabeta(child, player, alpha, beta)
        nodes += n
        if player == 'X':
            best = max(best, v)
            alpha = max(alpha, best)
        else:
            best = min(best, v)
            beta = min(beta, best)
        if alpha >= beta:
            break      # the other player will never allow this line
    return best, nodes
```
- **cut only when alpha > beta (strict; still exact)**: first fails test 2 (fails 2, 6). Symptom: test 2 gets `False`.
```python
LINES = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6),
         (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]

def winner(board):
    """'X' or 'O' if a line is full of one mark, else None."""
    for a, b, c in LINES:
        if board[a] != '.' and board[a] == board[b] == board[c]:
            return board[a]
    return None

def other(player):
    return 'O' if player == 'X' else 'X'

def alphabeta(board, player, alpha, beta):
    """Minimax value for X with pruning, moves tried in cell order
    0 to 8. Return (value, nodes), counting every call."""
    w = winner(board)
    if w:
        return (1 if w == 'X' else -1), 1
    if '.' not in board:
        return 0, 1
    nodes = 1
    best = -2 if player == 'X' else 2
    for i in range(9):
        if board[i] != '.':
            continue
        child = board[:i] + player + board[i + 1:]
        v, n = alphabeta(child, other(player), alpha, beta)
        nodes += n
        if player == 'X':
            best = max(best, v)
            alpha = max(alpha, best)
        else:
            best = min(best, v)
            beta = min(beta, best)
        if alpha > beta:
            break      # the other player will never allow this line
    return best, nodes
```
- **the window is not passed down: children always get (-2, 2)**: first fails test 2 (fails 2, 6). Symptom: test 2 gets `False`.
```python
LINES = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6),
         (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]

def winner(board):
    """'X' or 'O' if a line is full of one mark, else None."""
    for a, b, c in LINES:
        if board[a] != '.' and board[a] == board[b] == board[c]:
            return board[a]
    return None

def other(player):
    return 'O' if player == 'X' else 'X'

def alphabeta(board, player, alpha, beta):
    """Minimax value for X with pruning, moves tried in cell order
    0 to 8. Return (value, nodes), counting every call."""
    w = winner(board)
    if w:
        return (1 if w == 'X' else -1), 1
    if '.' not in board:
        return 0, 1
    nodes = 1
    best = -2 if player == 'X' else 2
    for i in range(9):
        if board[i] != '.':
            continue
        child = board[:i] + player + board[i + 1:]
        v, n = alphabeta(child, other(player), -2, 2)
        nodes += n
        if player == 'X':
            best = max(best, v)
            alpha = max(alpha, best)
        else:
            best = min(best, v)
            beta = min(beta, best)
        if alpha >= beta:
            break      # the other player will never allow this line
    return best, nodes
```
- **a table keyed on the board alone stores bounded values as exact**: first fails test 3 (fails 3, 7). Symptom: test 3 gets `1`.
```python
LINES = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6),
         (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]

def winner(board):
    """'X' or 'O' if a line is full of one mark, else None."""
    for a, b, c in LINES:
        if board[a] != '.' and board[a] == board[b] == board[c]:
            return board[a]
    return None

def other(player):
    return 'O' if player == 'X' else 'X'

_T = {}
def alphabeta(board, player, alpha, beta):
    """Minimax value for X with pruning, moves tried in cell order
    0 to 8. Return (value, nodes), counting every call."""
    if board in _T:
        return _T[board], 1
    w = winner(board)
    if w:
        return (1 if w == 'X' else -1), 1
    if '.' not in board:
        return 0, 1
    nodes = 1
    best = -2 if player == 'X' else 2
    for i in range(9):
        if board[i] != '.':
            continue
        child = board[:i] + player + board[i + 1:]
        v, n = alphabeta(child, other(player), alpha, beta)
        nodes += n
        if player == 'X':
            best = max(best, v)
            alpha = max(alpha, best)
        else:
            best = min(best, v)
            beta = min(beta, best)
        if alpha >= beta:
            break      # the other player will never allow this line
    _T[board] = best
    return best, nodes
```
- **terminal boards not counted as nodes**: first fails test 7 (fails 7). Symptom: test 7 gets `(0, 1)`.
```python
LINES = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6),
         (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]

def winner(board):
    """'X' or 'O' if a line is full of one mark, else None."""
    for a, b, c in LINES:
        if board[a] != '.' and board[a] == board[b] == board[c]:
            return board[a]
    return None

def other(player):
    return 'O' if player == 'X' else 'X'

def alphabeta(board, player, alpha, beta):
    """Minimax value for X with pruning, moves tried in cell order
    0 to 8. Return (value, nodes), counting every call."""
    w = winner(board)
    if w:
        return (1 if w == 'X' else -1), 0
    if '.' not in board:
        return 0, 0
    nodes = 1
    best = -2 if player == 'X' else 2
    for i in range(9):
        if board[i] != '.':
            continue
        child = board[:i] + player + board[i + 1:]
        v, n = alphabeta(child, other(player), alpha, beta)
        nodes += n
        if player == 'X':
            best = max(best, v)
            alpha = max(alpha, best)
        else:
            best = min(best, v)
            beta = min(beta, best)
        if alpha >= beta:
            break      # the other player will never allow this line
    return best, nodes
```
### l19-tree-search.json `.screens[5].widget` (7 hidden tests)

- **UCT with exploitation and exploration swapped (c on the average)**: first fails test 1 (fails 1, 2, 4). Symptom: test 1 gets `1.622587035027936`.
```python
import math
import random

LINES = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6),
         (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]

def winner(board):
    """'X' or 'O' if a line is full of one mark, else None."""
    for a, b, c in LINES:
        if board[a] != '.' and board[a] == board[b] == board[c]:
            return board[a]
    return None

def other(player):
    return 'O' if player == 'X' else 'X'

def moves(board):
    """Empty cells, or none once someone has won."""
    return [] if winner(board) else [i for i in range(9) if board[i] == '.']

def playout(board, player, rng):
    """Random moves to the end; return 'X', 'O' or None (draw)."""
    while True:
        w = winner(board)
        if w:
            return w
        ms = moves(board)
        if not ms:
            return None
        i = rng.choice(ms)
        board = board[:i] + player + board[i + 1:]
        player = other(player)

class Node:
    def __init__(self, board, player, move=None, mover=None):
        self.board, self.player = board, player   # player to move
        self.move, self.mover = move, mover       # how we got here
        self.untried = moves(board)               # in cell order
        self.children = []
        self.n, self.w = 0, 0.0                    # visits, mover's wins

def uct_score(w, n, N, c=math.sqrt(2)):
    """Average plus bonus; an unvisited child scores infinity."""
    if n == 0:
        return math.inf
    return c * w / n + math.sqrt(math.log(N) / n)

def mcts(board, player, iterations, seed, c=math.sqrt(2)):
    """Select by UCT, expand the first untried move, play out
    at random, back up; return the most visited first move."""
    rng = random.Random(seed)
    root = Node(board, player)
    for _ in range(iterations):
        node, path = root, [root]
        while not node.untried and node.children:        # select
            parent = node
            node = max(parent.children,
                       key=lambda ch: uct_score(ch.w, ch.n, parent.n, c))
            path.append(node)
        if node.untried:                                 # expand
            m = node.untried.pop(0)
            b = node.board[:m] + node.player + node.board[m + 1:]
            child = Node(b, other(node.player), m, node.player)
            node.children.append(child)
            node = child
            path.append(node)
        result = playout(node.board, node.player, rng)   # simulate
        for nd in path:                                  # back up
            nd.n += 1
            if nd.mover is not None:
                if result == nd.mover:
                    nd.w += 1.0
                elif result is None:
                    nd.w += 0.5
    return max(root.children, key=lambda ch: ch.n).move
```
- **visit counts not backed up: only the new leaf is updated**: first fails test 5 (fails 5, 6, 7). Symptom: raises ValueError: math domain error.
```python
import math
import random

LINES = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6),
         (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]

def winner(board):
    """'X' or 'O' if a line is full of one mark, else None."""
    for a, b, c in LINES:
        if board[a] != '.' and board[a] == board[b] == board[c]:
            return board[a]
    return None

def other(player):
    return 'O' if player == 'X' else 'X'

def moves(board):
    """Empty cells, or none once someone has won."""
    return [] if winner(board) else [i for i in range(9) if board[i] == '.']

def playout(board, player, rng):
    """Random moves to the end; return 'X', 'O' or None (draw)."""
    while True:
        w = winner(board)
        if w:
            return w
        ms = moves(board)
        if not ms:
            return None
        i = rng.choice(ms)
        board = board[:i] + player + board[i + 1:]
        player = other(player)

class Node:
    def __init__(self, board, player, move=None, mover=None):
        self.board, self.player = board, player   # player to move
        self.move, self.mover = move, mover       # how we got here
        self.untried = moves(board)               # in cell order
        self.children = []
        self.n, self.w = 0, 0.0                    # visits, mover's wins

def uct_score(w, n, N, c=math.sqrt(2)):
    """Average plus bonus; an unvisited child scores infinity."""
    if n == 0:
        return math.inf
    return w / n + c * math.sqrt(math.log(N) / n)

def mcts(board, player, iterations, seed, c=math.sqrt(2)):
    """Select by UCT, expand the first untried move, play out
    at random, back up; return the most visited first move."""
    rng = random.Random(seed)
    root = Node(board, player)
    for _ in range(iterations):
        node, path = root, [root]
        while not node.untried and node.children:        # select
            parent = node
            node = max(parent.children,
                       key=lambda ch: uct_score(ch.w, ch.n, parent.n, c))
            path.append(node)
        if node.untried:                                 # expand
            m = node.untried.pop(0)
            b = node.board[:m] + node.player + node.board[m + 1:]
            child = Node(b, other(node.player), m, node.player)
            node.children.append(child)
            node = child
            path.append(node)
        result = playout(node.board, node.player, rng)   # simulate
        for nd in path[-1:]:                             # back up
            nd.n += 1
            if nd.mover is not None:
                if result == nd.mover:
                    nd.w += 1.0
                elif result is None:
                    nd.w += 0.5
    return max(root.children, key=lambda ch: ch.n).move
```
- **plays the best average, not the most visited**: SURVIVES every hidden test.
```python
import math
import random

LINES = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6),
         (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]

def winner(board):
    """'X' or 'O' if a line is full of one mark, else None."""
    for a, b, c in LINES:
        if board[a] != '.' and board[a] == board[b] == board[c]:
            return board[a]
    return None

def other(player):
    return 'O' if player == 'X' else 'X'

def moves(board):
    """Empty cells, or none once someone has won."""
    return [] if winner(board) else [i for i in range(9) if board[i] == '.']

def playout(board, player, rng):
    """Random moves to the end; return 'X', 'O' or None (draw)."""
    while True:
        w = winner(board)
        if w:
            return w
        ms = moves(board)
        if not ms:
            return None
        i = rng.choice(ms)
        board = board[:i] + player + board[i + 1:]
        player = other(player)

class Node:
    def __init__(self, board, player, move=None, mover=None):
        self.board, self.player = board, player   # player to move
        self.move, self.mover = move, mover       # how we got here
        self.untried = moves(board)               # in cell order
        self.children = []
        self.n, self.w = 0, 0.0                    # visits, mover's wins

def uct_score(w, n, N, c=math.sqrt(2)):
    """Average plus bonus; an unvisited child scores infinity."""
    if n == 0:
        return math.inf
    return w / n + c * math.sqrt(math.log(N) / n)

def mcts(board, player, iterations, seed, c=math.sqrt(2)):
    """Select by UCT, expand the first untried move, play out
    at random, back up; return the most visited first move."""
    rng = random.Random(seed)
    root = Node(board, player)
    for _ in range(iterations):
        node, path = root, [root]
        while not node.untried and node.children:        # select
            parent = node
            node = max(parent.children,
                       key=lambda ch: uct_score(ch.w, ch.n, parent.n, c))
            path.append(node)
        if node.untried:                                 # expand
            m = node.untried.pop(0)
            b = node.board[:m] + node.player + node.board[m + 1:]
            child = Node(b, other(node.player), m, node.player)
            node.children.append(child)
            node = child
            path.append(node)
        result = playout(node.board, node.player, rng)   # simulate
        for nd in path:                                  # back up
            nd.n += 1
            if nd.mover is not None:
                if result == nd.mover:
                    nd.w += 1.0
                elif result is None:
                    nd.w += 0.5
    return max(root.children, key=lambda ch: ch.w / ch.n).move
```
- **draws back up as 0, not 0.5**: SURVIVES every hidden test.
```python
import math
import random

LINES = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6),
         (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]

def winner(board):
    """'X' or 'O' if a line is full of one mark, else None."""
    for a, b, c in LINES:
        if board[a] != '.' and board[a] == board[b] == board[c]:
            return board[a]
    return None

def other(player):
    return 'O' if player == 'X' else 'X'

def moves(board):
    """Empty cells, or none once someone has won."""
    return [] if winner(board) else [i for i in range(9) if board[i] == '.']

def playout(board, player, rng):
    """Random moves to the end; return 'X', 'O' or None (draw)."""
    while True:
        w = winner(board)
        if w:
            return w
        ms = moves(board)
        if not ms:
            return None
        i = rng.choice(ms)
        board = board[:i] + player + board[i + 1:]
        player = other(player)

class Node:
    def __init__(self, board, player, move=None, mover=None):
        self.board, self.player = board, player   # player to move
        self.move, self.mover = move, mover       # how we got here
        self.untried = moves(board)               # in cell order
        self.children = []
        self.n, self.w = 0, 0.0                    # visits, mover's wins

def uct_score(w, n, N, c=math.sqrt(2)):
    """Average plus bonus; an unvisited child scores infinity."""
    if n == 0:
        return math.inf
    return w / n + c * math.sqrt(math.log(N) / n)

def mcts(board, player, iterations, seed, c=math.sqrt(2)):
    """Select by UCT, expand the first untried move, play out
    at random, back up; return the most visited first move."""
    rng = random.Random(seed)
    root = Node(board, player)
    for _ in range(iterations):
        node, path = root, [root]
        while not node.untried and node.children:        # select
            parent = node
            node = max(parent.children,
                       key=lambda ch: uct_score(ch.w, ch.n, parent.n, c))
            path.append(node)
        if node.untried:                                 # expand
            m = node.untried.pop(0)
            b = node.board[:m] + node.player + node.board[m + 1:]
            child = Node(b, other(node.player), m, node.player)
            node.children.append(child)
            node = child
            path.append(node)
        result = playout(node.board, node.player, rng)   # simulate
        for nd in path:                                  # back up
            nd.n += 1
            if nd.mover is not None:
                if result == nd.mover:
                    nd.w += 1.0
    return max(root.children, key=lambda ch: ch.n).move
```
- **the parent count in UCT is the child's own n**: SURVIVES every hidden test.
```python
import math
import random

LINES = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6),
         (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]

def winner(board):
    """'X' or 'O' if a line is full of one mark, else None."""
    for a, b, c in LINES:
        if board[a] != '.' and board[a] == board[b] == board[c]:
            return board[a]
    return None

def other(player):
    return 'O' if player == 'X' else 'X'

def moves(board):
    """Empty cells, or none once someone has won."""
    return [] if winner(board) else [i for i in range(9) if board[i] == '.']

def playout(board, player, rng):
    """Random moves to the end; return 'X', 'O' or None (draw)."""
    while True:
        w = winner(board)
        if w:
            return w
        ms = moves(board)
        if not ms:
            return None
        i = rng.choice(ms)
        board = board[:i] + player + board[i + 1:]
        player = other(player)

class Node:
    def __init__(self, board, player, move=None, mover=None):
        self.board, self.player = board, player   # player to move
        self.move, self.mover = move, mover       # how we got here
        self.untried = moves(board)               # in cell order
        self.children = []
        self.n, self.w = 0, 0.0                    # visits, mover's wins

def uct_score(w, n, N, c=math.sqrt(2)):
    """Average plus bonus; an unvisited child scores infinity."""
    if n == 0:
        return math.inf
    return w / n + c * math.sqrt(math.log(N) / n)

def mcts(board, player, iterations, seed, c=math.sqrt(2)):
    """Select by UCT, expand the first untried move, play out
    at random, back up; return the most visited first move."""
    rng = random.Random(seed)
    root = Node(board, player)
    for _ in range(iterations):
        node, path = root, [root]
        while not node.untried and node.children:        # select
            parent = node
            node = max(parent.children,
                       key=lambda ch: uct_score(ch.w, ch.n, ch.n, c))
            path.append(node)
        if node.untried:                                 # expand
            m = node.untried.pop(0)
            b = node.board[:m] + node.player + node.board[m + 1:]
            child = Node(b, other(node.player), m, node.player)
            node.children.append(child)
            node = child
            path.append(node)
        result = playout(node.board, node.player, rng)   # simulate
        for nd in path:                                  # back up
            nd.n += 1
            if nd.mover is not None:
                if result == nd.mover:
                    nd.w += 1.0
                elif result is None:
                    nd.w += 0.5
    return max(root.children, key=lambda ch: ch.n).move
```
- **the c argument ignored inside the tree (fixed sqrt 2)**: SURVIVES every hidden test.
```python
import math
import random

LINES = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6),
         (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]

def winner(board):
    """'X' or 'O' if a line is full of one mark, else None."""
    for a, b, c in LINES:
        if board[a] != '.' and board[a] == board[b] == board[c]:
            return board[a]
    return None

def other(player):
    return 'O' if player == 'X' else 'X'

def moves(board):
    """Empty cells, or none once someone has won."""
    return [] if winner(board) else [i for i in range(9) if board[i] == '.']

def playout(board, player, rng):
    """Random moves to the end; return 'X', 'O' or None (draw)."""
    while True:
        w = winner(board)
        if w:
            return w
        ms = moves(board)
        if not ms:
            return None
        i = rng.choice(ms)
        board = board[:i] + player + board[i + 1:]
        player = other(player)

class Node:
    def __init__(self, board, player, move=None, mover=None):
        self.board, self.player = board, player   # player to move
        self.move, self.mover = move, mover       # how we got here
        self.untried = moves(board)               # in cell order
        self.children = []
        self.n, self.w = 0, 0.0                    # visits, mover's wins

def uct_score(w, n, N, c=math.sqrt(2)):
    """Average plus bonus; an unvisited child scores infinity."""
    if n == 0:
        return math.inf
    return w / n + c * math.sqrt(math.log(N) / n)

def mcts(board, player, iterations, seed, c=math.sqrt(2)):
    """Select by UCT, expand the first untried move, play out
    at random, back up; return the most visited first move."""
    rng = random.Random(seed)
    root = Node(board, player)
    for _ in range(iterations):
        node, path = root, [root]
        while not node.untried and node.children:        # select
            parent = node
            node = max(parent.children,
                       key=lambda ch: uct_score(ch.w, ch.n, parent.n))
            path.append(node)
        if node.untried:                                 # expand
            m = node.untried.pop(0)
            b = node.board[:m] + node.player + node.board[m + 1:]
            child = Node(b, other(node.player), m, node.player)
            node.children.append(child)
            node = child
            path.append(node)
        result = playout(node.board, node.player, rng)   # simulate
        for nd in path:                                  # back up
            nd.n += 1
            if nd.mover is not None:
                if result == nd.mover:
                    nd.w += 1.0
                elif result is None:
                    nd.w += 0.5
    return max(root.children, key=lambda ch: ch.n).move
```
### l20-self-play.json `.screens[4].widget` (5 hidden tests)

- **no exploration: eps ignored**: SURVIVES every hidden test.
```python
import random

def self_play_nim(episodes, alpha, eps, seed, top=21):
    """Q[(n, k)]: value of taking k from n for the player to move.
    Both sides use the same table."""
    rng = random.Random(seed)
    Q = {(n, k): 0.0 for n in range(1, top + 1) for k in (1, 2, 3) if k <= n}

    def takes(n):
        return [k for k in (1, 2, 3) if k <= n]

    for _ in range(episodes):
        n = rng.randint(1, top)
        while n > 0:
            if rng.random() < 0:
                k = rng.choice(takes(n))
            else:
                k = max(takes(n), key=lambda j: Q[(n, j)])   # ties: fewest sticks
            n2 = n - k
            if n2 == 0:
                target = 1.0                                   # took the last stick
            else:
                target = -max(Q[(n2, j)] for j in takes(n2))   # the opponent's best, negated
            Q[(n, k)] += alpha * (target - Q[(n, k)])
            n = n2
    return Q
```
- **the opponent's worst, negated (min for max)**: first fails test 2 (fails 2, 3, 4). Symptom: test 2 gets `False`.
```python
import random

def self_play_nim(episodes, alpha, eps, seed, top=21):
    """Q[(n, k)]: value of taking k from n for the player to move.
    Both sides use the same table."""
    rng = random.Random(seed)
    Q = {(n, k): 0.0 for n in range(1, top + 1) for k in (1, 2, 3) if k <= n}

    def takes(n):
        return [k for k in (1, 2, 3) if k <= n]

    for _ in range(episodes):
        n = rng.randint(1, top)
        while n > 0:
            if rng.random() < eps:
                k = rng.choice(takes(n))
            else:
                k = max(takes(n), key=lambda j: Q[(n, j)])   # ties: fewest sticks
            n2 = n - k
            if n2 == 0:
                target = 1.0                                   # took the last stick
            else:
                target = -min(Q[(n2, j)] for j in takes(n2))   # the opponent's best, negated
            Q[(n, k)] += alpha * (target - Q[(n, k)])
            n = n2
    return Q
```
- **greedy ties broken to the most sticks**: SURVIVES every hidden test.
```python
import random

def self_play_nim(episodes, alpha, eps, seed, top=21):
    """Q[(n, k)]: value of taking k from n for the player to move.
    Both sides use the same table."""
    rng = random.Random(seed)
    Q = {(n, k): 0.0 for n in range(1, top + 1) for k in (1, 2, 3) if k <= n}

    def takes(n):
        return [k for k in (1, 2, 3) if k <= n]

    for _ in range(episodes):
        n = rng.randint(1, top)
        while n > 0:
            if rng.random() < eps:
                k = rng.choice(takes(n))
            else:
                k = max(reversed(takes(n)), key=lambda j: Q[(n, j)])   # ties: fewest sticks
            n2 = n - k
            if n2 == 0:
                target = 1.0                                   # took the last stick
            else:
                target = -max(Q[(n2, j)] for j in takes(n2))   # the opponent's best, negated
            Q[(n, k)] += alpha * (target - Q[(n, k)])
            n = n2
    return Q
```
- **minimax without alternating sign: the target is the opponent's best, not negated**: first fails test 2 (fails 2, 3, 4). Symptom: test 2 gets `False`.
```python
import random

def self_play_nim(episodes, alpha, eps, seed, top=21):
    """Q[(n, k)]: value of taking k from n for the player to move.
    Both sides use the same table."""
    rng = random.Random(seed)
    Q = {(n, k): 0.0 for n in range(1, top + 1) for k in (1, 2, 3) if k <= n}

    def takes(n):
        return [k for k in (1, 2, 3) if k <= n]

    for _ in range(episodes):
        n = rng.randint(1, top)
        while n > 0:
            if rng.random() < eps:
                k = rng.choice(takes(n))
            else:
                k = max(takes(n), key=lambda j: Q[(n, j)])   # ties: fewest sticks
            n2 = n - k
            if n2 == 0:
                target = 1.0                                   # took the last stick
            else:
                target = max(Q[(n2, j)] for j in takes(n2))   # the opponent's best, negated
            Q[(n, k)] += alpha * (target - Q[(n, k)])
            n = n2
    return Q
```
### homework-5.json `.items[0].widget` (9 hidden tests)

- **minimax without alternating sign: the child's value is not negated**: first fails test 3 (fails 3, 4, 7, 8). Symptom: test 3 gets `5`.
```python
from functools import lru_cache

LINES = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6),
         (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]

def winner(board):
    for a, b, c in LINES:
        if board[a] != '.' and board[a] == board[b] == board[c]:
            return board[a]
    return None

@lru_cache(maxsize=None)
def value(board, player):
    """Score for the player to move: a win is worth 1 + the empty
    cells left when it happens (quicker is better), a loss minus that."""
    if winner(board):
        return -(1 + board.count('.'))   # the previous mover won
    if '.' not in board:
        return 0
    other = 'O' if player == 'X' else 'X'
    return max(value(board[:i] + player + board[i + 1:], other)
               for i in range(9) if board[i] == '.')

def best_move(board):
    player = 'X' if board.count('X') == board.count('O') else 'O'
    other = 'O' if player == 'X' else 'X'
    empty = [i for i in range(9) if board[i] == '.']
    return max(empty, key=lambda i: -value(board[:i] + player + board[i + 1:], other))
```
- **no table of seen positions**: first fails test 7 (fails 7, 8, 9). Symptom: test 7 runs out of time.
```python
from functools import lru_cache

LINES = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6),
         (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]

def winner(board):
    for a, b, c in LINES:
        if board[a] != '.' and board[a] == board[b] == board[c]:
            return board[a]
    return None

def value(board, player):
    """Score for the player to move: a win is worth 1 + the empty
    cells left when it happens (quicker is better), a loss minus that."""
    if winner(board):
        return -(1 + board.count('.'))   # the previous mover won
    if '.' not in board:
        return 0
    other = 'O' if player == 'X' else 'X'
    return max(-value(board[:i] + player + board[i + 1:], other)
               for i in range(9) if board[i] == '.')

def best_move(board):
    player = 'X' if board.count('X') == board.count('O') else 'O'
    other = 'O' if player == 'X' else 'X'
    empty = [i for i in range(9) if board[i] == '.']
    return max(empty, key=lambda i: -value(board[:i] + player + board[i + 1:], other))
```
- **a win scored by the cells filled, so slower wins score more**: first fails test 2 (fails 2). Symptom: test 2 gets `0`.
```python
from functools import lru_cache

LINES = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6),
         (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]

def winner(board):
    for a, b, c in LINES:
        if board[a] != '.' and board[a] == board[b] == board[c]:
            return board[a]
    return None

@lru_cache(maxsize=None)
def value(board, player):
    """Score for the player to move: a win is worth 1 + the empty
    cells left when it happens (quicker is better), a loss minus that."""
    if winner(board):
        return -(10 - board.count('.'))   # the previous mover won
    if '.' not in board:
        return 0
    other = 'O' if player == 'X' else 'X'
    return max(-value(board[:i] + player + board[i + 1:], other)
               for i in range(9) if board[i] == '.')

def best_move(board):
    player = 'X' if board.count('X') == board.count('O') else 'O'
    other = 'O' if player == 'X' else 'X'
    empty = [i for i in range(9) if board[i] == '.']
    return max(empty, key=lambda i: -value(board[:i] + player + board[i + 1:], other))
```
- **draw at a full board checked before the win**: SURVIVES every hidden test.
```python
from functools import lru_cache

LINES = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6),
         (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]

def winner(board):
    for a, b, c in LINES:
        if board[a] != '.' and board[a] == board[b] == board[c]:
            return board[a]
    return None

@lru_cache(maxsize=None)
def value(board, player):
    """Score for the player to move: a win is worth 1 + the empty
    cells left when it happens (quicker is better), a loss minus that."""
    if '.' not in board:
        return 0
    if winner(board):
        return -(1 + board.count('.'))
    other = 'O' if player == 'X' else 'X'
    return max(-value(board[:i] + player + board[i + 1:], other)
               for i in range(9) if board[i] == '.')

def best_move(board):
    player = 'X' if board.count('X') == board.count('O') else 'O'
    other = 'O' if player == 'X' else 'X'
    empty = [i for i in range(9) if board[i] == '.']
    return max(empty, key=lambda i: -value(board[:i] + player + board[i + 1:], other))
```
### homework-5.json `.items[1].widget` (5 hidden tests)

- **UCT with exploitation and exploration swapped (c on the average)**: SURVIVES every hidden test.
```python
import math
import random

def mcts_nim(n, iterations, seed, c=math.sqrt(2)):
    """Nim, take 1 to 3, last stick wins. Edges (pile, take) keep
    visits N and wins W for the player who took. Return the take
    from n with the most visits."""
    rng = random.Random(seed)
    N, W = {}, {}
    for _ in range(iterations):
        path, pile = [], n
        while pile > 0:                                   # select / expand
            takes = [k for k in (1, 2, 3) if k <= pile]
            new = [k for k in takes if (pile, k) not in N]
            if new:
                N[(pile, new[0])], W[(pile, new[0])] = 0, 0.0
                path.append((pile, new[0]))
                pile -= new[0]
                break
            total = sum(N[(pile, k)] for k in takes)
            k = max(takes, key=lambda j: c * W[(pile, j)] / N[(pile, j)]
                    + math.sqrt(math.log(total) / N[(pile, j)]))
            path.append((pile, k))
            pile -= k
        last = len(path) - 1                              # index of the last taker
        while pile > 0:                                   # random playout
            pile -= rng.choice([k for k in (1, 2, 3) if k <= pile])
            last += 1
        for i, edge in enumerate(path):                   # back up
            N[edge] += 1
            if (last - i) % 2 == 0:
                W[edge] += 1.0
    takes = [k for k in (1, 2, 3) if k <= n]
    return max(takes, key=lambda k: N.get((n, k), 0))
```
- **visit counts not backed up: only the last edge in the tree counts**: first fails test 3 (fails 3, 4). Symptom: test 3 gets `[1, 1, 1]`.
```python
import math
import random

def mcts_nim(n, iterations, seed, c=math.sqrt(2)):
    """Nim, take 1 to 3, last stick wins. Edges (pile, take) keep
    visits N and wins W for the player who took. Return the take
    from n with the most visits."""
    rng = random.Random(seed)
    N, W = {}, {}
    for _ in range(iterations):
        path, pile = [], n
        while pile > 0:                                   # select / expand
            takes = [k for k in (1, 2, 3) if k <= pile]
            new = [k for k in takes if (pile, k) not in N]
            if new:
                N[(pile, new[0])], W[(pile, new[0])] = 0, 0.0
                path.append((pile, new[0]))
                pile -= new[0]
                break
            total = sum(N[(pile, k)] for k in takes)
            k = max(takes, key=lambda j: W[(pile, j)] / N[(pile, j)]
                    + c * math.sqrt(math.log(total) / N[(pile, j)]))
            path.append((pile, k))
            pile -= k
        last = len(path) - 1                              # index of the last taker
        while pile > 0:                                   # random playout
            pile -= rng.choice([k for k in (1, 2, 3) if k <= pile])
            last += 1
        for i, edge in enumerate(path):                   # back up
            if i == len(path) - 1:
                N[edge] += 1
            if (last - i) % 2 == 0:
                W[edge] += 1.0
    takes = [k for k in (1, 2, 3) if k <= n]
    return max(takes, key=lambda k: N.get((n, k), 0))
```
- **plays the best average, not the most visited**: SURVIVES every hidden test.
```python
import math
import random

def mcts_nim(n, iterations, seed, c=math.sqrt(2)):
    """Nim, take 1 to 3, last stick wins. Edges (pile, take) keep
    visits N and wins W for the player who took. Return the take
    from n with the most visits."""
    rng = random.Random(seed)
    N, W = {}, {}
    for _ in range(iterations):
        path, pile = [], n
        while pile > 0:                                   # select / expand
            takes = [k for k in (1, 2, 3) if k <= pile]
            new = [k for k in takes if (pile, k) not in N]
            if new:
                N[(pile, new[0])], W[(pile, new[0])] = 0, 0.0
                path.append((pile, new[0]))
                pile -= new[0]
                break
            total = sum(N[(pile, k)] for k in takes)
            k = max(takes, key=lambda j: W[(pile, j)] / N[(pile, j)]
                    + c * math.sqrt(math.log(total) / N[(pile, j)]))
            path.append((pile, k))
            pile -= k
        last = len(path) - 1                              # index of the last taker
        while pile > 0:                                   # random playout
            pile -= rng.choice([k for k in (1, 2, 3) if k <= pile])
            last += 1
        for i, edge in enumerate(path):                   # back up
            N[edge] += 1
            if (last - i) % 2 == 0:
                W[edge] += 1.0
    takes = [k for k in (1, 2, 3) if k <= n]
    return max(takes, key=lambda k: W.get((n, k), 0) / max(N.get((n, k), 0), 1))
```
- **minimax without alternating sign: every edge on the path credited with the win**: first fails test 1 (fails 1, 3, 4). Symptom: test 1 gets `1`.
```python
import math
import random

def mcts_nim(n, iterations, seed, c=math.sqrt(2)):
    """Nim, take 1 to 3, last stick wins. Edges (pile, take) keep
    visits N and wins W for the player who took. Return the take
    from n with the most visits."""
    rng = random.Random(seed)
    N, W = {}, {}
    for _ in range(iterations):
        path, pile = [], n
        while pile > 0:                                   # select / expand
            takes = [k for k in (1, 2, 3) if k <= pile]
            new = [k for k in takes if (pile, k) not in N]
            if new:
                N[(pile, new[0])], W[(pile, new[0])] = 0, 0.0
                path.append((pile, new[0]))
                pile -= new[0]
                break
            total = sum(N[(pile, k)] for k in takes)
            k = max(takes, key=lambda j: W[(pile, j)] / N[(pile, j)]
                    + c * math.sqrt(math.log(total) / N[(pile, j)]))
            path.append((pile, k))
            pile -= k
        last = len(path) - 1                              # index of the last taker
        while pile > 0:                                   # random playout
            pile -= rng.choice([k for k in (1, 2, 3) if k <= pile])
            last += 1
        for i, edge in enumerate(path):                   # back up
            N[edge] += 1
            W[edge] += 1.0
    takes = [k for k in (1, 2, 3) if k <= n]
    return max(takes, key=lambda k: N.get((n, k), 0))
```

## Fix pass

Edits only to the L4 and L5 files in `app/content/courses/rl/` and the committed number script `docs/reports/rl-L4-numbers.py` (its own corridor learner and the stated ratio range follow the homework-4 order fix). Frozen modules untouched. Every corrected number recomputed before writing (own code, or the solution run in plain Python; the review's values matched to 1e-9 unless noted). Checks: validator 0 errors, no `[ai-mutants]` warning on rl; voice scan 0 and 0; `rl-L4-numbers.py` 253 of 253 and `rl-L5-numbers.py` 172 of 172, exit 0; `grade-all --file <f> --code --local-cdn` 0 failures on all 10 edited files, run alone; playthrough green desktop and mobile on l13 to l20, homework-4, homework-5.

Level 4
- l16 screens[7], quiz[2], summary.ideas[2] (KL leash) | fixed as proposed, with the true distinction stated: a fixed-reference penalty bounds total drift (RLHF, the form `post-train` L2 uses, with $\beta$ and $\pi_{\text{ref}}$ the model before tuning); TRPO and PPO's clip limit each step from the previous policy. Title now "A leash to a reference".
- l14 screens[6] whole-return and off-by-one reward-to-go | fixed: test 8 `reinforce_corridor(3, 0.01, 0)` = 0.6208427163388979 (recomputed; the mutants give 0.7704728562063115 and 0.6019179723323418); two mutants added (test 8).
- l16 screens[4] no zeroing and whole-episode advantage | fixed: test 8 `train_policy(64, 0)[3]` = [-0.33355627478136485, 0.03646686415318586, 0.29708941062817906]; the mutants give [-0.6422, 0.0511, 0.5911] and [-0.2715, 0.1599, 0.1116]; both added as mutants (test 8).
- homework-4 items[0] within-episode baseline | fixed: b fixed through the episode, the dials step, then b learns over the episode's returns. Tests 1 to 3 and the example re-recorded (test 1 = (0.5016899025385794, 3.144907792241889), matching the review's variant). Consequence not in the review: the variance ratio is now 0.4987 to 0.6424 on seeds 0 to 19 (the old 0.17 to 0.33 came from the action-dependent baseline), so test 4's bound moved from 0.5 to 0.7 (it still rejects b = 0, ratio 1), the explain and feedback follow, and the number script's learner was updated. Mean final p over seeds 0 to 9 is 0.5734, inside 0.53 to 0.64. Old mutant 0 reworded; the old in-loop order added as a mutant (test 1).
- homework-4 items[1] loose variance sentence | fixed with the review's first wording; `variance_with` kept (test 6 still passes).
- l15 screens[5] explain, summary.ideas[2] (actor-critic) | fixed as proposed.
- l13 screens[6] trap and screens[9] explain (two reasons) | fixed; the option text is kept short ("When every state is visible and nothing reacts") to stay under the key-length warning.
- l13 quiz[2] 'eps' why | fixed as proposed.
- l15 screens[6] update-before-use (note) | fixed: test 10 added with the review's values (recomputed), mutant added (test 10).
- l13 screens[5] min-shift softmax (note) | fixed: test 10 `softmax([0.0, 1000.0])`, mutant added (test 10).
- l16 screens[4] how "(a few seconds)" (note) | fixed to "(well under a second)". The optional leave-one-out sentence for screens[8] is declined: it adds a concept to a screen with no room for it; `post-train` can state it.
- l13, l14 (two), l15 'sign' lines (note) | fixed, one `byKey` line each.

Level 5
- l17 screens[6] trap board | fixed: `XX.OO.X..`, canvas row 3 `["X","",""]`, 'xwins' why reworded (O is to move).
- l20 screens[6] AlphaGo 2016 playouts | fixed: AlphaGo still mixed the value network with fast playouts; AlphaZero dropped them. Prose trimmed to 60 words.
- l20 screens[6] and homework-5 items[5] "this level's policy idea" | fixed to "level 4's idea" and "level 4's policy idea".
- l19 screens[2] 'noroot' and quiz[0] 'nosq' | fixed to 1.3202 and 1.7303 (recomputed: 0.666667 + 1.414214 x 0.462098; 0.75 + 1.414214 x 0.693147). Wrong distractors only; no correct answer changed.
- l17 screens[5] test 1 timing | fixed: `range(30)` became `range(20)` (expect [0, 4, 8, 12, 16]); the solution stays unmemoised, so a correct unmemoised answer still passes. Measured with `tools/code-runner.mjs`, alone, three runs: test 1 now costs 57 to 58 ms against its 9,000 ms limit (margin 155x, was 1.4x); the whole 9-test suite takes 163 ms. A wrong answer cannot get through: test 1 checks the pattern up to 19 and `nim_losing(21)` checks beyond it.
- l19 screens[5] best average, own-n parent count, draws as 0, c ignored | fixed: test 8 `[mcts('X...O....', 'X', 40, s) for s in range(4)]` = [2, 6, 6, 3] (mutants [2, 6, 7, 3], [2, 2, 3, 3], [2, 1, 1, 3]); test 9 the same with `c=0.3` = [2, 3, 6, 6] (c ignored gives [2, 6, 6, 3], which test 8 cannot see). Four mutants added.
- homework-5 items[1] swapped UCT and best average | fixed: test 6 `[mcts_nim(9, 40, s) for s in range(4)]` = [1, 3, 1, 1] (both mutants [1, 1, 1, 1]); `how` says a short seeded search pins the rule and may still miss. Two mutants added.
- l20 screens[4] greedy self-play and most-sticks ties | fixed: test 6 `self_play_nim(30, 0.5, 0.2, 0)[(5, 1)]` = 0.779296875 (mutants 0.828125 and 0.6943359375). Screens[7] 'none' why reworded as proposed. Two mutants added.
- l17 screens[5] and homework-5 items[0] full board before win | fixed: l17 test 9 `minimax('XXOXXOOO.', 'X')` = 1; homework-5 test 10 `_after('OX......X', best_move('OX......X'))` = 0 (mutant 1). One mutant each.
- l18 screens[4] how (note) | fixed: names the `alpha >= beta` cut.
- l17 screens[7] depth wording (note) | fixed.
- l18 screens[8] 'all' and screens[6] 'three' (note) | fixed: "Hedge B has 10 scenarios"; 'three' given a line (the number of branches).
- l20 screens[1] 0.43 (note) | fixed: "0.43 of 200 games (0.39 in the long run)".
- homework-5 items[5] and items[3] (note) | fixed: Fan Hui and Lee Sedol and AlphaZero's opponents; "about twice the square root of the work".

Shared code and briefs
- `rl_ops_l4.py` (no finding) | none needed.
- `docs/briefs/rl.md` shared-files bullet (note) | deferred: it is the main session's file, not a content file.

Counts: 28 findings (7 errors, 11 warnings, 10 notes): 27 fixed (one in part: the optional l16 leave-one-out sentence is declined), 1 deferred (the brief bullet), none disputed. Graded answers changed: no correct numeric or choice answer; l19 two wrong-value distractors; homework-4 `train_corridor` expected outputs (tests 1 to 3, the example, test 4's bound) and l17 test 1's expected list.
