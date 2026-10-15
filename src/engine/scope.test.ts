// src/engine/scope.ts against docs/ARCHITECTURE.md 5.1, with the stage 3 leak test: no callback after its
// scope or an ancestor is disposed, every live one still runs, and nothing is left pending or reachable.
import { signal } from '@preact/signals-core';
import type { Scope } from '@zq/contracts/base';
import fc from 'fast-check';
import { afterEach, beforeEach, describe, expect, test, vi } from 'vitest';
import { createScope, type FrameSource } from './scope.ts';

// node:v8's queryObjects counts the objects with a constructor's prototype on their chain "in the heap
// after a full garbage collection, which can be useful for memory leak regression tests" [sourced:
// @types/node 22.20.5, v8.d.ts; experimental in Node 22]. src/ carries no Node types (src/tsconfig.json), so
// the module is imported by a computed name and given the one signature used here.
type Ctor = abstract new (...args: never[]) => unknown;
const v8 = 'node:v8';
const { queryObjects } = (await import(v8)) as {
  queryObjects: (ctor: Ctor, o: { format: 'count' }) => number;
};
const reachable = (ctor: Ctor) => queryObjects(ctor, { format: 'count' });

/** Frames on a fake clock. A tick runs the whole batch it took, even an entry cancelled mid-batch (harsher than rAF). */
class FakeFrames implements FrameSource {
  readonly pending = new Map<number, (t: number) => void>();
  #next = 0;
  now = 0;
  request(fn: (t: number) => void) {
    this.pending.set(++this.#next, fn);
    return this.#next;
  }
  cancel(handle: number) {
    this.pending.delete(handle);
  }
  tick(ms = 16) {
    this.now += ms;
    const batch = [...this.pending.values()];
    this.pending.clear();
    for (const fn of batch) fn(this.now);
  }
}

/** An EventTarget that counts its listeners, honouring `once`. */
class FakeTarget implements EventTarget {
  readonly listeners = new Map<EventListenerOrEventListenerObject, boolean>();
  addEventListener(
    _: string,
    fn: EventListenerOrEventListenerObject | null,
    o?: AddEventListenerOptions | boolean,
  ) {
    if (fn) this.listeners.set(fn, typeof o === 'object' && o.once === true);
  }
  removeEventListener(_: string, fn: EventListenerOrEventListenerObject | null) {
    if (fn) this.listeners.delete(fn);
  }
  dispatchEvent(e: Event) {
    for (const [fn, once] of [...this.listeners]) {
      if (once) this.listeners.delete(fn);
      if (typeof fn === 'function') fn(e);
    }
    return true;
  }
}

/** A marker that a callback's closure holds, so `reachable(Held)` counts the callbacks still kept. */
class Held {
  readonly mark: string = 'held';
}
/** A callback holding a fresh Held. It returns false, so a loop given it ends after its first frame. */
const holding = () => {
  const held = new Held();
  return () => held.mark === '';
};

let frames: FakeFrames;
beforeEach(() => {
  vi.useFakeTimers();
  frames = new FakeFrames();
});
afterEach(() => {
  vi.unstubAllGlobals(); // first, so a stubbed clearTimeout cannot outlive the fake timers
  vi.useRealTimers();
});

describe('timers and frames', () => {
  test('later runs once after its delay; a cancel before it, or a second cancel, does nothing more', () => {
    const scope = createScope(frames);
    const runs: string[] = [];
    scope.later(() => runs.push('a'), 10);
    const cancel = scope.later(() => runs.push('b'), 10);
    cancel();
    cancel();
    expect(vi.getTimerCount()).toBe(1);
    vi.advanceTimersByTime(9);
    expect(runs).toEqual([]);
    vi.advanceTimersByTime(1);
    expect(runs).toEqual(['a']);
    expect(vi.getTimerCount()).toBe(0);
  });

  test('every repeats until cancelled', () => {
    const scope = createScope(frames);
    let runs = 0;
    const cancel = scope.every(() => runs++, 5);
    vi.advanceTimersByTime(16);
    cancel();
    vi.advanceTimersByTime(50);
    expect(runs).toBe(3);
    expect(vi.getTimerCount()).toBe(0);
  });

  test('frame runs once with the frame time; one cancelled while queued never runs', () => {
    const scope = createScope(frames);
    const seen: number[] = [];
    let cancel: () => void = () => undefined;
    scope.frame((t) => {
      seen.push(t);
      cancel();
    });
    scope.frame(() => seen.push(-2))();
    expect(frames.pending.size).toBe(1);
    cancel = scope.frame(() => seen.push(-1));
    frames.tick();
    frames.tick();
    expect(seen).toEqual([16]);
    expect(frames.pending.size).toBe(0);
  });

  test('loop runs each frame while fn returns true, with dt 0 first, and stops on false or cancel', () => {
    const scope = createScope(frames);
    const calls: [number, number][] = [];
    scope.loop((t, dt) => calls.push([t, dt]) < 3);
    for (let i = 0; i < 5; i++) frames.tick(10);
    expect(calls).toEqual([
      [10, 0],
      [20, 10],
      [30, 10],
    ]);
    const cancel: () => void = scope.loop(() => {
      cancel();
      return true;
    });
    frames.tick();
    expect(frames.pending.size).toBe(0);
    scope.loop(() => true);
    scope.dispose();
    expect(frames.pending.size).toBe(0);
  });

  test('a timer or frame the platform runs after its cancel or dispose still calls nothing', () => {
    vi.stubGlobal('clearTimeout', () => undefined);
    vi.stubGlobal('clearInterval', () => undefined);
    const scope = createScope(frames);
    let runs = 0;
    scope.later(() => runs++, 5)();
    scope.every(() => runs++, 5)();
    scope.later(() => runs++, 5);
    scope.frame(() => {
      stopLoop(); // the loop's tick is in this batch already
    });
    const stopLoop = scope.loop(() => runs++ >= 0);
    frames.tick();
    scope.dispose();
    vi.advanceTimersByTime(20);
    expect(runs).toBe(0);
    vi.clearAllTimers();
  });

  test('the default source is requestAnimationFrame, and without one frames are a development error', () => {
    const scope = createScope();
    expect(() => scope.frame(() => undefined)).toThrow(/requestAnimationFrame/);
    expect(() => scope.loop(() => true)).toThrow(/requestAnimationFrame/);
    const fake = new FakeFrames();
    vi.stubGlobal('requestAnimationFrame', fake.request.bind(fake));
    vi.stubGlobal('cancelAnimationFrame', fake.cancel.bind(fake));
    const seen: number[] = [];
    scope.frame((t) => seen.push(t));
    scope.frame(() => seen.push(-1))();
    fake.tick(5);
    expect(seen).toEqual([5]);
    scope.loop(() => true);
    scope.dispose();
    expect(fake.pending.size).toBe(0);
  });
});

describe('listeners, effects and owned disposers', () => {
  test('listen adds the listener with its options and removes it on dispose, capture included', () => {
    const scope = createScope(frames);
    const target = new EventTarget();
    const seen: string[] = [];
    scope.listen(target, 'x', () => seen.push('bubble'));
    scope.listen(target, 'x', () => seen.push('capture'), { capture: true });
    scope.listen(target, 'x', () => seen.push('once'), { once: true });
    target.dispatchEvent(new Event('x'));
    target.dispatchEvent(new Event('x'));
    const remove = vi.spyOn(target, 'removeEventListener');
    scope.dispose();
    target.dispatchEvent(new Event('x'));
    expect(seen).toEqual(['bubble', 'capture', 'once', 'bubble', 'capture']);
    expect(remove.mock.calls.map((call) => call[2])).toEqual([true, false]); // the fired once is gone
  });

  test('an event a disposer dispatches while the scope is released reaches no listener of it', () => {
    const scope = createScope(frames);
    const target = new FakeTarget();
    const seen: string[] = [];
    scope.listen(target, 'x', () => seen.push('heard'));
    scope.own(() => target.dispatchEvent(new Event('x')));
    scope.dispose();
    expect(seen).toEqual([]);
    expect(target.listeners.size).toBe(0);
  });

  test('effect runs, re-runs on a change, cleans up on dispose and never runs after it', () => {
    const scope = createScope(frames);
    const s = signal(0);
    const log: string[] = [];
    scope.effect(() => {
      log.push(`run ${s.value}`);
      return () => log.push('cleanup');
    });
    s.value = 1;
    scope.own(() => {
      s.value = 2; // during release, before the effect stops
    });
    scope.dispose();
    s.value = 3;
    expect(log).toEqual(['run 0', 'cleanup', 'run 1', 'cleanup']);
  });

  test("effect passes signals' this through; a first run that throws, or disposes its scope or an ancestor, stops it", () => {
    const scope = createScope(frames);
    const s = signal(0);
    let runs = 0;
    scope.effect(function (this: { dispose: () => void }) {
      runs += s.value + 1;
      this.dispose();
    });
    s.value = 1;
    expect(runs).toBe(1);
    expect(() => {
      scope.effect(() => {
        throw new RangeError('first run');
      });
    }).toThrow(RangeError);
    const log: string[] = [];
    const kid = scope.child();
    kid.effect(() => {
      log.push(`own ${s.value}`);
      kid.dispose();
      return () => log.push('own cleanup');
    });
    scope.child().effect(() => {
      log.push(`ancestor ${s.value}`);
      scope.dispose();
      return () => log.push('ancestor cleanup');
    });
    // Each cleanup ran before effect() returned, with no signal write to prompt it.
    expect(log).toEqual(['own 1', 'own cleanup', 'ancestor 1', 'ancestor cleanup']);
    s.value = 5;
    expect(log).toHaveLength(4);
    expect(scope.disposed).toBe(true);
  });

  test('dispose aborts the signal, then releases in reverse order; a child aborts as its own release starts', () => {
    const scope = createScope(frames);
    const order: string[] = [];
    scope.signal.addEventListener('abort', () => order.push('abort'));
    scope.own(() => order.push('first'));
    const kid = scope.child();
    kid.own(() => order.push('kid'));
    scope.own(() => {
      order.push(`last, kid disposed ${kid.disposed}, kid aborted ${kid.signal.aborted}`);
    });
    scope.dispose();
    scope.dispose();
    expect(order).toEqual(['abort', 'last, kid disposed true, kid aborted false', 'kid', 'first']);
    expect([scope.disposed, kid.signal.aborted]).toEqual([true, true]);
  });

  test("what an effect's first run registers is released before the effect stops", () => {
    const scope = createScope(frames);
    const order: string[] = [];
    scope.own(() => order.push('before'));
    scope.effect(() => {
      scope.own(() => order.push('made in the first run'));
      return () => order.push('effect cleanup');
    });
    scope.own(() => order.push('after'));
    scope.dispose();
    expect(order).toEqual(['after', 'made in the first run', 'effect cleanup', 'before']);
  });

  test("a screen's scope disposed under a live root stops all of its subtree and none of the root", () => {
    const root = createScope(frames);
    const target = new FakeTarget();
    const s = signal(0);
    const heard: string[] = [];
    const fill = (scope: Scope, name: string) => {
      scope.later(() => heard.push(`${name} later`), 5);
      scope.every(() => heard.push(`${name} every`), 5);
      scope.frame(() => heard.push(`${name} frame`));
      scope.loop(() => heard.push(`${name} loop`) > 0);
      scope.listen(target, 'x', () => heard.push(`${name} listen`));
      scope.listen(target, 'x', () => heard.push(`${name} once`), { once: true });
      scope.effect(() => {
        heard.push(`${name} effect ${s.value}`);
      });
    };
    const screen = root.child();
    fill(root, 'root');
    fill(screen, 'screen');
    fill(screen.child(), 'widget');
    heard.length = 0; // the effects' first runs
    screen.dispose();
    vi.advanceTimersByTime(5);
    frames.tick();
    target.dispatchEvent(new Event('x'));
    s.value = 1;
    expect(heard).toEqual([
      'root later',
      'root every',
      'root frame',
      'root loop',
      'root listen',
      'root once',
      'root effect 1',
    ]);
    expect([vi.getTimerCount(), frames.pending.size, target.listeners.size]).toEqual([1, 1, 1]);
    root.dispose();
    expect([vi.getTimerCount(), frames.pending.size, target.listeners.size]).toEqual([0, 0, 0]);
  });

  // Helpers do the registering, so no frame of a test holds what they make.
  test('a disposed child leaves its parent, keeps no descendant, and is not released again', () => {
    const scope = createScope(frames);
    const node = (Object.getPrototypeOf(scope) as { constructor: Ctor }).constructor;
    const base = reachable(node);
    const kept: Scope[] = [];
    const churn = (keep: boolean) => {
      for (let i = 0; i < 8; i++) {
        const kid = scope.child();
        kid.child().own(() => undefined);
        kid.dispose();
        if (keep) kept.push(kid);
      }
    };
    churn(false);
    expect(reachable(node)).toBe(base); // neither the parent's children nor its entries keep them
    churn(true);
    expect(reachable(node)).toBe(base + kept.length); // and a disposed child keeps no descendant
    const kid = scope.child();
    const grandchild = kid.child();
    let releases = 0;
    grandchild.own(() => releases++);
    kid.dispose();
    expect([kid.disposed, grandchild.disposed, scope.disposed]).toEqual([true, true, false]);
    scope.dispose();
    expect(releases).toBe(1);
  });

  test('fired, finished and cancelled entries keep nothing, nor does a disposed scope still referenced', () => {
    const scope = createScope(frames);
    const target = new FakeTarget();
    const cancelled = () => {
      scope.later(holding(), 5)();
      scope.every(holding(), 5)();
      scope.frame(holding())();
      scope.loop(holding())();
      const held = holding();
      expect(() => {
        scope.effect(() => {
          throw new RangeError(String(held()));
        });
      }).toThrow(RangeError);
    };
    const firing = () => {
      scope.later(holding(), 5);
      scope.frame(holding());
      scope.loop(holding());
      scope.listen(target, 'x', holding(), { once: true });
    };
    const live = () => {
      scope.every(holding(), 5);
      scope.listen(target, 'x', holding());
      scope.own(holding());
      const held = holding();
      scope.child().effect(() => {
        held();
      });
    };
    cancelled();
    expect(reachable(Held)).toBe(0);
    firing();
    expect(reachable(Held)).toBe(4);
    vi.advanceTimersByTime(5);
    frames.tick();
    target.dispatchEvent(new Event('x'));
    expect(reachable(Held)).toBe(0);
    live();
    expect(reachable(Held)).toBe(4);
    scope.dispose();
    expect(reachable(Held)).toBe(0);
  });
});

describe('errors', () => {
  test('one throwing disposer is rethrown as itself after the rest have run', () => {
    const scope = createScope(frames);
    const ran: number[] = [];
    const boom = new RangeError('one');
    scope.own(() => ran.push(1));
    scope.own(() => {
      throw boom;
    });
    expect(() => {
      scope.dispose();
    }).toThrow(boom);
    expect(ran).toEqual([1]);
  });

  test('several are rethrown as an AggregateError, a child holding its own', () => {
    const scope = createScope(frames);
    const kid = scope.child();
    const fail = (message: string) => () => {
      throw new Error(message);
    };
    kid.own(fail('kid a'));
    kid.own(fail('kid b'));
    scope.own(fail('parent'));
    let caught: unknown;
    try {
      scope.dispose();
    } catch (error) {
      caught = error;
    }
    expect(caught).toBeInstanceOf(AggregateError);
    const [parent, inner] = (caught as AggregateError).errors as [Error, AggregateError];
    expect(parent.message).toBe('parent');
    expect(inner.errors.map((e: Error) => e.message)).toEqual(['kid b', 'kid a']);
  });

  test('registering on a disposed scope, or from one of its disposers, throws', () => {
    const scope = createScope(frames);
    const kid = scope.child();
    const late: unknown[] = [];
    scope.own(() => {
      try {
        kid.own(() => undefined);
      } catch (error) {
        late.push(error);
      }
    });
    scope.dispose();
    expect(late).toHaveLength(1);
    const register: ((s: typeof scope) => unknown)[] = [
      (s) => s.later(() => undefined, 1),
      (s) => s.every(() => undefined, 1),
      (s) => s.frame(() => undefined),
      (s) => s.loop(() => true),
      (s) => {
        s.listen(new EventTarget(), 'x', () => undefined);
      },
      (s) => {
        s.effect(() => undefined);
      },
      (s) => {
        s.own(() => undefined);
      },
      (s) => s.child(),
    ];
    for (const r of register) expect(() => r(scope)).toThrow(/disposed/);
    expect(vi.getTimerCount() + frames.pending.size).toBe(0);
  });
});

// The leak test. Random interleavings of registrations, cancels, children, timer and frame advances,
// events, signal writes and disposals of sub-scopes, against a model of which scopes are disposed. The root
// goes last, as the app root outlives every screen's scope (ARCHITECTURE.md 5.4). A callback may itself
// dispose a sub-scope (`kill`, -1 for none): its own, an ancestor mid-release, or an unrelated one; an owned
// disposer with an odd `ms` writes the signal while its scope is released. Safety: no callback runs once
// cancelled or once its scope is dead. Liveness: before the root goes, each registration neither cancelled
// nor dead has run exactly as often as its triggers say, since a scope live at the end was live throughout.
type Kind = 'later' | 'every' | 'frame' | 'loop' | 'listen' | 'once' | 'effect' | 'own';
interface RegOp {
  op: 'reg';
  kind: Kind;
  at: number;
  ms: number;
  kill: number;
}
type Op =
  | RegOp
  | { op: 'child'; at: number }
  | { op: 'dispose'; at: number }
  | { op: 'cancel'; at: number }
  | { op: 'advance'; ms: number }
  | { op: 'tick' }
  | { op: 'event' }
  | { op: 'write' };
/** The model's clocks: ms advanced, frames ticked, events dispatched. */
interface Clocks {
  now: number;
  ticks: number;
  events: number;
}

const at = fc.nat(63);
const item = <T>(list: readonly T[], i: number): T => {
  const value = list[i];
  if (value === undefined) throw new RangeError(`no item ${i}`);
  return value;
};
// fast-check's default size caps an array at 10 items whatever maxLength says [measured, review of
// 15 October 2026]; 'max' lets the interleavings reach 60 ops.
const ops = fc.array(
  fc.oneof(
    {
      arbitrary: fc.record({
        op: fc.constant('reg' as const),
        kind: fc.constantFrom<Kind>('later', 'every', 'frame', 'loop', 'listen', 'once', 'effect', 'own'),
        at,
        ms: fc.integer({ min: 1, max: 40 }),
        kill: fc.oneof({ arbitrary: fc.constant(-1), weight: 4 }, at),
      }),
      weight: 4,
    },
    fc.record({ op: fc.constantFrom('child' as const, 'dispose' as const, 'cancel' as const), at }),
    fc.record({ op: fc.constant('advance' as const), ms: fc.integer({ min: 0, max: 60 }) }),
    fc.record({ op: fc.constantFrom('tick' as const, 'event' as const, 'write' as const) }),
  ),
  { maxLength: 60, size: 'max' },
);

const RUNS = 1_000;
// Runs that dispose a sub-scope holding a callback that could still run, then fire a trigger: 294 to 320
// of 1,000 in eight runs [measured, 15 October 2026], so the floor fails only when a change stops the
// generator reaching the case.
const EXERCISED_FLOOR = 200;

test(
  'no callback runs after its scope or an ancestor is disposed, each live one runs, and nothing is left pending',
  { timeout: 60_000 }, // about 1 s alone [measured]; the margin is for a loaded machine
  () => {
    let exercised = 0;
    fc.assert(
      fc.property(ops, (list: Op[]) => {
        vi.clearAllTimers();
        const clock = new FakeFrames();
        const target = new FakeTarget();
        const s = signal(0);
        const scopes = [{ scope: createScope(clock), parent: -1, disposed: false }];
        const regs: {
          kind: Kind;
          scope: number;
          ms: number;
          from: Clocks;
          cancel?: () => void;
          cancelled: boolean;
          calls: number;
          seen: number; // an effect's last read of s
        }[] = [];
        const violations: string[] = [];
        const clocks: Clocks = { now: 0, ticks: 0, events: 0 };
        let liveEffects = 0;
        const sub = { armed: false, hit: false }; // a sub-scope disposal over pending callbacks, then a trigger
        const dead = (i: number): boolean => {
          const node = scopes[i];
          return node !== undefined && (node.disposed || dead(node.parent)); // the root's parent is -1
        };
        const under = (i: number, top: number): boolean =>
          i >= 0 && (i === top || under(item(scopes, i).parent, top));
        // Whether a trigger could still run the registration's callback.
        const pending = (r: (typeof regs)[number]): boolean => {
          if (r.cancelled || dead(r.scope) || r.kind === 'own') return false;
          if (r.kind === 'later' || r.kind === 'frame' || r.kind === 'once') return r.calls === 0;
          return r.kind !== 'loop' || r.calls <= r.ms % 4;
        };
        const dispose = (i: number) => {
          if (i > 0 && !dead(i) && regs.some((r) => under(r.scope, i) && pending(r))) sub.armed = true;
          const node = item(scopes, i);
          node.disposed = true; // before the call, so a callback the release triggers counts as late
          node.scope.dispose();
        };
        const disposeSub = (n: number) => {
          if (scopes.length > 1) dispose(1 + (n % (scopes.length - 1)));
        };
        const register = (step: RegOp, index: number, scope: Scope) => {
          const reg: (typeof regs)[number] = {
            kind: step.kind,
            scope: index,
            ms: step.ms,
            from: { ...clocks },
            cancelled: false,
            calls: 0,
            seen: -1,
          };
          const name = `${step.kind} ${regs.push(reg) - 1}`;
          const note = () => {
            reg.calls++;
            if (reg.cancelled || dead(index)) violations.push(name);
            if (step.kill >= 0) disposeSub(step.kill);
          };
          let left = step.ms % 4;
          if (step.kind === 'later') reg.cancel = scope.later(note, step.ms);
          else if (step.kind === 'every') reg.cancel = scope.every(note, step.ms);
          else if (step.kind === 'frame') reg.cancel = scope.frame(note);
          else if (step.kind === 'loop')
            reg.cancel = scope.loop(() => {
              note();
              return left-- > 0;
            });
          else if (step.kind === 'listen' || step.kind === 'once')
            scope.listen(target, 'ping', note, { once: step.kind === 'once' });
          else if (step.kind === 'effect')
            scope.effect(() => {
              reg.seen = s.value; // reading s subscribes the effect
              note();
              liveEffects++;
              return () => {
                liveEffects--;
              };
            });
          else
            scope.own(() => {
              reg.calls++;
              if (!dead(index)) violations.push(`${name} early`);
              if (step.ms % 2 === 1) s.value++;
              if (step.kill >= 0) disposeSub(step.kill);
            });
        };
        for (const step of list) {
          if (step.op === 'advance' || step.op === 'tick' || step.op === 'event' || step.op === 'write') {
            if (step.op !== 'advance' || step.ms > 0) sub.hit ||= sub.armed;
            if (step.op === 'advance') {
              clocks.now += step.ms;
              vi.advanceTimersByTime(step.ms);
            } else if (step.op === 'tick') {
              clocks.ticks++;
              clock.tick();
            } else if (step.op === 'event') {
              clocks.events++;
              target.dispatchEvent(new Event('ping'));
            } else s.value++;
          } else if (step.op === 'cancel') {
            const reg = regs[step.at % Math.max(regs.length, 1)];
            if (reg?.cancel) {
              reg.cancelled = true;
              reg.cancel();
            }
          } else if (step.op === 'dispose') disposeSub(step.at);
          else {
            const index = step.at % scopes.length;
            const { scope } = item(scopes, index);
            if (dead(index)) expect(() => scope.child()).toThrow(/disposed/);
            else if (step.op === 'child')
              scopes.push({ scope: scope.child(), parent: index, disposed: false });
            else register(step, index, scope);
          }
        }
        const expected = ({ kind, ms, from }: (typeof regs)[number]): number => {
          const elapsed = clocks.now - from.now;
          const ticks = clocks.ticks - from.ticks;
          const events = clocks.events - from.events;
          if (kind === 'later') return elapsed >= ms ? 1 : 0;
          if (kind === 'every') return Math.floor(elapsed / ms);
          if (kind === 'frame') return Math.min(1, ticks);
          if (kind === 'loop') return Math.min((ms % 4) + 1, ticks);
          if (kind === 'listen') return events;
          if (kind === 'once') return Math.min(1, events);
          return kind === 'effect' ? 1 : 0; // an effect's re-runs are checked through `seen`
        };
        const stalled = regs.flatMap((r, i) => {
          if (r.cancelled || dead(r.scope)) return [];
          const ok = r.kind === 'effect' ? r.calls >= 1 && r.seen === s.value : r.calls === expected(r);
          return ok ? [] : [`${r.kind} ${i} ran ${r.calls}`];
        });
        expect(stalled).toEqual([]);
        dispose(0);
        const left = [vi.getTimerCount(), clock.pending.size, target.listeners.size, liveEffects];
        expect(left).toEqual([0, 0, 0, 0]);
        vi.advanceTimersByTime(1_000);
        clock.tick();
        target.dispatchEvent(new Event('ping'));
        s.value++;
        expect(violations).toEqual([]);
        expect(regs.filter((r) => r.kind === 'own' && r.calls !== 1)).toEqual([]);
        expect(scopes.every(({ scope }) => scope.disposed && scope.signal.aborted)).toBe(true);
        if (sub.hit) exercised++;
      }),
      { numRuns: RUNS },
    );
    expect(exercised).toBeGreaterThanOrEqual(EXERCISED_FLOOR);
  },
);
