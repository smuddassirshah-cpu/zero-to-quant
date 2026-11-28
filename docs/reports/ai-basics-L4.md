# ai-basics level 4 (Language by counting): report

## Files

| File | Screens or items | Quiz |
|---|---|---|
| `l13-what-comes-next.json` | 10 screens (problem tap the words after “the” on an `array`, explore `array` stepper over the 19 pairs with a tally caption and a `table` widget for the row, problem name the next-word (bigram) table, ladder row for cat, ladder 19 pairs, trap the table read backwards on the full `table`, ladder edge empty row, code `count_pairs`, generalise, transfer keyboard), 13 min | 3 |
| `l14-chances-for-the-next-word.json` | 10 screens (problem chance of cat on `bars`, problem name count over row total with a `table` widget, 3 ladder: cat row, sat row, a fund text of 16 words, trap divide by 20 words, ladder edge seen once, code `chances`, generalise, transfer up after up), 13 min | 3 |
| `l15-writing-by-rolling-dice.json` | 12 screens (problem fair picks, explore `number-line` with a draggable $u$ and a derive caption, problem name sampling by tapping an interval, 3 ladder: running total, by hand, `console` of four seed-7 runs, trap always the top word, ladder edge running total `0.9999999999999999`, code `pick`, code `generate`, generalise, transfer chatbot), 15 min | 3 |
| `l16-temperature-and-tokens.json` | 12 screens (problem tap the bolder writer on a `pair` of `bars`, explore temperature `frames` control, problem square and rescale `table` widget, 2 ladder: temperature 2, tie stays a tie, trap “more creative”, generalise with the certain-row edge case, code `with_temperature`, 3 token screens on `array` (pieces, three splits, why pieces), transfer contract drafting), 15 min | 4 |
| `review-4.json` | 10 items, difficulty 2 to 4, `pass: 0.8`, every item `ab-language`, lessons interleaved (l13 2, l14 3, l15 2, l16 3) | |
| `homework-4.json` | 7 items, difficulty 3 to 5: code `row_chances` (4), code `bigram_writer` (5), order with a distractor (3), numeric temperature row (4), choice boundary (4), numeric “.emma.” pairs (3), longform “fluent nonsense” (5) | |
| `problems-4.json` | 3 chained problems, 13 parts: desk chat log (4; l13 to l16), up and down days (3; l13 to l15), Bank of England note at temperatures 1, 2 and $\tfrac12$ (5; l15, l16) | |

Stage 0, so no performance task. No dictionaries in learner code: `generate` uses a given `row_for` helper (the brief's route), the other functions use lists, `sorted` (one sentence in l13) and tuples.

## Self-check (SESSION PROTOCOL 4)

1. `node tools/validate.mjs`: 0 errors. Warnings on level 4 files: two “ladder usually reuses the previous canvas kind” (l13 empty-row array after the table, l14 fund array after bars) and 9 `O2-long-sentence` (all under 35 words, kept where splitting would push an explanation past three sentences).
2. `voice-scan.py 35 --summary` on the course folder: 0 over 35 words, 0 lesson ids in code spans, 0 doubled words (repeated data such as `up up down` sits in code spans), 0 explanations over three sentences.
3. `docs/reports/ai-basics-L4-numbers.py` (venv): exit 0, 421 of 421 checks. The 26 “check by hand” lines were read: each states the working (row totals, word counts) of its slip.
4. Playthrough with `--local-cdn`, desktop and `--mobile`, with `--why`: all passed. l13 13 checks, l14 13, l15 15, l16 16 (quizzes 3/3, 3/3, 3/3, 4/4); review-4 10 of 10; homework-4 7 of 7, longform marked by the button; problems-4 13 parts, 17 typed slips routed. l16 and problems-4 were replayed after their last edits. Screenshots read at 1280 and 440: the l16 three-splits screen first drew the pieces as labelled bands on a wrapped character array, and the band labels ran into the question at 440 px; it now stacks a pieces array above a character array (a `pair`). `grade-all.mjs --code` on the seven files: 75 widgets and 7 Python code widgets, 0 failures (solution passes, starter fails, every mutant fails its named test). `fresh-check.mjs --file problems-4.json`: 0 hits after one fix (a retold slip line shared with l14); 3 advisory shared-parameter notes (0.01, 0.06, 0.09 as chances), not reuse.

Mutants (ENGINE-BACKLOG 1263): 7 code widgets, 22 mutants, the taught bug among them each time (pairs read backwards, divide by the words or by the different words, `<=` on the boundary, no fallback to the last word, always the top word, no rescale, power ignored). The validator accepts the field.

## Numbers (each computed twice: a dictionary count against a positional scan; chances and temperature rows in exact fractions against floats)

- Course text: 20 words, 19 pairs, 9 different words. Row “the”: cat 3, mat 1, jam 1, dog 1 (pairs 1, 8, 18 are “the cat”); cat: sat, ate, “.” once each, “the” 0; sat: on 2; “.”: the 2; dog: sat 1. Chances $\tfrac12, \tfrac16, \tfrac16, \tfrac16$; running totals $\tfrac12, \tfrac23, \tfrac56, 1$; $u$ = 0.1 cat, 0.5 mat, 0.62 mat, 0.9 dog, 0 cat.
- Floats: the loop running total is `0.9999999999999999` (= 1 − 2⁻⁵³), and so is the plain left-to-right sum. Note for readers: Python 3.12's `sum()` is compensated and returns 1.0, so the lesson shows a loop; the `pick` test uses $u$ = `0.9999999999999999`, which equals the last running total and needs the fallback.
- Temperature $\tfrac12$: $\tfrac34, \tfrac1{12}$ ×3 (squares add to $\tfrac13$). Temperature 2: 0.366 (exactly $(\sqrt3 - 1)/2$) and 0.2113; roots 0.7071 and 0.4082, total 1.9319. Cat row stays $\tfrac13$; a certain row stays 1.
- Seed 7 (`random.Random(7)`, 11 draws a run): the four runs in the l15 console; the second, “the cat ate the cat sat on the mat . the cat”, is a hidden test of `generate`, so Pyodide reproduces it. Greedy writer: “the cat sat on the cat sat on”.
- Other figures: fund text rose $\tfrac23$; share table 68/130 = 0.523 (slips 0.527, 0.273); keyboard 30; 600 picks give 300 cats; FTSE $u$ = 0.6 gives fell; tokens 3 words, 5 pieces, 19 characters (21 with spaces); review: 11 pairs, 0.692, 2, down at the 0.65 boundary, 0.6, 12, names 6,763/18,327 = 0.369 (from `names.txt`, two ways; matches `makemore` L1's 6,763), 0.571, $\tfrac13$; homework: $\tfrac23$, mat, 5 pairs in “.emma.”; problems: 4, $\tfrac12$, news, $\tfrac23$; 9, $\tfrac23$, $\tfrac13$, down then up ×4; 0.5625, 0.0625, cut, hold, 0.9758.

## Conventions

Words in prose in curly quotes; next words in a row are listed in order of first appearance in the text (cat, mat, jam, dog), which is the order sampling walks. The sampling rule is “the first word whose running total is above $u$, else the last word”. Temperatures used: $\tfrac12$ (square), 1, 2 (square root) only. Tokens: spaces left out of all three splits.

## Brief errors and notes

- The brief names the report `docs/reports/ai-basics-4.md`; the wave rules say `ai-basics-L4.md`, used here.
- “In floats the running total is 0.9999999999999999” holds for a loop or `a + b + c + d`, not for `sum()` in Python 3.12 (see above).
- The brief's l13 edge case “a word that never appears first (an empty row)” has no instance in the course text (every word starts a pair; the final “.” has a row from earlier full stops), so l13 uses “the dog sat on the mat”, where mat's row is empty.
- `row_chances` returns `(next_word, count, total)` triples rather than bare `(count, total)` pairs, so each fraction carries its word.

## Proposed course.json change

None.
