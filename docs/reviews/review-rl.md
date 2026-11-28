# rl (Reinforcement learning) L1 to L3: second-reader findings

Scope: every file in `app/content/courses/rl/` at 47218c36 (lessons l1 to l12, `review-1` to `-3`, `homework-1` to `-3`, `problems-1` to `-3`).
Method: ran `docs/reports/rl-L1-numbers.py`, `-L2-`, `-L3-` with the venv (359, 252 and 207 checks, exit 0; they rebuild every agent and the grid independently and check values at JSON paths, so they check rather than restate); `grade-all.mjs --file <f> --code --local-cdn <pkgs>` on all 21 files (0 failures, every solution passes, every starter fails); every code widget's solution re-run in CPython by my own harness against its hidden tests with 62 hand-written wrong solutions (list with whole sources in the appendix); every stated number recomputed with my own code (own gridworld, value and policy iteration, Q-learning, SARSA on the cliff, TD and MC on the random walk, the four bandit agents over seeds 0 to 199, Beta integrals by quadrature), and every distractor's value derived from its `why`; tolerance overlaps scanned (none); `voice-scan.py 35` (0 over 35 words, 0 explanations over three sentences) plus an em-dash, exclamation and American-spelling grep (none).
Format: `path | screen/item | severity | what is wrong | fix`. Severity: error = wrong number, false claim or wrong grading; warning = weak test, loose claim or teaching issue; note = style.

Counts: 7 errors, 13 warnings, 12 notes.

## Level 1 (Bandits)

- app/content/courses/rl/review-1.json | items[7] wrong 'swap' (0.35) | error | The why "You added the fills to the second parameter" gives Beta(3, 17), mean 0.15. 0.35 is 7/20, the second parameter over the sum. | Value 0.15 with the current why, or keep 0.35 with why "You took the second parameter over the sum, 7/20."
- app/content/courses/rl/l2-exploring-at-random.json | screens[0] wrong 'all-lost' (60) | warning | The why "You counted each random order as a lost fill" gives 100 lost fills; 60 is 100 x 0.60, charging each random order C's whole fill chance. | Why: "You charged each random order C's whole fill chance, 0.60. It loses only the gap to C on average."
- app/content/courses/rl/l2-exploring-at-random.json, l4-sampling-beliefs.json | l2 screens[1] (ε = 0: 56.0) against l2 screens[5], l4 screens[6] and [7], review-1 items[8], homework-1 items[5] (greedy: 61.8) | warning | The same agent is quoted at two levels. ε = 0 and plain greedy differ only in the extra `rng.random()` draw, so the gap is seed noise: my reruns give 56.0 ± 4.2 and 61.8 ± 4.4 (standard errors over 200 seeds). A learner sees "greedy" at 56 on one screen and 62 on the next. 61.8 also equals the l2 screens[4] answer (the sum of 1/√t), a coincidence that invites confusion. | Add to l2 screens[1] explain: "The ε = 0 line is plain greedy with a different random stream; over 200 seeds its 56.0 and greedy's 61.8 differ by noise."
- app/content/courses/rl/l1-which-machine.json | screens[5] code `run_greedy` | warning | The hidden tests cannot see the update rule the screen teaches. A constant step `Q[a] += 0.1 * (r - Q[a])` passes all 7 tests: greedy locks onto the first arm that wins, and any update that keeps Q above 0 makes the same choices. | Return `(total, n, Q)` and test Q exactly on one seed (seed 1 ends with Q_A = 0.449), or add a test where two arms both hold positive estimates (for example `ps = [0.9, 0.9]`).
- app/content/courses/rl/l3-optimism.json | screens[6] prose | note | "three strategies stand as below": the rows are arms of one UCB1 agent, not strategies. | "the three arms stand as below".
- app/content/courses/rl/l3-optimism.json | summary.ideas[2] | note | "on venues 0.05 apart it beat epsilon-greedy only after about 40,000 pulls" states a 20-seed result on these venues as a rule for any arms 0.05 apart. | "On these venues, in 20 seeded runs, it overtook epsilon-greedy only between 40,000 and 50,000 pulls."
- app/content/courses/rl/l4-sampling-beliefs.json | screens[7] option 'luck' why | note | "All four agents ran on the same 200 seeds. The gap is not luck." Shared seeds do not give shared random streams; the reason is the size of the gap against its noise. | "Over 200 seeds greedy's 61.8 against Thompson's 20.8 is about ten standard errors apart."

## Level 2 (MDPs and value iteration)

- app/content/courses/rl/l8-improving-a-policy.json | screens[0] prose | error | "the policy 'always move U' has the values shown, all negative": the canvas shows +0.1505 at row 1, column 4, where a slip R reaches the +1. | "all negative except row 1, column 4".
- app/content/courses/rl/l7-value-iteration.json | screens[4] wrong 'bound' (131) | error | The why says "That is the guarantee from 0.9^k", but 0.9^k ≤ 10^-6 needs k = 132 (l6 screens[5] keys 131 as the round-down slip), and the dashed bound on the change, 0.96 x 0.9^(k-1), also first drops below 10^-6 at sweep 132. | Value 132.
- app/content/courses/rl/l7-value-iteration.json | screens[5] wrong 'keep-all' (3.65) | error | The why "You averaged the six rolls and 3.15 as seven numbers" gives (21 + 3.15)/7 = 3.45. | Value 3.45.
- app/content/courses/rl/l6-what-a-policy-is-worth.json | screens[9] explain | warning | "The limit costs about £4, so a wider limit is worth up to that much to this desk." £3.93 is the gap between starting flat and starting at the limit. A rule that never reached the limit would be worth 4/0.05 = £80 from flat, £18.69 more than £61.31. | "Starting at the limit costs about £4 against starting flat. Never hitting it would be worth £80, so the limit costs £18.69 from flat."
- app/content/courses/rl/l8-improving-a-policy.json | screens[5] prose and explain | warning | "so the loop cannot flip between tied moves" and "Keeping a tied action stops the loop from swapping U and R for ever on the deterministic grid": without the keep rule (first best in U, R, D, L within 1e-9, or a strict arg-max) policy iteration still stops, after 6 evaluations against 5. | "Keeping a tied action guarantees the loop stops whatever the tie rule. Here it also saves one evaluation, 5 against 6."
- app/content/courses/rl/l5-states-and-rewards.json | screens[6] trap | warning | The trap repeats screen 4's sum with one step fewer, keyed on the same two slips (no step cost, discounting the first reward) that screen 4 already keys. Nothing new is trapped. | Trap a path with a bump into the wall (the agent stays and still pays 0.04), or one that ends in the pit, which learners often score as 0.
- app/content/courses/rl/l7-value-iteration.json | screens[4] canvas | note | The dashed line is labelled "bound 0.96 x 0.9^(k-1)", but 0.96 is the deterministic grid's first change; the slippery grid's own bound starts at 0.76. It holds, loosely, and it coincides with the deterministic changes. | Label it "bound (deterministic changes follow it exactly)", or draw 0.76 x 0.9^(k-1) for the slippery curve.
- app/content/courses/rl/l6-what-a-policy-is-worth.json | screens[7] code `evaluate_policy` | note | Every hidden test uses γ = 0.9, so a solve with 0.9 written in place of `gamma` passes. | Add one test at another discount, e.g. `evaluate_policy(opt, 0.1, 0.5)['r4c1']`.
- app/content/courses/rl/l7-value-iteration.json | screens[7] code `greedy_policy` | note | A tie test by exact equality (`q[a] == best`) passes, because the tied floats on this grid are equal bit for bit. Harmless here; the lesson's 1e-9 rule is right. | Optional: add a case whose tied values come from different sums.

## Level 3 (TD and Q-learning)

- app/content/courses/rl/l11-q-learning.json | screens[7] prose, feedback.correct and explain | error | "With a step cost, zero is an optimistic start, like level 1's optimistic estimates." On the deterministic grid every Q* outside the pit is at least 0.25 (V* runs from 0.3228 to 0.96), so a start at 0 is below the truth: pessimistic in level 1's sense. Untried moves win early only because tried moves fall to about −0.04 before the goal's value reaches them. (l12 screens[6] is right to call zero optimistic: there every true value is −9 or lower.) | Explain: "Zero is not optimistic here: the true values are positive. Untried moves still win early, because tried ones drop below 0 before news of the goal arrives." Drop "as in level 1" from feedback.correct.
- app/content/courses/rl/l9-learning-from-episodes.json | screens[1] option 'E' why | error | "Episode 1 already reached E twice": seed 7's first episode, C D E D E D E, reaches E three times. | "Episode 1 already reached E."
- app/content/courses/rl/l9-learning-from-episodes.json | screens[9] wrong 'pos' (1.95) | error | Dropping the losing year gives (3.2 + 0.6 + 2.0)/3 = 1.9333, or 1.45 over four years; 1.95 matches neither. | Value 1.9333.
- app/content/courses/rl/l11-q-learning.json | screens[8] explain | warning | "(Sutton and Barto, section 2.7)": the step-size conditions are equation (2.7) in section 2.5; section 2.7 is upper-confidence-bound action selection. | "(Sutton and Barto, equation 2.7)".
- app/content/courses/rl/l11-q-learning.json, homework-3.json | l11 screens[8] prose; homework-3 items[5] prompt | warning | "needed 4,400 to 15,250 episodes to match value iteration on 8 of 10 seeds" reads as convergence, but those are first-match times and the greedy policy keeps flickering. An independent run (my own slip sampling): 8 of 10 seeds first matched between 2,100 and 19,250 episodes, 2 never, and no seed matched at episode 20,000. | "first matched value iteration after 4,400 to 15,250 episodes on 8 of 10 seeds, then lost the match again; 2 seeds never matched within 20,000."
- app/content/courses/rl/l11-q-learning.json, homework-3.json | l11 screens[5] `q_update`; homework-3 items[0] | warning | No hidden test sees the terminal mask the prose asks for. Ignoring `terminal` (target `r + gamma * max Q(s2, .)` always) passes all 7 l11 tests and all 8 homework tests, because end-cell Q values are never updated and stay 0. ai-safety L1 reuses this update. | Add to l11: setup `Q = {...0.0}; Q[('r1c5', 'U')] = 0.5`, call `q_update(Q, 'r1c4', 'R', 0.96, 'r1c5', 0.1, 0.9, True)`, expect 0.096. In homework-3 the mutant behaves identically (end cells are never updated), so no test there can catch it; the l11 test is the fix.
- app/content/courses/rl/l11-q-learning.json, homework-3.json | l11 screens[5] `q_learning`; homework-3 items[0] | warning | The greedy tie rule is not pinned: breaking ties at random, or in the order L, D, R, U, passes every hidden test in both widgets. The seeded figures on screen (3 wrong cells after 50 episodes, 2,934 steps, 0.2489 at 500 episodes) depend on the U, R, D, L rule, so a learner can pass and then fail to reproduce them. This is the "greedy policy with no ties rule" bug. | Add one exact seeded test, e.g. `max(q_learning(500, 0.1, 0.2, 0)[('r4c1', a)] for a in ACTIONS)` expect 0.24894561528839818 (isclose), and the same for `learn_gridworld(500, 0)`.
- app/content/courses/rl/l11-q-learning.json | quiz[2] explain | warning | "it converges to Q* whatever exploring rule supplies the data": only if the rule keeps trying every move in every cell and the steps shrink (the lesson's own summary note says so). A greedy rule supplies data and does not converge. | "...whatever exploring rule supplies the data, as long as it keeps trying every move."
- app/content/courses/rl/review-3.json | items[5] wrong 'var' (157), tol 0 | warning | The slip gives (0.25/0.02)^2 = 156.25; a learner types 156.25 or 156 and the key never fires. | Value 156.25, tol 1.
- app/content/courses/rl/l11-q-learning.json, homework-3.json (for ai-safety L1) | l11 screens[5]; homework-3 items[0] | warning | ai-safety L1 is briefed to import "the rl course's gridworld and Q-learning helpers ... never retype" (`docs/briefs/ai-safety.md` lines 22 and 40) and cites a "Shared code files" section of `docs/briefs/rl.md` that does not exist. rl ships no module: the helpers are inline starters hard-wired to the 4 x 5 grid (`'r1c1'` names, globals `move`, `reward`, `TERMINAL`), and the episode loop `while s not in TERMINAL` has no step cap. The ai-safety world is 5 x 5 with (row, col) from 0, γ = 0.95, α = 0.5, at most 60 steps an episode, and a coin that pays for ever: its greedy policy loops, so the rl loop would never end. | Engine or brief item, not a content fix here: either ship an `rl_ops.py` with `q_learning(env, episodes, alpha, eps, seed, gamma, max_steps)` and add the "Shared code files" section to `docs/briefs/rl.md`, or change the ai-safety brief to retype the loop with a step cap. Also: the ai-safety brief calls per-cell arrows "pending engine A3"; rl already uses `state.arrows` (engine 1229).
- app/content/courses/rl/l12-safe-or-greedy.json | screens[3] explain, screens[5] explain | note | "About one walk in seven (0.1409) falls" counts only the six cliff-edge cells; S is next to the cliff too (a random R from S falls), so a whole walk falls with chance 1 − 0.975^7 = 0.162, a risk the higher route shares. | "About one walk in seven falls from those six cells."
- app/content/courses/rl/l12-safe-or-greedy.json | screens[6] prose | note | "On seeds 0 to 4, after 500 episodes...": with ε = 0 nothing random is used, so every seed gives the same run. | "With ε = 0 the run is the same for every seed: after 500 episodes both agents walk the same route."
- app/content/courses/rl/l12-safe-or-greedy.json | screens[0] canvas | note | The drawn 13-move "higher route" climbs to row 1 between columns 3 and 5; a learner may ask why not the 11-move route along row 2. It is SARSA's learned route (seeds 0 to 4). | Caption: "Green: the route SARSA learns, 13 moves."
- app/content/courses/rl/l12-safe-or-greedy.json | screens[8] widget.answer | note | Stored as 0.5999999999999996. | 0.6.
- app/content/courses/rl/l12-safe-or-greedy.json, problems-1.json | l12 screens[4] widget.how; problems-1 items[2] parts[1] explain | note | "4 a episode"; "0.008 a order". | "4 an episode"; "0.008 an order".
- app/content/courses/rl (11 code widgets: l1 s4, l2 s3 and s7, l3 s7, l5 s7, l9 s4, l10 s4, l11 s5, l12 s4, homework-1 items[0], homework-2 items[1]) | widget.how | note | "math.isclose" in prose without code formatting (read as American "math"), as in review-1.5. | `math.isclose`.

## Automated checks (no finding)

- The three brief corrections hold. UCB1 against epsilon-greedy on 0.45, 0.55, 0.60: my own agents give 37.8 ± 0.5 against 24.0 ± 1.4 at 1,000 pulls over seeds 0 to 199; over 20 seeds UCB1's mean regret is 304.7 against 299.5 at 40,000 pulls and 335.0 against 366.3 at 50,000, so it overtakes between them. Undiscounted dice: the finite games rise 3.5, 4.25, 4.6667, 4.9444, 5.1296, 5.2747 towards 6, past 4.5833, and l5 makes no claim that the discount keeps it finite. Slippery contraction: the largest change falls by a ratio of 0.465 to 0.473 over sweeps 16 to 25 (about 0.50 later), against 0.9 for the bound; the deterministic changes are exactly 0.96 x 0.9^(k-1) to sweep 7, then 0.
- Recomputed and matching: all grid value tables on screen (V* at slip 0, 0.1, 0.2, sweeps 1 to 8, "always U", the four policy-iteration frames, Q-learning frames at 0, 50, 200, 500 episodes, within 5e-5); sweep counts 8, 25, 38 and in-place 17 (24 at 1e-10); policy iteration 4 and 5 evaluations with changes 13, 5, 1; slip 0.2 at r2c4 (L 0.2255, U 0.1961); step cost 0 at r3c5 (D 0.3670); Q-learning optimal on 50 of 50 seeds at 200 and 500 episodes, 2,934.46 steps, 0.3228 after 2,000 episodes (seeds 0 to 49 within 1.8e-5); fixed start 10, 4, 1, 0 untouched cells; cliff SARSA −20.03 and Q-learning −31.34, SARSA ahead on all 20 seeds, routes 13 and 9; TD and MC RMS curves (0.0581, 0.1098, 0.1588, 0.1853 at 25; 0.0553, 0.0867 at 100; α = 0.5 0.1382 and 0.1528; 0.0625 over seeds 0 to 19); decaying TD 0.0305; MC within 0.0087 over 3,000 episodes; seed 7 episodes; P(A beats B) 0.6921, 0.8007, 0.5276 by quadrature, 0.69605 by 20,000 seeded draws; greedy lock-ins 127 of 200; ε curves 56.0, 40.6, 24.0, 30.0; optimistic greedy 27.9; small-bonus UCB 18.3; Thompson 20.8; seed 12 hook 7, 3, 5.
- Hidden tests reject the classic bugs where the lesson teaches them: SARSA-style bootstrapping in Q-learning (l11 test 2, homework-3 test 2), Q-learning in place of SARSA and the reverse (l12 tests 1 and 4), in-place value iteration where the lesson asks for synchronous sweeps (l7 test 1), UCB without the bonus (l3 test 1, homework-1 test 1), single arg-max where ties are taught (l7 test 7, homework-2 test 2, l8 tests 2 and 6), rewards in place of returns (l9 test 3), missing terminal mask in TD and SARSA (l10 test 2 crashes on `V[None]`, l12 test 2). The exceptions are the l11 and homework-3 terminal mask and tie rule, and l1 `run_greedy`'s update rule, listed above.
- Tolerances: no distractor overlaps its answer or another distractor. Seeded results are stated as seeded results except l3 summary.ideas[2] (above).
- No re-teaching of `markov` or `graphs-dp`: first-step analysis and backward induction are cited by name and used, not rebuilt.

## Appendix: wrong solutions tried, per code widget

For ENGINE-BACKLOG 1263. Each entry gives the whole source, the 1-based hidden tests it fails (the first is the `test` field for a `mutants` entry) and a symptom. Entries marked SURVIVES pass every hidden test: they are the test gaps above, not mutants to paste until a test is added. Results are from CPython 3 with the widget's `prelude`; grade-all in Pyodide should agree, since every case is deterministic or seeded with `random.Random`.

### homework-1.json `.items[0].widget` (7 hidden tests)
- **UCB with no bonus**: first fails test 1 (fails 1, 2, 3, 6). Symptom: The ucb agent ranks by mean alone.
```python
import math
import random

def bandit_league(ps, T, seeds):
    """Mean regret of epsilon-greedy (0.1), UCB1 and Thompson sampling over the same seeds."""
    k = len(ps)
    best = max(ps)

    def pull(p, rng):
        return 1 if rng.random() < p else 0

    def league_regret(n):
        return sum(c * (best - p) for c, p in zip(n, ps))

    def eps_greedy(seed):
        rng = random.Random(seed)
        Q, n = [0.0] * k, [0] * k
        for _ in range(T):
            if rng.random() < 0.1:
                a = rng.randrange(k)
            else:
                m = max(Q)
                a = rng.choice([i for i in range(k) if Q[i] == m])
            r = pull(ps[a], rng)
            n[a] += 1
            Q[a] += (r - Q[a]) / n[a]
        return n

    def ucb(seed):
        rng = random.Random(seed)
        Q, n = [0.0] * k, [0] * k
        for t in range(1, T + 1):
            s = [math.inf if n[i] == 0 else Q[i] for i in range(k)]
            a = s.index(max(s))
            r = pull(ps[a], rng)
            n[a] += 1
            Q[a] += (r - Q[a]) / n[a]
        return n

    def thompson(seed):
        rng = random.Random(seed)
        w, l = [0] * k, [0] * k
        for _ in range(T):
            d = [rng.betavariate(1 + w[i], 1 + l[i]) for i in range(k)]
            a = d.index(max(d))
            if pull(ps[a], rng):
                w[a] += 1
            else:
                l[a] += 1
        return [w[i] + l[i] for i in range(k)]

    out = {}
    for name, agent in [('eps', eps_greedy), ('ucb', ucb), ('thompson', thompson)]:
        out[name] = sum(league_regret(agent(s)) for s in seeds) / len(seeds)
    return out
```
- **regret from rewards**: first fails test 1 (fails 1, 2, 3). Symptom: Thompson regret uses wins (rewards), not pull counts.
```python
import math
import random

def bandit_league(ps, T, seeds):
    """Mean regret of epsilon-greedy (0.1), UCB1 and Thompson sampling over the same seeds."""
    k = len(ps)
    best = max(ps)

    def pull(p, rng):
        return 1 if rng.random() < p else 0

    def league_regret(n):
        return sum(c * (best - p) for c, p in zip(n, ps))

    def eps_greedy(seed):
        rng = random.Random(seed)
        Q, n = [0.0] * k, [0] * k
        for _ in range(T):
            if rng.random() < 0.1:
                a = rng.randrange(k)
            else:
                m = max(Q)
                a = rng.choice([i for i in range(k) if Q[i] == m])
            r = pull(ps[a], rng)
            n[a] += 1
            Q[a] += (r - Q[a]) / n[a]
        return n

    def ucb(seed):
        rng = random.Random(seed)
        Q, n = [0.0] * k, [0] * k
        for t in range(1, T + 1):
            s = [math.inf if n[i] == 0 else Q[i] + math.sqrt(2 * math.log(t) / n[i]) for i in range(k)]
            a = s.index(max(s))
            r = pull(ps[a], rng)
            n[a] += 1
            Q[a] += (r - Q[a]) / n[a]
        return n

    def thompson(seed):
        rng = random.Random(seed)
        w, l = [0] * k, [0] * k
        for _ in range(T):
            d = [rng.betavariate(1 + w[i], 1 + l[i]) for i in range(k)]
            a = d.index(max(d))
            if pull(ps[a], rng):
                w[a] += 1
            else:
                l[a] += 1
        return [w[i] for i in range(k)]

    out = {}
    for name, agent in [('eps', eps_greedy), ('ucb', ucb), ('thompson', thompson)]:
        out[name] = sum(league_regret(agent(s)) for s in seeds) / len(seeds)
    return out
```

### homework-1.json `.items[1].widget` (5 hidden tests)
- **counts reward before the switch**: first fails test 1 (fails 1, 2, 3, 4). Symptom: Returns the total reward, not the reward after the switch.
```python
import random

def run_drift(before, after, switch, T, alpha, seed):
    """Epsilon-greedy (0.1) on arms whose win chances are `before` for pulls 1 to switch and `after` from then on.
    alpha=None uses sample means; otherwise a constant step. Returns the reward collected after the switch."""
    rng = random.Random(seed)
    k = len(before)
    Q, n = [0.0] * k, [0] * k
    late = 0
    for t in range(1, T + 1):
        ps = before if t <= switch else after
        if rng.random() < 0.1:
            a = rng.randrange(k)
        else:
            m = max(Q)
            a = rng.choice([i for i in range(k) if Q[i] == m])
        r = 1 if rng.random() < ps[a] else 0
        n[a] += 1
        step = 1 / n[a] if alpha is None else alpha
        Q[a] += step * (r - Q[a])
        late += r
    return late
```
- **alpha ignored**: first fails test 1 (fails 1, 3, 5). Symptom: Always uses the sample mean.
```python
import random

def run_drift(before, after, switch, T, alpha, seed):
    """Epsilon-greedy (0.1) on arms whose win chances are `before` for pulls 1 to switch and `after` from then on.
    alpha=None uses sample means; otherwise a constant step. Returns the reward collected after the switch."""
    rng = random.Random(seed)
    k = len(before)
    Q, n = [0.0] * k, [0] * k
    late = 0
    for t in range(1, T + 1):
        ps = before if t <= switch else after
        if rng.random() < 0.1:
            a = rng.randrange(k)
        else:
            m = max(Q)
            a = rng.choice([i for i in range(k) if Q[i] == m])
        r = 1 if rng.random() < ps[a] else 0
        n[a] += 1
        step = 1 / n[a]
        Q[a] += step * (r - Q[a])
        if t > switch:
            late += r
    return late
```

### homework-2.json `.items[0].widget` (9 hidden tests)
- **single arg-max**: first fails test 2 (fails 2, 5). Symptom: One best action per state.
```python
import numpy as np

def solve_mdp(P, R, gamma):
    """P[a, s, t] and R[a, s, t] as NumPy arrays. Return (values, policy):
    values[s] optimal, policy[s] the set of best action indices."""
    P, R = np.asarray(P, float), np.asarray(R, float)
    expected = (P * R).sum(axis=2)          # [a, s]: expected reward of a in s
    V = np.zeros(P.shape[1])
    while True:
        Q = expected + gamma * P @ V        # [a, s]
        new = Q.max(axis=0)
        done = np.max(np.abs(new - V)) < 1e-12
        V = new
        if done:
            break
    Q = expected + gamma * P @ V
    best = Q.max(axis=0)
    policy = [{int(np.argmax(Q[:, s]))} for s in range(P.shape[1])]
    return V.tolist(), policy
```
- **reward summed, not expected**: first fails test 1 (fails 1, 3, 4). Symptom: Uses R.sum(axis=2) instead of (P * R).sum(axis=2).
```python
import numpy as np

def solve_mdp(P, R, gamma):
    """P[a, s, t] and R[a, s, t] as NumPy arrays. Return (values, policy):
    values[s] optimal, policy[s] the set of best action indices."""
    P, R = np.asarray(P, float), np.asarray(R, float)
    expected = R.sum(axis=2)
    V = np.zeros(P.shape[1])
    while True:
        Q = expected + gamma * P @ V        # [a, s]
        new = Q.max(axis=0)
        done = np.max(np.abs(new - V)) < 1e-12
        V = new
        if done:
            break
    Q = expected + gamma * P @ V
    best = Q.max(axis=0)
    policy = [set(int(a) for a in np.flatnonzero(Q[:, s] > best[s] - 1e-9)) for s in range(P.shape[1])]
    return V.tolist(), policy
```

### homework-2.json `.items[1].widget` (5 hidden tests)
- **bound from the last change**: first fails test 2 (fails 2). Symptom: Uses the last sweep's change, not the first.
```python
import numpy as np

def vi_with_bound(P, R, gamma, k):
    """k sweeps from V = 0. Return (V_k, bound) with bound = gamma**k * max|V_1 - V_0| / (1 - gamma)."""
    P, R = np.asarray(P, float), np.asarray(R, float)
    expected = (P * R).sum(axis=2)
    V = np.zeros(P.shape[1])
    first = None
    for i in range(k):
        new = (expected + gamma * P @ V).max(axis=0)
        first = np.max(np.abs(new - V))
        V = new
    return V.tolist(), gamma ** k * (first or 0.0) / (1 - gamma)
```
- **gamma^(k-1)**: first fails test 1 (fails 1, 2). Symptom: Bound uses gamma^(k - 1).
```python
import numpy as np

def vi_with_bound(P, R, gamma, k):
    """k sweeps from V = 0. Return (V_k, bound) with bound = gamma**k * max|V_1 - V_0| / (1 - gamma)."""
    P, R = np.asarray(P, float), np.asarray(R, float)
    expected = (P * R).sum(axis=2)
    V = np.zeros(P.shape[1])
    first = None
    for i in range(k):
        new = (expected + gamma * P @ V).max(axis=0)
        if first is None:
            first = np.max(np.abs(new - V))
        V = new
    return V.tolist(), gamma ** (k - 1) * (first or 0.0) / (1 - gamma)
```

### homework-3.json `.items[0].widget` (8 hidden tests)
- **bootstraps with the action taken**: first fails test 2 (fails 2, 3, 4, 5, 6). Symptom: Target uses Q(t, a), not the max.
```python
import random

def learn_gridworld(episodes, seed):
    """Q-learning on the deterministic course gridworld. Return Q as {(cell, action): value}."""
    wall, ends = 'r2c3', {'r1c5': 1.0, 'r2c5': -1.0}
    cells = [f'r{r}c{c}' for r in range(1, 5) for c in range(1, 6) if f'r{r}c{c}' != wall]
    open_cells = [s for s in cells if s not in ends]
    moves = {'U': (-1, 0), 'R': (0, 1), 'D': (1, 0), 'L': (0, -1)}

    def move(s, a):
        r, c = int(s[1]) + moves[a][0], int(s[3]) + moves[a][1]
        t = f'r{r}c{c}'
        return t if 1 <= r <= 4 and 1 <= c <= 5 and t != wall else s

    rng = random.Random(seed)
    Q = {(s, a): 0.0 for s in cells for a in 'URDL'}
    for _ in range(episodes):
        s = rng.choice(open_cells)
        while s not in ends:
            if rng.random() < 0.2:
                a = rng.choice('URDL')
            else:
                a = max('URDL', key=lambda b: Q[(s, b)])
            t = move(s, a)
            r = ends.get(t, 0.0) - 0.04
            target = r if t in ends else r + 0.9 * Q[(t, a)]
            Q[(s, a)] += 0.1 * (target - Q[(s, a)])
            s = t
    return Q
```
- **true on-policy SARSA**: first fails test 5 (fails 5, 6). Symptom: Chooses a2 first and bootstraps with it.
```python
import random

def learn_gridworld(episodes, seed):
    """Q-learning on the deterministic course gridworld. Return Q as {(cell, action): value}."""
    wall, ends = 'r2c3', {'r1c5': 1.0, 'r2c5': -1.0}
    cells = [f'r{r}c{c}' for r in range(1, 5) for c in range(1, 6) if f'r{r}c{c}' != wall]
    open_cells = [s for s in cells if s not in ends]
    moves = {'U': (-1, 0), 'R': (0, 1), 'D': (1, 0), 'L': (0, -1)}

    def move(s, a):
        r, c = int(s[1]) + moves[a][0], int(s[3]) + moves[a][1]
        t = f'r{r}c{c}'
        return t if 1 <= r <= 4 and 1 <= c <= 5 and t != wall else s

    rng = random.Random(seed)
    Q = {(s, a): 0.0 for s in cells for a in 'URDL'}
    def choose(s):
        return rng.choice('URDL') if rng.random() < 0.2 else max('URDL', key=lambda b: Q[(s, b)])

    for _ in range(episodes):
        s = rng.choice(open_cells)
        a = choose(s)
        while s not in ends:
            t = move(s, a)
            r = ends.get(t, 0.0) - 0.04
            if t in ends:
                Q[(s, a)] += 0.1 * (r - Q[(s, a)])
                break
            a2 = choose(t)
            Q[(s, a)] += 0.1 * (r + 0.9 * Q[(t, a2)] - Q[(s, a)])
            s, a = t, a2
    return Q
```
- **no step cost**: first fails test 3 (fails 3, 5, 6, 8). Symptom: Moves are free.
```python
import random

def learn_gridworld(episodes, seed):
    """Q-learning on the deterministic course gridworld. Return Q as {(cell, action): value}."""
    wall, ends = 'r2c3', {'r1c5': 1.0, 'r2c5': -1.0}
    cells = [f'r{r}c{c}' for r in range(1, 5) for c in range(1, 6) if f'r{r}c{c}' != wall]
    open_cells = [s for s in cells if s not in ends]
    moves = {'U': (-1, 0), 'R': (0, 1), 'D': (1, 0), 'L': (0, -1)}

    def move(s, a):
        r, c = int(s[1]) + moves[a][0], int(s[3]) + moves[a][1]
        t = f'r{r}c{c}'
        return t if 1 <= r <= 4 and 1 <= c <= 5 and t != wall else s

    rng = random.Random(seed)
    Q = {(s, a): 0.0 for s in cells for a in 'URDL'}
    for _ in range(episodes):
        s = rng.choice(open_cells)
        while s not in ends:
            if rng.random() < 0.2:
                a = rng.choice('URDL')
            else:
                a = max('URDL', key=lambda b: Q[(s, b)])
            t = move(s, a)
            r = ends.get(t, 0.0)
            target = r if t in ends else r + 0.9 * max(Q[(t, b)] for b in 'URDL')
            Q[(s, a)] += 0.1 * (target - Q[(s, a)])
            s = t
    return Q
```
- **no terminal mask (SURVIVES)**: passes every hidden test. Symptom: Bootstraps from end cells, whose Q is never updated.
```python
import random

def learn_gridworld(episodes, seed):
    """Q-learning on the deterministic course gridworld. Return Q as {(cell, action): value}."""
    wall, ends = 'r2c3', {'r1c5': 1.0, 'r2c5': -1.0}
    cells = [f'r{r}c{c}' for r in range(1, 5) for c in range(1, 6) if f'r{r}c{c}' != wall]
    open_cells = [s for s in cells if s not in ends]
    moves = {'U': (-1, 0), 'R': (0, 1), 'D': (1, 0), 'L': (0, -1)}

    def move(s, a):
        r, c = int(s[1]) + moves[a][0], int(s[3]) + moves[a][1]
        t = f'r{r}c{c}'
        return t if 1 <= r <= 4 and 1 <= c <= 5 and t != wall else s

    rng = random.Random(seed)
    Q = {(s, a): 0.0 for s in cells for a in 'URDL'}
    for _ in range(episodes):
        s = rng.choice(open_cells)
        while s not in ends:
            if rng.random() < 0.2:
                a = rng.choice('URDL')
            else:
                a = max('URDL', key=lambda b: Q[(s, b)])
            t = move(s, a)
            r = ends.get(t, 0.0) - 0.04
            target = r + 0.9 * max(Q[(t, b)] for b in 'URDL')
            Q[(s, a)] += 0.1 * (target - Q[(s, a)])
            s = t
    return Q
```
- **random tie-break (SURVIVES)**: passes every hidden test. Symptom: Ignores the U, R, D, L tie order the prose asks for.
```python
import random

def learn_gridworld(episodes, seed):
    """Q-learning on the deterministic course gridworld. Return Q as {(cell, action): value}."""
    wall, ends = 'r2c3', {'r1c5': 1.0, 'r2c5': -1.0}
    cells = [f'r{r}c{c}' for r in range(1, 5) for c in range(1, 6) if f'r{r}c{c}' != wall]
    open_cells = [s for s in cells if s not in ends]
    moves = {'U': (-1, 0), 'R': (0, 1), 'D': (1, 0), 'L': (0, -1)}

    def move(s, a):
        r, c = int(s[1]) + moves[a][0], int(s[3]) + moves[a][1]
        t = f'r{r}c{c}'
        return t if 1 <= r <= 4 and 1 <= c <= 5 and t != wall else s

    rng = random.Random(seed)
    Q = {(s, a): 0.0 for s in cells for a in 'URDL'}
    for _ in range(episodes):
        s = rng.choice(open_cells)
        while s not in ends:
            if rng.random() < 0.2:
                a = rng.choice('URDL')
            else:
                m = max(Q[(s, b)] for b in 'URDL')
                a = rng.choice([b for b in 'URDL' if Q[(s, b)] == m])
            t = move(s, a)
            r = ends.get(t, 0.0) - 0.04
            target = r if t in ends else r + 0.9 * max(Q[(t, b)] for b in 'URDL')
            Q[(s, a)] += 0.1 * (target - Q[(s, a)])
            s = t
    return Q
```

### homework-3.json `.items[1].widget` (4 hidden tests)
- **constant step 0.1**: first fails test 2 (fails 2, 3). Symptom: Uses alpha = 0.1, not 1/n.
```python
import random

def walk_once(rng):
    s, states, rewards = 2, [], []
    while True:
        states.append('ABCDE'[s])
        s += 1 if rng.random() < 0.5 else -1
        if s == 5:
            rewards.append(1)
            return states, rewards
        rewards.append(0)
        if s == -1:
            return states, rewards

def td0_decaying(episodes, seed):
    """TD(0) on the random walk from V = 0.5, gamma 1, step 1/n on a state's n-th update. Return [V['A'], ..., V['E']]."""
    rng = random.Random(seed)
    V = {s: 0.5 for s in 'ABCDE'}
    n = {s: 0 for s in 'ABCDE'}
    for _ in range(episodes):
        states, rewards = walk_once(rng)
        for i, s in enumerate(states):
            n[s] += 1
            last = i == len(states) - 1
            target = rewards[i] if last else rewards[i] + V[states[i + 1]]
            V[s] += 0.1 * (target - V[s])
    return [V[s] for s in 'ABCDE']
```
- **step 1/(n + 1)**: first fails test 2 (fails 2, 3). Symptom: Counts the initial 0.5 as a visit.
```python
import random

def walk_once(rng):
    s, states, rewards = 2, [], []
    while True:
        states.append('ABCDE'[s])
        s += 1 if rng.random() < 0.5 else -1
        if s == 5:
            rewards.append(1)
            return states, rewards
        rewards.append(0)
        if s == -1:
            return states, rewards

def td0_decaying(episodes, seed):
    """TD(0) on the random walk from V = 0.5, gamma 1, step 1/n on a state's n-th update. Return [V['A'], ..., V['E']]."""
    rng = random.Random(seed)
    V = {s: 0.5 for s in 'ABCDE'}
    n = {s: 0 for s in 'ABCDE'}
    for _ in range(episodes):
        states, rewards = walk_once(rng)
        for i, s in enumerate(states):
            n[s] += 1
            last = i == len(states) - 1
            target = rewards[i] if last else rewards[i] + V[states[i + 1]]
            V[s] += (target - V[s]) / (n[s] + 1)
    return [V[s] for s in 'ABCDE']
```

### l1-which-machine.json `.screens[4].widget` (8 hidden tests)
- **pull uses <=**: first fails test 1 (fails 1, 2, 3). Symptom: A pull fills when rng.random() equals p, so pull(0.0, rng) can return 1.
```python
import random

def pull(p, rng):
    """One order at a venue with fill chance p: 1 for a fill, else 0."""
    return 1 if rng.random() > p else 0

def regret(ps, pulls):
    """Expected regret of these pull counts, against always playing the best arm."""
    best = max(ps)
    return sum(n * (best - p) for n, p in zip(pulls, ps))
```
- **regret against the mean arm**: first fails test 4 (fails 4, 5, 6, 8). Symptom: Regret measured against the average arm, not the best.
```python
import random

def pull(p, rng):
    """One order at a venue with fill chance p: 1 for a fill, else 0."""
    return 1 if rng.random() < p else 0

def regret(ps, pulls):
    """Expected regret of these pull counts, against always playing the best arm."""
    best = sum(ps) / len(ps)
    return sum(n * (best - p) for n, p in zip(pulls, ps))
```

### l1-which-machine.json `.screens[5].widget` (7 hidden tests)
- **first-index tie**: first fails test 1 (fails 1, 2, 3, 4, 7). Symptom: Greedy breaks ties by the first index instead of argmax_random, so every run starts on A.
```python
import random

def pull(p, rng):
    return 1 if rng.random() < p else 0

def argmax_random(values, rng):
    """The index of a largest value; ties are broken at random."""
    best = [i for i, v in enumerate(values) if v == max(values)]
    return rng.choice(best)

def run_greedy(ps, T, seed):
    """Always play the arm with the best estimate. Return (total reward, pulls per arm)."""
    rng = random.Random(seed)
    k = len(ps)
    Q = [0.0] * k
    n = [0] * k
    total = 0
    for _ in range(T):
        a = Q.index(max(Q))
        r = pull(ps[a], rng)
        n[a] += 1
        Q[a] += (r - Q[a]) / n[a]   # old + step * error
        total += r
    return total, n
```
- **constant step instead of 1/n (SURVIVES)**: passes every hidden test. Symptom: Q[a] += 0.1 * (r - Q[a]): not the running mean.
```python
import random

def pull(p, rng):
    return 1 if rng.random() < p else 0

def argmax_random(values, rng):
    """The index of a largest value; ties are broken at random."""
    best = [i for i, v in enumerate(values) if v == max(values)]
    return rng.choice(best)

def run_greedy(ps, T, seed):
    """Always play the arm with the best estimate. Return (total reward, pulls per arm)."""
    rng = random.Random(seed)
    k = len(ps)
    Q = [0.0] * k
    n = [0] * k
    total = 0
    for _ in range(T):
        a = argmax_random(Q, rng)
        r = pull(ps[a], rng)
        n[a] += 1
        Q[a] += 0.1 * (r - Q[a])   # old + step * error
        total += r
    return total, n
```

### l10-one-step-ahead.json `.screens[4].widget` (7 hidden tests)
- **returns the new value**: first fails test 1 (fails 1, 2, 3). Symptom: td0_update returns V[s], not delta.
```python
import random

def random_walk_episode(rng):
    """Start at 'C'; step right if rng.random() < 0.5, else left. Return (states, rewards)."""
    s, states, rewards = 2, [], []
    while True:
        states.append('ABCDE'[s])
        s += 1 if rng.random() < 0.5 else -1
        if s == 5:
            rewards.append(1)
            return states, rewards
        rewards.append(0)
        if s == -1:
            return states, rewards

def td0_update(V, s, r, s2, alpha, gamma, terminal):
    """Update V[s] in place by one TD(0) step and return the TD error."""
    target = r if terminal else r + gamma * V[s2]
    delta = target - V[s]
    V[s] += alpha * delta
    return V[s]

def td0_random_walk(episodes, alpha, seed):
    """TD(0) on the random walk from V = 0.5 everywhere, gamma 1. Return [V['A'], ..., V['E']]."""
    rng = random.Random(seed)
    V = {s: 0.5 for s in 'ABCDE'}
    for _ in range(episodes):
        states, rewards = random_walk_episode(rng)
        for i, s in enumerate(states):
            last = i == len(states) - 1
            td0_update(V, s, rewards[i], None if last else states[i + 1], alpha, 1.0, last)
    return [V[s] for s in 'ABCDE']
```
- **Monte Carlo target**: first fails test 6 (fails 6). Symptom: Every step uses the final reward as its target.
```python
import random

def random_walk_episode(rng):
    """Start at 'C'; step right if rng.random() < 0.5, else left. Return (states, rewards)."""
    s, states, rewards = 2, [], []
    while True:
        states.append('ABCDE'[s])
        s += 1 if rng.random() < 0.5 else -1
        if s == 5:
            rewards.append(1)
            return states, rewards
        rewards.append(0)
        if s == -1:
            return states, rewards

def td0_update(V, s, r, s2, alpha, gamma, terminal):
    """Update V[s] in place by one TD(0) step and return the TD error."""
    target = r if terminal else r + gamma * V[s2]
    delta = target - V[s]
    V[s] += alpha * delta
    return delta

def td0_random_walk(episodes, alpha, seed):
    """TD(0) on the random walk from V = 0.5 everywhere, gamma 1. Return [V['A'], ..., V['E']]."""
    rng = random.Random(seed)
    V = {s: 0.5 for s in 'ABCDE'}
    for _ in range(episodes):
        states, rewards = random_walk_episode(rng)
        for i, s in enumerate(states):
            last = i == len(states) - 1
            td0_update(V, s, rewards[-1], None, alpha, 1.0, True)
    return [V[s] for s in 'ABCDE']
```
- **starts from 0**: first fails test 4 (fails 4). Symptom: Estimates start at 0, not 0.5.
```python
import random

def random_walk_episode(rng):
    """Start at 'C'; step right if rng.random() < 0.5, else left. Return (states, rewards)."""
    s, states, rewards = 2, [], []
    while True:
        states.append('ABCDE'[s])
        s += 1 if rng.random() < 0.5 else -1
        if s == 5:
            rewards.append(1)
            return states, rewards
        rewards.append(0)
        if s == -1:
            return states, rewards

def td0_update(V, s, r, s2, alpha, gamma, terminal):
    """Update V[s] in place by one TD(0) step and return the TD error."""
    target = r if terminal else r + gamma * V[s2]
    delta = target - V[s]
    V[s] += alpha * delta
    return delta

def td0_random_walk(episodes, alpha, seed):
    """TD(0) on the random walk from V = 0.5 everywhere, gamma 1. Return [V['A'], ..., V['E']]."""
    rng = random.Random(seed)
    V = {s: 0.0 for s in 'ABCDE'}
    for _ in range(episodes):
        states, rewards = random_walk_episode(rng)
        for i, s in enumerate(states):
            last = i == len(states) - 1
            td0_update(V, s, rewards[i], None if last else states[i + 1], alpha, 1.0, last)
    return [V[s] for s in 'ABCDE']
```

### l11-q-learning.json `.screens[5].widget` (7 hidden tests)
- **bootstraps with the action taken (SARSA-like)**: first fails test 2 (fails 2, 3, 4, 6). Symptom: Target uses Q(s2, a), not the max.
```python
import random

ROWS, COLS = 4, 5
WALL = {'r2c3'}
TERMINAL = {'r1c5': 1.0, 'r2c5': -1.0}
STEP = -0.04
MOVES = {'U': (-1, 0), 'R': (0, 1), 'D': (1, 0), 'L': (0, -1)}
SIDES = {'U': 'LR', 'D': 'LR', 'L': 'UD', 'R': 'UD'}
CELLS = [f'r{r}c{c}' for r in range(1, ROWS + 1) for c in range(1, COLS + 1)
         if f'r{r}c{c}' not in WALL]

def move(s, a):
    """The cell reached from s by action a; a wall or the edge leaves the agent at s."""
    r, c = map(int, s[1:].split('c'))
    dr, dc = MOVES[a]
    t = f'r{r + dr}c{c + dc}'
    if not (1 <= r + dr <= ROWS and 1 <= c + dc <= COLS) or t in WALL:
        return s
    return t

def reward(t):
    return TERMINAL.get(t, 0.0) + STEP

ACTIONS = 'URDL'
OPEN = [s for s in CELLS if s not in TERMINAL]

def q_update(Q, s, a, r, s2, alpha, gamma, terminal):
    """One Q-learning update of Q[(s, a)], in place; return the new value."""
    target = r if terminal else r + gamma * Q[(s2, a)]
    Q[(s, a)] += alpha * (target - Q[(s, a)])
    return Q[(s, a)]

def q_learning(episodes, alpha, eps, seed, gamma=0.9):
    """Deterministic grid. Each episode starts at rng.choice(OPEN). Each step: if rng.random() < eps,
    a = rng.choice(ACTIONS), else the first best action in the order U, R, D, L. Return Q."""
    rng = random.Random(seed)
    Q = {(s, a): 0.0 for s in CELLS for a in ACTIONS}
    for _ in range(episodes):
        s = rng.choice(OPEN)
        while s not in TERMINAL:
            if rng.random() < eps:
                a = rng.choice(ACTIONS)
            else:
                a = max(ACTIONS, key=lambda b: Q[(s, b)])
            t = move(s, a)
            q_update(Q, s, a, reward(t), t, alpha, gamma, t in TERMINAL)
            s = t
    return Q

def greedy_matches(Q, optimal_sets):
    """True if every open cell's first-best action lies in its optimal set."""
    return all(max(ACTIONS, key=lambda b: Q[(s, b)]) in optimal_sets[s] for s in OPEN)
```
- **mean of next actions**: first fails test 2 (fails 2, 3, 4, 6). Symptom: Target averages the next Q values.
```python
import random

ROWS, COLS = 4, 5
WALL = {'r2c3'}
TERMINAL = {'r1c5': 1.0, 'r2c5': -1.0}
STEP = -0.04
MOVES = {'U': (-1, 0), 'R': (0, 1), 'D': (1, 0), 'L': (0, -1)}
SIDES = {'U': 'LR', 'D': 'LR', 'L': 'UD', 'R': 'UD'}
CELLS = [f'r{r}c{c}' for r in range(1, ROWS + 1) for c in range(1, COLS + 1)
         if f'r{r}c{c}' not in WALL]

def move(s, a):
    """The cell reached from s by action a; a wall or the edge leaves the agent at s."""
    r, c = map(int, s[1:].split('c'))
    dr, dc = MOVES[a]
    t = f'r{r + dr}c{c + dc}'
    if not (1 <= r + dr <= ROWS and 1 <= c + dc <= COLS) or t in WALL:
        return s
    return t

def reward(t):
    return TERMINAL.get(t, 0.0) + STEP

ACTIONS = 'URDL'
OPEN = [s for s in CELLS if s not in TERMINAL]

def q_update(Q, s, a, r, s2, alpha, gamma, terminal):
    """One Q-learning update of Q[(s, a)], in place; return the new value."""
    target = r if terminal else r + gamma * sum(Q[(s2, b)] for b in ACTIONS) / 4
    Q[(s, a)] += alpha * (target - Q[(s, a)])
    return Q[(s, a)]

def q_learning(episodes, alpha, eps, seed, gamma=0.9):
    """Deterministic grid. Each episode starts at rng.choice(OPEN). Each step: if rng.random() < eps,
    a = rng.choice(ACTIONS), else the first best action in the order U, R, D, L. Return Q."""
    rng = random.Random(seed)
    Q = {(s, a): 0.0 for s in CELLS for a in ACTIONS}
    for _ in range(episodes):
        s = rng.choice(OPEN)
        while s not in TERMINAL:
            if rng.random() < eps:
                a = rng.choice(ACTIONS)
            else:
                a = max(ACTIONS, key=lambda b: Q[(s, b)])
            t = move(s, a)
            q_update(Q, s, a, reward(t), t, alpha, gamma, t in TERMINAL)
            s = t
    return Q

def greedy_matches(Q, optimal_sets):
    """True if every open cell's first-best action lies in its optimal set."""
    return all(max(ACTIONS, key=lambda b: Q[(s, b)]) in optimal_sets[s] for s in OPEN)
```
- **no gamma**: first fails test 2 (fails 2, 6). Symptom: Target r + max Q, undiscounted.
```python
import random

ROWS, COLS = 4, 5
WALL = {'r2c3'}
TERMINAL = {'r1c5': 1.0, 'r2c5': -1.0}
STEP = -0.04
MOVES = {'U': (-1, 0), 'R': (0, 1), 'D': (1, 0), 'L': (0, -1)}
SIDES = {'U': 'LR', 'D': 'LR', 'L': 'UD', 'R': 'UD'}
CELLS = [f'r{r}c{c}' for r in range(1, ROWS + 1) for c in range(1, COLS + 1)
         if f'r{r}c{c}' not in WALL]

def move(s, a):
    """The cell reached from s by action a; a wall or the edge leaves the agent at s."""
    r, c = map(int, s[1:].split('c'))
    dr, dc = MOVES[a]
    t = f'r{r + dr}c{c + dc}'
    if not (1 <= r + dr <= ROWS and 1 <= c + dc <= COLS) or t in WALL:
        return s
    return t

def reward(t):
    return TERMINAL.get(t, 0.0) + STEP

ACTIONS = 'URDL'
OPEN = [s for s in CELLS if s not in TERMINAL]

def q_update(Q, s, a, r, s2, alpha, gamma, terminal):
    """One Q-learning update of Q[(s, a)], in place; return the new value."""
    target = r if terminal else r + max(Q[(s2, b)] for b in ACTIONS)
    Q[(s, a)] += alpha * (target - Q[(s, a)])
    return Q[(s, a)]

def q_learning(episodes, alpha, eps, seed, gamma=0.9):
    """Deterministic grid. Each episode starts at rng.choice(OPEN). Each step: if rng.random() < eps,
    a = rng.choice(ACTIONS), else the first best action in the order U, R, D, L. Return Q."""
    rng = random.Random(seed)
    Q = {(s, a): 0.0 for s in CELLS for a in ACTIONS}
    for _ in range(episodes):
        s = rng.choice(OPEN)
        while s not in TERMINAL:
            if rng.random() < eps:
                a = rng.choice(ACTIONS)
            else:
                a = max(ACTIONS, key=lambda b: Q[(s, b)])
            t = move(s, a)
            q_update(Q, s, a, reward(t), t, alpha, gamma, t in TERMINAL)
            s = t
    return Q

def greedy_matches(Q, optimal_sets):
    """True if every open cell's first-best action lies in its optimal set."""
    return all(max(ACTIONS, key=lambda b: Q[(s, b)]) in optimal_sets[s] for s in OPEN)
```
- **reward of the cell left**: first fails test 3 (fails 3, 4, 6). Symptom: Passes reward(s) for the step.
```python
import random

ROWS, COLS = 4, 5
WALL = {'r2c3'}
TERMINAL = {'r1c5': 1.0, 'r2c5': -1.0}
STEP = -0.04
MOVES = {'U': (-1, 0), 'R': (0, 1), 'D': (1, 0), 'L': (0, -1)}
SIDES = {'U': 'LR', 'D': 'LR', 'L': 'UD', 'R': 'UD'}
CELLS = [f'r{r}c{c}' for r in range(1, ROWS + 1) for c in range(1, COLS + 1)
         if f'r{r}c{c}' not in WALL]

def move(s, a):
    """The cell reached from s by action a; a wall or the edge leaves the agent at s."""
    r, c = map(int, s[1:].split('c'))
    dr, dc = MOVES[a]
    t = f'r{r + dr}c{c + dc}'
    if not (1 <= r + dr <= ROWS and 1 <= c + dc <= COLS) or t in WALL:
        return s
    return t

def reward(t):
    return TERMINAL.get(t, 0.0) + STEP

ACTIONS = 'URDL'
OPEN = [s for s in CELLS if s not in TERMINAL]

def q_update(Q, s, a, r, s2, alpha, gamma, terminal):
    """One Q-learning update of Q[(s, a)], in place; return the new value."""
    target = r if terminal else r + gamma * max(Q[(s2, b)] for b in ACTIONS)
    Q[(s, a)] += alpha * (target - Q[(s, a)])
    return Q[(s, a)]

def q_learning(episodes, alpha, eps, seed, gamma=0.9):
    """Deterministic grid. Each episode starts at rng.choice(OPEN). Each step: if rng.random() < eps,
    a = rng.choice(ACTIONS), else the first best action in the order U, R, D, L. Return Q."""
    rng = random.Random(seed)
    Q = {(s, a): 0.0 for s in CELLS for a in ACTIONS}
    for _ in range(episodes):
        s = rng.choice(OPEN)
        while s not in TERMINAL:
            if rng.random() < eps:
                a = rng.choice(ACTIONS)
            else:
                a = max(ACTIONS, key=lambda b: Q[(s, b)])
            t = move(s, a)
            q_update(Q, s, a, reward(s), t, alpha, gamma, t in TERMINAL)
            s = t
    return Q

def greedy_matches(Q, optimal_sets):
    """True if every open cell's first-best action lies in its optimal set."""
    return all(max(ACTIONS, key=lambda b: Q[(s, b)]) in optimal_sets[s] for s in OPEN)
```
- **no terminal mask (SURVIVES)**: passes every hidden test. Symptom: Ignores `terminal`; end-cell Q stays 0 so no test sees it.
```python
import random

ROWS, COLS = 4, 5
WALL = {'r2c3'}
TERMINAL = {'r1c5': 1.0, 'r2c5': -1.0}
STEP = -0.04
MOVES = {'U': (-1, 0), 'R': (0, 1), 'D': (1, 0), 'L': (0, -1)}
SIDES = {'U': 'LR', 'D': 'LR', 'L': 'UD', 'R': 'UD'}
CELLS = [f'r{r}c{c}' for r in range(1, ROWS + 1) for c in range(1, COLS + 1)
         if f'r{r}c{c}' not in WALL]

def move(s, a):
    """The cell reached from s by action a; a wall or the edge leaves the agent at s."""
    r, c = map(int, s[1:].split('c'))
    dr, dc = MOVES[a]
    t = f'r{r + dr}c{c + dc}'
    if not (1 <= r + dr <= ROWS and 1 <= c + dc <= COLS) or t in WALL:
        return s
    return t

def reward(t):
    return TERMINAL.get(t, 0.0) + STEP

ACTIONS = 'URDL'
OPEN = [s for s in CELLS if s not in TERMINAL]

def q_update(Q, s, a, r, s2, alpha, gamma, terminal):
    """One Q-learning update of Q[(s, a)], in place; return the new value."""
    target = r + gamma * max(Q[(s2, b)] for b in ACTIONS)
    Q[(s, a)] += alpha * (target - Q[(s, a)])
    return Q[(s, a)]

def q_learning(episodes, alpha, eps, seed, gamma=0.9):
    """Deterministic grid. Each episode starts at rng.choice(OPEN). Each step: if rng.random() < eps,
    a = rng.choice(ACTIONS), else the first best action in the order U, R, D, L. Return Q."""
    rng = random.Random(seed)
    Q = {(s, a): 0.0 for s in CELLS for a in ACTIONS}
    for _ in range(episodes):
        s = rng.choice(OPEN)
        while s not in TERMINAL:
            if rng.random() < eps:
                a = rng.choice(ACTIONS)
            else:
                a = max(ACTIONS, key=lambda b: Q[(s, b)])
            t = move(s, a)
            q_update(Q, s, a, reward(t), t, alpha, gamma, t in TERMINAL)
            s = t
    return Q

def greedy_matches(Q, optimal_sets):
    """True if every open cell's first-best action lies in its optimal set."""
    return all(max(ACTIONS, key=lambda b: Q[(s, b)]) in optimal_sets[s] for s in OPEN)
```
- **random tie-break (SURVIVES)**: passes every hidden test. Symptom: Greedy ties broken at random, not U, R, D, L.
```python
import random

ROWS, COLS = 4, 5
WALL = {'r2c3'}
TERMINAL = {'r1c5': 1.0, 'r2c5': -1.0}
STEP = -0.04
MOVES = {'U': (-1, 0), 'R': (0, 1), 'D': (1, 0), 'L': (0, -1)}
SIDES = {'U': 'LR', 'D': 'LR', 'L': 'UD', 'R': 'UD'}
CELLS = [f'r{r}c{c}' for r in range(1, ROWS + 1) for c in range(1, COLS + 1)
         if f'r{r}c{c}' not in WALL]

def move(s, a):
    """The cell reached from s by action a; a wall or the edge leaves the agent at s."""
    r, c = map(int, s[1:].split('c'))
    dr, dc = MOVES[a]
    t = f'r{r + dr}c{c + dc}'
    if not (1 <= r + dr <= ROWS and 1 <= c + dc <= COLS) or t in WALL:
        return s
    return t

def reward(t):
    return TERMINAL.get(t, 0.0) + STEP

ACTIONS = 'URDL'
OPEN = [s for s in CELLS if s not in TERMINAL]

def q_update(Q, s, a, r, s2, alpha, gamma, terminal):
    """One Q-learning update of Q[(s, a)], in place; return the new value."""
    target = r if terminal else r + gamma * max(Q[(s2, b)] for b in ACTIONS)
    Q[(s, a)] += alpha * (target - Q[(s, a)])
    return Q[(s, a)]

def q_learning(episodes, alpha, eps, seed, gamma=0.9):
    """Deterministic grid. Each episode starts at rng.choice(OPEN). Each step: if rng.random() < eps,
    a = rng.choice(ACTIONS), else the first best action in the order U, R, D, L. Return Q."""
    rng = random.Random(seed)
    Q = {(s, a): 0.0 for s in CELLS for a in ACTIONS}
    for _ in range(episodes):
        s = rng.choice(OPEN)
        while s not in TERMINAL:
            if rng.random() < eps:
                a = rng.choice(ACTIONS)
            else:
                m = max(Q[(s, b)] for b in ACTIONS)
                a = rng.choice([b for b in ACTIONS if Q[(s, b)] == m])
            t = move(s, a)
            q_update(Q, s, a, reward(t), t, alpha, gamma, t in TERMINAL)
            s = t
    return Q

def greedy_matches(Q, optimal_sets):
    """True if every open cell's first-best action lies in its optimal set."""
    return all(max(ACTIONS, key=lambda b: Q[(s, b)]) in optimal_sets[s] for s in OPEN)
```
- **last-best tie order (SURVIVES)**: passes every hidden test. Symptom: Greedy ties broken in the order L, D, R, U.
```python
import random

ROWS, COLS = 4, 5
WALL = {'r2c3'}
TERMINAL = {'r1c5': 1.0, 'r2c5': -1.0}
STEP = -0.04
MOVES = {'U': (-1, 0), 'R': (0, 1), 'D': (1, 0), 'L': (0, -1)}
SIDES = {'U': 'LR', 'D': 'LR', 'L': 'UD', 'R': 'UD'}
CELLS = [f'r{r}c{c}' for r in range(1, ROWS + 1) for c in range(1, COLS + 1)
         if f'r{r}c{c}' not in WALL]

def move(s, a):
    """The cell reached from s by action a; a wall or the edge leaves the agent at s."""
    r, c = map(int, s[1:].split('c'))
    dr, dc = MOVES[a]
    t = f'r{r + dr}c{c + dc}'
    if not (1 <= r + dr <= ROWS and 1 <= c + dc <= COLS) or t in WALL:
        return s
    return t

def reward(t):
    return TERMINAL.get(t, 0.0) + STEP

ACTIONS = 'URDL'
OPEN = [s for s in CELLS if s not in TERMINAL]

def q_update(Q, s, a, r, s2, alpha, gamma, terminal):
    """One Q-learning update of Q[(s, a)], in place; return the new value."""
    target = r if terminal else r + gamma * max(Q[(s2, b)] for b in ACTIONS)
    Q[(s, a)] += alpha * (target - Q[(s, a)])
    return Q[(s, a)]

def q_learning(episodes, alpha, eps, seed, gamma=0.9):
    """Deterministic grid. Each episode starts at rng.choice(OPEN). Each step: if rng.random() < eps,
    a = rng.choice(ACTIONS), else the first best action in the order U, R, D, L. Return Q."""
    rng = random.Random(seed)
    Q = {(s, a): 0.0 for s in CELLS for a in ACTIONS}
    for _ in range(episodes):
        s = rng.choice(OPEN)
        while s not in TERMINAL:
            if rng.random() < eps:
                a = rng.choice(ACTIONS)
            else:
                a = max(ACTIONS[::-1], key=lambda b: Q[(s, b)])
            t = move(s, a)
            q_update(Q, s, a, reward(t), t, alpha, gamma, t in TERMINAL)
            s = t
    return Q

def greedy_matches(Q, optimal_sets):
    """True if every open cell's first-best action lies in its optimal set."""
    return all(max(ACTIONS, key=lambda b: Q[(s, b)]) in optimal_sets[s] for s in OPEN)
```

### l12-safe-or-greedy.json `.screens[4].widget` (7 hidden tests)
- **SARSA with max**: first fails test 1 (fails 1, 3, 4). Symptom: sarsa_update bootstraps with the max (Q-learning).
```python
import random

START, GOAL = (4, 1), (4, 8)
CLIFF = {(4, c) for c in range(2, 8)}
MOVES = {'U': (-1, 0), 'R': (0, 1), 'D': (1, 0), 'L': (0, -1)}

def cliff_step(s, a):
    """Move on the 4 by 8 grid; off the edge stays put; the cliff costs 100 and sends you to START."""
    r = min(max(s[0] + MOVES[a][0], 1), 4)
    c = min(max(s[1] + MOVES[a][1], 1), 8)
    if (r, c) in CLIFF:
        return START, -100
    return (r, c), -1

def sarsa_update(Q, s, a, r, s2, a2, alpha, gamma, terminal):
    """One SARSA update of Q[(s, a)], in place; return the new value."""
    target = r if terminal else r + gamma * max(Q[(s2, b)] for b in 'URDL')
    Q[(s, a)] += alpha * (target - Q[(s, a)])
    return Q[(s, a)]

def cliff_run(agent, episodes, seed, alpha=0.5, eps=0.1):
    """agent 'sarsa' or 'q'. Mean reward of the last 100 episodes."""
    rng = random.Random(seed)
    Q = {((r, c), a): 0.0 for r in range(1, 5) for c in range(1, 9) for a in 'URDL'}

    def choose(s):
        if rng.random() < eps:
            return rng.choice('URDL')
        return max('URDL', key=lambda b: Q[(s, b)])

    totals = []
    for _ in range(episodes):
        s, a, total = START, choose(START), 0
        while s != GOAL:
            s2, r = cliff_step(s, a)
            total += r
            if s2 == GOAL:
                Q[(s, a)] += alpha * (r - Q[(s, a)])
                break
            a2 = choose(s2)
            if agent == 'sarsa':
                sarsa_update(Q, s, a, r, s2, a2, alpha, 1.0, False)
            else:
                best = max(Q[(s2, b)] for b in 'URDL')
                Q[(s, a)] += alpha * (r + best - Q[(s, a)])
            s, a = s2, a2
        totals.append(total)
    return sum(totals[-100:]) / len(totals[-100:])
```
- **no terminal mask**: first fails test 2 (fails 2). Symptom: Ignores `terminal` (s2 is None at the goal).
```python
import random

START, GOAL = (4, 1), (4, 8)
CLIFF = {(4, c) for c in range(2, 8)}
MOVES = {'U': (-1, 0), 'R': (0, 1), 'D': (1, 0), 'L': (0, -1)}

def cliff_step(s, a):
    """Move on the 4 by 8 grid; off the edge stays put; the cliff costs 100 and sends you to START."""
    r = min(max(s[0] + MOVES[a][0], 1), 4)
    c = min(max(s[1] + MOVES[a][1], 1), 8)
    if (r, c) in CLIFF:
        return START, -100
    return (r, c), -1

def sarsa_update(Q, s, a, r, s2, a2, alpha, gamma, terminal):
    """One SARSA update of Q[(s, a)], in place; return the new value."""
    target = r + gamma * Q[(s2, a2)]
    Q[(s, a)] += alpha * (target - Q[(s, a)])
    return Q[(s, a)]

def cliff_run(agent, episodes, seed, alpha=0.5, eps=0.1):
    """agent 'sarsa' or 'q'. Mean reward of the last 100 episodes."""
    rng = random.Random(seed)
    Q = {((r, c), a): 0.0 for r in range(1, 5) for c in range(1, 9) for a in 'URDL'}

    def choose(s):
        if rng.random() < eps:
            return rng.choice('URDL')
        return max('URDL', key=lambda b: Q[(s, b)])

    totals = []
    for _ in range(episodes):
        s, a, total = START, choose(START), 0
        while s != GOAL:
            s2, r = cliff_step(s, a)
            total += r
            if s2 == GOAL:
                Q[(s, a)] += alpha * (r - Q[(s, a)])
                break
            a2 = choose(s2)
            if agent == 'sarsa':
                sarsa_update(Q, s, a, r, s2, a2, alpha, 1.0, False)
            else:
                best = max(Q[(s2, b)] for b in 'URDL')
                Q[(s, a)] += alpha * (r + best - Q[(s, a)])
            s, a = s2, a2
        totals.append(total)
    return sum(totals[-100:]) / len(totals[-100:])
```
- **Q-learning branch uses a2**: first fails test 4 (fails 4). Symptom: Both agents become SARSA.
```python
import random

START, GOAL = (4, 1), (4, 8)
CLIFF = {(4, c) for c in range(2, 8)}
MOVES = {'U': (-1, 0), 'R': (0, 1), 'D': (1, 0), 'L': (0, -1)}

def cliff_step(s, a):
    """Move on the 4 by 8 grid; off the edge stays put; the cliff costs 100 and sends you to START."""
    r = min(max(s[0] + MOVES[a][0], 1), 4)
    c = min(max(s[1] + MOVES[a][1], 1), 8)
    if (r, c) in CLIFF:
        return START, -100
    return (r, c), -1

def sarsa_update(Q, s, a, r, s2, a2, alpha, gamma, terminal):
    """One SARSA update of Q[(s, a)], in place; return the new value."""
    target = r if terminal else r + gamma * Q[(s2, a2)]
    Q[(s, a)] += alpha * (target - Q[(s, a)])
    return Q[(s, a)]

def cliff_run(agent, episodes, seed, alpha=0.5, eps=0.1):
    """agent 'sarsa' or 'q'. Mean reward of the last 100 episodes."""
    rng = random.Random(seed)
    Q = {((r, c), a): 0.0 for r in range(1, 5) for c in range(1, 9) for a in 'URDL'}

    def choose(s):
        if rng.random() < eps:
            return rng.choice('URDL')
        return max('URDL', key=lambda b: Q[(s, b)])

    totals = []
    for _ in range(episodes):
        s, a, total = START, choose(START), 0
        while s != GOAL:
            s2, r = cliff_step(s, a)
            total += r
            if s2 == GOAL:
                Q[(s, a)] += alpha * (r - Q[(s, a)])
                break
            a2 = choose(s2)
            if agent == 'sarsa':
                sarsa_update(Q, s, a, r, s2, a2, alpha, 1.0, False)
            else:
                best = Q[(s2, a2)]
                Q[(s, a)] += alpha * (r + best - Q[(s, a)])
            s, a = s2, a2
        totals.append(total)
    return sum(totals[-100:]) / len(totals[-100:])
```

### l2-exploring-at-random.json `.screens[3].widget` (8 hidden tests)
- **explore excludes the favourite**: first fails test 4 (fails 4, 5). Symptom: Random pulls skip the current best arm, so the stream and the floor change.
```python
import random

def pull(p, rng):
    return 1 if rng.random() < p else 0

def argmax_random(values, rng):
    best = [i for i, v in enumerate(values) if v == max(values)]
    return rng.choice(best)

def epsilon_greedy(ps, T, eps, seed):
    """Run epsilon-greedy for T pulls and return the total reward."""
    rng = random.Random(seed)
    k = len(ps)
    Q = [0.0] * k
    n = [0] * k
    total = 0
    for _ in range(T):
        if rng.random() < eps:
            a = rng.choice([i for i in range(k) if i != Q.index(max(Q))])
        else:
            a = argmax_random(Q, rng)       # exploit
        r = pull(ps[a], rng)
        n[a] += 1
        Q[a] += (r - Q[a]) / n[a]
        total += r
    return total

def regret_floor(ps, eps):
    """The least regret per pull that exploring at rate eps can cost."""
    return eps * (max(ps) - sum(ps) / len(ps))
```
- **floor uses the worst arm**: first fails test 6 (fails 6, 7). Symptom: Floor taken as eps times the gap to the worst arm.
```python
import random

def pull(p, rng):
    return 1 if rng.random() < p else 0

def argmax_random(values, rng):
    best = [i for i, v in enumerate(values) if v == max(values)]
    return rng.choice(best)

def epsilon_greedy(ps, T, eps, seed):
    """Run epsilon-greedy for T pulls and return the total reward."""
    rng = random.Random(seed)
    k = len(ps)
    Q = [0.0] * k
    n = [0] * k
    total = 0
    for _ in range(T):
        if rng.random() < eps:
            a = rng.randrange(k)            # explore
        else:
            a = argmax_random(Q, rng)       # exploit
        r = pull(ps[a], rng)
        n[a] += 1
        Q[a] += (r - Q[a]) / n[a]
        total += r
    return total

def regret_floor(ps, eps):
    """The least regret per pull that exploring at rate eps can cost."""
    return eps * (max(ps) - min(ps))
```
- **rng.random() skipped when exploiting at eps 0**: first fails test 3 (fails 3). Symptom: No draw when eps is 0, so the seeded stream shifts.
```python
import random

def pull(p, rng):
    return 1 if rng.random() < p else 0

def argmax_random(values, rng):
    best = [i for i, v in enumerate(values) if v == max(values)]
    return rng.choice(best)

def epsilon_greedy(ps, T, eps, seed):
    """Run epsilon-greedy for T pulls and return the total reward."""
    rng = random.Random(seed)
    k = len(ps)
    Q = [0.0] * k
    n = [0] * k
    total = 0
    for _ in range(T):
        if eps > 0 and rng.random() < eps:
            a = rng.randrange(k)            # explore
        else:
            a = argmax_random(Q, rng)       # exploit
        r = pull(ps[a], rng)
        n[a] += 1
        Q[a] += (r - Q[a]) / n[a]
        total += r
    return total

def regret_floor(ps, eps):
    """The least regret per pull that exploring at rate eps can cost."""
    return eps * (max(ps) - sum(ps) / len(ps))
```

### l2-exploring-at-random.json `.screens[7].widget` (6 hidden tests)
- **full step**: first fails test 1 (fails 1, 2, 5, 6). Symptom: Replaces the estimate by the reward.
```python
def ewma_update(q, r, alpha):
    """Move estimate q a fraction alpha of the way towards reward r."""
    return r
```
- **step towards old**: first fails test 1 (fails 1, 2, 4, 5, 6). Symptom: Sign of the error reversed.
```python
def ewma_update(q, r, alpha):
    """Move estimate q a fraction alpha of the way towards reward r."""
    return q + alpha * (q - r)
```

### l3-optimism.json `.screens[7].widget` (9 hidden tests)
- **UCB with no bonus**: first fails test 1 (fails 1, 2, 7, 8, 9). Symptom: Scores are the means alone: greedy with first-index ties.
```python
import math
import random

def pull(p, rng):
    return 1 if rng.random() < p else 0

def hoeffding_bound(n, eps):
    """One-sided bound on P(mean of n rewards in [0, 1] exceeds its value by eps)."""
    return math.exp(-2 * n * eps ** 2)

def ucb_scores(means, counts, t):
    """UCB1 scores at pull t; an arm never pulled scores infinity."""
    return [math.inf if c == 0 else m
            for m, c in zip(means, counts)]

def run_ucb(ps, T, seed):
    """Run UCB1 for T pulls. Return (total reward, pulls per arm)."""
    rng = random.Random(seed)
    k = len(ps)
    Q = [0.0] * k
    n = [0] * k
    total = 0
    for t in range(1, T + 1):
        s = ucb_scores(Q, n, t)
        a = s.index(max(s))          # ties: the lowest index
        r = pull(ps[a], rng)
        n[a] += 1
        Q[a] += (r - Q[a]) / n[a]
        total += r
    return total, n
```
- **bonus without the 2**: first fails test 1 (fails 1, 2, 7, 8, 9). Symptom: Bonus sqrt(ln t / n).
```python
import math
import random

def pull(p, rng):
    return 1 if rng.random() < p else 0

def hoeffding_bound(n, eps):
    """One-sided bound on P(mean of n rewards in [0, 1] exceeds its value by eps)."""
    return math.exp(-2 * n * eps ** 2)

def ucb_scores(means, counts, t):
    """UCB1 scores at pull t; an arm never pulled scores infinity."""
    return [math.inf if c == 0 else m + math.sqrt(math.log(t) / c)
            for m, c in zip(means, counts)]

def run_ucb(ps, T, seed):
    """Run UCB1 for T pulls. Return (total reward, pulls per arm)."""
    rng = random.Random(seed)
    k = len(ps)
    Q = [0.0] * k
    n = [0] * k
    total = 0
    for t in range(1, T + 1):
        s = ucb_scores(Q, n, t)
        a = s.index(max(s))          # ties: the lowest index
        r = pull(ps[a], rng)
        n[a] += 1
        Q[a] += (r - Q[a]) / n[a]
        total += r
    return total, n
```
- **two-sided bound**: first fails test 4 (fails 4, 5). Symptom: hoeffding_bound returns the two-sided 2 e^{-2 n eps^2}.
```python
import math
import random

def pull(p, rng):
    return 1 if rng.random() < p else 0

def hoeffding_bound(n, eps):
    """One-sided bound on P(mean of n rewards in [0, 1] exceeds its value by eps)."""
    return 2 * math.exp(-2 * n * eps ** 2)

def ucb_scores(means, counts, t):
    """UCB1 scores at pull t; an arm never pulled scores infinity."""
    return [math.inf if c == 0 else m + math.sqrt(2 * math.log(t) / c)
            for m, c in zip(means, counts)]

def run_ucb(ps, T, seed):
    """Run UCB1 for T pulls. Return (total reward, pulls per arm)."""
    rng = random.Random(seed)
    k = len(ps)
    Q = [0.0] * k
    n = [0] * k
    total = 0
    for t in range(1, T + 1):
        s = ucb_scores(Q, n, t)
        a = s.index(max(s))          # ties: the lowest index
        r = pull(ps[a], rng)
        n[a] += 1
        Q[a] += (r - Q[a]) / n[a]
        total += r
    return total, n
```
- **last index on a tie**: first fails test 7 (fails 7, 8, 9). Symptom: Ties go to the highest index.
```python
import math
import random

def pull(p, rng):
    return 1 if rng.random() < p else 0

def hoeffding_bound(n, eps):
    """One-sided bound on P(mean of n rewards in [0, 1] exceeds its value by eps)."""
    return math.exp(-2 * n * eps ** 2)

def ucb_scores(means, counts, t):
    """UCB1 scores at pull t; an arm never pulled scores infinity."""
    return [math.inf if c == 0 else m + math.sqrt(2 * math.log(t) / c)
            for m, c in zip(means, counts)]

def run_ucb(ps, T, seed):
    """Run UCB1 for T pulls. Return (total reward, pulls per arm)."""
    rng = random.Random(seed)
    k = len(ps)
    Q = [0.0] * k
    n = [0] * k
    total = 0
    for t in range(1, T + 1):
        s = ucb_scores(Q, n, t)
        a = len(s) - 1 - s[::-1].index(max(s))          # ties: the lowest index
        r = pull(ps[a], rng)
        n[a] += 1
        Q[a] += (r - Q[a]) / n[a]
        total += r
    return total, n
```

### l4-sampling-beliefs.json `.screens[4].widget` (8 hidden tests)
- **posterior swaps wins and losses**: first fails test 1 (fails 1, 2, 4). Symptom: Wins added to the second parameter.
```python
import random

def posterior(wins, losses, a=1, b=1):
    """Beta parameters after wins and losses, from a Beta(a, b) prior."""
    return (a + losses, b + wins)

def prob_a_beats_b(a1, b1, a2, b2, draws, seed):
    """Share of seeded draws in which Beta(a1, b1) exceeds Beta(a2, b2)."""
    rng = random.Random(seed)
    wins = 0
    for _ in range(draws):
        if rng.betavariate(a1, b1) > rng.betavariate(a2, b2):
            wins += 1
    return wins / draws
```
- **count not share**: first fails test 5 (fails 5, 6, 7, 8). Symptom: prob_a_beats_b returns the count of wins, not the share.
```python
import random

def posterior(wins, losses, a=1, b=1):
    """Beta parameters after wins and losses, from a Beta(a, b) prior."""
    return (a + wins, b + losses)

def prob_a_beats_b(a1, b1, a2, b2, draws, seed):
    """Share of seeded draws in which Beta(a1, b1) exceeds Beta(a2, b2)."""
    rng = random.Random(seed)
    wins = 0
    for _ in range(draws):
        if rng.betavariate(a1, b1) > rng.betavariate(a2, b2):
            wins += 1
    return wins
```

### l4-sampling-beliefs.json `.screens[5].widget` (6 hidden tests)
- **greedy on posterior means**: first fails test 1 (fails 1, 2, 3, 4). Symptom: Picks the largest posterior mean, no draws: greedy, not Thompson.
```python
import random

def pull(p, rng):
    return 1 if rng.random() < p else 0

def run_thompson(ps, T, seed):
    """Thompson sampling with Beta(1, 1) priors. Return (total reward, pulls per arm)."""
    rng = random.Random(seed)
    k = len(ps)
    wins = [0] * k
    losses = [0] * k
    total = 0
    for _ in range(T):
        draws = [(1 + wins[i]) / (2 + wins[i] + losses[i]) for i in range(k)]
        a = draws.index(max(draws))
        r = pull(ps[a], rng)
        if r:
            wins[a] += 1
        else:
            losses[a] += 1
        total += r
    return total, [w + l for w, l in zip(wins, losses)]
```
- **Beta parameters swapped**: first fails test 1 (fails 1, 2, 3, 4). Symptom: Draws from Beta(1 + losses, 1 + wins).
```python
import random

def pull(p, rng):
    return 1 if rng.random() < p else 0

def run_thompson(ps, T, seed):
    """Thompson sampling with Beta(1, 1) priors. Return (total reward, pulls per arm)."""
    rng = random.Random(seed)
    k = len(ps)
    wins = [0] * k
    losses = [0] * k
    total = 0
    for _ in range(T):
        draws = [rng.betavariate(1 + losses[i], 1 + wins[i]) for i in range(k)]
        a = draws.index(max(draws))
        r = pull(ps[a], rng)
        if r:
            wins[a] += 1
        else:
            losses[a] += 1
        total += r
    return total, [w + l for w, l in zip(wins, losses)]
```

### l5-states-and-rewards.json `.screens[7].widget` (10 hidden tests)
- **discounts the first reward**: first fails test 1 (fails 1, 2). Symptom: G = gamma r0 + gamma^2 r1 + ...
```python
ROWS, COLS = 4, 5
WALL = {'r2c3'}
TERMINAL = {'r1c5': 1.0, 'r2c5': -1.0}
STEP = -0.04
MOVES = {'U': (-1, 0), 'R': (0, 1), 'D': (1, 0), 'L': (0, -1)}
SIDES = {'U': 'LR', 'D': 'LR', 'L': 'UD', 'R': 'UD'}
CELLS = [f'r{r}c{c}' for r in range(1, ROWS + 1) for c in range(1, COLS + 1)
         if f'r{r}c{c}' not in WALL]

def move(s, a):
    """The cell reached from s by action a; a wall or the edge leaves the agent at s."""
    r, c = map(int, s[1:].split('c'))
    dr, dc = MOVES[a]
    t = f'r{r + dr}c{c + dc}'
    if not (1 <= r + dr <= ROWS and 1 <= c + dc <= COLS) or t in WALL:
        return s
    return t

def discounted_return(rewards, gamma):
    """G = rewards[0] + gamma * rewards[1] + gamma**2 * rewards[2] + ..."""
    return sum(gamma ** (k + 1) * r for k, r in enumerate(rewards))

def transition(s, a, slip):
    """{next cell: chance}; leave out moves with chance 0."""
    out = {}
    for b, p in ((a, 1 - 2 * slip), (SIDES[a][0], slip), (SIDES[a][1], slip)):
        if p > 0:
            t = move(s, b)
            out[t] = out.get(t, 0) + p
    return out

def dice_value(gamma, tol):
    """Iterate V = E[max(X, gamma * V)] from V = 0 until a step changes V by less than tol."""
    V = 0.0
    while True:
        new = sum(max(x, gamma * V) for x in range(1, 7)) / 6
        if abs(new - V) < tol:
            return new
        V = new
```
- **slips into the same cell overwrite**: first fails test 5 (fails 5). Symptom: out[t] = p, so a corner loses chance.
```python
ROWS, COLS = 4, 5
WALL = {'r2c3'}
TERMINAL = {'r1c5': 1.0, 'r2c5': -1.0}
STEP = -0.04
MOVES = {'U': (-1, 0), 'R': (0, 1), 'D': (1, 0), 'L': (0, -1)}
SIDES = {'U': 'LR', 'D': 'LR', 'L': 'UD', 'R': 'UD'}
CELLS = [f'r{r}c{c}' for r in range(1, ROWS + 1) for c in range(1, COLS + 1)
         if f'r{r}c{c}' not in WALL]

def move(s, a):
    """The cell reached from s by action a; a wall or the edge leaves the agent at s."""
    r, c = map(int, s[1:].split('c'))
    dr, dc = MOVES[a]
    t = f'r{r + dr}c{c + dc}'
    if not (1 <= r + dr <= ROWS and 1 <= c + dc <= COLS) or t in WALL:
        return s
    return t

def discounted_return(rewards, gamma):
    """G = rewards[0] + gamma * rewards[1] + gamma**2 * rewards[2] + ..."""
    return sum(gamma ** k * r for k, r in enumerate(rewards))

def transition(s, a, slip):
    """{next cell: chance}; leave out moves with chance 0."""
    out = {}
    for b, p in ((a, 1 - 2 * slip), (SIDES[a][0], slip), (SIDES[a][1], slip)):
        if p > 0:
            t = move(s, b)
            out[t] = p
    return out

def dice_value(gamma, tol):
    """Iterate V = E[max(X, gamma * V)] from V = 0 until a step changes V by less than tol."""
    V = 0.0
    while True:
        new = sum(max(x, gamma * V) for x in range(1, 7)) / 6
        if abs(new - V) < tol:
            return new
        V = new
```
- **dice discount outside the max**: first fails test 8 (fails 8, 9, 10). Symptom: V = gamma E[max(X, V)].
```python
ROWS, COLS = 4, 5
WALL = {'r2c3'}
TERMINAL = {'r1c5': 1.0, 'r2c5': -1.0}
STEP = -0.04
MOVES = {'U': (-1, 0), 'R': (0, 1), 'D': (1, 0), 'L': (0, -1)}
SIDES = {'U': 'LR', 'D': 'LR', 'L': 'UD', 'R': 'UD'}
CELLS = [f'r{r}c{c}' for r in range(1, ROWS + 1) for c in range(1, COLS + 1)
         if f'r{r}c{c}' not in WALL]

def move(s, a):
    """The cell reached from s by action a; a wall or the edge leaves the agent at s."""
    r, c = map(int, s[1:].split('c'))
    dr, dc = MOVES[a]
    t = f'r{r + dr}c{c + dc}'
    if not (1 <= r + dr <= ROWS and 1 <= c + dc <= COLS) or t in WALL:
        return s
    return t

def discounted_return(rewards, gamma):
    """G = rewards[0] + gamma * rewards[1] + gamma**2 * rewards[2] + ..."""
    return sum(gamma ** k * r for k, r in enumerate(rewards))

def transition(s, a, slip):
    """{next cell: chance}; leave out moves with chance 0."""
    out = {}
    for b, p in ((a, 1 - 2 * slip), (SIDES[a][0], slip), (SIDES[a][1], slip)):
        if p > 0:
            t = move(s, b)
            out[t] = out.get(t, 0) + p
    return out

def dice_value(gamma, tol):
    """Iterate V = E[max(X, gamma * V)] from V = 0 until a step changes V by less than tol."""
    V = 0.0
    while True:
        new = sum(gamma * max(x, V) for x in range(1, 7)) / 6
        if abs(new - V) < tol:
            return new
        V = new
```

### l6-what-a-policy-is-worth.json `.screens[7].widget` (9 hidden tests)
- **end rows absorb**: first fails test 1 (fails 1). Symptom: End cells get P[i, i] = 1, so I - gamma P changes their row.
```python
import numpy as np

ROWS, COLS = 4, 5
WALL = {'r2c3'}
TERMINAL = {'r1c5': 1.0, 'r2c5': -1.0}
STEP = -0.04
MOVES = {'U': (-1, 0), 'R': (0, 1), 'D': (1, 0), 'L': (0, -1)}
SIDES = {'U': 'LR', 'D': 'LR', 'L': 'UD', 'R': 'UD'}
CELLS = [f'r{r}c{c}' for r in range(1, ROWS + 1) for c in range(1, COLS + 1)
         if f'r{r}c{c}' not in WALL]

def move(s, a):
    """The cell reached from s by action a; a wall or the edge leaves the agent at s."""
    r, c = map(int, s[1:].split('c'))
    dr, dc = MOVES[a]
    t = f'r{r + dr}c{c + dc}'
    if not (1 <= r + dr <= ROWS and 1 <= c + dc <= COLS) or t in WALL:
        return s
    return t

def transition(s, a, slip):
    """{next cell: chance}: the intended move with 1 - 2*slip, each side move with slip."""
    out = {}
    for b, p in ((a, 1 - 2 * slip), (SIDES[a][0], slip), (SIDES[a][1], slip)):
        if p > 0:
            t = move(s, b)
            out[t] = out.get(t, 0) + p
    return out

def reward(t):
    """Reward for entering cell t: its payoff plus the step cost."""
    return TERMINAL.get(t, 0.0) + STEP

def policy_matrix(policy, slip):
    """P (19 by 19) and r (19) for a policy {cell: action}, in the order of CELLS.
    An end cell's row of P is zero and its r is 0."""
    n = len(CELLS)
    P = np.zeros((n, n))
    r = np.zeros(n)
    for i, s in enumerate(CELLS):
        if s in TERMINAL:
            P[i, i] = 1.0
            continue
        for t, p in transition(s, policy[s], slip).items():
            P[i, CELLS.index(t)] += p
            r[i] += p * reward(t)
    return P, r

def evaluate_policy(policy, slip, gamma):
    """{cell: value} from solving (I - gamma P) v = r."""
    P, r = policy_matrix(policy, slip)
    v = np.linalg.solve(np.eye(len(CELLS)) - gamma * P, r)
    return {s: float(v[i]) for i, s in enumerate(CELLS)}
```
- **reward of the start cell**: first fails test 2 (fails 2, 4, 6, 7, 8). Symptom: r[i] uses reward(s), not reward(t).
```python
import numpy as np

ROWS, COLS = 4, 5
WALL = {'r2c3'}
TERMINAL = {'r1c5': 1.0, 'r2c5': -1.0}
STEP = -0.04
MOVES = {'U': (-1, 0), 'R': (0, 1), 'D': (1, 0), 'L': (0, -1)}
SIDES = {'U': 'LR', 'D': 'LR', 'L': 'UD', 'R': 'UD'}
CELLS = [f'r{r}c{c}' for r in range(1, ROWS + 1) for c in range(1, COLS + 1)
         if f'r{r}c{c}' not in WALL]

def move(s, a):
    """The cell reached from s by action a; a wall or the edge leaves the agent at s."""
    r, c = map(int, s[1:].split('c'))
    dr, dc = MOVES[a]
    t = f'r{r + dr}c{c + dc}'
    if not (1 <= r + dr <= ROWS and 1 <= c + dc <= COLS) or t in WALL:
        return s
    return t

def transition(s, a, slip):
    """{next cell: chance}: the intended move with 1 - 2*slip, each side move with slip."""
    out = {}
    for b, p in ((a, 1 - 2 * slip), (SIDES[a][0], slip), (SIDES[a][1], slip)):
        if p > 0:
            t = move(s, b)
            out[t] = out.get(t, 0) + p
    return out

def reward(t):
    """Reward for entering cell t: its payoff plus the step cost."""
    return TERMINAL.get(t, 0.0) + STEP

def policy_matrix(policy, slip):
    """P (19 by 19) and r (19) for a policy {cell: action}, in the order of CELLS.
    An end cell's row of P is zero and its r is 0."""
    n = len(CELLS)
    P = np.zeros((n, n))
    r = np.zeros(n)
    for i, s in enumerate(CELLS):
        if s in TERMINAL:
            continue
        for t, p in transition(s, policy[s], slip).items():
            P[i, CELLS.index(t)] += p
            r[i] += p * reward(s)
    return P, r

def evaluate_policy(policy, slip, gamma):
    """{cell: value} from solving (I - gamma P) v = r."""
    P, r = policy_matrix(policy, slip)
    v = np.linalg.solve(np.eye(len(CELLS)) - gamma * P, r)
    return {s: float(v[i]) for i, s in enumerate(CELLS)}
```
- **gamma hard-coded to 0.9 (SURVIVES)**: passes every hidden test. Symptom: Ignores the gamma argument; every test uses 0.9.
```python
import numpy as np

ROWS, COLS = 4, 5
WALL = {'r2c3'}
TERMINAL = {'r1c5': 1.0, 'r2c5': -1.0}
STEP = -0.04
MOVES = {'U': (-1, 0), 'R': (0, 1), 'D': (1, 0), 'L': (0, -1)}
SIDES = {'U': 'LR', 'D': 'LR', 'L': 'UD', 'R': 'UD'}
CELLS = [f'r{r}c{c}' for r in range(1, ROWS + 1) for c in range(1, COLS + 1)
         if f'r{r}c{c}' not in WALL]

def move(s, a):
    """The cell reached from s by action a; a wall or the edge leaves the agent at s."""
    r, c = map(int, s[1:].split('c'))
    dr, dc = MOVES[a]
    t = f'r{r + dr}c{c + dc}'
    if not (1 <= r + dr <= ROWS and 1 <= c + dc <= COLS) or t in WALL:
        return s
    return t

def transition(s, a, slip):
    """{next cell: chance}: the intended move with 1 - 2*slip, each side move with slip."""
    out = {}
    for b, p in ((a, 1 - 2 * slip), (SIDES[a][0], slip), (SIDES[a][1], slip)):
        if p > 0:
            t = move(s, b)
            out[t] = out.get(t, 0) + p
    return out

def reward(t):
    """Reward for entering cell t: its payoff plus the step cost."""
    return TERMINAL.get(t, 0.0) + STEP

def policy_matrix(policy, slip):
    """P (19 by 19) and r (19) for a policy {cell: action}, in the order of CELLS.
    An end cell's row of P is zero and its r is 0."""
    n = len(CELLS)
    P = np.zeros((n, n))
    r = np.zeros(n)
    for i, s in enumerate(CELLS):
        if s in TERMINAL:
            continue
        for t, p in transition(s, policy[s], slip).items():
            P[i, CELLS.index(t)] += p
            r[i] += p * reward(t)
    return P, r

def evaluate_policy(policy, slip, gamma):
    """{cell: value} from solving (I - gamma P) v = r."""
    P, r = policy_matrix(policy, slip)
    v = np.linalg.solve(np.eye(len(CELLS)) - 0.9 * P, r)
    return {s: float(v[i]) for i, s in enumerate(CELLS)}
```

### l7-value-iteration.json `.screens[7].widget` (10 hidden tests)
- **in-place (Gauss-Seidel) sweep**: first fails test 1 (fails 1, 2, 3). Symptom: Writes each new value straight into V: 17 sweeps, not 25.
```python
ROWS, COLS = 4, 5
WALL = {'r2c3'}
TERMINAL = {'r1c5': 1.0, 'r2c5': -1.0}
STEP = -0.04
MOVES = {'U': (-1, 0), 'R': (0, 1), 'D': (1, 0), 'L': (0, -1)}
SIDES = {'U': 'LR', 'D': 'LR', 'L': 'UD', 'R': 'UD'}
CELLS = [f'r{r}c{c}' for r in range(1, ROWS + 1) for c in range(1, COLS + 1)
         if f'r{r}c{c}' not in WALL]

def move(s, a):
    """The cell reached from s by action a; a wall or the edge leaves the agent at s."""
    r, c = map(int, s[1:].split('c'))
    dr, dc = MOVES[a]
    t = f'r{r + dr}c{c + dc}'
    if not (1 <= r + dr <= ROWS and 1 <= c + dc <= COLS) or t in WALL:
        return s
    return t

def transition(s, a, slip):
    """{next cell: chance}: the intended move with 1 - 2*slip, each side move with slip."""
    out = {}
    for b, p in ((a, 1 - 2 * slip), (SIDES[a][0], slip), (SIDES[a][1], slip)):
        if p > 0:
            t = move(s, b)
            out[t] = out.get(t, 0) + p
    return out

def reward(t):
    """Reward for entering cell t: its payoff plus the step cost."""
    return TERMINAL.get(t, 0.0) + STEP

def q_value(V, s, a, slip, gamma):
    return sum(p * (reward(t) + gamma * V[t]) for t, p in transition(s, a, slip).items())

def value_iteration(slip, gamma, tol):
    """Sweep from all zeros, each new value from the previous table.
    Stop after the first sweep whose largest change is below tol. Return (values, sweeps)."""
    V = {s: 0.0 for s in CELLS}
    sweeps = 0
    while True:
        sweeps += 1
        change = 0.0
        for s in CELLS:
            nv = 0.0 if s in TERMINAL else max(q_value(V, s, a, slip, gamma) for a in 'URDL')
            change = max(change, abs(nv - V[s]))
            V[s] = nv
        if change < tol:
            return V, sweeps

def greedy_policy(values, slip, gamma):
    """{cell: set of actions whose q_value is within 1e-9 of the best} for every non-end cell."""
    out = {}
    for s in CELLS:
        if s in TERMINAL:
            continue
        q = {a: q_value(values, s, a, slip, gamma) for a in 'URDL'}
        best = max(q.values())
        out[s] = {a for a in q if q[a] > best - 1e-9}
    return out
```
- **end cells backed up**: first fails test 1 (fails 1, 2, 3, 4, 5, 6, 8, 9, 10). Symptom: End cells are not held at 0.
```python
ROWS, COLS = 4, 5
WALL = {'r2c3'}
TERMINAL = {'r1c5': 1.0, 'r2c5': -1.0}
STEP = -0.04
MOVES = {'U': (-1, 0), 'R': (0, 1), 'D': (1, 0), 'L': (0, -1)}
SIDES = {'U': 'LR', 'D': 'LR', 'L': 'UD', 'R': 'UD'}
CELLS = [f'r{r}c{c}' for r in range(1, ROWS + 1) for c in range(1, COLS + 1)
         if f'r{r}c{c}' not in WALL]

def move(s, a):
    """The cell reached from s by action a; a wall or the edge leaves the agent at s."""
    r, c = map(int, s[1:].split('c'))
    dr, dc = MOVES[a]
    t = f'r{r + dr}c{c + dc}'
    if not (1 <= r + dr <= ROWS and 1 <= c + dc <= COLS) or t in WALL:
        return s
    return t

def transition(s, a, slip):
    """{next cell: chance}: the intended move with 1 - 2*slip, each side move with slip."""
    out = {}
    for b, p in ((a, 1 - 2 * slip), (SIDES[a][0], slip), (SIDES[a][1], slip)):
        if p > 0:
            t = move(s, b)
            out[t] = out.get(t, 0) + p
    return out

def reward(t):
    """Reward for entering cell t: its payoff plus the step cost."""
    return TERMINAL.get(t, 0.0) + STEP

def q_value(V, s, a, slip, gamma):
    return sum(p * (reward(t) + gamma * V[t]) for t, p in transition(s, a, slip).items())

def value_iteration(slip, gamma, tol):
    """Sweep from all zeros, each new value from the previous table.
    Stop after the first sweep whose largest change is below tol. Return (values, sweeps)."""
    V = {s: 0.0 for s in CELLS}
    sweeps = 0
    while True:
        sweeps += 1
        new = {s: max(q_value(V, s, a, slip, gamma) for a in 'URDL')
               for s in CELLS}
        change = max(abs(new[s] - V[s]) for s in CELLS)
        V = new
        if change < tol:
            return V, sweeps

def greedy_policy(values, slip, gamma):
    """{cell: set of actions whose q_value is within 1e-9 of the best} for every non-end cell."""
    out = {}
    for s in CELLS:
        if s in TERMINAL:
            continue
        q = {a: q_value(values, s, a, slip, gamma) for a in 'URDL'}
        best = max(q.values())
        out[s] = {a for a in q if q[a] > best - 1e-9}
    return out
```
- **single arg-max**: first fails test 7 (fails 7, 8, 10). Symptom: greedy_policy keeps one best action, dropping ties.
```python
ROWS, COLS = 4, 5
WALL = {'r2c3'}
TERMINAL = {'r1c5': 1.0, 'r2c5': -1.0}
STEP = -0.04
MOVES = {'U': (-1, 0), 'R': (0, 1), 'D': (1, 0), 'L': (0, -1)}
SIDES = {'U': 'LR', 'D': 'LR', 'L': 'UD', 'R': 'UD'}
CELLS = [f'r{r}c{c}' for r in range(1, ROWS + 1) for c in range(1, COLS + 1)
         if f'r{r}c{c}' not in WALL]

def move(s, a):
    """The cell reached from s by action a; a wall or the edge leaves the agent at s."""
    r, c = map(int, s[1:].split('c'))
    dr, dc = MOVES[a]
    t = f'r{r + dr}c{c + dc}'
    if not (1 <= r + dr <= ROWS and 1 <= c + dc <= COLS) or t in WALL:
        return s
    return t

def transition(s, a, slip):
    """{next cell: chance}: the intended move with 1 - 2*slip, each side move with slip."""
    out = {}
    for b, p in ((a, 1 - 2 * slip), (SIDES[a][0], slip), (SIDES[a][1], slip)):
        if p > 0:
            t = move(s, b)
            out[t] = out.get(t, 0) + p
    return out

def reward(t):
    """Reward for entering cell t: its payoff plus the step cost."""
    return TERMINAL.get(t, 0.0) + STEP

def q_value(V, s, a, slip, gamma):
    return sum(p * (reward(t) + gamma * V[t]) for t, p in transition(s, a, slip).items())

def value_iteration(slip, gamma, tol):
    """Sweep from all zeros, each new value from the previous table.
    Stop after the first sweep whose largest change is below tol. Return (values, sweeps)."""
    V = {s: 0.0 for s in CELLS}
    sweeps = 0
    while True:
        sweeps += 1
        new = {s: 0.0 if s in TERMINAL else max(q_value(V, s, a, slip, gamma) for a in 'URDL')
               for s in CELLS}
        change = max(abs(new[s] - V[s]) for s in CELLS)
        V = new
        if change < tol:
            return V, sweeps

def greedy_policy(values, slip, gamma):
    """{cell: set of actions whose q_value is within 1e-9 of the best} for every non-end cell."""
    out = {}
    for s in CELLS:
        if s in TERMINAL:
            continue
        q = {a: q_value(values, s, a, slip, gamma) for a in 'URDL'}
        best = max(q.values())
        out[s] = {max(q, key=q.get)}
    return out
```
- **last sweep not counted**: first fails test 1 (fails 1, 2, 3). Symptom: Returns sweeps - 1.
```python
ROWS, COLS = 4, 5
WALL = {'r2c3'}
TERMINAL = {'r1c5': 1.0, 'r2c5': -1.0}
STEP = -0.04
MOVES = {'U': (-1, 0), 'R': (0, 1), 'D': (1, 0), 'L': (0, -1)}
SIDES = {'U': 'LR', 'D': 'LR', 'L': 'UD', 'R': 'UD'}
CELLS = [f'r{r}c{c}' for r in range(1, ROWS + 1) for c in range(1, COLS + 1)
         if f'r{r}c{c}' not in WALL]

def move(s, a):
    """The cell reached from s by action a; a wall or the edge leaves the agent at s."""
    r, c = map(int, s[1:].split('c'))
    dr, dc = MOVES[a]
    t = f'r{r + dr}c{c + dc}'
    if not (1 <= r + dr <= ROWS and 1 <= c + dc <= COLS) or t in WALL:
        return s
    return t

def transition(s, a, slip):
    """{next cell: chance}: the intended move with 1 - 2*slip, each side move with slip."""
    out = {}
    for b, p in ((a, 1 - 2 * slip), (SIDES[a][0], slip), (SIDES[a][1], slip)):
        if p > 0:
            t = move(s, b)
            out[t] = out.get(t, 0) + p
    return out

def reward(t):
    """Reward for entering cell t: its payoff plus the step cost."""
    return TERMINAL.get(t, 0.0) + STEP

def q_value(V, s, a, slip, gamma):
    return sum(p * (reward(t) + gamma * V[t]) for t, p in transition(s, a, slip).items())

def value_iteration(slip, gamma, tol):
    """Sweep from all zeros, each new value from the previous table.
    Stop after the first sweep whose largest change is below tol. Return (values, sweeps)."""
    V = {s: 0.0 for s in CELLS}
    sweeps = 0
    while True:
        sweeps += 1
        new = {s: 0.0 if s in TERMINAL else max(q_value(V, s, a, slip, gamma) for a in 'URDL')
               for s in CELLS}
        change = max(abs(new[s] - V[s]) for s in CELLS)
        V = new
        if change < tol:
            return V, sweeps - 1

def greedy_policy(values, slip, gamma):
    """{cell: set of actions whose q_value is within 1e-9 of the best} for every non-end cell."""
    out = {}
    for s in CELLS:
        if s in TERMINAL:
            continue
        q = {a: q_value(values, s, a, slip, gamma) for a in 'URDL'}
        best = max(q.values())
        out[s] = {a for a in q if q[a] > best - 1e-9}
    return out
```
- **exact-equality ties (SURVIVES)**: passes every hidden test. Symptom: Ties by q == best; passes because tied floats happen to be equal here.
```python
ROWS, COLS = 4, 5
WALL = {'r2c3'}
TERMINAL = {'r1c5': 1.0, 'r2c5': -1.0}
STEP = -0.04
MOVES = {'U': (-1, 0), 'R': (0, 1), 'D': (1, 0), 'L': (0, -1)}
SIDES = {'U': 'LR', 'D': 'LR', 'L': 'UD', 'R': 'UD'}
CELLS = [f'r{r}c{c}' for r in range(1, ROWS + 1) for c in range(1, COLS + 1)
         if f'r{r}c{c}' not in WALL]

def move(s, a):
    """The cell reached from s by action a; a wall or the edge leaves the agent at s."""
    r, c = map(int, s[1:].split('c'))
    dr, dc = MOVES[a]
    t = f'r{r + dr}c{c + dc}'
    if not (1 <= r + dr <= ROWS and 1 <= c + dc <= COLS) or t in WALL:
        return s
    return t

def transition(s, a, slip):
    """{next cell: chance}: the intended move with 1 - 2*slip, each side move with slip."""
    out = {}
    for b, p in ((a, 1 - 2 * slip), (SIDES[a][0], slip), (SIDES[a][1], slip)):
        if p > 0:
            t = move(s, b)
            out[t] = out.get(t, 0) + p
    return out

def reward(t):
    """Reward for entering cell t: its payoff plus the step cost."""
    return TERMINAL.get(t, 0.0) + STEP

def q_value(V, s, a, slip, gamma):
    return sum(p * (reward(t) + gamma * V[t]) for t, p in transition(s, a, slip).items())

def value_iteration(slip, gamma, tol):
    """Sweep from all zeros, each new value from the previous table.
    Stop after the first sweep whose largest change is below tol. Return (values, sweeps)."""
    V = {s: 0.0 for s in CELLS}
    sweeps = 0
    while True:
        sweeps += 1
        new = {s: 0.0 if s in TERMINAL else max(q_value(V, s, a, slip, gamma) for a in 'URDL')
               for s in CELLS}
        change = max(abs(new[s] - V[s]) for s in CELLS)
        V = new
        if change < tol:
            return V, sweeps

def greedy_policy(values, slip, gamma):
    """{cell: set of actions whose q_value is within 1e-9 of the best} for every non-end cell."""
    out = {}
    for s in CELLS:
        if s in TERMINAL:
            continue
        q = {a: q_value(values, s, a, slip, gamma) for a in 'URDL'}
        best = max(q.values())
        out[s] = {a for a in q if q[a] == best}
    return out
```

### l8-improving-a-policy.json `.screens[5].widget` (9 hidden tests)
- **no keep-on-tie rule**: first fails test 2 (fails 2, 9). Symptom: Always switches to the first best action: 6 evaluations on the deterministic grid.
```python
import numpy as np

ROWS, COLS = 4, 5
WALL = {'r2c3'}
TERMINAL = {'r1c5': 1.0, 'r2c5': -1.0}
STEP = -0.04
MOVES = {'U': (-1, 0), 'R': (0, 1), 'D': (1, 0), 'L': (0, -1)}
SIDES = {'U': 'LR', 'D': 'LR', 'L': 'UD', 'R': 'UD'}
CELLS = [f'r{r}c{c}' for r in range(1, ROWS + 1) for c in range(1, COLS + 1)
         if f'r{r}c{c}' not in WALL]

def move(s, a):
    """The cell reached from s by action a; a wall or the edge leaves the agent at s."""
    r, c = map(int, s[1:].split('c'))
    dr, dc = MOVES[a]
    t = f'r{r + dr}c{c + dc}'
    if not (1 <= r + dr <= ROWS and 1 <= c + dc <= COLS) or t in WALL:
        return s
    return t

def transition(s, a, slip):
    """{next cell: chance}: the intended move with 1 - 2*slip, each side move with slip."""
    out = {}
    for b, p in ((a, 1 - 2 * slip), (SIDES[a][0], slip), (SIDES[a][1], slip)):
        if p > 0:
            t = move(s, b)
            out[t] = out.get(t, 0) + p
    return out

def reward(t):
    """Reward for entering cell t: its payoff plus the step cost."""
    return TERMINAL.get(t, 0.0) + STEP

def q_value(V, s, a, slip, gamma):
    return sum(p * (reward(t) + gamma * V[t]) for t, p in transition(s, a, slip).items())

def evaluate_policy(policy, slip, gamma):
    n = len(CELLS)
    P, r = np.zeros((n, n)), np.zeros(n)
    for i, s in enumerate(CELLS):
        if s not in TERMINAL:
            for t, p in transition(s, policy[s], slip).items():
                P[i, CELLS.index(t)] += p
                r[i] += p * reward(t)
    v = np.linalg.solve(np.eye(n) - gamma * P, r)
    return {s: float(v[i]) for i, s in enumerate(CELLS)}

def policy_iteration(slip, gamma):
    """Start from U everywhere. Improve: keep the current action if it is within 1e-9 of the best,
    else take the first best in the order U, R, D, L. Stop when nothing changes.
    Return (values, policy, number of evaluations)."""
    policy = {s: 'U' for s in CELLS if s not in TERMINAL}
    evaluations = 0
    while True:
        V = evaluate_policy(policy, slip, gamma)
        evaluations += 1
        new = {}
        for s in policy:
            q = {a: q_value(V, s, a, slip, gamma) for a in 'URDL'}
            best = max(q.values())
            new[s] = next(a for a in 'URDL' if q[a] > best - 1e-9)
        if new == policy:
            return V, policy, evaluations
        policy = new

def same_policy(p1, p2, values, slip, gamma):
    """True if, in every non-end cell, both actions are within 1e-9 of the best q_value."""
    for s in CELLS:
        if s in TERMINAL:
            continue
        q = {a: q_value(values, s, a, slip, gamma) for a in 'URDL'}
        best = max(q.values())
        if q[p1[s]] <= best - 1e-9 or q[p2[s]] <= best - 1e-9:
            return False
    return True
```
- **strict arg-max**: first fails test 2 (fails 2). Symptom: max(q, key=q.get) with no tolerance or keep rule.
```python
import numpy as np

ROWS, COLS = 4, 5
WALL = {'r2c3'}
TERMINAL = {'r1c5': 1.0, 'r2c5': -1.0}
STEP = -0.04
MOVES = {'U': (-1, 0), 'R': (0, 1), 'D': (1, 0), 'L': (0, -1)}
SIDES = {'U': 'LR', 'D': 'LR', 'L': 'UD', 'R': 'UD'}
CELLS = [f'r{r}c{c}' for r in range(1, ROWS + 1) for c in range(1, COLS + 1)
         if f'r{r}c{c}' not in WALL]

def move(s, a):
    """The cell reached from s by action a; a wall or the edge leaves the agent at s."""
    r, c = map(int, s[1:].split('c'))
    dr, dc = MOVES[a]
    t = f'r{r + dr}c{c + dc}'
    if not (1 <= r + dr <= ROWS and 1 <= c + dc <= COLS) or t in WALL:
        return s
    return t

def transition(s, a, slip):
    """{next cell: chance}: the intended move with 1 - 2*slip, each side move with slip."""
    out = {}
    for b, p in ((a, 1 - 2 * slip), (SIDES[a][0], slip), (SIDES[a][1], slip)):
        if p > 0:
            t = move(s, b)
            out[t] = out.get(t, 0) + p
    return out

def reward(t):
    """Reward for entering cell t: its payoff plus the step cost."""
    return TERMINAL.get(t, 0.0) + STEP

def q_value(V, s, a, slip, gamma):
    return sum(p * (reward(t) + gamma * V[t]) for t, p in transition(s, a, slip).items())

def evaluate_policy(policy, slip, gamma):
    n = len(CELLS)
    P, r = np.zeros((n, n)), np.zeros(n)
    for i, s in enumerate(CELLS):
        if s not in TERMINAL:
            for t, p in transition(s, policy[s], slip).items():
                P[i, CELLS.index(t)] += p
                r[i] += p * reward(t)
    v = np.linalg.solve(np.eye(n) - gamma * P, r)
    return {s: float(v[i]) for i, s in enumerate(CELLS)}

def policy_iteration(slip, gamma):
    """Start from U everywhere. Improve: keep the current action if it is within 1e-9 of the best,
    else take the first best in the order U, R, D, L. Stop when nothing changes.
    Return (values, policy, number of evaluations)."""
    policy = {s: 'U' for s in CELLS if s not in TERMINAL}
    evaluations = 0
    while True:
        V = evaluate_policy(policy, slip, gamma)
        evaluations += 1
        new = {}
        for s in policy:
            q = {a: q_value(V, s, a, slip, gamma) for a in 'URDL'}
            best = max(q.values())
            new[s] = max(q, key=q.get)
        if new == policy:
            return V, policy, evaluations
        policy = new

def same_policy(p1, p2, values, slip, gamma):
    """True if, in every non-end cell, both actions are within 1e-9 of the best q_value."""
    for s in CELLS:
        if s in TERMINAL:
            continue
        q = {a: q_value(values, s, a, slip, gamma) for a in 'URDL'}
        best = max(q.values())
        if q[p1[s]] <= best - 1e-9 or q[p2[s]] <= best - 1e-9:
            return False
    return True
```
- **same_policy compares actions**: first fails test 6 (fails 6). Symptom: Reports a difference wherever the actions differ, ties included.
```python
import numpy as np

ROWS, COLS = 4, 5
WALL = {'r2c3'}
TERMINAL = {'r1c5': 1.0, 'r2c5': -1.0}
STEP = -0.04
MOVES = {'U': (-1, 0), 'R': (0, 1), 'D': (1, 0), 'L': (0, -1)}
SIDES = {'U': 'LR', 'D': 'LR', 'L': 'UD', 'R': 'UD'}
CELLS = [f'r{r}c{c}' for r in range(1, ROWS + 1) for c in range(1, COLS + 1)
         if f'r{r}c{c}' not in WALL]

def move(s, a):
    """The cell reached from s by action a; a wall or the edge leaves the agent at s."""
    r, c = map(int, s[1:].split('c'))
    dr, dc = MOVES[a]
    t = f'r{r + dr}c{c + dc}'
    if not (1 <= r + dr <= ROWS and 1 <= c + dc <= COLS) or t in WALL:
        return s
    return t

def transition(s, a, slip):
    """{next cell: chance}: the intended move with 1 - 2*slip, each side move with slip."""
    out = {}
    for b, p in ((a, 1 - 2 * slip), (SIDES[a][0], slip), (SIDES[a][1], slip)):
        if p > 0:
            t = move(s, b)
            out[t] = out.get(t, 0) + p
    return out

def reward(t):
    """Reward for entering cell t: its payoff plus the step cost."""
    return TERMINAL.get(t, 0.0) + STEP

def q_value(V, s, a, slip, gamma):
    return sum(p * (reward(t) + gamma * V[t]) for t, p in transition(s, a, slip).items())

def evaluate_policy(policy, slip, gamma):
    n = len(CELLS)
    P, r = np.zeros((n, n)), np.zeros(n)
    for i, s in enumerate(CELLS):
        if s not in TERMINAL:
            for t, p in transition(s, policy[s], slip).items():
                P[i, CELLS.index(t)] += p
                r[i] += p * reward(t)
    v = np.linalg.solve(np.eye(n) - gamma * P, r)
    return {s: float(v[i]) for i, s in enumerate(CELLS)}

def policy_iteration(slip, gamma):
    """Start from U everywhere. Improve: keep the current action if it is within 1e-9 of the best,
    else take the first best in the order U, R, D, L. Stop when nothing changes.
    Return (values, policy, number of evaluations)."""
    policy = {s: 'U' for s in CELLS if s not in TERMINAL}
    evaluations = 0
    while True:
        V = evaluate_policy(policy, slip, gamma)
        evaluations += 1
        new = {}
        for s in policy:
            q = {a: q_value(V, s, a, slip, gamma) for a in 'URDL'}
            best = max(q.values())
            if q[policy[s]] > best - 1e-9:
                new[s] = policy[s]
            else:
                new[s] = next(a for a in 'URDL' if q[a] > best - 1e-9)
        if new == policy:
            return V, policy, evaluations
        policy = new

def same_policy(p1, p2, values, slip, gamma):
    """True if, in every non-end cell, both actions are within 1e-9 of the best q_value."""
    for s in CELLS:
        if s in TERMINAL:
            continue
        q = {a: q_value(values, s, a, slip, gamma) for a in 'URDL'}
        best = max(q.values())
        if p1[s] != p2[s]:
            return False
    return True
```

### l9-learning-from-episodes.json `.screens[4].widget` (7 hidden tests)
- **every-visit MC**: first fails test 3 (fails 3, 4). Symptom: Averages the return after every visit.
```python
import random

def returns_from_episode(rewards, gamma):
    """[G_0, G_1, ...]: the return after each step of one episode."""
    G, out = 0.0, []
    for r in reversed(rewards):
        G = r + gamma * G
        out.append(G)
    return out[::-1]

def mc_evaluate(episodes, gamma=1.0):
    """episodes: a list of (states, rewards). Average the return after each state's FIRST visit in an episode."""
    total, count = {}, {}
    for states, rewards in episodes:
        seen = set()
        for s, G in zip(states, returns_from_episode(rewards, gamma)):
            if True:
                total[s] = total.get(s, 0.0) + G
                count[s] = count.get(s, 0) + 1
    return {s: total[s] / count[s] for s in total}

def random_walk_episode(rng):
    """Start at 'C'; step right if rng.random() < 0.5, else left. Return (states, rewards)."""
    s, states, rewards = 2, [], []
    while True:
        states.append('ABCDE'[s])
        s += 1 if rng.random() < 0.5 else -1
        if s == 5:
            rewards.append(1)
            return states, rewards
        rewards.append(0)
        if s == -1:
            return states, rewards
```
- **rewards, not returns**: first fails test 3 (fails 3, 4, 5, 7). Symptom: Averages the next reward (the lesson trap).
```python
import random

def returns_from_episode(rewards, gamma):
    """[G_0, G_1, ...]: the return after each step of one episode."""
    G, out = 0.0, []
    for r in reversed(rewards):
        G = r + gamma * G
        out.append(G)
    return out[::-1]

def mc_evaluate(episodes, gamma=1.0):
    """episodes: a list of (states, rewards). Average the return after each state's FIRST visit in an episode."""
    total, count = {}, {}
    for states, rewards in episodes:
        seen = set()
        for s, G in zip(states, rewards):
            if s not in seen:
                seen.add(s)
                total[s] = total.get(s, 0.0) + G
                count[s] = count.get(s, 0) + 1
    return {s: total[s] / count[s] for s in total}

def random_walk_episode(rng):
    """Start at 'C'; step right if rng.random() < 0.5, else left. Return (states, rewards)."""
    s, states, rewards = 2, [], []
    while True:
        states.append('ABCDE'[s])
        s += 1 if rng.random() < 0.5 else -1
        if s == 5:
            rewards.append(1)
            return states, rewards
        rewards.append(0)
        if s == -1:
            return states, rewards
```
- **discount applied forwards**: first fails test 1 (fails 1, 5). Symptom: G = gamma r + G.
```python
import random

def returns_from_episode(rewards, gamma):
    """[G_0, G_1, ...]: the return after each step of one episode."""
    G, out = 0.0, []
    for r in reversed(rewards):
        G = gamma * r + G
        out.append(G)
    return out[::-1]

def mc_evaluate(episodes, gamma=1.0):
    """episodes: a list of (states, rewards). Average the return after each state's FIRST visit in an episode."""
    total, count = {}, {}
    for states, rewards in episodes:
        seen = set()
        for s, G in zip(states, returns_from_episode(rewards, gamma)):
            if s not in seen:
                seen.add(s)
                total[s] = total.get(s, 0.0) + G
                count[s] = count.get(s, 0) + 1
    return {s: total[s] / count[s] for s in total}

def random_walk_episode(rng):
    """Start at 'C'; step right if rng.random() < 0.5, else left. Return (states, rewards)."""
    s, states, rewards = 2, [], []
    while True:
        states.append('ABCDE'[s])
        s += 1 if rng.random() < 0.5 else -1
        if s == 5:
            rewards.append(1)
            return states, rewards
        rewards.append(0)
        if s == -1:
            return states, rewards
```


## Fix pass

I recomputed every corrected number before writing it: 0.15 (3/20), 132 (smallest k with 0.9^k <= 1e-6, by loop and by logarithm), 3.45 ((21 + 3.15)/7), 1.9333 (5.8/3), 156.25 ((0.25/0.02)^2), the new l5 return 0.7016 (also the l5 screens[4] value three moves from the goal), the gamma 0.5 value in l6 (by a second, iterative solve), and the minimum true Q on the deterministic grid (0.2505, bar the two moves into the pit at -1.04). For the flicker finding I reran the lesson's own slippery agents (seeds 0 to 9, checked every 50 episodes to 20,000): all 8 that matched lost the match again, and none matches at 20,000. After the edits: validator 0 errors and no `[ai-mutants]` warning on rl files, `voice-scan.py 35` 0 and 0, the three number scripts exit 0 (359, 256 and 223 checks), `grade-all.mjs --code` 0 failures on every rl file, playthrough green with and without `--mobile` on every edited file.

Status: fixed 32, disputed 0, deferred 0 (7 errors, 13 warnings, 12 notes). Where a fix differs from the proposal, the line says why. Mutants: 61 added across the 21 Python code widgets (the 62 in the appendix less one that no test can catch, see line 22); every widget carries two or more, and `grade-all` confirms each fails the stated test first. New hidden tests are appended, so no existing test number moved.

### Level 1 (7 fixed)

1. review-1 items[7] 'swap': fixed, value 0.15 with the current why (Beta(3, 17), mean 3/20).
2. l2 screens[0] 'all-lost': fixed, the why now says each random order was charged C's whole fill chance, 0.60.
3. l2 screens[1] / quoted greedy figures: fixed, an added sentence says the 56.0 and 61.8 differ only by noise (explain stays at three sentences).
4. l1 screens[5] `run_greedy`: fixed with a different test from the proposal. Both proposals fail on arithmetic: the greedy agent starts at Q = 0, so the first arm to win holds Q > 0 and the rest hold 0, and `ps = [0.9, 0.9]` or any seed gives identical choices under a constant step (I searched 480 runs, none differ). Changing the return would break every example. Instead test 8 replaces `argmax_random` in `setup` with a recorder and checks the estimates passed on the last step: `[0.3061224489795918, 0.0, 0.0]` (15/49) against 0.266 for the constant step. The constant-step mutant is now a mutant (test 8); `how` says to call `argmax_random` for every choice.
5. l3 screens[6] prose: fixed, "the three arms stand as below".
6. l3 summary.ideas[2]: fixed, "on these venues, in 20 seeded runs, it overtook epsilon-greedy only between 40,000 and 50,000 pulls".
7. l4 screens[7] 'luck': fixed with one change. My run over seeds 0 to 199 gives greedy 61.76 (SE 4.35) and Thompson 20.77 (SE 1.07), a gap of 9.2 combined standard errors, so the line says "about nine", not ten.

### Level 2 (9 fixed)

8. l8 screens[0] prose: fixed, "all negative except row 1, column 4".
9. l7 screens[4] 'bound': fixed, value 132; the why now says 0.9^k <= 10^-6 needs 132 sweeps.
10. l7 screens[5] 'keep-all': fixed, value 3.45.
11. l6 screens[9] explain: fixed in one combined sentence (a longer text would break the three-sentence limit): starting at the limit costs about £4 against flat, and never hitting it is worth £80, so the limit costs £18.69 from flat (80 - 61.31).
12. l8 screens[5] prose and explain: fixed, the keep rule "guarantees the loop stops whatever the tie rule" and here saves one evaluation, 5 against 6.
13. l5 screens[6] trap: fixed by a new trap, a bump into the wall then U then R (return 0.7016). Distractors: 0.824 (skips the bump), 0.7416 (bump pays nothing), 0.81 (no step costs). `rl-L2-numbers.py` now checks them, with V(3) as the second method.
14. l7 screens[4] canvas label: fixed, "(deterministic changes follow it exactly)".
15. l6 screens[7] gamma: fixed, test 10 `evaluate_policy(opt, 0.1, 0.5)['r4c1']` = -0.07233115507108162; the hard-coded-gamma mutant now fails it.
16. l7 screens[7] exact-equality ties: fixed, test 11 sets two values 1e-12 apart (so U and R tie within 1e-9 but not exactly); the exact-equality mutant now fails it.

### Level 3 (16 fixed)

17. l11 screens[7]: fixed. Prose, feedback.correct and explain now say zero is not optimistic here: every true Q except the two moves into the pit is at least 0.25 (minimum 0.2505), so zero is below the truth. Untried moves still win early because tried ones drop below 0 before news of the goal arrives. "As in level 1" is gone.
18. l9 screens[1] 'E': fixed, "Episode 1 already reached E."
19. l9 screens[9] 'pos': fixed, value 1.9333.
20. l11 screens[8] explain: fixed, "equation 2.7".
21. l11 screens[8] prose, homework-3 items[5]: fixed as proposed, "first matched ... then lost the match again; the other 2 never matched within 20,000". Verified on the lesson's own seeds (see above).
22. Terminal mask, l11: fixed, test 8 (`Q[('r1c5', 'U')] = 0.5`, update 'r1c4' R with terminal True, expect 0.096; the unmasked target gives 0.141). homework-3: no test can see the mask there (end cells are never updated in `learn_gridworld`), as the review says; the mutant is listed only in l11, and the l11 test is the fix.
23. Tie rule, l11 and homework-3: fixed, one exact seeded value in each, `max(Q[('r4c1', a)] ...)` after 500 episodes on seed 0 = 0.24894561528839818, as proposed. Random and last-best tie mutants now fail test 9 in both widgets. `how` states the U, R, D, L rule.
24. l11 quiz[2] explain: fixed, "as long as it keeps trying every move".
25. review-3 items[5] 'var': fixed, value 156.25 with tolerance 1.
26. ai-safety shared code: fixed on the content side by `app/content/data/ai/rl_ops_l3.py` (documented in `docs/reports/rl-3.md`), shipped through the `data` of the l11 code widget and exercised by its test 10; `rl-L3-numbers.py` checks it reproduces the course's numbers bit for bit. Not done here, outside rl: adding "Shared code files" to `docs/briefs/rl.md`, naming `rl_ops_l3.py` in `docs/briefs/ai-safety.md`, and noting that `state.arrows` (engine 1229) exists.
27. l12 screens[3] and [5] explain: fixed, the 0.1409 now reads as falling "from those six cliff-edge cells"; screens[5] says "from its six edge cells".
28. l12 screens[6] prose: fixed, "With ε = 0 the run is the same for every seed".
29. l12 screens[0] caption: fixed, "Green: the route SARSA learns, 13 moves."
30. l12 screens[8] answer: fixed, 0.6.
31. l12 screens[4] how and problems-1 items[2] parts[1]: fixed, "an episode", "an order".
32. `math.isclose` formatting: fixed in 10 `how` strings by edit and in the eleventh (l11) by its rewrite.
