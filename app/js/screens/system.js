/* Design system and visual test page (#system): tokens, type, buttons, answer states and course art, then a gallery
   that renders every registered canvas kind (ZQ.canvas.kinds) and every registered widget kind (ZQ.widgets.kinds)
   in labelled cards, with theme and motion toggles. Canvas samples are the JSON examples from
   js/engine/canvas/README.md and README-B.md; widget samples follow docs/AUTHORING.md section 3 and render through
   ZQ.player.renderItem, so canvas-bound widgets drive their canvas as in a lesson. A kind with no sample shows a
   warning card, so a new kind cannot slip past this page. The code widget loads Python only on request. */
(function () {
  'use strict';
  const CANVAS_SAMPLES = {
    "grid": {"params": {"rowLabel": "First die", "colLabel": "Second die", "cells": "pair", "text": "marked"}, "state": {"shade": {"eight": ["r2c6", "r3c5", "r4c4", "r5c3", "r6c2"]}, "outline": "cross5", "dim": ["r1c1"], "mark": {"r5c5": {"text": "×2", "tone": "notyet"}}}},
    "tree": {"params": {"levels": [{"label": "First draw", "branches": [{"id": "r", "label": "Red", "p": "3/5"}, {"id": "b", "label": "Blue", "p": "2/5"}]}, {"label": "Second draw", "branches": [{"id": "r", "label": "Red", "p": {"r": "2/4", "b": "3/4"}}, {"id": "b", "label": "Blue", "p": {"r": "2/4", "b": "1/4"}}]}], "leaves": {"r-r": "6/20", "r-b": "6/20", "b-r": "6/20", "b-b": "2/20"}}, "state": {"highlight": ["r-b"], "unknown": ["b-b"]}},
    "venn": {"params": {"sets": ["A", "B"], "labels": {"A": "Rain", "B": "Wind"}, "values": {"A": 12, "B": 8, "AB": 5, "none": 15}, "universe": "All 40 days"}, "state": {"shade": ["AB"]}},
    "number-line": {"params": {"min": -5, "max": 5, "step": 1}, "state": {"points": [{"id": "p1", "x": -2, "label": "a"}], "intervals": [{"id": "i1", "from": -1, "to": 2, "open": [true, false]}], "arrows": [{"id": "j1", "from": -2, "to": 1, "label": "+3"}]}},
    "boxes": {"params": {"containers": [{"id": "urn", "label": "Urn", "kind": "urn", "items": [{"id": "b1", "colour": 1}, {"id": "b2", "colour": 1}, {"id": "b3", "colour": 2}]}, {"id": "hand", "label": "Drawn", "kind": "hand", "capacity": 2}]}, "state": {"draw": ["b3"]}},
    "area": {"params": {"shape": "rect", "grid": [3, 4], "size": [4, 3], "labels": {"bottom": "$\\tfrac{3}{4}$ of the width", "left": "$\\tfrac{2}{3}$"}}, "state": {"shade": {"width": {"cols": 3}, "height": {"rows": 2}}}},
    "balance": {"params": {"left": [{"id": "x1", "kind": "unknown"}, {"id": "x2", "kind": "unknown"}, {"id": "w3", "kind": "weight", "value": 3}], "right": [{"id": "w11", "kind": "weight", "value": 11}]}, "state": {}},
    "circle": {"params": {"values": true}, "state": {"angle": 60, "shade": "sector"}},
    "table": {"params": {"columns": ["$x$", "$P(X = x)$"], "rows": [["0", "0.25"], ["1", {"edit": true}], ["2", "0.25"]], "align": ["center", "right"]}, "state": {"highlight": {"rows": [1]}}},
    "plane": {"params": {"x": [-1, 5], "y": [-1, 6], "functions": [{"id": "f", "expr": "a*x^2", "label": "$f(x)$"}], "params": {"a": 0.25}}, "state": {"points": [{"id": "p1", "x": 2, "y": 1, "drag": true, "on": "f", "label": "P"}], "tangent": {"f": "f", "x": "p1", "label": "slope"}, "riemann": {"f": "f", "from": 0, "to": 4, "n": 4, "rule": "left", "showSum": true}}},
    "bars": {"params": {"categories": [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], "xLabel": "Total of two dice", "exact": [{"x": "7", "y": 0.1667}, {"x": "6", "y": 0.1389}, {"x": "8", "y": 0.1389}], "sim": {"trials": [10, 100, 1000], "outcome": "d6()+d6()", "seed": 7}}, "state": {"ran": 0, "caption": "Run some rolls and watch the 7 bar."}},
    "distribution": {"params": {"family": "normal", "params": {"mu": 0, "sigma": 1}, "showMean": true, "showSd": true}, "state": {"shade": {"from": -1, "to": 1}}},
    "scatter": {"params": {"points": [[1, 2.1], [2, 2.9], [3, 3.2], [4, 4.8], [5, 5.1]], "x": "Hours studied", "y": "Score"}, "state": {"line": {"m": 0.5, "b": 2}, "residuals": "line", "showSSE": true}},
    "series": {"params": {"series": [{"id": "px", "label": "Strategy", "values": [100, 104, 101, 97, 99, 106]}], "format": "money", "currency": "£"}, "state": {"drawdown": true, "markers": [{"id": "peak", "i": 1, "label": "peak"}]}},
    "walk": {"params": {"steps": 60, "p": 0.5, "paths": 40, "barriers": [-10, 10], "sim": {"seed": 1}}, "state": {"showMean": true, "showHits": true}},
    "matrix": {"params": {"matrices": [{"id": "A", "rows": [[1, 2], [3, 4]], "label": "$\\mathbf{A}$"}, {"id": "B", "rows": [[5, 6], [7, 8]], "label": "$\\mathbf{B}$"}, {"id": "C", "rows": [[19, 22], [43, 50]], "label": "$\\mathbf{AB}$"}], "ops": ["×", "="]}, "state": {"hidden": ["C"], "product": {"a": "A", "b": "B", "c": "C", "i": 0, "j": 1}}},
    "vectors": {"params": {"x": [-1, 6], "y": [-1, 5], "vectors": [{"id": "u", "v": [3, 1], "label": "$\\mathbf{u}$"}, {"id": "v", "v": [1, 3], "label": "$\\mathbf{v}$"}]}, "state": {"show": ["sum"], "drag": ["u", "v"]}},
    "graph": {"params": {"markov": true, "nodes": [{"id": "bull", "label": "Bull", "x": 0.2, "y": 0.5}, {"id": "bear", "label": "Bear", "x": 0.8, "y": 0.5}], "edges": [{"from": "bull", "to": "bull", "w": 0.9}, {"from": "bull", "to": "bear", "w": 0.1}, {"from": "bear", "to": "bull", "w": 0.3}, {"from": "bear", "to": "bear", "w": 0.7}]}, "state": {"distribution": {"bull": 0.75, "bear": 0.25}}},
    "array": {"params": {"cells": [2, 5, 8, 12, 16, 23, 38, 56]}, "state": {"pointers": [{"id": "lo", "at": 0, "label": "lo"}, {"id": "mid", "at": 3, "label": "mid"}, {"id": "hi", "at": 7, "label": "hi"}], "highlight": {"range": [0, 3]}}},
    "payoff": {"params": {"legs": [{"id": "c1", "type": "call", "side": "long", "strike": 95, "premium": 7, "label": "long 95 call"}, {"id": "c2", "type": "call", "side": "short", "strike": 105, "premium": 2.5, "label": "short 105 call"}], "range": [80, 120], "label": "bull spread"}, "state": {"spot": 102}},
    "orderbook": {"params": {"bids": [[99.98, 300], [99.97, 500], [99.96, 200]], "asks": [[100.0, 200], [100.01, 400], [100.02, 300]]}, "state": {"order": {"side": "buy", "size": 750}}},
  };
  const CANVAS_ABOUT = {
    grid: 'Cell grid: sample spaces, two-dice tables, area models', tree: 'Probability and decision trees', venn: 'Two or three set Venn diagrams',
    'number-line': 'Points, intervals and jumps on a line', boxes: 'Balls, cards and coins in urns and boxes', area: 'Area models and geometric probability',
    balance: 'Two-pan scale with weights and unknowns', circle: 'Unit circle, angles, sine and cosine', table: 'Static or editable data table',
    plane: 'Coordinate plane: functions, tangents, areas, Riemann sums', bars: 'Bar charts and histograms, with simulation', distribution: 'A pmf or pdf with a shaded region',
    scatter: 'Points, a fitted line and residuals', series: 'Time series with markers and shaded drawdowns', walk: 'Random walks and price paths',
    matrix: 'Matrices with highlighted rows, columns and pivots', vectors: '2D vectors, sums and projections', graph: 'Nodes and edges, Markov chains',
    array: 'Array cells with index labels and pointers', payoff: 'Option payoff and P&L against the underlying', orderbook: 'Bid and ask ladder with a market order',
  };

  /* One item per widget kind (docs/AUTHORING.md 3). Canvas-bound kinds carry their canvas. */
  const WIDGET_SAMPLES = {
    choice: { question: 'Two fair dice. The first shows 5. What is $P(\\text{total} = 7)$ now?', widget: { kind: 'choice', layout: 'grid', options: [
      { id: 'a', text: '$1/6$', correct: true }, { id: 'b', text: '$1/36$', why: 'You kept the whole table as the denominator.' }, { id: 'c', text: '$2/6$', why: 'You counted (5, 2) and (2, 5), but (2, 5) is gone.' }] } },
    multi: { question: 'Which totals can two dice make with a 6 showing? Select all that apply.', widget: { kind: 'multi', options: [
      { id: 'a', text: '7', correct: true }, { id: 'b', text: '12', correct: true }, { id: 'c', text: '6', why: 'A 6 and the smallest other face, 1, already make 7.' }, { id: 'd', text: '13', why: 'The largest total is 6 + 6.' }] } },
    numeric: { question: 'Type $P(\\text{total} = 7 \\mid \\text{first} = 5)$.', widget: { kind: 'numeric', answer: 0.1667, tol: { abs: 0.0005 }, placeholder: 'fraction or decimal', accept: 'Any form equal to 1/6',
      wrong: [{ id: 'whole', value: 0.0278, tol: { abs: 0.001 } }] } },
    expression: { question: 'Simplify $\\tfrac{x}{2} + \\tfrac{1}{2}$.', widget: { kind: 'expression', answer: '\\frac{x+1}{2}', accept: ['(x+1)/2', 'x/2+1/2', '0.5x+0.5'], wrong: [{ id: 'forgot-half', tex: 'x+1' }], keyboard: 'algebra' } },
    slider: { question: 'Set $p$ so the distribution is symmetric.', canvas: { kind: 'distribution', params: { family: 'binomial', params: { n: 10, p: 0.3 } }, state: {} },
      widget: { kind: 'slider', min: 0, max: 1, step: 0.05, start: 0.3, bind: 'p', label: '$p$', answer: 0.5, tol: 0.02, wrong: [{ id: 'low', from: 0, to: 0.45 }] } },
    'drag-point': { question: 'Drag the point to $2.5$.', canvas: { kind: 'number-line', params: { min: 0, max: 5, step: 0.5 }, state: { points: [{ id: 'p1', x: 1, label: 'a', drag: true }] } },
      widget: { kind: 'drag-point', points: [{ id: 'p1', target: 2.5, tol: 0.25 }] } },
    place: { question: 'Build $\\dfrac{n!}{(n-k)!}$.', widget: { kind: 'place', mode: 'assign', tokens: [{ id: 't1', text: '$n!$' }, { id: 't2', text: '$(n-k)!$' }],
      slots: [{ id: 'num', label: 'numerator', accepts: ['t1'] }, { id: 'den', label: 'denominator', accepts: ['t2'] }] } },
    'tap-regions': { question: 'Tap the two rolls that total 7 and contain a 5.', canvas: { kind: 'grid', params: { rowLabel: 'First die', colLabel: 'Second die', cells: 'sum' }, state: {} },
      widget: { kind: 'tap-regions', answer: ['r5c2', 'r2c5'], wrong: [{ id: 'double', set: ['r5c2', 'r2c5', 'r5c5'] }] } },
    order: { question: 'Put the derivation in order.', widget: { kind: 'order', lines: [
      { id: 's1', text: 'Write $P(A \\cap B) = P(A \\mid B)\\,P(B)$' }, { id: 's2', text: 'Write $P(A \\cap B) = P(B \\mid A)\\,P(A)$' }, { id: 's3', text: 'Equate them and divide by $P(B)$' }], answer: ['s1', 's2', 's3'] } },
    table: { question: 'Fill in the missing probability.', widget: { kind: 'table', columns: ['$x$', '$P(X = x)$'], rows: [['0', { edit: true, answer: 0.25, tol: { abs: 0.001 } }], ['1', '0.5'], ['2', '0.25']] } },
    manipulate: { question: 'Solve for $x$.', widget: { kind: 'manipulate', start: 's0', target: 's3', states: {
      s0: { tex: '2x + 3 = 11', ops: [{ label: 'Subtract 3 from both sides', to: 's1' }, { label: 'Divide both sides by 2', to: 's0b', why: 'Dividing now leaves a fraction on the left; clear the 3 first.' }] },
      s0b: { tex: 'x + \\tfrac{3}{2} = \\tfrac{11}{2}', ops: [{ label: 'Subtract 3/2 from both sides', to: 's3' }] },
      s1: { tex: '2x = 8', ops: [{ label: 'Divide both sides by 2', to: 's3' }] }, s3: { tex: 'x = 4' } } } },
    balance: { question: 'Leave $x$ alone on one pan.', canvas: { kind: 'balance', params: { left: [{ id: 'x1', kind: 'unknown', label: 'x' }, { id: 'w3', kind: 'weight', value: 3 }], right: [{ id: 'w7', kind: 'weight', value: 7 }] } },
      widget: { kind: 'balance', left: [{ id: 'x1', kind: 'unknown', label: 'x' }, { id: 'w3', kind: 'weight', value: 3 }], right: [{ id: 'w7', kind: 'weight', value: 7 }], moves: ['remove-both', 'halve-both'], target: { left: ['unknown'], right: [4] } } },
    sketch: { question: 'Sketch the payoff of a call struck at 100.', canvas: { kind: 'plane', params: { x: [80, 120], y: [-4, 24] }, state: {} },
      widget: { kind: 'sketch', control: 5, target: 'max(x - 100, 0)', xRange: [80, 120], band: 2, wrong: [{ id: 'linear', expr: '0.5*(x - 80)', band: 2 }] } },
    code: { question: 'Return the sum of the squares.', widget: { kind: 'code', language: 'python', starter: 'def sum_squares(xs):\n    return 0\n', solution: 'def sum_squares(xs):\n    return sum(x * x for x in xs)\n',
      examples: [{ call: 'sum_squares([1, 2])', expect: '5' }], tests: [{ call: 'sum_squares([])', expect: '0', compare: 'equal' }, { call: 'sum_squares([3])', expect: '9', compare: 'equal' }, { call: 'sum_squares([1, 2, 3])', expect: '14', compare: 'equal' }],
      how: 'Check runs 3 hidden tests.' } },
    longform: { kind: 'longform', prompt: 'Explain why $P(A \\mid B)$ and $P(B \\mid A)$ can differ.', model: 'They share the numerator $P(A \\cap B)$ but divide by different events, $P(B)$ and $P(A)$.',
      rubric: [{ points: 4, text: 'Writes both as a joint probability over a marginal' }, { points: 3, text: 'Names the different denominators' }, { points: 3, text: 'Gives an example where they differ' }] },
  };

  /* Variants worth seeing on their own: drawn after the one-per-kind samples. Canvas variants render through
     ZQ.player.renderItem so their explore controls (canvas.controls) work as in a lesson. */
  const CANVAS_EXTRAS = [
    { name: 'pair (circle and sine)', about: 'Two canvases side by side; derive reads the circle and moves the point on the sine curve', spec: { kind: 'pair', active: 'right',
      left: { kind: 'circle', params: { values: false }, state: { angle: 30 } },
      right: { kind: 'plane', params: { x: [0, 6.3], y: [-1.2, 1.2], functions: [{ id: 's', expr: 'sin(x)' }] }, state: { points: [{ id: 'P', x: 0, y: 0, label: 'P' }] } },
      derive: { 'right:P.x': 'angle * pi / 180', 'right:P.y': 'sin(angle * pi / 180)', caption: 'sin {{angle}}° = {{fixed(sin(angle * pi / 180), 3)}}' },
      controls: [{ bind: 'left:angle', min: 0, max: 360, step: 15, label: 'Angle' }] } },
    { name: 'plane (geometry)', about: 'axes: false, a filled polygon with vertex labels, a right-angle mark and an angle arc', spec: { kind: 'plane',
      params: { x: [0, 6], y: [0, 4], axes: false, equal: true },
      state: { points: [{ id: 'A', x: 1, y: 0.6 }, { id: 'B', x: 5, y: 0.6 }, { id: 'C', x: 1, y: 3.4 }], polygons: [{ id: 'tri', points: ['A', 'B', 'C'], vertexLabels: ['A', 'B', 'C'], colour: 2 }],
        angles: [{ id: 'r', at: 'A', from: 'B', to: 'C', right: true }, { id: 'th', at: 'B', from: 'A', to: 'C', label: '$\\theta$' }], segments: [{ id: 'h', from: 'B', to: 'C', label: 'hypotenuse', labelOffset: [10, -12] }] } } },
    { name: 'area (signed pieces)', about: '(x + 5)(x − 2): the −2 strip is subtracted (hatched); a diagonal halves one piece', spec: { kind: 'area',
      params: { shape: 'rect', grid: [2, 2], size: [4, 3], colSizes: [3, 1.5], rowSizes: [3, -1], colLabels: ['$x$', '$5$'], rowLabels: ['$x$', '$-2$'], labels: { c11: '$x^2$', c12: '$5x$', c21: '$-2x$', c22: '$-10$' } },
      state: { shade: { a: ['c11', 'c12'] }, diagonal: { c12: '\\' } } } },
    { name: 'series (log scale)', about: 'yScale: "log" with price-labelled ticks', spec: { kind: 'series', params: { series: [{ id: 'px', label: 'Price', values: [10, 14, 21, 30, 46, 70, 100, 150, 230, 340, 500] }], yScale: 'log', money: '£' }, state: {} } },
    { name: 'area (re-cut)', about: 'Explore controls bound to grid.cols, split.rows and shade (fraction readout): the half stays shaded as the cuts change', spec: { kind: 'area',
      params: { shape: 'rect', grid: [1, 2], size: [4, 2] }, state: { shade: 0.5, split: [1, 1] },
      controls: [{ bind: 'grid.cols', min: 2, max: 12, step: 2, label: 'Pieces across' }, { bind: 'split.rows', min: 1, max: 4, step: 1, label: 'Cuts down' }, { bind: 'shade', min: 0, max: 1, step: 0.125, label: 'Shaded', format: 'fraction' }] } },
    { name: 'area (circle, 12 sectors)', about: 'Grid lines stay visible inside the shading', spec: { kind: 'area', params: { shape: 'circle', sectors: 12 }, state: { shade: { a: ['c11', 'c12', 'c13'], b: ['c13', 'c14'] } } } },
    { name: 'number-line (labels)', about: 'labelPos above, below, left and right; close points stacked; labels kept clear of jump arrows', spec: { kind: 'number-line',
      params: { min: 0, max: 10, step: 1 },
      state: { points: [{ id: 'a', x: 2, label: 'start' }, { id: 'b', x: 5, label: 'end' }, { id: 'c', x: 7, label: '$x$' }, { id: 'd', x: 7.5, label: 'close', colour: 2 }, { id: 'e', x: 9, label: 'below', labelPos: 'below' }, { id: 'f', x: 0.5, label: 'right', labelPos: 'right', colour: 3 }],
        intervals: [{ id: 'i1', from: 6, to: 8, label: 'interval', labelPos: 'below' }], arrows: [{ id: 'j1', from: 2, to: 5, label: '+3' }] } } },
    { name: 'grid (lattice paths)', about: 'lattice: true, a coloured route through the points, state.cells filling counts, a shade set with its own colour', spec: { kind: 'grid',
      params: { rows: 4, cols: 5, rowHeads: false, colHeads: false, lattice: true },
      state: { cells: { r4c1: '1', r3c1: '1', r4c2: '1', r3c2: '2' }, shade: { start: { ids: ['r4c1'], colour: 3 }, end: { ids: ['r1c5'], colour: 2 } },
        paths: [{ id: 'route', cells: ['r4c1', 'r4c2', 'r3c2', 'r3c3', 'r2c3', 'r2c4', 'r1c4', 'r1c5'], colour: 1 }], caption: 'Routes so far: **2** to `r3c2`' } } },
    { name: 'grid (staggered rows)', about: 'rowOffsets shifts each row, as on a keyboard; the outline follows the shift', spec: { kind: 'grid',
      params: { rows: 3, cols: 10, rowHeads: false, colHeads: false, rowOffsets: [0, 0.25, 0.75], cells: [['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P'], ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ';'], ['Z', 'X', 'C', 'V', 'B', 'N', 'M', ',', '.', '/']] },
      state: { shade: { home: { ids: ['r2c1', 'r2c2', 'r2c3', 'r2c4', 'r2c7', 'r2c8', 'r2c9', 'r2c10'], colour: 2 } }, outline: ['r2c4', 'r2c7'] } } },
    { name: 'tree (compact, 16 leaves)', about: 'compact: true, four tosses top to bottom, a labelled root and the current node', spec: { kind: 'tree',
      params: { orient: 'tb', compact: true, rootLabel: 'Start', label: 'Four tosses of a coin', levels: [1, 2, 3, 4].map(k => ({ label: `Toss ${k}`, branches: [{ id: 'H', label: 'H' }, { id: 'T', label: 'T' }] })) },
      state: { current: 'H-T', highlight: ['H-T'] } } },
    { name: 'plane (contours and heat)', about: 'A heat map of f(x, y) behind a contour family (levels), each level labelled on its curve', spec: { kind: 'plane',
      params: { x: [-3, 3], y: [-3, 3], equal: true, functions: [{ id: 'h', heat: 'x^2 + y^2', range: [0, 12], colour: 1 }, { id: 'c', contour: 'x^2 + y^2', levels: [1, 4, 9], colour: 1, labelAvoid: false }] } } },
    { name: 'vectors (transform)', about: 'state.transform { angle, shear } turns the basis, the grid and the unit square; an angle mark between two arrows', spec: { kind: 'vectors',
      params: { range: [-3, 3] }, state: { transform: { angle: 30, shear: 0.5 }, vectors: [{ id: 'u', v: [2, 0], label: '$\\mathbf{u}$' }, { id: 'w', v: [1, 1.5], label: '$\\mathbf{w}$', colour: 3 }], angles: [{ id: 'th', a: 'u', b: 'w', label: '$\\theta$' }] },
      controls: [{ bind: 'angle', min: 0, max: 90, step: 5, label: 'Angle' }, { bind: 'shear', min: -1, max: 1, step: 0.25, label: 'Shear' }] } },
    { name: 'matrix (groups and labels)', about: 'Two highlight groups in their own colours, row and column labels, a scale factor and an augmented bar', spec: { kind: 'matrix',
      params: { matrices: [{ id: 'A', rows: [[2, -1, 0, 3], [1, 3, -2, 5], [0, 1, 4, -1]], rowLabels: ['$R_1$', '$R_2$', '$R_3$'], colLabels: ['$x$', '$y$', '$z$', ''], bar: 3 }, { id: 'Q', rows: [[1, -1], [1, 1]], scale: '\\tfrac{1}{\\sqrt{2}}' }], ops: ['$\\quad$'] },
      state: { highlight: { A: [{ rows: [0], colour: 2 }, { cols: [1], colour: 4 }] }, pivot: { A: [[0, 0]] } } } },
    { name: 'tree (27 leaves, branching)', about: 'Three-way fans with staggered labels; a control sets how many branches the second stage shows', spec: { kind: 'tree',
      params: { compact: true, levels: [0, 1, 2].map(() => ({ branches: ['a', 'b', 'c'].map(id => ({ id, p: '\\tfrac{1}{3}' })) })) },
      state: { branching: { 1: 3 } }, controls: [{ bind: 'branching.1', min: 1, max: 3, step: 1, label: 'Options at stage 2' }] } },
    { name: 'series (reference line)', about: 'hlines draws a limit across a partial-sum chart; the label keeps clear of the line', spec: { kind: 'series',
      params: { height: 220, indexFrom: 1, series: [{ id: 's', label: 'Partial sums', values: [1, 1.25, 1.361, 1.424, 1.464, 1.491, 1.512, 1.527, 1.539, 1.55] }], hlines: [{ id: 'lim', y: 1.6449, label: '$\\pi^2/6$' }] },
      derive: { caption: 'A log slider: {{n}} terms' }, controls: [{ bind: 'n', min: 1, max: 1000, scale: 'log', perDecade: 1, label: 'Terms', start: 10 }] } },
    { name: 'grid (running total)', about: 'derive reads the tap selection: selected.length and total(selected) in the caption', spec: { kind: 'grid',
      params: { rows: 3, cols: 3, cells: 'sum' }, state: { selected: ['r1c1', 'r3c3'] }, derive: { caption: '{{selected.length}} tapped, total {{total(selected)}}' } } },
    { name: 'distribution (tails and overlay)', about: 'Two shaded tails summed, a normal overlay following n and p, a continuity strip under it, an observed value', spec: { kind: 'distribution',
      params: { family: 'binomial', params: { n: 40, p: 0.5 }, overlay: [{ id: 'nrm', family: 'normal', params: { mu: 'n * p', sigma: 'sqrt(n * p * (1 - p))' } }] },
      state: { shade: [{ to: 14 }, { from: 26 }, { id: 'cc', from: 13.5, to: 14.5, under: 'nrm' }], observed: { x: 27, label: 'observed 27' } },
      controls: [{ bind: 'n', min: 10, max: 60, step: 2, label: '$n$' }] } },
    { name: 'distribution (custom and CDF)', about: 'A custom discrete support with its mean, and the same law as a step CDF', spec: { kind: 'pair', stack: true,
      left: { kind: 'distribution', params: { height: 220, family: 'discrete', values: [-1, 0.5, 2, 5], probs: [0.4, 0.3, 0.2, 0.1], showMean: true } },
      right: { kind: 'distribution', params: { height: 220, family: 'discrete', values: [-1, 0.5, 2, 5], probs: [0.4, 0.3, 0.2, 0.1], cdf: true } } } },
    { name: 'bars (grouped simulation)', about: 'groups draw two bars per category with a legend; each trial returns [X, Y]', spec: { kind: 'bars',
      params: { categories: [0, 1, 2, 3, 4, 5, 6], groups: [{ id: 'X', label: 'p = 0.3' }, { id: 'Y', label: 'p = 0.6', colour: 3 }], sim: { outcome: '[binomial(6, 0.3), binomial(6, 0.6)]', seed: 3 } }, state: { ran: 300 } } },
    { name: 'bars (curve and cut)', about: 'A simulated histogram (sim.let, filter), a normal curve that follows k, a cut that recolours the tail, a reference line', spec: { kind: 'bars',
      params: { bins: { min: -4, max: 4, width: 0.5 }, proportion: true, params: { k: 4 }, sim: { let: { xs: 'sample(k, u(-1, 1))' }, outcome: 'sum(xs)', seed: 2 },
        curves: [{ id: 'nrm', expr: 'w * exp(-x^2 / (2 * k / 3)) / sqrt(2 * pi * k / 3)', label: 'normal' }], hlines: [{ id: 'h', y: 0.1, label: '10%' }] },
      state: { ran: 1000, cut: { at: 2, colour: 2, label: 'beyond {at}' } }, controls: [{ bind: 'k', min: 1, max: 8, step: 1, label: 'Terms $k$' }, { bind: 'cut.at', min: 0, max: 3.5, step: 0.5, label: 'Cut' }] } },
    { name: 'grid (population and margins)', about: 'population: 1000 dots shaded by group counts, and a joint table with its margins', spec: { kind: 'pair', stack: true,
      left: { kind: 'grid', params: { population: 1000 }, state: { groups: [{ id: 'tp', count: 9, label: 'ill, test positive' }, { id: 'fp', count: 99, label: 'well, test positive' }] } },
      right: { kind: 'grid', params: { rows: 2, cols: 2, rowHeads: ['A', 'not A'], colHeads: ['B', 'not B'], cells: [['12', '18'], ['8', '62']], margins: true } } } },
    { name: 'walk (Markov chain)', about: 'model: "markov" simulates state paths from P; xStep ticks every 5 steps; a reseed button', spec: { kind: 'walk',
      params: { model: 'markov', states: ['Bull', 'Flat', 'Bear'], P: [[0.8, 0.15, 0.05], [0.2, 0.6, 0.2], [0.1, 0.3, 0.6]], start: 'Flat', steps: 20, paths: 3, xStep: 5 },
      controls: [{ reseed: true, label: 'New paths' }] } },
    { name: 'number-line (log-odds)', about: 'scale: "log-odds" places probabilities by their log odds; a Bayes update is one jump', spec: { kind: 'number-line',
      params: { scale: 'log-odds', min: 0.01, max: 0.99, format: 'percent' }, state: { points: [{ id: 'a', x: 0.2, label: 'prior' }, { id: 'b', x: 0.8, label: 'posterior' }], arrows: [{ id: 'j', from: 0.2, to: 0.8, label: 'odds ×16' }] } } },
    { name: 'payoff (spot drag)', about: 'drag: "spot" moves the expiry price; showTotal: false shows each leg; a leg without its floor', spec: { kind: 'payoff',
      params: { range: [60, 140], drag: 'spot', showTotal: false, legs: [{ id: 'c', type: 'call', strike: 100, premium: 5, label: 'long call', labelAt: 0.9 }, { id: 'f', type: 'call', strike: 100, premium: 5, floor: false, colour: 5, label: 'no floor', labelAt: 0.1 }] }, state: { spot: 110 } } },
    { name: 'bars (below zero)', about: 'Negative values hang below the zero baseline; value labels in pounds', spec: { kind: 'bars',
      params: { categories: [{ id: 'jan', label: 'Jan', value: 120 }, { id: 'feb', label: 'Feb', value: -80 }, { id: 'mar', label: 'Mar', value: 45 }, { id: 'apr', label: 'Apr', value: -150 }, { id: 'may', label: 'May', value: 200 }], yLabel: 'P&L (£)', showValues: true, money: '£', decimals: 0 }, state: {} } },
    { name: 'matrix (wide)', about: 'Three wide matrices scale down to the column instead of running off it', spec: { kind: 'matrix',
      params: { matrices: [{ id: 'A', rows: [[1.25, -3.5, 12.75, 0.5], [2, 4.125, -6, 8]] }, { id: 'B', rows: [[10.5, 20.25], [30, 40.75], [-5.5, 6], [7, 8.25]] }, { id: 'C', rows: [[105.94, 162.47], [97.44, 278.63]] }], ops: ['*', '='] }, state: { highlight: { A: { rows: [0] }, B: { cols: [1] } } } } },
    { name: 'console (pytest run)', about: 'Monospace lines that keep their indentation; ids l1, l2, ...; one line shaded, a prompt line muted', spec: { kind: 'console',
      params: { title: 'Terminal', lines: ['$ pytest -q', '..F.                                     [100%]', 'FAILED test_returns.py::test_flat - assert 0.01 == 0.0', '    def test_flat():', '>       assert daily_return(100, 101) == 0.0', 'E       assert 0.01 == 0.0', '1 failed, 3 passed in 0.12s'] },
      state: { shade: { fail: ['l6'] }, tone: { l3: 'err', l7: 'muted' }, caption: 'The `E` line shows **what** the assert compared' } } },
    { name: 'graph (lanes and pills)', about: 'Lanes behind the graph, pill nodes sized to their labels, a dashed node for a fetched commit', spec: { kind: 'graph',
      params: { height: 260, directed: true, lanes: [{ y: 0.15, label: 'origin' }, { y: 0.85, label: 'local' }],
        nodes: [{ id: 'a', label: 'a1f', x: 0.1, y: 0.85 }, { id: 'b', label: 'b2e', x: 0.35, y: 0.85 }, { id: 'c', label: 'c3d', x: 0.6, y: 0.15, dashed: true }, { id: 'm', label: 'main', x: 0.9, y: 0.85, shape: 'pill' }],
        edges: [{ from: 'b', to: 'a' }, { from: 'c', to: 'b' }, { from: 'm', to: 'b', dashed: true }] } } },
    { name: 'graph (ring, rotate)', about: 'layout: "ring" seats the nodes round a circle; state.rotate turns them; labels relabel; the radius fits the longest label', spec: { kind: 'graph',
      params: { layout: 'ring', directed: false, nodes: ['A', 'B', 'C', 'D', 'E'].map(id => ({ id, label: id })), edges: [{ from: 'A', to: 'B' }, { from: 'B', to: 'C' }] },
      state: { rotate: 1, labels: { A: 'Alice', B: 'Bryony' }, current: 'A' } } },
    { name: 'boxes (folders and files)', about: 'A card is as wide as its file name; a box is closed on all four sides', spec: { kind: 'boxes',
      params: { containers: [{ id: 'docs', kind: 'box', label: 'docs', capacity: 2, items: [{ id: 'f1', kind: 'card', label: 'notes.txt' }, { id: 'f2', kind: 'card', label: 'prices.csv' }] }, { id: 'code', kind: 'box', label: 'code', capacity: 2, items: [{ id: 'f3', kind: 'card', label: 'week.py' }] }] } } },
    { name: 'vectors (points and labels)', about: 'Labelled points (O, A, B, M) and vector labels at the middle of the arrow', spec: { kind: 'vectors',
      params: { x: [-1, 5], y: [-1, 4], vectors: [{ id: 'a', v: [4, 1], label: '$\\mathbf{a}$', labelPos: 'mid', labelSide: 'right' }, { id: 'b', v: [1, 3], label: '$\\mathbf{b}$', labelPos: 'mid' }],
        points: [{ id: 'O', x: 0, y: 0, label: 'O', labelPos: 'nw' }, { id: 'A', x: 4, y: 1, label: 'A', labelPos: 'e' }, { id: 'B', x: 1, y: 3, label: 'B', labelPos: 'n' }, { id: 'M', x: 2.5, y: 2, label: 'M', labelPos: 'ne' }] } } },
  ];
  const WIDGET_EXTRAS = [
    { name: 'balance (signed)', kind: 'balance', item: { question: 'Solve $7 - 3x = 22$ on the scale.', canvas: { kind: 'balance', params: { left: [{ id: 'w7', kind: 'weight', value: 7 }, { id: 'x', kind: 'unknown', coef: -3 }], right: [{ id: 'w22', kind: 'weight', value: 22 }] } },
      widget: { kind: 'balance', left: [{ id: 'w7', kind: 'weight', value: 7 }, { id: 'x', kind: 'unknown', coef: -3 }], right: [{ id: 'w22', kind: 'weight', value: 22 }], moves: ['subtract-both', 'add-both', 'divide-both'], target: { left: ['unknown'], right: [-5] } } } },
    { name: 'place (boxes)', kind: 'place', item: { question: 'Put the sealed bag and the tails coin in the hand.', canvas: { kind: 'boxes', params: { containers: [{ id: 'urn', kind: 'urn', label: 'Urn', items: [{ id: 'c1', kind: 'coin' }, { id: 'c2', kind: 'coin', face: 'T' }, { id: 'g1', kind: 'bag', label: '?' }] }, { id: 'hand', kind: 'hand', label: 'Hand' }] } },
      widget: { kind: 'place', mode: 'boxes', answer: { hand: ['g1', 'c2'] } } } },
    { name: 'tap-regions (table rows)', kind: 'tap-regions', item: { question: 'Tap the row the query returns first.', canvas: { kind: 'table', params: { tap: 'rows', columns: ['ticker', 'close'], rows: [['`AAPL`', 182.5], ['`MSFT`', 410.25], ['`TSLA`', 171]] } },
      widget: { kind: 'tap-regions', answer: ['r1'], countWord: 'tapped' } } },
    { name: 'tap-regions (console line)', kind: 'tap-regions', item: { question: 'Tap the line that names the failing test.', canvas: { kind: 'console', params: { lines: ['$ pytest -q', '..F', 'FAILED test_a.py::test_flat', '1 failed, 2 passed'] } },
      widget: { kind: 'tap-regions', answer: ['l3'], countWord: 'tapped' } } },
    { name: 'tap-regions (vectors)', kind: 'tap-regions', item: { question: 'Tap the vector that points up and to the left.', canvas: { kind: 'vectors', params: { x: [-4, 4], y: [-1, 4], vectors: [{ id: 'u', v: [3, 1], label: '$\\mathbf{u}$' }, { id: 'w', v: [-2, 3], label: '$\\mathbf{w}$' }] } },
      widget: { kind: 'tap-regions', answer: ['w'], countWord: 'tapped' } } },
    /* item 304: the C++ mode in both shapes; they load the compiler (about 26 MB) only on request */
    { name: 'code (C++ function)', kind: 'code', item: { question: 'Write `double mean(const std::vector<double>& xs)`.', widget: { kind: 'code', language: 'cpp', starter: '#include <vector>\n\ndouble mean(const std::vector<double>& xs) {\n    return 0;\n}\n',
      solution: '#include <vector>\n\ndouble mean(const std::vector<double>& xs) {\n    double total = 0;\n    for (double x : xs) total += x;\n    return xs.empty() ? 0 : total / xs.size();\n}\n',
      examples: [{ call: 'mean', args: [[1, 2, 3, 4]], expect: 2.5, compare: 'isclose' }],
      tests: [{ call: 'mean', args: [[1, 2, 3, 4]], expect: 2.5, compare: 'isclose' }, { call: 'mean({0.1, 0.2, 0.3})', expect: 0.2, compare: 'isclose' }, { setup: 'std::vector<double> xs(10, 7.5);', call: 'mean(xs)', expect: 7.5, compare: 'isclose' }],
      how: 'Check compiles your code once and runs 3 hidden tests.' } } },
    { name: 'code (C++ program)', kind: 'code', item: { question: 'Read two prices from `std::cin` and print the return.', widget: { kind: 'code', language: 'cpp', starter: '#include <iostream>\n#include <iomanip>\n\nint main() {\n    double old_price, new_price;\n    std::cin >> old_price >> new_price;\n}\n',
      solution: '#include <iostream>\n#include <iomanip>\n\nint main() {\n    double old_price, new_price;\n    std::cin >> old_price >> new_price;\n    std::cout << "Return: " << std::fixed << std::setprecision(2) << (new_price - old_price) / old_price * 100 << "%\\n";\n}\n',
      examples: [{ compare: 'stdout', stdin: '250\n262.5\n', expect: 'Return: 5.00%\n' }],
      tests: [{ compare: 'stdout', stdin: '250\n262.5\n', expect: 'Return: 5.00%\n' }, { compare: 'stdout', stdin: '100 90', expect: 'Return: -10.00%\n' }, { compare: 'stdout', stdin: '1\n2\n', expect: 'Return: 100.00%\n', exact: true }],
      how: 'Check runs your program three times with different input.' } } },
    { name: 'code (stdout and stdin)', kind: 'code', item: { question: 'Read two prices with `input()` and print the return.', widget: { kind: 'code', language: 'python', starter: 'old = float(input())\nnew = float(input())\n', solution: 'old = float(input())\nnew = float(input())\nprint(f"Return: {(new - old) / old * 100:.2f}%")\n',
      examples: [{ compare: 'stdout', stdin: '250\n262.5\n', expect: 'Return: 5.00%\n' }],
      tests: [{ compare: 'stdout', stdin: '250\n262.5\n', expect: 'Return: 5.00%\n' }, { compare: 'stdout', stdin: '100\n90\n', expect: 'Return: -10.00%\n' }, { stdin: '1\n2\n', call: 'len(printed)', expect: '1' }], how: 'Check runs your program three times with different input.' } } },
    { name: 'expression (factorised)', kind: 'expression', item: { question: 'Factorise $2x + 6$.', widget: { kind: 'expression', answer: '2(x+3)', accept: ['2(x+3)'], form: 'factorised' } } },
    { name: 'tap-regions (count)', kind: 'tap-regions', item: { question: 'Shade any 3 of the 4 parts.', canvas: { kind: 'area', params: { shape: 'rect', grid: [1, 4], size: [4, 1] }, state: {} },
      widget: { kind: 'tap-regions', count: 3, among: ['c11', 'c12', 'c13', 'c14'], countWord: 'parts' } } },
    { name: 'tap-regions (number-line points)', kind: 'tap-regions', item: { question: 'Tap the two numbers above 4.', canvas: { kind: 'number-line', params: { min: 0, max: 6, step: 1 }, state: { points: [{ id: 'p1', x: 1, label: 'a' }, { id: 'p2', x: 3, label: 'b' }, { id: 'p3', x: 4.5, label: 'c' }, { id: 'p4', x: 5.5, label: 'd' }] } },
      widget: { kind: 'tap-regions', answer: ['p3', 'p4'], countWord: 'tapped' } } },
  ];

  const pretty = (o) => JSON.stringify(o, null, 2);

  ZQ.screen({
    id: 'system', title: 'Design system', group: 'Reference', shell: true, tab: 'none',
    render(root, Z) {
      const { esc, icon } = Z;
      const tracks = (Z.content && Z.content.tracks) || {};
      const sw = (name, v, note = '') => `<div class="ds-sw"><i style="background:var(${v})"></i><b>${esc(name)}</b><span>${note || v.replace('--', '')}</span></div>`;
      const seg = (name, label, opts, val) => `<div class="ds-seg" role="radiogroup" aria-label="${label}"><span class="t-caption muted">${label}</span>${opts.map(([v, l]) => `<label><input type="radio" name="ds-${name}" value="${v}" ${val === v ? 'checked' : ''}><span>${l}</span></label>`).join('')}</div>`;
      const canvasKinds = Object.keys((Z.canvas && Z.canvas.kinds) || {}).sort();
      const widgetKinds = Object.keys((Z.widgets && Z.widgets.kinds) || {}).sort();

      root.innerHTML = `
      <div class="ds">
        <header class="ds-head"><div class="t-overline muted">Reference</div><h1 class="t-course-title" style="margin:4px 0 8px">Design system</h1>
          <p class="t-body secondary" style="margin:0;max-width:62ch">Tokens recreated from the research spec (docs/design-research.md), then every diagram and answer widget the lessons can use, drawn from sample specs. Switch the theme here to check both.</p></header>

        <div class="ds-bar" role="toolbar" aria-label="Page settings">
          ${seg('theme', 'Theme', [['system', 'System'], ['light', 'Light'], ['dark', 'Dark']], Z.settings.theme)}
          ${seg('motion', 'Motion', [['system', 'System'], ['full', 'Full'], ['reduced', 'Reduced']], Z.settings.motion)}
          <nav class="ds-jump" aria-label="Sections"><a href="#system" data-jump="ds-tokens">Tokens</a><a href="#system" data-jump="ds-canvases">Canvases (${canvasKinds.length})</a><a href="#system" data-jump="ds-widgets">Widgets (${widgetKinds.length})</a></nav>
        </div>

        <section id="ds-tokens"><h2 class="t-h1">Colour</h2>
          <h3 class="t-overline muted">Surfaces and ink</h3><div class="ds-grid">${sw('Canvas', '--bg-canvas')}${sw('Sunken', '--bg-sunken')}${sw('Line', '--line')}${sw('Ink', '--ink')}${sw('Secondary', '--text-2')}${sw('Muted', '--text-muted')}</div>
          <h3 class="t-overline muted">Verdicts</h3><div class="ds-grid">${sw('Progress', '--green-brand')}${sw('Correct face', '--green-face')}${sw('Correct frame', '--green-frame')}${sw('Not yet face', '--amber-face')}${sw('Not yet frame', '--amber-frame')}${sw('Hint', '--hint')}</div>
          <h3 class="t-overline muted">Streak and interaction</h3><div class="ds-grid">${sw('Pear 300', '--pear-300')}${sw('Pear 500', '--pear-500')}${sw('Pear 600', '--pear-600')}${sw('Movable', '--manip')}${sw('Neutral action', '--neutral-face')}${sw('Keyword', '--code-keyword')}</div>
          <h3 class="t-overline muted">Tracks</h3><div class="ds-grid">${['maths', 'prob', 'code', 'fin', 'ml', 'speed'].map(t => sw(tracks[t] || t, '--' + t, t)).join('')}</div>
          <h3 class="t-overline muted">Charts (validated order)</h3><div class="ds-grid">${[1, 2, 3, 4, 5, 6].map(i => sw('Slot ' + i, '--s' + i)).join('')}</div>
          <h3 class="t-overline muted">Mastery ramp</h3><div class="ds-grid">${[1, 2, 3, 4, 5, 6].map(i => sw('Step ' + i, '--seq-' + i)).join('')}</div>
        </section>

        <section><h2 class="t-h1">Type</h2>
          <div class="ds-type">
            <div><span class="t-caption muted">Display · Besley 500</span><div class="t-display">Zero to quant, one problem at a time.</div></div>
            <div><span class="t-caption muted">Lesson title · Archivo 700</span><div class="t-lesson-title">Shrinking the sample space</div></div>
            <div><span class="t-caption muted">Course title</span><div class="t-course-title">Conditional Probability</div></div>
            <div><span class="t-caption muted">Prose · 17/25</span><p class="t-prose" style="margin:0;max-width:540px">You roll two dice. A friend peeks and says the first die shows a <b>5</b>. Some outcomes are now impossible. Probability is what is left, measured again: ${Z.tex('P(A \\mid B) = \\dfrac{|A \\cap B|}{|B|}')}</p></div>
            <div><span class="t-caption muted">Overline · Stat · Code</span><div class="t-overline" style="color:var(--prob-deep)">Level 1</div><div class="t-stat">1,240</div><code class="t-code">def max_drawdown(prices: list[float]) -> float:</code></div>
          </div>
        </section>

        <section><h2 class="t-h1">Buttons</h2>
          <p class="t-body secondary" style="margin:0 0 16px">Pills with a hard 4px lip. Press one: the face sinks into the lip.</p>
          <div class="ds-row">
            <button class="btn" disabled>Check</button><button class="btn">Check</button><button class="btn secondary">Why?</button>
            <button class="btn correct">Continue</button><button class="btn secondary">Get help</button><button class="btn notyet">Try again</button>
            <span data-track="prob"><button class="btn track">Continue course</button></span><span data-track="maths"><button class="btn track lg">Start</button></span>
          </div>
        </section>

        <section><h2 class="t-h1">Answer states</h2>
          <div class="opts two" style="max-width:540px">
            <button class="opt">${Z.tex('\\tfrac{5}{36}')}</button>
            <button class="opt selected">${Z.tex('\\tfrac{1}{6}')}</button>
            <button class="opt correct">${Z.tex('\\tfrac{1}{11}')}<span class="badge">${icon('check')}</span></button>
            <button class="opt wrong">${Z.tex('\\tfrac{1}{12}')}<span class="badge">${icon('cross')}</span></button>
          </div>
          <div class="ds-row" style="margin-top:16px">
            <span class="chip correct">${icon('check', 'xs')} Correct · +15 XP</span><span class="chip notyet">${icon('cross', 'xs')} Not quite right</span>
            <span class="streak-pill">11${Z.bolt(true)}<span class="rest-slots"><i class="on"></i><i></i></span></span><span class="streak-pill">11${Z.bolt(false)}<span class="rest-slots"><i class="on"></i><i></i></span></span>
          </div>
          <div style="max-width:420px;margin-top:16px">${Z.weekStrip()}</div>
          <div style="max-width:540px;margin-top:16px;display:grid;gap:12px"><div class="bar"><i style="width:40%"></i></div><div class="dots"><i class="ok"></i><i class="bad"></i><i class="cur"></i><i></i><i></i></div></div>
        </section>

        <section><h2 class="t-h1">Course art</h2>
          <div class="ds-art">${(window.ZQArt && ZQArt.kinds ? ZQArt.kinds : ['die', 'tree', 'bars', 'bell', 'walk', 'matrix', 'payoff', 'layers', 'code', 'candles', 'scatter', 'balance', 'circle', 'surface', 'timer', 'graph']).map((k, i) => {
            const t = ['prob', 'maths', 'code', 'fin', 'ml', 'speed'][i % 6];
            return `<figure data-track="${t}"><div class="ds-art-box">${window.ZQArt ? ZQArt(k) : ''}</div><figcaption class="t-caption muted">${esc(k)}</figcaption></figure>`; }).join('')}</div>
        </section>

        <section id="ds-canvases"><h2 class="t-h1">Canvases</h2>
          <p class="t-body secondary ds-lead">Every registered canvas kind, drawn from the example in its README. Ids an author may highlight are listed in the spec.</p>
          <div class="ds-gal" data-gal="canvas"></div>
        </section>

        <section id="ds-widgets"><h2 class="t-h1">Widgets</h2>
          <p class="t-body secondary ds-lead">Every registered answer widget in a sample item. Fill answer applies the authored answer, Check grades it as a lesson would, Reset draws it again.</p>
          <div class="ds-gal" data-gal="widget"></div>
        </section>
      </div>`;

      const cleanups = [];
      const rng = (() => { let a = 7; return () => { a = (a + 0x6D2B79F5) >>> 0; let t = a; t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; })();
      const card = (kind, about, spec, body) => Z.h(`<article class="card ds-card" data-kind="${esc(kind)}" aria-labelledby="ds-k-${esc(kind)}">
          <header class="ds-card-h"><h3 class="ds-kind" id="ds-k-${esc(kind)}"><code>${esc(kind)}</code></h3>${about ? `<p class="t-caption muted">${esc(about)}</p>` : ''}</header>
          <div class="ds-card-b"></div>
          ${body || ''}
          ${spec ? `<details class="ds-spec"><summary class="t-caption">Spec</summary><pre class="t-code">${esc(pretty(spec))}</pre></details>` : ''}
        </article>`);
      const missing = (kind, what) => Z.h(`<article class="card ds-card is-missing" data-kind="${esc(kind)}"><header class="ds-card-h"><h3 class="ds-kind"><code>${esc(kind)}</code></h3></header>
          <p class="t-body ds-warn">${icon('flag', 'sm')}<span>No sample ${what} for this kind. Add one to js/screens/system.js.</span></p></article>`);

      /* Canvases */
      const cg = root.querySelector('[data-gal="canvas"]');
      canvasKinds.forEach(kind => {
        const s = CANVAS_SAMPLES[kind];
        if (!s) { cg.append(missing(kind, 'canvas')); return; }
        const spec = { kind, params: s.params, state: s.state };
        const el = card(kind, CANVAS_ABOUT[kind], spec);
        cg.append(el);
        const host = el.querySelector('.ds-card-b');
        try {
          const cv = Z.canvas.create(host, JSON.parse(JSON.stringify(spec)), { mode: 'lesson', rng, reducedMotion: Z.reducedMotion() });
          if (cv && cv.destroy) cleanups.push(() => { try { cv.destroy(); } catch (e) { /* already gone */ } });
        } catch (e) { console.error(`Canvas ${kind} failed`, e); host.innerHTML = `<p class="t-body ds-warn">${icon('flag', 'sm')}<span>This canvas threw: ${esc(e.message)}</span></p>`; }
      });
      Object.keys(CANVAS_SAMPLES).filter(k => !canvasKinds.includes(k)).forEach(k => cg.append(missing(k + ' (not registered)', 'renderer')));
      CANVAS_EXTRAS.forEach(x => {
        const el = card(x.name, x.about, x.spec);
        cg.append(el);
        try {
          const h = Z.player.renderItem({ id: 'ds-x', canvas: JSON.parse(JSON.stringify(x.spec)) }, el.querySelector('.ds-card-b'), { mode: 'set', key: 'ds-' + x.name });
          Z.mathify(el);
          cleanups.push(() => { try { h.destroy(); } catch (e) { /* gone */ } });
        } catch (e) { console.error(`Canvas ${x.name} failed`, e); }
      });

      /* Widgets */
      const wg = root.querySelector('[data-gal="widget"]');
      const mountWidget = (el, kind, item) => {
        const host = el.querySelector('.ds-card-b'), out = el.querySelector('.ds-out');
        if (el._h) { try { el._h.destroy(); } catch (e) { /* gone */ } el._h = null; }
        host.innerHTML = ''; out.textContent = ''; out.className = 't-caption ds-out';
        try {
          el._h = Z.player.renderItem(JSON.parse(JSON.stringify({ id: 'ds-' + kind, difficulty: 2, ...item })), host, { mode: 'set', key: 'ds-' + kind });
          Z.mathify(host);
        } catch (e) { console.error(`Widget ${kind} failed`, e); host.innerHTML = `<p class="t-body ds-warn">${icon('flag', 'sm')}<span>This widget threw: ${esc(e.message)}</span></p>`; }
      };
      const variants = WIDGET_EXTRAS.filter(x => widgetKinds.includes(x.kind));
      widgetKinds.concat(variants.map(x => x.name)).forEach(name => {
        const extra = variants.find(x => x.name === name);
        const kind = name, item = extra ? extra.item : WIDGET_SAMPLES[kind];
        if (!item) { wg.append(missing(kind, 'item')); return; }
        const lazy = kind === 'code', cpp = !!(extra && extra.item.widget && extra.item.widget.language === 'cpp'); // item 304: C++ cards load the compiler on request too
        const el = card(kind, null, item.widget || item, `<div class="ds-acts">
            ${lazy || cpp ? `<button type="button" class="btn secondary" data-load>${cpp ? 'Load the C++ compiler and render' : 'Load Python and render'}</button>` : ''}
            <button type="button" class="btn secondary" data-fill${lazy || cpp ? ' hidden' : ''}>Fill answer</button>
            <button type="button" class="btn" data-check${lazy || cpp ? ' hidden' : ''}>Check</button>
            <button type="button" class="link-btn" data-reset${lazy || cpp ? ' hidden' : ''}>Reset</button>
            <span class="t-caption ds-out" role="status" aria-live="polite"></span></div>`);
        wg.append(el);
        if (cpp) el.querySelector('.ds-card-b').innerHTML = '<p class="t-caption muted">The C++ code widget loads clang (about 26 MB) from the jsDelivr CDN, so it renders on request.</p>';
        else if (lazy) el.querySelector('.ds-card-b').innerHTML = '<p class="t-caption muted">The code widget loads Python (about 10 MB) from the jsDelivr CDN, so it renders on request.</p>';
        else mountWidget(el, kind, item);
        el.addEventListener('click', async (e) => {
          const out = el.querySelector('.ds-out');
          if (e.target.closest('[data-load]')) { e.target.closest('[data-load]').hidden = true; el.querySelectorAll('[data-fill], [data-check], [data-reset]').forEach(b => { b.hidden = false; }); mountWidget(el, kind, item); }
          else if (e.target.closest('[data-reset]')) mountWidget(el, kind, item);
          else if (e.target.closest('[data-fill]') && el._h) { const ok = el._h.answerCorrect();
            if (ok === false) { el._h.reveal(); out.className = 't-caption ds-out is-no'; out.textContent = 'This widget has no way to apply its authored answer (answerCorrect returned false), so it shows the solution instead.'; }
            else { out.className = 't-caption ds-out'; out.textContent = 'Answer applied.'; } }
          else if (e.target.closest('[data-check]') && el._h) {
            out.textContent = 'Checking…';
            try {
              const r = await el._h.check();
              if (r && r.pending) { out.textContent = 'Opened the next step. Check again to grade it.'; return; }
              out.className = 't-caption ds-out ' + (r && r.ok ? 'is-ok' : 'is-no');
              out.textContent = r ? (r.ok ? 'Correct.' : `Not yet${r.key != null ? `, key "${r.key}"` : ''}.`) : 'Nothing to check yet.';
            } catch (err) { out.textContent = 'Check threw: ' + err.message; }
          }
        });
        cleanups.push(() => { if (el._h) { try { el._h.destroy(); } catch (e) { /* gone */ } } });
      });
      Object.keys(WIDGET_SAMPLES).filter(k => !widgetKinds.includes(k)).forEach(k => wg.append(missing(k + ' (not registered)', 'widget')));

      /* Toolbar */
      root.querySelector('.ds-bar').addEventListener('change', (e) => {
        if (e.target.name === 'ds-theme') Z.setSetting('theme', e.target.value);
        if (e.target.name === 'ds-motion') Z.setSetting('motion', e.target.value);
      });
      root.querySelector('.ds-jump').addEventListener('click', (e) => {
        const a = e.target.closest('[data-jump]'); if (!a) return;
        e.preventDefault();
        const t = root.querySelector('#' + a.dataset.jump); if (t) t.scrollIntoView({ behavior: Z.reducedMotion() ? 'auto' : 'smooth', block: 'start' });
      });
      const off = Z.on('settings', (s) => {
        const pick = (name, v) => { const r = root.querySelector(`input[name="ds-${name}"][value="${v}"]`); if (r) r.checked = true; };
        pick('theme', s.theme); pick('motion', s.motion);
      });
      window.ZQSystem = { canvasKinds: () => canvasKinds.slice(), widgetKinds: () => widgetKinds.slice(), card: (k) => root.querySelector(`.ds-card[data-kind="${k}"]`) };
      return () => { cleanups.forEach(f => f()); if (typeof off === 'function') off(); delete window.ZQSystem; };
    },
  });
})();
