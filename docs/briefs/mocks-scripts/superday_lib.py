"""Item constructors shared by superday_strats_build.py and superday_developer_build.py (standard library only).

Each constructor returns an exam item in the AUTHORING section 5 shape. Choice options are shuffled by the caller's
seeded random.Random, and ids a, b, c, d are given after the shuffle, so no id says which option is the key.
`voice_problems(doc)` lists learner-visible sentences of 20 words or more, explanations over three sentences,
exclamation marks and dashes, so a build stops before it writes a file that the voice scan would reject.
"""
import json
import re


def numeric(answer, tol, wrongs=(), placeholder='a number', unit=None, accept=None, label='Your answer', **extra):
    w = {'kind': 'numeric', 'answer': answer, 'tol': {'abs': tol}, 'placeholder': placeholder, 'label': label}
    if unit:
        w['unit'] = unit
    if wrongs:
        w['wrong'] = [{'id': i, 'value': v, 'tol': {'abs': t}} for i, v, t, _ in wrongs]
    w['accept'] = accept if accept is not None else f'{answer}'
    w.update(extra)
    return w


def byKey(wrongs):
    return {i: txt for i, _, _, txt in wrongs}


def choice(rng, options):
    """options: list of (text, None) for the key or (text, why) for a distractor."""
    opts = [dict(text=t, **({'correct': True} if why is None else {'why': why})) for t, why in options]
    rng.shuffle(opts)
    for k, o in zip('abcdef', opts):
        o['id'] = k
    out = []
    for o in opts:
        d = {'id': o['id'], 'text': o['text']}
        if o.get('correct'):
            d['correct'] = True
        else:
            d['why'] = o['why']
        out.append(d)
    return {'kind': 'choice', 'layout': 'stack', 'shuffle': True, 'options': out}


def fb(correct, generic, wrongs=()):
    f = {'correct': correct, 'generic': generic}
    if wrongs:
        f['byKey'] = byKey(wrongs)
    return f


def item(iid, diff, skills, tags, pace, title, question, widget, feedback, explain, prose=None):
    it = {'id': iid, 'difficulty': diff, 'skills': skills, 'tags': tags, 'pace': pace, 'title': title}
    if prose:
        it['prose'] = prose
    it['question'] = question
    it['widget'] = widget
    it['feedback'] = feedback
    it['explain'] = {'text': explain}
    return it


def part(question, widget, feedback, explain=None):
    p = {'question': question, 'widget': widget, 'feedback': feedback}
    if explain:
        p['explain'] = {'text': explain}
    return p


def parts_item(iid, diff, skills, tags, pace, title, prose, parts, explain=None):
    it = {'id': iid, 'difficulty': diff, 'skills': skills, 'tags': tags, 'pace': pace, 'title': title, 'prose': prose, 'parts': parts}
    if explain:
        it['explain'] = {'text': explain}
    return it


def longform(iid, diff, skills, tags, pace, title, prompt, model, rubric):
    assert sum(p for p, _ in rubric) == 10, (iid, sum(p for p, _ in rubric))
    return {'id': iid, 'difficulty': diff, 'skills': skills, 'tags': tags, 'pace': pace, 'title': title, 'kind': 'longform',
            'prompt': prompt, 'model': model, 'rubric': [{'points': p, 'text': t} for p, t in rubric]}


# ---------------------------------------------------------------- voice
SKIP = {'id', 'kind', 'skills', 'tags', 'answer', 'starter', 'solution', 'prelude', 'postlude', 'setup', 'call', 'expect',
        'compare', 'language', 'layout', 'tests', 'examples', 'types', 'args', 'signature', 'unit', 'style'}


def _strings(o, path=''):
    if isinstance(o, str):
        yield path, o
    elif isinstance(o, dict):
        for k, v in o.items():
            if k not in SKIP:
                yield from _strings(v, f'{path}.{k}' if path else k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from _strings(v, f'{path}.{i}')


def _mask(t):
    t = re.sub(r'```.*?```', ' ', t, flags=re.S)
    t = re.sub(r'`[^`]*`', 'CODE', t)
    t = re.sub(r'\$\$.*?\$\$', ' MATH ', t, flags=re.S)
    return re.sub(r'\$[^$]*\$', 'MATH', t)


def _sentences(t):
    out = []
    for line in _mask(t).split('\n'):
        line = re.sub(r'^([-*]|\d+\.)\s+', '', line.strip())
        for s in re.split(r'(?:(?<=[.?!])|(?<=[.?!]\*\*)|(?<=[.?!]\*)|(?<=[.!]")|(?<=[.?!]\)))\s+(?=\S)', line):
            if s.strip():
                out.append(s.strip())
    return out


def voice_problems(doc):
    bad = []
    for path, t in _strings(doc):
        if '!' in _mask(t) or '—' in t or '–' in t:
            bad.append((path, 'exclamation or dash', t[:80]))
        for s in _sentences(t):
            n = len([w for w in s.split() if re.search(r'[A-Za-z0-9£]', w)])
            if n >= 20:
                bad.append((path, f'{n} words', s))
        if re.search(r'(explain\.text|\.why|\.byKey\.[^.]+)$', path) and len(_sentences(t)) > 3:
            bad.append((path, 'over three sentences', t[:80]))
    return bad


def write(doc, path):
    bad = voice_problems(doc)
    for b in bad:
        print('VOICE', *b)
    assert not bad, f'{len(bad)} voice problems'
    with open(path, 'w', encoding='utf8') as f:
        json.dump(doc, f, indent=2, ensure_ascii=False)
        f.write('\n')
