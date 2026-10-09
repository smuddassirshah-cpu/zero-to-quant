// A sample widget for the contract tests, written against WidgetLogic alone: pick options from a list. It
// proves a concrete widget can implement the contract; the tests read its types, never run it.
import type { Json, LocalId, Mark } from '@zq/contracts/base';
import type { BaseConfig, Target, WidgetLogic } from '@zq/contracts/widget';

export interface PickerConfig extends BaseConfig {
  options: LocalId[];
}
// A and V must be JSON with exact keys: a Readonly alias is both, where an interface is not JSON and an index
// signature would widen keyof V, so tweenable would accept any name (widget.ts, decision notes).
export type PickerA = Readonly<{ picked: LocalId[] }>;
export type PickerV = Readonly<{ zoom: number }>;

const strings = (value: Json): LocalId[] =>
  Array.isArray(value) ? value.filter((x) => typeof x === 'string') : [];
const element = (id: LocalId) => `option:${id}`;
const targets = (c: PickerConfig): Target[] =>
  c.options.map((id) => ({ id: element(id), label: id, role: 'option' }));

export const picker: WidgetLogic<PickerConfig, PickerA, PickerV> = {
  type: 'picker',
  v: 1,
  tier: 'input',
  cluster: 'core',
  answers: ['choice'],
  stateVersion: 2,
  tweenable: ['zoom'],
  init: (_c, s) => ({ a: { picked: [] }, v: { zoom: s.rng('zoom').int(1, 3) } }),
  migrate: (saved, from) => (from === 1 ? { a: { picked: strings(saved) }, v: { zoom: 1 } } : null),
  answer: (_c, s) => (s.a.picked.length > 0 ? { type: 'choice', ids: s.a.picked } : null),
  dirty: (_c, s) => s.a.picked.length > 0,
  solved: (_c, s, key) => ({ a: { picked: strings(key) }, v: s.v }),
  summarise: (_c, before, after) =>
    `Picked ${after.a.picked.filter((id) => !before.a.picked.includes(id)).join(', ')}`,
  answerObjects: (c) => c.options.map(element),
  marks: (_c, s, grade) => {
    const mark: Mark = grade.verdict === 'correct' ? 'correct' : 'not-yet';
    return Object.fromEntries(s.a.picked.map((id) => [element(id), mark]));
  },
  predicates: { 'picked-all': (c, s) => s.a.picked.length === c.options.length },
  staticTargets: targets,
  recipes: { flash: (_c, s) => [{ k: 'highlight', ids: s.a.picked.map(element), style: 'flash' }] },
  describe: (c, s, level) =>
    level === 'brief'
      ? `${s.a.picked.length} of ${c.options.length} options picked`
      : `Options ${c.options.join(', ')}; picked ${s.a.picked.join(', ')}.`,
  targets: (c) => targets(c),
};
