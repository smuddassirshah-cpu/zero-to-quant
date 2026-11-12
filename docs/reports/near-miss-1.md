# Near-miss pass, part 1

64 drills (`near-miss-1`). Validator: 0 errors, 0 `[near-miss]` warnings on this list. `planted-check --near-miss` in the real runtime: 0 failures in every batch.

## Per drill

- ci-balanced-run: wrote new (plant 0) | Overwriting the stored position for each running total measures from the nearest earlier match, not the earliest, so a longer balanced run is missed.
- ci-basket-cover: existing (plant 2) | Shrinking by one trade per step with `if`, not `while`, records covers that are not yet as short as they can be.
- ci-best-block: existing (plant 1) | Its loops stop one short, so blocks touching the last row or column are never tried.
- ci-best-route-value: existing (plant 2) | Keeping only downward routes never lets a route bend at a depot to join two branches.
- ci-best-session: existing (plant 0) | Starting afresh after a run that totals exactly 0 loses the earlier start of an equal run.
- ci-board-words: existing (plant 0) | Never putting a letter back after a walk returns blocks that cell for every later start.
- ci-broken-steps: existing (plant 1) | Allowing only strides of 1 and 2 forgets the stride of 3.
- ci-busiest-links: existing (plant 1) | `most_common` breaks ties by first appearance, not alphabetically.
- ci-camera-cover: existing (plant 1) | It closes each rectangle at `r2` and `c2`, so the last row and column of every camera are lost.
- ci-capped-repeats: existing (plant 1) | Shrinking while a count is `>= m` refuses a stretch that holds an id exactly `m` times.
- ci-capped-trips: existing (plant 4) | The shortcut for a large `k` takes each upward run as its own trip, but with a fee, joining two runs across a small dip can pay more.
- ci-cell-formula: existing (plant 0) | It parses by recursion, which runs out of call depth at the default limit when calls nest thousands deep.
- ci-change-ways: existing (plant 0) | Putting the fares in the outer loop counts each order of the same coins separately.
- ci-cheapest-pairs: existing (plant 0) | Pushing both neighbours of every trade, with no record of what is queued, reaches the same trade twice.
- ci-cheapest-route: existing (plant 2) | Breaking a tie by the smaller previous town settles the end of the route, not its first towns.
- ci-checkpoint-route: existing (plant 1) | Keeping the first search's marks blocks the second leg from cells the courier may cross again.
- ci-clear-rate: existing (plant 1) | It starts the top of the search one below the largest queue, so it can never return that rate.
- ci-code-classes: existing (plant 1) | It keys on the set of letters at each parity, so it drops repeats and merges `axaxb` with `axbxb`.
- ci-cooldown-trades: existing (plant 0) | Buying from `cash[i - k]` allows a buy one day too soon, after only `k - 1` rest days.
- ci-cpp-first-missing: wrote new (plant 0) | Checking only 1 to n and returning n when all are present misses the case where 1 to n are all there, so the answer is n + 1.
- ci-cpp-insert-interval: wrote new (plant 0) | Merging only while the next start is strictly below the new end leaves intervals that merely touch as separate entries.
- ci-cpp-longest-sum-k: wrote new (plant 0) | Overwriting the stored index for each prefix total measures from the latest match, not the earliest, so a longer stretch is shortened.
- ci-cpp-range-sums: wrote new (plant 0) | Keeping the prefix table in int overflows once a rectangle sum passes 2,147,483,647, though the sums reach 10^10.
- ci-cpp-sum-pairs: wrote new (plant 0) | Taking the raw remainder x % k leaves it negative for a negative number, so such a number is never paired with the remainder it needs.
- ci-double-checks: existing (plant 0) | Placing new visits from the start of a job wastes them on minutes later jobs cannot use.
- ci-downward-path-sums: existing (plant 2) | Starting the count of totals empty, without the 0 above the root, misses every run that starts at the root.
- ci-drop-point-routes: existing (plant 0) | Adding up the routes through each drop point counts a route once for every drop point it meets.
- ci-ends-to-target: existing (plant 0) | Always closing the larger end is a greedy that can overshoot when a smaller lot was needed.
- ci-equal-three: existing (plant 1) | It never records the empty start, so balanced stretches that begin with the first call are lost.
- ci-even-desks: existing (plant 1) | Giving each next-strongest trader to the weaker desk is a greedy that an exact split beats.
- ci-even-vowels: existing (plant 1) | It overwrites each pattern with its latest position, so it measures from the nearest match, not the earliest.
- ci-exact-venue-runs: existing (plant 0) | One window counts one stretch per right edge, missing the other good starts that end there.
- ci-excused-outages: existing (plant 2) | Starting a new run at today when the excuses run out throws away the days that could still be kept.
- ci-ferry-timetable: existing (plant 0) | Always waiting for the next sailing misses the one leaving at the very minute the traveller arrives.
- ci-fewest-tokens: existing (plant 1) | Recording the smallest token that reaches each amount finds a fewest payment, but not always the one the tie rule asks for.
- ci-first-circular-rule: existing (plant 2) | Searching from `b` for `a` before each rule is right, but each search can cover the whole chain, too slow.
- ci-first-fit-slot: existing (plant 3) | Trying only gaps that begin at or after `start` misses a gap that `start` falls inside, so the job is pushed past it.
- ci-first-misplaced: existing (plant 2) | The first drop in an in-order read is not always the first misplaced level in preorder.
- ci-flood-reach: existing (plant 2) | A recursive fill is right on small grids but runs out of call depth at the default limit when the wet region is large.
- ci-frame-triples: existing (plant 1) | Adding 1 for a good pair forgets that every rod between `i` and `j` also works with `j`.
- ci-free-block: existing (plant 1) | It finds the largest square of free desks, but a rectangle can hold more.
- ci-funded-projects: existing (plant 1) | Taking the cheapest projects first spends the `k` choices on small profits.
- ci-grace-sessions: existing (plant 1) | Taking the last session's end shrinks a visit when a short session sits inside a long one.
- ci-half-fare-route: existing (plant 0) | Halving the dearest road of the plain cheapest route misses a route that is dearer in full but cheaper with the voucher.
- ci-handoff-distances: existing (plant 1) | A fixed ten levels of jumps reach only 1,023 lines up, too few for a deep tree.
- ci-hold-limit: existing (plant 2) | Counting crates upwards lets row `c` read a row that already holds this crate, so one crate is loaded twice.
- ci-hop-score: existing (plant 1) | Keeping depot `i - k - 1` in the window allows a hop of `k + 1` depots.
- ci-interval-intersections: wrote new (plant 0) | Keeping an overlap only when lo < hi drops the single shared point, which the brief counts as [x, x].
- ci-invoice-matches: existing (plant 0) | Without skipping a repeated amount at the same depth, the same way is listed once for each choice of equal invoices.
- ci-island-shapes: existing (plant 1) | Naming a shape by its search moves, with no mark for stepping back, gives two different shapes one name.
- ci-k-bit-count: existing (plant 1) | Subtracting the count up to `lo` instead of `lo - 1` drops `lo` from its own range.
- ci-kth-gap: existing (plant 0) | It counts pairs strictly closer than the trial gap, so the search lands one past the answer.
- ci-late-fills-merge: existing (plant 1) | The loop stops when the log runs out, so late fills earlier than every logged fill are never copied.
- ci-level-totals: existing (plant 1) | Using `>=` hands a tie to the deeper level.
- ci-light-cargo: existing (plant 3) | The knapsack table over weight is right but has `cap + 1` cells to update for every parcel.
- ci-line-from-pairs: existing (plant 2) | Starting from the smallest name overall picks a middle station when that name is not an end.
- ci-live-median: existing (plant 1) | One shared record of cancelled sizes lets a cancel in one half remove an equal live order from the other.
- ci-log-compactor: existing (plant 0) | It removes each run once but never looks again, so letters that meet after a deletion stay.
- ci-long-mirrors: existing (plant 1) | Growing only from letters misses every stretch of even length.
- ci-long-stairwell: existing (plant 1) | Adding up the whole first row starts from a count of 1 on the steps below 0, where there should be none.
- ci-longest-rising: existing (plant 3) | Scanning the tails from the far end for the place to put a reading is not a binary search, and costs $O(n \times \text{length})$ when the chain is long.
- ci-loop-cables: existing (plant 0) | Pointing rack `a` itself at the other group, not its root, cuts `a` off from the racks it was joined to.
- ci-loop-starts: existing (plant 0) | The skip-ahead greedy finds one working depot, but the brief asks for every one.
- ci-mean-stretches: existing (plant 0) | It never records the empty start, so a stretch that begins on day 0 is not counted.

## Tests added

None. Every marked plant fails at least one existing hidden test.

## Drills not done

None.

## Statement or model faults

None seen.
