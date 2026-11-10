# Brief: Phase 4 drill packs 1 to 4 (pack `ci`, 60 drills; PLAN 2d item D and 2a "Drill packs 1 to 4"; `docs/briefs/interview-plan.md` line 202)

The developer route's volume: interview-level problems after `coding-int`, harder than the `dsa` pack. Everything in `docs/briefs/drills-1.8.md` holds (shape, fields, stdin variant, fresh rule, checks 1 to 5, its check 4a) except where this brief differs. Pattern file: `app/content/drills/ci-pair-gaps.json`. Read two finished `dsa-` drills of your patterns first so you do not repeat them: a `ci` drill is a harder problem, never a `dsa` drill with bigger numbers.

## Differences from the 1.8 brief

- Files `app/content/drills/ci-<slug>.json`, `"pack": "ci"`, `"course": "coding-int"`, `skills` from skills the `coding-int` lessons declare. Python only.
- `difficulty` 2 to 5 per pack of 15: three at 2, five at 3, five at 4, two at 5. `pace` 900 to 2,700 seconds. At 4 and 5 the obvious method must fail the large hidden test on time, and `how` names the step from the obvious method to the target one.
- Two stdin drills a pack, not three.
- `tags`: `"pack-<n>"` first, so the pack can be drawn by number.
- **Planted wrong solutions (ENGINE-BACKLOG 844, AUTHORING section 5, required here).** Every drill carries `planted`: two or three wrong solutions a real candidate writes (off by one at the boundary, the tie broken the wrong way, the empty input not handled, the greedy that fails one case, the right idea at the wrong complexity), each with its `slip` sentence. Every one must fail at least one hidden test. If one passes, the tests are too weak: add the test that catches it; never weaken the planted solution.
- `notes`: each of the three lines must be true of this drill's own solution; a reason you cannot show from the code does not go in (two reviews found false reasons there).

## Packs (one agent each, 15 drills)

| Pack | Patterns | Ideas to cover |
| --- | --- | --- |
| 1 | `hashing`, `prefix-sums` | arrays and hashing: grouping by a computed key, counting pairs by complement, longest run by set lookups, subarray sums with a prefix map, products without division, two-dimensional prefix sums, frequency buckets |
| 2 | `two-pointers`, `windows` | sorted-array pair and triple search, partitioning in place, merging from the back, shrinking windows with a count map, windows with at most k of something, fixed windows with a deque maximum |
| 3 | `stacks-queues`, `binary-search` | monotonic stack spans and next-greater on a circle, expression evaluation, largest rectangle, a queue from two stacks under load, search in a rotated list, first and last position, search on the answer with a feasibility check |
| 4 | `trees`, `heaps-tries` | lowest common ancestor, path sums, serialise and rebuild, level views, validate with bounds, k-way merge, running median with two heaps, top k by frequency, prefix lookups and word search with a trie |

## Checks (all required before hand-back)

1 to 5 as the 1.8 brief, with the names `docs/reports/drills-ci-<n>-check.py` and `docs/reports/drills-ci-<n>.md` and the inbox heading `Raised later (drills ci <n>):`. The check script also runs every planted solution in CPython and asserts it fails a test.
6. From `app/`: `node tools/planted-check.mjs --drill <id> --require --local-cdn <pkgs>` for all 15: green.

Do not edit engine files, `course.json`, lessons, or other agents' drills. Commit in your worktree with "drills ci pack <n>" in the message; never push.
