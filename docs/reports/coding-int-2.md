# coding-int level 2 ("Strings and simulation"): report

Written from `docs/briefs/coding-int.md` `## Level 2`, following `docs/LEVEL-BRIEF.md` and `docs/AUTHORING.md`. Lesson ids, names, objectives and skills are those of `course.json`. Prices are whole pence throughout (said on the first screen of l8 and l10). Builders and checkers live in the scratchpad folder `coding-int-2` (`build_all.py` rebuilds every file; each builder asserts every keyed number by two methods before it writes).

## Files

All in `app/content/courses/coding-int/`, plus three data files.

| File | Screens | Quiz / items | Code widgets | Notes |
| --- | --- | --- | --- | --- |
| `l6-anagrams-and-palindromes.json` | 10 | 4 | `find_anagrams` (8 tests), `longest_palindrome` (10) | `ci-strings`; `array` canvases with gap cells for centres |
| `l7-parsing-with-a-stack.json` | 11 | 5 | `calculate` (15), `decode_string` (10) | `ci-strings`; two stacks as a stacked `pair` of arrays; a `manipulate` explore with canvas patches |
| `l8-simulating-the-rules.json` | 11 | 4 | `run_strategy` (9), `strategy_from_file` (3, `data`) | `ci-strings`, `ci-timed`; statement in a `console` |
| `l9-grids-and-matrices.json` | 12 | 4 | `spiral_order` (8), `rotate` (6), `capture_regions` (8) | `ci-strings`; `grid` with a `frames` stepper |
| `l10-matching-engine.json` | 12 | 4 | `run_book` + `levels` in Python (12) and C++ (12) | `ci-strings`, `ci-design`; `orderbook` with an `order.size` slider, `pair` with an `array` queue |
| `review-2.json` | | 10 items, d 2 to 4 | | every item has `tags` and `skills`; all five lessons |
| `homework-2.json` | | 8 items, d 3 to 5 (one 5) | `simplify_path` (7), `life_step` (7), `longest_valid_parentheses` (10) | one `longform` (10-point rubric), one `order`, `tags` on each |
| `app/content/data/coding-int/ticks-40.csv`, `ticks-3.csv`, `ticks-header-only.csv` | | | | copied from `docs/briefs/coding-int-scripts/data/`; `ticks-40.csv` checked byte for byte against the text in the brief |

Every code screen has `pace` (600, 840 or 900 s as the brief gives) and `tags`. Every screen carries a family tag from the brief's list for its lesson. New homework families: `path-stack`, `game-of-life`, `longest-valid-brackets` (the brief named none for those items).

## Validator

`node tools/validate.mjs`: **0 errors**. Warnings for my files: one, `l9` screen 8 ("a ladder screen usually reuses the previous canvas kind"): the brief puts the trap (a `console`) between two grid ladders. Level 1 files are missing in this worktree and only warn (`not yet written: 14 of 19 lessons, 3 of 4 reviews, 3 of 4 homework`).

Voice: `VOICE_BASE=<worktree>/app/content/courses/coding-int python3 docs/reviews/voice-scan.py` gives 0 explanations over three sentences and 0 sentences over 20 words (3,233 scanned). No em-dashes, no exclamation marks in prose, £ and pence only.

## Playthrough

`node tools/playthrough.mjs --lesson coding-int/<each of the five> --set coding-int/review-2 --set coding-int/homework-2 --local-cdn <pkgs>`: all passed.

| File | Desktop | 390 px (`--mobile --why`) |
| --- | --- | --- |
| l6 | ok, 14 checks, quiz 4/4 | ok |
| l7 | ok, 16 checks, quiz 5/5 | ok |
| l8 | ok, 15 checks, quiz 4/4 | ok |
| l9 | ok, 16 checks, quiz 4/4 | ok |
| l10 | ok, 16 checks, quiz 4/4 | ok |
| review-2 | ok, recorded 10 of 10 | ok |
| homework-2 | ok, 8 of 8 right, 37 of 37 marks | ok |

The same seven files were played again with `--mobile --why --shots` (390 px copies of every screen, each task's Why? sheet and each wrong-answer Why?): all passed, 486 screenshots. After the last fix (the l10 trap's book total and labels in its explanation) l10 was played again on desktop and at 390 px: passed.

Screenshots were read for every screen at 1280 px and 390 px. Layout fixes made from them: the two parser stacks were drawn about 20 px a cell in a side-by-side `pair` of `array` canvases in `stack` mode, so they became horizontal arrays with a `top` pointer in a stacked `pair`; an empty stack draws nothing, so its caption says "Numbers: empty"; the l10 hook and trap pairs are stacked (`stack: true`) because the side-by-side order book was unreadable; the l8 file screen's starter puts `load_prices` first so the learner's part is in view.

## Starters and solutions in the app (Pyodide 0.27.7 and YoWASP clang 21)

Each code widget was opened in the browser with the local CDN, its starter set (touched) and graded, then its solution graded (script `coding-int-2/zqshot.mjs --codecheck`). Native runs (`coding-int-2/checkcode.py`) gave the same failing rows.

| Widget | Starter fails (in app) | Solution | Wasm time, solution (all tests) | Native CPython |
| --- | --- | --- | --- | --- |
| l6 `find_anagrams` | 3 of 8 (1, 7, 8) | passes | 0.18 s | 0.09 s slowest case |
| l6 `longest_palindrome` | 7 of 10 | passes | 1.36 s (`'a' * 3000` dominates) | 1.02 s |
| l7 `calculate` | 2 of 15 (6, 7) | passes | 0.04 s | under 0.01 s |
| l7 `decode_string` | 8 of 10 | passes | 0.04 s | under 0.01 s |
| l8 `run_strategy` | 9 of 9 | passes | 0.04 s | under 0.01 s |
| l8 `strategy_from_file` | 2 of 3 | passes | 0.04 s | under 0.01 s |
| l9 `spiral_order` | 4 of 8 | passes | 0.09 s | 0.02 s |
| l9 `rotate` | 4 of 6 | passes | 0.06 s | 0.01 s |
| l9 `capture_regions` | 5 of 8 | passes | 0.26 s (400 by 400) | 0.04 s |
| l10 `run_book`/`levels` (Python) | 10 of 12 | passes | 0.06 s | under 0.01 s |
| l10 `run_book`/`levels` (C++) | 10 of 12 | passes | 8.8 s for the first Check (cold compile and warm-up; 10.1 s for the starter before it); runs take milliseconds | g++ `-O1 -fno-exceptions` |
| H2.1 `simplify_path` | 5 of 7 | passes | 0.02 s | under 0.01 s |
| H2.2 `life_step` | 5 of 7 | passes | 0.11 s | 0.01 s |
| H2.3 `longest_valid_parentheses` | 6 of 10 (2, 4, 5, 6, 8, 10) | passes | 0.08 s | 0.01 s |

`longest_palindrome` carries `budget: 10000` as a margin for slow phones; it needs 1.4 s here.

**Matching engine, clang and wasm against g++.** The C++ reference was compiled natively with `g++ -std=c++17` and `-std=c++20`, both `-O1 -fno-exceptions`, and matched the Python reference on the 12 tests and 300 seeded random streams (308 streams, 0 mismatches; `coding-int-2/cpp_check.py`). In the app (clang 21, libc++ hardening, wasm32) the same reference passes the same 12 tests and the starter fails 10 of 12, as natively. No difference was seen. The Python reference also matches an independent flat-list brute force on 4,000 random streams (limit, market, cancel and amend mixed; `coding-int-2/l10ref.py`).

## Numbers and their sources

Every keyed answer is asserted in the builder by two methods before the file is written (brute force or a second implementation in each case):

- l6: anagram starts of `dcabbacbed` for `abc` are 1, 4, 5 (by `Counter` and by sorting each window); 8 windows; 99,001 windows ($n - w + 1$ and by counting starts); 13 centres for 7 letters; palindromic substrings of `abba` and `aaa` are 6 and 6 (by centres and by listing all substrings); palindromic rearrangements (`carerac`, `abcabc`, `aabbccd` yes; `abcd`, `aabbcd` no) by odd counts and by trying every permutation; quiz: 9 windows, `ttaccoa` only.
- l7: the 15 `calculate` rows and quiz values (`12/2*3` = 18, `-8/3` = −2) by the two-stack reference and an independent `ast` evaluator with truncating division; `2*(5+5*2)/3+(6/2+8)` = 21 with an operator-stack peak of 4 (a separate counter); decode rows and lengths 8, 9, 729, 9 by the stack decoder and by repeated innermost replacement with a regular expression; stack depth 3 for `2[a3[b4[c]]]`.
- l8: two bot implementations (the reference loop and a forward scan from each buy) agree on 5,000 random lists; hook `[6, 1]`; trap `[-5, 2]` and the same-day variant `[-10, 3]`; screen 3 list `[100, 98, 99, 100, 103]` where rule 1 and rule 3 both hold on day 4; screen 4 sells on day 5; screen 10 `[250, 240, 245, 252, 249, 247, 236, 240]` gives `[-1, 2]` (same-day variant 3, strict take-profit variant −2), chosen so it differs from the review list; files: `ticks-40.csv` `[249, 8]`, `ticks-3.csv` `[700, 1]`, header only `[0, 0]`, each file parsed by `csv.DictReader` and by `split(',')`.
- l9: spirals by the bounds method and by a visited-set walk (3 by 4 ends at 7; 300 by 300 ends at 45,149); rotations by the transpose-and-reverse code and by `zip(*m[::-1])`; the index map $(r, c) \to (c, n - 1 - r)$ checked on a labelled 5 by 5; capture boards by the stack search and by a fixed-point brute force (the lesson board's safe cells are `r2c5`, `r3c5`, `r3c6`, `r4c2`, `r5c2`; the quiz board captures 2).
- l10: every trade list and level by the reference and the brute force; hook leaves 2; total traded 10; screen 11 best bid 99, best ask 100, traded 4.
- Review: 3, 7, the three palindromic rearrangements, 7, 9, −2, 10 (both bot implementations), 8 (two spiral methods), row 4 column 3 (and each distractor's map), 1 (engine and brute force). Wrong values named in feedback are asserted too (23, 25, 9, 2, 50,125, 49,725 and so on).
- Homework: `simplify_path` against `posixpath.normpath` on 3,000 random paths; `life_step` against a `Counter` of live neighbours, 4,079 on the 100 by 100 board; `longest_valid_parentheses` against an $O(n^3)$ check on 2,000 random strings; 50,124 for the 250 by 400 spiral (two methods); longform trace `[-1, 2]`; engine total 8; the time-rule item `[-5, 2]` with distractors `[1, 2]` (`> 3`), `[2, 3]` (`== 2`), `[0, 1]` (no time rule), all as in `numbers_fix.py`.

## Where the files differ from the brief, and why

- **AUTHORING against the brief.** `data` on the l8 widget is exactly AUTHORING's shape (`"data": { "ticks-40.csv": "content/data/coding-int/ticks-40.csv", ... }`), which is also the brief's. No difference.
- **Difficulty 4 on lesson screens.** The validator caps lesson screens at 3, so `calculate` (l7 screen 6) and the Python engine (l10 screen 7) are difficulty 3 on their screens.
- **One widget per screen.** l7 screen 7 asked for a `numeric` and a `choice`; the two lengths are a `table` widget, and "what to push on `[`" is quiz item 5. l7 screen 4 (value 21 and peak 4), l6 screen 10 (6 and 6), l9 screen 5 (three index maps) and l10 screen 11 (bid, ask, traded) are `table` widgets for the same reason.
- **l7 screen 9 derive.** The brief's ordered decode rules are also homework item 6. The lesson orders the trace of `2[b3[a]]` instead (with the same distractor), and the homework keeps the general rules, with the four cases marked interchangeable (`same`) since their order inside the loop does not matter.
- **l6 quiz.** "Centres for `n = 7`" repeats screen 5, so the quiz asks how many of the 13 are gaps (6).
- **l8 `run_strategy`.** The statement says `prices` may be empty, so a ninth test `run_strategy([])` gives `[0, 0]`; the starter fails 9 of 9 (it raises `IndexError` on the empty list).
- **l8 screen 2.** An `explore` needs an interactive canvas, so the price `array` has a day slider whose caption shows each check, beside the `table` widget of positions at the close.
- **l8 `strategy_from_file` starter.** `load_prices` comes first and the finished `run_strategy` below it, so the part to write is in view.
- **Reference code.** l7's truncating division is written `q = abs(a) // abs(b)` with the sign restored, and l9's `capture_regions` rebuild is shortened; both are equivalent and checked against the independent methods above. The brief's tables are otherwise used row for row.
- **Canvases.** l7 draws each stack as a horizontal `array` with a `top` pointer in a stacked `pair` (stack mode was too small in a pair). l10's hook book adds a bid at 99 (#3) and an ask level at 101 (#4) for context; the questions are unchanged.
- **Review item 7** gives the bot's rules as a short list so each line stays under 20 words.

## Backlog

Five bullets under "Raised later (coding-int L2, 4 Nov)" in `docs/BACKLOG-INBOX.md`: table-cell `wrong[]` ids refused as `byKey` keys by the validator; `array` stack mode unreadable in a side-by-side `pair`; an empty `array` draws nothing; the `orderbook` level label sits in the bid column and is replaced by the walk; the playthrough never checks that lesson and homework starters fail.

## Course map

No `course.json` change proposed.
