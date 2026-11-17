# Exam second item 3.3: topic-3.3

File: `app/content/exams/topic-3.3.json`. Brief: `docs/briefs/exam-second-item.md` (Author), with the session AG cap of 36 items.

## Pairs, recomputed

Rule: a level's essential skills are the skills tagged on its review items; a pair is an (exam, skill) whose skill has at most one auto (non-longform) item in the exam. Computed from the exam and the `course.json` of brainteasers, game-theory, mental-pressure, mm-games and puzzles (topic 3.3). 12 pairs, matching the 16 Nov table:

| skill | levels | auto items before |
|---|---|---|
| bz-invariant | brainteasers L1, L2 | 1 |
| bz-quick | brainteasers L3 | 1 |
| bz-search | brainteasers L1, L2, L3 | 1 |
| bz-strategy | brainteasers L2 | 1 |
| gm-auction | game-theory L2 | 1 |
| gm-mixed | game-theory L1, L3 | 1 |
| gm-normal | game-theory L1, L2 | 1 |
| gm-poker | game-theory L3 | 1 |
| gm-sequential | game-theory L2 | 1 |
| mp-speed | mental-pressure L1, L3 | 1 |
| pz-conditioning | puzzles L2, L5 | 1 |
| pz-geometry | puzzles L3, L5 | 1 |

## What changed

The exam already held 30 items, so (a) did not apply.

(b) Three items carry two listed skills, each needing both: a toy-poker indifference (the course tags `l13-toy-poker` with both), a conditional probability read off areas, and a tree turned into its table of plans (`l6-game-trees` teaches that table).

(c) Removed, the only items whose skills keep two other auto items:

| removed | d | skills | kept on those skills |
|---|---|---|---|
| e-even-faces | 3 | pz-expectation | e-cube-walk, e-next-in-line, e-biased-bits |
| e-edge-lift | 2 | mg-quote | e-twelve-put, e-four-dice-desk |
| e-ten-cards | 3 | mg-update | e-skew-short, e-four-dice-desk |

No other item qualifies: every other skill sits at two auto items. With three combined items and three swaps, the six single-skill pairs left need six new items: 30 - 3 + 9 = 36, the fewest that cover every pair (no honest combination was found for bz-invariant with bz-strategy, nor among bz-quick, bz-search, gm-auction and mp-speed).

New items:

| id | d | skills | widget |
|---|---|---|---|
| e-divide-4512 | 2 | mp-speed | numeric (4512 / 48 = 94) |
| e-thousand-days | 2 | bz-quick | choice (Monday + 1000 days: Sunday) |
| e-bags-any-fake | 3 | bz-search | numeric (any subset of 5 bags fake, digital scale: 31 coins) |
| e-divides-forty | 3 | bz-invariant | numeric (pigeonhole on odd parts, 1 to 40: 21) |
| e-bluff-or-check | 3 | gm-poker, gm-mixed | numeric (call share making bet and check equal: 0.48) |
| e-consecutive-numbers | 3 | bz-strategy | choice (consecutive numbers, Ana 3, Ben 4: Ana on statement 3) |
| e-second-price-win | 3 | gm-auction | numeric (price expected given a win at £90, three bidders: £60) |
| e-alerts-close | 4 | pz-conditioning, pz-geometry | numeric (both in first half hour given within 20 minutes: 0.4) |
| e-tree-plans | 5 | gm-sequential, gm-normal | numeric on a tree canvas (pure Nash cells of the 2 x 9 table: 3) |

Pairs left: none. After the edit every skill of the exam has at least two auto items (pz-expectation 3, all others 2).

Ramp: 36 items, difficulty 2: 7, 3: 18, 4: 7, 5: 4 (19%, 50%, 19%, 11%).

Minutes: 75 x 36 / 30 = 90 (exact). Hours note: the exam's time rises by 15 minutes, 0.25 h; the main session runs `readiness-sums.mjs --write`.

## Reuse

`fresh-check.mjs --file content/exams/topic-3.3.json`: no hit on a new item. A first draft used the bird between two trains for bz-quick; fresh-check found it in `puzzles/l12-ants` quiz 2, so it was replaced by the day-of-week item. Page-number digits (in `mm-games/l1`) and a painted cube (in `mock-oa-trader-3`) were rejected for the same reason. Each new item is a different task from the exam's existing item on its skill and from the lessons and reviews read (`l4`, `l7`, `l9`, `l10`, `l12` to `l15` and reviews 1 to 3 of brainteasers; `l6`, `l7`, `l8`, `l9`, `l10`, `l13` and reviews 1 to 3 of game-theory): the lessons cover one fake bag per weighing, hat codes, muddy children, the seller's expected price and the standard bluff and call shares, not these tasks.

## Gates

- `node tools/validate.mjs`: 0 errors; no warning on a new item (three older warnings on e-two-hundred-coins, e-next-in-line and e-bluff-catcher are untouched).
- `VOICE_BASE=app/content/exams python3 docs/reviews/voice-scan.py 35`: 0 and 0.
- `docs/reports/exam-second-item-3.3-numbers.py`: 94 checks, exit 0. Each key twice (closed form and brute force, a grid or a simulation), every wrong value, every printed number, the 36-item count, the minutes and the two-auto-items rule.
- `node tools/grade-all.mjs --file content/exams/topic-3.3.json --local-cdn <pkgs>`: 32 widgets, 0 failures.
- `node tools/playthrough.mjs --exam topic-3.3 --local-cdn <pkgs>`: 36 of 36, passed, desktop and `--mobile`. Screenshots at 440 px checked: the tree fits the column with legible leaf labels.

Backlog bullets: 0.
