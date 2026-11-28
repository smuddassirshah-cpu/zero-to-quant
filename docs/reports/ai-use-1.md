# ai-use level 1: How a chatbot is made (report)

Author: content agent, wave session AK, branch `ai-w1-ai-use`. Brief: `docs/briefs/ai-use.md` Level 1 (with `docs/briefs/ai-strand-interfaces.md`).

## Files

| File | Screens or items | Quiz | Canvases and widgets |
|---|---|---|---|
| `l1-reading-the-internet.json` | 10 screens | 4 | table, bars (frames: 20-word table against an illustrative big model), array (tokens with the next one hidden), console; choice |
| `l2-from-predictor-to-assistant.json` | 9 screens | 4 | pair of consoles (tap a side), graph pipeline with frames (stage 1, stage 2), table, order with `after`; tap-regions on table rows; multi |
| `l3-learning-from-preferences.json` | 9 screens | 3 | pair (tap a side), graph frames (stage 3), table widget (rank three replies), tap rows, bars (illustrative 0.55 / 0.45) |
| `l4-confident-and-wrong.json` | 9 screens | 4 | console, array stepper over "the dog sat on the mat ." with a numeric for 1/36, multi, place (sort five claims into three bins), pair |
| `review-1.json` | 10 items, `pass: 0.8` | | au-making 6, au-limits 4; difficulty 2 to 4 |
| `homework-1.json` | 8 items | | order (9-step pipeline, `after`), a difficulty-5 two-part item (tap three of six claims, then why), numeric on a fresh text, multi, longform (10-point rubric, model answer) |
| `problems-1.json` | 3 problems, 10 parts | | p1 fresh 15-token text (count, chance, unseen sentence 1/6, name the effect), p2 tax chatbot (habit, danger, order of fixes), p3 best-fund transcript (tap, confidence, training cause); difficulty 4, 3, 5 |

Skills as in `course.json`: `au-making` for l1 to l3, `au-limits` for l4. Lesson ids, names and objectives copied from `course.json`.

## Checks (SESSION PROTOCOL 4)

1. Validator: `node tools/validate.mjs` 0 errors. Warnings on these files: 4 ladder canvas-kind changes (array to console, table to graph and back), 4 sentences of 20 to 24 words that quote the course text, nothing else.
2. Voice: `VOICE_BASE=app/content/courses/ai-use/ python3 docs/reviews/voice-scan.py 35 --summary`: over 35 words 0, lesson ids in code spans 0 (doubled words 0, explanations over three sentences 0).
3. Numbers: `docs/reports/ai-use-L1-numbers.py` with the venv Python: 79 of 79 checks, exit 0.
4. Playthrough with `--local-cdn` and `--mobile` (desktop and 440 px) on l1 to l4, review-1, homework-1 and problems-1: all passed; an earlier run with `--tablet --why` also passed (every slip routed). `grade-all.mjs --file` 0 failures on all seven files; `fresh-check.mjs --file problems-1.json` 0 hits.
Screenshots looked at: fixed right-aligned text tables (now `align: "left"`), a rank column cut off at 440 px (moved to the second column), and an array band label that showed raw KaTeX (now plain "1/6").

## Numbers and sources

Every number is in the script, each two ways (a Counter over the token list, and a scan of the spaced string; exact fractions).
- ai-basics text, 20 tokens, 19 pairs; row for "the": cat 3, mat 1, jam 1, dog 1 (1/2, 1/6, 1/6, 1/6), as `docs/briefs/ai-s0s1-scripts/stage0.py`.
- "the dog sat on the mat ." = 1/6 x 1 x 1 x 1 x 1/6 x 1 = 1/36 (about 0.028); not in the text. "the cat sat on the mat ." is in the text and is also 1/36 (l4 quiz).
- review r8: "the dog sat on the cat sat on the mat ." = 1/216 (0.00463); slips 1/72 and 1/36.
- homework h4: text "the bank raised rates . the fund raised cash . the bank cut costs ."; "the fund raised rates ." = 1/3 x 1/2 = 1/6.
- problems p1: text "the fund bought gold . the bank sold bonds . the fund sold gold ." (15 tokens); fund after the 2 of 3 = 2/3; "the bank sold gold ." = 1/3 x 1 x 1/2 x 1 = 1/6; slips 2/15 and 1/2.
- Illustrative distributions (said so on screen): l1 big-model frame 0.45, 0.30, 0.15, 0.05, 0.05, 0 (sum 1); l3 shares 0.55, 0.45.
- Small sums in example chats: 15% of £200 = £30, 10% of £90 = £9. l4 edge case: UK coins went decimal in 1971 (Decimal Day, 15 February 1971).
- Claims about training follow the brief's references (Karpathy 2023 and 2025): pretraining as next-token prediction over web text; fine-tuning as the same training on example conversations written by people, changing style and habits more than knowledge; rankings of pairs of replies making preferred replies likely; hallucination from likely text, from training that rewards a confident answer, and from no sense of what it does not know (examples that admit doubt are the mitigation). No model names, sizes, prices or dates of products are stated. Every transcript, firm, fund, book and study is invented and labelled.

## Notes for the second reader

- The brief's "l1 says a chatbot is that table made enormous" is carried by the l1 explore (table against big model) and the transfer.
- No `explore` in l2's hook position: the hook is the pair tap, the explore is the pipeline graph. l1, l3 and l4 likewise.
- Ladder canvas-kind warnings are deliberate (a token row, then a transcript).

## Proposed course.json change

None.

## Backlog

Four bullets added to `docs/BACKLOG-INBOX.md` under "Raised later (ai-use level 1)".
