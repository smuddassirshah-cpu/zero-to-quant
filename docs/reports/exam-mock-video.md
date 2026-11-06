# Report: exam mock-video (recorded video interview)

Brief: `docs/briefs/mocks.md`, section `## mock-video` (written first in this task, appended at the end of the file).

## Files

- `app/content/exams/mock-video.json` (new): 5 papers of one `longform` prompt each, 2 checks.
- `docs/briefs/mocks-scripts/mock_video_build.py` (new): writes the JSON; holds every prompt, rubric, model and timing; asserts each number two ways.
- `docs/briefs/mocks-scripts/mock_video_check.py` (new): second route; imports `app/tools/numbers_lib.py`; 155 checks, exit 0.
- `docs/briefs/mocks.md`: `## mock-video` appended (no other section touched).
- `docs/readiness.md`: the four hand-written `mock-video` rows now read "exists" (lines 263, 526, 653, 781); `node tools/readiness-sums.mjs --write` then regenerated `app/content/readiness.json` (mocks present and missing per role). No generated block in the markdown changed.
- `docs/BACKLOG-INBOX.md`: 5 bullets under `Raised later (mock mock-video):`.

## Shape

| # | Paper | Prompt | Think | Answer (`seconds`) | Paper minutes | Item, family |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | `motivation` | What do you expect to find hardest in a quant internship, and how are you preparing for it? | 30 s | 120 s | 2.5 | `v1-hardest-part`, `hardest-part` |
| 2 | `someone-elses-error` | Behavioural: a mistake in someone else's numbers (paper name: Prompt 2: behavioural) | 30 s | 120 s | 2.5 | `v2-others-error`, `others-error` |
| 3 | `more-work-than-time` | Behavioural: a week with more work than time (paper name: Prompt 3: behavioural) | 30 s | 120 s | 2.5 | `v3-too-much-work`, `too-much-work` |
| 4 | `fair-price` | Technical: a fair price for a die game paying £10 for a six and £4 for a five (paper name: Prompt 4: technical) | 30 s | 90 s | 2 | `v4-fair-price`, `fair-price` |
| 5 | `heads-pairs` | Technical: expected head-then-head pairs in 100 flips (paper name: Prompt 5: technical) | 30 s | 90 s | 2 | `v5-heads-pairs`, `heads-pairs` |
| 6 | check `one-take` | I answered every prompt aloud, in one take each | | | | |
| 7 | check `marked-from-recording` | I marked each answer from my recording or a friend's notes | | | | |

5 prompts, 690 s = 11.5 minutes on the clocks, 2 checks. Every paper: `scoring` 1/0/0, `pass: 1`, `navigation: "forward"`, `skip: false`. Every item: difficulty 3, `tags: [family, "recorded-video"]`, `pace` = paper seconds, `seconds` = answer time, a 10-point rubric with one `required` time row and one filler-word row, a model labelled as an example with its word count and spoken time. No `followUps` (a one-way round has no interviewer). `requires: ["recruiting/l10-recorded-video"]`; style `research`.

Pass: the attempt passes when all five prompts reach 7 of 10 with the time row ticked and both checks are ticked. This is the author's line, not a published cut-off.

## Closest faithful version, and the engine gap that blocks it

- No microphone (DECISIONS, 29 Oct). The learner records on a phone or answers to a friend; the app times and gives the rubric.
- No thinking timer before an answer timer: each prompt is its own one-item paper, paper clock = thinking + answer time, which submits at zero (one take, no going back). The learner presses Start the clock when the thinking time is up; the amber last quarter falls inside the answer time.
- **Gap, Must:** an exam paper has no Mark my answer button for a longform item. Probed in Chromium on this mock (a real learner submitting all five papers scores 0 of 5; the results page shows each model and rubric locked at 0 of 10) and on `mock-superday-trader`. The playthrough passes only through the test hook. This mock cannot be passed by a real learner until the engine adds a marking step; bullet 1 in the inbox.

## Sources (what such rounds contain)

- `content/prep.json` (`asOf` 2026-10): JP Morgan official self-recorded video, reported three behavioural questions; Morgan Stanley official on-demand video; Goldman Sachs reported recorded video; IMC reported short recorded video in the first stage.
- `recruiting/l10-recorded-video`: about 30 s to prepare, about 2 minutes to answer, usually one take; 130 words a minute.
- Web, reported Nov 2026: [quantvault.org, JPMorgan HireVue video interview](https://quantvault.org/jpmorgan-hirevue-video-interview.html) (3 questions, about 30 s prep, 2 minutes at most, one retry); [Glassdoor, J.P. Morgan internship interviews](https://clear.glassdoor.nl/Interview/J-P-Morgan-Internship-Program-Interview-Questions-EI_IE145.0,10_KO11,29.htm) (no redo on most questions).
- Firm names appear only in `models` and `description`, with "reported, as of Nov 2026" (the check script asserts it).

## Numbers, each computed twice

| Place | Value | Route A (build) | Route B (check) |
| --- | --- | --- | --- |
| Clocks | 150, 150, 150, 120, 120 s; 690 s; 11.5 min | 30 + answer per prompt; sum | `minutes` × 60 = 30 + `seconds` = `pace`; Fraction sum = 23/2 |
| Models | 195, 185, 194, 115, 113 words; 90, 85, 90, 53, 52 s | `split()`, `round(Fraction(w·60, 130))` | regex `\S+`, integer half-up rounding |
| Prompt 1 | 20 × 6 = 120 problems; medians 23 and 15 inside the 25-minute limit | product | sum of six 20s |
| Prompt 2 | 1.1 × 0.9 = 0.99, a 1% loss; averaged 0% | Fractions; 100 → 110 → 99 | Decimal |
| Prompt 3 | 6 + 3 + 3 = 12 h, 12 − 3 = 9; 40/6 ≈ 6.7, 10/3 ≈ 3.3, 0 per hour | Fractions | Decimal |
| Prompt 4 | (10 + 4)/6 = 14/6, about £2.33; £2.50 − £2.33 = £1/6, about 17p; 600 × 1/6 = £100; £10 − £2.50 = £7.50 | Fractions over the six faces | Decimal |
| Prompt 5 | 100 − 1 = 99 pairs; 1/2 × 1/2 = 1/4; 99 × 0.25 = 24.75 | Fractions and a sum of 99 indicator means; brute force on 12 flips gives 11/4 | exact counting over all 2^12 flips, Decimal product |

The check script also confirms that every number in every prompt, model, rubric row, title, check, the description and `models` belongs to the set computed for that place, then runs `check_wrongs()` (no `wrong[]` here) and `report()`.

## Results

- Validator: `node tools/validate.mjs` 0 errors; no warning names `mock-video`.
- Voice scan on a copy (`VOICE_BASE` = scratchpad folder holding only `mock-video.json`): 0 sentences over 20 words, 0 explanations over three sentences (also 0 over 19).
- `python3 -I docs/briefs/mocks-scripts/mock_video_check.py`: 155 of 155, exit 0. The build script's asserts pass.
- `node tools/fresh-check.mjs --exam mock-video --min-run 10`: 0 hits. Grep of the key nouns: "find hardest" appears only in a recruiting homework-3 list of questions to ask an interviewer; after the fix pass the technical prompts are new setups (a die paying £10 and £4; head-then-head pairs in 100 flips) on expectation, the one topic every path naming the mock reaches, and no longer repeat algo-think `l9-halving`. The `puzzles` dice-game and `l3-waiting-for-hh` lessons share the topic, not the wording. The bank `video-answer` family (`behavioural-2..4`) is near prompt 3: one prepared story answers both. Prompts avoid the recruiting course's team, challenge, why-this-role, project, failure, decision, disagreement and learn-fast prompts and the superday fit and case papers.
- Playthrough `--exam mock-video`: ok, 5 of 5, passed; mock checks ok. With `--mobile`: same, all passed.
- Screenshots looked at (scratchpad `exam-mock-video/`): start card at 1280 and 440 (description, Models line, part cards; the 440 part cards wrap narrowly, inbox bullet 4), prompts 1 and 5 with the 2:00 and 1:30 clocks at 1280 and 440, the checks page at 440, the results page passed (1280) and as a real learner (0 of 5, models and rubrics shown locked). No overlap or sideways scroll.
- `node tools/readiness-sums.mjs`: OK after updating the four hand-written rows and `--write`.

## Proposals

- No `prep.json` change (the entries exist). No `course.json` change.
- Engine: inbox bullets 1 (Must, marking in exam papers) and 2 (Should, thinking timer and a locking answer clock) are what make this mock usable and faithful.

## Build script

`docs/briefs/mocks-scripts/mock_video_build.py` (committed beside `mock_video_check.py`) holds every prompt, rubric, model and timing; read it there. Fix pass 6 Nov 2026: see `docs/reviews/review-exam-mock-video.md`.
