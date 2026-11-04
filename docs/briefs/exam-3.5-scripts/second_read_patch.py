"""Second-read fixes for topic-3.5.json (4 Nov 2026), applied after build.py has written the file.

build.py calls apply(path).  It holds the changes the second reader and the answer check asked for:
fresh content for the two duplicate items, renamed functions, stronger code tests, wider tolerances,
an unambiguous order item, the rq-case tag, an id rename and trimmed code paces.  Every number is asserted.
"""
import json
from fractions import Fraction as F
import numpy as np


def apply(T):
  s = open(T).read()
  s = s.replace('newest_first', 'latest_values').replace('best_window', 'peak_window_total')
  d = json.loads(s)
  I = {it['id']: it for it in d['items']}


  def opt(it, oid):
      return next(o for o in it['widget']['options'] if o['id'] == oid)


  # ---------------------------------------------------------------- item 4: six looks
  assert F(5, 100) / 6 == F(1, 120) and abs(0.05 / 6 - 0.008333333) < 1e-9
  assert F(6) * F(12, 1000) == F(72, 1000) and 0.012 > 0.05 / 6 and 6 * 0.012 > 0.05
  it = I['e-eight-looks']
  it['id'] = 'e-six-looks'
  it['title'] = 'The best of six signals'
  it['prose'] = 'You test six candidate signals on the same history. The best has $p = 0.012$. You want the chance of any false positive across all six to stay at 5%.'
  opt(it, 'a')['text'] = 'No. It must beat $0.05/6 \\approx 0.0083$, and it does not.'
  opt(it, 'b')['text'] = 'Yes. 0.012 is below 0.05, so it passes the test.'
  opt(it, 'b')['why'] = 'You compared with 0.05 as if you had tried one signal. Six looks need a stricter bar.'
  opt(it, 'c')['text'] = 'No. There is only a 1.2% chance that the signal is real.'
  opt(it, 'd')['text'] = 'It cannot be judged until you see the other five $p$-values.'
  it['feedback']['correct'] = 'Each of six tests must clear $0.05/6 \\approx 0.0083$. The $p$ of 0.012 does not.'
  it['explain']['text'] = 'With six looks, each test must beat $0.05/6 \\approx 0.0083$ to keep the chance of any false positive at 5%. The best $p$ of 0.012 does not. The same test in another form: the corrected $p$ is $6 \\times 0.012 = 0.072$, above 0.05.'

  # ---------------------------------------------------------------- item 18: wording
  it = I['e-two-statements']
  it['explain']['text'] = 'If B reads 0, A writes 2 and then B writes 0, the final value is 0. Other orders give 2 and 6, so 0, 2 and 6 are all possible, and 8 is not. An atomic removes the undefined behaviour, but only a mutex per statement forces 2 or 6.'

  # ---------------------------------------------------------------- item 19: unambiguous order
  it = I['e-weekly-hit-case']
  L = {l['id']: l for l in it['widget']['lines']}
  L['s1']['text'] = "Define the label first: the stock's return beats the index's over the next five days"
  L['s2']['text'] = "Build features known at each Friday's close, then split by date with a gap of five days"
  L['s3']['text'] = 'On the training weeks, find the baseline hit rate by always guessing the more common label'
  L['s4']['text'] = 'On the training weeks, fit a simple model'
  L['s5']['text'] = 'Compare the two hit rates on the test weeks'
  L['s6']['text'] = 'Report the gap with an interval and the weeks where it fails'
  it['widget']['same'] = [['s3', 's4']]
  it['feedback']['correct'] = 'Define the label, build features and split with a gap, then find the baseline and fit in either order. Compare and report.'
  it['feedback']['generic'] = 'A label that looks five days ahead overlaps its neighbours, so the split needs a gap.'
  it['explain']['text'] = 'The label looks five days ahead, so train and test weeks overlap unless a gap separates them. The baseline and the model both use the training weeks, so either can come first. Compare them on the test weeks, then report the gap with its uncertainty.'

  # ---------------------------------------------------------------- item 20: replaced
  it = I['e-two-singles-steps']
  new20 = {
      'id': 'e-next-higher-steps', 'difficulty': 3, 'skills': ['ci-patterns'], 'tags': ['price-stack-pass'], 'pace': 150,
      'title': 'The next higher price',
      'prose': 'Daily closing prices sit in a list. For each day we want the next later day with a higher close, in one pass over the list.',
      'question': 'Put the steps in order. Leave out the two that do not belong.',
      'widget': {
          'kind': 'order',
          'lines': [
              {'id': 's1', 'text': 'Start with an empty stack of days still waiting for a higher close'},
              {'id': 's2', 'text': 'For each day, pop every waiting day with a lower close and record this day as its answer'},
              {'id': 's3', 'text': 'Push the new day onto the stack'},
              {'id': 's4', 'text': 'After the last day, mark the days still on the stack as having no higher close'},
              {'id': 'x1', 'text': 'Compare each day with every later day and stop at the first higher close',
               'why': 'That gives the right answers but takes quadratic time. The stack touches each day once.'},
              {'id': 'x2', 'text': 'Push the new day first, then pop the days with a lower close',
               'why': 'The new day would sit on top and block the pops, so the lower days never leave.'},
          ],
          'answer': ['s1', 's2', 's3', 's4'],
          'distractors': ['x1', 'x2'],
      },
      'feedback': {
          'correct': 'Start empty, pop and record, push, then mark what is left.',
          'generic': 'Ask when a day leaves the stack, and which days are still on it at the end.',
      },
      'explain': {'text': 'A day waits on the stack until a higher close arrives. Each day is pushed once and popped at most once, so the pass is linear. Days still waiting at the end have no higher close.'},
  }
  # hand check: closes 5, 3, 4, 7: 3 -> 4, 5 -> 7, 4 -> 7, 7 -> none
  assert [next((j for j in range(i + 1, 4) if [5, 3, 4, 7][j] > [5, 3, 4, 7][i]), None) for i in range(4)] == [3, 2, 3, None]
  d['items'][d['items'].index(it)] = new20
  I['e-next-higher-steps'] = new20

  # ---------------------------------------------------------------- item 16 and 25: tolerances
  it = I['e-first-component']
  assert round(8 / 11, 4) == 0.7273 and abs(0.7273 - 0.73) < 0.005 and abs(0.7273 - 0.6364) > 0.005
  it['question'] = 'What share of the total variance does the first principal component carry? Give one decimal place.'
  it['widget']['tol'] = {'abs': 0.005}
  it['widget']['placeholder'] = 'a percentage, one decimal place'
  it['widget']['accept'] = '72.7% (within 0.5 points)'
  it = I['e-persistence-gain']
  assert F(1) - F(256, 100) / F(32, 10) == F(1, 5)
  it['widget']['tol'] = {'abs': 0.005}
  it['widget']['accept'] = '20% (within 0.5 points)'

  # ---------------------------------------------------------------- item 21: rename id
  I['e-sixty-five-minutes']['id'] = 'e-seventy-minutes'

  # ---------------------------------------------------------------- item 28: skills
  I['e-online-slope']['skills'] = ['rq-data', 'rq-linalg', 'rq-case']

  # ---------------------------------------------------------------- pace of code items
  for iid, p in (('e-active-symbols', 360), ('e-costliest-desk', 360), ('e-newest-first', 450)):
      I[iid]['pace'] = p

  # ---------------------------------------------------------------- item 27: end-point slope test
  xs = np.array([1, 2, 3, 4])
  sp = np.polyfit(xs, [0, 9, 9, 6], 1)[0]
  sq = np.polyfit(xs, [0, 1, 7, 5], 1)[0]
  assert abs(sp - 1.8) < 1e-12 and abs(sq - 2.1) < 1e-12 and sq > sp          # least squares picks q
  assert (6 - 0) / 3 == 2.0 and abs((5 - 0) / 3 - 1.6667) < 1e-3 and 2.0 > 5 / 3  # end points pick p
  # exact, as Fractions
  def slope(ys):
      n = 4; sx = 10; sxx = 30
      sy = sum(ys); sxy = sum(x * y for x, y in zip([1, 2, 3, 4], ys))
      return F(n * sxy - sx * sy, n * sxx - sx * sx)
  assert slope([0, 9, 9, 6]) == F(9, 5) and slope([0, 1, 7, 5]) == F(21, 10)
  it = I['e-costliest-desk']
  it['widget']['tests'].append({
      'call': "costliest_desk(pd.DataFrame({'desk': ['p'] * 4 + ['q'] * 4, 'size': [1, 2, 3, 4] * 2, 'cost': [0, 9, 9, 6, 0, 1, 7, 5]}), 4)",
      'expect': "'q'", 'compare': 'equal'})
  it['widget']['how'] = 'Check runs 8 hidden tests. They try two `min_rows` limits and no qualifying desk. They also try an empty frame, one distinct size, all slopes negative and interleaved rows. One test has end points that point to the wrong desk. Each answer must equal the expected name or `None`.'

  # ---------------------------------------------------------------- item 30: capacity cap and k above held count
  it = I['e-newest-first']
  tests = it['widget']['tests']
  t3 = tests[2]
  assert t3['args'][1:] == [8, 8] and len(t3['args'][0]) == 20
  t3['args'][2] = 12   # k above the 8 held after the ring has wrapped
  assert t3['expect'] == [20, 19, 18, 17, 16, 15, 14, 13]
  types = ['std::vector<int>', 'int', 'int']
  new_t = {'call': 'latest_values', 'args': [list(range(1, 11)), 4, 6], 'types': types, 'expect': [10, 9, 8, 7], 'compare': 'equal'}
  tests.insert(4, new_t)
  it['widget']['how'] = 'Check runs 7 hidden tests. They cover a ring that wraps, fewer values than `k` and a capacity of 1. Two tests use a `k` above the capacity. They also run 300 pushes through 32 slots and an empty list. A wrong mask or a missing capacity cap fails them.'

  d['items'] = d['items']

  # ---------------------------------------------------------------- sentences of 20 words, split or trimmed
  def subst(o, old, new):
      n = 0
      if isinstance(o, dict):
          for k, v in o.items():
              if isinstance(v, str) and old in v:
                  o[k] = v.replace(old, new); n += 1
              else:
                  n += subst(v, old, new)
      elif isinstance(o, list):
          for i, v in enumerate(o):
              if isinstance(v, str) and old in v:
                  o[i] = v.replace(old, new); n += 1
              else:
                  n += subst(v, old, new)
      return n

  for old, new in [
      ("A `get` or a `put` of a stored key, at steps 5 and 6, moves it to the newest end.", "A `get` or `put` of a stored key at steps 5 and 6 moves it to the newest end."),
      ("A gross edge of 4 basis points a trade is lost to costs of 5 basis points a round trip.", "A gross edge of 4 basis points is lost to costs of 5 basis points a round trip."),
      ("should return the largest sum of $k$ consecutive values, or `None` when the list has fewer than $k$ values.", "should return the largest sum of $k$ consecutive values. It should return `None` when the list has fewer than $k$ values."),
      ("They cover the window edge, a repeated symbol, a symbol that returns, an idle tool and trades at one time.", "They cover the window edge, a repeated symbol, a returning symbol, an idle tool and trades at one time."),
      ("Use the nearest-rank rule: the $p$th percentile", "Use the nearest-rank rule. The $p$th percentile"),
  ]:
      assert subst(d, old, new) == 1, old

  open(T, 'w').write(json.dumps(d, indent=2, ensure_ascii=False) + '\n')
  return d
