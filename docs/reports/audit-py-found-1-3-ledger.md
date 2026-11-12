# Claim ledger: py-found L1 to L3 (concept audit, blind)

Scope: `app/content/courses/py-found/` l1 to l12, review-1 to review-3, homework-1 to homework-3 (performance tasks included). One row per definition, rule, method step, convention, always/never/every/only claim, code-behaviour claim, stated output or number, and the reasoning in each explain, why, hint and feedback line. Lines that share one basis share one row. Verdicts: correct, wrong, imprecise, misleading, unverified.

Paths are JSON paths inside the named file: `s3` is `screens[3]`, `q1` is `quiz[1]`, `i4` is `items[4]`, `o2` is `widget.options[2]` (with its `why`), `w1` is `widget.wrong[1]`, `byKey.x` is `feedback.byKey.x`.

Basis: `run A`, `run B` and `run C` name the three blocks of `docs/reports/py-found-L1-3-concepts.py` (A: solution against hidden tests and starter against them; B: the prose block is executed, the keyed option must describe the run and every other option must not; C: a hand-written check whose label starts with the same file and path). Every `run` row passed under CPython 3.13.18 and under Pyodide 0.27.7 (CPython 3.12.7), unless the verdict says otherwise. Sources: PyRef is *The Python Language Reference* (3.12), PyLib *The Python Standard Library* (3.12), PyTut *The Python Tutorial* (3.12), each with its section; IEEE 754 is the binary64 format; Wiki TC is the Python wiki page TimeComplexity.

Version notes are marked `[ver]`.

## Level 1

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l1-why-not-0-3 | s0.prose, options, hints, feedback, byKey.true | `0.1 + 0.2 == 0.3` prints `False`; `==` asks for an exact match and works on floats; the line prints the comparison, not the sum | correct | run B; PyTut 15 |
| l1-why-not-0-3 | s0.hints[2], feedback.correct | the sum is 0.30000000000000004 | correct | run C; shortest repr, PyTut 15 |
| l1-why-not-0-3 | s0.explain.text | 0.3 is stored "as 0.29999999999999998" | imprecise | finding 2: to 17 places the stored value is 0.29999999999999999 (run C); the digits given are a truncation, beside a rounded sum |
| l1-why-not-0-3 | s0.explain.canvas.caption | the two differ by about 0.00000000000000006 | correct | run C (5.55e-17) |
| l1-why-not-0-3 | s1.prose, options, feedback, explain | truncating 1/3 to n decimals leaves a gap that shrinks tenfold per digit and never reaches zero; 0.00000000333 at 8 digits | correct | derivation: gap is (1/3) x 10^-n; run C |
| l1-why-not-0-3 | s1.explain.text | 0.1 is 0.000110011... in binary, repeating; a float keeps the nearest value with 53 binary digits | correct | run C; IEEE 754 binary64 (53-bit significand) |
| l1-why-not-0-3 | s2.prose | a float is a number with a decimal point, stored in binary with about 17 significant digits | correct | 53 bits is 15.95 decimal digits and 17 always round-trip (run C; PyTut 15); loose but not misleading at "about" |
| l1-why-not-0-3 | s2.canvas rows | stored 0.1, 0.2, 0.3 to 20 places | correct | run C (`'%.20f'`) |
| l1-why-not-0-3 | s2.options, hints, explain | `print(0.1 + 0.2)` shows 0.30000000000000004; stored 0.1 and 0.2 are high, stored 0.3 is low; `print` shows the shortest decimal that reads back as the value | correct | run C; PyTut 15 (repr since 3.1) |
| l1-why-not-0-3 | s3.prose, answer, byKey, explain | halves, quarters and eighths are exact in binary; the six checks; `0.1 * 3` is 0.30000000000000004; `0.7 + 0.1` is 0.7999999999999999 | correct | run C |
| l1-why-not-0-3 | s3.explain.text | prices in pounds and pence are hundredths, so they drift too | correct | true of every hundredth except multiples of 0.25; derivation |
| l1-why-not-0-3 | s4.prose | never test computed floats with `==`; `math.isclose(a, b)` allows a gap of one billionth of the larger number | correct | PyLib math.isclose (rel_tol=1e-09 times max(abs(a), abs(b))) |
| l1-why-not-0-3 | s4.options key, o2, o3 | the lines print `True`, then `False`; next to 0.3 the allowance is 0.0000000003 | correct | run C |
| l1-why-not-0-3 | s4.hints[1], hints[2], o1.why, feedback.correct, byKey.tt, explain.text, explain.canvas.values.r1c2 | on line 2 "the larger number is 0.0", so the allowed gap is 0 | wrong | finding 1: the larger of 5.55e-17 and 0.0 is 5.55e-17 and the allowance is 5.55e-26 (run C; PyLib math.isclose). The printed `False` and the `abs_tol` remedy are right |
| l1-why-not-0-3 | s4.explain.text | near zero give `abs_tol`: `math.isclose(x, 0.0, abs_tol=1e-9)` | correct | run C; PyLib math.isclose |
| l1-why-not-0-3 | s5.prose, solution, tests, hints, byKey, explain | half a penny as a money tolerance; `abs(a - b) < 0.005`; without `abs` a negative gap passes; `==` fails test 1 | correct | run A, run C |
| l1-why-not-0-3 | s6.prose, options, hints, explain, explain.canvas | ten `+= 0.1` end at 0.9999999999999999, so `short` prints; `range(10)` runs ten times; running totals | correct | run B, run C. `[ver]` `sum([0.1] * 10)` is 1.0 from 3.12 (compensated summation); the screen uses a loop, so it is unaffected |
| l1-why-not-0-3 | s7.prose | whole numbers are exact however many you add; `round(x)` gives the nearest whole number as an `int` | correct | PyLib Built-in Functions, round (ties to even is taught in homework-1 i0); int is unbounded, PyLib Numeric Types |
| l1-why-not-0-3 | s7.solution, tests, hints, byKey.test-2, test-3, test-6, explain | `round(p * 100)` per price; `0.29 * 100` is 28.999999999999996; `int` chops; 1999 and 1999.9999999999998 as the two slips | correct | run A, run C |
| l1-why-not-0-3 | s8.prose, options, explain | the safe zero test is `abs(pnl) < 0.005`; `==` and default `isclose` fail on drift; `round(pnl) == 0` passes a £0.40 loss | correct | run C |
| l1-why-not-0-3 | s8.o1.why | next to 0.0 "the allowed gap is zero", so `isclose` acts like `==` | wrong | finding 1 (same reasoning); "acts like `==`" itself is right (run C) |
| l1-why-not-0-3 | s9.prose, solution, tests, hints, byKey, explain | `550.00 / 1.10` is 499.99999999999994; `//` divides whole numbers and drops the remainder; 55000 // 110 is 500 | correct | run A, run C; PyRef 6.7 (floor division; equal to dropping the remainder for positive values) |
| l1-why-not-0-3 | summary | nearest binary value; compare by gap or `isclose` with `abs_tol` near zero; whole pence with `round(p * 100)`; `int(0.29 * 100)` is 28 | correct | rows above |
| l1-why-not-0-3 | q0 | `round(2.675, 2)` prints 2.67; the stored value in full; `round(2.675)` is 3 | correct | run B, run C; PyLib round (note on 2.675) |
| l1-why-not-0-3 | q1 | `/` always returns a float; `6 / 3` prints 2.0; small whole numbers are exact as floats | correct | run B; PyRef 6.7 |
| l1-why-not-0-3 | q2 | `0.57 * 100` is 56.99999999999999; `int` gives 56 (chops towards zero); slip 57 | correct | run C; PyLib int |
| l1-why-not-0-3 | q3 | `0.5 + 0.25 == 0.75` True, `0.2 + 0.4 == 0.6` False (0.6000000000000001); a few tenth sums land exactly by luck | correct | run B, run C (`0.1 + 0.3 == 0.4`) |
| l2-slicing | s0 answer, wrong sets, byKey, explain | `closes[1:4]` is indices 1, 2, 3; starts at `a`, stops before `b`; `b - a` items inside the list | correct | run C; PyLib Sequence Types, note 4 |
| l2-slicing | s1 | `closes[-k]` is `closes[len - k]`; `closes[-2]` is index 4; slips 2 and 3 | correct | run C; PyLib Sequence Types, note 3 |
| l2-slicing | s2 | `closes[-3:]` prints the last three in order; a missing end runs to the end; `[100.4, 103.1]` is `closes[-3:-1]`; 100.40 prints as 100.4 | correct | run B, run C |
| l2-slicing | s3 | step; `closes[0:6:2]` is 0, 2, 4; `closes[1::2]` is 1, 3, 5; wrong sets | correct | run C; PyLib Sequence Types, note 5 |
| l2-slicing | s4 | `prices[len(prices) - n:]`; `prices[-n:]` breaks at n = 0 because -0 is 0 | correct | run A, run C |
| l2-slicing | s5 | `closes[4::5]`; an empty slice, not an error, with three closes; a start of 0 gives `[101.2, 104.0]` | correct | run A, run C |
| l2-slicing | s6 | `b = a` puts a second name on one list; `len(b)` prints 4; assignment never copies a list | correct | run B; PyRef 7.2 (assignment binds a name to an object) |
| l2-slicing | s7.prose | every slice builds a new list, so `a[:]` is a "full copy" | imprecise | finding 3: a slice of a list is a new list (PyLib Sequence Types, `s[:]` is a shallow copy), one level deep (run C) |
| l2-slicing | s7 answer, byKey, explain | `a` and `b` label the list of line 1, `c` the list of line 3; appending through `a` never changes `c` | correct | run C |
| l2-slicing | s8 | copy with `closes[:]`, then append; the caller's list is unchanged | correct | run A |
| l2-slicing | s9 | `a[i:j:k]` rule; with step 1 it holds `j - i` items when both ends lie inside the list; `closes[2:7]` has 5; slips 6 and 7 | correct | run C |
| l2-slicing | s10 | 5-day mean; `sum(closes[-n:]) / n`; 517.40 / 5 = 103.48; first five give 101.40; n at least 1 so -0 cannot bite | correct | run A, run C |
| l2-slicing | summary | slice rule; negative index; `b = a` against `a[:]` | correct | rows above |
| l2-slicing | q0, q1 | `[::-1]` is a reversed copy; a slice past the end stops, an index past the end raises `IndexError`; Python never pads a slice | correct | run B, run C |
| l2-slicing | q2, q3 | `2 3` for copy against name; `closes[1:20:3]` has 7 items; slips 6 and 19 | correct | run B, run C |
| l3-unpacking | s0 | the right side is built first from the old values, then handed out left to right; prints `99.5 100.5` | correct | run B; PyRef 6.16, 7.2 |
| l3-unpacking | s1 | a tuple is values in a fixed order, written with round brackets; unpacking matches by position | correct | PyRef 6.2.3 (the comma makes the tuple; l7 s4 says so); PyRef 7.2 |
| l3-unpacking | s2 | three values into two names: `ValueError: too many values to unpack`; a starred name collects a list; `_` for a spare field | correct | run B (message checked), run C |
| l3-unpacking | s3 | `trade[1] = 72.55` raises `TypeError: 'tuple' object does not support item assignment`; tuples are immutable; Python never builds a new tuple for you | correct | run B, run C; PyLib Tuples (a tuple holding a list is treated in homework-1 i3) |
| l3-unpacking | s4 | `enumerate` hands out (index, item) pairs from 0; prints 1 then 3 | correct | run B; PyLib enumerate |
| l3-unpacking | s5 key, o0, o1, o3, hints, explain | `zip` pairs item by item and stops when the shorter list runs out; nothing is padded | correct | run B, run C; PyLib zip |
| l3-unpacking | s5.o2.why | "`zip` never complains about lengths" | imprecise | finding 4 `[ver]`: `zip(..., strict=True)` raises `ValueError` from 3.10 (run C; PyLib zip) |
| l3-unpacking | s6 | `zip(closes, closes[1:])` gives `len - 1` pairs; simple return (p1 - p0) / p0; 0.0476 when divided by the later close | correct | run A, run C; convention stated by formula |
| l3-unpacking | s7 | `split(",")` returns strings; `'72.50' * '100\n'` is a `TypeError`; `+` would join them; `float(price) * int(qty)` is 7250.0; `int` ignores the newline | correct | run B, run C |
| l3-unpacking | s8 | `",".join(parts)` needs strings; `f"{price:.2f}"`; separators only between parts; `split` and `join` undo each other | correct | run A, run C; PyLib str.join |
| l3-unpacking | s9 | `for ticker, price in rows`; with `enumerate` the second name holds a whole tuple; `ticker, price = rows` unpacks the list; three names raise `ValueError` | correct | run C |
| l3-unpacking | s10 | `strip`, `upper`, `float`, `int`; `float` and `int` ignore surrounding spaces; a returned tuple fixes the record's shape | correct | run A, run C; PyLib str.strip, float |
| l3-unpacking | summary | tuple as fixed record; counts must agree; `zip(closes, closes[1:])`; `split` gives strings | correct | rows above |
| l3-unpacking | q0 | `in` on a string searches inside, on a list compares whole items: `True`, `False` | correct | run B; PyRef 6.10.2 |
| l3-unpacking | q1, q2, q3 | `", ".join` output; `enumerate(..., start=1)` last line `2 Tue`; `strip` then `split(".")` gives `['72', '50']` | correct | run B, run C |
| l4-one-line-lists | s0 | `[round(r * 100, 1) for r in rets]` prints `[1.2, -3.4, 0.5]`; one new list; the `for` part defines `r` | correct | run B; PyRef 6.2.4 |
| l4-one-line-lists | s1, s2 | a trailing `if` filters; 0.0 fails `r < 0`; indices `[1, 3, 6, 8]` | correct | run B; derivation |
| l4-one-line-lists | s3 | `[d for d, r in zip(dates, rets) if r < 0]`; `<=` would keep the flat day | correct | run A |
| l4-one-line-lists | s4 | plain `sorted` compares character codes and every capital comes before every lower-case letter; `key=str.lower` changes the comparison, the items come back unchanged | correct | run B, run C; PyRef 6.10.1 (strings compare by code point) |
| l4-one-line-lists | s5 | a key function receives one item; `reverse=True` puts the largest first; whole tuples come back | correct | derivation; PyLib sorted |
| l4-one-line-lists | s6 | `sorted(rets, key=abs, reverse=True)[:n]`; `sorted` leaves its argument alone; a slice past the end returns what exists; byKey slips | correct | run A, run C |
| l4-one-line-lists | s7 | tuples compare field by field, first fields first; `max(days)` prints `('Wed', 0.012)`; `max` returns a whole item; a key fixes it | correct | run B, run C; PyRef 6.10.1 (lexicographic) |
| l4-one-line-lists | s8, s9 | a comprehension is the loop-and-append pattern; keep a loop when a step needs the previous result; `list(zip(...))` pairs with no loop | correct | PyRef 6.2.4; judgement on readability, standard (PEP 8 spirit) |
| l4-one-line-lists | s10 | `max` and `min` with `key=`; unpack the date; all-loss case; `max` without a key picks 2026-10-15 | correct | run A, run C |
| l4-one-line-lists | summary, q0 to q3 | filter output `[101.2, 100.4]`; `min(..., key=len)` is `bp`; `rets.sort()` returns `None`; `r <= 0` keeps 4 | correct | run B |
| review-1 | i0 key, o0, explain | `1.1 + 2.2 == 3.3` is `False`; the sum is 3.3000000000000003; compare with a tolerance such as `abs(a - b) < 1e-9` | correct | run B, run C |
| review-1 | i0.o2.why | the line prints the comparison, "not the product" | wrong | finding 14: `1.1 + 2.2` is a sum (run C reads the string) |
| review-1 | i1, i2, i3 | `closes[-4:-1]`; nested unpacking `i, (d, px)` prints `2 Wed 100.4`; sort by a key function then `[0][0]` is `AZN` | correct | run B |
| review-1 | i4 | `-4.35 * 100` is -434.99999999999994; `int` chops towards zero to -434; `round` gives -435; slips -435 and 434 | correct | run C |
| review-1 | i5 | slice copy against second name: `101.2 100.0` | correct | run B |
| review-1 | i6 key, o0, o3, explain | `'4.85' * 2` repeats the text; convert with `float` first | correct | run B |
| review-1 | i6.o2.why | "only string times string fails" | wrong | finding 15: a string times a float fails too (run C); homework-3 i7 model shows it |
| review-1 | i7 | `rising_days`: pair with `zip`, number with `enumerate(..., start=1)`, strict `>` | correct | run A |
| homework-1 | i0 | `round` sends an exact tie to the even neighbour: 2 + 4 = 6; an `int` comes back; this avoids an upward bias; for pence ties are rare | correct | run B, run C; PyLib round; IEEE 754 roundTiesToEven |
| homework-1 | i1 | `closes[3:-2]` of 20 has 15 items; slips 16, 17, 1 by the routes named | correct | run C |
| homework-1 | i2 | `[[0.0, 0.0]] * 3` repeats one inner list; a comprehension builds separate ones | correct | run B, run C; PyLib Sequence Types, note 2 |
| homework-1 | i3 | a tuple fixes which objects it holds, not what happens inside them | correct | run B; PyRef 3.1 |
| homework-1 | i4 | k-day return (p[t+k] - p[t]) / p[t]; `zip(closes, closes[k:])`; n - k values; 0.02 from neighbours | correct | run A |
| homework-1 | i5 | parse by `strip`, `split`, skip the header; a return belongs to the later date; Windows line endings stripped; slips named in byKey | correct | run A |
| homework-1 | i6 | Python's sort is stable: tied items keep their order; the order is guaranteed | correct | run B, run C; PyLib sorted ("guaranteed to be stable") |
| homework-1 | i7.prompt, rubric | the script prints `mismatch: 0.30 vs 0.30`; `:.2f` rounds only the display; tolerance fix; whole-pence fix with `round`; pence for a ledger | correct | run C. `[ver]` `sum([0.10, 0.20])` is still 0.30000000000000004 under 3.12's compensated `sum` |
| homework-1 | i7.model | 0.30 "is stored as 0.29999999999999998"; `isclose(0.1 + 0.2 - 0.3, 0.0)` is `False` "because one billionth of 0.0 is 0" | wrong | finding 16 (the two classes of findings 1 and 2; run C) |
| homework-1 | i8 | the comprehension equal to the loop; an `if` before the `for` needs an `else`; a filter goes at the end | correct | run C; PyRef 6.2.4, 6.13 |
| homework-1 | i9 | overnight gap (open - previous close) / previous close; flags by `abs(gap) > limit`; a gap equal to the limit stays out; byKey slips | correct | run A |

## Level 2

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l5-lookup-by-name | s0, s1 | key and value; `d[key]` reads by name, not position; storing under an existing key replaces its value; each key holds one value | correct | PyLib Mapping Types |
| l5-lookup-by-name | s2 | `book[ticker] * prices[ticker]`; a quoted `"ticker"` raises `KeyError: 'ticker'`; short positions carry the sign | correct | run A, run C |
| l5-lookup-by-name | s3 | `.items()` hands back pairs; keys come out in the order first added; replacing a value keeps the key's place; `sorted(prices)` for alphabetical | correct | run B, run C. `[ver]` guaranteed by the language from 3.7 (PyLib Mapping Types, "Changed in version 3.7") |
| l5-lookup-by-name | s4 | `len` of a dict counts keys; `history["VOD"][-1]` indexes the stored list: `2 0.74` | correct | run B |
| l5-lookup-by-name | s5 | a missing key raises `KeyError: 'TSCO'`; `get` returns `None` or the default | correct | run B, run C |
| l5-lookup-by-name | s6 | `get(k, default)`; default only when the key is missing; `get` never raises `KeyError` and never adds the key | correct | run B, run C; PyLib dict.get |
| l5-lookup-by-name | s7 | `history.get(ticker, [])` folds a missing ticker into the empty-list case; `[-1]` on an empty list raises `IndexError` | correct | run A, run C |
| l5-lookup-by-name | s8, s9 | summary block; `len(d)` stays 1; fee as rate times notional; keys match exactly ("lse" is not "LSE"); 20.0, 7.275, 1.5 | correct | run A, run C |
| l5-lookup-by-name | summary, q0 to q3 | `3 500`; `list(d)` gives keys in insertion order; 5.8 with slips 3.8 and 4.3; a stored `None` is returned, not the default | correct | run B |
| l6-membership | s0, s1, s2 | a set holds each value at most once; `set(trades)` drops repeats; `in` gives `True` or `False`; `3 False True`; a set has no positions and may print in any order | correct | run B, run C; PyLib Set Types |
| l6-membership | s3 | `counts[t] = counts.get(t, 0) + 1`; keys in first-seen order | correct | run A |
| l6-membership | s4 key, o1, o3, hints, explain | a list miss costs 5,000 comparisons, a hit 2,500 on average; a set hashes the value to where it would be stored: about 1; five billion against about a million | correct | run C (counted with an instrumented `__eq__`); Wiki TC (list `in` O(n); set `in` O(1) average) |
| l6-membership | s4.o2.why, hints[2], s5.explain, s7.prose, summary.ideas[0] | a set "looks only there", "in the one place"; `x in s` takes about one step "however big `s` is" | imprecise | finding 5: average case; with clashing hashes a lookup costs up to n (run C: 500 comparisons; Wiki TC, set `in` worst case O(n)) |
| l6-membership | s5 | `first_seen` with a set for membership and a list for order; `list(set(trades))` loses the order; the caller's list unchanged | correct | run A; PyLib Set Types (unordered) |
| l6-membership | s6 | `in` on a dict checks keys only; a key holding 0 is still a key; `300 in book.values()` | correct | run B, run C |
| l6-membership | s7 | `{}` is an empty dict, `set()` an empty set, `{"BP", "VOD"}` a set; "`set()` is the only way to write an empty set" | correct | run C; PyRef 6.2.6 ("an empty set cannot be constructed with `{}`"); no empty-set literal exists |
| l6-membership | s8 | netting with `get`; a second loop builds the open book; deleting keys while looping over a dictionary is an error (`RuntimeError`) | correct | run A, run C (the error comes wherever the deleted key sits) |
| l6-membership | summary, q0 to q3 | set length 2; `"VOD" in {"BP": "VOD"}` is `False`; buys minus sells is 1; `{}.add` raises `AttributeError: 'dict' object has no attribute 'add'` | correct | run B, run C |
| l7-arguments | s0, s1 | a default fills a left-out parameter; a passed value replaces it; unnamed values fill from the left, named ones go to their parameter | correct | run B, run C; PyRef 6.3.4 |
| l7-arguments | s2 | positional argument, keyword argument, default; a positional after a keyword is a `SyntaxError` before anything runs; keyword order never matters | correct | run C; PyRef 6.3.4 (grammar of the argument list) |
| l7-arguments | s3 | `def fee(notional, rate=0.001, minimum=1.50)`; `max(notional * rate, minimum)`; order matters for positional calls | correct | run A |
| l7-arguments | s4 | `return a, b` builds one tuple; commas make the tuple; prints `(4.91, 4.72) 2` | correct | run B; PyRef 6.2.3, 7.6 |
| l7-arguments | s5, q3 | a string opening the body is the docstring, stored as `__doc__`, shown by `help`; a comment is discarded; mid and spread | correct | run A, run C; PyRef 8.7 |
| l7-arguments | s6, q2 | a default is evaluated once, when `def` runs; every call that leaves it out shares the object; `['BP', 'VOD']`; 3 | correct | run B, run C; PyRef 8.7 ("evaluated ... when the function definition is executed") |
| l7-arguments | s7 | `None` as the default and a fresh object inside the call; `None` cannot change; a passed book is still updated in place | correct | run A; PyRef 8.7 |
| l7-arguments | s8 | defaults after plain parameters; `f(1, c=[5])` returns `(1, 2, [5])` | correct | run B |
| l7-arguments | s9, summary.formula | maximum drawdown as the largest 1 - value/peak with the starting £1 a peak; -10% twice gives 0.19; mean of returns | correct | run A, run C; standard definition (Bacon, *Practical Portfolio Performance Measurement*, ch. on risk) |
| l7-arguments | q0, q1 | `scale(5, offset=1)` is 11; two values into three names: `ValueError: not enough values to unpack (expected 3, got 2)` | correct | run B, run C |
| l8-who-changes-the-list | s0, s1 | `b = a` adds a label; `list(a)` builds a new list with the same values; `[5, 8, 3]` | correct | run B, run C |
| l8-who-changes-the-list | s2 | a call makes the parameter another label on the object passed; Python never copies on a call; a function that changes the object mutates its argument | correct | run B; PyRef 6.3.4, PyTut 4.8 (call by object reference) |
| l8-who-changes-the-list | s3 options, hints, feedback | `costs = []` moves a local label; `costs.clear()` empties the caller's list: `[1.5, 2.0] []` | correct | run B, run C |
| l8-who-changes-the-list | s3.explain.text | "Methods change objects; `=` moves names" | imprecise | finding 6: many methods change nothing and `d[k] = v`, `xs[0] = v` change the object (run C) |
| l8-who-changes-the-list | s4 key, o2, o3, hints, explain | `sorted` returns a new list; `.sort()` sorts in place and returns `None`; `prices = prices.sort()` loses the list | correct | run B, run C; PyLib list.sort |
| l8-who-changes-the-list | s4.o1.why, q1.feedback.generic | "a method that changes a list in place returns `None`" | imprecise | finding 6: `list.pop` changes the list and returns the item (run C); s9 hedges with "most" |
| l8-who-changes-the-list | s5, s6 | `xs.sort()` inside a function reorders the caller's list; `sorted(xs)` works on a copy; pure function; median of an even count | correct | run A, run B |
| l8-who-changes-the-list | s7 | `return` inside a loop ends the call; falling off the end returns `None`; `1 None`; callers test with `is None` | correct | run B; PyRef 7.6 |
| l8-who-changes-the-list | s8.prose, solution, tests | `dict(book)` copies; `del new[ticker]` removes a key; a new book is returned | correct | run A |
| l8-who-changes-the-list | s8.explain.text, summary.ideas[2], summary.trap | with the copy "every change lands on the copy"; "copy first" makes a function safe | imprecise | finding 7: `dict(d)`, `list(a)` and `a[:]` copy one level; a list stored as a value is shared (run C; PyLib copy, shallow against deep). True for the number values shown |
| l8-who-changes-the-list | s9 | pure: `sorted(xs)`, `xs + [1]`, `dict(d)`; mutating: `xs.sort()`, `xs.append(1)`, `d[k] = v`; most such calls return `None` | correct | run C |
| l8-who-changes-the-list | s10 | early `return None` when a held ticker has no price; £3,145.00; neither dictionary changes | correct | run A, run C |
| l8-who-changes-the-list | summary.ideas[0], ideas[1], formula | assignment and calls never copy; `append`, `sort`, `clear` change the object and return `None` | correct | rows above |
| l8-who-changes-the-list | q0 to q3 | `xs = xs + [0]` builds a new list: `[1] [1, 0]`; `[3, 1, 2].sort()` gives `None`; 150; `[2]` with a `None` default | correct | run B |
| review-2 | i0, i1 | `get` with a default: 300; `3 5` for set and list lengths | correct | run B |
| review-2 | i2 | volume adds `abs(qty)`; netting adds `qty` | correct | run A |
| review-2 | i3, i4 | `('buy', 100, 4.85)`; a lookup hands back the stored list itself: 3 | correct | run B |
| review-2 | i5, i6 | best and worst from a real ticker, not from 0; merge on a copy, net, drop zeros; `dict(a)` leaves both books unchanged | correct | run A (values are whole numbers, so one level of copy is enough) |
| review-2 | i7 | `[]` and `list()` defaults are both made once; a tuple has no `append` (`AttributeError`) | correct | run C |
| review-2 | i8 | pairs in `.items()`, keys in `.keys()`, `in fees` checks keys: `True True False` | correct | run B |
| homework-2 | i0, i1 | latest close per ticker, skipping empty lists; label against `dict(book)` copy: `0 300` | correct | run A, run B |
| homework-2 | i2 | fill P&L `qty * (close - price)`; £35.00, £20.00, £30.00, £8.00 | correct | run A, run C |
| homework-2 | i3 solution, tests, byKey.test-3, test-4 | defaults, `get` for unlisted venues, `max` for the minimum; 0.0012 x 800 = 0.96 | correct | run A, run C |
| homework-2 | i3.byKey.test-1 | "Test 1 calls `commission(20000.00)`" | wrong | finding 17: test 1 calls `commission(25000.00)` (run C compares the strings) |
| homework-2 | i4 | net, drop flat tickers, value what is open, `None` at the first missing price | correct | run A |
| homework-2 | i5.model, rubric | `KeyError: 'BP'`; the shared default gives `{'BP': 100, 'VOD': 50}`; `tickers.sort()` returns `None` and the loop raises `TypeError: 'NoneType' object is not iterable`; `prices[t] in prices` tests a price against keys; 3145.0 | correct | run C |
| homework-2 | i6, i7 | `False None`; 9 with slips 18 and 3 | correct | run B |
| homework-2 | i8 tests, byKey, weights | weight is value over total with cash in the total; a short has a negative weight; `/` not `//`; a new dictionary | correct | run A, run C; convention stated in the prose |
| homework-2 | i8.solution, question, explain | `if total == 0: return None` guards the division for an "exactly hedged" book | misleading | finding 18: `==` on a computed float total, against l1 s4; a book hedged with 0.3 against 0.1 + 0.2 slips through with weights near 1e16 (run C) |

## Level 3

| file | JSON path | claim | verdict | basis |
|---|---|---|---|---|
| l9-splitting-files | s0 key, hints, explain | `import pricing` loads `pricing.py`, found beside the script; a `.py` file you import is a module | correct | run C; PyRef 5.2 to 5.5; PyLib sys.path (first entry is the script's folder) |
| l9-splitting-files | s0.byKey.q-d-c | "`import` only loads `.py` files" | imprecise | finding 8: folders (packages), compiled and built-in modules import too (run C; PyRef 5.2) |
| l9-splitting-files | s1 | `import pricing` creates one name; the dot reaches inside; prints 0.05 | correct | run C (real files) |
| l9-splitting-files | s2 | log return ln(p1 / p0) with `math.log`; 0.04879 against 0.05; a log return is never above the simple one and they match only when the price is unchanged | correct | run A, run C; derivation: ln(1 + r) <= r with equality only at r = 0 |
| l9-splitting-files | s3, summary.ideas[1], q3 | type hints convert nothing and are not checked at run time; `"105" / "100"` raises the stated `TypeError`; `3 * "2.50"` prints `2.502.502.50` | correct | run B (message checked), run C; PyRef 8.7 (annotations do not change semantics); PEP 484 |
| l9-splitting-files | s4, summary.formula.note | importing runs every top-level line once; `0.05` then `0.0488`; a block under `if __name__ == "__main__":` is skipped on import | correct | run C (real files); PyRef 5.3.1 (module cache), PyLib `__main__` |
| l9-splitting-files | s5, q0 | `from statistics import mean` creates only `mean`; `statistics.mean` is a `NameError`; `mean(closes)` is 100.975; `import math` does not create `sqrt` | correct | run B, run C; PyRef 7.11 |
| l9-splitting-files | s6 | band of two sample standard deviations round the mean: £98.97 to £104.03; mean £101.50, sd about £1.26; `pstdev` divides by n | correct | run A, run C; PyLib statistics.stdev, pstdev |
| l9-splitting-files | s7 key, options, q2, review-3 i7 | a local `statistics.py` or `random.py` is imported in place of the real module; the stated `ImportError` and `AttributeError` | correct | run C (real files). `[ver]` 3.13 appends a hint to both messages; the quoted starts still match |
| l9-splitting-files | s7.hints[1], explain.text, summary.ideas[2], summary.trap, q2.explain | "the folder of the script you run is searched first"; never name a file `math.py` | imprecise | finding 9: built-in modules are found before any folder; `math` is built in on Pyodide and on this CPython, so a local `math.py` is not imported (run C; PyRef 5.3, `sys.meta_path` order). The advice is still sound |
| l9-splitting-files | s8 | two import forms; the standard library ships with Python; module table; `from collections import Counter` | correct | PyLib (math, statistics, random, datetime, csv, collections) |
| l9-splitting-files | s9 options, hints | seeding with the same number restarts the same sequence; prints `True`; seed 7 gives `[1.01, 0.99, 1.01]` | correct | run B, run C (same under 3.12 and 3.13) |
| l9-splitting-files | s9.explain.text | "anyone who runs your simulation with seed 7 gets your numbers" | imprecise | finding 11 `[ver]`: guaranteed across Python versions only for `random.random()`; `choice` may change (PyLib random, Notes on Reproducibility) |
| l9-splitting-files | s10 tests, canvas, feedback, explain | the seed 7 path; 21 prices for 20 days; 6 up days; last price £92.22 | correct | run A, run C |
| l9-splitting-files | s10.question, solution | `walk` calls `random.seed(seed)` on the shared generator | misleading | finding 10: the call resets the caller's random sequence too (run C); `random.Random(seed)` is the habit for anything larger (PyLib random, "class random.Random") |
| l9-splitting-files | q1 | `Counter(moves).most_common(1)` is `[('up', 3)]` | correct | run B |
| l10-reading-a-csv | s0, s1 | `csv.DictReader(text.splitlines())` gives one dict per line after the header, keyed by the header; every value is text, exactly as written; `csv.reader` gives a list per line | correct | run B, run C; PyLib csv.DictReader. `[ver]` rows are plain dicts from 3.8 |
| l10-reading-a-csv | s2 | read `row["close"]` by name and convert with `float`; a header-only file gives `[]` | correct | run A |
| l10-reading-a-csv | s3 | a space after the comma is kept: the key is `' close'` and `row["close"]` raises `KeyError`; `skipinitialspace=True` drops it, in the header too | correct | run B, run C; PyLib csv Dialect.skipinitialspace |
| l10-reading-a-csv | s4, summary.ideas[2], summary.trap | strings compare character by character: `max` over the text column gives `'99.80'`; over floats 102.5 | correct | run B, run C; PyRef 6.10.1 |
| l10-reading-a-csv | s5, s6 | UK date strings sort by the day digits; `datetime.strptime(d, "%d/%m/%Y")`; sort (date, string) pairs; the year end | correct | run A, run B, run C; PyLib datetime, strftime and strptime format codes |
| l10-reading-a-csv | s7 | convert each field once, as read; `int(row["qty"])`; `'250' * 1` is still text | correct | run C |
| l10-reading-a-csv | s8 | parse, sort by date, simple returns rounded to 4 places: [0.004, 0.0159, -0.0039, 0.0148]; reversing only works when the file is exactly newest first | correct | run A, run C (rounding is the item's stated output format) |
| l10-reading-a-csv | q0 to q3 | `'101.20' * 2` repeats; `DictReader` skips the header and empty lines: 5; a wrong format raises `ValueError`; ISO dates sort correctly as text | correct | run B, run C (the empty line is skipped under 3.12 and 3.13) |
| l11-when-things-go-wrong | s0, s1 | `float("n/a")` raises `ValueError` and the program stops there; `try` and `except ValueError` skip the bad value and the loop carries on | correct | run B, run C; PyRef 8.4 |
| l11-when-things-go-wrong | s2 solution, tests, hints, explain | `try` inside the loop round the one line; `float` reads `' 99.80 '`, not `''`, `'1,234.50'` or `'-'`; `None` raises `TypeError` and must not be skipped | correct | run A, run C |
| l11-when-things-go-wrong | s2.prose | "keep what `float` can read" as the test for a usable close | misleading | finding 12: `float` also reads `'nan'`, `'inf'` and `'1e5'` (run C; PyLib float grammar), so a feed's NaN marker becomes a close |
| l11-when-things-go-wrong | s3 | an `except` catches only the type it names; dividing by zero raises `ZeroDivisionError: float division by zero`; an exception travels out to the caller; Python does not return infinity | correct | run B (message checked), run C. `[ver]` the message reads "division by zero" from 3.14 |
| l11-when-things-go-wrong | s4, s5 | `raise ValueError("why")` leaves the function; `except ValueError as e` names it and printing shows the message; `int` raises for `'abc'` and `'2.5'` and strips spaces | correct | run A, run B, run C; PyRef 7.8 |
| l11-when-things-go-wrong | s6, summary.ideas[2], summary.trap | a bare `except` catches every error, typos included; `flaot` raises `NameError` each time; a named `except` lets it stop the program at line 5 | correct | run C; PyRef 8.4.1 |
| l11-when-things-go-wrong | s7 | a missing dict key raises `KeyError`; name exactly that | correct | PyLib Built-in Exceptions |
| l11-when-things-go-wrong | s8 | one or three pieces into two names raise `ValueError`; `None.split` raises `AttributeError`, a bug that must stop the program | correct | run A, run C |
| l11-when-things-go-wrong | summary.ideas[0], ideas[1], formula | an exception stops the program unless a `try` around the line (or a caller) has a matching `except`; raise for a value that makes no sense | correct | PyRef 4.3, 8.4 |
| l11-when-things-go-wrong | q0 to q3 | `int("12.5")` raises `ValueError`, `int(float("12.5"))` is 12; `KeyError` for a missing key; `None 0.25`; the whole `try` block is abandoned: 0 | correct | run B, run C |
| l12-data-with-behaviour | s0, s1 | a class bundles facts; `__init__` stores each argument as `self.name`; an instance; a method's first parameter is the object before the dot; 4050.0 | correct | run B; PyTut 9.3; PyRef 3.2 (instance methods) |
| l12-data-with-behaviour | s2 | P&L q x (p - avg); 90.0, -108.0, 25.0 (as floats 90.00000000000021 and so on, accepted by `isclose`) | correct | run A, run C |
| l12-data-with-behaviour | s3 | the default display is the class name and a memory address; `print`, the console and lists all use a defined `__repr__` | correct | run C; PyRef 3.3.1 (`object.__repr__`, `__str__`) |
| l12-data-with-behaviour | s4 solution, tests, byKey | `__repr__` must return a string; `:.2f`; a `__repr__` that prints raises `TypeError` | correct | run A, run C |
| l12-data-with-behaviour | s4.explain.text | "`str()` and lists fall back to `__repr__`" | imprecise | finding 13: `str()` falls back; a list always uses `__repr__`, even when `__str__` exists (run C; homework-3 i4 teaches the true rule) |
| l12-data-with-behaviour | s5 | `qty = qty` sets a local name only; `shel.qty` raises `AttributeError: 'Position' object has no attribute 'qty'` | correct | run B (message checked), run C |
| l12-data-with-behaviour | s6, summary.ideas[2], q2 | a list in the class body is made once and shared by every instance; create it in `__init__` | correct | run B, run C; PyTut 9.3.5 |
| l12-data-with-behaviour | s7, summary.formula | `shel.value(27.00)` is `Position.value(shel, 27.00)`; -108.0 | correct | run C; PyRef 3.2 |
| l12-data-with-behaviour | s8 | `Trade` and `Book`; `net`; cash flow as minus the sum of q x p: -420.0 and -4258.0; each book has its own list | correct | run A, run C |
| l12-data-with-behaviour | q0, q1, q3 | a method without `self` gets one argument too many (`TypeError`); `b = a` shares one object: 300; a list shows items by `__repr__` with no quotes | correct | run B, run C |
| review-3 | i0, i1 | both import forms create their own name: `True`; `sum` over strings raises `TypeError: unsupported operand type(s) for +: 'int' and 'str'` | correct | run B (message checked) |
| review-3 | i2, i3 | separate objects keep separate attributes: `150 100`; all five text closes are above `"100"` as text, three as numbers | correct | run B, run C |
| review-3 | i4 | a miscased key raises `KeyError` on every row and the bare `except` returns `[]` | correct | run C |
| review-3 | i5, i6 | mean close with `statistics.mean`, 101.4 from 507.00; `try` with `except KeyError` only; a list as a key raises `TypeError` | correct | run A, run C |
| review-3 | i8 | new average price (q p + q' p') / (q + q'); 26.50; cost computed before `self.qty` changes | correct | run A, run C |
| homework-3 | i0 | log returns add to the log of the whole move, 0.030529; +100% and -50% cancel as log returns only | correct | run A, run C; derivation |
| homework-3 | i1, i2 | `"%Y-%m-%d %H:%M"`; `%y` is a two-digit year, `%m` the month, `%M` minutes; `skip x` then `3.75` | correct | run B, run C; PyLib datetime format codes |
| homework-3 | i3 | parse the date, `try` only the `float`, skip on `ValueError`, sort (datetime, close) pairs, write back with `strftime`; a wrong header raises `KeyError` | correct | run A |
| homework-3 | i4 | `print(p)` uses `__str__`; a list uses `__repr__`, here the default | correct | run C |
| homework-3 | i5.prose, explain | above £100.00 only with 11 or more ups; exact chance 0.4119; 10 ups leave about £99.90; the simulated share converges to 0.4119 | correct | run C (exact binomial sum; Monte Carlo, 200,000 paths, within 3 standard deviations) |
| homework-3 | i5 tests, feedback | 0.407, 0.4085, 0.502 for the stated seeds | correct | run A under 3.12 and 3.13. `[ver]` tied to `random.choice` (finding 11) |
| homework-3 | i6 | parse the date in `__init__`; raise `ValueError` for a zero quantity; history sorted by parsed date | correct | run A |
| homework-3 | i7.model, rubric | shared class list; text fields give `TypeError: can't multiply sequence by non-int of type 'float'`; a bare `except` returns `[]`; `max` over text gives `'99.80'`; line numbers 5, 21, 22, 28; corrected module | correct | run C; lines counted by hand |
| homework-3 | i8 | whole pence with `round(amount * 100)`; three deposits of £0.70 added as floats give 2.0999999999999996; checks before any change; a list per instance | correct | run A, run C (a float-only account fails the hidden tests, as intended) |
