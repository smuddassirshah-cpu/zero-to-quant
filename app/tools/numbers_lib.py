"""Shared number-check helper for level number scripts (ENGINE-BACKLOG 573). Pure standard library.

Bank files (B2-E4): `Bank("statistics-1")` loads content/bank/<file id>.json with the same expect, claim, claim_text, stated, check_wrongs and
report. A path names an item by its id: bank.expect("items[beta-binomial-posterior-mean].widget.answer", 0.642857) (the file argument is
optional: bank.expect(path, value) and bank.expect("statistics-1", path, value) both work; claim_text(path, phrase, ok) and stated(path, phrase, ok) take no file), and [*] fans out. Hidden tests of a code item are
checked by running its `solution` in CPython in the script itself; check_wrongs reads numeric wrong[] values as for a level.

Use from docs/reports/<course>-L<n>-numbers.py:
    import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'app', 'tools'))
    from numbers_lib import Level
    lv = Level("odes", 3)                       # every lesson, the review, the homework and the problem set of that level
    lv.expect("l10", "screens[3].widget.answer", 3)               # numeric token equal to 3 in a string or number
    lv.expect("l10", "screens[3].prose", -0.5)                    # a minus may be written "-" or U+2212
    lv.expect("review", "items[2].widget.options[1].why", 1214)   # "1,214", "£1,214" and "$1{,}214$" all match
    lv.expect("l11", "screens[5].widget.wrong[0].value", 0.25, fmt="{:.2f}")   # fmt: the exact text that must appear
    lv.expect("l12", "screens[2]", 7)                             # a path that ends on an object or list searches every string below it
    lv.expect("l12", "screens[*].prose", 7)                       # [*] joins every element
    lv.check_wrongs()                                             # every numeric wrong[].value: outside the answer tolerance (ENGINE-BACKLOG 582)
    lv.claim(abs(a - b) < 0.01, "a and b agree")                  # a claim that is not one number: an inequality, a coverage statement (ENGINE-BACKLOG 606)
    lv.stated("l7", "screens[2].prose", "is always positive", x > 0)    # tied to its wording: fails while the sentence is in the text and false, passes once reworded
    lv.claim_text("l7", "screens[2].prose", "phrase", ok, "label")      # the same with your own label
    lv.report()                                                   # prints the count, exits 1 on any failure
`file` is a lesson id or a unique prefix ("l10"), "review", "homework" or "problems" (the level's problems-<n>.json, when it exists:
paths read items[i].parts[j].widget...). `lv.text(file, path)` returns the string
(strings below an object or list are joined with newlines) for ad-hoc checks. Without `fmt` a number matches any token
of equal value after normalisation (thousands commas, currency signs, LaTeX spacing and braces, U+2212, trailing zeros; a LaTeX fraction \\tfrac{3}{4}, \\frac{1}{2} or \\frac12 matches its value and its integers);
a string value must appear verbatim in the raw or the normalised text.
`lv.check_wrongs(file=None)` (one file, or the whole level) walks every widget or table cell with a numeric answer and a
wrong[] list. Each numeric wrong value must lie outside the answer's tolerance, by the validator's rule 581 and grade.js within()
(abs: |v-a| <= abs; rel: |v-a| <= |a|*rel; a wrong entry's own tol widens it, default abs 1e-9); a hit is a failed check. It also
reads the feedback.byKey text for that wrong id on the same screen or item and prints "check by hand" (not a failure) when the
text states numbers and none equals the wrong value: a count by default, the lines with verbose=True or --verbose. Call it in every number script, before report().
"""
import json
import os
import re
import sys

COURSES = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'content', 'courses')
BANK = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'content', 'bank')
_PART = re.compile(r'([A-Za-z_][\w-]*)|\[([^\]]+)\]')   # a key may hold a hyphen: feedback.byKey.test-3 (ENGINE-BACKLOG 606)


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
            elif not idx.isdigit():                       # [<item id>]: the list element whose "id" it is (bank files, B2-E4)
                hit = [x for x in n if isinstance(x, dict) and x.get('id') == idx] if isinstance(n, list) else []
                if len(hit) != 1:
                    raise KeyError(f'no element with id "{idx}" in {path}')
                nxt.append(hit[0])
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
        for fid in list(lv.get('lessons', [])) + [lv.get('review'), lv.get('homework'), f'problems-{n}']:   # problems-<n>.json when the level has a set
            p = os.path.join(d, f'{fid}.json') if fid else None
            if p and os.path.exists(p):
                with open(p, encoding='utf8') as f:
                    self.files[fid] = json.load(f)
        if not self.files:
            raise SystemExit(f'numbers_lib: no files for {course} level {n}')

    def _file(self, ref):
        if ref in ('review', 'homework', 'problems'):
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

    def claim(self, ok, label, note=''):
        """Record a claim that is not a single number (an inequality, a coverage statement, what a chart shows)."""
        return self._rec(bool(ok), label, '' if ok else (note or 'claim is false'))

    def claim_text(self, ref, path, phrase, ok, label=None):
        """A claim tied to its wording: while `phrase` is in the text, `ok` must be true; once a fix rewords it away the check passes,
        so a number script exits 0 after the content is fixed."""
        label = label or f'{ref} {path} says {phrase!r}'
        try:
            txt = self.text(ref, path)
        except KeyError as e:
            return self._rec(False, label, str(e))
        if phrase not in txt and phrase not in normalise(txt):
            return self._rec(True, label, 'wording no longer in the text')
        return self._rec(bool(ok), label, '' if ok else f'the sentence is still in the text and is false: {phrase!r}')

    def stated(self, ref, path, phrase, ok):
        return self.claim_text(ref, path, phrase, ok)

    def check_wrongs(self, file=None, verbose=False):
        """Assert no numeric wrong[] value lies inside its answer's tolerance; count the byKey texts that state other numbers
        ("check by hand": usually a line that states the working, not the wrong value) and print them only with verbose=True,
        `--verbose` or `-v` on the script's command line."""
        verbose = verbose or '--verbose' in sys.argv or '-v' in sys.argv
        def half(a, t):
            t = {'abs': t} if isinstance(t, (int, float)) else (t or {})
            return abs(a) * t['rel'] + 1e-12 if t.get('rel') is not None else (t.get('abs') or 0) + 1e-9
        hand = []

        def visit(node, path, fb, fid):
            if isinstance(node, list):
                for i, x in enumerate(node):
                    visit(x, f'{path}[{i}]', fb, fid)
                return
            if not isinstance(node, dict):
                return
            if isinstance(node.get('feedback'), dict) and isinstance(node['feedback'].get('byKey'), dict):
                fb = node['feedback']['byKey']
            ans, wr = node.get('answer'), node.get('wrong')
            if isinstance(ans, (int, float)) and not isinstance(ans, bool) and isinstance(wr, list):
                ha = half(ans, node.get('tol'))
                for i, w in enumerate(wr):
                    v = w.get('value') if isinstance(w, dict) else None
                    if not isinstance(v, (int, float)) or isinstance(v, bool):
                        continue
                    label = f'{fid} {path}.wrong[{i}] "{w.get("id")}" = {v!r} outside answer {ans!r} tolerance'
                    d = abs(v - ans)
                    if d <= ha:
                        self._rec(False, label, f'inside the tolerance +-{ha:.6g}: graded correct, never fires')
                    elif d <= ha + half(v, w.get('tol') or {'abs': 1e-9}):
                        self._rec(False, label, 'its own tolerance reaches the answer tolerance')
                    else:
                        self._rec(True, label, '')
                    t = fb.get(w.get('id')) if fb else None
                    if isinstance(t, str):
                        nums = _numbers(t)
                        if nums and not any(abs(x - v) <= 1e-9 * max(1.0, abs(v)) for x in nums):
                            hand.append(f'check by hand: {fid} byKey "{w.get("id")}" states {sorted(set(nums))[:6]} but wrong value is {v!r}')
            for k, x in node.items():
                visit(x, f'{path}.{k}' if path else k, fb, fid)
        for fid, doc in self.files.items():
            if file is None or fid == self._file(file)[0]:
                visit(doc, '', None, fid)
        if verbose:
            for h in hand:
                print(h)
        elif hand:
            print(f'check by hand: {len(hand)} byKey line(s) state numbers other than the wrong value (not failures; rerun with --verbose to list them)')
        return hand

    def _rec(self, ok, label, note):
        self.results.append((ok, label, note))
        print(f"{'ok ' if ok else 'BAD'} {label}" + (f'  ({note})' if note else ''))
        return ok

    def report(self):
        bad = [r for r in self.results if not r[0]]
        print(f'numbers_lib: {len(self.results) - len(bad)} of {len(self.results)} checks passed')
        if bad:
            sys.exit(1)


class Bank(Level):
    """One interview bank file, content/bank/<file id>.json (B2-E4). Paths read items[<item id>].widget.answer; item parts read
    items[<id>].parts[<n>].widget...; the file argument of expect and text may be left out, and claim_text and stated take none."""

    def __init__(self, file_id):
        self.course, self.n, self.id, self.results = 'bank', 0, file_id, []
        p = os.path.join(BANK, f'{file_id}.json')
        if not os.path.exists(p):
            raise SystemExit(f'numbers_lib: no bank file {file_id} ({p})')
        with open(p, encoding='utf8') as f:
            self.files = {file_id: json.load(f)}

    def _file(self, ref):
        if ref in (None, self.id, 'bank'):
            return self.id, self.files[self.id]
        raise KeyError(f'file "{ref}" is not the bank file {self.id}')

    def expect(self, *a, fmt=None):
        ref, path, value = a if len(a) == 3 else (None, *a)
        return super().expect(ref, path, value, fmt=fmt)

    def text(self, *a):
        ref, path = a if len(a) == 2 else (None, *a)
        return super().text(ref, path)

    def claim_text(self, path, phrase, ok, label=None):
        return Level.claim_text(self, None, path, phrase, ok, label)

    def stated(self, path, phrase, ok):
        return Level.claim_text(self, None, path, phrase, ok)
