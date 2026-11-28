# ai-use level 3: The risks (report)

Author: content agent, wave session AK, branch `ai-w1-ai-use`. Brief: `docs/briefs/ai-use.md` Level 3. Builds on level 1 only (l10's bias is l1's "it learns what its text shows"; l12's alignment is l3's "it learns what raters preferred").

## Files

| File | Screens or items | Quiz | Canvases and widgets |
|---|---|---|---|
| `l9-what-not-to-paste.json` | 10 screens | 3 | console (client list), graph with frames (device, servers, kept, read by people?, used in training?), place (ten items into three bins), tap the identifying lines, multi on an invented settings page, tap the re-identifiable row |
| `l10-bias-from-data.json` | 10 screens | 3 | table (past hires), bars with frames (past rates against model rates), numeric gap in points, tables, trap on "a computer cannot be biased", numeric lender test |
| `l11-misuse-and-fakes.json` | 9 screens | 3 | table of three reviews, multi (which are misuses), tap the scam's warning signs, place (misuse to harm), console voice note, tap the one misuse among honest uses |
| `l12-what-alignment-means.json` | 9 screens | 3 | table (the robot and the rug, a made-up story), place (measured against meant), tables, bars of 20 days of P&L with a numeric total |
| `review-3.json` | 10 items, `pass: 0.8` | | au-risks 8, au-alignment 2 (r9, r10); difficulty 2 to 4 |
| `homework-3.json` | 8 items | | difficulty-5 incident report in three parts (multi, then two choices), order (before you paste), longform (five rules for a small fund, 10-point rubric, model answer), an l12 item (ideas counted, quality meant), tap rows, numeric, multi, tap lines |
| `problems-3.json` | 3 problems, 11 parts | | p1 screening table: two rates, the gap, measured against meant (4); p2 retrained: new rate, new gap, why, which l9 rule (5); p3 a reward for accepted interviews: measure and meaning, what it learns, a fee scam (4) |

Skills as in `course.json`: `au-risks` for l9 to l11, `au-alignment` for l12.

## Checks (SESSION PROTOCOL 4)

1. Validator 0 errors. Remaining warnings on these files are sentences of 20 to 26 words (advisory; none over 35).
2. Voice scan (`VOICE_BASE=app/content/courses/ai-use/`, 35): over 35 words 0, lesson ids in code spans 0.
3. Numbers: `docs/reports/ai-use-L3-numbers.py` with the venv Python: 102 of 102 checks, exit 0.
4. Playthrough `--mobile --why --local-cdn` on l9 to l12, review-3, homework-3 and problems-3 (homework-3 with its parts checks): all passed, 10 typed slips routed in problems-3. l9 replayed with `--mobile --why` after its graph labels were split onto two lines (they overlapped at 440 px). `grade-all.mjs --file` 0 failures on all seven files; `fresh-check.mjs --file problems-3.json` 0 hits.

## Numbers and sources

All toy data, computed as float and exact fractions, rates also re-derived from the tables' own cells.
- l10 toy screening (the brief's 30% and 10%): 100 applicants a group, 40 meeting the requirements in each; past hires 30 and 10; model shortlist 33 and 9, a gap of 24 points against the past 20. Lender test: 140 and 104 of 200, 70% against 52%, 18 points. Quiz: 45 of 150 and 15 of 100, 15 points.
- l12 transfer: 19 days of +£2k and one of −£60k total −£22k.
- review-3 r5: 54 of 120 (45%) and 18 of 80 (22.5%), 22.5 points. homework-3 h6: 168 of 240 (70%) and 99 of 180 (55%), 15 points.
- problems-3: 56 of 160 = 35%, 6 of 40 = 15%, gap 20; after retraining 13 of 40 = 32.5%, gap 2.5.
- No regulation, law or named organisation's policy is stated. Every legal point says "check your employer's policy and the law where you work". Where pasted text goes is told as "may be kept, read or used in training, depending on the provider's policy and your settings", the framing of the brief and of Elements of AI's chapter on privacy. The settings page, every firm, message, review, person and place is invented and labelled. The robot and rug is labelled a made-up story. l12 names `ai-safety` (Stage 3) and its topics in one sentence, and teaches none of its methods.

## Proposed course.json change

None.

## Backlog

One bullet added to `docs/BACKLOG-INBOX.md` under "Raised later (ai-use level 3)".
