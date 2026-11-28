# rl level 4: performance task

- `homework-4.json`, item `h4-train-corridor`, index 0. Kind `code` (Python, difficulty 5).
- Matched objective: l16 "Build a policy network with the array autograd and train it with REINFORCE and a baseline." and l15 "Derive why a baseline leaves the gradient unbiased, and measure the variance it removes."
- Task: from a one-line stub, `train_corridor(episodes, seed)` builds the short corridor, runs REINFORCE with a learned running-mean baseline, and returns the final chance of right and the variance ratio of the baselined to the plain gradient estimates on the same episodes.
- 6 hidden tests, 1 example: three short seeded runs exactly (they pin the order of draws, the estimate before the baseline update, and that the baselined estimate steps the dials); the ratio below 0.5 for seeds 0 to 4 after 1,000 episodes; the mean final $p$ over seeds 0 to 9 between 0.53 and 0.64; the return shape. Four mutants (baseline updated before use, baseline never used, ratio upside down, whole return in place of reward-to-go) each fail test 1.
- Overlapping screens: l14 screen 7 codes plain REINFORCE on the corridor with the helpers given, and l15 screen 7 a baselined learner on the venues; the task asks for the corridor model, the learned baseline and the variance measurement together, from nothing, which no screen does.

Gates:
1. `node tools/validate.mjs`: 0 errors.
2. `VOICE_BASE=app/content/courses/rl python3 docs/reviews/voice-scan.py 35`: 0 and 0.
3. Numbers script `docs/reports/rl-L4-numbers.py` (venv): 253 checks, exit 0; it reruns the solution against every test and checks the thresholds with an independent learner.
4. Playthrough `--set rl/homework-4 --local-cdn <pkgs>`, with and without `--mobile`: all passed, the starter fails.
