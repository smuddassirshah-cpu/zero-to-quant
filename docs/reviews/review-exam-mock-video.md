# mock-video: second-reader findings

Scope: `app/content/exams/mock-video.json` (five one-item `longform` papers: three behavioural at 30 s thinking plus 120 s answering, 2.5 min each; two technical at 30 s plus 90 s, 2 min each; 11.5 min in all; every paper `pass: 1`, scoring `1, 0, 0`, forward only, no skip; checks `one-take` and `marked-from-recording`), read in full against `docs/briefs/mocks.md` (`### Shared rules for the mocks` and `## mock-video`), `docs/reports/exam-mock-video.md`, `docs/AUTHORING.md` sections 5 and 6 (performance tasks, "Mock pass marks", voice), DECISIONS ("Performance tasks", "Self-marked results", 29 Oct no recording), `content/prep.json` (paths that name the mock), `recruiting/l10-recorded-video`, `algo-think/l9-halving`, `testing/l9-twenty-tests`, `testing/homework-3`, `bank/behavioural-1..4.json`, the superday fit and case papers, and the engine code the mock depends on (`js/screens/exam.js` `between()` and `submit()`, `js/engine/widgets/longform.js`, `js/engine/mock.js`).

The known engine bug (no marking step inside exam papers, so every prompt scores 0 in the real UI) is not reported again. The findings judge the mock as if the learner can tick each rubric after each paper.

Format: `n. paper [path] | severity | problem | evidence | fix`. Severities: wrong, misleading, coverage, design, voice, layout.

## Script results

- `python3 docs/briefs/mocks-scripts/mock_video_check.py`: `numbers_lib: 155 of 155 checks passed`, exit 0.
- Validator (from `app/`): `0 errors, 3978 warnings`; no line names `mock-video`.
- `node tools/fresh-check.mjs --exam mock-video --min-run 10`: `0 hit(s) in 1 target file(s)`.
- Voice scan on a copy (`VOICE_BASE` = scratchpad folder with only this file): 184 sentences, 0 over 20 words, 0 explanations over three sentences. No exclamation mark, no em-dash. KaTeX only in rubric rows 4 and 5 and model 5.
- My recomputation agrees with every stated number: clocks 150, 150, 150, 120, 120 s, sum 690 s, 11.5 min; amber at a quarter of each paper (37.5 s and 30 s, `exam.js` `LOWAT`), inside the answer time; $1.1 \times 0.9 = 0.99$; $6 + 3 + 3 = 12$, $40/6 \approx 6.7$, $10/3 \approx 3.3$; $100 \times 0.05 = 5$, $1 - 0.95^{100} = 0.99408$; $0.05/100 = 0.0005$; $\lfloor \log_2 10^6 \rfloor + 1 = 20$, $2^{20} = 1{,}048{,}576$, $2^{19} = 524{,}288$, $10^6 / 20 = 50{,}000$; word counts and 130-wpm times as labelled.
- Firm names appear only in `models` and `description`, both marked reported, Nov 2026.

## What the author's script does not check

- That story numbers agree with each other: it whitelists 25, 31 and 19 for model 1 without checking that a 31-minute median fits a 25-minute limit (finding 3).
- Whether each rubric row rewards something the prompt asks for (finding 11), and whether the model label fits a technical prompt (finding 4).
- Which courses each path that names the mock has met, against a pass rule that needs all five papers (findings 1 and 2).
- What the start card and the between-papers screen show before a clock starts (finding 6).
- Model length against the 10 + 80 + 30 s budget that `l10-recorded-video` teaches (finding 5).
- Freshness beyond the n-gram tool: the near-identical "A million prices" problem in `algo-think/l9-halving` and the `video-answer` family in `bank/behavioural-*` (findings 12 and 13).
- How the coming marking step and the zero-slack paper clocks interact (finding 8).

## Timings against the sources

- 30 s thinking and 120 s answering for prompts 1 to 3 match every source the brief cites: quantvault (about 30 s, at most 2 minutes), the recruiting course (about 30 s, about 2 minutes, usually one take) and the bank's own `video-answer` items ("thirty seconds to prepare and two minutes to answer").
- 90 s for prompts 4 and 5 is the mock's own choice. No source gives a time for technical prompts (finding 9).
- One take with no retry is stricter than quantvault (one retry) and matches Glassdoor (no redo on most questions) and `l10` ("Most platforms reportedly allow none"). Sensible for rehearsal.
- Five prompts sit at the top of the reported range of three to five; JP Morgan is reported as three.

## Findings

1. Prompts 4 and 5 [`parts[3]`, `parts[4]`, with the pass rule `passed = every paper passed && checksOk`] | coverage | Every learner must pass both technical prompts, but most paths that name this mock have met neither course. Prompt 4 needs `testing` (Bonferroni or FDR, a held-back check: 3 of 10 points), which only `oa-research` contains. Prompt 5 needs `algo-think` (what binary search is), which `oa-research` and `oa-strats` contain. A strats learner therefore sits a researcher prompt cold, and a general-path or firm-path learner sits both cold. | `prep.json` steps: `general` has neither `testing` nor `algo-think`; `oa-strats` has `algo-think` but not `testing`; `firm-imc`, `firm-jp-morgan`, `firm-goldman-sachs` and `firm-morgan-stanley` have neither. All seven name `mock-video` in `mocks`. `docs/readiness.md` lists it for Undecided (the general path). Without the testing course, prompt 4's best honest mark is 7 of 10, and only with $1 - 0.95^{100}$ done in the head. | Engine (raise in the inbox): a paper field such as `track: "research"` or `"strats"`, so the start card marks it "for researchers" and the pass rule counts a track paper only for a learner on that track. Content now, until it lands: replace the description sentence "Both state every fact they need." with "Prompt 4 assumes the testing course, and prompt 5 the algo-think course." and "Without them, expect those two papers to fail." (finding 2 covers the false claim).

2. Description [`description`] | misleading | "Both state every fact they need." is false. Prompt 4 does not state any fix for many tests, and the rubric gives 3 points for one; prompt 5 does not say what binary search does, and every content row depends on it. The brief says the same thing in its parts table note. | Prompt 4 text: "A colleague tests 100 trading signals at the 5% level. None has a real edge. Explain how many will look significant, and what you would do before trusting one." Rubric rows "Names a fix for many tests ... (2)" and "Names a check on data held back (1)". Prompt 5 text names "binary search" and nothing more. | Apply the two sentences in finding 1. Correct the matching line in the report.

3. Prompt 1 [`parts[0].items[0].model`] | wrong | The model says each problem has a 25-minute limit, then that the median time fell from 31 minutes. A median above the limit is impossible if the limit holds. | "Each week I solve 20 timed problems, with a 25-minute limit on each. ... My median time has fallen from 31 minutes to 19." The check script's allowed set for `v1-hardest-part` is `{20, 25, 120, 31, 19}`, so it never compares them. | Change the sentence to "My median time has fallen from 23 minutes to 15." The word count stays 147. Update `mock_video_build.py` and the allowed set in `mock_video_check.py` to `{20, 25, 120, 23, 15}`, and add an assert that both medians are at most the limit.

4. Prompts 4 and 5 [`parts[3].items[0].model`, `parts[4].items[0].model`] | misleading | The label "Your own story is the real answer, so use this for its shape." fits a behavioural prompt, not a technical one. Prompts 4 and 5 have no story; the numbers and the reasoning are the answer. | Both technical models open with the same label as prompts 1 to 3; `mock_video_check.py` line 68 forces one label on all five. | For prompts 4 and 5 use "*An example answer. Match its order and its numbers. It is 139 words, about 64 seconds at 130 words a minute.*" (138 words for prompt 5). Let `LABEL` in the check script accept either first sentence pair, keyed on the item's skills.

5. Prompts 1 to 3 [`parts[0..2].items[0].model`] | design | The behavioural models run 143 to 147 words, 66 to 68 s of a 120 s answer. The lesson this mock `requires` teaches a full two-minute budget, so a learner who copies the model's shape leaves about 50 s unused. | `l10-recorded-video`: "$10 + 80 + 30 = 120$ s ... At 130 words a minute the whole answer is about 260 words." Labels: 147 words, 68 s; 144, 66 s; 143, 66 s. The technical models (64 s of 90 s) are proportionate. | Lengthen each behavioural model to 195 to 215 words (90 to 99 s), adding to the story section, not the close. In the build script assert $85 \le s \le 105$ for 120 s prompts. If the length stays, add to the label: "A full answer can run to about 100 seconds."

6. Prompts 2 and 3 [`parts[1].name`, `parts[2].name`] | design | The paper names give away the questions before any clock runs. The start card lists every part name, and the between-papers screen shows "Next: Prompt 2: a mistake you found" with no time limit. So prompts 2 and 3 get unlimited thinking time, unlike the platform, where the question appears only when the 30 s start. | `exam.js` `between()`: `<h1 ...>Next: ${Z.esc(p.name)}</h1>` and "the next clock starts when you begin". Names: "Prompt 2: a mistake you found", "Prompt 3: more work than time". Prompt 1 ("motivation") and 4 and 5 ("technical, researcher", "technical, strats") name only the kind. | Rename to "Prompt 2: behavioural" and "Prompt 3: behavioural". Keep the paper ids and the item titles (shown only inside the paper).

7. All papers [`parts[*].items[0].prompt`] | design | The prompt says "When the thinking time is up, press Start the clock" but gives no way to see when 30 s have passed. The paper clock is the only running timer, and the learner must work out that 2:30 less 30 s is 2:00. | Prompt head: "Thinking time 30 seconds, then answer time 2 minutes, in one take. When the thinking time is up, press Start the clock and speak." | Replace the second sentence with "When the paper clock shows 2:00, press Start the clock and speak." (1:30 on prompts 4 and 5). Extend the check script's expected strings to match.

8. All papers [`minutes` 2.5 and 2, against `seconds` 120 and 90] | design | Each paper clock is exactly thinking plus answer time, with no slack. If the coming marking step opens inside the paper, before submit, a learner who speaks to the limit is auto-submitted with the item unmarked, which scores 0 (`submit()` turns a `pending` result into `ok: false`). Marking "from the recording" also needs a replay of up to 2 minutes. | `exam.js` `submit(timeUp)`: `if (!r || r.pending) r = { ok: false, key: null };`. The paper clock cannot be lengthened without breaking the one-take timing. | Engine: open the marking step after the paper submits, outside its clock, either on the between-papers screen or on the results page. Content, once that lands: add to the description "Mark each answer after its paper ends, from the recording."

9. Top level [`models`, `description`] | misleading | `models` ascribes "short technical prompts" to the four firms' rounds, and the description gives 90 s for technical prompts beside the reported timings. No cited source gives technical prompts for these firms or any time for them. JP Morgan is reported as three behavioural questions; technical prompts are "on some platforms", per the recruiting course. | Brief sources: "JP Morgan ... reported as three behavioural questions"; "prompts are behavioural, motivation and, on some platforms, short technical questions". `models`: "Timed behavioural, motivation and short technical prompts." | `models`: "Reported, as of Nov 2026: one-way recorded video rounds at JP Morgan, Morgan Stanley, Goldman Sachs and IMC. Timed behavioural and motivation prompts; some platforms add technical ones." Description: "Prompts 4 and 5 are our own short technical prompts, with 90 seconds to answer."

10. Top level [`description`] | design | The description states the pass line but not that it is the author's. AUTHORING says the description, not only the report, must say so. | AUTHORING "Mock pass marks": "the description says so and calls it illustrative: firms do not publish cut-offs." Description: "Each answer needs 7 of 10, with its time row ticked." | Add after it: "This pass line is ours; firms do not publish one."

11. Prompt 4 [`parts[3].items[0].rubric[2]`, `prompt`] | design | Row 3 (2 points) rewards the chance of at least one false pass, which the prompt does not ask for. It also needs $0.95^{100}$ done mentally to "about 99.4%", with no calculator, in 30 s. A learner who answers exactly the question asked starts 2 points down. Prompt 5's row 4 (scan comparison, 1 point) has the same gap but costs less. | Prompt: "Explain how many will look significant, and what you would do before trusting one." Row 3: "Says at least one false pass is almost certain: $1 - 0.95^{100}$, about 99.4%". | Ask for it: end the prompt with "How many will look significant, and how likely is at least one? What would you do before trusting one?" (12 and 8 words). Loosen the row to "... $1 - 0.95^{100}$, over 99%". Keep the model's 99.4%.

12. Prompt 5 [`parts[4].items[0]`] | design | The prompt restates `algo-think/l9-halving`'s problem "A million prices" (a million prices, 20 looks, against a million for a scan), so an `algo-think` learner recites the lesson's answer. The report says the algo-think million-price setups "are about memory and pointers, not search", which is wrong. | `l9-halving` problem title "A million prices"; feedback "Twenty looks, against a million for a scan."; explain "$\lfloor \log_2 n \rfloor + 1$ looks. For a million that is $19 + 1 = 20$." | Either keep it as deliberate rehearsal and correct the report, or move to 4,000,000 prices: at most 22 comparisons; halving gives 2,000,000 then 1,000,000; $2^{22} = 4{,}194{,}304 \ge 4{,}000{,}000$, and 21 is not enough as $2^{21} = 2{,}097{,}152$; a scan needs up to 4,000,000, over 180,000 times as many ($4 \times 10^6 / 22 = 181{,}818$). Recompute all of these twice in the build script.

13. Prompt 3 [`parts[2].items[0]`] | design | The bank already holds a `video-answer` family (three items, `pace` 150, "thirty seconds to prepare and two minutes to answer"), so the brief's reason for fixed prompts ("no bank family holds recorded-video prompts") does not hold. Prompt 3 is also close to two bank prompts, so one prepared story answers all three. | `bank/behavioural-2.json` `video-answer-what-sets-you-apart`; `bank/behavioural-3.json` `video-answer-biggest-strength`; `bank/behavioural-4.json` `video-answer-under-pressure` and `star-story-short-handed-deadline` ("a deadline and not enough people"). | No change to the mock now. Correct the report's freshness line to name these, and raise a later item: draw one behavioural prompt from `bank/behavioural` tag `video-answer` once drawn longform items can carry `seconds`.

14. Prompt 2 [`parts[1].items[0].model`] | misleading | A fund moving +10% and then −10% on consecutive days is implausible, and an interviewer would notice. "Averaged two daily returns to get the two-day return" is an odd slip; the common one is adding them. Both give 0% here, so the story still works with the realistic version. | "a report on two funds. My teammate averaged two daily returns to get the two-day return. One fund rose 10% and then fell 10%". | "a report on two small-cap shares. My teammate added two daily returns to get the two-day return. One share rose 10% and then fell 10%". The word count becomes 145, so the label reads "145 words, about 67 seconds" ($145 \times 60 / 130 = 66.9$). Update the build script.

## Not findings

- Rubrics: every row is 10 points in total, the time row is required on each, and every row can be ticked honestly from a phone recording. The filler row and the time row need the recording or a friend's notes, which is what the `marked-from-recording` check asks for. The rubric stays hidden until marking (`longform.js` phase 2), so rows 1 of prompts 4 and 5 do not give the answer away.
- Pass rule: 7 of 10 with the time row, on each prompt, is sensible for self-marking, and the results are stored `how: self`, so they gate nothing. The only problem is finding 1.
- The two checks ask for what the app cannot see: no restarts, and marking from what was said.
- The superday fit and case papers and the recruiting prompts do not overlap prompts 1 to 4. Prompt 4 rehearses `testing/homework-3`'s Bonferroni bar for 100 tests (0.0005), which is fair on the researcher path.
- Layout: nothing new beyond the report's inbox bullet 4 (part cards wrap narrowly at 440 px).

## Engine items this mock needs

- A per-paper track flag, so a track's technical paper counts only for that track (finding 1).
- The longform marking step after a paper submits, outside its clock (finding 8). This is part of the known bug's fix.
- Minor: the marking panel says "Tick each point your working shows" on an aloud item; "your answer shows" would fit a spoken answer.

## Fix pass

I recomputed every number before writing it. Fractions, Decimal and brute force over all 2^12 flips agree: clocks 150, 150, 150, 120, 120 s (690 s); medians 23 and 15 inside the 25-minute limit; $(10+4)/6 = 14/6 \approx 2.33$, the loss at 2.50 is $1/6 \approx 17$p, $600/6 = 100$; $99 \times 0.25 = 24.75$. Models now run 195, 185, 194, 115 and 113 words (90, 85, 90, 53, 52 s at 130 words a minute). Common ground for the technical prompts: `closure.mjs --target mock-video` gives only `recruiting`; the seven paths' own references add random-vars level 2 on every path (`puzzles/level-1` and `mm-games` require it for JP Morgan, Goldman Sachs and IMC). Both technical prompts therefore use expected value and indicators only.

Status: fixed 12, disputed 0, deferred 2 (finding 8, and the bank draw in finding 13; the engine track field in finding 1 stays in the inbox).

1. Coverage: fixed in content. Prompts 4 and 5 now draw on random variables expectation only (a die game, head-then-head pairs), reached by every path.
2. Description "Both state every fact they need": fixed. Replaced by "Prompts 4 and 5 are our own short technical prompts ... They need only expected value, from the random variables course." The report's matching claim is corrected.
3. Prompt 1 median above the limit: fixed, 23 minutes to 15; the check script asserts both medians are at most the limit.
4. Technical model label: fixed. Prompts 4 and 5 read "Match its order and its numbers."; the check script keys the label on the kind of prompt.
5. Behavioural models too short: fixed, 195, 185 and 194 words (90, 85, 90 s); both scripts assert 85 to 105 s for 120 s prompts, and every model within the answer time at 150 words a minute.
6. Paper names: fixed. "Prompt 2: behavioural", "Prompt 3: behavioural", "Prompt 4: technical", "Prompt 5: technical"; both scripts assert the name shows only the kind.
7. Start-the-clock cue: fixed. "When the paper clock shows 2:00 (1:30), press Start the clock and speak." Both scripts check the string.
8. Zero-slack clocks and the marking step: deferred (engine). The inbox bullet for marking in exam papers stands; the description line about marking after the paper waits for that change.
9. `models` and the 90 s claim: fixed. `models` states the reported format and "some platforms add technical ones"; the description calls prompts 4 and 5 our own.
10. Pass line is ours: fixed, "This pass line is ours; firms do not publish one."
11. Prompt 4 rubric versus prompt: fixed by replacing the prompt. Every content row now has a key noun in its prompt, asserted by both scripts (the review's script gap).
12. Prompt 5 repeats "A million prices": fixed by replacing the topic; no binary search content remains. The report's freshness line is corrected.
13. Bank `video-answer` overlap: docs fixed (report and brief name the family); drawing from the bank is deferred to the inbox as the review proposes.
14. Prompt 2 fund story: fixed, "two small-cap shares", "added two daily returns"; the table still shows 0% for +10% then -10% added.

New script checks: story numbers agree (prompt 1 medians and weekly total, prompt 3 hours), key noun per rubric row, model length at 150 words a minute and the 85 to 105 s budget, label per kind, paper names, clock cue, description and `models` claims.

Gates:

- Validator: 0 errors, 3978 warnings, none names `mock-video`.
- Voice scan on a copy: 0 sentences over 20 words, 0 explanations over three sentences; no exclamation mark, no em-dash.
- `mock_video_build.py` asserts pass; `mock_video_check.py` 211 of 211, exit 0.
- `fresh-check.mjs --exam mock-video --min-run 10`: 0 hits.
- Playthrough `--exam mock-video`: 5 of 5, passed, mock checks ok; with `--mobile`: same.
- `readiness-sums.mjs`: OK.
