// src/engine/scope.ts against docs/ARCHITECTURE.md 5.1, with the stage 3 leak test: no callback after its
// scope or an ancestor is disposed, and nothing left pending.
import { signal } from '@preact/signals-core';
import fc from 'fast-check';
import { afterEach, beforeEach, describe, expect, test, vi } from 'vitest';
import { createScope, type FrameSource } from './scope.ts';

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

  test("effect passes signals' this through, and a first run that disposes the scope or throws leaves nothing", () => {
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
    scope.effect(() => {
      runs += s.value;
      scope.dispose();
    });
    s.value = 5;
    expect(runs).toBe(2);
  });

  test('dispose aborts the signal, then releases in reverse order of registration, children included', () => {
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

  test('a child disposed first leaves its parent, and is not released again', () => {
    const scope = createScope(frames);
    const kid = scope.child();
    const grandchild = kid.child();
    let releases = 0;
    grandchild.own(() => releases++);
    kid.dispose();
    expect([kid.disposed, grandchild.disposed, scope.disposed]).toEqual([true, true, false]);
    scope.dispose();
    expect(releases).toBe(1);
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
// events, signal writes and disposals, against a model of which scopes are disposed.
type Kind = 'later' | 'every' | 'frame' | 'loop' | 'listen' | 'once' | 'effect' | 'own';
type Op =
  | { op: 'reg'; kind: Kind; at: number; ms: number }
  | { op: 'child'; at: number }
  | { op: 'dispose'; at: number }
  | { op: 'cancel'; at: number }
  | { op: 'advance'; ms: number }
  | { op: 'tick' }
  | { op: 'event' }
  | { op: 'write' };

const at = fc.nat(30);
const item = <T>(list: readonly T[], i: number): T => {
  const value = list[i];
  if (value === undefined) throw new RangeError(`no item ${i}`);
  return value;
};
const ops = fc.array(
  fc.oneof(
    {
      arbitrary: fc.record({
        op: fc.constant('reg' as const),
        kind: fc.constantFrom<Kind>('later', 'every', 'frame', 'loop', 'listen', 'once', 'effect', 'own'),
        at,
        ms: fc.integer({ min: 1, max: 40 }),
      }),
      weight: 4,
    },
    fc.record({ op: fc.constantFrom('child' as const, 'dispose' as const, 'cancel' as const), at }),
    fc.record({ op: fc.constant('advance' as const), ms: fc.integer({ min: 0, max: 60 }) }),
    fc.record({ op: fc.constantFrom('tick' as const, 'event' as const, 'write' as const) }),
  ),
  { maxLength: 60 },
);

test('no callback runs after its scope or an ancestor is disposed, and nothing is left pending', () => {
  fc.assert(
    fc.property(ops, (list: Op[]) => {
      vi.clearAllTimers();
      const clock = new FakeFrames();
      const target = new FakeTarget();
      const s = signal(0);
      const root = createScope(clock);
      const scopes = [{ scope: root, parent: -1, disposed: false }];
      const regs: { scope: number; cancel?: () => void; cancelled: boolean }[] = [];
      const violations: string[] = [];
      const owned: number[] = [];
      let liveEffects = 0;
      const dead = (i: number): boolean => {
        const node = scopes[i];
        return node !== undefined && (node.disposed || dead(node.parent)); // the root's parent is -1
      };
      const dispose = (i: number) => {
        const node = item(scopes, i);
        node.disposed = true; // before the call, so a callback the release triggers counts as late
        node.scope.dispose();
      };
      for (const step of list) {
        if (step.op === 'advance') vi.advanceTimersByTime(step.ms);
        else if (step.op === 'tick') clock.tick();
        else if (step.op === 'event') target.dispatchEvent(new Event('ping'));
        else if (step.op === 'write') s.value++;
        else if (step.op === 'cancel') {
          const reg = regs[step.at % Math.max(regs.length, 1)];
          if (reg?.cancel) {
            reg.cancelled = true;
            reg.cancel();
          }
        } else {
          const index = step.at % scopes.length;
          const { scope } = item(scopes, index);
          if (step.op === 'dispose') dispose(index);
          else if (dead(index)) expect(() => scope.child()).toThrow(/disposed/);
          else if (step.op === 'child') scopes.push({ scope: scope.child(), parent: index, disposed: false });
          else {
            const reg: (typeof regs)[number] = { scope: index, cancelled: false };
            const r = regs.push(reg) - 1;
            const note = () => {
              if (reg.cancelled || dead(index)) violations.push(`${step.kind} ${r}`);
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
                if (s.value >= 0) note(); // reading s subscribes the effect
                liveEffects++;
                return () => {
                  liveEffects--;
                };
              });
            else
              scope.own(() => {
                if (!dead(index)) violations.push(`own ${r} early`);
                owned[r] = (owned[r] ?? 0) + 1;
              });
            if (step.kind === 'own') owned[r] ??= 0;
          }
        }
      }
      dispose(0);
      const pending = [vi.getTimerCount(), clock.pending.size, target.listeners.size, liveEffects];
      expect(pending).toEqual([0, 0, 0, 0]);
      vi.advanceTimersByTime(1_000);
      clock.tick();
      target.dispatchEvent(new Event('ping'));
      s.value++;
      expect(violations).toEqual([]);
      expect(owned.filter((n) => n !== 1)).toEqual([]);
      expect(scopes.every(({ scope }) => scope.disposed && scope.signal.aborted)).toBe(true);
    }),
    { numRuns: 1_000 },
  );
});
