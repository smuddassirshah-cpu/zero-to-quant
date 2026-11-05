# Engine pass: items 10 and 11 (duration honesty, workload single source)

PLAN 2c items 10 (F07) and 11 (F09). ENGINE-BACKLOG 556 to 563. Branch `worktree-agent-a4bee5463e0a0cd15`. Nothing under `app/content/` was edited in the worktree.

## Item 10: duration honesty

- Lesson `session` (`short` default, `workshop`, `project`). Validator: enum check, and `minutes` must fit: short 5 to 20, workshop 20 to 90, project 60 to 240. I kept the brief's ranges: the data has workshops of 25 to 60 minutes and no project. The old "10 to 15" rule is replaced.
- `manifest.json` gains `sessions` (`course/lesson` to `{ session, minutes }`, workshop and project only), so the app knows without opening every lesson.
- Matcher `app/tools/duration-prose.mjs`, five variants, first two screens' `prose`. Rates ("every 5 minutes") and offsets ("10 minutes later", "5-minute bars") are ignored; so is anything under 20 minutes (item times such as "two minutes a question"). Pattern and false positives are in `docs/AUTHORING.md` section 1.
- Warning `duration-prose` when the stated figure differs from `minutes` by more than 5. Shipped content: 8 warnings (the same 8 the narrow pattern of the review found), 0 after the content script on a scratch copy.

Hit counts (read-only, `node app/tools/duration-prose.mjs`), lessons in brackets:

| Filter | First screen | First two screens |
| --- | --- | --- |
| every match | 42 (32) | 60 (39) |
| minus rates and offsets | 42 (32) | 60 (39) |
| and 20 minutes or more | 18 (16) | 23 (19) |
| and differing from `minutes` by more than 5 | 17 (15) | 22 (18) |
| and not on the ignore list | 17 (15) | 22 (18) |

By variant, first two screens, 20 minutes or more: `digits-min` 16, `words-hour` 6, `digits-hour` 1, `words-min` 0, `half-hour` 0. Without the 20 minute floor `words-min` has 27 hits and `digits-min` 26, all item times. After the ignore list, 8 lessons warn before the script and 0 after. The review's "13" does not reproduce: 22 raw hits fall to 8 true ones once data durations are named.

### Hand-read decisions (every hit's context was read)

True hits, set by `app/tools/apply-item10-content.mjs` (nine lessons):

| Lesson | minutes | session | Prose |
| --- | --- | --- | --- |
| coding-int/l17-two-in-sixty | 14 to 60 | workshop | "This lesson budgets one hour for two problems" |
| contests/l13-virtual-contest | 15 to 60 | workshop | "four problems in 60 minutes ... set a 60-minute timer outside the app" |
| research-int/l1-two-regressions | 15 to 25 | workshop | "This lesson takes about 25 minutes" |
| research-int/l2-correlation-limits | 15 to 30 | workshop | "about 30 minutes" |
| research-int/l3-estimators-on-the-spot | 15 to 35 | workshop | "about 35 minutes" |
| research-int/l4-tests-in-words | 15 to 25 | workshop | "about 25 minutes" |
| research-int/l5-matrices-on-the-spot | 15 to 20 | short | "about 20 minutes" (gap is 5, so the validator never warned; set for honesty) |
| research-int/l14-house-price-case | 15 to 50 | workshop | "about 50 minutes with the code screens" |
| research-int/l19-timed-data-task | 15 to 25 | workshop | "A 25-minute task" |

False positives, named in `app/tools/duration-prose-ignore.json` with reasons (ten), not changed:

- **coding-int/l15-reading-an-assessment** (13 vs 60): the review's pair. 60 and 62 minutes are the assessment the learner triages, the data of the problems (the canvas says "Assessment of 65 minutes"). The lesson is a 13 minute triage exercise. Disagree with the review here; if the main session wants it a workshop, move it from the ignore file to `TRUE` in the script.
- coding-int/l19-a-live-round: 45 minutes is the reported length of the round the lesson models.
- contests/l14-which-first: a two-hour round and solving times of 10 to 50 minutes are scoring data. (The review's "contests/l13 15 vs 60" is real and is set.)
- contests/l16-upsolving: "two hours free this week" is the scenario.
- functions/l12-graphs-that-tell-stories (25 minutes of Sam's walk), limits/l17-somewhere-in-between (3 hours, an hour), limits-thm/l3-rare-events (an hour as a rate unit), mental-pressure/l11-word-problems (2 h 38 min journey), puzzles/l16-meeting (one hour interval), recruiting/l13-the-final-round (four 45-minute interview rounds in the story).

The script refuses to run (exit 1, "UNDECIDED") if the matcher flags a lesson on neither list, so a future hit is decided by a person.

Cards: Learn course card shows "Workshop, 60 min" (coding-int, contests) or "6 workshops, 25 to 50 min" (research-int) and says so in its accessible name; the course page row shows "Workshop, 25 min"; the lesson sheet and the title screen use the same label. Checked in Chromium on the scratch copy (coding-int card "Workshop, 60 min"; research-int card "6 workshops, 25 to 50 min"; six row tags; no page errors). Note: these workshop lessons open on a problem screen, not a title screen, so the player's title-screen label only shows on lessons that author a `title` screen; the sheet on the course page is the start screen they actually have. The contests card sits in stage 2 and was not captured; it uses the same code path.

## Item 11: workload single source

`app/js/hours.js` (`ZQ.hours`; `require` from node like `prereq.js`; loaded in `index.html` before `content.js`).

- API: `build({ curriculum, courses, written, sessions, minutes })` gives `lesson`, `level`, `course`, `courseWritten`, `topic`, `stage`, `total`, `roleSums`, `topicFromMinutes`; plus `stageHours`, `totalHours`, `months`, `sessionLabel`, `courseSessionLabel`, `role` (reads a role's totals from `readiness.json`).
- Contract kept: topic hours stored; shared across courses and lessons by weight. Weight is 1 for a short lesson, `minutes / 14` for a workshop or project. With no workshop the shares equal the old mapped-lesson counts, so `readiness.json` is byte-identical until item 10's script runs. Item 10's minutes flow through the weight: a topic total never moves, a workshop takes a bigger share.
- `readiness-sums.mjs` now gets its hours from it (`tools/hours-source.mjs` reads the files). After item 10's script on the scratch copy, role totals move by a few hours (up to about 8, for example 1,645 to 1,653 on one header), and `readiness-sums.mjs` exits 0 (the item 10 script regenerates `readiness.json` and the md blocks itself).
- Stage hours: derived at load in `content.js`, stored field ignored. Validator no longer requires it and warns when present (4 warnings until the script runs). `apply-item11-content.mjs` deletes the four stage-level lines (text edit, idempotent, validated as JSON before writing).
- Stage cards, Learn header and months agree: 555, 1,650, 940, 550 = 3,695. The hard-coded months table in `learn.js` (8, 21, 12, 6, which disagreed with curriculum.md's 9, 25, 14, 8) is replaced by `ZQ.hours.months` (9, 25, 14, 8). Prepare paths show no hours, so nothing there could disagree.
- `docs/curriculum.md`: marked block `<!-- generated:hours -->` written by `node app/tools/curriculum-hours.mjs --write`; `--check` also compares the opening totals, map rows and stage headings. The quant-path figures changed: the doc said 1,490 and 3,495 from a hand split of 30 h for vector calculus in 1.11; the contract's lesson share gives 33.5 h, so they are now 1,487 and 3,492. Flag for the user if the hand figure is preferred.
- Census last line: `Hours: stored stage total 3695, summed topic total 3695, gap 0` with or without the stored field; a preceding line says whether the legacy field is present (3,265, ignored) or absent.
- Topics 3.2 and 3.4 store 0 hours. Not invented. From lesson minutes: 3.2 has 46 lessons written, about 11 h (46 x 14 min); 3.4 has 30 lessons mapped and none written, about 7 h at 14 min. Both are lesson-time floors and far below the 150 to 250 h of comparable topics, which include practice. Shown beside the 0 in the curriculum.md block.

## Verification

From `app/`, local CDN `/tmp/claude-0/-home-user-zero-to-quant/e8dab463-5c35-50a7-b6b4-37dc6e82e1ac/scratchpad/pkgs`. The playthrough serves the `app/` its own script sits in, so "content" is chosen by running the scratch copy's `tools/playthrough.mjs` (no `--content` flag exists).

Scratch copy (`.../scratchpad/scratch`, both content scripts run, a second run changes nothing):

- `validate.mjs`: 0 errors, 0 `duration-prose` warnings.
- `readiness-sums.mjs`: exit 0. `census.mjs` last line: gap 0, legacy field absent. `curriculum-hours.mjs --check`: OK.
- `playthrough.mjs --routes-only`: All passed; `--routes-only --mobile`: All passed.
- `--lesson` on the nine changed lessons plus `coding-int/l15-reading-an-assessment`: all ok (quiz 4/4 each).

Worktree, scripts not run: `validate.mjs` 0 errors (2,116 warnings: 8 `duration-prose`, 4 stage hours); `readiness-sums.mjs` exit 0 and `readiness.json` unchanged; census gap 0 with the legacy-field line; `curriculum-hours.mjs --check` OK; `test-met-rule`, `test-validate-perf`, `test-validate-versions` pass; new `test-validate-session.mjs` 32 of 32; `--routes-only` with and without `--mobile` All passed.

`test-validate-why.mjs` FAILS in the worktree with "no cross-course string requires entry to test". It reads content only and none of my files touch it: since item 7 every cross-course edge is an object, so the case it needs no longer exists. Pre-existing; it needs a fixture (not fixed here).

Not run: full `--all` (as instructed).

## Commands for the main session

From the repo root after merging the branch:

```
node app/tools/apply-item10-content.mjs        # nine lessons; regenerates readiness.json and docs/readiness.md blocks
node app/tools/apply-item11-content.mjs        # removes stage hours from curriculum.json
node app/tools/validate.mjs 2>&1 | tail -3     # 0 errors; rewrites manifest.json with `sessions`
node app/tools/readiness-sums.mjs              # exit 0
node app/tools/curriculum-hours.mjs --check
node app/tools/census.mjs | tail -3
```

The manifest must be regenerated (the validator does it) before the app shows workshop labels.
