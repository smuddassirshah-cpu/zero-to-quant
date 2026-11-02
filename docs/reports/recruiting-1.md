# Report: recruiting level 1 ("The landscape")

Status: done. As-of date for every stated date count: **2 November 2026**. The coordinator moved it from 29 October 2026 after a container restart, so every day count in the brief was recomputed from 2 November (table below). The JP Morgan 1 November 2026 date is now taught as a date that has passed.

## Files written (`app/content/courses/recruiting/`)

| File | Contents |
|---|---|
| `l1-three-roles.json` | 10 screens (problem, problem, 4 ladder, trap, ladder, derive, transfer), 4 quiz items. Skill `rk-landscape`. |
| `l2-kinds-of-firm.json` | 10 screens (problem, problem, 4 ladder, trap, ladder, generalise with a task, transfer), 4 quiz. `rk-landscape`. |
| `l3-the-calendar.json` | 11 screens (problem, problem, 4 ladder, trap, 2 ladder, 2 transfer), 4 quiz. `rk-landscape`. |
| `l4-firm-by-firm.json` | 10 screens (problem, problem, 3 ladder, trap, ladder, 2 transfer, source-rule problem), 4 quiz. `rk-landscape`, `rk-assess`. |
| `l5-a-target-list.json` | 9 screens (problem, problem, 3 ladder, trap, ladder, generalise with a task, transfer), 4 quiz. `rk-landscape`, `rk-apply`. |
| `review-1.json` | 9 items, difficulty 2 to 4, interleaving l1 to l5 (choice, numeric, drag-point on the calendar, multi). No longform. |
| `homework-1.json` | 8 items, difficulty 3 to 5: dated target list (longform, 5), two-cycle calendar (longform, 4), summer-cycle `order` with one distractor (3), Optiver retake choice (4), SIG preparation multi (4), spread numeric (4), passed-deadline choice (3), days-to-start numeric (3). |

Generators and helper scripts are in the scratchpad folder `recruiting-1` (`common.py`, `l1.py` to `l5.py`, `sets.py`, `lint.py` for sentence length and dashes, `numbers2.py`, `scroll.mjs` and `model.mjs` for scrolled 390 px screenshots).

## Validator and playthrough

- `node tools/validate.mjs`: **0 errors**; no warnings on any recruiting level 1 file (the only recruiting warning is "not yet written" for levels 2 and 3).
- `node tools/playthrough.mjs --lesson recruiting/<id> --local-cdn <pkgs>`: l1 14 checks, l2 14, l3 15, l4 14, l5 13; every quiz 4/4; all passed. `--set recruiting/review-1`: 9 of 9 recorded, passed. `--set recruiting/homework-1`: 8 of 8, 41 of 41 marks, passed.
- Screenshots: every screen at 1280 and 390 px with `--mobile` and `--why`, plus scrolled 390 px captures of the l4 firm table (1,388 px tall inside a 330 px scroll box), the l5 programme table, and both homework model answers. Layout faults found and fixed: role-table cells too long (shortened); "Hedge a position" card overflowing (now "Hedge risk"); five calendar handles parked on one spot (now spaced 0.5 apart at the left); interval labels colliding with bars on stacked rows (all windows now on row 1 with no time overlap per screen); 4-column tables overflowing at 390 px in the l5 hook, the l5 transfer table widget and the homework model answer (all cut to 3 columns); daily ticks on a 70-day line (now weekly).

## Deviations from the brief

- Today is 2 November 2026, not 29 October: FOCUS is 6 days away (not 10), Point72 13 (not 17), Optiver FutureFocus 34 (not 38), Jane Street 3 January 62 (not 66); 1 July 2027 is 241 days, 34 full weeks and 3 days (the l3 numeric answer is 34, not 35). The review's deadline item answers 13.
- l3 hook uses `snap: 0.5` (not 1) so the test at 12.5 and the offer at 16.5 can be placed exactly; tolerance stays 1 month.
- l5 hook has 10 programmes, not 12: the fact table supports eligibility for only these ten. Jane Street INSIGHT and Discover Citadel Securities sit on the ladder screen instead, so the hook's answer is unambiguous.
- l5 tables and the target-list model use 3 columns (firm folded into the programme name), because 4 columns of ordinary text scroll sideways at 390 px.
- l1 has no `generalise` screen (no honest KaTeX rule exists for roles); its `derive` screen is an `order` with a distractor. l4 has none either; its summary formula is a set union of stage tests.

## Firm facts used (all "as reported" unless "official"; dates and sources as shown in the lessons)

| Fact | Where | Date | Source line in the lesson |
|---|---|---|---|
| F1, F2 cycle shape: postings July and August, rolling review, offers late October to mid-December, 1 to 2 week deadlines | l3, review, homework | 2026 | QuantVault internship timeline 2027; Quantt UK guide |
| F3 spring weeks: first-years of three-year or second-years of four-year degrees; apply Sep to Jan; run Mar and Apr | l3, review | 2026 guides | Warwick Business School blog; the-trackr |
| F4 off-cycle examples (Barclays 3 to 6 months; BlackRock six months, penultimate; UBS closed 30 Sep 2026), official postings | l3, l5 | Oct 2026 | search.jobs.barclays, careers.blackrock.com, targetjobs.co.uk |
| F5 first-year and diversity deadlines (FOCUS 8 Nov; INSIGHT, FTTP, Bridge 3 Jan; FutureFocus 6 Dec; Point72 15 Nov) | l1 hook, l3, l5, review, homework | checked 21 Oct 2026 | QuantVault early insight programmes page |
| F6 Discover Citadel Securities 2026 (deadline 13 Feb 2026, 24 to 27 Mar, first- or second-years in Europe), official; no 2027 date | l5 | 2026 event | citadelsecurities.com |
| F7 SIG Dublin and London summer 2027; Dublin discovery for second-years; no finance background needed | l1 trap, l2, l5 | Oct 2026 | efinancialcareers.com; careers-sig.icims.com |
| F8 IMC Amsterdam, start 28 Jun 2027, no finance knowledge needed, Netherlands work permission (official); no London intern postings (reported) | l1, l2, l5, homework | Oct 2026 | imc.com posting; Quantt tracker |
| F9 G-Research QR internship, Master's or above, "Ongoing" | l5 | Oct 2026 | gradcracker.com |
| F10 Optiver no retake within 8 months (official); 80 in 8 format and pass figures (reported, prep sites disagree) | l4, homework | Oct 2026 | optiver.com EU campus recruiting Q&A; QuantVault, Quantt |
| F11 JP Morgan QR coding challenge and recorded video (official, 2027 posting); London routes close 1 Nov 2026 (third-party, flagged) | l3, l4, review, homework | Oct 2026 | interview-gaps row; EP Advisory guide |
| F12 pay: HRT London £4,350 a week (TraderMath, 28 Sep 2026); Optiver London £10,000 to £14,000 a month (Quantt, summer 2026); London bank about £65,000 a year pro rata (2026 salary blog). All flagged third-party | l2 | Sep to Oct 2026 | as named |
| F13 return offers: Jane Street above 80%, Optiver 70% to 80%, Citadel 65% to 75%, banks about 50% (Quantt guides, no named sources, flagged) | l2 | 2026 | Quantt guides |
| F16 Citadel and Citadel Securities are separate firms with separate applications | l2, review | 2026 | as reported |
| F17 no finance knowledge needed (IMC, SIG); Jane Street reports no online test for traders | l1, l4, review | Oct 2026 | IMC and SIG postings |
| F18 US comparison; Jane Street FTTP New York 23 to 27 Mar 2026, London 7 to 11 Apr 2026 | l3 | 2026 | janestreet.com FTTP pages |
| interview-gaps section 1 rows (Optiver, Jane Street, SIG, IMC, Citadel Securities, Two Sigma, Citadel, JP Morgan, Goldman Sachs, Morgan Stanley), cut to a few words | l4 table, review, homework | Oct 2026 | Glassdoor, QuantVault, TraderMath, Quantt, firms' pages |

Every firm-fact screen tells the learner to check the firm's own page. No logos, styling or firm voice; Firm Q and the "London trading firm" are labelled invented. Model answers use an invented candidate (Nadia).

## Numbers (each computed by script, `numbers2.py`, and by hand)

| Number | Script | Hand check |
|---|---|---|
| 2 Nov to 8 Nov 2026 = 6 days; to 15 Nov = 13; to 30 Nov = 28 | date difference | same month subtraction |
| to 6 Dec 2026 = 34 | date difference | 28 + 6 |
| to 3 Jan 2027 = 62 | date difference | 28 + 31 + 3 |
| to 1 Dec 2026 = 29 (l3 quiz) | date difference | 28 + 1 |
| to 28 Jun 2027 = 238 = 34 weeks | date difference | 28 + 182 (Dec to May) + 28 |
| to 1 Jul 2027 = 241 = 34 weeks 3 days | date difference | 238 + 3 |
| £4,350 × 10 = £43,500 | product | £40,000 + £3,500 |
| £65,000 × 10/52 = £12,500 | product | £1,250 a week × 10 |
| £60,000 × 10/52 = £11,538.46 (l2 quiz) | product | £1,153.85 × 10 |
| £10,000 to £14,000 a month × 120/52 = £23,077 to £32,308 | product | 2.31 months × figures |
| £4,000 × 9 = £36,000; £3,000 × 10 = £30,000 | product | by hand |
| $0.95^{30}$ = 0.2146; $0.95^{15}$ = 0.4633 | power | ln 0.95 = −0.0513, × 30 = −1.539, e^ = 0.215 |
| $30 \times 0.05$ = 1.5; $15 \times 0.05$ = 0.75 | product | by hand |
| $0.9^{20}$ = 0.1216 (review); $0.9^{10}$ = 0.3487 (l5 quiz) | power | $0.9^5$ = 0.5905, squared 0.3487, squared 0.1216 |
| $0.92^{25}$ = 0.1244 (homework) | power | ln 0.92 = −0.0834, × 25 = −2.085, e^ = 0.124 |
| 8 months after 15 Jul 2027 = 15 Mar 2028; after 1 Dec 2026 = Aug 2027 | month count | by hand |

## Proposed course.json change

None.

## Backlog bullets added

Five bullets in `docs/BACKLOG-INBOX.md` under "Raised later (recruiting level 1):".
