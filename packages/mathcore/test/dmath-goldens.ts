// Shared by dmath.test.ts (Node) and dmath.browser.test.ts: reads the goldens tools/zqverify/dmath.py writes,
// checks a result against its 50-digit reference, and renders the bits golden. The bits golden lists every
// result whose bits differ from its correctly rounded reference, so with the goldens it records the bits of
// all 10,000 results. A NaN is compared as NaN: ECMAScript leaves a NaN's bit pattern to the engine [sourced:
// ECMA-262, NumericToRawBytes].
import { cos, exp, expm1, log, log1p, pow, sin, tanh } from '@zq/mathcore/dmath';

const FUNCTIONS: Readonly<Record<string, (...args: number[]) => number>> = {
  exp,
  log,
  log1p,
  expm1,
  tanh,
  pow,
  sin,
  cos,
};

export interface Case {
  readonly fn: string;
  readonly index: number;
  readonly args: readonly number[];
  /** The reference rounded to the nearest double. */
  readonly reference: number;
  /** (50-digit reference - reference) / ulp(reference), in thousandths. */
  readonly rem: number;
}

const view = new DataView(new ArrayBuffer(8));

function fromHex(hex: string): number {
  view.setBigUint64(0, BigInt(`0x${hex}`));
  return view.getFloat64(0);
}

function toHex(x: number): string {
  view.setFloat64(0, x);
  return view.getBigUint64(0).toString(16).padStart(16, '0');
}

export function parseGoldens(text: string): Case[] {
  const cases: Case[] = [];
  let fn = '';
  let index = 0;
  for (const line of text.split('\n')) {
    if (line === '' || line.startsWith('#')) continue;
    if (line.startsWith('@')) {
      fn = line.slice(1);
      index = 0;
      continue;
    }
    const fields = line.split(' ');
    const rem = Number(fields.pop());
    const reference = fromHex(fields.pop() ?? '');
    cases.push({ fn, index: index++, args: fields.map(fromHex), reference, rem });
  }
  return cases;
}

export function evaluate(c: Case): number {
  const f = FUNCTIONS[c.fn];
  if (f === undefined) throw new Error(`no dmath function ${c.fn}`);
  return f(...c.args);
}

const MIN_NORMAL = 2.2250738585072014e-308;

/**
 * The tolerance rule: within 1e-15 of the 50-digit reference relative to it; where the reference is below
 * 2^-1022 (subnormal, or zero after rounding), within one ulp there, 2^-1074, and a zero result carries the
 * reference's sign; NaN and infinite references must be met exactly.
 */
export function withinTolerance(c: Case, y: number): boolean {
  const ref = c.reference;
  if (Number.isNaN(ref) || !Number.isFinite(ref)) return Object.is(y, ref);
  view.setFloat64(0, ref);
  const ulp = 2 ** (Math.max(1, (view.getUint16(0) >> 4) & 0x7ff) - 1075);
  const ulps = Math.abs((y - ref) / ulp - c.rem / 1000);
  if (Math.abs(ref) >= MIN_NORMAL) return (ulps * ulp) / Math.abs(ref) <= 1e-15;
  return ulps <= 1 && (y !== 0 || ref !== 0 || Object.is(y, ref));
}

export function renderBits(cases: readonly Case[]): string {
  const lines = [
    '# The results of @zq/mathcore/dmath whose bits differ from the rounded reference in dmath.goldens.txt,',
    '# as "<function> <case index> <bits>"; every other result has its reference\'s bits. Written by Node',
    '# through `vitest run -u`; the browser project must reproduce it.',
  ];
  for (const c of cases) {
    const y = evaluate(c);
    if (!Object.is(y, c.reference)) lines.push(`${c.fn} ${c.index} ${Number.isNaN(y) ? 'nan' : toHex(y)}`);
  }
  return `${lines.join('\n')}\n`;
}
