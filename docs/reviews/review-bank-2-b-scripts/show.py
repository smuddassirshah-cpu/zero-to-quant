"""Compact dump of bank files for reading. Usage: show.py finance-1 [item-id ...]"""
import json, sys, os
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..', 'app', 'content', 'bank')


def show(name, only=None):
    d = json.load(open(os.path.join(ROOT, name + '.json')))
    print('FILE', d['id'], '|', d['name'], '|', d.get('description'))
    for it in d['items']:
        if only and it['id'] not in only:
            continue
        w = it['widget']
        print(f"\n### {it['id']} D{it['difficulty']} {w['kind']} pace={it.get('pace')} tags={it['tags']} skills={it.get('skills')} req={it.get('requires')} role={it['role']}")
        if it.get('prose'):
            print('P:', it['prose'])
        print('Q:', it.get('question'))
        if w['kind'] == 'numeric':
            known = ('kind', 'answer', 'tol', 'accept', 'label', 'placeholder', 'wrong', 'unit')
            print(f"A: {w['answer']} tol={w.get('tol')} accept={w.get('accept')} label={w.get('label')} ph={w.get('placeholder')} unit={w.get('unit')} extra={[k for k in w if k not in known]}")
            for x in w.get('wrong', []):
                print(f"  W {x['id']}: {x['value']} tol={x.get('tol')} -> {it['feedback'].get('byKey', {}).get(x['id'])}")
        elif w['kind'] == 'choice':
            for o in w['options']:
                print(f"  {'*' if o.get('correct') else '-'} [{len(o['text'])}] {o['text']}  || {o.get('why')}")
        elif w['kind'] == 'code':
            print('STARTER:', repr(w['starter']))
            print('EXAMPLES:', [(e['call'], e['expect'], e.get('compare')) for e in w['examples']])
            print('TESTS:')
            for t in w['tests']:
                print('   ', t['call'], '=>', t['expect'], t.get('compare'))
            for kind in ('examples', 'tests'):
                for i, c in enumerate(w[kind]):
                    extra = {k: v for k, v in c.items() if k not in ('call', 'expect', 'compare')}
                    if extra:
                        print(f'    {kind} {i + 1} also has', str(extra)[:500])
            print('HOW:', w.get('how'))
            print('SOLUTION:\n' + w['solution'])
            print('extra=', [k for k in w if k not in ('kind', 'language', 'starter', 'examples', 'tests', 'how', 'solution')])
        else:
            print(json.dumps(w)[:600])
        fb = it['feedback']
        print('FB+:', fb.get('correct'))
        print('FB?:', fb.get('generic'))
        print('EX:', it['explain']['text'])


if __name__ == '__main__':
    show(sys.argv[1], set(sys.argv[2:]) or None)
