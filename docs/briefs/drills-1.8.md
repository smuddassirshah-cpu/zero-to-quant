# Brief: topic 1.8 drills (pack `dsa`, 60 drills; PLAN 2d item D; gap file row 1.8)

Topic 1.8 has no drill of its own. These 60 are the independent practice between the taught lessons (`algo-think`, `ds`, `graphs-dp`) and `coding-int`: easy to medium, one idea each, written from a blank function. Binding rules: `docs/AUTHORING.md` section 5 "Drill" (lines about 536 to 546) and "Exam freshness" (577 to 582), section 3 `code`, section 6 voice. Pattern: `app/content/drills/ci-pair-gaps.json`.

## Shape

- Files `app/content/drills/dsa-<slug>.json`, `"pack": "dsa"`, Python only, plus an entry each in `drills/index.json` (appended; the merge unions by id). `course` is the taught course the idea comes from (`ds`, `algo-think` or `graphs-dp`); `skills` must be skills that course's lessons declare.
- `difficulty` 1 to 3: five at 1, six at 2, four at 3 per sub-pack. `pace` 480 to 1,500 seconds. One `pattern` from the fixed vocabulary; add no slug.
- Fields as the pattern file: `fn`, `returns`, `brief` (with one worked example), `constraints`, `hint`, `starter`, `examples` (2 or 3, each with a `note`), `tests` (10 to 14 hidden: empty or smallest input, a tie or duplicate case, a negative or boundary case, and one large input that only the target complexity passes inside the shared time limit in Pyodide), `how`, `solution`, `notes` (three lines: the idea, the trap, the cost).
- Stdin variant: three drills per sub-pack take the whole input as one string and return the output as a string: `solve_<slug>(text)`. The brief gives the input format line by line, as a HackerRank task does (first line `n`, then the values). Tag these `"tags": ["stdin", ...]`. Parsing is part of the task; tests include trailing newlines and extra spaces.
- Fresh: no setup from any lesson, quiz, review, homework, exam or existing drill, and no function name used by a lesson code widget. Run `node tools/fresh-check.mjs` as AUTHORING 577 says and judge each hit. Not a renamed classic copied from a site: write the task in your own setting (order books, sensor logs, timetables, stock counts), keep the pattern.

## Sub-packs (one agent each, 15 drills)

| Sub-pack | Patterns | Ideas to cover |
| --- | --- | --- |
| A | `hashing`, `prefix-sums`, `simulation` | counting with a dict, first repeat, grouping by key, set membership, running totals, range sums, difference arrays, in-place array passes |
| B | `two-pointers`, `windows`, `stacks-queues`, `binary-search` | opposite and same-direction pointers, fixed and growing windows, matching brackets, monotonic stack, queue simulation, search on a sorted list and on the answer |
| C | `trees`, `heaps-tries`, `intervals` | linked-list passes (lists given as Python lists of nodes or nested tuples; state the encoding), tree depth, traversals, binary search tree checks, top k with a heap, merging sorted runs, interval merge and overlap counts |
| D | `graphs`, `dp`, `greedy`, `backtracking` | grid and adjacency BFS and DFS, components, shortest steps, topological order, one-dimensional DP (ways, best sum, coins), a two-dimensional table, greedy with a proof line in `notes`, small subsets search |

## Checks (all required before hand-back)

1. `docs/reports/drills-dsa-<a|b|c|d>-check.py`, run with `<scratchpad>/venv/bin/python`: for every drill it runs the model `solution` on every example and hidden test, and also an independent slow method you write separately (brute force), and both must equal every `expect`. It also checks the `starter` fails at least one test. Exit 0.
2. From `app/`: `node tools/validate.mjs 2>&1 | tail -5` shows 0 errors.
3. `node tools/playthrough.mjs --drill <id> ... --local-cdn <pkgs>` for all 15, and again with `--mobile`: green.
4. Voice: British English, no exclamation marks, no em-dashes, sentences under 35 words, in `brief`, `hint`, `notes`, `note`.
5. Report `docs/reports/drills-dsa-<x>.md` (table: id, pattern, difficulty, pace, stdin, test count; fresh-check hits and your judgement). Engine limits go to `docs/BACKLOG-INBOX.md` under `Raised later (drills dsa <x>):`.

Do not edit engine files, `course.json`, lessons, or other agents' drills. Commit in your worktree with "drills dsa <x>" in the message; never push.
