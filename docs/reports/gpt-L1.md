# gpt level 1: Tokenisation (report)

Author: content agent, wave AK, branch `ai-w2-gpt` (from 4797a36a). Brief: `docs/briefs/gpt.md` Level 1, with `docs/briefs/ai-strand-interfaces.md`. `info` L2 was not written when this level was made; units follow `docs/briefs/info.md` Level 2 and its draft (one nat is $1/\ln 2 \approx 1.443$ bits; bits per byte is $L / (b \ln 2)$).

## Files

| File | Screens or items | Quiz | Canvases and widgets |
|---|---|---|---|
| `l1-text-as-bytes.json` | 11 | 4 | array (characters, bytes in hex with labels and bands, bits; frames over four strings), table (UTF-8 rows); choice, numeric, table widget (hex), tap-regions (start bytes), 3 code (`utf8_length`, `char_spans`, `safe_truncate`) |
| `l2-merging-pairs.json` | 12 | 3 | array (toy text, stepper over 4 merges, `wrap`), table, bars (tokens against merges), console (order log); multi, numeric, table widget, choice, 3 code (`pair_counts`, `merge`, `train_bpe`) |
| `l3-encode-and-decode.json` | 11 | 4 | array stepper, tables (vocabulary, held-out compression, losses); numeric, choice, 2 code (`encode`/`decode`, `bits_per_byte`) |
| `l4-cleaning-the-corpus.json` | 12 | 3 | console (first 11 lines, tap), bars (frames: full text, slice), tables (counts, shingle sets, tap rows); tap-regions, numeric, choice, 2 code (`dedup_lines`, `shingles`/`jaccard`) |
| `review-1.json` | 10 items, `pass: 0.8` | | difficulty 2 to 4, every lesson at least twice |
| `homework-1.json` | 6 items | | `h-bpe-class` (performance `code`, d5), near-duplicate headlines (`code`, d4), order (one BPE merge, with a distractor and `after`), longform (letter counting, 10-point rubric, model answer), numeric bits per byte, choice (leak check) |
| `problems-1.json` | 3 problems, 13 parts | | bond merges by hand to bits per byte (d5, l2 + l3), a client name in a byte field (d3, l1 + l3), transcripts: dedup, Jaccard, leak share, bits per byte (d4, l4 + l3) |

Skill `gpt-token` throughout; ids, names and objectives from `course.json`. Performance task report: `docs/reports/gpt-1-perf.md`.

## Checks (SESSION PROTOCOL 4)

1. Validator: 0 errors. Warnings on these files: 6 ladder canvas-kind changes (a table of the UTF-8 rows or of counts beside an array; kept on purpose) and nothing else.
2. Voice: `VOICE_BASE=app/content/courses/gpt/ python3 docs/reviews/voice-scan.py 35 --summary`: over 35 words 0, lesson ids in code spans 0.
3. Numbers: `docs/reports/gpt-L1-numbers.py` with the venv: 251 of 251, exit 0 (253 with `GPT_FULL_TEXT` set to the full text).
4. Playthrough, `--local-cdn`, desktop and `--mobile` (440 px), with `--why`, on all seven files in one run: all passed (4 lessons 15 checks each, review 10 of 10, homework 6 of 6 with the performance starter failing and the longform marked, problems 13 parts with 21 slips routed). `grade-all.mjs --file <each> --code --local-cdn`: 0 failures (12 Python widgets: solution passes, starter fails, 34 mutants each fail their named test). `fresh-check.mjs --file problems-1.json`: 0 hits (one advisory: token ids 256 to 259 shared with l3; stock ids). `fresh-check --file homework-1.json`: the method name `encode` shared with l3, by design (see the perf report).

Screenshots looked at: a 23-cell array cut off at 440 px (now `wrap: 12`), the bars' y label touching the 20,000 value label (y max raised), the explore frames, the code screens and the longform card; nothing else wrong.

## Runtime (Pyodide 0.27.7, node, `tools/code-runner.mjs`)

Per-case times of the solutions (the runner's `times`): `train_bpe` with 50 merges on 20,000 characters 667 ms (CPython 115 ms); the performance class's Shakespeare case 485 ms; `encode`/`decode` through 30 merges 125 ms; `dedup_lines` on the whole slice 5 ms; every other case under 15 ms. All under the 1 s desktop rule; the Shakespeare cases also carry `budget` 2,000 to 6,000 ms for phones. No case trains more than 50 merges on 20,000 bytes.

## Numbers and sources

Every figure is in the script, two ways (see its docstring). Planner figures reproduced exactly: UTF-8 lengths and bytes (`£` c2 a3, `€` e2 82 ac, `日` e6 97 a5, emoji f0 9f 93 88; Price £5 8 and 9; naïve café 10 and 12); toy merges `bi`, `bid`, ` bid`, ` bidd`, 10 tokens; 20,000 characters: 50 merges 13,665 tokens (1.4636), 200 merges 9,940 (2.0121), first eight merges as stated; full text 32,777 non-empty lines, 25,721 distinct, 7,056 repeats, GLOUCESTER 229, DUKE VINCENTIO 193, ROMEO 163.

New figures (mine, two ways each):
- Toy row lengths 23, 19, 15, 12, 10; after merge 1, `bi d` 4, space `bi` 3, `i d` 0. Token counts at 0, 25, 50, 100, 150, 200 merges: 20,000, 15,240, 13,665, 11,886, 10,731, 9,940; shrink 50 to 200 merges 27.3% (3,725 of 13,665).
- Held out (last 25,000 characters, 200 merges from the first 20,000): 13,809 tokens, 1.8104 bytes per token. Last 5,000 with 50 merges: 1.4434 (homework threshold 1.4).
- Bits per byte: 4.20 nats per token at 2.0121 is 3.0114; bigram 2.4554 nats is 3.5424; vendors 1.18 against 1.25; 1.30 nats is 1.8755; 3.6 at 4.1 is 1.2668; 2.95 at 3 is 1.4187; 4.1 at 15/7 is 2.7604; 2.2 at 4 is 0.7935.
- Slice (the data file): 7,606 non-empty lines, 5,920 distinct, 1,686 removed; top lines MENENIUS 162, CORIOLANUS 149, GLOUCESTER 149. Full text: 6,913 of the 7,056 repeats are speaker tags (a line ending in a colon after a blank line), 98.0%; 143 others.
- Shingles: the Shell story, 92 characters, 88 shingles, 83 shared, 93 in either, $J = 0.8925$; the distributor table 0.91, 0.83, 0.80 (0.801), 0.22, 0.19, 0.18; review headlines 58/68 = 0.8529.
- `strawberry` with the 200-merge Shakespeare tokeniser: space, `st`, `ra`, `w`, `b`, `er`, `r`, `y` (homework model answer).

Data: only the existing `tiny-shakespeare.txt` slice (no new data file). The full-text figures need the 1.1 MB text, which cannot be a data file; the script recomputes them when `GPT_FULL_TEXT` names it and otherwise checks the recorded planner values. Seeds: none (all figures deterministic). Every company, fund and note is invented.

## Notes for the second reader

- l1 hook offers "It depends on the tokeniser" as the third length the brief asks for.
- Brief traps: l2 trap is overlapping pairs (`1000`); counting on old bytes is the l2 name screen's `i d` cell and review `r-second-merge`. l3 trap is training order (`the there`); per-token comparison is the transfer and a quiz item.
- MinHash is named in l4's generalise screen only.

## Proposed course.json change

None.

## Backlog

Three bullets in `docs/BACKLOG-INBOX.md` under "Raised later (gpt level 1)".
