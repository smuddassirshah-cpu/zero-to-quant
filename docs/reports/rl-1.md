# rl level 1 (Bandits): report

## Files written

All in `app/content/courses/rl/`, skill `rl-bandit`, ids, names and objectives as in `course.json`.

| File | Screens / items | Quiz | Code screens | Shape |
|---|---|---|---|---|
| `l1-which-machine.json` | 11 | 4 | 2 (`pull` + `regret`, `run_greedy`) | explore hook (30 orders, frames slider), problem, problem (names regret), ladder ×4, trap, problem (edge: equal arms), generalise, transfer |
| `l2-exploring-at-random.json` | 11 | 3 | 2 (`epsilon_greedy` + `regret_floor`, `ewma_update`) | problem hook (floor), explore (recorded curves), problem, ladder ×5 (code, decaying ε, optimism, drifting arm as the edge case, code), trap, generalise, transfer |
| `l3-optimism.json` | 11 | 3 | 1 (`hoeffding_bound`, `ucb_scores`, `run_ucb`) | problem hook (standard error), explore (two bounds on a log axis), problem, ladder, derive (order, one distractor), ladder (score table), trap, ladder (code), ladder (recorded comparison), generalise (edge: untried arm), transfer |
| `l4-sampling-beliefs.json` | 11 | 3 | 2 (`posterior` + `prob_a_beats_b`, `run_thompson`) | problem hook, explore (Beta curves with a slider), problem (names Thompson, probability matching), ladder ×4, trap, ladder (edge: strong prior), generalise, transfer |
| `review-1.json` | 10 items, difficulty 2 to 4, `pass` 0.8 | | | every lesson twice or more |
| `homework-1.json` | 7 items, difficulty 3 to 5 | | 2 | performance `code` task `bandit_league` (5), `run_drift` code (4), `order` derivation with two distractors (4), numeric ×2, multi, longform (5, 10-point rubric) |
| `problems-1.json` | 3 problems, 12 parts, difficulty 4, 5, 3 | | | Beta update → P(A beats B) → expected pulls → update again; UCB bonus → score → choice → pulls needed; floor chain |

Traps: l1 judging an agent by its final estimates; l2 "more exploring is always safer"; l3 pulling the best estimate when another arm has few pulls (quiz: Chebyshev's bonus); l4 "Thompson is random, so worse than greedy". Edge cases: l1 equal arms (regret 0), l2 a venue whose chance drops halfway, l3 an untried arm scores infinity, l4 a strong prior $\mathrm{Beta}(50, 10)$ on a 0.45 arm.

## Gates

1. Validator: `node tools/validate.mjs` 0 errors overall; my files carry only advisory warnings (`O2-long-sentence` of 20 words or more, and "ladder usually reuses the previous canvas kind" where a ladder moves between a chart and a code or score table).
2. Voice: `VOICE_BASE=app/content/courses/rl python3 docs/reviews/voice-scan.py 35`: over 35 words 0, lesson ids in code spans 0.
3. Numbers: `docs/reports/rl-L1-numbers.py` with the venv: 359 of 359 checks, exit 0.
4. Playthrough with `--local-cdn .../scratchpad/aitiming/pkgs`, desktop and `--mobile`: all four lessons (15, 14, 14, 14 checks; quizzes full), `review-1` 10 of 10, `homework-1` 7 of 7 with the performance starter failing, `problems-1` 3 problems, 12 parts: all passed. Files changed after a green run were replayed in both modes. Screenshots in the scratchpad `rl-1/shots` and `shotsm`; read, no layout faults.
5. Also: `grade-all.mjs` on the seven files, 74 widgets, 0 failures; `fresh-check --file` on review, homework and problems: 0 hits (advisories only: the venue chances 0.45, 0.55, 0.6 shared on purpose).

## Numbers and their sources

Every seeded value is computed by the lesson's own `solution` (run against its tests in CPython by the number script, starter failing) and by an independent `Agent` class in the number script; the browser playthrough reproduces them in Pyodide.

| Number | Where | Source |
|---|---|---|
| 66.67, 0.00667, 6.67 | l1, l2 | $1000(0.6 - 1.6/3)$ in fractions; floor $\varepsilon(q^* - \bar q)$ |
| 0.75 | l1 | running mean both ways |
| Hook 7, 3, 5 fills of 10 | l1 | seed 12, round robin |
| Greedy seed 1: 449 fills, all A; seed 0: 546, all B; 127 of 200 lock-ins | l1, l2 | both implementations |
| Mean regret, seeds 0 to 199, T = 1000: greedy 61.8, ε 0 / 0.01 / 0.1 / 0.3 = 56.0 / 40.6 / 24.0 / 30.0, optimistic greedy 27.9, UCB1 37.8, UCB with $0.5\sqrt{\ln t/n}$ 18.3, Thompson 20.8 | l2, l3, l4 | both implementations |
| UCB1 overtakes ε = 0.1 between 40,000 and 50,000 pulls (20 seeds) | l3, homework | number script |
| 61.8 = $\sum_{t \le 1000} t^{-1/2}$; 0.1216 = $0.9^{20}$; 0.9576; drift sample mean 0.50 (seed 21) | l2 | direct and Euler-Maclaurin |
| 0.1549, 0.25, 0.1353, 0.2707, 0.00067, 0.0625 | l3 | closed forms; exact binomial tail checked below Hoeffding |
| 0.9597, 0.4292, 1.1754, table and trap scores, 1.6808, 1581.1, 0.3679 | l3 | closed forms |
| 0.6667, 0.5962, 0.6921 (quadrature; $10^6$ NumPy draws agree within 0.002), 0.6154, 0.5938, 0.5276, 0.5556, 40 | l4 | Beta algebra and quadrature |
| League means (seeds 0 to 19, T = 2000): arms 0.2/0.5/0.8: 70.46, 48.84, 9.09; venues: 35.20, 60.76, 32.89 | homework | both implementations |
| 922, 7369, 1597, 130, 205.5 fills gained by a constant step | review, homework, problems | closed forms; seeded |
| 2/3 and 1/2 for Beta(2, 1) and Beta(2, 2) against a uniform | problems | integrals and draws |

## Deviations from the brief (read these)

- **UCB1 does not beat epsilon-greedy on the planner's venues.** At $T = 1000$ over 200 seeds UCB1 averages 37.8 against 24.0; at $T = 2000$ over 20 seeds 60.8 against 35.2. It overtakes only between 40,000 and 50,000 pulls. The homework test "Thompson and UCB below epsilon-greedy on the planner's arms at T = 2,000" would be false, so the performance task checks exact seeded means, the ordering UCB < ε-greedy − 8 and Thompson < UCB − 20 on arms 0.2, 0.5, 0.8 (gaps 0.3), and the honest ordering on the venues (Thompson < UCB − 10, ε-greedy < UCB − 10). l3 teaches why (a worst-case bonus over-explores arms 0.05 apart; a smaller bonus does best) and l4's comparison shows it.
- The greedy agent breaks ties with `rng.choice` (a helper given in the starter), so it locks onto whichever arm wins first; seed 0 never tries the best venue.
- The homework league case sums 120,000 pulls (above the brief's 10,000 a case); it takes 0.2 s in CPython and carries `budget` 10,000 ms.
- Exact-on-seed tests depend on the update written `Q[a] += (r - Q[a]) / n[a]` and the bonus `math.sqrt(2 * math.log(t) / n)`: algebraically equal forms change float ties (the number script found this). Every code prose states those lines verbatim.

## Seeds and conventions

`pull(p, rng)` is `1 if rng.random() < p else 0`; every agent owns `random.Random(seed)`. Order of random calls: ε-greedy draws `rng.random()` first every step, then `randrange` or the tie-breaking `rng.choice`, then the pull; UCB1 uses the generator only for pulls; Thompson draws `betavariate` for every arm in order, then pulls. Regret is expected regret from pull counts, $\sum_a n_a(q^* - q(a))$. Builders and checks live in the scratchpad folder `rl-1`.

## course.json

No change proposed.
