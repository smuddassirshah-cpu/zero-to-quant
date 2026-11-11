"""Compact dump of a problems-<n>.json file for reading: one block per part.

Usage: python dump.py app/content/courses/<course>/problems-<n>.json
"""
import json
import sys

d = json.load(open(sys.argv[1]))


def tol(t):
    return '' if t is None else '±' + json.dumps(t, separators=(',', ':'))


for it in d['items']:
    extra = {k: v for k, v in it.items() if k not in ('id', 'difficulty', 'skills', 'prose', 'parts')}
    print(f"\n#### {it['id']} d{it['difficulty']} {it['skills']} "
          f"{json.dumps(extra, ensure_ascii=False)[:600] if extra else ''}")
    print('PROSE:', it['prose'])
    for i, p in enumerate(it['parts'], 1):
        w = p['widget']
        print(f"\n [{i}] Q: {p['question']}")
        ex = {k: v for k, v in p.items() if k not in ('question', 'widget', 'feedback', 'explain')}
        if ex:
            print('   EXTRA', json.dumps(ex, ensure_ascii=False)[:500])
        k = w['kind']
        fb = p['feedback']
        if k == 'choice':
            for o in w.get('options', []):
                print('   opt', json.dumps(o, ensure_ascii=False))
            print('   rest', json.dumps({a: b for a, b in w.items() if a not in ('options', 'kind')},
                                        ensure_ascii=False))
        else:
            rest = {a: b for a, b in w.items()
                    if a not in ('kind', 'answer', 'tol', 'accept', 'wrong', 'placeholder')}
            print(f"   {k} ANS={w.get('answer')!r} {tol(w.get('tol'))} accept={w.get('accept')!r} "
                  f"{json.dumps(rest, ensure_ascii=False) if rest else ''}")
            for x in w.get('wrong', []):
                print(f"   wrong {x['id']}={x.get('value', x.get('expr'))!r}{tol(x.get('tol'))} :: "
                      f"{fb.get('byKey', {}).get(x['id'])}")
        print('   OK:', fb.get('correct'))
        print('   GEN:', fb.get('generic'))
        for b in set(fb.get('byKey', {})) - {x['id'] for x in w.get('wrong', [])}:
            print('   byKey(extra)', b, fb['byKey'][b])
        e = p.get('explain')
        print('   EXP:', e['text'] if isinstance(e, dict) else e)
