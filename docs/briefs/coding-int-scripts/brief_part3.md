
## Level 3

You are a content agent on the Zero to Quant build in /home/user/zero-to-quant. Author course `coding-int` (topic 3.5), level 3 ("Design in code"): lessons `l11-lru-cache`, `l12-file-system`, `l13-requirements-change`, `l14-rate-limiter`, plus `review-3.json` and `homework-3.json`, in `app/content/courses/coding-int/`. Follow `docs/LEVEL-BRIEF.md` exactly and read `docs/AUTHORING.md` in full; use the lesson names, objectives and skill ids of `course.json` exactly. Use £ for money (prices in l13 are whole £). Scripts: `l3.py` (every problem of this level; the C++ LRU; random cross-checks), `harness.py`, `numbers_check.py`.

Level promise. Interviews at developer and strats desks and at some trading firms set a design problem in code: several small classes, a clear interface, and a requirement that arrives half-way. This level builds four such systems and teaches how to keep code open to change. Python by default; the LRU cache has a C++ twin.

**Engine features.** E11 (`parts`) in homework item 5. E3, E8 and E14 are not needed. Existing: `code` (a hidden driver in `postlude` replays operations; `__learner_source__` checks; C++ `postlude` driver), `array` (linked mode) for lists, `tree` for the folder tree, `table`, `order`, `choice`, `multi`, `longform`. Staged problems (l12, l13) use one `code` screen per stage; each later stage's starter is the reference solution of the previous stage plus stubs for the new methods, so every screen is self-contained.

**Builds on (by id) and what is new.**

| Lesson | Builds on | New over those |
| --- | --- | --- |
| l11-lru-cache | `ds` homework-3 h-lru (the Python LRU with sentinels), `ds` l12-nodes-and-pointers, `cpp` l15-maps | A from-memory recall against the clock, the C++ version with `std::list::splice` and an iterator map, a TTL cache where recency order is also expiry order, and LFU in homework. |
| l12-file-system | `py-found` l12-data-with-behaviour, `ds` l14-binary-trees, `ds` l16-tree-recursion | A tree of nodes that are folders or files, paths split on `/`, `mkdir -p` and append semantics, a recursive size. |
| l13-requirements-change | `py-found` l8-who-changes-the-list, `contests` l16-upsolving | Extending working code in three stages (positions, average cost, FIFO lots) so that earlier tests keep passing. |
| l14-rate-limiter | `ds` l11-first-in-first-out (the single-client sliding log), `ds` l7-prefix-sums | Per-client logs, fixed window against sliding log against token bucket with numbers, a token bucket in code, a ring-buffer hit counter in homework. |

### l11-lru-cache (14 min; tags `lru-cache`, `cache-ttl`, `cache-lfu`)

Objective: Combine a hash map and a linked list for constant-time get and put. The learner built this in `ds` homework-3; the lesson is the interview version: from memory, against a pace of 480 seconds, then in C++, then with expiry. Method stated after use: the dict maps a key to its node, the doubly linked list orders nodes by recency (head side most recent), sentinels remove the empty-list special cases, and every get or put moves its node to the front; when full, drop the node before the tail sentinel.

Screens (11):
1. Hook `problem`, `array` (linked mode) holding keys 2, 5, 9, most recent first; `order`: put the steps of `get` of key 9 in order (look up the node, unlink it, push it to the front, return its value; return -1 first if the key is absent).
2. `explore`, `array` with pointers `head` and `tail`; `choice`: which pointer assignments unlink a node (four assignments; the learner who writes only two leaves a dangling `prev`).
3. `problem`, code A, Python `LRUCache` (`pace` 480; no `OrderedDict`; the hidden tests check `'OrderedDict' not in __learner_source__`). Prose names `ds` homework-3 and says an interviewer often forbids the library class.
4. `ladder`, `numeric`: a cache of capacity 1 with the operations put 2 (value 1), get 2, put 3 (value 2), get 2, get 3: the gets return `1, -1, 2`; ask how many gets miss: 1.
5. `ladder`, code A in C++ (same tests): `std::list<std::pair<int,int>>` and `std::unordered_map<int, std::list<...>::iterator>`; `splice` moves a node in `O(1)` without invalidating iterators. Prose says why `std::list` iterators stay valid.
6. `trap`, `choice`: `put` of an existing key must update the value and move it to the front, not evict; the learner who evicts first on a full cache loses a live key (capacity 2: puts 1, 2, then 1 again). Name the action in `byKey`.
7. `problem`, code B, Python `TTLCache` (below): a use refreshes the entry.
8. `ladder`, `choice`: why the expired entries are exactly a suffix of the recency list (the time of last use is non-decreasing from the tail to the head); the learner picks the sentence that says so.
9. `generalise` + `derive` (`order` the steps of a `put`).
10. `transfer`, `choice`: LFU against LRU for a pricing service with a few very hot symbols and a long tail of scans; why a scan evicts hot keys under LRU (the lesson leads into homework item 1).
11. `transfer`, `numeric`: with a cache of 1,000 entries, 100,000 puts of keys 0 to 99,999, then gets of keys 99,000 to 99,999 and of key 0: the surviving keys are 99,000 to 99,999 and key 0 is gone, so the gets sum to 99,499,499 (`99,499,500 - 1`; by the closed form and by running the reference).

Quiz (4): a trace; a pointer update; capacity 1; the expiry rule.

**Problem 11.1** `LRUCache(capacity)` with `get(key)` and `put(key, value)`; Python and C++ twin; difficulty 4. Statement: "`get` returns the value or -1 and counts as a use; `put` inserts or updates and counts as a use; at capacity, `put` of a new key first drops the least recently used entry. Both are `O(1)`." Driver `run_lru(cap, ops)`: `ops` rows are `[0, key, value]` for `put` and `[1, key]` for `get`; the driver returns the list of `get` results. Reference (sentinels, no library class):

@@PY:l3:LRU_REF@@

Driver (`postlude`):

@@PY:l3:LRU_POST@@

Starter (a plain dict that never evicts; fails 6 of 8):

@@PY:l3:LRU_START@@

@@T:l3:lru@@

C++ twin: the same seven cases without the source check (six trace cases and the large case: 100,000 puts, 1,000 gets of the newest keys and one get of key 0, summed into a `long long`, expected 99,499,499). Driver in `postlude`, reference, starter (a plain `unordered_map`, fails 6 of 7). Compiled and run under `-std=c++17` and `-std=c++20`; the expected values come from the brute force `lru_brute` (a list of keys, `O(n)` per operation) on the small cases and from the closed form on the large one.

@@CPP:l3:LRU_CPP_REF@@

@@CPP:l3:LRU_CPP_START@@

@@CPP:l3:LRU_CPP_POST@@

**Problem 11.2** `TTLCache(capacity, ttl)` with `get(key, now)` and `put(key, value, now)`; Python; difficulty 4. Statement: "Times are whole seconds and never go backwards. An entry that was last used (by `get` or `put`) `ttl` or more seconds ago has expired: `get` returns -1 for it and it takes no room. A use refreshes the entry and makes it the most recent. When a new key arrives and the cache is full after expired entries are dropped, drop the least recently used." Driver `run_ttl(cap, ttl, ops)` with rows `[0, key, value, now]` and `[1, key, now]`. Reference (purges from the tail, which is enough because the order of last use is the order of expiry), starter (a dict, fails 6 of 6), tests (brute force: purges every expired key in a list on each call; 4,000 random runs agreed):

@@PY:l3:TTL_REF@@

@@PY:l3:TTL_POST@@

@@PY:l3:TTL_START@@

@@T:l3:ttl@@

### l12-file-system (14 min; tags `file-system`, `path-tree`, `recursive-size`)

Objective: Design classes for a small file system with paths, folders and files. Method stated after use: one `Node` class with a dict of children and a `content` that is `None` for a folder and a string for a file; a helper walks a path one name at a time and may create what is missing; every public method is a few lines on top of the helper.

Screens (10):
1. Hook `problem`, `tree` of `/a/b/c` with a file `d.txt` under `c`; `tap-regions`: tap the nodes `ls('/a')` lists (`b` only).
2. `explore`, `tree` with a control stepping `mkdir('/a/b/c')`; `numeric`: how many folders exist afterwards (3: `a`, `b`, `c`).
3. `ladder`, `choice`: `ls` of a file path returns the file name in a list, of a folder the sorted names inside it.
4. `ladder`, `choice`: `write` to a path whose folders do not exist creates them (like `mkdir -p`) and appends to a file that exists; the second write of `' world'` makes `'hello world'`.
5. `problem`, code A, Python `FileSystem` with `mkdir`, `write`, `read`, `ls`, `pace` 840, difficulty 4.
6. `trap`, `choice`: `'/'.split('/')` returns two empty strings; a path walker that does not skip empty names looks for a child named `''`. Name the action in `byKey`.
7. `ladder`, `numeric`: files `/logs/a.txt` (`abcd`), `/logs/old/b.txt` (`xy`) and `/logs/c.txt` (`abcdef`): `size('/logs')` is 12 and `size('/logs/old')` is 2 (by the tree and by adding the lengths).
8. `problem`, code B, extend the class with `size(path)` (recursive; the starter is the reference of A without `size`).
9. `generalise` + `derive` (`order` the walk).
10. `transfer`, `choice`: a design question an interviewer asks next ("add `rm`", "add `find(name)`", "add file permissions"): the learner sorts each into "one new method" or "a new field on `Node`".

Quiz (4): a path split; `ls` of a file; `mkdir` twice; a size.

**Problem 12.1** `FileSystem` with `mkdir(path)`, `write(path, text)`, `read(path)`, `ls(path)` (stage A) and `size(path)` (stage B); Python; difficulty 4. Statement: "Absolute paths start with `/`, the root is `/`. `mkdir` creates every missing folder and does nothing if the folder exists. `write` creates missing folders and the file and appends `text` to its content. `read` returns a file's content. `ls` of a folder returns the names inside it sorted (files and folders together); `ls` of a file returns a one-element list with its name. `size` of a file is the number of characters of its content; of a folder the total of every file below it. Inputs are valid: no operation uses a file as a folder." Driver `run_fs(ops)` with rows `('mkdir', path)`, `('write', path, text)`, `('ls', path)`, `('read', path)`, `('size', path)`, returning the results of `ls`, `read` and `size`. Reference, driver, starter (fails 5 of 6; stage A tests are rows 1 to 4 and 6, stage B adds row 5), tests (brute force: flat sets of folders and a dict of files keyed by the full path; 3,000 random valid sequences agreed):

@@PY:l3:FS_REF@@

@@PY:l3:FS_POST@@

@@PY:l3:FS_START@@

@@T:l3:fs@@

### l13-requirements-change (15 min; tags `requirements-change`, `average-cost`, `fifo-lots`)

Objective: Extend working code when the interviewer adds a requirement part-way. Skills `ci-design` and `ci-timed`. Method stated after use: keep the old calls valid (a new argument gets a default), add the new behaviour behind a name, run the old tests first, and only then the new ones. The running story is a trade ledger at a small desk, prices in whole £.

Stage 1: `Ledger()` with `trade(symbol, qty)` (signed whole shares, positive buys) and `position(symbol)`. Stage 2: `trade(symbol, qty, price=0)` keeps old calls valid; add `avg_cost(symbol)` and `realised(symbol)`; a sale realises `qty * (price - average cost)`; selling more than held raises `ValueError`. Stage 3: `Ledger(method='average')` or `Ledger(method='fifo')`; under `'fifo'` a sale consumes the oldest lots first and `avg_cost` is the average of the lots still held; the earlier tests must still pass.

Screens (11):
1. Hook `problem`, `table` of three trades (buy 100 at £10, buy 100 at £12, sell 150 at £13); `numeric`: position after the three (50).
2. `problem`, code A, stage 1 (`pace` 300, difficulty 2).
3. `ladder`, `numeric`: average cost after the two buys: £11. Realised on the sale by average cost: 150 times (13 minus 11) = £300.
4. `problem`, code B, stage 2 (starter: the reference of stage 1 with the new signatures stubbed; the tests include the stage 1 test).
5. `trap`, `choice`: adding `price` as a required argument breaks every old call; the learner who does that fails the stage 1 test. Name the action in `byKey`.
6. `ladder`, `numeric`: the interviewer asks for FIFO: realised on the same trades is 100 times (13 minus 10) plus 50 times (13 minus 12) = £350; the remaining lot is 50 at £12, so `avg_cost` is £12.
7. `problem`, code C, stage 3 (the tests of stages 1 and 2 plus the FIFO cases).
8. `ladder`, `choice`: which of two designs absorbs a fourth requirement (short selling) with the fewest changes: lots held in a deque, or only a running average; the learner chooses and a `why` names the cost.
9. `generalise` + `derive` (`order` the steps of absorbing a change).
10. `transfer`, `choice`: how an interviewer scores this (reading the new requirement, keeping old tests, naming the cost) and what to say aloud in the first minute.
11. `transfer`, `numeric`: trades `(10, £50)`, `(-4, £55)`, `(10, £40)`, `(-12, £45)` give realised £20 under FIFO and £35 under average cost (the homework item has this; use a different list in the lesson, computed twice).

Quiz (4): a position; an average cost; a FIFO lot; an old call.

**Problems 13.1 to 13.3** `Ledger`, three stages; Python; difficulty 2, 3 and 4. Tests use a `setup` line that builds a `Ledger` and replays trades, and a call that reads `[position, avg_cost, realised]` with `compare: "isclose"`. Stage 1 reference and starter (fails 2 of 3), tests:

@@PY:l3:LED1@@

@@PY:l3:LED1_START@@

@@T:l3:led1@@

Stage 2 reference (stage 2 tests include the stage 1 test as the last row), starter (fails 6 of 7):

@@PY:l3:LED2@@

@@PY:l3:LED2_START@@

@@T:l3:led2@@

Stage 3 reference (every earlier row plus four FIFO rows), starter (fails 10 of 11):

@@PY:l3:LED3@@

@@PY:l3:LED3_START@@

@@T:l3:led3@@

Checks: the incremental references were compared with a brute force that replays the whole history (lots in a list, recomputed from scratch) on 3,000 random trade lists, for both methods, with `isclose`. The worked numbers (50 held, average £11, realised £300; FIFO £350 and £12) come from that brute force and from the hand sums above.

### l14-rate-limiter (13 min; tags `rate-limit-log`, `token-bucket`, `rate-limit-window`)

Objective: Design a sliding-window counter and a rate limiter for timestamped events. Method stated after use: a sliding log keeps the accepted times of one client in a deque, drops those at or before `t - window`, and accepts only if fewer than `limit` remain; a token bucket holds up to `capacity` tokens, refills `rate` per second and spends one per request.

Screens (11):
1. Hook `problem`, `array` (queue mode) showing the log `[5, 6]` with limit 2 and window 10; `choice`: of three separate requests, at 14, at 15 and at 16, which are accepted? 14 no (both 5 and 6 are above 4), 15 yes (5 is not above 5, so only 6 counts), 16 yes (neither is above 6).
2. `explore`, `array` with a time control; the window slides.
3. `ladder`, `numeric`: with limit 2 and window 3 the times `0, 1, 2, 3, 4, 5` give `True, True, False, True, True, False`: four accepted.
4. `problem`, code A, Python `RateLimiter(limit, window)` with `allow(user, t)` (a dict of deques; `pace` 600). Prose says it extends the one-client version of `ds` l11.
5. `trap`, `choice`: a rejected request must not be recorded; the learner who appends before checking locks a client out for ever. Name the action in `byKey`.
6. `ladder`, `numeric`: a fixed one-minute counter with limit 100 admits 100 requests at second 59 and 100 more at second 60: 200 within two seconds; a sliding log admits 100 (computed by running both).
7. `problem`, code B, Python `TokenBucket(capacity, rate)` with `allow(t)`, `pace` 600, difficulty 4.
8. `ladder`, `numeric`: a bucket of capacity 2 with rate 2 gives, for the times `0, 0, 0, 1, 1, 1`, the answers `True, True, False, True, True, False`: four accepted (by the program and by adding tokens second by second).
9. `generalise` + `derive`.
10. `transfer`, `choice`: memory when a million clients each make one request: the log holds a million deques; the learner chooses to drop an idle client's entry when its deque empties.
11. `transfer`, `choice`: which limiter fits (a) a hard cap per minute on an exchange gateway (sliding log), (b) bursts allowed but a steady average (token bucket), (c) a cheap counter with some error (fixed window).

Quiz (4): an accept at the edge; a rejected request; a bucket after a pause; a limiter choice.

**Problem 14.1** `RateLimiter(limit, window)` with `allow(user, t)`; Python; difficulty 3. Statement: "Times are whole numbers that never go backwards. A request at `t` counts the accepted requests of the same user at times greater than `t - window`; it is accepted when that count is below `limit`. A rejected request is not recorded." Driver `run_limiter(limit, window, calls)` with `calls` rows `[user, t]` returning the list of accepted flags. Reference, driver, starter (a counter that never forgets; fails 6 of 6), tests (brute force: a list of accepted times per user, scanned; 3,000 random runs; the last case has 60,000 requests of one user and expects 1,000 accepted, by the closed form `20,000 s / 100 s * 5`):

@@PY:l3:RL_REF@@

@@PY:l3:RL_POST@@

@@PY:l3:RL_START@@

@@T:l3:rl@@

**Problem 14.2** `TokenBucket(capacity, rate)` with `allow(t)`; Python; difficulty 4. Statement: "The bucket starts full at time 0. Each whole second adds `rate` tokens, never above `capacity`. A request at `t` first adds the tokens for the time since the last request, then spends one token if it has at least one (accepted) or is rejected. `rate` and times are whole numbers." Driver `run_bucket(capacity, rate, times)`. Reference, driver, starter (allows the first `capacity` requests only; fails 5 of 6), tests (brute force: advances second by second; 3,000 random runs; the last case sends 4 requests a second for 50,000 seconds with capacity 10 and rate 1: 10 + 49,999 = 50,009 accepted, by the closed form and by the reference):

@@PY:l3:TB_REF@@

@@PY:l3:TB_POST@@

@@PY:l3:TB_START@@

@@T:l3:tb@@

### Level 3 review (`review-3.json`, 10 items, difficulty 2 to 4, interleaving all four lessons, every case unseen in the lessons, each with `tags` and `skills`)

| # | Lesson | Widget | d | Prompt (summary) | Key |
| --- | --- | --- | --- | --- | --- |
| 1 | l11 | `numeric` | 3 | Capacity 2; put 1, put 2, get 1, put 3, get 2, put 4, get 1, get 3, get 4 (values equal to keys). Sum of the gets. | 6 (`1, -1, -1, 3, 4`) |
| 2 | l11 | `choice` | 3 | Capacity 3; put 1, 2, 3; get 1; put 4; get 3. Which key was evicted? | 2 (recency, most recent first: 3, 4, 1) |
| 3 | l11 | `numeric` | 3 | TTL cache, capacity 2, ttl 5: put key 1 at time 0; get at times 4, 8, 13, 14. How many return -1? | 2 (ages 4, 4, 5, then gone) |
| 4 | l12 | `numeric` | 3 | Files `/docs/n/a.txt` (12345), `/docs/n/b.txt` (678), `/docs/c.txt` (9): `size('/docs')`. | 9 (`size('/docs/n')` is 8) |
| 5 | l12 | `choice` | 3 | After `mkdir('/b')`, `mkdir('/a')`, `write('/c.txt', '1')`, `mkdir('/a/z')`: what does `ls('/')` return? | `['a', 'b', 'c.txt']` |
| 6 | l13 | `numeric` | 3 | Buy 200 at £20, buy 100 at £23, sell 250 at £25: realised £ under FIFO. | 1,100 (`200 * 5 + 50 * 2`; average cost, £21 on 300 shares, gives `250 * 4 = 1,000`) |
| 7 | l13 | `choice` | 3 | Why does `trade(symbol, qty, price=0)` keep the stage 1 tests passing? | Old calls pass two arguments and the default fills the third. Distractors: Python ignores extra arguments; the tests are not run again; `price` is optional in every language. |
| 8 | l14 | `numeric` | 3 | Limit 3, window 10, requests at 1, 2, 3, 4, 10, 11, 12: how many are accepted? | 5 (`T T T F F T T`) |
| 9 | l14 | `numeric` | 3 | Bucket capacity 3, rate 1, requests at 0, 0, 0, 0, 1, 1, 2, 10: how many are accepted? | 6 |
| 10 | l14 | `choice` | 3 | A hit counter that only needs the last 300 seconds: what does a ring of 300 buckets cost as traffic grows? | Constant memory, 300 slots. Distractors: memory proportional to the hits, to the clients, to the seconds so far. |

### Level 3 homework (`homework-3.json`, 8 items, difficulty 3 to 5 with at least one 5, `tags` on each; two `code` items, one `longform`, one E11 `parts` item)

| # | Lesson | Kind | d | Item | Key or reference |
| --- | --- | --- | --- | --- | --- |
| 1 | l11 | `code` | 5 | `LFUCache(capacity)` (below). | tests below |
| 2 | l14 | `code` | 3 | `HitCounter` (below). | tests below |
| 3 | l14 | `longform` | 4 | Say aloud, timing yourself to three minutes: design a per-client rate limit for an exchange gateway. Compare fixed window, sliding log and token bucket on accuracy, memory and bursts, with the 200 against 100 example. | Model: a fixed window lets 200 requests through in two seconds around a boundary; a sliding log lets 100 and costs memory per request; a token bucket bounds the average and allows a burst of the capacity. Rubric (10): 2 states the three designs, 2 the boundary burst with numbers, 2 memory per design, 2 burst behaviour of the bucket, 2 a justified choice. |
| 4 | l14 | `numeric` | 4 | Limit 100 per minute. 100 requests arrive at second 59 and 100 at second 60. How many does a fixed one-minute counter admit? | 200 (a sliding log admits 100; both run in a script) |
| 5 | l13 | `parts` (E11), `numeric` ×3 | 4 | Trades `(10, £50)`, `(-4, £55)`, `(10, £40)`, `(-12, £45)`. Part 1: realised £ by average cost. Part 2: realised £ by FIFO. Part 3: average minus FIFO. | 35, 20, 15 (working below) |
| 6 | l11 | `order` | 4 | The steps of `get`: look up the node (return -1 if absent); unlink it; push it to the front; return its value. | Distractor: "delete the node and create a new one" with its `why` (the dict entry then points at a dead node). |
| 7 | l11 | `multi` | 3 | Which are `O(1)` with a dict of nodes and a doubly linked list: `get`, `put` of a new key at capacity, delete by key, list all keys in recency order, find the median key. | `get`, `put`, delete by key. The last two are `O(n)` and `O(n log n)`. |
| 8 | l11 | `numeric` | 5 | LFU with capacity 2 on `put 1, put 2, get 1, put 3, get 2, get 3, put 4, get 1, get 3, get 4` (values equal keys; ties go to the least recently used): sum of the gets. | 9 (`1, -1, 3, -1, 3, 4`; traced by hand and by the brute force) |

The working for item 5 above, stated plainly for the level agent: average cost after the first buy is £50; the sale of 4 at £55 realises `4 * (55 - 50) = £20`; 6 shares at £50 remain; the buy of 10 at £40 brings 16 shares at an average of `(6 * 50 + 10 * 40) / 16 = £43.75`; the sale of 12 at £45 realises `12 * (45 - 43.75) = £15`; total £35. FIFO: the first sale uses the £50 lot, realising £20; the second uses the 6 remaining £50 lots (`6 * (45 - 50) = -£30`) and 6 of the £40 lot (`6 * (45 - 40) = £30`); total £20. The difference is £15. (Both methods were computed in `numbers_check.py`.)

**Problem H3.1** `LFUCache(capacity)` with `get(key)` and `put(key, value)`; Python; difficulty 5. Statement: "As `LRUCache`, but when full drop the entry used the fewest times; ties go to the least recently used of those. A `get` or `put` of an existing key counts as a use; a new key starts at one use. Capacity 0 stores nothing. Both are `O(1)`." Driver `run_lfu(cap, ops)` as `run_lru`. Reference (frequency buckets of ordered dicts and a minimum frequency), starter (a plain dict; fails 6 of 7), tests (brute force: evicts by `min` over `(frequency, last use)`; 4,000 random runs agreed):

@@PY:l3:LFU_REF@@

@@PY:l3:LFU_POST@@

@@PY:l3:LFU_START@@

@@T:l3:lfu@@

**Problem H3.2** `HitCounter` with `hit(t)` and `count(t)`; Python; difficulty 3. Statement: "`hit(t)` records a hit at whole second `t`; `count(t)` returns the hits at times greater than `t - 300` and at most `t`. Calls come in non-decreasing time. Use a fixed amount of memory." Driver `run_hits(ops)` with rows `[0, t]` for `hit` and `[1, t]` for `count`. Reference (a ring of 300 buckets), driver, starter (counts every hit ever; fails 4 of 5), tests (brute force: a list of times; 2,000 random runs; the last case sends 50,000 hits at even seconds to 99,998 and counts at 99,999: 150):

@@PY:l3:HC_REF@@

@@PY:l3:HC_POST@@

@@PY:l3:HC_START@@

@@T:l3:hc@@

### Level 3 report notes

Report as `docs/LEVEL-BRIEF.md` says. Do not edit files outside `app/content/courses/coding-int/`.
