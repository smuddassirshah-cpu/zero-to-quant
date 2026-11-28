# rl level 5 (Search and self-play): report

## Files written

All in `app/content/courses/rl/`, skill `rl-search`, ids, names and objectives as in `course.json`. Pure Python throughout; no shared module was needed (no `rl_ops_l5.py`), and `autograd.py` and `rl_ops_l3.py` / `rl_ops_l4.py` are untouched.

| File | Screens / items | Quiz | Code | Shape |
|---|---|---|---|---|
| `l17-minimax.json` | 10 | 3 | `nim_losing`, `minimax` (memoised), `count_positions` | problem hook (tap the losing Nim piles 0 to 12), problem (take 1 from 21), ladder ×4 (backed-up tree, tic-tac-toe value 0, tree size against positions, code), trap (min node scored as a max), ladder edge (prefer the quicker win), generalise (forward edge to `game-theory` l5), transfer (alternating offers) |
| `l18-pruning-the-tree.json` | 10 | 3 | `alphabeta` returning (value, nodes) | problem hook (tap the leaves never read on a 9-leaf tree), problem (value unchanged), ladder ×3 (18,297 against 549,946; move order 7,275; code), trap (pruning is exact), ladder edge (worst order prunes nothing), generalise (alpha, beta, depth limits, table), transfer (pruning risk scenarios) |
| `l19-tree-search.json` | 10 | 3 | `uct_score`, `mcts` | problem hook (which child next), explore (visit counts at 20 to 1,000 iterations, frames), problem (UCT score), ladder ×3 (back-up of a draw, most-visited share, code), trap (lucky average), ladder edge (forced move), generalise, transfer (execution schedules under a simulator) |
| `l20-self-play.json` | 10 | 3 | `self_play_nim` | problem hook (negated target), explore (recorded win rate against a random player), problem (terminal target), ladder ×2 (the table recovers $n \bmod 4$; code), trap (only beats itself), ladder (AlphaGo and AlphaZero, marked as reading), generalise, transfer (a market of copies) |
| `review-5.json` | 10 items, difficulty 2 to 4, `pass` 0.8 | | | every lesson |
| `homework-5.json` | 6 items, difficulty 3 to 5 | | 2 | performance `code` `best_move` (5), `mcts_nim` code (4), `order` one MCTS iteration with a distractor (4), numeric (Knuth and Moore's minimal tree, 3), multi (4), longform (5, 10-point rubric) |
| `problems-5.json` | 3 problems, 11 parts, difficulty 4, 3, 5 | | | back up a tree, prune it, count leaves read in two orders; Nim with takes of 1 or 2 to a self-play target; UCT scores to the selected child |

Performance task: `docs/reports/rl-5-perf.md`.

## Gates

1. Validator: 0 errors; no `[ai-mutants]` warning. Advisory warnings only on my files (`O2-long-sentence`, point hints, one `O2-no-slip` on a count option whose why names what the count is).
2. Voice: `voice-scan.py 35` with `VOICE_BASE` the rl folder: over 35 words 0, lesson ids in code spans 0.
3. Numbers: `docs/reports/rl-L5-numbers.py` with the venv: 172 of 172, exit 0 (about 30 s).
4. `grade-all.mjs --code --local-cdn <pkgs>` on all seven files: 6 Python widgets, 0 failures; 14 mutants, each failing its named test first.
5. Playthrough `--local-cdn .../scratchpad/aitiming/pkgs`, desktop and `--mobile`: all four lessons, `review-5`, `homework-5` (performance starter fails), `--problems rl/problems-5`: all passed; files edited after a green run were replayed in both modes. Screens read; fix made: trees capped with `maxHeight` 360 so the 9-leaf tree fits a laptop screen.
6. `fresh-check --file` on review, homework and problems: 0 hits after one feedback line in problems-5 was reworded; one advisory (review-5 item 6 lists the four tic-tac-toe counts from l17 as options, by design).

## Numbers and their sources

| Number | Where | Check |
|---|---|---|
| Losing Nim piles 0, 4, 8, ... (and multiples of 5 for takes 1 to 4, of 3 for takes 1 to 2) | l17, l20, review, problems | recursion and the mod rule |
| Tic-tac-toe value 0; every first move 0 | l17 | memoised minimax on arrays and plain minimax |
| 549,946 nodes, 255,168 games | l17 | recursive walk and explicit stack walk |
| 5,478 positions of 19,683 fillings | l17, review | search and the legality count |
| Alpha-beta 18,297 nodes (cells 0 to 8), 7,275 (centre, corners, edges), value 0 | l18 | two implementations (array recursion; strings with explicit sides) |
| Hand trees: value 5, skipped b-2, b-3, c-3; worst order reads 9; review 6 leaves; problems 7 and 5 leaves | l18, review, problems | own leaf-reading routine, values by plain backing up |
| UCT 1.6280 and 2.6651; 1.9274; 1.3845; 1.7597, 1.8230, 2.1460 | l19, review, problems | formula, written two ways |
| MCTS visits from `XX.OO....`, seed 0: (9, 4, 3, 2, 2) at 20, (26, 11, 5, 4, 4) at 50, (140, 25, 13, 11, 11) at 200, (898, 47, 21, 17, 17) at 1,000 | l19 | re-run by an independent MCTS keyed on move paths, same random draws |
| Self-play win rate against a random player, seed 0: 0.43 at 0 episodes to 1.0 by 300 | l20, homework model | re-run with an array table |
| 500 episodes recover take $n \bmod 4$ and negative values at multiples of 4, seeds 0 to 4 | l20 | re-run |
| Minimal tree $3^2 + 3^2 - 1 = 17$ of 81 | homework | formula (Knuth and Moore 1975) |

Reading, marked as such in the text: AlphaGo beat Lee Sedol 4 games to 1 (Silver et al. 2016); AlphaZero learned Go, chess and shogi from self-play (Silver et al. 2018).

## Deviations and notes

- Grading stays inside the timing rule: full-game searches are graded only with a table (`count_positions`, `best_move`) or with pruning (18,297 nodes from the empty board, under a 20,000 ceiling with a 4 s budget); MCTS cases use at most 2,000 iterations.
- MCTS expands the first untried move in cell order and breaks UCT ties by order, so seeded runs are reproducible; the learner's code is tested on planted boards, not on visit counts.
- The quicker-win rule is taught in l17 as $10 - \text{depth}$; the homework model scores a win by 1 plus the empty cells left, the same ordering.

## course.json

No change proposed.
