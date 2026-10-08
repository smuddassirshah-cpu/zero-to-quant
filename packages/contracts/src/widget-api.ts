/*
 * What a widget view receives (docs/ARCHITECTURE.md 5.3, second listing), implemented by
 * src/engine/widgets/host.tsx; everything stateful is the host's.
 * Decision notes:
 * - preact and @preact/signals-core are imported as types only (5.3; eslint.config.js enforces it).
 * - `WidgetServices` carries `cas` and `mathfield`. Its `tex: TexService` (5.11), `python: PythonRuntime`
 *   and `sql: SqlRuntime` (5.9) join with the unit that transcribes 5.9 and 5.11; `TexService` is declared
 *   in src/engine/render, which this package may not import (4.5), so its interface must move here first.
 * - `CasService` is declared in answer.ts, which `GradeCtx` needs without the DOM lib, and re-exported here.
 */
import type { ReadonlySignal } from '@preact/signals-core';
import type { Ref } from 'preact';
import type { CasService } from './answer.ts';
import type { ElementId, HighlightStyle, Json, Mark, Scope, SeedSource } from './base.ts';
import type {
  BaseConfig,
  ClusterId,
  MotionMode,
  PresetDef,
  WidgetMode,
  WidgetModule,
  WidgetState,
} from './widget.ts';

export type { CasService };

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
  load(type: string, v: number): Promise<WidgetModule<BaseConfig, Json, Json>>; // imports the cluster chunk once per session
  preset(ref: `${string}@${number}`): Promise<PresetRuntime | null>; // the preset's runtime parts, from its own cluster chunk; null if unknown
  preload(clusters: readonly ClusterId[]): Promise<void>;
}
/** A preset at run time: `expand` is compile-only and is not bundled. */
export type PresetRuntime = Pick<
  PresetDef<BaseConfig, BaseConfig>,
  'type' | 'v' | 'predicates' | 'recipes' | 'describeAs'
>;
/** Services the host injects; 5.3 also lists tex, python and sql (see the decision notes). */
export interface WidgetServices {
  cas: (() => Promise<CasService>) | null; // only when logic.needs includes 'cas'
  mathfield: (() => Promise<MathfieldService>) | null;
}
