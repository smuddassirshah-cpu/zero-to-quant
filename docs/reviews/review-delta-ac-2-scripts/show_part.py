#!/usr/bin/env python3
"""Reading aid: print one part (1-based) of a problem-set item. show_part.py <file under app/content> <id> <part>"""
import json, sys
d = json.load(open('app/content/' + sys.argv[1]))
it = next(i for i in d['items'] if i['id'] == sys.argv[2])
print('prose:', it.get('prose'))
print(json.dumps(it['parts'][int(sys.argv[3]) - 1], indent=1, ensure_ascii=False))
