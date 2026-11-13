"""Shared checks for the py-found L1 and L2 number scripts (second read, session V).

Pure standard library. Used by docs/reports/py-found-L1-numbers.py and py-found-L2-numbers.py.

- check_code(lv): every Python `code` widget in the level. The solution passes every example and hidden test, the starter
  fails at least one, the `how` line and any "All N tests passed" line name the true test count, and every byKey key
  `test-N` (and every "Test N" it mentions) points at a real test. Tests run in one namespace, in order, as in the app.
- check_print(lv, ref, path, setup='', last_line=False): run the first ```python block of the item's prose (or prompt)
  in CPython, capture what it prints, and compare it with the keyed option. The expected output is read from the option
  text: each `code span` is one printed line; an option naming an `...Error` expects that exception. Also checks that no
  distractor reads as the same output (two right answers). Data-driven, so it passes again once a fix changes the code
  or the key consistently.
- run_snippet(code): (stdout, exception) for ad-hoc checks.
"""
import contextlib
import io
import math
import re

WORDS = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10}


def _walk_widgets(node, path, out):
    if isinstance(node, dict):
        w = node.get('widget')
        if isinstance(w, dict) and w.get('kind') == 'code':
            out.append((path, node, w))
        for k, v in node.items():
            _walk_widgets(v, f'{path}.{k}' if path else k, out)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            _walk_widgets(v, f'{path}[{i}]', out)


def _close(a, b, rel, abs_):
    """isclose on numbers, and element by element on lists and tuples (as the app's `isclose` compare does)."""
    if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
        return len(a) == len(b) and all(_close(x, y, rel, abs_) for x, y in zip(a, b))
    if isinstance(a, dict) and isinstance(b, dict):
        return a.keys() == b.keys() and all(_close(a[k], b[k], rel, abs_) for k in a)
    if isinstance(a, (int, float)) and isinstance(b, (int, float)) and not isinstance(a, bool) and not isinstance(b, bool):
        return math.isclose(a, b, rel_tol=rel, abs_tol=abs_)
    return a == b


def _run_tests(src, w):
    """Return (results, load_error): results is a list of (label, ok, note) over examples then tests."""
    ns = {'__name__': '__main__', '__learner_source__': src}
    try:
        with contextlib.redirect_stdout(io.StringIO()):
            if w.get('prelude'):
                exec(w['prelude'], ns)
            exec(src, ns)
            if w.get('postlude'):
                exec(w['postlude'], ns)
    except Exception as e:  # noqa: BLE001
        return [], f'{type(e).__name__}: {e}'
    res = []
    for kind in ('examples', 'tests'):
        for i, t in enumerate(w.get(kind, [])):
            label = f'{kind}[{i}] {t.get("call")}'
            try:
                with contextlib.redirect_stdout(io.StringIO()):
                    if t.get('setup'):
                        exec(t['setup'], ns)
                    cmp = t.get('compare', 'equal')
                    if cmp == 'raises':
                        try:
                            eval(t['call'], ns)
                            ok, note = False, 'no error'
                        except Exception as e:  # noqa: BLE001
                            ok, note = type(e).__name__ == t['expect'], type(e).__name__
                    else:
                        got = eval(t['call'], ns)
                        exp = eval(str(t['expect']), ns) if isinstance(t['expect'], str) else t['expect']
                        if cmp == 'isclose':
                            tol = t.get('tol') or {}
                            ok = _close(got, exp, tol.get('rel', 1e-9 if 'abs' not in tol else 0), tol.get('abs', 1e-12))
                        else:
                            ok = got == exp
                        note = f'got {got!r}, expected {exp!r}'
            except Exception as e:  # noqa: BLE001
                ok, note = False, f'{type(e).__name__}: {e}'
            res.append((label, ok, note))
    return res, None


def check_code(lv):
    n = 0
    for fid, doc in lv.files.items():
        found = []
        _walk_widgets(doc, '', found)
        for path, holder, w in found:
            if w.get('language', 'python') != 'python':
                continue
            n += 1
            where = f'{fid} {path}'
            res, err = _run_tests(w.get('solution', ''), w)
            lv.claim(err is None, f'{where}: solution loads', err or '')
            bad = [r for r in res if not r[1]]
            lv.claim(res and not bad, f'{where}: solution passes all {len(res)} examples and tests',
                     '; '.join(f'{b[0]} -> {b[2]}' for b in bad))
            sres, serr = _run_tests(w.get('starter', ''), w)
            tests_only = [r for r in sres if r[0].startswith('tests')]
            lv.claim(serr is not None or any(not r[1] for r in tests_only), f'{where}: starter fails at least one test')
            nt = len(w.get('tests', []))
            how = w.get('how', '')
            m = re.search(r'runs (\d+) hidden tests', how)
            lv.claim(m is None or int(m.group(1)) == nt, f'{where}: how says {m.group(1) if m else "-"} tests, there are {nt}')
            fb = holder.get('feedback', {}) or {}
            m = re.search(r'All (\w+) tests passed', fb.get('correct', ''))
            if m:
                k = WORDS.get(m.group(1), m.group(1))
                lv.claim(str(k) == str(nt), f'{where}: feedback.correct says all {m.group(1)} tests, there are {nt}')
            for key, line in (fb.get('byKey') or {}).items():
                mk = re.fullmatch(r'test-(\d+)', key)
                if not mk:
                    continue
                k = int(mk.group(1))
                lv.claim(1 <= k <= nt, f'{where}: byKey {key} names a real test (of {nt})')
                for mt in re.finditer(r'\bTest (\d+)\b', line):
                    lv.claim(int(mt.group(1)) == k, f'{where}: byKey {key} text says Test {mt.group(1)}')
    return n


def run_snippet(code, setup=''):
    buf = io.StringIO()
    err = None
    ns = {'__name__': '__main__'}
    try:
        with contextlib.redirect_stdout(buf):
            if setup:
                exec(setup, ns)
            exec(compile(code, '<snippet>', 'exec'), ns)
    except Exception as e:  # noqa: BLE001  (SyntaxError included)
        err = e
    return buf.getvalue(), err


def _code_block(text):
    m = re.search(r'```python\n(.*?)```', text, re.S)
    return m.group(1) if m else None


def _expected(option_text):
    """('error', 'TypeError', msg) or ('lines', [..])."""
    m = re.search(r'([A-Z][A-Za-z]*Error)(?::\s*([^`]*))?', option_text)
    if m and ('stop' in option_text or 'error' in option_text.lower()) and 'prints' not in option_text:
        return ('error', m.group(1), (m.group(2) or '').strip())
    return ('lines', re.findall(r'`([^`]*)`', option_text))


def check_print(lv, ref, path, setup='', last_line=False):
    fid, doc = lv._file(ref)
    item = doc
    for key, idx in re.findall(r'([A-Za-z_]\w*)|\[(\d+)\]', path):
        item = item[key] if key else item[int(idx)]
    code = _code_block(item.get('prose', '') or item.get('prompt', ''))
    where = f'{fid} {path}'
    if code is None:
        return lv.claim(False, f'{where}: no python block found')
    out, err = run_snippet(code, setup)
    lines = [ln.rstrip() for ln in out.strip('\n').split('\n')] if out.strip() else []
    if last_line:
        lines = lines[-1:]

    def matches(opt_text):
        kind, *rest = _expected(opt_text)
        if kind == 'error':
            return err is not None and type(err).__name__ == rest[0] and (not rest[1] or str(err).startswith(rest[1].rstrip('.')))
        return err is None and rest[0] == lines

    opts = item['widget']['options']
    right = [o for o in opts if o.get('correct')]
    got = f'{type(err).__name__}: {err}' if err else lines
    lv.claim(len(right) == 1 and matches(right[0]['text']), f'{where}: keyed option {right[0]["text"]!r} is what CPython does',
             f'CPython gives {got!r}')
    for o in opts:
        if not o.get('correct'):
            lv.claim(not matches(o['text']), f'{where}: distractor {o["id"]} is not also right', f'CPython gives {got!r}')
    return lines, err
