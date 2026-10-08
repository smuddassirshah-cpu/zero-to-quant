// Parity with the Python twin, tools/zqverify/expr.py, which parses with CPython's own parser and gives each
// operation its correctly rounded value (mpmath at 50 digits for the table functions and ^). Its goldens
// (expr.golden.jsonl) hold hand-picked cases, every table function, sqrt, atan2 and ^ over edge arguments
// (the zeros, +-1, +-inf, NaN), 300 random expressions built from the exact operations only and 1,000 random
// token strings, nearly all refused; rewrite them with
// `PYTHONPATH=tools uv run --project tools/py --locked python -m zqverify.expr`.
import { readFileSync } from 'node:fs';
import { describe, expect, it } from 'vitest';
import { compile, ParseError, parse, ScopeError } from '@zq/mathcore/expr';
import { MATH } from './expr-table.ts';

interface Golden {
  src: string;
  scope: Record<string, number>;
  free?: string[];
  value?: number | string;
  exact?: boolean;
  error?: 'parse' | 'scope';
}

const goldens = readFileSync(new URL('expr.golden.jsonl', import.meta.url), 'utf8')
  .split('\n')
  .filter(Boolean)
  .map((line) => JSON.parse(line) as Golden);

function outcome(g: Golden): { error: string } | { free: readonly string[]; value: number } {
  try {
    const c = compile(parse(g.src), MATH);
    return { free: c.free, value: c.evaluate(g.scope) };
  } catch (err) {
    if (err instanceof ParseError) return { error: 'parse' };
    if (err instanceof ScopeError) return { error: 'scope' };
    throw err;
  }
}

function agrees(g: Golden): boolean {
  const got = outcome(g);
  if ('error' in got || g.error !== undefined) return 'error' in got && got.error === g.error;
  const want = typeof g.value === 'string' ? Number(g.value.replace('inf', 'Infinity')) : (g.value ?? NaN);
  // A tolerance only for a finite, non-zero value of an inexact case: special values and zeros' signs match.
  const close =
    g.exact === false &&
    Number.isFinite(want) &&
    want !== 0 &&
    Math.abs(got.value - want) <= 1e-12 * Math.abs(want);
  return JSON.stringify(got.free) === JSON.stringify(g.free) && (Object.is(got.value, want) || close);
}

describe('the Python twin (tools/zqverify/expr.py)', () => {
  it('agrees on every golden: to the bit where only exact operations run, to 1e-12 elsewhere', () => {
    expect(goldens.length).toBeGreaterThan(1800);
    expect(goldens.filter((g) => g.exact === true).length).toBeGreaterThan(350);
    expect(goldens.filter((g) => g.exact === false).length).toBeGreaterThan(400);
    expect(goldens.filter((g) => !agrees(g)).map((g) => g.src)).toEqual([]);
  });
});
