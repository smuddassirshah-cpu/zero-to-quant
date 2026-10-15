// The expression language of calc-linalg 2.3 (docs/blueprint/work/widgets-calc-linalg.md; ARCHITECTURE.md
// 4.3): parse to a tree, print it back, compile it to closures. Decision notes:
// - Grammar, loosest first: expr = term {(+|-) term}; term = unary {(*|/) unary}; unary = - unary | power;
//   power = primary [^ unary]; primary = number | name | name(args) | (expr). So -x^2 is -(x^2), 2^-1 is a
//   half and ^ groups to the right, as in Python. A comparison < <= > >= == is only the first argument of
//   if [our choice: the grammar's unstated details, this paragraph and the next].
// - Numbers: digits with an optional fraction (".5" too, "1." not) and exponent, with at most 20 significant
//   digits, since ECMA-262 lets an engine round a longer literal either way (RoundMVResult [sourced]); a
//   literal that rounds to infinity is an error. Names: ASCII letter, then letters, digits and "_". Function
//   names, if, sum, pi and e are reserved.
// - A tree is one parse can build: finite numbers that are neither negative nor -0 (a minus is a neg node),
//   names in the grammar, known functions with their arity. print and compile refuse any other with
//   RangeError, so a builder (MathJSON, d/dx) writes -1 as neg(num 1), and print's text parses back to it.
// - No eval, no Function. The only property reads are the caller's scope (own properties, by Object.hasOwn)
//   and the caller's function table (own properties, checked at compile); the grammar's names live in a Map
//   and Sets.
// - The transcendental functions and ^ come from an ExprFunctions table, so an expression is deterministic
//   when its table is (dmath's, once dmath covers the list). abs, sign, floor, ceil, min, max and sqrt are
//   built in, since ECMA-262 defines each exactly (sec-math.sqrt: the correctly rounded root [sourced]).
// - Undefined points are NaN (2.3): a / 0; 0 ^ b for b < 0; ln and log10 of x <= 0; any NaN operand, even
//   where pow or a table function would map it to a number; an if whose comparison has a NaN side; a sum
//   whose bounds are not safe integers; and any evaluation whose sums would cost more than MAX_WORK in all.
//   Every operation propagates NaN, so a sum refused for the budget makes the whole value NaN.
// - ^ is the table's pow except where ECMA-262 and C99 Annex F differ, which the language fixes: NaN for a
//   NaN operand (C99 gives 1 for 1^NaN, both give 1 for NaN^0) and 1 for (+-1)^(+-Infinity) (ECMA-262 gives
//   NaN; C99, dmath and Python give 1) [our choice]. The two agree on every other special value [sourced:
//   ECMA-262 Number::exponentiate; recalled: C99 F.9.4.4], so a conforming table changes only rounding.
// - Untrusted text (the tutor's compute tool, PLAN.md 7.2) is bounded: MAX_LENGTH characters and MAX_DEPTH
//   nested brackets, so parse and compile are O(n) with recursion at most n deep. A sum costs its term count
//   times its term's node count (counted at compile), within MAX_WORK per evaluation, so an evaluation visits
//   at most n + MAX_WORK nodes; the tests count that, not time it. AI-TUTOR.md 5.3.2 gives compute 2 s. A
//   MAX_WORK budget of the costliest nodes found took, in Node 22.22.0: 67 to 111 ms of erf with the test
//   table, 109 to 200 ms of dmath's sin at 1e9 or 4e15 (the Payne-Hanek reduction) and 66 to 138 ms of dmath's
//   pow [measured: here at a load average of 10, and by the adversarial review of 8 October 2026]. That leaves
//   a phone several times slower inside the limit [inferred] [our choice: the limits].
// - A compiled expression keeps its variables in cells its closures share, so it is not re-entrant: a table
//   function must not evaluate the same compiled expression.

export const MAX_LENGTH = 1000;
export const MAX_DEPTH = 32;
export const MAX_WORK = 1_000_000;
const MAX_DIGITS = 20;

// prettier-ignore
const TABLE = [
  'sin', 'cos', 'tan', 'asin', 'acos', 'atan', 'sinh', 'cosh', 'tanh', 'exp', 'ln', 'log10', 'cbrt', 'Phi',
  'phi', 'erf',
] as const;
type Unary = (x: number) => number;
type Binary = (a: number, b: number) => number;
/** The functions an expression takes from its caller: dmath's, or any other deterministic set. */
export type ExprFunctions = Readonly<Record<(typeof TABLE)[number], Unary>> & {
  readonly atan2: Binary;
  readonly pow: Binary;
};
type Fn = (typeof TABLE)[number] | 'abs' | 'sign' | 'floor' | 'ceil' | 'sqrt' | 'atan2' | 'min' | 'max';
type Rel = '<' | '<=' | '>' | '>=' | '==';

/**
 * A parsed expression; `at` is the offset of its first character, or of its operator. A num's value is
 * finite and neither negative nor -0, and names are as parse reads them; print and compile throw RangeError
 * otherwise.
 */
export type Node = Readonly<
  { at: number } & (
    | { kind: 'num'; value: number }
    | { kind: 'const'; name: 'pi' | 'e' }
    | { kind: 'var'; name: string }
    | { kind: 'neg'; arg: Node }
    | { kind: 'bin'; op: '+' | '-' | '*' | '/' | '^'; left: Node; right: Node }
    | { kind: 'call'; fn: Fn; args: readonly Node[] }
    | { kind: 'if'; rel: Rel; left: Node; right: Node; then: Node; else: Node }
    | { kind: 'sum'; index: string; lo: Node; hi: Node; term: Node }
  )
>;

const ARITY = new Map<string, readonly [number, number]>([
  ...[...TABLE, 'abs', 'sign', 'floor', 'ceil', 'sqrt'].map((name) => [name, [1, 1]] as const),
  ['atan2', [2, 2]],
  ['min', [2, Infinity]],
  ['max', [2, Infinity]],
]);
const RESERVED: ReadonlySet<string> = new Set([...ARITY.keys(), 'if', 'sum', 'pi', 'e']);
const RELS: ReadonlySet<string> = new Set(['<', '<=', '>', '>=', '==']);
const OPS: ReadonlySet<string> = new Set(['+', '-', '*', '/', '^']);
const CONSTANTS: ReadonlySet<string> = new Set(['pi', 'e']);
const isFn = (name: string): name is Fn => ARITY.has(name);
const isRel = (t: string): t is Rel => RELS.has(t);

export type ParseErrorCode =
  | 'length' // longer than MAX_LENGTH
  | 'depth' // parentheses nested deeper than MAX_DEPTH
  | 'character' // a character outside the grammar
  | 'number' // a literal with more than 20 significant digits, or one that rounds to infinity
  | 'syntax' // a token where the grammar has none
  | 'function' // an unknown function
  | 'arity' // a function with the wrong number of arguments
  | 'reserved' // a function, if, sum, pi or e where a variable belongs
  | 'comparison'; // a comparison anywhere but the first argument of if, or an if without one

/** The only error parse throws; `at` is the offset where the source goes wrong. */
export class ParseError extends Error {
  override readonly name = 'ParseError';
  readonly code: ParseErrorCode;
  readonly at: number;
  constructor(code: ParseErrorCode, at: number, message: string) {
    super(`${message} (at ${at})`);
    this.code = code;
    this.at = at;
  }
}

/** Thrown by `evaluate` when the scope has no own number for a free variable. */
export class ScopeError extends Error {
  override readonly name = 'ScopeError';
  readonly variable: string;
  constructor(variable: string) {
    super(`no value for the variable ${variable}`);
    this.variable = variable;
  }
}

interface Token {
  readonly t: string; // 'num', 'name', 'end' or the operator itself
  readonly v: string;
  readonly at: number;
}

const isDigit = (c: number): boolean => c >= 48 && c <= 57;
const isLetter = (c: number): boolean => (c | 32) >= 97 && (c | 32) <= 122;

function tokenise(src: string): Token[] {
  const out: Token[] = [];
  const digitsFrom = (k: number): number => {
    while (isDigit(src.charCodeAt(k))) k++;
    return k;
  };
  let i = 0;
  while (i < src.length) {
    const c = src.charCodeAt(i);
    const start = i;
    if (c === 32 || c === 9 || c === 10 || c === 13) {
      i++;
      continue;
    }
    if (isDigit(c) || (c === 46 && isDigit(src.charCodeAt(i + 1)))) {
      i = digitsFrom(i);
      if (src.charCodeAt(i) === 46 && isDigit(src.charCodeAt(i + 1))) i = digitsFrom(i + 1);
      if ((src.charCodeAt(i) | 32) === 101) {
        const j = i + (src[i + 1] === '+' || src[i + 1] === '-' ? 2 : 1);
        if (isDigit(src.charCodeAt(j))) i = digitsFrom(j);
      }
      out.push({ t: 'num', v: src.slice(start, i), at: start });
    } else if (isLetter(c)) {
      while (isLetter(src.charCodeAt(i)) || isDigit(src.charCodeAt(i)) || src[i] === '_') i++;
      out.push({ t: 'name', v: src.slice(start, i), at: start });
    } else {
      const two = src.slice(i, i + 2);
      const op = two === '<=' || two === '>=' || two === '==' ? two : src.charAt(i);
      if (op.length === 1 && !'+-*/^(),<>'.includes(op)) {
        throw new ParseError('character', i, `unexpected character ${JSON.stringify(op)}`);
      }
      out.push({ t: op, v: op, at: start });
      i += op.length;
    }
  }
  return out;
}

/** Parses source text in the grammar of calc-linalg 2.3; throws only ParseError. */
export function parse(source: string): Node {
  if (source.length > MAX_LENGTH) {
    throw new ParseError('length', MAX_LENGTH, `longer than ${MAX_LENGTH} characters`);
  }
  const tokens = tokenise(source);
  const end: Token = { t: 'end', v: '', at: source.length };
  let i = 0;
  let depth = 0;
  const peek = (): Token => tokens[i] ?? end;
  const unexpected = (tok: Token): ParseError =>
    isRel(tok.t)
      ? new ParseError('comparison', tok.at, 'a comparison belongs only first in if(a < b, then, else)')
      : new ParseError('syntax', tok.at, tok.t === 'end' ? 'unexpected end' : `unexpected ${tok.v}`);
  const take = (t: string): Token => {
    const tok = peek();
    if (tok.t !== t) throw unexpected(tok);
    i++;
    return tok;
  };
  const open = (): void => {
    const tok = take('(');
    if (++depth > MAX_DEPTH) throw new ParseError('depth', tok.at, `more than ${MAX_DEPTH} nested brackets`);
  };
  const close = (): void => {
    take(')');
    depth--;
  };

  const binary = (operand: () => Node, ops: readonly ('+' | '-' | '*' | '/')[]): Node => {
    let left = operand();
    for (;;) {
      const tok = peek();
      const op = ops.find((o) => o === tok.t);
      if (op === undefined) return left;
      i++;
      left = { kind: 'bin', op, left, right: operand(), at: tok.at };
    }
  };
  const expr = (): Node => binary(term, ['+', '-']);
  const term = (): Node => binary(unary, ['*', '/']);
  const unary = (): Node => {
    const tok = peek();
    if (tok.t === '-') {
      i++;
      return { kind: 'neg', arg: unary(), at: tok.at };
    }
    const base = primary();
    const hat = peek();
    if (hat.t !== '^') return base;
    i++;
    return { kind: 'bin', op: '^', left: base, right: unary(), at: hat.at };
  };
  const primary = (): Node => {
    const tok = peek();
    if (tok.t === 'num') {
      i++;
      if (significant(tok.v) > MAX_DIGITS) {
        throw new ParseError('number', tok.at, `${tok.v} has more than ${MAX_DIGITS} significant digits`);
      }
      const value = Number(tok.v);
      if (value === Infinity) throw new ParseError('number', tok.at, `${tok.v} is too large`);
      return { kind: 'num', value, at: tok.at };
    }
    if (tok.t === '(') {
      open();
      const inner = expr();
      close();
      return inner;
    }
    if (tok.t !== 'name') throw unexpected(tok);
    i++;
    if (peek().t === '(') return call(tok);
    if (tok.v === 'pi' || tok.v === 'e') return { kind: 'const', name: tok.v, at: tok.at };
    if (RESERVED.has(tok.v)) throw new ParseError('reserved', tok.at, `${tok.v} needs its arguments`);
    return { kind: 'var', name: tok.v, at: tok.at };
  };
  const call = (tok: Token): Node => {
    const name = tok.v;
    let node: Node;
    if (name === 'if') {
      open();
      const left = expr();
      const rel = peek();
      if (!isRel(rel.t)) throw new ParseError('comparison', rel.at, 'if needs a comparison first');
      i++;
      const right = expr();
      take(',');
      const then = expr();
      take(',');
      node = { kind: 'if', rel: rel.t, left, right, then, else: expr(), at: tok.at };
    } else if (name === 'sum') {
      open();
      const index = take('name');
      if (RESERVED.has(index.v)) throw new ParseError('reserved', index.at, `${index.v} cannot be an index`);
      take(',');
      const lo = expr();
      take(',');
      const hi = expr();
      take(',');
      node = { kind: 'sum', index: index.v, lo, hi, term: expr(), at: tok.at };
    } else {
      const arity = ARITY.get(name);
      if (arity === undefined || !isFn(name)) {
        throw new ParseError('function', tok.at, `${name} is not a function`);
      }
      open();
      const args = [expr()];
      while (peek().t === ',') {
        i++;
        args.push(expr());
      }
      if (args.length < arity[0] || args.length > arity[1]) {
        throw new ParseError('arity', tok.at, `${name} takes ${arity.join(' to ')} arguments`);
      }
      node = { kind: 'call', fn: name, args, at: tok.at };
    }
    close();
    return node;
  };

  const tree = expr();
  if (peek().t !== 'end') throw unexpected(peek());
  return tree;
}

/** The digits of a literal's mantissa from its first non-zero digit to its last, as RoundMVResult counts. */
function significant(literal: string): number {
  const mantissa = literal.replace(/e.*/i, '').replace('.', '');
  return /[1-9](?:\d*[1-9])?/.exec(mantissa)?.[0].length ?? 0;
}

const isName = (name: unknown): boolean =>
  typeof name === 'string' && /^[A-Za-z][A-Za-z0-9_]*$/.test(name) && !RESERVED.has(name);
function valid(n: Node): boolean {
  switch (n.kind) {
    case 'num':
      return Number.isFinite(n.value) && (n.value > 0 || Object.is(n.value, 0));
    case 'const':
      return CONSTANTS.has(n.name);
    case 'var':
      return isName(n.name);
    case 'neg':
      return true;
    case 'bin':
      return OPS.has(n.op);
    case 'call': {
      const arity = ARITY.get(n.fn);
      return arity !== undefined && n.args.length >= arity[0] && n.args.length <= arity[1];
    }
    case 'if':
      return RELS.has(n.rel);
    case 'sum':
      return isName(n.index);
    default:
      return false;
  }
}
/** Throws RangeError unless parse could have built this node; print and compile check every node. */
function check(n: Node): void {
  if (!valid(n))
    throw new RangeError(`a ${String((n as { kind?: unknown }).kind)} node that parse does not build`);
}

const level = (n: Node): number =>
  n.kind === 'neg' ? 3 : n.kind !== 'bin' ? 5 : n.op === '^' ? 4 : n.op === '*' || n.op === '/' ? 2 : 1;

/**
 * Source text that parses back to the same tree, with the fewest brackets; RangeError for a tree parse does
 * not build. It can be longer than the text the tree came from (spaces round + and -, numbers in their
 * shortest round-trip form), so near MAX_LENGTH it may not parse again.
 */
export function print(node: Node): string {
  check(node);
  const wrap = (n: Node, min: number): string => (level(n) < min ? `(${print(n)})` : print(n));
  switch (node.kind) {
    case 'num':
      return String(node.value);
    case 'const':
    case 'var':
      return node.name;
    case 'neg':
      return `-${wrap(node.arg, 3)}`;
    case 'bin': {
      if (node.op === '^') return `${wrap(node.left, 5)}^${wrap(node.right, 3)}`;
      const l = level(node);
      return `${wrap(node.left, l)}${l === 1 ? ` ${node.op} ` : node.op}${wrap(node.right, l + 1)}`;
    }
    case 'call':
      return `${node.fn}(${node.args.map(print).join(', ')})`;
    case 'if':
      return `if(${print(node.left)} ${node.rel} ${print(node.right)}, ${print(node.then)}, ${print(node.else)})`;
    case 'sum':
      return `sum(${node.index}, ${print(node.lo)}, ${print(node.hi)}, ${print(node.term)})`;
  }
}

export interface Compiled {
  /** The free variables, in order of first appearance. */
  readonly free: readonly string[];
  /** Evaluates with the values of `free`, in its order: the hot path for samplers. */
  run(values: readonly number[]): number;
  /** Evaluates with each free variable read from the scope's own properties. */
  evaluate(scope: Readonly<Record<string, number>>): number;
}

interface Cell {
  v: number;
}
type Code = () => number;
const NAN: Code = () => NaN;

function own<K extends keyof ExprFunctions>(fns: ExprFunctions, name: K): ExprFunctions[K] {
  const f: unknown = Object.hasOwn(fns, name) ? fns[name] : undefined;
  if (typeof f !== 'function') throw new TypeError(`the function table has no function ${name}`);
  return f as ExprFunctions[K];
}

const eitherNaN = (x: number, y: number): boolean => Number.isNaN(x) || Number.isNaN(y);
const divide = (x: number, y: number): number => (y === 0 ? NaN : x / y);
const holds = (rel: Rel, x: number, y: number): boolean =>
  rel === '<' ? x < y : rel === '<=' ? x <= y : rel === '>' ? x > y : rel === '>=' ? x >= y : x === y;

/**
 * Compiles a tree to closures over the given function table, which must hold every function it calls;
 * RangeError for a tree parse does not build.
 */
export function compile(node: Node, fns: ExprFunctions): Compiled {
  const free = new Map<string, Cell>();
  let budget = 0;
  let nodes = 0;
  const cell = (name: string, bound: ReadonlyMap<string, Cell>): Cell => {
    let c = bound.get(name) ?? free.get(name);
    if (c === undefined) free.set(name, (c = { v: NaN }));
    return c;
  };
  const build = (n: Node, bound: ReadonlyMap<string, Cell>): Code => {
    check(n);
    nodes++;
    const sub = (m: Node): Code => build(m, bound);
    switch (n.kind) {
      case 'num':
      case 'const': {
        const v = n.kind === 'num' ? n.value : n.name === 'pi' ? Math.PI : Math.E;
        return () => v;
      }
      case 'var': {
        const c = cell(n.name, bound);
        return () => c.v;
      }
      case 'neg': {
        const a = sub(n.arg);
        return () => -a();
      }
      case 'bin': {
        const a = sub(n.left);
        const b = sub(n.right);
        if (n.op === '+') return () => a() + b();
        if (n.op === '-') return () => a() - b();
        if (n.op === '*') return () => a() * b();
        if (n.op === '/') return () => divide(a(), b());
        const pow = own(fns, 'pow');
        const power = (x: number, y: number): number =>
          eitherNaN(x, y) || (x === 0 && y < 0)
            ? NaN
            : (x === 1 || x === -1) && !Number.isFinite(y)
              ? 1
              : pow(x, y);
        return () => power(a(), b());
      }
      case 'call':
        return call(n.fn, n.args.map(sub));
      case 'if': {
        const [l, r, t, e] = [n.left, n.right, n.then, n.else].map(sub) as [Code, Code, Code, Code];
        const rel = n.rel;
        const choose = (x: number, y: number): number =>
          eitherNaN(x, y) ? NaN : holds(rel, x, y) ? t() : e();
        return () => choose(l(), r());
      }
      case 'sum': {
        const lo = sub(n.lo);
        const hi = sub(n.hi);
        const k: Cell = { v: NaN };
        const before = nodes;
        const term = build(n.term, new Map(bound).set(n.index, k));
        const size = nodes - before;
        return () => {
          const a = lo();
          const b = hi();
          if (!Number.isSafeInteger(a) || !Number.isSafeInteger(b)) return NaN;
          const count = Math.max(0, b - a + 1);
          const cost = count * size;
          if (cost > budget) return NaN;
          budget -= cost;
          let total = 0;
          for (let j = 0; j < count; j++) {
            k.v = a + j;
            total += term();
          }
          return total;
        };
      }
    }
  };
  // The parser guarantees each function's arity; NAN only fills the destructuring's type.
  const call = (fn: Fn, codes: readonly Code[]): Code => {
    const [a = NAN, b = NAN] = codes;
    switch (fn) {
      case 'abs':
        return () => Math.abs(a());
      case 'sign':
        return () => Math.sign(a());
      case 'floor':
        return () => Math.floor(a());
      case 'ceil':
        return () => Math.ceil(a());
      case 'sqrt':
        return () => Math.sqrt(a());
      case 'min':
        return () => codes.reduce((m, c) => Math.min(m, c()), Infinity);
      case 'max':
        return () => codes.reduce((m, c) => Math.max(m, c()), -Infinity);
      case 'atan2': {
        const f = own(fns, 'atan2');
        return () => {
          const y = a();
          const x = b();
          return eitherNaN(y, x) ? NaN : f(y, x);
        };
      }
      default: {
        const f = own(fns, fn);
        const positive = fn === 'ln' || fn === 'log10';
        return () => {
          const x = a();
          return Number.isNaN(x) || (positive && !(x > 0)) ? NaN : f(x);
        };
      }
    }
  };

  const root = build(node, new Map());
  const names = [...free.keys()];
  const cells = [...free.values()];
  const exec = (): number => {
    budget = MAX_WORK;
    return root();
  };
  return {
    free: names,
    run(values) {
      if (values.length !== cells.length) {
        throw new RangeError(`expected ${cells.length} values, got ${values.length}`);
      }
      cells.forEach((c, j) => {
        c.v = Number(values[j]);
      });
      return exec();
    },
    evaluate(scope) {
      for (const [name, c] of free) {
        const v = Object.hasOwn(scope, name) ? scope[name] : undefined;
        if (typeof v !== 'number') throw new ScopeError(name);
        c.v = v;
      }
      return exec();
    },
  };
}
