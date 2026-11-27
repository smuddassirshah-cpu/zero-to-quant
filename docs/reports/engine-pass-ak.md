# Engine pass AK: strand `ai` (ENGINE-BACKLOG 1218, PLAN section 8 A1)

Spec: `docs/briefs/ai-strand-curriculum.md` "Engine work" item 0, finding F1.

## Decisions
- Topic mark: derived. A topic is an AI topic when all its courses are `ai` (`topicStrand(t) === 'ai'`, `H.aiTopic`). No topic field. A mixed topic is a validator error.
- "Quant path only" hides the AI strand as well (it is not quant path). Separate setting `aiStrand` (default shown) and `aiToday` (default off, inert while hidden).
- Settings are not added to `state.js` defaults: an absent key reads as the default, so no saved document changes.

## Changes
- `tools/validate.mjs`: accepts `ai`; mixed-topic error; readiness.json may not list an ai course; stage-exam skill pool excludes ai skills.
- `js/content.js`: `strandOfCourse`, `isHidden`, `aiShown`, `aiToday`, `pathTopics`; `readiness.plan` drops ai unless opted in; stage `hours` re-derived without ai topics. Badge "AI strand" (`css/components.css`), aria label in `learn.js`, switches in `you.js`, `today.js` fallback course never ai, `learn.js` exit card uses `pathTopics`.
- `js/hours.js`: `isAi`, `aiTopic`, `ai()`; stage, total, stage in-app and outside, and `roleSums` leave ai out; `stageHours` and `totalHours` take an optional skip.
- `tools/census.mjs`, `tools/curriculum-hours.mjs`: ai left out of every figure, one AI line only when an ai course exists. `tools/readiness-sums.mjs` skips ai courses.
- Fixture: course `ai-sample` (topic 1.12, stage 1) in `tools/fixtures/mini-app`. Test `tools/test-strand-ai.mjs` (41 checks).
- Docs: `docs/AUTHORING.md` section 9, ENGINE-BACKLOG 1218.

## Results
- `node tools/validate.mjs`: 0 errors. Census tail identical to before (lessons 1,236, levels 283, hours 3,695, gap 0); `curriculum-hours.mjs` output byte-identical to HEAD.
- `test-strand-ai`, `test-hours-split`, `test-capstone`, all 25 `test-validate-*`: pass.
- `curriculum-hours.mjs --check` FAILS at HEAD already (30 prose figures in `docs/curriculum.md` out of date, e.g. opening in-app 678 against 756); not caused by this pass, left for the owner of that file.

## Open
- Not done: Learn and Review lists show AI topics as normal rows; no AI-specific section. `docs/readiness.md` prose unchanged (ai is simply absent). Stage-exam `draw` sources (bank, problems) are not checked for ai origin.
