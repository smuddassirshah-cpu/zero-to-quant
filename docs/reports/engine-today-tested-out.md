# Engine: Today pinned to a tested-out course (ENGINE-BACKLOG 461)

## Reproduction
Playwright (Chromium, `app/` served with python http.server, setup flag set, profile startStage 0), script at `/tmp/claude-0/-home-user-zero-to-quant/4b8cce5e-d242-5446-84a4-7179e480b15a/scratchpad/engine-today/repro.mjs`. The pass is seeded with `ZQ.state.examFinished({ id: 'topic-0.1', passed: true, ... })`, the same call the exam screen makes (`exam.js` line ~459), so case (c) is the same stored shape; the exam screen itself was not driven.

| Case | Before | After |
|---|---|---|
| a. 0.1 passed, part-open number-sense lesson | "Jump back in", Number Sense, exam card "0.1 passed" (BUG) | "Start here", Equations and Inequalities, exam card 0.2 |
| b. 0.1 passed, nothing open | Equations and Inequalities, exam 0.2 | same |
| control. not passed, part-open | Number Sense, exam 0.1 | same |
| d. passed, lesson position saved after the pass | (not run) | Number Sense resumes, exam card 0.1 passed (deliberate revisit) |

## Cause
`currentCourse` (today.js, learn.js, course.js) returned `sum.resume.course` before the `courseTestedOut` filter, and `renderToday` took `curItem` from `sum.resume`. Any unfinished lesson in a passed topic therefore pinned it. `passed` storage was correct.

## Change
- `app/js/content.js`: `resumeStands(resume)`, exported. A resume in a tested-out course stands only if `resume.at` is later than the latest passing attempt.
- `app/js/screens/today.js`, `learn.js`, `course.js`: `currentCourse` also requires `C.resumeStands(sum.resume)`; Today's `resume` variable uses it too.
- No progress data touched; the lesson stays reachable on Learn. No AUTHORING change.
