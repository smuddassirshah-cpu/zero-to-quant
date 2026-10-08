# Content format, authoring pipeline and verification

> **Appendix to `docs/PLAN.md`.** Moved from `docs/blueprint/work/content-format.md` on 7 October 2026 and tidied for the blueprint. Section numbers are unchanged, so citations elsewhere still resolve. `docs/PLAN.md` wins where the two differ; this file wins over the widget catalogues and the working papers in `docs/blueprint/work/`. Tidied in place:
>
> | Where | Was | Now |
> |---|---|---|
> | Decision 18, 3.2 (`RuntimeTag`, `Drill.aim`), 3.9, 6.1 step 8, 6.11, 7.6, 12.2, 13 item 15, 14 C7 | Four CI runtime tags; MicroPython with `ulab` as the Artifact's fallback | No MicroPython; placement by `needs` at run time. *Superseded by the revision 2 row below: Pyodide runs on the web app only* |
> | Decision 13, 8.2 | Two files per course; about 50 courses; the spike's 69 Python files | One bundle per course, one generator module per topic. *Counts superseded by the revision 2 row below: 103 courses, 26 topics, no Python in the Artifact* |
> | 3.2 `Topic` | `exam` required; every topic counted in the path | `exam` optional (0.4 and 0.5 close on exit parts; 2.4 waits for the owner's decision D4); `counted: false` for 3.2 |
> | 3.3 Why rows, 3.10 rules | `why.then` shown after a wrong answer | Unresolved screens show the diagnosis and `why.shown` only; `why.shown` passes the leak lint |
> | 3.1 | 1 to 4 courses per topic | 1 to 5 (`docs/CURRICULUM.md` 7, request 1) |
> | 14 C7, 13 item 2 | "`docs/PLAN.md` stage 22"; a 13 MB or 49 MB first Python load | Stage 25; 24 MB of files (`docs/PLAN.md` conflicts 4 and 8) |

> **Revised by the `docs/PLAN.md` review, 7 October 2026** (its section 13 lists the findings). Section numbers are unchanged.
>
> | Where | Was | Now |
> |---|---|---|
> | 3.2 `Lesson.introduces`, `ItemHead` | Up to 4 skills a lesson | At most 2, at level grain; `steps` tags with no card (`ASSESSMENT.md` 4.1); items gain `sibling` (required on long-form homework and paper items) and `imitates` (recreated book problems) |
> | 3.2 `long-form` | 10-point rubrics only; no consequence line | `scale` 10 or 3 (the quiz production item); an optional `consequence` line shown on result screens |
> | 3.2 `Lesson`, 9.3 | Every learner walks every ladder screen | `fastPath`: one sharp check item behind "Skip to the trap" when the hook and first ladder screen are first-try correct (lesson-creator's adaptive pace) |
> | 3.2 `Exam` | A fixed slot order | `shuffle` (default on) and `unlabelledSlots` (default 2) (`ASSESSMENT.md` 3.2) |
> | 6.13 point 1, 9.1 steps 5 to 7 | The owner checks that the English means what the maths computes, merges every lesson and checks every phone preview | An independent reviewer agent restates the maths from the English and `zqverify` checks the restatement; a paid human spot check of 5 lessons per course from Stage 1; the owner reviews per level on the long-lived preview Artifact |
> | 9.3 rules 15, 27 and new 34 to 38 | Quizzes test the introduced skill only; citations checked only by a person with the book | Prove, Derive and Show lessons have a production item; free-source locations are fetched and checked while authoring; method-free stems; fast path; time estimates by difficulty |
> | 13 item 1, 14 C8 and C11 | SciPy and statsmodels "not packaged"; "under 255 files"; C11 as a first level of the reference lesson | Packaged and measured (`ARCHITECTURE.md` 6.3.3); within the 230-file release budget; C11 is the reference lesson plus level W1 of `crs.numwork` (`docs/PLAN.md` stage 84) |

> **Revision 2 of `docs/PLAN.md`, 7 October 2026: the owner's decisions.** These rows win over anything below that reads otherwise. Section numbers are unchanged.
>
> | Where | Was | Now |
> |---|---|---|
> | Decision 18, 6.11 (runtime placement), 7.6, 13 items 1, 2 and 15 | Pyodide on both targets; the split-archive loader in the Artifact | **Python, SQL and C++ drills run on the web app only.** The Artifact publishes only files generated from this repository's own sources, so it has no Python or SQLite; every drill there shows its starter code and a handoff link and returns by result code (`ASSESSMENT.md` 14.3). CI still runs every drill on CPython 3.12 and Pyodide 314.0.7 |
> | 1.2 lesson flow, 6.1, 9.2 | Authored code runs at build time | Unchanged, and now load-bearing: it is why every lesson plays fully in the Artifact |
> | 7.6, 12.2 (the KaTeX sink) | KaTeX HTML output with KaTeX fonts | HTML with MathML on the web; MathML alone in the Artifact, in system maths fonts; the compiler's KaTeX render check runs both outputs (`ARCHITECTURE.md` decision 37) |
> | 8.2 | 85 courses in 21 topics; Python in 15 Artifact files | 103 courses in 26 topics (`docs/CURRICULUM.md` 0.1); no Python in the Artifact; about 198 files a release (`docs/PLAN.md` 5.6) |
> | 3.2 `Drill.needs` | Eight packages | Plus `cvxpy` and `highspy` at the 2.0b wave (`docs/PLAN.md` 5.7) |
> | 3.2 `Curriculum`, `Track` | Four tracks; one hours figure per item | `trk.ml-research` defined; A1 and 2.4 hours by track (`docs/CURRICULUM.md` decisions 7 and 8, section 7 request 2) |
> | Decision 13, 13 items 8 and 11 (second review round of `docs/PLAN.md`, edited in place) | 85 courses in 21 topics; the copyright rule and the glossary exemption awaiting the owner | 103 courses in 26 topics; both closed at decision 8's defaults |

Working paper for the Stage 2 Blueprint, 6 October 2026, revision 2. Scope: how lessons, items, generators and code drills are written, compiled, proved correct and graded. Input to `docs/PLAN.md` (component tree, interfaces, failure modes and execution stages for the content system).

**Revision 2** (same day) keeps every section number of the first draft, because the sibling papers and the curriculum files cite them. It reconciles this paper with what was written after it (`AI-TUTOR.md`, `ASSESSMENT.md`, `canon-gap.md`, the seven `docs/curriculum/*.md` files) and with the platform spikes (`spikes/README.md`), and re-runs every worked example. Section 0.3 lists each change and its reason.

**How to read it.**

- Section 0 lists every decision with the rejected alternatives, what was executed, and what revision 2 changed. Section 1 says what this paper takes from the six widget catalogues and the later papers, and what it changes in them.
- Sections 2 to 5 define the format: the files, the schema, identity and versioning, and generators.
- Sections 6 to 9 define the machinery: verification in CI, grading at runtime, the compile step, and the authoring workflow.
- Sections 10 and 11 are the worked examples. Both were executed (section 0.2), so every claim about them is measured.
- Sections 12 to 14 list what this paper needs from the widget, engine and tutor papers and the curriculum files, the open questions, and the build stages.

**Evidence tags** follow the design research: [measured] for values measured while writing this paper, [our choice] for decisions without outside evidence, [unverified] for facts not yet checked, [recalled] for facts from memory that a person should confirm, [inferred] for deductions. Values from `docs/curriculum.md`, `docs/design-research.md`, the prototype or the widget catalogues are untagged and cite their file.

---

## 0. Decisions in brief

### 0.1 Decisions

| # | Decision | Chosen | Rejected | Reason |
|---|---|---|---|---|
| 1 | Lesson and item source format | **YAML 1.2 under a strict profile**, with prose fields in a small Markdown dialect (ZQ Markdown) | Markdown with frontmatter and directives; MDX; TypeScript modules; JSON; TOML | About 74% of a lesson's lines are structure, not copy [measured, section 2.1]. YAML keeps structure and copy in one file, needs no escaping for TeX backslashes, and diffs line by line. MDX and TypeScript make content executable and double every TeX backslash |
| 2 | Generator source format | **TypeScript module plus a YAML spec beside it** (parameter box, phrasebook, levels), mirrored by a **Python verifier** | Generators as YAML templates with expressions; Python generators run at build time only | Generators must run on the device for unlimited practice, so they are code. Admissibility and answers are written twice, in two languages, and compared on every point |
| 3 | Schema | **zod 4** schemas in one package shared by compiler, preview and runtime; JSON Schema exported for editors | JSON Schema written by hand; TypeScript types only | One source of truth; runtime validation of bundles; `z.toJSONSchema` gives editor completion for agents and the owner [measured: the lesson schema exports] |
| 4 | Identity | **Immutable, human-readable, kind-prefixed ids** (`lsn.cond.shrinking-sample-space`); display numbers computed from position | UUIDs; ids built from curriculum numbers | Readable diffs and greppable references; renumbering the outline never touches learner progress |
| 5 | Change control | **`rev` per lesson, item, drill and generator, enforced by an answer hash** in an append-only `ids.lock.json` | Free edits; semantic versioning of the whole content set | A change to a correct answer, a tolerance or a screen order cannot merge without a `rev` bump and a changelog line. Copy edits need nothing |
| 6 | Learner-state migrations | **Data-only migrations** (`rename`, `merge`, `split`, `retire`) applied in order on load | Hand-written migration functions | Four operations cover every content change (moving a lesson between levels needs none, because ids do not change); data migrations are testable against stored learner snapshots |
| 7 | Correctness proof | **Two implementations must agree**: the author's declared answer (or the TypeScript generator) against an independent Python solver; Monte Carlo as a second check for probability | Trusting the author; review alone | The Stage 1 lesson shipped two equal-valued options on one screen; the verifier finds that in one line (section 10.6) |
| 8 | Verify language | **A whitelisted subset of Python expression syntax**, walked from `ast`, never `eval` or `sympify` | Python snippets per item; SymPy strings | Readable in a YAML diff, safe to run on agent-written content, and enough for almost every item. A sandboxed `.verify.py` file is the escape hatch |
| 9 | LaTeX parsing | **One parser for runtime and verification**: Compute Engine's standalone `latex-syntax` entry (128 KB gzipped) | SymPy `parse_latex`; our own LaTeX parser | The parser that grades the learner is the parser that checks the content, so a parsing quirk shows up in CI, not on a phone |
| 10 | Symbolic equivalence at runtime | **Compute Engine `latex-syntax` to MathJSON, then seeded numeric probing in the declared domain, plus structural form checks**. The full Compute Engine (1.19 MB gzipped) runs only in CI | Full Compute Engine on the device; mathjs; nerdamer | Measured in section 7.3: mathjs has no LaTeX input and reduced none of four identities; nerdamer 2.0.0 is four days old after five years without a release; the full Compute Engine is nine times the size of its parser |
| 11 | Numbers in content | **Answers are integers or exact strings** (`'10/109'`, `'1000 * 11/36'`); tolerances may be floats | Floats for answers | `0.1 + 0.2` problems never reach a check; YAML floats are rejected with a message |
| 12 | Diagnosis | **One `diagnose` list per graded screen**: a matcher, a misconception id (or `slip: true`), a line and a show-why recipe; choice options carry the same fields inline | Per-widget misconception maps; free-form feedback | One matching order everywhere (section 7.8); every line is tied to a named misconception the tutor and the mastery model can use |
| 13 | Compile output | **One JSON bundle per course and one generator module per topic**, plus a manifest, search, glossary, Notebook and skill graphs (tidied for the blueprint: was two files per course) | One file per level or lesson; a generator module per course | The Artifact accepts 255 files per publish and 511 per version. The path has 103 courses in 26 topics (`docs/CURRICULUM.md` 0.1; draft 1: 85 in 21): 103 bundles and 26 generator modules fit the release budget of `docs/PLAN.md` 5.6, where 206 per-course files would not |
| 14 | Search | **MiniSearch 7.2.0** (MIT, 18 KB gzipped) with one index per stage | Lunr; FlexSearch; Pagefind | MiniSearch serialises to one JSON file per index. Lunr's npm entry has not changed since July 2023 [measured: npm metadata]; Pagefind ships many chunk files and WebAssembly, which fights the file limit; FlexSearch was not measured and offers nothing the app needs beyond MiniSearch |
| 15 | Long-form marking | **Self-mark against a rubric of 4 to 10 points totalling 10 marks; Bertie drafts a mark per point with a verbatim quote as evidence (`AI-TUTOR.md` 2.7); the learner accepts or changes every point** | AI mark as the record; self-mark only | The owner asked for the tutor from day one; the record stays the learner's, and a quote that is not in the answer scores 0 |
| 16 | Authoring workflow | **Agent drafts, `zq check` loop, storyboard, adversarial reviewer agent, owner merges**, one lesson per pull request | Owner writes; whole levels per pull request | An 800-line lesson YAML is a reviewable diff; a level is five of them |
| 17 | Element references | **The widgets' own `kind:name` ids (`AI-TUTOR.md` 0.2), written with the widget in content: `grid/cell:5,5`**; recipe arguments and set answers use the bare `cell:5,5` | Revision 1's `grid:cell-5-5`; a second id scheme for content | One id per element across widgets, tutor act lines, set answers and hints. The compiler resolves every reference against the widget's `targets(config)` |
| 18 | Code runtimes | **Pyodide 314.0.7 on the web app only since `docs/PLAN.md` revision 2 (the Artifact hands every drill off); no runtime tags.** A drill declares `needs`; CI runs every drill on CPython 3.12 (raised from 3.11 by the `docs/PLAN.md` review, conflict 19: the soft deadline needs `sys.monitoring` and SciPy 1.18.0 needs 3.12) and on Pyodide with exactly its `needs` loaded; where it runs is decided at run time from `needs` against `PythonRuntime.available()` (`ARCHITECTURE.md` 5.9). C++ drills never run in the Artifact (tidied for the blueprint: was four CI runtime tags with MicroPython as the Artifact fallback) | MicroPython with `ulab` as a fallback runtime; CI tags | The owner dropped MicroPython after the iPhone spike ran Pyodide with NumPy and pandas inside the Artifact. One runtime means one grader and one set of tracebacks everywhere |
| 19 | Tracks | **Data in `curriculum.yaml`** (`trk.*`, each topic and course marked core, elective, optional or absent) | A fixed `trader`, `researcher`, `developer` enum on each course | `canon-gap.md` proposes a fourth track and an add-on; the owner has not decided. Data absorbs either answer without a schema change |
| 20 | Tutor fields | **Content, checked like copy**: `tutor.focus` on every task screen, `tutor.reps`, `why.rep`; a lint fails any tutor text that contains a value the screen's check accepts | Tutor context assembled from copy alone | `AI-TUTOR.md` 4.1 needs an outline title, representations and notes per screen. Tutor notes are not sealed, so the leak lint is the guard |

### 0.2 What was executed

The worked examples are not sketches. In a scratch install on 6 October 2026, run first for revision 1 and again, after every revision 2 change, on the files printed in sections 3.2, 10 and 11 [measured]:

- The schemas in section 3 compiled under zod 4.6.5 and validated the lesson in section 10, the library entries it references, and fixtures for the new schemas: `ASSESSMENT.md`'s `plan.yaml` example (its section 8.9) verbatim, a topic with gate and confirm exit parts, a three-form finals paper, and a long-form check (a rubric totalling 9 marks is rejected). `z.toJSONSchema` exported the lesson schema for editors.
- A 180-line prototype of the compiler front end (`zq check`) parsed the lesson under the strict YAML profile, merged `from:` widgets, resolved every reference including 36 element references against stand-in `targets(config)` functions for three widgets, ran the copy and tutor lints, and rendered all 50 formulas with KaTeX 0.19.0 in strict mode. It reports 0 errors and 0 warnings for the final file. Six planted faults (an element the grid does not have, a malformed set id, a recipe naming a missing cell, an accepted answer in tutor notes, a missing `tutor.focus`, a `from:` widget that changes task but keeps its label) gave 5 errors and 1 warning, one per fault.
- A 300-line prototype of the Python verifier (`zqverify`), fed by a 30-line Node pre-pass that turns formulas into MathJSON, recomputed every answer, every misconception value, the derivation chain and seven arithmetic claims in the copy, and ran a Monte Carlo check of $10^6$ trials for each of the six items that ask for a probability over a finite space. It reports 0 failures.
- The generator in section 11 ran over its whole parameter box of 21,760 points. The TypeScript generator and the Python verifier agreed on admissibility, level, answer and every misconception value at every point. All 2,093 admissible variants validated against the item schema and rendered 4,186 formulas without error. Injecting a one-character bug (`>=` to `>`) produced 864 disagreements.

**One schema bug found by running it.** In zod 4 a record keyed by an enum is exhaustive, so revision 1's `Exam.mix: z.record(z.enum(['1', ..., '5']), ...)` rejected every exam that gave no share to difficulty 1, which is every topic exam in design research 8.4. Revision 2 uses `z.partialRecord` there and for generator levels.

The prototypes stay out of the repository: the build stages in section 14 rebuild them properly. Section 10.6 lists what they found in the Stage 1 lesson.

### 0.3 What revision 2 changed, and why

| # | Change | Sections | Source |
|---|---|---|---|
| 1 | Element references use the widgets' `kind:name` ids, prefixed by the widget in content (`grid/cell:5,5`); `staticIds(config)` becomes the static form of `targets()` | 3.2, 3.5, 10, 12.1 | `AI-TUTOR.md` 0.2 settled the id syntax across five catalogues; this paper was the last holdout |
| 2 | `tutor.reps`, `why.rep`; `tutor.focus` required on task screens; the tutor leak lint | 3.2, 3.10, 6.10, 8.4, 9.3 | `AI-TUTOR.md` 4.1 (`ScreenCtx.notes`, `reps`, the outline, `why.rep`) and 8.1 (leak probe) |
| 3 | Long-form checks gain `genre` (proof, derivation, written, results-note) and `marking: tutor-draft \| self`; the marking contract becomes JSON lines with verbatim evidence | 3.2, 7.7 | `AI-TUTOR.md` 2.7 and decision 4. Revision 1's strict tool `record_marks` is withdrawn |
| 4 | `Skill` gains `encompasses`, `exercises`, `pattern` | 3.2 | `ASSESSMENT.md` 4.2 |
| 5 | `ExitPart` becomes the instrument union, with two changes: an id pattern that admits `1.9.exit`, and track names in place of a fixed enum | 3.2 | `ASSESSMENT.md` 2.10. Its ids (`1.9.exit`, `3.3.mocks`) fail its own `LocalId` |
| 6 | `Level.companion`; `Exam.kind` and explicit `forms`; the exam and hours rules in CI | 3.2, 3.8, 6.7 | `ASSESSMENT.md` 3.1, 3.2, 8.7 and 17 |
| 7 | Snapshots only for attempts the learner can revisit | 4.3 | `ASSESSMENT.md` 0.3 |
| 8 | `content/plan.yaml` and its schema | 2.5, 3.2 | `ASSESSMENT.md` 8.9 |
| 9 | Tracks as data (`trk.*`); `Course.tracks` removed | 3.1, 3.2 | `canon-gap.md` 5.2, item 3 |
| 10 | `Source` gains `isbn`, `toc` and the `cc-by-nc-nd` licence; `loc` is checked against `toc` | 3.2, 6.7 | `canon-gap.md` 5.2, item 1, and its licence notes |
| 11 | Runtime tags `micropython-ok`, `ulab-ok`, `pyodide-core`, `web`; `Drill.aim`; the Artifact file budget with Pyodide | 3.2, 6.11, 7.6, 8.2 | `spikes/README.md` (Pyodide on the owner's iPhone); the curriculum files' tags |
| 12 | `GeneratorSpec.desc` and `tutorParams`; `makeWhere` for Bertie's practice picks | 3.2, 5.4 | `AI-TUTOR.md` 2.11 |
| 13 | `Project` (`prj.*`), provisional | 3.1, 3.2, 3.8 | `stage1-statistics-ts.md` and `ASSESSMENT.md` (project instruments) already use project ids |
| 14 | Glossary terms exempt a banned word inside the term (`robust standard errors`) | 6.10 | `stage1-statistics-ts.md`, open item 8 |
| 15 | A table from the curriculum files' quiz letters to check kinds, and the `R` letter clash | 3.4, 13 | `docs/curriculum/*.md` |

**A conflict with the brief.** The brief for this paper states that Pyodide cannot run in the Artifact because the host serves no archives, and that WebAssembly in the Artifact was still being measured. `spikes/README.md`, written after the brief, records both as measured on the owner's iPhone: every probe check passed except service workers, and a repackaged Pyodide (archives split into JSON maps and `.wasm` files, reassembled in a worker) loaded NumPy and pandas and computed correctly. This paper followed the measurement. The brief's MicroPython fallback was later dropped by the owner (decision 18 as tidied), and on 7 October 2026 his publishing rule removed Python from the Artifact altogether (`docs/PLAN.md` revision 2): every drill hands off to the web app. `canon-gap.md` cites `use` values as "decision 3 in section 0.4"; they are `Citation.use` in section 3.2.

---

## 1. Inputs, and what this paper changes in them

**Inputs.** The curriculum (`docs/curriculum.md`), the design research (sections 5, 8, 9 and 10), the prototype lesson (`prototype/js/screens/lesson.js`), the owner's lesson-creator, maths-teaching, code-craft and project-forge skills, and six widget catalogues in this folder: `widgets-stage0.md`, `widgets-calc-linalg.md`, `widgets-prob-stats-ts.md`, `widgets-programming.md`, `widgets-finance-games.md` and `widgets-ml-research.md`. Revision 2 adds the papers written after revision 1, which build on it: `AI-TUTOR.md` (sections 0, 2.7, 2.10, 2.11, 4.1, 8.1), `ASSESSMENT.md` (0.3, 2.10, 3.1, 3.2, 4.2, 8.7, 8.9, 17), `canon-gap.md` (5.2, 6), the seven curriculum files in `docs/curriculum/`, and `spikes/README.md`.

**Names.** Widget type names follow the Stage 0 reconciliation (its section 15.1), which the programming catalogue also adopted: `choice`, `numeric-input`, `expression-input`, `derivation-steps`, `free-response`, `code-cell`, `outcome-grid`, `trial-simulator`, `sim-runner`. The engine paper fixes the final names; renaming is mechanical because content refers to widgets by `type` only.

**Checks.** The catalogues propose four overlapping `Check` unions. This paper merges them into one (section 3.4):

| Catalogue proposal | Becomes |
|---|---|
| `choice`, `multi` (calc-linalg), `choice` with `correct: string[]` (Stage 0) | `choice` with `select: one \| many` |
| `numeric`, `probability` (prob-stats) | `numeric`, with `probability: true` adding the $[0, 1]$ nudge and fraction, decimal and percent forms |
| `expression` (both) | `expression`, with `relation` and `form` |
| `set`, `interval`, `ordering`, `mapping`, `point`, `curve`, `matrix`, `distribution`, `predicate` | kept, fields merged |
| `state` (Stage 0), `policy` (prob-stats) | `predicate` with a registered name (`policy-optimal`) |
| `text` (Stage 0 long form), `free-text` (calc-linalg) | `long-form` |
| `text` (programming, predict the output) | `output` |
| `code` with an inline suite (programming) | `code` naming a drill; the suite lives in the drill's own files (section 3.9) |
| `multi` with parts (calc-linalg) | `parts` |

**Misconceptions.** Calc-linalg keys misconceptions by option inside the check and show-why recipes by misconception. Stage 0 and prob-stats list `{ when: Check, id, line, showWhy }`. Both become one `diagnose` list (section 3.3). Choice options may carry `mc`, `line` and `show` inline, which the compiler lifts into `diagnose`, because option-level feedback is easiest to review beside the option.

**Show-why.** Calc-linalg's declarative recipe (`set`, `highlight`, `annotate`, `ms`) and Stage 0's named recipes (`showWhy(key)`) are both kept: a step is either a widget recipe (`{ widget, recipe, args }`) or a declarative step.

**Generators.** Calc-linalg's interface `make(seed, difficulty)` stays as the runtime call. Its internals change: admissibility is decided at build time over a declared box, and `make` picks from a precomputed index (section 5). The catalogue's property test over 1,000 seeds becomes an exhaustive cross-check against Python where the box allows it.

**Tutor secrets.** Prob-stats decision 9 (a `secret()` block passed to Bertie only in lesson and explore modes) is adopted as `AI-TUTOR.md` settled it: the widget's `secret()` and the checker's summary of the check travel in a sealed answer block, and every reply passes a leak probe. The compiler supplies the content side: the check summary, accepted forms and diagnosis keys of the current screen (section 8.4).

**Element ids.** `AI-TUTOR.md` 0.2 chose the `kind:name` element ids (`cell:5,3`) and Stage 0's `targets()` method for every widget. Revision 2 adopts both (decision 17), replacing revision 1's `grid:cell-5-3` and `staticIds()`.

---

## 2. Authoring format

### 2.1 The decision

Lessons, items, sets, exams and libraries are **YAML 1.2 files under a strict profile**. Prose fields use **ZQ Markdown**, a small inline dialect. Generators are **TypeScript modules** with a **YAML spec** and a **Python verifier** beside them. Code drills keep code in **`.py` files** beside a `drill.yaml`.

Three measurements drove it [measured on the section 10 lesson]:

- **Copy is a minority of the file.** About 210 of the lesson's 793 lines carry learner-facing copy; the rest is structure: widget configs, checks, diagnoses, verify blocks, tutor fields, references. A format built around prose puts most of the file in its awkward corner.
- **Escaping corrupts maths silently.** While this paper was being prepared, an escaped `\t` inside a quoted string became a tab character, and KaTeX rendered `\tfrac{0.12}{0.30}` as the letters "frac" followed by the numbers, without any error. Formats that need backslash escaping (JSON, TypeScript strings, YAML double quotes) invite this on every formula. YAML single quotes and block scalars need none.
- **Diffs.** The owner reviews agent-written content as pull requests. In YAML with one sentence per line, a wording change is a one-line diff, and a change to an answer shows up as a change to `value:` or `correct:`, which section 4 then forces through a `rev` bump.

### 2.2 Rejected formats

The same piece of content, option D of the `first5` screen in the prototype, in each format:

```yaml
# YAML (chosen)
- id: d
  value: 5/6
  mc: mc.prob.complement-confusion
  line: That is the chance the total is not 8. Count the cells that do reach 8.
  show: [{ widget: grid, recipe: flash, args: { cells: ['cell:5,1', 'cell:5,2', 'cell:5,4', 'cell:5,5', 'cell:5,6'] } }]
```

```ts
// TypeScript module
{ id: 'd', value: '5/6', mc: 'mc.prob.complement-confusion',
  line: 'That is the chance the total is not 8. Count the cells that do reach 8.',
  show: [{ widget: 'grid', recipe: 'flash', args: { cells: ['cell:5,1', 'cell:5,2', 'cell:5,4', 'cell:5,5', 'cell:5,6'] } }] },
```

```md
<!-- Markdown with directives -->
:::option{#d value="5/6" mc="mc.prob.complement-confusion"}
That is the chance the total is not 8. Count the cells that do reach 8.
::show{widget=grid recipe=flash cells="cell:5,1;cell:5,2;cell:5,4;cell:5,5;cell:5,6"}
:::
```

```mdx
{/* MDX */}
<Option id="d" value="5/6" mc="mc.prob.complement-confusion"
  show={[{ widget: 'grid', recipe: 'flash', args: { cells: ['cell:5,1', 'cell:5,2', 'cell:5,4', 'cell:5,5', 'cell:5,6'] } }]}>
  That is the chance the total is not 8. Count the cells that do reach 8.
</Option>
```

| Format | Strength | Why rejected |
|---|---|---|
| Markdown with frontmatter and directives (MyST, remark-directive) | Prose reads naturally | Nested structure (a widget inside a screen inside a lesson, with option lists and recipes) needs either directive attributes, which flatten arrays into strings as above, or YAML inside directive bodies, which means two grammars, two parsers and error positions in neither. With about three quarters of lines structural, most authoring would happen in the weak half |
| MDX | Components read like the rendered page | Content becomes executable JavaScript, which contradicts "content is data" and the reason for this paper (the Stage 1 lesson's defects were in code). JSX attribute diffs are noisy; props holding arrays are JavaScript expressions that schemas cannot see until run |
| TypeScript modules | Types and autocompletion; generators in the same file | Every TeX backslash doubles (`'\\dfrac{5}{36}'`), which is the escape trap above. Logic creeps in, as it did in the prototype. Kept for generators only, where logic is the point |
| JSON | Exact, universal | No comments, every string quoted, every backslash escaped, no multi-line strings |
| TOML | Simple | Arrays of tables nest poorly at the depth of screens, widgets and options |
| A custom DSL | Could be terse | A grammar, a parser, an editor mode and error messages to maintain, for a format agents have never seen |

### 2.3 The strict YAML profile

Parsed with the `yaml` package (2.9.1, ISC) as YAML 1.2 with the core schema [measured version]. The compiler rejects:

| Rule | Why |
|---|---|
| Anchors, aliases and merge keys (`&a`, `*a`, `<<:`) | Hidden sharing makes a diff lie about what changed. Reuse goes through `from:` (section 3.5), which is explicit |
| Custom tags (`!foo`) | No executable or typed extensions |
| Duplicate keys | Silent last-wins overwrites |
| Double-quoted strings that contain a backslash | The escape trap. Use single quotes or a block scalar |
| Control characters other than newline, in any string | Catches the tab that an escaped `\t` leaves behind |
| Non-integer numbers in answer positions (`value`, `range`, matcher values) | Answers stay exact: write `'0.25'` or `1/4` |

YAML 1.2 already fixes the classic 1.1 traps (`no` and `yes` are strings; octal needs `0o`). Values such as `1.10` would still parse as numbers, which is why topic numbers are typed as strings in the schema and the formatter quotes them.

**Formatter.** `zq fmt` rewrites every file into one canonical style, so agents cannot produce churn: key order fixed by the schema, two-space indents, flow style for short maps of scalars, folded block scalars (`>-`) for prose longer than one line or containing `: `, one sentence per line inside them, single quotes for TeX. `zq check` fails on any file that `zq fmt` would change.

### 2.4 ZQ Markdown

Prose fields (`prose`, `question`, `line`, hints, `why`, solutions, summaries, model answers) accept:

| Syntax | Meaning |
|---|---|
| Plain text, folded across lines | One paragraph; a blank line inside a literal block (`\|-`) starts another |
| `**bold**`, `*italic*`, `` `code` `` | Emphasis and inline code |
| `$...$` | Inline maths. Opening `$` must be followed by a non-space; closing `$` must follow a non-space and must not be followed by a digit, so `costs $5 or $10` stays text (Pandoc's rule) |
| `$$...$$` | Display maths, on its own line |
| `\$` | A literal dollar sign |
| `[text](gls.prob.conditional-probability)` | A link to a glossary term, lesson (`lsn.`), card (`crd.`) or item (`itm.`) |
| `- item` | A list, only in summary ideas, solution steps and model answers |
| `{{path}}`, `{{#if path}}...{{else}}...{{/if}}` | Template values, only in feedback and explanation fields (section 3.6) |

Nothing else: no headings, HTML, images, tables or external links (those belong in `sources` and `notes`). The compiler turns each field into a compact token list, so the runtime has no Markdown parser and no `innerHTML` sink other than KaTeX's own output:

```json
[["t","That is a "],["l","gls.prob.conditional-probability",[["t","conditional probability"]]],["t",": "],["m","P(A \\mid B)"],["t",", the probability of "],["m","A"],["t"," given "],["m","B"],["t","."]]
```

### 2.5 File layout

Folders are for people; ids are identity. Moving or renaming a file changes nothing a learner can see.

```
content/
├── curriculum.yaml                 stages, topic order and tracks (trk.*); CI compares it with docs/curriculum.md
├── plan.yaml                       track orders, alongside rules, habits, deferrals (ASSESSMENT.md 8.9)
├── sources.yaml                    bibliography, src.* ids, editions and tables of contents
├── tex-macros.yaml                 KaTeX macros shared by build, preview and runtime
├── words.txt                       project dictionary for the spelling lint
├── migrations.yaml                 append-only learner-state migrations (section 4.5)
├── ids.lock.json                   every published id with kind, rev and answer hash; written by the release job only
├── topics/
│   └── 1.5-probability/
│       ├── topic.yaml              top.probability: cover list, resources, exit test, courses, exam
│       ├── skills.yaml             skl.prob.*
│       ├── misconceptions.yaml     mc.prob.*
│       ├── glossary.yaml           gls.prob.*
│       ├── notation.yaml           the topic's notation card
│       ├── exam.yaml               exm.prob.topic
│       └── conditional-probability/
│           ├── course.yaml         crs.cond
│           └── l1-updating-on-evidence/
│               ├── level.yaml      lesson order, level review, homework
│               ├── shrinking-the-sample-space.lesson.yaml
│               ├── bank.items.yaml practice, review and homework items
│               └── homework.set.yaml
├── generators/
│   └── prob/
│       ├── two-dice-conditional.gen.yaml     box, phrasebook, levels, semantics
│       ├── two-dice-conditional.gen.ts       accept, level, answer, diagnoses, build
│       ├── two-dice-conditional.verify.py    independent accept, level, answer, diagnoses
│       └── two-dice-conditional.golden.json  item hashes for fixed seeds
├── drills/
│   └── cond-p-given/
│       ├── drill.yaml              brief, mode, examples, edge cases, wrong solutions
│       ├── starter.py
│       ├── reference.py
│       ├── tests.py
│       └── wrong/denominator-36.py
├── projects/
│   └── backtest/project.yaml       prj.* brief, milestones, results-note item
└── assets/
    ├── assets.yaml                 ast.* ids, alt text, origin, licence
    └── art/probability-tree.svg
packages/
├── content-schema/                 zod schemas, inferred types, JSON Schema export      [TypeScript]
├── content-compiler/               the zq CLI: fmt, check, verify, build, preview        [TypeScript, Node 22]
├── graders/                        runtime graders, shared with CI replay               [TypeScript]
└── gen-kit/                        @zq/gen: defineGenerator, exact rationals, phrases    [TypeScript]
tools/
└── zqverify/                       independent verifier, uv-managed, pinned SymPy, NumPy, SciPy, statsmodels, mpmath  [Python 3.12]
```

The engine paper owns the rest of the repository tree.

---

## 3. Content model and schema

### 3.1 Hierarchy

```
Stage (stg.*)            curriculum.yaml; closed by the stage exit parts
 └ Topic (top.*)         numbered item such as 1.5; closed by the topic exam (exm.*) and its exit parts
    └ Course (crs.*)     1 to 5 per topic
       └ Level (lvl.*)   4 to 7 lessons, a level review, a homework set (set.*), companion reading and exercises
          └ Lesson (lsn.*)   8 to 12 screens, 10 to 15 minutes, a quiz of 3 to 5 items
             └ Screen     local id inside the lesson: one task
Tracks (trk.*): curriculum.yaml; each marks topics and courses core, elective, optional or absent
Libraries per topic: skills (skl.*), misconceptions (mc.*), glossary terms (gls.*), notation
Shared: items (itm.*), generators (gen.*), code drills (drl.*), projects (prj.*), sources (src.*), cards (crd.*), assets (ast.*)
```

A parent lists its children in order; a child never names its parent. Ordering therefore lives in one place, and the compiler rejects a lesson that no level lists, or that two levels list.

### 3.2 The schema

One package, `packages/content-schema`, holds every schema. The compiler validates source files with it, the runtime validates bundles with it, and `z.toJSONSchema` emits `schemas/*.schema.json` so the owner's editor and the authoring agents get completion and inline errors (the lesson file's first line points at it). The listing below is the file that validated the worked example and the revision 2 fixtures, in full. Two blocks belong to other papers and are copied here so the schema is complete in one place: the exit-part instruments (`ASSESSMENT.md` 2.10) and the plan (`ASSESSMENT.md` 8.9). Those papers own their meaning; this package owns their syntax.

```ts
// packages/content-schema/src/index.ts (zod 4). Shared by the compiler, the preview route and the runtime.
import { z } from 'zod';

/* ---------- 1. Identifiers ---------- */
export const KINDS = ['stg', 'top', 'trk', 'crs', 'lvl', 'lsn', 'itm', 'set', 'exm', 'prj', 'mc', 'skl', 'gen', 'drl', 'src', 'gls', 'crd', 'ast'] as const;
export type Kind = (typeof KINDS)[number];
const SEG = '[a-z0-9]+(?:-[a-z0-9]+)*';
export const Id = (k: Kind) =>
  z.string().max(80).regex(new RegExp(`^${k}\\.${SEG}(?:\\.${SEG}){0,3}$`), `expected an id of the form ${k}.namespace.name`);
export const LocalId = z.string().regex(/^[a-z][a-z0-9-]{0,31}$/);   // screen, widget, option, part, line, diagnosis key
// Element ids are the widgets' own kind:name ids (AI-TUTOR.md 0.2). Content always names the widget too, so adding a
// second widget to a screen later cannot make an old reference ambiguous.
export const ElementId = z.string().regex(/^[a-z][a-z0-9-]{0,23}:[a-z0-9][a-z0-9,._-]{0,47}$/);                       // 'cell:5,5'
export const ElementRef = z.string().regex(/^[a-z][a-z0-9-]{0,31}\/[a-z][a-z0-9-]{0,23}:[a-z0-9][a-z0-9,._-]{0,47}$/);  // 'grid/cell:5,5'
export const WidgetFrom = z.string().regex(/^[a-z][a-z0-9-]{0,31}\/[a-z][a-z0-9-]{0,31}$/);                            // 'shade/grid'
export const ScreenRef = z.string().regex(new RegExp(`^lsn\\.${SEG}(?:\\.${SEG}){0,3}#[a-z][a-z0-9-]{0,31}$`));

/* ---------- 2. Atoms ---------- */
export const Prose = z.string().min(1).max(1200);            // ZQ Markdown; copy lints run in the compiler
export const Tex = z.string().min(1).max(400);               // KaTeX source without delimiters
export const NumValue = z.union([z.number().int(), z.string().min(1).max(200)]);   // integer, '10/109' or an exact expression
export const Difficulty = z.number().int().min(1).max(5);
export const Rev = z.number().int().min(1);
export const Status = z.enum(['draft', 'review', 'live', 'retired']);
export const Seconds = z.number().int().min(10).max(3600);
export const Rep = z.enum(['picture', 'count', 'algebra', 'analogy', 'simulation', 'code']);   // representations, AI-TUTOR.md 4.1
export const Tol = z.object({ abs: z.number().nonnegative().optional(), rel: z.number().nonnegative().max(0.5).optional() })
  .refine(t => t.abs !== undefined || t.rel !== undefined, 'give abs, rel or both');

export const Citation = z.object({
  src: Id('src'),
  loc: z.string().min(1).max(120),                           // 'ch. 2, sec. 2.2', 'Lecture 4', 'PS 3, q. 2'
  use: z.enum(['basis', 'parallel-reading', 'problem-adapted', 'problem-inspired', 'further']),
  checked: z.boolean().default(false),                       // location confirmed against the source by a person
  note: z.string().max(200).optional(),
}).strict();

export const TutorNotes = z.object({
  focus: z.string().max(200).optional(),                     // what this screen is for, in one line; the tutor's outline title
  notes: z.string().max(600).optional(),                     // where learners get stuck; what a good nudge looks like
  reps: z.array(Rep).max(3).default([]),                     // representations that work here, for Bertie's why and explain
  avoid: z.array(z.string().max(80)).max(6).default([]),     // things Bertie must not say here (besides the answer)
}).strict();

/* ---------- 3. Feedback: hints, show-why, diagnoses, explanations ---------- */
export const Hints = z.object({
  nudge: Prose,                                              // a question back to the learner
  point: z.object({ text: Prose, highlight: z.array(ElementRef).min(1).max(4) }).strict(),
  step: Prose,                                               // the first step of the solution, worked
}).strict();

export const ShowStep = z.union([
  z.object({ widget: LocalId, recipe: z.string().regex(/^[a-z][a-z0-9-]*$/), args: z.record(z.string(), z.unknown()).optional() }).strict(),
  z.object({
    set: z.record(z.string(), z.union([z.number(), z.string()])).optional(),      // tween non-answer widget variables
    highlight: z.array(ElementRef).max(6).optional(),
    annotate: z.array(z.object({ at: ElementRef, text: z.string().max(80) }).strict()).max(3).optional(),
    ms: z.number().int().min(300).max(1200).optional(),
  }).strict(),
]);

const SetSel = z.union([z.enum(['none', 'some']), z.array(ElementId).min(1)]);
export const Matcher = z.discriminatedUnion('kind', [
  z.object({ kind: z.literal('option'), ids: z.array(LocalId).min(1) }).strict(),
  z.object({ kind: z.literal('value'), value: NumValue, tol: Tol.optional() }).strict(),
  z.object({ kind: z.literal('range'), lo: NumValue, hi: NumValue }).strict(),
  z.object({ kind: z.literal('expr'), equals: z.string() }).strict(),
  z.object({ kind: z.literal('set'), missing: SetSel.optional(), extra: SetSel.optional() }).strict(),
  z.object({ kind: z.literal('order'), first: LocalId.optional(), swapped: z.tuple([LocalId, LocalId]).optional() }).strict(),
  z.object({ kind: z.literal('predicate'), name: z.string().regex(/^[a-z][a-z0-9-]*$/), args: z.record(z.string(), z.unknown()).optional() }).strict(),
  z.object({ kind: z.literal('test'), failing: z.string() }).strict(),
]);

export const Diagnosis = z.object({
  key: LocalId.optional(),                                   // named so verify.diagnose can prove what this misconception produces
  match: Matcher,
  mc: Id('mc').optional(),
  slip: z.literal(true).optional(),                          // a slip, not a misconception
  line: Prose,                                               // verdict-chip line; may use {{template}} values
  show: z.array(ShowStep).max(4).optional(),
}).strict().refine(d => (d.mc === undefined) !== (d.slip === undefined), 'name a misconception (mc) or set slip: true, not both');

export const Why = z.object({
  rep: Rep,                                                  // the representation this explanation uses; Bertie picks another
  yours: Prose.optional(),                                   // after a correct answer: about the learner's own action
  shown: Prose.optional(),                                   // after a wrong answer or Show solution: no "you"
  then: Prose,                                               // shared remainder; the whole explanation is at most 3 sentences
}).strict();

export const Solution = z.object({
  line: Prose,                                               // verdict-chip text on Show solution
  steps: z.array(z.object({ text: Prose, tex: Tex.optional(), because: z.string().max(160).optional() }).strict()).optional(),
}).strict();

/* ---------- 4. Checks (answer specs) ---------- */
const NumForm = z.enum(['integer', 'decimal', 'fraction', 'mixed', 'percent', 'standard-form']);
const ExprForm = z.enum(['any', 'expanded', 'factorised', 'single-fraction', 'simplest-fraction', 'surd', 'a+bi', 'index']);
const VarDomain = z.object({ lo: z.number(), hi: z.number(), integer: z.boolean().default(false), avoid: z.array(z.number()).default([]) }).strict();
export const Unit = z.union([
  z.string().max(24),                                        // display label only: 'outcomes', 'rolls'
  z.object({ symbol: z.enum(['£', '$', '€', '%', 'bp', 'ms', 's', 'days', 'years']), at: z.enum(['prefix', 'suffix']).default('suffix'),
             convert: z.boolean().default(false) }).strict(),
]);
const Feature = z.object({
  kind: z.enum(['zero', 'extremum', 'sign', 'concavity', 'monotone', 'asymptote']),
  at: z.number().optional(), on: z.tuple([z.number(), z.number()]).optional(),
  value: z.union([z.number(), z.string()]).optional(), tol: z.number().positive().optional(),
}).strict();
const ModelLine = z.object({ id: LocalId, text: Prose.optional(), tex: Tex.optional(), because: z.string().max(160).optional() }).strict();
const RubricPoint = z.object({ id: LocalId, point: Prose, marks: z.number().int().min(1).max(3).default(1), evidence: z.array(LocalId).min(1) }).strict();
const StepTag = z.string().regex(/^[a-z][a-z0-9-]{1,40}$/);   // a sub-step of a skill: diagnosis, hints, the gap report; never an FSRS card
const CodeRef = z.object({ kind: z.literal('code'), drill: Id('drl') }).strict();

const BaseChecks = [
  z.object({ kind: z.literal('choice'), correct: z.union([LocalId, z.array(LocalId).min(1)]),
             select: z.enum(['one', 'many']).default('one'), partial: z.boolean().default(false) }).strict(),
  z.object({ kind: z.literal('numeric'), value: NumValue, tol: Tol.optional(), range: z.tuple([NumValue, NumValue]).optional(),
             integer: z.boolean().default(false), probability: z.boolean().default(false),
             forms: z.array(NumForm).min(1).default(['integer', 'decimal', 'fraction']),
             fractionsExact: z.boolean().default(true),
             requireForm: z.enum(['fraction', 'simplest-fraction', 'standard-form']).optional(),
             sf: z.number().int().min(1).max(10).optional(), dp: z.number().int().min(0).max(10).optional(),
             unit: Unit.optional(), autoDiagnose: z.boolean().default(true) }).strict(),
  z.object({ kind: z.literal('expression'), equals: z.string().min(1), vars: z.record(z.string(), VarDomain),
             relation: z.enum(['equal', 'equation', 'inequality', 'antiderivative', 'up-to-constant']).default('equal'),
             form: ExprForm.default('any'), assume: z.array(z.string()).default([]) }).strict(),
  z.object({ kind: z.literal('set'), correct: z.union([z.array(ElementId).min(1), z.object({ where: z.string() }).strict()]),
             partial: z.boolean().default(false) }).strict(),
  z.object({ kind: z.literal('interval'), correct: z.string() }).strict(),                     // '[3.35, 3.45)', unions with 'U'
  z.object({ kind: z.literal('ordering'), order: z.array(LocalId).min(2),
             before: z.array(z.tuple([LocalId, LocalId])).optional(),                      // partial order: any order meeting these is right
             exclude: z.array(LocalId).default([]),                                        // distractor lines that must be left out
             marks: z.enum(['all-or-nothing', 'per-position', 'longest-run']).default('all-or-nothing') }).strict(),
  z.object({ kind: z.literal('mapping'), pairs: z.array(z.tuple([LocalId, LocalId])).min(1) }).strict(),
  z.object({ kind: z.literal('point'), target: z.array(z.array(z.number()).min(1)).min(1), tol: z.number().positive(),
             metric: z.enum(['euclid', 'x', 'y', 'angle', 'angle-mod-pi']).default('euclid') }).strict(),
  z.object({ kind: z.literal('curve'), target: z.string(), band: z.number().positive(), coverage: z.number().min(0.5).max(1),
             features: z.array(Feature).default([]) }).strict(),
  z.object({ kind: z.literal('matrix'), equals: z.array(z.array(NumValue).min(1)).min(1), tol: z.number().nonnegative().optional(),
             relation: z.enum(['equal', 'echelon-row-equivalent', 'rref', 'columns-up-to-scale', 'orthonormal-columns']).default('equal') }).strict(),
  z.object({ kind: z.literal('distribution'), support: z.array(z.union([z.number(), z.string()])).min(1), masses: z.array(NumValue).min(1),
             metric: z.enum(['exact', 'tv', 'max-abs']).default('exact'), tol: z.number().nonnegative().optional() }).strict(),
  z.object({ kind: z.literal('predicate'), name: z.string().regex(/^[a-z][a-z0-9-]*$/), args: z.record(z.string(), z.unknown()).default({}) }).strict(),
  z.object({ kind: z.literal('output'), expect: z.union([z.string(), z.array(z.string()).min(1)]),
             compare: z.enum(['exact', 'normalised-ws', 'lines-unordered', 'regex']).default('normalised-ws') }).strict(),
  z.object({ kind: z.literal('resultset'), columns: z.array(z.string()).min(1), rows: z.array(z.array(z.unknown())),
             ordered: z.boolean().default(false), floatTol: z.number().nonnegative().optional() }).strict(),
  CodeRef,
  z.object({ kind: z.literal('long-form'), genre: z.enum(['proof', 'derivation', 'written', 'results-note']),
             scale: z.union([z.literal(10), z.literal(3)]).default(10),                  // 3: a quiz production item (review addition)
             rubric: z.array(RubricPoint).min(2).max(10), model: z.array(ModelLine).min(1),
             consequence: Prose.optional(),                                             // "would fail in production because ...", on result screens
             marking: z.enum(['tutor-draft', 'self']).default('tutor-draft'),               // AI-TUTOR.md 2.7
             minWords: z.number().int().min(0).max(400).default(0) }).strict()
    .refine(c => c.rubric.reduce((s, p) => s + p.marks, 0) === c.scale, 'rubric marks must total the scale')
    .refine(c => c.scale === 3 ? c.rubric.length <= 3 : c.rubric.length >= 4 && c.model.length >= 2, 'a 10-point rubric has 4 to 10 points; a 3-point one at most 3'),
] as const;
const BaseCheck = z.discriminatedUnion('kind', BaseChecks);
export const Check = z.union([
  BaseCheck,
  z.object({ kind: z.literal('parts'), parts: z.record(LocalId, BaseCheck) }).strict(),       // multi-part: green parts lock, amber reopen
]);

/* ---------- 5. Verification specs (CI only; never shipped) ---------- */
export const Space = z.union([
  z.object({ dice: z.array(z.number().int().min(2).max(20)).min(1).max(4) }).strict(),
  z.object({ coins: z.number().int().min(1).max(12) }).strict(),
  z.object({ product: z.array(z.array(z.union([z.string(), z.number()])).min(1)).min(1).max(4) }).strict(),
  z.object({ draw: z.object({ from: z.union([z.literal('deck'), z.record(z.string(), z.number().int().min(1))]),
                              k: z.number().int().min(1).max(6), ordered: z.boolean(), replace: z.boolean() }).strict() }).strict(),
]);
export const Verify = z.object({
  space: Space.optional(),
  let: z.record(z.string().regex(/^[A-Z][A-Za-z0-9]*$/), z.string()).optional(),   // named events: { A: 'a + b == 10' }
  answer: z.string().optional(),                     // independent value; must equal the check's declared answer
  set: z.string().optional(),                        // independent outcome set; must equal a resolved `where` set
  expect: z.union([z.number().int(), z.string()]).optional(),   // the author's own claim about a resolved value (a count)
  options: z.record(LocalId, z.string()).optional(), // value of each choice option on this instance
  diagnose: z.record(LocalId, z.string()).optional(),// value each named misconception produces
  chain: z.object({ lines: z.array(LocalId).min(2), bind: z.record(z.string(), z.string()) }).strict().optional(),
  simulate: z.union([z.boolean(), z.object({ trials: z.number().int().min(10_000).max(100_000_000) }).strict()]).optional(),
  script: z.string().regex(/^[a-z0-9/._-]+\.verify\.py$/).optional(),   // escape hatch, sandboxed in CI
}).strict();

/* ---------- 6. Widgets on a screen ---------- */
export const WidgetUse = z.object({
  id: LocalId,
  type: z.string().regex(/^[a-z][a-z0-9-]*$/).optional(),
  v: z.number().int().min(1).optional(),            // widget major version this config targets
  from: WidgetFrom.optional(),                       // start from that screen's widget config; fields here merge over it
  label: z.string().max(160).optional(),             // accessible name; also how Bertie names the widget
}).catchall(z.unknown())                             // the rest is validated by the widget's own schema in the compile step
  .refine(w => w.from !== undefined || (w.type !== undefined && w.v !== undefined && w.label !== undefined),
          'a widget needs type, v and label, or from');

/* ---------- 7. Screens ---------- */
export const Card = z.object({
  id: Id('crd'), title: z.string().max(60), tex: Tex, conditions: Prose.optional(),
  derivedIn: z.union([LocalId, ScreenRef]),          // where the formula is derived; never stated without a derivation
}).strict();

const ScreenBase = {
  id: LocalId,
  prose: Prose.optional(),                           // at most 60 words (lint)
  caption: z.string().max(60).optional(),            // canvas caption bar
  skills: z.array(Id('skl')).max(3).default([]),
  difficulty: Difficulty.optional(),
  context: z.literal('quant').optional(),            // transfer screens (design 8.3 step 7)
  enter: z.array(ShowStep).max(4).optional(),        // played when the screen opens
  tutor: TutorNotes.optional(),                      // required on task screens by the checklist (section 9.3, rule 31)
  notes: z.string().max(2000).optional(),            // author notes; never shipped
};
const TaskFields = {
  question: Prose,
  canvas: z.array(WidgetUse).max(3).default([]),
  input: WidgetUse.optional(),
  answer: LocalId.optional(),                        // the widget whose answer() is graded; default input.id
  layout: z.enum(['canvas-first', 'input-first']).default('canvas-first'),
  check: Check,
  diagnose: z.array(Diagnosis).max(8).default([]),
  otherwise: Prose.optional(),                       // fallback verdict line; required unless every wrong answer is diagnosed
  reason: Prose,                                     // verdict-chip line after a correct answer
  hints: Hints,
  why: Why,
  solution: Solution,
  accepted: Prose.optional(),                        // overrides the generated accepted-answer rule
  after: z.array(ShowStep).max(4).optional(),        // played on correct or reveal
  verify: Verify.optional(),
  est: Seconds.optional(),
};
const needsAnswerWidget = (s: { input?: unknown; answer?: string }) => s.input !== undefined || s.answer !== undefined;
const answerMsg = 'a task screen needs an input widget or an answer: naming a canvas widget';

export const Screen = z.discriminatedUnion('type', [
  z.object({ type: z.literal('title'), ...ScreenBase, art: Id('ast').optional() }).strict(),
  z.object({ type: z.literal('explore'), ...ScreenBase, canvas: z.array(WidgetUse).min(1).max(3),
             continueWhen: z.object({ predicate: z.string(), args: z.record(z.string(), z.unknown()).optional() }).strict().optional() }).strict(),
  z.object({ type: z.literal('problem'), ...ScreenBase, ...TaskFields }).strict().refine(needsAnswerWidget, answerMsg),
  z.object({ type: z.literal('ladder'), ...ScreenBase, ...TaskFields, constraint: z.string().max(80) }).strict().refine(needsAnswerWidget, answerMsg),
  z.object({ type: z.literal('demonstrate'), ...ScreenBase, canvas: z.array(WidgetUse).min(1).max(3) }).strict(),
  z.object({ type: z.literal('trap'), ...ScreenBase, ...TaskFields, trap: z.object({ mc: Id('mc'), bait: LocalId }).strict() }).strict().refine(needsAnswerWidget, answerMsg),
  z.object({ type: z.literal('generalise'), ...ScreenBase, ...TaskFields, rule: Prose, tex: Tex.optional() }).strict().refine(needsAnswerWidget, answerMsg),
  z.object({ type: z.literal('derive'), ...ScreenBase, ...TaskFields,
             leap: z.object({ naive: Prose, fails: Prose, pointsTo: Prose }).strict().optional() }).strict().refine(needsAnswerWidget, answerMsg),
  z.object({ type: z.literal('code'), ...ScreenBase, drill: Id('drl'), question: Prose, reason: Prose, hints: Hints, why: Why }).strict(),
  z.object({ type: z.literal('summary'), ...ScreenBase, ideas: z.array(Prose).length(3), card: Card.optional(), trap: Prose }).strict(),
]);

/* ---------- 8. Items ---------- */
const ItemUse = z.enum(['quiz', 'practice', 'review', 'homework', 'exam']);
const ItemHead = {
  id: Id('itm'), rev: Rev, status: Status.default('draft'),
  title: z.string().max(60),                         // homework lists and the Redo queue
  use: z.array(ItemUse).min(1),
  heldOut: z.boolean().default(false),               // exam-only; practice never shows it
  steps: z.array(StepTag).max(6).default([]),        // sub-steps exercised (ASSESSMENT.md 4.1); no card
  sibling: Id('itm').optional(),                     // same skill, different story; required on long-form homework and paper items (CI)
  imitates: z.string().regex(/^[a-z-]+-[0-9a-z.]+$/).optional(),   // the book problem a recreated problem follows, e.g. zhou-4.12 (ASSESSMENT.md 10.3)
};
export const AuthoredItem = z.object({
  ...ItemHead,
  calculator: z.enum(['none', 'basic', 'scientific', 'any']).default('any'),
  prompt: Prose.optional(),
  ...TaskFields,
  hints: Hints.optional(),                           // lesson screens need hints; items only for help-enabled practice
  difficulty: Difficulty,
  skills: z.array(Id('skl')).min(1).max(3),
  est: Seconds,
  marks: z.number().int().min(1).max(10).optional(), // default: difficulty; long-form: 10
  tutor: TutorNotes.optional(),                      // read only after the item is graded (AI-TUTOR.md 2.12)
  sources: z.array(Citation).default([]),
}).strict();
export const PinnedItem = z.object({
  ...ItemHead,
  from: z.object({ gen: Id('gen'), v: z.number().int().min(1), params: z.record(z.string(), z.union([z.number(), z.string()])) }).strict(),
}).strict();
export const Item = z.union([PinnedItem, AuthoredItem]);

/* ---------- 9. Lesson ---------- */
export const Lesson = z.object({
  zq: z.literal(1),
  id: Id('lsn'), rev: Rev, status: Status,
  title: z.string().min(3).max(60),
  summaryLine: z.string().max(140),
  frame: z.object({ why: Prose, before: Prose.optional() }).strict(),   // lesson-creator: the problem this concept solves
  insight: Prose,                                                      // maths-teaching: the one-line aha
  introduces: z.array(Id('skl')).min(1).max(2),     // level grain (ASSESSMENT.md 4.1); finer distinctions go in `steps`
  steps: z.array(StepTag).max(8).default([]),
  fastPath: z.object({ check: Id('itm') }).strict().optional(),   // "Skip to the trap" behind one sharp item (rule 35)
  uses: z.array(Id('skl')).default([]),
  requires: z.array(Id('lsn')).default([]),
  terms: z.array(Id('gls')).default([]),
  misconceptions: z.array(Id('mc')).min(1),
  edgeCases: z.array(z.object({ case: Prose, at: LocalId.or(Id('itm')) }).strict()).min(1),
  workedExample: z.object({ at: LocalId, naive: Prose, decision: Prose }).strict(),
  est: z.object({ minutes: z.number().int().min(5).max(20) }).strict(),
  sources: z.array(Citation).min(1),
  art: Id('ast').optional(),
  screens: z.array(Screen).min(8).max(12),
  quiz: z.array(Item).min(3).max(5),
  changelog: z.array(z.object({ rev: Rev, date: z.iso.date(), note: z.string().max(200), notify: z.boolean().default(false) }).strict()).default([]),
  authorship: z.object({ drafted: z.string(), reviewed: z.array(z.string()).default([]) }).strict(),
}).strict();

/* ---------- 10. Libraries ---------- */
export const Skill = z.object({                      // ASSESSMENT.md 4.2 adds encompasses, exercises and pattern
  id: Id('skl'), name: z.string().max(80), topic: Id('top'), description: Prose,
  requires: z.array(Id('skl')).default([]),                       // needed before this skill can be learned
  encompasses: z.array(z.object({ id: Id('skl'), w: z.number().min(0.1).max(1) }).strict()).default([]),
                                                                  // exercised as a component every time this skill is used
  exercises: z.array(Citation).default([]),                       // textbook exercises for remediation and companion work
  pattern: z.boolean().default(false),                            // an interview pattern (ASSESSMENT.md 10)
}).strict();
export const Misconception = z.object({
  id: Id('mc'), name: z.string().max(80),
  belief: Prose,                                     // the wrong model, as a learner would put it
  correction: Prose,                                 // the right model, in one or two sentences
  signs: z.array(z.string().max(160)).min(1),        // answers it produces
  sources: z.array(Citation).default([]),
}).strict();
export const Term = z.object({ id: Id('gls'), term: z.string().max(60), aliases: z.array(z.string()).default([]),
  short: Prose, notation: Tex.optional(), introducedIn: ScreenRef, related: z.array(Id('gls')).default([]) }).strict();
export const Source = z.object({
  id: Id('src'), kind: z.enum(['textbook', 'lecture-series', 'problem-set', 'exam', 'paper', 'course', 'website', 'docs']),
  title: z.string(), authors: z.array(z.string()).min(1), year: z.number().int(), edition: z.string().optional(),
  publisher: z.string().optional(), url: z.url().optional(), isbn: z.string().regex(/^[0-9X-]{10,17}$/).optional(),
  licence: z.enum(['copyright', 'cc-by', 'cc-by-sa', 'cc-by-nc', 'cc-by-nc-sa', 'cc-by-nc-nd', 'public-domain', 'other']),
  free: z.boolean(),
  toc: z.record(z.string(), z.string()).optional(), // chapter or lecture number to title, for the pinned edition (canon-gap.md 5.2)
}).strict();
export const Asset = z.object({ id: Id('ast'), file: z.string().regex(/^[a-z0-9/_-]+\.(svg|png|webp|jpg)$/), alt: z.string().min(1).max(300),
  origin: z.enum(['original', 'generated', 'third-party']), licence: z.string().optional() }).strict();

/* ---------- 11. Structure above the lesson ---------- */
const Companion = z.object({                         // outside reading and exercises that go with a level (ASSESSMENT.md 17)
  src: Id('src'), loc: z.string().min(1).max(120), exercises: z.string().max(200).optional(),
  hours: z.number().positive().max(40), checked: z.boolean().default(false) }).strict();
export const Level = z.object({ zq: z.literal(1), id: Id('lvl'), rev: Rev, title: z.string().max(60), summaryLine: z.string().max(140),
  lessons: z.array(Id('lsn')).min(4).max(7),
  review: z.object({ count: z.number().int().min(6).max(10), difficulty: z.tuple([Difficulty, Difficulty]).default([2, 4]) }).strict(),
  homework: Id('set'), bank: z.array(Id('itm')).default([]), generators: z.array(Id('gen')).default([]),
  companion: z.array(Companion).default([]) }).strict();
export const Course = z.object({ zq: z.literal(1), id: Id('crs'), rev: Rev, title: z.string().max(60), summaryLine: z.string().max(140),
  description: Prose, levels: z.array(Id('lvl')).min(1), primary: Citation, accent: z.string() }).strict();

// Exit parts: from ASSESSMENT.md 2.10, which owns them; two changes, section 3.2 notes.
const Instrument = z.discriminatedUnion('kind', [
  z.object({ kind: z.literal('exam'), exam: Id('exm'), pass: z.number().min(0.5).max(1) }).strict(),
  z.object({ kind: z.literal('drill'), drills: z.array(Id('drl')).min(1) }).strict(),
  z.object({ kind: z.literal('rubric'), items: z.array(Id('itm')).min(1), minPoints: z.number().int().min(1).max(10) }).strict(),
  z.object({ kind: z.literal('paste-verify'), check: z.enum(['s0-script', 'exit-1.1', 'exit-1.2', 'cpp-toolchain', 'exit-1.9']) }).strict(),
  z.object({ kind: z.literal('real-paper'), paper: z.enum(['gcse-higher-p1', 'khan-precalc-challenge', 'mit-1801-final', 'mit-1806-final', 'stat110-final']),
             count: z.number().int().min(1).max(3).default(1), pass: z.number().min(0.5).max(1), timedMinutes: z.number().int().optional() }).strict(),
  z.object({ kind: z.literal('problem-sets'), refs: z.array(z.string().max(80)).min(1) }).strict(),
  z.object({ kind: z.literal('counter'), counter: z.enum(['algo-solved']), target: z.number().int().positive() }).strict(),
  z.object({ kind: z.literal('timed-window'), pool: z.string(), minutes: z.number().int(), solved: z.number().int(), of: z.number().int() }).strict(),
  z.object({ kind: z.literal('median'), metric: z.enum(['zetamac-cold']), days: z.number().int(), minRuns: z.number().int(), target: z.number() }).strict(),
  z.object({ kind: z.literal('book-log'), book: z.enum(['zhou']), chapter: z.string(), share: z.number().min(0).max(1) }).strict(),
  z.object({ kind: z.literal('log-count'), log: z.enum(['mock-human', 'mock-stranger']), target: z.number().int().positive() }).strict(),
  z.object({ kind: z.literal('project'), projectKind: z.string(), count: z.number().int().positive() }).strict(),
]);
const TrackName = z.string().regex(/^[a-z][a-z-]{1,23}$/);   // the last segment of a trk.* id
const ExitPart = z.object({ id: z.string().regex(/^[0-9a-z][0-9a-z.-]{0,31}$/), text: Prose, gate: z.array(Instrument).min(1), confirm: z.array(Instrument).default([]),
  track: z.object({ deferTo: z.number().int().min(1).max(3), tracks: z.array(TrackName).min(1) }).strict().optional(),
  estHours: z.number().positive() }).strict();
export const Topic = z.object({ zq: z.literal(1), id: Id('top'), number: z.string().regex(/^\d\.\d+$/), title: z.string(), hours: z.number().int().positive(),
  cover: z.array(z.string()).min(1), resources: z.array(Citation).min(1), exit: z.array(ExitPart).min(1),
  courses: z.array(Id('crs')).min(1), exam: Id('exm').optional(),       // optional: 0.4 and 0.5 close on their Stage 0 exit parts (docs/CURRICULUM.md 4.4)
  counted: z.boolean().default(true),                                      // false: hours sit outside the path total (3.2, docs/CURRICULUM.md 2.2)
  coreInterview: z.union([z.boolean(), z.array(TrackName)]).default(false) }).strict();   // ASSESSMENT.md 5.4: held at 0.90; a track list limits it (1.6 on the researcher track)
export const Stage = z.object({ id: Id('stg'), number: z.number().int().min(0).max(3), title: z.string(), hours: z.number().int().positive(),
  topics: z.array(Id('top')).min(1), exit: z.array(ExitPart).min(1) }).strict();
const TrackStatus = z.enum(['core', 'elective', 'optional', 'absent']);
export const Track = z.object({ id: Id('trk'), title: z.string().max(40), description: Prose,       // tracks are data (canon-gap.md 5.2)
  topics: z.array(z.object({ top: Id('top'), status: TrackStatus }).strict()).min(1),
  courses: z.array(z.object({ crs: Id('crs'), status: TrackStatus }).strict()).default([]) }).strict();   // per-course overrides
export const Curriculum = z.object({ zq: z.literal(1), stages: z.array(Stage).min(1), tracks: z.array(Track).min(1) }).strict();

// content/plan.yaml (ASSESSMENT.md 8.9).
export const Plan = z.object({
  zq: z.literal(1),
  stages: z.array(z.object({ stage: z.number().int().min(0).max(3), order: z.record(TrackName, z.array(Id('top')).min(1)),
    projectOrder: z.record(TrackName, z.array(z.string().regex(/^[a-z][a-z0-9-]*$/))).optional() }).strict()).default([]),
  alongside: z.array(z.object({ item: Id('top'), block: z.enum(['main', 'build', 'review', 'mental']),
    beside: z.union([z.array(Id('top')).min(1), z.string().regex(/^stage-[0-3]$/)]),
    capHoursPerWeek: z.number().positive().optional(), startsWhen: z.string().max(80).optional() }).strict()).default([]),
  habits: z.record(z.string(), z.object({ from: Id('top'), hoursPerWeek: z.number().positive() }).strict()).default({}),
  deferrals: z.array(z.object({ exitPart: z.string(), toStage: z.number().int().min(1).max(3), tracks: z.array(TrackName).min(1) }).strict()).default([]),
}).strict();

/* ---------- 12. Sets and exams ---------- */
const Slot = z.union([
  z.object({ item: Id('itm') }).strict(),
  z.object({ drill: Id('drl') }).strict(),
  z.object({ gen: Id('gen'), difficulty: Difficulty, count: z.number().int().min(1).max(10) }).strict(),
  z.object({ pool: z.object({ skills: z.array(Id('skl')).min(1), difficulty: Difficulty, heldOut: z.boolean().default(false) }).strict(),
             count: z.number().int().min(1).max(20) }).strict(),
]);
export const ItemSet = z.object({ zq: z.literal(1), id: Id('set'), rev: Rev, kind: z.enum(['homework', 'practice']), title: z.string().max(60),
  slots: z.array(Slot).min(1), dueDays: z.number().int().min(1).max(30).optional() }).strict();
const ExamForm = z.object({ id: LocalId,
  sections: z.array(z.object({ title: z.string().max(60), minutes: z.number().int().optional(), slots: z.array(Slot).min(1) }).strict()).min(1) }).strict();
export const Exam = z.object({ zq: z.literal(1), id: Id('exm'), rev: Rev,
  kind: z.enum(['topic', 'finals', 'gcse', 'challenge', 'cold-set', 'level-check', 'placement']),   // ASSESSMENT.md 3.1
  title: z.string(), minutes: z.number().int().min(5).max(240), marks: z.number().int().positive(),
  pass: z.number().min(0.5).max(1).optional(), calculator: z.enum(['none', 'basic', 'scientific', 'any']),
  mix: z.partialRecord(z.enum(['1', '2', '3', '4', '5']), z.number().min(0).max(1)),   // shares by difficulty; CI: they sum to 1
  shuffle: z.boolean().default(true),                // slot order shuffled per sitting (ASSESSMENT.md 3.2)
  unlabelledSlots: z.number().int().min(0).max(4).default(2),   // slots replaced per form by whole-topic draws
  forms: z.array(ExamForm).min(1) }).strict();       // paper kinds need at least 3 forms (CI, ASSESSMENT.md 3.2)

/* ---------- 13. Code drills and projects (code lives in .py files beside drill.yaml) ---------- */
export const Drill = z.object({
  zq: z.literal(1), id: Id('drl'), rev: Rev, status: Status, title: z.string().max(60),
  language: z.enum(['python', 'sql', 'cpp', 'shell']),
  mode: z.enum(['drill', 'script', 'pytest', 'sql', 'answer', 'checker']),
  brief: Prose,                                      // at most 120 words on screen; the rest behind More
  entry: z.string().optional(),                      // function name (drill mode) or file (script mode)
  files: z.object({ starter: z.string(), reference: z.string(), tests: z.string(),
                    data: z.record(z.string(), z.string()).default({}) }).strict(),
  examples: z.array(z.string()).min(1),              // test names run on Run; all others run on Submit
  edge: z.array(z.string()).min(2),                  // test names that are edge cases (empty input, ties, overflow)
  needs: z.array(z.enum(['numpy', 'pandas', 'scipy', 'statsmodels', 'sklearn', 'matplotlib', 'pytest', 'hypothesis'])).default([]),
  timeLimitMs: z.number().int().min(500).max(20_000).default(5_000),
  wrong: z.array(z.object({ file: z.string(), failing: z.string(), mc: Id('mc').optional(), slip: z.literal(true).optional(),
                            line: Prose }).strict()).min(1),   // known-wrong solutions; each must fail the named test
  parsons: z.enum(['auto', 'off']).default('auto'),
  heldOut: z.boolean().default(false),
  difficulty: Difficulty, skills: z.array(Id('skl')).min(1).max(3), est: Seconds,
  hints: Hints.optional(), why: Why,
}).strict();
export const Project = z.object({                    // Stage 1 exit projects and Stage 2.3 projects [our choice; provisional]
  zq: z.literal(1), id: Id('prj'), rev: Rev, status: Status, title: z.string().max(60),
  kind: z.string().regex(/^[a-z][a-z0-9-]*$/),       // matches ASSESSMENT.md's project instrument (projectKind)
  brief: Prose,
  milestones: z.array(z.object({ id: LocalId, text: Prose, evidence: z.enum(['repo-check', 'paste-verify', 'self-report']),
                                 drill: Id('drl').optional(), hours: z.number().positive() }).strict()).min(1),
  note: Id('itm'),                                   // the results note: a long-form item with genre results-note
  skills: z.array(Id('skl')).default([]), sources: z.array(Citation).default([]),
}).strict();

/* ---------- 14. Generator specs (the logic lives in .gen.ts and .verify.py) ---------- */
const BoxDim = z.union([
  z.object({ int: z.tuple([z.number().int(), z.number().int()]) }).strict(),
  z.object({ enum: z.array(z.string()).min(1) }).strict(),
  z.object({ dec: z.tuple([z.string(), z.string()]), step: z.string() }).strict(),   // exact decimals, e.g. ['0.5', '3.0'] step '0.1'
]);
export const GeneratorSpec = z.object({
  zq: z.literal(1), id: Id('gen'), v: z.number().int().min(1), status: Status, title: z.string().max(60),
  desc: z.string().max(120),                         // one line for Bertie's practice catalogue (AI-TUTOR.md 2.11)
  skills: z.array(Id('skl')).min(1), use: z.array(ItemUse).min(1),
  semantics: z.string().min(1).max(4000),            // what the parameters mean, for the verifier's author
  box: z.record(z.string(), BoxDim),                 // the parameter box; admissibility is code, written twice
  admissible: z.string().max(2000),                  // the admissibility rule in words
  levels: z.partialRecord(z.enum(['1', '2', '3', '4', '5']), z.string()),   // the levels this generator serves, in words
  tutorParams: z.array(z.string()).default([]),      // box dimensions Bertie may fix when he asks for practice
  misconceptions: z.array(Id('mc')).min(1),
  phrases: z.record(z.string(), z.record(z.string(), z.string())),
  heldOut: z.number().min(0).max(0.5).default(0.2),  // share of each level's admissible index kept for exams
  sample: z.number().int().min(2_000).optional(),    // cross-check this many points when the box is too big to enumerate
  golden: z.string(),
}).strict();

export type LessonT = z.infer<typeof Lesson>;
export type CheckT = z.infer<typeof Check>;
```

**What the schema cannot say.** Cross-file and cross-field rules run in the compiler (section 6.7), because they need the whole content set: every `mc`, `skl`, `gls`, `src`, `ast`, `trk` and `prj` id exists; `from:` and element references resolve against `targets(config)`; a choice distractor carries `mc` or `slip`; the correct option carries no feedback; verify keys match diagnosis keys; an exam's `mix` sums to 1 and a paper has at least 3 forms; the lesson-level rules of the authoring checklist (section 9.3).

**Two changes to `ASSESSMENT.md` 2.10.** Its `ExitPart` used `id: LocalId`, which rejects its own ids (`1.9.exit`, `3.3.mocks`, `s0.gcse`), so the id pattern here admits digits and dots. Its `track.tracks` was a fixed enum of three tracks; here it takes track names, because tracks are data (decision 19). Both are syntax only; the meaning stays the assessment paper's.

### 3.3 Feedback: one structure for every graded screen

Each graded screen or item carries the same feedback fields, so the engine has one feedback path (design research 5.4 to 5.6):

| Field | Shown | Rule |
|---|---|---|
| `reason` | Verdict chip after a correct answer | At most 20 words per sentence |
| `diagnose[]` | Verdict chip and show-why after a matching wrong answer | First match wins (section 7.8); each names `mc` or sets `slip: true` |
| `otherwise` | Verdict chip after an undiagnosed wrong answer | Required unless every wrong answer is diagnosed (a choice whose distractors all carry feedback) |
| `hints.nudge`, `hints.point`, `hints.step` | The three-rung hint ladder (design 5.5) | Required on lesson screens; `point` names 1 to 4 elements to highlight |
| `why.yours`, `why.shown`, `why.then` | The Why? sheet | After a correct answer: `yours` (or `shown`) then `then`. After Show solution: `shown` (or `yours`) then `then`. After a wrong answer on a screen that is still unresolved: the matched diagnosis line and `shown` only, because `then` states the result and the reveal path is Show solution (`docs/PLAN.md` section 6, the Why rule); `shown` therefore passes the same leak lint as the tutor fields (section 3.10). At most 3 sentences in total (design 9.4) |
| `why.rep` | Not shown; sent to Bertie | The representation the authored explanation uses (`picture`, `count`, `algebra`, `analogy`, `simulation`, `code`), so "Explain it differently" uses another (`AI-TUTOR.md` 2.4) |
| `solution.line`, `solution.steps` | Show solution; homework and exam review | Steps carry a justification each ("no step left as obvious", lesson-creator) |
| `accepted` | The accepted-answer rule after grading | Generated from the check (section 7.9); an override is allowed but linted for the same numbers |
| `after` | Played on correct or reveal | Widget recipes or declarative steps |

`why.yours` refers to the learner's own action and `why.shown` states what happened without "you", which is the prototype's `why(pick, rev)` pattern written as data.

### 3.4 Checks

The `Check` union in section 3.2 covers every answer type the task lists:

| Answer type | Kind | Notes |
|---|---|---|
| Single choice | `choice` | `correct` is one option id; option values (`value`) are exact, so distractor sanity can compare them |
| Multiple select | `choice`, `select: many` | `partial: true` marks per option in homework |
| Numeric with tolerance and units | `numeric` | `tol` (absolute, relative or both), or `range`; `integer`; `forms`; `fractionsExact`; `sf`, `dp`, `requireForm`; `unit` as a label or a symbol with conversion; `probability` adds the $[0, 1]$ nudge |
| Expression | `expression` | Symbolic equivalence (section 7.3) under `vars` domains and `assume`; `relation` covers equations, inequalities, antiderivatives and "up to a constant"; `form` adds a structural requirement |
| Set or region | `set`, `interval`, `predicate` | `set.correct` may be a list or `{ where: ... }`, which the widget's build-time resolver turns into a list (section 8.1) |
| Ordering | `ordering` | `before` pairs define a partial order, so any order that meets them is right; `exclude` lists distractor lines that must be left out |
| Matching and bins | `mapping` | Per-card marks |
| Point or curve within tolerance | `point`, `curve` | `angle-mod-pi` for eigenvectors; `curve` uses a band, a coverage share and features |
| Matrix | `matrix` | Exact rational by default; relations for echelon forms and orthonormal columns |
| Distribution | `distribution` | Exact, total variation or maximum absolute difference |
| Code with tests | `code` | Names a drill; the drill holds the suite (section 3.9) |
| Long form with a rubric | `long-form` | `genre` (proof, derivation, written, results-note) sets Bertie's marking tier; 4 to 10 rubric points totalling 10 marks, enforced by the schema; each point names the model-answer lines that evidence it; `marking: tutor-draft` (default) or `self` |
| Predicted output, SQL result | `output`, `resultset` | From the programming catalogue |
| Multi-part | `parts` | One level of nesting; green parts lock, amber parts reopen (design 5.4) |

**The curriculum files' quiz letters.** The seven files in `docs/curriculum/` tag each lesson's quiz with letters. The letters are shorthand in those documents only and are never stored, so they map onto check kinds as follows:

| Letter | Meaning in the curriculum files | Check kind |
|---|---|---|
| N, X | Numeric; expression | `numeric`; `expression` |
| C, M | Single choice; multi-select | `choice`; `choice` with `select: many` |
| O, S | Order the steps; sort or match | `ordering`; `mapping` |
| I | Interval or solution set | `interval` or `set` |
| P | Point, direction, handle or curve on a canvas | `point` or `curve` |
| T | Predict the output of code | `output` |
| A | Matrix or vector entry | `matrix` |
| D | Distribution or a set of bars | `distribution` |
| B | A basis, subspace or parametric solution set | `predicate` (`same-subspace`, `same-affine-set`) |
| K | Code with tests | `code` |
| E | Entry graded by behaviour (slice, glob, pattern, format spec) | `predicate` (`selection-equals`, `format-produces`), or `output` with `compare: regex` |
| G, H | Reach a target state in a simulator; a shell or path task | `predicate` on the widget's state (the programming catalogue's `state`) |
| W, Z | Typed passage; timed speed set | `predicate` on the widget's result (`speed-drill`, typing trainer); their timers belong to the widget (`ASSESSMENT.md` 3.1) |
| R | Region selection (`stage0-precalc-computing.md`) **or** result table (`stage1-python-tools.md`) | `set` over region ids; `resultset`. The letter clashes; section 13 asks the curriculum files to rename one |

Every registered `predicate` has a TypeScript implementation in `packages/graders` and a Python twin in `zqverify`, compared on fixture states (section 6.2).

### 3.5 Widgets on a screen

A screen has up to three `canvas` widgets and at most one `input` widget. `answer:` names the widget whose `answer()` is graded, so a canvas widget can be the input (the dice grid on the `shade` screen). Only `id`, `type`, `v`, `label` and `from` are common; every other field belongs to the widget and is validated by the schema the widget module exports.

**`from: <screen>/<widget>`** starts from an earlier screen's widget config and merges the fields given here over it with JSON Merge Patch semantics (RFC 7386: objects merge, arrays and scalars replace, `null` deletes). Ladder screens ("the same canvas with one new constraint", design 5.2) then state only the constraint:

```yaml
canvas:
  - id: grid
    from: shade/grid
    task: none
    condition: { where: a == 5 or b == 5, outline: cross, caption: At least one die shows a 5 }
```

**`v`** pins the widget's major version. A widget's breaking config change ships as `v: 2` beside `v: 1`; the compiler lists every screen still on the old version, and a codemod moves them.

**Element references** in hints, show-why and declarative steps are `<widget id>/<kind>:<name>` (`grid/cell:5,5`, `grid/row:5`, `d/line:l2`, `sim/control:filter`). The part after the slash is the widget's own element id, in the `kind:name` form `AI-TUTOR.md` 0.2 fixed for every widget, so the id in a hint is the id in Bertie's act line and in the widget's DOM. Content always writes the widget prefix, even on a one-widget screen, so adding a second widget later cannot make an old reference ambiguous; the act line drops it on one-widget screens, as the tutor paper specifies. Inside a recipe's `args` and in set answers and matchers, where the widget is already known, elements are bare ids (`cells: ['cell:5,1']`, `missing: ['cell:4,4']`). The compiler checks every reference and every bare id against the widget's `targets(config)`: the element ids that config produces, computed without a DOM (section 12.1). Revision 2's prototype resolves 36 of them in the worked lesson.

### 3.6 Templates in feedback

Feedback sometimes needs the learner's own numbers ("(6, 1) adds to 7, not 8"; "Your 1,000 rolls kept 309"). The template language is deliberately small:

| Form | Meaning |
|---|---|
| `{{answer.value}}`, `{{answer.raw}}` | The learner's answer, formatted in en-GB, or as typed |
| `{{<widget>.<export>}}` | A value the widget declares in `exports(config)` (`sim.rolled`, `sim.kept`) |
| `{{extra.0.label}}`, `{{missing}}`, `{{hit.count}}` | Bindings a `set` matcher provides |
| `{{#if path}}...{{else}}...{{/if}}` | One level of condition on a truthy value |

No arithmetic, loops or function calls. The compiler checks that every path is declared by the widget or the matcher, and lints each branch of a condition as its own text.

### 3.7 Screens

The ten screen types of design research 5.2 map onto the schema as follows:

| Type | Required beyond the base | Purpose |
|---|---|---|
| `title` | `prose` (one framing sentence), optional `art` | The only screen without a task |
| `explore` | `canvas`; optional `continueWhen` predicate | Free manipulation before any question |
| `problem` | the task fields | A question on a canvas |
| `ladder` | the task fields and `constraint` | The same canvas with one new constraint; usually `from:` |
| `demonstrate` | `canvas` with a stepper | An animated step-through, then Continue |
| `trap` | the task fields and `trap: { mc, bait }` | The likely answer is the misconception; `bait` names the option or diagnosis that encodes it |
| `generalise` | the task fields, `rule` and optional `tex` | The rule stated as a description of what the learner did, then one confirmation item |
| `derive` | the task fields; optional `leap` (`naive`, `fails`, `pointsTo`) | Complete a missing line or order the steps; `leap` is required when the step is a creative one (maths-teaching, "motivate the leap") |
| `code` | `drill`, `question`, `reason`, `hints`, `why` | A code drill inside a lesson |
| `summary` | `ideas` (exactly 3), `trap`, optional `card` | Key ideas, the formula card saved to the Notebook, the common trap |

### 3.8 Items and sets

An **item** is a graded unit outside the lesson flow: lesson quiz, practice, level review, homework, exam. Items carry the same task fields as screens, plus `title`, `use`, `heldOut`, `calculator`, `difficulty`, `skills`, `est` and `marks`. A **pinned item** (`from: { gen, v, params }`) is one fixed instance of a generator, used when a quiz or homework set wants a particular variant.

**Sets** (`set.*`) list slots: a fixed item, a code drill, `count` instances of a generator at a level, or `count` items drawn from a skill pool. **Exams** (`exm.*`) carry a `kind` from `ASSESSMENT.md` 3.1 (`topic`, `finals`, `gcse`, `challenge`, `cold-set`, `level-check`, `placement`), a duration, total marks, a pass mark, a difficulty mix (design 8.4: 20% at 2, 50% at 3, 20% at 4, 10% at 5 for topic exams), a calculator rule, and an explicit list of **forms**, each a list of sections of slots. CI applies `ASSESSMENT.md` 3.2 to every paper kind: at least 3 forms; equal total marks across forms; each form's mix within 5 percentage points of the declared mix; every skill of the topic in some form; at least 50% of each form's marks from generator slots, or at least 5 forms; and an exam reserve holding at least $6 \times \text{forms} \times \text{count}$ admissible points for every generator slot, so six sittings stay fresh.

**Where items live.** Lesson quiz items sit inside the lesson file, because they are written and reviewed with it. Practice, review and homework items sit in `bank.items.yaml` per level. Every item id is global, so a quiz item can also appear in practice (`use: [quiz, practice, review]`).

**Companion work.** Each level lists the textbook sections and exercises from the topic's one resource that go with it (`companion`), with estimated hours. These are most of the curriculum's hours (`ASSESSMENT.md` 8.7 counts them as earned when logged), so CI requires each topic's estimates (lesson minutes, set and paper estimates, companion hours, exit-part `estHours`) to sum to within 10% of the topic's hours in `docs/curriculum.md`.

**Projects** (`prj.*`) are provisional [our choice]: a brief, milestones with their evidence kind (`repo-check`, `paste-verify`, `self-report`) and hours, an optional drill per milestone, and a results-note item (a `long-form` check with `genre: results-note`). The Stage 2 content work will extend the schema; ids already used by `stage1-statistics-ts.md` (`prj.stats.*`) stay valid.

### 3.9 Code drills

A drill is a folder: `drill.yaml` (validated by `Drill` in section 3.2) plus `starter.py`, `reference.py`, `tests.py`, optional data files and a `wrong/` folder of known-wrong solutions. Code stays in `.py` files so that it gets ruff, a formatter and readable diffs, and so the escape trap of section 2.1 cannot reach it.

`tests.py` uses a small library, `zqtest`, that runs unchanged on CPython and Pyodide (no pytest dependency; the programming catalogue's mini-pytest shim):

```python
from fractions import Fraction
from zqtest import case
from solution import p_given            # the learner's module

@case(example=True)
def total_ten_given_a_five():
    return p_given(lambda a, b: a + b == 10, lambda a, b: 5 in (a, b)), Fraction(1, 11)

@case(compare='exact')
def impossible_condition_raises():
    try:
        p_given(lambda a, b: True, lambda a, b: a + b == 13)
    except ZeroDivisionError:
        return 'raised', 'raised'
    return 'returned', 'raised'
```

Each `@case` returns `(actual, expected)`; the decorator sets visibility, the comparison (`isclose` with `rel_tol=1e-9` by default, `exact`, `fraction`, `allclose`, `allclose-up-to-sign`, `frame-equal`) and an optional per-test time limit. The programming catalogue's richer kinds (stdout, result set, complexity, figure, checker, learner-written tests) become further decorators in `zqtest`. Every `wrong/*.py` file names the test it must fail and the misconception it encodes; the runtime uses the same mapping to give a diagnosis line when the learner's first failing test matches (`match: { kind: test, failing: ... }`).

**Where a drill runs.** No runtime tags (decision 18 as tidied). `needs` lists every package the drill imports beyond the standard library; CI loads exactly those packages, so an undeclared import fails the build. At run time the drill runs wherever `PythonRuntime.available(needs)` answers `ok`; elsewhere it offers the web app with a result code (`ASSESSMENT.md` 14.3).

### 3.10 Tutor fields

Bertie is built in from the start, so the format carries tutor context from the start. Each field feeds a named part of the `TutorRequest` in `AI-TUTOR.md` 4.1:

| Content field | Where | `TutorRequest` field | Use |
|---|---|---|---|
| `introduces` (skill names), `insight` | Lesson | `lesson.objectives` (at most 4) | What the lesson is for |
| Earlier lessons in the course, `requires` | Lesson | `lesson.covered` | What Bertie may assume |
| The topic's `notation.yaml` | Topic | `lesson.notation` | Symbols Bertie must use |
| `terms`, each term's `introducedIn` | Lesson, glossary | `lesson.glossary`; the embargo list | Terms introduced so far, and the terms not yet introduced, which Bertie must not use |
| `tutor.focus`; `reason` once the screen is finished | Screen | `lesson.screens[].title`, `.keyIdea` | The outline |
| `sources` | Lesson | `lesson.references` (at most 6) | The only reading Bertie may recommend |
| Summary `card`s unlocked so far | Lesson | `lesson.cards` | Cards Bertie may open |
| `tutor.notes`, `tutor.reps` | Screen | `screen.notes`, `screen.reps` | Where learners stall; representations that work here |
| `tutor.avoid` | Screen | Appended to the per-call block | Phrases Bertie must not use on this screen |
| `diagnose[].mc` with each misconception's `belief` | Screen, library | `misconceptions.screen` | The screen's misconception register |
| The checker's summary of `check`; widget `secret()`; `solution` | Screen | `answer` (`sealed` until graded) | Lets Bertie aim a stuck learner correctly; the leak probe guards it |
| The accepted-answer rule (section 7.9) | Screen | `answer.accepted` | Sent only once the answer is open |
| `why` with `why.rep` | Screen | `why.text`, `why.rep` | Bertie's "differently" uses another representation |
| `genre`, `rubric`, `model` | Long-form check | `marking` | The marking prompt (section 7.7) |
| `desc`, `tutorParams` with their box bounds, the levels | Generator | `practice.generators` | Bertie picks generators and parameters; the page builds and checks the items (section 5.4) |

**Rules** (checklist rows 31 and 32, section 9.3): every task screen has `tutor.focus`, because the outline needs a title per screen; and no tutor field contains a value the screen's check accepts. The second is the content-side twin of the tutor paper's leak probe: `tutor.notes` is sent unsealed, so a note that says "the answer is $\tfrac{1}{6}$" would hand Bertie, and through him the learner, the answer. The compiler extracts candidate answers from the tutor fields and from `why.shown` (which an unresolved screen may show after a wrong answer, section 3.3) with the same extractor the tutor's leak probe uses (`@zq/graders` `leak.ts`, `docs/PLAN.md` section 3), and grades each with the screen's own check; any that grades correct is an error. Tutor fields are not learner-facing copy, so the sentence-length and words-per-screen lints skip them; dashes, banned words and spelling still apply.

Bertie never edits content or answer state; that rule lives in the tutor paper and the widget contracts.

---

## 4. Stable ids, versioning and migrations

### 4.1 Ids

```
<kind>.<namespace>.<name>        lsn.cond.shrinking-sample-space
                                 itm.cond.total-seven-has-three
                                 mc.prob.at-least-one-as-specific
                                 gen.prob.two-dice-conditional
```

- **Kinds:** `stg`, `top`, `trk`, `crs`, `lvl`, `lsn`, `itm`, `set`, `exm`, `prj`, `mc`, `skl`, `gen`, `drl`, `src`, `gls`, `crd`, `ast`.
- **Namespace:** the topic (`prob`) for libraries, the course (`cond`) for lessons and items. Up to three further dot segments are allowed for large courses.
- **Format:** lower-case kebab segments, at most 80 characters, matched by the `Id()` regex in section 3.2.
- **Local ids** (screens, widgets, options, diagnosis keys, model-answer lines) are unique inside their parent and addressed from outside as `lsn.cond.shrinking-sample-space#cross`.
- **Display numbers** ("Level 1 · Lesson 3", "1.5.2") are computed from position at build time. Renumbering the outline changes no id.
- **Immutability.** An id, once published, never changes meaning and never disappears from `ids.lock.json`. Renaming one is a migration (section 4.5), which is deliberately a little tedious.

Human-readable ids were chosen over UUIDs because the owner reads them in diffs and agents write them; the lock file catches collisions and reuse, which is the only thing UUIDs would add.

### 4.2 Revisions and the answer hash

Lessons, items, drills and generators carry `rev`, starting at 1. The compiler computes two hashes per entity:

- **`contentHash`** over the whole compiled entity.
- **`answerHash`** over what decides correct against not yet: the canonical check (correct option ids and the option values, value, tolerance, range, forms, set, order constraints, rubric points) and, for a lesson, its ordered screen ids. Copy, hints, explanations, diagnoses and widget styling are outside it, because they change what a learner is told, not whether an earlier answer was right.

`ids.lock.json` on `main` holds the last published `rev` and `answerHash` of every id. On a pull request:

| Change | Required |
|---|---|
| Copy, hints, explanations, show-why, styling | Nothing. `contentHash` changes; learners keep everything |
| A diagnosis added or changed, a hint, a source | Nothing; the verifier and grader replay still check the new diagnosis |
| Correct answer, option values or correctness, tolerance, range, forms, rubric | `rev` bump and a `changelog` line. CI fails "answer changed without a rev bump" otherwise |
| Screens added, removed or reordered in a lesson | Lesson `rev` bump and a changelog line |
| Generator output for an existing seed | Generator `v` bump (the golden file shows it, section 5.6) |
| An id removed | Forbidden. Set `status: retired` and add a migration |

`changelog[].notify: true` marks a change worth telling learners who already finished the lesson ("Updated: the second derivation step is now explained"). The course map shows a small dot on those lessons.

### 4.3 What learner progress refers to

The engine paper and `ASSESSMENT.md` 13 own the data model (an event log); this paper sets the rules it must follow so content edits keep progress valid:

- Every progress record is keyed by content id, and records the `rev` it was earned against: `lessons/<lsn id>` holds `{ rev, done: [screen ids], at: screen id, completedAt, quiz }`.
- Every attempt the learner can revisit outside the lesson stores a **snapshot**: the rendered question text, the learner's answer, the correct answer and the verdict. That covers quiz, level review, homework, exam, level check, weekly problem and redo attempts, and lesson screens that were revealed. History screens and homework review read the snapshot, so they never depend on old content or old generator code. Correct lesson screens and practice attempts store references only (`ASSESSMENT.md` 0.3: about 26,000 lesson-screen snapshots over the path would be stored and never read).
- Generated instances are stored as `{ gen, v, level, seed }`, plus the snapshot where the rule above asks for one. A reference without a snapshot is rebuilt from the generator only while `v` is unchanged; after a `v` bump the history row shows the verdict without the question.
- Mastery evidence attaches to skills (`skl.*`), not to items, so it survives item revisions.

### 4.4 What happens on each kind of change

| Content change | Lesson in progress | Lesson completed | Redo queue entry | Mastery |
|---|---|---|---|---|
| Copy edit | Resume at the same screen | Unchanged | Unchanged | Unchanged |
| Item `rev` bump | Not applicable | Unchanged | Shows the new `rev` | Kept |
| Screen added or reordered | Resume at the first screen after the last completed one, in the new order | Stays complete; dot if `notify` | Unchanged | Kept |
| Screen removed | As above; its result is kept for history | Stays complete | Entry for that screen is dropped with a note | Kept |
| Item retired | Not applicable | Unchanged | Replaced by `replacedBy`, else by a generator instance on the same skill at the same difficulty, else dropped with a note | Kept |
| Generator `v` bump | Not applicable | Not applicable | Same seed if `v` is unchanged; a fresh seed otherwise | Kept |

"Dropped with a note" means the learner's What changed sheet says which redo item went and why. Nothing disappears silently.

### 4.5 Migrations

`content/migrations.yaml` is append-only data. Each entry names the release it ships in:

```yaml
- release: 2027.01.14.1
  kind: rename                     # same content, new id
  from: lsn.cond.shrinking-sample-space
  to: lsn.cond.shrink-the-sample-space
- release: 2027.02.03.1
  kind: merge                      # many ids become one; completion if any part was complete; mastery by evidence-weighted mean
  from: [skl.prob.restrict-sample-space, skl.prob.conditional-by-counting]
  to: skl.prob.condition-by-counting
- release: 2027.02.03.1
  kind: split                      # one id becomes several; completion and mastery are copied to each part
  from: lsn.cond.bayes-and-total-probability
  to: [lsn.cond.total-probability, lsn.cond.bayes-rule]
- release: 2027.03.10.1
  kind: retire
  id: itm.cond.three-hearts
  replacedBy: itm.cond.three-hearts-v2
```

On load, the runtime applies every migration newer than the learner's recorded `contentRelease`, in order, then records the new release. Each operation is idempotent, so a crash mid-way is safe. **Test:** CI keeps learner-state fixtures from the last six releases (`tests/fixtures/learners/*.json`), migrates each to the current release, and asserts that every id they reference exists and is not retired.

**Release numbers** are dates (`2026.11.02.1`); the format version is the `zq: 1` field. A bundle whose format major version the app does not know shows "Update the app to open this course", never a broken lesson.

---

## 5. Item generators

### 5.1 What a generator is

A generator produces many verified variants of one item template: a seeded, deterministic function from a seed and a level to an item. It is four files:

| File | Contents | Runs |
|---|---|---|
| `<name>.gen.yaml` | The parameter **box** (the ranges of each parameter, as data), the admissibility rule and levels in words, the phrasebook, the misconceptions it can diagnose, the `semantics` text for the verifier's author, and for the tutor a one-line `desc` and the `tutorParams` Bertie may fix | Read by both implementations and by the tutor context |
| `<name>.gen.ts` | `accept(p)`, `level(p)`, `answer(p)`, `diagnoses(p)`, `build(p)` | Build time (all five) and on the device (`build` only) |
| `<name>.verify.py` | `accept(p)`, `level(p)`, `answer(p)`, `diagnoses(p)`, optionally `simulate(p, rng)` | CI only |
| `<name>.golden.json` | Hashes of the items built for fixed seeds at each level | CI only |

### 5.2 Declaring the parameter space

The box is a product of independent dimensions: `{ int: [lo, hi] }`, `{ enum: [...] }`, or `{ dec: ['0.5', '3.0'], step: '0.1' }` for exact decimals. Dependencies between parameters (a threshold that only makes sense up to twice the number of faces) are not encoded in the box; they belong to `accept`, which is code and is written twice. That keeps the box trivially enumerable by both languages and puts every judgement about "a good item" where two implementations must agree on it.

`accept(p)` returns false for parameter points that are out of range for their kind, give a degenerate item (an answer of 0 or 1, a condition that cannot happen), defeat the teaching point (news that does not change the chance), or leave too few distinct misconception values to diagnose.

### 5.3 Answers and misconceptions

- `answer(p)` returns an **exact** value: a rational from `@zq/gen` (BigInt numerator and denominator), an integer, an exact expression for symbolic items, or a float with a declared tolerance for items whose answer is genuinely irrational. Generators may not call `Math.random`, `Date`, the DOM, or transcendental `Math` functions in `accept`, `level` or `answer` (an ESLint rule set), because those differ between JavaScript engines in the last bit.
- `diagnoses(p)` returns the value each declared misconception produces, in a fixed priority order. Values that coincide with the answer, or sit within the separation distance of the answer or of a value kept earlier, are dropped. For the section 11 generator the distance is 0.01 with tolerances of 0.005, so a typed decimal can never match the answer and a diagnosis, or two diagnoses, at once.
- `build(p)` returns an item body (the `AuthoredItem` schema without the head fields): prompt, question, input, check, diagnoses with their lines, `otherwise`, `reason`, `why`, `solution`, difficulty, skills, estimated time. Text comes from the phrasebook in the YAML, so the finite set of phrases can be reviewed once.

### 5.4 Seeds, levels and the admissible index

At build time the compiler enumerates the box, keeps the admissible points, groups them by level, and emits an **admissible index** per level into the course's generator module. On the device:

```
make(seed, level)  =  build( index[level][ hash32(gen.id, seed) mod |index[level]| ] )
```

- Uniform over admissible variants, with no rejection loop on a phone.
- Byte-identical on every device: the hash is integer arithmetic and `build` uses exact rationals and string templates. CI checks the golden seeds in Chromium, WebKit and Firefox through Playwright.
- A set asks for consecutive seeds and skips repeats of a parameter point, so a homework set never shows the same numbers twice.
- **Exam reserve.** A seeded 20% of each level's index (`heldOut` in the spec) is reserved for exams and never returned by practice, so an exam variant is always unseen. CI checks that every exam's generator slots fit inside the reserve for all of the exam's parallel forms, with the six-sitting margin of section 3.8.
- **Bertie's picks.** In practice mode the tutor proposes `{ generator, params }` pairs (`AI-TUTOR.md` 2.11). Bertie may fix only the dimensions listed in `tutorParams`, within the box; the page calls `makeWhere(partial, seed)`, which draws a seeded point from the admissible, non-reserved index that matches the partial assignment, and drops the request if none matches. Bertie therefore steers the kind of question, never the numbers, and every served item is one CI has already checked. For the section 11 generator, `{ cond: at-least-one }` matches 485 admissible points (92 at level 2, 393 at level 4) before the reserve is removed [measured].

**Large boxes.** When a box has more than 200,000 points [our choice], the compiler samples it (`sample`, at least 2,000 points, stratified across every enum value and including every corner of the integer ranges) for the cross-check, and the device draws by rejection from the box with a cap of 64 tries, falling back to a 500-point index computed at build. CI requires an acceptance rate of at least 20% over 10,000 seeds, so the cap is never hit in practice.

### 5.5 Independence of the two implementations

The Python verifier is written from the `semantics` text in the spec, by a different agent session from the one that wrote the TypeScript, without reading it ("blind pairing"). The verifier for section 11 also uses a different style on purpose: sets of outcomes and their intersections in Python against counting loops in TypeScript. Blind pairing is a process rule that no machine can enforce; the pull request template records which session wrote each file, and section 6.13 lists it as a limit.

### 5.6 What CI does with a generator

1. Enumerates the box in Node, runs `accept`, `level`, `answer` and `diagnoses` at every point, and writes JSON lines.
2. Enumerates the box again in Python from the spec, runs the verifier, and compares point by point: the admissible sets must be identical, and so must levels, answers and every misconception value. Any disagreement fails the build and prints the parameter point.
3. Builds the item at every admissible point (or the sample) and runs it through the same schema, copy lints, KaTeX render, distractor sanity and grader replay as an authored item (section 6).
4. Runs `simulate` on a stratified sample (12 points per level, $10^6$ trials each, fixed seed) and requires each estimate within 4 standard errors of the exact answer. With a fixed seed this cannot flake.
5. Compares the golden hashes. A change for an existing seed without a `v` bump fails.
6. Renders a **specimen sheet**: one built item for each combination of the enum dimensions, as Markdown in the pull request's artefacts, so the owner can read the phrasebook in context once.

---

## 6. Verification

### 6.1 Principle and pipeline

**Every claim in the content is either computed twice or replayed through the grader that will judge the learner.** The author (or the TypeScript generator) states an answer; an independent Python implementation recomputes it; the runtime grader is then run on the canonical answer, its accepted forms and every diagnosed wrong answer, and must give the verdicts the content expects.

```
 content/*.yaml, *.gen.ts, drills/*.py
        │
        ▼
 [1] load      strict YAML profile, zod schemas ............................ Node
 [2] resolve   ids, from:, element refs, where-sets via widget resolvers ...... Node
 [3] lint      copy, structure, authoring checklist, KaTeX, widget configs .... Node
 [4] jobs      MathJSON for derivation lines and arithmetic claims (CE latex-syntax) ... Node
        │                       verify jobs (JSON lines)
        ▼
 [5] verify    answers, misconception values, spaces, chains, claims, simulation ... Python (zqverify)
 [6] generate  box enumeration, TS against Python, built-item checks ......... Node + Python
 [7] replay    runtime graders on correct, accepted and diagnosed answers ...... Node (packages/graders)
 [8] drills    reference, starter, wrong solutions, mutants ................. CPython 3.12, Pyodide 314.0.7
 [9] render    storyboard, overflow at 390px, axe ............................. Playwright
        │
        ▼
 [10] emit     bundles, indexes, manifest (section 8) .......................... Node
```

Steps 1 to 4 and 7 run in under a second per lesson; step 5 took 1.9 s for the section 10 lesson including six Monte Carlo runs of $10^6$ trials, and step 6 took 3.2 s for the section 11 generator's 21,760 points [measured on a 4-core container].

### 6.2 Two implementations of every answer

| Check kind | Declared side | Independent side (Python) | Agreement rule |
|---|---|---|---|
| `choice` | The correct option's `value`, or `verify.options` on the instance | `verify.answer` | Exact equality; the correct option equals the answer, no distractor does |
| `numeric` | `check.value` (exact) | `verify.answer` | Exact equality for rationals; for irrational answers, agreement within $10^{-12}$ relative using mpmath at 50 digits |
| `set` with `where` | The widget's build-time resolver (TypeScript) | `verify.set` over the declared space | Identical outcome sets; `expect` (the author's count) must match too |
| `expression` | `check.equals` | `verify.answer` built with SymPy | `simplify(a - b) == 0` under the declared assumptions, and agreement at 20 random points from the declared domain with mpmath |
| `matrix` | `check.equals` | SymPy `Matrix` exact, NumPy as a float cross-check | Exact, and the float result within $10^{-9}$ |
| `distribution` | `check.masses` | Enumeration with `Fraction`, or SciPy for named laws | Exact, or within $10^{-12}$ |
| `point`, `curve` | `check.target` | SymPy (solve, diff) and the defining property | Target satisfies the property within one thousandth of the check tolerance |
| `ordering` | `check.order` | The partial order `before` | The declared order satisfies every constraint; every `exclude` line is absent |
| `predicate` | The registered predicate (TypeScript) | Its Python twin, on the item's fixture states | Same truth value on every fixture |
| `code` | `reference.py` | `tests.py` | Section 6.11 |
| `long-form` | `model` lines | Derivation chain where the lines are maths; rubric anchoring always | Section 6.8 |
| generator | `.gen.ts` | `.verify.py` | Section 5.6 |

Which Python library answers which question:

| Domain | Primary | Second check |
|---|---|---|
| Discrete probability and counting | Exact enumeration with `fractions.Fraction` over the declared space | NumPy Monte Carlo, $10^6$ trials, 4 standard errors |
| Algebra, calculus, series, limits | SymPy | mpmath numeric evaluation, quadrature or summation at 50 digits |
| Linear algebra | SymPy exact | NumPy |
| Continuous probability and statistics | SciPy (`scipy.stats`, `integrate.quad`) | Monte Carlo with NumPy, or a closed form in SymPy |
| Regression and time series | statsmodels | NumPy normal equations |
| Finance (pricing, Greeks) | Closed forms in SymPy or mpmath | Binomial tree or Monte Carlo in NumPy |

Versions are pinned with `uv`, and SymPy is upgraded only through a pull request that reruns the whole corpus.

### 6.3 The verify language

A `verify` block is data, readable in a diff, and evaluated by `zqverify` without `eval`, `exec` or `sympify`: the string is parsed with Python's `ast` module and walked against a whitelist of node types and function names. Integer division produces exact fractions.

| Element | Meaning |
|---|---|
| `space` | `{ dice: [6, 6] }`, `{ coins: 3 }`, `{ product: [[up, down], [up, down]] }`, `{ draw: { from: deck, k: 2, ordered: false, replace: false } }` or an urn. Outcome variables are `a`, `b`, `c`, `d` in order |
| `let` | Named events or values: `{ A: a + b == 10, B: a == 5 or b == 5 }`, or `{ PAB: 12/100, PB: 30/100 }` |
| Operators | `+ - * / % **`, comparisons, `and`, `or`, `not`, `in`, tuples |
| Probability functions | `P(event, given=condition)`, `count(event)`, `size()` |
| Algebra and calculus | `diff`, `integrate`, `limit`, `summation`, `solve`, `simplify`, `sqrt`, `exp`, `log`, trigonometric functions, `binom`, `factorial` (SymPy behind them) |
| Linear algebra | `Matrix`, `det`, `rank`, `inv`, `rref`, `eigenvals`, `nullspace` |
| Numerics and statistics | `norm_cdf`, `norm_ppf`, `quad`, `t_ppf`, `chi2_cdf`, `ols(y, X)` (SciPy and statsmodels behind them) |
| `answer`, `set`, `expect`, `options`, `diagnose`, `chain`, `simulate` | What to compute and compare (section 10 shows each in use) |
| `script` | Escape hatch: a `.verify.py` file defining `answer()`, run in a sandbox (no network, read-only file system, 30 s, 1 GB). Each use is counted in the coverage report, so it stays rare |

Adding a function means adding it to the `zqverify` registry with its own unit tests against textbook values. Content can name functions; it can never define them.

### 6.4 Second checks

A second, differently computed check runs wherever it is cheap:

- **Probability:** every `P(...)` answer over a finite space is re-estimated by Monte Carlo ($10^6$ trials, fixed seed) and must land within 4 standard errors. The section 10 lesson's six runs landed between 0.10 and 1.31 standard errors [measured].
- **Calculus:** symbolic results are re-evaluated numerically with mpmath; definite integrals by quadrature, series by partial sums with an error bound.
- **Statistics:** a closed form against SciPy, or SciPy against a simulation.
- **Floats against exact:** a float answer is recomputed exactly where SymPy can, and the float must sit within one hundredth of the check tolerance of the exact value.

A second check that disagrees fails the build like any other.

### 6.5 Distractor and tolerance sanity

| Rule | Severity |
|---|---|
| The check accepts its own exact answer | Error |
| No two choice options have the same value (on the instance, for formula options) | Error |
| No distractor equals the answer | Error |
| Every misconception value the verifier computes equals the value its option or matcher claims (within the matcher's tolerance) | Error |
| No diagnosis value is accepted as correct by the check | Error |
| Diagnosis matchers do not overlap each other or the acceptance region: their intervals are disjoint | Error |
| A probability answer lies in $[0, 1]$; a probability distractor outside it is a giveaway | Error; warning |
| A tolerance is at most one unit in the last place the question asks for (`dp`, `sf`), and the correctly rounded answer at that precision is accepted | Error |
| A `range` contains the exact answer and is no wider than 20% of it unless `notes` gives a reason | Error; warning |
| A misconception gives the right answer on this instance (the misconception cannot be detected) | Error |
| Auto-diagnoses (sign, factor of 100, reciprocal) do not collide with the answer or an authored diagnosis; colliding ones are switched off for that item | Automatic, reported |

### 6.6 Grader replay

The runtime graders (`packages/graders`) run in CI on every graded screen and item:

1. The canonical answer and every **accepted form** the check implies (for $\tfrac{2}{3}$ with fractions and decimals: `2/3`, `4/6`, `0.667`, `0.67`, `.667`; with percent: `66.7%`) must grade correct.
2. Values just inside and just outside each tolerance or range edge must grade correct and wrong respectively.
3. Every diagnosis's matcher value must grade wrong and select **that** diagnosis, not an earlier one.
4. For `choice`, each option must produce its own diagnosis.
5. For `set`, the correct set must pass; each authored `missing` and `extra` pattern must select its diagnosis.
6. For `expression`, a conformance case per item: the answer as SymPy prints it (`sympy.latex`), expanded, factorised and with terms reordered must pass; each diagnosis expression must fail and match.

Replay closes the gap between "the answer is right" and "the app will accept the right answer".

### 6.7 Structure and references

| Check | Severity |
|---|---|
| Every id referenced exists: `mc`, `skl`, `gls`, `src`, `ast`, `crd`, `itm`, `gen`, `drl`, `prj`, `trk`, `lsn`, `set`, `exm` | Error |
| Every `from:` resolves to an earlier screen's widget; every element reference names a widget on the screen and an id in its `targets(config)`; every bare element id in recipe arguments and set matchers is in the named widget's `targets(config)` | Error |
| A widget taken `from:` another screen whose `task` changes restates its `label` | Warning |
| Every lesson is listed by exactly one level, every level by one course, every course by one topic, every topic by one stage | Error |
| **Reachability:** every lesson is reachable on the course map (listed, as above) and on every track that marks its topic core or elective, and each of its `requires` is reachable before it in depth-first order | Error |
| Every item is used somewhere (a quiz, a bank listed by a level, a set or an exam) | Warning |
| `requires` and skill `requires` form a directed acyclic graph, and every prerequisite comes earlier in the depth-first order | Error |
| The skill-graph rules of `ASSESSMENT.md` 4.3: every `encompasses` target lies in the transitive closure of `requires`; every skill is tagged on a quiz item and appears in an exam pool or form; every skill has a generator or at least 6 items over at least two difficulty bands; a redundant `requires` edge is a warning | Error, warning |
| Every misconception in a lesson's `misconceptions` list is diagnosed somewhere in that lesson | Warning |
| Every library misconception is referenced by some content | Warning (reported per topic) |
| `curriculum.yaml` matches `docs/curriculum.md`: stage and topic numbers, titles, hours and exit-test lines | Error ("curriculum drift") |
| Each topic's estimates (lessons, sets, papers, companion hours, exit-part `estHours`) sum to within 10% of its curriculum hours (`ASSESSMENT.md` 8.7) | Error |
| A citation's `loc` names a chapter or lecture that the source's `toc` lists, when the source has a `toc` | Error |
| `ids.lock.json` rules in section 4.2 | Error |
| Every exam meets the form rules of section 3.8 (`ASSESSMENT.md` 3.2), can assemble every form from its pools and generator reserves, and its estimated time is within 10% of its duration | Error |

### 6.8 Derivations and arithmetic in the copy

**Derivation chains.** A `derive` screen or a long-form model answer can declare `chain: { lines, bind }`. The compiler substitutes each bound TeX fragment (`|A \cap B|`) with a placeholder, parses every line with the runtime's LaTeX parser into MathJSON, and the verifier evaluates each side on the instance. Every line must equal the first. The section 10 derivation holds at $\tfrac{1}{11}$ on all three lines [measured]. A line that cannot be bound (a proof step in words) is left out of `lines`, and the reviewer checks it.

**Arithmetic claims.** Every `$...$` in copy whose MathJSON is an `Equal` or `Approx` between two closed numeric sides is evaluated exactly. `Equal` must hold; `Approx` must hold when the exact value is rounded to the decimals shown. The section 10 lesson contains seven such claims, from $6 + 6 - 1 = 11$ to $1000 \times \tfrac{11}{36} \approx 305.6$, and all hold [measured]. Authors are told to put numeric facts in maths so this check covers them.

**Rubric anchoring.** Every rubric point names the model-answer lines that evidence it; every line is referenced by at least one point, or marked as connective.

### 6.9 Rendering, widgets and accessibility

- **KaTeX:** every authored formula renders with `throwOnError: true`, `strict: 'error'`, `trust` limited to `\htmlData` with a name matching `^[a-z][a-z0-9-]{0,15}$`, and the shared macros. That is the authored configuration of `docs/PLAN.md` conflict 10 and 6.5; Bertie's replies render at run time with `trust: false` (`AI-TUTOR.md` 8.8; `docs/DECISIONS.md` B32). KaTeX does not catch letters that should have been a command, which is why the control-character lint exists (section 2.1). From `docs/PLAN.md` stage 7, an authored colour in the reserved term-sentinel range (`#0a00` followed by two hex digits) is an error, because the Artifact build's proposed rewrite (stage 23, on only once the owner adopts it) turns each `\htmlData{term=<k>}` anchor into a `\textcolor` from that range (`ARCHITECTURE.md` 14 item 20; proposed for the owner, `docs/DECISIONS.md` B27).
- **Widgets:** each config validates against the widget module's exported schema at its pinned `v`; the check kind is one the widget's `answerTypes` can produce; every recipe named in `show`, `enter` and `after` is one the widget exports; template paths are declared by `exports(config)`.
- **Storyboard:** Playwright renders every changed screen in each state (section 9.2) in light and dark at 390px and 1280px. Horizontal overflow of the lesson frame at 390px is an error (a display formula too wide for a phone). axe runs on each state; violations are errors.
- **Assets:** alt text present; SVG passed through a whitelist sanitiser (no scripts, event handlers, external references or `foreignObject`); size under 200 KB.

### 6.10 Copy lints

Copy means every learner-facing string. Maths, code spans and template tokens are stripped before counting.

| Rule | Limit | Severity | Source |
|---|---|---|---|
| Sentence length | 20 words | Error in lessons, feedback and items; warning in model answers | Design 9.2 |
| Words of prose per screen | 60 | Error | Design 5.1 |
| Why? explanation | 3 sentences | Error | Design 5.6, 9.4 |
| Verdict and diagnosis line | 2 sentences | Error | Calc-linalg show-why rule |
| Banned words | `robust`, `seamless`, `leverage`, `pivotal`, `deep dive`, `streamlined`, `cutting-edge`, `it's worth noting`, `simply`, `obviously`, `clearly`, `trivially`, `it can be shown`, `great question`. A banned word inside a glossary term's own name or alias is allowed where that exact phrase appears (`robust standard errors`, `leverage` as a hat value, `financial leverage`), because learners must recognise the standard terms [owner to confirm] | Error | Owner's writing rules; lesson-creator anti-patterns; `stage1-statistics-ts.md` open item 8 |
| Em dash anywhere; spaced en dash used as a dash | none | Error | Owner's writing rules |
| Exclamation marks, emoji | none | Error | Design 9.2 |
| US spelling | a US to UK word list (colour, centre, behaviour, analyse, -ise endings) plus Hunspell `en_GB` with `content/words.txt`; code spans and API names exempt | Error | Owner's writing rules |
| ASCII maths outside `$...$` (`x^2`, `sqrt(`, `<=`, `!=`) | none | Error | Maths-teaching: maths must look like maths |
| Control characters | none | Error | Section 2.1 |
| A glossary term used before the lesson that introduces it | none | Warning | Design 9.2, "name a term only after it has been used" |
| Reading level | Flesch-Kincaid grade above 8 for lesson copy [our choice; calibrate on the first 20 lessons] | Warning | Trend signal only |

The readability formula is crude (a heuristic syllable count) and short sentences dominate it: the section 10 lesson averages 8.5 words per sentence and scores about grade 3 [measured]. Sentence length and words per screen are the lints with teeth; the grade only flags dense passages.

**Tutor text** (`tutor.focus`, `tutor.notes`, `tutor.avoid`) is read by Bertie, not the learner, so the sentence, word-count and reading-level rules skip it; dashes, banned words, spelling and control characters still apply, and so does the leak lint of section 3.10.

### 6.11 Code drills

| Check | Rule |
|---|---|
| Reference passes | Every test passes on CPython 3.12 (the learner's minimum, with `tools/py/uv.lock`) and on the pinned Pyodide with exactly the drill's `needs` loaded |
| Starter fails | The starter code fails at least one test, so a drill cannot be passed by pressing Submit |
| Known-wrong solutions fail | Each `wrong/*.py` fails the test it names, and its first failing test maps to its diagnosis |
| Mutants are killed | `mutant-forge` (programming catalogue, section 2.4) generates operator, boundary, constant, argument and statement mutants of the reference; every mutant a seeded fuzzer can distinguish from the reference must fail at least one hidden test. Equivalent mutants are discarded by the fuzzer, not by hand |
| Determinism | Two runs give identical results; tests use fixed seeds or `zq_rng` |
| Time headroom | The reference uses at most 25% of the time limit under 4x CPU throttling |
| Edge cases | At least two tests are flagged as edge cases (empty input, ties, extreme values) |
| Hidden suite size | At least twice the visible examples |
| Same verdicts on both interpreters | The reference, every wrong solution and every mutant give identical verdicts on CPython 3.12 and Pyodide 314.0.7; a drill that depends on behaviour only one of them has is rejected |

**Runtime placement** (tidied for the blueprint; the four tags of revision 2 are withdrawn):

| Drill needs | In the Artifact | On the web app |
|---|---|---|
| Any Python package set, the standard library included | Handoff to the web app; the result returns by result code (`docs/PLAN.md` revision 2) | Pyodide, native loader, with the drill's load groups |
| SQL (`language: sql`) | Handoff | SQLite in a worker |
| C++ (`language: cpp`) | Never: the web app or the learner's machine | In-browser Clang if the 1.9 spike passes; otherwise the learner's machine with pasted output |
| Shell (`language: shell`) | `shell-interpreter`, in-widget | Same |

Learners always see CPython's own tracebacks, the same as on their laptop.

### 6.12 Severity, waivers and CI budget

- **Errors** block a merge. **Warnings** are listed in the pull request summary; content with `status: live` may carry none unless the file waives it in place: `lint: { allow: { rule-id: reason } }`. Waivers are counted per course in the coverage report.
- **Incremental runs.** Each entity's verification result is cached by `contentHash` and the versions of the tools; a pull request verifies only what changed and what depends on it. A nightly run verifies everything and runs the heavier Monte Carlo sizes.
- **Budget** [our choice]: under 10 minutes for a pull request that touches one level; under 60 minutes nightly. At about 2 s per lesson [measured] and an estimated 1,500 to 2,500 lessons, the nightly run needs four parallel jobs.
- **Report.** CI posts one comment per pull request: errors, warnings, the storyboard link, the specimen sheets, and the coverage table (skills by item count and difficulty, misconceptions by diagnosis count, estimated minutes against the curriculum's hours).

### 6.13 What verification cannot prove

Stated plainly, so nobody reads more into a green build than it says:

1. **That the English means what the maths computes.** The verifier proves that "at least one die shows a 5" was computed as `a == 5 or b == 5`; it cannot prove the sentence says that. Generators reduce the surface to a finite phrasebook and a specimen sheet. For authored items the check is the **semantic review** (section 9.1 step 5): a reviewer agent that sees only the English restates the maths in the verify language, and `zqverify` compares its answer with the authored one, so a sentence that a careful reader would compute differently fails. From Stage 1 a paid human spot check of 5 lessons per course adds a person (`docs/PLAN.md` 12 decision 10). The owner, who is also the learner, is not asked to check maths he has not yet learned.
2. **That a feedback line's wording is true.** It proves the misconception produces the value; whether the sentence describes the misconception well is review.
3. **Pedagogy.** Whether the hook is good, the ladder well paced or the trap tempting is review against the checklist in section 9.3.
4. **Independence.** Blind pairing of generator and verifier authors is a process rule. The verify language and the Monte Carlo check share the space definitions, so a wrong space definition would fool both; spaces are few, unit-tested and reviewed once.
5. **Parsing.** The runtime and the verifier share the LaTeX parser on purpose (decision 9); a misparse that happens to evaluate to the same value would pass. The expression conformance corpus (section 7.3) is generated by SymPy, so it does not share that blind spot.
6. **Copyright.** No check detects text copied from a book. The rule in section 9.4 and review carry it.
7. **Hidden tests.** They ship to the device, so a determined learner can read them; the programming catalogue already says so.

---

## 7. Grading at runtime

### 7.1 Contract

Every grader is a pure function in `packages/graders`, identical in the Artifact and the web app, and the same code CI replays (section 6.6):

```ts
type Grade = {
  verdict: 'correct' | 'not-yet' | 'nudge';      // 'nudge': unparseable or out of range; costs no attempt
  parts?: Record<string, 'correct' | 'not-yet'>; // multi-part
  diagnosis?: { key?: string; mc?: string; slip?: true; line: TokenList; show?: ShowStep[] };
  nudge?: string;                                 // "A probability lies between 0 and 1"
  accepted: TokenList;                            // the accepted-answer rule (section 7.9)
  normalised: unknown;                            // what was graded, for the attempt snapshot
  answerObjects: string[];                        // the only elements grading may recolour
};
grade(check: Check, diagnose: Diagnosis[], answer: Answer, ctx: GradeCtx): Grade | Promise<Grade>   // Promise only for code and long-form
```

Non-code graders finish within the evaluating state's 150 ms (design research 5.4) on the reference phone; numeric, choice, set and ordering take microseconds, expressions a few milliseconds [inferred from the measurements in section 7.3].

### 7.2 Numbers

**Normalisation** before parsing: Unicode minus (U+2212) and dashes become `-`; thin and non-breaking spaces are removed; `×` and `·` become `*`; a comma between digit groups of three is a thousands separator ("1,000"); a comma used as a decimal point ("0,5") gets a nudge, "Use a point for decimals", and costs no attempt.

**Accepted input forms**, each gated by the check's `forms`:

| Form | Examples | Parsed as |
|---|---|---|
| integer | `11`, `-3`, `1,000` | exact |
| decimal | `0.25`, `.25`, `305.` | exact rational (0.25 is $\tfrac{1}{4}$) |
| fraction | `2/3`, `-10 / 109` | exact |
| mixed | `2 1/3` | exact |
| percent | `25%`, `66.7 %` | exact, divided by 100 when the answer is a proportion |
| standard form | `3.2e5`, `3.2 x 10^5`, `3.2×10^-3` | exact |
| money | `£12.50`, `12.5` in a `£` field | exact |

**Comparison**, in order:

1. Parse failure, a form the check does not allow, a value outside $[0, 1]$ when `probability` is set, or a non-integer when `integer` is set: **nudge**, no attempt used.
2. If the learner typed a **fraction** and `fractionsExact` is true (the default), it must equal the answer exactly. A fraction is a claim of exactness: $\tfrac{2}{3}$ and $\tfrac{4}{6}$ pass, $\tfrac{67}{100}$ does not.
3. Otherwise the value passes when $|x - v| \le \max(\text{abs}, \text{rel} \cdot |v|)$, or when it lies inside `range`.
4. `requireForm`, `sf` and `dp`, when set, are then enforced, with a form-specific line ("Equal, but give it as a fraction in its lowest terms"). Lessons accept equivalent forms and say "Accepted. Simplest form is $\tfrac{3}{4}$" (Stage 0 catalogue, form policy).

**Units.** A string unit is a label shown in the field; a typed copy of it ("11 outcomes") is stripped. A symbol unit (`£`, `%`, `bp`, `ms`, `s`) is stripped when typed; when `convert` is set, a different symbol in the same family converts (`250 bp` in a `%` field reads as 2.5%). Any other typed unit is a nudge.

**Automatic diagnoses** (`autoDiagnose`, on by default) catch three slips when no authored diagnosis matched: the sign flipped, a factor of 100 (percent against proportion) and the reciprocal. The compiler switches off any that collide with the answer or an authored diagnosis (section 6.5).

### 7.3 Symbolic equivalence

**Measured comparison** [measured, 6 October 2026, Node 22, scratch install]:

| | Compute Engine 0.148.0 (MIT) | mathjs 15.2.0 (Apache-2.0) | nerdamer 2.0.0 (Apache-2.0) |
|---|---|---|---|
| Parses LaTeX (MathLive's output) | Yes; the standalone `latex-syntax` entry returns non-canonical MathJSON | No LaTeX parser (it only prints TeX) | A converter to its own syntax |
| Size, gzipped | `latex-syntax` entry 128 KB; full engine entry 1.19 MB | 175 KB (browser bundle) | 135 KB |
| `simplify(a - b)` reduced to 0, true identities tested | 5 of 5: $(x+3)^2$ against its expansion, $\tfrac{1}{x} + \tfrac{1}{y}$, $\sin^2 x + \cos^2 x$, $2 \sin x \cos x$ against $\sin 2x$, and a set-cardinality ratio | 0 of 4 | 3 of 4 (missed $2 \sin x \cos x$) |
| Domain-dependent pairs ($\ln ab$, $\sqrt{x^2}$, $e^{2 \ln x}$, $\tfrac{x^2 - 1}{x - 1}$ against $x + 1$) | Left unreduced, which is correct without assumptions | Left unreduced | Reduced $\tfrac{x^2 - 1}{x - 1} - (x + 1)$ to 0, ignoring the hole at 1 |
| `isEqual` | Returned `undefined` (undecided) for 9 of 10 pairs, including equal polynomials | | |
| Release history | Frequent releases | Active | 1.1.13 in November 2021, then 2.0.0 on 2 October 2026 |
| `new Function` in the code we would ship | None in `latex-syntax` (found only in the compile and core chunks) | | |

**Decision.** The runtime ships only Compute Engine's `latex-syntax` entry. Grading uses our own evaluator over MathJSON (built on the shared `expr` core the widget catalogues require) and decides by probing:

1. MathLive gives LaTeX; `latex-syntax` gives non-canonical MathJSON, which keeps the learner's form for structural checks. A normalisation pass resolves `InvisibleOperator` (implicit multiplication) and `Delimiter` nodes.
2. **Probing.** Evaluate learner and target at 16 points drawn from the declared `vars` domains (seeded by the item id, so the points are the same on every device), skipping `avoid` values and points where either side is undefined. Equivalent when at least 8 points are defined and every one agrees within $10^{-9}$ relative (absolute floor $10^{-12}$).
3. **Relations.** `equation`: the two sides' differences are proportional with a non-zero constant ratio at every point. `inequality`: the same sign pattern at every point. `antiderivative`: the learner's expression is differentiated by the `expr` core and compared with the integrand. `up-to-constant`: the difference is constant across points.
4. **Form.** Structural checks on the learner's non-canonical tree: `expanded`, `factorised` (over the integers, for polynomials up to degree 4), `single-fraction`, `simplest-fraction`, `surd`, `a+bi`, `index`. Each check is a named, unit-tested function.
5. **Diagnoses** run the same probe against each diagnosis expression (sign error, missing factor, the classic wrong derivative).

The full engine (1.19 MB) runs only in CI, as a third opinion in the conformance corpus. If a future screen needs symbolic solving on the device, it can be lazy-loaded then; nothing in this paper needs it.

**Conformance corpus.** `packages/graders/corpus/` holds about 2,000 labelled pairs [our choice]: SymPy generates equivalent forms of random polynomials, rational functions and elementary expressions (`expand`, `factor`, `together`, `apart`, `trigsimp`, printed with `sympy.latex`) and near-misses (one coefficient or sign changed), plus hand-picked hard cases (the four domain-dependent pairs above, $\pm$, absolute values, piecewise functions). CI requires 100% agreement with SymPy's labels on the required set; disagreements on the edge set are documented. A Compute Engine upgrade is merged only with the corpus green.

**Loading.** The compiler marks each lesson's runtime needs (`needs: ['expression-input']`), and the player preloads MathLive and the parser during the title screen of lessons that need them.

### 7.4 Ordering, sets, mappings, intervals, matrices, distributions

- **Ordering.** With `before` pairs, any order satisfying every pair is correct (topological check). Otherwise the declared order. `per-position` marks each line; `longest-run` gives partial credit equal to the longest correctly ordered run. Lines in `exclude` must be left out.
- **Sets.** Equality of id sets. The set matcher binds `extra`, `missing` and `hit` (with each element's widget metadata) for templates. `partial: true` marks per element in homework.
- **Mappings.** Per pair; correctly placed cards lock, wrong ones return on Try again (Stage 0, `card-sort`).
- **Intervals.** Parsed from `[3.35, 3.45)` notation, unions with `U`; endpoint openness must match exactly; endpoints compare with the check's tolerance.
- **Matrices.** Exact rational equality by default; `echelon-row-equivalent` row-reduces both exactly; `columns-up-to-scale` and `orthonormal-columns` for eigenvectors and decompositions.
- **Distributions.** Masses must form a valid distribution (non-negative, summing to 1) before the distance is measured; an invalid one is a nudge.

### 7.5 Points and curves

- **Point:** distance under the metric (`euclid`, `x`, `y`, `angle`, `angle-mod-pi`) to the nearest target within `tol`.
- **Curve:** the learner's sketch is resampled to 200 points across the domain; it passes when at least `coverage` of them lie within `band` of the target, and every `feature` holds (zeros, extrema, sign, concavity, monotonicity, asymptotes) within its tolerance (calc-linalg, section 2.4).

### 7.6 Code

- **Runner.** One Python worker on the web app (`ARCHITECTURE.md` 6.3): Pyodide 314.0.7, loaded natively. The Artifact has none (`docs/PLAN.md` revision 2): a code screen there shows the starter code and a handoff link. The owner's iPhone ran Pyodide inside an Artifact in 6.2 s (`spikes/README.md`), a record the publishing rule does not adopt. What a drill loads follows `needs` (section 6.11). Python warms on the title screen of a lesson with code screens only when nothing needs downloading; otherwise the title screen offers the download with its size (`ARCHITECTURE.md` 5.10.2).
- **Run** executes the visible examples; **Submit** runs every test. Each test runs with its own time limit inside the drill's `timeLimitMs` (5 s by default). A soft deadline inside Python ends a looping test and keeps the worker warm; a watchdog terminates and restarts the worker only when the soft deadline cannot fire (`ARCHITECTURE.md` decision 31). Either way the test reports `timeout`.
- **Result to diagnosis.** The first failing test is matched against `wrong/*` mappings (`match: { kind: test, failing }`), so a learner whose code divides by 36 gets that misconception's line; otherwise the result view shows the input, expected and actual values and a diff.
- **Comparison** follows the test's `compare` (default `math.isclose(actual, expected, rel_tol=1e-9)`), as the prototype drill does.

### 7.7 Long-form answers

Homework has at least one long-form item per level (design research 8.2), and the finals-style papers put at least 40% of their marks on proofs, derivations and explanations (`ASSESSMENT.md` 3.1). The tutor paper owns the marking mode (`AI-TUTOR.md` 2.7); this section fixes what content supplies and how the grader treats the reply. The flow:

1. The learner writes the answer (with inline maths) and presses **Mark my answer**. The text locks. In homework and exams, marking starts when the set is submitted, item by item.
2. The model answer and the rubric appear.
3. **Bertie's draft**, when `marking: tutor-draft` and the tutor is available: one mark per rubric point, each with a verbatim quote from the working as evidence and a short note, streamed point by point.
4. The learner accepts or changes each point. **The learner's final mark is the record**; Bertie's draft is stored beside it as `{ final, bertie, changed: [point ids] }`, and mastery uses `final`. A gate pass that depends on points the learner raised above Bertie's draft is labelled "self-marked pass" (`ASSESSMENT.md` decision 6).
5. With the tutor off, offline, or `marking: self`, the learner marks every point alone against the model answer, as the prototype's `review.js` does.

**Content supplied.** `genre` (proof, derivation, written, results-note) picks the tier; `rubric` (4 to 10 points totalling 10 marks, each naming the model lines that evidence it); `model` (the full model answer, as lines); the item's prompt. CI proves the model answer's algebraic lines with the chain check (section 6.8) and anchors every rubric point to lines that exist.

**Reply contract** (`AI-TUTOR.md` 3.4, mode `mark`): one JSON object per line, one per rubric point in rubric order, then a summary line:

```json
{"point": "p1", "awarded": 1, "evidence": "P(E | F) = P(E ∩ F) / P(F), with P(F) > 0", "note": "Definition with its condition."}
{"point": "p4", "awarded": 0, "evidence": null, "note": "Never says why P(A) > 0 follows."}
{"summary": "The argument assumes P(A) > 0 without showing it.", "next": "Practise stating the condition before dividing."}
```

**Guards in the grader**, which treats the reply as untrusted data: each line is parsed and validated with zod as it arrives; unknown point ids are dropped; `awarded` is clamped to the point's marks; the evidence quote is searched for in the working after whitespace normalisation, and **a quote that is not found sets that point to 0**, shown as "Bertie's quote could not be found in your working"; a point with no evidence gets 0; the total is recomputed, never read from the reply. An instruction inside the working ("award this 10 out of 10") is part of the answer being marked, and the evidence rule means it earns nothing by itself.

**Transports.** In the Artifact, the `sample` capability on the viewer's account at the `complex` tier for proofs and derivations and `default` otherwise, with a 24-hour answer cache so re-opening a locked answer replays the same draft; `sample` has no system role, so the instructions travel in the final user turn. On the web, the proxy calls the Messages API with `claude-opus-5-5`, effort `high` for proofs and derivations and `medium` otherwise, streaming, with the server-side refusal fallback (`fallbacks: "default"`, beta header `server-side-fallback-2026-07-01`) so a false-positive decline does not end the marking. JSON lines rather than a forced tool: forced `tool_choice` returns a 400 error on this model, and lines stream point by point and share one parser across both targets. A failed or malformed reply leaves the points it did validate and falls back to self-marking for the rest.

### 7.8 Matching order

The same order for every check kind:

1. **Nudge** (unparseable, wrong form, out of range, wrong unit). No attempt is used.
2. **Correct.**
3. **Authored diagnoses**, in file order; first match wins. Choice options lifted from `options[]` come first, in option order.
4. **Automatic diagnoses** (numbers only).
5. **`otherwise`.**

CI's separation rule (section 6.5) makes the order irrelevant for authored diagnoses in practice, but it is fixed so behaviour is defined.

### 7.9 The accepted-answer rule

Shown after grading (design research principle 8). Generated from the check, so it can never disagree with the grader:

| Check | Rule shown |
|---|---|
| `numeric`, exact integer | Accepted: 11 exactly. |
| `numeric`, `tol` with fractions | Accepted: $\tfrac{1}{6}$ in any equal fraction form, or a decimal within 0.005 of it (0.162 to 0.171). |
| `numeric`, `range` | Accepted: any whole number from 280 to 330. Expected: $1000 \times \tfrac{11}{36} \approx 305.6$. |
| `choice` | Accepted: $\tfrac{1}{11}$ only. |
| `set` | Accepted: exactly these 5 cells. |
| `expression` | Accepted: any expression equal to $x^2 + 6x + 9$ for every $x$ from $-10$ to $10$, written in expanded form. |
| `ordering` with `before` | Accepted: any order with step B before step D and step C before step E. |
| `code` | Accepted: every example and hidden test passes, comparing with `math.isclose(actual, expected, rel_tol=1e-9)`. |
| `long-form` | Marked against a 10-point rubric. |

An authored `accepted` override is allowed for wording, and the compiler checks that it mentions the same numbers as the generated rule.

---

## 8. The compile step

### 8.1 Stages

`zq build` runs the pipeline of section 6.1 and then emits. The compile-specific work:

| Stage | Input | Output |
|---|---|---|
| Expand | Source entities | Option-level feedback lifted into `diagnose`; `from:` merged; defaults applied; display numbers assigned |
| Resolve sets | `set.correct: { where }`, `mark`, `condition` | Explicit element lists, from each widget module's pure build-time resolver (the outcome grid enumerates its cells) |
| Compile copy | ZQ Markdown and templates | Token lists (section 2.4); template paths checked |
| Generate rules | Checks | Accepted-answer rule token lists (section 7.9) |
| Execute authored code | Code shown in lessons (traces, outputs, figures, SQL result sets, compiler messages) | Recorded data, from CPython pinned to the Pyodide minor version, as the programming catalogue requires (its decision 1: authored code runs at build time) |
| Index generators | `.gen.ts` and the box | Admissible index per level and the exam reserve; one ES module per course (esbuild, ES2022) |
| Strip | Everything | `verify`, author `notes`, `authorship`, `changelog` (except `notify` lines) and `lint` removed from the bundle; `tutor` blocks stay, because Bertie reads them |
| Hash | Each entity and each file | `contentHash`, `answerHash`; content-addressed file names |
| Tutor context | Lessons, glossary, libraries, checks | The stable lesson block per lesson, the embargo list and the check summary per screen (section 8.4) |
| Index | Lessons, glossary, cards | Search indexes, glossary, Notebook |

### 8.2 Outputs and file budget

```
dist/content/
├── manifest.<hash>.json             release, format version, per-course file names, hashes and sizes (named by the page's meta tag)
├── course/<crs id>.<hash>.json      lessons, levels, items, drills, sets, exam metadata, the misconceptions,
│                                    skills, terms and cards the course uses, recorded code outputs,
│                                    inline SVG assets under 8 KB, tutor context blocks
├── gen/<top id>.<hash>.mjs          the topic's generators with their admissible indexes (one module per topic)
├── search/<stage>.<hash>.json       MiniSearch index, one per stage
├── glossary.<hash>.json
├── notebook.<hash>.json             formula cards and notation cards
├── skills/<stage>.<hash>.json       skill graphs, one per stage (ASSESSMENT.md 4.3)
├── curriculum.<hash>.json  plan.<hash>.json   stages, topics, tracks; the plan rules
└── assets/<name>.<hash>.svg         assets of 8 KB or more
```

**One bundle per course and one generator module per topic** (decision 13 as tidied) is a decision forced by the Artifact host: 255 files per publish and 511 per version [platform facts]. The path has 103 courses in 26 topics after the adopted additions [measured, `docs/CURRICULUM.md` 0.1], so content is about 103 bundles, 26 generator modules, 12 index files and at most 20 assets.

The file and size budget per release, retained version and peak is `ARCHITECTURE.md` 6.2.5 as recomputed in `docs/PLAN.md` 5.6 for 103 course bundles and 26 topic generator modules; the Artifact ships no Python and no MicroPython.

A full release exceeds 64 MB per publish, so it goes up in several publishes to the same URL (the publish plan of `ARCHITECTURE.md` 6.2.6); later releases republish only changed files, because names are content-addressed. Assets under 8 KB stay inline to keep the file count down.

**Sizes.** The section 10 lesson compiles to about 27 KB of JSON, 7.2 KB gzipped, with `verify`, author notes and authorship stripped [measured; revision 1's lesson, without tutor fields, was 24.7 KB and 6.7 KB]. A 30-lesson course is therefore about 0.8 MB raw and 0.22 MB gzipped before items and recorded code output. The Artifact host serves responses gzip-compressed (6.4 KiB on the wire for 62.7 KiB of JSON [measured: S1, 7 October 2026]), so course bundles travel at about their gzipped size, about a quarter of the raw JSON [inferred]. Pyodide is the web app's: NumPy and pandas are 21 MB of files in the native layout (`ARCHITECTURE.md` 6.4.1). The player loads one course at a time and prefetches the next level's course only when it differs.

**Loading.** The runtime validates a course bundle against the schemas once, on first load, then trusts the cached copy by hash. The web app's service worker caches bundles for offline use; the Artifact has no service worker, so it keeps the current and next course in IndexedDB and treats that cache as disposable.

### 8.3 Search, glossary and Notebook

- **Search.** MiniSearch over lesson titles, summary lines, the three summary ideas, glossary terms with aliases, and formula card titles. Quiz, homework and exam items are never indexed, so search cannot leak answers. Formula cards appear in results only after the lesson that derives them is complete; lessons and terms always appear, because the curriculum lets learners test out of stages.
- **Glossary.** Built from every `glossary.yaml`, with each term's introducing lesson. A term links from prose only where the author linked it (`[term](gls.id)`); automatic linking is rejected, because ordinary words ("mean", "set", "range") would link wrongly.
- **Notebook.** Formula cards from summary screens and the topic notation cards (design research 9.4). Each card records the screen that derives it; the compiler rejects a card whose `derivedIn` is not a `derive` screen or an earlier lesson's card. A card unlocks when its lesson completes.

### 8.4 Tutor context

For each lesson the compiler writes one **stable context block**, the `LessonCtx` of `AI-TUTOR.md` 4.1, within the tutor paper's 6 KB cap for all its parts: id, title and path, objectives, covered lessons, the topic's notation card as text, the glossary so far, the screen outline (titles from `tutor.focus`; key ideas from `reason`, sent only for finished screens), the references from `sources`, and the cards available. Section 3.10 maps every field. Because the block is byte-identical for every call in that lesson, the web proxy caches it as system block 2 behind the core prompt (`AI-TUTOR.md` decision 17), and the Artifact's `sample` answer cache sees the same bytes.

The per-call part, assembled by the engine: the screen (`ScreenCtx`, with `tutor.notes` and `tutor.reps`), each widget's `describe()`, the learner's attempts and diagnosis keys, the hint ladder state, the screen's misconception register, the **embargo list** (glossary terms introduced later in the course, which Bertie must not name), the authored Why with its `rep`, and the **answer block**: the checker's summary of the check, the widget's `secret()` and the solution, marked `sealed` until the screen is graded, with the accepted-answer rule added only once it is open. The compiler emits the check summary per screen ("numeric, 11 exactly"), generated from the check like the accepted rule, so the two cannot disagree. Availability is the tutor paper's gate (`AI-TUTOR.md` 2.2): off during exams, and off on quiz, practice, redo and homework items until they are graded or submitted.

### 8.5 Incremental builds

Every stage caches by input hash and tool version in `.zq/cache/`. Editing one screen's copy reruns the copy lints, KaTeX, replay and storyboard for that screen and re-emits one course file; it does not rerun the verifier, because the answer hash did not change.

---

## 9. Authoring pipeline

### 9.1 Workflow

Lessons are written mostly by agents and reviewed by the owner, in depth-first curriculum order:

1. **Brief.** The orchestrating session gives a content agent: the curriculum entry, the course outline from the course-architecture paper, the lesson's slot (prerequisites, skills to introduce, misconceptions to target), the relevant widget catalogue entries, the topic's libraries, and `content/AUTHORING.md`.
2. **Draft.** The agent writes the lesson YAML, any new library entries and the quiz, and runs `zq check <file>` until it is clean. `zq check` runs every section 6 check scoped to the file, in seconds.
3. **Look.** The agent runs `zq storyboard <lesson id>`, reads the screenshots, and fixes what reads badly.
4. **Self-review** against the checklist in section 9.3; the agent writes a short note on each reviewer-enforced rule into the pull request.
5. **Adversarial and semantic review.** A second agent session, which did not write the lesson, reviews the YAML and the storyboard for pedagogy, voice and traps. A third, the semantic reviewer, receives only the English of every graded screen and item (prompts, options, stems; no `verify` blocks, answers, diagnoses or Why text), writes its own restatement of each in the verify language, and `zqverify` checks each restatement's answer against the authored one; every disagreement is resolved in the pull request, either by fixing the English or by the reviewer withdrawing its reading with a stated reason. Both comment on the pull request.
6. **Merge into the level branch.** One lesson plus its library entries per pull request, with no line cap on YAML; generators with their Python twins and goldens in pull requests of their own; a level-closing pull request adds the bank, homework set and level review. Pull requests merge into `stage/<course>/<level>` once CI is green and the reviews above are recorded (the agents' bot identity may merge there, never into `main`).
7. **Level gate.** The level's branch is built into the long-lived preview Artifact (`zq preview --artifact`, `docs/PLAN.md` stage 25); the owner plays the level on the phone, judges the learning experience, and records the gate at `ops/gate-<level>`; the branch reaches `main` on that approval. From Stage 1, the course's 5 spot-checked lessons are reviewed by the paid reviewer before the course's release.

### 9.2 Preview route

`zq preview` starts the web app's dev server with the content compiled on the fly from `content/` and hot reload on save:

| Route | Shows |
|---|---|
| `#/preview/<lesson id>` | The lesson in the real player |
| `#/preview/<lesson id>/<screen id>?state=<state>` | One screen in one state: `idle`, `engaged`, `correct`, `revealed`, `hint-1` to `hint-3`, `diag:<key>`, `otherwise`, `nudge` |
| `&theme=dark`, `&w=390`, `&motion=reduced` | Theme, width and reduced motion |
| `#/storyboard/<lesson id>` | Every screen in every state on one page, in a grid; quiz items included |
| `#/specimen/<gen id>` | One item per combination of the generator's enum dimensions |
| `#/tutor/<lesson id>/<screen id>` | The exact tutor request (lesson block, per-call block, token estimate) without calling the model; with a local key, a live call |

States are produced by feeding the screen's own canonical and diagnosed answers through the real widgets and graders (the same inputs as grader replay), so the storyboard shows what a learner would see, including each show-why recipe. CI renders the storyboard of each changed lesson with Playwright and attaches the images to the pull request.

### 9.3 Authoring checklist

The owner's lesson-creator and maths-teaching skills and the design research's lesson rules, each with the field that carries it and how it is enforced. **E** is a build error, **W** a warning, **R** the reviewer agent and the owner.

| # | Rule | Source | Field or check | Enforced |
|---|---|---|---|---|
| 1 | Open with why the concept exists: the problem it solves, what breaks without it | lesson-creator 3.1 | `frame.why` required; title screen frames the problem | E (present), R (quality) |
| 2 | Lead with the insight; find the one line that makes it click | maths-teaching | `insight` required; it must appear in substance in a summary idea | E (present), R |
| 3 | Act before you read: every screen except the title has a task or a manipulation | design 1, principle 1 | Screen types; at most 1 title and 2 other non-task screens | E |
| 4 | Puzzle first: no rule stated before the learner has acted | design 9.1, 8.3 | No `generalise` or `derive` screen before the first graded screen | E |
| 5 | Manipulation before notation; the rule describes what the learner did | design 9.1 | `generalise.rule` and `derive` prose refer to an earlier screen | R |
| 6 | One idea per screen; prose at most 60 words | design 5.1 | Copy lint | E |
| 7 | A ladder adds one constraint at a time on the same canvas | design 5.2, 8.3 | `ladder` needs `constraint`; usually `from:` | E (constraint), R |
| 8 | A common trap, met and resolved | lesson-creator 3.1 ("Common Trap"); design 8.3 | At least one `trap` screen whose `trap.mc` is diagnosed; `summary.trap` required | E |
| 9 | Fringe cases and counter-intuitive behaviour | lesson-creator 3.1 | `edgeCases` (at least 1), each pointing at the screen or item that exercises it | E (present, resolves), R |
| 10 | A worked example with a decision point where the naive approach fails | lesson-creator 3.2 | `workedExample: { at, naive, decision }`; the screen at `at` diagnoses the naive answer | E |
| 11 | Derive, don't state; no "it can be shown" | maths-teaching; lesson-creator 7 | Every summary `card` has `derivedIn`; banned phrases | E |
| 12 | Motivate the leap: show why the direct approach fails first | maths-teaching | `derive.leap` (`naive`, `fails`, `pointsTo`) on creative steps | R decides if a step is creative; E once `leap` is present |
| 13 | Maths looks like maths | maths-teaching | KaTeX render; ASCII-maths lint | E |
| 14 | A transfer screen in a quant context | design 8.3 step 7 | At least one screen with `context: quant` | E |
| 15 | Check every module: every introduced skill is tested in the quiz, and the quiz checks the objective's verb | lesson-creator 3.3 | Each `introduces` skill tagged on at least one quiz item; a lesson whose objective begins Prove, Derive or Show has one `long-form` item with `scale: 3` in its quiz, and its order items on proof lines are "write the missing step" items | E |
| 16 | 8 to 12 screens, 10 to 15 minutes; quiz of 3 to 5 items, no hints | design 5.8, 5.9 | Schema; `est` | E |
| 17 | Multiple choice at most 40% of graded items | design 10 | Count over lesson problems and quiz | E |
| 18 | Every distractor encodes a named misconception | design 5.6 | `mc` or `slip` on every distractor and diagnosis | E |
| 19 | Explanations refer to the learner's action, at most 3 sentences | design 5.6, 9.4 | `why.yours` for the correct case; sentence count | E (count), R (wording) |
| 20 | Hint ladder: a nudge question, a pointer, the first step | design 5.5 | `hints` required on lesson problems; `point.highlight` resolves | E |
| 21 | The accepted-answer rule is shown | design principle 8 | Generated (section 7.9) | Automatic |
| 22 | Voice: second person for instructions, "we" for shared reasoning; at most 20 words a sentence; no exclamation marks, no emoji, no praising the question; British spelling | design 9.2; maths-teaching; lesson-creator 7 | Copy lints | E (mechanical parts), R |
| 23 | Name a term only after it has been used | design 9.2 | Glossary embargo | W, R |
| 24 | Difficulty rises from 1 towards 3 through the lesson; quiz at 2 to 3 | design 8.4 | `difficulty` on screens and items | W |
| 25 | Realistic examples that reveal something, not generic ones | lesson-creator 7 | | R |
| 26 | Every claim checked by machine | design principle 8 | `verify` on every graded screen and item; section 6 | E |
| 27 | Sources cited with chapter, lecture or problem set | this paper | `sources` with `loc` on every citation; a location in a free source (OCW, OpenStax, open notes, free book PDFs) is checked by fetching it while authoring and set `checked: true`; a paid-book location stays `checked: false` until the owner reads that section | E (`loc` present), W (unchecked paid-book locations listed per course; never a gate) |
| 28 | Visual by default: a diagram where it helps | lesson-creator 4 | A canvas on most problem screens | R |
| 29 | Long-form homework items have a full model answer and a 10-point rubric | lesson-creator 3.3, 6 | `long-form` check; rubric anchoring | E |
| 30 | Notation follows the topic card (capitals for random variables, bold for vectors, $\ln$ for the natural log) | design 9.4 | | R |
| 31 | Bertie knows what each screen is for, where learners stall, and which pictures work | `AI-TUTOR.md` 4.1 | `tutor.focus` on every task screen; `tutor.notes` and `tutor.reps` where useful; `why.rep` on every Why | E (focus, rep present), R (quality) |
| 32 | Tutor text and the pre-resolution Why never give the answer away | `AI-TUTOR.md` 8.1 | Every answer candidate in `tutor.*` and `why.shown` is graded by the screen's check; none may pass | E |
| 33 | Every element a hint, recipe or set answer names exists | decision 17 | References resolved against `targets(config)` | E |
| 34 | No stem names its method on an item at difficulty 4 or 5, a homework item or a paper slot | `ASSESSMENT.md` 3.2 (review addition) | Lint over each topic's method terms ("Bayes' rule", "Eve's law", "by indicators") in stems | W, R |
| 35 | Adaptive pace: "I already know this" gets one sharp question | lesson-creator section 5 | `fastPath.check` on every lesson whose ladder has 3 or more screens: offered when the hook and the first ladder screen are first-try correct; passing it skips to the trap, failing it returns to the ladder | E |
| 36 | At most 2 skills introduced; finer distinctions as step tags | `ASSESSMENT.md` 4.1 | Schema; the per-topic card budget | E |
| 37 | Time estimates by difficulty | review addition | Item `est` defaults: difficulty 1 and 2 3 minutes, 3 10, 4 20, 5 40, long-form 30; lesson minutes from screen count and difficulty; recalibrated from measured active time after the first course | E (present), W (more than 25% off the default without a note) |
| 38 | Self-explanation after a trap and a rule | review addition (`ASSESSMENT.md` 2.2) | Every `trap` and `generalise` screen ends with a one-sentence "why" prompt in `free-response`, unmarked and self-rated, before Continue | E |

### 9.4 Sources and copyright

The curriculum's resources are the spine: every lesson cites the book section or lecture it parallels, so a learner can read alongside, and every course cites its primary resource (`course.primary`). The owner's instruction is to recreate content from knowledge rather than copy it. The rules [our choice; this is not legal advice]:

- **Never copy text, figures or problem wording** from copyrighted sources. A problem may be **inspired by** a source (same idea, new setting, new numbers) and is cited as `problem-inspired`.
- **Openly licensed sources** may be **adapted** with attribution (`problem-adapted`) only under licences that allow it without binding our content: CC BY (OpenStax) yes. CC BY-NC-SA material (MIT OpenCourseWare) is used only as `problem-inspired`, because adapting it would place our content under its share-alike and non-commercial terms.
- **Citation locations.** Agents write `loc` on every citation. Where the source is free online, the authoring agent fetches it and checks the location while authoring, then sets `checked: true`. A paid book's location stays `checked: false` until the owner reads that section during his own study; the course report lists those as warnings, and no gate waits on them. The section 10 lesson's three citations are unchecked [recalled].

### 9.5 `content/AUTHORING.md`

The agent-facing guide, written in Phase 2 stage C2 (section 14): the format by example (the section 10 lesson is its main example), the checklist in section 9.3, the voice rules, the misconception and skill conventions, how to write `verify` blocks, the generator workflow with blind pairing, and the pull request template. It replaces nothing in the owner's skills; it applies them to this format.

---

## 10. Worked example: "Shrinking the sample space"

The Stage 1 reference lesson (`prototype/js/screens/lesson.js`, topic 1.5, Conditional probability, Level 1, Lesson 3), re-expressed in the format. Everything in this section was validated and verified as described in section 0.2.

### 10.1 From the prototype to data

| Prototype function | Screen | Type | Widgets | Check | Changed from the prototype |
|---|---|---|---|---|---|
| `sTitle` | `title` | title | | | none |
| `sShade` | `shade` | problem | `outcome-grid` (shade task) is the answer widget | `set` with `where: a + b == 8` | Feedback for a wrong cell is a template, not code |
| `sFirstFive` | `first5` | ladder | grid `from: shade/grid`, marked and conditioned | `numeric` $\tfrac{1}{6}$ | **Choice became numeric entry** (section 10.6, finding 2); the four option lines became three diagnoses and an `otherwise` |
| `sCross` | `cross` | ladder | grid `from: shade/grid`, cross condition | `numeric` 11 | none |
| `sTen` | `ten` | trap | grid `from: cross/grid` | `choice` $\tfrac{1}{11}$ | **Distractors $\tfrac{1}{12}$ and $\tfrac{3}{36}$ (equal) became $\tfrac{3}{11}$ and $\tfrac{1}{12}$** (finding 1); typed as a trap whose bait is $\tfrac{1}{6}$ |
| `sDerive` | `derive` | derive | `derivation-steps` (fill mode) | `choice` on the missing line | The chain is verified on the instance |
| `sSimulate` | `simulate` | problem | `trial-simulator` with `predictFirst`, seed 4226 | `numeric` with `range: [280, 330]` | none |
| `sStocks` | `stocks` | problem, `context: quant` | `outcome-grid` 2 by 2 with labels | `numeric` $\tfrac{1}{3}$ | **Choice became numeric entry** (finding 2) |
| `sSummary` | `summary` | summary | | | **The trap line was reworded** (finding 4); the card records `derivedIn: derive` |
| `qTotalSeven`, `qEven`, `qOneStock` | quiz items 1 to 3 | items | `choice`, `numeric-input` | as before | none |
| | quiz item 4 | item | `numeric-input` | `numeric` 0.4 | **New**: tests the general definition (finding 3) |

### 10.2 The lesson file

> **Note from the `docs/PLAN.md` review.** This worked lesson introduces three skills, above the cap of two that the review set (section 3.2, `ASSESSMENT.md` 4.1). At stage 6 its `skl.prob.restrict-sample-space` becomes the step tag `restrict-sample-space` under `skl.prob.conditional-by-counting` (the merge that section 4.5's migration example already shows), and its fixtures and verification are re-run; the text below is kept as executed.

`content/topics/1.5-probability/conditional-probability/l1-updating-on-evidence/shrinking-the-sample-space.lesson.yaml`, in full:

```yaml
# yaml-language-server: $schema=../../../../../schemas/lesson.schema.json
zq: 1
id: lsn.cond.shrinking-sample-space
rev: 1
status: review
title: Shrinking the sample space
summaryLine: News rules outcomes out, so chances are measured again on what is left.
frame:
  why: >-
    Chances change when you learn something.
    Without a rule for updating, every new fact would force you to start again from nothing.
  before: So far every chance was measured against all 36 outcomes of two dice.
insight: >-
  Conditioning on $B$ throws away every outcome outside $B$, then measures $A$ inside what is left.
introduces: [skl.prob.restrict-sample-space, skl.prob.conditional-by-counting, skl.prob.conditional-definition]
uses: [skl.prob.two-dice-space, skl.prob.naive-definition, skl.prob.overlap-counting]
terms: [gls.prob.conditional-probability]
misconceptions:
  - mc.prob.ignore-condition
  - mc.prob.whole-space-denominator
  - mc.prob.at-least-one-as-specific
  - mc.prob.double-count-overlap
edgeCases:
  - case: The double (5, 5) satisfies "at least one 5" through both dice, yet it is one outcome.
    at: cross
  - case: >-
      $P(A \mid B)$ is undefined when $P(B) = 0$.
      You cannot condition on something impossible.
    at: summary
workedExample:
  at: ten
  naive: >-
    Read "at least one die is a 5" as "the first die is a 5" and answer $\tfrac{1}{6}$.
  decision: >-
    Decide which outcomes the news leaves.
    It leaves the whole cross of 11 cells, not one row of 6.
est: { minutes: 12 }
sources:
  - src: src.blitzstein-hwang-2019
    loc: ch. 2, sec. 2.2
    use: basis
  - src: src.stat110-2013
    loc: Lecture 4
    use: parallel-reading
  - src: src.zhou-2008
    loc: ch. 4, conditional probability and Bayes' formula
    use: further
art: ast.course-art.probability-tree
authorship:
  drafted: content-agent (session to be recorded)
  reviewed: []

screens:
  - id: title
    type: title
    prose: >-
      You roll two dice and learn something about the result.
      Some outcomes become impossible, so every chance has to be measured again on what is left.

  - id: shade
    type: problem
    difficulty: 1
    skills: [skl.prob.two-dice-space]
    tutor:
      focus: List the outcomes for a total of 8 as ordered pairs, before any news arrives.
      notes: Learners leave out the double (4, 4) or merge (2, 6) with (6, 2). Ask what the second die must show for each first die.
      reps: [picture, count]
    prose: >-
      Two fair dice give 36 outcomes, all equally likely.
      Each cell is one outcome: the row is the first die, the column is the second.
    question: Shade every outcome where the total is 8.
    caption: Tap a cell to shade it
    canvas:
      - id: grid
        type: outcome-grid
        v: 1
        label: Outcomes for two dice. Tap a cell to shade it.
        preset: two-dice
        task: shade
        liveCount: true
    answer: grid
    check:
      kind: set
      correct: { where: a + b == 8 }
    verify:
      space: { dice: [6, 6] }
      set: a + b == 8
      expect: 5
    diagnose:
      - match: { kind: set, missing: ['cell:4,4'], extra: none }
        mc: mc.prob.skip-doubles
        line: You missed (4, 4). A double is one outcome, and it counts.
        show: [{ highlight: ['grid/cell:4,4'] }]
      - match: { kind: set, extra: some }
        slip: true
        line: >-
          {{extra.0.label}} adds to {{extra.0.sum}}, not 8.
          {{#if extra.1}}Other shaded cells miss too.{{/if}}
    otherwise: You found {{hit.count}}. Try every first die from 1 to 6.
    reason: Five of the 36 outcomes add to 8.
    hints:
      nudge: If the first die shows 3, what must the second die show?
      point:
        text: Totals of 8 sit on one diagonal, and it starts in row 2.
        highlight: ['grid/cell:2,6']
      step: >-
        Go row by row. A first die of 2 needs a 6, and a 3 needs a 5.
        Carry on up to 6. Row 1 cannot reach 8.
    why:
      rep: picture
      yours: You shaded the five cells from (2, 6) down to (6, 2).
      shown: The five cells from (2, 6) down to (6, 2) add to 8.
      then: >-
        A first die of 1 cannot reach 8, so row 1 stays empty.
        That makes $P(\text{total is } 8) = \tfrac{5}{36}$.
    solution:
      line: The five cells from (2, 6) down to (6, 2) add to 8.

  - id: first5
    type: ladder
    constraint: The first die is known.
    difficulty: 1
    skills: [skl.prob.restrict-sample-space]
    tutor:
      focus: News removes outcomes, so the chance is measured again inside what is left.
      notes: Learners keep dividing by 36. Point at the lit row before any arithmetic.
      reps: [picture, count]
    prose: >-
      New roll. A friend peeks and tells you the first die shows 5.
      The cells marked in orange are the totals of 8 from the last screen.
    caption: 36 outcomes
    canvas:
      - id: grid
        from: shade/grid
        label: Outcomes for two dice. Totals of 8 are marked. Only row 5 is still possible.
        task: none
        mark: { where: a + b == 8 }
        condition: { where: a == 5, outline: row, caption: '6 outcomes left: the first die is 5' }
    enter: [{ widget: grid, recipe: shrink }]
    question: What is the chance the total is 8 now? Give a fraction or a decimal.
    input:
      id: p
      type: numeric-input
      v: 1
      label: Chance, as a fraction or decimal
      placeholder: For example 3/4
    check: { kind: numeric, value: 1/6, tol: { abs: 0.005 }, probability: true, forms: [fraction, decimal] }
    verify:
      space: { dice: [6, 6] }
      answer: P(a + b == 8, given=a == 5)
      diagnose:
        before: P(a + b == 8)
        all-36: count(a + b == 8 and a == 5) / size()
        not-8: P(a + b != 8, given=a == 5)
      simulate: true
    diagnose:
      - key: before
        match: { kind: value, value: 5/36, tol: { abs: 0.005 } }
        mc: mc.prob.ignore-condition
        line: That is the chance before the news. Only the 6 cells in row 5 are still possible.
        show: [{ widget: grid, recipe: peek, args: { ms: 1000 } }]
      - key: all-36
        match: { kind: value, value: 1/36, tol: { abs: 0.005 } }
        mc: mc.prob.whole-space-denominator
        line: That divides by all 36 outcomes. Only the 6 cells in row 5 are still possible.
        show: [{ widget: grid, recipe: peek, args: { ms: 1000 } }]
      - key: not-8
        match: { kind: value, value: 5/6, tol: { abs: 0.005 } }
        mc: mc.prob.complement-confusion
        line: That is the chance the total is not 8. Count the cells that do reach 8.
        show: [{ widget: grid, recipe: flash, args: { cells: ['cell:5,1', 'cell:5,2', 'cell:5,4', 'cell:5,5', 'cell:5,6'] } }]
    otherwise: Count the marked cells inside row 5, then divide by the cells in row 5.
    reason: One of the 6 cells left, (5, 3), adds to 8.
    hints:
      nudge: Which cells are still possible once you know the first die is 5?
      point:
        text: Only row 5 is still lit. How many cells does it have, and how many are marked?
        highlight: ['grid/row:5']
      step: Row 5 has 6 cells. One of them, (5, 3), adds to 8. Divide the marked cells by 6.
    why:
      rep: count
      yours: You counted inside row 5, the only row left once the first die is 5.
      shown: Only row 5 is still possible, because the first die is 5.
      then: >-
        One of its 6 cells, (5, 3), adds to 8.
        So the news moved the chance from $\tfrac{5}{36}$ to $\tfrac{1}{6}$.
    solution:
      line: Only (5, 3) adds to 8 in row 5, so the chance is $\tfrac{1}{6}$.

  - id: cross
    type: ladder
    constraint: The news no longer names a die.
    difficulty: 2
    skills: [skl.prob.restrict-sample-space, skl.prob.overlap-counting]
    tutor:
      focus: Count the outcomes with at least one 5, counting the shared corner once.
      notes: The common slip adds the row and the column and counts (5, 5) twice. Ask which cell is in both.
      reps: [picture, count]
    prose: Another roll. This time your friend only says that at least one die shows a 5.
    caption: 36 outcomes
    canvas:
      - id: grid
        from: shade/grid
        label: Outcomes for two dice. Row 5 and column 5 are still possible, forming a cross.
        task: none
        condition: { where: a == 5 or b == 5, outline: cross, caption: At least one die shows a 5 }
    enter: [{ widget: grid, recipe: shrink }]
    question: How many outcomes are left?
    input:
      id: n
      type: numeric-input
      v: 1
      label: Number of outcomes left
      unit: outcomes
      keypad: digits
    check: { kind: numeric, value: 11, integer: true, forms: [integer] }
    verify:
      space: { dice: [6, 6] }
      answer: count(a == 5 or b == 5)
      diagnose:
        twice: count(a == 5) + count(b == 5)
        minus-two: count(a == 5) + count(b == 5) - 2 * count(a == 5 and b == 5)
        one-row: count(a == 5)
        everything: size()
        ruled-out: count(not (a == 5 or b == 5))
    diagnose:
      - key: twice
        match: { kind: value, value: 12 }
        mc: mc.prob.double-count-overlap
        line: You counted the (5, 5) cell twice. Look at the corner.
        show:
          - { widget: grid, recipe: flash, args: { cells: ['cell:5,5'] } }
          - { widget: grid, recipe: badge, args: { cell: 'cell:5,5', text: '×2' } }
      - key: minus-two
        match: { kind: value, value: 10 }
        mc: mc.prob.over-subtract-overlap
        line: Row 5 and column 5 share only one cell, (5, 5). Take it away once, not twice.
        show:
          - { widget: grid, recipe: flash, args: { cells: ['cell:5,5'] } }
          - { widget: grid, recipe: badge, args: { cell: 'cell:5,5', text: '×2' } }
      - key: one-row
        match: { kind: value, value: 6 }
        mc: mc.prob.at-least-one-as-specific
        line: That is one row. The 5 can also be on the second die.
        show: [{ widget: grid, recipe: flash, args: { cells: ['cell:1,5', 'cell:2,5', 'cell:3,5', 'cell:4,5', 'cell:6,5'] } }]
      - key: everything
        match: { kind: value, value: 36 }
        mc: mc.prob.ignore-condition
        line: That is every outcome. Rolls with no 5 are ruled out.
        show: [{ widget: grid, recipe: peek, args: { ms: 1000 } }]
      - key: ruled-out
        match: { kind: value, value: 25 }
        mc: mc.prob.complement-confusion
        line: That counts the outcomes with no 5. You want the ones that are left.
        show: [{ widget: grid, recipe: peek, args: { ms: 1000 } }]
    otherwise: Count the cells that are still lit, each one once.
    reason: Row 5 plus column 5, with the corner counted once.
    hints:
      nudge: How many cells are in row 5? How many are in column 5?
      point:
        text: One cell sits in both row 5 and column 5.
        highlight: ['grid/cell:5,5']
      step: Row 5 has 6 cells and column 5 has 6. The corner (5, 5) is in both, so count it once.
    why:
      rep: count
      yours: You counted row 5 and column 5, and the corner (5, 5) belongs to both.
      shown: Row 5 and column 5 both contain the corner (5, 5).
      then: >-
        Counting it once gives $6 + 6 - 1 = 11$.
        The news shrank the sample space from 36 outcomes to 11.
    solution:
      line: 'Count the corner once: $6 + 6 - 1 = 11$ outcomes.'

  - id: ten
    type: trap
    trap: { mc: mc.prob.at-least-one-as-specific, bait: a }
    difficulty: 2
    skills: [skl.prob.conditional-by-counting]
    tutor:
      focus: The trap. At least one die showing a 5 is weaker news than the first die showing a 5.
      notes: A learner who fixed one die should list every cell the news allows, then look for totals of 10.
      reps: [picture, count]
      avoid: [calling the news the first die]
    prose: 'Same news as before: at least one die shows a 5. Now look for a total of 10.'
    caption: '11 outcomes left: at least one 5'
    canvas:
      - id: grid
        from: cross/grid
        label: Outcomes for two dice. Only the cross of row 5 and column 5 is still possible.
        start: conditioned
    question: What is the chance the total is 10?
    input:
      id: pick
      type: choice
      v: 1
      label: Answer options
      options:
        - id: a
          value: 1/6
          mc: mc.prob.at-least-one-as-specific
          line: >-
            That treats one die as fixed at 5.
            You only know at least one is a 5, so 11 cells are possible.
          show: [{ widget: grid, recipe: dim, args: { cells: ['cell:1,5', 'cell:2,5', 'cell:3,5', 'cell:4,5', 'cell:6,5'], ms: 1100 } }]
        - id: b
          value: 1/11
        - id: c
          value: 3/11
          mc: mc.prob.numerator-not-intersection
          line: >-
            You counted all three ways to make 10.
            Only (5, 5) is still possible; (4, 6) and (6, 4) have no 5.
          show: [{ widget: grid, recipe: mark, args: { where: a + b == 10 } }]
        - id: d
          value: 1/12
          mc: mc.prob.ignore-condition
          line: >-
            That is the chance of 10 before the news, 3 of 36.
            Two of those ways have no 5, so they are gone.
          show:
            - { widget: grid, recipe: mark, args: { where: a + b == 10 } }
            - { widget: grid, recipe: peek, args: { ms: 1100 } }
    check: { kind: choice, correct: b }
    verify:
      space: { dice: [6, 6] }
      answer: P(a + b == 10, given=a == 5 or b == 5)
      diagnose:
        a: P(a + b == 10, given=a == 5)
        c: count(a + b == 10) / count(a == 5 or b == 5)
        d: P(a + b == 10)
      simulate: true
    reason: Only (5, 5) adds to 10, out of 11 cells.
    after: [{ widget: grid, recipe: mark, args: { where: a + b == 10 } }]
    hints:
      nudge: Which pairs add to 10? Which of them contain a 5?
      point:
        text: Only one cell in the cross adds to 10.
        highlight: ['grid/cell:5,5']
      step: >-
        The pairs adding to 10 are (4, 6), (5, 5) and (6, 4).
        Only (5, 5) is in the cross, and the cross has 11 cells.
    why:
      rep: count
      yours: Your $\tfrac{1}{11}$ counts one cell, (5, 5), out of the 11 in the cross.
      shown: Only one cell in the cross, (5, 5), adds to 10, so the chance is $\tfrac{1}{11}$.
      then: >-
        The other ways to make 10, (4, 6) and (6, 4), contain no 5, so they dropped out.
        Before the news the chance was $\tfrac{3}{36} = \tfrac{1}{12}$.
    solution:
      line: 'Only (5, 5) adds to 10, out of 11 cells: $\tfrac{1}{11}$.'

  - id: derive
    type: derive
    difficulty: 3
    skills: [skl.prob.conditional-definition]
    tutor:
      focus: Turn the counting rule into the definition by dividing top and bottom by the same number.
      notes: If stuck, ask what can be done to a fraction without changing its value.
      reps: [algebra, count]
    prose: >-
      You counted the outcomes where both things happen, out of the outcomes still possible.
      That is a [conditional probability](gls.prob.conditional-probability):
      $P(A \mid B)$, the probability of $A$ given $B$.
    caption: Derivation
    canvas:
      - id: d
        type: derivation-steps
        v: 1
        label: Derivation with one missing line
        mode: fill
        lines:
          - { id: l1, tex: 'P(A \mid B) = \frac{|A \cap B|}{|B|}', why: What you counted }
          - { id: l2, tex: '= \frac{|A \cap B| / 36}{|B| / 36}', why: Divide top and bottom by 36, hidden: true }
          - { id: l3, tex: '= \frac{P(A \cap B)}{P(B)}', why: Each count over 36 is a probability }
        closing:
          text: 'With your numbers, $A$ is a total of 10 and $B$ is at least one 5:'
          tex: 'P(A \mid B) = \frac{1/36}{11/36} = \frac{1}{11}'
    question: Which line completes the derivation?
    input:
      id: pick
      type: choice
      v: 1
      label: Candidate lines
      columns: 1
      fills: 'd/line:l2'
      options:
        - id: a
          tex: '\dfrac{|A \cap B| / 36}{|B|}'
          mc: mc.prob.rescale-one-side
          line: Dividing only the top changes the value. Do the same to the bottom.
        - id: b
          tex: '\dfrac{|A| / 36}{|B| / 36}'
          mc: mc.prob.numerator-not-intersection
          line: The top must count outcomes in both A and B. Some outcomes in A lie outside B.
        - id: c
          tex: '\dfrac{|A \cap B| / 36}{|B| / 36}'
    check: { kind: choice, correct: c }
    verify:
      space: { dice: [6, 6] }
      let: { A: a + b == 10, B: a == 5 or b == 5 }
      answer: P(A, given=B)
      options:
        a: (count(A and B) / 36) / count(B)
        b: (count(A) / 36) / (count(B) / 36)
        c: (count(A and B) / 36) / (count(B) / 36)
      chain:
        lines: [l1, l2, l3]
        bind:
          'P(A \mid B)': P(A, given=B)
          '|A \cap B|': count(A and B)
          '|B|': count(B)
          'P(A \cap B)': P(A and B)
          'P(B)': P(B)
    reason: The same factor top and bottom keeps the value.
    after: [{ widget: d, recipe: show-closing }]
    hints:
      nudge: What can you do to the top and bottom of a fraction without changing its value?
      point:
        text: The missing line has to turn each count into a probability.
        highlight: ['d/line:l2']
      step: Divide both $|A \cap B|$ and $|B|$ by the same number, 36.
    why:
      rep: algebra
      yours: You divided both counts by 36, which leaves the fraction unchanged.
      shown: Dividing both counts by 36 leaves the fraction unchanged.
      then: >-
        Each count over 36 is a probability.
        The last line needs no counting, so it also works when outcomes are not equally likely.
    solution:
      line: Divide top and bottom by 36. The value stays the same.

  - id: simulate
    type: problem
    difficulty: 2
    skills: [skl.prob.restrict-sample-space]
    tutor:
      focus: Predict how many of 1,000 rolls pass the filter, then test the prediction by rolling.
      notes: Learners confuse the share of rolls the filter keeps with the share of kept rolls that total 10.
      reps: [simulation, count]
    prose: >-
      Time for an experiment. You will roll two dice many times and keep only the rolls with at least one 5.
      Predict first, then roll.
    question: Of 1,000 rolls, about how many survive the filter?
    layout: input-first
    input:
      id: est
      type: numeric-input
      v: 1
      label: Rolls that survive, out of 1,000
      unit: rolls
      keypad: digits
    canvas:
      - id: sim
        type: trial-simulator
        v: 1
        label: Two dice rolled many times, keeping rolls with at least one 5
        experiment: { kind: dice, dice: 2, filter: a == 5 or b == 5, event: a + b == 10 }
        batches: [10, 100, 1000]
        display: [last, counts, share, trace]
        exact: 1/11
        predictFirst: true
        seed: 4226
    check: { kind: numeric, value: 1000 * 11/36, range: [280, 330], integer: true, forms: [integer] }
    verify:
      space: { dice: [6, 6] }
      answer: 1000 * P(a == 5 or b == 5)
      diagnose:
        share-of-kept: 1000 * P(a + b == 10, given=a == 5 or b == 5)
        one-die: 1000 * P(a == 5)
        twice: 1000 * (count(a == 5) + count(b == 5)) / size()
        no-filter: 1000 * count(True) / size()
    diagnose:
      - key: share-of-kept
        match: { kind: value, value: 1000/11, tol: { abs: 1 } }
        mc: mc.prob.conditional-vs-condition-rate
        line: >-
          That uses $\tfrac{1}{11}$, the share of kept rolls with total 10.
          You want the share of all rolls that are kept.
      - key: one-die
        match: { kind: value, value: 1000/6, tol: { abs: 1 } }
        mc: mc.prob.at-least-one-as-specific
        line: That is the chance one particular die shows 5. Either die can show it.
      - key: twice
        match: { kind: value, value: 1000/3, tol: { abs: 1 } }
        mc: mc.prob.double-count-overlap
        line: 'That counts the (5, 5) roll twice: 12 in 36. The cross has 11 cells.'
      - key: no-filter
        match: { kind: value, value: 1000 }
        mc: mc.prob.ignore-condition
        line: Rolls with no 5 are thrown away, so fewer survive.
    otherwise: 'A roll survives when it lands in the cross: 11 of the 36 outcomes.'
    reason: About 11 in every 36 rolls contain a 5. Now roll to test it.
    hints:
      nudge: What fraction of the 36 outcomes has at least one 5?
      point:
        text: The filter keeps the same outcomes as the cross you counted earlier.
        highlight: ['sim/control:filter']
      step: 11 of the 36 outcomes survive, so expect about $1000 \times \tfrac{11}{36}$ rolls.
    why:
      rep: simulation
      yours: You estimated {{answer.value}}.
      then: >-
        11 of the 36 outcomes contain a 5, so about $\tfrac{11}{36}$ of rolls survive, $1000 \times \tfrac{11}{36} \approx 305.6$.
        {{#if sim.rolled}}Your {{sim.rolled}} rolls kept {{sim.kept}}.{{else}}Roll 1,000 to see how close the experiment comes.{{/if}}
    solution:
      line: Expect about $1000 \times \tfrac{11}{36} \approx 306$ rolls.

  - id: stocks
    type: problem
    context: quant
    difficulty: 3
    skills: [skl.prob.conditional-by-counting]
    tutor:
      focus: Transfer to two stocks. Learning that at least one rose leaves more outcomes than learning which one rose.
      notes: The usual slip assumes we know which stock rose. Quiz item 3 names the stock, so contrast the two.
      reps: [count, picture]
    prose: >-
      Two stocks, A and B, each finish the day up or down with equal chance, independently.
      After the close you hear one fact: at least one of them finished up.
    caption: Four equally likely outcomes
    canvas:
      - id: grid
        type: outcome-grid
        v: 1
        label: Four outcomes, each with chance one quarter
        rows: { label: A, values: [up, down] }
        cols: { label: B, values: [up, down] }
        cellText: { 'up,up': Both up, 'up,down': Only A up, 'down,up': Only B up, 'down,down': Both down }
        display: probability
        task: none
    question: What is the chance both finished up? Give a fraction or a decimal.
    input:
      id: p
      type: numeric-input
      v: 1
      label: Chance, as a fraction or decimal
      placeholder: For example 3/4
    check: { kind: numeric, value: 1/3, tol: { abs: 0.005 }, probability: true, forms: [fraction, decimal] }
    verify:
      space: { product: [[up, down], [up, down]] }
      answer: P(a == 'up' and b == 'up', given=a == 'up' or b == 'up')
      diagnose:
        before: P(a == 'up' and b == 'up')
        named: P(a == 'up' and b == 'up', given=a == 'up')
        exactly-one: P(a != b, given=a == 'up' or b == 'up')
      simulate: true
    diagnose:
      - key: before
        match: { kind: value, value: 1/4, tol: { abs: 0.005 } }
        mc: mc.prob.ignore-condition
        line: That is the chance before the news. Both down is now ruled out.
        show: [{ widget: grid, recipe: dim, args: { cells: ['cell:down,down'], ms: 1400 } }]
      - key: named
        match: { kind: value, value: 1/2, tol: { abs: 0.005 } }
        mc: mc.prob.at-least-one-as-specific
        line: That assumes you know which stock rose. You only know at least one did, so three outcomes remain.
        show:
          - { widget: grid, recipe: dim, args: { cells: ['cell:down,down'], ms: 1400 } }
          - { widget: grid, recipe: flash, args: { cells: ['cell:up,down', 'cell:down,up'] } }
      - key: exactly-one
        match: { kind: value, value: 2/3, tol: { abs: 0.005 } }
        mc: mc.prob.wrong-event
        line: That is the chance exactly one stock rose. Both up is one of the three outcomes left.
        show:
          - { widget: grid, recipe: dim, args: { cells: ['cell:down,down'], ms: 1400 } }
          - { widget: grid, recipe: flash, args: { cells: ['cell:up,down', 'cell:down,up'] } }
    otherwise: Rule out what the news makes impossible, then count the outcomes left.
    reason: Both up is one of three equal outcomes left.
    after: [{ widget: grid, recipe: condition, args: { where: a == 'up' or b == 'up' } }]
    hints:
      nudge: Which of the four outcomes does the news rule out?
      point:
        text: One of the four outcomes is impossible once you know at least one stock rose.
        highlight: ['grid/cell:down,down']
      step: Three outcomes remain, each equally likely. Count the ones where both are up.
    why:
      rep: count
      yours: You ruled out both down, which leaves three equal outcomes.
      shown: The news rules out both down, which leaves three equal outcomes.
      then: >-
        Only one of them has both up, so the chance is $\tfrac{1}{3}$, not $\tfrac{1}{2}$.
        Learning "at least one" leaves more possibilities than learning which one.
    solution:
      line: 'Both up is one of the three outcomes left: $\tfrac{1}{3}$.'

  - id: summary
    type: summary
    ideas:
      - News rules outcomes out. The outcomes still possible form the new sample space.
      - >-
        With equally likely outcomes, count inside what is left:
        $$P(A \mid B) = \frac{|A \cap B|}{|B|}$$
      - Divide top and bottom by the total, and the rule works for any outcomes, equally likely or not.
    card:
      id: crd.prob.conditional-probability
      title: Conditional probability
      tex: 'P(A \mid B) = \dfrac{P(A \cap B)}{P(B)}'
      conditions: 'Defined only when $P(B) > 0$: you cannot condition on something impossible.'
      derivedIn: derive
    trap: >-
      "At least one is a 5" is not "the first is a 5".
      Knowing the first die is a 5 leaves 6 outcomes; knowing at least one is a 5 leaves 11.

quiz:
  - id: itm.cond.total-seven-has-three
    rev: 1
    status: review
    title: A 3, given a total of 7
    use: [quiz, practice, review]
    difficulty: 2
    skills: [skl.prob.conditional-by-counting]
    est: 60
    prompt: Two fair dice are rolled. You are told the total is 7.
    question: What is the chance that one of the dice shows a 3?
    input:
      id: pick
      type: choice
      v: 1
      label: Answer options
      options:
        - id: a
          value: 1/6
          mc: mc.prob.at-least-one-as-specific
          line: That counts only (3, 4). The 3 can be on either die, so (4, 3) counts too.
        - id: b
          value: 2/11
          mc: mc.prob.transposed-conditional
          line: That is the chance of a total of 7 given a 3 is showing. The condition runs the other way here.
        - id: c
          value: 1/3
        - id: d
          value: 1/18
          mc: mc.prob.whole-space-denominator
          line: That divides by all 36 outcomes. A total of 7 leaves only 6.
    check: { kind: choice, correct: c }
    verify:
      space: { dice: [6, 6] }
      answer: P(a == 3 or b == 3, given=a + b == 7)
      diagnose:
        a: P(a == 3, given=a + b == 7)
        b: P(a + b == 7, given=a == 3 or b == 3)
        d: count((a == 3 or b == 3) and a + b == 7) / size()
      simulate: true
    reason: (3, 4) and (4, 3), out of 6 ways to make 7.
    why:
      rep: count
      then: >-
        A total of 7 leaves six outcomes, from (1, 6) to (6, 1).
        Two of them, (3, 4) and (4, 3), contain a 3.
        So the chance is $\tfrac{2}{6} = \tfrac{1}{3}$.
    solution:
      line: '(3, 4) and (4, 3) out of 6 outcomes: $\tfrac{1}{3}$.'

  - id: itm.cond.even-above-three
    rev: 1
    status: review
    title: Above 3, given even
    use: [quiz, practice, review]
    difficulty: 2
    skills: [skl.prob.restrict-sample-space]
    est: 60
    prompt: A fair six-sided die is rolled. You learn the result is even.
    question: What is the chance it is greater than 3? Give a fraction or a decimal.
    input:
      id: p
      type: numeric-input
      v: 1
      label: Chance, as a fraction or decimal
      placeholder: For example 3/4
    check: { kind: numeric, value: 2/3, tol: { abs: 0.005 }, probability: true, forms: [fraction, decimal] }
    verify:
      space: { dice: [6] }
      answer: P(a > 3, given=a % 2 == 0)
      diagnose:
        before: P(a > 3)
        one-of-three: (count(a > 3 and a % 2 == 0) - 1) / count(a % 2 == 0)
      simulate: true
    diagnose:
      - key: before
        match: { kind: value, value: 1/2, tol: { abs: 0.005 } }
        mc: mc.prob.ignore-condition
        line: That is the chance before you learned it was even. Only 2, 4 and 6 are left.
      - key: one-of-three
        match: { kind: value, value: 1/3, tol: { abs: 0.005 } }
        slip: true
        line: Of 2, 4 and 6, two are greater than 3, not one.
    otherwise: Only 2, 4 and 6 are left. Count the ones above 3.
    reason: 4 and 6, out of 2, 4 and 6.
    why:
      rep: count
      then: >-
        Learning the result is even leaves 2, 4 and 6.
        Two of those, 4 and 6, are greater than 3.
        So the chance is $\tfrac{2}{3}$.
    solution:
      line: '4 and 6 out of 2, 4 and 6: $\tfrac{2}{3}$.'

  - id: itm.cond.one-stock-known-up
    rev: 1
    status: review
    title: Both up, given A rose
    use: [quiz, practice, review]
    difficulty: 3
    skills: [skl.prob.conditional-by-counting]
    est: 75
    prompt: >-
      Stocks A and B each finish up or down with equal chance, independently.
      This time you learn that A finished up.
    question: What is the chance both finished up?
    input:
      id: pick
      type: choice
      v: 1
      label: Answer options
      options:
        - id: a
          value: 1/3
          mc: mc.prob.specific-as-at-least-one
          line: That answers "at least one rose". Here you know A rose, so only B is uncertain.
        - id: b
          value: 1/4
          mc: mc.prob.ignore-condition
          line: That is the chance before any news. Knowing A rose leaves two outcomes.
        - id: c
          value: 1/2
        - id: d
          value: 3/4
          mc: mc.prob.wrong-event
          line: That is the chance at least one stock rises. You already know A did.
    check: { kind: choice, correct: c }
    verify:
      space: { product: [[up, down], [up, down]] }
      answer: P(a == 'up' and b == 'up', given=a == 'up')
      diagnose:
        a: P(a == 'up' and b == 'up', given=a == 'up' or b == 'up')
        b: P(a == 'up' and b == 'up')
        d: P(a == 'up' or b == 'up')
      simulate: true
    reason: Knowing A rose leaves two equal outcomes.
    why:
      rep: count
      then: >-
        Knowing A rose leaves two equal outcomes: both up, and only A up.
        B rose in one of them, so the chance is $\tfrac{1}{2}$.
        Compare the lesson, where "at least one rose" left three outcomes and gave $\tfrac{1}{3}$.
    solution:
      line: 'Both up and only A up remain; one of the two has both up: $\tfrac{1}{2}$.'

  - id: itm.cond.signal-fires
    rev: 1
    status: review
    title: A signal fires
    use: [quiz, practice, review]
    difficulty: 3
    skills: [skl.prob.conditional-definition]
    est: 75
    prompt: >-
      A trading signal fires on 30% of days.
      On 12% of days it fires and the stock also rises.
    question: On a day the signal fires, what is the chance the stock rises? Give a decimal or a fraction.
    input:
      id: p
      type: numeric-input
      v: 1
      label: Chance, as a decimal or fraction
      placeholder: For example 0.25
    check: { kind: numeric, value: 2/5, tol: { abs: 0.005 }, probability: true, forms: [decimal, fraction, percent] }
    verify:
      let: { PAB: 12/100, PB: 30/100 }
      answer: PAB / PB
      diagnose:
        joint: PAB
        product: PAB * PB
    diagnose:
      - key: joint
        match: { kind: value, value: 3/25, tol: { abs: 0.005 } }
        mc: mc.prob.joint-as-conditional
        line: That is the chance it fires and rises on a random day. Here you already know it fired.
      - key: product
        match: { kind: value, value: 9/250, tol: { abs: 0.0005 } }
        slip: true
        line: Multiplying makes the chance smaller still. Conditioning divides by the chance of the news.
    otherwise: Divide the chance of both by the chance of the news.
    reason: 0.12 out of 0.30 is 0.4.
    why:
      rep: algebra
      then: >-
        Only the days when the signal fires are still possible, and they are 30% of all days.
        Fires-and-rises days are 12% of all days, so the chance is $\tfrac{0.12}{0.30} = 0.4$.
        No counting was needed, because the definition works with any probabilities.
    solution:
      line: '$P(\text{rise} \mid \text{fires}) = \tfrac{0.12}{0.30} = 0.4$.'
```

### 10.3 Library entries it uses

From `misconceptions.yaml`, `skills.yaml` and `glossary.yaml` of topic 1.5, and `content/sources.yaml`. Shown together here; in the repository they are four files. Revision 2 renames the skills as actions (`ASSESSMENT.md` 4.1, test 3), adds the `requires` and `encompasses` edges this lesson implies (each `encompasses` target lies in its skill's `requires` closure, which the prototype checked), one `exercises` citation, and a table of contents for Blitzstein and Hwang so the `loc` check of section 6.7 has something to check against. The chapter titles are [recalled].

```yaml
misconceptions:
  - id: mc.prob.ignore-condition
    name: Ignoring the condition
    belief: The news does not change the chance, so I use the probability I had before.
    correction: >-
      News rules outcomes out.
      Measure the event again inside the outcomes that are still possible.
    signs: ['gives P(A) when asked for P(A | B)', 'keeps all outcomes after a filter']
  - id: mc.prob.whole-space-denominator
    name: Dividing by the whole sample space
    belief: I count the outcomes in both events and divide by all the outcomes, as before.
    correction: After conditioning, the denominator is the size of the condition, not of the whole space.
    signs: ['gives |A ∩ B| / |S| when asked for P(A | B)']
  - id: mc.prob.at-least-one-as-specific
    name: Treating "at least one" as "this one"
    belief: Learning that at least one die shows a 5 is the same as learning that the first die shows a 5.
    correction: >-
      "At least one" leaves every outcome where either part qualifies.
      It is weaker news than naming which part, so more outcomes survive.
    signs: ['conditions on one named part instead of the union', 'boy or girl puzzle: answers 1/2 instead of 1/3']
  - id: mc.prob.specific-as-at-least-one
    name: Treating "this one" as "at least one"
    belief: Learning which part qualified is the same as learning that at least one did.
    correction: Naming the part is stronger news, so fewer outcomes survive.
    signs: ['answers 1/3 in the two-stock puzzle after being told A rose']
  - id: mc.prob.double-count-overlap
    name: Counting the overlap twice
    belief: The size of "A or B" is the size of A plus the size of B.
    correction: Outcomes in both are counted once, so subtract the overlap once.
    signs: ['|A| + |B| for |A ∪ B|']
  - id: mc.prob.over-subtract-overlap
    name: Subtracting the overlap twice
    belief: The overlap is counted in both sets, so I remove it from both.
    correction: The overlap was counted twice and should be counted once, so subtract it once.
    signs: ['|A| + |B| - 2|A ∩ B| for |A ∪ B|']
  - id: mc.prob.complement-confusion
    name: Answering the complement
    belief: (none stated by learners; it is a reading slip that shows up as a value)
    correction: Check which event the question asks about before counting.
    signs: ['gives 1 - p', 'counts the excluded outcomes']
  - id: mc.prob.numerator-not-intersection
    name: Counting all of A on top
    belief: The top of P(A | B) counts every outcome in A.
    correction: Only outcomes in both A and B can happen once B is known, so the top is |A ∩ B|.
    signs: ['|A| / |B| for P(A | B)']
  - id: mc.prob.rescale-one-side
    name: Rescaling one side of a fraction
    belief: Dividing the top of a fraction by a number turns a count into a probability without changing anything else.
    correction: A fraction keeps its value only when top and bottom are divided by the same number.
    signs: ['(|A ∩ B| / n) / |B|']
  - id: mc.prob.transposed-conditional
    name: Swapping the condition
    belief: The chance of A given B is the chance of B given A.
    correction: The condition decides the denominator. Swapping it changes the space you count in.
    signs: ['P(B | A) for P(A | B)', 'prosecutor fallacy']
  - id: mc.prob.wrong-event
    name: Measuring a different event
    belief: (a reading slip) I answered for a related event, not the one asked.
    correction: Name the event in words before counting it.
    signs: ['exactly one instead of both', 'at least one instead of both']
  - id: mc.prob.conditional-vs-condition-rate
    name: Confusing P(A | B) with P(B)
    belief: The share of filtered rolls with the event is the share of rolls that pass the filter.
    correction: P(B) is how often the filter passes; P(A | B) is how often A happens among those that pass.
    signs: ['uses P(A | B) to predict how many trials survive the filter']
  - id: mc.prob.joint-as-conditional
    name: Answering the joint probability
    belief: The chance that A and B both happen is the chance of A once B is known.
    correction: Knowing B shrinks the space to B, so divide the joint chance by P(B).
    signs: ['gives P(A ∩ B) for P(A | B)']
  - id: mc.prob.skip-doubles
    name: Leaving out doubles
    belief: A double such as (4, 4) is one roll counted once, so it does not need its own cell.
    correction: Every ordered pair is one outcome. (4, 4) is one cell and counts like any other.
    signs: ['finds 4 ways to total 8 instead of 5']

skills:
  - id: skl.prob.two-dice-space
    name: List the 36 outcomes of two dice as ordered pairs
    topic: top.probability
    description: List and count the outcomes of two dice as ordered pairs, so (2, 6) and (6, 2) are different outcomes.
  - id: skl.prob.naive-definition
    name: Find a probability by counting equally likely outcomes
    topic: top.probability
    description: Favourable over possible when outcomes are equally likely.
  - id: skl.prob.overlap-counting
    name: Count a union without counting the overlap twice
    topic: top.probability
    description: 'Count A or B as |A| + |B| - |A ∩ B|.'
  - id: skl.prob.restrict-sample-space
    name: Remove the outcomes that news rules out
    topic: top.probability
    description: Remove the outcomes the news rules out and count what is left.
    requires: [skl.prob.naive-definition]
  - id: skl.prob.conditional-by-counting
    name: Condition by counting outcomes
    topic: top.probability
    description: 'Compute P(A | B) as |A ∩ B| / |B| for equally likely outcomes.'
    requires: [skl.prob.restrict-sample-space]
    encompasses:
      - { id: skl.prob.restrict-sample-space, w: 1 }
      - { id: skl.prob.naive-definition, w: 1 }
  - id: skl.prob.conditional-definition
    name: Apply the definition of conditional probability
    topic: top.probability
    description: 'Use P(A | B) = P(A ∩ B) / P(B), and know it needs P(B) > 0.'
    requires: [skl.prob.conditional-by-counting]
    encompasses:
      - { id: skl.prob.conditional-by-counting, w: 0.5 }
    exercises:
      - { src: src.blitzstein-hwang-2019, loc: 'ch. 2, end-of-chapter exercises on conditional probability', use: problem-inspired }

terms:
  - id: gls.prob.conditional-probability
    term: conditional probability
    aliases: [probability given]
    short: The probability of $A$ once you know $B$ happened, written $P(A \mid B)$.
    notation: 'P(A \mid B)'
    introducedIn: 'lsn.cond.shrinking-sample-space#derive'

sources:
  - id: src.blitzstein-hwang-2019
    kind: textbook
    title: Introduction to Probability
    authors: [Joseph K. Blitzstein, Jessica Hwang]
    year: 2019
    edition: 2nd
    publisher: CRC Press
    licence: copyright
    free: true
    toc: { '1': Probability and counting, '2': Conditional probability, '3': Random variables and their distributions, '4': Expectation }
  - id: src.stat110-2013
    kind: lecture-series
    title: Statistics 110, Probability (Harvard)
    authors: [Joseph K. Blitzstein]
    year: 2013
    licence: other
    free: true
  - id: src.zhou-2008
    kind: textbook
    title: A Practical Guide to Quantitative Finance Interviews
    authors: [Xinfeng Zhou]
    year: 2008
    licence: copyright
    free: false
```

### 10.4 How to read it

- **Ladders by reference.** `first5`, `cross` and `ten` start from an earlier screen's grid with `from:` and state only what changed: the condition, the marks, the label. The first draft of this file forgot to restate `label` on those three screens, so the grid kept the `shade` screen's accessible name, "Tap a cell to shade it", on screens where nothing can be tapped. That is now a warning: a widget taken `from:` another screen whose `task` changes must restate its `label`.
- **Two styles of feedback.** `ten` keeps choice options, so each option carries `mc`, `line` and `show` beside it. `cross` and `first5` take typed numbers, so their feedback is a `diagnose` list with value matchers. The compiler turns both into the same structure (section 10.5).
- **Templates.** `shade` names the learner's own wrong cell (`{{extra.0.label}} adds to {{extra.0.sum}}`), and `simulate` quotes the learner's estimate and roll counts. Every path is declared by the widget or the matcher.
- **Verify blocks.** Each graded screen states its answer a second way. `answer:` must equal the declared check value; `diagnose:` computes what each misconception produces, which must equal the value its option or matcher claims; `chain:` proves the derivation; `simulate:` re-estimates by Monte Carlo. Quiz item 4 has no sample space, so it binds values with `let`.
- **Element ids.** Hints and declarative steps name `grid/cell:4,4`, `grid/row:5`, `d/line:l2` and `sim/control:filter`; recipe arguments and the set matcher on `shade` use bare ids (`cell:4,4`), because the widget is already named. The `stocks` grid labels its rows and columns `up` and `down`, so its cells are `cell:up,down` and so on, and its `cellText` keys use the same names.
- **Tutor blocks.** Each of the seven task screens has `tutor.focus`, which becomes Bertie's outline title, `tutor.notes` on where learners stall, and `tutor.reps`. Every Why names its `rep`, mostly `count`, with `picture` on `shade`, `algebra` on `derive` and quiz item 4, and `simulation` on `simulate`; Bertie's "differently" then reaches for another. None of the notes states an answer: the leak lint (section 3.10) grades every number in them. `ten` adds `tutor.avoid`, because calling the news "the first die" is exactly the trap.
- **What a reviewer still reads.** That "at least one die shows a 5" means `a == 5 or b == 5`; that each line describes its misconception well; that the trap is tempting. Section 6.13 lists these.

### 10.5 What the compiler emits for one screen

The `ten` screen in the course bundle: copy as token lists, the inherited grid merged and its condition resolved to cells, option feedback lifted into `diagnose`, the accepted rule generated, `verify` stripped, the tutor block kept for the tutor context, the answer hash attached. The hash is the one revision 1 emitted: revision 2 changed copy-adjacent fields (tutor text, element id spellings, `why.rep`) and nothing that decides correct against not yet (section 4.2).

```json
{
  "id": "ten",
  "type": "trap",
  "trap": {"mc": "mc.prob.at-least-one-as-specific", "bait": "a"},
  "difficulty": 2,
  "skills": ["skl.prob.conditional-by-counting"],
  "tutor": {
    "focus": "The trap. At least one die showing a 5 is weaker news than the first die showing a 5.",
    "notes": "A learner who fixed one die should list every cell the news allows, then look for totals of 10.",
    "reps": ["picture", "count"],
    "avoid": ["calling the news the first die"]
  },
  "prose": [["t", "Same news as before: at least one die shows a 5. Now look for a total of 10."]],
  "caption": "11 outcomes left: at least one 5",
  "canvas": [
    {
      "id": "grid",
      "type": "outcome-grid",
      "v": 1,
      "label": "Outcomes for two dice. Only the cross of row 5 and column 5 is still possible.",
      "preset": "two-dice",
      "task": "none",
      "condition": {
        "where": "a == 5 or b == 5",
        "outline": "cross",
        "caption": "At least one die shows a 5",
        "cells": ["cell:1,5", "cell:2,5", "cell:3,5", "cell:4,5", "cell:5,1", "cell:5,2", "cell:5,3", "cell:5,4", "cell:5,5", "cell:5,6", "cell:6,5"]
      },
      "start": "conditioned"
    }
  ],
  "question": [["t", "What is the chance the total is 10?"]],
  "input": {
    "id": "pick",
    "type": "choice",
    "v": 1,
    "label": "Answer options",
    "options": [
      {"id": "a", "value": "1/6", "tex": "\\dfrac{1}{6}"},
      {"id": "b", "value": "1/11", "tex": "\\dfrac{1}{11}"},
      {"id": "c", "value": "3/11", "tex": "\\dfrac{3}{11}"},
      {"id": "d", "value": "1/12", "tex": "\\dfrac{1}{12}"}
    ]
  },
  "check": {"kind": "choice", "correct": "b"},
  "reason": [["t", "Only (5, 5) adds to 10, out of 11 cells."]],
  "after": [
    {
      "widget": "grid",
      "recipe": "mark",
      "args": {"where": "a + b == 10", "cells": ["cell:4,6", "cell:5,5", "cell:6,4"]}
    }
  ],
  "hints": {
    "nudge": [["t", "Which pairs add to 10? Which of them contain a 5?"]],
    "point": {"text": [["t", "Only one cell in the cross adds to 10."]], "highlight": ["grid/cell:5,5"]},
    "step": [
      ["t", "The pairs adding to 10 are (4, 6), (5, 5) and (6, 4). Only (5, 5) is in the cross, and the cross has 11 cells."]
    ]
  },
  "why": {
    "rep": "count",
    "yours": [["t", "Your "], ["m", "\\tfrac{1}{11}"], ["t", " counts one cell, (5, 5), out of the 11 in the cross."]],
    "shown": [["t", "Only one cell in the cross, (5, 5), adds to 10, so the chance is "], ["m", "\\tfrac{1}{11}"], ["t", "."]],
    "then": [
      ["t", "The other ways to make 10, (4, 6) and (6, 4), contain no 5, so they dropped out. Before the news the chance was "],
      ["m", "\\tfrac{3}{36} = \\tfrac{1}{12}"],
      ["t", "."]
    ]
  },
  "solution": {"line": [["t", "Only (5, 5) adds to 10, out of 11 cells: "], ["m", "\\tfrac{1}{11}"], ["t", "."]]},
  "diagnose": [
    {
      "key": "a",
      "match": {"kind": "option", "ids": ["a"]},
      "mc": "mc.prob.at-least-one-as-specific",
      "line": [["t", "That treats one die as fixed at 5. You only know at least one is a 5, so 11 cells are possible."]],
      "show": [
        {
          "widget": "grid",
          "recipe": "dim",
          "args": {"cells": ["cell:1,5", "cell:2,5", "cell:3,5", "cell:4,5", "cell:6,5"], "ms": 1100}
        }
      ]
    },
    {
      "key": "c",
      "match": {"kind": "option", "ids": ["c"]},
      "mc": "mc.prob.numerator-not-intersection",
      "line": [["t", "You counted all three ways to make 10. Only (5, 5) is still possible; (4, 6) and (6, 4) have no 5."]],
      "show": [
        {
          "widget": "grid",
          "recipe": "mark",
          "args": {"where": "a + b == 10", "cells": ["cell:4,6", "cell:5,5", "cell:6,4"]}
        }
      ]
    },
    {
      "key": "d",
      "match": {"kind": "option", "ids": ["d"]},
      "mc": "mc.prob.ignore-condition",
      "line": [["t", "That is the chance of 10 before the news, 3 of 36. Two of those ways have no 5, so they are gone."]],
      "show": [
        {
          "widget": "grid",
          "recipe": "mark",
          "args": {"where": "a + b == 10", "cells": ["cell:4,6", "cell:5,5", "cell:6,4"]}
        },
        {"widget": "grid", "recipe": "peek", "args": {"ms": 1100}}
      ]
    }
  ],
  "accepted": [["t", "Accepted: "], ["m", "\\tfrac{1}{11}"], ["t", " only."]],
  "answerHash": "sha256:6f77a0cc2f9c6f1a"
}
```

### 10.6 What verification found in the prototype lesson

1. **Two options with the same value.** On `sTen` the prototype offered $\tfrac{1}{12}$ (labelled "counted the corner twice") and $\tfrac{3}{36}$ (labelled "ignored the condition"). They are the same number. A learner who ignored the condition and simplified would pick $\tfrac{1}{12}$ and be told they double-counted. With the prototype's options re-expressed, the verifier reports `options c and d have the same value 1/12` [measured]. Writing down what each misconception computes also showed that "counting the corner twice" gives $\tfrac{2}{12} = \tfrac{1}{6}$ when the corner is also the event, so the label was doubtful too. The new options are $\tfrac{1}{6}$, $\tfrac{1}{11}$, $\tfrac{3}{11}$ and $\tfrac{1}{12}$, each a distinct, verified misconception.
2. **Too much multiple choice.** Four of the prototype's seven lesson problems were multiple choice (57%), against the limit of 40% in design research section 10 (the "retry-until-green" critique). `first5` and `stocks` now take a typed fraction; with the quiz, 4 of 11 graded items are choice (36%).
3. **An introduced skill the quiz never tested.** The lesson derives $P(A \mid B) = \tfrac{P(A \cap B)}{P(B)}$ and says it works when outcomes are not equally likely, but every quiz item could be solved by counting. Quiz item 4 (a trading signal, given as percentages) now needs the definition itself.
4. **An ambiguous trap line.** "The first leaves 6 outcomes; the second leaves 11" can be read either way round. No check found this; review did. It now names both cases.

The final file passes every check [measured]:

```text
zq check    9 screens, 4 quiz items, 50 formulas, 36 element references: 0 errors, 0 warnings
zqverify    shade: set ['cell:2,6', 'cell:3,5', 'cell:4,4', 'cell:5,3', 'cell:6,2'] (author expects 5)
            first5: exact 1/6, simulated 0.16658 over 167,431 kept trials, 0.10 SE
            ten: exact 1/11, simulated 0.09113 over 306,094 kept trials, 0.42 SE
            stocks: exact 1/3, simulated 0.33283 over 749,123 kept trials, 0.93 SE
            itm.cond.total-seven-has-three: exact 1/3, simulated 0.33182, 1.31 SE
            itm.cond.even-above-three: exact 2/3, simulated 0.66679, 0.18 SE
            itm.cond.one-stock-known-up: exact 1/2, simulated 0.49942, 0.82 SE
            derive: derivation chain of 3 lines holds on the instance (value 1/11)
            7 arithmetic claims in the copy hold
            every misconception value matches its option or matcher
            failures: 0
```

### 10.7 Size

| | Prototype | This format |
|---|---|---|
| Lesson content | 562 lines, 37 KB of JavaScript (`sTitle` to `qOneStock`) | 793 lines, 32 KB of YAML, of which about 90 lines are `verify` blocks, about 210 lines are copy and about 40 lines are tutor fields |
| Machinery | About 750 more lines in the same file (grid, choice and numeric widgets, the player) | None: shared widgets and the shared player |
| Quiz | 3 items | 4 items |
| Compiled | | About 27 KB JSON, 7.2 KB gzipped |
| Proof of correctness | Review | Section 10.6 output |

The YAML is longer in lines than the prototype's screen code because it says more: verify blocks, misconception ids, sources, tutor guidance, a fourth quiz item, and one fact per line. It is shorter in bytes and contains no logic, and the machinery where the prototype's 23 review defects lived is written once, for every lesson.

---

## 11. Worked example: a generator and its Python verifier

`gen.prob.two-dice-conditional` produces practice, review, homework and exam variants of the lesson's core skill: two fair dice with 4 to 8 faces, one of four kinds of news, one of four kinds of event. Generated items have no canvas, because practice removes scaffolding (design research 5.5); the Why? sheet carries the explanation.

### 11.1 The spec

`content/generators/prob/two-dice-conditional.gen.yaml`:

```yaml
zq: 1
id: gen.prob.two-dice-conditional
v: 1
status: review
title: Conditional probability on two dice
desc: Chance of an event on two dice after news about the roll; four kinds of news, four kinds of event.
skills: [skl.prob.restrict-sample-space, skl.prob.conditional-by-counting]
use: [practice, review, homework, exam]
semantics: >-
  Two fair dice, each with `faces` faces numbered 1 to faces, are rolled.
  a is the first die and b the second; all faces^2 ordered pairs are equally likely.
  The learner is told that the condition `cond` holds, with parameter k, and is asked for the
  probability that the event `event` holds, with parameter m, given the condition.
  first-is: a = k. at-least-one: a = k or b = k. total-at-least: a + b >= k. no-value: a != k and b != k.
  total-is: a + b = m. double: a = b (m is 0). has-value: a = m or b = m. max-is: max(a, b) = m.
  Wrong values closer than 0.01 to the answer, or to a wrong value kept earlier in the priority order, are dropped.
box:
  faces: { int: [4, 8] }
  cond: { enum: [first-is, at-least-one, total-at-least, no-value] }
  k: { int: [1, 16] }
  event: { enum: [total-is, double, has-value, max-is] }
  m: { int: [0, 16] }
admissible: >-
  The parameters are in range for their kind (k at most faces except total-at-least, where 3 <= k <= 2 faces;
  m is 0 for double, 2 to 2 faces for total-is, 1 to faces otherwise); the condition has at least one outcome;
  the answer is strictly between 0 and 1; the news changes the chance; at least two misconception values
  survive deduplication.
levels:
  1: six-sided dice, the first die named, a total asked for
  2: six-sided dice, a named die or "at least one"
  3: six-sided dice, any condition
  4: other dice, no total threshold
  5: other dice, any condition
tutorParams: [faces, cond, event]
misconceptions:
  - mc.prob.ignore-condition
  - mc.prob.whole-space-denominator
  - mc.prob.transposed-conditional
  - mc.prob.numerator-not-intersection
  - mc.prob.at-least-one-as-specific
phrases:
  dice: { '6': Two fair dice are rolled., other: 'Two fair {faces}-sided dice are rolled, numbered 1 to {faces}.' }
  cond:
    first-is: the first die shows {k}
    at-least-one: at least one die shows {k}
    total-at-least: the total is at least {k}
    no-value: neither die shows {k}
  event:
    total-is: the total is {m}
    double: both dice show the same number
    has-value: at least one die shows {m}
    max-is: the higher die shows {m}
golden: two-dice-conditional.golden.json
```

### 11.2 The TypeScript generator

`content/generators/prob/two-dice-conditional.gen.ts`. It runs at build time to decide admissibility and levels, and on the device to build the item for a chosen parameter point. The executed copy imported a local stand-in for `@zq/gen` and read the YAML from disk; those two import lines are shown as the real build writes them.

```ts
// content/generators/prob/two-dice-conditional.gen.ts
// Pure: no DOM, no clock, no Math.random. Exact rationals only. The box, phrases and levels live in the .gen.yaml beside it.
import { defineGenerator, R, eq, str, tex, fill, type Rat } from '@zq/gen';
import spec from './two-dice-conditional.gen.yaml';             // the build plugin validates it against GeneratorSpec

type Cond = 'first-is' | 'at-least-one' | 'total-at-least' | 'no-value';
type Event = 'total-is' | 'double' | 'has-value' | 'max-is';
export type P = { faces: number; cond: Cond; k: number; event: Event; m: number };

const news = (p: P, a: number, b: number): boolean =>
  p.cond === 'first-is' ? a === p.k
  : p.cond === 'at-least-one' ? a === p.k || b === p.k
  : p.cond === 'total-at-least' ? a + b >= p.k
  : a !== p.k && b !== p.k;
const event = (p: P, a: number, b: number): boolean =>
  p.event === 'total-is' ? a + b === p.m
  : p.event === 'double' ? a === b
  : p.event === 'has-value' ? a === p.m || b === p.m
  : Math.max(a, b) === p.m;

// One pass over the F x F grid counts everything the item needs.
function tally(p: P) {
  let nC = 0, nE = 0, nEC = 0, nFirst = 0, nEFirst = 0;
  for (let a = 1; a <= p.faces; a++) for (let b = 1; b <= p.faces; b++) {
    const c = news(p, a, b), e = event(p, a, b);
    nC += +c; nE += +e; nEC += +(c && e);
    if (a === p.k) { nFirst++; nEFirst += +e; }
  }
  return { n: p.faces * p.faces, nC, nE, nEC, nFirst, nEFirst };
}

const inRange = (p: P) =>
  (p.cond === 'total-at-least' ? p.k >= 3 && p.k <= 2 * p.faces : p.k <= p.faces) &&
  (p.event === 'double' ? p.m === 0 : p.event === 'total-is' ? p.m >= 2 && p.m <= 2 * p.faces : p.m >= 1 && p.m <= p.faces);

// Wrong values in a fixed priority order. One within 0.01 of the answer or of a value already kept is dropped,
// so a typed decimal can never match two diagnoses, or a diagnosis and the answer (tolerances are 0.005).
function wrongValues(p: P): Array<[string, Rat]> {
  const t = tally(p);
  const out: Array<[string, Rat]> = [['mc.prob.ignore-condition', R(t.nE, t.n)], ['mc.prob.whole-space-denominator', R(t.nEC, t.n)]];
  if (t.nE > 0) out.push(['mc.prob.transposed-conditional', R(t.nEC, t.nE)]);
  if (t.nE <= t.nC) out.push(['mc.prob.numerator-not-intersection', R(t.nE, t.nC)]);
  if (p.cond === 'at-least-one') out.push(['mc.prob.at-least-one-as-specific', R(t.nEFirst, t.nFirst)]);
  const ans = R(t.nEC, t.nC), kept: Array<[string, Rat]> = [];
  const far = (x: Rat, y: Rat) => { const d = R(x.n * y.d - y.n * x.d, x.d * y.d); return (d.n < 0n ? -d.n : d.n) * 100n >= d.d; };
  for (const [id, v] of out) if (far(v, ans) && kept.every(([, w]) => far(v, w))) kept.push([id, v]);
  return kept;
}

const LINES: Record<string, string> = {
  'mc.prob.ignore-condition': 'That is the chance before the news. Only outcomes where {cond} are still possible.',
  'mc.prob.whole-space-denominator': 'That divides by all {n} outcomes. Only the {nC} where {cond} are still possible.',
  'mc.prob.transposed-conditional': 'That is the chance that {cond}, given that {event}. The condition runs the other way.',
  'mc.prob.numerator-not-intersection': 'You counted every outcome where {event}. Only those where {cond} as well still count.',
  'mc.prob.at-least-one-as-specific': 'That treats the first die as the one showing {k}. Either die can show it.',
};

export default defineGenerator<P>(spec, {
  accept(p) {
    if (!inRange(p)) return false;
    const t = tally(p);
    if (t.nC === 0 || t.nEC === 0 || t.nEC === t.nC) return false;     // news possible; answer strictly between 0 and 1
    if (eq(R(t.nEC, t.nC), R(t.nE, t.n))) return false;                 // the news must change the chance
    return wrongValues(p).length >= 2;
  },
  level(p) {
    const six = p.faces === 6;
    if (six && p.cond === 'first-is' && p.event === 'total-is') return 1;
    if (six && (p.cond === 'first-is' || p.cond === 'at-least-one')) return 2;
    if (six) return 3;
    return p.cond === 'total-at-least' ? 5 : 4;
  },
  answer(p) { const t = tally(p); return R(t.nEC, t.nC); },
  diagnoses(p) { return Object.fromEntries(wrongValues(p)); },
  build(p) {
    const t = tally(p), ans = R(t.nEC, t.nC);
    const v = { ...p, n: t.n, nC: t.nC, nEC: t.nEC };
    const cond = fill(spec.phrases.cond[p.cond], v), ev = fill(spec.phrases.event[p.event], v);
    const all = { ...v, cond, event: ev };
    const dice = p.faces === 6 ? spec.phrases.dice['6'] : fill(spec.phrases.dice.other, v);
    return {
      title: 'Two dice, given some news',
      prompt: `${dice} You learn that ${cond}.`,
      question: `What is the chance that ${ev}? Give a fraction or a decimal.`,
      input: { id: 'p', type: 'numeric-input', v: 1, label: 'Chance, as a fraction or decimal' },
      check: { kind: 'numeric', value: str(ans), tol: { abs: 0.005 }, probability: true, forms: ['fraction', 'decimal'] },
      diagnose: wrongValues(p).map(([mc, w]) => ({ match: { kind: 'value', value: str(w), tol: { abs: 0.005 } }, mc, line: fill(LINES[mc], all) })),
      otherwise: `Keep the outcomes where ${cond}. Then count those where ${ev}.`,
      reason: `${t.nEC} of the ${t.nC} outcomes left.`,
      why: { rep: 'count', then: `The news leaves ${t.nC} of the ${t.n} outcomes. In ${t.nEC} of them ${ev}. So the chance is $${tex(R(t.nEC, t.nC))}$.` },
      solution: { line: t.nEC === Number(ans.n) ? `$\\tfrac{${t.nEC}}{${t.nC}}$.` : `$\\tfrac{${t.nEC}}{${t.nC}} = ${tex(ans)}$.` },
      difficulty: this.level(p), skills: spec.skills, est: 90,
    };
  },
});
```

### 11.3 The Python verifier

`content/generators/prob/two-dice-conditional.verify.py`, written from the spec's `semantics` without the TypeScript. Sets of outcomes and intersections rather than counting loops, so a shared slip is unlikely:

```python
# content/generators/prob/two-dice-conditional.verify.py
# Written from the .gen.yaml `semantics` text, without reading the TypeScript. Sets, not loops; Fractions, not floats.
from fractions import Fraction
from itertools import product


class TwoDiceConditional:
    id = 'gen.prob.two-dice-conditional'

    def space(self, p):
        return set(product(range(1, p['faces'] + 1), repeat=2))

    def condition(self, p):
        k = p['k']
        rule = {'first-is': lambda a, b: a == k, 'at-least-one': lambda a, b: k in (a, b),
                'total-at-least': lambda a, b: a + b >= k, 'no-value': lambda a, b: k not in (a, b)}[p['cond']]
        return {o for o in self.space(p) if rule(*o)}

    def event(self, p):
        m = p['m']
        rule = {'total-is': lambda a, b: a + b == m, 'double': lambda a, b: a == b,
                'has-value': lambda a, b: m in (a, b), 'max-is': lambda a, b: max(a, b) == m}[p['event']]
        return {o for o in self.space(p) if rule(*o)}

    def in_range(self, p):
        F, k, m = p['faces'], p['k'], p['m']
        k_ok = 3 <= k <= 2 * F if p['cond'] == 'total-at-least' else 1 <= k <= F
        m_ok = {'double': m == 0, 'total-is': 2 <= m <= 2 * F}.get(p['event'], 1 <= m <= F)
        return k_ok and m_ok

    def answer(self, p):
        C, E = self.condition(p), self.event(p)
        return Fraction(len(E & C), len(C))

    def diagnoses(self, p):
        S, C, E = self.space(p), self.condition(p), self.event(p)
        cands = [('mc.prob.ignore-condition', Fraction(len(E), len(S))),
                 ('mc.prob.whole-space-denominator', Fraction(len(E & C), len(S)))]
        if E:
            cands.append(('mc.prob.transposed-conditional', Fraction(len(E & C), len(E))))
        if len(E) <= len(C):
            cands.append(('mc.prob.numerator-not-intersection', Fraction(len(E), len(C))))
        if p['cond'] == 'at-least-one':
            first = {o for o in S if o[0] == p['k']}
            cands.append(('mc.prob.at-least-one-as-specific', Fraction(len(E & first), len(first))))
        ans, out = self.answer(p), {}
        for mc, v in cands:
            if abs(v - ans) >= Fraction(1, 100) and all(abs(v - w) >= Fraction(1, 100) for w in out.values()):
                out[mc] = v
        return out

    def accept(self, p):
        if not self.in_range(p):
            return False
        S, C, E = self.space(p), self.condition(p), self.event(p)
        if not C or not (E & C) or (E & C) == C:
            return False
        if Fraction(len(E & C), len(C)) == Fraction(len(E), len(S)):
            return False
        return len(self.diagnoses(p)) >= 2

    def level(self, p):
        six = p['faces'] == 6
        if six and p['cond'] == 'first-is' and p['event'] == 'total-is':
            return 1
        if six and p['cond'] in ('first-is', 'at-least-one'):
            return 2
        if six:
            return 3
        return 5 if p['cond'] == 'total-at-least' else 4

    def simulate(self, p, rng, trials=1_000_000):
        F = p['faces']
        a, b = rng.integers(1, F + 1, trials), rng.integers(1, F + 1, trials)
        k, m = p['k'], p['m']
        c = {'first-is': a == k, 'at-least-one': (a == k) | (b == k), 'total-at-least': a + b >= k,
             'no-value': (a != k) & (b != k)}[p['cond']]
        e = {'total-is': a + b == m, 'double': a == b, 'has-value': (a == m) | (b == m),
             'max-is': (a == m) & (b <= m) | (b == m) & (a <= m)}[p['event']]
        return (c & e).sum() / c.sum(), c.sum()
```

### 11.4 The golden file and the CI run

`two-dice-conditional.golden.json` holds the first 12 hex digits of the SHA-256 of the built item for seeds 1 to 3 at each level. The executed copy used a stand-in for the engine's `hash32`, so these values change once, when the real hash lands:

```json
{
 "1": [
  "6d16931f7d8d",
  "23097030a0e3",
  "3b30b6c222b5"
 ],
 "2": [
  "1ab745cd487b",
  "7f9df6c9aced",
  "30f105899eea"
 ],
 "3": [
  "aee986968f43",
  "4b4a683291ed",
  "e952e80edacf"
 ],
 "4": [
  "bffd1cd5714d",
  "f46ab03e29ef",
  "f6683fdd17e7"
 ],
 "5": [
  "09cfe78eee32",
  "d942d35bc8f0",
  "157c422350c0"
 ]
}
```

The CI run [measured]:

```text
box points 21,760   admissible 2,093   per level: 1: 30   2: 142   3: 235   4: 1,226   5: 460
TypeScript and Python: 0 disagreements on accept, level, answer and misconception values
built items: 2,093 schema-valid, 4,186 formulas rendered, longest sentence 19 words
Monte Carlo, 12 points per level, 10^6 trials each: worst deviation 2.75 standard errors
time: 1.2 s (Node) + 2.5 s (Python) on a 4-core container
mutation: '>=' changed to '>' in the total-at-least rule gives 864 disagreements
```

Two things the run taught the generator before it was finished, both now in the files above: sentences of up to 24 words failed the copy lint, so the longest phrase ("the larger of the two numbers is 6") and the fallback line were shortened; and diagnosis tolerances of 0.005 needed misconception values at least 0.01 apart, or a typed decimal could match two of them, so the separation rule went into both implementations and the spec's `semantics`.

**Revision 2 and the golden rule.** Adding `rep: 'count'` to the built item's Why changed every golden hash, which section 4.2 treats as "generator output changed for an existing seed". The rule binds published generators only: `ids.lock.json` holds no entry for this one, whose `status` is `review`, so `v` stays 1. Once a generator is live, the same edit needs `v: 2`, and learners' stored seeds keep rendering from their snapshots.

### 11.5 One built item

Level 2, seed 7:

```text
Two fair dice are rolled. You learn that at least one die shows 2.
What is the chance that the higher die shows 6? Give a fraction or a decimal.

Accepted: 2/11 in any equal fraction form, or a decimal within 0.005 of it (0.177 to 0.186).
11/36  ignore-condition            That is the chance before the news. Only outcomes where at least one die shows 2 are still possible.
1/18   whole-space-denominator     That divides by all 36 outcomes. Only the 11 where at least one die shows 2 are still possible.
1      numerator-not-intersection  You counted every outcome where the higher die shows 6. Only those where at least one die shows 2 as well still count.
1/6    at-least-one-as-specific    That treats the first die as the one showing 2. Either die can show it.
Why?   The news leaves 11 of the 36 outcomes. In 2 of them the higher die shows 6. So the chance is 2/11.
```

The transposed-conditional value ($P(\text{news} \mid \text{event}) = \tfrac{2}{11}$) equals the answer here, so the generator dropped it, as section 5.3 requires.

---

## 12. What this paper needs from the other papers

### 12.1 From the widget library

Each widget module exports, besides its runtime interface (Stage 0 section 1.1, calc-linalg section 2.2):

| Export | Used by | Notes |
|---|---|---|
| `configSchema` (zod) | Compile step | Validates the widget-specific fields of every `WidgetUse` at the pinned `v` |
| `answerTypes` | Compile step | Which `Check` kinds the widget can be graded by |
| `targets(config)` | Compile step | The static form of the runtime `targets()` that `AI-TUTOR.md` 0.2 fixed: every `kind:name` element id (with its label and role) that the config produces, computed without a DOM. Elements that exist only at runtime (a dragged point's trail) are out of reach of content references by design |
| `exports(config)` | Compile step, template renderer | Template paths the widget provides (`sim.rolled`, `sim.kept`) and, for set answers, the metadata per element (`label`, `sum`) |
| `recipes` | Compile step | Named show-why and enter recipes with their argument schemas |
| `resolve(config, expr)` | Compile step | Pure build-time resolver from a `where` expression to element ids (the outcome grid enumerates its cells) |

Additions to specific widgets that the worked example needs:

- `outcome-grid`: `preset: two-dice`; `mark` and `condition` with `where`; `start: conditioned`; `cellText` keyed by `row,col` names; element ids `cell:r,c`, `row:r`, `col:c`, with `r` and `c` the row and column values (`cell:5,3`, `cell:up,down`); recipes `dim`, `mark`, `badge` and `condition` beside the catalogue's `shrink`, `flash` and `peek`; set-answer metadata `label` and `sum`.
- `trial-simulator`: element ids `control:filter`, `control:event`, `control:roll`, `control:batch` (the hint points at the filter); exports `rolled` and `kept`.
- `choice`: element ids `option:<id>`; `fills: <element ref>`, which previews the chosen option in a `derivation-steps` slot.
- `derivation-steps`: element ids `line:<line id>`; a `closing` line revealed after Check, and the `show-closing` recipe.

### 12.2 From the engine

- A bundle loader that validates once per hash, keeps the current and next course, and applies migrations (section 4.5) before progress is read.
- Progress keyed by content id and `rev`, attempts with snapshots, mastery on skills (section 4.3).
- The renderer for token lists and templates (sections 2.4 and 3.6), with KaTeX at runtime and no other `innerHTML` sink.
- The `Grade` contract in section 7.1 and the matching order in section 7.8.
- The engine's counter hash exposed to `@zq/gen` as `hash32(id, seed)`, and `makeWhere(partial, seed)` for the tutor's practice picks (section 5.4).
- A runtime policy (decided: `ARCHITECTURE.md` 5.9 and 6.3; section 6.11 as tidied; `docs/PLAN.md` revision 2): Pyodide on the web app with packages per `needs`; in the Artifact every drill hands off by result code.

### 12.3 From the tutor paper

- Use of the stable lesson block and the per-call part (section 8.4), the embargo, and the sealed answer block with its check summary.
- The long-form marking contract (section 7.7), which follows `AI-TUTOR.md` 2.7. One spelling to align: the tutor paper writes the long-form check as `{ kind: 'text' | 'free-text', rubric, model, marking: 'tutor-draft' }`, from the catalogues; the schema's name is `long-form`, with the same `marking` values and a `genre` that carries the tutor paper's `MarkingCtx.item.kind`.
- The `#/tutor` preview hook (section 9.2), so authors see the exact request.

### 12.4 From the curriculum files and the assessment paper

- **Curriculum files:** rename one of the two `R` quiz letters (section 3.4); `stage1-python-tools.md`'s result table could become `Q`. Treat `web` drills that need only NumPy and pandas as `pyodide-core` candidates: CI will tag them, and the hand-off shrinks to SciPy, statsmodels, scikit-learn and matplotlib work.
- **Assessment paper:** confirm the two syntax changes to `ExitPart` (section 3.2).

---

## 13. Open questions and unverified items

| # | Item | Status and effect |
|---|---|---|
| 1 | Pyodide repackaged for the Artifact on the owner's iPhone | **Measured, not adopted** [measured by the owner, `spikes/README.md`]: Python ready at 2.8 s, NumPy and pandas at 5.1 s, correct result at 6.2 s; the owner's publishing rule (`docs/PLAN.md` revision 2) keeps Python out of the Artifact. Open: memory headroom of the web app on older phones, measured per group at `docs/PLAN.md` stage 25 |
| 2 | Whether the Artifact host compresses responses | **Closed**: it does, with gzip (6.4 KiB on the wire for 62.7 KiB of JSON) [measured: S1, 7 October 2026, `docs/DECISIONS.md` section 4]; course bundles, the only large Artifact files since revision 2, travel compressed |
| 3 | MathLive's size, and that it emits LaTeX without loading Compute Engine's core | [unverified]. If it needs the core, expression screens cost about 1.2 MB more and the preload rule in section 7.3 covers them |
| 4 | Compute Engine `latex-syntax` under the Artifact's script policy | No `new Function` in that entry [measured by search]; a run inside a published Artifact is still needed [unverified] |
| 5 | Citation locations in the worked example (Blitzstein and Hwang section 2.2; Stat 110 Lecture 4; Zhou chapter 4) | [recalled]; `checked: false` until confirmed against the books |
| 6 | Reading-level threshold | Grade 8 warning is a guess [our choice]; calibrate on the first 20 lessons |
| 7 | The licence of the en-GB Hunspell dictionary package | [unverified]; it is a development tool and never ships, so any open licence works |
| 8 | Copyright rule for adapted problems (section 9.4) | **Closed**: as written (`docs/PLAN.md` 12 decision 8, default taken on 7 October 2026); it remains a reading of the licences, not legal advice, and is reviewed before anything is public (decision 13) |
| 9 | Size of the expression conformance corpus | About 2,000 pairs [our choice]; grow it from real disagreements |
| 10 | Odds as a numeric form (prob-stats asks for "a:b" where a screen asks for odds) | Not in the schema yet; add `odds` to `NumForm` when the first odds screen is written |
| 11 | The glossary exemption for banned words (`robust standard errors`, `leverage`) | **Closed**: allowed (`docs/PLAN.md` 12 decision 8, default taken on 7 October 2026); section 6.10 applies it |
| 12 | The `R` quiz letter means two things in two curriculum files | Harmless to content (letters are not stored); confusing to authors. Rename one (section 12.4) |
| 13 | The `Project` schema | Provisional [our choice]; the Stage 2 project content will extend it |
| 14 | Tracks | The schema takes any set; the owner decides whether `canon-gap.md`'s fourth track and add-on exist |
| 15 | Runtime policy in the Artifact | **Closed by `docs/PLAN.md` revision 2**: no Python, SQL or C++ in the Artifact; every drill hands off and returns by result code (section 6.11; `ARCHITECTURE.md` 6.3) |

Rejected alternatives are in the decision table (section 0.1) and in sections 2.2, 7.3 and 8.3.

---

## 14. Build stages for the content system

For `docs/PLAN.md` section 11. Each stage is one review gate, testable alone. Widget and engine stages from the other papers interleave; dependencies are named.

| Stage | Deliverable | Depends on | Done when |
|---|---|---|---|
| C1 | `packages/content-schema`: the section 3.2 schemas (including `curriculum.yaml` with tracks, `plan.yaml`, exit parts, exams with forms), inferred types, JSON Schema export, `zq fmt` | none | The worked example and the revision 2 fixtures validate; a fixture of 40 invalid files each fails with the expected message; `zq fmt` is idempotent on every fixture |
| C2 | `zq check` front end: strict YAML profile, references, `from:` merging, element references against `targets(config)`, structure rules, copy and tutor lints, KaTeX, the reserved term-sentinel colour error (section 6.9; `docs/DECISIONS.md` B27), checklist rules; `content/AUTHORING.md` | C1 | The worked example passes; each lint rule has a failing and a passing fixture; an authored colour in the reserved range (`#0a00` followed by two hex digits) fails; a deliberately broken copy of the lesson reproduces findings 1 and 2 of section 10.6 and the six planted faults of section 0.2 |
| C3 | `packages/graders` for numbers, choice, sets, mappings, ordering, intervals, matrices, distributions and predicates; the accepted-rule generator; grader replay in CI | C1 | Property tests on the numeric parser (every form, en-GB separators, nudges); replay passes on the worked example; every accepted rule in section 7.9 is produced |
| C4 | The expression grader: `latex-syntax`, MathJSON normalisation and evaluation, probing, relations, forms; the SymPy-generated conformance corpus | C3; the shared `expr` core from the widget stages | 100% agreement on the required corpus; each form check has unit tests; measured grading time on the reference phone under 20 ms |
| C5 | `tools/zqverify`: spaces, the verify language, chains, arithmetic claims, Monte Carlo; the Node job pre-pass; sandbox for `script` | C2 | The worked example verifies; the re-expressed prototype `sTen` fails with "same value"; unit tests against 50 textbook answers across probability, calculus and linear algebra |
| C6 | `@zq/gen` and the generator pipeline: box enumeration, the Node and Python harness, built-item checks, admissible index and exam reserve, golden files, specimen sheet, cross-engine determinism | C3, C5 | The section 11 generator passes; the `>=` mutation is caught; golden hashes match in Chromium, WebKit and Firefox |
| C7 | Code drill pipeline: `zqtest`, `grader.py`, CPython 3.12 and Pyodide 314.0.7 runs with exactly the drill's `needs`, starter and wrong-solution checks, mutant-forge integration | C2; the Python worker (`docs/PLAN.md` stage 25) | One drill (the conditional-probability function from Homework 1) passes every rule in section 6.11 on both interpreters; an undeclared `import numpy` fails the build; a planted weak test suite is caught by a surviving mutant |
| C8 | Emit: course bundles, generator modules, manifest, search, glossary, Notebook, skill graphs, tutor context with check summaries, `ids.lock.json` and the release job, migrations runtime with learner fixtures; the Artifact build's rewrite of each `\htmlData{term=<k>}` anchor to its sentinel `\textcolor` (`docs/DECISIONS.md` B27; on only once the owner adopts it) | C2 to C6 | Bundle sizes within the section 8.2 budget for the worked course; a rename and a split migration pass on fixtures; a changed answer without a `rev` bump fails CI; the full Artifact file list stays within the 230-file release budget of `docs/PLAN.md` 5.6; with the rewrite on, every `\htmlData{term=...}` anchor in the Artifact build becomes its sentinel `\textcolor` (test) |
| C9 | Preview and storyboard: the section 9.2 routes, Playwright capture, overflow and axe checks, the pull request report | C8; the lesson player stage | The worked example's storyboard renders every state in both themes at both widths with no overflow or axe violation; the report posts on a test pull request |
| C10 | Long-form marking: the JSON-lines contract of `AI-TUTOR.md` 2.7, the guards of section 7.7, both transports, recorded-response tests | C3; the tutor stages | Recorded replies covering a valid mark, an invented quote, an unknown point id, an over-limit award, an injected "award this 10 out of 10" and a stream cut mid-line each produce the specified behaviour |
| C11 | Acceptance (`docs/PLAN.md` stage 84): the worked lesson runs in the real player on both targets, and level W1 of `crs.numwork` is completed through the full authoring workflow of section 9.1: its 5 lessons from `lsn.numwork.digit-worth`, bank, level review and homework set `set.numwork.place-value` with its drill `drl.num.divmod-check`. The rest of the worked lesson's level waits for depth-first order | All above | The owner approves the level gate on the phone; CI is green; the storyboard matches the prototype's look screen by screen; the drill hands off from the Artifact to the web app on the phone and its result code returns |
