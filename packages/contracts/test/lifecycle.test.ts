// The contract's side of docs/ARCHITECTURE.md 5.4: the types each lifecycle step relies on. The steps
// themselves (locking, grade generations, the draft debounce, scope disposal) are host behaviour, which
// src/engine/widgets/host.tsx's own tests check when it is built (stage 10a); a types-only package cannot.
import type { Answer, Grade } from '@zq/contracts/answer';
import type { Json, Scope, SeedSource } from '@zq/contracts/base';
import type { DraftStore } from '@zq/contracts/platform';
import type { BaseConfig, Target, WidgetState } from '@zq/contracts/widget';
import type { PresetRuntime, WidgetApi, WidgetModule, WidgetRegistry } from '@zq/contracts/widget-api';
import { describe, expectTypeOf, test } from 'vitest';
import type { picker, PickerA, PickerConfig, PickerV } from './picker.ts';

type Api = WidgetApi<PickerA, PickerV>;
type S = WidgetState<PickerA, PickerV>;
type P = typeof picker;

describe('the lifecycle of a widget instance, its types (5.4)', () => {
  test('1 compile: staticTargets needs only the config', () => {
    expectTypeOf<P['staticTargets']>().toEqualTypeOf<(config: PickerConfig) => Target[]>();
  });

  test('2 load: the registry resolves a module from its cluster chunk, and a preset runtime', () => {
    expectTypeOf<WidgetRegistry['load']>().returns.resolves.toEqualTypeOf<
      WidgetModule<BaseConfig, Json, Json>
    >();
    expectTypeOf<WidgetRegistry['preset']>().returns.resolves.toEqualTypeOf<PresetRuntime | null>();
  });

  test('3 mount: a saved draft is Json to migrate, or init runs with the seed', () => {
    expectTypeOf<NonNullable<P['migrate']>>().parameters.toEqualTypeOf<
      [saved: Json, fromVersion: number, config: PickerConfig]
    >();
    expectTypeOf<NonNullable<P['migrate']>>().returns.toEqualTypeOf<S | null>();
    expectTypeOf<P['init']>().parameters.toEqualTypeOf<[config: PickerConfig, seed: SeedSource]>();
  });

  test('4 interact: change during a gesture, commit at its end, view for view state', () => {
    expectTypeOf<Api['change']>().parameter(0).toEqualTypeOf<(s: S) => S>();
    expectTypeOf<Api['commit']>().parameter(0).toEqualTypeOf<((s: S) => S) | undefined>();
    expectTypeOf<Api['view']>().parameter(0).toEqualTypeOf<(v: PickerV) => PickerV>();
  });

  test('5 check: the answer goes to the graders, and marks read the grade they return', () => {
    expectTypeOf<P['answer']>().returns.toEqualTypeOf<Answer | null>();
    expectTypeOf<NonNullable<P['marks']>>().parameter(2).toEqualTypeOf<Grade>();
  });

  test('9 leave: the scope disposes what the instance owned; the final draft is the state itself', () => {
    expectTypeOf<Api['scope']>().toEqualTypeOf<Scope>();
    // DraftStore.put takes Json, and WidgetState is a Readonly alias, so a state is Json as it stands.
    expectTypeOf<S>().toExtend<Json>();
    expectTypeOf<S>().toExtend<Parameters<DraftStore['put']>[1]>();
  });
});
