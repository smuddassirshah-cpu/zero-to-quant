# ai-use level 2: Asking and checking (report)

Author: content agent, wave session AK, branch `ai-w1-ai-use`. Brief: `docs/briefs/ai-use.md` Level 2. This level is the app's one home of prompting (review F4).

## Files

| File | Screens or items | Quiz | Canvases and widgets |
|---|---|---|---|
| `l5-asking-well.json` | 10 screens | 4 | pair (tap the clear request), place (sort a request into task, context, format, example), console, table; order with a distractor (split a long request; "make it sound positive" left out); tap rows (the honest "I cannot know") |
| `l6-checking-the-sums.json` | 11 screens | 4 | number-line explore with a years slider (simple against compound, live caption), number-line band, tables, tap the dropped row, console; `code` screen `compound(principal, rate, years)` (5 hidden tests) |
| `l7-checking-claims.json` | 8 screens | 3 | console (invented study), tap checkable claims, place (claim to best check), tables, trap on a working link |
| `l8-asking-for-the-working.json` | 8 screens | 3 | pair (bare answer against worked answer), tap the wrong step, numeric 12.68%, multi (good jobs for a chatbot), table (tool choice), numeric 6.17% |
| `review-2.json` | 10 items, `pass: 0.8` | | au-asking 5 (r1, r2, r3, r9, r10), au-checking 6 (r4 to r9); difficulty 2 to 4 |
| `homework-2.json` | 8 items | | difficulty-5 four-part item (tap two wrong figures and an invented source, recompute both, drop the source), order (checking steps, `after`), longform (10-point rubric, model answer), numerics (car, base, monthly card rate) |
| `problems-2.json` | 3 problems, 12 parts | | p1 estimate, exact, gap, which check (difficulty 4); p2 10% then 13%, gap, which percentage the chatbot used (3); p3 tap the wrong step, true yearly rate, cost, gap (5) |

Skills as in `course.json`: `au-asking` for l5 and l8, `au-checking` for l6, l7 and l8.

## Checks (SESSION PROTOCOL 4)

1. Validator 0 errors. Warnings on these files: 4 sentences of 20 words or more, each one quoting a chatbot or a long request.
2. Voice scan (`VOICE_BASE=app/content/courses/ai-use/`, 35): over 35 words 0, lesson ids in code spans 0.
3. Numbers: `docs/reports/ai-use-L2-numbers.py` with the venv Python: 197 of 197 checks, exit 0. It also runs the l6 code widget in CPython (solution passes all 5 tests, starter fails).
4. Playthrough `--mobile --why --local-cdn` on l5 to l8, review-2, homework-2 (with the parts checks) and problems-2: all passed, 15 typed slips routed in problems-2. l6 replayed with `--mobile` after one canvas change (the band screen now spans £2,700 to £2,800). `grade-all.mjs --file` 0 failures on all seven files; `fresh-check.mjs --file problems-2.json` 0 hits (one advisory chain-union warning: p1 follows the estimate-then-recompute pattern l6 teaches, on fresh numbers).

## Numbers and sources

All in the script, float against exact fractions, percentages also built from 10%, 5%, 2% and 1% parts.
- Brief figures: £2,400 at 3% for 5 years: £2,782.26 compound, £2,760 simple, band £2,760 to £2,784; 17% of £4,850 = £485 + £242.50 + £97 = £824.50 (chatbot's £971.50 is about 20%); $1.01^{12} - 1$ = 12.68%.
- l6: fall £80 to £60 is 25% (wrong base 33.3%); costs total £5,530, dropping July (£760) gives £4,770; 15% of £2,400 = £360; growth £40m to £50m is 25% (wrong base 20%). Code tests: 2782.26, 1102.5, 665.5, 4850, 100.
- l8: share £50 up 20% then down 20% = £48; coat £80 down 25% then up 25% = £75 (wrong base gives £80); $1.005^{12} - 1$ = 6.17%; quiz £200 up 10% then down 10% = £198.
- review-2: 6% of £3,500 = £210; 12% of £2,350 = £282 (£305.50 is 13%); £5,000 at 4% for 3 years = £5,624.32; salary £1,200 up 5% twice = £1,323.
- homework-2: £3,000 at 5% for 4 years = £3,646.52 (three years is exactly £3,472.875, a tie; that slip's band of 0.01 takes both roundings); 15% of £3,000 = £450 (£540 is 18%); car £12,000 at 15% a year for 2 years = £8,670; £64 to £80 is 25%; $1.02^{12} - 1$ = 26.82%.
- problems-2: £8,000 at 6% for 4 years = £10,099.82 (simple £9,920, gap £179.82); 13% of £6,400 = £832 (£1,152 is 18%, gap £320); $1.015^{12} - 1$ = 19.56%, cost on £2,000 = £391.24 (£391.20 from the rounded rate), gap £31.24.
- Prompting habits (task, context, format, example; paste the material; allow "I do not know") follow the brief's reference, Anthropic's prompt engineering documentation, in our own words. "Working can be written to fit an answer given first" follows Karpathy (2025). l7 names the Office for National Statistics as the publisher of UK inflation figures (a source, not a policy). Every study, journal, firm, fund and figure in a transcript is invented and labelled.

## Proposed course.json change

None.

## Backlog

Two bullets added to `docs/BACKLOG-INBOX.md` under "Raised later (ai-use level 2)".
