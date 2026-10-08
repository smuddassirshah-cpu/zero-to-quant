// docs/ARCHITECTURE.md 5.4, the lifecycle of a widget instance, walked step by step through the contract with
// the sample widget: the logic's half runs, the host's half is checked by type.
import type { Grade } from '@zq/contracts/answer';
import type { Json, Scope } from '@zq/contracts/base';
import type { BaseConfig, WidgetModule, WidgetState } from '@zq/contracts/widget';
import type { PresetRuntime, WidgetApi, WidgetRegistry } from '@zq/contracts/widget-api';
import { describe, expect, expectTypeOf, test } from 'vitest';
import { config, picker, seed, type PickerA, type PickerState, type PickerV } from './picker.ts';

type Api = WidgetApi<PickerA, PickerV>;
const pick =
  (id: string) =>
  (s: PickerState): PickerState => ({ ...s, a: { picked: [...s.a.picked, id] } });
const start = picker.init(config, seed);
const engaged = pick('four')(pick('two')(start));
const both = ['option:two', 'option:four'];

describe('the lifecycle of a widget instance (5.4)', () => {
  test('1 compile: staticTargets names every element content may reference, without a DOM', () => {
    expect(picker.staticTargets(config).map((t) => `${t.role} ${t.id}`)).toEqual([
      'option option:two',
      'option option:three',
      'option option:four',
    ]);
  });

  test('2 load: the registry resolves a module from its cluster chunk, and a preset runtime', () => {
    expectTypeOf<WidgetRegistry['load']>().returns.resolves.toEqualTypeOf<
      WidgetModule<BaseConfig, Json, Json>
    >();
    expectTypeOf<WidgetRegistry['preset']>().returns.resolves.toEqualTypeOf<PresetRuntime | null>();
  });

  test('3 mount: an older draft migrates or is discarded; otherwise init runs with the seed', () => {
    expect(picker.migrate?.(['two'], 1, config)).toEqual({ a: { picked: ['two'] }, v: { zoom: 1 } });
    expect(picker.migrate?.({ picked: ['two'] }, 0, config)).toBeNull();
    expect(start).toEqual({ a: { picked: [] }, v: { zoom: 1 } });
    expect(picker.describe(config, start, 'brief').length).toBeLessThanOrEqual(300);
  });

  test('4 interact: change during a gesture, commit at its end, view for view state', () => {
    expectTypeOf(pick('two')).toEqualTypeOf<Parameters<Api['change']>[0]>();
    expectTypeOf<Api['commit']>().parameter(0).toEqualTypeOf<((s: PickerState) => PickerState) | undefined>();
    expectTypeOf<Api['view']>().parameter(0).toEqualTypeOf<(v: PickerV) => PickerV>();
    expect([picker.dirty(config, start), picker.dirty(config, engaged)]).toEqual([false, true]);
    expect(picker.summarise(config, start, engaged)).toBe('Picked two, four');
  });

  test('5 check: the answer goes to the graders, and marks paint the answer objects', () => {
    expect(picker.answer(config, start)).toBeNull();
    expect(picker.answer(config, engaged)).toEqual({ type: 'choice', ids: ['two', 'four'] });
    const answerObjects = picker.answerObjects(config, engaged);
    const grade: Grade = { verdict: 'correct', accepted: [], normalised: null, answerObjects };
    expect(picker.marks?.(config, engaged, grade)).toEqual({
      'option:two': 'correct',
      'option:four': 'correct',
    });
    expect(picker.recipes?.flash?.(config, engaged, {})).toEqual([
      { k: 'highlight', ids: both, style: 'flash' },
    ]);
  });

  test('6 to 8: try again restores only v, show solution uses solved, start over repeats init', () => {
    expect(picker.answer(config, { ...engaged, v: { zoom: 3 } })).toEqual(picker.answer(config, engaged));
    expect(picker.solved?.(config, start, ['two', 'four'])).toEqual({ a: engaged.a, v: start.v });
    expect(picker.init(config, seed)).toEqual(start);
  });

  test('9 leave: the scope disposes what the instance owned; the final draft is a JSON copy', () => {
    expectTypeOf<Api['scope']>().toEqualTypeOf<Scope>();
    // DraftStore.put takes Json, and WidgetState is an interface, so the host saves { a, v }.
    expectTypeOf<WidgetState<PickerA, PickerV>>().not.toExtend<Json>();
    expectTypeOf<{ a: PickerA; v: PickerV }>().toExtend<Json>();
  });
});
