#!/bin/sh
# usage: run.sh script.py
# Run gen_data.py first: the level and item checks read ./data/*.csv (not committed; regenerate from the fixed seeds).
# Needs SciPy 1.14.1, scikit-learn 1.6.1, statsmodels and pandas; set PYLIB to a
# folder made with `pip install --target <folder> ...` if system python lacks them.
D=$(cd "$(dirname "$0")" && pwd)
cd "$D" && PYTHONPATH="${PYLIB:-}" python3 -I -c "import sys; sys.path[:0]=['${PYLIB:-.}','$D']; exec(open('$1').read())"
