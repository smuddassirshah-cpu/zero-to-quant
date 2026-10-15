import fc from 'fast-check';
import { describe, expect, it } from 'vitest';
import {
  compile,
  MAX_DEPTH,
  MAX_LENGTH,
  MAX_WORK,
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
    // At most 20 significant digits, counted from the first non-zero digit to the last (RoundMVResult).
    for (const src of [
      '12345678901234567890',
      '0.00012345678901234567890e3',
      '100000000000000000000000000',
      '1.000000000000000000000000000',
      '0.0000000000000000000000000001',
      '0000000000000000000000000000',
    ]) {
      expect(parse(src), src).toMatchObject({ kind: 'num', value: Number(src) });
    }
    expect([value('100000000000000000000000000'), value('1.000000000000000000000000000')]).toEqual([1e26, 1]);
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
      ['x + 123456789012345678901', 'number', 4],
      ['1.00000000000000011102230246251565404236316680908203125', 'number', 0],
      ['.100000000000000000001e5', 'number', 0],
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
const tree = (num: fc.Arbitrary<number>): fc.Arbitrary<Node> =>
  fc.letrec<{ node: Node }>((tie) => ({
    node: fc.oneof(
      { maxDepth: 5, depthSize: 'small' },
      num.map((value): Node => ({ kind: 'num', value, at: 0 })),
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
        .tuple(
          fc.constantFrom('<', '<=', '>', '>=', '=='),
          tie('node'),
          tie('node'),
          tie('node'),
          tie('node'),
        )
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
// The trees parse builds, whose numbers are finite and neither negative nor -0, and trees over any double.
const TREE = tree(fc.double({ min: 0, noNaN: true, noDefaultInfinity: true }).map(Math.abs));
const ANY_TREE = tree(fc.double());
const nums = (n: Node): number[] =>
  n.kind === 'num'
    ? [n.value]
    : n.kind === 'const' || n.kind === 'var'
      ? []
      : n.kind === 'neg'
        ? nums(n.arg)
        : n.kind === 'call'
          ? n.args.flatMap(nums)
          : n.kind === 'sum'
            ? [n.lo, n.hi, n.term].flatMap(nums)
            : n.kind === 'if'
              ? [n.left, n.right, n.then, n.else].flatMap(nums)
              : [n.left, n.right].flatMap(nums);

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
      fc.property(TREE, (t) => {
        const src = print(t);
        fc.pre(src.length <= MAX_LENGTH);
        expect(strip(parse(src))).toEqual(strip(t));
      }),
      { numRuns: 500 },
    );
  });

  it('refuses, as compile does, a tree parse does not build', () => {
    const num = (value: number): Node => ({ kind: 'num', value, at: 0 });
    const x: Node = { kind: 'var', name: 'x', at: 0 };
    const bad: unknown[] = [
      { kind: 'bin', op: '^', left: num(-1), right: num(2), at: 0 },
      { kind: 'call', fn: 'atan2', args: [num(0), num(-0)], at: 0 },
      num(Infinity),
      num(NaN),
      { kind: 'var', name: 'x y', at: 0 },
      { kind: 'var', name: 'sin', at: 0 },
      { kind: 'var', name: '__proto__', at: 0 },
      { kind: 'const', name: 'tau', at: 0 },
      { kind: 'bin', op: 'constructor', left: x, right: x, at: 0 },
      { kind: 'call', fn: 'constructor', args: [x], at: 0 },
      { kind: 'call', fn: 'atan2', args: [x], at: 0 },
      { kind: 'if', rel: '!=', left: x, right: x, then: x, else: x, at: 0 },
      { kind: 'sum', index: 'pi', lo: x, hi: x, term: x, at: 0 },
      { kind: 'toString', at: 0 },
    ];
    for (const n of bad as Node[]) {
      expect(() => print(n), JSON.stringify(n)).toThrow(RangeError);
      expect(() => compile(n, MATH), JSON.stringify(n)).toThrow(RangeError);
    }
    // Over any double: a tree with a negative, -0 or non-finite number is refused, and any other round-trips.
    fc.assert(
      fc.property(ANY_TREE, (t) => {
        if (nums(t).every((v) => Number.isFinite(v) && (v > 0 || Object.is(v, 0)))) {
          const src = print(t);
          fc.pre(src.length <= MAX_LENGTH);
          expect(strip(parse(src))).toEqual(strip(t));
        } else {
          expect(() => print(t)).toThrow(RangeError);
          expect(() => compile(t, MATH)).toThrow(RangeError);
        }
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
      `sum(k, 1, ${MAX_WORK + 1}, 1)`,
      'sum(k, 9007199254740992, 9007199254740992, 1)',
    ]) {
      expect(value(src), src).toBeNaN();
    }
    expect(value('0^0')).toBe(1);
    expect(value('ln(1e308*10)')).toBe(Infinity);
    expect(Object.is(value('sqrt(-0)'), -0)).toBe(true);
    expect(value('1e308*10')).toBe(Infinity);
  });

  it('takes ^ and the transcendental functions from the table, and the exact ones from IEEE-754', () => {
    const fns: ExprFunctions = { ...MATH, sin: () => 42, pow: () => 7, atan2: () => 9 };
    expect(value('sin(1) + 2^3 + atan2(1, 2)', {}, fns)).toBe(58);
    expect(value('abs(-3) + sign(-2) + floor(-2.5) + ceil(2.5) + min(4, 2, 3) + max(1, 5)')).toBe(9);
    expect(value('sqrt(2)', {}, fns)).toBe(Math.SQRT2);
    expect(compile(parse('sqrt(x)'), MATH).run([1e-300])).toBe(1e-150);
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

  it('fixes (+-1)^(+-Infinity) at 1, which the table does not decide', () => {
    // Math.pow gives NaN here (ECMA-262), C99 and dmath give 1; a table pow that answers 7 is never asked.
    for (const fns of [MATH, { ...MATH, pow: () => 7 }]) {
      for (const src of ['1^(1e308*10)', '1^(-1e308*10)', '(-1)^(1e308*10)', '(-1)^(-1e308*10)']) {
        expect(value(src, {}, fns), src).toBe(1);
      }
      expect(value('1^(0/0)', {}, fns)).toBeNaN();
      expect(value('(-1)^x', { x: 2 }, fns)).toBe(fns === MATH ? 1 : 7);
    }
    expect(value('2^(1e308*10) + 0.5^(1e308*10)')).toBe(Infinity);
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
    // A sum costs its count times its term's nodes: 500 here (if, k, 0, 495 minus signs and k, 1), so 2,000
    // terms cost MAX_WORK exactly, though only four nodes of each run.
    const wide = (hi: number): string => `sum(k, 1, ${hi}, if(k < 0, ${'-'.repeat(495)}k, 1))`;
    expect(value(wide(MAX_WORK / 500))).toBe(MAX_WORK / 500);
    expect(value(wide(MAX_WORK / 500 + 1))).toBeNaN();
    // The outer sum costs 400 times 4 (the inner sum, 1, its hi, 1), and each inner one its count.
    const inner = (MAX_WORK - 1600) / 400;
    expect(value(`sum(i, 1, 400, sum(j, 1, ${inner}, 1))`)).toBe(400 * inner);
    expect(value(`sum(i, 1, 400, sum(j, 1, ${inner + 1}, 1))`)).toBeNaN();
    const c = compile(parse(`sum(k, 1, ${MAX_WORK}, 1)`), MATH);
    expect([c.run([]), c.run([])]).toEqual([MAX_WORK, MAX_WORK]);
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

  it('charges the costliest terms their nodes, so they run at most MAX_WORK node visits', () => {
    // A term's nodes, and the table calls among them (a table function, or ^), counted apart from compile's
    // own count. The terms hold no if or sum.
    const TABLE: ReadonlySet<string> = new Set(Object.keys(MATH));
    const count = (n: Node): readonly [number, number] => {
      const kids: readonly Node[] =
        n.kind === 'neg' ? [n.arg] : n.kind === 'bin' ? [n.left, n.right] : n.kind === 'call' ? n.args : [];
      const fromTable = (n.kind === 'call' && TABLE.has(n.fn)) || (n.kind === 'bin' && n.op === '^');
      return kids.map(count).reduce(([a, b], [c, d]) => [a + c, b + d], [1, fromTable ? 1 : 0]);
    };
    // Every function of the table counts its calls and returns 1, so the check is exact and fast. Time per
    // node is the table's, measured in expr.ts's notes and not tested: the 1 s bound this test once had failed
    // at 1,047 to 1,900 ms under coverage at load averages of 8 to 20 on a shared 4-core machine [measured].
    let calls = 0;
    const tally = (): number => {
      calls++;
      return 1;
    };
    const counting = Object.fromEntries(Object.keys(MATH).map((f) => [f, tally])) as Record<
      keyof ExprFunctions,
      typeof tally
    >;
    const chain = (unit: string, sep: string): string =>
      Array.from({ length: Math.floor(960 / (unit.length + sep.length)) }, () => unit).join(sep);
    // erf is the test table's costliest node; sin at 1e9 and pow, dmath's [measured: expr.ts's notes].
    const terms = [
      ...['erf(.5)', 'Phi(.5)', 'sin(1e9)', '1.5^1023.9', 'k^k', 'cbrt(k)', 'atan2(k, k)'].map((u) =>
        chain(u, '+'),
      ),
      chain('k', '*'),
      `max(${chain('k', ',')})`,
      '-'.repeat(959) + 'k',
    ];
    for (const term of terms) {
      const [nodes, perTerm] = count(parse(term));
      const hi = Math.floor(MAX_WORK / nodes);
      const rest = MAX_WORK - hi * nodes;
      // The first sum spends `fill` one-node terms; with fill = rest, the second costs what is left exactly.
      const src = (fill: number): string => `sum(j,1,${fill},1)+sum(k,1,${hi},${term})`;
      expect(src(rest + 1).length).toBeLessThanOrEqual(MAX_LENGTH);
      calls = 0;
      expect(compile(parse(src(rest)), counting).run([]), term.slice(0, 20)).not.toBeNaN();
      expect(calls, term.slice(0, 20)).toBe(hi * perTerm);
      calls = 0;
      expect(compile(parse(src(rest + 1)), counting).run([])).toBeNaN();
      expect(calls).toBe(0);
    }
    // The notes' times were measured at this budget, so a larger one needs measuring again.
    expect(MAX_WORK).toBeLessThanOrEqual(1_000_000);
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
