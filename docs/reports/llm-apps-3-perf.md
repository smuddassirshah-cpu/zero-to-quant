# llm-apps level 3: performance task

- `homework-3.json`, item `h-agent`, index 0. Kind `code` (Python, difficulty 5).
- Matched objective: l11 "Build an agent loop with stop conditions and a step cap against a scripted model." (also l10 "Code a parser that validates a model's tool call and returns errors the model can act on." and l9 "Write tool definitions as JSON schemas and validate arguments against them.").
- Task: from a stub holding only the class and method signatures, `Agent(tools, schemas, max_steps).run(task, model)` shows the model each tool's name, description and input schema; validates every call (types, required, enum, bounds, extra keys); returns every failure as an actionable tool error (JSON named for broken arguments, the real tools listed for an unknown name, the field and expected type or the missing field, a tool's own exception message passed on); stops on an answer, after 3 identical calls in a row or at the cap; and returns the messages with a score (right answer, required tools, invalid calls, steps, success).
- 11 hidden tests, 1 example, on 8 hidden scripted tasks registered in the test setup (H01 to H08, tickers and dates no lesson uses): a clean task, one planted failure of each kind (broken JSON, unknown tool, integer date, missing date, a holiday close), an endless search under caps of 8 and 2, an answer from memory, the invalid-call count and the roles of a run's messages. Seven mutants, each first failing its own test with a `byKey` line: JSON not caught, tools not listed, type not named, tool exception not caught, no repeat stop, answer-only success, cap off by one.
- Overlapping screens: l9 screen 8 codes `validate`; l10 screen 8 codes `parse_call` and `run_call`; l11 screen 8 codes `run_agent` and `repeated_call`; l12 screen 9 codes `score_trajectory` (screens counted from 0). The task joins all four into one class from nothing, with the tools passed as plain functions and schemas, and is tested on hidden tasks.

Gates:
1. `node tools/validate.mjs`: 0 errors.
2. `VOICE_BASE=app/content/courses/llm-apps python3 docs/reviews/voice-scan.py 35`: 0 over 35 words, 0 lesson ids in code spans, 0 doubled words.
3. Numbers script `docs/reports/llm-apps-L3-numbers.py` (venv, strict, through `tools/run-number-scripts.mjs`): exit 0; it reruns the solution and a route-B twin harness against every test and checks every mutant's first failing test.
4. Playthrough `--set llm-apps/homework-3 --local-cdn <pkgs>`, with and without `--mobile`: all passed, the starter fails. `grade-all.mjs --code --strict-feedback`: 0 failures.
