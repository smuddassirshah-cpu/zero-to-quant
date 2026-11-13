# Concept audit: algo-think L1 to L3 (round 1, blind)

Auditor: Fable, 12 Nov 2026, branch `claude/fable-audit`. Scope: `app/content/courses/algo-think/` l1 to l14, review-1 to review-3, homework-1 to homework-3 (Stage 1, topic 1.8, full ledger depth). Blind rule kept: `docs/reviews/review-1.8.md`, `docs/reviews/voice-1.8-algo-think.txt` and the 1.8 and algo-think reports were opened only after the ledger and the findings below were committed (WIP commit named in the hand-back).

- Ledger: `docs/reports/audit-algo-think-1-3-ledger.md`, 376 rows: correct 346, wrong 3, imprecise 24, misleading 1, unverified 2.
- Script: `docs/reports/algo-think-L1-3-concepts.py`, 123 checks. It exits 1 at present: 104 pass and 19 fail, and each failing check tests a sentence named in a finding below (the finding number is printed). No check fails for any other reason.
- Code: all 41 Python code widgets were run under CPython 3.13 with the recursion limit at 1000. Every solution passes its tests and no starter does. Pyodide 0.27.7 (local build) confirms the recursion limit of 1000, 16-byte floats and the `max()` error text. There is no C++ in this course.

Findings: 22 (wrong 3, imprecise 18, misleading 1); serious 2, minor 20. Two further rows are `unverified` (U1, U2).

## Findings

1. `l3-memory.json` | `screens[0].prose` (program A), with `screens[0].canvas.derive.caption`, `screens[0].widget.options[0..3]`, `screens[0].hints[2]`, `screens[0].explain.text` | **wrong, serious** | The lesson's model of an O(1) program is `for p in prices[1:]: best = max(best, p)`, and the screen says "A holds 1 extra value" and "O(1) for A". The slice `prices[1:]` builds a new list of n - 1 references before the loop starts, so A's extra space is O(n). Screen 8 of the same lesson teaches exactly this about `prices[::-1]` ("A slice builds a new list of n values"). | Evidence: `tracemalloc` peak for A is 80,040 bytes at n = 10^4 and 800,040 bytes at n = 10^5 under CPython, and 40,044 and 400,044 bytes under Pyodide; a loop over `prices` itself peaks under 2,000 bytes (script, finding 1 and its companion check). Basis: Python docs, sequence types: slicing a list returns a new list. | Fix, in `screens[0].prose`, replace program A by

   ```python
   # A
   best = prices[0]
   for p in prices:
       best = max(best, p)
   ```

   The first pass compares `prices[0]` with itself, which changes nothing; the result is the same (checked). Every other sentence on the screen is then true as it stands. (`l1` screen 0 uses the same slice but makes no memory claim, so it needs no change.)

2. `l3-memory.json` | `screens[5].hints[1].text` | **wrong, minor** | "Days 1 to 3 total $8 - 3$: `pre[4] - pre[1]`." `pre` is `[0, 3, 4, 8, 9, 14]`, so `pre[4]` is 9. 8 - 3 is 5, not the 6 the screen wants, and 8 is `pre[3]`: the off-by-one that `feedback.byKey.test-4` warns against. | Evidence: script; the screen's own explain caption says "$9 - 3 = 6$". | Fix: "Days 1 to 3 total $9 - 3$: `pre[4] - pre[1]`."

3. `homework-1.json` | `items[6].explain.text` | **wrong, minor** | "A million appends with step 10 make about $5 \times 10^{10}$ copies, against about $2 \times 10^6$ with doubling." Doubling from capacity 1 makes 1,048,575 copies for a million appends; $2 \times 10^6$ is the bound $2n$, not the count. | Evidence: script (`total_copies(10**6)` = 1,048,575 = $2^{20} - 1$). | Fix: "A million appends with step 10 make about $5 \times 10^{10}$ copies, against about $10^6$ with doubling. Fixed growth is $O(n^2)$ in total, whatever the step."

4. `l13-quicksort.json` | `screens[7].question`, `screens[7].widget.options[0].text` (the graded key), `screens[4].explain.text` | **imprecise, serious** | The key says that with a random pivot "every input has expected cost $O(n \log n)$", and screen 4 says "the expected cost is $O(n \log n)$ on every input". That theorem needs distinct values. The lesson's own Lomuto partition sends every value equal to the pivot to the left, so on n equal values each partition peels off one value whatever index is drawn: n(n-1)/2 comparisons, every time. The same screen's explain ("Many equal values are still a problem for Lomuto") and quiz 3 ("a run of equal values gives $O(n^2)$") contradict the key. | Evidence: script: 3,000 equal values cost 4,498,500 comparisons with a random pivot; 3,000 sorted distinct values cost under $3 n \log_2 n$. Basis: CLRS 7.4.2 analyses randomised quicksort for distinct elements; problem 7-2 treats equal elements. | Fix: `screens[7].question`: "With a random pivot and distinct values, which input order is the worst case?" `screens[7].widget.options[0].text`: "None in particular: every order has expected cost $O(n \log n)$". `screens[4].explain.text`, first sentence: "A random pivot splits the range unevenly sometimes, but with distinct values the expected cost is $O(n \log n)$ whatever their order."

5. `l13-quicksort.json` | `quiz[2].prose` | **imprecise, minor** | "Quicksort with Lomuto, comparing prices only, sorts three trades" has the key `[(1, 'c'), (5, 'b'), (5, 'a')]`, and the explain assumes "The pivot is c", that is, the last value. The item names no pivot rule, and the quicksort the learner wrote in this lesson draws the pivot at random. Under that version the wrong option `[(1, 'c'), (5, 'a'), (5, 'b')]` also comes out. | Evidence: script: the last-pivot run gives c, b, a; 60 seeds of the random-pivot version give both c, b, a and c, a, b. | Fix: "Quicksort with Lomuto, taking the last value as pivot each time and comparing prices only, sorts three trades: `[(5, 'a'), (5, 'b'), (1, 'c')]`."

6. `l2-big-o.json` | `screens[6].widget.options[3]`, `quiz[0].widget.options[1]`, `summary.ideas[2]` | **imprecise, minor** | Screen 6 defines $f = O(g)$ as an upper bound, then grades "$O(n^2 \log n)$" wrong for $2n \log n + 40n + 9$, and the quiz grades "$O(n^2)$" wrong for $5n$. Both are true statements under that definition. The course uses big O for the smallest class that holds, as most interviews do, but never says so; the same silent convention grades options in `l8` screens 6 and 8 and `homework-2` item 4. The summary line "Doubling $n$ adds a constant to $O(\log n)$, doubles $O(n)$" is likewise true of $\log n$ and $n$, not of everything that is $O(n)$. | Evidence: script: $2n\log_2 n + 40n + 9 \le 60 n^2 \log_2 n$ for $n \ge 2$; $5n \le 5n^2$ for $n \ge 1$. Basis: CLRS 3.1 ($O$ is an upper bound; $\Theta$ is the tight one). | Fix: add to the end of `screens[6].prose`: "Big O is an upper bound, so $n$ is also $O(n^2)$. By convention we quote the smallest class that holds." `screens[6].widget.options[3].why`: "True as an upper bound, but not the smallest class. A sum grows like its fastest term, so $O(n \log n)$ is enough." `quiz[0].widget.options[1].why`: "True as a loose upper bound, but not the smallest class. The inner loop always runs 5 times, so the total is $5n$." `summary.ideas[2]`: "Doubling $n$ adds a constant to $\log n$, doubles $n$ and quadruples $n^2$."

7. `l4-cheap-on-average.json` | `screens[5].widget.options[3].why` | **imprecise, minor** | "Tripling resizes less often, so it copies less in total". False for some run lengths: 4 appends copy 4 elements under tripling and 3 under doubling; 28 appends copy 40 against 31. What is true is the bound: under $1.5n$ against under $2n$. | Evidence: script (tripling copies more at n = 4, 28 to 32, 244 to 256). | Fix: "Tripling resizes less often, and its total stays under $1.5n$ against $2n$ for doubling. It just wastes more spare slots."

8. `l4-cheap-on-average.json` | `screens[0].explain.text` | **imprecise, minor** | "Python's `list.append` works this way, with a slightly smaller growth factor." CPython grows a list by about one eighth, a factor near 1.125, not slightly under 2. | Evidence: script (measured capacity ratio 1.125). Basis: CPython `Objects/listobject.c`, `list_resize`: `new_allocated = newsize + (newsize >> 3) + 6`, rounded to a multiple of 4. | Fix: "Python's `list.append` works this way, with a much smaller growth factor of about 1.125."

9. `l4-cheap-on-average.json` | `quiz[0].feedback.correct`, `quiz[0].widget.options[2].why`, `quiz[0].widget.options[3].why` | **imprecise, minor** | The feedback says "$1 + 2 + \dots + n$ copies" and the whys say the calls copy "$1, 2, 3, \dots$ elements", while the explain says call $k$ copies $k - 1$ elements, total $\tfrac{n(n-1)}{2}$. The two counts differ by $n$. The explain is the one that matches the lesson's rule that writing the new element is not a copy. | Evidence: script. | Fix: `feedback.correct`: "$0 + 1 + \dots + (n - 1)$ copies: quadratic." `options[2].why`: "There is no doubling here: the calls copy $0, 1, 2, \dots$ elements, an arithmetic sum." `options[3].why`: "Vectorising helps whole-array operations. A Python loop of copies is still $0 + 1 + \dots + (n - 1)$."

10. `l8-cost-of-recursion.json` | `screens[6].explain.text` | **imprecise, minor** | "`fib`'s calls shrink by 1, so its tree is $n$ levels deep and doubles on each." Screen 4 has just said `fib` grows by about 1.618 a step, not 2. The levels of `fib(5)` hold 1, 2, 4, 6, 2 calls. | Evidence: script. | Fix: "`fib`'s calls shrink by 1 or 2, so its tree is $n$ levels deep, and the top half of those levels double." (Checked for n = 2 to 17: n levels, and levels 0 to $\lfloor n/2 \rfloor$ are full.)

11. `l8-cost-of-recursion.json` | `screens[8].feedback.correct`; `review-2.json` | `items[8].feedback.correct` | **imprecise, minor** | "$1 + 2 + \cdots + n = 2n - 1$". Written like this it is the arithmetic series of lesson 1, which sums to $\tfrac{n(n+1)}{2}$. The sum meant is the doubling one, $1 + 2 + 4 + \cdots + n$. | Evidence: script ($1 + \dots + 8 = 36$; $1 + 2 + 4 + 8 = 15$). | Fix, `l8`: "$1 + 2 + 4 + \cdots + n = 2n - 1$, which is $O(n)$." `review-2`: "$1 + 2 + 4 + \cdots + n = 2n - 1$ units: $O(n)$."

12. `l6-call-stack.json` | `screens[7].explain.text` | **imprecise, minor** | "The loop pops the last item pushed, so it visits in the same last-in, first-out order as the recursion." With `stack.extend(children(item))` the loop goes depth first, as the recursion does, but takes each node's children last to first. A learner who needs the same visiting order must push the children reversed. | Evidence: script (recursion r, a, a1, a2, b; loop r, b, a, a2, a1). | Fix, second sentence: "The loop pops the last item pushed, so it goes depth first as the recursion does, though it takes each node's children last to first."

13. `l6-call-stack.json` | `quiz[3].widget.options[1].why` | **imprecise, minor** | "Each frame sees only its own names and the module's." A function also reads the names of any function it is defined inside, and the built-ins. The point of the item is that it never sees its caller's names. | Evidence: script (a nested function reads its enclosing function's variable). Basis: Python language reference 4.2.2, resolution of names. | Fix: "You expected `inner` to see `outer`'s `n`. A function sees its own names, then those of the code it is written inside, here the module, never its caller's."

14. `l9-halving.json` | `screens[7].widget.options[1].why` | **imprecise, minor** | "With `<=`, the loop runs once more when `lo == hi`. Then `mid == hi` and `hi = mid` changes nothing, so it never ends." It spins only when `xs[mid] >= target`. When every value is below the target the loop ends with `lo == hi == len(xs)`, and the extra pass reads `xs[len(xs)]` and raises `IndexError`. | Evidence: script (targets 5, 25, 35 spin; target 45 on `[10, 20, 30, 40]` raises `IndexError`). | Fix: "With `<=`, the loop runs again when `lo == hi`. If `xs[mid] >= target`, `hi = mid` changes nothing and it never ends; if `lo` has reached `len(xs)`, `xs[mid]` raises `IndexError`."

15. `l10-search-the-answer.json` | `screens[9].explain.text` | **imprecise, minor** | "Testing every rate from 1,000 up would take hundreds." The limit lies at or above 2,500, so a scan from 1,000 in steps of one order a minute runs at least 1,501 tests. | Evidence: script. | Fix, last sentence: "Testing every rate from 1,000 up would take more than 1,500."

16. `homework-2.json` | `items[5].explain.text` | **misleading, minor** | "The crossing count costs nothing extra, because the merge already compares each pair that matters." The merge does not compare each crossing pair: 64 reversed values have 2,016 inversions, found with 192 comparisons. The count is free because the left half is sorted, so one comparison settles a whole group of pairs. The stated reason would make a learner think the method is still pair by pair. | Evidence: script. | Fix, second sentence: "The crossing count costs nothing extra: the left half is sorted, so one comparison shows that every left item still waiting is bigger."

17. `l13-quicksort.json` | `screens[8].feedback.correct`, `screens[8].explain.text`; `homework-3.json` | `items[6].explain.text` | **imprecise, minor** | "about $2n$ comparisons on average" and "For a million trades that is about 2 million steps". $n + n/2 + n/4 + \dots$ assumes each pivot halves the range. With a random pivot the median costs about $2(1 + \ln 2)n \approx 3.4n$ comparisons; only the minimum or maximum costs about $2n$. The next screen's table ("$2n$ to $4n$") is right. | Evidence: script: exact expectation 3.35n at n = 1,501 for the median, 1.99n for the minimum, 2.97n for the 20th percentile; simulation agrees. Basis: Knuth, "Mathematical Analysis of Algorithms" (1972), mean comparisons of FIND. | Fix, `l13` `screens[8].feedback.correct`: "One side per step, so about $2n$ to $4n$ comparisons on average: $O(n)$." `screens[8].explain.text`: "Quicksort recurses on both sides; quickselect keeps one. If every step halved the range, the work would be $n + n/2 + n/4 + \dots \approx 2n$; random pivots make it about $3.4n$ for a median, still $O(n)$. For a million trades that is a few million steps, not 20 million." `homework-3` `items[6].explain.text`, second sentence: "Each round keeps one side, so the expected work is about $2n$ to $4n$."

18. `l14-best-step-now.json` | `screens[7].widget.lines[2].text` | **imprecise, minor** | "Every other meeting of $O$ starts after $o$ ends, so after $g$ ends too". This lesson lets touching meetings share the room (`s >= last_end`), so the next meeting of $O$ may start exactly when $o$ ends. The proof needs "at or after". | Evidence: script (`[(9, 10), (10, 11)]` is a valid schedule). Basis: CLRS 16.1 defines compatibility with $s_j \ge f_i$. | Fix: "Every other meeting of $O$ starts when $o$ ends or later, so no earlier than $g$ ends"

19. `l8-cost-of-recursion.json` | `screens[9].explain.text` | **imprecise, minor** | "So every practical pricer recombines; the course Binomial trees builds one." Non-recombining trees are used when the model does not recombine: a stock paying a known cash dividend, and HJM-type rate models. The course meant is named Pricing with Trees in `app/content/courses/trees/course.json`. | Basis: Hull, *Options, Futures and Other Derivatives* (9th ed.), 21.3 (known dollar dividend: the tree does not recombine) and 32.1 (HJM: non-recombining tree). | Fix, last sentence: "So pricers use a recombining tree whenever the model allows it; the course Pricing with Trees builds one."

20. `homework-3.json` | `items[7].model` (part a), `items[7].rubric[1].text` | **imprecise, minor** | "its worst case is $O(n^2)$ unless the pivot is random or chosen by median-of-medians". A random pivot leaves the worst case at $O(n^2)$; it only makes that case very unlikely on any input. Median-of-medians is what removes it. | Basis: CLRS 9.2 (randomised select: expected linear, worst case quadratic) and 9.3 (worst-case linear select). | Fix, model: "It works in place. Its worst case is $O(n^2)$: a random pivot makes that very unlikely, and median-of-medians rules it out." Rubric: "States quickselect's $O(n^2)$ worst case and how a random pivot makes it unlikely"

21. `l3-memory.json` | `quiz[2].explain.text` | **imprecise, minor** | "(Libraries use Welford's update, which is steadier in floating point.)" NumPy, the library this course uses, computes a variance in two passes: the mean, then the mean squared deviation. Welford's update is one method for streams, not what libraries in general do. | Basis: NumPy source `numpy/_core/_methods.py`, `_var`; Knuth, vol 2, 4.2.2 (the one-pass recurrence credited to Welford, 1962). | Fix: "(Welford's update keeps the same three-number budget and is steadier in floating point.)" Checked: Welford keeps the count, the running mean and the running sum of squared deviations.

22. `l10-search-the-answer.json` | `screens[8].widget.options[3].why` | **imprecise, minor** | "You stopped with the price 34p away. The tolerance asks for a penny." This screen states no tolerance; the penny belongs to the bond screen three screens earlier. | Evidence: reading of `screens[8].prose` and `question`. | Fix: "You stopped with the price 34p from £12.00. Keep halving until the price is as close as you need."

## Unverified rows (not counted as findings)

- U1. `l11-sorting-by-hand.json` | `screens[9].explain.text` | "New levels usually land near the touch, so insertion into a nearly sorted list fits an order book well." An unsourced remark about markets. The list is also sorted from low to high, so only the bid side has its touch at the end. Suggested text: "When a new level lands near the end, as here, insertion into a sorted list is cheap."
- U2. `l13-quicksort.json` | `screens[6].explain.text` | "Real data often arrives sorted or nearly sorted". Unsourced. Suggested text: "Data can arrive sorted or nearly sorted, so a fixed first or last pivot is risky."

## Checks the brief asks for, and what they found

- Big O against its stated case. Worst, best and average are named where they matter: binary search worst case (`l9` screen 2), insertion sort worst, best and random (`l11`), merge sort every input (`l12`), quicksort average and worst (`l13`), amortised against worst single append (`l4`). The gaps are findings 4, 6, 17 and 20.
- Operation counts. Every stated count of comparisons, copies, calls, frames and multiplications was reproduced by running the algorithm with a counter (script). The only wrong counts are findings 2, 3 and 9.
- Recursion depths. `fact`, `sum_list`, `fib`, `max_rec`, `power_fast` and the pricer: all depths match (script; Pyodide limit 1000).
- Greedy. Each greedy claim carries its condition: coins "depend on the coin system" and are checked against a dynamic programme; earliest finish first is proved by exchange and checked against brute force on 400 random diaries; fractional against 0/1 knapsack is stated; the market-order fill is "for a single order". The only gap is finding 18.
- Conventions. Annual coupons and annual compounding are stated in the bond items; VaR as the loss at the 5th percentile matches Hull ch. 22; touching intervals do not clash, said where it first matters.

## Gates

- `node tools/validate.mjs`: 0 errors (4,531 warnings); `content/manifest.json` unchanged.
- Number scripts: `docs/reports/algo-think-2-perf-numbers.py` exit 0; `docs/reports/algo-think-3-perf-numbers.py` exit 0. No `algo-think-L*-numbers.py` exists.
- `grade-all.mjs --file` on review-1, review-2, review-3, homework-1, homework-2, homework-3: 0 failures each (33 non-code widgets). It does not run code widgets, so the 41 code widgets were run separately as described above.
- Concepts script: exit 1, 19 failing checks, all tied to findings 1 to 18 (finding 6 has two).

## Overlap with the earlier read

Read after WIP commit `67c114de`: `docs/reviews/review-1.8.md` (it covers algo-think, ds and graphs-dp; only its algo-think findings are counted) and `docs/reviews/voice-1.8-algo-think.txt` (sentence lengths only, nothing conceptual).

The earlier read made 11 algo-think findings. Two are conceptual: `homework-3` `items[1]` option `b` ("each coin is at least double the one below" given as the rule that makes greedy safe; 1, 4, 9 refutes it) and `l3-memory` `screens[4]` (a 32-bit build "reports roughly half"; it is about 20 bytes against 32). Both were fixed in its fix pass, and this audit checked the fixed text and found it right (ledger rows `homework-3 i1` and `l3 s4.ex`). The other nine are not conceptual: tests that let a slower solution pass (three), a sentence that did not parse (one), explanations over three sentences (two), sentence length (one) and chart labels (two).

| Conceptual findings | Count |
|---|---|
| Found by this audit only | 22 (wrong 3, imprecise 18, misleading 1) |
| Found by the earlier review only | 2 (both already fixed) |
| Found by both | 0 |

New `wrong` findings that no earlier read found: **3** (findings 1, 2 and 3), over three levels. That is above the convergence limit of one per three levels, so the course needs another blind round after the fix pass.

Note for the fixer: the earlier fix pass (its item 13) already quotes "about $3.4n$" for quickselect, which agrees with finding 17; the lesson text still says "about $2n$".

## Fix pass

Fixer: Opus, 13 Nov 2026. Every fix was re-derived by my own run (`tracemalloc`, counters, brute force) or source before it was written. Content strings only; no key id, tolerance, slip value or code widget (solution, starter, tests) changed, so no code widget needed re-running. One wrong option text changed (finding 4, option `d`).

1. **fixed** (code changed, claim kept). Program A now loops over `prices` itself: `tracemalloc` peak 48 bytes at n = 10^4 and 10^5, against 80,040 and 800,040 for the slice; max still 108 on the screen's prices. Caption, options, hints and explain hold as written; no other screen, review or homework item reuses the program (`l1` uses the slice with no memory claim).
2. **fixed**. `pre = [0, 3, 4, 8, 9, 14]`, so `pre[4] - pre[1] = 9 - 3 = 6`.
3. **fixed**. My counter: 1,048,575 copies for 10^6 appends with doubling from capacity 1.
4. **fixed differently**. Counted with the lesson's Lomuto and random pivot: 3,000 equal values cost 4,498,500 = n(n-1)/2 on every seed; 3,000 sorted distinct values cost 38,914. Question now says "With a random pivot and distinct values, which input order is the worst case?"; key `a` (id unchanged) reads "every order has expected cost $O(n \log n)$"; screen 4 explain as the auditor proposed. Differently: wrong option `d` "Input with no duplicates" no longer fits a question about order of distinct values, so it is now "An order chosen to beat the pivot", why "The input is fixed before the pivots are drawn, so no order can aim at them." The screen's explain on equal values now agrees with the question.
5. **fixed**. Last-value pivot gives c, b, a; 200 seeds of the random pivot give both c, b, a and c, a, b.
6. **fixed**. $2n\log n + 40n + 9 \le 60 n^2 \log n$ for $n \ge 2$ and $5n \le 5n^2$ (CLRS 3.1); convention sentence added to the prose, the two whys and the summary as proposed.
7. **fixed differently**. Tripling copies 4 against 3 at n = 4 and 40 against 31 at n = 28, under $1.5n$ and $2n$ for every n to 3,000. Why now opens "Not in general:" so it rebuts the option rather than implying tripling always copies less.
8. **fixed**. `sys.getsizeof` capacity ratio 1.125 (CPython `list_resize`, `newsize + (newsize >> 3) + 6`).
9. **fixed**. Call k copies k - 1: sum 45 = 10·9/2 at n = 10, against 55 for $1 + \dots + n$.
10. **fixed differently**. Levels of `fib(5)` are 1, 2, 4, 6, 2; for n = 2 to 17 the tree has n levels and levels 0 to ⌊n/2⌋ are full. Worded "`fib`'s calls shrink by 1 or 2: $n$ levels deep, doubling on each level of the top half." to stay under 20 words.
11. **fixed**. $1 + 2 + 4 + 8 = 15 = 2 \cdot 8 - 1$; both feedback lines now show the doubling sum.
12. **fixed differently**. Recursion r, a, a1, a2, b; loop r, b, a, a2, a1. Same content as proposed, split into two sentences.
13. **fixed differently**. A nested function reads its enclosing `n` (run; language reference 4.2.2). Now "A function sees its own names and those of the code around it, here the module. It never sees its caller's."
14. **fixed**. My run on `[10, 20, 30, 40]`: targets 5, 25, 35, 40 spin, 45 raises `IndexError`; the invariant makes `lo == hi < len(xs)` imply `xs[hi] >= target`, so these are the only two cases.
15. **fixed**. 2,500 passes, so a scan from 1,000 runs at least 1,502 tests, more than 1,500.
16. **fixed**. 64 reversed values: 2,016 inversions with 192 merge comparisons; when a right item is taken, every left item still waiting is bigger.
17. **fixed**. Simulated random-pivot quickselect at n = 20,001: 3.34n for the median, 1.88n for the minimum; theory $2(1 + \ln 2) = 3.386$. Feedback, explain and `homework-3` as proposed.
18. **fixed**. `[(9, 10), (10, 11)]` is a valid schedule under `s >= last_end`; line now "starts when $o$ ends or later".
19. **fixed**. Hull 21.3 (known cash dividend: the tree does not recombine) and HJM non-recombining trees; `trees/course.json` name is "Pricing with Trees".
20. **fixed**. CLRS 9.2 and 9.3: randomised select is quadratic in the worst case; median-of-medians is worst-case linear.
21. **fixed**. NumPy `_var` takes the mean, then the mean squared deviation; Welford keeps count, mean and $M_2$, three numbers.
22. **fixed**. £12.34 - £12.00 = 34p; the screen states no tolerance.
- U1. **fixed** (stated as a condition). "When new levels land near the end, as here, insertion into a sorted list fits an order book well." 4 comparisons and 3 shifts rechecked for a level three places from the end.
- U2. **fixed** (hedged). "Data can arrive sorted or nearly sorted, so a fixed first or last pivot is risky."

Scripts: `docs/reports/algo-think-L1-3-concepts.py` now has 124 checks and exits 0. Each of the 19 FINDING checks was rewritten to read the corrected string from the content (helper `T()`) and recompute the corrected claim; the finding 1 check executes program A as it now stands in the prose and measures it, and one new check keeps the old slice's O(n) peak as evidence. Checks for findings 10 and 13 match my wording, not the auditor's. `algo-think-2-perf-numbers.py` and `algo-think-3-perf-numbers.py` exit 0.

Gates: validator 0 errors, 4,531 warnings (as before), manifest unchanged; voice scan 35: 0 and 0; playthrough desktop and `--mobile` green for l2, l3, l4, l6, l8, l9, l10, l11, l13, l14, homework-1, homework-2, homework-3, review-2.

## Fix-pass read

Fresh read of the fixer's diff `ae8bb185~1..ae8bb185` (14 files, 37 changed lines), without sight of the audit, ledger or fix-pass notes. Every changed string was read in its item, and every count was recomputed in a throwaway Python script (Lomuto partition as in l13, comparison counter in the loop, random pivot swapped to `hi`; 200 runs per quickselect cell at n = 20,000, 60 runs per quicksort cell at n = 4,000).

Rows read: 37. Verdicts: 37 correct, 0 wrong, 0 imprecise, 0 misleading, 0 unverified.

| # | File | JSON path | New text (short) | Verdict | Basis |
|---|------|-----------|------------------|---------|-------|
| 1 | homework-1 | h-fixed-code explain | step 10: about 5e10 copies, against about 1e6 with doubling | correct | Run: `copies_fixed(1_000_000, 10)` = 49,999,500,000; doubling from capacity 1 = 2^20 - 1 = 1,048,575 (1,310,710 from capacity 10). |
| 2 | homework-2 | sort-count explain | left half sorted, so one comparison shows every left item still waiting is bigger | correct | If a[i] > b[j] and a is sorted, a[i..] > b[j]. Run with that assertion in the merge: 3, 2 and 99,930,366 match the tests. |
| 3 | homework-3 | kth_largest explain | expected work about 2n to 4n | correct | Knuth, TAOCP 3, 5.2.2 ex. 32: about 2n(1 + H(a)) nats; 2n for the minimum, (2 + 2 ln 2)n = 3.39n for the median. Run: 1.99n to 3.33n. |
| 4 | homework-3 | kth_largest explain | random pivot keeps sorted input from being the worst case | correct | Run: sorted and shuffled input give the same counts (median 3.327n against 3.332n). |
| 5 | homework-3 | h-var-report model (a) | quickselect about 2n to 4n, so 2 to 4e7 comparisons | correct | As row 3 with n = 1e7. |
| 6 | homework-3 | h-var-report model (a) | It works in place. Its worst case is O(n^2): random pivot makes that very unlikely, median-of-medians rules it out | correct | Hoare FIND worst case n(n-1)/2; Blum, Floyd, Pratt, Rivest, Tarjan (1973) give worst-case O(n). Simulated P&L values are distinct, so the equal-values caveat of l13 does not bite. |
| 7 | homework-3 | h-var-report model (a) | three quickselects cost about 6 to 12e7 | correct | 2.11n + 2.40n + 3.39n = 7.9n = 7.9e7, inside the range; run gives 2.11n, 2.32 to 2.41n, 3.33n. |
| 8 | homework-3 | h-var-report rubric[1] | states the O(n^2) worst case and how a random pivot makes it unlikely | correct | Agrees with model (a) as changed. |
| 9 | homework-3 | h-var-report rubric[0] (context) | quickselect about 2n to 4n | correct | Agrees with rows 3 and 5. |
| 10 | l10 | bisect-vol option d why | stopped with the price 34p from £12.00; keep halving until close enough | correct | Black-Scholes, S = K = 100, r = 0.05, T = 1, sigma = 0.25: 12.336, so 34p. Agrees with option b's £12.34. |
| 11 | l10 | orders-a-minute explain | 11 tests pin the limit to within one order a minute | correct | Width 1,500: 1500/2^10 = 1.46, 1500/2^11 = 0.73. |
| 12 | l10 | orders-a-minute explain | testing every rate from 1,000 up would take more than 1,500 | correct | Limit is at least 2,500, so rates 1,001 to 2,501 at least: 1,501 tests. |
| 13 | l11 | order-book explain | when new levels land near the end, as here, insertion fits an order book well | correct | 3 passes plus the stopping test = 4 comparisons, 3 shifts, matching the step hint; the claim is now conditional on the stated case. |
| 14 | l13 | quicksort code explain | with distinct values the expected cost is O(n log n) whatever their order | correct | CLRS 7.4.2. Run: 1.14 to 1.15 n log2 n on sorted, reverse, shuffled and organ-pipe input. All-equal input gives n(n-1)/2 = 7,998,000 at n = 4,000, so the "distinct" condition is needed and is stated. |
| 15 | l13 | sorted-input explain | data can arrive sorted or nearly sorted, so a fixed first or last pivot is risky | correct | Run: fixed last pivot on sorted n = 2,000 gives 1,999,000, the figure in the step hint. |
| 16 | l13 | random-pivot question | with a random pivot and distinct values, which input order is the worst case? | correct | Conditions now match the key; the explain line on equal values no longer contradicts it. |
| 17 | l13 | random-pivot option a (key) | none in particular: every order has expected cost O(n log n) | correct | As row 14. |
| 18 | l13 | random-pivot option d | an order chosen to beat the pivot; why: input is fixed before the pivots are drawn | correct | Oblivious-adversary argument, CLRS 7.3. Does not overlap options b and c, whose `why` lines still hold. |
| 19 | l13 | quickselect feedback.correct | about 2n to 4n comparisons on average: O(n) | correct | As row 3. |
| 20 | l13 | quickselect explain | if every step halved the range the work would be about 2n; random pivots make it about 3.4n for a median | correct | Geometric sum 2n; (2 + 2 ln 2)n = 3.386n; run 3.33n at n = 20,000. |
| 21 | l13 | quickselect explain | for a million trades, a few million steps, not 20 million | correct | 3.4e6 against 1e6 x log2(1e6) = 1.99e7. |
| 22 | l13 | q-stable prose | Lomuto, taking the last value as pivot each time, comparing prices only | correct | Run with the lesson's partition (`<=`) and no random swap: `[(1,'c'), (5,'b'), (5,'a')]`, the key. The added clause is needed: a random pivot would make the output random. |
| 23 | l14 | exchange-proof s3 | every other meeting of O starts when o ends or later, so no earlier than g ends | correct | Touching meetings do not clash in this lesson (`s >= last_end`); g ends no later than o (s2), so start >= end(o) >= end(g). |
| 24 | l2 | big-O definition prose | Big O is an upper bound, so n is also O(n^2); by convention we quote the smallest class | correct | Definition with c = 1, n0 = 1. CLRS 3.1. |
| 25 | l2 | definition option `product` why | O(n^2 log n): true as an upper bound, but not the smallest class | correct | 2n log n + 40n + 9 <= 51 n^2 log n for n >= 2. Agrees with the new prose and with option `const`. |
| 26 | l2 | summary ideas[2] | doubling n adds a constant to log n, doubles n and quadruples n^2 | correct | log(2n) = log n + log 2; (2n)^2 = 4n^2. |
| 27 | l2 | q-fixed-inner option n2 why | true as a loose upper bound, not the smallest class; inner loop always runs 5 times, total 5n | correct | 5n <= 5n^2 for n >= 1. |
| 28 | l3 | screen 1 prose, program A | `for p in prices:` after `best = prices[0]` | correct | Run on the canvas prices: A gives 108, B gives 108. The loop now visits every cell, as the stepping canvas does. |
| 29 | l3 | prefix-sums hint `point` | days 1 to 3 total 9 - 3: `pre[4] - pre[1]` | correct | Run: pre = [0, 3, 4, 8, 9, 14]; 9 - 3 = 6 = 1 + 4 + 1, the example's value. |
| 30 | l3 | q-variance explain | Welford's update keeps the same three-number budget and is steadier in floating point | correct | Welford (1962); Knuth, TAOCP 2, 4.2.2: state is count, mean, M2. Run on 1e9 + U(0,1): naive 5120.0, Welford 0.083314, true 0.083314. |
| 31 | l4 | first screen explain | Python's `list.append` works this way, with a much smaller growth factor of about 1.125 | correct | CPython `list_resize`: new size + (new size >> 3) + 6. Run with `sys.getsizeof`: successive capacity ratios 1.125. |
| 32 | l4 | tripling option `worse` why | not in general: tripling's total stays under 1.5n, against 2n for doubling; price is more spare slots | correct | (3^m - 1)/2 with 3^(m-1) < n. Run to n = 5,000: max ratios 1.4991 and 1.9993. "Not in general" is right: tripling copies more at n = 4 and n = 28 to 32, and at n = 1,000 (1,093 against 1,023). |
| 33 | l4 | q-np-append options and feedback | the calls copy 0, 1, 2, ... elements; 0 + 1 + ... + (n - 1) copies: quadratic | correct | Call k copies k - 1 elements; sum n(n-1)/2, as the explain line says. Three changed strings, one claim. |
| 34 | l6 | explicit-stack explain | the loop goes depth first like the recursion; it takes each node's children last to first | correct | Run on a six-node tree: loop A C F B E D, recursion A B D E C F. |
| 35 | l6 | q-scope option `three` why | a function sees its own names and those of the code around it, here the module; never its caller's | correct | Python reference 4.2.2 (lexical scoping). Run: `NameError: name 'n' is not defined`; with a module-level `n = 9` it prints 9. |
| 36 | l8 | merge-tree explain; four-recurrences feedback; lattice explain; review-2 q feedback | fib: n levels deep, doubling on each level of the top half; 1 + 2 + 4 + ... + n = 2n - 1; pricers use a recombining tree whenever the model allows it; course Pricing with Trees | correct | Run: fib(16) call tree has 16 levels, full (2^d calls) to level 8. T(n) = 2T(n/2) + 1, T(1) = 1 gives 15 and 127 at n = 8 and 64. Lattice 101 x 102 / 2 = 5,151; 2^101 - 1 = 2.535e30. Non-recombining cases (path-dependent payoffs, discrete cash dividends) exist, Hull ch. 21, so the hedge is right. Course name matches `curriculum.json`. |
| 37 | l9 | q-condition option `le` why | with `<=`: if `xs[mid] >= target`, `hi = mid` changes nothing and it never ends; if `lo` has reached `len(xs)`, IndexError | correct | Run of the lesson's loop (`lo, hi = 0, len(xs)`) with `<=` on 45 list and target pairs: 19 never end, 26 raise `IndexError`, none returns. |

### Findings

None. No changed string is wrong, imprecise or misleading.

Notes, no action needed:

- homework-3 model (a): the "very unlikely" worst case assumes distinct values. Simulated P&L values are, and l13 states the equal-values caveat, so the line stands.
- l13 quickselect: measured means sit slightly under the asymptotic 3.39n at n = 20,000 (3.33n), as the lower-order terms predict.
