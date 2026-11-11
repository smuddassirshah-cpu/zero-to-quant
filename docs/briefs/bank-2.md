# Brief: interview question bank, part 2 (200 items)

Part 2 of the interview question bank (`docs/PLAN.md` and `docs/briefs/interview-plan.md`: about 400 items in all, part 2 is "statistics, finance, coding and more behavioural"; root `PLAN.md` line "Bank part 2 (200 items)"). It writes 200 items into 16 new files in `app/content/bank/`, in four authoring sessions of 50 items each. Two authors can work at once: author A takes sessions 1 and 2, author B takes sessions 3 and 4, and no file is shared. Part 1 is `docs/briefs/bank.md` (20 files, 200 items, live). After part 2 the bank holds 400 items in 36 files.

Part 1 said it held all the behavioural items. The orchestrator has since asked for more, so part 2 adds 32 (the bank then holds 62).

Every answer in section 5 was computed twice by the planner (closed form against enumeration, a linear solve, a seeded simulation or a brute-force twin; C++ facts by `g++ -std=c++20 -fsyntax-only` constant evaluation). Nothing was saved to disk, so each session's committed number script is the record and must reproduce every value. One item is marked `[verify]`.

## 1. What the engine does (checked today in `validate.mjs` `checkBank`, `checkItem`, `checkParts`, `js/engine/select.js`, `tools/playthrough.mjs`, `tools/fresh-check.mjs` and `AUTHORING.md` section 5)

- A bank file is `app/content/bank/<name>.json`: `{ "id": "<name>", "name", "description" (optional), "items": [...] }`. `id` must equal the kebab-case file name; at least one item; a warning above 200 items. The manifest lists every `bank/*.json`. `"sample": true` hides a file (`sample-draw.json` is the only one).
- A bank item is an ordinary item (`id` kebab-case and unique in its file, `difficulty` 1 to 5, `question`, `widget`, `feedback`, `explain`, optional `prose`, `canvas`, `skills`) plus `tags` (required, a list of at most four kebab-case names, the first is the family), `role` (non-empty list from `trader`, `research`, `developer`, `strats`), `style` (one of `mental-maths`, `probability`, `brainteaser`, `market-making`, `statistics`, `finance`, `coding`, `behavioural`; another word is a warning), `source` (one plain line, at most 120 characters), optional `requires` (list of `course/lesson-id`, each checked against that course's map) and optional `pace` (seconds). `skills`, if given, must be real skill ids of any course. `longform` is allowed and needs no `question`. `parts` (2 to 6) are allowed.
- **Tags are not checked against anything.** Any kebab-case word passes. The deck takes `tags[0]` as the family. A course item joins the deck only if it carries `tags`; an untagged course item is counted under its first skill in the pace lines. So a bank item whose first tag is a course skill id shares a family with that course's untagged items in the pace lines, and one whose first tag is a course tag is dealt beside the tagged course items.
- **Widget kinds.** `numeric`, `choice`, `multi`, `expression`, `order`, `table`, `longform` and the rest pass. **`code` is an error**, on the item ("a code item cannot run in the bank deck") and on a part ("a code part cannot run in the bank deck"), for Python and C++ alike.
- The deck (`#bank`) deals 8: due items first, then new ones, one family at a time. Each item has a Leitner box (1, 3, 7, 30 days), keyed by `bank/<file id>/<item id>`: **never rename an item id or a file id once written**. An item with `requires` is drawn only when every named lesson is finished.
- `skills` do real work: the weekly mixed review draws an unseen bank item only when one of its `skills` belongs to a course the learner has met (`select.js` `courseOfItem`). It leaves out `longform` and `code` items (`practiceKind`).
- **Prefix draws.** A mock or stage paper may say `"from": "bank/<prefix>"`, which matches every file `<prefix>-1`, `<prefix>-2` and so on. Live draws use `bank/probability`, `bank/brainteasers` and `bank/market-making` (stage 1, stage 3, `mock-superday-research`). So part 2 must not add files under those three prefixes. Nothing draws `bank/behavioural`, `bank/statistics`, `bank/finance` or `bank/coding` today.
- Tools: `node tools/playthrough.mjs --bank <file id>` plays every item of one file through the real deck from its key; `node tools/fresh-check.mjs --bank <file id>` compares question text with every lesson, set, exam and drill; `ZQ.test.answerWrong()` exists in the player. The validator warns on `[answer-form]`, `[key-length]`, `[tight-band]`, `[wrong-band]`, `[wide-wrong-band]`, `[shown-arithmetic]`, `[shuffled-position]` and `[accept-form]`.
- Not built, so do not design for it: spoken mode with timers (a `longform` is typed, then self-marked), `timed` on a deck, SM-2 ease.

### Engine requirements (each is a requirement for an engine pass, not something to write around)

- **[Must] B2-E1. Python `code` items in the bank.** Today `checkBank` and `checkParts` refuse every `code` widget. Wanted: a bank item or part may carry `widget.kind: "code"` with `language` absent or `"python"`; the deck page runs it as a level review page does (Run examples, Submit, hidden tests); the item is right when every hidden test passes; `playthrough.mjs --bank` first checks that the untouched starter fails, then pastes `solution` and expects every test to pass; `fresh-check.mjs --bank` compares the function name with lesson and drill code. C++ `code` stays refused (compile time in a deck of 8), so part 2 has no C++ `code` item. Update `AUTHORING.md` section 5 (the bank bullet and "Drawn items, Code"). Blocks the 24 `code` items (six per session). Until it lands those 24 are not written and no other kind stands in for them; the other 176 may proceed.
- **[Must] B2-E2. The `--routes-only` pace check assumes no pace of 200 s or more.** It makes the second deck item take 200 s and expects exactly one item over pace. A `code` item needs 240 to 480 s. Wanted: the check reads the second item's `pace` and adds 20 s. Blocks every `pace` above 180.
- **[Must] B2-E3. `--bank --mobile` changes nothing.** `bankPlay` never sets a phone viewport, so the overflow check runs at 1280 px only (raised by the part 1 second read, still open). Wanted: with `--mobile` the whole `--bank` loop repeats at 440 x 956 and fails on sideways scroll. Blocks acceptance step 3, which is otherwise empty.
- **[Must] B2-E4. `numbers_lib.py` has no bank loader.** `Level(course, n)` reads course levels only. Wanted: `Bank("<file id>")` with the same `expect`, `claim`, `check_wrongs` and `report`, paths of the form `items[<item id>].widget.answer`. Blocks the committed number script of acceptance step 2.
- **[Must] B2-E5. A misspelt family passes the validator.** Wanted: a warning `[bank-family]` when a bank item's first tag is neither a skill id of some `course.json` nor the first tag of an item in `content/courses/`. Part 1 lost two families this way.
- **[Must] B2-E6. The results list shows only `question`** (`review.js` `stemOf`), so part 1's 30 behavioural items all read "Answer aloud, then write your answer here." Wanted: for a `longform` item the row shows `widget.prompt`. Part 2 does not depend on it, because rule 11 gives every behavioural item its own `question` line; the requirement is for part 1's items.

Order: one engine pass does B2-E1 to B2-E5 before any session starts its coding file.

## 2. File layout

One file per group per session, 16 files, id equal to the name. New prefixes keep the live prefix draws unchanged.

| Group | Files | Items per file | `style` | `name` of the file |
| --- | --- | --- | --- | --- |
| statistics | `statistics-1.json` to `statistics-4.json` | 15 each | `statistics` | "Interview statistics, set n" |
| finance | `finance-1.json` to `finance-4.json` | 15 each | `finance` | "Interview finance, set n" |
| coding | `coding-1.json` to `coding-4.json` | 12 each | `coding` | "Interview coding, set n" |
| behavioural | `behavioural-5.json` to `behavioural-8.json` | 8 each | `behavioural` | "Interview behavioural questions, set n" (n is 5 to 8) |

Session n writes `statistics-n`, `finance-n`, `coding-n` and `behavioural-(n+4)`. Each file has a one-sentence `description` naming its kinds of question and saying that each item keeps its own schedule. Item ids are `<family>-<two to four words>`, unique across the whole bank (check against all 36 files and `sample-draw.json`). An id names the setting, never a number that a fix pass might change.

| Session | statistics | finance | coding | behavioural | Total |
| --- | --- | --- | --- | --- | --- |
| 1 | 15 | 15 | 12 | 8 | 50 |
| 2 | 15 | 15 | 12 | 8 | 50 |
| 3 | 15 | 15 | 12 | 8 | 50 |
| 4 | 15 | 15 | 12 | 8 | 50 |
| All | 60 | 60 | 48 | 32 | 200 |

| Session | D2 | D3 | D4 | D5 | numeric | choice | code | longform |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 12 | 25 | 11 | 2 | 32 | 4 | 6 | 8 |
| 2 | 12 | 19 | 16 | 3 | 28 | 8 | 6 | 8 |
| 3 | 5 | 28 | 15 | 2 | 30 | 6 | 6 | 8 |
| 4 | 9 | 20 | 18 | 3 | 27 | 9 | 6 | 8 |
| All | 38 | 92 | 60 | 10 | 117 | 27 | 24 | 32 |

There is no difficulty 1. The spread sits lower than part 1 on purpose: these families are asked in online assessments and first rounds, where the test is speed on standard results. 70 items (difficulty 4 and 5) carry `requires`; 130 are drawable on a fresh save.

Each coding file holds six Python `code` tasks (B2-E1), five reasoning-about-code items (numeric or choice, no code runs) and one C++ reading item (choice). C++ appears only as reading items, because the bank will not run C++.

### Which prep paths gain items

`prep.json` names courses and lessons, never bank tags, and is not edited here. A path gains a bank item when the item's `skills` belong to a course on the path (the weekly review then draws it) and when its `requires` lesson is on the path.

| Group | Courses its items' `skills` come from | Prep paths that gain items |
| --- | --- | --- |
| statistics | `estimation`, `testing`, `regression`, `arma`, `garch`, `coint`, `stat-models`, `limits-thm`, `research-int` | `oa-research`, `interview-research`, `superday-research`, `interview-strats`, `interview-trader` (through `limits-thm`), `firm-two-sigma`, `firm-citadel`, `firm-jp-morgan`, `firm-goldman-sachs`, `firm-morgan-stanley` |
| finance | `markets`, `options`, `micro`, `trees`, `garch` | `interview-trader`, `superday-trader`, `interview-strats`, `superday-strats`, `firm-jp-morgan`, `firm-morgan-stanley` |
| coding | `py-found`, `algo-think`, `ds`, `graphs-dp`, `numpy-pandas`, `coding-int`, `cpp` | `oa-research`, `oa-strats`, `oa-developer`, `interview-research`, `interview-strats`, `interview-developer`, `superday-research`, `superday-strats`, `superday-developer`, `firm-jane-street`, `firm-two-sigma`, `firm-citadel`, `firm-jp-morgan`, `firm-goldman-sachs`, `firm-morgan-stanley` |
| behavioural | `recruiting` | every path except `firm-citadel` (it has no `recruiting` step) |

No mock draws the new prefixes. Adding `bank/statistics`, `bank/finance` or `bank/coding` to a mock `draw` is an orchestrator decision after the second read.

## 3. Families and the tags they use

A family is an item's first tag. Every family below is either a skill id in a `course.json` or a tag already carried by course items (counts read from the course files today). Copy them exactly. The numbers are items by session (1/2/3/4).

**statistics**

| Family tag | From | Kind of tag | Items 1/2/3/4 | Total |
| --- | --- | --- | --- | --- |
| `es-estimators` | `estimation` | skill | 1/0/1/1 | 3 |
| `es-biasvar` | `estimation` | skill | 1/0/0/0 | 1 |
| `es-mle` | `estimation` | skill | 1/1/0/1 | 3 |
| `es-intervals` | `estimation` | skill | 1/1/1/1 | 4 |
| `es-bayes` | `estimation` | skill | 1/1/1/1 | 4 |
| `ht-setup` | `testing` | skill | 0/1/1/1 | 3 |
| `ht-pvalue` | `testing` | skill | 1/2/0/0 | 3 |
| `ht-errors` | `testing` | skill | 0/1/1/0 | 2 |
| `ht-multiple` | `testing` | skill | 0/0/1/1 | 2 |
| `rg-fit` | `regression` | skill | 0/1/1/1 | 3 |
| `rg-inference` | `regression` | skill | 1/0/1/1 | 3 |
| `rg-diagnostics` | `regression` | skill | 0/0/1/1 | 2 |
| `rg-multiple` | `regression` | skill | 1/1/1/1 | 4 |
| `ts-models` | `arma` | skill | 1/0/0/0 | 1 |
| `ts-acf` | `arma` | skill | 1/1/1/0 | 3 |
| `ts-forecast` | `arma` | skill | 0/1/1/0 | 2 |
| `gv-models` | `garch` | skill | 0/0/0/1 | 1 |
| `gv-forecast` | `garch` | skill | 0/0/0/1 | 1 |
| `co-spurious` | `coint` | skill | 0/0/0/1 | 1 |
| `sm-nonpar` | `stat-models` | skill | 0/0/0/1 | 1 |
| `dl-clt` | `limits-thm` | skill | 0/1/0/0 | 1 |
| `power` | `research-int` | tag (2 items) | 1/0/0/1 | 2 |
| `multiple-testing` | `research-int` | tag (8) | 1/0/0/0 | 1 |
| `two-regressions` | `research-int` | tag (12) | 1/0/0/0 | 1 |
| `sample-size-for-signal` | `research-int` | tag (6) | 1/0/0/0 | 1 |
| `correlation-bounds` | `research-int` | tag (10) | 1/0/0/0 | 1 |
| `shrinkage-mse` | `research-int` | tag (8) | 0/1/0/0 | 1 |
| `collinear-features` | `research-int` | tag (1) | 0/1/0/0 | 1 |
| `measurement-error` | `research-int` | tag (3) | 0/1/0/0 | 1 |
| `estimator-bias` | `research-int` | tag (6) | 0/0/1/0 | 1 |
| `weak-signal` | `research-int` | tag (9) | 0/0/1/0 | 1 |
| `equicorrelation` | `research-int` | tag (5) | 0/0/1/0 | 1 |

**finance**

| Family tag | From | Kind of tag | Items 1/2/3/4 | Total |
| --- | --- | --- | --- | --- |
| `fi-interest` | `markets` | skill | 1/1/1/1 | 4 |
| `fi-bonds` | `markets` | skill | 1/1/2/1 | 5 |
| `fi-equity` | `markets` | skill | 1/0/0/1 | 2 |
| `fi-forwards` | `markets` | skill | 1/2/2/1 | 6 |
| `op-payoff` | `options` | skill | 0/0/1/0 | 1 |
| `op-strategies` | `options` | skill | 1/2/1/1 | 5 |
| `op-parity` | `options` | skill | 1/1/1/1 | 4 |
| `op-greeks` | `options` | skill | 1/0/1/1 | 3 |
| `ms-book` | `micro` | skill | 1/1/1/1 | 4 |
| `ms-orders` | `micro` | skill | 1/0/0/1 | 2 |
| `ms-costs` | `micro` | skill | 1/1/1/1 | 4 |
| `ms-mm` | `micro` | skill | 0/1/0/0 | 1 |
| `tp-riskneutral` | `trees` | skill | 1/0/1/0 | 2 |
| `tp-multistep` | `trees` | skill | 1/1/1/1 | 4 |
| `tp-bs` | `trees` | skill | 0/0/2/1 | 3 |
| `gv-risk` | `garch` | skill | 1/1/0/0 | 2 |
| `greek-signs` | `trees` | tag (9) | 1/0/0/0 | 1 |
| `option-estimate` | `trees` | tag (9) | 1/0/0/1 | 2 |
| `gamma-pnl` | `trees` | tag (12) | 0/1/0/1 | 2 |
| `digital-option` | `trees` | tag (9) | 0/1/0/1 | 2 |
| `exotic-ranking` | `trees` | tag (11) | 0/1/0/0 | 1 |

**coding**

| Family tag | From | Kind of tag | Items 1/2/3/4 | Total |
| --- | --- | --- | --- | --- |
| `pf-types` | `py-found` | skill | 3/0/0/0 | 3 |
| `pf-functions` | `py-found` | skill | 2/1/0/0 | 3 |
| `pf-collections` | `py-found` | skill | 0/2/0/0 | 2 |
| `pf-idioms` | `py-found` | skill | 0/2/2/1 | 5 |
| `pf-classes` | `py-found` | skill | 0/0/0/1 | 1 |
| `at-complexity` | `algo-think` | skill | 1/0/0/0 | 1 |
| `at-recursion` | `algo-think` | skill | 0/1/1/0 | 2 |
| `at-search` | `algo-think` | skill | 0/0/2/1 | 3 |
| `at-sort` | `algo-think` | skill | 0/0/1/0 | 1 |
| `at-greedy` | `algo-think` | skill | 0/0/1/0 | 1 |
| `ds-arrays` | `ds` | skill | 1/1/0/1 | 3 |
| `ds-hashing` | `ds` | skill | 1/1/0/0 | 2 |
| `ds-pointers` | `ds` | skill | 0/1/0/1 | 2 |
| `ds-stacks` | `ds` | skill | 0/0/1/0 | 1 |
| `ds-trees` | `ds` | skill | 0/0/0/1 | 1 |
| `gd-dp` | `graphs-dp` | skill | 0/1/1/1 | 3 |
| `gd-traversal` | `graphs-dp` | skill | 0/0/0/1 | 1 |
| `np-broadcast` | `numpy-pandas` | skill | 0/0/1/0 | 1 |
| `edge-case-list` | `coding-int` | tag (10) | 1/1/0/1 | 3 |
| `integer-division` | `coding-int` | tag (3) | 2/0/0/0 | 2 |
| `complexity-read` | `coding-int` | tag (2) | 1/0/0/0 | 1 |
| `simulation-rules` | `coding-int` | tag (9) | 0/0/1/1 | 2 |
| `bit-lowest` | `coding-int` | tag (3) | 0/0/0/1 | 1 |
| `copy-vs-move` | `cpp` | tag (5) | 0/1/0/0 | 1 |
| `virtual-dispatch` | `cpp` | tag (6) | 0/0/1/0 | 1 |
| `defined-vs-undefined` | `cpp` | tag (5) | 0/0/0/1 | 1 |

**behavioural** (all `recruiting` tags)

| Family tag | Course items carrying it | Items 1/2/3/4 | Total | Bank total after part 2 |
| --- | --- | --- | --- | --- |
| `star-story` | 9 | 3/3/3/3 | 12 | 22 |
| `why-us` | 5 | 1/1/1/1 | 4 | 9 |
| `reasoning-aloud` | 5 | 1/1/1/1 | 4 | 8 |
| `project-account` | 3 | 1/1/0/1 | 3 | 6 |
| `cv-lines` | 2 | 1/0/1/0 | 2 | 3 |
| `video-answer` | 5 | 1/0/1/0 | 2 | 5 |
| `final-round` | 4 | 0/1/0/1 | 2 | 4 |
| `after-rejection` | 3 | 0/1/0/1 | 2 | 4 |
| `return-offer` | 2 | 0/0/1/0 | 1 | 1 |

No second tag is used. Do not invent a first tag. If a family proves wrong, use the nearest one in these tables and say so in the report.

## 4. Rules for every item

1. **Our own wording and numbers.** Never copy a reported question, a book problem or a course item. Section 5 fixes the numbers; the sentences are yours.
2. **Firm names never appear** in any field. Say "a trading firm", "a market maker", "a bank" or "a hedge fund". Behavioural models use an invented candidate, a generic university setting and firm types.
3. **Every stated number is computed twice** in the session's number script, by two routes that share no code (closed form against enumeration, a linear solve, a brute-force twin or a seeded simulation with a stated tolerance), `Fraction` where the value is rational, with an `assert`. This covers the key, every `wrong` value, every number in `feedback`, `why`, `accept` and `explain`, and every hidden-test `expect`. The values in section 5 are the planner's; the script must reproduce them or the item is reported, not shipped.
4. **Freshness against part 1.** No item may share a template with a part 1 item. Templates already used there and so banned here: the chance of at least one event in n tries, expected distinct values in n draws, a flagged-item posterior from a base rate, delta times contracts as a hedge size, the zero-profit spread against informed flow, the square-root-of-time vol conversion, a percentage chain, the rule of 72. The planner already replaced six ideas for this reason.
5. **Freshness against courses and drills.** Run `node tools/fresh-check.mjs --bank <file id>` (acceptance step 4). The planner read every tagged item of `research-int`, `trees` and `ito` in the families used and the 270 drill names, and changed numbers or twists where they met (list in section 6). No item here is a puzzle from `puzzles` or `brainteasers`. Before writing a `code` item, grep `content/drills` and `content/courses` for its function name and its core rule.
6. **Typed answers state the wanted form.** Every `numeric` question whose key is not a whole number says the form in the question ("to 2 decimal places", "in per cent to 1 decimal place", "in pounds", "as a decimal", "to the nearest whole number"), so `[answer-form]` stays silent. Say the unit in the question.
7. **Tolerance accepts what the feedback prints.** `answer` holds the unrounded value where section 5 gives one. The band must contain the exact value, the value rounded as the question asks, and every form the `accept` line and `feedback.correct` print. Half a unit of the asked place is the default; section 5 gives a wider band where a rule of thumb and the exact value both deserve the mark. No key band may touch a wrong band. `accept` states the fraction and the decimal where both exist.
8. **Numeric items** carry `label`, `placeholder` where a fraction is welcome, and at least two `wrong` entries (`id`, `value`, `tol`), each with a `feedback.byKey` line. Section 5 lists the slips to use; add a third where a natural one exists on the other side of the key. A `wrong` value is given to the places the question asks for.
9. **`wrong` and `why` name the slip.** Every `byKey` line and every option `why` opens with the learner's action in the second person ("You divided by n.", "You kept the delta term only."), then gives the correction. Not the option's flaw ("That ignores..."). A `generic` line points to the method without the answer.
10. **Choice items**: `shuffle` left at its default (on), exactly one `correct`, four options, a `why` on each distractor. Options are of even length: the key is never the longest by more than 9 characters (`[key-length]` must be silent; put the reason in `explain`). No option is named by position. The key never sits between a times-ten pair or two equal slips.
11. **Spoken questions** (`longform`): `widget.prompt` is the interviewer's question as asked. `question` is "Answer aloud, then type it: " followed by three to six words that name this prompt (for example "Answer aloud, then type it: the risk that failed."), so no two rows of a results list match. No `prose`. `model` is a first-person spoken answer of 120 to 180 words by an invented candidate. `rubric` is six lines worth 2, 2, 2, 2, 1 and 1 (part 1's shape). Every line can be ticked from the typed text alone: no tone, eye contact or delivery. If the prompt or a rubric line states a time, `pace` equals it (120 for "two minutes", 90 for "ninety seconds"). Use at most one backtest story per file; vary the settings (a society, a lab, a part-time job, a team sport, a coursework group).
12. **Code items** (after B2-E1): pure Python, standard library only, one function, the signature and one worked call in `prose`, the task in `question`. `starter` is the signature with `...`. Two `examples`, six to ten hidden `tests` that include every case in section 5, `solution`, and a `how` line. Exact results use `"compare": "equal"`, a `Fraction` result `"compare": "fraction"`. The number script runs `solution` on every test in CPython, shows the starter fails, and shows that each "trap" named in section 5 fails at least one hidden test. `pace` 240 to 480.
13. **Reasoning-about-code items**: the code sits in `prose` in a fenced block of at most eight lines; nothing runs. The number script executes the same lines and asserts the key and each slip.
14. **Explanations**: `explain.text` at most three sentences, one idea, the number with its working. No sentence reports the author's check ("A seeded simulation agrees"); use the sentence for the method. Write "per cent", never "percent".
15. **Voice**: British English, second person, no exclamation marks, no em-dashes, no emoji, £ for money (write "dollars" in words), KaTeX in `$...$` with `10{,}000` for thousands. Aim for sentences under 20 words; the gate is 35 (`voice-scan.py 35`).
16. **Fields.** `tags`: the family from section 5, alone. `style`: the group's. `role`: from the Roles column (T `trader`, R `research`, S `strats`, D `developer`). `source`: "Original". `skills`: the family when it is a skill id, plus the skill ids of the "Draws on" lesson. `requires`: `["<Draws on>"]` only at difficulty 4 or 5. `pace` from the table.
17. **A claim must hold as worded.** "Tightest", "smallest", "always" and "cannot" are checked in the number script with `claim`. Where a large-sample or rule-of-thumb value is asked for, the question says so.
18. **The `question` field** carries the one thing to answer; `prose` carries the set-up. A bank item has no hints.

### Item skeletons

Numeric (the part 1 shape, with the explanation ending on method):

```json
{
  "id": "es-bayes-seven-in-ten",
  "difficulty": 3,
  "skills": ["es-bayes", "es-mle"],
  "tags": ["es-bayes"],
  "role": ["research", "strats"],
  "style": "statistics",
  "source": "Original",
  "pace": 90,
  "prose": "Your prior for a coin's chance of heads is Beta(2, 2). You then see 7 heads in 10 flips.",
  "question": "What is the posterior mean? Give 4 decimal places or a fraction.",
  "widget": { "kind": "numeric", "answer": 0.642857, "tol": { "abs": 0.0005 }, "accept": "9/14, or 0.6429.", "label": "Posterior mean", "placeholder": "fraction or decimal",
    "wrong": [ { "id": "no-prior", "value": 0.7, "tol": { "abs": 0.0005 } }, { "id": "one-each", "value": 0.6667, "tol": { "abs": 0.0005 } } ] },
  "feedback": { "correct": "Correct. 9/14 = 0.6429.", "generic": "Not quite right. Add the prior counts to the observed counts first.",
    "byKey": { "no-prior": "You used 7/10 and left the prior out. Beta(2, 2) adds 2 heads and 2 tails.", "one-each": "You added one head and one tail. This prior adds two of each." } },
  "explain": { "text": "A Beta(2, 2) prior acts like 2 heads and 2 tails seen before. The posterior is Beta(9, 5). Its mean is $9/14 = 0.6429$." }
}
```

Code (valid only after B2-E1):

```json
{
  "id": "integer-division-lot-round",
  "difficulty": 3,
  "skills": ["ci-strings"],
  "tags": ["integer-division"],
  "role": ["developer", "research", "strats"],
  "style": "coding",
  "source": "Original",
  "pace": 300,
  "prose": "An order size must be a whole number of lots. `lot_round(qty, lot)` rounds a signed quantity towards zero: `lot_round(250, 100)` is `200`.",
  "question": "Complete `lot_round`.",
  "widget": { "kind": "code", "language": "python", "starter": "def lot_round(qty, lot):\n    ...\n",
    "examples": [ { "call": "lot_round(250, 100)", "expect": "200", "compare": "equal" }, { "call": "lot_round(-250, 100)", "expect": "-200", "compare": "equal" } ],
    "tests": [ { "call": "lot_round(-250, 100)", "expect": "-200", "compare": "equal" }, { "call": "lot_round(-99, 100)", "expect": "0", "compare": "equal" } ],
    "how": "Submit runs 7 hidden tests. Each result must equal the expected whole number.",
    "solution": "def lot_round(qty, lot):\n    lots = abs(qty) // lot\n    return lots * lot if qty >= 0 else -lots * lot\n" },
  "feedback": { "correct": "Every hidden test passed.", "generic": "Not all tests pass yet. Try a negative quantity that is not a whole number of lots." },
  "explain": { "text": "Floor division rounds down, so `-250 // 100` is `-3`. Round the size, then put the sign back." }
}
```

(The `skills` of the code skeleton are copied from the Draws-on lesson when written.) A choice item uses `widget.options` with `correct: true` on one and a `why` on each other. A longform item is `{ "id", "difficulty", "skills", "tags", "role", "style", "source", "pace", "question", "widget": { "kind": "longform", "prompt", "model", "rubric": [ { "points": 2, "text": "..." } ] }, "feedback": { "correct", "generic" }, "explain": { "text" } }`; copy the field names from `bank/behavioural-4.json`.

## 5. The items

Columns: **Id** (the real item id), **Family** (first and only tag), **D**, **Kind**, **Pace** (seconds), **Roles**, **Draws on** (`course/lesson-id`: its skills are copied, and it is the `requires` at difficulty 4 or 5), **Question** (the situation and its exact numbers; the wording is the author's), **Answer** (the key, its working, the tolerance where the key is not whole, and the slips for `wrong`). Whole-number keys take `tol` 0 unless stated. If an idea cannot be made correct and unambiguous, swap it for another of the same family, kind and difficulty and say so in the report.

### Session 1 (author A)

##### Session 1: statistics (15 items, file `statistics-1.json`)

| Id | Family | D | Kind | Pace | Roles | Draws on | Question | Answer |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `es-mle-waits-between-trades` | `es-mle` | 2 | numeric | 75 | R,S | `estimation/l6-maximising` | Six waits between trades are 4, 9, 2, 7, 5 and 3 seconds, modelled as exponential. Maximum-likelihood rate per second, as a decimal. | 0.2 (6/30), tol 0.0005. Slips: 5 (gave the mean wait), 0.1667 (used 5/30). |
| `es-biasvar-four-closes` | `es-biasvar` | 3 | numeric | 90 | R,S | `estimation/l4-bias-against-variance` | Four closes are 4, 7, 9 and 12. Unbiased sample variance, to 2 decimal places. | 11.33 (34/3), tol 0.005. Slips: 8.50 (divided by 4), 3.37 (gave the standard deviation). |
| `es-intervals-halve-the-width` | `es-intervals` | 2 | numeric | 60 | R,S,T | `estimation/l9-how-precise` | A 95% interval for a mean from 64 observations has half-width 2.94. How many observations give half-width 1.47 at the same spread? | 256. Slips: 128 (doubled n), 32 (halved n). |
| `es-bayes-seven-in-ten` | `es-bayes` | 3 | numeric | 90 | R,S | `estimation/l12-updating-a-belief` | Prior Beta(2, 2) on a coin's chance of heads, then 7 heads in 10 flips. Posterior mean, to 4 decimal places or a fraction. | 0.6429 (9/14), tol 0.0005. Slips: 0.7 (left the prior out), 0.6667 (added one head and one tail). |
| `ht-pvalue-thirteen-of-sixteen` | `ht-pvalue` | 3 | numeric | 120 | R,S,T | `testing/l3-p-value` | 16 flips give 13 heads. Exact two-sided p-value for a fair coin, to 4 decimal places. | 0.0213 (697/32768), tol 0.0005. Slips: 0.0106 (one tail), 0.0124 (normal curve at z = 2.5). |
| `power-one-sided-shift` | `power` | 4 | numeric | 150 | R,S | `research-int/l4-tests-in-words` | Known sd 12, n = 36. Test mean 0 against a higher mean at 5% one-sided (critical z 1.645). The true mean is 4. Power, to 4 decimal places. | 0.6387 ($\Phi(0.355)$), tol 0.001. Slips: 0.3613 (gave the miss rate), 0.5160 (used the two-sided 1.96). |
| `multiple-testing-how-many-tests` | `multiple-testing` | 4 | numeric | 150 | R,S | `research-int/l4-tests-in-words` | A signal has z = 3.2, two-sided p = 0.001374. Largest number of tests for which it still passes Bonferroni at 5% overall. | 36 (0.05/0.001374 = 36.38). Slips: 37 (rounded up), 72 (used the one-sided p). |
| `two-regressions-two-slopes` | `two-regressions` | 3 | numeric | 75 | R,S | `research-int/l1-two-regressions` | The least squares slope of y on x is 2.5 and of x on y is 0.1. Correlation, as a decimal. | 0.5 ($\sqrt{2.5 \times 0.1}$), tol 0.0005. Slips: 0.25 (no square root), 0.04 (divided the slopes). |
| `rg-inference-t-from-r-squared` | `rg-inference` | 3 | numeric | 100 | R,S | `regression/l6-is-slope-zero` | A one-predictor regression on 102 points has $R^2 = 0.2$. The slope's t statistic, to 1 decimal place. | 5.0 ($\sqrt{0.2 \times 100/0.8}$), tol 0.04. Slips: 4.5 ($\sqrt{0.2} \times 10$, no $1 - R^2$), 2.5 (used $R^2/(1 - R^2)$ without the root). |
| `rg-multiple-left-out-factor` | `rg-multiple` | 4 | numeric | 120 | R,S | `regression/l9-several-predictors` | $y = 1.5x_1 - 2x_2 +$ noise, and regressing $x_2$ on $x_1$ gives slope 0.4. Slope of y on $x_1$ alone, to 1 decimal place. | 0.7 (1.5 - 2 × 0.4), tol 0.005. Slips: 1.5 (no bias), 2.3 (added the bias). |
| `ts-models-ar1-long-run-variance` | `ts-models` | 3 | numeric | 90 | R,S | `arma/l7-today-depends-on-yesterday` | $x_t = 0.6x_{t-1} + e_t$ with noise variance 16. Stationary variance of x. | 25 (16/0.64), tol 0.005. Slips: 40 (divided by 1 - 0.6), 16 (noise only). |
| `ts-acf-ma1-first-lag` | `ts-acf` | 3 | numeric | 90 | R,S | `arma/l9-shocks-that-linger` | $x_t = e_t + 0.75e_{t-1}$. Lag-1 autocorrelation, to 2 decimal places. | 0.48 (0.75/1.5625), tol 0.005. Slips: 0.75 (gave the coefficient), 0.43 (divided by 1.75). |
| `sample-size-for-signal-sharpe-years` | `sample-size-for-signal` | 4 | numeric | 120 | R,S,T | `research-int/l10-weak-signals` | A strategy's true annual Sharpe ratio is 0.7. Years of returns until its expected t statistic reaches 2, to 1 decimal place. | 8.2 ($(2/0.7)^2 = 8.16$), tol 0.05. Slips: 2.9 (no square), 7.8 (used 1.96). |
| `correlation-bounds-highest-third` | `correlation-bounds` | 4 | numeric | 150 | R,S | `research-int/l2-correlation-limits` | corr(X, Y) = 0.28 and corr(Y, Z) = 0.96. Highest possible corr(X, Z), to 4 decimal places. | 0.5376 (0.2688 + 0.96 × 0.28; the lowest is 0), tol 0.0005. Slips: 0.2688 (product only), 1 (no limit). |
| `es-estimators-median-standard-error` | `es-estimators` | 5 | numeric | 180 | R,S | `estimation/l2-estimates-vary` | 100 normal draws with sd 2. Large-sample standard error of the sample median, to 3 decimal places. | 0.251 ($0.2\sqrt{\pi/2} = 0.2507$; 40,000 seeded samples give 0.2499), tol 0.002. Slips: 0.2 (standard error of the mean), 0.314 (no square root on $\pi/2$). |

##### Session 1: finance (15 items, file `finance-1.json`)

| Id | Family | D | Kind | Pace | Roles | Draws on | Question | Answer |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `fi-interest-monthly-to-annual` | `fi-interest` | 2 | numeric | 60 | T,S | `markets/l3-comparing-rates` | 6% a year compounded monthly. Effective annual rate, in per cent to 2 decimal places. | 6.17 ($1.005^{12} - 1$), tol 0.004. Slips: 6.18 (continuous, 6.1837), 6.00 (nominal). |
| `fi-bonds-duration-move` | `fi-bonds` | 2 | numeric | 60 | T,S | `markets/l6-yield` | Modified duration 7. The yield rises 25 basis points. Approximate price change, in per cent to 2 decimal places. | -1.75, tol 0.005. Slips: 1.75 (sign), -17.5 (read 25 bp as 2.5%). |
| `fi-forwards-six-month-fair` | `fi-forwards` | 2 | numeric | 75 | T,S | `markets/l10-cost-of-carry` | Share £80, no dividends, 5% continuously compounded. Fair six-month forward, in pounds to 2 decimal places. | 82.03 ($80e^{0.025}$ = 82.0252), tol 0.005. Slips: 82.00 (simple interest), 84.10 (a full year). |
| `fi-equity-growing-dividend` | `fi-equity` | 3 | numeric | 75 | T,S,R | `markets/l7-shares` | Next year's dividend is £3 and grows 4% a year for ever. Required return 9%. Price in pounds. | 60 (3/0.05), tol 0.005. Slips: 33.33 (no growth), 62.40 (grew the first dividend again). |
| `op-parity-price-the-put` | `op-parity` | 3 | numeric | 100 | T,S | `options/l9-put-call-parity` | Share £50, strike £52, six months, 4% continuously compounded, no dividends. The call costs £3.10. Put, in pounds to 2 decimal places. | 4.07 ($3.10 - 50 + 52e^{-0.02}$ = 4.0703), tol 0.005. Slips: 5.10 (strike not discounted), 2.13 (signs swapped). |
| `op-strategies-bull-spread-breakeven` | `op-strategies` | 2 | numeric | 60 | T,S | `options/l5-spreads` | Buy the 100 call at £6 and sell the 110 call at £2. Break-even share price at expiry, in pounds. | 104. Slips: 106 (ignored the premium received), 108 (added both premiums). |
| `op-greeks-second-order-estimate` | `op-greeks` | 3 | numeric | 75 | T,S | `options/l12-how-price-responds` | A call costs £4.00 with delta 0.45 and gamma 0.05. The share rises £2. Estimated new price, in pounds to 2 decimal places. | 5.00 (4 + 0.90 + 0.10), tol 0.005. Slips: 4.90 (delta only), 5.10 (no half on gamma). |
| `tp-riskneutral-one-step-with-rate` | `tp-riskneutral` | 3 | numeric | 100 | T,S,R | `trees/l3-risk-neutral` | A share at 100 moves to 120 or 90 in one step. The rate is 5% over the step. Call struck at 105, to 2 decimal places. | 7.14 (q = 0.5, 7.5/1.05; replication gives the same), tol 0.005. Slips: 7.50 (not discounted), 5.00 (q = 1/3 from a zero rate). |
| `tp-multistep-american-put-two-step` | `tp-multistep` | 5 | numeric | 180 | S,T,R | `trees/l7-american-on-a-tree` | Share 100; each step it rises 10% or falls 10%; the rate is 5% a step; two steps. American put struck at 100, to 2 decimal places. | 2.55 (q = 0.75; exercise at 90 for 10; 2.5510), tol 0.005. Slips: 1.42 (European), 2.68 (root not discounted). |
| `ms-book-sweep-four-hundred` | `ms-book` | 2 | numeric | 60 | T,D | `micro/l2-walking-the-book` | Offers: 100 at 10.01, 200 at 10.02, 500 at 10.04. A market buy takes 400. Average price paid, in pounds to 4 decimal places. | 10.0225 (4009/400), tol 0.00005. Slips: 10.0233 (unweighted mean), 10.0400 (last price). |
| `ms-costs-effective-spread` | `ms-costs` | 3 | numeric | 75 | T,D | `micro/l5-crossing-the-spread` | Bid 19.98, ask 20.02. Your buy fills at 20.01. Effective spread, in basis points of the mid. | 10 (2 × 0.01/20.00), tol 0.005. Slips: 20 (quoted spread), 5 (not doubled). |
| `ms-orders-stop-through-a-gap` | `ms-orders` | 2 | choice | 60 | T,D | `micro/l4-market-or-limit` | You hold a sell stop at 95. Bad news comes and the next trade is 93. What happens to the stop, and to a stop-limit at 95? | The stop becomes a market order and sells near 93; the stop-limit rests unfilled at 95. Distractors: sells at 95; both sell at 93; neither triggers. `[verify]` against the wording of `micro/l4`: a definition, not run. |
| `greek-signs-calendar-spread` | `greek-signs` | 4 | choice | 100 | T,S | `trees/l14-greeks-by-shape` | Long a one-year at-the-money call, short a three-month call at the same strike, r = 0. Signs of gamma, vega and theta. | Gamma negative, vega positive, theta positive (Black-Scholes at 100, vol 20%: -0.0200, +19.77, +4.00 a year). Distractors: the three other sign patterns a long call, a short call and a long straddle give. |
| `gv-risk-one-day-var` | `gv-risk` | 3 | numeric | 75 | T,S,R | `garch/l10-value-at-risk` | A £3,000,000 position, daily vol 1.2%, normal returns. One-day 99% value at risk in pounds, using 2.326. | 83,736, tol 1. Slips: 59,220 (used 1.645), 264,796 (scaled to ten days). |
| `option-estimate-short-dated-call` | `option-estimate` | 4 | numeric | 90 | T,S | `trees/l13-rules-of-thumb` | Share £150, vol 32%, expiry one sixteenth of a year, r = 0. At-the-money call by the 0.4 rule, in pounds to 2 decimal places. | 4.80 (0.4 × 150 × 0.32 × 0.25; Black-Scholes 4.79), tol 0.02. Slips: 1.20 (used T, not its root), 19.20 (no time factor). |

##### Session 1: coding (12 items, file `coding-1.json`)

| Id | Family | D | Kind | Pace | Roles | Draws on | Question | Answer |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `ds-arrays-sign-changes` | `ds-arrays` | 2 | code | 240 | D,R,S | `ds/l1-arrays-in-memory` | Write `sign_changes(pnl)`: the number of times consecutive non-zero entries differ in sign. Zeros are skipped. | `[3, -1, 0, -2, 5, 0, 0, -4]` gives 3; `[]` 0; `[0, 0]` 0; `[1, 2, 3]` 0; `[-1, 0, 1]` 1. Trap: comparing neighbours without dropping zeros. |
| `ds-hashing-price-mode` | `ds-hashing` | 2 | code | 240 | D,R,S | `ds/l4-frequencies` | Write `price_mode(prices)`: the most frequent price, the highest on a tie, `None` for an empty list. | `[101, 100, 101, 100, 99]` gives 101; `[5]` 5; `[]` None; `[7, 8, 9]` 9. Trap: `max(set(xs), key=xs.count)` with no tie rule. |
| `edge-case-list-to-pence` | `edge-case-list` | 3 | code | 360 | D,R,S | `coding-int/l16-edge-cases-first` | Write `to_pence(text)`: a price string to whole pence as an `int`. A £ sign, thousands commas, outer spaces and a leading `-` are optional; there are no, one or two decimals. | `"£1,234.50"` gives 123450; `"0.07"` 7; `"12"` 1200; `"£3.5"` 350; `"-£2.05"` -205; `"£0.29"` 29; `" £19.99 "` 1999. Trap: `int(float(s) * 100)` gives 28, -204 and 1998. |
| `integer-division-lot-round` | `integer-division` | 3 | code | 300 | D,R,S | `coding-int/l7-parsing-with-a-stack` | Write `lot_round(qty, lot)`: round a signed quantity towards zero to a multiple of `lot`. | `(-250, 100)` gives -200; `(250, 100)` 200; `(-99, 100)` 0; `(300, 100)` 300; `(-300, 100)` -300. Trap: `qty // lot * lot` gives -300 for the first. |
| `pf-types-parse-fix` | `pf-types` | 3 | code | 360 | D | `py-found/l2-slicing` | Write `parse_fix(msg)`: `"35=D;55=VOD.L;38=100"` to a dict of int tag to string value. Split each field at its first `=`; a repeated tag keeps the last value; `""` gives `{}`. | `{35: "D", 55: "VOD.L", 38: "100"}`; `"58=a=b"` gives `{58: "a=b"}`; `"35=D;35=F"` gives `{35: "F"}`; `""` gives `{}`. Traps: `split("=")` without a limit; no guard for the empty string. |
| `pf-functions-binom-tail` | `pf-functions` | 4 | code | 420 | R,S,T | `py-found/l7-arguments` | Write `binom_tail(n, k)`: the exact chance, as a `Fraction`, of at least k heads in n fair flips. | `(16, 13)` gives 697/65536; `(10, 5)` 319/512; `(5, 0)` 1; `(4, 5)` 0; `(0, 0)` 1. `compare: "fraction"`. Traps: a float result; "more than k" for "at least k". |
| `pf-types-round-half-even` | `pf-types` | 3 | numeric | 45 | D,R | `py-found/l1-why-not-0-3` | What does `round(0.5) + round(1.5) + round(2.5)` return in Python 3? | 4 (0 + 2 + 2). Slips: 6 (rounded halves up), 3 (rounded halves down). |
| `pf-functions-default-list` | `pf-functions` | 3 | numeric | 60 | D,R | `py-found/l7-arguments` | `def add(x, acc=[]): acc.append(x); return len(acc)`. What is `add(1) + add(2) + add(3)`? | 6 (1 + 2 + 3, one shared list). Slips: 3 (a fresh list each call), 9 (three every time). |
| `complexity-read-doubling-inner` | `complexity-read` | 3 | choice | 60 | D,R,S | `algo-think/l2-big-o` | Outer `for i in range(n)`, inner `j = 1` then `while j < n: j *= 2`. Running time? | $O(n \log n)$ (10,240 inner steps at n = 1,024). Distractors: $O(n)$, $O(n^2)$, $O(\log n)$. |
| `at-complexity-tripling-loop` | `at-complexity` | 2 | numeric | 45 | D,R,S | `algo-think/l1-counting-work` | `i = 1; count = 0`, then `while i < 1000: i *= 3; count += 1`. Final `count`? | 7 ($3^7$ = 2,187). Slips: 6 (stopped at 729), 333 (divided 1,000 by 3). |
| `pf-types-backward-slice` | `pf-types` | 2 | numeric | 45 | D,R | `py-found/l2-slicing` | `xs = list(range(10))`. What is `sum(xs[7:2:-2])`? | 15 (`[7, 5, 3]`). Slips: 25 (step of -1), 12 (started at 6). |
| `integer-division-toward-zero` | `integer-division` | 3 | choice | 60 | D | `cpp/l2-fixed-types` | For ints, C++ `-7 / 2` and `-7 % 2`, against Python `-7 // 2` and `-7 % 2`. | C++ gives -3 and -1; Python gives -4 and 1. Distractors: both -3 and -1; both -4 and 1; C++ -4 and 1 with Python -3 and -1. |

##### Session 1: behavioural (8 items, file `behavioural-5.json`)

| Id | Family | D | Kind | Pace | Roles | Draws on | Prompt | The model must show |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `star-story-risk-that-failed` | `star-story` | 3 | longform | 120 | T,R,S,D | `recruiting/l11-stories-that-answer` | Tell me about a risk you took that did not pay off. | The odds as you saw them then, the loss in a number, and what you would repeat. |
| `star-story-unpopular-decision` | `star-story` | 3 | longform | 120 | T,R,S,D | `recruiting/l11-stories-that-answer` | Describe a decision of yours that was unpopular with the group. | Your reason, how you told them, and the result against the alternative. |
| `star-story-unasked-problem` | `star-story` | 3 | longform | 120 | T,R,S,D | `recruiting/l11-stories-that-answer` | Tell me about a problem you spotted that nobody had asked you to look for. | How you noticed, whom you told and when, and what changed. |
| `why-us-a-first-year-day` | `why-us` | 4 | longform | 120 | T,R,S | `recruiting/l8-why-this-firm` | What do you think a first-year in this role does all day, and which part would you find hardest? | Three concrete tasks, one honest weakness, and a plan for it. |
| `reasoning-aloud-bet-with-unknown-odds` | `reasoning-aloud` | 4 | longform | 120 | T,R,S | `recruiting/l12-reasoning-aloud` | I offer you a bet and I will not tell you the odds. What do you ask me before you decide? You have two minutes. | Questions in order of value: payoff, who sets the price, repeats, stake limit; then a decision rule. |
| `project-account-decision-to-redo` | `project-account` | 4 | longform | 150 | R,S,D | `recruiting/l7-projects-that-count` | Which decision in your project would you make differently now, and what would it change? | The decision, the evidence that it was wrong, the redo, and the size of the effect. |
| `cv-lines-change-of-direction` | `cv-lines` | 3 | longform | 120 | T,R,S,D | `recruiting/l6-one-page-cv` | Take me through the change of direction on your CV. | The reason at the time, what carried over, and no apology. |
| `video-answer-teach-me-something` | `video-answer` | 3 | longform | 90 | T,R,S,D | `recruiting/l10-recorded-video` | You have thirty seconds to prepare and ninety seconds to answer. Teach me something you know well that I probably do not. | One idea, one example, a check that the listener followed, inside ninety seconds. |

### Session 2 (author A)

##### Session 2: statistics (15 items, file `statistics-2.json`)

| Id | Family | D | Kind | Pace | Roles | Draws on | Question | Answer |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `es-mle-two-coins-ratio` | `es-mle` | 3 | numeric | 100 | R,S,T | `estimation/l5-which-fits` | A coin is either fair or lands heads with chance 0.8. Five flips give four heads. The likelihood of 0.8 divided by the likelihood of fair, to 2 decimal places. | 2.62 (0.08192/0.03125 = 2.6214), tol 0.005. Slips: 0.38 (ratio upside down), 10.49 (treated all five as heads). |
| `shrinkage-mse-best-multiplier` | `shrinkage-mse` | 5 | numeric | 150 | R,S | `research-int/l6-bias-variance-aloud` | The true mean is 3 and the sample mean has variance 3. You report c times the sample mean. The c with the smallest mean squared error, as a decimal. | 0.75 (9/(9 + 3); the error falls from 3 to 2.25), tol 0.0005. Slips: 1 (kept it unbiased), 0.5 (used 3/(3 + 3)). |
| `es-intervals-poll-margin` | `es-intervals` | 2 | numeric | 75 | R,S,T | `estimation/l9-how-precise` | 240 of 400 people say yes. The 95% margin of error in percentage points, to 1 decimal place, using 1.96. | 4.8 (4.801), tol 0.04. Slips: 4.9 (used p = 0.5), 2.4 (left out 1.96). |
| `es-bayes-prior-and-sample` | `es-bayes` | 4 | numeric | 120 | R,S | `estimation/l12-updating-a-belief` | Your prior for a mean return is normal with mean 0% and sd 2%. A sample mean of 3% has standard error 1%. Posterior mean, in per cent to 1 decimal place. | 2.4 (3/1.25), tol 0.005. Slips: 1.5 (plain average), 0.6 (weights swapped). |
| `ht-setup-ten-paired-days` | `ht-setup` | 3 | numeric | 90 | R,S | `testing/l8-two-groups` | Over 10 days, strategy A minus strategy B has mean 1.2 and sd 1.5. Paired t statistic, to 2 decimal places. | 2.53 ($1.2/(1.5/\sqrt{10})$), tol 0.005. Slips: 0.80 (no root of n), 2.40 (used the root of 9). |
| `ht-pvalue-z-two-and-a-half` | `ht-pvalue` | 2 | choice | 45 | R,S,T | `testing/l3-p-value` | A test statistic is z = 2.5. Which is its two-sided p-value? | About 0.012 (0.01242). Distractors: 0.006 (one tail), 0.025, 0.05. |
| `ht-pvalue-bigger-sample` | `ht-pvalue` | 2 | numeric | 60 | R,S | `testing/l4-t-test` | A test gives z = 2.4. The same mean and sd in a sample 2.25 times the size gives what z? One decimal place. | 3.6 (2.4 × 1.5), tol 0.005. Slips: 5.4 (multiplied by 2.25), 1.6 (divided by 1.5). |
| `ht-errors-equal-error-cutoff` | `ht-errors` | 4 | numeric | 150 | R,S | `testing/l5-two-ways-wrong` | One observation is N(0, 1) under the null and N(3, 1) under the alternative. You reject above the cut-off that makes the two error rates equal. That error rate, to 4 decimal places. | 0.0668 (cut-off 1.5, $1 - \Phi(1.5)$), tol 0.0005. Slips: 0.1336 (added both errors), 0.0013 (cut-off at 3). |
| `rg-fit-point-at-the-mean` | `rg-fit` | 3 | choice | 90 | R,S | `regression/l2-slope-formula` | The points (1, 2), (2, 3) and (3, 7) give slope 2.5. You add the point (2, 10). What happens to the slope? | It stays 2.5: x = 2 is the mean of x, so only the intercept moves (from -1 to 0.5). Distractors: it rises; it falls; it depends on the residual. |
| `rg-multiple-useless-predictor` | `rg-multiple` | 3 | choice | 75 | R,S | `regression/l9-several-predictors` | You add a pure-noise predictor to a fitted regression. What can happen to $R^2$ and adjusted $R^2$? | $R^2$ cannot fall; adjusted $R^2$ can (it fell in 1,371 of 2,000 seeded trials, $R^2$ in none). Distractors: both must rise; both can fall; neither changes. |
| `collinear-features-inflation-factor` | `collinear-features` | 4 | numeric | 100 | R,S | `regression/l10-collinearity` | Two predictors correlate 0.9. Their variance inflation factor, to 2 decimal places. | 5.26 (1/0.19), tol 0.005. Slips: 10.00 (used 1 - r), 2.29 (gave the standard-error factor). |
| `ts-forecast-two-steps-ahead` | `ts-forecast` | 3 | numeric | 90 | R,S | `arma/l11-forecast-intervals` | An AR(1) series with mean 10 and coefficient 0.6 stands at 15 today. Two-step forecast, to 1 decimal place. | 11.8 (10 + 0.36 × 5), tol 0.005. Slips: 13.0 (one step), 5.4 (dropped the mean). |
| `ts-acf-two-day-variance-ratio` | `ts-acf` | 4 | numeric | 120 | R,S,T | `arma/l5-own-past` | Daily returns have lag-1 autocorrelation -0.15. The variance of a two-day return divided by twice the one-day variance, to 2 decimal places. | 0.85 (1 + $\rho_1$), tol 0.005. Slips: 1.00 (assumed independence), 1.15 (sign). |
| `measurement-error-noisy-regressor` | `measurement-error` | 4 | numeric | 120 | R,S | `research-int/l1-two-regressions` | The true slope is 1.2. x has variance 5 and is observed with independent noise of variance 3. The slope least squares reports, to 2 decimal places. | 0.75 (1.2 × 5/8), tol 0.005. Slips: 1.20 (no attenuation), 1.92 (scaled the wrong way). |
| `dl-clt-mean-of-hundred` | `dl-clt` | 2 | numeric | 75 | R,S,T | `limits-thm/l11-sums-look-normal` | 100 independent draws have mean 5 and sd 4. The chance the sample mean exceeds 5.8, to 4 decimal places. | 0.0228 (z = 2), tol 0.0005. Slips: 0.4207 (no root of n), 0.0455 (both tails). |

##### Session 2: finance (15 items, file `finance-2.json`)

| Id | Family | D | Kind | Pace | Roles | Draws on | Question | Answer |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `fi-interest-three-payments-pv` | `fi-interest` | 2 | numeric | 75 | T,S | `markets/l2-present-value` | £500 at the end of each of three years, discounted at 8%. Present value, in pounds to 2 decimal places. | 1,288.55, tol 0.005. Slips: 1,500.00 (not discounted), 1,190.75 (all discounted three years). |
| `fi-bonds-zero-coupon-yield` | `fi-bonds` | 2 | numeric | 75 | T,S | `markets/l6-yield` | A five-year zero-coupon bond costs 78.35 per 100. Annual yield, in per cent to 2 decimal places. | 5.00 ($1.05^5$ = 1.27628), tol 0.005. Slips: 5.53 (simple interest), 4.33 (21.65/5). |
| `fi-forwards-rich-forward` | `fi-forwards` | 4 | numeric | 120 | T,S | `markets/l10-cost-of-carry` | A share costs £200 and pays £4 at the year end. The rate is 3% simple. A one-year forward is quoted at £205. Riskless profit per share at delivery, in pounds. | 3 (fair is 206 - 4 = 202: sell the forward, borrow, buy the share). Slips: -1 (left the dividend out), 7 (subtracted the dividend twice). |
| `fi-forwards-futures-daily-loss` | `fi-forwards` | 2 | numeric | 60 | T,S | `markets/l11-margin` | You are long 10 index futures at £50 a point. The index moves from 4,000 to 3,960. Loss in pounds. | 20,000. Slips: 2,000 (one contract), 400 (points times contracts). |
| `op-strategies-covered-call-at-fifty` | `op-strategies` | 2 | numeric | 60 | T,S | `options/l8-with-the-stock` | Buy a share at £40 and sell the 45 call for £2. The share ends at £50. Profit in pounds. | 7 (5 + 2). Slips: 12 (no cap), 5 (no premium). |
| `op-strategies-butterfly-best-case` | `op-strategies` | 3 | numeric | 90 | T,S | `options/l7-butterfly` | Calls at 90, 100 and 110 cost £12.50, £6.00 and £2.50. Buy one, sell two, buy one. Largest profit at expiry, in pounds. | 7 (pays 10 at 100, costs 3). Slips: 10 (ignored the cost), 3 (gave the cost). |
| `op-parity-call-under-its-floor` | `op-parity` | 4 | numeric | 120 | T,S | `options/l10-bounds` | Share £100, zero rate, no dividends. A European call struck at 95 trades at £4.50. Smallest riskless profit from buying it and shorting the share, in pounds to 2 decimal places. | 0.50 (floor 5.00 less 4.50), tol 0.005. Slips: 5.00 (gave the floor), 4.50 (gave the price). |
| `gamma-pnl-break-even-move` | `gamma-pnl` | 4 | numeric | 120 | T,S | `trees/l18-gamma-and-hedging` | A delta-hedged long option has gamma 0.04 and loses £0.045 a day to theta. The daily share move that breaks even, in pounds to 1 decimal place. | 1.5 ($\sqrt{2 \times 0.045/0.04}$), tol 0.005. Slips: 1.1 (no factor of 2: 1.06), 1.125 (no square root; band 0.001). |
| `digital-option-at-the-money` | `digital-option` | 3 | numeric | 100 | S,T | `trees/l15-digitals` | Share and strike £50, vol 30%, three months, r = 0. A digital call paying £1, to 4 decimal places. | 0.4701 ($\Phi(-0.075)$; 4 million seeded draws give 0.4704), tol 0.0005. Slips: 0.5000 (ignored the drift term), 0.5299 (used $d_1$). |
| `tp-multistep-two-step-call` | `tp-multistep` | 4 | numeric | 150 | S,T,R | `trees/l5-two-steps` | Share 40; each step it is multiplied by 1.25 or 0.8; zero rate; two steps. European call struck at 40, to 2 decimal places. | 4.44 (q = 4/9, $(16/81) \times 22.5 = 40/9$), tol 0.005. Slips: 5.63 (q = 1/2), 10.00 (weighted 22.5 by q once). |
| `ms-book-weighted-mid` | `ms-book` | 3 | numeric | 75 | T,D | `micro/l7-where-is-the-price` | Bid 99.98 for 900 shares, ask 100.02 for 100 shares. The size-weighted mid, each price weighted by the size on the other side, to 3 decimal places. | 100.016, tol 0.0005. Slips: 99.984 (own-side sizes), 100.000 (plain mid). |
| `ms-costs-impact-four-times-size` | `ms-costs` | 4 | numeric | 90 | T,R | `micro/l6-impact` | Under a square-root impact model an order of 4% of daily volume costs 40 basis points. Cost of an order of 16% of daily volume, in basis points. | 80. Slips: 160 (linear), 40 (no change). |
| `ms-mm-spread-less-drift` | `ms-mm` | 2 | numeric | 60 | T | `micro/l11-adverse-selection` | You trade 1,000 shares and earn a half-spread of 1p on each. The price then moves 0.4p against you on average. Net result in pounds. | 6. Slips: 10 (ignored the move), 14 (added the move). |
| `gv-risk-two-desks` | `gv-risk` | 4 | numeric | 100 | T,S,R | `garch/l10-value-at-risk` | Two desks each have a one-day value at risk of £1m, with normal P&L and correlation 0.5. Combined value at risk, in £ millions to 3 decimal places. | 1.732 ($\sqrt{3}$), tol 0.0005. Slips: 2.000 (added), 1.414 (assumed no correlation). |
| `exotic-ranking-basket-or-calls` | `exotic-ranking` | 4 | choice | 100 | S,T | `trees/l17-which-is-cheaper` | A call on a half-and-half basket of two shares, or half a call on each share, all at the money. Which costs more? | The two separate calls, unless the shares move as one (seeded: 9.95 against 8.13 at correlation 0.3). Distractors: the basket call; always equal; it depends on the rate only. |

##### Session 2: coding (12 items, file `coding-2.json`)

| Id | Family | D | Kind | Pace | Roles | Draws on | Question | Answer |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `pf-idioms-argmax-last` | `pf-idioms` | 2 | code | 240 | D,R,S | `py-found/l13-one-at-a-time` | Write `argmax_last(xs)`: the index of the largest value, the last such index on a tie, `None` for an empty list. | `[3, 7, 7, 1]` gives 2; `[]` None; `[-2]` 0; `[1, 2, 3]` 2. Trap: `xs.index(max(xs))` gives 1. |
| `edge-case-list-second-largest` | `edge-case-list` | 2 | code | 240 | D,R,S | `coding-int/l16-edge-cases-first` | Write `second_largest(xs)`: the second largest distinct value, `None` when there are fewer than two distinct values. | `[5, 5, 3]` gives 3; `[4]` None; `[2, 2]` None; `[-1, -5, -3]` -3; `[]` None. Trap: `sorted(xs)[-2]` gives 5 and 2. |
| `ds-pointers-merge-ticks` | `ds-pointers` | 3 | code | 360 | D,R | `ds/l5-both-ends` | Write `merge_ticks(a, b)`: two lists of `(time, price)`, each sorted by time, into one sorted list. On equal times the ticks of `a` come first. | `[(1, 10.0), (4, 10.2)]` and `[(1, 9.9), (2, 10.1), (4, 10.3)]` give `[(1, 10.0), (1, 9.9), (2, 10.1), (4, 10.2), (4, 10.3)]`; `[]` and `[(3, 1.0)]` give `[(3, 1.0)]`. Trap: `sorted(a + b)` orders ties by price. |
| `ds-arrays-round-trips` | `ds-arrays` | 3 | code | 300 | D,T,S | `ds/l1-arrays-in-memory` | Write `round_trips(trades)`: apply signed trades from a flat position and count the returns to exactly zero from a non-zero position. | `[5, -5, 3, 2, -5, 0, -1, 1]` gives 3; `[0, 0]` 0; `[]` 0; `[2, -4, 2]` 1. Trap: counting every zero position gives 4 and 2. |
| `pf-collections-top-symbols` | `pf-collections` | 3 | code | 360 | D,R,S | `py-found/l5-lookup-by-name` | Write `top_symbols(trades, k)`: from `(symbol, quantity)` pairs, the k symbols with the largest total quantity, ties in alphabetical order. | `[("VOD", 300), ("BP", 500), ("VOD", 200), ("AZN", 500), ("HSBA", 100)]` with k = 2 gives `["AZN", "BP"]`; k = 3 gives `["AZN", "BP", "VOD"]`; `([], 2)` gives `[]`. Trap: sorting by total alone keeps input order on ties. |
| `gd-dp-walk-above-zero` | `gd-dp` | 5 | code | 480 | R,S,D | `graphs-dp/l16-grid-paths` | Write `nonneg_walk_counts(n)`: for walks of n steps of +1 or -1 from 0 that never go below 0, a dict of end position to number of walks (reachable ends only). | n = 0 gives `{0: 1}`; n = 3 `{1: 2, 3: 1}`; n = 4 `{0: 2, 2: 3, 4: 1}`; n = 10 has 42 at 0 and totals 252; n = 20 has 16,796 at 0. Trap: enumerating all $2^{20}$ paths is too slow for a 22-step test. |
| `pf-collections-first-of-ties` | `pf-collections` | 3 | choice | 60 | D,R | `py-found/l5-lookup-by-name` | Count the words of `"to be or not to be"` into `d` with `d[w] = d.get(w, 0) + 1`. What is `max(d, key=d.get)`? | `"to"` (the first inserted of the two words with count 2). Distractors: `"be"`, `"not"`, a `TypeError`. |
| `pf-functions-late-binding` | `pf-functions` | 4 | numeric | 75 | D,R | `py-found/l7-arguments` | `fs = [lambda x: x + i for i in range(3)]`. What is `sum(f(10) for f in fs)`? | 36 (each lambda reads i = 2). Slips: 33 (bound i early), 30 (ignored i). |
| `at-recursion-count-the-calls` | `at-recursion` | 3 | numeric | 90 | D,R,S | `algo-think/l8-cost-of-recursion` | `def f(n): return 1 if n <= 1 else f(n // 2) + f(n // 3)`. How many calls of `f` does `f(12)` make, counting the first? | 13 (the value returned is 7). Slips: 7 (gave the value), 12 (left the first call out). |
| `ds-hashing-list-membership` | `ds-hashing` | 2 | choice | 45 | D,R | `ds/l2-constant-time-lookup` | A loop over 20,000 ids runs `if x in seen` where `seen` is a list. Which change helps most? | Make `seen` a set (200 lookups took 0.015 s on the list and 0.000007 s on the set). Distractors: sort the list first; use a tuple; cache `len(seen)`. |
| `pf-idioms-spent-generator` | `pf-idioms` | 3 | choice | 60 | D,R | `py-found/l13-one-at-a-time` | `g = (x * x for x in range(4))`, then `a = sum(g)`, `b = sum(g)`, `print(a, b)`. What prints? | `14 0`. Distractors: `14 14`, `0 14`, a `StopIteration` error. |
| `copy-vs-move-vector-copy` | `copy-vs-move` | 3 | choice | 60 | D | `cpp/l19-moving-not-copying` | C++: `std::vector<int> v{1, 2, 3}; auto w = v; w.push_back(4);`. Python: `v = [1, 2, 3]; w = v; w.append(4)`. Sizes of v and w in each. | C++ 3 and 4 (a copy); Python 4 and 4 (one list). Distractors: 4 and 4 in both; 3 and 4 in both; C++ 4 and 4 with Python 3 and 4. |

##### Session 2: behavioural (8 items, file `behavioural-6.json`)

| Id | Family | D | Kind | Pace | Roles | Draws on | Prompt | The model must show |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `star-story-difficult-colleague` | `star-story` | 3 | longform | 120 | T,R,S,D | `recruiting/l11-stories-that-answer` | Tell me about a time you worked with someone you found difficult. | Their view put fairly, what you changed in your own conduct, the outcome. |
| `star-story-too-much-to-do` | `star-story` | 3 | longform | 120 | T,R,S,D | `recruiting/l11-stories-that-answer` | Describe a time you had too many things to do. How did you choose? | The list, the rule you ranked by, what you dropped and whom you told. |
| `star-story-unfair-criticism` | `star-story` | 4 | longform | 120 | T,R,S,D | `recruiting/l11-stories-that-answer` | Tell me about criticism you thought was unfair. | What was said, the part that was right, what you did with it. |
| `why-us-internship-before-more-study` | `why-us` | 3 | longform | 120 | T,R,S,D | `recruiting/l8-why-this-firm` | Why an internship now, rather than more study first? | What you can learn only on a desk, what study would add, a clear choice. |
| `reasoning-aloud-five-losses-running` | `reasoning-aloud` | 4 | longform | 120 | T,R,S | `recruiting/l12-reasoning-aloud` | In a trading game you have lost on five trades in a row. Talk me through what you check before the sixth. You have two minutes. | Luck against error: the chance of five losses at your edge, a check of each trade's price, a size rule. |
| `final-round-questions-for-us` | `final-round` | 3 | longform | 120 | T,R,S,D | `recruiting/l13-the-final-round` | It is the end of the day and I ask whether you have any questions for me. What do you ask, and why? | Two questions only this interviewer can answer, the reason for each, none answered on the website. |
| `after-rejection-applied-before` | `after-rejection` | 4 | longform | 120 | T,R,S,D | `recruiting/l15-after-a-rejection` | You applied to us last year and were turned down. What is different this time? | The gap named plainly, what you did about it with evidence, no blame. |
| `project-account-too-good-to-be-true` | `project-account` | 5 | longform | 150 | R,S,D | `recruiting/l7-projects-that-count` | Your result looks too good. Convince me it is not a bug. | Three checks in order (leakage, a baseline, held-out data), what each showed, what would still worry you. |

### Session 3 (author B)

##### Session 3: statistics (15 items, file `statistics-3.json`)

| Id | Family | D | Kind | Pace | Roles | Draws on | Question | Answer |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `es-estimators-pool-two-estimates` | `es-estimators` | 4 | numeric | 120 | R,S | `estimation/l3-right-target` | Two independent unbiased estimates have variances 4 and 12. Variance of the best weighted average. | 3 (weights 0.75 and 0.25), tol 0.005. Slips: 4 (equal weights), 8 (averaged the variances). |
| `estimator-bias-divide-by-n` | `estimator-bias` | 3 | numeric | 90 | R,S | `research-int/l3-estimators-on-the-spot` | Five draws come from a population with variance 10. Expected value of the variance estimate that divides by n. | 8 (4/5 × 10), tol 0.005. Slips: 10 (no bias), 12.5 (scaled the wrong way). |
| `es-intervals-wider-confidence` | `es-intervals` | 3 | numeric | 100 | R,S | `estimation/l10-catching-the-truth` | A 95% interval for a mean runs from 2 to 10 (multiplier 1.96). Upper end of the 99% interval (multiplier 2.576), to 2 decimal places. | 11.26 (6 + 4 × 2.576/1.96), tol 0.005. Slips: 10.62 (added the gap in multipliers), 13.14 (scaled the end point). |
| `es-bayes-arrivals-per-day` | `es-bayes` | 4 | numeric | 120 | R,S | `estimation/l12-updating-a-belief` | Your prior for a Poisson rate per day is gamma with shape 3 and rate 1. You count 12 events in 5 days. Posterior mean rate, to 1 decimal place. | 2.5 (15/6), tol 0.005. Slips: 2.4 (data only), 3.0 (prior only). |
| `ht-setup-die-sixty-rolls` | `ht-setup` | 3 | numeric | 100 | R,S,T | `testing/l18-counts-against-expectations` | 60 rolls give counts 5, 8, 9, 8, 10 and 20 for faces 1 to 6. Chi-squared statistic against a fair die, to 1 decimal place. | 13.4 (above 11.07, the 5% point on 5 degrees of freedom), tol 0.005. Slips: 134.0 (not divided by 10), 2.0 (absolute gaps). |
| `weak-signal-daily-edge` | `weak-signal` | 3 | numeric | 90 | R,S,T | `research-int/l10-weak-signals` | A signal earns a mean of 0.05% a day with daily sd 1% over 400 days. Its t statistic, to 1 decimal place. | 1.0 (0.05 × 20), tol 0.005. Slips: 0.1 (no root of n: 0.05, band 0.001 on 0.05), 0.8 (gave the annual Sharpe, 0.79). |
| `ht-errors-sample-for-power` | `ht-errors` | 5 | numeric | 180 | R,S | `testing/l6-power` | You want to detect a shift of 2 when the sd is 10, two-sided at 5% (1.96) with power 80% (0.8416). Smallest sample size. | 197 ($(2.8016 \times 5)^2 = 196.2$; power 0.7995 at 196, 0.8015 at 197). Slips: 97 (no power term), 155 (one-sided 1.645). |
| `ht-multiple-share-false` | `ht-multiple` | 3 | numeric | 90 | R,S | `testing/l9-twenty-tests` | 200 independent signals are each tested at 1%, and 14 pass. Estimated share of the 14 that are false, in per cent to 1 decimal place. | 14.3 (2 expected by luck, 2/14), tol 0.05. Slips: 1.0 (gave the level), 7.0 (14/200). |
| `rg-fit-correlation-from-sums` | `rg-fit` | 2 | numeric | 60 | R,S | `regression/l3-how-much-explained` | Total sum of squares 200, residual sum of squares 50, and the slope is negative. Correlation, to 3 decimal places. | -0.866 ($-\sqrt{0.75}$), tol 0.0005. Slips: 0.866 (sign), -0.750 (no root). |
| `rg-inference-new-observation` | `rg-inference` | 4 | numeric | 120 | R,S | `regression/l5-how-sure` | A line is fitted to 25 points with residual sd 2. At the mean of x, the standard error for predicting one new observation, to 2 decimal places. | 2.04 ($2\sqrt{1 + 1/25}$), tol 0.005. Slips: 0.40 (error of the fitted mean), 2.00 (ignored the fit's own error). |
| `rg-diagnostics-fanning-residuals` | `rg-diagnostics` | 3 | choice | 75 | R,S | `regression/l11-assumptions-fail` | Residuals fan out as x grows. What does that do to the least squares fit? | The slope is still unbiased; its usual standard error is wrong (seeded: mean slope 0.497 for a true 0.5, reported error 0.152 against 0.163). Distractors: the slope is biased up; nothing changes; $R^2$ becomes negative. |
| `rg-multiple-partial-out` | `rg-multiple` | 5 | choice | 150 | R,S | `regression/l9-several-predictors` | Which two-stage recipe gives the coefficient on $x_1$ from regressing y on $x_1$ and $x_2$? | Regress y on $x_2$ and $x_1$ on $x_2$, then residual on residual (seeded: 2.006 both ways, 1.51 from y on $x_1$ alone). Distractors: y on $x_1$ alone; residual of y on $x_2$ against raw $x_1$; the mean of the two simple slopes. |
| `ts-forecast-half-life` | `ts-forecast` | 3 | numeric | 90 | R,S,T | `arma/l12-half-life` | An AR(1) deviation decays with coefficient 0.75 a day. Half-life in days, to 1 decimal place. | 2.4 ($\ln 0.5/\ln 0.75 = 2.41$), tol 0.05. Slips: 2.0 (0.5/0.25), 4.0 (1/0.25). |
| `ts-acf-noise-band` | `ts-acf` | 3 | numeric | 75 | R,S | `arma/l6-pure-noise` | 400 observations of white noise. Half-width of the 95% band for a sample autocorrelation, to 3 decimal places. | 0.098 (1.96/20), tol 0.0005. Slips: 0.050 (left out 1.96), 0.005 (divided by n: 0.0049). |
| `equicorrelation-many-assets-vol` | `equicorrelation` | 4 | numeric | 150 | R,S,T | `research-int/l5-matrices-on-the-spot` | 25 assets each have vol 20%, every pair correlates 0.25, and weights are equal. Portfolio vol, in per cent to 1 decimal place. | 10.6 ($\sqrt{0.04(0.04 + 0.96 \times 0.25)}$ = 10.58), tol 0.05. Slips: 4.0 (independent), 10.0 (the many-asset limit). |

##### Session 3: finance (15 items, file `finance-3.json`)

| Id | Family | D | Kind | Pace | Roles | Draws on | Question | Answer |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `fi-interest-loan-payment` | `fi-interest` | 3 | numeric | 100 | S,T | `markets/l4-npv` | You borrow £10,000 at 10% and repay in three equal year-end payments. Each payment, in pounds to 2 decimal places. | 4,021.15 (the balance ends at 0), tol 0.005. Slips: 4,333.33 (simple interest), 3,333.33 (no interest). |
| `fi-bonds-three-year-coupon` | `fi-bonds` | 3 | numeric | 100 | S,T | `markets/l5-pricing-a-bond` | A three-year bond pays a 6% annual coupon and yields 4%. Price per 100, to 2 decimal places. | 105.55, tol 0.005. Slips: 100.00 (par), 118.00 (not discounted). |
| `fi-bonds-pound-per-basis-point` | `fi-bonds` | 3 | numeric | 90 | S,T | `markets/l6-yield` | You hold £10m face of a bond priced at 98 with modified duration 4.5. Pounds lost for a rise of one basis point. | 4,410, tol 0.5. Slips: 4,500 (ignored the price), 44,100 (a tenth of a per cent). |
| `fi-forwards-geared-loss` | `fi-forwards` | 3 | numeric | 90 | T,S | `markets/l13-leverage` | You invest £100,000 of your own and £100,000 borrowed at 4%. The asset falls 10% over the year. Return on your own money, in per cent. | -24, tol 0.005. Slips: -20 (no interest), -10 (no gearing). |
| `fi-forwards-currency-forward` | `fi-forwards` | 3 | numeric | 100 | S,T | `markets/l9-agreeing-today` | A pound costs 1.2500 dollars today. One-year simple rates are 5% in dollars and 3% in pounds. One-year forward in dollars per pound, to 4 decimal places. | 1.2743 (1.25 × 1.05/1.03), tol 0.00005. Slips: 1.2262 (rates swapped), 1.2750 (added the 2% gap). |
| `op-payoff-short-strangle-loss` | `op-payoff` | 3 | numeric | 75 | T,S | `options/l4-buying-or-writing` | You sell the 95 put for £2.20 and the 105 call for £1.80. The share ends at 88. Profit or loss in pounds. | -3 (4 - 7), tol 0.005. Slips: -7 (no premium), 4 (premium only). |
| `op-strategies-one-by-two-breakeven` | `op-strategies` | 4 | numeric | 120 | T,S | `options/l5-spreads` | Buy one 100 call at £5 and sell two 110 calls at £2.50 each. Upper break-even share price at expiry, in pounds. | 120 (zero cost; the payoff peaks at 10 and then falls one for one). Slips: 110 (gave the peak), 115 (halved the fall). |
| `op-parity-implied-forward` | `op-parity` | 3 | numeric | 100 | S,T | `options/l9-put-call-parity` | At strike 100 the call costs £7.20 and the put £5.10. The discount factor to expiry is 0.98. Implied forward price, to 2 decimal places. | 102.14 (100 + 2.10/0.98), tol 0.005. Slips: 102.10 (premium gap not compounded), 100.10 (gave the spot). |
| `op-greeks-vol-move-pnl` | `op-greeks` | 2 | numeric | 60 | T,S | `options/l12-how-price-responds` | You are long 50 contracts of 100 options. Each option has vega £0.12 per vol point. Implied vol moves from 18% to 21%. Profit in pounds. | 1,800. Slips: 18 (one contract of one option), 600 (one vol point). |
| `tp-bs-at-the-money-delta` | `tp-bs` | 4 | numeric | 100 | S,T | `trees/l10-black-scholes` | An at-the-money call, one year, vol 40%, r = 0. Its delta, to 2 decimal places. | 0.58 ($\Phi(0.2)$ = 0.5793), tol 0.005. Slips: 0.50 (ignored $\sigma^2T/2$), 0.42 (used $d_2$). |
| `tp-riskneutral-analyst-view` | `tp-riskneutral` | 3 | choice | 90 | S,T,R | `trees/l3-risk-neutral` | A share at 100 moves to 130 or 80, zero rate. An analyst is sure the up chance is 60%. Price of a put struck at 100? | £12 (q = 0.4, so 0.6 × 20). Distractors: £8 (the analyst's 0.4 × 20), £10 (even chances), £20 (the payoff). |
| `tp-multistep-monthly-up-factor` | `tp-multistep` | 3 | numeric | 75 | S,R | `trees/l6-calibrating` | Vol is 30% a year and the tree has monthly steps. The up factor $u = e^{\sigma\sqrt{\Delta t}}$, to 4 decimal places. | 1.0905, tol 0.00005. Slips: 1.0253 (no square root), 1.3499 (no time step). |
| `ms-book-who-gets-filled` | `ms-book` | 3 | numeric | 75 | T,D | `micro/l3-the-queue` | Resting bids: A 200 at 50.00 (09:00), B 300 at 50.00 (09:01), C 100 at 50.01 (09:02). A market sell of 450 arrives. How many shares does B buy? | 150 (C 100 first on price, then A 200 on time). Slips: 250 (time before price), 300 (filled B in full). |
| `ms-costs-shortfall-with-unfilled` | `ms-costs` | 4 | numeric | 120 | T,R | `micro/l5-crossing-the-spread` | You decide to buy 10,000 shares at 25.00. 6,000 fill at an average of 25.06, the rest never fills, the close is 25.20 and commission is £30. Implementation shortfall in pounds. | 1,190 (360 + 800 + 30). Slips: 390 (ignored the unfilled shares), 1,160 (no commission). |
| `tp-bs-vega-rule` | `tp-bs` | 4 | numeric | 100 | S,T | `trees/l10-black-scholes` | Share £100, three months, at the money, r = 0, vol 20%. Vega per vol point, in pounds to 2 decimal places. | 0.20 (0.4 × 100 × 0.5/100; exact 0.1992), tol 0.005. Slips: 0.40 (no time factor), 0.10 (used T, not its root). |

##### Session 3: coding (12 items, file `coding-3.json`)

| Id | Family | D | Kind | Pace | Roles | Draws on | Question | Answer |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `pf-idioms-trend-direction` | `pf-idioms` | 2 | code | 240 | D,R,S | `py-found/l13-one-at-a-time` | Write `trend(xs)`: 1 if strictly rising, -1 if strictly falling, otherwise 0. Fewer than two values give 0. | `[1, 2, 5]` gives 1; `[5, 2, 1]` -1; `[1, 1, 2]` 0; `[4]` 0; `[]` 0; `[1, 3, 2]` 0. Trap: comparing only the first and last values. |
| `at-sort-largest-gap` | `at-sort` | 2 | code | 240 | D,R,S | `algo-think/l11-sorting-by-hand` | Write `largest_gap(xs)`: the largest difference between neighbours once sorted; 0 for fewer than two values. | `[10, 3, 8, 20]` gives 10; `[5]` 0; `[]` 0; `[4, 4, 4]` 0; `[-3, 2]` 5. Trap: gaps in input order give 12. |
| `at-greedy-orders-to-fill` | `at-greedy` | 3 | code | 300 | D,T,S | `algo-think/l14-best-step-now` | Write `orders_to_fill(sizes, target)`: the fewest resting orders whose sizes sum to at least `target`; 0 when `target` is 0 or less; -1 when it cannot be done. | `([200, 50, 400, 100], 450)` gives 2; with 750 gives 4; with 751 gives -1; `([200, 50], 0)` 0; `([], 5)` -1. Trap: taking orders in input order gives 3. |
| `at-search-count-in-range` | `at-search` | 3 | code | 300 | D,R,S | `algo-think/l9-halving` | Write `count_in_range(xs, lo, hi)`: `xs` is sorted; count the values with lo ≤ x ≤ hi in $O(\log n)$ time. | `([1, 3, 3, 5, 8, 8, 9], 3, 8)` gives 5; with (4, 4) gives 0; with (9, 2) gives 0; `([], 0, 1)` 0; the even numbers below 2,000,000 with (5, 1000001) give 499,998. Trap: a negative count when hi is below lo. |
| `simulation-rules-clip-position` | `simulation-rules` | 4 | code | 420 | D,T,S | `coding-int/l8-simulating-the-rules` | Write `apply_orders(orders, limit)`: start flat; fill each signed order as far as keeps the absolute position at or under `limit`; return the list of signed fills. | `([6, 7, -20, 3], 10)` gives `[6, 4, -20, 3]`; `([5, 5, 5], 0)` gives `[0, 0, 0]`; `([], 3)` gives `[]`; `([-4, -4, 9, 9], 5)` gives `[-4, -1, 9, 1]`. Trap: rejecting a whole order that breaches gives `[6, 0, 0, 3]`. |
| `at-recursion-depth-weighted-sum` | `at-recursion` | 4 | code | 360 | D,R | `algo-think/l5-calls-itself` | Write `depth_sum(x)`: `x` is a list of ints and lists nested to any depth; add each int times its depth, the top list being depth 1. | `[1, [2, 3], [[4]]]` gives 23; `[]` 0; `[[], [[]]]` 0; `[5, [-1, [2, [3]]]]` 21. Trap: a plain sum gives 10 and 9. |
| `pf-idioms-stable-ties` | `pf-idioms` | 3 | choice | 60 | D,R | `py-found/l14-sorting-by-what-matters` | `sorted([("b", 2), ("a", 2), ("c", 1)], key=lambda t: t[1])`. In what order do the letters come out? | c, b, a (ties keep their input order). Distractors: c, a, b; a, b, c; b, a, c. |
| `at-search-stuck-loop` | `at-search` | 4 | choice | 100 | D,R,S | `algo-think/l9-halving` | `lo, hi = 0, len(xs)`, then `while lo < hi:` with `mid = (lo + hi) // 2`, `if xs[mid] < x: lo = mid`, `else: hi = mid`. What is wrong? | `lo = mid` never moves once `hi` is `lo + 1`, so searching 6 in `[1, 3, 5, 7]` never ends; it needs `lo = mid + 1`. Distractors: `hi = mid` skips an element; `mid` overflows; the loop needs `lo <= hi`. |
| `ds-stacks-push-pop-trace` | `ds-stacks` | 2 | numeric | 45 | D,R | `ds/l9-last-in-first-out` | On an empty stack: push 3, push 5, pop, push 2, push 7, pop, pop. Sum of the popped values. | 14 (5 + 7 + 2; 3 remains). Slips: 10 (popped from the front), 17 (all values). |
| `gd-dp-table-size` | `gd-dp` | 3 | numeric | 60 | D,R | `graphs-dp/l15-common-subsequence` | A longest-common-subsequence table for strings of length 6 and 9 has a row and a column for the empty prefix. How many cells? | 70 (7 × 10). Slips: 54 (no empty prefix), 15 (added the lengths). |
| `np-broadcast-column-plus-row` | `np-broadcast` | 3 | numeric | 75 | R,S | `numpy-pandas/l4-broadcasting` | `a = np.array([[1], [2], [3]])` and `b = np.array([10, 20, 30, 40])`. What is `(a + b).sum()`? | 324 (shape (3, 4): 4 × 6 + 3 × 100). Slips: 106 (added the two sums), 312 (counted a once per row: 12 + 300). |
| `virtual-dispatch-missing-virtual` | `virtual-dispatch` | 4 | choice | 75 | D | `cpp/l21-virtual-dispatch` | `struct B { char name() const { return 'B'; } };` and `struct D : B { char name() const { return 'D'; } };`. What does `name()` return through a `const B&` bound to a `D`? | 'B': without `virtual` the static type decides (with `virtual` it is 'D'). Distractors: 'D'; a compile error; undefined behaviour. |

##### Session 3: behavioural (8 items, file `behavioural-7.json`)

| Id | Family | D | Kind | Pace | Roles | Draws on | Prompt | The model must show |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `star-story-persuaded-with-data` | `star-story` | 3 | longform | 120 | T,R,S,D | `recruiting/l11-stories-that-answer` | Tell me about a time you changed someone's mind with data. | The claim, the one chart or number that did it, the decision that followed. |
| `star-story-chose-to-stop` | `star-story` | 4 | longform | 120 | T,R,S,D | `recruiting/l11-stories-that-answer` | Describe a time you chose to stop working on something. | The evidence for stopping, the cost already sunk, what the time went to instead. |
| `star-story-helped-at-a-cost` | `star-story` | 3 | longform | 120 | T,R,S,D | `recruiting/l11-stories-that-answer` | Tell me about a time you helped someone succeed at a cost to yourself. | What it cost in hours or marks, why you chose it, what happened to both of you. |
| `why-us-how-you-tested-the-fit` | `why-us` | 3 | longform | 120 | T,R,S,D | `recruiting/l8-why-this-firm` | What have you done to find out whether you would like this work? | Two things you tried, what each told you, one thing that surprised you. |
| `reasoning-aloud-are-you-sure` | `reasoning-aloud` | 4 | longform | 120 | T,R,S | `recruiting/l12-reasoning-aloud` | You give an answer you believe, and I say: are you sure? Show me what you do next, out loud. You have two minutes. | A second route to the answer, said aloud, then keep or change it with a reason. |
| `video-answer-competed-and-lost` | `video-answer` | 3 | longform | 120 | T,R,S,D | `recruiting/l10-recorded-video` | You have thirty seconds to prepare and two minutes to answer. Describe a time you competed and lost. | The contest, the margin, what you changed in practice afterwards. |
| `return-offer-quiet-in-meetings` | `return-offer` | 4 | longform | 120 | T,R,S,D | `recruiting/l14-offers-and-deadlines` | Halfway through an internship your manager says your work is fine but you are quiet in meetings. What do you do in the next two weeks? | Three dated actions, how you would check they worked, a follow-up with the manager. |
| `cv-lines-proficient-in-python` | `cv-lines` | 3 | longform | 120 | R,S,D | `recruiting/l6-one-page-cv` | Your CV says "proficient in Python". Tell me what that means, with evidence. | One piece of code by size and purpose, one thing you cannot yet do, no list of libraries. |

### Session 4 (author B)

##### Session 4: statistics (15 items, file `statistics-4.json`)

| Id | Family | D | Kind | Pace | Roles | Draws on | Question | Answer |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `es-estimators-error-of-the-vol` | `es-estimators` | 4 | numeric | 120 | R,S,T | `estimation/l2-estimates-vary` | 50 daily returns, taken as normal, have sample sd 1.2%. Large-sample standard error of that sd, in per cent to 2 decimal places. | 0.12 ($1.2/\sqrt{100}$; 200,000 seeded samples give 0.1205), tol 0.005. Slips: 0.17 (used the root of 50), 0.02 (divided by 50: 0.024). |
| `es-mle-best-precision-rate` | `es-mle` | 4 | numeric | 120 | R,S | `testing/l16-best-possible-precision` | 100 yes-or-no trials have true rate 0.2. Smallest standard deviation an unbiased estimator of the rate can have, to 2 decimal places. | 0.04 ($\sqrt{0.16/100}$; the information is 625), tol 0.0005. Slips: 0.0016 (gave the variance; band 0.0001), 0.40 (no division by n). |
| `es-intervals-two-desk-gap` | `es-intervals` | 3 | numeric | 100 | R,S,T | `estimation/l9-how-precise` | Two desks are watched for 50 days each. Mean daily P&L is £10.4k and £9.6k, each with sd £2k. Lower end of the 95% interval for the gap, in £ thousands to 3 decimal places, using 1.96. | 0.016 (0.8 - 1.96 × 0.4), tol 0.0005. Slips: 0.246 (error of one mean only), 1.584 (upper end). |
| `es-bayes-three-from-three` | `es-bayes` | 4 | numeric | 100 | R,S,T | `estimation/l12-updating-a-belief` | You hold a uniform prior on a success rate. The first three trials all succeed. Chance the fourth succeeds, as a decimal. | 0.8 (4/5), tol 0.0005. Slips: 1 (used 3/3), 0.75 (3/4). |
| `sm-nonpar-shuffled-labels` | `sm-nonpar` | 3 | numeric | 120 | R,S | `stat-models/l11-permutation-tests` | Group A is {8, 9} and group B is {1, 2, 3}. One-sided permutation p-value for the difference in means, as a decimal. | 0.1 (1 of the 10 ways to choose two values), tol 0.0005. Slips: 0.05 (counted ordered pairs), 0.2 (doubled it). |
| `ht-setup-one-or-two-sided` | `ht-setup` | 2 | choice | 60 | R,S,T | `testing/l2-measuring-surprise` | A test gives z = 1.8 and the level is 5%. Is it significant? | One-sided yes (p = 0.036), two-sided no (p = 0.072). Distractors: yes both ways; no both ways; two-sided yes, one-sided no. |
| `ht-multiple-better-of-two` | `ht-multiple` | 5 | numeric | 150 | R,S | `testing/l12-data-snooping` | Two independent strategies have no skill, so each t statistic is standard normal. Expected value of the larger one, to 3 decimal places. | 0.564 ($1/\sqrt{\pi}$; 2 million seeded pairs give 0.5641), tol 0.001. Slips: 0 (no selection), 0.798 (the mean absolute value). |
| `power-half-the-effect` | `power` | 2 | numeric | 60 | R,S | `research-int/l4-tests-in-words` | A test needs 150 observations for 80% power. The true effect turns out half as large. How many observations now? | 600. Slips: 300 (doubled), 212 (root two). |
| `rg-fit-next-year-return` | `rg-fit` | 3 | numeric | 90 | R,S,T | `regression/l2-slope-formula` | Fund returns in one year and the next correlate 0.5. Each year the mean is 6% and the sd 10%. A fund made 26%. Its expected return next year, in per cent. | 16 (6 + 0.5 × 20), tol 0.005. Slips: 26 (no pull to the mean), 13 (halved the return). |
| `rg-inference-overall-f` | `rg-inference` | 4 | numeric | 120 | R,S | `regression/l7-summary-table` | A regression with 3 predictors on 44 observations has $R^2 = 0.3$. Overall F statistic, to 2 decimal places. | 5.71 ((0.3/3)/(0.7/40)), tol 0.005. Slips: 5.86 (41 residual degrees), 0.43 (no degrees of freedom). |
| `rg-diagnostics-most-leverage` | `rg-diagnostics` | 2 | choice | 60 | R,S | `regression/l4-reading-residuals` | A line is fitted to x values 1, 2, 3, 4 and 20. Which point has the most leverage? | The point at x = 20 (hat value 0.984; the others are 0.30 or less). Distractors: x = 1; x = 3; all equal. |
| `rg-multiple-dummy-and-slope` | `rg-multiple` | 2 | numeric | 60 | R,S | `regression/l9-several-predictors` | The fit is $y = 3 + 2x + 4D + 1.5xD$, where D is 0 or 1. Fitted value at x = 2 with D = 1. | 14. Slips: 11 (left the interaction out), 7 (set D to 0). |
| `gv-models-ewma-after-a-shock` | `gv-models` | 3 | numeric | 100 | R,S,T | `garch/l5-recent-days-more` | An EWMA uses decay 0.94. Yesterday's vol was 1% and today's return is 3%. New vol, in per cent to 2 decimal places. | 1.22 ($\sqrt{0.94 \times 1 + 0.06 \times 9}$ = 1.2166), tol 0.005. Slips: 1.12 (averaged vols, not variances), 2.92 (weights swapped). |
| `gv-forecast-long-run-vol` | `gv-forecast` | 3 | numeric | 100 | R,S | `garch/l8-long-run-variance` | A GARCH(1,1) has $\omega = 0.0000045$, $\alpha = 0.10$ and $\beta = 0.88$. Long-run daily vol, in per cent to 1 decimal place. | 1.5 ($\sqrt{0.000225}$), tol 0.005. Slips: 23.8 (annualised), 0.02 (gave the variance times 100: 0.0225; band 0.001). |
| `co-spurious-two-walks` | `co-spurious` | 4 | choice | 120 | R,S | `coint/l1-two-walks` | You regress one random walk on another that is independent of it. What should you expect from the slope's t statistic? | It cannot be trusted: in 1,000 seeded pairs of 500 steps, 88.5% had a t statistic beyond 1.96 in size, against 5.1% after differencing. Distractors: near zero as usual; valid if $R^2$ is high; valid once n passes 100. |

##### Session 4: finance (15 items, file `finance-4.json`)

| Id | Family | D | Kind | Pace | Roles | Draws on | Question | Answer |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `fi-interest-one-year-forward-rate` | `fi-interest` | 3 | numeric | 90 | S,T | `markets/l3-comparing-rates` | The one-year rate is 3% and the two-year rate 4%, both compounded yearly. Rate for the second year, in per cent to 2 decimal places. | 5.01 ($1.04^2/1.03 - 1$), tol 0.004. Slips: 5.00 (2 × 4 - 3), 1.00 (the gap). |
| `fi-bonds-duration-and-convexity` | `fi-bonds` | 4 | numeric | 100 | S,T | `markets/l6-yield` | A bond has modified duration 8 and convexity 80. The yield rises 1 percentage point. Price change, in per cent to 1 decimal place. | -7.6 (-8 + 0.5 × 80 × 0.01), tol 0.005. Slips: -8.0 (duration only), -7.2 (no half). |
| `fi-equity-combine-two-sharpes` | `fi-equity` | 4 | numeric | 120 | T,R,S | `markets/l8-measuring-returns` | Two uncorrelated strategies have Sharpe ratios 0.6 and 0.8. Best Sharpe ratio from combining them, to 1 decimal place. | 1.0 ($\sqrt{0.36 + 0.64}$; a search over weights agrees), tol 0.005. Slips: 0.7 (average), 1.4 (sum). |
| `fi-forwards-implied-rate` | `fi-forwards` | 3 | numeric | 90 | S,T | `markets/l10-cost-of-carry` | A share costs £100 and pays no dividends. Its six-month forward is £102. Implied continuously compounded annual rate, in per cent to 2 decimal places. | 3.96 ($2\ln 1.02$), tol 0.004. Slips: 4.00 (simple), 4.04 (compounded twice a year). |
| `digital-option-from-two-calls` | `digital-option` | 4 | numeric | 100 | S,T | `trees/l15-digitals` | The 98 call costs £5.90 and the 102 call £3.70. Approximate price of a digital paying £1 above 100, to 2 decimal places. | 0.55 (2.20/4), tol 0.005. Slips: 2.20 (not divided by the width), 1.10 (divided by 2). |
| `op-strategies-protective-put-floor` | `op-strategies` | 2 | numeric | 60 | T,S | `options/l8-with-the-stock` | You hold a share at £120 and buy the 110 put for £3. Largest possible loss, in pounds. | 13. Slips: 10 (no premium), 7 (subtracted the premium). |
| `op-parity-exercise-before-dividend` | `op-parity` | 4 | choice | 120 | S,T | `options/l11-exercise-early` | A deep in-the-money American call, the day before the last dividend of £2.00. The same-strike put costs £0.50 and interest on the strike to expiry is £0.30. Exercise? | Exercise: the dividend of 2.00 beats 0.80, a gain of £1.20 (Black-Scholes example: share 60, strike 50, hold worth 8.80 against 10). Distractors: never exercise a call early; hold, since 0.80 of time value is lost; indifferent. |
| `gamma-pnl-hedger-trades` | `gamma-pnl` | 3 | choice | 75 | T,S | `trees/l18-gamma-and-hedging` | You are long a call and delta hedged. The share rises. What does the hedge need? | Sell shares (delta goes from 0.52 to 0.56 as the share goes from 100 to 101), and buy them back after a fall. Distractors: buy shares; do nothing; buy more calls. |
| `op-greeks-put-delta-from-call` | `op-greeks` | 2 | numeric | 45 | T,S | `options/l12-how-price-responds` | A European call has delta 0.62 and the share pays no dividends. Delta of the put at the same strike and expiry, to 2 decimal places. | -0.38, tol 0.005. Slips: 0.38 (sign), -0.62 (copied the call). |
| `tp-multistep-lookback-two-step` | `tp-multistep` | 5 | numeric | 180 | S,R | `trees/l5-two-steps` | Share 100; each step it is multiplied by 1.2 or 0.8; zero rate; two steps. An option pays the highest price on the path, the start included, less 100. Its price. | 16 ((44 + 20 + 0 + 0)/4 with q = 0.5), tol 0.005. Slips: 11 (priced the plain call), 32 (averaged the two paying paths only). |
| `ms-book-opening-auction` | `ms-book` | 4 | numeric | 120 | T,D | `micro/l12-venues` | Buy orders: 300 at 10.3, 200 at 10.2, 400 at 10.1. Sell orders: 250 at 10.0, 300 at 10.1, 300 at 10.2. The auction picks the price that trades the most shares. How many trade? | 550, at 10.1 (250 at 10.0, 500 at 10.2, 300 at 10.3). Slips: 500 (cleared at 10.2), 850 (all the sells). |
| `ms-orders-immediate-or-cancel` | `ms-orders` | 2 | numeric | 60 | T,D | `micro/l4-market-or-limit` | An immediate-or-cancel buy for 1,000 has limit 30.05. Offers: 400 at 30.03, 300 at 30.05, 600 at 30.06. How many shares fill? | 700. Slips: 1,000 (ignored the limit), 400 (stopped at the first level). |
| `ms-costs-participation-time` | `ms-costs` | 2 | numeric | 60 | T,R | `micro/l8-liquidity` | You must buy 60,000 shares at 10% of market volume. The market trades 150,000 shares an hour. Hours needed. | 4. Slips: 0.4 (no participation rate), 40 (applied the rate twice). |
| `option-estimate-straddle-implied-move` | `option-estimate` | 3 | numeric | 90 | T,S | `trees/l13-rules-of-thumb` | A £50 share reports results tomorrow. The at-the-money straddle expiring the day after costs £4.00. One-standard-deviation move implied, in per cent, taking the straddle as 0.8 standard deviations. | 10 (£5 on £50; exact 10.03), tol 0.05. Slips: 8 (straddle over the share), 6.4 (multiplied by 0.8). |
| `tp-bs-delta-and-finishing-chance` | `tp-bs` | 4 | choice | 90 | S,T | `trees/l10-black-scholes` | A call has delta 0.30. What is the risk-neutral chance it finishes in the money? | Below 30%: it is $\Phi(d_2)$, which is under $\Phi(d_1)$ (24.2% at vol 25%, six months, r = 0). Distractors: exactly 30%; above 30%; 70%. |

##### Session 4: coding (12 items, file `coding-4.json`)

| Id | Family | D | Kind | Pace | Roles | Draws on | Question | Answer |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `pf-idioms-count-above-mean` | `pf-idioms` | 2 | code | 240 | D,R,S | `py-found/l4-one-line-lists` | Write `above_mean(xs)`: how many values are strictly above the mean; 0 for an empty list. | `[1, 2, 3, 10]` gives 1; `[4, 4, 4]` 0; `[]` 0; `[-1, 1]` 1. Traps: "at or above" gives 3 for the second; no guard for the empty list. |
| `ds-arrays-local-peaks` | `ds-arrays` | 3 | code | 300 | D,R,S | `ds/l1-arrays-in-memory` | Write `local_peaks(xs)`: the indices, ends excluded, whose value is strictly greater than both neighbours. | `[1, 3, 2, 4, 4, 1, 5]` gives `[1]`; `[1, 2]` gives `[]`; `[2, 9, 1, 8, 3]` gives `[1, 3]`; `[]` gives `[]`. Trap: "at least" counts the plateau and gives `[1, 3, 4]`. |
| `ds-pointers-median-of-three` | `ds-pointers` | 3 | code | 300 | D,R,S | `ds/l6-sliding-window` | Write `median3(xs)`: the median of each window of three consecutive values; `[]` for fewer than three. | `[5, 1, 4, 2, 8]` gives `[4, 2, 4]`; `[1, 2]` gives `[]`; `[7, 7, 1]` gives `[7]`; `[]` gives `[]`. Trap: the middle element of each window gives `[1, 4, 2]`. |
| `simulation-rules-settle-day` | `simulation-rules` | 4 | code | 420 | D,T,S | `coding-int/l8-simulating-the-rules` | Write `settle_day(trade_day, lag, holidays)`: days are whole numbers, day 0 is a Monday, a day whose remainder on division by 7 is 5 or 6 is a weekend, `holidays` is a set. Return the day `lag` business days after `trade_day`. | `(3, 2, set())` gives 7; `(4, 2, {7})` 9; `(0, 0, set())` 0; `(4, 1, {7, 8})` 9; `(2, 5, {4})` 10. Trap: `trade_day + lag` then skipping forward gives 8 for the first. |
| `at-search-smallest-n` | `at-search` | 3 | code | 360 | D,R,S | `algo-think/l10-search-the-answer` | Write `smallest_n(target)`: the smallest n of 0 or more with n(n + 1)/2 at least `target`. `target` may be as large as $10^{18}$. | 0 gives 0; 1 gives 1; 7 gives 4; 10 gives 4; 11 gives 5; $10^{18}$ gives 1,414,213,562. Traps: a counting loop times out on the last; a float square root is off by one near $10^{18}$. |
| `gd-dp-dice-total-ways` | `gd-dp` | 4 | code | 420 | R,S,T | `graphs-dp/l13-climbing-stairs` | Write `dice_ways(n, total)`: the number of ordered ways n six-sided dice can sum to `total`. | `(2, 7)` gives 6; `(3, 10)` 27; `(10, 35)` 4,395,456; `(0, 0)` 1; `(2, 13)` 0; `(0, 3)` 0. Trap: plain recursion without a table is too slow for a 40-dice test. |
| `pf-classes-shared-class-list` | `pf-classes` | 4 | numeric | 75 | D,R | `py-found/l12-data-with-behaviour` | `class Book:` has `levels = []` in the class body and `def add(self, x): self.levels.append(x)`. After `p, q = Book(), Book()`, `p.add(1)` and `q.add(2)`, what is `len(p.levels)`? | 2 (one list shared by the class). Slips: 1 (a list per object), 0. |
| `ds-trees-heap-trace` | `ds-trees` | 3 | numeric | 90 | D,R | `ds/l17-always-the-smallest` | `h = [5, 1, 8, 3, 2]`, `heapify(h)`, `a = heappop(h)`, `b = heappushpop(h, 4)`. What is `a + b + h[0]`? | 6 (1 + 2 + 3). Slips: 7 (took b as 4, the pushed value), 5 (took `h[0]` as 2). |
| `bit-lowest-and-count` | `bit-lowest` | 3 | numeric | 75 | D | `coding-int/l5-bit-tricks` | With `x = 44`, what is `(x & -x) + bin(x).count("1")`? | 7 (4 + 3; 44 is 101100 in binary). Slips: 5 (used the bit's index, 2), 35 (took the highest bit, 32). |
| `edge-case-list-median-test` | `edge-case-list` | 3 | choice | 75 | D,R,S | `coding-int/l16-edge-cases-first` | `def median(xs): s = sorted(xs); return s[len(s) // 2]`. Which input returns a wrong value, rather than raising? | `[4, 1, 3, 2]` (returns 3; the median is 2.5). Distractors: `[]` (raises `IndexError`), `[5]` (5 is right), `[3, 1, 2]` (2 is right). |
| `gd-traversal-depth-first-order` | `gd-traversal` | 3 | choice | 75 | D,R | `graphs-dp/l3-going-deep` | Edges: A to B and C; B to D; C to D and E; D to F; E to F. A recursive depth-first search from A takes neighbours in the order listed. Visit order? | A, B, D, F, C, E. Distractors: A, B, C, D, E, F (breadth first); A, B, D, C, E, F; A, C, E, F, D, B. |
| `defined-vs-undefined-wraparound` | `defined-vs-undefined` | 4 | choice | 75 | D | `cpp/l22-undefined-behaviour` | C++ with 32-bit ints: `unsigned u = 0;` then `u - 1`, and `int i = INT_MAX;` then `i + 1`. Which is well defined? | Only the unsigned one, which is 4,294,967,295; the signed sum is undefined behaviour (the compiler rejects it in a constant expression). Distractors: both wrap; neither is defined; only the signed one. |

##### Session 4: behavioural (8 items, file `behavioural-8.json`)

| Id | Family | D | Kind | Pace | Roles | Draws on | Prompt | The model must show |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| `star-story-tempted-to-cut-a-corner` | `star-story` | 4 | longform | 120 | T,R,S,D | `recruiting/l11-stories-that-answer` | Tell me about a time you were tempted to cut a corner. | The shortcut, who would have been affected, what you did, what it cost you. |
| `star-story-dull-task-done-well` | `star-story` | 3 | longform | 120 | T,R,S,D | `recruiting/l11-stories-that-answer` | Describe the most boring task you have had to do well. | Why it mattered, how you kept the error rate down, a count of what you got through. |
| `star-story-asked-for-help-late` | `star-story` | 3 | longform | 120 | T,R,S,D | `recruiting/l11-stories-that-answer` | Tell me about a time you asked for help later than you should have. | The hours lost, the sign you ignored, the rule you use now. |
| `why-us-what-worries-you` | `why-us` | 4 | longform | 120 | T,R,S,D | `recruiting/l8-why-this-firm` | What worries you about this job? | One real worry tied to the work, the evidence for it, how you would find out early. |
| `reasoning-aloud-correct-me-politely` | `reasoning-aloud` | 3 | longform | 120 | T,R,S | `recruiting/l12-reasoning-aloud` | I say: a fair coin has landed heads five times, so a tail is due. Put me right without being rude. You have two minutes. | Agreement on what is true, the independence point with the number 1/2, a check the listener can do. |
| `final-round-earlier-answer-was-wrong` | `final-round` | 4 | longform | 120 | T,R,S,D | `recruiting/l13-the-final-round` | In your fourth interview of the day you realise an answer you gave in the second was wrong. What do you do? | Finish the current question, correct the answer briefly at a natural point, no long apology. |
| `after-rejection-no-feedback` | `after-rejection` | 3 | longform | 120 | T,R,S,D | `recruiting/l15-after-a-rejection` | You are turned down after a final round and given no feedback. How do you work out what to change? | A written recall of each round the same day, the weakest round by evidence, one change and a date. |
| `project-account-one-number` | `project-account` | 5 | longform | 150 | R,S,D | `recruiting/l7-projects-that-count` | Give me the one number that sums up your project, and tell me how it could mislead. | The number with its unit and baseline, two ways it flatters, what you would show beside it. |

## 6. Per-session notes

- **Engine first.** B2-E1 to B2-E5 land before a session writes its `coding-n.json`. A session may write its other three files while waiting, and reports them as a partial hand-in.
- **Session 1** sets the house style for the three new groups: the first `code` items, the first reasoning-about-code items and the `question` line of rule 11. State the `how` wording and the test count you settled on, so sessions 2 to 4 copy it. `power-one-sided-shift` and `multiple-testing-how-many-tests` both draw on `research-int/l4`; keep their settings apart (a mean shift, a list of signals).
- **Session 2** is the heaviest on difficulty 4 in finance (seven items). `gd-dp-walk-above-zero` is the hardest `code` item of the bank: its hidden tests include n = 22, which needs the table method.
- **Session 3** carries the two difficulty 5 statistics items; `rg-multiple-partial-out` is a choice whose options are recipes, so keep the four the same length. `np-broadcast-column-plus-row` is reasoning only: nothing imports NumPy in the deck.
- **Session 4** carries the three choice items with simulated figures (`co-spurious-two-walks`, and in session 3 `rg-diagnostics-fanning-residuals`; in session 2 `rg-multiple-useless-predictor`). The printed figures are from the planner's seeds. Your script fixes its own seed and prints its own figures; write those into the item, and state only the conclusion in the option text.
- **Changed by the planner for freshness** (keep the changes): `option-estimate-short-dated-call` (the first numbers matched a `trees` item exactly), `digital-option-at-the-money` (vol and expiry changed from a `trees` item), `correlation-bounds-highest-third` (the pair 0.6 and 0.8 is in `research-int`), `power-one-sided-shift` (the shift of 2.5 standard errors is in `research-int`), `multiple-testing-how-many-tests` (40 tests and t = 3 are in `research-int`), `shrinkage-mse-best-multiplier`, `measurement-error-noisy-regressor`, `two-regressions-two-slopes` (slopes 1.6 and 0.4 are in `research-int`). Code tasks avoid the 270 drill names read on 11 Nov; five first ideas were dropped because a drill does the same job (a winning streak, histogram bins, time under water, sessions by gap, splitting pence).
- **C++ reading items** are checked in the number script by compiling a file of `static_assert` lines with `g++ -std=c++20 -fsyntax-only` (or the local clang); the script skips them with a printed warning, not a pass, when no compiler is present.

## 7. Acceptance (per session)

From `app/` unless a path is absolute. `<pkgs>` is the scratchpad `pkgs` folder named in `docs/LEVEL-BRIEF.md`. A session is handed to the second reader only when all eight steps pass.

1. **Validator.** `node tools/validate.mjs 2>&1 | tail -5` reports 0 errors, and no warning names one of your four files (in particular `[answer-form]`, `[key-length]`, `[tight-band]`, `[wrong-band]`, `[wide-wrong-band]`, `[shown-arithmetic]`, `[bank-family]`). It rewrites `content/manifest.json`; that is expected.
2. **Numbers.** `python3 docs/reports/bank-2-s<n>-numbers.py` is committed and exits 0. It computes every key, every `wrong` value, every figure in feedback and explanations, and every hidden-test `expect` by two routes with `assert`; reads the four files through `numbers_lib.Bank` (B2-E4) with `expect` on each stored value and `check_wrongs()` on each file; runs each `solution` against its tests, shows each starter fails and each named trap fails a test; and executes the lines of every reasoning-about-code item.
3. **Playthrough.** `node tools/playthrough.mjs --bank statistics-<n> --bank finance-<n> --bank coding-<n> --bank behavioural-<n+4> --local-cdn <pkgs> 2>&1 | tail -30` is green (50 of 50), then again with `--mobile` (B2-E3). Then `node tools/playthrough.mjs --routes-only --local-cdn <pkgs>` is green with and without `--mobile` (B2-E2).
4. **Freshness.** `node tools/fresh-check.mjs --bank <file id>` exits 0 for each of the four files. Run it again with `--min-run 10`, read every hit, and list each in the report with "rewritten" or the reason it is stock phrasing.
5. **Voice scan.** `VOICE_BASE=/home/user/zero-to-quant/app/content/bank/ python3 docs/reviews/voice-scan.py 35 --summary` reports explanations over three sentences 0 and sentences over 35 words 0. It scans the whole folder: fix only your own files and report a failure in another session's file.
6. **Wrong answers route.** With a scratch script (never in the repo) that deals your files and calls `ZQ.test.answerWrong()`, confirm that each `wrong` id shows its `byKey` line and each distractor its `why`. Say how many were checked.
7. **Counts.** The report states items per file, per family, per difficulty and per kind, and they match sections 2, 3 and 5. A difference needs a reason.
8. **Report** at `docs/reports/bank-2-s<n>.md`: files and counts, the output tail of steps 1 to 5, each number with its two routes (or a pointer to the script line), changes from section 5 and why, any item swapped, the `[verify]` item's resolution, and open questions. Engine or schema limits go to `docs/BACKLOG-INBOX.md` under `Raised later (bank part 2 session n):`, one bullet each with the wanted behaviour. Hand back at most six lines.

Do not edit: engine files (`app/js/`, `app/tools/`, `app/css/`, `app/index.html`), any `course.json`, `content/courses/`, exams, `content/prep.json`, `docs/reviews/voice-scan.py`, part 1 bank files, another session's files, or this brief. Commit per file group on the session's branch with the session number in the message.

## 8. Order and hand-off

1. Engine pass for B2-E1 to B2-E5 (B2-E6 may ride with it).
2. Sessions 1 and 3 in parallel (authors A and B), then sessions 2 and 4. Session 1's report fixes the `how` wording and the `question` line before sessions 2 and 4 start.
3. One second read of all 16 files (`docs/reviews/review-bank-2.md`, pattern `docs/reviews/review-bank-1.md`): run the four number scripts, re-derive 30 answers afresh, read all 32 rubrics, check family counts against section 3, key lengths, pace against stated times, and that no part 1 template recurs. One fix pass.
4. Orchestrator: decide on mock draws from the new prefixes, tick `PLAN.md` "Bank part 2 (200 items)", add a `PROGRESS.md` line, and update the bank sentence in `AUTHORING.md` section 5 (36 files, 400 items).

## Carried from part 1 (its two "Changes after" sections and its reviews)

| What went wrong in part 1 | Where this brief designs it out |
| --- | --- |
| Family names drifted from course tags (`coupon-collector`, `derangements`, `hats-mod-k`, `weighing-scale`) | Section 3 lists only skill ids and tags read from the course files today; B2-E5 makes the validator check them |
| 16 of session 1's 50 items matched course or exam items; 9 duplicates in sessions 2 to 4 | Section 5 fixes the numbers after a read of the tagged course items and the drill names; rules 4 and 5; acceptance step 4 |
| Two "why" lines described the wrong option; one percentage in a "why" was off | Rule 3 extends the two-route check to every figure in feedback; `numbers_lib.Bank.check_wrongs` |
| "Tightest interval" was true only among centred intervals | Rule 17 |
| A question gave no decimal places, so 0.33 failed | Rules 6 and 7; `[answer-form]` and `[tight-band]` must be silent |
| The key was the longest option in 21 of 53 choices | Rule 10; `[key-length]` |
| `pace` 180 on a "two minutes" prompt; rubric lines that cannot be ticked from text | Rule 11 |
| Every behavioural row read the same in the results list | Rule 11 (`question` line) and B2-E6 |
| Explanations ended "A seeded simulation agrees" | Rule 14 |
| 67 "why" lines opened with the option's flaw | Rule 9 |
| "percent" in learner text | Rule 14 |
| Ids kept numbers that a fix pass later changed | Section 2: ids name the setting |
| `--mobile` did nothing for `--bank`; no way to play one file | B2-E3; `--bank` exists since ENGINE-BACKLOG 462 |

## Changes after session 1

(empty: the orchestrator records here what session 1 changed)

## Changes after sessions 2 to 4

(empty)
