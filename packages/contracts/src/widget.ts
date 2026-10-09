/*
 * The widget contract (docs/ARCHITECTURE.md 5.3, first listing), without its view half; test/lifecycle.test.ts
 * and test/catalogue.test.ts check the contract's side of 5.4 and 5.6.
 * Decision notes:
 * - Pure and Node-safe like `WidgetLogic` itself: this module imports neither preact nor widget-api.ts.
 *   preact's jsx.d.ts carries `/// <reference lib="dom" />`, so a program that reached it would compile with
 *   the DOM lib whatever its tsconfig says, and @zq/compiler and tools/zq, which read `WidgetLogic` through
 *   `CompilerRegistry`, have no DOM (4.3) [measured: tsc 6.0.3, test/node-libs.test.ts]. 5.3's
 *   `WidgetViewProps`, `WidgetView` and `WidgetModule` name `VNode` and `WidgetApi`, so they live in
 *   widget-api.ts, the view half, with the registry that loads them.
 * - `ClusterId` has 26 members: 5.3's listing shows 22, but ARCHITECTURE.md decision 8 and 6.4.1 count
 *   26 since revision 2, and WIDGETS.md, which owns clusters, adds `analysis`, `numerics`, `optim` and `dl`
 *   (its decision 19, recorded against this union in its 0.3).
 * - Two members of the listing are not here. `WidgetSchemaModule` types its schemas as zod's `ZodType`, and
 *   zod is not yet a dependency of this package; `CompilerRegistry`, which reads it, belongs to the second
 *   contracts unit of stage 3.
 * - `A` and `V` must be JSON with exact keys. An interface is not assignable to `Json` (no implicit index
 *   signature), an index signature widens `keyof V` so `tweenable` accepts any name, and the lint rule
 *   consistent-type-definitions refuses `type V = { ... }`; `type V = Readonly<{ ... }>` passes all three
 *   [measured: tsc 6.0.3 and ESLint, test/widget.test.ts]. `WidgetState` itself is an interface, as 5.3
 *   writes it, so the host saves a draft as a `{ a, v }` copy.
 * - `prettier-ignore` keeps 5.3's own line layout for its long unions; test/drift.test.ts compares every
 *   declaration with the listing.
 */
import type { Answer, AnswerType, Grade, MotionStep } from './answer.ts';
import type { ElementId, Json, LocalId, Mark, SeedSource } from './base.ts';

export type WidgetTier = 'primitive' | 'input' | 'scene' | 'composite' | 'preset'; // 'scene': 5.14
// prettier-ignore
export type ClusterId =
  | 'core' | 'number' | 'algebra' | 'geometry' | 'precalc' | 'computing'
  | 'calculus' | 'linalg' | 'stochastic' | 'probability' | 'statistics' | 'timeseries'
  | 'python' | 'data' | 'tools' | 'algorithms' | 'cpp'
  | 'finance' | 'projects' | 'interview' | 'ml' | 'research'
  | 'analysis' | 'numerics' | 'optim' | 'dl'; // 26 lazy chunks (WIDGETS.md decision 19)
// prettier-ignore
export type WidgetMode = 'lesson' | 'explore' | 'demonstrate' | 'quiz' | 'practice' | 'review'
                       | 'homework' | 'exam' | 'placement' | 'readonly';
export type MotionMode = 'full' | 'reduced' | 'test'; // 'test': every animation lands at once

/** Fields every widget config has (content-format WidgetUse); the rest is the widget's own schema. */
export interface BaseConfig {
  id: LocalId;
  type: string;
  v: number;
  label: string;
  preset?: `${string}@${number}`; // the compiler records which preset produced this config, pinned, e.g. 'two-dice@1'
  seed?: number;
}

/** a: answer state, graded, saved and restored. v: view state (zoom, step, time cursor), which show-why may tween. Both JSON. */
export interface WidgetState<A extends Json, V extends Json> {
  a: A;
  v: V;
}

// prettier-ignore
export interface Target {
  id: ElementId; label: string;
  role: 'handle' | 'cell' | 'region' | 'token' | 'slot' | 'option' | 'mark' | 'control'
      | 'line' | 'node' | 'edge' | 'term' | 'readout' | 'test';
}
export interface Tryable {
  control: ElementId;
  label: string;
  range?: [number, number];
  step?: number;
  options?: string[];
}
export interface TableView {
  caption: string;
  columns: string[];
  rows: (string | number)[][];
}
export type Predicate<C, A extends Json, V extends Json> = (
  config: C,
  s: WidgetState<A, V>,
  args: Record<string, Json>,
) => boolean;

/** Pure and Node-safe: no DOM, no Preact, no CSS, no clock, no Math.random. Imported by the app, the compiler and CI. */
export interface WidgetLogic<C extends BaseConfig, A extends Json, V extends Json> {
  readonly type: string; // kebab-case, unique
  readonly v: number; // major version; content pins it (content-format 3.5)
  readonly tier: Exclude<WidgetTier, 'preset'>;
  readonly cluster: ClusterId;
  readonly answers: readonly AnswerType[]; // [] for display-only widgets
  readonly stateVersion: number; // bump when the saved shape of a or v changes
  readonly tweenable?: readonly (keyof V & string)[]; // view fields show-why may tween
  readonly needs?: readonly ('python' | 'sql' | 'cas' | 'mathfield')[]; // services the host must inject

  // State
  init(config: C, seed: SeedSource): WidgetState<A, V>;
  migrate?(saved: Json, fromVersion: number, config: C): WidgetState<A, V> | null; // null: discard the draft
  answer(config: C, s: WidgetState<A, V>): Answer | null; // null keeps Check disabled
  dirty(config: C, s: WidgetState<A, V>): boolean; // enables Start over
  solved?(config: C, s: WidgetState<A, V>, key: Json): WidgetState<A, V>; // Show solution; key: the check's canonical answer
  summarise(config: C, before: WidgetState<A, V>, after: WidgetState<A, V>): string; // action-log sentence, at most 120 characters

  // Grading support
  answerObjects(config: C, s: WidgetState<A, V>): ElementId[]; // the only elements grading may recolour
  marks?(config: C, s: WidgetState<A, V>, grade: Grade): Record<ElementId, Mark>; // default: every answer object takes the verdict
  predicates?: Record<string, Predicate<C, A, V>>; // named state tests a `predicate` check may call

  // Build time (the compiler calls these through CompilerRegistry; content-format 6.7, 8.1, 12.1)
  staticTargets(config: C): Target[]; // every element content may reference in hints and show-why, with label and role, no DOM
  exports?: Record<string, (config: C, s: WidgetState<A, V>) => string | number>; // template values (content-format 3.6); the keys are the paths the compiler checks
  elementMeta?(config: C, id: ElementId): Record<string, string | number> | null; // per-element template metadata for set answers ('label', 'sum'; content-format 12.1)
  resolvers?: Record<string, (config: C, query: Json) => string[]>; // `{ where }` sets to explicit ids

  // Show-why
  recipes?: Record<string, (config: C, s: WidgetState<A, V>, args: Record<string, Json>) => MotionStep[]>;

  // Text, tables and the tutor (ai-tutor 5.5)
  describe(config: C, s: WidgetState<A, V>, level: 'brief' | 'full'): string; // learner-visible facts only; brief at most 300 characters, full at most 2 KB
  targets(config: C, s: WidgetState<A, V>): Target[]; // at most 40
  table?(config: C, s: WidgetState<A, V>): TableView | null; // every chart's Table view
  secret?(config: C, s: WidgetState<A, V>): string | null; // hidden truths, sent only in the sealed answer block
  tryable?(config: C, s: WidgetState<A, V>): Tryable[]; // never an answer object
  tryValue?(
    config: C,
    s: WidgetState<A, V>,
    control: ElementId,
    value: number | string,
  ): WidgetState<A, V> | null;
  code?(config: C, s: WidgetState<A, V>): { files: { name: string; numbered: string }[] } | null; // programming 2.8
}

/** A preset: configuration over a base widget, expanded by the compiler. No view, no state of its own. */
export interface PresetDef<P extends BaseConfig, C extends BaseConfig> {
  type: string;
  v: number;
  cluster: ClusterId;
  base: { type: string; v: number };
  expand(config: P): Omit<C, 'id' | 'label'>; // pure; the result is validated by the base widget's schema
  predicates?: Record<string, Predicate<C, Json, Json>>; // registered as '<preset type>/<name>'
  recipes?: Record<
    string,
    (config: C, s: WidgetState<Json, Json>, args: Record<string, Json>) => MotionStep[]
  >;
  describeAs?: string; // replaces the base widget's name in describe()
}

/** fixtures.ts default-exports WidgetFixture[]. The contract suite, the browser tests, the gallery and the storyboard all read this one shape. */
export interface WidgetFixture<C extends BaseConfig, A extends Json, V extends Json> {
  name: string; // kebab-case; the gallery URL segment
  config: C;
  seed?: number;
  states?: Record<string, WidgetState<A, V>>; // named states for screenshots ('engaged', 'solved')
  paths?: {
    // every interactive fixture has all three, and all three reach `expect`
    pointer: FixtureStep[];
    keyboard: FixtureStep[];
    tapTap: FixtureStep[];
  };
  expect?: { answer?: Answer | null; predicates?: Record<string, boolean> };
  sealed?: Json; // the check's canonical answer, for the leak tests of 8.1.1
}
export type FixtureStep =
  | { do: 'drag'; id: ElementId; to: { x: number; y: number } } // widget coordinates, converted through the host scale
  | { do: 'tap'; id: ElementId }
  | { do: 'key'; key: string; id?: ElementId; times?: number } // focuses `id` first when given
  | { do: 'type'; id: ElementId; text: string }
  | { do: 'expect'; answer?: Answer | null; announce?: string };
