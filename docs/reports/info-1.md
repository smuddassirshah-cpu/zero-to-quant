# info level 1 (Surprise and entropy): author report

Branch `ai-w1-info`. Brief: `docs/briefs/info.md` Level 1. Generators live in the scratchpad `info-1` folder (not committed).

## Files

| File | Screens or items | Quiz | Notes |
|---|---|---|---|
| `l1-surprise-in-bits.json` | 11 | 4 | array halving game (frames), plane $-\log_2 p$ with a point on the curve, `surprise_bits` code |
| `l2-average-surprise.json` | 11 | 4 | grouped bars (chance, surprise), binary entropy curve, table of terms, `entropy_bits` code |
| `l3-codes-that-save-space.json` | 12 | 4 | tree decode (ordered tap), prefix rows (tap), Huffman demonstrate, tie pair of trees, `is_prefix_free`, `huffman_lengths` |
| `l4-how-far-text-compresses.json` | 10 | 3 | 27-bar symbol shares (frames), `letter_entropy` and `compressed_bits_per_char` on `names.txt` |
| `review-1.json` | 10 items, `pass: 0.8` | | if-surprise 5, if-codes 5, difficulty 2 to 4 |
| `homework-1.json` | 8 items | | code d4 (`average_code_length`, `code_gap`), order d4, longform d5, performance task d5 |
| `problems-1.json` | 4 items, 16 parts | | difficulty 3, 4, 4, 5; every lesson used |

## Self-check (SESSION PROTOCOL 4)

1. Validator: 0 errors (`node tools/validate.mjs`); no warning on any info file.
2. Voice: `VOICE_BASE=app/content/courses/info python3 docs/reviews/voice-scan.py 35`: 0 over 35 words and 0 lesson ids in code spans; 0 doubled words.
3. Numbers: `docs/reports/info-L1-numbers.py` (venv Python) exits 0, 510 of 510 checks. Every stated figure is computed by two methods (log2 against ln / ln 2; Huffman by heap lengths against the sum of merged weights; letter entropy by shares against $\log_2 N - \tfrac1N\sum c\log_2 c$; bigram by pair counts against a 27 by 27 table) and found in the JSON. Each code solution is run on its hidden tests and each starter fails one. `check_wrongs` passes; the 58 "check by hand" byKey lines were read and state working, not the slip value.
4. Playthrough: `node tools/playthrough.mjs --lesson info/<each> --set info/review-1 --set info/homework-1 --problems info/problems-1 --mobile --local-cdn <pkgs>`: all passed at 1280 and 440 (quizzes 4/4, 4/4, 4/4, 3/3; homework 8 of 8 with the performance starter failing; problems 4 problems, 16 parts). Screenshots read at both widths; fixes made: y-axis labels on bars, demonstrate captions doubled, 27-bar labels thinned on a phone (letters now first so a, e and the end mark are labelled).
- Also: `grade-all.mjs` on the seven files, 0 failures; `fresh-check.mjs --file content/courses/info/problems-1.json`, 0 hits (6 advisory shared-parameter lines: chances such as 0.15 and 0.05, stock).

## Numbers and sources

All from the brief's header (recomputed by the script) except: Pyodide's zlib (1.2.13, Python 3.12.7) packs `names.txt` into 103,135 bytes, 3.6165 bits per byte, the same as CPython; measured with Pyodide 0.27.7 from the local package folder and in the playthrough's hidden test (tolerance 0.01). New figures: halt 10.97 bits, signal entropy 1.295, router entropy 1.923 and Huffman 1.95, feed Huffman 1.7 against 1.648, and the rest listed in the script with both methods.

## Conventions

- Bits by default; nats only where converted. Surprise $s(p) = -\log_2 p$ for $0 < p \le 1$. The names stream is each name plus `.` (228,146 symbols, 27 distinct). Code tests on Huffman compare the average length and the Kraft sum, never lengths where ties exist.
- Credit line for `names.txt` is in the `how` line of both l4 code widgets.

## Proposals

- No `course.json` change.
- `app/content/data/ai/README.md` says `names.txt` has 32,032 names; the file has 32,033 lines (MD5 matches the brief). The lessons state 32,033. A one-word fix for the README's owner.
