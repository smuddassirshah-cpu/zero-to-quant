"""Per lesson of each level, how often each idea a set leans on appears (all strings of the lesson file).
A zero row for a whole level is an idea the set uses and the level does not teach; the reader then looked wider.

Usage (repo root): python3 docs/reviews/problems-0.2-a-scripts/taught.py
"""
import glob
import json
import re

IDEAS = {
    ('equations', 1): {
        'expression from a story': r'in terms of|[Ww]rite an expression|expression for',
        'like terms': r'like terms',
        'expand, negative multiplier': r'-\s?\d\(|minus sign|taking away a negative|- \(',
        'decimal coefficient': r'\d\.\d+[a-z]\b',
        'letter times itself is a square': r'[a-z] \\times [a-z]|\^2',
        'factorise fully / HCF': r'highest common factor|[Ff]actorise fully|common factor',
        'take a letter out': r'[a-z]\(\d*[a-z] ?[+-]',
        'substitute': r'[Ss]ubstitut|put .* in for',
        'equal for every value': r'for every|always equal|any value|every value|identit',
    },
    ('equations', 2): {
        'form an equation': r'[Ww]rite an equation|equation for|as an equation',
        'two-step solve, reverse order': r'reverse order|[Uu]ndo',
        'unknown on both sides': r'both sides',
        'clear fractions, every term': r'every term|[Mm]ultiply (both sides|every|each)',
        'top of a fraction in a bracket': r'bracket',
        'clear decimals': r'clear the decimals|by 100\b|by 1000|times 100',
        'percentage as a decimal': r'0\.0\d|\d%|per cent',
        'round down in context': r'round(s|ed)? down|whole number of|largest whole|at most',
        'negative solution / dividing negatives': r'negative',
    },
    ('equations', 3): {
        'at least / at most / more than': r'at least|at most|more than|no more than',
        'filled and hollow dots': r'[Ff]illed|[Hh]ollow',
        'reverse the sign on a negative': r'revers|flip',
        'double inequality, all three parts': r'three parts|double inequalit|both rules|all three',
        'count the whole numbers': r'whole numbers?|integers?',
        'change the subject': r'the subject',
        'subject appears twice, factor out': r'appears twice|take .* out as a factor|common factor',
        'inequality typed or written by the learner': r'"kind": ?"expression"',
    },
    ('functions', 1): {
        'function notation f(x)': r'[a-zA-Z]\(\d+\)',
        'rule from a table, step not 1': r'each row|per row|step of|climb',
        'find c from one row': r'solve for \$?c|\+ c\b',
        'undo the rule (input from output)': r'[Uu]ndo|backwards|reverse',
        'domain': r'[Dd]omain',
        'range': r'\b[Rr]ange',
        'one output for each input': r'one output|two outputs|exactly one',
        'square has two inputs / plus or minus': r'\\pm|two inputs|both -?\d+ and|squared is positive|\(-\d+\)\^2',
        'range of a curve needs the turning value': r'highest point|turning|never negative|at most|at least',
    },
    ('functions', 2): {
        'table of values': r'table of values',
        'gradient from two points': r'rise over run|rise .* run',
        'negative gradient': r'falls|negative gradient|m = -',
        'intercept c from a point': r'intercept',
        'crossing the horizontal axis': r'x-intercept|horizontal axis|x-axis|y = 0',
        'parallel': r'[Pp]arallel',
        'perpendicular, product -1': r'[Pp]erpendicular|= -1',
        'where two lines meet (set equal)': r'meet|cross|intersect|same \$?y',
    },
    ('functions', 3): {
        'parabola': r'[Pp]arabola',
        'roots from factorised form': r'factoris|bracket is 0|product is 0|each bracket',
        'turning point halfway between roots': r'halfway|midway|symmetr|mirror',
        'increasing / decreasing': r'increasing|decreasing',
        'cubic': r'[Cc]ubic|x\^3',
        'exponential, doubling': r'doubl|2\^',
        'power that is not a whole number': r'\^\{?\d\.\d|2\^\{[^}]*\.',
        'trial and improvement / estimate a crossing': r'trial|try |narrow|estimate|between \d+ and \d+',
        'distance-time: gradient is speed': r'speed|distance-time',
        'average speed': r'average speed',
        'solve f = g where graphs meet': r'graphs? (meet|cross)|where .* meet|intersect',
        'flat line y = k': r'flat line|horizontal line|line \$y = \d+\$',
    },
}

for (course, n), ideas in IDEAS.items():
    cj = json.load(open(f'app/content/courses/{course}/course.json'))
    lessons = next(lv for lv in cj['levels'] if lv['n'] == n)['lessons']
    print(f'== {course} level {n}: ' + ', '.join(l.split('-')[0] for l in lessons))
    blobs = [open(f'app/content/courses/{course}/{l}.json').read() for l in lessons]
    for idea, rx in ideas.items():
        counts = [len(re.findall(rx, b)) for b in blobs]
        print(f'   {"ZERO" if not any(counts) else "    "} {idea:48s} {counts}')
