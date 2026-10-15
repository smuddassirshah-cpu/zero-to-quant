# Zero to Quant

An interactive learning app that takes one learner from school arithmetic to quant-interview readiness, following the 3,100-hour curriculum in `docs/curriculum.md`. Lessons are short and hands-on in the style of Brilliant: you manipulate a diagram, answer, get feedback on your own answer, and only then meet the rule.

## Run it

```sh
app/run.sh
```

Open `http://localhost:8080` in Chrome. The app is a static folder: no accounts, no server code, no build step. Your progress stays in this browser and can be exported from the You screen.

## What is here

- `app/`: the app. See `app/README.md` for the folders, the content validator and how the pieces fit.
- `docs/curriculum.md`: the curriculum: four stages, their topics, hours, resources and exit tests.
- `docs/PLAN.md`: the engine blueprint and build contract.
- `docs/AUTHORING.md`: the contract for lesson, review, homework, exam and drill files.
- `docs/design-research.md`: the researched design language, lesson anatomy and voice.

## Status

Every course of the curriculum is mapped (60 courses, 830 lessons with names and objectives). Lessons are being written course by course; `node app/tools/validate.mjs --summary` lists what is written and what is not.
