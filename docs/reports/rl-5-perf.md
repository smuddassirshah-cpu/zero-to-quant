# rl level 5: performance task

- `homework-5.json`, item `h5-best-move`, index 0. Kind `code` (Python, difficulty 5).
- Matched objective: l17 "Code minimax and find the value of a small game." and l18 "Implement alpha-beta pruning and a table of seen positions, and count the work saved."
- Task: from a one-line stub, `best_move(board)` for tic-tac-toe: work out whose turn it is, search the game with a table of seen positions (alpha-beta optional), prefer the quicker win, and return the cell.
- 9 hidden tests, 1 example: a win in one; a board where a slower forced win sits at a lower cell than the immediate win; a block; a fork (the only winning move); the opening (must keep the draw); a forced move; 10 seeded games against a random player moving first and 10 moving second, none lost; a win for O when O is to move. Three mutants (every win scored alike, the opponent's value not negated, always playing as X) fail tests 2, 1 and 9.
- Overlapping screens: l17 screen 6 codes `minimax` returning a value and l18 screen 5 `alphabeta`; neither chooses a move, scores wins by depth or plays whole games. The task asks for the move-choosing player from nothing.

Gates:
1. `node tools/validate.mjs`: 0 errors.
2. `VOICE_BASE=app/content/courses/rl python3 docs/reviews/voice-scan.py 35`: 0 and 0.
3. Numbers script `docs/reports/rl-L5-numbers.py` (venv): exit 0; it reruns the solution against every test.
4. Playthrough `--set rl/homework-5 --local-cdn <pkgs>`, with and without `--mobile`: all passed, the starter fails.
