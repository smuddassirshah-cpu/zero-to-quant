"""Shared number-check helper for level number scripts (ENGINE-BACKLOG 573). Pure standard library.

Use from docs/reports/<course>-L<n>-numbers.py:
    import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
    from numbers_lib import Level
    lv = Level("odes", 3)                       # every lesson, the review and the homework of that level
    lv.expect("l10", "screens[3].widget.answer", 3)               # numeric token equal to 3 in a string or number
    lv.expect("l10", "screens[3].prose", -0.5)                    # a minus may be written "-" or U+2212
    lv.expect("review", "items[2].widget.options[1].why", 1214)   # "1,214", "£1,214" and "$1{,}214$" all match
    lv.expect("l11", "screens[5].widget.wrong[0].value", 0.25, fmt="{:.2f}")   # fmt: the exact text that must appear
    lv.expect("l12", "screens[2]", 7)                             # a path that ends on an object or list searches every string below it
    lv.expect("l12", "screens[*].prose", 7)                       # [*] joins every element
    lv.report()                                                   # prints the count, exits 1 on any failure
`file` is a lesson id or a unique prefix ("l10"), "review" or "homework". `lv.text(file, path)` returns the string
(strings below an object or list are joined with newlines) for ad-hoc checks. Without `fmt` a number matches any token
of equal value after normalisation (thousands commas, currency signs, LaTeX spacing and braces, U+2212, trailing zeros; a LaTeX fraction \\tfrac{3}{4}, \\frac{1}{2} or \\frac12 matches its value and its integers);
a string value must appear verbatim in the raw or the normalised text.
"""
import json
import os
import re
import sys

COURSES = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'content', 'courses')
_PART = re.compile(r'([A-Za-z_][\w]*)|\[(\d+|\*)\]')


def _strings(x):
    if isinstance(x, str):
        return [x]
    if isinstance(x, dict):
        return [s for v in x.values() for s in _strings(v)]
    if isinstance(x, list):
        return [s for v in x for s in _strings(v)]
    if isinstance(x, (int, float)) and not isinstance(x, bool):
        return [repr(x)]
    return []


def _walk(node, path):
    """Return the list of nodes a path selects ([*] fans out)."""
    nodes = [node]
    for key, idx in _PART.findall(path):
        nxt = []
        for n in nodes:
            if key:
                if not isinstance(n, dict) or key not in n:
                    raise KeyError(f'no key "{key}" in {path}')
                nxt.append(n[key])
            elif idx == '*':
                if not isinstance(n, list):
                    raise KeyError(f'[*] on a non-list in {path}')
                nxt.extend(n)
            else:
                if not isinstance(n, list) or int(idx) >= len(n):
                    raise KeyError(f'no index {idx} in {path}')
                nxt.append(n[int(idx)])
        nodes = nxt
    return nodes


def normalise(s):
    s = s.replace('−', '-').replace('–', '-').replace('£', '').replace('\\pounds', '')
    s = re.sub(r'\\[,;:! ]|\\text\{[^}]*\}|\\mathrm\{[^}]*\}', '', s)
    s = re.sub(r'\{,\}', ',', s)
    s = s.replace('{', '').replace('}', '').replace('$', '')
    while True:                                   # thousands separators
        t = re.sub(r'(?<=\d),(?=\d{3}(?!\d))', '', s)
        if t == s:
            break
        s = t
    return s


_NUM = re.compile(r'(?<![\w.])-?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?(?![\d]|\.\d)')


_FRAC = re.compile(r'\\[dtc]?frac\s*(?:\{([^{}]+)\}\s*\{([^{}]+)\}|(\d)(\d))')


def _numbers(s):
    out = []
    fr = []

    def _frac(m):                                 # \tfrac{3}{4}, \frac34: keep both integers as tokens and add the value
        a, b = (m.group(1), m.group(2)) if m.group(1) is not None else (m.group(3), m.group(4))
        try:
            x, y = float(normalise(a)), float(normalise(b))
            if y != 0:
                fr.append(x / y)
        except ValueError:
            pass
        return f' {a} {b} '
    s = _FRAC.sub(_frac, s)
    for m in _NUM.finditer(normalise(s)):
        try:
            out.append(float(m.group(0).rstrip('.')))
        except ValueError:
            pass
    return out + fr


class Level:
    def __init__(self, course, n):
        self.course, self.n, self.files, self.results = course, n, {}, []
        d = os.path.join(COURSES, course)
        with open(os.path.join(d, 'course.json'), encoding='utf8') as f:
            lv = json.load(f)['levels'][n - 1]
        for fid in list(lv.get('lessons', [])) + [lv.get('review'), lv.get('homework')]:
            p = os.path.join(d, f'{fid}.json') if fid else None
            if p and os.path.exists(p):
                with open(p, encoding='utf8') as f:
                    self.files[fid] = json.load(f)
        if not self.files:
            raise SystemExit(f'numbers_lib: no files for {course} level {n}')

    def _file(self, ref):
        if ref in ('review', 'homework'):
            ref = f'{ref}-{self.n}'
        hits = [k for k in self.files if k == ref] or [k for k in self.files if k.startswith(ref)]
        if len(hits) != 1:
            raise KeyError(f'file "{ref}" matches {hits or "nothing"} in {sorted(self.files)}')
        return hits[0], self.files[hits[0]]

    def text(self, ref, path):
        _, doc = self._file(ref)
        return '\n'.join(s for n in _walk(doc, path) for s in _strings(n))

    def expect(self, ref, path, value, fmt=None):
        label = f'{ref} {path} = {value!r}'
        try:
            txt = self.text(ref, path)
        except KeyError as e:
            return self._rec(False, label, str(e))
        if isinstance(value, str):
            ok = value in txt or value in normalise(txt)
        elif fmt is not None:
            want = fmt(value) if callable(fmt) else fmt.format(value)
            ok = want in txt or normalise(want) in normalise(txt)
        else:
            ok = any(abs(x - value) <= 1e-9 * max(1.0, abs(value)) for x in _numbers(txt))
        return self._rec(ok, label, '' if ok else f'not found in: {txt[:120]!r}')

    def _rec(self, ok, label, note):
        self.results.append((ok, label, note))
        print(f"{'ok ' if ok else 'BAD'} {label}" + (f'  ({note})' if note else ''))
        return ok

    def report(self):
        bad = [r for r in self.results if not r[0]]
        print(f'numbers_lib: {len(self.results) - len(bad)} of {len(self.results)} checks passed')
        if bad:
            sys.exit(1)
