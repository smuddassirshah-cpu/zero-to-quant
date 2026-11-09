"""Print exam items. Usage: show.py <exam.json> blind|key <id-prefix>...
blind prints question and options only; key adds the key, why, feedback and explain."""
import json
import sys

f, mode = sys.argv[1], sys.argv[2]
pats = sys.argv[3:]
d = json.load(open(f))
for pi, p in enumerate(d['parts']):
    for ii, it in enumerate(p.get('items', [])):
        if not any(it['id'].startswith(x) for x in pats):
            continue
        print('=== parts[%d].items[%d]' % (pi, ii), it['id'], 'part', p['id'], it.get('difficulty'), it.get('pace'))
        print('Q:', it['question'])
        w = it['widget']
        print('widget', w.get('type'), [k for k in w if k != 'options'])
        if 'lines' in w:
            for ln in w['lines']:
                print('   line:', ln if mode == 'key' else {k: v for k, v in ln.items() if k not in ('why', 'value', 'p')} if isinstance(ln, dict) else ln)
        for o in w.get('options', []):
            extra = ''
            if mode == 'key':
                extra = '  [CORRECT]' if o.get('correct') else '  why: ' + str(o.get('why'))
            print('  ', o['id'], ':', o['text'], extra)
        if mode == 'key':
            for k in w:
                if k not in ('options', 'type'):
                    print('  w.', k, w[k])
            print('FB:', it.get('feedback'))
            print('EX:', it.get('explain'))
