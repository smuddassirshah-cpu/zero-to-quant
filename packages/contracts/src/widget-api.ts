/*
 * The view half of the widget contract (docs/ARCHITECTURE.md 5.3): the second listing, what a widget view
 * receives, implemented by src/engine/widgets/host.tsx; everything stateful is the host's.
 * Decision notes:
 * - preact and @preact/signals-core are imported as types only (5.3; eslint.config.js enforces it).
 * - `WidgetViewProps`, `WidgetView` and `WidgetModule` come from 5.3's first listing (widget.ts there): they
 *   name `VNode` and `WidgetApi`, and preact's types bring the DOM lib with them, so they stay out of the
 *   pure widget.ts that @zq/compiler reads (see its decision notes).
 * - `WidgetServices.tex` is `TexService` from render.ts: 5.11 declares it in src/engine/render, which this
 *   package may not import (4.5). `python` and `sql` are 5.9's runtimes from platform.ts.
 * - The registry returns `AnyWidgetModule` and `PresetRuntime` picks from `AnyPresetDef`, where 5.3 writes
 *   `WidgetModule<BaseConfig, Json, Json>` and `PresetDef<BaseConfig, BaseConfig>`, which accept no concrete
 *   widget (widget.ts's decision notes); `View` is declared as a method for the same reason.
 * - `CasService` is declared in answer.ts, which `GradeCtx` needs without the DOM lib, and re-exported here.
 */
import type { ReadonlySignal } from '@preact/signals-core';
import type { Ref, VNode } from 'preact';
import type { CasService } from './answer.ts';
import type { ElementId, HighlightStyle, Json, Mark, Scope, SeedSource } from './base.ts';
import type { PythonRuntime, SqlRuntime } from './platform.ts';
import type { TexService } from './render.ts';
import type {
  AnyPresetDef,
  AnyWidgetLogic,
  BaseConfig,
  ClusterId,
  MotionMode,
  WidgetLogic,
  WidgetMode,
  WidgetState,
} from './widget.ts';

export type { CasService };

export interface WidgetViewProps<C extends BaseConfig, A extends Json, V extends Json> {
  config: C;
  api: WidgetApi<A, V>;
}
export type WidgetView<C extends BaseConfig, A extends Json, V extends Json> = (
  props: WidgetViewProps<C, A, V>,
) => VNode | null;
export interface WidgetModule<C extends BaseConfig, A extends Json, V extends Json> {
  logic: WidgetLogic<C, A, V>;
  View: WidgetView<C, A, V>;
}
/** `WidgetModule<BaseConfig, Json, Json>` as the registry holds it: every concrete module is assignable to it. */
export interface AnyWidgetModule {
  logic: AnyWidgetLogic;
  View: { m(props: WidgetViewProps<BaseConfig, Json, Json>): VNode | null }['m'];
}

export interface WidgetApi<A extends Json, V extends Json> {
  readonly state: ReadonlySignal<WidgetState<A, V>>; // read through useComputed only (2.5 rule 1)
  readonly locked: ReadonlySignal<boolean>; // evaluating, correct, revealed, graded quiz items, exam review
  readonly ghost: boolean; // true for the tutor's ghost copy: render read-only
  readonly mode: WidgetMode;
  readonly motion: ReadonlySignal<MotionMode>;
  readonly theme: ReadonlySignal<'light' | 'dark'>;
  readonly scope: Scope;
  readonly seed: SeedSource;
  readonly services: WidgetServices;

  change(update: (s: WidgetState<A, V>) => WidgetState<A, V>): void; // during a gesture; the first change engages Check
  commit(update?: (s: WidgetState<A, V>) => WidgetState<A, V>): void; // gesture end: action log, announcement, draft save, clears tutor marks
  view(update: (v: V) => V): void; // view-only change: never engages Check, never graded
  announce(text: string): void; // the screen's polite region, at most one message per 600 ms
  feedback(event: 'tap' | 'snap' | 'lift' | 'drop'): void; // sound and haptic through the platform
  el(id: ElementId): ElementProps; // spread onto every targetable element; the same object for the same id for the instance's life, so refs and bound signals never churn a render
}
export interface ElementProps {
  ref: Ref<Element>; // lets the overlay place badges, rings and notes
  'data-zq-id': string;
  'data-zq-mark': ReadonlySignal<Mark | undefined>; // bound signal: no re-render on grade
  'data-zq-hl': ReadonlySignal<HighlightStyle | undefined>;
}
/** MathLive, lazily loaded, fonts shared with KaTeX, sounds off. */
export interface MathfieldService {
  mount(
    el: HTMLElement,
    o: { value: string; onInput(latex: string): void },
  ): { set(latex: string): void; focus(): void; destroy(): void };
}
export interface WidgetRegistry {
  has(type: string, v: number): boolean;
  cluster(type: string, v: number): ClusterId;
  load(type: string, v: number): Promise<AnyWidgetModule>; // imports the cluster chunk once per session
  preset(ref: `${string}@${number}`): Promise<PresetRuntime | null>; // the preset's runtime parts, from its own cluster chunk; null if unknown
  preload(clusters: readonly ClusterId[]): Promise<void>;
}
/** A preset at run time: `expand` is compile-only and is not bundled. */
export type PresetRuntime = Pick<AnyPresetDef, 'type' | 'v' | 'predicates' | 'recipes' | 'describeAs'>;
export interface WidgetServices {
  tex: TexService; // section 5.11
  cas: (() => Promise<CasService>) | null; // only when logic.needs includes 'cas'
  mathfield: (() => Promise<MathfieldService>) | null;
  python: PythonRuntime | null; // only for widgets that declare 'python'
  sql: SqlRuntime | null;
}
