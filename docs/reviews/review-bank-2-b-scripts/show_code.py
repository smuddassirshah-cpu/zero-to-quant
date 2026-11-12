"""show.py for a coding file with the model solutions hidden, so a reader can solve from the statement first."""
import io, sys, contextlib
import show

buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    show.show(sys.argv[1], set(sys.argv[2:]) or None)
skip = False
for line in buf.getvalue().split('\n'):
    if line.startswith('SOLUTION:'):
        skip = True
        continue
    if line.startswith('extra='):
        skip = False
        continue
    if not skip:
        print(line)
