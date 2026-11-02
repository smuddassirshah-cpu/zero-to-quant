# Topic 0.7 (Getting hired): second-reader findings

Scope: every lesson, review and homework file in `app/content/courses/recruiting/` (l1 to l15, review-1 to review-3, homework-1 to homework-3) and `app/content/exams/topic-0.7.json`.
Method: every stated number recomputed twice in Python (date differences with `datetime` and by month sums; pay by weekly, monthly and annual routes; $(1-p)^n$ directly and through `exp(n ln(1-p))`; guess values as fractions; the reroll game, the coupon count and the best-of-200 Sharpe by numerical integration of the normal maximum); every model answer's stated word count and speaking time recounted; dated facts checked against 2 November 2026 and across lessons, reviews, homework and the exam; claims checked against `docs/briefs/recruiting.md` (fact table F1 to F18) and DECISIONS (firm names, 2 Nov); distractor values re-derived from their `why`; tolerances checked for correct roundings; style scanned with a script (`style.py` in the reviewer's scratchpad: exclamation marks, dashes, money symbols, American spellings, firm names outside l4, sentences over 20 words, explanations over three sentences). Playthrough with `--local-cdn` and `--mobile` screenshots: l1, l3, l4, l6, l7, l9, l11, l13, l14, review-1, homework-3 and the exam all pass; screenshots looked at for the hooks, the tables and the calendar canvases.
Format: `path | screen/item | severity | what is wrong | fix`. Severity: error = wrong number, false claim or wrong grading; warning = weak explanation, overstated claim, grading that rejects a defensible answer, or a binding-rule breach; note = style.

All stated numbers check, including every date count from 2 November 2026 (6, 13, 29, 34, 62, 69, 238 and 241 days), every pay figure (£43,500, £12,500, £11,538, £10,385, £23,077 to £32,308, £27,692), every $(1-p)^n$ value, every guess value, 4.25, 14/3, 14.7, 1/221 and the "best of 200 near 1.6" claim (2.746 / √3 = 1.585). All model word counts match their stated counts (85, 80, 86, 207, 174, 150, 169, 155, 169, 155, 147, 62 and 64 words). No exclamation marks, no em-dashes, £ throughout (dollars only in the US comparison). Levels 2 and 3 and the exam name no firm.

## Level 1

- app/content/courses/recruiting/l5-a-target-list.json | screens[2] canvas row 5 | error | "Banks' quant research summers: usually for Final-year and Master's students." Bank summer internships are for penultimate-year students; a final-year undergraduate graduates before the summer (l3 and the exam's Omar item both teach penultimate year). | "Penultimate-year and Master's students".
- app/content/courses/recruiting/l3-the-calendar.json | screens[7] | warning | Amir's keyed answer is "September and October 2027, the first weeks of the course", but the canvas shows the 2028 window open from July 2027 and the lesson has just taught rolling review: he can apply from July, before the course starts. The "never" why ("Master's students apply ... in their first weeks") also ignores that a one-year MSc's summer is its dissertation term. The extra sentence about a four-year MMath is a second edge case in one screen. | Key "From July 2027, as postings open, and no later than his first weeks"; why for "never": "Many one-year MSc students intern in the summer; check the course allows it." Move the MMath sentence to the explain or drop it.
- app/content/courses/recruiting/l4-firm-by-firm.json | screens[1] | warning | The order key forces "Online assessment" before "Recorded video or recruiter call", but the screen's own table shows both in one first stage for JP Morgan and Goldman Sachs, and some bank videos come first. The byKey "The video or recruiter call follows the online test" states it as a rule. | `"same": [["oa", "vid"]]`, and byKey "The online test and the video often come together, straight after the application."
- app/content/courses/recruiting/l5-a-target-list.json | screens[8] | warning | One-word status for a sent application accepts "Applied", "applied", "sent" but rejects "Submitted" and "Done", equally right in one word. | Add "submitted", "done" and "sent 1 nov" to `accept`.
- app/content/courses/recruiting/l1-three-roles.json | screens[5], screens[6] | warning | Names Goldman Sachs, Morgan Stanley, IMC and SIG. DECISIONS (2 Nov) and the review brief: firms are named only in l4. | screens[5]: "Some banks call their desk quants strats (l4, as reported October 2026)." screens[6] canvas: "A trading firm's trader-intern posting, official, October 2026" and "Another trading firm's listing, October 2026"; explain "Two trading firms state ... (l4 sources)".
- app/content/courses/recruiting/l2-kinds-of-firm.json | screens[1] to [6], screens[8], summary.ideas[2], quiz[2] | warning | 45 firm names (examples column, pay sources, return rates, offices, Citadel and Citadel Securities). Same rule. | Replace names by type: "one high-frequency firm, London", "a market maker", "a top trading firm"; the Citadel trap becomes "a hedge fund and a market maker that share a name (l4)". Move the named examples column and the office table into l4 if they must stay.
- app/content/courses/recruiting/l3-the-calendar.json | screens[3], screens[4], screens[8] | warning | Names Barclays, BlackRock, UBS, JP Morgan, Jane Street, Point72 and Optiver. Same rule. | "A bank's off-cycle programme", "a first-year programme at a trading firm", and so on; keep the dates, which carry the teaching.
- app/content/courses/recruiting/l5-a-target-list.json | screens[0], [1], [4], [6], [8] | warning | 36 firm names in the target-list tables and the Discover and INSIGHT screen. Same rule. | Rows as "Trading firm A, first-year programme | First-years, UK | 8 Nov 2026" with the caption's sources kept; the real list is the learner's own in homework 1.
- app/content/courses/recruiting/review-1.json | items[1], items[4], items[5], items[8] | warning | Firm names (Jane Street, Optiver, Point72, Citadel, JP Morgan, Goldman Sachs, Morgan Stanley). items[5] also introduces Jane Street facts that l4 does not hold (mental maths without paper, dice games, making markets, video rounds) and cites "interview-gaps analysis", an internal document the learner cannot see. | Name firm types; take items[5]'s process from l4's row only, or invent "Firm T"; source line "candidate reports gathered for l4, October 2026".
- app/content/courses/recruiting/homework-1.json | items[0], [1], [3], [4], [6], [7] | warning | Firm names in the model answers and four items. items[4] adds SIG facts absent from l4 ("Quantitative Evaluation", multi-stage items, a poker and decision-theory round, a rival "16 questions in 20 minutes" report). | items[3], [6], [7]: "one trading firm's official 8-month rule (l4)", "a bank's third-party close date", "a trading firm's Amsterdam internship". items[4]: use only l4's row (17 questions, 60 minutes, calculator) or an invented firm. Models: name firm types; the learner's own list may name firms.
- app/content/courses/recruiting/l5-a-target-list.json | screens[4] explain | note | "no 2027 date was published by 29 October 2026": every other date count uses 2 November. | "when checked on 29 October 2026", or "by 2 November 2026" if re-checked.
- app/content/courses/recruiting/l3-the-calendar.json | screens[6] | note | `target: 2, tol: 3` accepts days 0 and 1 (2 and 3 November), before the CV is ready on 4 November. | `target: 3.5, tol: 1.5` (4 to 5 November).
- app/content/courses/recruiting/review-1.json | items[3] | note | `target 8.5, tol 1` with `snap 0.5` accepts 7.5 (mid-February). | `target: 8.75, tol: 0.75` (8 to 9.5, March to mid-April).
- app/content/courses/recruiting/l1-three-roles.json | screens[2] option `dev` why | note | "Researchers code, but in Python and on data" overstates: research at many trading firms uses C++. | "Researchers code, but on data questions, not on systems."
- app/content/courses/recruiting/l2-kinds-of-firm.json | screens[0] canvas row 3 | note | "Trading firm, trading" joins one firm's reported pay (£43,500) to another firm's return rate (70% to 80%), so it reads as one firm's figures. | Caption: "Each row combines reports from different firms of that kind."
- app/content/courses/recruiting/l2-kinds-of-firm.json | quiz[3] | note | Repeats screens[1]'s question word for word. | Ask instead "Whose money does a hedge fund invest?" or give a new firm description.
- app/content/courses/recruiting/homework-1.json | items[0] and items[1] models | note | The same invented candidate sends FOCUS "5 Nov" in the target list and finishes it "on 4 November" in the calendar. | One date in both.
- app/content/courses/recruiting/l2-kinds-of-firm.json | screens[0] explain, screens[2] explain | note | Four sentences each (limit three). | screens[0]: merge the last two ("The insight week leads at most to an interview; the job offer at the end is a **return offer**."). screens[2]: merge the two checks.
- app/content/courses/recruiting/l3-the-calendar.json | screens[4] explain | note | Four sentences. | "November has 28 days left after the 2nd, so 6 December is 28 + 6 = 34 days away and 3 January 28 + 31 + 3 = 62."
- app/content/courses/recruiting/homework-1.json | items[7] explain | note | Four sentences. | Merge "June adds 28, so 238" into the December-to-May sentence.

## Level 2

- app/content/courses/recruiting/l6-one-page-cv.json | screens[0] | error | "Tap the four lines an interviewer could not test" keys the skills line, but screens[6] (the trap) teaches that a listed language is exactly what an interviewer tests, and the byKey for r10 says the line "invites six questions". As worded, the keyed set is wrong for r10. | Question: "Tap the four lines that give Sam nothing to defend." Explain: "... state adjectives, a duty, a padded list or a cliché."
- app/content/courses/recruiting/l10-recorded-video.json | screens[1], screens[11] | error | "The format is reported for a bank's recorded round in l4" and "A bank's recorded round is reported to ask three questions of these kinds (l4)". l4 shows only "recorded video"; it never gives 30 s to prepare, 2 minutes, one take or three questions. The learner is told to find a source that is not there. | Add the reported format (F11: three behavioural questions, about 30 s to prepare, about 2 minutes, one take, October 2026) to l4 screens[0]'s JP Morgan row or a new l4 screen; until then cite "candidate reports, October 2026" here without "l4".
- app/content/courses/recruiting/l6-one-page-cv.json | screens[5] | warning | Prose says "Sam has no finance job yet worth leading with", but the canvas shows his data internship at an asset manager, which screens[2] made his strongest line. Experience before projects is then equally right, and the key rejects it. | Prose "Sam's projects show more of what the role tests than his internship"; or `"same": [["proj", "exp"]]` with the explain "Projects or experience, whichever shows more of the role, comes second."
- app/content/courses/recruiting/l9-sitting-an-assessment.json | screens[0] card `paper` | warning | "Scrap paper?" in Do is ambiguous: read as "paper on the desk" it belongs in Do not for a proctored test that bans it, which screens[6] and the byKey ("Some tests allow scrap paper and some do not") both allow. | Card "Check paper rule".
- app/content/courses/recruiting/l8-why-this-firm.json | screens[9] canvas and option `spec` | warning | "Hedge fund: Holds positions for days or weeks" is labelled "(l2)", but l2 says nothing about holding periods, and many quant funds trade intraday. The keyed answer rests on it ("A fund holds for weeks"). | Column header without "(l2)"; row "Hedge fund (research) | Tests ideas for weeks before they trade"; keyed answer "... A research role spends weeks before an idea trades."
- app/content/courses/recruiting/l9-sitting-an-assessment.json | screens[4] | note | "When is a guess worth making" keys the break-even case ("costs nothing on average"), which is not worth making in expectation. | "From when does a guess stop costing marks on average?"
- app/content/courses/recruiting/l6-one-page-cv.json | quiz[2] | note | The question line is two statements with no question. | Add "What do you do with Rust on the CV?"
- app/content/courses/recruiting/l7-projects-that-count.json | screens[9] | note | Options (100, 45, 260, 585) are not ordered but `shuffle` is off. | `"shuffle": true`.
- app/content/courses/recruiting/l7-projects-that-count.json | screens[2], screens[11]; homework-2.json items[4]; homework-3.json items[0] | note | The same momentum project is long-only ("Buy the top tenth") in l7 screens[2] but long-short ("sold the bottom tenth") in l7 screens[11] and homework-2, and uses monthly prices everywhere except homework-3 ("20 years of daily prices"). | One method: "bought the top tenth and sold the bottom tenth", monthly prices, in all four.
- app/content/courses/recruiting/homework-2.json | items[4] model | note | Section labels say 15, 30, 45 and 30 s, but at 130 words a minute the sections hold 12, 25, 34 and 25 s (207 words, 1:36). | "(about 12 s)", "(about 25 s)", "(about 34 s)", "(about 25 s)", or one line: "the same shares, scaled to 96 s".
- app/content/courses/recruiting/l10-recorded-video.json | screens[4] explain; screens[6] option `a` why | note | The explain says the 30 seconds are "for choosing and noting", while the `choose` distractor says spending them choosing is the slip. Story A's why "the setback was not hers" is weak: she led the team that hit the missing data. | Explain "... so the 30 seconds are for picking one and noting three words." Why: "It answers teamwork; the setback in it is the team's, not a failure of hers."
- app/content/courses/recruiting/l8-why-this-firm.json | screens[1] prose; l9-sitting-an-assessment.json summary.ideas[1] | note | 24 and 21 words. | Split after "evidence", and "At +1 and −1 with four options, a guess is worth −1/2, −1/3, 0 or +1. It rises as you rule options out."
- app/content/courses/recruiting/homework-2.json | items[0] to [4] models | note | Eight sentences of 21 to 47 words, mostly the "Why it scores 10" lines. | Break each "Why it scores" line into a short list.

## Level 3

- app/content/courses/recruiting/homework-2.json | items[5] model, answer 2 | warning | Nadia's challenge story is "failed a probability exam with 38% ... 74% in the resit", but the same invented candidate's exam story is 52% then 71% in l10 screens[6], l11 screens[4] and homework-3 items[1]. Also l10 screens[6] calls 52% "failed", which is a UK pass (homework-3 rightly frames it as missing her 70% aim). | homework-2: "In January I scored 52% on a probability exam, against a 70% aim." and "71% in June". l10 screens[6] row B: "52% against a 70% aim; new revision plan; 71% in June", as in l11.
- app/content/courses/recruiting/l8-why-this-firm.json | screens[5]; l10-recorded-video.json screens[6], screens[11]; l13-the-final-round.json screens[10] | warning | Nadia's evidence drifts: she built "an options pricer ... checked against 200 quoted prices" (l8, l10 story C), but her CV in homework-2 lists only a dice market simulator, and l13's keyed reply calls the dice simulator "a pricing tool". | Add the options pricer to the homework-2 CV model, or make l8 screens[5] and l10 story C the dice market simulator; l13 key "A pricing tool for one product, like my options pricer but tested on live quotes".
- app/content/courses/recruiting/l11-stories-that-answer.json | screens[5] row Contest | note | Prefilled "Deadline: Yes" for the trading-game story, whose cue words hold no deadline; the hint says "look for a date". | Cue words "Trading game, one afternoon; chose half size with data missing", or the cell "No".
- app/content/courses/recruiting/l12-reasoning-aloud.json | screens[8] canvas | note | The number line runs 1 to 6 for the reroll game while the question is a £2 to £10 game. | Labels 0 to 12 with the allowed band 2 to 10 and a point at 11, or no canvas.
- app/content/courses/recruiting/l14-offers-and-deadlines.json | screens[1] prose | note | "old, but the pattern holds" is an unsourced claim. | "old; Quantt's UK guide (2026) reports one to two weeks."
- app/content/courses/recruiting/review-3.json | items[8] | note | "her chance" has no antecedent. | "Ten of Ella's rejections came after ..."
- app/content/courses/recruiting/l13-the-final-round.json | screens[0] prose | note | 22-word sentence. | "Nadia has four 45-minute rounds. Probability is at 9:30, market making at 10:30, coding at 11:30 and behavioural at 13:30."
- app/content/courses/recruiting/homework-3.json | items[0] to [5], items[8] models | note | Twelve sentences over 20 words, most the shared "Why it scores 10" line (40 words). | Write it as a list of the seven rubric points.

## Exam (topic-0.7)

- app/content/exams/topic-0.7.json | items[1] option `b` why and explain | warning | "A hedge fund ... holds positions for days or weeks" overgeneralises, as in l8 screens[9]. | Why: "You picked a fund. A hedge fund invests outside investors' money, and a research intern tests ideas before they trade." Explain: drop "holds positions longer".
- app/content/exams/topic-0.7.json | items[21] feedback.correct | note | "the bank's quant research summer" can be read as r7 ("Quant research summer 2027", closed). | "the London research summer and the bank research summer."
- app/content/exams/topic-0.7.json | items[19] explain, items[26] prose, items[28] model (d) | note | 21, 22 and 23-word sentences. | Split at the colon in each.

## Layout (playthrough screenshots)

- app/content/courses/recruiting/l3-the-calendar.json | screens[0] | warning | The five draggable steps start at months 0 to 2 in steps of 0.5, so the dots overlap into one blob and the five stacked labels do not line up with their dots, on desktop and at 390 px (the axis has about 13 px a month). The learner cannot tell which dot is "Apply". | Park the points apart, for example at 0, 2, 4, 6 and 8 with `labelPos` alternating above and below, or start them on a second row.
- app/content/courses/recruiting/l9-sitting-an-assessment.json | screens[0]; l1-three-roles.json screens[0] | warning | At 390 px the `boxes` canvas scales the card text to about 7 px; "Scrap paper?" and "Phone on desk" touch their borders. | Deck `cols: 1` so the canvas grows taller rather than narrower, and two-word labels; raise an engine bullet for a minimum card font on `boxes`.
- app/content/courses/recruiting/l7-projects-that-count.json | screens[0] | note | The `pair` stack draws Entry A narrower and centred, Entry B full width, so the two read as different kinds of thing. | Give both sides the same table width (engine) or pad Entry A's rows to similar length.
- (engine) every lesson screen at 390 px | note | The left-edge rail handle overlaps the first letters of the question line (seen on l14 screens[3] and exam items[21], [25] and [28]). | ENGINE-BACKLOG: inset the handle or add a 16 px left gutter at narrow widths.
- app/content/courses/recruiting/l4-firm-by-firm.json | screens[4] row 2 | note | Jane Street's first round reads "dice and card games" and keys Probability Puzzles, while review-1 items[5] lists making markets in the same rounds. | Cell "Phone rounds: dice and card probability", and keep review-1 to l4's facts.

## Counts

3 errors, 17 warnings, 29 notes.

## Fix pass

Targeted string edits only; no file was regenerated, and no lesson, screen or item id changed. I recomputed every number I touched (Python `datetime` and `fractions`, a word count of each edited model answer, and the brief's games with an iterated-deletion and indifference script in the scratchpad folder `fix-0.7`). A style script over every recruiting file and the exam finds no exclamation mark or em-dash. It also finds no new sentence over 20 words outside quoted CV lines, and no explanation over three sentences. A firm-name scan finds no firm outside l4 in levels 1 to 3, the reviews, the homework or the exam.

Firm policy (DECISIONS, 2 Nov). Level 1 now names firms by type. Where one lesson compares several, it uses letters kept the same across l2, l5 and homework 1: trading firm A, market maker B, hedge fund C, trading firms D and E, hedge fund F, research firm G. Two items that only worked with a firm name now use invented firms: the shared-name trap and quizzes use Firm H or Firm K with "Firm K Securities", pointing to the real pair in l4. Review-1 items[5] uses Firm T and homework-1 items[4] uses Firm S. Every keyed answer is unchanged.

Status: fixed 48, disputed 0, deferred 1 (an engine change). Where a fix differs from the proposal, the line says why. Screen, item and quiz numbers are zero-based, as in the findings.

### Level 1 (20)

1. l5 s2 row 5 (error): fixed, "Penultimate-year and Master's students". The same claim was in the exam's `e-target-rows` row r5 ("Penultimate or final year" for a bank research summer). That row now reads "Penultimate year; London"; the keyed rows r2 and r5 still hold for Omar. No other summer-internship row says final year. The two off-cycle rows (l3 s3, l5 s0) keep "penultimate or final year", which is what those real off-cycle postings say.
2. l3 s7 Amir: fixed as proposed. Key "From July 2027, as postings open, and no later than his first weeks"; the `never` why is the proposed line. The MMath sentence left the prose; the explain keeps it in its third sentence, so it is still three sentences.
3. l4 s1 order: fixed, `same: [["oa", "vid"]]` and the proposed `vid` line. The `oa` line no longer states an order either.
4. l5 s8 status: fixed, `accept` gains "sent 1 nov", "submitted" and "done".
5. l1 firm names: fixed as proposed. The s6 explain also points to l4 for the rounds.
6. l2 firm names: fixed. The examples column became firm types, and the pay rows "High-frequency firm" and "Market maker". The return-rate and office tables use letters, and the Citadel trap uses invented Firm H. The summary idea and quiz[2] now say "a hedge fund and a market maker can share a name". I moved nothing into l4: the arithmetic and the reading of reports are the teaching, not the names.
7. l3 firm names: fixed with firm types ("A UK bank", "Trading firm, first-year programme"). Every date and day count is unchanged.
8. l5 firm names: fixed with the letters above and firm types. The caption keeps its sources without firm domains. Keys r0 to r4 and r0, r4 are unchanged.
9. review-1 items[1], [4], [5] and [8]: fixed. Items[5] is now invented Firm T, so it no longer adds facts l4 lacks. The "interview-gaps analysis" source is gone. Items[8] uses Firm K.
10. homework-1: fixed. The models name firms by type and letter and say the learner's own list names them. Items[3] now states the 8-month rule in the prose, because the stem no longer names the firm; the key (mid-March 2028) is unchanged. Items[4] is invented Firm S, built only from the stated stages. Items[6] and [7] use "a large bank" and "a trading firm".
11. l5 s4 explain: fixed, "when checked on 29 October 2026 it had no 2027 date".
12. l3 s6: fixed, `target 3.5, tol 1.5`. Correction to the proposal: this accepts days 2 to 5 from 2 November, which is 4 to 7 November, not "4 to 5 November". It matches the hint "day 2 to 5".
13. review-1 items[3]: fixed, `target 8.75, tol 0.75`. With snap 0.5 it accepts 8, 8.5, 9 and 9.5: March to mid-April. Mid-February (7.5) now fails.
14. l1 s2 `dev` why: fixed as proposed.
15. l2 s0 caption: fixed, "Each row combines reports from different firms of that kind".
16. l2 quiz[3]: fixed with a new firm description (an invented firm that trades only its own capital). The option ids and the key `prop` are unchanged.
17. homework-1 models: fixed. Both now send firm A's application on 4 November, as l5 s8 does.
18. l2 s0 and s2 explains: fixed, three sentences each.
19. l3 s4 explain: fixed with different wording. The proposed single sentence runs to 22 words, so the explain is three sentences: "So 6 December is 28 + 6 = 34 days away, and 3 January 28 + 31 + 3 = 62."
20. homework-1 items[7] explain: fixed, three sentences. Checked: 2 November 2026 to 28 June 2027 is 238 days = 34 weeks.

### Level 2 (13)

21. l6 s0 (error): fixed with different wording. "Nothing to defend" does not fit r10 either: a six-language list gives Sam too much to defend. The question is now "Tap the four lines with no evidence behind them". The prose and hint say the same, and the explain names "adjectives, a duty, a padded list or a cliché". The key is unchanged.
22. l10 s1 and s11 (error): fixed with the proposal's interim option. Both screens and the s1 explain now cite "candidate reports, October 2026" without "l4". l10 itself states the format (30 s, 2 minutes, one take, three questions), so l4 was not extended.
23. l6 s5: fixed with the proposed prose, "Sam's projects show more of what the role tests than his internship".
24. l9 s0 card: fixed, "Check paper rule". The hint now says "check the paper rule".
25. l8 s9: fixed as proposed. The column header has no "(l2)", the row is "Hedge fund (research) | Tests ideas for weeks before they trade", and the keyed text ends "A research role spends weeks before an idea trades."
26. l9 s4: fixed, "In a test that allows skipping, when does a guess stop costing marks on average?"
27. l6 quiz[2]: fixed, adds "What do you do with Rust on the CV?"
28. l7 s9: fixed, `shuffle: true`.
29. Momentum method: fixed. Every version now buys the top tenth and sells the bottom tenth on monthly prices: l7 s2 row and homework-3 items[0] ("monthly prices", "and selling the losers", and the look-ahead fix "lagging the signal by one month"). l7 s11 and homework-2 already said so. Homework-3 items[0] is now 178 words, about 1 minute 22 seconds (82.2 s), and its header says so.
30. homework-2 items[4]: fixed, labels "about 12 s", "about 25 s", "about 34 s" and "about 25 s" (26, 55, 73 and 54 words after item 33's split). The total is 208 words, 96 s, so "about 210 words: 1 minute 36 seconds" stands.
31. l10 s4 and s6: fixed as proposed (the explain and story A's why).
32. l8 s1 prose and l9 summary idea 2: fixed, both split as proposed.
33. homework-2 models: fixed. Each "Why it scores 10" line is a list. The other long sentences are split. Items[1] and [3] keep 85 and 86 words; items[2] is now 81 words and its header says "About 81 words".

### Level 3 (8)

34. Nadia's exam story: fixed. Homework-2 items[5] is now "In January I scored 52% on a probability exam, against a 70% aim", then three timed past papers a week and 71% in June. l10 s6 row B is "52% against a 70% aim; new revision plan; 71% in June", as in l11, l13 and homework 3. The option, the feedback and s11 now say "the exam below her aim", not "the failed exam". Review-2's anonymous 38% / 74% answer is not Nadia's, so it stays.
35. Nadia's evidence: fixed by adding the options pricer to her homework-2 CV ("Options pricer, Python, Jan 2027 ... checked it against 200 quoted prices"), since l8 and l10 lean on it. l13 s10's key is "A pricing tool for one product, like my options pricer but tested on live quotes". Its hint is "Her CV has an options pricer".
36. l11 s5 Contest: fixed, cue words "Trading game, one afternoon; chose half size with data missing" in both tables. The nudge hint also says "time limit". Deadline stays Yes.
37. l12 s8: fixed. The number line now runs £0 to £12, with "Pays £2 to £10" as a closed band and a point at £11.
38. l14 s1: fixed, "(... April 2004). That source is old; Quantt's UK guide (2026) reports one to two weeks."
39. review-3 items[8]: fixed, "Ten of Ella's rejections came after the same market-making round."
40. l13 s0: fixed as proposed.
41. homework-3 models: fixed. The shared "Why it scores 10" line is a seven-point list in six models, and the final-plan line is a list too. Long sentences in items[0], [2], [3] and [4] and in the final plan are split. Items[2] and [4] are now 168 and 170 words (both about 1 minute 18 seconds); items[3] keeps 155.

### Exam (3)

42. items[1] `b` why and explain: fixed as proposed. "Holds positions longer" is gone.
43. items[21] `feedback.correct`: fixed, "the London research summer and the bank research summer".
44. items[19], [26] and [28] (d): fixed. Items[19] now reads "the retry waits 8 months, from 20 November 2026 to 20 July 2027". Items[26] now opens "This is a line on your CV." Items[28] (d) is split after "the clock starts".

### Layout (5)

45. l3 s0: fixed. The steps start at months 0, 2, 6, 8 and 10 with labels alternating above and below. Each start is outside every target's tolerance, and 4 stays clear of Today at 4.03. The 390 px screenshot shows five separate dots with readable labels.
46. l9 s0 and l1 s0 cards: fixed in two ways. l9's deck is `cols: 1` with "Check paper rule" and "Phone visible", and every label now fits its card at 390 px. On l1, `cols: 1` made the four containers fit one row and shrank the cards further (screenshot), so the deck stays at three columns. Its labels became two words ("Quote prices", "Clean data", "Fix crashes"). An engine bullet for a minimum card font is in `docs/BACKLOG-INBOX.md`.
47. l7 s0: fixed in content. Entry A's rows are padded ("Momentum backtest, a personal project, spring 2027"; a longer tool list), so both tables now draw full width at 390 px. An engine bullet for equal pair widths is in the inbox.
48. Rail handle over the question line: deferred. It is an engine change; the bullet is in `docs/BACKLOG-INBOX.md`.
49. l4 s4 row 2: fixed, "Phone rounds: dice and card probability". Review-1 keeps to l4's facts by using invented Firm T (line 9 above).

### Answer check (answers-2026-11-02.md), 6 applied

- homework-3 `hw3-final-plan`: the model now gives two questions for each round (8 in all), so it meets the rubric line. Its "Why" line says "two questions for each round".
- topic-0.7 `e-cycle-plan` (c): now "four options each". The −0.5 holds: 1/4 − 3/4.
- topic-0.7 `e-target-rows`: as item 43.
- game-theory brief, L1 l2: the drill falls "in three rounds", with a round defined as deleting every move strictly dominated at that point. The worked 3 × 3's round count is keyed 3 (C; then M and B; then R). Checked: drill T; then L and C; then M.
- game-theory brief, L1 review: the checked replacements. Mixed (2, 0), (0, 3) / (0, 2), (1, 0) has no pure equilibrium, with Ana T 2/5 and Ben L 1/3. Saddle rows (5, 7), (2, 3) have value 5 at row 1, column 1.
- game-theory brief, L2 review: two fifths of the average, level 2 = 50 × (2/5)² = 8; five bidders ±£9, overshoot 9 × 4/6 = £6; three rounds at δ = 0.7, Ana keeps 1 − 0.7 × 0.3 = 79%. The "Number checks" rows now read "in 3 rounds" and list 2/5 and 1/3, saddle 5, 8, 6.00 and 0.79.

### Acceptance

From `app/`, with `--local-cdn`:
- `node tools/validate.mjs`: 0 errors (385 warnings, none in recruiting or topic-0.7).
- `--lesson`: l1 to l15 all pass, and l11 to l15 also pass with `--mobile`. l15 had no edits and was run for the check. 390 px screenshots of l1, l3, l7, l9 and l12 were looked at.
- `--set`: review-1, review-3, homework-1, homework-2 and homework-3 pass.
- `--exam topic-0.7`: 30 of 30, passed.

Graded answers changed: two tolerances (l3 s6 target 3.5 ± 1.5; review-1 items[3] 8.75 ± 0.75) and one accept list (l5 s8); one order gains a `same` group (l4 s1). Every keyed option, row, cell and number is otherwise unchanged. Not changed: `course.json`, any id, engine files, `prep.json`.
