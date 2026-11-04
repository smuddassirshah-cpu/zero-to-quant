#!/bin/sh
# Runs every check for the topic 3.5 mocks and the topic 3.5 exam plan (standard library; numpy and pandas for qd_tasks.py).
# Each script ends with ALL AGREE, PLAN OK, FRESH or VOICE: clean.  Run from anywhere.
D=$(cd "$(dirname "$0")" && pwd)
cd "$D" || exit 1
python3 -I gen_qd_data.py && python3 -I oa_code.py | tail -1 && python3 -I research_mocks.py | tail -1 \
  && python3 -I qd_tasks.py | tail -1 && python3 -I exam35_plan.py | tail -1 && python3 -I fresh.py | tail -1 && python3 -I voice.py
