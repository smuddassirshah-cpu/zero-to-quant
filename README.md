# Zero to Quant

An interactive learning app that takes one learner from school arithmetic to quant-interview readiness, following the 3,100-hour curriculum in `docs/curriculum.md`. Lessons are short and hands-on in the style of Brilliant: you manipulate a diagram, answer, get feedback on your own answer, and only then meet the rule.

## Get started

You need:

- Git, to clone.
- Python 3, only for `app/run.sh`, which is `python3 -m http.server`.
- Chrome or Chromium. The app uses WebAssembly in background workers.
- A network connection on first use (see below). Node is needed only for the checking tools, not to run the app.

```sh
git clone https://github.com/smuddassirshah-cpu/zero-to-quant.git
cd zero-to-quant
app/run.sh            # port 8080; pass another port as the first argument
```

Open `http://localhost:8080` in Chrome. A fresh browser opens `#setup` (name, track, weekly hours, starting stage) and then `#today`. The app must be served over `http`: opened as a `file://` page it cannot fetch its content or start its workers. There are no accounts, no server code and no build step. Your progress stays in this browser and can be exported from the You screen.

Maths and code tools load from the jsDelivr CDN the first time a lesson needs them, so the first such lesson is slow. `app/README.md` lists what loads, what you see if it fails, and how to self-host.

## What is here

- `app/`: the app. See `app/README.md` for the folders, the content validator and how the pieces fit.
- `docs/curriculum.md`: the curriculum: four stages, their topics, hours, resources and exit tests.
- `docs/PLAN.md`: the engine blueprint and build contract.
- `docs/AUTHORING.md`: the contract for lesson, review, homework, exam and drill files.
- `docs/design-research.md`: the researched design language, lesson anatomy and voice.

## Status

Every course of the curriculum is mapped and written: 1,236 lessons in 79 course maps, 283 levels, 29 topic exams, 4 stage exams, 16 mock assessments, 270 code drills, 100 Fluency sets and 167 problem sets, about 3,695 hours of teaching. `node app/tools/census.mjs` prints the current counts.

Checks: `node app/tools/validate.mjs` (run from `app/`) must report 0 errors, and `.github/workflows/acceptance.yml` runs the full acceptance on every push (`docs/CI.md`).
