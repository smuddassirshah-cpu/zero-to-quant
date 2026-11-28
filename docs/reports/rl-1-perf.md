# rl level 1: performance task

- `homework-1.json`, item `h-bandit-league`, index 0. Kind `code` (Python, difficulty 5).
- Matched objective: l4 "Build a Thompson sampling agent from Beta posteriors and compare three agents' regret." (also l1 "Write a bandit simulator ..." and l3 "... code the UCB1 agent").
- Task: from a stub, `bandit_league(ps, T, seeds)` runs epsilon-greedy (0.1), UCB1 and Thompson sampling on the same seeds and returns each agent's mean expected regret.
- 7 hidden tests, 1 example: exact seeded means on three set-ups, the key set, equal arms (all 0), and two ordering tests with margins (arms 0.2, 0.5, 0.8: UCB < ε-greedy − 8, Thompson < UCB − 20; venues 0.45, 0.55, 0.6: Thompson and ε-greedy each 10 below UCB). `budget` 10,000 ms; 0.2 s a league in CPython.
- Overlapping screens: l2 screen 4, l3 screen 8 and l4 screen 6 build the three agents one at a time with helpers given; the task asks for all three from a blank start, with shared seeds and regret from counts, which no screen does.

Gates:
1. `node tools/validate.mjs`: 0 errors.
2. `VOICE_BASE=app/content/courses/rl python3 docs/reviews/voice-scan.py 35`: 0 and 0.
3. Numbers script `docs/reports/rl-L1-numbers.py` (venv): 359 checks, exit 0; it reproduces every expected mean with an independent implementation.
4. Playthrough `--set rl/homework-1 --local-cdn <pkgs>`, with and without `--mobile`: all passed, the starter fails.
