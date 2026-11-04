
## Level 2

You are a content agent on the Zero to Quant build in /home/user/zero-to-quant. Author course `coding-int` (topic 3.5), level 2 ("Strings and simulation"): lessons `l6-anagrams-and-palindromes`, `l7-parsing-with-a-stack`, `l8-simulating-the-rules`, `l9-grids-and-matrices`, `l10-matching-engine`, plus `review-2.json` and `homework-2.json`, in `app/content/courses/coding-int/`. Follow `docs/LEVEL-BRIEF.md` exactly and read `docs/AUTHORING.md` in full; use the lesson names, objectives and skill ids of `course.json` exactly. Use £ for money (prices in l8 and l10 are whole pence; say so on the first screen). Scripts: `l2.py` (every problem of this level, brute forces, C++ cross-check of the matching engine on 300 random streams), `l2_data.py` (price files), `harness.py`, `numbers_check.py`, `numbers_check2.py`.

Level promise. The learner turns text into code that is right at the edges: string questions with counts and centres, nested expressions, a long rule statement as an online assessment sets it, a matrix without off-by-one errors, and a small matching engine. It is the first level where the clock is part of the lesson, so every code screen carries a `pace`.

**Engine features.** E14 (data files) in l8 screen 8; E3, E8 and E11 are not needed. Existing: `code` (Python and C++; Python `data` is E14), `grid` canvas for matrices (grid ids are one-based, cell text plain), `orderbook` canvas for the engine, `console` for an assessment statement and its output, `array` (stack mode) for the parser, `manipulate`, `order`, `tap-regions`, `table`.

**Builds on (by id) and what is new.**

| Lesson | Builds on | New over those |
| --- | --- | --- |
| l6-anagrams-and-palindromes | `ds` l4-frequencies (anagram counts and key), `ds` l5-both-ends (palindrome by two pointers), `ds` l6-sliding-window | Counting inside a moving window of fixed width, expanding from `2n - 1` centres, and when a string can be rearranged into a palindrome. |
| l7-parsing-with-a-stack | `ds` l9-last-in-first-out (brackets, postfix), `algo-think` l5-calls-itself | Infix with precedence on two stacks, unary minus, division that truncates toward zero, nested decoding with a stack of (text, count). |
| l8-simulating-the-rules | `contests` l1-reading-statements, `contests` l15-debugging-under-time, `py-found` l10-reading-a-csv | Turning an eight-rule statement into state, events and an order of checks; reading a price file (E14). |
| l9-grids-and-matrices | `graphs-dp` l4-islands, `ds` l1-arrays-in-memory | Boundary shrinking for spiral order, index maps for in-place rotation, flood fill from the border; Game of Life in homework. |
| l10-matching-engine | `ds` l18-order-book-heaps, `micro` l1-bids-and-asks, `micro` l3-the-queue, `cpp` l15-maps | An event processor over price levels with FIFO queues; market orders; cancel and amend by id; the same engine in C++ with `std::map` and `std::deque`. |

### l6-anagrams-and-palindromes (13 min; tags `anagram-window`, `palindrome-centres`, `palindrome-permutation`)

Objective: Solve string questions with counts, two pointers and expanding centres. Method stated after use: to find anagrams of `p` in `s`, keep a count of the letters in the current window of length `len(p)`, add the new letter, drop the old one, and compare the counts; to find palindromes, grow outwards from each of the `2n - 1` centres (each letter, and each gap between two letters) while the two ends match.

Screens (10):
1. Hook `problem`, `array` of `cbaebabacd` with a highlight range of width 3; `tap-regions`: tap the starts of windows that are anagrams of `abc`; answer index 0 and index 6.
2. `explore`: slide the window with a control; `numeric`: how many windows of width 3 does `cbaebabacd` have (8).
3. `ladder`, `numeric`: sorting every window of width 1,000 in a string of 100,000 does 99,001 sorts of 1,000 letters; the count version updates 100,000 times (answer: the number of windows, 99,001, computed as `n - w + 1` and by counting starts).
4. `problem`, code A, `find_anagrams`, `pace` 600.
5. `ladder`, `array` showing centres of `abba` (7 centres: four letters and three gaps); `numeric`: the number of centres of a string of 7 letters is 13 (`2n - 1`).
6. `problem`, code B, `longest_palindrome`, `pace` 600.
7. `trap`, `choice`: a learner who only expands from letters misses even palindromes: `cbbd` has the answer `bb`; right answer 2 (the gap centre).
8. `generalise` + `derive` (`order`: for each centre set `lo` and `hi`, widen while equal and in range, record if longer).
9. `transfer`, `multi`: which of `carerac`, `abcabc`, `aabbccd`, `abcd`, `aabbcd` can be rearranged into a palindrome (at most one letter with an odd count): `carerac`, `abcabc`, `aabbccd`.
10. `transfer`, `numeric`: how many palindromic substrings has `abba` (6: `a`, `b`, `b`, `a`, `bb`, `abba`) and how many has `aaa` (6), counted by centres and by listing every substring.

Quiz (4): window counts; centres for `n = 7`; palindromic permutation; the worst case of centre expansion on `aaaa...` (quadratic).

**Problem 6.1** `find_anagrams(s, p)`; Python; difficulty 3. Statement: "Return the start index of every window of `s` that is an anagram of `p`, in increasing order." Reference, starter (finds exact copies of `p`, not anagrams; fails 4 of 8), tests (the last has 100,000 letters and `p` of 1,000):

@@PY:l2:FA_REF@@

@@PY:l2:FA_START@@

@@T:l2:fa@@

**Problem 6.2** `longest_palindrome(s)`; Python; difficulty 3. Statement: "Return the longest palindromic substring of `s`; when two have the same length, the one that starts first; the empty string for an empty input." Reference, starter (returns the first letter; fails 7 of 10), tests (the last has `'a' * 3000`, so 3,000 centres expanding fully: about 9 million steps, inside the limit):

@@PY:l2:LP_REF@@

@@PY:l2:LP_START@@

@@T:l2:lp@@

### l7-parsing-with-a-stack (14 min; tags `expression-parse`, `decode-nested`, `integer-division`)

Objective: Evaluate and decode nested expressions with a stack. Method stated after use: keep a stack of numbers and a stack of operators; before pushing an operator, apply every operator on top that binds at least as tightly; a closing bracket applies operators back to its opening bracket; a minus where an operand is expected is unary.

Screens (11):
1. Hook `problem`, `array` (stack mode, two stacks) for `3+2*2`; `numeric`: the value (7); the learner who evaluates left to right gets 10.
2. `explore`, `manipulate` over `3+2*2`: push, push, push, apply `*`, apply `+`; the postfix form is `3 2 2 * +` (cite `ds` l9 for postfix).
3. `ladder`, `choice`: `10-2-3` must be 5, not 11: equal precedence applies the earlier operator first (`>=`).
4. `ladder`, `numeric`: `2*(5+5*2)/3+(6/2+8)` is 21 (hand: `2*15/3 = 10`, `6/2 + 8 = 11`); the peak size of the operator stack is 4.
5. `trap`, `numeric`: `-7/2` under the statement's rule, which truncates toward zero: -3. Python's `//` gives -4. Name the action in `byKey` ("You used floor division").
6. `problem`, code A, `calculate`, `pace` 840, difficulty 4.
7. `ladder`, `numeric`: decode `3[a2[c]]` has length 9 and `2[abc]3[cd]ef` has length 14; `choice` for what to push on `[` (the pair: text so far and the count).
8. `problem`, code B, `decode_string`, `pace` 600.
9. `generalise` + `derive` (`order` the decode steps with the distractor "push the digits as characters").
10. `transfer`, `choice`: a risk formula in a config file with brackets and `-` signs: which of the two parsers (stack, or `eval`) a firm would allow, and why (`eval` runs arbitrary code).
11. `transfer`, `numeric`: `9[9[9[a]]]` decodes to 729 letters (`9^3`), so decode in place would be `O(output)`; the stack is `O(depth)`.

Quiz (4): precedence with equal ranks; truncation; a decode length; the stack depth on nested brackets.

**Problem 7.1** `calculate(s)`; Python; difficulty 4. Statement: "`s` holds non-negative whole numbers, `+ - * /`, spaces and brackets; a `-` may also be unary (`-(2+3)*4`, `2*-3`). `/` truncates toward zero. Every input is valid and never divides by zero. Return the value as an `int`." Reference (two stacks and a unary operator), starter (calls `eval` with `//`; fails 2 of 15: negative division and unary minus), tests:

@@PY:l2:CALC_REF@@

@@PY:l2:CALC_START@@

@@T:l2:calc@@

Checks: 3,913 random expressions compared with a parser built on `ast` with truncating division; the postfix forms and values of `3+2*2` (`3 2 2 * +`, 7), `10-2-3` (`10 2 - 3 -`, 5) and `(1+2)*3` (`1 2 + 3 *`, 9) match the stack evaluator.

**Problem 7.2** `decode_string(s)`; Python; difficulty 3. Statement: "`k[text]` repeats `text` `k` times; `k` may have several digits; brackets nest; letters outside brackets stay as they are. Every input is valid." Reference, starter (returns `s`; fails 8 of 10), tests:

@@PY:l2:DS_REF@@

@@PY:l2:DS_START@@

@@T:l2:ds@@

### l8-simulating-the-rules (14 min; tags `simulation-rules`, `file-read`, `edge-order`)

Objective: Turn a long rule statement into a correct simulation, as online assessments often ask. Method stated after use: list the state (what must be remembered between steps), the events (what arrives each step) and the order of the checks; write one function that applies one event; test it on a hand-built trace. Skills `ci-strings` and `ci-timed`.

The running story (a rule-based bot as an assessment states it, prices in whole pence):

> A bot trades one unit of one stock. It starts flat. Day 0 never trades. While flat on day `i >= 1` it buys at that day's price when the price is below the previous day's price. While long, on each later day it sells at that day's price if, in this order: (1) the price is at least 5% above the entry price (`100 * p >= 105 * entry`); (2) the price is at most 3% below the entry (`100 * p <= 97 * entry`); (3) it has held for exactly 3 days (`i - bought == 3`). A bot that sells on day `i` does not buy on day `i`. If it still holds at the end it sells at the last price. Return `[total profit in pence, number of trades]`.

Screens (11):
1. Hook `problem`, `console` showing the statement and a six-day price list `[100, 98, 99, 100, 104, 110]`; `numeric`: total profit (6). The learner traces by hand: buys 98 on day 1, sells 104 on day 4 (`10400 >= 10290`).
2. `explore`, `table` widget with columns day, price, state, action filled for the six days (the learner completes it).
3. `ladder`, `choice`: which rule fires first on a day when the price is both 5% up and the third day: rule 1 (the order of checks decides).
4. `ladder`, `numeric`: the time rule counts days since the buy. A bot that buys on day 2 sells on which day if no other rule fires? Day 5 (`2 + 3`). (The homework item uses a list where `== 3` and `> 3` differ.)
5. `problem`, code A, `run_strategy`, `pace` 840.
6. `trap`, `choice`: prices `[100, 95, 90, 85]`. The stop rule sells at 90 on day 2 (`9000 <= 9215`). A bot that also buys on the day it sells gets `[-10, 3]`; the right answer is `[-5, 2]` (it buys at 85 on day 3 and sells at the end for 0). Name the action in `byKey` ("You let the bot buy on the day it sold"). Both traces were run and the correct one was checked by hand.
7. `generalise`: state, events, order, in fenced code; `derive`: `order` the six steps of reading a long statement.
8. `problem`, code B (E14), `strategy_from_file` reading `ticks-40.csv`, `ticks-3.csv` and `ticks-header-only.csv`; `data` on the widget. The starter includes the working `run_strategy` and a `load_prices` stub.
9. `transfer`, `choice`: which of three statements of the same rule is ambiguous ("sells after three days" against "sells on the third day after the buy"): the learner picks the ambiguity and the question to ask.
10. `transfer`, `numeric`: a different price list the agent chooses and computes twice (suggested: `[100, 95, 100, 106, 90, 89, 95, 99]` gives `[10, 2]`: the review item uses it, so choose another for the lesson).
11. `transfer`, `choice` on testing: write two hand traces before the code (the lesson of `contests` l15).

Quiz (4): an order-of-checks question; the same-day buy rule; a file edge case (header only); a traced profit.

**Problem 8.1** `run_strategy(prices)`; Python; difficulty 4. Statement: the story above; `prices` is a list of whole numbers, possibly empty; return `[profit, trades]` as a list of two ints. Reference, starter (profit is the last price minus the first, one trade; fails 8 of 8), tests (expected values from a second implementation that scans forward from each buy, matched on 5,000 random lists):

@@PY:l2:RS_REF@@

@@PY:l2:RS_START@@

@@T:l2:rs@@

**Problem 8.2** `strategy_from_file(path)`; Python; difficulty 3; E14: `"data": { "ticks-40.csv": "content/data/coding-int/ticks-40.csv", "ticks-3.csv": "content/data/coding-int/ticks-3.csv", "ticks-header-only.csv": "content/data/coding-int/ticks-header-only.csv" }`. The level agent creates these three files with exactly the text below (the first line is the header `day,price_pence`; rows end with a newline; `ticks-header-only.csv` is the header and nothing else; `ticks-3.csv` is `0,10000`, `1,9900`, `2,10600`). Statement: "`path` is a CSV with columns `day` and `price_pence` in day order. Read the prices and return what `run_strategy` returns for them." The starter shows `run_strategy` complete (the reference above) and a stub `load_prices(path)`, so the learner writes only the reader. Reference reader:

```python
import csv

def load_prices(path):
    with open(path) as f:
        return [int(row['price_pence']) for row in csv.DictReader(f)]

def strategy_from_file(path):
    return run_strategy(load_prices(path))
```

Tests (starter, whose `load_prices` returns an empty list, fails 2 of 3; checked with the files in a working directory): `strategy_from_file('ticks-40.csv')` returns `[249, 8]`, `strategy_from_file('ticks-3.csv')` returns `[700, 1]` (buy 9,900 on day 1, sell 10,600 on day 2 because `1060000 >= 1039500`), and `strategy_from_file('ticks-header-only.csv')` returns `[0, 0]`. The 40-row file was generated by `l2_data.py` (seed 77) and is given in full for the level agent:

@@FILE:data/ticks-40.csv@@

Each file's rows were parsed two ways (`csv.DictReader` and a `split(',')`), and the three expected values come from the reference and a second implementation that agree.

### l9-grids-and-matrices (14 min; tags `matrix-spiral`, `matrix-rotate`, `flood-border`)

Objective: Traverse, rotate and flood-fill a matrix without off-by-one errors. Method stated after use: keep four bounds (`top`, `bottom`, `left`, `right`) and shrink them after each side of a spiral; rotate a square by transposing and then reversing each row; flood fill from the cells you know are safe, here the border, instead of from the cells you doubt.

Screens (12):
1. Hook `problem`, `grid` 3 by 4 with the numbers 1 to 12; `tap-regions`: "Walk clockwise round the edge. Tap every cell on the first lap." Answer every cell except `r2c2` and `r2c3` (the numbers 6 and 7 are left for the second lap).
2. `explore`, `grid` with a stepper over the spiral; `numeric`: the last number visited in a 3 by 4 matrix is 7 (computed by the bounds method and by a visited-set walk).
3. `ladder`, `choice`: a 1 by 3 and a 3 by 1 matrix: which `if` stops the bottom row being read twice (`top < bottom`) and the left column (`left < right`).
4. `problem`, code A, `spiral_order`, `pace` 600.
5. `ladder`, `numeric` (rotation): in a 5 by 5 matrix rotated 90° clockwise, the value at row 0, column 1 moves to row 1, column 4 (zero-based): `(r, c)` goes to `(c, n - 1 - r)`. Provide `(1, 3)` to `(3, 3)` and `(4, 0)` to `(0, 0)` as the next two checks.
6. `problem`, code B, `rotate` (in place, returns nothing), `pace` 600.
7. `trap`, `choice`: building a new matrix and assigning it to the parameter name leaves the caller's matrix unchanged; the test checks the caller's list. Name the action in `byKey`.
8. `ladder`, `grid` with a border of `X` and `O` regions; `tap-regions`: tap the `O` cells that cannot be captured (those connected to the border).
9. `problem`, code C, `capture_regions`, `pace` 720.
10. `generalise` + `derive` (`order` the four-bounds loop).
11. `transfer`, `choice`: a heat map of a book's depth as a grid: which traversal prints a clockwise ring.
12. `transfer`, `numeric`: the last value of the spiral of a 300 by 300 matrix filled row by row from 0: 45,149.

Quiz (4): a bound update; the transpose and reverse; a border region count; the memory of copying versus in place.

**Problem 9.1** `spiral_order(m)`; Python; difficulty 3. Statement: "Return the entries of a rectangular matrix (list of rows) in clockwise spiral order from the top left; `[]` for no rows." Reference, starter (row-major order; fails 4 of 8), tests (the last is 300 by 300, checking the last entry, 45,149, from a visited-set walk):

@@PY:l2:SO_REF@@

@@PY:l2:SO_START@@

@@T:l2:so@@

**Problem 9.2** `rotate(m)`; Python; difficulty 3. Statement: "Rotate an `n` by `n` matrix 90° clockwise in place. Return nothing." Tests set up `m`, call `rotate(m)` and then read `m`, so a new list assigned to the name inside the function fails. Reference, starter (does nothing; fails 4 of 6), tests:

@@PY:l2:ROT_REF@@

@@PY:l2:ROT_START@@

@@T:l2:rot@@

**Problem 9.3** `capture_regions(board)`; Python; difficulty 4. Statement: "`board` is a list of equal-length strings of `X` and `O`. Every group of `O` cells (joined up, down, left and right) that does not touch the border becomes `X`. Return a new list of strings." Reference (seed from the border, stack), starter (returns the board unchanged; fails 5 of 8), tests (the last is 400 by 400 with an open interior joined to nothing at the border: no `O` survives; the reference is checked by a fixed-point brute force on 2,000 random boards):

@@PY:l2:CR_REF@@

@@PY:l2:CR_START@@

@@T:l2:cr@@

### l10-matching-engine (15 min; tags `book-events`, `price-levels`, `amend-priority`)

Objective: Simulate price-time priority matching of limit and market orders. Skills `ci-strings` and `ci-design`. Method stated after use: one queue per price level, a map from price to queue for each side, and a map from order id to where it rests; a limit order trades against the best opposite levels it crosses, oldest first, at the resting price, and the rest rests; a market order trades until filled or the other side is empty, and its remainder is dropped.

The event format (use these codes in the statement, in Python and in C++; every field is a whole number, ids are unique, `side` is 0 for buy and 1 for sell, prices are whole pence): `[0, id, side, price, qty]` limit order; `[1, id, side, qty]` market order; `[2, id]` cancel (ignored if the id does not rest); `[3, id, new_qty]` amend (ignored if the id does not rest): a smaller quantity keeps the place in the queue, an equal quantity changes nothing, a larger quantity loses the place and joins the back of the same level. A trade is `[taker_id, maker_id, price, qty]`. `run_book(events)` returns the trades in order; `levels(events, side)` returns the resting levels of one side after all events as `[price, total_qty]`, best first.

Screens (12):
1. Hook `problem`, `orderbook` with asks 3 at 100 (id 1) and 4 at 100 (id 2) (level labels `#1`, `#2`); `numeric`: a buy limit of 5 at 100 leaves how many at the ask level: 2.
2. `explore`, `orderbook` with a market order control; the learner watches fills at each level.
3. `ladder`, `table` widget: trades produced by the stream `[[0,1,1,101,4],[0,2,1,102,6],[0,3,0,102,7]]`: `[3,1,101,4]` and `[3,2,102,3]`; the buy of 7 is filled in full, and 3 remain on the ask side at 102.
4. `ladder`, `choice`: the maker's price is the trade price (the buyer pays 101, not 102).
5. `ladder`, `numeric`: one bid of 10 at 99, then a market sell of 4, then a market sell of 20 (`[[0,1,0,99,10],[1,2,1,4],[1,3,1,20]]`): the trades are 4 and 6, the other 14 is dropped, and the bid side ends empty. Ask for the total traded: 10.
6. `trap`, `choice`: amend a quantity up from 5 to 8 at the front of a level: the order loses its place. With two sells of 5 at 101 and a buy of 6, the amended order trades 1 and the other 5. Name the action in `byKey`.
7. `problem`, code A, Python `run_book` and `levels`, `pace` 900, difficulty 4.
8. `ladder`, code A in C++ (same twelve tests): `std::map<int, std::deque<Resting>>` and `std::unordered_map` for ids.
9. `generalise` + `derive` (`order` the matching loop).
10. `transfer`, `choice`: heaps with lazy deletion (`ds` l18) against price-level queues: which makes cancel by id cheaper and amend simpler (the queue), and which needs `O(log n)` per best-price query (a plain dict needs a scan; the map gives it).
11. `transfer`, `numeric`: after `[[0,1,0,100,2],[0,2,0,99,3],[0,3,1,99,4],[0,4,1,100,1]]` the best bid is 99 and the best ask is 100, so the spread is 1 penny; the total traded is 4.
12. `transfer`, `choice`: the hidden requirements an interviewer adds next (self-trade prevention, immediate-or-cancel, order modification time stamps): which changes one function (a rule in the matching loop) and which changes the data structure.

Quiz (4): trade price; leftover of a market order; a cancelled order that does not rest; the amend rules.

**Problem 10.1** `run_book(events)` and `levels(events, side)`; Python and C++ twin; difficulty 4. Python reference (price-level queues), starter (both functions return an empty list; fails 10 of 12), and the twelve tests, which are the same in C++ (`call: "run_book"`, `args: [<events>]`, `types: ["std::vector<std::vector<int>>"]`; rows of different lengths; for `levels`, `args: [<events>, side]` and `types: ["std::vector<std::vector<int>>", "int"]`):

@@PY:l2:BOOK_REF@@

@@PY:l2:BOOK_START@@

@@T:l2:book@@

C++ reference and starter (the same signatures, `std::vector<std::vector<int>> run_book(std::vector<std::vector<int>> events)` and `std::vector<std::vector<int>> levels(std::vector<std::vector<int>> events, int side)`; the starter returns `{}` and fails 10 of 12). The reference was compiled under `-std=c++17` and `-std=c++20`, matched the twelve tests, and matched the brute force on 300 random event streams:

@@CPP:l2:BOOK_CPP_REF@@

@@CPP:l2:BOOK_CPP_START@@

Checks: the Python reference and a brute force that rescans a flat list for the best price and earliest sequence agree on 4,000 random streams (limit, market, cancel and amend mixed).

### Level 2 review (`review-2.json`, 10 items, difficulty 2 to 4, interleaving all five lessons, every case unseen in the lessons, each with `tags` and `skills`)

| # | Lesson | Widget | d | Prompt (summary) | Key |
| --- | --- | --- | --- | --- | --- |
| 1 | l6 | `numeric` | 2 | How many windows of `abab` are anagrams of `ab`? | 3 (starts 0, 1 and 2) |
| 2 | l6 | `numeric` | 3 | How many palindromic substrings has `abcba`? | 7 (`a`, `b`, `c`, `b`, `a`, `bcb`, `abcba`; by centres and by listing) |
| 3 | l6 | `multi` | 3 | Which can be rearranged into a palindrome: `civic`, `ivicc`, `aabbcd`, `abcde`, `xxyyz`? | `civic`, `ivicc`, `xxyyz` (checked by counting odd letters and by trying every arrangement) |
| 4 | l7 | `numeric` | 3 | `(8+2)*(9-4)/5-3`. | 7 (`10 * 5 / 5 - 3`) |
| 5 | l7 | `numeric` | 3 | Length of the decode of `2[x3[y]]z`. | 9 (`2 * (1 + 3) + 1`; by repeated replacement) |
| 6 | l7 | `numeric` | 3 | `-9/4` when division truncates toward zero. | -2 (floor division gives -3) |
| 7 | l8 | `numeric` | 3 | Profit in pence of the bot on `[100, 95, 100, 106, 90, 89, 95, 99]`. | 10 (two trades: 95 to 100, then 90 to 95) |
| 8 | l9 | `numeric` | 2 | Last entry of the clockwise spiral of the 4 by 3 matrix with rows `1 2 3`, `4 5 6`, `7 8 9`, `10 11 12`. | 8 (the spiral is `1 2 3 6 9 12 11 10 7 4 5 8`; by the bounds method and a visited-set walk) |
| 9 | l9 | `choice` | 3 | A 5 by 5 matrix is rotated 90° clockwise: where does the entry at row 2, column 3 go (zero-based)? | row 3, column 2 (`(r, c)` goes to `(c, n - 1 - r)`). Distractors: row 2, column 1 (a counter-clockwise turn); row 3, column 3 (a transpose); row 1, column 2. |
| 10 | l10 | `numeric` | 3 | Three sells of 4 at 100 (ids 1, 2, 3 in that order); id 1 is amended down to 2; a buy of 7 at 100 arrives. How many does id 3 trade? | 1 (id 1 keeps its place and trades 2, id 2 trades 4, id 3 trades 1; by the engine and by hand) |

### Level 2 homework (`homework-2.json`, 8 items, difficulty 3 to 5 with at least one 5, `tags` on each; three `code` items, one `longform`)

| # | Lesson | Kind | d | Item | Key or reference |
| --- | --- | --- | --- | --- | --- |
| 1 | l7 | `code` | 3 | `simplify_path(path)` (below). | tests below |
| 2 | l9 | `code` | 4 | `life_step(board)` (below). | tests below |
| 3 | l7 | `code` | 5 | `longest_valid_parentheses(s)` (below). | tests below |
| 4 | l8 | `longform` | 4 | Say aloud, timing yourself to three minutes, how you read a long statement: state, events, order of checks, a hand trace. Use the bot on `[100, 99, 99, 99, 98, 97]`. | Model: state is long or flat, entry price and buy day; the event is a day's price; the order is take profit, stop, time; the trace buys 99 on day 1, sells 98 on day 4 for -1, buys 97 on day 5 and sells it at the end: `[-1, 2]`. Rubric (10): 2 names the state, 2 the events, 2 the order of checks, 2 a hand trace with the numbers, 2 the end-of-data rule. |
| 5 | l9 | `numeric` | 4 | Last entry of the clockwise spiral of a 300 by 300 matrix filled row by row from 0. | 45,149 (the bounds method and a visited-set walk) |
| 6 | l7 | `order` | 4 | Decode with a stack: on a digit build the count; on `[` push the text so far and the count and start fresh; on `]` pop, repeat the current text count times and append it to the popped text; on a letter append; return the text. | Distractor: "push the digits as characters onto the stack" with its `why` (a count of 12 splits into 1 and 2). |
| 7 | l10 | `numeric` | 4 | After `[[0,1,0,100,2],[0,2,0,99,3],[0,3,1,99,4],[0,4,1,100,1]]`, what quantity has traded in total? | 4 (trades `[3,1,100,2]` and `[3,2,99,2]`; the spread is then 1) |
| 8 | l8 | `choice` | 3 | For prices `[100, 99, 99, 99, 98, 97]`, which result does the correct rule (`i - bought == 3`) give? | `[-1, 2]`. Distractors: `[-2, 1]` (the rule written `> 3`), `[0, 1]`, `[-1, 1]`. |

**Problem H2.1** `simplify_path(path)`; Python; difficulty 3. Statement: "`path` is an absolute Unix path starting with `/`. `.` means here, `..` means up one folder (the root stays the root), repeated slashes count as one, a name such as `...` is an ordinary name. Return the shortest equivalent path with no trailing slash (the root is `/`)." Reference, starter (returns the path unchanged; fails 5 of 7), tests (brute: `posixpath.normpath` on 3,000 random paths):

@@PY:l2:SP_REF@@

@@PY:l2:SP_START@@

@@T:l2:sp@@

**Problem H2.2** `life_step(board)`; Python; difficulty 4. Statement: "`board` is a rectangle of 0 and 1. One step of the Game of Life: a live cell with 2 or 3 live neighbours (of 8) lives; a dead cell with exactly 3 becomes live; the border has no neighbours beyond it. Return the new board." Reference, starter (returns a copy; fails 5 of 7), tests (brute: counts neighbours with a `Counter` over live cells; the last case is 100 by 100 and sums the live cells):

@@PY:l2:LF_REF@@

@@PY:l2:LF_START@@

@@T:l2:lf@@

**Problem H2.3** `longest_valid_parentheses(s)`; Python; difficulty 5. Statement: "`s` holds `(` and `)`. Return the length of the longest valid (well-formed, contiguous) bracket substring." Reference (a stack of indices with a base of -1), starter (twice the number of `()` pairs; fails 5 of 10), tests (the last is `(` repeated 50,000 times then `)` 50,000 times, answer 100,000, which stops a cubic checker):

@@PY:l2:LV_REF@@

@@PY:l2:LV_START@@

@@T:l2:lv@@

### Level 2 report notes

Report as `docs/LEVEL-BRIEF.md` says. Add to the report any difference between the clang and wasm run and the `g++` runs of the matching engine. Do not edit files outside `app/content/courses/coding-int/` and `app/content/data/coding-int/`.
