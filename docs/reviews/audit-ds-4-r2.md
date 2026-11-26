# Blind concept audit, round 2: ds level 4 (Trees and heaps)

Auditor `ds-4-r2`, commit read 6c01af87. Files: `l14-binary-trees`, `l15-search-trees`, `l16-tree-recursion`,
`l17-always-the-smallest`, `l18-order-book-heaps`, `review-4`, `homework-4` (course `ds`, Stage 1, full ledger).
Read blind: no earlier review, audit, author report or author script on this course was opened before the ledger
and the findings below were written.

- Ledger: `docs/reports/audit-ds-4-r2-ledger.md`, 1,068 rows: 1,056 correct, 2 wrong, 9 imprecise, 1 misleading, 0 unverified.
- Script: `docs/reports/ds-L4-concepts-r2.py`, 98 checks; 96 pass and 2 fail (findings 1 and 4), so it exits 1 until those are fixed.
- Sources: CLRS 4th ed. (ch. 6, 12, 13, 16, 20, appendix B), Sedgewick and Wayne 4th ed. (2.4, 3.2), CPython `heapq` and `bisect`
  documentation, Harris, *Trading and Exchanges* ch. 6, Hull ch. 12 and 13.

## Findings

Eight findings: 1 `wrong`, 6 `imprecise`, 1 `misleading`; 1 serious, 7 minor. No graded key and no slip value is wrong.

1. `l14-binary-trees.json` | `screens[7].feedback.byKey.d` and `screens[7].widget.options[3].why` | **wrong, minor** |
   The feedback says sorting "hides the bug on this tree", and the `why` says "sorting only hides the bug". It hides
   nothing: the screen asks for D, B, E, A, F, C, G, and sorting returns A, B, C, D, E, F, G. The option is wrong on this
   very tree, not only on other trees. A learner who checks the claim finds it false, or carries away that in-order of
   this tree is alphabetical. |
   Evidence: concepts check `l14 s7 byKey.d` (fails): `sorted(pre-order) = ABCDEFG`, in-order = `DBEAFCG`. Basis: CLRS 12.1,
   in-order follows positions; labels are sorted only in a search tree. |
   Fix, `feedback.byKey.d`: `You sorted the output. That returns A to G in alphabetical order, not D, B, E, A, F, C, G. In-order follows positions in the tree, not the labels.`
   Fix, `options[3].why`: `Sorting gives A to G alphabetically, which is not the in-order of this tree. In-order follows positions, not labels, so sorting cannot repair the walk.`

2. `l18-order-book-heaps.json` | `screens[5].hints[0].text` and `summary.ideas[2]` | **imprecise, serious** |
   "A heap can only remove cheaply from the top" and "Never delete from the middle of a heap" are stated as facts about
   heaps. They are facts about `heapq` used without an index. A heap that knows an entry's position deletes it in
   $O(\log n)$: move the last item into the hole, then sift up or down. That is the standard follow-up question to this
   very design ("how would you cancel in $O(\log n)$ without lazy deletion?"), so the learner carries away a wrong limit
   of the structure. The option `why` on the same screen is right as written (it blames the $O(n)$ search and the shift). |
   Evidence: concepts check `l18 s5 evidence`: 2,000 deletes at a known index on a 1,023-item heap, heap rule kept, at
   most 40 comparisons each. Basis: CLRS exercise 6.5-10 (HEAP-DELETE in $O(\lg n)$); Sedgewick and Wayne 2.4, `IndexMinPQ.delete`. |
   Fix, `hints[0].text`: `With `heapq` alone, only the top can be removed cheaply. Finding any other entry is an $O(n)$ search.`
   Fix, `summary.ideas[2]`: `Cancel by marking the order dead and dropping dead entries as they reach the top. With `heapq`, do not delete from the middle: finding the entry costs $O(n)$.`
   Add to `screens[5].explain.text` (fourth sentence is over the three-sentence rule, so replace the last sentence):
   `Each entry is popped at most once, so the clean-up is paid for once; a heap that tracks each entry's index can instead delete it in $O(\log n)$.`

3. `homework-4.json` | `items[1].widget` (`how`, `tests`) | **misleading, minor** |
   The item teaches the $k$-way merge: one heap entry per list, $O(N \log k)$. The hidden tests do not check it. Pushing
   all $N$ items into one heap and popping them (a heapsort, $O(N \log N)$, the cost the prose says to avoid) passes all
   nine tests, as does `heapify` on the joined lists. Test 9 blocks `sorted` and `.sort` only. |
   Evidence: sweep H2, submission "every item into one heap": PASS under Pyodide 0.27.7. |
   Fix: add to `prelude` (tested in CPython 3: model 500, `heapq.merge` 500, one heap 100,000, `heapify` 100,000):
   ```python
   import heapq as _hq
   _peak = [0]
   def _watch(f):
       def g(heap, *a):
           r = f(heap, *a)
           _peak[0] = max(_peak[0], len(heap))
           return r
       return g
   for _n in ("heappush", "heapreplace", "heappushpop", "heapify"):
       setattr(_hq, _n, _watch(getattr(_hq, _n)))
   def peak_heap(f):
       _peak[0] = 0
       f()
       return _peak[0]
   ```
   and the test `{"call": "peak_heap(lambda: merge_k([list(range(i, 100000, 500)) for i in range(500)])) <= 500", "expect": "True", "compare": "equal"}`
   before the `NO_SORT` test, with `how`: `Check runs 10 hidden tests: empty lists, repeats, and 500 lists of 200 items. Test 9 checks that your heap never holds more than one entry per list. Test 10 checks that you did not call `sorted` or `.sort`.`
   and `feedback.byKey.test-9`: `Test 9 measures your heap. Keep one entry per list: after each pop, push only the next item of that same list.`
   The fixer must run it under Pyodide; a learner who writes `from heapq import heappush` before the prelude runs is not counted (a false pass, never a false fail).

4. `review-4.json` | `items[5].prose`, `items[5].widget.options[3].why` | **imprecise, minor** |
   Option d, `[8, 3, 10, 3, 6, None, 14]`, is marked wrong because of the repeated 3. That is wrong only under the
   course's strict rule, which this item does not state. Under the CLRS definition (left keys $\le$ node $\le$ right
   keys) the list is a binary search tree, so the item has two right answers under a standard convention. The `why`
   names "the strict rule", but the learner sees it only after answering. |
   Evidence: concepts check `rev i5 option d` (fails). Basis: CLRS 12.1, binary-search-tree property with $\le$. |
   Fix, `items[5].prose`: `Each list is a tree in level order, with `None` for a missing child. As in lesson 15, values may not repeat: the left side is strictly smaller and the right side strictly larger.`

5. `l17-always-the-smallest.json` | `screens[5].feedback.byKey.test-5` | **imprecise, minor** |
   The line gives one cause for failing test 5: writing to index 0 after the last pop. Both natural codings of that
   mistake do fail test 5 first. But so does a second, equally natural mistake: reading the right child at `2i + 2`
   without a bounds check. Test 5 is the first test in which a node has a left child and no right one, so that learner
   also lands here with `IndexError` and is sent to the wrong line of their code. |
   Evidence: sweep W9, "right child read without a bounds check": `test-5`, `IndexError: list index out of range`; the
   named mistake gives `list assignment index out of range`. |
   Fix: `Test 5 pops until the heap is empty. After the last `heap.pop()` the list is empty: do not write to index 0. If a read raised `IndexError`, a right child was missing: check `2 * i + 2 < len(heap)` first.`

6. `l17-always-the-smallest.json` | `screens[2].explain.text` | **imprecise, minor** |
   "A push makes at most as many swaps as the tree has levels." The bound is one fewer. Two screens later the key is 19
   swaps for 20 levels, and 20 is the graded slip `levels` ("swaps happen between levels"). The explain teaches the slip. |
   Evidence: concepts check `l17 s4` (worst-case push on 1,000,000 items: 19 swaps, 20 levels). Basis: CLRS 6.1, height $\lfloor \lg n \rfloor$. |
   Fix: `4 climbed past 9 and 5 and stopped under 2. Each swap moves one level up, so a push makes at most one swap fewer than the tree has levels. This is **sift-up**.`

7. `l17-always-the-smallest.json` | `screens[5].widget.how`, `screens[5].feedback.byKey.test-11` | **imprecise, minor** |
   `how` says "Test 11 checks you did not import `heapq`". The test is `'heapq' not in __learner_source__`: the word
   anywhere, a comment such as `# no heapq here` included. A correct hand-written heap with that comment fails test 11
   and is told to write the swaps itself. Homework 4 item 2 already reads tokens for the same purpose. |
   Evidence: the test string itself; sweep W9 "uses heapq" fails test 11 as the line says. |
   Fix (content only), `how` last sentence: `Test 11 fails if the word `heapq` appears anywhere in your code, comments included.`
   `feedback.byKey.test-11`: `Test 11 looks for the word `heapq` anywhere in your code, comments included. Write the swaps yourself here; the next screens use `heapq`.`
   Better: reuse the token postlude of `homework-4` item 2 with `'heapq' not in _tokens`.

8. `homework-4.json` | `items[6].widget.model` (recommendation) | **imprecise, minor** |
   "Every message is $O(1)$" for the tick array. Two sentences earlier the model says the best-quote pointer must move
   when its level empties, which is a scan over ticks: cheap in practice, not $O(1)$ in the worst case. A learner
   marking their own answer against the model would mark a correct caveat as an error. |
   Basis: derivation; a level that empties with the next live level $t$ ticks away costs $t$ steps. |
   Fix: `**Recommendation.** The array by tick, with a FIFO queue per level and an id dict. Add, cancel and lookup are $O(1)$, and only the best-quote pointer can take longer, when a level empties. Range queries are direct.` (rest unchanged)

### Notes (no finding)

- N1. `homework-4` `items[5]` slip `levels` has value 36 and no feedback line. The bottom level of a 100-item heap holds
  37 items (indices 63 to 99). No claim is made, so nothing is false; if a line is ever added, the value should be 37.
- N2. `l15` `screens[5]`: a recursive `contains` with no `None` case at all fails test 5 (an absent value) with
  `AttributeError`, before test 6. There is no `test-5` line, so that learner sees only the generic line. The `test-6`
  line is true of its test and two of three codings reach it.
- N3. `homework-4` `items[1]`: heap entries of `(value, iterator)` fail test 4 with `TypeError` on the tie. The `test-4`
  line speaks of dropped copies. Item 5 of the same homework teaches that very error, so no change is needed.
- N4. `l18` `screens[5]` option d (quantity set to 0) is a valid tombstone scheme if reads skip it; the `why` says so
  ("unless every read skips it"), so it is correct as written.
- N5. "Most orders on a busy book are cancelled" (`l18` s5, `homework-4` item 7 prompt) is an empirical market fact that a
  simulation cannot test; it matches published cancel-to-trade ratios (SEC MIDAS; Hasbrouck and Saar 2009), marked correct on that basis.

## Code widgets: `test-N` lines and `mutants`

All 15 Python widgets were run under the page's Pyodide 0.27.7 (wasm32, recursion limit 3000) through
`app/tools/code-runner.mjs`, with 150 submissions (`python docs/reports/ds-L4-concepts-r2.py --sweep <pkgs>`): every
solution, starter and mutant, plus two or three natural codings of each named mistake.

- Solutions: 15 of 15 pass. Starters: 15 of 15 fail test 1.
- `mutants`: 24 entries on 11 widgets; **24 of 24 fail their named test first**, with the stated symptom
  (for example l14 s10 mutant 0 gives 412; l17 s5 mutant 0 raises `IndexError` on the last pop; l18 s9 mutants give A1 before A9).
  Four widgets carry no `mutants` (l15 s7, homework items 1, 2 and 8); their lines were swept the same way.
- `feedback.byKey.test-N`: 51 lines. 49 correct: for each, at least two of my codings of the named mistake fail test N
  first, or the line only describes its test and is true. 2 imprecise (findings 5 and 7).
- The two new 13th tests: `l16` s6 test 13 (zigzag, unbalanced at 3) is the first test failed by all four flag-propagation
  mutants and by my mixed-flag coding; `l18` s9 test 13 is the first failed by all three id-tie mutants. `l15` s5 has 13 tests, all recomputed.
- Timing-dependent results (not lines): `homework-4` item 2 with a linear scan of list heads stops at test 8 after 5 s;
  item 3 with a full re-sort per value stops at test 9 after 5 s. Both are the intended outcome and depend on machine speed.
- Wrong programs that pass every test: one, finding 3. Checked and rejected: full sort in `top_k` (test 11, memory),
  full in-order list in `kth_smallest` (test 8), height at every node in `is_balanced` (test 10), unpruned range walk (test 9),
  `min` + `remove` as `pop` (test 4), fills at the buy price or the midpoint (test 4), one trade per `match` call (test 4).

## Tool results

- `node tools/validate.mjs`: 0 errors, 4,610 warnings (repository-wide; unchanged by this audit, `manifest.json` untouched).
- `node tools/run-number-scripts.mjs --only ds` (venv Python 3 first on PATH): 1 script, 1 passed, 0 new failures.
- `node tools/grade-all.mjs --file <7 files> --local-cdn <pkgs> --code`: 55 widgets and 15 Python code widgets, 0 failures.
- `docs/reports/ds-L4-concepts-r2.py`: exit 1 (96 pass, 2 fail: findings 1 and 4); with `--sweep`: 150 submissions, 0 unexpected.
- No playthrough was run (not asked of an auditor). The venv's NumPy stack is newer than CI's pins; no figure here depends on it (standard library only).

## Overlap with the earlier reads

Filled after the ledger and the findings above were written. Earlier reads opened then: round 1 `docs/reviews/audit-ds-4.md`
(23 findings, its fix pass and its fix-pass read, 2 findings), `docs/reviews/review-1.8.md` (3 conceptual findings at level 4),
`docs/reviews/answers-2026-11-03.md` (1), and the names only of `docs/reports/ds-L4-*`. `review-1.9.md` has nothing on these files.

| Count | Conceptual findings |
|---|---|
| This audit only | 7 (findings 1, 2, 3, 4, 5, 6, 8) |
| Earlier reads only | 29 (round 1: 23; its fix-pass read: 2; review-1.8: 3; answers-2026-11-03: 1), all fixed before this read |
| Both | 1 (finding 7: the raw `heapq` source check, noted and left unchanged by answers-2026-11-03 and by round 1's overlap note) |

New `wrong` that no earlier read found: **1** (finding 1, minor), in three levels' worth of content (five lessons, a review
and a homework). That is within the convergence rule's limit of one new `wrong` per three levels.

How the findings relate to earlier work, counted as "both" only for the same defect:

- Finding 1 (`l14` s7, sorting "hides the bug") is old text that round 1 marked correct in its ledger; neither round 1 nor its fix pass touched it.
- Finding 3 is the same class as review-1.8's `merge_k` warning (`sorted` passed; fixed by `NO_SORT`) but a different program: one heap of all items.
- Finding 4 is on the item whose `explain` round 1 (finding 16) and the fix-pass read (F2) reworded; neither raised the unstated duplicate convention.
- Finding 5 is on a line that round 1's fix pass wrote (its finding 18). The line is right for the mistake it names; the second cause is new.
- Findings 2, 6 and 8 are on text no earlier read questioned.
- All 25 lines round 1 and its fix-pass read changed were re-read here as ledger rows: 24 correct, 1 imprecise (finding 5). The five `wrong` of round 1
  (l15 s6 "go left at 10", l16 s4 `test-2`, l14 s9 slip `gross`, review-4 item 4 option d, l17 quiz 2 option d) are all correct now;
  the last is confirmed by 10,000 random runs (`l17 quiz1 d` check).
- Both new hidden tests (13) and all 24 `mutants` hold: see "Code widgets" above.

## Fix pass

Opus fixer, from commit 50fc0df9. Each basis is the fixer's own derivation or source; own checks in the scratch folder
`fix-ds4r2/checks.py` and a 12-submission Pyodide sweep (`fix-ds4r2/subs.py`), not the auditor's code.

1. **fixed** (l14 s7 `byKey.d`, option d `why`). Basis: walking the A to G tree gives in-order D B E A F C G; the buggy walk sorted gives A B C D E F G, so sorting returns a wrong answer here and hides nothing (CLRS 12.1: in-order follows positions).
2. **fixed** (l18 s5 hint 0, `explain` last sentence joined with a semicolon to stay at three sentences, `summary.ideas[2]`). Basis: an own indexed heap (position dict, move last into the hole, sift up then down) kept the heap rule over 3,000 deletes on 4,095 items, at most 21 comparisons each, under 2 log2 n = 24; CLRS ch. 6.5 HEAP-DELETE exercise. CPython `heapq` docs ("Priority Queue Implementation Notes") recommend marking entries removed, since the public API has no sift: the claims now name `heapq`.
3. **fixed differently** (homework-4 item 2). Added one hidden test 9, `peak_heap(...20 lists of 100...) <= 20`; `NO_SORT` is now test 10; `how` and `feedback.byKey.test-9` added; 3 `mutants` (heappush every item, heapify the joined lists, push every `(value, list, position)` entry), all failing test 9. Differs from the audit's prelude: it patched the shared `heapq` module, which persists in the page's one Pyodide and would nest wrappers on every run. The prelude instead puts a counting copy in `sys.modules`, unwraps any earlier copy, and the postlude puts the real module back; `merge_k` keeps the copy it imported, `from heapq import ...` included. Smaller input than the audit's (2,000 items, 3 to 5 ms). Pyodide sweep: model, `heapq.merge`, `heapreplace`, `import heapq as hq` and `from heapq import *` codings all PASS; four one-heap codings fail test 9; `sorted` fails test 10. Model test 8 at 224 ms against 5 s with the wrapper.
4. **fixed** (review-4 item 5 prose). Basis: own check, `[8, 3, 10, 3, 6, None, 14]` is a search tree under CLRS's `<=` rule and not under the strict one; lesson 15 states the strict rule ("not inserted again", "strictly above"), so the prose now states it before the learner answers.
5. **fixed** (l17 s5 `test-5`). Basis: Pyodide sweep, three codings that read `2i + 2` unchecked (`l < n` loop, `min` over both children, a `smallest` loop) all fail test 5 first with `IndexError: list index out of range`; the line now names both causes.
6. **fixed** (l17 s2 `explain`). Basis: a worst-case push climbs from depth floor(log2 n) to 0, so swaps are levels minus one of the tree holding the new item; own run, 1,000,000 items, 19 swaps, 20 levels, matching the s4 key.
7. **fixed** (content only: l17 s5 `how` last sentence, `test-11`). Basis: test 11 is `'heapq' not in __learner_source__`; own Pyodide run of a correct hand-written heap with the comment `# written by hand, no heapq` fails test 11. The test is unchanged (rule 4: the finding does not require it).
8. **fixed** (homework-4 item 7 `model`). Basis: own tick-array run, emptying the best level with the next live bid 500 ticks away moves the pointer 500 steps; add, cancel and lookup stay $O(1)$.

Gates: validator 0 errors (4,610 warnings, unchanged); voice scan 35 on the five files 0 and 0; `ds-L4-concepts-r2.py` exit 0 (99 checks), with `--sweep` 153 submissions, 0 unexpected; `ds-L4-concepts.py` and `ds-L4-fixread.py` exit 0; `run-number-scripts --only ds` 1 passed; `grade-all --code` on the five files 0 failures; playthrough of l14, l17, l18, review-4, homework-4 green desktop and `--mobile`. Re-pointed in `ds-L4-concepts-r2.py` (docstring says so): "hw i1 expects" skips the new peak test, a new check covers it, and the H2 sweep expects test-9 and test-10 where the test list moved.
