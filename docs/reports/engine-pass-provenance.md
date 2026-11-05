# Engine pass: result provenance (PLAN 2c item 3, N01)

Summary. Graded rows now carry `how` (auto, self, external). Longform items and the mock and stage tick-box checks are self; all else is auto. `rate()` sends self rows to `state.selfMarked` and leaves `skills[s]` alone; they earn no MP or item XP. You shows a "Self-marked" block outside the mastery map. Prerequisite met reads `passedAuto`, stored at finish on exam attempts and review records, so self rows and checks never meet a level. Old saves import unchanged; old aggregates cannot be split. A provenance check sits in `--routes-only`. Verification results are in the hand-back.

## Changes
- `app/js/state.js`: `howOf`, `isSelf`, `provenance(item)`, `selfRec`; `itemsOf` passes `how`; `rate(..., { how })`; quiz, review, homework and exam loops skip MP and item XP for self rows; `reviewFinished` stores `passedAuto`; `examFinished` takes `passedAuto` and `checks` and stores them on the attempt; `doc.selfMarked` default and `ZQ.state.selfMarked` getter.
- `app/js/screens/review.js`: `resultRow` and the homework submit rows set `how` from `provenance(item)`.
- `app/js/screens/exam.js`: rows carry `how`; `passedAuto` is the pass over auto items per paper (self items dropped from both sides, `passNet` scaled, a paper with no auto item skipped, none at all means false); checks stored as self.
- `app/js/engine/widgets/longform.js`: `grade()` returns `how: 'self'`; the marking line no longer says the mastery map trusts the mark.
- `app/js/prereq.js`: `examPassedAuto` replaces the plain exam pass in `derivedMet` (topic and stage); `reviewPassed` prefers `passedAuto`.
- `app/js/screens/you.js`: `selfHTML` card, hidden when empty.
- `app/tools/playthrough.mjs`: `provenanceChecks` (a, b, c of the brief).
- `docs/AUTHORING.md` section 13, `docs/ENGINE-BACKLOG.md` item 521.

## Decisions and limits
- Self counts live in a top-level `selfMarked`, not inside `skills`, so no skill record is created or changed by a self row.
- Old exam attempts without `passedAuto` count as `passed` on exams the manifest's `selfExams` does not list (no longform, no check part), and not at all on listed ones or without a manifest; levels already in `state.prereq.met` stay met (sync records them on every change). Old reviews fall back to `passed`.
- Follow-up: `ZQ.content.examPassedAuto` and `examPassedAt` (js/content.js) are the one rule; `topicPassed`, `courseTestedOut`, the resume check and prereq all read it. `tools/validate.mjs` writes `selfExams` to the manifest. Playthrough check (d): an old passed attempt counts on topic-1.5, not on topic-1.1.
- Self-marked misses still join the redo queue.
- Content untouched. Unit of proof for (c) calls `examFinished` directly; the exam screen computes `passedAuto` (checked by `--exam topic-1.1`).
