# Second read: near-miss marks on existing plants (session AD)

Scope: the 120 `ci-` drills whose `nearMiss` mark went onto an existing plant in session AC (`docs/reports/near-miss-1.md` 57, `near-miss-2.md` 61, `near-miss-3.md` 2), less the 12 sampled in `docs/reviews/review-problems-eigen-4.md`. That leaves 108, not 106: all 108 were read. Every mark in the content matches the index the reports give. No content or engine file was edited.

Method: for each drill a script printed the brief, the model, the marked plant (as a diff against the model where short) and every other plant's `slip`. Model and every plant of all 108 drills were run natively in CPython against the hidden tests (`equal` compare, 2 s per test, recursion limit 1,000). All 108 models pass every test. Every marked plant fails at least one test and passes at least one (`ci-light-cargo` plant 3 was rerun under a memory cap: 5 pass, 7 fail).

The line drawn: a missed tie, boundary, duplicate or base case in the target method is `sound`, and so is the slower order the constraints name. A plant is not the near miss when it is a different naive method (a greedy where the target is a table or a search), a transposition, a parsing slip, or a rule of the brief left out, and a nearer plant sits on the same drill.

## Counts by verdict

| verdict | drills |
|---|---|
| `sound` | 91 |
| `wrong-plant` | 14 |
| `none-qualifies` | 3 |
| `shallow` with no better answer | 0 |
| total | 108 |

All 17 non-sound verdicts are confirmed by running: the marked plant, the plant the mark should move to, and each new plant fail at least one hidden test and pass at least one. Figures below are tests failed over tests run; `t` marks failures by time only.

## Non-sound drills

Format: drill file | drill id | verdict | marked plant index | evidence | exact fix.

- `app/content/drills/ci-broken-steps.json` | `ci-broken-steps` | wrong-plant | 1 | The marked plant drops the stride of 3, a rule of the brief left out (6/12). Plant 2 is the model's recurrence with steps 1 and 2 seeded by hand, so a cracked step among them is ignored: the base case missed (3/12). | move mark to planted[2]
- `app/content/drills/ci-ends-to-target.json` | `ci-ends-to-target` | wrong-plant | 0 | Closing the larger end is a greedy, a different method from the window on the lots kept (2/15). Plant 2 is the model without the check for `x` above the total (2/15). | move mark to planted[2]
- `app/content/drills/ci-even-desks.json` | `ci-even-desks` | wrong-plant | 1 | Strongest trader to the weaker desk is a greedy, not the reach table (4/12). Plant 0 is the plain subset-sum table without the count of traders, the target one dimension short (4/12). | move mark to planted[0]
- `app/content/drills/ci-funded-projects.json` | `ci-funded-projects` | wrong-plant | 1 | Cheapest projects first is the wrong greedy key (7/13). Plant 2 takes the best profits among projects affordable at the start and never lets the growing fund unlock more: the heap never refilled (8/13). | move mark to planted[2]
- `app/content/drills/ci-log-compactor.json` | `ci-log-compactor` | wrong-plant | 0 | Run lengths taken modulo `k` in one pass use no stack at all (6/14). Plant 1 is the stack that forgets the count of the letters now on top after a deletion, the same cascade missed inside the target method (6/14, the same six tests). | move mark to planted[1]
- `app/content/drills/ci-mirror-pieces.json` | `ci-mirror-pieces` | wrong-plant | 3 | Longest-piece greedy from both ends is a patched greedy, not the table (1/14). Plant 4 is the recursion on the first piece with no memo, the method the constraints name as too slow (5/14t). | move mark to planted[4]
- `app/content/drills/ci-others-product.json` | `ci-others-product` | wrong-plant | 1 | A forgotten final `% MOD` is a slip, and shows no gap in the prefix and suffix method (5/13). Plant 2 forms the exact product and divides each cell out, the natural method the brief rules out (4/13t). | move mark to planted[2]
- `app/content/drills/ci-pillar-queens.json` | `ci-pillar-queens` | wrong-plant | 1 | Checking one diagonal only leaves out a rule of the brief (8/14). Plant 0 is the textbook search with a guard in every row, never an empty row, so it counts only placements in the first `q` rows (5/14). | move mark to planted[0]
- `app/content/drills/ci-priced-edits.json` | `ci-priced-edits` | wrong-plant | 0 | Insert and delete prices swapped is a transposition, the class judged not true for `ci-spiral-cells` (4/12). Plant 1 is the unit-cost table with its first row and column left as counts, the textbook table one step short of priced edits (9/12). | move mark to planted[1]
- `app/content/drills/ci-relay-masts.json` | `ci-relay-masts` | wrong-plant | 0 | Every new relay on the longest gap is a greedy closed form, not the search on the answer (4/13). Plant 1 is the model's search counting `g // L` relays, one too many when `L` divides `g`: the boundary missed (5/13). | move mark to planted[1]
- `app/content/drills/ci-stone-hops.json` | `ci-stone-hops` | wrong-plant | 0 | Always hopping to the furthest stone is a greedy, not the search (1/15). Plant 5 is the breadth-first search that looks at every place in reach, without the furthest-seen mark, the order the constraints rule out (3/15t). | move mark to planted[5]
- `app/content/drills/ci-three-feed-common.json` | `ci-three-feed-common` | wrong-plant | 2 | One pairwise longest common string matched with the third feed is a different method (1/15). Plant 3 is the three-way recursion with no memo, right and named as too slow (3/15t). | move mark to planted[3]
- `app/content/drills/ci-tolerant-common.json` | `ci-tolerant-common` | wrong-plant | 0 | First close tick left in `b` is a greedy, not the table (4/13). Plant 2 is the model with `<` for `<=`, refusing ticks exactly `tol` apart: the tie missed (7/13). | move mark to planted[2]
- `app/content/drills/ci-trace-count.json` | `ci-trace-count` | wrong-plant | 0 | The word-search walk with used marks carries two faults: it forbids the returns the brief allows and it follows each trace singly (7/13). Plant 3 follows every trace with no marks, right and too slow, one step from the layer table (4/13t). | move mark to planted[3]
- `app/content/drills/ci-free-block.json` | `ci-free-block` | none-qualifies | 1 | The largest-square table answers another question (6/13). Plant 0 never resets a column at a taken desk, a slip (6/13). The near miss should be the model's stack with no closing height, so a rectangle reaching the last column is never measured. | add new plant A below, marked; unmark planted[1]
- `app/content/drills/ci-read-preorder.json` | `ci-read-preorder` | none-qualifies | 2 | Splitting on single spaces is a parsing slip (3/12); plant 0 is another, and plant 1 reads the right part first. The near miss should be the right build taking tokens with `pop(0)`, quadratic. | add new plant B below, marked; unmark planted[2]
- `app/content/drills/ci-rebuild-from-orders.json` | `ci-rebuild-from-orders` | none-qualifies | 1 | A slice one id short breaks every tree of two or more ids (11/12, all errors); plant 0 builds the right part first and plant 2 ignores `ino`. The near miss should be the model with no position table, searching `ino` for each root. | add new plant C below, marked; unmark planted[1]

## New plants

Each was run natively against the drill's examples and hidden tests.

Plant A, `ci-free-block`. Examples 1 of 2 pass; hidden tests 7 pass, 6 fail (wrong answers).

```python
def largest_free_block(rows):
    if not rows:
        return 0
    c = len(rows[0])
    up = [0] * c
    best = 0
    for row in rows:
        for j in range(c):
            up[j] = up[j] + 1 if row[j] == '.' else 0
        stack = []
        for j, h in enumerate(up):
            left = j
            while stack and stack[-1][1] >= h:
                left, top = stack.pop()
                best = max(best, top * (j - left))
            stack.append((left, h))
    return best
```

slip: `Without a closing height of 0 the stack is never emptied at the end of a row, so rectangles that reach the last column are never measured.`

Plant B, `ci-read-preorder`. Examples 2 of 2 pass; hidden tests 10 pass, 2 fail by time (tests 10 and 11 take 23 s and 60 s natively, against under 0.2 s for the model).

```python
def read_tree(text):
    tokens = text.split()
    def build():
        token = tokens.pop(0)
        if token == '#':
            return None
        left = build()
        right = build()
        return (int(token), left, right)
    return build()
```

slip: `Taking each token with pop(0) is right but shifts the whole list every time, which is $O(n^2)$ and too slow for 100,000 values.`

Plant C, `ci-rebuild-from-orders`. Examples 2 of 2 pass; hidden tests 11 pass, 1 fails by time (test 11 takes 17 s natively, against under 0.2 s for the model).

```python
def rebuild(pre, ino):
    pos = 0
    def build(lo, hi):
        nonlocal pos
        if lo >= hi:
            return None
        root = pre[pos]
        pos += 1
        mid = ino.index(root)
        left = build(lo, mid)
        right = build(mid + 1, hi)
        return (root, left, right)
    return build(0, len(ino))
```

slip: `Searching the whole of ino for each root is right but takes $O(n)$ a node, far too slow for 100,000 ids.`

Note on plant C: the plain slicing version (`pre[1:i + 1]`, `ino[:i]`) is the more natural near miss, but it passes all 12 hidden tests natively, each in under 0.2 s. The tests do not rule out the method the constraints call too costly. A test that does would be a large generated one, which AUTHORING advises against, so the search of the whole list is offered in its place.

## Sound but borderline

Left as `sound`; listed so a later reader need not rediscover them.

- `ci-shift-picks` plant 3: the richest-free-day greedy against a table target. AUTHORING names this plant as a pattern of the near miss, so it stands. Plant 2 (day 1's base case) is the table one step short.
- `ci-capped-repeats` plant 1 and `ci-smooth-orderings` plant 1: a boundary read as `>=`, sound by the tie rule, but each fails most tests (12/13 and 10/14), so a learner meets it on the worked example.
- `ci-clear-rate` plant 1: the search's top set one below the largest queue, a boundary no learner is led to; the drill has only two plants.
- `ci-rota-swaps` plant 3 and `ci-three-leg-nets` plant 3: the model with a contrived wrong term (the larger count of the two end letters; a cut-off that assumes a target of 0 or more). Each is one real gap and fails one test.

## Not judged

Nothing was left unjudged. Limits of the check: runs were native CPython, not the page runtime, so time-based verdicts rest on a 2 s per-test alarm (the three new plants were timed in full). No C++ drill is in the list.

Scripts and results: scratch only (`read-near-miss/` in the session scratchpad: `list.py`, `run.py`, `runp.py`, `ex.py`, `dump.py`, `newplants.py`, `res.json`).

## Fix pass

Each target plant was rerun natively in CPython (2 to 5 s per test) before the edit: every one failed at least one hidden test and passed at least one, as the review says. No finding disputed.

- `ci-broken-steps`: fixed, mark moved to planted[2] (native 3 fail of 12).
- `ci-ends-to-target`: fixed, mark moved to planted[2] (2 of 15, both errors).
- `ci-even-desks`: fixed, mark moved to planted[0] (4 of 12).
- `ci-funded-projects`: fixed, mark moved to planted[2] (8 of 13).
- `ci-log-compactor`: fixed, mark moved to planted[1] (6 of 14).
- `ci-mirror-pieces`: fixed, mark moved to planted[4] (5 of 14, by time).
- `ci-others-product`: fixed, mark moved to planted[2] (4 of 13, by time).
- `ci-pillar-queens`: fixed, mark moved to planted[0] (5 of 14).
- `ci-priced-edits`: fixed, mark moved to planted[1] (9 of 12).
- `ci-relay-masts`: fixed, mark moved to planted[1] (5 of 13).
- `ci-stone-hops`: fixed, mark moved to planted[5] (3 of 15, by time).
- `ci-three-feed-common`: fixed, mark moved to planted[3] (3 of 15, by time).
- `ci-tolerant-common`: fixed, mark moved to planted[2] (7 of 13).
- `ci-trace-count`: fixed, mark moved to planted[3] (4 of 13, by time).
- `ci-free-block`: fixed, plant A added as planted[2] with the review's slip, marked; planted[1] unmarked (native 6 fail of 13).
- `ci-read-preorder`: fixed, plant B added as planted[3] with the review's slip, marked; planted[2] unmarked (native 2 fail of 12, by time). The page runtime accepts it: `planted-check` 0 failures.
- `ci-rebuild-from-orders`: fixed, plant C added as planted[3] with the review's slip, marked; planted[1] unmarked (native 1 fail of 12, by time). The page runtime accepts it: `planted-check` 0 failures.
- `ci-rebuild-from-orders` slicing solution passing all 12 hidden tests: deferred. Per the reviewer, the natural slicing version (`pre[1:i + 1]`, `ino[:i]`) passes every hidden test natively, each in under 0.2 s, though the constraints call it too costly for 100,000 ids; a test that rules it out would be a large generated one, which AUTHORING advises against. Hidden tests left unchanged.

Gates:
- `node tools/validate.mjs`: 0 errors. `[near-miss]` warnings 0 before, 0 after; `[negative-key]` 3 before, 2 after.
- `planted-check --near-miss --local-cdn` on all 17 edited drills: 0 failures (the two time-only plants, B and C, are accepted in the page runtime).
- Number scripts: `drills-ci-4-check.py` flagged the two new slow plants (planted[3] past 2.5 s); added `("ci-read-preorder", 3)` and `("ci-rebuild-from-orders", 3)` to its `SLOW_PLANTED` set, which requires them to time out on a hidden test, and it exits 0. The other scripts covering edited drills (`drills-ci-1`, `2`, `3`, `6`, `7`, `8-check`, `8-indep`, `8-wrong`) exit 0 on the edited ids.

l13 edit (`app/content/courses/complex/l13-fourier-pricing.json`, `screens[10]`): recomputed $0.5(e^{-0.08875} - 1) = -0.042463$, so the key -0.0425 stands and +0.0425 is $-\lambda\kappa$. Added `wrong` entry `sign` (value 0.0425, abs 0.0005) and `feedback.byKey.sign`: "$+0.0425$ is $-\lambda\kappa$, the amount added to the drift. $\lambda\kappa$ itself is negative, because the mean jump is a fall." `docs/reports/complex-L3-numbers.py` gained three checks (value of `wrong[2]`, the feedback text, and the sign of $\lambda\kappa$) and exits 0 (183 of 183). `grade-all.mjs --file` on the lesson: 0 failures. Playthrough `--lesson complex/l13-fourier-pricing`: All passed, with and without `--mobile`. The graded answer is unchanged; one wrong-answer route was added.
