"""Print keys, distractor whys, feedback and explanations for one part of a mock (after the blind sitting).

Usage: python show.py <exam json> <part index>
"""
import json
import sys

d = json.load(open(sys.argv[1]))
p = d['parts'][int(sys.argv[2])]
for it in p['items']:
    w = it['widget']
    print(f"## {it['id']}  tags={it['tags']}  title={it['title']}")
    if w['kind'] == 'choice':
        for o in w['options']:
            print('  ', '*' if o.get('correct') else '-', o['text'], '|', o.get('why', ''))
    else:
        print('   answer', w['answer'])
    print('   FB', it['feedback'])
    print('   EX', it['explain']['text'])
