# rl level 3: performance task

- `homework-3.json`, item `h-learn-gridworld`, index 0. Kind `code` (Python, difficulty 5).
- Matched objective: l11 "Build a Q-learning agent whose greedy policy matches value iteration on a gridworld." This is the Stage 2 strand exit.
- Task: from a stub, `learn_gridworld(episodes, seed)` builds the deterministic gridworld and runs Q-learning ($\alpha = 0.1$, $\gamma = 0.9$, $\varepsilon = 0.2$, random open starts), returning the Q-table.
- 8 hidden tests, 1 example: table size; greedy policy in value iteration's optimal sets for seeds 0, 1, 2, 3 and 7 after 500 episodes (ties allowed); the start's largest $Q$ within 0.05 of 0.3228 after 2,000 episodes for seeds 0 and 5; end cells untouched; r1c4's largest $Q$ within 0.02 of 0.96.
- Overlapping screens: l11 screen 6 codes the same agent with the grid helpers given; the task asks for the grid model, the agent and its parameters from nothing, which no screen does.

Gates:
1. `node tools/validate.mjs`: 0 errors.
2. `VOICE_BASE=app/content/courses/rl python3 docs/reviews/voice-scan.py 35`: 0 and 0.
3. Numbers script `docs/reports/rl-L3-numbers.py` (venv): 207 checks, exit 0; it reruns the solution against every test.
4. Playthrough `--set rl/homework-3 --local-cdn <pkgs>`, with and without `--mobile`: all passed, the starter fails.
