"""Per-set shape checks the brief asks for. Run from the repo root.

- numeric parts whose question names no answer form (flagging those whose answer is not a whole number)
- explanations of more than three sentences; exclamation marks, em-dashes, dollar money, common US spellings
- typed share, difficulty spread, parts per item, skills against course.json
- later parts that do not restate a value (no "part", "Using", "from" and no number of an earlier answer in the question)
"""
import json
import re

FORM = re.compile(r'Give |whole number|decimal|fraction|nearest|percentage|per cent|negative number|Leave out|Write |Simplify', re.I)
US = re.compile(r'\b(color|center|favor|analyz|modeled|modeling|labeled|canceling|canceled|traveled|percent\b|math\b)', re.I)


def sentences(text):
    t = re.sub(r'\$[^$]*\$', 'M', text)            # maths out, so a decimal point is not a sentence end
    t = re.sub(r'\b(e\.g|i\.e)\.', 'eg', t)
    return [s for s in re.split(r'(?<=[.?])\s+', t.strip()) if s]


for c in ('limits', 'integrals'):
    course = json.load(open(f'app/content/courses/{c}/course.json'))
    for n in (1, 2, 3):
        d = json.load(open(f'app/content/courses/{c}/problems-{n}.json'))
        items = d['items']
        parts = [(it, i, p) for it in items for i, p in enumerate(it['parts'], 1)]
        typed = sum(p['widget']['kind'] in ('numeric', 'expression') for _, _, p in parts)
        print(f'\n== {c} problems-{n}: {len(items)} problems, {len(parts)} parts, typed {typed}, '
              f'difficulties {[it["difficulty"] for it in items]}, parts/item {[len(it["parts"]) for it in items]}')
        for it in items:
            bad = [s for s in it['skills'] if s not in course['skills']]
            if bad:
                print('  unknown skill', it['id'], bad)
        for it, i, p in parts:
            w = p['widget']
            where = f'  {it["id"]} part {i}'
            if w['kind'] == 'numeric' and not FORM.search(p['question']):
                a = w.get('answer')
                whole = a is not None and float(a) == int(a)
                print(f'{where}: no form sentence; answer {a} ({"whole" if whole else "NOT WHOLE"}); unit {w.get("unit")}')
            texts = [p['question'], p['explain']['text'], it['prose']] + list(p['feedback'].values())[:2] \
                + list(p['feedback'].get('byKey', {}).values()) \
                + [o.get('text', '') + ' ' + o.get('why', '') for o in w.get('options', [])]
            ns = len(sentences(p['explain']['text']))
            if ns > 3:
                print(f'{where}: explanation has {ns} sentences')
            for tx in texts:
                if '!' in re.sub(r'\$[^$]*\$', '', tx) or '—' in tx or US.search(re.sub(r'\$[^$]*\$', '', tx)):
                    print(f'{where}: voice: {tx[:90]}')
                if re.search(r'(?<!\\)\$\d', re.sub(r'\$[^$]*\$', '', tx)):
                    print(f'{where}: dollar money: {tx[:90]}')
            if i > 1 and not re.search(r'[Pp]art|Using|from|With |So ', p['question']):
                print(f'{where}: question names no earlier part: {p["question"][:110]}')
            if w['kind'] == 'choice':
                opts = w['options']
                lens = [len(o['text']) for o in opts]
                right = next(o for o in opts if o.get('correct'))
                if len(right['text']) == max(lens) and sorted(lens)[-1] > 1.25 * sorted(lens)[-2]:
                    print(f'{where}: correct option is the longest by more than a quarter {lens}')
                for o in opts:
                    if re.search(r'\b(first|second|third|last|above|below) option|option [A-Da-d]\b', o.get('text', '') + o.get('why', '')):
                        print(f'{where}: option named by place')
