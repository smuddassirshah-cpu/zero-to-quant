#!/bin/sh
# usage: run.sh script.py   (uses the scratchpad pylib with SciPy 1.14.1, scikit-learn 1.6.1, statsmodels)
S=/tmp/claude-0/-home-user-zero-to-quant/ab4c69e5-1166-5ca2-9e21-f6569e1af79e/scratchpad
cd $S/research-int && PYTHONPATH=$S/pylib python3 -I -c "import sys; sys.path[:0]=['$S/pylib','$S/research-int']; exec(open('$1').read())"
