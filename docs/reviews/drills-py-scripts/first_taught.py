"""Where is each construct a drill needs first shown in its course?
Run from the repo root: python docs/reviews/drills-py-scripts/first_taught.py
Prints, per course, token -> first file (in course order) whose text holds it."""
import json, re, os
ROOT = 'app/content/courses'
TOKENS = {
 'py-found': ['sorted(', '.sort(', 'divmod', 'round(', 'set(', ' & ', 'sum(', '] * ', ':,', ':02d', 'abs(', 'range(1, len', '.get(', 'csv.reader', 'DictReader', 'StringIO', '.strip()', 'zip(', 'yield', 'next(', 'raise ValueError', 'ZeroDivisionError', 'TypeError', 'except ValueError', 'continue', 'class ', '__init__', 'None', '-1, -1', 'is not', 'def '],
 'numpy-pandas': ['np.abs', 'flatnonzero', 'np.where', 'argmax', 'axis=1', 'ffill', 'limit=', 'read_csv', 'index_col', 'parse_dates', 'strftime', 'shift(', '[:, None]', 'np.newaxis', 'reshape', '.agg(', 'groupby', 'resample', 'W-FRI', '.first()', '.last()', 'dropna', 'merge(', 'outer', 'reset_index', 'fillna', 'fill_value', 'rolling', '.std(', 'ddof', '.where(', 'pct_change', '"ME"', "'ME'", 'index.month', 'sort_values', '.rename(', 'size', '.tolist()', '.copy()', 'np.asarray', ' & '],
 'plotting': ['cumprod', 'cummax', 'ax.hist', 'bins', 'set_ylim', 'scatter', 'drawdown', 'np.histogram', 'ax.bar', 'pivot', 'unstack', 'imshow', 'days since', 'under water', 'underwater'],
}


def order(course):
    c = json.load(open(f'{ROOT}/{course}/course.json'))
    ids = re.findall(r'"((?:l\d+|review|homework)[a-z0-9-]*)"', json.dumps(c))
    seen = []
    for i in ids:
        if i not in seen and os.path.exists(f'{ROOT}/{course}/{i}.json'):
            seen.append(i)
    return seen


for course, toks in TOKENS.items():
    ids = order(course)
    print('==', course, ' '.join(ids))
    texts = {i: json.dumps(json.load(open(f'{ROOT}/{course}/{i}.json')), ensure_ascii=False).replace('\\"', '"') for i in ids}
    for t in toks:
        first = next((i for i in ids if t in texts[i]), None)
        print(f'  {t!r:22} {first}')
