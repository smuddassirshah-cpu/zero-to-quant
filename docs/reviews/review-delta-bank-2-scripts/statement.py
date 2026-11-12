#!/usr/bin/env python3
"""What a learner sees of a code task before Submit: prose, question, starter, the two examples and the `how` line.
No tests and no solution, so that the reader's own solution is written blind. Usage: statement.py <id> ..."""
import json, glob, sys
items = {}
for f in sorted(glob.glob('app/content/bank/*.json')):
    for it in json.load(open(f)).get('items', []):
        items[it['id']] = (f.split('/')[-1][:-5], it)
for i in sys.argv[1:]:
    f, it = items[i]; w = it['widget']
    print(f"===== {f} {i} d{it['difficulty']} pace{it['pace']} req{it.get('requires')}")
    print('PROSE:', it.get('prose')); print('Q:', it['question']); print('STARTER:', repr(w['starter'])); print('HOW:', w.get('how'))
    for t in w.get('examples', []): print('  EX', json.dumps(t, ensure_ascii=False)[:300])
    print('n tests:', len(w.get('tests', [])), '| generic:', it['feedback'].get('generic'))
