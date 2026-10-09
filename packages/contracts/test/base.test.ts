// Compile-time tests of docs/ARCHITECTURE.md 5.1: `tsc -b` checks every assertion; vitest runs them as no-ops.
import type { effect } from '@preact/signals-core';
import type * as base from '@zq/contracts/base';
import type { Json, Rng, Scope, Token } from '@zq/contracts/base';
import { describe, expectTypeOf, test } from 'vitest';
import type { Words } from './types.ts';

type ListenOptions = Parameters<Scope['listen']>[3];
type EffectFn = Parameters<Scope['effect']>[0];

describe('shared primitives (5.1)', () => {
  test('Json admits JSON values and nothing else', () => {
    expectTypeOf<{ a: [1, 'x', null, { b: true }]; c: number[] }>().toExtend<Json>();
    expectTypeOf<undefined>().not.toExtend<Json>();
    expectTypeOf<{ a: undefined }>().not.toExtend<Json>();
    expectTypeOf<bigint>().not.toExtend<Json>();
    expectTypeOf<() => void>().not.toExtend<Json>();
  });

  test('ids are strings; marks and highlight styles are closed sets', () => {
    expectTypeOf<[base.ContentId, base.LocalId, base.ElementId]>().toEqualTypeOf<[string, string, string]>();
    expectTypeOf<base.Mark>().toEqualTypeOf<Words<'correct not-yet kept reveal'>>();
    expectTypeOf<base.HighlightStyle>().toEqualTypeOf<Words<'ring wash flash'>>();
  });

  test('Token is compiled ZQ Markdown: content-format 2.4 example, then every other tag', () => {
    expectTypeOf([
      ['t', 'That is a '],
      ['l', 'gls.prob.conditional-probability', [['t', 'conditional probability']]],
      ['m', 'P(A \\mid B)'],
      ['b', [['i', [['c', 'x']]]]],
      ['M', '\\frac{1}{11}'],
      ['v', 'd.total'],
      ['if', 'd.even', [['t', 'even']], []],
      ['p'],
      ['ul', [[['t', 'one']], [['t', 'two']]]],
    ] satisfies base.TokenList).toExtend<Token[]>();
    expectTypeOf<['l', string]>().not.toExtend<Token>();
    expectTypeOf<['h1', string]>().not.toExtend<Token>();
    expectTypeOf<['p', string]>().not.toExtend<Token>();
  });

  test('Scope owns timers, frames, listeners, effects and aborts', () => {
    expectTypeOf<keyof Scope>().toEqualTypeOf<
      Words<'signal disposed later every frame loop listen effect own child dispose'>
    >();
    expectTypeOf<Pick<Scope, 'signal' | 'disposed'>>().toEqualTypeOf<
      Readonly<{ signal: AbortSignal; disposed: boolean }>
    >();
    type Timer = (fn: () => void, ms: number) => () => void;
    expectTypeOf<Scope['later']>().toEqualTypeOf<Timer>();
    expectTypeOf<Scope['every']>().toEqualTypeOf<Timer>();
    expectTypeOf<Scope['frame']>().toEqualTypeOf<(fn: (t: number) => void) => () => void>();
    expectTypeOf<Scope['loop']>().toEqualTypeOf<(fn: (t: number, dt: number) => boolean) => () => void>();
    expectTypeOf<Scope['listen']>().parameters.toEqualTypeOf<
      [target: EventTarget, type: string, fn: (e: Event) => void, opts?: ListenOptions]
    >();
    // lib.dom's AddEventListenerOptions, spelt out so base.ts needs no DOM lib.
    expectTypeOf<NonNullable<ListenOptions>>().toEqualTypeOf<
      Pick<AddEventListenerOptions, keyof AddEventListenerOptions>
    >();
    expectTypeOf<Scope['own']>().toEqualTypeOf<(dispose: () => void) => void>();
    expectTypeOf<Scope['child']>().toEqualTypeOf<() => Scope>();
    expectTypeOf<Scope['dispose']>().toEqualTypeOf<() => void>();
  });

  test("an effect takes what signals' effect takes: 5.1's cleanup or nothing, void calls included", () => {
    expectTypeOf<EffectFn>().toEqualTypeOf<Parameters<typeof effect>[0]>();
    expectTypeOf<() => void>().toExtend<EffectFn>(); // a function declared (): void, or inferred from a void call
    expectTypeOf<() => undefined>().toExtend<EffectFn>();
    expectTypeOf<() => () => void>().toExtend<EffectFn>();
    expectTypeOf<() => number>().not.toExtend<EffectFn>();
    expectTypeOf<() => Promise<void>>().not.toExtend<EffectFn>();
  });

  test('Rng and SeedSource are the contracts @zq/mathcore/rng implements', () => {
    expectTypeOf<Rng>().toEqualTypeOf<{
      next(): number;
      at(index: number): number;
      int(lo: number, hi: number): number;
      normal(): number;
      fork(stream: string): Rng;
    }>();
    expectTypeOf<base.SeedSource>().toEqualTypeOf<{ readonly seed: number; rng(stream: string): Rng }>();
  });
});
