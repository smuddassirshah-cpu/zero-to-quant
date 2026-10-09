// Compile-time tests of docs/ARCHITECTURE.md 5.14: typed paths, bindings, node kinds and a sample scene.
import type { Json } from '@zq/contracts/base';
import type * as s from '@zq/contracts/scene';
import type { BaseConfig } from '@zq/contracts/widget';
import { describe, expectTypeOf, test } from 'vitest';
import type { Words } from './types.ts';

type Deep = Readonly<{ a: { b: { c: { d: { e: { f: number } } } } }; list: { x: number }[] }>;
type Config = BaseConfig & Readonly<{ max: number }>;
type A = Readonly<{ theta: number }>;
type V = Readonly<{ zoom: number }>;
type D = Readonly<{ point: { x: number; y: number } }>;
type Src = s.SceneSrc<Config, null, A, V, D>;
type Node = s.SceneNode<Src, A, V>;

describe('scenes (5.14)', () => {
  test('PathOf: every dotted key path with its prefixes, at most five keys deep, arrays as values', () => {
    expectTypeOf<s.PathOf<Deep>>().toEqualTypeOf<Words<'a a.b a.b.c a.b.c.d a.b.c.d.e list'>>();
    expectTypeOf<'a.b.c.d.e.f'>().not.toExtend<s.PathOf<Deep>>();
    expectTypeOf<'list.0.x'>().not.toExtend<s.PathOf<Deep>>();
    expectTypeOf<Words<'c.max c.label k a.theta v.zoom d.point.x'>>().toExtend<s.PathOf<Src>>();
    expectTypeOf<'d.point.z'>().not.toExtend<s.PathOf<Src>>();
  });

  test('a binding is a path or a pure function of the sources; controls write only a and v', () => {
    expectTypeOf<'d.point.y'>().toExtend<s.Bind<Src, number>>();
    expectTypeOf<{ from: (src: Src) => boolean }>().toExtend<s.Bind<Src, boolean>>();
    expectTypeOf<{ from: (src: Src) => string }>().not.toExtend<s.Bind<Src, boolean>>();
    expectTypeOf<s.Write<Src, A, V, Json>['path']>().toEqualTypeOf<Words<'a a.theta v v.zoom'>>();
  });

  test('node kinds: the generic one takes every primitive and input but the three with kinds of their own', () => {
    expectTypeOf<s.PrimType>().toEqualTypeOf<
      | Words<'plot-2d drag-point slider number-line region-select token-tray'>
      | Words<'stepper sketch-pad cell-grid matrix plot-3d sim-runner chance-object mass-editor array-strip'>
      | Words<'node-link code-surface diff-view text-terminal speed-timer scratch-pad cashflow-timeline'>
      | Words<'price-ladder position-editor voice-capture span-track choice numeric-input expression-input'>
      | Words<'card-sort derivation-steps free-response order-ticket quote-entry'>
    >();
    expectTypeOf<{ id: 'm'; prim: 'marks'; props: Record<string, never> }>().not.toExtend<Node>();
    expectTypeOf<{ id: 'm'; prim: 'marks'; type: 'curve'; data: 'd.point' }>().not.toExtend<Node>(); // MarkType is opaque
    expectTypeOf<{ id: 'f'; embed: 'unit-circle'; config: 'c'; state: 'a' }>().not.toExtend<Node>(); // pinned type@v
  });

  test('a scene written as data types without a cast', () => {
    const scene = {
      type: 'angle-demo',
      v: 1,
      cluster: 'precalc',
      answers: ['numeric'],
      stateVersion: 1,
      tweenable: ['zoom'],
      init: () => ({ a: { theta: 0 }, v: { zoom: 1 } }),
      derive: (_c, _k, st) => ({ point: { x: st.a.theta, y: st.v.zoom } }),
      layout: {
        layout: 'column',
        children: [
          { id: 'turn', prim: 'slider', props: { min: 0, max: 'c.max' }, writes: { path: 'a.theta' } },
          { id: 'f', prim: 'live-formula', tex: '\\theta = {a}', slots: { a: 'a.theta' } },
          { id: 'inner', embed: 'unit-circle@1', config: { from: (src) => src.c.max }, state: 'v' },
        ],
      },
      answer: (_c, st) => ({ type: 'numeric', raw: String(st.a.theta) }),
      describe: { brief: 'Angle {a.theta}.' },
      exports: ['d.point.x'],
    } satisfies s.SceneDef<Config, null, A, V, D>;
    expectTypeOf(scene.layout.children).items.toExtend<Node>();
    expectTypeOf<s.SceneDef<Config, null, A, V, D>['exports']>().toEqualTypeOf<
      readonly Words<'d d.point d.point.x d.point.y'>[] | undefined
    >();
  });
});
