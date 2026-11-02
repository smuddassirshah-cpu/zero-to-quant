# Report: recruiting level 2 ("The application")

Status: done. Authored 2 November 2026. Dated firm facts are pointers to l4 (October 2026) or l1; no firm is named anywhere in level 2. Generic firm types only ("one trading firm's official rule, in l4", "a bank's recorded round, l4"). Invented firms: Firm K, Firm M, Bank N, Fund P, Firms A and B, Bank C. Invented candidates: Sam (the weak CV), Jo (no finance job), Ben (the memorised answer) and Nadia, reused from level 1 for every model answer.

## Files written (`app/content/courses/recruiting/`)

| File | Contents |
|---|---|
| `l6-one-page-cv.json` | 11 screens: problem (CV table, tap 4 weak rows), problem, 4 ladder, trap (padded skills line), ladder (edge case: no finance job), generalise (verb + task + tool + number), follow-up problem ("how?" on a CV line), transfer (multi on three lines). 4 quiz. `rk-apply`. |
| `l7-projects-that-count.json` | 12 screens: problem (`pair` of two tables, `tap: "sides"`), problem, ladder `order` from the seven results-note headings (distractor: tool list), ladder `drag-point` on a 0 to 120 s line (15/45/90, live `derive` caption), ladder numeric (260 words), ladder multi (follow-ups on a number), problem (lead project per track), trap (Sharpe 2.1, best of 200), ladder (edge case: failed signal), generalise (budget in KaTeX), follow-up problem ("what would make 0.4 wrong?"), transfer (`console` 12-line account, tap l6 and l9). 4 quiz. `rk-apply`, `rk-behave`. |
| `l8-why-this-firm.json` | 11 screens: problem (three "why us" rows, tap the strongest), problem (three parts), 4 ladder (why trading or research; sources multi; 45 s numeric on a number line; `order` refitting evidence to a bank's strats desk, with a trader-reason distractor), trap (pay or prestige), ladder (edge case: a firm you know little about), generalise (fact + evidence + role), follow-up problem ("why not a hedge fund?"), transfer (`console` model paragraph, rubric multi). 4 quiz. `rk-apply`, `rk-behave`. |
| `l9-sitting-an-assessment.json` | 12 screens: problem (`boxes` Do / Do not, `place` boxes mode), problem (four parts), 5 ladder (8-month retake on a calendar line; blind-guess numeric −0.5; when to guess; 60/17 minutes numeric; proctoring multi), derive (`order` of the test morning, distractor "full mock straight before"), trap ("take it once to see the format"), ladder (edge case: connection drops), follow-up problem (five options, −0.25: blind guess worth 0), transfer (which test to sit first). 4 quiz. `rk-assess`. |
| `l10-recorded-video.json` | 12 screens: problem (`console` timestamped transcript, tap l5), problem (format table, 25% numeric), ladder `drag-point` (10 and 90 s, `tol` 10), generalise (budget in KaTeX, 173 words numeric), 4 ladder (three words not a script; set-up multi; story to question), trap (memorised answer or long preamble), ladder (edge case: an unexpected question), speaking-practice problem (answer aloud with a phone timer, then tick the model's rubric lines), follow-up problem ("what would you do differently?"), transfer (three question kinds to three stories). 4 quiz. `rk-assess`, `rk-behave`. |
| `review-2.json` | 9 items, difficulty 2 to 4, every item with `skills` and `tags`: weak CV line (table, tap), stronger project entry, 90-second budget (33.75 s), strongest "why us" sentence, one ruled out (−1/3), 15 items in 25 minutes (100 s), first answering line (console, tap), best of 150 settings, 8-month retake against the summer 2028 window. No longform. |
| `homework-2.json` | 8 items, every item with `skills` and `tags`: the one-page CV (longform, 5); three "why this firm" paragraphs (longform, 4 each; models for invented Firm M, Bank N, Fund P); the two-minute project account (longform, 4); three recorded-video practice answers (longform, 4); the assessment day `order` with distractor (4); net score under negative marking (numeric, 4). Each longform rubric sums to 10. |

Interview form: each lesson has one screen opening "**Follow-up.**" (the same task pushed the way an interviewer pushes it) and a pace in the prose where a timed task fits (l6 and l7 follow-ups, l8 45 s and 20 s, l9 follow-up, l10 30 s and 2 minutes). `tags` (kebab-case families: `cv-lines`, `cv-follow-up`, `cv`, `project-entry`, `project-account`, `project-follow-up`, `why-us`, `why-us-follow-up`, `negative-marking`, `assessment-pace`, `assessment-plan`, `video-answer`, `video-follow-up`) sit on every review and homework item and on each lesson's follow-up and transfer screen. Every `choice` and `multi` has `shuffle: true` except the ordered date options (l9 retake, l9 quiz) and the ordered word counts (l7 generalise). Each lesson's last screen says what homework 2 asks for. No audio anywhere; every spoken task says "answer aloud, then mark it" and "use a phone timer".

Helper scripts are in the scratchpad folder `rc2`: `common.py`, `l6.py` to `l10.py`, `sets.py` (generators), `lint.py` (sentence length, em-dashes, `!`, American spellings, sentence count of explanations), `rc2_numbers.py` (every number twice), `scroll.mjs` and `model.mjs` (scrolled 390 px captures).

## Validator and playthrough

- `node tools/validate.mjs`: **0 errors**; no warnings on any level 2 file (the only recruiting warning is "not yet written" for level 3).
- `node tools/playthrough.mjs --lesson recruiting/<id> --local-cdn <pkgs>`: l6 15 checks, l7 16, l8 15, l9 16, l10 16; every quiz 4/4; all passed (rerun after the last edits). `--set recruiting/review-2`: 9 of 9 recorded, passed. `--set recruiting/homework-2`: 8 of 8, 68 of 68 marks, passed.
- Screenshots: every screen at 1280 and 390 px with `--mobile --why` (524 files), plus scrolled 390 px captures of the l6 CV table (14 rows in a 360 px box), the l7 and l10 transcripts, and the homework CV model. Faults found and fixed: l9 cards overflowing their outlines (labels cut to 15 characters or fewer); Do and Do not cards filling from the bottom (now `fill: "top"`); a numeric placeholder repeating its unit ("words words", now "a number"); the "Again" label on the l9 calendar overlapping the applications bar (now below); the correct l9 transfer option the longest by far (shortened); no cue that the CV table scrolls (prose now says "Scroll the table to the end"); a project-account model whose stated length did not match its word count (recounted and restated).

## Deviations from the brief

- No firm is named in level 2 (orchestrator's rule): the brief's "Optiver allows no reset or retake within 8 months" is "one trading firm's official rule, in l4 (read October 2026)", and the HireVue facts are "a bank's recorded round, reported in l4 (October 2026)".
- The brief's review item "a 15-item, 25-minute sequence test, reported in l4" is posed as a hypothetical ("Say a sequence test gives ..."), because l4 does not report that format.
- l10 transcript lines carry timestamps (0:00 to 1:50), so "30 seconds of preamble" is visible rather than inferred from word counts (the first four lines hold only 40 words).
- l6 hook has 14 rows and asks for exactly 4 lines "an interviewer could not test": the profile line, "Responsible for data analysis", the six-language skills line and "Reading, travel".
- l7 hook transcript (transfer) asks for two taps: the missing number (l6) and the drift (l9), as the brief offers both.
- l9 transfer uses Nadia's three described links (Firms A, B, Bank C) rather than the learner's own list; the learner's own plan is homework 2's order item.
- Homework video rubric (the brief says "a rubric of 10"): 3 points first sentence, 3 points one story with a number, 3 points inside two minutes (one each per answer), 1 point three-line notes. Its model honestly scores 9 (one answer ran to 2:10) and says so.

## Firm and firm-type references (all as pointers, dated)

| Reference | Where | Date given | Source line |
|---|---|---|---|
| Trading firms state no finance knowledge is needed (F17) | l6 edge case, l8 ladder distractor | l1, as reported October 2026 | l1 trap |
| l4's table as a source to check against the firm's page | l8 sources ladder | dated October 2026 | l4 |
| One trading firm's official no-retake rule, 8 months (F10) | l9 ladder 1, l9 trap, review `r2-retake-window` | read October 2026 | l4 (official) |
| The reported 80 in 8 with +1/−1 and no skipping (F10) | l9 ladders 2 and 3 | October 2026 | l4 |
| 17 items in 60 minutes, rising difficulty (interview-gaps, SIG row) | l9 timing ladder | October 2026 | l4 |
| Attention games, proprietary and short | l9 timing explanation | October 2026 | l4 |
| Calculator allowed in one test, mental in another | l9 proctoring explanation | October 2026 | l4 |
| A bank's recorded round: one question, about 30 s to prepare, about 2 min, usually one take (F11) | l10 format screen, l10 transfer | October 2026 | candidate reports gathered for l4 |

## Numbers (each computed by script, `rc2_numbers.py`, and by a second route)

| Number | Where | Route 1 | Route 2 |
|---|---|---|---|
| 2 minutes at 130 words a minute = 260 words | l7, l10, quiz, homework | 130 × 2 | 120 s × 130/60 |
| 45 s = 97.5, "about 100" words | l7 generalise, l8 ladder | 130 × 0.75 | 195/2 as a fraction |
| 15 + 30 + 45 + 30 = 120 s; 32.5 + 65 + 97.5 + 65 = 260 words | l7 | sum | per section at 130/60 |
| 10 + 80 + 30 = 120 s; 80 s = 173.3 words | l10 | 130 × 80/60 | two thirds of 260 |
| 90 s = 195 words | l7 quiz | 130 × 1.5 | three quarters of 260 |
| 90 s account, result share = 33.75 s (about 73 words) | review | 45 × 90/120 | 37.5% × 90 |
| 250 words = 115 s | l8 quiz | 250/130 × 60 = 115.4 | 1.92 min × 60 |
| Model "why us" paragraphs: 85, 80, 86 words (39, 37, 40 s) | homework | word count | count/130 × 60 |
| Model project account: 207 words = 1 min 36 s | homework | 207 × 60/130 = 95.5 s | 207/130 = 1.59 min |
| Model l8 paragraph: 62 words, "about 60" | l8 transfer | word count | by line: 17 + 16 + 15 + 14 |
| Warm-up 30 of 120 s = 25% | l10 | 30/120 | quarter of 2 minutes |
| 40 to 6 minutes = 6.7 times faster | l6 | 40/6 | 85% time cut |
| Blind guess, 4 options, +1/−1: −0.5; one out −1/3; two out 0; three out +1 | l9, review, summary | p − (1 − p) | enumerate options |
| 5 options, +1/−0.25: blind 0; one out 1/16 | l9 follow-up | 1/5 − 4/5 × 1/4 | exact fractions |
| 80 in 8 = 6 s an item | l9, quiz | 480/80 | 10 items a minute |
| 17 in 60 = 3.53 minutes an item | l9 | 60/17 | 3600/17 s ÷ 60 |
| 15 in 25 = 100 s an item | review | 1500/15 | 1.67 min × 60 |
| 15 Nov 2026 + 8 months = 15 Jul 2027 (242 days); 1 Dec 2026 + 8 = 1 Aug 2027; 20 Nov 2026 + 8 = 20 Jul 2027 | l9, quiz, review | month count | date arithmetic in Python |
| Net score: 60 × (0.9 − 0.1) + 10 × 0 = 48 (wrong keys 54, 59, 43) | homework | expected value per item | 54 right − 6 wrong |
| Expected best of 200 no-edge Sharpes over 3 years ≈ 1.6 | l7 trap | E[max of 200 N(0,1)] = 2.746 (integral) × 1/√3 = 1.585 | simulation of 20,000 sets: 2.746 |

The Sharpe standard error is taken as $1/\sqrt{T}$ for a Sharpe near zero with $T$ years of data (Lo, 2002), as the Backtesting Engine trials line uses.

## Proposed change to `course.json`

None.

## Engine limits (5 bullets in `docs/BACKLOG-INBOX.md` under "Raised later (recruiting level 2):")

Hard-coded longform placeholder; card text overflowing `boxes` cards; no scroll cue on a capped `table` or `console`; the homework start card's time estimate (48 minutes for hours of writing); no lesson countdown for the 30 s and 2 minute timers (E6). The `tags` field is still unchecked by the validator (already raised by mm-games level 1) and dated facts still need E19 (already raised by recruiting level 1); not repeated.
