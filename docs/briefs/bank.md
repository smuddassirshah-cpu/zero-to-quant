# Brief: interview question bank, part 1 (200 items)

Part 1 of the interview question bank (`docs/briefs/interview-plan.md`, engine item E7, built in engine pass B, `docs/reports/engine-pass-b.md`). It writes 200 items into `app/content/bank/`, in four authoring sessions of 50 items each. One content agent writes one session from its section below. Session 1 is fully specified and runs first. Sessions 2 to 4 are specified to the same level and may run in parallel, because each writes only its own five files.

The plan sizes the whole bank at about 400 items: part 1 (this brief) is 200 and part 2 (statistics, finance, coding and more behavioural) is 200 later. The plan also asks for about 30 behavioural questions as spoken `longform` items with rubrics. Part 1 holds all 30, so part 2 adds no behavioural family.

## 1. What the engine does (checked in `AUTHORING.md` section 5, `validate.mjs` `checkBank` and `select.js`, not taken from the plan)

- A bank file is `app/content/bank/<name>.json`: `{ "id": "<name>", "name", "description" (optional), "items": [...] }`. The validator needs `id` to equal the kebab-case file name, at least one item, and warns above 200 items. The manifest lists every `bank/*.json`.
- A bank item is an ordinary item (`id`, `difficulty` 1 to 5, `question`, `widget`, `feedback`, `explain`, optional `prose`, `canvas`, `skills`) plus `tags` (list, family first, at most four), `role` (list from `trader`, `research`, `developer`, `strats`), `style` (one of `mental-maths`, `probability`, `brainteaser`, `market-making`, `statistics`, `finance`, `coding`, `behavioural`), `source` (one plain line, at most 120 characters, shown under the question in the results), optional `requires` (list of `course/lesson-id`) and optional `pace` (seconds). A `code` widget is an error. `longform` is allowed.
- The deck (card on Review, route `#bank`) deals 8 items: due ones first, then new ones, one family at a time (the first tag), so two neighbours rarely share a family. Each item has its own Leitner box (1, 3, 7, 30 days). A bank miss never joins the redo queue. Items are keyed by the uid `bank/<file id>/<item id>`: **never rename an item id or a file id once written**, because the learner's schedule keys on it.
- The deck also draws every tagged quiz, review and homework item of a finished lesson, under its own uid and the same family space. So a bank item and a course item with the same first tag are dealt as one family. That is the reason families reuse course tag names (section 3).
- The deck shows "n s of p s pace" per item, an average and the slowest families, and counts items over `pace`. Marks, XP and the schedule never read time.
- An item with `requires` is drawn only when every named lesson is finished. The Review card says how many are still locked.
- Not built, so do not design for it: spoken mode with timers and recording (E10; a `longform` is typed, then self-marked against its rubric), `timed` on a deck, a bank draw for exam papers (E3), SM-2 ease, a bank view by family (E18).
- Engine limits found while writing this brief (each is also in the hand-back):
  1. `tools/playthrough.mjs --routes-only` makes the **second** deck item "take" 200 s and expects exactly one item over pace. An item with `pace` of 200 or more, drawn second, makes it fail ("Over pace: 1 of"). So **every `pace` in part 1 is at most 180**.
  2. The same check expects the Review card to say "N new", where N is the number of bank items without `requires` (across every bank file), and the deck to draw exactly that many. If every item carried `requires`, the card would be hidden on a fresh save and the check would time out. So `requires` is set only on difficulty 4 and 5 items (section 4, rule 9).
  3. There is no flag to play one bank file. `--routes-only` plays one random deck of 8. Section 7 says how the author covers the rest.
  4. The deck takes an item's `tags[0]` as its family. A misspelt family is a valid kebab word and the validator cannot catch it: copy tags from section 3 exactly.

## 2. File layout

One file per family group per session, 20 files in all, named `<group>-<session>.json`, id equal to the name. This is what the engine allows (the file name is never read for the family, so any split works) and it is the safest for four sessions: no two agents ever edit one file, and each file stays far below the 200 cap.

| Group | Files | Items per file | `style` for the group's items | `name` of the file |
| --- | --- | --- | --- | --- |
| probability | `probability-1.json` to `probability-4.json` | 15, 15, 14, 12 | `probability` | "Interview probability, set n" |
| brainteasers | `brainteasers-1.json` to `-4.json` | 10 each | `brainteaser` | "Interview brainteasers, set n" |
| mental | `mental-1.json` to `-4.json` | 10 each | `mental-maths` | "Interview mental maths, set n" |
| market-making | `market-making-1.json` to `-4.json` | 10, 8, 8, 8 | `market-making` | "Interview market making, set n" |
| behavioural | `behavioural-1.json` to `-4.json` | 5, 7, 8, 10 | `behavioural` | "Interview behavioural questions, set n" |

Give each file a one-sentence `description` that says which kinds of question it holds and that each item keeps its own schedule. Item ids are kebab-case, `<family>-<two or three words>` (for example `urns-reds-before-blue`), unique across the whole bank, not only within the file, so a later merge never collides. The "Ref" column in the tables below (for example `1p03`) is a working label for the report, never an id.

Item counts, by session and group:

| Session | probability | brainteasers | mental | market-making | behavioural | Total |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 15 | 10 | 10 | 10 | 5 | 50 |
| 2 | 15 | 10 | 10 | 8 | 7 | 50 |
| 3 | 14 | 10 | 10 | 8 | 8 | 50 |
| 4 | 12 | 10 | 10 | 8 | 10 | 50 |
| All | 56 | 40 | 40 | 34 | 30 | 200 |

Difficulty and kind, by session:

| Session | D2 | D3 | D4 | D5 | numeric | choice | expression | longform |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 8 | 20 | 17 | 5 | 31 | 14 | 0 | 5 |
| 2 | 10 | 18 | 16 | 6 | 28 | 14 | 1 | 7 |
| 3 | 9 | 21 | 14 | 6 | 29 | 13 | 0 | 8 |
| 4 | 6 | 23 | 13 | 8 | 28 | 12 | 0 | 10 |
| All | 33 | 82 | 60 | 25 | 116 | 53 | 1 | 30 |

Difficulty is the plan's reported level (the bank is interview practice, so there is no difficulty 1 and difficulty 2 is the warm-up). `expression` is rare on purpose: bank answers are numbers or choices, which is how an interviewer hears them.

## 3. Families and the tags they use

A **group** is the file prefix. A **family** is an item's first tag, and it reuses the tag name that course lessons already put on their drill, quiz, review and homework items, so the deck mixes bank and course items under one family. The script `scratchpad/brief-bank/tags.py` read every `tags` value in the courses `puzzles`, `brainteasers`, `mental-pressure`, `mm-games`, `game-theory` and `recruiting`; its output is `scratchpad/brief-bank/tags-output.txt` (full path `/tmp/claude-0/-home-user-zero-to-quant/7da692d4-a4e3-50a3-8a6e-3e8b2ccfe9ff/scratchpad/brief-bank/tags-output.txt`). Counts below are course items (lesson, review and homework) already carrying the tag as their first tag.

Which course tags map to which bank group:

- **probability**: the `puzzles` tags (`ants`, `bayes-in-a-minute`, `broken-stick`, `buffon`, `cards-and-colours`, `duels`, `kelly`, `largest-of-several`, `meeting`, `ruin-in-interviews`, `urns`, `when-to-stop`, `who-wins`, and the rest in the table), plus `dice-ev` (carried by `mm-games` items). Five families have no course tag yet because `puzzles` l1 to l5 were tagged by lesson only in part: `coupon-collector`, `at-least-one`, `derangements`, `waiting-for-hh`, `indicator-tricks`. They are bank-only families here; the bank sample already uses the first three. Propose tagging the matching `puzzles` items in the report, never edit them.
- **brainteasers**: the `brainteasers` tags, unchanged (all 40 used are existing tags). `backward-induction` and `common-knowledge` are shared with `game-theory`, which is fine.
- **mental**: the `mental-pressure` tags (`percent-chain`, `fraction-compare`, `estimate-product`, `sequences`, `sqrt-newton`, `negative-marking`, `ranking`, `battery`, `probability`, and so on) plus `mental-arithmetic`, the family the engine gives generated arithmetic items. Use `mental-arithmetic` for plain products and quotients.
- **market-making**: the `mm-games` tags (`card-fair`, `fermi`, `intervals`, `skew`, `informed-loss`, `hedge-ratio`, `arbitrage`, `options-game`, and so on) plus `dice-ev`, which is shared with probability.
- **behavioural**: the `recruiting` tags: `star-story`, `why-us`, `reasoning-aloud`, `project-account`, `video-answer`, `after-rejection`, `final-round`, `cv-lines`. The plan's six themes (why trading, a failure, a decision with incomplete information, teamwork, a disagreement, a project you owned) map onto these families, as the tables show. `game-theory` contributes no part 1 family (its tags belong to bank part 2 and the track it serves).


**probability** (file prefix `probability-`)

| Family tag | Items by session (1/2/3/4) | Total | Course items already carrying this tag |
| --- | --- | --- | --- |
| `ants` | 1/0/0/1 | 2 | puzzles 6 |
| `at-least-one` | 1/0/1/0 | 2 | none (bank-only family) |
| `bayes-in-a-minute` | 1/0/1/1 | 3 | puzzles 9 |
| `betting-on-sequences` | 0/0/1/0 | 1 | puzzles 9 |
| `broken-stick` | 1/0/0/1 | 2 | puzzles 9 |
| `buffon` | 0/0/1/0 | 1 | puzzles 6 |
| `cards-and-colours` | 1/1/0/0 | 2 | puzzles 7 |
| `coupon-collector` | 2/0/1/1 | 4 | none (bank-only family) |
| `derangements` | 1/0/1/0 | 2 | none (bank-only family) |
| `dice-ev` | 2/2/1/1 | 6 | mm-games 3 |
| `doubling-up` | 0/0/1/0 | 1 | puzzles 8 |
| `duels` | 0/1/0/1 | 2 | puzzles 10 |
| `estimating-n` | 0/1/0/1 | 2 | puzzles 9 |
| `exceeding-one` | 0/1/0/0 | 1 | puzzles 6 |
| `expected-distance` | 0/0/1/0 | 1 | puzzles 5 |
| `fair-from-biased` | 0/1/0/0 | 1 | puzzles 8 |
| `given-the-total` | 0/1/0/1 | 2 | puzzles 10 |
| `indicator-tricks` | 0/1/0/1 | 2 | none (bank-only family) |
| `kelly` | 0/0/1/1 | 2 | puzzles 10, mm-games 3, game-theory 5 |
| `largest-of-several` | 1/0/0/1 | 2 | puzzles 5 |
| `meeting` | 0/1/0/0 | 1 | puzzles 7 |
| `random-chords` | 0/0/1/0 | 1 | puzzles 8 |
| `ruin-in-interviews` | 1/0/1/0 | 2 | puzzles 8 |
| `semicircle` | 0/1/0/0 | 1 | puzzles 8 |
| `urns` | 1/1/0/0 | 2 | puzzles 7 |
| `waiting-for-hh` | 2/0/1/0 | 3 | none (bank-only family) |
| `when-to-hedge` | 0/0/1/0 | 1 | puzzles 10 |
| `when-to-stop` | 0/2/0/0 | 2 | puzzles 1 |
| `who-wins` | 0/1/0/1 | 2 | puzzles 11 |

**brainteasers** (file prefix `brainteasers-`)

| Family tag | Items by session (1/2/3/4) | Total | Course items already carrying this tag |
| --- | --- | --- | --- |
| `average-speed` | 0/1/0/0 | 1 | brainteasers 3 |
| `backward-induction` | 0/0/1/0 | 1 | brainteasers 3, game-theory 4 |
| `bridge-crossing` | 1/0/0/0 | 1 | brainteasers 8 |
| `burning-ropes` | 1/0/0/0 | 1 | brainteasers 3 |
| `clock-angle` | 1/0/0/0 | 1 | brainteasers 7 |
| `colouring-chequer` | 0/1/0/0 | 1 | brainteasers 6 |
| `common-knowledge` | 0/1/0/1 | 2 | brainteasers 6 |
| `constants` | 0/0/1/0 | 1 | brainteasers 6 |
| `cycle-following` | 0/1/0/0 | 1 | brainteasers 10 |
| `divisibility` | 0/0/1/0 | 1 | brainteasers 3 |
| `double-counting` | 0/0/1/0 | 1 | brainteasers 3 |
| `egg-drop` | 1/0/0/0 | 1 | brainteasers 8 |
| `egg-drop-dp` | 0/0/0/1 | 1 | brainteasers 2 |
| `hats-line-parity` | 1/0/0/0 | 1 | brainteasers 5 |
| `hats-mod-k` | 0/0/1/0 | 1 | brainteasers 3 |
| `hats-simultaneous` | 0/0/0/1 | 1 | brainteasers 3 |
| `hourglasses` | 0/1/0/0 | 1 | brainteasers 3 |
| `invariant-parity` | 1/0/0/0 | 1 | brainteasers 5 |
| `invariant-product` | 0/0/0/1 | 1 | brainteasers 1 |
| `jugs` | 1/0/0/0 | 1 | brainteasers 4 |
| `last-digit` | 0/1/0/0 | 1 | brainteasers 6 |
| `missing-information` | 0/0/0/1 | 1 | brainteasers 1 |
| `monovariant` | 0/0/0/1 | 1 | brainteasers 3 |
| `pairing` | 0/0/0/1 | 1 | brainteasers 5 |
| `pigeonhole-pairs` | 0/1/0/0 | 1 | brainteasers 3 |
| `pigeonhole-worst-case` | 0/1/0/0 | 1 | brainteasers 7 |
| `pirates` | 1/0/0/1 | 2 | brainteasers 10 |
| `powers-of-two` | 0/0/1/0 | 1 | brainteasers 2 |
| `relative-speed` | 0/0/1/0 | 1 | brainteasers 1 |
| `river-crossing` | 0/0/0/1 | 1 | brainteasers 1 |
| `rule-of-72` | 0/1/0/0 | 1 | brainteasers 5 |
| `scheduling` | 0/0/1/0 | 1 | brainteasers 2 |
| `telescoping` | 0/0/1/0 | 1 | brainteasers 3 |
| `trailing-zeros` | 1/0/0/0 | 1 | brainteasers 3 |
| `weighing-heavy` | 1/0/0/0 | 1 | brainteasers 6 |
| `weighing-heavy-or-light` | 0/0/0/1 | 1 | brainteasers 2 |
| `weighing-scale` | 0/0/1/0 | 1 | brainteasers 2 |
| `work-rate` | 0/1/0/0 | 1 | brainteasers 2 |

**mental** (file prefix `mental-`)

| Family tag | Items by session (1/2/3/4) | Total | Course items already carrying this tag |
| --- | --- | --- | --- |
| `battery` | 0/0/0/1 | 1 | mental-pressure 11 |
| `estimate-exact` | 0/1/0/1 | 2 | mental-pressure 1 |
| `estimate-product` | 1/0/1/0 | 2 | mental-pressure 1 |
| `fraction-compare` | 1/0/0/1 | 2 | mental-pressure 1 |
| `fraction-gap` | 0/1/0/0 | 1 | mental-pressure 2 |
| `fraction-odds` | 0/0/1/0 | 1 | mental-pressure 1 |
| `mental-arithmetic` | 2/2/2/2 | 8 | none (bank-only family) |
| `negative-marking` | 1/0/0/0 | 1 | mental-pressure 10, recruiting 3 |
| `net-score` | 0/0/1/0 | 1 | mental-pressure 1 |
| `percent-chain` | 1/0/1/1 | 3 | mental-pressure 1 |
| `percent-points` | 0/1/0/0 | 1 | mental-pressure 1 |
| `percent-reverse` | 0/1/0/0 | 1 | mental-pressure 2 |
| `probability` | 0/0/0/1 | 1 | mental-pressure 8 |
| `ranking` | 1/0/1/0 | 2 | mental-pressure 8 |
| `sequence-differences` | 0/1/0/0 | 1 | mental-pressure 1 |
| `sequence-ratio` | 0/1/0/0 | 1 | mental-pressure 1 |
| `sequence-woven` | 0/0/1/0 | 1 | mental-pressure 1 |
| `sequences` | 1/0/0/1 | 2 | mental-pressure 8 |
| `skip-budget` | 0/1/0/0 | 1 | mental-pressure 1 |
| `sqrt-newton` | 1/0/1/1 | 3 | mental-pressure 3 |
| `sqrt-vol` | 0/1/0/0 | 1 | mental-pressure 1 |
| `word-filled` | 0/0/0/1 | 1 | mental-pressure 1 |
| `word-interest` | 1/0/0/0 | 1 | mental-pressure 1 |
| `word-time` | 0/0/1/0 | 1 | mental-pressure 1 |

**market-making** (file prefix `market-making-`)

| Family tag | Items by session (1/2/3/4) | Total | Course items already carrying this tag |
| --- | --- | --- | --- |
| `arbitrage` | 0/1/0/1 | 2 | mm-games 6 |
| `calibration` | 0/0/0/1 | 1 | mm-games 1 |
| `card-fair` | 1/1/1/1 | 4 | mm-games 12 |
| `contracts` | 0/1/0/0 | 1 | mm-games 6 |
| `coverage` | 0/0/1/0 | 1 | mm-games 1 |
| `dice-ev` | 1/0/0/1 | 2 | mm-games 3 |
| `digit-count` | 0/1/0/0 | 1 | mm-games 2 |
| `fermi` | 1/1/0/0 | 2 | mm-games 1 |
| `fermi-error` | 1/0/1/0 | 2 | mm-games 2 |
| `game-edge` | 0/0/0/1 | 1 | mm-games 3 |
| `hedge-ratio` | 1/0/1/1 | 3 | mm-games 4 |
| `informed-loss` | 1/0/0/1 | 2 | mm-games 5 |
| `intervals` | 1/0/1/0 | 2 | mm-games 7 |
| `ledger-pnl` | 0/0/1/0 | 1 | mm-games 10 |
| `options-game` | 0/1/0/0 | 1 | mm-games 12 |
| `outcome-vs-edge` | 0/1/0/0 | 1 | mm-games 4 |
| `position-limit` | 1/0/0/1 | 2 | mm-games 3 |
| `quote-centre` | 1/0/1/0 | 2 | mm-games 3 |
| `skew` | 0/1/0/0 | 1 | mm-games 2 |
| `thinking-aloud` | 0/0/1/0 | 1 | mm-games 4 |
| `zero-profit-spread` | 1/0/0/0 | 1 | mm-games 2 |

**behavioural** (file prefix `behavioural-`)

| Family tag | Items by session (1/2/3/4) | Total | Course items already carrying this tag |
| --- | --- | --- | --- |
| `after-rejection` | 0/1/0/1 | 2 | recruiting 3 |
| `cv-lines` | 0/0/1/0 | 1 | recruiting 2 |
| `final-round` | 0/0/1/1 | 2 | recruiting 4 |
| `project-account` | 1/1/0/1 | 3 | recruiting 3 |
| `reasoning-aloud` | 1/1/1/1 | 4 | recruiting 4 |
| `star-story` | 2/2/3/3 | 10 | recruiting 9 |
| `video-answer` | 0/1/1/1 | 3 | recruiting 4 |
| `why-us` | 1/1/1/2 | 5 | recruiting 5 |

A second tag is allowed and is never used here except where an item idea needs it; do not invent new first tags. If a session finds that a family name above is wrong, use the nearest existing tag and say so in the report.

## 4. Rules for every item

1. **Our own wording and numbers.** Never copy a reported question, a book's problem or a course item. The idea column names a classic *structure* only. Change the numbers, the setting and the sentence order.
2. **Firm names never appear** in a bank item: not in `question`, `prose`, `feedback`, `explain`, `source` or a model answer. Say "a trading firm", "a market maker", "a bank" or "a hedge fund" (DECISIONS: "Firm names", 2 Nov). Behavioural model answers use an invented candidate and firm types.
3. **Every stated number is computed twice**, once in closed form and once by enumeration, a linear solve or a seeded simulation checked against the exact value, both as `Fraction` where the answer is rational, with an `assert` that they agree (the mocks brief standard). The brief gives parameters, not answers, on purpose: compute them. Where an idea says "fair value" with a quote, the quote is a fair value plus a stated width, also computed.
4. **Choice items**: `"shuffle": true`, exactly one `correct`, three or four options, every distractor with a `why` that names the learner's action ("You added the two chances."). Distractors follow "Distractors (4 Nov)": the key never sits between a times-ten pair or between two equal slips. Interval and ranking choices carry `shuffle: true` too (DECISIONS "Numeric distractors"); write a ranking as a choice of listed orderings.
5. **Numeric items**: `answer`, an `abs` or `rel` tolerance with an `accept` line, a `label`, a `placeholder` when a fraction is welcome, and at least two `wrong` entries with an `id` and a `value`, each with a `feedback.byKey` line naming the learner's action. The `wrong` values only route feedback, so they may sit either side of the key ("Numeric distractors", 5 Nov). A fraction answer states both the fraction and the decimal in `accept`.
6. **`feedback.why`** on every wrong value (the `why` of a choice option, the `byKey` line of a numeric `wrong`), plus a `generic` line that points to the method without giving the answer.
7. **Explanations**: `explain.text` at most three sentences, each under 20 words, one idea, the number shown with its working. No "it can be shown".
8. **Voice**: British English, no exclamation marks, no em-dashes (use a comma, colon or full stop), sentences under 20 words, £ for money, second person, no emoji.
9. **Tags and fields.** `tags[0]` is the family from the table. `role` from the Roles column (T trader, R research, S strats, D developer). `style` from the group. `source` is one plain line: "Original" for a new item, or "Adapted from <course> <lesson id>" only if the idea is a deliberate variant, never "from <firm>". `pace` from the table, at most 180. `skills`: copy the skill ids of the "Draws on" lesson from its `course.json` map, so the item raises that skill. `requires`: `["<course>/<lesson id>"]` copied from "Draws on" **only when difficulty is 4 or 5**; difficulty 2 and 3 items have no `requires`. A lesson in `requires` must exist in that course's map (the validator checks).
10. **No duplicates.** Before writing an item, grep the course files for its structure and numbers. For example `grep -rl "pirates" app/content/courses/*/` then read the hits, and `grep -rn "<key number>" app/content/courses/{puzzles,brainteasers,mental-pressure,mm-games,recruiting}`. Also check `app/content/bank/sample.json` and the other sessions' tables. If a course item has the same structure and the same numbers, change the numbers or the twist. State in the report which items you changed for this reason.
11. **Spoken questions** (behavioural `longform`): the `prompt` is the interviewer's question, written the way it is asked. The `model` is a spoken answer written out in the first person of an invented candidate, about 120 to 180 words, in situation, task, action and result form where the family is `star-story`, with the reasoning aloud where it is `reasoning-aloud`. The `rubric` has 4 to 6 lines summing to exactly 10 points, each line a behaviour the interviewer marks (a specific situation, your own action named, a number or result, a lesson, a short answer, clarity). `pace` is the answer time in seconds, 120 to 180. Do not invent employers, grades or universities by name that exist: keep them generic ("a first-year group project", "a society trading game").
12. **The `question` field** carries the one thing to answer; `prose` carries the set-up. Say the unit in the question ("in pounds", "to the nearest minute"). KaTeX is allowed (`$...$`); never use `\$` for a dollar sign (it does not render), so use £ or write "dollars".

### Item skeletons

Numeric (copy the shape of `bank/sample.json`):

```json
{
  "id": "urns-reds-before-first-blue",
  "difficulty": 3,
  "skills": ["pz-symmetry"],
  "tags": ["urns"],
  "role": ["trader", "research"],
  "style": "probability",
  "source": "Original",
  "pace": 120,
  "prose": "A bag holds 8 red and 3 blue counters. You draw without replacement until the first blue counter.",
  "question": "How many red balls do you expect to draw first?",
  "widget": { "kind": "numeric", "answer": 2, "tol": { "abs": 0.005 }, "accept": "8/4 = 2.", "label": "Expected reds", "placeholder": "fraction or decimal",
    "wrong": [ { "id": "ratio", "value": 2.6667, "tol": { "abs": 0.001 } }, { "id": "half", "value": 4, "tol": { "abs": 0.001 } } ] },
  "feedback": { "correct": "8/4 = 2.", "generic": "Not quite right. Think of the blue balls as cutting the reds into equal gaps.",
    "byKey": { "ratio": "You divided reds by blues. Divide by one more than the blues, 3 + 1.", "half": "You took half the reds. The 3 blues cut the reds into 4 gaps, and only the first gap counts." } },
  "explain": { "text": "The 3 blue counters cut the 8 reds into 4 gaps of equal expected size. The first gap holds 8/4 = 2 reds on average. A seeded simulation agrees." }
}
```

(The numbers in this skeleton are illustrative, not an item to ship: session 1's item `1p10` uses other numbers. Its `skills` and `source` follow the rules in section 4.) A choice item uses `widget.options` with `correct: true` on one, a `why` on every other, and `"shuffle": true`. An `expression` item gives `answer` as KaTeX with an `accept` list of equivalent forms. A longform item is `{ "id", "difficulty", "tags", "role", "style", "source", "pace", "question": "Answer aloud, then write your answer here.", "widget": { "kind": "longform", "prompt", "model", "rubric": [ { "points": 3, "text": "..." } ] }, "feedback": { "correct", "generic" }, "explain": { "text" } }`: check `recruiting/homework-1.json` for a live example and copy its field names. A bank item is not a lesson screen: no hints, no ladder.

## 5. The items

Columns: **Ref** (working label), **Family** (first tag), **Item idea**, **Kind**, **D** (difficulty), **Pace** (seconds), **Roles** (T trader, R research, S strats, D developer), **Draws on** (`course/lesson-id`, the lesson whose method the item uses: copy its skill ids, and its id into `requires` only at difficulty 4 or 5).

An idea gives the situation and the parameters. It is not the finished question text and carries no answer. Where an idea names a choice, write three or four options with the misconception distractors listed in rule 4. If an idea cannot be made correct, unambiguous and answerable in its pace, swap it for another of the same family, kind and difficulty from the same lesson and say so in the report.

### Session 1 (50 items; run this first)

##### Session 1: probability (15 items, file `probability-1.json`)

| Id | Family (first tag) | Item idea | Kind | D | Pace | Roles | Draws on |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1p01 | `dice-ev` | Roll a fair d8 and may reroll once. Fair value of playing the best rule. | numeric | 3 | 120 | T,R,S | `puzzles/l1-dice-games` |
| 1p02 | `dice-ev` | Paid the smaller of two d10 rolls. Which of four values is the fair value (distractors: mean of means, larger, 5.5-1). | choice | 2 | 75 | T,S | `puzzles/l1-dice-games` |
| 1p03 | `coupon-collector` | Expected rolls to see every face of a d4, then say how it compares with a d8 (ask for the d8 value). | numeric | 3 | 120 | T,R,S | `puzzles/l2-every-coupon` |
| 1p04 | `coupon-collector` | Expected number of different colours in 8 draws with replacement from 5 colours (indicator method). | numeric | 4 | 150 | T,R | `puzzles/l4-indicator-tricks` |
| 1p05 | `waiting-for-hh` | Expected flips of a fair coin until TTH first appears (first-step equations). | numeric | 4 | 150 | T,R | `puzzles/l3-waiting-for-hh` |
| 1p06 | `waiting-for-hh` | Which pattern of HHT and HTH is waited for longer, and why: four-option choice with the overlap trap. | choice | 3 | 90 | T,R,S | `puzzles/l3-waiting-for-hh` |
| 1p07 | `at-least-one` | Smallest n so that n fair flips give at least one head with chance above 99%. | numeric | 2 | 60 | T,R,S | `counting-chance/l1-every-outcome` |
| 1p08 | `derangements` | Five people take hats at random: chance exactly two get their own. | numeric | 4 | 150 | T,R | `puzzles/l5-hats` |
| 1p09 | `cards-and-colours` | Two cards drawn from a full deck: chance the second is red given the first is a heart. | numeric | 4 | 100 | T,R,S | `puzzles/l7-cards-and-colours` |
| 1p10 | `urns` | An urn holds 7 red and 3 blue balls, drawn without replacement: expected reds before the first blue. | numeric | 4 | 120 | T,R | `puzzles/l8-urns` |
| 1p11 | `bayes-in-a-minute` | A screen flags 2% of clean trades and 90% of bad ones; 0.5% are bad. Chance a flagged trade is bad. | numeric | 3 | 120 | T,R,S | `puzzles/l9-bayes-in-a-minute` |
| 1p12 | `ruin-in-interviews` | Fair bets of £1 from £4 until £0 or £10: chance of reaching £10 and expected number of bets (ask for the duration). | numeric | 3 | 120 | T,R,S | `puzzles/l10-ruin-in-interviews` |
| 1p13 | `largest-of-several` | Four uniform draws on [0, 1]: chance the largest exceeds 0.8. | choice | 3 | 100 | T,R,S | `puzzles/l11-largest-of-several` |
| 1p14 | `ants` | Twenty ants on a 3 m rod walk at 1 m a minute, bouncing: expected minutes until the last one falls off. | numeric | 4 | 150 | T,S | `puzzles/l12-ants` |
| 1p15 | `broken-stick` | A stick breaks at two random points: chance the longest piece exceeds half the stick. | numeric | 5 | 180 | T,R | `puzzles/l13-broken-stick` |

##### Session 1: brainteasers (10 items, file `brainteasers-1.json`)

| Id | Family (first tag) | Item idea | Kind | D | Pace | Roles | Draws on |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1b01 | `bridge-crossing` | Five people cross a bridge with one torch: crossing times 1, 2, 5, 8 and 12 minutes, at most two at a time. Fastest total. | numeric | 4 | 180 | T,S | `brainteasers/l11-crossings-and-schedules` |
| 1b02 | `burning-ropes` | Two uneven ropes each burn in 60 minutes: how to time 45 minutes. | choice | 3 | 120 | T,S | `brainteasers/l5-ropes-and-jugs` |
| 1b03 | `clock-angle` | Angle between the hands at 7:24 (our own time). | numeric | 2 | 60 | T,S | `brainteasers/l12-clocks-and-trains` |
| 1b04 | `jugs` | Measure exactly 4 litres with a 7-litre and a 5-litre jug: fewest pours. | numeric | 4 | 150 | T,S | `brainteasers/l5-ropes-and-jugs` |
| 1b05 | `egg-drop` | Two eggs, a 60-floor building: fewest drops that guarantee the answer in the worst case. | numeric | 4 | 180 | T,R,S | `brainteasers/l9-egg-drop` |
| 1b06 | `hats-line-parity` | Seven prisoners in a line guess their own hat colour (two colours) from the front: guaranteed survivors. | numeric | 4 | 150 | T,S | `brainteasers/l7-hat-strategies` |
| 1b07 | `pirates` | Four pirates split 100 coins by backward induction: how many the proposer keeps. | numeric | 5 | 180 | T,S | `brainteasers/l6-back-from-the-end` |
| 1b08 | `weighing-heavy` | Twelve coins, one heavier, a balance: fewest weighings (then ask for 27 coins). | choice | 5 | 120 | T,S | `brainteasers/l4-weighing-coins` |
| 1b09 | `invariant-parity` | A row of lamps all off; each move flips three adjacent lamps. Can all be on? (choice with the parity reason). | choice | 3 | 120 | T,R,S | `brainteasers/l1-what-stays-the-same` |
| 1b10 | `trailing-zeros` | Trailing zeros of 125! in base 10, and in base 12 as follow-up (ask base 10 only). | numeric | 2 | 75 | T,R,S,D | `brainteasers/l13-digits-and-remainders` |

##### Session 1: mental (10 items, file `mental-1.json`)

| Id | Family (first tag) | Item idea | Kind | D | Pace | Roles | Draws on |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1m01 | `mental-arithmetic` | 47 times 63 without a calculator. | numeric | 3 | 25 | T | `mental-pressure/l2-two-by-two` |
| 1m02 | `mental-arithmetic` | 1,260 divided by 18. | numeric | 2 | 25 | T | `mental-pressure/l3-big-division` |
| 1m03 | `percent-chain` | A price rises 20% then falls 20%: net change in percent. | numeric | 2 | 20 | T,S | `mental-pressure/l6-percent-of-percent` |
| 1m04 | `fraction-compare` | Which is larger of 7/9 and 11/14: four-option choice that includes both and two ties. | choice | 2 | 20 | T | `mental-pressure/l5-which-fraction` |
| 1m05 | `estimate-product` | Estimate 48.7 times 212 to within 2%: pick the nearest of four values. | choice | 3 | 25 | T | `mental-pressure/l7-estimating-products` |
| 1m06 | `sequences` | Next term of 2, 5, 11, 23, 47. | numeric | 3 | 30 | T | `mental-pressure/l10-next-in-sequence` |
| 1m07 | `sqrt-newton` | Square root of 7,300 to the nearest whole number. | numeric | 4 | 30 | T | `mental-pressure/l8-square-roots` |
| 1m08 | `word-interest` | £8,000 at 5% compound for three years, to the nearest pound. | numeric | 3 | 45 | T,S | `mental-pressure/l11-word-problems` |
| 1m09 | `negative-marking` | Blind guess among 4 options with +1 and -1/3: expected score of guessing, and whether to guess with one option removed. | choice | 3 | 40 | T | `mental-pressure/l13-negative-marking` |
| 1m10 | `ranking` | Rank four chances (given as fractions and percents) from least to most likely: order widget as choice of orderings. | choice | 4 | 45 | T | `mental-pressure/l14-ranking-likelihoods` |

##### Session 1: market-making (10 items, file `market-making-1.json`)

| Id | Family (first tag) | Item idea | Kind | D | Pace | Roles | Draws on |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1k01 | `card-fair` | Two cards of a shuffled deck: fair value of the sum of their ranks (ace 1, court cards 10). | numeric | 3 | 90 | T | `mm-games/l9-cards-revealed` |
| 1k02 | `dice-ev` | Contract pays the larger of two d4: fair value and a sensible two-way price. | numeric | 4 | 90 | T | `mm-games/l2-dice-sum` |
| 1k03 | `fermi` | How many £1 coins in a stack as tall as a 20-storey building: one-significant-figure choice. | choice | 2 | 75 | T,S | `mm-games/l4-fermi` |
| 1k04 | `fermi-error` | Estimate with two inputs each off by 30%: range of the product (choice of intervals). | choice | 3 | 90 | T,S | `mm-games/l4-fermi` |
| 1k05 | `intervals` | Pick the tightest interval you would defend 90% of the time for the total of five dice. | choice | 4 | 90 | T | `mm-games/l3-how-wide` |
| 1k06 | `quote-centre` | After a customer buys at your offer, how far to move your centre if each trade carries 0.2 of information. | numeric | 3 | 75 | T | `mm-games/l7-skewing` |
| 1k07 | `informed-loss` | One in five customers knows the value (says value 10 vs 0); average cost to you of a width-2 quote. | numeric | 4 | 120 | T,S | `mm-games/l8-informed-flow` |
| 1k08 | `position-limit` | You are long 8 against a limit of 10 and a customer wants to buy 5: what you can do. | choice | 3 | 60 | T | `mm-games/l10-position-limits` |
| 1k09 | `hedge-ratio` | Short 50 of a contract that moves 0.6 per 1 of a hedge instrument: size the hedge. | numeric | 3 | 75 | T,S | `mm-games/l11-hedging` |
| 1k10 | `zero-profit-spread` | Break-even width when 30% of trades are against an informed trader who gains 4 per trade. | numeric | 5 | 120 | T,R,S | `mm-games/l6-edge` |

##### Session 1: behavioural (5 items, file `behavioural-1.json`)

| Id | Family (first tag) | Item idea | Kind | D | Pace | Roles | Draws on |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1h01 | `star-story` | Tell me about a time you got something wrong at work or university and what changed (spoken, story form). | longform | 3 | 150 | T,R,S,D | `recruiting/l11-stories-that-answer` |
| 1h02 | `star-story` | Describe a disagreement with a teammate and how you settled it. | longform | 3 | 150 | T,R,S,D | `recruiting/l11-stories-that-answer` |
| 1h03 | `why-us` | Why do you want to trade rather than work in research or on a bank desk? | longform | 4 | 120 | T,S | `recruiting/l8-why-this-firm` |
| 1h04 | `project-account` | Walk me through a project you owned: the goal, your decisions and the result. | longform | 5 | 180 | T,R,S,D | `recruiting/l7-projects-that-count` |
| 1h05 | `reasoning-aloud` | You must pick between two options with half the information you want: say how you would decide aloud. | longform | 4 | 150 | T,R,S | `recruiting/l12-reasoning-aloud` |

### Session 2 (50 items)

##### Session 2: probability (15 items, file `probability-2.json`)

| Id | Family (first tag) | Item idea | Kind | D | Pace | Roles | Draws on |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2p01 | `dice-ev` | Paid the larger of a d6 and a d4: fair value. | numeric | 3 | 100 | T,R,S | `puzzles/l1-dice-games` |
| 2p02 | `dice-ev` | Paid the square of one d10 roll: fair value as an expression in n for an n-sided die. | expression | 4 | 120 | T,R,S | `puzzles/l1-dice-games` |
| 2p03 | `indicator-tricks` | Expected number of runs in 12 flips of a coin that lands heads with chance 0.3. | numeric | 4 | 150 | T,R | `puzzles/l4-indicator-tricks` |
| 2p04 | `when-to-stop` | Roll a d10 up to twice and keep the last roll you choose: value of the best rule. | numeric | 3 | 120 | T,R,S | `puzzles/l6-when-to-stop` |
| 2p05 | `when-to-stop` | Cards: 3 red and 2 black, turned one at a time, +£1 red and -£1 black, stop any time: value of the game. | numeric | 5 | 180 | T,R | `puzzles/l6-when-to-stop` |
| 2p06 | `fair-from-biased` | A coin shows heads with chance 0.2. Expected flips to make one fair bit by the pair method. | numeric | 3 | 120 | T,R,S,D | `puzzles/l25-fair-from-biased` |
| 2p07 | `estimating-n` | Five tickets drawn from 1 to N show a maximum of 84: the unbiased estimate of N. | numeric | 3 | 120 | T,R | `puzzles/l26-estimating-n` |
| 2p08 | `given-the-total` | Two dice sum to 9 given at least one shows a 4: chance it is the pair (4, 5). | numeric | 4 | 120 | T,R,S | `puzzles/l27-given-the-total` |
| 2p09 | `duels` | Two shooters alternate, hitting with chance 1/3 and 1/2 respectively: chance the first shooter wins. | numeric | 4 | 120 | T,R,S | `puzzles/l28-duels` |
| 2p10 | `semicircle` | Four random points on a circle: chance all lie on one semicircle. | choice | 4 | 150 | T,R | `puzzles/l14-semicircle` |
| 2p11 | `exceeding-one` | Expected number of uniform draws until the running sum first exceeds 2. | choice | 5 | 180 | T,R | `puzzles/l15-exceeding-one` |
| 2p12 | `meeting` | Two people each arrive uniformly in a 45-minute window and wait 10 minutes: chance they meet. | numeric | 3 | 120 | T,R,S | `puzzles/l16-meeting` |
| 2p13 | `who-wins` | Take 1 to 4 stones from 23; last stone loses. Go first or second, and what first move. | choice | 3 | 100 | T,R,S | `puzzles/l19-who-wins` |
| 2p14 | `cards-and-colours` | Expected number of red cards before the first ace in a full deck. | numeric | 5 | 150 | T,R | `puzzles/l7-cards-and-colours` |
| 2p15 | `urns` | Polya urn from 2 red and 1 blue, a drawn ball returned with one more of its colour: chance of two reds in the first three draws. | numeric | 4 | 150 | T,R | `puzzles/l8-urns` |

##### Session 2: brainteasers (10 items, file `brainteasers-2.json`)

| Id | Family (first tag) | Item idea | Kind | D | Pace | Roles | Draws on |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2b01 | `hourglasses` | Time 9 minutes with a 4-minute and a 7-minute hourglass: fewest flips. | numeric | 3 | 120 | T,S | `brainteasers/l5-ropes-and-jugs` |
| 2b02 | `common-knowledge` | Three logicians each wear a mark known to the other two: what each learns after each round of "I do not know". | choice | 5 | 150 | T,S | `brainteasers/l10-what-they-know` |
| 2b03 | `pigeonhole-pairs` | Among 13 people, how many must share a birth month; follow-up with sock pairs (choice). | choice | 2 | 60 | T,R,S,D | `brainteasers/l3-pigeonhole` |
| 2b04 | `pigeonhole-worst-case` | Socks of four colours in a drawer: fewest to take in the dark to guarantee three of a kind. | numeric | 4 | 90 | T,R,S,D | `brainteasers/l3-pigeonhole` |
| 2b05 | `cycle-following` | Two hundred boxes and a shuffled list: why following the cycle works (choice) and the survival chance bound. | choice | 5 | 180 | R,S | `brainteasers/l8-prisoners-and-boxes` |
| 2b06 | `last-digit` | Last digit of 7 to the power 2026. | numeric | 2 | 60 | T,R,S,D | `brainteasers/l13-digits-and-remainders` |
| 2b07 | `rule-of-72` | Years for a balance to triple at 6% a year to the nearest year (rule of 72 variants). | numeric | 3 | 60 | T,S | `brainteasers/l15-numbers-to-know` |
| 2b08 | `average-speed` | A trip of 60 miles at 40 mph then 60 miles back at 60 mph: average speed. | numeric | 2 | 60 | T,R,S,D | `brainteasers/l12-clocks-and-trains` |
| 2b09 | `work-rate` | Three pumps fill a tank in 6, 8 and 12 hours: time with the first two only. | numeric | 2 | 75 | T,S | `brainteasers/l12-clocks-and-trains` |
| 2b10 | `colouring-chequer` | Remove two opposite corners from a chequerboard of 8 by 8: can dominoes cover it? (choice with reason). | choice | 3 | 100 | T,R,S | `brainteasers/l2-colouring-boards` |

##### Session 2: mental (10 items, file `mental-2.json`)

| Id | Family (first tag) | Item idea | Kind | D | Pace | Roles | Draws on |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2m01 | `mental-arithmetic` | 86 times 44. | numeric | 2 | 25 | T | `mental-pressure/l2-two-by-two` |
| 2m02 | `mental-arithmetic` | 3,150 divided by 14. | numeric | 2 | 25 | T | `mental-pressure/l3-big-division` |
| 2m03 | `percent-reverse` | After a 25% rise a price is £150: the original price. | numeric | 2 | 20 | T,S | `mental-pressure/l6-percent-of-percent` |
| 2m04 | `percent-points` | A rate moves from 4% to 5%: percentage points and percent change (choice of pair). | choice | 2 | 20 | T,S | `mental-pressure/l6-percent-of-percent` |
| 2m05 | `fraction-gap` | Which pair of fractions has the larger gap: 5/8 and 3/5, or 7/12 and 4/7. | choice | 3 | 30 | T | `mental-pressure/l5-which-fraction` |
| 2m06 | `estimate-exact` | Estimate 31.2 times 19.8 and choose the exact one-decimal answer (choice with four close options). | choice | 4 | 25 | T | `mental-pressure/l7-estimating-products` |
| 2m07 | `sequence-differences` | Next term of 3, 4, 7, 12, 19. | numeric | 4 | 30 | T | `mental-pressure/l10-next-in-sequence` |
| 2m08 | `sequence-ratio` | Next term of 4, 6, 9, 13.5. | numeric | 3 | 25 | T | `mental-pressure/l10-next-in-sequence` |
| 2m09 | `sqrt-vol` | Annual volatility 24%: daily volatility with 256 trading days, to two significant figures. | numeric | 3 | 30 | T,R,S | `mental-pressure/l8-square-roots` |
| 2m10 | `skip-budget` | In 80 questions in 8 minutes, how many seconds on average per question and which to skip (choice). | choice | 4 | 30 | T | `mental-pressure/l9-eighty-in-eight` |

##### Session 2: market-making (8 items, file `market-making-2.json`)

| Id | Family (first tag) | Item idea | Kind | D | Pace | Roles | Draws on |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2k01 | `card-fair` | Three cards from a shuffled deck: fair value of the number of hearts and a two-way price. | numeric | 3 | 90 | T | `mm-games/l9-cards-revealed` |
| 2k02 | `digit-count` | Write the numbers 1 to 200: fair value of the count of the digit 1. | numeric | 4 | 100 | T,S | `mm-games/l1-unknown-quantity` |
| 2k03 | `fermi` | Estimate the number of London taxis: choice of one-significant-figure answers. | choice | 2 | 75 | T,S | `mm-games/l4-fermi` |
| 2k04 | `skew` | You are short 6 and the book is symmetric: which way to shift both quotes (choice with reasons). | choice | 3 | 60 | T | `mm-games/l7-skewing` |
| 2k05 | `arbitrage` | Quotes on A, B and A+B conflict: spot the free profit and its size. | numeric | 3 | 90 | T,S | `mm-games/l15-arbitrage-in-a-book` |
| 2k06 | `contracts` | Contract pays the larger of two d6 minus 3: fair value and a price you would quote. | numeric | 4 | 90 | T,R,S | `mm-games/l16-several-contracts` |
| 2k07 | `options-game` | Call and put on a card game outcome: fair value of the call struck at 6. | numeric | 5 | 120 | T,R,S | `mm-games/l17-options-on-a-game` |
| 2k08 | `outcome-vs-edge` | You lose £40 on a trade with positive edge: judge the decision (choice with four reasons). | choice | 2 | 60 | T,R,S | `mm-games/l6-edge` |

##### Session 2: behavioural (7 items, file `behavioural-2.json`)

| Id | Family (first tag) | Item idea | Kind | D | Pace | Roles | Draws on |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 2h01 | `star-story` | Describe a time you led without being in charge. | longform | 4 | 150 | T,R,S,D | `recruiting/l11-stories-that-answer` |
| 2h02 | `star-story` | Tell me about a time you had to learn something hard quickly. | longform | 3 | 150 | T,R,S,D | `recruiting/l11-stories-that-answer` |
| 2h03 | `why-us` | Why a market maker rather than a hedge fund? | longform | 3 | 120 | T,S | `recruiting/l8-why-this-firm` |
| 2h04 | `video-answer` | Thirty seconds to prepare, two minutes to answer: what makes you stand out from other applicants? | longform | 4 | 150 | T,R,S,D | `recruiting/l10-recorded-video` |
| 2h05 | `after-rejection` | Tell me about a rejection or a setback and what you did next. | longform | 3 | 150 | T,R,S,D | `recruiting/l15-after-a-rejection` |
| 2h06 | `project-account` | Explain one technical project to a non-specialist in two minutes. | longform | 4 | 180 | R,S,D | `recruiting/l7-projects-that-count` |
| 2h07 | `reasoning-aloud` | You are given a puzzle you have seen before: what do you say? | longform | 4 | 150 | T,R,S | `recruiting/l12-reasoning-aloud` |

### Session 3 (50 items)

##### Session 3: probability (14 items, file `probability-3.json`)

| Id | Family (first tag) | Item idea | Kind | D | Pace | Roles | Draws on |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 3p01 | `dice-ev` | Pay the second-largest of three d6 rolls: fair value. | numeric | 4 | 150 | T,R,S | `puzzles/l11-largest-of-several` |
| 3p02 | `coupon-collector` | Expected packs to collect all 6 stickers when each pack holds one at random, and the expected packs for the last one. | numeric | 3 | 120 | T,R,S | `puzzles/l2-every-coupon` |
| 3p03 | `at-least-one` | A signal fires with chance 3% each day: chance of at least one fire in 60 independent days. | numeric | 3 | 75 | T,R,S | `counting-chance/l1-every-outcome` |
| 3p04 | `derangements` | Eight guests take coats at random: expected number who get their own and its variance (choice of pairs). | choice | 4 | 150 | T,R | `puzzles/l5-hats` |
| 3p05 | `waiting-for-hh` | A strategy loses a day with chance 0.4: expected days until two losing days in a row. | numeric | 5 | 150 | T,R,S | `puzzles/l3-waiting-for-hh` |
| 3p06 | `bayes-in-a-minute` | A signal fires on 55% of good days and 25% of bad days, good days 30% of days: chance the day is good given a fire. | numeric | 4 | 120 | T,R,S | `puzzles/l9-bayes-in-a-minute` |
| 3p07 | `ruin-in-interviews` | Bets with win chance 0.45 from £3 to £9: chance of reaching £9. | numeric | 5 | 180 | T,R,S | `puzzles/l10-ruin-in-interviews` |
| 3p08 | `betting-on-sequences` | Bet on each flip of a 0.6 coin with the Kelly fraction: growth per flip to three decimals. | numeric | 4 | 150 | T,R,S | `puzzles/l20-betting-on-sequences` |
| 3p09 | `kelly` | A bet pays 2 to 1 and wins with chance 0.4: the Kelly fraction and whether it is a bet. | numeric | 4 | 120 | T,R,S | `puzzles/l21-kelly` |
| 3p10 | `when-to-hedge` | You hold a position that gains £6 or loses £4 with equal chance: when does a costly hedge pay (choice). | choice | 4 | 100 | T,R,S | `puzzles/l22-when-to-hedge` |
| 3p11 | `doubling-up` | Double the stake after each loss from a £1 base until a win or a cap of £16: chance of a loss run to the cap. | numeric | 4 | 120 | T,R,S | `puzzles/l23-doubling-up` |
| 3p12 | `random-chords` | A chord of a circle is drawn by picking two random points on the circle: chance it is longer than the radius. | numeric | 4 | 150 | T,R | `puzzles/l29-random-chords` |
| 3p13 | `expected-distance` | Two uniform points on a unit segment: expected distance and expected squared distance (ask for the square). | numeric | 3 | 120 | T,R,S | `puzzles/l18-expected-distance` |
| 3p14 | `buffon` | A needle of length 3 on lines 5 apart: chance it crosses a line. | numeric | 5 | 150 | T,R | `puzzles/l17-buffon` |

##### Session 3: brainteasers (10 items, file `brainteasers-3.json`)

| Id | Family (first tag) | Item idea | Kind | D | Pace | Roles | Draws on |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 3b01 | `hats-mod-k` | Five prisoners with hats numbered 0 to 4 guess their own: strategy guaranteeing one right (choice). | choice | 5 | 150 | T,S | `brainteasers/l7-hat-strategies` |
| 3b02 | `weighing-scale` | Nine coins, one lighter, balance: fewest weighings and the first split. | choice | 2 | 75 | T,S | `brainteasers/l4-weighing-coins` |
| 3b03 | `backward-induction` | Take-or-split pot game with three rounds: what the first player does (choice). | choice | 3 | 120 | T,R,S | `brainteasers/l6-back-from-the-end` |
| 3b04 | `scheduling` | Four jobs of lengths 3, 5, 2 and 6 on two machines: smallest finishing time. | numeric | 3 | 120 | T,S,D | `brainteasers/l11-crossings-and-schedules` |
| 3b05 | `divisibility` | Smallest number divisible by 1 to 10. | numeric | 2 | 60 | T,R,S,D | `brainteasers/l13-digits-and-remainders` |
| 3b06 | `powers-of-two` | A pond doubles its weed each day and is full on day 30: when is it a quarter full and when with four weeds. | numeric | 2 | 60 | T,S | `brainteasers/l15-numbers-to-know` |
| 3b07 | `telescoping` | Sum of 1/(k(k+1)) for k from 1 to 99. | numeric | 3 | 75 | T,R,S | `brainteasers/l14-sums-in-one-line` |
| 3b08 | `double-counting` | At a party of 11 people each shakes hands with an odd number: why impossible (choice). | choice | 3 | 100 | T,R,S | `brainteasers/l1-what-stays-the-same` |
| 3b09 | `relative-speed` | Two trains 90 miles apart at 30 and 45 mph, a bird at 60 mph: distance flown. | numeric | 2 | 75 | T,S | `brainteasers/l12-clocks-and-trains` |
| 3b10 | `constants` | Sum of the first 20 cubes, and the first 20 squares as a quick check. | numeric | 3 | 75 | T,R,S,D | `brainteasers/l15-numbers-to-know` |

##### Session 3: mental (10 items, file `mental-3.json`)

| Id | Family (first tag) | Item idea | Kind | D | Pace | Roles | Draws on |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 3m01 | `mental-arithmetic` | 73 times 28. | numeric | 2 | 25 | T | `mental-pressure/l2-two-by-two` |
| 3m02 | `mental-arithmetic` | 4,355 divided by 13 as a decimal to one place. | numeric | 3 | 30 | T | `mental-pressure/l4-decimals-fast` |
| 3m03 | `percent-chain` | Three successive moves of +10%, -10% and +10%: net percent to one decimal. | numeric | 3 | 30 | T,S | `mental-pressure/l6-percent-of-percent` |
| 3m04 | `fraction-odds` | Odds of 3 to 7 against: the implied chance as a percent. | numeric | 2 | 20 | T | `mental-pressure/l5-which-fraction` |
| 3m05 | `estimate-product` | Estimate 6.82 times 14.7 times 3.1 to within 3%. | choice | 3 | 30 | T | `mental-pressure/l7-estimating-products` |
| 3m06 | `sequence-woven` | Next term of 2, 10, 4, 20, 8, 40. | numeric | 4 | 35 | T | `mental-pressure/l16-harder-sequences` |
| 3m07 | `sqrt-newton` | Square root of 11 to two decimals by one Newton step from 3.3. | numeric | 4 | 40 | T,S | `mental-pressure/l8-square-roots` |
| 3m08 | `word-time` | A job takes 6 people 10 days: days for 4 people, and the day count of 4 working half-time (choice). | choice | 3 | 40 | T | `mental-pressure/l11-word-problems` |
| 3m09 | `net-score` | 80 questions, 61 right, 14 wrong and 5 skipped, +1 and -1: net score and accuracy. | numeric | 2 | 20 | T | `mental-pressure/l13-negative-marking` |
| 3m10 | `ranking` | Rank five chances given as odds, fractions and decimals (choice of orderings). | choice | 4 | 45 | T | `mental-pressure/l14-ranking-likelihoods` |

##### Session 3: market-making (8 items, file `market-making-3.json`)

| Id | Family (first tag) | Item idea | Kind | D | Pace | Roles | Draws on |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 3k01 | `card-fair` | Hearts-only contract on four cards from a deck: fair value of hearts seen and quote. | numeric | 3 | 90 | T | `mm-games/l9-cards-revealed` |
| 3k02 | `fermi-error` | Fermi estimate with one error 2x low: effect on the final answer (choice). | choice | 2 | 60 | T,S | `mm-games/l4-fermi` |
| 3k03 | `intervals` | Choose the interval for the number of heads in 100 flips that you would defend 95% of the time. | choice | 3 | 75 | T,R,S | `mm-games/l14-quoting-an-interval` |
| 3k04 | `coverage` | Of 20 intervals you gave at 80% confidence, 12 held the answer: what to change (choice). | choice | 3 | 75 | T,R,S | `mm-games/l14-quoting-an-interval` |
| 3k05 | `quote-centre` | A trade at your bid moves your fair value from 50 to 49.4: size of the move per unit of flow. | numeric | 3 | 75 | T | `mm-games/l7-skewing` |
| 3k06 | `ledger-pnl` | Ledger of five trades with a mark: P&L and which trade lost the most. | numeric | 3 | 100 | T,S | `mm-games/l13-full-game` |
| 3k07 | `hedge-ratio` | Hedge a basket worth 2.4 per point with an instrument worth 0.8 per point: units needed. | numeric | 2 | 60 | T,S | `mm-games/l11-hedging` |
| 3k08 | `thinking-aloud` | The interviewer says "make me a market in the number of letters in your name times 7": what do you say first (choice). | choice | 3 | 75 | T | `mm-games/l12-thinking-aloud` |

##### Session 3: behavioural (8 items, file `behavioural-3.json`)

| Id | Family (first tag) | Item idea | Kind | D | Pace | Roles | Draws on |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 3h01 | `star-story` | Describe a time you disagreed with someone senior. | longform | 4 | 150 | T,R,S,D | `recruiting/l11-stories-that-answer` |
| 3h02 | `star-story` | Tell me about a decision you made with incomplete information. | longform | 4 | 150 | T,R,S,D | `recruiting/l11-stories-that-answer` |
| 3h03 | `star-story` | Describe a time you worked in a team that was failing. | longform | 3 | 150 | T,R,S,D | `recruiting/l11-stories-that-answer` |
| 3h04 | `why-us` | What would you want to learn in your first six months on a trading desk? | longform | 5 | 120 | T,S | `recruiting/l8-why-this-firm` |
| 3h05 | `video-answer` | Describe your biggest strength with one example, in two minutes. | longform | 3 | 120 | T,R,S,D | `recruiting/l10-recorded-video` |
| 3h06 | `final-round` | A question stumps you in the final round: say what you do in the next minute. | longform | 4 | 150 | T,R,S | `recruiting/l13-the-final-round` |
| 3h07 | `cv-lines` | Pick the weakest line of your CV and defend it for two minutes. | longform | 3 | 150 | T,R,S,D | `recruiting/l6-one-page-cv` |
| 3h08 | `reasoning-aloud` | Estimate a number you have no data for, aloud, and state what would change your mind. | longform | 5 | 150 | T,R,S | `recruiting/l12-reasoning-aloud` |

### Session 4 (50 items)

##### Session 4: probability (12 items, file `probability-4.json`)

| Id | Family (first tag) | Item idea | Kind | D | Pace | Roles | Draws on |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4p01 | `dice-ev` | Roll a d6 with up to three rolls, keeping the last you choose: value of the best rule. | numeric | 4 | 150 | T,R,S | `puzzles/l6-when-to-stop` |
| 4p02 | `coupon-collector` | Each d6 roll costs £1 and a £20 prize pays once all six faces have shown: expected profit. | numeric | 3 | 150 | T,R,S | `puzzles/l2-every-coupon` |
| 4p03 | `indicator-tricks` | Expected number of empty boxes when 12 balls go into 8 boxes at random. | numeric | 3 | 120 | T,R | `puzzles/l4-indicator-tricks` |
| 4p04 | `bayes-in-a-minute` | Two independent positive tests with sensitivity 0.9, false positive 0.08 and base rate 0.02: posterior. | numeric | 4 | 150 | T,R,S | `puzzles/l9-bayes-in-a-minute` |
| 4p05 | `largest-of-several` | Expected minimum of three independent exponential waits with rates 1, 2 and 3. | numeric | 3 | 120 | T,R | `puzzles/l11-largest-of-several` |
| 4p06 | `ants` | Fly between two trains closing at 40 mph each from 120 miles apart, fly at 90 mph: distance flown. | numeric | 2 | 90 | T,S | `puzzles/l12-ants` |
| 4p07 | `broken-stick` | Break a stick in two at a random point: expected length of the longer piece. | choice | 3 | 90 | T,R,S | `puzzles/l13-broken-stick` |
| 4p08 | `estimating-n` | Capture and recapture: 50 tagged, 40 caught, 8 tagged: estimate the total. | numeric | 2 | 75 | T,R,S | `puzzles/l26-estimating-n` |
| 4p09 | `duels` | Three shooters with hit chances 0.4, 0.7 and 1.0 shoot in turn, weakest first: first shooter best first shot (choice). | choice | 5 | 180 | T,R | `puzzles/l28-duels` |
| 4p10 | `who-wins` | Alternate taking 1, 2 or 5 from 40 items, last item wins: winning first move. | numeric | 3 | 120 | T,R,S,D | `puzzles/l19-who-wins` |
| 4p11 | `given-the-total` | Three dice sum to 10 given the first shows a 3: chance the others are (3, 4) in some order. | numeric | 4 | 120 | T,R,S | `puzzles/l27-given-the-total` |
| 4p12 | `kelly` | Bet repeatedly with win chance 0.55 at even odds: expected log growth at twice the Kelly fraction (choice of signs). | choice | 5 | 150 | T,R,S | `puzzles/l21-kelly` |

##### Session 4: brainteasers (10 items, file `brainteasers-4.json`)

| Id | Family (first tag) | Item idea | Kind | D | Pace | Roles | Draws on |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4b01 | `weighing-heavy-or-light` | Twelve coins, one different in an unknown direction, three weighings: first weighing and reading (choice). | choice | 5 | 180 | T,S | `brainteasers/l4-weighing-coins` |
| 4b02 | `pirates` | Five pirates and 100 coins: the proposer keeps how many. | numeric | 5 | 180 | T,S | `brainteasers/l6-back-from-the-end` |
| 4b03 | `egg-drop-dp` | Three eggs on a 100-floor building: fewest drops in the worst case. | numeric | 5 | 180 | T,R,S,D | `brainteasers/l9-egg-drop` |
| 4b04 | `river-crossing` | A farmer, wolf, goat and cabbage: fewest crossings. | numeric | 2 | 90 | T,S | `brainteasers/l11-crossings-and-schedules` |
| 4b05 | `pairing` | Eight teams knock-out: number of matches and why (choice). | choice | 2 | 60 | T,R,S,D | `brainteasers/l3-pigeonhole` |
| 4b06 | `invariant-product` | A board of numbers where you replace two by their sum minus one: final value is fixed. Find it (numeric). | numeric | 4 | 150 | T,R,S | `brainteasers/l1-what-stays-the-same` |
| 4b07 | `monovariant` | A stack of coins where a move splits a pile: why the process must end (choice). | choice | 4 | 150 | R,S,D | `brainteasers/l1-what-stays-the-same` |
| 4b08 | `hats-simultaneous` | Three people with red or blue hats guess together: best guaranteed winning chance. | numeric | 4 | 150 | T,R,S | `brainteasers/l7-hat-strategies` |
| 4b09 | `common-knowledge` | Cheating spouses puzzle with 3 cheaters: day the cheaters act (numeric). | numeric | 5 | 180 | T,S | `brainteasers/l10-what-they-know` |
| 4b10 | `missing-information` | A question gives a price and a count but no unit: what you would ask first (choice). | choice | 3 | 75 | T,R,S | `brainteasers/l16-mixed-set` |

##### Session 4: mental (10 items, file `mental-4.json`)

| Id | Family (first tag) | Item idea | Kind | D | Pace | Roles | Draws on |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4m01 | `mental-arithmetic` | 97 times 53. | numeric | 2 | 25 | T | `mental-pressure/l2-two-by-two` |
| 4m02 | `mental-arithmetic` | 7,448 divided by 28. | numeric | 3 | 30 | T | `mental-pressure/l3-big-division` |
| 4m03 | `percent-chain` | A fund falls 30% then needs what percent gain to recover (to the nearest percent). | numeric | 3 | 25 | T,S | `mental-pressure/l6-percent-of-percent` |
| 4m04 | `fraction-compare` | Order 5/7, 8/11 and 13/18: pick the middle one. | choice | 3 | 30 | T | `mental-pressure/l5-which-fraction` |
| 4m05 | `estimate-exact` | Estimate 0.0481 times 2,060 and choose the answer (choice). | choice | 3 | 25 | T | `mental-pressure/l7-estimating-products` |
| 4m06 | `sequences` | Next term of 1, 3, 7, 15, 31, 63 and the 10th term. | numeric | 3 | 35 | T | `mental-pressure/l16-harder-sequences` |
| 4m07 | `sqrt-newton` | Square root of 2,400 to the nearest tenth. | numeric | 3 | 35 | T,S | `mental-pressure/l8-square-roots` |
| 4m08 | `word-filled` | A tank fills in 12 hours and a drain empties it in 20: hours to fill with both. | numeric | 3 | 40 | T | `mental-pressure/l11-word-problems` |
| 4m09 | `probability` | Chance of at least two heads in four flips as a fraction. | numeric | 3 | 30 | T,R,S | `mental-pressure/l15-probability-at-speed` |
| 4m10 | `battery` | Five quick-fire items (a fraction, a percent, a product, a term, a probability) answered as one chain, last answer (numeric). | numeric | 5 | 60 | T | `mental-pressure/l17-full-battery` |

##### Session 4: market-making (8 items, file `market-making-4.json`)

| Id | Family (first tag) | Item idea | Kind | D | Pace | Roles | Draws on |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4k01 | `card-fair` | Face-up cards with 5 cards seen and 47 hidden: fair value of the next card rank. | numeric | 3 | 75 | T | `mm-games/l9-cards-revealed` |
| 4k02 | `dice-ev` | Quote a market on the product of two d6 rolls: fair value and width you would use. | numeric | 3 | 90 | T | `mm-games/l2-dice-sum` |
| 4k03 | `informed-loss` | You quote 98 at 102 around fair 100; a buyer lifts you and it is informed: how many uninformed trades pay it back. | numeric | 4 | 100 | T,R,S | `mm-games/l8-informed-flow` |
| 4k04 | `position-limit` | Long 9 with a limit of 10 and flow arriving both ways: which order (choice). | choice | 3 | 60 | T | `mm-games/l10-position-limits` |
| 4k05 | `hedge-ratio` | Option delta 0.35 on 40 contracts: shares to hedge. | numeric | 2 | 60 | T,S | `mm-games/l11-hedging` |
| 4k06 | `arbitrage` | Prices of three contracts violate a sum rule by £3: the trade to put on (choice). | choice | 3 | 90 | T,S | `mm-games/l15-arbitrage-in-a-book` |
| 4k07 | `game-edge` | A game costs £5 and pays the square of a d6 in pounds over 10: edge and whether to quote it. | numeric | 4 | 100 | T,R,S | `mm-games/l5-two-sided` |
| 4k08 | `calibration` | Of 50 estimates at 90% confidence, 40 held: miscalibration and the fix (choice). | choice | 3 | 75 | T,R,S | `mm-games/l14-quoting-an-interval` |

##### Session 4: behavioural (10 items, file `behavioural-4.json`)

| Id | Family (first tag) | Item idea | Kind | D | Pace | Roles | Draws on |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 4h01 | `star-story` | Describe a time you ran something with a deadline and not enough people. | longform | 3 | 150 | T,R,S,D | `recruiting/l11-stories-that-answer` |
| 4h02 | `star-story` | Tell me about a time you gave someone hard feedback. | longform | 4 | 150 | T,R,S,D | `recruiting/l11-stories-that-answer` |
| 4h03 | `star-story` | Describe a time you changed your mind in front of others. | longform | 4 | 150 | T,R,S,D | `recruiting/l11-stories-that-answer` |
| 4h04 | `why-us` | Why do you want to be a quant researcher rather than a trader? | longform | 3 | 120 | R,S | `recruiting/l8-why-this-firm` |
| 4h05 | `why-us` | What do you do outside study that tells us how you think? | longform | 3 | 120 | T,R,S,D | `recruiting/l8-why-this-firm` |
| 4h06 | `video-answer` | Tell me about a time you worked under pressure, in two minutes, after thirty seconds to prepare. | longform | 3 | 150 | T,R,S,D | `recruiting/l10-recorded-video` |
| 4h07 | `after-rejection` | A mentor says you were not chosen because you gave up too early in the final round: respond. | longform | 4 | 150 | T,R,S,D | `recruiting/l15-after-a-rejection` |
| 4h08 | `final-round` | You have an offer deadline in 48 hours and another firm has not replied: say what you do. | longform | 4 | 150 | T,R,S,D | `recruiting/l14-offers-and-deadlines` |
| 4h09 | `project-account` | Describe the hardest bug or analysis error in your project and how you found it. | longform | 4 | 180 | R,S,D | `recruiting/l7-projects-that-count` |
| 4h10 | `reasoning-aloud` | The interviewer interrupts your answer with a harder follow-up: how do you carry on. | longform | 5 | 150 | T,R,S | `recruiting/l12-reasoning-aloud` |

## 6. Per-session notes

- **Session 1** has five behavioural items: one per theme, all difficulty 3 or 4. They are the first spoken-form items in the app, so write the five rubrics with care and reuse their rubric shape in sessions 2 to 4 (state the shape in your report). Session 1 also sets the house style for numeric `wrong` entries and for `byKey` lines, so write them with care.
- **Session 2** carries the only `expression` item (`2p02`, the fair value of the squared roll as a function of the number of sides).
- **Session 3** is the heaviest on difficulty 4, with the Kelly and gambler's ruin items. Check `kelly` first: `puzzles` l21 and `game-theory` already carry many items with that tag, so its bank items must use a different bet.
- **Session 4** is the heaviest on spoken items (10) and holds the hardest brainteasers (difficulty 5). Its `battery` item is a chained numeric: write it as five short stated steps in `prose` and ask only for the last result.

## 7. Acceptance

From `app/` unless a path is absolute. Use `--local-cdn <pkgs>` where the playthrough needs packages (the scratchpad `pkgs` folder named in `docs/LEVEL-BRIEF.md`).

1. `node tools/validate.mjs 2>&1 | tail -5` reports 0 errors. Warnings about other courses' unwritten lessons are fine. No `style` or `source` warning from your files. It rewrites `content/manifest.json`; that is expected.
2. `node tools/playthrough.mjs --routes-only --local-cdn <pkgs> 2>&1 | tail -30` is green, then again with `--mobile`. This plays the bank deck (the card, one deck of 8 answered right, the pace line, the schedule, a miss, an old save).
3. **Playing every item.** The engine has no flag to play one bank file, and one `--routes-only` deck reaches only 8 items. So write a scratch Playwright script in your own scratchpad folder (never in the repo) that copies the deck loop of `tools/playthrough.mjs` (the `bankChecks` function: `ZQ.select.bankDeck({ n: 8 })`, `ZQ.test.answerCorrect()`, `ZQ.test.check()`, `ZQ.test.continue()`) and repeats it until every item of your session's files has been dealt and answered correctly, clearing `ZQ.state.bank` between sittings if it must. Items with `requires` are dealt only after their lessons are finished: import a save that marks those lessons finished, or run once per lesson. In the report say how many of your 50 items were played, and that every `choice` shuffled option set had exactly one correct. Also confirm the starter state: a wrong answer for each `wrong` id gives its `byKey` line, and a wrong choice shows its `why`.
4. **Voice scan**, both counts zero: `VOICE_BASE=/home/user/zero-to-quant/app/content/bank/ python3 docs/reviews/voice-scan.py` must report "explanations over three sentences: 0" and "over 20 words: 0". I ran it on the folder in this session: it works unchanged on `content/bank/` (it reads every `.json` there, including `sample.json`, and scanned 198 sentences with 0 and 0). Because it scans the whole folder, the other sessions' files count too: fix only your own, and report a failure in someone else's file rather than editing it. Run it once with `--summary` for the report. If it needs a change, say so in the hand-back; do not edit the script.
5. **Numbers**: a script `bank-1-<session>.py` in your scratchpad folder `bank-1-<session>/` computes every keyed answer and every `wrong` value two ways with `assert`s, writes nothing into the repo, and is embedded in full in the report with its output.
6. **Grep for duplicates** (rule 10) and list in the report the 5 closest course items you found and what you changed.
7. **Counts**: the report states items per file, per family, per difficulty and per kind, and they match the tables (a difference needs a reason).
8. **Report** at `docs/reports/bank-1-<session>.md`: files written with item counts, validator and playthrough results, the voice scan output, the script and its output, every number with its two computations, the item ids with their working refs, changes from the table and why, a proposal of any course item to tag, and the open question list. Hand back at most six lines.
9. **Inbox**: every engine or schema limitation that bent an item goes to `docs/BACKLOG-INBOX.md` as unnumbered bullets under a heading `Raised later (bank part 1 session n):` (n is your session number), one bullet per limitation, with the workaround and the wanted behaviour, in the style of the existing bullets.

Do not edit: engine files (`app/js/`, `app/tools/`, `app/css/`, `app/index.html`), any `course.json`, `content/courses/` files, exams, `content/prep.json`, `docs/reviews/voice-scan.py`, another session's bank files, or `docs/briefs/bank.md`. No git write commands: the orchestrator commits. Other agents are editing other folders at the same time; the validator rewriting `content/manifest.json` is expected.

## 8. The sample bank, `bank/sample.json`

Ten items adapted from level reviews (`dice-ev`, `digit-count`, `fermi`, `coupon-collector`, `mental-arithmetic`, `at-least-one`, `regime-length`, `derangements`). `KNOWN_ISSUES.md` says it is probably learner-visible, and it is: the manifest lists it, so the deck draws it. It shows as "Sample interview bank" under the families it carries, so a learner would see ten items that also exist in their course reviews and would answer each twice.

Recommendation, not an action (do not delete it in a bank session):

1. Keep `sample.json` until session 1 has landed and its playthrough is green, because the `--routes-only` bank check needs at least one bank file.
2. Then remove it in a separate cleanup commit by the orchestrator (`git rm app/content/bank/sample.json`, re-run the validator to rewrite the manifest, re-run `--routes-only`). Nothing in `app/js/` or the playthrough names the file (the `bank/sample/x` string in the old-save check is only a made-up uid).
3. Little is lost: the ten items are variants of course review items, and the tagged ones (for example `dice-ev`, `fermi`, `regime-length`) are still dealt from their lessons. The families `coupon-collector`, `derangements` and `at-least-one` have no course tag, and session 1 covers them with new items (`1p03`, `1p08`, `1p07`). No bank item here repeats a sample item.
4. Update `docs/AUTHORING.md` (the sentence "The sample file is `content/bank/sample.json`...") and the `KNOWN_ISSUES.md` line at the same time.

## 9. Order and hand-off

Run session 1 first. When it is green, run sessions 2, 3 and 4 in parallel (disjoint files), then one second-read session for the whole bank (`docs/reviews/review-bank-1.md`, pattern `docs/reviews/review-1.5.md`: re-derive a sample of 30 answers, run the voice scan, read the behavioural rubrics, check family balance against section 3 and that no `pace` exceeds 180), then the sample cleanup in section 8, then a `PLAN.md` tick and a `PROGRESS.md` line.
