// Exact rationals over BigInt (docs/ARCHITECTURE.md 4.3; CONTENT-FORMAT.md 5.3 and 7.2). Decision notes:
// - Canonical form always: the denominator is positive and gcd(|n|, d) = 1, so equality is a field compare
//   and a value has one spelling, `toString`'s "n/d" (or "n"), the authored `NumValue` form.
// - Immutable plain objects, no class, so values cross a worker boundary by structured clone [our choice].
// - Errors are RangeErrors: a zero denominator, a non-integer or unsafe number, a malformed string, and an
//   exponent beyond EXPONENT_LIMIT, which bounds the size of a BigInt a typed string can create [our choice].
export interface Rational {
  readonly n: bigint;
  readonly d: bigint;
}

export const EXPONENT_LIMIT = 1000;

const DECIMAL = /^(-?)(\d*)(?:\.(\d*))?(?:[eE]([+-]?\d+))?$/;
const FRACTION = /^(-?\d+)\/(\d+)$/;

function gcd(a: bigint, b: bigint): bigint {
  while (b !== 0n) [a, b] = [b, a % b];
  return a;
}

function big(x: bigint | number): bigint {
  if (typeof x === 'bigint') return x;
  if (!Number.isSafeInteger(x)) throw new RangeError(`not a safe integer: ${x}`);
  return BigInt(x);
}

/** n/d in lowest terms with a positive denominator. Throws on a zero denominator. */
export function rat(n: bigint | number, d: bigint | number = 1n): Rational {
  let [p, q] = [big(n), big(d)];
  if (q === 0n) throw new RangeError('division by zero');
  if (q < 0n) [p, q] = [-p, -q];
  const g = gcd(p < 0n ? -p : p, q);
  return { n: p / g, d: q / g };
}

export const add = (a: Rational, b: Rational): Rational => rat(a.n * b.d + b.n * a.d, a.d * b.d);
export const sub = (a: Rational, b: Rational): Rational => rat(a.n * b.d - b.n * a.d, a.d * b.d);
export const mul = (a: Rational, b: Rational): Rational => rat(a.n * b.n, a.d * b.d);
export const div = (a: Rational, b: Rational): Rational => rat(a.n * b.d, a.d * b.n);
export const neg = (a: Rational): Rational => ({ n: -a.n, d: a.d });

/** -1, 0 or 1 as a is below, equal to or above b. */
export function cmp(a: Rational, b: Rational): -1 | 0 | 1 {
  const l = a.n * b.d;
  const r = b.n * a.d;
  return l < r ? -1 : l > r ? 1 : 0;
}

export const eq = (a: Rational, b: Rational): boolean => a.n === b.n && a.d === b.d;

/** The canonical spelling: "n" for an integer, otherwise "n/d", with an ASCII minus. */
export const toString = (a: Rational): string => (a.d === 1n ? `${a.n}` : `${a.n}/${a.d}`);

/** True when the decimal expansion terminates: the denominator has no prime factor but 2 and 5. */
export function terminates(a: Rational): boolean {
  let d = a.d;
  while (d % 2n === 0n) d /= 2n;
  while (d % 5n === 0n) d /= 5n;
  return d === 1n;
}

/** A terminating decimal in ASCII: "-12.5", ".25", "305.", "3.2e-4". No grouping, no other characters. */
export function fromDecimal(text: string): Rational {
  const m = DECIMAL.exec(text);
  const [, sign = '', whole = '', frac = '', exp = '0'] = m ?? [];
  if (!m || whole + frac === '') throw new RangeError(`not a decimal: ${JSON.stringify(text)}`);
  if (Math.abs(Number(exp)) > EXPONENT_LIMIT) throw new RangeError(`exponent beyond ${EXPONENT_LIMIT}`);
  const e = Number(exp) - frac.length;
  const digits = BigInt(sign + whole + frac);
  return e >= 0 ? rat(digits * 10n ** BigInt(e)) : rat(digits, 10n ** BigInt(-e));
}

/** The canonical spelling back to a value: "n", "n/d" (either sign on n only) or a terminating decimal. */
export function parse(text: string): Rational {
  if (!FRACTION.test(text)) return fromDecimal(text);
  const [n, d] = text.split('/').map(BigInt) as [bigint, bigint];
  return rat(n, d);
}
