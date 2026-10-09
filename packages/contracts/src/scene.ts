/*
 * Scenes (docs/ARCHITECTURE.md 5.14): a composite written as data, which `defineScene` turns into 5.3's
 * `WidgetLogic`. Types only: `defineScene` is a function, and this package has no runtime code, so it is built
 * with the scene layer at src/widgets/scene/define.ts, where 4.5's tree puts it (stage 14).
 * Decision notes:
 * - `PathOf` is the recursive template-literal type 5.14 describes: every dotted path of object keys into T,
 *   its prefixes included ('d', 'd.point', 'd.point.x'), at most five keys deep, and never into an array,
 *   which is one value (marks data, a table's rows) [our choice]. test/scene.test.ts checks the depth limit.
 * - `PrimType` is what 5.14's comment on the first node kind says: "any primitive or input other than the
 *   three below", the 29 primitives and 8 inputs of WIDGETS.md 4.1 and 4.2 but `marks`, `live-formula` and
 *   `value-table`, which have node kinds of their own. `HostPrim` and `WritingPrim` stay in
 *   src/widgets/scene/nodes.ts, which 5.14 gives them.
 * - `Bindable<S>` is a primitive's props, each a JSON value or a binding: 5.14's `SceneView` makes "every bound
 *   property a computed signal over the five sources" [inferred]. `MarkType`, `SpaceToken` and
 *   `DeclarativeRecipe` have no definition in any paper (WIDGETS.md 4.1.2 lists the mark types partly in
 *   words; tokens.css has no spacing scale), so they are opaque until stages 11 and 14 define them.
 * - Pure and Node-safe, like widget.ts: the compiler and CI read scenes through the registry.
 */
import type { Answer, AnswerType, MotionStep } from './answer.ts';
import type { Json, LocalId, SeedSource } from './base.ts';
import type { BaseConfig, ClusterId, WidgetLogic, WidgetState } from './widget.ts';

declare const opaque: unique symbol;
type Opaque<Name extends string> = Readonly<{ [opaque]: Name }>;

// prettier-ignore
export type PrimType =
  | 'plot-2d' | 'drag-point' | 'slider' | 'number-line' | 'region-select'
  | 'token-tray' | 'stepper' | 'sketch-pad' | 'cell-grid' | 'matrix' | 'plot-3d' | 'sim-runner' | 'chance-object'
  | 'mass-editor' | 'array-strip' | 'node-link' | 'code-surface' | 'diff-view' | 'text-terminal' | 'speed-timer'
  | 'scratch-pad' | 'cashflow-timeline' | 'price-ladder' | 'position-editor' | 'voice-capture' | 'span-track'
  | 'choice' | 'numeric-input' | 'expression-input' | 'card-sort' | 'derivation-steps' | 'free-response'
  | 'order-ticket' | 'quote-entry';
export type Bindable<S> = Readonly<Record<string, Json | Bind<S>>>;
export type MarkType = Opaque<'MarkType'>;
export type SpaceToken = Opaque<'SpaceToken'>;
export type DeclarativeRecipe = Opaque<'DeclarativeRecipe'>;

/** The five sources a scene binds to: config, prepared constants, answer state, view state, derived values. */
export interface SceneSrc<C, K, A, V, D> {
  c: C;
  k: K;
  a: A;
  v: V;
  d: D;
}
type Depth = [0, 0, 1, 2, 3, 4]; // Depth[n] is n - 1
// prettier-ignore
type Path<T, D extends number> = D extends 0 ? never : T extends readonly unknown[] ? never : T extends object
  ? { [K in keyof T & string]: K | `${K}.${Path<T[K], Depth[D]>}` }[keyof T & string]
  : never;
/** Dotted paths into T, checked by the type system ('d.point.x', 'a.theta'). */
export type PathOf<T> = Path<T, 5>;
export type Bind<S, T = unknown> = PathOf<S> | { from: (src: S) => T }; // a path, or a named pure function written in scene.ts
export interface Write<S, A, V, T> {
  // controls write answer or view state only
  path: PathOf<{ a: A; v: V }>;
  from?: (value: T, src: S) => Json; // e.g. a dragged point to an angle
}

// prettier-ignore
export type SceneNode<S, A, V> =
  | { id: LocalId; prim: PrimType; props: Bindable<S>;                                          // any primitive or input other than the three below
      children?: SceneNode<S, A, V>[];                                                          // HostPrim only
      writes?: Write<S, A, V, Json>;                                                            // WritingPrim only
      answer?: true; tryable?: true; visibleWhen?: Bind<S, boolean> }
  | { id: LocalId; prim: 'marks'; type: MarkType; data: Bind<S>; style?: Bindable<S>; table?: true; visibleWhen?: Bind<S, boolean> }
  | { id: LocalId; prim: 'live-formula'; tex: string; slots: Record<string, Bind<S>> }
  | { id: LocalId; prim: 'value-table'; rows: Bind<S>; columns: { key: string; label: string }[]; table?: true }
  | { layout: 'row' | 'column' | 'stack' | 'grid' | 'overlay'; gap?: SpaceToken; children: SceneNode<S, A, V>[] }
  | { id: LocalId; embed: `${string}@${number}`; config: Bind<S>; state: PathOf<{ a: A; v: V }> }; // another scene, or a bespoke composite's controlled component

// prettier-ignore
export interface SceneDef<C extends BaseConfig, K extends Json, A extends Json, V extends Json, D extends Json> {
  readonly type: string; readonly v: number; readonly cluster: ClusterId;
  readonly answers: readonly AnswerType[]; readonly stateVersion: number;
  readonly tweenable?: readonly (keyof V & string)[];
  readonly needs?: WidgetLogic<C, A, V>['needs'];
  prepare?(config: C): K;                                    // once per config: paths, grids, constants; layers binding only c and k are static
  init(config: C, seed: SeedSource): WidgetState<A, V>;
  derive(config: C, k: K, s: WidgetState<A, V>): D;          // pure; once per state change; at most 2 ms P95 at 4x throttling
  readonly layout: SceneNode<SceneSrc<C, K, A, V, D>, A, V>;
  answer(config: C, s: WidgetState<A, V>, d: D): Answer | null;
  describe: { brief: string; full?: string };                // templates over {c.*}, {k.*}, {a.*}, {v.*}, {d.*}; node phrases are appended
  exports?: readonly PathOf<{ d: D }>[];                     // template values content may use
  recipes?: Record<string, DeclarativeRecipe | ((config: C, s: WidgetState<A, V>, args: Record<string, Json>) => MotionStep[])>;
  secret?(config: C, s: WidgetState<A, V>, d: D): string | null;
  solved?(config: C, s: WidgetState<A, V>, key: Json): WidgetState<A, V>;
  migrate?: WidgetLogic<C, A, V>['migrate'];
  overrides?: Partial<Pick<WidgetLogic<C, A, V>, 'dirty' | 'summarise' | 'marks' | 'predicates' | 'targets' | 'table' | 'tryValue' | 'resolvers' | 'elementMeta'>>;   // at most 3
}
