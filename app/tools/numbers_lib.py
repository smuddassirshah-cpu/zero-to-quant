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
    lv.slip("problems", "items[1].parts[2]", "inverted", ("printed", 59425.3), ("unrounded", 59424.9))   # every route of one slip inside its band, outside the key band (ENGINE-BACKLOG 1081)
    lv.check_slips()                                            # a wrong[] entry's optional "slip" expression must give its value (ENGINE-BACKLOG 1029)
    lv.claim(abs(a - b) < 0.01, "a and b agree")                # a claim that is not one number: an inequality, a coverage statement (ENGINE-BACKLOG 606)
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

Coverage (ENGINE-BACKLOG 1267): report() also lists every number in the level's on-screen text (prose, question, hints, explain, how, why, model answers, byKey
lines, summary, canvas labels, table cells; not code, years, list numbers, "lesson 3"-style ids, exponents or subscripts) that no check compared against. A number
is covered when an expect, check_wrongs (answers and wrong values), slip, claim(..., covers=[...]) or literal value equals it to its stated precision (a
trailing-zero integer to its last non-zero digit; "25%" also by value x 100; sign ignored). Default: print the count and the first five, never fail.
Strict: Level(course, n, coverage="strict") or ZQ_NUMBERS_STRICT=1 makes an uncovered number fail the run; coverage="off" skips it; --verbose lists them all.
    lv.literal("12,500", why="a round figure from the brief, not a computed result")   # a deliberately unchecked number; why is required
"""
import json
import math
import os
import re
import sys

COURSES = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'content', 'courses')
BANK = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'content', 'bank')
_PART = re.compile(r'([A-Za-z_][\w-]*)|\[([^\]]+)\]')   # a key may hold a hyphen: feedback.byKey.test-3 (ENGINE-BACKLOG 606)


_SLIP_NAMES = {'sqrt': math.sqrt, 'exp': math.exp, 'ln': math.log, 'log': math.log, 'log10': math.log10, 'abs': abs, 'pow': math.pow,
               'min': min, 'max': max, 'round': round, 'pi': math.pi, 'e': math.e}


def slip_eval(expr):
    """Evaluate the "slip" expression of a wrong[] entry (ENGINE-BACKLOG 1029): numbers, + - * / ^ ** ( ), the constants pi and e, and the functions
    sqrt, exp, ln, log (natural), log10, abs, pow, min, max, round: the same grammar as tools/validate.mjs. Returns a float, or None when it does not read."""
    t = str(expr).replace('^', '**')
    if not re.fullmatch(r'[\d\s.+\-*/(),A-Za-z_]*', t):
        return None
    if any(i not in _SLIP_NAMES for i in re.findall(r'[A-Za-z_][A-Za-z_0-9]*', t)):
        return None
    try:
        v = float(eval(t, {'__builtins__': {}}, dict(_SLIP_NAMES)))   # noqa: S307 (characters and names are whitelisted above)
    except Exception:
        return None
    return v if math.isfinite(v) else None


def _half(a, t):
    t = {'abs': t} if isinstance(t, (int, float)) else (t or {})
    return abs(a) * t['rel'] + 1e-12 if t.get('rel') is not None else (t.get('abs') or 0) + 1e-9


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


_CODE = re.compile(r'```.*?```|`[^`\n]*`', re.S)
_IDISH = re.compile(r'\b(?:lessons?|levels?|items?|screens?|parts?|problems?|steps?|hints?|homework|review)\s+\d+(?:\s*(?:and|,|to|-)\s*\d+)*', re.I)
_LISTNUM = re.compile(r'(?m)^[ \t]*\(?\d+[.)]\s')
_SCI = re.compile(r'(\d+(?:\.\d+)?)\s*(?:\\times|\\cdot|×)\s*10\^(-?\d+)')
_POW10 = re.compile(r'(?<![\w.])10\^(-?\d+)')
_SLASH = re.compile(r'(?<![\w./])(\d+)\s*/\s*(\d+)(?![\w./])')
_EXPSUB = re.compile(r'(?<![\w.])\d+(?:\.\d+)?\^\s*-?[\d.]+|\^\s*-?[\d.]+|_\d+')
_TEXT_KEYS = {'prose', 'question', 'text', 'hint', 'hints', 'explain', 'how', 'why', 'label', 'caption', 'title', 'generic', 'correct', 'byKey', 'summary',
              'ideas', 'trap', 'note', 'objectives', 'rows', 'prompt', 'model',
              'postlude', 'symptom', 'placeholder', 'unit', 'description'}
_TEXT_SKIP = {'id', 'kind', 'type', 'highlight', 'rung', 'values', 'ids', 'accept', 'tol', 'answer', 'wrong', 'starter', 'solution', 'tests', 'examples',
              'mutants', 'setup', 'call', 'expect', 'compare', 'source', 'code'}
_CANVAS_TEXT = {'caption', 'title', 'text'}      # axis, tick, node and frame labels are not claims
_ANSWER_PATHS = ('explain', 'hints', 'how', 'why', 'byKey', 'feedback', 'options', 'lines')


_WORDN = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10, 'twelve': 12}
_DEN = {'half': 2, 'halves': 2, 'third': 3, 'thirds': 3, 'quarter': 4, 'quarters': 4, 'fifth': 5, 'fifths': 5, 'tenth': 10, 'tenths': 10}
_WORDFRAC = re.compile(r'\b(a|one|two|three|four|five|three)\s+(half|halves|third|thirds|quarter|quarters|fifth|fifths|tenth|tenths)\b', re.I)
_WORDMULT = re.compile(r'\b(twice|thrice|double|doubles|doubled|triple|tripled|halved|(one|two|three|four|five|six|seven|eight|nine|ten|twelve)\s+times)\b', re.I)
_UNIT = re.compile(r'\s*(?:bits?|nats?|bytes?|ms|s\b|seconds?|secs?|minutes?|hours?|days?|hz|kb|mb|gb|kg|km|cm|pence|pounds?|percent|per\s+cent|x\b)', re.I)
_ARITH_BEFORE = re.compile(r'(?:[+*/=×÷]|\\times|\\cdot|\\div|\btimes|\bby|\bplus|\bminus|\bequals|\bis|\bgives?|\bmakes?|\btotal)\s*$|\s-\s*$', re.I)
_ARITH_AFTER = re.compile(r'\s*(?:[+*/=×÷]|\\times|\\cdot|\\div|\btimes\b|\s-\s)', re.I)


def _stated(s):
    """Numbers a learner reads in a string, as (value, tolerance, percent, shown, strong). `strong` marks the claims a reader checks: decimals, fractions, percentages,
    money, a number with a unit, a whole number in arithmetic, a whole number over 100, and words for fractions and multiples ("a third", "twice") converted to values.
    Other whole numbers are weak (by size, see Level.uncovered). Code, years, list numbers, "lesson 3" ids, exponents and subscripts are left out."""
    out = []
    s = _LISTNUM.sub(' ', _IDISH.sub(' ', _CODE.sub(' ', s)))
    s = re.sub(r'(?:£|\\pounds\s*)\s*(?=[\d.])', '\x01', s)

    def frac(m):
        a, b = (m.group(1), m.group(2)) if m.group(1) is not None else (m.group(3), m.group(4))
        try:
            x, y = float(normalise(a)), float(normalise(b))
            if y != 0:
                out.append((x / y, max(5e-4, 1e-3 * abs(x / y)), False, f'{a}/{b}', True))
        except ValueError:
            pass
        return ' '

    def val(m, v, tol, shown=None):
        out.append((v, tol, False, shown or m.group(0), True))
        return ' '

    def words(m):
        w = m.group(0).lower()
        if m.re is _WORDFRAC:
            n = 1 if m.group(1).lower() in ('a', 'one') else _WORDN.get(m.group(1).lower(), 3 if m.group(1).lower() == 'three' else 2)
            return val(m, n / _DEN[m.group(2).lower()], 5e-4)
        k = {'twice': 2, 'double': 2, 'doubles': 2, 'doubled': 2, 'thrice': 3, 'triple': 3, 'tripled': 3, 'halved': 0.5}.get(w)
        return val(m, k if k else _WORDN[m.group(2).lower()], 1e-9)
    s = _WORDFRAC.sub(words, s)
    s = _WORDMULT.sub(words, s)
    s = normalise(_FRAC.sub(frac, s))
    s = _SCI.sub(lambda m: val(m, float(m.group(1)) * 10 ** int(m.group(2)), 1e-3 * float(m.group(1)) * 10 ** int(m.group(2))), s)
    s = _POW10.sub(lambda m: val(m, 10.0 ** int(m.group(1)), 1e-9), s)
    s = _SLASH.sub(lambda m: val(m, int(m.group(1)) / int(m.group(2)), max(5e-4, 1e-3 * int(m.group(1)) / int(m.group(2)))) if int(m.group(2)) else ' ', s)
    s = _EXPSUB.sub(' ', s)
    for m in _NUM.finditer(s):
        raw = m.group(0).rstrip('.')
        if re.fullmatch(r'-?(?:1[5-9]\d\d|20\d\d)', raw):
            continue                                              # a year
        try:
            v = float(raw)
        except ValueError:
            continue
        d = raw.lstrip('-')
        whole = re.fullmatch(r'\d+', d) is not None
        if re.fullmatch(r'\d+\.\d+', d):
            tol = 0.5 * 10 ** -len(d.split('.')[1])
        elif whole:
            tol = 0.5 * 10 ** max(len(d) - len(d.rstrip('0')) - 1, 0)   # 12,500 reads to the hundred, 11,000 to the thousand
        else:
            tol = 1e-9 * max(1.0, abs(v))
        after, before = s[m.end():m.end() + 14], s[max(0, m.start() - 14):m.start() + (1 if raw.startswith('-') else 0)]
        pct = after.lstrip().startswith(('%', '\\%'))
        strong = (not whole) or pct or abs(v) > 100 or before.endswith('\x01') or bool(_UNIT.match(after)) \
            or bool(_ARITH_BEFORE.search(before)) or bool(_ARITH_AFTER.match(after))
        out.append((v, tol + 1e-9, pct, raw, strong))
    return out


def _text_strings(node, path, fid, out, text=False, canvas=False):
    """Collect (file, path, string) for every on-screen string: under a text key, minus code, answers and ids; a canvas contributes only its label keys."""
    if isinstance(node, str):
        if text:
            out.append((fid, path, node))
    elif isinstance(node, list):
        for i, x in enumerate(node):
            _text_strings(x, f'{path}[{i}]', fid, out, text, canvas)
    elif isinstance(node, dict):
        for k, x in node.items():
            if k in _TEXT_SKIP:
                continue
            p = f'{path}.{k}' if path else k
            if k == 'canvas':
                _text_strings(x, p, fid, out, False, True)
            elif canvas:
                _text_strings(x, p, fid, out, text or k in _CANVAS_TEXT, True)
            else:
                _text_strings(x, p, fid, out, text or k in _TEXT_KEYS, False)


class Level:
    def __init__(self, course, n, coverage=None):
        self.course, self.n, self.files, self.results, self.coverage = course, n, {}, [], coverage
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

    def _cv(self):
        return self.__dict__.setdefault('_cvals', [])

    def _cover(self, *vals, at=None):
        """Record values some check compared against (numbers, or strings whose numbers count). `at` is (file id, path): the value then covers that screen or item
        only (a path that does not name one, such as "screens" or "screens[*]", covers the file); without it the value covers the whole level."""
        fid = unit = None
        if at:
            fid = at[0]
            m = re.match(r'(?:screens|items|quiz)\[(\d+)\]', at[1] or '')
            unit = None                    # file level: a screen-level match was measured and tripled the uncovered counts
        for v in vals:
            if isinstance(v, str):
                self._cv().extend((x[0], fid, unit) for x in _stated(v))
            elif isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v):
                self._cv().append((float(v), fid, unit))

    def literal(self, value, why):
        """ENGINE-BACKLOG 1267: mark a number (or the numbers of a string) as deliberately unchecked; `why` is required and listed by report()."""
        if not isinstance(why, str) or len(why.strip()) < 8:
            raise ValueError('literal(): why must say why the number is left unchecked')
        self._cover(value)
        self.__dict__.setdefault('_lits', []).append((value, why))

    def uncovered(self):
        """Every on-screen number no check compared against: a list of (file, path, shown)."""
        strs = []
        for fid, doc in self.files.items():
            _text_strings(doc, '', fid, strs)
        import bisect
        cv, seen, out = {}, set(), []
        for v, f, u in self._cv():
            cv.setdefault((f, u), []).append(abs(v))
            cv.setdefault('all', []).append(abs(v))
        for lst in cv.values():
            lst.sort()
        for fid, path, text in strs:
            reading = any(k in path for k in _ANSWER_PATHS)
            um = re.match(r'(?:screens|items|quiz)\[\d+\]', path)
            local = [cv[k] for k in ((fid, None), (None, None)) if k in cv]          # a fraction or a word ("a third") must be covered in its own file
            for v, tol, pct, shown, strong in _stated(text):
                if not strong and not (reading and abs(v) > 12):    # a bare whole number: prose skips up to 100, explain-class text up to 12
                    continue
                a = abs(v)
                hit = False
                lists = local if re.search(r'[/a-z]', shown) else [cv.get('all', [])]       # a plain number may be covered anywhere in the level
                for t in ((a, a / 100) if pct else (a,)):
                    for lst in lists:
                        i = bisect.bisect_left(lst, t - tol)
                        if i < len(lst) and lst[i] <= t + tol:
                            hit = True
                key = (fid, um.group(0) if um else path, round(a, 9))        # one number per screen or item: the same figure in a hint, explain and byKey is read once
                if not hit and key not in seen:
                    seen.add(key)
                    out.append((fid, path, shown))
        return out

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
            self._cover(value, at=(self._file(ref)[0], path))
        except KeyError:
            self._cover(value)
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

    def claim(self, ok, label, note='', covers=()):
        """Record a claim that is not a single number (an inequality, a coverage statement, what a chart shows). `covers`: the numbers the claim compares (coverage, 1267)."""
        self._cover(*covers)
        return self._rec(bool(ok), label, '' if ok else (note or 'claim is false'))

    def claim_text(self, ref, path, phrase, ok, label=None, covers=()):
        """A claim tied to its wording: while `phrase` is in the text, `ok` must be true; once a fix rewords it away the check passes,
        so a number script exits 0 after the content is fixed."""
        label = label or f'{ref} {path} says {phrase!r}'
        self._cover(*covers)
        try:
            txt = self.text(ref, path)
        except KeyError as e:
            return self._rec(False, label, str(e))
        if phrase not in txt and phrase not in normalise(txt):
            return self._rec(True, label, 'wording no longer in the text')
        return self._rec(bool(ok), label, '' if ok else f'the sentence is still in the text and is false: {phrase!r}')

    def stated(self, ref, path, phrase, ok, covers=()):
        return self.claim_text(ref, path, phrase, ok, covers=covers)

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
                self._cover(ans, *[w.get('value') for w in wr if isinstance(w, dict)], at=(fid, path))
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

    def slip(self, ref, path, wid, *routes):
        """ENGINE-BACKLOG 1081: one slip as a list of routes. `path` selects the part (or the widget) holding the numeric answer, e.g. "items[1].parts[2]"; `wid` is the id of its wrong[]
        entry; each route is a value a learner who makes the slip reaches (from the stated inputs, from the unrounded inputs, from the printed error: a number, or a (label, number) pair).
        Every route must lie inside the slip's band and outside the key's band, the two bands must not meet, and a part must carry a byKey line for the id.
        Pattern: lv.slip("problems", "items[1].parts[2]", "inverted", ("printed", 59425.3), ("unrounded", 59424.9))"""
        label = f'{ref} {path} slip "{wid}"'
        try:
            node = _walk(self._file(ref)[1], path)
        except KeyError as e:
            return self._rec(False, label, str(e))
        if len(node) != 1:
            return self._rec(False, label, f'the path selects {len(node)} nodes, not one')
        part = node[0]
        w = part.get('widget') if isinstance(part, dict) and isinstance(part.get('widget'), dict) else part
        ans, ent = (w.get('answer') if isinstance(w, dict) else None), [x for x in (w.get('wrong') or []) if isinstance(x, dict) and x.get('id') == wid] if isinstance(w, dict) else []
        if not isinstance(ans, (int, float)) or isinstance(ans, bool) or len(ent) != 1 or not isinstance(ent[0].get('value'), (int, float)):
            return self._rec(False, label, 'no numeric answer, or no single numeric wrong entry with this id')
        e, ha = ent[0], _half(ans, w.get('tol'))
        self._cover(ans, e['value'], *[r[1] if isinstance(r, tuple) else r for r in routes], at=(self._file(ref)[0], path))
        hs, ok = _half(e['value'], e.get('tol') or {'abs': 1e-9}), True
        ok &= self._rec(abs(e['value'] - ans) > ha + hs, f'{label}: band apart from the key band', f'the slip band {e["value"]!r} +-{hs:.6g} meets the key band {ans!r} +-{ha:.6g}')
        fb = part.get('feedback') if isinstance(part, dict) else None
        if isinstance(fb, dict):
            ok &= self._rec(isinstance((fb.get('byKey') or {}).get(wid), str), f'{label}: byKey line', 'no feedback.byKey line for this id')
        for r in routes:
            name, v = r if isinstance(r, tuple) else ('route', r)
            ok &= self._rec(abs(v - e['value']) <= hs, f'{label}: {name} {v:.6g} inside its band', f'misses the slip band {e["value"]!r} +-{hs:.6g}')
            ok &= self._rec(abs(v - ans) > ha, f'{label}: {name} {v:.6g} outside the key band', f'lies inside the key band {ans!r} +-{ha:.6g}: graded correct')
        return bool(ok)

    def check_slips(self, file=None):
        """ENGINE-BACKLOG 1029: every wrong[] entry that carries a "slip" expression must evaluate to its value (within its band, or once rounded to the value's own
        decimals). Same grammar as the validator's [slip-expr]; call it in a number script beside check_wrongs. Returns the number of entries checked."""
        n = [0]

        def visit(node, path, fid):
            if isinstance(node, list):
                for i, x in enumerate(node):
                    visit(x, f'{path}[{i}]', fid)
                return
            if not isinstance(node, dict):
                return
            wr = node.get('wrong')
            if isinstance(wr, list):
                for i, w in enumerate(wr):
                    if not isinstance(w, dict) or 'slip' not in w:
                        continue
                    n[0] += 1
                    label = f'{fid} {path}.wrong[{i}] "{w.get("id")}" slip {w["slip"]!r}'
                    v, val = (slip_eval(w['slip']) if isinstance(w['slip'], str) else None), w.get('value')
                    if v is None or not isinstance(val, (int, float)) or isinstance(val, bool):
                        self._rec(False, label, 'does not read as arithmetic, or the entry has no numeric value')
                        continue
                    r = repr(val)
                    dp = len(r.split('.')[1]) if '.' in r and 'e' not in r else 0
                    ok = abs(v - val) <= _half(val, w.get('tol') or {'abs': 1e-9}) or abs(round(v, dp) - val) <= 1e-9 * max(1.0, abs(val))
                    self._rec(ok, label, '' if ok else f'works out to {v:.8g}, not the value {val!r}')
            for k, x in node.items():
                visit(x, f'{path}.{k}' if path else k, fid)
        for fid, doc in self.files.items():
            if file is None or fid == self._file(file)[0]:
                visit(doc, '', fid)
        return n[0]

    def _rec(self, ok, label, note):
        self.results.append((ok, label, note))
        print(f"{'ok ' if ok else 'BAD'} {label}" + (f'  ({note})' if note else ''))
        return ok

    def _coverage(self):
        mode = getattr(self, 'coverage', None) or ('strict' if os.environ.get('ZQ_NUMBERS_STRICT') == '1' else 'warn')
        if mode == 'off':
            return
        miss = self.uncovered()
        lits = self.__dict__.get('_lits', [])
        verbose = '--verbose' in sys.argv or '-v' in sys.argv
        print(f'numbers_lib: coverage: {len(miss)} on-screen number(s) no check compared against' + (f', {len(lits)} marked literal' if lits else '') + (' (strict)' if mode == 'strict' else ''))
        for fid, path, shown in (miss if verbose or mode == 'strict' else miss[:5]):
            print(f'  uncovered {fid} {path}: {shown}')
        if miss and not verbose and mode != 'strict' and len(miss) > 5:
            print(f'  ... {len(miss) - 5} more (--verbose lists them; lv.literal(value, why=...) marks one as deliberate)')
        if miss and mode == 'strict':
            self.results.append((False, f'coverage: {len(miss)} uncovered number(s)', 'check each with expect, or mark it with literal()'))

    def report(self):
        self._coverage()
        bad = [r for r in self.results if not r[0]]
        print(f'numbers_lib: {len(self.results) - len(bad)} of {len(self.results)} checks passed')
        if bad:
            sys.exit(1)


class Bank(Level):
    """One interview bank file, content/bank/<file id>.json (B2-E4). Paths read items[<item id>].widget.answer; item parts read
    items[<id>].parts[<n>].widget...; the file argument of expect and text may be left out, and claim_text and stated take none."""

    def __init__(self, file_id, coverage=None):
        self.course, self.n, self.id, self.results, self.coverage = 'bank', 0, file_id, [], coverage
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
