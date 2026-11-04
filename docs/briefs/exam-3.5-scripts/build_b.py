"""Items of topic-3.5, part B: the coding-int items (12 to 21)."""
from helpers import *

I = {}

# ---------------------------------------------------------------- 12 pattern pick
I[12] = item(
    "e-halts-pattern", 2, ["ci-patterns"], ["pattern-pick"], 60,
    title="Which pattern",
    prose="A venue publishes 5,000 trading halts. Each is a start minute and an end minute, and the halt does not include its end minute.",
    question="You must report the most halts in force at one minute. Which approach fits?",
    widget=choice([
        ("a", "Sort the starts and ends together, then sweep with a counter", True, None),
        ("b", "Build a trie from the minute numbers written as strings", False,
         "A trie answers prefix questions about strings. Overlapping halts have no prefix structure."),
        ("c", "XOR every start minute with every end minute together", False,
         "XOR finds a value left unpaired. Counting overlaps needs a running total."),
        ("d", "Keep a monotonic deque of start minutes over a fixed window", False,
         "A fixed window needs one width. These halts all have different lengths."),
    ]),
    feedback=fb("Turn each halt into a $+1$ and a $-1$ event, sort them and sweep.",
                "Ask what changes over time: how many halts are in force."),
    explain="Turn each halt into two events: $+1$ at its start and $-1$ at its end. Sort the events and add them up in order. The largest running total is the answer, and the sort costs $O(n \\log n)$.")

# ---------------------------------------------------------------- 13 deque trace
I[13] = item(
    "e-deque-back-pops", 3, ["ci-patterns"], ["deque-trace"], 120,
    title="Count the pops from the back",
    prose="A monotonic deque of indices finds the maximum of every window of 4 prices. Before each push it pops from the back every price at most the new one. It pops from the front when that index leaves the window. The prices, in order, are 7, 3, 9, 4, 6, 8, 2, 5, 5, 1.",
    question="How many pops from the back happen in all?",
    widget=numeric(6, abs_=0, placeholder="a whole number", label="Pops from the back", unit="pops",
                   wrong=[("fronts", 2, 0), ("both", 8, 0), ("strict", 5, 0)], accept="6"),
    feedback=fb("The back pops are 2, 1, 1, 1 and 1, which total 6.",
                "Walk the prices one at a time and count only the pops from the back.",
                {"fronts": "You counted pops from the front, 2. The question asks about the back.",
                 "both": "You added the 2 front pops. Count back pops only.",
                 "strict": "You popped only smaller prices. The rule says at most the new one, so the second 5 pops the first."}),
    explain="The 9 pops 3 and 7: 2 pops. The 6, 8 and first 5 pop 4, 6 and 2, and the second 5 pops the first. In all, $2 + 1 + 1 + 1 + 1 = 6$ pops from the back.")

# ---------------------------------------------------------------- 14 two singles (order)
I[14] = item(
    "e-two-singles-steps", 3, ["ci-patterns"], ["two-singles-xor"], 150,
    title="Two ids without a pair",
    prose="A list of 1,000,002 trade ids holds every id twice, except two ids, $a$ and $b$, that appear once. We want both in two passes and constant extra space.",
    question="Put the steps in order. Leave out the two that do not belong.",
    widget=order([
        ("s1", "XOR every id together to get $a \\oplus b$", None),
        ("s2", "Isolate the lowest set bit of that total, $d = t \\,\\&\\, (-t)$", None),
        ("s3", "Split the ids by whether bit $d$ is set", None),
        ("s4", "XOR each group on its own to read off $a$ and $b$", None),
        ("x1", "Count every id in a dict, then keep the two with a count of 1", "That works, but the dict needs space in proportion to the list. The bit method keeps constant space."),
        ("x2", "XOR the total into each group before reading it", "That adds $a \\oplus b$ to both group results and spoils them."),
    ], ["s1", "s2", "s3", "s4"], ["x1", "x2"]),
    feedback=fb("XOR the lot, isolate a bit that differs, split on it, then XOR each group.",
                "Think about what the total of all the ids equals, once the pairs cancel."),
    explain="XOR cancels equal pairs, so the total is $a \\oplus b$, which is not zero. A set bit in it means $a$ and $b$ differ there, so that bit splits them into two groups. Each group XORs down to one of the two ids.")

# ---------------------------------------------------------------- 15 stack parse
I[15] = item(
    "e-signed-division", 3, ["ci-strings"], ["stack-parse"], 120,
    title="Evaluate with signs",
    prose="A parser handles `+ - * /`. The operators `*` and `/` bind tighter, and equal ranks go left to right. A minus sign directly before a number belongs to that number. Division truncates toward zero.",
    question="What is `25 + 7 * -4 / 3 + 17 / -5`?",
    widget=numeric(13, abs_=0, placeholder="a whole number", label="Value",
                   wrong=[("floor", 11, 0), ("no-signs", 37, 0), ("left-to-right", 5, 0)], accept="13"),
    feedback=fb("$-28/3$ truncates to $-9$ and $17/(-5)$ to $-3$, so $25 - 9 - 3 = 13$.",
                "Do the products and quotients first, truncating each toward zero.",
                {"floor": "You rounded down. Truncation toward zero gives $-9$ and $-3$, not $-10$ and $-4$.",
                 "no-signs": "You dropped the two minus signs. They flip the sign of each term.",
                 "left-to-right": "You ignored precedence. Multiplication and division go before addition."}),
    explain="First $7 \\times (-4) = -28$, and $-28 / 3$ truncates to $-9$. Next $17 / (-5)$ truncates to $-3$. So the value is $25 - 9 - 3 = 13$.")

# ---------------------------------------------------------------- 16 rule trace
I[16] = item(
    "e-margin-rules", 2, ["ci-strings", "ci-timed"], ["rule-trace"], 60,
    title="Read the rules, then trace",
    prose="An assessment describes a margin account that starts at £500. Each day, in this order: (1) if the balance is below £400, add £250. (2) Add the day's profit or loss. (3) If the balance is above £700, withdraw half of the amount above £700. The six daily results are $-120$, $-90$, $+60$, $+400$, $-250$ and $-180$, in £.",
    question="What is the balance after day 6?",
    widget=numeric(420, abs_=0, unit="£", placeholder="an amount", label="Balance",
                   wrong=[("withdraw-all", 270, 0), ("never-withdraw", 570, 0), ("half-balance", 320, 0)], accept="420"),
    feedback=fb("The balances run 380, 540, 600, 850, 600 and 420.",
                "Apply the three rules in order each day and write the balance down after day 1.",
                {"withdraw-all": "You withdrew all the amount above £700. The rule takes half of it.",
                 "never-withdraw": "You skipped rule 3. Day 4 ends above £700, so half of the excess leaves.",
                 "half-balance": "You withdrew half of the whole balance. Only half of the amount above £700 leaves."}),
    explain="Day 1 ends at £380. Day 2 tops up to £630 and ends at £540, and day 3 at £600. Day 4 reaches £1,000, so £150 leaves, giving £850, then £600 and £420.")

# ---------------------------------------------------------------- 17 price-time
I[17] = item(
    "e-crossing-buy", 3, ["ci-strings", "ci-design"], ["price-time"], 120,
    title="A buy order crosses the book",
    prose="Four sell orders rest on the book, as shown. Matching uses price-time priority, and each trade is at the resting order's price. A buy order for 20 units at a limit of 100.5 now arrives.",
    canvas={"kind": "table", "params": {
        "columns": ["Order", "Units", "Price", "Arrived"],
        "rows": [["A", "10", "101.0", "1st"], ["B", "5", "100.5", "2nd"], ["C", "8", "100.5", "3rd"], ["D", "6", "100.0", "4th"]],
        "align": ["left", "center", "center", "center"]}, "state": {}},
    question="Which fills happen, in order?",
    widget=choice([
        ("a", "D 6 at 100.0, then B 5 and C 8 at 100.5. One unit rests as a bid.", True, None),
        ("b", "A 10 at 101.0, then B 5 and C 5 at 100.5. Nothing rests.", False,
         "You matched in arrival order. Price priority comes first, and A is above the limit anyway."),
        ("c", "D 6, then B 5 and C 8, all at 100.5. One unit rests as a bid.", False,
         "You traded at the incoming limit. Each fill happens at the resting order's price, so D trades at 100.0."),
        ("d", "D 6 at 100.0, then C 8 and B 5 at 100.5. One unit rests as a bid.", False,
         "You swapped the two orders at 100.5. B arrived before C, so B fills first."),
    ]),
    feedback=fb("Best price first: D. Then B before C by arrival. A is above the limit, so one unit rests.",
                "Sort the sellers by price, then by arrival, and stop at the limit."),
    explain="The lowest price trades first, so D fills 6 at 100.0. The two orders at 100.5 trade in arrival order, B then C, for 13 units in all. A is above the 100.5 limit, so the last unit rests as a bid.")

# ---------------------------------------------------------------- 18 lru state (table)
I[18] = item(
    "e-cache-evictions", 3, ["ci-design"], ["cache-state"], 150,
    title="Who gets evicted",
    prose="A least recently used cache holds 4 keys. A `get` or a `put` of a stored key counts as a use. A `get` of a missing key changes nothing. A `put` of a new key evicts the least recently used key when the cache is full. The steps are: (1) put P, (2) put Q, (3) put R, (4) put S. Then (5) get Q, (6) put P, (7) put T, (8) get R, (9) put U, (10) get P.",
    question="Fill in the table. Type a single letter in each cell.",
    widget={"kind": "table", "columns": ["Question", "Your answer"], "rows": [
        ["Key evicted by step 7", {"edit": True, "answer": "R"}],
        ["Key evicted by step 9", {"edit": True, "answer": "S"}],
        ["Least recently used key after step 10", {"edit": True, "answer": "Q"}],
        ["Most recently used key after step 10", {"edit": True, "answer": "P"}],
    ]},
    feedback=fb("Step 7 evicts R and step 9 evicts S. After step 10 the order runs Q, T, U, P.",
                "Write the keys from least to most recently used after every step.",
                {"r0c1": "Step 7 evicts the key unused longest. A `get` or a `put` of a stored key, at steps 5 and 6, moves it to the newest end.",
                 "r1c1": "After step 7 the order is S, Q, P, T. The missing `get` of R changes nothing, so the oldest key, S, goes.",
                 "r2c1": "Write the keys from oldest to newest use after step 10. The `get` of P at step 10 moves P to the end.",
                 "r3c1": "The newest key is the one used last. Step 10 was a `get` of P."}),
    explain="Steps 5 and 6 turn P, Q, R, S into R, S, Q, P, so T evicts R. The missed get of R changes nothing, so U evicts S. The final order is Q, T, U, P.")

# ---------------------------------------------------------------- 19 minutes plan
I[19] = item(
    "e-sixty-five-minutes", 3, ["ci-timed"], ["minutes-plan"], 120,
    title="Spend the minutes",
    prose="An online assessment gives 70 minutes and four problems. Each can be solved in full, solved in part, or skipped. You earn the marks only if you spend the minutes shown.",
    canvas={"kind": "table", "params": {
        "columns": ["Problem", "Full marks", "Full min", "Part marks", "Part min"],
        "rows": [["P1", "30", "28", "12", "9"], ["P2", "40", "36", "18", "13"], ["P3", "25", "20", "10", "6"], ["P4", "50", "44", "20", "15"]],
        "align": ["left", "center", "center", "center", "center"]}, "state": {}},
    question="What is the most marks you can earn in 70 minutes?",
    widget=numeric(82, abs_=0, unit="marks", placeholder="a whole number", label="Most marks",
                   wrong=[("full-only", 75, 0), ("fill-the-clock", 80, 0), ("all-partial", 60, 0)], accept="82"),
    feedback=fb("Part of P1, all of P2, parts of P3 and P4: 82 marks in 66 minutes.",
                "Compare every mix of skip, part and full that fits inside 70 minutes.",
                {"full-only": "You allowed only full solutions, which reach 75. Partial credit lifts the total.",
                 "fill-the-clock": "You found a plan worth 80 that uses all 70 minutes. A plan using 66 minutes is worth 82.",
                 "all-partial": "You took every part and left 27 minutes unused. Spend them on a full solution."}),
    explain="Take part of P1, all of P2, and parts of P3 and P4: $12 + 40 + 10 + 20 = 82$ marks in $9 + 36 + 6 + 15 = 66$ minutes. All 81 mixes were checked. Full solutions alone reach only 75.")

# ---------------------------------------------------------------- 20 edge case list
CODE20 = "```python\ndef best_window(xs, k):\n    if len(xs) <= k:\n        return None\n    best = sum(xs[:k])\n    for i in range(1, len(xs) - k + 1):\n        best = max(best, sum(xs[i:i + k]))\n    return best\n```"
I[20] = item(
    "e-window-inputs", 4, ["ci-timed"], ["edge-case-list"], 210,
    title="Inputs that expose the bug",
    prose="`best_window(xs, k)` should return the largest sum of $k$ consecutive values, or `None` when the list has fewer than $k$ values. This version has one planted bug.\n\n" + CODE20,
    question="Select all that apply. Which calls return a wrong answer?",
    widget=multi([
        ("a", "`best_window([6], 1)`", True, None),
        ("b", "`best_window([2, 3, 5], 3)`", True, None),
        ("c", "`best_window([4, 1], 2)`", True, None),
        ("d", "`best_window([], 2)`", False, "The list is shorter than $k$, so `None` is right, and the code returns it."),
        ("e", "`best_window([1, 2], 3)`", False, "Two values cannot fill a window of 3. `None` is right, and the code returns it."),
        ("f", "`best_window([5, 1, 4, 2], 2)`", False, "The list is longer than $k$, so the loop runs and returns 6, which is right."),
    ]),
    feedback=fb("The three calls with exactly $k$ values fail: the guard returns `None` for them.",
                "Find the inputs where the guard `len(xs) <= k` gives the wrong branch."),
    explain="The guard uses `<=`, so a list with exactly $k$ values counts as too short. For those lists the answer is the sum of the whole list. The three calls with exactly $k$ values expose it.")

# ---------------------------------------------------------------- 21 active symbols (code, python)
SOL21 = '''from collections import deque

class ActiveSymbols:
    def __init__(self, window):
        self.window = window
        self.log = deque()
        self.count = {}

    def _expire(self, t):
        while self.log and self.log[0][0] <= t - self.window:
            _, s = self.log.popleft()
            self.count[s] -= 1
            if self.count[s] == 0:
                del self.count[s]

    def tick(self, symbol, t):
        self._expire(t)
        self.log.append((t, symbol))
        self.count[symbol] = self.count.get(symbol, 0) + 1

    def active(self, t):
        self._expire(t)
        return len(self.count)
'''
START21 = '''class ActiveSymbols:
    """Distinct symbols traded in the last `window` s."""

    def __init__(self, window):
        pass

    def tick(self, symbol, t):
        """Record a trade in `symbol` at time t."""
        pass

    def active(self, t):
        """Distinct symbols with t - window < s <= t."""
        pass
'''
LARGE21 = ("a = ActiveSymbols(2000)\ntotal = 0\nfor i in range(100000):\n"
           "    a.tick((i * 7919) % 30011, i // 3)\n    total += a.active(i // 3)")
T21 = [
    ("a.active(8)", "2", {"setup": "a = ActiveSymbols(10)\na.tick('X', 1)\na.tick('Y', 5)\na.tick('X', 8)"}),
    ("[a.active(9), a.active(10)]", "[1, 0]", {"setup": "a = ActiveSymbols(10)\na.tick('X', 0)"}),
    ("a.active(3)", "1", {"setup": "a = ActiveSymbols(5)\nfor i in range(4):\n    a.tick('X', i)"}),
    ("[a.active(11), a.active(14), a.active(18), a.active(19)]", "[2, 1, 0, 0]",
     {"setup": "a = ActiveSymbols(10)\na.tick('X', 0)\na.tick('Y', 4)\na.tick('X', 8)"}),
    ("[a.active(0), a.active(100)]", "[0, 0]", {"setup": "a = ActiveSymbols(3)"}),
    ("[a.active(5), a.active(6)]", "[2, 0]", {"setup": "a = ActiveSymbols(1)\na.tick('A', 5)\na.tick('B', 5)\na.tick('A', 5)"}),
    ("total", None, {"setup": LARGE21}),   # expect filled in by build.py from the independent reference
]
I[21] = item(
    "e-active-symbols", 4, ["ci-design", "ci-timed"], ["event-window"], 480,
    title="Symbols that are trading now",
    prose="A market data tool shows how many different symbols have traded recently.",
    question="Write the class `ActiveSymbols(window)`. `tick(symbol, t)` records a trade in `symbol` at time `t`. `active(t)` returns how many distinct symbols traded at a time $s$ with $t - \\text{window} < s \\le t$. Times never go back across calls. Each call should take constant time on average.",
    widget=code_py(START21, SOL21, "", examples=[T21[0]], tests=T21,
                   how="Check runs 7 hidden tests. They cover the window edge, a repeated symbol, a symbol that returns, an idle tool and trades at one time. One test makes 100,000 calls, and a scan of the whole log fails its 5 s limit."),
    feedback=fb("Keep a queue of recent trades and a count per symbol, and expire old trades on each call.",
                "A scan of the whole history on each call is too slow for 100,000 calls."),
    explain="Keep a queue of (time, symbol) and a count of queued trades per symbol. Each call first drops trades at or before $t - \\text{window}$, lowering counts and removing symbols that reach zero. The answer is the number of symbols counted, and each trade enters and leaves the queue once.")

ITEMS_B = I
