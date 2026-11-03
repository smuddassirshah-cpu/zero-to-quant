# Engine pass B: interview bank (E7), per-item timing (E9) and `tags`

Items 456 to 458 in `docs/ENGINE-BACKLOG.md` (status block "Engine pass B: status"). The five inbox bullets (E7, E9 and three on `tags`) were moved out of `docs/BACKLOG-INBOX.md`.

## Items

- **456 (E7), the bank and the Interview practice deck.** `content/bank/<family>.json` is listed in the manifest and loaded through `ZQ.content.bankIds()` and `bank(id)`. A card on Review (data-sec `bank`, hidden until the pool is not empty) says how many questions are due and new, from how many families, how many are scheduled later and how many still unlock with lessons. It links to `#bank`, a set page (`mountBank` in `review.js`, reusing `setPage` and `runSet`) of 8 questions from `ZQ.select.bankDeck`. Each item has its own Leitner schedule in the saved state: `doc.bank[uid] = { box, due, seen, miss, last, secs, at, family }`. A new item starts in box 1; a right answer moves it up (1, 3, 7, 30 days), so a first right answer returns in 3 days; a miss goes back to box 1, due in 1 day. A bank miss does not join the redo queue (nothing is scheduled twice). The deck takes due items first (oldest due first), then new ones, one family at a time (round robin, then no two neighbours from one family when avoidable). An item whose `requires` lessons are not all finished is never drawn. Tagged quiz, review and homework items of finished lessons feed the deck under their own uid; this was cheap because it filters the existing practice pool on `tags`. Old saves have no `bank` or `timing`; `fresh()` and `normalise()` default both, so they load unchanged (checked in the playthrough by deleting both keys and importing). Right answers move skill scores and the streak count as practice does (no XP, no MP).
- **457 (E9), per-item timing and `pace`.** `runSet` stamps `seconds` on each checked result (shown to checked time); the exam screen counts the time each question is open (back and forth adds up). `ZQ.mock.pacing` builds one line: average, slowest families (top three by mean seconds, by first tag, else first skill, else `mental-arithmetic` for a generated item) and items over `pace`, naming each ("question 2, 3 min 20 s against 45 s"). It is on every set summary (practice, weekly, level review, redo, bank) and on the exam result (also each question's "34 s of 45 s pace"). Exam attempts keep `itemSeconds`; `ZQ.state.timing.families[family] = { n, seconds, over }` is a running log from exams, mocks, practice and the bank deck. Optional `pace` (positive seconds) on any item, lesson screen or drill, validated. Grading, XP, mastery and pass marks never read time.
- **458, `tags`.** Defined in AUTHORING sections 2 and 5; the validator checks it on lesson screens, quiz, review, homework, exam, mock and bank items and drills. No existing content file failed the new rules.

## Files changed

Engine: `app/js/state.js` (bank, timing, `bankResult`, `logTiming`), `app/js/content.js`, `app/js/engine/select.js`, `app/js/engine/mock.js` (`pacing`, `family`, `fmtSeconds`), `app/js/engine/player.js` (`seconds` on set results), `app/js/screens/review.js` (card, `#bank`, pace line), `app/js/screens/exam.js` (per-question time, result line), `app/css/screens/review.css`, `app/css/screens/exam.css`. Tools: `app/tools/validate.mjs`, `app/tools/playthrough.mjs`. Docs: `docs/AUTHORING.md`, `docs/ENGINE-BACKLOG.md`, `docs/BACKLOG-INBOX.md`. Content: only the new `app/content/bank/sample.json` (the manifest is rewritten by the validator).

## Author-facing fields

`tags` (list of kebab-case family names, family first), `pace` (seconds), bank files with `role`, `style`, `source`, `requires`. Full text in AUTHORING section 5 and the "Bank, tags and pace rules" paragraph of section 7.

## The sample bank

`bank/sample.json`, ten items adapted from mm-games, puzzles, mental-pressure, counting-chance and markov level reviews, seven families. Every numeric answer was checked a second time away from the source (brute force or exact fractions, `engine-pass-b/check_bank.py` in the scratchpad): 20 sevens; E|X-Y| of two dice 70/36 = 1.9444; about 70,000 coins to the mile (160,000 / 2.3 = 69,565, and 1,609.344 m / 2.25 cm = 71,526); E[max of three dice] 4.9583; 12 H12 = 37.2385; 58 x 34 = 1972; 0.042 / 0.0007 = 60; 1 - (5/6)^3 = 0.4213; 1 / (1 - 0.75) = 4 days; exactly one fixed point among six = 264/720 = 0.3667. One item (`one-fixed-point`) carries `requires: ["counting-chance/l1-every-outcome"]` so the locked path is exercised.

## Playthrough

The checks run under **`--routes-only`** (no new flag), after the routes: `bankChecks` and `paceExamChecks` in `app/tools/playthrough.mjs`. `Date.now` is skewed from the tool so an item can "take" 200 s and schedules can move by days without waiting. It checks: the Review card (new count, locked line, start link, no sideways scroll); the draw excludes the locked item; families are mixed; a deck sitting (every item right, seconds on each result, a pace line with the average, the slowest families and exactly one item over pace, and the return-day note); the schedule (every item in the 3-day box, due 3 days ahead, seconds kept, per-family timing logged); a miss (box 1, due in 1 day); two days on only the missed item is due; forty days on everything is due; an old save without `bank` or `timing` loads and still works. Then one exam (`mock-sample`, else `topic-1.5`) is sat with one question taking 90 s: the result has the pace line and per-question seconds, the attempt keeps `itemSeconds` of the right length, family timing is logged, and the marks are untouched.

Results (from `app/`, with `--local-cdn` set to the scratchpad `pkgs`):
- `node tools/validate.mjs`: 0 errors.
- `node tools/playthrough.mjs --routes-only` (bank deck and timing checks included): All passed, at 1280 px and with `--mobile`.
- `--exam mock-sample --exam topic-1.5 --set mm-games/review-1 --lesson mm-games/l1-unknown-quantity`: All passed, with and without `--mobile` (mock-sample 11 of 11, net 14 of 14; topic-1.5 30 of 30).
- Full coverage in four shards (899 lessons in three, then every review and homework set and all 21 exams in one): all passed, 0 failures. Warnings in the validator are the existing not-yet-written notes.

## Screenshots

In `engine-pass-b/shots/` of the scratchpad: `hub-bank-*`, `hub-bank-due-*`, `bank-start-*`, `bank-done-*`, `bank-done-pace-*` and `exam-result-*`, each as `light` and `dark` at 1280 and 390 px, inspected. Two defects found and fixed from them: the start button in the card had dark text on a dark ground (the section needed `data-track`), and over-pace items were numbered with a bare digit (now "question 2"). In the test the exam's "Time used" badge reads 0:01 against a pace line of minutes only because the tool skews `Date.now` and the exam clock reads `performance.now`.

## Follow-ups

1. SM-2 with a self-rated ease (the brief offered it as an alternative); not built.
2. Fold the weekly problems into the deck after topic 3.3 starts (E7 text); not built.
3. `timed` on a deck; the set page already supports it, a bank file has nowhere to put it.
4. Tagged lesson screens (drill and follow-up screens) in the deck: the redo resolver already reads screens by ref, so the pool needs a screen branch only.
5. A readiness view over `ZQ.state.timing` and `doc.bank` (E18); timing is not stored for reviews, redo or homework.
6. A family registry to check a tag against: today a misspelt family is a valid kebab word. The content tags written so far (`cv-lines`, `dice-ev`) have no common list.
7. The real bank is a content pass: families, `role` and `style` per item, `requires` against the lesson ids.
8. A bank item's `tags` and the quiz item's `tags` share one family space, so a family spread over the bank and lessons is dealt as one family in the round robin.
