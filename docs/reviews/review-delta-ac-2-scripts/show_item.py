#!/usr/bin/env python3
"""Reading aid: print any object with the given id from one content file, whole.
Usage (repo root): python docs/reviews/review-delta-ac-2-scripts/show_item.py <file under app/content> <id> [<id> ...]"""
import json, sys


def walk(o, ids):
    if isinstance(o, dict):
        if o.get('id') in ids:
            print('=====', o['id'])
            print(json.dumps(o, indent=1, ensure_ascii=False))
            return
        for v in o.values():
            walk(v, ids)
    elif isinstance(o, list):
        for v in o:
            walk(v, ids)


walk(json.load(open('app/content/' + sys.argv[1])), set(sys.argv[2:]))
