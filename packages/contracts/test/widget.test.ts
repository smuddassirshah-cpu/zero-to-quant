// Compile-time tests of the widget contract and the view API (docs/ARCHITECTURE.md 5.3).
import type { ReadonlySignal } from '@preact/signals-core';
import type { MotionStep } from '@zq/contracts/answer';
import type { HighlightStyle, Json, LocalId, Mark } from '@zq/contracts/base';
import type { PythonRuntime, SqlRuntime } from '@zq/contracts/platform';
import type { TexService } from '@zq/contracts/render';
import type * as w from '@zq/contracts/widget';
import type { BaseConfig, WidgetLogic } from '@zq/contracts/widget';
import type * as api from '@zq/contracts/widget-api';
import type { WidgetModule } from '@zq/contracts/widget-api';
import type { Ref, VNode } from 'preact';
import { describe, expectTypeOf, test } from 'vitest';
import type { PickerA, PickerConfig, PickerV } from './picker.ts';
import type { OptionalKeys, RequiredKeys, Words } from './types.ts';

type L = WidgetLogic<BaseConfig, Json, Json>;
type Api = api.WidgetApi<PickerA, PickerV>;

describe('the widget contract (5.3)', () => {
  test('WidgetLogic: what every widget implements, and what it may leave out', () => {
    expectTypeOf<RequiredKeys<L>>().toEqualTypeOf<
      | Words<'type v tier cluster answers stateVersion init answer dirty summarise'>
      | Words<'answerObjects staticTargets describe targets'>
    >();
    expectTypeOf<OptionalKeys<L>>().toEqualTypeOf<
      | Words<'tweenable needs migrate solved marks predicates exports elementMeta'>
      | Words<'resolvers recipes table secret tryable tryValue code'>
    >();
    expectTypeOf<L['tier']>().toEqualTypeOf<Exclude<w.WidgetTier, 'preset'>>();
    expectTypeOf<NonNullable<L['needs']>[number]>().toEqualTypeOf<Words<'python sql cas mathfield'>>();
    expectTypeOf<NonNullable<L['recipes']>[string]>().returns.toEqualTypeOf<MotionStep[]>();
  });

  test('ClusterId has the 26 lazy chunks of WIDGETS.md decision 19; modes and roles are closed sets', () => {
    expectTypeOf<w.ClusterId>().toEqualTypeOf<
      | Words<'core number algebra geometry precalc computing calculus linalg stochastic probability'>
      | Words<'statistics timeseries python data tools algorithms cpp finance projects interview ml'>
      | Words<'research analysis numerics optim dl'>
    >();
    expectTypeOf<w.WidgetMode>().toEqualTypeOf<
      Words<'lesson explore demonstrate quiz practice review homework exam placement readonly'>
    >();
    expectTypeOf<w.MotionMode>().toEqualTypeOf<Words<'full reduced test'>>();
    expectTypeOf<w.Target['role']>().toEqualTypeOf<
      Words<'handle cell region token slot option mark control line node edge term readout test'>
    >();
  });

  test('state halves are JSON with exact keys: a Readonly alias, not an interface', () => {
    interface Bare {
      picked: LocalId[];
    }
    interface Indexed {
      [key: string]: Json;
      zoom: number;
    }
    expectTypeOf<Bare>().not.toExtend<Json>();
    expectTypeOf<Indexed>().toExtend<Json>();
    expectTypeOf<keyof Indexed & string>().toEqualTypeOf<string>();
    expectTypeOf<PickerA>().toExtend<Json>();
    type P = WidgetLogic<PickerConfig, PickerA, PickerV>;
    expectTypeOf<['zoom']>().toExtend<NonNullable<P['tweenable']>>();
    expectTypeOf<['picked']>().not.toExtend<NonNullable<P['tweenable']>>();
  });

  test('a concrete module is not assignable to the registry erased type without a cast', () => {
    // keyof Json is never (tweenable), and the function-typed properties and View are contravariant in C.
    expectTypeOf<WidgetLogic<PickerConfig, PickerA, PickerV>>().not.toExtend<L>();
    expectTypeOf<WidgetModule<PickerConfig, PickerA, PickerV>>().not.toExtend<
      WidgetModule<BaseConfig, Json, Json>
    >();
  });

  test('BaseConfig, presets and fixtures', () => {
    expectTypeOf<RequiredKeys<BaseConfig>>().toEqualTypeOf<'id' | 'type' | 'v' | 'label'>();
    expectTypeOf<'two-dice@1'>().toExtend<NonNullable<BaseConfig['preset']>>();
    expectTypeOf<'two-dice'>().not.toExtend<NonNullable<BaseConfig['preset']>>();
    expectTypeOf<w.PresetDef<BaseConfig, PickerConfig>['expand']>().returns.toEqualTypeOf<
      Omit<PickerConfig, 'id' | 'label'>
    >();
    expectTypeOf<keyof api.PresetRuntime>().toEqualTypeOf<Words<'type v predicates recipes describeAs'>>();
    type Paths = NonNullable<w.WidgetFixture<PickerConfig, PickerA, PickerV>['paths']>;
    expectTypeOf<keyof Paths>().toEqualTypeOf<Words<'pointer keyboard tapTap'>>();
    expectTypeOf<w.FixtureStep['do']>().toEqualTypeOf<Words<'drag tap key type expect'>>();
  });
});

describe('the view API (5.3)', () => {
  test('signals are read-only to the view; writes go through change, commit and view', () => {
    expectTypeOf<RequiredKeys<Api>>().toEqualTypeOf<
      | Words<'state locked ghost mode motion theme scope seed services'>
      | Words<'change commit view announce feedback el'>
    >();
    expectTypeOf<OptionalKeys<Api>>().toBeNever();
    expectTypeOf<Api['state']>().toEqualTypeOf<ReadonlySignal<Readonly<{ a: PickerA; v: PickerV }>>>();
    expectTypeOf<Api['theme']>().toEqualTypeOf<ReadonlySignal<'light' | 'dark'>>();
    expectTypeOf<Api['feedback']>().parameter(0).toEqualTypeOf<Words<'tap snap lift drop'>>();
    expectTypeOf<Api['view']>().returns.toBeVoid();
  });

  test('el(id) gives the props every targetable element spreads', () => {
    expectTypeOf<api.ElementProps>().toEqualTypeOf<{
      ref: Ref<Element>;
      'data-zq-id': string;
      'data-zq-mark': ReadonlySignal<Mark | undefined>;
      'data-zq-hl': ReadonlySignal<HighlightStyle | undefined>;
    }>();
  });

  test('a view is a Preact component; services are lazy and null when not needed', () => {
    expectTypeOf<WidgetModule<PickerConfig, PickerA, PickerV>['View']>().toEqualTypeOf<
      (props: { config: PickerConfig; api: Api }) => VNode | null
    >();
    expectTypeOf<api.WidgetServices>().toEqualTypeOf<{
      tex: TexService;
      cas: (() => Promise<api.CasService>) | null;
      mathfield: (() => Promise<api.MathfieldService>) | null;
      python: PythonRuntime | null;
      sql: SqlRuntime | null;
    }>();
    expectTypeOf<api.MathfieldService['mount']>().parameter(0).toEqualTypeOf<HTMLElement>();
  });
});
