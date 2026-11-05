# Zero-to-Quant: curriculum review and agent handoff

## 0. Status, provenance and operating constraints

```yaml
document_type: consolidated_review_and_recommendations
repository: smuddassirshah-cpu/zero-to-quant
reviewed_branch: claude/amazing-wright-d4mx7i
reviewed_commit: f9a4545573e3c2a5ba4ffd1e2d2a79610ebe4b4a
review_date: 2026-11-05
target_learner: maths enthusiast; no formal education beyond GCSE
target_outcome: independently demonstrate readiness for interviews in a specified quant role
review_mode: read_only
repository_mutations_performed: none
clone_status: attempted_but_failed_due_to_missing_workspace_github_credentials
access_used: authenticated_GitHub_connector_at_exact_commit
runtime_testing_performed: false
assessment_scope: source_based_curriculum_and_pedagogy_review
```

This document consolidates the review already delivered to the user. It is not a new audit of subsequent commits. It does not authorize implementation, commits, pushes, new branches, merges, deletions or repository edits. The user authorized a read-only evaluation and creation of this separate Markdown handoff. Recommendations and acceptance criteria below are proposals, not implemented changes or empirically validated standards. Any later implementation must follow the user's then-current authorization.

Receiving agent: verify findings against the current branch before acting. Preserve the distinction between (a) observed source facts, (b) educational interpretation, and (c) proposed remedies. Do not silently reinterpret this document as a request to execute the repository's development/session protocol. The validator is documented as rewriting `app/content/manifest.json`; do not run it during a strictly read-only pass.

Evidence base: all 79 course maps; curriculum and manifest; prerequisite, mastery and assessment logic; interview-path and bank inventories; selected homework and mocks; 46 first/last lesson samples across 23 courses. This is not an exhaustive mathematical certification, learner-outcomes study, or browser usability test. Sample proportions must not be extrapolated to the entire curriculum.

Repository evidence paths below are relative to the repository root. Resolve them at the reviewed commit using:

`https://github.com/smuddassirshah-cpu/zero-to-quant/blob/f9a4545573e3c2a5ba4ffd1e2d2a79610ebe4b4a/<path>`

## 1. Primary conclusion

The app is a credible and substantial teaching framework, particularly for school-maths foundations, probability, misconception correction and research hygiene. It is not yet a dependable standalone system for establishing quant interview readiness.

Core failure mode: completion and short-assessment performance are allowed to stand in for independent competence. The app teaches guided understanding more convincingly than it verifies unfamiliar problem-solving, sustained coding, independent research and spoken reasoning under interview conditions.

Highest-value next work: improve evidence of learning, role-specific progression and independent assessment before expanding breadth further. Do not equate authored lesson count, green playthroughs, hours logged, XP, or a mastery badge with interview readiness.

## 2. Verified inventory at reviewed commit

| Stage | Mapped lessons | Authored lessons | Missing |
|---|---:|---:|---:|
| 0: From nothing | 193 | 193 | 0 |
| 1: Foundations | 560 | 507 | 53 |
| 2: Intermediate | 202 | 150 | 52 |
| 3: Advanced | 259 | 204 | 55 |
| Total | 1214 | 1054 | 160 |

Counts include optional pure mathematics. They describe file availability, not depth, correctness or educational completeness. They were obtained from course maps plus actual repository files/manifest, not copied from historical progress reports.

Additional inventory:

- 79 course maps.
- 200 dedicated interview-bank questions across 20 non-sample bank files.
- 35 non-sample standalone coding drills; additional coding tasks exist within lessons/homework.
- 11 non-sample mock assessments.
- 23 interview-preparation paths.
- Stage-exam file exists only for Stage 0. Later topic exams and mocks exist; they are not equivalent to the promised integrated stage exits.

Consequential incomplete courses:

| Course ID | Authored/mapped | Relevance |
|---|---:|---|
| complex | 0/13 | Derivatives/Fourier pricing foundations |
| odes | 0/18 | Differential-equation foundation for pricing/PDEs |
| numerics | 0/17 | Conditioning, stability, numerical reliability |
| convex | 0/17 | Optimisation and constrained portfolios |
| stat-models | 0/18 | Research/statistical modelling breadth |
| momentum-rep | 5/15 | Independent paper-replication endpoint |
| pairs-rep | 0/15 | Independent paper-replication endpoint |
| analysis | 19/24 | Optional proof-based mathematical breadth |
| linear-maps | 14/19 | Optional proof-based linear algebra |
| vector-calc | 0/12 | Optional mathematical breadth |
| algebra | 0/17 | Optional mathematical breadth |
| topology | 0/13 | Optional mathematical breadth |

Evidence: `app/content/curriculum.json`, `app/content/manifest.json`, `app/content/courses/*/course.json` and corresponding lesson files.

## 3. Strengths to preserve

### S01. Concrete foundations suited to GCSE entry

Early lessons introduce meaning before notation: fractions through equal pieces/number lines; algebra through envelopes containing unknown amounts; functions as input-output machines; conditioning by removing incompatible outcomes. Preserve this approach and the assumption that unfamiliar notation is teachable, not evidence of low ability.

Evidence: `courses/number-sense/l1-what-a-fraction-measures.json`, `courses/equations/l1-letters-for-numbers.json`, `courses/functions/l1-machines.json`, `courses/conditional/l1-what-changes.json` under `app/content/`.

### S02. Coherent instructional structure

Problem/exploration -> increasing constraints -> misconception -> generalisation/derivation -> application. Authored distractor feedback explains the learner's error. Multiple representations connect diagrams, quantities, notation and code. Preserve these mechanisms; improve transfer assessment rather than removing useful scaffolding.

Evidence: `docs/AUTHORING.md`, sampled lesson files.

### S03. Substantial probability and interview content

Coverage includes conditioning, indicators, conditional expectation, Markov chains, stopping problems, geometric probability and follow-ups that alter a solved problem's assumptions. Role-specific paths, timed coding, games, behavioural preparation, spoken prompts and spaced/mixed practice already exist. Do not propose these as wholly absent features.

Evidence: probability course maps, `app/content/courses/puzzles/course.json`, `app/content/prep.json`, `app/js/engine/select.js`.

### S04. Strong research hygiene

Backtesting/alpha content explicitly addresses point-in-time universes, delistings, leakage, costs, turnover, held-out evaluation, multiple trials, uncertainty and reporting failures. Synthetic-data limits are acknowledged. Preserve this emphasis and the practice of reporting negative results.

Evidence: `app/content/courses/backtest/homework-4.json`, `app/content/courses/alpha/homework-4.json`.

## 4. Findings, consequences and proposed acceptance criteria

### F01 — Readiness is insufficiently operationalised by role

Priority: P0 (outcome definition). Type: educational judgement supported by source structure.

Observed:

- Written curriculum recognises trader/researcher/developer differences; 23 prep paths exist.
- Main Today selection uses curriculum order, start stage, availability and completion/test-out state. It does not implement a distinct career-specific main learning sequence.
- Finance knowledge is framed too universally as required before trader/researcher interviews. Public employer guidance does not support that universal claim.

Impact: a GCSE learner can mistake the broad curriculum for a prerequisite to every quant interview and spend substantial effort on low-priority material before practising the target role.

Proposed remedy: define explicit role-specific outcomes; fork early after a shared foundation; keep switching tracks possible. Treat employer formats as dated and role/office-specific, not universal.

Proposed acceptance:

- Each role has an explicit set of unfamiliar tasks the learner must perform independently.
- Required, recommended and optional material are distinguished by role.
- Main recommended next work is consistent with the chosen role, rather than only the separate Prepare page.
- No single completion percentage or hours total is presented as sufficient evidence of readiness.

Evidence: `docs/curriculum.md`; `app/content/prep.json`; `app/js/screens/today.js:74-100`; `app/js/content.js` course filtering; external sources E01-E03.

### F02 — Some dependencies are larger than the competence they protect

Priority: P1. Type: observed dependencies + educational judgement.

Observed:

- `coding-int/L1` requires `graphs-dp/L4`, `algo-think/L3`, `contests/L3`.
- `coding-int/L4` requires `coding-int/L3`, `contests/L4`.
- `systems/L1` requires `cpp-pricing/L3`.
- Recursive dependency tracing for the trader superday reaches 35 courses, including algorithms/contests. This is a dependency-course count, not a requirement to complete every lesson: test-outs and overrides exist.

Impact: focused paths expand into broad chains; a systems learner may be gated on pricing-course packaging rather than the necessary C++/memory concepts.

Proposed remedy: prerequisite units should be the smallest necessary competencies. Use targeted diagnostics or short recaps when full levels introduce excessive unrelated material. Do not simply disable all gating.

Proposed acceptance:

- Every required dependency has a short, defensible learning rationale.
- Entry to systems can be earned by demonstrating relevant programming/memory skills.
- Coding/interview access does not require unrelated contest content merely because a needed concept happens to be taught there.
- Dependency closures are reviewed by role, including test-out options.

Evidence: `app/content/courses/coding-int/course.json:26,67`; `app/content/courses/systems/course.json:26`; `app/content/exams/mock-superday-trader.json`; `app/js/prereq.js`.

### F03 — Authored advanced content depends on unwritten prerequisites

Priority: P0 for derivatives route. Type: verified source fact.

Observed:

- `pdes/L1` requires `odes/L4` and `ito/L3`.
- `pdes/L3` requires `pdes/L2` and `numerics/L4`.
- ODE and numerical-methods lessons are not authored.

Impact: a fresh learner cannot complete the PDE route through normal in-app teaching under strict prerequisites. Opening early removes a lock, not the knowledge gap. Missing replication/statistical-modelling content also limits research-route completeness; optional pure-maths gaps have lower urgency for many interview targets.

Proposed acceptance:

- Every advertised required route is traversable through authored teaching or a legitimate diagnostic/external-study pathway.
- Required but unwritten material is explicitly marked as a route limitation.
- No route is declared complete solely because its advanced destination lessons exist.

Evidence: `app/content/courses/pdes/course.json:28,53`; ODE/numerics course maps and manifest.

### F04 — Quiz format often fails to assess the lesson's stated performance

Priority: P0 for readiness validity. Type: observed non-random sample + interpretation.

In the 46 sampled lessons, end-of-lesson quizzes contain 182 questions: 98 choice, 81 numeric, 1 expression, 2 multiple-selection; no code or long-form response. This does not imply coding/writing is absent elsewhere.

Concrete examples:

- `proof/l15-proof-a-stranger-can-check`: objective is writing a checkable proof; lesson quiz is four multiple-choice questions.
- `coding-int/l19-a-live-round`: lesson includes actual code tasks, but quiz checks choices/numbers.
- `ito/l17-derivation-aloud`: largely selecting/ordering explanations, not independently producing and defending a spoken derivation.

Impact: recognition and short answers can be mistaken for generative reasoning and independent performance.

Proposed remedy: retain formative scaffolding; progressively fade it. Distinguish introduced/practised from independently demonstrated competence. Assess the actual verb in the objective: write, derive, code, explain, defend.

Proposed acceptance:

- Every high-level outcome maps to at least one independent performance task.
- Mastery of a coding outcome cannot rely solely on a non-coding quiz.
- Proof/explanation outcomes include production from a blank start, not only rearrangement of supplied steps.
- Cross-topic problems require selecting a method without its name being given.

Evidence: sampled lesson files above; `docs/AUTHORING.md`.

### F05 — Aggregate passes and self-marking overstate assessment evidence

Priority: P0. Type: verified implementation facts + validity judgement.

Observed:

1. Lesson mastery threshold is 80% on a short quiz.
2. `quizFinished` does not add missed quiz items to redo when aggregate mastery is reached; e.g. 4/5 can leave one missed concept unqueued.
3. Level test-outs draw up to six items from the level review. Unseen-first selection within that small review helps, but repeated attempts can reuse material.
4. A passed topic exam can satisfy all levels in the topic, hiding weak subskills behind aggregate performance.
5. Long-form answers reveal a model and rely on self-ticked rubric points; seven points counts as right. This is reflection evidence, not independent grading.
6. Coding OA mock passes at one of two problems; written curriculum target is two problems in 60 minutes. Distinguish an illustrative mock threshold from the curriculum's own readiness criterion; do not claim a universal employer pass mark.
7. Coding OA mock draws from the same pool available in the drill library. A request not to practise that pack first does not maintain an unseen holdout.
8. Only Stage 0 has a stage-exam file, despite the written plan's integrated stage exits.

Proposed remedy: separate practice, diagnostic and readiness assessments. Use holdout tasks, essential-skill floors, delayed reassessment and human review where the app cannot evaluate performance.

Proposed acceptance:

- Every missed essential concept gets remediation even when the total score passes.
- Topic/stage readiness includes essential-skill coverage; aggregate success cannot conceal critical deficits.
- Readiness tasks are withheld from practice or clearly labelled previously seen.
- Self-marked and independently verified outcomes have distinct evidence status.
- Oral reasoning is assessed by another person using a rubric; speaking prompts alone are not counted as verified oral competence.
- Coding/mock thresholds are reconciled with the explicitly selected outcome.
- Stage exit claims match actual available assessment mechanisms.

Evidence: `app/js/state.js:235-249`; `app/js/prereq.js:22-24,89`; `app/js/screens/review.js:670-718`; `app/js/engine/widgets/longform.js`; `app/content/exams/mock-oa-code.json:6,24`; exam inventory.

### F06 — Guided projects do not establish independent research/development

Priority: P1. Type: verified task design + judgement.

Observed: final alpha lesson provides the surrounding pipeline and asks for four gaps to be filled. Final alpha/backtest homework reports the course's seeded study. Independent GitHub projects are requested in the curriculum, but app completion does not provide equivalent evidence of completion and quality.

Impact: learners can finish prescribed components without learning to formulate questions, obtain/reconcile unfamiliar data, select methods, build an end-to-end workflow or defend an inconclusive result.

Proposed remedy: follow guided projects with independently specified capstones on unseen data and external review. Keep the synthetic study as a learning tool; do not treat it as real-market evidence.

Proposed acceptance:

- Learner produces a complete executable project outside the lesson environment.
- Reviewer can rerun from a clean environment, reproduce quoted results and inspect tests.
- Learner justifies question, data choices, split, baseline, methods, limitations and failed approaches.
- Learner can answer unprepared follow-ups and adapt one requirement.
- Research route completes an actual independent replication/out-of-sample extension or an explicitly equivalent outcome.

Evidence: `app/content/courses/alpha/l16-research-note.json:899-911`; alpha/backtest final homework; replication course maps; `docs/curriculum.md`.

### F07 — Universal short-lesson packaging strains advanced learning

Priority: P1. Type: observed examples + judgement.

Observed:

- `research-int/l1-two-regressions`: metadata 15 minutes; opening prose says about 25 minutes.
- `coding-int/l19-a-live-round`: metadata 15 minutes; objective is a 45-minute live problem with follow-ups.
- `measure-prob/l1-why-measure` introduces countability, zero-probability events, Cantor-set length and a Vitali-set/axiom-of-choice argument while proof/analysis is optional.

Impact: depth and prerequisite maturity exceed the apparent session size. A learner starting at GCSE may misattribute an unrealistic estimate or missing bridge to their own ability.

Proposed remedy: distinguish short conceptual lessons, extended problem workshops and project sessions. Make minimal mathematical reasoning common to relevant tracks without forcing all optional pure mathematics onto them.

Proposed acceptance:

- Duration metadata and prose agree and identify external practice time separately.
- Advanced lessons either establish prerequisite reasoning or route to a concise bridge.
- Timings are calibrated against target learners, not the author executing known solutions.

Evidence: lesson paths above; `docs/AUTHORING.md`; `app/content/courses/measure-prob/course.json`.

### F08 — Explanatory precision needs review beyond answer-key checking

Priority: P1; verify current source before correction. Type: specific mathematical findings, not an estimated global error rate.

Example A: `ito/l1-walk-to-bm.json:897-904`.

- Summary says a scale larger than `1/sqrt(n)` blows up. Literal counterexample: `2/sqrt(n)` yields endpoint variance 4, not divergence.
- Formula presents Brownian motion as an ordinary limit of scaled walks without specifying convergence. The standard invariance-principle statement is process convergence in distribution, not an unqualified pathwise equality.
- Proposed criterion: correct the generalisation and name the intended convergence, while keeping the introductory explanation accessible. Verify finite-grid versus limiting claims as part of the same review.

Example B: `pdes/l1-equations-in-two-variables.json:1194`.

- Summary says only `V` multiplied by `V` makes the equation nonlinear.
- Counterexamples: `(V_S)^2` and `sin(V)` also introduce nonlinearity.
- Proposed criterion: definition covers dependence on the unknown and its derivatives; distinguish variable coefficients from nonlinear dependence.

Do not infer that all content is incorrect from these examples. Conversely, passing the authored answers through the renderer does not establish that definitions, assumptions and generalisations are correct.

Proposed acceptance: a separate mathematical review checks definitions, assumptions, limiting statements, equivalence claims and explanatory summaries, alongside numeric keys and code solutions.

External corroboration: E04-E05.

### F09 — Workload representations disagree

Priority: P2. Type: verified data discrepancy.

| Stage | Sum of topic hours | Stored stage hours |
|---|---:|---:|
| 0 | 555 | 515 |
| 1 | 1650 | 1400 |
| 2 | 940 | 800 |
| 3 | 550 | 550 |
| Total | 3695 | 3265 |

Written curriculum: 3695 hours, or 3495 excluding counted pure-maths material. Learn header sums stored stage fields. Optional stochastic calculus has zero allocated hours, so the total does not include the complete derivatives route.

Impact: inconsistent expectations and misleading route comparisons. Hours are author estimates, not readiness measurements.

Proposed acceptance:

- One authoritative workload definition feeds lesson/topic/stage/role summaries.
- Optional content and external practice are counted or explicitly excluded.
- Role-specific estimates state assumptions and uncertainty.
- Completion is gated by demonstrated capabilities, not hours accumulated.

Evidence: `docs/curriculum.md`; `app/content/curriculum.json`; `app/js/screens/learn.js:154-161`.

## 5. Role-specific outcome assessment

| Role | Current strengths | Main remaining requirements |
|---|---|---|
| Trader | Extensive probability, numerical fluency, games and interview preparation | Shorter relevant route; unseen problems; external spoken mocks; assessment of adapting reasoning |
| Researcher | Probability/statistics, validation, research hygiene | Independent unfamiliar-data work; completed replication endpoint; defensible research and external review |
| Developer | Broad algorithms, coding and systems coverage | Sustained native coding/debugging/profiling; independent systems project; live coding/design evaluation |
| Derivatives/desk quant | Authored advanced stochastic/PDE material | Complete ODE/numerical prerequisites; mathematical precision; independent derivation and numerical validation |

Planning priorities, not universal hiring requirements:

- Trader: prioritise probability, numerical fluency, uncertainty, communication and games; extensive ML/PDE/abstract algebra can often wait.
- Researcher: prioritise probability, statistics, linear algebra, Python, experimental design and independent data analysis; much low-latency C++/contest specialisation can wait.
- Developer: prioritise programming, algorithms, C++, systems/debugging; broad stochastic calculus and paper replication can often wait.
- Derivatives: prioritise calculus, probability, differential equations, numerics and pricing; some trader-game/contest content can wait.

Keep skill acquisition separate from getting an interview. The app is not a credential. Some research employers describe quantitative degrees among strong-candidate characteristics; that is relevant to application strategy, not proof that self-directed learning is futile or that every firm imposes the same requirement. Do not promise hiring or degree equivalence.

## 6. Recommended work order if implementation is later authorized

1. Define role-specific readiness contracts (F01).
2. Strengthen assessment validity and task-objective alignment (F04-F05).
3. Audit role routing and dependency closures (F02), including missing prerequisite chains (F03).
4. Establish independent capstones and external evaluation (F06).
5. Audit advanced explanations and prerequisite bridges (F07-F08).
6. Reconcile workload metadata (F09).
7. Pilot with actual GCSE-entry learners before making end-to-end effectiveness claims.

Pilot evaluation should observe where learners stall, their retention after a delay, ability to solve genuinely unfamiliar problems, ability to explain choices, and ability to complete tasks outside the app. No target success percentages are supplied here: they require an explicit assessment design and calibration.

Do not close findings merely by adding more lesson files, raising pass thresholds, making copy more confident, or rerunning authored-answer playthroughs. A successful remediation must address the specific gap between instruction and demonstrated independent performance.

## 7. Suggested response from the receiving agent

Unless the user separately authorizes implementation, return a read-only response with:

1. Current branch/commit and divergence from the reviewed snapshot.
2. One disposition per F01-F09: confirmed / partially confirmed / already resolved / disputed, with exact source evidence.
3. Distinction between observed defects and pedagogical recommendations.
4. Dependency-ordered remediation proposal, preserving existing strengths.
5. Acceptance evidence for each proposed item; identify what needs a human reviewer or learner pilot.
6. Explicit list of any repository mutations performed (expected: none under the existing read-only instruction).

## 8. External reference register

These references were consulted during the original review; no new employer-format verification was performed for this consolidation. Treat recruiting information as time-sensitive. The university/paper references support mathematical definitions, not the educational effectiveness of this app.

- E01: Jane Street, Trading Interviews — conversational problem-solving, probability/statistics, possible coding/data analysis; no required prior finance knowledge or advanced college maths. https://www.janestreet.com/trading-interviews/
- E02: Citadel, Candidate FAQs: Quantitative Research — statistics, coding, data and research experience; quantitative degrees among strong-candidate characteristics; finance can be taught. https://www.citadel.com/careers/career-perspectives/candidate-faqs-quantitative-research/
- E03: Citadel, Our Campus Quantitative Research Interview Process — programming, research ability, algorithms/problem-solving and explaining approaches. https://www.citadel.com/careers/career-perspectives/our-quantitative-research-interview-process/
- E04: Stein's method for rough paths — introductory statement of Donsker convergence in distribution to Brownian motion. https://arxiv.org/abs/1707.01269
- E05: University of Toronto PDE textbook, section 1.3, Classification of equations — linearity/nonlinearity in the unknown function and derivatives. https://www.math.utoronto.ca/courses/apm346h1/20169/PDE-textbook/Chapter1/S1.3.html

