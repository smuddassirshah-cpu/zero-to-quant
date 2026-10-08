import fc from 'fast-check';
import { describe, expect, it } from 'vitest';
import {
  compile,
  MAX_DEPTH,
  MAX_LENGTH,
  MAX_TERMS,
  ParseError,
  parse,
  print,
  ScopeError,
  type Compiled,
  type ExprFunctions,
  type Node,
  type ParseErrorCode,
} from '@zq/mathcore/expr';
import { MATH } from './expr-table.ts';

type Fn = Extract<Node, { kind: 'call' }>['fn'];
// The one-argument functions of calc-linalg 2.3, restated from the paper.
const UNARY =
  'sin cos tan asin acos atan sinh cosh tanh exp ln log10 sqrt cbrt abs sign floor ceil Phi phi erf'.split(
    ' ',
  ) as Fn[];
const RESERVED = [...UNARY, 'atan2', 'min', 'max', 'if', 'sum', 'pi', 'e'];

const value = (src: string, scope: Record<string, number> = {}, fns = MATH): number =>
  compile(parse(src), fns).evaluate(scope);
const fails = (src: string): ParseError => {
  try {
    parse(src);
  } catch (err) {
    if (err instanceof ParseError) return err;
    throw err;
  }
  throw new Error(`${src} parsed`);
};
// Fully bracketed, to show the grouping.
const full = (n: Node): string =>
  n.kind === 'bin'
    ? `(${full(n.left)} ${n.op} ${full(n.right)})`
    : n.kind === 'neg'
      ? `(-${full(n.arg)})`
      : print(n);
const strip = (n: Node): unknown =>
  JSON.parse(JSON.stringify(n, (k, v: unknown) => (k === 'at' ? undefined : v)));

describe('parse', () => {
  it('groups as calc-linalg 2.3 and Python do', () => {
    const cases: [string, string][] = [
      ['1 + 2*3', '(1 + (2 * 3))'],
      ['1 - 2 - 3', '((1 - 2) - 3)'],
      ['8/4/2', '((8 / 4) / 2)'],
      ['8/4*2', '((8 / 4) * 2)'],
      ['2^3^2', '(2 ^ (3 ^ 2))'],
      ['-x^2', '(-(x ^ 2))'],
      ['2^-x^2', '(2 ^ (-(x ^ 2)))'],
      ['-a*b', '((-a) * b)'],
      ['a*-b', '(a * (-b))'],
      ['a - -b', '(a - (-b))'],
      ['--a', '(-(-a))'],
      ['(-a)^b', '((-a) ^ b)'],
      ['(a + b)*c', '((a + b) * c)'],
    ];
    for (const [src, grouped] of cases) expect(full(parse(src)), src).toBe(grouped);
  });

  it('reads decimal and scientific numbers, names, constants and white space', () => {
    expect(value(' .5 + 007\t+ 1.5e-3*2E+3\n')).toBe(10.5);
    expect(parse('1e5')).toEqual({ kind: 'num', value: 1e5, at: 0 });
    for (const name of ['x', 'x_1', 'W_t', 'lambda', 'theta', 'E', 'pi2'])
      expect(parse(name).kind).toBe('var');
    expect(value('pi + e')).toBe(Math.PI + Math.E);
    expect(parse('sin (x)')).toMatchObject({ kind: 'call', fn: 'sin' });
  });

  it('reports each error with its code and its position', () => {
    const cases: [string, ParseErrorCode, number][] = [
      ['', 'syntax', 0],
      ['1 +', 'syntax', 3],
      ['2x', 'syntax', 1],
      ['1.', 'character', 1],
      ['1 # 2', 'character', 2],
      ['x²', 'character', 1],
      ['2**3', 'syntax', 2],
      ['+1', 'syntax', 0],
      ['(1', 'syntax', 2],
      ['1)', 'syntax', 1],
      ['sin', 'reserved', 0],
      ['sum + 1', 'reserved', 0],
      ['foo(1)', 'function', 0],
      ['x(1)', 'function', 0],
      ['pi(1)', 'function', 0],
      ['sin(1, 2)', 'arity', 0],
      ['min(1)', 'arity', 0],
      ['x < 1', 'comparison', 2],
      ['if(x, 1, 2)', 'comparison', 4],
      ['if(1 < 2 < 3, 1, 2)', 'comparison', 9],
      ['if(1 < 2, 1)', 'syntax', 11],
      ['sum(pi, 1, 2, 3)', 'reserved', 4],
      ['sum(1, 1, 2, 3)', 'syntax', 4],
      ['1e999', 'number', 0],
      ['__proto__', 'character', 0],
      ['('.repeat(MAX_DEPTH + 1) + '1' + ')'.repeat(MAX_DEPTH + 1), 'depth', MAX_DEPTH],
      ['x'.repeat(MAX_LENGTH + 1), 'length', MAX_LENGTH],
    ];
    for (const [src, code, at] of cases) {
      const err = fails(src);
      expect([err.code, err.at], src).toEqual([code, at]);
      expect(err.message).toContain(`(at ${at})`);
    }
    expect(parse('('.repeat(MAX_DEPTH) + '1' + ')'.repeat(MAX_DEPTH))).toMatchObject({ kind: 'num' });
    expect(parse('x'.repeat(MAX_LENGTH))).toMatchObject({ kind: 'var' });
  });
});

const NAME = fc.stringMatching(/^[A-Za-z][A-Za-z0-9_]{0,3}$/).filter((s) => !RESERVED.includes(s));
const TREE = fc.letrec<{ node: Node }>((tie) => ({
  node: fc.oneof(
    { maxDepth: 5, depthSize: 'small' },
    fc.double({ min: 0, noNaN: true, noDefaultInfinity: true }).map((v): Node => ({
      kind: 'num',
      value: Math.abs(v),
      at: 0,
    })),
    fc.constantFrom('pi' as const, 'e' as const).map((name): Node => ({ kind: 'const', name, at: 0 })),
    NAME.map((name): Node => ({ kind: 'var', name, at: 0 })),
    tie('node').map((arg): Node => ({ kind: 'neg', arg, at: 0 })),
    fc
      .tuple(fc.constantFrom('+', '-', '*', '/', '^' as const), tie('node'), tie('node'))
      .map(([op, left, right]): Node => ({ kind: 'bin', op, left, right, at: 0 })),
    fc
      .tuple(fc.constantFrom(...UNARY), tie('node'))
      .map(([fn, arg]): Node => ({ kind: 'call', fn, args: [arg], at: 0 })),
    fc
      .tuple(
        fc.constantFrom('min', 'max', 'atan2' as const),
        fc.array(tie('node'), { minLength: 2, maxLength: 3 }),
      )
      .map(([fn, args]): Node => ({
        kind: 'call',
        fn,
        args: fn === 'atan2' ? args.slice(0, 2) : args,
        at: 0,
      })),
    fc
      .tuple(fc.constantFrom('<', '<=', '>', '>=', '=='), tie('node'), tie('node'), tie('node'), tie('node'))
      .map(([rel, left, right, then, otherwise]): Node => ({
        kind: 'if',
        rel,
        left,
        right,
        then,
        else: otherwise,
        at: 0,
      })),
    fc
      .tuple(NAME, tie('node'), tie('node'), tie('node'))
      .map(([index, lo, hi, term]): Node => ({ kind: 'sum', index, lo, hi, term, at: 0 })),
  ),
})).node;

describe('print', () => {
  it('writes the fewest brackets', () => {
    const cases: [string, string][] = [
      ['((a)) + (b*c)', 'a + b*c'],
      ['a - (b - c)', 'a - (b - c)'],
      ['a/(b*c)', 'a/(b*c)'],
      ['(2^3)^2', '(2^3)^2'],
      ['-(a*b) - -(c^d)', '-(a*b) - -c^d'],
      ['if(x<0,-x,x)', 'if(x < 0, -x, x)'],
      ['sum(k,1,n,k^2)+max(1,2,3)', 'sum(k, 1, n, k^2) + max(1, 2, 3)'],
      ['1e21 + 1e-7', '1e+21 + 1e-7'],
    ];
    for (const [src, printed] of cases) expect(print(parse(src)), src).toBe(printed);
  });

  it('round-trips every tree through its text', () => {
    fc.assert(
      fc.property(TREE, (tree) => {
        const src = print(tree);
        fc.pre(src.length <= MAX_LENGTH);
        expect(strip(parse(src))).toEqual(strip(tree));
      }),
      { numRuns: 500 },
    );
  });
});

describe('compile', () => {
  it('computes + - * and / in IEEE-754 doubles, with NaN for a zero divisor', () => {
    const c: Compiled = compile(parse('a + b*c - a/b'), MATH);
    expect(c.free).toEqual(['a', 'b', 'c']);
    fc.assert(
      fc.property(fc.double(), fc.double(), fc.double(), (a, b, c3) => {
        const expected = b === 0 ? NaN : a + b * c3 - a / b;
        expect(c.run([a, b, c3])).toBe(expected);
        expect(c.evaluate({ a, b, c: c3 })).toBe(expected);
      }),
    );
  });

  it('makes every undefined point NaN', () => {
    for (const src of [
      '1/0',
      '-1/-0',
      '0^-1',
      '1^(0/0)',
      '(0/0)^0',
      'ln(0)',
      'ln(-1)',
      'log10(-0)',
      'sqrt(-1)',
      'sin(0/0)',
      'atan2(0/0, 1)',
      'max(1, 0/0, 2)',
      'if(0/0 < 1, 1, 2)',
      'sum(k, 0.5, 2, k)',
      `sum(k, 1, ${MAX_TERMS + 1}, 1)`,
      'sum(k, 9007199254740992, 9007199254740992, 1)',
    ]) {
      expect(value(src), src).toBeNaN();
    }
    expect(value('0^0')).toBe(1);
    expect(value('ln(1e308*10)')).toBe(Infinity);
    expect(value('1e308*10')).toBe(Infinity);
  });

  it('takes ^ and the transcendental functions from the table, and the exact ones from IEEE-754', () => {
    const fns: ExprFunctions = { ...MATH, sin: () => 42, pow: () => 7, atan2: () => 9 };
    expect(value('sin(1) + 2^3 + atan2(1, 2)', {}, fns)).toBe(58);
    expect(value('abs(-3) + sign(-2) + floor(-2.5) + ceil(2.5) + min(4, 2, 3) + max(1, 5)')).toBe(9);
    for (const fn of UNARY) expect(value(`${fn}(0.5)`), fn).toBeGreaterThan(-1);
    expect(Object.is(value('min(0, -0)'), -0)).toBe(true);
    expect(Object.is(value('max(-0, 0)'), 0)).toBe(true);
    expect(Object.is(value('sign(-0)'), -0)).toBe(true);
    expect(() => compile(parse('erf(1)'), { ...MATH, erf: undefined } as unknown as ExprFunctions)).toThrow(
      TypeError,
    );
    const inherited = Object.assign(Object.create(MATH) as ExprFunctions, { sin: MATH.sin });
    expect(() => compile(parse('cos(1)'), inherited)).toThrow(TypeError);
    expect(compile(parse('sin(0)'), inherited).run([])).toBe(0);
  });

  it('evaluates only the branch if chooses', () => {
    const calls: string[] = [];
    const fns: ExprFunctions = {
      ...MATH,
      sin: () => (calls.push('sin'), 1),
      cos: () => (calls.push('cos'), 2),
    };
    const c = compile(parse('if(x < 0, sin(x), cos(x))'), fns);
    expect([c.run([-1]), c.run([1]), c.run([0])]).toEqual([1, 2, 2]);
    expect(calls).toEqual(['sin', 'cos', 'cos']);
    const rels = ['<', '<=', '>', '>=', '=='].map((rel) => value(`if(2 ${rel} 2, 1, 0)`));
    expect(rels).toEqual([0, 1, 0, 1, 1]);
  });

  it('sums from lo to hi with its own index, within one budget for the whole evaluation', () => {
    expect(value('sum(k, 1, n, 1/k)', { n: 4 })).toBe(1 + 1 / 2 + 1 / 3 + 1 / 4);
    expect(value('sum(k, 3, 2, k)')).toBe(0);
    expect(value('sum(x, 1, 3, x) + x', { x: 10 })).toBe(16);
    expect(value('sum(k, 1, k, k)', { k: 4 })).toBe(10);
    expect(value('sum(i, 1, 3, sum(i, 1, i, i))')).toBe(1 + 3 + 6);
    const inner = MAX_TERMS / 400 - 1;
    expect(value(`sum(i, 1, 400, sum(j, 1, ${inner}, 1))`)).toBe(400 * inner);
    expect(value(`sum(i, 1, 400, sum(j, 1, ${inner + 1}, 1))`)).toBeNaN();
    const c = compile(parse(`sum(k, 1, ${MAX_TERMS}, 1)`), MATH);
    expect([c.run([]), c.run([])]).toEqual([MAX_TERMS, MAX_TERMS]);
  });

  it('reads variables from the scope by own name only', () => {
    expect(() => value('x + y', { x: 1 })).toThrow(ScopeError);
    expect(() => value('x', { x: '1' } as unknown as Record<string, number>)).toThrow(/variable x/);
    expect(() => value('x', Object.create({ x: 1 }) as Record<string, number>)).toThrow(ScopeError);
    expect(value('x', Object.assign(Object.create(null) as Record<string, number>, { x: 2 }))).toBe(2);
    expect(value('constructor + prototype', { constructor: 1, prototype: 2 })).toBe(3);
    const c = compile(parse('x - y'), MATH);
    expect(c.run([5, 3])).toBe(2);
    expect(() => c.run([5])).toThrow(RangeError);
  });

  it('gives the same bits on every evaluation', () => {
    fc.assert(
      fc.property(TREE, fc.double(), (tree, x) => {
        const c = compile(tree, MATH);
        const values = c.free.map(() => x);
        expect(c.run(values)).toBe(c.run(values));
      }),
      { numRuns: 300 },
    );
  });
});

describe('untrusted text', () => {
  const tokens = [
    ...'0123456789.eE+-*/^(),<>= _\t#[]{}xyzk'.split(''),
    'pi',
    'sin',
    'min',
    'atan2',
    'if',
    'sum',
    '<=',
  ];
  const unsafe = ['__proto__', 'constructor', 'prototype', 'toString', 'valueOf', 'hasOwnProperty', 'canary'];
  const text = fc.oneof(
    fc.string({ unit: fc.constantFrom(...tokens, ...unsafe), maxLength: 40 }),
    fc.string({ unit: 'binary', maxLength: 40 }),
  );

  it('throws nothing but ParseError, and what parses evaluates to a number', () => {
    fc.assert(
      fc.property(text, (src) => {
        let tree: Node;
        try {
          tree = parse(src);
        } catch (err) {
          expect(err).toBeInstanceOf(ParseError);
          return;
        }
        const c = compile(tree, MATH);
        expect(typeof c.run(c.free.map(() => 1.5))).toBe('number');
      }),
      { numRuns: 3000 },
    );
  });

  it('parses, prints, compiles and evaluates the deepest trees the limits allow', () => {
    const n = (MAX_LENGTH - 1) / 2;
    for (const src of ['-'.repeat(MAX_LENGTH - 1) + '1', '2^'.repeat(n) + '1', '1' + '-1'.repeat(n)]) {
      const tree = parse(src);
      const text = print(tree);
      if (text.length <= MAX_LENGTH) expect(strip(parse(text))).toEqual(strip(tree));
      expect(typeof compile(tree, MATH).run([])).toBe('number');
    }
    expect(value('-'.repeat(MAX_LENGTH - 1) + '1')).toBe(-1);
  });

  it('never reads or writes Object.prototype', () => {
    const before = Object.getOwnPropertyNames(Object.prototype);
    Object.defineProperty(Object.prototype, 'canary', { value: 7, configurable: true, writable: true });
    try {
      for (const name of unsafe.slice(1)) {
        expect(() => value(name), name).toThrow(ScopeError);
        expect(value(name, { [name]: 3 })).toBe(3);
        expect(fails(`${name}(1)`).code).toBe('function');
      }
      expect(fails('__proto__').code).toBe('character');
      fc.assert(
        fc.property(text, (src) => {
          try {
            const c = compile(parse(src), MATH);
            c.evaluate(Object.fromEntries(c.free.filter((n) => n !== 'canary').map((n) => [n, 1])));
          } catch (err) {
            if (!(err instanceof ParseError || (err instanceof ScopeError && err.variable === 'canary')))
              throw err;
          }
        }),
        { numRuns: 2000 },
      );
    } finally {
      Reflect.deleteProperty(Object.prototype, 'canary');
    }
    expect(Object.getOwnPropertyNames(Object.prototype)).toEqual(before);
  });
});
